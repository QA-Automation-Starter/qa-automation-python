# SPDX-License-Identifier: Apache-2.0
"""
Base class for Kafka BDD self-tests, mirroring RabbitMQ BDD test structure.
"""
from typing import Generic, TypeVar

from qa_pytest_kafka.kafka_configuration import KafkaConfiguration
from qa_pytest_kafka.kafka_steps import KafkaSteps

K = TypeVar("K")
V = TypeVar("V")


class KafkaTests(Generic[K, V]):
    steps: KafkaSteps[K, V]
    config: KafkaConfiguration

    def setup_method(self) -> None:
        self.config = KafkaConfiguration()
        # Patch config for test
        self.config.parser.read_dict({
            'kafka': {
                'bootstrap_servers': 'localhost:9092',
                'topic': 'selftest-topic',
                'group_id': 'selftest-group',
            }
        })
        self.steps = KafkaSteps[K, V](self.config)

    def teardown_method(self) -> None:
        pass  # No-op for now, extend if needed
