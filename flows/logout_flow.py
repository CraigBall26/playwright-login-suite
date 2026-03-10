# Flow wrapper that handles the full logout sequence.
# Keeps the test code cleaner by encapsulating the steps.

from pages.dashboard_page import DashboardPage


class LogoutFlow:
    def __init__(self, page):
        self.page = page
        self.dashboard = DashboardPage(page)

    def logout(self):
        # Open the user menu (button or initials avatar)
        self.dashboard.open_user_menu()

        # Click the logout button
        self.dashboard.click_logout()

        # The fan site does not navigate away after logout — the session cookie
        # is cleared but the URL stays on fan.hudl.com/. Tests that need to
        # assert session invalidation should check for the absence of the
        # authenticated user menu rather than waiting for a URL change.
        return self.page
