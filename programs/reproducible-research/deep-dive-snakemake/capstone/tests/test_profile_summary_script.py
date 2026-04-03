from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_profile_summary_script_compares_shared_and_different_settings(tmp_path: Path) -> None:
    local = tmp_path / "local.yaml"
    ci = tmp_path / "ci.yaml"
    slurm = tmp_path / "slurm.yaml"

    local.write_text(
        "# local\nrerun-incomplete: true\nprintshellcmds: true\nlatency-wait: 30\n",
        encoding="utf-8",
    )
    ci.write_text(
        "# ci\nrerun-incomplete: true\nprintshellcmds: true\nlatency-wait: 30\n",
        encoding="utf-8",
    )
    slurm.write_text(
        "# slurm\nprintshellcmds: true\nlatency-wait: 60\njobs: 200\n",
        encoding="utf-8",
    )

    output = tmp_path / "profile-summary.json"
    script = Path(__file__).resolve().parents[1] / "scripts" / "profile_summary.py"
    subprocess.run(
        [
            sys.executable,
            str(script),
            "--local",
            str(local),
            "--ci",
            str(ci),
            "--slurm",
            str(slurm),
            "--out",
            str(output),
        ],
        check=True,
    )

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["shared_settings"] == {"printshellcmds": True}
    assert payload["differing_settings"]["latency-wait"] == {
        "ci": 30,
        "local": 30,
        "slurm": 60,
    }
    assert payload["differing_settings"]["rerun-incomplete"] == {
        "ci": True,
        "local": True,
        "slurm": None,
    }
    assert payload["profile_only_settings"] == {
        "jobs": ["slurm"],
        "rerun-incomplete": ["ci", "local"],
    }
