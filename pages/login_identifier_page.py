# Page object for the identifier (email) step of the login flow.

from playwright.sync_api import Page

from locators import login_identifier_locators as L  # noqa: N812
from pages.base_page import BasePage


class LoginIdentifierPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.email_input = page.locator(L.EMAIL_INPUT)
        self.continue_button = page.locator(L.CONTINUE_BUTTON)

    def goto(self):
        # Correct URL from your repo
        self.page.goto("https://www.hudl.com/login")

    def wait_for_loaded(self):
        # Use BasePage helpers for consistency
        self.wait_for_visible(self.email_input)
        self.wait_for_visible(self.continue_button)

    def submit_identifier(self, email: str):
        # Consistent with BasePage helpers
        self.wait_for_visible(self.email_input)
        self.email_input.fill(email)
        self.continue_button.click()
