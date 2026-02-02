# SPDX-FileCopyrightText: 2026 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0
import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Iterator, Optional

from playwright.sync_api import Browser
from playwright.sync_api import Locator as PlaywrightLocator
from playwright.sync_api import Page, Playwright
from qa_pytest_commons.selector import Selector
from qa_pytest_commons.ui_protocols import UiContext, UiElement

if TYPE_CHECKING:
    from qa_pytest_commons.ui_configuration import UiConfiguration

"""
Playwright adapter for backend-agnostic UiElement and UiContext protocols.
Supports cross-platform browsers: Chromium, Firefox, WebKit
"""


@dataclass
class PlaywrightConfig:
    """Configuration for Playwright browser creation."""
    browser: str
    headless: bool
    maximize: bool
    viewport_width: int
    viewport_height: int
    launch_args: list[str]
    launch_options: dict[str, Any]
    context_options: dict[str, Any]

    @classmethod
    def from_parser(cls, parser: Any) -> "PlaywrightConfig":
        """Parse Playwright configuration from INI parser."""
        playwright_section = parser["playwright"] if parser.has_section(
            "playwright") else {}

        browser = playwright_section.get("browser", "chromium").lower()
        headless = parser.getboolean("playwright", "headless", fallback=False)
        maximize = parser.getboolean("playwright", "maximize", fallback=False)
        viewport_width = parser.getint(
            "playwright", "viewport_width", fallback=1920)
        viewport_height = parser.getint(
            "playwright", "viewport_height", fallback=1080)

        launch_args = []
        if "launch_args" in playwright_section:
            launch_args = json.loads(playwright_section["launch_args"])

        launch_options = {}
        if "launch_options" in playwright_section:
            launch_options = json.loads(playwright_section["launch_options"])

        context_options = {}
        if "context_options" in playwright_section:
            context_options = json.loads(playwright_section["context_options"])

        return cls(
            browser=browser,
            headless=headless,
            maximize=maximize,
            viewport_width=viewport_width,
            viewport_height=viewport_height,
            launch_args=launch_args,
            launch_options=launch_options,
            context_options=context_options,
        )


class PlaywrightUiElement(UiElement):
    """
    Playwright adapter for UiElement protocol.
    Wraps a Playwright Locator and implements the backend-agnostic UiElement interface.
    """

    _locator: PlaywrightLocator

    def __init__(self, locator: PlaywrightLocator) -> None:
        object.__setattr__(self, '_locator', locator)

    def click(self) -> None:
        self._locator.click()

    def type(self, text: str) -> None:
        self._locator.clear()
        self._locator.fill(text)

    def clear(self) -> None:
        self._locator.clear()

    def scroll_into_view(self) -> None:
        self._locator.scroll_into_view_if_needed()

    def execute_script(self, script: str, *args: object) -> object:
        """Execute script on this element using the page's evaluate method."""
        return self._locator.evaluate(script, *args)

    @property
    def text(self) -> str:
        """Get element text content, returning empty string if None."""
        return self._locator.text_content() or ""

    def __getattr__(self, name: str) -> Any:
        """Delegate all other attribute access to the wrapped Playwright Locator."""
        return getattr(self._locator, name)

    def __setattr__(self, name: str, value: Any) -> None:
        """Delegate attribute setting to the wrapped Playwright Locator."""
        if name == '_locator':
            object.__setattr__(self, name, value)
        else:
            setattr(self._locator, name, value)

    def __repr__(self) -> str:
        return repr(self._locator)

    def __str__(self) -> str:
        return str(self._locator)


# Alias for backward compatibility
LocatorWrapper = PlaywrightUiElement


class PlaywrightUiContext(UiContext[PlaywrightUiElement]):
    _page: Page

    def __init__(self, page: Page) -> None:
        self._page = page

    def find_element(
            self, by: str, value: Optional[str]) -> PlaywrightUiElement:
        selector_str = self._build_playwright_selector(
            Selector(by, value or ""))
        return PlaywrightUiElement(self._page.locator(selector_str).first)

    def find_elements(
            self, by: str, value: Optional[str]) -> Iterator[PlaywrightUiElement]:
        selector_str = self._build_playwright_selector(
            Selector(by, value or ""))
        return (PlaywrightUiElement(e) for e in self._page.locator(selector_str).all())

    def get(self, url: str) -> None:
        # Use a reasonable timeout to prevent hanging, Playwright default is 30 seconds
        # but we make it explicit and use wait_until="networkidle" to ensure page is fully loaded
        self._page.goto(url, wait_until="networkidle")

    def execute_script(self, script: str, *args: object) -> Any:
        return self._page.evaluate(script, *args)

    @staticmethod
    def _launch_browser(
        playwright: Playwright, browser_type: str, launch_args: dict[str, Any]
    ) -> Browser:
        """Launch browser based on type."""
        if browser_type in ("chromium", "chrome"):
            return playwright.chromium.launch(**launch_args)
        elif browser_type == "firefox":
            return playwright.firefox.launch(**launch_args)
        elif browser_type == "webkit":
            return playwright.webkit.launch(**launch_args)
        else:
            raise ValueError(
                f"Unsupported browser type: {browser_type}. "
                f"Supported: chromium, chrome, firefox, webkit"
            )

    @staticmethod
    def _build_context_args(config: PlaywrightConfig) -> dict[str, Any]:
        """Build context arguments based on configuration."""
        # For maximize, use full screen dimensions instead of viewport: None
        # which can cause issues with Firefox
        if config.maximize:
            context_args: dict[str, Any] = {
                "viewport": {"width": 1920, "height": 1080}
            }
        else:
            context_args = {"viewport": {
                "width": config.viewport_width, "height": config.viewport_height}}

        # Merge custom context options
        context_args.update(config.context_options)
        return context_args

    @staticmethod
    def _build_launch_args(config: PlaywrightConfig) -> dict[str, Any]:
        """Build browser launch arguments based on configuration."""
        launch_args: dict[str, Any] = {"headless": config.headless}

        if config.launch_args:
            launch_args["args"] = config.launch_args
        launch_args.update(config.launch_options)
        return launch_args

    @staticmethod
    def create_browser_and_page(
        configuration: "UiConfiguration",
    ) -> tuple[Playwright, Browser, Page]:
        """
        Creates and returns a fully configured Playwright browser and page.

        Reads configuration from [playwright] section in the configuration parser.

        Supported browsers (cross-platform):
        - chromium, chrome (default)
        - firefox
        - webkit

        Configuration options:
        - browser: str (default: chromium)
        - headless: bool (default: false)
        - maximize: bool (default: false)
        - viewport_width: int (default: 1920)
        - viewport_height: int (default: 1080)
        - launch_args: JSON array (optional)
        - launch_options: JSON object (optional)
        - context_options: JSON object (optional)

        Args:
            configuration: UiConfiguration instance with parser access.

        Returns:
            tuple[Playwright, Browser, Page]: Playwright instance, browser, and page.

        Raises:
            ValueError: If an unsupported browser type is specified.
        """
        from playwright.sync_api import sync_playwright

        config = PlaywrightConfig.from_parser(configuration.parser)

        # Build launch arguments
        launch_args = PlaywrightUiContext._build_launch_args(config)

        # Start Playwright and launch browser
        playwright = sync_playwright().start()
        try:
            browser = PlaywrightUiContext._launch_browser(
                playwright, config.browser, launch_args)
        except ValueError:
            playwright.stop()
            raise

        # Create page with context options
        context_args = PlaywrightUiContext._build_context_args(config)
        page = browser.new_page(**context_args)

        return playwright, browser, page

    @staticmethod
    def _build_playwright_selector(selector: Selector) -> str:
        """
        Converts a Selector object to a Playwright selector string.
        """
        if selector.by == "id":
            return f"#{selector.value}"
        elif selector.by == "xpath":
            return selector.value
        elif selector.by == "css selector":
            return selector.value
        elif selector.by == "link text":
            return f"text={selector.value}"
        elif selector.by == "partial link text":
            return f"text={selector.value}"
        elif selector.by == "name":
            return f"[name='{selector.value}']"
        elif selector.by == "tag name":
            return selector.value
        elif selector.by == "class name":
            return f".{selector.value}"
        else:
            return selector.value
