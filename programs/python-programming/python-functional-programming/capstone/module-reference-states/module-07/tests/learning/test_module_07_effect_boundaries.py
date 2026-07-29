"""Executable learning proofs for the Module 07 effect-boundary delta."""

from __future__ import annotations

import builtins
from collections.abc import Iterator
from io import StringIO

import pytest

from funcpipe_rag.core.rag_types import RawDoc
from funcpipe_rag.domain.capabilities import StorageRead
from funcpipe_rag.domain.effects import IOPlan, io_delay, io_map, perform
from funcpipe_rag.infra.adapters import FileStorage, InMemoryStorage
from funcpipe_rag.result.types import ErrInfo, Ok, Result


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


def test_io_plan_defers_rag_read_until_the_shell_performs_it() -> None:
    """Describing a storage read is pure; perform owns its execution."""

    events: list[str] = []
    storage = InMemoryStorage(
        preload={
            "docs.csv": [
                RawDoc(doc_id="d1", title="One", abstract="Alpha", categories="fp"),
                RawDoc(doc_id="d2", title="Two", abstract="Beta", categories="python"),
            ]
        }
    )

    def delayed_read() -> Result[Iterator[Result[RawDoc, ErrInfo]], ErrInfo]:
        events.append("read")
        return Ok(storage.read_docs("docs.csv"))

    plan: IOPlan[list[str]] = io_map(
        io_delay(delayed_read),
        lambda items: [item.value.doc_id for item in items if isinstance(item, Ok)],
    )

    assert events == []
    assert perform(plan) == Ok(["d1", "d2"])
    assert events == ["read"]
