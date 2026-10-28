---
module_id: DARCH-018
program: Data Architecture Engineering
level: 1
module_number: 18
title: Temporal and Historical Modeling
status: complete
last_verified: 2026-09-03
---

# Temporal and Historical Modeling

## One-Page Review

### Governing question

How can a team model facts, events, states, identities, relationships, and knowledge across time so that current, historical, retroactive, prospective, disputed, and corrected answers remain reproducible without confusing business validity, recording history, clock readings, civil time, or retention?

### Essential definitions

- **Valid time** is the interval during which a fact is asserted to hold in the modeled domain; SQL terminology often calls it application time.
- **Recorded time** is the interval during which a database or information system held a particular assertion; related literature also uses transaction time or system time under more specific semantics.
- A **bitemporal fact** records both valid-time and recorded-time dimensions, allowing questions about what was believed when concerning what was true when.
- An **instant** is a temporal point under a reference system and precision; an **interval** is an extent bounded by instants, possibly open or unbounded.
- **Granularity** is the resolution at which time is represented or interpreted, such as day, second, or nanosecond.
- A **temporal state** is a value or relationship applicable over an interval; an **event** asserts an occurrence at an instant or during an interval.
- A **retroactive correction** changes the recorded account of an earlier valid period; a **prospective change** is recorded now for a future valid period.
- A **temporal query context** declares the valid-time point or interval, recorded-time cutoff, time zone/calendar, version, and authority used to interpret an answer.

### Central model, mechanism, or theorem

Represent a historical assertion as:

`F = (subject, predicate, value, valid_interval, recorded_interval, source, authority, evidence, version)`

Use half-open intervals `[start, end)` by default for contiguous, discrete records: an interval includes its start and excludes its end. For intervals `A` and `B`, overlap exists when `A.start < B.end` and `B.start < A.end`. Adjacency at one shared endpoint is therefore not overlap. A temporal answer is not complete unless it names both “valid when?” and, when knowledge can change, “known or recorded when?”

### Critical invariants

- Every temporal field names its semantic role, reference system, precision, granularity, zone/offset behavior, uncertainty, and source.
- Valid time, recorded/system time, occurrence time, observation time, publication time, and processing time remain distinct.
- Interval-bound conventions are uniform and explicit; adjacency, overlap, gaps, infinity, and empty intervals have defined behavior.
- For every key and temporal dimension, non-overlap or allowed overlap is an enforceable domain rule rather than an assumption.
- Corrections append new recorded assertions and close earlier recorded intervals; they do not rewrite evidence invisibly.
- Current state is a projection at a declared valid and recorded context, not an unqualified stored truth.
- Civil-time values retain the named zone, applicable rule-set version when required, and ambiguity/nonexistence resolution.
- Historical identifiers, code systems, units, authorities, and schema/rule versions remain resolvable for the time questioned.
- Retention, redaction, legal hold, deletion, compaction, archive, and restoration preserve only authorized history and disclose limitations.
- Temporal tests cover boundaries, clock and calendar anomalies, late facts, corrections, overlapping assertions, gaps, and replay.

### Common failures

Common failures are using `created_at` for every time; storing only the latest row; treating update time as business validity; using inclusive end dates inconsistently; representing open-ended intervals with arbitrary sentinel dates; allowing overlap without authority rules; assuming timestamps impose causality; converting a recurring civil schedule to UTC too early; storing an offset without the named zone; ignoring daylight-saving gaps and folds; assuming the time-zone database is timeless truth; applying today's codes or exchange rates to history; editing past rows after correction; retaining audit logs that cannot answer as-of queries; and claiming complete history after retention or migration discarded evidence.

### Compact example

On 10 August, payroll learns that an employee's salary increased effective 1 July, not 1 August as previously recorded. A current-only table overwrites the amount and loses both the earlier belief and the correction date. A bitemporal model closes the old assertion's recorded interval on 10 August, retains its valid intervals as previously known, and appends corrected assertions whose recorded interval begins 10 August. Queries can answer “salary valid on 15 July according to records on 5 August” and “salary valid on 15 July according to records now.”

### Connections

[DARCH-014](014-entities-relationships-and-business-keys.md) supplies temporally scoped identity and relationships. [DARCH-017](017-event-schemas-and-information-models.md) distinguishes event occurrence and recording times. This module establishes historical semantics before [DARCH-019](../ROADMAP.md) governs model versions and [DARCH-020](../ROADMAP.md) reconciles conflicting models.

## Governing Question

Time enters data in many roles. A contract is effective during one interval, a system learns about it later, an event occurs at an instant, an observer detects it afterward, a row is committed later still, and an analyst processes it next day. Calling all of these `timestamp` erases the questions the data must answer.

History is also a history of knowledge. An organization may discover a late fact, correct an earlier error, receive conflicting evidence, or schedule a future change. “What was true on 1 July?” differs from “What did we believe on 1 July about 1 July?” and “What do we now believe about 1 July?” A single effective date cannot answer all three.

Temporal modeling therefore begins with domain questions, authority, and evidence—not database types. It defines time dimensions and interval semantics, chooses event, state, or bitemporal structures, and preserves versions needed for reproducible decisions. Physical system clocks and time-zone libraries then implement bounded portions of that model.

## Why This Matters

Temporal mistakes alter money, rights, safety, compliance, availability, and analysis. Overlapping price intervals can bill two amounts. A retroactive entitlement correction can require repayment. A daylight-saving fold can schedule a job twice. A late clinical result can change what was known at a treatment decision. A model that stores only current state cannot reconstruct or explain these outcomes.

Allen's paper on [temporal intervals](https://doi.org/10.1145/182.358434) formalized qualitative interval relations such as before, meets, overlaps, during, starts, and finishes, with converses and equality. These relations are more expressive than comparing one timestamp and expose why interval endpoints and topology matter.

Snodgrass's freely available book, [*Developing Time-Oriented Database Applications in SQL*](https://www.cs.arizona.edu/~rts/tdbbook.pdf), develops valid-time, transaction-time, and bitemporal database techniques. ISO/IEC [9075-2:2023 SQL/Foundation](https://www.iso.org/standard/76584.html) is the current SQL foundation standard. Product support and terminology vary, so architectural semantics must be explicit rather than inferred from a feature name.

Temporal correctness also depends on civil authorities and changing rules. The IANA [time-zone database theory](https://www.iana.org/time-zones/theory) documents scope, historical limitations, identifiers, offsets, daylight-saving changes, calendars, and leap-second concerns. “Store UTC” is useful for instants but does not preserve every civil-time intent, recurring schedule, or historical rule.

## Prerequisites and Retrieval

You should understand entities, keys, relationships, events, state, intervals, inequalities, databases, transactions, distributed clocks, time zones, schemas, provenance, retention, privacy, and migration.

Retrieve instant, interval, duration, period, valid time, application time, transaction time, system time, recorded time, bitemporal, as-of, known-as-of, effectivity, event time, observation time, ingestion time, granularity, precision, uncertainty, half-open interval, unbounded endpoint, overlap, adjacency, gap, coalescing, correction, retraction, retroactive, prospective, snapshot, temporal object, audit log, civil time, offset, zone, calendar, leap second, and clock skew.

As a retrieval test, inspect `start = 2026-11-01 01:30`, `end = 2026-11-01 02:30`. Ask which calendar and named zone apply, whether the start is the first or second 01:30 during a daylight-saving fold, whether endpoints are inclusive, what precision applies, whether this is validity or recording time, who asserted it, and when the system learned it. Without these coordinates, duration and ordering may be ambiguous.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish valid, application, recorded, transaction, system, occurrence, observation, ingestion, and processing time;
2. choose instants, intervals, events, temporal properties, temporal objects, snapshots, audit logs, and bitemporal structures by question;
3. define half-open boundaries, unbounded endpoints, granularity, precision, uncertainty, adjacency, overlap, gaps, and coalescing;
4. model retroactive corrections, prospective changes, late facts, disputes, retractions, and supersession without invisible history rewriting;
5. query current, as-of, known-as-of, and bitemporal state with explicit authority and version context;
6. represent civil time, UTC instants, offsets, named zones, calendars, daylight-saving gaps/folds, and time-zone rule versions appropriately;
7. enforce temporal keys, referential integrity, non-overlap, cardinality, state-transition, and lifecycle constraints;
8. combine event histories and state histories while preserving derivation, replay, corrections, and snapshots;
9. govern temporal retention, privacy, security, legal hold, archive, recovery, migration, and historical limitations;
10. verify temporal models with boundary, adversarial, property, query, replay, and source-reconciliation evidence.

## Core Exposition

**Begin with temporal questions.** Write the decisions and queries before choosing fields. “Which price applies to order acceptance at 10:03?” asks valid time. “Which price did the service have recorded when it accepted the order?” adds recorded time. “When did the price-change event arrive?” asks another lifecycle time. Each answer may differ legitimately.

Specify subject, predicate, value, authority, temporal dimension, granularity, and consequence. A person's address, legal name, mailing contact, residence, and delivery destination have different validity. A device reading has measurement time, receipt time, and calibration context. Avoid one generic `effective_at` used for incompatible predicates.

**Separate valid and recorded time.** Valid time describes when an assertion applies in the domain. Recorded time describes when a particular information system held the assertion. In a bitemporal table, each logical assertion occupies a rectangle in valid-time by recorded-time space.

Suppose a contract rate of 100 was recorded on 1 January as valid from January onward. On 10 March the organization learns that the rate changed to 110 effective 15 February. The new knowledge begins on 10 March but applies retroactively from 15 February. Retaining both dimensions explains earlier invoices and supports corrected ones.

“Transaction time” often means system-maintained commit history and can have database-specific semantics. “Recorded time” can include application or authoritative registration semantics. Name the actual clock, boundary, and owner. Do not claim system time represents user awareness, external publication, or legal notice unless the workflow proves it.

**Distinguish event and state time.** An event occurs; a state holds. `DoorOpened` is an occurrence, while `DoorState = OPEN` holds until another governed transition. An event timestamp does not automatically define the state's end. Missed, duplicate, or corrected events can make reconstruction uncertain.

Store events when sequence, causality, audit, or reconstruction matters. Store temporal state when direct as-of queries and constraints matter. Often retain authoritative events plus governed state projections and reconciliation. Do not call an audit trail an event source unless it preserves complete ordered semantics and exact reducers.

**Choose temporal scope per fact.** Some entities are stable while properties vary. A Person may have temporal names and addresses. Some relationships are temporal: employment, ownership, membership, authorization. Some entire versions form coherent state: a contract amendment changes several terms together.

Use effectivity on a relationship or assertion when the interval is part of domain meaning. Use a temporal property when one attribute varies independently. Use a temporal object when coordinated versions matter. Martin Fowler's [temporal patterns](https://martinfowler.com/eaaDev/timeNarrative.html) compare audit logs, effectivity, temporal properties, snapshots, and temporal objects; they are design patterns, not universal database prescriptions.

**Define interval boundaries.** Half-open `[start, end)` intervals are usually composable: `[Jan 1, Feb 1)` meets `[Feb 1, Mar 1)` without overlap or gap. Duration is `end - start`. One instant belongs to at most one adjacent version. This convention avoids subtracting a smallest unit from an inclusive end.

Inclusive business language such as “valid through 31 January” should map to the next boundary at the domain granularity, for example `[2026-01-01, 2026-02-01)` for whole days. Do not convert to `23:59:59.999`; precision can increase and create gaps.

Record whether an endpoint is open, closed, or unbounded when the domain requires other topologies. An empty interval `[t,t)` can be valid as an empty set but may be prohibited for state. Define zero-duration events separately rather than abusing empty effectivity.

**Represent infinity deliberately.** Null endpoints can mean unbounded, unknown, not applicable, or missing. Do not overload them. A sentinel such as `9999-12-31` collides with valid domain dates, causes arithmetic errors, and leaks physical conventions into interfaces.

Use native unbounded ranges where supported, explicit endpoint variants, or a separate bound kind. Map to external systems with documented loss. Query APIs should expose “unbounded” semantically rather than requiring consumers to recognize a magic date.

**Use interval relations precisely.** For intervals A and B, distinguish before, meets, overlaps, starts, during, finishes, equals, and their converses. “Conflicts” may mean any overlap, overlap above a threshold, or overlap among assertions from the same authority. Define it.

Allen's interval algebra reasons qualitatively without exact distances. Quantitative models also need endpoints and durations. Do not infer causal order merely from before; shared causes, reporting delay, and independent clocks remain possible.

**Enforce non-overlap where warranted.** For a key such as `(product, market, price_type)`, the rule may permit at most one authoritative price at each valid instant. Check overlap within that exact partition and authority. Competing source assertions may legitimately overlap if the model preserves disagreement.

PostgreSQL's current [range-type documentation](https://www.postgresql.org/docs/current/rangetypes.html) describes built-in ranges, inclusive/exclusive bounds, canonical forms, operators, and exclusion constraints that can enforce non-overlap. Treat this as one physical mechanism; logical invariants must survive other implementations, bulk paths, replicas, and migrations.

Race conditions matter. A pre-insert query followed by insert does not enforce non-overlap under concurrency without appropriate transaction or constraint behavior. Test simultaneous writers, boundary equality, open endpoints, and restoration.

**Define temporal keys.** A temporal version often has key `(continuity_id, valid_start)` or a surrogate plus uniqueness rules. This is not automatically sufficient when retroactive corrections produce several recorded versions for the same valid start. Bitemporal identity may need assertion identity plus both dimensions.

Keep continuity identity separate from version identity. A contract remains one contract across amendments, while each amendment or temporal state has identity and provenance. References must state whether they target the continuity, the version valid at a time, or a fixed historical version.

**Model temporal referential integrity.** A relationship valid during interval R may require its referenced entity or role to exist throughout R, at R's start, or at the event instant. State the containment rule. A current foreign key cannot prove historical containment.

If an Employee Assignment is valid `[a,b)`, its Position and Employee identities may need valid coverage for the same period. Splitting referenced intervals should not invalidate meaning if coverage remains continuous. Cross-system checks need snapshot/version and reconciliation policy.

Deletion and retirement do not necessarily end historical referential existence. Use tombstones or retained continuity records where authorized. A cascade can erase required evidence; a restrict can block lawful deletion. Separate operational removal, domain end, and historical retention.

**Handle temporal cardinality.** “One active manager per team” is a temporal non-overlap constraint partitioned by team and manager-role type. “At least one” across time is harder: every instant in a required coverage interval must be covered. Gaps at boundaries matter.

For percentage allocations, totals may need equal 100 percent at every instant under one authority and class. Split all intersecting endpoints into atomic segments, evaluate applicable assertions per segment, and report gaps or excess. Sampling one day per month cannot prove continuous validity.

**Coalesce cautiously.** Adjacent intervals with identical value, source, authority, and relevant provenance may be combined for simpler queries. Coalescing can erase meaningful assertion boundaries, approval events, or recording history. Define which attributes determine equivalence and whether raw history remains.

Never coalesce across a correction boundary merely because the final value matches. “We believed 100, corrected to 110, then corrected back to 100” is not equivalent to uninterrupted belief when decision explanation matters.

**Model bitemporal correction append-only.** When a correction arrives at recorded time `r2`, close the current recorded interval at `r2` and append rows describing the revised valid history with recorded start `r2`. Earlier recorded slices remain queryable. The corrected valid interval may require splitting multiple rows.

Protect atomicity so no query sees half of the correction. Record correction identity, source assertion, authority, reason, affected versions, and evidence. An application-maintained sequence can complement timestamps when commits share precision.

Fowler's [bitemporal history](https://martinfowler.com/articles/bitemporal-history.html) explains actual/valid and record-time dimensions through retroactive changes. Terminology differs across sources; define local vocabulary and map it to standards rather than arguing from labels.

**Query with two coordinates.** A valid-time query asks `valid_contains(v)`. A recorded-time query asks what row version the system held at `r`. A bitemporal query applies both. “Current” normally means valid now and recorded now, but “now” must identify clock and transaction snapshot.

Expose APIs such as `as_valid_at` and `known_at` rather than one ambiguous `as_of`. Defaulting to current can be ergonomic, but responses should state evaluation context. Cache keys need both coordinates and model/rule versions; otherwise historical queries can receive current results.

Historical answers also depend on identity crosswalks, code systems, units, calendars, time-zone rules, schema versions, and authorization. Preserve or version these dependencies. Applying today's exchange rate or postal boundary to a past assertion creates a new analytical projection, not recovered historical truth.

**Treat recorded time as perspective-specific.** A source system, integration hub, warehouse, and regulator can record the same assertion at different times. There is no single universal transaction time across independent systems. Preserve lineage between perspectives.

A data warehouse load timestamp is not the source's recorded time. Carry source validity and source-recorded time when available, then add ingestion and warehouse-recorded time. This can create more than two relevant dimensions; select those needed by decisions while retaining provenance.

**Represent uncertainty.** A historical date may be known only to a year, an event may occur within a window, a clock may have error bounds, and sources can disagree. Do not convert `circa 1900` to `1900-01-01T00:00:00Z` without qualification.

Model earliest/latest bounds, precision, confidence, method, and source as appropriate. Interval relations can become possible sets rather than single facts under uncertainty. High-impact decisions need conservative rules and expert review.

Unknown is not unbounded. “End date unknown” differs from “continues indefinitely.” Estimated differs from exact. Redacted differs from unknown. Preserve these variants in schemas and queries.

**Distinguish duration from calendar period.** Twenty-four hours is not always one local civil day across daylight-saving transitions. One month has variable length. Business days depend on jurisdictional calendars and holidays. Represent the intended quantity and calendar rule.

Adding a duration to an instant differs from advancing a civil schedule. “Run every day at 09:00 Europe/Paris” should retain local time and named zone; converting future occurrences once to UTC freezes today's rules. Recompute with a pinned or current policy as the application requires.

**Store instants and civil intent separately.** An instant can be normalized to UTC for comparison while retaining original offset when evidential. A future appointment may need local date/time, named IANA zone, ambiguity choice, and rule-set version, because political rules can change before it occurs.

PostgreSQL's [date/time documentation](https://www.postgresql.org/docs/current/datatype-datetime.html) distinguishes timestamp types and explains named zones, offsets, and daylight-saving behavior. Product semantics matter: a type named “with time zone” may store an instant rather than the original zone identity. Test round trips.

RFC 3339 defines a useful timestamp syntax with offsets. A numeric offset is not a time-zone rule set. `-04:00` does not say whether a location observes daylight saving or what future law applies. Time-zone abbreviations are ambiguous and historically variable.

**Handle gaps and folds.** When clocks move forward, some local times do not exist; when clocks move backward, some occur twice. A parser or database may silently choose one. Define whether input rejects, shifts, or requires an offset/fold indicator. Record the choice.

Test transition dates for every supported zone, not merely the developer's zone. Include zones with unusual offsets and rule changes. Pin time-zone data in reproducible calculations and track updates; future schedule recalculation may intentionally use new rules.

**Recognize time-zone database limits.** IANA tz data represents known and predicted civil-time rules for representative locations, with historical uncertainty and an explicit practical scope. Zone boundaries are not geospatial boundaries, and past rules can be corrected. Store source and release where historical reproducibility requires it.

Do not interpret a location's old timestamp with the newest database and call the result immutable truth without noting the rule version. Conversely, retaining an obsolete future rule after law changes can schedule incorrectly. Define whether a use seeks historically reproduced computation or current best knowledge.

**Address clocks and causality.** Wall clocks can skew, step, smear, or lack synchronization. Monotonic clocks measure durations within one runtime but do not map directly to civil instants. Distributed timestamp order does not prove happened-before.

Record clock source, synchronization, uncertainty, and monotonic sequence where relevant. Use causal identifiers, logical clocks, versions, or consensus order for operations requiring stronger ordering. Safety margins should exceed evidenced clock uncertainty.

Leap seconds and smearing complicate exact UTC. Many POSIX systems ignore leap seconds; providers can smear differently. Systems needing scientific, financial-market, navigation, or legal precision require domain-specific time-scale expertise beyond ordinary timestamp libraries.

**Use temporal ontologies within scope.** The W3C [Time Ontology in OWL](https://www.w3.org/TR/owl-time/) supplies vocabulary for instants, intervals, duration, temporal positions, reference systems, and topological relations. The cited edition is a Candidate Recommendation Draft, not a final Recommendation. Its constructs can support interchange while local constraints and database behavior still need specification.

Open-world ontology semantics differ from closed-world integrity checks. Absence of an end may not imply unbounded validity. Do not assume an OWL reasoner will enforce database completeness or non-overlap without appropriate shapes, rules, and validation.

**Design snapshots as derived artifacts.** A snapshot represents state at a valid and recorded context under exact reducer/model versions. Record watermark, included sources, ordering, gaps, corrections, filters, schema, creation time, and digest. A snapshot can accelerate queries and replay but does not replace authoritative history unless governance says so.

Validate snapshot against events or temporal assertions using counts, identities, invariants, hashes, and sampled semantics. A current snapshot cannot answer former-known-as-of questions unless it retains recorded history.

**Separate audit logs from queryable history.** Audit logs record actions for accountability and diagnosis. They may contain before/after images, actor, request, and time, but often lack domain validity, complete semantics, or stable schemas. Temporal tables support as-of state. Event stores preserve governed occurrences. These can coexist.

Do not promise historical reconstruction from an audit log without testing it. Missing bulk operations, privileged bypasses, truncation, redaction, clock ambiguity, and application-only changes can break reconstruction. An audit trail can prove that a record changed while remaining unable to prove what domain fact was valid.

**Model state transitions and duration invariants.** Some states must follow an allowed graph and have non-overlapping validity. Others allow concurrent substates. A status history should record transition occurrence, effective interval, authority, cause, and correction rather than only successive labels.

Enforce minimum/maximum durations only with clear calendar semantics. A 30-day cancellation window differs from one calendar month or 20 business days. Define start event, endpoint inclusion, zone, holidays, exceptions, and clock.

**Aggregate history correctly.** Slowly changing dimensions, balances, headcount, active subscriptions, and exposure are time-dependent. Joining two temporal histories on identity alone creates combinations that never coexisted. Intersect valid intervals and, when required, recorded intervals before aggregation.

Point-in-time joins need exact query context. Period measures distinguish flow during an interval from stock at an instant. Summing daily balances differs from end-of-month balance. Late corrections require restatement policy and reproducible report versions.

**Protect historical data.** History increases sensitivity and linkability. Old addresses, roles, health states, locations, and identifiers can reveal more than current state. Apply purpose, authorization, minimization, encryption, retention, legal hold, deletion, redaction, subject access, correction, and incident controls to every temporal version and derived snapshot.

Append-only is not an exemption from deletion obligations. Possible architectures include separated encrypted payloads, key destruction, tombstones, redacted projections, retention partitions, or irreversible aggregation, each with limitations. Authorized legal and privacy review must choose.

Record access time and purpose for historical queries where risk warrants it. Prevent ordinary current-state roles from automatically gaining all history. Temporal query APIs can be powerful exfiltration surfaces.

**Plan retention and historical limitations.** Define earliest reliable valid and recorded dates, gaps, migrated sources, precision changes, known inaccuracies, and retained artifacts. If history begins at system launch, do not represent pre-launch state as known unchanged.

Retention can truncate recorded history while retaining current valid facts. Mark the horizon so known-as-of queries outside it fail explicitly rather than fabricate an answer. Legal holds can create exceptions; record scope and release.

**Migrate temporal data carefully.** Inventory source semantics for every date and timestamp. Detect sentinel values, implicit zones, inclusive ends, overlapping rows, duplicates, gaps, precision truncation, and update-time misuse. Do not mechanically rename columns to `valid_from`.

Define target intervals, conversion rules, uncertainty, source lineage, ambiguous cases, and rejection handling. Use a cutover time, capture concurrent changes, preserve source-recorded history, validate boundary cases and invariants, and retain rollback. Migrating only current rows cannot yield complete history.

**Test temporal behavior.** Use property tests for interval overlap, adjacency, containment, splitting, coalescing, and bitemporal correction. Test minimum/maximum instants, empty and unbounded ranges, precision, concurrent writes, time-zone gaps/folds, leap days, calendar boundaries, rule updates, and clock skew.

Test queries at one tick before, exactly at, and one tick after every boundary under the declared granularity. Verify as-of and known-as-of answers against hand-built histories. Replay corrections and compare projections. Run privacy/deletion and recovery exercises.

**Govern temporal models.** Maintain a temporal-field registry with name, meaning, clock, reference system, zone policy, granularity, precision, uncertainty, source, authority, retention, and owner. Record interval convention, temporal keys, overlap rules, query contexts, correction protocol, and version dependencies.

Review changes to precision, time-zone library, calendar, endpoint convention, clock source, retention, identity, schema, and authority as semantic changes. Monitor overlap violations, gaps, late arrivals, correction latency, unresolved disputes, as-of query failures, and migration exceptions.

## Definitions and Notation

Let a temporal assertion be:

`F = (S, P, V, Iv, Ir, O, A, E, M)`

where `S` is subject, `P` predicate, `V` value, `Iv` valid interval, `Ir` recorded interval, `O` source observation, `A` authority, `E` evidence, and `M` model/rule version. Several sources may assert conflicting `F` values over the same valid interval; resolution requires an authority rule, not interval arithmetic alone.

For half-open intervals `A = [a1,a2)` and `B = [b1,b2)`, define:

`overlap(A,B) iff a1 < b2 and b1 < a2`

`meet(A,B) iff a2 = b1`

`contains(A,t) iff a1 <= t and t < a2`

Unbounded endpoints require extended ordering or explicit bound variants. Granularity and precision determine how input values map to endpoints; do not add a machine epsilon to simulate inclusive business dates.

A bitemporal query answer at valid instant `v` and recorded instant `r` selects assertions satisfying `contains(Iv,v)` and `contains(Ir,r)`, then applies source/authority and conflict rules. Omitting `r` usually means the latest recorded perspective, which must be stated.

## Mechanisms, Invariants, or Proof Structure

Use ten gates to design and assure temporal information.

**1. Question gate.** State decisions, subject, predicate, current/as-of/known-as-of query, consequence, and required historical horizon.

**2. Dimension gate.** Define valid, recorded, occurrence, observation, publication, ingestion, processing, and other necessary time roles without conflation.

**3. Representation gate.** Choose instant, interval, event, temporal property/object, snapshot, audit, valid-time, recorded-time, or bitemporal structure.

**4. Boundary gate.** Define start/end inclusion, infinity, empty interval, granularity, precision, uncertainty, overlap, adjacency, gaps, and coalescing.

**5. Integrity gate.** Enforce temporal keys, non-overlap, coverage, referential containment, cardinality, state transitions, authority, and concurrency.

**6. Civil-time gate.** Bind time scale, calendar, UTC/offset/zone, zone database and version, daylight-saving gaps/folds, recurrence, leap behavior, and clock quality.

**7. Correction gate.** Govern late facts, retroactive/prospective changes, disputes, append-only recorded history, supersession, retraction, and consequence propagation.

**8. Query and derivation gate.** Version as-of contexts, joins, aggregations, events, reducers, snapshots, reference data, and reproducibility evidence.

**9. Protection and lifecycle gate.** Control purpose, access, retention, legal hold, deletion, archive, migration, recovery, limitations, and verified retirement.

**10. Challenge gate.** Test every boundary, overlap/gap, concurrent write, clock anomaly, civil-time transition, correction, replay, migration exception, and protected-history path.

The executable example checks four narrow temporal-registry failures: missing recorded time, overlapping valid intervals, missing named zone for civil time, and an inclusive-end convention where half-open intervals are required.

<!-- bijux-verify: {"id":"temporal-model-integrity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"items=4\nvalid=0\nfindings=address:missing-recorded-time,meeting:missing-time-zone,policy:non-half-open-interval,price:overlapping-validity\nready=false\n","stderr":""}} -->
```python
items = (
    {"id": "address", "recorded_time": "", "overlap": False, "civil_time": False, "time_zone": "", "end_exclusive": True},
    {"id": "price", "recorded_time": "2026-09-03", "overlap": True, "civil_time": False, "time_zone": "", "end_exclusive": True},
    {"id": "meeting", "recorded_time": "2026-09-03", "overlap": False, "civil_time": True, "time_zone": "", "end_exclusive": True},
    {"id": "policy", "recorded_time": "2026-09-03", "overlap": False, "civil_time": False, "time_zone": "", "end_exclusive": False},
)

findings = []
valid = 0
for item in items:
    local = []
    if not item["recorded_time"]:
        local.append("missing-recorded-time")
    if item["overlap"]:
        local.append("overlapping-validity")
    if item["civil_time"] and not item["time_zone"]:
        local.append("missing-time-zone")
    if not item["end_exclusive"]:
        local.append("non-half-open-interval")
    if local:
        findings.extend(f"{item['id']}:{finding}" for finding in local)
    else:
        valid += 1

print(f"items={len(items)}")
print(f"valid={valid}")
print("findings=" + ",".join(sorted(findings)))
print(f"ready={str(valid == len(items)).lower()}")
```

The checker validates four declared registry predicates only. It does not prove temporal truth, clock accuracy, interval completeness, authority, civil-time interpretation, non-overlap under concurrency, bitemporal correction, privacy, retention, migration, or reproducible replay. Those require domain rules, exact implementations, representative histories, boundary tests, operational evidence, and accountable review.

## Alternatives and Trade-Offs

**Current state versus retained history.** Current state is simple and efficient but cannot reconstruct prior facts or beliefs. Full history supports audit and correction at greater storage, query, privacy, and governance cost.

**Events versus temporal state.** Events preserve occurrences and causal sequence; temporal state directly answers as-of queries and constraints. Event reconstruction depends on completeness and reducers. Combining authoritative events with governed projections often works best.

**Valid-time versus bitemporal.** Valid-time history answers what applied when. Bitemporal history also explains changing knowledge but multiplies rows, queries, and correction complexity. Use it where retroactive knowledge affects material decisions.

**Inclusive versus half-open intervals.** Inclusive ends match some business language but complicate adjacency and precision. Half-open intervals compose cleanly. Translate whole-period inclusive language at semantic boundaries.

**Null versus explicit unbounded endpoint.** Null is compact but can conflate unknown and infinity. Explicit variants preserve meaning at schema cost. Native ranges can help inside one database but need portable mappings.

**UTC instant versus civil schedule.** UTC supports instant comparison. Local time plus named zone preserves human scheduling intent and future rule changes. Many applications need both, with an explicit ambiguity policy.

**System-managed versus application-managed history.** System versioning captures row changes consistently but may not encode domain validity or authority. Application history can express semantics but has more bypass risk. Layer controls and reconcile.

**Coalesced versus assertion-preserving history.** Coalescing simplifies queries and storage. Assertion-preserving history retains decision and correction boundaries. Keep raw evidence when explanation matters and derive coalesced views.

## Failure Modes and Misconceptions

1. **A timestamp makes data temporal.** Its role, clock, reference system, precision, and authority determine meaning.
2. **Update time is valid time.** When a system learned a fact can differ from when it applied.
3. **One history axis is always enough.** Retroactive corrections require a separate history of knowledge when prior decisions matter.
4. **Events automatically reconstruct state.** Missing, reordered, corrected, or semantically weak events can make replay invalid.
5. **Inclusive end is intuitive and safe.** It creates overlap or tiny gaps when granularity and precision change.
6. **Null end means forever.** It may mean unknown, not applicable, missing, or unbounded.
7. **No duplicate current row means no overlap.** Temporal overlap concerns intervals and can arise under concurrent writes.
8. **UTC solves all time problems.** It does not preserve future civil schedules, calendars, zone identity, or historical rule provenance.
9. **An offset identifies a zone.** Many zones share an offset now and diverge across dates or future rules.
10. **Timestamp order proves causality.** Independent clocks, batching, and observation delay invalidate that inference.
11. **Audit logs provide temporal queries.** They may lack validity, complete capture, stable schemas, and efficient reconstruction.
12. **Append-only means facts cannot be corrected.** New assertions can retract or supersede earlier claims while retaining evidence.
13. **Today's reference data explains history.** Codes, units, identities, boundaries, and rules also change over time.
14. **More history is always better.** Retention increases exposure, cost, and deletion obligations.
15. **A successful migration recreates history.** Current rows plus invented start dates cannot prove past states or prior knowledge.

## Worked Examples

### Example 1

A price valid through 31 January is stored with `end = 2026-01-31 23:59:59`. Nanosecond-capable consumers find a gap. The model uses whole-day `[2026-01-01, 2026-02-01)` validity and records currency, market, authority, and recorded interval.

### Example 2

Two salary records overlap after a retroactive correction. Instead of deleting the earlier row, the bitemporal transaction closes its recorded interval and appends the corrected valid history, preserving what payroll believed before correction.

### Example 3

A recurring meeting is stored only as UTC instants for the next year. A jurisdiction changes daylight-saving rules. The model retains local time, named zone, recurrence, ambiguity policy, and rule-set basis, then regenerates future occurrences under approved policy.

### Example 4

An employment relationship references a position that appears current but did not exist during the assignment's first month. Temporal referential validation checks interval coverage and exposes the historical orphan.

### Example 5

A warehouse joins customer segment history and price history on customer ID without intersecting intervals. It produces segment-price combinations that never coexisted. The corrected join intersects valid intervals and pins recorded cutoff and model versions.

### Example 6

A museum record says an artifact was created in “about 1700.” Import converts it to midnight UTC on 1 January. The revised model records a bounded or calendar-granularity estimate, source, confidence, and reference system without false precision.

### Example 7

At a fall daylight-saving transition, `01:30` occurs twice. Booking input requires named zone plus chosen offset or fold; ambiguous local times are rejected for correction rather than silently assigned.

### Example 8

A deletion request removes current contact data but leaves temporal versions, snapshots, audit exports, and backups accessible to ordinary support roles. The lifecycle applies purpose-based access and authorized deletion/redaction across every historical representation.

### Example 9

An event replay under a new reducer yields a different state because today's code system reinterprets an old status. The projection pins reducer, schema, code-system, and time-zone versions and labels any current-rule reinterpretation as a new analytical view.

### Example 10

A migration assigns `valid_from = created_at` to every legacy row. Source review shows created time was load time and historical effective dates are unavailable. The target records validity as unknown before migration, retains source lineage, and discloses the reliable horizon instead of fabricating history.

## Cross-Program Connections

- **Database engineering:** temporal tables, ranges, exclusion constraints, indexes, transactions, query optimization, and restoration implement histories.
- **Data engineering:** event time, watermarks, windows, slowly changing dimensions, CDC, late data, backfill, replay, and point-in-time joins depend on temporal semantics.
- **API and service engineering:** as-of parameters, effective dates, versioned resources, events, idempotency, and compatibility expose time to consumers.
- **Platform engineering:** clock synchronization, schema registries, time-zone data, retention, archive, replay, policy, and observability support temporal controls.
- **Distributed systems:** causality, logical clocks, consensus order, clock skew, partitions, and retries constrain time claims.
- **Security and privacy:** historical access, linkability, retention, deletion, redaction, legal hold, and audit require explicit temporal scope.
- **Programming languages:** interval types, algebraic variants, immutable versions, date/time libraries, precision, and property tests encode rules.
- **Systems engineering:** lifecycle states, configuration baselines, effectivity, traceability, maintenance history, hazards, and evidence use temporal models.

## References

1. Allen, J. F., “Maintaining Knowledge about Temporal Intervals,” *Communications of the ACM*, 26(11), 1983. <https://doi.org/10.1145/182.358434>
2. Snodgrass, R. T., *Developing Time-Oriented Database Applications in SQL*, Morgan Kaufmann, 2000. <https://www.cs.arizona.edu/~rts/tdbbook.pdf>
3. ISO/IEC, *9075-2:2023 Information technology—Database languages SQL—Part 2: Foundation*, 2023. <https://www.iso.org/standard/76584.html>
4. W3C, *Time Ontology in OWL*, Candidate Recommendation Draft, 2022. <https://www.w3.org/TR/owl-time/>
5. Klyne, G., and Newman, C., *RFC 3339: Date and Time on the Internet: Timestamps*, IETF, 2002. <https://www.rfc-editor.org/rfc/rfc3339.html>
6. Internet Assigned Numbers Authority, *Theory and Pragmatics of the tz Code and Data*, current web edition. <https://www.iana.org/time-zones/theory>
7. PostgreSQL Global Development Group, *Range Types and Date/Time Types*, current documentation. <https://www.postgresql.org/docs/current/rangetypes.html>
8. Fowler, M., *Bitemporal History*, 2021. <https://martinfowler.com/articles/bitemporal-history.html>

## Exercises

### Exercise 1

Model bitemporal salary history where a raise recorded on 1 August as effective 1 August is corrected on 10 August to have been effective 1 July. Show the valid and recorded intervals and answer two as-of questions.

### Exercise 2

Design temporal constraints for room reservations using half-open intervals. Cover adjacency, overlap, cancellation, open-ended holds, concurrency, time zone, precision, and boundary tests.

### Exercise 3

Model a recurring 09:00 appointment in `America/New_York` for one year. Explain UTC conversion, daylight-saving gaps/folds, time-zone updates, cancellation exceptions, and reproducible history.

### Exercise 4

Compare audit log, event history, valid-time state, system-versioned state, and bitemporal state for customer addresses. State which questions each can answer and where evidence remains insufficient.

### Exercise 5

Plan migration of legacy policy records with inclusive end dates, sentinel `9999-12-31`, overlaps, date-only values, unknown zones, and no recorded history. Include conversion, quarantine, validation, disclosure, rollback, and protection.

## Answers to the Exercises

### Answer 1

Assume old salary 100 and new salary 110. Before 1 August the system records 100 valid `[begin, 1 Aug)` and 110 valid `[1 Aug, infinity)`, both with recorded interval beginning when entered and ending 10 August for the belief being corrected. At recorded time 10 August, append the revised view: 100 valid `[begin, 1 Jul)` and 110 valid `[1 Jul, infinity)`, each with recorded interval `[10 Aug, infinity)`. Exact implementation may split rows while preserving assertion identity and provenance.

At valid 15 July and recorded 5 August, the answer is 100 because the correction was not yet recorded. At valid 15 July and recorded 11 August, the answer is 110. Both answers state currency, employment agreement, source, authority, granularity, and query snapshot. The correction event links old and new assertions; it does not erase the invoice or payroll decisions made under earlier knowledge.

### Answer 2

Represent each active reservation as `[start,end)` over instants, with room, reservation identity, named-zone civil intent where needed, status, authority, and recorded history. Reservations for one room conflict when `a.start < b.end` and `b.start < a.end`; `[10:00,11:00)` and `[11:00,12:00)` are adjacent and permitted. Require `start < end`. An open-ended hold uses an explicit unbounded endpoint and a separate hold policy, not a magic date.

Cancellation ends or supersedes validity under a recorded transition; retain prior belief if decisions require it. Enforce exclusion atomically under concurrent inserts, including bulk paths. Test exact shared endpoints, one precision unit around them, contained intervals, equal intervals, unbounded bounds, cancellation races, zone gaps/folds, and restoration. Specify cleanup for expired holds and distinguish room-local schedule from normalized instant.

### Answer 3

Store recurrence rule, local time 09:00, IANA zone `America/New_York`, start/end local dates, duration semantics, time-zone database version or update policy, and exception identities. Generate each occurrence by resolving local civil time under the applicable zone rules, then store or derive its UTC instant. Offsets change across daylight saving, so one fixed UTC time does not preserve 09:00.

Although 09:00 normally avoids gaps/folds, the general resolver must define nonexistent and duplicate local-time behavior for rule changes and other schedules. A cancellation targets a recurrence occurrence identity rather than merely an old UTC value. Preserve generated-version history when published appointments must be reproducible; future occurrences may be regenerated after rule updates under approved policy. Record which rule set produced notifications and reconcile changed future times with consumers.

### Answer 4

An audit log can show who changed address fields and when recorded, but may not reliably state when an address was valid or support efficient as-of queries. An event history can reconstruct state if events are complete, ordered under required scope, versioned, corrected, and replayable; otherwise it provides occurrence evidence only. Valid-time state answers which address is asserted for a domain time under a current perspective.

System-versioned state answers what row image the database held at a system time, subject to product semantics and bypass coverage, but not necessarily business validity. Bitemporal state answers what address was valid at `v` according to records at `r`, supporting retroactive correction. None alone proves residence, delivery suitability, or source authority. Each needs identity, address type, valid/recorded semantics, provenance, missingness, protection, retention, and verification against authorized sources.

### Answer 5

Inventory each field's actual semantics and source. Convert inclusive date-only `[start,end]` to half-open `[start,end+1 day)` only where whole-day Gregorian semantics are proven. Map sentinel `9999-12-31` to explicit unbounded only when source rules say “continues”; otherwise preserve unknown. Partition by temporal key and detect overlaps, gaps, duplicates, reversed and empty intervals. Quarantine ambiguous cases with lineage rather than choosing winners.

Unknown zones cannot be reconstructed from offsets or locations without evidence; retain local date/time and uncertainty. No recorded history means the migration can establish a new recorded interval at cutover but cannot recreate prior beliefs. Define reliable-history horizon and limitations. Capture concurrent source changes, validate counts, keys, interval relations, boundary queries, samples, current state, and protected records. Run dual queries, preserve rollback mappings and source snapshots under authorized retention, restrict historical access, and verify deletion, archive, recovery, and consumer results before cutover.
