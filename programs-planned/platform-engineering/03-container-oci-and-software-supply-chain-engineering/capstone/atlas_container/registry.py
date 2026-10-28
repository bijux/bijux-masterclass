from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
import threading
import urllib.error
import urllib.parse
import urllib.request
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .canonical import canonical_json_bytes, parse_json_object
from .digest import digest_hex, sha256_digest, verify_digest

_TAG = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9._-]{0,127}$")
_REPOSITORY_COMPONENT = re.compile(r"^[a-z0-9]+(?:[._-][a-z0-9]+)*$")
_MAX_BLOB_BYTES = 64 * 1024 * 1024
_MAX_MANIFEST_BYTES = 4 * 1024 * 1024


class RegistryStore:
    """A deliberately small, filesystem-backed Distribution teaching store.

    It models content-addressed blobs, repository-scoped links, immutable
    manifest digests, mutable tags, and the referrers relationship. It is not a
    production registry and does not implement authentication, chunked upload,
    garbage collection, or the complete Distribution conformance surface.
    """

    def __init__(self, root: Path):
        self.root = root.resolve()
        self.blobs = self.root / "blobs" / "sha256"
        self.repositories = self.root / "repositories"
        self.uploads: dict[str, str] = {}
        self.lock = threading.Lock()

    @staticmethod
    def _atomic_write(path: Path, data: bytes) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".atlas-registry-", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)

    def _repo(self, name: str) -> Path:
        if not isinstance(name, str) or not name or "\x00" in name or "\\" in name:
            raise ValueError("invalid repository name")
        components = name.split("/")
        if any(not _REPOSITORY_COMPONENT.fullmatch(component) for component in components):
            raise ValueError("invalid repository name")
        candidate = self.repositories.joinpath(*components)
        if self.repositories.resolve() not in candidate.resolve(strict=False).parents:
            raise ValueError("repository path escapes registry root")
        return candidate

    @staticmethod
    def _reference(reference: str) -> str:
        if reference.startswith("sha256:"):
            digest_hex(reference)
            return reference
        if not _TAG.fullmatch(reference):
            raise ValueError("invalid manifest tag")
        return reference

    def _link_blob(self, name: str, digest: str) -> None:
        repo = self._repo(name)
        marker = repo / "blobs" / digest_hex(digest)
        self._atomic_write(marker, (digest + "\n").encode())

    def put_blob(self, data: bytes, digest: str, *, name: str | None = None) -> None:
        if len(data) > _MAX_BLOB_BYTES:
            raise ValueError("blob exceeds course registry size limit")
        verify_digest(data, digest)
        path = self.blobs / digest_hex(digest)
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with path.open("xb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
        except FileExistsError:
            if path.read_bytes() != data:
                raise ValueError("blob collision")
        if name is not None:
            self._link_blob(name, digest)

    def get_blob(self, digest: str, *, name: str | None = None) -> bytes:
        if name is not None:
            marker = self._repo(name) / "blobs" / digest_hex(digest)
            if not marker.is_file():
                raise FileNotFoundError("blob is not linked to repository")
        data = (self.blobs / digest_hex(digest)).read_bytes()
        verify_digest(data, digest)
        return data

    def begin_upload(self, name: str) -> str:
        self._repo(name)
        upload = uuid.uuid4().hex
        with self.lock:
            self.uploads[upload] = name
        return upload

    def complete_upload(self, name: str, upload: str, data: bytes, digest: str) -> None:
        with self.lock:
            owner = self.uploads.get(upload)
            if owner != name:
                raise ValueError("unknown upload or repository mismatch")
        self.put_blob(data, digest, name=name)
        with self.lock:
            self.uploads.pop(upload, None)

    def _require_descriptor(self, name: str, descriptor: Any, location: str) -> None:
        if not isinstance(descriptor, dict):
            raise ValueError(f"{location} descriptor must be an object")
        digest = descriptor.get("digest")
        size = descriptor.get("size")
        if not isinstance(digest, str) or not isinstance(size, int) or isinstance(size, bool):
            raise ValueError(f"{location} descriptor is incomplete")
        data = self.get_blob(digest, name=name)
        if len(data) != size:
            raise ValueError(f"{location} descriptor size mismatch")

    def _validate_manifest_references(self, name: str, data: bytes) -> None:
        value = parse_json_object(data)
        if value.get("schemaVersion") != 2:
            raise ValueError("manifest schemaVersion must be 2")
        if isinstance(value.get("manifests"), list):
            for number, descriptor in enumerate(value["manifests"]):
                self._require_descriptor(name, descriptor, f"manifests[{number}]")
        else:
            self._require_descriptor(name, value.get("config"), "config")
            layers = value.get("layers")
            if not isinstance(layers, list):
                raise ValueError("manifest layers must be an array")
            for number, descriptor in enumerate(layers):
                self._require_descriptor(name, descriptor, f"layers[{number}]")
        if "subject" in value:
            self._require_descriptor(name, value["subject"], "subject")

    def put_manifest(self, name: str, reference: str, data: bytes, media_type: str) -> str:
        if len(data) > _MAX_MANIFEST_BYTES:
            raise ValueError("manifest exceeds course registry size limit")
        self._repo(name)
        reference = self._reference(reference)
        digest = sha256_digest(data)
        if reference.startswith("sha256:") and reference != digest:
            raise ValueError("manifest digest reference does not match body")
        self._validate_manifest_references(name, data)
        self.put_blob(data, digest, name=name)
        repo = self._repo(name)
        self._atomic_write(
            repo / "manifests" / digest_hex(digest),
            (media_type + "\n").encode(),
        )
        if not reference.startswith("sha256:"):
            self._atomic_write(repo / "tags" / reference, (digest + "\n").encode())
        return digest

    def resolve(self, name: str, reference: str) -> tuple[bytes, str, str]:
        repo = self._repo(name)
        reference = self._reference(reference)
        digest = reference
        if not reference.startswith("sha256:"):
            digest = (repo / "tags" / reference).read_text().strip()
        media_type = (repo / "manifests" / digest_hex(digest)).read_text().strip()
        return self.get_blob(digest, name=name), media_type, digest

    def referrers(self, name: str, subject: str, artifact_type: str | None = None) -> dict[str, Any]:
        digest_hex(subject)
        repo = self._repo(name)
        descriptors = []
        manifest_dir = repo / "manifests"
        markers = sorted(manifest_dir.glob("*")) if manifest_dir.exists() else []
        for marker in markers:
            digest = "sha256:" + marker.name
            data = self.get_blob(digest, name=name)
            try:
                manifest = parse_json_object(data)
            except Exception:
                continue
            if manifest.get("subject", {}).get("digest") != subject:
                continue
            if artifact_type and manifest.get("artifactType") != artifact_type:
                continue
            descriptor: dict[str, Any] = {
                "mediaType": manifest.get(
                    "mediaType", "application/vnd.oci.image.manifest.v1+json"
                ),
                "digest": digest,
                "size": len(data),
            }
            if manifest.get("artifactType"):
                descriptor["artifactType"] = manifest["artifactType"]
            if manifest.get("annotations"):
                descriptor["annotations"] = manifest["annotations"]
            descriptors.append(descriptor)
        return {
            "schemaVersion": 2,
            "mediaType": "application/vnd.oci.image.index.v1+json",
            "manifests": descriptors,
        }


class RegistryHandler(BaseHTTPRequestHandler):
    server_version = "AtlasRegistry/1.1"

    @property
    def store(self) -> RegistryStore:
        return self.server.store  # type: ignore[attr-defined]

    def log_message(self, fmt: str, *args: Any) -> None:
        return

    def _send(
        self,
        code: int,
        body: bytes = b"",
        headers: dict[str, str] | None = None,
    ) -> None:
        self.send_response(code)
        for name, value in (headers or {}).items():
            self.send_header(name, value)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _error(self, code: int, error_code: str, message: str) -> None:
        body = canonical_json_bytes(
            {"errors": [{"code": error_code, "message": message}]}
        )
        self._send(code, body, {"Content-Type": "application/json"})

    def _parts(self) -> list[str]:
        path = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
        if "\x00" in path or "\\" in path:
            raise ValueError("invalid request path")
        return path.strip("/").split("/")

    def _read_body(self, maximum: int) -> bytes:
        raw = self.headers.get("Content-Length")
        if raw is None:
            raise ValueError("Content-Length is required")
        length = int(raw)
        if length < 0 or length > maximum:
            raise ValueError("request body exceeds course registry limit")
        body = self.rfile.read(length)
        if len(body) != length:
            raise ValueError("request body ended early")
        return body

    def do_GET(self) -> None:
        try:
            if urllib.parse.urlsplit(self.path).path == "/v2/":
                self._send(
                    200,
                    headers={"Docker-Distribution-Api-Version": "registry/2.0"},
                )
                return
            parts = self._parts()
            if len(parts) >= 5 and parts[0] == "v2" and "blobs" in parts:
                idx = parts.index("blobs")
                name = "/".join(parts[1:idx])
                digest = "/".join(parts[idx + 1 :])
                data = self.store.get_blob(digest, name=name)
                self._send(200, data, {"Docker-Content-Digest": digest})
                return
            if len(parts) >= 5 and parts[0] == "v2" and "manifests" in parts:
                idx = parts.index("manifests")
                name = "/".join(parts[1:idx])
                reference = "/".join(parts[idx + 1 :])
                data, media, digest = self.store.resolve(name, reference)
                self._send(
                    200,
                    data,
                    {"Content-Type": media, "Docker-Content-Digest": digest},
                )
                return
            if len(parts) >= 5 and parts[0] == "v2" and "referrers" in parts:
                idx = parts.index("referrers")
                name = "/".join(parts[1:idx])
                subject = "/".join(parts[idx + 1 :])
                query = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)
                artifact_type = query.get("artifactType", [None])[0]
                body = canonical_json_bytes(
                    self.store.referrers(name, subject, artifact_type)
                )
                self._send(
                    200,
                    body,
                    {"Content-Type": "application/vnd.oci.image.index.v1+json"},
                )
                return
            self._error(404, "NAME_UNKNOWN", "registry route not found")
        except (FileNotFoundError, ValueError) as exc:
            self._error(404, "MANIFEST_UNKNOWN", str(exc))
        except Exception:
            self._error(500, "UNKNOWN", "registry request failed")

    do_HEAD = do_GET

    def do_POST(self) -> None:
        try:
            parts = self._parts()
            if len(parts) >= 5 and parts[0] == "v2" and parts[-2:] == ["blobs", "uploads"]:
                name = "/".join(parts[1:-2])
                upload = self.store.begin_upload(name)
                location = f"/v2/{name}/blobs/uploads/{upload}"
                self._send(
                    202,
                    headers={"Location": location, "Docker-Upload-UUID": upload},
                )
            else:
                self._error(404, "NAME_UNKNOWN", "registry route not found")
        except ValueError as exc:
            self._error(400, "NAME_INVALID", str(exc))

    def do_PUT(self) -> None:
        try:
            parts = self._parts()
            query = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)
            if "uploads" in parts:
                idx = parts.index("blobs")
                name = "/".join(parts[1:idx])
                upload = parts[-1]
                digest = query.get("digest", [""])[0]
                body = self._read_body(_MAX_BLOB_BYTES)
                self.store.complete_upload(name, upload, body, digest)
                self._send(
                    201,
                    headers={
                        "Docker-Content-Digest": digest,
                        "Location": f"/v2/{name}/blobs/{digest}",
                    },
                )
                return
            if "manifests" in parts:
                idx = parts.index("manifests")
                name = "/".join(parts[1:idx])
                reference = "/".join(parts[idx + 1 :])
                body = self._read_body(_MAX_MANIFEST_BYTES)
                media = self.headers.get(
                    "Content-Type", "application/vnd.oci.image.manifest.v1+json"
                ).split(";", 1)[0].strip()
                digest = self.store.put_manifest(name, reference, body, media)
                self._send(201, headers={"Docker-Content-Digest": digest})
                return
            self._error(404, "NAME_UNKNOWN", "registry route not found")
        except ValueError as exc:
            self._error(400, "DIGEST_INVALID", str(exc))
        except Exception:
            self._error(500, "UNKNOWN", "registry request failed")


class RegistryServer(ThreadingHTTPServer):
    def __init__(self, address: tuple[str, int], store: RegistryStore):
        super().__init__(address, RegistryHandler)
        self.store = store


class RegistryClient:
    def __init__(self, base_url: str):
        self.base = base_url.rstrip("/")

    def _request(
        self,
        method: str,
        path: str,
        body: bytes = b"",
        headers: dict[str, str] | None = None,
    ) -> tuple[int, bytes, dict[str, str]]:
        request = urllib.request.Request(
            self.base + path,
            data=body if method in {"POST", "PUT"} else None,
            method=method,
            headers=headers or {},
        )
        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                return response.status, response.read(), dict(response.headers.items())
        except urllib.error.HTTPError as exc:
            return exc.code, exc.read(), dict(exc.headers.items())

    def ping(self) -> None:
        status, _, _ = self._request("GET", "/v2/")
        if status != 200:
            raise RuntimeError("registry ping failed")

    def push_blob(self, name: str, data: bytes) -> str:
        digest = sha256_digest(data)
        status, body, headers = self._request("POST", f"/v2/{name}/blobs/uploads/")
        if status != 202:
            raise RuntimeError(f"blob upload was not accepted: {body.decode(errors='replace')}")
        location = headers["Location"]
        separator = "&" if "?" in location else "?"
        status, body, response_headers = self._request(
            "PUT",
            location + separator + urllib.parse.urlencode({"digest": digest}),
            data,
        )
        if status != 201 or response_headers.get("Docker-Content-Digest") != digest:
            raise RuntimeError(f"blob upload failed digest verification: {body.decode(errors='replace')}")
        return digest

    def push_manifest(
        self, name: str, reference: str, data: bytes, media_type: str
    ) -> str:
        status, body, headers = self._request(
            "PUT",
            f"/v2/{name}/manifests/{reference}",
            data,
            {"Content-Type": media_type},
        )
        if status != 201:
            raise RuntimeError(f"manifest upload failed: {body.decode(errors='replace')}")
        return headers["Docker-Content-Digest"]

    def get_manifest(self, name: str, reference: str) -> tuple[bytes, str]:
        status, data, headers = self._request("GET", f"/v2/{name}/manifests/{reference}")
        if status != 200:
            raise RuntimeError(f"manifest pull failed: {data.decode(errors='replace')}")
        return data, headers["Docker-Content-Digest"]

    def get_referrers(
        self, name: str, subject: str, artifact_type: str | None = None
    ) -> dict[str, Any]:
        query = ""
        if artifact_type:
            query = "?" + urllib.parse.urlencode({"artifactType": artifact_type})
        status, data, _ = self._request("GET", f"/v2/{name}/referrers/{subject}{query}")
        if status != 200:
            raise RuntimeError(f"referrers query failed: {data.decode(errors='replace')}")
        return parse_json_object(data)


def serve(root: Path, host: str, port: int) -> None:
    server = RegistryServer((host, port), RegistryStore(root))
    print(json.dumps({"host": host, "port": server.server_port}), flush=True)
    server.serve_forever()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=0)
    args = parser.parse_args()
    serve(args.root, args.host, args.port)


if __name__ == "__main__":
    main()
