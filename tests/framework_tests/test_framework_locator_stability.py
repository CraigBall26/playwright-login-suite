# TC‑200: Framework Locator Stability
# -------------------------------------------------------------------
# Validates that all critical selectors in the locator layer resolve
# correctly. Protects the framework from selector drift and catches UI
# changes early.

import pytest

from flows.login_flow import LoginFlow
from pages.login_identifier_page import LoginIdentifierPage
from pages.login_password_page import LoginPasswordPage


@pytest.mark.framework
def test_framework_locator_stability(fresh_page, hudl_credentials, login_data):
    # Identifier Page
    identifier = LoginIdentifierPage(fresh_page)
    identifier.goto(login_data["login_url"])

    # Assert Identifier locators exist
    identifier.assert_email_input_present()
    identifier.assert_continue_button_present()
    identifier.assert_privacy_policy_present()
    identifier.assert_terms_of_service_present()

    # Proceed to Password Page
    identifier.submit_identifier(hudl_credentials["email"])
    password = LoginPasswordPage(fresh_page)
    password.wait_for_loaded()

    # Assert Password locators exist
    password.assert_password_input_present()
    password.assert_submit_button_present()
    password.assert_privacy_policy_present()
    password.assert_terms_of_service_present()

    # Use the flow to complete login cleanly
    flow = LoginFlow(fresh_page, login_data)
    dashboard = flow.login(hudl_credentials["email"], hudl_credentials["password"])

    # Wait for the fan site to load before checking dashboard selectors.
    dashboard.wait_for_loaded()

    # Dashboard locators
    dashboard.assert_webnav_present()
