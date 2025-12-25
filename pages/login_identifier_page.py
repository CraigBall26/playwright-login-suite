# First step/page of a two-step login flow.
# Handles entering email and moving to the enter password page.
# Displays alternative social login options.


class LoginIdentifierPage:
    # Selectors for page elements
    def __init__(self, page):
        self.page = page
        self.email_input = page.locator("#username")
        self.continue_button = page.get_by_role("button", name="Continue", exact=True)

    # Navigate to the Hudl login page.
    def goto(self):
        self.page.goto("https://www.hudl.com/login")

    # Ensure the login page is fully loaded and interactive.
    def wait_for_loaded(self):
        self.continue_button.wait_for(state="visible")

    # Inputs an email and clicks the continue button.
    def submit_email(self, email):
        self.wait_for_loaded()
        self.email_input.fill(email)

        # Click the correct Continue button
        self.continue_button.click()
