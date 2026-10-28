from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
import io
from pathlib import Path

import pytest

from analysis_service.artifacts import FileSystemArtifactStore
from analysis_service.failures import ServiceError


def test_atomic_idempotent_publish(tmp_path: Path) -> None:
    store = FileSystemArtifactStore(tmp_path)
    first = store.stage_bytes(b"result", "text/plain")
    path = store.publish(first, "artifacts/aa/result")
    assert path.read_bytes() == b"result"

    replay = store.stage_bytes(b"result", "text/plain")
    assert store.publish(replay, "artifacts/aa/result") == path
    assert not replay.temporary_path.exists()


def test_concurrent_identical_publish_has_one_object(tmp_path: Path) -> None:
    store = FileSystemArtifactStore(tmp_path)
    staged = [store.stage_bytes(b"same bytes", "text/plain") for _ in range(16)]

    with ThreadPoolExecutor(max_workers=16) as executor:
        paths = list(
            executor.map(
                lambda item: store.publish(item, "objects/sha256/same"),
                staged,
            )
        )

    assert len(set(paths)) == 1
    assert paths[0].read_bytes() == b"same bytes"
    assert all(not item.temporary_path.exists() for item in staged)


def test_different_bytes_at_same_key_fail(tmp_path: Path) -> None:
    store = FileSystemArtifactStore(tmp_path)
    store.publish(store.stage_bytes(b"a", "text/plain"), "same")
    conflicting = store.stage_bytes(b"b", "text/plain")
    with pytest.raises(RuntimeError, match="different bytes"):
        store.publish(conflicting, "same")
    assert not conflicting.temporary_path.exists()


def test_path_traversal_rejected(tmp_path: Path) -> None:
    store = FileSystemArtifactStore(tmp_path)
    staged = store.stage_bytes(b"x", "text/plain")
    with pytest.raises(ValueError):
        store.publish(staged, "../escape")
    store.discard(staged)


def test_upload_limit_deletes_staging(tmp_path: Path) -> None:
    store = FileSystemArtifactStore(tmp_path)
    with pytest.raises(ServiceError) as failure:
        asyncio.run(
            store.stage_upload(
                io.BytesIO(b"x" * 9),
                "text/plain",
                8,
            )
        )
    assert failure.value.status == 413
    assert not list((tmp_path / ".staging").iterdir())


def test_empty_upload_is_rejected_and_cleaned(tmp_path: Path) -> None:
    store = FileSystemArtifactStore(tmp_path)
    with pytest.raises(ServiceError) as failure:
        asyncio.run(store.stage_upload(io.BytesIO(b""), "text/plain", 8))
    assert failure.value.status == 422
    assert not list((tmp_path / ".staging").iterdir())


def test_integrity_verification(tmp_path: Path) -> None:
    store = FileSystemArtifactStore(tmp_path)
    staged = store.stage_bytes(b"good", "text/plain")
    path = store.publish(staged, "k")
    path.write_bytes(b"bad")
    with pytest.raises(ServiceError) as failure:
        store.path_for("k", staged.checksum_sha256)
    assert failure.value.code == "artifact-integrity"


def test_orphan_audit(tmp_path: Path) -> None:
    store = FileSystemArtifactStore(tmp_path)
    store.publish(store.stage_bytes(b"a", "text/plain"), "kept")
    store.publish(store.stage_bytes(b"b", "text/plain"), "orphan")
    assert store.orphan_keys({"kept"}) == {"orphan"}
