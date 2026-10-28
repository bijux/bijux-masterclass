---
module_id: SARCH-048
program: Software Engineering: Software Architecture
level: 1
module_number: 48
title: Deployment Units and Release Independence
status: complete
last_verified: 2026-09-06
---

# Deployment Units and Release Independence

## One-Page Review

### Governing question

How should an architecture choose deployable boundaries so that changes can be built, verified, released, activated, rolled back, and operated independently when useful—without pretending that packaging alone removes runtime, data, contract, or organizational coupling?

### Essential definitions

- A **deployment unit** is the smallest artifact or coordinated artifact set installed as one operational change under one version and lifecycle.
- A **release** makes a version eligible for use; **deployment** installs it; **activation** exposes behavior or traffic. These events can be separate.
- **release independence** is the ability to change one owned capability without requiring an otherwise unnecessary simultaneous change to another unit.
- **co-deployment** means units must be changed in one coordinated operation for correctness or compatibility; frequent accidental co-deployment is evidence of coupling.
- A **compatibility window** is the set of old/new participant combinations supported during rollout and rollback.
- **version skew** is simultaneous operation of different versions across instances, clients, schemas, messages, or regions.
- **expand-and-contract** first introduces a representation compatible with old and new participants, migrates use, then removes the old form after evidence permits.
- A **feature flag** separates code deployment from behavior activation; it is temporary runtime configuration with ownership and removal obligations.
- A **canary** exposes a new version to a bounded slice to gather evidence before broad activation.
- **rollback** restores a prior deployable or behavior, while **roll-forward** applies a correcting successor; neither automatically reverses persisted effects.
- **deployment blast radius** is the set of users, operations, data, and dependencies exposed to one deployment failure.

### Central model, mechanism, or theorem

Represent deployables as vertices $U$ and required coordinated changes as edges in graph $G_d=(U,E_d)$. Edge $(u,v)$ must have a concrete reason: incompatible contract, shared data migration, runtime ordering, shared configuration, or inseparable operational invariant. Connected components approximate current co-deployment sets; removing an edge requires changing its underlying contract or state transition, not merely creating another repository.

If one rollout must change $n$ independently modeled units and each succeeds with probability $p$, simplified all-success probability is $p^n$. At $p=0.995$ and $n=20$, $0.995^{20}\approx0.90461$. Real failures are correlated, so this is an explanatory model, not a release forecast.

### Critical invariants

- distinguish source module, ownership boundary, build artifact, deployment unit, runtime process, data authority, and team;
- every deployable has one owner, immutable identity, provenance, configuration contract, rollout policy, and operational evidence;
- independent deployment requires supported old/new combinations at every synchronous, asynchronous, data, and client contract;
- producers expand before consumers depend; consumers stop old use before producers contract;
- schema changes preserve rollback and mixed-version behavior until evidence closes the compatibility window;
- state-changing deployments define effect, migration, recovery, rollback, and roll-forward semantics;
- shared libraries, base images, sidecars, gateways, and platform controls do not force synchronized application release without a proven necessity;
- flags have typed defaults, scope, audit, expiry, failure behavior, and removal ownership;
- canaries limit exposure but do not prove rare, long-duration, or unrepresented behavior;
- build, release, deployment, activation, and configuration evidence remain distinct;
- rollout concurrency, unavailable capacity, dependency load, and regional sequencing are bounded;
- test mixed versions, rollback, failed migration, lost control plane, dependency skew, and disaster recovery.

### Common failures

Common failures include equating one repository with one deployable; splitting a monolith into artifacts that must always release together; changing provider and every consumer simultaneously; deploying breaking schema and code in one step; assuming rollback reverses writes; using mutable tags; rebuilding artifacts per environment; activating all users at deployment time; leaving permanent flags; treating a passing canary as universal correctness; forcing fleet-wide application releases for a shared library patch; and counting deployment frequency without measuring user outcomes, failed changes, or recovery.

### Compact example

Order API v2 adds an optional response field. Providers deploy additive support first while old consumers ignore the field. New consumers then use it with a safe default when absent. Only after telemetry shows all supported consumers migrated may the field become required or the old representation be removed. The provider and consumers can deploy separately because the compatibility window is designed; separate pipelines alone would not create that independence.

### Connections

[SARCH-015](015-modifiability-and-evolvability-tactics.md) supplies change tactics; [SARCH-017](017-interoperability-tactics.md) supplies contract evolution; [SARCH-039](039-microservices-architecture.md) separates service forces; [SARCH-042](042-shared-database-versus-database-per-service.md) supplies data coupling. [SARCH-049](../ROADMAP.md) next examines configuration topology. Software Delivery and Reliability Engineering owns delivery mechanics and metrics in depth.

## Governing Question

A deployment unit turns architecture into operational change. Code that looks modular in source can still be released as one executable. Separately packaged services can still require lockstep rollout because their contracts break under mixed versions. A shared database, client fleet, message history, or platform policy can couple changes long after repositories are separated.

The architectural task is to choose units whose ownership and change forces are coherent, then design compatibility and state transitions that make independent release possible. Independence is a capability used when it reduces risk or lead time, not a command to deploy every component separately.

## Why This Matters

Every additional coordination edge increases scheduling, verification, rollback, and incident complexity. A small change waits for unrelated teams. One failed component can block an entire suite. Emergency repair requires rebuilding or redeploying much more than the affected capability.

Too many tiny deployables create another cost: pipelines, identities, configuration, telemetry, capacity, on-call knowledge, version combinations, and supply-chain surfaces. The right boundary minimizes unnecessary coordination while retaining coherent ownership, testing, operation, and failure containment.

Release independence makes architectural modularity observable. If two capabilities cannot change without simultaneous deployment, their effective boundary is weaker than their diagrams imply.

## Prerequisites and Retrieval

Retrieve module, component, service, artifact, package, process, image, repository, build, release, deployment, activation, version, compatibility, schema, migration, rollback, feature flag, canary, ownership, provenance, capacity, availability, observability, and incident recovery.

From SARCH-015 retrieve modifiability tactics and information hiding; SARCH-017 provides interoperability; SARCH-018 provides evidence; SARCH-027 provides development and build views; SARCH-032 provides modular-monolith boundaries; SARCH-039 provides service boundaries; and SARCH-041 through SARCH-047 provide data, integration, edge, and cache consequences.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish code, ownership, build, deployment, runtime, and data boundaries;
2. identify and justify co-deployment edges;
3. choose deployment-unit granularity from change, failure, ownership, and operational forces;
4. design compatibility windows for providers, consumers, clients, messages, and schemas;
5. apply expand-and-contract without breaking mixed deployments or rollback;
6. separate immutable build, release, deployment, configuration, and activation;
7. design flags, canaries, rollout order, and capacity safeguards;
8. reason honestly about rollback after state changes;
9. reduce shared-library, platform, and database release coupling;
10. collect evidence that release independence improves outcomes rather than merely multiplying deployables.

## Core Exposition

**Separate architectural boundaries.** A source module is a compile-time organization. A repository is a version-control boundary. A build artifact is produced and identified together. A deployment unit is installed together. A process is scheduled and fails together. A data authority owns state. A team owns decisions and operation.

These may align, but alignment is a design outcome. One modular monolith can contain strong domain modules deployed as one executable. One repository can produce several independent artifacts. One service can require several coordinated artifacts. Count and name each boundary rather than inferring one from another.

**Define independence as ability.** Release independence means a change to unit A can reach production without requiring a semantically unrelated new version of B. A and B may still be deployed together for convenience. The key is whether they must coordinate for correctness.

Independence is not isolation. Runtime calls, shared infrastructure, organizational policies, and business workflows remain. It reduces one form of temporal change coupling; it does not erase dependency.

**Map the co-deployment graph.** For each recent or planned change, record which units had to change together and why. Reasons include breaking APIs, shared database assumptions, common configuration schema, duplicated constants, shared runtime loading, synchronized protocol state, or one untestable release bundle.

Do not accept “the pipeline does it that way” as a domain reason. Mark operational convenience separately from correctness. Repeated edges reveal the effective deployment component. Removing the edge requires a compatibility mechanism or changed ownership, not simply another pipeline.

**Choose coarse enough units.** A deployable should have coherent purpose, owner, runtime needs, scaling, data, security, and failure behavior. Splitting every class or function makes ownership and operation expensive. If two pieces always change, scale, recover, and fail together, one unit may be clearer.

Choose fine enough units when capabilities have different change rates, teams, security domains, resource profiles, availability needs, or blast radii. Quantify expected benefit against pipeline, platform, testing, and on-call cost.

**Do not confuse microservices with independent deployment.** A service is independently deployable only if its contracts tolerate mixed versions and its state transition can roll safely. A distributed monolith has many processes but requires coordinated releases.

A modular monolith can provide significant source and ownership independence while accepting one deployment schedule. Extract a separate unit only when operational independence has a concrete value that exceeds distribution cost.

**Build once and promote immutably.** Produce one immutable artifact with content-derived or otherwise unique identity and recorded source, dependencies, toolchain, tests, and provenance. Promote that exact artifact through environments. Do not rebuild “the same version” for production, because the bytes and evidence would differ.

Configuration supplies environment-specific values under a versioned contract. Secrets remain external protected inputs. A mutable tag such as `latest` is not durable deployment identity; record the resolved immutable digest or equivalent.

**Separate release, deployment, and activation.** A version can be built and released to an artifact store, deployed with no traffic, then activated gradually. This separation permits preloading, verification, instant routing changes, and fast deactivation.

It also adds states. Operators must know which version is available, installed, configured, receiving traffic, and authoritative. A feature present in code but disabled is still a supply-chain and attack surface; activation does not define whether the code exists.

**Design compatibility from consumers backward.** Independent rollout requires old consumer/new provider, new consumer/old provider, and relevant intermediate combinations. Additive fields with safe defaults often help. Changing units, error meaning, ordering, timing, or side effects can break behavior without changing syntax.

Unknown consumers create risk. Observe actual versions but do not assume absence from telemetry proves nonexistence. Publish support windows, deprecation evidence, and removal criteria.

**Use expand-and-contract.** First expand the provider or storage representation while preserving old behavior. Deploy consumers that can read both and write under the transition policy. Migrate or backfill. Verify no supported old use remains. Then contract in a later deployment.

This sequence turns one incompatible simultaneous change into several compatible changes. Each step must leave the system coherent and reversible within its declared window. Do not combine expansion and removal because tests pass in an environment where all components changed together.

**Evolve database schemas safely.** Add nullable or safely defaulted structures before code uses them. Avoid long blocking changes without measuring production behavior. Deploy readers tolerant of both forms, migrate data idempotently, switch writes, validate, and remove old form only after rollback no longer needs it.

Shared databases increase the consumer set: reports, jobs, repairs, triggers, and external tools may depend on schema. Private ownership and audited access reduce unknown coupling. A migration tool success proves execution, not application compatibility or acceptable lock behavior.

**Handle messages and retained history.** Old messages can outlive producers and consumers. New consumers must interpret supported historical schemas; rollback consumers may see messages from newer producers. An event meaning cannot be edited in place because new code prefers a different model.

Use versioned envelopes and semantic compatibility. Upcasters or translators need ownership, tests, performance, and replay evidence. Removing an old consumer does not remove old messages from archives or recovery paths.

**Account for client-controlled deployment.** Mobile, desktop, device, and partner clients may remain old for months or years. A server rollout cannot assume simultaneous upgrade. Authenticate versions only as a signal; never trust a client-reported version for authorization.

Maintain compatible endpoints or a governed minimum-version policy with user and safety consequences. Test slow adoption, offline use, restored old backups, and clock/date errors. “Force update” is a product and operational decision, not a universal compatibility mechanism.

**Control shared libraries.** A source or binary library update can require rebuilding every consumer, producing a fleet-wide release. This may be appropriate for a critical vulnerability, but frequent shared-domain changes create hidden lockstep coupling.

Keep shared libraries focused on stable technical mechanisms. Domain policy belongs behind owned contracts or within owning modules. Support a version range, allow staged upgrades, test compatibility, and record which artifact contains which dependency rather than assuming repository declarations equal deployed reality.

**Treat base images and sidecars similarly.** Platform-owned runtime layers, agents, proxies, and sidecars can change behavior across every application. Independent update reduces application rebuilds but introduces version skew and shared blast radius. Bundled update improves tested combination control but forces coordinated release.

Choose from security urgency, compatibility, operational ownership, and rollback. Test platform changes against representative workloads and constrain rollout. A platform component must not silently change application protocol semantics.

**Use feature flags with discipline.** A flag can decouple deployment from activation, limit users, compare behavior, or provide a kill switch. Define owner, purpose, type, default, allowed scopes, evaluation failure, authorization, audit, expiry, and removal condition.

Flags create code-path combinations and can be stateful. Activating a new write format may make deactivation unsafe. Treat schema-changing or irreversible flags as migrations, not booleans. Remove flags and dead branches after the decision window.

**Use canaries as bounded evidence.** A canary limits initial exposure and compares health under real traffic. Select representative tenants, request types, regions, and state. Observe user and business outcomes, not only CPU and error rate.

Rare failures, end-of-month workloads, long memory leaks, disaster behavior, and unrepresented customers remain untested. Expand exposure only within defined thresholds and time. Preserve capacity for old and new versions during rollout.

**Plan rollout order and skew.** Rolling deployment temporarily creates mixed instances. If routing is random, one client can alternate versions. Session affinity reduces some variation but creates imbalance and does not solve shared data compatibility.

For each participant graph, identify allowed versions and order. Provider-first is common for additive changes; consumer-first is common for removing dependence on an old field. Regional sequencing must consider cross-region calls and shared state.

**Budget rollout capacity.** If fraction $u$ of instances may be unavailable during rollout, remaining capacity must meet admitted demand under target utilization and failure reserve. A deployment that removes instances can trigger overload and false canary failures.

Set maximum unavailable and surge from measured workload, dependency capacity, startup time, warm caches, and zone placement. Prevent many services from simultaneously creating restart or cache-fill storms.

**Design rollback before deploying.** Binary rollback works only if previous code can read current data, messages, configuration, and dependencies. A new version may have emitted events, changed external effects, or deleted information. Deactivation may stop further exposure but cannot undo completed actions.

Prefer roll-forward when rollback would misinterpret state. Keep repair and reconciliation procedures. State explicitly which transitions are reversible, compensatable, or irreversible and who authorizes action.

**Avoid environment-specific artifacts.** Differences between test and production should be declared configuration and external resources, not untracked binary mutation. Sign and verify artifact identity. Validate that environment configuration matches the artifact's supported schema before activation.

Environment parity does not require equal scale or sensitive data. It requires that meaningful behavior, topology, permissions, and failure assumptions are represented or their differences are known and tested elsewhere.

**Give every deployable an operational contract.** Define owner, service level, resource and scaling profile, health semantics, dependencies, configuration, data, security identity, observability, rollout, rollback, recovery, and decommissioning. A unit no one can diagnose independently is not operationally independent.

Health probes should represent readiness for admitted operations without making every dependency a circular global prerequisite. Deployment automation must distinguish starting, ready, serving, degraded, and safe to remove.

**Measure outcomes, not unit count.** Useful evidence includes lead time, waiting for coordination, deployment frequency, failed-change rate, recovery time, rollback success, user impact, version-skew defects, release size, and ownership load. More deployments or repositories are not automatically better.

Compare before and after boundary changes. A split that lowers one team's lead time but increases incidents, platform cost, and cross-team diagnosis may not be an improvement. DORA research treats delivery performance as a multidimensional capability rather than one metric [1].

**Secure the delivery boundary.** Protect source, build workers, dependencies, artifact stores, provenance, signing keys, deployment identities, configuration, secrets, and control planes. Least privilege separates build, release approval, deployment, activation, and emergency access where consequence warrants it.

Verify artifact identity at deployment. Record who or what authorized the change, but do not put secrets in provenance or logs. A signed artifact establishes a cryptographic relationship to a key and bytes; it does not prove code safety or business approval by itself.

**Test release independence.** In addition to latest-together tests, run old/new provider-consumer matrices, rolling instance mixtures, schema expansion and contraction, message replay, old clients, configuration skew, dependency upgrades, rollback after writes, and control-plane loss.

Exercise partial deployment, stalled rollout, zone loss, capacity reduction, slow startup, failed readiness, cache cold start, and disaster restore. Confirm the previous stable version can operate on actual current state before calling rollback safe.

**Know when coordinated deployment is correct.** Some invariants genuinely require one atomic operational transition: tightly coupled firmware and hardware, a safety-certified set, or a local transaction implemented inside one executable. Do not introduce distribution solely to maximize an independence metric.

Make coordination explicit, small, rehearsed, and evidence-backed. The defect is accidental or unnecessarily broad lockstep, not coordination itself.

## Definitions and Notation

Let deployment graph $G_d=(U,E_d)$ contain deployment units $U$. Edge $(u,v)\in E_d$ means correctness currently requires coordinated versions or transition. Label each edge by contract, data, configuration, runtime, platform, or operational cause.

Let supported-version relation $K(u,v)$ contain pairs of versions allowed to interact. A rolling plan is valid only if every reachable intermediate pair remains in $K$ and shared state remains readable under planned rollback.

For $n$ independently modeled changes each succeeding with probability $p$, simplified all-success probability is $p^n$. This illustrative calculation does not model shared pipelines, environments, people, dependencies, or correlated failure.

Let rollout temporarily make $m$ of $N$ instances unavailable. If planned per-instance capacity is $c$ and admitted peak is $\lambda$, necessary capacity is $(N-m)c\ge\lambda$, with separate failure-domain and dependency constraints.

## Mechanisms, Invariants, or Proof Structure

**Boundary invariant.** Source, repository, build, deployable, process, owner, data authority, and team boundaries are named independently and aligned only by explicit design.

**Coordination invariant.** Every required co-deployment edge has a current correctness reason; tooling habit alone is not accepted as necessity.

**Compatibility invariant.** Every rollout and rollback state uses supported contract, data, message, configuration, client, and dependency version combinations.

**Expand-contract argument.** When old and new participants cannot change atomically, adding compatible representation before dependence and removing old representation after migration preserves an overlap in which each intermediate deployment remains supported.

**Artifact invariant.** One immutable identified artifact is built with evidence and promoted; environment-specific inputs are external versioned configuration.

**State invariant.** Deployment, activation, deactivation, rollback, roll-forward, compensation, and data repair remain distinct operations with explicit effect semantics.

**Capacity invariant.** Remaining instances, zones, dependencies, startup work, cache warming, and rollout concurrency meet bounded admitted demand.

**Ownership invariant.** Every deployable and flag has one durable owner for compatibility, operation, incident response, migration, and removal.

**Security invariant.** Artifact provenance, authorization, identity, secrets, and control-plane operations remain least-privileged and auditable.

**Evidence invariant.** Build success, deployment completion, readiness, traffic activation, technical health, business outcome, and recovery are observed separately.

## Alternatives and Trade-Offs

| Choice | Advantages | Costs and risks | Prefer when |
|---|---|---|---|
| Single deployable | simple consistency and operations | broad blast radius and coordination | change and runtime forces are coherent |
| Modular monolith | strong source boundaries with one release | shared runtime and schedule | distribution offers little current value |
| Independent services | selective scale, release, and failure ownership | network, data, platform, and skew complexity | autonomy has measurable value |
| Monorepository | atomic source changes and shared tooling | ownership and build coupling if unmanaged | repository boundaries need not equal deployment |
| Multiple repositories | access and lifecycle separation | cross-repo discovery and coordination | ownership or security warrants it |
| Expand-and-contract | safe mixed-version transition | more deployments and temporary complexity | participants cannot change atomically |
| Feature flag | separate activation and bounded exposure | combinations, configuration, cleanup | behavior can switch safely |
| Canary | limits initial blast radius | incomplete representativeness | outcomes can be measured before expansion |
| Rolling deployment | efficient continuous capacity | version skew | adjacent versions are compatible |
| Blue-green deployment | fast switch and rollback target | doubled capacity and state routing | environment duplication is affordable |
| Coordinated release | preserves a genuine atomic transition | waiting and broad blast radius | invariant cannot be decomposed safely |

## Failure Modes and Misconceptions

1. **“One repository equals one deployment unit.”** Source control and runtime lifecycle differ.
2. **“Separate artifacts are independently deployable.”** breaking contracts can force lockstep.
3. **“Microservices guarantee autonomy.”** distributed monoliths remain coordinated.
4. **“Independent means always separate.”** it is an ability, not a scheduling command.
5. **“Additive schema is always compatible.”** defaults, limits, and semantics may still break.
6. **“Tests passed with everything upgraded.”** mixed states remain untested.
7. **“Rollback restores the old world.”** persisted and external effects remain.
8. **“A flag makes any rollout reversible.”** new state can make deactivation unsafe.
9. **“Canary success proves safety.”** rare and unrepresented behavior remains.
10. **“Shared libraries reduce coupling.”** upgrades can force fleet rebuilds.
11. **“Mutable tags identify deployments.”** their bytes can change.
12. **“Rebuilding per environment is promotion.”** it creates different artifacts.
13. **“Database migration belongs to the pipeline.”** application compatibility and state semantics govern it.
14. **“More deployment frequency is always better.”** outcomes and failed changes matter.
15. **“Platform upgrades are transparent.”** sidecars and base layers change behavior.
16. **“Coordination is architectural failure.”** some atomic invariants justify it.

## Worked Examples

### Example 1

**Situation.** Twenty independently modeled components each have deployment success probability 0.995, and a suite change requires all twenty.

**Reasoning.** Simplified all-success probability is $0.995^{20}\approx0.90461$. Independence is unrealistic because components share pipelines and environments, but the model exposes how broad coordination creates more failure opportunities. Break unnecessary edges through compatible contracts and smaller changes.

**Conclusion.** A strong local deployment rate does not make a large lockstep release equally strong.

### Example 2

**Situation.** A service renames database column `total` to `amount` while old instances remain.

**Reasoning.** Add `amount` first while retaining `total`; deploy code able to read both and write under a defined dual-write or database-derived transition; backfill idempotently; validate counts and values; switch reads; stop old writes; then remove `total` after rollback support and unknown consumers close. Each step has a recovery point.

**Conclusion.** Expand-and-contract turns a breaking rename into mixed-version-compatible transitions.

### Example 3

**Situation.** A domain-policy library update forces 80 services to rebuild and deploy together.

**Reasoning.** The library has become shared domain ownership. Move the policy to its owning service or stable module contract, or support multiple library versions with explicit compatibility. Retain shared libraries for stable technical mechanisms. Urgent security upgrades can still justify coordinated fleet rollout under evidence.

**Conclusion.** Source reuse can create greater deployment coupling than an owned runtime contract.

### Example 4

**Situation.** A feature flag enables a new order state for 5% of users, then operators disable it.

**Reasoning.** Old code may not understand orders already written in the new state. The flag is not safely reversible unless both paths read that state or migration/repair exists. Separate read compatibility deployment from state creation, constrain activation, record affected entities, and define roll-forward or compensation.

**Conclusion.** Activation reversibility depends on state semantics, not the existence of a switch.

### Example 5

**Situation.** A canary reports normal CPU and HTTP errors, but invoices are rounded incorrectly.

**Reasoning.** Infrastructure metrics miss the business defect. Compare invoice totals, currencies, rounding invariants, sampled source inputs, and downstream acceptance for representative tenants. Stop expansion, disable new calculation if state-compatible, identify affected invoices, and repair under audit.

**Conclusion.** Canary evidence must include domain outcomes and reconciliation.

### Example 6

**Situation.** A rolling deployment removes three of twelve instances; each remaining instance safely serves 900 requests/s and peak demand is 9,500/s.

**Reasoning.** Remaining capacity is $9\times900=8{,}100$/s, below demand. Reduce maximum unavailable, add surge capacity, lower admitted load, or sequence outside peak. Include slow startup, cold caches, zone distribution, and dependency limits in the tested plan.

**Conclusion.** Rollout settings are capacity decisions, not merely deployment speed controls.

### Example 7

**Situation.** A mobile API removes a field two weeks after new server and client releases.

**Reasoning.** Many devices remain old, offline, or restored from backup. Measure active supported versions, retain compatibility for the published window, provide safe defaults, and define a humane minimum-version policy. Do not treat missing telemetry as proof that no old client exists.

**Conclusion.** Client-controlled deployment lengthens compatibility windows and weakens rollout assumptions.

### Example 8

**Situation.** A platform updates a sidecar proxy independently and connection reuse changes application latency.

**Reasoning.** Stage by workload and zone, test protocol and timeout behavior, compare application and user outcomes, retain compatible previous sidecar, and bound simultaneous restarts. Record sidecar version with incidents. Application owners need visibility even when the platform owns deployment.

**Conclusion.** Platform-managed deployables preserve ownership but are not behaviorally invisible.

### Example 9

**Situation.** Production is rebuilt from the same Git tag after staging passes.

**Reasoning.** Dependency resolution, compiler, base image, or build environment can produce different bytes. Build once, assign immutable digest, capture dependencies and provenance, verify, sign under policy, and promote the same artifact with validated production configuration. Record actual deployed digest.

**Conclusion.** A source tag identifies inputs imperfectly; immutable artifact identity supports reproducible promotion evidence.

### Example 10

**Situation.** Railway control software and certified configuration must change under one safety case.

**Reasoning.** Splitting deployments solely for autonomy could invalidate verified combinations. Keep the certified set as one coordinated deployment unit or define separately certified compatibility matrices. Rehearse installation, rollback limits, degraded operation, and manual authority; record exact artifacts and configuration.

**Conclusion.** Genuine safety invariants can justify coordinated deployment when scope and evidence are explicit.

## Cross-Program Connections

- **Software Delivery and Reliability Engineering:** owns pipelines, deployment strategies, delivery metrics, change failure, recovery, and operational automation in depth.
- **Software Engineering Patterns:** module and dependency patterns influence source boundaries but do not determine deployables.
- **Software Design and Domain Modeling:** domain ownership and aggregate invariants guide coherent change units.
- **API and Service Engineering:** owns contract compatibility, deprecation, consumer tests, and version negotiation.
- **Database Engineering:** owns online schema change, transactions, backfill, locking, and rollback limits.
- **Platform Engineering:** supplies artifacts, identities, environments, rollout controllers, flags, policy, and observability.
- **Security Engineering:** owns supply-chain threats, provenance, signing, least privilege, secrets, and emergency access.
- **Distributed Systems Engineering:** owns version skew, partial rollout, configuration consistency, and failure during transitions.

## References

1. Nicole Forsgren, Jez Humble, and Gene Kim, *Accelerate: The Science of Lean Software and DevOps*, IT Revolution, 2018.
2. Jez Humble and David Farley, *Continuous Delivery*, Addison-Wesley, 2010.
3. David Lorge Parnas, “On the Criteria To Be Used in Decomposing Systems into Modules,” *Communications of the ACM* 15(12), 1972. <https://doi.org/10.1145/361598.361623>
4. Sam Newman, *Building Microservices*, 2nd ed., O'Reilly Media, 2021.
5. Matthew Skelton and Manuel Pais, *Team Topologies: Organizing Business and Technology for Fast Flow of Value*, 2nd ed., IT Revolution, 2025. <https://itrevolution.com/product/team-topologies/>
6. Martin Fowler, “Feature Toggles,” 2017. <https://martinfowler.com/articles/feature-toggles.html>
7. NIST, *Secure Software Development Framework (SSDF) Version 1.1*, SP 800-218, February 2022. <https://csrc.nist.gov/pubs/sp/800/218/final>
8. SLSA Community, *Supply-chain Levels for Software Artifacts Specification, Version 1.2*, approved November 2025. <https://slsa.dev/spec/v1.2/>

## Exercises

### Exercise 1

Define deployment unit, release, deployment, activation, release independence, co-deployment, compatibility window, version skew, expand-and-contract, feature flag, canary, rollback, roll-forward, and deployment blast radius. Distinguish repository, build artifact, process, and data authority.

### Exercise 2

A rollout has 18 instances, each planned for 700 requests/s. Peak admitted demand is 9,000/s. Compute capacity with four instances unavailable and the maximum integer unavailable instances that preserve the simplified capacity condition. State why this is not a rollout guarantee.

### Exercise 3

Design an expand-and-contract migration from integer cents to a structured money representation shared by an API, database, message stream, batch export, and old mobile clients. Include rollout, backfill, validation, rollback, and removal evidence.

### Exercise 4

Compare a modular monolith, five independently deployed services, and five separately packaged but lockstep services for a billing capability. Address ownership, contracts, data, scaling, testing, platform cost, failure, and change coordination.

### Exercise 5

Design deployment units and release transitions for an intermittently connected emergency-dispatch system spanning central services, station servers, vehicle devices, radio gateways, maps, and safety rules. Cover client lag, immutable artifacts, configuration, compatibility, capacity, activation, rollback limits, security, evidence, and manual operation.

## Answers to the Exercises

### Answer 1

A **deployment unit** is installed as one operational change. A **release** makes a version eligible; **deployment** installs it; **activation** exposes behavior. **Release independence** permits one owned capability to change without unrelated simultaneous changes. **Co-deployment** is required coordinated change. A **compatibility window** defines supported old/new combinations; **version skew** is their simultaneous operation. **Expand-and-contract** adds compatible form, migrates, then removes old form. A **feature flag** separates code and behavior; a **canary** limits initial exposure. **Rollback** restores a prior deployable or behavior; **roll-forward** corrects with a successor. **Blast radius** is exposed users, data, operations, and dependencies. A repository stores source, an artifact is a build output, a process runs and fails, and data authority owns truth; none automatically determines another.

### Answer 2

With four unavailable, capacity is $(18-4)\times700=9{,}800$/s, leaving 800/s arithmetic margin. Require $(18-m)700\ge9{,}000$, so $18-m\ge12.857$ and at least 13 instances must remain; maximum integer unavailable is $18-13=5$. Six unavailable leave only 8,400/s. This omits traffic skew, startup and warmup, zones, shared failures, per-request cost, dependencies, retry load, health-detection delay, and safety reserve. Measured failure-domain rollout tests and admission policy must validate it.

### Answer 3

First add structured currency and minor-unit amount while retaining integer cents; define exact conversion, currency authority, range, rounding, and mismatch rejection. Database stores both or derives one transactionally. API and messages add optional structured form with stable defaults; batch manifests version the schema. Deploy servers and consumers that read both before any producer depends on the new form. Backfill idempotently and reconcile counts and sums by currency. New writers populate both under one policy; old mobile clients continue receiving cents. Shift reads and compare results, then stop old writes. Retain rollback readers until all supported clients, messages, exports, jobs, and restored states are compatible. Remove cents only in a later contraction after evidence and published client policy. Rollback never interprets new currencies it cannot represent.

### Answer 4

A modular monolith offers one runtime and transaction boundary, lower platform cost, and simpler integrated tests; it accepts one deployment schedule and broader blast radius. Five genuine services can scale, secure, own, and release independently when domains, data, contracts, and teams differ, but pay network, consistency, platform, observability, mixed-version, and on-call costs. Five lockstep artifacts pay much of that distribution cost without release autonomy and form a distributed monolith. Choose the monolith when change and runtime forces cohere; independent services when measured autonomy, scaling, security, or failure needs justify them. Lockstep services should either restore compatibility and ownership independence or recombine. Repository count is not decisive.

### Answer 5

Central dispatch and each station server are owned deployables with versioned APIs and replicated data contracts; vehicle clients and radio gateways have long compatibility windows and offline protocols. Maps are immutable versioned data artifacts; safety rules are signed configuration or code under a certified lifecycle, not casual flags. Build each binary once, record digest and provenance, promote exact artifacts, and authenticate deployment identities. Expand contracts before devices use them; tolerate supported old devices, sequence station and central rollout, and test mixed radio formats. Activation proceeds by region and station with capacity for old/new instances and disconnected vehicles. Rollback is allowed only if prior versions read current incident, assignment, and message state; completed dispatches cannot be undone and require reconciliation. Local commanders retain narrowly delegated manual authority during disconnection. Evidence records artifact, configuration, rule version, client version, business outcomes, missed/duplicate messages, and recovery. Full credit requires that release convenience never overrides current safety authority or honest irreversible effects.
