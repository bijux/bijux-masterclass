from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .archive import LayerFile, build_layer
from .canonical import canonical_json_bytes
from .layout import Descriptor, OciLayout

IMAGE_CONFIG = "application/vnd.oci.image.config.v1+json"
IMAGE_MANIFEST = "application/vnd.oci.image.manifest.v1+json"
IMAGE_LAYER_GZIP = "application/vnd.oci.image.layer.v1.tar+gzip"
IMAGE_INDEX = "application/vnd.oci.image.index.v1+json"


@dataclass(frozen=True)
class ImageBuild:
    manifest: Descriptor
    config: Descriptor
    layers: tuple[Descriptor, ...]
    diff_ids: tuple[str, ...]


def build_image(
    layout: OciLayout,
    *,
    architecture: str,
    entries: list[LayerFile],
    entrypoint: list[str],
    user: str = "65532:65532",
    env: list[str] | None = None,
    labels: dict[str, str] | None = None,
    annotations: dict[str, str] | None = None,
) -> ImageBuild:
    compressed, layer_digest, diff_id = build_layer(entries)
    layer_desc = layout.put_blob(compressed, IMAGE_LAYER_GZIP)
    if layer_desc.digest != layer_digest:
        raise AssertionError("layer digest changed after storage")
    config_value: dict[str, Any] = {
        "created": "1970-01-01T00:00:00Z",
        "architecture": architecture,
        "os": "linux",
        "config": {
            "User": user,
            "Env": sorted(env or ["PATH=/usr/local/bin:/usr/bin:/bin"]),
            "Entrypoint": entrypoint,
            "WorkingDir": "/",
            "Labels": dict(sorted((labels or {}).items())),
        },
        "rootfs": {"type": "layers", "diff_ids": [diff_id]},
        "history": [
            {
                "created": "1970-01-01T00:00:00Z",
                "created_by": "atlas deterministic OCI builder",
            }
        ],
    }
    config_desc = layout.put_json(config_value, IMAGE_CONFIG)
    manifest_value = {
        "schemaVersion": 2,
        "mediaType": IMAGE_MANIFEST,
        "config": config_desc.as_dict(),
        "layers": [layer_desc.as_dict()],
        "annotations": dict(sorted((annotations or {}).items())),
    }
    manifest_desc = layout.put_json(
        manifest_value,
        IMAGE_MANIFEST,
        annotations=annotations,
        platform={"os": "linux", "architecture": architecture},
    )
    return ImageBuild(manifest_desc, config_desc, (layer_desc,), (diff_id,))


def build_index(layout: OciLayout, manifests: list[Descriptor], annotations: dict[str, str]) -> Descriptor:
    value = {
        "schemaVersion": 2,
        "mediaType": IMAGE_INDEX,
        "manifests": [manifest.as_dict() for manifest in manifests],
        "annotations": dict(sorted(annotations.items())),
    }
    descriptor = layout.put_json(value, IMAGE_INDEX, annotations=annotations)
    layout.write_index([descriptor], annotations={"org.opencontainers.image.ref.name": "atlas-release"})
    return descriptor


def artifact_manifest(
    layout: OciLayout,
    *,
    subject: Descriptor,
    artifact_type: str,
    payload: bytes,
    payload_media_type: str,
    annotations: dict[str, str] | None = None,
) -> Descriptor:
    payload_desc = layout.put_blob(payload, payload_media_type)
    value = {
        "schemaVersion": 2,
        "mediaType": IMAGE_MANIFEST,
        "artifactType": artifact_type,
        "config": {
            "mediaType": "application/vnd.oci.empty.v1+json",
            "digest": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "size": 0,
        },
        "layers": [payload_desc.as_dict()],
        "subject": subject.as_dict(),
        "annotations": dict(sorted((annotations or {}).items())),
    }
    # OCI empty JSON blob is zero bytes for this instructional fixture.
    layout.put_blob(b"", "application/vnd.oci.empty.v1+json")
    return layout.put_json(
        value,
        IMAGE_MANIFEST,
        artifactType=artifact_type,
        annotations=annotations,
    )
