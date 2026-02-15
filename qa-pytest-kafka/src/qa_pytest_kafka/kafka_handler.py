# SPDX-License-Identifier: Apache-2.0

import threading
from dataclasses import dataclass, field
from types import TracebackType
from typing import Callable, Final, Iterator, Mapping, final

from confluent_kafka import Consumer
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
    def from_kafka[VV](
            msg: KafkaMessage,
            deserializer: Callable[[bytes], VV]) -> "Message[VV]":
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

    _received_messages: Final[dict[K, Message[V]]] = field(
        default_factory=lambda: dict(), init=False)
    _worker_thread: threading.Thread = field(init=False)
    _shutdown_event: threading.Event = field(
        default_factory=threading.Event, init=False)
    _lock: threading.RLock = field(default_factory=threading.RLock, init=False)

    def __post_init__(self) -> None:
        """Starts the consumer thread for handling asynchronous Kafka operations."""
        self._worker_thread = threading.Thread(
            target=self._worker_loop, name="kafka-consumer", daemon=True)
        self._worker_thread.start()

    def __enter__(self) -> "KafkaHandler[K, V]":
        """Context manager entry. Returns self."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None
    ) -> None:
        """Context manager exit. Ensures the handler is closed."""
        self.close()

    def _worker_loop(self) -> None:
        """Internal consumer loop for processing Kafka messages."""
        try:
            with Consumer({
                'bootstrap.servers': self.bootstrap_servers,
                'group.id': self.group_id,
                'auto.offset.reset': 'earliest',
                'enable.auto.commit': False,
            }) as consumer:
                consumer.subscribe([self.topic])
                while not self._shutdown_event.is_set():
                    msg = consumer.poll(0.5)
                    if msg is None:
                        continue
                    error = msg.error()
                    if error is not None:
                        self.log.warning(f"Kafka error: {error}")
                        continue
                    message = Message.from_kafka(msg, self.consuming_by)
                    key = self.indexing_by(message)
                    with self._lock:
                        self._received_messages[key] = message
                    self.log.debug(f"received {key}")
        except Exception as e:
            self.log.error(f"Unhandled error in consumer thread: {e}")

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

    def close(self) -> None:
        """Gracefully shuts down the consumer thread."""
        self._shutdown_event.set()
        self._worker_thread.join(timeout=5.0)

    @property
    def received_messages(self) -> Mapping[K, Message[V]]:
        """Returns a snapshot of all received messages, indexed by key."""
        with self._lock:
            return dict(self._received_messages)
