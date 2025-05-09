# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

import inspect
import logging.config
import sys
from typing import Callable, Optional

import pytest

# https://docs.python.org/3/whatsnew/3.13.html
MIN_PYTHON_VERSION = (3, 13)
pytest_plugins = ["pytest_html"]


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    if sys.version_info < MIN_PYTHON_VERSION:
        raise pytest.UsageError(
            f"Python version must be {MIN_PYTHON_VERSION} or higher for these tests.")

    logging.config.fileConfig('logging.ini')


def pytest_html_report_title(report) -> None:  # type: ignore
    report.title = "Tests Report"


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(
        item: pytest.Item, call: pytest.CallInfo[None]) -> None:
    # NOTE: this is required in order to have source code added to report even for successful tests
    if call.when == "call":
        item._report_sections.append(  # type: ignore
            ('call', 'body', get_test_body(item)))


def get_test_body(item: pytest.Item) -> str:
    function: Optional[Callable[..., None]] = getattr(item, 'function', None)
    if function is None:
        return "No function found for this test item."

    try:
        return inspect.getsource(function)
    except Exception as e:
        return f"Could not get source code: {str(e)}"
