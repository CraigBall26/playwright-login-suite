# TC‑005 — Session Remains Active After Page Refresh
#
# Confirms that a logged‑in user stays logged in after refreshing the page.
# This validates that Hudl maintains the authenticated session correctly and
# does not require re‑authentication.

import pytest

from flows.login_flow import LoginFlow


@pytest.mark.positive
def test_session_remains_active_after_refresh(fresh_page, hudl_credentials, login_data):
    page = fresh_page

    login_flow = LoginFlow(page, login_data)
    dashboard = login_flow.login(
        email=hudl_credentials["email"],
        password=hudl_credentials["password"],
    )

    # Ensure the dashboard is fully loaded before refreshing.
    dashboard.wait_for_loaded()

    # Refresh the page and confirm the session persists.
    page.reload()
    dashboard.wait_for_loaded()
