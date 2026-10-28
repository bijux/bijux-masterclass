from __future__ import annotations

from pathlib import Path
import json
from typing import Any

import jsonschema

from .envelope import EventEnvelope


def load_schema(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("schema root must be an object")
    return value


def validate_payload(event: EventEnvelope, schema: dict[str, Any]) -> None:
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.Draft202012Validator(
        schema, format_checker=jsonschema.FormatChecker()
    ).validate(event.data)
