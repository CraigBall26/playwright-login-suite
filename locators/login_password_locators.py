# Login Password Locators
# Raw selectors for the password step of the login flow.
# These are used directly by LoginPasswordPage.

# Core fields
PASSWORD_INPUT = "input[name='password']"
SUBMIT_BUTTON = "button[type='submit']"

# Toggles
SHOW_PASSWORD_TOGGLE = "[data-testid='password-visibility-toggle']"

# Edit email button
EDIT_EMAIL_BUTTON = "[data-link-name='edit-username']"

# Error selectors with fallback logic
PASSWORD_ERROR_SELECTORS = (
    # MOST COMMON / FASTEST MATCH FIRST
    "text=/enter your password/i",
    "#error-cs-password-required",
    # Incorrect-password variants
    "div.c4de1c3f0.c040bb180:has-text('incorrect')",
    "div.c092c43cb:has-text('incorrect')",
    "[data-testid='login-error']",
    ".auth0-global-message-error",
    ".alert-error",
    # Unknown-user variants
    "div.auth0-global-message.auth0-global-message-error",
    "[data-testid='error']",
    # Fallbacks
    "div[class*='error']:has-text('incorrect')",
    "p:has-text('We can')",
    "[data-qa='error-message']",
)


# Primary error selector (first-choice)
PASSWORD_ERROR = PASSWORD_ERROR_SELECTORS[0]
