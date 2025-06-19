# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from typing import Any, Generic, TypeVar, override

from qa_pytest_commons.abstract_tests_base import AbstractTestsBase
from qa_pytest_webdriver.selenium_configuration import SeleniumConfiguration
from qa_pytest_webdriver.selenium_steps import SeleniumSteps
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

# NOTE: python limitation; we cannot declare it such as:
# class SeleniumTests[TSteps:SeleniumSteps[TConfiguration], TConfiguration: SeleniumConfiguration](AbstractTestsBase[TSteps, TConfiguration]):
_TConfiguration = TypeVar("_TConfiguration", bound=SeleniumConfiguration)
# TSteps can be any subclass of SeleniumSteps, with any configuration type parameter.
# However, Python's type system cannot enforce that the parameter to SeleniumSteps is
# itself a subclass of SeleniumConfiguration; this is the closest we can get:
_TSteps = TypeVar("_TSteps", bound=SeleniumSteps[Any])


class SeleniumTests(
        Generic[_TSteps, _TConfiguration],
        AbstractTestsBase[_TSteps, _TConfiguration]):
    _web_driver: WebDriver  # not thread safe

    @property
    def web_driver(self) -> WebDriver:
        '''
        Returns the web driver instance.

        Returns:
            WebDriver: The web driver instance.
        '''
        return self._web_driver

    @override
    def setup_method(self):
        super().setup_method()

        options = Options()
        options.add_argument("--start-maximized")  # type: ignore
        self._web_driver = Chrome(
            options,
            self._configuration.service)

    @override
    def teardown_method(self):
        try:
            self._web_driver.quit()
        finally:
            super().teardown_method()
