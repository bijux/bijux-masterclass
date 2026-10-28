# Capstone evidence map

| Claim | Primary object/oracle | Strongest local conclusion | Not proved locally |
|---|---|---|---|
| Course 2 continuity | predecessor manifest and byte verification | Packaging consumes the exact 13-file handoff | Course 2 cloud resources are currently operated |
| Source identity | deterministic source-tree digest | Checked source inputs did not change within the tour | Git review/protected branch or external source transparency |
| Exact image bytes | descriptor size/digest verification | Every checked OCI edge names the bytes retrieved | Independent OCI implementation conformance |
| Filesystem result | layer digest, DiffID, safe ordered reconstruction | Merged rootfs follows checked changesets/whiteouts | Every overlay/snapshotter implementation behaves identically under all edge cases |
| Controlled rebuild | repeated semantic build and equal index digest | Same controlled inputs/toolchain/implementation reproduced bytes | Reproducibility across independent builders or compromised-toolchain resistance |
| Platform truth | ELF machine inspection for amd64/arm64 | Entrypoint machine identity agrees with descriptor | Native behavior, ABI/kernel/CPU-feature compatibility on every target |
| Registry transport | loopback push/pull/tag/digest/referrer trace | Distribution mechanics preserve checked content and subject relationships | Production auth, retention, replication, GC, availability, DR |
| Runtime identity and mounts | Atlas probe output in bounded harness | PID 1, UID/GID 65532, read-only `/etc`, writable tmp/state under harness | Full rootless daemon, OCI conformance, seccomp/LSM, hostile sandbox safety |
| Inventory | CycloneDX course fixture and completeness assertions | Required controlled components are subject-bound | Complete arbitrary-ecosystem discovery |
| Vulnerability/VEX | deterministic database/findings/VEX policy | Policy classification mechanism works for fixtures | Current real-world vulnerability intelligence or whole-program reachability |
| Build origin | in-toto/SLSA-shaped provenance | Statement fields, subject, materials, builder, and policy mechanics work | Operated builder isolation or trustworthy external identity |
| Signer identity | DSSE Ed25519 verification and fingerprint policy | Exact bytes are authenticated by the fixture key | Production key secrecy, Fulcio/Rekor, HSM, rotation operations |
| Release authorization | categorical policy report and rejected candidates | Non-compensable gates compose correctly in the course profile | Production organizational approval or target admission enforcement |
| Course 4 continuity | successor handoff manifest | Exact image/runtime/storage/health/evidence contracts are exported | Kubernetes implementation or admission behavior |

## Evidence use rule

A conclusion may be no stronger than its weakest required evidence class. For example, the checked release can be accepted for the educational Course 4 handoff while production-registry and operated-signing evidence remains `not-executed`. It cannot be called production-deployed or production-proven.
