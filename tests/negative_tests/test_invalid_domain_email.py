# TC‑101: Invalid Domain Email
# -------------------------------------------------------------------
# Validates that the identifier page rejects email addresses with
# structurally valid local parts but invalid domain components.

import pytest

from flows.login_flow import LoginFlow
from test_data import load_json

_emails = load_json("login/invalid_emails.json")


@pytest.mark.parametrize("email", _emails["domains"])
def test_invalid_domain_email(page, login_data, email):
    flow = LoginFlow(page, login_data)
    flow.goto_login()

    identifier = flow.identifier
    identifier.submit_identifier(email)

    # The user should remain on the identifier step.
    identifier.assert_still_on_identifier_step()

    # The UI should display the invalid email error message.
    identifier.assert_invalid_email_error()
