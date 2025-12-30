# Base helpers shared across all pages.
# Handles fallback selectors, waiting, and simple interactions.

from playwright.sync_api import Page

from locators.dashboard_locators import SSR_WEBNAV_CONTAINER


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # Selector resolution
    def _first_available(self, selector: str):
        # Returns the first locator from a comma-separated list.
        # Does NOT pre-check visibility or existence.
        # Lets Playwright handle waiting, restoring original suite behaviour.
        for sel in [s.strip() for s in selector.split(",")]:
            return self.page.locator(sel)

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

    # Offline helpers
    def is_offline(self) -> bool:
        return self.page.context.offline

    def assert_offline(self) -> None:
        assert self.page.context.offline is True

    def assert_not_loaded(self, timeout: int = 3000) -> None:
        from pytest import raises

        with raises(Exception):  # noqa: B017
            self.wait_for_loaded(timeout=timeout)

    # Page-level load hook (optional override)
    def wait_for_loaded(self):
        # Child pages override this.
        pass

    # Helper to assert a page does NOT load
    def assert_page_does_not_load(self, wait_fn, timeout: int = 5000):
        # Give the UI time to attempt navigation.
        self.page.wait_for_timeout(timeout)

        # Attempt to wait for the page to load.
        # If it loads, this method returns normally (which is a failure for the test).
        # If it does NOT load, Playwright will raise, which the test expects.
        wait_fn()

    # Environment simulation helpers (safe, isolated, opt‑in)
    def apply_slow_network(self, delay_ms: int = 400):
        # Adds artificial latency to every network request without blocking
        def throttle(route):
            route.request.frame.page.wait_for_timeout(delay_ms)
            route.continue_()

        self.page.context.route("**/*", throttle)

    def remove_slow_network(self):
        # Removes the slow‑network routing rule and allows pending requests
        self.page.context.unroute("**/*")
        self.page.wait_for_timeout(500)
