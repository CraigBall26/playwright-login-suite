# Final step of the login flow.
# Confirms the user has successfully reached the authenticated dashboard.

from locators.dashboard_locators import SSR_WEBNAV_CONTAINER
from pages.base_page import BasePage


class DashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def wait_for_loaded(self):
        # Uses the full fallback chain from the repo.
        # Ensures the test passes across all Hudl dashboard variants.
        self.wait_for_selector(SSR_WEBNAV_CONTAINER)

    def wait_for_dashboard(self):
        self.wait_for_loaded()
