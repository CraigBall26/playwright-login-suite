# First step/page of a two-step login flow.
# Handles entering username and moving to the enter password page.
# Displays alternative social login options.

from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = "#username"
        self.continue_button = "#continue"

    def enter_username(self, username: str):
        self.page.fill(self.username_input, username)

    def click_continue(self):
        self.page.click(self.continue_button)
