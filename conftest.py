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
    browser = playwright.webkit.launch(
        headless=False,  # run like a real browser
        args=["--start-maximized"],
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


# Slow network fixture for environment tests.
@pytest.fixture
def slow_network(browser):
    """
    Creates a fresh context + page with artificial latency added to
    fetch() and XMLHttpRequest. Useful for simulating slow environments.
    """

    context = browser.new_context(
        viewport={"width": 1280, "height": 800},
        java_script_enabled=True,
    )

    page = context.new_page()

    # Inject artificial latency into all network requests.
    page.add_init_script("""
        const originalFetch = window.fetch;
        window.fetch = async (...args) => {
            await new Promise(r => setTimeout(r, 300)); // 300ms delay
            return originalFetch(...args);
        };

        const originalOpen = XMLHttpRequest.prototype.open;
        XMLHttpRequest.prototype.open = function(...args) {
            this.addEventListener('readystatechange', () => {
                if (this.readyState === 1) {
                    const delay = 300;
                    const start = Date.now();
                    while (Date.now() - start < delay) {}
                }
            });
            return originalOpen.apply(this, args);
        };
    """)

    # Longer timeouts to match the slower environment.
    context.set_default_navigation_timeout(60000)
    context.set_default_timeout(60000)

    yield page
    context.close()
