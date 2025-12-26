# Final step of the login flow.
# Confirms the user has successfully reached the authenticated dashboard.

# DashboardPage
# --------------
# Represents the Hudl dashboard after a successful login.
# This page object uses the SSR WebNav container as the anchor
# for confirming that the user has reached a logged‑in state.
#
# The selector chain comes from locators/dashboard_locators.py
# and includes a primary selector plus fallbacks for layout variations.

from pages.base_page import BasePage
from locators.dashboard_locators import SSR_WEBNAV_CONTAINER


class DashboardPage(BasePage):
    """
    Page object for the Hudl dashboard.
    Provides a stable post-login anchor using the SSR WebNav container.
    """

    def __init__(self, page):
        super().__init__(page)

    def wait_for_loaded(self):
        """
        Wait for the dashboard's global navigation to appear.
        This is the most reliable indicator that the user is logged in.
        """
        # Diagnostic: print the current URL so environment tests can see
        # exactly where the login flow ended up.
        print("CURRENT URL:", self.page.url)

        self.wait_for_selector(SSR_WEBNAV_CONTAINER)

    def wait_for_dashboard(self):
        """
        Public wrapper for waiting until the dashboard is ready.
        """
        self.wait_for_loaded()
