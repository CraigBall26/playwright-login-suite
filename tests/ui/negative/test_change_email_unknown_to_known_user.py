# TC‑109: Switch from Unknown → Known User (Wrong Password)
# -------------------------------------------------------------------
# Validates that a user who begins logging in with an unknown email can
# return to the identifier step using the “Edit email” link, switch to a
# known Hudl account, and that submitting an incorrect password triggers
# the appropriate error and prevents login.

import pytest

from flows.login_flow import LoginFlow


@pytest.mark.negative
def test_edit_email_switch_unknown_to_known_wrong_password(
    fresh_page, login_data, hudl_credentials, randomized_unknown_email
):
    flow = LoginFlow(fresh_page, login_data)
    flow.goto_login()

    # Begin login with an unknown user.
    flow.identifier.submit_identifier(randomized_unknown_email)
    flow.password.wait_for_loaded()

    # Switch to a known user via "Edit email".
    flow.edit_identifier_and_attempt_login(
        new_email=hudl_credentials["email"],
        password="incorrect-password",
    )

    # The UI should display the incorrect‑password error.
    flow.password.assert_password_error()

    # No redirect to the dashboard should occur.
    flow.base.assert_not_on_dashboard()
