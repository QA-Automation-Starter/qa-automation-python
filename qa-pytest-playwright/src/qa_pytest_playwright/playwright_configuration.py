# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from functools import cached_property
from typing import Callable, final

from playwright.sync_api import Browser, Playwright
from qa_pytest_commons.base_configuration import BaseConfiguration


class PlaywrightConfiguration(BaseConfiguration):
    """
    PlaywrightConfiguration extends BaseConfiguration to provide Playwright-specific configuration options.

    This class exposes properties for retrieving the UI URL and initializing the Playwright browser launcher,
    leveraging configuration values and dynamic browser management.
    """

    @cached_property
    @final
    def landing_page(self) -> str:
        """
        Returns the UI URL from the configuration parser.

        Returns:
            str: The URL string specified under the "playwright/landing_page" in the configuration.

        Raises:
            KeyError: If the "playwright" section or "landing_page" key is not present in the configuration parser.
        """
        return self.parser["playwright"]["landing_page"]

    # FIXME Browser launcher here is currently specific to Chromium.
    # This method should be extended to support different browsers based on configuration.
    @cached_property
    @final
    def service(self) -> Callable[[Playwright], Browser]:
        """
        Creates and returns a browser launcher function.

        Returns:
            Callable[[Playwright], Browser]: A function that takes a Playwright instance and returns a Browser.
                Currently launches Chromium with headless=False and GPU disabled.

        Note:
            This method currently supports only Chromium, but may be extended to support different browsers
            (Firefox, WebKit) based on configuration in the future.
        """
        # NOTE may add support for providing different browser launchers per configuration
        def launch_browser(playwright: Playwright) -> Browser:
            return playwright.chromium.launch(
                headless=False, args=["--disable-gpu"]
            )
        return launch_browser
