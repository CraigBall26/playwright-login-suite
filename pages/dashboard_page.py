# Page: Dashboard
# ----------------
# Handles the post-login dashboard view and provides helpers for verifying
# that the user has reached a logged-in state.

from locators import dashboard_locators as L  # noqa: N812
from pages.base_page import BasePage


class DashboardPage(BasePage):
    # Locators
    SSR_WEBNAV_CONTAINER = L.SSR_WEBNAV_CONTAINER

    def __init__(self, page):
        super().__init__(page)

    def wait_for_loaded(self):
        # Uses BasePage._first_available to confirm the nav container exists
        self._first_available(self.SSR_WEBNAV_CONTAINER)
