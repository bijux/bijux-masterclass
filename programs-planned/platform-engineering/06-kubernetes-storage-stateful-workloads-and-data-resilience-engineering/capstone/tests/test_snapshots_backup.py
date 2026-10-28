import tempfile
import unittest
from pathlib import Path

from atlas_data.backup import BackupRepository
from atlas_data.snapshots import SnapshotCoordinator


class SnapshotTests(unittest.TestCase):
    def test_crash_snapshot_is_labelled(self):
        record = SnapshotCoordinator().crash_snapshot("db", ["data"])
        self.assertEqual(record.consistency, "crash")
        self.assertEqual(record.recovery_point, "uncoordinated")

    def test_application_group_snapshot_records_checkpoint(self):
        record = SnapshotCoordinator().application_snapshot(
            "db",
            ["wal", "data"],
            lambda: "checkpoint-10",
        )
        self.assertEqual(record.consistency, "application")
        self.assertEqual(record.volumes, ("data", "wal"))
        self.assertEqual(record.recovery_point, "checkpoint-10")

    def test_snapshot_replay_is_idempotent(self):
        coordinator = SnapshotCoordinator()
        first = coordinator.application_snapshot(
            "db", ["data"], lambda: "checkpoint-1"
        )
        second = coordinator.application_snapshot(
            "db", ["data"], lambda: "checkpoint-1"
        )
        self.assertEqual(first.id, second.id)


class BackupTests(unittest.TestCase):
    def test_backup_and_empty_restore(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            source.mkdir()
            (source / "state.json").write_text(
                '{"generation":42}\n', encoding="utf-8"
            )
            (source / "artifact.bin").write_bytes(b"atlas")
            repo = BackupRepository(root / "repo")
            manifest = repo.backup_directory(source, "atlas", 42)
            result = repo.restore(manifest.id, root / "restore")
            self.assertTrue(result.verified)
            self.assertEqual(result.generation, 42)
            self.assertEqual(result.files, 2)

    def test_restore_requires_empty_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            source.mkdir()
            (source / "x").write_text("x", encoding="utf-8")
            repo = BackupRepository(root / "repo")
            manifest = repo.backup_directory(source, "atlas", 1)
            destination = root / "restore"
            destination.mkdir()
            (destination / "old").write_text("old", encoding="utf-8")
            with self.assertRaises(ValueError):
                repo.restore(manifest.id, destination)

    def test_missing_object_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            source.mkdir()
            (source / "x").write_text("x", encoding="utf-8")
            repo = BackupRepository(root / "repo")
            manifest = repo.backup_directory(source, "atlas", 1)
            digest = manifest.files[0]["sha256"]
            (repo.objects / str(digest)).unlink()
            with self.assertRaises(FileNotFoundError):
                repo.restore(manifest.id, root / "restore")

    def test_manifest_identity_is_stable_for_content(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            source.mkdir()
            (source / "x").write_text("x", encoding="utf-8")
            repo = BackupRepository(root / "repo")
            first = repo.backup_directory(source, "atlas", 1)
            second = repo.backup_directory(source, "atlas", 1)
            self.assertEqual(first.id, second.id)
            self.assertEqual(first.created_ns, second.created_ns)

    def test_tampered_manifest_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            source.mkdir()
            (source / "x").write_text("x", encoding="utf-8")
            repo = BackupRepository(root / "repo")
            manifest = repo.backup_directory(source, "atlas", 1)
            path = repo.manifests / f"{manifest.id}.json"
            document = __import__("json").loads(path.read_text())
            document["generation"] = 99
            path.write_text(__import__("json").dumps(document))
            with self.assertRaises(ValueError):
                repo.load(manifest.id)

    def test_symlink_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            source.mkdir()
            target = root / "target"
            target.write_text("secret", encoding="utf-8")
            (source / "link").symlink_to(target)
            repo = BackupRepository(root / "repo")
            with self.assertRaises(ValueError):
                repo.backup_directory(source, "atlas", 1)


if __name__ == "__main__":
    unittest.main()
