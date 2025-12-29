# TC-101: Unknown Email and Incorrect Password (Valid Format)
# -----------------------------------
# Verifies that an UNKNOWN user (valid-format email that does not belong
# to any Hudl account) cannot log in, even when providing a valid-format password.
#
# Hudl does not validate whether an email exists during the identifier step.
#
# Trello: https://trello.com/c/wilXx8EE/203-login-with-incorrect-but-valid-email-and-password

import pytest

from flows.login_flow import LoginFlow
from pages.dashboard_page import DashboardPage


@pytest.mark.negative
def test_login_with_unknown_user_and_incorrect_password(
    fresh_page, login_data, randomized_unknown_email
):
    flow = LoginFlow(fresh_page, login_data)

    # Start on the login page.
    flow.goto_login()

    # Use a valid-format but UNKNOWN email with a random suffix.
    flow.identifier.submit_identifier(randomized_unknown_email)

    # We SHOULD reach the password page.
    flow.password.wait_for_loaded()

    # Submit a valid-format but incorrect password from test_data.
    incorrect_password = login_data["valid_but_incorrect_credentials"]["password"]
    flow.password.submit_password(incorrect_password)

    # Assert that the password error appears.
    flow.password.assert_password_error()

    # Assert no redirect to dashboard.
    dashboard = DashboardPage(fresh_page)
    assert dashboard.any_dashboard_element_present() is False
    assert "/home" not in fresh_page.url
