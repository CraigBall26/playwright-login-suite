# Login Password Locators
# Core fields
PASSWORD_INPUT = "input[name='password']"
CONTINUE_BUTTON = "button[type='submit']"

# Toggles
SHOW_PASSWORD_TOGGLE = "[data-testid='password-visibility-toggle']"

# Error messages
PASSWORD_ERROR_SELECTORS = [
    "div.c4de1c3f0.c040bb180:has-text('incorrect')",
    "div.c092c43cb:has-text('incorrect')",
    "[data-testid='login-error']",
    ".auth0-global-message-error",
    ".alert-error",
]
