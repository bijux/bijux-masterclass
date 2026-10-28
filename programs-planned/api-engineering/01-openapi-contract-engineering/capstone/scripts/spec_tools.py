from __future__ import annotations

import copy
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator

import yaml
from jsonschema import Draft202012Validator, FormatChecker

HTTP_METHODS = {"get", "put", "post", "delete", "options", "head", "patch", "trace"}
ROOT = Path(__file__).resolve().parents[1]
SPEC_DIR = ROOT / "spec"


class CourseValidationError(RuntimeError):
    """Raised when a deterministic course gate fails."""


@dataclass(frozen=True)
class RefTarget:
    document: Path
    fragment: str
    value: Any


def load_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CourseValidationError(f"missing YAML document: {path}") from exc
    except yaml.YAMLError as exc:
        raise CourseValidationError(f"invalid YAML in {path}: {exc}") from exc


def write_yaml(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(value, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )


def json_pointer_get(document: Any, fragment: str) -> Any:
    if fragment in {"", "#"}:
        return document
    pointer = fragment[1:] if fragment.startswith("#") else fragment
    if pointer == "":
        return document
    if not pointer.startswith("/"):
        raise CourseValidationError(f"unsupported non-JSON-Pointer fragment: {fragment}")
    current = document
    for raw in pointer[1:].split("/"):
        token = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            try:
                current = current[int(token)]
            except (ValueError, IndexError) as exc:
                raise CourseValidationError(f"invalid array pointer token {token!r}") from exc
        elif isinstance(current, dict):
            if token not in current:
                raise CourseValidationError(f"pointer token {token!r} not found")
            current = current[token]
        else:
            raise CourseValidationError(f"pointer traverses scalar at token {token!r}")
    return current


def resolve_ref(ref: str, current_file: Path) -> RefTarget:
    path_part, sep, fragment_part = ref.partition("#")
    target_file = current_file if not path_part else (current_file.parent / path_part).resolve()
    if target_file.suffix.lower() not in {".yaml", ".yml", ".json"}:
        raise CourseValidationError(f"unsupported reference target: {ref}")
    document = load_yaml(target_file)
    fragment = f"#{fragment_part}" if sep else ""
    value = json_pointer_get(document, fragment)
    return RefTarget(document=target_file, fragment=fragment, value=value)


def iter_ref_locations(node: Any, current_file: Path, trail: tuple[str, ...] = ()) -> Iterator[tuple[str, Path, tuple[str, ...]]]:
    if isinstance(node, dict):
        ref = node.get("$ref")
        if isinstance(ref, str):
            yield ref, current_file, trail
        for key, value in node.items():
            yield from iter_ref_locations(value, current_file, trail + (str(key),))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from iter_ref_locations(value, current_file, trail + (str(index),))


def validate_references(entry_file: Path) -> list[str]:
    errors: list[str] = []
    visited: set[tuple[Path, str]] = set()

    def visit(node: Any, current_file: Path, trail: tuple[str, ...]) -> None:
        if isinstance(node, dict):
            ref = node.get("$ref")
            if isinstance(ref, str):
                try:
                    target = resolve_ref(ref, current_file)
                except CourseValidationError as exc:
                    errors.append(f"{current_file}:{'/'.join(trail)}: {exc}")
                    return
                key = (target.document, target.fragment)
                if key not in visited:
                    visited.add(key)
                    visit(target.value, target.document, trail + ("$ref",))
            for key, value in node.items():
                if key != "$ref":
                    visit(value, current_file, trail + (str(key),))
        elif isinstance(node, list):
            for index, value in enumerate(node):
                visit(value, current_file, trail + (str(index),))

    visit(load_yaml(entry_file), entry_file.resolve(), ())
    return errors


def bundle_document(entry_file: Path) -> Any:
    cache: dict[tuple[Path, str], Any] = {}

    def expand(node: Any, current_file: Path, stack: tuple[tuple[Path, str], ...]) -> Any:
        if isinstance(node, dict):
            if isinstance(node.get("$ref"), str):
                ref = node["$ref"]
                if ref.startswith("#"):
                    # Internal references remain valid in the output document.
                    return {key: expand(value, current_file, stack) for key, value in node.items()}
                target = resolve_ref(ref, current_file)
                key = (target.document, target.fragment)
                if key in stack:
                    raise CourseValidationError(
                        "external reference cycle: "
                        + " -> ".join(f"{p}#{f}" for p, f in stack + (key,))
                    )
                if key not in cache:
                    cache[key] = expand(copy.deepcopy(target.value), target.document, stack + (key,))
                resolved = copy.deepcopy(cache[key])
                siblings = {
                    key_name: expand(value, current_file, stack)
                    for key_name, value in node.items()
                    if key_name != "$ref"
                }
                if siblings:
                    if not isinstance(resolved, dict):
                        raise CourseValidationError(f"$ref siblings require an object target: {ref}")
                    resolved.update(siblings)
                return resolved
            return {key: expand(value, current_file, stack) for key, value in node.items()}
        if isinstance(node, list):
            return [expand(value, current_file, stack) for value in node]
        return node

    return expand(load_yaml(entry_file), entry_file.resolve(), ())


def iter_path_operations(spec: dict[str, Any]) -> Iterator[tuple[str, str, dict[str, Any], dict[str, Any]]]:
    for path, path_item in (spec.get("paths") or {}).items():
        if not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            lower = str(method).lower()
            if lower in HTTP_METHODS and isinstance(operation, dict):
                yield path, lower.upper(), operation, path_item
        for method, operation in (path_item.get("additionalOperations") or {}).items():
            if isinstance(operation, dict):
                yield path, str(method), operation, path_item


def iter_all_operations(spec: dict[str, Any]) -> Iterator[tuple[str, str, dict[str, Any], dict[str, Any]]]:
    yield from iter_path_operations(spec)

    def callbacks(node: Any, context: str) -> Iterator[tuple[str, str, dict[str, Any], dict[str, Any]]]:
        if not isinstance(node, dict):
            return
        for callback_name, callback_map in (node.get("callbacks") or {}).items():
            if not isinstance(callback_map, dict):
                continue
            for expression, path_item in callback_map.items():
                if not isinstance(path_item, dict):
                    continue
                for method, operation in path_item.items():
                    if str(method).lower() in HTTP_METHODS and isinstance(operation, dict):
                        yield f"{context} callback:{callback_name}:{expression}", str(method).upper(), operation, path_item

    for path, method, operation, _ in iter_path_operations(spec):
        yield from callbacks(operation, f"{method} {path}")

    for webhook_name, path_item in (spec.get("webhooks") or {}).items():
        if not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            if str(method).lower() in HTTP_METHODS and isinstance(operation, dict):
                yield f"webhook:{webhook_name}", str(method).upper(), operation, path_item


def operation_ledger(spec: dict[str, Any], include_events: bool = True) -> list[dict[str, Any]]:
    iterator = iter_all_operations(spec) if include_events else iter_path_operations(spec)
    rows: list[dict[str, Any]] = []
    for path, method, operation, _ in iterator:
        rows.append(
            {
                "path": path,
                "method": method,
                "operationId": operation.get("operationId"),
                "summary": operation.get("summary"),
                "tags": operation.get("tags", []),
                "security": operation.get("security"),
            }
        )
    return sorted(rows, key=lambda row: (row["path"], row["method"]))


def _parameter_objects(path_item: dict[str, Any], operation: dict[str, Any]) -> list[dict[str, Any]]:
    objects: list[dict[str, Any]] = []
    for item in list(path_item.get("parameters") or []) + list(operation.get("parameters") or []):
        if isinstance(item, dict):
            objects.append(item)
    return objects


def validate_openapi_structure(spec: dict[str, Any], expected_version: str) -> list[str]:
    errors: list[str] = []
    if spec.get("openapi") != expected_version:
        errors.append(f"expected openapi {expected_version}, found {spec.get('openapi')!r}")
    if not isinstance(spec.get("info"), dict):
        errors.append("missing info object")
    if not isinstance(spec.get("paths"), dict) or not spec["paths"]:
        errors.append("paths must be a non-empty object")
    if expected_version.startswith("3.1") and not spec.get("jsonSchemaDialect"):
        errors.append("3.1 baseline must declare jsonSchemaDialect")
    if expected_version == "3.2.0":
        expected_dialect = "https://spec.openapis.org/oas/3.2/dialect/2025-09-17"
        if spec.get("jsonSchemaDialect") != expected_dialect:
            errors.append(
                "3.2 frontier must declare the exact OAS 3.2 dialect URI "
                f"{expected_dialect!r}"
            )

    operation_ids: dict[str, str] = {}
    for path, method, operation, path_item in iter_all_operations(spec):
        label = f"{method} {path}"
        op_id = operation.get("operationId")
        if not isinstance(op_id, str) or not op_id:
            errors.append(f"{label}: missing operationId")
        elif op_id in operation_ids:
            errors.append(f"{label}: duplicate operationId {op_id!r}; first used by {operation_ids[op_id]}")
        else:
            operation_ids[op_id] = label
        if not operation.get("summary"):
            errors.append(f"{label}: missing summary")
        if "security" not in operation:
            errors.append(f"{label}: security decision must be explicit")
        responses = operation.get("responses")
        if not isinstance(responses, dict) or not responses:
            errors.append(f"{label}: responses must be non-empty")
        else:
            if not any(str(code).startswith(("2", "3")) for code in responses):
                if path.startswith("webhook:") or "callback:" in path:
                    pass
                else:
                    errors.append(f"{label}: no success response")
        if method == "GET" and "requestBody" in operation:
            errors.append(f"{label}: GET request bodies are outside this course contract")

        if path.startswith("/") and "{" in path:
            template_names = set(re.findall(r"\{([^{}]+)\}", path))
            declared = {
                parameter.get("name")
                for parameter in _parameter_objects(path_item, operation)
                if parameter.get("in") == "path" and parameter.get("required") is True
            }
            missing = template_names - declared
            if missing:
                errors.append(f"{label}: undeclared required path parameters: {sorted(missing)}")

        for parameter in _parameter_objects(path_item, operation):
            if parameter.get("in") == "path" and parameter.get("required") is not True:
                errors.append(f"{label}: path parameter {parameter.get('name')!r} is not required")

    tags = [tag.get("name") for tag in spec.get("tags", []) if isinstance(tag, dict)]
    for row in operation_ledger(spec):
        for tag in row["tags"]:
            if tag not in tags:
                errors.append(f"{row['method']} {row['path']}: unknown tag {tag!r}")

    if expected_version == "3.2.0":
        parents = {
            tag.get("name"): tag.get("parent")
            for tag in spec.get("tags", [])
            if isinstance(tag, dict)
        }
        for name, parent in parents.items():
            if parent and parent not in parents:
                errors.append(f"tag {name!r} refers to missing parent {parent!r}")
        for name in parents:
            seen: set[str] = set()
            current = name
            while parents.get(current):
                if current in seen:
                    errors.append(f"tag parent cycle includes {current!r}")
                    break
                seen.add(current)
                current = parents[current]

    return errors


def _iter_schema_examples(schema: Any, trail: tuple[str, ...] = ()) -> Iterator[tuple[Any, dict[str, Any], tuple[str, ...]]]:
    if not isinstance(schema, dict):
        return
    examples = schema.get("examples")
    if isinstance(examples, list):
        for index, example in enumerate(examples):
            yield example, schema, trail + ("examples", str(index))
    for key, value in schema.items():
        if key not in {"examples", "example"}:
            yield from _iter_schema_examples(value, trail + (str(key),))


def _format_validation_errors(instance: Any, schema: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"{'/'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path))
    ]


def validate_examples(spec: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    for name, schema in (spec.get("components", {}).get("schemas", {}) or {}).items():
        if not isinstance(schema, dict):
            continue
        for example, owning_schema, trail in _iter_schema_examples(schema, ("components", "schemas", name)):
            example_errors = _format_validation_errors(example, owning_schema)
            errors.extend(f"{'/'.join(trail)}: {message}" for message in example_errors)

    def walk(node: Any, trail: tuple[str, ...]) -> None:
        if isinstance(node, dict):
            schema = node.get("schema")
            if isinstance(schema, dict):
                if "example" in node:
                    for message in _format_validation_errors(node["example"], schema):
                        errors.append(f"{'/'.join(trail + ('example',))}: {message}")
                examples = node.get("examples")
                if isinstance(examples, dict):
                    for name, example_object in examples.items():
                        if isinstance(example_object, dict):
                            if "value" in example_object:
                                candidate = example_object["value"]
                            elif "dataValue" in example_object:
                                candidate = example_object["dataValue"]
                            else:
                                continue
                            for message in _format_validation_errors(candidate, schema):
                                errors.append(f"{'/'.join(trail + ('examples', str(name)))}: {message}")
            for key, value in node.items():
                walk(value, trail + (str(key),))
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, trail + (str(index),))

    walk(spec, ())
    return errors


def validate_fixture_manifest(bundle: dict[str, Any], manifest_path: Path) -> tuple[int, list[str]]:
    manifest = load_yaml(manifest_path)
    schemas = bundle.get("components", {}).get("schemas", {})
    errors: list[str] = []
    count = 0
    for case in manifest.get("cases", []):
        count += 1
        case_id = case.get("id", f"case-{count}")
        schema_name = case.get("schema")
        expected = case.get("valid")
        file_path = (manifest_path.parent / case["file"]).resolve()
        if schema_name not in schemas:
            errors.append(f"{case_id}: unknown schema {schema_name!r}")
            continue
        try:
            instance = json.loads(file_path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{case_id}: cannot read JSON fixture {file_path}: {exc}")
            continue
        actual_errors = _format_validation_errors(instance, schemas[schema_name])
        actual_valid = not actual_errors
        if actual_valid != bool(expected):
            detail = "valid" if actual_valid else "; ".join(actual_errors[:3])
            errors.append(
                f"{case_id}: expected valid={expected}, validator observed {detail}"
            )
    return count, errors


def deep_merge(target: Any, update: Any) -> Any:
    if isinstance(target, dict) and isinstance(update, dict):
        result = copy.deepcopy(target)
        for key, value in update.items():
            result[key] = deep_merge(result[key], value) if key in result else copy.deepcopy(value)
        return result
    if isinstance(target, list):
        if isinstance(update, list):
            return copy.deepcopy(target) + copy.deepcopy(update)
        return copy.deepcopy(target) + [copy.deepcopy(update)]
    return copy.deepcopy(update)


_PATH_EXACT = re.compile(r"^\$\.paths\['(?P<path>[^']+)'\](?:\.(?P<field>[A-Za-z0-9_-]+))?$")
_TAG_FILTER = re.compile(r"^\$\.tags\[\?@\.name\s*==\s*'(?P<name>[^']+)'\]$")


def _select_overlay_nodes(document: dict[str, Any], expression: str) -> list[tuple[Any, Any]]:
    if expression == "$.info":
        return [(document, "info")]
    match = _PATH_EXACT.match(expression)
    if match:
        path = match.group("path")
        field = match.group("field")
        if path not in document.get("paths", {}):
            return []
        if field is None:
            return [(document["paths"], path)]
        if field not in document["paths"][path]:
            return []
        return [(document["paths"][path], field)]
    match = _TAG_FILTER.match(expression)
    if match:
        name = match.group("name")
        return [
            (document["tags"], index)
            for index, tag in enumerate(document.get("tags", []))
            if isinstance(tag, dict) and tag.get("name") == name
        ]
    raise CourseValidationError(f"local overlay engine does not support JSONPath: {expression}")


def apply_overlay(document: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(document)
    if overlay.get("overlay") != "1.1.0":
        raise CourseValidationError("expected Overlay 1.1.0")
    actions = overlay.get("actions")
    if not isinstance(actions, list) or not actions:
        raise CourseValidationError("overlay actions must be a non-empty list")
    for index, action in enumerate(actions):
        modifiers = [name for name in ("update", "remove", "copy") if name in action]
        if len(modifiers) != 1:
            raise CourseValidationError(f"overlay action {index} must have exactly one modifier")
        selected = _select_overlay_nodes(result, action.get("target", ""))
        if action.get("remove") is True:
            # Remove list indices in descending order to preserve identity.
            for parent, key in sorted(
                selected,
                key=lambda item: item[1] if isinstance(item[1], int) else -1,
                reverse=True,
            ):
                if isinstance(parent, list):
                    parent.pop(key)
                else:
                    parent.pop(key, None)
        elif "update" in action:
            for parent, key in selected:
                parent[key] = deep_merge(parent[key], action["update"])
        else:
            raise CourseValidationError("the training overlay engine intentionally omits copy")
    return result


def validate_overlay(overlay: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if overlay.get("overlay") != "1.1.0":
        errors.append("overlay version must be 1.1.0")
    info = overlay.get("info")
    if not isinstance(info, dict) or not info.get("title") or not info.get("version"):
        errors.append("overlay info requires title and version")
    actions = overlay.get("actions")
    if not isinstance(actions, list) or not actions:
        errors.append("overlay requires at least one action")
        return errors
    for index, action in enumerate(actions):
        if not isinstance(action, dict) or not action.get("target"):
            errors.append(f"action {index}: target is required")
            continue
        modifiers = [name for name in ("update", "remove", "copy") if name in action]
        if len(modifiers) != 1:
            errors.append(f"action {index}: expected exactly one update/remove/copy modifier")
    return errors


def validate_arazzo(workflow: dict[str, Any], openapi_spec: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if workflow.get("arazzo") != "1.1.0":
        errors.append("arazzo version must be 1.1.0")
    if not workflow.get("info", {}).get("title") or not workflow.get("info", {}).get("version"):
        errors.append("arazzo info requires title and version")
    sources = workflow.get("sourceDescriptions")
    if not isinstance(sources, list) or not sources:
        errors.append("at least one sourceDescription is required")
    known_operations = {
        row["operationId"] for row in operation_ledger(openapi_spec) if row["operationId"]
    }
    workflow_ids: set[str] = set()
    for wf in workflow.get("workflows", []):
        wf_id = wf.get("workflowId")
        if not wf_id:
            errors.append("workflow without workflowId")
            continue
        if wf_id in workflow_ids:
            errors.append(f"duplicate workflowId {wf_id!r}")
        workflow_ids.add(wf_id)
        steps = wf.get("steps")
        if not isinstance(steps, list) or not steps:
            errors.append(f"workflow {wf_id!r} has no steps")
            continue
        step_ids: list[str] = []
        for index, step in enumerate(steps):
            step_id = step.get("stepId")
            if not step_id:
                errors.append(f"workflow {wf_id!r} step {index} lacks stepId")
                continue
            if step_id in step_ids:
                errors.append(f"workflow {wf_id!r} duplicates stepId {step_id!r}")
            refs = [step.get("operationId"), step.get("operationPath"), step.get("workflowId")]
            if sum(value is not None for value in refs) != 1:
                errors.append(f"step {step_id!r} must select exactly one operation/workflow")
            operation_id = step.get("operationId")
            if operation_id and operation_id not in known_operations:
                # With multiple descriptions this may be a runtime expression. This course has one.
                errors.append(f"step {step_id!r} references unknown operationId {operation_id!r}")
            serialized = json.dumps(step)
            for referenced_step in re.findall(r"\$steps\.([A-Za-z0-9_-]+)\.", serialized):
                if referenced_step not in step_ids:
                    errors.append(
                        f"step {step_id!r} forward-references or misses step {referenced_step!r}"
                    )
            step_ids.append(step_id)
    return errors


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
            k: copy.deepcopy(v) for k, v in schema.items() if k != "allOf"
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


def _record(
    bucket: list[dict[str, str]],
    location: str,
    reason: str,
) -> None:
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
                _record(breaking, location, f"request types no longer accepted: {sorted(removed)}")
            if new_types - old_types:
                _record(additive, location, f"request types added: {sorted(new_types-old_types)}")
        else:
            if new_types - old_types:
                _record(breaking, location, f"response may emit new types: {sorted(new_types-old_types)}")
            if old_types - new_types:
                _record(risky, location, f"response types narrowed: {sorted(old_types-new_types)}")

    old_enum = old.get("enum")
    new_enum = new.get("enum")
    if isinstance(old_enum, list) and isinstance(new_enum, list):
        old_values = {json.dumps(v, sort_keys=True) for v in old_enum}
        new_values = {json.dumps(v, sort_keys=True) for v in new_enum}
        if direction == "request":
            if old_values - new_values:
                _record(breaking, location, "request enum narrowed")
            if new_values - old_values:
                _record(additive, location, "request enum widened")
        else:
            if new_values - old_values:
                _record(risky, location, "response enum widened; exhaustive consumers require review")
            if old_values - new_values:
                _record(risky, location, "response enum narrowed; behavior changed")

    # Constraint direction follows the admitted-instance set. Requests may not
    # become narrower; responses may not become wider without consumer review.
    lower_keys = ("minimum", "exclusiveMinimum", "minLength", "minItems", "minProperties")
    upper_keys = ("maximum", "exclusiveMaximum", "maxLength", "maxItems", "maxProperties")
    for key in lower_keys:
        ov, nv = old.get(key), new.get(key)
        if isinstance(ov, (int, float)) and isinstance(nv, (int, float)) and ov != nv:
            if direction == "request" and nv > ov:
                _record(breaking, location, f"request {key} increased from {ov} to {nv}")
            elif direction == "response" and nv < ov:
                _record(risky, location, f"response {key} decreased from {ov} to {nv}")
            else:
                _record(additive, location, f"{key} changed from {ov} to {nv}")
    for key in upper_keys:
        ov, nv = old.get(key), new.get(key)
        if isinstance(ov, (int, float)) and isinstance(nv, (int, float)) and ov != nv:
            if direction == "request" and nv < ov:
                _record(breaking, location, f"request {key} decreased from {ov} to {nv}")
            elif direction == "response" and nv > ov:
                _record(risky, location, f"response {key} increased from {ov} to {nv}")
            else:
                _record(additive, location, f"{key} changed from {ov} to {nv}")

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
                _record(breaking, f"{location}.{prop}", "previous request property is no longer accepted")
            else:
                _record(risky, f"{location}.{prop}", "documented request property removed")
        for prop in sorted(new_props.keys() - old_props.keys()):
            if prop in new_required:
                _record(breaking, f"{location}.{prop}", "new request property is required")
            else:
                _record(additive, f"{location}.{prop}", "optional request property added")
    else:
        for prop in sorted(old_required - new_required):
            _record(breaking, f"{location}.{prop}", "required response property removed or made optional")
        for prop in sorted(old_props.keys() - new_props.keys()):
            _record(breaking, f"{location}.{prop}", "response property removed")
        for prop in sorted(new_props.keys() - old_props.keys()):
            _record(risky, f"{location}.{prop}", "response property added; strict closed-schema consumers require review")

    for prop in sorted(old_props.keys() & new_props.keys()):
        _compare_schema(
            old_props[prop], new_props[prop], old_root, new_root, direction,
            f"{location}.{prop}", breaking, risky, additive,
        )

    old_items, new_items = old.get("items"), new.get("items")
    if isinstance(old_items, dict) and isinstance(new_items, dict):
        _compare_schema(
            old_items, new_items, old_root, new_root, direction,
            f"{location}[]", breaking, risky, additive,
        )

    old_additional = old.get("additionalProperties", True)
    new_additional = new.get("additionalProperties", True)
    if direction == "request" and old_additional is not False and new_additional is False:
        _record(breaking, location, "request object became closed")
    if direction == "response" and old_additional is False and new_additional is not False:
        _record(risky, location, "response object became open")

    for keyword in ("oneOf", "anyOf", "not", "if", "then", "else", "dependentSchemas"):
        if old.get(keyword) != new.get(keyword) and (keyword in old or keyword in new):
            target = breaking if direction == "request" else risky
            _record(target, location, f"{keyword} composition changed")


def _parameters(path_item: dict[str, Any], operation: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    result: dict[tuple[str, str], dict[str, Any]] = {}
    for item in list(path_item.get("parameters") or []) + list(operation.get("parameters") or []):
        if isinstance(item, dict) and isinstance(item.get("name"), str) and isinstance(item.get("in"), str):
            result[(item["in"], item["name"])] = item
    return result


def compare_contracts(old: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    """Classify provider changes using request/response direction.

    This is a deliberately conservative course gate, not a claim that static
    analysis can prove every consumer compatible. `risky` changes require an
    explicit review decision even when they are not blocked automatically.
    """
    breaking: list[dict[str, str]] = []
    risky: list[dict[str, str]] = []
    additive: list[dict[str, str]] = []

    old_ops = {(p, m): (op, item) for p, m, op, item in iter_path_operations(old)}
    new_ops = {(p, m): (op, item) for p, m, op, item in iter_path_operations(new)}

    for key, (old_op, old_item) in old_ops.items():
        path, method = key
        location = f"{method} {path}"
        if key not in new_ops:
            _record(breaking, location, "operation removed")
            continue
        new_op, new_item = new_ops[key]
        if old_op.get("operationId") != new_op.get("operationId"):
            _record(breaking, location, "operationId changed")
        if old_op.get("security") != new_op.get("security"):
            _record(breaking, location, "security requirements changed")

        old_params = _parameters(old_item, old_op)
        new_params = _parameters(new_item, new_op)
        for pkey, old_parameter in old_params.items():
            ploc = f"{location} parameter {pkey[0]}:{pkey[1]}"
            if pkey not in new_params:
                _record(breaking, ploc, "parameter removed")
                continue
            new_parameter = new_params[pkey]
            if not old_parameter.get("required") and new_parameter.get("required"):
                _record(breaking, ploc, "parameter became required")
            _compare_schema(
                old_parameter.get("schema"), new_parameter.get("schema"),
                old, new, "request", ploc, breaking, risky, additive,
            )
        for pkey, new_parameter in new_params.items():
            if pkey not in old_params:
                target = breaking if new_parameter.get("required") else additive
                _record(target, f"{location} parameter {pkey[0]}:{pkey[1]}", "parameter added")

        old_body = old_op.get("requestBody") if isinstance(old_op.get("requestBody"), dict) else None
        new_body = new_op.get("requestBody") if isinstance(new_op.get("requestBody"), dict) else None
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
                _record(breaking, f"{location} request {media}", "request media type removed")
            for media in sorted(set(new_content) - set(old_content)):
                _record(additive, f"{location} request {media}", "request media type added")
            for media in sorted(set(old_content) & set(new_content)):
                _compare_schema(
                    old_content[media].get("schema"), new_content[media].get("schema"),
                    old, new, "request", f"{location} request {media}",
                    breaking, risky, additive,
                )

        old_responses = old_op.get("responses") or {}
        new_responses = new_op.get("responses") or {}
        for status in sorted(set(old_responses) - set(new_responses), key=str):
            _record(breaking, f"{location} response {status}", "response removed")
        for status in sorted(set(new_responses) - set(old_responses), key=str):
            _record(risky, f"{location} response {status}", "new response status requires consumer review")
        for status in sorted(set(old_responses) & set(new_responses), key=str):
            old_response = old_responses[status] if isinstance(old_responses[status], dict) else {}
            new_response = new_responses[status] if isinstance(new_responses[status], dict) else {}
            old_content = old_response.get("content") or {}
            new_content = new_response.get("content") or {}
            for media in sorted(set(old_content) - set(new_content)):
                _record(breaking, f"{location} response {status} {media}", "response media type removed")
            for media in sorted(set(new_content) - set(old_content)):
                _record(additive, f"{location} response {status} {media}", "response media type added")
            for media in sorted(set(old_content) & set(new_content)):
                _compare_schema(
                    old_content[media].get("schema"), new_content[media].get("schema"),
                    old, new, "response", f"{location} response {status} {media}",
                    breaking, risky, additive,
                )

    for path, method in sorted(new_ops.keys() - old_ops.keys()):
        _record(additive, f"{method} {path}", "operation added")

    return {
        "compatible": not breaking,
        "reviewRequired": bool(risky),
        "breaking": breaking,
        "risky": risky,
        "additive": additive,
        # Backward-compatible key retained for existing course reports.
        "nonBreaking": additive + risky,
    }


def ensure_no_errors(label: str, errors: Iterable[str]) -> None:
    materialized = list(errors)
    if materialized:
        detail = "\n".join(f"- {message}" for message in materialized)
        raise CourseValidationError(f"{label} failed:\n{detail}")
