# TC-400: Login Page Is Reachable
# -------------------------------------------------------------------
# Confirms the login page is up and serving HTML. If this fails,
# every UI test will time out without a clear reason why.

import pytest


@pytest.mark.api
def test_login_page_is_reachable(login_page_response):
    # Should come back as a successful response.
    assert login_page_response.status_code == 200

    # Should be HTML, not JSON or a raw error string.
    assert "text/html" in login_page_response.headers.get("Content-Type", "")
