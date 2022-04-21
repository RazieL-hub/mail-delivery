from datetime import datetime, timedelta
from time import sleep, strptime

import httpx
from celery import Celery
from sqlalchemy import text

from celery.schedules import crontab

from apps.events_config.querys import update_last_send, get_type_event_and_last_send
from core.config import get_settings

from database.sync_connect_postgres import SessionLocal
from apps.report.querys import update_task_status, get_task_query, task_prepare_to_send, \
    count_messages_for_user_and_event

token = get_settings().bot_token
chat_id = get_settings().chat_id
payload = f"https://www.xeroxscanners.com/downloads/Manuals/XMSSD/PDF_Converter_Pro_Quick_Reference_Guide.RU.pdf"
api_telegram = f"https://api.telegram.org/bot{token}"
message_url = f"{api_telegram}/sendMessage?chat_id={chat_id}&text="
document_url = f"{api_telegram}/sendDocument"

celery_app = Celery("worker", backend="rpc://user:bitnami@rabbitmq:5672//",
                    broker="amqp://user:bitnami@rabbitmq:5672//")
celery_app.conf.update(task_track_started=True)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/10', ), send_report_telegram)


# @celery_app.task(acks_late=True)
# def send_report_email():
#     with SessionLocal() as db:
#         db.execute(text(update_task_status).bindparams())
#         db.commit()


@celery_app.task()
def send_report_telegram():
    """
    count_messages_for_user_and_event :   user_id, type_event_id, count(*), MIN(date_created), MAX(date_created)
    """
    with SessionLocal() as db:
        db.execute(task_prepare_to_send)
        cursor = db.execute(count_messages_for_user_and_event)
        count_msg = cursor.fetchall()
        for row in count_msg:
            if row[2] > 10:
                """UPDATE reports set status_send = true, prepare_message = false 
                where user_id = :user_id
                and type_event_id = :type_event_id
                and status_send = false
                and prepare_message = true"""
                db.execute(text(update_task_status).bindparams(user_id=row[0], type_event_id=row[1]))
                cursor = db.execute(text(get_type_event_and_last_send).bindparams(type_event_id=row[1]))
                event = cursor.fetchone()
                if (datetime.now() - event[1]) > timedelta(minutes=event[2]) and \
                        (event[3] < datetime.now().time() < event[4]):
                    httpx.post(
                        f"{message_url}Сообщений по типу событий {event[0]} с {row[3]} по {row[4]} "
                        f"было {row[2]}. Иди смотри журнал")
                    db.execute(text(update_last_send).bindparams(type_event_id=row[1], date_time=datetime.now()))

            if row[2] == 1:
                db.execute(text(update_task_status).bindparams(user_id=row[0], type_event_id=row[1]))
                cursor = db.execute(text(get_type_event_and_last_send).bindparams(type_event_id=row[1]))
                event = cursor.fetchone()
                if (datetime.now() - event[1]) > timedelta(minutes=event[2]) and \
                        (event[3] < datetime.now().time() < event[4]):
                    cursor = db.execute(text().bindparams)

        db.commit()