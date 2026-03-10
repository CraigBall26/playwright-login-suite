# TC-407: Login Page Response Is Not Cached
# -------------------------------------------------------------------
# If you're on a shared computer, the last thing you want is the browser
# serving the previous person's login page from cache. no-store stops that.

import pytest


@pytest.mark.api
def test_login_page_is_not_cached(login_page_response):
    # no-store must be present — it's the directive that prevents caching entirely.
    cache_control = login_page_response.headers.get("Cache-Control", "")
    assert "no-store" in cache_control.lower(), (
        f"Expected Cache-Control to include 'no-store'. Got: '{cache_control}'"
    )
