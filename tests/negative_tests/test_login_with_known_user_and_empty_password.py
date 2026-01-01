# TC‑107: Known User + Empty Password
# -------------------------------------------------------------------
# Validates that a known Hudl user cannot proceed when the password
# field is left empty and that the appropriate error message appears.

import pytest

from flows.login_flow import LoginFlow


@pytest.mark.negative
def test_login_with_known_user_and_empty_password(
    fresh_page, hudl_credentials, login_data
):
    flow = LoginFlow(fresh_page, login_data)
    flow.goto_login()

    # Enter a known user email and advance to the password page.
    flow.identifier.submit_identifier(hudl_credentials["email"])
    flow.password.wait_for_loaded()

    # Submit an empty password.
    flow.password.submit_password("")

    # The UI should display the empty‑password error.
    flow.password.assert_password_error()

    # No redirect to the dashboard should occur.
    flow.base.assert_not_on_dashboard()
