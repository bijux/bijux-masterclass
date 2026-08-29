---
module_id: DE-002
program: Data Engineering
level: 1
module_number: 2
title: Rows, Columns, Records, and Events
status: complete
last_verified: 2026-08-29
---

# Rows, Columns, Records, and Events

## One-Page Review

### Governing question

How should a data engineer choose and preserve the meaning of rows, columns, records, and events while data moves between logical models and physical layouts?

### Essential definitions

- A **field** is a named or positioned component with a declared meaning and value domain.
- A **record** is one bounded collection of fields interpreted together.
- A **row** is a record-like observation aligned to a tabular schema and a declared grain.
- A **column** is the values of one field across many rows; it can be a logical attribute and a physical vector.
- **Grain** states exactly what one row or record represents.
- An **event** is an immutable claim that a named occurrence happened, with identity, source, type, time semantics, and payload.
- A **snapshot** represents state at a boundary; a **change record** represents a transition or captured mutation.
- **Row-oriented** and **column-oriented** describe physical adjacency, not different business truth.

### Central model, mechanism, or theorem

Treat a dataset as `schema + grain + identity + time + representation`. A lossless row-to-column transpose preserves the same cells when row alignment, field identity, type, nullability, and ordering metadata are retained. Turning events into current-state rows is not a transpose: it is a stateful fold over an ordered, deduplicated history under domain transition rules.

### Critical invariants

- Every row has one explicit grain and every field is meaningful at that grain.
- Columns remain aligned: position `i` across all columns describes one row.
- Record field names, types, units, and null meanings survive serialization boundaries.
- Event identity is stable within a source namespace and differs from delivery identity.
- Event occurrence time, recording time, and processing time are not conflated.
- Events describe occurrences; mutable snapshots describe state at a stated boundary.
- Replayed or duplicated delivery does not create a second business occurrence.
- Physical reorientation preserves values but does not silently change semantics or precision.

### Common failures

Common failures are calling every object an event, using one row for mixed grains, treating a column file as a semantic model, losing row alignment during independent column processing, overwriting history with current state, using processing time as occurrence time, confusing message retries with new events, omitting units and null meaning, and assuming nested records flatten without ambiguity.

### Compact example

Three order events—`OrderPlaced`, `PaymentCaptured`, and `OrderCancelled`—are three occurrence records even if they share one `order_id`. A current-order snapshot may be one row per order with a latest status. Producing that row requires ordering rules, duplicate handling, and a transition policy; it cannot be obtained by merely choosing different columns.

### Connections

[DE-001](001-data-producers-consumers-and-lifecycle.md) establishes producer, consumer, and version boundaries. [DE-003](../ROADMAP.md) develops textual encodings. The relational meaning of rows connects to [Database Engineering](../../18-database-engineering/ROADMAP.md); event protocols connect to [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md).

## Governing Question

“The data is tabular” can describe a logical relation, a dataframe API, a CSV rendering, a database result, or a columnar memory batch. “The data is events” can describe historical domain occurrences, change-data-capture records, telemetry samples, or merely messages on a broker. These labels are too broad to establish meaning.

The governing problem is to specify what one observation represents, how fields belong to it, what identity and time mean, and which transformations preserve or derive meaning. A physical representation can change without changing facts: the same batch may be accessed row by row or stored as adjacent typed columns. By contrast, converting an occurrence history into a current snapshot changes the information model and demands domain rules.

Codd's [relational model](https://doi.org/10.1145/362384.362685) separates logical tuples and attributes from physical organization. Apache Arrow's current [columnar-format specification](https://arrow.apache.org/docs/format/Columnar.html) defines language-independent arrays and record batches for efficient memory interchange. The CloudEvents [core specification](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md) standardizes event context for interoperability. They address different layers and should not be collapsed into one vocabulary.

## Why This Matters

Representation mistakes become semantic defects downstream. If an order table mixes one row per order with one row per item, summing order totals over rows double-counts. If two column arrays are filtered with different masks, position alignment breaks and values are assigned to the wrong entity. If a retry receives a new event identity, an at-least-once transport can manufacture duplicate business effects.

Events and snapshots answer different questions. An event history can answer what occurred, in which declared order, and what was known at a time—if the history is complete and corrections are modeled. A snapshot efficiently answers current state at one boundary but normally cannot reconstruct discarded transitions. Keeping only events shifts state derivation and replay obligations to consumers; keeping only snapshots discards history. Many systems require both, with explicit derivation lineage.

Physical orientation affects performance. Row adjacency favors retrieving many fields for a small number of records and appending complete records. Column adjacency favors scanning one or a few fields across many observations, compact typed storage, vector operations, and field-specific encoding. These are workload properties, not guarantees: nested values, variable widths, selection patterns, compression, caches, and implementation overhead alter results.

Schemas bind representations. A numeric array without a unit cannot distinguish cents from euros. A timestamp without an instant/local-time interpretation is not portable. A null bitmap can represent absence mechanically while leaving “unknown,” “not applicable,” “not yet observed,” and “redacted” semantically ambiguous. Data engineering owns the fidelity of both values and their interpretation.

The distinction also affects compatibility. Adding an optional record field may be mechanically readable by old consumers, yet change business meaning if absence is interpreted incorrectly. Changing an event type from “requested” to “completed” while retaining its name is syntactically compatible and semantically breaking. Compatibility is a producer-consumer relationship over retained data, not only a parser property.

## Prerequisites and Retrieval

You should understand arrays, dictionaries, tuples, schemas, identifiers, timestamps, and basic database tables. Recall that a value's physical bytes, logical type, and domain meaning are distinct. Recall from [DE-001](001-data-producers-consumers-and-lifecycle.md) that a producer is defined at a boundary and that versioned lineage is required for reproducible derivation.

This chapter uses “record” generically and “row” for schema-aligned tabular observations. Specific file formats and libraries may use these words differently; when reading a specification, prefer its defined terminology.

## Learning Objectives

After completing this module, you should be able to:

- state the grain and identity of a row or record;
- distinguish logical attributes from physical column vectors;
- explain when row/column transposition is lossless;
- identify alignment, type, nullability, unit, and nesting hazards;
- distinguish events, messages, change records, commands, and snapshots;
- define event identity and multiple time coordinates;
- derive current state from events with explicit ordering and transition rules;
- compare row-oriented and column-oriented layouts from workload evidence;
- design validation for representation conversions and replay;
- scope human review for high-consequence record and event semantics.

## Core Exposition

A **field** couples a value position with meaning. Named fields make association explicit; positional fields require an external schema. A field definition includes a stable name or identifier, logical domain, physical encoding, nullability, unit or reference system, constraints, and evolution rules where relevant. “`amount: integer`” is incomplete without scale, currency, sign policy, and rounding boundary.

A **record** groups fields that should be interpreted as one observation. Records may be flat or nested, fixed or extensible, ordered or name-addressed depending on their model. A Python dictionary, protocol message, database tuple, and log entry can each carry records, but their equality, missing-field, ordering, and type behavior differ.

A **row** is a record placed in a tabular model. Its most important property is grain: the sentence “one row represents …”. Examples include one row per accepted order, per order line, per account-day balance, per sensor-reading occurrence, or per customer at month end. A table can contain a unique identifier without having clear grain; grain includes the temporal and aggregation boundary.

Mixed grain is a common error. Suppose an order header is repeated on each item row. `order_total` is then at order grain while `item_quantity` is at item grain. Summing both columns together treats repetition as new facts. The design can separate header and lines, mark nonadditive values, or define a deliberate denormalized row and its aggregation rules. Convenience does not remove the mismatch.

A **column** has two meanings. Logically, it is one attribute across a row set. Physically, it may be a contiguous or segmented typed array plus validity and offset buffers. Independent columns form a table only with a shared length and row-position alignment. Sorting or filtering one vector alone silently reassigns values to other fields.

Row orientation stores fields of an observation near one another. Column orientation stores values of an attribute near one another. A logical table does not mandate either. A database may combine row pages, columnar indexes, compressed segments, caches, and materialized projections. A pipeline may read row-oriented JSON and produce an Arrow record batch without changing the declared observations.

A row-to-column transpose is lossless under explicit conditions. Given rows `r_0 ... r_{n-1}` and schema fields `f_0 ... f_{m-1}`, column `C_j[i] = r_i[f_j]`. Reconstructing `r_i` from every `C_j[i]` succeeds if field identity, row count, common position, value domain, null state, and any required record order are preserved. Nested lists need offsets; variable-width values need offsets or lengths; dictionaries need mapping identity; extensions need metadata.

Apache Arrow version 1.5, in the documentation published with Arrow 25.0.1 and checked 2026-08-29, specifies arrays as same-typed value sequences and describes physical buffers, validity, variable-size offsets, nested layouts, record batches, and schemas. It promotes adjacency and vector-friendly access, while explicitly leaving mutation coordination to implementations. Arrow does not decide the business grain or truth of a field.

An **event** is a record whose asserted meaning is an occurrence. Its type should be past-tense or otherwise unambiguously factual: `OrderAccepted` or `TemperatureObserved`. A command such as `ShipOrder` requests an action and may be rejected; it is not evidence that shipping occurred. A notification reports something to an audience but may omit the durable identity or history required for event replay.

An event envelope and its data serve different purposes. Context supports routing, deduplication, interpretation, and provenance without understanding the whole payload. CloudEvents 1.0.2 requires `id`, `source`, `specversion`, and `type`; the combination of `source` and `id` is defined to be unique for each distinct event. Optional `subject`, `time`, `datacontenttype`, and `dataschema` add scope and interpretation. Conforming shape does not prove the event is true, authorized, complete, or delivered once.

Identity needs namespaces. A database row key, event identifier, aggregate identifier, and delivery/message identifier answer different questions. Multiple delivery attempts of one event retain the event's identity while transport attempt identifiers may change. A corrected assertion normally becomes a new event referencing the superseded event; rewriting the old bytes destroys auditability unless the governed system explicitly uses mutable logs.

Time also has coordinates:

- **occurrence time:** when the represented real or domain event happened;
- **recorded time:** when the producer committed or recorded it;
- **publication time:** when it became available at the boundary;
- **ingestion time:** when a pipeline accepted it;
- **processing time:** when an operator handled it;
- **valid time:** when the represented fact applies in the domain;
- **system time:** when a database version was current in the recording system.

One timestamp cannot safely stand for all of them. Clocks can be imprecise or skewed, and late events are normal. An event-time sequence may require a source sequence, causal dependency, or domain ordering rule rather than timestamps alone.

A **snapshot** records state at a boundary: current customer profile, closing balance, or inventory at midnight. It can be full or incremental. A **change record** describes a captured before/after mutation or log operation; it may expose storage mechanics rather than a domain event. “Row updated” does not explain whether an order was corrected, fulfilled, or merely reindexed.

Folding events into state needs an initial state `s_0` and transition function `delta(s,e)`. For an ordered history `e_1 ... e_n`, `s_n = delta(...delta(delta(s_0,e_1),e_2)...,e_n)`. The fold also needs event selection, deduplication, ordering, versioned transition logic, invalid-transition policy, and completeness bounds. If these are missing, “replay” is not reproducible.

Events may be immutable while their interpretation evolves. A schema identifier and producer version help select a decoder, but reference data and business rules may also be versioned. Reprocessing old events with today's tax or geography rules can produce a valid new interpretation that differs from the historically published result. A pipeline must say whether it reproduces old computation or restates history under new policy.

Nested records complicate flattening. A customer with three addresses can become three rows, arrays inside one row, or a separate address relation. Flattening can create Cartesian multiplication when two repeated children are expanded together. Field paths can collide after delimiter-based naming. The target grain and reconstruction requirement should decide the method.

Null and missing differ. A missing field may mean an older schema, intentional omission, or absent producer knowledge. An explicit null is a carried marker. An empty string or zero is a value. Some formats collapse distinctions; some preserve them. The boundary contract must define which distinctions matter before conversion.

## Definitions and Notation

Let schema `S = (f_1:D_1, ..., f_m:D_m)`. A record `r` conforms when every required `f_j` has one domain-valid value or allowed null state, optional/missing behavior follows the schema, and no unrecognized field violates the evolution policy.

Let a batch contain records `R = (r_0, ..., r_{n-1})`. Its column representation is `C_j = (r_0[f_j], ..., r_{n-1}[f_j])`. Alignment invariant: every `|C_j| = n` and position `i` refers to the same observation across columns.

Represent an event as `e = (source, id, type, subject, t_occ, t_rec, schema, data)`. Distinct occurrence identity satisfies uniqueness of `(source,id)` within the governed history. Let `delivery(e,k)` be delivery attempt `k`; it is not a new `e`.

Let `fold_delta(s_0,H)` apply versioned transition `delta` to a deduplicated, validly ordered history `H`. A derived snapshot is reproducible only when `s_0`, `H` identity/order, `delta` version, configuration, and invalid-event policy are recorded.

## Mechanisms, Invariants, or Proof Structure

For a representation boundary, review four layers:

1. **Semantic layer:** grain, identity, field meanings, units, nulls, and time.
2. **Logical layer:** record, relation, event, snapshot, or change model.
3. **Physical layer:** row/column buffers, encoding, nesting, ordering, and partitions.
4. **Operational layer:** versioning, delivery, deduplication, replay, quarantine, and evidence.

A lossless conversion proof uses round-trip and invariant checks. Validate input conformance, convert without coercion, reconstruct, and compare every value plus missing/null state under the source semantics. Include empty batches, zero fields if supported, nested empties, boundary numerics, non-ASCII text, nulls, and malformed offsets. A byte round trip is stronger than a displayed-value comparison but still does not prove domain meaning.

For event-derived snapshots, separately check:

- identity uniqueness and duplicate handling;
- ordering and tie policy;
- allowed transition preconditions;
- determinism for fixed versioned inputs;
- completeness or stated watermark/cutoff;
- correction and retraction semantics;
- lineage from each state field to events and rules.

The executable model transposes schema-aligned rows into columns and independently reconstructs them. It then validates unique event identity and folds order events into a current-state record. The same event delivered twice is deduplicated by `(source,id)`.

<!-- bijux-verify: {"id":"records-columns-events","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"columns={'order_id': ('o1', 'o2'), 'amount_cents': (1250, 800)}\nround_trip=True\nstate=(('o1', 'paid'), ('o2', 'placed'))\ndistinct_events=3 deliveries=4\n","stderr":""}} -->
```python
schema = ("order_id", "amount_cents")
rows = (
    {"order_id": "o1", "amount_cents": 1250},
    {"order_id": "o2", "amount_cents": 800},
)

if any(tuple(row) != schema for row in rows):
    raise ValueError("record fields or order differ from schema")
columns = {field: tuple(row[field] for row in rows) for field in schema}
if len({len(values) for values in columns.values()}) != 1:
    raise ValueError("columns are not aligned")
reconstructed = tuple(
    {field: columns[field][index] for field in schema}
    for index in range(len(rows))
)

deliveries = (
    {"source": "orders", "id": "1", "order_id": "o1", "type": "placed"},
    {"source": "orders", "id": "2", "order_id": "o2", "type": "placed"},
    {"source": "orders", "id": "3", "order_id": "o1", "type": "paid"},
    {"source": "orders", "id": "3", "order_id": "o1", "type": "paid"},
)
unique = {}
for event in deliveries:
    key = (event["source"], event["id"])
    if key in unique and unique[key] != event:
        raise ValueError("one event identity has conflicting content")
    unique[key] = event

state = {}
allowed = {None: {"placed"}, "placed": {"paid"}}
for event in unique.values():
    order_id = event["order_id"]
    prior = state.get(order_id)
    if event["type"] not in allowed.get(prior, set()):
        raise ValueError("invalid order transition")
    state[order_id] = event["type"]

print(f"columns={columns}")
print(f"round_trip={reconstructed == rows}")
print(f"state={tuple(sorted(state.items()))}")
print(f"distinct_events={len(unique)} deliveries={len(deliveries)}")
```

The code assumes insertion order is the authoritative event order, exact Python types are acceptable, and the event set is complete. Real systems need explicit sequences or ordering keys, schema versions, timestamps with defined semantics, persistent deduplication, transactional state updates, correction rules, and provenance. A successful trace is empirical evidence for these inputs, not proof that arbitrary histories or production transports are correct.

## Alternatives and Trade-Offs

**Rows versus columns.** Row layouts favor point retrieval and whole-record mutation; column layouts favor scans, vector operations, and encoding by value distribution. Hybrid formats and late materialization combine them. Benchmark the real projection, selectivity, nesting, and hardware.

**Flat versus nested records.** Flat records integrate easily with tabular operations. Nested records preserve aggregate structure and optional/repeated groups. Flattening improves some queries but can duplicate parent facts and complicate round trips.

**Events versus snapshots.** Events retain occurrence history and enable alternate projections when complete. Snapshots simplify current reads and bound replay. Periodic snapshots plus an event suffix can reduce recovery time while keeping history, but snapshot version and event cutoff must align.

**Domain events versus change records.** Domain events express business occurrences and stable consumer meaning. Change-data-capture records can be generated reliably from database commits but expose table operations and schema. Translating CDC into domain events requires an owned semantic transformation.

**Wide versus narrow records.** Wide records reduce joins and may fit consumer access, but mix grains and evolution ownership easily. Narrow records preserve focused meaning but require composition. Choose from semantic ownership before storage convenience.

**Positioned versus named fields.** Position is compact and fast when schema identity is exact. Names improve inspectability and some evolution paths but cost bytes and can still be ambiguous. Stable numeric field identifiers can separate wire identity from display names.

**Immutable correction versus in-place update.** Append-only corrections preserve evidence and replay but require consumers to interpret supersession. In-place updates simplify current views but erase history unless versions are retained elsewhere. Regulatory and domain authority determine which evidence must persist.

## Failure Modes and Misconceptions

1. **A row is self-explanatory.** Without grain, identity, units, and time, its fields can be combined incorrectly.
2. **Columnar means analytical semantics.** Orientation is physical; transactional or analytical meaning comes from workload and model.
3. **Columns can be transformed independently.** They may be processed separately only while a common selection/permutation preserves row alignment.
4. **Every broker message is an event.** Commands, retries, control messages, and snapshots can travel through the same transport.
5. **Event ID equals entity ID.** Many events can describe one entity; occurrence identity and subject identity differ.
6. **Exactly one event follows from exactly one delivery.** Delivery semantics and business occurrence identity are separate.
7. **A timestamp orders everything.** Clock resolution, skew, ties, late arrival, and causal relations require explicit policy.
8. **CDC is a domain event log.** Storage changes can omit intent and include implementation-only mutations.
9. **Null, missing, and empty are interchangeable.** Collapsing them can change eligibility, counts, and compatibility.
10. **A round trip proves semantic preservation.** It checks represented distinctions, not whether the source field meant what the schema claims.

## Worked Examples

### Example 1

**Question:** What is the grain of a row with `customer_id`, `month`, and `closing_balance`?

**Reasoning:** A defensible sentence is “one row per customer per calendar month at the declared closing boundary.” The month timezone, currency, account aggregation, and correction policy complete the meaning.

**Conclusion:** Column names suggest but do not fully establish grain.

### Example 2

**Question:** Why does filtering only the `amount` vector corrupt a column batch?

**Reasoning:** The retained positions no longer align with `order_id` and other fields. Compute one Boolean mask or index vector from the row predicate and apply it to every column.

**Conclusion:** Column independence is constrained by a shared row-position invariant.

### Example 3

**Question:** Is `{"order_id":"o1","status":"paid"}` an event?

**Reasoning:** It could be a current snapshot. An event would name an occurrence such as `PaymentCaptured`, carry distinct occurrence identity and source, define time, and state what the payload asserts. Shape alone is insufficient.

**Conclusion:** Eventhood is semantic, not a JSON-object property.

### Example 4

**Question:** A `PaymentCaptured` event is delivered three times. How many business events exist?

**Reasoning:** One if all attempts retain the same trusted `(source,id)` and content. The consumer needs durable deduplication around effects; three delivery records can still be retained operationally.

**Conclusion:** Delivery multiplicity does not determine occurrence multiplicity.

### Example 5

**Question:** May processing time replace missing occurrence time?

**Reasoning:** Only if labeled as processing time. It gives an upper observation boundary, not when the domain occurrence happened. Inferring occurrence can distort windows, lateness, and causal analysis.

**Conclusion:** Record available coordinates without renaming one into another.

### Example 6

**Question:** Flatten a customer with two addresses and three phone numbers into one table.

**Reasoning:** Expanding both arrays produces six combinations unless their elements have a pairing relation. Separate child tables preserve two and three facts; nested arrays preserve the aggregate; a deliberate pairing key can justify joined rows.

**Conclusion:** Naive flattening can manufacture a Cartesian product of unrelated facts.

### Example 7

**Question:** Does converting two rows to two same-length columns guarantee losslessness?

**Reasoning:** No. Field names, types, null state, order/alignment, precision, timezone, encoding, and nested offsets must also survive. Equal lengths are one invariant, not the whole contract.

**Conclusion:** Losslessness is relative to every represented distinction consumers require.

### Example 8

**Question:** A CDC record says `orders.status` changed from `pending` to `paid`. Is that equivalent to `PaymentCaptured`?

**Reasoning:** Not necessarily. A repair, migration, test write, or reconciliation could update the field. The domain service must establish whether a capture occurred and publish or derive the event under owned rules.

**Conclusion:** Storage transition and domain occurrence require an explicit semantic bridge.

### Example 9

**Question:** A clinical pipeline converts medication-administration events into one current patient row. Is a successful replay enough?

**Reasoning:** No. Dose identity, corrections, late charting, units, route, occurrence/recorded time, canceled administrations, source completeness, and patient matching require named clinical, pharmacy, data, and safety review. Independent reconciliation and adverse boundary cases are necessary. This chapter claims no external review.

**Conclusion:** High-consequence event folds require domain authority beyond technical determinism.

### Example 10

**Question:** When is a columnar representation a poor choice?

**Reasoning:** A workload that fetches and mutates complete individual records with little scanning may pay reconstruction and update costs without using column locality. Small data can make orientation irrelevant. Measurement on representative operations decides.

**Conclusion:** Physical orientation follows workload evidence, not fashion.

## Cross-Program Connections

[Database Engineering](../../18-database-engineering/ROADMAP.md) formalizes rows as tuples under relational schemas and develops physical row/column storage later. [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) explains arrays, locality, and representation invariants beneath column buffers.

[API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) owns protocol envelopes, commands, event interfaces, and consumer compatibility. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) develops ordering, duplication, clocks, logs, and delivery failure. Data engineering consumes those mechanisms while owning pipeline-level schema, derivation, quality, and replay.

[Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) governs enterprise semantic ownership and canonical concepts. [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md) implements distributed columnar execution, partitioning, shuffles, and streaming state at scale.

## References

- E. F. Codd, [*A Relational Model of Data for Large Shared Data Banks*](https://doi.org/10.1145/362384.362685), *Communications of the ACM* 13(6), 1970. Primary source separating relational tuples and attributes from physical access paths.
- Apache Arrow Project, [*Arrow Columnar Format, format version 1.5*](https://arrow.apache.org/docs/format/Columnar.html), documentation published with Arrow 25.0.1, checked 2026-08-29. Official current memory-layout, array, buffer, nesting, and record-batch specification.
- Cloud Native Computing Foundation CloudEvents project, [*CloudEvents Core Specification 1.0.2*](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md), 2022. Official event context, identity, source, type, time, schema, and data rules.
- Cloud Native Computing Foundation CloudEvents project, [*CloudEvents Primer 1.0.2*](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/primer.md), 2022. Official explanatory rationale for event interoperability and context.
- World Wide Web Consortium, [*PROV-DM: The PROV Data Model*](https://www.w3.org/TR/prov-dm/), W3C Recommendation, 2013. Standard conceptual model for entities, activities, agents, derivation, and responsibility.
- Martin Kleppmann, [*Designing Data-Intensive Applications*](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/), O'Reilly Media, 2017. Durable treatment of encoding, dataflow, logs, streams, time, and derived state.
- Ralph Kimball and Margy Ross, [*The Data Warehouse Toolkit*, third edition](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/books/data-warehouse-dw-toolkit/), Wiley, 2013. Durable source on declaring grain and interpreting analytical rows.

## Exercises

### Exercise 1

For a dataset with `sensor_id`, `observed_at`, `temperature_value`, and `unit`, write a complete grain sentence and identify field, row, column, and record.

### Exercise 2

Given three aligned columns of length four, derive the reconstruction rule and list checks needed before removing rows whose quality flag is false.

### Exercise 3

Diagnose an “event” stream whose messages contain entity ID, current status, and publication timestamp but receive a fresh message ID on every retry. Propose a durable contract.

### Exercise 4

Compare event history, periodic snapshots, and database change records for reconstructing customer-account state. Include semantics, storage, replay, correction, and operational trade-offs.

### Exercise 5

An autonomous vehicle pipeline converts sensor detections into columnar batches, tracked-object events, and current world-model snapshots. Specify invariants, failure cases, evidence, and named human-review roles required before claiming the conversion safe.

## Answers to the Exercises

### Answer 1

One row represents one temperature observation reported by one sensor for one explicitly defined occurrence instant, before any aggregation. Each named component is a field with a domain: sensor identifier, instant, numeric value, and unit code. The record is the four fields interpreted together; the row is that record aligned to the dataset schema. A column is one field's values across all observation rows. The contract must also state timestamp precision/timezone, allowed units and conversion policy, sensor namespace, null behavior, calibration/version context, and whether repeated readings at one instant are distinct.

### Answer 2

For columns `C_1,C_2,C_3` and schema `f_1,f_2,f_3`, reconstruct row `r_i = {f_1:C_1[i], f_2:C_2[i], f_3:C_3[i]}` for `0 <= i < 4`. First require equal lengths, stable field identity, domain/null conformance, and common row-position provenance. Derive one retained-index sequence `I = [i | quality[i] is true]`, validate the quality field's missing-value policy, and build every output column as `C_j[I]` using exactly the same ordered indexes. Check output alignment, row count, boundary empty/all-kept cases, and round-trip selected rows against a record-oriented oracle.

### Answer 3

The messages are retryable current-state notifications, not yet durable occurrence events. Fresh retry IDs prevent business deduplication, publication time does not identify the status transition time, and a snapshot cannot say which transition occurred. Define a source namespace and stable event ID per distinct transition, subject/entity ID separately, event type such as `OrderPaid`, occurrence and recorded times, schema version, payload meaning, and correction/supersession policy. Retries retain event identity and content while carrying separate delivery-attempt metadata. If the producer can only publish current snapshots, label them snapshots with version/observation boundaries instead of inventing event history.

### Answer 4

Event history preserves named occurrences and supports alternate deterministic projections when identity, ordering, completeness, and versioned rules are available; it costs storage and replay complexity. Periodic snapshots bound recovery and simplify current reads, but must identify the included event frontier and derivation version and cannot replace older history when audit is required. Database change records can be captured reliably near commits and reproduce table mutations, yet expose storage schemas and may not express domain intent. Corrections can be compensating/superseding events, replacement snapshots, or subsequent row changes; consumers need explicit precedence. A robust design often retains governed source changes/events, derives domain history, and publishes aligned snapshots with lineage rather than declaring one representation universally authoritative.

### Answer 5

At the detection batch boundary, require schema/type/unit calibration, equal column lengths, timestamp and sensor-frame definitions, null masks, object-candidate identity, and lossless row/column correspondence. At the event boundary, require stable source/event identity, tracked-object subject identity, ordering/late-data rules, coordinate-frame transformations, association confidence, correction/retraction, and duplicate delivery handling. At the snapshot boundary, require a versioned deterministic fold, completeness frontier, bounded staleness, valid kinematic/state invariants, and lineage to detections and model versions. Test empty/saturated batches, dropped or duplicated frames, clock skew, wraparound, occlusion, identity swaps, conflicting sensors, malformed offsets, precision loss, replay, restart, and target-hardware deadlines; compare with independent record-oriented and scenario oracles. Named reviewers must include perception and tracking specialists, vehicle-control/system-safety engineers, data/format engineers, test and simulation owners, and the independent assurance authority required by the applicable regime. Passing conversion tests alone does not establish safe vehicle behavior, and no external human review is claimed here.
