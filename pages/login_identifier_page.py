# Page object for the identifier (email) step of the login flow.

from playwright.sync_api import Page

from locators import login_identifier_locators as L  # noqa: N812
from pages.base_page import BasePage


class LoginIdentifierPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.email_input = page.locator(L.EMAIL_INPUT)
        self.continue_button = page.locator(L.CONTINUE_BUTTON)

    def goto(self, url: str):
        self.page.goto(url)

    # Ensure the identifier page is fully loaded before interacting.
    def goto_login(self, url: str):
        self.page.goto(url)
        self.wait_for_loaded()

    def wait_for_loaded(self, timeout=5000):
        # Wait for core elements to be visible. Timeout is adjustable for
        # slow‑network environment tests.
        self.wait_for_visible(self.email_input, timeout=timeout)
        self.wait_for_visible(self.continue_button, timeout=timeout)

    def submit_identifier(self, email: str):
        # Wait for email input to be visible before interacting
        self.wait_for_visible(self.email_input)
        self.wait_and_fill(L.EMAIL_INPUT, email)
        self.wait_and_click(L.CONTINUE_BUTTON)

    # Error assertions

    def assert_empty_email_error(self) -> None:
        self.page.locator(L.EMPTY_EMAIL_ERROR).wait_for(state="visible")

    def assert_invalid_email_error(self) -> None:
        self.page.locator(L.INVALID_EMAIL_ERROR).wait_for(state="visible")

    def assert_unknown_email_error(self) -> None:
        self.page.locator(L.UNKNOWN_EMAIL_ERROR).wait_for(state="visible")

    # Page-state assertions

    def assert_still_on_identifier_step(self) -> None:
        self.assert_url_contains("identifier")
        self.assert_url_not_contains("password")

    def assert_password_input_not_visible(self) -> None:
        self.assert_not_visible("input[type='password']")
