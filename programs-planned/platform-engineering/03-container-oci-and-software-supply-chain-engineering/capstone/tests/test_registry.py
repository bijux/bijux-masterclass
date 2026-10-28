from __future__ import annotations

import tempfile
import threading
from pathlib import Path

from atlas_container.canonical import canonical_json_bytes
from atlas_container.digest import sha256_digest
from atlas_container.image import IMAGE_MANIFEST
from atlas_container.registry import RegistryClient, RegistryServer, RegistryStore


def test_registry_push_pull_tag_resolution_and_referrers() -> None:
    with tempfile.TemporaryDirectory() as td:
        server = RegistryServer(("127.0.0.1", 0), RegistryStore(Path(td)))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            client = RegistryClient(f"http://127.0.0.1:{server.server_port}")
            client.ping()
            config = b"{}"
            config_digest = client.push_blob("atlas/api", config)
            manifest = canonical_json_bytes(
                {
                    "schemaVersion": 2,
                    "mediaType": IMAGE_MANIFEST,
                    "config": {
                        "mediaType": "application/example",
                        "digest": config_digest,
                        "size": len(config),
                    },
                    "layers": [],
                }
            )
            digest = client.push_manifest("atlas/api", "1.0.0", manifest, IMAGE_MANIFEST)
            pulled, resolved = client.get_manifest("atlas/api", "1.0.0")
            assert pulled == manifest
            assert resolved == digest

            payload_digest = client.push_blob("atlas/api", b"evidence")
            referrer = canonical_json_bytes(
                {
                    "schemaVersion": 2,
                    "mediaType": IMAGE_MANIFEST,
                    "artifactType": "application/example",
                    "config": {
                        "mediaType": "application/example",
                        "digest": config_digest,
                        "size": len(config),
                    },
                    "layers": [
                        {
                            "mediaType": "text/plain",
                            "digest": payload_digest,
                            "size": 8,
                        }
                    ],
                    "subject": {
                        "mediaType": IMAGE_MANIFEST,
                        "digest": digest,
                        "size": len(manifest),
                    },
                }
            )
            client.push_manifest(
                "atlas/api", sha256_digest(referrer), referrer, IMAGE_MANIFEST
            )
            refs = client.get_referrers("atlas/api", digest)
            assert len(refs["manifests"]) == 1
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)


def test_registry_scopes_blobs_to_repository_and_rejects_unsafe_names() -> None:
    import pytest

    with tempfile.TemporaryDirectory() as td:
        store = RegistryStore(Path(td))
        digest = sha256_digest(b"payload")
        store.put_blob(b"payload", digest, name="atlas/api")
        assert store.get_blob(digest, name="atlas/api") == b"payload"
        with pytest.raises(FileNotFoundError):
            store.get_blob(digest, name="other/repository")
        with pytest.raises(ValueError):
            store.put_blob(b"payload", digest, name="../escape")
        with pytest.raises(ValueError):
            store.put_manifest("atlas/api", "../../tag", b"{}", IMAGE_MANIFEST)


def test_registry_rejects_unknown_upload_and_unlinked_manifest_dependencies() -> None:
    import pytest

    with tempfile.TemporaryDirectory() as td:
        store = RegistryStore(Path(td))
        digest = sha256_digest(b"payload")
        with pytest.raises(ValueError):
            store.complete_upload("atlas/api", "unknown", b"payload", digest)

        missing = canonical_json_bytes(
            {
                "schemaVersion": 2,
                "mediaType": IMAGE_MANIFEST,
                "config": {
                    "mediaType": "application/example",
                    "digest": digest,
                    "size": 7,
                },
                "layers": [],
            }
        )
        with pytest.raises(FileNotFoundError):
            store.put_manifest("atlas/api", "1.0.0", missing, IMAGE_MANIFEST)
