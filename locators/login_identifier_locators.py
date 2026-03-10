# Locators for the identifier (email) step of the login flow only.
# These are raw selectors used by LoginIdentifierPage. No logic or methods here.
# Auth0's Universal Login Page (ULP) varies its markup between releases, so
# error selectors are listed with a primary value and multiple fallbacks.

from locators.shared_locators import SharedLocators

# Core inputs -----------------------------------
EMAIL_INPUT = "role=textbox[name='Email']"
CONTINUE_BUTTON = "button[data-action-button-primary='true']"

# Error messages (identifier-level) ------------
# Auth0 can surface errors as text nodes, data-testid attributes, or class-based
# containers depending on the ULP version. The tuple below is ordered by
# specificity — the most reliable selectors first, generic fallbacks last.
EMPTY_EMAIL_ERROR = "text=Enter an email address"
INVALID_EMAIL_ERROR = "text=Enter a valid email."
UNKNOWN_EMAIL_ERROR = "text=We didn't recognize that email"

IDENTIFIER_ERROR_SELECTORS = (
    EMPTY_EMAIL_ERROR,
    INVALID_EMAIL_ERROR,
    UNKNOWN_EMAIL_ERROR,
    # Generic Auth0 error containers
    "[data-testid='ui-error']",
    "[data-testid='error']",
    ".auth0-global-message-error",
    "div.auth0-global-message.auth0-global-message-error",
    ".alert-error",
    # Fallbacks for text-based errors
    "div[class*='error']",
    "div[class*='error']:has-text('email')",
    "p:has-text('email')",
)

# Social login buttons (shared across both login steps)
GOOGLE_BUTTON = SharedLocators.GOOGLE_BUTTON
APPLE_BUTTON = SharedLocators.APPLE_BUTTON
FACEBOOK_BUTTON = SharedLocators.FACEBOOK_BUTTON
