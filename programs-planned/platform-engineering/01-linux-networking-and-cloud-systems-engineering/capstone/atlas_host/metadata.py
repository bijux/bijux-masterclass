from __future__ import annotations

import ipaddress
from dataclasses import dataclass
from urllib.parse import urlsplit


class MetadataPolicyError(ValueError):
    pass


@dataclass(frozen=True)
class MetadataEndpoint:
    provider: str
    url: str
    required_header: tuple[str, str] | None
    session_token_required: bool


PROFILES = {
    "aws": MetadataEndpoint("aws", "http://169.254.169.254/latest/", None, True),
    "gcp": MetadataEndpoint("gcp", "http://metadata.google.internal/computeMetadata/v1/", ("Metadata-Flavor", "Google"), False),
    "azure": MetadataEndpoint("azure", "http://169.254.169.254/metadata/instance", ("Metadata", "true"), False),
}


def validate_metadata_endpoint(endpoint: MetadataEndpoint) -> None:
    parsed = urlsplit(endpoint.url)
    if parsed.scheme != "http" or not parsed.hostname:
        raise MetadataPolicyError("metadata endpoint must be an explicit HTTP link-local endpoint")
    if parsed.username or parsed.password or parsed.fragment:
        raise MetadataPolicyError("metadata endpoint may not contain userinfo or fragment")
    if parsed.hostname == "metadata.google.internal":
        return
    try:
        address = ipaddress.ip_address(parsed.hostname)
    except ValueError as exc:
        raise MetadataPolicyError("unapproved metadata hostname") from exc
    if address != ipaddress.ip_address("169.254.169.254"):
        raise MetadataPolicyError("metadata endpoint must use the approved link-local address")
