# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass, field
from typing import Callable, Final, Iterator, Mapping, cast, final

from confluent_kafka import Consumer, KafkaError
from confluent_kafka import Message as KafkaMessage
from confluent_kafka import Producer
from qa_testing_utils.logger import LoggerMixin


@dataclass(frozen=True)
class Message[V]:
    """
    Represents a Kafka message with business content and metadata.

    Fields:
        content: The business payload of the message (None if message is empty).
        headers: Optional headers as a dictionary.
        key: Optional message key (for partitioning).
        offset: Kafka-assigned sequence number within a partition.
            - Not part of business equality or hash.
            - Excluded from __eq__ and __hash__ to ensure tests and business logic
              compare messages by content, key, and headers only.
            - Used for tracking consumer progress and ordering, not for business identity.
    """
    content: V | None
    headers: dict[str, bytes | str | None] = field(default_factory=lambda: {})
    key: bytes | None = None
    offset: int | None = field(default=None, compare=False, hash=False)

    @staticmethod
    def from_kafka(
            msg: KafkaMessage,
            deserializer: Callable[[bytes], V]) -> "Message[V]":
        """Factory method to construct a Message from a confluent_kafka message."""
        raw_value = msg.value()
        return Message(
            content=deserializer(raw_value) if raw_value is not None else None,
            headers=dict(msg.headers() or []),
            key=msg.key(),
            offset=msg.offset()
        )


@final
@dataclass
class KafkaHandler[K, V](LoggerMixin):
    bootstrap_servers: Final[str]
    topic: Final[str]
    group_id: Final[str]
    indexing_by: Final[Callable[[Message[V]], K]]
    consuming_by: Final[Callable[[bytes], V]]
    publishing_by: Final[Callable[[V], bytes]]
    _received_messages: dict[K, Message[V]] = field(
        default_factory=lambda: cast(dict[K, Message[V]], {}), init=False)

    def publish(self, messages: Iterator[Message[V]]) -> None:
        with Producer({'bootstrap.servers': self.bootstrap_servers}) as producer:
            for message in messages:
                value = self.publishing_by(
                    message.content) if message.content is not None else None
                producer.produce(self.topic, value, message.key,
                                 headers=list(message.headers.items()))
                self.log.debug(f"published {message}")

    def publish_values(self, values: Iterator[V]) -> None:
        self.publish((Message(content=value) for value in values))

    def consume(self, timeout: float = 5.0) -> None:
        with Consumer({
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': self.group_id,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False,
        }) as consumer:
            consumer.subscribe([self.topic])
            end_time = timeout
            while end_time > 0:
                msg = consumer.poll(0.5)
                end_time -= 0.5
                if msg is None:
                    continue
                error = msg.error()
                if error is not None:
                    partition_eof = getattr(KafkaError, "_PARTITION_EOF", None)
                    if partition_eof is not None and error.code() == partition_eof:
                        continue
                    self.log.warning(f"Kafka error: {error}")
                    continue
                message = cast(
                    Message[V],
                    Message.from_kafka(msg, self.consuming_by))
                key = self.indexing_by(message)
                self._received_messages[key] = message
                self.log.debug(f"received {key}")

    @property
    def received_messages(self) -> Mapping[K, Message[V]]:
        return dict(self._received_messages)
