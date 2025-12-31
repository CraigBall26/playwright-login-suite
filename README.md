Hudl Login Flow Automation Suite This project automates the Hudl login flow using Playwright and Python. The scope is intentionally small and focused on the login experience and the behaviours around it. Everything is organised to be easy to read, easy to run, and easy for reviewers to follow.

📌 What This Project Covers A simple, organised automation framework

Positive, negative, framework, and environment‑based tests

Clear structure without unnecessary complexity

A realistic look at how users interact with the login flow

📁 Project Structure Code Code tests/ positive_tests/ negative_tests/ framework_tests/ environment_tests/

flows/ pages/ locators/ test_data/ environment/ login/ Folder overview locators/ – all selectors in one place

pages/ – page objects for Identifier, Password, Dashboard

flows/ – small reusable steps like login and logout

tests/ – the actual test files, grouped by type

test_data/ – structured data for login and environment scenarios

This keeps things tidy and avoids repeating code.

🧪 Test Coverage

All test IDs and descriptions are listed here:

👉 TEST_COVERAGE.md

🛠️ Tools Used Playwright (Python)

Pytest Black, Ruff, isort Makefile for simple commands

I chose Python because it’s the language I’m most comfortable with. Playwright supports multiple languages, but using Python let me focus on the tests themselves rather than learning a new syntax.

🚀 Setup & Running the Tests Full setup instructions are available here:

👉 SETUP.md

This includes installation, environment variables, and how to run the suite.

🔐 Credentials

Credentials are loaded from environment variables. Nothing sensitive is stored in the repo.

👤 Author

Craig Ball — Senior QA Engineer.

I’m an American football fan, which influences how I think about realistic user scenarios and edge cases.

📄 Notes The suite is intentionally focused on the login flow

Tests run against the public Hudl UI

Selectors are centralised to keep things stable

The framework is designed to be readable and straightforward
