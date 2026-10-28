"""Directional schema-change classification for the course release gate.

This module is deliberately small: it models the compatibility decisions used by
Course 9's release exercises. It is not presented as a complete replacement for
an independent GraphQL schema-diff tool.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SchemaChange:
    """One normalized change discovered between two schema releases."""

    kind: str
    coordinate: str
    active_operation_uses: bool = False


@dataclass(frozen=True)
class CompatibilityDecision:
    """The course policy's classification and its concise reason."""

    classification: str
    reason: str


_BREAKING_CHANGES = {
    "remove-field",
    "remove-type",
    "add-required-argument",
    "add-required-input-field",
    "remove-enum-value",
    "output-nonnull-to-nullable",
}

_REVIEW_REQUIRED_CHANGES = {
    "add-enum-value",
    "add-union-member",
    "add-interface-implementation",
    "output-nullable-to-nonnull",
    "increase-fanout",
}

_ADDITIVE_CHANGES = {
    "add-optional-field",
    "add-optional-argument",
    "deprecate-field",
}


def classify(change: SchemaChange) -> CompatibilityDecision:
    """Classify one normalized schema change under the course policy."""

    if change.kind in _BREAKING_CHANGES:
        return CompatibilityDecision("breaking", change.kind)
    if change.kind in _REVIEW_REQUIRED_CHANGES:
        return CompatibilityDecision("review-required", change.kind)
    if change.kind in _ADDITIVE_CHANGES:
        return CompatibilityDecision("additive", change.kind)
    return CompatibilityDecision("review-required", "unknown change")
