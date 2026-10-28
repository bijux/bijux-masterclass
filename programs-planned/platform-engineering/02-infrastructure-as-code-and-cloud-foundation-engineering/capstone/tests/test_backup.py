from __future__ import annotations

from pathlib import Path
import shutil

import pytest

from cloud_model.backup import BackupError, create_manifest, materialize_backup, restore_backup


def make_source(root: Path) -> Path:
    source = root / "source"
    (source / "results").mkdir(parents=True)
    (source / "results" / "r1.json").write_text('{"result":"ATLAS"}\n')
    (source / "spool").mkdir()
    (source / "spool" / "completed.txt").write_text("r1\n")
    return source


def test_backup_and_empty_restore(tmp_path: Path) -> None:
    source = make_source(tmp_path)
    manifest = create_manifest(source, release="1.0", consistency_point="job-r1")
    backup = tmp_path / "backup"
    restore = tmp_path / "restore"
    materialize_backup(source, backup, manifest)
    result = restore_backup(backup, restore)
    assert result["verified"] is True
    assert (restore / "results" / "r1.json").read_text() == '{"result":"ATLAS"}\n'


def test_restore_rejects_nonempty_destination(tmp_path: Path) -> None:
    source = make_source(tmp_path)
    manifest = create_manifest(source, release="1.0", consistency_point="job-r1")
    backup = tmp_path / "backup"
    materialize_backup(source, backup, manifest)
    destination = tmp_path / "restore"
    destination.mkdir()
    (destination / "old").write_text("hidden dependency")
    with pytest.raises(BackupError, match="empty"):
        restore_backup(backup, destination)


def test_tampered_backup_rejected(tmp_path: Path) -> None:
    source = make_source(tmp_path)
    manifest = create_manifest(source, release="1.0", consistency_point="job-r1")
    backup = tmp_path / "backup"
    materialize_backup(source, backup, manifest)
    (backup / "results" / "r1.json").write_text("tampered")
    with pytest.raises(BackupError, match="mismatch"):
        restore_backup(backup, tmp_path / "restore")
