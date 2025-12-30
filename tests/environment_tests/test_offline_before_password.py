# TC‑301: Offline Before Password Page
# -------------------------------------------------------------------
# This test validates Hudl’s behaviour when the user loses network connectivity
# *before* reaching the password page. Coaches hit this scenario when opening
# the login screen on a bus, in a stadium tunnel, or in rural practice fields
# where signal drops suddenly. After submitting their email, Auth0 should fail
# gracefully and the password page should never load.
#
# Trello: https://trello.com/c/0n7PuK9K/219-tc301-offline-mode-login-attempt


import pytest
from playwright.sync_api import TimeoutError

from flows.login_flow import LoginFlow
from pages.login_password_page import LoginPasswordPage


@pytest.mark.environment
def test_offline_before_password(fresh_page, login_data, randomized_unknown_email):
    page = fresh_page
    flow = LoginFlow(page, login_data)

    # Load the login page *before* going offline.
    flow.goto_login()

    # Instantiate the password page object while still online.
    # This ensures locators bind to a stable DOM before connectivity drops.
    password_page = LoginPasswordPage(page)

    # Now simulate offline mode.
    page.context.set_offline(True)

    # Attempt to submit an identifier while offline.
    flow.identifier.submit_identifier(randomized_unknown_email)

    # Assert that the password page does NOT load.
    with pytest.raises(TimeoutError):
        password_page.wait_for_loaded(timeout=5000)

    # Restore network for teardown.
    page.context.set_offline(False)
