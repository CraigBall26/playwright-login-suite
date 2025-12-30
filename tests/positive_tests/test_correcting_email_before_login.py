# TC‑004: Correcting Email Before Login (Back Navigation Works)
# -------------------------------------------------------------------
# This test case validates that a user can correct their email address
# before completing the login flow. There are two navigation paths:
#
# 1. Browser's Back button.
# 2. "Edit" button on the password page.
#
# Both paths should return the user to the email entry screen, allow
# correction, and still permit a successful login.
#
# Trello: https://trello.com/c/7v4wk04g/207-tc-004correcting-email-before-login-back-navigation-works

import pytest

from flows.login_flow import LoginFlow
from pages.login_password_page import LoginPasswordPage


@pytest.mark.positive
def test_back_navigation_via_browser_button(
    fresh_page, hudl_credentials, login_data, randomized_unknown_email
):
    flow = LoginFlow(fresh_page, login_data)

    # Submit the random incorrect identifier.
    flow.goto_login()
    flow.identifier.submit_identifier(randomized_unknown_email)

    # Complete login after correcting email using the browser Back button.
    dashboard = flow.login_after_browser_back(
        correct_email=hudl_credentials["email"],
        password=hudl_credentials["password"],
    )

    # Confirm the dashboard has fully loaded.
    dashboard.wait_for_loaded()


@pytest.mark.login
def test_back_navigation_via_edit_button(
    fresh_page, hudl_credentials, login_data, randomized_unknown_email
):
    flow = LoginFlow(fresh_page, login_data)

    # Submit the random incorrect identifier.
    flow.goto_login()
    flow.identifier.submit_identifier(randomized_unknown_email)

    # Wait for the password page to load.
    password_page = LoginPasswordPage(fresh_page)
    password_page.wait_for_loaded()

    # Complete login after correcting email using the Edit button.
    dashboard = flow.login_after_edit(
        correct_email=hudl_credentials["email"],
        password=hudl_credentials["password"],
    )

    # Confirm the dashboard has fully loaded.
    dashboard.wait_for_loaded()
