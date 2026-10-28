from __future__ import annotations

from pathlib import Path
from typing import Any

from .archive import apply_layer
from .canonical import parse_json_object
from .layout import OciLayout


def unpack_manifest(layout: OciLayout, manifest_digest: str, destination: Path) -> dict[str, Any]:
    manifest = parse_json_object(layout.get_blob(manifest_digest))
    for descriptor in manifest.get("layers", []):
        apply_layer(layout.get_blob(descriptor["digest"]), destination)
    config = parse_json_object(layout.get_blob(manifest["config"]["digest"]))
    return config
