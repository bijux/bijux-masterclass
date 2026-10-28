from __future__ import annotations

import unittest
from pathlib import Path


CAP = Path(__file__).resolve().parents[1]


class HostPolicyTests(unittest.TestCase):
    def test_identity_domains_are_separate(self) -> None:
        sysusers = (CAP / "sysusers.d" / "atlas.conf").read_text()
        self.assertIn("m atlas-api atlas-spool", sysusers)
        self.assertIn("m atlas-worker atlas-spool", sysusers)
        self.assertNotIn("m atlas-edge atlas-spool", sysusers)
        self.assertIn("u atlas-backup", sysusers)

        tmpfiles = (CAP / "tmpfiles.d" / "atlas.conf").read_text()
        self.assertIn("/var/lib/atlas/spool 2770 root atlas-spool", tmpfiles)
        self.assertIn("events.jsonl 0660 root atlas-log", tmpfiles)

    def test_units_match_identity_domains(self) -> None:
        api = (CAP / "systemd" / "atlas-api.service").read_text()
        worker = (CAP / "systemd" / "atlas-worker.service").read_text()
        edge = (CAP / "systemd" / "atlas-edge.service").read_text()
        self.assertIn("SupplementaryGroups=atlas-spool atlas-runtime atlas-log", api)
        self.assertIn("SupplementaryGroups=atlas-spool atlas-runtime atlas-log", worker)
        self.assertIn("SupplementaryGroups=atlas-runtime atlas-log", edge)
        self.assertNotIn("atlas-spool", edge)
        self.assertIn("CapabilityBoundingSet=\n", edge)
        self.assertIn("AmbientCapabilities=\n", edge)

    def test_firewall_does_not_flush_unowned_rules(self) -> None:
        rules = (CAP / "nftables" / "atlas.nft").read_text()
        self.assertNotIn("flush ruleset", rules)
        self.assertIn("table inet atlas_filter", rules)

    def test_cloud_init_contains_no_key_or_unpinned_package_update(self) -> None:
        config = (CAP / "cloud-init" / "atlas.yaml").read_text()
        self.assertNotIn("ssh_authorized_keys", config)
        self.assertNotIn("package_update: true", config)
        self.assertNotIn("REPLACE_", config)


if __name__ == "__main__":
    unittest.main()
