# Second step/page of a two-step login flow.
# Handles entering the password and submitting the login form.

from playwright.sync_api import Page


class LoginPasswordPage:
    def __init__(self, page: Page):
        self.page = page
        self.password_input = page.locator("input[type='password']")
        self.submit_button = page.get_by_role("button", name="Sign in")

    def enter_password(self, password: str):
        self.password_input.fill(password)

    def submit(self):
        self.submit_button.click()
