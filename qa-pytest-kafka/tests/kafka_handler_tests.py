# SPDX-License-Identifier: Apache-2.0

from hamcrest import assert_that, equal_to, has_entries, has_property
from qa_pytest_kafka.kafka_handler import KafkaHandler


class KafkaHandlerTests:
    def should_publish_and_consume(self) -> None:
        handler = KafkaHandler[str, str](
            bootstrap_servers='localhost:9092',
            topic='selftest-topic',
            group_id='selftest-group',
            indexing_by=lambda m: m.content,
            consuming_by=lambda b: b.decode(),
            publishing_by=lambda s: s.encode()
        )
        handler.publish_values(iter(["foo", "bar"]))
        handler.consume(timeout=5.0)
        received = handler.received_messages
        # Assert that received contains at least the expected messages with correct content
        assert_that(
            received,
            # has_entries checks for presence and value, ignores extra keys
            has_entries({
                "foo": has_property("content", equal_to("foo")),
                "bar": has_property("content", equal_to("bar")),
            })
        )
