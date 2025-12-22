# First step/page of a two-step login flow.
# Handles entering email and moving to the enter password page.
# Displays alternative social login options.


class LoginIdentifierPage:
    def __init__(self, page):
        self.page = page
        self.email_input = page.get_by_role("textbox", name="Email")
        self.continue_button = page.get_by_role("button", name="Continue", exact=True)

    # Navigate to the Hudl login page.
    def goto(self):
        self.page.goto("https://www.hudl.com/login")

    # Inputs an email and clicks the continue button.
    def submit_email(self, email):
        self.email_input.fill(email)
        self.continue_button.click()
