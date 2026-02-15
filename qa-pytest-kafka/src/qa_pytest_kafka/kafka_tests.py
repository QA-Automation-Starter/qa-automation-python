# SPDX-License-Identifier: Apache-2.0
"""
Base class for Kafka BDD self-tests, mirroring RabbitMQ BDD test structure.
"""
from collections.abc import Callable
from typing import Any, override

from qa_pytest_commons.abstract_tests_base import AbstractTestsBase
from qa_pytest_kafka.kafka_configuration import KafkaConfiguration
from qa_pytest_kafka.kafka_handler import KafkaHandler, Message
from qa_pytest_kafka.kafka_steps import KafkaSteps


class KafkaTests[
    K,
    V,
    TSteps: KafkaSteps[Any, Any, Any],
    TConfiguration: KafkaConfiguration
](AbstractTestsBase[TSteps, TConfiguration]):
    """
    Base class for BDD-style Kafka integration tests.

    Type Args:
        K: The type of the message key.
        V: The type of the message content.
        TSteps: The steps implementation type.
        TConfiguration: The configuration type, must be a KafkaConfiguration.
    """
    _handler: KafkaHandler[K, V]

    @override
    def setup_method(self) -> None:
        super().setup_method()
        self._handler = self._create_handler()

    def _create_handler(self) -> KafkaHandler[K, V]:
        return KafkaHandler[
            K, V
        ](
            bootstrap_servers=self.configuration.bootstrap_servers,
            topic=self.configuration.topic,
            group_id=self.configuration.group_id,
            indexing_by=self._indexing_by(),
            consuming_by=self._consuming_by(),
            publishing_by=self._publishing_by(),
        )

    def _indexing_by(self) -> Callable[[Message[V]], K]:
        raise NotImplementedError()

    def _consuming_by(self) -> Callable[[bytes], V]:
        raise NotImplementedError()

    def _publishing_by(self) -> Callable[[V], bytes]:
        raise NotImplementedError()
