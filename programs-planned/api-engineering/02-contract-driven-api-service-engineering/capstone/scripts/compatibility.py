"""Conservative, direction-aware OpenAPI compatibility analysis.

The checker is deliberately smaller than a general-purpose API-diff product.
It is used as an educational gate and never claims to prove every consumer
compatible. Hard breaks block a minor release; risky response changes require
an explicit review decision; additive changes are recorded as release evidence.
"""
from __future__ import annotations

import copy
import json
from typing import Any, Iterator

HTTP_METHODS = {
    "get", "put", "post", "delete", "options", "head", "patch", "trace"
}


def iter_path_operations(
    spec: dict[str, Any],
) -> Iterator[tuple[str, str, dict[str, Any], dict[str, Any]]]:
    for path, path_item in (spec.get("paths") or {}).items():
        if not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            lower = str(method).lower()
            if lower in HTTP_METHODS and isinstance(operation, dict):
                yield path, lower.upper(), operation, path_item
        for method, operation in (path_item.get("additionalOperations") or {}).items():
            if isinstance(operation, dict):
                yield path, str(method).upper(), operation, path_item


def _local_pointer(document: dict[str, Any], ref: str) -> Any:
    if not ref.startswith("#/"):
        return None
    current: Any = document
    for token in ref[2:].split("/"):
        key = token.replace("~1", "/").replace("~0", "~")
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def _resolved_schema(schema: Any, root: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(schema, dict):
        return {}
    ref = schema.get("$ref")
    if isinstance(ref, str):
        target = _local_pointer(root, ref)
        if isinstance(target, dict):
            merged = copy.deepcopy(target)
            merged.update({k: v for k, v in schema.items() if k != "$ref"})
            return _resolved_schema(merged, root)
    branches = schema.get("allOf")
    if isinstance(branches, list):
        merged: dict[str, Any] = {
            key: copy.deepcopy(value)
            for key, value in schema.items()
            if key != "allOf"
        }
        properties: dict[str, Any] = dict(merged.get("properties") or {})
        required = set(merged.get("required") or [])
        for branch in branches:
            item = _resolved_schema(branch, root)
            properties.update(item.get("properties") or {})
            required.update(item.get("required") or [])
            for key in ("type", "additionalProperties"):
                if key in item and key not in merged:
                    merged[key] = copy.deepcopy(item[key])
        if properties:
            merged["properties"] = properties
        if required:
            merged["required"] = sorted(required)
        return merged
    return schema


def _types(schema: dict[str, Any]) -> set[str]:
    value = schema.get("type")
    if isinstance(value, str):
        return {value}
    if isinstance(value, list):
        return {str(item) for item in value}
    if "properties" in schema:
        return {"object"}
    if "items" in schema:
        return {"array"}
    return set()


def _record(bucket: list[dict[str, str]], location: str, reason: str) -> None:
    item = {"location": location, "reason": reason}
    if item not in bucket:
        bucket.append(item)


def _compare_schema(
    old_raw: Any,
    new_raw: Any,
    old_root: dict[str, Any],
    new_root: dict[str, Any],
    direction: str,
    location: str,
    breaking: list[dict[str, str]],
    risky: list[dict[str, str]],
    additive: list[dict[str, str]],
) -> None:
    old = _resolved_schema(old_raw, old_root)
    new = _resolved_schema(new_raw, new_root)
    if not old or not new:
        if old != new:
            _record(risky, location, "schema shape changed and requires review")
        return

    old_types = _types(old)
    new_types = _types(new)
    if old_types and new_types and old_types != new_types:
        if direction == "request":
            removed = old_types - new_types
            if removed:
                _record(
                    breaking,
                    location,
                    f"request types no longer accepted: {sorted(removed)}",
                )
            added = new_types - old_types
            if added:
                _record(additive, location, f"request types added: {sorted(added)}")
        else:
            added = new_types - old_types
            if added:
                _record(
                    breaking,
                    location,
                    f"response may emit new types: {sorted(added)}",
                )
            removed = old_types - new_types
            if removed:
                _record(
                    risky,
                    location,
                    f"response types narrowed: {sorted(removed)}",
                )

    old_enum = old.get("enum")
    new_enum = new.get("enum")
    if isinstance(old_enum, list) and isinstance(new_enum, list):
        old_values = {json.dumps(value, sort_keys=True) for value in old_enum}
        new_values = {json.dumps(value, sort_keys=True) for value in new_enum}
        if direction == "request":
            if old_values - new_values:
                _record(breaking, location, "request enum narrowed")
            if new_values - old_values:
                _record(additive, location, "request enum widened")
        else:
            if new_values - old_values:
                _record(
                    risky,
                    location,
                    "response enum widened; exhaustive consumers require review",
                )
            if old_values - new_values:
                _record(risky, location, "response enum narrowed; behavior changed")

    lower = (
        "minimum", "exclusiveMinimum", "minLength", "minItems", "minProperties"
    )
    upper = (
        "maximum", "exclusiveMaximum", "maxLength", "maxItems", "maxProperties"
    )
    for key in lower:
        old_value, new_value = old.get(key), new.get(key)
        if (
            isinstance(old_value, (int, float))
            and isinstance(new_value, (int, float))
            and old_value != new_value
        ):
            if direction == "request" and new_value > old_value:
                _record(
                    breaking,
                    location,
                    f"request {key} increased from {old_value} to {new_value}",
                )
            elif direction == "response" and new_value < old_value:
                _record(
                    risky,
                    location,
                    f"response {key} decreased from {old_value} to {new_value}",
                )
            else:
                _record(
                    additive,
                    location,
                    f"{key} changed from {old_value} to {new_value}",
                )
    for key in upper:
        old_value, new_value = old.get(key), new.get(key)
        if (
            isinstance(old_value, (int, float))
            and isinstance(new_value, (int, float))
            and old_value != new_value
        ):
            if direction == "request" and new_value < old_value:
                _record(
                    breaking,
                    location,
                    f"request {key} decreased from {old_value} to {new_value}",
                )
            elif direction == "response" and new_value > old_value:
                _record(
                    risky,
                    location,
                    f"response {key} increased from {old_value} to {new_value}",
                )
            else:
                _record(
                    additive,
                    location,
                    f"{key} changed from {old_value} to {new_value}",
                )

    if old.get("pattern") != new.get("pattern"):
        if old.get("pattern") or new.get("pattern"):
            target = breaking if direction == "request" else risky
            _record(target, location, "regular-expression constraint changed")
    if old.get("uniqueItems") is not True and new.get("uniqueItems") is True:
        target = breaking if direction == "request" else risky
        _record(target, location, "uniqueItems became true")

    old_props = old.get("properties") if isinstance(old.get("properties"), dict) else {}
    new_props = new.get("properties") if isinstance(new.get("properties"), dict) else {}
    old_required = set(old.get("required") or [])
    new_required = set(new.get("required") or [])

    if direction == "request":
        for prop in sorted(new_required - old_required):
            _record(breaking, f"{location}.{prop}", "request property became required")
        for prop in sorted(old_props.keys() - new_props.keys()):
            if new.get("additionalProperties") is False:
                _record(
                    breaking,
                    f"{location}.{prop}",
                    "previous request property is no longer accepted",
                )
            else:
                _record(
                    risky,
                    f"{location}.{prop}",
                    "documented request property removed",
                )
        for prop in sorted(new_props.keys() - old_props.keys()):
            target = breaking if prop in new_required else additive
            reason = (
                "new request property is required"
                if prop in new_required
                else "optional request property added"
            )
            _record(target, f"{location}.{prop}", reason)
    else:
        for prop in sorted(old_required - new_required):
            _record(
                breaking,
                f"{location}.{prop}",
                "required response property removed or made optional",
            )
        for prop in sorted(old_props.keys() - new_props.keys()):
            _record(breaking, f"{location}.{prop}", "response property removed")
        for prop in sorted(new_props.keys() - old_props.keys()):
            _record(
                risky,
                f"{location}.{prop}",
                "response property added; strict closed-schema consumers require review",
            )

    for prop in sorted(old_props.keys() & new_props.keys()):
        _compare_schema(
            old_props[prop],
            new_props[prop],
            old_root,
            new_root,
            direction,
            f"{location}.{prop}",
            breaking,
            risky,
            additive,
        )

    old_items, new_items = old.get("items"), new.get("items")
    if isinstance(old_items, dict) and isinstance(new_items, dict):
        _compare_schema(
            old_items,
            new_items,
            old_root,
            new_root,
            direction,
            f"{location}[]",
            breaking,
            risky,
            additive,
        )

    old_additional = old.get("additionalProperties", True)
    new_additional = new.get("additionalProperties", True)
    if direction == "request" and old_additional is not False and new_additional is False:
        _record(breaking, location, "request object became closed")
    if direction == "response" and old_additional is False and new_additional is not False:
        _record(risky, location, "response object became open")

    for keyword in (
        "oneOf", "anyOf", "not", "if", "then", "else", "dependentSchemas"
    ):
        if old.get(keyword) != new.get(keyword) and (keyword in old or keyword in new):
            target = breaking if direction == "request" else risky
            _record(target, location, f"{keyword} composition changed")


def _parameters(
    path_item: dict[str, Any], operation: dict[str, Any]
) -> dict[tuple[str, str], dict[str, Any]]:
    result: dict[tuple[str, str], dict[str, Any]] = {}
    values = list(path_item.get("parameters") or []) + list(
        operation.get("parameters") or []
    )
    for item in values:
        if (
            isinstance(item, dict)
            and isinstance(item.get("name"), str)
            and isinstance(item.get("in"), str)
        ):
            result[(item["in"], item["name"])] = item
    return result


def compare_contracts(
    old: dict[str, Any], new: dict[str, Any]
) -> dict[str, Any]:
    breaking: list[dict[str, str]] = []
    risky: list[dict[str, str]] = []
    additive: list[dict[str, str]] = []

    old_ops = {
        (path, method): (operation, item)
        for path, method, operation, item in iter_path_operations(old)
    }
    new_ops = {
        (path, method): (operation, item)
        for path, method, operation, item in iter_path_operations(new)
    }

    for key, (old_operation, old_item) in old_ops.items():
        path, method = key
        location = f"{method} {path}"
        if key not in new_ops:
            _record(breaking, location, "operation removed")
            continue
        new_operation, new_item = new_ops[key]
        if old_operation.get("operationId") != new_operation.get("operationId"):
            _record(breaking, location, "operationId changed")
        if old_operation.get("security") != new_operation.get("security"):
            _record(breaking, location, "security requirements changed")

        old_parameters = _parameters(old_item, old_operation)
        new_parameters = _parameters(new_item, new_operation)
        for parameter_key, old_parameter in old_parameters.items():
            parameter_location = (
                f"{location} parameter {parameter_key[0]}:{parameter_key[1]}"
            )
            if parameter_key not in new_parameters:
                _record(breaking, parameter_location, "parameter removed")
                continue
            new_parameter = new_parameters[parameter_key]
            if not old_parameter.get("required") and new_parameter.get("required"):
                _record(breaking, parameter_location, "parameter became required")
            _compare_schema(
                old_parameter.get("schema"),
                new_parameter.get("schema"),
                old,
                new,
                "request",
                parameter_location,
                breaking,
                risky,
                additive,
            )
        for parameter_key, new_parameter in new_parameters.items():
            if parameter_key not in old_parameters:
                target = breaking if new_parameter.get("required") else additive
                _record(
                    target,
                    f"{location} parameter {parameter_key[0]}:{parameter_key[1]}",
                    "parameter added",
                )

        old_body = (
            old_operation.get("requestBody")
            if isinstance(old_operation.get("requestBody"), dict)
            else None
        )
        new_body = (
            new_operation.get("requestBody")
            if isinstance(new_operation.get("requestBody"), dict)
            else None
        )
        if old_body and not new_body:
            _record(breaking, f"{location} request", "request body removed")
        elif not old_body and new_body:
            target = breaking if new_body.get("required") else additive
            _record(target, f"{location} request", "request body added")
        elif old_body and new_body:
            if not old_body.get("required") and new_body.get("required"):
                _record(breaking, f"{location} request", "request body became required")
            old_content = old_body.get("content") or {}
            new_content = new_body.get("content") or {}
            for media in sorted(set(old_content) - set(new_content)):
                _record(
                    breaking,
                    f"{location} request {media}",
                    "request media type removed",
                )
            for media in sorted(set(new_content) - set(old_content)):
                _record(
                    additive,
                    f"{location} request {media}",
                    "request media type added",
                )
            for media in sorted(set(old_content) & set(new_content)):
                _compare_schema(
                    old_content[media].get("schema"),
                    new_content[media].get("schema"),
                    old,
                    new,
                    "request",
                    f"{location} request {media}",
                    breaking,
                    risky,
                    additive,
                )

        old_responses = old_operation.get("responses") or {}
        new_responses = new_operation.get("responses") or {}
        for status in sorted(set(old_responses) - set(new_responses), key=str):
            _record(breaking, f"{location} response {status}", "response removed")
        for status in sorted(set(new_responses) - set(old_responses), key=str):
            _record(
                risky,
                f"{location} response {status}",
                "new response status requires consumer review",
            )
        for status in sorted(set(old_responses) & set(new_responses), key=str):
            old_response = (
                old_responses[status]
                if isinstance(old_responses[status], dict)
                else {}
            )
            new_response = (
                new_responses[status]
                if isinstance(new_responses[status], dict)
                else {}
            )
            old_content = old_response.get("content") or {}
            new_content = new_response.get("content") or {}
            for media in sorted(set(old_content) - set(new_content)):
                _record(
                    breaking,
                    f"{location} response {status} {media}",
                    "response media type removed",
                )
            for media in sorted(set(new_content) - set(old_content)):
                _record(
                    additive,
                    f"{location} response {status} {media}",
                    "response media type added",
                )
            for media in sorted(set(old_content) & set(new_content)):
                _compare_schema(
                    old_content[media].get("schema"),
                    new_content[media].get("schema"),
                    old,
                    new,
                    "response",
                    f"{location} response {status} {media}",
                    breaking,
                    risky,
                    additive,
                )

    for path, method in sorted(new_ops.keys() - old_ops.keys()):
        _record(additive, f"{method} {path}", "operation added")

    return {
        "compatible": not breaking,
        "reviewRequired": bool(risky),
        "breaking": breaking,
        "risky": risky,
        "additive": additive,
    }
