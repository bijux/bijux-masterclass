---
module_id: SARCH-027
program: Software Engineering: Software Architecture
level: 1
module_number: 27
title: Development and Build Views
status: complete
last_verified: 2026-09-06
---

# Development and Build Views

## One-Page Review

### Governing question

How can an architecture description expose how people and automation organize, change, generate, verify, package, and trace software so that source responsibilities become trustworthy deployable artifacts without hidden dependencies or irreproducible steps?

### Essential definitions

- A **development element** is a source-owned unit such as a repository, package, module, interface definition, test suite, configuration source, or generator.
- A **source revision** is an immutable identity for a selected state of version-controlled source.
- A **dependency** is an input required to interpret, build, test, package, or run another element.
- A **build step** transforms declared inputs under a declared toolchain and environment into outputs or explicit failure.
- A **build graph** is a directed dependency graph whose nodes are inputs, transformations, checks, and artifacts.
- A **generated source** or artifact is output produced by a generator; its authority depends on the governed source and generation process.
- A **hermetic build** is isolated from undeclared inputs according to a stated boundary; hermeticity does not by itself imply reproducibility or security.
- A **reproducible build** allows independent parties, given the same declared source, environment, and instructions, to recreate bit-for-bit identical specified artifacts.
- **provenance** is verifiable information about where, when, how, and from which inputs an artifact was produced.
- A **software bill of materials** records identified software components and relationships for a defined artifact or product scope; it is an inventory, not proof of safety.

### Central model, mechanism, or theorem

Model production as a directed graph

$$
B=(I,T,A,E,O,P,V),
$$

where $I$ is immutable inputs, $T$ transformations and checks, $A$ outputs, $E$ dependency edges, $O$ ownership, $P$ build and security policy, and $V$ evidence such as results, digests, signatures, and provenance.

For an acyclic build graph with duration $w(v)\ge0$, earliest completion satisfies

$$
C(v)=w(v)+\max_{u\in pred(v)}C(u),
$$

with maximum zero for a source node. This calculates the modeled critical path; cache misses, queueing, contention, retries, and dynamic discovery require additional evidence.

### Critical invariants

- declare product, source, generated, test, toolchain, artifact, and ownership boundaries;
- map architectural modules to source units without assuming repository equals component;
- use immutable identities for source, dependencies, toolchains, build instructions, and outputs;
- make every consequential build input and network dependency explicit;
- keep the build graph acyclic or distinguish intentional bootstrap stages;
- separate generation source, generated output, review authority, and regeneration policy;
- isolate untrusted input and least-privilege build credentials, workers, caches, and publication paths;
- verify checks and provenance against policy before artifact promotion;
- distinguish repeatable, reproducible, hermetic, deterministic, and trusted builds;
- model developer workflow, continuous integration, release, recovery, and degraded operation;
- reconcile build outputs with deployment, runtime, data, security, and operational views;
- bind claims to versioned graph, environment, results, artifacts, and evidence limits.

### Common failures

Common failures include equating repository, package, service, team, and deployment unit; hiding generated code and toolchains; downloading mutable dependencies during a build; trusting filenames or version tags as immutable identity; allowing source changes to bypass owners and checks; storing secrets in source or logs; giving untrusted builds publication credentials; treating a passing build as correct software; calling one repeated local build reproducible; confusing provenance presence with provenance verification; publishing before checks finish; and making rollback depend on artifacts or tools that were not retained.

### Compact example

Two builds use the same source revision but resolve dependency range `library>=2` at different times. One obtains version 2.4 and the other 2.5, producing different artifacts. The source revision alone does not define the build. Lock the dependency identity, record toolchain and environment, isolate undeclared network access, and bind provenance to the output digest.

### Connections

[SARCH-022](022-module-and-code-views.md) supplies static implementation structure; [SARCH-025](025-deployment-views.md) consumes immutable artifacts; [SARCH-026](026-data-and-information-views.md) supplies provenance and metadata semantics. [SARCH-028](../ROADMAP.md) next develops operational views. Software Delivery, Platform, Security, Testing, Compiler, and Programming-Language programs deepen the mechanisms.

## Governing Question

An architecture exists not only in running components but in the system that produces them. Repository boundaries affect ownership. Package dependencies affect change and vulnerability exposure. Build graphs affect feedback time and repeatability. Generators affect review authority. CI workers, caches, registries, and credentials affect supply-chain trust.

The governing problem is to show how an intended source change becomes a specific artifact under controlled inputs, transformations, checks, and authorities. The view must support development flow and independent verification without pretending that automation alone proves correctness.

## Why This Matters

Production failures often originate before deployment: an undeclared compiler changes output; generated code is stale; a transitive dependency is replaced; a cache crosses trust boundaries; a test result applies to a different artifact; a signing key is available to unreviewed code; or a rollback artifact cannot be reconstructed.

Development structure also shapes modifiability. A shared package with unstable responsibilities forces synchronized changes. A repository split across one atomic invariant makes safe change difficult. Slow feedback encourages batching and bypass. Ambiguous ownership leaves interfaces and generated outputs ungoverned.

A development and build view lets architects reason about change locality, feedback, reproducibility, supply-chain security, artifact identity, and recovery. It connects human collaboration to machine transformations and provides the correspondence needed to ask whether the artifact tested is the artifact deployed.

## Prerequisites and Retrieval

Retrieve module, package, repository, workspace, source revision, dependency, interface, generated code, toolchain, environment, build step, graph, artifact, digest, cache, test, policy, credential, runner, registry, provenance, attestation, signature, reproducibility, hermeticity, deterministic behavior, bill of materials, publication, promotion, rollback, and conformance.

From prior modules, retrieve architecture decisions, modifiability and testability tactics, module/code views, deployment views, information provenance, trust boundaries, and quality evidence. Distinguish human-reviewed source, fetched dependency, generated intermediate, test result, release record, and deployable artifact.

## Learning Objectives

After completing this module, you should be able to:

1. define development elements, source revisions, dependencies, build steps, artifacts, and provenance;
2. map architectural modules to repositories, packages, owners, interfaces, and deployment units;
3. construct and review an acyclic build graph with explicit immutable inputs;
4. compute a modeled critical path and explain its evidence limits;
5. distinguish deterministic, repeatable, reproducible, hermetic, and trusted builds;
6. govern generated code, caches, dependencies, toolchains, and build credentials;
7. bind tests, attestations, bills of materials, and promotions to artifact identities;
8. compare monorepository, multirepository, local, remote, and staged build arrangements;
9. design build recovery and operation when network, registry, workers, or signing services fail;
10. reconcile development and build views with runtime, deployment, security, and operations.

## Core Exposition

**Frame the concern.** State product scope, stakeholders, lifecycle state, source boundary, artifact boundary, environment, and decision. Developers may need package dependencies and feedback paths. Security reviewers need trust and credential boundaries. Release engineers need promotion and recovery. Auditors need correspondence from approved source to deployed digest.

ISO/IEC/IEEE 42010:2022 remains the current published architecture-description edition as checked on 2026-09-06 [1]. It supports concern-governed model kinds and correspondences; it does not prescribe repository layout or a pipeline product. Development structure and build flow may need separate linked projections.

**Map architecture to development elements.** Identify repositories, workspaces, packages, modules, interface definitions, migrations, policy sources, tests, documentation, generators, and ownership. Relate them to architectural responsibilities. Do not assume one repository equals one service, one package equals one component, or one team owns every artifact it deploys.

A development dependency means one source element requires another to compile, generate, test, configure, or understand. Label dependency kind and stability. Public API, implementation-only dependency, generated contract, test fixture, shared configuration, and build plugin create different change consequences.

**Choose repository boundaries by change and authority.** A monorepository can support atomic cross-package change, shared tooling, and whole-tree analysis, but needs scalable ownership, selective builds, and dependency enforcement. Multiple repositories can isolate authority and release cadence, but distributed changes require compatibility windows and cross-repository evidence.

Repository topology should not substitute for modularity. A monorepository can contain tightly coupled code; separate repositories can share an unstable runtime contract. Record allowed dependency directions, interface owners, review rules, release relationships, and exceptions.

**Use immutable identities.** Bind a build to source revision, dependency digests, toolchain, build instructions, configuration, environment image, generators, reference data, and output digest. Human-readable versions and tags aid discovery but may move or collide. Immutability is scoped: an identifier is useful only if its issuing authority and canonical bytes are defined.

Retain enough metadata to reproduce or diagnose a build. Environment variables, locale, timezone, filesystem ordering, timestamps, random seeds, network responses, and processor behavior can affect output. Either make them declared inputs, normalize them, or state that the result is not reproducible.

**Construct the build graph.** Nodes represent immutable inputs, transformations, checks, and outputs. Edges mean “required as input,” not merely temporal sequence. Each transformation records command or action identity, toolchain, environment, inputs, outputs, expected failure behavior, resources, owner, and evidence.

The graph should be acyclic for one build evaluation. A source generator needing a compiler built by that generator creates a bootstrap problem; model trusted seed, bootstrap stages, and verification separately rather than hiding the cycle. Dynamic dependency discovery must produce an explicit graph or recorded input set before a strong completeness claim.

**Make generated material governed.** Identify the authoritative source: schema, interface definition, grammar, model, templates, or generator code. State whether generated output is committed, reviewed, formatted, reproducible, and checked for freshness. Editing generated output directly creates divergence unless policy explicitly treats it as authoritative.

Generated code can execute in consumers with broad privilege. Review generator changes, templates, plugins, and inputs according to their reach. A small generator dependency can alter many artifacts. Bind generator version and output digest to provenance.

**Control dependencies.** Record direct and resolved transitive identities, source and registry, license, integrity, platform variants, optional features, and update policy. A lock file is useful evidence but does not prove the registry served trustworthy content or that the dependency is safe.

Use authenticated sources, integrity verification, controlled mirrors, review of high-risk changes, and reproducible retrieval where appropriate. Build scripts and compiler plugins are executable dependencies, not inert metadata. Separate dependency resolution from execution when this reduces authority.

**Distinguish build properties.** A deterministic build produces the same outputs for the same inputs within a specified model. A repeatable build can be repeated by the same party or environment. A reproducible build permits another party to reconstruct bit-for-bit identical specified artifacts from the declared source, environment, and instructions [4].

A hermetic build is isolated from undeclared input according to a boundary. Hermeticity supports reasoning about inputs but can deterministically produce malicious output. Reproducibility can detect unexplained differences but does not show the source is correct. Trust also depends on source control, review, builder isolation, provenance authenticity, verification policy, and consumer decisions.

**Model caches carefully.** Caches improve feedback and capacity but become correctness and trust boundaries. Cache keys must include every semantically relevant input. A missing compiler flag can return an artifact for the wrong configuration. Shared caches can allow one trust domain to poison another.

Record cache namespace, key derivation, integrity verification, writer authority, retention, eviction, and miss behavior. A cache hit should not bypass required policy or attach a stale test result to a new artifact. Recovery must tolerate cache loss unless the cache is explicitly durable state.

**Bind checks to artifacts.** Compile, static analysis, tests, scans, review approvals, and policy results apply to exact inputs or outputs. Record tool versions, configuration, environment, result, exclusions, and artifact digest. A green check for source revision `s` does not automatically apply to an independently rebuilt artifact unless correspondence is verified.

Order checks by cost and risk for feedback, but do not publish before required gates complete. Quarantine failed or unknown outputs. Flaky checks are evidence defects: retry can collect diagnostic evidence, but “passed once” should not silently replace a failed result.

**Protect the build trust boundary.** Treat proposed source, pull-request scripts, dependencies, test fixtures, generators, and artifacts as potentially untrusted. Separate untrusted execution from protected credentials and publication. Use least-privilege, short-lived identities; isolate workers; protect caches and logs; approve promotion; and record administrative actions.

NIST SP 800-218, the Secure Software Development Framework, organizes secure development practices around preparing the organization, protecting software, producing well-secured software, and responding to vulnerabilities [5]. The current SLSA 1.2 specification, released in November 2025 and checked on 2026-09-06, provides source and build tracks plus attestation formats for incrementally stronger supply-chain properties [3]. These calibrate controls; teams must still define threats and verify evidence.

**Record provenance and verify it.** Provenance relates an output artifact to source, dependencies, builder, invocation, environment, and time. It should be generated by an authority appropriate to the claim, bound immutably to the artifact, protected from tampering, distributed, retained, and checked against consumer expectations.

Provenance presence is not verification. A signed statement can be authentic but describe an untrusted builder or unexpected source. The SLSA 1.2 provenance documentation defines provenance as verifiable information tracing artifacts through their production [2]. Consumer policy decides acceptable repositories, revisions, builders, parameters, dependencies, and assurance levels.

**Use bills of materials with scope.** An SBOM identifies components and relationships for a defined artifact or product. Record format/version, creation method, depth, platform variants, completeness, and artifact binding. Generated, statically linked, dynamically loaded, runtime-provided, and service dependencies may need different representations.

An inventory supports vulnerability, license, and incident workflows but does not prove exploitability, absence of components, or security. Keep it synchronized with the artifact and handle unknowns. A vulnerability result also depends on advisory version, matching method, configuration, reachability, and remediation status.

**Model promotion and publication.** Separate build from release selection and environment promotion. The same immutable artifact can move through environments with different configuration, or policy may require environment-specific artifacts. Record who authorizes promotion, required evidence, publication destination, rollback identity, and revocation.

Never rebuild “the same version” for production without creating and verifying a new artifact identity and provenance. Retain artifacts, attestations, dependency evidence, configuration compatibility, and tools for the rollback window. Revocation and incident response need distribution and consumer paths.

**Plan failure and recovery.** Challenge source host, dependency registry, build worker, cache, test service, signing service, artifact registry, network, identity provider, and policy engine. Decide whether development stops, uses a controlled mirror, consumes previously verified inputs, or performs an emergency build under separately governed authority.

Recovery includes restoring trustworthy source, workers, dependencies, keys, policies, artifacts, and evidence. A backup of source alone cannot recreate an artifact if the toolchain or dependencies disappeared. Periodic reconstruction and verification can test the recovery claim in a recorded environment.

**Reconcile adjacent views.** Map code modules to source packages and owners; generated interfaces to runtime connectors; artifacts to deployment units and digests; migrations to data views; credentials to security authority; tests to quality scenarios; and build/run evidence to operational views. An artifact with no source, a deployed digest with no provenance, or a runtime component with no build path is a review finding.

## Definitions and Notation

Define a build model

$$
B=(I,T,A,E,O,P,V),
$$

where $I$ is immutable input identities; $T$ transformations and checks; $A$ output artifacts; $E\subseteq(I\cup T\cup A)^2$ input-dependency edges; $O$ ownership and authority; $P$ policy; and $V$ evidence.

For acyclic graph $G=(N,E)$ with nonnegative modeled duration $w(v)$, define earliest completion

$$
C(v)=w(v)+\max_{u\in pred(v)}C(u),
$$

where the maximum for a source node is zero. Build completion is $\max_{a\in A}C(a)$. This assumes unlimited parallel resources and fixed known durations; queueing, resource limits, cache state, retry, and discovery alter reality.

Let $H(x)$ be the chosen cryptographic digest of canonical artifact bytes. A reproducibility observation for independent builds $b_1,b_2$ is $H(A_{b_1})=H(A_{b_2})$ under declared-equivalent inputs and environments. Equality supports that observation; it neither proves source correctness nor rules out collusion or a shared compromised input.

## Mechanisms, Invariants, or Proof Structure

Use this development-and-build review mechanism.

1. **Frame:** name product, source, environment, lifecycle state, stakeholders, decisions, and threats.
2. **Map development:** identify repositories, packages, modules, interfaces, tests, generators, owners, and dependency rules.
3. **Freeze inputs:** bind source, dependencies, toolchains, configuration, environment, reference data, and network inputs immutably.
4. **Build the graph:** record transformations, checks, dependency edges, outputs, failures, resources, and bootstrap stages.
5. **Govern generation and cache:** establish authority, freshness, key completeness, integrity, namespace, and miss behavior.
6. **Protect execution:** isolate untrusted work, minimize credentials, separate publication, and audit administrative paths.
7. **Bind evidence:** attach checks, provenance, signatures, inventories, and approvals to exact source and output identities.
8. **Promote:** verify consumer policy, publish immutably, retain rollback, and support revocation.
9. **Challenge and recover:** remove source, registry, workers, cache, keys, network, and policy services; reconstruct trust.
10. **Reconcile:** map build outputs to deployment, runtime, data, security, quality, and operational views.

The governing invariants are explicit ownership, immutable inputs and outputs, complete consequential dependencies, acyclic evaluation, governed generation, isolated authority, artifact-bound evidence, verified promotion, recoverable production, cross-view correspondence, and bounded claims.

For a finite acyclic build graph, evaluating nodes in topological order ensures every predecessor output is available before its consumer. Induction over the topological sequence proves this scheduling property. It does not prove transformations are deterministic, inputs complete, outputs correct, or resources sufficient.

## Alternatives and Trade-Offs

**Monorepository versus multiple repositories.** A monorepository enables atomic change and shared analysis but needs scalable ownership and selective builds. Multiple repositories isolate authority and cadence but require compatible cross-repository evolution and distributed evidence.

**Committed versus generated-on-demand output.** Committing generated output aids review and consumers without the generator but creates freshness and noisy diffs. On-demand generation avoids duplication but requires available, trusted, versioned generators. In either case, declare authority and verify regeneration.

**Local versus remote build.** Local builds give fast autonomy and direct diagnosis but vary by workstation. Remote builds centralize isolation, capacity, and provenance but add queueing and service dependency. Use equivalent declared inputs and retain a recovery path.

**Source build versus binary dependency.** Source builds increase inspection and platform control but expand build complexity. Verified binaries reduce time but transfer trust to producer, registry, and provenance. Neither choice removes dependency governance.

**Maximum reproducibility versus optimized outputs.** Reproducibility can constrain timestamps, paths, randomized optimization, and environment diversity. Some profile-guided or hardware-specific builds deliberately vary; record inputs and evidence instead of making a false bit-identity claim.

**Fast feedback versus exhaustive gates.** Early narrow checks shorten developer loops; comprehensive checks raise confidence but consume time. Layer checks by risk and keep required promotion gates explicit. A slow gate is not a reason to publish first.

**Central build platform versus federated builders.** Centralization standardizes controls and evidence but creates capacity and compromise concentration. Federation supports specialized platforms and autonomy but requires interoperable identities, provenance, and consumer verification.

## Failure Modes and Misconceptions

- **Repository equals architecture module.** Source, runtime, ownership, and deployment boundaries differ.
- **The source revision defines the build.** Dependencies, tools, configuration, environment, and external inputs also matter.
- **A lock file proves trustworthy dependencies.** It records resolution; integrity, origin, review, and execution authority remain.
- **Generated means safe to ignore in review.** Generators and inputs can change broad executable behavior.
- **Hermetic means reproducible.** Isolation from undeclared inputs does not remove nondeterminism.
- **Reproducible means correct or secure.** Identical artifacts can faithfully reproduce defects or malicious source.
- **A cache hit is equivalent to a build.** Only a complete key and verified artifact justify reuse.
- **A green pipeline proves correctness.** Checks cover selected claims under recorded conditions.
- **Signed provenance is automatically trusted.** Verify signer, builder, inputs, parameters, and consumer policy.
- **An SBOM proves complete security.** It is a scoped inventory with collection and matching limits.
- **The tested source is the deployed artifact.** Bind results through immutable output identity and promotion.
- **Rollback means rebuild the old source.** Rebuilding can produce different bytes; retain verified artifacts and compatible state.
- **CI failure is only a productivity issue.** It can block security response, recovery, and safe release.

## Worked Examples

### Example 1

**Situation.** One repository contains billing, notifications, and a shared utility package, while billing and notifications deploy separately.

**Reasoning.** Model packages and allowed dependencies independently of the repository boundary. Assign separate owners and build targets. If both depend on unstable utility internals, the repository enables atomic edits but does not provide modularity. Introduce owned interfaces and tests while retaining intentional shared tooling.

**Conclusion.** Repository topology supports workflow but does not define architectural responsibility.

### Example 2

**Situation.** Generator G needs compiler C, while C's parser source is generated by G.

**Reasoning.** The apparent build graph cycles. Define trusted seed artifacts $G_0,C_0$, use them to build new G and C in staged order, then compare a later rebuild or apply another bootstrap verification strategy. Record the seed trust and stages rather than pretending ordinary topological evaluation works.

**Conclusion.** Bootstrap cycles require explicit trusted seeds and verification stages.

### Example 3

**Situation.** Source preparation takes 2 minutes; independent compile steps take 7 and 4; linking after both takes 3; packaging takes 1.

**Reasoning.** Preparation completes at 2. Compiles complete at 9 and 6. Link waits for the slower predecessor and completes at $\max(9,6)+3=12$. Packaging completes at 13. The modeled critical path is prepare, seven-minute compile, link, package.

**Conclusion.** Parallel durations combine through predecessor maxima, not a sum of all work.

### Example 4

**Situation.** Builds from one revision differ only on a workstation whose locale sorts `ä` differently.

**Reasoning.** File ordering derived from locale was an undeclared input. Declare and pin locale, sort by a canonical byte rule, or include the locale in artifact identity. Then rebuild independently and compare specified outputs, while preserving diagnostic differences.

**Conclusion.** Reproducibility work exposes hidden environmental inputs.

### Example 5

**Situation.** One developer runs the same build twice and gets identical digests.

**Reasoning.** This is evidence of repeatability in one environment, not independent reproducibility. A second controlled party reconstructs from the declared source, toolchain, dependencies, and instructions. Matching digests provide stronger evidence, still bounded by shared inputs and possible collusion.

**Conclusion.** Repeatability, reproducibility, and trust are distinct claims.

### Example 6

**Situation.** An API client is generated from schema version 14, but the repository contains an edited generated file.

**Reasoning.** Declare the schema and generator as authority, regenerate in a clean environment, and compare. If manual edits are intended, move them to supported extension points or make the output authoritative and stop claiming regeneration. Add a freshness check bound to generator version.

**Conclusion.** Generated output needs one explicit authority and a verifiable regeneration policy.

### Example 7

**Situation.** Release `2.1` contains binaries for two processor architectures.

**Reasoning.** The release name identifies a collection, not one artifact. Each platform build has distinct toolchain inputs, digest, tests, provenance, and possibly SBOM. Promotion verifies the selected platform artifact rather than attaching one attestation to the label `2.1`.

**Conclusion.** Bind evidence to individual immutable artifacts, not only a release name.

### Example 8

**Situation.** A pull request changes its build script and the CI job holds production registry credentials.

**Reasoning.** The proposed code can exfiltrate credentials or publish an artifact before review. Run untrusted checks without production secrets; after approval, rebuild trusted inputs in a protected worker and use a narrow publisher identity. Bind provenance and promotion to that artifact.

**Conclusion.** Separate untrusted evaluation from trusted build and publication authority.

### Example 9

**Situation.** A remote cache returns a passing test bundle for source revision `s`, but a compiler flag changed.

**Reasoning.** If the flag is absent from the cache key, the result applies to a different build. Include source, toolchain, flags, environment, dependencies, and test inputs in the key; verify returned digest and trust namespace. Invalidate or quarantine ambiguous entries.

**Conclusion.** An incomplete cache key can attach valid evidence to the wrong artifact.

### Example 10

**Situation.** A safety controller must be patched while its normal dependency registry is unavailable.

**Reasoning.** Use a controlled offline mirror of previously verified dependencies, a retained toolchain, protected signing authority, and an isolated build environment. Record emergency authorization, source revision, inputs, tests, independent review, artifact digest, provenance, device compatibility, and later reconciliation. If required evidence cannot be produced, the risk authority decides between known vulnerability and unverified change; automation does not hide the choice.

**Conclusion.** Build recovery must restore trustworthy inputs, authority, verification, and artifact traceability—not merely source access.

## Cross-Program Connections

- **Software Delivery and Reliability Engineering:** integration, release, promotion, rollback, observability, and incident response operationalize the graph.
- **Platform Engineering:** developer portals, remote builders, caches, policy, registries, and workload identity provide the build platform.
- **Security:** source control, dependencies, isolation, provenance, signatures, credentials, and publication form the supply-chain threat surface.
- **Software Testing and Quality Engineering:** checks, environments, fixtures, coverage, nondeterminism, and evidence determine what a result supports.
- **Compiler Engineering:** parsing, code generation, linking, optimization, target platforms, and bootstrap determine transformations.
- **Programming Languages:** modules, packages, type interfaces, metaprogramming, and dependency resolution shape development boundaries.
- **Cloud Engineering:** elastic workers, managed registries, identities, and regional dependencies specialize remote execution.
- **Database and Data Engineering:** migrations, schemas, generated clients, data fixtures, and provenance join software and data change.

## References

1. ISO/IEC/IEEE, *ISO/IEC/IEEE 42010:2022 Software, systems and enterprise — Architecture description*, 2nd ed., November 2022. Official catalogue; current edition checked 2026-09-06. https://www.iso.org/standard/74393.html
2. SLSA Community, “Provenance,” *SLSA Specification 1.2*, approved specification. Retrieved 2026-09-06. https://slsa.dev/spec/v1.2/provenance
3. SLSA Community, *SLSA Specification Version 1.2*, approved November 2025. Current version checked 2026-09-06. https://slsa.dev/spec/v1.2/
4. Reproducible Builds Project, “Definitions: When is a build reproducible?” Retrieved 2026-09-06. https://reproducible-builds.org/docs/definition/
5. National Institute of Standards and Technology, *Secure Software Development Framework (SSDF) Version 1.1*, NIST SP 800-218, February 2022. https://doi.org/10.6028/NIST.SP.800-218
6. Paul Clements et al., *Documenting Software Architectures: Views and Beyond*, 2nd ed., Addison-Wesley, 2010.
7. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021.
8. Mike Clark, *Pragmatic Project Automation*, Pragmatic Bookshelf, 2004.

## Exercises

### Exercise 1

Precisely distinguish repository, package, architecture module, component, deployment unit, build step, artifact, release, provenance, and attestation. Give two non-one-to-one correspondences.

### Exercise 2

A build graph has source S taking 1 minute, parallel generators G1 and G2 taking 3 and 5, compile C after both taking 4, tests T after C taking 6, packaging P after C taking 2, and release R after T and P taking 1. Compute earliest completion for every node and the critical path under unlimited parallel resources.

### Exercise 3

Diagnose a “reproducible” build that pins source and dependencies but reads current time, fetches a mutable compiler image, embeds an absolute workspace path, and uses a shared writable cache. Classify the defects and propose checks.

### Exercise 4

Compare monorepository and multiple-repository organization for ten services sharing schemas and generated clients. Address ownership, atomic change, compatibility, feedback, build graph, security, and release autonomy.

### Exercise 5

Transfer the method to firmware for a fleet of field robots that may be offline for months. Design source, dependency, toolchain, simulation, hardware test, signing, artifact, staged promotion, rollback, revocation, and recovery views.

## Answers to the Exercises

### Answer 1

A **repository** is a version-control boundary; a **package** is a source or distribution unit; an **architecture module** is an implementation responsibility; a **component** is runtime behavior; a **deployment unit** is independently released or installed; a **build step** transforms inputs; an **artifact** is an immutable output; a **release** is a governed selection of artifacts and metadata; **provenance** records production facts; an **attestation** is an authenticated statement about an artifact or property.

One repository can contain many packages and deployment units. One component can be built from several packages, while one artifact can contain several components. One release can contain platform-specific artifacts, each with distinct provenance and tests.

### Answer 2

$C(S)=1$. Since both generators depend on S, $C(G1)=1+3=4$ and $C(G2)=1+5=6$. Compile waits for both, so $C(C)=\max(4,6)+4=10$. Tests complete at $C(T)=10+6=16$; packaging completes at $C(P)=10+2=12$. Release waits for both and completes at $C(R)=\max(16,12)+1=17$ minutes.

The critical path is S, G2, C, T, R with duration $1+5+4+6+1=17$ minutes. This assumes fixed durations, unlimited workers, no cache effects, no queueing, and no retry.

### Answer 3

Pinned source and resolved dependencies are insufficient. Current time is an undeclared or varying input; normalize it or pass a declared build epoch. The mutable compiler image leaves toolchain identity unresolved; bind it by verified digest. The absolute workspace path makes output environment-specific; remove it, remap paths, or declare it. The shared writable cache can introduce undeclared content or cross-trust poisoning; use complete keys, integrity checks, scoped writers, or disable it for verification.

Run two clean builds with declared-equivalent inputs in independently controlled environments, compare specified artifact bytes and digests, and use diff tools to localize mismatches. Block undeclared network access, log attempted reads, verify toolchain and dependency integrity, and record provenance. A matching result supports one reproducibility observation; it does not prove correctness or security.

### Answer 4

A monorepository enables atomic schema, producer, and client changes and whole-tree compatibility tests. It needs owners for schemas and generators, dependency rules, selective builds, protected publication, and scalable review. Services can still release independently if artifacts and compatibility are versioned.

Multiple repositories isolate write authority and release cadence. Schema changes require published versioned contracts, compatibility windows, generated-client distribution, cross-repository test evidence, and coordinated retirement. Atomic source change becomes a staged protocol change. A central generator or registry can remain a common security and availability dependency.

Choose using change coupling, authority, scale, and recovery. In either arrangement, bind generated clients to schema and generator versions, prevent consumers from importing producer internals, isolate untrusted builds, and attach tests and provenance to each artifact. Repository choice does not replace modular contracts.

### Answer 5

Bind application, control algorithms, safety rules, hardware abstraction, bootloader, configuration schema, and tests to reviewed source revisions and owners. Mirror dependency source and binaries with integrity and license records. Retain qualified cross-compilers, linkers, simulators, device models, build environments, and calibration reference data by immutable identity.

The graph produces simulator artifacts first, runs deterministic and adversarial scenarios, builds per-hardware firmware, performs static checks, flashes representative hardware, executes hardware-in-the-loop tests, and packages signed firmware with device compatibility, SBOM, test evidence, and provenance. Untrusted changes run without fleet signing or publication credentials. Protected promotion verifies source, builder, parameters, results, and output digest.

Stage deployment through laboratory units, a small monitored field cohort, then larger cohorts, preserving previous verified firmware and compatible configuration. Robots reject wrong hardware, expired authorization, replay, and revoked artifacts. Offline devices retain bounded safe behavior and an update journal. Revocation reaches connected units immediately and is queued for disconnected units; mission policy decides whether vulnerable offline units may continue.

Recovery retains source, mirrors, toolchains, signing succession, artifact registry, policies, hardware fixtures, and evidence. Periodic clean rebuild and recovery drills check that old supported versions remain reconstructible or that retained artifacts remain verifiable. Fleet reconciliation records each robot's installed digest, configuration, last contact, failed update, rollback, and exception without assuming uniform state.
