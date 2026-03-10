# TC‑103: Whitespace‑Only Identifier Submission
# -------------------------------------------------------------------
# Validates that the identifier page rejects inputs containing only
# whitespace characters (spaces, tabs, newlines) and prevents
# progression to the password step.

import pytest

from flows.login_flow import LoginFlow


@pytest.mark.parametrize("email", [" ", "  ", "\t"])
def test_whitespace_only_identifier(page, login_data, email):
    flow = LoginFlow(page, login_data)
    flow.goto_login()

    identifier = flow.identifier
    identifier.submit_identifier(email)

    # The user should remain on the identifier step.
    identifier.assert_still_on_identifier_step()

    # The UI should display the invalid email error message.
    identifier.assert_invalid_email_error()
