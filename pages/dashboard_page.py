# Page object for the Hudl dashboard after login.

from playwright.sync_api import Page

from locators.dashboard_locators import SSR_WEBNAV_CONTAINER
from pages.base_page import BasePage


class DashboardPage(BasePage):
    # Expose the selector so tests can reference it directly
    SSR_WEBNAV_CONTAINER = SSR_WEBNAV_CONTAINER

    def __init__(self, page: Page):
        super().__init__(page)
        # Raw locator (may match multiple elements — handled by BasePage)
        self.nav_container = page.locator(SSR_WEBNAV_CONTAINER)

    # Ensure the dashboard is fully loaded before interacting.
    def wait_for_loaded(self):
        loc = self._first_available(self.SSR_WEBNAV_CONTAINER)
        self.wait_for_visible(loc)

    # Used by negative tests to confirm we did NOT reach the dashboard.
    def any_dashboard_element_present(self) -> bool:
        try:
            return self.nav_container.count() > 0
        except Exception:
            return False
