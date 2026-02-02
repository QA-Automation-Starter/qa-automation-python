# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from typing import Any, override

from qa_pytest_commons.abstract_tests_base import AbstractTestsBase
from qa_pytest_commons.ui_configuration import UiConfiguration
from qa_pytest_commons.ui_protocols import UiContext, UiElement
from qa_pytest_webdriver.selenium_steps import SeleniumSteps
from qa_pytest_webdriver.selenium_ui_adapter import SeleniumUiContext
from selenium.webdriver.remote.webdriver import WebDriver


class SeleniumTests[
    TSteps: SeleniumSteps[Any],
    TConfiguration: UiConfiguration
](AbstractTestsBase[TSteps, TConfiguration]):
    """
    Base class for Selenium-based UI test cases.

    This class manages the lifecycle of a Selenium WebDriver for each test method.
    It is generic over the types of steps and configuration used.

    Attributes:
        _web_driver (WebDriver): The Selenium WebDriver instance (not thread safe).

    Type Parameters:
        TSteps: The type of the steps class, typically derived from SeleniumSteps.
        TConfiguration: The type of the configuration class, typically derived from UiConfiguration.
    """
    _web_driver: WebDriver  # not thread safe

    @property
    def ui_context(self) -> UiContext[UiElement]:
        '''
        Returns the web driver instance.

        Returns:
            UiContext[UiElement]: The web driver instance.
        '''
        return SeleniumUiContext(self._web_driver)

    @override
    def setup_method(self):
        '''
        Initializes a Selenium WebDriver before each test method.

        If you need to customize browser options, override this method
        or configure settings in the [selenium] section of your .ini file.
        '''
        super().setup_method()
        self._web_driver = SeleniumUiContext.create_driver(self._configuration)

    @override
    def teardown_method(self):
        '''
        Quits the Selenium WebDriver after each test method.
        '''
        try:
            self._web_driver.quit()
        finally:
            super().teardown_method()
