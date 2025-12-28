# Flow wrapper that handles the full login sequence.
# Keeps the test code cleaner by encapsulating the steps.

from pages.login_identifier_page import LoginIdentifierPage
from pages.login_password_page import LoginPasswordPage
from pages.dashboard_page import DashboardPage


class LoginFlow:
    def __init__(self, page):
        self.page = page
        self.identifier = LoginIdentifierPage(page)
        self.password = LoginPasswordPage(page)
        self.dashboard = DashboardPage(page)

    def login(self, email: str, password: str) -> DashboardPage:
        # Go to login page
        self.identifier.goto()

        # Enter email
        self.identifier.submit_identifier(email)

        # Wait for password page
        self.password.wait_for_loaded()

        # Enter password
        self.password.submit_password(password)

        # Return dashboard page object
        return self.dashboard
