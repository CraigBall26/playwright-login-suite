# Logs in once manually and saves the authenticated session to storage_state.json
# Run this script manually before running the test suite.

import os

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

HUDL_EMAIL = os.getenv("HUDL_EMAIL")
HUDL_PASSWORD = os.getenv("HUDL_PASSWORD")


def run():
    with sync_playwright() as p:
        browser = p.webkit.launch(headless=False)
        context = browser.new_context()

        page = context.new_page()
        page.goto("https://www.hudl.com/login")

        # Step 1: enter email
        page.get_by_label("Email").fill(HUDL_EMAIL)

        # Click the primary Continue button (not Google/Facebook/Apple)
        page.locator("button[data-action-button-primary='true']").click()

        # Step 2: enter password
        # Select ONLY the input, not the "show password" toggle
        page.locator("input#password").fill(HUDL_PASSWORD)

        # Click the primary Continue button again
        page.locator("button[data-action-button-primary='true']").click()

        # Wait for successful login redirect
        page.wait_for_url("**/home**", timeout=30000)

        # Save authenticated session
        context.storage_state(path="storage_state.json")

        browser.close()


if __name__ == "__main__":
    run()
