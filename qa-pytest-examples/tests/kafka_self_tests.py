# SPDX-License-Identifier: Apache-2.0
"""
Integration/Bdd self-test for Kafka BDD steps.
"""
import pytest
from hamcrest import assert_that, equal_to, has_entries, has_property
from qa_pytest_kafka import (
    KafkaConfiguration,
    KafkaHandler,
    KafkaSteps,
    Message,
)


def _kafka_broker_available(bootstrap_servers: str) -> bool:
    try:
        from confluent_kafka import Producer
        p = Producer({'bootstrap.servers': bootstrap_servers})
        p.flush(0.5)
        return True
    except Exception:
        return False


@pytest.mark.skipif(
    not _kafka_broker_available('localhost:9092'),
    reason="Kafka broker not available on localhost:9092"
)
def test_kafka_steps_publish_and_consume():
    config = KafkaConfiguration()
    # Patch config for test
    config.parser.read_dict({
        'kafka': {
            'bootstrap_servers': 'localhost:9092',
            'topic': 'selftest-topic',
            'group_id': 'selftest-group',
        }
    })
    handler = KafkaHandler[
        str, str
    ](
        bootstrap_servers=config.bootstrap_servers,
        topic=config.topic,
        group_id=config.group_id,
        indexing_by=lambda m: m.content,
        consuming_by=lambda b: b.decode(),
        publishing_by=lambda s: s.encode()
    )
    steps = KafkaSteps[str, str](config).a_kafka_handler(handler)
    steps.publishing([Message(content="foo"), Message(content="bar")])
    steps.consuming()
    received = handler.received_messages
    assert_that(
        received,
        has_entries({
            "foo": has_property("content", equal_to("foo")),
            "bar": has_property("content", equal_to("bar")),
        })
    )
