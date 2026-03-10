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
    # Primary — Auth0 ULP error span, present for incorrect password.
    "span.ulp-input-error-message",
    # Empty password — Auth0 shows this in a div rather than a span.
    "text=Enter your password",
    # Generic ULP error containers covering both cases.
    ".ulp-error-info",
    "span[class*='error-message']",
    # Broader fallbacks retained for resilience against Auth0 UI changes.
    "[data-testid='login-error']",
    ".auth0-global-message-error",
    "div[class*='error']:has-text('incorrect')",
    "[data-qa='error-message']",
)


# Primary error selector (first-choice)
PASSWORD_ERROR = PASSWORD_ERROR_SELECTORS[0]
