# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

import inspect
import logging.config
from pathlib import Path
from typing import Callable, Optional

import pytest


def configure(config: pytest.Config,
              path: Path = Path(__file__).parent / "logging.ini") -> None:
    """
    Configures logging for pytest using a specified INI file, or defaults to internal logging.ini.
    """
    if path.is_file():
        logging.info(f"logging ini from: {path}")
        logging.config.fileConfig(path)
    else:
        logging.warning(f"couldn't find logging ini file {path}")


def makereport(
        item: pytest.Item, call: pytest.CallInfo[None]) -> None:
    """
    Appends the source code of the test function to the pytest report for the given test item.

    This function ensures that the source code is included in the report even for successful tests,
    by adding a custom report section during the 'call' phase of test execution.

    Args:
        item (pytest.Item): The pytest test item being reported.
        call (pytest.CallInfo[None]): The call information for the test execution phase.

    Returns:
        None
    """

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
