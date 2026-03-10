# TC‑003 — Positive Login With Saved Session
#
# Validates that a previously saved Hudl session allows the user to access the
# dashboard without re-entering credentials. Real coaches don’t log in every
# time they open Hudl — Auth0 sessions persist, and this test ensures the suite
# can restore a valid session and land directly on the dashboard.

from typing import Any

import pytest

from pages.dashboard_page import DashboardPage


@pytest.mark.positive
def test_login_with_saved_session(context_with_session: Any, login_data: Any):
    page = context_with_session.new_page()

    # Navigate directly to the dashboard using the restored session.
    page.goto(f"{login_data['base_url']}/home")

    # Confirm the dashboard loads successfully.
    dashboard = DashboardPage(page)
    dashboard.wait_for_loaded()
