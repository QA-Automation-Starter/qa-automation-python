# SPDX-License-Identifier: Apache-2.0
"""
Integration/Bdd self-test for Kafka BDD steps.
"""
from typing import Callable, override

from qa_pytest_kafka import KafkaConfiguration, KafkaSteps, Message
from qa_pytest_kafka.kafka_tests import KafkaTests
from qa_testing_utils.matchers import tracing, yields_items


class KafkaSelfTests(
    KafkaTests
    [str, str, KafkaSteps[str, str, KafkaConfiguration],
     KafkaConfiguration]):
    _steps_type = KafkaSteps
    _configuration = KafkaConfiguration()

    def should_publish_and_consume(self) -> None:
        (self.steps
            .given.a_kafka_handler(self._handler)
            .when.publishing([Message(content="foo"), Message(content="bar")])
            .and_.consuming()
            .then.the_received_messages(
                yields_items([
                    tracing(Message(content="foo")),
                    tracing(Message(content="bar")),
                ])
            )
         )

    @override
    def _indexing_by(self) -> Callable[[Message[str]], str]:
        return lambda message: message.content

    @override
    def _consuming_by(self) -> Callable[[bytes], str]:
        return lambda payload: payload.decode()

    @override
    def _publishing_by(self) -> Callable[[str], bytes]:
        return lambda value: value.encode()

# --8<-- [end:class]
