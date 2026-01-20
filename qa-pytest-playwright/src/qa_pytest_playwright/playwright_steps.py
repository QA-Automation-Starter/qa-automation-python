# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass
from typing import Callable, Iterator, Optional, Tuple, Union, final, overload

from hamcrest.core.matcher import Matcher
from playwright.sync_api import Locator as PlaywrightLocator
from playwright.sync_api import Page
from qa_pytest_commons.generic_steps import GenericSteps
from qa_pytest_playwright.playwright_configuration import (
    PlaywrightConfiguration,
)
from qa_testing_utils.logger import Context


@dataclass(frozen=True)
class Locator:
    """
    Represents a Selenium locator as a (by, value) pair.

    Attributes:
        by (str): The Selenium locator strategy (e.g., By.ID, By.XPATH).
        value (str): The locator value.
    """
    by: str
    value: str

    def as_tuple(self) -> Tuple[str, str]:
        """
        Returns the locator as a tuple (by, value), suitable for Selenium APIs.

        Returns:
            Tuple[str, str]: The locator as a tuple.
        """
        return (self.by, self.value)


# Playwright locator strategies
class By:
    """
    Factory for Playwright locators, matching Playwright's locator API.

    Provides static methods to create Locator objects for each Playwright locator strategy.
    """

    @staticmethod
    def id(value: str) -> Locator:
        """
        Creates a locator for elements with the given id attribute.

        Args:
            value (str): The id value.
        Returns:
            Locator: The locator object.
        """
        return Locator("id", value)

    @staticmethod
    def xpath(value: str) -> Locator:
        """
        Creates a locator for elements matching the given XPath expression.

        Args:
            value (str): The XPath expression.
        Returns:
            Locator: The locator object.
        """
        return Locator("xpath", value)

    @staticmethod
    def link_text(value: str) -> Locator:
        """
        Creates a locator for elements with the given link text.

        Args:
            value (str): The link text.
        Returns:
            Locator: The locator object.
        """
        return Locator("text", value)

    @staticmethod
    def partial_link_text(value: str) -> Locator:
        """
        Creates a locator for elements with the given partial link text.

        Args:
            value (str): The partial link text.
        Returns:
            Locator: The locator object.
        """
        return Locator("text", value)

    @staticmethod
    def name(value: str) -> Locator:
        """
        Creates a locator for elements with the given name attribute.

        Args:
            value (str): The name value.
        Returns:
            Locator: The locator object.
        """
        return Locator("xpath", f"//input[@name='{value}']")

    @staticmethod
    def tag_name(value: str) -> Locator:
        """
        Creates a locator for elements with the given tag name.

        Args:
            value (str): The tag name.
        Returns:
            Locator: The locator object.
        """
        return Locator("xpath", f"//{value}")

    @staticmethod
    def class_name(value: str) -> Locator:
        """
        Creates a locator for elements with the given class name.

        Args:
            value (str): The class name.
        Returns:
            Locator: The locator object.
        """
        return Locator("xpath", f"//*[contains(@class, '{value}')]")

    @staticmethod
    def css_selector(value: str) -> Locator:
        """
        Creates a locator for elements matching the given CSS selector.

        Args:
            value (str): The CSS selector.
        Returns:
            Locator: The locator object.
        """
        return Locator("css", value)


type ElementSupplier = Callable[[], PlaywrightLocator]
type LocatorOrSupplier = Union[Locator, ElementSupplier]


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
    def clicking_once(self, element_supplier: ElementSupplier) -> "PlaywrightSteps[TConfiguration]":
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
        self, element: Locator) -> "PlaywrightSteps[TConfiguration]": ...

    @overload
    def clicking(
        self, element: ElementSupplier) -> "PlaywrightSteps[TConfiguration]": ...

    @final
    def clicking(self, element: LocatorOrSupplier) -> "PlaywrightSteps[TConfiguration]":
        """
        Clicks the element specified by a locator or supplier, with retry logic.

        Args:
            element (LocatorOrSupplier): Locator or callable returning a Playwright Locator.
        Returns:
            Self: The current step instance for chaining.
        """
        return self.retrying(lambda: self.clicking_once(self._resolve(element)))

    @final
    @Context.traced
    def typing_once(self, element_supplier: ElementSupplier, text: str) -> "PlaywrightSteps[TConfiguration]":
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
    def typing(self, element: Locator,
               text: str) -> "PlaywrightSteps[TConfiguration]": ...

    @overload
    def typing(self, element: ElementSupplier,
               text: str) -> "PlaywrightSteps[TConfiguration]": ...

    @final
    def typing(self, element: LocatorOrSupplier, text: str) -> "PlaywrightSteps[TConfiguration]":
        """
        Types the given text into the element specified by a locator or supplier, with retry logic.

        Args:
            element (LocatorOrSupplier): Locator or callable returning a Playwright Locator.
            text (str): The text to type.
        Returns:
            Self: The current step instance for chaining.
        """
        return self.retrying(lambda: self.typing_once(
            self._resolve(element),
            text))

    @final
    def the_element(
            self, locator: Locator, by_rule: Matcher[PlaywrightLocator],
            context: Optional[Page] = None) -> "PlaywrightSteps[TConfiguration]":
        """
        Asserts that the element found by the locator matches the given matcher.

        Args:
            locator (Locator): The locator to find the element.
            by_rule (Matcher[PlaywrightLocator]): Matcher for the element.
            context (Optional[Page]): Optional page context (defaults to _page).
        Returns:
            Self: The current step instance for chaining.
        """
        return self.eventually_assert_that(
            lambda: self._element(locator, context),
            by_rule)

    @final
    def the_elements(
            self, locator: Locator, by_rule:
            Matcher[Iterator[PlaywrightLocator]],
            context: Optional[Page] = None) -> "PlaywrightSteps[TConfiguration]":
        """
        Asserts that the elements found by the locator match the given matcher.

        Args:
            locator (Locator): The locator to find the elements.
            by_rule (Matcher[Iterator[PlaywrightLocator]]): Matcher for the elements iterator.
            context (Optional[Page]): Optional page context (defaults to _page).
        Returns:
            Self: The current step instance for chaining.
        """
        return self.eventually_assert_that(
            lambda: self._elements(locator, context),
            by_rule)

    @final
    @Context.traced
    def _elements(
        self, locator: Locator, context: Optional[Page] = None
    ) -> Iterator[PlaywrightLocator]:
        page = context or self._page
        return iter(page.locator(self._build_playwright_selector(locator)).all())

    @final
    @Context.traced
    def _element(
        self, locator: Locator, context: Optional[Page] = None
    ) -> PlaywrightLocator:
        page = context or self._page
        element = page.locator(self._build_playwright_selector(locator))
        self._scroll_into_view(element)
        return element

    def _scroll_into_view(
            self, element: PlaywrightLocator) -> PlaywrightLocator:
        element.scroll_into_view_if_needed()
        return element

    @final
    def _resolve(self, element: LocatorOrSupplier) -> ElementSupplier:
        if isinstance(element, Locator):
            return lambda: self._element(element)
        return element

    @staticmethod
    def _build_playwright_selector(locator: Locator) -> str:
        """
        Converts a Locator object to a Playwright selector string.

        Args:
            locator (Locator): The locator with strategy and value.
        Returns:
            str: The Playwright selector string.
        """
        if locator.by == "id":
            return f"#{locator.value}"
        elif locator.by == "xpath":
            return locator.value
        elif locator.by == "css":
            return locator.value
        elif locator.by == "text":
            return f"text={locator.value}"
        else:
            return locator.value
