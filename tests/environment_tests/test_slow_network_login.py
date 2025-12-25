# TC-200: Login With Slow Network Conditions
# Trello: https://trello.com/c/6vJanHyQ/200-test-200
#
# Validate login flow when network is intentionally slowed.
# This simulates real-world conditions,
# such as mobile data on a training field or congested WiFi.

import pytest

from pages.dashboard_page import DashboardPage
from pages.login_identifier_page import LoginIdentifierPage
from pages.login_password_page import LoginPasswordPage


@pytest.mark.environment
def test_slow_network_login(slow_network, hudl_credentials):
    # Slow_network provides a fresh page with latency applied to every request.
    page = slow_network

    # Page objects for each step of the login flow.
    identifier_page = LoginIdentifierPage(page)
    password_page = LoginPasswordPage(page)

    # Start on the login page.
    identifier_page.goto()

    # Enter email address and continue to password page.
    identifier_page.submit_email(hudl_credentials["email"])

    # Enter password and submit the login form.
    password_page.submit_password(hudl_credentials["password"])

    # Create the dashboard page object once login has completed.
    dashboard_page = DashboardPage(page)

    # Wait for the dashboard UI to appear.
    dashboard_page.wait_for_dashboard()

    # Confirmation that the user is logged in.
    dashboard_page.assert_logged_in()
