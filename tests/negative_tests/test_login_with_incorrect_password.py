# Test-100: Login With Invalid Password
# -------------------
# Verify that when a user enters a valid email and an
# invalid password, login does not succeed, the user is not
# taken to the dashboard, and an appropriate error message is displayed

# Trello: https://trello.com/c/E37jkxMO/122-test-100-login-with-invalid-password

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
    print(page.url)
    print(page.content())

    # Enter email address and continue to password page.
    identifier_page.submit_identifier(hudl_credentials["email"])
    print(page.url)

    # Wait for the password page to fully load.
    password_page.wait_for_loaded()

    # Submit an incorrect password.
    password_page.submit_password("WrongPass!123")

    # Assert the error message is shown.
    password_page.assert_password_error()
