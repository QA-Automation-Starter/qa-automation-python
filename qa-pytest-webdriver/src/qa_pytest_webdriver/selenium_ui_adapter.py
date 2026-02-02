# SPDX-FileCopyrightText: 2026 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0
from typing import TYPE_CHECKING, Any, Iterator, Optional

from qa_pytest_commons.ui_protocols import UiContext, UiElement
from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

if TYPE_CHECKING:
    from qa_pytest_commons.ui_configuration import UiConfiguration

"""
Selenium adapter for backend-agnostic UiElement and UiContext protocols.
"""


class SeleniumUiElement(WebElement, UiElement):
    def __init__(self, element: WebElement) -> None:
        # Copy all attributes from the original WebElement
        self.__dict__ = element.__dict__

    def type(self, text: str) -> None:
        super().clear()
        super().send_keys(text)

    def scroll_into_view(self) -> None:
        self.parent.execute_script(  # type: ignore[attr-defined]
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            self)

    @property
    def text(self) -> str:
        return super().text


class SeleniumUiContext(UiContext[SeleniumUiElement]):
    _driver: WebDriver

    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver

    def find_element(self, by: str, value: Optional[str]) -> SeleniumUiElement:
        return SeleniumUiElement(self._driver.find_element(by, value))

    def find_elements(
            self, by: str, value: Optional[str]) -> Iterator[SeleniumUiElement]:
        return (SeleniumUiElement(e) for e in self._driver.find_elements(by, value))

    def get(self, url: str) -> None:
        self._driver.get(url)

    def execute_script(self, script: str, *args: UiElement) -> Any:
        return self._driver.execute_script(script, *args)  # type: ignore

    @staticmethod
    def create_driver(configuration: "UiConfiguration") -> WebDriver:
        """
        Creates and returns a fully configured Selenium WebDriver.

        Reads configuration from [selenium] section in the configuration parser.
        Supported settings:
        - browser: "chrome", "chromium" (default), or "firefox"
        - headless: true/false (default: false)
        - maximize: true/false (default: false) - if true, ignores window_width/height
        - window_width: int (default: 1920)
        - window_height: int (default: 1080)
        - Additional browser-specific arguments can be specified as:
          - chrome_arguments: comma-separated list
          - firefox_arguments: comma-separated list

        Args:
            configuration: UiConfiguration instance with parser access.

        Returns:
            WebDriver: Fully configured Selenium WebDriver instance.

        Raises:
            ValueError: If an unsupported browser type is specified.
        """
        parser = configuration.parser
        selenium_section = parser["selenium"] if parser.has_section(
            "selenium") else {}

        browser = selenium_section.get("browser", "chromium").lower()
        headless = parser.getboolean("selenium", "headless", fallback=False)
        maximize = parser.getboolean("selenium", "maximize", fallback=False)
        window_width = parser.getint("selenium", "window_width", fallback=1920)
        window_height = parser.getint(
            "selenium", "window_height", fallback=1080)

        if browser == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("-headless")

            # Add custom Firefox arguments if specified
            if "firefox_arguments" in selenium_section:
                for arg in selenium_section["firefox_arguments"].split(","):
                    options.add_argument(arg.strip())

            service = FirefoxService(GeckoDriverManager().install())
            driver = Firefox(options=options, service=service)
        elif browser in ("chromium", "chrome"):
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")

            # Add custom Chrome arguments if specified
            if "chrome_arguments" in selenium_section:
                for arg in selenium_section["chrome_arguments"].split(","):
                    options.add_argument(arg.strip())

            service = ChromeService(ChromeDriverManager().install())
            driver = Chrome(options=options, service=service)
        else:
            raise ValueError(
                f"Unsupported browser type: {browser}. "
                f"Supported: chromium, chrome, firefox"
            )

        if maximize:
            driver.maximize_window()
        else:
            driver.set_window_size(window_width, window_height)
        return driver
