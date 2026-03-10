# TC-408: Auth0 Identity Provider Is Reachable
# -------------------------------------------------------------------
# Pings identity.hudl.com directly. If Auth0 is down, nobody can log
# in even if the Hudl front-end looks fine.

import pytest
import requests

from constants import REQUEST_TIMEOUT


@pytest.mark.api
def test_auth0_identity_provider_is_reachable(env_config):
    # Hit the identity provider root directly.
    response = requests.get(env_config.identity_url, timeout=REQUEST_TIMEOUT)

    # A 4xx is fine — Auth0's root typically redirects or requires parameters.
    # A 5xx means something is genuinely wrong on their end.
    assert response.status_code < 500, (
        f"Auth0 returned a server error: {response.status_code}. "
        "Nobody can log in while this is down."
    )
