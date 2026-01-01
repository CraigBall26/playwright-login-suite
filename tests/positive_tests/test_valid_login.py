# TC‑000: Valid Login
# -------------------
# Full end‑to‑end login using the real Auth0 UI, confirming that a valid user
# can authenticate successfully and reach a logged‑in state.
#
# Trello: https://trello.com/c/nGoMICYw/102-test-000-valid-login-dashboard-check

import pytest

from flows.login_flow import LoginFlow


@pytest.mark.positive
def test_valid_login(fresh_page, hudl_credentials, login_data):
    # Use the LoginFlow wrapper to keep the steps clean.
    flow = LoginFlow(fresh_page, login_data)

    # Perform a full valid login using known credentials.
    dashboard = flow.login(
        hudl_credentials[2],
        hudl_credentials["cra"],
    )

    # Confirm the dashboard has fully loaded using the canonical sync point.
    dashboard.wait_for_loaded()

    # Assert that a known dashboard element is present.
    loc = dashboard._first_available(dashboard.SSR_WEBNAV_CONTAINER)
    assert loc.count() > 0
