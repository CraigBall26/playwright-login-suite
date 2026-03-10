# TC-403: Protected Route Redirects Unauthenticated Users
# -------------------------------------------------------------------
# Confirms that visiting /home without a session results in a redirect
# rather than the page being served directly.

import pytest
import requests

from constants import REQUEST_TIMEOUT


@pytest.mark.api
def test_home_redirects_unauthenticated(env_config):
    # Stop requests following the redirect so we can inspect it directly.
    response = requests.get(
        env_config.home_url,
        allow_redirects=False,
        timeout=REQUEST_TIMEOUT,
    )

    # Should redirect away from the protected content.
    assert 300 <= response.status_code < 400, (
        f"Expected a redirect for an unauthenticated request to /home, "
        f"got {response.status_code}"
    )
