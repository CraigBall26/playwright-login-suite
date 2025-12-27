# Dashboard Locators
# ------------------
# Provides a stable chain of selectors for detecting the real Hudl dashboard
# after a successful login. These selectors intentionally avoid generic
# elements that also appear on Auth0 pages.

# Primary SSR WebNav selector — unique to the real Hudl dashboard
SSR_WEBNAV_PRIMARY = (
    "#ssr-webnav > div > div.hui-webnav__grid.hui-navcontainer > "
    "nav.hui-webnav__grid-col--onewhole.hui-globalnav."
    "uni-env--dark.uni-environment--dark > "
    "div:nth-child(2)"
)

# Fallback: broader SSR WebNav container (still dashboard‑specific)
SSR_WEBNAV_FALLBACK = "nav.hui-globalnav, nav.hui-webnav__grid-col--onewhole"

# Combined fallback chain — intentionally excludes generic selectors
SSR_WEBNAV_CONTAINER = f"{SSR_WEBNAV_PRIMARY}, {SSR_WEBNAV_FALLBACK}"
