---
module_id: DE-014
program: Data Engineering
level: 1
module_number: 14
title: Slowly Changing Dimensions
status: complete
last_verified: 2026-09-02
---

# Slowly Changing Dimensions

## One-Page Review

### Governing question

When a descriptive attribute changes, should historical facts retain the value that was valid when they occurred, be restated under the current value, retain only an original/previous value, or support more than one of those views—and how will the model prove the choice?

### Essential definitions

- A **slowly changing dimension (SCD)** is a dimension whose attribute changes are handled by an explicit historical policy rather than an accidental overwrite.
- A **durable/business key** identifies the same business entity across versions; a **surrogate key** identifies one warehouse dimension row/version.
- **Valid time** is when an attribute value is true in the business domain. **System/load time** is when the warehouse learned or recorded it.
- A **half-open interval** $[s,e)$ includes its start and excludes its end, so adjacent versions can meet at one boundary without overlap.
- **Type 0** retains the original attribute. **Type 1** overwrites it. **Type 2** adds a new dimension row/version. **Type 3** adds a column for limited alternate/previous state.
- A **mini-dimension (Type 4)** separates a set of volatile profile attributes and assigns the fact both base and profile keys.
- **Types 5, 6 and 7** are hybrid techniques that support both historical and current-value analysis using current outriggers/attributes or dual keys.
- An **inferred member** is a placeholder dimension row created so an early fact can resolve before descriptive details arrive.
- A **late-arriving change** has a business-effective time earlier than its warehouse arrival, possibly requiring interval surgery and fact restatement.
- **As-was reporting** groups a fact by the dimension version valid at fact time; **as-is reporting** groups historical facts by the entity's current classification.

### Central model, mechanism, or theorem

For durable entity key $b$, model Type 2 versions

$$
V_b=\{v_1,\ldots,v_k\},\qquad I(v_i)=[s_i,e_i),
$$

where each version has a unique surrogate key and governed tracked attributes. Correct publication requires nonempty, nonoverlapping intervals; exactly one intended version must resolve for every fact time in the covered domain:

$$
|\{v\in V_b:t_f\in I(v)\}|=1.
$$

A fact stores that resolved surrogate key for stable as-was analysis. As-is analysis must use a separately named current path. Under disjoint half-open intervals, as-of resolution is unique; completeness is a separate coverage requirement.

### Critical invariants

- SCD behavior is chosen per attribute from business reporting needs, not per table by habit.
- Durable keys identify entities; surrogate keys uniquely identify Type 2 versions and remain stable once facts reference them.
- Type 2 intervals are nonempty, nonoverlapping and consistently half-open.
- There is at most one current version per durable key and exactly one when the entity is active under policy.
- Fact resolution uses the declared business/effective time, not ingestion time by convenience.
- Every eligible fact resolves to one version or an explicit unknown/inferred/error member.
- Type 1 overwrite is acknowledged as restatement and triggers affected aggregate/cache refresh.
- Current and historical rollups use distinct paths and names; neither silently substitutes for the other.
- Late corrections are idempotent, preserve audit evidence and restate affected facts only under an approved policy.
- Deletes, merges, splits, privacy erasure and source-key reuse have explicit semantics beyond ordinary attribute change.

### Common failures

Calling every update Type 1; applying one SCD type to all attributes; using natural key as a Type 2 primary key; assigning a new durable identity on every change; inclusive interval ends that double-match boundaries; gaps or overlaps; multiple current rows; resolving facts by load date; regenerating surrogate keys on full reload; hashing unstable serialization; treating changed audit timestamps as business change; expiring and inserting non-atomically; losing late facts; modifying an old Type 2 row in place; joining facts by durable key without as-of/current intent; labeling current rollup as historical; turning volatile continuous measurements into version explosions; interpreting source deletion as warehouse erasure; and assuming a Type 2 table alone provides bitemporal audit.

### Compact example

Customer `C1` belongs to North from January 1 until March 1, then West from March 1 onward. A February fact resolves to the North surrogate; March and April facts resolve to West. As-was totals are North 40 and West 80. As-is reporting through the current customer classification groups all 120 under West. Both answers can be valid, but they answer different questions and must use explicit paths.

### Connections

[DE-011](011-grain-and-the-meaning-of-a-row.md) defines row identity and time, [DE-012](012-facts-dimensions-and-measures.md) defines fact/dimension roles, and [DE-013](013-star-and-snowflake-schemas.md) establishes safe hierarchy paths. Planned DE-015 extends snapshot fact behavior and is indexed in the [Data Engineering roadmap](../ROADMAP.md). Temporal constraints connect to [Database Engineering](../../18-database-engineering/ROADMAP.md), historical conformance to [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md), and atomic publication to [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md).

## Governing Question

For each mutable dimension attribute, can its owner state which historical question must remain answerable, which timestamps define truth, and which exact dimension row every old and new fact should reference?

“Slowly changing” describes a modeling family, not a promise that changes are rare. A customer segment may change daily; a legal name may change once; a product category correction may arrive months late. The engineer's task is to preserve the required analytical perspectives with controlled identity, intervals and restatement.

The [Kimball SCD Type 2 guidance](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/type-2/) distinguishes durable identity from version-row identity: a new tracked value creates a new row with a new surrogate key, and facts use the applicable key. Effective/expiration timestamps and a current indicator make version state explicit.

History requirements precede implementation. If all prior facts should appear under today's sales region, Type 1 may be correct. If reports must reproduce the region at transaction time, Type 2 is needed. If both views matter, a hybrid/current path is warranted. Type numbers are shorthand; business names such as `region_at_sale` and `current_region` prevent misuse.

## Why This Matters

Dimensions drive filters and groupings. Overwriting a customer's region can move years of revenue between regions without changing a fact row. That may be intentional restatement—or silent corruption of historical reporting. SCD policy determines which one.

Type 2 history makes facts reproducible under past context. A sale that stores the surrogate customer version selected at event time remains attached to that version even after later changes. This supports audit, cohort and policy analysis.

The same history introduces sharp invariants. Overlapping versions double-match facts. Gaps leave facts unmatched. Inclusive end dates can match two rows at midnight. Multiple current flags confuse current reporting. A surrogate sequence that changes after reload breaks every referencing fact.

Late-arriving data makes the problem operational. A change effective last month but received today may split an existing interval and require facts in that period to be re-keyed. The warehouse must decide whether reports restate, preserve knowledge-as-of-load, or retain both valid and system time.

Advanced SCD types exist because users often need both as-was and as-is questions. They add power and complexity. Explicit role names, tests, lineage and semantic measures are essential so the same “region” label does not select different populations unpredictably.

## Prerequisites and Retrieval

Retrieve dimension purpose and grain; durable/business keys; source-system identifiers and key-reuse policy; existing surrogate keys; every dimension attribute and owner; which attributes are immutable, corrective, current-only or historically tracked; valid-time and load-time timestamps; source precision/timezone; source change-data-capture sequence; delete/tombstone behavior; merge/split/reparent events; late and out-of-order frequency; fact event-time fields; existing fact foreign keys; inferred/unknown members; interval boundary convention; current flag; source precedence; attribute canonicalization; hash/diff logic; null semantics; initial effective date; open-ended sentinel policy; active/inactive policy; load concurrency; transactional guarantees; restatement rules; aggregate/materialized view dependencies; privacy/retention constraints; historical report requirements; current-rollup requirements; audit horizon; data volume/change rate; backfill strategy; reconciliation controls; and downstream semantic relationships.

Distinguish entity identity from row version; natural/durable key from source-local key; surrogate key from change sequence; attribute correction from real-world change; valid time from load/system time; event time from dimension effective time; as-was from as-is; Type 0 from Type 1; Type 2 versioning from event sourcing; Type 3 prior value from complete history; mini-dimension profile from base entity; current flag from latest loaded row; unknown from inferred and not applicable; deletion from inactivation and erasure; late dimension detail from late business-effective change; gap from intentional inactivity; closed-open from inclusive-inclusive intervals; and full historical retention from bitemporal knowledge history.

Build a source change matrix. For each attribute, record example old/new values, authoritative timestamp, correction rules, historical questions, selected technique, consumer impact and tests. Include boundary facts exactly at change time, duplicate changes, changes that revert to an earlier value, same-timestamp conflicts, no-op normalization differences and new entities whose first fact arrives before details.

## Learning Objectives

After completing this module, you should be able to:

1. select SCD behavior per attribute from reporting requirements;
2. distinguish durable entity identity from Type 2 version identity;
3. model and prove nonoverlapping half-open effective intervals;
4. resolve facts deterministically to the correct version at business time;
5. implement Types 0, 1, 2 and 3 and explain their information loss;
6. evaluate mini-dimension and hybrid Types 4 through 7;
7. handle inferred members, late changes, deletions and source-key anomalies;
8. separate as-was, as-is and knowledge-as-of reporting paths;
9. test, reconcile and observe dimension/fact history; and
10. migrate SCD policy without breaking historical interpretation.

## Core Exposition

### Start with attribute-level questions

Do not declare an entire dimension “Type 2” without examining attributes. A durable customer identifier may be Type 0; a corrected spelling may be Type 1; sales region may be Type 2; a current segment path may be hybrid.

For each attribute ask whether users need original, current, previous, complete as-was, knowledge-as-of or multiple perspectives. Write those questions in business language.

Group attributes into change sets only when they share effective time, source authority and history policy. One changed tracked attribute can create a new Type 2 row carrying a complete consistent version.

### Establish durable identity

The durable/business key links all versions of one entity. It must survive attribute changes and be scoped by source when identifiers can collide.

Source systems may reuse identifiers after deletion, merge customers or split organizations. A durable identity service or mapping policy must decide whether these are the same analytical entity.

Never infer durable sameness only from mutable names, addresses or email. Preserve mapping evidence and version it.

### Establish surrogate version identity

Each Type 2 row has a unique surrogate key. Facts reference this key so the selected historical context remains stable.

Do not truncate and regenerate surrogate keys. The current [Microsoft Fabric load guidance](https://learn.microsoft.com/en-us/fabric/data-warehouse/dimensional-modeling-load-tables) warns that regenerating dimension surrogates invalidates fact references and may make historical versions unrecoverable.

Surrogate allocation should be concurrency-safe and idempotent. A replay of the same logical change must find the existing version rather than create another.

### Model Type 0 retain-original attributes

Type 0 never changes after first authoritative capture. Original acquisition channel, original credit band or birth date under a retain-original contract are examples.

Reject or quarantine later differences unless an explicit correction process exists. “Immutable” is a policy, not a belief that sources never send changes.

If corrections are legally required, define whether they rewrite the original, create audit evidence elsewhere or produce a new semantic attribute.

### Model Type 1 overwrite attributes

Type 1 replaces the old value in the existing dimension row. The [Kimball Type 1 description](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/type-1/) emphasizes that this destroys prior attribute history.

Use it for corrections, attributes where only current truth matters, or deliberate restatement. Update every applicable version row when a current-only attribute coexists in a Type 2 dimension, depending on the chosen hybrid design.

Rebuild affected aggregates, cubes, caches and extracts. The fact table may not change, but its grouping labels and totals can.

### Model Type 2 add-row history

Type 2 expires the current version and inserts a new row with a new surrogate key. Retain durable key, version attributes, effective start/end and current status.

Use half-open intervals `[effective_from,effective_to)`. A change at `2026-03-01T00:00Z` makes the old version end and the new version start at that same instant; exactly one contains the boundary.

Choose open-ended representation: nullable end, infinity, or a maximum sentinel supported by every consumer. Do not mix conventions.

### Model Type 3 limited alternate state

Type 3 adds a column for a previous or alternate value while updating the primary current value. It retains limited history without adding rows.

The column must be semantically named, such as `previous_sales_region`, not `region_2`. A second change usually replaces the previously retained value, so this is not complete history.

Type 3 is useful for a stable organizational redefinition when users compare old/new classifications, but it scales poorly for unbounded change.

### Build a Type 2 row contract

A robust row includes surrogate key, durable key, tracked attributes, `valid_from`, `valid_to`, `is_current`, source version/sequence, record digest, load metadata and optional delete/status fields.

`is_current` is redundant with an open end but useful for access and validation. Redundancy creates an invariant: it must agree with interval state.

Separate source-effective metadata from warehouse audit metadata. A load timestamp cannot substitute for a missing business-effective time without an explicit approximation label.

### Use consistent half-open intervals

Half-open intervals avoid double matches at shared boundaries and work at any timestamp precision. Adjacent versions satisfy $e_i=s_{i+1}$.

Inclusive “end of day” timestamps such as `23:59:59` fail when source precision increases. Subtracting a millisecond or microsecond embeds engine-specific gaps.

Normalize timezones and precision before interval comparison. Preserve the raw source timestamp for audit.

### Enforce nonoverlap

For every durable key, require

$$
i\neq j\Rightarrow I(v_i)\cap I(v_j)=\varnothing.
$$

Database range/exclusion or temporal constraints can enforce this where available. PostgreSQL's current [range-type documentation](https://www.postgresql.org/docs/current/rangetypes.html) describes range values and exclusion constraints for nonoverlap.

Analytical engines may not enforce constraints; run exact interval tests during staging and before publication. Detect duplicates, inversions and zero-length intervals too.

### Enforce current-row cardinality

At most one row per durable key has `is_current=true`. Active entities generally require exactly one; closed/deleted entities may intentionally have zero.

Do not define current as the maximum surrogate key. Allocation order may differ from effective time, and late changes can insert older versions later.

Derive or validate current from the open interval and entity-status policy. Monitor multiple/zero current rows separately.

### Detect meaningful changes

Compare only attributes governed by the selected policy. Audit timestamps, whitespace normalization or source extraction order should not create Type 2 versions unless semantically material.

Canonicalize strings, nulls, decimals, codes and timezones before diffing. A record hash is an optimization over a declared canonical serialization, not the business rule itself.

On hash match, optionally compare fields in high-assurance paths to guard collision/serialization defects. Store the hash version so algorithms can evolve.

### Resolve facts as of event time

For fact durable key $b$ and event time $t_f$, choose the unique version satisfying

$$
v.b=b\land v.s\leq t_f<v.e.
$$

Resolve during fact loading and store the surrogate key. This makes ordinary star joins direct and stable.

If zero versions match, classify the reason: early fact, gap, unknown identity, timestamp error or deleted entity. If several match, quarantine because history overlaps.

### Separate as-was and as-is analysis

As-was joins a fact's stored Type 2 surrogate and reports the attributes valid at fact time. As-is follows durable identity to the current version and restates history under current attributes.

Give columns and measures explicit names such as `region_at_order` and `current_customer_region`. Never expose two paths both called `region`.

Hybrid Types 6 and 7 support both perspectives with different physical strategies. Test them with entities that change groups between fact dates.

### Handle Type 4 mini-dimensions

Type 4 separates rapidly changing or frequently analyzed profile attributes into a mini-dimension. Each distinct governed profile receives a surrogate key; facts store both base entity and profile keys.

The [Kimball Type 4 guidance](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/type-4-mini-dimension/) positions this technique for volatile attribute groups and large base dimensions.

Control profile cardinality. Continuous raw values can create near-one-row-per-fact profiles; band them only under a governed classification while retaining original measurements as facts where needed.

### Understand Type 5

Type 5 adds a current Type 1 mini-dimension reference to the base dimension while facts preserve the profile applicable at event time. It supports current profile access without traversing facts.

Name outrigger fields as current. Updating the base reference restates the current perspective but leaves historical fact profile keys intact.

This hybrid couples base-dimension refresh to profile changes and requires path-consistency tests.

### Understand Type 6

Type 6 embeds current versions of selected attributes on all Type 2 rows, while each row also retains its historical values. A current change updates the current attribute across every historical row for the durable key.

The approach makes both paths available through one dimension join but increases write amplification and redundant-state invariants.

Use distinct names and reconcile all rows for one durable key to the same current value. A partial update creates silent mixed rollups.

### Understand Type 7

Type 7 stores two fact-side routes: a surrogate key to the historical Type 2 row and a durable key that can reach the current row. It avoids rewriting current attributes onto all history rows.

The semantic model must constrain the durable-key current join to exactly one row. Historical and current relationships need explicit roles to avoid ambiguous filter paths.

Type 7 is powerful for dual reporting, but a generic durable-key join without current filtering fans out across every version.

### Choose hybrids by requirements

The [Kimball advanced SCD design tip](https://www.kimballgroup.com/2013/02/design-tip-152-slowly-changing-dimension-types-0-4-5-6-7/) summarizes Types 0 and 4–7 and their current/historical purposes. Use descriptive technique names alongside numbers because not every team uses the numbering consistently.

Prefer the simplest technique that answers required questions. Extra current paths multiply tests, documentation and user choices.

Record a decision table per attribute group: retained views, storage path, fact keys, update behavior and query examples.

### Handle inferred members

When a fact arrives before its dimension details, create an inferred member keyed by the durable identity with placeholder descriptions and an inferred flag, or quarantine the fact under policy.

When details arrive, fill the same inferred surrogate if they describe the same applicable version. Do not treat placeholder completion as a new business change automatically.

If later evidence shows the fact belongs to a different historical version, apply the late-arriving policy and retain repair lineage.

### Handle late-arriving dimension changes

Suppose an entity has interval `[Jan 1, infinity)` and a change effective March 1 arrives in April. Split the interval at March 1 and create the new version. Facts from March onward may need re-keying.

If another version already begins April 1, the late change creates `[Mar 1,Apr 1)` rather than overwriting the April version. Sort by business effective time and reconcile the whole key history.

Define a correction/restatement window, affected-report communication and idempotent replay. Retain original load evidence when knowledge-as-of reporting matters.

### Distinguish valid and system time

A Type 2 dimension typically records valid-time history, but its row updates can overwrite what the warehouse previously believed. It is not automatically bitemporal.

For knowledge-as-of questions—“what did the warehouse know on April 5?”—retain system-time versions or immutable change audit in addition to valid intervals.

Represent the two axes explicitly. Avoid calling load timestamps `effective_from`.

### Handle corrections versus changes

A correction says the prior recorded value was wrong for its claimed period; a change says reality transitioned at a boundary. They require different interval edits and governance.

For a correction affecting one old interval, update or supersede that version under audit policy. Do not create a new “change today” that leaves historically wrong facts attached.

Require reason code, source evidence, actor/process and affected range. Reconcile impacted facts and aggregates.

### Handle deletions and inactivity

Source disappearance may mean deletion, extract filtering, outage or inactivity. Do not infer semantics from “not matched by source” without source contract.

An inactive entity can close its current interval or create a Type 2 inactive version. Facts after closure require rejection or special semantics.

Privacy erasure can conflict with historical retention. Tokenize, redact or delete under legal policy while preserving only permitted aggregate/audit evidence. Ordinary SCD history is subordinate to those requirements.

### Handle merges, splits and key reuse

When two source identities merge, decide whether prior facts remain under original durable keys, map to a surviving identity for current reporting, or support both. Do not rewrite silently.

Splits create new entities and allocation/lineage questions. A reused source ID may require source era or generation in the durable key.

Maintain an identity relationship table for predecessor, successor, merge and split semantics rather than overloading Type 2 attribute versions.

### Publish changes atomically

A simple Type 2 change expires one current row and inserts its successor. Consumers must not observe a state with neither or both current rows unless the storage transaction/snapshot guarantees isolation.

Stage and validate proposed histories before publishing. Use transactions, atomic table/version swaps or snapshot commits supported by the platform.

Concurrency on the same durable key requires serialization, optimistic conflict detection or deterministic merge. Retrying must not create duplicate versions.

### Test dimension history

Test surrogate uniqueness, durable-key presence, nonempty intervals, nonoverlap, current-row cardinality, start/end precision, tracked-attribute hashes and source-sequence uniqueness.

Test coverage across the declared domain, including exact boundaries. Gaps may be legitimate only with reason/status.

Test attribute-specific policy: Type 0 never changes; Type 1 matches current authority; Type 2 changes yield versions; Type 6 current columns agree across all versions.

### Test fact resolution

For every eligible fact, assert exactly one resolved surrogate and verify the fact time lies in that version's interval. Compare stored resolution to a fresh authoritative as-of join.

Track unknown/inferred/error rates by source and time. A global low rate can hide a complete outage for a new source.

Test facts exactly at start/end boundaries, before first version, after closure, during gaps and around timezone transitions.

### Reconcile reporting perspectives

For additive facts, as-was and as-is grand totals should agree when they differ only in grouping classification and include the same population. Group distributions may differ.

Reconcile Type 1 restatements to affected aggregates and semantic caches. Reconcile late Type 2 repairs by before/after fact key and group totals.

If totals differ, isolate filters, unknown members, security or fanout before accepting “history changed” as explanation.

### Observe operational health

Monitor change counts by attribute/type, version rows per entity, interval overlaps/gaps, current-row defects, late-change age, inferred duration, restated fact count and special-member rates.

Watch sudden cardinality growth from unstable hashes or volatile attributes. Track dimension load/fact resolution latency and consumer query paths.

Retain distributions and examples, not only pass/fail. Slow drift often appears before thresholds fail.

### Evolve SCD policy safely

Moving Type 1 to Type 2 cannot reconstruct history that was never retained; source snapshots, logs or external evidence are required. State limitations explicitly.

Moving Type 2 to current-only should preserve an archival contract if historical consumers exist. Do not delete version rows merely to simplify diagrams.

For migrations, build new keys/intervals, dual-resolve facts, compare representative reports, version semantic paths and preserve rollback mappings until acceptance.

## Definitions and Notation

For durable key $b$, let version set $V_b$ contain rows $v$ with unique surrogate $k(v)$, tracked attributes $A(v)$ and valid interval $I(v)=[s(v),e(v))$. Use $e(v)=+\infty$ or one consistently governed representation for the open current end.

Define interval containment and overlap:

$$
t\in I(v)\iff s(v)\leq t<e(v),
$$

$$
I(v_i)\cap I(v_j)\neq\varnothing
\iff \max(s_i,s_j)<\min(e_i,e_j).
$$

The nonoverlap invariant requires the latter to be false for every distinct pair sharing $b$. Nonempty intervals require $s(v)<e(v)$.

Define fact resolution

$$
\rho(b,t)=\{v\in V_b:b(v)=b\land t\in I(v)\}.
$$

Uniqueness is $|\rho(b,t)|\leq1$; complete coverage for an eligible fact is $|\rho(b,t)|=1$. These are separate properties.

For fact $f$, historical grouping uses $A(\rho(b_f,t_f))$. Current grouping uses attribute $A(c(b_f))$ where $c(b)$ is the unique current version under entity-status policy. Grand-total preservation between those groupings requires the same fact population and a many-to-one classification path.

If system time is retained, each assertion also has system interval $J(v)=[u(v),z(v))$. A bitemporal query selects both business-valid and system-known intervals. Valid-time Type 2 alone supplies only $I$.

## Mechanisms, Invariants, or Proof Structure

Use this mechanism for each mutable dimension:

1. Define entity grain and durable identity, including merge/split/key-reuse policy.
2. Inventory attributes and authoritative valid/load/change timestamps.
3. Classify required views per attribute: original, current, prior, as-was or knowledge-as-of.
4. Choose the simplest SCD technique per coherent attribute group.
5. Define surrogate allocation, interval convention, open end and current status.
6. Canonicalize tracked values and version change-detection logic.
7. Stage proposed histories and reject duplicate, empty, overlapping or ambiguous versions.
8. Apply new, changed, late, corrected, deleted and inferred-member cases idempotently.
9. Publish expiration/insertion and affected fact changes atomically.
10. Resolve facts using durable key plus declared business time.
11. Expose historical and current query paths with distinct semantic names.
12. Test attribute policy, interval invariants, fact coverage and boundary instants.
13. Reconcile facts, aggregates and group movements after every restatement.
14. Monitor history growth, lateness, inferred members and current-row health.
15. Retain valid/system-time audit required by the reporting horizon.
16. Version policy changes and migrate consumers with dual-run evidence.

The executable fixture uses ISO dates and exact integer amounts to demonstrate interval resolution and two reporting perspectives. It is not evidence about database concurrency, optimizer behavior or a production history.

<!-- bijux-verify: {"id":"scd-as-of-resolution","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"versions=2\ncurrent_versions=1\noverlaps=0\nresolved_surrogates=[101, 102, 102]\nhistorical_totals={'North': 40, 'West': 80}\ncurrent_totals={'West': 120}\ngrand_totals_equal=True\n","stderr":""}} -->
```python
versions = (
    {"surrogate": 101, "durable": "C1", "region": "North", "start": "2026-01-01", "end": "2026-03-01", "current": False},
    {"surrogate": 102, "durable": "C1", "region": "West", "start": "2026-03-01", "end": None, "current": True},
)
facts = (
    {"fact": "F1", "durable": "C1", "when": "2026-02-15", "amount": 40},
    {"fact": "F2", "durable": "C1", "when": "2026-03-01", "amount": 60},
    {"fact": "F3", "durable": "C1", "when": "2026-04-01", "amount": 20},
)

def contains(version, instant):
    return version["start"] <= instant and (version["end"] is None or instant < version["end"])

def overlaps(left, right):
    left_end = left["end"] or "9999-12-31"
    right_end = right["end"] or "9999-12-31"
    return max(left["start"], right["start"]) < min(left_end, right_end)

resolved = []
historical_totals = {}
for fact in facts:
    matches = [v for v in versions if v["durable"] == fact["durable"] and contains(v, fact["when"])]
    assert len(matches) == 1
    version = matches[0]
    resolved.append(version["surrogate"])
    historical_totals[version["region"]] = historical_totals.get(version["region"], 0) + fact["amount"]

current = [v for v in versions if v["current"]]
current_totals = {current[0]["region"]: sum(fact["amount"] for fact in facts)}
overlap_count = sum(overlaps(versions[i], versions[j]) for i in range(len(versions)) for j in range(i + 1, len(versions)))

print("versions=" + str(len(versions)))
print("current_versions=" + str(len(current)))
print("overlaps=" + str(overlap_count))
print("resolved_surrogates=" + str(resolved))
print("historical_totals=" + str(dict(sorted(historical_totals.items()))))
print("current_totals=" + str(current_totals))
print("grand_totals_equal=" + str(sum(historical_totals.values()) == sum(current_totals.values())))
```

Critical invariants are:

- **Identity:** durable key groups entity versions; surrogate key identifies exactly one row.
- **Interval:** every version is nonempty and intervals for one durable key do not overlap.
- **Current:** current-row cardinality agrees with active/inactive policy.
- **Resolution:** each eligible fact maps to exactly one version at declared business time.
- **Stability:** referenced surrogate keys are not regenerated or repurposed.
- **Attribute policy:** every change follows its declared retain, overwrite, version or hybrid rule.
- **Perspective:** as-was and as-is paths are distinct and preserve the intended fact population.
- **Audit:** late changes and corrections retain source, reason and before/after evidence.
- **Atomicity:** expiration, insertion and re-keying are not partially published.
- **Reconciliation:** version keys, facts and totals balance after every change.

**Proof sketch — disjoint half-open intervals guarantee unique as-of resolution.** Suppose two distinct versions $v_i,v_j$ of the same durable key both resolve for time $t$. Then $t\in I(v_i)$ and $t\in I(v_j)$, so their intersection is nonempty, contradicting the nonoverlap invariant. Therefore at most one version resolves. Half-open boundaries make adjacent intervals `[a,b)` and `[b,c)` disjoint because $b$ is excluded from the first and included in the second. Existence still requires coverage; uniqueness alone permits gaps.

## Alternatives and Trade-Offs

**Type 0 versus correction path.** Retain-original gives stable cohort identity but preserves source mistakes. A governed correction path can repair errors while retaining audit. Define which meaning “original” carries.

**Type 1 versus Type 2.** Type 1 is compact and serves current restatement but destroys past classification. Type 2 preserves as-was context at row-growth and load/query complexity cost.

**Type 3 versus full history.** Type 3 makes one prior/alternate view easy but has bounded capacity. Type 2 or event history supports unbounded changes.

**Type 2 versus event sourcing.** Type 2 materializes valid dimension states for analytics. An event log preserves change causality. Retain both when audit/reconstruction needs exceed dimensional querying.

**Nullable open end versus sentinel.** Null expresses unboundedness but complicates predicates; a sentinel simplifies comparison but can collide with real dates or platform limits. Standardize one contract.

**Date versus timestamp intervals.** Dates are simpler for day-effective policy. Timestamps preserve intraday transitions but require timezone/precision discipline. Match source/business semantics.

**Resolve at load versus query.** Load-time surrogate resolution makes queries simple and stable; late corrections require re-keying. Query-time as-of joins use latest history but cost more and can change reports. Often store the historical key and offer separate restated paths.

**Type 4 versus Type 2 explosion.** Mini-dimensions control base-dimension churn for volatile profiles but add fact keys and profile semantics. Ordinary Type 2 is simpler for modest change.

**Type 6 versus Type 7.** Type 6 makes current attributes available in one join but rewrites all historical rows. Type 7 avoids that rewrite with dual paths/keys but demands careful semantic relationships.

**Restate facts versus preserve prior reports.** Re-keying late facts improves valid-time truth; immutable prior report reproduction needs system-time snapshots/audit. Dual requirements imply bitemporal evidence or versioned outputs.

**Database constraint versus validation job.** Enforced temporal constraints reject overlap immediately where supported. Batch tests work across analytical engines but permit bad staged data. Use both where practical.

**Full reload versus incremental merge.** Full rebuild can simplify deterministic derivation but must preserve surrogate mappings and atomic publication. Incremental changes reduce work but complicate out-of-order history. Test equivalence.

## Failure Modes and Misconceptions

- **“SCD type is chosen per table.”** Different attributes often require different policies.
- **“Slowly means changes are infrequent.”** The techniques also handle volatile attributes; rate affects design.
- **“Type 1 keeps history in audit columns.”** Last-modified metadata does not preserve prior values.
- **“Type 2 natural key is unique.”** Durable key repeats across versions; surrogate key is row-unique.
- **“Largest surrogate is current.”** Surrogate allocation need not follow effective time.
- **“Current flag alone defines history.”** Intervals and active policy must agree.
- **“Inclusive ends are intuitive.”** Shared boundary instants can match twice.
- **“Subtract one second from the end.”** Precision changes create gaps or overlaps.
- **“No overlap means complete history.”** Intervals can be disjoint and still have gaps.
- **“One matching row in sample data proves resolution.”** Every eligible fact and adversarial boundary needs testing.
- **“Load time is close enough to effective time.”** Late/out-of-order changes make them diverge.
- **“A record hash defines semantic equality.”** Canonical fields and serialization define what the hash represents.
- **“Any source field change creates a Type 2 row.”** Audit/noise fields can cause version explosion.
- **“A revert can reuse the old surrogate.”** A new interval is a new version even if attributes repeat.
- **“Type 2 is bitemporal.”** It usually preserves valid states, not every prior warehouse belief.
- **“Facts can join to durable key safely.”** Multiple versions fan out unless current/as-of logic restricts the path.
- **“Current reporting should reuse historical labels.”** Current and as-was perspectives require explicit paths.
- **“Inferred-member completion is a business change.”** It may only fill late descriptive detail.
- **“Source disappearance means delete.”** It may be extract failure or filtering.
- **“Closing a row erases the entity.”** Inactivity and legal erasure are different operations.
- **“Truncate/reload is harmless for dimensions.”** Regenerated surrogates invalidate facts.
- **“Expire then insert can be separate jobs.”** Consumers may observe zero or multiple current rows.
- **“Late changes only affect the dimension.”** Facts and aggregates in the corrected interval may require restatement.
- **“Type 6 current columns update themselves.”** Every historical row for the durable key must remain consistent.
- **“Type 7 dual keys remove ambiguity.”** Incorrect semantic relationships can still fan out.
- **“History can be added later.”** Destroyed prior values cannot be reconstructed without evidence.

## Worked Examples

### Example 1

A customer's email is corrected for a typographical error, while sales region changes on a known effective date. Treating both as Type 2 creates a false historical email version; treating both as Type 1 erases region history.

The attribute matrix applies audited Type 1 correction to email and Type 2 to region. The change reason distinguishes correction from business transition. A fact fixture around the region boundary verifies resolution.

### Example 2

Two customer versions use inclusive ends: North through March 1 and West beginning March 1. A sale at noon March 1 matches both under date-level comparison.

The model adopts half-open dates: North `[Jan 1,Mar 1)`, West `[Mar 1,infinity)`. If transition is intraday, it uses normalized timestamps rather than pretending the whole date is precise.

### Example 3

A March 1 region change arrives April 10 after an April 1 change is already recorded. A naive load expires the April row and makes the late region current.

The loader sorts by effective time and inserts the late version only for `[Mar 1,Apr 1)`. It preserves the April current row, re-resolves March facts under policy and records the late source sequence.

### Example 4

A fact arrives for a new supplier before the supplier extract. Dropping the fact understates purchases; mapping all missing suppliers to one unknown prevents later identity-specific repair.

The loader creates an inferred member for the supplier durable key with a stable surrogate and placeholder attributes. Arrival of details fills that member if effective semantics agree. Inferred age and amount are monitored.

### Example 5

Management wants revenue both under territory at sale time and under today's territory. A Type 2-only join supports the first but users manually join durable keys for the second and multiply rows.

The model implements a named Type 7 current path restricted to the unique current version. `territory_at_sale` uses fact surrogate; `current_territory` uses durable/current resolution. Grand totals reconcile while group distributions differ.

### Example 6

A customer dimension tracks a continuously changing risk score as Type 2, creating millions of versions and slow fact resolution.

The raw score becomes a time-stamped fact. A governed risk-band mini-dimension supplies analytical profiles where needed, and facts reference the applicable profile. Band/version ownership is explicit.

### Example 7

A Type 6 customer dimension updates `current_segment` on only the open version. Old surrogate rows retain stale current segments, so historical facts grouped by that column disagree.

The update runs atomically across every row sharing the durable key. A test asserts one distinct current-segment value per durable key and equality with the open version.

### Example 8

A source deletes a product ID from a daily snapshot. The warehouse closes the product immediately, but the absence was caused by a partial source export.

Deletion requires an authoritative tombstone or repeated complete-snapshot evidence under contract. Missing-extract health gates block publication. Inactivity is a Type 2 status only after valid evidence.

### Example 9

Two customer source IDs merge. Rewriting all historical facts to the surviving durable key changes audited customer counts and cohorts.

The warehouse retains original historical identities and records a merge/successor relationship. Current consolidated reporting follows the relationship through a separately governed path; as-was reporting remains stable.

### Example 10

A team rebuilds Type 2 history from source snapshots and assigns new surrogate sequences. The dimension looks correct, but existing facts now point to unrelated versions.

The rebuild reuses a durable version-mapping registry or atomically rebuilds and re-keys every dependent fact with full reconciliation. Key mappings, fact counts and historical group totals are acceptance gates.

## Cross-Program Connections

- [Database Engineering](../../18-database-engineering/ROADMAP.md): ranges, exclusion/temporal constraints, indexes and transactions support interval integrity.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md): durable identity and historical conformance coordinate dimensions across processes.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md): incremental merges, backfills and version growth affect scalable storage and computation.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): retention, erasure and attribute access constrain historical storage.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): ordering, retries, atomic publication and late messages shape SCD correctness.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md): change events need stable identity, effective time and deletion semantics.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): catalogs, semantic layers and quality gates expose safe historical/current paths.

## References

1. Kimball Group, [Type 1: Overwrite](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/type-1/). Defines current-value overwrite and its loss of history.
2. Kimball Group, [Type 2: Add New Row](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/type-2/). Defines new surrogate versions, effective/expiration timestamps and current indicators.
3. Kimball Group, [Type 4: Add Mini-Dimension](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/type-4-mini-dimension/). Describes separation of volatile profile attributes and dual fact keys.
4. Kimball Group, [Design Tip 152: Slowly Changing Dimension Types 0, 4, 5, 6 and 7](https://www.kimballgroup.com/2013/02/design-tip-152-slowly-changing-dimension-types-0-4-5-6-7/). Explains original-value, mini-dimension and current/historical hybrid techniques.
5. Microsoft, [Load Tables in a Dimensional Model](https://learn.microsoft.com/en-us/fabric/data-warehouse/dimensional-modeling-load-tables). Provides current SCD loading, inferred-member and surrogate-key guidance.
6. Microsoft, [Slowly Changing Dimension Type 2](https://learn.microsoft.com/en-us/fabric/data-factory/slowly-changing-dimension-type-two). Shows source, change detection and Type 2 version-row structure.
7. Microsoft, [Modeling Dimension Tables in Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/dimensional-modeling-dimension-tables). Describes surrogate keys and historical dimension attributes.
8. PostgreSQL Global Development Group, [Range Types](https://www.postgresql.org/docs/current/rangetypes.html). Defines half-open range semantics and exclusion constraints for nonoverlap.
9. PostgreSQL Global Development Group, [Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html). Documents unique, primary, foreign and temporal constraint behavior.

## Exercises

### Exercise 1

A customer dimension includes durable customer ID, legal name, corrected email, original acquisition channel, sales region, loyalty tier and continuously varying credit score. Choose and justify SCD behavior per attribute. Identify what should be modeled as a fact or mini-dimension instead.

### Exercise 2

For durable key `P7`, versions are `[Jan 1,Apr 1)` Basic, `[Apr 1,Jul 1)` Plus and `[Jul 1,infinity)` Premium. Resolve facts at Dec 31, Jan 1, Mar 31, Apr 1 and Jul 1. State results for gaps/boundaries and write interval/current invariants.

### Exercise 3

A change effective February 15 arrives May 10. Existing versions are `[Jan 1,Mar 1)` North and `[Mar 1,infinity)` West. Design the late-change update for value Central, including ambiguity policy, fact re-keying, atomicity and knowledge-as-of evidence.

### Exercise 4

Design Type 6 and Type 7 alternatives for reporting employee facts by department at event time and current department. Compare keys, updates, joins, invariants, storage and failure modes.

### Exercise 5

A warehouse currently overwrites product category (Type 1) but must introduce reproducible historical category reporting. Produce a migration and validation plan, including what cannot be recovered, how new facts resolve, dual-run semantics and consumer communication.

## Answers to the Exercises

### Answer 1

Durable customer ID is Type 0 identity under a no-reuse policy. Original acquisition channel is Type 0. A true typographical email correction is audited Type 1; if email history is analytically required, use Type 2 instead. Legal name needs policy: Type 1 for current/legal restatement or Type 2 for as-was regulated documents. Sales region is typically Type 2 because facts need historical attribution. Loyalty tier may be Type 2 or a mini-dimension/current hybrid if it changes frequently and both perspectives matter.

Continuously varying credit score is normally a time-stamped fact, not a Type 2 attribute. A governed score band can be part of a mini-dimension if profile analysis warrants it. The attribute matrix must specify authority, effective time, correction behavior and current/historical questions rather than copying these defaults blindly.

### Answer 2

December 31 before the first start has no match and must follow the explicit prehistory/unknown policy. January 1 and March 31 resolve Basic; April 1 resolves Plus because Basic excludes its end; July 1 resolves Premium because Plus excludes its end. Exact timezones/precision must match the interval contract.

Require unique surrogates, nonempty intervals, pairwise nonoverlap per `P7`, at most one current row, and exactly one current row for an active product. Eligible covered facts must match exactly one interval. If coverage is promised from January 1 onward, adjacent ends/starts must leave no gap, and the Premium row alone is open/current.

### Answer 3

The late Central value conflicts with already recorded boundaries unless its end is known. If evidence says Central was valid `[Feb 15,Mar 1)`, shorten North to `[Jan 1,Feb 15)`, insert Central for that interval and retain West from March 1. If evidence says Central continued beyond March 1, the May input conflicts with West history and must be resolved by source precedence/owner rather than arrival order.

Stage the complete proposed timeline, reject overlap/gap outside policy, allocate/reuse versions idempotently, and identify facts from February 15 to the selected end. Publish dimension edits and fact surrogate re-keying with transaction/snapshot atomicity, then rebuild affected aggregates and reconcile grand/group totals. Retain original system-load history or immutable change audit so reports can reproduce what was known before May 10.

### Answer 4

Type 6 stores a fact's historical surrogate and places both `department_at_event` plus `current_department` attributes on every Type 2 employee row. A current change inserts/expires historical versions as needed and overwrites `current_department` across all rows for the durable employee. It gives one dimension join but creates write amplification; assert one current value across all versions.

Type 7 stores/reaches both the fact-time surrogate and durable employee key. Historical join uses surrogate; current join filters durable key to the unique current version. It avoids rewriting all history but adds relationship/path complexity and risks fanout if the current predicate is absent. Both need distinct semantic names, one current row, stable durable identity, boundary fact tests and grand-total reconciliation. Choose based on semantic-tool support, update cost and path clarity.

### Answer 5

Type 1 overwrites destroyed old category values, so history cannot be recovered from the dimension alone. Inventory source snapshots, change logs, archived extracts and report outputs; declare periods/attributes with insufficient evidence rather than inventing versions. Build a new Type 2 product/category history with durable keys, stable surrogates, half-open intervals and provenance confidence.

From the cutover onward, resolve new facts to event-time versions. Backfill historical fact keys only where evidence yields exactly one version; classify unresolved periods. Publish `category_at_event` and `current_category` distinctly, dual-run old current-restated reports and new historical reports, reconcile fact populations/totals and explain expected group movement. Version contracts, obtain owner acceptance, preserve rollback mappings and communicate that pre-evidence historical results remain unavailable or approximate.
