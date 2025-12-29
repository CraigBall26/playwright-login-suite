# Flow wrapper that handles the full login sequence.
# Keeps the test code cleaner by encapsulating the steps.

from pages.dashboard_page import DashboardPage
from pages.login_identifier_page import LoginIdentifierPage
from pages.login_password_page import LoginPasswordPage


class LoginFlow:
    def __init__(self, page, login_data):
        self.page = page
        self.login_url = login_data["login_url"]

        self.identifier = LoginIdentifierPage(page)
        self.password = LoginPasswordPage(page)
        self.dashboard = DashboardPage(page)

    def goto_login(self):
        self.page.goto(self.login_url)

    # Standard positive login flow.
    def login(self, email: str, password: str) -> DashboardPage:
        self.goto_login()
        self.identifier.submit_identifier(email)
        self.password.wait_for_loaded()
        self.password.submit_password(password)
        return self.dashboard

    # Login after correcting email using the Edit button.
    def login_after_edit(self, correct_email: str, password: str) -> DashboardPage:
        # Click the Edit Email link on the password page.
        self.password.click_edit_email()

        # Submit the corrected identifier.
        self.identifier.submit_identifier(correct_email)

        # Wait for the new password page.
        self.password.wait_for_loaded()

        # Submit password and complete login.
        self.password.submit_password(password)

        return self.dashboard

    # Login after correcting email using the browser Back button.
    def login_after_browser_back(
        self, correct_email: str, password: str
    ) -> DashboardPage:
        # Browser back returns to the identifier page.
        self.page.go_back()

        # Submit the corrected identifier.
        self.identifier.submit_identifier(correct_email)

        # Wait for the password page again.
        self.password.wait_for_loaded()

        # Submit password and complete login.
        self.password.submit_password(password)

        return self.dashboard

    # Attempt to edit identifier and login (negative test).
    def edit_identifier_and_attempt_login(self, new_email: str, password: str) -> None:
        # Click the Edit Email link on the password page.
        self.password.click_edit_email()

        # Submit the new identifier.
        self.identifier.submit_identifier(new_email)

        # Wait for the new password page.
        self.password.wait_for_loaded()

        # Attempt login with the provided password.
        self.password.submit_password(password)
