# TC-000: Valid Login
# -------------------
# Full end‑to‑end login using the real Auth0 UI, confirming that a valid user
# can authenticate successfully and reach a logged‑in state.
#
# Trello: https://trello.com/c/nGoMICYw/102-test-000-valid-login-dashboard-check

import pytest

from pages.dashboard_page import DashboardPage
from pages.login_identifier_page import LoginIdentifierPage
from pages.login_password_page import LoginPasswordPage


@pytest.mark.login
def test_valid_login(fresh_page, hudl_credentials):
    # Page objects for each step of the login flow.
    identifier_page = LoginIdentifierPage(fresh_page)
    password_page = LoginPasswordPage(fresh_page)
    dashboard_page = DashboardPage(fresh_page)

    # Start on the login page.
    identifier_page.goto()

    # Enter email address and continue to the password page.
    identifier_page.submit_identifier(hudl_credentials["email"])

    # Enter password and submit the login form.
    password_page.submit_password(hudl_credentials["password"])

    # Small pause to allow redirects to complete.
    fresh_page.wait_for_timeout(3000)

    # Assert we landed on a logged-in page.
    assert "/home" in fresh_page.url or "/dashboard" in fresh_page.url

    # Wait for the logged-in UI to load.
    dashboard_page.wait_for_logged_in()
