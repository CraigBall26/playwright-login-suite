# Setup page/room for tests
# Keeps tests clean by handling Playwright lifecycle in one place.
# Keeps the framework readable

import pytest
from playwright.sync_api import sync_playwright


# Launches a fresh Chromium browser for each test.
@pytest.fixture
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


# Creates a new page for each test.
@pytest.fixture
def page(browser):
    page = browser.new_page()
    yield page
    page.close()
