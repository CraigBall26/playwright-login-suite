# TC‑001 — Valid Login
#
# Confirms that a user with correct credentials can complete the full login flow
# and reach a fully loaded DashboardPage. Uses the LoginFlow wrapper to keep the
# test readable and aligned with real user behaviour.

import pytest

from flows.login_flow import LoginFlow


@pytest.mark.positive
def test_valid_login(fresh_page, hudl_credentials, login_data):
    flow = LoginFlow(fresh_page, login_data)

    # Perform the full login sequence using valid credentials.
    dashboard = flow.login(
        hudl_credentials["email"],
        hudl_credentials["password"],
    )

    # Confirm the dashboard is fully loaded after login completes.
    dashboard.wait_for_loaded()
