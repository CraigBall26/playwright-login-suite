# Page Objects for the dashboard page after a successful login.
# Responsibilities:
# - confirming the authenticated fan.hudl.com page has loaded
# - providing stable selectors for the fan site nav
# - supporting logout flows and session tests
# - ensuring negative tests can reliably detect non-dashboard states

import re

from playwright.sync_api import expect

from locators.dashboard_locators import (
    LOGOUT_BUTTON,
    SSR_WEBNAV_CONTAINER,
    USER_MENU_BUTTON,
    USER_MENU_DROPDOWN,
)
from pages.base_page import BasePage


class DashboardPage(BasePage):
    # Stable selectors for detecting the real Hudl dashboard
    SSR_WEBNAV_CONTAINER = SSR_WEBNAV_CONTAINER
    USER_MENU_BUTTON = USER_MENU_BUTTON
    USER_MENU_DROPDOWN = USER_MENU_DROPDOWN
    LOGOUT_BUTTON = LOGOUT_BUTTON

    def wait_for_loaded(self, timeout=15000):
        # The OIDC callback chain (hudl.com → identity → fan.hudl.com) takes
        # several seconds. Confirm the URL has settled before asserting on the
        # nav — using expect() so Playwright retries rather than waiting for a
        # load event (the fan site SPA does not reliably fire one).
        expect(self.page).to_have_url(
            re.compile(r"fan\.hudl\.com", re.IGNORECASE), timeout=timeout
        )
        self.wait_for_selector(self.SSR_WEBNAV_CONTAINER, timeout=timeout)

    def open_user_menu(self):
        # Click the avatar/display-name container to reveal the dropdown.
        # Menu items are already in the DOM (CSS show/hide) so we just
        # wait for the logout link to become visible after the click.
        self._first_available(self.USER_MENU_BUTTON).first.click()
        self.wait_for_selector(self.LOGOUT_BUTTON)

    def click_logout(self):
        self.page.click(self.LOGOUT_BUTTON)

    def any_dashboard_element_present(self) -> bool:
        return self.page.locator(self.SSR_WEBNAV_CONTAINER).is_visible()

    # Explicit assertions for clarity in tests
    def assert_webnav_present(self):
        loc = self._first_available(self.SSR_WEBNAV_CONTAINER)
        assert loc.count() > 0

    def assert_on_dashboard(self) -> None:
        self.wait_for_loaded()
        # Fan accounts land on fan.hudl.com; team accounts on /home.
        pattern = re.compile(r"fan\.hudl\.com|/home", re.IGNORECASE)
        expect(self.page).to_have_url(pattern)

    def assert_not_on_dashboard(self) -> None:
        # Use the URL-based check from BasePage. Checking for element absence
        # is unreliable — Auth0 login pages also contain header elements which
        # would cause a false positive with a broad element selector.
        super().assert_not_on_dashboard()

    # Helper for slow-load scenarios
    def wait_for_loaded_slow(self):
        self.wait_for_loaded(timeout=20000)

    def assert_session_invalidated(self, timeout: int = 15000) -> None:
        # The fan site is public — there is no auth redirect after logout.
        # Instead assert that the authenticated user menu is no longer rendered,
        # which is the reliable signal that the session cookie has been cleared.
        expect(self.page.locator(self.USER_MENU_BUTTON)).not_to_be_visible(
            timeout=timeout
        )

    def logout(self):
        self.open_user_menu()
        self.click_logout()
