# TC‑006 — Correcting Email Before Login (Back Navigation Works)
#
# Validates that a user can correct their email address before completing the
# login flow. Two navigation paths are covered:
#   1. Using the browser Back button.
#   2. Using the "Edit" link on the password page.
# Both paths should return the user to the identifier step, allow correction,
# and still permit a successful login.

import pytest

from flows.login_flow import LoginFlow
from pages.login_password_page import LoginPasswordPage


@pytest.mark.positive
def test_back_navigation_via_browser_button(
    fresh_page, hudl_credentials, login_data, randomized_unknown_email
):
    flow = LoginFlow(fresh_page, login_data)

    # Submit an incorrect identifier to reach the password step.
    flow.goto_login()
    flow.identifier.submit_identifier(randomized_unknown_email)

    # Correct the email using the browser Back button and complete login.
    dashboard = flow.login_after_browser_back(
        correct_email=hudl_credentials["email"],
        password=hudl_credentials["password"],
    )

    # Confirm the dashboard has fully loaded after correction.
    dashboard.wait_for_loaded()


@pytest.mark.positive
def test_back_navigation_via_edit_button(
    fresh_page, hudl_credentials, login_data, randomized_unknown_email
):
    flow = LoginFlow(fresh_page, login_data)

    # Submit an incorrect identifier to reach the password step.
    flow.goto_login()
    flow.identifier.submit_identifier(randomized_unknown_email)

    # Wait for the password page to load before editing the email.
    password_page = LoginPasswordPage(fresh_page)
    password_page.wait_for_loaded()

    # Correct the email using the Edit link and complete login.
    dashboard = flow.login_after_edit(
        correct_email=hudl_credentials["email"],
        password=hudl_credentials["password"],
    )

    # Confirm the dashboard has fully loaded after correction.
    dashboard.wait_for_loaded()
