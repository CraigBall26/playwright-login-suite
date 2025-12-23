# TC-101 — Login With Incorrect Password
# Trello: https://trello.com/c/AtXenhxi/123-test-101-login-with-incorrect-password
#
# Checks that entering a valid email with an incorrect password does not
# allow access to the dashboard. Appropriate error message should be shown.

import os
import pytest

from pages.login_identifier_page import LoginIdentifierPage
from pages.login_password_page import LoginPasswordPage
from tests.tests_data.login_data import WRONG_PASSWORD


@pytest.mark.login
@pytest.mark.negative
def test_login_with_incorrect_password(page):
    # Load only environment variables provided by CI or local shell.
    email = os.getenv("HUDL_EMAIL")

    identifier_page = LoginIdentifierPage(page)
    password_page = LoginPasswordPage(page)

    # Start on the login page.
    identifier_page.goto()

    # Enter valid email and click continue.
    identifier_page.submit_email(email)

    # Enter an incorrect password and attempt login.
    password_page.submit_password(WRONG_PASSWORD)

    print(page.inner_text("body"))  # TEMP DEBUG
    password_page.assert_incorrect_password_message()
