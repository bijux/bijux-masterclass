# Production claims and evidence boundary

This course is a release-oriented educational reference. It does not claim to be an operated production build service, hardened container runtime, or production registry.

## Executed in the release environment

The published proof executed:

- controlled deterministic OCI-layout construction;
- complete digest propagation through layers, manifests, configurations, and indexes;
- safe archive-path validation, bounded extraction, whiteout application, and symlink-escape rejection;
- multi-architecture Go compilation and ELF-to-platform label verification;
- full reachable OCI graph validation, including descriptor size and digest checks;
- root-managed namespace and root-filesystem execution showing PID 1, UID/GID 65532, a read-only image root, writable bounded temporary/state paths, and deliberate cleanup;
- repository-scoped local distribution of blobs, manifests, tags, digests, and OCI referrers;
- rejection of unsafe repository names, cross-repository blob leakage, invalid uploads, and unlinked manifest dependencies;
- CycloneDX/VEX generation and deterministic vulnerability-policy checks;
- SLSA provenance generation, DSSE signing, payload-type validation, signature verification, and source/builder/subject policy;
- exact predecessor and successor handoff verification;
- accepted, review-required, not-executed, and deliberately rejected release decisions.

## What the executed proof does not establish

It is not equivalent to:

- OCI runtime or distribution conformance certification;
- a fully rootless runtime architecture;
- a hostile multi-tenant sandbox proof;
- a hardened BuildKit, Tekton, GitHub Actions, or cloud build service;
- native runtime execution on both advertised CPU architectures;
- a production trust root, Fulcio identity, Rekor inclusion proof, or operated Sigstore deployment;
- complete dependency discovery for arbitrary language ecosystems;
- vulnerability reachability proof from whole-program analysis;
- current public vulnerability intelligence—the checked database is a deterministic teaching fixture;
- representative container performance or capacity evidence;
- production registry authentication, retention, replication, garbage collection, key rotation, backup, or disaster recovery;
- Kubernetes admission enforcement, scheduling, networking, or storage behavior.

## Claim discipline

Every laboratory names:

1. the mechanism exercised;
2. the exact oracle;
3. the evidence produced;
4. the strongest supported claim;
5. the stronger claim that remains unproved.

A missing external environment is reported as `not-executed`, never converted into a synthetic pass.
