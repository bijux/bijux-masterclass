---
module_id: SEPAT-099
program: Software Engineering: Patterns
level: 2
module_number: 99
title: Recognizing Golden Hammer, Big Ball of Mud, and Distributed Monolith
status: complete
last_verified: 2026-08-29
---

# Recognizing Golden Hammer, Big Ball of Mud, and Distributed Monolith

## One-Page Review

### Governing question

How can engineers diagnose solution monoculture, structural erosion and distributed coupling from evidence—without using anti-pattern names as insults—and choose treatments that improve outcomes without triggering another unjustified rewrite?

### Essential definitions

- An **anti-pattern** is a recurring response to context that appears attractive but repeatedly produces harmful consequences, together with a refactored alternative—not merely “bad code.”
- **Golden Hammer** is habitual application of a familiar technology/pattern to problems whose forces call for materially different solutions.
- **solution monoculture** is portfolio dependence on one tool/model, reducing fitness and resilience; standardization is not automatically monoculture.
- **Big Ball of Mud (BBoM)** is a system whose structure/boundaries have eroded so dependencies, knowledge and change effects are difficult to predict or contain.
- **distributed monolith** consists of separately deployed components that remain tightly change-, data-, release-, runtime- or failure-coupled, gaining network complexity without useful independence.
- **change coupling** means components frequently change together for one feature/defect.
- **release coupling** means compatibility/deployment requires coordinated versions or order for ordinary changes.
- **failure coupling** means one component's slowness/unavailability predictably incapacitates others beyond an intentional boundary.
- **data/authority coupling** means multiple components share/write private schemas or require synchronous cross-boundary transactions to decide.
- **architecture fitness evidence** measures desired properties continuously: dependency constraints, deployability, version skew, blast radius, flow and operational outcomes.

### Central model, mechanism, or theorem

Diagnosis is multi-dimensional evidence, not a scalar score. For component/capability graph (G=(V,E)), classify edges by static dependency, co-change, runtime calls, shared data/authority, coordinated release and failure propagation. A proposed boundary is valuable only if it reduces relevant coupling while preserving necessary cohesion/consistency.

- Golden Hammer signal: tool choice remains constant while problem forces vary, alternatives are not evaluated, and mismatches recur.
- BBoM signal: dependency cycles/ownership diffusion/change amplification rise and declared boundaries do not predict change.
- distributed-monolith signal: physical deployment count rises but independent change/release/operate/fail capability does not.

No threshold proves a label. Combine repository, delivery, runtime, incident, data and human workflow evidence; test a treatment hypothesis on one bounded slice.

### Critical invariants

- Start with observed harm/forces; never diagnose by aesthetics, repository count or technology choice alone.
- Distinguish intentional coupling/cohesion from accidental coupling and actual monoliths from distributed monoliths.
- Triangulate static, historical, runtime, release, incident, data and team evidence over a stated window.
- Normalize metrics for system/team size and avoid Goodhart-style target gaming.
- Treat security, reliability, delivery, cost and cognitive load as outcomes, not just code graph shape.
- Map authoritative decisions/data; shared read access and shared multi-writer ownership are different risks.
- Identify organizational/process incentives that sustain the structure; code-only remedies rarely last.
- Prefer reversible bounded treatments with baseline, hypothesis, target, guardrails and stop criteria.
- Do not prescribe microservices for BBoM or one platform for Golden Hammer by reflex.
- Reassess after intervention and remove scaffolding; improvement is empirical, not declared by diagram.

### Common failures

Failures include calling any monolith mud; counting cycles without context; blaming developers; using service count as modularity; replacing an in-process call with RPC while keeping chatty transactions; splitting tables into services; shared database writes; synchronous fan-out; lockstep releases hidden by one pipeline; copying one framework everywhere; technology standards with no exception process; rewrite as universal cure; “domain-driven” renaming without authority change; teams gaming deployment/coverage metrics; and treating temporary incident coordination as permanent release coupling.

### Compact example

Six “services” have separate containers/repositories. Checkout synchronously calls five, three write one database schema, every release uses one version manifest, and failure of pricing stops order history reads. Physical distribution exists; decision, data, release and failure independence do not. First treatment is not six more services: map order authority, move history reads off the live chain, prohibit cross-owner writes, establish backward-compatible contracts and collapse components that have no independent lifecycle.

### Connections

[Pattern Hype](009-pattern-hype-and-cargo-cult-design.md), [Selecting from Forces](010-selecting-a-pattern-from-forces-rather-than-names.md), [Pattern Composition](006-pattern-composition.md) and [Diagnosing Behavioral Pattern Misuse](050-diagnosing-behavioral-pattern-misuse.md) establish judgment. [Strangler Fig](097-strangler-fig.md) and [Branch by Abstraction](098-branch-by-abstraction-pattern.md) offer bounded treatments. The successor [Pattern Review](../ROADMAP.md) converts diagnosis into an evidence-based decision process.

## Governing Question

How should a review distinguish healthy standardization, pragmatic disorder and purposeful distributed systems from anti-patterns that measurably harm change, correctness and operations?

Anti-pattern labels are memorable and therefore dangerous. “Mud” can mean “code I dislike”; “distributed monolith” can mean “service that calls another”; “golden hammer” can reject useful standards. A credible diagnosis identifies context, repeated response, attractive forces, harmful consequences, evidence and a better path. It stays falsifiable: what observation would disprove it?

Systems optimize under deadlines, staff changes, acquisitions, incidents and uncertain domains. Big Ball of Mud may be locally rational when architecture work receives no budget and delivery is rewarded narrowly. Distributed monoliths arise when teams split processes/repositories without moving decision/data ownership or compatibility. Golden Hammers arise from expertise, procurement, platform incentives and operational economies. Treatment must address those forces or the structure returns.

## Why This Matters

Misdiagnosis wastes years. A well-modularized monolith can deploy safely and preserve strong transactions; splitting it may create a distributed monolith. A shared relational database can be the right tool; using it for every graph/search/queue workload without comparison can be a Golden Hammer. Some exploratory systems appropriately begin with fluid boundaries; prematurely imposing layers can slow learning.

Conversely, untreated coupling compounds. Simple changes touch many teams/files/services, releases coordinate, tests require the world, incidents cascade and no one owns authoritative decisions. Engineers avoid risky areas, adding workarounds and further erosion. Tool monoculture forces awkward models and concentrates vendor/skill/outage risk.

Evidence-driven anti-pattern recognition turns frustration into actionable hypotheses. It also prevents architecture theater: boxes and repository splits do not substitute for independent ownership, deployability and failure containment.

## Prerequisites and Retrieval

Learners should retrieve:

- pattern form: context, forces, solution, consequences and evidence;
- cohesion, coupling, dependency direction, cycles and information hiding;
- bounded contexts, aggregate/data authority and team ownership;
- versioned contracts, backward compatibility and independent deployment;
- distributed latency/failure, deadlines, bulkheads and asynchronous workflows;
- delivery metrics, change history, incident analysis and value-stream mapping;
- modular monoliths, service boundaries and database ownership;
- sociotechnical/organizational architecture and Goodhart's law.

Before continuing, explain why “five repositories and Kubernetes” provides no evidence that five capabilities can change or fail independently.

## Learning Objectives

After this module, learners can:

1. define anti-pattern without weaponizing it;
2. distinguish Golden Hammer from appropriate standardization;
3. diagnose BBoM from dependency/change/ownership evidence;
4. distinguish modular monolith, microservices and distributed monolith;
5. collect/triangulate static, historical, runtime, data and team evidence;
6. map coupling across change, release, runtime, failure and authority dimensions;
7. identify incentives/constraints sustaining harmful responses;
8. design bounded reversible treatment experiments;
9. reject universal microservice/rewrite/platform cures;
10. communicate diagnosis with uncertainty, ownership and success/stop criteria.

## Core Exposition

### Use the full anti-pattern form

Write:

1. **Context:** system, mission, scale, lifecycle, teams and constraints.
2. **Forces:** speed, familiarity, transactions, procurement, operations, regulation, staffing.
3. **Recurring response:** what teams repeatedly do.
4. **Why attractive:** local benefits and incentives.
5. **Harmful consequences:** specific outcomes and affected stakeholders.
6. **Evidence:** observations over a bounded period with limitations.
7. **Refactored solution:** smaller experiments, not aspirational target art.
8. **Counterevidence/stop rule:** what would invalidate diagnosis/treatment.

This form keeps empathy and causality. “Developers were lazy” explains little. “Ownership changes quarterly; delivery incentives reward local throughput; no compatibility tests; shared schema makes safe local release impossible” suggests interventions.

### Diagnose Golden Hammer by fitness mismatch

Standardization can lower training, integration, security and on-call cost. It becomes Golden Hammer when decision procedure collapses: “we use Kafka/Kubernetes/microservices/event sourcing/relational databases/one cloud for everything,” alternatives cannot be tried, and problem forces contradict the chosen tool.

Look for:

- solution chosen before requirements/forces;
- product vocabulary reshaped around framework primitives;
- simple workloads paying disproportionate operational cost;
- missing benchmark/alternative/exit criteria;
- exception requests socially or procedurally impossible;
- recurring workarounds/sidecars/queues inside queues;
- staff/vendor concentration and correlated failures;
- success measured by adoption rather than business/reliability outcomes.

A platform “paved road” is healthy when it fits most cases, publishes service levels/costs, supports evidence-based exceptions and evolves from feedback. Diversity has cost too. Treatment is a fitness matrix and thin experiments, not indiscriminate polyglot freedom.

### Diagnose Big Ball of Mud as boundary erosion

Foote and Yoder describe haphazard growth where structure becomes difficult to discern. Symptoms span code and work:

- high dependency cycles and unstable directions;
- one change touches unrelated areas/teams (“shotgun surgery”);
- shared mutable globals/schema and utility dumping grounds;
- business rules duplicated/inconsistent;
- tests require huge fixtures/environment and cannot isolate capability;
- ownership unclear; most experts must approve ordinary changes;
- deploy/rollback blast radius unpredictable;
- build/test time and defect/change lead time rise;
- architecture docs differ from actual dependencies.

Cycles alone do not prove mud: mutually recursive algorithms or cohesive packages may be correct. A large monolith is not automatically mud; explicit modules, owner-local data and enforced dependencies can make it healthy. Compare declared capability boundaries with co-change/import/runtime/data graphs. If changes stay cohesive inside modules and releases remain reliable, size is not diagnosis.

Treatment begins with observability and seams: identify one high-change/high-harm capability, establish characterization tests and dependency rules, move authority/logic behind a stable module, eliminate cross-writes, and measure change blast radius. Branch by Abstraction or Strangler may help. A rewrite without domain learning/process change often reproduces mud.

### Diagnose distributed monolith by missing independence

Services justify network/process cost through some combination of independent ownership, change/release, scaling, technology, availability or security boundary. A distributed monolith pays cost but retains coupling:

- synchronous chatty call chains for one decision;
- table/entity-shaped services with no decision authority;
- shared private database schemas or cross-service writes;
- cross-service ACID assumptions/two-phase coupling for ordinary operations;
- one release train/version matrix/end-to-end environment required for every change;
- incompatible contracts deployed lockstep;
- one shared library model forcing simultaneous upgrade;
- failure/latency cascades without deadlines/degradation/bulkheads;
- services cannot test/run/restore/on-call independently;
- one feature requires coordinated changes across many repositories/teams.

Coordination is not categorically wrong. A rare business launch or breaking regulatory change can coordinate. Diagnose frequency/necessity: can ordinary compatible changes deploy independently under version skew? Shared infrastructure is not the same as shared domain authority. One pipeline can deploy many independently; separate pipelines can still lockstep via human process.

Treat by capability/ownership, not more splitting. Combine nanoservices that share lifecycle; create one owner per decision/data; use coarse contracts; remove cross-writes; support backward compatibility; move noncritical reads to local projections; bound synchronous dependencies; and build consumer/provider tests. Sometimes the best cure is a modular monolith.

### Build an evidence portfolio

**Static:** import/module/package/service dependency graph, cycles, fan-in/out, architecture-rule violations, shared schemas/libraries.

**Change history:** files/services/teams co-changed per feature, change-set size, hotspots, reverts and ownership concentration. Beware generated files, bulk formatting and repository boundaries.

**Delivery:** lead time, failed changes, rollback scope, coordinated release frequency, version-skew tests and environment bottlenecks.

**Runtime:** traces/call depth/fan-out, latency budgets, retry amplification, availability dependency, queue/connection saturation and blast radius.

**Data:** tables/topics written/read by owners, transactions, consistency/joins, replication and schema-change coordination.

**Incidents:** propagation graph, recovery coordination, unclear ownership, recurrence and counterfactual containment.

**Human workflow:** cognitive load, onboarding, dependency wait time, approvals, team topology and exception mechanisms.

Use a bounded representative window and disclose missing telemetry. Correlation is not causation: co-change may reflect one cohesive capability. Interview affected engineers/domain/operators and inspect work items to interpret metrics.

### Quantify without creating a magic score

Useful measures include change-set spread, probability two components co-change, dependency-cycle count/size, synchronous critical-path length, release coordination ratio, shared-write count, version-skew pass rate, incident propagation, time-to-owner and percentage of changes staying within a capability.

Do not sum them into “architecture health 73.” Weights hide value judgments and invite gaming. Use a dashboard of distributions/graphs tied to hypotheses. Compare trend/baseline and peer capabilities normalized by size/traffic/risk. A metric becomes a target and can cease being useful: teams may split commits to reduce spread without reducing coordination.

### Treat by leverage and reversibility

Select one costly recurring change/failure. Hypothesis example: “Moving refund decision and data behind Payments module will reduce median services changed per refund feature from five to two without increasing p99 or failure rate.” Establish baseline, intervention, target, guardrails, owner, period and stop/reversal.

Potential treatments:

- delete unused capability/dependency;
- enforce module/API/data ownership;
- consolidate inseparable services;
- introduce facade/adapter/anti-corruption boundary;
- move shared decisions to a cohesive owner;
- add compatible contracts/version skew tests;
- replace synchronous query chains with owner APIs/local materialized views where staleness permits;
- limit approved platform scope and create exception experiments;
- invest in tests/build/deployment/observability;
- align team ownership with durable capabilities.

Avoid broad “microservices transformation” or “rewrite.” Strangler/Branch by Abstraction creates incremental evidence. Stop when marginal improvement no longer justifies disruption.

### Deterministic coupling-evidence summary

This executable example summarizes observed edges across dimensions. It intentionally reports dimensions rather than producing a diagnostic score.

<!-- bijux-verify: {"id":"sepat-099-coupling-evidence","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"components=catalog,checkout,inventory,pricing\nstatic=2 cochange=3 runtime=3 shared-write=1 lockstep=2\ncheckout-links=catalog:runtime,inventory:cochange|lockstep|runtime|shared-write,pricing:cochange|lockstep|runtime\ndiagnosis=requires-context-not-a-score\n","stderr":""}} -->
```python
evidence = {
    ("checkout", "catalog"): {"runtime"},
    ("checkout", "inventory"): {"cochange", "runtime", "shared-write", "lockstep"},
    ("checkout", "pricing"): {"cochange", "runtime", "lockstep"},
    ("catalog", "pricing"): {"static", "cochange"},
    ("inventory", "pricing"): {"static"},
}
dimensions = ["static", "cochange", "runtime", "shared-write", "lockstep"]
components = sorted({name for edge in evidence for name in edge})
counts = {dimension: 0 for dimension in dimensions}
for signals in evidence.values():
    for signal in signals:
        counts[signal] += 1

checkout = []
for (left, right), signals in evidence.items():
    if left == "checkout":
        checkout.append(right + ":" + "|".join(sorted(signals)))

print("components=" + ",".join(components))
print(" ".join(dimension + "=" + str(counts[dimension]) for dimension in dimensions))
print("checkout-links=" + ",".join(checkout))
print("diagnosis=requires-context-not-a-score")
```

The run proves deterministic counting for five invented edges only. It does not measure a repository/system, infer causality, diagnose an anti-pattern, select thresholds, evaluate business outcomes or validate a treatment.

## Definitions and Notation

Let components/capabilities be vertices (V). Define evidence relations over window (T): static dependency (E_s), co-change (E_c), runtime call (E_r), shared-authority/write (E_d), lockstep release (E_l), failure propagation (E_f), and team dependency (E_o). These relations can differ in direction/weight.

For changes $q\in Q_T$, let spread (S(q)=|components(q)|); coordination ratio at boundary (b) can be (CR_b=|\{q:S_b(q)>1\}|/|Q_b|), but component definitions and work-item grouping affect it. Runtime critical-chain reliability under independent failures approximates product of dependency availabilities only under assumptions rarely exact; use observed traces/incidents and conditional behavior.

**Cohesion** is related responsibilities changing/operating together for one reason. **Coupling** is dependence across boundaries. **Independence** is dimensional, not absolute: change, deploy, scale, data, failure and team independence can differ. **Counterevidence** is observation supporting a healthy explanation, such as reliable version skew and cohesive co-change.

## Mechanisms, Invariants, or Proof Structure

1. **Frame concern neutrally.** State harm, affected capability/stakeholder and evidence window—not label/person blame.
2. **Map context/forces.** Domain lifecycle, transactions, scale, regulation, staffing, platform and incentive constraints.
3. **Collect dimensions.** Static, co-change, runtime, release, data, incident and workflow evidence with limitations.
4. **Map authority/cohesion.** Identify where decisions/data belong and which co-change is intentional.
5. **Test hypotheses.** Golden Hammer fitness mismatch; BBoM boundary erosion; distributed monolith missing independence.
6. **Seek counterevidence.** Healthy standardization, modular monolith, compatible services, temporary coordination.
7. **Prioritize harm.** Frequency × consequence × tractability, including security/reliability/cognitive load.
8. **Design bounded treatment.** Baseline, target, guardrails, owner, duration, rollback/stop and expected causal mechanism.
9. **Deliver incrementally.** Seams, ownership rules, consolidation/extraction, contracts and telemetry in reviewable changes.
10. **Re-measure/learn.** Compare outcomes, investigate confounders, stop/reverse/expand, then remove scaffolding.

The evidence can support inference: if ordinary changes repeatedly span declared boundaries, releases require lockstep, shared writes exist and failures cascade, the claim of useful service independence is contradicted. It does not prove “distributed monolith” as a mathematical category or identify one unique cause. Causal confidence improves through bounded interventions and outcome change.

## Alternatives and Trade-Offs

**Healthy standardization** reduces cognitive/operational/supply-chain cost and enables automation; preserve it with published fitness/exception path.

**Modular monolith** gives local calls/transactions and one deployable while enforcing capability modules. Often a strong treatment for nanoservice coupling.

**Microservices** justify network cost through independent ownership/change/scale/failure needs; they are not a maturity tier.

**Service-based architecture/coarse services** balances deployment boundaries and transactions; boundary count need not maximize.

**Legacy encapsulation** places a stable facade around messy internals; rational when rewrite value is low and change surface can be bounded.

**Incremental modularization/strangling** targets hotspots with feedback; slower aesthetically but safer than broad rewrite.

**Platform paved roads with exceptions** balance economies and fitness; uncontrolled polyglot diversity creates another cost.

**Intentional coupling** is correct when one transaction/release constitutes one cohesive business invariant. Do not distribute it merely for independence metrics.

## Failure Modes and Misconceptions

- **“Anti-pattern means bad people.”** It is a recurring systemic response with attractive forces.
- **“One tool everywhere is Golden Hammer.”** Standardization may be fit; inspect mismatches and exception process.
- **“Large monolith is mud.”** Size/deployment shape does not prove boundary erosion.
- **“Cycles prove mud.”** Interpret purpose, size, change and ownership.
- **“Many services mean microservices.”** Process count is not decision/release/failure independence.
- **“Any coordination is distributed monolith.”** Rare intentional launches differ from routine lockstep.
- **“Shared database proves it.”** Shared reads/schema can vary; cross-owner writes/transactions are stronger evidence.
- **“RPC type safety fixes coupling.”** It can make unhealthy chatty dependencies efficient/explicit.
- **“Events decouple.”** Shared schemas, temporal coupling and coordinated consumers can remain.
- **“Split more.”** Nanoservices can increase runtime/release coupling.
- **“Rewrite cleans mud.”** Domain/process/incentive problems recreate it.
- **“Adopt DDD.”** Vocabulary/diagrams without authority and enforced dependencies do not change coupling.
- **“One metric diagnoses architecture.”** Metrics require context/counterevidence and can be gamed.
- **“Tool replacement cures Golden Hammer.”** The decision monoculture can simply choose a new hammer.
- **“Target diagram is improvement.”** Only measured change/failure/delivery/business outcomes establish progress.

## Worked Examples

### Example 1

**Situation.** Organization mandates PostgreSQL for transactions, queues, full-text and graph traversal.

**Reasoning.** Standardizing relational OLTP may be fit; graph workaround complexity and queue correctness incidents suggest mismatches. Compare operational benefit and thin alternatives for those workloads; retain PostgreSQL where it wins.

**Conclusion.** Diagnose Golden Hammer per force/outcome, not because one tool appears often.

### Example 2

**Situation.** A 2-million-line monolith has enforced modules, owner-local schemas, 90% changes within one module and reliable releases.

**Reasoning.** Size is large, but boundaries predict change and ownership. It may be a healthy modular monolith. Investigate hotspots rather than label entire codebase mud.

**Conclusion.** BBoM is structural/operational erosion, not line count or one deployable.

### Example 3

**Situation.** Three packages form a dependency cycle but implement one parser algorithm and change together.

**Reasoning.** It may be one cohesive module artificially split; consolidate or document internals. Cycle metric alone does not show cross-capability harm.

**Conclusion.** Interpret graph edges through cohesion and change reasons.

### Example 4

**Situation.** Twelve services have separate repos but every feature modifies six and uses one coordinated release manifest.

**Reasoning.** Repository/process separation has not delivered change/release independence. Map data/decision ownership and version-skew barriers; consolidate inseparable slices or establish compatible contracts.

**Conclusion.** Ordinary co-change/lockstep is strong distributed-monolith evidence.

### Example 5

**Situation.** Checkout makes eight synchronous fine-grained calls, each with retries and no end-to-end deadline.

**Reasoning.** Latency/failure amplify; partial retries multiply load. Move decision to cohesive owner, batch coarse calls, use deadlines and local projections for stale-tolerant reads. Async messaging alone is not automatically correct.

**Conclusion.** Runtime topology should follow ownership and failure semantics, not table-shaped services.

### Example 6

**Situation.** Services share one database for reads, but each table has one writer/owner and contracts permit version skew.

**Reasoning.** Shared storage is a coupling/security risk, yet not sufficient diagnosis. Measure schema coordination, unauthorized joins, failure/scaling and release independence. It may be transitional or intentional.

**Conclusion.** Multi-writer authority and routine lockstep are stronger evidence than shared physical location alone.

### Example 7

**Situation.** Team proposes microservices to fix a tangled monolith.

**Reasoning.** Network boundaries around unclear domains externalize the tangles. First establish characterization, modular boundaries and data ownership; extract only where independent lifecycle is evidenced.

**Conclusion.** Modularize understanding before distributing confusion.

### Example 8

**Situation.** Platform adoption is 95%, but teams tunnel unsupported workloads through sidecars and manual operations.

**Reasoning.** Adoption target hides fitness. Measure reliability/cost/lead time and exception wait. Publish capability limits, create evidence-based exception lane and improve paved road from recurring signals.

**Conclusion.** Golden Hammer treatment repairs decision governance, not merely technology.

### Example 9

**Situation.** After modularization, median services changed falls five→two, but incidents and lead time worsen.

**Reasoning.** Structural target improved while outcomes degraded, perhaps due to new contracts/ownership bottleneck. Stop expansion, inspect confounders and adjust/reverse. Do not cherry-pick the favored metric.

**Conclusion.** Treatment succeeds only within multi-dimensional guardrails.

### Example 10

**Situation.** A national benefits platform's anti-pattern review recommends rapid service decomposition based on cycle and deployment counts.

**Reasoning.** Eligibility transactions, statutory rules, appeals, privacy and seasonal loads require domain/operational interpretation. Obtain change/release/data/incident evidence, simulate failure and pilot one reversible boundary. Named human policy, caseworker, safety/reliability, privacy/security and accessibility reviewers must assess consequences; metrics cannot choose acceptable benefit-denial risk.

**Conclusion.** High-stakes diagnosis needs human-governed outcomes and incremental evidence, not architecture scoring.

## Cross-Program Connections

- **Software Design/Domain Modeling:** cohesion, information hiding, bounded contexts and authority distinguish useful boundaries.
- **Architecture:** deployable topology must follow ownership, change, scale and failure forces rather than fashion.
- **Distributed Systems:** latency, partial failure, retries, transactions and ordering expose costs of false independence.
- **Database Engineering:** shared writes, schemas and cross-boundary transactions reveal data authority coupling.
- **Delivery/Reliability:** co-change, version skew, incidents, blast radius and lead time supply outcome evidence.
- **Security Engineering:** unclear ownership and copied/shared data weaken authorization, least privilege and incident containment.
- **Platform Engineering:** paved roads need fitness, exception paths and adoption/outcome separation.
- **Testing and Quality:** architecture tests, contract/version-skew suites and treatment experiments make boundaries falsifiable.

## References

- Brian Foote and Joseph Yoder, [Big Ball of Mud](http://www.laputan.org/mud/), 1997/1999, retrieved 2026-08-29. Foundational pattern language for haphazard growth and architectural erosion.
- William J. Brown et al., *AntiPatterns: Refactoring Software, Architectures, and Projects in Crisis*, Wiley, 1998. Defines anti-pattern/refactored-solution form and Golden Hammer.
- Sam Newman, *Monolith to Microservices*, O'Reilly Media, 2019. Service-boundary, decomposition and distributed-monolith trade-offs.
- Amazon Web Services, [Decomposing Monoliths into Microservices](https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-decomposing-monoliths/), AWS Prescriptive Guidance, retrieved 2026-08-29. Current decomposition guidance including distributed-monolith risks; cloud recommendations remain contextual.
- Neal Ford, Rebecca Parsons, and Patrick Kua, *Building Evolutionary Architectures*, second edition, O'Reilly Media, 2022. Architecture fitness functions and incremental change.
- Matthew Skelton and Manuel Pais, *Team Topologies*, IT Revolution, 2019. Sociotechnical ownership, cognitive load and interaction modes.
- Nicole Forsgren, Jez Humble, and Gene Kim, *Accelerate*, IT Revolution, 2018. Empirical delivery-performance measures and organizational capabilities.
- David Lorge Parnas, [On the Criteria To Be Used in Decomposing Systems into Modules](https://www.cs.umd.edu/class/spring2003/cmsc838p/Design/criteria.pdf), *Communications of the ACM* 1972. Foundational information-hiding decomposition criterion.

## Exercises

### Exercise 1

Define Golden Hammer, Big Ball of Mud and distributed monolith in anti-pattern form. Give counterevidence that would weaken each diagnosis.

### Exercise 2

Given co-change, runtime, data and release graphs for four components, explain why no weighted score can replace interpretation. Propose two falsifiable hypotheses.

### Exercise 3

Diagnose a system with 30 services, one shared ORM model/database, synchronous chains, one release train and low incident rate but slow changes.

### Exercise 4

Compare modular-monolith consolidation, service-boundary repair, Strangler Fig, Branch by Abstraction and platform exception governance as treatments for the three anti-patterns.

### Exercise 5

Conduct a preliminary diagnosis for an unfamiliar regulated payments platform whose teams demand a rewrite. Specify evidence, counterevidence, pilot, guardrails and human review.

## Answers to the Exercises

### Answer 1

Golden Hammer: varying problem contexts repeatedly receive one familiar solution because of expertise/standardization incentives, causing observable fitness harm; counterevidence is favorable workload comparison, lower total operating risk and a functioning exception process. BBoM: boundaries/ownership erode so dependencies/change/failures become unpredictable and cross concerns; counterevidence is enforced modules, cohesive co-change, clear authority and contained releases/incidents despite size. Distributed monolith: separately deployed pieces retain routine change/data/release/runtime/failure coupling without useful independence; counterevidence is backward-compatible version skew, owner-local data, independent routine deploy/restore/scale and bounded degradation. Each diagnosis also needs attractive forces and a refactored response, not just symptoms.

### Answer 2

Weights encode hidden values: a shared-write edge can outweigh ten static calls for correctness, while one mandated synchronized launch differs from every ordinary release. Component size, risk and work-item grouping distort counts; a score invites gaming. Hypothesis one: “shared inventory writes cause checkout coordination”; prohibit cross-writes behind owner API in one slice, expecting fewer coordinated changes without latency/failure regression. Hypothesis two: “synchronous pricing queries cause checkout cascades”; build a bounded local price projection/fallback, expecting lower incident propagation and p99 with stated staleness guardrail. Baseline and counterevidence (cohesive transaction, already compatible deploys) determine whether to proceed.

### Answer 3

Separate services plus shared ORM/database and synchronous chains indicate missing data/decision/runtime independence; one release train and slow changes add change/release coupling. Low incident rate is important counterevidence: do not claim failure harm that data denies. Map table writers, feature co-change, version compatibility and call deadlines; determine whether a modular monolith would preserve reliability while lowering network/release cost. Start by assigning table/decision owners and stopping cross-writes, add contract/version-skew tests, shorten one critical chain, and measure lead time plus incident guardrail. Consolidate nanoservices that share lifecycle rather than split further. Diagnose “distributed monolith affecting change flow,” not universally unreliable architecture.

### Answer 4

Modular-monolith consolidation treats distributed nanoservice coupling when components lack independent lifecycle, and can make BBoM boundaries enforceable locally. Service-boundary repair retains services but gives capability authority, coarse compatible contracts, local data and bounded failure. Strangler Fig incrementally moves externally bounded capabilities from mud/legacy; it requires known authority and decommission. Branch by Abstraction replaces a pervasive internal implementation, useful for Golden Hammer tool replacement or seam creation without distributed routing. Platform exception governance treats the decision monoculture behind Golden Hammer by publishing fitness limits and safe experiments. These combine: establish modules/authority, branch a tool, strangle one capability, consolidate false services, and change incentives. None is a universal cure.

### Answer 5

Frame claimed harm: change lead time, payment defects, outage propagation, cost or regulatory evidence—not “old.” Over 6–12 representative months collect feature co-change by capability/team, service/import/runtime chains, shared database writers/transactions, coordinated releases/version-skew tests, p99/deadline/retry behavior, incidents/near misses, ownership wait and audit/security findings. Map payment authority, ledger settlement, reconciliation, refunds, chargebacks and external networks. Seek counterevidence: strong transaction/audit integrity, seasonal reliability, cohesive co-change and constraints a rewrite might break.

Pilot one reversible high-friction but bounded read/decision seam: establish characterization/regulatory fixtures, owner-local interface/data rules and either modularize internally or build a shadow projection; do not duplicate money effects. Hypothesis and targets might reduce components/teams per change and lead time while preserving exact ledger reconciliation, p99, fraud/security and incident rate. Stop/rollback on any unmatched monetary entry, authorization regression, missed deadline or unsupported recovery. Named human payments-domain, accounting, risk, compliance, privacy/security, operations and accessibility reviewers approve semantics and treatment gates. Reassess causal evidence before expanding; a rewrite is authorized only if bounded alternatives cannot meet objectives and migration preserves authority/audit/recovery.
