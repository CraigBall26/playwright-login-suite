# Dashboard Locators
# ------------------

# Primary SSR WebNav selector
SSR_WEBNAV_PRIMARY = (
    "#ssr-webnav > div > div.hui-webnav__grid.hui-navcontainer > "
    "nav.hui-webnav__grid-col--onewhole.hui-globalnav."
    "uni-env--dark.uni-environment--dark > "
    "div:nth-child(2)"
)

# Fallback: broader SSR WebNav container
SSR_WEBNAV_FALLBACK = "nav.hui-globalnav, nav.hui-webnav__grid-col--onewhole"

# Fallback: generic Hudl global navigation container
SSR_WEBNAV_GENERIC = "header, nav[role='navigation']"

# Combined fallback chain
SSR_WEBNAV_CONTAINER = (
    f"{SSR_WEBNAV_PRIMARY}, {SSR_WEBNAV_FALLBACK}, {SSR_WEBNAV_GENERIC}"
)
