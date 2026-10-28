---
module_id: SARCH-080
program: Software Engineering: Software Architecture
level: 2
module_number: 80
title: Planning Architecture Evolution Across Multiple Releases
status: complete
last_verified: 2026-09-06
---

# Planning Architecture Evolution Across Multiple Releases

## One-Page Review

### Governing question

How can architects plan a sequence of releases that delivers present value, preserves architectural invariants, creates the capabilities needed by later changes, learns from uncertainty, and leaves every intermediate production state coherent?

### Essential definitions

- an **evolution outcome** is a stakeholder result the architecture must enable or protect over a declared horizon;
- an **architecture increment** is a bounded change to responsibilities, interfaces, data authority, quality mechanisms, or deployment structure that leaves an operable state;
- a **release state** is the complete architecture, behavior, data, operations, and compatibility condition after a release;
- a **transition architecture** is intentionally temporary structure that enables movement between release states and has removal conditions;
- an **enabler** creates capability or reduces uncertainty needed for later outcomes;
- **architectural runway** is implemented and validated capability that makes near-term delivery feasible; it is not speculative infrastructure inventory;
- a **dependency** is a condition that must be satisfied before or with an increment;
- a **compatibility window** is the supported interval in which old and new versions or representations coexist;
- a **decision checkpoint** is a planned opportunity to continue, revise, hold, reverse, or stop based on evidence;
- **rolling-wave planning** specifies near releases precisely and later releases by outcomes, constraints, and options, refining them as evidence arrives;
- **option value** is the value of preserving an informed future choice;
- **architecture debt** is an intentional or accidental design condition whose consequences include future risk or rework, not merely any unfinished architecture work.

### Central model, mechanism, or theorem

Let increments $I$ form a directed acyclic prerequisite graph $G=(I,E)$ after genuine dependency cycles are resolved. A release assignment $r:I\rightarrow\{1,\ldots,H\}$ is feasible only if every edge $(i,j)\in E$ satisfies $r(i)<r(j)$ when $j$ requires completed evidence from $i$, release capacity is respected, and every resulting release state satisfies hard invariants. A topological schedule is necessary for prerequisites but insufficient for success: value, uncertainty, compatibility, operational readiness, external deadlines, and evidence gates remain.

Plan the next release from verified current state; preserve later alternatives; and update the graph, estimates, risks, and target state after each checkpoint. The target architecture is a hypothesis constrained by durable outcomes, not a frozen endpoint.

### Critical invariants

- every release produces an operable, supportable, and recoverable architecture state;
- hard safety, security, data, legal, accessibility, and continuity constraints hold throughout transition;
- prerequisites represent real evidence or mechanism needs rather than political preference;
- one authority exists for each mutable fact in mixed states;
- contracts and schemas support every deployed version combination in the compatibility window;
- temporary components have owners, budgets, telemetry, expiry, and removal work;
- capacity includes architecture, migration, verification, operation, and retirement effort;
- uncertainty and external dependencies are visible and revisited;
- roadmap changes preserve decision history without treating sunk cost as a reason to continue;
- completed increments retire superseded paths and demonstrably move an outcome or reduce decisive uncertainty.

### Common failures

Common failures include drawing a target diagram with no safe path; treating architecture as a preliminary stage; planning features without enablers or retirement; inventing dependencies to protect ownership; scheduling by component instead of vertical outcomes; putting every cross-cutting change in the first release; calling unimplemented intentions runway; using one-point estimates; filling future releases with false precision; ignoring mixed-version states; accumulating permanent flags and bridges; funding construction but not migration and operation; measuring boxes delivered instead of outcomes; continuing because of sunk cost; and allowing emergency exceptions without owners or expiry.

### Compact example

A five-release order modernization must first observe current behavior and establish delivery capability. Release 1 adds trace evidence and a verified deployment path. Release 2 creates an internal order seam. Release 3 can then evolve the contract and copy data in parallel. Release 4 transfers one bounded authority under compatibility and recovery gates. Release 5 retires the old route, store, credentials, and transition code. Later assignments remain conditional on observed coupling, data quality, and workload; failure of a gate changes the plan rather than being hidden as schedule variance.

### Connections

[SARCH-070](070-running-an-evidence-based-architecture-review.md) supplies review decisions, [SARCH-072](072-evolutionary-architecture-principles.md) supplies feedback and fitness, and [SARCH-073](073-versioned-contracts-and-compatibility.md) through [SARCH-079](079-decommissioning-architectural-components.md) supply the mechanisms being sequenced. [SARCH-081](../ROADMAP.md) next examines organizational communication structure.

## Governing Question

Architecture evolves through production states, not directly from current diagram to target diagram. A useful roadmap explains which capability changes first, which mechanisms and evidence it requires, how old and new coexist, what can be learned, which decisions remain open, and how obsolete structure disappears. It combines product value and architecture work rather than placing them in separate plans.

The planning problem is dynamic. Requirements, threats, workloads, suppliers, regulation, staff capability, and system understanding change. Detailed plans for distant releases create an illusion of control; refusing to anticipate any dependency creates avoidable rework. Rolling-wave planning balances these risks: commit precisely where evidence supports action and preserve outcome-oriented options farther out.

## Why This Matters

Feature-only roadmaps consume architectural capacity invisibly. A feature may require identity, data ownership, observability, deployment, or performance capability that does not exist. When this is discovered during delivery, teams add fragile shortcuts, delay value, or create debt without recording it. Conversely, architecture-only roadmaps can fund generic platforms and redesigns with no stakeholder outcome or adoption path.

Multi-release change introduces transitional risk. Schemas coexist, contracts span versions, two systems operate, data moves, teams learn new mechanisms, and rollback changes meaning. Each bridge adds states that need testing and support. If removal is not planned, transition architecture becomes the permanent architecture.

The official ISO record for ISO/IEC/IEEE 42020:2019, checked 2026-09-06, describes architecture processes across architecture lifecycles and multiple projects; it was confirmed in 2025 and moved to “to be revised” status in January 2026 while remaining published [1]. SEI research on architecture-aware release planning explicitly analyzes architectural dependencies alongside cost and early value rather than treating them as separate concerns [3].

## Prerequisites and Retrieval

Retrieve stakeholder, outcome, constraint, quality-attribute scenario, architecture decision, baseline, target state, transition architecture, capability, enabler, dependency, directed graph, cycle, topological order, critical path, capacity, estimate range, uncertainty, risk, option, technical debt, compatibility window, expand-migrate-contract, feature flag, canary, data authority, migration, rollback, roll forward, fitness function, service objective, recovery, roadmap, release, program increment, decision checkpoint, and retirement.

SARCH-061 through SARCH-070 provide trade-off, risk, metric, cost, and review tools. SARCH-071 through SARCH-079 provide drift, evolutionary design, compatibility, decomposition, routing, data migration, modularization, strategy selection, and retirement. This chapter integrates those decisions across releases without replacing product, delivery, finance, safety, or legal planning disciplines.

## Learning Objectives

After completing this module, you should be able to:

1. express architecture evolution as outcomes and coherent release states;
2. distinguish architecture increments, product increments, enablers, and transition architecture;
3. build and challenge a typed dependency graph;
4. resolve cycles and derive a feasible release order without treating it as sufficient;
5. allocate capacity for discovery, implementation, migration, validation, operation, and retirement;
6. plan compatibility, authority, recovery, and mixed-version evidence in each state;
7. use rolling horizons, checkpoints, and option value under uncertainty;
8. integrate debt decisions and external dependencies transparently;
9. evaluate progress through outcomes, fitness evidence, and removed risk rather than activity;
10. revise or stop a roadmap while preserving durable direction and decision history.

## Core Exposition

**Start from verified current state.** Inventory deployed versions, dependencies, data authority, quality behavior, delivery capability, incidents, costs, teams, contracts, and active transition mechanisms. Separate intended architecture from observed structure. A roadmap beginning from a stale target or repository picture sequences the wrong work.

Record evidence dates and uncertainty. Identify unsafe or unsupported conditions requiring immediate containment. Current-state discovery is bounded: gather enough to make the next decision, then expand where one finding indicates a broader class.

**Define durable evolution outcomes.** State stakeholder results over a useful horizon: pricing releases independently within one day; regional loss preserves emergency intake; customer data stays within jurisdiction; unit cost remains below a bound at forecast volume; or an unsupported platform retires by a date. Include affected population, environment, response, and measure.

Avoid topology goals such as “fifty services” unless service count is causally necessary, which is rare. Several architectures may meet one outcome. Durable outcomes guide adaptation when a planned technology or organization changes.

**Declare hard invariants and guardrails.** Identify conditions that every intermediate state must preserve: one ledger authority, no duplicate payment, safety interlock availability, authenticated access, accessible critical workflow, records retention, data locality, and recoverability. Name the accountable authority and evidence for each.

Do not average hard constraints into roadmap scoring. An early value release cannot compensate for an unauthorized data transfer. If a transition cannot preserve a gate, redesign the transition or obtain a legitimate decision; do not mark the risk accepted by an unrelated role.

**Define release states, not lists of tasks.** Describe the complete operable condition after each release: responsibilities, interfaces, deployed versions, authority, data, traffic, flags, operations, support, recovery, security, and known temporary structure. State what users can do and what failure modes exist.

A release named “build new service” is incomplete. It may have no consumer, data, authority, or operational value. Prefer a vertical state such as “new eligibility path shadows 10% of qualified traffic with effects isolated and discrepancies adjudicated.”

**Identify architecture increments and enablers.** An increment changes a bounded architecture decision or establishes evidence. Examples include creating an internal seam, introducing a compatible contract, fencing data authority, isolating a resource pool, automating restore, or removing a shared writer. A product increment delivers stakeholder behavior; one change can be both.

An enabler has a named consumer and horizon. Observability for a forthcoming cutover is credible; an enterprise event platform “for future agility” without adopters or decisions is inventory. Define acceptance and expiry for experiments and scaffolding.

**Build typed dependencies.** For each increment, record prerequisites by type: behavior knowledge, data, contract, technical mechanism, operational capacity, security or assurance, external supplier, organization, and decision authority. Explain why ordering is necessary and what evidence discharges it.

Distinguish hard from preferred order. “Team A wants to finish first” is scheduling preference. “The candidate cannot consume the old schema until the additive field exists” is a compatibility dependency. False dependencies serialize work; missing dependencies create rework and unsafe release states.

**Resolve cycles rather than scheduling them.** Dependency cycles mean the current increments cannot be strictly ordered. Break a cycle by changing scope, adding compatibility, introducing a seam, moving one decision, combining an atomic set, using a temporary adapter, or proving a presumed dependency unnecessary.

Do not label the entire cycle “Release 1” without checking capacity and operability. Some cyclic changes require one atomic coordinated release; others reveal poor boundaries. Record the reason and mixed-state behavior.

**Find feasible order with graph reasoning.** After cycles are resolved, topological ordering exposes possible sequences and parallel work. Critical-path analysis identifies a lower bound under estimated durations and fixed dependencies. Capacity-constrained scheduling assigns work to releases.

These mechanisms do not choose value or validate estimates. A topologically valid plan can deliver no outcome, overload one team, violate an invariant, or depend on unavailable evidence. Use graphs to reveal consequences, then apply stakeholder and practitioner judgment.

**Plan compatibility as work.** Each interface and schema change needs supported producer-consumer combinations, deployment order, defaults, unknown-field behavior, and removal conditions. Expand, migrate, and contract often span releases. Budget tests and telemetry for the window.

Count compatibility states. Multiple overlapping versions multiply combinations and support burden. Bound fleet skew, define upgrade lag, and avoid starting another incompatible transition before the current one contracts unless evidence justifies the interaction.

**Plan data authority explicitly.** Describe source of truth, backfill snapshot, change capture, reconciliation, cutover position, fencing, read routing, write routing, rollback horizon, and retirement in each release. “Migrate data later” conceals the hardest dependency.

One mutable fact retains one authority. Parallel comparison can use replicas; dual writes need a real protocol and repair ownership. After incompatible destination writes, roll forward may replace rollback. Put that decision checkpoint before crossing it.

**Plan operational capability before exposure.** A new topology needs build, deploy, configuration, identity, telemetry, limits, capacity, support, incident response, backup, restore, and vulnerability handling. Decide which capabilities must exist before shadow, canary, or authority.

Avoid demanding a perfect platform before the first outcome. Implement the smallest durable mechanism that supports the next releases and has owners. Later generalization should follow multiple real consumers, not imagined reuse.

**Allocate full lifecycle capacity.** Estimate discovery, design, implementation, test, migration, data repair, dual operation, documentation, training, support, incident learning, and retirement. Include cross-team coordination and external lead time. Feature capacity that ignores these activities creates hidden overload.

Use ranges and confidence, not one number. Separate elapsed dependency time from active effort. Reserve capacity for operational events and newly discovered work. Do not treat a risk buffer as free scope available whenever a feature estimate grows.

**Balance early value and rework.** Delivering value early generates feedback and return; implementing a prerequisite early can avoid repeated rework. SEI release-planning research formalizes this trade-off with architecture dependencies, cost, and value [3]. Models help compare assumptions but do not determine ethical or safety priorities.

Sometimes deliberate short-term debt enables a critical outcome. Record the compromised quality, consequence, owner, principal, accumulating cost or risk, detection signal, repayment trigger, latest acceptable release, and contingency. “We will clean it up” is not a debt strategy.

**Preserve option value under uncertainty.** Delay irreversible choices when learning is likely and delay cost is acceptable. Create seams, portable data representations, or bounded prototypes that preserve alternatives. Conversely, make a decision early when long lead time, safety evidence, or widespread dependency makes delay expensive.

An option needs an exercise condition and expiry. Indefinite abstraction or multi-platform support can cost more than the choice it preserves. Measure the price paid for reversibility.

**Use rolling horizons.** Specify the next release in concrete work, gates, owners, and operations. Specify the following few releases as coherent states and likely dependencies. Express distant horizons as outcomes, constraints, decision points, and options rather than task-level promises.

Refine after every release using actual evidence. Rolling-wave planning is not permission to lack direction. Outcomes and invariants persist; details change as the system and environment reveal themselves.

**Manage external dependencies.** Track standards, suppliers, contracts, procurement, platform roadmaps, certificates, data agreements, regulation, partner versions, hardware, hiring, and organizational decisions. Record owner, lead time, confidence, fallback, and latest decision date.

Do not hide external uncertainty behind a fixed milestone. A supplier promise is evidence with confidence, not architecture fact. Build a fallback when consequence and uncertainty justify its cost.

**Coordinate teams through contracts and outcomes.** Assign each increment an accountable owner while preserving end-to-end outcome ownership. Use interface and data contracts, integration milestones, decision records, and shared evidence. A central architecture group cannot own every implementation decision; a team cannot change a shared invariant alone.

Reduce cross-team coupling by fixing architecture, not only adding meetings. Temporary collaboration can be appropriate while establishing a boundary. Define when the interaction mode ends.

**Maintain decision records and traceability.** Record context, options, decision, assumptions, consequences, evidence, owner, date, review trigger, and supersession. Link outcomes to increments, tests, telemetry, risks, releases, and retirement. Preserve why a plan changed.

Avoid turning records into approval theater. Lightweight records written near the decision support learning. Current state, not an obsolete decision, governs action; supersede rather than silently edit history.

**Design evidence gates and checkpoints.** Before each state transition define required functional, quality, security, data, operational, accessibility, cost, and recovery evidence. Define sample or workload, threshold, observation interval, authority, and possible decisions: proceed, hold, narrow, correct, reverse, roll forward, or stop.

A gate that always produces “proceed” is ceremony. Preserve failures and dissent. If evidence is unavailable, do not relabel the increment complete; change the plan or keep the affected authority unchanged.

**Track architecture fitness and outcomes.** Select a balanced set of leading and lagging measures tied to mechanisms: dependency violations, compatibility, restore success, latency distribution, saturation, change touch, release coordination, incident blast radius, unit cost, and stakeholder result. Assign owners and response.

Metrics are partial. Passing a structural rule does not prove domain quality; deployment frequency does not prove value; zero observed incidents can reflect low exposure. Combine automation with semantic review, operational exercises, and user evidence.

**Operate transition architecture deliberately.** Adapters, routers, dual readers, replication, translators, flags, comparison stores, and temporary teams are production components. Budget capacity, security, observability, recovery, and support. Give each removal conditions and a latest review point.

Limit simultaneous transitions. Each adds interaction states and diagnostic ambiguity. Finish contraction and retirement where possible before opening another cross-cutting compatibility window.

**Replan without losing discipline.** At checkpoints compare actual versus assumed value, cost, duration, risk, coupling, and evidence. Update dependencies and target hypotheses. Stop an increment whose mechanism no longer affects the outcome. Accelerate when a threat or external deadline changes.

Sunk cost is historical evidence, not future benefit. Preserve reusable learning and artifacts, but evaluate remaining work against current alternatives. Explain changes to affected stakeholders and maintain operational coherence.

**Finish through retirement and benefit realization.** A release that activates the new path but leaves old authority, data, routes, licenses, flags, and operations has not completed the architectural increment. Schedule decommissioning and post-removal observation as first-class work.

Compare realized stakeholder outcomes and operating cost with baseline. Feed findings into the next planning wave. Architecture evolution is successful when the system can keep changing safely—not when a target diagram is finally matched.

## Definitions and Notation

Let:

- $I$ be architecture and product increments in the planning horizon;
- $E\subseteq I\times I$ be hard prerequisite edges;
- $G=(I,E)$ be the prerequisite graph;
- $r(i)$ be the assigned release for increment $i$;
- $d(i)$ be estimated effort in a declared capacity unit;
- $C_h$ be available capacity in release $h$;
- $Q_h$ be hard invariants required in release state $h$;
- $V_h(i)$ be estimated stakeholder value of increment $i$ in release $h$;
- $P(i)$ be the evidence gate for $i$;
- $X_h$ be temporary transition components present after release $h$;
- $expiry(x)$ be the removal or review condition for $x\in X_h$;
- $A_h(f)$ be the authoritative owner of mutable fact $f$ in release $h$.

A simple feasible assignment requires $r(i)<r(j)$ for every prerequisite $(i,j)$ that must be completed before $j$, and $\sum_{i:r(i)=h}d(i)\le C_h$. It must also satisfy every $Q_h$, gate, ownership, compatibility, and operational constraint. Dependencies that can complete within one atomic release need an explicit different relation rather than being forced into this strict model.

## Mechanisms, Invariants, or Proof Structure

**Topological feasibility theorem.** A finite directed graph has a topological order if and only if it is acyclic. If it has a directed cycle, each member must precede itself through transitivity, which is impossible. If it is acyclic, at least one vertex has indegree zero; removing it and applying induction constructs an order. This proves ordering feasibility only for the declared graph.

**Executable capacity schedule.** This deterministic example schedules ready increments into releases of capacity three. Dependencies must be completed in an earlier release, so it does not start newly unblocked work in the same release.

<!-- bijux-verify: {"id":"schedule-evolution-increments","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"release1=['observe', 'platform'] effort=3\nrelease2=['seam'] effort=2\nrelease3=['contract', 'data-copy'] effort=3\nrelease4=['cutover'] effort=1\nrelease5=['retire'] effort=2\n","stderr":""}} -->
```python
work = {
    "observe": (1, set()),
    "platform": (2, set()),
    "seam": (2, {"observe"}),
    "contract": (1, {"seam"}),
    "data-copy": (2, {"seam"}),
    "cutover": (1, {"contract", "data-copy", "platform"}),
    "retire": (2, {"cutover"}),
}
done = set()
release = 0
while len(done) < len(work):
    release += 1
    ready = [name for name in sorted(work) if name not in done and work[name][1] <= done]
    chosen, used = [], 0
    for name in ready:
        effort = work[name][0]
        if used + effort <= 3:
            chosen.append(name)
            used += effort
    if not chosen:
        raise ValueError("cycle, oversized increment, or unsatisfied dependency")
    done.update(chosen)
    print(f"release{release}={chosen} effort={used}")
```

Execution verifies one finite greedy schedule. It does not prove estimates, value, gate passage, resource interchangeability, or optimality.

**Capacity lower bound.** Ignoring dependencies and indivisibility, total effort yields lower bound $\lceil\sum_i d(i)/C\rceil$ for constant release capacity $C$. Dependencies, specialized skills, uncertainty, and gates can only preserve or increase the required number under this model. The bound is not a promise.

**Authority invariant.** For every release state $h$ and mutable fact $f$, exactly one $A_h(f)$ may commit final state unless one logical authority is enforced by a documented protocol. The roadmap must describe authority transfer, not merely code deployment.

**Transition-debt invariant.** Every $x\in X_h$ has an owner, operating evidence, and $expiry(x)$. If its purpose becomes durable, redesign and fund it as permanent architecture; if not, remove it. An absent removal increment makes the roadmap structurally incomplete.

**Value-order counterexample.** Scheduling the highest immediate-value item first can force rework when it depends on a missing architectural mechanism. Scheduling every mechanism first delays all feedback. Therefore neither feature-only ranking nor architecture-first ordering dominates generally; dependency, rework, learning, and time-dependent value must be considered together.

## Alternatives and Trade-Offs

**Detailed long-range plan versus rolling wave.** Detail aids coordination but decays under uncertainty. Rolling waves preserve adaptability but require durable outcomes and disciplined checkpoints to avoid drift.

**Architecture-first versus vertical slices.** Up-front mechanisms reduce repeated rework but risk unused infrastructure. Vertical slices yield outcome feedback but may repeat work without selected enablers. Combine the minimum enabling path with a real consumer.

**Strict sequencing versus parallel work.** Sequencing simplifies dependencies and authority. Parallel work shortens elapsed time but increases integration, version, resource, and coordination risk. Parallelize only genuinely independent increments.

**Temporary adapter versus coordinated cutover.** An adapter supports compatibility and incremental rollout but adds latency and states. Coordinated cutover shortens transition but concentrates risk and excludes slow consumers.

**Fixed capacity allocation versus adaptive allocation.** Fixed allocation protects architectural investment. Adaptive allocation responds to evidence but can starve retirement and debt. Use outcome-based guardrails and explicit exceptions.

**Central roadmap versus federated roadmaps.** Central planning exposes shared dependencies but can detach from implementation. Federated plans use local knowledge but can conflict. Share outcomes, contracts, constraints, and integration evidence while keeping bounded ownership.

## Failure Modes and Misconceptions

1. **“The target diagram is the roadmap.”** it omits safe intermediate states and evidence.
2. **“Architecture happens before features.”** both evolve through outcome-bearing increments.
3. **“Every enabler is runway.”** unvalidated capability without a near consumer is speculation.
4. **“A dependency is anything another team requests.”** hard order needs a technical, evidence, or authority reason.
5. **“A topological order is a release plan.”** value, capacity, invariants, gates, and people remain.
6. **“Put a cycle in one release.”** atomicity, capacity, and operability still require proof.
7. **“Future releases need exact tasks.”** distant precision hides uncertainty.
8. **“Rolling wave means no long-term direction.”** durable outcomes and constraints guide refinement.
9. **“Compatibility is implementation detail.”** mixed states dominate multi-release risk.
10. **“Deploying transfers data authority.”** cutover and fencing are separate mechanisms.
11. **“Rollback always remains possible.”** new state and external effects create boundaries.
12. **“Architecture capacity is overhead.”** it includes work required to deliver and sustain outcomes.
13. **“A buffer absorbs arbitrary scope.”** operational uncertainty and risk need protected capacity.
14. **“Debt is any incomplete improvement.”** record a deliberate condition and consequence.
15. **“Metrics make replanning objective.”** measures are partial and require interpretation.
16. **“Temporary components are free.”** they need full production ownership and removal.
17. **“Sunk cost justifies finishing.”** remaining value and risk govern the next decision.
18. **“Activation completes an increment.”** retirement and realized outcome close it.

## Worked Examples

### Example 1

**Situation.** Product schedules personalized pricing before the platform can observe rule versions or restore pricing state.

**Reasoning.** The feature has value but lacks diagnosability and recovery prerequisites. Release 1 adds versioned decision evidence and rehearsed restore with a minimal real pricing consumer; Release 2 enables a bounded pricing cohort. The platform work is accepted by capability evidence, not component installation.

**Conclusion.** Enablers belong before dependent exposure and beside a real outcome.

### Example 2

**Situation.** Teams claim A depends on B, B on C, and C on A, so all must ship together.

**Reasoning.** Typed analysis finds A needs C's stable fact, not its runtime API; C's callback exists only for notification. A versioned fact and outbox remove the callback, making the graph acyclic. The remaining atomic data change receives one coordinated state and rollback plan.

**Conclusion.** Resolve dependency meaning before accepting a giant coordinated release.

### Example 3

**Situation.** The executable schedule places contract and data-copy work together in Release 3.

**Reasoning.** Both depend on the completed seam and fit capacity. This is only structural feasibility. If data classification approval is absent or the same specialist must do both, the real plan changes. The scheduler cannot infer those constraints unless modeled.

**Conclusion.** Graph schedules expose assumptions; they do not replace planning judgment.

### Example 4

**Situation.** A six-month roadmap lists exact tasks for Release 1 and equally exact tasks three years away.

**Reasoning.** The distant list assumes workload, supplier, regulation, and architecture discoveries that have not occurred. The plan keeps near work concrete, expresses the next states and dependencies, and rewrites distant detail as outcomes, constraints, options, and decision dates.

**Conclusion.** Precision should decline as uncertainty increases while direction remains durable.

### Example 5

**Situation.** A schema transition supports three producer and four consumer versions indefinitely.

**Reasoning.** Twelve nominal pairs plus data states and intermediaries expand testing and support. The roadmap bounds skew, specifies supported pairs, migrates laggards, measures use, and schedules contract removal. A new breaking change waits unless overlapping windows are explicitly justified.

**Conclusion.** Compatibility windows consume capacity and must contract.

### Example 6

**Situation.** A team deploys a new order writer in Release 2 and schedules data migration for Release 4.

**Reasoning.** The state has ambiguous authority and no complete data. The plan moves snapshot, change capture, reconciliation, and fencing before write cutover, or keeps the candidate shadow-only. Each release now identifies source position and authoritative writer.

**Conclusion.** Deployment order must follow data and authority state, not code completion.

### Example 7

**Situation.** An emergency deadline requires a security workaround that adds a shared gateway dependency.

**Reasoning.** Qualified owners accept a bounded exception because it immediately closes a critical exposure. The debt record names affected qualities, gateway failure risk, telemetry, owner, repayment design, and latest release. Capacity is reserved and the exception cannot renew silently.

**Conclusion.** Deliberate debt can be rational only with consequence, detection, and repayment governance.

### Example 8

**Situation.** A supplier promises a required export API “next quarter.”

**Reasoning.** The roadmap records the dependency, owner, confidence, contractual evidence, latest decision date, and fallback bulk export. A checkpoint chooses the supplier path or activates the fallback before it can block data migration.

**Conclusion.** External promises are uncertain dependencies requiring decisions and contingencies.

### Example 9

**Situation.** A migration misses its cost target after three releases, but leadership argues that stopping wastes prior investment.

**Reasoning.** The checkpoint compares remaining cost, current outcome, new evidence, alternatives, retirement burden, and reusable learning. Past spend is excluded from prospective benefit. The program narrows to the valuable capability and retires unused transition components.

**Conclusion.** Sunk cost informs learning but cannot justify future work.

### Example 10

**Situation.** A target service handles all traffic, while the old database, bridge, flags, credentials, and on-call remain unscheduled.

**Reasoning.** Activation delivered only part of the increment. A release state explicitly migrates residual consumers, fences authority, archives or deletes data, removes bridge and flags, updates recovery, closes operations, and measures cost and incident reduction.

**Conclusion.** Retirement and realized benefit are roadmap work, not post-project cleanup.

## Cross-Program Connections

- [SEME](../../10-software-engineering-methods-and-evolution/ROADMAP.md) owns lifecycle, evolution process, estimation, maintenance, and legacy change methods.
- [SDRE](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) supplies delivery flow, progressive release, telemetry, recovery, incident learning, and operational capacity.
- [TOCC](../../15-theory-of-computation-and-complexity/ROADMAP.md) supplies graph and scheduling complexity foundations where relevant.
- [DARCH](../../20-data-architecture-engineering/ROADMAP.md) supplies data strategy, lineage, ownership, governance, and lifecycle dependencies.
- [SEC](../../25-security-engineering/ROADMAP.md) owns evolving threat, assurance, identity, vulnerability, and risk constraints.
- [SYSENG](../../26-systems-engineering/ROADMAP.md) develops lifecycle planning, configuration, verification, transition, stakeholder, and assurance coordination.
- [API](../../28-api-and-service-engineering/ROADMAP.md) owns contract rollout, version coexistence, deprecation, and consumer migration mechanisms.
- [PLAT](../../29-platform-engineering/ROADMAP.md) supplies product-managed delivery and runtime enablers with adoption and retirement accountability.

## References

1. ISO/IEC/IEEE. “ISO/IEC/IEEE 42020:2019 Software, systems and enterprise — Architecture processes.” Official record checked 2026-09-06. https://www.iso.org/standard/68982.html
2. ISO/IEC/IEEE. *ISO/IEC/IEEE 42010:2022 Software, systems and enterprise — Architecture description*. 2nd ed., 2022.
3. Raghvinder Sangwan, Ashkan Negahban, Robert Nord, and Ipek Ozkaya. “Optimization of Software Release Planning Considering Architectural Dependencies, Cost, and Value.” *IEEE Transactions on Software Engineering* 48(4), 2022. https://doi.org/10.1109/TSE.2020.3020013
4. Neil Ernst, Mary Popeck, Felix Bachmann, and Patrick Donohoe. “Creating Software Modernization Roadmaps: The Architecture Options Workshop.” WICSA, 2016. https://www.sei.cmu.edu/library/creating-software-modernization-roadmaps-the-architecture-options-workshop/
5. Robert Nord, Ipek Ozkaya, and Philippe Kruchten. “Agile in Distress: Architecture to the Rescue.” XP, 2014.
6. Ipek Ozkaya. *Managing Technical Debt*. Addison-Wesley, 2019.
7. Neal Ford, Rebecca Parsons, Patrick Kua, and Pramod Sadalage. *Building Evolutionary Architectures*. 2nd ed. O'Reilly Media, 2022.
8. Jez Humble and David Farley. *Continuous Delivery*. Addison-Wesley, 2010.
9. Barry W. Boehm. “A Spiral Model of Software Development and Enhancement.” *Computer* 21(5), 1988. https://doi.org/10.1109/2.59
10. David L. Parnas. “Designing Software for Ease of Extension and Contraction.” *IEEE Transactions on Software Engineering* SE-5(2), 1979. https://doi.org/10.1109/TSE.1979.234169
11. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*. 4th ed. Addison-Wesley, 2021.
12. Martin Fowler. “Foreword to Building Evolutionary Architectures.” 5 October 2017. Checked 2026-09-06. https://martinfowler.com/articles/evo-arch-forward.html

## Exercises

### Exercise 1

Define evolution outcome, architecture increment, release state, transition architecture, enabler, architectural runway, dependency, compatibility window, decision checkpoint, rolling-wave planning, option value, and architecture debt.

### Exercise 2

Five increments have efforts $[2,3,4,2,1]$ and constant release capacity 5. Derive the workload-only lower bound on releases. Then explain why a dependency chain of the 2-, 4-, and 1-unit increments can require at least three releases under the strict earlier-release dependency rule.

### Exercise 3

A roadmap deploys a new service, migrates data two releases later, keeps all versions supported indefinitely, and contains no retirement work. Diagnose the invalid release states and revise the dependency and gate model.

### Exercise 4

Design a five-release evolution plan for a retail order platform. Include outcomes, current evidence, hard invariants, typed dependencies, enablers, compatibility, data authority, operational capability, capacity, checkpoints, debt, transition components, recovery, retirement, and measures.

### Exercise 5

A regional public-transit program must evolve ticketing, real-time information, accessibility services, vehicle devices, payment, maintenance, and emergency operation across agencies and procurement cycles. Propose a rolling roadmap without claiming architecture alone determines transport policy, fare justice, safety approval, accessibility adequacy, labor agreement, or lawful data use.

## Answers to the Exercises

### Answer 1

An evolution outcome is a stakeholder result architecture enables or protects. An architecture increment is a bounded decision or mechanism change leaving an operable state. A release state is the whole architecture and operating condition after delivery. Transition architecture is temporary production structure with removal conditions. An enabler creates capability or evidence for later outcomes. Architectural runway is implemented and validated near-term capability. A dependency is a required prior or concurrent condition. A compatibility window supports old and new coexistence. A checkpoint chooses next action from evidence. Rolling-wave planning details near work and preserves outcome-oriented later options. Option value is value of an informed future choice. Architecture debt is a design condition carrying future risk or rework.

### Answer 2

Total effort is $2+3+4+2+1=12$. Ignoring dependencies and indivisibility, the capacity lower bound is $\lceil12/5\rceil=3$ releases. This bound cannot prove a feasible schedule.

If the 2-unit increment must complete before the 4-unit increment, which must complete before the 1-unit increment, strict dependency rules assign them to three distinct releases even though their total effort is only 7. Other work can fill remaining capacity where independent, but the chain alone imposes a three-release elapsed lower bound. Specialized skills, gates, and indivisibility may increase it further.

### Answer 3

Deployment before data creates a candidate with no coherent authority or complete state unless it is explicitly shadow-only. Indefinite support creates an unbounded compatibility matrix and no contract state. Missing retirement leaves old authority, consumers, data, operations, flags, and cost outside the plan.

Define the candidate's first release as nonauthoritative with isolated effects and operational evidence. Add compatible contracts before mixed operation. Schedule snapshot, CDC, reconciliation, and recovery before write cutover. Give each release one source of authority and supported version pairs. Gate cutover on data, correctness, security, performance, operations, and recovery; fence old writers. Bound consumer migration and schema contraction. Add a retirement increment for old routes, stores, credentials, jobs, support, recovery, and transition code, followed by benefit measurement.

### Answer 4

Outcome: reduce promotion-change lead time and contain inventory failure without duplicate orders. Baseline change sets, releases, call/data graphs, incidents, latency, capacity, restore, and team handoffs. Hard invariants include one order authority, exact payment reference, authorized price, no oversell beyond policy, authenticated access, accessible checkout, and tested recovery.

Release 1 adds decision/version traces, focused characterization, deploy-and-restore capability, and resource limits using a real order slice. Release 2 creates internal Pricing and Inventory seams, assigns decision and data ownership, and denies new table bypasses. Release 3 expands compatible contracts, builds a versioned inventory projection, and starts snapshot-plus-CDC data copy with reconciliation. Release 4 shadows then canaries stable customer cohorts; Orders owns workflow, Inventory owns reservations, old writers are fenced at an evidence checkpoint. Release 5 migrates remaining consumers, contracts schemas, removes bridge, flags, credentials, old store and recovery, and measures outcomes.

Typed dependencies cover behavior, contract, data, operations, security, team, and supplier needs. Capacity includes migration, verification, dual operation, support, and retirement, with ranges and incident reserve. A bounded gateway workaround is recorded as debt with telemetry, owner, and Release-5 repayment. Every transition component has expiry. Checkpoints can hold, narrow, reverse before incompatible state, or roll forward afterward. Measures include lead time, touched units, contract failures, discrepancy, latency, saturation, incident blast radius, restore, cost, and user outcome.

### Answer 5

Establish accountable transit, accessibility, safety, payment, privacy, security, maintenance, procurement, labor, emergency, municipal, operator, and rider representation. Baseline vehicle and station devices, offline behavior, feeds, tickets, identities, data authority, contracts, suppliers, radio and network coverage, recovery, manual work, and agency dependencies. Define durable outcomes such as bounded information age, usable accessible journeys, resilient fare validation, and local emergency operation, while leaving policy decisions to responsible processes.

Near release: instrument source/version and accessibility outcomes, characterize offline behavior, prove signed deployment and rollback on one device class, and rehearse feed recovery. Next, establish compatible information and ticket contracts plus one agency's nonauthoritative shadow. Then migrate bounded data and devices with versioned authority, reconciliation, and fallback. A later release transfers a coherent region or route under safety, accessibility, payment, capacity, privacy, operations, and recovery gates. The following release retires old radios, credentials, feeds, contracts, stores, and support after seasonal and emergency evidence.

Track procurement and supplier lead times with fallbacks and decision dates. Preserve compatibility for slow vehicle upgrades but bound skew and sunset. Allocate training, field service, dual operation, incident response, data repair, and retirement. Checkpoints incorporate riders and operators and can stop expansion. Architecture provides traceable states, authority, evidence, and contingencies; it cannot itself approve safety, fares, accessibility, labor terms, emergency policy, procurement law, or data processing.
