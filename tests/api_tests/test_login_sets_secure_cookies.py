# TC-404: Auth Cookies Are Served With the Secure Flag
# -------------------------------------------------------------------
# Checks that any cookies set during the login redirect chain carry
# the Secure flag so they can't travel over plain HTTP.

import pytest
import requests

from constants import REQUEST_TIMEOUT


@pytest.mark.api
def test_auth_cookies_have_security_flags(env_config):
    # Follow the full redirect chain and collect any cookies that get set.
    session = requests.Session()
    session.get(env_config.login_url, timeout=REQUEST_TIMEOUT)

    all_cookies = session.cookies

    # Skip rather than fail if no cookies were set — nothing to assert against.
    if not all_cookies:
        pytest.skip("No cookies were set during the redirect chain — nothing to check.")

    # Every cookie should carry the Secure flag.
    for cookie in all_cookies:
        assert cookie.secure, (
            f"Cookie '{cookie.name}' on {cookie.domain} is missing the Secure flag"
        )
