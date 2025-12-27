# Test: Locator Checks
# --------------------
# Validates that all critical selectors in the locator layer resolve to at
# least one element on the real UI. Protects the framework from selector
# drift and catches UI changes early.
#
# Trello: https://trello.com/c/jdSYIjSA/201-test-500-test-locator-checks


import pytest

from pages.dashboard_page import DashboardPage
from pages.login_identifier_page import LoginIdentifierPage
from pages.login_password_page import LoginPasswordPage


@pytest.mark.framework
def test_locator_checks(fresh_page, hudl_credentials):
    # Identifier Page Objects
    identifier = LoginIdentifierPage(fresh_page)
    identifier.goto()

    # Assert Identifier locators exist
    assert identifier.email_input.count() > 0
    assert identifier.continue_button.count() > 0

    # Password Objects
    identifier.submit_identifier(hudl_credentials["email"])
    password = LoginPasswordPage(fresh_page)
    password.wait_for_loaded()

    # Assert Password locators exist
    assert password.password_input.count() > 0
    assert password.continue_button.count() > 0
    assert password.show_password_toggle.count() > 0

    # Dashboard Objects
    password.submit_password(hudl_credentials["password"])

    # Match TC‑000: wait for redirect before checking dashboard selectors
    fresh_page.wait_for_url("**/home", timeout=15000)

    dashboard = DashboardPage(fresh_page)

    # NEW: wait for the nav container to appear before asserting
    fresh_page.wait_for_selector(dashboard.SSR_WEBNAV_CONTAINER, timeout=5000)

    dashboard.wait_for_loaded()

    # Dashboard Locator
    loc = dashboard._first_available(dashboard.SSR_WEBNAV_CONTAINER)
    assert loc.count() > 0
