import httpx
from celery import Celery
from sqlalchemy import text

from celery.schedules import crontab

from apps.events_config.querys import get_test_event_all, update_all_task
from database.sync_connect_postgres import SessionLocal
from apps.report.querys import update_task_status, get_task_query

celery_app = Celery("worker", backend="rpc://user:bitnami@rabbitmq:5672//",
                    broker="amqp://user:bitnami@rabbitmq:5672//")
celery_app.conf.update(task_track_started=True)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/1'), send_report_telegram)


@celery_app.task(acks_late=True)
def send_report_email():
    with SessionLocal() as db:
        db.execute(text(update_task_status).bindparams())
        db.commit()


@celery_app.task()
def send_report_telegram():
    with SessionLocal() as db:
        query = text(get_test_event_all).bindparams(status=False)
        cursor = db.execute(query)
        count = cursor.fetchall()
        if len(count) > 10:
            response = httpx.post(
                f"https://api.telegram.org/bot5161207966:AAHTqn3R15Y5DVp2ya6APh5hNGhr6G39Lw8/sendMessage?chat_id=-1001576623026&text={len(count)} соощений for user with id 99 I ETO POLNAYA JOPA POTOMU 4to NE ZNAU KAK Polu4it' COUNT IMENNO KAK ZNA$ENIE IZ COURSOR")
            query = text(update_all_task).bindparams(old_status=False, new_status=True)
            db.execute(query)
            db.commit()

        else:
            response = httpx.post(
                f"https://api.telegram.org/bot5161207966:AAHTqn3R15Y5DVp2ya6APh5hNGhr6G39Lw8/sendMessage?chat_id=-1001576623026&text={len(count)} сообщений ")
            query = text(update_all_task).bindparams(old_status=False, new_status=True)
            db.execute(query)
            db.commit()