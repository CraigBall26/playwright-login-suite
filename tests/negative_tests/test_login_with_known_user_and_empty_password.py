# TC‑102 — Login with a Known User + Empty Password
# -------------------------------------------------------------------
# This test validates that a known Hudl user cannot proceed when the
# password field is left empty. An error message should show.
#
# Trello: https://trello.com/c/BOcH1UcU/209-tc-102-login-with-known-user-and-empty-password

import pytest

from flows.login_flow import LoginFlow
from pages.dashboard_page import DashboardPage


@pytest.mark.negative
def test_login_with_known_user_and_empty_password(
    fresh_page, hudl_credentials, login_data
):
    flow = LoginFlow(fresh_page, login_data)

    # Start on the login page.
    flow.goto_login()

    # Enter a KNOWN user email and continue to password page.
    flow.identifier.submit_identifier(hudl_credentials["email"])

    # Wait for the password page to fully load.
    flow.password.wait_for_loaded()

    # Submit an EMPTY password.
    flow.password.submit_password("")

    # Assert that the password error appears.
    flow.password.assert_password_error()

    # Assert no redirect to dashboard.
    dashboard = DashboardPage(fresh_page)
    assert dashboard.any_dashboard_element_present() is False
    assert "/home" not in fresh_page.url
