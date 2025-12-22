# TC-000 — Valid Login
# Trello: https://trello.com/c/nGoMICYw/102-test-000-valid-login
#
# Checks that valid Hudl credentials load the dashboard.

import os

import pytest
from dotenv import load_dotenv

from pages.dashboard_page import DashboardPage
from pages.login_identifier_page import LoginIdentifierPage
from pages.login_password_page import LoginPasswordPage


@pytest.mark.login
def test_valid_login(page):
    # Load environment variables from .env file
    email = os.getenv("HUDL_EMAIL")
    password = os.getenv("HUDL_PASSWORD")

    # Page objects for each step of the login flow.
    identifier_page = LoginIdentifierPage(page)
    password_page = LoginPasswordPage(page)

    # Start on the login page.
    identifier_page.goto()

    # Enter email address and continue to password page.
    identifier_page.submit_email(email)

    # Enter password and submit the login form.
    password_page.submit_password(password)

    # Create the dashboard page object once login has completed.
    dashboard_page = DashboardPage(page)

    # Waitto finish redirecting and for the dashboard UI to appear.
    dashboard_page.wait_for_dashboard()

    # Confirmation that the user is logged in.
    dashboard_page.assert_logged_in()
