# Playwright Login Suite

A focused automation suite for Hudl's login flow, built with **Playwright** and **pytest**. Covers UI behaviour end-to-end and HTTP-layer checks at the API level, with a CI pipeline that runs both in sequence.

---

## Tech

- Python 3.12
- Playwright (sync API, WebKit + Chromium)
- pytest
- requests (API layer)
- Ruff (linting)
- GitHub Actions

---

## Structure

```
tests/
  api/                        # TC-400–410  HTTP-level smoke tests (no browser)
  ui/
    positive/               # TC-001–006  happy path flows
    negative/               # TC-100–109  validation and error states
    framework/              # TC-300–302  locator and component checks
    environment/            # TC-200–204  offline, slow network, multi-tab
```

See [TEST_PLAN.md](TEST_PLAN.md) for the full list of test cases.

---

## Setup & Running the Tests

This section explains how to install dependencies, configure your environment, and run the test suite locally.
Follow the steps below in order after opening the terminal.

---

**1. Clone the repository**
```bash
git clone https://github.com/CraigBall26/playwright-login-suite.git
cd playwright-login-suite
```

**2. Create and activate a virtual environment**

A virtual environment keeps project dependencies isolated.
```bash
python3 -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
```

**3. Install Python dependencies**

All required packages are listed in `requirements.txt`.
```bash
pip install -r requirements.txt
```

**4. Install Playwright browsers**

Playwright requires browser binaries to run tests.
```bash
playwright install
```

**5. Leave the virtual environment**
```bash
deactivate
```

**6. Set your environment variables**

The suite uses environment variables for credentials. No credentials are stored in the repository.

macOS / Linux:
```bash
export HUDL_EMAIL='your-email'
export HUDL_PASSWORD='your-password'   # Use single quotes if your password contains !, $, &, etc.
```

Windows PowerShell:
```powershell
setx HUDL_EMAIL "your-email"
setx HUDL_PASSWORD "your-password"
```
> Restart your terminal after using `setx`.

**7. Re-activate the virtual environment**
```bash
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
```

**8. Run the test suite**

Run all tests:
```bash
pytest
```

Run a specific group:
```bash
pytest tests/api
pytest tests/ui/positive
pytest tests/ui/negative
pytest tests/ui/framework
pytest tests/ui/environment
```

Run by marker:
```bash
pytest -m api           # HTTP-layer checks only (fast, no browser)
pytest -m positive
pytest -m negative
pytest -m framework
pytest -m environment
```

Run a single test file:
```bash
pytest tests/ui/positive/test_valid_login.py
```

Run a single test by node ID:
```bash
pytest tests/ui/positive/test_valid_login.py::test_valid_login
```

Other useful flags:
```bash
pytest --headed -m positive    # show the browser window
pytest --env staging           # run against staging
pytest --maxfail=1             # stop on first failure
```

**9. Troubleshooting**

*Playwright browsers missing:*
```bash
playwright install
```

*Environment variables not detected:*
Ensure your terminal session is restarted and the virtual environment is active.

*Import errors:*
Confirm you are running commands from the project root.

---

## CI

GitHub Actions runs three jobs in order:

1. **api-tests** — stateless HTTP checks, no browser, runs in seconds
2. **framework-tests** — UI layer, ruff lint included
3. **environment-tests** — offline, slow network, multi-tab scenarios

Framework and environment jobs only run if the previous job is green.

---

## Notes

Intentionally lightweight — the goal is clarity and practical patterns, not a full framework. Page objects, fixture-based setup, environment-driven config, and a clean separation between UI and API test layers.
