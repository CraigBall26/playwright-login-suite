# TC‑303: Login in Two Tabs (Multi‑Tab Login Consistency)
# -------------------------------------------------------------------
# This test validates how Hudl behaves when a user logs in on one browser
# tab and then opens a second tab. Because both tabs share the same browser
# context, Hudl should recognise the existing authenticated session and
# redirect the second tab straight to the dashboard without showing the
# login flow again. Coaches do this constantly when juggling film, messages,
# and team dashboards across multiple tabs.
#
# Trello: https://trello.com/c/EsMeKHlr/222-tc-303-login-two-tabs

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

    # Open Tab B
    tab_b = tab_a.open_new_tab()

    # Navigate Tab B to the dashboard URL
    tab_b.page.goto(f"{login_data['base_url']}/home")

    # Tab B should already be authenticated and land directly on the dashboard
    dashboard_b = DashboardPage(tab_b.page)
    dashboard_b.wait_for_loaded()
