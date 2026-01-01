# High‑level flow for the login process.
# Handles:
# - navigating to the login page
# - completing identifier and password steps
# - returning the correct page object at each stage
# - supporting positive, negative, and environment tests

from pages.base_page import BasePage
from pages.dashboard_page import DashboardPage
from pages.login_identifier_page import LoginIdentifierPage
from pages.login_password_page import LoginPasswordPage


class LoginFlow:
    def __init__(self, page, login_data):
        self.page = page
        self.login_data = login_data

        # Page objects used throughout the flow
        self.identifier = LoginIdentifierPage(page)
        self.password = LoginPasswordPage(page)
        self.dashboard = DashboardPage(page)

        # BasePage reference (required by framework tests)
        self.base = BasePage(page)

    # Navigation -----------------------------------

    def goto_login(self):
        self.page.goto(self.login_data["login_url"])

    # Full login -----------------------------------

    def login(self, email: str, password: str):
        # Navigate to the login page FIRST
        self.goto_login()

        # Identifier step
        self.identifier.enter_email(email)
        self.identifier.submit()

        # Password step
        self.password.wait_for_loaded()
        self.password.enter_password(password)
        self.password.submit()

        # Dashboard
        self.dashboard.wait_for_loaded()
        return self.dashboard

    # Identifier-only step --------------------------

    def enter_identifier(self, email: str):
        self.identifier.enter_email(email)
        self.identifier.submit()
        return self.password

    # Password-only step ----------------------------

    def enter_password(self, password: str):
        self.password.wait_for_loaded()
        self.password.enter_password(password)
        self.password.submit()
        return self.dashboard

    # Login expecting failure -----------------------

    def login_expect_failure(self, email: str, password: str):
        self.identifier.enter_email(email)
        self.identifier.submit()

        self.password.wait_for_loaded()
        self.password.enter_password(password)
        self.password.submit()

        return self.password

    # Edit email + retry login
    def edit_identifier_and_attempt_login(self, new_email: str, password: str):
        # Click the "Edit email" link on the password page
        self.password.click_edit_email()

        # Now back on the identifier page
        self.identifier.wait_for_loaded()

        # Enter the new (unknown) email
        self.identifier.enter_email(new_email)
        self.identifier.submit()

        # Enter password for the new email
        self.password.enter_password(password)
        self.password.submit()
        return self.password

    # Browser back navigation -----------------------

    def login_after_browser_back(self, correct_email: str, password: str):
        self.page.go_back()

        self.identifier.wait_for_loaded()
        self.identifier.enter_email(correct_email)
        self.identifier.submit()

        self.password.wait_for_loaded()
        self.password.enter_password(password)
        self.password.submit()

        return self.dashboard

    # Edit email via UI link ------------------------

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
