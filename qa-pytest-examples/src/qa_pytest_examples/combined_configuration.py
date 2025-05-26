# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path

from qa_pytest_examples.swagger_petstore_configuration import SwaggerPetstoreConfiguration
from qa_pytest_examples.terminalx_configuration import TerminalXConfiguration


class CombinedConfiguration(
        SwaggerPetstoreConfiguration, TerminalXConfiguration):

    def __init__(
            self,
            path: Path = Path("qa-pytest-examples/resources/combined-default-config.ini")):
        super().__init__(path)
