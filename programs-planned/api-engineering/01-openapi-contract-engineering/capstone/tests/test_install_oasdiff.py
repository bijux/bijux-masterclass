from __future__ import annotations

import hashlib
import io
import tarfile
from pathlib import Path

import pytest

from install_oasdiff import InstallError, asset_name, extract_executable, parse_checksum, verify_checksum


def test_asset_name_for_linux_amd64() -> None:
    assert asset_name("1.27.0", "Linux", "x86_64") == "oasdiff_1.27.0_linux_amd64.tar.gz"


def test_asset_name_for_darwin_uses_universal_release() -> None:
    assert asset_name("1.27.0", "Darwin", "arm64") == "oasdiff_1.27.0_darwin_all.tar.gz"


def test_parse_and_verify_checksum() -> None:
    content = b"release archive"
    digest = hashlib.sha256(content).hexdigest()
    assert parse_checksum(f"{digest}  oasdiff_1.27.0_linux_amd64.tar.gz\n", "oasdiff_1.27.0_linux_amd64.tar.gz") == digest
    verify_checksum(content, digest)


def test_checksum_mismatch_is_rejected() -> None:
    with pytest.raises(InstallError, match="checksum mismatch"):
        verify_checksum(b"tampered", "0" * 64)


def test_extracts_only_expected_executable(tmp_path: Path) -> None:
    buffer = io.BytesIO()
    payload = b"#!/bin/sh\necho oasdiff version 1.27.0\n"
    with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
        info = tarfile.TarInfo("release/oasdiff")
        info.size = len(payload)
        info.mode = 0o755
        archive.addfile(info, io.BytesIO(payload))
    destination = tmp_path / "bin" / "oasdiff"
    extract_executable(buffer.getvalue(), destination)
    assert destination.read_bytes() == payload
    assert destination.stat().st_mode & 0o111
