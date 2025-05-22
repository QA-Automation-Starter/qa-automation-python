# SPDX-License-Identifier: Apache-2.0
"""
qa_pytest_rabbitmq.queue_handler

Core RabbitMQ queue handler, similar to Java QueueHandler.
"""

from typing import Callable, Iterable, Dict, Any
from qa_pytest_rabbitmq.message import Message
import threading
import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties


class QueueHandler[K, V]:
    """Handles publishing and consuming messages from RabbitMQ queues."""

    def __init__(
        self,
        queue: str,
        connection_params: Any,
        indexing_by: Callable[[Message[V]], K],
        consuming_by: Callable[[bytes], V],
        publishing_by: Callable[[V], bytes],
    ) -> None:
        self._queue = queue
        self._connection_params = connection_params
        self._indexing_by = indexing_by
        self._consuming_by = consuming_by
        self._publishing_by = publishing_by
        self._connection = pika.BlockingConnection(connection_params)
        self._channel: BlockingChannel = self._connection.channel()
        self._messages: dict[K, Message[V]] = {}
        self._consumer_tag: str | None = None
        self._lock = threading.Lock()

    def publish(self, messages: Iterable[Message[V]]) -> None:
        for message in messages:
            self._channel.basic_publish(
                exchange='',
                routing_key=self._queue,
                body=self._publishing_by(message.content),
                properties=message.properties
            )

    def publish_values(self, values: Iterable[V]) -> None:
        self.publish((Message[V](content=value) for value in values))

    def consume(self) -> str:
        def callback(
                ch: BlockingChannel,
                method: Basic.Deliver,
                properties: BasicProperties,
                body: bytes) -> None:
            value = self._consuming_by(body)
            msg = Message[V](content=value, properties=properties)
            key = self._indexing_by(msg)
            with self._lock:
                self._messages[key] = msg
            ch.basic_ack(delivery_tag=method.delivery_tag)

        consumer_tag = self._channel.basic_consume(
            queue=self._queue,
            on_message_callback=callback,
            auto_ack=False)

        self._consumer_tag = str(consumer_tag)
        threading.Thread(target=self._channel.start_consuming,
                         daemon=True).start()
        return self._consumer_tag

    def cancel(self) -> str:
        if self._consumer_tag:
            self._channel.basic_cancel(self._consumer_tag)
            tag = self._consumer_tag
            self._consumer_tag = None
            return str(tag)
        return ""

    def close(self) -> None:
        if self._consumer_tag:
            self.cancel()
        self._channel.close()
        self._connection.close()

    def recieved_messages(self) -> Dict[K, Message[V]]:
        with self._lock:
            return dict(self._messages)
