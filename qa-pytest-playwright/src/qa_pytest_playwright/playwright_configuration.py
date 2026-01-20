# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from functools import cached_property
from typing import Callable, final

from playwright.sync_api import Browser
from qa_pytest_commons.base_configuration import BaseConfiguration


class PlaywrightConfiguration(BaseConfiguration):
    """
    PlaywrightConfiguration extends BaseConfiguration to provide Playwright-specific configuration options.

    This class exposes properties for retrieving the UI URL and initializing the Playwright Service,
    leveraging configuration values and dynamic driver management.
    """

    @cached_property
    @final
    def landing_page(self) -> str:
        """
        Returns the UI URL from the configuration parser.

        Returns:
            str: The URL string specified under the "selenium/base" in the configuration.

        Raises:
            KeyError: If the "selenium" section or "base" key is not present in the configuration parser.
        """
        return self.parser["selenium"]["landing_page"]

    # TODO configure browser launch options based on configuration
    @cached_property
    @final
    def service(self) -> Callable[[], Browser]:
        """
        Creates and returns a callable that launches a Playwright browser instance using the sync API.

        Returns:
            Callable[[], Browser]: A callable that returns a Playwright Browser instance when invoked.
                The browser will be launched with default Chromium configuration.

        Note:
            This method currently launches Chromium by default but may be extended to support
            different browser engines based on configuration in the future.
        """
        from playwright.sync_api import sync_playwright

        def launch_browser() -> Browser:
            """Launch and return a Playwright browser instance."""
            playwright = sync_playwright().start()
            return playwright.chromium.launch()

        return launch_browser
