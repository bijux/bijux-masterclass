---
module_id: SEPAT-020
program: Software Engineering: Patterns
level: 1
module_number: 20
title: Comparing Creational Patterns Under Change
status: complete
last_verified: 2026-08-28
---

# Comparing Creational Patterns Under Change

## One-Page Review

### Governing question

Given concrete change scenarios and quality constraints, which creation mechanism localizes the uncertain decisions with the least lifecycle, authority, concurrency, and cognitive cost—and how will evidence trigger replacement or removal?

### Essential definitions

- A **change scenario** names a stimulus, environment, affected artifact, response, and measurable response target.
- A **creation decision** selects product type, representation, configuration, identity, scope, timing, ownership, or reuse policy.
- A **variation axis** is one independently changing creation dimension, such as storage backend or regional policy.
- A **sensitivity point** is a design decision whose small change strongly affects a quality attribute.
- A **tradeoff point** affects multiple quality attributes in opposing ways.
- **Pareto dominance** means one alternative is no worse on every evaluated criterion and strictly better on at least one.
- **regret** is loss relative to the best alternative after an uncertain scenario becomes known.
- A **fitness function** is an automated or reviewable check that detects erosion of a design constraint.
- **option value** is the benefit of preserving a low-cost future change; it is not permission to implement every speculative extension.
- **contraction** removes a pattern when its variation, lifecycle, or evidence no longer justifies the indirection.

### Central model, mechanism, or theorem

For alternatives $a\in A$, scenarios $s\in S$, evidence-based likelihood/importance weights $w_s\ge0$, and bounded consequence ratings $c(a,s)$, an illustrative expected-loss model is

$$
L(a)=\sum_{s\in S}w_sc(a,s).
$$

Do not add incomparable measurements until their scales and stakeholder meanings are defined. First remove dominated alternatives, identify hard feasibility constraints, analyze sensitivity to plausible weights, and expose worst-case regret. A numerical minimum is a decision aid, not proof: uncertain scenarios, interaction effects, tail risk, irreversible migration, safety, and organizational capability require explicit qualitative and empirical review.

### Critical invariants

- The baseline of direct construction is evaluated before adding a named pattern.
- Each candidate addresses a stated variation, identity, timing, lifecycle, or resource problem.
- Hard correctness, security, safety, and compatibility constraints filter candidates before convenience scoring.
- Costs include code, generated/runtime machinery, debugging, testing, operations, migration, and removal.
- Pattern combinations have explicit ownership; a container, factory, builder, pool, and lazy cell do not all own the same lifecycle accidentally.
- Evidence distinguishes observed, measured, inferred, assumed, and unknown claims.
- Sensitivity and adversarial scenarios accompany any weighted score.
- Every selected pattern has fitness functions, review triggers, and a contraction path.

### Common failures

Common failures include selecting from pattern names before framing the problem, rewarding hypothetical flexibility without scenarios, comparing only happy-path code size, summing ordinal scores as if they were physical quantities, hiding hard constraints inside weights, treating popularity as evidence, stacking patterns until ownership is unclear, forgetting migration/removal cost, optimizing creation while product behavior remains incompatible, using a process-local Singleton for distributed uniqueness, and interpreting one benchmark or one weighted winner as universal correctness.

### Compact example

Three alternatives—direct construction, a creation function, and Builder—receive illustrative consequence ratings under variant, optional-configuration, invalid-construction, and simple-call scenarios. One weight profile favors the creation function; a configuration-heavy profile favors Builder. The reversal is the lesson: scenario assumptions, not pattern prestige, drive selection. The numbers are reproducible but not empirical evidence.

### Connections

[SEPAT-011 through SEPAT-019](../ROADMAP.md) provide the candidate mechanisms. [SEPAT-010](010-selecting-a-pattern-from-forces-rather-than-names.md) establishes evidence-based pattern choice. Comparison under change connects to [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md), [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md), and [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md).

## Governing Question

Which construction decisions are likely or costly to change, which qualities constrain them, and what is the smallest mechanism that makes those decisions explicit, testable, and replaceable?

Creational patterns are not mutually exclusive products in a catalog. A composition root may call an Abstract Factory whose selected product uses Builder, whose expensive resources come from a pool, while optional metadata is loaded lazily. This can be coherent—or a lifecycle maze. The comparison must assign one owner to each decision.

## Why This Matters

Creation code is where environment choices, domain invariants, resource authority, and runtime lifecycle meet. Direct constructors can scatter policy; overengineered factories can scatter indirection. The right choice changes with product variants, deployment topology, regulation, workload, language features, and team capability.

Graduate-level design requires more than recalling intents. It requires framing change scenarios, rejecting infeasible alternatives, making consequences falsifiable, measuring uncertain claims, tracing ownership, and revisiting decisions as evidence changes.

## Prerequisites and Retrieval

You should understand modules 011–019, quality attributes, scenarios, Pareto reasoning, expected value, testing, and lifecycle. Retrieve these facts:

1. Constructors, static creation functions, and direct dependency injection are legitimate baselines.
2. Factory Method varies a product through an overridable creation point; Abstract Factory coordinates a product family.
3. Builder controls staged assembly; Prototype copies an exemplar graph under explicit edge policy.
4. Singleton combines cardinality and access unless deliberately separated.
5. Object Pool governs leased reuse; Lazy Initialization governs demand timing.
6. A pattern's intent says nothing about whether a specific implementation satisfies behavioral, concurrency, or operational obligations.

## Learning Objectives

After completing this module, you should be able to:

- translate anticipated change into concrete quality-attribute scenarios;
- map creation decisions to candidate mechanisms and baselines;
- eliminate infeasible and Pareto-dominated alternatives before scoring;
- build and critique a transparent consequence matrix;
- perform weight, threshold, and worst-case sensitivity analysis;
- assign lifecycle and authority ownership in combined patterns;
- design experiments and fitness functions for disputed claims;
- document selection, uncertainty, expiry, migration, and contraction.

## Core Exposition

### Frame the decision neutrally

Do not begin with “Which pattern should we use?” Begin with current construction, observed pain, likely stimuli, affected stakeholders, constraints, and desired response. A scenario such as “add a payment provider in two engineer-days without editing settlement policy” is testable; “be flexible” is not.

Record why the decision is being made now. If direct construction has no observed defect and the change is cheap, deferral can be rational.

### Establish the baseline

Write the simplest correct direct constructor or creation function. Measure its dependency count, invariant visibility, testability, startup behavior, and change diffusion. Candidate patterns must beat this baseline on relevant scenarios after their own costs.

Language features matter. Named arguments, algebraic data types, modules, traits/protocols, macros, code generation, ownership types, and standard lazy cells can provide intent without classic class structures.

### Map decisions, not names

Use this stable map:

- **constructor/creation function:** straightforward valid construction and small selection policy;
- **Factory Method:** framework/algorithm delegates one creation step to an extension subtype or hook;
- **Abstract Factory:** one selection chooses a compatible family of products;
- **Builder:** staged or readable assembly with cross-field validation and optional parts;
- **Prototype:** creation from a configured exemplar where graph identity/copy policy is known;
- **Singleton scope:** explicit one-instance cardinality in a declared boundary, usually without global lookup;
- **Object Pool:** expensive/scarce instances are leased, sanitized, validated, and bounded;
- **Dependency Injection:** a root assembles a dependency graph with explicit bindings and lifetimes;
- **Lazy Initialization:** construction is deferred under a specified concurrent failure state machine.

These solve different dimensions. Do not compare Pool against Builder as if only one may exist; decide whether either dimension exists.

### Define scenarios

A change scenario includes source/stimulus, environment, artifact, response, and measure. Examples: add one regional product family without cross-family mismatch; rotate credentials without mixed generations; introduce one optional field without invalid intermediate objects; survive a dependency outage without unbounded construction attempts.

Include operational and negative scenarios: startup failure, cancellation, partial construction, concurrent first use, rolling upgrade, invalid configuration, security revocation, shutdown, and pattern removal.

### Hard constraints first

Filter alternatives that cannot satisfy required type compatibility, domain invariant, safety property, authority boundary, licensing constraint, runtime budget, or deployment topology. Do not give a safety violation “100 points” and let convenience compensate with 101.

Unknown feasibility is not zero cost. Mark it unknown and require a spike, proof, expert review, or experiment before selection.

### Consequence matrix

For each feasible candidate, record consequence per scenario with rationale and evidence class. Use natural units where possible: changed modules, startup milliseconds, allocations, maximum live sessions, graph validation defects, or recovery time.

If ordinal ratings are unavoidable, define anchors—for example 0=no material work, 1=localized edit, 3=multi-module coordinated edit, 5=architecture migration—and keep them separate from measured quantities. A weighted sum is transparent aggregation, not scientific precision.

### Pareto and sensitivity analysis

Remove dominated alternatives. Identify sensitivity points: a Builder may win only if configuration variation is frequent; a pool may win only above a measured construction cost or under a hard resource budget.

Vary weights across credible stakeholder profiles. Compute break-even thresholds. Use minimax regret when scenario probabilities are deeply uncertain and downside matters. Report reversals rather than tuning weights to protect a favorite.

### Interaction effects

Pattern costs are not additive. DI plus Lazy can move provider failure to request time. Abstract Factory plus Builder can either separate family choice from product assembly or duplicate validation. Pool plus Singleton can clarify one pool per graph or create global hidden state.

Draw ownership: who creates, configures, publishes, lends, resets, invalidates, and closes each object? Every action has one authoritative component and observable failure path.

### Behavioral substitutability

Creational abstraction makes types constructible through one interface; it does not make products behaviorally interchangeable. Define preconditions, postconditions, invariants, errors, concurrency, performance envelope, security, and lifecycle contracts.

Contract tests help but cannot prove arbitrary future implementations. High-risk variants require independent domain and operational evidence.

### Cost of optionality

Option value depends on probability, impact, lead time, and cost to preserve the option. An interface and creation function may cheaply preserve backend substitution; a plugin platform with dynamic loading, sandboxing, compatibility, signing, and operations may cost more than a later migration.

Prefer reversible decisions and evolutionary seams. Record the earliest evidence that would justify more machinery.

### Experiments

Turn disputed claims into tests: benchmark direct allocation versus pool under representative contention; run mutation/alias tests for Prototype; model-check lazy state transitions; compile or start the production DI graph; simulate variant additions; fault-inject factory startup and cleanup.

Predefine workload, environment, metric, acceptance threshold, repetitions, and interpretation. Retain raw evidence. A successful experiment supports only the tested scope.

### Decision record

Record context, scenarios, constraints, alternatives, evidence, matrix, sensitivity, decision, ownership, consequences, implementation plan, fitness functions, expiry/review date, and supersession path.

Write rejected alternatives fairly. Future readers need to know which assumption changed before reopening the choice.

### Fitness and contraction

Examples of fitness functions include forbidden global access, exactly one production binding per key, no direct long-to-short scope edge, pool live count below budget, Builder cross-field property tests, Prototype ownership policy coverage, and lazy essential-path warm-up before readiness.

Define contraction triggers: only one stable product remains; optional configuration disappears; construction becomes cheap; exemplars no longer exist; runtime platform provides the mechanism; plugin ecosystem closes; or indirection costs exceed change benefit. Removing a pattern is successful evolution, not failure.

## Definitions and Notation

Let alternatives be $A$, scenarios $S$, and criteria $Q$. Feasibility predicate $F(a)$ is true only if hard constraints are supported by evidence. Let $c_q(a,s)$ be consequence in a defined scale and $w_{s,q}$ an explicitly justified weight.

$$
L(a)=\sum_{s\in S}\sum_{q\in Q}w_{s,q}c_q(a,s),\qquad a\in\{a:F(a)\}.
$$

Alternative $a$ dominates $b$ when every evaluated consequence is no worse and at least one is better. Scenario regret is

$$
R(a,s)=c(a,s)-\min_{b\in A}c(b,s),
$$

after consequences are placed on one defensible scale. Minimax-regret selection minimizes $\max_sR(a,s)$. Let $E(x)\in\{observed,measured,inferred,assumed,unknown\}$ classify each consequential claim.

## Mechanisms, Invariants, or Proof Structure

### Decision procedure

1. Freeze the decision statement and baseline.
2. Elicit scenarios and hard constraints from affected stakeholders.
3. Map each creation decision to the smallest candidate mechanisms.
4. Reject infeasible alternatives and separate unknowns.
5. Record consequences and evidence without aggregation.
6. Remove dominated alternatives.
7. Aggregate only defined comparable scales.
8. Vary weights, thresholds, and adversarial scenarios.
9. Run targeted experiments for sensitive assumptions.
10. Select with ownership, fitness, expiry, and contraction rules.

### Conditional correctness

If the candidate set contains the relevant alternatives, hard constraints are correctly classified, consequence scales validly represent stakeholder loss, weights match the selected decision context, and interaction effects are included, minimizing $L$ selects the minimum modeled weighted loss. Those premises are rarely fully knowable; therefore the result is conditional and must be accompanied by sensitivity and qualitative review.

### Executable illustrative matrix

<!-- bijux-verify: {"id":"creational-sensitivity-matrix","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"baseline-best=factory:26\nconfig-heavy-best=builder:18\nselection-reversed=True\n","stderr":""}} -->
```python
alternatives = {
    "direct": (5, 4, 3, 1),
    "factory": (1, 3, 1, 2),
    "builder": (3, 1, 1, 4),
}

def evaluate(weights):
    scores = {}
    for name, consequences in alternatives.items():
        scores[name] = sum(
            weight * consequence
            for weight, consequence in zip(weights, consequences)
        )
    return min(scores, key=lambda name: (scores[name], name)), scores


baseline_name, baseline_scores = evaluate((5, 4, 5, 2))
config_name, config_scores = evaluate((1, 6, 5, 1))

print(f"baseline-best={baseline_name}:{baseline_scores[baseline_name]}")
print(f"config-heavy-best={config_name}:{config_scores[config_name]}")
print(f"selection-reversed={baseline_name != config_name}")
```

Independent recomputation: Factory scores $5+12+5+4=26$ in the baseline profile. Builder scores $3+6+5+4=18$ in the configuration-heavy profile. The run proves deterministic arithmetic for invented ordinal inputs only. It does not validate the scales, scenarios, alternatives, weights, pattern implementations, or any production selection.

## Alternatives and Trade-Offs

**Direct construction** minimizes machinery and debugging distance. Its cost rises when policy and variants scatter across consumers.

**Creation functions/simple factories** centralize modest selection and naming with low commitment. They are often the best first seam.

**Factory Method** fits framework extension at one creation hook but couples variability to inheritance/overrides.

**Abstract Factory** preserves family compatibility but can make adding a new product kind expensive across every family.

**Builder** clarifies complex assembly and validation but may duplicate the product API and encourage invalid intermediate builder state.

**Prototype** makes exemplar variation cheap but introduces graph-copy, identity, provenance, and resource policy.

**Singleton scope** enforces cardinality locally but global access hides dependencies; distributed uniqueness needs coordination.

**Object Pool** amortizes or bounds resources but adds lease, sanitation, queueing, and shutdown complexity.

**Dependency Injection** centralizes graph policy but can become container opacity and lifecycle error.

**Lazy Initialization** avoids unused work but moves latency/failure to demand and adds concurrency/invalidation state.

The correct answer may be one mechanism, a carefully owned combination, or no named pattern.

## Failure Modes and Misconceptions

- **“The catalog is the candidate set.”** Language and domain-specific baselines may be better.
- **“More patterns mean more flexibility.”** Interaction and ownership costs can reduce changeability.
- **“Weighted score is objective.”** Inputs encode judgments and evidence quality.
- **“Hard constraints can be heavily weighted.”** Infeasible candidates should be filtered.
- **“One winner applies to the whole system.”** Different bounded contexts have different scenarios.
- **“Factory implies substitutability.”** Construction compatibility is not behavioral compatibility.
- **“Benchmark victory proves architecture.”** It supports one workload and environment.
- **“Unknown equals average.”** Unknown needs evidence or conservative treatment.
- **“A decision record freezes design.”** Expiry and changed assumptions invite review.
- **“Removing a pattern admits failure.”** Contraction restores simplicity when variation disappears.

## Worked Examples

### Example 1

A stable immutable coordinate has two required values. Direct construction with validation is clearer than Builder or factory hierarchy. **Conclusion:** The baseline wins when variation and lifecycle are trivial.

### Example 2

A parser selects JSON or CSV from a trusted enum. A creation function localizes the small choice; a plugin system is deferred until third-party runtime extension is real. **Conclusion:** Preserve a cheap seam without buying speculative infrastructure.

### Example 3

A cross-platform UI must create mutually compatible window, menu, and input products. Abstract Factory is selected after a mismatch scenario and family-level contract tests are defined. **Conclusion:** Family coherence, not product count, motivates the pattern.

### Example 4

An immutable deployment request has 22 optional fields and cross-field rules. Builder wins the configuration-heavy profile, terminates in one validation boundary, and is property-tested. **Conclusion:** Staged assembly is justified by configuration semantics.

### Example 5

Simulation trials differ slightly from calibrated exemplar graphs. Prototype is chosen only after owned/shared/external edge policy and identity regeneration are explicit. **Conclusion:** Exemplar variation must pay for copy complexity.

### Example 6

A service needs one metrics registry per application graph. DI creates and shares it explicitly; a global Singleton accessor is rejected. **Conclusion:** Combine cardinality with visible access policy.

### Example 7

Database connections are scarce and expensive. A root-owned bounded pool is selected from measured acquisition cost and server capacity; Builder is separately used for immutable query options. **Conclusion:** Orthogonal creation dimensions may justify an owned combination.

### Example 8

A rarely used signed export engine takes 400 ms to load. Lazy initialization wins only after an explicit async load API, failure caching by artifact generation, bounded warming, and shutdown ownership are specified. **Conclusion:** Timing policy carries lifecycle obligations.

### Example 9

A runtime DI container and reflection add startup/debugging cost while the graph becomes static. Generated/manual composition replaces it without changing constructor injection. **Conclusion:** Preserve the architectural relation while contracting machinery.

### Example 10

A rail-signaling vendor proposes Abstract Factory for interlocking families, pooled command channels, and lazy route tables. Safety analysis first filters any design lacking fenced authority, fail-safe local invariants, bounded timing, and certified compatibility. **Conclusion:** Pattern comparison begins after—not instead of—system safety feasibility.

## Cross-Program Connections

- **Software Design and Domain Modeling:** information hiding and bounded contexts determine where creation decisions belong.
- **Software Architecture:** quality scenarios, sensitivity, tradeoff points, and decision records govern system-level choice.
- **Testing and Quality Engineering:** contracts, properties, mutation, concurrency, fault, and graph tests provide distinct evidence.
- **Performance Engineering:** benchmarks, distributions, queueing, allocation, and sensitivity support disputed cost claims.
- **Security Engineering:** factories and containers allocate capabilities; hard authority constraints precede convenience.
- **Reliability Engineering:** startup, retry, overload, readiness, drain, and rollback are creation consequences.
- **Distributed Systems:** process-local patterns interact with replicas, coordination, generations, and fleet storms.
- **Programming Languages:** type systems, ownership, modules, metaprogramming, and standard primitives reshape implementations.
- **Systems Engineering:** hazard, traceability, human authority, and real-time constraints define feasibility.
- **Engineering Management:** organizational ownership and review capability affect lifecycle and option cost.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Canonical intents, structures, collaborations, and consequences of GoF creational patterns.
2. David L. Parnas, “On the Criteria To Be Used in Decomposing Systems into Modules,” *Communications of the ACM* 15(12), 1972, pp. 1053–1058, DOI 10.1145/361598.361623. Establishes change-oriented information hiding as a modularization criterion.
3. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, fourth edition, Addison-Wesley, 2021, ISBN 978-0-13-688609-9. Develops quality-attribute scenarios, tactics, tradeoffs, and architecture evaluation.
4. CMU Software Engineering Institute, [“The Architecture Tradeoff Analysis Method”](https://insights.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method-2/), accessed 2026-08-28. Provides a structured method for risks, sensitivity points, and tradeoffs across competing quality attributes.
5. Martin Fowler, [“Inversion of Control Containers and the Dependency Injection Pattern”](https://martinfowler.com/articles/injection.html), 2004, accessed 2026-08-28. Compares injection and Service Locator and emphasizes separating configuration from use.
6. Michael Nygard, *Release It!*, second edition, Pragmatic Bookshelf, 2018, ISBN 978-1-68050-239-8. Provides operational stability, timeout, bulkhead, circuit-breaker, and capacity consequences relevant to creation choices.
7. Neal Ford, Rebecca Parsons, and Patrick Kua, *Building Evolutionary Architectures*, second edition, O'Reilly, 2022, ISBN 978-1-4920-9311-1. Develops fitness functions and guided incremental architectural change.

## Exercises

### Exercise 1

Recompute every score in the executable matrix, identify its decision reversal, and critique at least eight validity threats. Add a direct-construction-friendly profile without claiming the profile is empirical.

### Exercise 2

For a document renderer with three output families, complex per-document options, expensive reusable font engines, and a rarely used signed-export feature, assign each creation decision to the smallest mechanism and draw lifecycle ownership.

### Exercise 3

Compare direct creation function, Abstract Factory, and plugin registry for adding storage backends. Define scenarios, hard constraints, evidence classes, experiments, sensitivity, fitness functions, and contraction triggers.

### Exercise 4

A system currently combines a global Singleton container, lazy providers, and a connection pool. Plan an incremental redesign that makes dependencies, scope, failure timing, capacity, and shutdown explicit while preserving service.

### Exercise 5

An unfamiliar railway interlocking platform asks you to choose creational patterns for regional variants, command-channel reuse, and route-table initialization. Produce a graduate-level decision and evidence plan without making a safety claim.

## Answers to the Exercises

### Answer 1

Baseline weights `(5,4,5,2)` yield: direct $25+16+15+2=58$, factory $5+12+5+4=26$, Builder $15+4+5+8=32$; factory wins. Configuration-heavy `(1,6,5,1)` yields direct $5+24+15+1=45$, factory $1+18+5+2=26$, Builder $3+6+5+4=18$; Builder wins.

Threats include invented alternatives, omitted combinations, vague scenario definitions, ordinal multiplication, unjustified interval assumptions, arbitrary weights, correlated scenarios, missing interaction costs, missing migration/removal cost, no uncertainty ranges, stakeholder omission, hard constraints hidden as consequences, no evidence quality adjustment, and winner sensitivity. A direct-friendly illustrative profile `(1,1,1,8)` yields direct 20, factory 21, and Builder 37. It demonstrates tunability, not real preference. The decision record must expose all inputs and use measured natural units where possible.

### Answer 2

Use an Abstract Factory only for the coherent output family—page, font mapping, and graphics backend—if cross-family mixing is invalid. Use Builder for immutable per-document options and cross-field validation. The root owns a bounded Object Pool of expensive font-engine sessions if measurement and licensing/resource budgets justify reuse; leases never enter the document model. Use an explicit lazy asynchronous provider for signed export only if use is rare, with artifact/key generation, failure policy, warm option, and close ownership. DI/manual composition at the executable root selects the family, builds one pool, and supplies narrow capabilities.

Ownership is: root creates/configures/starts/closes family factory, pool, and lazy export cell; family factory creates compatible renderer products but does not close root resources; Builder creates one validated document request; pool creates/lends/resets/evicts font sessions; lease holder returns them; lazy cell initializes/publishes/closes the signed exporter. Test family compatibility, Builder properties, pool capacity/sanitation/failure, lazy single-flight/generation, and reverse-order shutdown. Do not add Prototype or Singleton unless an independent exemplar/cardinality problem appears.

### Answer 3

Scenarios include adding a compile-time internal backend, adding a third-party runtime backend, rotating credentials, preserving transaction/error semantics, deploying incompatible plugin versions, startup under missing backend, sandbox escape, and removing a backend. Hard constraints include data integrity, authorization, supported consistency, secret isolation, signed/allowlisted plugins if dynamic, bounded startup/resources, and schema compatibility.

A creation function is baseline and likely wins for a few internally deployed backends. Abstract Factory is relevant if each backend supplies a coherent family such as connection, transaction, migration, and query-dialect products. A registry is relevant only for runtime extension, and it incurs discovery, versioning, signing, isolation, collision, unload, and operational costs. Classify actual change history as observed, benchmark/startup results as measured, design consequences as inferred, future ecosystem likelihood as assumed, and untested isolation as unknown.

Experiments implement one representative backend under each feasible seam, run shared behavioral/transaction/fault contracts, measure changed modules/build/startup, and threat-model dynamic loading. Sensitivity varies backend frequency and third-party need. Fitness checks exactly one binding per backend key, family compatibility, contract suite, secret authority, plugin provenance, and resource closure. Contract to a creation function when runtime extension disappears; contract Abstract Factory if only one product kind remains; remove unused registry machinery promptly.

### Answer 4

Inventory every container lookup, lazy provider, resource, scope, first-use effect, and shutdown path. Freeze new locator calls. Establish one composition root that initially adapts the existing container. Extract one vertical slice: add constructor/parameter dependencies, create explicit graph scopes, and remove its locator keys. Repeat leaf-to-root with contract and graph tests; do not introduce another general registry.

Separate lazy behavior: required clients initialize before readiness; truly optional expensive features receive explicit async providers with single-flight, failure, deadline, generation, and close policy. Keep the connection pool root-owned and hard-bounded; specify lease, reset, validation, timeout, cancellation, metrics, and drain. Replace global access with one injected pool instance per application graph. Startup records owned resources and rolls back in reverse; shutdown stops consumers, drains leases/lazy attempts, and closes dependencies. Roll out graph generations with capacity for overlap, observe lookup count until zero, delete the container adapter, and contract any lazy/pool mechanism whose measured rationale disappears.

### Answer 5

Begin with hazards and domain decisions, not names. Regional variants may justify a statically selected, versioned family factory only if it prevents incompatible interlocking, route, signal-aspect, and device-protocol components. Command channels may be pre-established or pooled only under a safety-owned subsystem with authenticated endpoint identity, exclusive/declared sharing, state sanitation, bounded capacity/timing, health semantics, epoch fencing, and deterministic drain. Required route tables must be authenticated, validated, internally consistent, and ready before traffic control; first-command lazy initialization is infeasible. A generation mechanism can build offline, validate, atomically publish at a safe operational boundary, pin old readers, and retire safely.

Hard constraints include fail-safe movement authority, route conflict/occupancy invariants, stale-authority rejection, bounded worst-case timing, independent local interlocks, configuration provenance, cybersecurity, and safe degraded states. Evidence includes requirements traceability, formal/state/protocol analysis where tractable, independent numerical and proof review, worst-case timing, static analysis, code review, family compatibility contracts, model checking, simulation, hardware-in-the-loop, network/partition/replay/restart fault injection, endurance, operational drills, human-factors assessment, and controlled certification evidence. Sensitivity considers region count, change frequency, resource limits, latency, failure recovery, and fleet topology, but no weighted score may override a safety constraint.

Named signaling/domain, railway systems, controls, real-time, functional-safety, cybersecurity, human-factors, operations, maintainability, independent verification, quality, and regulatory/certification authorities must review and approve. Record assumptions, ownership, fitness functions, change triggers, and fallback/contraction. This repository chapter, matrix, or pattern selection proves no railway safety or deployment suitability.
