# Page object for the password step of the login flow.

from playwright.sync_api import Page
from locators.login_password_locators import (
    PASSWORD_INPUT,
    CONTINUE_BUTTON,
    ERROR_MESSAGE,
)


class LoginPasswordPage:
    def __init__(self, page: Page):
        self.page = page
        self.password_input = page.locator(PASSWORD_INPUT)
        self.continue_button = page.locator(CONTINUE_BUTTON)
        self.error_message = page.locator(ERROR_MESSAGE)

    def submit_password(self, password: str):
        self.password_input.fill(password)
        self.continue_button.wait_for(state="visible")
        self.continue_button.click()

    def assert_incorrect_password_message(self):
        self.error_message.wait_for(state="visible")
