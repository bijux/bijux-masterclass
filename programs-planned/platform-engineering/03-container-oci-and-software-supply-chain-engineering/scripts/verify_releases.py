#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

COURSE = Path(__file__).resolve().parents[1]
RELEASES = COURSE / "capstone" / "releases"
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")

accepted = json.loads((RELEASES / "accepted" / "release.json").read_text())
if accepted.get("release") != "atlas-workload-release-1.0.0":
    raise SystemExit("accepted release has the wrong identity")
if accepted.get("decision") != "accepted-for-course-4-handoff":
    raise SystemExit("accepted release lacks the checked decision")
images = accepted.get("images")
if not isinstance(images, list) or {item.get("name") for item in images} != {"atlas-api", "atlas-worker"}:
    raise SystemExit("accepted release must identify API and worker images")
for image in images:
    if not DIGEST.fullmatch(str(image.get("digest", ""))):
        raise SystemExit(f"accepted image has invalid digest: {image}")
    if image.get("runtimeUser") != "65532:65532":
        raise SystemExit(f"accepted image has unexpected runtime user: {image}")
    platforms = {(p.get("os"), p.get("architecture")) for p in image.get("platforms", [])}
    if platforms != {("linux", "amd64"), ("linux", "arm64")}:
        raise SystemExit(f"accepted image platform set is incomplete: {image}")
    evidence = accepted.get("evidence", {}).get("images", {}).get(image["name"], {})
    if evidence.get("subject") != image["digest"]:
        raise SystemExit(f"evidence subject mismatch for {image['name']}")
    if evidence.get("policyDecision") != "accepted":
        raise SystemExit(f"image policy did not accept {image['name']}")

expected = {
    "rejected-mutable-tag": "rejected",
    "rejected-root-runtime": "rejected",
    "rejected-missing-platform": "rejected",
    "rejected-secret-layer": "rejected",
    "rejected-incomplete-sbom": "rejected",
    "rejected-wrong-subject": "rejected",
    "rejected-untrusted-builder": "rejected",
    "review-required-native-evidence": "review-required",
    "not-executed-production-registry": "not-executed",
}
candidates = sorted(RELEASES.glob("*/candidate.json"))
seen: dict[str, str] = {}
for path in candidates:
    value = json.loads(path.read_text())
    ident = value.get("id")
    decision = value.get("expectedDecision")
    if ident in seen:
        raise SystemExit(f"duplicate candidate id: {ident}")
    seen[str(ident)] = str(decision)
    for key in ("title", "failedGate", "condition", "evidenceClass", "reviewQuestion"):
        if not str(value.get(key, "")).strip():
            raise SystemExit(f"{path} missing {key}")
if seen != expected:
    raise SystemExit(f"release candidate corpus mismatch: {seen}")
print("PASS release fixtures — 1 accepted, 7 rejected, 1 review-required, 1 not-executed")
