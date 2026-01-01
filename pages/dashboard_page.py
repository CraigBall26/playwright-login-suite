# Page Objects for the dashboard page after a successful login.
# Responsibilities:
# - confirming the authenticated dashboard has loaded
# - providing stable selectors for SSR WebNav
# - supporting logout flows and session tests
# - ensuring negative tests can reliably detect non-dashboard states

from locators.dashboard_locators import (
    LOGOUT_BUTTON,
    SSR_WEBNAV_CONTAINER,
    USER_MENU_BUTTON,
    USER_MENU_DROPDOWN,
)
from pages.base_page import BasePage


class DashboardPage(BasePage):
    # Stable selectors for detecting the real Hudl dashboard
    SSR_WEBNAV_CONTAINER = SSR_WEBNAV_CONTAINER
    USER_MENU_BUTTON = USER_MENU_BUTTON
    USER_MENU_DROPDOWN = USER_MENU_DROPDOWN
    LOGOUT_BUTTON = LOGOUT_BUTTON

    def wait_for_loaded(self, timeout=5000):
        # Use BasePage fallback logic so SSR variants are handled correctly.
        self.wait_for_selector(self.SSR_WEBNAV_CONTAINER, timeout=timeout)

    def open_user_menu(self):
        # Opens the user menu in the SSR WebNav header.
        if self.page.locator(self.USER_MENU_BUTTON).is_visible():
            self.page.click(self.USER_MENU_BUTTON)
        else:
            # Fallback to the initials avatar (hover-activated).
            self.page.hover(self.USER_MENU_DROPDOWN)

        # Give the menu time to fully render
        self.page.wait_for_timeout(150)

        # Wait for the logout button to appear.
        self.wait_for_selector(self.LOGOUT_BUTTON)

    def click_logout(self):
        self.page.click(self.LOGOUT_BUTTON)

    def any_dashboard_element_present(self) -> bool:
        return self.page.locator(self.SSR_WEBNAV_CONTAINER).is_visible()

    # Explicit assertions for clarity in tests
    def assert_on_dashboard(self) -> None:
        # Use BasePage helper for URL + UI confirmation
        self.wait_for_loaded()
        self.assert_url_contains("home")

    def assert_not_on_dashboard(self) -> None:
        # Negative login tests rely on UI absence
        assert self.any_dashboard_element_present() is False

    # Helper for slow-load scenarios
    def wait_for_loaded_slow(self):
        self.wait_for_loaded(timeout=20000)

    def logout(self):
        self.open_user_menu()
        self.click_logout()
