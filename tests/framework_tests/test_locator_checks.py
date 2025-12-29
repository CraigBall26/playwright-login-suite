# Test: Locator Checks
# --------------------
# Validates all critical selectors in the locator layer.
# Protects the framework from selector drift and catches UI changes early.
#
# Trello: https://trello.com/c/jdSYIjSA/201-test-500-test-locator-checks

import pytest

from flows.login_flow import LoginFlow
from pages.login_identifier_page import LoginIdentifierPage
from pages.login_password_page import LoginPasswordPage


@pytest.mark.framework
def test_locator_checks(fresh_page, hudl_credentials, login_data):
    # --- Identifier Page ---
    identifier = LoginIdentifierPage(fresh_page)
    identifier.goto(login_data["login_url"])

    # Assert Identifier locators exist
    assert identifier.email_input.count() > 0
    assert identifier.continue_button.count() > 0

    # Proceed to Password Page
    identifier.submit_identifier(hudl_credentials["email"])
    password = LoginPasswordPage(fresh_page)
    password.wait_for_loaded()

    # Assert Password locators exist
    assert password.password_input.count() > 0
    assert password.continue_button.count() > 0

    # Use the flow to complete login cleanly
    flow = LoginFlow(fresh_page, login_data)
    dashboard = flow.login(hudl_credentials["email"], hudl_credentials["password"])

    # Wait for redirect before checking dashboard selectors
    fresh_page.wait_for_url("**/home", timeout=15000)
    dashboard.wait_for_loaded()

    # Dashboard locators
    loc = dashboard._first_available(dashboard.SSR_WEBNAV_CONTAINER)
    assert loc.count() > 0
