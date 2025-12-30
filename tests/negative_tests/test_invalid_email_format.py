# TC‑106: Invalid Email Format
# -------------------------------------------------------------------
# This test validates that the identifier page correctly rejects
# malformed email addresses and does not progress to the password step.
# Each case is parametrized using a human‑readable key for clarity.
#
# The flow layer still requires login_data for URL navigation, even
# though credentials are irrelevant for identifier‑page validation.

import pytest

from flows.login_flow import LoginFlow
from test_data.login.invalid_emails import INVALID_EMAIL_FORMATS


@pytest.mark.parametrize("case,email", INVALID_EMAIL_FORMATS.items())
def test_invalid_email_format(page, case, email):
    flow = LoginFlow(page)
    flow.goto_login()

    identifier = flow.identifier
    identifier.submit_identifier(email)  # <-- correct method call

    identifier.assert_still_on_identifier_step()
    identifier.assert_invalid_email_error()
