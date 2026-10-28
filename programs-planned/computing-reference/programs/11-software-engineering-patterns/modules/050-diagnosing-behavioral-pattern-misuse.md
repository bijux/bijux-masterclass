---
module_id: SEPAT-050
program: Software Engineering: Patterns
level: 1
module_number: 50
title: Diagnosing Behavioral Pattern Misuse
status: complete
last_verified: 2026-08-28
---

# Diagnosing Behavioral Pattern Misuse

## One-Page Review

### Governing question

How can engineers determine whether a behavioral pattern still resolves a real recurring design pressure or has become accidental complexity, then simplify or replace it with evidence while preserving behavior, ownership, compatibility, effects, and operational safety?

### Essential definitions

- A **pattern** is a named recurring context-problem-forces-solution-consequences relationship, not a code template.
- **pattern misuse** is a pattern-shaped structure whose assumptions do not match the current problem or whose liabilities exceed its demonstrated benefit.
- **accidental complexity** arises from the chosen representation/tooling rather than the essential domain problem.
- A **change axis** is a dimension that evolves independently: algorithms, states, operations, variants, policies, effects, or deployments.
- A **behavioral seam** is a controlled substitution point used by real variation, testing, isolation, or compatibility.
- **indirection tax** is the navigation, allocation, lifecycle, dispatch, configuration, and diagnostic cost introduced by a seam.
- A **pattern collapse** removes an unused abstraction while preserving required behavior.
- A **migration invariant** is a property/observable that must hold while changing the structure.
- A **transitional abstraction** exists only to support migration/compatibility and has an explicit removal condition.

### Central model, mechanism, or theorem

For design (d), observed workload/change history (H), required invariants (I), and evidence measures, compare benefit and cost vectors rather than counting pattern names:

\[
V(d\mid H,I)=B_{variation}+B_{ownership}+B_{test}+B_{compat}
-C_{navigation}-C_{state}-C_{lifecycle}-C_{runtime}-C_{operations}.
\]

This is a decision framework, not a universal numerical metric. Misuse is supported when the assumed benefit is absent or cheaper alternatives preserve (I) under representative evidence. Low class count, high coverage, or one benchmark alone cannot prove the diagnosis.

### Critical invariants

- Diagnosis begins with a reproduced maintenance/runtime/test/operational symptom and an explicit pattern assumption—not aesthetic dislike.
- Runtime control, state, data, effect, ownership, and failure paths are traced end to end before restructuring.
- Repository history and likely future change distinguish independent variation from speculative flexibility.
- Simplification candidates state preserved outputs, errors, effects, order, transactions, performance, compatibility, and security properties.
- Language/framework-native mechanisms are assessed using their actual semantics and support horizon.
- Migration proceeds in reversible observable steps with differential/characterization evidence and no duplicate effects.
- Transitional adapters, flags, and dual paths have owners, telemetry, deadlines/removal criteria, and cannot become permanent ambiguity.
- A successful refactoring establishes scoped preservation/improvement, not universal architectural or domain correctness.

### Common failures

Common failures include “patterns are always good,” “patterns are always overengineering,” counting classes as complexity, replacing polymorphism with one giant switch, replacing explicit control flow with reflection/configuration, deleting seams used by compatibility/tests, using speculative future variants to justify current cost, treating coverage as preservation proof, microbenchmarking away observability/security, rewriting without behavioral inventory, running old/new effectful paths simultaneously, leaving adapters forever, renaming a god object `Mediator`, and declaring success because diagrams contain fewer boxes.

### Compact example

A small deterministic triage heuristic classifies three evidence records: a single-variant wrapper stack suggests collapsing indirection; a listener design with lifecycle hazards requires repairing ownership first; a Strategy with several independently changing algorithms retains its seam. The heuristic only organizes investigation.

### Connections

[SEPAT-049](049-object-mother-and-test-data-builder.md) reduces fixture construction noise; [SEPAT-051](../ROADMAP.md) begins enterprise application patterns with Transaction Script. Misuse diagnosis connects to [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md), [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md), and [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md).

## Governing Question

What concrete force originally justified the abstraction, does current evidence still show that force, which liabilities are causing harm, and what smaller or differently owned design can preserve required behavior with a safer migration?

Patterns are hypotheses about where change and responsibility belong. Diagnosis tests those hypotheses against code, runtime traces, incidents, review experience, and history rather than judging vocabulary in isolation.

## Why This Matters

Behavioral patterns distribute control across objects. This can isolate variation beautifully, but it also hides call order, mutable state, effects, lifecycle, and failure paths. As requirements and languages evolve, yesterday's useful seam can become today's maze.

Unprincipled removal is equally dangerous. A seemingly redundant Strategy may be a compatibility boundary; a callback may carry shutdown rules; a State object may enforce transitions. Evidence-driven simplification protects hard-won semantics.

## Prerequisites and Retrieval

You should understand the preceding behavioral patterns, refactoring, version control, runtime tracing/profiling, characterization tests, contracts, concurrency, transactions, and deployment. Retrieve these facts:

1. Pattern applicability includes context and forces; matching structure alone is insufficient.
2. A code smell is a prompt to investigate, not a proof of defect or prescribed refactoring.
3. Repository history is incomplete evidence of future change but stronger than imagined variation alone.
4. Equivalent return values do not imply equivalent effects, errors, order, performance, or disclosure.
5. Native language features can eliminate ceremony while introducing different exhaustiveness, ambiguity, or compatibility trade-offs.
6. Architecture change across durable state/process boundaries needs migration and rollback, not only code edits.

## Learning Objectives

After completing this module, you should be able to:

- recover a pattern's original context, force, invariant, and expected change axis;
- map hidden control/state/effect/lifecycle paths and reproduce concrete symptoms;
- use history, runtime, test, incident, and review evidence without mistaking metrics for proof;
- recognize characteristic misuse across major behavioral patterns;
- compare collapse, repair, replacement, decomposition, and language-native alternatives;
- design scoped preservation evidence and safe incremental migrations;
- remove transitional abstraction after measured convergence;
- review simplification in high-stakes systems without overstating safety or correctness.

## Core Exposition

### Start from a real symptom

Record a change that touched many unrelated places, an incident whose path was hard to trace, an order-dependent bug, a listener leak, a performance regression, a compatibility blockage, or tests coupled to internals. Include reproduction and impact.

“Too many classes” or “I dislike patterns” is not enough. The same structure may be cheap in one language/toolchain and costly in another.

### Recover the design hypothesis

Read adjacent code, tests, documentation, decision records, and introducing commits. Ask which variants/operations/states/clients/deployments were expected to change and which invariant/compatibility boundary the pattern protected.

Do not assume the current class name reflects original intent. A `Strategy` may now be a deployment adapter; a `Mediator` may own a transaction.

### Draw the actual runtime graph

Trace one representative success and each important failure/cancellation path. Mark dispatch, callbacks, state writes, locks, queues, I/O, transactions, retries, and resource ownership. Record order and thread/process boundaries.

Static dependency diagrams miss runtime plugin loading, callback retention, reflection, and event recursion. Runtime traces miss dormant compatibility/error cases; use both.

### Identify the change axes

Mine commits/issues for changes to algorithms, data variants, operations, states, policies, protocols, and effects. Count co-change cautiously: widespread edits may indicate wrong boundaries, but generated/synchronized changes distort counts.

Ask whether variation is independent. If every Strategy changes with the same context and only one is deployed, the seam may be speculative. If third parties or rolling versions implement it, the seam has compatibility value even with one local implementation.

### Inventory the indirection tax

Measure navigation hops, callback depth, class/config count, initialization/lifecycle states, runtime allocations, dispatch cost, queue/lock behavior, error translation, debugging steps, test doubles, and operational configuration. Qualitative review burden matters alongside metrics.

Do not add unlike quantities into a fake universal score. Use the vector to compare concrete candidates under the same workload and invariants.

### Establish preservation obligations

List public/internal compatibility, return values, error taxonomy, effects/order, transaction boundaries, idempotency, concurrency, cancellation, resource limits, logging/audit, authorization, serialization, and performance SLOs. Mark intentionally changed behavior separately.

Characterization tests cover current observations; domain/reference tests decide correctness. Preserve known defects only long enough to separate structure change from correction.

### Form multiple hypotheses

Candidates include keep as-is, repair lifecycle/contracts, inline/collapse, replace with function/table/ADT pattern matching/native multimethod, split one overloaded abstraction, move ownership, or adopt a different pattern whose forces actually fit.

Do not choose “replace pattern X with pattern Y” before diagnosing. Often the best result is a named function and explicit conditional.

### Diagnose Chain and Command misuse

A Chain of Responsibility misfits when order/terminal semantics are hidden, handlers mutate shared context, every request traverses all nodes, or only one fixed handler exists. Repair with explicit pipeline/result policy or collapse to direct calls.

Command misfits when hundreds of one-line classes have no scheduling, queueing, undo, authorization, logging, retry, or composition value. First-class functions may suffice. Retain Command where request identity/lifecycle/effects are real.

### Diagnose Interpreter and Iterator misuse

Interpreter misfits when an ad hoc grammar grows without parser tooling, source positions, resource limits, versioning, or security, or when configuration would suffice. Use a parser/validated AST/existing language where appropriate.

Iterator misfits when custom cursors duplicate a language protocol, mutation/concurrency is undefined, or resources leak on early exit. Adopt the native iteration/resource pattern unless compatibility or specialized traversal semantics justify custom APIs.

### Diagnose Mediator and Memento misuse

Mediator becomes a god coordinator when it knows every component state, business rule, and effect; satellites become anemic. Split workflows/domains or move invariants to owners while keeping only genuine coordination.

Memento misfits when snapshots serialize whole graphs, secrets/resources, or unbounded history without restoration validation. Prefer commands/deltas/event log or bounded domain snapshots according to recovery semantics.

### Diagnose Observer and callback misuse

Signals include hidden critical workflows, listener leaks, unspecified order, synchronous blocking, recursive storms, swallowed errors, unbounded async work, and crash-lost obligations. Repair subscription ownership and bounded semantics; move durable business effects to outbox/workflow.

Do not replace every observer with direct coupling. Optional UI/telemetry notifications can remain one-to-many local events once lifecycle and failure are explicit.

### Diagnose State and Strategy misuse

State misfits when a stable enum/conditional is clearer, state objects hold no behavior, transitions are scattered, or concurrent/persisted transitions bypass one owner. Conversely, a giant state switch with many state-specific operations may justify State.

Strategy misfits with one implementation, no independent algorithm evolution, and wrappers/configuration more complex than a parameter/function. Retain it for real substitution, testing at an external boundary, or independently released implementations.

### Diagnose Template Method and Visitor misuse

Template Method misfits when subclasses override most hooks, require call-order knowledge, share little invariant, or inheritance blocks independent composition. Replace with explicit collaborators/functions/composition, preserving the invariant skeleton owner.

Visitor misfits when element variants change more often than operations, defaults silently skip new variants, traversal/state/effects are duplicated, or native exhaustive pattern matching is clearer. Retain for stable variants with many operations and binary/plugin constraints that match.

### Diagnose Null, Specification, and Policy misuse

Null Object is dangerous when it converts required dependency, outage, authorization, audit, persistence, or alarm absence into success. Make optionality valid and observable; otherwise fail construction or return explicit error/deny.

Specification/Policy misfit when generic field/operator trees erase domain language, in-memory and query semantics diverge, facts are fetched inside rules, outcomes collapse to Boolean, or untrusted callers select permissive rules. Narrow the language/decision owner and restore typed evidence.

### Diagnose Method, Role, and double-dispatch misuse

Method Object misfits when it merely moves a long method into mutable fields without clearer phases or ownership; simplify to pure functions/pipeline/domain types. Role Object misfits as a dictionary of nullable extensions without identity, constraints, lifecycle, or authority.

Double dispatch misfits for a sparse/rapidly changing matrix, where a typed registry or native multimethod/pair match is clearer. Verify language overload/ambiguity and ordered-pair semantics before replacement.

### Diagnose test-pattern misuse

Object Mothers/builders misfit when defaults hide assertion premises, fixtures are shared mutable graphs, helpers duplicate production invariants/oracles, or a central DSL couples every test. Move salient values inline, use fresh aggregate builders, and split ownership.

Test convenience is not evidence quality. A shorter Arrange block can make failures harder to diagnose.

### Assess language and framework evolution

First-class functions can replace some Command/Strategy objects; generators native iterators; algebraic data types/exhaustive matching some State/Visitor; native multiple dispatch some two-stage callbacks; structured concurrency/streams some listener infrastructure.

Confirm exact semantics, debugger/tool support, binary/source compatibility, team competence, and long-term platform support. Fewer source lines can shift complexity to runtime magic.

### Refactor through a strangler seam

Introduce a comparison boundary around old/new pure behavior, or route one controlled cohort to new behavior. For effects, shadow only decision/plans and apply one authoritative path. Record mismatches with bounded redacted evidence.

Move one responsibility/call path at a time, run focused checks, and keep commits coherent/reversible. Remove obsolete branches only after usage and parity evidence meet explicit criteria.

### Verify outcomes, not aesthetics

Compare maintenance task touch points, navigation/debug steps, error diagnosability, lifecycle states, runtime latency/allocation, incidents, and test coupling. Review with maintainers/operators/security/domain owners.

Reduced code/class count is helpful only if responsibilities and behavior became clearer. Record trade-offs and remaining limitations.

### Remove transitional complexity

Adapters, feature flags, dual writes/reads, compatibility callbacks, and deprecations need owners, dates, telemetry, and deletion commits. A migration that leaves two authoritative paths is incomplete.

Preserve externally required compatibility deliberately, but isolate it at the boundary rather than contaminating the new core.

## Definitions and Notation

Let candidate designs (D), required invariant/observation set (I), representative cases (W), and observation function (Obs(d,w)). Preservation obligation is

\[
\forall w\in W:\ Obs(d_{old},w)=Obs(d_{new},w)
\]

except separately approved semantic deltas. Evidence from finite (W) does not prove equality for all possible inputs/states. Benefit/cost vectors are ordinal/contextual decision aids; avoid false precision across incomparable dimensions.

## Mechanisms, Invariants, or Proof Structure

### Evidence-driven diagnosis procedure

1. Reproduce one concrete symptom and recover the pattern's context/force/change-axis hypothesis.
2. Map runtime control, data, state, effect, failure, lifecycle, and ownership paths.
3. Inspect change/incident/test/runtime history and compatibility/deployment constraints.
4. State preservation invariants and intentional behavior corrections separately.
5. Compare keep, repair, collapse, split, native-feature, and replacement candidates.
6. Build characterization/reference/differential/performance/security/concurrency evidence proportional to risk.
7. Migrate one reversible path at a time with one authoritative effect path and rollback.
8. Measure outcomes, document trade-offs, and delete transitional structures after convergence.

### Executable finite model

The following deterministic heuristic organizes three synthetic investigations. It is not a pattern detector or refactoring proof; its thresholds are explicit prompts that require source, history, runtime, and domain evidence.

<!-- bijux-verify: {"id":"misuse-triage","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"wrapper=collapse-indirection\nobserver=repair-lifecycle-first\nstrategy=retain-and-test-seam\n","stderr":""}} -->
```python
class DesignEvidence:
    def __init__(self, runtime_variants, forwarding_layers, independent_changes, lifecycle_hazards):
        self.runtime_variants = runtime_variants
        self.forwarding_layers = forwarding_layers
        self.independent_changes = independent_changes
        self.lifecycle_hazards = lifecycle_hazards


def triage(evidence):
    if evidence.lifecycle_hazards > 0:
        return "repair-lifecycle-first"
    if (
        evidence.runtime_variants <= 1
        and evidence.forwarding_layers >= 3
        and evidence.independent_changes == 0
    ):
        return "collapse-indirection"
    if evidence.runtime_variants >= 2 and evidence.independent_changes >= 2:
        return "retain-and-test-seam"
    return "measure-before-change"


wrapper = DesignEvidence(1, 4, 0, 0)
observer = DesignEvidence(3, 2, 4, 2)
strategy = DesignEvidence(3, 1, 5, 0)
print("wrapper=" + triage(wrapper))
print("observer=" + triage(observer))
print("strategy=" + triage(strategy))
```

Priority of lifecycle hazards prevents collapsing a leaky/racy design before its ownership semantics are understood. The heuristic cannot determine whether reported counts are valid, which behavior to preserve, or whether an alternative is better.

## Alternatives and Trade-Offs

- **Keep and document:** cheapest when the pattern still fits and confusion is onboarding/tooling debt.
- **Repair the implementation:** preserve a valid seam while fixing lifecycle, contracts, errors, or effects.
- **Inline/collapse:** removes unused variation and navigation; can lose compatibility or test boundaries.
- **Split responsibilities:** resolves a god Mediator/Policy/Mother without discarding useful sub-patterns.
- **Language-native feature:** reduces ceremony; changes portability, exhaustiveness, ambiguity, and tooling.
- **Table/data/DSL:** makes cases explicit and administrable; needs validation, versioning, security, and diagnostics.
- **Different pattern:** useful only when its context/forces demonstrably match better.
- **Rewrite:** can reset structural debt; carries parity, migration, schedule, integration, and operational risk.
- **Leave a boundary adapter:** preserves external compatibility; adds transitional or permanent edge complexity.

The right outcome can be “do nothing yet” when evidence is weak and the risk/cost of change exceeds demonstrated harm.

## Failure Modes and Misconceptions

- **“Pattern names prove design quality.”** Applicability, implementation, and consequences determine fitness.
- **“One implementation makes every interface wrong.”** External compatibility/testing/deployment may justify it.
- **“History predicts the future.”** It informs but does not settle planned regulatory/product/platform change.
- **“Fewer classes means simpler.”** Giant switches/configuration/reflection can hide worse complexity.
- **“Native language features are free.”** They carry semantics, version, tool, and team constraints.
- **“Characterization tests prove equivalence.”** They cover finite observations, often preserving defects.
- **“Shadow both paths.”** Effectful dual execution can duplicate irreversible actions.
- **“A benchmark chooses architecture.”** Maintainability, safety, security, compatibility, and operations also matter.
- **“Migration adapters can remain.”** Without removal criteria they create permanent dual authority.
- **“Successful simplification proves correctness.”** Domain and high-stakes evidence remain independent.

## Worked Examples

### Example 1

A Strategy has one local implementation but three third-party implementations across binary boundaries. History shows independent changes. **Conclusion:** Local class count alone would misdiagnose the seam.

### Example 2

Five forwarding decorators add no policy, metrics, security, or variation. Characterization tests support inlining four. **Conclusion:** Collapse indirection with preserved observables.

### Example 3

An Observer leaks screens and loses payment notifications on crash. Explicit subscription fixes retention; outbox handles the durable obligation. **Conclusion:** Split lifecycle repair from delivery architecture.

### Example 4

A State hierarchy has eight empty classes and all transitions in one service. A typed enum/table makes ownership explicit. **Conclusion:** State-shaped classes without state behavior add ceremony.

### Example 5

A Visitor default silently skips a new security-sensitive AST node. Exhaustive ADT matching blocks compilation instead. **Conclusion:** Evolution behavior matters more than pattern familiarity.

### Example 6

A Null repository discards writes after configuration failure. Startup validation removes the invalid optionality. **Conclusion:** Do not “simplify” required effects into success.

### Example 7

A generic Policy engine accepts arbitrary fields and returns Boolean. Narrow domain decisions with typed indeterminate/error improve trust. **Conclusion:** Generality can erase semantics.

### Example 8

A Test Data Builder default computes the expected discount using production Policy. Independent boundary constants expose a defect. **Conclusion:** Test abstractions must not share the oracle.

### Example 9

Old/new pricing paths are shadowed, but only the authoritative old path charges. Decision mismatches are redacted and measured. **Conclusion:** Compare pure plans before switching effects.

### Example 10

A control-system callback graph is flattened and unit tests pass, but worst-case timing and hazard independence are not revalidated. **Conclusion:** Structural simplicity is not safety evidence.

## Cross-Program Connections

- **Programming Languages and Semantics:** dispatch, effects, algebraic types, closures, matching, and evaluation order shape alternatives.
- **Object-Oriented Programming:** polymorphism, composition, identity, lifecycle, and contracts explain pattern costs/benefits.
- **Software Design and Domain Modeling:** boundaries, invariants, ownership, language, and change axes ground diagnosis.
- **Testing and Quality Engineering:** characterization, differential, property, mutation, concurrency, and fault tests support preservation.
- **Algorithm Engineering:** profiles, allocation, latency distributions, workload models, and benchmarks quantify runtime liabilities.
- **Security Engineering:** authorization, fail-safe defaults, plugin trust, disclosure, and audit prevent unsafe simplification.
- **Database Engineering:** transactions, migrations, dual read/write, snapshots, and compatibility constrain changes.
- **Distributed Systems:** version skew, retries, idempotency, partitions, observability, and rollout complicate pattern boundaries.
- **Engineering Management:** ownership, review load, cognitive/navigation cost, planned roadmap, and deletion work affect outcomes.
- **Safety and High-Assurance Engineering:** hazard analysis, independent assurance, timing/resource proofs, and controlled change exceed refactoring tests.

## References

1. Christopher Alexander et al., *A Pattern Language*, Oxford University Press, 1977, ISBN 978-0-19-501919-3. Establishes patterns as contextual relationships among recurring problems, forces, and consequences.
2. Erich Gamma et al., *Design Patterns: Elements of Reusable Object-Oriented Software*, Addison-Wesley, 1994, ISBN 978-0-201-63361-0. Canonical behavioral pattern intents, structures, applicability, and consequences.
3. Martin Fowler, with Kent Beck, *Refactoring: Improving the Design of Existing Code*, second edition, Addison-Wesley, 2018, ISBN 978-0-13-475759-9. Provides smell-driven, behavior-preserving incremental restructuring.
4. Joshua Kerievsky, *Refactoring to Patterns*, Addison-Wesley, 2004, ISBN 978-0-321-21335-8. Connects evolutionary refactoring motivations to pattern introduction and simplification.
5. William J. Brown et al., *AntiPatterns: Refactoring Software, Architectures, and Projects in Crisis*, Wiley, 1998, ISBN 978-0-471-19713-3. Provides recurring poor-solution diagnosis and refactored solutions.
6. Peter Norvig, [“Design Patterns in Dynamic Programming”](https://www.norvig.com/design-patterns/design-patterns.pdf), 1996. Demonstrates how language features change pattern implementation and necessity.
7. David L. Parnas, [“On the Criteria To Be Used in Decomposing Systems into Modules”](https://doi.org/10.1145/361598.361623), *Communications of the ACM* 15(12), 1972. Grounds decomposition in hidden design decisions/changeability rather than execution steps.
8. Mohamad Kessentini et al., [“A Large-Scale Empirical Study of the Impact of Spaghetti Code and Blob Anti-Patterns on Program Comprehension”](https://doi.org/10.1016/j.infsof.2020.106278), *Information and Software Technology* 122, 2020. Provides scoped empirical evidence on anti-patterns and comprehension.

## Exercises

### Exercise 1

Trace the executable triage heuristic and state exactly what its outputs establish and cannot establish.

### Exercise 2

Diagnose a Strategy/Template Method subsystem using symptoms, change history, runtime graph, invariants, and alternatives.

### Exercise 3

Design a safe migration from a synchronous Observer carrying critical effects to explicit local notification plus durable workflow.

### Exercise 4

Create a comparative diagnosis for Visitor versus exhaustive pattern matching under changing variants and operations.

### Exercise 5

Review behavioral-pattern simplification in a high-stakes system without claiming safety, domain, or regulatory correctness.

## Answers to the Exercises

### Answer 1

Wrapper has one variant, four forwarding layers, no independent changes, and no lifecycle hazard; the second branch returns collapse-indirection. Observer has two lifecycle hazards, so the first branch returns repair-lifecycle-first even though it also has variation/change. Strategy has three variants and five independent changes with no hazard, so retain-and-test-seam.

The run establishes deterministic branch precedence and exact results for three synthetic integer records. It does not validate the counts, thresholds, pattern identification, maintenance benefit, lifecycle repair, preservation invariants, alternative design, performance, compatibility, or domain correctness. `measure-before-change` is also unexecuted. It is a discussion scaffold, not an automated architectural verdict.

### Answer 2

Reproduce a real change/bug: perhaps adding one pricing algorithm requires edits in base template, hooks, factory, configuration, and tests. Map one request through selection, inherited skeleton/hooks, state, I/O, errors, effects, thread/transaction. Mine changes: do algorithms vary independently, or do all subclasses change whenever the skeleton changes? Identify subclass hook override ratios, call-order assumptions, protected state, deployments/plugins, and test seams without treating counts as proof.

Preserve price/error/rounding, effect/order, authorization, telemetry, compatibility, and latency. Compare: keep and document; repair Template Method hooks; replace inheritance with composed Strategy functions; collapse if one real algorithm; split fact gathering/pure calculation/effects. Implement pure old/new differential corpus and boundary/property/mutation tests, then migrate one server-owned cohort with one authoritative effect path. Benchmark representative distributions, inspect diagnostics/security, rollback on unexplained mismatches, and delete adapters/flags after parity/use criteria.

### Answer 3

Inventory every event, publisher transaction point, listener owner/lifetime/thread/order/error, and effect obligation. Classify ephemeral UI/cache/metrics versus durable payment/audit/notification work. First return idempotent subscription handles, snapshot outside locks, bound reentrancy/work, define failure reporting, and add retention/concurrency tests so current semantics are known.

Define durable event ID/schema/aggregate sequence/minimal data and persist state plus outbox atomically. Relay with lease/retry/lag; consumers authenticate/authorize, deduplicate/idempotently apply, handle order/version/poison/dead-letter/reconciliation, and record outcomes. Shadow messages/decisions but never duplicate effects. Fault-inject crashes at commit/publish/consume/effect, broker outage, duplicates/reordering, schema skew, and shutdown. Controlled cutover keeps rollback/replay/drain, then removes business-critical listener path while retaining explicit local notifications.

### Answer 4

Construct element-operation matrix and repository history: frequency/ownership of new element rows versus operation columns, binary/plugin boundaries, traversal/effects, default omissions, and language/tool support. Visitor benefits stable rows, separately added operation columns, OO/binary protocols, and per-operation state; it costs broad updates for new rows and traversal boilerplate. Sealed ADT matching offers compiler exhaustiveness and local operation functions but centralizes row awareness and may not support third-party variants/binary evolution.

Preserve exact dispatch, result/errors, traversal order/sharing/cycles, transformations, effects, compatibility, and performance. Prototype one representative operation with exhaustive match, run full matrix coordinate tests, deep/shared/cyclic/property/differential/mutation tests, compiler/version compatibility, and benchmarks. If rows change often and language matching is stronger, migrate operation by operation behind pure comparison; if external visitors or stable rows dominate, repair defaults/exhaustiveness instead. Record trade-offs rather than declaring one universally simpler.

### Answer 5

Define system purpose, hazards/consequences, current pattern responsibility, timing/resource/concurrency requirements, interfaces/state/effects, failure/degraded modes, compatibility, cybersecurity, human workflow, and exact proposed improvement. Trace every success/fault/cancellation path and recover safety requirements, assumptions, independence, and operational evidence before changing control flow.

Evidence requires requirements/hazard traceability, independent domain/safety/verification review, old/new behavioral/effect/error/timing equivalence over authoritative cases, state/concurrency/formal analysis where required, worst-case resource and fault-injection tests, hardware/site/workflow/human-factors trials, cybersecurity, migration/rollback/monitoring/proof-test/incident records, and applicable quality/regulatory change control. Named domain/clinical/controls, safety, verification, security, human-factors, quality/regulatory, and operations reviewers approve. Fewer classes, green tests, and lower median latency establish no safety or regulatory fitness.
