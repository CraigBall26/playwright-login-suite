# TC-405: Login Page Sends Standard Security Headers
# -------------------------------------------------------------------
# Checks for HSTS, X-Content-Type-Options, and clickjacking protection
# on the login page response.

import pytest


@pytest.mark.api
def test_login_page_has_security_headers(login_page_response):
    headers = login_page_response.headers

    # HSTS forces HTTPS for all future visits to this domain.
    assert "Strict-Transport-Security" in headers, (
        "Missing Strict-Transport-Security header — "
        "HTTPS is not being enforced by the browser"
    )

    # nosniff stops the browser guessing file types —
    # blocks a class of injection attacks.
    x_content_type = headers.get("X-Content-Type-Options", "")
    assert "nosniff" in x_content_type.lower(), (
        f"Expected X-Content-Type-Options: nosniff, got: '{x_content_type}'"
    )

    # Either X-Frame-Options or CSP frame-ancestors prevents the page being iframed.
    has_x_frame = "X-Frame-Options" in headers
    has_csp_frame_ancestors = "frame-ancestors" in headers.get(
        "Content-Security-Policy", ""
    )
    assert has_x_frame or has_csp_frame_ancestors, (
        "No clickjacking protection found — expected either X-Frame-Options "
        "or a Content-Security-Policy with frame-ancestors"
    )
