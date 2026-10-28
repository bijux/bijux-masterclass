from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Mapping, Any


def verify_publication(publication: Mapping[str,Any], root: Path, sbom: Mapping[str,Any], provenance: Mapping[str,Any]) -> tuple[bool,str]:
    if sbom.get("bomFormat") != "CycloneDX" or sbom.get("specVersion") != "1.7":
        return False,"invalid-sbom-profile"
    if provenance.get("predicateType") != "https://slsa.dev/provenance/v1":
        return False,"invalid-provenance-profile"
    for item in publication.get("artifacts",[]):
        path = root / item["path"]
        if not path.is_file():
            return False,"missing-artifact"
        if hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
            return False,"artifact-digest-mismatch"
    return True,"verified"


def publication_decision(*, has_digest: bool, has_sbom: bool, has_provenance: bool) -> str:
    return "publish" if has_digest and has_sbom and has_provenance else "incomplete-publication"
