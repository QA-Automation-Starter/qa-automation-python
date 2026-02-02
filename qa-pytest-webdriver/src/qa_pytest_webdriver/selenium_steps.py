# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0


from qa_pytest_commons.ui_steps import UiSteps
from qa_pytest_webdriver.selenium_configuration import SeleniumConfiguration


class SeleniumSteps[TConfiguration: SeleniumConfiguration](
    UiSteps[TConfiguration]
):
    """
    BDD-style step definitions for Selenium-based UI operations.

    Type Parameters:
        TConfiguration: The configuration type, must be a SeleniumConfiguration.

    Attributes:
        _ui_context (UiContext[UiElement]): The UI context instance used for browser automation.
    """
    pass
