---
module_id: SARCH-069
program: Software Engineering: Software Architecture
level: 2
module_number: 69
title: Cost Models and Unit Economics
status: complete
last_verified: 2026-09-06
---

# Cost Models and Unit Economics

## One-Page Review

### Governing question

How can an architecture team connect resource consumption, lifecycle commitments, and delivered outcomes to defensible cost decisions without confusing an invoice allocation with causality or optimizing away reliability, security, safety, and future options?

### Essential definitions

- a **cost object** is the product, tenant, transaction, capability, environment, or decision whose cost is being studied;
- a **cost driver** is a measurable factor that changes resource consumption or another causal component of cost;
- a **direct cost** is traceable to one cost object; an **indirect cost** requires an explicit allocation rule;
- a **fixed cost** does not change within the relevant activity range and time horizon; a **variable cost** changes with activity; a **step cost** changes when a capacity threshold is crossed;
- **marginal cost** is the cost of one additional unit or a small increment; **average cost** is total cost divided by units;
- **total cost of ownership** covers acquisition, integration, operation, change, assurance, support, migration, and retirement within a declared boundary and horizon;
- **unit cost** divides an eligible cost numerator by an eligible technical or business denominator;
- **unit economics** connects technology cost to a delivered unit of value or outcome, not merely to infrastructure utilization;
- **contribution margin** is revenue less attributable variable cost under a declared accounting policy; it is not net profit;
- **opportunity cost** is the value of the best forgone alternative; a **sunk cost** cannot be changed by the current decision.

### Central model, mechanism, or theorem

For output volume $q$ over a declared horizon, a useful first model is

$$
C(q)=F+vq+S(q)+E(q),
$$

where $F$ is fixed cost in the relevant range, $v$ is variable cost per unit, $S(q)$ represents capacity steps, and $E(q)$ represents explicitly modeled externalities or expected consequences. Average cost is $AC(q)=C(q)/q$; discrete marginal cost is $MC(q,\Delta q)=[C(q+\Delta q)-C(q)]/\Delta q$. Their difference matters: fixed-cost dilution can lower average cost even when the next unit costs the same, while a threshold can make the next small batch unusually expensive.

### Critical invariants

- every number names scope, period, currency, price basis, cost object, denominator, and source;
- attempted work, successful work, timely-correct work, customers, and revenue are not interchangeable denominators;
- cost allocation is labeled as a policy unless evidence supports a causal claim;
- shared, idle, committed, support, migration, assurance, and retirement costs remain visible;
- capacity headroom and independent recovery resources are evaluated against the qualities they protect;
- historical invoice cost is not automatically the cost of a future architecture;
- uncertainty, sensitivity, thresholds, and tail scenarios accompany point estimates;
- sunk cost is excluded from forward choice, while switching and reversibility costs are included;
- economics informs decisions but does not grant authority to waive legal, safety, security, privacy, accessibility, or reliability obligations;
- the model is reconciled with measured consumption and delivered outcomes after implementation.

### Common failures

Common failures include optimizing cost per request while retries rise; dividing by registered rather than active customers; treating an equal split as causal attribution; hiding shared platforms as “free”; classifying all consumption-priced services as variable; assuming idle failover capacity is waste; ignoring people, licenses, data movement, taxes, support, assurance, and exit; using list prices after negotiated commitments; amortizing over an implausible lifetime; treating expected loss as a safety permission; comparing alternatives with different quality; counting sunk expenditure in a go-forward choice; and presenting a precise forecast without a sensitivity range.

### Compact example

A service costs \$120,000 per month before traffic and \$0.004 per attempted transaction. At 20 million attempts, total cost is \$200,000 and average cost is \$0.010 per attempt, while marginal cost away from a capacity threshold remains \$0.004. If only 19 million attempts become timely, correct outcomes, the decision-relevant unit cost is $\$200{,}000/19{,}000{,}000\approx\$0.010526$. The denominator changes the diagnosis without changing the invoice.

### Connections

[SARCH-068](068-threat-modeling-at-architecture-scale.md) supplies security consequences and controls that cost analysis must preserve. [SARCH-070](../ROADMAP.md) next integrates quantitative evidence into an architecture review. [SARCH-066](066-performance-and-capacity-models.md) and [SARCH-067](067-availability-and-reliability-models.md) supply the workload, capacity, and failure models used here.

## Governing Question

Architecture commits an organization to resource demand, operational work, supplier relationships, migration paths, and failure exposure. Cost therefore is not a label attached after design. It is behavior produced by workload, topology, state, quality requirements, price schedules, labor, and time.

The architect's task is to build a model fit for a particular decision: define comparable outcomes, expose causal drivers, preserve material constraints, quantify uncertainty, and specify how evidence will update the model. The objective is not the lowest invoice. It is sustainable value within stakeholder-approved obligations and risk boundaries.

## Why This Matters

A cheap request can be an expensive business outcome when it is duplicated, late, incorrect, fraudulent, manually reconciled, or followed by support work. Conversely, intentionally unused capacity may be economically rational when it contains overload, enables maintenance, or provides recovery. A model that sees only metered compute rewards locally visible savings and hides system-wide consequences.

Cost structure also changes architectural flexibility. A long commitment can reduce a rate while increasing lock-in. A shared platform can exploit economies of scale while creating allocation disputes and a broad dependency. A managed service can reduce operational labor while increasing data-movement cost and exit complexity. These are not accounting details after the fact; they are architecture trade-offs.

## Prerequisites and Retrieval

Retrieve rate, stock, flow, probability, expectation, distribution, confidence interval, sensitivity analysis, present value, queue, utilization, throughput, goodput, capacity headroom, service-level objective, error budget, availability, reliability, threat, control, coupling, reversibility, and quality-attribute scenario.

From SARCH-061 through SARCH-068 retrieve explicit scenarios, trade-off points, fitness functions, dependency structure, capacity, reliability, and threat models. Basic finance and management-accounting terms are introduced here only to the precision needed for architecture. Finance owns financial reporting, tax, capital policy, and official discount rates; product and domain authorities own value and obligations; this chapter owns the trace from architecture mechanisms to decision-relevant cost.

## Learning Objectives

After completing this module, you should be able to:

1. define cost objects, boundaries, horizons, drivers, and allocation policies for an architecture decision;
2. distinguish fixed, variable, step, marginal, average, opportunity, sunk, and lifecycle costs;
3. construct unit-cost denominators that represent successful stakeholder outcomes;
4. trace workload classes through resource demand and price schedules;
5. model shared services, idle capacity, commitments, migration, and retirement without hiding them;
6. compare alternatives at equivalent quality and risk boundaries;
7. use break-even, present-value, expected-consequence, scenario, and sensitivity calculations appropriately;
8. distinguish measured cost, forecast cost, allocated cost, and causal explanation;
9. design telemetry and governance that reconcile model predictions with operation;
10. present an economic recommendation with uncertainty, guardrails, decision rights, and falsification criteria.

## Core Exposition

**Frame the decision before collecting numbers.** State the decision, alternatives, stakeholders, cost object, time horizon, currency, price date, regions, workloads, and required outcomes. “Reduce cloud cost” is not a decision. “Choose a two-year deployment architecture for the European document-conversion service while meeting its latency, availability, retention, and data-residency requirements” is reviewable.

Define the counterfactual. A saving is the difference between feasible alternatives under the same boundary, not the difference from an arbitrary budget. The baseline may be continue, retire, defer, buy, build, share, or redesign. Include transition periods in which old and new systems operate together.

**Choose the cost object.** A resource bill can be grouped by account, service, team, product, tenant, feature, environment, transaction, or outcome. No grouping is universally correct. The object must match the decision right: a team can act on service cost, a product owner on cost to serve a cohort, and an executive on portfolio investment.

Shared resources require two views. The stewardship view accounts for the whole resource so no cost disappears. The decision view asks which cost changes if a particular choice changes. An allocation can distribute responsibility without proving that any recipient caused the cost.

**Set the boundary.** Direct infrastructure includes compute, storage, network, accelerator, and managed-service consumption. A fully loaded boundary may also include software licenses, support, observability, security controls, facilities, operational labor, incident response, compliance evidence, vendor management, integration, training, and shared platforms.

Lifecycle scope adds discovery, acquisition, migration, parallel operation, data conversion, validation, change, decommissioning, retention, and exit. State exclusions. Omitting a cost can be reasonable for a narrow marginal decision, but it must not masquerade as total cost of ownership.

**Classify behavior over a relevant range.** Fixed and variable are conditional classifications. A salaried team may be fixed for next month's traffic decision but variable over a three-year portfolio decision. A database cluster can be fixed within its current capacity band, step-variable at node thresholds, and avoidable after contract expiry.

Do not infer behavior from billing vocabulary. “Serverless” or consumption pricing does not make all cost proportional to useful output: minimum instances, provisioned throughput, retained state, retries, logging, and support may remain fixed or nonlinear. Likewise, owned hardware has energy and wear costs at the margin even when purchase cost is sunk.

**Separate average and marginal cost.** Average cost spreads the selected numerator over the selected denominator. Marginal cost asks what changes for an increment. The average may fall through fixed-cost dilution while marginal cost is constant. Near a capacity step, a small increment can trigger a large discrete cost. Long-run marginal analysis permits capacity and staffing to change; short-run analysis does not.

Architecture decisions frequently depend on incremental rather than fully allocated cost. A shared platform with spare capacity may serve one more team cheaply even though its allocated average cost is high. Once the increment crosses a scaling or staffing threshold, that conclusion changes. Record the range for which the estimate applies.

**Model workload classes.** Aggregate transaction counts conceal different resource demand. Partition demand by operation, tenant, size, region, priority, consistency, model, cache behavior, or failure path. For class $c$ and resource $k$, a linear first approximation is

$$
C_c=\sum_k u_{c,k}p_k,
$$

where $u_{c,k}$ is class consumption and $p_k$ is the effective unit rate. Add fixed and nonlinear terms separately. This is an attribution model only when measurement and mapping are sound; it becomes a forecast when $u$ or $p$ is projected.

Connect logical demand to physical consumption: business events produce API calls; calls fan out to services; services read, write, transfer, log, and retry; replicas and indexes multiply work. Trace amplification. The cheapest component rate can be irrelevant if topology causes more units to be consumed.

**Use an outcome denominator.** Technical unit metrics such as cost per CPU-hour, stored gibibyte, or request help engineers control resources. Business unit metrics such as cost per settled payment, resolved case, active learner, or on-time shipment connect spending to value [8]. Both are useful, but they answer different questions.

Define eligibility and success. Attempts, accepted requests, completed workflows, correct results, and durable settlements are distinct. Exclude or separately report synthetic traffic, abuse, replays, cancellations, and internal maintenance when appropriate. Segment cohorts when averaging would hide an expensive or underserved group.

Goodput is work that meets the full outcome contract. If retries raise attempts faster than successful outcomes, cost per attempt may look stable while cost per good outcome rises. Pair unit cost with latency, correctness, freshness, durability, security, and availability indicators so efficiency cannot improve by degrading the service.

**Trace price mechanics.** Effective price depends on region, time, volume tiers, reservation or commitment, license, support tier, tax, currency, data direction, operation count, and billing granularity. Preserve the distinction among list, contracted, amortized, and realized rates. Current vendor prices are mutable evidence, not durable architecture constants.

Commitments exchange flexibility and utilization risk for a lower rate. Model upfront charges, eligible usage, term, utilization distribution, resale or modification options, and opportunity cost. A break-even hour count is necessary but insufficient: correlated demand decline, architecture change, and service retirement can strand the commitment.

**Model capacity steps and headroom.** Capacity is constrained by the first saturated bottleneck, not by average utilization. Replicas, partitions, licenses, network links, and on-call coverage can change discretely. Use the performance model from SARCH-066 to translate workload into safe capacity, including peak distribution, maintenance, failure, and growth.

Headroom is not automatically waste. It may protect latency, absorb forecast error, tolerate failure, or preserve recovery. Attribute its cost to the requirement it satisfies. Unused capacity with no named requirement, evidence, or owner is a candidate for removal; required reserve is part of delivering the unit.

**Include reliability and security economics without pricing away obligations.** Expected consequence can compare uncertain options when outcomes, probabilities, dependencies, and losses are defensible:

$$
\mathbb{E}[L]=\sum_i P(H_i)L_i.
$$

This is not permission to accept catastrophic harm, nor a claim that every impact is monetizable. Heavy tails, strategic attackers, common causes, missing events, ethical duties, regulation, and distributional harm can invalidate a simple expectation. Use scenarios and ranges when calibration is weak.

Security, privacy, safety, accessibility, integrity, and minimum reliability are constraints established by authorized stakeholders and applicable obligations. Cost analysis can compare compliant mechanisms and expose residual consequences. It cannot decide that an unlawful, discriminatory, unsafe, or insecure outcome is cheap enough.

**Account for people and operations.** Architectural complexity consumes attention through review, deployment, patching, incident response, capacity planning, data governance, vendor management, and learning. Headcount multiplication is a crude proxy because work is not homogeneous and teams share responsibilities. Prefer observed activity, queue, interruption, and service ownership evidence, with ranges for future work.

Automation has acquisition, maintenance, and failure costs. A tool that reduces routine effort can increase rare diagnostic difficulty. Include the human system, escalation paths, specialist concentration, time zones, turnover, and recovery rehearsal rather than treating labor as a flat percentage of infrastructure.

**Include data and movement.** Storage cost depends on replicas, versions, indexes, backups, retention, retrieval, operations, encryption, and deletion evidence. Movement can be charged by direction or boundary and can dominate a compute saving. Data gravity also creates latency, privacy, jurisdiction, and exit constraints not captured by a transfer rate.

Model steady-state and transition data separately. A migration may require backfill, validation, dual write, parallel read, reconciliation, freeze, archive, and rollback copies. “Move 100 TB” understates operations, retries, scanning, verification, and retained source data.

**Value time consistently.** Alternatives distribute cash and benefits differently. Present value discounts a future amount $X_t$ at periodic rate $r$ as $X_t/(1+r)^t$. For cash costs,

$$
PV(C)=\sum_{t=0}^{T}\frac{C_t}{(1+r)^t}.
$$

Use the organization's finance-approved rate, currency assumptions, tax treatment, and horizon for an actual investment decision. Present value makes timing comparable; it does not make forecast inputs certain. Report undiscounted operational quantities too, so architecture mechanisms remain visible.

**Preserve options and switching costs.** A reversible architecture can have value under uncertainty because it permits later learning. That value is not captured by comparing expected monthly invoices alone. Record contract exit, data export, compatibility, skill, rewrite, testing, parallel-run, and customer-transition costs.

Do not count sunk cost as a reason to continue. The current decision compares future consequences of feasible choices. Existing assets can still have opportunity value, disposal cost, or constraints; those are forward-looking. “We have already spent \$2 million” alone is not an economic argument for another dollar.

**Run sensitivity and scenario analysis.** Identify uncertain drivers: demand, mix, cache hit rate, data size, failure rate, staff effort, negotiated rate, exchange rate, migration duration, or retirement date. Vary one input to find sensitivity and vary coherent sets to form scenarios. Locate break-even boundaries rather than hiding them behind one forecast.

A robust choice performs acceptably across plausible scenarios. A fragile winner depends on one optimistic input and deserves a pilot, option, guardrail, or different choice. Probability distributions are valuable only when calibrated; otherwise, transparent ranges are more honest than simulated precision.

**Govern definitions and evidence.** Give each metric an owner, formula, version, source, coverage, latency, quality rule, and change process. Reconcile resource records to invoices and business events to outcome records. Track unallocated cost explicitly. Restatement after corrected data should be visible rather than silently rewriting history.

The current FinOps Framework describes collaborative financial accountability and distinguishes resource-efficiency from business unit metrics [8]. That operating model is useful, but architecture retains responsibility for mechanism and quality: cost data alone does not explain why the system consumed resources or whether the outcome was correct.

**Close the feedback loop.** Before implementation, state forecast ranges and the observations that would falsify them. After rollout, compare workload, consumption, unit rate, total cost, quality, and outcomes. Decompose variance into price, volume, mix, efficiency, quality, and scope effects.

Optimization is an experiment. A cache change may reduce database reads but increase staleness and invalidation work; a shared service may lower average cost but widen blast radius. Retain rollback criteria and observe the whole outcome vector.

## Definitions and Notation

Let:

- $o$ denote a cost object and $B$ its declared boundary;
- $T$ denote the analysis horizon and $t$ a period within it;
- $q_c$ denote eligible output units for workload class $c$;
- $g_c\le q_c$ denote units meeting the declared good-outcome contract;
- $u_{c,k}$ denote consumption of resource $k$ by class $c$;
- $p_{k,t}$ denote the effective rate for resource $k$ in period $t$;
- $F_t$ denote fixed cost in the relevant range;
- $S_t(q)$ denote discrete or nonlinear capacity cost;
- $A_t$ denote allocated indirect cost under a named policy;
- $L_i$ denote the consequence assigned to scenario $i$ and $P(H_i)$ its modeled probability;
- $r$ denote a finance-approved periodic discount rate;
- $C_t$ denote cash cost in period $t$;
- $V_t$ denote revenue or another explicitly governed value measure.

Then a fully stated unit metric has the form

$$
UC=\frac{\sum_{t\in T}C_t(B,o)}{\sum_{c,t}g_{c,t}},
$$

with scope, eligibility, quality, and period definitions attached. If the denominator is attempts rather than good outcomes, label it accordingly.

**Measured cost** comes from observed consumption and effective rates. **Forecast cost** projects future drivers. **Allocated cost** distributes indirect cost by policy. **Avoidable cost** disappears if a choice is made within the stated horizon. **Incremental cost** is the forward difference between alternatives. **Economic cost** may include opportunity cost and external consequences beyond recorded expenditure. These quantities may differ without any arithmetic error.

## Mechanisms, Invariants, or Proof Structure

### Decision procedure

1. State decision, counterfactual, stakeholders, constraints, alternatives, horizon, and uncertainty.
2. Define cost objects and reconcile a complete stewardship boundary.
3. Define technical and business denominators, including success and quality eligibility.
4. Trace each workload class through architecture mechanisms to resource consumption and operational work.
5. Apply effective rate schedules, commitments, capacity steps, shared costs, and lifecycle transitions.
6. Separate measured, allocated, forecast, marginal, and expected-consequence quantities.
7. Compare alternatives at equal required quality; show non-monetized consequences separately.
8. Recompute totals, units, break-even points, present values, and boundary cases.
9. Run sensitivity and coherent scenarios; identify dominant assumptions and irreversible commitments.
10. Assign owners, thresholds, evidence, falsification criteria, review dates, and decision authority.

### Executable unit-cost calculation

The following standard-library calculation reproduces the compact example. It proves only the arithmetic for the stated hypothetical model.

<!-- bijux-verify: {"id":"unit-cost-denominators","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"total=200000.00\naverage per attempt=0.010000\nmarginal per additional attempt=0.004000\ncost per good outcome=0.010526\n","stderr":""}} -->
```python
fixed = 120_000
variable_per_attempt = 0.004
attempts = 20_000_000
good_outcomes = 19_000_000

total = fixed + variable_per_attempt * attempts
print(f"total={total:.2f}")
print(f"average per attempt={total / attempts:.6f}")
print(f"marginal per additional attempt={variable_per_attempt:.6f}")
print(f"cost per good outcome={total / good_outcomes:.6f}")
```

### Invariants to test

- **reconciliation:** direct, shared, and explicitly unallocated amounts reconcile to the selected total;
- **dimensional consistency:** quantities combined in an equation have compatible currency, period, and unit dimensions;
- **denominator integrity:** every counted unit meets the eligibility and quality definition;
- **comparison symmetry:** alternatives use the same boundary, horizon, demand, and required outcomes;
- **causal humility:** an allocation key does not become a causal driver without intervention or other evidence;
- **constraint preservation:** an optimization does not violate a protected requirement;
- **forward relevance:** go-forward decisions exclude irrecoverable expenditure but include future switching cost;
- **uncertainty visibility:** point estimates retain ranges, scenarios, and sensitive assumptions;
- **no hidden remainder:** untagged and shared cost remains visible;
- **feedback:** observed outcomes update forecasts and decision records.

## Alternatives and Trade-Offs

**Dedicated versus shared.** Dedicated resources simplify attribution, isolation, and local control but can duplicate fixed cost and idle capacity. Shared resources pool demand and expertise but need tenancy controls, service ownership, priority policy, allocation governance, and common-cause analysis. Compare at the same isolation and recovery standard.

**Owned versus managed.** Ownership can provide control, specialized performance, and predictable high-utilization economics while requiring capital, skills, maintenance, and renewal. Managed services can accelerate delivery and transfer some operational mechanisms, while retaining customer responsibility, integration work, rate exposure, data movement, and exit cost. “Build versus buy” is a lifecycle responsibility comparison, not a sticker-price contest.

**On-demand versus commitment.** On-demand capacity preserves elasticity and exit options at a higher unit rate. Commitments can reduce effective price when eligible demand is stable, but expose utilization, forecast, and lock-in risk. Mixed portfolios can reserve the stable base and leave uncertain peaks flexible.

**Central optimization versus local ownership.** Central purchasing and standards can improve rates and consistency. Local teams know workload mechanisms and can respond quickly. A workable governance model provides timely shared cost data, central negotiation and guardrails, and local responsibility for controllable drivers without charging teams for costs they cannot influence.

**Fine-grained versus coarse allocation.** Fine granularity can reveal expensive tenants and features but adds telemetry, storage, reconciliation, and behavioral gaming. Coarse allocation is cheaper and more stable but less actionable. Increase precision only where a decision can use it and the allocation error is material.

**Efficiency versus reserve.** High utilization can lower apparent unit cost in steady state but increases queueing delay and reduces fault, maintenance, and demand headroom. Reserve can be rational insurance. Tie it to capacity and reliability models instead of applying a universal utilization target.

**Short horizon versus lifecycle.** A short horizon supports operational decisions with fewer uncertain assumptions. It can favor choices that create later migration or retirement burdens. A lifecycle horizon captures those effects but adds forecast uncertainty. Present both when they lead to different decisions.

**Financial cost versus broader consequence.** Monetary comparison is useful for fungible resources and governed financial outcomes. Environmental load, privacy, safety, accessibility, labor conditions, strategic dependence, and public harm may require separate measures and constraints. Monetization must not erase affected stakeholders or decision authority.

## Failure Modes and Misconceptions

1. **“The bill is the model.”** An invoice records charge structure, not causal architecture, outcome quality, or future behavior.
2. **“Allocated means caused.”** Equal, revenue-weighted, or usage-weighted splits are policies unless causal evidence supports them.
3. **“Average cost predicts the next unit.”** Fixed dilution and capacity steps make average and marginal cost differ.
4. **“Consumption pricing is purely variable.”** Minimums, state, commitments, operations, and staffing introduce fixed and nonlinear terms.
5. **“Cost per request is unit economics.”** It is a resource-efficiency metric unless requests reliably represent stakeholder value.
6. **“More attempts mean more value.”** Retries, abuse, duplicates, and failed work can increase attempts while goodput falls.
7. **“Idle capacity is waste.”** Named failure, maintenance, and latency headroom can be required delivery capacity.
8. **“A lower rate guarantees savings.”** Eligibility, utilization, workload growth, data movement, and lock-in determine realized cost.
9. **“Shared services are free to consumers.”** Their cost and constraints exist even when not transferred through chargeback.
10. **“Headcount times salary measures operational cost.”** It ignores work distribution, queues, interruptions, learning, and shared responsibility.
11. **“Expected loss settles risk.”** Probability and consequence may be uncalibrated, heavy-tailed, non-monetizable, or constrained by duty.
12. **“Sunk investment justifies continuation.”** Only future consequences distinguish current alternatives.
13. **“Present value removes uncertainty.”** Discounting normalizes timing; it does not validate forecasts.
14. **“Detailed numbers are accurate numbers.”** Granularity can amplify tagging, sampling, billing, and allocation errors.
15. **“A global average is fair.”** It can hide expensive mixes, subsidized cohorts, regional constraints, or underserved users.
16. **“Optimization is complete when the invoice falls.”** Quality degradation, toil, risk, or deferred migration can move cost elsewhere.
17. **“Vendor categories are durable architecture concepts.”** Products, prices, and meters change; mechanisms and demand remain the stable layer.
18. **“Finance or engineering can decide alone.”** Cost, value, obligations, and technical causality belong to different accountable roles.

## Worked Examples

### Example 1

**Situation.** A monthly service has fixed cost $F=\$120{,}000$, variable cost $v=\$0.004$ per attempt, and 20 million attempts, away from any capacity threshold.

**Reasoning.** Variable cost is $0.004\times20{,}000{,}000=\$80{,}000$. Total cost is $\$200{,}000$. Average cost is $200{,}000/20{,}000{,}000=\$0.010$ per attempt. The next attempt adds $\$0.004$ under the local linear assumption, not $\$0.010$; the fixed cost does not recur.

**Conclusion.** Average cost describes the selected population; marginal cost supports an incremental decision and differs by the allocated fixed component.

### Example 2

**Situation.** The service in Example 1 produces 19 million timely, correct outcomes from 20 million attempts.

**Reasoning.** Cost per attempt remains $200{,}000/20{,}000{,}000=\$0.010$. Cost per good outcome is $200{,}000/19{,}000{,}000\approx\$0.010526$. If a retry change raises attempts without increasing good outcomes, the first metric can remain deceptively stable while the second worsens.

**Conclusion.** The denominator must encode the outcome relevant to the decision; attempts and goodput are not substitutes.

### Example 3

**Situation.** Each replica safely supports two million monthly outcomes and costs \$1,800. Demand rises from 9.8 million to 10.2 million outcomes.

**Reasoning.** Ceiling division requires $\lceil9.8/2\rceil=5$ replicas before and $\lceil10.2/2\rceil=6$ after. The 400,000-output increase triggers \$1,800 of step cost, or $\$1{,}800/400{,}000=\$0.0045$ per incremental output from the replica step alone. At 10.4 million, the sixth replica is already present and this particular marginal step is zero until the next boundary.

**Conclusion.** Discrete capacity makes marginal cost range-dependent; a global constant-rate model misses threshold effects.

### Example 4

**Situation.** A system processes ten million operations. A read consumes a hypothetical \$0.001 of attributable resources and a write \$0.006. The mix changes from eight million reads and two million writes to six million reads and four million writes.

**Reasoning.** Initial attributable cost is $\$8{,}000+\$12{,}000=\$20{,}000$, or \$0.002 per operation. New cost is $\$6{,}000+\$24{,}000=\$30{,}000$, or \$0.003 per operation. Total volume is unchanged, but cost rises 50% because the workload mix changes.

**Conclusion.** Volume-only forecasts fail when operation classes have different resource demand; mix is a causal driver.

### Example 5

**Situation.** Flexible capacity costs a hypothetical \$0.12 per eligible hour. A one-year commitment costs \$600 upfront plus \$0.04 for each eligible hour used.

**Reasoning.** Break-even solves $0.12h=600+0.04h$, so $h=600/0.08=7{,}500$ hours. At 8,000 hours, flexible cost is \$960 and committed cost is \$920, a \$40 saving. At 7,000 hours, flexible cost is \$840 and committed cost is \$880, a \$40 loss. Neither calculation values lost flexibility or demand correlation.

**Conclusion.** A lower committed rate creates value only above its utilization boundary and after option costs are considered.

### Example 6

**Situation.** Architecture B saves a hypothetical \$18,000 per month in compute but transfers 300 terabytes per month across a charged boundary at \$0.08 per gigabyte. Use decimal units for this illustration.

**Reasoning.** Transfer volume is $300{,}000$ GB, costing $300{,}000\times\$0.08=\$24{,}000$. Net measured change is an increase of $\$24{,}000-\$18{,}000=\$6{,}000$ per month before migration, latency, privacy, or operational effects.

**Conclusion.** Workload placement must trace the whole data path; a component-level compute saving can increase system cost.

### Example 7

**Situation.** A modeled incident has annual probability 0.02 and monetized loss \$2 million. A control costs \$25,000 annually and, under a provisional model, removes that path.

**Reasoning.** The simple expected loss is $0.02\times\$2{,}000{,}000=\$40{,}000$, exceeding control cost by \$15,000. Before recommending, reviewers test probability calibration, control coverage, common causes, loss distribution, secondary harms, and legal duties. If the event can cause non-monetized safety harm, the expectation does not authorize acceptance.

**Conclusion.** Expected consequence can expose a trade-off under explicit assumptions; it does not certify the risk model or replace constraints and accountable acceptance.

### Example 8

**Situation.** A shared platform costs \$90,000 monthly. Teams A, B, and C use 60%, 30%, and 10% of measured requests, but B's requests consume four times the compute of A's and C's.

**Reasoning.** An equal split allocates \$30,000 each. A request-count split allocates \$54,000, \$27,000, and \$9,000. Neither represents compute causality because request classes differ. If the purpose is stewardship, either governed rule can reconcile the \$90,000. If the purpose is optimization, resource demand by class and fixed shared cost must be separated.

**Conclusion.** Allocation accuracy is relative to purpose; reconciliation does not establish causation or controllability.

### Example 9

**Situation.** A migration costs \$300,000 now and is forecast to save \$9,000 at each month-end for 36 months. Finance supplies a hypothetical monthly discount rate of 0.5%.

**Reasoning.** The annuity present value is

$$
9{,}000\frac{1-(1.005)^{-36}}{0.005}\approx\$295{,}839.15.
$$

Net present value of savings less migration is approximately $-\$4{,}160.85$. With no discounting, nominal savings would be \$324,000 and appear favorable. The result is sensitive to duration, achieved savings, transition cost, and approved rate.

**Conclusion.** Timing can reverse a nominal comparison; the recommendation should expose the break-even assumptions rather than announce one precise truth.

### Example 10

**Situation.** A retry policy leads to 10.8 million total attempts, 9.8 million good outcomes, and \$108,000 cost. A dashboard reports exactly \$0.010 per attempt.

**Reasoning.** The dashboard arithmetic is $\$108{,}000/10.8$ million $=\$0.010$. Outcome cost is $\$108{,}000/9.8$ million $\approx\$0.011020$. The architecture team also examines whether retries amplify overload and whether 200,000 additional successes justify their latency and failure effects.

**Conclusion.** Stable attempt cost can coexist with expensive goodput and harmful feedback; unit economics must follow outcomes and mechanisms.

## Cross-Program Connections

- [DBE-065](../../18-database-engineering/modules/065-cost-models.md) owns optimizer cost estimates for choosing database plans; this chapter owns monetary and lifecycle models for architecture choices.
- [DE-097](../../19-data-engineering/modules/097-pipeline-capacity-and-cost.md) owns pipeline-specific capacity and cost; this chapter supplies the cross-system decision boundary and quality-preserving comparison.
- [LSDS-099](../../21-large-scale-data-systems-engineering/modules/099-cost-attribution-and-workload-governance.md) owns large-scale data workload attribution; this chapter generalizes stewardship, causal humility, and unit outcomes across architectures.
- [PLAT-082](../../29-platform-engineering/modules/082-control-plane-capacity.md) owns platform control-plane capacity; this chapter explains how shared reserve and allocation enter architecture economics.
- [SARCH-068](068-threat-modeling-at-architecture-scale.md) provides adversarial paths and residual risks whose controls and consequences must remain visible rather than being reduced to infrastructure price.
- [SARCH-070](../ROADMAP.md) uses this cost evidence together with quality scenarios, risks, capacity, reliability, and threats in a governed architecture review.

## References

1. Srikant M. Datar and Madhav V. Rajan, *Horngren's Cost Accounting: A Managerial Emphasis*, Global 17th ed., Pearson, print ISBN 9781292363073, 2020. Cost behavior, cost objects, allocation, and decision relevance.
2. Hal R. Varian, *Intermediate Microeconomics: A Modern Approach*, 9th ed., W. W. Norton, 2014. Marginal, average, fixed, and variable cost foundations.
3. Richard A. Brealey, Stewart C. Myers, Franklin Allen, and Alex Edmans, *Principles of Corporate Finance*, 14th ed., McGraw Hill, 2023. Present value, opportunity cost, and investment comparison.
4. Robert S. Kaplan and Robin Cooper, *Cost & Effect: Using Integrated Cost Systems to Drive Profitability and Performance*, Harvard Business School Press, 1998. Activity-based cost and managerial decision use.
5. Barry W. Boehm, *Software Engineering Economics*, Prentice-Hall, 1981. Lifecycle software cost estimation and economic decision framing.
6. Raj Jain, *The Art of Computer Systems Performance Analysis*, Wiley, 1991. Workload, measurement, experimental design, and performance/cost reasoning.
7. Betsy Beyer, Chris Jones, Jennifer Petoff, and Niall Richard Murphy, eds., *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly, 2016, especially “Embracing Risk” and capacity-planning discussions, https://sre.google/sre-book/table-of-contents/ (retrieved 2026-09-06).
8. FinOps Foundation, “FinOps Framework” and “Unit Economics” capability, current framework, https://www.finops.org/framework/ and https://www.finops.org/framework/capabilities/unit-economics/ (retrieved 2026-09-06).
9. ISO/IEC 25010:2023, *Systems and software engineering—Systems and software Quality Requirements and Evaluation (SQuaRE)—Product quality model*, 2nd ed., November 2023, https://www.iso.org/standard/78176.html (retrieved 2026-09-06).
10. Ron Ross, Mark Winstead, and Michael McEvilley, *Engineering Trustworthy Secure Systems*, NIST SP 800-160 Vol. 1 Rev. 1, November 2022, https://doi.org/10.6028/NIST.SP.800-160v1r1 (retrieved 2026-09-06).

## Exercises

### Exercise 1

Define fixed, variable, step, average, marginal, opportunity, and sunk cost. For each, state why the classification requires a horizon or relevant range.

### Exercise 2

A service has monthly fixed cost \$75,000, variable cost \$0.006 per attempt, 15 million attempts, and 13.5 million good outcomes. Compute total cost, cost per attempt, cost per good outcome, and marginal cost per additional attempt away from a threshold. Explain the difference.

### Exercise 3

A product dashboard allocates every shared platform dollar by team headcount and reports that Team X “causes” 40% of platform cost. Diagnose the claim and design evidence suitable for both stewardship and an incremental architecture decision.

### Exercise 4

Compare a dedicated regional data service, a shared internal platform, and a managed external service. Construct a decision matrix that includes direct rates, capacity steps, people, data movement, quality, security, commitments, migration, and exit. State when each could be rational.

### Exercise 5

A public emergency-dispatch system proposes consolidating independent regional failover capacity because cost per dispatched incident is lower at high utilization. Produce a model and recommendation that respects uncertain disasters, safety, accessibility, jurisdiction, cyberattack, and recovery authority.

## Answers to the Exercises

### Answer 1

A fixed cost is unchanged within a declared activity range and period; a variable cost changes with activity; a step cost is fixed within a band and jumps at a threshold. Average cost is selected total cost divided by selected units. Marginal cost is the forward cost of an additional unit or increment. Opportunity cost is the best forgone alternative's value. Sunk cost is irrecoverable under all current alternatives.

Time and range matter because behavior changes. Staff may be fixed next month but avoidable after a year; a five-node cluster is fixed until demand needs a sixth; a commitment is sunk after purchase but avoidable before signing. Average and marginal cost also depend on which costs, units, and capacity changes the decision permits. A strong answer names these conditions rather than assigning permanent labels.

### Answer 2

Variable cost is $\$0.006\times15{,}000{,}000=\$90{,}000$. Total cost is $\$75{,}000+\$90{,}000=\$165{,}000$. Cost per attempt is $\$165{,}000/15{,}000{,}000=\$0.011$. Cost per good outcome is $\$165{,}000/13{,}500{,}000\approx\$0.012222$. Away from a threshold, one more attempt adds \$0.006 under the stated linear model.

Average attempt cost includes \$0.005 of fixed cost per current attempt, whereas local marginal cost does not repeat the fixed amount. Outcome cost is higher because only 90% of attempts meet the goodput definition. Accept equivalent exact fractions and careful rounding; reject an answer that calls \$0.011 the marginal cost without introducing a capacity change.

### Answer 3

The dashboard demonstrates a governed allocation that reconciles shared cost if headcount records and the 40% arithmetic are correct. It does not show causal resource demand, avoidability, or Team X's control. Headcount may be selected for simplicity or ability to pay, but platform cost may instead be driven by storage, requests, high-cost operations, tenant isolation, reserve, support, or a fixed minimum.

For stewardship, reconcile the entire invoice into direct, allocated, and explicitly unallocated amounts; document the headcount rule, owner, version, and limitations. For an incremental decision, measure Team X workload by class, trace resource and operational demand, identify spare capacity and thresholds, and estimate the counterfactual with and without the proposed change. Preserve fixed shared cost separately. A good diagnosis distinguishes policy fairness from causal inference and names uncertainty.

### Answer 4

A suitable matrix has rows for required latency, availability, durability, residency, security evidence, isolation, peak and failure capacity, direct consumption, step thresholds, commitments, licenses, data movement, observability, on-call and specialist work, integration, migration, parallel operation, retirement, and exit. Each cell records mechanism, cost range, evidence, owner, and uncertainty—not just a score.

Dedicated regional service can be rational for strict isolation, locality, predictable heavy demand, or independent recovery, despite duplicated reserve and skills. A shared internal platform can be rational when workloads pool well, common mechanisms are mature, allocation is governable, and common-cause risk is acceptable. A managed service can be rational when its capabilities and evidence replace substantial internal work and its rates, responsibilities, data paths, and exit are acceptable. There is no universal winner; compare equivalent required outcomes and run demand, rate, failure, and migration scenarios.

### Answer 5

Define the cost object as a successful, timely, accessible, correctly routed incident response—not a raw request. Model ordinary, surge, regional-disaster, communications-loss, malicious-load, supplier-loss, and control-plane-compromise scenarios. Trace call and data paths, responder jurisdiction, language and accessibility services, location privacy, priority, latency, queueing, regional capacity, common dependencies, failover coverage, repair authority, and drills. Reconcile steady-state cost while labeling independent reserve as serving disaster and recovery requirements.

The recommendation should reject consolidation based solely on average utilization. Compare at least regional independence, pooled service with physically and administratively independent reserves, and hybrid routing. Use ranges for correlated demand and failure where probabilities are not defensible. Set non-negotiable safety, legal, accessibility, privacy, and cybersecurity constraints through accountable authorities; quantify compliant alternatives; pilot only reversible traffic; and require overload, partition, compromised-control, and recovery exercises. Approve consolidation only if evidence shows required outcomes and independence remain satisfied across the governed scenarios. This is an architecture recommendation, not emergency-service, safety, legal, privacy, accessibility, or security certification.
