from __future__ import annotations

import re
from pathlib import Path
from typing import Mapping, Any


class TemplateError(ValueError):
    pass


_SECRET_PATTERNS = [re.compile(r'(?i)(api[_-]?key|password|secret|token)\s*[:=]\s*[\'"]?[A-Za-z0-9+/=_-]{8,}')]


def _validate(params: Mapping[str,str], spec: Mapping[str,Any]) -> None:
    for rule in spec["parameters"]:
        name = rule["name"]
        if name not in params or not params[name]:
            raise TemplateError(f"missing-parameter:{name}")
        value = params[name]
        if "pattern" in rule and re.fullmatch(rule["pattern"], value) is None:
            raise TemplateError(f"invalid-parameter:{name}")
        if "enum" in rule and value not in rule["enum"]:
            raise TemplateError(f"invalid-parameter:{name}")
        if "minLength" in rule and len(value) < int(rule["minLength"]):
            raise TemplateError(f"invalid-parameter:{name}")


def render_template(*, skeleton: Path, destination: Path, params: Mapping[str,str], spec: Mapping[str,Any]) -> list[Path]:
    _validate(params, spec)
    if destination.exists() and any(destination.iterdir()):
        raise TemplateError("destination-not-empty")
    values = dict(params)
    values["owner_short"] = params["owner"].split("/",1)[-1]
    values["system_short"] = params["system"].split("/",1)[-1]
    written: list[Path] = []
    for source in sorted(skeleton.rglob("*.tmpl")):
        rel = source.relative_to(skeleton)
        target = destination / str(rel)[:-5]
        text = source.read_text(encoding="utf-8")
        for key, value in values.items():
            text = text.replace("{{" + key + "}}", value)
        if "{{" in text or "}}" in text:
            raise TemplateError(f"unresolved-placeholder:{rel}")
        if any(pattern.search(text) for pattern in _SECRET_PATTERNS):
            raise TemplateError(f"embedded-secret:{rel}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        written.append(target)
    expected = set(spec["outputs"])
    actual = {str(p.relative_to(destination)) for p in written}
    if expected != actual:
        raise TemplateError(f"output-mismatch:{sorted(expected ^ actual)}")
    return written
