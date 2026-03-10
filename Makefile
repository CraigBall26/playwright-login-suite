# Shortcuts for common tasks

# Run the test suite.
test:
    pytest --disable-warnings

# Run Ruff with the same strictness as CI.
lint:
    ruff check . --fix --exit-non-zero-on-fix


# Auto-format codebase with Ruff.
format:
    ruff format .

# Install pre-commit hooks for automatic checks.
hooks:
    pre-commit install

