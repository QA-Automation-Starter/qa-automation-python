# SPDX-License-Identifier: Apache-2.0

import pika
from dataclasses import dataclass, field
from types import TracebackType
from typing import Any, Callable, Iterable, Dict, Type, Self
from pika.adapters.select_connection import SelectConnection
from pika.channel import Channel
from pika.spec import Basic, BasicProperties
from threading import Lock, Event, Thread

from qa_testing_utils.logger import LoggerMixin
from qa_testing_utils.object_utils import require_not_none
from qa_testing_utils.string_utils import EMPTY_STRING, to_string


@to_string()
@dataclass(frozen=True)
class Message[V]:
    """Represents a message with content and optional properties."""
    content: V
    properties: BasicProperties = field(default_factory=BasicProperties)


@dataclass
class QueueHandler[K, V](LoggerMixin):
    """Handles publishing and consuming messages from RabbitMQ queues."""

    connection_params: pika.URLParameters
    queue: str
    indexing_by: Callable[[Message[V]], K]
    consuming_by: Callable[[bytes], V]
    publishing_by: Callable[[V], bytes]

    _messages: dict[K, Message[V]] = field(default_factory=dict, init=False)
    _lock: Lock = field(default_factory=Lock, init=False)
    _queue_declared: Event = field(default_factory=Event, init=False)
    _channel_opened: Event = field(default_factory=Event, init=False)
    _connection: SelectConnection | None = field(default=None, init=False)
    _channel: Channel | None = field(default=None, init=False)

    def _on_message(self, ch: Channel, method: Basic.Deliver,
                    props: BasicProperties, body: bytes) -> None:
        try:
            message = Message(self.consuming_by(body), props)
            key = self.indexing_by(message)
            with self._lock:
                self._messages[key] = message
            self.log.debug(f"received {key}")
            ch.basic_ack(delivery_tag=require_not_none(method.delivery_tag))
        except Exception as e:
            self.log.warning(f"skipping unknown type {e}")
            ch.basic_reject(delivery_tag=require_not_none(
                method.delivery_tag), requeue=True)

    def _on_queue_declared(self, _: Any) -> None:
        if not self._channel:
            raise RuntimeError("channel not ready")

        consumer_tag = self._channel.basic_consume(
            queue=self.queue,
            on_message_callback=self._on_message,
            auto_ack=False)

        if self._connection and self._connection.ioloop:
            self._connection.ioloop.add_callback_threadsafe(self._queue_declared.set)
        else:
            self._queue_declared.set()

        self.log.debug(f"consumer started with tag {consumer_tag}")

    def _on_channel_open(self, channel: Channel) -> None:
        self._channel = channel
        self._channel_opened.set()
        channel.queue_declare(
            queue=self.queue, callback=self._on_queue_declared)

    def _on_connection_open(self, connection: Any) -> None:
        self._connection = connection
        connection.channel(on_open_callback=self._on_channel_open)

    def consume(self) -> None:
        def _run():
            self._connection = SelectConnection(
                parameters=self.connection_params,
                on_open_callback=self._on_connection_open,
            )
            self._connection.ioloop.start()

        Thread(target=_run, daemon=True).start()
        self._queue_declared.wait(timeout=5)

    def publish(self, messages: Iterable[Message[V]]) -> None:
        if not self._channel_opened.wait(timeout=5):
            raise RuntimeError("channel not ready")
        if not self._channel:
            raise RuntimeError("channel not ready")

        for message in messages:
            self.log.debug(f"publishing {message}")
            self._channel.basic_publish(
                exchange=EMPTY_STRING,
                routing_key=self.queue,
                body=self.publishing_by(message.content),
                properties=message.properties,
            )

    def publish_values(self, values: Iterable[V]) -> None:
        self.publish(Message(value) for value in values)

    def received_messages(self) -> Dict[K, Message[V]]:
        with self._lock:
            return dict(self._messages)

    def close(self) -> None:
        if self._connection:
            self._connection.close()
            self._connection.ioloop.stop()

    def __enter__(self) -> Self:
        return self

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_value: BaseException | None,
            traceback: TracebackType | None) -> None:
        self.close()
