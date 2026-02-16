# SPDX-License-Identifier: Apache-2.0
"""
Integration/Bdd self-test for Kafka BDD steps.
"""
from typing import override
from uuid import uuid4

from confluent_kafka import Consumer, Producer
from qa_pytest_kafka import (
    KafkaConfiguration,
    KafkaHandler,
    KafkaSteps,
    Message,
)
from qa_pytest_kafka.kafka_tests import KafkaTests
from qa_testing_utils.matchers import tracing, yields_items
from qa_testing_utils.string_utils import EMPTY_STRING


# --8<-- [start:class]
class KafkaSelfTests(
    KafkaTests
    [str, str, KafkaSteps[str, str, KafkaConfiguration],
     KafkaConfiguration]):
    _steps_type = KafkaSteps
    _configuration = KafkaConfiguration()

    # --8<-- [start:func]
    def should_publish_and_consume(self) -> None:
        (self.steps
            .given.a_kafka_handler(self._handler)
            .when.publishing([Message(content="foo"), Message(content="bar")])
            .then.the_received_messages(
                yields_items([
                    tracing(Message(content="foo")),
                    tracing(Message(content="bar")),
                ])
            )
         )
    # --8<-- [end:func]

    @override
    def setup_method(self) -> None:
        super().setup_method()
        # Create Consumer with unique group_id per test for isolation
        self._handler = KafkaHandler[str, str](
            Consumer({
                'bootstrap.servers': self.configuration.bootstrap_servers,
                'group.id': f'test-{uuid4()}',
                'auto.offset.reset': 'earliest',
                'enable.auto.commit': False,
            }),
            Producer({
                'bootstrap.servers': self.configuration.bootstrap_servers,
            }),
            self.configuration.topic,
            indexing_by=lambda message: message.content or EMPTY_STRING,
            consuming_by=lambda payload: payload.decode(),
            publishing_by=lambda value: value.encode())

# --8<-- [end:class]
