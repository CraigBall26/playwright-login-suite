# Locators for the identifier (email) step of the login flow only
from locators.shared_locators import SharedLocators

# Inputs
EMAIL_INPUT = "role=textbox[name='Email']"
CONTINUE_BUTTON = "button[data-action-button-primary='true']"

# Errors (identifier-level)
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


@property
def google_button(self):
    return self.page.locator(SharedLocators.GOOGLE_BUTTON)


@property
def apple_button(self):
    return self.page.locator(SharedLocators.APPLE_BUTTON)


@property
def facebook_button(self):
    return self.page.locator(SharedLocators.FACEBOOK_BUTTON)
