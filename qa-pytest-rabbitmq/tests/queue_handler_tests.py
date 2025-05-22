# SPDX-License-Identifier: Apache-2.0

from contextlib import closing
from typing import cast
import pika
from string_utils.generation import random_string
from hamcrest import assert_that, equal_to, has_length
from qa_pytest_rabbitmq.queue_handler import QueueHandler
from qa_testing_utils.object_utils import require_not_none
from qa_testing_utils.string_utils import EMPTY_STRING
from .abstract_queue_handler_tests import AbstractQueueHandlerTests


class QueueHandlerTests(AbstractQueueHandlerTests):
    def should_have_a_working_rabbitmq(self) -> None:
        some_text = random_string(10)
        with closing(pika.BlockingConnection(self.local_rabbit_mq)) as connection:
            with closing(connection.channel()) as channel:

                channel.basic_publish(
                    exchange=EMPTY_STRING,
                    routing_key=self.trace(
                        queue_name := require_not_none(
                            channel.queue_declare(
                                queue=EMPTY_STRING,
                                exclusive=True)
                            .method
                            .queue)),
                    body=some_text.encode())

                # NOTE types-pika incorrectly stubs body as str...
                _, _, body = channel.basic_get(
                    queue=queue_name,
                    auto_ack=True)

                assert_that(cast(bytes, body).decode(), equal_to(some_text))

    def should_retrieve_one_message(self) -> None:
        """Publishes and retrieves a message using QueueHandler."""
        import time
        connection_params = pika.ConnectionParameters("localhost")
        connection = pika.BlockingConnection(connection_params)
        channel = connection.channel()
        queue_result = channel.queue_declare(queue="", exclusive=True)
        queue_name = queue_result.method.queue  # type: ignore[attr-defined]
        channel.close()  # type: ignore
        connection.close()  # type: ignore
        handler = QueueHandler[int, bytes](
            queue=queue_name,  # type: ignore[arg-type]
            connection_params=connection_params,
            indexing_by=lambda m: hash(m.content),
            consuming_by=lambda b: b,
            publishing_by=lambda b: b,
        )
        handler.publish_values([b"abcd"])
        handler.consume()
        Retrying(
            stop=stop_after_attempt(4),
            wait=wait_exponential(min=1, max=10),
            retry=retry_if_exception_type(Exception),
            before_sleep=before_sleep_log(self.log, logging.DEBUG)
        )
        timeout = 20.0
        poll_interval = 0.2
        start = time.monotonic()
        while True:
            if handler.recieved_messages():
                break
            if time.monotonic() - start > timeout:
                raise AssertionError("Message was not received within timeout")
            time.sleep(poll_interval)
        assert_that(tuple(handler.recieved_messages().values()), has_length(1))
        handler.close()
