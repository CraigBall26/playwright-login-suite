# TC‑002 — Session Remains Active After Page Refresh
# --------------------------------------------------
# Confirms that a logged‑in user stays logged in after refreshing the page.
# This validates that Hudl maintains the authenticated session correctly and
# does not require re‑authentication.
#
# Trello: https://trello.com/c/m3EWNfa7/205-tc-002-session-remains-active-after-refresh

import pytest

from flows.login_flow import LoginFlow


@pytest.mark.positive
def test_session_remains_active_after_refresh(fresh_page, hudl_credentials, login_data):
    page = fresh_page

    # Log in using the LoginFlow.
    login_flow = LoginFlow(page, login_data)
    dashboard = login_flow.login(
        email=hudl_credentials["email"],
        password=hudl_credentials["password"],
    )

    # Confirm the dashboard is fully loaded.
    dashboard.wait_for_loaded()

    # Refresh the page.
    page.reload()

    # Confirm the dashboard is still visible (session persisted).
    dashboard.wait_for_loaded()
