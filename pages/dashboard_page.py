# Page Objects for the Hudl dashboard page after a successful login.

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
        # Waits for the SSR WebNav container — the clearest signal the
        # dashboard has finished loading. Timeout is adjustable for
        # slow‑network environment tests.
        self.page.wait_for_selector(self.SSR_WEBNAV_CONTAINER, timeout=timeout)

    def open_user_menu(self):
        # Opens the user menu in the SSR WebNav header.
        # Prefer the existing button if visible
        if self.page.locator(self.USER_MENU_BUTTON).is_visible():
            self.page.click(self.USER_MENU_BUTTON)
        else:
            # Fallback to the initials avatar (hover-activated)
            self.page.hover(self.USER_MENU_DROPDOWN)

        # Wait for the logout button to appear
        self.page.wait_for_selector(self.LOGOUT_BUTTON, state="visible")

    def click_logout(self):
        # Clicks the logout button inside the user menu.
        self.page.click(self.LOGOUT_BUTTON)

    def any_dashboard_element_present(self) -> bool:
        # Used by negative login tests to confirm we did NOT reach the dashboard.
        return self.page.locator(self.SSR_WEBNAV_CONTAINER).is_visible()

    # Explicit assertions for clarity in tests
    def assert_on_dashboard(self) -> None:
        self.wait_for_loaded()
        assert "/home" in self.page.url

    def assert_not_on_dashboard(self) -> None:
        assert self.any_dashboard_element_present() is False
        assert "/home" not in self.page.url

    # Helper for slow-load scenarios
    def wait_for_loaded_slow(self):
        self.wait_for_loaded(timeout=20000)

    def logout(self):
        # Opens the user menu and clicks the logout button.
        # Hudl’s SSR WebNav requires a hover or button click to reveal the menu.
        self.open_user_menu()
        self.click_logout()
