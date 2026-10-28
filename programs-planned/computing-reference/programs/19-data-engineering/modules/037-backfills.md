---
module_id: DE-037
program: Data Engineering
level: 1
module_number: 37
title: Backfills
status: complete
last_verified: 2026-09-02
---

# Backfills

## One-Page Review

### Governing question

How can historical output be filled, repaired, or rematerialized over an exact scope without corrupting live data, mixing semantic versions, overwhelming dependencies, or claiming success before complete validation and atomic publication?

### Essential definitions

- A **backfill** is an intentional, bounded materialization of missing or superseded historical output under declared source, reference, transformation, schema, and runtime versions.
- A **backfill request** records why work is needed, the intended output scope, semantic policy, approvals, priority, resource envelope, validation, publication, and rollback plan.
- A **logical unit** is the smallest independently owned output slice, such as an event-time day, tenant/day pair, key range, or immutable source interval.
- The **output ownership set** $U$ is the exact set of logical outputs the backfill may replace or supersede.
- The **input context** $C(U)$ is all source/reference state required to compute $U$, including joins, window halos, prior state, and transitive dependencies; it can be larger than $U$.
- A **backfill manifest** enumerates units, bounds, input cuts/versions, code/config/runtime, dependency mapping, candidate destinations, expected checks, and run identities.
- A **backfill operation key** names the logical request plus unit and remains stable across physical attempts.
- A **fence** prevents an older candidate from overwriting newer live or corrective state, using versions, leases with fencing tokens, or conditional publication from an expected generation.
- A **shadow generation** is isolated candidate output not visible through the trusted production pointer until validation succeeds.
- A **catch-up interval** covers changes after the frozen historical source cut and before cutover.
- **supersession** records that one output generation/version replaces another without erasing lineage.
- A **rebuild horizon** is the oldest point for which raw inputs, schemas, code/config, reference history, and capacity still support faithful recomputation.

### Central model, mechanism, or theorem

Let $O_g$ be trusted output generation $g$, $U$ the exact owned output-key set, $S_c$ and $R_c$ immutable source/reference state at cut $c$, and $F_v$ transformation version $v$. Correct candidate output for the scope is

$$
B_U=F_v(S_c,R_c)\restriction_U.
$$

Publication must preserve every unowned key and replace exactly $U$:

$$
O_{g+1}=\left(O_g\restriction_{K\setminus U}\right)\cup B_U.
$$

The reads needed to calculate $B_U$ may be the larger dependency closure $C(U)$. Reading only inputs whose partition labels equal $U$ is correct only if $C(U)=U$ has been proved.

Partition the ownership set into retryable units $U_1,\ldots,U_n$ such that their output ownership is disjoint and complete:

$$
\biguplus_{i=1}^{n}U_i=U.
$$

Each attempt writes isolated candidate output; one validated manifest selects exactly one accepted result per intended unit. Final publication is conditional on expected base generation/fence, so a stale backfill cannot erase live progress.

### Critical invariants

- Purpose, owner, approval, source of truth, correction/as-was/as-now semantics, output scope, and downstream impact are explicit.
- $U$ uses exact key/range/time-zone/precision/interval conventions; expected units are enumerated before execution.
- $C(U)$ includes transitive lineage, joins, window/session halos, state initialization, reference versions, and boundary context.
- Source objects/snapshots/log positions, reference generations, code/config/runtime, schema, and target base are immutable or content-addressed for the request.
- One operation key per logical unit survives retry; attempts write isolated outputs and cannot mutate trusted state piecemeal.
- Unit ownership covers $U$ without gaps/overlap; manifests select exactly one accepted attempt per expected unit.
- Concurrent live ingestion, corrections, other backfills, schema work, and compaction are serialized, fenced, or safely rebased under declared rules.
- A backfill never regresses newer source/entity/output versions, replays additive effects, duplicates external notifications, or deletes outside $U$.
- Admission, concurrency, scan/write rate, lock/log/replication pressure, quotas, storage, and cost stay within measured budgets and stop conditions.
- Validation proves inputs, units, candidates, key/multiplicity/schema/value/business controls, unchanged outside scope, and downstream compatibility.
- Publication/cutover binds candidate generation, backfill manifest, validation evidence, source/reference cuts, version lineage, and checkpoint atomically/conditionally.
- Pause, resume, cancel, reconcile, rollback/forward repair, retention, security, audit, and rebuild procedures are tested.

### Common failures

Common failures include treating scheduler success as data correctness; choosing dates without defining output grain; using inclusive ends twice; confusing processing date with event time; reading only partitions being written despite windows/joins; replaying current mutable dimensions when “as-was” history is required; running old code against new schemas; mutating production partitions task by task; reusing ordinary scheduled-run identity; clearing successful runs without data-generation evidence; launching thousands of units without admission control; backfilling newest-first when state depends on prior outputs; backfilling oldest-first when urgent recent correctness was the real objective; letting an old backfill overwrite live data; interpreting absence in a partial source as delete; retrying additive effects; publishing a partial range; validating only row counts; forgetting downstream aggregates/caches; expiring raw input or tombstones mid-run; and deleting the rollback generation before acceptance.

### Compact example

A model publishes trailing three-day sums. A backfill owns output days 4–6, but it must read source days 2–6: days 2–3 are context for day 4 and are not output ownership. Its candidate is `(4,90),(5,120),(6,150)`. While it runs, live processing advances target generation 12 to 13 and corrects day 8. Publication against expected generation 12 is rejected. The backfill rebases on 13, replaces only days 4–6, proves day 8 remains unchanged, and conditionally publishes generation 14. Replaying the same candidate is a no-op.

### Connections

[DE-030](030-designing-replayable-raw-ingestion.md) preserves historical source evidence, [DE-032](032-sql-transformation-pipelines.md) defines graph/version publication, [DE-034](034-partitioned-processing.md) defines unit ownership and manifests, [DE-035](035-incremental-models.md) defines full equivalence and affected sets, and [DE-036](036-merge-and-upsert-semantics.md) defines versioned mutation. DE-038 next specializes late correction/restatement; DE-039 and DE-040 address determinism and batch testing.

## Governing Question

What evidence lets an operator deliberately recompute history while proving the selected history, semantics, dependencies, resource impact, and published result are exactly the intended ones?

A backfill is often invoked as a command with two dates. That interface hides the important questions. Which clock do the dates belong to? Are bounds inclusive or half-open? Do they name source rows, output partitions, scheduler logical dates, or business reporting periods? Which source and reference versions are authoritative? Which code version should reinterpret history? What later outputs depend on the selected interval?

The safest definition starts from owned output, not scheduled runs. The request names exact logical outputs that may change and calculates all context needed to compute them. It freezes inputs and semantics, stages candidate results, validates them, then publishes by a fenced transition. Scheduler dates and partition buttons are mechanisms for executing the manifest, not the meaning of the result.

Backfills are intentionally abnormal load. They compress months or years of historical work into hours or days while live traffic continues. Source APIs, warehouses, databases, catalogs, object stores, downstream models, and observability systems can all saturate. Admission and rate controls are correctness controls because overload can cause retries, retention loss, delayed live data, or partial downstream propagation.

Historical meaning is another choice. A code-change backfill commonly asks, “What would version $v_2$ produce from retained historical facts?” A reproducibility replay asks, “Can version $v_1$ reproduce the output originally published?” A business restatement may apply a newly authoritative correction and current policy to old periods. These are different axes; label them rather than calling every result “fixed history.”

## Why This Matters

Backfills create data that was missing during initial adoption, repair failed/corrupt intervals, propagate source corrections, populate new columns, apply new business logic, migrate models, rebuild indexes/features, or recover after disaster. Without a governed path, teams improvise production SQL and one-off scripts precisely when blast radius is largest.

A correct pipeline can still produce an incorrect backfill if boundaries differ. A daily job scheduled at midnight might process the previous UTC day, a local business day, or a rolling 24-hour interval. Passing `2026-03-01` through the wrong interpretation can duplicate midnight, omit a daylight-saving hour, or assign an event to a different period than the live pipeline.

Dependencies amplify scope. Recomputing source day 20 for a trailing seven-day metric can change outputs 20–26. A dimension correction can affect facts across its validity interval. A session event can merge two sessions beyond a fixed window. A cumulative balance can affect every later output. Input context and output ownership therefore require lineage plus operator-specific influence, not path-name equality.

Live coexistence is the central operational hazard. A historical job may start from generation 50, run for hours, then overwrite a target after live generation 60 has arrived. Replacing an entire table loses generations 51–60; merging without source/output versions can regress overlapping keys. Shadow generations, source-version guards, expected-base commits, and catch-up make overlap explicit.

Partial visibility damages trust. If 364 of 365 daily partitions update in place and the final partition fails, consumers see a mixture of old and new logic with no coherent version. Even if every partition operation is atomic, the set is not. An isolated candidate manifest and one publication pointer create a reviewable generation boundary.

Operationally, backfills compete with revenue-bearing and freshness-critical work. They can exhaust database I/O, replication/WAL retention, warehouse slots, object listings, catalog commits, queues, rate limits, and budgets. Throttling based only on CPU misses dependency pressure. Backfill SLOs must be subordinate to explicit live-data protection unless the incident decision says otherwise.

## Prerequisites and Retrieval

Retrieve request owner, reason, incident/change/approval evidence, severity/deadline, semantic objective, source of truth, target datasets/consumers, output grain/key/partition specs, exact intended units and exclusions, event/valid/ingestion/processing/scheduler time roles, time zones/calendars/precision/interval conventions, source snapshots/manifests/log positions and retention, reference/dimension history, code/SQL/config/schema/runtime/container/adapter versions, secrets and permissions, lineage graph and partition mappings, window/session/state dependencies, current and desired target generations, live checkpoints and source versions, concurrent jobs/backfills/corrections/compaction/schema changes, idempotency keys and receipts, retry/cancellation behavior, target overwrite/merge/snapshot semantics, validation controls/oracles, downstream materializations/caches/exports, service and freshness SLOs, source/warehouse/database/catalog/object-store quotas, compute/storage/network/log/lock/replication capacity, cost budget, concurrency/admission policy, observability, quarantine, audit/security/privacy/residency, retention/garbage collection, rollback/forward repair, and recovery drills.

Distinguish backfill request from physical run; logical unit from task attempt; scheduler logical date from event/output interval; output ownership from input context; selected partitions from dependency closure; missing materialization from stale/wrong materialization; source correction from transformation change; original/as-was/current/as-now reference state; historical code from current code; source cut from run start time; backfill identity from scheduled-run identity; retry from a new semantic request; candidate completion from production publication; data transaction from manifest-generation commit; live checkpoint from backfill progress; pause from cancel; cancel from rollback; failed task from invalid data; row count from exact key/value equivalence; unit completion from whole-request acceptance; and physical cleanup from semantic supersession.

Create a request contract before execution:

| Concern | Required decision and evidence |
|---|---|
| Intent | Fill, repair, correction, code/schema migration, reproducibility replay, or recovery; owner/approval |
| Semantics | Output contract; old/new code; as-was/as-now references; correction authority; expected differences |
| Scope | Exact owned output keys/ranges, time role/zone/calendar, half-open bounds, exclusions, expected unit set |
| Context | Source/reference cuts, transitive parents, joins, window halos, state seeds, downstream affected closure |
| Identity | Request ID, unit operation key, attempt ID, payload/config digest, superseded generation |
| Execution | Unit graph/order, concurrency, retry, pause/resume/cancel, resources, quotas, stop conditions |
| Coexistence | Live/backfill overlap, source/entity versions, fence/lease, expected base, catch-up and cutover |
| Output | Isolated target, manifest/receipts, exact ownership/replacement rule, schema and retention |
| Assurance | Dry-run plan, input/candidate/action counts, keys/values/controls, differential tests, consumer checks |
| Lifecycle | Publication, rollback/forward repair, audit/lineage, retention/GC, cost report, incident follow-up |

## Learning Objectives

After completing this module, you should be able to:

1. classify the purpose and semantic axes of a backfill rather than equating it with rerunning dates;
2. define exact output ownership and derive complete input/dependency context for joins, windows, state, and references;
3. produce a deterministic manifest of immutable units, versions, candidates, checks, and operation identities;
4. choose correct unit boundaries, ordering, partition mapping, and idempotent retry behavior;
5. coordinate backfills with live ingestion, other writers, compaction, and schema work using fencing and conditional publication;
6. plan admission, concurrency, throttling, stop conditions, priority, cost, and dependency protection;
7. stage and validate a coherent candidate generation without exposing partial historical state;
8. distinguish scheduler/orchestrator capabilities from end-to-end data correctness guarantees;
9. test boundaries, failures, cancellation, unknown outcomes, version drift, rollback, and rebuild; and
10. assemble lineage, operational, security, and acceptance evidence for durable supersession.

## Core Exposition

### Classify the request

Name why historical materialization changes. A **fill** creates outputs never produced. A **repair** regenerates corrupt/missing outputs under the same intended semantics. A **logic migration** applies a new transformation. A **schema population** materializes a field or representation. A **source correction/restatement** applies newly authoritative facts. A **reproducibility replay** attempts the original result from original artifacts. A **recovery rebuild** restores derived state after loss.

The classification determines expected differences. A repair should match the old contract; a migration should differ in reviewed ways; a reproducibility replay should pin historical code/reference/runtime; a restatement may deliberately change accepted reports. Do not validate all categories with “new equals old.”

Create a new semantic request ID when source, scope, code, reference policy, schema, or correction authority changes. Physical retries retain the same request/unit operation keys. Reusing an old request ID after altering meaning makes receipts and comparisons ambiguous.

### Define output ownership exactly

Start with the target grain and logical key. A time range alone is insufficient for a tenant/day target: include tenant set and any scenario/model/version dimension. For ranges, prefer half-open $[start,end)$ under an explicit time zone/calendar/precision. Enumerate expected units before launch.

Output ownership $U$ is what may be replaced. Context rows outside $U$ are read-only. If the candidate includes context-only rows and dynamic overwrite infers replacement scope from emitted data, it can overwrite valid neighboring output. Project/write only owned keys and verify candidate key set is exactly (or a declared subset of) $U$.

Some units are sparse. “Every calendar day” differs from “every source partition that exists.” Record whether an empty output is an expected successful unit, an absent source, or an error. An empty candidate must not automatically mean delete the existing unit.

### Derive context and affected closure

Trace lineage from owned output backward to all inputs and forward to all outputs affected by the change. For a trailing $w$-day window over output days $[a,b)$, direct input context may begin at $a-(w-1)$ while output ownership remains $[a,b)$. Centered windows need both sides. Session windows can have data-dependent reach.

Joins require the correct reference cut and all rows capable of matching owned facts. Filtering both sides to the same date is unsafe when dimensions are not time-partitioned that way. Valid-time joins require interval versions spanning fact event times. “Current dimension” recomputation intentionally uses as-now state and must be labeled as such.

Cumulative/recursive state needs a seed immediately before $U$ or recomputation from an earlier trustworthy checkpoint. A correction can influence every later cumulative output. Either expand $U$ through the dependency closure, rebuild a new generation, or prove a state-delta propagation mechanism.

Partition mapping can be one-to-one, many-to-one, one-to-many, or dynamic. Materializing one monthly output may require all daily inputs; one input day may affect several feature windows; tenant sharding may not align across parents. Store mapping/version in the manifest rather than deriving it from filename conventions at runtime.

### Freeze reproducible inputs and semantics

Bind every input to an immutable snapshot, object version/digest, log interval, or transaction-consistent cut. A live table name is not a historical source identity. If source cannot time travel, copy/manifest the required state before running, or state that the result is an as-now recomputation rather than faithful historical replay.

Pin transformation source SHA/digest, compiled SQL, configuration/feature flags, schema contracts, dependency packages, adapter/engine/container/runtime, locale/time-zone database, and reference generations. Current mutable secrets may be necessary for access, but their privileges and endpoint identities belong in evidence; never persist secret values.

Define the semantic axes independently:

- fact/source state: original cut, corrected historical cut, or current reconstruction;
- reference state: as-was at event time, original load-time, or as-now;
- transformation: original version or new version;
- output contract/schema: old compatible form, expanded dual form, or new generation; and
- runtime: reproduced historical environment or approved current implementation.

Mixing axes may be intentional, but must have a name and acceptance oracle.

### Build a deterministic manifest and dry run

The manifest records request ID, unit keys/bounds, source/reference identities, dependency/context bounds, code/config/schema/runtime, expected target base/fence, candidate paths, operation keys, resource class, checks, and downstream scope. Sign or content-address it when tamper evidence matters.

A dry run expands the exact unit graph without executing mutations. It shows existing successful/in-progress/failed units; units eligible for reprocessing; estimated rows/bytes/files/scans/writes; expected dependency calls; conflicts with retention or schema; ordering; concurrency; cost; and candidate/publication destinations.

Airflow's backfill facility creates past scheduled runs over dates and exposes reprocessing behavior, concurrency, ordering, and dry run. Dagster models backfills over asset/job partitions and can execute partitions across one or multiple runs. These are valuable controls, but neither tool can infer your source truth, halo, target ownership, or safe write semantics. Encode those in data contracts and unit code.

### Choose units, order, and dependencies

Units should be independently retryable, bounded, and observably complete. Too small creates scheduler/catalog/file overhead; too large creates long retries, transactions, spill, and poor isolation. Size from measured source/output bytes, skew, runtime, locks/logs, and commit costs, not a fixed “one day” rule.

Use chronological order when each unit consumes prior output state or when it minimizes catch-up complexity. Reverse order can restore the most recent business-visible periods first when units are independent; Airflow exposes such ordering as a mechanism. Parallel order is safe only when ownership and dependencies are disjoint or explicitly coordinated.

Represent dependencies between units as a DAG. Do not rely on launch order alone. A downstream monthly unit should start only after all required daily candidate units validate, unless it deliberately reads the old trusted generation and will be recomputed again.

An indexed batch system can map a fixed manifest unit to an execution index. Kubernetes documents that more than one Pod may start for the same Job index, so each attempt still needs isolated output and idempotent/manifest-selected effects. Controller completion is not exactly-once execution.

### Make each unit replay-safe

Derive a stable operation key from request identity plus logical unit, target, and semantic manifest digest. Attempts get separate attempt IDs. A matching completed receipt can return the recorded result; the same operation key with a different manifest/digest fails closed.

Prefer deterministic replacement of the exact owned unit, versioned merge, or immutable candidate objects. Append is safe only for unique event/effect identities. External effects—notifications, exports, billing, cache invalidations—need separate idempotency/outbox/receipt protocols or should occur once after whole-generation publication.

Write attempt-specific outputs, never a shared mutable “day=…” location from several retries. A unit receipt records input identities, candidate objects/digests, row/key/control values, runtime, and terminal outcome. The request manifest selects one accepted attempt for each expected unit.

If an acknowledgement is lost, inspect target snapshot/transaction and receipt state. Retrying because the orchestrator says failed can duplicate a committed effect. Conversely, marking success based only on object existence can accept a truncated or stale attempt.

### Isolate candidates from production

For small transactional targets, one transaction may replace an exact unit and record its receipt. Large multi-unit requests usually need shadow tables/schemas/branches/generations. All units write candidate state; consumers continue reading the old trusted generation.

The candidate manifest must contain exactly the expected unit set and one accepted attempt per unit, plus schema, input/output counts/digests, rejects, and validation. Do not publish because the number of files happens to match; prove logical ownership and occurrence/key conservation.

Apache Iceberg documents branches/tags and an audit-branch workflow in which writes occur on an independent branch, validation precedes fast-forward, and snapshot references have retention rules. This is one implementation of write-audit-publish, not a universal substitute for backfill semantics. Schema selection and concurrent branch ancestry still require care.

For a mutable in-place target, readers may observe mixed versions unless transactions cover the whole request or a version column/view pointer filters to one generation. Updating a `logic_version` column unit by unit does not help if readers omit the filter.

### Coordinate with live and concurrent work

Choose a coexistence protocol before launch:

- **pause and fence live writes:** simplest semantics, but consumes freshness/downtime budget;
- **shadow from frozen cut, catch up, cut over:** strongest isolation for large migration, with extra storage and catch-up complexity;
- **version-aware merge:** live and backfill overlap per key, accepting only newer authoritative versions;
- **disjoint ownership:** backfill and live own provably separate units, with a catalog commit that composes both; or
- **serialize requests:** target-side lease/fencing token or queue prevents overlapping backfills/compaction/schema changes.

A lease without fencing is advisory. A paused/expired holder can resume and write after a new holder. Include a monotonically increasing fencing token or expected target generation in writes/publication.

Snapshot isolation can provide a stable read but does not automatically prevent a stale write from erasing later output. Serializable transactions may abort conflicting work; retry the whole transaction from fresh state. Table catalogs may reject optimistic conflicts; classify/rebase rather than blindly retry old candidate metadata.

Schema changes during a long backfill can invalidate candidate compatibility. Freeze/pin schema or use an expand-contract window that both old/live and backfill writers/readers support. Do not contract until the candidate, catch-up, rollback window, and old workers are finished.

### Protect live service and dependencies

Backfills enter through admission control with owner, budget, time window, priority, resource class, maximum concurrency, rate, duration, retry, and stop conditions. Reserve capacity for live freshness and interactive workloads. Separate pools/queues/warehouses can isolate some resources but shared sources, catalogs, networks, and destinations remain coupled.

Monitor database CPU/I/O, locks, WAL/redo and replica lag; warehouse slots/queues/spill/credits; object-store requests/listing/errors; catalog commit latency/conflicts; source API quota/rate limit; network; worker memory/disk; output file/metadata growth; and live pipeline lag/error. Throttle on the first constrained dependency, not only backfill worker CPU.

Use bounded concurrency with feedback. Increasing workers can increase contention and make completion slower. Hot tenants/partitions require weights rather than one-unit-one-slot fairness. Retry storms need jitter/backoff and a global budget; deterministic data errors should quarantine/stop rather than consume transient retries.

Define automatic pause/abort conditions: live freshness/error SLO breach, source retention danger, replication lag, lock timeout/deadlock rate, cost ceiling, unexpected scan/rewrite amplification, validation drift, catalog conflict, storage headroom, or security incident. Pause should prevent new units and let safe in-flight boundaries finish; cancel must record which attempts/effects exist.

### Validate at unit and generation levels

Before execution validate manifest/schema, source/reference reachability and retention, expected unit set, input coverage, code artifact, target base, permissions, capacity, and dry-run estimates. Fail before mutation if a required historical object/schema/reference is gone.

Per-unit validation checks exact input objects/cuts, context bounds, output ownership, schema, keys/multiplicity, null/domain distributions, counts, sums and components, rejects, business invariants, deterministic retry, and candidate digest. Empty units require explicit expected-empty evidence.

Generation validation checks all expected units exactly once; no extra/gap/overlap; cross-unit/global uniqueness; boundary continuity; aggregate components; referential integrity; downstream compatibility; unchanged outside $U$; expected old/new differences; and comparison with a full independent oracle or trusted controls at the same cut.

Row counts alone miss offsetting omissions/duplicates, wrong keys, stale versions, misclassified deletes, and wrong values. Totals alone miss compensating changes. Compare both set differences, per-key values/versions, distributions, and domain questions. Sample only where complete checks are infeasible, and state detection limits.

### Publish, catch up, and supersede

Before publication, freeze or observe the current target generation. If it differs from the planned base, evaluate whether candidate ownership is disjoint and composable; otherwise rebase/recompute. Never overwrite newer live state merely because the historical run started first.

For shadow migration, capture changes after source cut $c$, apply the catch-up interval through cut $d$, validate again, briefly fence if needed, then atomically/conditionally switch the trusted pointer. Bind request/manifest, source/reference cuts, code/schema/runtime, checks, candidate snapshot, prior generation, and rollback reference.

Downstream models, caches, indexes, extracts, features, and reports may need their own affected-set backfills. Publish lineage/supersession events and schedule downstream work from the accepted upstream generation, not from task completion. Avoid simultaneous partial propagation through the graph.

Keep the prior generation and required source/candidate evidence through an observation/acceptance window. Semantic rollback can restore the pointer only if downstream/external effects are compatible; otherwise use forward correction and explicitly reconcile irreversible exports/messages.

### Operate pause, resume, cancellation, and recovery

Pause stops admission of new units while recording in-flight state. Resume revalidates source retention, code/config/schema, target base/fence, credentials, capacity, and existing receipts; it does not assume yesterday's environment remains compatible.

Cancellation has a state machine: requested, admission stopped, workers signaled, in-flight transactions resolved, candidate attempts inventoried, trusted publication checked, external effects reconciled, terminal canceled/failed state recorded. Deleting scheduler runs or candidate files first destroys evidence needed for safe resolution.

On partial failure, retry failed units only when the same semantic manifest remains valid. A source object replacement, code/config change, target rebase, or correction may require a new candidate generation or new request. Preserve successful immutable candidates if their premises still hold.

Disaster recovery tests should rebuild the coordinator/manifest/receipt state, not merely restart workers. Prove that accepted units, missing units, ambiguous attempts, and publication outcome can be derived from durable evidence after loss of orchestrator metadata.

### Govern lineage, security, retention, and cost

Lineage needs job definition and version, unique run/request/attempt identities, input/output dataset namespaces/versions, partition/key ranges, source/reference cuts, and supersession relationship. OpenLineage's Job/Run/Dataset model and dataset version/partition facets provide a vocabulary; the backfill-specific request and ownership evidence still must be modeled.

Historical data can be more sensitive than current data. Old before-images, deleted subjects, expired consent, or prior tenant assignments may be legally restricted. Obtain purpose/authority, minimize columns and scope, use dedicated least-privilege roles, encrypt temporary candidates, isolate tenants, audit reads/writes, redact logs/rejects, and delete temporary copies under approved retention.

Backfill retention must cover raw inputs, schemas, reference history, tombstones/dedup receipts, code/config/runtime, candidate/prior snapshots, validation, and operation receipts until acceptance, replay, audit, and rollback obligations end. Coordinate snapshot expiration/vacuum/garbage collection; otherwise cleanup can invalidate a running request or its rollback.

Estimate and record scan, compute, shuffle, write/rewrite, catalog, storage, egress, API, and human-review cost. Compare actual to plan per unit and revise remaining forecast. Cost variance can indicate a semantic defect such as missing pruning or unexpected dependency fanout, not merely a billing issue.

## Definitions and Notation

Let:

- $K$ be the logical output-key domain;
- $O_g:K\rightharpoonup V$ be trusted output generation $g$;
- $U\subseteq K$ be the exact output ownership set for the request;
- $C(U)$ be the transitive input/reference/state context needed to compute $U$;
- $S_c,R_c$ be immutable source and reference states at cut $c$;
- $F_v$ be transformation/contract version $v$;
- $B_U=F_v(S_c,R_c)\restriction_U$ be candidate output;
- $U_1,\ldots,U_n$ be retryable output units whose bag/set ownership is disjoint and complete;
- $q$ be the request identity, $op(q,U_i)$ a stable unit operation key, and $a_{ij}$ a physical attempt;
- $M_q$ be the final candidate/receipt manifest; and
- $P_g$ be the trusted publication pointer/checkpoint for generation $g$.

Output replacement is exact:

$$
replace(O_g,U,B_U)(k)=
\begin{cases}
B_U(k), & k\in U;\\
O_g(k), & k\notin U.
\end{cases}
$$

This requires candidate behavior for missing owned keys: delete, explicit empty, retain, or reject must be declared. A partial candidate cannot silently substitute for $B_U$.

Context and ownership differ:

$$
U\subseteq K_{output},\qquad C(U)\subseteq K_{inputs}\cup K_{references}\cup K_{state},
$$

and neither containment direction between their labels is generally meaningful. Context may precede/follow time-owned output, include all dimension rows, or use a prior checkpoint.

For half-open daily output intervals $U=[a,b)$ and trailing window width $w$ days, a simple direct context is

$$
C(U)=[a-(w-1),b).
$$

The extra left interval is read-only halo. Sessionization, recursion, and data-dependent joins can require wider or unbounded closure; do not force them into this formula.

Manifest completeness requires

$$
\biguplus_{i=1}^{n}U_i=U
$$

and exactly one accepted attempt receipt for each $U_i$. Physical attempts may overlap because retries/speculation occur, but accepted logical ownership may not.

Publication from expected base $g$ is a compare-and-swap:

$$
CAS(P_g=g,\;P:=g+1,M_q).
$$

Failure means target state changed; it does not mean the candidate is wrong, only that its publication premise must be reevaluated. Rebase is valid when recomputation/version reconciliation proves candidate composition with the new base.

Let actual unit resource vector be $r_i=(cpu,memory,scan,write,locks,redo,api,cost)$. Admission chooses concurrency so aggregate demand remains inside declared dependency envelopes. This is an empirical capacity constraint, not a fixed formula; skew and retries make averages insufficient.

“Complete” has levels: attempt finished, unit candidate validated, every request unit accepted, generation globally validated, production published, downstream closure refreshed, and owner acceptance observed. Record them separately. A green scheduler run proves only its own terminal state.

## Mechanisms, Invariants, or Proof Structure

Use this operational state machine:

1. **Proposed:** owner states intent, semantic axes, exact output scope, source of truth, downstream effects, deadline, and risk.
2. **Planned:** immutable manifest expands $U$, $C(U)$, units/dependencies, versions, capacity/cost, validation, publication, and rollback.
3. **Admitted:** dry run and reviews pass; target fence/base and resource budgets are reserved.
4. **Running:** attempts consume fixed units, write isolated candidates, emit receipts, and obey feedback throttles/stop conditions.
5. **Candidate complete:** manifest selects one validated attempt per unit and proves exact ownership coverage.
6. **Validated:** generation/global/downstream/security checks pass and expected differences are approved.
7. **Published:** conditional pointer/transaction exposes one generation and binds checkpoint/lineage/supersession.
8. **Observed:** live and downstream behavior meet the acceptance window; prior generation remains available.
9. **Closed:** owner accepts, temporary candidates expire under policy, and cost/incident evidence is retained.

Retries do not change semantic identity. If attempt $a_{i1}$ fails after writing candidate objects, attempt $a_{i2}$ uses the same $op(q,U_i)$ but separate paths/receipt. The manifest accepts at most one. If both finish, equality checks can support reuse, but selecting both would duplicate output.

The preservation proof follows from exact ownership. For $k\notin U$, replacement chooses $O_g(k)$, so candidate work cannot change unowned output. For $k\in U$, validation proves $B_U(k)=F_v(S_c,R_c)(k)$ under the declared equivalence. Therefore the published generation changes exactly the intended region. This proof fails if dynamic overwrite infers a broader region, if missing candidate keys silently retain/delete contrary to policy, or if a stale base overwrites concurrent work.

The reference model below demonstrates trailing-window context, isolated ownership, a rejected stale-base publication, safe rebase that preserves a newer unowned live output, and idempotent replay. It intentionally excludes distributed scheduling, source mutation, schema/reference changes, unbounded sessions, target transactions, resource pressure, and real catalog behavior.

<!-- bijux-verify: {"id":"backfill-owned-range-reference-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"owned_days=(4, 5, 6)\ncontext_days=(2, 3, 4, 5, 6)\ncandidate=((4, 90), (5, 120), (6, 150))\nstale_base_rejected=True\npublished_generation=14\noutside_preserved=True\nowned_equivalent=True\nreplay_stable=True\n","stderr":""}} -->
```python
source = {day: day * 10 for day in range(1, 9)}
owned = (4, 5, 6)


def trailing_three(day):
    return sum(source[d] for d in range(day - 2, day + 1))


context = tuple(range(min(owned) - 2, max(owned) + 1))
candidate = {day: trailing_three(day) for day in owned}

# Generation 12 contains the old two-day logic.
base = {
    day: sum(source[d] for d in range(max(1, day - 1), day + 1))
    for day in source
}


def publish(current_generation, expected_generation, current, patch, ownership):
    if current_generation != expected_generation:
        raise ValueError("stale base generation")
    if set(patch) != set(ownership):
        raise ValueError("candidate ownership mismatch")
    output = dict(current)
    output.update(patch)
    return current_generation + 1, output


# Live processing advances to generation 13 and fixes day 8 while the backfill runs.
latest = dict(base)
latest[8] = trailing_three(8)

try:
    publish(13, 12, latest, candidate, owned)
    stale_rejected = False
except ValueError:
    stale_rejected = True

# Rebase on 13, replacing only owned days, then publish generation 14.
generation, result = publish(13, 13, latest, candidate, owned)
_, replayed = publish(generation, generation, result, candidate, owned)
outside = set(result) - set(owned)

print(f"owned_days={owned}")
print(f"context_days={context}")
print(f"candidate={tuple(sorted(candidate.items()))}")
print(f"stale_base_rejected={stale_rejected}")
print(f"published_generation={generation}")
print(f"outside_preserved={all(result[d] == latest[d] for d in outside)}")
print(f"owned_equivalent={all(result[d] == trailing_three(d) for d in owned)}")
print(f"replay_stable={replayed == result}")
```

The code reads days 2–6 but writes 4–6. Day 2 and day 3 are context, not permission to replace those outputs. The initial publication attempt is rejected because the trusted generation is 13 rather than expected 12. Rebase preserves live-corrected day 8 because it lies outside $U$. Reapplying absolute owned values is stable.

In a real system, rebase also revalidates input/reference cuts, target schema, overlapping entity/output versions, downstream state, and table/file conflicts. If the candidate computation itself depends on target generation or live reference state, simple patch reuse may be invalid and recomputation is required.

## Alternatives and Trade-Offs

| Approach | Best fit | Strength | Main risk or obligation |
|---|---|---|---|
| In-place unit replacement | Small disjoint units and transactional target | Low temporary storage | Mixed-version visibility across many units; exact delete/ownership semantics |
| Version-aware row merge | Overlap with live per-key changes | Can preserve newer rows | Authoritative comparable versions, tombstones, uniqueness, concurrency |
| Shadow table/schema | Large logic/schema migration | Full validation and easy pointer cutover | Storage, catch-up, grants/consumers, long build |
| Table-format branch/WAP | Snapshot-capable governed table | Isolated lineage and atomic reference change | Branch/schema/ancestry/conflict/retention semantics are implementation-specific |
| Full generation rebuild | Broad dependency or logic change | Simple whole-state equivalence | Highest scan/write/time/cost; catch-up needed |
| Partition-by-partition overwrite | Natural exact independent output partitions | Bounded retries and workload | Partial visibility unless versioned pointer; context/ownership confusion |
| Event replay into idempotent sinks | Immutable source events and stateful consumers | Preserves source history and ordering | State bootstrap, duplicates, side effects, replay horizon |
| Historical-code replay | Audit/reproducibility question | Tests original reproducibility | Old dependencies/schema/security may be unavailable or unsafe |
| Current-code restatement | Approved new historical meaning | Uniform new semantics | Comparability changes; needs owner acceptance and downstream supersession |
| Pause live and rebuild | Short workload/freshness tolerance | Simplest coexistence | Downtime/freshness gap and catch-up capacity |

Do not choose shadow versus in-place solely by table size. Consider reader version filtering, atomic pointer facilities, downstream coupling, source retention, live write rate, rollback, privacy, and available temporary capacity. A small but high-stakes table may justify a shadow generation; a huge append-only table may support exact partition replacement safely.

Unit granularity trades retry cost against coordination overhead. Ten thousand tiny daily/tenant jobs can overwhelm schedulers and catalogs. One annual job can fail after hours and monopolize resources. Group units without losing internal ownership/receipt visibility.

Run direction is a policy choice. Recent-first improves urgent current reports but can violate cumulative dependencies. Oldest-first supports sequential state but delays current correction. Dependency-aware waves or shadow full generation may resolve the conflict.

Reusing original code can improve reproducibility but preserve known bugs and depend on vulnerable/unavailable runtimes. Porting semantics to a supported runtime requires a differential oracle and an explicit claim: semantic reproduction, not binary replay.

## Failure Modes and Misconceptions

**“Backfill means run the DAG for old dates.”** Scheduler logical dates do not define source cuts, output keys, reference versions, code, or safe writes. A backfill request/manifest must.

**“The selected date range is the complete scope.”** Windows, joins, state, and downstream dependencies expand context or affected output. Trace both directions.

**“Read and write the same partitions.”** Halo/context partitions are often read-only. Writing them can overwrite correct neighboring data.

**“The current source reconstructs history.”** Mutable source tables and current dimensions may have lost prior versions. Label as-now reconstruction or stop if as-was evidence is required.

**“Use the newest code because it is best.”** The question may be reproducibility under old semantics. Choose code/reference/schema axes explicitly.

**“Successful old runs need no reprocessing.”** A run can be green while output is absent, corrupt, or generated under superseded logic. Inspect dataset generation evidence, not run state alone.

**“Clear every old run and retry.”** This can lose receipts, duplicate committed effects, and remove diagnostic evidence. Create a governed new request/supersession.

**“One run per day guarantees isolation.”** Days may share windows, state, dimension changes, files, or target commits. Logical dependencies matter.

**“The scheduler runs each unit once.”** Workers can retry or duplicate. Kubernetes explicitly notes more than one Pod can start for one Job index. Sink effects must be replay-safe.

**“More parallelism finishes faster.”** Shared source, database, warehouse, catalog, and storage contention can reduce throughput and damage live SLOs.

**“A lease prevents stale writes.”** Without fencing/expected-generation enforcement, an expired holder can resume after replacement and still mutate data.

**“Snapshot read prevents lost updates.”** Stable reads do not by themselves prevent a stale candidate from overwriting a newer target generation.

**“Per-partition atomicity gives all-or-nothing backfill.”** Readers can observe a mixture unless publication selects one coherent generation.

**“Empty candidate means delete the partition.”** Empty can reflect legitimate no rows, missing source, wrong filter, lost permissions, or failure. Require explicit completeness evidence and policy.

**“Matching total proves the backfill.”** Omissions/duplicates or category movements can offset. Compare keys, multiplicities, versions, values, deletes, components, and domain questions.

**“Cancel means nothing else happened.”** In-flight or ambiguously acknowledged units may have committed. Resolve receipts and target truth.

**“Rollback restores everything.”** Downstream exports, notifications, caches, or consumed events may be irreversible; reconcile or forward-correct them.

**“Delete candidates immediately to save cost.”** Acceptance, rollback, audit, and ambiguous-outcome resolution require retained evidence under a declared lifecycle.

## Worked Examples

### Example 1

A trailing seven-day revenue model must replace outputs March 10–12. It reads facts March 4–12 and the full customer-reference versions valid over those events, but writes only output dates 10–12. The manifest labels March 4–9 as context. Tests compare exact outputs for 10–12 and prove all other output partitions remain byte/logically unchanged.

### Example 2

A local-time daily report backfills `2026-11-01` in `America/New_York`, a 25-hour fall-back day. The request names local calendar boundaries and their two UTC offsets, uses half-open instants, and tests both 01:30 occurrences. A naive 24-hour UTC slice would omit an hour or assign it to the next day.

### Example 3

A new `country_normalized` column can be populated from authoritative event-time address history for only 70% of old rows. The backfill writes normalized value plus provenance where evidence exists and explicit unknown elsewhere; it does not fill current country into all history. Acceptance compares known/unknown distributions and does not falsely enforce non-null.

### Example 4

An Airflow backfill dry run lists 365 historical logical dates. The data manifest contains 360 expected output units because five market holidays intentionally have no unit. The team uses the governed unit manifest rather than assuming scheduler-date count is source completeness; expected-empty/absent semantics are documented.

### Example 5

A cumulative account balance is wrong starting at day 20. Recomputing day 20 alone is insufficient; every later balance depends on it. The request either owns days 20 through current using the trusted day-19 closing seed, or rebuilds from the last verified checkpoint. Units run chronologically and reconcile opening/closing conservation.

### Example 6

A two-year shadow rebuild starts at source cut 500. Live ingestion continues to cut 620. After base validation, the pipeline applies change interval `(500,620]`, fences briefly at 625, applies `(620,625]`, revalidates, and conditionally switches the pointer. Both intervals use stable occurrence identity so boundary overlap is harmless and gaps are prohibited.

### Example 7

Two backfills want tenant A/day 8. Request X applies corrected facts at source version 12; request Y applies new logic to version 11 facts. A simple queue order could let Y overwrite X. Governance resolves semantic precedence, or a composed request applies new logic to version 12. Output lineage records both superseded requests.

### Example 8

Increasing concurrency from 20 to 100 workers raises warehouse queue time, catalog conflicts, source replica lag, and retry volume; throughput falls. A feedback controller reduces admission to 12, reserves slots for live ingestion, and pauses if replica lag approaches WAL retention headroom. Completion is slower but bounded and recoverable.

### Example 9

An indexed batch launches duplicate attempts for unit 42 after a node failure. Both write isolated candidate prefixes. Their content digests match; the manifest selects the first validated receipt and garbage-collects the other after acceptance. No task writes directly to the trusted output prefix.

### Example 10

A request is canceled after 997 of 1,000 candidates validate and the catalog commit response times out. Operators first query the trusted pointer and publication receipt. If the new generation is current, cancellation cannot imply rollback; they move to observation or explicitly restore the prior pointer and reconcile downstream effects. If not published, they retain candidates for diagnosis/reuse under policy.

## Cross-Program Connections

[Database Engineering](../../18-database-engineering/ROADMAP.md) supplies snapshots, time travel, transactions, isolation, locks, versioned upserts, bulk updates, indexes, logs/replication, schema migrations, and rollback mechanics.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) connects immutable logs, offsets/epochs, at-least-once execution, idempotence, leases/fencing, compare-and-swap, ambiguous commits, state transfer, and recovery.

[Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) connects interval algebra, dependency closure, DAG scheduling, partitioning, stable reduction, incremental algorithms, graph reachability, and complexity/cost bounds.

[Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) connects migration patterns, units of work, commands, receipts/outbox, resumable workflows, sagas, configuration versioning, and rollback/forward repair.

[Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) connects differential/oracle testing, boundary analysis, property/model-based tests, fault injection, mutation tests, concurrency schedules, and evidence limits.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects requirements/acceptance, configuration control, hazards, capacity/admission, change review, stop conditions, incident command, verification, and lifecycle disposal.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) connects batch job primitives, schedulers, workload queues, quotas, policy, data/catalog services, secrets, observability, cost allocation, and paved-road backfill controls.

[Security Engineering](../../25-security-engineering/ROADMAP.md) connects purpose limitation, least privilege, tenant isolation, historical/deleted data, audit integrity, temporary-copy retention, key management, and incident response.

## References

1. Apache Airflow, [Backfill](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/backfill.html). Documents past scheduled-run creation, reprocessing behavior, independent concurrency limits, reverse ordering, dry run, and partitioned DAG backfills. Accessed 2026-09-02.
2. Dagster, [Backfilling Data](https://docs.dagster.io/guides/build/partitions-and-backfills/backfilling-data). Documents partition/asset backfill selection, launch, monitoring, and single-run versus multi-run policies. Accessed 2026-09-02.
3. dbt Labs, [Microbatch Incremental Models](https://docs.getdbt.com/docs/build/incremental-microbatch). Documents event-time bounds, atomic/idempotent batches, targeted start/end backfills, retry, lookback, UTC assumptions, adapter-specific replacement, and upstream filtering. Accessed 2026-09-02.
4. Apache Iceberg, [Branching and Tagging](https://iceberg.apache.org/docs/latest/branching/). Documents snapshot lineages/references, retention, audit branches, validation before fast-forward, and schema behavior across branches/tags. Accessed 2026-09-02.
5. Apache Iceberg, [Spark Writes](https://iceberg.apache.org/docs/latest/spark-writes/). Documents explicit overwrite modes, branch writes, write-audit-publish configuration, merge/file rewrite behavior, and atomic overwrite operations. Accessed 2026-09-02.
6. Kubernetes, [Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/). Documents indexed work, parallelism/completions, per-index retries/failures, deadlines, terminal states, and the possibility of multiple Pods for one index. Accessed 2026-09-02.
7. PostgreSQL Global Development Group, [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html). Documents snapshot visibility, concurrent update behavior, serialization anomalies/failures, and whole-transaction retry requirements. Accessed 2026-09-02.
8. Apache Beam, [Programming Guide](https://beam.apache.org/documentation/programming-guide/#watermarks-and-late-data). Documents event versus processing time, windows, watermarks, late data, triggers, allowed lateness, and state lifecycle relevant to historical replay boundaries. Accessed 2026-09-02.
9. OpenLineage, [Object Model](https://openlineage.io/docs/spec/object-model/). Defines Job, Run, and Dataset identities plus source code, dataset version, partition, lifecycle, quality, and output-statistics facets useful for backfill lineage. Accessed 2026-09-02.

## Exercises

### Exercise 1

A trailing five-day metric must replace output days `[20,24)`—days 20, 21, 22, and 23. Derive the minimum direct source-day context under ordinary inclusive trailing windows. State the output ownership set and explain what may go wrong if every read day is dynamically overwritten.

### Exercise 2

A backfill request has 120 expected units. Execution records 123 successful physical attempts because three units were retried after lost acknowledgements; two intended units have no validated receipt, and two unexpected unit keys exist. Can the request publish? Specify the exact manifest checks and safe next actions.

### Exercise 3

A customer model originally used event-time tier history and code `v1`. The proposed historical rebuild uses code `v2` and today's customer tier table. Classify the possible semantic objectives and design evidence that prevents the result from being mislabeled as an as-was reproduction.

### Exercise 4

A live pipeline advances a table from generation 70 to 74 while a backfill candidate built from 70 owns partitions A and B. Live generation 74 changed B and C. Design publication/rebase behavior for the backfill. State when candidate A can be reused and why blindly overwriting A+B is unsafe.

### Exercise 5

A planned 1,000-unit backfill at concurrency 40 pushes source replica lag from 30 seconds to 18 minutes, live freshness beyond SLO, and retry rate from 1% to 20%. Design admission/throttling/stop behavior, resume criteria, and the operational evidence required before continuing.

## Answers to the Exercises

### Answer 1

For output day $d$, a trailing five-day window reads $[d-4,d]$. Across outputs 20–23, the union is source days 16 through 23 inclusive, or half-open day labels `[16,24)`. Thus output ownership is `{20,21,22,23}` while direct context is `{16,17,18,19,20,21,22,23}`.

Days 16–19 are context only. If candidate rows for every read day enter a dynamic overwrite, the job may replace outputs outside its authority with incomplete, old-logic, or context-shaped data. The writer projects exactly owned output keys, validates exact candidate ownership, and publishes replacement only for `[20,24)`.

### Answer 2

It cannot publish. Physical attempt success count is irrelevant to exact logical coverage. The manifest must enumerate precisely the 120 expected unit keys, show at least one validated candidate for each, select exactly one accepted attempt/receipt per unit, reject unexpected units, and prove selected candidates use the same request manifest/source/reference/code/schema/base. It also checks disjoint ownership, candidate digests, global schema/key controls, no gap/overlap, and publication fence.

Resolve the three ambiguous retry pairs from target/candidate/receipt evidence and select at most one each. Rerun or repair the two missing intended units under the same operation keys if their premises remain valid. Quarantine/remove the two unexpected keys from the candidate manifest after diagnosing manifest/worker mismatch; do not silently count them toward 120. Revalidate globally before publication.

### Answer 3

Possible objectives include: reproduce original outputs using `v1` plus original event-time tiers; repair original semantics under a supported reimplementation; apply `v2` logic to original event-time tiers; apply `v1` or `v2` to corrected historical tier versions; or intentionally restate history under today's tier (“as-now”). Code and reference-time axes are independent.

The request names the selected objective and expected differences, pins source cut, original/corrected/current reference generation, transformation/compiled SQL/runtime, schema, and target contract, and labels output lineage accordingly. For as-was reproduction, today's mutable tier table is disallowed unless proven identical for every relevant event time; use retained bitemporal/version history. Compare with original outputs and source controls, explain approved differences, and prevent the candidate from inheriting the old generation label if semantics differ.

### Answer 4

Publication against expected base 70 must fail because current is 74. Partition B overlaps a live change, so blindly replacing A+B can erase newer B. Partition C must remain unchanged in all cases.

If lineage proves A is disjoint from every 71–74 change, its source/reference/code/schema premises remain valid, and the target format supports composing its exact candidate, A can be reused. B must be recomputed/reconciled from generation 74 or applied with authoritative per-row versions that preserve newer state. Build a rebased candidate/manifest against expected 74, validate A/B and unchanged C, then conditionally publish 75. If dependencies couple A and B or target commits cannot safely compose selected files, recompute both from the new base.

### Answer 5

Pause admission immediately and let only safe in-flight unit boundaries resolve; the live freshness breach and 36× replica-lag increase satisfy stop conditions, while retry amplification indicates overload. Do not respond by launching replacements. Record in-flight/ambiguous receipts, throttle or cancel according to source-retention risk, and reserve capacity for live recovery.

Diagnose per-unit scans, query plans, locks, replica WAL/redo, concurrency, retry classes, and dependency limits. Resume only after live freshness and replica lag remain below recovery thresholds for a fresh observation window, source retention has headroom, ambiguous units reconcile, and a reduced concurrency/rate (possibly weighted by unit size) passes a canary wave. Use feedback control and automatic pause thresholds.

Evidence includes planned versus actual rows/bytes/runtime/cost per unit, replica lag and retention headroom, live/backfill queue/freshness/error time series, lock/I/O/CPU/log metrics, retry causes, canary throughput at new concurrency, source and target validation, remaining forecast/deadline, owner/incident approval, and updated runbook/manifest configuration.
