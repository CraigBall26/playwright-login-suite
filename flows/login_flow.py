# Flow wrapper that handles the full login sequence.
# Keeps the test code cleaner by encapsulating the steps.

from pages.base_page import BasePage
from pages.dashboard_page import DashboardPage
from pages.login_identifier_page import LoginIdentifierPage
from pages.login_password_page import LoginPasswordPage


class LoginFlow:
    def __init__(self, page, login_data=None):
        self.page = page

        # Allow negative tests (like TC‑106) to skip passing login_data.
        # Positive tests still pass the full JSON object.
        self.login_url = (
            login_data["login_url"] if login_data else "https://www.hudl.com/login"
        )

        # Base helpers (URL checks, visibility checks, dashboard checks)
        self.base = BasePage(page)

        # Page objects
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
        self.password.click_edit_email()
        self.identifier.submit_identifier(correct_email)
        self.password.wait_for_loaded()
        self.password.submit_password(password)
        return self.dashboard

    # Login after correcting email using the browser Back button.
    def login_after_browser_back(
        self, correct_email: str, password: str
    ) -> DashboardPage:
        # Try to go back using browser history.
        try:
            self.page.go_back(wait_until="domcontentloaded")
        except Exception:
            # In CI, Auth0 often collapses the identifier page out of history.
            # Fall back to manually navigating to the login URL.
            self.page.goto(self.login_url)

        # Now guaranteed to be on the identifier step.
        self.identifier.submit_identifier(correct_email)
        self.password.wait_for_loaded()
        self.password.submit_password(password)
        return self.dashboard

    # Attempt to edit identifier and login (negative test).
    def edit_identifier_and_attempt_login(self, new_email: str, password: str) -> None:
        self.password.click_edit_email()
        self.identifier.submit_identifier(new_email)
        self.password.wait_for_loaded()
        self.password.submit_password(password)
