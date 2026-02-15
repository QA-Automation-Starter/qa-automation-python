# SPDX-License-Identifier: Apache-2.0
"""
Integration/Bdd self-test for Kafka BDD steps.
"""
from qa_pytest_kafka import (
    KafkaConfiguration,
    KafkaHandler,
    KafkaSteps,
    Message,
)
from qa_pytest_kafka.kafka_tests import KafkaTests
from qa_testing_utils.matchers import tracing, yields_items


class KafkaSelfTests(KafkaTests[str, str]):
    _handler: KafkaHandler[str, str]
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

    def setup_method(self) -> None:
        super().setup_method()
        self._handler = KafkaHandler[
            str, str
        ](
            bootstrap_servers=self.config.bootstrap_servers,
            topic=self.config.topic,
            group_id=self.config.group_id,
            indexing_by=lambda m: m.content,
            consuming_by=lambda b: b.decode(),
            publishing_by=lambda s: s.encode()
        )

# --8<-- [end:class]
