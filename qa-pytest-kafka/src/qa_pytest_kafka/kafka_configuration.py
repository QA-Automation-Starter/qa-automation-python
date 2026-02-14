# SPDX-License-Identifier: Apache-2.0

from functools import cached_property

from qa_pytest_commons.base_configuration import BaseConfiguration


class KafkaConfiguration(BaseConfiguration):
    """
    Kafka-specific test configuration.
    Provides access to the Kafka bootstrap servers from the configuration parser.
    """
    @cached_property
    def bootstrap_servers(self) -> str:
        return self.parser.get("kafka", "bootstrap_servers")

    @cached_property
    def topic(self) -> str:
        return self.parser.get("kafka", "topic")

    @cached_property
    def group_id(self) -> str:
        return self.parser.get("kafka", "group_id")
