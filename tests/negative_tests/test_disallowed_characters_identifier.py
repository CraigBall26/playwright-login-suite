# TC‑104: Disallowed Characters in Identifier
# -------------------------------------------------------------------
# Validates that the identifier page rejects email addresses containing
# characters not permitted in either the local part or the domain.

import pytest

from flows.login_flow import LoginFlow
from test_data.login.invalid_emails import INVALID_EMAIL_DISALLOWED_CHARS


@pytest.mark.parametrize("email", INVALID_EMAIL_DISALLOWED_CHARS)
def test_disallowed_characters_identifier(page, login_data, email):
    flow = LoginFlow(page, login_data)
    flow.goto_login()

    identifier = flow.identifier
    identifier.submit_identifier(email)

    # The user should remain on the identifier step.
    identifier.assert_still_on_identifier_step()

    # The UI should display the invalid email error message.
    identifier.assert_invalid_email_error()
