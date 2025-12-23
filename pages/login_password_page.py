# Second step of a two-step login flow.
# Handles entering the password and submitting the login form.


class LoginPasswordPage:
    def __init__(self, page):
        self.page = page
        self.password_input = page.locator("input[name='password']")
        self.login_button = page.locator("button[type='submit']")

    # Inputs a password and clicks the login button.
    def submit_password(self, password):
        self.password_input.wait_for()
        self.password_input.fill(password)
        self.login_button.click()

    # Asserts that we are still on the same page after a failed login attempt.
    def assert_still_on_password_page(self):
        assert "/login/password" in self.page.url, (
            f"Expected to still be on the password page, but URL is: {self.page.url}"
        )
        assert self.password_input.is_visible(), (
            "Password input is not visible — user may have navigated away unexpectedly."
        )

    # Asserts that the incorrect password error message is visible.
    def assert_incorrect_password_message(self):
        error_message = self.page.get_by_text(
            "Your email or password is incorrect. Try again."
        )
        assert error_message.is_visible(), (
            "Incorrect password error message is not visible."
        )
