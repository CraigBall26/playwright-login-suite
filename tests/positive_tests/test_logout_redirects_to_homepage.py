# TC‑001 — Logout Redirects to Homepage
# -----------------------------------
# Confirms that a logged‑in Hudl user is correctly logged out and redirected
# back to the public homepage. This validates the logout flow and ensures
# authenticated sessions are properly terminated.
#
# Trello: https://trello.com/c/8yQ0QF0U/201-test-010-logout-redirects-to-homepage

import pytest

from flows.login_flow import LoginFlow
from flows.logout_flow import LogoutFlow
from pages.dashboard_page import DashboardPage


@pytest.mark.positive
def test_logout_redirects_to_homepage(fresh_page, hudl_credentials, login_data):
    # Login using the flow wrapper.
    login_flow = LoginFlow(fresh_page, login_data)
    dashboard = login_flow.login(
        hudl_credentials["email"],
        hudl_credentials["password"],
    )

    # Confirm the dashboard has fully loaded before logging out.
    dashboard.wait_for_loaded()

    # Perform logout.
    logout_flow = LogoutFlow(fresh_page)
    logout_flow.logout()

    # Wait for the public homepage to settle.
    fresh_page.wait_for_load_state("networkidle")

    # Assert we are no longer on the dashboard.
    assert "/home" not in fresh_page.url

    # Assert we are on a Hudl homepage variant.
    assert fresh_page.url.startswith("https://www.hudl.com")

    # Assert dashboard elements are no longer present.
    dashboard = DashboardPage(fresh_page)
    assert dashboard.any_dashboard_element_present() is False
