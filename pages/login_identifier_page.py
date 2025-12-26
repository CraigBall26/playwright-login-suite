# Page object for the identifier (email) step of the login flow.
# Keeping selectors simple and readable

from playwright.sync_api import Page
from locators import login_identifier_locators as L
from locators.shared_locators import SharedLocators as S


class LoginIdentifierPage:
    def __init__(self, page: Page):
        self.page = page

        # Core fields
        self.email_input = page.locator(L.EMAIL_INPUT)
        self.continue_button = page.locator(L.CONTINUE_BUTTON)

        # Social login buttons (SHARED)
        self.google_button = page.locator(S.GOOGLE_BUTTON)
        self.facebook_button = page.locator(S.FACEBOOK_BUTTON)
        self.apple_button = page.locator(S.APPLE_BUTTON)

        # Footer links (SHARED)
        self.create_account_link = page.locator(S.CREATE_ACCOUNT_LINK)
        self.privacy_policy_link = page.locator(S.PRIVACY_POLICY_LINK)
        self.terms_of_service_link = page.locator(S.TERMS_OF_SERVICE_LINK)

        # Errors
        self.invalid_email_error = page.locator(L.INVALID_EMAIL_ERROR)

    # Navigate to the login page.
    def goto(self):
        self.page.goto("https://www.hudl.com/login")
        # self.email_input.wait_for(state="visible")

    # Enter email address and continue to the password page.
    def submit_identifier(self, email: str):
        self.email_input.fill(email)
        self.continue_button.wait_for(state="visible")
        self.continue_button.click()
