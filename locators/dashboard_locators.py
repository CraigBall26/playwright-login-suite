# Dashboard Locators
# ------------------
# Selectors for the fan.hudl.com post-login page.
# The account used for this suite is a fan account, which lands on
# fan.hudl.com after login rather than the team dashboard.
#
# The fan site nav uses CSS module class names (fanWebnav_*). The partial
# class matches below are intentionally broad so they survive hash changes
# in the CSS module suffix.

# Primary nav container — always present on authenticated fan pages.
FAN_WEBNAV_CONTAINER = "header[class*='fanWebnav_navbar']"

# User menu trigger — the avatar + display name container.
# Clicking it reveals the dropdown menu items (CSS show/hide, not dynamic).
USER_MENU_BUTTON = "div[class*='fanWebnav_globalUserItem']"

# Logout link — stable data-qa-id attribute inside the user dropdown.
LOGOUT_BUTTON = "a[data-qa-id='hui-logout']"

# Aliases used by DashboardPage for backwards compatibility.
SSR_WEBNAV_CONTAINER = FAN_WEBNAV_CONTAINER
USER_MENU_DROPDOWN = USER_MENU_BUTTON
