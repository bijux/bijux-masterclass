from __future__ import annotations

import inspect
import json
from collections.abc import Mapping
from pathlib import Path
from types import FrameType


def dispatch_incident(
    incident_id: str,
    /,
    severity: str = "warning",
    *,
    retries: int = 0,
    **metadata: str,
) -> str:
    return f"{incident_id}:{severity}:retries={retries}:metadata={len(metadata)}"


class MemberEvidenceTarget:
    def __init__(self) -> None:
        self.property_reads = 0

    @property
    def risk_score(self) -> int:
        self.property_reads += 1
        return 7


def signature_evidence() -> dict[str, object]:
    """Describe call shape separately from semantic behavior."""

    signature = inspect.signature(dispatch_incident)
    return {
        "signature": str(signature),
        "parameter_kinds": {
            name: parameter.kind.name.lower()
            for name, parameter in signature.parameters.items()
        },
        "annotation_names": sorted(dispatch_incident.__annotations__),
        "return_annotation": str(signature.return_annotation),
        "evidence_strength": "strong-call-shape",
    }


def binding_evidence() -> dict[str, object]:
    """Use Python's binding rules instead of manually matching arguments."""

    signature = inspect.signature(dispatch_incident)
    bound = signature.bind(
        "INC-42",
        retries=2,
        owner="platform",
    )
    bound.apply_defaults()

    try:
        signature.bind(incident_id="INC-42")
    except TypeError:
        keyword_for_positional_only_rejected = True
    else:
        keyword_for_positional_only_rejected = False

    partial = signature.bind_partial(retries=3)
    return {
        "bound_arguments": dict(bound.arguments),
        "keyword_for_positional_only_rejected": keyword_for_positional_only_rejected,
        "partial_arguments": dict(partial.arguments),
        "evidence_strength": "strong-call-matching",
    }


def provenance_evidence() -> dict[str, object]:
    """Compare normal file-backed provenance with deterministic generated-code failure."""

    module = inspect.getmodule(dispatch_incident)
    file_path = inspect.getfile(dispatch_incident)
    try:
        inspect.getsource(dispatch_incident)
    except (OSError, TypeError):
        file_backed_source_available = False
    else:
        file_backed_source_available = True

    namespace: dict[str, object] = {}
    generated_code = compile(
        "def generated_handler():\n    return 'generated'\n",
        "<generated-runtime-evidence>",
        "exec",
    )
    exec(generated_code, namespace)
    generated_handler = namespace["generated_handler"]

    try:
        inspect.getsource(generated_handler)
    except (OSError, TypeError):
        generated_source_available = False
    else:
        generated_source_available = True

    return {
        "module": None if module is None else module.__name__,
        "file_name": Path(file_path).name,
        "file_backed_source_available": file_backed_source_available,
        "generated_file_label": inspect.getfile(generated_handler),
        "generated_source_available": generated_source_available,
        "evidence_strength": "best-effort-provenance",
    }


def member_evidence() -> dict[str, object]:
    """Contrast resolved member enumeration with raw attached structure."""

    dynamic_target = MemberEvidenceTarget()
    dynamic_members = dict(inspect.getmembers(dynamic_target))
    dynamic_reads = dynamic_target.property_reads

    static_target = MemberEvidenceTarget()
    raw_property = inspect.getattr_static(static_target, "risk_score")
    static_reads = static_target.property_reads
    return {
        "dynamic_value": dynamic_members["risk_score"],
        "property_reads_after_getmembers": dynamic_reads,
        "static_value_is_property": isinstance(raw_property, property),
        "property_reads_after_static_lookup": static_reads,
        "evidence_strength": "structural-before-dynamic",
    }


def caller_names(limit: int) -> tuple[str, ...]:
    """Snapshot a bounded caller-name diagnostic without retaining frame objects."""

    if limit < 1:
        raise ValueError("limit must be at least 1")

    frame: FrameType | None = inspect.currentframe()
    if frame is None:
        return ()
    try:
        names = []
        current = frame.f_back
        while current is not None and len(names) < limit:
            names.append(current.f_code.co_name)
            current = current.f_back
        return tuple(names)
    finally:
        del frame


def frame_evidence() -> dict[str, object]:
    """Collect a minimal diagnostic snapshot and label its trust boundary."""

    return {
        "caller_names": list(caller_names(2)),
        "bounded_to": 2,
        "retains_frame_objects": False,
        "evidence_strength": "diagnostic-only",
    }


def build_evidence() -> Mapping[str, dict[str, object]]:
    """Build the five evidence packets taught in Module 03."""

    return {
        "signature": signature_evidence(),
        "binding": binding_evidence(),
        "provenance": provenance_evidence(),
        "members": member_evidence(),
        "frames": frame_evidence(),
    }


def render_evidence() -> str:
    """Render stable JSON for inspection, comparison, and review."""

    return json.dumps(build_evidence(), indent=2, sort_keys=True)
