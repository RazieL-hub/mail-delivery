import datetime
import random

from aiokafka import AIOKafkaConsumer
from sqlalchemy import text

from apps.report.querys import create_task
from apps.report.schemas import ReportSchema
from core.celery import celery_app
from database.async_connect_postgres import Session


async def consume(loop):
    consumer = AIOKafkaConsumer("test", loop=loop, bootstrap_servers="kafka:9092")  # ENV
    await consumer.start()
    try:
        async for msg in consumer:
            async with Session() as db:
                query = text(create_task).bindparams(**ReportSchema().dict())
                task = await db.execute(query)
                await db.commit()
                last_task = task.first()

                task_name = "core.celery.send_report"
                celery_app.send_task(task_name, args=[last_task.id],
                                     eta=datetime.datetime.now() + datetime.timedelta(seconds=random.randrange(2)))
    except Exception as e:
        print(e)
    finally:
        await consumer.stop()
#
#
# asyncio.run(consume())
