# TC‑102: Empty Email on Identifier Page
# -------------------------------------------------------------------
# Validates that submitting an empty email address on the identifier
# page prevents progression to the password step and triggers the
# appropriate validation error.

import pytest

from flows.login_flow import LoginFlow


@pytest.mark.negative
def test_empty_email_identifier_validation(fresh_page, login_data):
    flow = LoginFlow(fresh_page, login_data)
    flow.goto_login()

    identifier = flow.identifier
    identifier.submit_identifier("")

    # The UI should display the empty‑email validation error.
    identifier.assert_empty_email_error()

    # The user should remain on the identifier step.
    identifier.assert_still_on_identifier_step()

    # The password input should not be visible.
    identifier.assert_password_input_not_visible()

    # No redirect to the dashboard should occur.
    flow.base.assert_not_on_dashboard()
