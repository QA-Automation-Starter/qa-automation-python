# SPDX-FileCopyrightText: 2026 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0
import json
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
"""


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
        self._page.goto(url)

    def execute_script(self, script: str, *args: object) -> Any:
        return self._page.evaluate(script, *args)

    @staticmethod
    def create_browser_and_page(
        configuration: "UiConfiguration",
    ) -> tuple[Playwright, Browser, Page]:
        """
        Creates and returns a fully configured Playwright browser and page.

        Reads configuration from [playwright] section in the configuration parser.
        Supported settings:
        - browser: "chromium" (default), "chrome", "firefox", or "webkit"
        - headless: true/false (default: false)
        - maximize: true/false (default: false) - if true, uses full browser window (viewport=None)
        - launch_args: JSON array of browser launch arguments (e.g., ["--disable-gpu"])
        - viewport_width: int (default: 1920)
        - viewport_height: int (default: 1080)
        - Additional launch/context options can be specified as JSON:
          - launch_options: JSON object with Playwright launch() parameters
          - context_options: JSON object with new_context() parameters

        Args:
            configuration: UiConfiguration instance with parser access.

        Returns:
            tuple[Playwright, Browser, Page]: Playwright instance, browser, and page.

        Raises:
            ValueError: If an unsupported browser type is specified.
        """
        from playwright.sync_api import sync_playwright

        parser = configuration.parser
        playwright_section = parser["playwright"] if parser.has_section(
            "playwright") else {}

        browser_type = playwright_section.get("browser", "chromium").lower()
        headless = parser.getboolean("playwright", "headless", fallback=False)
        maximize = parser.getboolean("playwright", "maximize", fallback=False)
        viewport_width = parser.getint(
            "playwright", "viewport_width", fallback=1920)
        viewport_height = parser.getint(
            "playwright", "viewport_height", fallback=1080)

        # Build launch arguments
        launch_args: dict[str, Any] = {"headless": headless}

        # Add custom launch arguments from config
        if "launch_args" in playwright_section:
            launch_args["args"] = json.loads(playwright_section["launch_args"])

        # Merge custom launch options if specified
        if "launch_options" in playwright_section:
            custom_options = json.loads(playwright_section["launch_options"])
            launch_args.update(custom_options)

        # Start Playwright and launch browser
        playwright = sync_playwright().start()

        if browser_type in ("chromium", "chrome"):
            browser = playwright.chromium.launch(**launch_args)
        elif browser_type == "firefox":
            browser = playwright.firefox.launch(**launch_args)
        elif browser_type == "webkit":
            browser = playwright.webkit.launch(**launch_args)
        else:
            playwright.stop()
            raise ValueError(
                f"Unsupported browser type: {browser_type}. "
                f"Supported: chromium, chrome, firefox, webkit"
            )

        # Build context options
        if maximize:
            # viewport=None uses full browser window size
            context_args: dict[str, Any] = {"viewport": None}
        else:
            context_args = {
                "viewport": {"width": viewport_width, "height": viewport_height}
            }

        # Merge custom context options if specified
        if "context_options" in playwright_section:
            custom_context = json.loads(playwright_section["context_options"])
            context_args.update(custom_context)

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
