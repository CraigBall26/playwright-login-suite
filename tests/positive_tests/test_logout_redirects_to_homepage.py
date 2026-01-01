# TC‑004 — Logout Redirects to Homepage
#
# Confirms that a logged‑in Hudl user is correctly logged out and redirected
# back to the public homepage. This validates the logout flow and ensures
# authenticated sessions are properly terminated.

import pytest

from flows.login_flow import LoginFlow
from flows.logout_flow import LogoutFlow


@pytest.mark.positive
def test_logout_redirects_to_homepage(fresh_page, hudl_credentials, login_data):
    login_flow = LoginFlow(fresh_page, login_data)
    dashboard = login_flow.login(
        hudl_credentials["email"],
        hudl_credentials["password"],
    )

    # Ensure the dashboard is fully loaded before logging out.
    dashboard.wait_for_loaded()

    # Perform logout.
    logout_flow = LogoutFlow(fresh_page)
    logout_flow.logout()

    # Wait for the public homepage to settle.
    fresh_page.wait_for_load_state("networkidle")

    # Confirm we are no longer on the dashboard.
    dashboard.assert_not_on_dashboard()

    # Confirm we are on a Hudl homepage variant.
    assert fresh_page.url.startswith(login_data["base_url"])
