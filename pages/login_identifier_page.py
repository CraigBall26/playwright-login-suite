# Page object for the identifier (email) step of the login flow.
# Keeping selectors simple and readable for stability and reviewer clarity.

from playwright.sync_api import Page
from locators.login_identifier_locators import (
    EMAIL_INPUT,
    CONTINUE_BUTTON,
    ERROR_MESSAGE,
)


class LoginIdentifierPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_input = page.locator(EMAIL_INPUT)
        self.continue_button = page.locator(CONTINUE_BUTTON)

    # Navigate directly to the Hudl login page.
    def goto(self):
        self.page.goto("https://www.hudl.com/login")
        self.email_input.wait_for(state="visible")

    # Enter the email address and continue to the password page.
    def submit_identifier(self, email: str):
        self.email_input.fill(email)
        self.continue_button.wait_for(state="visible")
        self.continue_button.click()

    # Auth0 shows incorrect password errors on THIS page, not the password page.
    def assert_incorrect_password_message(self):
        error = self.page.locator(ERROR_MESSAGE)
        error.wait_for(state="visible")
