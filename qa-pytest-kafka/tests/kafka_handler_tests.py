# SPDX-License-Identifier: Apache-2.0

import pytest
from hamcrest import assert_that, equal_to, has_entries, has_property
from qa_pytest_kafka.kafka_handler import KafkaHandler


def _kafka_broker_available(bootstrap_servers: str) -> bool:
    try:
        from confluent_kafka import Producer
        p = Producer({'bootstrap.servers': bootstrap_servers})
        p.flush(0.5)
        return True
    except Exception:
        return False


class KafkaHandlerTests:
    @pytest.mark.skipif(
        not _kafka_broker_available('localhost:9092'),
        reason="Kafka broker not available on localhost:9092"
    )
    def should_publish_and_consume(self) -> None:
        handler = KafkaHandler[
            str, str
        ](
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
