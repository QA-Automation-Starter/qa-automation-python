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
    '''
    Docstring for configure

    :param config: pytest config object
    :param path: path of ini file; defaults to the one packaged with qa_testing_utils
    '''
    if path.is_file():
        logging.info(f"logging ini from: {path}")
        logging.config.fileConfig(path)
    else:
        logging.warning(f"couldn't find logging ini file {path}")


def makereport(
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
