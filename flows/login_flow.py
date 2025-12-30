# Flow object that orchestrates the full login sequence.
# Handles identifier submission, password entry, and optional navigation paths.

from playwright.sync_api import Page

from pages.dashboard_page import DashboardPage
from pages.login_identifier_page import LoginIdentifierPage
from pages.login_password_page import LoginPasswordPage


class LoginFlow:
    def __init__(self, page: Page, login_data: dict):
        self.page = page
        self.login_data = login_data

        self.identifier = LoginIdentifierPage(page)
        self.password = LoginPasswordPage(page)

        # Restore compatibility with older tests (flow.base.identifier, etc.)
        self.base = self

    # Entry point for tests that start at the login screen
    def goto_login(self, timeout: int = 5000):
        self.identifier.goto_login(self.login_data["login_url"])
        self.identifier.wait_for_loaded(timeout=timeout)

    # Standard login path
    def login(self, email: str, password: str, timeout: int = 5000) -> DashboardPage:
        self.goto_login(timeout=timeout)
        self.identifier.submit_identifier(email)

        self.password.wait_for_loaded(timeout=timeout)
        self.password.submit_password(password)

        dashboard = DashboardPage(self.page)
        dashboard.wait_for_loaded(timeout=timeout)
        return dashboard

    def edit_identifier_and_attempt_login(
        self, new_email: str, password: str, timeout: int = 5000
    ) -> None:
        # Click Edit to return to identifier step
        self.password.click_edit_email()
        self.identifier.wait_for_loaded(timeout=timeout)

        # Submit the corrected identifier
        self.identifier.submit_identifier(new_email)

        # Continue login attempt
        self.password.wait_for_loaded(timeout=timeout)
        self.password.submit_password(password)

    # Login path after using browser Back from the password page
    def login_after_browser_back(
        self, correct_email: str, password: str, timeout: int = 5000
    ) -> DashboardPage:
        # Browser back to identifier step
        self.page.go_back()
        self.identifier.wait_for_loaded(timeout=timeout)

        # Submit corrected email
        self.identifier.submit_identifier(correct_email)

        # Continue login
        self.password.wait_for_loaded(timeout=timeout)
        self.password.submit_password(password)

        dashboard = DashboardPage(self.page)
        dashboard.wait_for_loaded(timeout=timeout)
        return dashboard

    # Login path after clicking Edit on the password page
    def login_after_edit(
        self, correct_email: str, password: str, timeout: int = 5000
    ) -> DashboardPage:
        # Click Edit to return to identifier step
        self.password.click_edit_email()

        self.identifier.wait_for_loaded(timeout=timeout)

        # Submit corrected email
        self.identifier.submit_identifier(correct_email)

        # Continue login
        self.password.wait_for_loaded(timeout=timeout)
        self.password.submit_password(password)

        dashboard = DashboardPage(self.page)
        dashboard.wait_for_loaded(timeout=timeout)
        return dashboard

    # Assertion helpers used by negative tests
    def assert_not_on_dashboard(self):
        DashboardPage(self.page).assert_not_on_dashboard()

    def assert_on_dashboard(self):
        DashboardPage(self.page).assert_on_dashboard()
