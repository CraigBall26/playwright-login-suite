# TC-406: Login Page Sends a Content Security Policy Header
# -------------------------------------------------------------------
# Checks that a CSP header is present. Without one, injected scripts
# have no browser-level restriction on a page handling credentials.

import pytest


@pytest.mark.api
def test_login_page_has_csp_header(login_page_response):
    # CSP header must be present and non-empty.
    csp = login_page_response.headers.get("Content-Security-Policy", "")
    assert csp, (
        "No Content-Security-Policy header on the login page — "
        "XSS has no browser-level restriction here."
    )
