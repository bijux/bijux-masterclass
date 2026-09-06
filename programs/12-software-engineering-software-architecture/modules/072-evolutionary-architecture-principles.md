---
module_id: SARCH-072
program: Software Engineering: Software Architecture
level: 2
module_number: 72
title: Evolutionary Architecture Principles
status: complete
last_verified: 2026-09-06
---

# Evolutionary Architecture Principles

## One-Page Review

### Governing question

How can architects shape a system so it can change incrementally across structure, behavior, data, deployment, security, operations, and organization while preserving critical properties and learning before commitments become irreversible?

### Essential definitions

- an **evolutionary architecture** supports guided, incremental change across multiple architectural dimensions;
- an **architectural dimension** is one independently meaningful axis of change or evaluation, such as availability, data authority, deployability, cost, privacy, or team ownership;
- **guided change** has an explicit direction, constraints, evidence, and accountable decisions rather than treating all change as progress;
- an **increment** is a bounded transition that can be built, observed, and evaluated without requiring the entire target architecture to exist;
- an **invariant envelope** is the set of nonnegotiable properties every admitted transition must preserve under stated conditions;
- **reversibility** is the practical ability to return to an acceptable state, including restoration of data and external commitments—not merely reverting source;
- **optionality** is the availability of feasible future choices; an option has value only if the organization can exercise it;
- a **fitness function** is an objective evaluation of an architectural characteristic, not a scalar score for the whole architecture;
- an **evolution hypothesis** predicts how a bounded change will affect named outcomes and what evidence would challenge that prediction;
- **retirement evidence** demonstrates that an old path, contract, datum, dependency, or responsibility can be removed without violating the transition's acceptance conditions.

### Central model, mechanism, or theorem

Model evolution as a sequence of states $x_0,x_1,\ldots,x_n$. Let $K_t$ be the invariant envelope applicable at time $t$, $G$ a desired outcome region, and $q(x_t,e_t)$ a vector of measured or judged characteristics under environment $e_t$. An admissible transition requires

$$
x_t\in K_t\quad\land\quad x_{t+1}\in K_{t+1}
$$

plus stated preconditions, evidence, observation, and recovery. Reaching $G$ is not sufficient if an intermediate state violates a critical invariant. Conversely, keeping every invariant does not prove the destination is valuable. Architecture evolves through a controlled loop: frame, constrain, change, observe, compare, decide, and retain or revise.

### Critical invariants

- every increment has a stakeholder outcome, hypothesis, bounded scope, owner, and stopping rule;
- critical safety, integrity, security, legal, and availability properties apply to intermediate states as well as the destination;
- multiple dimensions are evaluated together; local improvement may create system-wide harm;
- observation precedes irreversible expansion or retirement;
- rollback claims include state, schema, messages, identities, clients, and external side effects;
- compatibility and coexistence are designed explicitly when old and new paths overlap;
- fitness evidence is versioned and interpreted within its environment and coverage;
- options are not accumulated without expiry, cost ownership, and exercise tests;
- obsolete assumptions and target states can be revised without hiding the decision;
- migration completes only when superseded paths and controls are deliberately retired.

### Common failures

Common failures include equating evolutionary with unplanned; declaring a fixed five-year diagram while ignoring feedback; optimizing one dimension; treating a feature flag as rollback; making irreversible schema or public-contract changes first; running old and new paths without a single authority; collecting telemetry without decision thresholds; preserving every option forever; confusing component deployment with end-to-end independence; migrating without decommission criteria; using temporary duplication as permanent architecture; automating shallow proxies; making experiments on nonconsenting or safety-critical populations; and assuming small changes have small blast radii.

### Compact example

A billing team wants to replace a rating engine. It first defines invariants: no duplicate charge, every accepted usage record reaches one auditable terminal state, and operators can route new work back within five minutes. The new engine shadows inputs without authority, then rates a synthetic cohort, then a small reversible production cohort while old and new outputs are reconciled. Expansion stops when discrepancy exceeds a stated bound. Only after representative billing cycles, recovery exercises, client migration, and ledger reconciliation does the team remove the old engine. The architecture changes through evidence-bearing states rather than one cutover promise.

### Connections

[SARCH-064](064-architecture-fitness-functions.md) develops characteristic-specific feedback, and [SARCH-071](071-architectural-drift-and-erosion.md) distinguishes legitimate evolution from damaging divergence. [SARCH-073](../ROADMAP.md) next develops the compatibility mechanics required when contracts evolve.

## Governing Question

Architecture makes some changes easier and others harder. Because requirements, threats, workloads, suppliers, laws, teams, and technologies change, a design optimized for one forecast can become a constraint. Yet “we will evolve it later” is not a mechanism. Evolutionary architecture makes the capacity to change an explicit quality, and it couples that capacity to guidance and evidence.

The core challenge is temporal. A destination diagram hides the states required to reach it. A safe final topology may require an unsafe data backfill, ambiguous dual authority, incompatible clients, or an untested recovery period. Architects must reason about the path, including intermediate invariants, operational control, learning, and retirement.

## Why This Matters

Long-lived software participates in a changing environment. Lehman's work on software evolution described continuing change and increasing complexity pressures in systems embedded in real-world activity [2]. Parnas distinguished aging caused by failure to adapt from degradation caused by changes made without sufficient understanding [3]. These are not laws that predict a particular system's future, but they frame a durable engineering reality: both stasis and uncontrolled modification can cause harm.

Large irreversible changes concentrate uncertainty. The organization learns about workload, failure, usability, integration, and operations only after much of the commitment has been made. Smaller transitions can produce earlier evidence and preserve alternatives. Smallness alone, however, is insufficient. A one-line authorization change or schema deletion can have enormous consequences. Increment size must be judged by blast radius, reversibility, and evidence—not diff lines.

Evolution also spans organizational and economic boundaries. A component may be modular in source yet require synchronized releases, one specialist, a shared database, or a supplier negotiation. An architecture becomes evolvable when technical seams, operational controls, evidence pipelines, decision authority, funding, and team capability align.

## Prerequisites and Retrieval

Retrieve architecture, stakeholder concern, quality attribute, architectural decision, rationale, constraint, invariant, precondition, postcondition, interface, contract, compatibility, coupling, cohesion, modularity, information hiding, abstraction, authority, state transition, feedback loop, leading and lagging indicator, experiment, control, canary, shadow traffic, feature flag, observability, rollback, roll forward, blast radius, error budget, technical debt, expected value, option, migration, and decommissioning.

SARCH-051 through SARCH-060 provide distributed failure mechanisms. SARCH-061 through SARCH-070 provide scenario, risk, fitness, coupling, capacity, reliability, threat, cost, and review methods. SARCH-071 provides drift and erosion control. This chapter integrates those capabilities into evolution principles; later chapters provide detailed compatibility, decomposition, parallel-run, data-migration, and decommissioning mechanics.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish evolutionary architecture from adaptation, maintenance, arbitrary emergence, and periodic replacement;
2. define outcome direction and an invariant envelope without pretending to predict a fixed terminal design;
3. decompose architectural change into evidence-bearing transitions across multiple dimensions;
4. formulate evolution hypotheses, measures, thresholds, stopping rules, and decision rights;
5. evaluate practical reversibility across code, state, contracts, data, identity, and external effects;
6. use modularity, information hiding, compatibility, isolation, and replaceability to preserve options;
7. design nested feedback loops with appropriate cadence and evidence limits;
8. manage temporary coexistence, duplication, flags, adapters, and migration debt;
9. decide when to expand, revise, contain, reverse, roll forward, or retire an evolutionary path;
10. govern evolution in high-consequence environments without substituting experimentation for required assurance.

## Core Exposition

**Define evolutionary architecture precisely.** Ford, Parsons, Kua, and Sadalage define an evolutionary architecture around guided, incremental change across multiple dimensions [1]. Each term prevents a common distortion. *Guided* excludes directionless accumulation. *Incremental* makes transitions and feedback visible. *Multiple dimensions* prevents a local metric from becoming the architecture.

Evolution differs from runtime adaptation. An adaptive system changes behavior or configuration in response to conditions through mechanisms already designed into it. Architectural evolution changes significant structures, responsibilities, constraints, or their rationale across time. An adaptive controller can itself evolve, but autoscaling alone is not architectural evolution.

Maintenance is broader: it includes defect correction, environment adaptation, enhancement, and prevention. Some maintenance is architecturally insignificant. Evolutionary architecture concentrates on preserving the ability to make consequential change while protecting important outcomes.

**Choose direction, not a fictional final certainty.** State the outcomes the architecture should increasingly enable: independent regional recovery, bounded data exposure, faster safe product variation, lower marginal cost, supplier replaceability, or another stakeholder result. Add constraints and time horizons. Avoid a universal label such as “become cloud native.”

A target architecture can coordinate near-term work, but it is a revisable hypothesis. Record what evidence or environmental change would cause revision. Separate durable principles—such as one authority for a financial decision—from provisional choices—such as a particular queue product.

**Define the invariant envelope.** Some properties cannot be traded away during migration: no duplicate financial settlement, no unsafe command, no unauthorized disclosure, preservation of an auditable record, or continuity above an agreed threshold. Express each invariant with scope, assumptions, enforcement, observation, and authority.

The envelope can change through accountable governance, but not silently because a transition is inconvenient. In regulated or safety-critical systems, qualified hazard analysis, independent assurance, change control, and authorization may define the admissible states. Architecture practice supports those processes; it does not replace them.

**Model the path as states and transitions.** Describe the current state $x_0$, the next bounded state $x_1$, and the evidence needed before $x_2$. Each transition names preconditions, changes, expected outcome, affected dimensions, monitoring, threshold, recovery, duration, and retirement implications.

This exposes unsafe middle states. A destination with one clean database per domain may require a period of replicated records, dual formats, and reconciliation. A new identity boundary may require temporary translation. The transition architecture deserves the same rigor as the target because users experience it in production.

**Build increments around learning.** A useful increment answers a decision-relevant question. “Deploy the new engine” is an activity. “Determine whether the new engine preserves invoice totals within the defined reconciliation rules at representative peak mix” is a learning objective.

Select the smallest cohort, traffic shape, dataset, region, internal consumer, or shadow mode that produces relevant evidence without exposing unacceptable consequence. Define how evidence changes the next decision. If every outcome leads to expansion, the activity is rollout theater rather than an experiment.

**State evolution hypotheses.** A hypothesis links mechanism to outcome: “Isolating recommendation computation behind an asynchronous boundary will prevent its saturation from consuming checkout request capacity.” State alternatives and counterevidence. Name metrics at both the local mechanism and stakeholder outcome.

Do not convert architecture into only statistically randomized experimentation. Many changes cannot be randomized, samples may be dependent, and safety or fairness constraints may prohibit exposure. Analytical models, simulations, formal reasoning, tests, recovery exercises, production observation, incident history, and expert judgment provide different evidence. Match the method to the claim.

**Evaluate multiple dimensions.** A change that improves deployability may worsen consistency, privacy, cost, latency, cognitive load, or recovery. Identify dimensions before the transition and define which are constraints, objectives, or monitored side effects. SARCH-062 provides scenario structure and SARCH-063 provides trade-off reasoning.

Never collapse a heterogeneous vector into a weighted score without defensible measurement and authority. A score can hide a noncompensable safety constraint: enough cost savings do not cancel an unauthorized command path. Present Pareto trade-offs and accountable decisions where dimensions cannot be reduced legitimately.

**Protect options through information hiding.** Parnas's extension-and-contraction work emphasizes structures that permit subsets and extensions without pervasive change [4]. Hide volatile decisions behind stable responsibilities. A module boundary is valuable when likely changes remain localized and externally visible assumptions are limited.

Stability does not mean immutability. A stable boundary has deliberate evolution rules, semantic ownership, and consumers that are not coupled to incidental implementation. Avoid prematurely generalizing every possible future. An abstraction over one example usually preserves imagined options while adding real complexity.

**Make replaceability concrete.** To claim a component is replaceable, identify contracts, data, identities, operational controls, observability, deployment, licenses, supplier obligations, skills, and exit mechanisms. Exercise replacement seams with a fake, secondary implementation, import/export test, or disaster scenario where appropriate.

A vendor-neutral interface that leaks proprietary semantics is not a practical option. Neither is an unused export format that cannot preserve history. Option value depends on the cost and time to exercise the option under the conditions in which it would be needed.

**Prefer reversible decisions under high uncertainty.** Delay a commitment only while waiting can produce valuable information and options remain feasible. The “last responsible moment” is not the latest conceivable date; it is the last point before delay destroys an important option, increases exposure, or forces rushed execution.

Reversibility is a spectrum. Reverting a binary may be easy while reversing schema deletion, customer communication, copied personal data, physical-device firmware, or an external financial action is impossible. Classify decisions by reversibility and front-load evidence for costly-to-reverse commitments.

**Distinguish rollback from recovery.** A deployment rollback restores a prior software artifact. It may not restore data, queued messages, issued tokens, external side effects, or client expectations. Define a recovery state that remains acceptable and test the whole procedure.

Sometimes rolling forward is safer than rollback because state has crossed a compatibility boundary. Record that condition before rollout. Ensure operators know which mechanism applies and have authority, signals, and time to use it.

**Use expand-and-contract change.** Introduce a new path without immediately removing the old one; migrate bounded use; observe and reconcile; expand; then retire the old path. This pattern applies to interfaces, schemas, dependencies, identity policies, data stores, and deployment topologies.

Coexistence creates its own architecture. Define authority, routing, duplication, consistency, failure behavior, and duration. “Both systems run” is unsafe when both can authoritatively mutate the same business fact. Later modules develop contract, decomposition, parallel-run, and data-migration variants.

**Separate observation from authority.** Shadow execution can compute outcomes without committing them, allowing comparison with lower consequence. A canary receives authoritative work for a bounded cohort, so rollback and state reconciliation matter. Parallel run may mean observation, dual calculation, dual write, or dual authority; these are not interchangeable.

State which path decides, which records are evidence, how nondeterminism is handled, and what discrepancy threshold means. Do not expose users or sensitive data to experimental paths without appropriate consent, privacy, legal, safety, and security controls.

**Automate characteristic-specific guidance.** Fitness functions turn selected architectural intentions into repeatable feedback. Use source rules, contract tests, policy evaluation, performance and reliability experiments, cost checks, threat controls, deployment observations, and human reviews at suitable cadences.

Automation is most useful for stable, observable constraints. It can also ossify proxies. Version functions beside rationale, test them for false results, and review whether they still predict the concern. SARCH-064 covers their design and evidence limits in depth.

**Nest feedback loops.** Fast loops catch cheap defects during editing and integration. Deployment loops evaluate compatibility, policy, and canary behavior. Operational loops detect workload and failure effects. Quarterly or event-triggered reviews reconsider assumptions, suppliers, regulations, organization, and architectural direction.

Cadence must match change speed and consequence. A yearly review cannot control daily topology drift; a per-commit test cannot assess rare disaster recovery. Connect loops so that operational evidence can change design rules and design hypotheses can change telemetry.

**Manage blast radius.** Bound exposure by tenant, region, request class, data classification, internal population, feature, capacity cell, or time window. Isolation must match failure mechanism. A regional canary does not contain failure when regions share a global control plane or ledger.

Define escalation steps and automatic or human stop authority. Measure both the cohort and unaffected control population. Verify that routing and kill mechanisms work during degraded conditions, not only when the control plane is healthy.

**Treat feature controls as architecture.** Flags, routing rules, configuration, and policy gates can separate deployment from activation and make increments possible. They also create state combinations, testing burden, hidden dependencies, and security exposure. Record owner, purpose, allowed combinations, expiry, and removal evidence.

A flag is not rollback if both branches mutate incompatible data or an old client cannot interpret the new state. Long-lived flags become variation points and should be designed and governed as such. Short-lived flags should be removed when their decision closes.

**Budget temporary complexity.** Adapters, replicated data, duplicate computation, translation layers, and compatibility branches enable safer change but increase operational surface. Name them as transition architecture with cost, risk, owner, and sunset conditions.

Do not optimize transition code as if it must live forever, but do not make it unobservable or unsafe. Temporary mechanisms often outlive forecasts. Include them in threat, capacity, support, and recovery reasoning for as long as they exist.

**Preserve a single source of authority.** During migration, distinguish system of record, decision authority, read model, cache, replica, comparison output, and audit record. Dual writes can fail partially; dual readers can observe different versions; reconciliation can conceal semantic disagreement.

Assign authority per business fact and transition state. If authority transfers, define the exact event, fencing, replay, rollback implications, and audit. Data migration receives dedicated treatment in SARCH-076.

**Make compatibility a temporal property.** Producers and consumers rarely change simultaneously. Design a compatibility window across deployed versions, stored data, queued messages, replay, rollback, and external clients. Test mixed-version states, not only old-only and new-only endpoints.

Compatibility can reduce immediate coordination but adds semantic and testing cost. Plan its removal. SARCH-073 develops backward, forward, full, and behavioral compatibility without compressing them into “nonbreaking.”

**Align teams with increments.** A technically small transition can require five approval queues and synchronized work across teams. Give a team the authority and capability to execute, observe, and recover its bounded change, or explicitly manage the coordination as part of the architecture.

Platforms can reduce the cost of safe evolution through reusable routing, telemetry, policy, environments, and rollback capabilities. A mandatory platform that cannot support a necessary experiment becomes an architectural constraint. Team and governance structures are developed in SARCH-081 through SARCH-090.

**Control work in progress.** Many simultaneous migrations multiply coexistence states, cognitive load, and interaction risk. Limit active architecture transitions, especially when they share data or infrastructure. Make blocked retirement visible rather than starting new fronts indefinitely.

Sequence by dependency and learning. Resolve the uncertainty that changes other decisions first. Avoid building downstream target components before validating the boundary or data semantics they depend on.

**Plan retirement from the beginning.** Define how the organization will know that old code, data, contract versions, identities, routes, infrastructure, support procedures, licenses, and dashboards are unused. Absence of traffic over one interval may be weak evidence for seasonal or offline consumers.

Retirement is not housekeeping after evolution; it realizes the simplification and removes attack, cost, and cognitive surfaces. If removal is impossible, the architecture has accumulated another permanent variant. SARCH-079 examines decommissioning in depth.

**Revisit the path when evidence changes.** At every decision gate, choose to expand, hold, revise, contain, reverse, roll forward, or stop. Preserve observations and rationale. Do not treat sunk cost as evidence that the target remains correct.

An evolutionary architecture is successful when it changes direction responsibly, not when it completes every original roadmap item. The destination, constraints, and environment can change; the integrity of the evidence-and-decision process must remain visible.

## Definitions and Notation

Let:

- $X$ be the set of representable architectural states;
- $x_t\in X$ be the architecture state admitted at decision time $t$;
- $e_t$ be the relevant environment, workload, threat, and organizational conditions;
- $K_t\subseteq X$ be the invariant envelope applicable at $t$;
- $G_t\subseteq X$ be a revisable desired outcome region rather than one exact target;
- $\Delta_t:x_t\mapsto x_{t+1}$ be a proposed bounded transition;
- $q(x_t,e_t)=(q_1,\ldots,q_m)$ be a vector of characteristic evidence;
- $h_t$ be the evolution hypothesis for $\Delta_t$;
- $B(\Delta_t)$ be its potential blast-radius set;
- $\rho(\Delta_t)$ be a structured reversibility assessment, not a universal scalar;
- $E_t$ be evidence collected before, during, and after the transition;
- $d_t$ be the accountable decision to expand, hold, revise, contain, reverse, roll forward, or stop.

The state model is deliberately abstract. A real state includes code, data, contracts, deployment, configuration, identities, external commitments, and operational readiness. Membership in $K_t$ is a claim requiring concern-specific evidence.

## Mechanisms, Invariants, or Proof Structure

**Path-safety proposition.** Suppose a final state $x_n$ belongs to $K_n$. This fact alone does not imply that the path is admissible. A counterexample requires only an intermediate $x_j\notin K_j$. Therefore destination review cannot replace transition review. A sufficient modeled condition is $x_i\in K_i$ for every admitted $i$, plus valid evidence that the model corresponds to reality.

**No monotonicity assumption.** An improvement in $q_1$ need not improve $q_2$. For example, synchronous calls may reduce data staleness while increasing latency coupling and failure propagation. Therefore $q(x,e)$ remains a vector unless a legitimate decision model supplies comparable units and weights. Pareto improvement is possible but not guaranteed at each temporary state.

**Executable transition check.** The following finite example checks a few declared invariants for a staged route migration.

<!-- bijux-verify: {"id":"check-evolution-states","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"baseline: valid\nshadow: valid\ncanary: valid\nexpanded: valid\nretired: valid\nall_states_valid=true\n","stderr":""}} -->
```python
states = [
    {"name": "baseline", "old": True,  "new": False, "share": 0,   "rollback": False, "retire_evidence": False},
    {"name": "shadow",   "old": True,  "new": True,  "share": 0,   "rollback": True,  "retire_evidence": False},
    {"name": "canary",   "old": True,  "new": True,  "share": 5,   "rollback": True,  "retire_evidence": False},
    {"name": "expanded", "old": True,  "new": True,  "share": 100, "rollback": True,  "retire_evidence": True},
    {"name": "retired",  "old": False, "new": True,  "share": 100, "rollback": False, "retire_evidence": True},
]

def valid(state):
    has_authoritative_path = state["old"] or (state["new"] and state["share"] > 0)
    routed_work_is_ready = state["share"] == 0 or state["new"]
    old_removal_is_evidenced = state["old"] or state["retire_evidence"]
    partial_exposure_is_reversible = state["share"] in (0, 100) or state["rollback"]
    return all((has_authoritative_path, routed_work_is_ready,
                old_removal_is_evidenced, partial_exposure_is_reversible))

results = []
for state in states:
    result = valid(state)
    results.append(result)
    print(f'{state["name"]}: {"valid" if result else "invalid"}')
print(f"all_states_valid={str(all(results)).lower()}")
```

Execution proves only that these dictionaries satisfy four encoded Boolean predicates. It does not prove real routing, data compatibility, recovery, or retirement safety. Those claims require evidence from the actual mechanisms.

**Reversibility invariant.** A transition may be called reversible only relative to a named acceptable recovery state and time bound. Source rollback is neither necessary nor sufficient. If an external side effect cannot be undone, recovery may require compensation or roll-forward rather than reversal.

**Option-value reasoning.** Suppose an irreversible design costs 100 to replace if a future condition occurs with probability $0.4$. Its simplified expected mismatch cost is $0.4\times100=40$. A reversible probe costing 12 that reveals the condition perfectly before commitment would have a gross expected advantage of 28, before delay, probe error, and exercise costs. This calculation is a decision aid under strong assumptions, not a general price for modularity.

**Retirement invariant.** Transition complexity remains part of the architecture until old authority, routes, contracts, data, permissions, support procedures, and recovery dependencies have evidence-backed disposition. Sending zero normal traffic does not establish full retirement if replay, seasonal, administrative, or recovery paths remain.

## Alternatives and Trade-Offs

**Predictive target versus directional architecture.** A detailed target coordinates known near-term dependencies but becomes brittle as uncertainty grows. Direction plus invariants preserves learning but may leave teams without enough coordination. Use precise near-term transition states and increasingly conditional longer-term decisions.

**Reversible probe versus up-front analysis.** Probes expose real behavior but incur build, exposure, cleanup, and ethical costs. Models and reviews are cheaper for eliminating impossible or hazardous options but depend on assumptions. Use analysis to bound safe learning and experiments to test decision-critical uncertainty.

**Modular flexibility versus operational simplicity.** Replaceable elements and compatibility layers preserve options but add interfaces, versions, observability, and failure modes. A stable low-change system may benefit from a simpler integrated design. Buy optionality where volatility and consequence justify its carrying cost.

**Rollback versus roll forward.** Rollback is fast when state and interfaces remain compatible. Roll forward is safer after irreversible state change or when rollback code is less exercised. Predefine the boundary and test both relevant procedures.

**Shadow versus canary versus parallel authority.** Shadowing minimizes decision consequence but may not reproduce latency, concurrency, or side effects. Canary traffic tests authoritative behavior for a bounded cohort. Dual authority can test more but creates reconciliation and integrity risk. Select the weakest exposure that answers the question.

**Strict invariants versus exploration.** Nonnegotiable constraints protect critical outcomes; too many constraints freeze design and encode preferences. Limit hard invariants to authorized consequential properties. Use objectives, monitors, and review triggers for dimensions where trade-offs and discovery remain legitimate.

**Build flexibility versus accept debt.** An extension point, abstraction, or export path has present cost. Accepting a bounded hard-to-change decision can be rational when volatility is low, horizon is short, or alternatives are cheap. Record the assumption and trigger rather than claiming universal future-proofing.

## Failure Modes and Misconceptions

1. **“Evolutionary means architecture emerges by itself.”** Guidance, constraints, feedback, and decisions distinguish evolution from accidental accumulation.
2. **“Incremental means low risk.”** A tiny authorization or data change can have a large blast radius.
3. **“The target makes the path safe.”** Intermediate states can violate invariants even when the destination is acceptable.
4. **“One fitness score captures architecture.”** Heterogeneous qualities and noncompensable constraints resist valid scalar aggregation.
5. **“A green test proves the characteristic.”** It proves only its encoded predicate under its execution conditions.
6. **“A feature flag provides rollback.”** Incompatible state and external effects can make the old branch unusable.
7. **“Shadow results equal production results.”** Shadow paths may omit authority, contention, timing, and side effects.
8. **“Dual write means safe parallel run.”** Partial failure and ordering can create irreconcilable authorities.
9. **“Backward-compatible syntax preserves behavior.”** Semantics, timing, defaults, errors, and side effects may change.
10. **“More optionality is always better.”** Options incur carrying, testing, security, and cognitive costs.
11. **“Delay is the last responsible moment.”** Delay becomes irresponsible when it removes feasible choices or increases exposure.
12. **“A modular codebase is independently deployable.”** Data, operations, contracts, and teams may still impose lockstep.
13. **“Telemetry creates feedback.”** Feedback exists only when evidence reaches a decision with thresholds and authority.
14. **“Canaries contain every failure.”** Shared control planes, ledgers, queues, or identities can propagate beyond a cohort.
15. **“Temporary duplication is free.”** It consumes capacity, creates inconsistency, and expands attack and support surfaces.
16. **“Migration ends when traffic moves.”** Old data, clients, permissions, replay, recovery, and procedures may remain.
17. **“Experimentation overrides assurance.”** High-consequence domains retain safety, legal, ethical, privacy, and regulatory obligations.
18. **“Completing the roadmap proves success.”** Evidence may justify changing or stopping the original path.

## Worked Examples

### Example 1

**Situation.** A team defines “move to microservices” as its evolutionary direction.

**Reasoning.** The phrase names a structural style, not an outcome. Interviews reveal the actual concern: four product groups cannot release because a shared order build and database require synchronized regression. The direction becomes “permit independently authorized order-rule changes without cross-group release coordination while preserving one order-state authority.” Measures include coordination events, mixed-version compatibility, invariant violations, and recovery. A modular monolith, services, or another structure may satisfy it.

**Conclusion.** Evolution should be guided by stakeholder outcomes and constraints, not a fashionable destination label.

### Example 2

**Situation.** The final payment design has one ledger authority, but the migration plan allows both old and new services to write for two weeks.

**Reasoning.** Both endpoints can accept the same idempotency key but use different uniqueness scopes. During a delayed retry they can commit two charges. The final-state diagram hides this unsafe intermediate state. The team changes the path: the old service retains authority, the new service shadows calculations, then a fenced routing decision transfers authority per account. Reconciliation and recovery evidence precede each expansion.

**Conclusion.** Every transition state—not only the target—must satisfy critical integrity invariants.

### Example 3

**Situation.** Architects propose a generic rules engine because policy might vary in the future.

**Reasoning.** Only one stable rule exists, no stakeholder owns future variation, and the engine adds a language, runtime, privilege boundary, and deployment dependency. The option cannot be valued or exercised responsibly. The team instead isolates the rule behind a narrow responsibility and records a trigger: introduce externalized rules when two independently released policy sets exist.

**Conclusion.** Information hiding can preserve a change seam without paying prematurely for speculative generality.

### Example 4

**Situation.** A recommendation service is suspected of causing checkout overload.

**Reasoning.** The hypothesis says asynchronous isolation will bound checkout resource consumption when recommendation latency rises. The transition introduces a queue for 1% of eligible, non-sensitive traffic, with a control cohort. Measures cover checkout tail latency, queue age, recommendation yield, resource saturation, and lost updates. Expansion stops if checkout improves but queue age breaches the product limit. A forced-dependency failure exercise tests isolation.

**Conclusion.** An increment should test a mechanism and side effects across multiple dimensions, not merely deploy a component.

### Example 5

**Situation.** A release flag can route traffic to software version 1 or 2, so the team calls the change reversible.

**Reasoning.** Version 2 writes a new enum value that version 1 rejects, and it emits an event old consumers dead-letter. After any version-2 write, routing back causes failures. The team adds tolerant readers, deploys consumer support first, and separates schema expansion from value activation. Until mixed-version recovery passes, the flag controls traffic but does not provide rollback.

**Conclusion.** Practical reversibility includes persistent state, messages, and consumers—not just executable selection.

### Example 6

**Situation.** A search replacement produces the same top result as the old engine for 99.5% of shadow queries.

**Reasoning.** Aggregate agreement hides that accessibility queries and one language cohort diverge systematically. Shadow execution also excludes write-after-read freshness because it does not own indexing. The team segments comparison by critical cohort, defines acceptable equivalence rather than exact rank equality, and runs a bounded canary that includes freshness and failure recovery.

**Conclusion.** Shadow evidence is useful only within its population, semantics, and missing production mechanisms.

### Example 7

**Situation.** An organization maintains adapters for four suppliers “to preserve optionality,” but only one adapter has been exercised in three years.

**Reasoning.** The unused adapters fail current authentication and cannot export complete history. They create patching and testing costs without a feasible switch. The team tests the two plausible exit routes, repairs one, retires the rest, and records exercise cadence and supplier-trigger conditions. It budgets the retained option's carrying cost.

**Conclusion.** An option exists only when it remains exercisable; untested variation is often inventory, not resilience.

### Example 8

**Situation.** A regional canary limits a new scheduler to 5% of requests, apparently bounding blast radius.

**Reasoning.** All regions share one global work queue and control-plane database. The canary's malformed lease records block old schedulers globally. Request percentage does not isolate the failure mechanism. The team uses a separate queue namespace and control-plane cell, verifies fencing, and limits authority as well as traffic.

**Conclusion.** Blast-radius boundaries must contain the relevant state and control dependencies, not only request routing.

### Example 9

**Situation.** A migration has moved 100% of normal traffic, and the team wants to delete the old service.

**Reasoning.** Evidence inventory finds annual tax replay, offline clients that synchronize monthly, a disaster runbook calling the old endpoint, and an emergency identity grant. The team observes a representative period, migrates replay, contacts or expires clients under policy, tests recovery, revokes identity, removes routes, archives required records, and then decommissions infrastructure.

**Conclusion.** Traffic migration is one input to retirement; complete disposition spans rare paths, data, identity, and operations.

### Example 10

**Situation.** A medical-device monitoring architecture needs a protocol change to address a newly discovered hazard.

**Reasoning.** Randomly exposing patients to an unassured protocol is unacceptable. Qualified safety and clinical authorities define the invariant envelope and evidence plan. Engineers use formal interface analysis, simulators, recorded traces under governance, hardware-in-the-loop tests, independent verification, staged manufacturing controls, and authorized deployment cohorts. Rollback and mixed-fleet behavior are analyzed before field change.

**Conclusion.** Evolutionary principles apply in high-consequence systems, but learning mechanisms must remain inside ethical, safety, legal, and regulatory authority.

## Cross-Program Connections

- [CONPAR](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies ordering, atomicity, progress, and interference reasoning for coexistence and authority transfer.
- [SEPAT](../../11-software-engineering-patterns/ROADMAP.md) supplies seams such as adapter and facade, while this chapter evaluates their temporal cost and removal.
- [SDRE](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) develops pipelines, progressive delivery, observability, incident learning, and recovery mechanisms that implement feedback.
- [DBE](../../18-database-engineering/ROADMAP.md) supplies transaction, schema, replication, backfill, and consistency mechanics needed for reversible data evolution.
- [DARCH](../../20-data-architecture-engineering/ROADMAP.md) extends temporal compatibility, lineage, ownership, and lifecycle reasoning across data estates.
- [SYSENG](../../26-systems-engineering/ROADMAP.md) connects baselines, configuration control, verification, lifecycle, interfaces, hazards, and physical-system constraints.
- [API](../../28-api-and-service-engineering/ROADMAP.md) develops consumer-aware compatibility and rollout across service contracts.
- [PLAT](../../29-platform-engineering/ROADMAP.md) provides reusable environments, policy, routing, telemetry, and self-service controls that reduce the cost of safe increments.

## References

1. Neal Ford, Rebecca Parsons, Patrick Kua, and Pramod Sadalage. *Building Evolutionary Architectures*. 2nd ed. O'Reilly Media, 2022.
2. M. M. Lehman. “Programs, Life Cycles, and Laws of Software Evolution.” *Proceedings of the IEEE* 68, no. 9 (1980): 1060–1076. https://doi.org/10.1109/PROC.1980.11805
3. David L. Parnas. “Software Aging.” In *Proceedings of the 16th International Conference on Software Engineering*, 279–287, 1994. https://doi.org/10.1109/ICSE.1994.296790
4. David L. Parnas. “Designing Software for Ease of Extension and Contraction.” *IEEE Transactions on Software Engineering* SE-5, no. 2 (1979): 128–138. https://doi.org/10.1109/TSE.1979.234169
5. Barry W. Boehm. “A Spiral Model of Software Development and Enhancement.” *Computer* 21, no. 5 (1988): 61–72. https://doi.org/10.1109/2.59
6. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*. 4th ed. Addison-Wesley, 2021.
7. Murat Erder, Pierre Pureur, and Eoin Woods. *Continuous Architecture in Practice: Software Architecture in the Age of Agility and DevOps*. Addison-Wesley, 2021.
8. Jez Humble and David Farley. *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*. Addison-Wesley, 2010.
9. Carliss Y. Baldwin and Kim B. Clark. *Design Rules, Volume 1: The Power of Modularity*. MIT Press, 2000.
10. ISO, IEC, and IEEE. *ISO/IEC/IEEE 42020:2019, Software, Systems and Enterprise—Architecture Processes*. 1st ed., July 2019. https://www.iso.org/standard/68982.html

## Exercises

### Exercise 1

Define guided change, increment, invariant envelope, reversibility, optionality, evolution hypothesis, and retirement evidence. Distinguish architectural evolution from runtime adaptation.

### Exercise 2

An architecture path has four states. $x_0,x_1,x_3\in K$, but $x_2\notin K$ because two writers can commit the same financial decision. The final state $x_3$ is otherwise desirable. Evaluate the path and propose a safer transition structure.

### Exercise 3

A team says a database migration is reversible because it can redeploy the old binary. The new binary drops a column, emits a new event enum, and has processed 4% of production orders. Diagnose the claim and specify the evidence required for rollback, compensation, or roll-forward.

### Exercise 4

Design an evolutionary plan for replacing a shared notification platform used by twenty teams. Include outcome direction, dimensions, invariants, cohorts, feedback, compatibility, authority, blast radius, stopping rules, temporary complexity, and retirement.

### Exercise 5

A city wants to evolve a water-control system that combines old programmable controllers, radio links, cloud analytics, manual operation, and public-safety responsibilities. Apply evolutionary architecture principles while respecting safety, cybersecurity, procurement, environmental, accessibility, labor, and regulatory authority.

## Answers to the Exercises

### Answer 1

Guided change has a stated outcome direction, constraints, evidence, and accountable decisions. An increment is a bounded transition that can be evaluated independently of full destination completion. An invariant envelope is the set of critical properties every admitted state must preserve under stated conditions. Reversibility is the practical ability to reach an acceptable recovery state across code, data, contracts, identities, operations, and external effects. Optionality is a set of feasible future choices, including the capability to exercise them. An evolution hypothesis predicts how a mechanism will affect an outcome and what would challenge it. Retirement evidence supports removal of a superseded path and its associated state, authority, and procedures.

Runtime adaptation selects behavior within already designed mechanisms in response to conditions, such as autoscaling. Architectural evolution changes significant structure, constraints, responsibilities, or rationale over time. An adaptive mechanism can evolve, but adaptation is not sufficient evidence of an evolutionary architecture.

### Answer 2

The path is inadmissible under the model because path safety requires every admitted state to remain in its applicable envelope. A desirable $x_3$ does not compensate for the integrity violation in $x_2$. The plan should preserve one authority during coexistence. For example, retain the old writer while the new path shadows and reconciles; introduce routing with a fenced authority token per account or partition; migrate a bounded cohort; and transfer authority only after compatibility, idempotency, recovery, and reconciliation pass.

If no intermediate state can preserve the invariant, the target or migration mechanism must change. Evaluation requires evidence that fencing works under retries, partitions, delayed messages, and operator error—not merely a diagram showing one writer at the endpoints.

### Answer 3

Redeploying the binary is not rollback. Dropped data may be unrecoverable, old code may reject the enum already stored or queued, and the 4% of orders may have produced external side effects. First stop expansion within authorized operational procedures and preserve evidence. Determine whether the column was physically deleted, backed up, reconstructable, or semantically transformed. Inventory stored and in-flight new enum values, consumer compatibility, issued messages, ledger effects, and client state.

Rollback requires a tested old reader for every reachable state, restoration within acceptable loss and time bounds, compatible consumers, and reconciliation of side effects. If that cannot be established, define compensation where domain-valid or roll forward with tolerant readers, schema restoration, message translation, and bounded replay. Validate on protected copies or authorized environments before production action. A complete answer distinguishes binary rollback, data recovery, business compensation, and roll-forward.

### Answer 4

The direction might be “allow each team to send governed notifications independently while preserving consent, audit, delivery policy, and bounded failure.” Dimensions include delivery correctness, privacy, security, accessibility, latency, cost, supplier dependence, team autonomy, and recovery. Invariants include one consent authority, no send without policy evaluation, auditable terminal outcome, and protection of sensitive content.

Baseline producers, message formats, templates, identities, channels, callbacks, data retention, traffic, rare jobs, and recovery. Introduce a compatibility facade and shadow validation, then migrate internal low-risk producers, one channel, and bounded tenants. The old platform remains authority until routing transfers per producer. Compare policy decisions and outcomes, inject dependency failure, and segment by accessible format and critical cohort. Stop on consent discrepancy, duplicate sends, unexplained loss, or shared-resource saturation.

Track adapters, duplicated templates, replay, and routing flags as temporary architecture with owners and expiry. Expand only after representative load and recovery evidence. Retirement covers old clients, scheduled campaigns, callbacks, credentials, data, suppliers, runbooks, dashboards, and disaster paths. Alternative implementations are acceptable, but evaluation requires all dimensions, explicit authority, reversible cohorts, meaningful thresholds, and complete decommission evidence.

### Answer 5

Begin with accountable water operations, public-safety, control engineering, cybersecurity, environmental, accessibility, procurement, supplier, labor, legal, and regulatory stakeholders. They define decision rights and nondelegable constraints. Baseline controller firmware, logic, sensors, actuators, radio topology, cloud services, identities, manual modes, physical interlocks, supplier support, and operating procedures. Architecture reviewers do not certify safety or authorize live experiments.

Define an invariant envelope around safe pressure and quality control, authenticated commands, local fail-safe operation, manual authority, audit, environmental obligations, and continuity. Create separate, bounded evolution hypotheses—for example, cloud analytics can improve leak detection without gaining control authority. Use offline analysis, simulators, hardware-in-the-loop tests, staged lab networks, shadow telemetry, and independently reviewed evidence before any authorized field cohort. Isolate radio and control segments, constrain identities, and ensure loss of cloud or communications leaves an accepted local state.

Plan mixed-fleet protocol compatibility, supplier and procurement lead times, operator training, accessible interfaces, maintenance staffing, rollback or roll-forward boundaries, and emergency procedures. Pilot only where qualified authorities approve consequence and recovery. Monitor environmental and operational outcomes, not just software health. Retire credentials, old radios, data copies, routes, and procedures only with verified coverage. The model answer must preserve human override and physical safety, avoid unauthorized live fault injection, and explicitly defer certification and regulatory approval to the responsible institutions.
