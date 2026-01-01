# TC‑302: Offline Before Password Page
# -------------------------------------------------------------------
# Validates Hudl’s behaviour when the user loses network connectivity
# *before* reaching the password page. Coaches hit this scenario when
# opening the login screen on a bus, in a stadium tunnel, or in rural
# practice fields where signal drops suddenly. After submitting their
# email, Auth0 should fail gracefully and the password page should never
# load.

from typing import Any

import pytest
from playwright.sync_api import TimeoutError

from flows.login_flow import LoginFlow
from pages.login_password_page import LoginPasswordPage


@pytest.mark.environment
def test_offline_before_password(
    fresh_page: Any,
    login_data: Any,
    randomized_unknown_email: str,
):
    page = fresh_page
    flow = LoginFlow(page, login_data)

    try:
        # Load the login page *before* going offline.
        flow.goto_login()

        # Instantiate the password page object while still online.
        password_page = LoginPasswordPage(page)

        # Now simulate offline mode.
        page.context.set_offline(True)

        # Attempt to submit an identifier while offline.
        flow.identifier.submit_identifier(randomized_unknown_email)

        # Assert that the password page does NOT load.
        with pytest.raises(TimeoutError):
            password_page.wait_for_loaded(timeout=5000)

    finally:
        # Restore network state to avoid cross‑test contamination.
        page.context.set_offline(False)
        page.context.unroute("**/*")
