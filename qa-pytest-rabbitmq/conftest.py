# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

import pytest
import qa_pytest_rabbitmq
from qa_testing_utils.conftest_helpers import *


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    """
    Pytest hook to configure logging before tests run.
    """
    configure(config, Path(qa_pytest_rabbitmq.__file__).parent / "logging.ini")


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(
        item: pytest.Item, call: pytest.CallInfo[None]) -> pytest.TestReport:
    """
    Pytest hook to customize test report generation.
    """
    return makereport(item, call)
