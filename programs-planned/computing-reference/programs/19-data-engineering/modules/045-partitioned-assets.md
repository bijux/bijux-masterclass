---
module_id: DE-045
program: Data Engineering
level: 1
module_number: 45
title: Partitioned Assets
status: complete
last_verified: 2026-09-03
---

# Partitioned Assets

## One-Page Review

### Governing question

How should a data product divide its logical obligation into stable partitions so each partition has unambiguous membership, dependency mapping, completeness, generation, publication, and lifecycle semantics while the whole asset remains queryable and operable?

### Essential definitions

- A **data asset** is a durable governed data product with stable identity, owner, contract, lineage, and accepted materializations.
- An **asset partition** is one logical slice of an asset's obligation under a versioned partition definition; it is not merely a directory, file, table partition, or task.
- A **partition dimension** is one named axis such as business date, region, tenant, source, or bucket.
- A **partition key** is the canonical identity of one point/cell in the partition space, encoded reversibly and unambiguously.
- A **partition definition** declares dimension domains, key encoding, membership, intervals/calendars, start/end/dynamic rules, null/invalid policy, and version.
- A **partition inventory** is the authoritative expected set and state of keys for a bounded asset horizon.
- A **partition mapping** maps one downstream partition to the exact set of required upstream partitions or generation selections.
- A **partition generation** is one immutable accepted materialization of one logical asset partition, bound to inputs, code/schema/policy, manifest, and quality evidence.
- A **valid-empty partition** is complete evidence that the partition contains zero qualifying occurrences; it differs from missing, skipped, blocked, or unknown.
- **Partition pruning** eliminates physical data whose trusted partition metadata proves it cannot satisfy a predicate.
- **Partition evolution** changes a partition specification while preserving the ability to interpret existing data and distinguish old/new layouts.
- A **multi-dimensional partition space** combines named dimensions, often as a Cartesian product or an explicitly constrained subset.

### Central model, mechanism, or theorem

For asset $A$ with versioned logical population $D_A$ and total membership function

$$
p_s:D_A\rightarrow K_s,
$$

partition $k$ owns occurrence bag $P_k=\{x\in D_A:p_s(x)=k\}$. Correctness over an intended key set $E\subseteq K_s$ requires disjoint coverage

$$
\biguplus_{k\in E}P_k=D_A|_E.
$$

For downstream partition $d$, dependency mapping $M_{u\rightarrow v}(d)$ returns exact upstream keys. Readiness is

$$
ready(d)=\bigwedge_{u\in parents(v)}\bigwedge_{k\in M_{u\rightarrow v}(d)} accepted(u,k,g_{u,k}),
$$

under schema, quality, freshness, and generation-compatibility rules. The downstream manifest binds those generations. Missing mapped input blocks; an accepted zero-row manifest satisfies readiness when emptiness is valid. Physical layout and execution shards may differ from the logical partition space, but every accepted generation retains their relationship.

### Critical invariants

- Asset identity, partition-spec version, dimension names/order/domains, key encoding, membership function, calendar/time zone, null/error behavior, and effective range are explicit.
- Partition keys are stable, canonical, reversible, type-safe, tenant-scoped where required, and never inferred solely from paths.
- The bounded expected inventory distinguishes expected, not-yet-eligible, ready, materializing, accepted, valid-empty, missing, blocked, failed, quarantined, skipped, superseded, expired, and retired.
- Logical asset partitions, source/input partitions, execution tasks/shards, physical table/file partitions, and query predicates remain distinct.
- Every occurrence belongs to exactly one logical partition for a given spec, or to a declared quarantine/exclusion outcome with conservation evidence.
- Every downstream partition maps to a complete and minimal exact set of upstream partition generations, including window context, broadcasts, and many-to-one relations.
- A valid-empty partition has the same manifest and acceptance evidence as nonempty output except for zero counts; absence is never silently interpreted as empty.
- Retries and overlapping attempts create candidates; one validated generation is accepted through idempotent, fenced publication.
- Query pruning is an optimization derived from trusted metadata, not a substitute for row-level correctness or access control.
- Partition count, cardinality, skew, small files, metadata load, scan pruning, scheduling fan-out, and repair time fit measured operating envelopes.
- Evolution preserves old partition interpretation and makes spec transitions, rewritten data, and mixed-layout scans observable.
- Retention, deletion, legal hold, correction, and retirement act on logical obligations and accepted generations, not only storage prefixes.

### Common failures

Using directory names as the only partition registry; encoding keys with an ambiguous delimiter; treating local day as UTC day; using ingestion date for event-time ownership; creating one partition per user; taking an unconstrained cross product of tenants, dates, regions, and versions; confusing physical file partitions with logical data obligations; using mutable “latest” inputs; mapping daily output to only one hourly input; forgetting lookback context; counting upstream messages instead of resolving keys; treating missing as empty; triggering downstream from task success before partition publication; overwriting one shared path from retries; assuming pruning proves row membership; trusting user-supplied partition filters for authorization; changing bucket/hash/calendar rules under the same spec; dropping old physical partitions before consumers or legal policy permit; and launching an unbounded repair for every missing cell.

### Compact example

A sales asset has date × region keys for two dates and two regions: four expected partitions. Each downstream key requires same-date/same-region orders plus same-date exchange rates. Orders exist for three cells; rates exist for both dates. Three sales partitions are ready, including one whose accepted orders generation has zero rows. The fourth is blocked by missing orders. A date predicate prunes the logical inventory to two keys, but only one is ready. Reversing input-record order produces the same canonical mappings. **Conclusion:** partition identity, readiness, emptiness, and pruning are separate claims derived from declared metadata.

### Connections

[DE-034](034-partitioned-processing.md) distinguishes input, execution, and physical output partitioning. [DE-041](041-directed-acyclic-graphs-and-dependencies.md) introduces edge mappings; [DE-042](042-tasks-jobs-assets-and-datasets.md) defines assets and generations; [DE-043](043-scheduling-and-event-triggered-execution.md) creates partition-keyed intent; [DE-044](044-retries-timeouts-and-idempotency.md) protects attempts/publication. This module makes the logical asset partition contract explicit; DE-046 next plans controlled historical materialization.

## Governing Question

For a governed data asset, what exactly does one partition key mean, which occurrences and dependencies does it own, what evidence makes it complete, how is one generation accepted, and how can definitions and physical layouts evolve without changing historical meaning invisibly?

Partitioning solves several different problems. Logical partitions divide data-product obligations into independently addressable slices. Execution partitions divide work across tasks. Physical partitions and files influence storage, pruning, and lifecycle. Source-system partitions may reflect broker shards or database ranges. These shapes can align, but correctness never follows merely because they share the word “partition.”

An asset partition is valuable because it gives the system a stable unit for scheduling, retry, lineage, freshness, quality, correction, backfill, retention, and consumer communication. “Sales for Europe on 2026-09-01 under calendar/spec v3” is a domain obligation. It can be computed with 20 tasks, stored in 6 files, and read through a table snapshot. Those mechanics do not change its identity.

The partition definition must answer both set membership and operational expectation. Which date role owns a record? Are interval ends half-open? Which time zone/calendar defines a day? Which tenants or regions exist on a date? Is an empty result a valid complete materialization? Which hourly parents feed one daily child? Which old partitions remain queryable after the definition evolves? Without these answers, a grid in an orchestrator UI can look complete while data is omitted or duplicated.

The governing design goal is therefore not maximum parallelism or maximum pruning. It is a stable semantic index over a product's obligations, with physical and operational choices attached but not conflated.

## Why This Matters

Partition identity controls correctness. If one producer assigns a midnight occurrence to the prior UTC day and another uses tenant-local date, a union can duplicate or omit boundary records. If ranges use inclusive endpoints on both sides, the boundary belongs twice; if both exclude it, it disappears. Such defects often survive aggregate checks because counts can coincidentally balance.

Dependency mappings determine readiness. A daily aggregate commonly requires 24 hourly parents, but daylight-saving civil days may contain 23 or 25 hourly instants. A seven-day metric needs context before its output date. A regional fact may depend on one global rates partition broadcast to every region. A scheduler arrow does not encode those sets. The downstream partition manifest must resolve exact accepted upstream generations.

Missing and empty are operational opposites. An accepted zero-row partition proves the source scope was evaluated and no records qualified under its contract. A missing partition may mean not due, lost trigger, unavailable source, failed computation, intentionally skipped scope, deleted evidence, or registry error. Treating absence as empty quietly publishes incomplete datasets; treating every empty partition as missing causes endless retries and false incidents.

Partition count can move cost from data scan to metadata/control planes. One partition per customer per hour may create millions of cells, tasks, catalog entries, files, checks, and alerts. Even if each query prunes perfectly, listing and planning can dominate. Conversely, one yearly partition prevents efficient repair and pruning. Cardinality, data size, skew, consumer predicates, lateness, and operational recovery all influence granularity.

Physical partitioning is not a free indexing mechanism. High-cardinality columns create many small directories/files. Low-cardinality or skewed values create hot partitions. Queries may not use the partition predicate. Some table formats support hidden transforms and mixed partition specifications; others expose directory values directly. The logical asset contract should survive a change from daily files to monthly physical layout or from identity date to month transform.

Evolution makes historical semantics visible. Adding a region, changing a hash bucket count, adopting a fiscal calendar, or replacing UTC dates with business dates can reassign occurrences. A silent in-place change causes the same key to mean different populations across time. Versioned specs, effective ranges, migration mappings, and explicit correction/rebuild plans prevent this ambiguity.

Partition state is also governance data. Keys can reveal tenants, jurisdictions, investigations, or medical cohorts. A partition filter can become an authorization boundary only when enforced by trusted policy; directory hiding or query pruning does not provide access control. Retention and deletion must account for manifests, candidates, snapshots, receipts, caches, and downstream derivatives, not merely drop one folder.

## Prerequisites and Retrieval

Retrieve [Schemas, Nullability, and Type Fidelity](008-schemas-nullability-and-type-fidelity.md), [Time, Time Zones, and Event Timestamps](009-time-time-zones-and-event-timestamps.md), [Grain and the Meaning of a Row](011-grain-and-the-meaning-of-a-row.md), [Watermarks and High-Water Marks](022-watermarks-and-high-water-marks.md), [Partitioned Processing](034-partitioned-processing.md), [Late Corrections and Restatement](038-late-corrections-and-restatement.md), and modules [DE-041](041-directed-acyclic-graphs-and-dependencies.md) through [DE-044](044-retries-timeouts-and-idempotency.md).

Retrieve the asset contract: stable asset identifier; owner and consumers; row/event grain; source-of-truth population; completeness and freshness objectives; schema and semantic versions; accepted empty behavior; late/correction rules; query patterns; privacy/security classification; retention/deletion/legal-hold requirements; and recovery objectives.

Retrieve the logical partition definition: dimensions and types; static/dynamic/time/range/hash domains; dimension order; canonical key encoding/escaping; membership function; event/processing/business-time role; interval boundaries; calendar/time zone/tzdb assumptions; dynamic-key authority; start/end horizon; exclusions; null/invalid/out-of-range behavior; expected-inventory generator; spec version; effective range; and migration rule.

Retrieve dependency mappings: upstream/downstream asset/spec versions; same-key, offset, window, fan-in, fan-out, broadcast, aggregation, split, and custom mappings; exact accepted generation lookup; optional/required inputs; lookback/lookahead; schema/quality/freshness compatibility; valid-empty behavior; missing/blocked policy; and lineage evidence. Test mappings at month/year/leap/daylight-saving/calendar boundaries.

Retrieve operational state: intended keys; eligibility; scheduling/run requests; attempts; candidate and accepted generations; manifests; row/byte/file counts; quality results; freshness; blocked reasons; missing upstreams; retries; supersession; corrections; backfill selection; incidents; manual overrides; and consumer acknowledgements. Inventory sources must be authoritative enough to distinguish absent state from stale UI/cache.

Retrieve physical layout: table-format/catalog version; partition transforms and spec IDs; directory conventions; file/object manifests and checksums; clustering/sorting; bucket/hash algorithm; file size/count; statistics; pruning behavior; snapshot isolation; commit/pointer semantics; compaction; schema/partition evolution; metadata retention; object consistency; and reader compatibility. Reproduce engine-version-specific behavior rather than assuming similar SQL syntax means the same thing.

Retrieve scale evidence: key cardinality by dimension/time; active horizon; sparse/dense cells; row/byte distributions; skew and hot keys; small files; catalog/listing latency; planning time; scheduler/UI limits; task startup; check/lineage event volume; concurrency; query predicate distribution; bytes pruned/scanned; partition repair duration; and cost. Estimate both expected and pathological Cartesian products.

Before implementation, complete a partition contract:

| Concern | Required decision and evidence |
|---|---|
| Asset | Stable identity, owner, grain, schema, consumers, service objective |
| Logical space | Dimensions, domains, types, exclusions, expected-set generator |
| Membership | Source fields, transform/version, interval/calendar/null/error rules |
| Key | Canonical encoding, parse, ordering, namespace, collision/escape policy |
| Mapping | Each downstream key to exact required upstream keys/generations |
| State | Expected, ready, accepted, empty, missing, blocked, failed, retired semantics |
| Generation | Inputs, code/schema/config, manifest, controls, publication identity |
| Physical shape | Table spec, paths/files, transforms, clustering, compaction, pruning |
| Evolution | Spec IDs, effective bounds, old readers/data, migration and rollback |
| Operations | Scheduling, retries, repair/backfill, capacity, reconciliation, evidence |
| Governance | Tenant authorization, retention, deletion, legal hold, audit |

## Learning Objectives

After completing this module, you should be able to:

1. distinguish logical asset, source, execution, storage, and query partitioning;
2. define static, dynamic, temporal, range, hash/bucket, and multi-dimensional partition spaces;
3. design canonical typed keys and versioned membership rules with complete boundary behavior;
4. generate and reconcile bounded expected partition inventories without materializing unsafe Cartesian products;
5. specify same-key, offset, window, aggregation, broadcast, split, and custom dependency mappings;
6. distinguish accepted empty, missing, not-yet-eligible, blocked, failed, skipped, superseded, expired, and retired partitions;
7. bind exact input generations and publish one immutable validated generation per logical partition revision;
8. align logical partitions with physical layout, pruning, file sizing, skew, compaction, and metadata limits;
9. evolve partition specifications and lifecycle policy without silently reassigning historical meaning; and
10. test, observe, secure, reconcile, repair, and decommission partitioned assets at realistic scale.

## Core Exposition

### Begin with the asset obligation

Define the asset independently of how it runs or where it is stored. Record its stable identity, grain, population, owner, schema/semantic contract, service objective, consumer uses, and accepted-generation boundary. Then ask which subsets can be owned, validated, corrected, and consumed independently.

A useful partition often follows a dominant domain boundary: business day, accounting period, region, tenant cohort, source shard, or a bounded hash range. It should be small enough for isolated retry and freshness, yet large enough to avoid metadata/task/file explosion. The right boundary comes from semantics and operating evidence, not available CPU count.

Do not partition merely because a field exists. Customer ID may be a frequent filter but one logical partition per customer can be infeasible and can expose tenant identifiers. A stable bucket dimension may support execution/storage distribution while customer remains a row-level and authorization key. Logical and physical decisions can differ.

State the acceptance unit. If consumers can safely read each daily-region cell independently, it can be one partition generation. If four regional cells must reconcile to one global ledger before visibility, the accepted asset boundary may be the whole day even if compute and storage are region-sharded. Partitioning must not violate cross-cell invariants.

### Define the partition space

Common definitions include:

- **static:** a governed finite set such as `us`, `eu`, `jp`; additions/removals are catalog changes;
- **dynamic:** keys registered by an authoritative process at runtime, with lifecycle and approval rather than arbitrary task strings;
- **time-window:** half-open intervals generated from an anchor, cadence, time zone, and calendar;
- **integer/range:** typed half-open ranges with bounds and out-of-range policy;
- **hash/bucket:** canonical entity bytes mapped by a named stable algorithm and modulus/spec;
- **multi-dimensional:** cells combining dimensions, usually a product or constrained relation; and
- **irregular/domain calendar:** fiscal periods, market sessions, releases, campaigns, or source delivery IDs from a versioned registry.

For multiple dimensions $D_1,\ldots,D_m$, the naive space is $K=D_1\times\cdots\times D_m$ with size $|K|=\prod_i|D_i|$. This may be wrong when not every tenant exists in every region/date or when regions become effective at different times. Define an eligibility relation $R\subseteq K$ or generate expected keys from authoritative membership/effective-dating state.

Keep the horizon bounded. A time definition may be conceptually open-ended, but inventory queries and scheduler expansion use explicit start/end. Dynamic partitions need authority, deduplication, validation, removal/tombstone policy, and reconciliation against their source registry.

### Make keys canonical and typed

A partition key is an identity, not display text. Encode dimension names or use a schema whose fixed order is versioned. Escape separators and reserved characters. Canonicalize dates, integers, enums, Unicode, case, and percent/URL encoding deliberately. Parse must be the inverse of encode for every valid key.

The string `2026-09-01|eu` is acceptable only if neither field can contain unescaped `|`, dimension order is known, and date/region types are validated. JSON can be canonicalized but ordinary object serialization may reorder fields or vary whitespace. A structured database key avoids string ambiguity while UIs can render a stable external form.

Namespace keys by asset and partition-spec version where global collision matters. Do not include attempt ID in the logical key. A correction can create a new generation of the same partition key because partition identity names scope, while generation identity names accepted content/lineage.

Ordering is separate from identity. Lexical date order works only for canonical fixed-width forms. Region enum order may be display policy, not semantics. Hash buckets have no domain ordering. Never infer source causality or latest generation from partition-key sort order.

### Specify membership and boundary rules

For every valid occurrence, membership must be deterministic under the chosen spec. Name the source field and its semantic role. Event time, transaction-effective date, ingestion time, and processing time answer different questions. If fallback is allowed when event time is absent, label and count it; do not silently mix time roles.

Use half-open ranges $[a,b)$ so adjacent boundaries meet without overlap. Declare timestamp precision and normalization. A local civil day is generated in a named time zone and can span 23 or 25 elapsed hours; derive its UTC instants from the calendar rather than add 24 hours. Business calendars require versions and domain ownership.

Hash partitioning requires canonical key bytes, named algorithm/version, seed, signed/unsigned conversion, modulus/bucket rule, and null behavior. Runtime-default language hashes may change between processes or versions. Changing bucket count generally reassigns members and is partition evolution, not configuration trivia.

Null, malformed, ambiguous, and out-of-domain values need explicit quarantine, sentinel bucket, rejection, or exclusion. A sentinel such as `unknown` is a genuine logical category only when consumers accept that meaning; it must not hide parsing defects. Conservation checks include quarantined/excluded populations.

### Maintain an expected partition inventory

Generate expected keys for a bounded horizon from the versioned definition and eligibility relation. Persist or reproducibly derive enough state to answer whether a key was expected, when it became eligible, which spec applies, and whether its absence is intentional. File listings are observed storage, not the expected inventory.

An inventory record can include asset/spec/key, dimension values, effective interval, expectation/eligibility source, desired generation/fingerprint, state, selected inputs, latest candidate/accepted generation, quality/freshness, block reason, owner, timestamps, and provenance. Store histories or transitions when incident reconstruction matters.

State vocabulary must be explicit:

- `not_expected`: outside the governed space/effective relation;
- `expected_not_due`: valid future or not-yet-eligible obligation;
- `ready`: all exact inputs and policy gates resolve;
- `materializing`: one or more attempts exist;
- `accepted_nonempty` or `accepted_empty`: validated published generation;
- `blocked`: expected but a named prerequisite/policy is absent;
- `failed`/`quarantined`: attempt or data failure with terminal/recovery policy;
- `skipped`/`waived`: explicit authorized disposition, not success;
- `superseded`: older generation replaced by correction; and
- `expired`/`retired`: lifecycle state with retained evidence.

Avoid a single traffic-light status that collapses these distinctions. A green whole-asset dashboard can report coverage ratio plus freshness/quality and still list exceptions.

### Distinguish empty from missing

An empty partition has an accepted manifest with zero input/output counts as appropriate, schema, code/config version, exact source scope, completeness/watermark evidence, quality results, and publication identity. Downstream mapping can consume this evidence and compute a valid zero contribution.

Missing means the expected inventory has no acceptable generation. It may be blocked, late, failed, not yet due, intentionally waived, or lost. Diagnose from inventory and upstream mapping. Never synthesize empty because a path does not exist, a query returned no rows from an eventually consistent replica, or an event was not received.

Some assets omit physical data files for empty partitions. Retain a catalog/manifest record so absence of rows remains distinguishable from absence of processing. Readers resolve accepted generations through metadata, not directory existence alone.

Optional partitions need a contract. A country with no legal operation may be `not_expected`; a country expected to have zero orders can be accepted empty; a temporarily unavailable source is blocked. These categories affect denominators in coverage and service-objective metrics.

### Map dependencies explicitly

For edge $u\rightarrow v$, mapping $M_{u,v}(d)$ returns the exact upstream logical keys required for downstream key $d$. Then resolve one accepted compatible generation for each key and bind it in the downstream run manifest. Mapping keys without generation binding still allows mutable inputs.

Common shapes are:

- identity/same-key: daily-region orders to daily-region normalized orders;
- time offset: today's comparison consumes yesterday plus today;
- window: seven-day output consumes seven or more daily inputs including context;
- many-to-one aggregation: 24 hourly UTC inputs to one UTC day;
- one-to-many split: one global snapshot feeds region-specific outputs;
- broadcast: one same-date rates partition feeds every region;
- dimension projection: date × region downstream maps to date-only upstream;
- cross-calendar/custom: market session maps to exact source intervals; and
- sparse relation: only tenant-region pairs registered as valid are required.

Mapping must define behavior at first key, daylight-saving changes, month/year/leap boundaries, missing offsets, dynamic-key addition/removal, optional parents, empty parents, and spec-version transition. Test totality over expected downstream keys and ensure every returned upstream key belongs to its upstream domain.

Minimality matters for cost and lineage, but completeness comes first. A seven-day output that consumes only its date is wrong; a mapping that consumes the whole source history may be safe but wasteful and causes excessive invalidation. Document why each key is required.

### Bind generations and define readiness

Partition readiness is a predicate over accepted input generations, not upstream task statuses. Each mapped upstream key must resolve a generation whose schema/semantics, quality, completeness, freshness, security, and epoch are compatible. Optional or fallback inputs follow explicit rules and label output degradation.

The downstream manifest freezes the resolution before execution. A retry uses the same upstream generations. If a source correction arrives, policy creates a superseding downstream logical generation/request rather than silently changing input under an existing attempt key.

For fan-in, compare the required set with resolved accepted set. Message counts are insufficient: two events can describe the same source, wrong dates, old generations, or incompatible epochs. Preserve block reasons by upstream asset and key so reconciliation and operators know what is missing.

Readiness does not necessarily mean immediate admission. Capacity, maintenance, approval, privacy holds, or deadline policy may defer work. Keep data readiness separate from scheduling and resource state.

### Publish one generation per revision

Each attempt writes an immutable candidate for exactly one logical partition revision or for a declared atomic group. The candidate manifest binds partition spec/key, upstream generations, code/schema/config/policy, attempt/fence, objects/files, statistics, digests, quarantine, and checks.

Validate membership conservation, schema, row/business keys, counts, duplicates, bounds, referential rules, and domain quality. Then publish using a transactional catalog commit or conditional pointer update. A matching idempotency key/fingerprint returns the accepted generation; a stale fencing token or competing fingerprint is rejected. DE-044 supplies the retry proof.

Consumers resolve through the accepted asset/partition catalog or table snapshot. Do not treat last file modification time, directory success marker alone, or job exit as generation identity. Downstream lineage records exact accepted generation IDs.

Some products need atomic multi-partition publication—for example, a day of regions that must reconcile globally. Compute cells independently if useful, but publish a parent snapshot manifest that selects the complete accepted set. State whether consumers may observe individual cells before the group closes.

### Separate logical and physical partitioning

Logical date × region partitions can be stored as files partitioned only by month, clustered by region, and compacted into size-controlled objects. Alternatively, one logical daily partition can span many physical hash buckets. Keep a mapping in the generation manifest/table metadata.

Physical layout optimizes scan, write, lifecycle, and metadata. Choose columns/transforms frequently present in selective predicates, with sustainable cardinality and distribution. Clustering/sorting and file statistics can complement coarse partitioning. Over-partitioning produces empty directories and small files; under-partitioning scans excess data and makes repair coarse.

Table formats differ. Apache Iceberg defines partition specs and transforms separately from source columns and supports hidden partitioning; readers use metadata to plan files across specs. Hive-style layouts commonly expose `PARTITIONED BY` directory/catalog values. BigQuery supports time-unit, ingestion-time, and integer-range partitioning and prunes qualifying partitions when predicates allow. Verify exact engine behavior.

Never assume path values are truthful row values. Validate during write or use a table format that tracks transforms, and test corruption/misplacement. Query pruning based on bad metadata can omit matching records. Row-level predicates remain necessary when the query contract requires them.

### Engineer pruning without changing semantics

Given query predicate $q$ and partition metadata summary $s(f)$ for physical unit $f$, prune only when the planner can soundly prove no row in $f$ satisfies $q$. False positives read extra data; false negatives omit valid results and are correctness defects.

Use typed predicates aligned with the engine's partition transform. Wrapping a partition column in an unsupported function, comparing incompatible types, or filtering a derived field can disable pruning. Inspect query plans and bytes/files scanned for representative workloads rather than assume the optimizer inferred intent.

Partition projection can compute candidate partition values from configured rules instead of retrieving every catalog entry. AWS Athena documents this as an in-memory calculation and notes that poorly matched ranges can project many empty partitions. Projection configuration becomes governed metadata; an incorrect range can omit or waste scans.

Pruning does not authorize data. A caller allowed to request `region=eu` must be independently prevented from querying `region=us`; do not concatenate untrusted keys into paths or SQL. Apply parameterization, object/catalog permissions, row/column policies, and tenant-bound manifests.

### Control cardinality, skew, and files

Estimate key count over active horizon. For daily × 5 regions × 10,000 tenants, one year yields 18.25 million cells before versions/corrections. If most are empty, use a sparse eligibility registry, coarser logical ownership, or tenant as row/security dimension rather than unconditional partition axis.

Measure rows, bytes, files, runtime, and query activity per partition. Median hides hot cells; inspect high percentiles and largest keys. A global customer or `unknown` bucket can dominate. Salting can split physical execution, but logical recombination and key stability remain required.

Set target file-size ranges from storage/query engine evidence. Compaction rewrites physical files into a new table snapshot/generation without changing logical row meaning; preserve lineage and prevent it from racing corrections or retention. Avoid one file per task as a durable layout rule.

Control scheduling/event/check fan-out. Materializing a million partitions individually can overwhelm orchestration even when compute is cheap. Vectorized/batched execution may materialize several logical keys while retaining per-key manifests and acceptance. UI and API pagination must not load the whole space.

### Evolve the partition definition safely

Assign immutable spec IDs. Changes include add/drop/rename dimension, new static/dynamic keys, new calendar/time zone, interval granularity, transformed source field, bucket algorithm/count, null policy, effective membership, key encoding, and physical table transform. Classify whether the change affects logical ownership, physical layout only, or both.

For logical change, define effective boundary and mapping between old/new keys. An occurrence must not be owned by both or neither unless an explicit overlap/cutover state exists. Historical data can retain old semantics, be rebuilt under new spec as a distinct generation, or expose a compatibility view. Never reinterpret old paths in place.

Iceberg partition evolution can add, remove, or change partition fields without rewriting existing data; files retain the spec used when written and planning spans mixed specs. This is a physical/table-format capability, not proof that a domain calendar change preserves logical meaning. Maintain the asset-level spec contract above it.

Roll out reader compatibility before writers emit a new spec. Test pruning and lifecycle across mixed data. Record rollback: whether new-spec writes stop, how accepted snapshots revert, and how candidate/rewrite data is cleaned without deleting still-referenced files.

### Govern lifecycle, deletion, and correction

Retention can be asset-wide, dimension-specific, or generation-specific. Partition expiration/drop may delete physical data, metadata, or both depending on engine. Confirm snapshots/time travel, legal holds, replicas, caches, candidates, and downstream derivatives. A dropped catalog entry does not prove every copy is erased.

Keep minimal tombstone/evidence as policy allows: partition identity/spec, generation, deletion authorization, time, scope, storage cleanup, lineage notification, and verification. Privacy policy may require minimizing key contents or tokenizing tenant identifiers.

Late data and corrections create a new partition generation or restatement linked to the prior accepted generation. Recompute its justified downstream closure using exact mappings. A correction to one hour may affect one daily asset plus seven rolling-window outputs; it should not indiscriminately rebuild all history or silently mutate one file.

Decommissioning stops new expected keys, freezes or migrates consumers, resolves active candidates/attempts, publishes final dispositions, applies retention/deletion, removes triggers and dynamic-key producers, and retains lineage/receipts as required. Mark retired rather than let partitions look mysteriously missing.

### Reconcile and operate the partitioned asset

For bounded horizon $H$, compare expected inventory $E_H$, accepted generation keys $A_H$, active work, candidates, physical table manifests, dependency resolution, and consumer freshness. Raw set difference $E_H-A_H$ is only a candidate exception: subtract not-yet-due, authorized skip/waiver, expiry, and retirement, then classify remaining keys.

Detect accepted keys not expected under any effective spec; multiple accepted current generations; same key/different fingerprint conflict; accepted partition with missing parent generation; valid-empty without completeness evidence; physical files absent from accepted manifest; orphan candidates; stale dynamic keys; and lifecycle actions inconsistent with holds.

Metrics include expected/eligible/accepted/empty/missing/blocked/failed counts; coverage and freshness by age/spec/dimension; readiness delay; materialization and publication latency; corrections; row/byte/file distribution; small-file ratio; metadata/planning latency; bytes pruned/scanned; query heat; mapping fan-in/out; reconciliation age; and repair cost. Bound metric labels.

Repair begins with diagnosis and preview. A missing accepted partition may require trigger repair, upstream completion, same-fingerprint retry, or new correction intent. DE-046 develops historical selection, ordering, capacity, and approval. This module supplies the exact keys and generations that a backfill plan must name.

### Secure and test every boundary

Authorize asset/spec/key inventory, data resolution, materialization, retry, backfill, correction, publish, waive, expire, delete, and inspect-lineage operations. Bind tenant from trusted identity/context, not key text. Validate dynamic keys and mapping outputs against permitted domains. Audit bulk selections and overrides.

Test encode/decode round trips, canonical equality, delimiters/Unicode/case, invalid/null/out-of-range inputs, adjacent interval boundaries, leap days, daylight-saving gaps/folds, calendar revisions, bucket stability, and dimension product constraints. Property tests can prove each generated occurrence maps once within bounded domains.

Test mappings at boundaries and against a simple independent oracle. Assert every expected downstream key maps only to valid upstream keys, includes required context, handles accepted empty correctly, and blocks missing inputs. Reverse input order and vary scheduling; bindings must remain deterministic.

Inject retries, concurrent attempts, stale fences, partial candidate files, manifest corruption, publication acknowledgement loss, mixed spec data, compaction races, expired partitions, catalog lag, and unauthorized cross-tenant keys. Query representative predicates and inspect plans/results for both pruning efficiency and result equality against an unpruned oracle.

Production evidence includes definition/spec diffs, bounded inventory reconciliation, actual table/catalog manifests, engine-version integration tests, query plans, storage/object checks, lineage, quality, consumer verification, capacity tests, access audits, retention proofs, and incident exercises. A green partition grid is an index into evidence, not the evidence itself.

## Definitions and Notation

Let asset $A=(id,owner,G,C,S)$ have stable identity, grain/population contract $G$, schema/semantics $C$, and set of partition specifications $S$. A spec

$$
s=(id_s,dimensions,domains,encode,decode,p_s,effective_s)
$$

defines typed dimensions/domains, canonical key functions, membership $p_s$, and effective range. For all valid keys, require $decode(encode(values))=values$ and canonical re-encoding equality.

For source occurrence bag $D$ and bounded intended scope $D|_E$, partition bag

$$
P_k=\{x\in D:p_s(x)=k\},\qquad k\in E
$$

must satisfy $\biguplus_{k\in E}P_k=D|_E$. Quarantine/exclusion is modeled as a named outcome and included in conservation, not discarded before comparison.

For dimensions $D_1,\ldots,D_m$, naive product $K=\prod_iD_i$ may be restricted by eligibility relation $R_s\subseteq K$. Expected inventory over horizon $H$ is

$$
E(A,s,H)=\{encode_s(x):x\in R_s\land eligible(x,H)\}.
$$

This separates valid space from bounded expected obligations and from accepted materializations.

Dependency mapping $M_{u,v,s_u,s_v}:K_v\rightarrow\mathcal{P}(K_u)$ returns a finite set of upstream keys. For downstream $d$, resolved input manifest is

$$
I_d=\{(u,k,g_{u,k}):u\in parents(v), k\in M_{u,v}(d)\},
$$

where each $g_{u,k}$ is one accepted compatible generation. Optional/fallback relations require separate policy rather than removal from the set silently.

A partition generation

$$
g=(A,s,k,revision,h,I,code,schema,manifest,quality,published)
$$

binds logical scope/spec, correction revision, fingerprint, inputs, interpretation, physical manifest, controls, and publication transition. Candidate $c_{attempt}$ is not $g$ until accepted.

Let expected eligible keys be $E$, accepted nonempty $N$, accepted empty $Z$, authorized dispositions $W$, and unresolved $U$. A basic coverage partition requires these states disjoint and

$$
E=N\uplus Z\uplus W\uplus U.
$$

Coverage ratio can be $(|N|+|Z|+|W_{counted}|)/|E|$ only after policy states whether any waivers count. Publish numerator/denominator and exclusions rather than one unexplained percentage.

Logical partition key $k$, generation $g$, attempt $a$, execution shard $e$, physical partition spec/field values $f$, file/object $o$, and query predicate $q$ are distinct identifiers. A manifest records their relationships. Conflating them makes retry, correction, pruning, and lineage claims ambiguous.

## Mechanisms, Invariants, or Proof Structure

The assurance structure has eight layers.

**1. Partition meaning is versioned.** The asset grain/population and spec define dimension types, domains, membership, boundaries, key encoding, eligibility, and effective range. Therefore a key has one interpretable logical scope under one spec. Silent rule changes invalidate this premise.

**2. Membership conserves occurrences.** For bounded input generation, assign each valid occurrence through $p_s$ exactly once and record quarantine/exclusion. Reconcile bag counts and stable identities, not just set membership. This proves coverage/disjointness only for the tested/authoritative population and mapping version.

**3. Expected inventory is independent of observed output.** Generate $E$ from definition and authoritative eligibility, not files or completed runs. Therefore missing output remains detectable, and accepted output outside $E$ is anomalous rather than expanding expectation retroactively.

**4. Dependency mapping is total and exact.** For every expected downstream key, $M$ returns valid upstream keys with required context. Readiness resolves exact accepted compatible generations and distinguishes empty from absent. This blocks process-success or message-count shortcuts.

**5. Attempts cannot redefine scope.** Run manifests freeze spec/key, inputs, code/schema/config, and expected effect. Attempts write isolated candidates. Idempotency and fencing admit one validated generation per logical revision, so retry overlap cannot mix physical outputs.

**6. Publication defines visibility.** A transactional catalog/snapshot or conditional pointer selects complete manifests. Consumers and downstream mappings resolve accepted generations through it. Files and task states outside that boundary cannot satisfy readiness.

**7. Physical optimization preserves logical results.** Partition transforms, clustering, pruning, compaction, and spec evolution may change files scanned/stored but query results must match a logical/unpruned oracle for the same accepted snapshot and authorization. Mixed specs retain their interpretation.

**8. Reconciliation and lifecycle close the system.** Compare expected, accepted, attempts, candidates, physical manifests, downstream consumption, and lifecycle actions. Every discrepancy has owner and disposition; retention/deletion preserves required evidence and removes all governed copies.

Key invariants include:

- canonical key decoding is injective over valid dimension tuples;
- every expected key names one effective logical spec and asset namespace;
- every accepted generation belongs to an expected/explicitly authorized key and has one manifest;
- accepted empty contains affirmative completeness evidence;
- exact upstream generation bindings are immutable within a generation fingerprint;
- mapping never invents out-of-domain keys and handles every expected downstream key;
- candidate/attempt output cannot be resolved as current without publication;
- stale attempts and prior spec writers cannot replace a newer accepted pointer;
- pruning and lifecycle rules are derived from trusted metadata and verified against results/holds;
- spec evolution does not silently change historical key populations;
- dynamic-key creation/deletion and manual waiver are authorized, audited, and reconciled;
- control-plane cardinality remains bounded and paginated.

### Executable partition-inventory model

The following finite model demonstrates canonical date × region keys, exact date-region plus date-only fan-in, valid-empty versus missing, deterministic mappings independent of input order, and logical predicate pruning. It does not model real calendars/time zones, storage/table formats, files, concurrency, publication, catalog consistency, quality, authorization, performance, or dynamic/evolving specs.

<!-- bijux-verify: {"id":"partitioned-asset-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"partition_count=4\nready_count=3\nblocked_partitions=((\u00272026-09-02|us\u0027, (\u0027orders\u0027,)),)\nvalid_empty_partitions=(\u00272026-09-01|us\u0027,)\nmapped_input_count=6\ncoverage_complete=False\npruned_for_date=(\u00272026-09-02|eu\u0027, \u00272026-09-02|us\u0027)\npartition_keys_stable=True\n","stderr":""}} -->
```python
from itertools import product


DATES = ("2026-09-01", "2026-09-02")
REGIONS = ("eu", "us")
EXPECTED = tuple(f"{day}|{region}" for day, region in product(DATES, REGIONS))

ORDERS = {
    ("2026-09-01", "eu"): ("orders-g1", 3),
    ("2026-09-01", "us"): ("orders-g2", 0),
    ("2026-09-02", "eu"): ("orders-g3", 2),
}
RATES = {
    "2026-09-01": "rates-g7",
    "2026-09-02": "rates-g8",
}


def decode(key: str) -> tuple[str, str]:
    day, region = key.split("|")
    assert day in DATES and region in REGIONS
    return day, region


def inventory(
    order_items: tuple[tuple[tuple[str, str], tuple[str, int]], ...]
) -> tuple[tuple[tuple[str, tuple[str, str]], ...], tuple, tuple]:
    orders = dict(order_items)
    ready = []
    blocked = []
    empty = []
    for key in EXPECTED:
        day, region = decode(key)
        missing = []
        if (day, region) not in orders:
            missing.append("orders")
        if day not in RATES:
            missing.append("rates")
        if missing:
            blocked.append((key, tuple(missing)))
            continue
        order_generation, rows = orders[(day, region)]
        ready.append((key, (order_generation, RATES[day])))
        if rows == 0:
            empty.append(key)
    return tuple(ready), tuple(blocked), tuple(empty)


items = tuple(ORDERS.items())
ready, blocked, empty = inventory(items)
reverse_ready, reverse_blocked, reverse_empty = inventory(tuple(reversed(items)))
pruned = tuple(key for key in EXPECTED if decode(key)[0] == "2026-09-02")
print(f"partition_count={len(EXPECTED)}")
print(f"ready_count={len(ready)}")
print(f"blocked_partitions={blocked}")
print(f"valid_empty_partitions={empty}")
print(f"mapped_input_count={sum(len(inputs) for _key, inputs in ready)}")
print(f"coverage_complete={len(ready) == len(EXPECTED)}")
print(f"pruned_for_date={pruned}")
print(
    "partition_keys_stable="
    f"{(ready, blocked, empty) == (reverse_ready, reverse_blocked, reverse_empty)}"
)
```

Every ready downstream key binds two accepted upstream generations: regional orders and date-only rates, giving six mapped inputs. The US partition for September 1 is ready and valid empty because orders has an accepted zero-row generation. September 2 US is blocked because no orders generation exists. Date pruning selects both expected September 2 keys and does not claim both are ready.

## Alternatives and Trade-Offs

**Unpartitioned versus partitioned asset.** One asset generation simplifies atomicity and metadata but makes recovery and incremental freshness coarse. Partitions isolate scope and work while introducing inventory, mapping, and partial-coverage semantics.

**Time versus entity/category dimensions.** Time supports append/correction/retention and common predicates. Entity dimensions isolate tenants/regions but can be high-cardinality or skewed. Combine only when the product and control plane can sustain the space.

**Static versus dynamic keys.** Static sets are reviewable and bounded. Dynamic sets reflect runtime entities but need authoritative registration, validation, tombstones, reconciliation, pagination, and abuse controls.

**Dense Cartesian product versus sparse eligibility relation.** Dense products are simple and make absence visible. Sparse registries avoid impossible cells but require authoritative effective-dating and must not remove expected failures from the denominator.

**Daily versus hourly temporal granularity.** Hourly improves latency and repair locality but creates 24× metadata/tasks/files and complex civil-time boundaries. Daily reduces overhead but repeats more work after late input. Consumers and source completeness decide.

**Business/event time versus ingestion time.** Business/event time preserves domain attribution but requires late corrections and clock/calendar policy. Ingestion time is operationally easy and monotonic at the platform boundary, but does not answer when the event occurred.

**Explicit physical partitions versus hidden transforms.** Explicit directory values are portable and visible but couple queries/writers to layout. Hidden transforms let table metadata derive pruning while easing evolution, at the cost of table-format/catalog dependency.

**Identity versus transformed partition columns.** Identity preserves exact values and can explode cardinality. Month/day/bucket/truncate transforms reduce layout cardinality and enable pruning patterns but scan extra rows and require metadata-aware planning.

**One logical key per task versus batched materialization.** One-to-one gives simple retry/status but high scheduler overhead. Batching amortizes startup while requiring per-key manifests and clear partial-failure/acceptance behavior.

**Per-partition versus group publication.** Per-partition publication maximizes independent freshness. Group snapshots preserve cross-partition invariants but allow one slow cell to delay all. Hierarchical manifests can retain cell evidence under group acceptance.

**Pre-created empty partitions versus manifest-only emptiness.** Physical placeholders can aid some tools but cause metadata/files. Manifest-only zero-row generations are cheaper if every reader resolves the catalog and never equates missing files with missing processing.

**Catalog enumeration versus partition projection.** Enumeration records exact known keys and state but can become large. Projection avoids catalogs for regular spaces but may enumerate many nonexistent values and requires highly accurate rules.

**Partition expiration versus explicit lifecycle workflow.** Native expiration is efficient but may not coordinate snapshots, holds, derivatives, or audit. A governed workflow adds evidence and dependency handling at operational cost; use native mechanisms beneath it when semantics align.

**In-place rewrite versus new generation/spec.** In-place changes look simple but erase lineage and race readers. Immutable generations/specs plus pointer transition cost storage and metadata but provide rollback, audit, and reproducibility.

## Failure Modes and Misconceptions

- **“A folder is a partition.”** A folder is a physical convention; logical identity and acceptance require governed metadata.
- **“One date string has obvious meaning.”** Time role, zone, calendar, precision, and interval boundaries determine membership.
- **“Every day is 24 hours.”** Civil-time days cross offset changes; generate exact instants from the named zone/calendar.
- **“Inclusive ranges are clearer.”** Adjacent inclusive ends duplicate boundaries; use a declared interval convention.
- **“The runtime hash is stable.”** Language/process hashes can change; specify canonical bytes and algorithm/version.
- **“Null belongs in an arbitrary bucket.”** Null/invalid membership needs declared domain meaning or quarantine.
- **“More partitions means more speed.”** Skew, startup, metadata, file, and coordination overhead can dominate.
- **“One customer per partition improves isolation.”** It can create cardinality explosions and does not itself enforce authorization.
- **“Cross products are complete.”** Many dimension combinations may be impossible; use an effective eligibility relation.
- **“No file means zero rows.”** It can mean missing, failed, late, expired, or catalog inconsistency.
- **“Task success makes the partition ready.”** Readiness requires an accepted generation and exact quality/completeness evidence.
- **“Two upstream events satisfy two inputs.”** Resolve named upstream keys and compatible accepted generations.
- **“Daily downstream needs one hourly parent.”** It usually needs the exact interval set, including 23/25-hour civil days where applicable.
- **“Same key means same content.”** Corrections create generations; key names scope, generation names accepted revision.
- **“Retry can write the final path.”** Overlapping attempts can mix files; isolate candidates and fence publication.
- **“Physical and logical partitioning must match.”** They optimize different boundaries and can evolve independently.
- **“Pruning is automatic.”** Predicate shape, transform, types, metadata, and engine behavior determine pruning.
- **“Pruned data is unauthorized data.”** Optimization is not access control.
- **“Path values prove row values.”** Misplaced/corrupt files can violate them; validate membership and manifests.
- **“Partition evolution rewrites meaning safely.”** Format support preserves physical interpretation, not domain-semantic equivalence.
- **“Drop partition proves deletion.”** Snapshots, objects, caches, replicas, candidates, and derivatives may remain.
- **“Compaction is invisible.”** It creates new physical metadata/snapshots and can race writers/lifecycle.
- **“The green grid proves completeness.”** The UI summarizes state; manifests, mappings, controls, and reconciliation prove it.
- **“Backfill means select a date range.”** Exact keys, dependencies, generations, capacity, ordering, and approval are required.
- **“Retired partitions should disappear.”** Retained disposition prevents them from appearing mysteriously missing.

## Worked Examples

### Example 1

A UTC daily partition owns $[2026\text{-}09\text{-}01T00:00Z,2026\text{-}09\text{-}02T00:00Z)$. An event exactly at the end belongs to the next day. Half-open intervals provide disjoint adjacency.

### Example 2

An asset has 365 dates, 12 regions, and 20,000 tenants. A dense product has 87.6 million cells. Because only 60,000 tenant-region relations are active and most have no daily obligation, an effective sparse registry plus coarser batching avoids materializing impossible keys.

### Example 3

A daily revenue partition requires 24 UTC hourly facts and one daily rates partition. Its mapping lists all 25 upstream keys and accepted generations. One hourly valid-empty manifest satisfies readiness; one missing hour blocks it.

### Example 4

A seven-day rolling metric for September 7 maps to facts September 1–7. A correction to September 3 affects rolling outputs September 3–9, subject to asset boundaries. Same-date mapping would under-invalidate and under-compute.

### Example 5

Two attempts compute date × region `2026-09-01|eu`. Both write immutable candidates. The current fence accepts candidate B; candidate A later completes but cannot swap the partition pointer. The logical key remains the same while attempts/candidates differ.

### Example 6

A source produces no orders for a region. The accepted orders manifest records zero rows, source watermark past interval end, schema, controls, and generation. Downstream consumes it as a zero contribution rather than retrying forever.

### Example 7

A table is logically daily-region but physically partitioned by month and clustered by region. A one-day/one-region query prunes the month using the transform and uses clustering/file statistics within it. Logical daily repair does not require one physical directory per day.

### Example 8

An Athena projection rule declares years 2000–2100 while data exists only for two years. Queries can project many empty partitions and waste planning/scans. Tight governed ranges or a catalog/eligibility source better match reality.

### Example 9

An Iceberg table adds a bucket transform for new files. Old files retain their prior spec; planning evaluates both. The asset catalog records this as physical spec evolution, while logical business-date partition identity remains unchanged.

### Example 10

A retention job drops a table partition while an older snapshot and object copies remain. The governance record stays `deletion_pending` until snapshot expiry, object cleanup, replica/cache handling, downstream notification, and legal-hold verification complete.

## Cross-Program Connections

[API-017](../../28-api-and-service-engineering/modules/017-filtering-sorting-and-pagination.md) defines typed filters and bounded traversal for partition inventories. [API-037](../../28-api-and-service-engineering/modules/037-idempotency-keys.md), [API-038](../../28-api-and-service-engineering/modules/038-concurrency-control-at-the-api-boundary.md), and [API-070](../../28-api-and-service-engineering/modules/070-designing-an-asynchronous-api-for-replay-and-evolution.md) support safe materialization/backfill control APIs.

[PLAT-043](../../29-platform-engineering/modules/043-batch-and-scheduled-workload-templates.md) provides candidate/fencing golden paths, while [PLAT-069](../../29-platform-engineering/modules/069-platform-eventing.md) can carry accepted-generation notifications. The platform exposes scalable partition views and controls; domain/data owners define membership, completeness, and mapping.

[DBE-062](../../18-database-engineering/modules/062-predicate-pushdown-and-projection-pruning.md) covers database predicate and projection pruning. This module keeps query-engine optimization distinct from logical asset obligations and orchestration state.

Within Data Engineering, [DE-034](034-partitioned-processing.md) owns parallel execution/storage mechanics and [DE-038](038-late-corrections-and-restatement.md) owns corrections. [DE-041](041-directed-acyclic-graphs-and-dependencies.md) through [DE-044](044-retries-timeouts-and-idempotency.md) establish graph, asset, trigger, and attempt semantics. DE-046 uses this exact inventory/mapping model to plan backfills.

## References

1. Dagster, [Partitioning Assets](https://docs.dagster.io/guides/build/partitions-and-backfills/partitioning-assets). Documents time-based, static, two-dimensional, and dynamic asset partition definitions and partition-keyed materialization. Accessed 2026-09-03.
2. Dagster, [Defining Dependencies Between Partitioned Assets](https://docs.dagster.io/guides/build/partitions-and-backfills/defining-dependencies-between-partitioned-assets). Documents same/different partition definitions, time-window mappings, offsets, and custom partition mappings. Accessed 2026-09-03.
3. Apache Iceberg, [Table Specification: Partitioning](https://iceberg.apache.org/spec/#partitioning). Defines partition specs, fields, transforms, spec identifiers, and representation used to interpret partitioned data. Accessed 2026-09-03.
4. Apache Iceberg, [Evolution: Partition Evolution](https://iceberg.apache.org/docs/latest/evolution/#partition-evolution). Documents adding, removing, and changing partition fields without rewriting existing files and planning across mixed specs. Accessed 2026-09-03.
5. Google Cloud, [Introduction to Partitioned Tables in BigQuery](https://cloud.google.com/bigquery/docs/partitioned-tables). Documents time-unit, ingestion-time, and integer-range partitioned tables and their operational/query characteristics. Accessed 2026-09-03.
6. Google Cloud, [Query Partitioned Tables](https://cloud.google.com/bigquery/docs/querying-partitioned-tables). Documents qualifying filters and partition pruning behavior for BigQuery partition types. Accessed 2026-09-03.
7. Google Cloud, [Manage Partitioned Tables](https://cloud.google.com/bigquery/docs/managing-partitioned-tables). Documents partition expiration, updates, and deletion/lifecycle behavior in BigQuery. Accessed 2026-09-03.
8. Amazon Web Services, [Use Partition Projection with Amazon Athena](https://docs.aws.amazon.com/athena/latest/ug/partition-projection.html). Documents rule-based in-memory partition value calculation, configuration, ranges, and behavior with sparse/empty projected partitions. Accessed 2026-09-03.
9. Delta Lake, [Best Practices: Choose the Right Partition Column](https://docs.delta.io/latest/best-practices.html#choose-the-right-partition-column). Provides physical partition-column guidance concerning common predicates, cardinality, and data volume. Accessed 2026-09-03.
10. Apache Hive, [LanguageManual DDL](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL). Documents partitioned table declarations and partition add/drop/repair operations in Hive metadata. Accessed 2026-09-03.

## Exercises

### Exercise 1

Design a versioned partition definition for orders by Europe/Stockholm business day and region. Specify time field, half-open UTC instants, calendar/DST behavior, region domain/effective dates, key encoding, empty/missing semantics, and tests at spring/fall offset transitions.

### Exercise 2

A downstream daily-region metric needs same-key orders, all hourly traffic for the local civil day, same-date global rates, and the prior six daily-region metric partitions for a rolling window. Define mapping and readiness, including valid-empty, missing, first-six-days, and correction behavior.

### Exercise 3

An asset definition combines 730 dates, 30 regions, 50,000 tenants, and 8 source types. Compute the dense cell count. Propose a defensible logical/physical design when only 120,000 tenant-region pairs are active and most consumers filter date plus region rather than tenant.

### Exercise 4

A table changes physical partitioning from identity `event_date` to month transform plus 32 customer buckets. Explain spec/version handling, old/new file planning, logical partition identity, reader rollout, pruning verification, compaction, rollback, and why the change does or does not require logical restatement.

### Exercise 5

Build a reconciliation procedure for a 90-day date × region asset. Include expected inventory, eligibility, accepted empty/nonempty, blocked inputs, active attempts/candidates, physical manifests, multiple generations, consumer freshness, expiration/legal holds, authorization, repair preview, and evidence.

## Answers to the Exercises

### Answer 1

Use spec `orders-business-day-region/v1` with typed dimensions `day=YYYY-MM-DD` and enum `region`, canonical named-field or escaped fixed-order encoding, and an authoritative region effective-date registry. Membership uses the governed order business timestamp, not ingestion time. For each local day, resolve `[local 00:00, next local 00:00)` in `Europe/Stockholm` through the named time-zone database/calendar; store resulting UTC instants and calendar version, so transition days can span 23 or 25 hours. An accepted zero-row manifest after source completeness is valid empty; absent accepted evidence is missing/blocked. Test instants immediately before/at/after both bounds, leap day, spring gap, fall fold (including repeated local labels), calendar changes, invalid zone/region, and encode/decode round trips. Historical slots retain v1 meanings if tz/calendar rules evolve.

### Answer 2

For downstream key `(d,r)`, map orders to `(d,r)`; derive the exact UTC hourly keys covering local interval $d$ (23/24/25 where applicable); map rates to date-only key under its declared calendar; and map rolling parents to `(d-6,r),...,(d-1,r)`. Resolve exact accepted compatible generations and bind them. Accepted-empty inputs satisfy their named contribution; missing required inputs block. For the first six dates, either define a shorter-window bootstrap explicitly or require prehistory—never silently omit parents. A corrected hourly/order/rates/rolling parent creates a superseding output generation and invalidates the exact downstream closure according to mapping.

### Answer 3

The dense product is $730\times30\times50{,}000\times8=8{,}760{,}000{,}000$ cells, operationally unsuitable. Use a sparse effective registry for 120,000 valid tenant-region relations only if tenant-level logical ownership is genuinely needed; even that times date/source may remain huge. Given dominant date-region queries, prefer logical date × region partitions with tenant and source represented in rows/manifests or bounded execution buckets, enforcing tenant authorization independently. Physically partition coarsely by date/month and region, then cluster/bucket by tenant as measured. Batch per-key orchestration, retain source-type completeness in the manifest, and validate cardinality/skew/files/planning before rollout.

### Answer 4

Create a new immutable physical table partition spec ID effective for new files; retain the old spec ID on old files so metadata-aware readers plan both. If logical asset membership remains exact event date, the logical date partition key/spec need not change: month and bucket are physical transforms recorded in generation manifests. Roll out mixed-spec-capable readers first, write canaries, compare results with an unpruned oracle, inspect plans/bytes/files, and verify bucket algorithm/canonical key. Compaction can rewrite old files under the new physical spec in new snapshots without changing logical rows, with lineage and concurrent-write protection. Rollback switches the accepted table snapshot/writer policy and preserves referenced files. Restatement is required only if source membership, logical grain, row content, or accepted generation semantics change—not merely because physical placement changes.

### Answer 5

Generate bounded expected keys from the effective spec plus region registry for 90 days; classify future/not-due, expired, retired, and authorized waivers. Resolve accepted manifests and separate nonempty from affirmative empty. For unresolved keys, compute exact upstream mappings and block reasons; inspect scheduled/run/attempt state and immutable candidates. Verify each accepted key has one current generation/fingerprint, valid controls, exact input lineage, and referenced physical files/table snapshot; detect unexpected keys, duplicates, orphans, stale fences, and mixed-spec errors. Compare consumer-observed generation/freshness. Apply expiration only after hold/snapshot/replica/derivative checks. Expose tenant-scoped, paginated evidence. Preview repairs with exact keys, cause, inputs, cost, order, capacity, downstream impact, and authorization; then retry unchanged work, create correction intent, repair triggers, or retain a governed disposition. Reconcile again and retain the before/after record.
