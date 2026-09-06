---
module_id: SARCH-098
program: Software Engineering: Software Architecture
level: 2
module_number: 98
title: Architecture Under Severe Cost Constraints
status: complete
last_verified: 2026-09-06
---

# Architecture Under Severe Cost Constraints

## One-Page Review

### Governing question

How can an architecture deliver the smallest safe, operable, and evolvable service inside a hard lifecycle budget without hiding costs in people, risk, user exclusion, deferred maintenance, or an unowned future?

### Essential definitions

- a **hard budget** is a spend or resource ceiling whose breach threatens the service; a **target** is negotiable;
- **total cost of ownership** includes acquisition, use, people, support, migration, compliance, incidents, recovery, and exit;
- **unit cost** divides governed cost by a useful outcome such as an accepted case, not an easily inflated request count;
- **marginal cost** is the additional cost of one more unit under stated load and tier;
- **cost attribution** maps consumption to a responsible product, capability, tenant, cohort, or experiment;
- a **cost driver** is a measurable cause such as retained bytes, CPU-seconds, egress, cardinality, or operator minutes;
- **degradation** preserves a smaller declared service; **failure** violates the contract;
- a **budget invariant** is a property that must hold even when spend is exhausted, such as never dropping an accepted payment;
- **option value** is the value of preserving a low-cost future choice; premature distribution can destroy it;
- **reversibility** is the ability to undo a choice before irreversible data, contract, or organizational commitments accumulate.

### Central model, mechanism, or theorem

Model the architecture decision as

$$
\min_A C_{life}(A)\quad\text{subject to}\quad I(A)=\mathrm{true},\; Q_j(A)\ge q_j,
$$

where $C_{life}$ is lifecycle cost, $I$ contains nonnegotiable safety, security, integrity, legal, and accessibility invariants, and $Q_j$ are minimum service qualities. A design below the cash ceiling but outside these constraints is infeasible, not “lean.”

For period cost

$$
C=C_f+C_p+\sum_i p_i x_i+C_o+C_r,
$$

$C_f$ is fixed commitments, $C_p$ people and process, $p_ix_i$ metered resources, $C_o$ operational work, and $C_r$ explicitly modeled risk or expected loss. Unit cost is $u=C/N_g$ for $N_g$ good, accepted outcomes. Changing the denominator can make a dashboard cheaper without changing reality.

Little’s relation $L=\lambda W$ links average in-flight work $L$, accepted arrival rate $\lambda$, and average time $W$ under stable conditions. Reducing worker capacity below arrival rate does not save sustainably: queues and delay grow until admission, demand, or service changes.

### Critical invariants

- safety, security, data integrity, lawful access, accessibility, and accepted durable work are never optional cost tiers;
- the budget model includes people, incidents, contracts, migration, recovery, and exit—not only metered infrastructure;
- every cost metric names scope, period, allocation rule, currency, price version, and useful denominator;
- admission occurs before overload; retry cannot amplify exhausted capacity;
- degradation is explicit, ordered, observable, reversible, and tested;
- durable data has owner, retention, rebuildability, deletion, backup, and restore cost;
- shared infrastructure has fair attribution and isolation, including large consumers and idle commitments;
- a “cheaper” component is accepted only with its operational, failure, lock-in, and learning costs;
- measurement cost and cardinality are bounded without making critical failures invisible;
- experiments and optional features have budgets, expiry, and removal paths;
- reserved safety and recovery capacity cannot be consumed by ordinary demand;
- no optimization claim exceeds the measured workload and price assumptions.

### Common failures

Common failures include optimizing list price instead of lifecycle cost; dividing by requests rather than useful outcomes; using free labor as zero cost; removing backups before disposable caches; setting autoscaling with no spend ceiling; retrying overload; storing every event forever; creating a service per feature; buying commitments before demand is known; hiding shared cost in “platform”; choosing a managed service without exit economics; sampling away rare failures; batching latency-sensitive work; forcing inaccessible self-service; deferring patches; ignoring egress and support; and cutting redundancy without revising the recovery contract.

### Compact example

A case service has €18,000/month total budget. Fixed contracts cost €3,000, two engineers’ allocated time €9,000, operations €1,500, and risk reserve €1,000, leaving €3,500 for metered resources. At 20,000 accepted cases, lifecycle unit cost is €0.90/case, not the €0.175/case suggested by infrastructure alone. The architecture uses one modular deployment, one transactional store, queued optional reports, bounded attachments, tested backup, and explicit admission. It preserves case acceptance, privacy, accessibility, and recovery while degrading exports and recomputation first.

### Connections

[SARCH-012](012-performance-and-latency-tactics.md), [SARCH-013](013-scalability-and-capacity-tactics.md), [SARCH-067](067-availability-and-reliability-models.md), and [SARCH-069](069-cost-models-and-unit-economics.md) provide component models. [SARCH-092](092-architecture-for-high-change-product-domains.md) preserves option value, [SARCH-093](093-architecture-for-extreme-read-or-write-scale.md) handles extreme demand, and [SARCH-097](097-architecture-for-long-lived-scientific-systems.md) exposes lifecycle custody. [SARCH-099](../ROADMAP.md) next compares viable architectures.

## Governing Question

Severe cost constraint is not permission to build a system that externalizes harm, depends on heroic operators, or cannot recover. It means the architecture must identify the smallest legitimate service, the few costs that dominate it, and the mechanisms that keep spending and load within a survivable envelope.

Costs are coupled to structure. A service boundary adds deployment, observation, network, security, data, and coordination surfaces. A convenience query can dominate egress. A low-cost database can demand expensive specialists. Architecture must reason in useful outcomes over time, not vendor line items in isolation.

## Why This Matters

Public-interest organizations, early products, small businesses, schools, laboratories, and services in low-resource environments often face ceilings rather than optimization targets. An unexpected bill can terminate the product. Yet indiscriminate cuts create breaches, lost records, exclusion, and operational overload whose costs arrive later or fall on others.

The current FinOps Framework, checked 2026-09-06, explicitly connects technology cost to business value, planning, unit economics, architecture, usage, and governance [6], [7]. Google’s overload guidance emphasizes resource-based capacity, controlled degradation, and avoiding harmful retries [5]. These practices inform evidence; they do not replace product, finance, security, legal, accessibility, or operational authority.

## Prerequisites and Retrieval

Retrieve fixed, variable, marginal, average, sunk, opportunity, switching, and expected cost; budget; forecast; unit economics; attribution; capacity; utilization; queue; arrival and service rate; admission; backpressure; retry; degradation; SLO; error budget; recovery point and time; retention; egress; commitment; option; lock-in; and total cost of ownership.

From SARCH-007 retrieve trade-offs; SARCH-011 through SARCH-020 provide quality tactics; SARCH-032 supplies modular monoliths; SARCH-057 supplies queues; SARCH-066 and SARCH-067 supply quantitative capacity and reliability; SARCH-069 supplies cost models; SARCH-089 supplies exception risk; and SARCH-092 through SARCH-097 provide advanced workload constraints.

## Learning Objectives

After completing this module, you should be able to:

1. state a hard budget beside nonnegotiable invariants and minimum qualities;
2. calculate lifecycle and unit cost with an honest denominator;
3. locate dominant cost drivers through measurement rather than intuition;
4. choose the minimum coherent architecture and preserve option value;
5. design admission, quotas, degradation, and recovery inside a spend envelope;
6. evaluate build, buy, managed, self-hosted, and commitment choices with switching cost;
7. bound data, observability, compute, network, and human operational cost;
8. prevent optimization from shifting harm to users, workers, or future teams;
9. validate savings against workload, failure, and quality evidence;
10. govern budgets continuously as prices, demand, and architecture change.

## Core Exposition

**Define the minimum legitimate service.** List the outcomes users require and the consequences of absence or error. Separate essential, valuable, experimental, and obsolete capabilities. State nonnegotiable integrity, safety, security, privacy, legal, accessibility, and recovery properties before choosing cuts.

The cheapest valid architecture may offer less breadth, slower optional work, bounded history, or explicit admission. It cannot silently lose accepted work or make essential access available only to users with newer devices. Product and affected stakeholders decide the minimum service; an infrastructure bill does not.

**Construct lifecycle cost.** Include development and review, runtime resources, licenses, support, security, compliance, on-call, incidents, data migration, backups, restoration, training, supplier management, and exit. Price volunteer or founder labor at its scarce capacity even when cash expense is zero. Otherwise the design consumes an invisible, finite subsidy.

Separate fixed and variable costs by period and scenario. Include currency, tax, discount, price tier, region, contract term, and measurement source. Model baseline, expected, peak, incident, growth, and termination cases. A monthly average that excludes a migration or traffic attack is not a ceiling.

**Choose an honest unit.** Infrastructure cost per request rewards splitting one useful action into more requests. Prefer accepted case, completed order, active learner served, report delivered, or gigabyte durably retained—then distinguish resource-efficiency metrics from value metrics. The FinOps Foundation currently makes the same distinction in its unit-economics capability [7].

Define good outcome and rejection. A failed request, bot request, duplicate retry, and successful payment should not share an unqualified denominator. Report volume beside unit cost: a lower unit cost caused by excluding hard users is not improvement.

**Measure the dominant drivers.** Build a cost tree from capability to component to resource: CPU-seconds, memory-hours, retained bytes, reads, writes, requests, logs, metrics cardinality, egress, external calls, seats, tickets, and operator minutes. Reconcile estimates to invoices and people allocation.

Prioritize by contribution and controllability. A 50% optimization of 2% of spend saves 1%; a 10% reduction of a 60% driver saves 6%. Preserve uncertainty ranges. Allocation tags and labels can be missing or manipulated, so validate with independent totals and shared-cost policy.

**Prefer the minimum coherent structure.** Begin with one deployable application and one durable store when they meet failure, scale, ownership, and release needs. Modules preserve internal boundaries without paying distributed coordination tax. Add caches, queues, replicas, search, streams, and services only for evidenced constraints.

Minimal does not mean unstructured. A tangled monolith creates expensive change and failure. Maintain domain seams, explicit transactions, testability, dependency direction, and replacement points. Delay irreversible distribution while keeping the evidence and interfaces needed to evolve.

**Preserve option value.** Use reversible decisions for uncertain demand: portable data, documented contracts, replaceable adapters, short commitments, measured pilots, and scheduled review. Avoid buying peak capacity or complex orchestration before the workload exists. Also avoid a design whose emergency migration would exceed the organization’s entire budget.

Reversibility has carrying cost. Supporting three databases “just in case” is not option value if it triples testing. Preserve the few high-value exits: authoritative data export, identity independence, reproducible build, documented recovery, and contract termination.

**Control demand before adding supply.** Authenticate and validate cheaply, apply quotas and budgets, reject impossible or abusive work, deduplicate, coalesce, cache within correctness limits, and batch suitable work. Make clients honor backpressure. Retries require exponential delay, jitter, caps, and idempotency; they must not turn scarce capacity into a collapse.

Admission belongs ahead of saturated resources. Reserve capacity for health, recovery, security, and high-value operations. Queue only work that remains valuable later and bound queue age and bytes. When $\lambda$ exceeds sustained $\mu$, backlog grows; a cheap queue merely delays the visible failure.

**Design ordered degradation.** Identify modes before overload: omit personalization, reduce result depth, serve a bounded stale cache, defer reports, reduce media variants, or reject optional work. State triggers, user message, quality effect, invariant, owner, exit, and test.

Never degrade authentication, authorization, integrity, audit required for harm control, or accessibility. A cheaper approximate result needs explicit semantics. Google’s overload guidance describes cheaper degraded responses but also admits that errors are necessary when capacity cannot compute them [5].

**Budget reliability from consequence.** More replicas and regions cost money; too little recovery can end the organization. Define RPO, RTO, failure domains, maximum outage, and data-loss consequence. Protect irrecoverable accepted state first; recomputable views and caches may use cheaper recovery.

A backup that has never restored is speculative savings. Test restore time and labor. One regional deployment plus off-region backup may be rational for some services; safety-critical or national emergency services may require independent live paths. Record the legitimate risk decision.

**Bound data lifecycle.** Every byte should be authoritative, derived, cached, audit, diagnostic, or transient, with retention, deletion, compression, access, and rebuild rules. Expensive data commonly hides in attachments, duplicate events, debug logs, indexes, snapshots, and forgotten environments.

Do not delete raw or audit evidence without authority. First remove duplicates and abandoned copies, expire disposable caches, tier cold data, compact under replay requirements, and rebuild derived products on demand when compute and dependency costs support it. Include retrieval and deletion cost, not storage price alone.

**Treat network movement as architecture.** Co-locate chatty compute and data, compress where CPU and latency justify it, aggregate safely, prefer content identity for deduplication, and expose pagination and bulk interfaces. Cross-region, cross-zone, Internet, and provider egress have different cost and failure consequences.

Cache keys include authorization and semantic variation. A cache hit that leaks tenant data is not savings. Measure hit rate, origin avoidance, invalidation, stale consequence, object size, and egress. Avoid moving data merely because compute looks cheaper elsewhere.

**Choose compute to workload shape.** Shared steady workloads may fit reserved capacity; bursty interruptible work may use queued elastic or preemptible resources; latency-sensitive work needs ready capacity. Serverless reduces idle operations for some shapes but can add per-invocation, state, observability, and lock-in costs.

Benchmark useful work, cold start, tail latency, memory, storage, network, and failure recovery. Autoscaling requires maximum replicas, per-tenant quotas, budget alerts, and overload policy. Infinite elasticity against abusive demand is an infinite-spend design.

**Make algorithmic cost visible.** An $O(n^2)$ comparison can dominate any hosting discount. Bound input, select indexes, precompute stable results, avoid fan-out, stream rather than materialize, and use approximate algorithms only with acceptable error. Profile production-shaped distributions, including skew.

Efficiency can reduce both cost and latency, but complexity has maintenance cost. A clever encoding saving €30/month is irrational if it needs specialist response. Prefer understandable optimizations on dominant paths and remove them when assumptions disappear.

**Control observability without blindness.** Logs, traces, metrics, profiles, and audit have different purposes. Set structured event schemas, severity, sampling, cardinality, retention, redaction, and per-source budgets. Preserve security and business audit according to risk; sample high-volume successful traces while retaining errors and exemplars.

Dynamic sampling can capture anomalies, but triggering after an event may miss its beginning. Keep low-cost aggregate signals and bounded flight recording. Budget query and egress, not only ingestion. Observe the optimizer itself: dropped telemetry and sampling changes are material evidence.

**Evaluate managed versus self-hosted honestly.** Managed service price buys some operation, upgrades, durability mechanisms, support, and elasticity but not correct schema, access policy, cost control, or exit. Self-hosting saves margin only if the team can operate it safely within labor and incident capacity.

Compare equivalent service levels and fully loaded people. Include minimum fees, data movement, backup, support tier, required replicas, feature coupling, price-change exposure, migration tooling, and contract exit. Run a bounded proof with actual workload; do not extrapolate a toy benchmark.

**Use commitments only for stable demand.** Reserved use, enterprise contracts, and volume discounts exchange flexibility for price. Cover measured base load, not optimistic growth. Separate committed and variable capacity, renewal date, utilization, breakage, currency, and owner.

Sunk commitment is not a reason to send unsuitable workload to a platform. Reforecast. A saving against on-demand list price is not real if the committed resource stays idle or prevents a cheaper architecture.

**Allocate shared cost fairly.** Platforms, networks, security, support, and observability serve many products. Attribute direct use where reliable; allocate shared fixed cost by a governed driver; report unallocated and idle cost separately. One tenant’s burst must not silently consume every team’s budget.

Chargeback can incentivize gaming; showback supports learning but may lack authority. Use quotas, anomaly detection, and joint review. The allocation policy is a social and financial model, not physical truth.

**Protect human capacity.** Manual deployment, noisy alerts, fragile recovery, ticket gates, and bespoke variants shift invoice savings into cognitive load. Measure pages, tickets, interrupts, deployment minutes, incident hours, and expert concentration. Google’s SRE workbook describes operational overload as preventing progress on important work [9].

Automate repeated safe work after simplifying it. Do not build a platform whose maintenance exceeds the work it removes. Reduce product variants and unsupported promises. Documentation, training, and predictable failure modes are cost controls.

**Govern cost continuously.** Put budgets and unit-cost objectives in architecture decisions. Forecast before launches; alert on rate and projected ceiling; require owner and expiry for exceptions; review dominant drivers; and verify savings after change. Keep finance, product, operations, security, and affected users in the decision.

Prices and demand change. A current FinOps framework update is evidence of evolving practice, not a permanent taxonomy [6]. Bind estimates to retrieval date and price input, preserve calculation, and rerun scenarios. Roll back optimization if it violates quality or merely shifts cost.

**Test the budget envelope.** Replay expected, peak, bot, retry, large-object, hot-key, tenant-skew, regional-failure, provider-price, currency, commitment, and staff-loss scenarios. Assert cost rate, admission, queue age, degradation, SLO, data integrity, recovery, and user outcomes.

Run shadow or canary measurement where possible. A cheaper code path must pass functional, performance, security, accessibility, and failure checks appropriate to its claim. Report measured environment and confidence; never claim universal savings.

## Definitions and Notation

Let:

- $A$ be a candidate architecture and $C_{life}(A)$ its lifecycle cost;
- $I(A)$ be the conjunction of nonnegotiable invariants;
- $Q_j(A)$ be measured quality $j$ with minimum $q_j$;
- $C_f,C_p,C_o,C_r$ be fixed, people, operational, and risk cost;
- $x_i$ be metered resource quantity at price $p_i$;
- $N_g$ be good accepted outcomes and $u=C/N_g$ unit cost;
- $\lambda$ be accepted work arrival rate, $\mu$ service rate, $L$ average in-flight work, and $W$ average time in system;
- $B$ be period budget and $H=B-C$ remaining headroom;
- $m_i=\partial C/\partial x_i$ be marginal cost under a local model;
- $D_k$ be an explicit degradation mode with entry and exit conditions.

Currency, period, tax, allocation, and price version are part of every value. Expected loss $C_r=\sum_h P(h)L(h)$ can compare bounded risks, but rare catastrophic harms, uncertain probabilities, and legal duties cannot always be reduced honestly to one expectation.

## Mechanisms, Invariants, or Proof Structure

**Feasibility before optimization.** If architecture $A$ violates $I$ or any $Q_j\ge q_j$, it is outside the feasible set regardless of price. Among feasible designs, lower modeled cost is preferable only for the declared workload and assumptions. This prevents a spreadsheet from trading an unpriced mandatory property.

**Queue derivation.** Under stable long-run conditions, Little’s relation is $L=\lambda W$ [3]. If admission keeps $\lambda<\mu$, backlog can remain bounded under an appropriate variability model. If sustained $\lambda>\mu$, unfinished work increases at average rate at least $\lambda-\mu$ until demand or admission changes. Buying a queue does not change conservation of work.

**Unit-cost denominator test.** Suppose period cost is €18,000 and 20,000 accepted cases yield $u=€0.90$. Infrastructure-only cost €3,500 divided by the same outcomes is €0.175, but it excludes €14,500 of modeled lifecycle cost. If requests double through an API change while cases stay constant, cost per request can halve without any user value or cash saving. Therefore denominator governance is part of the architecture evidence.

**Executable degradation policy.** The following finite router preserves protected actions, uses a valid cache for ordinary reads, defers optional work, and rejects excess before execution. Production policy needs authentication, atomic budgets, distributed concurrency, measured costs, and accessible user responses.

<!-- bijux-verify: {"id":"route-under-budget","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"protected-capacity\nserve-cache\ndefer-optional\nreject-budget\nserve-normal\nreject-overload\n","stderr":""}} -->
```python
def route(work, *, headroom, load, cache_valid):
    if work["protected"]:
        return "protected-capacity"
    if work["kind"] == "read" and cache_valid:
        return "serve-cache"
    if work["optional"] and (headroom < work["cost"] or load > 0.8):
        return "defer-optional"
    if headroom < work["cost"]:
        return "reject-budget"
    if load <= 0.8:
        return "serve-normal"
    return "reject-overload"

base = {"kind": "write", "cost": 3, "protected": False, "optional": False}
cases = [
    (base | {"protected": True}, 0, 1.0, False),
    (base | {"kind": "read"}, 0, 1.0, True),
    (base | {"optional": True}, 1, 0.5, False),
    (base, 1, 0.5, False),
    (base, 5, 0.5, False),
    (base, 5, 0.9, False),
]
for work, headroom, load, cache_valid in cases:
    print(route(work, headroom=headroom, load=load, cache_valid=cache_valid))
```

## Alternatives and Trade-Offs

**Breadth versus quality floor.** Fewer complete capabilities may be safer than many unreliable ones. Protect essential outcomes and cut optional breadth before hidden integrity or accessibility.

**Vertical simplicity versus distributed scale.** One deployable and database reduce fixed operational surfaces. Distribution adds independent scaling or failure isolation when evidence requires it, but each boundary has recurring cost.

**Provisioned versus elastic.** Provisioned capacity can be cheaper and predictable for stable base load; elasticity avoids idle capacity for bursts but creates price exposure. Combine a measured base with capped burst when appropriate.

**Synchronous versus deferred.** Immediate work simplifies user outcome and may be required. Queued work smooths peaks and uses cheap windows but adds storage, delay, retry, cancellation, and operator burden.

**Exact versus approximate.** Approximation can cut compute or storage but must preserve an error contract. It is unsuitable when one omitted item violates safety, money, or rights.

**Managed versus self-hosted.** Managed reduces some labor and upgrade risk at a premium and switching boundary. Self-hosting can reduce direct spend only when competence and incident capacity exist.

**Retention versus rebuild.** Retaining derived data saves recomputation; rebuilding saves storage. Compare access rate, compute, dependency availability, egress, recovery time, and governance.

## Failure Modes and Misconceptions

- **“Cheapest invoice wins.”** It omits people, incidents, recovery, and exit.
- **“Open source is free.”** License price can be zero while operation is expensive.
- **“Autoscaling controls cost.”** It can scale a bill without a ceiling.
- **“A queue solves overload.”** It stores overload until age or capacity fails.
- **“Retries improve reliability.”** Unbounded retry amplifies saturated dependencies.
- **“Every request has equal cost.”** Payload, query, tenant, and cache behavior differ.
- **“Cost per request is value.”** Request count is often manipulable and unrelated to outcomes.
- **“One region is irresponsible.”** Consequence and tested recovery determine topology.
- **“Three regions guarantee safety.”** Shared data, credentials, and deployment can fail together.
- **“Observability should be cut first.”** Blind failure and audit loss can cost more.
- **“Sampling is neutral.”** It can erase rare, slow, or disadvantaged cohorts.
- **“Commitments are guaranteed savings.”** Idle or unsuitable commitments are cost.
- **“Microservices are cheaper to scale.”** Independent scaling may not repay fixed complexity.
- **“Managed means no operations.”** Schema, policy, cost, incidents, and exit remain.
- **“Degradation is just fewer features.”** It needs explicit semantics and user truth.
- **“Security can wait for revenue.”** Breach and unsafe authority are not valid financing.
- **“Founder time is free.”** It is finite capacity and concentration risk.
- **“Optimization is permanent.”** Workloads, prices, contracts, and teams change.

## Worked Examples

### Example 1

**Nonprofit case management.** A €18,000 monthly ceiling includes €3,000 fixed, €9,000 allocated people, €1,500 operations, €1,000 risk reserve, and €3,500 metered resources. At 20,000 accepted cases, full unit cost is €0.90. The design protects durable case intake, privacy, accessibility, backup, and restore; it defers exports and removes abandoned media variants. **Conclusion:** an honest unit cost changes which optimization matters.

### Example 2

**One region with tested recovery.** A young product cannot fund two live regions. Its consequence analysis permits four hours of outage and 15 minutes of data loss. It uses one region across failure zones, off-region immutable backups, infrastructure definitions, a quarterly restore exercise, and a migration trigger. It does not advertise continuous regional availability. **Conclusion:** explicit lower service with verified recovery can be more responsible than unfunded active-active complexity.

### Example 3

**Image variants dominate storage.** An education service stores every upload in 18 sizes, though analytics show four sizes serve 99.7% of views. It retains the original and four canonical derivatives, generates rare sizes on demand with a bounded cache, and validates accessibility and print needs before deletion. **Conclusion:** classify authoritative, reproducible, and cached data before buying more storage.

### Example 4

**Retry storm during overload.** A clinic service handles 100 writes/s but receives 130; clients retry every second. The queue grows by at least 30/s before retries and then faster. Admission rejects optional bulk imports, preserves protected clinical writes, returns retry guidance with jitter, and drains scheduled work later. **Conclusion:** overload control changes demand; buffering alone does not.

### Example 5

**Batching reports.** Individual reports cost €0.04 in repeated scans; one hourly shared computation costs €8 for 1,000 reports, or €0.008 each. Reports allow two-hour latency, so batching saves €32 per 1,000 while preserving a freshness label. Urgent statutory reports retain an immediate path. **Conclusion:** latency flexibility can buy large savings when policy distinguishes exceptions.

### Example 6

**Tiered inference.** A support system routes all cases to an expensive model. A tested rules baseline resolves 70%, a small model handles 25%, and 5% reach the expensive model; uncertain cases go to humans. Evaluation includes accuracy, subgroup errors, latency, appeals, and workload, not token price alone. **Conclusion:** cascades save only when routing and fallback preserve decision quality and human capacity.

### Example 7

**Egress surprise.** Compute in a cheap region reads 40 TB/month from data elsewhere, and transfer costs exceed compute savings. Co-locating the job, sending a minimized intermediate, or scheduling one governed replica is cheaper. The team includes failure, residency, and staleness before moving. **Conclusion:** component price without data topology is not architecture cost.

### Example 8

**Cardinality explosion.** A release adds user ID to every metric, multiplying active series and exhausting the telemetry budget. The team removes unbounded identity from metrics, keeps aggregate SLO signals, uses sampled traces with protected error cohorts, and retains authorized audit events separately. **Conclusion:** telemetry types need distinct identity, retention, and cost policy.

### Example 9

**Managed versus self-hosted database.** Self-hosting saves €2,000/month in quoted fees but adds 30 engineer hours, patching, backup, and an estimated incident burden beyond the team’s capacity. A smaller managed tier plus query/index repair saves more lifecycle cost. A portable logical export and restore test protect exit. **Conclusion:** compare equivalent operations and failure obligations, not license or instance price.

### Example 10

**Disaster-information service.** Budget is fixed while storm traffic is uncertain. The service precomputes static multilingual guidance, uses CDN caches with signed version and expiry, reserves origin capacity for authoritative alerts and corrections, caps expensive search, degrades maps before text, and protects accessibility. Public authorities—not cost automation—authorize alerts. **Conclusion:** static stability, priority, and truthful degradation preserve the high-value path under both spend and load pressure.

## Cross-Program Connections

- [Software Engineering: Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) owns operational load, delivery, incident, and SLO practice.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) owns query, index, storage, and engine cost mechanisms.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) owns pipeline, retention, and batch cost execution.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns value, governance, lifecycle, and meaning of retained data.
- [Large-Scale Data Systems](../../21-large-scale-data-systems-engineering/ROADMAP.md) owns resource-efficient distributed processing.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns threat and control mechanisms that define nonnegotiable security cost.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns shared developer capability and attribution mechanisms.
- [Cloud and Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) owns provider resources, commitments, and infrastructure implementation.

## References

1. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021.
2. Martin L. Abbott and Michael T. Fisher, *The Art of Scalability*, 2nd ed., Addison-Wesley, 2015.
3. John D. C. Little, “A Proof for the Queuing Formula: L = λW,” *Operations Research* 9(3), 1961. [DOI record](https://doi.org/10.1287/opre.9.3.383).
4. David J. Collis and Michael G. Rukstad, “Can You Say What Your Strategy Is?”, *Harvard Business Review*, 2008.
5. Alejandro Forero Cuervo, “Handling Overload,” in *Site Reliability Engineering*, O’Reilly/Google, 2016. [Official online chapter](https://sre.google/sre-book/handling-overload/).
6. FinOps Foundation, “FinOps Framework Overview.” [Official framework](https://www.finops.org/framework/). Current 2026 framework checked 2026-09-06.
7. FinOps Foundation, “Capability: Unit Economics.” [Official capability guidance](https://www.finops.org/framework/capabilities/unit-economics/). Current guidance checked 2026-09-06.
8. Martin Kleppmann and Chris Riccomini, *Designing Data-Intensive Applications*, 2nd ed., O’Reilly Media, February 2026. [Publisher record](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/).
9. Maria-Hendrike Peetz et al., “Identifying and Recovering from Overload,” in *The Site Reliability Workbook*, O’Reilly/Google, 2018. [Official online chapter](https://sre.google/workbook/overload/).
10. David L. Parnas, “On the Criteria To Be Used in Decomposing Systems into Modules,” *Communications of the ACM* 15(12), 1972. [DOI record](https://doi.org/10.1145/361598.361623).
11. Jerome H. Saltzer and Michael D. Schroeder, “The Protection of Information in Computer Systems,” *Proceedings of the IEEE* 63(9), 1975. [MIT-hosted paper](https://web.mit.edu/Saltzer/www/publications/protection/).
12. John R. Douceur et al., “Leveraging Statistical Estimation to Save Energy in Cloud Computing,” *E2DC 2014*. [Microsoft Research publication](https://www.microsoft.com/en-us/research/publication/leveraging-statistical-estimation-to-save-energy-in-cloud-computing/).

## Exercises

### Exercise 1

**Define feasibility.** A proposal removes encryption, backup, and screen-reader testing to meet a cash ceiling. Explain why the optimization formulation rejects it and propose a legitimate reframing.

### Exercise 2

**Calculate lifecycle unit cost.** Monthly costs are €4,000 fixed, €12,000 people, €5,000 metered, €2,000 operations, and €1,000 modeled risk. The service produces 30,000 accepted outcomes from 900,000 requests. Compute lifecycle cost per accepted outcome, infrastructure-only cost per outcome, and lifecycle cost per request. Explain which metric should govern product value.

### Exercise 3

**Diagnose queue economics.** Accepted work arrives at 75 jobs/minute and sustained service is 60. The queue begins empty. Ignoring variability, calculate backlog after two hours and explain why cheaper queued workers have not solved the budget problem. Give three controls.

### Exercise 4

**Compare two viable database choices.** Design a five-year comparison between a managed database and self-hosting. Include equivalent quality, labor, incident, backup, restore, growth, commitment, support, data movement, lock-in, and exit evidence.

### Exercise 5

**Transfer to a rural public library network.** Design a severely constrained architecture for 60 libraries with intermittent links, old devices, multilingual and accessible catalogs, patron privacy, lending integrity, digital media, and two central operators. Define the minimum service, lifecycle budget model, degradation order, data/observability policy, recovery, attribution, governance, and validation.

## Answers to the Exercises

### Answer 1

Encryption, recoverability, and accessibility are candidate invariants or minimum qualities. A design violating them is outside the feasible set; its lower price cannot win the constrained optimization. Reframe by narrowing legitimate scope, reducing optional features, retaining fewer authorized derived copies, using one coherent deployment, serving static content, deferring nonessential reports, negotiating a different recovery objective with legitimate owners, or admitting fewer users honestly. Security, data, legal, accessibility, product, and affected-user authorities must decide real floors. The answer must not relabel externalized harm as savings.

### Answer 2

Lifecycle cost is €24,000/month, so cost per accepted outcome is €24,000/30,000 = €0.80. Metered infrastructure alone is €5,000/30,000 ≈ €0.1667 per outcome. Lifecycle cost per request is €24,000/900,000 ≈ €0.0267. Accepted-outcome unit cost is the strongest of these for product value because it connects full modeled cost to a useful result. The other metrics diagnose infrastructure and traffic efficiency. All should report scope and volume; the outcome definition must not exclude hard or rejected users to improve the number.

### Answer 3

Arrival exceeds service by 15 jobs/minute. After 120 minutes the idealized backlog is $15\cdot120=1{,}800$ jobs, and it continues growing. The queue changes timing, not conservation of work; delayed jobs may lose value and add storage and operations. Controls include admission or quotas that reduce accepted rate, increasing efficient service capacity within a measured budget, simplifying or batching the job to reduce work, and degrading or removing low-value job classes. Unlimited retry is harmful. A credible answer also bounds age and communicates rejection or delay.

### Answer 4

Normalize both candidates to the same workload, regions, durability assumptions, RPO/RTO, security, support hours, upgrade obligation, and growth scenarios. Managed cost includes tier, storage, operations, backup, replicas, I/O, egress, support, price and commitment exposure, feature coupling, and provider incident/exit limits. Self-hosted cost includes compute, storage, replicas, backup, monitoring, licenses, patching, on-call, specialist labor, capacity headroom, incident loss, and hardware or cloud operation.

For each year model baseline, peak, failure, migration, and termination; separate cash, allocated labor, and uncertainty. Benchmark representative queries and restore, rehearse upgrades, and measure operator time. Test logical export, restore into an alternate, identity/network dependencies, data-movement duration/cost, and last reversible date. Use sensitivity analysis for demand, staff rate, incident frequency, price, and currency. Choose only among candidates that meet the same invariants and quality floors; document residual lock-in and review triggers rather than claiming one universal winner.

### Answer 5

The minimum service is local catalog search, accessible multilingual patron interaction, privacy-preserving patron identity, offline lending/return with bounded item authority, durable local transaction evidence, and eventual central reconciliation. Optional recommendations, analytics, high-resolution covers, and bulk reports degrade first. Each branch uses a modest local application and transactional store with stable item/patron/operation IDs; the center uses one modular application and one authoritative catalog rather than dozens of services. Static catalog snapshots and language/accessibility resources travel in resumable packages. Rare digital media uses capped, licensed caching; essential text outranks images.

The lifecycle model includes two operators, branch support, old-device testing, connectivity, storage, backups, security, accessibility review, incident travel, licensing, training, migration, and exit—not only hosting. Units include cost per active branch and accepted loan, with volume and rejection. Rights allocate unique item loans to the holding branch; cross-branch reservations remain pending when coordination is unavailable. Local queues are byte/age bounded, retries idempotent, and reconnect is jittered. One branch cannot consume every central or network budget.

Retain authoritative loans, corrections, consent, and required audit; expire caches, sampled diagnostics, and obsolete media under policy. Metrics avoid patron identity and bound branch/cardinality; security audit remains separately protected. Degradation labels stale catalog and pending reservation honestly, never weakens authorization or screen-reader support. Recovery uses encrypted local journals, tested branch export, central off-site backup, documented cold start, and quarterly sample restore. Lost-device and credential epochs fence reconnect.

Govern monthly budget, projected ceiling, operator workload, queue age, sync delay, accepted loans, privacy events, accessibility defects, cache effectiveness, storage, and restore evidence with library, finance, privacy, accessibility, branch, and patron representation. Validate long partitions, cold old devices, clock error, duplicate loans, disk full, reconnect herd, central outage, corrupt catalog, lost branch device, language fallback, keyboard/screen-reader flows, price change, and one-operator absence. The architecture succeeds by preserving lending and equitable access inside an honest envelope, not by serving the most connected patrons cheaply.
