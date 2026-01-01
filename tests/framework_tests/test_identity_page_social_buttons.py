# TC‑201: Identity Page Social Buttons
# -------------------------------------------------------------------
# Validates that all social login buttons on the identity step are present
# and that each redirects to the correct provider domain.

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
    identifier.assert_google_button_present()
    identifier.assert_apple_button_present()
    identifier.assert_facebook_button_present()

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
