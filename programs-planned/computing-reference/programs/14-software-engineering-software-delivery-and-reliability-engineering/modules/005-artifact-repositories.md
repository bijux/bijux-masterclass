---
module_id: SDRE-005
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 5
title: Artifact Repositories
status: complete
last_verified: 2026-09-06
---

# Artifact Repositories

## One-Page Review

### Governing question

How should a delivery system store, identify, retrieve, govern, and retire built artifacts so that a consumer receives the intended immutable bytes rather than a convenient mutable substitute?

### Essential definitions

- an **artifact** is a bounded output of a build, such as a package, executable, archive, image manifest, layer, or metadata document;
- an **artifact repository** is a controlled service that persists artifacts and their descriptive metadata for later retrieval;
- a **coordinate** is an ecosystem-shaped logical name, such as group, name, version, classifier, and extension;
- a **content digest** identifies bytes using a specified digest algorithm and representation boundary;
- an **immutable release coordinate** may be created once and may not later name different bytes;
- a **mutable reference** or **channel** can be moved deliberately to another immutable artifact;
- **promotion** changes eligibility or a reference to an existing digest without rebuilding its bytes;
- a **proxy repository** retrieves from an upstream and retains a governed local copy;
- **quarantine** stores an upload where normal consumers cannot select it until applicable checks pass;
- **retention** decides how long bytes and metadata remain available;
- **garbage collection** removes content proven unreachable or expired under retention policy;
- **provenance**, **SBOMs**, and **signatures** are related evidence objects, not properties created merely by storage.

### Central model, mechanism, or theorem

Separate immutable content from names. Let object storage be a partial map

$$
O:d\mapsto b \quad\text{with}\quad H(b)=d,
$$

and let an immutable release index be $I:c\mapsto d$. Publishing $(c,b)$ is valid only when the server recomputes $H(b)=d$ and either $c$ is absent or $I(c)=d$. A pre-existing $I(c)=d'\ne d$ is a conflict, not an update.

Mutable channels use a separate map $M:m\mapsto d$ with authorization, compare-and-set or serialization, history, and audit evidence. Consumers that need repeatability resolve the channel once and retain the resulting digest.

### Critical invariants

- artifact boundaries, media types, and digest algorithms are explicit;
- the repository recomputes content identity rather than trusting the uploader's claim;
- a release coordinate never changes bytes after first publication;
- mutable channels are visibly distinct from immutable releases;
- promotion reuses an accepted digest rather than rebuilding per environment;
- metadata changes cannot silently mutate the referenced artifact;
- write, read, delete, promote, and channel-move authorities are least-privileged and auditable;
- upstream proxies retain content identity and origin evidence;
- quarantine is not selectable by production consumers;
- retention preserves every reachable blob and evidence object needed by supported releases;
- deletion is fail-safe, reviewable, and recoverable where policy requires;
- repository availability, integrity, authenticity, and software correctness remain separate claims.

### Common failures

Common failures include overwriting a released version, deploying a floating tag without recording its digest, trusting a client checksum, mixing snapshots with releases, serving the wrong media type, accepting partial multi-blob publication, promoting by rebuild, proxying mutable upstream bytes under a stable local name, giving CI delete authority, letting quarantine leak into resolution, deleting shared blobs by age alone, retaining binaries without their evidence, and treating storage replication as a backup or authenticity proof.

### Compact example

A pipeline uploads package bytes under content digest `d1`, then creates immutable coordinate `payments/2.4.0 -> d1`. Staging and production promotion both select `d1`; no rebuild occurs. A mutable `candidate` channel may later move from `d1` to `d2`, but its history records actor, reason, old digest, new digest, and time. A deployment resolves `candidate` to `d2` and records `d2`. Reusing `payments/2.4.0` for `d2` is rejected.

### Connections

[SDRE-004](004-incremental-builds-and-caching.md) distinguishes ephemeral action-cache results from durable delivery artifacts. [SDRE-006](../ROADMAP.md) next defines compatibility-oriented versions and release identity; SDRE-007 through SDRE-009 add provenance, SBOM, and signing evidence.

## Governing Question

A successful build leaves bytes somewhere. Delivery begins when those bytes must outlive a worker, cross a trust boundary, support rollback, and remain unambiguous months later. A generic file share can retain a file, but it does not by itself define identity, media type, immutability, selection, authorization, evidence linkage, or safe deletion.

An artifact repository is therefore part storage system, part naming system, and part delivery control plane. Its core obligation is modest but strict: when a consumer requests an accepted identity, return the corresponding complete bytes and metadata—or fail explicitly. It must not silently substitute a newer upload, an upstream mutation, a partial object, or a quarantined candidate.

## Why This Matters

Build-once promotion depends on durable identity. If staging tests digest $d_1$ but production resolves the same label to $d_2$, the test evidence does not apply. Rollback similarly requires the old artifact and enough metadata to select and operate it, not just the source revision from which someone hopes to rebuild it.

Repositories also concentrate risk. They hold executable content, credentials may grant broad publication power, and a popular proxy can distribute one bad object widely. Availability failures can halt delivery; integrity failures can corrupt it; confidentiality failures can disclose proprietary packages. Each needs a distinct control and evidence story.

Repository ecosystems encode different coordinate and metadata conventions. Maven defines a path layout derived from group, artifact, version, classifier, and extension [1]. The OCI Distribution Specification defines an API for distributing content-addressed blobs and manifests, and is intentionally usable beyond container images [2]. These are concrete protocols, not a universal logical model; the invariants in this chapter apply across them.

## Prerequisites and Retrieval

Retrieve artifact, build identity, content digest, collision-resistance assumption, canonical bytes, coordinate, version, namespace, media type, manifest, index, metadata, immutable release, mutable channel, promotion, proxy, quarantine, retention, reachability, garbage collection, authentication, authorization, audit trail, replication, backup, and restore.

From SDRE-001 retrieve build-once promotion and the distinction between artifact and release identity. From SDRE-002 retrieve verified external dependency content and authorized origins. From SDRE-003 retrieve reproducible bytes and evidence limits. From SDRE-004 retrieve the distinction between an action result and a durable releasable artifact.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish artifact storage, logical coordinates, content identity, and mutable selection;
2. design create-once semantics for release coordinates;
3. explain manifests, blobs, media types, and multi-object publication;
4. design build-once promotion across environments;
5. separate hosted, proxy, aggregate, release, snapshot, and quarantine roles;
6. apply least privilege to repository operations and delivery actors;
7. reason about upstream mutability, proxy caching, and dependency confusion;
8. define retention and garbage collection using reachability and policy holds;
9. design backup, restore, reconciliation, and integrity verification;
10. diagnose artifact-selection incidents without confusing storage with authenticity or correctness.

## Core Exposition

**Define the artifact boundary.** A coordinate or digest is meaningful only over specified bytes. Is the artifact a `.jar`, its detached signature, a POM, an OCI manifest, an image index, a layer, or a release bundle containing all of them? A repository often stores a graph: a manifest references configuration and layer blobs; metadata references packages; attestations refer to subjects by digest. Record each media type and edge.

The digest identity $d=H(b)$ binds one byte sequence under one algorithm. It does not bind a human name, origin, producer, policy approval, behavior, or safety. Those claims require authenticated metadata and governance. Collision resistance is an assumption, not mathematical injectivity over arbitrary bytes.

**Separate coordinate from content identity.** Humans and tools need coordinates such as `org.example:parser:2.3.1`. A release coordinate should be a create-once mapping to a content digest. Repeating the same publication can be idempotent when the coordinate and bytes match; different bytes at the same coordinate must fail.

This rule prevents “fixed in place” releases. A correction receives a new release identity, even if the old upload was accidental. Otherwise caches, lockfiles, SBOMs, signatures, vulnerability findings, test results, and deployments can disagree about what the version means.

**Make mutability explicit.** Teams still need channels such as `candidate`, `stable`, or a rolling snapshot line. Model these separately from releases. Moving a channel is an authorized state transition with an expected old digest, new digest, actor, reason, time, and policy result. A consumer that must reproduce a deployment records the resolved digest, not only the channel.

An OCI tag is a familiar mutable reference while a manifest digest is content identity. The OCI Image Specification 1.1.1 defines descriptors containing digest, media type, and size and defines manifests and indexes as content-addressed structures [3]. Product policy decides whether a tag may move; the digest remains the deployment evidence.

**Publish graphs completely.** Multi-object formats complicate atomicity. OCI upload flows place blobs before a manifest that references them; the distribution specification requires blob and manifest operations and defines response/error behavior [2]. A repository should reject or withhold selection of a manifest whose referenced content is missing, invalid, unauthorized, or in the wrong namespace.

Use a staging transaction or quarantine state: upload bytes, recompute digests, validate format and media type, ensure referenced objects exist, attach required evidence, run policy, then create the selectable release mapping. A client timeout after publication makes retry important: create-once idempotence lets the client learn whether the intended mapping exists.

**Promote identity, not a rebuild.** Build once, assign digest, validate it, then move eligibility through candidate, staging, and production. Environment-specific configuration belongs outside the immutable binary when feasible. If packaging genuinely changes bytes, it creates a different artifact with its own identity and evidence; calling that operation “promotion” hides a rebuild.

Promotion state can live as environment policy records or mutable channel mappings. Either way, record the exact digest. Passing tests on `d_1` cannot authorize `d_2` merely because both share a version label.

**Assign repository roles.** A hosted repository accepts organization-produced content. A proxy repository retrieves upstream content and retains a local copy. An aggregate view searches several sources under an explicit precedence policy. A release repository accepts immutable versions. A snapshot repository accepts expiring, replaceable development identities. Quarantine receives uploads before ordinary resolution.

Do not combine roles merely for convenience. A resolver searching internal and public namespaces without ownership rules can select an attacker-controlled public package with a colliding name. Repository order is not enough when configuration drifts; define namespace ownership and authorized origins, as introduced in SDRE-002.

**Proxy upstreams defensively.** On first fetch, verify transport and expected content identity where available, record upstream URI and retrieval time, then retain the exact bytes. If an upstream serves different bytes under the same logical coordinate, fail or create an explicit incident record; do not silently replace the cached object.

A proxy improves availability and repeatability only after it has the needed closure. A cache miss during an upstream outage still fails. Offline release preparation should verify that every locked dependency and its metadata is present before the release window. The Update Framework illustrates a stronger update-repository design with separately trusted, versioned, and expiring metadata roles intended to resist rollback, freeze, and key-compromise scenarios [4]; adopting one idea without its full client state machine does not inherit its guarantees.

**Enforce authorization by operation.** Publishing is not one permission. Separate upload to quarantine, create release coordinate, move channel, promote eligibility, read confidential artifacts, administer retention, delete content, change policy, and restore backup. CI that builds an untrusted contribution should not inherit release-publication credentials. Human emergency access should be time-bound and audited.

Authentication establishes an actor identity under some mechanism; authorization decides an allowed operation; an audit event records what the system observed. None proves the artifact benign. NIST SP 800-161 Revision 1 Update 1 places such controls within broader organizational cyber-supply-chain risk management rather than treating a repository as the whole program [7]. Later modules add provenance, SBOM, and signatures, while the Security Engineering program owns their adversarial analysis.

**Bind evidence as first-class objects.** Store or reference checksums, provenance, SBOMs, signatures, test results, policy decisions, licenses, and vulnerability-analysis identities using the artifact digest as subject. Avoid embedding mutable “latest scan result” inside immutable release metadata. Instead, append versioned evidence records whose own identities and issuers are explicit. SLSA 1.2 and the in-toto Attestation Framework define current supply-chain statement and subject conventions useful at this boundary [5] and [6].

The OCI referrers mechanism supports discovering manifests that refer to a subject descriptor [2]. The mechanism provides linkage and discovery; policy still decides which artifact types, issuers, freshness, and verification outcomes are required.

**Design retention from obligations.** Storage age alone is unsafe. Let roots include currently supported releases, deployed digests, rollback candidates, legal or incident holds, and retained evidence. Trace references from roots through manifests, layers, attachments, and metadata. Only unreachable objects that also satisfy age and policy rules become deletion candidates.

Shared blobs make reference counting subtle. A layer unused by one tag can still be reachable from another manifest. Concurrent publication can race with collection. Use snapshots, epochs, leases, or transactional coordination so a collector does not delete content between upload and manifest publication.

**Distinguish replication, backup, and archive.** Replication serves availability and may copy corruption or deletion quickly. A backup preserves recoverable state across a fault boundary. An archive retains selected material for long-term obligations. Define recovery-point and recovery-time objectives, encryption and key recovery, immutability or deletion protection, restore authority, and regular restore exercises.

A successful restore must preserve mappings, bytes, metadata, permissions, and audit continuity. Recompute digests after restore and reconcile references. A backup job's success message is weaker evidence than retrieving and validating a representative restored graph.

**Observe the repository.** Measure publication success and latency, resolution errors, missing blobs, digest mismatches, authorization denials, upstream failures, replication lag, storage growth, garbage-collection candidates and results, backup age, restore tests, and channel movement. Avoid logging credentials or confidential payloads.

Define service objectives around consumer operations: can a deployment resolve and fetch the complete pinned artifact within its deadline? Raw object-store availability can look healthy while metadata lookup or authorization is broken.

## Definitions and Notation

- $B$: set of possible artifact byte strings;
- $D$: set of digest identifiers including algorithm;
- $C$: set of immutable release coordinates;
- $N$: set of mutable channel names;
- $H:B\to D$: selected content-digest function;
- $O:D\rightharpoonup B$: partial content store;
- $I:C\rightharpoonup D$: create-once release index;
- $M:N\rightharpoonup D$: mutable channel map;
- $R\subseteq D\times D$: reference edges from a manifest or metadata object to required objects;
- $Roots$: digests protected by deployment, support, rollback, evidence, legal, or incident policy;
- $Reach(Roots)$: transitive closure of protected content under $R$.

Assume the repository recomputes digests over canonical stored bytes, accepted algorithms meet the threat model, operations are authorized, and mappings are durably serialized. These premises must be evidenced in an implementation; the notation does not establish them.

## Mechanisms, Invariants, or Proof Structure

**Create-once theorem.** Assume all successful operations on coordinate $c$ are serialized and the only transition for absent $c$ sets $I(c)=d$. Any later request with the same $d$ is idempotent and any request with $d'\ne d$ is rejected. Then after first success, $I(c)$ remains equal to its original $d$.

**Proof.** Induct over later operations. The base state after first success is $I(c)=d$. For one subsequent operation, an equal digest leaves the mapping unchanged; a different digest is rejected and also leaves it unchanged. Thus the invariant is preserved. By induction it holds for every finite operation sequence. The result depends on serialization and on there being no privileged overwrite path.

**Retrieval integrity proposition.** If a consumer requests digest $d$, receives bytes $b$, recomputes $H(b)=d$, uses the intended algorithm and byte boundary, and accepts the collision assumption, then the received bytes match that content identity. This does not establish that the coordinate was authorized, the producer trusted, or the software correct.

**Safe collection condition.** A deletion candidate $x$ must satisfy

$$
x\notin Reach(Roots) \land expired(x) \land \neg hold(x) \land \neg leased(x).
$$

This is necessary under the model, not sufficient for a real collector whose reference graph may be stale or incomplete.

**Executable verification.** This finite repository model uses a deliberately weak teaching checksum so it can run without imports. It demonstrates create-once coordinates, separate mutable channels, server recomputation, and idempotent retry. It is not cryptography or durable storage.

<!-- bijux-verify: {"id":"model-immutable-artifact-repository","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"push_v1=created\nrepeat=exists\nconflict=rejected\nrelease=d9-857\nchannel_before=d9-857\nchannel_after=d9-858\nrelease_unchanged=True\nbad_bytes=rejected\n","stderr":""}} -->
```python
objects = {}
releases = {}
channels = {}

def content_id(data):
    return f"d{len(data)}-{sum(ord(char) for char in data)}"

def put_object(claimed, data):
    if content_id(data) != claimed:
        return "rejected"
    objects.setdefault(claimed, data)
    return "stored"

def publish(coordinate, data):
    digest = content_id(data)
    put_object(digest, data)
    if coordinate not in releases:
        releases[coordinate] = digest
        return "created"
    if releases[coordinate] == digest:
        return "exists"
    return "rejected"

print(f"push_v1={publish('payments/1.0.0', 'binary-v1')}")
print(f"repeat={publish('payments/1.0.0', 'binary-v1')}")
print(f"conflict={publish('payments/1.0.0', 'binary-v2')}")
print(f"release={releases['payments/1.0.0']}")

channels['candidate'] = content_id('binary-v1')
print(f"channel_before={channels['candidate']}")
channels['candidate'] = content_id('binary-v2')
print(f"channel_after={channels['candidate']}")
print(f"release_unchanged={releases['payments/1.0.0'] == content_id('binary-v1')}")
print(f"bad_bytes={put_object(content_id('binary-v1'), 'tampered')}")
```

## Alternatives and Trade-Offs

**Coordinates versus digests.** Coordinates are understandable and ecosystem-compatible; digests are precise byte identities. Persist both and use digests for repeatable consumption.

**Monolithic versus federated repositories.** One service simplifies discovery and policy but enlarges blast radius. Federation separates ownership and failure domains but complicates routing, replication, and governance.

**Eager mirroring versus on-demand proxying.** Mirroring improves offline readiness at storage cost. On-demand proxying saves space but leaves first use dependent on upstream availability.

**Strict immutability versus snapshot convenience.** Create-once releases preserve meaning. Replaceable snapshots accelerate experimentation only when isolated, visibly named, and excluded from release evidence.

**Central policy versus ecosystem-native metadata.** Central controls improve consistency; native formats preserve interoperability. Adapt policy at controlled boundaries without rewriting artifact bytes invisibly.

**Immediate versus delayed deletion.** Immediate collection saves cost but narrows recovery. Delayed, soft-deleted, or versioned storage consumes capacity while improving incident response and mistaken-deletion recovery.

**Repository as gate versus repository as store.** Integrated scanning and policy can prevent unsafe selection, but coupling every check to upload reduces availability. Quarantine and promotion separate durable receipt from consumer eligibility.

## Failure Modes and Misconceptions

- **“A version is immutable by convention.”** Enforce create-once server-side.
- **“A tag is an artifact identity.”** Record its resolved digest.
- **“A checksum proves authenticity.”** It binds bytes only under assumptions.
- **“The client supplied a digest.”** The repository must recompute it.
- **“Promotion rebuilds for each environment.”** Different bytes are different artifacts.
- **“Metadata can be edited safely.”** It may change resolution and evidence.
- **“The proxy has it somewhere.”** Verify the complete locked closure.
- **“HTTPS makes upstream content immutable.”** Transport and naming are distinct.
- **“Quarantined means stored securely.”** Ensure ordinary resolution cannot select it.
- **“CI needs administrator access.”** Separate narrow publication operations.
- **“Replication is backup.”** Replicas can copy loss and corruption.
- **“Old means unreachable.”** Shared blobs and supported releases remain roots.
- **“Garbage collection is local.”** Publication and references can race with it.
- **“Repository uptime equals delivery readiness.”** Resolution, authorization, and graphs matter.
- **“Stored artifacts are correct.”** Storage preserves bytes, including bad ones.

## Worked Examples

### Example 1

**Overwrite attempt.** A team uploads corrected bytes under `ledger/3.1.0`, already published. The repository returns conflict; the team publishes `3.1.1` and deprecates the old coordinate without changing it. **Conclusion:** correction creates a new identity.

### Example 2

**Floating deployment.** Staging resolves `stable` to $d_1$; the channel moves before production, which receives $d_2$. The pipeline changes its release record to pin $d_1$ after approval. **Conclusion:** a channel is selection input, not durable evidence.

### Example 3

**Partial image.** Configuration and one layer upload, but another layer fails. The manifest remains unselectable until every referenced digest exists and verifies. **Conclusion:** publish the graph's root last under completeness checks.

### Example 4

**Idempotent retry.** A client times out after publishing. Retry with the same coordinate and digest returns the existing mapping; retry with different bytes conflicts. **Conclusion:** create-once semantics make ambiguity recoverable.

### Example 5

**Mutable upstream.** A proxy previously cached package coordinate `x/1.2`; upstream later serves different bytes. The proxy retains the old digest, raises an incident, and refuses silent replacement. **Conclusion:** local repeatability requires content identity and mutation policy.

### Example 6

**Dependency confusion.** Internal package `payroll-core` is absent from one aggregate view, so resolution falls through to a public namesake. Namespace ownership rejects public origin for the internal prefix. **Conclusion:** search order is weaker than origin authorization.

### Example 7

**Evidence attachment.** A new vulnerability scan refers to release digest $d$ without altering its manifest. Both old and new scan records remain identifiable with issuer, database revision, and time. **Conclusion:** append evidence; do not mutate artifact identity.

### Example 8

**Shared-layer collection.** Tag A is deleted, but its layer is also referenced by supported manifest B. Reachability from B preserves the layer. **Conclusion:** garbage collection follows the reference graph, not tag age alone.

### Example 9

**Replica loss.** An erroneous delete replicates to every serving node. An isolated versioned backup restores objects and mappings; reconciliation recomputes digests and checks references. **Conclusion:** replication and tested recovery solve different failures.

### Example 10

**Emergency rollback.** The binary remains, but its configuration schema and migration metadata were deleted. Rollback cannot be judged safe. Retention roots expand to the complete release and operational evidence bundle. **Conclusion:** recoverability is a graph property.

## Cross-Program Connections

- [Database Engineering](../../18-database-engineering/ROADMAP.md) owns transactions, indexes, constraints, and storage mechanisms underlying repository implementations.
- [Distributed Systems](../../27-distributed-systems-engineering/ROADMAP.md) owns replication, consistency, partial failure, and distributed garbage collection.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns cryptographic verification, threats, signing, authorization, and supply-chain attack analysis.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns artifact repositories offered as an internal developer-platform product.
- [Cloud Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) owns cloud storage and managed-service architecture.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) connects metadata, lineage, retention, and governance across enterprise information systems.

## References

1. Apache Maven Project, “Maven Repository Layout” and repository metadata model, current documentation checked 2026-09-06. [Official layout](https://maven.apache.org/repository/layout.html).
2. Open Container Initiative, *Distribution Specification 1.1.1*, released March 2025. [Official specification repository](https://github.com/opencontainers/distribution-spec/tree/v1.1.1). Version and release status checked 2026-09-06.
3. Open Container Initiative, *Image Format Specification 1.1.1*, released April 2025. [Official specification repository](https://github.com/opencontainers/image-spec/tree/v1.1.1). Version and release status checked 2026-09-06.
4. The Update Framework, *Specification*, current 1.0 series checked 2026-09-06. [Official specification](https://theupdateframework.github.io/specification/latest/).
5. SLSA, *Specification 1.2*, current specification checked 2026-09-06. [Official specification](https://slsa.dev/spec/v1.2/).
6. in-toto project, *Attestation Framework*, current specification checked 2026-09-06. [Official specification](https://github.com/in-toto/attestation/tree/main/spec).
7. NIST, *Cybersecurity Supply Chain Risk Management Practices for Systems and Organizations*, SP 800-161 Revision 1 Update 1, November 2024. [Official publication](https://csrc.nist.gov/pubs/sp/800/161/r1/upd1/final).

## Exercises

### Exercise 1

**Distinguish identities.** For a Maven package, an OCI image index, and a compressed executable, identify logical coordinate, byte boundary, content digest, mutable reference, and evidence objects. State what each identity does not prove.

### Exercise 2

**Trace publication.** Design a retry-safe multi-blob publication protocol from quarantine through validation and immutable release creation. Cover missing blobs, duplicate upload, client timeout, conflicting coordinate, and concurrent garbage collection.

### Exercise 3

**Diagnose substitution.** Staging and production used the same version string but different bytes. Give an investigation, containment, correction, and evidence-preservation procedure.

### Exercise 4

**Design repository governance.** Define repository roles, namespace ownership, least-privilege actors, promotion, proxy rules, retention, deletion, backup, audit events, and availability objectives for a multi-team organization.

### Exercise 5

**Transfer to firmware.** Design an artifact repository for signed device firmware with hardware variants, calibration-independent binaries, staged rollout channels, long support periods, safety evidence, legal holds, revocation, and offline recovery.

## Answers to the Exercises

### Answer 1

For Maven, the coordinate contains group, artifact, version, classifier, and extension; the artifact digest covers the selected file bytes, while repository metadata and signatures are separate objects. For OCI, a tag is a mutable reference, a manifest or index digest identifies its JSON bytes, and descriptors link configuration and layer digests. For the executable, distinguish digest of compressed archive from digest of extracted executable; neither silently substitutes for the other.

Coordinates aid selection but may be mutable unless policy forbids it. Digests support byte identity under algorithm and boundary assumptions but do not prove origin or behavior. Signatures authenticate a statement under a key and policy; provenance describes a claimed production event; SBOMs describe claimed contents. None alone proves correctness, safety, current approval, or absence of compromise.

### Answer 2

Create an upload transaction with actor, namespace, intended coordinate, expected object descriptors, media types, and expiry. Upload each blob under a server-recomputed digest; duplicate identical uploads are idempotent. Keep objects leased from collection. Validate formats, reference closure, authorization, evidence requirements, and policy in quarantine. Then serialize release creation: absent coordinate becomes the root digest, equal mapping returns success, and unequal mapping conflicts.

Publish no selectable root before referenced objects exist. If the client times out, it queries the coordinate and transaction: equal mapping confirms success, absent state permits retry, and different mapping is an incident. Release leases only after the mapping is durable and collector snapshots can observe it. Failed transactions expire after evidence retention and recovery policy allow cleanup.

### Answer 3

Freeze channel movement and affected publication, preserve both byte sets, digests, manifests, coordinate history, cache/proxy logs, actors, credentials, policy versions, build provenance, test records, and deployments. Determine whether overwrite, mutable tag movement, proxy mutation, rebuild, race, compromise, or recording error caused divergence. Inventory every consumer of each digest.

Contain by pinning known accepted digests, revoking suspect write authority, quarantining disputed content, and blocking promotion. Correct server-side immutability and require approval records to bind a digest. Publish any corrected bytes under a new release identity, repeat applicable checks, and assess rollback or forward repair. Do not delete disputed evidence or claim that restoring one mapping repairs already deployed systems.

### Answer 4

Separate hosted release, snapshot, upstream proxy, quarantine, and aggregate views. Assign namespace owners and permitted origins. Build workers upload only to quarantine; a policy identity creates releases; delivery identities read approved namespaces and move only their owned environment channel; repository administrators cannot approve releases by infrastructure privilege alone; retention and emergency deletion need distinct, audited authority.

Create-once release mappings point to recomputed digests. Promotion reuses one digest. Proxy changes under stable coordinates fail visibly. Retention roots include support, deployment, rollback, evidence, incident, and legal obligations; collection uses complete reachability plus expiry, hold, and lease checks. Maintain isolated recoverable backups and exercise graph restoration. Audit actor, operation, coordinate, old/new digest, policy, result, and time. Set objectives for complete pinned resolution and retrieval, not just storage-node uptime.

### Answer 5

Use immutable coordinates containing product, hardware family, firmware release, and format while the content digest identifies exact unsigned or signed bytes. Model each hardware variant separately. Keep per-device secrets and calibration data outside common firmware unless they intentionally create distinct personalized artifacts. Attach build provenance, SBOM, signing statement, test and safety evidence, compatibility matrix, and revocation status by subject digest.

Channels such as pilot and stable may move only through authorized, recorded transitions; devices resolve and retain a digest. Long-term roots include supported fleets, rollback images, bootloader compatibility, evidence, investigations, and legal holds. Revocation prevents new selection but does not erase bytes needed for forensics or rollback analysis. Maintain geographically and administratively isolated backups with keys and offline restore procedures. Block rollout on missing variant closure, invalid signature policy, incompatible boot chain, absent safety evidence, unexplained byte change, expired authorization, or untested recovery. Legitimate product, safety, security, and regulatory owners decide release.
