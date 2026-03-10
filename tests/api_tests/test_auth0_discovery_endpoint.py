# TC-409: OIDC Metadata Endpoint Returns Valid Configuration
# -------------------------------------------------------------------
# Checks the Auth0 discovery document is reachable and contains the
# fields the login flow needs to start an authentication request.

import pytest
import requests

from constants import (
    OIDC_DISCOVERY_PATH,
    REQUEST_TIMEOUT,
    REQUIRED_OIDC_FIELDS,
)


@pytest.mark.api
def test_oidc_metadata_endpoint_returns_valid_config(env_config):
    url = f"{env_config.identity_url}{OIDC_DISCOVERY_PATH}"

    # Fetch the discovery document.
    response = requests.get(url, timeout=REQUEST_TIMEOUT)

    # Should be reachable and return a 200.
    assert response.status_code == 200, (
        f"OIDC metadata endpoint returned {response.status_code}, expected 200"
    )

    # Must be valid JSON — a broken body here stops the flow
    # before the user sees a form.
    try:
        config = response.json()
    except Exception:
        pytest.fail("OIDC metadata endpoint did not return valid JSON")

    # Each required field must be present.
    for field in REQUIRED_OIDC_FIELDS:
        assert field in config, f"OIDC config is missing required field: '{field}'"
