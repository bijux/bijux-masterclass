---
module_id: SEPAT-010
program: Software Engineering: Patterns
level: 1
module_number: 10
title: Selecting a Pattern from Forces Rather Than Names
status: complete
last_verified: 2026-08-28
---

# Selecting a Pattern from Forces Rather Than Names

## One-Page Review

### Governing question

How can a designer move from a concrete problem and competing forces to a defensible pattern—or to a simpler non-pattern alternative—without letting familiar names predetermine the answer?

### Essential definitions

- A **force** is a contextual pressure, objective, constraint, uncertainty, or stakeholder need that shapes an acceptable solution.
- A **hard constraint** is a condition an alternative must satisfy; benefit on another criterion cannot compensate for violating it.
- A **quality-attribute scenario** operationalizes a concern through source, stimulus, environment, artifact, response, and response measure.
- A **candidate mechanism** is the causal behavior an alternative offers, independent of its catalog name or implementation syntax.
- A **consequence profile** records benefits, liabilities, assumptions, and residual risks for one alternative in one context.
- **Pareto dominance** occurs when one feasible alternative is no worse on every evaluated criterion and strictly better on at least one.
- The **Pareto frontier** is the set of feasible alternatives not dominated by another; it exposes real trade-offs rather than forcing a false total ranking.
- A **sensitivity point** is a decision or parameter whose change materially affects a quality outcome; a **trade-off point** affects multiple qualities in competing ways.
- **Robustness** is the degree to which a choice remains acceptable under plausible changes to assumptions, estimates, and scenarios.

### Central model, mechanism, or theorem

Let (A) be candidate alternatives and (H) hard constraints. First compute

$$
A_F=\{a\in A\mid h(a)=true\text{ for every }h\in H\}.
$$

For minimized consequence vector $c(a)=(c_1,\ldots,c_k)$, alternative (a) dominates (b) when

$$
c_i(a)\le c_i(b)\ \forall i
\quad\text{and}\quad
c_j(a)<c_j(b)\ \text{for some }j.
$$

Remove dominated alternatives, evaluate the remaining frontier with prioritized scenarios, uncertainty, and reversibility, then record why one mechanism fits. A pattern name labels the selected recurring relationship after this reasoning; it is not an input that bypasses it.

### Critical invariants

- Define the decision boundary and stakeholders before enumerating patterns.
- Translate vague qualities into scenarios and measurable response conditions.
- Separate hard constraints from preferences and forecasts.
- Generate alternatives at the mechanism level, including a simplest adequate baseline and “defer.”
- Evaluate every candidate against the same forces, scenarios, and evidence standards.
- Reject dominated candidates but do not manufacture a single winner when a frontier remains.
- Test sensitivity to uncertain weights, estimates, workloads, and future events.
- Record residual risk, owner, review trigger, and reversal path.

### Common failures

Common failures include starting with a catalog category, treating every requirement as equally weighted, compensating for a safety violation with convenience, comparing candidates against different scenarios, confusing desired qualities with mechanisms, using one scalar score before filtering feasibility, declaring a Pareto frontier to be indecision, ignoring team and operational forces, optimizing the happy path, and documenting only the chosen pattern rather than rejected alternatives and assumptions.

### Compact example

A pricing component needs runtime-selectable pure policies but no stateful lifecycle. Direct branching fails the runtime-selection constraint. A function table and Strategy objects both pass. Under equal change effort, the table has less allocation and conceptual cost, so it dominates objects in this context. If policies later acquire stateful lifecycle and related operations, objects become the only feasible candidate. The name Strategy follows the changed forces.

### Connections

[SEPAT-004](004-pattern-intent-and-applicability.md) tests individual applicability, [SEPAT-005](005-trade-offs-and-negative-consequences.md) supplies consequence analysis, and [SEPAT-009](009-pattern-hype-and-cargo-cult-design.md) protects selection from prestige and cargo-cult copying. The method connects to architecture scenarios in [Software Engineering: Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md), verification in [Software Engineering: Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md), and formal comparison in [Theory of Computation and Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md).

## Governing Question

What evidence-preserving procedure takes a designer from stakeholder outcomes to a mechanism-level choice while retaining trade-offs, uncertainty, and the legitimate choice of no named pattern?

Catalogs improve recall, but catalog browsing is a poor first step. A designer who begins in “Behavioral Patterns” has already framed the problem as object collaboration. The actual force may be data representation, a transaction boundary, a language feature, an organizational dependency, or a requirement that should be removed.

Force-led selection delays names until the problem has an operational shape. It filters infeasible candidates, removes strictly inferior ones, and makes the remaining judgment reviewable. It is systematic without pretending software design is fully reducible to arithmetic.

## Why This Matters

Design choices usually optimize several outcomes at once: modifiability, latency, availability, safety, confidentiality, cost, usability, delivery speed, and comprehension. These outcomes interact. A cache lowers latency but changes staleness and invalidation. Asynchrony absorbs bursts but changes ordering and failure visibility. Indirection enables substitution but increases navigation.

A name-first process hides those interactions behind a familiar diagram. A force-led process exposes which mechanism produces which consequence under which assumption. This supports graduate-level critique, production decision records, and later correction when the context changes.

The method also avoids two symmetric errors: forcing a catalog pattern when direct code is adequate and rejecting patterns merely because a small example can be coded without them. Selection compares lifecycle outcomes at the real boundary.

## Prerequisites and Retrieval

You should understand pattern form, applicability, trade-offs, evidence, basic set notation, and partial orders. Retrieve these facts:

1. A requirement such as “fast” or “flexible” is not testable until its stimulus, environment, response, and measure are stated.
2. Constraints and objectives differ: an infeasible alternative cannot win through unrelated benefits.
3. Two alternatives can be incomparable because each is better on a different criterion.
4. A pattern's mechanism may be available through functions, types, processes, protocols, or platform services.
5. Estimates and future frequencies are uncertain and should be varied, not hidden.
6. A decision can be locally rational and later become wrong as forces change.

## Learning Objectives

After completing this module, you should be able to:

- elicit forces from stakeholders, evidence, and system boundaries;
- write measurable quality-attribute scenarios;
- separate hard constraints, objectives, preferences, and uncertainty;
- generate mechanism-level alternatives without catalog anchoring;
- calculate feasibility and Pareto dominance for small decision sets;
- identify sensitivity and trade-off points;
- design prototypes and tests that discriminate among candidates;
- write a decision record with residual risks, triggers, and reversal.

## Core Exposition

### Define the decision, not the solution

State what is being decided, for whom, over what lifetime, and at what boundary. “Choose an Observer implementation” presupposes the answer. “Coordinate an accepted order with zero or more independently evolving notification consumers” preserves alternatives.

Identify decision authority and affected stakeholders. Developers, operators, security, finance, users, data owners, and regulators can experience different consequences. Missing stakeholders become missing forces.

### Elicit forces from evidence

Sources include requirements, change history, incidents, profiles, capacity tests, contracts, regulation, team topology, deployment constraints, and uncertainty. Phrase each force with provenance:

- observed: four policy additions touched twelve call sites;
- required: notification intent must survive process failure;
- measured: p99 response must remain below 80 ms at 2,000 requests/s;
- forecast: tenant count may grow from 20 to 2,000, confidence low;
- preferred: one team favors language-native tools due to on-call familiarity.

Do not merge these evidence classes into one unqualified list.

### Operationalize quality attributes

A scenario has source, stimulus, environment, artifact, response, and measure. “The system is modifiable” becomes: during normal development, a product engineer adds one policy to the pricing component; only one owned module changes; existing clients do not change; focused tests complete within five minutes.

For availability: during a regional message-broker outage, accepted medication orders retain exactly one durable notification intent; clinical ordering remains within its availability objective; queued intents reconcile within a defined recovery window.

Scenarios distinguish forces that share a name. “Performance” can mean latency, throughput, jitter, memory, cold start, or cost under a particular load.

### Classify hard constraints

Hard constraints define feasibility: legal prohibition, safety invariant, protocol compatibility, budget ceiling, language/platform limit, physical deadline, or required failure behavior. Challenge allegedly hard constraints—some are preferences with powerful sponsors—but never allow a score to compensate for a genuine violation.

Express constraints as predicates when possible. Examples: `preserves_order_identity`, `p99 <= 80 ms`, `supports_offline_operation`, or `no network dependency in control loop`.

### Generate mechanisms before names

Ask what must vary, who selects, when binding occurs, where state lives, how failures propagate, and what authority owns consistency. Generate mechanisms such as direct call, function parameter, lookup table, polymorphic object, message channel, immutable value, explicit state machine, transaction coordinator, or replicated log.

Then map mechanisms to known patterns for consequences and vocabulary. This order prevents a catalog's categories from limiting the search. Include the current design, simplest adequate alternative, composition, experiment, and deferral.

### Build a consequence matrix

Use the same rows for every candidate: each scenario response, construction effort, runtime overhead, conceptual load, test strategy, failure modes, security surface, operations, migration, compatibility, reversibility, and evidence confidence.

Cells contain reasoned consequences and provenance. “High modifiability” is too vague. “One new table entry under current stateless policies; unverified for policies with lifecycle” exposes both mechanism and limit.

### Filter, then compare

Apply hard constraints before preferences. Next remove dominated candidates. Dominance is stronger than “lower total score”: no declared criterion favors the dominated alternative.

The frontier can contain several alternatives. That is information, not failure. It reveals where stakeholder priorities, uncertainty, or a discriminating experiment is needed. A weighted sum can choose among frontier points only when scale, independence, and compensation assumptions are defensible.

### Use scenarios as tests

Walk each high-priority scenario through every candidate. Identify responsibilities, interactions, state changes, failure points, and response measures. Build a spike when an estimate controls the result: benchmark dispatch overhead, simulate queue failure, implement one policy addition, or conduct a blinded comprehension task.

Prototype the uncertain mechanism, not the entire production system. Preserve comparable baselines and record toolchain, data, workload, and validity limits.

### Find sensitivity and trade-off points

A queue capacity may strongly affect latency and loss. A cache time-to-live affects latency and staleness. A Strategy selection boundary affects modifiability and traceability. These are sensitivity points.

A decision becomes a trade-off point when improving one attribute harms another: batching raises throughput but latency; encryption protects confidentiality but consumes resources; replication raises availability but complicates consistency. Patterns organize such decisions but do not eliminate them.

### Analyze uncertainty and robustness

Vary uncertain inputs across credible ranges. If a small weight or workload change reverses the choice, the decision is fragile. Gather evidence, prefer reversibility, or delay. If one candidate remains feasible and near-best across ranges, it is robust.

Consider regret: if forecast variation does not arrive, what did the abstraction cost? If it arrives suddenly, what does delayed adoption cost? Avoid expected-value arithmetic when tail safety or legal constraints dominate.

### Decide and preserve rationale

Record selected mechanism and pattern name, forces, scenarios, constraints, alternatives, evidence, trade-offs, uncertainty, residual risks, and dissent. State a review trigger such as policy state appearing, latency exceeding a threshold, consumer count changing, or a compatibility window ending.

The record should let a future reviewer reconstruct why the decision was rational then and whether it remains rational now. “We chose Strategy for flexibility” fails that test.

## Definitions and Notation

Let forces be partitioned into hard constraints (H), evaluated criteria (C), and uncertainties (U). The feasible set is

$$
A_F=\bigcap_{h\in H}\{a\in A:h(a)=true\}.
$$

For minimized criterion vector $c(a)\in\mathbb{R}^k$, define strict Pareto dominance

$$
a\prec b
\iff
(\forall i,\ c_i(a)\le c_i(b))
\land
(\exists j,\ c_j(a)<c_j(b)).
$$

The nondominated frontier is

$$
P=\{a\in A_F:\nexists b\in A_F\text{ such that }b\prec a\}.
$$

For scenarios $Q=\{q_1,\ldots,q_m\}$, record response measure (r(a,q)) and evidence confidence (e(a,q)). A robust decision remains feasible over a declared uncertainty set $\Omega$:

$$
h(a,\omega)=true
\quad\forall h\in H,\ \forall\omega\in\Omega.
$$

This is a strong condition; when it is unattainable, state failure regions and contingency actions. Pareto analysis cannot compare omitted criteria, prove causal effects, or decide stakeholder values.

## Mechanisms, Invariants, or Proof Structure

### Frame one neutral decision statement

Name the boundary, outcome, stakeholders, lifetime, and authority without embedding a pattern name.

### Build scenarios and constraints

Operationalize the most important forces. Mark evidence provenance and distinguish non-compensable constraints.

### Enumerate diverse alternatives

Include direct, language-native, catalog, composed, platform, experimental, and deferred choices where relevant. Describe their mechanisms before labels.

### Compute feasibility and dominance

The executable example filters alternatives and computes a Pareto frontier across change effort, runtime overhead, and conceptual count. Binary capabilities are hard constraints.

<!-- bijux-verify: {"id":"feasible-pareto-selection","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"stable: feasible=direct,table,objects frontier=direct,table\nruntime: feasible=table,objects frontier=table\nstateful: feasible=objects frontier=objects\n","stderr":""}} -->
```python
alternatives = {
    "direct": {
        "costs": (5, 1, 1),
        "capabilities": {"runtime": False, "stateful": False},
    },
    "table": {
        "costs": (2, 2, 2),
        "capabilities": {"runtime": True, "stateful": False},
    },
    "objects": {
        "costs": (2, 3, 4),
        "capabilities": {"runtime": True, "stateful": True},
    },
}

contexts = {
    "stable": set(),
    "runtime": {"runtime"},
    "stateful": {"runtime", "stateful"},
}


def dominates(left, right):
    return all(a <= b for a, b in zip(left, right)) and any(
        a < b for a, b in zip(left, right)
    )


for context, required in contexts.items():
    feasible = [
        name
        for name, data in alternatives.items()
        if all(data["capabilities"][capability] for capability in required)
    ]
    frontier = [
        name
        for name in feasible
        if not any(
            other != name
            and dominates(
                alternatives[other]["costs"], alternatives[name]["costs"]
            )
            for other in feasible
        )
    ]
    print(
        f"{context}: feasible={','.join(feasible)} "
        f"frontier={','.join(frontier)}"
    )
```

In the stable context, direct and table are incomparable: direct has lower runtime/concept costs while table has lower change effort. Objects are dominated by table. Requiring runtime selection removes direct; requiring stateful policies leaves objects. These results depend entirely on the declared capabilities and cost vector.

### Evaluate the remaining frontier

Walk prioritized scenarios, seek discriminating evidence, test sensitivity, and identify residual risks. Do not silently reintroduce filtered candidates because their names are familiar.

### Record choice and change triggers

Preserve the matrix, evidence, dissent, rollback path, and events that require reevaluation. A completed decision includes how it can expire.

## Alternatives and Trade-Offs

**Informal expert judgment.** Fast and capable of integrating tacit context. It can hide assumptions, authority effects, and inconsistent comparisons.

**Catalog lookup by intent.** Efficient after the decision is well framed. Catalog categories and examples can anchor the search prematurely.

**Checklist.** Prevents omission of recurring concerns. Binary answers flatten trade-offs and can become ceremonial compliance.

**Weighted decision matrix.** Makes priorities visible and supports sensitivity analysis. It assumes scales and compensation that may not be valid.

**Pareto analysis.** Safely removes strictly inferior candidates and preserves trade-offs. It often leaves multiple frontier choices and depends on complete criteria.

**Scenario-based evaluation.** Connects qualities to concrete system responses and stakeholders. Scenario choice and analysis effort can bias results.

**Prototype or experiment.** Reduces technical uncertainty with local evidence. It may underrepresent lifecycle, scale, or rare failures.

**Defer the decision.** Preserves learning and avoids speculative structure. It can increase cost when the boundary becomes irreversible or current exposure is unsafe.

## Failure Modes and Misconceptions

1. **Start with the catalog chapter.** This constrains mechanisms before the problem is operationalized.
2. **“Flexible” is a force specification.** It lacks stimulus, response, boundary, and measure.
3. **Every force belongs in one weighted score.** Hard safety, legal, and compatibility constraints are not compensable.
4. **The lowest score is objectively best.** Criteria, scales, weights, and evidence confidence remain contextual.
5. **The Pareto frontier selects a winner.** It removes domination; stakeholder judgment or evidence resolves remaining trade-offs.
6. **More alternatives always improve analysis.** Redundant cosmetic variants consume effort; seek mechanism diversity.
7. **A benchmark settles architecture.** Workload, hardware, implementation maturity, and lifecycle effects bound the claim.
8. **Patterns guarantee quality attributes.** Mechanisms only influence outcomes under assumptions and correct implementation.
9. **Team skill is an illegitimate force.** Learnability and operational competence affect production outcomes, though skills can change.
10. **Decision records are permanent verdicts.** They preserve rationale and triggers for reevaluation.

## Worked Examples

### Example 1

**Question:** Factory Method or direct construction for a parser?

**Reasoning:** One parser, one platform, and centralized construction favor direct creation. Subclasses that must select tightly coupled product variants create a Factory Method force; external configuration may favor a creation function or registry instead.

**Conclusion:** Determine who selects and when binding occurs before naming the factory pattern.

### Example 2

**Question:** Switch, function table, or Strategy objects for pricing?

**Reasoning:** Stable branches favor direct code; stateless runtime selection makes a table feasible; cohesive state and lifecycle make objects feasible. Evaluate change touch points, observability, allocation, and comprehension under the same scenarios.

**Conclusion:** The variation mechanism follows binding time and policy semantics.

### Example 3

**Question:** Observer or explicit calls for order notifications?

**Reasoning:** Fixed mandatory ordered actions favor explicit orchestration. Independently changing optional consumers support Observer, while durable cross-process delivery requires a messaging mechanism with stronger failure semantics than in-process callbacks.

**Conclusion:** Subscriber variability does not erase ordering, durability, or authority forces.

### Example 4

**Question:** Decorator or a fixed middleware pipeline?

**Reasoning:** Per-object dynamic combinations support Decorator. One application-wide ordered chain with global policy can be clearer as explicit middleware. Validate ordering, duplicate application, error mapping, and introspection.

**Conclusion:** Composition granularity and ordering authority discriminate the alternatives.

### Example 5

**Question:** Composite or a plain recursive data type for a document tree?

**Reasoning:** Uniform operations across leaves and groups support Composite. An algebraic data type plus exhaustive recursion may provide the same mechanism with stronger closed-world checking. Frequent node variants versus operations decide the trade.

**Conclusion:** Include language-native representation in the candidate set.

### Example 6

**Question:** State objects or an enum transition table for a workflow?

**Reasoning:** A small auditable state space with data-driven transitions favors a table. State-specific cohesive behavior, guards, and lifecycle may support objects. Safety-critical workflows also require reachability and invariant analysis independent of representation.

**Conclusion:** State pattern shape is not a substitute for transition-system evidence.

### Example 7

**Question:** Adapter or Anti-Corruption Layer at a provider boundary?

**Reasoning:** A narrow interface mismatch favors Adapter. A foreign domain model with semantic translation, policy, and corruption risk needs a broader translation boundary. Compare ownership, error semantics, identity, and evolution.

**Conclusion:** Translation depth and domain protection distinguish mechanisms that look structurally similar.

### Example 8

**Question:** Cache-Aside or no cache for a product endpoint?

**Reasoning:** First operationalize latency, load, staleness, invalidation, privacy, and failure. If the database meets objectives, no cache is feasible and simpler. Otherwise prototype hit distribution and invalidation under representative workload.

**Conclusion:** A performance pattern is selected from measured bottlenecks and consistency tolerance.

### Example 9

**Question:** What does the executable Pareto example prove?

**Reasoning:** It correctly computes feasibility and dominance for three declared alternatives and vectors. It does not validate the vector values, omitted criteria, binary capability model, or transfer to another system.

**Conclusion:** Formal comparison strengthens internal consistency while evidence determines external relevance.

### Example 10

**Question:** When should a team select no pattern yet?

**Reasoning:** If candidates remain feasible but results reverse under plausible workloads, build a discriminating slice, retain a direct boundary, and set a decision date. Do not freeze an irreversible public protocol during uncertainty.

**Conclusion:** A bounded evidence-gathering decision can be more rigorous than premature selection.

## Cross-Program Connections

- **Theory of Computation and Complexity:** sets, orders, computability limits, and cost models discipline formal comparison.
- **Algorithms & Data Structures:** asymptotic and workload analysis turn performance forces into bounded claims.
- **Programming Languages:** algebraic data types, closures, traits, macros, and effects change the available mechanisms.
- **Software Design:** cohesion, coupling, information hiding, and change history generate candidate boundaries.
- **Software Architecture:** quality scenarios, sensitivity points, and trade-off points scale the method to systems.
- **Testing & Quality Engineering:** experiments and property, load, failure, and usability tests discriminate candidates.
- **Security Engineering:** threats and trust boundaries create hard constraints that convenience cannot offset.
- **Distributed Systems:** failure, ordering, consistency, and partition assumptions must be explicit.
- **Cloud Engineering:** managed-service capabilities alter feasibility, lock-in, cost, and operational ownership.
- **Engineering Management:** stakeholder values, team topology, budget, and decision authority shape the frontier.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Organizes pattern selection through intent, applicability, structure, collaborations, and consequences.
2. Frank Buschmann, Regine Meunier, Hans Rohnert, Peter Sommerlad, and Michael Stal, [*Pattern-Oriented Software Architecture, Volume 1: A System of Patterns*](https://www.wiley.com/en-us/Wiley%2BSoftware%2BPatterns%2BSeries-c-7544), Wiley, 1996, ISBN 978-0-471-95869-7. Relates architectural patterns, design patterns, and idioms through problem contexts and forces.
3. Len Bass, Paul Clements, and Rick Kazman, [*Software Architecture in Practice*, 4th ed.](https://www.pearson.com/en-us/subject-catalog/p/software-architecture-in-practice/P200000000111), Addison-Wesley, 2021. Develops quality-attribute scenarios, architectural tactics, analysis, and trade-off reasoning.
4. Rick Kazman, Mark H. Klein, Mario R. Barbacci, Thomas A. Longstaff, Howard F. Lipson, and Jeromy Carriere, [“The Architecture Tradeoff Analysis Method”](https://insights.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method-2/), Software Engineering Institute, 1998. Presents scenario-driven evaluation of interacting quality attributes and architectural trade-offs.
5. Software Engineering Institute, [“Architecture Tradeoff Analysis Method Collection”](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/), accessed 2026-08-28. Describes business drivers, utility trees, scenarios, risks, sensitivity points, and trade-off points.
6. Jeff Tyree and Art Akerman, [“Architecture Decisions: Demystifying Architecture”](https://doi.org/10.1109/MS.2005.27), *IEEE Software* 22(2), pp. 19–27, 2005. Provides a structured approach to recording architectural decisions and rationale.
7. Martin Fowler, [“Who Needs an Architect?”](https://martinfowler.com/ieeeSoftware/whoNeedsArchitect.pdf), *IEEE Software* 20(5), pp. 11–13, 2003. Connects architectural significance to shared understanding and decisions perceived as difficult to change.
8. Philippe Kruchten, [“The 4+1 View Model of Architecture”](https://doi.org/10.1109/52.469759), *IEEE Software* 12(6), pp. 42–50, 1995. Uses scenarios to relate multiple architectural views and stakeholder concerns.

## Exercises

### Exercise 1

Rewrite “choose Observer for a flexible notification system” as a neutral decision statement and three complete quality-attribute scenarios. Classify hard constraints, objectives, preferences, and forecasts.

### Exercise 2

Using the executable alternatives, add a hard constraint `latency_cost <= 2`. Recompute feasible sets and frontiers for all three contexts, and explain the stateful result.

### Exercise 3

Compare direct construction, a creation function, Factory Method, and Abstract Factory for a cross-platform document exporter. Produce mechanisms, constraints, a consequence matrix, and a Pareto argument without invented scalar weights.

### Exercise 4

A team is choosing Cache-Aside, write-through caching, or no cache for patient demographics. Design scenarios, safety/privacy constraints, a discriminating experiment, sensitivity analysis, rollback, and review triggers.

### Exercise 5

An unfamiliar autonomous rail-control system must coordinate sensor processing and actuator commands under hard real-time and fail-safe obligations. Develop a graduate-level force-led selection process for direct calls, event dispatch, and message queues, including formal constraints, adversarial schedules, evidence, dominance limits, and human review requirements.

## Answers to the Exercises

### Answer 1

Neutral statement: choose how an accepted order coordinates zero or more notification consumers over the next two years while preserving ordering, durability, privacy, evolvability, and operational recovery.

Scenario one: during normal operation, a product team adds one optional notification consumer; the order producer and existing consumers do not change; contract and integration tests complete within ten minutes. Scenario two: during broker or process failure after order acceptance, exactly one durable notification intent remains associated with the order and reconciles within five minutes of recovery without duplicate user-visible action. Scenario three: when an unauthorized tenant submits or observes a notification, enforcement denies access, emits an auditable event within one second, and exposes no patient data.

Hard constraints include accepted-order/intent atomicity, authorization, tenant isolation, bounded clinically required delivery, and identity. Objectives include change isolation, recovery time, throughput, and comprehensibility. A team preference for its current broker is not a constraint. Future consumer count is a forecast with confidence and range. Observer is one candidate mechanism; explicit orchestration, transactional outbox plus broker, and workflow coordination remain alternatives.

### Answer 2

Apply the new predicate to the second component of each cost vector. Direct latency cost is 1 and table is 2, so both pass; objects is 3 and fails. Stable feasibility becomes `direct,table` with frontier `direct,table`. Runtime feasibility becomes `table` with frontier `table`. Stateful feasibility becomes empty because the only stateful-capable alternative violates the latency constraint.

An empty feasible set is not permission to choose the least violating pattern. Reconsider the implementation estimates, optimize or redesign an object mechanism, weaken the latency bound only with authorized evidence, introduce another state representation, or declare the requirements inconsistent. Hard constraints expose the conflict.

### Answer 3

Direct construction binds one concrete exporter at the composition root. A creation function centralizes selection without subclass coupling. Factory Method lets each document-application subclass choose a product through an overridable creation step. Abstract Factory creates coherent families of exporters and related resources across platforms.

Hard constraints might require PDF and SVG output, deterministic fonts, offline use, and platform licensing. Evaluate number and coherence of product families, binding time, subclass ownership, platform variability, runtime configuration, testing, dependency direction, conceptual load, and plugin compatibility. If one exporter serves all platforms, direct creation dominates the others on concepts and is no worse on required capabilities. If runtime platform selection is required, a creation function can dominate Factory Method when subclass extension has no benefit. If exporters, fonts, color profiles, and renderers must vary as coherent platform families, Abstract Factory becomes feasible in a way the simpler candidates are not. The frontier changes with evidenced family coherence; no arbitrary weight is required to eliminate infeasible or dominated choices.

### Answer 4

Scenarios specify measured read latency and throughput by region; update-to-read staleness; emergency correction propagation; cache/database outage; unauthorized access; patient merge; deletion; and recovery. Hard constraints include correct patient identity, authorized access, bounded critical-field staleness, auditable changes, deletion propagation, and one authoritative record. Objectives include p99 latency, database load, availability, cloud cost, and operator burden.

Replay a de-identified representative trace against no cache, Cache-Aside, and write-through prototypes. Inject skew, eviction, outage, concurrent update, merge, poison entry, and region partition. Compare hit distribution, stale critical reads, invalidation delay, latency tails, cost, and recovery; one implementation team and identical data avoid an unfair baseline. Vary read/write ratio, regional delay, cache size, and critical-field staleness bounds. Roll back through routing with the database remaining authoritative; never dual-author demographics. Review when load doubles, staleness incidents occur, schema/privacy policy changes, or measured database capacity makes the cache unnecessary.

### Answer 5

Define the boundary from sampled sensor input through validated state estimate to actuator command. Hard constraints include deadline (D), worst-case execution time plus scheduling and communication bound at most (D), deterministic priority, bounded memory, fail-safe output on missed/invalid input, command freshness, authenticated code/configuration, independence required by the hazard analysis, and traceability. Throughput or extensibility cannot compensate for violating any constraint.

Direct calls minimize dispatch and queue uncertainty but couple schedule and failure. In-process event dispatch can separate handlers yet requires bounded fan-out, ordering, and execution. Message queues add buffering and temporal decoupling but introduce queueing delay, stale commands, overflow, reordering, and additional failure state. Analyze worst-case schedules, not averages: simultaneous sensor bursts, priority inversion, handler overrun, dropped/duplicated/reordered events, full queue, clock drift, partition, restart, corrupted input, and actuator timeout.

Use static timing analysis, schedulability analysis, bounded model checking where tractable, hardware-in-the-loop tests, fault injection, independent hazard analysis, and traceable requirements. Pareto dominance can remove an alternative only for modeled criteria after feasibility; it cannot certify safety, completeness of hazards, independence, or worst-case bounds. If no candidate satisfies constraints, redesign the allocation or requirements rather than score violations. Named safety, real-time, security, systems, operations, and domain authorities must review evidence; production approval cannot be inferred from this chapter or an internal software review.
