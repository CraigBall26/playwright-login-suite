# TC-000: Valid Login
# This test covers the full login flow using the real Auth0 UI.
# Notes:
# - The identifier page can hydrate slowly, so we wait for the field.
# - The password page loads only after a successful identifier step.
# - Hudl redirects different account types to different landing pages.
# - The SSR WebNav container is the most stable logged-in element for this account.

import pytest
from pages.login_identifier_page import LoginIdentifierPage
from pages.login_password_page import LoginPasswordPage
from pages.dashboard_page import DashboardPage


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

    # Step 2: prove we landed on a logged-in page.
    assert "/home" in fresh_page.url or "/dashboard" in fresh_page.url

    # Step 3: wait for the logged-in UI to load.
    dashboard_page.wait_for_logged_in()
