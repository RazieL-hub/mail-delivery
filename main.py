import asyncio
import datetime
import json
import logging
import random

import aiokafka
from fastapi import FastAPI, Depends
from sqlalchemy import text

from api.v1 import v1_router
from apps.report.schemas import ReportSchema
from core.celery import celery_app
from core.consumer import consume
from database.async_connect_postgres import Session, get_session
from apps.report.querys import create_task
number = 0
name = f"CONSUMER NAME {number}"
events = ['эксплуатационный мониторинг состояний приборов учета',
          'эксплуатационный мониторинг состояний УСПД и УКПКЭ',
          'эксплуатационный мониторинг состояний каналов связи',
          'эксплуатационный мониторинг состояний программного и аппаратного обеспечения',
          'регистрация', 'обработка критических событий']

titles = ['RANDOM TITLE 1', 'RANDOM TITLE 2', 'RANDOM TITLE 3', 'RANDOM TITLE 4', 'RANDOM TITLE 5', 'RANDOM TITLE 6']

data = [{
    'send_type': 'email',
    'parameters': {
        'emails': ['testemail@gmail.com', ],
        'title': random.choice(events),
        'text': f'{random.choice(titles)} {random.randrange(1, 100)}'
    }}, {
    'send_type': 'telegram',
    'parameters': {
        'chat_ids': ['-100........', ],
        'text': f'{random.choice(titles)} {random.randrange(1, 100)}'
    }}]

app = FastAPI()


async def start_consumer():
    loop = asyncio.get_event_loop()
    while True:
        consumer = aiokafka.AIOKafkaConsumer("test", loop=loop, bootstrap_servers="kafka:9092",)
        await consumer.start()
        try:

            async for msg in consumer:
                async with Session() as db:
                    query = text(create_task).bindparams(**ReportSchema().dict())
                    task = await db.execute(query)
                    await db.commit()
                    last_task = task.first()
                    message = json.loads(msg.value)
                    if message['send_type'] == 'email':
                        task_name = "core.celery.send_report_email"
                        celery_app.send_task(task_name, args=[last_task.id],
                                             eta=datetime.datetime.now() + datetime.timedelta(seconds=random.randrange(2)))
                    elif message['send_type'] == 'telegram':
                        task_name = 'core.celery.send_report_telegram'
        except Exception as e:
            print(222, e)
        finally:
            await consumer.stop()
            with open(file='finish_test.txt', mode='w') as file:
                file.write(str(datetime.datetime.now()))


@app.on_event("startup")
async def startup_event():
    workers = 4  # ENV
    for worker in range(workers):
        asyncio.create_task(start_consumer())


app.include_router(v1_router)

@app.get("/")
async def root():
    return {'message': 'hello world'}


@app.get('/test_mailer_sent')
async def test_mailer_delivery(db: Session = Depends(get_session)):
    # count = 0
    # with open(file='start_test.txt', mode='w') as file:
    #     file.write(str(datetime.datetime.now()))
    #
    # for i in range(150000):
    #     count += 1
    #     query = text(create_task).bindparams(**ReportSchema().dict())
    #     task = await db.execute(query)
    #     await db.commit()
    #     last_task = task.first()
    #     print(random.choice(data))
    #     task_name = "core.celery.send_report"
    #     celery_app.send_task(task_name, args=[last_task.id, count],
    #                          eta=datetime.datetime.now() + datetime.timedelta(seconds=random.randrange(2)))

    return {'message': 'Mailer delivery started'}
