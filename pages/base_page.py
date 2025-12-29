# Base helpers shared across all pages.
# Handles fallback selectors, waiting, and simple interactions.

from playwright.sync_api import Page

from locators.dashboard_locators import SSR_WEBNAV_CONTAINER


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # Selector resolution
    def _first_available(self, selector: str):
        # Returns the first locator that matches from a comma-separated list.
        for sel in [s.strip() for s in selector.split(",")]:
            loc = self.page.locator(sel)
            if loc.count() > 0:
                return loc
        raise AssertionError(f"No selector matched: {selector}")

    # Waiting helpers
    def wait_for_visible(self, locator, timeout: int = 5000):
        locator.wait_for(state="visible", timeout=timeout)
        return locator

    def wait_for_attached(self, locator, timeout: int = 5000):
        locator.wait_for(state="attached", timeout=timeout)
        return locator

    def wait_for_url_contains(self, text: str, timeout: int = 15000):
        self.page.wait_for_url(f"**{text}**", timeout=timeout)

    def wait_for_selector(self, selector: str, timeout: int = 10000):
        loc = self._first_available(selector)
        loc.wait_for(state="visible", timeout=timeout)
        return loc

    # Interaction helpers
    def wait_and_click(self, selector: str, timeout: int = 5000):
        loc = self._first_available(selector)
        loc.wait_for(state="visible", timeout=timeout)
        loc.click()

    def wait_and_fill(self, selector: str, value: str, timeout: int = 5000):
        loc = self._first_available(selector)
        loc.wait_for(state="visible", timeout=timeout)
        loc.fill(value)

    # Visibility check
    def is_visible(self, selector: str, timeout: int = 3000) -> bool:
        try:
            loc = self._first_available(selector)
            loc.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    # URL assertions
    def assert_url_contains(self, text: str) -> None:
        assert text in self.page.url

    def assert_url_not_contains(self, text: str) -> None:
        assert text not in self.page.url

    # Visibility assertions
    def assert_not_visible(self, selector: str) -> None:
        element = self.page.locator(selector)
        assert element.is_visible() is False

    # Dashboard assertions
    def assert_not_on_dashboard(self) -> None:
        from pages.dashboard_page import DashboardPage

        dashboard = DashboardPage(self.page)
        assert dashboard.any_dashboard_element_present() is False
        assert "/home" not in self.page.url

    # Logged-in check
    def wait_for_logged_in(self, timeout: int = 10000):
        return self.wait_for_selector(SSR_WEBNAV_CONTAINER, timeout=timeout)

    # Page-level load hook (optional override)
    def wait_for_loaded(self):
        # Child pages override this.
        pass
