# Shared selectors used across multiple pages.
# Centralises repeated UI patterns so page objects stay clean and consistent.


class SharedLocators:
    # Global UI
    LOADING_SPINNER = "[data-qa='loading-spinner'], .spinner, [role='progressbar']"
    ALERT = "[data-qa='alert'], .alert, [role='alert']"
    FORM_ERROR = "[data-qa='form-error'], .form-error, .field-error"
    MODAL = "[data-qa='modal'], .modal, [role='dialog']"

    # Social login buttons
    GOOGLE_BUTTON = "button[data-provider='google']"
    APPLE_BUTTON = "button[data-provider='apple']"
    FACEBOOK_BUTTON = "button[data-provider='facebook']"

    # Footer links
    CREATE_ACCOUNT_LINK = "role=link[name='Create Account']"
    PRIVACY_POLICY_LINK = "role=link[name='Privacy Policy']"
    TERMS_OF_SERVICE_LINK = "role=link[name='Terms of Service']"

    # Back navigation (required by identifier + password pages)
    BACK_BUTTON = "button[data-qa='back-to-identifier'], a[href*='identifier']"
