# TC‑103 - Switch from Known to Unknown User via "Edit email"
# -------------------------------------------------------------------
# This test validates that a user who begins logging in with a known Hudl
# account can return to the identifier step using the “Edit email” link,
# replace the email with an UNKNOWN user, and attempt to log in again using
# the known user's password. Hudl should correctly reject this attempt and
# display an appropriate error.
#
# Trello: https://trello.com/c/oQJE7kbh/210-tc-103-switch-from-known-to-unknown-user

import pytest

from flows.login_flow import LoginFlow
from pages.dashboard_page import DashboardPage


@pytest.mark.negative
def test_edit_email_switch_to_unknown_user(
    fresh_page, hudl_credentials, login_data, randomized_unknown_email
):
    flow = LoginFlow(fresh_page, login_data)

    # Start login with a KNOWN user.
    flow.goto_login()
    flow.identifier.submit_identifier(hudl_credentials["email"])

    # Now on the password page.
    flow.password.wait_for_loaded()

    # Tap "Edit email" and switch to an UNKNOWN user.
    flow.edit_identifier_and_attempt_login(
        new_email=randomized_unknown_email,
        password=hudl_credentials["password"],  # Known user's password
    )

    # Assert that the login attempt fails.
    flow.password.assert_password_error()

    # Assert no redirect to dashboard.
    dashboard = DashboardPage(fresh_page)
    assert dashboard.any_dashboard_element_present() is False
    assert "/home" not in fresh_page.url
