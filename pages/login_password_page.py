# Second step of a two-step login flow.
# Handles entering the password and submitting the login form.


class LoginPasswordPage:
    def __init__(self, page):
        self.page = page

    def wait_for_loaded(self):
        # Wait for the password URL to load
        self.page.wait_for_url("**/u/login/password**", timeout=20000)

        # Wait for the password input to appear
        self.page.locator("input#password").wait_for(state="visible", timeout=20000)

        # Define selectors now that the DOM is ready
        self.password_input = self.page.locator("input#password:visible")
        self.login_button = self.page.get_by_role("button", name="Continue", exact=True)

    def submit_password(self, password):
        self.wait_for_loaded()

        # Ensure the field is visible (editable is not a valid state)
        self.password_input.wait_for(state="visible")

        # Click before typing (Auth0 sometimes requires focus)
        self.password_input.click()

        # Type instead of fill (more reliable for Auth0)
        self.password_input.type(password, delay=50)

        # Blur to trigger Auth0 validation
        self.page.keyboard.press("Tab")

        # Wait for the Continue button to become enabled
        self.page.wait_for_selector('button:has-text("Continue"):not([disabled])')

        # Click the enabled Continue button
        self.login_button.click()

    # Assert that an incorrect password error message is shown.
    def assert_incorrect_password_message(self):
        error = self.page.locator("#error-element-password")
        error.wait_for(state="visible", timeout=8000)
