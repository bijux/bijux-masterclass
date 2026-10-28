from __future__ import annotations

from .models import Certificate, Decision


def _dns_match(pattern: str, hostname: str) -> bool:
    pattern = pattern.lower().rstrip(".")
    hostname = hostname.lower().rstrip(".")
    if pattern.startswith("*."):
        return hostname.endswith(pattern[1:]) and hostname.count(".") == pattern.count(".")
    return pattern == hostname


def select_certificate(
    certificates: list[Certificate],
    hostname: str,
    now: int,
) -> Decision:
    valid = [
        certificate
        for certificate in certificates
        if certificate.not_before <= now <= certificate.not_after
        and any(_dns_match(name, hostname) for name in certificate.dns_names)
    ]
    if not valid:
        return Decision(False, "NoValidCertificate", {"host": hostname})

    valid.sort(
        key=lambda certificate: (
            max(len(name) for name in certificate.dns_names),
            certificate.not_after,
        ),
        reverse=True,
    )
    return Decision(
        True,
        "CertificateSelected",
        {"certificate": valid[0]},
    )


def verify_backend(
    hostname: str,
    certificate: Certificate,
    trust_issuers: set[str],
    now: int,
) -> Decision:
    if certificate.issuer not in trust_issuers:
        return Decision(False, "UntrustedIssuer", {})
    if not certificate.not_before <= now <= certificate.not_after:
        return Decision(False, "CertificateTimeInvalid", {})
    if not any(_dns_match(name, hostname) for name in certificate.dns_names):
        return Decision(False, "HostnameMismatch", {})
    return Decision(
        True,
        "Verified",
        {"host": hostname, "certificate": certificate.name},
    )
