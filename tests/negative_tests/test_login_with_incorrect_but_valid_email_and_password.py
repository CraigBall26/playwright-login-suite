# TC-101: Incorrect Email and Password (Valid Format)
# -----------------------------------
# Hudl does not validate whether an email exists during the identifier step.
# Any valid email will advance to the password page. The error
# only appears after submitting a password.
#
# Trello: https://trello.com/c/wilXx8EE/203-login-with-incorrect-but-valid-email-and-password


import pytest

from pages.dashboard_page import DashboardPage
from pages.login_identifier_page import LoginIdentifierPage
from pages.login_password_page import LoginPasswordPage


@pytest.mark.login
def test_login_with_incorrect_but_valid_email_and_password(fresh_page):
    identifier = LoginIdentifierPage(fresh_page)
    identifier.goto()

    # Enter a valid but incorrect email
    unknown_email = "1notarealuser_123456@example.com"
    identifier.submit_identifier(unknown_email)

    # We SHOULD reach the password page
    password = LoginPasswordPage(fresh_page)
    password.wait_for_loaded()

    # Submit a valid password
    password.submit_password("SomeValidPassword123!")

    # Assert that error appears
    password.assert_password_error()

    # Assert no redirect to dashboard
    dashboard = DashboardPage(fresh_page)
    assert dashboard.any_dashboard_element_present() is False
    assert "/home" not in fresh_page.url
