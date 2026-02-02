# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from qa_pytest_commons.ui_steps import UiSteps
from qa_pytest_playwright.playwright_configuration import (
    PlaywrightConfiguration,
)


class PlaywrightSteps[TConfiguration: PlaywrightConfiguration](
    UiSteps[TConfiguration]
):
    """
    BDD-style step definitions for Playwright-based UI operations.

    Type Parameters:
        TConfiguration: The configuration type, must be a PlaywrightConfiguration.

    Attributes:
        _ui_context (UiContext[UiElement]): The Playwright UI context used for browser automation.
    """
    pass
