---
module_id: DE-011
program: Data Engineering
level: 1
module_number: 11
title: Grain and the Meaning of a Row
status: complete
last_verified: 2026-09-02
---

# Grain and the Meaning of a Row

## One-Page Review

### Governing question

What exactly does one row assert, which key identifies that assertion, and which joins and aggregations preserve its meaning without omission or double counting?

### Essential definitions

- **Grain** is the precise business-level proposition represented by one row: the entity, event, observation, relationship or snapshot at stated dimensions and time semantics.
- A **grain declaration** is a sentence such as “one row per fulfilled order line at fulfillment event time,” written before choosing columns.
- A **grain key** is the smallest governed attribute set that uniquely identifies rows at the declared grain. It may be a natural, composite or generated identity, but its semantics must be known.
- A **fact** is an observation or measurement at a declared grain. A **dimension attribute** describes or classifies entities used to filter and group facts.
- **Atomic grain** is the lowest level captured by the business process and available source evidence, before analytical summarization.
- A **transaction fact row** records one event. A **periodic snapshot row** records state or measurements for a regular period. An **accumulating snapshot row** tracks one process instance across milestones.
- A **functional dependency** $G\rightarrow A$ means one grain-key value determines one value of attribute $A$ in the relation.
- **Join cardinality** describes how many matching rows each side can contribute. A **fanout** occurs when one input row matches multiple rows and is replicated.
- An **additive measure** may be summed across designated dimensions at its grain. Semi-additive and non-additive measures require narrower aggregation rules.
- **Summarization** transforms a lower-grain relation to a coarser grain by grouping and aggregating.
- A **bridge** represents a governed many-to-many relationship; allocation weights may be required before measures can be summed through it.
- A **mixed-grain table** contains rows or columns whose propositions cannot share one consistent grain, making ordinary aggregation ambiguous.

### Central model, mechanism, or theorem

Represent the row contract as

$$
R=(P,G,T,D,M,U,V),
$$

where $P$ is the row proposition, $G$ its unique key, $T$ temporal semantics, $D$ dimensional context, $M$ measures, $U$ units/aggregation rules and $V$ version. A valid table satisfies

$$
\forall r_1,r_2:\ G(r_1)=G(r_2)\Rightarrow r_1=r_2
$$

under the table's identity semantics.

A join is safe for an additive measure from left relation $L$ only when every left row contributes with total multiplicity/weight one at the output grain. If left row $l$ matches $d(l)>1$ right rows and its measure is repeated, post-join summation contributes $d(l)m(l)$ rather than $m(l)$. Pre-aggregate, deduplicate the right side, allocate weights summing to one, or keep the measure out of that path.

### Critical invariants

- Every table and query result has a plain-language grain declaration independent of its current columns.
- The grain key is unique, non-null where identity requires it, enforced or continuously tested, and stable across retries.
- All facts and dimension references in one row are valid at the same declared grain and time interpretation.
- Measures record units, null semantics and allowed aggregation dimensions; balances and ratios are not treated as universally additive.
- Every join has expected cardinality, unmatched policy and post-join row/mass reconciliation.
- Grouping keys explicitly declare the output grain; selected attributes are functionally dependent on them or deliberately aggregated.
- Window calculations normally preserve input row identity; grouping normally changes it. Their use is not interchangeable.
- Deduplication defines duplicate identity, source precedence and a deterministic survivor; `DISTINCT` is not a business rule.
- Snapshot rows identify period/as-of semantics and do not mix event flow with point-in-time stock.
- Many-to-many bridges prevent uncontrolled fanout and carry allocation when additive reporting requires it.
- Unknown/not-applicable dimension members remain explicit rather than making facts disappear in inner joins.
- Grain tests cover duplicates, omissions, fanout, temporal overlap, late changes and reconciliation to authoritative controls.

### Common failures

Defining grain as “whatever columns are present”; choosing dimensions before the business process and grain; declaring “one row per customer” while storing multiple addresses or periods; using a generated row ID to conceal duplicate business events; mixing order totals with order lines; summing inventory balances across dates; averaging precomputed averages; joining facts directly at incompatible grains; assuming a dimension key is unique without testing; joining a Type 2 dimension without an as-of predicate; using `SELECT DISTINCT` to hide fanout; deduplicating without deterministic precedence; treating row count as entity count; grouping by month while selecting an arbitrary day; counting non-null values when the metric is event rows; ignoring nested/repeated child grain; and publishing a wide table with transaction, daily and lifetime measures in one ambiguous row.

### Compact example

Two orders total 100 and 50 currency units. Their three lines total 60, 40 and 50. Joining order headers to lines yields three rows; summing repeated `order_total` after the join gives 250, while the correct order total is 150. Line revenue also sums to 150, but coincidence does not make the grains interchangeable. The order key is unique in headers; `(order_id,line_id)` is unique in lines. Metrics must be aggregated at their own grain before comparison or joined after safe summarization.

### Connections

[DE-002](002-rows-columns-records-and-events.md) introduces records and events; [DE-008](008-schemas-nullability-and-type-fidelity.md) defines key/type fidelity; [DE-009](009-time-time-zones-and-event-timestamps.md) supplies temporal semantics; [DE-010](010-designing-a-reproducible-data-boundary.md) makes grain tests replayable. The next modules develop facts, dimensions, star schemas and slowly changing dimensions. Relational constraints connect to [Database Engineering](../../18-database-engineering/ROADMAP.md), domain propositions to [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md), and metrics to [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md).

## Governing Question

If a reviewer points to one row, can the model owner finish the sentence “this row means exactly one …” without listing columns or saying “it depends”?

Grain is the semantic type of a row. It defines what can repeat, what must be unique, which facts belong together, how time applies and how joins should behave. A table name such as `sales`, `customer` or `activity` is not enough. `sales` might mean one payment, order, order line, shipment line, daily product-store summary or monthly account statement. Each supports different questions and aggregation.

The [Kimball four-step dimensional design process](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/four-4-step-design-process/) places “declare the grain” after selecting the business process and before identifying dimensions and facts. This order prevents available columns or desired dashboards from silently defining the model.

A useful declaration names the business event/state, identity, time role and inclusion rules: “one row per accepted meter reading emitted by a device, identified by `(device_id,reading_sequence)`, carrying source observation time and platform ingestion time.” It says more than “device by day,” which could describe event rows, daily aggregates or snapshots.

Once grain is explicit, database constraints and data tests can enforce parts of it. PostgreSQL's [constraint documentation](https://www.postgresql.org/docs/current/ddl-constraints.html) describes composite unique and primary keys. A constraint proves uniqueness under its database/null semantics; it does not prove that the chosen key matches the business proposition. That remains a modeling judgment supported by source evidence.

## Why This Matters

Most analytical overcounting is a grain error expressed through a join or aggregation. An order total repeated on every order line looks plausible until summed. A customer row repeated for each address makes `count(*)` an address count, not a customer count. A daily balance summed over a month becomes “balance-days,” not month-end balance.

Grain controls dimensionality. A monthly product target cannot be compared directly to daily store-product sales without choosing a common grain and allocation rule. Joining them on product alone repeats the target for every sale; joining on product and month still repeats it across stores and days unless it is first aligned or deliberately allocated.

Grain also controls correctness over time. A fact joined to a customer dimension with multiple historical versions needs an as-of rule; joining only by customer business key fans out. A periodic snapshot must say whether its date is start, end, observation time or reporting label. “Current status” cannot reconstruct past state.

Operationally, a stable grain key supports idempotent loads, corrections, deletion and lineage. If a retry generates a new surrogate row ID each time without a business event identity, duplicates appear valid. If the natural event lacks a stable identifier, the model needs an explicit deduplication key and acknowledged collision/omission risk.

Grain determines performance but should not be compromised casually for it. Atomic facts allow flexible aggregation; pre-aggregates serve known queries efficiently. Maintain both with clear lineage and reconciliation instead of mixing summary columns into atomic rows.

## Prerequisites and Retrieval

Retrieve the business process and owner; source system transactions/events/states; source primary/natural keys; retry and correction behavior; entity identifiers; event and ingestion timestamps; delete/tombstone semantics; sample duplicates and missing records; all source joins; table DDL and constraints; declared/current partitioning; row counts by source and period; distinct counts for candidate keys; null patterns; functional-dependency profiles; expected relationship cardinalities; dimensional keys; historical version intervals; measures, formulas, units and currencies; additivity rules; control totals; snapshot schedules and as-of definitions; nested/repeated fields; allocation rules; late-arriving behavior; deduplication precedence; current dashboards/queries; grouping/window logic; materialized aggregates; access/security filters; reconciliation tolerances; and consumers whose metrics would change.

Distinguish business process from source table; entity from event; event from state; state from snapshot; transaction grain from line grain; atomic detail from summary; natural key from surrogate key; row key from partition key; uniqueness from non-nullness; duplicate byte record from duplicate business event; correction from a second event; dimension attribute from fact; measure from label; stock from flow; additive from semi-additive/non-additive; count rows from count distinct entities; `count(*)` from `count(column)`; grouping from windowing; join match from valid dimensional relationship; many-to-one from many-to-many; current dimension match from as-of match; bridge membership from allocated measure; null member from missing dimension row; and physical nested row from logical child observation.

Write the candidate grain in plain language before profiling keys. Then test whether the source can support it. A source order can contain repeated line numbers after amendments; `(order_id,line_number)` may identify the latest state but not every change event. Evidence may require version, effective time or source log position.

## Learning Objectives

After completing this module, you should be able to:

1. write precise grain declarations for events, entities, relationships and snapshots;
2. derive candidate grain keys and verify uniqueness, null and stability behavior;
3. express functional dependencies implied by a row contract;
4. distinguish transaction, periodic snapshot and accumulating snapshot grains;
5. classify measures by valid aggregation dimensions and time behavior;
6. predict join cardinality and prove when fanout overcounts a measure;
7. transform grain safely with grouping, window functions, bridges and allocation;
8. design deterministic duplicate/correction rules and idempotent loads;
9. test temporal, nested and cross-fact grain boundaries; and
10. document, version and reconcile grain changes for downstream consumers.

## Core Exposition

### Start with a business process

A dimensional model represents measurements from a business process: ordering, fulfillment, inventory, claims, web sessions or device observation. Select one process boundary before selecting tables.

The source schema is evidence, not the model. One source table may mix header and detail; one process may span several services. Interviews, events, keys and reconciliation controls reveal what actually happens.

Name inclusion and exclusion. “Fulfilled line” differs from “ordered line”; canceled and returned items may be separate events, state changes or measures.

### Declare grain in a sentence

Use “one row per …” followed by identity and time. Avoid column lists. Good declarations are testable:

- one row per order line as originally accepted;
- one row per product-store at local business-day close;
- one row per claim lifecycle, updated at defined milestones;
- one row per student-course enrollment relationship and effective interval.

If the sentence contains “or,” it often hides mixed grain. Split models unless the alternatives truly share one proposition and key.

### Separate entity, event and state grain

An entity row says which thing exists and describes it. An event row says something happened. A state row says what was true at an observation/effective point. Their update and history semantics differ.

One customer can have many orders, addresses and status changes. A table with one row per customer cannot include unaggregated order or address repetitions without changing grain.

An event is normally append-oriented; state may be overwritten or versioned. State derived from events needs a declared cutoff and precedence.

### Prefer atomic fact grain

Atomic grain is the lowest captured level of the business process, not necessarily the smallest physical message. It preserves dimensional detail and supports unanticipated aggregation.

Atomic does not mean unmodeled. An order line may still combine quantity and extended price because both are observations of the same line event. A click event and session summary should not share one row.

Publish pre-aggregates for performance only with explicit source grain, target grain, formulas and reconciliation.

### Understand transaction grain

A transaction-grain row records one measurement event: sale line, payment, shipment scan or reading. Its key should survive retries and distinguish corrections according to domain rules.

Some sources publish current transaction state rather than immutable events. Decide whether changes overwrite, create versions or emit adjustment facts. Do not call an updated state row an immutable event.

Transaction time and effective/event time remain explicit, especially for late postings and backdated corrections.

### Understand periodic snapshots

A periodic snapshot records measures for a defined period or as-of boundary, such as product-store-day inventory. Its grain includes all dimensional keys plus the snapshot period/as-of identity.

The [Kimball dimensional modeling techniques](https://www.kimballgroup.com/wp-content/uploads/2013/08/2013.09-Kimball-Dimensional-Modeling-Techniques11.pdf) distinguish transaction, periodic snapshot and accumulating snapshot fact tables. In a periodic snapshot, the period—not an individual transaction—is part of the grain.

Declare dense versus sparse behavior. Does every account receive a row every day, or only accounts with activity? Row count then has different meaning.

### Understand accumulating snapshots

An accumulating snapshot has one row per process instance, such as an order-to-delivery pipeline, with milestone dates updated as work progresses. Its grain is the lifecycle instance, not each milestone event.

It supports elapsed-time and pipeline-state analysis. It does not replace the event stream when audit requires every transition or repeated/reopened milestones.

Define update keys, late/out-of-order milestone precedence and terminal/reopen behavior. Historical snapshots may be needed if analysts require as-known-at reporting.

### Choose a grain key

Derive the key from the proposition. It may be a source event ID, composite business key or generated key linked to a stable deduplication identity.

A surrogate key can make storage joins convenient, but it does not prove business uniqueness. Retain and constrain the natural/deduplication key when possible.

Measure candidate key uniqueness across the full history and adversarial cases. Require non-null components or define how missing identity is quarantined.

### Express functional dependencies

At grain $G$, every single-valued row attribute should be determined by $G$. Write $G\rightarrow A$ for each attribute or measure $A$ under the row's time semantics.

If `order_id → customer_id` but not `order_id → product_id`, an order-grain table can store customer once but cannot store one unaggregated product. At line grain, `(order_id,line_id)` may determine product and quantity.

Profiling an accidental dependency in current data is not proof of a durable rule. Obtain domain ownership and enforce what the contract requires.

### Enforce uniqueness and non-nullness

Use a primary/unique constraint where the system supports it. Composite uniqueness matches composite grain. Understand null behavior; some unique constraints allow multiple null-containing combinations.

For append-only/object data, run duplicate-key tests at production scale and record violating examples. Bloom filters or approximate counts may screen, but exact completion requires an exact authoritative check for governed keys.

Test stability across retries, corrections, backfills and source migrations—not merely uniqueness in one batch.

### Model dimensions at compatible grain

Dimension references describe the fact at its event/effective time. Each foreign key should resolve to exactly one intended dimension row, including explicit unknown/not-applicable members as designed.

A dimension business key can have multiple historical versions. Join with effective interval or resolve the surrogate version during load. Overlapping intervals break uniqueness and cause fanout.

Role-playing dates such as order, ship and delivery date are different relationships even when they reuse one date dimension.

### Keep measures at the row grain

Each stored measure must describe the row proposition. Order total belongs at order grain; line extended amount belongs at line grain. Repeating the order total on lines is denormalized presentation and unsafe for ordinary summation.

Label units, currency and sign conventions. A quantity and price can share a line row, but lifetime customer value cannot unless it is explicitly a snapshot/repeated attribute with restricted aggregation.

Computed measures retain formula/version and null behavior.

### Classify additivity

An additive flow such as line revenue can sum across product, customer and time when units/currency align. A balance is often additive across accounts but not across snapshot dates. A ratio or unit price is generally non-additive.

For averages, retain additive components such as sum and count rather than averaging subgroup averages. A rate needs aligned numerator/denominator grains.

Record allowed aggregation dimensions in the semantic contract. A numeric column is not automatically a measure, and `SUM` availability is not evidence of meaning.

### Treat row counts as measures

`count(*)` counts rows at the relation's current grain. It counts lines in a line table, snapshots in a snapshot table and bridge memberships in a bridge table.

PostgreSQL's [aggregate documentation](https://www.postgresql.org/docs/current/functions-aggregate.html) distinguishes row count from count of non-null expressions. State whether a metric is event count, distinct entity count, non-null observation count or weighted membership.

Do not rename line count “orders” merely because every line carries an order ID.

### Predict join cardinality before joining

For each join, write expected matches per left row and right row: one-to-one, many-to-one, one-to-many, many-to-many or optional. State unmatched policy.

Validate right-side uniqueness before a supposed many-to-one lookup. After joining, compare row count, distinct grain keys, null matches and control totals.

Filters on the right side can turn a left join effectively into an inner join when applied after the join. Test omissions as carefully as fanout.

### Prevent header-detail fanout

Joining order headers to lines is correctly one-to-many if the output grain becomes line. Header attributes may repeat; header additive measures cannot then be blindly summed.

Pre-aggregate line measures to order grain before joining to order measures, or report separate fact tables through conformed dimensions. If allocating header measures to lines, use a documented basis and prove weights sum to one per header.

Never rely on `DISTINCT` to remove replicated measures; line rows differ, so legitimate detail remains and the metric is still repeated.

### Handle many-to-many relationships

A campaign may have multiple owners; a patient may have multiple diagnoses; a sale may receive multiple promotions. A direct join can multiply facts by membership count.

Use a bridge at one row per fact/entity–member relationship. For additive rollups, assign allocation weights $w_i$ with $\sum_i w_i=1$ within the parent grain or clearly label unallocated coverage counts.

Membership count and allocated measure answer different questions. Preserve both without presenting each as total revenue.

### Align facts before comparing them

Two fact tables can share dimensions but differ in grain: daily store-product sales versus monthly regional targets. Joining raw facts creates a Cartesian multiplication inside common keys.

Choose a comparison grain, aggregate each fact independently to it, then join. If one side is coarser, decide whether to keep the comparison coarse or allocate it using governed weights.

Reconcile each pre-aggregation to its source before combining.

### Treat GROUP BY as a grain transformation

SQL `GROUP BY` condenses input rows sharing grouping expressions into one output row per group, as documented by PostgreSQL [SELECT](https://www.postgresql.org/docs/current/sql-select.html). The grouping set is the output grain.

Every nonaggregated selected attribute must be part of the group or functionally dependent on it under the engine's rules. Arbitrary “any value” selectors conceal mixed grain.

Document filters before aggregation and `HAVING` filters after aggregation; they change which propositions reach the result.

### Treat window functions as grain-preserving

A window calculation accesses related rows while retaining each input row's separate identity, as PostgreSQL's [window tutorial](https://www.postgresql.org/docs/current/tutorial-window.html) explains. It adds context at the existing grain rather than condensing rows.

`sum(amount) over (partition by customer)` repeated on every order row is a customer-level derived value carried at order grain. Summing it again repeats the customer total.

Ranking and deduplication need a deterministic total order. Equal timestamps without a stable tie-breaker yield unstable survivors.

### Deduplicate by business identity

Define what duplicates mean. Byte-identical events may be legitimate repeated readings; different payloads with one event ID may be corrections or conflicts.

Specify partition key, precedence fields, ordering direction, tie-breaker, retained loser evidence and late-arrival behavior. Reject irreconcilable conflicts rather than choosing arbitrarily.

`SELECT DISTINCT` compares selected values and changes with the projection. It is not a durable identity rule.

### Model corrections and reversals

A correction can replace prior state, create a new version, or post an adjustment/reversal event. Choose based on audit and analytical needs.

If events are immutable, reversal and corrected entries each have their own event grain and link to the original. Net measures sum under sign rules.

If a snapshot is restated, retain load/as-known time when reproducibility requires the original publication.

### Include time in the grain when required

State and relationship rows often need effective intervals. `customer_id` alone is not unique when history is retained; `(customer_id,valid_from)` or a surrogate version key may identify rows, with non-overlap constraints.

Periodic fact grain includes snapshot period. Event grain includes event identity, not necessarily timestamp alone; multiple events can share a timestamp.

Choose event, effective, processing and snapshot time roles explicitly.

### Unpack nested and repeated data

A document may be one physical row with an array of line items. Logically it contains one order proposition and many line propositions. Exploding the array changes grain.

Carry parent keys and element identity/ordinal. An ordinal is stable only if source ordering is contractual. Generate identity carefully when arrays can reorder.

After explode, verify child count and parent preservation; after regrouping, define order and duplicate semantics.

### Avoid mixed-grain wide tables

A customer-wide table containing latest profile, every transaction field, monthly totals and lifetime value repeats some measures and omits others. Different columns have incompatible keys and time meaning.

Separate fact/state products and expose a semantic layer that joins or aggregates them safely for use cases. Denormalized serving tables may repeat values, but their metric contract must prevent invalid summation.

Convenience is not a substitute for one coherent row proposition.

### Test grain continuously

Test non-null and uniqueness of grain keys; referential match cardinality; row counts; functional dependencies; no temporal overlap; accepted/rejected duplicates; allocation weight sums; and measure reconciliations.

Profile distributions of matches per key, not only averages. One rare fanout can corrupt a high-value measure.

Run tests on backfills and late partitions. Compare to source control totals at source and target grains.

### Version grain changes as breaking changes

Changing from order to order-line grain changes row count, keys, measure additivity and consumer queries even if table/columns remain. Publish a new product or explicit contract version.

Provide mapping, dual-run reconciliation, consumer inventory, migration examples and deprecation window. Do not silently “add detail” to an existing table.

Record old/new grain in catalog metadata and semantic measures.

## Definitions and Notation

Let relation $R$ have row set $r\in R$ and grain key function $G:R\rightarrow K$. Grain uniqueness requires

$$
G(r_1)=G(r_2)\Rightarrow r_1=r_2.
$$

In practice equality here means the same governed row assertion, not necessarily byte-identical storage. Candidate attributes satisfy functional dependencies $G\rightarrow A_i$ under the same effective-time semantics.

For left row $l$ joined to right relation $D$, define match degree

$$
d(l)=|\{d\in D\mid join(l,d)\}|.
$$

An unweighted post-join sum of left measure $m$ is $\sum_{l\in L}d(l)m(l)$. It equals the original $\sum_lm(l)$ only under relevant conditions such as $d(l)=1$, zero measures for exceptional degrees, or governed weights whose per-left total is one.

For target grouping key $H$, summarization creates one output row per distinct $H(r)$ and aggregate state over its preimage. The output grain is $H$, not the input key $G$.

For bridge memberships $B_l$ with weights $w(l,b)$, full allocation requires

$$
\sum_{b\in B_l}w(l,b)=1
$$

for each allocated parent row $l$, subject to explicit zero/unassigned policy.

## Mechanisms, Invariants, or Proof Structure

Use this mechanism for every analytical relation:

1. Select and name one business process.
2. Write “one row per …” with event/state, identity, time and inclusion semantics.
3. Inventory source keys, retries, corrections, deletes and historical behavior.
4. Choose the lowest useful captured grain and a stable candidate grain key.
5. Profile and enforce key uniqueness, non-nullness and cross-batch stability.
6. List functional dependencies implied by the row proposition.
7. Attach only dimensions and facts valid at that same grain and time.
8. Classify each measure's unit, null rule and additive dimensions.
9. Declare transaction, periodic snapshot or accumulating snapshot behavior.
10. Specify every join's cardinality, temporal predicate and unmatched policy.
11. Pre-aggregate incompatible facts or use governed bridges/allocation.
12. Treat grouping as new grain and windows as retained grain with repeated context.
13. Define duplicate/correction precedence and preserve conflict evidence.
14. Reconcile row counts, distinct keys, match degrees and additive control totals.
15. Run late, historical, nested, many-to-many and adversarial boundary fixtures.
16. Version any grain change and migrate consumers with dual-run evidence.

The executable model makes header-detail fanout visible. It uses exact integer currency units for a deterministic teaching fixture, not evidence about a database optimizer or production workload.

<!-- bijux-verify: {"id":"row-grain-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"order_count=2\nline_count=3\njoined_rows=3\nwrong_order_total=250\ncorrect_order_total=150\nline_revenue=150\ngrain_key_unique=True\n","stderr":""}} -->
```python
orders = (
    {"order_id": "o1", "order_total": 100},
    {"order_id": "o2", "order_total": 50},
)
lines = (
    {"order_id": "o1", "line_id": 1, "line_revenue": 60},
    {"order_id": "o1", "line_id": 2, "line_revenue": 40},
    {"order_id": "o2", "line_id": 1, "line_revenue": 50},
)

joined = tuple(
    (order, line)
    for order in orders
    for line in lines
    if order["order_id"] == line["order_id"]
)
order_keys = tuple(order["order_id"] for order in orders)
line_keys = tuple((line["order_id"], line["line_id"]) for line in lines)
grain_key_unique = len(set(order_keys)) == len(order_keys) and len(set(line_keys)) == len(line_keys)

print("order_count=" + str(len(orders)))
print("line_count=" + str(len(lines)))
print("joined_rows=" + str(len(joined)))
print("wrong_order_total=" + str(sum(pair[0]["order_total"] for pair in joined)))
print("correct_order_total=" + str(sum(order["order_total"] for order in orders)))
print("line_revenue=" + str(sum(line["line_revenue"] for line in lines)))
print("grain_key_unique=" + str(grain_key_unique))
```

Critical invariants are:

- **Proposition:** every row asserts exactly one declared business fact/state/relationship.
- **Identity:** the grain key is unique, non-null as required and stable under retry.
- **Dependency:** single-valued attributes and facts are determined by the grain.
- **Time:** event/snapshot/effective semantics align across the row and joins.
- **Measure:** unit, null and additivity rules accompany every metric.
- **Join:** expected match degree and unmatched behavior are tested before aggregation.
- **Transformation:** grouping declares a new grain; window values remain attached to old rows.
- **History:** duplicates, corrections and dimensional versions resolve deterministically.
- **Reconciliation:** row/mass/control totals prove preservation at each boundary.

**Proof sketch — unweighted fanout overcounts a positive additive measure.** Let left relation $L$ contain measure $m(l)\geq0$, and suppose a join repeats each left row once per right match. The post-join sum is $S'=\sum_l d(l)m(l)$, while the original is $S=\sum_lm(l)$. Then $S'-S=\sum_l(d(l)-1)m(l)$. If every retained row has $d(l)\geq1$ and at least one row has $d(l)>1$ with $m(l)>0$, the difference is positive, hence $S'>S$. A many-to-one uniqueness guarantee makes $d(l)\leq1$ but unmatched rows still require policy. Allocation replaces each replication with weights whose sum is one.

## Alternatives and Trade-Offs

**Atomic versus aggregate fact.** Atomic grain maximizes flexibility and traceability but costs storage and query work. Aggregate facts accelerate common workloads but answer fewer questions. Keep explicit lineage and reconcile aggregates to atomic sources.

**Natural versus surrogate grain key.** Natural keys expose business identity and aid idempotency but can be wide, mutable or absent. Surrogates are compact and stable inside the warehouse but can hide duplicate business propositions. Often use surrogate storage identity plus a constrained business/dedup key.

**Transaction versus periodic snapshot.** Transactions preserve flow and event detail. Periodic snapshots simplify state/as-of analysis and dense reporting. A balance can often be derived from events only with complete history and rules; storing snapshots can improve operability at duplication cost.

**Accumulating snapshot versus milestone events.** One lifecycle row makes pipeline duration convenient. Separate milestone events preserve repeats and history. Store both when operational dashboards and forensic history differ.

**Sparse versus dense snapshot.** Sparse rows reduce volume but make absence ambiguous. Dense snapshots make row count and zero activity explicit but grow quickly. Define whether absence means zero, missing or not applicable.

**Pre-aggregate versus allocate.** Keeping comparisons at a common coarse grain avoids invented detail. Allocation enables finer reporting but embeds assumptions. Preserve unallocated totals and label allocated outputs.

**Bridge versus array/repeated dimension.** A bridge makes membership grain and weights queryable. Arrays are compact and convenient but explode into fanout during analysis. Either representation needs explicit child identity and aggregation semantics.

**Physical constraint versus data test.** Constraints fail invalid writes immediately but may be unavailable on append/object systems and can cost ingestion throughput. Batch tests are flexible but allow bad data to land. Use both appropriate to trust zones.

**Overwrite versus evented correction.** Overwrite presents current truth simply but loses as-known history. Reversal/adjustment facts preserve audit but complicate netting. Effective/versioned state offers another path. Match regulatory and analytical requirements.

**Window versus grouped aggregate.** Windows retain detail with contextual values, useful for ranks and comparisons. Grouping reduces to the target grain. Repeated window aggregates are dangerous if later summed as if atomic.

**One wide table versus multiple fact tables.** Wide serving tables can simplify one dashboard but mix grains and repeat measures. Multiple facts preserve meaning and reuse conformed dimensions, at the cost of semantic-layer/query design.

**Strict one-grain contract versus typed union.** A union with a row-kind discriminator can represent heterogeneous events, but every kind has distinct required fields and measures. For analytical facts, separate tables are usually clearer; unioned event logs need kind-specific contracts.

## Failure Modes and Misconceptions

- **“Grain is the list of columns.”** Columns implement a prior row proposition; adding/removing one need not define grain.
- **“The primary key is the grain.”** It enforces chosen storage identity but may be a meaningless generated ID.
- **“Unique in this sample means a business key.”** Future corrections, retries or source mergers can break accidental uniqueness.
- **“One row per customer can contain all addresses.”** Repetition changes the logical child grain or requires a collection contract.
- **“Atomic means one source message.”** A message can contain multiple events/lines, and one event can span messages.
- **“More detail can be added without breaking consumers.”** Grain changes keys, counts and aggregation behavior.
- **“All numeric facts are additive.”** Balances, ratios, prices and distinct counts have constrained rules.
- **“Average of averages is an average.”** It requires weighting by contributing counts, not equal subgroup weights.
- **“Row count means customer/order count.”** It counts current row propositions.
- **“`count(column)` counts events.”** It excludes null expressions and answers another question.
- **“A left join cannot lose rows.”** Later filters on right-side values can remove unmatched rows.
- **“A foreign key prevents fanout.”** It ensures referenced existence, while right-side uniqueness/cardinality determines matches.
- **“`DISTINCT` fixes a join.”** It can hide symptoms, drop legitimate duplicates and changes with projection.
- **“The dimension has one row per customer.”** Historical versions make business key non-unique without as-of resolution.
- **“Joining on month aligns facts.”** Other dimensions and source grains can still cause multiplication.
- **“A bridge makes measures safe.”** Allocation or explicit coverage semantics are still required.
- **“Daily balance sums to monthly balance.”** Stock measures are generally not additive across snapshot time.
- **“Missing snapshot row means zero.”** It may mean failed capture, inactivity or sparse design.
- **“Window sum is a new summary row.”** It is repeated on each retained input row.
- **“Latest row is deterministic.”** Equal precedence timestamps need a stable tie-breaker and conflict policy.
- **“Timestamp identifies an event.”** Multiple events can share precision and clocks can be corrected.
- **“Ordinal identifies nested children forever.”** Reordering changes ordinals unless sequence is contractual.
- **“Control totals alone prove grain.”** Equal totals can hide offsetting duplication and omission.
- **“Performance justifies mixed grain.”** Serving optimization needs an explicit, constrained metric contract.
- **“Null dimension keys can be dropped.”** Facts then disappear; unknown/not-applicable semantics should be explicit.

## Worked Examples

### Example 1

An order source has one header row per order and many line rows. The proposed fact table repeats `order_total` on each line because analysts want one table. Order `o1` has two lines, so the total appears twice.

The model stores line revenue at `(order_id,line_id)` grain and order total at `order_id` grain. Reports aggregate each fact to a shared comparison grain before joining. If a serving view repeats order total, its metadata forbids summing that column and exposes a safe explicit order measure.

### Example 2

A customer export has `customer_id`, email and address. Some customers have three addresses, so `customer_id` is not unique. Calling it customer grain causes customer counts and joins to fan out.

The model separates one customer entity row from an address relation at `(customer_id,address_id,valid_from)` grain. A primary-address rule produces a deterministic as-of relationship when needed. Tests enforce customer uniqueness and nonoverlapping address intervals.

### Example 3

A store-product-day inventory snapshot contains ending quantity. Summing seven days returns quantity-days, not the end-of-week stock. It is additive across stores/products at one timestamp but semi-additive across time.

The semantic measure selects the final valid snapshot for period-end balance and separately offers average daily inventory using a defined denominator. Missing snapshot days remain `missing`, not zero. Dense/sparse capture behavior is documented.

### Example 4

A monthly regional target is joined to daily store sales on `(region,month)`. The target repeats for every store-day row, and summing it produces a huge number.

The report first aggregates sales to region-month, then joins the one target row. A store-level target requires an approved allocation whose weights sum to one within region-month. Allocated and authoritative target measures have distinct names.

### Example 5

A fact references customer business key `C7`. The dimension has two Type 2 versions for `C7`, and the join omits event-time validity. Every fact for that customer matches twice.

The load resolves exactly one dimension surrogate using `effective_from <= event_time < effective_to`. Tests reject overlapping intervals and zero/multiple matches except governed unknown handling. Historical facts keep the resolved version key.

### Example 6

A pipeline deduplicates with `row_number() over (partition by event_id order by ingested_at desc)`. Two conflicting records share identical `ingested_at`; different execution plans choose different survivors.

The contract adds source sequence and immutable payload digest as precedence/tie-break evidence, or quarantines irreconcilable ties. Losers and reason codes remain auditable. The grain key is event ID only after the policy resolves conflicts.

### Example 7

A patient encounter has multiple diagnoses. Joining encounter cost through the diagnosis bridge repeats cost for every diagnosis. Counting diagnoses is valid; summing encounter cost is not.

The model offers unallocated encounter count/cost at encounter grain and an allocated diagnosis cost with weights summing to one per encounter. Analysts can also report “encounters associated with diagnosis,” clearly labeled as coverage rather than mutually exclusive totals.

### Example 8

A grouped query produces one row per product-month but selects store name through an arbitrary-value function. Multiple stores contribute, so the label has no functional dependency on the grouping key.

The query either adds store to the grouping grain, removes store, or derives a legitimate aggregate such as contributing-store count. The output contract lists `(product_id,month)` as key and tests its uniqueness.

### Example 9

An accumulating claim snapshot has one row per claim with submitted, reviewed and paid milestones. Some claims reopen and can be reviewed twice. Overwriting the one review timestamp loses process history.

The accumulating table retains defined first/latest milestones for operational duration, while a separate claim-event fact records every transition. The two products reconcile by claim and clearly state their different grains.

### Example 10

An order JSON document is one physical record containing a `lines` array. Exploding produces one row per array element. The source lacks stable line IDs and may reorder lines after correction.

The boundary obtains a source line identity or derives a documented content-based identity with collision/conflict handling; it does not assume ordinal is eternal. It verifies child count, header linkage and order total reconciliation after explode.

## Cross-Program Connections

**Database Engineering.** Primary/unique/foreign/exclusion constraints, functional dependencies and query cardinality make portions of the grain contract executable. Database statistics do not replace semantic declarations.

**Software Design and Domain Modeling.** Entities, value objects, domain events and aggregates help distinguish identity, state and occurrence before data reaches analytics. Analytical grain should reflect these meanings without copying transactional schemas blindly.

**Data Architecture Engineering.** Catalogs and contracts should publish grain, keys, time roles, additivity, lineage and owners so facts can be composed safely across products.

**Large-Scale Data Systems Engineering.** Distributed joins, shuffles, skew and approximate aggregation amplify the cost of unclear cardinality. Grain-aware partitioning and pre-aggregation improve both correctness and scale.

**API and Service Engineering.** Pagination, retries, event IDs and nested payloads influence duplicate identity and logical child grain. API “resource” does not necessarily equal analytical row.

**Machine Learning Engineering.** Training examples have a grain, often entity-time. Joining future or multirow features without point-in-time alignment creates leakage and duplication.

**Security Engineering.** Row-level access policies operate at a grain. Exploding or aggregating data can change which principal or group a row represents and must preserve authorization intent.

**Systems Engineering.** Grain is an interface invariant. Hazards arise when subsystems each use locally plausible but incompatible definitions of an event, unit, period or identity.

## References

1. Kimball Group, [Four-Step Dimensional Design Process](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/four-4-step-design-process/), retrieved 2026-09-02.
2. Kimball Group, [Dimensional Modeling Techniques](https://www.kimballgroup.com/wp-content/uploads/2013/08/2013.09-Kimball-Dimensional-Modeling-Techniques11.pdf), retrieved 2026-09-02.
3. Microsoft, [Understand Star Schema and Its Importance](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema), retrieved 2026-09-02.
4. Microsoft, [Dimensional Modeling in Microsoft Fabric Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/dimensional-modeling-overview), retrieved 2026-09-02.
5. PostgreSQL Global Development Group, [Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html), retrieved 2026-09-02.
6. PostgreSQL Global Development Group, [SELECT and GROUP BY](https://www.postgresql.org/docs/current/sql-select.html), retrieved 2026-09-02.
7. PostgreSQL Global Development Group, [Window Functions Tutorial](https://www.postgresql.org/docs/current/tutorial-window.html), retrieved 2026-09-02.
8. PostgreSQL Global Development Group, [Aggregate Functions](https://www.postgresql.org/docs/current/functions-aggregate.html), retrieved 2026-09-02.

## Exercises

### Exercise 1

An ecommerce source provides orders, lines, payments, shipments and returns. Write grain declarations and candidate keys for each fact product. Place order total, line revenue, payment amount, shipped quantity and returned quantity. Define joins, corrections and reconciliations without mixing grains.

### Exercise 2

A table claims one row per account-day but may contain multiple intraday observations, missing inactive days and both opening/closing balances. Diagnose the actual grain and redesign transaction/snapshot products. State dense/sparse behavior and valid daily/monthly aggregations.

### Exercise 3

Sales are at store-product-day grain; targets at region-product-month; stores map to multiple sales territories over effective intervals. Design a comparison and optional allocation. Include bridge grain, temporal matching, weights, output keys and tests preventing fanout.

### Exercise 4

A deduplication query partitions by `event_id` and orders only by ingestion timestamp. Source retries can tie, corrections reuse IDs and deleted events arrive as tombstones. Specify row propositions, precedence, deterministic tie-breaks, conflict handling, retained evidence and idempotent keys.

### Exercise 5

A consumer wants one wide customer table with current profile, all addresses, last order, monthly revenue, lifetime revenue and open-case count. Explain the grains involved and propose durable fact/state products plus a safe serving layer. Include semantic measures and verification.

## Answers to the Exercises

### Answer 1

Use one row per accepted order keyed by `order_id`; one row per order line keyed by `(order_id,line_id)`; one row per payment transaction keyed by payment event ID; one row per shipment line event keyed by shipment event/line; and one row per return line event keyed by return event/line. Keep order total at order grain, line revenue at line grain, payment amount at payment grain, and shipped/returned quantities at their event-line grains.

Aggregate children independently to order or order-line before comparison. Link reversals/corrections to original events or version state explicitly. Reconcile line revenue to governed order controls, payments to settled order amounts under timing rules, and shipped/returned quantities to line quantities. Tests cover key uniqueness, match degree, omissions and retry idempotence.

### Answer 2

If multiple intraday observations exist, the actual row grain includes account plus observation instant/sequence; calling it account-day is false. Preserve an atomic balance-observation fact. Derive a periodic account-day snapshot with one declared close/as-of observation, opening and closing fields whose selection rules are explicit.

Choose dense rows for every active account-day or sparse changed accounts and define absence accordingly. Balances are additive across accounts at one as-of time, not across days. Monthly end balance selects the last valid daily close; average daily balance uses defined daily observations and denominator. Enforce `(account_id,business_date)` on the snapshot and reconcile selected observations.

### Answer 3

First aggregate sales to region-product-month using each store's one valid region mapping as of sale day. If sales territories are many-to-many, use a bridge at `(store_id,territory_id,effective_interval)` grain and reject overlaps/conflicting interval resolution. Direct territory reporting of total sales needs weights summing to one per store/effective instant.

Compare region-product-month sales with the unique target at that key. For store/territory detail, allocate target through approved weights and name it allocated target; preserve authoritative regional target. Tests enforce target uniqueness, one regional match per sale, bridge weight sums, no temporal gaps/overlaps, output-key uniqueness and source/allocated total reconciliation.

### Answer 4

Define immutable attempt rows at `(source,event_id,source_sequence_or_attempt)` and resolved current event state at `(source,event_id)`. Precedence should use source version/sequence before ingestion time. Add immutable payload digest as a deterministic tie-break diagnostic, but quarantine equal-precedence conflicting payloads rather than arbitrarily declaring one truth.

Model corrections as higher versions and tombstones as explicit terminal versions under source rules. Retain all attempts, loser/conflict reasons and original bytes. The resolved product uses stable event key for idempotent upsert; reprocessing the same attempt changes nothing. Tests cover tied times, out-of-order versions, duplicate retries, correction after retry, tombstone, resurrection policy and conflicts.

### Answer 5

The request combines customer current-state grain, address relationship/history grain, order grain, customer-month aggregate grain, customer-lifetime aggregate grain and customer-as-of open-case state. A single row can carry derived values only by selecting/aggregating other grains under explicit cutoff; “all addresses” is a nested child collection, not scalar customer data.

Maintain a current/versioned customer dimension, address relationship product, atomic order/revenue fact and case-state/event fact. Publish customer-month revenue and optionally a customer-current serving view with `last_order` selection rule, lifetime sum cutoff and open-case as-of time. Expose safe semantic measures rather than summable repeated totals. Verify source reconciliations, one row per customer in the view, deterministic latest selection, point-in-time correctness and no fanout when addresses are requested.
