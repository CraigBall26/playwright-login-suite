# TC‑005: Positive Login With Saved Session
# -------------------------------------------------------------------
# Validates that a previously saved Hudl session allows the user to
# access the dashboard without re-entering credentials. Real coaches
# don’t log in every time they open Hudl — Auth0 sessions persist, and
# this test ensures the automation suite can restore a valid session
# and land directly on the dashboard.
#
# Trello: https://trello.com/c/enSlSiYb/208-tc-006positive-login-with-saved-session

from typing import Any

import pytest

from pages.dashboard_page import DashboardPage


@pytest.mark.positive
def test_login_with_saved_session(context_with_session: Any, login_data: Any):
    # Use the pre-authenticated session created in conftest.
    page = context_with_session.new_page()

    # Navigate directly to the dashboard.
    page.goto(f"{login_data['base_url']}/home")

    # Confirm the dashboard loads successfully.
    dashboard = DashboardPage(page)
    dashboard.wait_for_loaded()
