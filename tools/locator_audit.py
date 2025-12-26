# tools/locator_audit.py
from pathlib import Path
import sys
import time
from importlib import import_module
from playwright.sync_api import sync_playwright

# Ensure the repo root is on sys.path so imports like "locators.*" work
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Debug info to confirm import paths when running
print("Locator audit running")
print("cwd:", Path.cwd())
print("project root added to sys.path:", ROOT)
print("sys.path (first 5 entries):")
for p in sys.path[:5]:
    print("  ", p)

# Map page names to (url, locator_module, locator_class_name)
# Replace the URLs with your real local/dev/staging URLs before running.
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
    Accepts a comma-separated selector string (fallbacks).
    Returns (matched_selector or None, count)
    """
    for sel in [s.strip() for s in selector_str.split(",")]:
        try:
            loc = page.locator(sel)
            count = loc.count()
            if count > 0:
                return sel, count
        except Exception:
            # ignore invalid selectors or frame issues here
            continue
    return None, 0


def audit():
    results = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        for name, (url, module_path, class_name) in PAGES:
            print(f"\n=== Auditing {name} @ {url} ===")
            try:
                mod = import_module(module_path)
            except Exception as e:
                print(f"ERROR importing {module_path}: {e}")
                results[name] = {"import_error": str(e)}
                continue

            try:
                loc_class = getattr(mod, class_name)
            except AttributeError:
                print(f"ERROR: {class_name} not found in {module_path}")
                results[name] = {"class_error": f"{class_name} not found"}
                continue

            page = context.new_page()
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=15000)
                time.sleep(0.5)
            except Exception as e:
                print(f"ERROR loading {url}: {e}")
                results[name] = {"navigation_error": str(e)}
                page.close()
                continue

            page_results = {}
            for attr in [a for a in dir(loc_class) if a.isupper()]:
                selector = getattr(loc_class, attr)
                matched, count = check_selectors(page, selector)
                page_results[attr] = {
                    "selector": selector,
                    "matched": bool(matched),
                    "matched_selector": matched,
                    "count": count,
                }
                status = "OK" if matched else "MISSING"
                print(
                    f"{attr:20} {status:8} matched={matched} count={count} selector_used={matched}"
                )
            results[name] = page_results
            page.close()

        browser.close()
    return results


if __name__ == "__main__":
    r = audit()
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
        # exit non-zero so CI can catch failures
        raise SystemExit(2)
    print("\nAll locators matched at least one element.")
    raise SystemExit(0)
