import asyncio
import datetime
import json
import random

import aiokafka
from fastapi import FastAPI
from sqlalchemy import text

from api.v1 import v1_router
from apps.report.schemas import ReportSchema
from core.celery import celery_app
from database.async_connect_postgres import Session
from apps.report.querys import create_task, get_task_query

app = FastAPI()


async def start_consumer():
    loop = asyncio.get_event_loop()
    while True:
        consumer = aiokafka.AIOKafkaConsumer("test", loop=loop, bootstrap_servers="kafka:9092", )
        await consumer.start()
        try:
            async for msg in consumer:
                message = json.loads(msg.value)
                async with Session() as db:
                    query = text(create_task).bindparams(user_id=message['user_id'],
                                                         type_event=message['type_event'],
                                                         report_data=json.dumps(message['data']),
                                                         date_created=datetime.datetime.now(),
                                                         status=False)
                    await db.execute(query)
                    await db.commit()

                # async with Session() as db:
                #     query = text(create_task).bindparams(**ReportSchema().dict())
                #     task = await db.execute(query)
                #     await db.commit()
                #     last_task = task.first()
                #     message = json.loads(msg.value)
                #     if message['send_type'] == 'email':
                #         task_name = "core.celery.send_report_email"
                #         celery_app.send_task(task_name, args=[last_task.id],
                #                              eta=datetime.datetime.now() + datetime.timedelta(
                #                                  seconds=random.randrange(2)))
                #     elif message['send_type'] == 'telegram':
                #         task_name = 'core.celery.send_report_telegram'
        except Exception as e:
            print(222, e)
        finally:
            await consumer.stop()
            with open(file='finish_test.txt', mode='w') as file:
                file.write(str(datetime.datetime.now()))


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_consumer())


app.include_router(v1_router)


@app.get("/")
async def root():
    return {'message': 'hello world'}
