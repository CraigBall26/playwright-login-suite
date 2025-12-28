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

        # Hudl redirects to https://www.hudl.com/en_gb/ (or region equivalent)
        return self.page
