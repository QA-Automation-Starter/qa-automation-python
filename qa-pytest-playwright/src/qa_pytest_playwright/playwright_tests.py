# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from typing import Any, override

from qa_pytest_commons.abstract_tests_base import AbstractTestsBase
from qa_pytest_playwright.playwright_configuration import (
    PlaywrightConfiguration,
)
from qa_pytest_playwright.playwright_steps import PlaywrightSteps


class PlaywrightTests[
    TSteps: PlaywrightSteps[Any],
    TConfiguration: PlaywrightConfiguration
](AbstractTestsBase[TSteps, TConfiguration]):
    """
    Base class for Playwright-based UI test cases.

    This class manages the lifecycle of a Playwright WebDriver for each test method.
    It is generic over the types of steps and configuration used.

    Attributes:
        _web_driver (WebDriver): The Playwright WebDriver instance (not thread safe).
    Type Parameters:
        TSteps: The type of the steps class, typically derived from PlaywrightSteps.
        TConfiguration: The type of the configuration class, typically derived from PlaywrightConfiguration.
    """
    # TODO not sure how the playwright interface is called and what its methods are
    # the initialization below should be adjusted accordingly
    # _web_driver: WebDriver  # not thread safe

    # @property
    # def web_driver(self) -> WebDriver:
    #     '''
    #     Returns the web driver instance.

    #     Returns:
    #         WebDriver: The web driver instance.
    #     '''
    #     return self._web_driver

    @override
    def setup_method(self):
        '''
        Initializes a local Chrome WebDriver before each test method.

        If you need to customize or use other driver, override this method in your test class.
        '''
        super().setup_method()

        # options = Options()
        # options.add_argument("--start-maximized")  # type: ignore
        # self._web_driver = Chrome(
        #     options,
        #     self._configuration.service)

    @override
    def teardown_method(self):
        '''
        Quits the Playwright WebDriver after each test method.
        '''
        # try:
        #     # self._web_driver.quit()
        # finally:
        #     super().teardown_method()
