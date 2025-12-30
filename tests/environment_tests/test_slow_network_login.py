# TC‑300: Slow Network Login Attempt
# -------------------------------------------------------------------
# This test validates that the Hudl login flow remains stable and
# predictable when the network connection is intentionally slowed.
# This simulates real‑world conditions coaches experience on the
# practice field, on team buses, or in congested stadium WiFi
# environments. Even under these “third‑and‑long” network conditions,
# the login flow should remain functional and responsive.
#
# Trello: https://trello.com/c/XpkJsh7S/218-tc-300-slow-network-login-attempt

import time

from flows.login_flow import LoginFlow


def test_slow_network_login(page, hudl_credentials, login_data):
    # Apply throttling to simulate slow network conditions.
    def throttle(route):
        time.sleep(0.4)  # 400ms artificial latency per request
        route.continue_()

    page.context.route("**/*", throttle)

    flow = LoginFlow(page, login_data)

    # Perform a full valid login
    dashboard = flow.login(
        hudl_credentials["email"],
        hudl_credentials["password"],
    )

    # Allow extra time for the dashboard to load
    dashboard.wait_for_loaded(timeout=20000)

    # Remove throttling after the test and allow pending requests to settle.
    page.context.unroute("**/*")
    time.sleep(2)
