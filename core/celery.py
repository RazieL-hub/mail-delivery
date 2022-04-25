from datetime import datetime, timedelta

import httpx
from celery import Celery
from sqlalchemy import text

from celery.schedules import crontab

from apps.events_config.querys import get_type_event_and_last_send, update_last_send
from core.config import get_settings

from database.sync_connect_postgres import SessionLocal
from apps.report.querys import update_task_status, count_messages_for_user_and_event, \
    all_reports_status_false, select_report

token = get_settings().bot_token
chat_id = get_settings().chat_id
payload = "https://www.xeroxscanners.com/downloads/Manuals/XMSSD/PDF_Converter_Pro_Quick_Reference_Guide.RU.pdf"
api_telegram = f"https://api.telegram.org/bot{token}"
message_url = f"{api_telegram}/sendMessage?chat_id={chat_id}&text="
celery_app = Celery("worker", backend="rpc://user:bitnami@rabbitmq:5672//",
                    broker="amqp://user:bitnami@rabbitmq:5672//")
celery_app.conf.update(task_track_started=True)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/1', ), send_report_telegram)


@celery_app.task(name='send_one_message', bind=True, max_retries=5, retry_jitter=True)
def send_one_message(self, type_event_id: int, user_id: int, reports_id: tuple):
    with SessionLocal() as db:
        cursor = db.execute(text(select_report).bindparams(type_event_id=type_event_id,
                                                           user_id=user_id,
                                                           reports_id=tuple(reports_id)))
        report = cursor.fetchone()
        cursor = db.execute(text(get_type_event_and_last_send).bindparams(type_event_id=type_event_id))
        event = cursor.fetchone()
        if (datetime.now() - event[1]) > timedelta(minutes=event[2]) \
                and (event[3] < datetime.now().time() < event[4]):
            msg = ''
            if report[1]['text']:
                msg += report[1]['text']
            if report[1]['payload']:
                msg += f" Ссылка на документ: {report[1]['payload']}"
                res_text = httpx.post(f"{message_url}{msg}'")
                print(f"STATUS CODE send_one_message TEXT {res_text.status_code}")
            db.execute(text(update_task_status).bindparams(user_id=user_id,
                                                           type_event_id=type_event_id,
                                                           reports_id=tuple(reports_id)))
            db.commit()


@celery_app.task(name='send_group_message', bind=True, max_retries=5, retry_jitter=True)
def send_group_message(self, type_event_id: int, user_id: int, reports_id: tuple):
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
                if report[1]['payload']:
                    msg += f"Ссылка на файл {report[1]['payload']}. \n"

            res_text = httpx.post(f"{message_url}{msg}")
            print(f"STATUS CODE send_group_message TEXT {res_text.status_code}")
            db.execute(text(update_task_status).bindparams(user_id=user_id,
                                                           type_event_id=type_event_id,
                                                           reports_id=tuple(reports_id)))
            db.commit()


@celery_app.task(name='send_briefing_message', bind=True, max_retries=5, retry_jitter=True)
def send_briefing_message(self, type_event_id: int, user_id: int, reports_id: tuple, count_messages: int,
                          date_start: datetime, date_finish: datetime):
    with SessionLocal() as db:
        cursor = db.execute(text(get_type_event_and_last_send).bindparams(type_event_id=type_event_id))
        event = cursor.fetchone()
        if (datetime.now() - event[1]) > timedelta(minutes=event[2]) \
                and (event[3] < datetime.now().time() < event[4]):
            res_text = httpx.post(f"{message_url}Сообщений по типу событий {event[0]} с {date_start} по "
                                  f"{date_finish} для пользователя {event[5]} было {count_messages}. "
                                  f"Иди смотри журнал")
            print(f"STATUS CODE send_briefing_message TEXT {res_text.status_code}")
            db.execute(text(update_task_status).bindparams(user_id=user_id,
                                                           type_event_id=type_event_id,
                                                           reports_id=tuple(reports_id)))
            db.execute(text(update_last_send).bindparams(type_event_id=type_event_id, date_time=datetime.now()))
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
