# SPDX-License-Identifier: Apache-2.0

from typing import Iterable, Iterator, Self, final

from hamcrest.core.matcher import Matcher
from qa_pytest_commons.generic_steps import GenericSteps
from qa_pytest_kafka.kafka_configuration import KafkaConfiguration
from qa_pytest_kafka.kafka_handler import KafkaHandler, Message
from qa_testing_utils.logger import Context
from qa_testing_utils.object_utils import require_not_none


class KafkaSteps[K, V, TConfiguration: KafkaConfiguration](
        GenericSteps[TConfiguration]):
    """
    BDD-style step definitions for Kafka operations.

    Type Parameters:
        K: The type of the message key.
        V: The type of the message content.
        TConfiguration: The configuration type, must be a KafkaConfiguration.
    """
    _kafka_handler: KafkaHandler[K, V]

    @Context.traced
    @final
    def a_kafka_handler(self, kafka_handler: KafkaHandler[K, V]) -> Self:
        self._kafka_handler = kafka_handler
        return self

    @Context.traced
    @final
    def publishing(self, messages: Iterable[Message[V]]) -> Self:
        self._kafka_handler.publish(iter(messages))
        return self

    @Context.traced
    @final
    def the_received_messages(
            self, by_rule: Matcher[Iterator[Message[V]]]) -> Self:
        return self.eventually_assert_that(
            lambda: iter(self._kafka_handler.received_messages.values()),
            by_rule)

    @Context.traced
    @final
    def the_message_by_key(self, key: K, by_rule: Matcher[Message[V]]) -> Self:
        return self.eventually_assert_that(
            lambda: require_not_none(self._kafka_handler.received_messages.get(key)),
            by_rule)
