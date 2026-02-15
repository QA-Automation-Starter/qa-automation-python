# Kafka self-test: verifies broker connectivity and basic publish/consume
import time

import pytest
from confluent_kafka import Consumer, Producer


def _kafka_broker_available(bootstrap_servers: str) -> bool:
    try:
        p = Producer({'bootstrap.servers': bootstrap_servers})
        p.flush(0.5)
        return True
    except Exception:
        return False


def _produce_and_consume(bootstrap_servers: str, topic: str) -> bool:
    message = b"self-test-message"
    producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer.produce(topic, value=message)
    producer.flush(2)
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'self-test-group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False,
    })
    consumer.subscribe([topic])
    start = time.time()
    while time.time() - start < 5:
        msg = consumer.poll(0.5)
        if msg and not msg.error() and msg.value() == message:
            consumer.close()
            return True
    consumer.close()
    return False


@pytest.mark.skipif(not _kafka_broker_available('localhost:9092'),
                    reason="Kafka broker not available on localhost:9092")
def should_publish_and_consume_selftest() -> None:
    topic = "selftest-topic"
    assert _produce_and_consume(
        'localhost:9092', topic), "Kafka self-test failed: could not publish and consume message"
