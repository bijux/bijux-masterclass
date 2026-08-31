---
module_id: SEPAT-004
program: Software Engineering: Patterns
level: 1
module_number: 4
title: Pattern Intent and Applicability
status: complete
last_verified: 2026-08-28
---

# Pattern Intent and Applicability

## One-Page Review

### Governing question

How can a designer decide that a pattern is genuinely a candidate for a situation before investing in its implementation?

### Essential definitions

- **Intent** states the recurring problem addressed and the essential design effect produced, without fixing one implementation.
- **Applicability** is the set of situation properties under which the pattern's mechanism plausibly resolves relevant forces.
- A **precondition** must hold for the solution to operate as claimed.
- An **indication** is observable evidence that the pattern's problem or force configuration may be present.
- A **contraindication** is a situation property that makes the pattern unsafe, ineffective, or disproportionately costly.
- A **hard constraint** disqualifies any candidate that violates it; it is not a preference to average against benefits.
- A **context match** is evidence that a concrete situation corresponds to the pattern's declared context at the relevant abstraction level.
- A **candidate** has passed an applicability screen; it has not yet won comparison against simpler or competing designs.
- A **false positive** applies a pattern where its motivating forces are absent; a **false negative** rejects a useful pattern because its surface implementation looks unfamiliar.

### Central model, mechanism, or theorem

For situation (x) and pattern (\Pi), an applicability screen asks

$$
ApplicableCandidate(\Pi,x)=Pre(\Pi,x)\land ProblemMatch(\Pi,x)
\land ForceMatch(\Pi,x)\land \neg Contra(\Pi,x).
$$

Each term requires evidence and can be true, false, or unknown. Passing means “compare this pattern with alternatives,” not “implement it.” Intent guides recognition by specifying the transition the pattern seeks:

$$
intent(\Pi): (problematic\ context)\rightarrow(resulting\ design\ effect).
$$

### Critical invariants

- Intent names a problem and design effect, not a product, participant list, or promised quality slogan.
- Applicability conditions discriminate among situations; “when flexibility is needed” is too broad.
- Preconditions and hard constraints are evaluated before weighted preferences.
- Evidence comes from the present situation, not from the pattern's popularity.
- Unknown evidence remains unknown; it is not silently treated as a match.
- Surface syntax does not determine applicability; different mechanisms can realize the same intent.
- Passing the screen only admits a candidate to comparison, experiment, and consequence analysis.

### Common failures

Common failures include writing intent as “use class X,” copying catalog applicability without examining local facts, treating symptoms as root causes, converting all conditions into scores, assuming known uses guarantee a match, ignoring organizational and operational context, applying a pattern for possible future variation, and rejecting a functional or data-oriented realization because it lacks catalog-shaped classes.

### Compact example

Adapter is a candidate when an application owns a meaningful contract, a required provider is incompatible, translation can preserve needed semantics, and containing provider change matters. It is contraindicated when the “local” interface merely mirrors the provider, callers require provider-specific capabilities directly, or translation would hide essential semantics. Passing these checks does not prove Adapter is better than direct use, replacement, or a broader anti-corruption boundary.

### Connections

[SEPAT-003](003-reading-and-writing-a-pattern-form.md) locates intent and applicability in the full form. [SEPAT-005](../ROADMAP.md) deepens consequence comparison, and [SEPAT-010](../ROADMAP.md) performs final pattern selection from forces. Applicability relies on [SDDM-001's problem/solution separation](../../09-software-engineering-software-design-and-domain-modeling/modules/001-distinguishing-the-problem-domain-from-the-solution-domain.md) and on evidence practices from [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md).

## Governing Question

What evidence must be true of *this* system before a familiar pattern deserves serious consideration?

Pattern recognition is fast and useful. Experienced designers see one-to-many notification and think Observer, incompatible provider APIs and think Adapter, or varying algorithms and think Strategy. Recognition generates hypotheses. It does not decide the design.

An applicability screen slows the transition from name recognition to implementation. It recovers the pattern's intent, tests necessary context and preconditions, finds local force evidence, and searches deliberately for contraindications. The result is a candidate set small enough for consequence analysis and experiments.

## Why This Matters

Most pattern misuse is not an incorrect class diagram. It is a context error. A technically accurate Object Pool around cheap immutable objects adds synchronization and lifecycle complexity without resolving scarcity. A correct Observer implementation with a fixed subscriber set makes control less visible. A retry mechanism around a non-idempotent operation creates duplicate effects.

Applicability reasoning prevents sunk-cost bias. Before creating participants and interfaces, the team asks what present evidence justifies them. It also improves constructive disagreement: reviewers can dispute whether runtime variation exists, whether translation preserves semantics, or whether a hard latency bound disqualifies a candidate, rather than arguing that a pattern is “clean.”

Applicability evolves. A pattern can become justified after scale, variability, failure, or ownership changes. It can become unjustified when a provider is removed or variation stabilizes. Recording the conditions makes introduction and removal reviewable.

## Prerequisites and Retrieval

You should understand context, forces, solution, and consequences from SEPAT-001 through SEPAT-003. Retrieve these facts:

1. Similar code does not prove the same design problem.
2. Mandatory constraints must be satisfied before preferences are optimized.
3. Evidence can be observed, measured, inferred with uncertainty, or missing.
4. An implementation mechanism and the pattern intent it may realize are separate.
5. Anticipated change has probability, impact, and accommodation cost; it is not automatically a current force.
6. A simpler design is a candidate and must not be excluded merely because it has no pattern name.

## Learning Objectives

After completing this module, you should be able to:

- write an intent statement that combines problem and essential design effect;
- distinguish context, preconditions, indications, contraindications, and consequences;
- construct an evidence-based applicability predicate;
- handle unknown evidence explicitly;
- separate hard constraints from preferences and scoring aids;
- recognize false-positive and false-negative pattern matches;
- screen a candidate without prematurely selecting it;
- record applicability assumptions so later maintainers can reassess them.

## Core Exposition

### Intent is a recognition key

Intent is the shortest faithful statement of a pattern. A useful form is: “Address [recurring problem] by [essential relationship or effect], so that [dominant force] can be resolved, accepting [boundary if necessary].” It should be understandable without participant names, though established pattern intents sometimes use them for precision.

“Provide flexibility” is not intent because almost any abstraction can claim it. “Use interchangeable strategy objects” overfits one implementation. “Vary an algorithm independently of the clients that use it by delegating the decision to a replaceable policy role” states problem and design effect while allowing objects, functions, or modules.

Intent also defines scope. Adapter changes the relation between incompatible interfaces; it does not make incompatible semantics equivalent. Observer handles notification dependency; it does not guarantee durable delivery. Circuit Breaker suppresses likely failing calls; it does not repair the dependency. Overstated intent leads directly to overapplication.

### Context identifies the reference class

Applicability asks whether the concrete situation belongs to the class described by the pattern. Match at the relevant abstraction level. A system can have many objects without having the allocation-cost context for Flyweight. A service can have failures without the repeated remote-call and recovery-probe context for Circuit Breaker.

Context facts should be inspectable. For Strategy: how many algorithms exist, who selects them, when selection changes, and whether their state/lifecycle differs. For Observer: how many dependents exist, whether the set changes, what notification semantics are required, and how failures propagate. Replace adjectives with evidence.

### Preconditions enable the mechanism

A precondition is required for the solution to work as claimed. Retry of an effectful operation may require an idempotency key or deduplication contract. Hash-based Flyweight lookup requires stable keys and shareable intrinsic state. Optimistic locking requires a version comparison at the write authority.

Some preconditions can be created, but their creation cost belongs in evaluation. Adding stable identity, a transaction boundary, or a schema registry is not free setup. If the pattern description hides such infrastructure, expand the local applicability record.

### Indications generate hypotheses

Indications are observable symptoms: repeated switches on type, change-prone construction branches, unbounded resource growth, duplicated message processing, or coordinated edits across providers. They tell the reviewer where to investigate.

Symptoms are not proof. Repeated switches can express stable exhaustive domain cases better than polymorphism. Coordinated edits can be one coherent change, not harmful coupling. Trace the symptom to a recurring force before treating it as applicability evidence.

### Forces determine local priority

Pattern catalogs list typical forces. Local applicability requires evidence that the important ones are active and prioritized similarly. Abstract Factory is more plausible when families of products must remain compatible and switch together. If only one product varies, a creation function may suffice.

Force match is not exact identity. New contexts introduce additional forces: language tooling, team familiarity, regulatory traceability, deployment constraints, or platform costs. A pattern can remain applicable with adaptation, but its consequence profile changes.

### Contraindications deserve active search

Confirmation bias makes indications easy to see after a pattern is named. Search for facts that would defeat it. For Observer: fixed dependents, strict visible sequencing, transactional all-or-nothing behavior, or subscriber failures that must immediately abort the publisher. For Proxy: callers must reason explicitly about network latency and partial failure. For Singleton: multiple tenants or tests require isolated instances.

Contraindications vary in severity. Some are hard disqualifiers; others demand a variant or mitigation. Record which is which. “Team unfamiliarity” can be addressed through training; “would conceal a legally required approval step” may be non-negotiable.

### Unknown is a first-class result

Teams often lack evidence about change frequency, traffic distribution, failure correlation, or implementation cost. Treat the condition as unknown and define an information-gathering action: mine change history, instrument latency, prototype a boundary, or interview operators.

Unknown should not default to “build for flexibility.” That transfers uncertainty into permanent complexity. Nor should it default to rejection when migration later would be irreversible. Compare the cost of learning now, deferring, and retrofitting.

### Hard gates before weighted comparison

Security, safety, protocol, legal, and hard resource constraints can disqualify a pattern instance. Do not allow a high convenience score to compensate for violating them. First evaluate admissibility. Then compare admissible candidates across softer forces.

Numerical matrices can expose assumptions, but ratings are often ordinal and correlated. “Operability” and “debuggability” may double-count the same concern. Use scores to discover sensitivity, not declare truth.

### Applicability is not selection

Several patterns can be applicable simultaneously, and the simplest direct design can remain best. A varying creation problem may admit Factory Method, Abstract Factory, Builder, configuration data, or a creation function. Applicability creates a candidate set. Selection compares consequences, composition, implementation cost, and evidence.

Patterns can also compose. Adapter may be applicable at a provider boundary while Strategy chooses among adapters. Passing one screen does not imply the entire system should be organized around that pattern.

### Applicability has a lifecycle

Record the evidence and expiry conditions in a design decision: provider count, change rate, subscriber variability, load distribution, or failure profile. Monitor whether expected consequences materialize. If the triggering force disappears, reassess.

This turns “we use Strategy” into a falsifiable statement: “three independently evolving pricing policies are selected per contract; adding one should not change checkout orchestration.” If that variability collapses to one policy, removing the role becomes a legitimate improvement.

## Definitions and Notation

For pattern (\Pi) and situation (x), define evidence-valued predicates

$$
Pre_i(\Pi,x),Problem(\Pi,x),Force_j(\Pi,x),Contra_k(\Pi,x)
\in\{true,false,unknown\}.
$$

A hard admissibility gate is

$$
Admissible(\Pi,x)=\bigwedge_i Pre_i(\Pi,x)\land
\neg\bigvee_{k\in H}Contra_k(\Pi,x),
$$

where (H) is the set of hard contraindications. Under three-valued reasoning, any false precondition fails the gate; unknown evidence yields an unresolved gate rather than a pass.

Let (M) be locally material forces. A force match requires not merely mention but evidence that the pattern's solution decisions address them:

$$
ForceMatch(\Pi,x)=\forall f\in M,\ \exists q\in Decisions(\Pi):Supports(q,f,x).
$$

The final screen result is one of

$$
\{reject,investigate,candidate\}.
$$

`candidate` means admissible with sufficient current match; `investigate` means a material unknown remains; `reject` means the problem is absent, a required precondition fails, or a hard contraindication holds.

An intent can be represented as a scoped relation (I_\Pi:X_C\rightarrow X_{C'}), mapping a class of problematic contexts to a class of resulting contexts through the pattern mechanism. This notation expresses scope; it does not claim every application succeeds.

## Mechanisms, Invariants, or Proof Structure

### Normalize the intent

Remove product names, incidental participants, and quality slogans. State the problem and essential effect. Compare the result with the pattern's canonical sources to avoid redefining a familiar name.

### Gather situation evidence

For every context and force claim, name a source: change history, production telemetry, interface inventory, incident record, test, contract, or stakeholder decision. Mark inference and uncertainty.

### Evaluate hard gates

List preconditions and hard contraindications before preferences. If a precondition can be constructed, add its cost and ownership to the candidate. Stop a candidate that violates a mandatory constraint.

### Challenge symptom causality

For each indication, ask what alternative causes explain it. Repeated conditional logic may be a stable exhaustive domain model; high allocation may be caused by retained objects rather than object count. Confirm the causal force.

### Screen an Adapter candidate

This executable screen models explicit evidence states. It admits Adapter to comparison but deliberately does not select it.

<!-- bijux-verify: {"id":"adapter-applicability-screen","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"preconditions: pass\napplicability signals: 3/3\nhard contraindications: none\nscreen result: candidate for comparison\nselection result: not decided\n","stderr":""}} -->
```python
situation = {
    "owned_local_contract": True,
    "provider_interface_mismatch": True,
    "translation_preserves_required_semantics": True,
    "provider_change_or_replacement_matters": True,
    "callers_require_raw_provider_api": False,
}

preconditions = (
    situation["owned_local_contract"],
    situation["translation_preserves_required_semantics"],
)
signals = (
    situation["provider_interface_mismatch"],
    situation["provider_change_or_replacement_matters"],
    situation["owned_local_contract"],
)
hard_contraindications = (situation["callers_require_raw_provider_api"],)

print("preconditions:", "pass" if all(preconditions) else "fail")
print(f"applicability signals: {sum(signals)}/{len(signals)}")
print("hard contraindications:", "present" if any(hard_contraindications) else "none")
candidate = all(preconditions) and all(signals) and not any(hard_contraindications)
print("screen result:", "candidate for comparison" if candidate else "reject or investigate")
print("selection result: not decided")
```

### Search for disconfirmation

Assign a reviewer to argue for direct code or a competing pattern. Test at least one case where the candidate should be rejected. A useful screen must be capable of returning `reject`.

### Record and expire assumptions

Store context facts, evidence date, unknowns, candidate alternatives, and conditions for reassessment. Link telemetry or tests that can reveal when assumptions change.

## Alternatives and Trade-Offs

**Catalog checklist.** Fast and consistent, but generic wording can hide missing local evidence. Add system-specific facts beside every condition.

**Decision table.** Makes hard gates and combinations visible. Large tables become difficult when evidence is qualitative or conditions interact.

**Weighted matrix.** Exposes priorities and sensitivity among admissible candidates. It can create false precision and must not absorb mandatory constraints.

**Prototype or spike.** Generates evidence about feasibility, API shape, and some costs. A small prototype may omit lifecycle, scale, failure, and migration consequences.

**Change-history analysis.** Tests whether anticipated variation has actually occurred. Future contractual change can still matter even when history is stable.

**Direct implementation first.** Produces evidence and avoids speculative abstraction. It is risky when later migration would cross a public compatibility boundary or irreversible data format.

**Architecture decision record.** Captures one local applicability and selection argument. It complements rather than replaces the reusable pattern description.

## Failure Modes and Misconceptions

1. **Recognizing a pattern proves applicability.** Recognition only proposes a hypothesis.
2. **Intent is a list of participants.** Intent states problem and design effect at a reusable level.
3. **An indication is a precondition.** Symptoms prompt investigation; preconditions enable the mechanism.
4. **All conditions can be weighted.** Mandatory constraints and hard contraindications must gate first.
5. **Unknown means probably true.** Unknown requires investigation or an explicit risk decision.
6. **A known use matches the current context.** It supports feasibility under its own context, not local fit.
7. **Possible future change justifies present abstraction.** Probability, impact, retrofit cost, and reversibility must be examined.
8. **Team familiarity is irrelevant.** Cognitive and operational capability can be material forces, though they are not always hard constraints.
9. **Different syntax means a different pattern.** Functions, objects, data, or modules can realize one intent.
10. **Passing applicability means implementation should begin.** The candidate still needs alternatives, consequences, evidence, and proportionality comparison.

## Worked Examples

### Example 1

**Question:** Is Strategy applicable when an application has one tax algorithm?

**Reasoning:** One stable algorithm provides no present runtime or independent-evolution force. A function is sufficient. If jurisdictions are contractually scheduled to diverge, the team can record that evidence and the cost of later extraction, but a hypothetical possibility alone is weak.

**Conclusion:** Strategy is not currently indicated unless meaningful variation or selection exists.

### Example 2

**Question:** Does high object count make Flyweight applicable?

**Reasoning:** Measure whether memory is materially consumed by duplicated immutable intrinsic state, whether stable keys exist, and whether context-dependent extrinsic state can remain outside shared objects. If retention comes from references or mutable per-object data, Flyweight does not address the cause.

**Conclusion:** Object count is an indication; shareable duplicated state and material memory pressure establish the relevant match.

### Example 3

**Question:** A publisher has four fixed safety checks in a mandated order. Is Observer applicable?

**Reasoning:** The subscriber set does not vary, ordering must be visible, and any failure aborts the operation. Observer's decoupled registration introduces ambiguity and lifecycle state while opposing dominant forces. Direct orchestration is clearer.

**Conclusion:** Fixed, ordered, fail-fast collaboration is a contraindication for Observer in this context.

### Example 4

**Question:** When is Builder a candidate rather than a long constructor?

**Reasoning:** Builder becomes plausible when construction is staged, several valid representations share a process, optional parts create readability problems, or the final object must remain immutable while intermediate state is validated. Ten parameters alone may be better addressed by cohesive value objects or named arguments.

**Conclusion:** Construction process and invariant forces matter more than parameter count.

### Example 5

**Question:** A remote payment call times out after committing. Is Retry applicable?

**Reasoning:** Transient failure and lost responses indicate retry, but duplicate charges are a hard contraindication unless the provider supports stable idempotency keys or status reconciliation. The unknown original outcome must be resolved explicitly.

**Conclusion:** Retry remains rejected or unresolved until duplicate-effect safety is established.

### Example 6

**Question:** What does the Adapter screen prove?

**Reasoning:** It verifies the declared booleans produce two passing preconditions, three signals, no hard contraindication, and candidate status. It does not validate those booleans, compare direct provider use, or establish that translation preserves all business semantics.

**Conclusion:** Executable screening makes decision rules reproducible while evidence review and selection remain human obligations.

### Example 7

**Question:** Is a first-class function implementation evidence against Strategy?

**Reasoning:** If clients delegate a varying algorithm to a selected callable with a stable contract, the essential intent can hold without strategy classes. State, lifecycle, multiple operations, or discovery requirements may later justify objects.

**Conclusion:** Applicability follows the problem and design effect, not catalog-shaped syntax.

### Example 8

**Question:** A team wants Abstract Factory because two products exist. What else is required?

**Reasoning:** The pattern addresses families of related products that must remain compatible and vary together. Two independent products do not create that force. The team should identify family selection, compatibility invariants, and change ownership.

**Conclusion:** Product multiplicity is insufficient; coordinated family variation is the discriminating applicability condition.

### Example 9

**Question:** Can organizational context contraindicate a plugin framework?

**Reasoning:** A plugin architecture may fit runtime extension forces, yet the organization lacks version governance, isolation, signing, ownership, and support capability. These may be constructible preconditions, but until funded they make the solution operationally unsafe.

**Conclusion:** Technical fit does not erase organizational mechanisms required to sustain a pattern.

### Example 10

**Question:** When should an existing pattern instance be removed?

**Reasoning:** A service retained Strategy after five providers became one permanent internal provider. No runtime selection or independent algorithm evolution remains; the interface adds navigation and mocks without isolating change. Compatibility does not expose it publicly. Simplifying to direct logic passes current constraints.

**Conclusion:** Applicability is temporal; loss of the motivating force can justify refactoring away from the pattern.

## Cross-Program Connections

- **Programming Languages & Semantics:** intent is abstract, while applicability can depend on concrete language guarantees.
- **Object-Oriented and Functional Programming:** equivalent pattern roles can be realized through objects, functions, modules, or data.
- **Software Design & Domain Modeling:** symptoms in code must be traced to actual domain or solution pressures.
- **Software Architecture:** architectural constraints can be hard gates for lower-level pattern candidates.
- **Testing & Quality Engineering:** prototypes, contract tests, telemetry, and change tests supply applicability evidence.
- **Database Engineering:** identity, transaction, consistency, and query constraints determine persistence-pattern fit.
- **Distributed Systems:** partial failure and ambiguous outcomes create preconditions and contraindications for resilience patterns.
- **Security Engineering:** authority and trust constraints disqualify otherwise convenient mechanisms.
- **Platform Engineering:** organizational lifecycle, upgrade, and support capability shape framework applicability.
- **Engineering Management:** team cognitive load, ownership, and migration capacity are legitimate contextual forces.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/design-patterns-elements-of-reusable-object-oriented-software/P200000009480/9780321700698), Addison-Wesley, 1994, ISBN 978-0-201-63361-0. Its catalog template makes intent, motivation, and applicability distinct review surfaces.
2. The Hillside Group, [“Gang of Four Template”](https://hillside.net/index.php/gang-of-four-template), accessed 2026-08-28. Lists intent and concrete applicability situations separately from structure, implementation, and consequences.
3. Frank Buschmann, Regine Meunier, Hans Rohnert, Peter Sommerlad, and Michael Stal, *Pattern-Oriented Software Architecture, Volume 1: A System of Patterns*, Wiley, 1996, ISBN 978-0-471-95869-7. Develops context, problem, forces, solution, and consequence reasoning across architectural, design, and idiomatic scope.
4. Frank Buschmann, Kevlin Henney, and Douglas C. Schmidt, [*Pattern-Oriented Software Architecture, Volume 5: On Patterns and Pattern Languages*](https://www.oreilly.com/library/view/pattern-oriented-software/9780471486480/30_pattern-concept.html), Wiley, 2007. Critically examines intent, context, forces, evidence, pattern quality, and pattern relations.
5. Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2002, ISBN 978-0-321-12742-6. Organizes enterprise patterns around “how it works” and “when to use it,” demonstrating context-sensitive selection among alternatives.
6. Gerard Meszaros and Jim Doble, [“A Pattern Language for Pattern Writing”](https://hillside.net/index.php/a-pattern-language-for-pattern-writing), in *Pattern Languages of Program Design 3*, Addison-Wesley, 1998. Provides problem/solution summaries, indications, context, rationale, and resulting-context guidance.
7. Christopher Alexander, *The Timeless Way of Building*, Oxford University Press, 1979, ISBN 978-0-19-502402-9. Grounds applicability in resolving a system of forces wherever a context makes a pattern relevant, with local adaptation.

## Exercises

### Exercise 1

Write a one-sentence intent for Proxy that does not mention a proxy class and does not claim remote access is transparent. Then list two distinct Proxy contexts.

### Exercise 2

Change the Adapter screen so `callers_require_raw_provider_api` is true. Recompute the printed hard-contraindication and screen-result lines. Explain why a high applicability-signal count cannot override the result.

### Exercise 3

A team proposes Object Pool because constructing a value object takes 20 microseconds. Create an applicability investigation: preconditions, evidence to measure, indications, contraindications, and the direct alternative.

### Exercise 4

Compare Observer, Mediator, and direct orchestration for a checkout workflow with a fixed fraud check, optional analytics, a transactional inventory reservation, and strict audit ordering. Identify which patterns are candidates for which interactions rather than choosing one for the whole workflow.

### Exercise 5

An unfamiliar scientific platform expects user-defined analysis algorithms next year, but requirements are incomplete and the current release has one algorithm. Produce an uncertainty-aware decision: current screen status for Strategy, evidence-gathering plan, reversible design choice, hard constraints, and explicit trigger for introducing or rejecting the pattern.

## Answers to the Exercises

### Answer 1

A defensible intent is: “Stand in for another object or service to mediate access while preserving an explicitly declared client contract and making access policy or lifecycle controllable.” It avoids promising that latency, failure, identity, or location differences disappear.

Two contexts are: (1) a virtual proxy defers construction of an expensive local object until first use while callers can tolerate lazy failure; and (2) a protective proxy checks caller authority before forwarding an operation to a sensitive local capability. A remote proxy is a third context, but its contract must expose or deliberately manage network latency, partial failure, serialization, and retries.

### Answer 2

The program would print `hard contraindications: present` and `screen result: reject or investigate`; the three applicability signals remain `3/3`. A required raw provider API means the proposed local contract cannot mediate all needed behavior without leakage or loss. Because the contraindication is declared hard, signals cannot compensate. The team must narrow Adapter to only translatable capabilities, expose an explicit provider-specific boundary, or reconsider ownership of the local contract.

### Answer 3

Preconditions include expensive reusable resources, a valid reset/health check between borrowers, bounded concurrent demand, and a lifecycle that safely returns or discards instances. Measure allocation rate, construction latency distribution, total share of request time, garbage-collection or allocator pressure, concurrency, and memory retention under representative load.

The 20-microsecond observation is only an indication if construction occurs often enough to matter. Contraindications include cheap immutable values, state that cannot be reset reliably, thread affinity, security residue between borrowers, and synchronization cost exceeding construction savings. The direct alternative is ordinary construction, perhaps after removing accidental allocation or batching work. Pool only after an end-to-end benchmark shows a material budget violation and a prototype demonstrates safe lifecycle plus net benefit.

### Answer 4

Direct orchestration fits the fixed fraud check and transactional inventory reservation because ordering, failure propagation, and transaction boundaries must be visible. Mediator may be a candidate if several checkout participants coordinate bidirectionally and direct dependencies are genuinely tangled, but a single orchestrator function may already fill that role without a named object pattern.

Observer or an event callback is a candidate only for optional analytics after the authoritative transaction outcome, where analytics failure must not roll back checkout. Its applicability requires explicit event timing, payload, delivery, and loss policy. Strict audit ordering may require a direct durable write or transactional outbox rather than an in-process Observer. The correct design composes interaction-specific mechanisms instead of labeling the whole workflow with one pattern.

### Answer 5

The current Strategy screen is `investigate`, not `candidate`: one algorithm exists, runtime selection is unconfirmed, and next year's extension contract is unknown. Gather evidence by interviewing prospective users, drafting two representative algorithm interfaces, identifying required inputs/outputs/state, testing whether plugins need isolation, and estimating retrofit cost across any public data formats.

Keep the current algorithm behind one small domain operation owned by the composition boundary, but do not create a registry, plugin lifecycle, or hierarchy yet. This reversible seam limits migration without asserting variation. Hard constraints include deterministic scientific results, reproducible provenance, resource quotas, validation of untrusted algorithms, and compatibility of stored results.

Introduce Strategy when at least two independently meaningful algorithms share a stable behavioral contract and selection varies by run, user, or configuration with funded lifecycle ownership. Reject or defer it if algorithms require incompatible data models, selection remains build-time and rare, or isolation demands a separate process/service boundary rather than an in-process role. Record a review date and the exact evidence still unknown.
