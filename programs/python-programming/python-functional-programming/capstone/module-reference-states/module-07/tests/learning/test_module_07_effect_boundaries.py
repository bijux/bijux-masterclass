"""Executable learning proofs for the Module 07 effect-boundary delta."""

from __future__ import annotations

import builtins
from collections.abc import Iterator
from datetime import datetime, timezone
from io import StringIO

import pytest

from funcpipe_rag.core.rag_types import RawDoc
from funcpipe_rag.domain.capabilities import Clock, Logger, StorageRead
from funcpipe_rag.domain.composition import logged_read
from funcpipe_rag.domain.effects import IOPlan, io_delay, io_map, perform
from funcpipe_rag.domain.logging import LogEntry, trace_stage, trace_value
from funcpipe_rag.fp.effects.writer import pure as writer_pure
from funcpipe_rag.fp.effects.writer import run_writer
from funcpipe_rag.infra.adapters import (
    CollectingLogger,
    FileStorage,
    InMemoryStorage,
    MonotonicTestClock,
)
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


def test_read_capability_grants_no_write_authority() -> None:
    """A structural adapter can satisfy only the narrow capability it needs."""

    class ReadOnlyDocs:
        def read_docs(self, path: str) -> Iterator[Result[RawDoc, ErrInfo]]:
            yield Ok(RawDoc(doc_id=path, title="Read only", abstract="", categories="fp"))

    reader: StorageRead = ReadOnlyDocs()

    results = list(reader.read_docs("d1"))

    assert results == [Ok(RawDoc(doc_id="d1", title="Read only", abstract="", categories="fp"))]
    assert not hasattr(reader, "write_chunks")


def test_partial_storage_read_closes_the_owned_file(monkeypatch: pytest.MonkeyPatch) -> None:
    """A consumer that stops early must close the resource-owning iterator."""

    events: list[str] = []
    csv_file = StringIO(
        "doc_id,title,abstract,categories\n"
        "d1,One,Alpha,fp\n"
        "d2,Two,Beta,python\n"
    )

    def open_csv(*args: object, **kwargs: object) -> StringIO:
        events.append("open")
        return csv_file

    monkeypatch.setattr(builtins, "open", open_csv)
    iterator = FileStorage().read_docs("docs.csv")

    assert events == []
    assert next(iterator) == Ok(RawDoc(doc_id="d1", title="One", abstract="Alpha", categories="fp"))
    assert events == ["open"]
    assert not csv_file.closed

    iterator.close()

    assert csv_file.closed


def test_structured_logs_remain_data_until_the_shell_emits_them() -> None:
    """Writer records an inspectable trace before a Logger performs output."""

    program = trace_stage("read docs").and_then(
        lambda _: trace_value("doc_count", 2).and_then(
            lambda _: writer_pure(["d1", "d2"])
        )
    )
    doc_ids, entries = run_writer(program)
    logger = CollectingLogger()

    assert doc_ids == ["d1", "d2"]
    assert entries == (
        LogEntry(level="INFO", msg="read docs"),
        LogEntry(level="DEBUG", msg="doc_count=2"),
    )
    assert logger.entries == []

    for entry in entries:
        logger.log(entry)

    assert logger.entries == list(entries)


def test_clock_and_logger_capabilities_make_time_explicit() -> None:
    """Injected capabilities turn time-dependent logging into a stable trace."""

    clock = MonotonicTestClock(datetime(2025, 1, 1, tzinfo=timezone.utc))
    logger = CollectingLogger()

    def record_ingest(doc_id: str, *, clock: Clock, logger: Logger) -> None:
        logger.log(LogEntry(level="INFO", msg=f"ingest {doc_id} at {clock.now().isoformat()}"))

    record_ingest("d1", clock=clock, logger=logger)
    record_ingest("d2", clock=clock, logger=logger)

    assert logger.entries == [
        LogEntry(level="INFO", msg="ingest d1 at 2025-01-01T00:00:00.000001+00:00"),
        LogEntry(level="INFO", msg="ingest d2 at 2025-01-01T00:00:00.000002+00:00"),
    ]


def test_logged_read_composes_capabilities_without_eager_effects() -> None:
    """The helper delays both storage access and its observational log."""

    doc = RawDoc(doc_id="d1", title="One", abstract="Alpha", categories="fp")
    storage = InMemoryStorage(preload={"docs.csv": [doc]})
    logger = CollectingLogger()
    read = logged_read(storage, logger)

    plan = read("docs.csv")

    assert logger.entries == []

    result = perform(plan)

    assert isinstance(result, Ok)
    assert list(result.value) == [Ok(doc)]
    assert logger.entries == [LogEntry(level="INFO", msg="read_docs path=docs.csv")]
