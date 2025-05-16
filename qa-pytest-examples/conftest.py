# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from qa_testing_utils.conftest_helpers import *

import pytest


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    configure(config)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(
        item: pytest.Item, call: pytest.CallInfo[None]) -> None:
    makereport(item, call)
