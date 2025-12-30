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
        # Prefer the existing button if visible (your original behaviour)
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
