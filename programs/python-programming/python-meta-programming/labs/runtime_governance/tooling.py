from __future__ import annotations

import ast
from collections.abc import Iterator
from contextlib import contextmanager
import importlib
from importlib.abc import Loader, MetaPathFinder
from importlib.machinery import ModuleSpec
import sys
from types import ModuleType


class VirtualModuleFinder(MetaPathFinder, Loader):
    """Serve one exact virtual module and record every owned import event."""

    def __init__(self, module_name: str, attributes: dict[str, object]) -> None:
        if not module_name.isidentifier():
            raise ValueError("virtual module name must be one identifier")
        self.module_name = module_name
        self.attributes = dict(attributes)
        self.events: list[str] = []

    def find_spec(
        self,
        fullname: str,
        path: object = None,
        target: ModuleType | None = None,
    ) -> ModuleSpec | None:
        if fullname != self.module_name:
            return None
        self.events.append(f"find:{fullname}")
        return ModuleSpec(fullname, self)

    def create_module(self, spec: ModuleSpec) -> ModuleType | None:
        self.events.append(f"create:{spec.name}")
        return None

    def exec_module(self, module: ModuleType) -> None:
        self.events.append(f"exec:{module.__name__}")
        module.__dict__.update(self.attributes)


@contextmanager
def installed_virtual_module(
    module_name: str,
    attributes: dict[str, object],
) -> Iterator[VirtualModuleFinder]:
    """Install one exact finder and remove both hook and module on exit."""

    if module_name in sys.modules:
        raise RuntimeError(f"module already loaded: {module_name}")
    finder = VirtualModuleFinder(module_name, attributes)
    sys.meta_path.insert(0, finder)
    try:
        yield finder
    finally:
        if finder in sys.meta_path:
            sys.meta_path.remove(finder)
        loaded = sys.modules.get(module_name)
        if loaded is not None and loaded.__loader__ is finder:
            sys.modules.pop(module_name, None)


class ConstantRewriter(ast.NodeTransformer):
    """Rewrite one exact string constant while counting owned changes."""

    def __init__(self, old: str, new: str) -> None:
        self.old = old
        self.new = new
        self.replacements = 0

    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        if node.value == self.old:
            self.replacements += 1
            return ast.copy_location(ast.Constant(self.new), node)
        return node


def rewrite_constant(source: str, old: str, new: str) -> tuple[object, int]:
    """Compile trusted internal source after one observable AST rewrite."""

    tree = ast.parse(source, mode="exec")
    rewriter = ConstantRewriter(old, new)
    transformed = rewriter.visit(tree)
    ast.fix_missing_locations(transformed)
    code = compile(transformed, "<constant-rewriter>", "exec")
    namespace: dict[str, object] = {}
    exec(code, {"__builtins__": {}}, namespace)  # noqa: S102
    return namespace.get("result"), rewriter.replacements


def tooling_evidence() -> dict[str, object]:
    """Expose hook lifetime, no-hook behavior, and transform provenance."""

    module_name = "_bijux_runtime_governance_virtual"
    with installed_virtual_module(
        module_name,
        {"status": "virtual", "owner": "VirtualModuleFinder"},
    ) as finder:
        module = importlib.import_module(module_name)
        hook_installed = finder in sys.meta_path
        module_visible = module_name in sys.modules
        status = module.status  # type: ignore[attr-defined]
        events = list(finder.events)

    no_hook_failure = ""
    try:
        importlib.import_module(module_name)
    except ModuleNotFoundError as error:
        no_hook_failure = type(error).__name__

    transformed_result, replacements = rewrite_constant(
        "result = 'draft'",
        "draft",
        "approved",
    )
    return {
        "import_hook": {
            "module_name": module_name,
            "events": events,
            "status_inside_scope": status,
            "hook_installed_inside_scope": hook_installed,
            "module_cached_inside_scope": module_visible,
            "hook_present_after_scope": finder in sys.meta_path,
            "module_cached_after_scope": module_name in sys.modules,
            "no_hook_failure": no_hook_failure,
        },
        "ast_transform": {
            "source": "result = 'draft'",
            "result": transformed_result,
            "replacement_count": replacements,
            "filename": "<constant-rewriter>",
        },
        "boundaries": {
            "application_import_hook_approved": False,
            "untrusted_source_approved": False,
            "tooling_only": True,
            "no_hook_mode_required": True,
        },
    }
