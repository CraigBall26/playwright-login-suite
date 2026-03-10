# TC-402: Static Assets Load Correctly
# -------------------------------------------------------------------
# Checks the favicon is reachable and served as an image. A broken
# asset usually points to a CDN or deployment issue.

import pytest
import requests

from constants import FAVICON_PATH, REQUEST_TIMEOUT


@pytest.mark.api
def test_favicon_loads(env_config):
    # Request the favicon directly.
    url = f"{env_config.base_url}{FAVICON_PATH}"
    response = requests.get(url, timeout=REQUEST_TIMEOUT)

    # Should be reachable.
    assert response.status_code == 200, (
        f"Favicon returned {response.status_code}, expected 200"
    )

    # Should be served as an image, not an HTML error page with a 200 status.
    content_type = response.headers.get("Content-Type", "")
    assert "image" in content_type, (
        f"Expected an image content type for favicon, got: {content_type}"
    )
