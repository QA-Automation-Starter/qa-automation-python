# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    Final,
    Generic,
    Iterator,
    Mapping,
    TypeVar,
    final,
)

from confluent_kafka import Consumer, KafkaError, Producer
from qa_testing_utils.logger import LoggerMixin

K = TypeVar("K")
V = TypeVar("V")


@dataclass(frozen=True)
class Message(Generic[V]):
    """
    Represents a Kafka message with business content and metadata.

    Fields:
        content: The business payload of the message.
        headers: Optional headers as a dictionary.
        key: Optional message key (for partitioning).
        offset: Kafka-assigned sequence number within a partition.
            - Not part of business equality or hash.
            - Excluded from __eq__ and __hash__ to ensure tests and business logic
              compare messages by content, key, and headers only.
            - Used for tracking consumer progress and ordering, not for business identity.
    """
    content: V
    headers: dict[str, Any] = field(default_factory=dict)
    key: bytes | None = None
    offset: int | None = field(default=None, compare=False, hash=False)


@final
@dataclass
class KafkaHandler(Generic[K, V], LoggerMixin):
    bootstrap_servers: Final[str]
    topic: Final[str]
    group_id: Final[str]
    indexing_by: Final[Callable[[Message[V]], K]]
    consuming_by: Final[Callable[[bytes], V]]
    publishing_by: Final[Callable[[V], bytes]]
    _received_messages: dict[K, Message[V]] = field(
        default_factory=dict, init=False)

    def publish(self, messages: Iterator[Message[V]]) -> None:
        producer = Producer({'bootstrap.servers': self.bootstrap_servers})
        for message in messages:
            producer.produce(self.topic, value=self.publishing_by(
                message.content), key=message.key, headers=message.headers)
            self.log.debug(f"published {message}")
        producer.flush()

    def publish_values(self, values: Iterator[V]) -> None:
        self.publish((Message(content=value) for value in values))

    def consume(self, timeout: float = 5.0) -> None:
        consumer = Consumer({
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': self.group_id,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False,
        })
        consumer.subscribe([self.topic])
        end_time = timeout
        while end_time > 0:
            msg = consumer.poll(0.5)
            end_time -= 0.5
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    self.log.warning(f"Kafka error: {msg.error()}")
                    continue
            content = self.consuming_by(msg.value())
            message = Message(
                content=content, headers=msg.headers() or {},
                key=msg.key(),
                offset=msg.offset())
            key = self.indexing_by(message)
            self._received_messages[key] = message
            self.log.debug(f"received {key}")
        consumer.close()

    @property
    def received_messages(self) -> Mapping[K, Message[V]]:
        return dict(self._received_messages)
