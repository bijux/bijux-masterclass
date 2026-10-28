from __future__ import annotations

import gzip
import io
import os
import shutil
import stat
import tarfile
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable

from .digest import sha256_digest

_MAX_COMPRESSED_LAYER = 64 * 1024 * 1024
_MAX_UNCOMPRESSED_LAYER = 256 * 1024 * 1024
_MAX_MEMBER_SIZE = 64 * 1024 * 1024
_MAX_MEMBERS = 10_000


@dataclass(frozen=True)
class LayerFile:
    path: str
    data: bytes = b""
    mode: int = 0o644
    kind: str = "file"  # file or directory


def _safe_path(path: str) -> str:
    """Return a normalized relative POSIX path or reject the entry.

    The course builder deliberately accepts a smaller path profile than tar.
    Absolute paths, parent traversal, NUL bytes, backslashes, and the root
    entry are rejected rather than normalized into a different meaning.
    """

    if not isinstance(path, str) or not path:
        raise ValueError("layer path must be a non-empty string")
    if "\x00" in path:
        raise ValueError("layer path contains a NUL byte")
    if "\\" in path:
        raise ValueError("layer path must use POSIX separators")
    if path.startswith("/"):
        raise ValueError(f"absolute layer path is forbidden: {path}")

    pure = PurePosixPath(path)
    parts = pure.parts
    if not parts or parts == (".",):
        raise ValueError("layer path must name an entry")
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError(f"unsafe layer path: {path}")
    return "/".join(parts)


def deterministic_tar(entries: Iterable[LayerFile]) -> bytes:
    prepared = sorted(entries, key=lambda item: _safe_path(item.path))
    if len(prepared) > _MAX_MEMBERS:
        raise ValueError("layer contains too many entries")

    names: set[str] = set()
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w", format=tarfile.PAX_FORMAT) as tar:
        for entry in prepared:
            name = _safe_path(entry.path)
            if name in names:
                raise ValueError(f"duplicate layer entry: {name}")
            names.add(name)
            if len(entry.data) > _MAX_MEMBER_SIZE:
                raise ValueError(f"layer entry exceeds size limit: {name}")

            info = tarfile.TarInfo(name=name)
            info.uid = 0
            info.gid = 0
            info.uname = ""
            info.gname = ""
            info.mtime = 0
            info.mode = entry.mode & 0o7777
            info.pax_headers = {}
            if entry.kind == "directory":
                if entry.data:
                    raise ValueError(f"directory entry has a body: {name}")
                info.type = tarfile.DIRTYPE
                info.size = 0
                tar.addfile(info)
            elif entry.kind == "file":
                info.type = tarfile.REGTYPE
                info.size = len(entry.data)
                tar.addfile(info, io.BytesIO(entry.data))
            else:
                raise ValueError(f"unsupported layer entry kind: {entry.kind}")
    result = stream.getvalue()
    if len(result) > _MAX_UNCOMPRESSED_LAYER:
        raise ValueError("uncompressed layer exceeds course safety limit")
    return result


def deterministic_gzip(data: bytes) -> bytes:
    if len(data) > _MAX_UNCOMPRESSED_LAYER:
        raise ValueError("uncompressed layer exceeds course safety limit")
    output = io.BytesIO()
    with gzip.GzipFile(fileobj=output, mode="wb", filename="", mtime=0) as gz:
        gz.write(data)
    compressed = output.getvalue()
    if len(compressed) > _MAX_COMPRESSED_LAYER:
        raise ValueError("compressed layer exceeds course safety limit")
    return compressed


def build_layer(entries: Iterable[LayerFile]) -> tuple[bytes, str, str]:
    tar_bytes = deterministic_tar(entries)
    compressed = deterministic_gzip(tar_bytes)
    return compressed, sha256_digest(compressed), sha256_digest(tar_bytes)


def _bounded_gzip_decompress(data: bytes) -> bytes:
    if len(data) > _MAX_COMPRESSED_LAYER:
        raise ValueError("compressed layer exceeds course safety limit")
    with gzip.GzipFile(fileobj=io.BytesIO(data), mode="rb") as gz:
        raw = gz.read(_MAX_UNCOMPRESSED_LAYER + 1)
    if len(raw) > _MAX_UNCOMPRESSED_LAYER:
        raise ValueError("uncompressed layer exceeds course safety limit")
    return raw


def _target(root: Path, member: str) -> Path:
    safe = _safe_path(member)
    resolved_root = root.resolve()
    candidate = resolved_root.joinpath(*PurePosixPath(safe).parts)

    # Following a pre-existing symlink while applying an archive would make
    # the archive writer act on a location it did not name. Reject every
    # symlink in the path, including the final entry when it already exists.
    current = resolved_root
    for part in PurePosixPath(safe).parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"layer path traverses a symlink: {member}")
    return candidate


def _remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink(missing_ok=True)
    elif path.is_dir():
        shutil.rmtree(path)


def _write_file_atomically(path: Path, data: bytes, mode: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.is_dir():
        shutil.rmtree(path)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".atlas-layer-", delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    try:
        temporary.chmod(mode & 0o7777)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def apply_layer(compressed: bytes, rootfs: Path) -> None:
    """Apply one constrained OCI-style tar+gzip layer.

    Whiteouts are processed in a first pass. This prevents archive member
    ordering from deleting files introduced by the same layer after an opaque
    marker. Only regular files and directories are accepted by this teaching
    profile; links, devices, sparse files, and special nodes are rejected.
    """

    rootfs.mkdir(parents=True, exist_ok=True)
    raw = _bounded_gzip_decompress(compressed)
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as tar:
        members = tar.getmembers()
        if len(members) > _MAX_MEMBERS:
            raise ValueError("layer contains too many entries")

        names: set[str] = set()
        validated: list[tuple[tarfile.TarInfo, str]] = []
        for member in members:
            name = _safe_path(member.name)
            if name in names:
                raise ValueError(f"duplicate layer entry: {name}")
            names.add(name)
            if member.size < 0 or member.size > _MAX_MEMBER_SIZE:
                raise ValueError(f"layer entry exceeds size limit: {name}")
            if not (member.isdir() or member.isfile()):
                raise ValueError(f"unsupported tar entry type for {name}")
            validated.append((member, name))

        # OCI whiteouts affect the lower rootfs. Process them before extracting
        # this layer's ordinary entries, independent of tar member order.
        for member, name in validated:
            base = PurePosixPath(name).name
            parent = PurePosixPath(name).parent
            if base == ".wh..wh..opq":
                if not member.isfile() or member.size != 0:
                    raise ValueError(f"opaque whiteout must be an empty regular file: {name}")
                directory = rootfs.resolve() if str(parent) == "." else _target(rootfs, str(parent))
                if directory.exists() and not directory.is_dir():
                    raise ValueError(f"opaque whiteout parent is not a directory: {name}")
                if directory.exists():
                    for child in list(directory.iterdir()):
                        _remove_path(child)
            elif base.startswith(".wh."):
                if not member.isfile() or member.size != 0:
                    raise ValueError(f"whiteout must be an empty regular file: {name}")
                victim_name = base[4:]
                if not victim_name or victim_name in {".", ".."}:
                    raise ValueError(f"invalid whiteout target: {name}")
                victim_path = parent / victim_name
                victim = _target(rootfs, str(victim_path))
                _remove_path(victim)

        for member, name in validated:
            base = PurePosixPath(name).name
            if base == ".wh..wh..opq" or base.startswith(".wh."):
                continue
            target = _target(rootfs, name)
            if member.isdir():
                if target.exists() and not target.is_dir():
                    _remove_path(target)
                target.mkdir(parents=True, exist_ok=True)
                target.chmod(member.mode & 0o7777)
            else:
                source = tar.extractfile(member)
                if source is None:
                    raise ValueError(f"missing body for {name}")
                data = source.read(_MAX_MEMBER_SIZE + 1)
                if len(data) != member.size:
                    raise ValueError(f"tar body size mismatch for {name}")
                _write_file_atomically(target, data, member.mode)


def entries_from_directory(source: Path) -> list[LayerFile]:
    source = source.resolve()
    entries: list[LayerFile] = []
    for path in sorted(source.rglob("*")):
        rel = path.relative_to(source).as_posix()
        st = path.lstat()
        if stat.S_ISLNK(st.st_mode):
            raise ValueError(f"symlinks are not accepted by this teaching builder: {rel}")
        if path.is_dir():
            entries.append(LayerFile(rel, mode=st.st_mode & 0o7777, kind="directory"))
        elif path.is_file():
            if st.st_size > _MAX_MEMBER_SIZE:
                raise ValueError(f"source file exceeds layer size limit: {rel}")
            entries.append(LayerFile(rel, path.read_bytes(), st.st_mode & 0o7777))
        else:
            raise ValueError(f"unsupported source entry type: {rel}")
    return entries
