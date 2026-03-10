# TC‑100: Invalid Email Format
# -------------------------------------------------------------------
# Validates that the identifier page correctly rejects malformed email
# addresses and does not progress to the password step. Each case uses
# a human‑readable key for clarity and reviewer friendliness.

import pytest

from flows.login_flow import LoginFlow
from test_data import load_json

_emails = load_json("login/invalid_emails.json")


@pytest.mark.parametrize("case,email", _emails["formats"].items())
def test_invalid_email_format(page, login_data, case, email):
    flow = LoginFlow(page, login_data)
    flow.goto_login()

    identifier = flow.identifier
    identifier.submit_identifier(email)

    # The user should remain on the identifier step.
    identifier.assert_still_on_identifier_step()

    # The UI should display the invalid email error message.
    identifier.assert_invalid_email_error()
