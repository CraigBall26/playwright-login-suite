# TC‑104 - Switch from Known to Known User via "Edit email" (Wrong Password)
# -------------------------------------------------------------------
# This test validates that a user who begins logging in with a known Hudl
# account can return to the identifier step using the “Edit email” link,
# re-enter the SAME known email, and attempt to log in again using an
# incorrect password. Hudl should correctly reject this attempt and display
# an appropriate error.
#
# Trello: https://trello.com/c/iFdhxQmc/211-tc-104-known-user-edit-email-same-known-user-but-wrong-password

import pytest

from flows.login_flow import LoginFlow
from pages.dashboard_page import DashboardPage


@pytest.mark.negative
def test_edit_email_switch_to_known_user_wrong_password(
    fresh_page, hudl_credentials, login_data
):
    flow = LoginFlow(fresh_page, login_data)

    # Start login with a KNOWN user.
    flow.goto_login()
    flow.identifier.submit_identifier(hudl_credentials["email"])

    # Now on the password page.
    flow.password.wait_for_loaded()

    # Tap "Edit email" and re-enter the SAME known email, but use a wrong password.
    flow.edit_identifier_and_attempt_login(
        new_email=hudl_credentials["email"],
        password="incorrect-password",  # Intentionally wrong
    )

    # Assert that the login attempt fails.
    flow.password.assert_password_error()

    # Assert no redirect to dashboard.
    dashboard = DashboardPage(fresh_page)
    assert dashboard.any_dashboard_element_present() is False
    assert "/home" not in fresh_page.url
