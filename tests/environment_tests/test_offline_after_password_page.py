# TC‑302: Offline After Password Page
# -------------------------------------------------------------------
# This test validates Hudl’s behaviour when the user loses network connectivity
# *after* reaching the password page. This scenario happens when a coach enters
# their email successfully, walks into a tunnel, or hits a dead zone right as
# they’re about to enter their password. Auth0 should fail gracefully and the
# dashboard should never load.
#
# Trello: https://trello.com/c/0n7PuK9K/220-tc302-offline-after-password-page


import pytest
from playwright.sync_api import TimeoutError

from flows.login_flow import LoginFlow
from pages.dashboard_page import DashboardPage


@pytest.mark.environment
def test_offline_after_password_page(fresh_page, login_data, randomized_known_email):
    page = fresh_page
    flow = LoginFlow(page, login_data)

    # Navigate to the password page while online.
    password_page = flow.goto_password_page(randomized_known_email)

    # Instantiate the dashboard page object while still online.
    dashboard_page = DashboardPage(page)

    # Now simulate offline mode.
    page.context.set_offline(True)

    # Attempt to submit a password while offline.
    password_page.submit_password("any-password")

    # Assert that the dashboard does NOT load.
    # Playwright raises TimeoutError when the expected selector never appears.
    with pytest.raises(TimeoutError):
        dashboard_page.wait_for_loaded(timeout=5000)

    # Restore network for teardown.
    page.context.set_offline(False)
