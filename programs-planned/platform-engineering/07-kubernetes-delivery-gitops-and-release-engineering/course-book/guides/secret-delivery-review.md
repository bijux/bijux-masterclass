# Guide — Secret delivery review

A secret-delivery review follows the value from authority to use without writing the plaintext into the evidence bundle.

Document:

- source authority and secret version identity;
- decryption or retrieval identity;
- controller and namespace scope;
- plaintext locations and lifetime;
- Kubernetes projection method;
- workload reload behavior;
- overlap and revocation order;
- recovery and break-glass authority;
- logs, caches, and diff redaction.

Test a real rotation with synthetic values. A synchronized Secret or ExternalSecret is not enough; the workload must prove adoption of the new version before the old version is revoked. Scan Git history, rendered output, logs, and reports for the synthetic plaintext after cleanup.

## Extended reader notes

For each secret, draw the path from authoritative source through controller, Kubernetes representation or mount, process adoption, and predecessor revocation. Name every identity and audit source on the path. Decide how an outage at each step affects existing and new workloads.

Test rotation with overlapping validity. Confirm the new version appears, the workload actually uses it, and only then revoke the old version. Test decryption or source failure without deleting the last-known-good target. Verify repository scanning and controller log redaction.

Do not store real secrets in course evidence. Use synthetic versions and record identities, timestamps, and adoption outcomes rather than plaintext.
