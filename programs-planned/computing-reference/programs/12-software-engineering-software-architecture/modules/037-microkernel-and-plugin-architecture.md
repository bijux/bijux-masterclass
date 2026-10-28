---
module_id: SARCH-037
program: Software Engineering: Software Architecture
level: 1
module_number: 37
title: Microkernel and Plugin Architecture
status: complete
last_verified: 2026-09-06
---

# Microkernel and Plugin Architecture

## One-Page Review

### Governing question

How can a system keep a small, coherent core while allowing independently developed extensions to add behavior without gaining accidental authority over the whole product?

### Essential definitions

- A **microkernel architecture** places stable, essential policy and coordination in a deliberately small core and moves variable capabilities into replaceable extensions. This application-architecture meaning is related to, but distinct from, an operating-system microkernel.
- A **plugin** is a separately identifiable extension installed into a host through declared contracts and lifecycle rules.
- An **extension point** states where and under what semantics extensions may contribute, replace, observe, or intercept behavior.
- A **service provider interface (SPI)** is the host-facing contract implemented by a provider; an application programming interface (API) is commonly the contract called by clients. A plugin system may expose both.
- The **host** discovers, validates, loads, initializes, invokes, stops, and possibly unloads plugins.
- A **contribution** is data or behavior supplied at an extension point, such as a command, parser, renderer, or storage driver.
- A **capability** is an explicit authority to perform a class of action or access a resource.
- **Compatibility** means that a particular host, extension contract, plugin, platform, and dependency set can interact with the required semantics—not merely that their version strings parse.
- **In-process isolation** is primarily a software boundary; **out-of-process isolation** can add address-space, identity, resource, and crash boundaries.
- A **contract test kit** exercises observable obligations shared by every implementation of an extension contract.

### Central model, mechanism, or theorem

Let core $K$ publish extension points $P=\{p_1,\ldots,p_m\}$ and let installed plugins be $G=\{g_1,\ldots,g_n\}$. A plugin $g$ is eligible for point $p$ only when

$$
Eligible(g,p)=Declared(g,p)\land Compatible(g,p)\land Trusted(g)\land ResourcesAvailable(g).
$$

Composition selects and orders only eligible contributions. The lifecycle is explicit:

$$
discovered\rightarrow validated\rightarrow loaded\rightarrow initialized\rightarrow active\rightarrow draining\rightarrow stopped\rightarrow unloaded.
$$

Failure may occur from any state and must lead to a declared quarantine, retry, rollback, or terminal state. The core is extensible only where its contracts say so; dynamic loading alone does not create a sound plugin architecture.

### Critical invariants

- keep the core sufficient for its essential policy but no larger than justified;
- make every extension point's inputs, outputs, side effects, ordering, concurrency, failure, and version semantics explicit;
- depend on stable contracts, not plugin implementations or private host internals;
- separate discovery, selection, authorization, loading, activation, and invocation;
- validate identity, provenance, compatibility, dependencies, configuration, and requested capabilities before activation;
- grant least authority and treat plugin code according to its trust boundary;
- bound time, memory, CPU, threads, descriptors, storage, network access, and contribution counts where relevant;
- define deterministic conflict and ordering rules; reject unsatisfiable or cyclic configurations;
- make lifecycle transitions, state ownership, upgrades, migration, drain, rollback, and recovery explicit;
- contain or surface plugin failures without silently corrupting host state;
- preserve observability by plugin identity, version, extension point, invocation, and outcome;
- test the host contract, every plugin, compatibility matrices, negative cases, and recovery behavior.

### Common failures

Frequent failures include calling any dynamically loaded library a plugin; turning the core into a catch-all; exposing host internals as an accidental SPI; allowing plugins to reach global mutable state; trusting signatures as proof of safety; resolving dependencies nondeterministically; permitting cyclic interceptor ordering; hot-unloading code with live calls; sharing unversioned persisted state; letting one plugin exhaust the host; swallowing plugin exceptions; loading incompatible binary interfaces; giving every extension full filesystem or network access; testing plugins only with mocks; and assuming process isolation alone prevents semantic damage.

### Compact example

An editor core owns documents, authorization, undo, and command dispatch. A formatter plugin implements `format(document_snapshot, options) -> edits` at a versioned extension point. The host validates its identity and compatibility, grants access only to the snapshot, runs it with a deadline, validates returned edits, and applies them through the core's transaction and undo policy. The plugin adds formatting without owning document persistence or bypassing authorization.

### Connections

[SARCH-032](032-modular-monoliths.md) supplies strong internal boundaries; [SARCH-036](036-client-server-architecture.md) supplies remote-boundary reasoning used for out-of-process plugins. [SARCH-038](../ROADMAP.md) next examines service-oriented architecture. Software Engineering Patterns owns object-level patterns; Operating Systems owns kernel architecture and protection mechanisms.

## Governing Question

Products often need a stable identity and a variable feature set. Editors accept language tools, databases accept storage or procedural extensions, build systems accept task providers, and analysis platforms accept importers and rules. Rebuilding the host for every variation slows delivery and gives optional features excessive coupling to essential policy.

Microkernel and plugin architecture addresses that pressure by distinguishing what must remain coherent from what may vary independently. The hard problem is not loading code. It is defining a small core, meaningful extension contracts, controlled composition, lifecycle, compatibility, authority, failure containment, and evidence. An extension mechanism without these disciplines merely moves coupling to runtime.

## Why This Matters

A well-designed plugin system supports product lines, third-party ecosystems, optional deployments, specialized hardware, and different release cadences. It can keep the host understandable while allowing features to evolve independently. It can also make replacement and experimentation cheaper because variants meet the same explicit contract.

The same openness creates risk. Plugin code may execute inside the host's trust and failure domain. Compatibility spans host versions, plugin versions, platforms, dependencies, state formats, and configurations. A plugin can block startup, deadlock shared resources, corrupt data, leak secrets, or destabilize the user interface. Marketplace scale adds provenance, review, revocation, and support concerns.

Architecture therefore must answer who owns essential policy, what may be extended, who can install an extension, what authority it receives, how it is selected, and how the system recovers when it fails. “We have a plugin API” is not an architectural assurance.

## Prerequisites and Retrieval

Retrieve module, component, interface, dependency, information hiding, cohesion, coupling, inversion of control, dynamic linking, process, thread, address space, authentication, authorization, least privilege, version compatibility, state machine, transaction, idempotency, concurrency, resource budget, observability, fault containment, and rollback.

From SARCH-014 retrieve modularity tactics; SARCH-015 provides evolvability; SARCH-022 through SARCH-024 distinguish module, component-and-connector, and runtime views; SARCH-032 provides modular-monolith boundaries; and SARCH-036 explains why moving a plugin out of process changes failure and communication semantics.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish a microkernel architecture from dynamic linking, frameworks, operating-system microkernels, and arbitrary add-ons;
2. identify essential core policy and justify what belongs outside it;
3. specify extension points as semantic contracts rather than callback signatures;
4. design discovery, validation, composition, activation, drain, and removal lifecycles;
5. reason about host-plugin dependency direction and information hiding;
6. define compatibility, dependency, conflict, and deterministic ordering rules;
7. choose in-process or out-of-process execution from trust, latency, failure, and operational needs;
8. constrain plugin authority and resource consumption;
9. govern plugin-owned state, upgrades, rollback, and recovery;
10. design contract, compatibility, security, failure, and operational tests for an extension ecosystem.

## Core Exposition

**Begin with variability, not a loader.** A plugin architecture is justified when a coherent product must support capabilities that vary by customer, domain, deployment, or release cadence. The architecture identifies a stable center and planned axes of variation. If all features ship, change, and fail together, ordinary modules may be simpler.

Loading a library at runtime does not establish the style. A sound design needs stable extension semantics, composition, lifecycle, compatibility, authority, and recovery. Conversely, plugins need not be dynamically loaded: statically selected providers can still implement explicit extension contracts and preserve architectural separation.

**Define the core by essential responsibility.** The core—often called the microkernel or host kernel—owns the minimum policy needed to keep the product coherent. Typical responsibilities include domain identity, canonical state, authorization, lifecycle coordination, contribution registry, transaction boundaries, and invariant enforcement. “Minimum” is not a line-count target. A core too small can push shared policy into inconsistent plugins; a core too large becomes the monolith the style was meant to avoid.

Parnas's information-hiding argument places change-prone design decisions behind module interfaces [1]. Apply it in both directions: plugins should not know private host representation, and the host should not encode the internals of particular plugins. The stable contract carries only information required for collaboration.

**Distinguish APIs from SPIs.** An API is commonly consumed by a caller to use host services. An SPI is implemented by a provider so the host can call it. A plugin often implements one or more SPIs and calls a restricted host API. The distinction clarifies direction and authority: implementing `Renderer` does not imply permission to mutate documents, read credentials, or register arbitrary network handlers.

Name every extension point by domain intent: `document.formatter`, `build.executor`, or `storage.codec`. Generic hooks such as `beforeAnything(object)` become accidental universal backdoors. Each point should say whether a plugin contributes a named item, chooses among alternatives, decorates a pipeline, observes facts, validates a proposal, or replaces a strategy.

**Specify semantics beyond types.** A callback signature expresses shape, not meaning. The contract must define valid inputs, ownership, nullability, units, encoding, result obligations, side effects, error taxonomy, retries, cancellation, deadlines, thread safety, reentrancy, ordering, determinism, privacy, and compatibility.

For a formatter, decide whether input is mutable, whether edits may overlap, how offsets are encoded, whether the operation must be deterministic, and how cancellation is observed. For an authentication plugin, specify fail-closed behavior, audit obligations, identity binding, and which claims the core will accept. These semantic rules belong with the extension point and its tests.

**Control dependency direction.** Plugins compile or configure against stable extension contracts and restricted host services. The core invokes abstractions without importing plugin implementations. A composition root discovers and connects implementations. This inversion keeps optional features from becoming compile-time prerequisites of essential policy.

Do not confuse inversion with absence of dependency. The host depends semantically on the behavior it requests; the plugin depends syntactically and semantically on the SPI. Record both. A dependency view, runtime connector view, deployment view, and trust view reveal different risks.

**Separate discovery from activation.** Discovery finds plugin candidates through static registration, configuration, directory scanning, package metadata, a registry, or an administrative service. Discovery is not approval. A candidate must be checked for identity, provenance, signature policy, compatible contract, dependencies, conflicts, platform, configuration, capabilities, and resource requirements before loading or activation.

Static registration is predictable and easy to analyze but requires rebuilding or redeploying the host. Dynamic discovery supports independent installation but increases startup, supply-chain, compatibility, and recovery complexity. Directory scanning is convenient but dangerous when filesystem write permission implies code-execution authority.

**Make selection deterministic.** Multiple plugins may implement the same point. Define whether the host chooses exactly one, all, a priority order, a user-selected provider, a capability match, or a composed chain. Tie-breaking must be stable. Never let filesystem enumeration or hash-map order decide production behavior.

If contributions declare `before` and `after` constraints, build a directed ordering graph. Activation succeeds only if the graph is acyclic and all required vertices exist. A topological order may still be nonunique; add stable tie-breaking or reject ambiguity when order changes semantics.

**Resolve dependencies as a model, not a sequence of guesses.** Plugins can require host capabilities, extension-contract ranges, other plugin capabilities, native libraries, or platform features. State whether dependencies are required or optional, singleton or multiple, private or shared. Version ranges must have declared meaning; semantic version syntax cannot prove semantic compatibility.

Dependency solving chooses a set that satisfies constraints and conflicts. If no solution exists, report a concise explanation and preserve the last known-good set. Automatically choosing a different major version or silently disabling a security plugin converts a configuration error into hidden behavior.

**Model lifecycle explicitly.** A useful lifecycle separates discovery, validation, loading, initialization, activation, drain, stop, and unload. Initialization acquires or prepares resources; activation makes contributions visible. This separation allows the host to reject a plugin before users depend on it.

Stopping new invocations is not unloading. Active calls, callbacks, threads, file handles, memory references, timers, and native code may remain. Drain waits or cancels according to contract. In runtimes that cannot reliably unload code, “disable” may mean stop contributions now and remove code after host restart. Say so honestly.

**Treat hot reload as a distributed state change inside one product.** Replacing an active plugin must coordinate new admission, in-flight work, state snapshot or migration, dependency graphs, contribution registries, and rollback. An atomic pointer swap is insufficient if old code owns threads or durable state.

Define quiescence: no new calls enter the old version, every prior call finishes or is safely cancelled, and owned resources reach a transferable or terminal state. If this cannot be guaranteed, use restart-based replacement. Operational simplicity is often worth brief planned unavailability.

**Choose the isolation boundary deliberately.** In-process plugins offer low call overhead, direct language types, and simple debugging. They commonly share address space, runtime, privileges, heap, scheduler, and crash fate. Language access modifiers are not a security boundary against hostile code.

Out-of-process plugins communicate through IPC or a network protocol. They add serialization, latency, deployment, supervision, and versioning costs, but can have separate identities, memory limits, filesystems, network policies, and restart lifecycles. They still can return malicious data, consume host capacity, or trigger authorized harmful operations. Process isolation strengthens mechanisms; it does not replace semantic validation.

**Grant capabilities instead of ambient access.** A plugin should receive narrow handles for necessary actions rather than unrestricted host objects or ambient operating-system authority. A spell checker may need document text but not credential storage. An exporter may need a destination stream but not arbitrary filesystem traversal.

Saltzer and Schroeder's protection principles include least privilege, fail-safe defaults, economy of mechanism, and complete mediation [2]. Apply them at installation and invocation. Installation authority, execution authority, and resource authority are distinct. A valid signature establishes a key-related provenance claim; it does not prove correctness, benevolence, or vulnerability absence.

**Validate across every trust boundary.** Treat plugin metadata, configuration, dependencies, returned contributions, errors, logs, and state migrations as inputs. Validate sizes, encodings, identifiers, paths, URLs, edits, queries, and generated artifacts. A trusted first-party plugin can still be defective; an untrusted plugin may be intentionally adversarial.

For third-party ecosystems, govern publisher identity, package immutability, review level, signatures, revocation, vulnerability response, permission disclosure, update channels, and audit history. Avoid claiming that marketplace review creates perfect safety.

**Bound resource use.** Each plugin can consume CPU, memory, threads, descriptors, storage, network bandwidth, queue slots, log volume, and invocation time. The host needs per-plugin and aggregate budgets, admission, cancellation, quotas, and saturation evidence. An in-process plugin may be impossible to preempt safely; this can justify process isolation for untrusted or expensive work.

If plugin limits are individually valid but their total exceeds host capacity, the architecture still fails. Budget composition must account for concurrency and shared overhead. Measure actual usage, but do not turn one benchmark into a universal capacity guarantee.

**Contain failures and define degradation.** A plugin may fail during discovery, initialization, invocation, state migration, or stop. Decide which failures block host startup, disable one contribution, fall back to a safe provider, retry, quarantine the plugin, or require operator intervention. Security, authorization, and data-integrity extensions often must fail closed; decorative extensions may fail open.

Do not catch every exception and continue with potentially corrupted shared state. In-process failure can violate host invariants before an exception appears. Establish transaction boundaries and validate proposed changes before committing them. Supervise out-of-process plugins and bound restart loops.

**Own state explicitly.** State may belong to the core, one plugin instance, a plugin family, a tenant, or a shared extension contract. Define schema, version, ownership, backup, migration, encryption, retention, concurrent access, and deletion. Plugins must not write private fields into an unversioned shared blob.

Upgrades should distinguish code activation from durable-state migration. A forward migration can make rollback impossible. Expand-compatible-contract-and-contract techniques, dual readers, or migration checkpoints can preserve rollback, but they add complexity. Test old-code/new-state and new-code/old-state combinations that operations may actually produce.

**Preserve transactions and invariants.** A plugin that proposes domain changes should do so through core-owned commands or transactions. The core validates authorization and invariants and commits atomically where possible. Giving the plugin a direct database connection may bypass audit, locking, tenancy, and rollback policy.

Callbacks inside a host transaction can deadlock, block locks, or make an external side effect that cannot be rolled back. Prefer compute-then-validate for pure contributions, use outbox or post-commit work for external effects, and document reentrancy. A plugin must not call back into the same non-reentrant host operation unless the contract permits it.

**Version observable contracts.** Compatibility includes source, binary, wire, behavior, data, configuration, and operational expectations. A plugin can load successfully yet break because a default, error, ordering rule, unit, or timing assumption changed. State the compatibility dimension and support window.

OSGi Core Release 8 defines a mature modular runtime model with bundles, lifecycle, services, metadata, and versioning [3]. It is useful evidence that runtime modularity needs more than class loading, but adopting OSGi—or any framework—does not decide a product's domain boundaries or security policy.

Use additive evolution when semantics permit, deprecate with usage evidence, and test a matrix of supported host, SPI, plugin, platform, and persisted-state versions. The matrix can grow multiplicatively; declare a finite supported region rather than implying every combination works.

**Observe the ecosystem.** Record plugin identity and version, publisher, extension point, lifecycle transition, activation result, capability grant, invocation count, latency, failures, resource use, quarantine, and state migration. Correlate plugin work with the host operation without leaking plugin or user secrets.

Aggregated host metrics can hide one failing extension. Conversely, high plugin error counts may represent correctly rejected hostile inputs. Logs and traces are evidence of observed execution, not proof that unobserved state is sound.

**Test contracts and hostile behavior.** A contract test kit should run against every provider and include valid, boundary, malformed, slow, concurrent, cancellation, reentrancy, and failure cases. Host tests use deliberately defective plugins: failure during initialization, infinite work, excessive allocation, invalid contributions, dependency cycles, corrupt state, and refusal to stop.

Test installation, upgrade, rollback, revocation, host restart, plugin crash, partial state migration, mixed versions, and last-known-good recovery. Mocks help host development but can encode the host's assumptions; real independent implementations reveal ambiguities.

**Govern extension-point evolution.** Every public extension point becomes a long-lived product commitment. Assign an owner, compatibility policy, documentation, test kit, telemetry, deprecation process, and retirement criteria. Extension points should be few and intentional. Adding a universal escape hatch to satisfy one plugin creates permanent coupling and authority.

Third-party ecosystems need support boundaries: which host versions are supported, who diagnoses failures, whether plugins can be remotely disabled, how publishers are notified, and what happens when a critical dependency is abandoned. Governance is part of the architecture because it determines which configurations can exist.

**Know when not to use the style.** Use ordinary internal modules when all code is owned, released, trusted, and deployed together and variability is modest. Use configuration for declarative choices that do not require new behavior. Use separate services when independent scaling, identity, failure containment, or technology warrants the communication boundary. Use scripting only when the language, authority, and lifecycle are explicitly governed.

A plugin architecture can exist inside a modular monolith, and out-of-process plugins can resemble services. Name the decisive property: extension contracts controlled by a host. Do not use “microkernel” to imply smallness, security, or reliability without evidence.

## Definitions and Notation

Let $K$ be the core, $P=\{p_1,\ldots,p_m\}$ extension points, and $G=\{g_1,\ldots,g_n\}$ installed plugins. `Declared(g,p)` means plugin $g$ declares a contribution to $p$. `Compatible(g,p)` is true only within a stated host, contract, platform, dependency, configuration, and state-version context.

Let $Cap(g)$ be capabilities requested by $g$ and $Grant(g)\subseteq Cap(g)$ those granted by policy. An invocation is authorized only if its required capability is in $Grant(g)$ and the core still mediates the target resource.

For an ordering graph $D=(V,E)$, vertices are contributions and edge $(a,b)$ means $a$ must run before $b$. A valid activation order exists only if $D$ is acyclic. If multiple topological orders exist and order affects behavior, policy supplies a stable tie-breaker or rejects the ambiguity.

Let $R_j(g)$ be plugin $g$'s reserved demand for resource class $j$ and $B_j$ the host budget. A necessary admission condition is

$$
\sum_{g\in Active}R_j(g)+R_j(candidate)\le B_j.
$$

This is a planning bound, not a performance theorem: reservations may not equal use, resources interact, and in-process execution may resist enforcement.

The plugin lifecycle state set is $L=\{discovered,validated,loaded,initialized,active,draining,stopped,unloaded,failed,quarantined\}$. Every transition has an actor, precondition, side effect, timeout, observable outcome, and recovery rule.

## Mechanisms, Invariants, or Proof Structure

**Core invariant.** Essential domain authority and cross-plugin invariants have one owner in the core or an explicitly named authority. Optional plugins cannot silently redefine them.

**Contract invariant.** Each extension point defines semantics, not only types. A contribution outside declared effects, ordering, resource, or authority rules is rejected or contained.

**Dependency invariant.** Core policy does not import or inspect concrete plugin internals. Plugins depend on supported contracts and restricted services, not private host representation.

**Eligibility derivation.** Discovery supplies candidates but makes no safety claim. Compatibility without trust permits hostile code; trust without compatibility permits breakage; both without resources permit overload. Therefore activation requires their conjunction plus declared contribution.

**Ordering argument.** A directed cycle $a\prec b\prec c\prec a$ requires each contribution to precede itself by transitivity, which no strict execution order can satisfy. Rejecting cycles is necessary. Acyclicity permits a topological order, but deterministic semantics may require tie-breaking among incomparable vertices.

**Lifecycle invariant.** A plugin becomes callable only after validation and initialization succeed. Stop prevents new admission before unload. Failed drain never masquerades as successful unload.

**Authority invariant.** Installation, activation, and invocation do not imply ambient authority. Every sensitive operation is mediated using plugin identity, principal, resource, and granted capability.

**State invariant.** Every durable field has one schema owner and compatible migration/rollback path. A plugin upgrade cannot mutate shared durable state outside that policy.

**Containment invariant.** The chosen boundary matches the consequence of failure. An in-process boundary cannot honestly promise memory, crash, or privilege isolation that its runtime and operating system do not enforce.

**Evidence invariant.** Passing contract tests demonstrates the tested observations for a declared matrix; signatures demonstrate a provenance property; process separation demonstrates a mechanism. None proves universal correctness or safety.

## Alternatives and Trade-Offs

| Choice | Advantages | Costs and risks | Prefer when |
|---|---|---|---|
| Ordinary modules | simple build, tracing, transactions, and ownership | coordinated releases; less external extensibility | one team and release unit own variation |
| Static plugins | analyzable set; predictable startup; compiler/linker checks | rebuild or redeploy to change providers | deployments choose variants infrequently |
| Dynamic in-process plugins | low latency; direct types; rich host integration | shared crash, memory, privilege, and resource domain | trusted, performance-sensitive extensions |
| Out-of-process plugins | stronger crash, identity, resource, and privilege controls | IPC, serialization, supervision, and deployment cost | untrusted, failure-prone, or independently operated extensions |
| Declarative configuration | easy validation and review; no arbitrary code | limited expressiveness | choices are data, not new algorithms |
| Embedded scripting | flexible domain automation | language sandbox, debugging, compatibility, and authority burden | bounded user logic is a product requirement |
| Separate services | independent scaling, release, and technology | remote latency, partial failure, operations, and data consistency | capability is independently owned and operationally substantial |
| One selected provider | simple semantics and state ownership | less composition | alternatives are mutually exclusive |
| Ordered contribution chain | composable cross-cutting behavior | ordering, reentrancy, latency, and failure coupling | each stage has narrow semantics and deterministic order |
| Restart-based upgrade | simple quiescence and cleanup model | temporary interruption | safe unload cannot be guaranteed |
| Hot replacement | lower interruption | complex drain, state transfer, rollback, and observation | continuity requirement justifies verified machinery |

Architecture may combine choices. A host can use static trusted renderers, out-of-process third-party analyzers, and declarative themes. Apply the strictest boundary warranted by each extension point rather than declaring one universal plugin policy.

## Failure Modes and Misconceptions

1. **“Dynamic loading means plugin architecture.”** Loading is one mechanism; the style requires stable contracts, composition, lifecycle, and governance.
2. **“A tiny core is always better.”** Moving shared invariants into plugins creates duplication and inconsistent policy.
3. **“Interfaces guarantee decoupling.”** Semantics, shared data, order, timing, and release policy can remain tightly coupled.
4. **“Signed means safe.”** A signature binds content to a key under a verification policy; it does not establish correctness or harmlessness.
5. **“First-party plugins need full trust.”** Defects and compromised build systems still justify least privilege and validation.
6. **“Process isolation solves security.”** It helps enforce memory and resource boundaries but cannot validate authorized requests or returned data.
7. **“Version ranges prove compatibility.”** Versions are declarations; behavioral and state compatibility need evidence.
8. **“Discovery implies activation.”** Candidates must pass policy and compatibility checks first.
9. **“Priority numbers define an order.”** Equal priorities, missing dependencies, and cycles need deterministic resolution.
10. **“Disable equals unload.”** Live calls, threads, references, native libraries, and state may remain.
11. **“Hot reload is just swapping a pointer.”** Admission, in-flight calls, state, dependencies, and rollback must coordinate.
12. **“Catching plugin exceptions contains failure.”** The plugin may already have mutated shared state or exhausted resources.
13. **“Contract tests prove correctness.”** They support only the tested obligations, implementations, versions, and environments.
14. **“Plugins may own their database tables without coordination.”** Shared transactions, backups, retention, and migrations still require authority.
15. **“A generic hook is future-proof.”** Broad hooks expose internals, obscure authority, and freeze accidental behavior.
16. **“Microkernel here means an OS kernel.”** This chapter concerns application architecture; operating-system microkernels move OS services across protection and communication boundaries.

## Worked Examples

### Example 1

**Situation.** An editor needs independently supplied formatters for different languages.

**Reasoning.** The core owns documents, authorization, versions, transactions, and undo. It publishes `document.formatter` with immutable document snapshot, language identifier, options, deadline, and cancellation input. A plugin returns a bounded ordered edit set, not a mutable document handle. The core validates nonoverlapping offsets against the snapshot version before applying edits as one undoable transaction. Registration is static for built-in formatters, so dynamic loading is unnecessary.

**Conclusion.** Static plugins still realize the architecture when stable extension contracts and core-owned invariants separate variable formatting from essential document policy.

### Example 2

**Situation.** Host 5 changes an extension result from byte offsets to Unicode scalar indices, but a plugin built for Host 4 loads successfully.

**Reasoning.** The binary signature has not changed, yet behavior has. For text `Aé`, UTF-8 byte and scalar positions differ. Applying byte offset 2 as scalar index 2 can target the wrong boundary or exceed the document. Compatibility must therefore identify the coordinate system in the contract version. Host 5 rejects the old provider or supplies an explicit adapter whose conversions and limits are tested.

**Conclusion.** Loadability is weaker than semantic compatibility; units and encodings are contract elements.

### Example 3

**Situation.** Plugin `reporting` requires parser capability version 2, plugin `legacy-import` requires version 1, and the host permits only one parser provider.

**Reasoning.** Installing whichever directory entry appears first is nondeterministic. The constraints require two mutually incompatible singleton providers, so no valid composition exists. The resolver reports the minimal conflict, leaves the last known-good plugin set active, and asks an operator to upgrade `legacy-import`, choose a compatible adapter, or remove one feature. Silently disabling either plugin would change product behavior.

**Conclusion.** Dependency failure is a governed configuration outcome, not permission to guess.

### Example 4

**Situation.** A signed third-party theme plugin asks for document contents and unrestricted network access.

**Reasoning.** Theme rendering needs colors, fonts, and bounded presentation metadata, not document text or network egress. The signature establishes package provenance under the publisher key but does not justify requested authority. Installation denies the extra capabilities. If the plugin cannot operate with the minimal grant, it remains inactive and the host records the decision without executing its initialization code.

**Conclusion.** Provenance and least authority answer different questions; signed code still receives only necessary capabilities.

### Example 5

**Situation.** An image decoder plugin processes files from unknown users and sometimes crashes on malformed inputs.

**Reasoning.** In-process execution shares the host's memory and crash domain, so exception handling cannot contain native memory corruption. The host moves decoding into a supervised process with a read-only input handle, bounded output, memory and CPU limits, no network, and a short lifetime. It validates decoded dimensions before allocation and substitutes a safe error image on failure. The process boundary adds serialization and startup cost, measured against the security consequence.

**Conclusion.** Out-of-process execution is justified by hostile inputs and failure consequence, while output validation remains necessary.

### Example 6

**Situation.** A host has memory budget $B=2{,}048$ MiB. Core and shared overhead reserve 1,100 MiB. Active plugins reserve 220, 180, and 160 MiB. A candidate requests 500 MiB.

**Reasoning.** Existing reservation is $1{,}100+220+180+160=1{,}660$ MiB. Adding the candidate yields $2{,}160$ MiB, exceeding the budget by $112$ MiB. Admission rejects or requires a different configuration. Accepting because each plugin individually requests less than 2,048 MiB ignores aggregate demand. The calculation remains a planning bound; measured peaks and shared allocations still require observation.

**Conclusion.** Resource admission must compose plugin reservations with core and shared demand.

### Example 7

**Situation.** Three request interceptors declare `auth before audit`, `audit before compression`, and `compression before auth`.

**Reasoning.** The graph contains the directed cycle $auth\prec audit\prec compression\prec auth$. Any proposed first item must also come after another item in the cycle. No strict order satisfies all constraints. The host rejects activation and reports the cycle. Dropping one edge silently could put compression before authentication or audit before identity establishment, changing security semantics.

**Conclusion.** Cyclic ordering constraints are unsatisfiable and must fail deterministically.

### Example 8

**Situation.** Operators want to replace an active pricing plugin without restarting while 80 invocations and delayed callbacks are outstanding.

**Reasoning.** The host first removes the old version from new selection, marks it draining, and routes new work to the validated new version. It waits for old invocations and callbacks under a deadline. If the plugin's state is versioned and transferable, migration occurs at a declared checkpoint; otherwise replacement aborts and the old version resumes. If calls cannot be accounted for or the runtime cannot unload safely, the architecture uses a controlled restart rather than claiming hot replacement.

**Conclusion.** Safe replacement requires quiescence and state rules; inability to prove them changes the deployment strategy.

### Example 9

**Situation.** A tax plugin upgrade migrates its durable table irreversibly before the new code passes a production health check.

**Reasoning.** Rolling code back leaves the old plugin unable to read the new schema. A safer plan first deploys a backward-compatible schema expansion, uses code that can read old and new rows, migrates with checkpoints, verifies results, and contracts only after the rollback window closes. The core records schema ownership and prevents another plugin from modifying the table. Backups help disaster recovery but do not make an online rollback instantaneous.

**Conclusion.** Code activation and durable-state migration need separate, tested compatibility and rollback policies.

### Example 10

**Situation.** A laboratory instrument host accepts vendor drivers, but a defective driver requests an unsafe actuator setting.

**Reasoning.** The driver translates a device protocol; it does not own physical safety. The core validates requested ranges, operating mode, calibration state, interlocks, principal authority, and rate limits before issuing commands. The driver runs in a restricted process and cannot address hardware directly. If it times out, the host enters the instrument's defined safe state and records an audit event. Process isolation contains crashes, while core mediation protects the domain invariant.

**Conclusion.** High-consequence plugin systems keep safety authority in a small core and use isolation as a supporting mechanism, not the safety proof.

## Cross-Program Connections

- **Software Engineering Patterns:** factories, adapters, dependency injection, strategy, observer, and command can implement parts of a plugin system; none alone establishes its architectural trust and lifecycle model.
- **Software Engineering: Software Delivery and Reliability Engineering:** artifact provenance, progressive delivery, rollback, supervision, observability, and incident response govern plugin releases.
- **Operating Systems:** processes, address spaces, privilege, scheduling, resource limits, dynamic linking, and OS microkernels supply enforcement mechanisms and a distinct use of “microkernel.”
- **Security Engineering:** capabilities, sandboxing, code signing, supply-chain controls, revocation, mediation, and malicious-input handling determine the extension trust boundary.
- **API and Service Engineering:** out-of-process plugins need versioned protocols, error semantics, deadlines, cancellation, and compatibility.
- **Database Engineering:** plugin-owned schemas, transactions, migrations, concurrency, and recovery require explicit data authority.
- **Platform Engineering:** registries, installation policy, supported matrices, diagnostics, and self-service determine whether an ecosystem remains operable.
- **Programming Languages and Semantics:** type systems, module systems, effects, reflection, and runtime loading shape what extension contracts can enforce.

## References

1. David L. Parnas, “On the Criteria To Be Used in Decomposing Systems into Modules,” *Communications of the ACM* 15(12), 1972. <https://doi.org/10.1145/361598.361623>
2. Jerome H. Saltzer and Michael D. Schroeder, “The Protection of Information in Computer Systems,” *Proceedings of the IEEE* 63(9), 1975. <https://doi.org/10.1109/PROC.1975.9939>
3. OSGi Alliance, *OSGi Core Release 8*, 2020. <https://docs.osgi.org/specification/osgi.core/8.0.0/>
4. Frank Buschmann, Regine Meunier, Hans Rohnert, Peter Sommerlad, and Michael Stal, *Pattern-Oriented Software Architecture, Volume 1: A System of Patterns*, Wiley, 1996.
5. Clemens Szyperski, Dominik Gruntz, and Stephan Murer, *Component Software: Beyond Object-Oriented Programming*, 2nd ed., Addison-Wesley, 2002.
6. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021.
7. Ross Anderson, *Security Engineering: A Guide to Building Dependable Distributed Systems*, 3rd ed., Wiley, 2020. <https://www.cl.cam.ac.uk/~rja14/book.html>
8. Object Management Group, *Common Object Request Broker Architecture (CORBA) Specification, Version 3.4*, 2021. <https://www.omg.org/spec/CORBA/3.4/About-CORBA>

## Exercises

### Exercise 1

Define core, plugin, extension point, SPI, capability, and compatibility. Explain why a dynamically loaded library is not necessarily a plugin architecture.

### Exercise 2

A host budget is 8 GiB. The core and shared runtime reserve 3.2 GiB. Four active plugins reserve 0.7, 0.9, 1.1, and 0.4 GiB. A candidate reserves 2.0 GiB. Apply the chapter's necessary admission bound, show the arithmetic, and state two limitations of the conclusion.

### Exercise 3

A plugin passes unit tests but occasionally freezes the host during shutdown. Diagnose the missing lifecycle evidence and propose a focused test and containment design.

### Exercise 4

Compare in-process and out-of-process execution for a first-party compiler extension that handles proprietary source code and runs for minutes. Recommend a design, including authority and resource controls, and state what evidence could change your choice.

### Exercise 5

Design a plugin boundary for a hospital infusion-pump management system that accepts vendor device adapters. Identify core policy, extension contract, trust and isolation, lifecycle, state, failure behavior, compatibility evidence, and one feature you would refuse to make extensible.

## Answers to the Exercises

### Answer 1

The **core** owns stable essential policy and coordination. A **plugin** is a separately identifiable extension installed under declared contracts and lifecycle. An **extension point** defines where and how contributions participate. An **SPI** is the provider-facing contract a plugin implements. A **capability** is explicit authority for a class of action or resource. **Compatibility** is the supported semantic relationship among host, contract, plugin, platform, dependencies, configuration, and state. Dynamic loading supplies code at runtime but does not by itself define contribution semantics, authority, selection, compatibility, lifecycle, resource bounds, or recovery; without those properties it is only a loading technique.

### Answer 2

Active reservation is $3.2+0.7+0.9+1.1+0.4=6.3$ GiB. With the candidate it becomes $6.3+2.0=8.3$ GiB, which exceeds the 8 GiB budget by 0.3 GiB. The necessary bound therefore rejects this configuration unless reservations or other allocations change. Limitations include that reservations may differ from actual peaks, resources interact, shared allocation may be double-counted or omitted, and the arithmetic says nothing about latency or safe enforcement. Any two of these with the correct bound earn full credit.

### Answer 3

Unit invocation tests do not show that stop prevents new calls, active calls terminate, plugin threads and callbacks are accounted for, deadlines work, resources close, or unload occurs safely. A focused test activates the plugin, starts a deliberately blocked invocation and delayed callback, initiates drain, verifies new admission is rejected, releases or cancels work, and checks that every thread, handle, contribution, and lifecycle event reaches the declared terminal state within a deadline. Containment may run the plugin in a supervised process so the host can terminate it after graceful drain fails; the host must still preserve transaction and state integrity. Merely catching a shutdown exception is insufficient.

### Answer 4

Minutes-long, compute-heavy work favors an out-of-process worker because scheduling, memory, CPU, cancellation, crash recovery, and secret access can be controlled independently. Give it read-only scoped source input, a bounded output channel, no ambient network or filesystem access, per-job identity, deadlines, quotas, and validated diagnostics/artifacts. Encrypt IPC and minimize logged source. In-process execution could be preferable if measured serialization dominates, the compiler runtime cannot operate remotely, the code is strongly trusted, and enforceable cooperative cancellation and resource accounting are demonstrated. The recommendation should change only from evidence about workload, threat model, failure consequence, toolchain constraints, and observed performance—not from “first party” alone.

### Answer 5

The core owns patient-device association, authenticated operator intent, dosage limits, drug-library rules, interlocks, audit, and the final command decision. A vendor adapter implements a versioned SPI translating canonical bounded device operations and returning typed status; it never receives a raw unrestricted hardware or database handle. Run it under a vendor identity in a restricted process with only the assigned device channel, bounded CPU/memory/time, and signed immutable package provenance plus independent validation. Lifecycle covers staged installation, compatibility validation, inactive initialization, activation, drain, rollback, quarantine, and safe restart. Adapter state is versioned and limited to protocol/session data; clinical authority remains core-owned. On timeout, malformed output, crash, or incompatible version, stop new commands, preserve an auditable unknown-outcome state, query device state through a trusted path when possible, and enter the clinically defined safe procedure. Test supported host/adapter/device/firmware combinations plus malformed, delayed, duplicate, restart, and rollback cases. Refuse to make dosage safety limits extensible by the vendor adapter. A complete alternative may place the safety authority in certified device firmware, but it must name that authority and retain end-to-end mediation and evidence.
