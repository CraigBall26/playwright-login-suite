# Page object for the Hudl dashboard.
# Contains locators for interacting with the dashboard page.


class DashboardPage:
    def __init__(self, page):
        self.page = page

        # No stable UI elements exist for consumer accounts with no teams.
        # The only reliable indicator of login is the /home URL.
        self.home_url_pattern = "**/home**"

    # Wait for the dashboard to finish loading after login.
    def wait_for_dashboard(self):
        # If we reach /home, the user is authenticated.
        self.page.wait_for_url(self.home_url_pattern, timeout=20000)

    # Confirmation that the user is logged in.
    def assert_logged_in(self):
        assert "/home" in self.page.url, "Expected to be on /home after login."

    # Opens the user/account menu in the top navigation bar.
    # Not available for consumer accounts with no teams.
    def user_menu(self):
        raise NotImplementedError("This account type does not display a user menu.")
