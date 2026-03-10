# TC-401: HTTP Upgrades to HTTPS
# -------------------------------------------------------------------
# Checks the server redirects plain HTTP requests to HTTPS so
# credentials are never sent over an unencrypted connection.

import pytest
import requests

from constants import REQUEST_TIMEOUT


@pytest.mark.api
def test_http_upgrades_to_https(env_config):
    # Swap https:// for http:// to simulate a plain HTTP request.
    http_url = env_config.login_url.replace("https://", "http://", 1)

    # Stop requests following the redirect so we can inspect it directly.
    response = requests.get(http_url, timeout=REQUEST_TIMEOUT, allow_redirects=False)

    # Should redirect rather than serve the page over plain HTTP.
    assert response.status_code in range(300, 400), (
        f"Expected an HTTP→HTTPS redirect, got {response.status_code}"
    )

    # The redirect destination should be the HTTPS version of the URL.
    location = response.headers.get("Location", "")
    assert location.startswith("https://"), (
        f"Redirect should point to HTTPS, got: {location}"
    )
