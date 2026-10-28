# Worked walkthrough — Atlas Workload Release 1.0

This walkthrough follows one API release through every identity boundary. It is deliberately more detailed than a tool tutorial because most serious mistakes occur when evidence from one phase is used to authorize another.

## 1. Freeze the predecessor contract

Course 2 already decided that Atlas API:

- listens on port 8080 behind an edge;
- runs as non-root, separately from the worker;
- writes durable spool/results only under `/var/lib/atlas`;
- receives configuration and secrets at runtime;
- must stop within thirty seconds;
- uses workload identity rather than static cloud keys.

Container packaging may express these requirements but may not weaken them. The first proof is therefore the exact predecessor manifest, not a Containerfile build.

## 2. Identify source and build materials

The checked source digest covers the Go module, API/worker/probe source, Containerfiles, ignore file, and base-image lock. The release record also names compiler/toolchain and base subjects. A git tag alone is insufficient because untracked context, generated files, submodules, or mutable materials can influence output.

The build graph has three outputs:

```text
atlas-api       deployable
atlas-worker    deployable
atlas-probe     verification-only
```

Each is cross-compiled for `linux/amd64` and `linux/arm64`. `CGO_ENABLED=0`, `-trimpath`, empty build ID, stable file metadata, and deterministic tar/gzip encoding narrow the controlled-rebuild experiment. They do not prove a compromised compiler could not emit malicious bytes.

## 3. Build one platform-specific image

For `atlas-api/linux/amd64`, the semantic builder:

1. compiles the binary;
2. verifies ELF `EM_X86_64` against the intended architecture;
3. creates a deterministic layer containing directories, binary, and release marker;
4. computes compressed layer digest and uncompressed DiffID;
5. writes the OCI image configuration with entrypoint, user, labels, history, and DiffID;
6. writes the image manifest referencing config and layer descriptors.

At this point there are already three different identities:

```text
compressed layer digest
configuration digest
platform manifest digest
```

The platform manifest is the deployable subject for a runtime that selects exactly this architecture. None of the three is interchangeable.

## 4. Build the image index

The amd64 and arm64 manifest descriptors are placed into an OCI image index with platform fields. The index digest becomes the release-level image identity. The executable architecture check prevents the index from merely asserting a label.

Adding another platform later does not preserve this digest. Even unchanged child manifests now appear in a different index byte sequence. Evidence attached to the old index must not be silently reused for the new one.

## 5. Inspect the graph before distribution

The reviewer traverses from index to every child, verifies descriptor size/digest/media type, parses configuration, recomputes layer DiffIDs, applies layer changes in order, and confirms the configured entrypoint exists. Historical layers are scanned separately for fixture secrets and prohibited content.

The controlled rebuild repeats the entire API build under the same semantic builder/toolchain and compares the top-level digest. Equality supports a bounded determinism claim. It does not support “all conforming builders will reproduce these bytes.”

## 6. Publish to the course registry

Blobs are uploaded before manifests. Platform manifests are published by digest, then the index by digest, then the discovery tag `1.0.0`. Pull verification uses the digest. The tag exists for humans and tooling that need discovery; it is not placed in the authority chain.

The loopback course registry implements a bounded Distribution subset. It demonstrates blob/manifest/tag/digest/referrer mechanics, not production authentication, replication, retention, garbage collection, or disaster recovery.

## 7. Produce subject-bound inventory and origin evidence

For each deployable image index:

- a CycloneDX 1.7 course-profile SBOM identifies Atlas and controlled dependency fixtures;
- vulnerability matching uses a deterministic course database;
- VEX provides one bounded applicability decision;
- an in-toto/SLSA-shaped provenance statement names the image subject, source digest, builder ID, build type, parameters, and materials;
- a DSSE envelope is signed by a public deterministic course key.

The key proves the signing and verification mechanism only. Because the private fixture is distributed with the course, it provides no production identity assurance.

Each evidence object is published as a referrer to the exact image subject. The verifier rejects valid evidence for a previous digest.

## 8. Evaluate release policy in dependency order

Policy checks identity and object integrity before signatures or vulnerability findings. The order is important:

```text
immutable subject
→ complete graph
→ required platforms
→ runtime contract
→ secret/build checks
→ inventory/risk
→ provenance/signature/builder authorization
→ promotion evidence
```

A clean scan cannot compensate for a mutable tag. A valid signature cannot compensate for the wrong subject. An average score cannot compensate for UID 0 or missing platform evidence.

The API and worker pass the dependency-light policy. The probe is verification-only and is excluded from default deployment.

## 9. Execute the bounded runtime proof

The probe image is unpacked into a bundle. The checked mini-runtime creates private namespaces, maps UID/GID 65532, presents a read-only root, mounts writable temporary/state paths, and executes the probe as PID 1. The probe reports:

- UID/GID 65532;
- PID 1;
- expected hostname;
- `/etc` not writable;
- `/tmp` and `/var/lib/atlas` writable.

The harness is host-root-managed in the build environment. The evidence supports the effective workload mapping and mount behavior, not a fully rootless daemon/runtime architecture or hostile multi-tenant sandbox.

## 10. Authorize and hand off

The accepted release record selects exact API and worker index digests, source digest, platform sets, runtime user/entrypoint, evidence objects, signer fingerprint, and evidence class. It also records what remains unexecuted.

Course 4 receives:

- immutable image identities;
- ports and process roles;
- health and termination semantics;
- durable/ephemeral/configuration mount classes;
- runtime security profile;
- resource hypotheses;
- supply-chain verification policy;
- known risks.

It does not receive pre-written Kubernetes manifests. The next course must learn reconciliation and workload APIs while preserving the contract.

## Final review question

At every arrow in the walkthrough, ask:

> Did the next phase consume the exact subject and guarantees produced by the previous phase, or did it substitute a tag, a default, a claim from another platform, or evidence for another digest?

That question is the shortest reliable audit of a workload-release pipeline.
