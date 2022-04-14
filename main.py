import datetime

from fastapi import FastAPI, Depends
from sqlalchemy import text

from apps.report.schemas import ReportSchema
from core.celery import celery_app
from database.async_connect_postgres import Session, get_session
from apps.report.querys import create_task

app = FastAPI()


@app.get("/")
async def root():
    return {'message': 'hello world'}


@app.get('/test_mailer_sent')
async def test_mailer_delivery(db: Session = Depends(get_session)):
    query = text(create_task).bindparams(**ReportSchema().dict())
    task = await db.execute(query)
    await db.commit()
    last_task = task.first()
    task_name = "core.celery.test_celery"
    celery_app.sent_report(task_name, args=[last_task.id],
                           eta=datetime.datetime.now() + datetime.timedelta(seconds=30))

    return {'message': 'Mailer delivery started'}
