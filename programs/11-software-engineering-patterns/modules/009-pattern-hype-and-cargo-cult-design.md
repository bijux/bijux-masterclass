---
module_id: SEPAT-009
program: Software Engineering: Patterns
level: 1
module_number: 9
title: Pattern Hype and Cargo-Cult Design
status: complete
last_verified: 2026-08-28
---

# Pattern Hype and Cargo-Cult Design

## One-Page Review

### Governing question

How can a team use pattern knowledge without copying prestigious structures whose forces, mechanisms, and consequences do not fit its system?

### Essential definitions

- **Pattern hype** is confidence in a pattern that exceeds the quality or relevance of the supporting evidence.
- **Cargo-cult design** copies a solution's visible form while omitting, misunderstanding, or lacking the forces and causal mechanism that made the original useful.
- **Ceremonial patterning** adds named roles mainly to signal sophistication, conformity, or architectural legitimacy.
- **Premature generalization** creates a variation mechanism before evidence identifies what varies and along which stable dimension.
- **Pattern matching by name** moves directly from a familiar symptom or noun to a catalog label without comparing forces and alternatives.
- A **mechanism claim** explains how a collaboration is expected to change an outcome under stated assumptions.
- A **disconfirming condition** states observable evidence that would weaken or reverse a design decision.
- An **adoption margin** is the estimated local benefit of a candidate over the simplest adequate alternative after costs and uncertainty are included.
- **Option value** is the value of retaining a reversible future choice; it is not the value of implementing every anticipated choice now.

### Central model, mechanism, or theorem

For candidate design (p), context (x), evidence (E), and explicit force set (F), use a comparative decision model

$$
M(p\mid x,F,E)=B(p\mid x,F,E)-C(p\mid x,F,E)-U(p\mid x,E).
$$

(B) is expected benefit, (C) is implementation and lifecycle cost, and (U) is an uncertainty allowance. Adopt (p) only when it has a defensible positive margin over a simpler alternative, not merely a positive score in isolation. The numbers may be ordinal decision aids; they are not universal measurements. Record assumptions, predicted observations, review date, and removal triggers.

### Critical invariants

- Begin with an observed recurring problem, not a desired pattern name.
- Connect every introduced role to a force and a causal mechanism.
- Compare against the simplest adequate design and at least one relevant alternative.
- Distinguish local measurements, published empirical evidence, expert judgment, and speculation.
- Include construction, comprehension, testing, operation, migration, and removal costs.
- State disconfirming evidence and an owner or review event.
- Do not infer quality from pattern count, diagram resemblance, or vocabulary density.
- Preserve reversibility until the force and mechanism are demonstrated.

### Common failures

Common failures include choosing by catalog familiarity, equating more interfaces with lower coupling, implementing anticipated variation that never arrives, reproducing another company's scale architecture, converting every dependency into a factory or service locator, treating annotations as evidence of separation, counting patterns as a quality metric, using a weighted score to hide assumptions, and retaining failed abstractions because removing them would admit error.

### Compact example

A service builds one immutable formatter with a stable constructor. A team proposes Factory, Registry, Strategy, and Plugin roles because “formatting changes.” History shows only literal template edits, not alternative algorithms or runtime selection. Direct construction plus a pure formatting function is the simpler adequate design. Record triggers—multiple independently deployed formats or runtime selection—and defer the roles until one appears.

### Connections

[SEPAT-004](004-pattern-intent-and-applicability.md) establishes applicability; [SEPAT-005](005-trade-offs-and-negative-consequences.md) makes liabilities explicit; [SEPAT-008](008-refactoring-toward-and-away-from-patterns.md) supplies a reversible response when evidence changes. [SEPAT-010](../ROADMAP.md) develops force-led selection. The evidence discipline connects to [Software Engineering: Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) and architectural governance to [Software Engineering: Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md).

## Governing Question

When does pattern literacy improve judgment, and when does it substitute recognizable form for causal reasoning?

Patterns compress experience. That compression is useful only when the reader reconstructs the context, forces, mechanism, and consequences. Copying class names or diagram topology does not copy the conditions that made a solution work. A technically correct implementation of Strategy, Visitor, CQRS, or Microservices can therefore be a poor design.

The corrective is not pattern rejection. “Never use patterns” is another context-free slogan. The engineering task is comparative: identify the decision, establish evidence, choose the least costly structure that addresses current forces, and make the choice revisable.

## Why This Matters

Hype changes the burden of proof. A fashionable pattern is treated as a default, while a direct design must defend its simplicity. This reverses sound reasoning. Every additional role consumes naming, navigation, testing, runtime, ownership, and migration capacity, whether or not the intended benefit appears.

Cargo-cult design is especially costly at system scale. A company may copy event sourcing, service meshes, or dozens of microservices from an organization with different traffic, regulation, staffing, deployment, and failure boundaries. The copied topology introduces real distributed-state and operational obligations while the copied rationale remains imaginary.

Patterns also create social incentives. Familiar names accelerate communication, but diagrams rich in canonical roles can signal expertise independent of fitness. Review practices must reward explicit forces, alternatives, evidence, and deletion criteria rather than pattern density.

## Prerequisites and Retrieval

You should understand pattern form, intent, applicability, trade-offs, composition, and refactoring. Retrieve these facts:

1. A pattern describes a recurring problem and a reusable solution relationship, not mandatory source code.
2. Applicability and consequences are part of a pattern, not optional commentary.
3. The same structure can have different effects under different workload, team, language, and deployment conditions.
4. An abstraction lowers one kind of coupling by introducing another dependency and another concept.
5. Tests and metrics are evidence for bounded claims; neither automatically explains causality.
6. Reversible delay can preserve option value without building speculative infrastructure.

## Learning Objectives

After completing this module, you should be able to:

- distinguish pattern use, pattern hype, cargo-cult copying, and deliberate experimentation;
- trace pattern roles to observed forces and mechanisms;
- compare a pattern with the simplest adequate alternative;
- write measurable predictions and disconfirming conditions;
- build a transparent force-evidence matrix without laundering judgment into arithmetic;
- identify social and organizational drivers of ceremonial patterning;
- design a bounded trial with removal and review criteria;
- challenge overengineering without replacing analysis with anti-pattern dogma.

## Core Exposition

### Recognition is a hypothesis

Seeing repeated conditionals and saying “Strategy” is useful hypothesis generation. It is not a decision. The conditionals may vary together, remain stable, or encode validation rather than algorithms. Inspect change history, ownership, state, performance, and client needs before selecting the mechanism.

Pattern fluency increases the number of hypotheses available. It can also increase false positives: once a designer knows a form, ordinary code starts to resemble its problem statement. Treat recognition as the start of inquiry.

### Form without mechanism

Cargo-cult design preserves visible form but loses causal content. An interface plus three implementations resembles Strategy. It delivers strategic substitution only if clients use a stable policy contract and an appropriate selection authority. If clients type-check concrete implementations or one branch remains privileged, the roles do not provide the claimed decoupling.

Ask a counterfactual question: if this role were removed, which predicted outcome would worsen, through what path? If no answer is observable, the role may be ceremonial.

### Hype amplifiers

Several processes amplify weak claims:

- **authority transfer:** success by a respected author or company is transferred to a different context;
- **survivorship bias:** published successes are visible while abandoned implementations are not;
- **measurement substitution:** pattern count, interface count, or diagram conformity replaces change and outcome evidence;
- **tool lock-in:** a framework makes one structure cheap to generate, hiding its lifecycle costs;
- **vocabulary prestige:** canonical names make a proposal sound reviewed before it is analyzed;
- **escalation of commitment:** prior migration cost becomes a reason to retain a harmful design;
- **resume architecture:** technology or patterns are selected for novelty rather than system outcomes.

These are risk factors, not diagnoses of intent. Review the artifact and evidence, not a colleague's motives.

### Evidence ladder

Pattern claims can rest on different evidence:

1. **Analogy:** another design used the pattern.
2. **Mechanistic argument:** roles plausibly address stated forces.
3. **Repository evidence:** changes, incidents, dependencies, or measurements demonstrate the force locally.
4. **Comparative evidence:** alternatives are evaluated against the same scenarios and criteria.
5. **Operational evidence:** the deployed design changes predicted outcomes without unacceptable regressions.
6. **Replicated evidence:** similar effects appear in sufficiently comparable contexts.

Higher rungs usually support stronger claims, but mechanistic relevance remains necessary. A benchmark on unlike workloads can be weaker than careful local analysis. Published research on pattern quality reports heterogeneous and often inconclusive effects; it does not license universal benefit or universal rejection.

### The simplest adequate alternative

The comparison baseline is not “do nothing badly.” It is the smallest design that satisfies current requirements with acceptable risk. For Strategy, it may be a function parameter or table. For Abstract Factory, direct construction at a composition root may suffice. For Observer, explicit ordered calls may be clearer when participants are fixed.

Simplicity includes future change cost, not just lines of code. A direct design that scatters a volatile rule across twenty sites is not simple. Conversely, a framework-generated hierarchy with few handwritten lines can still be conceptually and operationally complex.

### Decision records that can be wrong

A useful decision record contains:

- context and decision boundary;
- observed forces with provenance;
- candidate mechanisms and alternatives;
- assumptions and excluded concerns;
- predicted measurable outcomes;
- expected construction and lifecycle costs;
- disconfirming evidence and expiry or review event;
- migration, rollback, and removal path;
- owner and evidence links.

Writing only reasons for adoption creates advocacy, not a decision record. A falsifiable record makes reversal an expected engineering response rather than a loss of status.

### Force-evidence matrices

A matrix can expose reasoning. Rows are forces such as policy volatility, runtime selection, stateful lifecycle, latency, team ownership, and compatibility. Columns are alternatives. Cells contain evidence-linked effects, not labels such as “good” and “bad.”

Weights and scores can summarize, but they are sensitive to scale and assumptions. Report raw criteria, ties, and sensitivity. Never convert an invented precision such as 7.3 into a claim that one design is scientifically superior.

### Delay and option value

YAGNI rejects building functionality merely because it might be needed. It does not forbid preparing low-cost seams or making irreversible choices carefully. Delay can be active: keep construction centralized, add characterization tests, monitor variation, and record a trigger.

An option has value when it preserves a meaningful future choice at lower cost than committing now. A generic plugin platform can destroy option value by fixing the wrong extension model. Small reversible boundaries often preserve more possibilities.

### Bounded experiments

When forces are plausible but evidence is weak, run a bounded trial. Choose one representative slice, define baseline and success measures, cap time and scope, preserve rollback, and schedule a decision. Measure outcomes linked to the mechanism: change lead time, defect escape, onboarding comprehension, memory, latency, failure isolation, or deployment independence.

Do not use implementation completion as the success measure. “We deployed CQRS” says nothing about whether read/write independence improved enough to justify duplication and consistency costs.

### De-adoption is part of governance

Patterns need exit conditions. If runtime selection never occurs, policy objects may collapse to functions. If independently deployable services always change together, boundaries may be merged. If an event log cannot meet privacy deletion obligations, the persistence model may need replacement.

Track predicted outcomes after adoption. At a review event, retain, adapt, remove, or gather more evidence. Avoid sunk-cost reasoning. A well-documented removal improves organizational knowledge because it narrows applicability.

### Socially safe review

Pattern challenges can become status contests. Review with neutral questions: What changed repeatedly? Which force requires this role? What is the direct alternative? What observation would change the decision? Who owns the added runtime or conceptual surface?

Permit experiments without granting indefinite permanence. Credit designers for deleting unsupported structures. This makes evidence correction psychologically and operationally feasible.

## Definitions and Notation

Let $A=\{a_0,a_1,\ldots,a_n\}$ be alternatives, where (a_0) is the simplest adequate baseline. Let $F=\{f_1,\ldots,f_m\}$ be forces with evidence records (E_i). A transparent ordinal model is

$$
S(a)=\sum_{i=1}^{m} w_i r_{ia}-K(a)-U(a),
$$

where (w_i) is declared importance, (r_{ia}) is the alternative's supported response to force (i), (K) is lifecycle cost, and (U) is uncertainty. The adoption margin is

$$
\Delta(a)=S(a)-S(a_0).
$$

The decision rule is conditional, not a theorem of design quality:

$$
adopt(a)\text{ only if }\Delta(a)>\tau
\quad\text{and hard constraints hold.}
$$

Threshold $\tau$ reflects migration risk and consequence severity. Scores support comparison and sensitivity analysis; they do not establish causal effects. A pattern claim should also identify

$$
(F,M,P,D),
$$

where (F) is observed forces, (M) the proposed mechanism, (P) predicted observations, and (D) disconfirming observations. A copied form with no credible (F) or (M) is cargo-cult risk even if its implementation is canonical.

## Mechanisms, Invariants, or Proof Structure

### Establish the baseline

Specify the current design, the simplest adequate alternative, and current outcome measurements. Do not compare a polished pattern to a deliberately neglected baseline.

### Trace forces to evidence

For each force, cite change history, incidents, workload measurements, contract needs, team topology, regulation, or explicit uncertainty. Separate current fact from forecast.

### Explain the causal chain

For every role, write “role enables mechanism; under assumption; predicted outcome changes.” Remove roles with no chain. Check whether language or platform features supply the mechanism more directly.

### Compare total obligations

Include teaching, navigation, tests, configuration, runtime failure, observability, deployment, data migration, compatibility, security, and later removal. Count responsibility, not merely source lines.

### Test a transparent decision model

The following executable model selects among a direct branch, a function table, and stateful strategy objects in three declared contexts. Its integer weights are pedagogical assumptions, not empirical constants.

<!-- bijux-verify: {"id":"force-evidence-selection","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"stable: direct score=-1\nvariable: table score=9\nstateful: objects score=15\n","stderr":""}} -->
```python
alternatives = {
    "direct": {"variation": 0, "runtime": 0, "state": 0, "cost": 1},
    "table": {"variation": 2, "runtime": 2, "state": 0, "cost": 3},
    "objects": {"variation": 2, "runtime": 2, "state": 3, "cost": 6},
}

contexts = {
    "stable": {"variation": 0, "runtime": 0, "state": 0},
    "variable": {"variation": 3, "runtime": 3, "state": 0},
    "stateful": {"variation": 3, "runtime": 3, "state": 3},
}


def score(alternative, forces):
    response = alternatives[alternative]
    benefit = sum(forces[name] * response[name] for name in forces)
    return benefit - response["cost"]


for context, forces in contexts.items():
    scores = {name: score(name, forces) for name in alternatives}
    winner = max(scores, key=lambda name: (scores[name], -len(name)))
    print(f"{context}: {winner} score={scores[winner]}")
```

The negative stable score means every alternative imposes cost while the direct form loses least. In the variable context, a function table supplies the modeled variation and selection benefits without the object cost. Only the stateful context pays for object roles. These results follow from the declared integers; changing a weight can change the winner.

### Define predictions and disconfirmation

Specify measurement windows and confounders. A Strategy adoption might predict fewer files touched per policy addition without increasing defect rate or navigation time. Evidence of no new policies and slower comprehension supports removal.

### Preserve a reversal path

Prefer an internal seam, one slice, and explicit compatibility boundary. Avoid data formats or public APIs that make an unproven structure expensive to reverse.

## Alternatives and Trade-Offs

**Direct implementation.** Minimizes concepts and indirection. It becomes expensive when a proven variation is scattered or clients depend on unstable decisions.

**Language-native function or data structure.** Often supplies substitution without class roles. It may not model stateful lifecycle, related operations, or nominal contracts well.

**Named catalog pattern.** Compresses communication and carries known consequences. Familiarity can suppress local analysis and import obsolete language assumptions.

**Framework convention.** Provides tooling and ecosystem interoperability. It can make accidental complexity look free and constrain removal.

**Bounded experiment.** Generates local evidence while limiting exposure. Short trials can miss lifecycle and rare-failure effects.

**Decision deferral.** Avoids premature commitment and preserves learning. Delay is harmful when an irreversible boundary must be chosen or current risk is already unacceptable.

**Organization-wide standard.** Reduces local variety and training cost. It can erase contexts where the standard's assumptions fail.

## Failure Modes and Misconceptions

1. **Known pattern means proven solution.** Recognition proposes a hypothesis; context and mechanism determine fit.
2. **More interfaces always reduce coupling.** Interfaces relocate dependencies and add contracts; they do not erase coupling.
3. **A famous company validates our design.** Its scale, team, regulation, and platform may not transfer.
4. **YAGNI means no architecture.** It rejects unsupported future work, not explicit current boundaries or irreversible-risk analysis.
5. **Pattern counts measure quality.** Counts reward structure independent of outcomes and are easily gamed.
6. **A scoring matrix makes the choice objective.** Weights, ratings, omissions, and uncertainty remain judgments.
7. **Generated boilerplate is free.** Readers, operators, tests, upgrades, and incident responders pay its lifecycle cost.
8. **Removing a pattern wastes prior investment.** Sunk costs do not establish future value.
9. **Pattern skepticism proves pragmatism.** Reflexive rejection is as context-free as hype.
10. **Successful deployment confirms the mechanism.** Outcomes need a baseline, measurement, and alternative explanations.

## Worked Examples

### Example 1

**Question:** Does one stable constructor need Abstract Factory?

**Reasoning:** No product family, platform variation, or runtime selection is evidenced. Direct construction at one composition root already localizes the decision. Record a trigger for multiple coherent product families.

**Conclusion:** Centralized direct construction is the simplest adequate baseline.

### Example 2

**Question:** When are Strategy objects cargo-cult structure?

**Reasoning:** Three pure policies selected from a fixed key can be represented by a function table. Objects become justified if policies acquire cohesive state, lifecycle, multiple operations, or a required nominal contract.

**Conclusion:** Select the mechanism that matches the variation, not the class diagram.

### Example 3

**Question:** Should an in-memory collection be wrapped in Repository immediately?

**Reasoning:** If there is one storage mechanism and no domain query boundary, the wrapper may merely rename collection calls. Persistence substitution, aggregate identity, query ownership, or unit-of-work coordination would supply forces.

**Conclusion:** A repository role needs domain and persistence obligations, not a database-shaped noun.

### Example 4

**Question:** Is Singleton appropriate because configuration has one instance?

**Reasoning:** One process instance does not require global access. Explicit construction and injection preserve lifecycle visibility and test isolation. Singleton is a separate access mechanism with hidden-dependency costs.

**Conclusion:** Do not infer global lookup from cardinality.

### Example 5

**Question:** Does a fixed three-step pipeline need Observer?

**Reasoning:** Mandatory ordered stages with coupled failure semantics are clearer as direct calls. Observer fits independently changing subscribers or notification topology, but requires explicit ordering and failure policies.

**Conclusion:** Fixed control flow is not automatically publish-subscribe.

### Example 6

**Question:** Why can copying microservices be cargo-cult architecture?

**Reasoning:** Independent deployment and ownership may be absent while network failure, distributed transactions, versioning, and observability costs appear immediately. Compare a modular monolith under the same team and workload forces.

**Conclusion:** Copying topology without organizational and operational forces copies costs more reliably than benefits.

### Example 7

**Question:** Should two specialized reports trigger CQRS?

**Reasoning:** Database views or read models within one transactional system may satisfy query needs. Independent scaling, security, schema evolution, or write-model protection could justify stronger separation; eventual consistency remains a cost.

**Conclusion:** Read variation alone does not mandate separate stores or services.

### Example 8

**Question:** When is Visitor supported rather than ceremonial?

**Reasoning:** A stable closed set of element variants and frequently added cross-cutting operations supports Visitor's double-dispatch trade. If variants change often or the language has algebraic data types with exhaustive matching, alternatives may fit better.

**Conclusion:** Verify which axis is stable before choosing the extension mechanism.

### Example 9

**Question:** What does the executable scoring example demonstrate?

**Reasoning:** Once corrected, declared weights can show why direct, table, and object structures win under different assumed forces. It cannot prove the weights, completeness, causal effects, or transfer to another project.

**Conclusion:** Use arithmetic to expose assumptions, never to manufacture certainty.

### Example 10

**Question:** How should governance respond when a plugin platform receives no external plugins for a year?

**Reasoning:** Compare adoption predictions with registrations, change history, incidents, comprehension, and maintenance cost. If only one internal implementation remains, preserve the public compatibility period, migrate callers, and contract the platform.

**Conclusion:** De-adoption is a normal evidence-driven outcome, not an architectural failure.

## Cross-Program Connections

- **Software Design:** cohesion and change history identify real variation axes.
- **Software Architecture:** architectural decision records make assumptions and reversibility durable.
- **Testing & Quality Engineering:** experiments, baselines, validity threats, and bounded claims discipline evaluation.
- **Data Engineering:** CQRS and event sourcing claims must include consistency, retention, privacy, and migration costs.
- **Distributed Systems:** local method calls and network protocols have fundamentally different failure models.
- **Cloud & Platform Engineering:** managed products and frameworks can amplify authority transfer and lock-in.
- **Security Engineering:** copied security patterns can fail when assets, threats, trust boundaries, or enforcement points differ.
- **Human-Computer Interaction:** comprehension and navigation are measurable design outcomes for maintainers.
- **Engineering Management:** incentives, ownership, staffing, and sunk-cost effects shape pattern adoption.
- **Research Methods:** causal claims require operational definitions, comparison, uncertainty, and attention to validity.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Presents patterns as recurring design knowledge with applicability, collaborations, and consequences rather than mandatory templates.
2. Christopher Alexander, Sara Ishikawa, and Murray Silverstein, *A Pattern Language: Towns, Buildings, Construction*, Oxford University Press, 1977, ISBN 978-0-19-501919-3. Establishes context-linked, generative patterns and languages rather than isolated copied forms.
3. Martin Fowler, [“Yagni”](https://martinfowler.com/bliki/Yagni.html), 2015, accessed 2026-08-28. Explains the cost of building presumptive features and distinguishes present capability from anticipated need.
4. Frederick P. Brooks Jr., [“No Silver Bullet—Essence and Accident in Software Engineering”](https://history.computer.org/pioneers/pdfs/B/Brooks.pdf), *Computer* 20(4), pp. 10–19, 1987. Challenges universal order-of-magnitude solution claims in software engineering.
5. Fadi Wedyan and Somia Abufakher, [“Impact of Design Patterns on Software Quality: A Systematic Literature Review”](https://doi.org/10.1049/iet-sen.2018.5446), *IET Software* 14(1), pp. 1–17, 2020. Synthesizes heterogeneous findings and reports limited consensus about particular patterns' quality effects.
6. Maria Riaz, Travis Breaux, and Laurie Williams, [“How Have We Evaluated Software Pattern Application? A Systematic Mapping Study of Research Design Practices”](https://doi.org/10.1016/j.infsof.2015.04.002), *Information and Software Technology* 65, pp. 14–38, 2015. Maps empirical evaluations and highlights contextual and generalizability limits.
7. Michael Feathers, [*Working Effectively with Legacy Code*](https://www.pearson.com/en-us/subject-catalog/p/working-effectively-with-legacy-code/P200000008984), Prentice Hall, 2004. Provides low-risk seams and feedback techniques that support reversible evidence gathering.
8. Martin Fowler, [“Who Needs an Architect?”](https://martinfowler.com/ieeeSoftware/whoNeedsArchitect.pdf), *IEEE Software* 20(5), pp. 11–13, 2003. Frames architecture partly through decisions that are hard to change, supporting deliberate treatment of reversibility.

## Exercises

### Exercise 1

Audit a proposal that adds Factory, Registry, and Strategy around one stable report generator. Produce a force-evidence table, simplest adequate alternative, adoption triggers, and disconfirming conditions.

### Exercise 2

Modify the executable model so the direct alternative scores 3 in the stable context in two different ways. Explain how each modification changes the model's meaning and why neither validates the weights empirically.

### Exercise 3

A ten-person company proposes thirty microservices because a large technology company uses them. Write a bounded comparison against a modular monolith, including predictions, measures, confounders, rollback, and decision date.

### Exercise 4

Design a governance review for an existing event-sourcing platform whose original audit requirement has changed. Include sunk costs, privacy deletion, recovery, read latency, staffing, compatibility, and de-adoption criteria.

### Exercise 5

An unfamiliar national health system proposes Observer-based asynchronous notifications for medication orders. Analyze the decision at graduate level: define safety and operational forces, causal mechanism, alternatives, hard constraints, experimental evidence, adversarial cases, and disconfirming conditions.

## Answers to the Exercises

### Answer 1

Evidence shows one generator, one construction path, no runtime registration, and template edits that change together. Factory responds to no observed product-family force; Registry responds to no dynamic discovery force; Strategy responds weakly to possible formatting variation. Their costs include four contracts, selection configuration, navigation, tests, and removal.

Use one pure `generate(report, template)` function constructed directly at the composition root. Centralize the template decision and add behavior tests. Adoption triggers are two independently evolving algorithms, runtime policy selection, external plugins, or stateful policy lifecycle. Disconfirm the pattern proposal if six months of changes remain literal/template edits, comprehension time rises, or no independent implementation appears. Revisit at the trigger rather than an arbitrary desire for pattern completeness.

### Answer 2

First, set direct `cost` to (-3). This produces (0-(-3)=3), but it reinterprets a cost as a subsidy and is therefore mathematically possible but semantically suspect. Second, add a `clarity` force of weight 4 in the stable context, give direct a clarity response of 1, give the other alternatives 0, and extend every context and response consistently. Direct then scores (4-1=3); the model now claims that directness supplies an evidenced simplicity benefit rather than merely imposing the least cost.

Both modifications can be internally consistent, yet they express different assumptions. Neither establishes that weights 3 or 4, response values, or costs 1/3/6 correspond to observed project outcomes. The exercise demonstrates numerical underdetermination: desired rankings can be manufactured unless inputs have provenance, sensitivity is reported, and hard constraints remain outside the score.

### Answer 3

Baseline a modular monolith with enforced modules, one deployment pipeline, and owned interfaces. Compare one representative business boundary extracted as a service, not all thirty. Predict reduced independent-deployment lead time and smaller ownership coordination without unacceptable latency, incidents, cloud cost, or consistency defects.

Measure deployment coupling, lead time, cross-boundary changes, incident recovery, p95/p99 latency, error budgets, infrastructure cost, and engineer comprehension before and during a fixed eight-week trial. Confounders include team learning, concurrent feature load, new tooling, and unequal investment in alternatives. Preserve one authoritative data path and a route back behind a compatibility boundary. Decide on a stated date to retain, adapt, revert, or gather more evidence. Do not generalize one boundary's result automatically to twenty-nine others.

### Answer 4

Restate the remaining audit and replay obligations; sunk implementation cost is recorded but excluded from future-value comparison. Measure deletion feasibility, key-destruction policy, event and snapshot recovery time, projection lag, read latency, storage growth, schema evolution, on-call load, and scarcity of event-sourcing expertise. Compare retaining the platform, limiting it to regulated aggregates, and migrating to current-state storage plus an append-only audit log.

Hard constraints include lawful erasure or approved cryptographic deletion, provable audit integrity, recovery objectives, and compatibility for downstream consumers. Trial one aggregate with dual-read comparison but one authoritative write path. De-adopt when revised requirements no longer need replay, privacy risk remains unacceptable, recovery misses objectives, and total operating cost exceeds a simpler compliant alternative. Use expand–migrate–contract, signed reconciliation, consumer inventory, rollback points, and an explicit retention decision for historical events.

### Answer 5

Forces include medication timeliness, duplicate suppression, ordering, patient identity, authorization, auditability, intermittent endpoints, escalation, workload bursts, and independent subscriber evolution. Observer or publish-subscribe can decouple producers from changing notification consumers and buffer bursts, but only if durable delivery, identity, policy, and operational ownership complete the causal mechanism.

Compare synchronous explicit calls, a transactional outbox with a durable broker, and workflow orchestration. Hard constraints include one authorized order identity, atomic relation between accepted order and notification intent, bounded delivery/escalation time, idempotent consumers, privacy, traceability, and a safe manual path. Test duplicate, delayed, reordered, poisoned, unauthorized, missing, and replayed messages; broker outage; database commit failure; clock skew; patient merge; subscriber timeout; and regional partition. Use simulation, fault injection, contract tests, trace reconciliation, and a shadow cohort without allowing duplicate clinical action.

Disconfirm the asynchronous choice if delay violates clinical bounds, reconciliation cannot prove notification intent, subscriber independence is absent, operators cannot recover poisoned work safely, or a simpler transactional workflow meets all constraints with lower risk. No trial may infer patient safety from message-delivery counts alone; named clinical, security, privacy, and operations reviewers are required before production authorization.
