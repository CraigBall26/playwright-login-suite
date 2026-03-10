# TC-410: Login Page Responds Correctly to Non-English Accept-Language
# -------------------------------------------------------------------
# Checks that sending a French Accept-Language header doesn't break
# the login page for international users.

import pytest
import requests

from constants import REQUEST_TIMEOUT, TEST_LOCALE


@pytest.mark.api
def test_login_page_responds_to_non_english_language_header(env_config):
    # Request the login page with a French language preference.
    response = requests.get(
        env_config.login_url,
        headers={"Accept-Language": TEST_LOCALE},
        timeout=REQUEST_TIMEOUT,
    )

    # Should still return a successful response.
    assert response.status_code == 200, (
        f"Login page returned {response.status_code} for Accept-Language: {TEST_LOCALE}"
    )

    # Should still be HTML, not a redirect or error body.
    content_type = response.headers.get("Content-Type", "")
    assert "text/html" in content_type, (
        f"Expected text/html for a French-language request, got: {content_type}"
    )
