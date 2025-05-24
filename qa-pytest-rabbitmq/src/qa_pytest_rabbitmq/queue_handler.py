# SPDX-License-Identifier: Apache-2.0

import threading
from typing import Any, Callable, Iterator
from collections.abc import Mapping
from dataclasses import dataclass, field
from types import TracebackType
from typing import Self, Type
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import BasicProperties

from qa_testing_utils.logger import LoggerMixin
from qa_testing_utils.object_utils import require_not_none
from qa_testing_utils.string_utils import EMPTY_STRING, to_string


@to_string()
@dataclass(frozen=True)
class Message[V]:
    """Represents a message with content and optional properties."""
    content: V
    properties: BasicProperties = field(default_factory=BasicProperties)


@to_string()
@dataclass
class QueueHandler[K, V](LoggerMixin):
    """
    Retrieves RabbitMQ messages from specified queue via provided channel.
    Messages are converted by specified value function and indexed by specified
    key function.

    Messages are consumed in background threads and made available for retrieval
    by their key.

    Typical workflow:
    1. build it with external channel
    2. start consumption -- this will run in background until closing
    3. retrieve messages
    """

    channel: BlockingChannel
    queue: str
    indexing_by: Callable[[Message[V]], K]
    consuming_by: Callable[[bytes], V]
    publishing_by: Callable[[V], bytes]

    _received_messages: dict[K, Message[V]] = field(
        default_factory=lambda: dict[K, Message[V]]())
    _consumer_tag: str | None = field(default=None, init=False)
    _consuming: bool = field(default=False, init=False)
    _lock: threading.RLock = field(default_factory=threading.RLock, init=False)
    _consumer_thread: threading.Thread | None = field(default=None, init=False)

    def __enter__(self) -> Self:
        """Enter context manager."""
        self.log.debug("initializing queue handler with external channel")
        return self

    def __exit__(self,
                 exc_type: Type[BaseException] | None,
                 exc_value: BaseException | None,
                 traceback: TracebackType | None) -> None:
        """Exit context manager."""
        self.close()

    def consume(self) -> str:
        """
        Start the message consumption process and return immediately.

        Returns:
            Consumer tag
        """
        if self._consuming:
            raise RuntimeError("consumer already started")

        # Set QoS
        self.channel.basic_qos(prefetch_count=16)

        def callback(ch: BlockingChannel, method: Any,
                     properties: BasicProperties, body: bytes) -> None:
            """Handle incoming messages."""
            try:
                # Deserialize message content
                content = self.consuming_by(body)
                message = Message(content=content, properties=properties)

                # Extract key
                key = self.indexing_by(message)
                self.log.debug(f"received {key}")

                # Store message
                with self._lock:
                    self._received_messages[key] = message

                # Acknowledge message
                ch.basic_ack(delivery_tag=require_not_none(method.delivery_tag))

            except Exception as e:
                self.log.warning(f"skipping unknown type {e}")
                # Reject and requeue the message
                ch.basic_reject(
                    delivery_tag=require_not_none(
                        method.delivery_tag),
                    requeue=True)

        # Start consuming
        self._consumer_tag = self.channel.basic_consume(
            queue=self.queue,
            on_message_callback=callback
        )

        self._consuming = True

        # Start consuming in background thread
        self._consumer_thread = threading.Thread(
            target=self._start_consuming,
            daemon=True,
            name="rabbitmq-consumer"
        )
        self._consumer_thread.start()

        consumer_tag = require_not_none(self._consumer_tag)
        self.log.debug(f"set-up consumer with tag {consumer_tag}")
        return consumer_tag

    def _start_consuming(self) -> None:
        """Start the consuming loop in background thread."""
        try:
            self.channel.start_consuming()
        except Exception as e:
            self.log.error(f"error in consuming loop: {e}")
            self._consuming = False

    def cancel(self) -> str:
        """
        Cancel the consumption, previously started by consume().

        Returns:
            The consumer tag

        Raises:
            RuntimeError: If consumer was not started
        """
        if not self._consumer_tag:
            raise RuntimeError("consumer not started")

        self.log.debug(f"cancelling consumer by tag {self._consumer_tag}")

        self.channel.stop_consuming()
        self._consuming = False

        # Wait for consumer thread to finish
        if self._consumer_thread and self._consumer_thread.is_alive():
            self._consumer_thread.join(timeout=5.0)

        return self._consumer_tag

    def close(self) -> None:
        """Close the queue handler and cancel consumption."""
        try:
            if self._consuming:
                self.cancel()
        except Exception as e:
            self.log.error(f"while closing got {e}")
        # Note: We don't close the channel since it's provided externally
        # The caller is responsible for managing the channel and connection lifecycle

    def publish(self, messages: Iterator[Message[V]]) -> None:
        """
        Publish multiple messages to the queue.

        Args:
            messages: Iterator of messages to publish
        """
        for message in messages:
            self.log.debug(f"publishing {message}")
            body = self.publishing_by(message.content)
            self.channel.basic_publish(
                exchange=EMPTY_STRING,
                routing_key=self.queue,
                body=body,
                properties=message.properties
            )

    def publish_values(self, values: Iterator[V]) -> None:
        """
        Publish multiple values as messages to the queue.

        Args:
            values: Iterator of values to publish
        """
        messages = (Message(content=value) for value in values)
        self.publish(messages)

    def received_messages(self) -> Mapping[K, Message[V]]:
        """
        Get unmodifiable view of retrieved messages.

        Returns:
            Mapping of received messages indexed by key
        """
        with self._lock:
            return dict(self._received_messages)
