---
module_id: SEPAT-030
program: Software Engineering: Patterns
level: 1
module_number: 30
title: Combining Structural Patterns Without Indirection Explosion
status: complete
last_verified: 2026-08-28
---

# Combining Structural Patterns Without Indirection Explosion

## One-Page Review

### Governing question

How can Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy, package facades, and ports/adapters be combined so each boundary owns a distinct decision while end-to-end call paths, effects, latency, identity, failure, and change remain understandable?

### Essential definitions

- **structural composition** combines patterns whose responsibilities and contracts remain independently identifiable.
- **indirection depth** is the number of runtime delegation or translation boundaries on a representative path.
- **static dependency depth** is the longest relevant import/build dependency path; it can differ from runtime depth.
- **semantic compression** is the amount of complexity a boundary hides behind a smaller coherent contract.
- A **pass-through layer** delegates without owning a stable decision, translation, policy, or invariant.
- **multiplicity** is the number of inner invocations caused by one outer call; retries and fan-out may multiply.
- A **responsibility ledger** records each boundary's owner, input/output contract, effect, order, failure, and reason to exist.
- **architecture contraction** removes, merges, or replaces boundaries after their decision or variability disappears.
- A **fitness function** is an objective check that protects a chosen architectural property.
- **indirection explosion** occurs when layers, wrappers, interfaces, mappings, and factories grow faster than the independent decisions they isolate.

### Central model, mechanism, or theorem

Model a realized path as directed graph (G=(V,E)). Each node (v) has responsibility (r(v)), owner (o(v)), cost (c(v)), and possible invocation multiplier (m(v)\ge0). For a path (p=(v_1,\ldots,v_d)), maximum subject attempts are

\[
A(p)=\prod_{i=1}^{d}m(v_i),
\]

and additive latency estimate is (L(p)=\sum_i c(v_i)) only when execution is sequential and costs are suitably defined. Depth alone is not a quality theorem. A boundary is justified when it protects a durable independent decision or provides measured semantic compression exceeding its cognitive, runtime, failure, and change cost.

### Critical invariants

- Every boundary has one named durable responsibility and owner; no two layers unknowingly own the same effect.
- Runtime order, source dependency direction, construction graph, and deployment path are documented separately.
- Authorization, retry, transaction, caching, identity, deadline, cancellation, and close have explicit single authorities.
- Translations preserve required information and do not silently strengthen guarantees.
- Multiplicity, fan-out, queueing, buffering, and tail-latency budgets are bounded end to end.
- Production composition is inspectable and tested, including framework/platform-added layers.
- Architecture checks target actual properties rather than arbitrary universal depth limits.
- Obsolete pass-through boundaries are contracted with compatibility and rollout evidence.

### Common failures

Common failures include naming every wrapper a pattern, adding interface/adapter/facade pairs one-for-one, hiding service location behind factories, stacking client and platform retries, placing cache before authorization, nesting transactions across retry incorrectly, losing deadlines through adapters, mapping errors at every layer until causes vanish, reflecting/unwrapping around policy, creating cycles between package facades and ports, tracing every wrapper as one logical operation, measuring average rather than tail cost, and refusing to remove layers because the original reason is forgotten.

### Compact example

A realized request path is `audit → authorize → cache → retry(3) → transport`. A validator confirms unique IDs, `authorize` before `cache`, one retry owner, and transport last. Depth is five and maximum transport attempts are three. Adding a second retry is rejected before startup.

### Connections

[SEPAT-021](021-adapter.md) through [SEPAT-029](029-ports-and-adapters-as-a-structural-pattern.md) provide the structural tools being composed. [SEPAT-031](../ROADMAP.md) introduces behavioral request chains. This synthesis connects to [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md), [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md), and [Performance Engineering topics in Systems Engineering](../../26-systems-engineering/ROADMAP.md).

## Governing Question

For every extra boundary on an important path, what independent change or invariant does it protect, what observations does it alter, and how will the team know when its benefit no longer exceeds its cost?

Patterns are a vocabulary for forces and consequences, not collectible artifacts. Combining them well requires an explicit model of the realized system rather than class names or a diagram of intended layers.

## Why This Matters

Production paths commonly combine a package facade, driving adapter, application facade, ports, provider adapter, proxy, cache, decorators, and remote gateway. Each can be locally reasonable while the whole becomes slow, opaque, cyclic, or semantically contradictory.

Conversely, flattening every boundary couples volatile decisions and spreads policy. The objective is not minimum layers; it is minimum accidental complexity for the required independent decisions.

## Prerequisites and Retrieval

You should understand all structural patterns, dependency graphs, retries, transactions, caching, authorization, observability, performance measurement, and refactoring. Retrieve these facts:

1. Runtime call direction, source dependency direction, and deployment topology are different graphs.
2. Sequential retry layers multiply attempts rather than add them.
3. Wrapper order changes security, consistency, metrics, and failure.
4. A short interface can hide great complexity; file or method count alone does not measure value.
5. Frameworks, clients, meshes, and gateways may add behavior absent from application source.
6. Refactoring requires behavior-preserving evidence for the observations that matter.

## Learning Objectives

After completing this module, you should be able to:

- build runtime, dependency, construction, and deployment views of one path;
- assign each structural boundary a distinct responsibility and owner;
- calculate call multiplicity and reason about latency/failure composition;
- validate security, retry, transaction, cache, context, and lifecycle order;
- distinguish deep useful modules from pass-through layers;
- create architecture fitness functions tied to actual risks;
- contract obsolete indirection incrementally and safely;
- review high-stakes compositions without overstating evidence.

## Core Exposition

### Start from the realized path

Trace a representative request from entry to effect and back, including generated clients, framework filters, dependency-injection interceptors, service mesh, gateway, database driver, and callbacks. Record short circuits and fan-out.

Draw separate views for source imports, runtime calls, object construction/lifetime, deployment/network hops, and data ownership. Collapsing them into one arrows diagram conceals important contradictions.

### Give every boundary a responsibility ledger

For each node record stable ID/version, pattern role, durable responsibility, owner, contract, before/after behavior, short circuit, multiplicity, context, errors, lifecycle, cost, and evidence. If two nodes both claim retry or transaction authority, resolve the conflict.

If nobody can state the decision a layer owns, it is a candidate for contraction—not automatically safe to delete, because consumers may rely on accidental behavior.

### Compose by semantics, not pattern names

A package facade may expose a driving port; an HTTP adapter translates into it; a use-case facade coordinates driven ports; a provider adapter uses a protection/cache proxy; decorators observe the boundary. This is coherent if responsibilities and directions remain distinct.

Do not add a GoF class structure merely to label a design. Language functions, modules, data types, or platform controls can implement the same responsibility more directly.

### Validate order constraints

Model `before`, `after`, `requires`, `conflicts`, and multiplicity. Authorization generally precedes protected cache disclosure. One logical metric normally sits outside retry while attempt telemetry sits inside. Per-attempt transactions belong inside a safe retry coordinator; one operation idempotency identity surrounds attempts.

Topological order is insufficient when multiple legal orders have different semantics. Reject material ambiguity unless policy declares a canonical choice.

### Calculate invocation amplification

If client retry permits two attempts and a sidecar permits three, the subject may see six attempts. Fan-out to four replicas can yield 24 downstream operations. Cache short circuits may reduce average calls but not miss-path worst case.

Compute bounds for each outcome class and enforce them in configuration and tests. Do not rely on averages for overload or duplicate-effect risk.

### Budget end-to-end latency and resources

Use one absolute deadline. Allocate remaining budget across sequential steps and reserve cleanup/reconciliation time. Bound queue, concurrency, buffer, payload, retries, cache keys, and telemetry cardinality.

Latency is not always additive: parallel fan-out uses maxima plus coordination, queues are load-dependent, and retries condition on failure. Measure representative p95/p99/p99.9 and saturation behavior.

### Preserve information through translation

Every Adapter/Facade/Proxy may map types and errors. Repeated mapping can reduce a precise conflict or indeterminate outcome to generic failure. Define a stable outcome algebra once at each true trust/domain boundary and retain causal evidence internally.

Avoid converting identifiers, currency, units, timestamps, or Unicode forms repeatedly. Each conversion needs one owner and tested round-trip/loss contract.

### Align identity and lifecycle

Bridge implementors, proxies, decorators, pooled/flyweight objects, and adapters can each introduce object identities and close behavior. Define stable resource identity separately from wrapper identity and one owner for subject disposal.

Shared inners and asynchronous callbacks require explicit reference/lifetime rules. Unwrapping may violate protection or observability and is not a harmless debugging aid.

### Make architecture observable without duplicating telemetry

Expose a redacted realized-chain description and stable composition digest. Trace logical operations and physical attempts at different levels; avoid one span per trivial in-process delegation unless diagnostic value justifies it.

Record bounded layer/error IDs, queue wait, cache outcome, attempt number, and deadline budget. Never dump secrets, payloads, or unbounded dynamic graph labels.

### Protect intent with fitness functions

Examples include forbidden dependency cycles, one retry authority, authorization-before-cache, maximum reviewed runtime depth for a critical path, no provider types in ports, deterministic chain order, bounded import time, and p99 budgets.

Thresholds are system-specific and reviewed. A universal “no more than five layers” rule can reject deep useful modules and accept five meaningless ones.

### Contract safely

Candidates include one-to-one pass-through wrappers, adapters with identical contracts after vendor removal, facades serving one caller with no compression, duplicate policy layers, and factories with one permanent implementation.

Characterize behavior, map consumers, remove one boundary at a time, preserve stable paths where needed, compare shadow outcomes, progressively roll out, and retain rollback. Update diagrams, telemetry, ownership, and fitness functions in the same intent.

## Definitions and Notation

Let graphs be (G_s) for source dependencies, (G_r) for runtime calls, (G_c) for construction/lifecycle, and (G_d) for deployment hops. Acyclicity in (G_s) does not imply no runtime callback cycle in (G_r).

For path (p), define depth (d(p)), cost observations (c_i), multipliers (m_i), and fan-out (f_i). Worst-case leaf operations are bounded by

\[
W(p)\le\prod_i m_i f_i
\]

when bounds are independent and finite. Actual distributions require measurement and correlation analysis.

Let benefit ledger (B(v)) include volatility isolation, semantic compression, enforcement, and test control; cost ledger (C(v)) include cognitive navigation, runtime overhead, failure states, compatibility, and ownership coordination. (B>C) is a decision framework, not a dimensionally exact universal formula.

## Mechanisms, Invariants, or Proof Structure

### Composition review

1. Select critical successful and failing paths.
2. Extract all four graphs from code/config/deployment evidence.
3. Build a responsibility ledger for every boundary.
4. Validate order, conflicts, multiplicity, context, errors, and lifecycle.
5. Calculate worst-case calls/resources and measure distributions.
6. Inspect production composition and telemetry.
7. Encode the most important properties as fitness functions.
8. Contract unjustified boundaries incrementally with compatibility evidence.

### Executable mechanism

This simple configuration validator demonstrates order, uniqueness, one retry authority, terminal transport, depth, and attempt bounds. It is not a general architecture-analysis engine.

<!-- bijux-verify: {"id":"structural-chain-validator","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"valid=True depth=5 max-attempts=3\nduplicate=False reason=duplicate:retry\n","stderr":""}} -->
```python
def validate_chain(chain, retry_limit):
    seen = set()
    for layer in chain:
        if layer in seen:
            return (False, "duplicate:" + layer, 0)
        seen.add(layer)
    if "authorize" not in seen or "cache" not in seen:
        return (False, "missing-security-order", 0)
    if chain.index("authorize") > chain.index("cache"):
        return (False, "authorize-after-cache", 0)
    if chain[-1] != "transport":
        return (False, "transport-not-terminal", 0)
    attempts = retry_limit if "retry" in seen else 1
    return (True, "ok", attempts)


production = ["audit", "authorize", "cache", "retry", "transport"]
valid, reason, attempts = validate_chain(production, 3)
print("valid=" + str(valid) + " depth=" + str(len(production)) + " max-attempts=" + str(attempts))

duplicate_retry = ["authorize", "cache", "retry", "retry", "transport"]
valid, reason, attempts = validate_chain(duplicate_retry, 3)
print("duplicate=" + str(valid) + " reason=" + reason)
```

A production validator needs stable descriptors, partial-order constraints, capability requirements, lifecycle ownership, canonical configuration digests, framework/platform discovery, and configuration provenance.

### Proof obligations

Prove only graph properties for the complete graph source used. Prove multiplicity bounds from every retry/fan-out/short-circuit policy and their composition. Performance remains empirical, and “justified abstraction” requires human/domain judgment supported by evidence.

The snippet proves two finite list evaluations. It does not prove the deployed chain matches configuration or that its policies are correct.

## Alternatives and Trade-Offs

| Strategy | Benefit | Risk |
|---|---|---|
| Explicit composition graph | inspectable order/ownership | descriptor maintenance |
| Framework middleware/interceptors | standard integration | hidden auto-added layers |
| Compile-time/static wiring | early validation and speed | less runtime variability |
| Dynamic plugin composition | extensibility | ambiguity, trust, lifecycle |
| Platform-native controls | shared operational ownership | remote/common-mode semantics |
| Inlined/direct implementation | minimal depth | greater coupling/duplication |
| Coarse deep module | semantic compression | internal complexity concentration |

The correct mix depends on variability, trust, performance, and ownership—not fashion or a fixed pattern count.

## Failure Modes and Misconceptions

### “More patterns mean better architecture”

Patterns describe recurring trade-offs. Unneeded instances add complexity without isolating a real decision.

### “Depth is always bad”

A deep module can hide substantial complexity behind a small contract. Pass-through depth with no semantic compression is the stronger smell.

### “The diagram is the system”

Generated proxies, framework filters, service meshes, and alternate bypasses can change the realized path. Inspect deployment and runtime evidence.

### “Each layer can own its own retry and timeout”

Retries multiply and timeout resets exceed the user deadline. Use one operation policy and remaining budgets.

### “Generic errors reduce coupling”

They can destroy recovery knowledge. Stable error algebras should abstract implementation without erasing meaning.

### “Refactoring out a wrapper is risk-free”

Clients may observe timing, errors, identity, serialization, metrics, or undocumented behavior. Characterize and migrate.

### “Architecture metrics are universal laws”

Depth, coupling, and symbol counts are signals. Thresholds need context, trend, and explicit quality goals.

## Worked Examples

### Example 1

An API adapter calls an application facade through a driving port; the facade coordinates two driven ports. Each boundary owns protocol, use-case, or external-capability semantics. **Conclusion:** Several layers can be coherent when decisions differ.

### Example 2

Controller, facade, service, manager, coordinator, and handler all forward the same DTO to one repository. Characterization permits collapsing five. **Conclusion:** Renamed pass-through layers are indirection explosion.

### Example 3

Client retry 2 × mesh retry 3 × replica fan-out 4 gives an upper bound of 24 leaf calls. One retry owner and quorum-aware fan-out reduce the bound. **Conclusion:** Multiplicity must be calculated end to end.

### Example 4

A cache proxy precedes authorization and leaks a tenant result. Reordering authorization before cache plus tenant/policy/data generations repairs the contract. **Conclusion:** Structural order can be a security invariant.

### Example 5

Retry wraps one transaction, so a failed transaction is reused. Moving a fresh per-attempt transaction inside safe retry aligns lifecycle. **Conclusion:** Retry and transaction scopes compose nontrivially.

### Example 6

Four adapters translate one error until `indeterminate payment` becomes `bad request`. One owned boundary algebra preserves uncertainty and cause. **Conclusion:** Repeated abstraction can destroy essential information.

### Example 7

Source dependencies are acyclic, but runtime callbacks form proxy → adapter → plugin → proxy recursion. Runtime graph tests and reentrancy guards expose it. **Conclusion:** One graph cannot prove whole-system structure.

### Example 8

A global trace creates eight identical logical spans for wrappers. One logical span plus nested attempt/remote spans reduces noise and cost. **Conclusion:** Observability should reflect semantics, not class count.

### Example 9

A facade/adapter pair once isolated two vendors; only one owned provider remains and contracts now match. Consumer tests support merging while retaining the public path. **Conclusion:** Architecture should contract after variability disappears.

### Example 10

A railway command path adds proxies, adapters, retries, audit decorators, and remote gateways. Review rejects automatic retry of indeterminate actuation and retains independent interlocks. **Conclusion:** Structural composition cannot substitute for system safety engineering.

## Cross-Program Connections

- **Programming Languages and Semantics:** effects, types, modules, dispatch, and reflection determine boundary cost.
- **Object-Oriented Programming:** delegation, identity, substitutability, and ownership recur across the graph.
- **Concurrent Programming:** cancellation, reentrancy, synchronization, queues, and lifecycle span layers.
- **Software Methods and Evolution:** characterization, incremental refactoring, compatibility, and ownership enable contraction.
- **Software Architecture:** graph views, modularity, deployment topology, and fitness functions preserve intent.
- **Testing and Quality:** architecture tests, contract tests, fault injection, and production-chain tests provide evidence.
- **Delivery and Reliability:** configuration provenance, progressive rollout, rollback, saturation, and observability govern changes.
- **Security Engineering:** complete mediation, trusted context, tenant isolation, and redaction depend on order.
- **Distributed Systems:** retries, partial failure, fan-out, deadlines, and indeterminate outcomes dominate amplification.
- **Systems Engineering:** hazard controls, physical effects, common-mode failures, and human authority bound abstraction.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Provides the structural-pattern catalog and pattern-composition vocabulary.
2. David L. Parnas, [“On the Criteria To Be Used in Decomposing Systems into Modules”](https://dl.acm.org/doi/10.1145/361598.361623), *Communications of the ACM* 15(12), 1972. Grounds boundaries in hidden changeable design decisions.
3. John Ousterhout, *A Philosophy of Software Design*, second edition, Yaknyam Press, 2021, ISBN 978-1-7321022-1-7. Develops deep modules, complexity, information leakage, and tactical-versus-strategic design.
4. Vlad Khononov, [*Balancing Coupling in Software Design*](https://www.informit.com/store/balancing-coupling-in-software-design-universal-design-9780137353484), Addison-Wesley, 2024. Provides a modern framework for coupling, modular knowledge boundaries, and trade-offs.
5. Neal Ford, Rebecca Parsons, Patrick Kua, and Pramod Sadalage, [*Building Evolutionary Architectures*, second edition](https://www.oreilly.com/library/view/building-evolutionary-architectures/9781492097532/), O'Reilly, 2022. Provides architecture fitness functions and guided incremental change.
6. Martin Fowler, [*Refactoring: Improving the Design of Existing Code*, second edition](https://www.pearson.com/en-us/subject-catalog/p/refactoring-improving-the-design-of-existing-code/P200000000254/9780134757599), Addison-Wesley, 2018. Provides behavior-preserving incremental design change and refactoring discipline.
7. Michael Nygard, *Release It!*, second edition, Pragmatic Bookshelf, 2018, ISBN 978-1-68050-239-8. Provides stability-pattern interactions, timeouts, retries, bulkheads, and production failure reasoning.

## Exercises

### Exercise 1

Trace the executable validator, derive the maximum attempts, and list important properties it cannot validate.

### Exercise 2

Build responsibility and order ledgers for a path containing package facade, HTTP adapter, application facade, authorization, cache, retry, transaction, provider adapter, and remote proxy.

### Exercise 3

Given client retry 2, gateway retry 2, fan-out 3, and per-leaf fallback 2, calculate the bound and design a safer composition.

### Exercise 4

Plan contraction of a six-layer pass-through service path with public compatibility, telemetry, rollout, and rollback constraints.

### Exercise 5

Review a deeply layered safety-critical command path in an unfamiliar domain without claiming correctness or deployment suitability.

## Answers to the Exercises

### Answer 1

The production list contains five unique names, authorization index 1 precedes cache index 2, and transport is last. One retry with limit three yields three maximum transport attempts. The duplicate list encounters the second retry and returns `duplicate:retry` before computing attempts.

It cannot establish that configured classes match names, authorization is correct/current, cache keys/invalidation are safe, retries are idempotent, deadlines/cancellation propagate, transport is the only effect, framework/platform layers are absent, lifecycle is sound, errors preserve meaning, or latency/resources fit budgets. A real validator needs typed descriptors, provenance, constraints, deployment discovery, and behavioral tests.

### Answer 2

The package facade owns stable public names/types; HTTP adapter owns protocol/authentication translation; application facade owns one use-case workflow; authorization owns current access decision; cache owns freshness/storage and comes after authorization for protected disclosure; retry owns bounded safe attempts and one idempotency identity; per-attempt transaction sits inside retry; provider adapter owns provider translation; remote proxy owns serialization/transport/deadline/error knowledge.

Record for each stable ID/version, owner, before/after/short-circuit behavior, input/output/error contract, context, multiplier, lifecycle, cost, and tests. Outer-to-inner may be HTTP/authentication → application/audit → authorization → cache → logical metrics → retry → per-attempt transaction → attempt trace → provider adapter → remote transport, subject to the actual domain. Pass one deadline and cancellation, reject duplicate retry/transaction authorities, keep tenant/policy/data generations in cache semantics, and expose indeterminate remote effects. Inspect generated client, framework, gateway, and mesh additions.

### Answer 3

The independent finite upper bound is (2\times2\times3\times2=24) leaf operations per logical request. Correlation and short circuits change observed distribution but do not make the configured worst-case safe. If effects are non-idempotent, even two can be unacceptable.

Choose one retry authority with operation knowledge, typically the client/application or one controlled gateway—not both. Bind a payload-scoped idempotency key and one deadline. Make fan-out semantics explicit: use only required replicas/quorum, cancel losing safe reads, and never duplicate writes casually. Treat fallback as selection, not another retry tree, with its own remaining budget. Enforce attempt/fan-out bounds in config, expose logical versus attempt metrics, fault-inject each failure point, and load-test saturation/tails.

### Answer 4

Inventory consumers and characterize values, errors, ordering, side effects, timing, identity, serialization, reflection, telemetry, and extension hooks at the public boundary. Build runtime/source/construction/deployment graphs and identify which layers own no distinct decision. Preserve the canonical public entry while redirecting it internally to the target implementation.

Remove one pass-through at a time in reviewable commits. Add contract and differential/shadow tests, architecture checks preventing reintroduction, and metrics comparing outcome/latency/error/cardinality. Roll out by cohort/canary with rollback to old composition; keep temporary adapters only with named removal criteria. Update ownership/docs/telemetry and remove dead dependency/configuration code. Do not combine layers that actually separate trust, transaction, compatibility, or independently changing ownership.

### Answer 5

Extract every realized layer including platform and device firmware, then assign authority for identity, authorization, validation, sequencing, deadlines, retry, transaction, command acceptance, confirmation, audit, cancellation, and safe state. Reject duplicate/reset authority and any automatic retry of indeterminate physical actuation without a validated authenticated idempotency/sequence and reconciliation protocol. Preserve independent interlocks and fail-safe controls outside the software wrapper chain.

Evidence requires traceable requirements/hazard and common-cause analysis, graph/order/multiplicity review, formal/state/timing analysis where tractable, dimensional and boundary recomputation, static analysis, independent code/protocol review, simulator/digital-twin and hardware-in-the-loop tests, loss/duplicate/reorder/delay/partition/restart/power/resource faults, security threat testing, operator/human-factors exercises, and controlled deployment/recovery. Named domain, controls/real-time, functional-safety, hardware, cybersecurity, human-factors, quality, regulatory, operations, reliability, and independent verification authorities approve. Pattern composition and passing software tests establish no system safety or deployment suitability.
