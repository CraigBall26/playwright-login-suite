# TC-001 Logout Redirects to Homepage
# --------------------
# Confirms that a logged-in user can successfully log out and is redirected
# to the correct Hudl homepage.
#
# Trello: https://trello.com/c/tB7GOa79/204-tc-001-test-logout-redirects-to-hudl-homepage

from flows.login_flow import LoginFlow
from flows.logout_flow import LogoutFlow


def test_logout_redirects_to_homepage(fresh_page, hudl_credentials):
    # Login
    login_flow = LoginFlow(fresh_page)
    dashboard = login_flow.login(
        hudl_credentials["email"],
        hudl_credentials["password"],
    )
    dashboard.wait_for_loaded()

    # Logout
    logout_flow = LogoutFlow(fresh_page)
    page_after_logout = logout_flow.logout()

    # Assert redirect to Hudl homepage
    assert page_after_logout.url.startswith("https://www.hudl.com")
