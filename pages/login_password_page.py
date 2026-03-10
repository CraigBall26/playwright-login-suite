# LoginPasswordPage
# Handles all interactions on the password step.
# Responsibilities:
# - entering the password
# - submitting the password
# - validating password errors
# - ensuring the page loads correctly after identifier step

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import expect

from locators import login_password_locators as L  # noqa: N812
from locators.shared_locators import SharedLocators
from pages.base_page import BasePage


class LoginPasswordPage(BasePage):
    # Page object for the password entry step.
    def __init__(self, page):
        super().__init__(page)

        # Core elements
        self.password_input = L.PASSWORD_INPUT
        self.submit_button = L.SUBMIT_BUTTON

        # Error messages (Auth0 has multiple variants)
        self.password_error = L.PASSWORD_ERROR
        self.error_selectors = L.PASSWORD_ERROR_SELECTORS

        # Optional UI elements
        self.back_button = SharedLocators.BACK_BUTTON
        self.edit_email_button = L.EDIT_EMAIL_BUTTON

        # Footer links
        self.privacy_policy_link = self.page.locator(SharedLocators.PRIVACY_POLICY_LINK)
        self.terms_of_service_link = self.page.locator(
            SharedLocators.TERMS_OF_SERVICE_LINK
        )

        # Social login buttons
        self.google_button = self.page.locator(SharedLocators.GOOGLE_BUTTON)
        self.apple_button = self.page.locator(SharedLocators.APPLE_BUTTON)
        self.facebook_button = self.page.locator(SharedLocators.FACEBOOK_BUTTON)

    # Navigation / load -----------------------------------

    def wait_for_loaded(self, timeout: int = 3000):
        # Must raise TimeoutError when offline or blocked.
        try:
            self.page.wait_for_selector(self.password_input, timeout=timeout)
        except Exception:
            raise PlaywrightTimeoutError("Password page did not load") from None

    # Core actions -----------------------------------------

    def enter_password(self, password: str):
        self.wait_and_fill(self.password_input, password)

    def submit(self):
        self.wait_and_click(self.submit_button)

    def submit_password(self, password: str):
        self.enter_password(password)
        self.submit()

    # Validation helpers -----------------------------------

    def assert_password_input_present(self):
        assert self.page.locator(self.password_input).count() > 0

    def assert_submit_button_present(self):
        assert self.page.locator(self.submit_button).count() > 0

    def assert_password_error(self, timeout: int = 3000):
        # Build a combined locator with or_() so Playwright retries the whole
        # set of selectors automatically until one is visible or timeout fires.
        # The previous loop used is_visible() (synchronous, no retry) which
        # could miss an error message that hadn't rendered yet.
        # .first avoids strict mode violations when Auth0 renders multiple
        # error containers simultaneously (e.g. empty + policy errors).
        loc = self.page.locator(self.error_selectors[0])
        for selector in self.error_selectors[1:]:
            loc = loc.or_(self.page.locator(selector))
        expect(loc.first).to_be_visible(timeout=timeout)

    # Step assertion ----------------------------------------

    def assert_still_on_password_step(self, timeout: int = 3000):
        self.assert_url_contains("password", timeout=timeout)
        self.wait_for_selector(self.password_input, timeout=timeout)

    # Optional navigation -----------------------------------

    def click_back_to_identifier(self):
        loc = self._first_available(self.back_button)
        loc.click()

    def click_edit_email(self):
        loc = self._first_available(self.edit_email_button)
        loc.click()

    # Footer link assertions -------------------------------

    def assert_privacy_policy_present(self):
        assert self.privacy_policy_link.count() > 0

    def assert_terms_of_service_present(self):
        assert self.terms_of_service_link.count() > 0

    # Footer link interactions ------------------------------

    def click_privacy_policy(self):
        self.privacy_policy_link.first.click()

    def click_terms_of_service(self):
        self.terms_of_service_link.first.click()

    # Social login interactions -----------------------------

    def click_google(self):
        self.google_button.first.click()

    def click_facebook(self):
        self.facebook_button.first.click()

    def click_apple(self):
        self.apple_button.first.click()
