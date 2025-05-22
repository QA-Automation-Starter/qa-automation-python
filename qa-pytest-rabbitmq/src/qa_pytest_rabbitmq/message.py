# SPDX-License-Identifier: Apache-2.0
"""
qa_pytest_rabbitmq.message

Message wrapper, similar to Java Message<V>.
"""
import pika

class Message[V]:
    """Represents a message with content and optional properties (pika.BasicProperties)."""
    def __init__(self, content: V, properties: pika.BasicProperties | None = None) -> None:
        self.content = content
        self.properties = properties or pika.BasicProperties()
