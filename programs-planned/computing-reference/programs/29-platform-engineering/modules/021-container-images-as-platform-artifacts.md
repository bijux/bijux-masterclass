---
module_id: PLAT-021
program: Platform Engineering
level: 1
module_number: 21
title: Container Images as Platform Artifacts
status: complete
last_verified: 2026-09-02
---

# Container Images as Platform Artifacts

## One-Page Review

### Governing question

How should a platform build, identify, verify, distribute, promote, run, update, and retire container images as immutable software artifacts rather than treating tags, Dockerfiles, or scanner reports as deployable truth?

### Essential definitions

- A **container image** is an OCI-described content graph containing a manifest, configuration, and ordered filesystem layers; an image index can select manifests for multiple platforms.
- A **descriptor** identifies referenced content by media type, byte size, and cryptographic digest, with optional annotations and platform information where allowed.
- A **digest** is a content-derived identifier such as `sha256:<hex>`; changing the covered bytes changes the digest.
- A **tag** is a human-readable repository reference that a registry can move to different manifest content.
- A **layer** is a filesystem changeset applied in order; deleting a file in a later layer does not remove its bytes from an earlier layer.
- A **build input** is any source, base image, dependency, build definition, parameter, secret-mediated fetch, or builder state that can affect output or evidence.
- **provenance** is verifiable information describing where, when, and how an artifact was produced, including builder and material identities.
- An **attestation** is a signed statement whose subject is an artifact digest and whose predicate expresses claims such as provenance or an SBOM.
- **promotion** is an authorized change in an artifact's eligibility for an environment or channel without changing its bytes.
- **reproducibility** means independently rebuilding declared inputs can produce bit-for-bit identical output; **hermeticity** concerns whether undeclared external inputs can influence a build.

### Central model, mechanism, or theorem

Model a releasable image as $A=(G,B,R,P,S,V,Q,L)$: OCI content graph $G$, declared build inputs and process $B$, runtime contract $R$, provenance $P$, software inventory $S$, verification results $V$, policy qualification $Q$, and lifecycle record $L$. Deployment resolves an approved reference to immutable digest $d$, verifies graph bytes and evidence subjects against $d$, selects the correct platform manifest, and records the executed digest. A tag helps discovery; it is never sufficient identity or provenance.

### Critical invariants

- Every built, tested, scanned, signed, promoted, deployed, rolled back, and audited artifact is joined by immutable digest.
- Production promotion moves the same verified bytes; it does not rebuild from the same source for each environment.
- Builder-generated provenance is evaluated against trusted signer, builder, source, parameters, and dependency expectations—not merely checked for signature validity.
- Secrets, source-control credentials, package tokens, caches, and build tools do not remain in runtime layers or image configuration.
- Multi-platform releases verify and qualify each selected manifest; an index-level label cannot hide an unreviewed variant.
- Image configuration declares a least-privilege runtime contract, while runtime policy independently enforces identity, filesystems, capabilities, resources, and connectivity.
- Vulnerability findings are time-bound observations; exceptions have owner, scope, evidence, compensation, expiry, and rebuild trigger.
- Tags may move only under declared publishing rules; deployed workload status records the resolved digest.
- Retention and garbage collection preserve live, rollback, investigation, legal, and attestation reachability before deleting content.

### Common failures

Deploying `latest`; confusing `imagePullPolicy: Always` with immutable selection; rebuilding for production; copying only a tag; signing before the final mutation; verifying a signature but not identity or claims; scanning one architecture; installing debugging tools in runtime images; deleting secrets in a later layer; embedding environment configuration; running as root by default; accepting stale base images indefinitely; equating small size with safety; relying on CVE count alone; mutating release tags; losing attestations during registry copy; and garbage-collecting rollback evidence.

### Compact example

A release index names Linux `amd64` and `arm64` manifests. Each manifest digest has matching builder provenance, SBOM, expected signer identity, zero unresolved critical findings under the current policy, runtime-contract tests, and independent promotion status. The platform copies content and referrers by digest into the production registry, verifies the destination graph, binds a human release tag to the approved index digest, and deploys by digest. Workload status records the selected architecture manifest. A later base-image advisory opens a reviewable rebuild; it does not mutate the deployed digest or retroactively change its evidence.

### Connections

Retrieve platform boundaries and consumer responsibility from [PLAT-001](001-platform-engineering-as-complexity-management.md) through [PLAT-009](009-platform-team-boundaries.md), value and journey evidence from [PLAT-010](010-defining-a-platform-s-value-proposition.md) through [PLAT-012](012-time-to-first-successful-deployment.md), declarative interfaces from [PLAT-013](013-command-line-interfaces.md) through [PLAT-018](018-feedback-and-error-diagnostics.md), release contracts from [PLAT-019](019-golden-path-versioning.md), and decision-grade measurement from [PLAT-020](020-measuring-developer-experience-without-vanity-metrics.md).

## Governing Question

Which exact bytes will run, for which platform, produced from which inputs by which builder, with what runtime contract and evidence, under whose policy and lifecycle authority?

An image is more than a tar archive and less than a running workload. It packages a root filesystem and default execution parameters, but it does not establish the runtime identity, network policy, secrets, volumes, resource limits, or host isolation that will surround a container. Its familiar name may be a mutable tag. Its scan may be stale. Its signature may be valid but unauthorized. Platform engineering must preserve these distinctions.

The durable abstraction is an immutable artifact plus a graph of evidence and policy decisions. That abstraction supports reproducible selection, safe promotion, incident response, rollback, architecture-specific qualification, and eventual retirement.

## Why This Matters

Container images cross unusually many trust boundaries. Application teams choose source and dependencies. Base-image maintainers publish operating-system content. Build platforms assemble layers. registries store and serve manifests and blobs. Security systems attach findings and attestations. Deployment controllers select references. Runtimes unpack and execute bytes on shared hosts. A weakness at any handoff can invalidate the release claim.

Tags make these handoffs look simpler than they are. `registry.example/payments:1.8` is memorable, but the registry may later resolve it to different content. Even `imagePullPolicy: Always` asks Kubernetes to resolve a name each time; if that name is a mutable tag, different starts can select different digests. Digest references turn content selection into an auditable decision.

Immutability does not mean software never changes. It means a published digest's meaning does not change. Patches create a new artifact and evidence set. Promotion changes authorization around a digest. Rollback selects an earlier retained digest. This separation makes change reviewable.

Supply-chain evidence also needs precision. An SBOM inventories declared or discovered components; it does not prove absence of malware. A vulnerability scan compares an artifact against tools and knowledge at a time; it does not prove safety. A signature proves control of a signing identity over a payload; policy must still decide whether that identity, builder, subject, and claims are acceptable.

## Prerequisites and Retrieval

Retrieve platform capabilities, team boundaries, service journeys, contract diagnostics, versioning, measurement, trust boundaries, artifact repositories, CI/CD, dependency management, release policy, vulnerability management, incident response, and rollback from prior modules and your software-engineering foundations.

You should understand hashes, digital signatures, public-key identities, JSON, HTTP registries, filesystem archives, package managers, build graphs, caches, Linux users and permissions, process signals, environment variables, multi-architecture execution, policy evaluation, threat modeling, and eventual consistency.

## Learning Objectives

After completing this module, you should be able to:

1. explain OCI manifests, indexes, configurations, layers, descriptors, digests, tags, and registry distribution;
2. define a platform image contract covering build, runtime, evidence, qualification, and lifecycle;
3. design controlled build contexts, pinned inputs, cache rules, reproducibility tests, and trusted builders;
4. minimize runtime content and privilege without sacrificing required operability;
5. generate, bind, verify, preserve, and interpret provenance, SBOMs, signatures, and scan results;
6. qualify every variant in a multi-platform release and record runtime selection;
7. promote exact bytes through registries and environments with digest-based policy;
8. respond to vulnerabilities through risk analysis, rebuild, exceptions, and rollout rather than tag mutation; and
9. retain and retire images without losing rollback or incident evidence.

## Core Exposition

### Understand the OCI content graph

The OCI Image Specification describes content through descriptors. A descriptor includes media type, digest, and size. Fetching by descriptor allows the consumer to verify both length and content digest before interpreting the bytes. Content-addressed blobs can be shared safely when the digest algorithm and verification are trusted.

An image manifest references exactly one image configuration and an ordered list of layers. The configuration records architecture, operating system, root-filesystem diff identifiers, history, and execution defaults such as user, environment, entrypoint, arguments, working directory, ports, labels, and stop signal. The layers supply filesystem changes. Configuration is metadata for the image as a whole, not a property of one layer.

An image index references one or more manifests, commonly for platform combinations such as Linux `amd64` and Linux `arm64`. Pulling the index does not mean all variants run or have identical packages. A client chooses a compatible descriptor using platform metadata and obtains that manifest's configuration and layers.

The digest of an index, manifest, configuration, and layer identifies each object's bytes separately. A release therefore has a graph of identities, not one magical file hash. Policy can approve the index while retaining variant evidence, but it must not assume one variant's test or scan applies to another.

### Distinguish tags, digests, and release names

A registry reference can use `repository:tag` or `repository@digest`. Tags are mutable mappings under most registry protocols. Digests are content identifiers. A release name such as `1.8.0` is a product contract whose publishing policy may require immutability, but the characters alone do not enforce it.

Use tags for human discovery, channels, and update proposals. Resolve tags in a controlled release step and record the resulting digest. Use digests in promotion records, deployment intent, evidence subjects, allowlists, incident timelines, and rollback plans. If an interface accepts a tag, expose its resolved digest before execution and prevent time-of-check/time-of-use drift.

Some systems display both: `payments:1.8.0@sha256:...`. This preserves recognizable intent while enforcing bytes. If the tag moves, the digest still selects the original content. Do not assume a tag-plus-digest reference asks the runtime to verify that the tag still points there; the digest is authoritative.

### Define the artifact contract

Represent a releasable image as

$$
A=(G,B,R,P,S,V,Q,L),
$$

where $G$ is the OCI graph, $B$ declared inputs and build process, $R$ runtime contract, $P$ provenance, $S$ software inventory, $V$ verification results, $Q$ policy qualification, and $L$ lifecycle record.

The contract identifies owner, source revision, build definition, builder identity, parameters, base digests, locked dependencies, target platforms, output descriptors, expected entrypoint, user, writable paths, signals, ports, health behavior, supported orchestrators, SBOMs, provenance, signatures, tests, scan timestamps, exceptions, channels, promotion history, deployments, support dates, retention, and retirement authority.

Keep claims typed. “Built by trusted builder” is provenance verification. “Contains no known critical vulnerability under scanner database $v$ at time $t$” is a time-bound scan result. “Runs as numeric user 65532 under a read-only root filesystem” is a tested runtime claim. None implies the others.

### Control the build context and inputs

The build context is an input boundary. Exclude source-control metadata, credentials, local build products, test reports, editor state, package caches, and unrelated files. An ignore file reduces accidental inclusion and cache invalidation, but validate the sent context rather than trusting patterns blindly.

Pin the source revision, build definition, frontend syntax, builder mode, base image digest, package lockfiles, remote downloads, toolchains, and platform parameters. Verify checksums and signatures where the upstream ecosystem supports them. Avoid unconstrained package-manager updates inside a release build; they make output depend on repository state at execution time.

Build secrets must use an ephemeral secret channel whose content does not become an instruction argument, environment default, history entry, build log, cache key disclosed to untrusted parties, or filesystem layer. Deleting a copied token later is insufficient because the earlier layer remains addressable.

Network access broadens the input set. A hermetic build reads declared, content-verified materials from controlled stores. Where full hermeticity is impractical, record accessed repositories, lock resolution, restrict egress, snapshot dependencies, and distinguish the weaker guarantee in provenance.

### Use trusted builders and provenance

The builder is part of the trust base. A local workstation can create correct bytes but offers different isolation, identity, logging, and tamper resistance from a hardened hosted builder. Platform policy should distinguish builder modes and identities whose security properties differ.

SLSA provenance binds artifact subjects to materials, builder, build type, invocation, and execution metadata. It helps consumers form expectations about where and how content arose. Provenance is useful only when verified: authenticate the signer, validate the attestation format, match subject digest, check trusted builder and source, compare parameters and dependencies with policy, and reject unexpected or ambiguous claims.

Generate provenance at the build platform, not by an untrusted post-build script that merely restates user input. Protect signing identities from build workloads where the target assurance requires it. Preserve the evidence with the artifact and ensure registry replication does not detach it.

### Design for reproducibility without confusing it with trust

A reproducible build yields identical bytes from equivalent declared inputs. It exposes hidden clocks, unordered archives, locale, filesystem traversal, random values, unpinned downloads, and builder variation. `SOURCE_DATE_EPOCH` provides a deterministic timestamp input for tools that honor it, but it does not normalize every source of nondeterminism automatically.

Test reproducibility on independent workers and compare output graph digests. When they differ, compare layer and configuration objects to localize the cause. Record the environment and do not “fix” equality by discarding meaningful security inputs.

Reproducibility and provenance complement each other. Reproducibility can detect or deter some build manipulation, yet two identical malicious builds remain malicious. Signed provenance can faithfully describe a compromised builder. Hermeticity can exclude undeclared inputs while executing a declared hostile compiler. Trust comes from combined source, dependency, builder, review, verification, and runtime controls.

### Construct minimal, operable runtime images

Use multi-stage builds to separate compilers, package managers, test tools, headers, and source from the runtime filesystem. Copy only the application and declared runtime dependencies into the final stage. A smaller graph improves transfer and inspection and often reduces attack surface, but byte size alone is not a security metric.

Choose base images by provenance, maintenance, compatibility, update route, package transparency, and support—not fashion. A `scratch` or distroless image can reduce content but complicate certificates, timezone data, name resolution, shell-based health checks, and incident procedures. Include what the runtime contract requires, and provide external debugging mechanisms rather than an ungoverned toolbox in every production image.

Set a numeric non-root user where possible, deterministic working directory, explicit entrypoint and arguments, correct file ownership, required stop signal, and minimal environment defaults. Do not bake environment secrets, endpoints, tenant identity, or production-only configuration into the artifact. One digest should move across environments while deployment configuration changes around it.

Run contract tests with a read-only root filesystem, declared writable mounts, dropped capabilities, no privilege escalation, restricted network, realistic resource bounds, graceful termination, and architecture emulation or native workers as appropriate. Image defaults help portability; admission and runtime policy enforce consequence.

### Treat layers as security and efficiency boundaries

Layer order affects caching, distribution, and secret persistence. Put stable expensive dependency steps before frequently changing application content when doing so does not weaken input integrity. Couple package-index refresh and installation in one instruction so a cached stale index is not reused with a new install request. Clean temporary data in the same layer that created it.

Compression digest and uncompressed diff identifier serve different graph roles. Registries distribute compressed blobs by descriptor digest; root-filesystem configuration records uncompressed changes. Do not invent identity by hashing an extracted directory and assuming it equals the manifest digest.

Shared layers save bandwidth and storage but also couple consumers to a base. Inventory reachability from final manifests, not only repository names. A base-layer advisory may affect many application digests even though none changed. Dependency graph queries must support impact analysis and coordinated rebuilds.

### Inventory components with SBOMs

Generate SBOMs from the final image and, where useful, reconcile them with build-time dependency metadata. A source-only SBOM can miss operating-system packages or files copied from another stage; a filesystem scanner can miss statically linked or vendored components. Record tool, version, configuration, scope, and relationship to the image digest.

Attach an SBOM as an attestation or OCI-associated artifact whose subject is the exact manifest digest. For a multi-platform index, record whether each variant has its own SBOM and whether any index-level document is merely an aggregation. Preserve package identifiers, versions, licenses, source, and dependency relationships with stated uncertainty.

An SBOM enables inventory, licensing, vulnerability correlation, and incident search. It does not prove that listed components are reachable, configured dangerously, authentic, or complete. Those are separate analysis questions.

### Scan and reason about vulnerabilities

Scan final variant digests after assembly and again when advisory knowledge changes. Store scanner identity, database version or timestamp, policy revision, packages examined, severity source, exploitability context, suppressions, and result digest. Scan bases before platform endorsement and descendants for inherited plus application content.

CVE counts are not a risk score. Severity, reachability, exposure, privilege, compensating controls, exploit maturity, data, service consequence, and fix availability matter. Conversely, “not reachable” is an evidence claim that can become false when configuration changes.

Exceptions name the exact digest and finding, owner, rationale, supporting analysis, controls, environment, expiry, and rebuild or revocation trigger. Never whitelist a mutable tag or all future descendants. A new scanner database can change qualification without changing image bytes; preserve both the original release decision and current operational posture.

### Sign and verify identities and claims

Sign the final immutable subject after all content mutation. A signature over a manifest digest does not cover a later rebuilt image that shares its tag. For keyless signing, verification checks certificate identity and issuer plus transparency or trusted bundle evidence as required. For managed keys, verification checks the appropriate trusted key version and revocation state.

Signature validity answers whether the payload and signature match a key or identity. Authorization asks whether that identity may make this claim for this repository, source, builder, and channel. Claim verification checks subject digest and predicate. Freshness, revocation, and policy version remain additional concerns.

Avoid “signed therefore safe.” A compromised authorized pipeline can sign malicious content. Combine source controls, isolated builders, provenance expectations, artifact verification, vulnerability and policy checks, and deployment authorization.

### Qualify multi-platform releases

Build each target on controlled native or emulated infrastructure with platform explicitly declared. Verify index descriptors, platform fields, configuration architecture/OS, and actual executable compatibility. Do not copy an `amd64` SBOM or scan result onto `arm64`; their base layers and binaries differ.

Record qualification per variant: tests, provenance, inventory, scans, runtime contract, signer, exceptions, and support. Index eligibility is the intersection of required variant eligibility for its advertised support set. If one variant fails, either withhold the index, publish a narrower explicit support set, or issue a new index; never leave a broken advertised platform hidden behind a shared tag.

The following synthetic gate demonstrates digest-bound evidence across two variants.

<!-- bijux-verify: {"id":"container-image-variant-gate","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"variants=2\nunique_digests=2\nsigned=2\nprovenance_bound=2\nsbom_bound=2\ncritical_findings=0\npromotion_eligible=2\ntag_only_references=1\n","stderr":""}} -->
```python
variants = [
    {"platform": "linux/amd64", "digest": "sha256:aaa", "signature": True,
     "provenance_subject": "sha256:aaa", "sbom_subject": "sha256:aaa", "critical": 0},
    {"platform": "linux/arm64", "digest": "sha256:bbb", "signature": True,
     "provenance_subject": "sha256:bbb", "sbom_subject": "sha256:bbb", "critical": 0},
]
references = ["registry.example/app:1.8.0", "registry.example/app@sha256:index"]
eligible = [
    variant for variant in variants
    if variant["signature"]
    and variant["provenance_subject"] == variant["digest"]
    and variant["sbom_subject"] == variant["digest"]
    and variant["critical"] == 0
]
print(f"variants={len(variants)}")
print(f"unique_digests={len({variant['digest'] for variant in variants})}")
print(f"signed={sum(variant['signature'] for variant in variants)}")
print(f"provenance_bound={sum(variant['provenance_subject'] == variant['digest'] for variant in variants)}")
print(f"sbom_bound={sum(variant['sbom_subject'] == variant['digest'] for variant in variants)}")
print(f"critical_findings={sum(variant['critical'] for variant in variants)}")
print(f"promotion_eligible={len(eligible)}")
print(f"tag_only_references={sum('@sha256:' not in reference for reference in references)}")
```

The fixture checks subject equality and one simplified finding threshold. It does not validate digest syntax, bytes, signature identity, attestation authenticity, scan quality, runtime behavior, or an index. Real policy must perform those checks.

### Promote artifacts, not rebuild recipes

Build once in a controlled release pipeline. Test and qualify the resulting digest. Promotion records authorize that digest for a channel or environment. Copy by digest when registries are separated, including manifests, blobs, signatures, provenance, SBOMs, and other required referrers; then verify destination digests and evidence reachability.

Do not rebuild the same commit for staging and production. Dependency repositories, base tags, clocks, and builders can yield different bytes, and staging evidence would not cover production. Environment configuration belongs in deployment resources, secret systems, and policy.

Promotion can use immutable metadata in a policy service, signed release statements, or controlled destination repositories. Mutable channel tags can point to the approved digest for discovery, but deployment resolution and audit bind the digest. Separate authorization to publish content, attach evidence, promote, move channels, deploy, and delete.

### Deploy and observe exact content

Kubernetes accepts tags and digests. With `Always`, the kubelet resolves the name to a digest on each launch and can use cached bytes for that digest. This does not make a mutable tag immutable. With `IfNotPresent`, a cached tag resolution can further obscure intended updates. Use digest-pinned workload specifications for controlled releases.

Admission verifies registry scope, digest pinning, evidence, policy qualification, platform support, exceptions, and runtime requirements before accepting workload intent. The node runtime must still verify downloaded content. Record requested index digest, selected manifest digest, node platform, runtime identity, and container image ID in workload status and deployment evidence.

Observe image-pull failures, registry latency, cache hit behavior, signature/policy denial, architecture mismatch, startup and termination, runtime exceptions, and drift. Do not expose registry credentials or sensitive evidence in user-facing diagnostics.

### Patch, rebuild, and revoke

Images are immutable snapshots, so dependency fixes require a new build and digest. An unchanged application source can produce a new release when the base or toolchain changes; provenance explains why. Automated update proposals should change pinned inputs, rebuild, run the full gate, and preserve review.

Set rebuild objectives based on exposure and consequence. Track base and dependency support, advisory changes, credential or signer compromise, policy revisions, and runtime deprecation. A recurring rebuild tests that sources and dependencies remain available, but blindly rebuilding on a timer can introduce unreviewed changes if inputs are not locked.

When content or evidence becomes untrusted, revoke promotion eligibility, block new deployments, inventory running digests, assess exposure, replace progressively, and preserve incident evidence. Killing every running container immediately may cause greater harm; emergency authority and service risk decide containment order.

### Retain and retire safely

Registry deletion interacts with shared blobs, manifests, indexes, referrers, replicas, caches, and garbage collection. Removing a tag may not delete content; deleting an untagged manifest may break an index or evidence link if reachability is misunderstood.

Retention policy covers active deployments, rollback windows, staged releases, incident holds, legal requirements, provenance, SBOMs, scan history, exceptions, and reproducibility inputs. Inventory runtime digest use from clusters and other consumers rather than registry pulls alone. Offline systems and disaster-recovery procedures can be latent consumers.

Retirement disables new promotion and deployment, migrates consumers, verifies rollback successors, preserves required evidence, removes discovery names, waits through recovery windows, and then deletes according to registry semantics. Audit records exact deleted and retained digests and whether recovery is possible.

## Definitions and Notation

Let descriptor $x=(m,n,d,a)$ contain media type $m$, byte size $n$, digest $d$, and optional attributes $a$. Let $H(b)$ be the accepted digest function over bytes $b$. Descriptor verification requires observed size $\lvert b\rvert=n$ and $H(b)=d$ before content interpretation.

Let OCI graph $G=(N,E)$ contain index, manifest, configuration, and layer nodes $N$ with descriptor references $E$. For target platform $p$, selection function $\sigma(G,p)=m_p$ returns a supported manifest or fails; it must not silently choose an incompatible variant.

Let evidence item $e$ have subject set $\operatorname{subj}(e)$. Evidence is bound to artifact digest $d$ only if $d\in\operatorname{subj}(e)$ and the statement, signature, identity, and policy all verify. Subject equality alone is necessary but insufficient.

Let $Q_t(d,p)\in\{\text{eligible},\text{denied},\text{exception},\text{unknown}\}$ be qualification of digest $d$ for platform/environment policy $p$ at time $t$. Because vulnerability knowledge, revocation, and policy change, $Q_t$ can change while $d$ remains immutable.

## Mechanisms, Invariants, or Proof Structure

The artifact path is source and declared materials $\rightarrow$ isolated builder $\rightarrow$ OCI graph $\rightarrow$ digest verification $\rightarrow$ provenance and inventory $\rightarrow$ tests and scans $\rightarrow$ policy qualification $\rightarrow$ digest-preserving promotion $\rightarrow$ admission and runtime verification $\rightarrow$ observed deployment $\rightarrow$ rebuild, rollback, revocation, or retirement.

Traceability runs forward from source revision and materials to every variant and backward from running container image ID to manifest, index, promotion, evidence, builder, and source. A broken link makes the claim unknown rather than implicitly trusted.

Core invariants are digest identity, same-byte promotion, evidence-subject binding, signer/builder authorization, variant-specific qualification, no secret persistence, least-privilege runtime contract, time-bounded scan interpretation, explicit exception lifecycle, observed runtime digest, and reachability-aware retention.

Cryptographic digest verification provides an integrity argument under assumptions about the algorithm and trusted expected digest. It does not prove benign content, correct source, safe configuration, or authorization. The chapter makes no proof that a conforming image is secure.

## Alternatives and Trade-Offs

**Tags versus digests:** tags improve discovery and channel updates; digests provide immutable identity. Publish both, enforce digest for consequence, and preserve controlled tag history.

**Central base images versus team ownership:** curated bases concentrate patching and policy but create coupling and bottlenecks. Team-selected bases improve fit but expand trust and support. Offer a small supported portfolio with explicit escape review.

**Minimal versus operable images:** fewer tools and packages reduce surface and transfer, while certificates, locales, diagnostics, and emergency operation may require content. Derive contents from the runtime and incident contract, not a size contest.

**Native versus emulated multi-platform builds:** native workers better represent execution but cost more and expand infrastructure. Emulation simplifies coordination but can hide behavior or performance differences. Test consequential variants natively before broad promotion.

**Online versus hermetic dependency resolution:** online builds see current fixes but are hard to reproduce and expose repository compromise. Snapshots and mirrors improve control but require freshness operations. Use reviewable pinned updates into controlled stores.

**Key-managed versus identity-based signing:** long-lived keys offer offline control but require custody and rotation. Short-lived identity certificates reduce key handling but depend on issuer, transparency, time, and verification bundles. Policy must state the trust model.

**Registry-per-environment versus shared registry:** separation constrains access and failure domains but risks incomplete copy and evidence drift. A shared registry simplifies identity but needs strong promotion metadata and permissions. Both must preserve digest and evidence.

**Blocking versus monitoring policy:** admission blocking prevents known violations but can harm availability during verifier outages. Monitoring reduces coupling but permits exposure. Tier rules by consequence, cache verified decisions safely, fail explicitly, and retain emergency authority.

## Failure Modes and Misconceptions

- **“A container is an image.”** An image is packaged content and defaults; a container is a runtime instance with additional state and policy.
- **“A version tag is immutable.”** Immutability is a registry and governance property; record and deploy its digest.
- **“Always pull gets the same release.”** It repeatedly resolves the name; a mutable tag can select different content.
- **“We tested the Dockerfile.”** Tests cover an output digest, not every future execution of a recipe.
- **“Deleting the secret removes it.”** Earlier layers remain in the content graph; never copy the secret into a layer.
- **“Rebuilding the commit promotes it.”** Rebuilds can change bytes and invalidate prior evidence; promote the tested digest.
- **“One scan covers the index.”** Variants have different manifests, layers, packages, and vulnerabilities.
- **“Zero known CVEs means secure.”** Databases are incomplete, configuration matters, and malicious or vulnerable behavior may lack a CVE.
- **“Signed means trusted.”** Verify identity, issuer/key, subject, claims, authorization, revocation, and policy.
- **“An SBOM proves completeness.”** Tool scope and package discoverability limit inventory; record method and uncertainty.
- **“Smaller is always safer.”** Missing trust stores, update mechanisms, or diagnostics can make operation less safe.
- **“Garbage collection is storage housekeeping.”** It can destroy rollback and investigation evidence or break graph reachability.

## Worked Examples

### Example 1

Release tag `2.3.0` moves after a rebuild. Deployment policy rejects tag-only intent, and audit shows the old and new digests instead of pretending one release identity remained stable.

### Example 2

A token is copied during dependency installation and deleted in the next instruction. Layer inspection recovers it. The pipeline rotates the token and switches to an ephemeral build-secret mount with a no-secret layer test.

### Example 3

An `amd64` image passes tests, while the `arm64` binary contains the wrong native library. Variant qualification denies the release index until native execution and SBOM evidence pass for `arm64`.

### Example 4

A signature is cryptographically valid but issued to a developer's interactive identity rather than the release builder. Policy rejects it because the repository/channel requires the hosted builder identity and matching provenance.

### Example 5

Staging and production rebuild the same commit one day apart. A base tag moved, producing distinct digests. The platform replaces environment rebuilds with one digest-preserving promotion.

### Example 6

A minimal image lacks certificate authorities required for outbound TLS. The runtime contract adds a maintained trust bundle explicitly; adding a shell and package manager is unnecessary.

### Example 7

A high-severity library finding is unreachable in the deployed binary, while a medium issue exposes a network parser. Risk review prioritizes the parser and records time-bounded reachability evidence for the high finding.

### Example 8

Registry replication copies the image but omits provenance and SBOM referrers. Destination verification blocks promotion and copies the complete subject evidence before binding the release tag.

### Example 9

A signing issuer is compromised. The platform blocks new deployments signed under the affected trust path, inventories running digests, preserves evidence, rebuilds with a restored identity, and stages replacement by service consequence.

### Example 10

An apparently unused image supports an offline disaster-recovery cluster. Runtime and recovery inventory catches the latent dependency before tag removal and garbage collection.

## Cross-Program Connections

Operating systems contributes processes, filesystems, users, signals, namespaces, capabilities, and architecture. Distributed systems contributes content-addressed graphs, registries, replication, caching, eventual consistency, and failure recovery. Cryptography contributes hashes, signatures, identities, transparency, and revocation limits.

Software engineering contributes dependency locking, builds, tests, release immutability, reproducibility, and configuration separation. API engineering contributes OCI distribution, media types, content negotiation, errors, idempotent upload, and compatibility. Security contributes supply-chain threats, least privilege, secrets, vulnerability response, provenance, and incident containment.

Data engineering contributes lineage, inventories, graph queries, evidence retention, and time-versioned findings. Reliability contributes startup, health, graceful shutdown, resource behavior, progressive rollout, rollback, and emergency policy. Platform product management contributes supported bases, paved paths, exceptions, adoption, and consumer-facing diagnostics.

## References

- Open Container Initiative, [*OCI Image Format Specification*](https://github.com/opencontainers/image-spec), current specification retrieved September 2, 2026. Descriptors, manifests, indexes, configurations, layers, digests, layouts, annotations, and artifact relationships.
- Open Container Initiative, [*OCI Image Configuration*](https://github.com/opencontainers/image-spec/blob/main/config.md), current specification retrieved September 2, 2026. Root-filesystem changes, execution parameters, history, platform fields, diff identifiers, and runtime defaults.
- Open Container Initiative, [*OCI Image Media Types*](https://github.com/opencontainers/image-spec/blob/main/media-types.md), current specification retrieved September 2, 2026. Media types and descriptor relationships among indexes, manifests, configurations, and layers.
- Open Container Initiative, [*OCI Distribution Specification*](https://github.com/opencontainers/distribution-spec/blob/main/spec.md), current specification retrieved September 2, 2026. Registry pull, push, content discovery, manifests, blobs, tags or digests, errors, and referrers behavior.
- SLSA, [*SLSA Specification 1.2*](https://slsa.dev/spec/v1.2/), approved specification retrieved September 2, 2026. Supply-chain levels, tracks, provenance, verification, build-platform assessment, and attestation formats.
- SLSA, [*Build: Verifying Artifacts*](https://slsa.dev/spec/v1.2/verifying-artifacts), approved guidance retrieved September 2, 2026. Provenance authentication, expectations, artifact subjects, dependency verification, and enforcement locations.
- SLSA, [*Build: Distributing Provenance*](https://slsa.dev/spec/v1.2/distributing-provenance), approved guidance retrieved September 2, 2026. Artifact-attestation relationships, publication, immutability, multiple attestations, and container applicability.
- Sigstore, [*Verifying Signatures*](https://docs.sigstore.dev/cosign/verifying/verify/), current documentation retrieved September 2, 2026. Image digest claims, certificate identity, issuer, bundles, keys, and verification behavior.
- Kubernetes Project, [*Images*](https://kubernetes.io/docs/concepts/containers/images/), current documentation retrieved September 2, 2026. Image names, tags, digests, pull policies, cache behavior, parallel pulls, credentials, and pull failures.
- Docker, [*Building Best Practices*](https://docs.docker.com/build/building/best-practices/), current documentation retrieved September 2, 2026. Multi-stage builds, trusted/minimal bases, rebuilds, build context, packages, cache, CI, non-root execution, and digest pinning.
- Reproducible Builds, [*SOURCE_DATE_EPOCH Specification*](https://reproducible-builds.org/specs/source-date-epoch/), revision 1.1. Deterministic build timestamp input and timestamp-clamping requirements.
- NIST, [*Application Container Security Guide (SP 800-190)*](https://csrc.nist.gov/pubs/sp/800/190/final), 2017. Image, registry, orchestrator, container, and host threat categories and security recommendations.

## Exercises

### Exercise 1

Define the artifact contract and release gate for a multi-platform payment service image. Include OCI graph, inputs, builder, runtime, evidence, variant policy, promotion, deployment, vulnerability response, and retirement.

### Exercise 2

Threat-model a build that uses a mutable base tag, unrestricted network, package token, shared cache, self-hosted runner, generated SBOM, vulnerability scan, and developer signature. Identify false assurances and durable controls.

### Exercise 3

Design a digest-preserving promotion from a build registry to staging and production registries. Address referrers, tag behavior, verification, authorization, partial copy, concurrent promotion, rollback, and garbage collection.

### Exercise 4

Respond to a critical base-image advisory affecting 600 image digests across three architectures, including an offline fleet, a regulated service, and a signer revocation. Specify inventory, prioritization, rebuild, evidence, rollout, exceptions, and audit.

### Exercise 5

Transfer the model to virtual-machine images used for hospital clinical systems. Address identity, variants, build provenance, packages, credentials, configuration, scanning, promotion, boot/runtime enforcement, patching, rollback, and clinical authority.

## Answers to the Exercises

### Answer 1

Publish an OCI index digest with separately identified `amd64` and `arm64` manifests, configurations, and layers. Pin source, build definition, builder mode, base digests, lockfiles, remote checksums, and target platform. Trusted hosted builders generate signed provenance with matching subjects; final-image SBOMs, scans, unit/integration/runtime-contract tests, and reproducibility results bind each manifest. The runtime contract specifies numeric non-root user, entrypoint, stop behavior, read-only root, writable mounts, ports, resource assumptions, and no embedded environment secrets. Variant gates verify graph bytes, signer/builder/source expectations, inventory, current vulnerability policy, payment security controls, and native execution. Promote the same index and referrer graph by digest; destination verification precedes controlled tag binding. Admission requires digest, qualified evidence, supported platform, and least privilege, while status records selected manifest. Advisory changes open pinned rebuilds and progressive replacement; exceptions are digest-specific and expiring. Retention preserves live, rollback, incident, regulated, and offline dependencies before retirement and garbage collection.

### Answer 2

The mutable base and online package repository make inputs time-dependent; pin digests and package snapshots or verified locks. Restrict network to declared mirrors and record materials. Pass the token through an ephemeral secret channel, redact logs, isolate caches by trust and input, and prove no secret enters layers or configuration. A self-hosted runner's owner, isolation, persistence, and signing authority need assessment; use a distinct builder identity and move consequential releases to a hardened builder. Cache hits are not provenance and can import poisoned output unless content and scope are verified. The SBOM may omit copied, static, or OS content; generate from the final variant and record method. A scan is time- and database-bound and needs risk context. A developer signature can be valid but unauthorized and cannot substitute for builder provenance. Bind final digest, SBOM, provenance, scan, and signature; verify signer, issuer/key, subject, builder, source, parameters, materials, and policy independently.

### Answer 3

Select the qualified source index digest, enumerate its descriptor closure and required signature, provenance, SBOM, scan, and promotion statements, and copy by digest. Use idempotent blob upload and manifest publication, but treat a published index as the commit point only after dependencies exist. Verify every destination byte against descriptors and every evidence subject and authorization. Record source and destination registry, digest, copy operation, policy revision, actor, and time. Bind immutable release tags only after verification; mutable channel tags use compare-and-set or serialized authorization so concurrent promotions cannot overwrite silently. A partial copy remains ineligible and is safe to retry or collect after a quarantine window. Staging and production authorization are separate records over identical bytes. Rollback reauthorizes a retained prior digest with current safety review. Garbage collection traces indexes, manifests, blobs, referrers, live deployments, rollback sets, replicas, and holds before deletion.

### Answer 4

Query SBOM and base lineage by affected package and base digest, then reconcile against registry graphs, cluster image IDs, offline manifests, and recovery systems across all architectures. Separately inventory artifacts whose trust depends on the revoked signer. Prioritize by exploitability, exposure, privilege, data, service consequence, active deployment, offline update latency, and fix availability—not count alone. Freeze new affected promotion, restore a trusted signing path, pin the corrected base, rebuild every supported variant on an approved builder, regenerate provenance and SBOMs, rescan, run contract and regression tests, and issue new digests. Roll out canaries and high-exposure services first while clinical/regulatory authority approves the regulated path and offline operators receive authenticated bundles plus verification instructions. Any delay exception names exact digest, environment, controls, owner, expiry, and forced replacement trigger. Do not mutate tags to conceal affected content. Preserve old evidence and signer history for investigation, record every running-to-replacement mapping, and retire only after live, offline, rollback, and disaster-recovery inventories reconcile.

### Answer 5

Treat each VM disk, firmware/boot metadata, architecture, and hardware profile as an immutable variant identified by digest inside a release index. Pin operating-system repository snapshots, clinical application source, drivers, agents, policy, and builder configuration. A controlled builder generates provenance, package and file inventories, signatures, vulnerability findings, boot tests, clinical integration tests, and configuration schema evidence per variant. Never bake patient data, machine credentials, environment endpoints, or ward identity into the image; inject them through authorized provisioning with auditable secrets. Promotion moves identical image bytes through test and production catalogs. Boot verifies signature, digest, measured or secure-boot expectations, and authorization; runtime enforces identity, network, storage encryption, monitoring, and least privilege. A patch produces a new image and controlled rollout with validated backup, state migration, downtime, forward recovery, and rollback limits. Clinical engineering, patient safety, security, privacy, operations, and clinical leadership own consequence decisions. Technical artifact qualification never proves a VM is clinically appropriate for a specific patient workflow.
