# SPDX-FileCopyrightText: 2026 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import dataclass
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
Supports cross-platform browsers: Chrome/Chromium, Firefox
"""


@dataclass
class SeleniumConfig:
    """Configuration for Selenium WebDriver creation."""
    browser: str
    headless: bool
    maximize: bool
    window_width: int
    window_height: int
    chrome_arguments: list[str]
    firefox_arguments: list[str]

    @classmethod
    def from_parser(cls, parser: Any) -> "SeleniumConfig":
        """Parse Selenium configuration from INI parser."""
        selenium_section = parser["selenium"] if parser.has_section(
            "selenium") else {}

        browser = selenium_section.get("browser", "chromium").lower()
        headless = parser.getboolean("selenium", "headless", fallback=False)
        maximize = parser.getboolean("selenium", "maximize", fallback=False)
        window_width = parser.getint("selenium", "window_width", fallback=1920)
        window_height = parser.getint(
            "selenium", "window_height", fallback=1080)

        chrome_args = []
        if "chrome_arguments" in selenium_section:
            chrome_args = [
                arg.strip()
                for arg in selenium_section["chrome_arguments"].split(",")]

        firefox_args = []
        if "firefox_arguments" in selenium_section:
            firefox_args = [
                arg.strip()
                for arg in selenium_section["firefox_arguments"].split(",")]

        return cls(
            browser=browser,
            headless=headless,
            maximize=maximize,
            window_width=window_width,
            window_height=window_height,
            chrome_arguments=chrome_args,
            firefox_arguments=firefox_args,
        )


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
    def _create_chrome(config: SeleniumConfig) -> WebDriver:
        """Create Chrome/Chromium WebDriver."""
        options = ChromeOptions()
        if config.headless:
            options.add_argument("--headless=new")
        for arg in config.chrome_arguments:
            options.add_argument(arg)

        service = ChromeService(ChromeDriverManager().install())
        driver = Chrome(options=options, service=service)
        return driver

    @staticmethod
    def _create_firefox(config: SeleniumConfig) -> WebDriver:
        """Create Firefox WebDriver."""
        options = FirefoxOptions()
        if config.headless:
            options.add_argument("-headless")
        for arg in config.firefox_arguments:
            options.add_argument(arg)

        service = FirefoxService(GeckoDriverManager().install())
        driver = Firefox(options=options, service=service)
        return driver

    @staticmethod
    def _apply_window_settings(
            driver: WebDriver, config: SeleniumConfig) -> None:
        """Apply window size or maximize settings."""
        if config.maximize:
            driver.maximize_window()
        else:
            driver.set_window_size(config.window_width, config.window_height)

    @staticmethod
    def create_driver(configuration: "UiConfiguration") -> WebDriver:
        """
        Creates and returns a fully configured Selenium WebDriver.

        Reads configuration from [selenium] section in the configuration parser.

        Supported browsers (cross-platform):
        - chromium, chrome (default)
        - firefox

        Configuration options:
        - browser: str (default: chromium)
        - headless: bool (default: false)
        - maximize: bool (default: false)
        - window_width: int (default: 1920)
        - window_height: int (default: 1080)
        - chrome_arguments: comma-separated string (optional)
        - firefox_arguments: comma-separated string (optional)

        Args:
            configuration: UiConfiguration instance with parser access.

        Returns:
            WebDriver: Fully configured Selenium WebDriver instance.

        Raises:
            ValueError: If an unsupported browser type is specified.
        """
        config = SeleniumConfig.from_parser(configuration.parser)

        if config.browser in ("chromium", "chrome"):
            driver = SeleniumUiContext._create_chrome(config)
        elif config.browser == "firefox":
            driver = SeleniumUiContext._create_firefox(config)
        else:
            raise ValueError(
                f"Unsupported browser type: {config.browser}. "
                f"Supported: chromium, chrome, firefox"
            )

        SeleniumUiContext._apply_window_settings(driver, config)
        return driver
