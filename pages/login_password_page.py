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
