from __future__ import annotations

from typing import Any


class ModuleInterfaceError(ValueError):
    pass


def validate_module_interface(module: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    name = str(module.get("name", ""))
    if not name:
        errors.append("module name is required")
    variables = module.get("variables", [])
    outputs = module.get("outputs", [])
    seen: set[str] = set()
    for variable in variables:
        var_name = str(variable.get("name", ""))
        if not var_name:
            errors.append("variable name is required")
            continue
        if var_name in seen:
            errors.append(f"duplicate variable: {var_name}")
        seen.add(var_name)
        if not variable.get("type"):
            errors.append(f"variable {var_name} must declare a type")
        if variable.get("sensitive") and variable.get("default") not in (None, ""):
            errors.append(f"secret-like variable {var_name} must not have a material default")
        if var_name.endswith("_id") and variable.get("description", "").lower().find("owner") < 0:
            errors.append(f"identifier input {var_name} must document the owner boundary")
    output_names: set[str] = set()
    for output in outputs:
        out_name = str(output.get("name", ""))
        if not out_name:
            errors.append("output name is required")
            continue
        if out_name in output_names:
            errors.append(f"duplicate output: {out_name}")
        output_names.add(out_name)
        if not output.get("description"):
            errors.append(f"output {out_name} needs a consumer-oriented description")
    if module.get("configuresProvider"):
        errors.append("reusable child modules must not own provider configuration")
    if module.get("readsRemoteState"):
        errors.append("reusable child modules must not consume broad remote state")
    return errors


def compare_module_versions(old: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    old_vars = {v["name"]: v for v in old.get("variables", [])}
    new_vars = {v["name"]: v for v in new.get("variables", [])}
    breaking: list[str] = []
    review: list[str] = []
    additive: list[str] = []
    for name in sorted(set(old_vars) - set(new_vars)):
        breaking.append(f"input removed: {name}")
    for name in sorted(set(new_vars) - set(old_vars)):
        row = new_vars[name]
        if row.get("required", False):
            breaking.append(f"new required input: {name}")
        else:
            additive.append(f"new optional input: {name}")
    for name in sorted(set(old_vars) & set(new_vars)):
        before, after = old_vars[name], new_vars[name]
        if before.get("type") != after.get("type"):
            breaking.append(f"input type changed: {name}")
        if before.get("default") != after.get("default"):
            review.append(f"input default changed: {name}")
    old_outputs = {o["name"] for o in old.get("outputs", [])}
    new_outputs = {o["name"] for o in new.get("outputs", [])}
    for name in sorted(old_outputs - new_outputs):
        breaking.append(f"output removed: {name}")
    for name in sorted(new_outputs - old_outputs):
        additive.append(f"output added: {name}")
    return {"breaking": breaking, "review": review, "additive": additive}
