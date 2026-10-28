#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

CAPSTONE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAPSTONE))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from atlas_container.handoff import write_handoff
from run_capstone_tour import run_tour


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main() -> int:
    report = run_tour()
    write_json(CAPSTONE / "reports" / "capstone-tour.json", report)

    release = dict(report["release"])
    release["decision"] = "accepted-for-course-4-handoff"
    release["decisionScope"] = (
        "Dependency-light release-mechanism evidence. Native builders, target "
        "runtimes, production registry controls, operated identity, and capacity "
        "remain separate environment-backed proofs."
    )
    release["evidence"] = report["evidence"]
    write_json(CAPSTONE / "releases" / "accepted" / "release.json", release)

    image_evidence = report["evidence"]["images"]
    attachments = {
        "images": {
            item["name"]: {
                "subjectDigest": item["digest"],
                "sbom": image_evidence[item["name"]]["sbom"],
                "provenanceEnvelope": image_evidence[item["name"]][
                    "provenanceEnvelope"
                ],
                "policyDecision": image_evidence[item["name"]]["policyDecision"],
                "referrerCount": 2,
            }
            for item in release["images"]
        },
        "signer": report["evidence"]["signer"],
        "verificationPolicy": report["evidence"]["policy"],
        "trustBoundary": "fixture key; not a production trust root",
        "unexecuted": [
            "independent native BuildKit or equivalent build",
            "native arm64 execution where target hardware is unavailable",
            "production OCI runtime and seccomp/LSM enforcement",
            "production registry authentication, retention, replication, and recovery",
            "operated signing identity and transparency verification",
            "representative capacity evidence",
        ],
    }
    write_handoff(CAPSTONE / "handoff", release, attachments)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
