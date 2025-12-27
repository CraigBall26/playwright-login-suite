# Login Password Locators
# Core fields
PASSWORD_INPUT = "input[name='password']"
CONTINUE_BUTTON = "button[type='submit']"

# Toggles
SHOW_PASSWORD_TOGGLE = "[data-testid='password-visibility-toggle']"

# Error messages
PASSWORD_ERROR_SELECTORS = [
    # TC‑101: Unknown email
    "text=Incorrect username or password",
    # TC‑100: Valid email + wrong password
    "text=Your email or password is incorrect",
    # Additional Auth0 variants (fallbacks)
    "text=Invalid email or password",
    "text=Wrong email or password",
    "[data-testid='login-error']",
    ".auth0-global-message-error",
    ".alert-error",
]
