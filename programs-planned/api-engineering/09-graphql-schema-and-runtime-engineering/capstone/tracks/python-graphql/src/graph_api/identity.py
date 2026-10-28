from __future__ import annotations
import base64
from .model import ValidationError

_ALLOWED = {"Project", "AnalysisRun", "Artifact"}

def encode_global_id(type_name: str, local_id: str) -> str:
    if type_name not in _ALLOWED:
        raise ValidationError("unsupported global identifier type")
    if not local_id or ":" in type_name:
        raise ValidationError("invalid local identifier")
    raw = f"{type_name}:{local_id}".encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")

def decode_global_id(value: str) -> tuple[str, str]:
    try:
        padded = value + "=" * (-len(value) % 4)
        raw = base64.urlsafe_b64decode(padded.encode("ascii")).decode("utf-8")
        type_name, local_id = raw.split(":", 1)
    except Exception as exc:
        raise ValidationError("malformed global identifier") from exc
    if type_name not in _ALLOWED or not local_id:
        raise ValidationError("unsupported global identifier")
    return type_name, local_id
