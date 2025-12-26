# Setup page/room for tests.
# Keeps tests clean by handling Playwright lifecycle in one place.
# Keeps the framework readable.

import os

import pytest
from dotenv import load_dotenv

# Load .env file automatically.
load_dotenv()


# Browser fixture (WebKit avoids Auth0 bot detection).
@pytest.fixture(scope="session")
def browser(playwright):
    # WebKit must run headless to avoid Inspector and random crashes.
    browser = playwright.webkit.launch(
        headless=True,
    )
    return browser


# Context fixture using an authenticated session (storage_state.json).
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


# Fresh context for login tests (no storage_state).
@pytest.fixture
def fresh_context(browser):
    return browser.new_context(
        viewport={"width": 1280, "height": 800},
        java_script_enabled=True,
    )


# Fresh page for login tests (no session).
@pytest.fixture
def fresh_page(fresh_context):
    return fresh_context.new_page()


# Hudl login details pulled from .env.
@pytest.fixture
def hudl_credentials():
    return {
        "email": os.getenv("HUDL_EMAIL"),
        "password": os.getenv("HUDL_PASSWORD"),
    }
