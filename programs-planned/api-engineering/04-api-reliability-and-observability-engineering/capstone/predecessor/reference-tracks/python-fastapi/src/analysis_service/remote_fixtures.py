"""Resolve the course's controlled remote-object fixture URLs safely.

The adapter intentionally supports one HTTPS origin backed by an
operator-controlled local fixture directory. It rejects credentials, alternate
ports, query strings, fragments, traversal segments, and symbolic links. This
is a teaching adapter, not a general-purpose HTTP object-store client.
"""
from __future__ import annotations

from pathlib import Path
import stat
from urllib.parse import unquote, urlsplit


class RemoteFixtureError(RuntimeError):
    """The durable remote-object reference violates the fixture policy."""


def resolve_remote_fixture(root: Path, uri: str) -> Path:
    """Return a regular, non-symlink file below *root* for an approved URI."""

    try:
        parsed = urlsplit(uri)
        port = parsed.port
    except ValueError as exc:
        raise RemoteFixtureError("remote object URI is invalid") from exc

    if (
        parsed.scheme != "https"
        or parsed.hostname != "objects.example.test"
        or parsed.username
        or parsed.password
        or port is not None
        or parsed.query
        or parsed.fragment
    ):
        raise RemoteFixtureError("untrusted remote object URI")

    try:
        decoded_path = unquote(parsed.path, errors="strict")
    except UnicodeDecodeError as exc:
        raise RemoteFixtureError(
            "remote object path is not valid UTF-8"
        ) from exc

    if "\x00" in decoded_path or "\\" in decoded_path:
        raise RemoteFixtureError("remote object path contains an unsafe byte")

    segments = [segment for segment in decoded_path.split("/") if segment]
    if not segments or any(segment in {".", ".."} for segment in segments):
        raise RemoteFixtureError("remote object path traversal")

    try:
        fixture_root = root.resolve(strict=True)
    except FileNotFoundError as exc:
        raise FileNotFoundError(root) from exc

    candidate = fixture_root
    final_metadata = None
    for segment in segments:
        candidate = candidate / segment
        metadata = candidate.lstat()
        if stat.S_ISLNK(metadata.st_mode):
            raise RemoteFixtureError("remote fixture contains a symbolic link")
        final_metadata = metadata

    assert final_metadata is not None  # guarded by the non-empty segment rule
    resolved = candidate.resolve(strict=True)
    if fixture_root != resolved and fixture_root not in resolved.parents:
        raise RemoteFixtureError("remote fixture escaped root")
    if not stat.S_ISREG(final_metadata.st_mode):
        raise RemoteFixtureError("remote fixture is not a regular file")
    return resolved
