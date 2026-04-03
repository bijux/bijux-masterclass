# workflow/scripts/provenance.py

import datetime
import importlib
import json
import platform
import subprocess
import sys
from pathlib import Path


def _utc_now_iso() -> str:
    # Avoid utcnow() deprecation; produce ISO-8601 UTC with "Z"
    return datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z")


def resolve_snakemake_version(python_executable: str) -> str:
    try:
        module = importlib.import_module("snakemake")
        version = getattr(module, "__version__", "")
        if version:
            return str(version)
    except Exception:
        pass

    try:
        return subprocess.check_output(
            [python_executable, "-c", "import snakemake; print(snakemake.__version__)"],
            text=True,
        ).strip()
    except Exception:
        return "unknown"


def main() -> None:
    # `snakemake` is an injected object (NOT the snakemake Python module).
    sm = snakemake  # type: ignore[name-defined]  # noqa: F821

    sm_version = resolve_snakemake_version(sys.executable)

    try:
        git_commit = (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                cwd=str(sm.workflow.basedir),  # type: ignore[attr-defined]
            )
            .decode()
            .strip()
        )
    except Exception:
        git_commit = "unknown"

    payload = {
        "schema_version": 2,
        "timestamp_utc": _utc_now_iso(),
        "python_version": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "snakemake_version": sm_version,
        "git_commit": git_commit,
        "config": sm.config,
    }

    out = Path(sm.output.json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
