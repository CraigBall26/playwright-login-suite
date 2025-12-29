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

# Load .env file automatically.
load_dotenv()


# BROWSER FIXTURE
# WebKit avoids Auth0 bot detection.
# Helps Debug visual tests with --headed option.
#   - Running normally: headless=True (fast, stable)
#   - Running with --headed: headless=False (visible browser)
#   - slow_mo added when headed to watch interactions
@pytest.fixture(scope="session")
def browser(playwright, pytestconfig):
    headed = pytestconfig.getoption("--headed")

    browser = playwright.webkit.launch(
        headless=not headed,  # headed=True → visible browser
        slow_mo=200 if headed else 0,  # slow motion only when debugging
    )
    return browser


# AUTHENTICATED CONTEXT (uses storage_state.json)
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


# FRESH CONTEXT (no storage_state) — used for login tests
@pytest.fixture
def fresh_context(browser):
    context = browser.new_context(
        viewport={"width": 1280, "height": 800},
        java_script_enabled=True,
    )
    yield context
    # Ensures clean state per test
    context.close()


# Fresh page for login tests (no session).
@pytest.fixture
def fresh_page(fresh_context):
    return fresh_context.new_page()


# HUDL CREDENTIALS
@pytest.fixture
def hudl_credentials():
    return {
        "email": os.getenv("HUDL_EMAIL"),
        "password": os.getenv("HUDL_PASSWORD"),
    }


# TEST DATA FIXTURES
# Loads structured JSON files from tests/test_data/.
# Keeps tests clean by centralising all data


def _load_json(relative_path: str):
    # Helper to load a JSON file from the test_data folder
    base_path = Path(__file__).parent / "test_data"
    file_path = base_path / relative_path

    with file_path.open() as f:
        return json.load(f)


# LOGIN TEST DATA
@pytest.fixture(scope="session")
def login_data():
    # Shared login data (safe synthetic values).
    return _load_json("login/login_data.json")


@pytest.fixture(scope="session")
def invalid_emails():
    # Invalid email cases.
    return _load_json("login/invalid_emails.json")


@pytest.fixture(scope="session")
def invalid_passwords():
    # Invalid password cases.
    return _load_json("login/invalid_passwords.json")


# ENVIRONMENT TEST DATA
@pytest.fixture(scope="session")
def env_urls():
    # Environment URLs used across tests.
    return _load_json("environment/urls.json")


@pytest.fixture(scope="session")
def env_timeouts():
    # Timeout values for page loads and waits.
    return _load_json("environment/timeouts.json")


@pytest.fixture
def randomized_unknown_email(login_data):
    # Generates a randomized email using test data.
    base_email = login_data["valid_but_incorrect_credentials"]["email"]

    # Split into local part + domain
    local, domain = base_email.split("@")

    # Generate a random 3-digit number (100–999)
    suffix = random.randint(100, 999)

    # Insert suffix before @
    randomized = f"{local}{suffix}@{domain}"
    return randomized
