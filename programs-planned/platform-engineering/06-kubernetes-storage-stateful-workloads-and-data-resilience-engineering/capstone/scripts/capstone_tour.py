#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from atlas_data.backup import BackupRepository
from atlas_data.binding import Binder, BindingError
from atlas_data.catalog import atlas_catalog
from atlas_data.csi import SemanticCSI
from atlas_data.fencing import FenceRegistry
from atlas_data.ledger import DurableLedger
from atlas_data.migration import MigrationPhase, MigrationPlan
from atlas_data.models import CapacitySegment, Claim, Node, StorageClass
from atlas_data.performance import StorageWorkload
from atlas_data.release import ReleaseEvaluator
from atlas_data.snapshots import SnapshotCoordinator
from atlas_data.stateful import StatefulSetPlanner
from atlas_data.topology import Scheduler


def main() -> int:
    checks: list[dict[str, object]] = []

    catalogue = atlas_catalog()
    checks.append({"name": "data-catalogue", "passed": len(catalogue) == 5})

    storage_class = StorageClass.atlas_default()
    claim = Claim(
        namespace="atlas-system",
        name="atlas-db-data",
        requested_gib=20,
        access_modes=("ReadWriteOncePod",),
        storage_class=storage_class.name,
    )
    binder = Binder([storage_class])
    delayed_rejected = False
    try:
        binder.bind(claim)
    except BindingError:
        delayed_rejected = True
    placement = Scheduler(
        nodes=[
            Node("node-a", "zone-a", attach_limit=4),
            Node("node-b", "zone-b", attach_limit=4),
        ],
        capacities=[
            CapacitySegment("zone-a", storage_class.name, 10),
            CapacitySegment("zone-b", storage_class.name, 100),
        ],
    ).place("atlas-db-0", [(claim.name, claim.requested_gib)])
    result = binder.bind(claim, selected_zone="zone-b")
    checks.append(
        {
            "name": "delayed-topology-binding",
            "passed": delayed_rejected
            and placement.node == "node-b"
            and result.volume.zone == "zone-b",
        }
    )

    csi = SemanticCSI("csi.atlas.example.invalid")
    volume = csi.create_volume("atlas-db-data", 20, "zone-b")
    replay = csi.create_volume("atlas-db-data", 20, "zone-b")
    csi.controller_publish(volume.id, "node-b")
    csi.node_stage(volume.id, "node-b")
    csi.node_publish(volume.id, "node-b", "/pods/atlas-db-0/data")
    csi.node_unpublish(volume.id, "/pods/atlas-db-0/data")
    csi.node_unstage(volume.id, "node-b")
    csi.controller_unpublish(volume.id, "node-b")
    checks.append(
        {
            "name": "csi-idempotent-lifecycle",
            "passed": replay.id == volume.id
            and not volume.attached_nodes
            and not volume.staged_nodes
            and not volume.published_targets,
        }
    )

    planner = StatefulSetPlanner(
        "atlas-db", "atlas-system", "atlas-db", ("data", "wal")
    )
    identity = planner.identity(0)
    checks.append(
        {
            "name": "stable-stateful-identity",
            "passed": identity.pod_name == "atlas-db-0"
            and identity.pvc_names
            == ("data-atlas-db-0", "wal-atlas-db-0"),
        }
    )

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        fence = FenceRegistry()
        old = fence.acquire("atlas-db")
        current = fence.acquire("atlas-db")
        ledger = DurableLedger(root / "ledger")
        ledger.commit(current, "sentinel", "generation-2")
        stale_rejected = False
        try:
            ledger.commit(old, "sentinel", "generation-1")
        except PermissionError:
            stale_rejected = True
        reopened = DurableLedger(root / "ledger")
        checks.append(
            {
                "name": "durable-fencing",
                "passed": stale_rejected
                and reopened.generation() == 2
                and reopened.read("sentinel") == "generation-2",
            }
        )

        source = root / "source"
        source.mkdir()
        (source / "ledger.json").write_text(
            '{"generation":2,"sentinel":"generation-2"}\n',
            encoding="utf-8",
        )
        (source / "artifact.bin").write_bytes(b"atlas-artifact")
        snapshot = SnapshotCoordinator().application_snapshot(
            "atlas-db",
            ["data", "wal"],
            lambda: "checkpoint-generation-2",
        )
        repo = BackupRepository(root / "backup")
        manifest = repo.backup_directory(source, "atlas-db", 2)
        restore = repo.restore(manifest.id, root / "restored")
        checks.append(
            {
                "name": "snapshot-and-empty-restore",
                "passed": snapshot.consistency == "application"
                and restore.verified
                and restore.generation == 2
                and restore.files == 2,
            }
        )

    workload = StorageWorkload(
        iops=1200,
        average_kib=16,
        p99_latency_ms=8.0,
        queue_depth=12,
    )
    checks.append(
        {
            "name": "performance-budget",
            "passed": workload.throughput_mib_s == 18.75
            and workload.within_budget(10.0, 16),
        }
    )

    migration = MigrationPlan(
        [
            MigrationPhase("expand", True, False, ("schema",)),
            MigrationPhase("backfill", True, False, ("counts",)),
            MigrationPhase(
                "cutover", False, True, ("old-writer-fenced", "restore")
            ),
        ]
    )
    migration.complete("expand", {"schema"})
    migration.complete("backfill", {"counts"})
    migration.complete("cutover", {"old-writer-fenced", "restore"})
    checks.append(
        {
            "name": "ordered-data-migration",
            "passed": migration.completed == ["expand", "backfill", "cutover"]
            and not migration.rollback_allowed(),
        }
    )

    evaluator = ReleaseEvaluator()
    accepted = evaluator.evaluate(
        {
            "predecessor": "pass",
            "single_writer": "pass",
            "restore_drill": "pass",
            "migration_compatibility": "pass",
        }
    )
    rejected = evaluator.evaluate(
        {
            "predecessor": "pass",
            "single_writer": "pass",
            "restore_drill": "fail",
            "migration_compatibility": "pass",
        }
    )
    checks.append(
        {
            "name": "categorical-release-gate",
            "passed": accepted.decision == "accepted"
            and rejected.decision == "rejected",
        }
    )

    passed = all(bool(item["passed"]) for item in checks)
    report = {
        "schemaVersion": "1.0",
        "capstone": "Atlas Data Plane 1.0",
        "checks": checks,
        "passed": passed,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
