# TC‑100 — Login with a Known User + a valid‑format but incorrect password.
# -----------------------------------
# Hudl does not validate whether an email exists during the identifier step.
# Any valid email will advance to the password page. The error
# only appears after submitting a password.
#
# Trello: https://trello.com/c/wilXx8EE/203-login-with-incorrect-but-valid-email-and-password

import pytest

from flows.login_flow import LoginFlow
from pages.dashboard_page import DashboardPage


@pytest.mark.negative
def test_login_with_known_user_and_incorrect_password(
    fresh_page, hudl_credentials, login_data
):
    # Use the LoginFlow wrapper to keep the steps clean.
    flow = LoginFlow(fresh_page, login_data)

    # Start on the login page.
    flow.goto_login()

    # Enter a KNOWN user email and continue to password page.
    flow.identifier.submit_identifier(hudl_credentials["email"])

    # Wait for the password page to fully load.
    flow.password.wait_for_loaded()

    # Submit a valid-format but incorrect password from test_data.
    incorrect_password = login_data["valid_but_incorrect_credentials"]["password"]
    flow.password.submit_password(incorrect_password)

    # Assert the error message is shown.
    flow.password.assert_password_error()

    # Assert no redirect to dashboard.
    dashboard = DashboardPage(fresh_page)
    assert dashboard.any_dashboard_element_present() is False
    assert "/home" not in fresh_page.url
