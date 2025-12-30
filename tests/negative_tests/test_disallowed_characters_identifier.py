# TC‑109: Disallowed Characters in Identifier
# -------------------------------------------------------------------
# This test validates that the identifier page correctly rejects
# email addresses containing characters that are not permitted in
# either the local part or the domain. These cases represent realistic
# user mistakes such as accidental punctuation, mobile keyboard slips,
# or copy/paste artifacts from spreadsheets or documents.
#
# Trello: https://trello.com/c/TlO3QHl3/216-tc-109-disallowed-characters-in-email

import pytest

from flows.login_flow import LoginFlow
from test_data.login.invalid_emails import INVALID_EMAIL_DISALLOWED_CHARS


@pytest.mark.parametrize("email", INVALID_EMAIL_DISALLOWED_CHARS)
def test_disallowed_characters_identifier(page, login_data, email):
    flow = LoginFlow(page, login_data)
    flow.goto_login()

    # Submit an email containing disallowed characters.
    identifier = flow.identifier
    identifier.submit_identifier(email)

    # Assert that we are STILL on the identifier step.
    identifier.assert_still_on_identifier_step()

    # Assert that the appropriate error is shown.
    identifier.assert_invalid_email_error()
