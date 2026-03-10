import json
from pathlib import Path

_BASE = Path(__file__).parent


def load_json(relative_path: str):
    return json.loads((_BASE / relative_path).read_text(encoding="utf-8"))
