# Test setup for the login‑flow suite.
# Keeps things tidy by handling browser setup, sessions, and test data in one place.

import json
import os
import random
from pathlib import Path

import pytest
from dotenv import load_dotenv

from config import get_config
from flows.login_flow import LoginFlow

# Load .env values for credentials.
load_dotenv()


# ---------------------------------------------------------------------------
# Environment configuration
# Controls which environment tests run against.
# Defaults to production; override with: pytest --env staging
# ---------------------------------------------------------------------------


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="production",
        help="Target environment: production (default) or staging",
    )


@pytest.fixture(scope="session")
def env_config(pytestconfig):
    return get_config(pytestconfig.getoption("--env"))


# ---------------------------------------------------------------------------
# Browser fixture
# Starts WebKit for all tests.
# Headless by default, but can show the browser when running with --headed.
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
# Authenticated context
# Opens a browser context using a saved session file.
# Used for tests that need a logged‑in user.
# ---------------------------------------------------------------------------


@pytest.fixture
def context(browser):
    ctx = browser.new_context(
        viewport={"width": 1280, "height": 800},
        java_script_enabled=True,
    )
    yield ctx
    ctx.close()


# Page fixture using the authenticated context.
@pytest.fixture
def page(context):
    p = context.new_page()
    yield p
    p.close()


# ---------------------------------------------------------------------------
# Fresh context (no session)
# Used for login tests that need a clean state.
# ---------------------------------------------------------------------------


@pytest.fixture
def fresh_context(browser):
    context = browser.new_context(
        viewport={"width": 1280, "height": 800},
        java_script_enabled=True,
    )
    yield context
    context.close()


# Fresh page for login tests.
@pytest.fixture
def fresh_page(fresh_context):
    return fresh_context.new_page()


# ---------------------------------------------------------------------------
# Credential fixture
# Loads Hudl credentials from environment variables.
# Keeps them hidden in test output.
# ---------------------------------------------------------------------------


class HiddenCredentials(dict):
    def __repr__(self):
        return "<hidden>"


@pytest.fixture(scope="session")
def hudl_credentials():
    return HiddenCredentials(
        {
            "email": os.getenv("HUDL_EMAIL"),
            "password": os.getenv("HUDL_PASSWORD"),
        }
    )


# ---------------------------------------------------------------------------
# Session fixtures
# Logs in once, saves the session, and reuses it for faster tests.
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

    # Wait for dashboard before saving the session.
    from pages.dashboard_page import DashboardPage

    dashboard = DashboardPage(page)
    dashboard.wait_for_loaded()

    context.storage_state(path="session.json")
    return "session.json"


# Context that loads the saved session.
@pytest.fixture
def context_with_session(browser, authenticated_session):
    return browser.new_context(
        viewport={"width": 1280, "height": 800},
        java_script_enabled=True,
        storage_state=authenticated_session,
    )


# ---------------------------------------------------------------------------
# Test data fixtures
# Loads JSON files from tests/test_data/.
# Keeps test data in one place.
# ---------------------------------------------------------------------------


def _load_json(relative_path: str):
    base_path = Path(__file__).parent / "test_data"
    file_path = base_path / relative_path

    with file_path.open() as f:
        return json.load(f)


# Login test data
@pytest.fixture(scope="session")
def login_data(env_config):
    data = _load_json("login/login_data.json")
    # Override URLs from centralised config so --env is respected.
    data["base_url"] = env_config.base_url
    data["login_url"] = env_config.login_url
    return data


@pytest.fixture(scope="session")
def invalid_emails():
    return _load_json("login/invalid_emails.json")


@pytest.fixture(scope="session")
def invalid_passwords():
    return _load_json("login/invalid_passwords.json")


# Environment test data
@pytest.fixture(scope="session")
def env_urls(env_config):
    return {
        "login_page": env_config.login_url,
        "home_url": env_config.home_url,
    }


@pytest.fixture(scope="session")
def env_timeouts(env_config):
    return {
        "page_load": env_config.page_load_timeout,
        "element_wait": env_config.element_wait_timeout,
    }


# Randomised unknown email for negative tests.
@pytest.fixture
def randomized_unknown_email(login_data):
    base_email = login_data["valid_but_incorrect_credentials"]["email"]

    local, domain = base_email.split("@")
    suffix = random.randint(100, 999)
    randomized = f"{local}{suffix}@{domain}"

    return randomized


# ---------------------------------------------------------------------------
# Chromium‑only page fixture
# Used for tests that must avoid macOS Apple login pop‑ups.
# Runs Chromium headless for a clean, predictable flow.
# ---------------------------------------------------------------------------


@pytest.fixture
def chromium_page(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
    browser.close()


# ---------------------------------------------------------------------------
# API fixtures
# Shared HTTP responses for the API test layer.
# Fetched once per session so the same request isn't repeated across tests.
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def login_page_response(env_config):
    import requests

    from constants import REQUEST_TIMEOUT

    return requests.get(env_config.login_url, timeout=REQUEST_TIMEOUT)
