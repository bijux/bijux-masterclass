---
module_id: DARCH-040
program: Data Architecture Engineering
level: 1
module_number: 40
title: Choosing an Integration Style from Semantics and Latency
status: complete
last_verified: 2026-09-03
---

# Choosing an Integration Style from Semantics and Latency

## One-Page Review

### Governing question

How should architects select and combine direct links, APIs, events, CDC, batches, replication, federation, and mediated integration from the meaning and timing of a consumer need, rather than from fashion, existing tools, or a single latency target?

### Essential definitions

- An **integration style** is a recurring allocation of interaction, movement, storage, time, failure, and ownership responsibilities across producer, intermediary, and consumer boundaries.
- **semantic fit** is how well a style preserves the authority, grain, identity, time, meaning, quality, correction, and consumer use of the required assertions.
- **latency** is elapsed time between two declared boundaries; **freshness** is age of the underlying source observation or business-effective state at use.
- A **command** asks an accountable recipient to act; a **query** requests a representation; an **event** records an occurrence; a **snapshot** represents a population at a boundary; a **change record** represents a source mutation.
- **temporal coupling** requires participants or states to be available within the same interaction window.
- **materialization** stores a representation for later use; **virtualization** computes across sources at access time.
- A **consistency requirement** states which observations or orderings must agree for a particular operation and failure scenario.
- A **selection constraint** makes an option unacceptable, such as a residency prohibition, unsupported recovery objective, or required transaction invariant.
- A **decision criterion** differentiates feasible options, such as change autonomy, consumer fan-out, end-to-end freshness, or lifecycle cost.
- A **trade study** compares feasible alternatives under shared scenarios, evidence, uncertainty, assumptions, and accountable decision rights.
- A **hybrid integration** deliberately combines styles while defining cross-style identity, authority, time, failure, protection, correction, and lifecycle.
- An **evolution trigger** is evidence that requires the decision to be revisited, such as workload growth, incidents, new consumers, changed regulation, or unacceptable latency.

### Central model, mechanism, or theorem

Represent a decision as:

`D = (need, assertions, interaction, time, population, workload, consistency, failure, protection, ownership, lifecycle, constraints, criteria, evidence, alternatives)`

First eliminate styles that cannot meet hard semantic, protection, or failure constraints. Then compare feasible styles across scenarios using evidence and explicit uncertainty. Latency is never one number: source-to-publication, queue, transfer, processing, cache, query, and decision delay contribute differently. A weighted matrix can expose assumptions, but its scores do not prove the winner; sensitivity, adversarial scenarios, prototypes, and accountable judgment remain necessary.

### Critical invariants

- Selection starts from a consumer decision or workflow and the exact assertions, commands, populations, and history it requires.
- Every latency, freshness, consistency, delivery, durability, and availability claim names its start, end, population, percentile or bound, workload, and failure context.
- Hard constraints are separated from preferences so a high aggregate score cannot compensate for an impermissible or incorrect design.
- Options are compared under equivalent semantics, protection, service, consumer outcomes, time horizon, and lifecycle scope.
- Producer authority and consumer fitness remain explicit regardless of whether data is requested, pushed, copied, materialized, or queried virtually.
- Failure analysis covers partial success, duplication, gaps, ordering, stale state, overload, retry, replay, source loss, intermediary loss, and consumer recovery.
- Protection analysis follows identities, payloads, metadata, intermediates, caches, copies, histories, regions, providers, retention, deletion, and audit.
- Cost includes build, run, source load, consumer work, change, incident, assurance, migration, coexistence, opportunity, and retirement.
- Hybrid designs state cross-style races, precedence, synchronization, correction, and which path is authoritative for each use.
- The decision records evidence, uncertainties, rejected alternatives, responsible approvers, review triggers, and exit or migration seams.

### Common failures

Common failures are choosing events because “real time” sounds desirable; choosing batch because the source already exports files; using API response time as data freshness; treating CDC rows as domain events; selecting federation to avoid acknowledging runtime dependency; selecting replication as backup; ranking options before eliminating policy violations; adding scores with arbitrary precision; comparing a mature incumbent to an untested ideal; measuring only happy-path latency; ignoring consumer processing and correction; forcing one style on all consumers; combining API and events without defining races; and recording no review trigger, migration seam, or retirement cost.

### Compact example

A fraud decision needs an authoritative payment-accepted fact within two seconds, can tolerate duplicate notification, must preserve per-payment order, and needs recovery after a six-hour outage. A governed event product satisfies the primary path; consumers implement idempotent effects and replay. An API provides authorized current detail after a version tied to the event. Daily snapshots serve model training. CDC remains internal to source publication. The architecture uses three styles because their semantic and temporal responsibilities differ, not because one technology won a universal score.

### Connections

[DARCH-031](031-point-to-point-integration-and-its-costs.md) through [DARCH-039](039-replication-and-synchronization.md) define the major integration styles and their liabilities. [DARCH-018](018-temporal-and-historical-modeling.md), [DARCH-027](027-producer-and-consumer-contracts.md), and [DARCH-028](028-cross-domain-dependencies.md) provide temporal, contractual, and systemic foundations. This module closes the Integration and Movement Architecture block and prepares [DARCH-041](../ROADMAP.md) on enterprise data warehouse architecture.

## Governing Question

Organizations often choose integration from whichever platform they have already purchased. Requirements are then rewritten as “API,” “event,” or “real-time” requirements, even when consumers need a coherent daily population, a domain command, a physical replication stream, or a cross-source analytical result.

The governing question is not which style is best. It is which allocation of interaction, time, state, failure, protection, and ownership best preserves the required meaning and consumer outcome across the full lifecycle.

## Why This Matters

Integration decisions harden into contracts, copies, operational dependencies, and team responsibilities. A low-latency prototype can create long-lived replay and privacy burdens. A simple batch can become a critical overnight dependency. A virtual query can move more data and create more source load than a materialized product.

Gregor Hohpe and Bobby Woolf's [Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/patterns/messaging/) supplies vocabulary for message channels, routing, transformation, endpoints, and operations. The [OpenAPI Specification 3.1.1](https://spec.openapis.org/oas/v3.1.1.html) and [AsyncAPI Specification 3.0.0](https://www.asyncapi.com/docs/reference/specification/v3.0.0) describe HTTP and message-driven interfaces. Pattern and interface descriptions support decisions; they do not make them.

[CloudEvents 1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md) standardizes common event context. PostgreSQL's [Logical Decoding Concepts](https://www.postgresql.org/docs/current/logicaldecoding-explanation.html) illustrates source-log capture mechanisms. The W3C [SPARQL 1.1 Federated Query](https://www.w3.org/TR/sparql11-federated-query/) recommendation illustrates query delegation to remote services. These mechanisms expose different facts and failure boundaries.

Google's [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) explains overload propagation and retry amplification. NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) frames trustworthy secure-system engineering across lifecycles. Selection must include both ordinary performance and exceptional system behavior.

## Prerequisites and Retrieval

You should understand point-to-point, hub-and-spoke, ESB, APIs, events, CDC, batch, federation, replication, data products, semantics, time, consistency, distributed failure, protection, service objectives, cost, trade studies, and lifecycle.

Retrieve command, query, event, change record, snapshot, authority, grain, population, latency, freshness, staleness, consistency, temporal coupling, fan-out, volume, interaction, materialization, virtualization, constraint, criterion, scenario, evidence, uncertainty, weight, score, sensitivity, prototype, hybrid, seam, and review trigger.

As a retrieval test, inspect “We need customer data in real time.” Ask which assertions and source, consumer decision, key and grain, business and observation time, maximum useful age, population, interaction, update rate, read rate, history, consistency, failure behavior, protection, cost, and consequence apply. “Real time” is not a selectable requirement.

## Learning Objectives

After completing this module, you should be able to:

1. translate vague integration requests into precise semantic, temporal, workload, consistency, protection, and lifecycle requirements;
2. distinguish commands, queries, events, change records, snapshots, replicated state, and virtual results;
3. decompose end-to-end latency and freshness across source, publication, transfer, queue, processing, cache, access, and decision boundaries;
4. identify hard constraints before scoring preferences and reject infeasible styles transparently;
5. compare direct, mediated, API, event, CDC, batch, replication, federation, and materialized products under shared scenarios;
6. model partial failure, retry, idempotency, ordering, replay, stale data, recovery, correction, and overload for each option;
7. trace purpose, authorization, minimization, copies, residency, retention, deletion, providers, and audit through each style;
8. estimate lifecycle costs and organizational coupling with uncertainty rather than initial build effort alone;
9. design hybrids with explicit authority, cross-style race behavior, synchronization, and consumer contracts;
10. write an evidence-backed decision record with sensitivity analysis, validation plan, migration seams, review triggers, and retirement.

## Core Exposition

**Start with the consumer outcome.** Name the person, system, or process using the data; the decision or effect; acceptable incorrectness; and response to missing or stale state.

“Integrate CRM with Billing” is topology. “Billing must price an order using the authoritative customer tier effective at acceptance” begins a semantic requirement.

**Classify the interaction.** A command asks an owner to change state. A query requests a representation. An event records an occurrence. A snapshot represents a population. A change record exposes source mutation.

Do not substitute one for another casually. Polling a query can approximate notifications but adds load and misses intermediate facts. Treating a command as an event hides rejection.

**Define assertions.** Record source authority, keys, grain, fields, units, codes, nulls, quality, provenance, limitations, and correction.

The same delivery technology can carry source facts, derived assertions, or opaque bytes. Semantic fitness precedes transport choice.

**Define population.** Decide whether the consumer needs one entity, a bounded set, every change, a complete snapshot, historical versions, or an aggregate.

Interactive APIs fit bounded selection. Batch and materialized products often fit complete populations. Events fit changes. Federation fits selective cross-source composition. These are tendencies, not rules.

**Define time concepts.** Separate business-effective, source observation, transaction, publication, ingestion, processing, cache, access, and decision time.

A five-millisecond response can contain day-old state. A daily batch can arrive on time but omit late business-effective records. Time semantics shape architecture.

**Define useful freshness.** Ask how old the source observation may be when used, for which population and consequence. Express objectives by percentile or bound and workload.

Avoid “real time,” “near real time,” and “live” without boundaries. Extremely low latency can be unnecessary, expensive, and less resilient.

**Decompose latency.** End-to-end delay may include source commit, outbox or capture, broker queue, transfer, consumer lag, transformation, cache, query, rendering, and human decision.

Optimizing network transit while ignoring queue or source-publication delay is ineffective. Measure components and total at consumer-relevant boundaries.

**Define consistency.** Identify invariants and observations that must agree: read-after-write, per-entity order, one snapshot, atomic multi-record state, bounded staleness, or eventual convergence.

Do not choose the strongest label reflexively. Stronger coordination can reduce availability and increase latency. Choose what the consumer outcome actually requires.

**Define history.** Current state, all transitions, periodic snapshots, audit evidence, and reproducible analytical history need different products.

An API for current state cannot reconstruct missed events. A CDC log may preserve physical changes without business explanations. A batch can omit intermediate transitions.

**Define update and read shape.** Measure events or changes per second, entity count, payload distributions, fan-out, query selectivity, full population size, concurrency, and bursts.

Daily averages conceal peaks and backfills. Include growth, month end, acquisition, disaster recovery, retry, replay, and slow consumers.

**Define direction and initiative.** Consumers can pull on demand, producers can push facts, or shared engines can evaluate requests. Each places discovery, retry, capacity, and availability differently.

Pull makes consumer timing explicit but can repeat work. Push improves notification but creates delivery and consumer-state duties. Federation defers integration to query time.

**Define temporal coupling.** Synchronous requests require concurrent availability and latency. Queues, files, and materializations decouple processing time but add state, staleness, and recovery.

Decoupling is not absence of dependency. Retention, backlog, schema, and consumer capacity replace immediate timing constraints.

**Define failure consequence.** Ask what happens if producer, path, intermediary, consumer, identity, schema registry, region, or operator fails.

Consider loss, duplication, reordering, partial population, stale state, inconsistent cross-source read, incorrect effect, and unknown delivery. Select a style whose failures can be detected and corrected.

**Define protection constraints.** Record purpose, minimization, subject relationship, fields, row policy, residency, providers, storage, retention, deletion, records, licensing, audit, and incidents.

A style that necessarily persists prohibited data in another region is infeasible regardless of speed. Eliminate it before scoring preferences.

**Define ownership.** Name who owns source assertions, interface, platform, transformations, consumer fitness, operations, protection, correction, and retirement.

Architectures fail when a central team owns transport but is assumed to own domain meaning, or consumers use copied state without accepting correction duties.

**Separate constraints from criteria.** Constraints are pass/fail requirements: a payment invariant cannot tolerate independent multi-writer conflict, or law forbids a copy. Criteria compare feasible choices: latency, autonomy, cost, or skill availability.

Do not let a weighted score offset a failed constraint. Record evidence and exception authority for every rejection.

**Compare a direct relationship.** A direct API, message, or file can minimize intermediaries for a few stable parties. It preserves local clarity when contracts and ownership are strong.

Fan-out, bespoke mappings, duplicated controls, unknown consumers, and change amplification make direct designs less attractive as the graph grows.

**Compare shared mediation.** A hub, broker, gateway, or ESB can reuse routing, protocol, transformation, policy, buffering, and observation.

It adds concentration, shared capacity, platform operation, change queues, and potential semantic centralization. Select named capabilities, not middleware as a blanket answer.

**Compare APIs.** APIs fit commands and bounded queries with explicit request-response behavior. They support authentication, authorization, conditional requests, errors, quotas, and consumer-driven timing.

They couple availability and can become poor bulk channels. Pagination over changing data may not form one snapshot. Current detail and complete history require different designs.

**Compare events.** Events fit authoritative occurrences consumed asynchronously by several parties. They support independent processing and replay where retained.

They add duplication, ordering, lag, idempotency, consumer state, schema evolution, and correction. Broker acceptance is not consumer outcome.

**Compare CDC.** CDC fits physical change propagation, replication, cache or index maintenance, migrations, and analytical ingestion when source mutations are relevant.

It couples to source schemas, keys, logs, transactions, snapshot handoffs, and retained-log risk. Derive domain events only through accountable semantics.

**Compare batch and files.** Batch fits coherent bulk populations, constrained partners, offline processing, archival evidence, and efficient analytical loading.

It adds schedules, manifests, atomic publication, arrival windows, backfills, storage, and delayed correction. A file is not self-describing.

**Compare replication.** Replication fits read locality, scale, standby recovery, migrations, and specialized local state. It can provide low read latency at the cost of copies and synchronization.

It adds lag, authority, conflicts, tombstones, failover, source load, residency, and reconciliation. It is not a backup by itself.

**Compare federation.** Federation fits selective cross-source questions when durable copying is undesirable and runtime dependency is acceptable.

It adds semantic mappings, mixed-time reads, planner uncertainty, source load, identity propagation, partial failure, spills, and unpredictable latency.

**Compare materialized products.** A warehouse table, aggregate, snapshot, index, or cache can offer stable service, historical reproducibility, and bounded source load.

It introduces freshness, duplication, storage, synchronization, protection, correction, and lifecycle. Materialization should have product ownership, not remain an accidental cache.

**Use feasibility screening.** For each option test semantic authority, required history, consistency, maximum latency and freshness, workload capacity, failure recovery, protection, organizational capability, and lifecycle.

Reject with a reason and evidence. A prototype can resolve unknown feasibility; it should not silently become production.

**Build scenarios.** Evaluate ordinary load, peak, producer outage, consumer outage, intermediary failure, network partition, schema change, credential rotation, replay, backfill, source correction, region loss, and retirement.

Styles that look equivalent on a happy path diverge under failure. Scenario outcomes are stronger than feature checklists.

**Use weighted matrices carefully.** Define criteria, scales, weights, evidence, uncertainty, and veto constraints. Calculate transparently.

Scores organize discussion. They do not measure truth on a common physical scale. Avoid decimal precision unsupported by evidence and never hide decisive concerns inside averages.

**Run sensitivity analysis.** Vary uncertain scores and weights. If the decision flips under small plausible changes, gather stronger evidence or prefer a reversible path.

If one option remains preferable across ranges, confidence increases. Sensitivity is still conditional on having included the right constraints and alternatives.

**Prototype risky mechanisms.** Test source load, event lag, API capacity, batch windows, federation plans, replica failover, schema evolution, and recovery at realistic scale.

Measure boundaries relevant to consumers. A synthetic throughput test does not prove semantic correctness, authorization, or operator readiness.

**Include organizational throughput.** A technically scalable platform can still have a four-week onboarding or mapping queue. Count review, release, incident, and ownership capacity.

Shared platforms need paved paths and guardrailed autonomy. Domain teams need support for contracts and operations. Selection allocates human work as well as machines.

**Include change autonomy.** Ask how a source schema, definition, policy, workload, consumer, or provider change propagates. Versioning and product boundaries can reduce coordinated releases.

Events and APIs do not guarantee autonomy if every consumer relies on accidental behavior. Batch does not guarantee coupling if contracts and versions are stable.

**Include correction.** Determine how a wrong source assertion reaches consumers, how affected populations and time are identified, and how reports, models, caches, and decisions are repaired.

Low-latency propagation can spread error faster. A style's value includes containment, provenance, correction, and consumer evidence.

**Include observability.** Require stable identifiers across source, product, route, event, batch run, snapshot, query, replica epoch, consumer, and outcome.

Track expected and actual publication, transfer, queue, processing, freshness, quality, protection, failure, replay, correction, and closure. Monitoring must match the style's failure modes.

**Include total cost.** Estimate build, infrastructure, source capacity, network, storage, licensing, operations, support, change, incidents, assurance, consumer work, migration, coexistence, and retirement.

Use ranges and evidence. Do not add hours, dollars, risk scores, and service percentages without an explicit decision method.

**Design hybrids by responsibility.** A common combination uses events for notification, APIs for current detail, and snapshots for bootstrap or analytics.

Define shared identity, authority, version, time, and correction. State whether the API is guaranteed to reflect an event before notification and how snapshot position aligns with events.

**Avoid redundant uncontrolled paths.** Publishing the same fact through API, event, file, and replica can create inconsistent contracts and protection.

Each path needs purpose and owner. Reuse one source-aligned semantic product while varying delivery only where consumer needs justify it.

**Define precedence.** If API, event, batch, and replica disagree, consumers need a rule: source authority, highest committed version, correction record, or explicit investigation.

Do not let arrival time choose truth accidentally. Preserve provenance and time boundaries so disagreements can be diagnosed.

**Design migration seams.** Use adapters, facades, dual publication, versioned contracts, snapshots plus positions, and consumer registration to move incrementally.

Change transport, semantics, ownership, and consumer behavior separately where possible. Parallel validation compares outcomes, not only bytes.

**Bound coexistence.** Dual paths add duplicate effects, inconsistent timing, extra copies, cost, and operational ambiguity. Name the authoritative path and rollback.

Set exit criteria and expiry. Temporary architecture needs stronger lifecycle discipline because it is easy to forget.

**Write the decision record.** Capture context, governing question, requirements, constraints, criteria, alternatives, evidence, scores, uncertainties, scenarios, risks, decision, dissent, controls, validation, owners, migration, and review triggers.

Make the decision understandable without the meeting. Link contracts and test evidence. Record what would falsify the choice.

**Define evolution triggers.** Revisit after new consumer types, order-of-magnitude workload change, repeated service failure, growing lag, correction difficulty, regulatory change, provider exit, cost threshold, or platform end of support.

A decision is valid for assumptions and time, not forever. Review triggers prevent sunk cost from masquerading as current evidence.

**Retire rejected and replaced paths.** Remove routes, jobs, topics, files, APIs, credentials, schemas, replicas, caches, connectors, alerts, docs, copies, and contracts after migration.

Preserve required history, provenance, holds, and correction. Verify consumers and absence of use. Selection includes the cost of ending the predecessor.

**Measure the chosen outcome.** Track semantic defects, end-to-end freshness, latency, availability, completeness, lag, duplicates, source load, protection exceptions, incidents, consumer satisfaction, change lead time, cost, and retirement.

Compare observed evidence with the decision record. If assumptions fail, adapt the architecture rather than defending the original label.

## Definitions and Notation

Represent decision $D=(N,A,I,T,P,W,C,F,Z,O,L,K,R,E)$, where $N$ is consumer need, $A$ assertions and authority, $I$ interaction, $T$ time and freshness, $P$ population and history, $W$ workload, $C$ consistency, $F$ failure and recovery, $Z$ protection, $O$ ownership and organization, $L$ lifecycle cost, $K$ hard constraints, $R$ ranked criteria, and $E$ evidence and uncertainty.

For style $s$, feasibility is predicate $Feasible(s)=\bigwedge_{k\in K} k(s)$. A score is considered only when this predicate holds. No finite preference score repairs a failed hard constraint without an authorized requirement change or exception.

For feasible style $s$, an illustrative additive score is $Score(s)=\sum_i w_i r_i(s)$, where weights $w_i$ and ratings $r_i$ share a declared ordinal scale and evidence. The arithmetic is exact; the model remains judgmental and non-compensatory concerns must stay as constraints.

Let end-to-end decision latency be $L_d=t_{decision}-t_{source\ occurrence}$ and data age at use be $F_u=t_{use}-t_{source\ observation}$ under compatible time meanings and clocks. Component delays can overlap, so summing measured percentiles blindly is invalid.

Define `JustifiedStyle(D,s,t)` as a review predicate requiring semantic fitness, constraint satisfaction, bounded temporal and failure behavior, effective protection, supportable workload and ownership, lifecycle advantage over alternatives, validation evidence, migration seams, and review triggers at time $t$.

## Mechanisms, Invariants, or Proof Structure

Use ten gates for every consequential style decision.

**1. Outcome gate.** Define consumer, decision or effect, consequence, assertions, source authority, keys, grain, quality, correction, and limitations.

**2. Time gate.** Define business, observation, publication, transfer, processing, cache, access, and decision times; freshness, latency, staleness, history, and calendars.

**3. Workload gate.** Quantify population, updates, reads, bytes, fan-out, selectivity, concurrency, bursts, growth, backfills, replay, and recovery.

**4. Consistency gate.** State transactions, ordering, read-after-write, snapshots, convergence, conflicts, duplication, gaps, idempotency, and reconciliation.

**5. Protection gate.** Apply purpose, minimization, identity, authorization, metadata, copies, regions, providers, retention, deletion, records, audit, and incidents.

**6. Feasibility gate.** Test every alternative against semantic, temporal, consistency, workload, failure, protection, organizational, and lifecycle constraints.

**7. Trade-study gate.** Compare feasible options using shared scenarios, evidence, ranges, weights, sensitivity, prototypes, costs, risks, and dissent.

**8. Hybrid gate.** Define cross-style identity, authority, precedence, time, races, synchronization, failure, protection, correction, and consumer contracts.

**9. Transition gate.** Plan seams, versions, parallel validation, cohorts, authoritative paths, coexistence bounds, rollback, communication, and predecessor retirement.

**10. Evidence gate.** Record decision, owners, assumptions, tests, outcomes, uncertainties, review triggers, metrics, corrections, revisions, and closure.

The executable example calculates one transparent illustrative preference matrix after feasibility screening.

<!-- bijux-verify: {"id":"integration-style-weighted-score","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"events_score=87\napi_score=81\nbatch_score=80\nranking=events,api,batch\nscore_margin_first_to_second=6\n","stderr":""}} -->
```python
weights = {
    "semantic_fit": 5,
    "latency_fit": 4,
    "population_fit": 3,
    "failure_fit": 4,
    "protection_fit": 5,
}
ratings = {
    "api":       {"semantic_fit": 4, "latency_fit": 5, "population_fit": 3, "failure_fit": 3, "protection_fit": 4},
    "events":    {"semantic_fit": 5, "latency_fit": 5, "population_fit": 2, "failure_fit": 4, "protection_fit": 4},
    "batch":     {"semantic_fit": 4, "latency_fit": 1, "population_fit": 5, "failure_fit": 4, "protection_fit": 5},
}

scores = {
    style: sum(weights[name] * value for name, value in criteria.items())
    for style, criteria in ratings.items()
}
ranking = sorted(scores, key=lambda style: (-scores[style], style))

for style in ranking:
    print(f"{style}_score={scores[style]}")
print(f"ranking={','.join(ranking)}")
print(f"score_margin_first_to_second={scores[ranking[0]] - scores[ranking[1]]}")
```

The arithmetic proves only that these declared integer ratings and weights produce scores 87, 81, and 80. It does not prove that criteria are complete, ratings are evidenced, scales are cardinal, compensation is legitimate, constraints pass, uncertainty is small, or events are the correct design. A real decision requires feasibility screening, traceable evidence, sensitivity, scenarios, prototypes, consumer validation, and accountable judgment.

## Alternatives and Trade-Offs

**One style versus hybrid.** One style simplifies operation and contracts but can distort unlike needs. Hybrids fit consumers better while adding cross-style identity, races, correction, and lifecycle.

**Pull versus push.** Pull makes consumer timing explicit and supports selective access; it adds repeated requests and source availability. Push reduces detection delay but adds delivery and consumer state.

**Synchronous versus asynchronous.** Synchronous interaction gives immediate outcome but couples latency and availability. Asynchrony buffers timing while adding lag, duplicates, replay, and deferred failure.

**Materialized versus virtual.** Materialization stabilizes workload, history, and service while adding copies and freshness. Virtual access reduces intended storage but depends on sources at query time.

**Current state versus change history.** Current products simplify use but lose transitions. Event or CDC histories support reconstruction and audit while increasing ordering, schema, retention, and replay duties.

**Strong consistency versus bounded staleness.** Coordination protects invariants and recent reads but costs latency and availability. Bounded stale copies can serve analysis efficiently when explicitly acceptable.

**Central mediation versus domain boundaries.** Shared platforms reuse routing, policy, and observation. Domain-owned products preserve meaning and change autonomy. Combine technical reuse with semantic accountability.

**Uniform standard versus exception.** Standards reduce variation and support costs. Evidence-based exceptions preserve fit for unusual latency, volume, protocol, residency, or failure needs.

**Quantitative score versus narrative scenario.** Scores expose priorities and sensitivity. Scenarios expose non-compensatory failures and operational realities. Consequential decisions need both.

**Optimal present choice versus reversible path.** A fully optimized platform may require irreversible migration. A seam-based option can preserve learning and rollback at temporary coexistence cost.

## Failure Modes and Misconceptions

1. **There is one best integration style.** Fitness depends on meaning, time, workload, failure, protection, and lifecycle.
2. **Low latency means fresh data.** Source observation and cache age remain.
3. **Real time is a requirement.** It lacks boundaries, percentile, consequence, and failure context.
4. **Events remove coupling.** Contracts, order, consumer state, and replay remain.
5. **APIs are unsuitable for all bulk work.** Export APIs can govern asynchronous snapshots without carrying each row interactively.
6. **Batch is always stale.** A coherent frequent batch can be fresher for use than a lagging event consumer.
7. **CDC produces domain events automatically.** Physical mutations need semantic derivation.
8. **Federation eliminates data movement.** Runtime buffers, shuffles, spills, caches, and results copy data.
9. **Replication guarantees availability.** Authority, quorum, lag, shared failure, and recovery matter.
10. **A weighted matrix makes the decision objective.** Criteria, weights, ratings, and compensation are judgments.
11. **A high score can offset failed policy.** Hard constraints require rejection or authorized exception.
12. **Average latency predicts user experience.** Tail, bursts, failures, and consumer processing dominate.
13. **The incumbent is proven and alternatives are speculative.** Existing defects and lifecycle costs need equal evidence.
14. **One delivery path should serve every consumer.** Populations, histories, and interaction needs legitimately differ.
15. **Hybrid means duplicating everything.** Responsibilities and data can be minimized per path.
16. **A successful prototype proves production fitness.** Protection, failure, scale, operations, and retirement remain.
17. **A decision record ends the decision.** Assumptions and review triggers require continued evidence.

## Worked Examples

### Example 1

A support screen needs one Customer record on demand with acceptable age thirty seconds. A protected API with conditional caching fits better than a complete event reconstruction. **Conclusion:** bounded selective queries favor request-driven access when availability and freshness are supportable.

### Example 2

A fraud detector must react within two seconds to PaymentAccepted for thousands of payments and recover after outage. An event product with per-payment order, idempotent effects, retention, and replay fits. **Conclusion:** fact semantics and independent timely consumers favor events.

### Example 3

A regulator needs a signed complete month-end population reproducible for seven years. A versioned snapshot with manifest, checksum, provenance, holds, and correction fits better than API crawling. **Conclusion:** coherent archival evidence favors governed batch artifacts.

### Example 4

A search index needs every committed product-row change but no business-event explanation. CDC plus snapshot handoff and idempotent keyed application fits. **Conclusion:** physical current-state maintenance can justify CDC without mislabeling mutations as domain facts.

### Example 5

An analyst runs a selective cross-source query monthly and policy forbids a durable combined copy. Federation with source-side authorization, budgets, explicit mixed-time semantics, and protected spills fits. **Conclusion:** selective composition and copy constraints can justify virtualization.

### Example 6

A regional catalog needs sub-50-millisecond reads and tolerates sixty seconds of staleness. Asynchronous replication with disclosed applied position fits; it is not used for write authority or backup. **Conclusion:** locality and bounded staleness can justify a replica.

### Example 7

A scoring matrix ranks events first by six points, but events would persist prohibited health data in an unavailable region. The option fails a hard constraint and is rejected. **Conclusion:** feasibility precedes preferences.

### Example 8

An API sends current Order detail after an OrderChanged event, but the API replica can lag the event. The event includes a source version; the API waits for or rejects below that version. **Conclusion:** hybrids require an explicit cross-style visibility contract.

### Example 9

A daily batch was assumed too slow, yet the event consumer has a fourteen-hour backlog during month end. End-to-end evidence shows the validated batch is fresher for reporting. **Conclusion:** labels do not determine achieved freshness.

### Example 10

Workload grows tenfold and federation repeatedly scans operational sources. A recorded trigger initiates a materialized aggregate pilot and migration. **Conclusion:** review triggers turn architecture decisions into revisable evidence rather than permanent doctrine.

## Cross-Program Connections

- **Distributed systems:** clocks, consistency, queues, retries, idempotency, partitions, replication, overload, and recovery determine feasible guarantees.
- **API and service engineering:** commands, queries, HTTP, events, contracts, gateways, compatibility, reliability, and deprecation implement interactive choices.
- **Data engineering:** CDC, streaming, batch, snapshots, materialization, federation, lineage, backfills, and serving implement movement and access.
- **Database engineering:** transactions, logs, snapshots, indexes, query plans, replicas, isolation, and backups shape underlying capabilities.
- **Platform engineering:** paved paths, brokers, gateways, transfer, connectors, identity, observability, capacity, and self-service affect organizational fit.
- **Cybersecurity and privacy:** purpose, minimization, copies, metadata, residency, providers, retention, deletion, and incidents create hard constraints.
- **Economics and decision science:** opportunity cost, ranges, multi-criteria analysis, sensitivity, option value, reversibility, and sunk cost support trade studies.
- **Systems engineering:** requirements, interfaces, scenarios, fault analysis, verification, assurance cases, decision records, and lifecycle discipline structure selection.

## References

1. Hohpe, G., and Woolf, B., *Enterprise Integration Patterns: Messaging Patterns Overview*, 2003. <https://www.enterpriseintegrationpatterns.com/patterns/messaging/>
2. OpenAPI Initiative, *OpenAPI Specification 3.1.1*, 2024. <https://spec.openapis.org/oas/v3.1.1.html>
3. AsyncAPI Initiative, *AsyncAPI Specification 3.0.0*, 2023. <https://www.asyncapi.com/docs/reference/specification/v3.0.0>
4. Cloud Native Computing Foundation, *CloudEvents Specification 1.0.2*, 2022. <https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md>
5. PostgreSQL Global Development Group, *Logical Decoding Concepts*, PostgreSQL Documentation. <https://www.postgresql.org/docs/current/logicaldecoding-explanation.html>
6. W3C, *SPARQL 1.1 Federated Query*, W3C Recommendation, 2013. <https://www.w3.org/TR/sparql11-federated-query/>
7. Beyer, B., Jones, C., Petoff, J., and Murphy, N. R., eds., *Site Reliability Engineering: Addressing Cascading Failures*, Google, 2016. <https://sre.google/sre-book/addressing-cascading-failures/>
8. NIST, *Systems Security Engineering: Considerations for a Multidisciplinary Approach in the Engineering of Trustworthy Secure Systems*, SP 800-160 Volume 1 Revision 1, 2022. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>

## Exercises

### Exercise 1

Translate “We need inventory data in real time” into a complete decision requirement covering meaning, time, workload, consistency, failure, protection, ownership, and lifecycle.

### Exercise 2

Construct a feasibility screen and weighted trade study for API, events, and batch for a fraud use case. Explain sensitivity and non-compensatory constraints.

### Exercise 3

Design a hybrid event, API, and snapshot architecture for Order data. Define cross-style identity, time, visibility, recovery, correction, and consumer contracts.

### Exercise 4

Compare CDC, replication, federation, and materialization for a search index, regional reader, exploratory analyst, and recurring executive report.

### Exercise 5

Write a migration and review plan from twenty direct file and API links to a mixed target architecture. Include evidence, cohorts, rollback, triggers, and retirement.

## Answers to the Exercises

### Answer 1

Name the consumer decision: for example, prevent sale of unavailable stock at order acceptance. Define authoritative Inventory assertions, product owner, item and location keys, grain, available-to-promise definition, reservations, units, nulls, quality, provenance, and correction. Separate business-effective, source-observation, publication, access, and decision time. Replace “real time” with a bound such as 99.9 percent of accepted inventory changes visible to order decisions within two seconds under declared load, and state maximum useful age and degraded behavior.

Quantify items, locations, update and read rates, payload, fan-out, concurrency, bursts, growth, backfills, and recovery. Define per-item ordering, read-after-write, duplicates, gaps, transaction scope, outage behavior, RPO and RTO where relevant, and correction. Specify purpose, fields, row access, regions, providers, copies, retention, deletion, audit, and incident constraints. Assign source, platform, consumer, operations, and protection ownership. Include cost horizon, change autonomy, versioning, migration, coexistence, retirement, evidence needed, and triggers such as workload growth or missed decision freshness.

### Answer 2

First define authoritative PaymentAccepted facts, two-second useful freshness, per-payment order, six-hour outage recovery, thousands-per-second workload, authorized fraud purpose, minimized fields, residency, replay retention, consumer idempotency, and correction. Feasibility screening might reject batch for the two-second action constraint and reject any event platform lacking required residency. API polling may remain feasible only if source load and missed-transition behavior are bounded. Events may be feasible with replay and consumer-state controls.

For feasible options choose criteria such as semantic fit, latency, fan-out, failure recovery, protection, change autonomy, operations, and lifecycle cost. Define ordinal scales, weights, evidence, uncertainty, and vetoes. Calculate scores transparently, then vary weights and uncertain ratings. If a one-point change reverses rank, gather prototype evidence. Run peak, broker outage, consumer outage, schema change, replay, and correction scenarios. The matrix organizes judgment; it cannot compensate for failed residency or fact semantics and does not prove cardinal differences among ratings.

### Answer 3

The Order domain owns stable order and event IDs, accepted and lifecycle facts, business-effective and publication time, schema versions, classifications, and correction. Events notify authorized consumers and carry enough state for prompt reactions. Per-order ordering, at-least-once delivery, idempotent effects, lag, retention, replay, dead letters, and consumer outcomes are explicit. The API serves authorized current detail and commands with resource versions, conditional requests, idempotency, errors, capacity, and freshness.

Each event includes the source version that its change created. An API read with minimum version either returns state at least that new, waits within a deadline, routes to authority, or reports unavailable; it never silently returns older detail. A versioned snapshot records a source position aligned with the event stream so analytics or new consumers bootstrap then apply later events. Corrections reference affected events and versions and flow to API state, snapshots, and registered consumers. Protection and retention vary by path but share purpose and authority. Failure scenarios cover event-before-read races, API outage, duplicate events, snapshot gaps, and replay. One path is authoritative for each operation, and all have migration and retirement evidence.

### Answer 4

Use CDC for a search index that needs every committed source mutation, with snapshot handoff, stable keys, schema history, deletes, idempotent application, lag, and reconciliation; derive business facts separately. Use asynchronous replication for a regional reader needing low latency and tolerating bounded staleness, with one write authority, applied-position evidence, failover rules, protection, and reconciliation. Use federation for a selective exploratory analyst when durable combined copies are undesirable and source load, mixed-time semantics, identity, spills, and partial failure can be bounded.

Use a materialized aggregate for a recurring executive report whose joins scan large sources and need reproducible historical results, stable service, governed metrics, and source protection. It adds freshness, storage, synchronization, and correction duties. These styles can coexist behind shared source products and identifiers. Selection is conditional on measured workload, consistency, history, protection, service, cost, and operating maturity. Reassess if queries become frequent, replica staleness becomes unacceptable, search needs domain semantics, or report freshness changes.

### Answer 5

Inventory every link, producer, consumer, purpose, assertion, key, grain, time, file or API contract, workload, schedule, transformation, service, protection, cost, failure, and owner using declared and runtime evidence. Identify unknown consumers through logs, credentials, network records, schedules, reports, and interviews. Classify needs as commands, queries, facts, snapshots, change records, replication, or cross-source computation. Screen options against semantics, consistency, latency, residency, recovery, and organizational constraints.

Retain justified direct links. Use APIs for bounded interactions, event products for reusable facts, snapshots for coherent bulk state, CDC for internal physical propagation, replication for locality, and materialized or federated products for analytical needs. Add stable identities, contracts, consumer registration, telemetry, and correction first. Migrate coherent cohorts through facades, adapters, dual publication, snapshot positions, and parallel validation. Compare meanings, values, time, order, gaps, service, protection, and decisions; define authoritative path and rollback.

Record review triggers for workload, incidents, lag, cost, consumer growth, regulation, and platform support. Bound coexistence and exceptions. After acceptance, stop old jobs and routes; revoke credentials and network rules; remove files, APIs, topics, schemas, caches, copies, alerts, providers, and docs; update catalogs and lineage; preserve required evidence and holds; and verify absence. Measure target outcomes against the decision record.
