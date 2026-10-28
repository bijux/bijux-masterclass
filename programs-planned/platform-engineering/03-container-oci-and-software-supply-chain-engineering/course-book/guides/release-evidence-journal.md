# Release evidence journal

Keep one journal entry per candidate subject. The journal is not a pasted CI log; it is an index into evidence that makes the release decision reproducible.

## Candidate identity

Record source repository/revision/digest, build invocation, image repositories, index/manifest digests, discovery tags, and intended environment. Never allow a tag-only entry.

## Build evidence

Record builder identity/version, build type/frontend, target platforms, base/toolchain/material digests, network/cache/secret policy, controlled-rebuild conditions, and output digests. State whether builds were native, cross, or emulated.

## Runtime evidence

Record runtime/version, effective configuration profile, host/kernel/architecture, UID/GID/capabilities, namespaces, mounts, resource settings, signal/exit behavior, and cleanup. Distinguish semantic harness evidence from independent OCI/native runtime evidence.

## Supply-chain evidence

For every image subject, link SBOM, completeness comparison, vulnerability database/time, findings, VEX/license dispositions, provenance envelope, signer/builder/source authorization, and referrer records.

## Decision

Use categorical results:

```text
accepted
rejected
review-required
not-executed
```

List the first failed non-compensable gate, exception scope/owner/expiry if any, rollback subjects, and residual risk. A green total score must never hide an identity or authority failure.

## Evidence boundary

Finish with two sentences:

1. the strongest claim supported by the entry;
2. the nearest stronger claim that remains unproved.

Example: “The Atlas probe executed under the checked namespace/mount profile as UID/GID 65532 with a read-only root. This does not prove a fully rootless OCI runtime, maintained seccomp/LSM enforcement, or safety for hostile multi-tenant code.”
