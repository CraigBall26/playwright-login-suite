# TC‑300: Login in Two Tabs (Multi‑Tab Login Consistency)
# -------------------------------------------------------------------
# Validates that when a user logs in on one browser tab, any additional
# tabs opened in the same browser context recognise the authenticated
# session and load the dashboard directly without showing the login flow.
# Coaches frequently work across multiple tabs, so this behaviour must
# remain stable and predictable.

import pytest

from flows.login_flow import LoginFlow
from pages.base_page import BasePage
from pages.dashboard_page import DashboardPage


@pytest.mark.environment
def test_login_two_tabs(
    fresh_page,
    hudl_credentials,
    login_data,
):
    # Tab A
    tab_a = BasePage(fresh_page)
    flow_a = LoginFlow(tab_a.page, login_data)

    # Login in Tab A
    dashboard_a = flow_a.login(
        email=hudl_credentials["email"],
        password=hudl_credentials["password"],
    )
    dashboard_a.wait_for_loaded()
    dashboard_a.assert_webnav_present()

    # Open Tab B
    tab_b = tab_a.open_new_tab()

    # Navigate Tab B to the dashboard URL
    tab_b.page.goto(f"{login_data['base_url']}/home")

    # Tab B should already be authenticated and land directly on the dashboard
    dashboard_b = DashboardPage(tab_b.page)
    dashboard_b.wait_for_loaded()
    dashboard_b.assert_webnav_present()
