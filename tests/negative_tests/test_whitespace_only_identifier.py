# TC‑108: Whitespace‑Only Identifier Submission
# -------------------------------------------------------------------
# This test validates that the identifier page correctly rejects
# attempts to continue when the email field contains only whitespace
# characters (spaces, tabs, or newlines). These inputs are not empty,
# but they are still invalid and should not progress to the password
# step.
#
# Trello: https://trello.com/c/876rnzrj/215-tc-108-whitespace-only-email

import pytest

from flows.login_flow import LoginFlow


@pytest.mark.parametrize("email", [" ", " ", "\t"])
def test_whitespace_only_identifier(page, login_data, email):
    flow = LoginFlow(page, login_data)
    flow.goto_login()

    # Submit whitespace-only input.
    identifier = flow.identifier
    identifier.submit_identifier(email)

    # Assert that we are STILL on the identifier step.
    identifier.assert_still_on_identifier_step()

    # Assert that the appropriate error is shown.
    identifier.assert_invalid_email_error()
