---
module_id: DE-076
program: Data Engineering
level: 2
module_number: 76
title: Data Contracts
status: complete
last_verified: 2026-09-03
---

# Data Contracts

## One-Page Review

### Governing question

How can producers and consumers turn a data interface into a durable, testable, evolvable agreement about identity, semantics, quality, service, governance, and change—without mistaking a schema document, catalog page, dashboard, or registry compatibility check for the whole contract?

### Essential definitions

- A **data contract** is a versioned agreement between accountable producers and identified consumers governing a data product/interface and the evidence required to use it safely.
- A **contract subject** is the stable product, dataset, stream, table, API, file family, or logical interface governed by the agreement.
- **Logical schema** expresses portable fields and types; **physical schema** expresses representation in a particular transport or engine.
- **Semantic identity** states grain, entity/event meaning, keys, field definitions, units, time semantics, null/default rules, and authoritative references.
- A **quality clause** specifies a falsifiable rule, population, threshold, severity, enforcement point, owner, and evidence.
- A **service-level objective** specifies availability, freshness, timeliness, retention, recovery, or support behavior for a measured population and window.
- A **compatibility policy** defines which producer and consumer versions may interoperate, in which direction, under which semantic equivalence.
- A **consumer obligation** states supported access, feedback, usage, security, migration, and acknowledgment duties; contracts are not producer-only promises.
- **Contract-as-code** stores machine-readable contract versions beside tests and change history while preserving human review and ownership.
- An **enforcement point** is where a clause is checked: authoring, CI, registry, ingestion, transformation, publication, serving, or continuous monitoring.
- A **contract instance/result** binds a contract version, data version, evaluator version, coverage, outcomes, and decision.
- A **breaking change** requires consumer migration or an explicitly negotiated new interface, even if a serialization registry calls it structurally compatible.
- A **waiver** is a scoped, owned, expiring exception with reason, risk, compensating control, and removal condition.
- **Deprecation** is the announced interval during which an old version remains supported while consumers migrate; **retirement** ends that support.
- A **contract ledger** preserves proposals, approvals, versions, checks, acknowledgments, incidents, waivers, deprecations, and retirement evidence.

### Central model, mechanism, or theorem

Let contract version $C_v$ contain identity/ownership $I_v$, semantic/schema clauses $S_v$, quality/service clauses $Q_v$, governance/use clauses $G_v$, and lifecycle/change protocol $L_v$:

$$
C_v=(I_v,S_v,Q_v,G_v,L_v).
$$

For data version $D_k$ and consumer profile $U_j$, safe publication requires applicable clause conformance, complete required coverage, and compatibility:

$$
Safe(C_v,D_k,U_j)\iff Conforms(C_v,D_k)\land Coverage=1\land Compatible(C_v,U_j).
$$

Structural compatibility is not semantic compatibility. A producer can preserve a required integer field named `amount` while changing its unit from cents to dollars. Shape and type checks pass, yet an old consumer divides by 100 and interprets 1,250 as USD 12.50 instead of USD 1,250.00. A complete contract makes unit semantics and migration part of compatibility.

### Critical invariants

- Every contract has stable subject identity, contract/spec versions, lifecycle status, environment/endpoints, producer owner, steward, support channel, and identified consumer classes.
- Grain, keys, entity/event meaning, field semantics, units, currency, time, presence/null/default, and reference vocabularies are explicit and versioned.
- Logical and physical types remain distinct; format-specific compatibility never substitutes for business-semantic equivalence.
- Quality and service clauses name populations, metrics, thresholds, windows, severity, coverage, evidence, and enforcement response.
- Security classification, permitted purpose, access, residency, retention, deletion, masking, and audit obligations travel with the interface.
- Contract changes are reviewed as diffs and classified against actual consumer profiles, not a universal major/minor label alone.
- Producer and consumer versions are independently identifiable; mixed deployments and historical/backfill compatibility are tested.
- A passing contract result binds pinned contract, data, transformation/reference, evaluator, and environment versions.
- Required clauses that cannot be evaluated yield unknown/failure under policy, never implicit conformance.
- Enforcement occurs before irreversible publication where feasible and continuously where properties can drift after release.
- Backward/forward/full compatibility directions are named, and semantic fixtures exercise supported producer-consumer pairs.
- Breaking changes use additive replacement, parallel versioning, dual write/read, translation, or coordinated cutover with rollback.
- Deprecation lists affected consumers, notification/acknowledgment, support end, telemetry, migration evidence, and retirement gate.
- Waivers cannot mutate history or become silent defaults; they expire and retain risk ownership.
- Contract success is measured through adoption, detection, incident reduction, migration health, and consumer outcomes—not document count.

### Common failures

Common failures include calling an inferred schema a contract; copying field names without grain or units; assuming backward schema compatibility means semantic safety; writing “fresh daily” without timezone, population, or deadline; declaring owners who cannot approve changes; omitting consumer obligations; testing only example rows; checking only new writes while historical data remains incompatible; publishing before contract results commit; treating registry acceptance as consumer acknowledgment; changing defaults or enum meaning without a type change; placing sensitive data rules only in prose; granting permanent waivers; versioning the file but not the subject or evaluator; allowing incompatible contract dialects to share one label; and retiring an interface because no dashboard traffic was observed despite uninstrumented consumers.

### Compact example

Contract C7 defines `amount` as a required integer in cents. Producer version P8 keeps the same field name and integer type but changes the unit to dollars. A shape/type compatibility check passes. An existing consumer divides the value 1250 by 100 and reports USD 12.50, although the producer intended USD 1,250.00. C7 therefore rejects publication to that consumer profile. A safe migration adds a new explicitly named/unit-tagged field or version, dual-publishes, validates semantic fixtures, observes acknowledgment, then deprecates the old representation.

### Connections

[DE-008](008-schemas-nullability-and-type-fidelity.md) establishes schema evolution, [DE-023](023-file-arrival-and-manifest-processing.md) supplies delivery evidence, [DE-049](049-run-metadata-and-operational-state.md) binds executions, [DE-066](066-time-travel-and-reproducible-reads.md) pins versions, [DE-071](071-completeness-validity-accuracy-and-consistency.md), [DE-072](072-schema-and-constraint-tests.md), [DE-073](073-reconciliation-tests.md), [DE-074](074-freshness-and-timeliness.md), and [DE-075](075-volume-and-distribution-monitoring.md) supply enforceable quality/service clauses. DE-077 assigns producer and consumer responsibilities.

## Governing Question

Data crosses an organizational boundary whenever one team makes a representation that another team relies on. The technical transport may be a table, topic, file, feature view, API, or report. The durable problem is the same: what is promised, to whom, under which meaning and limits, how is it verified, and how can it change without surprise?

A schema answers only part of that question. It may say `amount` is an integer but omit currency and scale; say `timestamp` but omit event versus processing time; say `customer_id` but omit grain, uniqueness, deletion, or pseudonymization. A registry can accept a wire-compatible change that violates downstream business logic.

A contract is also not a wish list. “High quality,” “near real time,” or “owner: data team” cannot be tested or operationalized. Each normative clause needs a measurable subject, scope, owner, enforcement point, and failure action. Descriptive documentation and examples help humans, but they must not be confused with enforceable guarantees.

The governing requirement is a living interface with a controlled lifecycle. Producers, consumers, platform, governance, and operations need one versioned source of truth, evidence from actual data and deployments, a change negotiation protocol, and a retirement mechanism that does not strand invisible consumers.

## Why This Matters

Without contracts, dependencies are discovered through incidents. Producers infer which columns matter from query logs; consumers reverse-engineer nulls and timing; owners debate whether a change was “breaking” after production fails. Local success metrics reward delivery while external costs remain hidden.

Contracts make assumptions reviewable before they become coupling. Stable IDs, grain, semantics, and objectives let tools detect many changes early. Consumer profiles and fixtures reveal compatibility beyond syntax. Ownership and support clauses shorten diagnosis when automation cannot decide.

Overly broad contracts create a different failure. If every observed detail becomes guaranteed, evolution freezes and enforcement becomes noisy. Contracts should protect deliberate public semantics and service outcomes, while labeling implementation details, previews, and non-guarantees.

Contracts connect governance to execution. Classification and permitted use affect access; retention and deletion affect storage; quality and freshness affect publication; lineage identifies impact; deprecation telemetry governs retirement. A catalog page that is disconnected from these controls becomes stale commentary.

The artifact itself can reveal sensitive endpoints, classifications, internal owners, or operational thresholds. Access, distribution, signing, and retention of contracts and evidence must match their risk while still allowing consumers to discover relevant terms.

## Prerequisites and Retrieval

Retrieve subject: stable product/dataset/stream/table identity, domain, purpose, intended and prohibited uses, environment, endpoints, formats, lifecycle status, and authoritative definitions.

Retrieve parties: accountable producer, technical owner, business steward, security/privacy roles, support/on-call, known consumers, consumer classes, criticality, acknowledgments, and escalation.

Retrieve semantics: entity/event, grain, keys, relationships, field IDs/names, definitions, logical/physical types, units/currency, timezone/time meaning, presence/null/default, enumerations, reference versions, ordering, duplicates, updates/deletes, and examples.

Retrieve delivery: access protocol, partitioning, version/snapshot, manifest/checkpoint, cadence, expected intervals, availability/freshness/timeliness, retention, recovery, replay/backfill, outage communication, and service windows.

Retrieve quality: schemas, constraints, expected populations, completeness, validity, accuracy, consistency, reconciliation, volume/distribution, thresholds, severity, tolerances, coverage, quarantine, and evidence.

Retrieve governance: classification, permitted purpose, license, access control, minimization, residency, encryption, masking, retention/deletion, legal hold, audit, sharing, and derived-data obligations.

Retrieve compatibility: current producer and consumer versions, registry modes, readers/writers, historical data, default/presence behavior, semantic fixtures, supported matrices, transformations, deployment order, and rollback.

Retrieve lifecycle: proposal/approval authority, review workflow, semantic version rules, effective date, notification, acknowledgment, migration support, parallel-run duration, deprecation, retirement, waivers, and ledger.

Retrieve enforcement: contract dialect/schema, parser/CLI/registry versions, CI gates, runtime tests, publication gate, continuous monitors, coverage, failure semantics, evidence store, signing/provenance, and control owner.

Distinguish standard version from contract version; contract identity from physical location; logical from physical type; documentation from obligation; producer assertion from independently observed evidence; schema compatibility from semantic compatibility; compatibility from consumer readiness; data SLO from compute SLA; proposed from active; deprecated from retired; exception from contract revision; and discovered consumer from unobserved consumer.

Create a contract inventory:

| Layer | Required content and evidence |
|---|---|
| Identity | Stable IDs, names, versions, status, domain, purpose, endpoints |
| Parties | Producer, steward, consumers, support, escalation and approvals |
| Semantics | Grain, keys, fields, units, time, null/default, references, mutations |
| Quality | Rules, populations, thresholds, severity, coverage and results |
| Service | Availability, freshness, deadlines, retention, recovery and support |
| Governance | Classification, use, access, residency, retention/deletion and audit |
| Compatibility | Direction, version matrix, fixtures, historical/backfill and rollout |
| Lifecycle | Proposal, activation, change, waiver, deprecation and retirement |
| Evidence | Data/contract/evaluator versions, results, acknowledgments and ledger |

Write a falsifiable claim: “Contract C12 for order-events v3 is active for producers P8–P9 and acknowledged consumer profiles U17/U22; each event is one immutable order transition keyed by `(order_id,event_id)`, amounts are decimal EUR minor units, timestamps are UTC event instants, deletes are tombstones, critical schema/key/domain/reconciliation checks cover every committed partition, 99.9% publish within ten minutes, confidential fields are purpose-limited and retained 30 days, backward semantic fixtures pass for the declared matrix, and v2 remains available until all registered consumers demonstrate migration or the approved 2026-12-01 retirement gate is met.”

## Learning Objectives

After completing this module, you should be able to:

1. distinguish a complete data contract from schema, documentation, SLA, or registry policy alone;
2. define stable subject identity, parties, purpose, grain, keys, semantics, and physical representations;
3. express quality, freshness, availability, retention, recovery, and support clauses as measurable obligations;
4. encode security, privacy, use, residency, deletion, and derived-data obligations;
5. map each normative clause to enforcement points, coverage, evidence, and failure action;
6. evaluate structural, wire, semantic, historical, and consumer-specific compatibility;
7. version contracts, data, transformations, references, evaluators, and consumer profiles independently;
8. design additive, parallel, dual-read/write, translation, deprecation, and rollback migrations;
9. govern proposals, approvals, acknowledgments, waivers, disputes, and retirement; and
10. measure adoption and outcomes without rewarding empty documents or untested clauses.

## Core Exposition

### Define the subject and parties

Give the contract and governed interface stable IDs. Names and physical locations change; IDs preserve lineage. Separate the contract-standard version, contract revision, product/interface version, producer implementation, and physical endpoint.

State purpose, intended consumers, supported uses, prohibited uses, limitations, and non-guarantees. The public surface should be narrow enough to evolve. Mark experimental fields and best-effort objectives explicitly rather than allowing examples to become accidental promises.

Assign accountable roles, not group aliases alone. The producer owns creation and supported semantics; a steward may own definitions/policy; platform owns enforcement infrastructure; consumers own declared use, version compatibility, and migration. List support and escalation with service windows.

Discover consumers through registration, access grants, lineage, query/topic subscription telemetry, and owner attestations. Each source is incomplete. Unknown consumers are a risk state, not evidence that retirement is safe.

### Specify semantics before syntax

Define one row/message/file's grain and business identity. State uniqueness, ordering, duplicates, updates, corrections, deletes/tombstones, late data, snapshot versus event semantics, and relationship cardinalities. Without grain, even correct field definitions remain ambiguous.

For every governed field, record stable field ID where supported, name, authoritative definition, logical and physical types, presence, null/default/empty meaning, unit/scale/currency, timezone and time role, allowed values, precision, sensitivity, examples, and lifecycle status.

Defaults are behavior. Writer omission, explicit null, reader-supplied default, producer-derived default, and unknown sentinel differ. Enumeration additions may be wire-compatible yet break exhaustive consumers. Unit or definition changes usually require a new semantic identity even if bits stay identical.

Separate portable logical semantics from server-specific representations. An instant may be Avro logical timestamp, SQL timestamptz, protobuf timestamp, or integer epoch. Contract fixtures should prove equivalent boundary behavior across supported encodings.

### Make quality and service clauses executable

Each clause states subject, population, predicate/metric, threshold, severity, enforcement point, evaluator version, evidence, owner, and response. “No duplicates” needs key and population; “99% complete” needs expected set, denominator, window, and critical-cohort policy.

Compose schema/constraint, completeness/accuracy/consistency, reconciliation, freshness/timeliness, and volume/distribution clauses. Preserve their distinctions. A fresh dataset may be wrong; a conforming dataset may be incomplete; a stable distribution may hide exact loss.

Service clauses identify consumer-visible outcomes. Availability says which endpoint/version is usable and how observed. Freshness identifies frontier and clock. Timeliness identifies expected interval and deadline. Retention identifies retrievable versions. Recovery identifies objectives, restore semantics, and validation.

Map clauses to controls. Lint contract syntax at authoring; compare revisions in CI; enforce compatible schemas at registry/write; validate data before atomic publication; continuously observe freshness and drift; periodically audit access, retention, and consumers. One gate rarely covers all properties.

### Encode governance and use

Classification belongs at product and field levels with inheritance/override rules. Link purposes, roles, access, masking/tokenization, encryption, residency, sharing, and audit. A public schema does not grant data access.

Retention includes raw, published, backups, caches, contract evidence, and derived products. Define deletion propagation, legal holds, and proof. Consumer obligations may require downstream retention/deletion, access review, incident notification, and prohibition on reidentification.

Contract tests must minimize sensitive samples. Prefer counts, protected digests, synthetic fixtures, and controlled quarantine references. Permissions for contract metadata and evidence may differ from permissions for row data.

Use authoritative definitions and policy IDs rather than duplicating mutable prose. Pin the referenced version/effective time so historical contracts remain interpretable.

### Evaluate compatibility as a relation

Compatibility is directional among writer, stored, reader, semantic, and contract versions. Define backward, forward, or full precisely for the chosen format. Then add semantic compatibility: does the new producer preserve the meaning and invariants expected by consumer profile $U_j$?

Build a matrix of supported producer-contract-consumer combinations. Test real or synthetic boundary fixtures: absent/null/default, numeric extremes, timezone/DST, Unicode, unknown enum, extra/missing field, reordered collections, duplicates, deletes, and historical records.

Schema-registry acceptance is one signal. It does not know arbitrary units, joins, expectations, latency, access, or consumer algorithms. Likewise, a consumer-driven fixture suite covers known cases, not every real-world property. Combine structural rules, semantic invariants, and observed canary/shadow evidence.

Classify changes per consumer: documentation-only, operationally compatible, additive with dormant risk, conditionally compatible, migration-required, or forbidden. The same change may be safe for one projection and breaking for another.

### Govern change and deployment

Represent a proposal as a diff with rationale, affected clauses, lineage impact, compatibility results, consumer list, risk, rollout, observability, rollback, effective date, and approvers. Machine diff finds structural changes; humans review semantic and policy changes.

Prefer expand-and-contract: add new field/interface, dual publish or translate, update consumers, observe parity, stop old writes, retain rollback, deprecate, then retire. Avoid changing meaning in place. Translation becomes a governed producer with its own tests and ownership.

Deployment order follows compatibility. A backward-compatible new reader may deploy before producer; an additive writer may wait for old-reader proof; a breaking change uses parallel versions. Historical/backfill writers must obey the version they emit, not only current code.

Activate a contract only when syntax, references, required tests, ownership, enforcement readiness, and approvals pass. Contract file merge is not production activation. Tie active contract IDs to endpoints and emitted data.

### Handle failure, waiver, and retirement

Contract evaluation states include pass, fail, pending, unknown, waived, and not-applicable. Store counts and coverage. A test crash or missing partition is unknown. A waiver wraps a known failure; it does not rewrite it as pass.

Waivers name exact clause, product/version/population, reason, risk owner, consumer impact, compensating control, start/expiry, review, and removal. Alert before expiry. Repeated waivers signal an unrealistic contract or unmanaged defect and require decision, not automatic renewal.

On breach, preserve versions/evidence; contain publication or serve labeled last-known-good according to policy; identify affected consumers; correct or replay; publish a new version; rerun checks; and communicate. Do not erase the failed instance.

Deprecation begins with alternative, migration guide, dates, support, consumer notification and acknowledgment, and usage telemetry. Retirement requires no supported consumer dependency, retention/legal checks, rollback/archive plan, access revocation, and owner approval. Lack of observed traffic is insufficient if observability is incomplete.

### Operate a contract platform without theater

Provide templates and standard vocabulary but allow typed extensions. Validate dialect/version explicitly. Generate catalog views, schemas, tests, policies, and lineage integrations from one canonical source where possible; label generated versus authoritative fields.

Store immutable contract revisions and signed/provenanced results. Query which data versions conformed to which contract and which consumers were supported. Monitor evaluator and enforcement coverage as carefully as clause outcomes.

Measure active contracts with identified owners/consumers, clauses actually enforced, evaluation coverage, preproduction break detection, escaped incidents, time to notify/migrate, waiver age, deprecated usage, false blocks, and consumer satisfaction. Raw contract count is a vanity metric.

Federate ownership with minimum interoperability: stable IDs, lifecycle states, change events, shared types/semantics, result schema, and escalation. Central bottlenecks invite bypass; ungoverned local dialects destroy portability.

## Definitions and Notation

Let:

- $C_v=(I_v,S_v,Q_v,G_v,L_v)$ be contract version $v$;
- $D_k$ be pinned data version $k$;
- $P_i$ and $U_j$ be producer implementation/profile $i$ and consumer profile $j$;
- $A(C_v)$ be applicable normative clauses;
- $Eval(a,D_k,E_m)$ be clause $a$ evaluated by engine/version $E_m$;
- $Pass(a,D_k)$ be a successful result under declared threshold;
- $Cov(a,D_k)$ be evaluated divided by intended coverage;
- $Compat(P_i,C_v,U_j)$ be declared structural and semantic compatibility; and
- $W_a$ be an optional scoped waiver attached to clause result $a$.

Contract conformance for a data version is

$$
Conforms(C_v,D_k)\iff \bigwedge_{a\in A(C_v)}Pass(a,D_k)\land Cov(a,D_k)=1,
$$

for clauses requiring complete coverage. A waiver changes the release decision under policy, not the underlying predicate:

$$
ReleaseAllowed=(Conforms\lor ApprovedWaiver)\land Compat\land GovernanceGate,
$$

while evidence continues to record the failed clause. Compatibility is not assumed transitive across semantic versions: $Compat(P_1,C_1,U)$ and $Compat(P_2,C_2,U)$ do not imply $Compat(P_2,C_1,U)$ or safe mixed data.

## Mechanisms, Invariants, or Proof Structure

Proof sketch that structural compatibility does not imply semantic compatibility:

1. Let contract C1 define required field `amount` with physical/logical type integer and semantic unit cents.
2. Consumer U1 accepts the field/name/type and computes displayed dollars as `amount / 100`.
3. Producer P2 emits the same required integer field, so shape and primitive-type checks pass.
4. P2 changes the semantic unit to dollars without changing the field identity or representation.
5. For emitted integer 1250, U1 displays USD 12.50 while P2 means USD 1,250.00.
6. Therefore structural shape/type compatibility does not imply preservation of consumer semantics.
7. Unit identity, semantic fixtures, version negotiation, and migration are independent contract obligations.

The counterexample does not diminish schema registries: they efficiently protect declared structural/wire rules. It establishes the boundary beyond which semantic and organizational evidence is required.

The executable reproduces the unchanged schema, semantic mismatch, unsafe release, and repaired unit agreement. It is a deterministic teaching abstraction, not an ODCS validator, schema registry, decimal/currency library, contract platform, or deployment controller.

<!-- bijux-verify: {"id":"semantic-contract-gate","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"schema_shape_match=True\nschema_type_match=True\nproducer_unit=dollars\nconsumer_unit=cents\nsemantic_contract_match=False\nconsumer_interpreted_dollars=12.50\nactual_dollars=1250.00\nsafe_to_publish=False\nrepaired_safe_to_publish=True\n","stderr":""}} -->
```python
from decimal import Decimal

field_name = "amount"
field_type = int
producer_unit = "dollars"
consumer_unit = "cents"
payload = {"amount": 1250}

shape_match = set(payload) == {field_name}
type_match = isinstance(payload[field_name], field_type)
semantic_match = producer_unit == consumer_unit
consumer_value = Decimal(payload[field_name]) / Decimal(100)
actual_value = Decimal(payload[field_name])

print(f"schema_shape_match={shape_match}")
print(f"schema_type_match={type_match}")
print(f"producer_unit={producer_unit}")
print(f"consumer_unit={consumer_unit}")
print(f"semantic_contract_match={semantic_match}")
print(f"consumer_interpreted_dollars={consumer_value:.2f}")
print(f"actual_dollars={actual_value:.2f}")
print(f"safe_to_publish={shape_match and type_match and semantic_match}")

repaired_producer_unit = "cents"
print(f"repaired_safe_to_publish={shape_match and type_match and repaired_producer_unit == consumer_unit}")
```

## Alternatives and Trade-Offs

1. **Central standard versus domain extensions:** common structure improves interoperability; typed extensions preserve domain meaning but need namespaces and governance.
2. **One canonical contract versus generated views:** one source reduces drift; generated schemas/tests/catalogs can lose unsupported semantics and require provenance.
3. **Producer-defined versus consumer-driven clauses:** producers understand source feasibility; consumers reveal actual risk. Durable contracts require negotiated authority.
4. **Strict enforcement versus advisory adoption:** strict gates prevent escape but can block immature products; advisory rollout needs deadlines and coverage visibility.
5. **Registry-time versus publication-time enforcement:** early checks are fast; data-dependent and service clauses require runtime evidence.
6. **Backward compatibility versus parallel version:** backward evolution reduces migration cost; parallel versions isolate breaking semantics at operational expense.
7. **Dual write versus translation:** dual write keeps producer control but risks divergence; translation centralizes compatibility while creating another owned pipeline.
8. **Known-consumer acknowledgment versus time-based deprecation:** acknowledgment protects critical users; deadlines prevent indefinite support but need discovery confidence.
9. **Fine-grained clauses versus simple contracts:** precision improves enforcement and diagnosis; excessive detail can guarantee implementation accidents.
10. **Fail closed versus labeled degraded service:** holding protects critical decisions; last-known-good maintains availability for consumers that accept staleness.
11. **Contract revision versus waiver:** revision admits a durable expectation change; waiver retains a temporary known deviation and risk.
12. **Open metadata versus restricted evidence:** discoverability enables safe use; sensitive endpoints, classifications, and samples require layered access.

## Failure Modes and Misconceptions

- **“A schema is the data contract.”** It omits many semantic, quality, service, governance, and lifecycle obligations.
- **“The catalog page is authoritative.”** Only if versioned and connected to actual enforcement/evidence.
- **“Registry-compatible means consumer-safe.”** Wire compatibility cannot prove unit, meaning, quality, or algorithm compatibility.
- **“Additive fields never break readers.”** Strict decoders, projections, costs, privacy, defaults, and exhaustive logic can break.
- **“Renaming with an alias preserves meaning.”** Identity mapping does not prove semantic equivalence.
- **“Same type means same field.”** Units, scale, time role, domain, and authority may change.
- **“Documentation-only changes are harmless.”** Correcting a definition can reveal that implementations were never aligned.
- **“Semantic version numbers decide impact.”** Impact is a relation to actual consumer behavior and deployment.
- **“The producer owns every term.”** Consumer obligations and negotiated risk are part of the interface.
- **“Consumers can remain anonymous.”** Unknown consumers make change and retirement risk unknowable.
- **“Query logs find all consumers.”** Caches, exports, service accounts, dormant jobs, and indirect derivatives evade them.
- **“Contract merge activates the change.”** Production activation requires enforcement and endpoint/data linkage.
- **“A passing sample certifies the dataset.”** Coverage and population determine the claim.
- **“Tests that crashed can be ignored.”** Required unknown evidence cannot become conformance.
- **“Runtime checks alone are enough.”** Security/use and deployment compatibility require additional controls.
- **“CI alone enforces data quality.”** Historical/current data and service behavior need runtime evaluation.
- **“Freshness belongs to the scheduler.”** It is a consumer-visible data property with frontier and population semantics.
- **“Availability means the endpoint responds.”** The promised version may still be stale, invalid, or inaccessible to consumers.
- **“Retention means storage TTL.”** Backups, caches, derived data, deletion, legal hold, and retrieval are involved.
- **“Classification grants access.”** Classification informs policy; explicit authorization still governs access.
- **“A waiver is a pass.”** It is a recorded policy exception around a retained failure.
- **“Waivers can be open-ended.”** Permanent exceptions are unmanaged contract changes or defects.
- **“Breaking changes require synchronized deployment.”** Parallel/expand-contract designs reduce atomic organizational coordination.
- **“Dual writes prove parity.”** They require independent reconciliation and failure handling.
- **“Historical data need not comply.”** Readers, backfills, replay, and retention define supported historical contracts.
- **“One consumer fixture proves all semantics.”** Fixtures cover declared cases and profiles, not arbitrary future behavior.
- **“No complaints mean success.”** Consumers may be unaware, silently compensating, or unable to identify owners.
- **“Deprecation is an email.”** It needs alternatives, dates, acknowledgments, telemetry, support, and a retirement gate.
- **“No traffic means safe retirement.”** Observability may be incomplete and dormant critical consumers may exist.
- **“More contracts mean maturity.”** Enforced coverage and improved outcomes matter; document counts invite theater.

## Worked Examples

### Example 1

An orders table contract declares one current row per order, stable UUID key, EUR decimal amount, UTC update instant, tombstone retention, 06:00 publication, critical reconciliation, confidential customer field, and a support owner. Its SQL schema is generated from—but cannot represent all of—the canonical contract.

### Example 2

An Avro field addition has a reader default and passes registry backward checks. A legacy consumer rejects unknown JSON fields after an intermediate conversion. The consumer matrix and end-to-end fixture classify the change as unsafe for that path until the converter is fixed.

### Example 3

An enum adds `REFUNDED`. Binary readers preserve the unknown number, but a consumer's exhaustive business switch maps it to failure. A semantic fixture and registered profile catch the break despite wire compatibility.

### Example 4

A daily file contract includes expected partition calendar, zero-row manifest, schema digest, source cut, control totals, freshness deadline, retention, and replay. The file's presence alone cannot satisfy the contract.

### Example 5

A privacy contract marks email restricted to fraud operations, tokenized for analytics, retained 30 days, and deletion-propagated to derivatives. Schema validation passes a plaintext email, but the governance gate rejects the unauthorized endpoint.

### Example 6

A producer proposes changing event timestamp from occurrence to processing time. Physical type remains timestamp. The semantic diff marks it breaking; a new field is added, both are emitted, consumers migrate, and old semantics are retired after acknowledgment.

### Example 7

A quality rule is waived for one source/date range during a documented upstream outage. The result remains failed-with-waiver, compensating reconciliation runs daily, and expiry pages the risk owner. Other sources and future intervals remain enforced.

### Example 8

A consumer has not queried for 60 days but owns a quarterly regulatory job. Registry and access registration identify it despite dormant telemetry, preventing premature retirement.

### Example 9

A contract platform reports 500 YAML files but only 120 active endpoints and 80 with recent complete results. Maturity reporting uses active ownership, enforcement coverage, escaped incidents, and migration outcomes rather than file count.

### Example 10

A translation service preserves v1 while producer v2 changes normalized entities. It receives its own contract, lineage, capacity/freshness objectives, semantic fixtures, reconciliation, and retirement plan; it is not treated as invisible compatibility glue.

## Cross-Program Connections

- **API and Service Engineering:** OpenAPI/AsyncAPI, consumer-driven contracts, version negotiation, compatibility, deprecation, error models, and SLOs parallel data interfaces.
- **Software Engineering:** type systems, design by contract, semantic versioning, fixtures, CI, code review, feature flags, and expand-contract migrations support lifecycle.
- **Distributed Systems:** mixed versions, eventual consistency, partial deployment, retries, ordering, clocks, and partition failure constrain enforcement.
- **Platform Engineering:** registries, catalogs, policy engines, lineage, test runners, evidence stores, templates, and developer workflows scale contracts.
- **Security Engineering:** classification, least privilege, integrity/signing, key management, audit, incident response, and supply-chain trust govern artifacts.
- **Privacy Engineering:** purpose limitation, minimization, consent, residency, retention/deletion, derived data, and data-subject rights become clauses.
- **Reliability Engineering:** SLIs/SLOs, error budgets, last-known-good, support, on-call, recovery, waivers, and incidents operationalize promises.
- **Product Management:** consumers, value, usability, roadmap, launch, adoption, deprecation, support cost, and feedback define viable interfaces.
- **Formal Methods:** preconditions, postconditions, invariants, refinement, temporal properties, proof obligations, and counterexamples clarify claims.
- **Organizational Design:** ownership, decision rights, negotiation, federation, incentives, escalation, and accountability decide whether contracts live.

## References

1. Bitol. [Open Data Contract Standard repository](https://github.com/bitol-io/open-data-contract-standard). Accessed 2026-09-03. Primary specification project for contract identity, schema, quality, service levels, roles, support, servers, and extensions.
2. Bitol. [ODCS fundamentals](https://github.com/bitol-io/open-data-contract-standard/blob/main/docs/fundamentals.md). Accessed 2026-09-03. Primary current documentation for standard version, contract identity/version/status, domain, purpose, limitations, usage, tags, and authoritative definitions.
3. Data Contract CLI. [Open Data Contract Standard](https://docs.datacontract.com/open-data-contract-standard). Accessed 2026-09-03. Primary tool documentation for ODCS structure, logical/physical types, linting, comparison, import, testing, and supported versions.
4. dbt Labs. [Model contracts](https://docs.getdbt.com/docs/mesh/govern/model-contracts). Accessed 2026-09-03. Primary documentation for enforced model names/types/constraints, preflight checks, platform behavior, and breaking-change considerations.
5. Confluent. [Schema evolution and compatibility](https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html). Accessed 2026-09-03. Primary documentation for backward, forward, full, transitive, and format-specific compatibility behavior.
6. Apache Avro. [Specification](https://avro.apache.org/docs/current/specification/). Accessed 2026-09-03. Primary specification for schemas, logical types, defaults, aliases, and writer-reader resolution.
7. Protocol Buffers. [Updating a message type](https://protobuf.dev/programming-guides/proto3/#updating). Accessed 2026-09-03. Primary guidance for field-number preservation, compatible type changes, unknown fields, enum evolution, and JSON risks.
8. JSON Schema. [Draft 2020-12 specification](https://json-schema.org/draft/2020-12). Accessed 2026-09-03. Primary specification bundle for structural assertion, annotation, vocabularies, and validation dialects.
9. OpenAPI Initiative. [OpenAPI Specification](https://spec.openapis.org/oas/latest.html). Accessed 2026-09-03. Primary interface specification for machine-readable operations, schemas, security, examples, and compatibility-relevant behavior.
10. AsyncAPI Initiative. [AsyncAPI Specification](https://www.asyncapi.com/docs/reference/specification/latest). Accessed 2026-09-03. Primary specification for event-driven channels, operations, messages, schemas, servers, security, and bindings.
11. Great Expectations. [Data quality use cases](https://docs.greatexpectations.io/docs/reference/learn/data_quality_use_cases/dq_use_cases_lp/). Accessed 2026-09-03. Primary documentation for executable distribution, freshness, integrity, missingness, schema, uniqueness, and volume checks.
12. OpenLineage. [Object model](https://openlineage.io/docs/spec/object-model/). Accessed 2026-09-03. Primary specification documentation for job/run/dataset identity, versions, lifecycle events, lineage, and extensible facets.
13. Semantic Versioning. [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html). Accessed 2026-09-03. Primary specification for public API versions, compatibility-signaling increments, prereleases, and immutability.
14. UK Government Data Quality Hub. [The Government Data Quality Framework](https://www.gov.uk/government/publications/the-government-data-quality-framework/the-government-data-quality-framework). Accessed 2026-09-03. Primary framework for ownership, user needs, quality dimensions, lifecycle controls, communication, and improvement.

## Exercises

### Exercise 1

Design a complete contract for an order-events topic consumed by billing, fraud, analytics, and customer support. Include identity, parties, grain, keys, mutation/order, schema/semantics, quality/service, governance, compatibility matrix, enforcement, and support.

### Exercise 2

Evaluate a proposed integer field unit change, enum addition, nullable-to-required change, tighter freshness SLO, and shorter retention. Classify each for three different consumers and design safe migration/deployment/rollback.

### Exercise 3

Map a contract-as-code implementation across authoring, CI, schema registry, ingestion, transformation, publication, catalog/lineage, continuous monitoring, evidence, and policy enforcement. State failure and coverage semantics.

### Exercise 4

Design a waiver and incident workflow for a critical completeness breach during an upstream outage. Include scope, evidence, risk, compensating controls, publication, communication, expiry, correction, revalidation, and recurrence.

### Exercise 5

Create a deprecation and retirement plan for a table with incomplete consumer discovery, quarterly jobs, extracts, caches, and derived products. Include alternative, telemetry, registration, acknowledgment, dates, archive, rollback, and proof.

## Answers to the Exercises

### Answer 1

Assign stable contract/topic/event IDs, active version/status, domain/purpose/limits, producer/steward/on-call, and registered consumer profiles. Define one immutable transition per `(order_id,event_id)`, partition/order rules, deduplication, corrections and tombstones. Specify every field's stable ID, presence/null/default, logical/physical type, unit/currency, event/commit times, enum/reference version, sensitivity, and examples. Add schema/key/domain/reconciliation/coverage rules, per-consumer freshness/availability/retention/replay objectives, purpose/access/masking/deletion/audit clauses, writer-reader-semantic matrix with boundary fixtures, preproduction/publication/continuous controls, versioned evidence, change approvals, support, waiver, and deprecation protocol.

### Answer 2

The unit change is semantic-breaking for every amount user despite identical type: add an explicit new field/version and dual publish. Enum addition may be safe for a pass-through consumer, breaking for exhaustive billing, and ignorable for an analytics projection; test unknown handling. Nullable-to-required is safe for new writers only if old stored records/readers and backfills remain supported or migrated. A tighter freshness SLO changes an operational promise and capacity/on-call cost even without schema impact; canary and negotiate effective date. Shorter retention breaks quarterly replay and compliance consumers unless archives/alternatives satisfy them. Build per-consumer matrix, deploy tolerant readers first, observe parity/acknowledgment, retain rollback, then stop/deprecate old output.

### Answer 3

Keep a canonical versioned contract with explicit dialect. Authoring validates syntax/references and ownership; CI diffs semantics, classifies change, runs schema and consumer fixtures; registry enforces chosen wire direction; ingestion binds writer/contract/data identity; transformations test grain/keys/quality and propagate classification/lineage; publication atomically binds complete results and version; catalog renders discoverable terms; continuous monitors enforce freshness/availability/drift; policy engines apply access/retention/deletion; evidence storage preserves evaluator, coverage, outcomes and decisions. Required evaluation failure is unknown and blocks according to severity. Generated views carry source/digest and never silently omit unsupported normative clauses.

### Answer 4

Preserve failed contract/data/evaluator versions and exact missing population. The waiver names the completeness clause, source and intervals, consumers, business risk, risk owner/approver, expiry, and removal condition. Compensating controls reconcile source manifests daily, serve a labeled last-known-good or hold critical consumers, restrict decisions, and notify owners with affected versions. Correct upstream cause, replay idempotently from pinned raw evidence, publish a new version, rerun completeness plus schema/reconciliation/freshness and unaffected controls, support downstream replay, and leave the original failure-with-waiver immutable. Alert before expiry and review recurrence; repeated need triggers contract feasibility or source-control redesign.

### Answer 5

Publish replacement contract/version, semantic mapping, migration guide, parity fixtures, support channel, earliest deprecation and retirement dates, archive/retention and rollback. Combine registration/access grants, lineage, query/topic logs, extract inventories, service owners, and attestations; label discovery coverage. Contact and obtain acknowledgment from critical owners including quarterly schedules; instrument old-version reads and derived refreshes; run both versions through at least the longest usage cycle. Retirement gate requires migrated/approved consumers, zero unexplained use, completed cache/extract/derived-data plan, legal/retention checks, archived contract/data needed for audit, access revocation plan, rollback window, and accountable approval. Missing telemetry delays or explicitly escalates risk—it does not prove absence.
