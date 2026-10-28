---
module_id: DE-012
program: Data Engineering
level: 1
module_number: 12
title: Facts, Dimensions, and Measures
status: complete
last_verified: 2026-09-02
---

# Facts, Dimensions, and Measures

## One-Page Review

### Governing question

Given a declared row grain, which observations belong in the fact table, which descriptive attributes belong in dimensions, and which aggregation rule produces a meaningful measure under each filter and grouping?

### Essential definitions

- A **fact** is an observation or measurement produced by a business process at the fact table's declared grain.
- A **dimension** supplies descriptive context—the who, what, where, when, why or how—used to filter, group and label facts.
- A **measure** is a governed calculation over fact rows. A stored fact column is an input; a semantic measure defines the aggregation, filters, units and exceptional cases.
- **Dimensionality** is the set of dimension roles associated with a fact. **Granularity** is the level represented by their key values and the rest of the row contract.
- An **additive fact** can be summed across every dimension applicable to the fact table. A **semi-additive fact** can be summed across some dimensions but not others. A **non-additive fact** cannot be meaningfully summed.
- A **derived measure** is calculated from other facts. Ratios should usually be derived from aggregated numerator and denominator components.
- A **factless fact table** records an event, eligibility or relationship using dimension keys even when no numeric fact is present.
- A **degenerate dimension** is a business identifier, such as an order number, stored in a fact table without a separate dimension row.
- A **role-playing dimension** is one physical dimension used in multiple semantic roles, such as order date and ship date.
- A **conformed dimension** or **conformed fact** has compatible meaning and content across participating business processes.

### Central model, mechanism, or theorem

For fact rows $F$ at grain $G$, define a measure contract

$$
M=(X,A,D,U,N,W,C),
$$

where $X$ identifies stored inputs, $A$ the aggregation or formula, $D$ the dimensions across which it is valid, $U$ units, $N$ null/unknown behavior, $W$ the time window or as-of rule and $C$ additional constraints. A query measure is valid only when its grouping, filters and joins satisfy that contract.

For a ratio with numerator $n_i$ and denominator $d_i$, aggregate components before division:

$$
R(S)=\frac{\sum_{i\in S}n_i}{\sum_{i\in S}d_i},
$$

subject to an explicit zero-denominator policy. In general, $R(S)$ is not the unweighted average of row ratios $n_i/d_i$.

### Critical invariants

- The business process and row grain are declared before dimensions and facts are selected.
- Every stored fact and dimension key is valid at exactly that grain and its time semantics.
- Dimension keys resolve to one intended member or an explicit unknown/not-applicable member.
- Descriptive labels and hierarchies live in governed dimensions rather than being repeated inconsistently in facts.
- Every measure declares formula, source columns, unit, null behavior, valid aggregation dimensions and temporal behavior.
- Additive components are retained when a ratio, percentage, average or rate must be recomputed at new grains.
- Snapshot balances are not summed through time unless the intended unit is explicitly balance-time.
- Counts identify what is counted: rows, distinct entities, eligible opportunities, successes or non-null observations.
- Multiple fact tables are aligned to a common grain before comparison; they are not joined row-to-row merely because they share dimensions.
- Semantic measures are tested against hand-recomputed fixtures, reconciliation controls and adversarial filters.

### Common failures

Treating every number as a fact and every string as a dimension; storing a manager's salary in a sales-line fact; using surrogate keys as measures; repeating descriptive text in huge fact tables; summing unit price, percentages or balances; averaging averages without weights; dividing before aggregation; interpreting `NULL` as zero; counting a nullable column when event rows are intended; joining two fact tables directly; letting role-playing dates share an ambiguous label; making factless rows indistinguishable from missing data; mixing currencies or units; hiding business identifiers that users need for drill-through; encoding rapidly changing measurements as dimension attributes; and publishing implicit measures whose default aggregation is wrong.

### Compact example

Three sale lines have net revenue 180, 80 and 135 and cost 120, 50 and 90. Total profit is 135, and gross margin is $135/395\approx34.18\%$. Averaging the three line margins gives about $34.72\%$, a different and generally incorrect result for portfolio margin. Revenue and cost are additive components; margin is a non-additive derived measure. A daily inventory balance, meanwhile, may be summed across products on a day but requires last-valid, average or another declared rule across days.

### Connections

[DE-011](011-grain-and-the-meaning-of-a-row.md) establishes the grain contract on which this classification depends. The planned DE-013 module will organize facts and dimensions physically, while planned DE-014 will govern historical dimension members; both are indexed in the [Data Engineering roadmap](../ROADMAP.md). Database constraints connect to [Database Engineering](../../18-database-engineering/ROADMAP.md), semantic definitions to [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md), and metric operation to [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md).

## Governing Question

After declaring what one row means, can a model owner explain why every remaining column is a dimension key, a degenerate identifier, a measure input or a narrowly justified operational attribute—and then state exactly how every measure behaves under aggregation?

Dimensional modeling is not a mechanical split of text into dimensions and numbers into facts. A numeric product code is descriptive identity, while a textual event outcome can be analyzed as a count. A unit price is numeric but usually non-additive. A customer tier may be stored as text but must resolve according to history at event time. Classification follows business meaning, grain and intended analysis.

The [Kimball facts guidance](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/facts-for-measurement/) defines facts as measurements produced by a process event and requires them to agree with the declared grain. Its example distinction is structural: sale-line quantity belongs to a sale-line event, while an unrelated organizational measurement does not become a sale-line fact merely because a report requests it.

The complementary [Kimball dimensions guidance](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/dimensions-for-context/) treats dimensions as the descriptive entry points used to filter and group facts. A dimension is therefore not a miscellaneous lookup. Its members and attributes establish reusable business context with owned identity and history.

## Why This Matters

Most dashboards are aggregations over fact rows through dimension filters. If facts, dimensions or measures are misclassified, the database can execute a syntactically valid query that answers no coherent business question. Wrong defaults then spread through extracts, semantic models, spreadsheets and executive decisions.

Fact design determines what can be measured. At atomic sale-line grain, analysts can aggregate by product, store and day. A monthly category summary cannot later recover the distribution across products or days. Conversely, attaching a monthly target to every line invents detail and causes fanout. Separate fact tables let each process preserve its own grain.

Dimension design determines whether people can find and trust the numbers. Stable labels, hierarchies, classifications, date attributes and explicit unknown members make filtering intelligible. Duplicated source descriptions in facts increase storage and allow spelling, ownership and history to diverge.

Measure design determines whether arithmetic is valid. Revenue can often be summed; balance usually cannot be summed across time; a rate should usually be recomputed from its components; a distinct customer count cannot be added across regions when customers overlap. The operator is part of the metric, not a visualization preference.

Operationally, these contracts enable testing. A fact load can assert dimension resolution and additive control totals. A dimension load can assert key uniqueness and history rules. A semantic layer can prevent unsafe implicit sums and expose only governed measures. Without classification, quality checks cannot distinguish a genuine zero, a missing member, an impossible aggregation or a late fact.

## Prerequisites and Retrieval

Retrieve the business process and owner; the grain declaration; source events, transactions and snapshots; natural and surrogate keys; candidate dimensions; dimension member ownership; descriptive attributes and hierarchies; event/effective/processing timestamps; dimension history requirements; source measures and formulas; units, currencies and scales; null and zero meaning; control totals; sign conventions; reversals and corrections; countable events; eligibility/coverage data; numerator and denominator components; snapshot density; balance/as-of rules; distinct-count populations; allocation rules; multiple-unit conversions; exchange-rate policy; role-playing date requirements; factless relationships; degenerate identifiers; drill-through needs; privacy classifications; query filters and grouping patterns; existing semantic measures; implicit aggregation defaults; refresh cadence; late facts/dimensions; reconciliation tolerances; and downstream consumers.

Distinguish a business process from an entity; an event from its descriptive context; a fact row from a source record; a numeric measurement from a numeric identifier; stored fact from query measure; base fact from derived measure; flow from stock; amount from unit price; additive from semi-additive and non-additive; zero from null, unknown and not applicable; event count from non-null value count; count from distinct count; average from weighted average; ratio-of-sums from average-of-ratios; transaction time from event time; dimension natural key from warehouse surrogate; current dimension value from as-of member; date role from date table; factless occurrence from coverage; relationship bridge from additive fact; operational audit attribute from analytical dimension; and conformed name from genuinely conformed semantics.

For each candidate measure, collect at least one small fixture with source rows and an authoritative expected total. Include edge cases: zeros, nulls, negative adjustments, duplicate events, mixed currencies, missing members, overlapping dimension history, empty groups and aggregation across time. The expected result must be independently recomputable rather than copied from the implementation under test.

## Learning Objectives

After completing this module, you should be able to:

1. classify fact, dimension, degenerate identifier and operational metadata columns by business meaning;
2. design measurement-event, snapshot and factless fact tables at consistent grain;
3. derive dimension roles and ensure one intended member resolves per fact;
4. distinguish stored fact inputs from governed semantic measures;
5. classify additive, semi-additive and non-additive behavior by dimension;
6. recompute ratios, rates and averages from additive components;
7. specify count, null, sign, currency, unit and time-window semantics;
8. align multiple facts without fact-to-fact fanout;
9. test measure contracts using invariants, reconciliation and boundary fixtures; and
10. evolve fact and dimension models without silently changing metric meaning.

## Core Exposition

### Begin with process and grain

Select the business process and declare one row before choosing columns. Ordering, payment, fulfillment and return are related but distinct processes. Their events, clocks, dimensions and measures may differ.

A fact table should represent observations from one coherent process at one consistent grain. A report's desired layout is not a process. If the report mixes order, shipment and monthly target measures, model those facts separately and combine already-aggregated results.

The grain determines which candidate facts and dimensions are admissible. Any column whose value is not single-valued and meaningful for the row proposition requires a different grain, an aggregation or another table.

### Recognize fact rows

A fact row records that something measurable or countable happened, existed or was eligible at a defined grain. It usually contains dimension foreign keys and numeric measurement columns, plus carefully chosen identifiers and timestamps.

Fact tables tend to grow with process activity. Size is a consequence, not a definition. A tiny target table can be a fact; a huge customer-profile table can be a dimension.

Some processes yield multiple facts at the same grain: quantity, gross amount, discount, tax and cost for one sale line. Store them together when their provenance, time semantics and dimensional context agree.

### Recognize dimensions

Dimensions describe the entities and classifications by which facts are filtered, grouped and labeled. Product, customer, location, promotion, channel and calendar are common examples.

A dimension has a unique warehouse member key, a durable business identity when available, descriptive attributes and explicit history semantics. Its attributes should be functionally dependent on the dimension member version.

Good dimensions use business vocabulary, readable labels and governed hierarchies. They should not become dumping grounds for unrelated flags or rapidly changing measurements.

### Do not classify by physical type

Data type does not determine role. `product_code=1042` is an identifier/dimension key even though it is numeric. `approval_status='approved'` can be counted through event rows even though it is text.

A numeric age, temperature or quantity may be a fact when measured at the process grain. An age band used for filtering can be a derived dimension attribute. Preserve the measurement when future bands may change.

Ask whether users aggregate the value, filter/group by it, drill through with it, or use it only for operations. Then check whether that use is valid at the grain.

### Distinguish stored facts from semantic measures

A stored column such as `net_amount` is a fact input. A semantic measure such as “recognized net revenue” defines aggregation, qualifying statuses, event-time window, currency policy and null behavior.

The same stored fact can feed several measures. Gross bookings and recognized revenue may select different event states. Conversely, one measure may combine several stored facts, such as profit equals net revenue minus cost.

Hide or discourage unsafe implicit aggregations. Expose named measures whose definitions are versioned, reviewed and testable.

### Model additive facts

An additive fact can be summed across every dimension associated with its fact table without changing its meaning. Transaction quantities and amounts are often additive when units and signs are compatible.

Additivity still has premises. Dollars and euros cannot be summed without a conversion policy; kilograms and units are not interchangeable; duplicate/reversal rows require correct signs; confidential and unrestricted populations may have distinct access scopes.

Record unit and currency either as invariant metadata or a dimension at the row grain. Aggregate only within compatible units or convert through governed rates at a declared date role.

### Model semi-additive facts

Semi-additive facts permit summation across some dimensions but not all. Account balance can usually be summed across accounts at one as-of time but not across successive days.

The [Kimball additivity classification](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/additive-semi-additive-non-additive-fact/) uses balances as the canonical time exception. Define the permitted operator across the forbidden dimension: last valid, first, minimum, maximum, average exposure, duration-weighted average or change.

Missing snapshots complicate last-value rules. Specify whether to carry forward, require an exact observation, tolerate a freshness interval or mark the result incomplete.

### Model non-additive facts

Ratios, percentages, unit prices and many indexes are non-additive. Summing them usually has no interpretable unit. An unweighted average is valid only when the metric definition explicitly gives every observation equal weight.

Store additive numerator and denominator components when possible. Compute conversion rate as total conversions divided by total eligible opportunities, not as the average of daily rates unless daily equality is the intended weighting.

Some facts support other operators. Unit price might use quantity-weighted average; temperature might use min/max/mean under a sampling contract; a categorical score might use an ordered percentile. “Non-additive” does not mean “unusable”—it means `SUM` is not the default algebra.

### Treat averages as ratios

An average $\bar{x}$ represents $\sum x_i/n$ over a defined population. To roll up subgroup averages, retain subgroup sums and counts:

$$
\bar{x}=\frac{\sum_j n_j\bar{x}_j}{\sum_j n_j}.
$$

If the observations have domain weights $w_i$, define $\sum_i w_ix_i/\sum_iw_i$ and document the weight. Do not infer weights from convenient row counts when the business exposure differs.

Null observations are normally excluded by SQL `avg`, while zeros are included. That behavior may or may not match the business population, so numerator and denominator should be explicit.

### Define counts precisely

Row count is a valid measure when each row is exactly the event being counted. `count(*)` counts selected rows; `count(column)` counts selected non-null values. Distinct count counts unique non-null expressions under engine semantics.

Name the population: orders placed, sale lines, customers purchasing, eligible members, successful payments or active account-days. These are not interchangeable.

Distinct counts are non-additive across overlapping groups. Region-level distinct customers cannot be summed into a national count when customers appear in several regions. Recompute over the union or use a purpose-built sketch with declared error semantics.

### Use factless fact tables

A factless fact row records an occurrence or relationship using dimension keys without a numeric measurement. Attendance, promotion eligibility and salesperson-region assignment are legitimate facts because row existence carries meaning.

The [Kimball factless-fact guidance](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/factless-fact-table/) distinguishes activity from coverage. To ask what did not happen, build the set of eligible opportunities and subtract observed events. Absence from an activity table alone is ambiguous.

Factless tables still need a grain key, time semantics and duplicate policy. A row count is only meaningful after those are defined.

### Handle degenerate dimensions

A transaction identifier such as invoice number can remain in a fact table as a degenerate dimension when it supports grouping or drill-through but has no independent descriptive attributes.

Do not move an identifier into a separate one-column dimension merely to satisfy a diagram. Conversely, if the identifier acquires reusable attributes or history, model the appropriate entity/process dimension.

Degenerate identifiers are not measures. Summing order numbers is meaningless; counting distinct order numbers may be a valid semantic measure.

### Use role-playing dimensions

One date dimension may play order-date, ship-date and delivery-date roles. Each foreign key and semantic relationship must be named by role so filters do not silently target the wrong clock.

The physical dimension members can be shared, but query paths and labels remain distinct. “Sales by month” is ambiguous until the date role is chosen.

Role-playing also applies to locations, employees and organizations—for example origin versus destination or buyer versus approver.

### Resolve dimensions at fact time

Every fact key should resolve to exactly one intended dimension member. For versioned dimensions, use the fact's declared event/effective time to select the correct version, then store the surrogate key.

Unknown, not applicable, redacted and error states have different meanings. Represent them with governed members rather than a null foreign key that causes facts to disappear from inner joins.

Late-arriving dimensions need a durable policy: inferred placeholder, quarantine or delayed fact load. Later repair must preserve audit and avoid changing already-reported history without notice.

### Keep dimensions descriptive

Attributes such as product name, category and brand belong in a product dimension because they describe product members and drive filters. Repeating them on every sale line increases volume and permits inconsistent labels.

Not every descriptor deserves a large standalone dimension. Low-cardinality flags from one process can form a small junk dimension; free-form comments may live in drill-through storage rather than an analytical dimension.

High-change attributes require care. A sensor reading is a fact, not a new dimension member every second. A governed band can be derived for analysis while retaining the original measurement.

### Keep facts at one measurement grain

The current [Microsoft Fabric fact-table guidance](https://learn.microsoft.com/en-us/fabric/data-warehouse/dimensional-modeling-fact-tables) describes fact tables as measurements plus dimension keys whose values determine granularity. It also notes that higher-grain storage sacrifices lower-level analysis.

Do not attach store-month rent to every sale line. Keep rent at store-month fact grain and sales at line grain. Compare them only after sales are aggregated to store-month or rent is explicitly allocated under a separate measure.

Header and line facts can coexist in separate tables. A semantic model may provide safe measures across both without physically repeating header amounts.

### Align multiple facts through dimensions

Multiple fact tables often share conformed date, product, location or customer dimensions. Compare facts by aggregating each independently to compatible conformed dimension members, then joining the results.

Direct fact-to-fact joins multiply rows whenever either side has more than one row for a join key. Even when totals happen to match, the query structure lacks a preservation guarantee.

Conformance requires equivalent meaning, not identical column names. Fiscal month, product category and customer segment must use compatible membership, history and null policies across processes.

### Govern formulas and signs

Write formulas from named inputs with units. For sale-line currency amounts:

$$
\text{net}=\text{gross}-\text{discount}+\text{tax},
\qquad
\text{profit}=\text{recognized net}-\text{cost}.
$$

The exact business formula may differ; the point is to make it explicit. Decide whether refunds are negative facts, separate positive return facts or status changes. Never mix sign conventions silently.

Derived columns may improve performance, but retain source components and test the identity. If tax is excluded from revenue in one system and included in another, “net” is not conformed.

### Govern null, zero and exceptional values

Zero means the measure was observed and had no quantity under its contract. Null can mean unknown, not applicable, not yet observed or invalid. Those states should not be collapsed without policy.

SQL aggregate functions generally ignore null inputs except row-count forms, and aggregation over no input rows can return null. The current [PostgreSQL aggregate documentation](https://www.postgresql.org/docs/current/functions-aggregate.html) specifies engine behavior; a semantic contract must decide how that maps to business meaning.

For division, define denominator-zero behavior: null/not defined, zero by convention, infinite, error or excluded. Preserve a denominator/status measure so consumers can distinguish no opportunity from failed measurement.

### Govern time and snapshot behavior

Event measures belong to an event date role. State measures belong to an as-of instant or period. Processing date is useful for operations but does not replace business time.

For periodic snapshots, declare dense versus sparse capture, expected cadence and freshness. “Last balance in month” needs an ordering rule, tie-breaker and policy for missing final-day rows.

For accumulating snapshots, milestone dates may be dimensions while elapsed durations are facts. Reopened workflows need version/update policy so durations remain explainable.

### Build the semantic measure contract

For every published measure record name, business owner, description, process, base fact table, row grain, input columns, formula, allowed dimensions, default aggregation, time role, filters, units/currency, null/zero behavior, distinct population, allocation/conversion rules, freshness and version.

Also record what is forbidden. “Ending inventory” forbids sum across snapshot dates; “gross margin” forbids sum and unweighted average; “unique customers” forbids addition across overlapping groups.

Expose the contract in semantic-layer metadata and human documentation. Enforcement should be as close as possible to the query surface.

### Test facts and dimensions independently

For a fact table, test grain-key uniqueness, required dimension keys, one-member resolution, accepted measure ranges, units, formula identities, sign rules and additive controls.

For a dimension, test surrogate uniqueness, natural-key/version rules, required labels, hierarchy integrity, effective interval overlap and explicit special members.

Then test the star together: join row preservation, unmatched classification, filter propagation, role-playing dates, aggregate totals and drill-through reconciliation.

### Test measures at several grains

Use hand-recomputed fixtures at atomic, daily, monthly and all-up grains. A correct result at one grouping does not prove summarizability.

Test empty populations, one row, unequal subgroup sizes, null inputs, zero denominators, negative corrections, missing snapshots, multiple currencies, duplicated joins and overlapping distinct populations.

The [PostgreSQL `SELECT` documentation](https://www.postgresql.org/docs/current/sql-select.html) explains that `GROUP BY` forms groups and aggregates over their input rows. Database syntax supplies mechanics; the measure contract supplies the valid population and operator.

### Reconcile and observe production behavior

Reconcile additive facts to authoritative source totals by period, unit and sign class. Reconcile counts by event status and distinct business identity. Reconcile dimensions by source-member coverage and history state.

Monitor unknown-member rates, unmatched facts, duplicate grain keys, late-arrival corrections, currency/unit anomalies and denominator-zero frequency. Alert on semantic invariants, not just job success.

Retain evidence for changed measures. A new filter, date role or currency policy is a definition change even when the measure name stays the same.

### Evolve without silent semantic drift

Adding a fact that is valid at existing grain can be backward compatible if units and null behavior are clear. Changing grain, sign, time role, eligibility, denominator or conformance is usually breaking.

Version measures or dual-publish during migration. Backfill under a declared policy, compare old/new results across representative slices and obtain business-owner acceptance.

Deprecate unsafe implicit columns and aliases. Historical reports need enough metadata to identify which definition produced them.

## Definitions and Notation

Let $F$ be a fact relation whose row set is indexed by $i$ and whose declared grain key is $G(i)$. Let $D_1,\ldots,D_k$ be dimension roles. Each fact row maps through key $d_j(i)$ to exactly one intended member of $D_j$, including governed special members.

For a query population $S\subseteq F$ defined by authorized filters and valid joins:

- an additive measure is $A(S)=\sum_{i\in S}x_i$ for compatible units;
- a count is $C(S)=|S|$ only when row propositions are the counted events;
- a distinct count is $U(S)=|\{e(i):i\in S, e(i)\neq\text{NULL}\}|$;
- a ratio is $R(S)=\sum_{i\in S}n_i/\sum_{i\in S}d_i$ under denominator policy;
- a weighted mean is $\bar{x}_w(S)=\sum_iw_ix_i/\sum_iw_i$;
- an as-of balance is $B(S,t)=\sum_e b(e,\tau_e(t))$, where $\tau_e(t)$ selects the governed valid observation for entity $e$ at time $t$.

Represent the measure contract as $M=(X,A,D,U,N,W,C)$. `X` names inputs; `A` is aggregation/formula; `D` lists compatible dimensional rollups; `U` carries units; `N` defines missing/zero/invalid behavior; `W` defines window/as-of selection; `C` contains eligibility, security, allocation and other constraints.

A fact is **fully additive** if sum is valid across every dimension role under compatible units. It is **semi-additive** if the valid operator varies by dimension. It is **non-additive** when sum is not meaningful. These labels apply to a fact under a contract, not to a numeric data type in isolation.

Two dimensions are conformed for a use only if their member identities, attribute meanings and rollups are compatible for that use. Two facts are conformed when their names, units, calculations and dimensional context mean the same thing. Conformance can be exact or a governed shrunken rollup; name equality alone is insufficient.

## Mechanisms, Invariants, or Proof Structure

Use this mechanism for each analytical process:

1. Select the business process and declare the atomic or chosen row grain.
2. Inventory source observations, entity descriptors, keys, clocks, units and control totals.
3. Classify columns by semantic role rather than data type.
4. Choose dimension roles that are single-valued for each fact row.
5. Design dimension member identity, history, special members and hierarchies.
6. Place only measurements consistent with the grain in the fact table.
7. Separate different processes or grains into different fact tables.
8. Retain additive components for ratios, rates, averages and allocations.
9. Declare every measure's formula, population, unit, sign, null and zero rules.
10. Classify valid aggregation independently across each dimension, especially time.
11. Define role-playing dimensions, degenerate identifiers and factless events explicitly.
12. Resolve each fact to one intended dimension member at the correct time.
13. Aggregate multiple facts independently to compatible conformed dimensions.
14. Test keys, join preservation, formulas and measures across adversarial grains.
15. Reconcile to independent row, amount and coverage controls.
16. Version semantic changes and retain migration evidence.

The executable fixture uses exact integer currency units. It demonstrates algebraic measure behavior, not performance or production completeness.

<!-- bijux-verify: {"id":"fact-measure-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"net_revenue=395\ncost=260\nprofit=135\nratio_of_sums_margin=34.1772\naverage_line_margin=34.7222\nlatest_inventory=18\nsummed_snapshots=28\nidentity_holds=True\n","stderr":""}} -->
```python
sales = (
    {"net": 180, "cost": 120},
    {"net": 80, "cost": 50},
    {"net": 135, "cost": 90},
)
inventory = (
    {"day": "2026-09-01", "balance": 10},
    {"day": "2026-09-02", "balance": 18},
)

net = sum(row["net"] for row in sales)
cost = sum(row["cost"] for row in sales)
profit = net - cost
ratio_of_sums = 100 * profit / net
average_line_margin = sum(
    100 * (row["net"] - row["cost"]) / row["net"] for row in sales
) / len(sales)
latest_inventory = max(inventory, key=lambda row: row["day"])["balance"]
summed_snapshots = sum(row["balance"] for row in inventory)
identity_holds = all(row["net"] >= row["cost"] for row in sales) and profit == sum(
    row["net"] - row["cost"] for row in sales
)

print("net_revenue=" + str(net))
print("cost=" + str(cost))
print("profit=" + str(profit))
print("ratio_of_sums_margin=" + format(ratio_of_sums, ".4f"))
print("average_line_margin=" + format(average_line_margin, ".4f"))
print("latest_inventory=" + str(latest_inventory))
print("summed_snapshots=" + str(summed_snapshots))
print("identity_holds=" + str(identity_holds))
```

Critical invariants are:

- **Process:** every fact table belongs to a named business process.
- **Grain:** every stored fact and dimension role is valid at one declared row grain.
- **Resolution:** each dimension foreign key reaches exactly one intended member or governed special member.
- **Context:** dimension attributes are descriptive, governed and valid for the member version.
- **Measure:** formula, population, operator, unit, time, null and sign semantics are explicit.
- **Additivity:** each dimension has a permitted aggregation rule rather than a universal numeric default.
- **Components:** non-additive results retain sufficient additive inputs for correct regrouping.
- **Alignment:** facts at different grains meet only after independent aggregation or explicit allocation.
- **Reconciliation:** row counts, formula identities, control totals and coverage balance independently.
- **Evolution:** semantic changes are versioned and observable to consumers.

**Proof sketch — ratio of sums differs from an unweighted average of ratios.** For two rows with positive denominators, let $r_i=n_i/d_i$. The ratio of sums is $(d_1r_1+d_2r_2)/(d_1+d_2)$, a denominator-weighted average. The unweighted average is $(r_1+r_2)/2$. Their difference is

$$
\frac{(d_1-d_2)(r_1-r_2)}{2(d_1+d_2)}.
$$

Thus they agree when denominators are equal, ratios are equal or a special cancellation occurs; otherwise they generally differ. The same reasoning extends to many rows: the intended population ratio weights each component ratio by its denominator.

## Alternatives and Trade-Offs

**Atomic versus aggregate facts.** Atomic facts preserve detail and flexible slicing but increase storage and query cost. Aggregate facts accelerate known workloads but cannot recover discarded dimensions. Keep lineage and reconciliation when both are published.

**Stored derived fact versus query-time measure.** Storing derived amounts can reduce computation and freeze source-time rules, but it can duplicate logic and become stale. Query-time formulas centralize definitions but may be expensive. Retain base inputs and test any stored identity.

**One fact table versus process-specific facts.** A consolidated fact can simplify a narrow workload when grains and measures truly align. Separate tables preserve distinct process semantics and prevent null-filled mixed rows. Prefer semantic composition over physical conflation.

**Surrogate versus natural dimension key.** Surrogates support versioned members and compact joins. Natural keys aid source traceability but may change or collide across systems. Retain both with owned mapping.

**Unknown member versus nullable foreign key.** Special members keep facts visible and classify missingness; they require governance and later repair. Nulls are physically simple but can disappear in joins and merge different meanings.

**Last-value versus average snapshot measure.** Last-value answers point-in-time state; average answers exposure over a window. Duration-weighted average handles irregular observations but needs intervals. Publish separately rather than letting visuals choose.

**Exact distinct count versus approximate sketch.** Exact counts are auditable but can be costly at scale. Sketches reduce cost but introduce algorithm/version/error semantics and may not support deletion. Label them distinctly.

**Precomputed ratio versus components.** A stored ratio is convenient at its original grain but unsafe to sum or average. Components support regrouping and reconciliation. Store the ratio only as a convenience with aggregation disabled.

**Factless bridge versus direct many-to-many relationship.** A bridge makes membership grain, effective time and coverage explicit. Direct semantic relationships may be concise but can obscure fanout. Neither makes additive measures safe without allocation or careful counting.

**Degenerate identifier versus separate dimension.** Keeping an attribute-free transaction number in the fact avoids a redundant table. A dimension becomes useful when the entity gains descriptive attributes, security rules or history.

**One physical date dimension versus duplicated role views.** Sharing members ensures calendar consistency. Role-specific views/aliases improve clarity and filter behavior at some metadata cost.

**Implicit versus explicit measures.** Implicit aggregation is fast to expose but lets clients choose unsafe operators. Explicit measures encode policy, naming and tests. Governed analytical products should default to explicit measures.

## Failure Modes and Misconceptions

- **“Numbers are facts; strings are dimensions.”** Semantic role, not physical type, determines classification.
- **“Every fact must be numeric.”** Factless rows record countable occurrences or coverage.
- **“Every numeric fact can be summed.”** Prices, ratios, balances and indexes have other algebra.
- **“A measure is just a column.”** A measure includes population, operator, units, filters and time rules.
- **“`SUM` is a harmless default.”** It can create nonsense while returning valid numeric output.
- **“Average of averages is close enough.”** Unequal subgroup sizes produce systematic weighting error.
- **“Average margin should average row margins.”** Portfolio margin is normally profit sum divided by revenue sum.
- **“Null and zero are equivalent.”** Unknown/not-applicable is not observed zero.
- **“`count(column)` counts rows.”** Null inputs are excluded.
- **“Distinct counts add across groups.”** Overlap double-counts shared entities.
- **“Balance is additive because accounts add.”** It is commonly additive across accounts but not time.
- **“Last snapshot means latest loaded row.”** Business as-of order may differ from ingestion order.
- **“Descriptions can stay in the fact for convenience.”** Repetition allows inconsistent labels and history.
- **“Surrogate keys are measures because they are integers.”** They are identities and must not be summed.
- **“A foreign key null simply means unknown.”** It might mean not applicable, error, late arrival or redaction.
- **“One date key is enough.”** Order, ship, delivery and processing dates answer different questions.
- **“Two facts sharing customer and date can be joined.”** Many rows on both sides can multiply.
- **“Same column name means conformed.”** Meaning, units, membership and history must also align.
- **“Currency conversion is formatting.”** It is a temporal measure transformation with rate provenance.
- **“Refunds are always negative sales.”** Sign and process policy must be declared.
- **“A ratio has no denominator when displayed as a percent.”** The denominator determines aggregation.
- **“No fact row means zero activity.”** It can mean missing ingestion or ineligibility.
- **“A factless table needs no duplicate rule.”** Row existence is the measurement, so duplicates matter.
- **“Dimensions never contain numbers.”** Codes, sequence labels and descriptive numeric bands can be attributes.
- **“Facts never contain text.”** Degenerate identifiers and narrow operational attributes may be justified.
- **“A passing dashboard total validates the model.”** Offsetting errors and one grouping can hide failures elsewhere.

## Worked Examples

### Example 1

A sale-line fact stores quantity, gross amount, discount, tax and cost with product, store, customer, promotion and order-date keys. Every value describes the same accepted line event.

The semantic layer publishes quantity, gross, discount and cost sums within compatible units. Net revenue and profit use named formulas. Product description and category come from the product dimension, not repeated source text.

### Example 2

A daily account snapshot stores closing balance. Analysts sum balances across accounts for one date, then accidentally sum across 30 dates.

The measure contract marks account balance semi-additive: `SUM` across account and governed organization dimensions, last-valid or average-exposure across date. A separate balance-days measure may deliberately sum across dates with that unit.

### Example 3

Two campaigns have 1 conversion from 2 opportunities and 90 from 100. Averaging their conversion rates gives 70%, while the population conversion rate is $91/102\approx89.22\%$.

The fact retains conversions and eligible opportunities. Campaign rate can be shown per campaign; a rollup recomputes ratio of sums. Zero-opportunity campaigns return an explicit undefined status.

### Example 4

A school wants to identify students absent from scheduled classes. Attendance events alone cannot distinguish absence from a class that was never scheduled.

A coverage factless table records one row per expected student-class-date occurrence. An activity factless table records attendance. An anti-join at matching grain yields absences, while separate controls detect missing ingestion.

### Example 5

An order number has no attributes beyond its value, but users need to count orders and drill from sale lines to the operational record.

The model stores `order_number` as a degenerate dimension on the line fact. `distinct order count` is explicit; order number is hidden from numeric aggregation. If order-level attributes later appear, they belong in an order fact or dimension appropriate to their semantics.

### Example 6

A fulfillment fact has order date, promised date, ship date and delivery date. A dashboard's generic “date” relationship changes depending on which visual is opened.

The model exposes four named roles over one conformed calendar. Each measure declares its default role, and alternate-role measures are explicit. Tests filter a known fixture to prove which events appear under each calendar selection.

### Example 7

A sale fact references customer `C4`, but the customer dimension has two valid historical versions. Joining by natural key doubles the sale and labels it with both old and new region.

The fact load resolves the one version whose effective interval contains sale event time and stores that surrogate key. Overlap tests reject ambiguous histories. Unknown/late identities map to a classified placeholder and are later repaired audibly.

### Example 8

Daily ad spend and sale-line revenue share campaign and date dimensions. Joining raw tables by campaign-date multiplies every spend row by every sale line.

Each fact is aggregated independently to campaign-date, then the summaries join one-to-one. Return on ad spend divides revenue sum by spend sum with zero-spend behavior declared. Drill-through remains in each source fact.

### Example 9

Product weight arrives in kilograms from one system and pounds from another. Summing the raw numeric column yields a plausible but meaningless total.

The fact records source unit and original value, then derives canonical kilograms using a versioned conversion. Controls reconcile both representations. Measures either group by original unit or use only the canonical value.

### Example 10

A semantic model exposes temperature, sensor ID and quality score as implicit sums. A user sums sensor IDs and quality percentages across samples.

The model hides raw numeric identifiers, exposes sample count, mean/min/max temperature under the sampling contract, and derives valid-quality rate from accepted and total sample counts. Unsafe implicit aggregation is disabled.

## Cross-Program Connections

- [Database Engineering](../../18-database-engineering/ROADMAP.md): primary/foreign keys and temporal constraints enforce parts of fact-dimension resolution.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md): conformed dimensions and semantic measures define reusable enterprise interfaces.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md): late events, lineage and distributed aggregation affect fact correctness.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): retries, clocks and partial failure shape deduplicated measurement events.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md): finite representation and reduction order constrain numerical measure behavior.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md): measurement validity and reconciliation are system-level feedback invariants.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md): operational event contracts supply stable identities, clocks and quantities to facts.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): shared metric catalogs and semantic layers turn measure contracts into governed platform capabilities.

## References

1. Kimball Group, [Facts for Measurements](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/facts-for-measurement/). Defines measurement facts as process observations consistent with fact-table grain.
2. Kimball Group, [Dimensions for Descriptive Context](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/dimensions-for-context/). Describes dimension attributes as filtering and grouping context.
3. Kimball Group, [Additive, Semi-Additive, and Non-Additive Facts](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/additive-semi-additive-non-additive-fact/). Classifies numeric facts by summarizability and recommends retaining additive ratio components.
4. Kimball Group, [Factless Fact Tables](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/factless-fact-table/). Covers occurrence, coverage and analysis of events that did not happen.
5. Microsoft, [Dimensional Modeling in Fabric Data Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/dimensional-modeling-overview). Provides current star-schema context for facts, dimensions and analytical workloads.
6. Microsoft, [Modeling Fact Tables in Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/dimensional-modeling-fact-tables). Documents fact measurements, dimension keys, granularity, role-playing dimensions and special members.
7. Microsoft, [Understand Star Schema and Its Importance for Power BI](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema). Distinguishes fact and dimension roles and discusses explicit measures, degenerate dimensions and factless facts.
8. PostgreSQL Global Development Group, [Aggregate Functions](https://www.postgresql.org/docs/current/functions-aggregate.html). Defines aggregate behavior, including count, sum and average semantics.
9. PostgreSQL Global Development Group, [`SELECT`](https://www.postgresql.org/docs/current/sql-select.html). Defines grouping, filtering and aggregate evaluation mechanics.

## Exercises

### Exercise 1

A checkout source supplies `order_id`, `line_id`, `product_code`, `product_name`, `customer_id`, `quantity`, `unit_price`, `discount_rate`, `net_amount`, `currency`, `order_timestamp` and `loaded_at`. The intended grain is one accepted order line. Classify every column as grain identity, dimension reference/attribute, fact input, degenerate identifier or operational metadata. Identify unsafe aggregations and propose the target fact/dimension arrangement.

### Exercise 2

Store A has 1 return among 10 sales; Store B has 40 returns among 100 sales. Compute each rate, the unweighted average of store rates and the overall return rate. Define the stored inputs, formula, denominator-zero behavior and valid rollup mechanism.

### Exercise 3

An inventory table contains product-store balances at irregular timestamps. Specify measures for end-of-day inventory, average inventory exposure and inventory change. Address missing observations, late records, ties, negative balances and aggregation across products, stores and time.

### Exercise 4

A university has course offerings, student enrollments and attendance scans. Design the fact and dimension structures needed to answer: attendance events, attendance rate, students absent from required sessions and distinct attendees by department. State grains and explain where counts are non-additive.

### Exercise 5

Marketing spend is daily at campaign-channel grain, leads are event-level, and revenue is sale-line-level. Design a safe campaign performance model and query pathway. Include conformed dimensions, attribution/allocation assumptions, role-playing time, zero denominators and reconciliation tests.

## Answers to the Exercises

### Answer 1

`(order_id,line_id)` is the business grain identity; `order_id` also serves as a degenerate drill-through/grouping identifier. `product_code` and `customer_id` resolve product and customer dimensions; `order_timestamp` resolves an order-date/time role. `quantity`, unit price, discount components and net amount are measurement inputs. `currency` is a unit/currency role or invariant only within constrained facts. `loaded_at` is operational lineage. `product_name` belongs in the product dimension and must not be trusted independently on every line.

Quantity and compatible currency amounts can be additive. Unit price and discount rate must not be summed; weighted price uses amount/quantity components, and effective discount rate uses total discount divided by eligible gross. Test `net_amount` against its declared formula. The line fact carries surrogate dimension keys, degenerate order number, timestamps and additive components; dimensions carry governed descriptions/history. Currency conversion, nulls, reversals and late customer/product resolution require explicit policy.

### Answer 2

Store A's rate is $1/10=10\%$ and Store B's is $40/100=40\%$. The unweighted store average is $(10\%+40\%)/2=25\%$. The overall rate is $41/110\approx37.27\%$. The difference arises because stores have unequal denominators.

Store additive `return_count` and `eligible_sale_count`, or derive them from uniquely identified event/status facts. Publish `return_rate=sum(return_count)/sum(eligible_sale_count)`. When the denominator is zero, return null plus the zero opportunity count rather than inventing performance. Rollups always aggregate components first; tests cover empty, one-store, unequal-size and corrected-sale populations.

### Answer 3

Declare snapshot grain as one product-store observation at an effective instant with deterministic observation identity. End-of-day inventory selects the last valid observation at or before the business cutoff within a freshness threshold. Ties use source sequence and stable identity; unresolved conflicting ties quarantine. Late observations trigger governed restatement or a new as-known version.

Average exposure integrates balance over valid time intervals and divides by covered duration, with gaps reported; a simple sample mean is only valid under the sampling contract. Inventory change is closing minus opening balance or a sum of complete movement facts. At one instant, compatible balances add across products/stores; across time use last/average/change rather than sum. Negative balances may be valid backorders or rule violations by product policy. Tests cover no observation, stale carry-forward, irregular intervals, correction and timezone cutoff.

### Answer 4

Use dimensions for student, course, offering, department, instructor, location and calendar/session roles. An offering/session factless coverage table has one row per scheduled offering-session. Enrollment coverage has one row per required student-session after effective enrollment rules. Attendance activity has one row per accepted student-session attendance event; repeated scans are deduplicated or modeled as scan events separately.

Attendance count is row count at accepted attendance grain. Attendance rate is attended required sessions divided by eligible required sessions. Absence is the anti-join of enrollment coverage to accepted attendance, not absence from raw scans. Distinct attendees by department must be recomputed per group; adding course-level distinct counts double-counts students who attend multiple courses. Reconcile scheduled sessions, enrollment eligibility, scan acceptance and unknown students independently.

### Answer 5

Keep spend at campaign-channel-day, leads at one lead event, and revenue at sale-line grain. Conform campaign, channel and calendar members; define spend date, lead-created date and sale/recognition date as explicit roles. Aggregate each fact independently to the reporting grain before joining. Never join raw leads to raw sales through campaign.

Attribution from sales to campaign is a separate governed relationship with model/version, eligibility window and weights summing according to policy. Publish unallocated authoritative revenue separately. Cost per lead is spend sum divided by accepted lead count; return on ad spend is attributed recognized revenue divided by spend, each with null/zero-denominator status. Reconcile spend to billing, leads to accepted event identities, revenue to finance controls, attribution weights by sale and joined summaries for one-row uniqueness at campaign-channel-period.
