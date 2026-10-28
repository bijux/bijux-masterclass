---
module_id: PLAT-032
program: Platform Engineering
level: 1
module_number: 32
title: Artifact and Image Management
status: complete
last_verified: 2026-09-02
---

# Artifact and Image Management

## One-Page Review

### Governing question

How should a platform identify, publish, discover, verify, distribute, assess, retain, quarantine, and delete immutable software artifacts without confusing mutable names, metadata, or yesterday's scan result with the bytes consumers execute?

### Essential definitions

- An **artifact** is immutable content intended for a consumer, such as an OCI image, package, chart, archive, binary, SBOM, or attestation.
- A **descriptor** identifies content by media type, byte size, and digest; it is the secure edge in the OCI content graph.
- A **manifest** describes one artifact composition, including configuration and layers; an **image index** points to multiple manifests, commonly for platforms.
- A **digest** is a collision-resistant content identifier calculated from bytes; a **tag** is a mutable human-readable pointer to a manifest.
- A **repository** is a named registry namespace containing manifests, blobs, tags, and associated artifacts.
- A **referrer** is an OCI manifest whose subject points to another manifest digest, enabling discovery of signatures, SBOMs, and attestations.
- **Promotion** changes an accepted digest's release/channel association without rebuilding its bytes.
- **Retention** decides how long named and referenced objects remain recoverable; **garbage collection** removes unreferenced storage blobs.
- **Quarantine** denies new use while preserving content and evidence for investigation or controlled recovery.
- **Revocation** changes a trust or authorization decision; it does not change an immutable artifact's digest.

### Central model, mechanism, or theorem

Treat the registry as a content graph $G=(V,E)$ plus mutable naming relation $T$. Each vertex $v\in V$ is immutable content with descriptor $(m,s,d)$ for media type, size, and digest. Each edge $u\to v$ is a digest-bound reference from an index, manifest, or subject relationship. Tags form $T:n\mapsto d$ and may change. A lifecycle decision must operate on the transitive content/evidence graph rooted at retained digests, not on tags alone. Consumer acceptance combines content integrity, platform compatibility, evidence authenticity, policy, and current authorization.

### Critical invariants

- Digests, not tags, are authoritative identities for publication, promotion, deployment, rollback, evidence, and incident response.
- Every descriptor's media type, size, and digest are verified before content is trusted or deeply processed.
- Multi-platform indexes and their selected manifests have distinct identities; evidence policy states which subjects it covers.
- Signatures, provenance, SBOMs, scan reports, and release decisions bind to exact subjects and remain discoverable with those subjects.
- Repository write, tag mutation, deletion, replication, policy, and administrative privileges are separate and least-privileged.
- Required evidence and acceptance policy are verified at promotion and consequential consumption, not merely generated at build time.
- Vulnerability state is time-varying; immutable bytes require repeated assessment and owned remediation decisions.
- Retention marks the complete reachable artifact/evidence/release graph before deletion; garbage collection never races active publication.
- Replicas verify content identity and expose measurable freshness; replication is neither backup nor automatic trust transfer.
- Quarantine, revocation, rollback, legal hold, recovery, and final deletion have explicit owners and audit trails.

### Common failures

Deploying mutable tags; signing a tag rather than its resolved digest; overwriting release tags without history; assuming image layers are private because a repository is private; scanning only on push; deleting a subject while retaining ambiguous evidence; garbage-collecting during writes; retaining tags but not referenced manifests; treating replication as backup; granting build jobs repository delete; using one shared pull secret everywhere; accepting any valid signer; ignoring index-versus-manifest subjects; allowing unsupported media-type conversion; and deleting a compromised artifact before preserving evidence.

### Compact example

A build publishes an amd64 manifest $d_a$, an arm64 manifest $d_b$, and index $d_i$ referencing both. The registry stores immutable release tags that resolve to $d_i$, plus signed provenance and SPDX referrers for $d_i$ and platform-specific scan attestations for $d_a,d_b$. Promotion verifies the index signature, allowed builder/materials, both platform policies, and current vulnerability exceptions before assigning the production channel to $d_i$. Deployments record $d_i$ and runtime-observed selected manifest. A critical base-image advisory later quarantines all three digests, preserves their graph/evidence, blocks new admission, maps deployments, and promotes a rebuilt index only after verification.

### Connections

This module consumes immutable build outputs and evidence from [PLAT-031](031-application-build-capability.md), container artifact semantics from [PLAT-021](021-container-images-as-platform-artifacts.md), and runtime selection from [PLAT-030](030-mapping-application-needs-to-kubernetes-primitives.md). It supplies governed artifact identities to PLAT-034 deployment capability and later release, security, observability, and incident-response capabilities.

## Governing Question

What lifecycle and control model lets humans use convenient names while every automated decision remains bound to immutable content, verified evidence, compatible platforms, current policy, and recoverable history?

An artifact repository is not just a file server. Content-addressed objects form graphs: an image index points to manifests; manifests point to configuration and layers; evidence manifests point back to subjects. Names, channels, policies, scan databases, ownership, and deployment state change around immutable vertices.

Management therefore spans two kinds of state. Content identity is immutable. Operational interpretation is mutable: a digest may move from candidate to approved, then quarantined, then retired without changing one byte. Good platforms preserve that distinction in APIs, schemas, permissions, dashboards, and incident procedures.

## Why This Matters

Artifacts are the handoff between building and running. If that handoff is ambiguous, a tested object can differ from the deployed one, an SBOM can describe the wrong image, a rollback can select an overwritten tag, or a deletion can remove evidence still needed for an investigation.

Registries also concentrate sensitive authority and substantial cost. They serve many tenants, store shared layers, issue or validate credentials, replicate across boundaries, and may hold proprietary code. A repository permission that appears narrow can expose every filesystem layer or allow a release tag to be replaced.

Content addressability creates strong integrity and deduplication properties, but not governance. Digests do not state whether content is safe, licensed, supported, authorized, compatible, or still accepted after new vulnerability intelligence. Those decisions require evidence and policy that evolve over time.

Lifecycle errors are often irreversible. Deleting the last reachable manifest can make blobs eligible for collection. Retaining everything indefinitely creates cost, legal, privacy, and attack-surface problems. The capability must make both preservation and erasure deliberate.

## Prerequisites and Retrieval

Retrieve cryptographic hashes, Merkle directed acyclic graphs, media types, OCI descriptors/manifests/indexes/layers/configuration, registries, HTTP content negotiation, tags, signatures, attestations, SBOMs, provenance, vulnerability scanning, authentication, authorization, Kubernetes image references and pull policy, storage durability, replication, backup, retention, garbage collection, audit logs, and incident response.

You should distinguish identity from naming; integrity from authenticity; signature validity from signer authorization; artifact inventory from dependency provenance; index digest from selected manifest digest; replication from backup; deletion from garbage collection; retention from legal hold; vulnerability detection from risk acceptance; and immutable artifact bytes from mutable lifecycle state.

## Learning Objectives

After completing this module, you should be able to:

1. explain the OCI content graph and verify descriptors safely;
2. design repository, namespace, tag, and digest conventions;
3. govern multi-platform image indexes and selected manifests;
4. attach and discover typed evidence without ambiguous subjects;
5. define least-privilege publication, pull, mutation, deletion, and administration;
6. promote, replicate, cache, and deploy artifacts without losing identity;
7. continuously reassess immutable artifacts against changing intelligence;
8. derive retention and garbage-collection behavior from graph reachability; and
9. operate quarantine, revocation, rollback, recovery, and deletion as auditable lifecycle states.

## Core Exposition

### Begin with artifact classes and consumers

Inventory what the platform stores: runnable images, image indexes, Helm charts, WebAssembly modules, language packages, firmware, build caches, SBOMs, provenance, signatures, scan reports, and policy decisions. Each class has a media type, expected consumer, size, confidentiality, evidence, compatibility, retention, and deletion contract.

Do not force every blob into “container image” semantics. OCI manifests can package other artifact types, but consumers must interpret `artifactType` and media types correctly. A registry that transports an object does not guarantee that a runtime understands it.

Define ownership at repository and digest granularity. The owning team answers support and remediation questions; the platform owns registry availability, integrity mechanisms, namespace policy, lifecycle automation, and evidence discoverability. Shared base artifacts need an explicit platform or foundation owner.

State service objectives separately for push, pull, metadata/listing, evidence lookup, replication freshness, scanning latency, and administrative operations. Pull availability can remain high while scan or catalog APIs are degraded.

### Understand the OCI graph

An OCI descriptor contains `mediaType`, `digest`, and `size`, with optional URLs, annotations, embedded data, platform, and artifact type depending on context. The digest binds raw bytes. The size lets a client reject unexpected length before expensive processing.

An image manifest references one configuration object and a sequence of filesystem layer descriptors. The configuration contains execution parameters and the ordered root filesystem history. A layer is a filesystem changeset, not a security boundary; consumers can retrieve and inspect it when authorized.

An image index contains descriptors for other manifests or indexes. A resolver selects a compatible descriptor using operating system, architecture, variant, and possibly implementation-specific policy. The index digest and selected manifest digest are different identities.

The graph gains evidence edges when a manifest declares a `subject`. The Distribution referrers API lists manifests that refer to a subject digest. Clients may need the specified tag-schema fallback where native referrers are unavailable. Capability conformance must test both publication and discovery behavior.

### Verify before interpreting

For descriptor $x=(m,s,d)$ and retrieved bytes $b$, safe consumption first checks $|b|=s$, then calculates $H(b)$ and verifies the encoded digest equals $d$. Only after that should parsers perform expensive or dangerous interpretation.

Content negotiation matters. The returned HTTP `Content-Type` and manifest `mediaType` must be handled according to the distribution contract. Silent conversion can change bytes and therefore digest identity. If a registry rewrites manifests, cross-registry identity and signatures may break.

Validate graph structure and bound traversal. Reject unsupported algorithms/media types, negative or excessive sizes, invalid JSON/schema, cycles where forbidden, excessive depth/fan-out, and decompression bombs. A valid digest only proves that retrieved bytes match the identifier.

Communicate expected digests through an authenticated channel. Recalculating a malicious digest supplied by the same compromised source confirms only self-consistency.

### Treat tags as user-interface state

Tags support discovery and workflows: `1.4.2`, `candidate`, `stable`, or a source revision. They are pointers, not versions by themselves. Record every tag mutation with actor, old digest, new digest, reason, policy, and time.

Use immutability rules for release/version tags. A channel tag may intentionally move, but consumers should resolve it through a promotion decision and record the resulting digest. Avoid `latest` in automation because its semantics are implicit and different tools assign special pull behavior.

Separate source-version, build-run, semantic-version, and release-channel names. One tag should not pretend to encode all four. Metadata can carry repository revision and build identity while promotion state records channels.

Provide reverse discovery: given a digest, show repositories, tags, evidence, platforms, owners, releases, deployments, retention holds, and vulnerability decisions. Incident response begins with digests, not guesses from names.

### Govern publication atomically at the logical level

A publisher uploads blobs, configuration, manifests, and indexes. Because blobs may be deduplicated and uploads retried, operations should be idempotent by digest. A manifest must never become an approved release merely because upload completed.

Use staging/candidate namespaces or lifecycle state until required evidence is present and verified. Logical publication is complete when the subject and required evidence are reachable, policy evaluation has a durable result, and the release catalog can expose one coherent record.

Registry protocols do not necessarily provide a cross-object transaction. Design reconciliation: detect orphan uploads, missing evidence, incomplete multi-platform sets, stale tags, and partial replication. Retry safely and make intermediate state non-consumable by protected environments.

Reject a publisher that claims a digest but uploads different bytes. Enforce repository naming, media type, maximum sizes, allowed artifact types, tag rules, quota, and evidence requirements at controlled boundaries.

### Manage multi-platform artifacts explicitly

An index should enumerate supported platform tuples and point to immutable manifests. Validate that every required platform exists exactly as policy expects and that unexpected variants do not slip into a broadly trusted index.

Tests and scans may differ per manifest because binaries and system packages differ. Provenance may cover one build producing the index and all manifests, or separate platform builds. Acceptance policy must understand the actual evidence subjects rather than assuming an index signature covers every claim about descendants.

At deployment, Kubernetes and the container runtime resolve the image index for a node's platform. Record both requested index digest and runtime image ID/selected manifest where possible. Otherwise an incident cannot determine which platform bytes ran.

Promotion of an index is all-or-nothing only if policy says so. A critical arm64 defect may quarantine the whole release or only prevent scheduling on arm64; the decision must align with channel semantics and user expectations.

### Attach evidence with typed subject relationships

Store signatures, SBOMs, provenance, scan results, and attestations as typed artifacts whose subject is the exact manifest or index digest. Preserve predicate type and schema version. A generic “metadata” attachment is too ambiguous for policy.

Evidence can have different scopes. An SBOM for an index may aggregate platform BOMs, while per-manifest BOMs describe actual packages. A signature may authenticate the index; platform scan results may refer to child manifests. The release catalog should render this graph, not flatten it into one green badge.

Verify evidence authenticity, authorized identity/issuer, subject digest, predicate type, schema, freshness where relevant, and claim-specific policy. A registry ACL preventing writes is helpful but does not replace cryptographic verification when evidence crosses boundaries.

Define what happens when subject deletion leaves referrers or when referrers are deleted first. Retention and replication must traverse both ordinary descriptor edges and subject relationships so evidence does not become misleading or orphaned.

### Design authentication and authorization by action

Use distinct identities for builders/publishers, evidence services, promotion controllers, replication agents, scanners, deployment consumers, humans, and administrators. Prefer short-lived workload credentials and repository-scoped tokens.

Separate capabilities: push content, create tags, mutate channel tags, pull, list, read evidence, delete manifests, run retention, administer policy, and configure replication. Build jobs should rarely delete or mutate production channel tags.

Repository read access exposes layers, configuration, and often proprietary source-derived content. Namespace secrecy is not access control. Audit successful and denied operations without logging bearer credentials.

Emergency administration needs strong authentication, time bounds, approval, session logging, and post-event review. A universal robot credential becomes a fleet-wide incident when leaked.

### Promote by digest and preserve the decision

Promotion evaluates an existing digest; it does not copy or rebuild merely to change environments. The decision record contains subject, source/build provenance, required evidence digests, policy version, exceptions, actor/controller identity, target channel, and time.

Copying the exact content graph to another registry may be necessary for latency or boundary reasons. Verify source and destination digests and evidence reachability. If the destination rewrites a manifest, it is a new digest requiring explicit correspondence and possibly new signatures.

Use immutable release records even when channel pointers move. Rollback selects a previously accepted digest whose current policy and runtime compatibility are understood. “Previous tag value” is insufficient if mutation history is incomplete.

Do not assume an old accepted artifact remains acceptable. Revoked signers, newly critical vulnerabilities, expired exceptions, removed licenses, or incompatible runtime policy can block rollback. Maintain emergency policy explicitly.

### Integrate with runtime pull behavior

Kubernetes image references may contain a tag, digest, or both; when both are present, the digest governs pulling. `imagePullPolicy` controls registry lookup behavior but does not turn a mutable tag into immutable identity.

Use digest references in deployed specifications and preserve the friendly source tag as annotation/catalog metadata. Admission can resolve tags and verify signatures/attestations, but resolution and mutation must produce an auditable digest-bound workload.

Plan registry availability, node caches, credential providers, pull concurrency, bandwidth, and image size. `IfNotPresent` may use local content; pre-pulled images require consistent node provisioning and credential-verification decisions. Node caches improve startup but are not authoritative repositories.

Observe pull latency, failures, throttling, authentication, platform selection, decompression/storage pressure, and runtime image IDs. A healthy registry control API does not imply every node can pull and unpack a large image.

### Reassess immutable artifacts continuously

Vulnerability and malware knowledge changes while bytes remain fixed. On push scanning gives an initial result. Scheduled and event-driven rescanning evaluates stored digests when databases, policies, or analyzers change.

Record scanner identity/version, vulnerability database snapshot, subject digest, analysis time, scope, result, and exceptions. Never overwrite history as if a new result had existed at release time. Expose current assessment and timeline.

Risk decisions consider reachability, exploitability, privilege, exposure, compensating controls, fix availability, environment, and business impact—not severity alone. Exceptions have owner, rationale, scope, expiry, and review.

When policy changes, query affected digests and deployments, notify owners, block new promotion/use where appropriate, rebuild from corrected inputs, verify replacements, and close exceptions. Scanning is valuable only when connected to action.

### Replicate for placement, not as a substitute for recovery

Replication serves geography, network boundaries, air gaps, availability, or provider independence. Define direction, namespace mapping, filters, deletion behavior, evidence inclusion, ordering, retry, conflict policy, and maximum acceptable lag.

Verify digest equality after transfer and test that clients can discover all required manifests/referrers. Measure last successful reconciliation and per-object lag. “Replication enabled” is not evidence that the latest release is present.

Replication can propagate malicious or accidentally deleted state. A backup preserves recoverable historical state under independent credentials and retention. Test restoration of manifest graphs, tags/history, evidence, policy/catalog metadata, and access configuration.

For air-gapped transfer, create a signed inventory of expected descriptors, validate media types and sizes before import, scan under the destination's intelligence, and preserve source identity. The boundary can apply stricter policy than the source.

### Derive retention from reachability and obligations

Retention inputs include active release channels, deployment references, rollback windows, support lifetimes, investigation needs, legal hold, regulatory erasure, vulnerability quarantine, replication lag, and ownership. A simple “delete untagged after seven days” can destroy digest-pinned releases or evidence.

Let $R$ be protected roots: deployed digests, supported releases, legal holds, quarantined investigations, and their required evidence. Let $\operatorname{reach}(R)$ be all descriptors reachable through manifests, indexes, and subject/evidence policy. Objects outside the marked set may become deletion candidates only after grace, replication, and race checks.

Deletion usually removes manifest reachability first; garbage collection later sweeps blobs not referenced by any surviving manifest. Shared layers remain while any manifest references them. Storage reclaimed is therefore not the sum of deleted image logical sizes.

Run a dry-run report, reconcile active writes, place the registry in its supported safe mode, mark, review, sweep, and validate afterward. Some registry implementations require read-only or stopped writes because concurrent uploads can be swept incorrectly.

### Quarantine and revoke without destroying evidence

Quarantine blocks new promotion, pull, admission, or deployment according to severity while retaining bytes, evidence, access logs, deployment mappings, and investigation notes. It should be reversible by an authorized decision.

Revocation can target a signer identity, certificate/trust root, provenance builder, artifact digest, release decision, or exception. Propagate it to promotion, admission, package consumers, catalogs, and mirrors. Immutable content remains; authorization changes.

Deletion follows preservation and impact analysis. Prematurely deleting a malicious artifact can destroy the subject needed to verify evidence or reproduce findings. Conversely, confidentiality or legal obligations may require prompt erasure; preserve only authorized metadata and attest that deletion occurred.

Provide an explicit state machine such as candidate → accepted → promoted → deprecated → retired, with side states quarantined and held. Each transition has policy, authority, notifications, and audit evidence.

### Operate cost, reliability, and tenancy

Measure stored unique bytes, logical referenced bytes, object count, request rate, egress, replication, scanning, deduplication, unreferenced age, evidence completeness, and ownership. Quotas should account for shared blobs without making costs incomprehensible.

Protect availability with request limits, upload size limits, fair rate controls, storage alerts, backend integrity checks, tested backup, regional strategy, and degraded read behavior. Catalog listing may be eventually consistent while digest pulls remain correct; document this.

Avoid cardinality explosions from per-digest metrics labels. Keep digest-level detail in queryable inventory/events and aggregate operational metrics by repository, tenant, media type, region, and status.

The following synthetic inventory demonstrates a lifecycle audit across heterogeneous artifacts.

<!-- bijux-verify: {"id":"artifact-lifecycle-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"artifacts=10\nimages=7\nindexes=2\nsigned=8\nsbom=8\nretained=7\nreplicated=4\nquarantined=2\npublic=2\n","stderr":""}} -->
```python
artifacts = [
    {"name":"api-index",      "kind":"index", "signed":True,  "sbom":True,  "retained":True,  "replicated":True,  "quarantined":False, "public":False},
    {"name":"api-amd64",      "kind":"image", "signed":True,  "sbom":True,  "retained":True,  "replicated":True,  "quarantined":False, "public":False},
    {"name":"api-arm64",      "kind":"image", "signed":True,  "sbom":True,  "retained":True,  "replicated":True,  "quarantined":False, "public":False},
    {"name":"worker-index",   "kind":"index", "signed":True,  "sbom":True,  "retained":True,  "replicated":True,  "quarantined":True,  "public":False},
    {"name":"worker-amd64",   "kind":"image", "signed":True,  "sbom":True,  "retained":True,  "replicated":False, "quarantined":True,  "public":False},
    {"name":"docs",           "kind":"image", "signed":True,  "sbom":True,  "retained":False, "replicated":False, "quarantined":False, "public":True},
    {"name":"cli",            "kind":"image", "signed":True,  "sbom":True,  "retained":True,  "replicated":False, "quarantined":False, "public":True},
    {"name":"legacy-service", "kind":"image", "signed":False, "sbom":False, "retained":True,  "replicated":False, "quarantined":False, "public":False},
    {"name":"preview",        "kind":"image", "signed":False, "sbom":False, "retained":False, "replicated":False, "quarantined":False, "public":False},
    {"name":"release-chart",  "kind":"chart", "signed":True,  "sbom":True,  "retained":False, "replicated":False, "quarantined":False, "public":False},
]

print(f"artifacts={len(artifacts)}")
print(f"images={sum(item['kind'] == 'image' for item in artifacts)}")
print(f"indexes={sum(item['kind'] == 'index' for item in artifacts)}")
for field in ("signed", "sbom", "retained", "replicated", "quarantined", "public"):
    print(f"{field}={sum(item[field] for item in artifacts)}")
```

The fixture identifies work; it does not demonstrate that signatures, SBOMs, retention, replication, quarantine, or public-access controls are correctly implemented.

## Definitions and Notation

Let $V$ be immutable content objects and $E\subseteq V\times V$ digest-bound descriptor or subject relationships. Let $G=(V,E)$ be the artifact graph. A descriptor for $v$ is $x(v)=(m(v),s(v),d(v))$, where $m$ is media type, $s$ byte size, and $d=H(\operatorname{bytes}(v))$.

Let $T$ be a time-varying partial naming function. $T_t(n)=d$ means name/tag $n$ points to digest $d$ at time $t$. It is valid for $T_{t_1}(n)\ne T_{t_2}(n)$ while both referenced artifacts remain immutable.

Let $R$ be protected root digests and $\operatorname{reach}_G(R)$ their transitive closure through required content and evidence edges. A candidate sweep set is $S=V\setminus\operatorname{reach}_G(R)$, narrowed further by grace, holds, active uploads, replica lag, and policy.

Let $P_t(d,e,c)$ be acceptance policy at time $t$ over digest $d$, evidence set $e$, and consumer context $c$. Immutability means $d$ is stable; it does not imply $P_{t_1}=P_{t_2}$.

For a multi-platform index $i$, selection is $\sigma(i,p)=m_p$ for compatible platform $p$, when exactly one allowed manifest is selected. Both $d(i)$ and $d(m_p)$ matter to evidence and runtime observation.

## Mechanisms, Invariants, or Proof Structure

The lifecycle mechanism is:

1. classify the artifact and expected consumers;
2. upload content idempotently and verify descriptor size/digest/media type;
3. assemble manifests/indexes and record immutable digest identities;
4. attach discoverable typed evidence to exact subjects;
5. evaluate policy and create a durable acceptance/promotion decision;
6. distribute or replicate the complete verified graph;
7. resolve by digest at consumption and observe selected platform content;
8. rescan/reassess as intelligence and policy change;
9. quarantine or revoke while preserving evidence and impact mappings; and
10. retain protected graph roots, delete eligible references, then safely garbage-collect unreachable blobs.

This is an assurance structure, not proof that an artifact is benign. Content hashes rely on algorithm and expected-digest integrity. Signatures rely on identity, trust roots, custody, and authorization. Evidence relies on producer accuracy and scope. Scanning relies on analyzer coverage and database currency. Runtime selection relies on platform metadata and implementation. Retention relies on a complete root/evidence graph and race-free mark/sweep.

The invariants are immutable content identity, explicit mutable naming, descriptor verification, index/manifest distinction, evidence subject binding, action-specific authority, current consumer policy, graph-aware retention, replication verification, and auditable state transitions.

## Alternatives and Trade-Offs

**One registry versus federated registries:** one service simplifies policy, search, and deduplication but creates concentration and boundary challenges. Federation improves locality and autonomy but requires identity-preserving replication, policy reconciliation, and global inventory.

**Immutable tags versus movable channels:** immutable version tags prevent accidental replacement. Movable channel tags support convenient progression. Use both, but make digest-bound release records authoritative and channel movement audited.

**Evidence in OCI referrers versus external databases:** referrers preserve subject proximity and portability. External catalogs enable richer queries and cross-ecosystem data. A robust platform can store portable evidence with artifacts and index it externally, reconciling both.

**Scan on push versus continuous scanning:** on-push scanning gives fast initial feedback. Continuous/event-driven reassessment catches new knowledge but consumes capacity and creates changing decisions. Risk tiering and incremental rescans balance cost.

**Replicate everything versus demand-driven replication:** eager replication improves readiness and air-gap availability at storage/egress cost. Demand-driven caches reduce cost but may fail during upstream outage. Protect critical release roots eagerly and cache low-risk content with measured miss behavior.

**Soft delete versus immediate erasure:** soft delete aids recovery and investigation but prolongs exposure. Immediate erasure meets some privacy/security needs but can break rollback/evidence. Policy must classify content and legal obligations rather than choose globally.

**Platform-wide versus tenant-managed retention:** central policy ensures minimum safety and cost control. Tenant policy reflects product support/legal needs. Combine platform guardrails with declared tenant roots, holds, and bounded overrides.

## Failure Modes and Misconceptions

- **“A semantic version tag is immutable by definition.”** Only registry policy and audit make tag mutation controlled.
- **“The digest proves who built the image.”** It identifies bytes; provenance/signatures address origin under separate assumptions.
- **“Signing the index covers every platform scan.”** Signature scope and vulnerability evidence scope must be evaluated explicitly.
- **“Private layers cannot leak.”** Authorized pullers can retrieve layers, and shared storage/configuration mistakes expand exposure.
- **“A green scan is permanent.”** intelligence, policy, and exploitability change.
- **“Deleting the tag deletes the bytes.”** Manifests and shared blobs may remain referenced; collection is a separate operation.
- **“Untagged means unused.”** digest-pinned deployments and referrer graphs may have no tag.
- **“Logical image size equals reclaimable storage.”** shared content-addressed layers remain while referenced.
- **“Replication is backup.”** replicated corruption/deletion lacks independent historical recovery.
- **“A registry copy always preserves digest.”** media conversion or manifest rewriting can change identity.
- **“Pull policy verifies authorization and signatures.”** registry lookup/cache behavior differs from admission evidence policy.
- **“Quarantine should delete immediately.”** investigation and impact analysis often require preserved subjects/evidence.
- **“Any valid signature is acceptable.”** consumer policy must constrain signer identity, issuer, subject, and claims.
- **“One admin token is operationally simpler.”** it couples every repository and lifecycle action into one compromise.

## Worked Examples

### Example 1

`payments:2.4.1` is overwritten after a hotfix. One cluster has cached the old manifest while another pulls the new one. Both report the same tag. The platform makes release tags immutable, records the original and replacement digests as distinct releases, and deploys by digest. Conclusion: a tag cannot simultaneously serve human versioning and immutable execution identity without enforced rules.

### Example 2

A descriptor claims size 2 KB but supplies a 4 GB compressed object whose digest is valid. A naive client decompresses before checking bounds. The safe client enforces declared/maximum size, verifies raw bytes and digest, validates media type/schema, then performs bounded unpacking. Conclusion: digest verification is necessary but safe parsing also needs resource boundaries.

### Example 3

An index references amd64 and arm64 manifests. Only the index has a signature; only amd64 has a recent scan. Policy requires both platform manifests to have current SBOM and scan evidence before the shared production channel moves. Promotion is rejected. Conclusion: index identity does not erase descendant-specific evidence obligations.

### Example 4

An SBOM and provenance are pushed as OCI artifacts with subjects pointing to an image digest. The destination registry supports manifest copy but omits referrers. A conformance check finds the missing evidence, so promotion remains incomplete. Conclusion: copying the runnable manifest alone does not replicate the release evidence graph.

### Example 5

A build identity can push blobs and manifests to its candidate repository but cannot mutate production tags or delete. An evidence service can attach attestations; a promotion controller alone moves channels; a retention service alone deletes after policy. Conclusion: registry authorization should represent lifecycle actions rather than broad read/write roles.

### Example 6

A Kubernetes Deployment specifies `app:stable@sha256:d1`. The tag later points to `d2`, but the digest still governs the pull. Admission records `d1`; runtime observation records child manifest `d1a` selected for arm64. Conclusion: friendly names can coexist with deterministic pull and platform-specific traceability.

### Example 7

A new vulnerability database marks base package in digest `d7` critical. The scan timeline retains the original clean result and adds a new failing assessment. The catalog maps `d7` to releases and deployments, expires the old exception, and triggers rebuild. Conclusion: immutable artifacts need append-only assessment history and mutable authorization.

### Example 8

Deleting 100 images reports 40 GB logical size, but garbage collection reclaims 3 GB because surviving manifests share most layers. Capacity planning based on logical size was wrong. Conclusion: reclaimable storage is determined by graph reachability and shared blobs.

### Example 9

Garbage collection marks objects while a publisher uploads a manifest whose layers are not yet reachable. The sweep deletes them, corrupting publication. The operator uses the registry's supported read-only maintenance mode, dry run, active-upload reconciliation, mark/sweep, and post-validation. Conclusion: lifecycle automation must respect implementation concurrency semantics.

### Example 10

A compromised signing identity authenticated ten digests. The platform revokes that identity in policy, quarantines affected releases, preserves artifacts/evidence, maps running workloads, and rebuilds with an approved identity. It does not pretend immutable bytes were “unsigned.” Conclusion: revocation changes acceptance and use, not historical content or claims.

## Cross-Program Connections

- **Data Structures Engineering:** Merkle DAGs, reachability, transitive closure, and mark-and-sweep explain registry identity and collection.
- **Computer Security:** content integrity, authenticated identities, authorization, least privilege, revocation, and evidence preservation govern trust.
- **Distributed Systems:** retries, partial publication, replication lag, eventual catalogs, idempotency, and failure domains shape registry operation.
- **Database Systems:** indexes, append-only histories, transactions, lineage, retention, and recovery inform artifact catalogs.
- **Operating Systems:** image layers/configuration become runtime filesystems and processes; node cache and unpacking impose local resource costs.
- **API and Service Engineering:** distribution protocols, content negotiation, pagination, conditional requests, rate limits, and typed errors form the service contract.
- **Reliability Engineering:** SLOs, capacity, backup/restore, degraded modes, and incident exercises make artifacts available and recoverable.
- **Governance and Compliance:** ownership, licenses, legal holds, erasure, audit trails, and exceptions affect artifact lifecycle beyond engineering convenience.

## References

1. Open Container Initiative, “Image Format Specification,” current specification, retrieved 2026-09-02. https://github.com/opencontainers/image-spec
2. Open Container Initiative, “Content Descriptors,” current specification, retrieved 2026-09-02. https://github.com/opencontainers/image-spec/blob/main/descriptor.md
3. Open Container Initiative, “Image Manifest,” current specification, retrieved 2026-09-02. https://github.com/opencontainers/image-spec/blob/main/manifest.md
4. Open Container Initiative, “Image Index,” current specification, retrieved 2026-09-02. https://github.com/opencontainers/image-spec/blob/main/image-index.md
5. Open Container Initiative, “Distribution Specification,” including referrers and deletion, current specification, retrieved 2026-09-02. https://github.com/opencontainers/distribution-spec/blob/main/spec.md
6. CNCF Distribution, “Garbage Collection,” official documentation, retrieved 2026-09-02. https://distribution.github.io/distribution/about/garbage-collection/
7. Kubernetes, “Images,” official documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/containers/images/
8. Sigstore, “Verifying Signatures,” official documentation, retrieved 2026-09-02. https://docs.sigstore.dev/cosign/verifying/verify/
9. Sigstore, “Kubernetes Policy Controller,” official documentation, retrieved 2026-09-02. https://docs.sigstore.dev/policy-controller/overview/
10. in-toto, “Attestation Framework Specification v1.2,” current specification, retrieved 2026-09-02. https://github.com/in-toto/attestation/blob/main/spec/README.md
11. SPDX Project, “SPDX Specification 3.0.1,” current specification, retrieved 2026-09-02. https://spdx.github.io/spdx-spec/v3.0.1/
12. Harbor Project, “Vulnerability Scanning,” official documentation, retrieved 2026-09-02. https://goharbor.io/docs/main/administration/vulnerability-scanning/

## Exercises

### Exercise 1

Explain descriptor, manifest, index, digest, tag, referrer, quarantine, deletion, and garbage collection. For each pair that is commonly confused, state the operational consequence of the confusion.

### Exercise 2

Trace a two-platform release from blob upload through index publication, evidence attachment, promotion, Kubernetes admission, node selection, runtime observation, and rollback. List every digest that must be retained.

### Exercise 3

A registry deletes untagged manifests after three days, runs garbage collection during uploads, replicates only tagged images, overwrites scan results, and gives build jobs delete permission. Diagnose at least seven failures and design corrections.

### Exercise 4

Design retention for a platform with 30-day preview artifacts, 13-month production rollback, continuous scanning, legal holds, air-gapped replication delayed up to seven days, and shared layers. Specify roots, grace, evidence, deletion, and verification.

### Exercise 5

A registry credential leak allowed an attacker to overwrite a channel tag, push a signed-looking attestation from an unauthorized identity, and delete several manifests. Design containment, evidence preservation, impact analysis, restoration, re-verification, consumer protection, and long-term control changes.

## Answers to the Exercises

### Answer 1

A descriptor binds media type, size, and digest to content. A manifest describes configuration/layers or a general artifact composition. An index points to multiple manifests, often by platform. A digest identifies exact bytes; a tag is a movable name. A referrer is a manifest whose subject identifies another manifest digest. Quarantine blocks or restricts use while preserving content. Deletion removes reachability through registry APIs; garbage collection later removes blobs no surviving manifest references. Confusing tag with digest makes deployments nondeterministic; index with manifest hides platform differences; referrer with embedded metadata breaks discovery/scope; quarantine with deletion destroys evidence; deletion with collection creates false storage/recovery expectations.

### Answer 2

Upload and verify shared and platform-specific blobs, configurations, then amd64 manifest $d_a$ and arm64 manifest $d_b$. Publish index $d_i$ referencing both. Attach platform SBOM/scan subjects to $d_a,d_b$ and index-level provenance/signature/release evidence to $d_i$ as policy specifies. Promotion records $d_i$ and evidence digests. Admission verifies $d_i$ and relevant child evidence, then workload specification records $d_i$. A node resolves platform $p$ to $d_a$ or $d_b$; runtime observation records both requested $d_i$ and selected child. Rollback selects a prior accepted index digest after current policy. Retain $d_i,d_a,d_b$, all referenced configurations/layers, every required evidence manifest/payload, and immutable release decisions; tags alone are insufficient roots.

### Answer 3

Untagged is not unused because digest-pinned deployments and evidence subjects may lack tags. Three days may be shorter than rollback, replication, or investigation grace. Collection during uploads can sweep not-yet-reachable blobs. Tag-only replication misses digest roots, children, and referrers. Overwriting scan results erases temporal evidence. Build delete permission violates least privilege. Additional failures include absent deployment/legal/quarantine roots and no dry-run/post-validation. Correct by maintaining a global root catalog, traversing content and evidence graphs, applying owned retention/holds and replication lag, separating candidate publication from acceptance, using registry-supported write quiescence/read-only GC, preserving append-only assessments, verifying replica digests/completeness, separating publisher/promoter/deleter identities, and auditing deletion.

### Answer 4

Roots include active previews for 30 days, every production digest and required evidence for at least 13 months, deployed digests beyond channel lifetime, quarantines, legal holds, and objects awaiting air-gap confirmation. Traverse indexes, manifests, configurations, layers, subject/referrer evidence, and release records. Preview expiry starts after last protected reference; production expiry requires no deployment/hold and rollback closure. Add more than seven days of replication grace plus failure margin. Continuous scan history stays subject-bound for the support/investigation period. Produce dry-run candidate reports by owner, verify destination presence and backup, quiesce writes as required, delete manifests, then collect only unmarked shared blobs. Recompute graph integrity, sample pulls/evidence, measure reclaimed unique bytes, and preserve audited deletion decisions.

### Answer 5

Revoke the credential, tokens, sessions, and derived identities; freeze tag mutation/deletion while preserving service reads if safe. Snapshot registry/catalog/audit/backend state, tag histories, manifests, referrers, trust roots, admission decisions, and deployment digests. Resolve the channel's old/new digests from independent release records and enumerate all operations by the credential. A valid cryptographic envelope from an unauthorized identity is rejected by consumer policy. Restore deleted graphs from independent backup/replica only after verifying descriptor digests and evidence subjects; do not trust attacker-controlled tags. Quarantine uncertain digests, pin workloads to last independently accepted digests, and block unmatched/unauthorized evidence at promotion and admission. Re-verify every affected release, scan current state, rotate scoped credentials, separate push/tag/delete/admin roles, enforce immutable release tags, add append-only tag history and alerts, test restoration, and review why consumer policy or permissions allowed the incident's effects.
