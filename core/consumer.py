from aiokafka import AIOKafkaConsumer
import asyncio
import json


async def consume():
    consumer = AIOKafkaConsumer('test', bootstrap_servers='localhost:9093')
    await consumer.start()
    try:
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, json.loads(msg.value), msg.timestamp)
    finally:
        await consumer.stop()


asyncio.run(consume())
