# Setup page/room for tests.
# Keeps tests clean by handling Playwright lifecycle in one place.
# Keeps the framework readable.

import os

import pytest
from dotenv import load_dotenv

# Load .env file automatically.
load_dotenv()


# ---------------------------------------------------------------------------
# BROWSER FIXTURE
# ---------------------------------------------------------------------------
# WebKit avoids Auth0 bot detection.
# This version RESPECTS pytest's --headed flag so you can debug visually.
#   - Running normally: headless=True (fast, stable)
#   - Running with --headed: headless=False (visible browser)
#   - slow_mo added when headed so you can watch interactions clearly
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def browser(playwright, pytestconfig):
    headed = pytestconfig.getoption("--headed")

    browser = playwright.webkit.launch(
        headless=not headed,  # headed=True → visible browser
        slow_mo=200 if headed else 0,  # slow motion only when debugging
    )
    return browser


# ---------------------------------------------------------------------------
# AUTHENTICATED CONTEXT (uses storage_state.json)
# ---------------------------------------------------------------------------
@pytest.fixture
def context(browser):
    return browser.new_context(
        viewport={"width": 1280, "height": 800},
        java_script_enabled=True,
        storage_state="storage_state.json",
    )


# Page fixture using the authenticated context.
@pytest.fixture
def page(context):
    return context.new_page()


# ---------------------------------------------------------------------------
# FRESH CONTEXT (no storage_state) — used for login tests
# ---------------------------------------------------------------------------
@pytest.fixture
def fresh_context(browser):
    context = browser.new_context(
        viewport={"width": 1280, "height": 800},
        java_script_enabled=True,
    )
    yield context
    context.close()  # ← CRITICAL FIX: ensures clean state per test


# Fresh page for login tests (no session).
@pytest.fixture
def fresh_page(fresh_context):
    return fresh_context.new_page()


# ---------------------------------------------------------------------------
# HUDL CREDENTIALS
# ---------------------------------------------------------------------------
@pytest.fixture
def hudl_credentials():
    return {
        "email": os.getenv("HUDL_EMAIL"),
        "password": os.getenv("HUDL_PASSWORD"),
    }
