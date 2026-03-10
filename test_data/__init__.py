# Test data helpers.
# Provides a single load_json() utility so test files and conftest fixtures
# can load JSON data files without repeating path-resolution boilerplate.

import json
from pathlib import Path

_BASE = Path(__file__).parent


def load_json(relative_path: str):
    # Resolve the path relative to the test_data/ directory and return
    # the parsed contents. Called at module level for pytest parametrize.
    return json.loads((_BASE / relative_path).read_text(encoding="utf-8"))
