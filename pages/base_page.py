# Base helpers shared across all pages.
# Handles fallback selectors, waiting, and simple interactions.

from playwright.sync_api import Page

from locators.dashboard_locators import SSR_WEBNAV_CONTAINER


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def _first_available(self, selector: str):
        # Returns the first locator that matches from a comma-separated list.
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
        # Waits for the first available selector from a comma-separated list.
        loc = self._first_available(selector)
        loc.wait_for(state="visible", timeout=timeout)
        return loc

    def wait_for_logged_in(self, timeout: int = 10000):
        # Waits for the global navigation to confirm logged-in state.
        return self.wait_for_selector(SSR_WEBNAV_CONTAINER, timeout=timeout)
