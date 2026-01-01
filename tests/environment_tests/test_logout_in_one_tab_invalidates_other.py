# TC‑301: Logout in One Tab Invalidates Session in Another
# -------------------------------------------------------------------
# Validates that when a user logs out in one browser tab, any additional
# tabs open in the same browser context lose their authenticated session
# and are forced back to the login flow. Coaches frequently work across
# multiple tabs, so session invalidation must behave consistently.

import pytest

from flows.login_flow import LoginFlow
from pages.base_page import BasePage
from pages.dashboard_page import DashboardPage
from pages.login_identifier_page import LoginIdentifierPage


@pytest.mark.environment
def test_logout_in_one_tab_invalidates_other(
    fresh_page,
    hudl_credentials,
    login_data,
):
    # Tab A: Login
    tab_a = BasePage(fresh_page)
    flow_a = LoginFlow(tab_a.page, login_data)

    dashboard_a = flow_a.login(
        email=hudl_credentials["email"],
        password=hudl_credentials["password"],
    )
    dashboard_a.wait_for_loaded()
    dashboard_a.assert_webnav_present()

    # Tab B: Open and navigate to dashboard
    tab_b = tab_a.open_new_tab()
    tab_b.page.goto(f"{login_data['base_url']}/home")

    dashboard_b = DashboardPage(tab_b.page)
    dashboard_b.wait_for_loaded()
    dashboard_b.assert_webnav_present()

    # Tab A: Logout
    dashboard_a.logout()

    # Tab B: Should now be forced back to login
    tab_b.page.reload()

    identifier = LoginIdentifierPage(tab_b.page)
    identifier.wait_for_loaded()
