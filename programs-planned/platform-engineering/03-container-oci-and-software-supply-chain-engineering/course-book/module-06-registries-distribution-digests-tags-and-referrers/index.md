# Module 6 — Registries, distribution, digests, tags, and referrers

A registry is a content distribution service, not a release authority. It stores blobs and manifests, resolves repository references, applies authentication and retention rules, and may expose subject referrers. It does not know whether a runnable image is secure, whether provenance is trusted, or whether a tag was approved.

This module separates transport from promotion.

## Learning outcomes

By the end of the module you can:

- explain repository, blob, manifest, tag, and digest identities;
- trace OCI Distribution push and pull flows;
- distinguish blob deduplication from repository authorization;
- reason about content negotiation and accepted media types;
- use subject/referrer relationships for evidence discovery;
- design immutable promotion and retention policy;
- analyze tag races, deletion, garbage collection, and mirror behavior;
- implement a bounded registry client/server flow and verify every transferred object.

## Repository names organize access; digests identify bytes

A reference can look like:

```text
registry.example.com/atlas/api:1.0
registry.example.com/atlas/api@sha256:<digest>
```

The repository name is an authorization and organization boundary. The tag is a mutable name within that repository. The digest is immutable byte identity for the selected manifest or index.

Release systems should promote by digest. Tags can be updated as human-facing pointers after the digest has been approved. Consumers that require immutability should resolve or deploy by digest.

A tag-to-digest record is useful evidence, but it must be captured at a specific time and cannot make the tag immutable retroactively.

## Blob upload flow

A simplified push sequence is:

1. check whether a blob already exists;
2. initiate upload;
3. send chunks or complete monolithically;
4. commit with the expected digest;
5. push child manifests after referenced blobs exist;
6. push the image index after platform manifests exist;
7. optionally attach evidence manifests and tags.

Registries verify content digests at commit. Clients should still verify downloaded content; transport success does not replace end-to-end integrity.

Blob existence and cross-repository mounts can avoid duplicate transfer. Authorization must prevent a caller from learning or mounting content across repositories in ways policy forbids.

## Pull flow and content negotiation

A client requests a manifest by tag or digest and advertises accepted media types. The registry returns bytes and a content type. The client verifies the response digest and parses according to the selected media type.

If a client fails to advertise index support, a registry or compatibility layer may return a different manifest representation. Record what bytes were actually received. Do not assume that requesting a tag always yields the same media type across clients.

Atlas release verification accepts the OCI index, manifest, config, layer, and artifact media types defined by its profile. Unexpected media types fail closed rather than being parsed optimistically.

## Deduplication and authorization are different

Content-addressed blobs may be physically stored once while referenced by many repositories. Logical repository access still matters.

A user authorized to pull `team-a/app` should not automatically gain permission to enumerate every repository that references the same blob. Conversely, a blob digest can reveal content existence even when no authorized manifest is visible, depending on registry policy.

Treat registry access as:

```text
repository-level subject authorization
+ manifest/reference authorization
+ blob fetch authorization
+ administration/retention authority
```

## Referrers bind evidence to subjects

The referrers API can enumerate manifests whose `subject` points to a given digest. This supports discoverable SBOMs, provenance, signatures, vulnerability reports, and other OCI artifacts.

Discovery is not verification. For each referrer:

1. verify its descriptor;
2. parse its artifact type/media type;
3. confirm its subject digest equals the candidate;
4. verify evidence-specific signatures/schema/policy;
5. reject stale evidence attached to another digest.

A malicious registry can omit a referrer, return an incomplete list, or serve stale metadata unless the client has stronger transparency/replication guarantees. Evidence availability and evidence authenticity are separate.

## Tags are mutable by design

Tags support workflows such as:

```text
build-20260809
candidate
staging
production
```

The risk is treating a tag as if it were the approved object. Between review and deployment, another actor can move it.

Safe promotion records:

```text
approved digest
source release decision
registry/repository
optional tags to update
actor and time
post-update tag resolution
```

Deployment manifests should retain the approved digest. A `production` tag can help humans, but it does not replace the digest.

Immutability policies can reject tag overwrite, but verify the exact registry behavior. Some systems enforce immutability per repository or pattern; some allow administrators to bypass it.

## Deletion and garbage collection

Deleting a tag removes one reference. The manifest and blobs may remain reachable through other tags, digests, referrers, caches, mirrors, or retention windows.

Deleting a manifest can orphan blobs. Garbage collection decides when unreferenced content is physically removed. Running GC concurrently with uploads or replication can corrupt availability if the registry implementation does not coordinate it safely.

Supply-chain retention often conflicts with aggressive storage cleanup. Reproducibility and incident response may require retaining:

- released image manifests/indexes;
- evidence artifacts;
- source/material metadata;
- revoked artifacts for forensics;
- previous deployable versions for rollback.

Retention policy should be release-aware, not only “delete untagged after seven days.”

## Mirrors, proxies, and caches

A registry mirror can reduce latency and external dependency. It also creates questions:

- Does it preserve exact digests and media types?
- How are upstream credentials scoped?
- Can it serve stale tag resolution?
- Is signature/referrer metadata mirrored?
- What happens when upstream deletes content?
- Is the mirror a trusted distribution source or only a cache?

Digest pulls make stale content detectable: the bytes either match or fail. Tag pulls can silently return an older or newer digest according to cache behavior.

## Registry compromise and digest guarantees

If a registry is compromised, an attacker cannot replace bytes under an existing cryptographic digest without breaking the digest assumption. They can:

- move tags;
- delete content;
- deny service;
- add malicious new manifests/tags;
- hide or add referrers;
- alter authorization;
- serve malformed responses;
- target clients that fail digest verification.

Signatures and provenance help decide which new digest to trust. Replication and retention help availability. No single mechanism solves all compromise outcomes.

## Worked case: tag moved after approval

A release reviewer approves:

```text
atlas/api:candidate -> sha256:AAA
```

The deployment job later executes:

```text
pull atlas/api:candidate
```

Between those events, another pipeline moves the tag to `sha256:BBB`. The deployment succeeds and runs unreviewed bytes.

Correct workflow:

1. resolve the tag during candidate creation;
2. verify `sha256:AAA` and all attached evidence;
3. record approval for `sha256:AAA`;
4. deploy `atlas/api@sha256:AAA`;
5. optionally update `production` to point to AAA;
6. verify tag update as separate convenience metadata.

The approval object never says “whatever candidate means later.”

## The course registry

The capstone includes a minimal loopback Distribution API implementation supporting:

- `/v2/` ping;
- blob upload/commit and retrieval;
- manifest push/get by tag or digest;
- tag resolution;
- subject referrers;
- digest and size verification.

It is intentionally not a production registry. It omits robust authentication, resumable production uploads, storage replication, garbage-collection coordination, quotas, and hardened HTTP serving. Its value is that the protocol and content identities are visible.

The native lane can use an OCI-compatible registry and tools such as `oras` or `skopeo` for independent evidence.

## Atlas capstone increment

You will push the three Atlas indexes and attached SBOM/provenance artifacts to the local registry. Then you will:

- pull by digest and verify exact objects;
- resolve a tag and record the mapping;
- move the tag and prove digest deployment is unaffected;
- enumerate referrers for the approved subject;
- simulate deletion/retention decisions;
- reject an evidence artifact bound to the wrong subject;
- document repository and administrative authority.

The output is a distribution record, not yet a release authorization.

## Registry review questions

1. Which repository contains the subject?
2. What exact digest is approved?
3. Which mutable names point to it now?
4. Which media types will clients accept?
5. Are all child blobs present and verified?
6. Which referrers exist, and are they complete enough for policy?
7. Who can push, retag, delete, administer, and run GC?
8. What is retained for rollback and forensics?
9. Which mirrors/caches can affect resolution?
10. Can the consumer operate by digest throughout?


## End-to-end push and pull trace

A client that pushes an image graph should proceed from leaves to roots:

```text
layer/config blobs
      ↓
platform manifests
      ↓
image index
      ↓
optional tag assignment
      ↓
subject-bound referrer artifacts
```

Before upload, compute the digest locally. After upload, verify the registry’s canonical digest header where available. Uploading a root manifest before all referenced blobs exist can create an unusable graph or be rejected depending on registry policy.

A pulling client resolves a tag only once, records the returned digest, then continues by digest. It verifies every response body. A tag may move between two GET requests; using it repeatedly within one release operation creates a mixed graph.

## Authentication and authorization boundaries

Registry authentication establishes a principal. Authorization should be scoped by repository and action, commonly `pull`, `push`, or administrative operations. Review:

- whether blob mounts permit cross-repository information leaks;
- whether a principal that can push blobs can also retarget protected tags;
- whether referrer artifacts require the same or different authority;
- whether deletion and garbage collection are separately controlled;
- whether CI credentials can overwrite production discovery references;
- whether anonymous pulls expose sensitive private artifacts.

Content addressing does not make unauthorized publication harmless. An attacker can upload a malicious but internally consistent graph. Trust policy must constrain source, builder, signer, and release authority.

## Cross-repository mounts and deduplication

Registries may mount an existing blob into another repository without re-upload. This saves bandwidth but introduces policy questions: can the caller prove pull access to the source and push access to the target? Does the mount leak that a digest exists? Is the blob retained if the source repository is deleted?

Global blob storage is an implementation detail. Repository-level authorization and manifest reachability remain the logical contract.

## Referrer discovery and subject verification

A referrers response is an index-like list of descriptors whose manifests claim the requested subject. The client must still pull each artifact manifest, verify its digest, and confirm that its `subject` equals the intended image/index digest. Artifact type and annotations help discovery but do not authorize the statement.

Fallback conventions may be needed for registries without the referrers API. The course profiles native referrers and records compatibility gaps rather than hiding them behind a tool.

## Retention as graph reachability plus policy

Garbage collection should start from protected roots:

- active releases;
- approved rollback releases;
- incident/forensic holds;
- evidence artifacts and their subjects;
- in-progress uploads according to timeout policy.

Traverse every referenced blob and referrer relationship. A registry can retain an image but delete its SBOM or provenance if evidence roots are not included. Conversely, retaining every historical upload forever creates cost and exposure. Policy needs ownership, retention periods, legal/incident holds, and a tested restore path.

## Failure matrix

| Symptom | First evidence |
|---|---|
| `MANIFEST_UNKNOWN` | repository, reference, auth scope, tag/digest resolution |
| blob 404 | manifest descriptor, upload completion, GC logs |
| digest mismatch | exact response bytes and expected descriptor |
| wrong platform pulled | index content, client platform matcher, accepted media types |
| missing attestations | subject digest, referrers capability, fallback repository |
| tag points elsewhere | protected-tag audit and release’s recorded digest |
| pull works in one site only | mirror freshness, proxy cache, regional replication |

Atlas’s local registry implements a transparent subset for these flows. It is not used to claim production registry durability, authentication, or conformance.

## A registry has two consistency models at once

Blobs and digest-addressed manifests are immutable by identity. Tags are mutable repository metadata. A deployment that resolves a tag at two different times can receive two different manifests while both requests succeed.

Use the tag for discovery and the digest for authorization:

```text
human intent:     atlas-api:1.0.0
resolved subject: platform/atlas-api@sha256:6e3b…
promotion record: exact digest plus evidence decision
runtime input:    exact digest
```

If a tag moves after approval, the approval remains attached to the digest, not to the tag string.

### Upload and publication are multi-step protocols

A registry upload can create temporary state before the final digest is known. The final request binds bytes to a digest and should reject a mismatch. Manifest publication should verify that referenced blobs exist and are linked to the repository policy context. Course registry tests reject unknown upload IDs, unsafe repository names, unlinked dependencies, and cross-repository blob reads.

A real registry adds authentication, authorization scopes, quotas, concurrent upload recovery, garbage collection, replication, and failure recovery. Those are explicitly outside the local subset.

### Referrers make evidence discoverable, not trustworthy

An OCI artifact manifest can identify a subject digest and carry an artifact type such as an SBOM or provenance statement. The referrers API answers “which descriptors claim this subject?” It does not answer:

- whether the signature is valid;
- whether the signer is trusted;
- whether the payload type is allowed;
- whether the statement subject actually matches policy;
- whether evidence is fresh and complete;
- whether a conflicting referrer should be preferred.

Discovery precedes verification. The Course 3 registry returns two referrers for each deployable Atlas image; release policy still verifies the payload and trust rules.

### Garbage collection is a release-governance concern

A blob can be unreachable from current tags but still be required by:

- a deployed digest;
- a rollback window;
- a retained provenance subject;
- a forensic investigation;
- a legal or audit hold;
- another repository link.

Define roots from active releases, rollback policy, referrers, and retention records before deletion. A tag list is not a complete reachability graph. Production registry garbage collection therefore belongs to an owned runbook with restore evidence, not an ad hoc disk-cleanup command.

## Continue

- [Exercises](exercises.md)
- [Worked answers](exercise-answers.md)
- [Laboratory](lab.md)
- [Checkpoint](checkpoint.md)
- [Previous stage](../module-05-multi-platform-images-abi-and-architecture-truth/index.md)
- [Next stage](../module-07-runtime-hardening-resource-control-and-operational-contracts/index.md)
