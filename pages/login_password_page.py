# Page object for the password step of the login flow.
# Keeping selectors simple and readable for stability and reviewer clarity.

from playwright.sync_api import Page
from locators import login_password_locators as L
from locators.shared_locators import SharedLocators as S


class LoginPasswordPage:
    def __init__(self, page: Page):
        self.page = page

        # Core fields
        self.password_input = page.locator(L.PASSWORD_INPUT)
        self.continue_button = page.locator(L.CONTINUE_BUTTON)

        # Toggles
        self.show_password_toggle = page.locator(L.SHOW_PASSWORD_TOGGLE)

        # Social login buttons (shared)
        self.google_button = page.locator(S.GOOGLE_BUTTON)
        self.facebook_button = page.locator(S.FACEBOOK_BUTTON)
        self.apple_button = page.locator(S.APPLE_BUTTON)

        # Footer links (shared)
        self.create_account_link = page.locator(S.CREATE_ACCOUNT_LINK)
        self.privacy_policy_link = page.locator(S.PRIVACY_POLICY_LINK)
        self.terms_of_service_link = page.locator(S.TERMS_OF_SERVICE_LINK)

        # Errors
        self.password_error = page.locator(L.PASSWORD_ERROR)

    # Ensure the password page has fully loaded before interacting.
    def wait_for_loaded(self):
        self.password_input.wait_for(state="visible")
        self.continue_button.wait_for(state="visible")  # matches identifier behaviour

    # Enter the password and continue to the dashboard.
    def submit_password(self, password: str):
        self.password_input.fill(password)
        self.continue_button.wait_for(
            state="visible"
        )  # ensures the real button is ready
        self.continue_button.click()

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

    # Error assertions
    def assert_password_error(self):
        self.password_error.wait_for(state="visible")
