# SPDX-License-Identifier: Apache-2.0
"""
Base class for Kafka BDD self-tests, mirroring RabbitMQ BDD test structure.
"""
from typing import Any

from qa_pytest_commons.abstract_tests_base import AbstractTestsBase
from qa_pytest_kafka.kafka_configuration import KafkaConfiguration
from qa_pytest_kafka.kafka_handler import KafkaHandler
from qa_pytest_kafka.kafka_steps import KafkaSteps


class KafkaTests[
    K,
    V,
    TSteps: KafkaSteps[Any, Any, Any],
    TConfiguration: KafkaConfiguration
](AbstractTestsBase[TSteps, TConfiguration]):
    """
    Base class for BDD-style Kafka integration tests.
    Manages the lifecycle of a Kafka handler for test scenarios.

    Type Args:
        K: The type of the message key.
        V: The type of the message content.
        TSteps: The steps implementation type.
        TConfiguration: The configuration type, must be a KafkaConfiguration.
    """
    _handler: KafkaHandler[K, V]
