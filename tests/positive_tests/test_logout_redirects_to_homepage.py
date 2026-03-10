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

    # Wait for the page to settle after logout.
    fresh_page.wait_for_load_state("domcontentloaded")

    # On the fan site, logout does not change the URL — both logged-in and
    # logged-out states land on fan.hudl.com. Assert on the nav state instead:
    # the authenticated user menu should no longer be present.
    from playwright.sync_api import expect

    expect(
        fresh_page.locator("div[class*='fanWebnav_globalUserItem']")
    ).not_to_be_visible(timeout=10000)
