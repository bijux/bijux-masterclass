from __future__ import annotations

import base64
import re
from typing import Any


SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)(password|secret|token|private[_-]?key)\s*[=:]\s*[^\s]+"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]


class ComputeError(ValueError):
    pass


def decode_user_data(value: str, *, encoded: bool = False) -> str:
    if not encoded:
        return value
    try:
        return base64.b64decode(value, validate=True).decode("utf-8")
    except Exception as exc:
        raise ComputeError(f"invalid base64 user data: {exc}") from exc


def validate_image_release(image: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in ("imageId", "architecture", "sourceDigest", "buildIdentity", "testReport"):
        if not image.get(key):
            errors.append(f"image release missing {key}")
    if image.get("architecture") not in {"amd64", "arm64"}:
        errors.append("image architecture must be amd64 or arm64")
    if image.get("mutableAlias") in {"latest", "current"}:
        errors.append("image release must not depend on a mutable alias")
    return errors


def validate_launch_contract(launch: dict[str, Any], image: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if launch.get("imageId") != image.get("imageId"):
        errors.append("launch image does not match approved image release")
    if launch.get("architecture") != image.get("architecture"):
        errors.append("launch and image architectures differ")
    metadata = launch.get("metadataOptions", {})
    if metadata.get("httpTokens") != "required":
        errors.append("IMDSv2 tokens must be required")
    if int(metadata.get("httpPutResponseHopLimit", 0)) not in {1, 2}:
        errors.append("metadata hop limit must be explicitly 1 or 2")
    if launch.get("publicIp"):
        errors.append("Atlas workload host must not have a public IP")
    if not launch.get("instanceProfile"):
        errors.append("instance profile is required")
    if not launch.get("privateSubnet"):
        errors.append("private subnet is required")
    user_data = decode_user_data(str(launch.get("userData", "")), encoded=bool(launch.get("userDataBase64")))
    for pattern in SECRET_PATTERNS:
        if pattern.search(user_data):
            errors.append("user data contains secret-like material")
            break
    if "latest" in user_data.lower() and ("curl" in user_data.lower() or "wget" in user_data.lower()):
        errors.append("bootstrap downloads a mutable latest artifact")
    if launch.get("rootIsDurableAuthority"):
        errors.append("root volume must not own durable Atlas results")
    if not launch.get("dataVolume", {}).get("encrypted"):
        errors.append("durable data volume must be encrypted")
    return errors


def replacement_capacity(
    *,
    current_instances: int,
    desired_instances: int,
    create_before_destroy: bool,
    quota: int,
) -> dict[str, Any]:
    peak = desired_instances + (current_instances if create_before_destroy else 0)
    return {
        "current": current_instances,
        "desired": desired_instances,
        "peakRequired": peak,
        "quota": quota,
        "sufficient": peak <= quota,
    }
