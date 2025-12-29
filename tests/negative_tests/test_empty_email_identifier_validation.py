# TC‑105 - Empty Email on Identifier Page
# -------------------------------------------------------------------
# This test validates that a user who submits an EMPTY email address
# on the identifier page is prevented from continuing.
# Hudl should display a validation error.
#
# Trello: https://trello.com/c/8WQmt4hW/212-tc-105-empty-email-on-identifier-page

import pytest

from flows.login_flow import LoginFlow


@pytest.mark.negative
def test_empty_email_identifier_validation(fresh_page, login_data):
    flow = LoginFlow(fresh_page, login_data)

    # Start login and attempt to submit an EMPTY email.
    flow.goto_login()
    flow.identifier.submit_identifier("")

    # Assert that the identifier step shows the empty-email validation error.
    flow.identifier.assert_empty_email_error()

    # Assert that we are STILL on the identifier step (no advance to password).
    flow.identifier.assert_still_on_identifier_step()

    # Assert that the password input is NOT visible.
    flow.identifier.assert_password_input_not_visible()

    # Assert no redirect to dashboard.
    flow.base.assert_not_on_dashboard()
