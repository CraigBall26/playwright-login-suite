# TC‑002 — Direct Navigation to /home When Logged Out Redirects to Login
#
# Confirms that a logged‑out user cannot access the authenticated /home route.
# Any unauthenticated navigation attempt should redirect the user back to the
# login identifier page, and no dashboard elements should be visible.

import pytest

from pages.dashboard_page import DashboardPage
from pages.login_identifier_page import LoginIdentifierPage


@pytest.mark.positive
def test_direct_navigation_redirects_to_login(fresh_page, env_config):
    page = fresh_page

    # Navigate directly to the authenticated /home route while logged out.
    page.goto(env_config.home_url)

    # Confirm we are redirected to the login identifier page.
    login_page = LoginIdentifierPage(page)
    login_page.wait_for_loaded()

    # Dashboard UI should not be visible when unauthenticated.
    dashboard = DashboardPage(page)
    dashboard.assert_not_on_dashboard()
