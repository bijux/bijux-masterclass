---
module_id: DARCH-004
program: Data Architecture Engineering
level: 1
module_number: 4
title: Systems of Record, Engagement, and Insight
status: complete
last_verified: 2026-09-03
---

# Systems of Record, Engagement, and Insight

## One-Page Review

### Governing question

How should an architecture assign and connect authoritative fact management, human or machine interaction, and analytical interpretation without creating competing truth, uncontrolled feedback, or fragile point-to-point coupling?

### Essential definitions

- A **system of record** is the authorized decision boundary for creating, changing, correcting, and retiring specified facts for a declared population and time—not necessarily the only place those facts are stored.
- A **system of engagement** supports an interaction or task at a participant boundary, often adapting presentation, workflow, latency, and context to users, devices, partners, or channels.
- A **system of insight** derives observations, measures, classifications, predictions, explanations, or recommendations from source data for a named decision and horizon.
- A **projection** is a derived representation maintained for a consumer purpose; its truth is conditional on source authority, transformation, snapshot, and freshness.
- **Write authority** is permission and accountability to accept a state transition for specified facts, distinct from physical ability to update a copy.
- **Decision authority** is the right to act or commit an outcome; an insight system may inform a decision without owning it.
- A **feedback path** carries decisions or learned information back toward an operational boundary and therefore requires an explicit command, contract, policy, and correction mechanism.

### Central model, mechanism, or theorem

Assign roles per fact and operation, not per vendor product:

`Role(system, fact, operation, context, time) -> {record, engagement, insight}`

For each authoritative fact family, there must be one unambiguous acceptance rule at a given boundary and time. Engagement systems submit intent or present state through contracts. Insight systems derive evidence and recommendations with provenance. Any path that changes authoritative state must return through an authorized command and validation boundary; copying or analyzing a fact does not confer write authority.

### Critical invariants

- Authority is scoped by fact, population, jurisdiction, operation, valid time, and system version.
- A single accepted state transition has one accountable decision boundary, even when several systems participate.
- Projections retain source identity, derivation, snapshot or event position, freshness, and correction behavior.
- Engagement channels do not silently create separate business rules or masters.
- Insight outputs identify evidence, model or rule version, uncertainty, intended decision, and accountable decision authority.
- Feedback into operations uses explicit commands, idempotency, authorization, validation, audit, and compensation or correction.
- A system-of-record designation is not a records-management, legal-admissibility, quality, availability, or universal-truth guarantee.

### Common failures

Typical failures are labeling whole platforms as record, engagement, or insight; naming a warehouse “the source of truth” for every fact; allowing a mobile application to persist an independent master; letting dashboards become undocumented APIs; writing model scores directly into operational tables; confusing event logs with automatically valid business facts; ignoring temporal authority during migration; and treating replicas or materialized views as authoritative because they are easier to query.

### Compact example

A customer enters a new delivery address in a mobile application. The app is the engagement boundary. An order service validates whether the address may change and records the accepted order-address version. A risk service derives a delivery-risk score from order and location data. The score may cause the app to request confirmation, but it cannot silently rewrite the address. Each role is scoped to a fact and decision, and the feedback path returns through the order service.

### Connections

[DARCH-003](003-current-state-data-landscape.md) discovers which systems actually play these roles. [DARCH-005](../ROADMAP.md) distinguishes operational, analytical, and shared data. [Data Engineering](../../19-data-engineering/ROADMAP.md) implements projections and pipelines; [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies transactional and replication guarantees; [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) develops the contracts through which engagement and feedback cross authority boundaries.

## Governing Question

Organizations use the phrases “system of record,” “system of engagement,” and “system of insight” to simplify a complex estate. The simplification can be useful: some boundaries accept durable facts, some optimize interaction, and some derive information for decisions. It becomes dangerous when the labels are attached permanently to products or architecture tiers.

One customer platform may be authoritative for contact preferences, an engagement surface for support cases, and a consumer of credit insight. A warehouse may be authoritative for a governed monthly metric while holding nonauthoritative copies of orders. A mobile client may accept user intent but lack authority to decide whether a regulated account change is valid. Roles depend on the fact, operation, context, and time.

The governing problem is to allocate authority and connect the roles. Which system may accept a fact? Which system presents or gathers information for a participant? Which system derives a measure or prediction? How fresh is each representation? How do corrections propagate? How can an insight influence an operation without bypassing policy? The answer is an explicit decision architecture, not a three-box diagram.

## Why This Matters

Ambiguous authority causes duplicate masters, divergent state, reconciliation queues, irreversible automation, and disputes over whose number is correct. The defect is often hidden while systems agree. It emerges during retries, outages, delayed replication, retroactive correction, mergers, model change, or policy exception—exactly when trustworthy behavior matters most.

Engagement needs differ from record-keeping needs. A customer interaction may require low latency, intermittent connectivity, personalized presentation, conversational context, and partial progress. An authoritative service may prioritize invariant enforcement, concurrency, audit, and durable correction. Combining them indiscriminately can make both worse; separating them without a contract can create two truths.

Insight needs also differ. Analytical systems combine history, apply alternative definitions, tolerate bounded delay, estimate uncertainty, and support exploration. They can reveal conditions no source system knows. Yet a useful prediction is not automatically an authorized fact, and an optimized analytical representation is not automatically allowed to drive an operational transition.

Modern architectures amplify feedback. Recommendation engines alter clicks that train future models. fraud scores change which transactions receive investigation and therefore which labels are observed. Inventory forecasts change replenishment and future demand. Without explicit decision and observation boundaries, systems of insight can reshape their own evidence while accountability disappears into a loop.

Clear role contracts enable independent evolution. Teams can replace an engagement channel without redefining account authority, build new projections without exposing private tables, and change a model without granting it unrestricted operational writes. The architecture preserves meaning and control while allowing representations to specialize.

## Prerequisites and Retrieval

You should understand APIs, events, transactions, replication, data pipelines, identity, access control, basic analytics, and the difference between commands and queries. Recall that a dataset identity differs from its distributions and that current-state claims require evidence.

Retrieve the concepts of business fact, invariant, source and valid time, idempotency, eventual consistency, lineage, model version, uncertainty, and human decision authority. Familiarity with CQRS, materialized views, event sourcing, and feedback loops helps, but this chapter introduces their architectural relevance.

## Learning Objectives

After completing this module, you should be able to:

- define system-of-record authority for a bounded fact family and operation;
- distinguish authoritative state, legal or official recordkeeping, physical persistence, replicas, and derived projections;
- identify engagement-specific responsibilities without duplicating domain authority;
- identify insight outputs, evidence, uncertainty, intended decisions, and decision owners;
- assign multiple roles to one system without collapsing the roles;
- design command, query, event, projection, and correction contracts between roles;
- reason about freshness, consistency, and behavior during partitions or stale reads;
- govern insight-to-operation feedback, including human review and automated action;
- represent temporal transfers of authority during migration;
- test a role map for competing writers, provenance gaps, uncontrolled feedback, and unrecoverable projections.

## Core Exposition

Begin with a business fact and decision, not a system name. “Customer data” is too broad. Separate legal-party identity, channel profile, delivery address for an order, marketing permission, billing account, support interaction, and calculated lifetime value. Each has different creation events, correction rules, policies, and authorities.

A **system of record** is authoritative because an organization delegates specified decisions to its boundary and backs them with rules and accountability. It may validate commands, enforce invariants, order changes, assign identifiers, preserve required history, expose accepted state, and issue facts to consumers. Storage technology alone cannot grant this role.

Authority must be stated as a tuple such as `(fact, population, operations, jurisdiction, valid interval, owner)`. An identity registry might authorize creation and correction of employee identifiers for active employees in one legal entity. Payroll may be authoritative for pay elections. A benefits provider may govern enrollment decisions under a contract. No single application is “the employee source of truth” without qualification.

The phrase **single source of truth** is often misleading. A fact can have one current write authority while legitimate historical, jurisdictional, consumer, and model-specific representations coexist. Different authorities can own different parts of a compound concept. The design objective is not one physical copy; it is unambiguous decision rights, contracts, and reconciliation.

Do not confuse architecture authority with legal records management. A database designated as system of record may fail statutory retention, authenticity, preservation, legal-hold, or evidentiary requirements. Conversely, an immutable archive can be the official preserved record without being the online command boundary. Legal, records, privacy, and audit authorities must decide those properties under the applicable regime.

Likewise, authority does not guarantee accuracy. An authorized service can accept an incorrect address based on flawed input. It is authoritative for the accepted state, not metaphysically true. Track provenance, uncertainty, disputes, and correction. Some facts—identity matches, estimated locations, clinical interpretations—may require competing claims rather than premature collapse to one value.

A **system of engagement** optimizes a participant interaction. Participants include customers, staff, devices, partners, suppliers, public users, and other systems. Responsibilities may include presentation, accessibility, localization, conversational context, input assistance, session state, offline capture, workflow navigation, consent interaction, notification, and recovery from partial work.

AIIM's early [systems of record and engagement discussion](https://info.aiim.org/aiim-blog/newaiimo/2010/10/20/systems-of-record-and-systems-of-engagement) framed systems of engagement around collaboration and human-centered interaction in contrast to transaction-centered enterprise records. The terminology is industry framing, not a normative architecture standard. Today, engagement boundaries include machine clients and automated channels as well as people.

An engagement system may originate intent without owning the resulting fact. A form can collect an address-change request, attach evidence and idempotency identity, and show the eventual outcome. The authoritative service decides whether the request satisfies policy and invariants. The engagement system should not report success merely because it stored the request locally.

Some engagement systems legitimately own engagement facts. A support platform may be authoritative for conversation messages and case workflow while consuming customer identity and account status from other authorities. Roles are not hierarchical. Being “engagement” does not mean disposable or nonauthoritative; it means the relevant interaction role is being described.

A **system of insight** transforms observations into information for a decision. Outputs include descriptive measures, diagnostic explanations, classifications, forecasts, anomaly signals, risk estimates, recommendations, simulations, and learned representations. Its contract should state input populations and snapshots, definitions, transformations, model or rule versions, freshness, uncertainty, known limitations, intended uses, prohibited uses, and owner.

Insight can be authoritative for a derived product under an approved definition. A finance measurement service may be the authorized publisher of monthly recurring revenue for a specific accounting view. That does not make it authoritative for underlying invoices, contracts, or cash receipts. Authority for a derived fact must include its definition, time boundary, revision policy, and inputs.

An insight is not a decision. A fraud score may inform approve, decline, or review actions; a human or automated policy boundary owns that action. Name the decision authority, thresholds, exception and appeal paths, required explanation, monitoring, and fallback. This separation prevents a model deployment from silently becoming a policy change.

One system can play all three roles for different facts. A commerce service may record accepted orders, present an operator console, and calculate a local availability signal. Separation of roles is conceptual before it is physical. A forced three-tier deployment can add latency and failure without clarifying authority.

Conversely, one role can be distributed. A globally partitioned order service may share one logical authority across regions through deterministic routing and conflict rules. A federated insight product may compute locally and aggregate governed outputs. “One system of record” need not mean one server, database, vendor, or team, but the logical decision boundary must remain testable.

Connections between roles use different messages. A **command** requests a state transition and expresses intent: `ChangeDeliveryAddress`. A **query** asks for a representation without changing authority. An **event** states that an accepted occurrence happened: `DeliveryAddressChanged`. A **projection update** changes a derived view. These message kinds require identities, versions, authorization, ordering, failure, and replay behavior.

Commands should carry an actor or principal, target aggregate, expected version where relevant, request identity for deduplication, claimed intent, policy context, and evidence. The authoritative boundary validates current state and either rejects or records an accepted transition. A transport acknowledgement is not the same as business acceptance.

Events should describe accepted facts in stable domain terms rather than leaking private storage changes. Consumers need event identity, subject, source, schema version, occurrence and recording times, sequence or causality where available, and correction or supersession semantics. Delivery may be repeated or delayed; consumers must not assume exactly-once business effects merely because a platform uses that phrase.

Queries and projections require freshness semantics. State whether a view is transactionally current, bounded-stale, event-positioned, snapshot-dated, periodically revised, or best effort. A response should identify source and `as_of` time where decisions depend on staleness. “Real time” is not a consistency contract.

The [CQRS pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs) separates write and read models so each can enforce or optimize different concerns. It can use one store or separate stores and materialized views. Separate stores introduce synchronization lag and failure; CQRS is not required merely because commands and queries are conceptually distinct.

A materialized view is a projection, not a new authority, unless governance explicitly assigns authority for a derived fact. It should be reproducible from a known source history or reconcilable against it. If a projection becomes an input to commands, record its position and tolerate stale decisions according to policy.

Event sourcing stores state changes as an ordered event history and derives current state by replay or projection. It can preserve intent and enable new views, but only accepted, well-designed domain events deserve authority. An append-only sequence of malformed or unauthorized messages is not trustworthy because it is immutable. Event evolution, deletion obligations, snapshots, and correction need explicit design.

W3C [PROV](https://www.w3.org/TR/prov-overview/) models entities, activities, agents, generation, use, derivation, and responsibility for interoperable provenance. Provenance helps consumers assess an insight or projection; it does not itself prove input quality, lawful use, correct transformation, or authorized action.

Corrections cross role boundaries differently from ordinary updates. An authority may replace a current value, append a correcting event, withdraw an assertion, or preserve several claims with status. Every projection and insight product needs a rule for retroactive recomputation, versioning, notification, and consumer reconciliation. Engagement surfaces must show corrected outcomes rather than indefinite optimistic state.

Deletion is also a distributed protocol. Removing an authoritative record may conflict with preservation, audit, fraud, or legal-hold duties. Authorized deletion or restriction must propagate to caches, indexes, analytical copies, features, exports, and backups according to policy. Derived aggregates may or may not remain permissible. The record role does not unilaterally settle these questions.

Availability choices should follow the decision. During a partition, may an engagement channel queue intent, operate on stale state, refuse the operation, or accept a limited local transition? A ticket note may be safely captured offline; increasing a credit limit may not. Record merge, conflict, expiry, and user communication behavior before failure occurs.

Caching accelerates engagement but creates temporal truth problems. Cache keys must include relevant tenant, policy, locale, and version dimensions. Invalidation and maximum staleness should match consequence. Never use a cache's physical writability as an excuse to bypass the authoritative command.

Insight systems introduce additional time coordinates: training period, input snapshot, feature observation time, prediction time, decision time, outcome time, and label maturity. A score without these identities cannot be reproduced or fairly evaluated. Model and feature versions join data-contract versions in the provenance chain.

Feedback begins when insight changes operations. Classify the path: advisory display, ranked work queue, human approval, policy-constrained automation, or autonomous actuation. As autonomy and consequence increase, require stronger validation, monitoring, explanation, rollback, override, and independent review.

Feedback can bias future evidence. If high-risk cases receive more investigation, confirmed labels will be denser for those cases. If recommendations determine exposure, click data reflect the prior model's choices. Preserve exploration or evaluation designs where responsible, distinguish observed outcomes from counterfactual claims, and involve appropriate statistical and domain expertise.

Controls belong at boundaries. Authenticate principals at engagement, authorize commands at the record boundary, validate schemas and invariants, protect events in transit and at rest, enforce purposes and access in analytical products, and audit decisions at the point of effect. Duplicating every control in every copy is costly; omitting inherited obligations is unsafe.

Migration creates time-bounded authority. During dual running, state which system accepts each operation, how changes synchronize, how conflicts resolve, and what evidence permits cutover. Two systems may both be technically writable while only one is authoritative, or authority may be partitioned by population. Record effective times and fence old writers before declaring transfer.

Do not declare a new system authoritative simply because data was loaded. Verify completeness, semantics, ordering, identity, constraints, corrections, access, performance, recovery, consumer migration, and operational ownership. After cutover, monitor old writes and reconcile until the rollback and retirement decisions are complete.

Evaluate role design through failure scenarios. What if the engagement channel retries after timeout? What if a projection lags? What if a correction predates the current snapshot? What if the model service is unavailable? What if two authorities claim the same operation? What if policy changes after an insight was computed? Answers should identify safe behavior, evidence, and accountable authority.

## Definitions and Notation

Let `S` be systems, `F` fact families, `O` operations, `C` contexts, and `T` time. Define:

`Role : S x F x O x C x T -> P({R, E, I})`

where `R` means record, `E` engagement, `I` insight, and `P` denotes a set of roles. Multiple roles are allowed. The mapping is incomplete unless each assignment has an accountable owner, contract, evidence, and valid interval.

For an authoritative fact-operation-context tuple `x`, define `Acceptors(x,t)` as the set of logical boundaries allowed to accept a transition at time `t`. The unambiguous-authority invariant is:

`|Acceptors(x,t)| = 1`

where one logical acceptor may be implemented by replicated components. Some domains deliberately permit multiple independent assertions; in that case, the authoritative fact is the set of attributed claims, and a separate policy governs resolution.

A projection `p` is described by `(sources, transform, source_positions, produced_at, as_of, schema, correction_rule, owner)`. Its staleness at decision time `td` may be expressed as `td - as_of`, but clock, event-time, and source-watermark semantics must be defined before comparing it with a limit.

An insight record `i` is `(evidence, method_version, produced_at, intended_decision, uncertainty, limitations, owner)`. A decision record `d` is distinct: `(authority, policy_version, inputs, action, occurred_at, explanation, appeal_or_override)`. Joining `i` to `d` provides traceability without pretending that the insight itself acted.

## Mechanisms, Invariants, or Proof Structure

Use eight gates to review record, engagement, and insight roles.

**1. Fact gate.** Decompose broad nouns into facts, populations, operations, time semantics, and jurisdictions. Identify disputes and multi-claim domains rather than forcing false singular truth.

**2. Authority gate.** Name the logical acceptor and accountable decision owner for each transition. Separate semantic authority, physical custody, platform operation, legal preservation, and risk approval.

**3. Engagement gate.** Describe actors, tasks, channels, accessibility, session and offline behavior, input validation, acknowledgements, failure communication, and the contract that submits intent.

**4. Projection gate.** Specify source identities, transformations, event or snapshot positions, freshness, reconciliation, correction, rebuild, and consumer expectations for every material view.

**5. Insight gate.** State definition or model, evidence, versions, uncertainty, intended and prohibited uses, decision owner, evaluation, fallback, and revision.

**6. Feedback gate.** Route operational effects through explicit authorized commands. Define idempotency, policy validation, human review where required, audit, compensation, appeal, and safe behavior under delay or failure.

**7. Evolution gate.** Version contracts, facts, projections, and models. Define dual-running authority, fencing, reconciliation, cutover, rollback, deletion, correction, and retirement.

**8. Assurance gate.** Exercise retries, stale reads, partitions, duplicate events, conflicting writers, unavailable insights, retroactive changes, policy updates, and recovery. Retain evidence at the point of acceptance and effect.

The executable review below checks a small role registry. It requires exactly one authoritative acceptor per fact and flags an insight system that can write authoritative state without an explicit command path. It also rejects a projection lacking source position. The fixture illustrates architecture linting, not automatic governance.

<!-- bijux-verify: {"id":"role-authority-review","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"facts=3\nvalid_authorities=2\nfindings=credit_limit:competing-authorities,offer_rank:uncontrolled-feedback,order_view:missing-source-position\nready=false\n","stderr":""}} -->
```python
facts = {
    "delivery_address": ("order-service",),
    "credit_limit": ("account-service", "crm"),
    "offer_rank": ("decision-service",),
}
systems = {
    "mobile-app": {"role": "engagement", "authoritative_write": False},
    "offer-model": {
        "role": "insight",
        "authoritative_write": True,
        "command_path": False,
        "finding_name": "offer_rank",
    },
}
projections = {
    "customer_view": {"source_position": "customer-events:481"},
    "order_view": {"source_position": ""},
}

findings = []
valid_authorities = 0
for fact, acceptors in facts.items():
    if len(acceptors) == 1:
        valid_authorities += 1
    else:
        findings.append(f"{fact}:competing-authorities")

for name, system in systems.items():
    if (
        system["role"] == "insight"
        and system["authoritative_write"]
        and not system.get("command_path")
    ):
        findings.append(f"{system['finding_name']}:uncontrolled-feedback")

for name, projection in projections.items():
    if not projection["source_position"]:
        findings.append(f"{name}:missing-source-position")

print(f"facts={len(facts)}")
print(f"valid_authorities={valid_authorities}")
print(f"findings={','.join(sorted(findings))}")
print(f"ready={str(not findings).lower()}")
```

The exact output establishes that the checker implements its declared conditions. It does not prove that the fact decomposition is correct, the named service has legitimate authority, the source position is genuine, or a command path is safe. Those claims need contracts, runtime evidence, policy authority, and human review.

## Alternatives and Trade-Offs

**Unified versus separated models.** One transactional model can simplify consistency and operations for a bounded domain. Separate command and query models can improve fit and scaling but add lag, replay, and reconciliation. Use separation where responsibilities and workloads justify it.

**Direct query versus replicated projection.** Direct queries reduce duplicate state and can provide current answers. They couple availability, schema, performance, and authorization. Projections decouple consumers but introduce freshness and lifecycle obligations.

**Central master versus federated authority.** A central master can align shared facts but may erase domain distinctions and become a bottleneck. Federated authorities preserve context but require explicit intersection contracts, identity resolution, and dispute forums.

**Synchronous command versus asynchronous intent.** Synchronous acceptance gives immediate outcome but couples availability and latency. Queued intent supports intermittent operation and smoothing but needs status, deduplication, expiry, user communication, and compensation.

**Event history versus current-state persistence.** Event history supports temporal explanation and rebuilding but adds schema evolution, replay, privacy, and storage complexity. Current-state persistence is simpler for many domains but may require separate audit and history. Neither is inherently more authoritative.

**Human review versus automated decision.** Human review can apply context and accountability but introduces delay, inconsistency, and workload. Automation can be consistent and fast but magnifies defects and feedback. Match review to consequence, uncertainty, reversibility, and governing rules.

**Warehouse metric versus operational calculation.** A warehouse can produce governed cross-domain and historical measures. Operational calculation can be fresher and closer to action. Definitions, source positions, revision, and intended decision determine which projection is fit.

**One product with multiple roles versus separate systems.** Colocation reduces distributed failure and overhead. Separation can isolate authority and optimize independently. Keep conceptual contracts explicit even when deployment is unified so later decomposition does not invent them under pressure.

## Failure Modes and Misconceptions

1. **A vendor category assigns authority.** Organizational decisions and contracts assign authority; products only implement it.
2. **System of record means only copy.** Replicas, archives, caches, and projections can coexist when their roles are explicit.
3. **Authoritative means correct forever.** Accepted facts can be uncertain, disputed, superseded, or corrected.
4. **System of record satisfies legal recordkeeping.** Preservation, authenticity, retention, hold, and admissibility require separate authority and evidence.
5. **Engagement systems are just user interfaces.** They can own interaction facts, workflow, accessibility, and channel-specific reliability.
6. **The client may enforce the business invariant.** Client validation improves experience; the authoritative boundary must enforce acceptance rules.
7. **Insight is truth.** A measure or prediction is conditional on definition, evidence, version, population, time, and uncertainty.
8. **A score may update operations directly.** Operational effect requires a named decision policy and authorized command path.
9. **A read replica becomes authoritative when the source is down.** Failover authority requires an explicit protocol, fencing, and reconciliation.
10. **An event log is automatically a system of record.** Only accepted domain events with governed identity and evolution can support that role.
11. **Real time means current.** Transport speed says nothing about source position, event time, correction, or consistency.
12. **Dual write is dual authority.** Technical writability must not obscure which transition is accepted during migration.

## Worked Examples

### Example 1

**Question:** Is a CRM the system of record for customer?

**Reasoning:** The question is underspecified. It may govern support interactions and marketing preferences while an identity service owns party identity and billing owns accounts.

**Conclusion:** Assign authority per fact and operation.

### Example 2

**Question:** A mobile app stores an address offline. Is it temporarily the system of record?

**Reasoning:** It records pending intent. Unless the architecture delegates local acceptance and merge authority, the address becomes authoritative only after server validation.

**Conclusion:** Persistence and authority are different.

### Example 3

**Question:** A warehouse publishes the approved monthly revenue metric. Is it a system of record?

**Reasoning:** It can be authoritative for that derived metric and version while remaining a nonauthoritative consumer of invoices, contracts, and cash receipts.

**Conclusion:** Derived facts can have bounded authority.

### Example 4

**Question:** Can a materialized order view be used to reject an address change?

**Reasoning:** Only if the decision policy accepts its bounded staleness and the command boundary revalidates necessary invariants against authoritative state.

**Conclusion:** A projection may inform a command but does not inherit write authority.

### Example 5

**Question:** The fraud model writes `blocked=true` into the payment table. What is missing?

**Reasoning:** The design hides decision authority, policy version, authorization, explanation, appeal, fallback, audit, and model unavailability behavior.

**Conclusion:** Route feedback through an explicit decision and command boundary.

### Example 6

**Question:** Two regional services accept address updates during migration.

**Reasoning:** Partition authority by population or designate one writer and fence the other. Define synchronization, conflict, effective time, rollback, and evidence.

**Conclusion:** Dual running requires one unambiguous acceptance rule.

### Example 7

**Question:** Does an immutable event stream prove the current balance?

**Reasoning:** Only if event acceptance, ordering, schema evolution, corrections, projection logic, and replay position are trustworthy and verified.

**Conclusion:** Immutability preserves bytes, not semantic validity.

### Example 8

**Question:** A support console shows “saved” after enqueueing a command.

**Reasoning:** Enqueue acknowledgement does not establish business acceptance. Show pending state and later accepted or rejected outcome with recovery guidance.

**Conclusion:** Engagement must communicate the authoritative state transition honestly.

### Example 9

**Question:** A recommendation increases clicks. Has the insight system succeeded?

**Reasoning:** Clicks may be a proxy shaped by exposure. Evaluate the owned outcome, guardrails, distribution, causal design, and feedback into future training data.

**Conclusion:** Interaction response is not automatically decision value.

### Example 10

**Question:** When may a read replica accept writes after primary failure?

**Reasoning:** Only under an authorized failover protocol with quorum or fencing assumptions, known recovery point, role transfer, conflict prevention, audit, and failback reconciliation.

**Conclusion:** Failover changes authority through protocol, not convenience.

## Cross-Program Connections

[API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) develops commands, queries, events, idempotency, versioning, authentication, and error contracts between role boundaries. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) explains partitions, ordering, replication, consensus, and failure assumptions beneath logical authority.

[Database Engineering](../../18-database-engineering/ROADMAP.md) supplies transactions, constraints, temporal data, logs, materialized views, replicas, and recovery. Database guarantees implement parts of authority but do not decide business semantics or accountability.

[Data Engineering](../../19-data-engineering/ROADMAP.md) builds projections, lineage, freshness, quality, serving, correction, backfill, and lifecycle mechanisms. [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md) develops distributed processing, streaming, serving, and analytical mechanisms used by insight systems.

[Security Engineering](../../25-security-engineering/ROADMAP.md) informs trust boundaries, authorization, audit, threat modeling, and control evidence. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes lifecycle, interface, authority, verification, validation, and safe feedback reasoning across people and technology.

## References

- John Mancini and AIIM, [*Systems of Record and Systems of Engagement — Initial Task Force Findings Released*](https://info.aiim.org/aiim-blog/newaiimo/2010/10/20/systems-of-record-and-systems-of-engagement), 2010. Primary industry context for the record/engagement distinction; framing rather than normative architecture law.
- Microsoft, [*CQRS Pattern*](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs), Azure Architecture Center, checked 2026-09-03. Official guidance on command/read-model separation, synchronization, materialized views, event sourcing, and trade-offs.
- W3C, [*PROV-Overview: An Overview of the PROV Family of Documents*](https://www.w3.org/TR/prov-overview/), W3C Working Group Note, 2013. Authoritative roadmap to interoperable provenance specifications for entities, activities, agents, derivation, and responsibility.
- W3C, [*Data Catalog Vocabulary (DCAT) — Version 3*](https://www.w3.org/TR/vocab-dcat-3/), W3C Recommendation, 2024. Normative distinction among conceptual datasets, distributions, services, series, and catalog records.
- NIST, [*Big Data Interoperability Framework: Volume 6, Reference Architecture, Version 3*](https://doi.org/10.6028/NIST.SP.1500-6r2), NIST SP 1500-6r2, 2019. Vendor-neutral provider, consumer, application, framework, orchestrator, management, and security/privacy roles.
- Martin Fowler, [*Event Sourcing*](https://martinfowler.com/eaaDev/EventSourcing.html), 2005. Primary pattern description of recording state changes as an event sequence, replay, temporal query, correction, and external update considerations.
- Microsoft, [*Materialized View Pattern*](https://learn.microsoft.com/en-us/azure/architecture/patterns/materialized-view), Azure Architecture Center, checked 2026-09-03. Official guidance on precomputed consumer-oriented views, update mechanisms, consistency, and applicability.
- IEEE, [*IEEE/ISO/IEC 42010-2022 — Architecture Description*](https://standards.ieee.org/ieee/42010/6846/), 2022. Official standard record for architecture-description concepts linking systems, concerns, viewpoints, views, and models.

## Exercises

### Exercise 1

Decompose “the CRM is our customer source of truth” into at least five fact-operation authority statements. Identify where the phrase remains ambiguous.

### Exercise 2

Design the command, event, and engagement states for an offline mobile delivery-address change. Include retry, expiry, rejection, correction, and user communication.

### Exercise 3

A warehouse publishes a churn score that automatically changes retention offers. Specify the insight, decision, and command records plus feedback risks and controls.

### Exercise 4

Compare direct queries and replicated projections for showing account status in a support console. Address availability, latency, authorization, staleness, correction, and incident behavior.

### Exercise 5

Create a dual-running authority plan for moving product-price maintenance from a legacy ERP to a product service. Include population, effective time, fencing, reconciliation, rollback, and retirement evidence.

## Answers to the Exercises

### Answer 1

Candidate statements are: the identity service accepts creation and merge of legal-party identities; CRM accepts support-channel profile changes; the consent service accepts purpose-specific marketing permissions; billing accepts billing-account status transitions; and the order service accepts the delivery address attached to an order version. Each statement must add population, jurisdiction, valid interval, operation, owner, correction, and contract. “Customer” remains ambiguous about party, account, profile, household, recipient, and historical versus current state. The architecture may preserve attributed competing claims for uncertain identity rather than falsely select one truth.

### Answer 2

The client records a pending intent with request identity, subject, proposed value, captured time, evidence, actor, expected version, and expiry. It displays `pending`, not `accepted`. On connection it submits an idempotent command. The order authority authenticates the actor, checks current version, policy, order state, address rules, and expiry, then emits accepted or rejected outcome. Retries reuse the request identity. A conflict returns current state and a safe resolution workflow. Accepted events update projections; rejection clears or preserves the draft with explanation. Later corrections are versioned and propagated. Telemetry and support procedures cover commands that remain indeterminate after timeout.

### Answer 3

The insight record names customer population, input snapshot and feature positions, model version, prediction time, score calibration and uncertainty, limitations, and intended retention decision. A separate decision record names the authorized policy, thresholds, eligibility, offer constraints, human or automated authority, explanation, and outcome. An idempotent command requests the offer change through the customer or offer authority, which revalidates state. Monitor disparate allocation, complaints, margin, opt-out, model unavailability, stale features, and override. Because offers affect behavior and future labels, preserve evaluation data and review selection bias; click or acceptance changes alone do not prove causal value.

### Answer 4

Direct query can provide current authoritative status and central authorization but couples the console to account-service availability, latency, load, and contract. A projection improves read isolation and local availability but needs event delivery, position, maximum staleness, classification, local access enforcement, correction, rebuild, and reconciliation. For high-consequence action, the console can display a positioned projection while the command boundary revalidates current status. During incidents, state whether stale display is labeled, whether operations are disabled, and which support override is authorized. Choose using task consequence and SLOs, not a universal preference.

### Answer 5

Partition products and operations explicitly. Before cutover, the ERP remains the only acceptor while the product service shadows changes and reconciles identifiers, prices, currencies, tax context, effective dates, approvals, and history. At a declared effective time or product partition, fence ERP writers and activate the new command path; do not rely on team convention. Record last accepted positions in both systems, reconcile counts and business invariants, monitor rejected and late writes, and preserve an authorized rollback window. Rollback defines reverse synchronization and fencing. Retirement requires migrated consumers, correction and audit access, policy and retention disposition, recovery evidence, no unauthorized old writes, and accountable approval.
