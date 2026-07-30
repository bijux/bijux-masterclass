from __future__ import annotations


def inspect_runtime_governance() -> dict[str, object]:
    """Expose accepted, constrained, and rejected runtime powers without execution."""

    return {
        "scope": "incident-plugin runtime",
        "constructed": False,
        "executed": False,
        "decisions": [
            {
                "mechanism": "action decorators",
                "outcome": "approve",
                "owner": "actions.py",
                "reason": "action metadata and wrapper history belong to callable policy",
                "observability": "action, action-wrapper, bind-action, and trace reports",
                "rollback": "remove the explicit decorator and redeploy",
                "proof": "runtime and CLI action tests",
            },
            {
                "mechanism": "field descriptors",
                "outcome": "approve",
                "owner": "fields.py",
                "reason": "coercion, validation, and per-instance storage belong to attribute access",
                "observability": "field, field-ownership, and field-system reports",
                "rollback": "replace the field declaration with ordinary explicit code",
                "proof": "field and CLI tests",
            },
            {
                "mechanism": "PluginMeta",
                "outcome": "approve",
                "owner": "framework.py",
                "reason": "tracked assignment events and generated class contracts require class-creation ownership",
                "observability": "class-creation and registry reports",
                "rollback": "clear registry state and remove the class-family policy in code",
                "proof": "namespace, class-creation, and registry tests",
            },
            {
                "mechanism": "process-global plugin registry",
                "outcome": "constrain",
                "owner": "framework.py",
                "reason": "in-process lookup is sufficient, but import-time state requires reset discipline",
                "observability": "registry and manifest reports",
                "rollback": "PluginMeta.clear_registry",
                "proof": "deterministic ordering, duplicate, and reset tests",
            },
            {
                "mechanism": "runtime introspection CLI",
                "outcome": "approve",
                "owner": "cli.py and public inspection helpers",
                "reason": "reviewers need non-constructing evidence before runtime invocation",
                "observability": "JSON commands and saved bundle manifests",
                "rollback": "commands are observational and do not mutate runtime policy",
                "proof": "CLI, public API, and bundle manifest tests",
            },
        ],
        "rejected_powers": [
            {
                "power": "eval or exec for plugin configuration",
                "reason": "configuration is data and has no code-execution requirement",
                "alternative": "explicit scalar parsing and field validation",
            },
            {
                "power": "application monkey patching",
                "reason": "shared runtime replacement obscures ownership and concurrent visibility",
                "alternative": "explicit dependency or adapter replacement",
            },
            {
                "power": "application import hooks or AST rewriting",
                "reason": "the runtime does not own process-wide import or source transformation",
                "alternative": "ordinary imports and tooling outside the application process",
            },
            {
                "power": "package discovery during class creation",
                "reason": "deployment discovery and external I/O are not class-definition facts",
                "alternative": "explicit discovery and configuration boundary",
            },
            {
                "power": "automatic metaclass conflict repair",
                "reason": "combined class-creation policies require semantic integration",
                "alternative": "explicit compatible owner with focused composition tests",
            },
        ],
        "review_gate": [
            "name the pressure and smallest honest owner",
            "state timing and public-surface consequences",
            "expose behavior through a non-destructive report",
            "provide rollback or refuse the mechanism",
            "pair every claim with focused executable proof",
        ],
        "evidence_commands": [
            "manifest",
            "field-system",
            "action-wrapper",
            "class-creation",
            "registry",
            "governance",
            "inspect",
            "verify-report",
        ],
    }
