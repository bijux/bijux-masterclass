---
module_id: PLAT-031
program: Platform Engineering
level: 1
module_number: 31
title: Application Build Capability
status: complete
last_verified: 2026-09-02
---

# Application Build Capability

## One-Page Review

### Governing question

How should a platform turn reviewed source into immutable deployable artifacts and trustworthy evidence while keeping developer feedback fast, release authority narrow, and every consequential input reconstructable?

### Essential definitions

- A **build** transforms declared source, dependencies, toolchain, parameters, and environment into one or more artifacts.
- A **build capability** is a supported platform product that owns build invocation, isolation, policy, evidence, publication, and lifecycle contracts.
- A **build recipe** is the version-controlled instruction set that declares how the transformation occurs.
- An **artifact** is a build output intended for consumption, such as an OCI image, package, archive, binary, or manifest.
- A **digest** is a collision-resistant content identifier; unlike a tag, it identifies bytes rather than a movable name.
- **Hermeticity** means the build observes only explicitly admitted inputs; reproducibility means equivalent declared inputs can recreate byte-identical specified outputs.
- **Provenance** is authenticated metadata binding an artifact to its builder, process, parameters, and inputs.
- An **SBOM** describes identified components and relationships in a software product; it is not proof that the build used only those components.
- An **attestation** is an authenticated statement whose predicate makes a typed claim about one or more artifact subjects.
- **Promotion** advances an already-built digest through environments or release channels without rebuilding it.

### Central model, mechanism, or theorem

Model a build request as $B=(S,D,T,R,P,E,N,C,Q)$: source $S$, dependencies $D$, toolchain $T$, recipe $R$, parameters $P$, environment $E$, network policy $N$, cache state $C$, and quality/security policy $Q$. The platform produces $F(B)=(A,V)$, where $A$ is a content-addressed artifact set and $V$ is verifiable evidence. Trust is not inherited from successful execution. A consumer accepts a digest only if artifact integrity, signer/builder identity, provenance predicate, admitted inputs, and release policy all verify against an independent expectation.

### Critical invariants

- Every consequential input is declared, pinned or resolved under recorded policy, and represented in evidence.
- Untrusted source changes cannot obtain release credentials, provenance-signing authority, trusted caches, or production publication rights.
- Builder identities and signing authority are controlled by the platform, not exposed to user-defined build steps.
- Build workers are ephemeral and isolated across runs; persistent state is explicit, scoped, and treated as an input.
- Network access is denied when feasible and otherwise restricted, observed, and reflected in the dependency-resolution contract.
- Artifacts are published and promoted by digest; mutable tags are discovery aliases, never the security identity.
- Provenance and SBOM subjects bind to the exact artifact digest, and consumers verify them rather than merely checking that files exist.
- A failed required test, policy, signature, evidence generation, or publication step cannot yield a releasable artifact.
- Cache reuse crosses only compatible trust boundaries and cannot inject unverified outputs into trusted builds.
- Rebuild, revocation, retention, base-image response, and capability version migration are owned lifecycle operations.

### Common failures

Running release builds on developer laptops; granting registry push or signing keys to arbitrary build scripts; resolving floating dependencies silently; trusting a tag as immutable; rebuilding separately per environment; allowing pull-request builds to write shared release caches; treating test success as provenance; treating an SBOM as integrity proof; generating evidence after an artifact can be changed; making the build network unrestricted; placing secrets in image layers or cache exports; claiming reproducibility after two identical runs on one worker; blocking all development on a single brittle pipeline; and keeping artifacts forever without ownership or revocation.

### Compact example

A service commit is accepted by a hosted build capability. An ephemeral worker checks out the immutable revision, selects a digest-pinned builder profile, resolves lockfile-pinned dependencies through an approved mirror, then builds without general network access. Tests and policy run before publication. The platform pushes one OCI image, records its manifest digest, produces an SPDX SBOM and SLSA provenance bound to that digest, and signs the evidence with workload identity unavailable to build steps. A release controller verifies source repository, revision, builder identity, recipe, parameters, and policy before assigning an environment tag to the same digest. Pull-request builds use separate identities, caches, repositories, and no release authority.

### Connections

This capability consumes image semantics from [PLAT-021](021-container-images-as-platform-artifacts.md) and application/runtime requirements from [PLAT-030](030-mapping-application-needs-to-kubernetes-primitives.md). It hands immutable artifacts to PLAT-032, deployment evidence to delivery capabilities, and operational ownership to observability, security, and software-supply-chain modules.

## Governing Question

What product contract lets application teams obtain fast, repeatable builds while enabling consumers to establish exactly what was built, from which inputs, by which controlled system, under which policy, and with which remaining uncertainty?

A command that compiles code is a mechanism. A platform capability must also define identities, boundaries, inputs, outputs, evidence, failure semantics, service levels, supported recipes, escape paths, and artifact lifecycle. Its purpose is not to centralize every tool choice. Its purpose is to make the common route trustworthy and operable while preserving explicit ownership for exceptions.

The strongest useful question is not “did CI pass?” It is “why should this exact digest be accepted for this use?” Answering requires evidence generated at the authoritative boundary and a consumer policy independent of the producer-controlled steps.

## Why This Matters

Builds sit between human-editable intent and executable production bytes. That position gives them unusual authority. A compromised dependency resolver, builder image, cache, plugin, release credential, or provenance generator can affect many applications even when the source repository is correct.

Builds also dominate developer feedback. A secure design that routinely takes an hour, fails opaquely, or cannot be reproduced locally drives teams toward bypasses. Conversely, a fast pipeline that cannot explain its inputs turns every incident into archaeology. Platform engineering must jointly optimize feedback, evidence, and containment.

Centralization creates leverage and correlated risk. One maintained builder profile can patch thousands of applications, but one malicious profile can compromise the same population. Therefore capability governance, staged profile rollout, tenant isolation, revocation, and transparent ownership are part of the technical design.

Finally, a produced artifact outlives the build worker. The durable result is not the log stream; it is the digest and the evidence required to use, reproduce, investigate, promote, or retire it. The capability is successful when consumers can make reliable decisions after the original worker no longer exists.

## Prerequisites and Retrieval

Retrieve version-control revisions, cryptographic hashes, public-key signatures, workload identity, least privilege, dependency graphs, package managers, lockfiles, container images, OCI manifests and registries, CI workflows, caches, test types, secrets, isolation, network policy, observability, retention, and incident response.

You should distinguish source review from artifact verification; authentication from authorization; a name from content identity; a build recipe from a builder implementation; a package inventory from provenance; compilation success from release eligibility; repeatability on one machine from independent reproducibility; and artifact production from environment-specific deployment.

## Learning Objectives

After completing this module, you should be able to:

1. specify an application-build capability as a versioned platform product;
2. enumerate and control consequential build inputs;
3. separate untrusted validation builds from trusted release builds;
4. design ephemeral isolation, network, secret, and cache boundaries;
5. distinguish hermeticity, repeatability, reproducibility, provenance, SBOMs, and signatures;
6. publish and promote immutable artifacts by digest;
7. construct producer evidence and independent consumer verification policy;
8. balance golden paths, extensibility, latency, cost, and correlated risk; and
9. operate builder profiles, artifacts, evidence, exceptions, and revocation throughout their lifecycle.

## Core Exposition

### Define the capability contract before selecting a pipeline engine

The product contract names supported source systems, languages, artifact types, architectures, builder profiles, dependency sources, policy gates, identities, evidence formats, retention, quotas, service objectives, and support ownership. It also states what application teams own: source correctness, declared dependencies, tests, recipe-specific configuration, vulnerability decisions, and runtime suitability.

Expose a small stable interface. Inputs might be repository plus immutable revision, recipe/profile version, target artifact type, declared parameters, and release intent. Outputs should include result state, artifact digest, evidence locations, test/policy results, logs, timing, and a diagnostic category. The interface should not expose the incidental topology of the current CI engine.

Version the contract. Updating a compiler, base image, buildpack, policy, or evidence predicate can change outputs and acceptance. A profile version lets teams test the successor, compare results, and migrate deliberately. Emergency revocation remains possible, but ordinary change should be observable and staged.

### Inventory every consequential input

Source is more than a branch name. Record repository identity, immutable revision, submodules, generated source, patches, and selected build context. A branch can move between authorization and checkout; the authoritative build must resolve and bind the exact revision.

Dependencies include direct and transitive packages, base images, system packages, plugins, downloaded tools, language runtimes, and generated artifacts. Lockfiles reduce ambiguity only if the resolver enforces them and verifies retrieved content. Repository metadata, yanked packages, mirrors, and platform-specific selection may still affect resolution.

The toolchain includes compiler, linker, package manager, builder frontend, operating-system libraries, and builder image. Pinning only the application dependencies while selecting `builder:latest` leaves a large undeclared variable.

Parameters and environment also matter: target architecture, optimization flags, feature gates, locale, timezone, timestamps, filesystem ordering, user/group IDs, paths, and injected version data. Secrets should authorize access without becoming artifact content; their values usually must not enter provenance, logs, or cache keys.

Represent the declared input closure as $I=S\cup D\cup T\cup R\cup P\cup E$. The actual observations $O$ should satisfy $O\subseteq I$ for a hermetic build. A network fetch, undeclared host file, clock-dependent value, or cross-run cache object outside $I$ violates that condition even if the output happens to be correct.

### Separate validation from release authority

Pull-request code is adversarial with respect to the build platform. It can read its environment, invoke tools unexpectedly, exfiltrate reachable credentials, poison writable caches, consume resources, and craft deceptive output. A contribution build therefore receives no production credentials or protected signing authority.

Use separate identities and trust domains for untrusted validation, protected-branch integration, and releases. A release build should start only from a revision satisfying source policy, on a hosted controlled builder. The platform, not the user script, generates and authenticates provenance after observing the build result.

Approval alone is not isolation. A trusted maintainer can mistakenly approve malicious code, and compromised credentials can authorize it. Minimize the consequence through ephemeral workers, narrow network paths, short-lived workload identity, protected repositories, independent policy, and signing material outside the build step.

Do not pass secrets merely because the workflow file requests them. Identity issuance must consider repository, revision/ref policy, event type, workflow/profile identity, environment, and audience. Prefer short-lived credentials with explicit claims over static registry or signing keys.

### Make workers ephemeral, isolated, and inspectable

Start each run from a known image or machine template. Destroy it after the run. Prevent one tenant or run from influencing another through processes, filesystems, networks, devices, metadata services, environment variables, or residual credentials. Stronger release tiers warrant stronger isolation than low-risk preview builds.

Run user-defined steps without privileged host sockets. A container that can control the host container daemon effectively controls the worker and often other credentials. Root inside a strongly isolated guest may be acceptable under a threat model; root plus a shared host control socket usually is not.

Bound CPU, memory, storage, process count, time, log volume, and concurrency. Resource controls protect service availability and make cost visible. They do not replace tenant isolation because kernel or runtime vulnerabilities may cross a shared boundary.

Retain enough telemetry for investigation without retaining secrets. Record worker/profile identity, run identity, source revision, lifecycle timings, network decisions, cache decisions, artifact digests, policy results, and evidence generation. Avoid dumping the entire environment.

### Control dependency resolution and network access

A fully networkless build is easiest to reason about after an explicit fetch stage has assembled verified dependencies. Where that is impractical, restrict egress to approved mirrors and services, authenticate them, record resolved digests, and monitor unexpected destinations.

Mirrors improve availability, policy, and incident response, but become trusted infrastructure. Define synchronization delay, integrity verification, namespace rules, malware response, deletion/yank handling, upstream outage behavior, and emergency deny policy. A mirror is not automatically safer than upstream.

Dependency pinning and freshness are different goals. Exact versions improve reconstruction; automated reviewed updates reduce exposure to known defects. The build capability should enforce deterministic resolution while a separate dependency-maintenance workflow proposes controlled changes.

Fail closed when a required dependency cannot be verified. A silent fallback from an approved mirror to the public Internet changes both the input set and the trust boundary.

### Partition caches as untrusted inputs

Caching can transform feedback time, but a cache hit is an input decision. Its key must cover every factor that affects the cached output: source subset, dependency lock, toolchain/profile, platform, parameters, and format version. Weak keys produce plausible but wrong artifacts.

Separate untrusted pull-request caches from protected/release caches. Prefer immutable content-addressed entries and verify their digests. A trusted build may consume a lower-trust cache only if it independently validates the cached product or treats the entry as a performance hint that cannot alter correctness.

Do not store secrets in build layers or exported caches. Dedicated secret mounts should be excluded from the filesystem snapshot. Do not use build arguments for confidential values when tooling records them in metadata or layers.

Measure hit rate alongside correctness, storage cost, eviction, transfer latency, and poisoning signals. A high hit rate with cross-tenant contamination is failure, not efficiency.

### Distinguish repeatability, hermeticity, and reproducibility

A **repeatable** build succeeds again under a similar controlled setup. A **deterministic** transformation produces the same output for the same modeled inputs. A **hermetic** build cannot observe undeclared inputs. A **reproducible** build lets another party recreate byte-identical specified artifacts from the same source, build instructions, and relevant environment.

These properties reinforce but do not imply one another. A hermetic build can deterministically produce malicious bytes. A non-hermetic build may coincidentally repeat. A reproducible build can prove correspondence between source and bytes only when an independent rebuild and comparison actually occur.

Control common nondeterminism: timestamps, archive member order, filesystem traversal, locale, timezone, random seeds, absolute paths, usernames, parallel race ordering, generated identifiers, and signatures embedded before comparison. Use a declared source timestamp when formats require time.

Test reproducibility across meaningfully independent environments and perturb irrelevant variables. Two runs reusing the same contaminated cache and builder are weak evidence. Record what artifacts are compared and any normalized fields; do not call a semantic comparison byte reproducibility.

### Build once, identify by digest, and promote

Publish the artifact after required build-local checks pass. OCI artifacts are content addressed: descriptors bind media type, size, and digest, while manifests bind configuration and layers. A registry tag is a mutable human-readable pointer and may refer to different manifests over time.

The deployment record should carry a digest such as `registry.example/app@sha256:...`. A tag like `release-2026-09` can aid discovery, but policy and rollback must retain the resolved digest. Verification recalculates or relies on registry content-addressing rules and compares the expected digest.

Build once and promote the same digest. Rebuilding for staging and production introduces different toolchains, dependency availability, clocks, or source state and breaks the evidence chain. Environment configuration belongs in deployment/runtime mechanisms unless an artifact must intrinsically differ.

Multi-platform image indexes need care: the index has its own digest and references platform-specific manifests. State whether policy attests the index, each manifest, or both, and ensure the consumer verifies the object it will execute.

### Generate evidence at the authoritative boundary

Provenance answers how an artifact was produced. It should bind subject digests to builder identity, build type, invocation, parameters, and resolved dependencies using the chosen predicate. The exact completeness and authenticity guarantees depend on the build platform and SLSA level; existence alone is only an initial step.

An in-toto attestation separates subject, predicate type, typed predicate, and authentication envelope/bundle. This lets policy distinguish an SBOM claim from provenance or test evidence. Do not accept arbitrary predicates merely because their envelope signature is valid.

An SPDX SBOM communicates components, relationships, licenses, provenance/integrity metadata, and other BOM information. Generate it as close to the authoritative build as possible, preserve package/file identifiers, and bind it to the exact subject. Compare generator observation with the actual packaged output when feasible.

A signature authenticates bytes or a statement under a trust root. It does not make the signed claim true, make the signer authorized, or make the artifact safe. Verification must check signature validity, subject digest, certificate/key identity, issuer, predicate, time/transparency evidence where required, and policy authorization.

Keep the platform signing identity inaccessible to user steps. The evidence service should observe an authenticated result, construct canonical claims, sign with short-lived workload identity or protected keys, publish atomically enough to prevent substitution, and expose auditable failures.

### Make consumer verification a separate control

Producer success is not consumer acceptance. Define an expectation $X$ over the artifact and evidence. A simplified decision is:

$$
\operatorname{accept}(a,v,X)=\operatorname{integrity}(a)\land\operatorname{authentic}(v)\land\operatorname{subject}(v)=\operatorname{digest}(a)\land X(v).
$$

The expectation can require an allowed source repository and revision policy, protected builder identity, approved build type/profile, admitted parameters, required dependency and material completeness, vulnerability/test policy, and an authorized release decision.

Verification should happen at promotion and again at consequential consumption, such as admission or package installation. Cache the result carefully, bound to the policy version and digest. Failures need an owned diagnostic path and tightly controlled, time-bounded break-glass—not a permanent “skip verification” switch.

Policy changes require compatibility planning. If today’s evidence is retained but tomorrow’s verifier rejects its predicate or trust root, rollback and incident reconstruction may fail. Preserve verifier versions, trust-root history, policy decisions, and evidence bundles according to retention requirements.

### Integrate tests and policy without confusing their claims

Unit, integration, static analysis, license, vulnerability, secret, and configuration checks answer different questions. Define which are advisory, merge-blocking, build-blocking, release-blocking, or deployment-blocking. A scanner outage needs an explicit availability policy; silently passing is rarely acceptable.

Run cheap deterministic checks early for feedback and expensive environment-dependent checks later. Parallelize independent checks, cancel obsolete runs, and avoid rebuilding the artifact in each stage. Tests should consume the same candidate digest or a clearly related intermediate when their result is used for release.

Record evidence with scope: which revision, artifact digest, test suite version, policy version, database snapshot, and environment produced the result. “Tests passed” without a subject and context is not reusable release evidence.

Vulnerability findings change after build as databases and exploit knowledge evolve. Build-time scanning is a snapshot, not permanent safety. Artifact management must support continuous reassessment, notification, rebuild, quarantine, and revocation.

### Design the developer experience as part of correctness

Provide a discoverable default with minimal required configuration, clear local parity, explainable logs, typed failure categories, estimated queue/runtime, retry semantics, and links from an artifact to inputs and evidence. Hide infrastructure complexity, not trust decisions.

Fast feedback comes from small contexts, dependency prefetch, safe caches, parallelism, incremental computation, worker right-sizing, and cancellation—not from weakening identity or evidence. Report queue time separately from execution and upload time so ownership is visible.

Support controlled extensions. Prefer declarative parameters, approved buildpacks/plugins, and versioned custom profiles before arbitrary privileged scripts. Each extension declares inputs, output contract, isolation tier, maintenance owner, and migration path.

An escape path is a product feature. Teams with unsupported toolchains can use a quarantined custom-build contract that still emits immutable artifacts and minimum evidence. Track exceptions by owner, expiry/review date, risk, usage, and intended durable support decision.

### Operate the capability and its blast radius

Define SLOs for request acceptance, queue delay, successful infrastructure execution, artifact publication, evidence availability, and diagnostic latency. Separate platform faults from application compilation/test failures. High application failure rate is not necessarily platform unavailability.

Roll builder profiles through canaries. Rebuild a representative corpus, compare artifacts and timings, inspect evidence schema, then expand. Retain the old profile long enough for controlled rollback unless it is revoked for security.

Maintain an inventory from application to profile, base/toolchain digest, artifact digest, evidence, owner, and release channels. When a base image or toolchain is compromised, query affected artifacts, block new use, rebuild from controlled inputs, verify replacements, and revoke or quarantine old digests.

Retention spans artifacts, evidence, logs, caches, and source availability. Evidence without its artifact is hard to use; an artifact without evidence may be unacceptable; a cache is disposable; sensitive logs may require shorter retention. State each lifecycle independently.

Capacity planning models arrival rate $\lambda$, mean worker service time $W$, concurrency $m$, resource class, and burst. Approximate offered work is $\lambda W$ worker-equivalents, but queue objectives require headroom for variance, failures, large builds, architecture partitions, and maintenance. Fair scheduling prevents one repository from monopolizing the fleet.

The following synthetic inventory demonstrates how a capability owner can audit heterogeneous build workflows without mistaking flags for assurance.

<!-- bijux-verify: {"id":"build-capability-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"builds=8\nisolated=7\nnetworkless=4\npinned=7\nprovenance=6\nsbom=6\nsigned=5\ntrusted_release=4\n","stderr":""}} -->
```python
builds = [
    {"name": "api-release",    "isolated": True,  "networkless": True,  "pinned": True,  "provenance": True,  "sbom": True,  "signed": True,  "trusted_release": True},
    {"name": "worker-release", "isolated": True,  "networkless": True,  "pinned": True,  "provenance": True,  "sbom": True,  "signed": True,  "trusted_release": True},
    {"name": "web-preview",    "isolated": True,  "networkless": False, "pinned": True,  "provenance": True,  "sbom": True,  "signed": False, "trusted_release": False},
    {"name": "mobile-release", "isolated": True,  "networkless": False, "pinned": True,  "provenance": True,  "sbom": True,  "signed": True,  "trusted_release": True},
    {"name": "docs-preview",   "isolated": True,  "networkless": True,  "pinned": True,  "provenance": True,  "sbom": True,  "signed": False, "trusted_release": False},
    {"name": "legacy-local",   "isolated": False, "networkless": False, "pinned": False, "provenance": False, "sbom": False, "signed": False, "trusted_release": False},
    {"name": "firmware-release","isolated": True, "networkless": True,  "pinned": True,  "provenance": False, "sbom": False, "signed": True,  "trusted_release": True},
    {"name": "cli-candidate",  "isolated": True,  "networkless": False, "pinned": True,  "provenance": True,  "sbom": True,  "signed": True,  "trusted_release": False},
]

print(f"builds={len(builds)}")
for field in ("isolated", "networkless", "pinned", "provenance", "sbom", "signed", "trusted_release"):
    print(f"{field}={sum(build[field] for build in builds)}")
```

The counts reveal gaps for prioritization. They do not establish that any flag is implemented correctly or that a workflow meets a SLSA level, security objective, or release policy.

## Definitions and Notation

Let:

- $S$ be immutable source inputs;
- $D$ be resolved dependency materials;
- $T$ be the toolchain and builder implementation;
- $R$ be the versioned build recipe;
- $P$ be declared build parameters;
- $E$ be relevant environment attributes;
- $N$ be the admitted network/input policy;
- $C$ be selected cache inputs;
- $Q$ be required tests and policies;
- $A$ be produced artifacts;
- $V$ be provenance, SBOMs, signatures, and other typed evidence; and
- $X$ be the consumer's independent acceptance expectation.

The modeled build is $F(S,D,T,R,P,E,N,C,Q)=(A,V)$. This is a specification boundary, not a claim that the implementation is purely functional. Hidden clocks, files, services, races, and caches make observed execution state larger than the declared tuple.

For one artifact $a$, $d(a)=H(\operatorname{bytes}(a))$ is its content digest under approved collision-resistant hash $H$. Content addressability requires a consumer to bind decisions to $d(a)$, not merely a tag $t$ where $t\mapsto d(a)$ may change.

Let $M(v)$ be the material set recorded by provenance and $O$ the actual consequential inputs. Completeness seeks $O\subseteq M(v)$; accuracy seeks that recorded identities and digests match what execution observed. Authenticity of $v$ is separate from both properties.

For reproducibility, two sufficiently independent executions with equivalent declared inputs should produce specified artifacts $a_1,a_2$ such that $d(a_1)=d(a_2)$. One equality is evidence for the tested boundary, not a universal proof of determinism or absence of compromise.

## Mechanisms, Invariants, or Proof Structure

The assurance chain is:

1. authorize an immutable source revision under source policy;
2. select a versioned builder profile and declared input policy;
3. execute in an isolated ephemeral environment with bounded authority;
4. resolve or admit verified materials and partitioned cache inputs;
5. run the recipe and required tests/policies;
6. publish artifacts under content digests;
7. generate authenticated typed evidence at the platform boundary;
8. independently verify artifact, subject, identity, predicate, inputs, and release expectation; and
9. promote the same accepted digest and retain lifecycle evidence.

The structure is compositional, not a mathematical proof of safe software. Each link supplies a narrower guarantee. Hashes detect changed bytes under algorithm assumptions. Signatures authenticate under key/identity and trust-root assumptions. Provenance reports build facts under builder integrity and completeness assumptions. Reproducible comparison detects some divergence under independence assumptions. Tests and scanners cover only their modeled behaviors and current knowledge. Consumer policy turns these claims into a use-specific decision.

Key invariants are input closure, cross-run isolation, authority separation, digest identity, subject binding, typed claim interpretation, fail-closed required gates, build-once promotion, cache trust partitioning, and owned revocation. Violate any one and a green pipeline may still publish an unacceptable artifact.

## Alternatives and Trade-Offs

**Dockerfile-like recipes versus buildpacks:** explicit recipes maximize control and visibility but can duplicate hardening and maintenance. Buildpacks provide curated detection, layers, SBOM integration, and rebasing, but add lifecycle/profile governance and may constrain unusual builds. Support both behind one evidence contract when warranted.

**Shared workers versus dedicated isolation:** shared ephemeral workers improve utilization and elasticity. Dedicated guests or hardware reduce cross-tenant exposure and support sensitive workloads at greater cost and startup latency. Assign tiers from threat, secret, privilege, and compliance needs.

**Online resolution versus prefetched hermetic builds:** online resolution is simpler and fresher but expands nondeterminism and egress. Prefetch/freeze stages improve auditability and offline reconstruction but add storage, mirroring, and workflow complexity.

**Central profiles versus repository-owned toolchains:** central profiles enable patching, consistency, support, and fleet evidence. Repository ownership improves autonomy and specialty support but distributes maintenance and may enlarge trust. A stable minimum contract plus governed custom profiles avoids a false binary.

**Key-based versus identity-based signing:** long-lived keys support offline and private environments but demand rotation, custody, and compromise response. Short-lived identity certificates reduce static secret handling but depend on identity providers, claims, transparency/time services, and trust-root availability.

**Strict gates versus advisory evidence:** strict gates prevent known violations but can halt delivery during service/database failure and create bypass pressure. Advisory results preserve flow but transfer risk to consumers. Classify each policy by consequence, freshness, availability behavior, and exception authority.

**Rebuild promotion versus build-once promotion:** rebuilding can incorporate environment-specific content but breaks artifact identity and multiplies uncertainty. Build once whenever differences are configuration; create separately identified variants only when the executable artifact truly must differ.

## Failure Modes and Misconceptions

- **“The branch was protected, so the artifact is trusted.”** Checkout, dependencies, builder, credentials, and publication remain separate attack surfaces.
- **“The tag identifies what passed.”** Tags can move; preserve and verify the manifest or artifact digest.
- **“A valid signature means safe software.”** It authenticates a payload under a trust decision; it does not validate source behavior or predicate truth.
- **“An SBOM proves provenance.”** An inventory and a production history answer different questions and require subject binding.
- **“The lockfile makes the build hermetic.”** Toolchains, base images, network services, environment, generated code, and caches may remain undeclared.
- **“A hosted runner is automatically isolated.”** Isolation strength, persistence, privileges, network, metadata services, and secret exposure require explicit assessment.
- **“Cache hits cannot affect correctness.”** Cached outputs are inputs; weak keys and cross-trust writes can substitute bytes.
- **“Two matching builds prove reproducibility.”** They support a scoped claim only if inputs and environments are sufficiently independent and comparison is byte-exact.
- **“Tests can run against any equivalent rebuild.”** A different digest is a different release candidate unless correspondence is explicitly established.
- **“A scanner passed at build time, so no later action is needed.”** vulnerability knowledge and policy change after publication.
- **“No network is always enough.”** Prefetched materials, builder images, caches, and host state also require integrity and declaration.
- **“The golden path should prohibit all exceptions.”** Unsupported needs will move outside visibility; governed minimum contracts and explicit escape paths preserve evidence.
- **“Keep every artifact just in case.”** Unlimited retention raises cost, exposure, and ownership ambiguity; legal, rollback, investigation, and deletion needs must be modeled.

## Worked Examples

### Example 1

A team builds `main` by tag and deploys `app:latest`. The tag can resolve to different bytes at build, scan, and deploy time. The capability resolves the source revision, publishes the OCI manifest, records digest `sha256:d1`, binds scan/provenance/SBOM evidence to `d1`, and deploys `app@sha256:d1`. A friendly release tag may also point to `d1`. Conclusion: human names aid navigation; the digest is the decision identity.

### Example 2

A pull request changes the build script to print environment variables and upload them. If the job receives a registry password and provenance key, review code has release authority. The platform instead gives PR jobs an isolated identity, read-only dependency access, a PR cache namespace, and a preview repository; protected release jobs use a hosted profile and platform-side evidence signer. Conclusion: event/ref approval and execution authority must be separated.

### Example 3

A project pins language packages but uses `ubuntu:latest` and downloads a compiler install script. Its lockfile is stable while the OS packages and compiler move. The team pins the builder/base digests, verifies the compiler material, records both in provenance, and schedules automated updates. Conclusion: the declared dependency closure includes toolchain and base materials, not only application packages.

### Example 4

A build depends on a public package registry. General egress is disabled after a fetch job retrieves lockfile-selected packages through an approved mirror and verifies their digests. The build consumes the frozen bundle offline. If the mirror cannot supply a verified package, the run fails instead of falling back to public resolution. Conclusion: availability fallback must not silently change the trust boundary.

### Example 5

A release cache key contains only the repository name. A malicious PR writes a compiled object with that key; the release later reuses it. Partitioning cache namespaces blocks the write, while a stronger key includes source subset, toolchain/profile digest, target, flags, and cache format. Release builds verify content-addressed entries. Conclusion: cache design is part of supply-chain integrity.

### Example 6

Two builds differ because archives embed current time, filesystem order, and an absolute workspace path. The recipe sorts inputs, uses a declared source timestamp, strips/remaps build paths, fixes locale/timezone, and compares outputs from independent clean workers. Matching digests then support a defined reproducibility claim. Conclusion: reproducibility requires a stated perimeter and deliberate nondeterminism control.

### Example 7

A pipeline emits an SBOM JSON beside an image, but neither document identifies the image digest. A later rebuild overwrites the tag, leaving the SBOM ambiguous. The evidence generator creates an in-toto statement whose subject is the manifest digest and whose typed predicate contains the SPDX BOM, then authenticates it. Conclusion: evidence is useful only when subject, predicate, and authenticity are unambiguous.

### Example 8

A valid provenance signature says the artifact came from `experimental-builder` using an unreviewed recipe. Cryptographic verification passes, but release policy permits only `platform/release-v7`, protected repositories, and networkless resolution. The consumer rejects it. Conclusion: authenticity answers who made the claim; authorization policy decides whether that claim is acceptable.

### Example 9

The same source is rebuilt once for staging and once for production. A package disappears between runs, producing different digests. The capability instead builds one candidate, tests and attests that digest, then promotion controllers assign staging and production channel metadata to it after policy checks. Conclusion: environment progression should preserve artifact identity.

### Example 10

A base-image incident identifies digest `sha256:b0`. The platform inventory maps `b0` through provenance materials to 214 application artifacts and their owners. New acceptance is denied, rebuilds use patched base `b1`, replacement digests are verified and promoted, and old digests are quarantined according to risk. Conclusion: build capability ownership continues through impact analysis, rebuild, and revocation.

## Cross-Program Connections

- **Software Engineering Patterns:** build recipes and capability interfaces separate stable contracts from replaceable pipeline implementations.
- **Operating Systems:** process, filesystem, namespace, privilege, and resource isolation determine the real worker boundary.
- **Computer Security:** least privilege, signing, trust roots, policy, adversarial inputs, and revocation underpin artifact acceptance.
- **Distributed Systems:** queues, retries, idempotency, immutable identifiers, consistency, and partial failure shape hosted build execution.
- **Data Engineering:** lineage and schema thinking transfer directly to provenance, SBOMs, evidence evolution, and impact queries.
- **API and Service Engineering:** versioned build APIs need idempotency, typed failures, quotas, observability, and lifecycle compatibility.
- **Reliability Engineering:** SLOs, capacity, canaries, incident response, and dependency failure govern the capability as a service.
- **Formal Methods:** input closure, invariants, and independently checked expectations clarify what evidence can and cannot establish.

## References

1. Supply-chain Levels for Software Artifacts, “SLSA Specification v1.2” and “Build Track Basics,” approved current specification, retrieved 2026-09-02. https://slsa.dev/spec/v1.2/
2. Open Container Initiative, “Image Format Specification,” current specification, retrieved 2026-09-02. https://github.com/opencontainers/image-spec
3. Open Container Initiative, “Distribution Specification,” current specification, retrieved 2026-09-02. https://github.com/opencontainers/distribution-spec
4. in-toto, “Attestation Framework Specification v1.2,” current specification, retrieved 2026-09-02. https://github.com/in-toto/attestation/blob/main/spec/README.md
5. SPDX Project, “SPDX Specification 3.0.1,” current specification, retrieved 2026-09-02. https://spdx.github.io/spdx-spec/v3.0.1/
6. Sigstore, “Verifying Signatures with Cosign,” official documentation, retrieved 2026-09-02. https://docs.sigstore.dev/cosign/verifying/verify/
7. National Institute of Standards and Technology, “Secure Software Development Framework (SSDF) Version 1.1,” NIST SP 800-218, February 2022. https://doi.org/10.6028/NIST.SP.800-218
8. Reproducible Builds, “Definitions” and “Making Plans,” project documentation, retrieved 2026-09-02. https://reproducible-builds.org/docs/definition/
9. Cloud Native Buildpacks, “Lifecycle” and API specifications, official documentation, retrieved 2026-09-02. https://buildpacks.io/docs/for-platform-operators/concepts/lifecycle/
10. Docker, “BuildKit” and “Cache Storage Backends,” official documentation, retrieved 2026-09-02. https://docs.docker.com/build/cache/backends/
11. Tekton, “Chains: Artifact Signatures and Attestations,” official documentation, retrieved 2026-09-02. https://tekton.dev/docs/chains/
12. Kubernetes, “Application Security Checklist,” official documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/security/application-security-checklist/

## Exercises

### Exercise 1

Define artifact digest, provenance, SBOM, signature, hermetic build, reproducible build, and promotion. For each, state one guarantee it does not provide.

### Exercise 2

Trace a protected release from immutable source revision through consumer acceptance. Name the identity and trust boundary at every step and identify where user-defined code must not hold signing authority.

### Exercise 3

A release workflow uses a shared writable cache with pull requests, resolves `builder:latest`, downloads packages from unrestricted Internet, pushes `app:stable`, creates an unsigned SBOM referring only to that tag, and then rebuilds for production. Diagnose at least six distinct violations and propose a corrected design.

### Exercise 4

Compare online dependency resolution with prefetched networkless builds for a company supporting 500 repositories across four language ecosystems. Design a two-tier capability that balances feedback latency, mirror availability, reconstruction, and release assurance.

### Exercise 5

A newly disclosed compiler compromise affects one builder profile used during the last 90 days. Design the investigation and recovery workflow, including inventory queries, acceptance policy, evidence, rebuild ordering, communication, rollback constraints, and retirement of affected artifacts.

## Answers to the Exercises

### Answer 1

A digest identifies exact bytes under a hash assumption but says nothing about origin or safety. Provenance reports builder/process/inputs but does not prove source correctness or completeness unless the builder provides those guarantees. An SBOM inventories components/relationships but does not prove the artifact was built only from them. A signature authenticates bytes or claims under a trust root but does not authorize the signer or establish claim truth. Hermeticity excludes undeclared observations but does not make inputs benign. Reproducibility permits byte-identical recreation under a declared perimeter but does not prove both builds uncompromised. Promotion advances an existing digest but does not itself establish that the digest meets policy.

### Answer 2

The source system authenticates authors/reviewers and resolves an immutable accepted revision. An orchestration identity requests a declared profile for that revision. The build platform authenticates the request, issues an ephemeral worker identity, and runs user code inside the isolated worker with only admitted material/network access. A platform observer receives the result, computes the artifact digest, and generates provenance/SBOM statements. A signer identity outside user steps authenticates those statements and publication uses a narrowly scoped registry identity. A release controller authenticates an authorized release decision. Finally, the consumer verifies digest, signature/certificate issuer and identity, predicate/subject, allowed source/builder/parameters/materials, and release policy. User code never receives the provenance signer, protected registry promotion, or production deployment authority.

### Answer 3

The shared writable cache permits lower-trust poisoning; partition it and use complete content-addressed keys plus verification. `builder:latest` leaves the toolchain movable; pin a builder/profile digest and record it. Unrestricted Internet makes inputs open-ended; prefetch verified materials or restrict resolution to authenticated mirrors and record digests. `app:stable` is a mutable name; retain and verify the manifest digest. The SBOM lacks authenticated subject binding; put the exact digest in a typed attestation and authenticate it. Rebuilding for production creates a new candidate; promote the tested digest instead. Additional defects include absent provenance, unclear source revision, unprotected signing, and no independent acceptance policy. The corrected release uses an accepted immutable revision, isolated hosted builder, pinned inputs, partitioned cache, bounded network, artifact digest, platform-generated signed provenance and SBOM, policy verification, and build-once promotion.

### Answer 4

Tier one serves untrusted and ordinary feedback builds with isolated ephemeral workers, ecosystem-specific read-through mirrors, pinned lockfile enforcement, separate cache namespaces, bounded egress, no release credentials, and preview artifacts. It optimizes queue/startup/cache performance and reports all resolved materials. Tier two serves protected releases: an explicit fetch stage freezes and verifies dependencies from managed mirrors, the build runs networkless where toolchains permit, builder profiles are digest-pinned, caches are trusted/read-only or independently verified, and platform evidence is authenticated. Mirror policy defines integrity, synchronization, yanks, outage behavior, and no silent upstream fallback. Teams can reproduce from retained material bundles and profile definitions. Languages not yet networkless use restricted observed egress with a time-bound exception and the same minimum digest/evidence contract.

### Answer 5

First revoke or deny the compromised profile/toolchain in new consumer policy and stop promotion of newly affected digests. Query provenance materials and the application/profile inventory for the compiler digest, time interval, repositories, artifact digests, releases, environments, and owners; do not infer impact from tags. Preserve evidence, logs, trust roots, and source/profile definitions. Prioritize Internet-facing, privileged, widely distributed, and critical artifacts, then rebuild accepted source revisions on a clean patched profile with fresh trusted dependencies and isolated caches. Compare outputs where meaningful, generate new provenance/SBOMs/signatures, rescan, and independently verify replacements. Communicate affected and replacement digests, exposure, actions, and uncertainty. Promotion must preserve environment compatibility; rollback cannot select an affected digest merely because it was previously stable. Quarantine or revoke old artifacts, update admission/package policy, monitor attempted use, retain incident evidence, and retire the compromised profile only after the affected inventory has an owned disposition.
