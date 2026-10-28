---
module_id: SDRE-041
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 41
title: Reliability, Availability, and Durability
status: complete
last_verified: 2026-09-06
---

# Reliability, Availability, and Durability

## One-Page Review

### Governing question

How can engineers specify and measure whether a service continues to behave correctly, is usable when needed, and preserves acknowledged state—without collapsing three different properties into “uptime” or “nines”?

### Essential definitions

- **service contract** defines the operation, eligible population, acceptable outcome, latency, consistency, and data obligations;
- **failure** is an externally observable deviation from that contract;
- **fault** is an adjudged or hypothesized cause of an error; an **error** is internal state liable to cause failure;
- **reliability** is the probability of failure-free service over a stated interval under stated conditions;
- **availability** is the probability or observed proportion that service is usable when required, under a declared demand model;
- **durability** is the probability that acknowledged state remains retrievable with required integrity over a stated horizon and failure model;
- **integrity** means the required correctness and consistency of state; corrupt but present bytes are not durable useful state;
- **mission time** is the interval over which failure-free behavior is required;
- **repair time** is time from failure under the measurement policy to restored acceptable service;
- **acknowledgment point** is the event after which the system claims an operation or state is committed;
- **failure domain** is a set of components susceptible to a common cause;
- **redundancy** provides alternatives; **diversity** reduces shared mechanisms; neither alone proves independence;
- a **recovery objective** bounds acceptable loss or restoration time; it is not evidence that recovery works.

### Central model, mechanism, or theorem

Let $T$ be time to service failure under a declared environment. Reliability over mission time $t$ is

$$
R(t)=P(T>t).
$$

For an alternating repairable process with finite mean uptime $U$ and downtime $D$, steady-state time availability is

$$
A=\frac{U}{U+D}.
$$

For acknowledged objects $O$ and a horizon $h$, empirical durability can be measured as the fraction that remain retrievable and correct at $h$, but the estimate is meaningful only with defined object identity, acknowledgment, correctness checks, censoring, and failure coverage.

### Critical invariants

- define the user-visible contract before classifying a failure;
- name the population, interval, demand model, and measurement boundary for every rate;
- separate time availability, request success, partial availability, and latency compliance;
- reliability concerns uninterrupted correct service; repair can restore availability after reliability has failed;
- durability begins at a declared acknowledgment and includes integrity, not mere replica presence;
- retries can improve apparent request success while hiding unreliable attempts;
- redundancy claims require failure-domain and common-cause analysis;
- scheduled maintenance is included or excluded only by explicit policy;
- “nines” apply to one exact indicator and window, not an entire architecture;
- tests, restoration exercises, checksums, and monitoring provide bounded evidence, not guaranteed future correctness.

### Common failures

Common failures are equating availability with process uptime, using an unweighted average of regional percentages, counting retried success while omitting failed attempts and latency, calling a replica durable without checking correlated deletion, treating a backup catalog as restore evidence, assuming independent failures because machines differ, multiplying component availabilities without path semantics, excluding maintenance after observing it, claiming annual durability from a short quiet sample, accepting writes before their promised persistence boundary, and using mean repair time while hiding a long-tailed recovery distribution.

### Compact example

A document service defines successful write as an authenticated request acknowledged only after a recoverable record reaches two independent failure domains. Availability counts eligible writes completed within 500 ms; reliability for a ten-minute editing mission is the probability of no contract failure; durability asks whether each acknowledged revision remains correct and retrievable after one year under named failures. Client retries are recorded separately. A regional outage may break mission reliability, while failover restores availability. Replica counts, checksums, restore exercises, deletion propagation, and out-of-band inventories supply different pieces of durability evidence.

### Connections

[SDRE-040](040-instrumenting-a-service-for-diagnosis.md) supplies measurement evidence. [SDRE-042](../ROADMAP.md) through [SDRE-045](../ROADMAP.md) next formalize indicators, objectives, agreements, and error budgets; [SDRE-047](../ROADMAP.md) and [SDRE-048](../ROADMAP.md) develop failure domains and redundancy.

## Governing Question

“Reliable,” “available,” and “durable” are often used as synonyms for “probably works.” That ambiguity becomes dangerous at an acknowledgment boundary. A service can be available for new writes while losing previously acknowledged data. It can be durable but unavailable during a long restoration. It can be highly available across a month yet fail every ten-minute mission at least once.

Each property needs an event, population, interval, environment, and evidence. Reliability asks whether a failure occurs during a mission. Availability asks whether acceptable service is obtainable when demanded. Durability asks whether acknowledged state survives and remains correct over time and failures.

The governing question is therefore a specification problem before it is arithmetic: what promise is made, from whose boundary, for which work or state, across which time and faults, and which observations could honestly support or contradict it?

## Why This Matters

The dependability taxonomy associated with IFIP WG 10.4 distinguishes faults, errors, failures, and attributes such as reliability and availability [1]. ISO/IEC 25010:2023 provides a current product-quality model for specifying and evaluating ICT product properties [2]. These vocabularies guide questions; neither substitutes for a service-specific contract.

Google SRE frames reliability as an explicit trade-off rather than an unbounded maximum and derives time- and request-based availability from user-visible outcomes [3, 4]. Its SLO guidance describes availability as service usability and durability as retained data over a long period [5]. The data-integrity chapter emphasizes that intact but inaccessible data and available but corrupted data create distinct user harm [6].

Current PostgreSQL documentation illustrates how an acknowledged commit's durability depends on write-ahead logging, storage behavior, configuration, and failure assumptions [7]. Its synchronous replication documentation explicitly trades additional acknowledgment latency for stronger placement of commit records [8]. These are mechanism examples, not universal storage guarantees.

## Prerequisites and Retrieval

Retrieve service, operation, outcome, latency, request, mission, probability, conditional probability, random variable, expectation, distribution, fault, error, failure, repair, retry, timeout, replica, quorum, integrity, checksum, commit, persistence, recovery, backup, failure domain, common cause, censoring, and confidence interval.

From SDRE-031 retrieve symptom and mechanism. From SDRE-033 retrieve valid populations and aggregation. From SDRE-038 retrieve actionability and missing evidence. From SDRE-040 retrieve measurement points, operation boundaries, attempts, logical outcomes, and evidence health.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish fault, error, failure, reliability, availability, durability, and integrity;
2. write a service contract with an explicit observation boundary;
3. compute time- and request-based availability without mixing populations;
4. derive steady-state availability under an alternating uptime/repair model;
5. reason about mission reliability and constant-hazard assumptions;
6. define durability from acknowledgment through verified retrieval;
7. expose retry, partial-service, maintenance, and censoring effects;
8. evaluate redundancy under independent and common-cause failures;
9. select tests and operational evidence appropriate to each property;
10. reject “nines” claims whose indicator, window, and failure model are unspecified.

## Core Exposition

**Define acceptable service first.** A response is not successful merely because a process answered. Define eligible demand, outcome semantics, deadline, consistency, authorization, and state effects. An HTTP success carrying incorrect data is a failure. A correct response after the user's deadline can be unavailable for that operation. A durable write that cannot be read within the recovery contract is not currently available.

State whose observation governs. Client, load balancer, server, database, and operator see different populations. A request that never reaches the server is absent from server logs but still failed for the client. Use black-box and white-box evidence while keeping the user boundary primary.

**Separate impairment levels.** A fault is a hypothesized or adjudged cause: a software defect, bit flip, operator action, or partition. It may create an erroneous internal state. A failure occurs when delivered service deviates from the contract [1]. Not every fault activates, not every internal error escapes, and the observed symptom does not identify its root cause.

This chain matters for evidence. Fault injection shows behavior under a selected cause; it does not enumerate all faults. Error detection can trigger correction before failure. A failure counter measures contract deviations, not latent defects.

**Specify reliability as a mission property.** Let $T$ be time from an agreed initial state to the first contract failure. Then $R(t)=P(T>t)$ under stated load, environment, version, dependencies, and maintenance policy. Reliability is about uninterrupted acceptable service through the mission.

If lifetime is modeled as exponential with constant hazard $\lambda$, then $R(t)=e^{-\lambda t}$ and mean time to failure is $1/\lambda$. This model is convenient, not a default law. Software changes, correlated incidents, aging hardware, diurnal load, and repair policies violate constant hazard or identical trials. Show empirical survival or interval-specific failure rates when the exponential premises do not hold.

Reliability and availability can diverge. A service that fails hourly and repairs in one second may have high time availability but poor one-day mission reliability. A nonrepairable device can be reliable for a short mission while having no repair-based availability after failure.

**Define availability from demand.** Time availability over observation interval $W$ is acceptable-service time divided by eligible time. Request availability is acceptable operations divided by eligible operations. The two differ when demand varies: a five-minute outage at peak may affect more users than an hour overnight.

For alternating uptime and repair cycles with finite stable means $U$ and $D$, renewal reasoning gives long-run time fraction $A=U/(U+D)$. Often this is written $MTTF/(MTTF+MTTR)$. The expression assumes a clear two-state boundary, stationary cycles, and an observation process that captures them. It does not apply automatically to degraded multi-region services.

Partial availability needs population weighting. If region $i$ has $s_i$ successful and $n_i$ eligible operations, aggregate availability is $\sum_i s_i/\sum_i n_i$, not the unweighted mean of regional ratios unless equal-region weighting is the intended user model.

The executable model shows the distinction with controlled intervals and request counts.

<!-- bijux-verify: {"id":"reliability-availability-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"time availability: 97.22%\nrequest availability: 93.33%\nmission reliability: 50.00%\nsteady-state model: 97.22%\n","stderr":""}} -->
```python
uptimes = [100, 200, 50]
downtimes = [2, 8, 0]
successful_requests = 1400
eligible_requests = 1500
successful_missions = 3
eligible_missions = 6

time_availability = sum(uptimes) / (sum(uptimes) + sum(downtimes))
request_availability = successful_requests / eligible_requests
mission_reliability = successful_missions / eligible_missions
mean_uptime = sum(uptimes) / len(uptimes)
mean_downtime = sum(downtimes) / len(downtimes)
steady_state = mean_uptime / (mean_uptime + mean_downtime)

print(f"time availability: {time_availability:.2%}")
print(f"request availability: {request_availability:.2%}")
print(f"mission reliability: {mission_reliability:.2%}")
print(f"steady-state model: {steady_state:.2%}")
```

The equal number of uptime and downtime observations makes the ratio of means equal the ratio of sums. This controlled equality can fail with mismatched or censored cycles. The three observed percentages answer different questions.

**Make window and policy visible.** A monthly 99.9% indicator does not imply every day or user received 99.9%. “Planned downtime excluded” changes the eligible interval and can incentivize reclassification. Declare maintenance, dependency, client, abuse, invalid-request, and force-majeure handling before observing results.

One additional nine reduces the allowed failure fraction by a factor of ten. It does not make architectures comparable when their indicators differ. Google SRE's availability table is arithmetic under its stated no-planned-downtime assumption, and its guidance prefers request aggregation when service is partially available or load varies [4].

**Account for retries.** Suppose an operation succeeds after two failed attempts. Logical request availability may count success, while attempt reliability exposes two dependency failures and user latency includes all attempts. Both are useful. Counting only final success can hide overload, retry amplification, and a shrinking safety margin.

Define cancellation and timeout. A client abandonment may be a failure even if the server eventually completes. Duplicate success can violate semantics. Use idempotency and attempt identifiers without merging the populations.

**Define durability at acknowledgment.** A durability promise begins when the system tells the caller that state is committed. Define the object or mutation, required integrity, retention horizon, deletion policy, failure model, placement, and retrieval test. “Eleven nines” without those fields is not reviewable.

Acknowledgment before durable media or required replicas narrows latency and weakens the surviving-failure set. A write-ahead log can order recovery if the log reaches storage with the promised semantics [7]. Synchronous replication can wait for remote receipt, write, flush, or apply depending on configuration, with distinct latency and loss implications [8]. Always state the exact acknowledgment boundary.

Durability is not availability. Three intact offline copies may preserve state while the service is unavailable. A fast empty response may be available at the protocol level yet violate integrity. Checksums detect some corruption but do not repair it, prove semantic correctness, or protect against authorized mistaken deletion.

**Measure durability by cohorts and horizons.** Let $O_t$ be objects acknowledged in cohort $t$. At horizon $h$, test whether each eligible object is retrievable and correct. Report lost, corrupt, unavailable, intentionally deleted, not-yet-observed, and censored separately. User deletion should not count as loss, but delayed deletion may violate a different contract.

Rare-loss estimates need large exposure and careful upper bounds. Observing zero losses in a small or short sample is not proof of perfect durability. Correlated events violate independent-object assumptions; a faulty migration can affect an entire cohort at once.

**Analyze redundancy through failure domains.** For two components independently available with probabilities $A_1$ and $A_2$, a service requiring both has $A=A_1A_2$ under the model. A parallel service that works when either works has $A=1-(1-A_1)(1-A_2)$ only if failures are independent, failover is correct and timely, dependencies are included, and either component alone satisfies the contract.

Real replicas share software, operators, credentials, power, networks, control planes, schemas, and deletion commands. Common causes dominate extreme tails. Diversity can reduce some shared faults but adds incompatibility and operational complexity. SDRE-047 and SDRE-048 develop this in depth.

**Connect prevention, tolerance, removal, and forecasting.** Prevent faults with review, types, testing, safe change, and access control. Tolerate activated faults with isolation, redundancy, retry, failover, and degradation. Remove faults with diagnosis, repair, rollback, and data correction. Forecast with models and evidence whose assumptions are visible [1].

No mechanism improves every property. Synchronous replication can improve durability under selected failures while increasing write latency and possibly reducing write availability. Aggressive failover can restore availability while risking split-brain writes. Caches improve read availability while serving stale data outside the consistency contract.

**Use multiple evidence types.** Monitoring estimates observed outcomes. Reliability tests exercise selected loads and faults. Model checking can prove properties of an abstract model. Fault injection tests chosen failures. Restore exercises demonstrate one recovery path in one environment. Checksums detect covered corruptions. Audits verify process and configuration. None proves universal future behavior.

Record exact versions, topology, workload, fault, duration, sample size, censoring, and result. Expand tests when an incident reveals a class not covered. Treat missing telemetry as missing evidence rather than successful service.

## Definitions and Notation

Let a service contract $C$ map eligible demand and state to acceptable outcomes. A failure occurs when delivered service violates $C$ at the observation boundary. Let $T$ be time to first failure; reliability is $R(t)=P(T>t)$.

For observed acceptable-service time $G$ and eligible time $W>0$, time availability is $A_t=G/W$. For successful eligible operations $S$ and total eligible operations $N>0$, request availability is $A_r=S/N$.

For an alternating renewal model, $U$ is mean uptime and $D$ mean repair downtime, both finite and nonnegative with $U+D>0$. Steady-state availability is $A=U/(U+D)$.

Let $O$ be a cohort of acknowledged objects, $L_h$ the objects lost or irreparably corrupt by horizon $h$, and $E_h$ those whose status is evaluable. Empirical cohort durability is $1-|L_h|/|E_h|$ when $|E_h|>0$, with censoring and unavailable-but-intact states reported separately.

## Mechanisms, Invariants, or Proof Structure

**Survival definition.** The event $T>t$ means no contract failure has occurred throughout the mission interval. It is stronger than being available at the endpoint $t$ because a repaired mid-interval failure violates uninterrupted service.

**Renewal fraction.** Over many stable cycles, total uptime is approximately $nU$ and total cycle time $n(U+D)$; their ratio tends to $U/(U+D)$. The derivation relies on representative complete cycles and a two-state measurement model.

**Weighted aggregation.** Regional success counts sum before division: $A=\sum s_i/\sum n_i$. An unweighted mean gives every region equal influence, a different estimand. Equality occurs only under special weights or equal denominators.

**Series and parallel arguments.** Under independence, both components being available has probability $A_1A_2$; at least one available is the complement of both unavailable, $1-(1-A_1)(1-A_2)$. Shared faults or failed switchover invalidate the independence/coverage premises.

**Acknowledgment invariant.** A state transition cannot satisfy a post-acknowledgment durability promise if the claimed surviving copies or log records have not crossed their promised persistence boundaries before acknowledgment.

**Integrity invariant.** Retrieval alone is insufficient: if returned state violates the correctness predicate, useful durability failed even though bytes exist. Verification must bind identity, version, and integrity.

## Alternatives and Trade-Offs

**Time versus request availability.** Time is intuitive for continuously demanded binary services. Request weighting better represents varying load and partial failure but depends on complete eligible-demand observation.

**Attempt versus logical-operation measures.** Attempt measures reveal mechanism instability. Logical outcomes represent user-visible success. Record both when retries or hedges exist.

**Repair speed versus failure prevention.** Faster repair raises availability without improving pre-failure reliability. Prevention lengthens missions but may cost delivery speed. Mature systems invest in both.

**Synchronous versus asynchronous acknowledgment.** Waiting for durable remote state strengthens selected durability guarantees and adds latency or reduces write availability during partitions. Earlier acknowledgment accepts a defined loss window.

**Replication versus backup.** Replication supports availability and rapid recovery but can copy corruption or deletion. Versioned, isolated backups can survive those causes but restore more slowly. Neither replaces tested recovery.

**Homogeneous versus diverse redundancy.** Homogeneous copies are simpler and share defects. Diverse implementations reduce some common modes while adding disagreement and maintenance risk.

**Failover versus consistency.** Fast failover may preserve access and risk conflicting writes. Conservative coordination protects consistency and can reject work. The service contract chooses the trade.

**Aggregate versus cohort durability.** Aggregate ratios summarize exposure; cohort views reveal release, media, migration, or age effects. Both need explicit censoring.

**Mean versus distribution.** Mean repair time supports a simple model and hides long tails. Quantiles and worst credible cases better inform user and incident expectations, with adequate samples.

## Failure Modes and Misconceptions

1. **“Reliability is uptime.”** Uptime omits correctness, demand, latency, and mission continuity.
2. **“Availability and reliability are identical.”** Repair can restore availability after mission reliability has failed.
3. **“Durability means the disk accepted a write.”** The promise depends on acknowledgment, media semantics, failure domains, integrity, and horizon.
4. **“Present bytes are correct data.”** Corruption can preserve presence while violating integrity.
5. **“A replica is a backup.”** Online replicas often share deletion and corruption paths.
6. **“Two replicas square the loss probability.”** Only an adequate independent-failure model permits that multiplication.
7. **“Failover is instantaneous and perfect.”** Detection, decision, routing, warm-up, and state convergence can all fail.
8. **“Retries improve reliability.”** They may improve logical success while increasing attempts, load, and latency.
9. **“Monthly nines apply to every user.”** Aggregates can hide concentrated harm.
10. **“Planned maintenance never counts.”** Inclusion is a contract policy, not an after-the-fact excuse.
11. **“Zero observed loss proves perfect durability.”** Exposure, censoring, detection coverage, and correlation constrain the evidence.
12. **“MTTR is one universal interval.”** Detection, acknowledgment, mitigation, restoration, and verification boundaries differ.
13. **“Checksums prevent corruption.”** They detect covered changes; repair and independent truth are separate.
14. **“Backups prove recovery.”** Only validated restoration demonstrates a bounded recovery path.
15. **“Component nines multiply into service nines.”** Path semantics, dependencies, common causes, and degraded states matter.
16. **“A stronger guarantee is always better.”** Reliability competes with latency, availability, velocity, complexity, and cost [3].

## Worked Examples

### Example 1

**Separate three properties.** A store rejects writes for ten minutes but preserves every acknowledged object. Write availability fails; durability does not. After service returns, a one-hour upload mission that crossed the outage was not failure-free. **Conclusion:** availability, mission reliability, and durability need separate events.

### Example 2

**Compute time availability.** Controlled cycles contain 350 minutes up and 10 down. Availability is $350/360=97.22\%$. This result does not describe how many requests failed or whether recovered data was correct. **Conclusion:** the denominator defines the claim.

### Example 3

**Compare demand weighting.** Region A succeeds on 990 of 1,000 requests; region B succeeds on 1 of 10. Aggregate request availability is $991/1{,}010=98.12\%$. The equal-region mean is $(99\%+10\%)/2=54.5\%$. **Conclusion:** both calculations are valid for different populations; label the estimand.

### Example 4

**Relate repair and availability.** Mean uptime is 720 hours and mean repair downtime 2 hours. Under the alternating stationary model, $A=720/(720+2)=99.723\%$. Halving repair to one hour gives $99.861\%$ but does not change the modeled time to first failure. **Conclusion:** repair improves availability, not mission reliability before failure.

### Example 5

**Use a constant-hazard model carefully.** With $\lambda=0.001$ failures/hour, exponential mission reliability for 100 hours is $e^{-0.1}=90.48\%$. A release changing hazard after hour 20 violates the constant-rate premise. **Conclusion:** an equation is only as valid as its environment assumptions.

### Example 6

**Expose retry evidence.** One logical request makes three attempts: timeout, timeout, success, completing after 1.4 seconds against a 1-second deadline. Final-status-only counting says success; the user contract says failure, and attempt evidence shows instability. **Conclusion:** logical, attempt, and deadline outcomes must coexist.

### Example 7

**Evaluate serial components.** Two independently available required services have $A_1=0.999$ and $A_2=0.99$. Modeled joint availability is $0.999\times0.99=98.901\%$. A shared identity provider adds another dependency and breaks this two-component model. **Conclusion:** architecture semantics precede multiplication.

### Example 8

**Evaluate ideal parallel redundancy.** Two independently failing replicas each have availability 0.99. If either alone is sufficient and failover is perfect, $A=1-(0.01)^2=99.99\%$. Shared power or a faulty release creates common cause and lowers real availability. **Conclusion:** the formula is conditional, not a replication guarantee.

### Example 9

**Define a durability cohort.** Of 1,000 acknowledged objects due for one-year verification, 980 are verified correct, 2 are irreparably corrupt, 8 are temporarily unavailable, and 10 were intentionally deleted under policy. If deleted objects are ineligible and unavailable status is reported separately, evaluable objects are 982 and empirical integrity-preserving durability is $980/982=99.796\%$. **Conclusion:** classification and censoring must accompany the ratio.

### Example 10

**Compare acknowledgment policies.** Policy A acknowledges after local memory; a host crash can lose acknowledged writes. Policy B acknowledges after local durable log and remote durable receipt; it survives either single host loss under placement assumptions but adds network and flush latency and may reject writes during partition. **Conclusion:** durability strength, latency, and write availability trade at the acknowledgment point.

## Cross-Program Connections

1. [DIST-001](../../27-distributed-systems-engineering/ROADMAP.md) connects failure models, partitions, replication, and consensus.
2. [DBE-001](../../18-database-engineering/ROADMAP.md) connects commit, WAL, integrity, and recovery to database mechanisms.
3. [DARCH-001](../../20-data-architecture-engineering/ROADMAP.md) connects retention, ownership, and recovery contracts to data architecture.
4. [LSDS-001](../../21-large-scale-data-systems-engineering/ROADMAP.md) connects correlated failure and distributed storage to scale.
5. [SYSENG-001](../../26-systems-engineering/ROADMAP.md) connects reliability models, hazards, feedback, and lifecycle evidence.
6. [SARCH-001](../../12-software-engineering-software-architecture/ROADMAP.md) connects service paths and failure domains to architectural structure.
7. [STQE-001](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) connects fault injection and recovery tests to evidence quality.
8. [OS-001](../../22-operating-systems/ROADMAP.md) connects process, storage, clocks, and crash behavior to mechanisms.
9. [CLOUD-001](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) connects regional placement, managed guarantees, and capacity to infrastructure.
10. [SEC-001](../../25-security-engineering/ROADMAP.md) connects integrity, availability attacks, deletion authority, and audit evidence.

## References

1. Avizienis, A., Laprie, J.-C., Randell, B., and Landwehr, C. “Basic Concepts and Taxonomy of Dependable and Secure Computing.” *IEEE Transactions on Dependable and Secure Computing* 1(1), 2004; IFIP WG 10.4 publication index. <https://www.dependability.org/wg10.4/publications.html>. Retrieved 2026-09-06.
2. ISO/IEC. *ISO/IEC 25010:2023 Systems and Software Engineering—SQuaRE—Product Quality Model*. Second edition, November 2023. <https://www.iso.org/standard/78176.html>. Retrieved 2026-09-06.
3. Alvidrez, M. “Embracing Risk.” *Site Reliability Engineering*. O'Reilly/Google, 2016. <https://sre.google/sre-book/embracing-risk/>. Retrieved 2026-09-06.
4. Google. “Availability Table.” *Site Reliability Engineering*. <https://sre.google/sre-book/availability-table/>. Retrieved 2026-09-06.
5. Beyer, B., Jones, C., Petoff, J., and Murphy, N. R., eds. “Service Level Objectives.” *Site Reliability Engineering*. O'Reilly/Google, 2016. <https://sre.google/sre-book/service-level-objectives/>. Retrieved 2026-09-06.
6. Blum, R., and Singh, R. “Data Integrity: What You Read Is What You Wrote.” *Site Reliability Engineering*. O'Reilly/Google, 2016. <https://sre.google/sre-book/data-integrity/>. Retrieved 2026-09-06.
7. PostgreSQL Global Development Group. “Reliability.” PostgreSQL 18 documentation. <https://www.postgresql.org/docs/current/wal-reliability.html>. Retrieved 2026-09-06.
8. PostgreSQL Global Development Group. “Log-Shipping Standby Servers—Synchronous Replication.” PostgreSQL 18 documentation. <https://www.postgresql.org/docs/current/warm-standby.html>. Retrieved 2026-09-06.

## Exercises

### Exercise 1

Define fault, error, failure, reliability, availability, durability, integrity, mission time, acknowledgment point, and failure domain. Give one sentence distinguishing each of the three central properties.

### Exercise 2

A service experiences complete cycles of 600, 900, and 300 minutes up followed by 5, 15, and 10 minutes down. Compute observed time availability and the ratio-of-means steady-state estimate. Explain why the equality holds here.

### Exercise 3

Region A serves 9,900 of 10,000 eligible requests successfully; region B serves 450 of 500; region C serves 0 of 20. Compute aggregate request availability and equal-region mean. Diagnose what each reveals and hides.

### Exercise 4

Write separate reliability, availability, and durability contracts for a collaborative note service. Include mission, operation, deadline, acknowledgment, horizon, integrity, failures, retries, deletion, and recovery evidence.

### Exercise 5

Transfer the model to an implanted medical-device monitoring service that receives readings, raises urgent notifications, and stores clinical history. Explain how safety changes the contracts, evidence, and acceptable trade-offs without claiming certification.

## Answers to the Exercises

### Answer 1

A fault is a hypothesized or adjudged cause; an error is internal state liable to cause failure; a failure is externally observed service deviation. Reliability is probability of failure-free service over a stated mission. Availability is probability or proportion of acceptable service when demanded. Durability is probability acknowledged state remains retrievable and correct over a horizon and failure model. Integrity is required state correctness and consistency. Mission time is the uninterrupted interval of interest. The acknowledgment point begins the system's commitment claim. A failure domain groups components sharing a cause. Reliability asks “no failure throughout?”, availability “usable now or on demand?”, and durability “is acknowledged state still correct and retrievable?”

### Answer 2

Total uptime is $600+900+300=1{,}800$ minutes and downtime $5+15+10=30$. Observed availability is $1{,}800/1{,}830=98.3607\%$. Mean uptime is 600 and mean downtime 10, so $600/(600+10)=98.3607\%$. Equality holds because uptime and downtime lists contain the same three complete paired cycles; dividing both totals by three leaves the ratio unchanged. It need not hold with incomplete, length-biased, or mismatched observations.

### Answer 3

Aggregate successes are $9{,}900+450+0=10{,}350$ of $10{,}520$, so request availability is $98.384\%$. Regional rates are 99%, 90%, and 0%; equal-region mean is 63%. The aggregate represents a randomly selected eligible request and is dominated by region A. The equal-region mean gives tiny region C equal weight and exposes broad geographic inequality but not affected-request share. Report counts and both views; investigate why C has only 20 requests rather than declaring either percentage universally correct.

### Answer 4

Reliability: from a synchronized note open, a 30-minute editing mission must accept, order, and display authorized edits without contract failure under stated client, region, and dependency conditions; retries and reconnections remain visible. Availability: eligible read and edit operations must complete with correct authorized state within declared client-visible deadlines, partitioned by region and cohort, with maintenance policy fixed in advance. Durability: after the service acknowledges an edit, that version must remain retrievable and semantically correct for the retention horizon despite named single-domain failures; authorized deletion ends eligibility and must itself meet a deletion contract. Define acknowledgment after the promised log/replica boundary, checksums plus semantic validation, independent backups, cohort audits, restore exercises, and unavailable/censored classifications. Acceptable variants must keep the three populations and boundaries separate.

### Answer 5

Reliability covers uninterrupted correct acquisition and evaluation over a clinically defined monitoring mission. Availability covers timely access and urgent notification delivery to authorized roles when demanded. Durability covers acknowledged readings, alert decisions, and clinically required history remaining correct and retrievable for the governed horizon. Safety requires hazard analysis: false negatives, false positives, stale readings, clock errors, patient/device mismatch, communication loss, and delayed escalation have different consequences. Use independent local alarms where cloud loss is unsafe, explicit unknown states, conservative bounded degradation, trained escalation, integrity and identity checks, redundant failure domains, controlled updates, restore exercises, and human factors evidence. Latency, battery, privacy, and alarm fatigue remain trade-offs. This design answer is not certification, clinical validation, or proof of safety.
