# TC‑300: Slow Network Login Attempt
# -------------------------------------------------------------------
# This test validates that the Hudl login flow remains stable and
# predictable when the network connection is intentionally slowed.
# This simulates real‑world conditions coaches experience on the
# practice field, on team buses, or in congested stadium WiFi
# environments.
#
# Trello: https://trello.com/c/XpkJsh7S/218-tc-300-slow-network-login-attempt

from flows.login_flow import LoginFlow
from pages.base_page import BasePage


def test_slow_network_login(page, hudl_credentials, login_data):
    base = BasePage(page)

    # Apply slow network simulation
    base.apply_slow_network(delay_ms=400)

    # Increase default timeout for slow-network conditions
    page.set_default_timeout(20000)

    flow = LoginFlow(page, login_data)

    # Perform a full valid login
    dashboard = flow.login(
        hudl_credentials["email"],
        hudl_credentials["password"],
    )

    # Allow extra time for dashboard to load
    dashboard.wait_for_loaded(timeout=20000)

    # Clean up routing
    base.remove_slow_network()
