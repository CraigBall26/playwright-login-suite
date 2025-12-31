# TC:202 – Legal Links (Identity + Password Pages)
# --------------------------------------------------
# Ensures Privacy Policy and Terms of Service links exist on both login steps
# and open in a new tab as expected.
#
# Trello: https://trello.com/c/UaG9f3Lm/226-tc202-legal-buttons

import pytest

from pages.login_identifier_page import LoginIdentifierPage
from pages.login_password_page import LoginPasswordPage


@pytest.mark.framework
def test_identity_and_password_legal_links(fresh_page, login_data, hudl_credentials):
    page = fresh_page

    # Identity Page
    identifier = LoginIdentifierPage(page)
    identifier.goto(login_data["login_url"])
    identifier.wait_for_loaded()

    # Footer link presence
    assert identifier.privacy_policy_link.count() > 0
    assert identifier.terms_of_service_link.count() > 0

    # Privacy Policy (new tab)
    identifier.click_and_capture_popup(identifier.click_privacy_policy, "privacy")

    # Terms of Service (new tab)
    identifier.click_and_capture_popup(identifier.click_terms_of_service, "terms")

    # Move to Password Page
    identifier.submit_identifier(hudl_credentials["email"])
    password = LoginPasswordPage(page)
    password.wait_for_loaded()

    # Footer link presence
    assert password.privacy_policy_link.count() > 0
    assert password.terms_of_service_link.count() > 0

    # Privacy Policy (new tab)
    password.click_and_capture_popup(password.click_privacy_policy, "privacy")

    # Terms of Service (new tab)
    password.click_and_capture_popup(password.click_terms_of_service, "terms")
