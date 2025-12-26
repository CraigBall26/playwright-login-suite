# Shared selectors used across multiple pages.
# Keeps repeated patterns in one place.


class SharedLocators:
    # Global UI
    LOADING_SPINNER = "[data-qa='loading-spinner'], .spinner, [role='progressbar']"
    ALERT = "[data-qa='alert'], .alert, [role='alert']"
    FORM_ERROR = "[data-qa='form-error'], .form-error, .field-error"
    MODAL = "[data-qa='modal'], .modal, [role='dialog']"

    # Social login buttons (shared across both login steps)
    GOOGLE_BUTTON = "role=button[name='Continue with Google']"
    FACEBOOK_BUTTON = "role=button[name='Continue with Facebook']"
    APPLE_BUTTON = "role=button[name='Continue with Apple']"

    # Footer links (shared across both login steps)
    CREATE_ACCOUNT_LINK = "role=link[name='Create Account']"
    PRIVACY_POLICY_LINK = "role=link[name='Privacy Policy']"
    TERMS_OF_SERVICE_LINK = "role=link[name='Terms of Service']"
