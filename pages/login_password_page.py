# Page object for the password step of the login flow.
# Keeping selectors simple and readable for stability and reviewer clarity.

from playwright.sync_api import Page

from locators import login_password_locators as L  # noqa: N812
from locators.shared_locators import SharedLocators as S
from pages.base_page import BasePage


class LoginPasswordPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # Core fields
        self.password_input = page.locator(L.PASSWORD_INPUT)
        self.continue_button = page.locator(L.CONTINUE_BUTTON)

        # Optional toggle (A/B tested — not guaranteed)
        self.show_password_toggle = page.locator(L.SHOW_PASSWORD_TOGGLE)

        # Edit email button (returns user to identifier step)
        self.edit_email_button = page.locator(L.EDIT_EMAIL_BUTTON)

        # Social login buttons
        self.google_button = page.locator(S.GOOGLE_BUTTON)
        self.facebook_button = page.locator(S.FACEBOOK_BUTTON)
        self.apple_button = page.locator(S.APPLE_BUTTON)

        # Footer links
        self.create_account_link = page.locator(S.CREATE_ACCOUNT_LINK)
        self.privacy_policy_link = page.locator(S.PRIVACY_POLICY_LINK)
        self.terms_of_service_link = page.locator(S.TERMS_OF_SERVICE_LINK)

    # Ensure the password page is fully loaded before interacting.
    def wait_for_loaded(self):
        self.wait_for_visible(self.password_input)
        self.wait_for_visible(self.continue_button)

    # Enter the password and continue to the dashboard.
    def submit_password(self, password: str):
        self.wait_for_visible(self.password_input)
        self.password_input.fill(password)
        self.continue_button.click()

    # Click the "Edit" button to return to the identifier page.
    def click_edit_email(self):
        self.wait_for_visible(self.edit_email_button)
        self.edit_email_button.click()

    # Error assertions
    def assert_password_error(self):
        # Resolve the correct error selector using fallback logic
        selector = ",".join(L.PASSWORD_ERROR_SELECTORS)
        loc = self._first_available(selector)
        self.wait_for_visible(loc)

    # Social login actions
    def click_google(self):
        self.google_button.click()

    def click_facebook(self):
        self.facebook_button.click()

    def click_apple(self):
        self.apple_button.click()

    # Footer link actions
    def click_create_account(self):
        self.create_account_link.click()

    def click_privacy_policy(self):
        self.privacy_policy_link.click()

    def click_terms_of_service(self):
        self.terms_of_service_link.click()
