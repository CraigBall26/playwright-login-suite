# Page object for the Identifier step of the login flow.
# Handles:
# - entering and submitting the user's email
# - validating identifier‑step error states
# - ensuring the flow does not advance on invalid input
# - interacting with footer legal links


from locators import login_identifier_locators as L  # noqa: N812
from locators.shared_locators import SharedLocators
from pages.base_page import BasePage


class LoginIdentifierPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        # Core elements
        self.email_input = L.EMAIL_INPUT
        self.continue_button = L.CONTINUE_BUTTON

        # Error messages (Auth0 has multiple variants)
        self.empty_email_error = L.EMPTY_EMAIL_ERROR
        self.invalid_email_error = L.INVALID_EMAIL_ERROR
        self.unknown_email_error = L.UNKNOWN_EMAIL_ERROR
        self.error_selectors = L.IDENTIFIER_ERROR_SELECTORS

        # Footer links
        self.privacy_policy_link = self.page.locator(SharedLocators.PRIVACY_POLICY_LINK)
        self.terms_of_service_link = self.page.locator(
            SharedLocators.TERMS_OF_SERVICE_LINK
        )

        # Social login buttons
        self.google_button = self.page.locator(L.GOOGLE_BUTTON)
        self.apple_button = self.page.locator(L.APPLE_BUTTON)
        self.facebook_button = self.page.locator(L.FACEBOOK_BUTTON)

        # Back navigation (required by multiple tests)
        self.back_button = SharedLocators.BACK_BUTTON

    # Navigation -----------------------------------

    def goto(self, url: str):
        self.page.goto(url)

    def load(self):
        self.wait_for_selector(self.email_input)

    def wait_for_loaded(self, timeout: int = 3000):
        self.wait_for_selector(self.email_input, timeout=timeout)

    # Core actions ----------------------------------

    def enter_email(self, email: str):
        self.wait_and_fill(self.email_input, email)

    def submit(self):
        self.wait_and_click(self.continue_button)

    def submit_identifier(self, email: str):
        self.enter_email(email)
        self.submit()

    # Validation helpers ----------------------------

    def assert_empty_email_error(self):
        self.wait_for_selector(self.empty_email_error)

    def assert_invalid_email_error(self):
        self.wait_for_selector(self.invalid_email_error)

    def assert_unknown_email_error(self):
        self.wait_for_selector(self.unknown_email_error)

    def assert_any_identifier_error(self):
        for selector in self.error_selectors:
            if self.is_visible(selector):
                return
        raise AssertionError("Expected an identifier error, but none were visible.")

    def assert_password_input_not_visible(self):
        assert not self.page.locator("input[type='password']").is_visible()

    # Step assertion --------------------------------

    def assert_still_on_identifier_step(self, timeout: int = 3000):
        self.assert_url_contains("identifier", timeout=timeout)
        self.wait_for_selector(self.email_input, timeout=timeout)

    # Footer link interactions ----------------------

    def click_privacy_policy(self):
        self.privacy_policy_link.first.click()

    def click_terms_of_service(self):
        self.terms_of_service_link.first.click()

    # Social login interactions ---------------------

    def click_google_and_capture(self):
        with self.page.expect_navigation() as nav:
            self.google_button.first.click()
        return nav.value.url

    def click_apple_and_capture(self):
        with self.page.expect_navigation() as nav:
            self.apple_button.first.click()
        return nav.value.url

    def click_facebook_and_capture(self):
        with self.page.expect_navigation() as nav:
            self.facebook_button.first.click()
        return nav.value.url

    # Back navigation -------------------------------

    def click_back_to_identifier(self):
        loc = self._first_available(self.back_button)
        loc.click()
