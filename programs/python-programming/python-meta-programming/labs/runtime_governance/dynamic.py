from __future__ import annotations

import ast


class DynamicExecutionRefused(ValueError):
    """Reject source outside the published arithmetic language."""


_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Constant,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.USub,
    ast.UAdd,
)


def _validate_arithmetic(tree: ast.AST) -> None:
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED_NODES):
            raise DynamicExecutionRefused(
                f"syntax is outside the arithmetic policy: {type(node).__name__}"
            )
        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool) or not isinstance(
                node.value,
                (int, float),
            ):
                raise DynamicExecutionRefused(
                    "arithmetic constants must be int or float"
                )
            if abs(node.value) > 1_000_000:
                raise DynamicExecutionRefused(
                    "arithmetic constants must not exceed 1000000"
                )


def evaluate_arithmetic(source: str) -> int | float:
    """Evaluate one bounded internal expression; this is not a sandbox."""

    if len(source) > 120:
        raise DynamicExecutionRefused("arithmetic source exceeds 120 characters")
    try:
        tree = ast.parse(source, mode="eval")
    except SyntaxError as error:
        raise DynamicExecutionRefused("arithmetic source is invalid") from error
    _validate_arithmetic(tree)
    code = compile(tree, "<arithmetic-policy>", "eval")
    result = eval(code, {"__builtins__": {}}, {})  # noqa: S307
    if isinstance(result, bool) or not isinstance(result, (int, float)):
        raise DynamicExecutionRefused("arithmetic result must be int or float")
    return result


def dynamic_execution_evidence() -> dict[str, object]:
    """Expose one narrow trusted route and one refused untrusted route."""

    refused_message = ""
    try:
        evaluate_arithmetic("__import__('os').getcwd()")
    except DynamicExecutionRefused as error:
        refused_message = str(error)

    return {
        "accepted": {
            "source": "6 * 7 + 1",
            "result": evaluate_arithmetic("6 * 7 + 1"),
            "mode": "eval",
            "filename": "<arithmetic-policy>",
            "syntax_owner": "_validate_arithmetic",
        },
        "refused": {
            "source": "__import__('os').getcwd()",
            "failure_type": DynamicExecutionRefused.__name__,
            "message": refused_message,
            "executed": False,
        },
        "trust_boundary": {
            "intended_input": "bounded internal arithmetic",
            "untrusted_input_owner": "separate process or purpose-built service",
            "empty_builtins_is_a_sandbox": False,
            "ast_validation_is_a_sandbox": False,
        },
        "claim_limits": [
            "the validator narrows accepted syntax",
            "the route is not safe for adversarial source",
            "resource isolation requires an operating-system process boundary",
        ],
    }
