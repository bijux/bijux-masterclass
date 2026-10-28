from __future__ import annotations

import ipaddress
import json
import ssl
import subprocess
from pathlib import Path


def openssl_text(path: Path) -> str:
    return subprocess.run(
        ["openssl", "x509", "-in", str(path), "-noout", "-text"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout


def main() -> int:
    cap = Path(__file__).resolve().parents[1]
    cert = cap / "pki" / "atlas.crt"
    ca = cap / "pki" / "ca.crt"
    decoded = ssl._ssl._test_decode_cert(str(cert))  # type: ignore[attr-defined]
    sans: set[str] = set()
    for kind, value in decoded.get("subjectAltName", []):
        if kind == "DNS":
            sans.add(value)
        elif kind == "IP Address":
            sans.add(str(ipaddress.ip_address(value)))
    required = {"atlas.test", "localhost", "127.0.0.1", "::1"}
    missing = sorted(required - sans)
    if missing:
        raise SystemExit(f"certificate SANs missing: {missing}")

    leaf_text = openssl_text(cert)
    ca_text = openssl_text(ca)
    if "CA:FALSE" not in leaf_text or "TLS Web Server Authentication" not in leaf_text:
        raise SystemExit("leaf certificate lacks server constraints")
    if "CA:TRUE" not in ca_text or "Certificate Sign" not in ca_text:
        raise SystemExit("fixture CA lacks CA constraints")

    subprocess.run(
        ["openssl", "verify", "-CAfile", str(ca), "-verify_hostname", "atlas.test", str(cert)],
        check=True,
        capture_output=True,
        text=True,
    )
    context = ssl.create_default_context(cafile=str(ca))
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    report = {
        "subjectAltNames": sorted(sans),
        "courseMinimumTls": context.minimum_version.name,
        "caLoaded": True,
        "fixtureOnly": True,
    }
    target = cap / "reports" / "pki.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
