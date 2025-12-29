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

        # Hudl does not navigate to a new URL after logout — it simply clears
        # the session and reloads the same homepage URL (e.g., / or /en_gb/).
        return self.page
