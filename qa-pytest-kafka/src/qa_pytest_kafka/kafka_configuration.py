# SPDX-License-Identifier: Apache-2.0

from functools import cached_property
from urllib.parse import ParseResult, parse_qs, urlparse

from qa_pytest_commons.base_configuration import BaseConfiguration


class KafkaConfiguration(BaseConfiguration):
    """
    Kafka-specific test configuration.
    Provides access to the Kafka bootstrap servers from the configuration parser.
    """
    @cached_property
    def _kafka_url(self) -> ParseResult:
        url = self.parser.get("kafka", "url")
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc or not parsed.path:
            raise ValueError(f"malformed kafka url: {url}")
        return parsed

    @cached_property
    def bootstrap_servers(self) -> str:
        return self._kafka_url.netloc

    @cached_property
    def topic(self) -> str:
        return self._kafka_url.path.lstrip("/")

    @cached_property
    def group_id(self) -> str:
        group_id = parse_qs(self._kafka_url.query).get("group_id", [])
        if group_id:
            return group_id[0]
        raise ValueError("missing group_id in kafka url")
