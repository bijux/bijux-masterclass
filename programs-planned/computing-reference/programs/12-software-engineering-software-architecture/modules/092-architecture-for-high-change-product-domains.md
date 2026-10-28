---
module_id: SARCH-092
program: Software Engineering: Software Architecture
level: 2
module_number: 92
title: Architecture for High-Change Product Domains
status: complete
last_verified: 2026-09-06
---

# Architecture for High-Change Product Domains

## One-Page Review

### Governing question

How should architects design a product domain whose goals, rules, user understanding, workflows, integrations, and competitive environment change rapidly, without converting uncertainty into permanent complexity or sacrificing correctness, safety, operability, and coherent domain meaning?

### Essential definitions

- a **high-change domain** has frequent, consequential changes in product understanding or domain behavior—not merely frequent deployments;
- a **product hypothesis** is a falsifiable claim that a change will improve a named outcome for a defined population under stated constraints;
- **volatility** is observed frequency and consequence of change in a concept, decision, interface, or dependency;
- a **stable core** contains semantics and invariants that should change only with deliberate migration; it is discovered, not assumed;
- a **volatile edge** contains policy, presentation, workflow, or integration choices expected to change independently;
- a **seam** is a boundary at which behavior can be varied, tested, replaced, or intercepted;
- **option value** is the value of retaining a feasible future choice under uncertainty;
- **reversibility** is the practical ability to restore an acceptable state within the relevant time and consequence bounds;
- **deploy** places an artifact in an environment; **release** exposes behavior or makes it authoritative;
- a **feature flag** selects behavior at runtime or build time and creates additional configuration states;
- a **fitness function** repeatedly evaluates an architectural characteristic within a declared evidence boundary;
- **architectural runway** is the smallest evidenced capability needed for foreseeable product movement, not speculative infrastructure;
- **transition architecture** is production structure needed while old and new behavior coexist;
- **sacrificial architecture** is intentionally replaceable structure with explicit scope, learning goal, and exit—not careless code.

### Central model, mechanism, or theorem

Represent a change-ready product architecture as

$$
P=(Y,H,K,V,S,E,R,L),
$$

where $Y$ is product outcomes and affected populations, $H$ falsifiable hypotheses and uncertainty, $K$ non-negotiable semantic and risk invariants, $V$ observed volatility, $S$ seams, ownership, and contracts, $E$ experiment and operational evidence, $R$ exposure, release, recovery, and authority, and $L$ lifecycle of flags, variants, data, dependencies, debt, and retirement. Optimize for learning inside $K$, not raw change count.

### Critical invariants

- every product change names an outcome, population, uncertainty, and stopping condition;
- correctness, safety, security, privacy, accessibility, financial, legal, and shared semantic constraints are not experiment variables unless legitimate authority says so;
- volatile policy is separated from stable identity, history, authorization, and audit semantics;
- a seam owns meaning and state, not just an interface type;
- deploy and release can be separated without creating ambiguous authority;
- every flag has type, owner, scope, default, observability, expiry, and removal path;
- experiments bound population, duration, data use, interaction effects, and harm;
- data schema and event changes remain compatible through every supported mixed-version state;
- rollback claims include state, data, external effects, and user consequences;
- platform and supplier dependencies have version, service, exit, and degraded behavior;
- change evidence includes product outcomes, rework, incidents, recovery, burden, and excluded cohorts;
- learned-stable behavior is consolidated and temporary variants are retired.

### Common failures

Common failures include equating high change with microservices; optimizing deployment count; creating one service per hypothesis; placing all policy in generic rule engines; calling a shared database flexible; treating JSON as a semantic contract; retaining flags indefinitely; running overlapping experiments without interference analysis; measuring average conversion while hiding harmed cohorts; using rollback after irreversible effects; building a generic platform for imagined scale; allowing product vocabulary to fork across channels; coupling every release to one integrated environment; and using “sacrificial” to excuse missing tests, ownership, or security.

### Compact example

A marketplace changes ranking and seller-promotion policy weekly, while order identity, money, consent, and fulfillment history must remain coherent. The architecture keeps authoritative order and ledger semantics in a stable core, exposes versioned eligibility and ranking seams, and records policy version with each decision. Candidate policies run offline, shadow, then for a bounded cohort behind expiring experiment flags. Guardrails block financial, privacy, accessibility, and seller-contract violations. Exposure can stop without erasing already committed orders; outcome and cohort evidence drive the next decision. Successful behavior is consolidated and the flag, duplicated path, and unused data are removed.

### Connections

[SARCH-072](072-evolutionary-architecture-principles.md) supplies invariant-preserving evolution. [SARCH-073](073-versioned-contracts-and-compatibility.md) and [SARCH-080](080-planning-architecture-evolution-across-multiple-releases.md) supply coexistence and sequencing. [SARCH-093](../ROADMAP.md) next examines a different dominant pressure: extreme read or write scale.

## Governing Question

Product teams learn by changing software and observing consequences. In a high-change domain, that loop is unusually frequent and the target itself moves: vocabulary changes, policy differs by market, workflows are contested, suppliers evolve, and yesterday's successful behavior becomes today's constraint. Architecture must shorten responsible learning without making every idea a permanent branch of the system.

The challenge is selective stability. Some concepts should change cheaply; others must remain coherent across every experiment. A fast checkout experiment cannot redefine money or lose orders. A recommendation test cannot silently change consent. An easily deployed service can still require five teams, a shared schema, and irreversible data migration. Changeability is therefore a system quality with semantic, operational, organizational, and ethical dimensions.

## Why This Matters

Lehman's work on software evolution describes continuing adaptation and complexity pressure for systems embedded in real activity [2]. Parnas distinguishes aging caused by failure to adapt from degradation caused by poorly controlled change [3]. These are explanatory frames, not schedules or universal laws. They show why both rigid architecture and uncontrolled flexibility carry cost.

ISO/IEC 25010:2023 is the current second edition of the product-quality model and defines nine quality characteristics for specifying and evaluating ICT and software products over their lifecycle [1]. Modularity, adaptability, reliability, security, interaction capability, and other qualities remain trade-offs; no single “agility” score establishes fitness.

The 2024 DORA research separates delivery throughput from instability and adds deployment rework rate alongside change failure rate [8]. The maintained metrics history, checked 2026-09-06, records that evolution [9]. These population-level research results inform measurement but do not prove that increasing deployment frequency will improve a specific product. The architecture must connect delivery capability to actual user and system outcomes.

## Prerequisites and Retrieval

Retrieve product outcome, hypothesis, experiment, population, cohort, counterfactual, uncertainty, volatility, option, expected value, invariant, constraint, domain model, bounded context, cohesion, coupling, information hiding, seam, contract, compatibility, deployment, release, feature flag, canary, shadow, observability, rollback, roll forward, blast radius, data authority, lineage, transition architecture, technical debt, platform, and decommissioning.

SARCH-061 through SARCH-070 provide trade-off, scenario, risk, fitness, coupling, capacity, reliability, threat, cost, and evidence methods. SARCH-071 through SARCH-080 provide drift, evolution, compatibility, decomposition, parallel run, migration, modernization, retirement, and roadmap mechanics. SARCH-081 through SARCH-091 supply organizational and governance boundaries. This module selects and composes those tools for high-change product work.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish product-domain change from deployment activity and infrastructure churn;
2. map observed volatility by concept, policy, interface, data, dependency, and consequence;
3. identify stable invariants without freezing uncertain product behavior;
4. design cohesive seams around meaning, authority, and independent change;
5. separate deployment, release, experiment, and authoritative effects;
6. govern feature flags and variants as temporary architecture;
7. design bounded experiments with guardrails and cohort evidence;
8. evaluate rollback, compatibility, data, platform, and supplier constraints;
9. measure learning flow together with stability, rework, and human outcomes; and
10. consolidate learning and retire temporary mechanisms before they become permanent complexity.

## Core Exposition

**Map change empirically.** Inspect product decisions, support cases, incidents, roadmap churn, schema history, dependency upgrades, regulatory changes, and code-change coupling. Interview people who understand why changes occurred. Record frequency, lead time, consequence, coordination, and uncertainty for concepts and decisions—not only files. A frequently edited utility may be stable semantics suffering poor boundaries; a rarely edited pricing rule may still be expected to change soon.

**Separate product uncertainty from engineering instability.** Product uncertainty concerns what users need, which policy works, or how a market behaves. Engineering instability concerns unreliable builds, fragile releases, incidents, or uncontrolled variants. Fast learning requires both the capacity to vary behavior and a trustworthy delivery/observation system. Do not celebrate churn caused by defects as product responsiveness.

**Name invariants before options.** Identify identity, money, inventory, authorization, privacy, accessibility, safety, audit, contractual, and domain consistency conditions that must hold across experiments. Some are local; some cross systems or organizations. State who may change them and what evidence is required. Invariants create the region inside which product options can be exercised safely.

**Find the learned-stable core.** Stability is evidenced by semantic centrality, accumulated dependencies, low legitimate variation, and high migration consequence—not by age. Customer identity or committed ledger history may form a core. Presentation order may not. Revisit the boundary as learning changes; “core” must not become a political label protecting one team or database.

**Place volatile decisions behind cohesive seams.** A seam should own vocabulary, input assumptions, output meaning, state, errors, version, authority, and lifecycle. A pricing seam that exposes tables to every caller does not hide the pricing decision. Separate policy from mechanism only where policy is genuinely coherent; one universal rules engine can erase domain types, scatter control flow, and make impact analysis harder.

**Choose deployment granularity from coordination evidence.** Independent processes help when a cohesive capability needs independent release, scale, isolation, security, or ownership. A modular monolith may give faster local feedback and transactional integrity when product boundaries are still moving. Microservices do not manufacture domain understanding; premature distribution hardens guesses into network contracts.

**Stabilize contracts, not implementations.** Define semantic preconditions, results, errors, identity, time, units, authorization, idempotency, and compatibility. Use version coexistence, expand-migrate-contract, consumer evidence, and retirement criteria. A flexible envelope or JSON object still breaks consumers when meaning, defaults, or omissions change.

**Separate deploy from release.** Deploy inactive code, data structures, and compatible contracts before exposing behavior. Release by cohort, account, geography, capability, or time only when the selection key is legitimate and observable. Keep one authority for irreversible effects. A hidden UI does not prevent a new background writer from acting.

**Classify flags.** Release flags support gradual exposure and should be short-lived. Experiment flags assign cohorts and preserve attribution. Operational flags change runtime response under explicit authority. Permission flags express durable entitlements and should use an authorization model, not an informal toggle. For each, record owner, type, default, evaluation point, population, dependencies, telemetry, fail behavior, expiry, and removal.

**Bound experiments.** Write hypothesis, primary outcome, guardrails, population, exclusions, duration, assignment, sample and interference assumptions, stopping rules, authority, and data use. Inspect heterogeneous effects rather than average outcome alone. Do not experiment with hard obligations or expose people to material harm merely because a flag makes rollout easy.

**Preserve attribution.** Record policy, model, content, schema, flag, dependency, and configuration versions with outcomes. Control simultaneous experiments whose interactions can confound evidence. Observe exposure actually received, not only assignment. Qualitative research and support evidence can explain why a numeric outcome moved.

**Treat observability as product architecture.** Trace a user or business outcome through decision, side effect, downstream state, correction, and recovery. Infrastructure health can remain green while customers receive duplicate charges or inaccessible content. Protect telemetry privacy, minimize collection, expose missing data, and prevent metrics from becoming worker surveillance.

**Design real reversal.** Rollback requires old code to understand new data, external effects to be compensable, contracts to remain supported, and authority to move safely. When reversal is impossible, use smaller cohorts, delayed commitment, parallel observation, reconciliation, and roll-forward repair. State the last reversible point before exposure.

**Manage data as accumulated commitment.** New fields and events create long-lived consumers, retention, privacy, lineage, and deletion obligations. Keep authoritative histories separate from experimental features. Backfill and derived data carry policy version and provenance. Remove unused experimental data after legitimate retention decisions; do not keep it “for future learning” by default.

**Build the smallest runway justified by a change horizon.** Forecast near-term product moves as scenarios, identify shared prerequisites, and implement only capabilities that reduce several evidenced constraints or protect a critical invariant. A generic multi-region, event, or plugin platform built for imagined futures consumes option value rather than creating it. Record adoption and exit assumptions.

**Control dependency volatility.** External APIs, frameworks, stores, models, and platforms change on their own cadence. Place anti-corruption boundaries around unstable semantics, pin exact versions, observe deprecations, test upgrades, retain exit data, and define degraded modes. Abstraction has value only if it preserves plausible alternatives at acceptable cost.

**Fund cleanup with the experiment.** Flags, duplicate paths, adapters, temporary schemas, shadow stores, and comparison telemetry are transition architecture. Define removal triggers and ownership before introduction. When a hypothesis succeeds, consolidate the chosen behavior. When it fails, remove its machinery and data. When evidence is ambiguous, time-box further learning rather than preserving every branch.

**Measure the whole learning system.** Track hypothesis-to-evidence time, decision latency, batch size, deployment lead time, failed-change recovery, change failure, rework, experiment cleanup, flag age, compatibility incidents, support demand, affected-cohort outcomes, accessibility, privacy, operational toil, and team cognitive burden. Metrics diagnose constraints; they do not rank individuals or prove value.

## Definitions and Notation

Let $P=(Y,H,K,V,S,E,R,L)$. $Y$ maps product outcomes to populations and accountable owners. $H$ contains hypotheses, alternatives, and uncertainty. $K$ contains non-compensable and bounded invariants. $V$ records observed and anticipated change by concept and consequence. $S$ maps seams to meaning, state, authority, contracts, and owners. $E$ contains experiment and operational evidence. $R$ defines deployment, release, authoritative effects, stop, rollback, and recovery. $L$ manages variants, flags, transition structures, data, dependencies, debt, and retirement.

For $n$ independent changes, each with failure probability $p$ over the declared horizon, the probability of at least one failure is

$$
P(\text{at least one})=1-(1-p)^n.
$$

With $p=0.02$ and $n=10$, this is $1-0.98^{10}\approx0.1829$. This model does not prove large batches fail more in practice: independence, equal probability, definition of failure, exposure, detection, and consequence may all be wrong. It illustrates why accumulating uncertain changes can widen the set of possible causes and effects.

A **decision half-life** is informal shorthand for how quickly the assumptions supporting a choice are expected to become materially stale. It is not a physical constant. Use it to set review cadence, not to manufacture precision.

## Mechanisms, Invariants, or Proof Structure

### Invariant-envelope rule

Every experiment and release names the invariant envelope it must preserve. Evidence of product benefit cannot compensate for violation of an applicable hard constraint. Unknown evidence routes to containment or review according to consequence.

### Single-authority rule

For each irreversible outcome identity, one path is authoritative at a time or a domain-approved reconciliation protocol governs concurrent authority. Shadow and experiment paths cannot silently duplicate charges, notifications, allocations, or legal decisions.

### Variant-lifecycle rule

Every introduced variant has identity, type, owner, scope, evidence, expiry, and removal. A successful experiment without consolidation and a failed experiment without deletion are incomplete architectural changes.

### Learning-integrity rule

Evidence connects assignment, actual exposure, configuration, outcome, cohort, missingness, and interference. Aggregate improvement cannot justify an unseen harmful subgroup or an invalid measurement pipeline.

### Executable change-route illustration

<!-- bijux-verify: {"id":"high-change-route","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"copy experiment: bounded-release\nledger rewrite: architecture-review\nunknown telemetry: evidence-inconclusive\nshared event removal: compatibility-plan\nexpired flag: retire-variant\nstable local rule: normal-delivery\n","stderr":""}} -->
```python
def route(*, hard_invariant, evidence_current, shared_contract,
          experiment, reversible, variant_expired):
    if variant_expired:
        return "retire-variant"
    if not evidence_current:
        return "evidence-inconclusive"
    if shared_contract:
        return "compatibility-plan"
    if hard_invariant:
        return "architecture-review"
    if experiment:
        return "bounded-release" if reversible else "architecture-review"
    return "normal-delivery"

cases = {
    "copy experiment": (False, True, False, True, True, False),
    "ledger rewrite": (True, True, False, True, False, False),
    "unknown telemetry": (False, False, False, True, True, False),
    "shared event removal": (False, True, True, False, False, False),
    "expired flag": (False, True, False, True, True, True),
    "stable local rule": (False, True, False, False, False, False),
}
for name, facts in cases.items():
    print(f"{name}: {route(hard_invariant=facts[0], evidence_current=facts[1], shared_contract=facts[2], experiment=facts[3], reversible=facts[4], variant_expired=facts[5])}")
```

This finite router demonstrates decision ordering, not a production risk model. Real routing also needs legitimate authority, multidimensional consequences, affected populations, data effects, observability, recovery evidence, and explicit handling for facts that remain unknown.

### Proposition: deployment frequency does not imply learning

Suppose a team deploys one hundred times but measures no product exposure or outcome; another deploys once and obtains valid evidence that rejects a major hypothesis. The first has higher deployment frequency and can have less product learning. Therefore deployment frequency alone cannot establish learning rate.

### Proposition: configurability does not imply change independence

Suppose ten policies are data rows in one generic rule engine, but every change requires global regression, shared deployment, and one expert. Configuration changed representation but not coordination. Therefore a configurable mechanism can remain tightly coupled.

## Alternatives and Trade-Offs

**Modular monolith versus services.** One process gives fast tests and strong transactions; services offer independent release and isolation at network and operational cost. Choose from observed coupling and outcomes, not the perceived modernity of topology.

**Code versus rules or data.** Externalized policy can improve review and runtime variation. It can also weaken types, scatter control flow, and create a second programming language. Use it for bounded coherent policy with equivalent tests, versioning, and observability.

**Build versus platform.** A shared platform removes repeated complexity but creates dependency, common failure, and roadmap coupling. Build a platform when product demand repeats and consumers shape it; otherwise use a local capability with an exit seam.

**Experiment versus judgment.** Experiments estimate selected causal effects under assumptions. Domain expertise, qualitative evidence, law, ethics, and strategy address questions experiments cannot. Never randomize merely because instrumentation exists.

**Reversible shortcut versus durable design.** A bounded shortcut can buy learning and preserve option value. It becomes debt when its condition and exit are lost. Fund characterization, monitoring, security, cleanup, and decision dates with the shortcut.

## Failure Modes and Misconceptions

1. **“High change means deploy often.”** Product meaning may be static while engineering churns.
2. **“Microservices create agility.”** They can harden uncertain boundaries.
3. **“A stable core never changes.”** It changes deliberately through governed migration.
4. **“Everything volatile belongs in configuration.”** Generic rules can destroy types and cohesion.
5. **“JSON is flexible.”** Consumers still depend on semantics.
6. **“Feature flags are not architecture.”** They multiply reachable configurations.
7. **“Deploy equals release.”** Inactive code and authoritative exposure differ.
8. **“Rollback is always available.”** Data and external effects may be irreversible.
9. **“Average uplift proves benefit.”** A cohort can be harmed.
10. **“More experiments mean more learning.”** Confounding and weak measures can reduce knowledge.
11. **“A platform always increases speed.”** Provider queues and lock-in can slow teams.
12. **“One generic model prevents duplication.”** It may erase domain truth.
13. **“Small diffs have small risk.”** A one-line authorization change can have wide consequence.
14. **“Options are free.”** Abstractions and variants have carrying cost.
15. **“Sacrificial means low quality.”** Temporary systems still need bounded risk and ownership.
16. **“Telemetry is objective.”** Selection, missingness, definitions, and incentives shape it.
17. **“Successful experiments can remain flagged.”** Unremoved variants preserve complexity.
18. **“Changeability outranks every quality.”** It is one concern inside legitimate constraints.

## Worked Examples

### Example 1

**Situation.** A subscription team changes offer copy daily but billing recognition rules rarely change.

**Reasoning.** Map volatility separately. Put copy and presentation behind a bounded content seam; keep contract identity, price, currency, consent, tax, and ledger semantics in a governed core. Record which offer version produced an agreement.

**Conclusion.** Selective stability makes frequent presentation learning compatible with durable financial meaning.

### Example 2

**Situation.** A startup proposes one microservice for every new product hypothesis.

**Reasoning.** Hypotheses are expected to fail and boundaries are uncertain. Begin with cohesive modules, ownership, flags, and outcome evidence inside one deployable where possible. Extract only when independent scale, release, isolation, or ownership is repeatedly valuable.

**Conclusion.** Logical seams preserve options without paying premature distribution cost.

### Example 3

**Situation.** A checkout experiment changes button text but a background worker begins reserving stock for the candidate path.

**Reasoning.** UI exposure is not effect authority. Fence reservation by experiment cohort and idempotent order identity, or keep candidate behavior shadow-only. Observe abandoned reservations and ensure stop removes provisional state.

**Conclusion.** Release architecture must bound downstream effects, not merely visible presentation.

### Example 4

**Situation.** An experiment increases average conversion by 3%.

**Reasoning.** Inspect assignment, exposure, missingness, multiple tests, duration, novelty, refunds, support, latency, accessibility, and cohort effects. One protected cohort sees more failed checkouts. Stop expansion, investigate mechanism, and do not average the harm away.

**Conclusion.** Product evidence requires guardrails and heterogeneous outcomes.

### Example 5

**Situation.** A release flag is still evaluated two years after full rollout.

**Reasoning.** Find owner, evaluation points, defaults, tests, configuration, and dependencies. Verify one behavior is authoritative, remove dead path and flag data, simplify tests and telemetry, and retain the durable decision record. If the flag represents entitlement, migrate it to authorization semantics.

**Conclusion.** Flag retirement completes the architectural change.

### Example 6

**Situation.** A new seller-ranking policy must change weekly.

**Reasoning.** Define typed eligibility, scoring inputs, policy version, explanation, fairness and contractual guardrails, fallback, replay, and outcome evidence. Keep order and payment authority outside ranking. Shadow and canary policies before bounded release; preserve seller appeal.

**Conclusion.** A policy seam owns meaning and evidence rather than becoming arbitrary executable configuration.

### Example 7

**Situation.** A team promises instant rollback after changing a customer-status schema.

**Reasoning.** Old readers reject the new state and emails have already been sent. Use expand-migrate-contract, suppress new emission until consumers are ready, make notifications idempotent and correctable, and prefer roll-forward for committed semantics. Test every mixed version.

**Conclusion.** Reversal is a system property, not a deployment command.

### Example 8

**Situation.** Product leaders request a generic event platform for possible future domains.

**Reasoning.** Identify two near-term capabilities, throughput, ordering, privacy, retention, schema, operations, and ownership needs. Implement the smallest shared transport and evidence that serves them, preserving an exit boundary. Defer universal workflow and canonical-data machinery until repeated demand appears.

**Conclusion.** Evidence-bounded runway preserves more options than speculative generality.

### Example 9

**Situation.** A supplier API changes quarterly and forces synchronized product releases.

**Reasoning.** Place a domain-owned anti-corruption boundary around supplier vocabulary, version it internally, record provenance, test both versions, cache only within valid semantics, and define degraded behavior and exit data. Do not abstract features no plausible alternate supplier supports.

**Conclusion.** A narrow semantic boundary contains external volatility without pretending vendors are interchangeable.

### Example 10

**Situation.** A public-benefits portal experiments with application guidance during a policy change.

**Reasoning.** Keep eligibility law, submitted evidence, decision authority, appeal, language, accessibility, privacy, and audit invariant. Experiment only with approved guidance presentation on a bounded population, ensuring no applicant loses deadline or channel access. Measure completion, comprehension, errors, support, and subgroup outcomes; include caseworkers and affected communities. Consolidate proven guidance and delete unnecessary experiment data.

**Conclusion.** High-change public products can learn rapidly without treating rights or access as experiment variables.

## Cross-Program Connections

- [Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) owns variation, indirection, modularity, and the costs of generic mechanisms.
- [Testing and Software Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns experiment validity, test design, oracles, and regression evidence.
- [Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) owns continuous delivery, progressive release, telemetry, recovery, and operational metrics.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns durable meaning, authority, lineage, privacy, and data lifecycle.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns authorization, threat, experiment abuse, and secure delivery.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns paved roads, consumer-oriented platform capabilities, and self-service constraints.

## References

1. ISO/IEC, [ISO/IEC 25010:2023, *Systems and software engineering — SQuaRE — Product quality model*](https://www.iso.org/standard/78176.html), 2nd ed., November 2023; official published status checked 2026-09-06.
2. Meir M. Lehman, “Programs, Life Cycles, and Laws of Software Evolution,” *Proceedings of the IEEE*, vol. 68, no. 9, pp. 1060–1076, 1980, [DOI 10.1109/PROC.1980.11805](https://doi.org/10.1109/PROC.1980.11805).
3. David L. Parnas, “Software Aging,” *Proceedings of the 16th International Conference on Software Engineering*, pp. 279–287, 1994, [DOI 10.1109/ICSE.1994.296790](https://doi.org/10.1109/ICSE.1994.296790).
4. Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2003. Domain models, bounded contexts, and anti-corruption layers.
5. Jez Humble and David Farley, *Continuous Delivery*, Addison-Wesley, 2010. Deployment pipelines, releasability, and configuration discipline.
6. Neal Ford, Rebecca Parsons, Patrick Kua, and Pramod Sadalage, [*Building Evolutionary Architectures*](https://www.oreilly.com/library/view/building-evolutionary-architectures/9781492097532/), 2nd ed., O'Reilly, November 2022.
7. Pete Hodgson, [“Feature Toggles (aka Feature Flags)”](https://martinfowler.com/articles/feature-toggles.html), October 2017. Flag categories, configuration, testing, and carrying cost.
8. DORA, [*Accelerate State of DevOps Report 2024*](https://dora.dev/research/2024/dora-report/), report version 2024.3. Throughput, instability, rework, user focus, and platform findings with observational limitations.
9. DORA, [“A History of DORA's Software Delivery Metrics”](https://dora.dev/insights/dora-metrics-history/), maintained research history updated January 2026; checked 2026-09-06.
10. Ronny Kohavi, Diane Tang, and Ya Xu, *Trustworthy Online Controlled Experiments*, Cambridge University Press, 2020. Experiment design, guardrails, and interpretation.
11. Nicole Forsgren, Jez Humble, and Gene Kim, *Accelerate*, IT Revolution, 2018. Delivery capabilities and empirical software-performance context.
12. Matthew Skelton and Manuel Pais, [*Team Topologies*](https://teamtopologies.com/book), 2nd ed., IT Revolution, September 2025; official publisher and maintained concept record checked 2026-09-06.

## Exercises

### Exercise 1

Distinguish high product-domain change, high deployment frequency, and engineering instability. Give one example where each occurs without the other two.

### Exercise 2

Under the illustrative independence model, compute the probability of at least one failure across 20 changes when each has $p=0.01$. State at least five reasons the result cannot determine a safe batch size.

### Exercise 3

Diagnose this proposal: “Put every business rule in one dynamic JSON rules service so all teams can change instantly.” Identify at least ten architectural risks and propose a more coherent boundary strategy.

### Exercise 4

Design the hypothesis-to-retirement lifecycle for a new marketplace search-ranking policy. Include invariants, seams, data, flags, exposure, evidence, rollback, authority, and cleanup.

### Exercise 5

A humanitarian cash-assistance service must adapt weekly to changing eligibility policy, intermittent field connectivity, fraud, currency volatility, privacy, accessibility, partner organizations, and beneficiary appeal rights. Design a high-change architecture that protects stable meaning and authority.

## Answers to the Exercises

### Answer 1

High product change occurs when a policy team revises eligibility weekly even if releases are manual and reliable. High deployment frequency occurs when a stable infrastructure component receives many safe dependency and configuration releases without product-semantic change. Engineering instability occurs when repeated hotfixes and rollbacks repair defects although the desired product behavior is stable. The dimensions can interact, but using deployment count as a proxy for product learning confuses them. A valid answer identifies changed meaning, delivery activity, and unplanned failure separately.

### Answer 2

$1-(1-0.01)^{20}=1-0.99^{20}\approx1-0.8179=0.1821$, about 18.21%. It cannot choose batch size because failures may not be independent; changes have unequal probabilities and consequences; “failure” and horizon are unspecified; interactions can create or prevent faults; exposure and detection differ; repeated release overhead matters; one change may be irreversible; and the inputs are hypothetical. The model illustrates accumulated opportunity under assumptions, not acceptable risk or causal benefit from splitting.

### Answer 3

Risks include erased domain vocabulary; weak types; runtime parser failure; ambiguous defaults; shared availability and latency; one global deployment and test scope; policy conflicts; hidden evaluation order; unrestricted code-like behavior; authorization ambiguity; data overexposure; version and replay gaps; poor explanation; one expert bottleneck; cross-team priority; blast radius; and permanent stale rules. Map actual rule families and invariants first. Keep cohesive volatile policy with its owning bounded context, using typed inputs, outputs, version, authority, tests, provenance, and replay. Share a mechanism library or platform only for repeated evaluation, audit, rollout, and observability needs while leaving semantics domain-owned. Use explicit contracts between domains and reserve hard legal or safety interpretation for legitimate authorities.

### Answer 4

Define a hypothesis about a named search outcome and seller/buyer cohorts. Preserve identity, consent, prohibited-content, contractual, accessibility, privacy, payment, and order invariants. Place ranking behind a typed domain seam with policy and feature versions, input provenance, explanation, fallback, and replay. Evaluate offline and shadow first, then use an expiring experiment flag with stable assignment, bounded traffic, interaction controls, guardrails, and stopping thresholds. Measure actual exposure, relevance, conversion, diversity, latency, complaints, support, seller impact, and subgroup harm. Keep ranking nonauthoritative over orders and money. Roll back exposure if no irreversible effect exists; otherwise repair and roll forward. Product, domain, privacy, accessibility, security, and contractual authorities retain their decisions. On success consolidate the policy and remove old branch, flag, shadow data, and obsolete telemetry; on failure remove candidate machinery and record learning.

### Answer 5

Keep beneficiary identity, application history, policy provenance, money, consent, appeal, audit, and partner authority in a stable semantic core. Version eligibility policies by jurisdiction and effective interval; never overwrite the rule used for a prior decision. A typed evaluation seam accepts authoritative facts with provenance and returns result, reasons, missing evidence, policy version, and appeal route. Separate policy interpretation authority from software deployment. Field clients cache signed policy and bounded spending or case rights, expose staleness, preserve local drafts, and reconcile idempotently after reconnect; they cannot silently invent current eligibility.

Use compatible schemas, store-and-forward events, explicit conflict policy, currency and time units, encrypted least-data storage, device revocation, accessible and multilingual workflows, and human support. Test weekly policy candidates against historical and adversarial cases, shadow before authority, and canary only where rights are protected. Hard guardrails cover duplicate payment, unauthorized decision, lost appeal, exclusion, privacy, and inaccessible mandatory steps. Monitor missing and delayed data, fraud signals with contestability, payment outcomes, cohort errors, partner burden, connectivity, support, and appeals. Flags and duplicated policies expire after effective-date migration and reconciliation. Partner, financial, legal, privacy, accessibility, security, field, and affected-community authorities govern their consequences. Rapid change remains inside stable rights, evidence, and correction semantics.
