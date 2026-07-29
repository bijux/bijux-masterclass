"""Executable learning proofs for the Module 07 effect-boundary delta."""

from __future__ import annotations

import builtins
from io import StringIO

import pytest

from funcpipe_rag.core.rag_types import RawDoc
from funcpipe_rag.domain.capabilities import StorageRead
from funcpipe_rag.infra.adapters import FileStorage, InMemoryStorage
from funcpipe_rag.result.types import Ok


def test_storage_adapters_preserve_rag_read_behavior(monkeypatch: pytest.MonkeyPatch) -> None:
    """Domain behavior depends on StorageRead, not a concrete storage class."""

    docs = [
        RawDoc(doc_id="d1", title="One", abstract="Alpha", categories="fp"),
        RawDoc(doc_id="d2", title="Two", abstract="Beta", categories="python"),
    ]
    csv_file = StringIO(
        "doc_id,title,abstract,categories\n"
        "d1,One,Alpha,fp\n"
        "d2,Two,Beta,python\n"
    )
    monkeypatch.setattr(builtins, "open", lambda *args, **kwargs: csv_file)

    def read_ids(storage: StorageRead, path: str) -> list[str]:
        return [item.value.doc_id for item in storage.read_docs(path) if isinstance(item, Ok)]

    memory_ids = read_ids(InMemoryStorage(preload={"docs.csv": docs}), "docs.csv")
    file_ids = read_ids(FileStorage(), "docs.csv")

    assert memory_ids == ["d1", "d2"]
    assert file_ids == memory_ids
