# TC‑003 — Direct Navigation to /home When Logged Out Redirects to Login
# ----------------------------------------------------------------------
# Confirms that a logged‑out user cannot access the authenticated /home route.
# Hudl should always redirect unauthenticated users back to the login page.
#
# Trello: https://trello.com/c/4t6JKEzZ/206-tc-003-direct-navigation-to-home-when-logged-out-redirects-to-login

import pytest

from pages.dashboard_page import DashboardPage
from pages.login_identifier_page import LoginIdentifierPage


@pytest.mark.positive
def test_direct_navigation_redirects_to_login(fresh_page, env_urls):
    page = fresh_page

    # Navigate directly to the authenticated /home route while logged out.
    page.goto(env_urls["home_url"])

    # Confirm we are redirected to the login identifier page.
    login_page = LoginIdentifierPage(page)
    login_page.wait_for_loaded()

    # Assert dashboard elements are not visible.
    dashboard = DashboardPage(page)
    assert page.locator(dashboard.SSR_WEBNAV_CONTAINER).count() == 0
