# Shortcuts for common tasks

# Run the test suite.
test:
    pytest

# Check codebase with Ruff.
lint:
    ruff check .

# Auto-format codebase with Ruff.
format:
    ruff format .

# Install pre-commit hooks for automatic checks.
hooks:
    pre-commit install