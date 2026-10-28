# Runbook — TLS identity or rotation failure

1. Record transport address, SNI, expected hostname, and HTTP authority.
2. Inspect the complete certificate chain, SANs, validity, key usage, and trust root.
3. Confirm Gateway status reports the intended certificate reference resolved.
4. Distinguish frontend termination, passthrough, and backend re-encryption.
5. Test wrong-hostname and untrusted-issuer negative controls.
6. During rotation, test old/new overlap and eventual old-identity removal.
7. Never use disabled verification as evidence that the incident is repaired.
