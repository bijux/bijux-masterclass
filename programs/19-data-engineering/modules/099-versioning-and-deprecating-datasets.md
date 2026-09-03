---
module_id: DE-099
program: Data Engineering
level: 2
module_number: 99
title: Versioning and Deprecating Datasets
status: complete
last_verified: 2026-09-03
---

# Versioning and Deprecating Datasets

## One-Page Review

### Governing question

How can a producer change a shared dataset’s structure, meaning, behavior, policy, and delivery while consumers migrate deliberately and evidence—not hope or a calendar—determines when an old contract may be retired?

### Essential definitions

- A **dataset identity** names the enduring product concept; a **dataset version** names an immutable or durably specified consumer contract within that concept.
- A **state version** identifies a particular materialized snapshot or transaction state. Many state versions may conform to one contract version.
- An **implementation version** identifies code, configuration, runtime, and dependencies used to produce state. It need not be visible as a consumer contract version.
- A **contract** specifies structural, semantic, quality, temporal, policy, delivery, and support promises at a named boundary.
- A **compatible change** preserves a declared consumer’s valid use and required observations within the contract; compatibility is directional, scoped, and consumer-dependent.
- A **breaking change** makes at least one supported use invalid or materially changes its promised result, side effects, timing, policy, or interpretation without an accepted migration.
- A **current/latest alias** is a mutable pointer to a selected supported version. It is convenient discovery, not an immutable identifier.
- A **version pin** binds a consumer to a named contract version; it improves reproducibility but transfers upgrade responsibility to that consumer.
- **Deprecation** announces that use remains possible but migration should begin and future behavior/support may change under policy.
- **Sunset** is the planned end of service for a deprecated version; **retirement** is the completed removal after gates pass.
- A **migration window** is the interval in which old and replacement contracts coexist with documented mapping, validation, support, and deadlines.
- A **consumer inventory** joins declared ownership, lineage, access/query telemetry, exports, cached copies, and acknowledgments to identify affected use.
- A **compatibility adapter** presents one contract using another representation or computation; it reduces consumer coordination but adds latency, cost, semantic risk, and lifespan to govern.

### Central model, mechanism, or theorem

Let $U_c(v)$ be the set of valid uses of version $v$ for consumer $c$, and $O_c(v,u)$ the observations promised for use $u$. A change from $v_1$ to $v_2$ is backward compatible for consumer $c$ under equivalence relation $\equiv_c$ only if

$$
\forall u\in U_c(v_1): u\in U_c(v_2)\land O_c(v_2,u)\equiv_c O_c(v_1,u).
$$

This is a specification test, not an automatically decidable universal theorem. Structural compatibility can coexist with semantic breakage: a `decimal` column may retain its type while changing from dollars to cents. Compatibility is generally not symmetric or transitive across undocumented assumptions.

Retirement at time $t$ requires a conjunction of evidence:

$$
R(v,t)=ReplacementReady\land NoticeMet\land KnownMigrated\land NoUnexplainedUse\land CopiesGoverned\land RecoveryPreserved\land Approval.
$$

A sunset date makes `NoticeMet` testable; it does not make the other predicates true. Unknown ownership or incomplete telemetry is evidence of uncertainty, not zero consumers.

### Critical invariants

- Product identity, contract version, state/snapshot, implementation build, schema ID, distribution/file format, and current alias are distinct and recorded together.
- Version triggers evaluate structure, meaning, units, keys, grain, population, null/default behavior, quality, freshness, ordering, policy, delivery, history, and support—not column names alone.
- Every supported version has an immutable identifier, owner, contract, release time, lifecycle state, compatibility claim, lineage, quality/SLO evidence, policy, replacement, and recovery/retention rule.
- Existing versions do not silently change outside their published compatibility policy; bug fixes that alter results receive explicit scope, evidence, and communication.
- The replacement exists, is documented, access-approved, capacity-tested, backfilled as needed, and independently validated before deprecation begins.
- Consumers can pin versions and compare old/new outputs; mutable aliases move through an observable, reversible decision rather than hidden name reuse.
- Consumer discovery combines multiple evidence sources and records telemetry coverage, owners, unknowns, indirect lineage, exports, caches, and contractual consumers.
- Deprecation, sunset, and retirement are separate states with named dates, support changes, reminders, exception rules, and accountable approvals.
- Retirement requires migration evidence or explicit risk acceptance for every known consumer plus a quiet observation window with explained residual traffic.
- Old data, schemas, lineage, code, policy and deletion/recovery semantics remain available for the required reproducibility, audit, retention, and disaster-recovery horizon after service retirement.

### Common failures

Versioning every daily load; equating Git commit, table snapshot, schema ID, and product version; using `latest` in reproducible jobs; treating add-column as universally compatible; changing units, keys, population, null meaning or correction policy without a major contract change; reusing a deleted field name or numeric tag; overwriting an old version in place; producing v1 and v2 from divergent logic without reconciliation; announcing deprecation before the replacement is ready; finding consumers from lineage alone; treating zero observed queries as zero use; ignoring extracts, notebooks, ML features, partner deliveries and cached copies; forcing big-bang migration; extending old versions forever without an owner; deleting history required for audit or recovery; and retiring automatically when a date arrives despite blockers.

### Compact example

`customer_value` v1 exposes `customer_id`, `country_name`, and `lifetime_value_usd`. V2 replaces country name with ISO country code and exposes integer cents. Physical types still parse for many consumers, but meaning and expected values break. The producer publishes v2 beside v1, backfills both from one canonical calculation, provides a mapping and diff, identifies three direct and two export consumers, migrates them, observes 30 quiet days on v1, then moves v1 from deprecated to retired while retaining its contract and recovery artifacts. **Conclusion:** versioning manages consumer meaning and migration; it is not a file-name suffix.

### Connections

[DE-064](064-schema-evolution.md) supplies storage-level evolution, [DE-066](066-time-travel-and-reproducible-reads.md) distinguishes state history, [DE-076](076-data-contracts.md) defines promises, [DE-082](082-dataset-and-column-lineage.md) traces impact, and [DE-098](098-disaster-recovery-for-data-products.md) preserves versions across recovery. [API-084](../../28-api-and-service-engineering/modules/084-deprecation-and-sunset.md) contributes lifecycle signaling; dataset migration adds materialized history, semantic diffs, batch/stream coexistence, exports, and reproducibility.

## Governing Question

For a proposed dataset change, which identity is changing, which supported consumers and historical reads are affected, what precise compatibility relation is claimed, whether a new contract version is required, how old and new states will coexist and reconcile, how consumers will discover and complete migration, which lifecycle gates control deprecation/sunset/retirement, and what must remain retained for audit, replay, deletion, rollback, and disaster recovery?

## Why This Matters

Shared datasets behave like interfaces. Queries, dashboards, pipelines, APIs, feature jobs, notebooks, exports, contractual reports and human decisions rely on more than names and types. They rely on grain, keys, units, population, time semantics, correction behavior, quality, policy, delivery cadence and support. A producer may rename a column cleanly at the storage layer yet break every consumer. More subtly, a producer may preserve the schema while changing “revenue” from booked to recognized revenue and return plausible but wrong results.

Data systems also use the word *version* for different things. A table snapshot identifies one state. A schema registry ID identifies one serialization schema. A Git commit identifies source. A container digest identifies runtime. A contract version identifies what consumers may assume. A daily release identifies an edition. A mutable relation such as `customers` may point to today’s chosen contract. Collapsing these identities makes lineage, reproduction, incident rollback, and deprecation ambiguous. Creating a new major contract for every state update, however, produces unusable churn.

Compatibility is not an intrinsic label on a schema diff. Adding a nullable column is structurally readable by many consumers, yet can break `SELECT *` exports, positional inserts, strict deserializers, cost budgets, or privacy allowlists. Removing a field may be harmless to one consumer and fatal to another. Type widening can be safe at a file-format level while overflowing an application or changing equality. A bug fix may correct the contract or may overturn a behavior that consumers operationalized. A defensible decision names the consumer surface, direction, time horizon, equivalence, and evidence.

Deprecation is where producer incentives collide with consumer reality. Producers cannot operate every version forever: duplicate computation, storage, tests, incidents, policies and expertise accumulate. Consumers need a stable migration window and cannot respond to a hidden rename or last-minute notice. A date alone resolves neither problem. Producers need a ready replacement, actionable diffs, coexistence, telemetry, support and enforcement. Consumers need ownership, pins, tests and scheduled work. Retirement needs evidence that known and hidden uses have been addressed.

The lifecycle continues after serving stops. Historical reports may cite v1. A regulated decision may need its exact semantics. A disaster recovery point may contain v1 state. Deletion must remove subject data from retained versions. A pipeline replay may need its writer schema and code. Service retirement, metadata retention and physical deletion therefore have different clocks. Good versioning makes change routine while keeping evidence honest and the number of live surfaces bounded.

## Prerequisites and Retrieval

Retrieve the enduring product record: stable product/dataset identifier, human name, purpose, owner and steward, consumers and contracts, business criticality, classification, current aliases, delivery surfaces, support tier, geographic scope, retention/deletion obligations, and authoritative versus derived status.

Retrieve all version axes: contract/product versions, table snapshot or transaction IDs, schema registry IDs, writer/reader schemas, file/table format version, source commit, build/image and dependency lock, transformation/config/rule versions, reference-data editions, partition/sort specs, distribution/export versions, model/feature bindings, current pointer, and catalog identifiers. Determine which are immutable and which are pointers.

Retrieve current and proposed contracts: field names and stable IDs/tags, types, nullability/defaults, keys and grain, allowed values, units/currency/time zone, population and filters, event/effective/processing time, update/correction/deletion behavior, ordering/deduplication, quality and reconciliation thresholds, freshness/completeness/availability, access/classification, formats/protocols, location, support, and known undocumented behaviors.

Retrieve change intent and evidence: problem, change class, alternatives, schema/semantic diff, migration mapping, old/new test fixtures, historical recomputation, distribution and business-total comparisons, performance/cost/capacity, policy review, backfill/replay plan, rollback boundary, failure behavior, launch gates, incident ownership, and decision record. Separate producer implementation change from consumer-observable change.

Retrieve consumer evidence: declared registrations, contractual deliveries, query/access/audit logs, column usage and `SELECT *`, workflow and SQL lineage, API/BI/notebook/catalog references, exports and file downloads, stream subscriptions, feature/model lineage, caches and extracts, service accounts, owners/on-call contacts, usage frequency and seasonality, criticality, version pins, last observation, migration state, acknowledgment, exception and retirement validation. Record telemetry retention and blind spots.

Retrieve lifecycle policy: stability levels, compatibility rules, version-number policy, minimum notice, deprecation and sunset semantics, support changes, migration assistance, reminder cadence, quiet-window length, exception criteria/approver/expiry, maximum supported versions, historical metadata/data retention, legal holds, physical deletion, discovery behavior, current alias movement, rollback, and recovery obligations.

Distinguish product identity from distribution location; version from state; contract from schema; format compatibility from semantic compatibility; writer-to-reader from reader-to-writer compatibility; additive from harmless; deprecation from behavioral change; sunset from retirement; unobserved from unused; direct from indirect consumer; version pin from abandonment; service removal from evidence deletion; rollback from restoring an old contract; and migration completion from merely creating the replacement.

Create a dataset-version record:

| Concern | Required evidence and decision |
|---|---|
| Identity | Stable product ID, immutable version ID, aliases, state/schema/code identifiers |
| Contract | Structure, semantics, grain, quality, time, policy, delivery and support |
| Change | Typed diff, compatibility scope/direction, evidence, reviewer and decision |
| Production | Canonical logic, old/new materialization, backfill/replay, capacity and reconciliation |
| Consumers | Inventory sources, owners, use, pin, criticality, migration state and unknowns |
| Lifecycle | Released, current, deprecated, sunset, retired dates and support semantics |
| Migration | Replacement, mapping, examples, dual-run, tests, communications and exceptions |
| Evidence | Usage coverage, acknowledgments, quiet window, approval and audit receipt |
| Preservation | History, schemas, lineage, code, policy, deletion, citation and recovery horizon |

Write a falsifiable claim: “Dataset D v2 changes country name to ISO code and lifetime value from decimal USD to integer cents, so it is incompatible with v1 despite parseable types. V2 has an immutable identifier and complete contract; both versions derive from one canonical base and reconcile at customer/currency/day controls; v2 backfill and SLOs pass; all 17 declared, 9 lineage-discovered, and 3 export consumers have owners; 28 migrated and one time-bounded exception expires before sunset; v1 emits catalog/query notices for 120 days; unexplained v1 use remains zero for 30 days; alias movement is canaried and reversible; and retirement retains v1 contract, schemas, lineage, code and required snapshots for seven years while applying deletion policy.”

## Learning Objectives

After completing this module, you should be able to:

1. distinguish dataset/product, contract, schema, state, implementation, distribution and alias identities;
2. classify structural, semantic, temporal, quality, behavioral, policy, delivery and operational changes;
3. reason about directional consumer-scoped compatibility rather than relying on schema syntax alone;
4. decide when to evolve in place, publish a new contract version, add an adapter, fork a product, or reject a change;
5. design concurrent old/new production, backfill, dual-run, reconciliation, canary, pointer movement and rollback;
6. construct a multi-source consumer inventory with explicit coverage and unknown-use risk;
7. operate release, current, deprecation, sunset, retirement, exception and preservation states;
8. create actionable migration contracts, communications, support and enforcement without surprise breakage;
9. preserve reproducibility, audit, deletion, lineage and disaster recovery after service retirement; and
10. govern an estate to limit version sprawl while measuring migration and compatibility outcomes.

## Core Exposition

### Separate the identities called version

Give the enduring dataset concept a stable identifier independent of storage name. Give each consumer contract an immutable version identifier. Link each produced state to contract version, snapshot/transaction, writer schema, code/config/runtime and source boundaries. Link each distribution—table, file set, topic, API or export—to the version it realizes. Represent predecessor, replacement and current relationships in catalog metadata. W3C DCAT 3, for example, provides vocabulary for version, previous/current/has-version relationships, status and version notes; it does not dictate when your domain needs a new release.

One contract may govern thousands of hourly snapshots because values change while meaning remains stable. One snapshot can sometimes be read through more than one compatible contract projection. A code release that improves execution without altering promised observations need not create a contract version. Conversely, a semantic correction can require a new contract even when schema and code location look unchanged. State this taxonomy in tooling and documentation so a request for “the version” yields a qualified answer.

Treat aliases as pointers. `analytics.customers` or an unversioned catalog URI can resolve to the selected current contract, while `customers@1` remains stable. Consumers needing reproducibility pin. Interactive users may choose current and accept governed movement. Record which choice each consumer makes. Never reuse a version identifier or silently retarget an immutable path; doing so destroys citations and makes recovery receipts lie.

### Define the whole consumer contract

Begin with structure: fields, stable IDs/tags, types, cardinality, nullability, defaults, constraints, keys, grain, nesting and order guarantees. Add semantics: definitions, units, currencies, time zones, enum meanings, population, inclusions/exclusions, aggregation, deduplication, joins and slowly changing history. Add temporal behavior: event/effective/processing time, cadence, lateness, corrections, restatement and watermark behavior. Add quality/SLOs, access/classification/masking, retention/deletion, delivery/location/format, ownership/support and lifecycle policy.

Schema formats encode only part of this contract. Avro specifies resolution between writer and reader schemas. Protocol Buffers uses stable numeric field identifiers and warns against tag reuse. Iceberg tracks columns with IDs and defines allowed evolution. These mechanisms prevent particular decoding or column-association failures; they cannot determine whether a renamed concept, new unit, widened population, shifted business day, slower delivery, or more permissive access is acceptable.

Make defaults semantic. Adding nullable `tax` may parse, but does null mean unknown, not applicable, zero, not yet computed, or withheld? Adding an enum value can break exhaustive application logic. Removing a constraint may allow values older consumers never handled. Define missing, unknown and future values, and include examples at boundaries. Contracts should be testable yet acknowledge narrative domain meaning that requires review.

### Classify change across every observable dimension

Create a typed diff. Structural changes include add/drop/rename/reorder, type/cardinality/nullability/default/key/grain changes. Semantic changes include definitions, units, sign, population, classification, enum meaning and reference-data edition. Temporal changes include cadence, time basis, lateness, restatement and retention. Behavioral changes include ordering, deduplication, corrections, error handling and default alias behavior. Quality/SLO changes affect accuracy, completeness, freshness and availability. Policy changes affect who can see what and where. Delivery changes affect name, protocol, encoding, compression, partitioning and location.

Label proposed compatibility per direction and surface: can an old reader consume new writes; can a new reader consume old history; can old and new producers coexist; can historical queries reproduce; will downstream computations preserve promised outputs? A registry’s `BACKWARD`, `FORWARD` or `FULL` label typically applies to specified schema rules and history depth. It is supporting evidence, not a declaration of business compatibility.

Test counterexamples. `int` to `long` may decode but exceed consumer bounds. Adding a column may break positional extracts, `SELECT *` schemas and allowlists. Renaming with stable table field ID may preserve engine reads but break SQL text and BI bindings. Dropping a field may not affect observed queries but can break seasonal jobs outside telemetry retention. Fixing an incorrect total may be contract-preserving if the definition was clear, yet consumer decisions may need restatement and notice. Record the reasoning, not just a green checker.

### Choose evolution, version, adapter, fork, or rejection

Evolve a contract in place when the change is within published compatibility policy for supported consumers and historical reads. Use a new contract version for intentional incompatibility or material semantic behavior change. Use an adapter when a trustworthy, bounded transformation can present an old contract from the new canonical state or vice versa. Fork into a new product when purpose, population, ownership, authority or lifecycle diverges enough that “version” would falsely imply substitutability. Reject a change when it violates safety, privacy, legal, correctness, or unsupported migration constraints.

Do not apply software Semantic Versioning mechanically. Its major/minor/patch language can support communication only after the public dataset contract and compatibility meanings are defined. A patch that changes historical values can be more consequential than a major schema bump. Some ecosystems use integers or dates. The durable requirements are immutable unique identifiers, ordering/relationships where meaningful, no reuse, explicit notes, and an enforced policy.

Minimize live versions. Prefer additive evolution and compatibility views for small projections when semantics remain sound. Batch intentional breaking changes into a predictable cadence. Limit supported versions and require an owner/cost for exceptions. But do not conceal a break to avoid “major version” optics; understated change transfers cost to incidents and silent analytical error.

### Build the replacement before starting the clock

A deprecation notice without a usable replacement is a demand, not a migration plan. Publish the new contract and stable identifier. Provision access through normal policy. Backfill required history with pinned sources, code and reference data. Establish quality, freshness, completeness, performance, capacity, cost and recovery evidence. Provide field/semantic mappings, query examples, changed behaviors, known non-equivalences, validation queries and support contacts.

Produce old and new versions from a shared canonical intermediate when possible. This reduces divergent business logic while keeping each projection explicit. When v2 changes core semantics, dual-compute both from pinned inputs and reconcile using version-specific expectations. Do not implement v1 by casually selecting from v2 if v2 cannot reproduce v1 meaning; an adapter should fail visibly rather than invent values.

Test with representative consumers. Run contract tests, old-reader/new-writer and new-reader/old-writer matrices, historical reads, backfill and streaming overlap, late correction, null/default/enum boundaries, policy tests, performance and cost. Compare row/key coverage, domain control totals, distributions and sampled records. Differences are classified as intended, corrected defects, data drift or unexplained. Unexplained differences block current-alias movement.

### Discover consumers and quantify uncertainty

Start with explicit registration and contracts, but assume they are incomplete. Join query/audit logs, column-level lineage, orchestration graphs, SQL/code search, BI metadata, API logs, topic consumer groups, feature/model lineage, export/download records, object access, service accounts, catalogs, support tickets and owner interviews. Follow indirect lineage through intermediate datasets. Look for copies beyond governed telemetry: spreadsheets, local extracts, partner files, cached dashboards and scheduled jobs.

For each consumer record owner, purpose, criticality, surface and columns, query or schema, frequency/seasonality, version binding, last observed use, upstream/downstream dependencies, migration state, test evidence and contact status. Separate declared, observed, inferred, contractual, historical and unknown. A service account is not an owner. A query last seen 31 days ago may be a quarterly close. Retain evidence longer than important cycles or seek explicit attestation.

Measure coverage: share of access surfaces instrumented, lookback length, ownership rate, lineage freshness/completeness, unexplained traffic and export visibility. “Zero consumers” is defensible only within those bounds. Unknown use increases notice, compatibility, canary and fallback needs; it does not become zero because the dashboard is blank.

### Publish a migration contract

Announce lifecycle state, not merely a date. Identify product and exact old/replacement versions, rationale, compatibility classification, semantic and structural diffs, release/current/deprecation/sunset dates, support changes, migration steps, mappings, access, validation examples, known limitations, rollback, contacts and exception process. Put the notice where consumers work: catalog, contract registry, query warnings where feasible, API/response metadata for service surfaces, build/CI warnings, change feed, direct owner communication and incident/support channels.

IETF’s `Deprecation` response field signals deprecation without itself changing resource behavior, and `Sunset` can communicate expected unavailability. The same separation is useful for dataset catalogs even when HTTP is not the delivery surface: deprecated does not mean broken today, and sunset is not a surprise removal. Notices need machine-readable metadata plus human guidance.

Make the plan bilateral. Producers commit to coexistence, support, fixes, evidence and dates. Consumers commit to an owner, chosen target, implementation, dual-run comparison, acceptance and removal of old pins/copies. Track acknowledgments and blockers. Communicate at announcement, replacement readiness, midpoint, approaching sunset and completion; tailor urgency to criticality instead of generating unactionable broadcast noise.

### Migrate through coexistence and controlled pointer movement

Run old and new versions concurrently through the declared window. Backfill v2 history or document the start boundary. Shadow consumer logic against v2, compare results and performance, then canary lower-risk consumers. Dual reads can reveal differences but should not become permanent complexity. Dual writes require idempotency, atomicity assumptions and reconciliation; they can create two authorities if ownership is unclear.

Consumers pin v2 explicitly during validation. Once v2 is accepted as current, move the mutable current alias through a reviewed, observable, atomic, and reversible operation. An unpinned consumer then changes behavior, so alias movement is itself a release. Record old/new targets and time; monitor queries, errors, quality, latency, cost and support signals. Keep rollback possible without overwriting v2 evidence.

Migration acceptance should be consumer-specific. A dashboard compares key metrics and visual semantics. A finance export reconciles control totals. A model evaluates feature distributions and outcome performance. A regulatory report confirms definitions and citations. “Query ran” is rarely enough. Remove old references from code, schedules, catalogs, caches and documentation; otherwise dormant rollback code can silently revive v1.

### Operate deprecation, sunset, retirement, and exceptions

Use an explicit state machine: proposed, prerelease, supported, current, deprecated, sunset-reached, retired, preserved, and physically deleted as applicable. Not every state is linear: a prerelease can be rejected; current can roll back; sunset can extend under approved exception; retirement can preserve evidence. Define allowed operations and support for each state.

Deprecation starts when the replacement and migration materials pass readiness. During the window, keep v1 behavior within its contract, operate its SLO/support policy, notify consumers, measure progress and resolve blockers. Sunset marks the planned service stop. Reaching it triggers a retirement decision, not blind deletion. If gates fail, choose a documented extension, exception, forced break with accepted risk, or cancellation; never silently drift.

Exceptions name consumer, reason, impact, owner, compensating controls, cost, new deadline and approver. They expire. Charge operational attention to the decision without using punitive surprise. One critical exception may justify continued service; dozens of low-value unknown pins may justify stronger enforcement. Governance balances consumer harm against security exposure, maintenance burden, duplicated spend and blocked evolution.

### Retire from evidence, then preserve what remains required

The retirement gate requires replacement readiness; minimum notice; migration or explicit exception for known consumers; no unexplained old-version traffic over a representative quiet window; removed indirect jobs, exports and aliases; policy and compliance approval; rollback/recovery plan; and accountable sign-off. Verify access logs, failed query attempts, lineage, schedules, storage reads and consumer attestations after disabling nonproduction paths or introducing reversible denial. Traffic after sunset is evidence to investigate, not merely a metric to wait out.

Retire service in bounded steps: freeze writes, remove current/default discovery, deny new adoption, disable scheduled production, revoke normal access, monitor, remove serving/materialization, and clean infrastructure. Use tombstones or clear catalog status so the name is not silently reused. Preserve incident/audit receipts. Revoke stale credentials and policies tied only to the old surface.

Service retirement does not imply immediate physical deletion. Retain contract, schema, version notes, lineage, source/code/runtime identity, quality evidence and citations for the required horizon. Retain data snapshots only when justified by audit, reproducibility, legal hold and recovery policies; continue applying access, deletion and minimization. Ensure DE-098 recovery cannot restore a retired version as current or resurrect removed subject data. Eventually delete physical state and keys under a separately approved disposition record.

### Govern version portfolios and learn from outcomes

Maintain an estate view of products with multiple live versions, age in state, current/deprecated consumers, unknown ownership, exception debt, duplicated compute/storage, incident history and planned retirement. Set guardrails such as maximum supported majors, minimum notice by tier, evidence windows covering business cycles, and required telemetry coverage. Allow explicit deviations when impact justifies them.

Measure producer outcomes: compatibility defects, unplanned rollbacks, migration lead time, notice compliance, live-version count, old-version spend, support load and retirements. Measure consumer outcomes: owned dependencies, explicit pins, test coverage, acknowledgment latency, migration completion and surprise breaks. Avoid vanity metrics: high migration percentage can hide the only safety-critical consumer; zero v1 queries can reflect missing logs.

Feed incidents and migrations back into contract design. If every change requires a major version, the contract may expose unstable implementation details. If silent semantic breaks recur, review gates may be schema-only. If deprecations never finish, inventory, authority, replacement quality or incentive design may be weak. Versioning is a socio-technical control loop, not a numbering convention.

## Definitions and Notation

Let $D$ be an enduring dataset product and $V(D)$ its contract versions. Let $s\in S(v)$ identify a materialized state conforming to version $v$; $i$ identify implementation; $\sigma$ writer schema; and $a_t(D)$ the mutable current alias at time $t$. A reproducibility receipt is at least $(D,v,s,i,\sigma,inputs,policy,time)$, subject to domain needs.

For consumer $c$, direction $d$, surface $q$, and observation equivalence $\equiv_c$, write

$$
Compat(v_1\rightarrow v_2\mid c,d,q,\equiv_c)\in\{true,false,unknown\}.
$$

`unknown` is necessary when use, telemetry or semantics are incomplete. Aggregate compatibility over supported consumers is true only if every required scoped relation is true or an explicitly approved migration/exception removes that consumer from the claim.

Let inventory union be $I=I_{declared}\cup I_{observed}\cup I_{lineage}\cup I_{contractual}\cup I_{exports}\cup I_{attested}$. Set union removes duplicate identities but does not prove completeness. Record coverage vector $K=(surfaces,lookback,ownership,lineage,export)$ rather than one misleading percentage.

For version $v$, lifecycle events have ordered policy times $t_{release}\le t_{deprecate}\le t_{sunset}$ when all exist. Actual retirement $t_{retire}$ may be later and requires the retirement predicate. Deprecation duration is $t_{sunset}-t_{deprecate}$; it says nothing about replacement readiness or migration completeness.

During dual production, define keyed comparison classes $M$ matched/equivalent, $E$ expected differences, $X$ old-only, $Y$ new-only, and $U$ unexplained differences. Promotion policy may require $U=0$ and bounded, approved $X,Y,E$ under named coverage. Row equality alone may be inappropriate when semantics intentionally change; use mappings and domain controls.

## Mechanisms, Invariants, or Proof Structure

### Dataset version and deprecation mechanism

1. Resolve enduring product identity and record contract, state, schema, implementation, distribution and alias identifiers separately.
2. Inventory current contract and consumers, telemetry coverage, historical/recovery obligations and lifecycle policy.
3. Type the proposed structural, semantic, temporal, quality, policy, delivery and support changes.
4. Evaluate directional compatibility for each supported consumer class and historical read; record false and unknown cases.
5. Choose compatible evolution, new version, adapter, product fork or rejection with accountable review.
6. Publish an immutable replacement contract, identifiers, version notes, mappings, examples, access and support.
7. Build/backfill from pinned sources and canonical logic; test schemas, semantics, policies, SLOs, capacity, recovery and old/new reconciliation.
8. Discover and assign direct, indirect, contractual, export, cached and unknown consumers; publish inventory coverage.
9. Announce deprecation and sunset with machine/human signals; track bilateral migration plans and expiring exceptions.
10. Coexist, shadow, dual-run and canary; accept per consumer; move current alias atomically and reversibly with monitoring.
11. At sunset evaluate replacement, notice, migration, quiet-use, copy, recovery and approval gates; retire in bounded observable steps.
12. Preserve required contracts/data/provenance securely, delete when due, audit outcomes and reduce recurring version debt.

### Conditional claim: structural readability does not imply semantic compatibility

**Claim.** If a new dataset is structurally readable by an old consumer, it does not follow that the change is compatible with that consumer’s contract.

**Proof by counterexample.** Keep field name `amount` and physical type `integer`, but change unit from dollars to cents. An old consumer successfully reads `2500` where it previously expected 2500 dollars, while the producer means 25 dollars. Parsing succeeds and the observation violates promised equivalence. Therefore readability is insufficient. The claim does not say structural checks are unnecessary; failure to parse is itself often an incompatibility.

### Conditional claim: a reached sunset date is insufficient for retirement

**Claim.** $t\ge t_{sunset}$ alone does not establish that version $v$ may be safely retired under an evidence-gated policy.

**Proof by counterexample.** Suppose notice duration is satisfied but one active critical export still reads v1 and has no functioning v2 mapping. The calendar predicate is true while `KnownMigrated` is false, so their conjunction $R(v,t)$ is false. The result follows directly. A policy may explicitly authorize a forced break, but that is risk acceptance with accountable scope, not evidence that migration completed safely.

### Executable retirement-gate illustration

This deterministic fixture evaluates four inventory records after sunset. It blocks retirement for one observed unmigrated consumer and one ownerless consumer, even though two consumers migrated. It illustrates evidence accounting only; it cannot discover hidden consumers, prove telemetry coverage, validate replacement semantics, or grant retirement approval.

<!-- bijux-verify: {"id":"dataset-retirement-gate","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"consumers=4\nmigrated=2\nactive_old=1\nunknown_owner=1\nsunset_reached=true\nretire_allowed=false\nblockers=active-old:billing-export,unknown-owner:legacy-query\n","stderr":""}} -->
```python
consumers = [
    {"name": "risk-dashboard", "owner": "risk", "migrated": True, "last_old_day": 40},
    {"name": "ml-features", "owner": "ml", "migrated": True, "last_old_day": 55},
    {"name": "billing-export", "owner": "billing", "migrated": False, "last_old_day": 94},
    {"name": "legacy-query", "owner": None, "migrated": False, "last_old_day": None},
]
today = 95
sunset_day = 90
quiet_window = 30

active_old = [
    item["name"]
    for item in consumers
    if not item["migrated"]
    and item["last_old_day"] is not None
    and today - item["last_old_day"] < quiet_window
]
unknown_owner = [item["name"] for item in consumers if item["owner"] is None]
blockers = [f"active-old:{name}" for name in active_old]
blockers += [f"unknown-owner:{name}" for name in unknown_owner]

print(f"consumers={len(consumers)}")
print(f"migrated={sum(item['migrated'] for item in consumers)}")
print(f"active_old={len(active_old)}")
print(f"unknown_owner={len(unknown_owner)}")
print(f"sunset_reached={str(today >= sunset_day).lower()}")
print(f"retire_allowed={str(today >= sunset_day and not blockers).lower()}")
print(f"blockers={','.join(blockers)}")
```

## Alternatives and Trade-Offs

- **In-place evolution versus parallel version:** in-place change limits surfaces and cost when genuinely compatible; parallel versions isolate breaks but require duplicate operation and migration.
- **Integer/date/semantic identifiers:** integers communicate ordered contract generations; dates communicate edition time; semantic numbers communicate policy categories. None substitutes for immutable metadata and notes.
- **Pinned versus current alias:** pins give reproducibility and consumer control but can fossilize dependencies; current aliases ease upgrades but make pointer movement an observable release.
- **Shared canonical base versus independent implementations:** a base reduces drift and duplicate logic; independent implementations can isolate radically different semantics but multiply reconciliation and maintenance.
- **View adapter versus materialized old version:** a view reduces storage/backfill but adds query cost and depends on v2 expressibility; materialization isolates performance and history at higher cost.
- **Dual write versus backfill:** dual write supplies current coexistence but risks divergence and split authority; backfill gives repeatable history but may miss real-time behavior and consume capacity.
- **Automatic schema check versus manual semantic review:** automation catches known structural rules consistently; humans and domain tests evaluate meaning but can be slow/inconsistent. Use both with decision records.
- **Additive forever versus periodic major cleanup:** additions avoid immediate breaks but accumulate confusing fields and cost; predictable major releases concentrate migration and simplify the long-lived contract.
- **Broad notice versus targeted ownership:** broad announcements reach unknowns but create noise; targeted plans create accountability but depend on complete inventory.
- **Fixed sunset versus evidence-gated sunset:** fixed dates create urgency and cost bounds; evidence gates prevent unsafe retirement. Combine a real target with explicit escalation/exception decisions.
- **Long compatibility window versus rapid evolution:** long windows protect slow and seasonal consumers but multiply cost/security exposure; short windows demand stronger ownership, tooling and support.
- **Usage telemetry versus attestation:** telemetry observes some real behavior but misses offline/cached use; attestation covers intent and contracts but can become stale. Corroborate sources.
- **Retain old data versus retain only metadata:** data enables exact historical reproduction but carries cost/privacy risk; metadata may explain history without reproducing values. Apply domain retention and legal rules.
- **Rollback alias versus forward repair:** pointer rollback restores prior behavior quickly when old production remains valid; forward repair avoids lost new writes but may take longer. Predefine data reconciliation.

## Failure Modes and Misconceptions

- **One overloaded “version” field.** Consumers cannot tell whether it identifies state, schema, contract, code or format.
- **Daily loads as major versions.** State changes overwhelm the contract lifecycle with noise.
- **Git equals deployed behavior.** Unrecorded configuration, data, reference editions and runtime still affect outputs.
- **Schema equals contract.** Units, population, grain, time, quality, policy and correction behavior remain ungoverned.
- **Additive equals safe.** `SELECT *`, strict bindings, exports, privacy allowlists and cost can break.
- **Parseable equals compatible.** Readable values may have incompatible meaning, range or defaults.
- **Type widening is universal.** Format-level promotion may overflow code, alter precision or break JSON/text consumers.
- **Name-based rename optimism.** SQL, BI and files often bind by name even if table metadata uses stable IDs.
- **Field/tag reuse.** Old serialized or archived data becomes ambiguous; deleted identities should remain reserved.
- **Silent semantic correction.** A justified bug fix can still require restatement, consumer impact review and notice.
- **Mutable old version.** In-place breaking changes destroy reproduction and make pins dishonest.
- **Reusing a retired name.** Dormant queries can return a new concept instead of failing visibly.
- **`latest` in regulated/reproducible work.** Later alias movement changes results without changing the job.
- **Version for every implementation release.** Live contract surfaces grow without consumer value.
- **Never version to avoid complexity.** Complexity reappears as coordinated outages and silent errors.
- **Major number proves break magnitude.** Numbering has meaning only through explicit local policy.
- **Replacement after announcement.** Consumers lose migration time waiting for usable access and history.
- **V2 without historical backfill boundary.** Consumers compare unequal periods and misdiagnose semantics.
- **Independent v1/v2 drift.** Fixes land in one lineage and reconciliation becomes permanently unexplained.
- **Adapter without expiry.** Temporary compatibility becomes an unowned critical service.
- **Lineage-only inventory.** Direct downloads, notebooks, dynamic SQL, exports and external partners disappear.
- **Logs-only inventory.** Lookback gaps, failed calls, cached copies and seasonal use appear unused.
- **Service account as owner.** Migration blockers cannot be assigned to a person/team with authority.
- **Email equals acknowledgment.** Broadcast delivery does not create a plan, test or accepted owner.
- **Calendar-driven deletion.** Sunset arrives while critical consumers, copies or recovery dependencies remain.
- **Exception without expiry/cost.** Old versions continue indefinitely through passive avoidance.
- **Percent migrated vanity.** Ninety-nine trivial consumers can hide one critical unmigrated ledger.
- **Query success as acceptance.** Semantics, totals, timing, policy and performance may still be wrong.
- **Dual-read forever.** Complexity and cost become the permanent architecture instead of a migration control.
- **Immediate physical deletion.** Audit, citations, replay and disaster recovery lose required evidence.
- **Retain everything forever.** Versioning becomes an excuse to violate minimization and deletion obligations.
- **Recovery revives retired current.** Restored aliases/policies undo lifecycle decisions.
- **No post-retirement monitoring.** Remaining callers fail silently and teams cannot validate the decision.

## Worked Examples

### Example 1

A table receives a new nullable `promotion_code`. Registry checks call it additive. One consumer uses `SELECT *` into a fixed-column CSV, another enforces an approved-column privacy list, and a third selects named fields. The first two break while the third does not. The producer either adapts those surfaces or versions the export contract; “additive” was not a product-wide compatibility proof.

### Example 2

An Iceberg table renames `cust_id` to `customer_id` while preserving its field ID. Iceberg-aware reads preserve column association, but raw Parquet readers, SQL text and BI definitions bind names. The team records storage-format compatibility and interface incompatibility separately, publishes a compatibility view, and migrates named consumers before removing it.

### Example 3

An Avro producer adds a field with a default and verifies writer/reader schema resolution in both deployment directions. A consumer nonetheless breaks because its application rejects unknown enum values elsewhere in the record. The compatibility matrix includes generated/application code and real messages, not only registry acceptance.

### Example 4

`net_revenue` keeps decimal type but moves from transaction currency to reporting currency. Because units and reference exchange-rate edition change, the producer publishes v2, retains explicit currency/rate fields, backfills with pinned rates, reconciles per currency/day and prevents an unversioned alias move until finance accepts restated totals.

### Example 5

A dbt model has v1 current and v2 prerelease. V2 removes an unreliable country name. During coexistence, consumers pin v2 for validation while unpinned references remain on v1. After contract, backfill and consumer gates pass, the maintainer moves the current pointer and marks v1 deprecated with a published migration window.

### Example 6

Access logs show no v1 queries for 45 days, apparently exceeding a 30-day quiet window. Inventory review finds a quarterly regulatory export and a partner download outside platform logs. Retirement is blocked until both migrate. Telemetry described only instrumented recent activity; it did not establish absence.

### Example 7

A v1 compatibility view derives country name from v2 country code through a reference table. Historical names and geopolitical boundaries changed, so the adapter cannot exactly reproduce v1 without versioned reference data. The team pins the original reference edition for retained history and discloses non-equivalence for new codes rather than silently using current names.

### Example 8

At sunset, 28 of 29 consumers have migrated. The remaining billing export is critical and active; its exception names an owner, compensating reconciliation, operating cost, and a 14-day deadline approved by product and finance. V1 service continues only for that identity. This is governed residual risk, not a false claim that retirement completed.

### Example 9

After v1 serving is retired, catalog metadata, contract, writer schemas, transformation digest, lineage and required snapshots remain for seven-year audit. Normal query access is revoked, legal holds are honored, and deletion requests propagate to retained data. Preservation is narrower than continued service and more controlled than keeping everything online.

### Example 10

A regional recovery restores a snapshot from before v1 retirement and an old catalog pointer. Recovery automation reapplies lifecycle events and current policy, leaves v1 preserved but noncurrent, and restores v2 as the service alias only after validation. The disaster plan preserves evidence without reversing deprecation governance.

## Cross-Program Connections

- [DE-039](039-deterministic-transformations.md), [DE-049](049-run-metadata-and-operational-state.md), and [DE-050](050-designing-an-operable-data-workflow.md) provide reproducible logic, receipts and operable change paths.
- [DE-064](064-schema-evolution.md), [DE-066](066-time-travel-and-reproducible-reads.md), and [DE-070](070-operating-a-transactional-table-format.md) distinguish schema/table evolution and state history from contract versioning.
- [DE-073](073-reconciliation-tests.md), [DE-076](076-data-contracts.md), and [DE-077](077-producer-and-consumer-responsibilities.md) supply comparison, promises and bilateral ownership.
- [DE-082](082-dataset-and-column-lineage.md), [DE-083](083-data-catalogs.md), [DE-088](088-retention-and-deletion.md), and [DE-089](089-auditability-and-provenance.md) connect inventory, discovery, disposition and historical evidence.
- [DE-094](094-data-apis.md) and [DE-098](098-disaster-recovery-for-data-products.md) connect service signaling and recovery-safe lifecycle state.
- [API-081](../../28-api-and-service-engineering/modules/081-backward-and-forward-compatibility.md), [API-082](../../28-api-and-service-engineering/modules/082-additive-and-breaking-changes.md), [API-083](../../28-api-and-service-engineering/modules/083-versioning-strategies.md), [API-084](../../28-api-and-service-engineering/modules/084-deprecation-and-sunset.md), and [API-085](../../28-api-and-service-engineering/modules/085-consumer-inventory-and-usage-evidence.md) provide interface lifecycle patterns specialized here for data state and semantics.
- [PLAT-085](../../29-platform-engineering/modules/085-upgrade-orchestration.md) connects fleet-wide coexistence, rollout and rollback; data products add historical backfill and semantic reconciliation.
- [DE-100](../ROADMAP.md) integrates version and retirement evidence into the final production data-product review.

## References

- World Wide Web Consortium, *Data Catalog Vocabulary (DCAT) — Version 3*, W3C Recommendation. <https://www.w3.org/TR/vocab-dcat-3/>
- dbt Labs, “Model Versions,” current dbt Developer Hub documentation. <https://docs.getdbt.com/docs/mesh/govern/model-versions>
- Apache Iceberg project, “Table Spec: Schema Evolution,” current specification. <https://iceberg.apache.org/spec/#schema-evolution>
- Apache Avro project, “Specification: Schema Resolution,” current specification. <https://avro.apache.org/docs/current/specification/#schema-resolution>
- Protocol Buffers project, “Proto Best Practices,” current documentation. <https://protobuf.dev/best-practices/dos-donts/>
- Google, “AIP-180: Backwards Compatibility.” <https://google.aip.dev/180>
- Google, “AIP-185: API Versioning.” <https://google.aip.dev/185>
- Internet Engineering Task Force, “The Deprecation HTTP Response Header Field,” RFC 9745. <https://www.rfc-editor.org/rfc/rfc9745.html>
- Internet Engineering Task Force, “The Sunset HTTP Header Field,” RFC 8594. <https://www.rfc-editor.org/rfc/rfc8594.html>
- OpenLineage project, “Dataset Version Facet,” current specification documentation. <https://openlineage.io/docs/spec/facets/dataset-facets/version_facet/>
- Semantic Versioning project, *Semantic Versioning 2.0.0*. <https://semver.org/>

## Exercises

### Exercise 1

Classify these changes for an hourly orders dataset and explain consumer-specific uncertainty: add nullable `coupon_code`; widen 32-bit integer quantity to 64-bit; rename a field while preserving an Iceberg ID; change `amount` from dollars to cents without changing integer type; exclude test orders previously included; move delivery from 10 to 25 minutes; and restrict one sensitive column. Decide which can evolve in place and which need a new contract or migration.

### Exercise 2

Design identifiers and a reproducibility receipt for a product with daily snapshots, Avro source events, two contract versions, a mutable `current` view, transformation code, reference exchange rates, and three file distributions. Explain what is immutable and what may move.

### Exercise 3

Recompute the executable retirement gate. Then suppose `billing-export` migrates on day 96 and its last v1 use remains day 94. On what earliest day does its 30-day quiet condition pass? Does that alone allow retirement, and what must happen to `legacy-query`?

### Exercise 4

Design an old/new validation program for changing `customer_value` from lifetime booked USD to trailing-365-day recognized reporting currency. Include contract, history, reference data, mapping, dual production, expected differences, controls, consumer-specific acceptance, performance, alias movement and rollback.

### Exercise 5

An estate has 180 shared datasets, 63 names ending in `_v2` or `_final`, no version registry, 14 simultaneous variants of one customer table, 40% lineage coverage, 60-day query logs, annual consumers, no deprecation policy, and indefinite snapshots containing personal data. Design a risk-prioritized path to governed versioning and retirement without renaming or deleting everything blindly.

## Answers to the Exercises

### Answer 1

Adding nullable `coupon_code` is often writer-to-old-reader compatible, but inspect `SELECT *`, positional exports, strict bindings, privacy allowlists, cost and null meaning. Widening 32-bit to 64-bit may be supported by a storage/serialization format in one direction, but old applications may overflow; constrain written range during rollout or version affected surfaces. Preserving an Iceberg field ID protects Iceberg-aware association, not name-bound SQL, BI or raw-file readers; add an alias/view or migrate them.

Dollars-to-cents is semantic breakage despite identical type and needs a new contract or a new clearly named field with controlled migration. Excluding test orders changes population and historical totals; whether it is a bug fix or v2 depends on the published v1 definition, but impact, restatement and notice are required. A 10-to-25-minute delivery shift violates consumers requiring the old freshness objective and cannot be called compatible for them. Restricting sensitive access is intentionally breaking for unauthorized workflows and may be mandatory; provide an approved replacement or risk decision without preserving an unsafe contract. Each answer records direction, consumer, surface and equivalence rather than one global label.

### Answer 2

Assign an enduring product ID such as `customer-value`. Give contract versions immutable IDs `customer-value/1` and `/2`. Give each daily state a transaction/snapshot ID and effective interval, and each Avro event its writer schema fingerprint/registry ID and source partition/offset. Record immutable source commit, build/image digest, configuration and reference-rate edition. Give each file distribution an immutable distribution ID, digest, format/schema, partition manifest and contract/state relation.

The `current` view is a mutable pointer whose target and movement events are audited. Human-friendly catalog aliases and physical locations may move, but version-specific identifiers must not retarget. A receipt for a result records product/contract, table snapshot, source boundaries and writer schemas, transformation/build/config, exchange-rate edition, distribution/digest where used, policy and time. That supports reproduction without pretending the contract number identifies daily values or code.

### Answer 3

Original output has four inventory records, two marked migrated, one recently active unmigrated old consumer, one ownerless record, sunset reached, and retirement denied with two blockers. If billing migrates on day 96, migration status can remove it from the fixture’s `active_old` condition immediately; a stricter policy also requires observing that its v1 traffic stops. Thirty days after last use on day 94 is day 124 when `today-last_old_day >= 30`.

That quiet condition alone is insufficient. Replacement readiness, notice, every known migration/exception, unexplained-use coverage, indirect copies, recovery/preservation and approval must pass. `legacy-query` needs a real owner and investigation: determine whether it is a duplicate identity, failed/dormant call, seasonal/contractual use or hidden consumer; then migrate, remove, or accept a scoped expiring exception. Unknown ownership cannot be converted to safe retirement by waiting.

### Answer 4

Publish v2 as trailing-365-day recognized value in named reporting currency, with customer grain, recognition/effective-time rules, exchange-rate source/edition, correction behavior, nulls, exclusions, quality/SLO, history boundary and policy. Keep v1 booked-lifetime-USD immutable. Provide mapping but explicitly state no row-wise equivalence: window, recognition basis and currency conversion intentionally differ.

Pin source snapshots/events, transaction classification and versioned FX rates. Build a canonical transaction-level base, then separate v1/v2 aggregations. Backfill at least 365 days plus correction horizon and validate late/reversed transactions. Dual-produce across closes. Partition differences into expected window expiry, recognition reclassification, FX conversion, new/excluded population and unexplained. Require unexplained zero at governed keys and reconcile transaction counts, booked/recognized controls, per-currency inputs, FX joins, customer/day totals and aggregate finance ledgers.

Inventory dashboards, exports, models and finance/regulatory consumers. Each validates relevant outcomes: finance signs control totals/rates, models assess distribution/performance, reports confirm definitions, and dashboards compare explained movement. Load-test additional backfill/query cost and both versions’ SLOs. Consumers pin v2 for shadow/canary. Move current alias atomically only after approvals and monitor errors, totals, latency and access. Rollback retargets the alias to still-operated v1 and preserves v2 state; reconcile writes/corrections during rollback rather than overwriting evidence.

### Answer 5

Inventory before renaming. Establish enduring product concepts, owners, consumers, criticality, classifications and authoritative/derived relationships. Treat suffixes as clues, not truth: `_v2` may be a real contract, abandoned experiment, state copy or unrelated product; `_final` communicates nothing durable. Prioritize the 14 customer variants, sensitive/high-impact datasets, externally delivered products, incident-prone surfaces and largest duplicated cost.

Define version taxonomy, immutable registry records, current pointers, compatibility/change policy, minimum notices, state machine, exception rules, supported-version bounds and preservation/deletion rules. Register existing states as discovered facts without falsely certifying them. Reconstruct contracts and lineage from schemas, SQL/code, access logs, catalog, BI, schedules, owners and samples. Raise telemetry retention or obtain annual consumer attestations; publish the 40%/60-day blind spots.

For the customer family, identify authoritative semantics and purposeful populations. Consolidate identical duplicates after reconciliation; designate distinct products where purpose/ownership differs; create explicit contract versions for substitutable breaking histories. Provide adapters only with owners and expiry. Establish a ready target, backfill, semantic diff and consumer migration plans before any deprecation. Use canary current pointers and keep stable version pins.

Classify indefinite snapshots by audit, recovery, legal hold and reproducibility need. Apply access/minimization, deletion across retained versions, and bounded disposition rather than mass deletion. Retire candidates only after notice, owned migration/exception, representative quiet windows spanning annual cycles or attestations, copy/lineage checks, recovery updates and approval. Measure live variants, unknown owners, compatibility defects, migration time, exception cost, retained sensitive data and surprise traffic. This yields durable control without mistaking aggressive cleanup for safe lifecycle management.
