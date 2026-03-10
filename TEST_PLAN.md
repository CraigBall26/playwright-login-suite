# Test Plan

Full list of test cases in the suite, grouped by category.

---

## Positive Tests — Happy Path

| TC | File | What it checks |
|---|---|---|
| TC-001 | `test_valid_login.py` | Valid credentials log in and land on the dashboard |
| TC-002 | `test_direct_navigation_redirects_to_login.py` | Unauthenticated visit to `/home` redirects to login |
| TC-003 | `test_login_with_saved_session.py` | Restored Auth0 session loads the dashboard without re-login |
| TC-004 | `test_logout_redirects_to_homepage.py` | Logout clears the session and returns to the public homepage |
| TC-005 | `test_session_remains_active_after_page_refresh.py` | Hard refresh on the dashboard keeps the user logged in |
| TC-006 | `test_correcting_email_before_login.py` | User can go back and correct their email before submitting the password |

---

## Negative Tests — Validation and Error States

| TC | File | What it checks |
|---|---|---|
| TC-100 | `test_invalid_email_format.py` | Malformed email strings show a validation error |
| TC-101 | `test_invalid_domain_email.py` | Emails with invalid domains are rejected |
| TC-102 | `test_empty_email_shows_error.py` | Submitting an empty email field shows an error |
| TC-103 | `test_whitespace_email_shows_error.py` | Whitespace-only input is treated as empty |
| TC-104 | `test_disallowed_characters_in_email.py` | Disallowed characters in the email field are rejected |
| TC-105 | `test_login_known_user_incorrect_password.py` | Known user + wrong password shows an error, not a crash |
| TC-106 | `test_login_unknown_user_incorrect_password.py` | Unknown user + wrong password shows an error |
| TC-107 | `test_known_user_empty_password.py` | Known user submitting an empty password shows a validation error |
| TC-108 | `test_change_email_to_known_user_wrong_password.py` | Editing email to a known account then submitting the wrong password |
| TC-109 | `test_change_email_unknown_to_known_user.py` | Editing email from an unknown account to a known one mid-flow |

---

## Framework Tests — Locators and Components

| TC | File | What it checks |
|---|---|---|
| TC-200 | `test_locator_stability.py` | Key locators resolve without error — catches selector drift early |
| TC-201 | `test_identity_page_social_buttons.py` | Google, Apple, and Facebook buttons are present and redirect correctly |
| TC-202 | `test_identity_and_password_legal_links.py` | Legal links on both login steps are present and point to the right URLs |

---

## Environment Tests — Resilience

| TC | File | What it checks |
|---|---|---|
| TC-300 | `test_login_two_tabs.py` | Logging in on one tab reflects authenticated state on another |
| TC-301 | `test_logout_in_one_tab_invalidates_other.py` | Logging out in one tab invalidates the session in a second tab |
| TC-302 | `test_offline_before_password.py` | Going offline before the password page shows a sensible error |
| TC-303 | `test_offline_after_password_page.py` | Going offline after submitting the password handles gracefully |
| TC-304 | `test_slow_network_login.py` | Login completes successfully under simulated slow network conditions |

---

## API Tests — HTTP Layer

No browser. Uses `requests` directly against the live endpoints.

| TC | File | What it checks |
|---|---|---|
| TC-400 | `test_login_page_reachable.py` | Login page returns 200 with `text/html` content type |
| TC-401 | `test_http_upgrades_to_https.py` | Plain `http://` request is redirected to `https://` |
| TC-402 | `test_static_assets_load.py` | `favicon.ico` returns 200 with an image content type |
| TC-403 | `test_dashboard_requires_login.py` | Unauthenticated request to `/home` gets a redirect, not a 200 |
| TC-404 | `test_login_sets_secure_cookies.py` | Cookies set during login carry the `Secure` flag |
| TC-405 | `test_login_page_security_headers.py` | HSTS, `X-Content-Type-Options`, and clickjacking protection are present |
| TC-406 | `test_login_page_csp_header.py` | `Content-Security-Policy` header is present on the login page |
| TC-407 | `test_login_page_not_cached.py` | `Cache-Control` includes `no-store` so the login page isn't cached |
| TC-408 | `test_auth0_identity_reachable.py` | Auth0 identity service (`identity.hudl.com`) returns sub-500 |
| TC-409 | `test_auth0_discovery_endpoint.py` | OIDC discovery endpoint returns valid JSON with all required fields |
| TC-410 | `test_login_page_localisation.py` | Login page responds correctly to a non-English `Accept-Language` header |
