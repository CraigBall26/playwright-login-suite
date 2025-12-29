# Flow wrapper that handles the full login sequence.
# Keeps the test code cleaner by encapsulating the steps.

from pages.dashboard_page import DashboardPage
from pages.login_identifier_page import LoginIdentifierPage
from pages.login_password_page import LoginPasswordPage


class LoginFlow:
    def __init__(self, page, login_data):
        self.page = page
        self.login_data = login_data

        self.identifier = LoginIdentifierPage(page)
        self.password = LoginPasswordPage(page)
        self.dashboard = DashboardPage(page)

    def goto_login(self):
        # Navigate using the URL stored in test_data
        self.identifier.goto(self.login_data["login_url"])

    def login(self, email: str, password: str) -> DashboardPage:
        # Go to login page
        self.goto_login()

        # Enter email
        self.identifier.submit_identifier(email)

        # Wait for password page
        self.password.wait_for_loaded()

        # Enter password
        self.password.submit_password(password)

        # Return dashboard page object
        return self.dashboard
