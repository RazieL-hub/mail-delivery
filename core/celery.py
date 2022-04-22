from datetime import datetime, timedelta
from time import sleep

import httpx
from celery import Celery
from sqlalchemy import text

from celery.schedules import crontab

from apps.events_config.querys import get_type_event_and_last_send
from core.config import get_settings

from database.sync_connect_postgres import SessionLocal
from apps.report.querys import update_task_status, count_messages_for_user_and_event, \
    all_reports_status_false, select_report

token = get_settings().bot_token
chat_id = get_settings().chat_id
payload = "https://www.xeroxscanners.com/downloads/Manuals/XMSSD/PDF_Converter_Pro_Quick_Reference_Guide.RU.pdf"
api_telegram = f"https://api.telegram.org/bot{token}"
message_url = f"{api_telegram}/sendMessage?chat_id={chat_id}&text="
document_url = f"{api_telegram}/sendDocument"

celery_app = Celery("worker", backend="rpc://user:bitnami@rabbitmq:5672//",
                    broker="amqp://user:bitnami@rabbitmq:5672//")
celery_app.conf.update(task_track_started=True)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/1', ), send_report_telegram)


@celery_app.task()
def send_one_message(type_event_id: int, user_id: int, reports_id: tuple):
    with SessionLocal() as db:
        cursor = db.execute(text(select_report).bindparams(type_event_id=type_event_id,
                                                           user_id=user_id,
                                                           reports_id=tuple(reports_id)))
        report = cursor.fetchone()
        cursor = db.execute(text(get_type_event_and_last_send).bindparams(type_event_id=type_event_id))
        event = cursor.fetchone()
        if (datetime.now() - event[1]) > timedelta(minutes=event[2]) \
                and (event[3] < datetime.now().time() < event[4]):
            if report[1]['text']:
                res_text = httpx.post(f"{message_url}Тут сообщение 1 и вот его текст:'{report[1]['text']}'")
                print(f"STATUS CODE send_one_message TEXT {res_text.status_code}")
            if report[1]['payload']:
                res_doc = httpx.post(f"{document_url}",
                                     data={'chat_id': chat_id, 'document': report[1]['payload']})
                print(f"STATUS CODE send_one_message DOC {res_doc.status_code}")
            db.execute(text(update_task_status).bindparams(user_id=user_id,
                                                           type_event_id=type_event_id, reports_id=tuple(reports_id)))
            db.commit()


@celery_app.task()
def send_group_message(type_event_id: int, user_id: int, reports_id: tuple):
    with SessionLocal() as db:
        cursor = db.execute(text(get_type_event_and_last_send).bindparams(type_event_id=type_event_id))
        event = cursor.fetchone()
        if (datetime.now() - event[1]) > timedelta(minutes=event[2]) \
                and (event[3] < datetime.now().time() < event[4]):
            msg = ''
            cursor = db.execute(text(select_report).bindparams(type_event_id=type_event_id,
                                                               user_id=user_id,
                                                               reports_id=tuple(reports_id)))
            reports = cursor.fetchall()
            for report in reports:
                msg = msg + report[1]['text'] + ' \n'

            res_text = httpx.post(f"{message_url}Сообщение 2 шаблон {msg}")
            print(f"STATUS CODE send_group_message TEXT {res_text.status_code}")
            for report in reports:
                if report[1]['payload']:
                    res_doc = httpx.post(f"{document_url}",
                                         data={'chat_id': chat_id, 'document': report[1]['payload']})
                    print(f"STATUS CODE send_group_message DOC {res_doc.status_code}")
                    sleep(0.7)
            db.execute(text(update_task_status).bindparams(user_id=user_id,
                                                           type_event_id=type_event_id, reports_id=tuple(reports_id)))
            db.commit()


@celery_app.task()
def send_briefing_message(type_event_id: int, user_id: int, reports_id: tuple, count_messages: int,
                          date_start: datetime, date_finish: datetime):
    with SessionLocal() as db:
        cursor = db.execute(text(get_type_event_and_last_send).bindparams(type_event_id=type_event_id))
        event = cursor.fetchone()
        if (datetime.now() - event[1]) > timedelta(minutes=event[2]) \
                and (event[3] < datetime.now().time() < event[4]):
            res_text = httpx.post(f"{message_url}Сообщений по типу событий {event[0]} с {date_start} по {date_finish} "
                       f"для пользователя {event[5]} было {count_messages}. Иди смотри журнал")
            print(f"STATUS CODE send_briefing_message TEXT {res_text.status_code}")
            db.execute(text(update_task_status).bindparams(user_id=user_id,
                                                           type_event_id=type_event_id, reports_id=tuple(reports_id)))
            sleep(0.7)
            db.commit()


@celery_app.task()
def send_report_telegram():
    with SessionLocal() as db:
        cursor = db.execute(all_reports_status_false)
        reports_id = cursor.fetchall()
        reports_id = tuple([number[0] for number in reports_id])
        cursor = db.execute(count_messages_for_user_and_event)
        count_messages = cursor.fetchall()

        for row in count_messages:
            if row[2] == 1:
                send_one_message.delay(type_event_id=row[1], user_id=row[0], reports_id=reports_id)
            if 1 < row[2] < 10:
                send_group_message.delay(type_event_id=row[1], user_id=row[0], reports_id=reports_id)
            if row[2] > 9:
                send_briefing_message.delay(type_event_id=row[1], user_id=row[0], reports_id=reports_id,
                                            count_messages=row[2], date_start=row[3], date_finish=row[4])
                db.commit()
