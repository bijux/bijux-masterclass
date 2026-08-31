---
module_id: SEPAT-098
program: Software Engineering: Patterns
level: 2
module_number: 98
title: Branch by Abstraction Pattern
status: complete
last_verified: 2026-08-29
---

# Branch by Abstraction Pattern

## One-Page Review

### Governing question

How can a team replace a deeply used implementation continuously on the mainline by introducing a stable abstraction, migrating callers incrementally, comparing old/new behavior, switching composition safely, and then removing every temporary branch?

### Essential definitions

- **Branch by Abstraction** replaces an internal implementation behind an abstraction while old and new code coexist on the shared mainline.
- A **seam** is a place where behavior can be substituted without editing every caller simultaneously.
- The **abstraction** expresses stable caller/domain capability and contract; it must not merely mirror old vendor/API quirks.
- An **old adapter** implements the new abstraction by delegating to the legacy implementation.
- A **replacement implementation** satisfies the same declared contract, possibly with a different internal model.
- **composition selection** chooses implementation at construction/configuration time; it should not scatter conditional branches through business code.
- A **release toggle** can temporarily select old/new behavior; it needs owner, scope, default, expiry and removal plan.
- **parallel/shadow comparison** invokes both implementations with effects isolated and compares normalized semantic results.
- **characterization tests** record relevant existing behavior before refactoring; they are evidence, not unquestionable specification.
- **convergence** means all callers use the abstraction, the replacement is authoritative, and old implementation/adapters/toggles/comparison scaffolding are removed.

### Central model, mechanism, or theorem

Let callers (C) depend on contract (A), and implementations (I_0,I_1\models A). Migration states are

$$
C\rightarrow I_0
\Rightarrow C\rightarrow A\rightarrow I_0
\Rightarrow C\rightarrow A\rightarrow\{I_0,I_1\}
\Rightarrow C\rightarrow A\rightarrow I_1
\Rightarrow C\rightarrow I_1\text{ through durable }A.
$$

Each arrow is a small releasable mainline change. Safety requires observational equivalence under the agreed contract for relevant inputs and effects: (obs_A(I_0,x)\equiv obs_A(I_1,x)), except documented intentional corrections. The pattern shortens integration branches; it does not make abstraction, state migration, concurrency or equivalence automatically correct.

### Critical invariants

- The abstraction belongs to caller/domain intent and exposes only semantics both implementations can honestly satisfy.
- Every caller migrates through the abstraction before implementation switching; bypasses are detected.
- Old adapter preserves behavior while seam introduction is independently tested/committed.
- Composition owns implementation choice; business methods do not repeatedly check flags.
- Stateful/effectful parallel execution has exactly one authoritative effect, with comparison isolated.
- Selection is deterministic and safe under configuration failure; incompatible state formats are gated.
- Contract tests run identically against old adapter and replacement, including errors, concurrency and resources.
- Performance, security, observability and operability are part of the contract evidence.
- Toggle/configuration has owner, creation/expiry, allowed states, telemetry and removal criterion.
- Completion deletes old code, bypasses, transitional adapter/toggle and stale tests/docs.

### Common failures

Failures include inventing an abstraction around the new library only; copying the old API wholesale; a giant “platform” interface; migrating callers and behavior in one unreviewable change; scattered `if new_backend`; untested old adapter; dual effects during comparison; nondeterministic cohort selection; two implementations writing incompatible state; ignoring concurrency/error/timeout/resource semantics; permanent toggles; retaining old transitive dependencies; testing mocks instead of shared contract suites; comparing only happy outputs; and calling a long-lived plug-in strategy a temporary migration.

### Compact example

A service replaces a password-hash verifier. First introduce `CredentialVerifier.verify(candidate, stored) -> VerificationResult` and an old adapter with unchanged behavior. Move all callers and prohibit direct legacy imports. Implement the new verifier; run shared invalid/malformed/timing/resource tests. Shadow only verification decisions, never rehash/write. Canary by tenant with safe default old. After compatible rehash-on-login migration and rollback horizon, switch default, remove old algorithm only when retained hashes no longer require it, then delete toggle/adapters/dependency.

### Connections

[Adapter](021-adapter.md), [Bridge](022-bridge.md), [Strategy](039-strategy.md), [Facade](025-facade.md) and [Dependency Injection](018-dependency-injection-as-a-creation-pattern.md) supply structure/composition. [Strangler Fig](097-strangler-fig.md) moves externally routed capabilities; Branch by Abstraction usually migrates inside one codebase/deployable. The successor [Anti-Patterns](../ROADMAP.md) examines abstractions/toggles that harden into a Golden Hammer or Big Ball of Mud.

## Governing Question

How should engineers construct and remove an abstraction branch so mainline remains deployable, implementation risk is isolated, and the result does not retain permanent migration debris?

A long-lived source-control branch delays integration and hides conflicts until replacement is “done.” Branch by Abstraction moves the branch point into a controlled runtime/composition seam on mainline. Small commits introduce interface, delegate through old behavior, add new behavior, switch and remove. Both implementations may coexist briefly, allowing production feedback and rollback.

The technique is most useful for internally pervasive components: persistence engines, clients, serializers, rendering, pricing algorithms, build subsystems or vendor libraries. It is not free. A bad abstraction freezes accidental semantics; stateful replacements need data migration; dual execution can duplicate effects; a forgotten toggle becomes permanent state-space. The removal half is part of the pattern.

## Why This Matters

Replacing a foundation often requires touching hundreds of call sites. Editing all callers and implementing the new backend simultaneously mixes two risks: structural redirection and semantic replacement. If tests fail, diagnosis is ambiguous. If work lives off-mainline, ongoing changes create merge debt and the untested delta grows.

An old adapter permits a safer proof: after callers depend on the new abstraction but it delegates to old code, behavior should remain unchanged. That commit validates the seam. Replacement can then be developed behind the same contract, compared and selected. Because each state is releasable, integration happens continuously.

However, “interface” is not synonymous with good boundary. If it exposes every old database primitive, the new implementation must mimic legacy and migration gains vanish. If it offers vague `execute(anything)`, callers still know implementation details. The right abstraction captures stable capability at the caller's altitude, with explicit errors, consistency, resource, security and observability semantics.

## Prerequisites and Retrieval

Learners should retrieve:

- interface segregation, dependency inversion, adapters, strategy and dependency injection;
- characterization, contract, property, differential and concurrency testing;
- trunk-based development, continuous integration and small reversible commits;
- feature-toggle taxonomy, ownership and lifecycle;
- state/schema expand–migrate–contract and compatibility;
- deterministic canary cohorts, shadow effects and observability;
- timeouts, cancellation, retries, resource ownership and security boundaries;
- dependency analysis, package/import enforcement and decommissioning.

Before continuing, explain why adding `NewDatabaseWrapper` whose methods match a chosen vendor SDK does not necessarily create a migration abstraction.

## Learning Objectives

After this module, learners can:

1. distinguish Branch by Abstraction from source branching, Strategy and Strangler Fig;
2. identify a stable internal capability seam and caller-owned contract;
3. introduce an old adapter without semantic change;
4. migrate callers incrementally and detect bypasses;
5. build shared contract/differential tests across implementations;
6. isolate effects/state during shadow or dual execution;
7. choose composition/toggle/cohort policy with safe failure behavior;
8. plan state/schema compatibility and rollback horizons;
9. separate structural, implementation, switch and removal commits;
10. prove completion by deleting transitional code and dependencies.

## Core Exposition

### Decide whether the branch belongs in code

Use Branch by Abstraction when one deployable has many direct dependencies on an implementation and a coherent substitution seam is possible. The replacement should be too large for one atomic refactor yet decomposable into safe mainline states. If the capability is already behind a stable interface, use ordinary implementation/configuration changes. If entire externally routed capabilities and independent data ownership move between systems, Strangler Fig is a better framing. If old and new remain permanently selectable for different policies, the final design may be Strategy/Bridge rather than a temporary branch.

Record forces and exit: affected callers, behavior/state, motivation, expected coexistence duration, evidence, switch mechanism, rollback horizon, obsolete dependencies and deletion criterion. Reject indefinite “maybe we need old forever.” Some formats require legacy readers long-term; isolate compatibility intentionally rather than retaining a global runtime toggle.

### Discover the actual dependency surface

Use import/call graphs, runtime traces, tests, configuration, reflection/plugin registration, build dependencies and operator scripts. Identify not only method calls but transaction, threading, cache, lifecycle, error, timing and resource assumptions. A filesystem replacement may depend on atomic rename/durability; an HTTP client replacement on cancellation/pooling/TLS; an ORM replacement on identity/transaction/lazy-loading semantics.

Write characterization tests for required behavior and adversarial edges. Separate contract from quirks/bugs. Approve corrections explicitly. Dependency architecture tests can forbid new direct imports and enumerate remaining bypasses until zero.

### Design at caller intent

Name operations by capability: `reserve`, `load_account`, `verify_credential`, not `executeSql` or the new SDK's types. Use domain/value DTOs owned near the abstraction. Define:

- preconditions/postconditions and identity/idempotency;
- errors and retryability;
- atomicity, consistency, ordering and concurrency;
- timeout/cancellation/backpressure;
- lifecycle, ownership and cleanup;
- performance/capacity bounds;
- authentication/authorization/data classification;
- metrics/tracing/audit behavior;
- version/state compatibility.

Keep interface narrow. When old/new differ, choose the business-needed common guarantee or expose an explicit capability query; do not pretend a stronger semantic exists. If callers truly need implementation-specific features, separate optional interfaces or delay those callers.

### Introduce the old adapter first

Create abstraction and implement it via legacy dependency. Migrate a small caller, then all callers, without changing authoritative behavior. Run existing, characterization and new shared contract tests. Compare telemetry/performance to baseline because wrappers can alter exceptions, cancellation, transactions or allocation.

Commit seam introduction separately from replacement logic. Enforce no direct legacy imports through package visibility/lint/architecture tests. If a bypass cannot migrate, document why and whether it blocks switch. Once all calls flow through the seam, the replacement branch point is owned centrally.

### Implement the replacement behind the same contract

Develop new implementation in small commits. Run one contract suite parameterized over old and new. Add implementation-specific tests only for internals/capabilities outside shared contract. Use generated/random/property cases where input space is large, plus recorded production-shaped fixtures and boundary failures.

Equivalence includes failures and nonfunctional semantics: cancellation must stop work, error classification drives retries, resource closure prevents leaks, transactions preserve invariants, security context and audit remain, latency/tail/capacity meet budgets. A new result that matches on happy paths but times out differently is not contract-equivalent.

For an approved behavior correction, version/record it and avoid forcing the old adapter to imitate a defect-free future unless needed. The abstraction can support a semantic version/mode during a bounded transition, but remove transitional modes when consumers move.

### Select in composition, not business logic

Prefer construction-time dependency injection: one `CredentialVerifier` instance chosen by configuration. Centralize policy, validation, safe defaults and telemetry. Do not scatter flag checks at every call; that doubles paths and makes cleanup difficult.

Selection can be build-time, deployment-wide, per process, deterministic cohort or per entity. Per-request random choice breaks state/cache/session continuity. Stateful implementation choice belongs at the state ownership key and may need stickiness. Invalid/unavailable configuration should fail closed or choose known safe owner; do not silently choose new.

Feature toggles are temporary operational controls. Record type (release/experiment/ops/permission), owner, creation, expiry, default, dependencies and removal issue. Test both states and configuration outage. Restrict change permissions/audit. Avoid combinatorial toggle interactions by migrating one bounded concern and pruning aggressively.

### Compare without duplicating effects

For pure/read operations, invoke both, normalize declared nondeterminism and compare semantic results/errors/performance. Keep one authoritative response. For writes/effects, do not blindly invoke twice. Options include:

- compare plans/intents before one execution;
- run new against a sandbox/isolated shadow store;
- replay sanitized recorded inputs offline;
- replicate authority into a derived test projection;
- use invariant/property comparison rather than duplicate calls.

Shadow must not charge, email, allocate, publish, mutate shared caches or consume one-time tokens. Differential logs minimize PII and have retention/access. Comparison load is bounded. A mismatch oracle independent of both implementations prevents shared-bug agreement.

### Migrate state and concurrency explicitly

Stateless library replacement is simplest. Stateful components need format/schema and ownership states. Introduce backward/forward-compatible representation, backfill under boundary, dual-read with comparison, or one authoritative write plus derived synchronization. Avoid uncoordinated dual writes. Fence old writers before new takes authority.

Rollback after new writes works only if old implementation can read/represent them or reverse synchronization is proven. Keep expand/migrate/contract fields until rollback horizon ends. For caches, cold fallback may be enough; for ledgers, state correctness dominates switch speed.

Concurrency semantics are part of contract. A replacement lock-free structure, client pool or transaction API must preserve linearization/order/cancellation needed by callers. Stress/model/concurrency tests complement functional equivalence. Shared parallel comparison itself can race and change behavior, so isolate resources.

### Switch progressively and observe

Start tests/dev, internal cohorts, low-risk deterministic canary, then expand. Gates cover semantic/security mismatches, errors/timeouts, p95/p99, saturation/leaks, business outcomes, state reconciliation and operator readiness. Record implementation identity/version in traces and metrics without exposing it as a permanent business concern.

Rollback policy differs by failure: flip composition for stateless compatible replacement; stop writes/reconcile for stateful; forward-fix after incompatible migration. Test actual rollback before promotion. Remove default dependence on remote flag service from hot paths; cache signed/validated configuration.

### Remove the branch

After full switch and horizon/soak:

1. verify all callers route to new and no bypass/import/runtime load occurs;
2. resolve state formats, archives and rollback obligations;
3. delete old implementation and old adapter;
4. delete toggle, selection branches, shadow comparison and migration-only telemetry/jobs;
5. remove old dependency, configuration, secrets, licenses and alerts;
6. simplify abstraction if it carried transitional compromises, while retaining a genuinely useful durable seam;
7. update ownership/docs/runbooks and verify clean build/dependency graph.

If abstraction exists only for migration and adds no design value, inline/remove it. Branch by Abstraction is complete when the branch converges, not when the toggle defaults to new.

### Deterministic contract comparison model

The executable model compares an old and replacement discount calculation over boundary cases, then centrally selects the replacement. Both use integer cents/basis points.

<!-- bijux-verify: {"id":"sepat-098-contract-comparison","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"cases=0:0=0,999:0=999,1000:500=950,2500:1200=2200\nequivalent=yes\nselected=new result=950\n","stderr":""}} -->
```python
def old_price(cents, discount_basis_points):
    discount = (cents * discount_basis_points) // 10000
    return cents - discount

class ReplacementPricing:
    def price(self, cents, discount_basis_points):
        kept_basis_points = 10000 - discount_basis_points
        return (cents * kept_basis_points + 9999) // 10000

replacement = ReplacementPricing()
cases = [(0, 0), (999, 0), (1000, 500), (2500, 1200)]
results = []
equivalent = True
for cents, rate in cases:
    old = old_price(cents, rate)
    new = replacement.price(cents, rate)
    equivalent = equivalent and old == new
    results.append(str(cents) + ":" + str(rate) + "=" + str(new))

selected = replacement
print("cases=" + ",".join(results))
print("equivalent=" + ("yes" if equivalent else "no"))
print("selected=new result=" + str(selected.price(1000, 500)))
```

The run proves equality for four integer cases only. It does not prove all-input equivalence, monetary policy, overflow across languages, configuration, concurrency, effects, performance, security, state migration or production switch safety.

## Definitions and Notation

Let (A) be contract consisting of observable operation semantics (Obs_A), legacy adapter (I_0), replacement (I_1), caller set (C=\{c_1,\ldots,c_m\}), and centralized selector (S(u,t)). `Migrated(c)` means caller depends only on (A), not concrete (I_0).

**Structural completion** requires (\forall c\in C:Migrated(c)) and no bypass. **Behavioral readiness** requires relevant (x\in X): (Obs_A(I_0,x)\equiv_C Obs_A(I_1,x)), plus nonfunctional/security budgets. This is tested evidence over a chosen domain, not proof for all possible inputs.

For stateful ownership (W_t(k)\in\{I_0,I_1\}), require one writer per key unless a single logical transaction protocol exists. **Rollback compatibility** means every state accepted by (I_1) during horizon can be correctly consumed/reversed into (I_0). **Convergence** requires selector fixed to (I_1), old path/dependency removed and temporary configuration state eliminated.

## Mechanisms, Invariants, or Proof Structure

1. **Frame replacement.** State motivation, surface, coexistence duration, risks, evidence, rollback and deletion endpoint.
2. **Discover dependencies.** Calls/imports/reflection/configuration plus transactions, resources, security and operator behavior.
3. **Define caller contract.** Stable intent, errors, consistency, concurrency, lifecycle, performance and policy.
4. **Wrap old behavior.** Implement old adapter; migrate callers without behavior change; prohibit bypasses.
5. **Build replacement.** Small mainline changes behind same contract; shared tests plus implementation tests.
6. **Prepare state/effects.** One authority, compatible formats, backfill/sync and effect-isolated comparison.
7. **Centralize selection.** Deterministic scoped composition/toggle with owner, safe default, expiry and audit.
8. **Compare/canary.** Semantic/error/security/performance evidence, representative/adversarial inputs and resource checks.
9. **Switch/soak.** Transfer authority, reconcile, meet gates and retain only honest rollback during horizon.
10. **Converge/delete.** Old adapter/implementation/dependency, toggle, shadow, bypasses, secrets and migration docs removed.

The technique reduces integration risk because seam introduction and semantic replacement are separately observable changes and both remain on mainline. This argument assumes the abstraction captures all dependency paths and the old adapter preserves behavior. Hidden bypasses or a leaky contract invalidate isolation. It is a risk-decomposition argument, not a proof of replacement equivalence.

## Alternatives and Trade-Offs

**Small atomic refactor** is preferable when replacement fits one reviewable commit and comprehensive tests; abstraction scaffolding would be waste.

**Source-control branch** isolates incomplete code but delays integration and accumulates merge/deployment risk. Short-lived branches can still deliver each Branch-by-Abstraction commit.

**Strategy/Bridge/plugin architecture** is durable multi-implementation design. Use when variants remain valuable; do not delete selection as migration debris.

**Strangler Fig** redirects externally visible capability/system traffic and transfers data/operations. Use when deployables/teams differ.

**Facade/Adapter only** can permanently isolate a vendor/API without a staged switch. Branch by Abstraction describes the temporal migration sequence.

**Fork/vendor patch** offers control but incurs long-term merge/security maintenance.

**Big-bang rewrite** may fit a tiny/frozen, easy-to-rollback component; it concentrates semantic and integration risk.

**Retain old** is rational when replacement value is lower than compatibility/state risk; encapsulate and monitor instead.

Choose by caller count, seam quality, replacement duration, state/effects, rollback needs and permanent value of the abstraction.

## Failure Modes and Misconceptions

- **“Any interface is Branch by Abstraction.”** The pattern is a convergent migration sequence with old/new coexistence.
- **“Copy old API.”** That fossilizes legacy quirks and constrains replacement.
- **“Design for new vendor.”** Caller-owned semantics disappear behind another leaky wrapper.
- **“One giant interface.”** Broad surface prevents independent migration/testing and violates segregation.
- **“Migrate callers and behavior together.”** Failures cannot distinguish seam from replacement.
- **“Mocks prove contract.”** Run the same suite against both real implementations.
- **“Happy output equality is enough.”** Errors, effects, cancellation, concurrency, performance and security matter.
- **“Call both writes and compare.”** External/state effects duplicate unless isolated.
- **“Flag anywhere.”** Centralize selection in composition and record lifecycle.
- **“Random per call canary.”** Stateful/resource/session behavior needs sticky scope.
- **“Toggle makes rollback.”** State/schema may not be backward-compatible.
- **“New default means done.”** Old imports/dependency/secrets/toggle/scaffolding remain.
- **“Abstraction must stay.”** Remove it if it has no durable design value after migration.
- **“Old format reader means old implementation.”** Retain narrow compatibility reader, not entire runtime, when history requires it.
- **“Mainline deployable means safe.”** Each state still needs tests, gates and operational evidence.

## Worked Examples

### Example 1

**Situation.** Fifty callers use a vendor storage SDK; team creates interface with methods named exactly after SDK operations.

**Reasoning.** Callers still depend on vendor batching/keys/errors. Define capability interfaces such as `DocumentStore.put/get_if_version`, with required atomicity/errors, then adapt vendor. Unsupported callers reveal real coupling.

**Conclusion.** Abstraction expresses caller intent and guarantees, not the replaced API surface.

### Example 2

**Situation.** Seam commit changes exceptions while supposedly delegating to old code.

**Reasoning.** Old adapter mapped timeout to generic unavailable, changing retry behavior. Shared characterization/error contract catches it. Fix mapping before any replacement work.

**Conclusion.** Old-adapter commit independently proves structural redirection preserves observable behavior.

### Example 3

**Situation.** Most callers migrated, but one reflection-based plugin instantiates legacy class.

**Reasoning.** Static import checks miss it; runtime construction telemetry/configuration inventory reveals bypass. Switch cannot complete until plugin uses factory/abstraction or is retired.

**Conclusion.** Dependency discovery needs static, configuration and runtime evidence.

### Example 4

**Situation.** New email provider runs in shadow and sends duplicate mail.

**Reasoning.** Comparing provider responses after sending is unsafe. Compare rendered message/effect intent, use provider sandbox/sink, or replay offline. Only authoritative implementation receives production send capability.

**Conclusion.** Dual execution must stop before irreversible effect boundary.

### Example 5

**Situation.** Flag is checked inside twelve pricing methods.

**Reasoning.** Mixed implementation within one calculation becomes possible and cleanup is scattered. Select one `PricingPolicy` at request/order scope in composition, then pass it through.

**Conclusion.** Centralized stable-scope selection prevents hybrid execution and simplifies removal.

### Example 6

**Situation.** New serializer writes version 3 records the old reader cannot parse; team advertises instant rollback.

**Reasoning.** Toggle reversal fails on v3 state. During rollback horizon dual-read/write a backward-compatible envelope or delay v3-only writes; otherwise declare forward recovery and preserve new reader.

**Conclusion.** Stateful rollback is a data compatibility proof, not a configuration action.

### Example 7

**Situation.** Contract tests pass but replacement has p99 latency 20× old and ignores cancellation.

**Reasoning.** Callers exhaust pools under timeout, causing outage. Add cancellation/resource/tail-load contract evidence and canary capacity gates before switch.

**Conclusion.** Nonfunctional behavior is part of substitutability in production.

### Example 8

**Situation.** After full switch, team retains old dependency “for safety.”

**Reasoning.** It preserves vulnerabilities, build size, secret/config paths and false rollback confidence. After horizon and restore evidence, delete old adapter/code/dependency and verify no runtime loads.

**Conclusion.** Dependency removal is completion evidence, not optional cleanup.

### Example 9

**Situation.** Two image encoders remain valuable for quality/cost policies after migration.

**Reasoning.** The abstraction/selection is now a deliberate Strategy. Remove migration toggle/shadow/old naming, define supported policies and own both implementations permanently.

**Conclusion.** Converge temporary mechanisms even when a durable multi-strategy design remains.

### Example 10

**Situation.** A hospital replaces a dose-calculation library and outputs disagree on rare renal cases.

**Reasoning.** Neither legacy parity nor new-library certification alone settles local safety. Use verified units/rounding/rule versions, adversarial clinical fixtures, effect-free shadow recommendations, audit and fail-safe fallback. Named human pharmacists, clinical-safety engineers, privacy/security and regulatory reviewers classify every high-risk mismatch before canary.

**Conclusion.** High-stakes abstraction replacement requires domain-governed semantics and named human review beyond automated equivalence.

## Cross-Program Connections

- **Object-Oriented Design:** dependency inversion, interface segregation, substitutability and adapters define the seam.
- **Software Evolution:** characterization tests, mainline integration and small commits decompose change risk.
- **Architecture:** internal abstraction versus externally routed strangling determines boundary and deployment topology.
- **Distributed Systems:** state synchronization, fencing, idempotency and rollback compatibility arise for stateful replacements.
- **Security Engineering:** provider substitution must preserve auth, secret handling, audit, timing and data classification.
- **Testing and Quality:** shared contract, differential, property, concurrency and performance tests establish substitution evidence.
- **Reliability Engineering:** canary, cancellation, resource saturation, telemetry and rollback gates protect operation.
- **Delivery Engineering:** toggle lifecycle, configuration rollout and dependency removal keep mainline deployable and convergent.

## References

- Martin Fowler, [Branch by Abstraction](https://martinfowler.com/bliki/BranchByAbstraction.html), 2014, retrieved 2026-08-29. Defines gradual mainline replacement through an abstraction layer.
- Paul Hammant, [Branch by Abstraction](https://www.branchbyabstraction.com/), retrieved 2026-08-29. Early detailed sequence and examples of the technique.
- Pete Hodgson, [Feature Toggles](https://martinfowler.com/articles/feature-toggles.html), 2017, retrieved 2026-08-29. Current durable taxonomy and practices for toggle decisions, routing and lifecycle.
- Jez Humble and David Farley, *Continuous Delivery*, Addison-Wesley, 2010. Mainline, deployment pipeline and incremental release foundations.
- Michael Feathers, *Working Effectively with Legacy Code*, Prentice Hall, 2004. Seams, characterization tests and dependency-breaking techniques.
- Erich Gamma et al., *Design Patterns*, Addison-Wesley, 1994. Adapter, Bridge and Strategy structures used by the migration technique.
- Barbara Liskov and Jeannette Wing, [A Behavioral Notion of Subtyping](https://dl.acm.org/doi/10.1145/197320.197383), ACM TOPLAS 1994. Formal foundation for behavioral substitutability beyond matching method signatures.
- Trisha Gee and Martin Fowler, [Parallel Change](https://martinfowler.com/bliki/ParallelChange.html), retrieved 2026-08-29. Expand–migrate–contract approach for compatible interface evolution adjacent to Branch by Abstraction.

## Exercises

### Exercise 1

Define seam, caller-owned abstraction, old adapter, centralized selection, shadow comparison and convergence. Distinguish the pattern from Strategy and Strangler Fig.

### Exercise 2

Plan commit boundaries for replacing a JSON serializer used by 80 callers while preserving old stored records and rollback.

### Exercise 3

Diagnose a migration whose shared tests use mocks, flag checks are scattered, both backends write, and old dependency remains after the new default.

### Exercise 4

Compare atomic refactor, Branch by Abstraction, permanent Strategy, vendor fork and Strangler Fig for replacing an embedded search library that may become a remote service later.

### Exercise 5

Design Branch by Abstraction for an unfamiliar cryptographic signing provider in a regulated financial system. Include semantics, key/state ownership, comparison, canary, rollback and retirement evidence.

## Answers to the Exercises

### Answer 1

A seam enables substitution. Caller-owned abstraction states stable needed capability/semantics. Old adapter delegates the abstraction to current implementation so structural migration is behavior-preserving. Central selection chooses one implementation at composition/stable cohort scope. Shadow comparison runs both with only one authoritative effect and compares normalized semantics. Convergence removes old implementation, bypasses, toggle and migration scaffolding. Strategy intentionally retains multiple implementations/policies; Branch by Abstraction is a temporary replacement sequence. Strangler Fig routes/moves externally bounded capabilities/data/operations between systems; Branch by Abstraction usually changes an internal dependency in one deployable.

### Answer 2

First inventory callers, reflection/configuration and stored-format versions; freeze contract fixtures for parsing/serialization/errors/canonicalization/resources. Commit a caller-owned `DocumentCodec` plus old adapter and tests. Migrate callers in small coherent commits and add architecture checks forbidding direct imports. Implement new codec behind interface with shared real-implementation, property/fuzz/cross-version fixtures. Add a versioned envelope and make new reader understand old; keep writer on old version initially. Add centralized selection/shadow for encode-decode comparison without mutating authority. Canary readers, then compatible writers; record rollback horizon and prevent new-only format until old rollback ends. Switch default after evidence, monitor stored-version inventory, remove old writer, and retain only a narrow old reader if retention requires. Finally remove toggle, old adapter/library, bypass checks specific to migration and stale config/docs; each commit remains buildable and verified.

### Answer 3

Mocks prove only the invented mock contract; parameterize suites over both real backends, including errors, cancellation, concurrency, security and resources. Move scattered flag checks into one factory/composition selection and choose at stable state key. Dual writes are split authority; select one authoritative writer and propagate/migrate durably, or use an explicit atomic protocol. New default is not convergence: inventory runtime imports/config/secrets/state compatibility, observe soak/rollback horizon, then delete old adapter/code/dependency and toggle. Reconcile any divergent state before further canary. Add effect isolation, deterministic cohort, architecture-import tests and dependency/build scan.

### Answer 4

Use atomic refactor if the embedded library is already isolated and replacement is small. Use Branch by Abstraction when many callers bind to its API: introduce domain search interface/old adapter, add replacement and switch incrementally. If two engines permanently serve different cost/quality workloads, converge into an intentional Strategy with supported policies. Fork only when short-term critical patches outweigh perpetual upstream/security merge burden. If replacement becomes an independently deployed remote search capability with separate data/index/operations, the later boundary may use Strangler Fig; design the abstraction around search semantics, not local/remote transport, so that transition is possible. Do not prematurely introduce a service solely because it might happen.

### Answer 5

Define `Signer.sign(key_ref, algorithm_profile, canonical_digest, request_id)` and `verify` with exact supported algorithms/parameters, canonical bytes, error taxonomy, latency, audit, authorization and non-exportable-key semantics. Old adapter preserves current HSM/provider behavior. Migrate all callers and prohibit direct SDK/key access. Replacement uses separate approved keys or a provider abstraction compatible with key custody; never send production signing twice. Compare verification results and signature validity via sandbox/test keys and independent standard vectors, including malformed inputs, rotation, outage, cancellation and rate limits.

Central selection is per key/tenant/profile with signed audited policy and safe default; canary low-risk keys only after capacity/security evidence. Key generation/import/rotation and audit records have one authority. Rollback requires old provider/key access and algorithm/state compatibility; once keys become new-provider non-exportable, route rollback may be impossible, so use forward recovery or dual-controlled migration before transfer. Named human cryptography, security, compliance and payments-domain reviewers approve algorithms, custody, mismatch handling and horizon. Retire by proving no calls/keys/audit dependencies require old provider, completing regulatory retention, revoking credentials/network, destroying keys under dual control, removing SDK/toggle/adapter and updating incident/DR evidence. Automated signature equality alone cannot validate governance or legal adequacy.
