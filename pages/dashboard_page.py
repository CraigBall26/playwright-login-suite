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
        self.page = page

    def wait_for_loaded(self):
        # Uses BasePage._first_available to confirm the nav container exists
        self._first_available(self.SSR_WEBNAV_CONTAINER)

    # Negative-check helper: returns True if ANY selector matches
    def any_dashboard_element_present(self) -> bool:
        for sel in [s.strip() for s in self.SSR_WEBNAV_CONTAINER.split(",")]:
            if self.page.locator(sel).count() > 0:
                return True
        return False
