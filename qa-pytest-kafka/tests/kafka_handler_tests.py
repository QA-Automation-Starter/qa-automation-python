# SPDX-License-Identifier: Apache-2.0

from hamcrest import assert_that, equal_to, has_entries, has_property
from qa_pytest_kafka.kafka_handler import KafkaHandler
from qa_testing_utils.string_utils import EMPTY_STRING
from tenacity import (
    Retrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)


class KafkaHandlerTests:
    def should_publish_and_consume(self) -> None:
        handler = KafkaHandler[str, str](
            bootstrap_servers='localhost:9092',
            topic='selftest-topic',
            group_id='selftest-group',
            indexing_by=lambda m: m.content or EMPTY_STRING,
            consuming_by=lambda b: b.decode(),
            publishing_by=lambda s: s.encode()
        )
        handler.publish_values(iter(["foo", "bar"]))

        # Retry until background consumer receives messages
        Retrying(
            stop=stop_after_attempt(10),
            wait=wait_exponential(min=1, max=5),
            retry=retry_if_exception_type(AssertionError)
        )(lambda: assert_that(
            handler.received_messages,
            has_entries({
                "foo": has_property("content", equal_to("foo")),
                "bar": has_property("content", equal_to("bar")),
            })
        ))
