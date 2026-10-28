from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from atlas_container.archive import LayerFile, apply_layer, build_layer
from atlas_container.canonical import canonical_json_bytes
from atlas_container.digest import sha256_digest, verify_digest
from atlas_container.image import artifact_manifest, build_image, build_index
from atlas_container.layout import OciLayout
from atlas_container.platform import select_manifest, verify_platform_label


def _layout(root: Path):
    layout = OciLayout(root)
    layout.initialize()
    amd = build_image(
        layout,
        architecture="amd64",
        entries=[LayerFile("usr/local/bin/atlas", b"amd64", 0o755)],
        entrypoint=["/usr/local/bin/atlas"],
    )
    arm = build_image(
        layout,
        architecture="arm64",
        entries=[LayerFile("usr/local/bin/atlas", b"arm64", 0o755)],
        entrypoint=["/usr/local/bin/atlas"],
    )
    index = build_index(
        layout,
        [amd.manifest, arm.manifest],
        {"org.opencontainers.image.version": "1.0.0"},
    )
    return layout, amd, arm, index


def test_canonical_json_binds_digest_to_exact_bytes() -> None:
    first = canonical_json_bytes({"b": 2, "a": 1})
    second = canonical_json_bytes({"a": 1, "b": 2})
    assert first == second
    digest = sha256_digest(first)
    verify_digest(first, digest)
    with pytest.raises(ValueError):
        verify_digest(first + b"x", digest)


def test_layer_is_deterministic_and_whiteout_removes_lower_entry(tmp_path: Path) -> None:
    entries = [
        LayerFile("data", mode=0o755, kind="directory"),
        LayerFile("data/old.txt", b"old", 0o644),
    ]
    assert build_layer(entries) == build_layer(reversed(entries))
    layer = build_layer(entries)[0]
    apply_layer(layer, tmp_path)
    assert (tmp_path / "data/old.txt").read_text() == "old"
    delete = build_layer([LayerFile("data/.wh.old.txt", b"", 0o000)])[0]
    apply_layer(delete, tmp_path)
    assert not (tmp_path / "data/old.txt").exists()


def test_layout_selects_platform_and_validates_descriptor_integrity(tmp_path: Path) -> None:
    layout, amd, arm, index = _layout(tmp_path)
    assert layout.validate() == []
    value = json.loads(layout.get_blob(index.digest))
    assert select_manifest(value, "linux", "amd64")["digest"] == amd.manifest.digest
    assert select_manifest(value, "linux", "arm64")["digest"] == arm.manifest.digest


def test_artifact_subject_is_the_image_index_not_a_tag(tmp_path: Path) -> None:
    layout, _, _, index = _layout(tmp_path)
    evidence = artifact_manifest(
        layout,
        subject=index,
        artifact_type="application/vnd.example.evidence+json",
        payload=b"{}",
        payload_media_type="application/json",
    )
    manifest = json.loads(layout.get_blob(evidence.digest))
    assert manifest["subject"]["digest"] == index.digest


def test_platform_label_must_match_elf_machine() -> None:
    header = bytearray(64)
    header[:4] = b"\x7fELF"
    header[5] = 1
    header[18:20] = (62).to_bytes(2, "little")
    verify_platform_label(bytes(header), "amd64")
    with pytest.raises(ValueError):
        verify_platform_label(bytes(header), "arm64")


def test_layer_rejects_absolute_parent_traversal_links_and_duplicate_entries(tmp_path: Path) -> None:
    from atlas_container.archive import deterministic_tar, deterministic_gzip
    import io
    import tarfile

    with pytest.raises(ValueError):
        build_layer([LayerFile("../../etc/passwd", b"x")])
    with pytest.raises(ValueError):
        build_layer([LayerFile("/etc/passwd", b"x")])
    with pytest.raises(ValueError):
        build_layer([LayerFile("same", b"a"), LayerFile("same", b"b")])

    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w") as tar:
        info = tarfile.TarInfo("link")
        info.type = tarfile.SYMTYPE
        info.linkname = "/etc/passwd"
        tar.addfile(info)
    with pytest.raises(ValueError):
        apply_layer(deterministic_gzip(stream.getvalue()), tmp_path)


def test_opaque_whiteout_is_independent_of_tar_member_order(tmp_path: Path) -> None:
    import gzip
    import io
    import tarfile

    lower = build_layer(
        [
            LayerFile("data", mode=0o755, kind="directory"),
            LayerFile("data/lower.txt", b"lower"),
        ]
    )[0]
    apply_layer(lower, tmp_path)

    # Put the ordinary file before the opaque marker. Correct application still
    # removes lower entries and preserves entries introduced by this layer.
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w") as tar:
        file_info = tarfile.TarInfo("data/current.txt")
        file_info.size = 7
        tar.addfile(file_info, io.BytesIO(b"current"))
        whiteout = tarfile.TarInfo("data/.wh..wh..opq")
        whiteout.size = 0
        tar.addfile(whiteout, io.BytesIO())
    apply_layer(gzip.compress(raw.getvalue(), mtime=0), tmp_path)
    assert not (tmp_path / "data/lower.txt").exists()
    assert (tmp_path / "data/current.txt").read_text() == "current"


def test_layer_refuses_to_follow_preexisting_rootfs_symlink(tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside-atlas-layer"
    outside.mkdir(exist_ok=True)
    (tmp_path / "data").symlink_to(outside, target_is_directory=True)
    layer = build_layer([LayerFile("data/payload", b"escape")])[0]
    with pytest.raises(ValueError):
        apply_layer(layer, tmp_path)
    assert not (outside / "payload").exists()


def test_layout_validation_walks_reachable_child_descriptors(tmp_path: Path) -> None:
    layout, _, _, index = _layout(tmp_path)
    root_index = layout.read_index()
    child_index = json.loads(layout.get_blob(index.digest))
    manifest_digest = child_index["manifests"][0]["digest"]
    manifest_path = layout.blobs / manifest_digest.split(":", 1)[1]
    manifest_path.write_bytes(manifest_path.read_bytes() + b"tamper")
    errors = layout.validate()
    assert any("unreadable descriptor" in error for error in errors)
