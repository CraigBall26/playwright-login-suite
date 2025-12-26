# TC-101 — Login With Incorrect Password
# Uses the same page object flow as the valid login test.
# Only difference: we enter a wrong password and assert the error.

import pytest
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

    # Submit an incorrect password.
    password_page.submit_password("WRONG_PASSWORD")

    # Assert that the incorrect password error is visible.
    password_page.assert_incorrect_password_error()

    # Assert that we did NOT reach the dashboard.
    assert "hudl.com/home" not in page.url
