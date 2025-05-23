# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass, field
from types import TracebackType
from typing import Callable, Iterable, Dict, Type, Self
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from threading import Lock, Thread

from qa_testing_utils.logger import LoggerMixin
from qa_testing_utils.object_utils import require_not_none
from qa_testing_utils.string_utils import EMPTY_STRING, to_string


@to_string()
@dataclass(frozen=True)
class Message[V]:
    """Represents a message with content and optional properties."""
    content: V
    properties: BasicProperties = field(default_factory=BasicProperties)


class QueueHandler[K, V](LoggerMixin):
    """Handles publishing and consuming messages from RabbitMQ queues."""

    def __init__(
            self,
            channel: BlockingChannel,
            queue: str,
            indexing_by: Callable[[Message[V]], K],
            consuming_by: Callable[[bytes], V],
            publishing_by: Callable[[V], bytes]) -> None:
        self._channel = channel
        self._queue = queue
        self._indexing_by = indexing_by
        self._consuming_by = consuming_by
        self._publishing_by = publishing_by
        self._messages: dict[K, Message[V]] = {}
        self._consumer_tag: str | None = None
        self._lock = Lock()

    def _on_message(
            self,
            ch: BlockingChannel,
            method: Basic.Deliver,
            props: BasicProperties,
            body: bytes) -> None:
        try:
            message = Message(self._consuming_by(body), props)
            key = self._indexing_by(message)
            with self._lock:
                self._messages[key] = message
            self.log.debug(f"received {key}")
            ch.basic_ack(delivery_tag=require_not_none(method.delivery_tag))
        except Exception as e:
            self.log.warning(f"skipping unknown type {e}")
            ch.basic_reject(
                delivery_tag=require_not_none(method.delivery_tag),
                requeue=True)

    def consume(self) -> str:
        self._channel.basic_qos(prefetch_count=16)
        self._consumer_tag = self._channel.basic_consume(
            queue=self._queue,
            on_message_callback=self._on_message,
            auto_ack=False,
        )
        Thread(target=self._channel.start_consuming, daemon=True).start()
        self.log.debug(f"set-up consumer with tag {self._consumer_tag}")
        return self._consumer_tag

    def publish(self, messages: Iterable[Message[V]]) -> None:
        for message in messages:
            self.log.debug(f"publishing {message}")
            self._channel.basic_publish(
                exchange=EMPTY_STRING,
                routing_key=self._queue,
                body=self._publishing_by(message.content),
                properties=message.properties,
            )

    def publish_values(self, values: Iterable[V]) -> None:
        self.publish(Message(value) for value in values)

    def cancel(self) -> str:
        if self._consumer_tag is None:
            raise IOError("consumer not started")

        self.log.debug(f"cancelling consumer by tag {self._consumer_tag}")
        self._channel.basic_cancel(self._consumer_tag)
        return self._consumer_tag

    def received_messages(self) -> Dict[K, Message[V]]:
        with self._lock:
            return dict(self._messages)

    def __enter__(self) -> Self:
        return self

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_value: BaseException | None,
            traceback: TracebackType | None) -> None:
        self.cancel()
