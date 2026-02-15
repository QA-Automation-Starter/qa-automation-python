# Kafka self-test: verifies broker connectivity and basic publish/consume
import time

from confluent_kafka import Consumer, Producer


def should_publish_and_consume() -> None:
    message = b"self-test-message"
    producer = Producer({'bootstrap.servers': 'localhost:9092'})
    producer.produce('selftest-topic', value=message)
    producer.flush(2)
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'self-test-group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False,
    })
    consumer.subscribe(['selftest-topic'])
    start = time.time()
    while time.time() - start < 5:
        msg = consumer.poll(0.5)
        if msg and not msg.error() and msg.value() == message:
            consumer.close()
            return
    consumer.close()
    raise AssertionError(
        "Kafka self-test failed: could not publish and consume message")
