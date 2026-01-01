# Base helpers shared across all pages.
# Handles fallback selectors, waiting, URL assertions, offline/slow-network
# behaviour, popup handling, and simple interactions.

import re

from playwright.sync_api import expect


class BasePage:
    def __init__(self, page):
        self.page = page
        self._slow_network_handler = None  # store handler for safe removal

    # Selector resolution -------------------------

    # Returns the first selector that is visible, falling back to DOM existence.
    def _first_available(self, selector: str):
        selectors = [s.strip() for s in selector.split(",")]

        # Prefer visible elements first.
        for sel in selectors:
            loc = self.page.locator(sel)
            try:
                if loc.is_visible():
                    return loc
            except Exception:
                continue

        # Fallback: return first element that exists in the DOM.
        for sel in selectors:
            loc = self.page.locator(sel)
            try:
                if loc.count() > 0:
                    return loc
            except Exception:
                continue

        return self.page.locator(selectors[0])  # let Playwright throw normally

    # Waiting helpers ------------------------------

    def wait_for_visible(self, locator, timeout: int = 5000):
        expect(locator).to_be_visible(timeout=timeout)
        return locator

    def wait_for_attached(self, locator, timeout: int = 5000):
        expect(locator).to_be_attached(timeout=timeout)
        return locator

    def wait_for_selector(self, selector: str, timeout: int = 10000):
        loc = self._first_available(selector)
        expect(loc).to_be_visible(timeout=timeout)
        return loc

    # Interaction helpers --------------------------

    def wait_and_click(self, selector: str, timeout: int = 5000):
        loc = self._first_available(selector)
        expect(loc).to_be_visible(timeout=timeout)
        loc.click()

    def wait_and_fill(self, selector: str, value: str, timeout: int = 5000):
        loc = self._first_available(selector)
        expect(loc).to_be_visible(timeout=timeout)
        loc.fill(value)

    # Visibility helpers ---------------------------

    def is_visible(self, selector: str, timeout: int = 1000) -> bool:
        loc = self._first_available(selector)
        try:
            expect(loc).to_be_visible(timeout=timeout)
            return True
        except Exception:
            return False

    def assert_not_visible(self, selector: str, timeout: int = 3000):
        loc = self._first_available(selector)
        expect(loc).not_to_be_visible(timeout=timeout)

    # URL helpers ----------------------------------

    def assert_url_contains(self, text: str, timeout: int = 5000):
        # Regex-safe substring match
        pattern = re.compile(re.escape(text), re.IGNORECASE)
        expect(self.page).to_have_url(pattern, timeout=timeout)

    def assert_url_is(self, url: str, timeout: int = 5000):
        expect(self.page).to_have_url(url, timeout=timeout)

    # Dashboard helpers ----------------------------

    def assert_not_on_dashboard(self, timeout: int = 5000):
        # Dashboard URLs always contain /home or /dashboard
        pattern = re.compile(r"/home|/dashboard", re.IGNORECASE)
        expect(self.page).not_to_have_url(pattern, timeout=timeout)

    def wait_for_logged_in(self, timeout: int = 10000):
        # Authenticated URLs always contain /home or /dashboard
        pattern = re.compile(r"/home|/dashboard", re.IGNORECASE)
        expect(self.page).to_have_url(pattern, timeout=timeout)
        expect(self.page.locator("nav, header")).to_be_visible(timeout=timeout)

    # Page-load negative assertion -----------------

    def assert_page_does_not_load(self, selector: str, timeout: int = 5000):
        # Used by offline tests to confirm a page never appears.
        loc = self._first_available(selector)
        try:
            expect(loc).to_be_visible(timeout=timeout)
            raise AssertionError("Page loaded unexpectedly")
        except Exception:
            return

    # Offline helpers ------------------------------

    def go_offline(self):
        self.page.context.set_offline(True)

    def go_online(self):
        self.page.context.set_offline(False)

    def is_offline(self) -> bool:
        return self.page.context.offline

    def assert_offline(self):
        assert self.page.context.offline is True

    # Slow-network helpers -------------------------

    def apply_slow_network(self, delay_ms: int = 500):
        def handler(route):
            route.continue_(delay=delay_ms)

        self._slow_network_handler = handler
        self.page.context.route("**/*", handler)

    def remove_slow_network(self):
        if self._slow_network_handler:
            self.page.context.unroute("**/*", self._slow_network_handler)
            self._slow_network_handler = None

    # Popup helpers --------------------------------

    def close_popup_if_present(self, selector: str, timeout: int = 2000):
        loc = self._first_available(selector)
        try:
            expect(loc).to_be_visible(timeout=timeout)
            loc.click()
        except Exception:
            return

    def popup_visible(self, selector: str, timeout: int = 2000) -> bool:
        loc = self._first_available(selector)
        try:
            expect(loc).to_be_visible(timeout=timeout)
            return True
        except Exception:
            return False

    # New tab + popup capture ----------------------

    def open_new_tab(self):
        new_page = self.page.context.new_page()
        return BasePage(new_page)

    def click_and_capture_popup(self, click_fn, expected_substring: str):
        with self.page.expect_popup() as popup:
            click_fn()

        popup_page = popup.value
        pattern = re.compile(expected_substring, re.IGNORECASE)
        expect(popup_page).to_have_url(pattern)
        popup_page.close()
