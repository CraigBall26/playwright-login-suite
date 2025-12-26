# Base helpers shared across all pages.
# Handles fallback selectors, waiting, and simple interactions.

from playwright.sync_api import Page

from locators.dashboard_locators import SSR_WEBNAV_CONTAINER


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def _first_available(self, selector: str):
        """
        Accepts a comma-separated selector string (fallbacks).
        Returns the first locator that exists on the page.
        """
        for sel in [s.strip() for s in selector.split(",")]:
            loc = self.page.locator(sel)
            if loc.count() > 0:
                return loc
        raise AssertionError(f"No selector matched: {selector}")

    def wait_and_click(self, selector: str, timeout: int = 5000):
        loc = self._first_available(selector)
        loc.wait_for(state="visible", timeout=timeout)
        loc.click()

    def wait_and_fill(self, selector: str, value: str, timeout: int = 5000):
        loc = self._first_available(selector)
        loc.wait_for(state="visible", timeout=timeout)
        loc.fill(value)

    def is_visible(self, selector: str, timeout: int = 3000) -> bool:
        try:
            loc = self._first_available(selector)
            loc.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def wait_for_selector(self, selector: str, timeout: int = 10000):
        """
        Generic wait helper used by child pages.
        Keeps waits consistent across the suite.
        """
        loc = self._first_available(selector)
        loc.wait_for(state="visible", timeout=timeout)
        return loc

    def wait_for_logged_in(self, timeout: int = 10000):
        """
        Confirms the user is fully logged in by waiting for the SSR WebNav container.
        This is the most stable post-login element for this account.
        """
        return self.wait_for_selector(SSR_WEBNAV_CONTAINER, timeout=timeout)
