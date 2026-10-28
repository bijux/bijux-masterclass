from __future__ import annotations

import struct
from typing import Any

_ELF_MACHINE = {
    62: "amd64",
    183: "arm64",
}


def elf_architecture(data: bytes) -> str:
    if len(data) < 20 or data[:4] != b"\x7fELF":
        raise ValueError("payload is not an ELF executable")
    endian = data[5]
    fmt = "<H" if endian == 1 else ">H" if endian == 2 else None
    if fmt is None:
        raise ValueError("unsupported ELF byte order")
    machine = struct.unpack_from(fmt, data, 18)[0]
    try:
        return _ELF_MACHINE[machine]
    except KeyError as exc:
        raise ValueError(f"unsupported ELF machine: {machine}") from exc


def verify_platform_label(binary: bytes, architecture: str) -> None:
    actual = elf_architecture(binary)
    if actual != architecture:
        raise ValueError(
            f"platform label mismatch: manifest says {architecture}, binary is {actual}"
        )


def select_manifest(index: dict[str, Any], os_name: str, architecture: str, variant: str | None = None) -> dict[str, Any]:
    matches = []
    for descriptor in index.get("manifests", []):
        platform = descriptor.get("platform", {})
        if platform.get("os") != os_name or platform.get("architecture") != architecture:
            continue
        if variant is not None and platform.get("variant") != variant:
            continue
        matches.append(descriptor)
    if len(matches) != 1:
        raise ValueError(f"expected one platform match, found {len(matches)}")
    return matches[0]
