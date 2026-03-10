# Shared constants for the API test suite.
#
# Keeping these here means test files stay readable and there's one place
# to update things like the request timeout or the OIDC path.

# How long to wait (in seconds) before giving up on an HTTP request.
REQUEST_TIMEOUT = 15

# Path to the favicon, used to check static assets are being served.
FAVICON_PATH = "/favicon.ico"

# Auth0's OIDC discovery document — the login flow fetches this on startup.
OIDC_DISCOVERY_PATH = "/.well-known/openid-configuration"

# The minimum fields that must be present in the OIDC discovery document
# for the login flow to work.
REQUIRED_OIDC_FIELDS = [
    "issuer",
    "authorization_endpoint",
    "token_endpoint",
]

# Accept-Language header value used to test international browser support.
TEST_LOCALE = "fr-FR,fr;q=0.9"
