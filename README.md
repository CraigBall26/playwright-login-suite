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
  positive_tests/       # TC-001–006  happy path flows
  negative_tests/       # TC-100–109  validation and error states
  framework_tests/      # TC-200–202  locator and component checks
  environment_tests/    # TC-300–304  offline, slow network, multi-tab
  api_tests/            # TC-400–410  HTTP-level smoke tests (no browser)
```

See [TEST_PLAN.md](TEST_PLAN.md) for the full list of test cases.

---

## Setup

```bash
git clone https://github.com/CraigBall26/playwright-login-suite.git
cd playwright-login-suite

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
playwright install
```

Create a `.env` file in the project root:

```
HUDL_EMAIL=your@email.com
HUDL_PASSWORD=yourpassword
```

---

## Running Tests

**All tests:**
```bash
pytest --disable-warnings
```

**By marker:**
```bash
pytest -m api           # HTTP-layer checks only (fast, no browser)
pytest -m positive
pytest -m negative
pytest -m framework
pytest -m environment
```

**Headed mode (local debugging):**
```bash
pytest --headed -m positive
```

**Against staging:**
```bash
pytest --env staging
```

**Stop on first failure:**
```bash
pytest --maxfail=1
```

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
