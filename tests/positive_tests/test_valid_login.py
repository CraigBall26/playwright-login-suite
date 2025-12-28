# TC-000: Valid Login
# -------------------
# Full end‑to‑end login using the real Auth0 UI, confirming that a valid user
# can authenticate successfully and reach a logged‑in state.
#
# Trello: https://trello.com/c/nGoMICYw/102-test-000-valid-login-dashboard-check

import pytest

from flows.login_flow import LoginFlow


@pytest.mark.login
def test_valid_login(fresh_page, hudl_credentials):
    flow = LoginFlow(fresh_page)

    # Perform the full login sequence.
    dashboard_page = flow.login(hudl_credentials["email"], hudl_credentials["password"])

    # Assert the dashboard is visible.
    fresh_page.wait_for_url("**/home", timeout=15000)
    dashboard_page.wait_for_loaded()

    # Final sanity check: URL should contain /home once logged in.
    assert "home" in fresh_page.url
