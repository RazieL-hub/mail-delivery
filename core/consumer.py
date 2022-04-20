import asyncio
import datetime
import json
import random

from aiokafka import AIOKafkaConsumer
from sqlalchemy import text

# from apps.report.querys import create_task
# from apps.report.schemas import ReportSchema
# from core.celery import celery_app
# from database.async_connect_postgres import Session


async def consume():
    consumer = AIOKafkaConsumer("test", bootstrap_servers="localhost:9093")
    last_timestamp = 0
    controller = {}
    await consumer.start()
    try:
        async for msg in consumer:
            q = datetime.datetime.utcfromtimestamp(msg.timestamp//1000).strftime('%Y-%m-%d %H:%M:%S')
            msg = json.loads(msg.value)
            controller.update({msg['user']: {msg['type_event']: [msg['data']]}})
            print(msg['user'])
            print(msg['type_event'])
            print(controller)


            # async with Session() as db:
                # query = text(create_task).bindparams(**ReportSchema().dict())
                # task = await db.execute(query)
                # await db.commit()
                # last_task = task.first()
                # task_name = "core.celery.send_report"
                # celery_app.send_task(task_name, args=[last_task.id],
                #                      eta=datetime.datetime.now() + datetime.timedelta(seconds=random.randrange(2)))
    except Exception as e:
        print(e)
    finally:
        await consumer.stop()


asyncio.run(consume())
