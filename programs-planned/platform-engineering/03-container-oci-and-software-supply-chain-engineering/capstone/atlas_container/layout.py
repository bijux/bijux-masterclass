from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .canonical import canonical_json_bytes, parse_json_object
from .digest import digest_hex, sha256_digest, verify_digest

OCI_LAYOUT_VERSION = "1.0.0"
IMAGE_INDEX = "application/vnd.oci.image.index.v1+json"
IMAGE_MANIFEST = "application/vnd.oci.image.manifest.v1+json"
IMAGE_CONFIG = "application/vnd.oci.image.config.v1+json"


@dataclass(frozen=True)
class Descriptor:
    mediaType: str
    digest: str
    size: int
    annotations: dict[str, str] | None = None
    platform: dict[str, str] | None = None
    artifactType: str | None = None

    def as_dict(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "mediaType": self.mediaType,
            "digest": self.digest,
            "size": self.size,
        }
        if self.annotations:
            value["annotations"] = dict(sorted(self.annotations.items()))
        if self.platform:
            value["platform"] = dict(sorted(self.platform.items()))
        if self.artifactType:
            value["artifactType"] = self.artifactType
        return value


class OciLayout:
    def __init__(self, root: Path):
        self.root = root
        self.blobs = root / "blobs" / "sha256"

    @staticmethod
    def _atomic_write(path: Path, data: bytes) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".atlas-oci-", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)

    def initialize(self) -> None:
        self.blobs.mkdir(parents=True, exist_ok=True)
        self._atomic_write(
            self.root / "oci-layout",
            canonical_json_bytes({"imageLayoutVersion": OCI_LAYOUT_VERSION}),
        )
        if not (self.root / "index.json").exists():
            self._atomic_write(
                self.root / "index.json",
                canonical_json_bytes(
                    {
                        "schemaVersion": 2,
                        "mediaType": IMAGE_INDEX,
                        "manifests": [],
                    }
                ),
            )

    def put_blob(self, data: bytes, media_type: str, **kwargs: Any) -> Descriptor:
        if not isinstance(media_type, str) or not media_type:
            raise ValueError("blob media type is required")
        digest = sha256_digest(data)
        path = self.blobs / digest_hex(digest)
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with path.open("xb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
        except FileExistsError:
            existing = path.read_bytes()
            if existing != data:
                raise ValueError("content-addressed blob collision")
        return Descriptor(media_type, digest, len(data), **kwargs)

    def get_blob(self, digest: str) -> bytes:
        data = (self.blobs / digest_hex(digest)).read_bytes()
        verify_digest(data, digest)
        return data

    def put_json(self, value: dict[str, Any], media_type: str, **kwargs: Any) -> Descriptor:
        return self.put_blob(canonical_json_bytes(value), media_type, **kwargs)

    def read_index(self) -> dict[str, Any]:
        return parse_json_object((self.root / "index.json").read_bytes())

    def write_index(
        self,
        manifests: list[Descriptor],
        annotations: dict[str, str] | None = None,
    ) -> None:
        value: dict[str, Any] = {
            "schemaVersion": 2,
            "mediaType": IMAGE_INDEX,
            "manifests": [descriptor.as_dict() for descriptor in manifests],
        }
        if annotations:
            value["annotations"] = dict(sorted(annotations.items()))
        self._atomic_write(self.root / "index.json", canonical_json_bytes(value))

    def _descriptor_blob(
        self,
        descriptor: Any,
        *,
        location: str,
        errors: list[str],
    ) -> tuple[dict[str, Any], bytes] | None:
        if not isinstance(descriptor, dict):
            errors.append(f"{location}: descriptor must be an object")
            return None
        media_type = descriptor.get("mediaType")
        digest = descriptor.get("digest")
        size = descriptor.get("size")
        if not isinstance(media_type, str) or not media_type:
            errors.append(f"{location}: descriptor mediaType is required")
        if not isinstance(digest, str):
            errors.append(f"{location}: descriptor digest is required")
            return None
        if not isinstance(size, int) or isinstance(size, bool) or size < 0:
            errors.append(f"{location}: descriptor size must be a non-negative integer")
            return None
        try:
            data = self.get_blob(digest)
        except Exception as exc:
            errors.append(f"{location}: unreadable descriptor {digest}: {exc}")
            return None
        if len(data) != size:
            errors.append(
                f"{location}: descriptor size mismatch for {digest}: "
                f"declared {size}, observed {len(data)}"
            )
        return descriptor, data

    def _validate_graph_descriptor(
        self,
        descriptor: Any,
        *,
        location: str,
        errors: list[str],
        visiting: set[str],
        visited: set[str],
    ) -> None:
        loaded = self._descriptor_blob(descriptor, location=location, errors=errors)
        if loaded is None:
            return
        descriptor_value, data = loaded
        digest = descriptor_value["digest"]
        media_type = descriptor_value.get("mediaType")
        if digest in visited:
            return
        if digest in visiting:
            errors.append(f"{location}: descriptor cycle detected at {digest}")
            return
        visiting.add(digest)

        if media_type in {IMAGE_INDEX, IMAGE_MANIFEST, IMAGE_CONFIG}:
            try:
                value = parse_json_object(data)
            except Exception as exc:
                errors.append(f"{location}: invalid JSON blob {digest}: {exc}")
                visiting.remove(digest)
                visited.add(digest)
                return

            if media_type == IMAGE_INDEX:
                if value.get("schemaVersion") != 2:
                    errors.append(f"{location}: image index schemaVersion must be 2")
                manifests = value.get("manifests")
                if not isinstance(manifests, list):
                    errors.append(f"{location}: image index manifests must be an array")
                else:
                    seen_platforms: set[tuple[str | None, str | None, str | None]] = set()
                    for number, child in enumerate(manifests):
                        platform = child.get("platform", {}) if isinstance(child, dict) else {}
                        key = (
                            platform.get("os"),
                            platform.get("architecture"),
                            platform.get("variant"),
                        )
                        if key != (None, None, None):
                            if key in seen_platforms:
                                errors.append(
                                    f"{location}: duplicate platform descriptor {key}"
                                )
                            seen_platforms.add(key)
                        self._validate_graph_descriptor(
                            child,
                            location=f"{location}.manifests[{number}]",
                            errors=errors,
                            visiting=visiting,
                            visited=visited,
                        )
            elif media_type == IMAGE_MANIFEST:
                if value.get("schemaVersion") != 2:
                    errors.append(f"{location}: image manifest schemaVersion must be 2")
                config = value.get("config")
                if config is None:
                    errors.append(f"{location}: image manifest config is required")
                else:
                    self._validate_graph_descriptor(
                        config,
                        location=f"{location}.config",
                        errors=errors,
                        visiting=visiting,
                        visited=visited,
                    )
                layers = value.get("layers")
                if not isinstance(layers, list):
                    errors.append(f"{location}: image manifest layers must be an array")
                else:
                    for number, child in enumerate(layers):
                        self._descriptor_blob(
                            child,
                            location=f"{location}.layers[{number}]",
                            errors=errors,
                        )
                if "subject" in value:
                    self._validate_graph_descriptor(
                        value["subject"],
                        location=f"{location}.subject",
                        errors=errors,
                        visiting=visiting,
                        visited=visited,
                    )
            elif media_type == IMAGE_CONFIG:
                if value.get("rootfs", {}).get("type") != "layers":
                    errors.append(f"{location}: image config rootfs type must be layers")
                diff_ids = value.get("rootfs", {}).get("diff_ids")
                if not isinstance(diff_ids, list):
                    errors.append(f"{location}: image config diff_ids must be an array")

        visiting.remove(digest)
        visited.add(digest)

    def validate(self) -> list[str]:
        """Validate the complete reachable OCI descriptor graph.

        This is a strict course profile, not an OCI conformance suite. It
        verifies local digest/size integrity and the graph shapes used by Atlas.
        """

        errors: list[str] = []
        try:
            layout = json.loads((self.root / "oci-layout").read_text())
            if layout.get("imageLayoutVersion") != OCI_LAYOUT_VERSION:
                errors.append("unsupported OCI layout version")
            index = self.read_index()
            if index.get("schemaVersion") != 2:
                errors.append("root index schemaVersion must be 2")
            if index.get("mediaType") != IMAGE_INDEX:
                errors.append("root index mediaType must be the OCI image index type")
            manifests = index.get("manifests")
            if not isinstance(manifests, list):
                errors.append("root index manifests must be an array")
                return errors
            visiting: set[str] = set()
            visited: set[str] = set()
            for number, descriptor in enumerate(manifests):
                self._validate_graph_descriptor(
                    descriptor,
                    location=f"index.manifests[{number}]",
                    errors=errors,
                    visiting=visiting,
                    visited=visited,
                )
        except Exception as exc:
            errors.append(str(exc))
        return errors
