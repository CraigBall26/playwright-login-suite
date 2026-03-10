# Shared selectors used across multiple pages.
# Centralises repeated UI patterns so page objects stay clean and consistent.
# Any selector used by more than one page object belongs here.


class SharedLocators:
    # Generic page state indicators ---------------
    LOADING_SPINNER = "[data-qa='loading-spinner'], .spinner, [role='progressbar']"
    ALERT = "[data-qa='alert'], .alert, [role='alert']"
    FORM_ERROR = "[data-qa='form-error'], .form-error, .field-error"
    MODAL = "[data-qa='modal'], .modal, [role='dialog']"

    # Social login buttons (identifier + password steps)
    GOOGLE_BUTTON = "button[data-provider='google']"
    APPLE_BUTTON = "button[data-provider='apple']"
    FACEBOOK_BUTTON = "button[data-provider='facebook']"

    # Footer links (present on both login steps) ---
    CREATE_ACCOUNT_LINK = "role=link[name='Create Account']"
    PRIVACY_POLICY_LINK = "role=link[name='Privacy Policy']"
    TERMS_OF_SERVICE_LINK = "role=link[name='Terms of Service']"

    # Back navigation (identifier + password pages)
    # Auth0 uses different markup depending on the flow variant.
    BACK_BUTTON = "button[data-qa='back-to-identifier'], a[href*='identifier']"
