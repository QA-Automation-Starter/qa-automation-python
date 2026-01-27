# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    Iterator,
    Optional,
    Self,
    Tuple,
    Union,
    final,
    overload,
)

from hamcrest.core.matcher import Matcher
from playwright.sync_api import Locator as PlaywrightLocator
from playwright.sync_api import Page
from qa_pytest_commons.generic_steps import GenericSteps
from qa_pytest_playwright.playwright_configuration import (
    PlaywrightConfiguration,
)
from qa_testing_utils.logger import Context


class LocatorWrapper:
    """
    Wrapper around Playwright Locator to provide Selenium-like .text property.

    This class wraps a Playwright Locator and delegates all method calls and attribute
    access to it, while providing an additional .text property for compatibility with
    Selenium-style code.
    """

    _locator: PlaywrightLocator

    def __init__(self, locator: PlaywrightLocator) -> None:
        object.__setattr__(self, '_locator', locator)

    @property
    def text(self) -> str:
        """Get element text content, returning empty string if None (matches Selenium behavior)."""
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
        """Return string representation delegating to wrapped Locator."""
        return repr(self._locator)

    def __str__(self) -> str:
        """Return string conversion delegating to wrapped Locator."""
        return str(self._locator)


@dataclass(frozen=True)
class Selector:
    """
    Represents an element selector as a (by, value) pair.

    Attributes:
        by (str): The locator strategy (e.g., By.ID, By.XPATH).
        value (str): The selector value.
    """
    by: str
    value: str

    def as_tuple(self) -> Tuple[str, str]:
        """
        Returns the selector as a tuple (by, value), suitable for Selenium APIs.

        Returns:
            Tuple[str, str]: The selector as a tuple.
        """
        return (self.by, self.value)


# Playwright locator strategies
class By:
    """
    Factory for element selectors, matching Playwright's locator API.

    Provides static methods to create Selector objects for each locator strategy.
    """

    @staticmethod
    def id(value: str) -> Selector:
        """
        Creates a selector for elements with the given id attribute.

        Args:
            value (str): The id value.
        Returns:
            Selector: The selector object.
        """
        return Selector("id", value)

    @staticmethod
    def xpath(value: str) -> Selector:
        """
        Creates a selector for elements matching the given XPath expression.

        Args:
            value (str): The XPath expression.
        Returns:
            Selector: The selector object.
        """
        return Selector("xpath", value)

    @staticmethod
    def link_text(value: str) -> Selector:
        """
        Creates a selector for elements with the given link text.

        Args:
            value (str): The link text.
        Returns:
            Selector: The selector object.
        """
        return Selector("text", value)

    @staticmethod
    def partial_link_text(value: str) -> Selector:
        """
        Creates a selector for elements with the given partial link text.

        Args:
            value (str): The partial link text.
        Returns:
            Selector: The selector object.
        """
        return Selector("text", value)

    @staticmethod
    def name(value: str) -> Selector:
        """
        Creates a selector for elements with the given name attribute.

        Args:
            value (str): The name value.
        Returns:
            Selector: The selector object.
        """
        return Selector("xpath", f"//input[@name='{value}']")

    @staticmethod
    def tag_name(value: str) -> Selector:
        """
        Creates a selector for elements with the given tag name.

        Args:
            value (str): The tag name.
        Returns:
            Selector: The selector object.
        """
        return Selector("xpath", f"//{value}")

    @staticmethod
    def class_name(value: str) -> Selector:
        """
        Creates a selector for elements with the given class name.

        Args:
            value (str): The class name.
        Returns:
            Selector: The selector object.
        """
        return Selector("xpath", f"//*[contains(@class, '{value}')]")

    @staticmethod
    def css_selector(value: str) -> Selector:
        """
        Creates a selector for elements matching the given CSS selector.

        Args:
            value (str): The CSS selector.
        Returns:
            Selector: The selector object.
        """
        return Selector("css", value)


type ElementSupplier = Callable[[], LocatorWrapper]
type SelectorOrSupplier = Union[Selector, ElementSupplier]


class PlaywrightSteps[TConfiguration: PlaywrightConfiguration](
    GenericSteps[TConfiguration]
):
    """
    BDD-style step definitions for Playwright-based UI operations.

    Type Parameters:
        TConfiguration: The configuration type, must be a PlaywrightConfiguration.

    Attributes:
        _page (Page): The Playwright Page instance used for browser automation.
    """

    _page: Page

    @final
    @Context.traced
    def a_page(self, page: Page) -> Self:
        """
        Sets the Playwright Page instance.

        Args:
            page (Page): The Playwright Page instance.
        Returns:
            Self: The current step instance for chaining.
        """
        self._page = page
        return self

    @final
    @Context.traced
    def at(self, url: str) -> Self:
        """
        Navigates to the specified URL with retry logic.

        Args:
            url (str): The URL to navigate to.
        Returns:
            Self: The current step instance for chaining.
        """
        def _navigate() -> Self:
            self._page.goto(url)
            return self

        return self.retrying(_navigate)

    @final
    @Context.traced
    def clicking_once(self, element_supplier: ElementSupplier) -> Self:
        """
        Clicks the element supplied by the given callable.

        Args:
            element_supplier (ElementSupplier): Callable returning a Playwright Locator.
        Returns:
            Self: The current step instance for chaining.
        """
        element_supplier().click()
        return self

    @overload
    def clicking(
        self, element: Selector) -> Self: ...

    @overload
    def clicking(
        self, element: ElementSupplier) -> Self: ...

    @final
    def clicking(self, element: SelectorOrSupplier) -> Self:
        """
        Clicks the element specified by a selector or supplier, with retry logic.

        Args:
            element (SelectorOrSupplier): Selector or callable returning a Playwright Locator.
        Returns:
            Self: The current step instance for chaining.
        """
        return self.retrying(lambda: self.clicking_once(self._resolve(element)))

    @final
    @Context.traced
    def typing_once(self, element_supplier: ElementSupplier, text: str) -> Self:
        """
        Types the given text into the element supplied by the callable.

        Args:
            element_supplier (ElementSupplier): Callable returning a Playwright Locator.
            text (str): The text to type.
        Returns:
            Self: The current step instance for chaining.
        """
        element = element_supplier()
        element.clear()
        element.fill(text)
        return self

    @overload
    def typing(self, element: Selector,
               text: str) -> Self: ...

    @overload
    def typing(self, element: ElementSupplier,
               text: str) -> Self: ...

    @final
    def typing(self, element: SelectorOrSupplier, text: str) -> Self:
        """
        Types the given text into the element specified by a selector or supplier, with retry logic.

        Args:
            element (SelectorOrSupplier): Selector or callable returning a Playwright Locator.
            text (str): The text to type.
        Returns:
            Self: The current step instance for chaining.
        """
        return self.retrying(lambda: self.typing_once(
            self._resolve(element),
            text))

    @final
    def the_element(
            self, selector: Selector, by_rule: Matcher[LocatorWrapper],
            context: Optional[Page] = None) -> Self:
        """
        Asserts that the element found by the selector matches the given matcher.

        Args:
            selector (Selector): The selector to find the element.
            by_rule (Matcher[LocatorWrapper]): Matcher for the element.
            context (Optional[Page]): Optional page context (defaults to _page).
        Returns:
            Self: The current step instance for chaining.
        """
        return self.eventually_assert_that(
            lambda: self._element(selector, context),
            by_rule)

    @final
    def the_elements(
            self, selector: Selector, by_rule:
            Matcher[Iterator[LocatorWrapper]],
            context: Optional[Page] = None) -> Self:
        """
        Asserts that the elements found by the selector match the given matcher.

        Args:
            selector (Selector): The selector to find the elements.
            by_rule (Matcher[Iterator[LocatorWrapper]]): Matcher for the elements iterator.
            context (Optional[Page]): Optional page context (defaults to _page).
        Returns:
            Self: The current step instance for chaining.
        """
        return self.eventually_assert_that(
            lambda: self._elements(selector, context),
            by_rule)

    @final
    @Context.traced
    def _elements(
        self, selector: Selector, context: Optional[Page] = None
    ) -> Iterator[LocatorWrapper]:
        page = context or self._page
        return (LocatorWrapper(loc) for loc in page.locator(self._build_playwright_selector(selector)).all())

    @final
    @Context.traced
    def _element(
        self, selector: Selector, context: Optional[Page] = None
    ) -> LocatorWrapper:
        page = context or self._page
        element = page.locator(self._build_playwright_selector(selector))
        self._scroll_into_view(element)
        return LocatorWrapper(element)

    def _scroll_into_view(
            self, element: PlaywrightLocator) -> PlaywrightLocator:
        element.scroll_into_view_if_needed()
        return element

    @final
    def _resolve(self, element: SelectorOrSupplier) -> ElementSupplier:
        if isinstance(element, Selector):
            return lambda: self._element(element)
        return element

    @staticmethod
    def _build_playwright_selector(selector: Selector) -> str:
        """
        Converts a Selector object to a Playwright selector string.

        Args:
            selector (Selector): The selector with strategy and value.
        Returns:
            str: The Playwright selector string.
        """
        if selector.by == "id":
            return f"#{selector.value}"
        elif selector.by == "xpath":
            return selector.value
        elif selector.by == "css":
            return selector.value
        elif selector.by == "text":
            return f"text={selector.value}"
        else:
            return selector.value
