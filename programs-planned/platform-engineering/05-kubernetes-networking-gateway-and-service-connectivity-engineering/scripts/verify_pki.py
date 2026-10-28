#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess

from common import ROOT, fail

pki = ROOT / "capstone" / "pki"
for key in [pki / "ca.key", pki / "atlas.key"]:
    if key.stat().st_mode & 0o077:
        fail(f"private fixture mode too broad: {key.relative_to(ROOT)}")

verify = subprocess.run(
    ["openssl", "verify", "-CAfile", str(pki / "ca.crt"), str(pki / "atlas.crt")],
    capture_output=True,
    text=True,
    check=False,
)
if verify.returncode:
    fail(f"PKI chain verification failed: {verify.stderr.strip()}")

host = subprocess.run(
    [
        "openssl",
        "verify",
        "-CAfile",
        str(pki / "ca.crt"),
        "-verify_hostname",
        "atlas.test",
        str(pki / "atlas.crt"),
    ],
    capture_output=True,
    text=True,
    check=False,
)
if host.returncode:
    fail(f"PKI hostname verification failed: {host.stderr.strip()}")
print("PASS local PKI chain, hostname, and private-fixture modes")
