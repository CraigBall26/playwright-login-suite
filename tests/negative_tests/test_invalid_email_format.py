# TC‑106: Invalid Email Format
# -------------------------------------------------------------------
# This test validates that the identifier page correctly rejects
# malformed email addresses and does not progress to the password step.
# Each case is parametrized using a human‑readable key for clarity.
#
# The flow layer still requires login_data for URL navigation, even
# though credentials are irrelevant for identifier‑page validation.
#
# Trello: https://trello.com/c/xxxxxxxx/213-tc-106-invalid-email-format

import pytest

from flows.login_flow import LoginFlow
from test_data.login.invalid_emails import INVALID_EMAIL_FORMATS


@pytest.mark.parametrize("case,email", INVALID_EMAIL_FORMATS.items())
def test_invalid_email_format(page, login_data, case, email):
    flow = LoginFlow(page, login_data)
    flow.goto_login()

    # Submit the email.
    identifier = flow.identifier
    identifier.submit_identifier(email)

    # Assert that we are STILL on the identifier step.
    identifier.assert_still_on_identifier_step()

    # Assert that the appropriate error is shown.
    identifier.assert_invalid_email_error()
