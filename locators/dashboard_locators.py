# Dashboard Locators
# ------------------
# Provides a stable chain of selectors for detecting the real Hudl dashboard
# after a successful login.

# Primary WebNav selector — unique to the real Hudl dashboard
SSR_WEBNAV_PRIMARY = (
    "#ssr-webnav > div > div.hui-webnav__grid.hui-navcontainer > "
    "nav.hui-webnav__grid-col--onewhole.hui-globalnav."
    "uni-env--dark.uni-environment--dark > "
    "div:nth-child(2)"
)

# Fallback WebNav selectors
SSR_WEBNAV_FALLBACK = "nav.hui-globalnav, nav.hui-webnav__grid-col--onewhole"
SSR_WEBNAV_CONTAINER = f"{SSR_WEBNAV_PRIMARY}, {SSR_WEBNAV_FALLBACK}"

# User menu button (we just check for visiblity)
USER_MENU_BUTTON = "button[data-qa='webnav-user-menu']"

# Logout button inside the user menu
LOGOUT_BUTTON = "a[data-qa-id='webnav-usermenu-logout']"

# Menu dropdown trigger (the initials avatar)
USER_MENU_DROPDOWN = "h5.uni-avatar__initials--user"
