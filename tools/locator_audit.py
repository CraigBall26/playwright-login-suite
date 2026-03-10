# tools/locator_audit.py
# ----------------------
# Offline utility for checking that every locator constant in the codebase
# still matches at least one real element on the live page.
#
# Run manually when selectors change or after a UI update:
#   python tools/locator_audit.py
#
# Exits with code 0 if all selectors match, 2 if any are missing (so CI
# can optionally run it as a blocking step).
import sys
import time
from importlib import (
    import_module,  # lets us load a module by its string name at runtime
)
from pathlib import Path  # cross-platform file path handling

from playwright.sync_api import sync_playwright

# Work out the repo root (one level above the tools/ folder) and add it
# to Python's import search path. Without this, "from locators.x import y"
# would fail when the script is run directly from the command line.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Print some context so it's obvious where the script is running from
# if something goes wrong with imports.
print("Locator audit running")
print("cwd:", Path.cwd())
print("project root added to sys.path:", ROOT)
print("sys.path (first 5 entries):")
for p in sys.path[:5]:
    print("  ", p)

# Each entry maps a short page name to a tuple of:
#   - the URL to load in the browser
#   - the dotted module path of the locator class (matches the file in locators/)
#   - the class name inside that module
#
# Swap the placeholder URLs for real ones before running.
PAGES = [
    (
        "login_identifier",
        (
            "https://your-app/login",
            "locators.login_identifier_locators",
            "LoginIdentifierLocators",
        ),
    ),
    (
        "password",
        (
            "https://your-app/login/password",
            "locators.password_locators",
            "PasswordLocators",
        ),
    ),
    (
        "dashboard",
        (
            "https://your-app/dashboard",
            "locators.dashboard_locators",
            "DashboardLocators",
        ),
    ),
]


def check_selectors(page, selector_str):
    """
    Takes a selector string (optionally comma-separated for fallbacks)
    and tries each one in turn against the current page.
    Returns the first selector that matches at least one element, plus
    the number of elements it matched. Returns (None, 0) if none matched.
    """
    for sel in [s.strip() for s in selector_str.split(",")]:
        try:
            loc = page.locator(sel)
            count = loc.count()
            if count > 0:
                return sel, count
        except Exception:
            # Some selectors can be malformed or target a frame — skip them
            # rather than crashing the whole audit.
            continue
    return None, 0


def audit():
    results = {}
    with sync_playwright() as pw:
        # Launch a headless Chromium browser — no window, runs in the background.
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})

        for name, (url, module_path, class_name) in PAGES:
            print(f"\n=== Auditing {name} @ {url} ===")

            # Dynamically import the locator module
            # (e.g. locators.login_identifier_locators).
            # This means we don't need a hardcoded import for each page —
            # adding a new entry to PAGES is all that's needed.
            try:
                mod = import_module(module_path)
            except Exception as e:
                print(f"ERROR importing {module_path}: {e}")
                results[name] = {"import_error": str(e)}
                continue

            # Pull the locator class out of the module by name.
            try:
                loc_class = getattr(mod, class_name)
            except AttributeError:
                print(f"ERROR: {class_name} not found in {module_path}")
                results[name] = {"class_error": f"{class_name} not found"}
                continue

            # Open a new browser tab and navigate to the page.
            page = context.new_page()
            try:
                # domcontentloaded is faster than waiting for all network requests —
                # we only need the DOM to be ready to query selectors.
                page.goto(url, wait_until="domcontentloaded", timeout=15000)
                # Small pause to let any JS-rendered elements appear.
                time.sleep(0.5)
            except Exception as e:
                print(f"ERROR loading {url}: {e}")
                results[name] = {"navigation_error": str(e)}
                page.close()
                continue

            page_results = {}

            # Iterate over every UPPER_CASE attribute on the locator class —
            # the convention in this codebase is that selector constants are
            # all caps (e.g. EMAIL_INPUT, SUBMIT_BUTTON).
            for attr in [a for a in dir(loc_class) if a.isupper()]:
                selector = getattr(loc_class, attr)
                matched, count = check_selectors(page, selector)
                page_results[attr] = {
                    "selector": selector,
                    # True if at least one element was found
                    "matched": bool(matched),
                    # which variant of the selector worked
                    "matched_selector": matched,
                    # how many elements matched
                    "count": count,
                }
                status = "OK" if matched else "MISSING"
                print(
                    f"{attr:20} {status:8} matched={matched} "
                    f"count={count} selector_used={matched}"
                )

            results[name] = page_results
            page.close()

        browser.close()
    return results


if __name__ == "__main__":
    r = audit()

    # Collect every selector that failed to match any element.
    missing = [
        (p, k)
        for p, v in r.items()
        if isinstance(v, dict)
        for k, s in v.items()
        if isinstance(s, dict) and not s.get("matched", True)
    ]

    if missing:
        print("\nMissing selectors:")
        for p, k in missing:
            print(f"- {p}.{k}")
        # Exit code 2 signals a failure — CI can treat this as a blocking error
        # if the audit is wired into the pipeline.
        raise SystemExit(2)

    print("\nAll locators matched at least one element.")
    raise SystemExit(0)
