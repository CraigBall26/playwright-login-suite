# Dashboard Locators
# ------------------
# Provides a stable chain of selectors for detecting the real Hudl dashboard
# after a successful login. These selectors are intentionally broad enough to
# survive SSR variants and UI experiments while remaining specific to the
# authenticated Hudl environment.

# Primary WebNav selector — kept for documentation, but not relied upon
SSR_WEBNAV_PRIMARY = (
    "#ssr-webnav > div > div.hui-webnav__grid.hui-navcontainer > "
    "nav.hui-webnav__grid-col--onewhole.hui-globalnav."
    "uni-env--dark.uni-environment--dark > "
    "div:nth-child(2)"
)

# Fallback WebNav selectors — broad enough to match all SSR variants
SSR_WEBNAV_FALLBACK = "nav, header, [data-qa='global-nav']"

# Option B: Welcome‑Home dashboard variant
# This nav is unique, stable, and strict‑mode‑safe.
SSR_WEBNAV_CONTAINER = "nav.hui-globalnav"

# User menu button (we just check for visibility)
USER_MENU_BUTTON = "button[data-qa='webnav-user-menu']"

# Logout button inside the user menu
LOGOUT_BUTTON = "div.hui-globalusermenu a[data-qa-id='webnav-usermenu-logout']"

# Menu dropdown trigger (the initials avatar)
USER_MENU_DROPDOWN = "h5.uni-avatar__initials--user"
