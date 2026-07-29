from __future__ import annotations

from funcpipe_rag.review.migration import ContractShape, assess_migration


def shape(
    fields: set[str],
    required: set[str],
    *,
    name: str = "chunk-metadata",
) -> ContractShape:
    return ContractShape(name, frozenset(fields), frozenset(required))


def test_optional_field_addition_is_structurally_backward_compatible() -> None:
    previous = shape({"source", "tags"}, {"source", "tags"})
    current = shape(
        {"source", "tags", "embedding_model"},
        {"source", "tags"},
    )

    assessment = assess_migration(previous, current)

    assert assessment.compatibility == "backward-compatible"
    assert assessment.added_fields == ("embedding_model",)


def test_new_required_field_requires_migration() -> None:
    previous = shape({"source"}, {"source"})
    current = shape({"source", "tags"}, {"source", "tags"})

    assessment = assess_migration(previous, current)

    assert assessment.compatibility == "requires-migration"
    assert assessment.newly_required_fields == ("tags",)


def test_removed_field_is_incompatible() -> None:
    previous = shape({"source", "tags"}, {"source"})
    current = shape({"source"}, {"source"})

    assessment = assess_migration(previous, current)

    assert assessment.compatibility == "incompatible"
    assert assessment.removed_fields == ("tags",)
