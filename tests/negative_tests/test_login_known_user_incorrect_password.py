# TC‑105: Known User + Valid‑Format but Incorrect Password
# -------------------------------------------------------------------
# Validates that a known user can reach the password page with a valid
# email, but submitting a valid‑format yet incorrect password triggers
# the appropriate error and prevents login.

import pytest

from flows.login_flow import LoginFlow


@pytest.mark.negative
def test_login_with_known_user_and_incorrect_password(
    fresh_page, hudl_credentials, login_data
):
    flow = LoginFlow(fresh_page, login_data)
    flow.goto_login()

    # Enter a known user email and advance to the password page.
    flow.identifier.submit_identifier(hudl_credentials["email"])
    flow.password.wait_for_loaded()

    # Submit a valid‑format but incorrect password.
    incorrect_password = login_data["valid_but_incorrect_credentials"]["password"]
    flow.password.submit_password(incorrect_password)

    # The UI should display the incorrect‑password error.
    flow.password.assert_password_error()

    # No redirect to the dashboard should occur.
    flow.base.assert_not_on_dashboard()
