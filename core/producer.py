import json
import os
from asyncio import sleep
import random
from aiokafka import AIOKafkaProducer
import asyncio

from dotenv import load_dotenv

load_dotenv()


def json_serializer(data):
    return json.dumps(data).encode('utf-8')


events = ['test event 1', 'test event 2', 'test event 3', 'test event 4', 'test event 5', 'test event 6']

async def send_one():
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9093', value_serializer=json_serializer)
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        data = {
            "user_id": random.randint(1, 4),
            "type_event": random.choice(events),
            "data": {
                "text": f"Some text {random.randint(1, 100)}",
                "payload": f"some payload ......................."
            }
        }
        await producer.send_and_wait("test", data)
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()
        await sleep(3)


while True:
    asyncio.run(send_one())
