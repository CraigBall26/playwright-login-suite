# Series 200 – Framework & Locator Stability
# Test 201 – Identity Page Social Buttons
# Validates that all social login buttons exist and navigate to the correct providers.

import pytest

from pages.login_identifier_page import LoginIdentifierPage


@pytest.mark.framework
def test_identity_page_social_buttons(fresh_page, login_data):
    page = fresh_page
    identifier = LoginIdentifierPage(page)

    # Navigate to the identity page
    identifier.goto(login_data["login_url"])
    identifier.wait_for_loaded()

    # Locator presence checks
    assert identifier.google_button.count() > 0
    assert identifier.apple_button.count() > 0
    assert identifier.facebook_button.count() > 0

    # Redirect domain checks
    # Google
    google_url = identifier.click_google_and_capture()
    assert "google" in google_url.lower()
    page.go_back()
    identifier.wait_for_loaded()

    # Apple
    apple_url = identifier.click_apple_and_capture()
    assert "apple" in apple_url.lower()
    page.go_back()
    identifier.wait_for_loaded()

    # Facebook
    fb_url = identifier.click_facebook_and_capture()
    assert "facebook" in fb_url.lower()
    page.go_back()
    identifier.wait_for_loaded()
