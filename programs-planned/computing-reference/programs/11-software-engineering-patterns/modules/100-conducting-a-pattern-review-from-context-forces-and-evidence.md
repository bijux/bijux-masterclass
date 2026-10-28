---
module_id: SEPAT-100
program: Software Engineering: Patterns
level: 2
module_number: 100
title: Conducting a Pattern Review from Context, Forces, and Evidence
status: complete
last_verified: 2026-08-29
---

# Conducting a Pattern Review from Context, Forces, and Evidence

## One-Page Review

### Governing question

How can a review decide whether a pattern is warranted, which variant/composition is safe, and what evidence/ownership makes the decision reversible and durable—without choosing by name, popularity or diagram?

### Essential definitions

- A **pattern review** is a structured decision process connecting a recurring context/problem and forces to candidate mechanisms, consequences, evidence, adoption and reassessment.
- **context** describes the current system/domain/team/lifecycle and constraints under which the decision applies.
- A **force** is a competing concern shaping the solution: correctness, latency, change, consistency, availability, security, cost, cognitive load or regulation.
- A **candidate** includes the named pattern, a no-pattern/simpler baseline and credible alternatives.
- A **claim** is a bounded falsifiable statement about a candidate under explicit assumptions.
- An **invariant** is a property that must remain true across relevant states/failures.
- An **evidence matrix** maps each decisive claim/invariant/failure to an appropriate oracle, method, environment/version, result and limitation.
- A **quality-attribute scenario** states source, stimulus, environment, affected artifact, response and measurable response criterion.
- A **decision record (ADR)** captures context, decision, status, consequences, alternatives and future supersession; it is not the entire analysis.
- A **fitness function** is an automated or reviewable check that detects erosion of a desired property over time.
- A **residual risk** remains after controls; an **assumption** is a premise whose invalidation triggers reassessment.
- **reversibility/option value** measures the ability/cost to change course as evidence arrives.

### Central model, mechanism, or theorem

Do not compute a universal pattern score. For context (K), forces (F=\{f_i\}), candidates (D=\{d_0,\ldots,d_m\}), evaluate each candidate against scenarios, invariants, costs and uncertainty:

\[
Review(K,F,D,E)\rightarrow\{adopt, bounded\ pilot, defer, reject\}
\]

with a rationale, not an algorithmic verdict. (d_0) is the simplest/no-pattern baseline. A decision is defensible when decisive claims have proportionate evidence, negative cases can falsify them, consequences/assumptions/residual risks are visible, affected owners accept obligations, and rollout has guardrails, rollback/exit and review triggers. Missing evidence should reduce commitment, not be replaced by stronger adjectives.

### Critical invariants

- Start from a concrete recurring problem and current baseline; pattern names enter after context/forces.
- Separate requirements, assumptions, preferences and constraints; rank conflicts with stakeholder owners.
- Compare at least the status quo/no-pattern baseline and credible alternatives at equivalent scope.
- Trace mechanism → guarantee → consequence → failure; never infer a guarantee from vocabulary.
- Every decisive claim has a matching evidence method and explicit limitation; tests/benchmarks/references are not interchangeable.
- Include causal negative/adversarial cases and failure/degraded modes, not only demonstrations.
- Evaluate composition interactions, resource budgets and organizational/operational ownership.
- Security, privacy, accessibility, compliance and irreversible effects receive proportionate human review.
- Decision record states rejected alternatives, migration, rollback/exit, fitness checks and reassessment triggers.
- Pilot/adoption is bounded and instrumented; outcome evidence can reject the chosen pattern without blame.

### Common failures

Failures include starting with “we need microservices/Event Sourcing”; pattern bingo; treating an example run as universal proof; benchmark without production distribution; vendor documentation as independent fitness evidence; comparing polished candidate to caricature baseline; hiding negative consequences; no failure budget; ignoring combinations (retry × timeout × queue); architecture diagram without authority/data path; “industry best practice” without context; decision by majority/seniority alone; automation pretending to decide ethics/domain risk; ADR written after the fact; no owner/exit; permanent pilot/toggle; and success defined as pattern adoption.

### Compact example

Problem: product search joins overload checkout database and needs p95 <150 ms; price/entitlement must remain current. Candidates: indexed direct query, replica, cache, materialized search view, service extraction. Evidence shows indexed query meets 80 ms at forecast load and source isolation is unnecessary; direct query plus index wins now. A fitness check alerts at p95 120 ms/CPU budget, and review triggers at 3× load/query divergence. Rejecting the more elaborate pattern is a successful review.

### Connections

[Recurring Problems, Context, Forces, and Consequences](001-recurring-problems-context-forces-and-consequences.md), [Reading and Writing a Pattern Form](003-reading-and-writing-a-pattern-form.md), [Selecting a Pattern from Forces Rather Than Names](010-selecting-a-pattern-from-forces-rather-than-names.md), [Pattern Composition](006-pattern-composition.md) and [Architecture Anti-Patterns](099-recognizing-golden-hammer-big-ball-of-mud-and-distributed-monolith.md) are prerequisites. This final module returns to the complete [Software Engineering: Patterns roadmap](../ROADMAP.md) as the program-level successor: independent pattern judgment across all ten blocks.

## Governing Question

How should an expert review transform an attractive pattern proposal into a falsifiable, owned and revisable engineering decision?

Patterns compress experience; they do not remove context. The same mechanism can be correct, unnecessary or harmful depending on consistency, scale, failure tolerance, team boundaries and lifecycle. Review quality is not measured by how many patterns are recognized or adopted. It is measured by whether the decision exposes the decisive relationships, predicts consequences, survives counterexamples and creates feedback.

The review is neither a ceremonial meeting nor a numerical architecture contest. It is a reusable reasoning record. Small reversible decisions need a short review; persistent data authority, distributed transactions, security controls or regulated decisions require deeper evidence and named human accountability. Proportionality matters.

## Why This Matters

Pattern language makes design discussable, but it can produce social shortcuts: familiar names feel proven, diagrams imply guarantees, precedent replaces evidence and dissent appears unsophisticated. The result is cargo-cult implementation or analysis paralysis.

A rigorous review controls both risks. It begins with the current system and cost of inaction. It asks whether an ordinary function/index/module/transaction is enough. It compares mechanisms at equivalent scope. It makes performance, correctness, compatibility, failure, operations and human workflow observable. It records uncertainty and creates a bounded pilot when evidence cannot be obtained cheaply before use.

The lasting output is not only an ADR. It includes accepted contract/invariants, evidence artifacts, operational ownership, fitness checks, rollout/rollback and triggers for supersession. A future engineer should understand why the decision was reasonable then and which changed premise permits a different decision now.

## Prerequisites and Retrieval

Learners should retrieve:

- full pattern form and distinction among pattern/principle/idiom/recipe/framework;
- requirements, quality attributes, constraints and trade-offs;
- invariants, preconditions, failure models and proof limitations;
- experiments, benchmarks, statistical distributions and confounding;
- unit/property/contract/integration/fault/security/usability review methods;
- ADRs, fitness functions, ownership and lifecycle management;
- migration, canary, rollback, compatibility and decommission;
- all Program 11 pattern families and anti-patterns.

Before continuing, take any proposed pattern and state the no-pattern baseline, one causal mechanism, one falsifying negative case and one residual risk. If any is missing, the proposal is not review-ready.

## Learning Objectives

After this module, learners can:

1. frame a review from current context/problem and counterfactual baseline;
2. elicit/rank forces as measurable scenarios with accountable stakeholders;
3. compare patterns, variants, compositions and simpler alternatives fairly;
4. derive guarantees from mechanisms/assumptions and enumerate failure modes;
5. construct a claim-to-evidence matrix with negative cases/limitations;
6. evaluate security, privacy, operations, evolution, cost and team obligations;
7. distinguish automated evidence from named human judgment;
8. choose adopt, pilot, defer or reject with reversible rollout/exit;
9. write a concise decision record and enforceable fitness functions;
10. conduct an independent high-stakes pattern review without cargo culting.

## Core Exposition

### Frame the decision, not the desired answer

Write one sentence: “In context K, recurring problem P causes observable harm H; by date/horizon T we need response R under constraints C.” Include current topology/data authority, workload/distributions, failure history, team/ownership, compliance/lifecycle and existing controls. State what happens if nothing changes.

Bad: “Should we use CQRS?” Better: “Product-detail reads drive 65% primary database CPU and three audience shapes leak persistence concerns; writes require immediate inventory/price authority; forecast traffic doubles in 12 months.” Now CQRS, explicit query DTOs/indexes, replica/cache/materialized view and no change can be compared.

Freeze proposal scope. Is review selecting an object collaboration, persistence boundary, resilience control, migration technique or system architecture? Do not let one pattern expand into a transformation portfolio unnoticed. Identify decision owner, affected domain/data/security/operations owners and deadline.

### Elicit forces as scenarios

Replace adjectives with quality-attribute scenarios:

- **Performance:** Under forecast peak distribution X, when request Y arrives, p95/p99 and saturation remain within Z.
- **Availability/degradation:** During dependency D outage for N minutes, operation O rejects/degrades with bounded impact.
- **Modifiability:** A representative policy change touches at most named owners/components and deploys under supported version skew.
- **Security:** A revoked tenant principal cannot obtain protected data, including through stale views/caches, within bound.
- **Recoverability:** After loss/corruption, restore/rebuild completes within RTO/RPO and reconciles.
- **Operability:** On-call can identify owner/failure and execute recovery within time/permission constraints.

Distinguish hard requirement, negotiable objective, assumption and preference. Rank conflicts through stakeholder authority: strong consistency versus availability, freshness versus cost, independence versus transaction simplicity. Not every force deserves a numeric weight; record priority/rationale and unacceptable outcomes.

### Establish the baseline and candidates

Always include:

- current/no-change with known cost/risk;
- simplest direct improvement (index, ordinary composition, module boundary, timeout);
- proposed pattern variants;
- credible alternative mechanisms;
- defer/pilot/retire if appropriate.

Compare equivalent scope and maturity. Do not price the baseline with worst incident while describing proposed system as ideal steady state. Include migration, coexistence, operations, staff, security review, vendor/exit and decommission cost—not only runtime cloud bill. Consider option value: a smaller reversible move may dominate a theoretically optimal irreversible one under uncertainty.

### Trace mechanisms to claims

For each candidate build a causal chain:

`context/assumptions -> mechanism -> invariant/guarantee -> desired response -> consequences/failure modes`.

Example: “bounded queue” does not guarantee stability by name. Mechanism limits in-flight items to N; when full, producer blocks/rejects under policy; memory attributable to queued payload is bounded if payload size also bounded; overload becomes delay/rejection rather than unbounded allocation. It may deadlock if producer holds a resource consumer needs, and it does not bound active worker memory.

Label model, mechanism, implementation, configuration and policy separately. Circuit-breaker state machine needs thresholds/time/probes; it does not make a slow dependency fast. Repository mediates aggregate persistence; it does not make arbitrary queries efficient. Event Sourcing preserves accepted history only if event semantics/schema/replay/store are governed.

### Review composition, not isolated pattern cards

Real systems compose. Draw request/data/effect paths and state owners. Analyze interactions:

- retry × timeout × fan-out can amplify load;
- circuit breaker × cache fallback can serve dangerously stale authorization;
- saga × outbox × idempotent consumer distributes responsibility across several stores;
- CQRS × materialized view creates explicit freshness/rebuild obligations;
- decorator/proxy chains can reorder auth, transaction, cache and telemetry;
- thread pool × bounded buffer × deadline determines admission/cancellation;
- Strangler × CDC requires ownership/fencing/rollback beyond routing.

Build a failure-mode table: initiating fault, observable propagation, detection, containment, recovery, state after recovery and evidence. Test correlated/shared dependencies; independence assumptions often fail in real infrastructure.

### Map claims to proportionate evidence

For each decisive claim record:

- exact bounded claim and assumptions;
- failure/counterexample it excludes;
- oracle/acceptance criterion;
- method/tool/environment/version/data distribution;
- positive and causal negative evidence;
- result/artifact/date/owner;
- limitation and residual risk.

Methods differ:

- proof/invariant/model review for logical state claims;
- unit/property/model checking for algorithms/state machines;
- contract/integration/version-skew tests for boundaries;
- fault/chaos/recovery drills for degraded behavior;
- benchmarks/load tests with representative distributions for performance;
- static/dynamic security tests plus threat/human review for security;
- accessibility/usability/domain review with affected people;
- production canary/telemetry and reconciliation for operational outcomes.

A benchmark cannot prove semantic correctness; a type check cannot prove authorization; a successful chaos experiment cannot prove all failures; a link to documentation proves stated product semantics only for versions/configuration examined. Missing evidence is visible uncertainty. Use a bounded pilot instead of pretend certainty.

### Demand causal negative cases

Positive examples show possibility. A negative case tests whether the mechanism rejects/fails for the predicted reason. For idempotency, replay the same stable identity and show one effect, then reuse identity with different payload and show conflict. For timeout propagation, inject dependency latency beyond deadline and show cancellation/resource release. For module boundary, deliberately add forbidden import and show architecture check fail.

Preserve negative regressions. Avoid weak tests that merely flip a boolean or assert implementation calls. The negative case should exercise the first decisive relationship. Explain state after failure: unchanged, partially committed, compensating, retryable or needs repair.

### Review nontechnical ownership and incentives

Every mechanism creates work: schema/version owners, on-call, capacity, incident, security review, consumer migration, cost allocation and retirement. A pattern is infeasible if the named owner lacks authority/capacity. YAML containing an owner name is not proof of ownership.

Ask who can change contract, who responds at 03:00, who funds duplicated stores, who approves risk, who notifies consumers and who deletes the pattern when forces disappear. Examine team cognitive load and dependency waits. An architecture that requires permanent coordination across teams contradicts an independence claim even if code can deploy separately.

High-stakes domain judgments cannot be automated away. Machines can validate presence/consistency of evidence; named qualified humans decide acceptable clinical, legal, financial, safety, privacy and accessibility risks, with a dated record and dissent/unresolved risk.

### Decide proportionately

Possible outcomes:

- **Adopt:** evidence is sufficient and consequences/ownership accepted.
- **Bounded pilot:** decisive uncertainty can be reduced safely with scope, duration, success/stop and no irreversible effect.
- **Defer:** need absent/not urgent; state trigger for reopening.
- **Reject:** mechanism conflicts with forces or cost/risk dominates; record conditions that could change conclusion.

Use voting only to surface views, never to manufacture truth. Decision owner explains trade-off and dissent. For irreversible/high-blast choices, require stronger evidence and staged commitment. For cheap reversible choices, avoid analysis paralysis.

### Record, execute and keep the decision alive

ADR fields: title/status/date/owner; context/problem/scope; forces/scenarios; decision and mechanism; alternatives/no-change; assumptions; positive/negative consequences; evidence links/limitations; security/privacy/operations; rollout/migration; rollback/exit; fitness functions; review triggers; human approvals/dissent; supersedes/superseded-by.

Implementation plan uses small coherent changes. Pilot guardrails observe correctness, latency, saturation, security/business outcomes and cost. Rollback is tested, not stated. Decommission/exit removes toggles/adapters/old paths when converged.

Fitness functions protect decisive properties: forbidden dependency edge, queue capacity, contract compatibility, no cross-owner writes, replay fixtures, recovery duration, source lag, read-model reconciliation or maximum retry budget. Some are CI checks; others scheduled drills/reviews. Every fitness function has owner, cadence, failure action and limitation. Reassess when assumptions/workload/regulation/ownership/vendor/cost changes or on scheduled horizon.

### A completeness checker, not a decision engine

The executable model identifies missing review evidence and returns `pilot`, never “chooses” a pattern. Human/domain judgment remains explicit.

<!-- bijux-verify: {"id":"sepat-100-review-evidence-gate","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"candidate=bounded-queue\ncovered=context,forces,baseline,alternatives,invariants,negative-case,owner,rollback\nmissing=production-load,recovery-drill,human-risk-review\noutcome=bounded-pilot\nautomated-decision=no\n","stderr":""}} -->
```python
required = [
    "context", "forces", "baseline", "alternatives", "invariants",
    "negative-case", "owner", "rollback", "production-load",
    "recovery-drill", "human-risk-review",
]
evidence = {
    "context", "forces", "baseline", "alternatives", "invariants",
    "negative-case", "owner", "rollback",
}
covered = [item for item in required if item in evidence]
missing = [item for item in required if item not in evidence]
outcome = "bounded-pilot" if missing else "review-ready"

print("candidate=bounded-queue")
print("covered=" + ",".join(covered))
print("missing=" + ",".join(missing))
print("outcome=" + outcome)
print("automated-decision=no")
```

The run proves deterministic set-membership/report ordering only. The checklist is illustrative, not universal; it cannot judge evidence quality, pattern fitness, stakeholder legitimacy, ethics, risk or adoption. A real review can reject despite no missing fields or adopt a proportionate small reversible change with explicitly accepted uncertainty.

## Definitions and Notation

Let context (K=(system,domain,workload,teams,lifecycle,constraints)); forces (F=\{f_1,\ldots,f_n\}); candidates (D=\{d_0,\ldots,d_m\}), with (d_0) baseline; assumptions (A_d); claims (C_d); invariants (I_d); evidence items (E=\{e_j\}); residual risks (R_d); and stakeholder/owner set (O).

An evidence relation (supports(e,c,K,b)) states evidence (e) supports bounded claim (c) in context (K) to boundary (b); it is not truth outside that boundary. A falsifier (n(c)) is a negative observation that contradicts c's mechanism/premise. **Evidence coverage** means each decisive claim has one or more appropriate items and limitations; it is not count maximization.

A quality scenario is tuple ((source,stimulus,environment,artifact,response,measure)). A decision outcome (J\in\{adopt,pilot,defer,reject\}) is a reasoned governance result, not a pure function of weights. For a pilot, define scope (S), horizon (T), success (P), guardrails (G), stop (X) and rollback/exit (Z).

**Confidence** should be expressed qualitatively/quantitatively only when calibration supports it. Do not write false probabilities. State known, unknown, assumption, evidence boundary and consequence if wrong.

## Mechanisms, Invariants, or Proof Structure

1. **Frame.** Current context, recurring problem/harm, no-change counterfactual, scope, owner and deadline.
2. **Elicit forces.** Measurable scenarios, constraints/assumptions/preferences, priorities and unacceptable outcomes.
3. **Generate candidates.** Baseline, simplest mechanism, proposed pattern variants/compositions, alternatives and defer/retire.
4. **Trace causality.** Mechanism, state/authority, invariants, claimed guarantees, consequences, costs and failure/degraded modes.
5. **Analyze composition.** End-to-end request/data/effect, resources, shared dependencies and interaction amplification.
6. **Plan evidence.** Claim-to-oracle matrix, causal negatives, versions/environments/distributions and limitation/residual risk.
7. **Review ownership/risk.** Domain, data, security/privacy, operations, finance, accessibility/compliance and human approvals.
8. **Decide proportionately.** Adopt/pilot/defer/reject; rationale, dissent, reversibility and conditions that change decision.
9. **Execute safely.** Small changes, bounded cohort, guardrails, reconciliation, tested rollback/exit and decommission.
10. **Sustain/reassess.** Fitness functions, telemetry, incident/assumption triggers, review date and superseding ADR.

The review establishes a defensible decision, not proof of future success. Argument validity requires claims follow from mechanisms under stated assumptions; evidence increases confidence within boundaries; a pilot tests uncertain causal claims. Unknown future workloads/people/adversaries remain. Honest residual risk and triggers are part of rigor.

## Alternatives and Trade-Offs

**Informal expert review** is fast and valuable for reversible local decisions; it risks tacit assumptions/knowledge loss. Capture the few decisive facts.

**ADR alone** records conclusion/context/consequences but may omit claim-level evidence and failure analysis. Pair it with proportionate supporting artifacts.

**Checklist/compliance gate** ensures minimum coverage and repeatability; it can become checkbox theater and cannot decide contextual fitness.

**Weighted decision matrix** makes preferences visible; numbers imply commensurability/precision and can hide veto constraints. Use as discussion aid, not oracle.

**ATAM-style facilitated evaluation** is valuable for major architecture quality-attribute trade-offs with scenarios/stakeholders; costly for small choices.

**Prototype/spike** reduces feasibility uncertainty but often lacks production load/failure/operations; keep disposable or convert deliberately.

**Production experiment/canary** provides realistic evidence but needs safe scope, ethics, guardrails and reversible effects.

**Benchmark/POC bake-off** compares implementations; workload/environment/maturity/vendor bias can mislead and it cannot settle domain governance.

**Do nothing/defer** preserves option value and avoids premature complexity; carries current harm and should have a review trigger.

Match process weight to decision reversibility, blast radius, persistence and stakes.

## Failure Modes and Misconceptions

- **“Pattern is proven.”** Literature supports recurring mechanism/consequences; local fitness still needs context.
- **“Best practice.”** Ask best under which forces and evidence.
- **“More evidence is always better.”** Seek decisive proportionate evidence; avoid analysis paralysis/noisy counts.
- **“Tests prove architecture.”** Each test supports bounded claims; organizational/operational/domain properties need other evidence.
- **“Benchmark chooses design.”** It addresses one environment/distribution, not semantics/operations/evolution.
- **“ADR is approval paperwork.”** It is a living reasoning/supersession record.
- **“Checklist decides.”** Completeness is not correctness or ethical legitimacy.
- **“Weighted score is objective.”** Weights/scales encode judgment and veto constraints may dominate.
- **“Consensus proves truth.”** Decision uses expertise/evidence; record dissent and accountable owner.
- **“Pilot means safe.”** Bound users/data/effects, stop/rollback and ethics.
- **“Rollback is deploy old.”** Data/schema/external effects may be irreversible.
- **“Automation replaces human review.”** It checks evidence shape/invariants; humans own domain risk.
- **“Pattern adopted means success.”** Outcomes and fitness functions decide; rejection/simplification can be success.
- **“One review lasts forever.”** Assumptions/workloads/ownership/regulation change; trigger reassessment.
- **“Documentation substitutes for ownership.”** Named owner must have authority, capacity and operational acceptance.

## Worked Examples

### Example 1

**Situation.** Team proposes Singleton for configuration because “there should be one.”

**Reasoning.** Force is consistent immutable startup configuration, not global access. Pass explicit configuration/dependency; process may have test instances and future multi-tenant variants. Singleton adds hidden coupling.

**Conclusion.** Pattern review can reject a name after identifying simpler mechanism matching the force.

### Example 2

**Situation.** Queue backlog caused memory exhaustion; proposal is bounded buffer of 1,000.

**Reasoning.** Define payload-size bound, arrival/service distribution, full policy, producer-held resources and deadline. Load/fault tests include slow consumer and negative deadlock case. Capacity 1,000 alone is unjustified.

**Conclusion.** Mechanism plus resource/failure assumptions—not class name—supports boundedness.

### Example 3

**Situation.** API p95 is slow; cache proposal benchmarks 10× faster on uniform keys.

**Reasoning.** Production is skewed, authorization-sensitive and update-heavy. Test real distribution, invalidation, stampede, revocation and stale policy; compare index/direct query. Benchmark supports only local hit latency.

**Conclusion.** Evidence must match decisive workload and semantic claims.

### Example 4

**Situation.** Retry and circuit breaker each pass component tests, but outage load increases.

**Reasoning.** Composition has three retries × fan-out × breaker half-open probes with no deadline/budget. Model request amplification; enforce one retry owner, deadlines, jitter/budget and bounded probes; inject correlated failure.

**Conclusion.** Review the composed failure system, not isolated pattern cards.

### Example 5

**Situation.** Event Sourcing proposal promises audit and temporal queries for simple preferences.

**Reasoning.** Compare current state plus targeted audit/bitemporal fields. Permanent event schemas, replay, privacy and operations exceed value; defer unless regulatory history/alternate projections emerge.

**Conclusion.** No-pattern/simpler baseline prevents benefit-only pattern selection.

### Example 6

**Situation.** Repository abstraction is proposed over a stable ORM for one aggregate.

**Reasoning.** If it captures aggregate-oriented operations and protects persistence semantics, it may help; if it mirrors every ORM query, it adds indirection. Write representative callers and migration/change scenario to decide.

**Conclusion.** Evaluate abstraction by information hiding and change force, not layer count.

### Example 7

**Situation.** Two alternatives remain uncertain after tests: local materialized view or synchronous owner API.

**Reasoning.** Run bounded read-only pilot: measure latency/availability/source load and projection staleness/reconciliation. Exclude authorization decisions, define stop and remove losing path.

**Conclusion.** A safe pilot buys information while preserving option value.

### Example 8

**Situation.** Review group votes 8–2 for microservices; dissent cites shared transaction.

**Reasoning.** Majority cannot remove invariant. Document payment/inventory atomicity, test compensation/business tolerance and compare modular monolith. Decision owner resolves evidence; record dissent/conditions.

**Conclusion.** Governance is accountable reasoning, not architecture plebiscite.

### Example 9

**Situation.** Chosen outbox works at launch, but cleanup lag later threatens storage.

**Reasoning.** Fitness checks include oldest unpublished row, table bytes, relay lag, duplicate rate and source capacity with owner/action. Threshold breach triggers incident/review, not silent pattern prestige.

**Conclusion.** A pattern decision remains alive through owned fitness functions and exit triggers.

### Example 10

**Situation.** Hospital considers asynchronous Saga for medication authorization across pharmacy/inventory/billing.

**Reasoning.** Map clinical authority, irreversible dispense, compensation limits, stale contraindications, deadlines/degraded mode, privacy and manual workflow. Simulate failure timelines; automated tests cannot decide acceptable patient harm. Named human clinical-safety, pharmacy, legal/privacy, security, accessibility and operations reviewers approve or reject each risk/compensation before any bounded non-effect pilot.

**Conclusion.** High-stakes pattern review combines technical evidence with qualified human judgment and may reject elegant distribution.

## Cross-Program Connections

- **Software Design and Domain Modeling:** invariants, authority, information hiding and representative change scenarios determine fit.
- **Architecture:** quality-attribute scenarios, trade-off analysis, ADRs and fitness functions sustain decisions.
- **Algorithms/Theory:** proofs/models establish conditional logical claims; complexity bounds assumptions/resources.
- **Distributed Systems:** failure/order/time/consistency models prevent pattern vocabulary from inventing guarantees.
- **Database/Data Engineering:** authority, schema history, backfill, reconciliation and retention supply durable evidence.
- **Security Engineering:** threat models, least privilege, privacy and human risk review must enter before adoption.
- **Testing/Quality:** claim-specific positive/negative/property/contract/fault evidence makes decisions falsifiable.
- **Delivery/Reliability/Platform:** canary, rollback, SLOs, operations, cost and decommission determine production viability.

## References

- Christopher Alexander et al., *A Pattern Language*, Oxford University Press, 1977. Foundational context/problem/forces/solution/consequence and pattern-language thinking.
- Erich Gamma et al., *Design Patterns*, Addison-Wesley, 1994. Canonical software pattern form, applicability, participants and consequences.
- Michael Nygard, [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions), 2011, retrieved 2026-08-29. Defines lightweight ADR status, context, decision and consequences.
- Carnegie Mellon Software Engineering Institute, [Architecture Tradeoff Analysis Method Collection](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/), retrieved 2026-08-29. Authoritative ATAM resources for stakeholder scenarios, quality attributes, sensitivity/trade-off and risk analysis.
- Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, fourth edition, Addison-Wesley, 2021. Quality-attribute scenarios, tactics, analysis and documentation.
- Neal Ford, Rebecca Parsons, and Patrick Kua, *Building Evolutionary Architectures*, second edition, O'Reilly Media, 2022. Fitness functions and incremental evolutionary change.
- Basili, Caldiera, and Rombach, [The Goal Question Metric Approach](https://www.cs.umd.edu/~basili/publications/technical/T78.pdf), 1994. Measurement derived from goals/questions rather than convenient metrics.
- Hillside Group, [Patterns Library](https://www.hillside.net/patterns/), retrieved 2026-08-29. Pattern-writing, languages and workshop lineage; references deepen but do not replace local review evidence.
- Nicole Forsgren, Jez Humble, and Gene Kim, *Accelerate*, IT Revolution, 2018. Empirical delivery/outcome measurement and organizational capability evidence.
- National Institute of Standards and Technology, [Secure Software Development Framework (SSDF) Version 1.1](https://csrc.nist.gov/pubs/sp/800/218/final), SP 800-218, 2022, retrieved 2026-08-29. Authoritative secure-development practice reference for proportional security evidence and ownership.

## Exercises

### Exercise 1

Write the minimum review frame for a proposed Circuit Breaker: context, problem, forces, baseline, two alternatives, one invariant, one negative case and one residual risk.

### Exercise 2

Build a claim-to-evidence matrix for a bounded worker queue. Match memory, overload, cancellation, fairness and recovery claims to appropriate evidence and limitations.

### Exercise 3

Diagnose a review that uses a weighted score, vendor benchmark, unanimous vote and ADR but has no failure model, owner, rollback or negative case.

### Exercise 4

Compare adopt, pilot, defer and reject outcomes for CQRS under three contexts: simple CRUD, read-heavy search and safety-critical authorization.

### Exercise 5

Conduct a model review for an unfamiliar national emergency-alert delivery pattern using publish–subscribe, competing consumers, retries, dead letters and deduplication. Include human governance.

## Answers to the Exercises

### Answer 1

Context/problem: checkout synchronously calls tax service; brief outages consume all worker threads and exceed 2-second deadline. Forces: fail fast, protect worker capacity, avoid blocking recovery, preserve tax correctness, observe degraded state. Baseline: deadline plus bounded concurrency/no breaker. Alternatives: cached last-known tax only where legally valid; asynchronous quote workflow. Circuit-breaker invariant: when open, no ordinary calls reach dependency; probes are bounded and state transitions concurrency-safe. Negative case: dependency remains slow while half-open receives concurrent requests—prove only configured probes pass and callers receive bounded result. Residual risk: correlated outage/cache invalidity or false opening can reject valid purchases; breaker does not make tax available. Evidence includes state-machine/concurrency tests, dependency-latency fault test, load/resource budget and legal/domain review of any fallback.

### Answer 2

Memory claim: queue stores at most N items and each admitted item ≤B bytes; inspect invariant/property tests plus allocation/load measurement, limitation excludes active-worker/runtime overhead. Overload claim: at capacity producer blocks/rejects within deadline under explicit policy; sustained arrival>service load test and causal negative unbounded queue, limitation covers tested distribution. Cancellation claim: blocked producers/consumers wake and ownership is released; concurrency/model/fault tests including shutdown races, limitation bounded schedules. Fairness claim needs precise definition and scheduler/implementation evidence; often reject guarantee and measure starvation distribution rather than assert. Recovery claim: after worker crash/restart, queued durability/at-least-once/idempotency semantics require process/persistence fault tests and reconciliation; an in-memory queue may explicitly lose items. Every row records environment, result, artifact and residual risk; one benchmark cannot fill all rows.

### Answer 3

The score hides weights/veto requirements; vendor benchmark covers its workload and may be biased; unanimity is governance evidence, not technical truth; ADR records a conclusion but missing reasoning. Pause irreversible adoption. Restate context/forces and no-pattern/credible alternatives; trace mechanism/authority/data/resource/failure paths; identify decision/operational/security/domain owners. Add causal negative/adversarial cases, representative benchmark, contract/fault/recovery/security evidence with limitations, migration/rollback and exit. Use the matrix only to expose priorities, not auto-rank. Record conditions for pilot/adopt/defer/reject and dissent. If small reversible, bounded pilot can gather missing evidence; otherwise reject/defer until decisive high-risk claims are supported.

### Answer 4

Simple CRUD with low load/simple queries: reject physical CQRS and use one model or logical query DTOs; revisit on measured divergence. Read-heavy search with overloaded source and tolerable seconds lag: pilot/adopt asynchronous search projection after durable publication, delete/idempotency, position, reconciliation, security and rebuild evidence; CQRS scope may be only search. Safety-critical authorization: a stale read model cannot grant/revoke safely unless a formally bounded grant/version protocol satisfies policy; use authoritative query or wait/fail closed. CQRS may still serve display while authorization remains authority. Defer if anticipated scale has no evidence. Outcome belongs to context/use case; “CQRS” is neither globally accepted nor rejected.

### Answer 5

Frame alert classes, jurisdictions, languages/accessibility, recipients/channels, deadlines, authority and harm of missed/duplicate/late alerts. Scenarios include regional broker/provider outage, subscriber surge, duplicate/reordered delivery, corrections/cancellation, expired alert and inaccessible/unauthorized recipient data. Authority publishes immutable versioned alert facts through durable outbox; pub-sub fans channel workflows; competing consumers partition by stable recipient/alert key; deadline-bounded retries use idempotent effect ledger; dead-letter/quarantine never silently marks delivered. Corrections/expiry dominate older versions. Human/manual fallback and reconciliation compare authorized recipients with provider acknowledgements.

Compare simpler provider broadcast, single durable queue and multi-channel pattern. Evidence: schema/version contract, state-machine/property tests, duplicate/gap/reorder and crash faults, region capacity/latency load, provider sandbox, accessibility/language fixtures, security/privacy threat tests, restore/replay and live drill with no real public effect. Pilot internal opt-in cohort, with zero unauthorized sends, bounded duplicate/miss targets, stop/rollback and provider isolation. Named human emergency-management, public-safety, legal/privacy/security, accessibility/language/community and operations reviewers decide acceptable latency, message meaning, channel equity and manual override. Fitness functions cover outbox age, end-to-end deadline, dedupe conflicts, dead letters, reconciliation and drill cadence. Reject automation that lacks accountable alert authority or hides undelivered populations behind aggregate success.
