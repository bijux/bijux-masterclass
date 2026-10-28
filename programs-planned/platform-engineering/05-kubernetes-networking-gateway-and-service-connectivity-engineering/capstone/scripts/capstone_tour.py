from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = [
    "packet_path_lab.py",
    "cni_lifecycle_lab.py",
    "service_convergence_lab.py",
    "dns_cache_lab.py",
    "network_policy_lab.py",
    "locality_failure_lab.py",
    "gateway_attachment_lab.py",
    "tls_gateway_lab.py",
    "egress_policy_lab.py",
    "final_game_day.py",
]


def main() -> None:
    environment = {**os.environ, "PYTHONPATH": str(ROOT)}
    for experiment in EXPERIMENTS:
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / experiment)],
            cwd=ROOT / "scripts",
            env=environment,
            check=True,
        )
    print(f"PASS Atlas Connectivity Plane tour — {len(EXPERIMENTS)} experiments")


if __name__ == "__main__":
    main()
