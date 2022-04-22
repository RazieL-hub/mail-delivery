import asyncio
import datetime
import json
import random

import aiokafka
from fastapi import FastAPI
from sqlalchemy import text

from api.v1 import v1_router
from apps.events_config.querys import get_event_config_query
from apps.report.schemas import ReportSchema
from core.celery import celery_app
from database.async_connect_postgres import Session
from apps.report.querys import create_task, get_task_query

app = FastAPI()


async def start_consumer():
    loop = asyncio.get_event_loop()
    while True:
        consumer = aiokafka.AIOKafkaConsumer("test", loop=loop, bootstrap_servers="mail_kafka:9092", )
        await consumer.start()
        try:
            async for msg in consumer:
                message = json.loads(msg.value)
                async with Session() as db:
                    query = text(get_event_config_query).bindparams(user_id=message['user_id'],
                                                                    type_event=message['type_event'])
                    cursor = await db.execute(query)
                    event = cursor.fetchone()
                    if event:
                        query = text(create_task).bindparams(user_id=message['user_id'],
                                                             type_event_id=event.id,
                                                             report_data=json.dumps(message['data']),
                                                             date_created=datetime.datetime.now(),
                                                             status_send=False)
                        await db.execute(query)
                        await db.commit()
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
