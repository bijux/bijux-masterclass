from __future__ import annotations

import re
from pathlib import Path

SENSITIVE_KEYS = {
    "password",
    "secret",
    "token",
    "api_key",
    "private_key",
    "client_secret",
}


def scan_repository(
    root: str | Path,
    forbidden_plaintexts: list[str] | None = None,
) -> list[str]:
    """Return bounded, high-signal secret-source findings.

    This is a course guard, not a replacement for a production secret scanner. It
    deliberately avoids treating schema words such as `kind: SecretStore` or
    metadata fields such as `secretKey` as secret values.
    """
    findings: list[str] = []
    forbidden = forbidden_plaintexts or []
    for path in Path(root).rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() not in {
            ".yaml",
            ".yml",
            ".json",
            ".md",
            ".txt",
            ".env",
        }:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for value in forbidden:
            if value and value in text:
                findings.append(f"{path}: contains forbidden plaintext")

        is_secret_resource = bool(
            path.suffix.lower() in {".yaml", ".yml"}
            and re.search(r"(?m)^\s*kind:\s*Secret\s*$", text)
        )
        if (
            is_secret_resource
            and re.search(r"(?m)^\s*(data|stringData):\s*$", text)
            and "ENC[" not in text
        ):
            findings.append(f"{path}: plaintext/base64 Kubernetes Secret source")

        if path.suffix.lower() in {".md", ".txt"}:
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            key = stripped.split(":", 1)[0].strip() if ":" in stripped else ""
            if key in {"apiVersion", "kind", "name", "namespace", "type"}:
                continue
            normalized = key.lower().replace("-", "_")
            if normalized not in SENSITIVE_KEYS:
                continue
            has_literal = re.search(r":\s*[^${}{\s][^\s]*", line)
            if (
                has_literal
                and "secretKeyRef" not in line
                and "remoteRef" not in line
                and "ENC[" not in line
                and "REDACTED" not in line
                and "example" not in str(path).lower()
            ):
                findings.append(
                    f"{path}:{line_number}: suspicious secret-like literal"
                )
    return sorted(set(findings))


def secret_version_event(
    name: str,
    version: str,
    adopted: bool,
    revoked_previous: bool,
) -> dict:
    return {
        "secret": name,
        "version": version,
        "adopted": adopted,
        "revokedPrevious": revoked_previous,
    }
