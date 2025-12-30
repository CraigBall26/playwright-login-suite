# TC‑107: Invalid Domain Email
# -------------------------------------------------------------------
# This test validates that the identifier page correctly rejects
# email addresses with structurally valid local parts but invalid
# domain components.
#
# Trello: https://trello.com/c/lKuD97IY/214-tc-107-invalid-domain-formats

import pytest

from flows.login_flow import LoginFlow
from test_data.login.invalid_emails import INVALID_EMAIL_DOMAINS


@pytest.mark.parametrize("email", INVALID_EMAIL_DOMAINS)
def test_invalid_domain_email(page, login_data, email):
    flow = LoginFlow(page, login_data)
    flow.goto_login()

    # Submit the invalid domain email.
    identifier = flow.identifier
    identifier.submit_identifier(email)

    # Assert that we are STILL on the identifier step
    identifier.assert_still_on_identifier_step()

    # Assert that the appropriate error is shown.
    identifier.assert_invalid_email_error()
