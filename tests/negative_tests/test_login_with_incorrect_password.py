# TC-100: Login With Incorrect Password
# -------------------
# Verify that when a user enters a valid email and an
# INCORRECT password, login does not succeed, the user is not
# taken to the dashboard, and an appropriate error message is displayed.
#
# Trello: https://trello.com/c/98NyXx2b/202-test-100-login-with-incorrect-but-valid-password

import pytest

from pages.dashboard_page import DashboardPage
from pages.login_identifier_page import LoginIdentifierPage
from pages.login_password_page import LoginPasswordPage


@pytest.mark.negative
def test_login_with_incorrect_password(page, hudl_credentials):
    # Page objects for each step of the login flow.
    identifier_page = LoginIdentifierPage(page)
    password_page = LoginPasswordPage(page)

    # Start on the login page.
    identifier_page.goto()

    # Enter email address and continue to password page.
    identifier_page.submit_identifier(hudl_credentials["email"])

    # Wait for the password page to fully load.
    password_page.wait_for_loaded()

    # Submit an incorrect password. Satisfy the password complexity requirements.
    password_page.submit_password("WrongPass!123")
    print(page.inner_text("body"))

    # Assert the error message is shown.
    password_page.assert_password_error()

    # Assert no redirect to dashboard.
    dashboard = DashboardPage(page)
    assert dashboard.any_dashboard_element_present() is False
    assert "/home" not in page.url
