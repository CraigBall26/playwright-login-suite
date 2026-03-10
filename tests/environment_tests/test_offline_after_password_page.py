# TC‑303: Offline After Password Page
# -------------------------------------------------------------------
# This test validates Hudl’s behaviour when the user loses network connectivity
# *after* reaching the password page. This scenario happens when a coach enters
# their email successfully, walks into a tunnel, or hits a dead zone right as
# they’re about to enter their password. Auth0 should fail gracefully and the
# dashboard should never load.
#


from typing import Any

import pytest

from flows.login_flow import LoginFlow
from pages.dashboard_page import DashboardPage


@pytest.mark.environment
def test_offline_after_password_page(
    fresh_page: Any,
    login_data: Any,
):
    page = fresh_page
    flow = LoginFlow(page, login_data)

    # Pull the incorrect-but-valid credentials directly from login_data.json
    creds = login_data["valid_but_incorrect_credentials"]

    try:
        # Navigate to the password page while online.
        flow.goto_login()
        flow.identifier.submit_identifier(creds["email"])

        # Ensure the password page is fully loaded before going offline
        flow.password.wait_for_loaded()

        # Instantiate the dashboard page object while still online.
        dashboard_page = DashboardPage(page)

        # Now simulate offline mode.
        page.context.set_offline(True)

        # Attempt to submit a password while offline.
        flow.password.submit_password(creds["password"])

        # Assert that the dashboard does NOT load.
        with pytest.raises(AssertionError):
            dashboard_page.wait_for_loaded(timeout=5000)

    finally:
        # Restore network and routing for teardown.
        page.context.set_offline(False)
        page.context.unroute("**/*")
