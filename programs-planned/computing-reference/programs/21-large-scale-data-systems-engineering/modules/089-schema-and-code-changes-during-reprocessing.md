---
module_id: LSDS-089
program: Large-Scale Data Systems Engineering
level: 2
module_number: 89
title: Schema and Code Changes During Reprocessing
status: complete
last_verified: 2026-09-04
---

# Schema and Code Changes During Reprocessing

## One-Page Review

### Governing question

When historical data and persisted state were produced under older schemas and code, how can engineers replay them with an explicit, testable meaning—without confusing successful decoding with semantic compatibility or silently mixing versions in one result?

### Essential definitions

- A **writer schema** describes bytes as originally encoded; a **reader schema** interprets them now.
- **wire compatibility** means old bytes can be decoded under defined resolution rules.
- **state compatibility** means persisted operator state maps safely to the recovering code/topology/serializer.
- **semantic compatibility** means the new computation preserves the intended business meaning and observable contract.
- A **semantic version** identifies code, configuration, schemas, models, reference data, time rules, and nondeterministic inputs that determine results.
- A **migration** transforms stored data/state from one representation or meaning to another with lineage.
- A **reinterpretation** reads old facts under new rules and intentionally creates a new result version.
- A **historical replay** reproduces the old meaning using the old semantic bundle.
- **dual read/write** supports an overlap where old and new formats or outputs coexist.
- A **compatibility matrix** records supported writer→reader, state→code, and producer→consumer combinations.
- A **golden corpus** is versioned representative/adversarial historical data with expected decoded and computed results.

### Central model, mechanism, or theorem

For input bytes $x$ written with schema $S_w$, replay specification

$$R=(X,S_w,S_r,C,K,M,T,Q,O),$$

pins input snapshot $X$, reader schema $S_r$, code/config/dependency bundle $C$, state/key serializer bundle $K$, model/reference versions $M$, time/nondeterminism policy $T$, quality/equivalence contract $Q$, and output version $O$. Result is

$$y_O=f_{C,M,T}(resolve(x,S_w,S_r),state_K).$$

Successful `resolve` proves only wire readability. Publication additionally requires supported state mapping, explicit business-semantics choice, deterministic/captured dependencies, consumer/output compatibility, and validation against $Q$. If $f$, defaults, reference truth, key identity, or output meaning changes, write a distinct $O$ and compare/migrate; never overwrite history while labeling it equivalent.

### Critical invariants

- Original writer schema/field identities and semantic bundle remain discoverable for retained data.
- Reader-schema resolution is tested for every historical writer version in scope.
- Defaults, aliases, promotions, nullability, enums, logical types, and unknown fields have explicit meaning.
- Stable field IDs/numbers are never reused for different meanings; keys require stronger migration controls.
- Persisted state maps by stable operator/state identity and compatible serializer or explicit migration.
- Code, configuration, libraries, model, reference data, locale, time zone, clock, and seeds are pinned.
- Historical reproduction and new-rule reinterpretation use different run/output semantic identities.
- Mixed-version partitions/records are either supported by contract or rejected, never accidental.
- Side effects and transactional sinks use version-aware stable identities during replay.
- Rollback retains readable old state/output and avoids irreversible format publication until approved.

### Common failures

Common failures include assuming backward-compatible decoding preserves business meaning; applying a new default to old absent data as if producers supplied it; reusing deleted field numbers/IDs; changing a key schema and merging distinct keys; reading all history with one latest schema without writer metadata; restoring state under auto-generated operator IDs; changing serializer/library/runtime silently; replaying against current mutable dimensions; changing time zone, rounding, collation, null, lateness, or ordering rules; combining old and new code outputs under one version; comparing only row counts; overwriting production before consumers are compatible; and deleting the old bundle before rollback.

### Compact example

Two old records total 3,500 cents. Reader schema adds `region` with default `UNKNOWN`, so both decode: one region is defaulted and one is explicitly `EU`. New code adds 20% tax to EU records, producing 4,000 cents. Wire compatibility passed, but semantics changed by 500 cents. The result belongs in `orders_total/v2`, with the old 3,500-cent `v1` preserved until comparison, consumer validation, cutover, and rollback policy complete.

### Connections

[LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md) supplies versioned effect identity, [LSDS-071](071-table-snapshots-and-atomic-commit.md) supplies versioned publication, [LSDS-074](074-schema-evolution-at-scale.md) supplies field evolution, [LSDS-085](085-checkpoint-based-recovery.md) supplies state compatibility, [LSDS-086](086-exactly-once-state-updates.md) supplies transition identity, and [LSDS-088](088-backfill-isolation.md) supplies shadow replay/cutover.

## Governing Question

Historical bytes outlive the code that wrote them. Reprocessing months later may cross dozens of input schemas, serializer versions, planner/runtime releases, model revisions, reference snapshots, and bug fixes. “It deserialized” says little about whether the output means the same thing.

Sometimes the goal is reproduction: explain what version 1 computed then. Sometimes it is correction: apply version 2 rules to all retained history. Sometimes state must migrate in place so a live stream can continue. These are different operations with different output identities and evidence.

The governing question is how to inventory versions, resolve wire schemas, map persisted state, pin executable semantics, choose reproduction versus reinterpretation, validate differences, protect consumers/effects, publish conditionally, and retain rollback. Compatibility must be a matrix and an experiment, not a hopeful boolean.

## Why This Matters

Schema evolution mechanisms deliberately make some changes readable: adding a field with a default, preserving unknown fields, renaming through aliases, widening numeric types, or tracking stable field IDs. But readable values can still change behavior. `UNKNOWN` region may route to a different tax policy; `int` to `long` may expose overflow previously rejected; a timestamp logical type or time-zone change can move daily partitions.

Persisted state is even stricter. Key bytes define identity and partition ownership. Dropping a key field can collapse distinct entities. A new optimizer can produce a different state topology. Serializer compatibility may support values but not keys, timers, or operator mappings. Rebuilding from source may be safer than interpreting incompatible state.

Code changes include configuration, dependency and runtime behavior, model artifacts, reference tables, locale/collation, random seeds, and external lookups. Reproducibility needs the whole semantic bundle. Otherwise a replay becomes an undocumented new computation that can neither explain the past nor support trustworthy correction.

## Prerequisites and Retrieval

Review replay-safe effects in [LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md), table snapshots in [LSDS-071](071-table-snapshots-and-atomic-commit.md), schema evolution in [LSDS-074](074-schema-evolution-at-scale.md), checkpoint compatibility in [LSDS-085](085-checkpoint-based-recovery.md), exactly-once state in [LSDS-086](086-exactly-once-state-updates.md), and isolated backfills in [LSDS-088](088-backfill-isolation.md).

You should understand writer/reader schemas, tagged fields, defaults, aliases, type promotion, logical types, schema registries, serialization, state backends, operator/key identity, savepoints, immutable artifacts, semantic versioning, deterministic replay, golden/property/differential testing, table snapshots, and canary cutover.

For diagnosis retain input object/log snapshot and writer schema per record/file, reader/output/state/key schema IDs, code/image/config/dependency/runtime/planner/model/reference digests, operator/state IDs, serializers, time zone/locale/rounding/lateness/seed, replay intent, compatibility decisions, migration mappings, golden/differential results, output namespace/snapshot, consumer versions, publication base, and rollback assets.

## Learning Objectives

After this module, you should be able to:

1. distinguish wire, state, semantic, output, and consumer compatibility;
2. inventory writer schemas and complete semantic bundles across a replay range;
3. reason about defaults, aliases, promotions, nulls, enums, logical types, and field identity;
4. migrate value state while treating key/state/topology changes conservatively;
5. choose old-code reproduction, new-code reinterpretation, explicit migration, or dual running;
6. pin code, config, dependencies, models, reference data, and time/nondeterminism;
7. design compatibility matrices and golden/differential/metamorphic tests;
8. version outputs and effect identities when semantics change;
9. stage consumer-compatible publication with fencing and rollback; and
10. audit mixed-version data and reject unproven combinations.

## Core Exposition

### Declare replay intent

Write one sentence: reproduce `v1` invoices from the 2025 close, or recompute them under `v2` tax law. Reproduction uses the historical semantic bundle and expected historical quirks. Correction/interpretation uses new rules and must create explicit lineage/version, even when output schema is unchanged.

State migration changes representation while intending to preserve logical state. Dual/shadow running compares versions over an overlap. Never let a generic “backfill” flag conceal which operation is happening.

### Inventory every writer and state version

Scan file manifests, message headers/registry IDs, table metadata, checkpoints, and deployment records. Count bytes/records/partitions for each writer schema, code generation, state serializer, model/reference version, and exceptional/corrupt category.

Do not infer schema solely from a current table catalog or filename. Preserve original writer metadata and field IDs. Unknown or missing provenance is a blocking category requiring recovery, quarantine, or explicitly limited guarantees.

### Resolve writer and reader schemas

Schema resolution is directional. Test every retained $S_w\rightarrow S_r$ pair. Adding a reader field may require a default; removing a reader field may ignore old data; renames need aliases or stable IDs; numeric promotions have range/precision behavior; enum changes need fallback policy.

Defaults fill absence at read time; they do not prove the producer asserted the value. Preserve provenance such as `region_source=defaulted_v2` when business logic distinguishes unknown from explicit. Test nested records, arrays/maps, unions, logical types, nulls, malformed bytes, and unknown fields.

### Preserve field identity

Names are mutable labels. Formats with field IDs or tag numbers use them as durable identity; never reuse a removed ID for a new meaning. A rename preserves identity only through supported mapping. Copy-by-position or name-only projection can silently swap fields after reorder/rename.

Output fields also need stable meaning. Reusing `total` after changing currency, tax inclusion, rounding, or unit is a semantic break even if type remains decimal.

### Treat keys as a separate migration

Key schema determines equality, partitioning, state address, deduplication, and effect identity. Removing or normalizing a key field may collapse entities; changing serialization may route the same entity to another partition. Generic value-schema compatibility does not prove key compatibility.

Build an explicit old-key→new-key mapping, detect collisions/splits, define merge semantics, repartition state/data, and reconcile counts/content. When safe mapping cannot be proven, rebuild new state from immutable inputs in a separate namespace.

### Map persisted operator state

Record stable operator UIDs, state names/types, serializers/snapshots, key-group mapping, timers, topology, and runtime version. On restore, each old state object must map exactly once to a compatible new owner or be explicitly migrated/discarded with business approval.

Auto-generated topology-position IDs are brittle. Value serializer migration may be supported while key evolution is not. Query/planner changes can alter optimized topology even when SQL looks similar. Test actual savepoint/checkpoint restoration with production-shaped state.

### Pin the executable semantic bundle

Use immutable code/image and dependency lock digests, runtime/JVM/interpreter/planner version, configuration and feature flags, UDFs, models, reference snapshots, locale, time zone, calendar, rounding, collation, seeds, and external lookup policy.

Build reproducibly and verify artifact availability before scheduling history. “Same Git commit” is insufficient if dependencies float or runtime configuration differs. Capture nondeterministic values or use versioned inputs.

### Classify code changes

Classify changes as representation-only, bug correction, new business policy, performance-only, output-contract change, or nondeterminism removal. Then write expected invariants and expected differences. An optimizer change intended as performance-only should preserve a defined result equivalence; floating-point order may require tolerance rather than bit equality.

Review filters, joins, null handling, aggregation order, rounding, watermark/lateness, dedup horizons, default values, and side effects. Tiny source diffs can change historical inclusion broadly.

### Build a compatibility matrix

Rows include every writer/state/code version; columns include candidate reader/code/output/consumer versions. Record supported, migratable, rebuild-required, quarantined, or unsupported with evidence/tool version. Include forward, backward, mixed, rollback, and replay paths.

A registry's compatibility setting is one input, not the whole matrix. It generally cannot reason about business calculations, state keys, query plans, external consumers, or historical reference data.

### Test with historical and generated data

Golden corpus covers every writer version plus missing/defaulted fields, renamed aliases, extremes, decimals, time zones/DST, nulls, enums, corrupt data, late/deleted records, and known incidents. Decode with old/new readers and run old/new code.

Use differential tests to classify output deltas, property tests for schema/state invariants, metamorphic tests for reorder/partition/retry invariance, and restore tests for state compatibility. Scale tests validate memory, skew, migration duration, and output layout.

### Version outputs and effects

Semantic change writes a new dataset/table branch/topic/view/model feature version or calculation version. Each record carries input lineage and semantic bundle digest where practical. Consumers select intentionally; mixed versions are queryable only if the contract defines reconciliation.

Effect/idempotency keys include semantic operation version when corrected effects are genuinely new; otherwise replay uses original keys to suppress duplicates. Compensation is a new auditable action, not silent overwrite.

### Choose migration topology

Offline conversion reads old snapshots and writes new-format state/output before cutover. On-read migration reduces bulk work but creates mixed latency and rollback complexity. Dual read/write supports gradual consumer migration but doubles paths and requires reconciliation. Rebuild-from-source is clearest when retained inputs and RTO allow it.

For live state, stop-with-savepoint/in-place restore minimizes duplicate running jobs but has cutover risk. Shadow rebuild keeps old live service while warming new state, then fences and switches at a defined frontier.

### Publish and roll back safely

Backfill writes isolated candidate output. Validate full interval coverage, schema/identity, old-versus-new expected differences, business invariants, consumers, and performance. Conditional publication checks the live base and approved semantic digest.

Retain old outputs/state/code/schema/reference snapshots through observation. Rollback readers and execution consistently; do not point old code at newly irreversible state. New downstream effects after cutover need a forward-fix/compensation plan.

### Observe and govern drift

Measure records/bytes by writer/reader/schema/code version; decode/default/alias/promotion/unknown/corrupt counts; state migration and key collisions; differential output classes; restore failures; candidate coverage; consumer errors; and publication/rollback outcomes.

Alert on unknown schema IDs, unapproved mixed versions, default spikes, digest drift, mutable reference reads, missing old artifacts, and output without semantic version. Audit approvals and retain compatibility evidence with the published snapshot.

## Definitions and Notation

Let:

- $x$ be bytes written under $S_w$ and interpreted under $S_r$;
- $resolve(x,S_w,S_r)$ be directional schema resolution;
- $C,K,M,T$ be code/config/dependency, state/key, model/reference, and time/nondeterminism bundles;
- $R=(X,S_w,S_r,C,K,M,T,Q,O)$ be replay specification;
- $f_{C,M,T}$ be transformation semantics;
- $y_O$ be output under semantic version $O$;
- $W$ be historical writer versions and $A\subseteq W$ accepted by the candidate;
- $\Delta(y_1,y_2)$ be classified differential results;
- $D$ be defaulted-field count and $U$ unknown/incompatible count;
- $v_0,v_1$ be old and candidate publication versions.

Coverage requires $A=W$ for the declared scope or explicit quarantine/exclusion. `resolve` success is not $\Delta=0$. Result equality must state bitwise, exact logical, set/multiset, ordered, aggregate, or tolerance relation. Default/promotion counts need records as denominator.

## Mechanisms, Invariants, or Proof Structure

### Decode-safety argument

For every writer version in scope, run the specified directional resolution and validate values/provenance under edge cases. If all succeed, candidate can decode the declared bytes. This proves representation readability only, not computation or business equivalence.

### Reproduction argument

Pin original $S_r,C,K,M,T$ and immutable $X$, capture nondeterminism, and execute deterministically. Under equivalent runtime behavior and complete artifacts, replay reconstructs historical $y_O$. Golden/differential checks test the premises; unavailable mutable dependencies weaken the claim explicitly.

### Migration-preservation argument

Define mapping $m:S_{old}\rightarrow S_{new}$ and invariant/equivalence $Q$. Prove identity/collision handling, transform every state/output item once, and validate $Q(old,m(old))$. Atomic versioned publication prevents partial interpretation; failed migration retains old version.

### Semantic-change argument

If $f_{old}\ne f_{new}$ for any accepted input, outputs have different semantic identities even when schemas match. Versioned shadow output plus classified $\Delta$ makes the change observable and prevents silent substitution. Approval selects which version becomes current.

### Adversarial verification

Test every writer version, missing/default/alias/unknown fields, reused IDs, numeric/decimal/time extremes, null/enums, corrupt bytes, key collisions, state/timer/topology changes, dependency/runtime drift, mutable references, nondeterminism, mixed partitions, consumer skew, effect replay, cutover race, rollback, and missing old artifacts.

## Alternatives and Trade-Offs

| Strategy | Strength | Cost or risk |
|---|---|---|
| Replay old bundle | Best historical reproduction | Old artifacts/vulnerabilities/dependencies must remain runnable |
| New reader with old business logic | Format modernization | Defaults/resolution can still change values |
| Explicit offline migration | Auditable, atomic new representation | Extra storage/time and migration code |
| On-read/lazy migration | Spreads cost | Mixed versions, latency tails, harder rollback |
| Dual read/write | Gradual consumer transition | Double complexity and reconciliation |
| Rebuild state from source | Avoids unsafe state mapping | Requires retained inputs, determinism, and time/capacity |
| Shadow new semantics | Strong comparison and rollback | Extra compute/storage and publication workflow |

Select separately for input decoding, persisted state, output, and consumers. One compatibility mode rarely fits all four.

## Failure Modes and Misconceptions

1. **Readable equals equivalent.** Wire success says nothing about business results.
2. **Default equals historical fact.** The producer never supplied it.
3. **Field number/ID reuse.** Old bytes acquire a new meaning.
4. **Name-only identity.** Rename/reorder maps the wrong field.
5. **Key treated as value.** Distinct entities collide or repartition silently.
6. **Latest schema for all history.** Original writer context disappears.
7. **Auto-generated state IDs.** Topology changes orphan or misassign state.
8. **Pinned code only.** Config, libraries, model, reference, and runtime drift.
9. **Current lookup during replay.** Historical computation becomes irreproducible.
10. **Unversioned corrected output.** Consumers cannot distinguish meanings.
11. **Count-only diff.** Key/value/order/timing changes remain hidden.
12. **Mixed candidate versions.** Retries silently combine semantic bundles.
13. **Registry setting as proof.** State, logic, consumers, and effects are untested.
14. **Irreversible early cutover.** Old code/state/output cannot resume.
15. **External effects ignored.** New rules repeat or conflict with prior actions.

## Worked Examples

### Example 1

Adding optional `region` with default `UNKNOWN` decodes old records, but tax logic must distinguish defaulted from explicitly supplied region.

### Example 2

Renaming `customer_id` preserves stable field ID/alias; dropping and recreating a same-named field with a new ID is a different field.

### Example 3

Widening integer to long is wire-compatible, yet downstream code casting back to integer can still overflow.

### Example 4

Dropping one key component collapses two historical keys. Value migration cannot decide how to merge balances without a business rule.

### Example 5

A SQL text change is small, but a new planner reorders joins and changes state topology; actual savepoint restore test fails before cutover.

### Example 6

Same commit with a floating dependency selects a newer time-zone database and moves records across daily boundaries.

### Example 7

Old and new totals differ by exactly the classified tax-rule change; unexplained key-set differences still block publication.

### Example 8

A shadow state rebuild consumes history to frontier 500, then live catch-up reaches 540 before a fenced switch.

### Example 9

An email correction is a new versioned effect; replaying the original welcome-email key remains deduplicated.

### Example 10

The executable fixture demonstrates wire-compatible defaulting plus an intentional semantic difference.

<!-- bijux-verify: {"id":"schema-code-replay","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"decoded=2\ndefaulted_region=1\nold_total_cents=3500\nnew_total_cents=4000\nsemantic_change=true\npublish_namespace=orders_total/v2\n","stderr":""}} -->
```python
written = [
    {"id": 1, "amount_cents": 1000},
    {"id": 2, "amount_cents": 2500, "region": "EU"},
]
decoded = []
defaulted = 0
for record in written:
    current = dict(record)
    if "region" not in current:
        current["region"] = "UNKNOWN"
        defaulted += 1
    decoded.append(current)

old_total = sum(record["amount_cents"] for record in decoded)
new_total = sum(
    record["amount_cents"] * (120 if record["region"] == "EU" else 100) // 100
    for record in decoded
)
print(f"decoded={len(decoded)}")
print(f"defaulted_region={defaulted}")
print(f"old_total_cents={old_total}")
print(f"new_total_cents={new_total}")
print(f"semantic_change={str(old_total != new_total).lower()}")
print("publish_namespace=orders_total/v2")
```

## Cross-Program Connections

- **Schema engineering:** writer/reader resolution, field identities, logical types, defaults, and compatibility registries govern bytes.
- **Distributed systems:** state identity, checkpoints, fencing, deterministic replay, and atomic publication govern execution.
- **Programming languages:** dependency resolution, runtime behavior, serialization, numeric semantics, and reproducible builds define code meaning.
- **Databases:** migrations, MVCC snapshots, constraints, transaction logs, and rollback preserve versioned truth.
- **Streaming:** keys, watermarks, timers, late data, state topology, and source frontiers complicate change.
- **ML systems:** model artifacts, features, reference sets, and stochastic seeds are semantic dependencies.
- **API engineering:** consumer compatibility and versioned idempotency/effect contracts bound external behavior.
- **Governance:** lineage, approval, audit, retention, and explainability distinguish reproduction from correction.

## References

1. Apache Avro, [Specification](https://avro.apache.org/docs/current/specification/). Current. Defines writer/reader schema resolution, defaults, aliases, promotions, and canonical forms.
2. Protocol Buffers, [Proto3 Language Guide](https://protobuf.dev/programming-guides/proto3/). Current. Documents safe message evolution, tag-number reservation, unknown fields, and wire constraints.
3. Apache Iceberg, [Schemas](https://iceberg.apache.org/docs/latest/schemas/). Current. Describes stable never-reused field IDs.
4. Apache Iceberg, [Table Specification](https://iceberg.apache.org/spec/). Current. Defines schema IDs, evolution, promotion, and metadata semantics.
5. Apache Flink, [State Schema Evolution](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/serialization/schema_evolution/). Current. Documents serializer migration support and key/Kryo limitations.
6. Apache Flink, [Upgrading Applications and Flink Versions](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/upgrading/). Current. Documents operator identity, topology/state compatibility, and upgrade paths.
7. Apache Flink, [Savepoints](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/savepoints/). Current. Documents stateful updates, operator IDs, ownership, and restore behavior.
8. Apache Flink, [Table and SQL Concepts](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/concepts/overview/). Current. Discusses planner topology and stateful evolution constraints.
9. Apache Beam, [Schemas](https://beam.apache.org/documentation/programming-guide/#schemas). Current. Documents schema fields, inference, and transformations.
10. Apache Spark, [Structured Streaming Programming Guide](https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html). Current. Documents state/checkpoint compatibility constraints and schema handling.
11. Apache Parquet, [Logical Types](https://parquet.apache.org/docs/file-format/types/logicaltypes/). Current. Defines logical annotations and compatibility constraints over physical types.
12. Apache Airflow, [Backfill](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/backfill.html). Current. Documents historical run intervals, version choice, reprocessing behavior, and concurrency.

## Exercises

### Exercise 1

Build a compatibility matrix for three writer schemas, two reader/code versions, persisted keyed state, and two consumer versions.

### Exercise 2

Explain why adding a field with a default can be wire-compatible but semantically incompatible during historical replay.

### Exercise 3

Design a migration that changes account key from `(tenant,legacy_id)` to `(tenant,canonical_id)` where several legacy IDs may merge.

### Exercise 4

Design a reproducible golden/differential test suite for a time-zone, rounding, model, and reference-data code change.

### Exercise 5

Plan a shadow state rebuild and cutover that preserves old-version rollback and prevents duplicate external effects.

## Answers to the Exercises

### Answer 1

Rows enumerate every writer schema and state serializer/operator/key topology; columns enumerate reader/code/output and consumer versions. For each pair record decode outcome, defaults/aliases/promotions, state mapping or rebuild requirement, semantic equivalence/change, output readability, rollback, test corpus, tool/runtime version, and owner. Mark supported, migratable, rebuild-required, quarantined, or unsupported. Include mixed historical files, forward/backward consumer reads, and old-code rollback against retained output/state.

### Answer 2

The reader can synthesize the field for old bytes, so decoding succeeds. The producer did not assert that value; new code may filter, tax, join, group, or route on it. Different defaults or “absent versus explicit” handling can therefore change results. Track default provenance, define historical meaning, compare old/new computation, and assign a new semantic output version when behavior changes.

### Answer 3

Pin an authoritative versioned mapping from each legacy key to canonical key; detect missing, split, and many-to-one cases. Define business merge order/algebra for balances, timers, dedup history, and effects, with reconciliation invariants. Repartition into a separate new-key state namespace, validate every old key consumed once and totals/content preserved under the merge rule, then fence old writers and conditionally switch. Retain old state/source/mapping/code for rollback; never let a generic serializer migration guess collisions.

### Answer 4

Include records around DST transitions, all zones, rounding half/ties/extremes, null/default fields, every writer schema, each model class/threshold edge, missing/changed reference keys, and known incidents. Pin time-zone database, locale, numeric library, model and reference snapshots. Run old/new bundles, compare exact keys and classified value/timestamp differences, use metamorphic partition/reorder/retry tests, and fail on unclassified deltas. Scale-test state/output layout and archive corpus plus expected results/digests.

### Answer 5

Create a new manifest/output/state/checkpoint/consumer namespace and remove live-effect authority. Rebuild pinned history under the candidate bundle, then catch up to a declared source frontier while old live continues. Differentially validate state/output and rehearse consumers. Fence old/candidate writers, atomically switch reader and processing ownership at the frontier, and preserve old snapshot/savepoint/code/schemas/references. Version effect keys so original effects deduplicate and intentional corrections are explicit; rollback uses a conditional pointer/execution switch with post-cutover effects reconciled.
