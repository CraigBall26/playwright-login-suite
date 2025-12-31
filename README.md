# Hudl Login Flow Automation Suite

Automated tests for the Hudl login flow using Playwright (Python). This repository focuses on a small, well-organised framework centered on the login experience and related behaviours.

---

## Table of contents
- [What this project covers](#what-this-project-covers)  
- [Project structure](#project-structure)  
- [Folder overview](#folder-overview)  
- [Test coverage](#test-coverage)  
- [Tools used](#tools-used)  
- [Setup & running the tests](#setup--running-the-tests)  
- [Credentials](#credentials)  
- [Author](#author)  
- [Notes](#notes)


---

## What this project covers
- A simple, readable automation framework with minimal complexity.  
- Positive, negative, environment-based, and framework tests.  
- Realistic user interaction scenarios for the Hudl login flow.

---

## Project structure
Root folders:
```
code/
  tests/
    positive_tests/
    negative_tests/
    framework_tests/
    environment_tests/
  flows/
  pages/
  locators/
  test_data/
  environment/
  login/
```


---

## Folder overview
- locators/ — centralised selectors for stability  
- pages/ — page objects (Identifier, Password, Dashboard)  
- flows/ — small reusable steps (e.g., login, logout)  
- tests/ — actual test files grouped by type  
- test_data/ — structured data for different login and environment scenarios

Keeping selectors and page behaviours separated reduces duplication and improves maintainability.


---

## Test coverage
All test IDs and descriptions are listed in [TEST_COVERAGE.md](./TEST_COVERAGE.md).


---

## Tools used
- Playwright (Python)  
- pytest  
- Black, Ruff, isort (formatting & linting)  
- Makefile (convenience commands)

Python was chosen for familiarity and to keep focus on tests rather than learning new syntax.


---

## Setup & running the tests
Full setup and run instructions are available in [SETUP.md](./SETUP.md). That document covers installation, environment variables, and how to execute the suite.


---

## Credentials
Credentials are loaded from environment variables. No sensitive data is stored in the repository.


---

## Author
Craig Ball — Senior QA Engineer

I’m an American football fan, which influences how I think about realistic user scenarios and edge cases.


---

## Notes
- The suite is intentionally focused on the login flow.  
- Tests run against the public Hudl UI.  
- Selectors are centralised to help keep tests stable.  
- The framework is designed to be readable and straightforward.
