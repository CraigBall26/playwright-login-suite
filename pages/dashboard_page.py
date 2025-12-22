# Page object for the Hudl dashboard.
# Contains locators for interacting with the dashboard page.

import re


class DashboardPage:
    def __init__(self, page):
        self.page = page
        # Uses regex to match the user initials in the user menu. Regexes are fun.
        self.user_menu = page.get_by_role("heading", name=re.compile(r"^[A-Z]{2}$"))

    def wait_for_dashboard(self):
        # Wait until we're on any hudl.com page (e.g., /home, /dashboard, etc.)
        self.page.wait_for_url("**hudl.com/**", timeout=15000)

        # Wait for the user menu initials to appear in the top-right corner.
        self.user_menu.wait_for(state="visible")

    def assert_logged_in(self):
        # Confirms the user menu is visible.
        self.user_menu.wait_for(state="visible")
