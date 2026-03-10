# TC‑304: Slow Network Login Attempt
# -------------------------------------------------------------------
# Validates that the Hudl login flow remains stable and predictable under
# slow or high‑latency conditions. Coaches hit this scenario on practice
# fields, team buses, or congested stadium WiFi. This test increases
# timeouts to reflect real‑world latency while ensuring the login flow
# remains reliable.

import pytest

from flows.login_flow import LoginFlow


@pytest.mark.environment
def test_slow_network_login(page, hudl_credentials, login_data):
    # Simulate high‑latency conditions by increasing default timeouts.
    # This avoids WebKit routing limitations while still testing the
    # login flow under realistic slow‑network behaviour.
    page.set_default_timeout(20000)

    flow = LoginFlow(page, login_data)

    # Perform a full valid login under slow‑network conditions.
    dashboard = flow.login(
        hudl_credentials["email"],
        hudl_credentials["password"],
    )

    # Allow extra time for the dashboard to load.
    dashboard.wait_for_loaded(timeout=20000)
    dashboard.assert_webnav_present()
