# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass

from qa.pytest.examples.model.terminalx_credentials import TerminalXCredentials


@dataclass(frozen=True)
class TerminalXUser:
    credentials: TerminalXCredentials
    name: str
