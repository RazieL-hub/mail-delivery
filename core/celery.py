import datetime

from celery import Celery
from sqlalchemy import text

from database.sync_connect_postgres import SessionLocal
from apps.report.querys import update_task_status

celery_app = Celery("worker", backend="rpc://user:bitnami@rabbitmq:5672//",
                    broker="amqp://user:bitnami@rabbitmq:5672//")
celery_app.conf.update(task_track_started=True)


@celery_app.task(acks_late=True)
def send_report_email(task_id: int):
    with SessionLocal() as db:
        db.execute(text(update_task_status).bindparams(task_id=task_id))
        db.commit()


def send_report_telegram(task_id: int):
    with SessionLocal() as db:
        db.execute(text(update_task_status).bindparams(task_id=task_id))
        db.commit()

