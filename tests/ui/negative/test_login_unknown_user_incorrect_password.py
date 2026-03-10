# TC‑106: Unknown User + Valid‑Format but Incorrect Password
# -------------------------------------------------------------------
# Validates that a valid‑format but unknown email advances to the
# password page, and that submitting a valid‑format yet incorrect
# password triggers the appropriate error and prevents login.

import pytest

from flows.login_flow import LoginFlow


@pytest.mark.negative
def test_login_with_unknown_user_and_incorrect_password(
    fresh_page, login_data, randomized_unknown_email
):
    flow = LoginFlow(fresh_page, login_data)
    flow.goto_login()

    # Enter a valid‑format but unknown email and advance to the password page.
    flow.identifier.submit_identifier(randomized_unknown_email)
    flow.password.wait_for_loaded()

    # Submit a valid‑format but incorrect password.
    incorrect_password = login_data["valid_but_incorrect_credentials"]["password"]
    flow.password.submit_password(incorrect_password)

    # The UI should display the incorrect‑password error.
    flow.password.assert_password_error()

    # No redirect to the dashboard should occur.
    flow.base.assert_not_on_dashboard()
