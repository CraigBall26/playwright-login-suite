# TC‑304: Logout in One Tab, Session Invalidated in Second Tab
# -------------------------------------------------------------------
# Validates how Hudl behaves when a user logs out in one browser tab
# while another tab is still open. Real coaches often keep multiple
# Hudl tabs open during film review, messaging, and roster management.
# Logging out in one tab should invalidate the session everywhere,
# forcing the second tab back to the login flow.
#
# Trello: https://trello.com/c/MgTR72Wy/223-tc304-logout-in-one-tab-session-invalidated-in-second-tab

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

    # Tab B: Open and navigate to dashboard
    tab_b = tab_a.open_new_tab()
    tab_b.page.goto(f"{login_data['base_url']}/home")

    dashboard_b = DashboardPage(tab_b.page)
    dashboard_b.wait_for_loaded()

    # Tab A: Logout
    dashboard_a.logout()

    # Tab B: Should now be forced back to login
    tab_b.page.reload()

    identifier = LoginIdentifierPage(tab_b.page)
    identifier.wait_for_loaded()
