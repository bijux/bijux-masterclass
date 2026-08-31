---
module_id: SEPAT-008
program: Software Engineering: Patterns
level: 1
module_number: 8
title: Refactoring Toward and Away from Patterns
status: complete
last_verified: 2026-08-28
---

# Refactoring Toward and Away from Patterns

## One-Page Review

### Governing question

How can an existing design move safely toward a pattern when forces emerge—and back toward simpler code when those forces disappear?

### Essential definitions

- **Refactoring** is a small internal structural change, or a sequence of such changes, that preserves declared observable behavior while improving understandability or changeability.
- An **observation boundary** states which outputs, effects, interfaces, timing classes, and operational behaviors must remain unchanged.
- A **characterization test** records behavior currently exhibited by a system, including behavior not yet fully understood.
- A **seam** is a place where behavior can be varied without editing the surrounding code directly.
- **Preparatory refactoring** changes structure so a later behavioral change becomes easier and safer.
- **Refactoring toward a pattern** incrementally creates roles or collaborations justified by observed forces.
- **Refactoring away from a pattern** removes roles or indirection whose benefits no longer exceed their costs.
- **Parallel change** or **expand–migrate–contract** keeps old and new structures valid while callers move incrementally.
- A **rollback point** is a coherent verified state to which the change can return safely.

### Central model, mechanism, or theorem

Let program states be (P_0,P_1,\ldots,P_n) and (Obs_C) the observations protected by contract (C). A refactoring sequence requires

$$
Obs_C(P_i)=Obs_C(P_{i+1})
\quad\text{for every }i<n.
$$

The final shape may instantiate or remove a pattern, but pattern names do not prove preservation. Each step needs preconditions, transformation, and verification. After the structural sequence, a separately reviewed behavioral change can use the new shape.

### Critical invariants

- The protected observation boundary is explicit and includes published interfaces where applicable.
- Every step leaves the repository coherent and passes the narrowest relevant checks.
- Tests assert behavior, not the internal collaboration being changed.
- Pattern roles are introduced only as forces become evidenced.
- Old and new paths cannot diverge silently during parallel change.
- Removing a pattern preserves necessary contracts and migration compatibility.
- Performance, concurrency, persistence, and security equivalence are not inferred from unit-output equality alone.

### Common failures

Common failures include calling a rewrite a refactor, mixing behavior changes with structural moves, snapshotting a bug as an unquestionable requirement, testing private call order, introducing all pattern roles at once, leaving dual paths indefinitely, removing an abstraction while published clients still depend on it, and treating green unit tests as proof of timing, transaction, or concurrency preservation.

### Compact example

A pricing function contains three branches that change independently. First characterize outputs and errors. Extract each branch into a named function, introduce a policy lookup behind the existing entry point, and verify the same cases after every move. Only then add a new policy. If two policies later disappear permanently, inline the remaining function and remove the lookup while retaining the public entry point and behavior.

### Connections

[SEPAT-004](004-pattern-intent-and-applicability.md) determines when a pattern is justified; [SEPAT-005](005-trade-offs-and-negative-consequences.md) determines when its balance changes. [SEPAT-009](../ROADMAP.md) addresses pattern-driven overengineering. Refactoring evidence connects to [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) and safe delivery to [Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md).

## Governing Question

What sequence of verified structural changes gets the design closer to its current forces without pretending the desired pattern is the starting requirement?

Patterns often emerge from refactoring. Repeated conditionals reveal a varying policy; scattered construction reveals an unstable creation decision; direct provider calls reveal an external contract boundary. The design does not need to predict every role up front. It can grow them when the pressure is concrete.

The reverse is equally important. A Strategy with one permanent implementation, a Factory hiding one trivial constructor, or an Observer with fixed ordered subscribers can outlive its purpose. Refactoring away is not regression. It is adaptation to a new context.

## Why This Matters

Large “pattern migrations” combine discovery, redesign, behavior change, and deployment. When they fail, the team cannot tell which assumption broke. Small refactorings create feedback and review points. They also preserve the option to stop before the catalog-perfect destination when a simpler structure resolves the force.

Refactoring away protects long-lived systems from abstraction sediment. Every pattern adds concepts and constraints. If expected variation never arrives, maintaining those roles consumes attention without delivering benefit. A safe removal sequence proves which contracts remain necessary.

## Prerequisites and Retrieval

You should understand pattern applicability, behavior contracts, tests, interfaces, and version control. Retrieve these facts:

1. Observable behavior depends on the declared observer and boundary.
2. A public interface can be observable even when implementation output is unchanged.
3. Tests sample behavior unless supported by stronger analysis or proof.
4. A seam enables substitution; it is not automatically a permanent abstraction.
5. Feature changes and refactorings can alternate, but one small step should have one clear intent.
6. A pattern's value is conditional and can expire.

## Learning Objectives

After completing this module, you should be able to:

- define a protected observation boundary for a refactoring;
- build characterization evidence without canonizing unintended behavior blindly;
- identify seams and preparatory refactorings;
- sequence small transformations toward a pattern;
- separate structural preservation from later feature changes;
- use expand–migrate–contract across published or distributed boundaries;
- refactor away from obsolete pattern roles;
- state the limits of tests as preservation evidence.

## Core Exposition

### Behavior preservation is relative

“No behavior change” needs an observer. Return values, exceptions, persistent writes, emitted events, logs, latency, memory, interface compatibility, and ordering are all observable to someone. A local refactor may preserve functional output while changing transaction boundaries or audit order.

Define the contract before moving structure. For pure computation, input/output equality may suffice. For a service, include API schema, error mapping, state effects, authorization, telemetry relied upon operationally, and performance budgets. Preserve accidental behavior only after deciding who depends on it and whether correcting it is a separate feature or bug fix.

### Characterize before changing

Legacy behavior is often underdocumented. Characterization tests create feedback: representative outputs, boundary cases, errors, and effects. They do not declare every observation desirable. Label surprising cases and resolve them explicitly.

Avoid tests tied to private method calls or current classes when those are the refactoring target. Assert through stable boundaries. Add targeted instrumentation temporarily when effects are otherwise invisible.

### Find the force before the pattern

Start from change history and friction. Which edits recur? Which decisions vary? Which dependencies block testing? Which failures cross boundaries? Then choose a small transformation that localizes that pressure.

Do not set “implement Strategy” as the success criterion. A function table may resolve policy variation before strategy objects are necessary. Do not force the final pattern diagram when an earlier stopping point is cohesive and verifiable.

### Preparatory moves

Common moves include rename for intent, extract function, split responsibility, move function, introduce parameter, wrap external call, isolate side effect, replace temporary with query, and add a narrow interface. Each reduces ambiguity or creates a seam.

Preparatory refactoring is valuable only in service of a near change. Broad speculative cleanup increases scope and merge conflict. Keep steps close to the demonstrated force.

### Toward a pattern

For Strategy, extract policy branches, make inputs explicit, equalize signatures, place selection at one boundary, and only then introduce a role if state or independent evolution needs it. For Adapter, first characterize the local capability and provider semantics, wrap one call, translate errors explicitly, migrate callers, then hide the provider behind the owned boundary.

For Observer, extract direct notifications, define event meaning and failure policy, introduce explicit subscriber registration, migrate optional dependents, and retain direct calls for mandatory ordered work. The goal may be a hybrid rather than a pure pattern instance.

### Parallel change

When all callers cannot move atomically, expand the system with a compatible new path, migrate callers while measuring both, then contract the old path. Examples include interface versions, database columns, event schemas, and module boundaries.

Dual paths introduce divergence risk. Establish one source of truth, comparison checks, migration inventory, deadlines, and removal ownership. “Temporary compatibility” without contraction criteria becomes permanent complexity.

### Separate structural and behavioral commits

A refactoring commit should make reviewable preservation claims. The following feature commit can add a new policy or behavior using the improved structure. When inseparable at deployment scale, still separate logical verification: old-vs-new equivalence first, then new-case evidence.

This discipline narrows diagnosis. It also makes rollback meaningful: reverting a feature need not discard a safe structural improvement.

### Away from a pattern

Reassess the forces. If variability, lifecycle, distribution, or compatibility disappeared, identify the minimum contract that remains. Inline trivial delegation, collapse one-use factories, replace registries with explicit construction, convert fixed observers to direct calls, or remove pass-through adapters.

Preserve published interfaces through a compatibility facade if needed. Remove internal role names only after callers and tests stop depending on them. Delete obsolete configuration, registrations, metrics, documentation, and operational alerts as part of contraction.

### Refactoring and data or distribution

Source-level atomicity does not extend across databases, deployed clients, or message consumers. Use expand–migrate–contract, dual reads/writes only with clear authority, backfill verification, and compatibility windows. A database or protocol change can preserve system behavior only when all coupled artifacts are considered.

Concurrency refactoring needs schedule-sensitive evidence: races, deadlocks, cancellation, ordering, and load. Passing deterministic examples does not prove equivalence across interleavings.

### Know when to stop

Stop when the current force is localized, behavior evidence passes, and another abstraction would serve only a hypothetical future. Record the next trigger. A refactoring sequence is successful even if it ends before a named pattern.

## Definitions and Notation

Let program state (P) include source, configuration, persistent schema, and relevant deployed contracts. Let (C) declare protected observations and environment assumptions. A refactoring (r) is a partial transformation

$$
r:P\rightharpoonup P'
$$

with precondition (Pre_r(P)) and preservation obligation

$$
Pre_r(P)\Rightarrow Obs_C(P)=Obs_C(r(P)).
$$

A sequence (R=r_n\circ\cdots\circ r_1) is safe only when every intermediate precondition holds and every step preserves the declared observations. Final equality follows by transitivity under the same (C); if the observation boundary or environment changes, the argument must be renewed.

Tests provide finite evidence set (T\subseteq Inputs). Passing establishes

$$
\forall t\in T,\ Obs_C(P,t)=Obs_C(P',t),
$$

not equality for all possible inputs or schedules. Static analysis, types, proofs, contracts, and production comparison can strengthen evidence.

For parallel change, states are

$$
P_{old}\rightarrow P_{old+new}\rightarrow P_{new},
$$

with compatibility and authority invariants maintained during the middle state.

## Mechanisms, Invariants, or Proof Structure

### Declare observations and risk

List API, output, error, state, event, timing, concurrency, security, and operational observations. Scale evidence to consequence severity.

### Establish feedback

Add characterization, contract, property, integration, and failure tests at stable boundaries. Record coverage gaps and nondeterminism.

### Make one structural move

Check preconditions, apply a named small transformation, run focused evidence, inspect the diff, and keep the state coherent. Commit when one durable intent is complete.

### Compare two structures

The executable example confirms selected price cases match before and after extracting policies. It does not prove universal equivalence.

<!-- bijux-verify: {"id":"conditional-to-policy-equivalence","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"standard: before=100 after=100 equal=True\nmember: before=90 after=90 equal=True\nclearance: before=70 after=70 equal=True\nchecked cases: 3\n","stderr":""}} -->
```python
def price_before(kind, amount):
    if kind == "member":
        return amount * 90 // 100
    if kind == "clearance":
        return amount * 70 // 100
    return amount


def standard(amount):
    return amount


def member(amount):
    return amount * 90 // 100


def clearance(amount):
    return amount * 70 // 100


policies = {"standard": standard, "member": member, "clearance": clearance}


def price_after(kind, amount):
    return policies[kind](amount)


for kind in ("standard", "member", "clearance"):
    before = price_before(kind, 100)
    after = price_after(kind, 100)
    print(f"{kind}: before={before} after={after} equal={before == after}")
print("checked cases: 3")
```

### Introduce or remove roles incrementally

Migrate one caller or case, compare behavior, then broaden. During removal, reverse dependencies and retain compatibility until consumers are proven migrated.

### Verify the resulting design

Run broader tests, static checks, performance and failure evidence as relevant. Inspect whether the target force is actually easier to handle and whether new roles have owners.

## Alternatives and Trade-Offs

**Rewrite.** Can replace deeply unsuitable structure quickly in a small bounded component. It loses incremental behavioral evidence and often underestimates hidden contracts.

**Branch-by-abstraction.** Supports long migrations behind a stable seam. It adds a temporary abstraction and coordination overhead.

**Feature flag.** Allows runtime comparison and rollback. Flags add state combinations and do not by themselves preserve structural equivalence.

**Automated refactoring tool.** Reliably applies supported transformations under language-model assumptions. Reflection, generated code, macros, dynamic calls, and external contracts can escape its analysis.

**Characterization tests.** Provide rapid feedback in poorly understood code. They can freeze defects if no one classifies surprising behavior.

**Formal equivalence.** Provides stronger assurance for tractable models. Modeling cost and environment assumptions limit use.

**Leave the design alone.** Appropriate when change pressure is absent and risk exceeds benefit. Record the trigger for reconsideration.

## Failure Modes and Misconceptions

1. **Any cleanup is refactoring.** Preservation and structural purpose define the term.
2. **Tests define all observable behavior.** They sample declared cases and may omit interfaces, timing, state, or schedules.
3. **Pattern shape is the destination.** The current force, not catalog fidelity, determines the stopping point.
4. **Behavior and refactoring can be mixed freely.** Mixing expands review and diagnosis; separate them where practical.
5. **A seam must become permanent architecture.** Remove it if it no longer carries useful variation.
6. **Expand–migrate–contract ends after migration starts.** Unremoved compatibility paths are unfinished work.
7. **Published interface changes are internal.** The interface is observable to external consumers.
8. **Green unit tests prove database or concurrency equivalence.** Cross-artifact and schedule evidence remain.
9. **Refactoring away loses flexibility.** Unused flexibility is a cost; retain only evidenced option value.
10. **Large pattern migrations are faster.** Their hidden assumptions and rollback surface often make them slower overall.

## Worked Examples

### Example 1

**Question:** How does repeated branching move toward Strategy?

**Reasoning:** Characterize cases, extract each algorithm, equalize inputs, centralize selection, and migrate callers. Introduce stateful strategy objects only if functions no longer express lifecycle or related operations.

**Conclusion:** Grow the smallest policy seam before committing to a class pattern.

### Example 2

**Question:** How can a provider integration move toward Adapter?

**Reasoning:** Define the local capability from client needs, wrap one provider call, preserve provider-specific errors explicitly, run shared contract tests, then migrate callers. Remove direct SDK dependencies only after inventory reaches zero.

**Conclusion:** Adapter emerges through a verified boundary, not a wholesale interface rewrite.

### Example 3

**Question:** When should one-use Factory be removed?

**Reasoning:** If construction is trivial, one product exists, and no compatibility boundary depends on the factory, inline construction at the composition root, migrate callers, and delete registration/configuration. Preserve validation in a named constructor if it remains valuable.

**Conclusion:** Remove creation indirection when its variability force disappears.

### Example 4

**Question:** Can fixed Observer callbacks become direct calls?

**Reasoning:** Characterize order and failure, replace one registered mandatory subscriber with an explicit call, compare traces, then remove registration state. Keep optional notifications event-driven if their forces differ.

**Conclusion:** Refactoring away can yield a hybrid with clearer critical control.

### Example 5

**Question:** How should Singleton be dismantled?

**Reasoning:** Find implicit access, add parameters at nearest seams, construct one explicit instance at the composition root, migrate consumers, then remove global lookup and reset hooks. Tests verify isolation and lifecycle.

**Conclusion:** Replace global access incrementally; instance count and dependency visibility are separate decisions.

### Example 6

**Question:** What does the executable equivalence check prove?

**Reasoning:** For amount 100 and three declared kinds, both implementations return identical integers. It does not cover other amounts, unknown kinds, overflow, performance, or mutable policy registration.

**Conclusion:** Executable examples support bounded cases and must not become universal equivalence claims.

### Example 7

**Question:** How can Template Method move toward composition?

**Reasoning:** Characterize subclass hooks, extract one varying step into a collaborator, delegate from the base algorithm, migrate subclasses, and remove overrides. Retain the template only if fixed algorithm order still matters.

**Conclusion:** Refactor role by role instead of replacing an inheritance tree atomically.

### Example 8

**Question:** What makes a database column rename a parallel change?

**Reasoning:** Add the new column, make code compatible with both under one write authority, backfill and verify, migrate readers, stop old writes, then remove the old column after every deployed consumer exits the compatibility window.

**Conclusion:** System behavior spans schema, data, code, and deployment; contraction is part of completion.

### Example 9

**Question:** Should a pass-through Facade remain for possible future use?

**Reasoning:** If it mirrors one stable subsystem, adds no policy, and is internal, measure callers and inline it. If it is a published compatibility boundary, retain the contract while simplifying the implementation.

**Conclusion:** Distinguish current internal indirection from externally valuable stability.

### Example 10

**Question:** How should a team stop a refactoring sequence?

**Reasoning:** After extracting a function table, adding a new policy requires one entry and no client changes. State and lifecycle remain trivial. Strategy classes would add navigation without resolving another force.

**Conclusion:** Stop at the smallest structure that makes the evidenced change safe.

## Cross-Program Connections

- **Programming Languages:** refactoring preconditions depend on name resolution, typing, macros, reflection, and module semantics.
- **Object-Oriented Programming:** extract collaborator, replace inheritance, and make dependencies explicit reshape object roles.
- **Functional Programming:** pure extraction and equivalence reasoning often create low-risk seams.
- **Software Design:** change history and responsibility cohesion reveal which pattern roles are justified.
- **Testing & Quality Engineering:** characterization, contract, property, concurrency, and differential tests support different preservation claims.
- **Database Engineering:** schema refactoring spans data, code, compatibility, and transaction authority.
- **Distributed Systems:** deployed consumers and protocols require parallel change and explicit compatibility windows.
- **Security Engineering:** authorization and audit observations must remain protected during structural moves.
- **Delivery Engineering:** small commits, flags, staged rollout, telemetry, and rollback carry refactoring safely into production.
- **Engineering Management:** contraction ownership and scope control prevent migrations from becoming permanent programs.

## References

1. Martin Fowler, [*Refactoring: Improving the Design of Existing Code*, 2nd ed.](https://www.pearson.com/en-us/subject-catalog/p/refactoring-improving-the-design-of-existing-code/P200000000254/9780134757599), Addison-Wesley, 2018. Defines disciplined behavior-preserving structural change and catalogs small transformations.
2. Martin Fowler, [“Definition of Refactoring”](https://martinfowler.com/bliki/DefinitionOfRefactoring.html), 2004, accessed 2026-08-28. Concise primary author statement distinguishing a refactoring from the sequence of refactoring.
3. Joshua Kerievsky, *Refactoring to Patterns*, Addison-Wesley, 2004, ISBN 978-0-321-21335-8. Develops incremental transformations toward and away from pattern structures while warning against premature patterns.
4. Michael Feathers, [*Working Effectively with Legacy Code*](https://www.pearson.com/en-us/subject-catalog/p/working-effectively-with-legacy-code/P200000008984), Prentice Hall, 2004, ISBN 978-0-13-117705-5. Establishes characterization tests, seams, sensing, separation, and dependency-breaking techniques.
5. Tom Mens and Tom Tourwé, [“A Survey of Software Refactoring”](https://doi.org/10.1109/TSE.2004.1265817), *IEEE Transactions on Software Engineering* 30(2), pp. 126–139, 2004. Surveys refactoring activities, preservation, formalisms, tools, and process effects.
6. William F. Opdyke, *Refactoring Object-Oriented Frameworks*, PhD dissertation, University of Illinois at Urbana-Champaign, 1992. Foundational formal and practical work on behavior-preserving object-oriented refactorings.
7. Paul Ambler and Martin Fowler, [“Evolutionary Database Design”](https://www.martinfowler.com/articles/evodb.html), accessed 2026-08-28. Explains database refactoring across schema, migration, code, tests, and deployment practices.

## Exercises

### Exercise 1

Define an observation boundary for refactoring a synchronous payment adapter. Include at least eight protected observations beyond the return value.

### Exercise 2

Extend the executable equivalence reasoning to amount 101. Compute all three outputs before and after, then identify two still-uncovered partitions.

### Exercise 3

Design a refactoring sequence from a global service locator toward explicit dependency injection, including characterization, seams, migration inventory, and contraction.

### Exercise 4

A codebase has Strategy, Factory, and Registry around one stable formatter. Design a refactoring away that preserves a published formatting API and plugin compatibility for one release.

### Exercise 5

An unfamiliar hospital scheduling platform must replace direct database writes with a Unit of Work while remaining continuously available. Produce an expand–migrate–contract plan with observation boundaries, transaction and concurrency invariants, verification, rollback points, and a criterion for stopping short of the full pattern.

## Answers to the Exercises

### Answer 1

Protect request schema, authorization decision, idempotency-key handling, provider request mapping, timeout/deadline behavior, error classification, persistent payment state, emitted domain events, audit records and order, trace correlation, retry count, and latency/resource budgets. Also protect published API compatibility and duplicate-effect behavior. Some observations may intentionally change later, but those changes belong in separately reviewed behavior work.

### Answer 2

Integer arithmetic gives standard (101), member (101\cdot90//100=90), and clearance (101\cdot70//100=70) in both implementations. The added case exercises truncation differently from 100. Still-uncovered partitions include negative or extremely large amounts, unknown `kind`, noninteger input, mutable/corrupt policy maps, and concurrency around policy registration. Exact domain constraints determine which are admissible.

### Answer 3

Inventory locator reads and lifecycle/reset behavior. Characterize consumer outputs, failures, singleton scope, startup, shutdown, and tests. Add explicit parameters at leaf consumers while temporarily defaulting through a narrow adapter to the locator. Move construction upward one layer at a time, passing dependencies explicitly and recording migrated call sites.

At the composition root, create the current one instance and supply it to consumers. Remove default locator fallback once inventory reaches zero, prohibit new reads through static checks, delete global registration/reset, and verify multi-instance isolation and lifecycle. Each layer migration is a rollback point. Keep direct construction for trivial immutable collaborators rather than forcing a container framework.

### Answer 4

Characterize the published formatting API and current plugin discovery. Introduce a simple internal formatter function behind the existing facade. Make Factory return that implementation, then replace internal Registry lookup with an explicit compatibility map for documented plugin keys. Migrate internal callers to the facade/function and compare outputs.

For one release, keep the published Factory/Registry entry points as deprecated adapters forwarding to the compatibility map, with usage telemetry and warnings. Publish migration instructions. After the compatibility window and verified external migration, remove plugin registration and factory roles if no independent formatter variation exists. Retain the published facade if it still owns compatibility; do not expose the internal simplification as an accidental breaking change.

### Answer 5

Define observations: appointment consistency, conflict detection, authorization, audit order, API/errors, transaction isolation, event publication, latency, and availability. Characterize direct writes and concurrent booking conflicts. Add a Unit-of-Work interface around the existing transaction path without changing behavior; initially it can delegate one write.

Expand by binding one scheduling operation to one explicit transaction scope and identity map while old operations remain unchanged. Add differential and concurrency tests. Migrate operations individually, ensuring repositories share the same scope and only Unit of Work commits. Use traffic cohorts or flags with telemetry for commit/rollback, conflict, duplicate identity, latency, and error changes. Rollback at each operation boundary by routing it to the old path; never dual-write without one authoritative outcome.

Contract after all operations and background jobs are inventoried, migrated, and stable: remove direct commit APIs, enforce access through the owned boundary, then delete compatibility paths. Fault-test crash, cancellation, deadlock retry, partial validation, and event publication. Stop short of a rich change-tracking Unit of Work if one explicit transaction coordinator around a few writes already preserves atomicity and no identity/change-tracking force exists. Pattern completeness is not the goal; verified transactional ownership is.
