# SPDX-License-Identifier: Apache-2.0

from uuid import uuid4

from confluent_kafka import Consumer, Producer
from hamcrest import assert_that, equal_to, has_entries, has_property
from qa_pytest_kafka.kafka_handler import KafkaHandler
from qa_testing_utils.object_utils import require_not_none
from qa_testing_utils.string_utils import EMPTY_STRING
from tenacity import (
    Retrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

_retrying = Retrying(
    stop=stop_after_attempt(10),
    wait=wait_exponential(min=1, max=5),
    retry=retry_if_exception_type((AssertionError, ValueError)))


def should_publish_and_consume_via_handler() -> None:
    with KafkaHandler[str, str](
        Consumer({
            'bootstrap.servers': 'localhost:9092',
            'group.id': f'test-{uuid4()}',
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False,
        }),
        Producer({
            'bootstrap.servers': 'localhost:9092',
        }),
        topic='selftest-topic',
        indexing_by=lambda m: m.content or EMPTY_STRING,
        consuming_by=lambda b: b.decode(),
        publishing_by=lambda s: s.encode()
    ) as handler:
        handler.publish_values(iter(["foo", "bar"]))

        # Retry until background consumer receives messages
        _retrying(lambda: assert_that(
            handler.received_messages,
            has_entries({
                "foo": has_property("content", equal_to("foo")),
                "bar": has_property("content", equal_to("bar")),
            })
        ))


def should_publish_and_consume() -> None:
    message = b"self-test-message"
    with Producer({'bootstrap.servers': 'localhost:9092'}) as producer:
        producer.produce('selftest-topic', value=message)
        producer.flush(2)

    with Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'self-test-group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False,
    }) as consumer:
        consumer.subscribe(['selftest-topic'])
        _retrying(lambda: assert_that(
            require_not_none(consumer.poll(0.5)).value(),
            equal_to(message)))
