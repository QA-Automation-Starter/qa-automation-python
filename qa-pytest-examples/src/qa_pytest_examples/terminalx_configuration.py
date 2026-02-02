# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

import random
from functools import cached_property
from typing import final

from qa_pytest_commons.ui_configuration import UiConfiguration
from qa_pytest_examples.model.terminalx_credentials import TerminalXCredentials
from qa_pytest_examples.model.terminalx_user import TerminalXUser


class TerminalXConfiguration(UiConfiguration):
    """
    Configuration for TerminalX UI tests.
    Provides access to entry point, users, and random user selection.
    """

    @cached_property
    @final
    def users(self) -> tuple[TerminalXUser, ...]:
        """
        Returns the list of TerminalX users from the configuration parser.

        Returns:
            tuple[TerminalXUser, ...]: The list of users.
        """
        users_section = self.parser["users"]
        return tuple(
            TerminalXUser(TerminalXCredentials.from_(
                username_password), name=key)
            for key, username_password in users_section.items()
        )

    @final
    @property
    def random_user(self) -> TerminalXUser:
        """
        Returns a random user from the list of users.

        Returns:
            TerminalXUser: A randomly selected user.
        """
        return random.choice(self.users)
