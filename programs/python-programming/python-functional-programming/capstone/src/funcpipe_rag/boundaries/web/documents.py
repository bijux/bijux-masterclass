"""Pure document payload translation for Module 09 web boundaries."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import cast

from funcpipe_rag.core.rag_types import RawDoc
from funcpipe_rag.result.types import Err, ErrInfo, Ok, Result


def parse_document_payloads(
    payloads: Iterable[Mapping[str, object]],
) -> Result[tuple[RawDoc, ...], ErrInfo]:
    """Translate HTTP-shaped mappings without importing a web framework."""

    documents: list[RawDoc] = []
    for index, payload in enumerate(payloads):
        required = ("doc_id", "title", "abstract")
        invalid = [name for name in required if not isinstance(payload.get(name), str)]
        categories = payload.get("categories", "")
        if invalid or not isinstance(categories, str):
            fields = invalid + ([] if isinstance(categories, str) else ["categories"])
            return Err(
                ErrInfo(
                    code="INVALID_DOCUMENT",
                    msg=f"document {index} requires string fields: {', '.join(fields)}",
                    stage="web.parse_document_payloads",
                )
            )
        documents.append(
            RawDoc(
                doc_id=cast(str, payload["doc_id"]),
                title=cast(str, payload["title"]),
                abstract=cast(str, payload["abstract"]),
                categories=categories,
            )
        )
    return Ok(tuple(documents))


__all__ = ["parse_document_payloads"]
