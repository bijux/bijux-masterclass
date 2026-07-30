from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import asdict, dataclass
import inspect


@dataclass(frozen=True, slots=True)
class PatchRecord:
    """Identity and rollback evidence for one scoped attribute patch."""

    owner_type: str
    attribute: str
    had_original: bool
    original_identity: int | None
    replacement_identity: int
    rollback_owner: str = "scoped_attribute_patch"

    def manifest(self) -> dict[str, object]:
        return asdict(self)


@contextmanager
def scoped_attribute_patch(
    owner: object,
    attribute: str,
    replacement: object,
) -> Iterator[PatchRecord]:
    """Patch one named owner and restore it even when the body fails."""

    if not attribute or attribute.startswith("__"):
        raise ValueError("patch attribute must be a non-dunder name")
    sentinel = object()
    original = inspect.getattr_static(owner, attribute, sentinel)
    record = PatchRecord(
        owner_type=type(owner).__name__,
        attribute=attribute,
        had_original=original is not sentinel,
        original_identity=None if original is sentinel else id(original),
        replacement_identity=id(replacement),
    )
    setattr(owner, attribute, replacement)
    try:
        yield record
    finally:
        if original is sentinel:
            delattr(owner, attribute)
        else:
            setattr(owner, attribute, original)


def patching_evidence() -> dict[str, object]:
    """Show owner-local patch visibility and guaranteed exception rollback."""

    class Renderer:
        @staticmethod
        def render(message: str) -> str:
            return f"original:{message}"

    original = inspect.getattr_static(Renderer, "render")

    def replacement(message: str) -> str:
        return f"patched:{message}"

    record: PatchRecord | None = None
    inside_result = ""
    failure_type = ""
    try:
        with scoped_attribute_patch(Renderer, "render", replacement) as active:
            record = active
            inside_result = Renderer.render("incident")
            raise RuntimeError("exercise rollback")
    except RuntimeError as error:
        failure_type = type(error).__name__

    restored = inspect.getattr_static(Renderer, "render")
    return {
        "inside_scope": {
            "result": inside_result,
            "replacement_visible": inside_result == "patched:incident",
            "record": record.manifest() if record is not None else {},
        },
        "after_scope": {
            "result": Renderer.render("incident"),
            "original_identity_restored": restored is original,
            "body_failure_type": failure_type,
        },
        "boundary": {
            "patched_owner": "Renderer.render",
            "process_wide_patch": False,
            "automatic_audit_storage": False,
            "concurrency_safe": False,
        },
        "claim_limits": [
            "finally guarantees ordinary rollback for this owner",
            "other threads can observe the replacement while the scope is active",
            "process crashes cannot run Python cleanup",
        ],
    }
