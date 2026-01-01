# Setup page/room for tests.
# Keeps tests clean by handling Playwright lifecycle in one place.
# Keeps the framework readable.
# Imports JSON test data files for easy access.

import json
import os
import random
from pathlib import Path

import pytest
from dotenv import load_dotenv

from flows.login_flow import LoginFlow

# Load .env file automatically.
load_dotenv()


# ---------------------------------------------------------------------------
# BROWSER FIXTURE
# WebKit avoids Auth0 bot detection.
# Helps debug visual tests with --headed option.
#   - Running normally: headless=True (fast, stable)
#   - Running with --headed: headless=False (visible browser)
#   - slow_mo added when headed to watch interactions
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def browser(playwright, pytestconfig):
    headed = pytestconfig.getoption("--headed")

    browser = playwright.webkit.launch(
        headless=not headed,
        slow_mo=200 if headed else 0,
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
    context.close()  # Ensures clean state per test


# Fresh page for login tests (no session).
@pytest.fixture
def fresh_page(fresh_context):
    return fresh_context.new_page()


# ---------------------------------------------------------------------------
# CREDENTIAL FIXTURE (hidden in terminal output)
# ---------------------------------------------------------------------------


class HiddenCredentials(dict):
    def __repr__(self):
        return "<hidden>"


@pytest.fixture
def hudl_credentials():
    return HiddenCredentials(
        {
            "email": os.getenv("HUDL_EMAIL"),
            "password": os.getenv("HUDL_PASSWORD"),
        }
    )


# ---------------------------------------------------------------------------
# SESSION FIXTURES
# These fixtures create and reuse a valid Hudl session.
# Speeds up tests by skipping the login UI when not needed.
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def authenticated_session(browser, login_data, hudl_credentials):
    context = browser.new_context(
        viewport={"width": 1280, "height": 800},
        java_script_enabled=True,
    )
    page = context.new_page()

    flow = LoginFlow(page, login_data)
    flow.login(hudl_credentials["email"], hudl_credentials["password"])

    # Wait for dashboard to fully load before saving session.
    from pages.dashboard_page import DashboardPage

    dashboard = DashboardPage(page)
    dashboard.wait_for_loaded()

    context.storage_state(path="session.json")
    return "session.json"


@pytest.fixture
def context_with_session(browser, authenticated_session):
    """
    Provides a browser context that automatically loads the saved session.
    Used for tests that require a logged-in user.
    """
    return browser.new_context(
        viewport={"width": 1280, "height": 800},
        java_script_enabled=True,
        storage_state=authenticated_session,
    )


# ---------------------------------------------------------------------------
# TEST DATA FIXTURES
# Loads structured JSON files from tests/test_data/.
# Keeps tests clean by centralising all data.
# ---------------------------------------------------------------------------


def _load_json(relative_path: str):
    base_path = Path(__file__).parent / "test_data"
    file_path = base_path / relative_path

    with file_path.open() as f:
        return json.load(f)


# LOGIN TEST DATA
@pytest.fixture(scope="session")
def login_data():
    return _load_json("login/login_data.json")


@pytest.fixture(scope="session")
def invalid_emails():
    return _load_json("login/invalid_emails.json")


@pytest.fixture(scope="session")
def invalid_passwords():
    return _load_json("login/invalid_passwords.json")


# ENVIRONMENT TEST DATA
@pytest.fixture(scope="session")
def env_urls():
    return _load_json("environment/urls.json")


@pytest.fixture(scope="session")
def env_timeouts():
    return _load_json("environment/timeouts.json")


@pytest.fixture
def randomized_unknown_email(login_data):
    base_email = login_data["valid_but_incorrect_credentials"]["email"]

    local, domain = base_email.split("@")
    suffix = random.randint(100, 999)
    randomized = f"{local}{suffix}@{domain}"

    return randomized
