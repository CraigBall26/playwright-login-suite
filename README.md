# **Hudl Login Flow Automation Suite**

Automated tests for the Hudl login flow using Playwright (Python).  
This repository focuses on a small, well‑organised framework centered on the login experience and related behaviours.
<br><br>

---

## **👤 Author**

Craig Ball — Senior QA Engineer  

I’m an American football fan, which influences how I think about realistic user scenarios and edge cases.

---

## **📚 Table of contents**

- [🚀 Setup & running the tests](#-setup--running-the-tests)  
- [📌 What this project covers](#-what-this-project-covers)  
- [📁 Project structure](#-project-structure)  
- [🗂️ Folder overview](#️-folder-overview)  
- [🛠️ Tools used](#️-tools-used)  
- [🔐 Credentials](#-credentials)  
- [📝 Notes](#-notes)  
- [🧪 Test coverage](#-test-coverage)

<br><br>

---

## **🚀 Setup & running the tests**

This section explains how to install dependencies, configure your environment, and run the test suite locally.  
Follow the steps below in order.

---

### **1. Clone the repository**

```bash
git clone https://github.com/CraigBall26/login-flow-automation.git
cd login-flow-automation
```

---

### **2. Create and activate a virtual environment**

A virtual environment keeps project dependencies isolated.

```bash
python3 -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
```

---

### **3. Install Python dependencies**

All required packages are listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

---

### **4. Install Playwright browsers**

Playwright requires browser binaries to run tests.

```bash
playwright install
```

---

### **5. Set your environment variables**

The suite uses environment variables for credentials.  
No credentials are stored in the repository.

macOS / Linux:

```bash
export HUDL_USERNAME="your-email"
export HUDL_PASSWORD="your-password"
```

Windows PowerShell:

```powershell
setx HUDL_USERNAME "your-email"
setx HUDL_PASSWORD "your-password"
```

Restart your terminal after using `setx`.

---

### **6. Run the test suite**

Run all tests:

```bash
pytest
```

Run a specific group:

```bash
pytest code/tests/positive_tests
pytest code/tests/negative_tests
pytest code/tests/environment_tests
pytest code/tests/framework_tests
```

Run a single test file:

```bash
pytest code/tests/positive_tests/test_login_success.py
```

Run a single test by node ID:

```bash
pytest code/tests/positive_tests/test_login_success.py::test_valid_login
```

---

### **7. Troubleshooting**

- **Playwright browsers missing:**  
  ```bash
  playwright install
  ```

- **Environment variables not detected:**  
  Ensure your terminal session is restarted and the virtual environment is active.

- **Import errors:**  
  Confirm you are running commands from the project root.

  <br><br>

---

## **📌 What this project covers**

- A simple, readable automation framework with minimal complexity.  
- Positive, negative, environment‑based, and framework tests.  
- Realistic user interaction scenarios for the Hudl login flow.

<br><br>

---

## **📁 Project structure**

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

## **🗂️ Folder overview**

- **locators/** — centralised selectors for stability  
- **pages/** — page objects (Identifier, Password, Dashboard)  
- **flows/** — small reusable steps (e.g., login, logout)  
- **tests/** — actual test files grouped by type  
- **test_data/** — structured data for different login and environment scenarios  

Keeping selectors and page behaviours separated reduces duplication and improves maintainability.

<br><br>

---

## **🛠️ Tools used**

- Playwright (Python)  
- pytest  
- Black, Ruff, isort (formatting & linting)  
- Makefile (convenience commands)

Python was chosen for familiarity and to keep focus on tests rather than learning new syntax.

<br><br>
---

## **🔐 Credentials**

Credentials are loaded from environment variables.  
No sensitive data is stored in the repository.

<br><br>

---

## **📝 Notes**

- The suite is intentionally focused on the login flow.  
- Tests run against the public Hudl UI.  
- Selectors are centralised to help keep tests stable.  
- The framework is designed to be readable and straightforward.

<br><br>

---

# **🧪 Test coverage**

Tests are grouped by category to match the folder structure in `tests/`.  
Each row includes the test ID, test name, and what the test validates.

---

## **1. Positive Tests (000–099)**

| Test ID | Test Name | Validates |
|--------|-----------|-----------|
| **TC‑000** | Valid login | Confirms a user can log in normally and reach the dashboard. Shows the core login flow works end‑to‑end. |
| **TC‑001** | Correcting email before login | Checks that fixing a mistyped email works as expected. Ensures the flow recovers cleanly from user error by using back buttons. |
| **TC‑002** | Direct navigation redirects to login | Verifies protected pages redirect unauthenticated users. Prevents bypassing the login screen. |
| **TC‑003** | Login with saved session | Confirms users with an active session skip the login page. Shows session persistence behaves correctly. |
| **TC‑004** | Logout redirects to homepage | Ensures logging out clears the session and returns the user to login. Confirms session invalidation works. |
| **TC‑005** | Session remains active after page refresh | Checks that refreshing the dashboard keeps the user logged in. Confirms session stability. |

---

## **2. Negative Tests (100–199)**

| Test ID | Test Name | Validates |
|--------|-----------|-----------|
| **TC‑100** | Invalid email format | Shows an error when the email format is wrong. Stops the user from continuing. |
| **TC‑101** | Invalid domain email | Rejects emails with invalid domains. Prevents users from progressing with unsupported addresses. |
| **TC‑102** | Empty email field | Ensures the user can’t continue with a blank email. Basic required‑field behaviour. |
| **TC‑103** | Whitespace‑only email | Treats whitespace as empty input. Prevents bypassing validation with invisible characters. |
| **TC‑104** | Disallowed characters in email | Blocks emails containing illegal characters. Confirms strict formatting rules. |
| **TC‑105** | Known user, wrong password | Shows a clear error for incorrect passwords. Keeps the user on the password page. |
| **TC‑106** | Unknown user, wrong password | Displays the correct error for unknown accounts. Avoids leaking information about valid users. |
| **TC‑107** | Known user, empty password | Prevents login when the password field is blank. Basic required‑field behaviour. |
| **TC‑108** | Switch from known → unknown user | Resets the flow when the email is changed. Ensures the UI updates correctly. |
| **TC‑109** | Switch from unknown → known user (wrong password) | Updates the flow after changing the email. Shows the correct password error. |

---

## **3. Framework Tests (200–299)**

**Framework tests validate the stability of the automation framework itself, ensuring selectors and shared UI components behave consistently across the suite.**

| Test ID | Test Name | Validates |
|--------|-----------|-----------|
| **TC‑200** | Locator stability | Confirms all selectors resolve correctly. Helps catch UI changes early. |
| **TC‑201** | Identity page social buttons | Checks that social login buttons appear as expected. Confirms the layout is consistent. |
| **TC‑202** | Identity & password page legal links | Ensures Privacy and Terms links are present and correct. Basic compliance check. |

---

## **4. Environment Tests (300–399)**

Environment tests reflect real situations Hudl users encounter — especially coaches and players dealing with unstable stadium Wi‑Fi, shared devices, and multiple tabs during film review.

| Test ID | Test Name | Validates |
|--------|-----------|-----------|
| **TC‑300** | Login in two tabs | Confirms logging in one tab updates the other. Mirrors a coach opening Hudl in multiple tabs during prep. |
| **TC‑301** | Logout invalidates other tabs | Ensures logging out in one tab logs out all tabs. Matches shared‑device use during practice. |
| **TC‑302** | Offline before password page | Shows the correct message when going offline early. Reflects losing Wi‑Fi while entering an email. |
| **TC‑303** | Offline after password page | Handles offline state mid‑flow without crashing. Matches unstable stadium or school Wi‑Fi. |
| **TC‑304** | Slow network login | Simulates a test under 3G conditions
