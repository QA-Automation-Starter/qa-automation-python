# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from functools import cached_property
from typing import final
from urllib.parse import urljoin

from qa.pytest.commons.abstract_configuration import AbstractConfiguration
from qa.testing.utils.string_utils import EMPTY


class RestConfiguration(AbstractConfiguration):

    @final
    @cached_property
    def endpoint_base(self) -> str:
        return self.parser["endpoint"]["base"]

    def endpoint_url(self, path: str = EMPTY) -> str:
        return urljoin(self.endpoint_base, path)
