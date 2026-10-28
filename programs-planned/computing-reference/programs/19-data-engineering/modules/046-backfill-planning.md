---
module_id: DE-046
program: Data Engineering
level: 1
module_number: 46
title: Backfill Planning
status: complete
last_verified: 2026-09-03
---

# Backfill Planning

## One-Page Review

### Governing question

How should a team convert a historical data need into a finite, dependency-correct, capacity-safe, resumable, observable, and auditable execution plan that cannot silently damage live production data?

### Essential definitions

- A **backfill** is an intentional bounded historical materialization or rematerialization under explicit source, reference, transformation, schema, output, and publication semantics.
- A **backfill request** records purpose, owner, authority, target outputs, policy, risk, service impact, validation, publication, rollback, and expiry.
- A **selection predicate** is a typed expression over asset identities, partition keys, generations, states, and dimensions that resolves to an immutable target set.
- A **frozen selection** is the exact enumerated target set plus definition/spec versions and digest used for approval and execution.
- A **dependency closure** adds every prerequisite work/input needed to produce selected targets under exact partition mappings.
- A **work unit** is one independently identifiable, retryable, and dispositioned node in the backfill plan.
- A **plan DAG** is the finite dependency graph of work units, accepted inputs to reuse, validation gates, publication, and downstream actions.
- A **wave** is a dependency-ready subset admitted together within resource, risk, and concurrency budgets.
- A **pilot** or **canary slice** is a representative bounded subset whose results and operating evidence gate wider execution.
- A **capacity envelope** bounds scan/read/write/compute, slots/concurrency, metadata, external calls, storage, cost, and live-work impact.
- A **stop condition** is a machine-evaluable safety threshold that pauses admission while preserving state for diagnosis.
- A **backfill checkpoint** records immutable plan/version, per-unit state/outcome, next eligible work, budgets, and reconciliation evidence so resume does not reinterpret scope.
- A **live head** is the current near-real-time production horizon protected from accidental historical selection and stale publication.

### Central model, mechanism, or theorem

Let approved target output keys be finite set $T$. Under versioned dependency mapping $M$, required closure is

$$
C(T)=T\cup\bigcup_{x\in T}M^*(x),
$$

partitioned into accepted reusable inputs $R$, planned work $W=C(T)\setminus R$, and terminal exclusions with explicit evidence. The plan graph $G_W=(W,E_W)$ must be acyclic. A wave $Q_i$ may be admitted only when all predecessors are accepted and resource vector sum stays within envelope $B_i$:

$$
\forall r:\sum_{w\in Q_i}cost_r(w)\le B_{i,r}.
$$

Coverage at completion requires every frozen target to have one accepted intended generation or an explicitly authorized non-success disposition, while no key outside the ownership set is replaced. Plan identity binds target digest, closure/mapping, input cuts, code/config/schema, base generation, policy, and approvals. Replanning any of these creates a new revision rather than mutating execution history.

### Critical invariants

- Purpose, semantic mode (`as-was`, `as-now`, correction, migration, recovery), owner, approval, expiry, target consumers, and success criteria are explicit.
- Selection syntax is typed, bounded, previewed, authorized, and frozen to exact asset/spec/partition/generation identities before work begins.
- Output ownership set and dependency/input closure are distinct; window halos, joins, reference history, prior state, and downstream invalidation are complete.
- Plan DAG is finite, acyclic, versioned, digestible, and deterministic from its frozen inputs and planner version.
- Existing accepted prerequisites are reused only after compatibility, quality, freshness, retention, and lineage checks; target outputs are not accidentally treated as reusable when replacement is required.
- Live schedules, corrections, schema changes, compaction, retention, and other backfills are isolated, serialized, fenced, or governed by explicit rebase rules.
- Admission respects multi-resource capacity, quotas, priority, fairness, retry amplification, cost, and live-work reservation—not only worker count.
- Pilot selection exercises representative size, age, schema/spec versions, skew, emptiness, joins, corrections, and sensitive cases before expansion.
- Stop, pause, resume, cancel, retry, replan, supersede, rollback/forward repair, and manual override have durable state and authorization.
- Each attempt writes isolated candidates; acceptance and publication use DE-044/DE-045 identity, validation, and fencing rules.
- Progress denominators use the frozen planned target/work sets and distinguish queued, blocked, running, candidate, accepted, failed, skipped, superseded, unknown, and cancelled.
- Completion reconciles plan, attempts, receipts, candidate and accepted generations, unchanged-outside-scope evidence, downstream state, consumer freshness, cost, and cleanup.

### Common failures

Accepting “last quarter” without time role or zone; executing a mutable query instead of freezing keys; selecting output dates but omitting rolling-window context; using today's mutable dimension values for an as-was reconstruction; selecting graph nodes with an ambiguous operator; treating all upstream history as work instead of reusing compatible accepted generations; starting newest-first when state is sequential; placing every partition in one wave; measuring only CPU while saturating source, warehouse logs, object listing, or catalog; using retries that multiply capacity; running the pilot only on tiny clean recent data; writing directly into live partitions; clearing task state as a backfill protocol; changing code/config mid-plan; reporting percent from discovered/completed tasks; treating cancel as rollback; allowing a stale plan to publish after live corrections; deleting candidates before uncertainty is reconciled; and declaring success because the orchestrator is green.

### Compact example

A request targets rolling outputs for September 3–4. Each rolling key needs three daily aggregates. September 1 aggregate is already accepted and compatible; aggregates September 2–4 must be materialized. The dependency-closed plan has five work units. With capacity 8, deterministic ready-set packing yields waves costing 7, 8, and 2. The current live head September 5 is absent from the frozen target and closure. All dependencies are satisfied by planned predecessors or the reused September 1 generation. **Conclusion:** a backfill is an immutable dependency/capacity plan, not a loop over dates.

### Connections

[DE-037](037-backfills.md) establishes historical computation, input-cut, validation, isolation, and publication correctness. [DE-041](041-directed-acyclic-graphs-and-dependencies.md) through [DE-045](045-partitioned-assets.md) supply graph, work identity, scheduling, retry, and partition inventory. This module turns those semantics into an executable control-plane plan. DE-047 and DE-048 next protect environment parameters and delivery; DE-049 records operational state.

## Governing Question

Given a historical intent, how can planners prove the exact output ownership set, dependency closure, semantic versions, execution order, capacity envelope, safety gates, and terminal evidence before allowing any attempt to modify trusted data?

The word backfill covers different intents. Filling never-produced partitions, repairing an incident, recomputing with corrected source data, applying a new business rule, migrating a schema, rebuilding after disaster, and replaying a historical event log may target the same dates but require different source cuts, code, reference semantics, lineage, consumer communication, and publication policy. Name the intent first.

DE-037 describes what makes the historical computation itself correct: exact output scope, larger input context, immutable source/reference versions, shadow generation, validation, and fenced publication. DE-046 focuses on the planner/control plane. It determines what finite work exists, which dependencies can be reused, in what order and batch size work may run, how live traffic is protected, how pilots and stop conditions gate expansion, and how progress/resume remain stable over days or weeks.

A plan is a durable proposal, not an imperative shell loop. It should be inspectable before execution, signed/approved according to risk, reproducible from pinned inputs, immutable once admitted, and superseded by explicit revision. The same plan powers dry-run cost estimation, authorization, scheduling, observability, and final reconciliation.

The planner must resist convenient ambiguity. Relative times move. “Failed partitions” changes while queried. A graph selection expression can include unintended descendants. Current reference data can rewrite history. One concurrency integer cannot bound heterogeneous resource pressure. A robust plan turns all these into concrete identities, sets, constraints, and evidence.

## Why This Matters

Backfills concentrate risk. They deliberately revisit large historical ranges, often when an incident or business deadline creates urgency. They can read cold storage, reconstruct old schemas, produce unusually large shuffles, contend with live ingestion, invalidate caches, trigger downstream workflows, duplicate external effects, and replace data consumers already trust.

Scope errors scale mechanically. A one-day off-by-one in a daily job becomes 90 wrong partitions over a quarter. An unconstrained graph selector can include every descendant. A missing tenant predicate can cross security boundaries. A rolling metric may require a halo before the selected output interval and may invalidate outputs after it. Previewing exact keys and closure is therefore a correctness and authorization gate.

Capacity mistakes cause secondary incidents. Historical work can saturate source APIs, database replicas, warehouse slots, transaction logs, broker partitions, object-store request rates, metadata/catalog services, network egress, and downstream services. Autoscaling more workers often makes the constrained dependency worse. Retry storms increase demand during failure. Reserve capacity for the live path and use feedback/stop conditions rather than a one-time worker-count guess.

Long plans experience change. New live generations arrive; code deploys; schemas evolve; credentials rotate; retention removes inputs; incidents shift priority; estimates prove wrong; a correction targets the same key. If the plan silently re-resolves “latest” or reloads its selection, it ceases to be the approved operation. Immutable plan revisions and fences make such changes explicit.

Operational state can mislead. One task might materialize ten partition keys; one key may require several tasks; retries add attempts; accepted-empty outputs are successful; a green compute attempt may lose publication; cancellation may leave committed effects. Progress must be based on the frozen logical denominator and accepted outcomes, with task/attempt counts as separate diagnostics.

Pilots reduce uncertainty only when representative. Running one tiny recent partition says little about old schema versions, sparse/empty periods, large tenants, skewed joins, deleted references, or partition-spec transitions. A pilot matrix deliberately samples the risk dimensions and applies the same publication/rollback path as the full plan.

Finally, backfills are governance events. They can alter financial reports, machine-learning features, customer exports, regulatory records, or deletion state. The request, preview, approvals, actor identities, source/code policy, execution evidence, exceptions, and consumer communication must support later review without relying on transient chat or scheduler logs.

## Prerequisites and Retrieval

Retrieve [Backfills](037-backfills.md), [Late Corrections and Restatement](038-late-corrections-and-restatement.md), [Testing a Multi-Stage Batch Pipeline](040-testing-a-multi-stage-batch-pipeline.md), and modules [DE-041](041-directed-acyclic-graphs-and-dependencies.md) through [DE-045](045-partitioned-assets.md). Be able to distinguish output ownership $U$, input/dependency closure $C(U)$, run requests, attempts, candidates, accepted generations, and physical files.

Retrieve the request context: incident/change/migration identifier; problem statement; desired consumer-visible outcome; semantic mode (`as-was`, `as-now`, corrected, migrated); authoritative owner; affected consumers; urgency/deadline; regulatory/privacy constraints; approval matrix; allowed environments; cost center; expiry; and rollback or forward-repair expectations.

Retrieve selection inputs: asset and graph versions; partition specs and canonical key types; calendars/time zones; exact date/range interval convention; tenant/region/source domains; dynamic-key effective history; current partition states; accepted generation inventory; missing/failed/quality/freshness predicates; exclusions; graph-selection language and precedence; maximum expansion; authorization rules; and preview/digest format.

Retrieve dependency semantics: versioned DAG; exact partition mappings; transitive upstream inputs; rolling/window/session halos; prior-state/checkpoint initialization; reference/dimension history; schema/semantic compatibility; accepted-empty behavior; optional/fallback policy; downstream closure/invalidation; external systems; publication groups; and conditional branches. Compare declared, compiled, and observed lineage.

Retrieve reproducibility evidence: immutable source objects/snapshots/log positions; source epochs; historical reference generations; code artifact and build provenance; transformation/schema/config/policy versions; runtime/container and dependency lock; environment-neutral parameters; target base generation; idempotency/fencing scheme; and retention horizon. Identify any input that no longer exists or cannot be interpreted faithfully.

Retrieve performance/capacity evidence: per-unit rows/bytes/files, scan/shuffle/write, duration, memory/CPU, warehouse slots, source QPS, transactions/log/locks/replication, object/catalog/list requests, network, external API quota, downstream fan-out, retry rates, skew, warmup/cold-start, cost, and variance by date/tenant/spec. Identify the actual bottleneck and live reservation.

Retrieve orchestration capabilities: dry-run/preview, backfill reprocessing policy, ordering, per-backfill active-run limit, pools/queues/priorities, delayed retry, indexed/batched work, pause/resume/cancel, durable state, checkpoint, event/audit stream, plan versioning, and maximum UI/API cardinality. Product features do not replace data semantics but shape implementation.

Retrieve validation/publication: candidate namespaces, output manifests, row/key/multiplicity/schema/value/business controls, reconciliation totals, unchanged-outside-scope test, quality thresholds, comparison/baseline, shadow/branch support, conditional publication, downstream notification, cache refresh, rollback, consumer verification, cleanup, and evidence retention.

Before approval, fill a plan contract:

| Concern | Required decision and evidence |
|---|---|
| Intent | Purpose, semantic mode, owner, consumers, deadline, expiry |
| Selection | Typed predicate, exact enumerated targets, exclusions, digest, authority |
| Closure | Required upstream work/inputs, reused generations, downstream impact |
| Versions | Source/reference cuts, graph/code/schema/config/runtime, base generation |
| Work DAG | Units, dependencies, ordering, grouping, idempotency/fencing keys |
| Capacity | Resource vectors, live reserve, pools/quotas, retry budget, cost cap |
| Gates | Preflight, pilot matrix, wave checks, stop conditions, approvals |
| State | Queued/blocked/running/candidate/accepted/failed/unknown/dispositioned |
| Publication | Validation, atomic group, conflict/rebase, cutover, consumer evidence |
| Recovery | Pause/resume/cancel/retry/replan/rollback/forward repair/cleanup |
| Governance | Least privilege, separation of duties, audit, retention, communication |

## Learning Objectives

After completing this module, you should be able to:

1. distinguish catch-up, retry, replay, repair, restatement, migration, disaster rebuild, and planned backfill;
2. compile typed selection predicates into immutable authorized target inventories with stable digests;
3. compute dependency-closed plan DAGs using exact partition mappings and compatible accepted-generation reuse;
4. choose dependency order, waves, grouping, pilots, and checkpoints for parallel and stateful workloads;
5. estimate multi-resource work and admit it within live reservations, retry budgets, quotas, fairness, and cost limits;
6. define preflight gates and machine-evaluable stop conditions for correctness, freshness, overload, and spend;
7. coordinate live schedules, corrections, schema changes, compaction, retention, and concurrent backfills using ownership and fencing;
8. model durable progress, pause/resume/cancel/retry/replan/supersession, and unknown outcomes without changing scope;
9. validate, publish, roll back or forward-repair, notify consumers, clean candidates, and reconcile exact outcomes; and
10. secure, test, audit, and operate the backfill planner at realistic cardinality and failure scale.

## Core Exposition

### Classify the historical intent

Start with why an output needs historical work. Common classes are:

- **gap fill:** expected output has no accepted generation;
- **retry/recovery:** unchanged logical work failed or has uncertain outcome;
- **source correction:** authoritative source generation changed;
- **logic restatement:** business rule, code, schema, or model changed;
- **reference restatement:** historical dimension/rates/policy interpretation changed;
- **migration:** materialize a new representation or contract alongside/over old;
- **disaster reconstruction:** recreate trusted generations from retained sources; and
- **experiment/audit:** compute shadow comparisons without intended production replacement.

Each class implies different identity. An unchanged retry reuses logical fingerprint; a correction or new rule creates a new intended generation. A shadow experiment must not inherit publication authority. A migration may require dual-read/write and consumer cutover rather than replacing historical keys immediately.

Specify `as-was` versus `as-now`. As-was recreates the output under historical source, references, code/policy, and known defects if exact reproduction is desired. As-now applies current approved meaning to historical source. Corrected mode may pin historical source plus selected corrected references/code. Labels like “rerun old dates” do not choose among them.

State success in consumer terms: exact generation coverage, schema/quality, freshness/cutover, reports reconciled, and no unauthorized effects. An orchestrator terminal state is evidence about execution only.

### Compile and freeze the target selection

Accept typed selection fields rather than arbitrary code or raw SQL: asset IDs, partition-spec versions, canonical key ranges/sets, dimension predicates, generation/state predicates, tenant scope, explicit include/exclude, and maximum count. Validate intervals and calendars. Require an exact upper bound and protect the live head by default.

Relative expressions such as `last_90_days` are convenient for preview but must resolve to absolute keys at a recorded instant under a recorded time zone/calendar. State queries such as `failed` or `missing` also resolve once. Execution uses the frozen enumeration, not the predicate rerun later.

Graph selection languages need precedence and expansion review. A selector can name ancestors/descendants or intersections/differences. dbt documents graph operators and set operators for node selection; regardless of tool, render the selected node set, partition set, count, owners, sensitive domains, and dependency closure before approval.

Canonicalize the frozen selection and compute a digest. Store planner version, asset/graph/partition-spec versions, caller/authority, query and resolution time, keys in stable order, exclusions, and reason. Pagination/export must not truncate preview. Reject expansions beyond policy unless a higher authorization path approves the exact result.

### Separate target ownership from dependency closure

Target set $T$ says which output generations the backfill may create or supersede. Closure $C(T)$ says what must be read or computed. A seven-day rolling target needs prior partitions; a join needs both sides; a stateful model may need a checkpoint or sequential predecessor; a downstream impact set may extend after $T$.

Traverse the versioned logical graph using exact partition mappings. Include external inputs, reference histories, quality/publication gates, conditional branches, and group snapshots. Validate every mapped key against its asset spec. Record whether an item is target output, recomputed prerequisite, immutable input reused, validation gate, publication unit, or downstream notification.

Do not automatically recompute the entire ancestry. Reuse an accepted upstream generation when it is retained, accessible, compatible with selected code/schema/policy, sufficiently trusted, and semantically correct for the request. Record the exact generation and proof. Conversely, do not reuse a target merely because an accepted old generation exists when replacement is the purpose.

Compute downstream invalidation separately. Replacing source day 10 may require rolling outputs days 10–16. Those can be added to target ownership under approval or reported as affected obligations for another plan. Hidden expansion during execution violates authorization.

### Construct a finite plan DAG

Create one plan node per retryable/dispositioned unit at a granularity supported by identity and publication. Nodes can materialize one partition, batch several independent keys while retaining per-key evidence, run validation, publish an atomic group, notify consumers, or verify cleanup. Edges encode actual readiness, not convenience order.

Run graph validation: all referenced nodes exist; no self-edge or directed cycle; exact producer/consumer key bindings resolve; required external accepted inputs exist; conditional branches are frozen or explicitly runtime-governed; and every selected target has a path to acceptance/publication. A feedback process becomes an epoch/state sequence rather than a same-plan cycle.

Deterministic topological order helps review and resume. It is not necessarily execution order: independent ready nodes can run concurrently. Stateful recurrence may require oldest-first. A validation pilot may impose a temporary gate before otherwise independent nodes. Newest-first can be appropriate for freshness only when each key is independent and publication cannot regress newer state.

Bind the plan identity to graph/work nodes/edges, target and closure digests, input generations, code/config/schema/runtime, base output generation, policy, and approvals. Once admitted, edits create `plan_revision+1` linked by supersession; attempts continue to reference the revision they executed.

### Estimate resource vectors, not one duration

For work unit $w$, estimate vector

$$
c(w)=(readBytes,sourceQPS,cpu,memory,shuffle,writeBytes,slots,logIO,objects,metadataCalls,externalCalls,cost,duration).
$$

Use representative historical telemetry by partition size, age, tenant, source/spec/schema version, and code path. Report estimate confidence and high-percentile bounds. Missing pruning, cold storage, changed compression, skew, or unavailable statistics widen uncertainty.

One worker count cannot protect all dimensions. Ten parallel units might fit CPU but saturate a source replica or warehouse transaction log. Rate limits bound calls over time; concurrency bounds simultaneous occupancy; total cost/storage bounds the full plan. Model retries and validation reads as load.

Reserve explicit capacity for live production and higher-priority recovery. A BigQuery reservation/assignment can isolate slot capacity by project/folder/organization and job type; Airflow pools allocate task slots; equivalent mechanisms must be mapped to real bottlenecks. A pool name without enforced downstream quota is only advisory.

Estimate the critical path and total work. The plan deadline must include pilot, wave execution, retry/backoff, validation, conflict/rebase, publication, consumer verification, and cleanup. Do not promise wall time from average task duration divided by workers when dependencies/skew dominate.

### Form dependency-ready capacity waves

At each admission decision, compute ready nodes whose predecessors have accepted outcomes, not merely finished attempts. Filter by policy, authorization, deadline, active incidents, input availability, plan pause/cancel, and publication conflicts. Pack a subset whose resource vector fits available envelope and fairness rules.

Bin packing is heuristic at scale; deterministic first-fit can make plans reviewable, while adaptive scheduling improves utilization. Preserve why each node was admitted or deferred. Never let an adaptive controller change its logical inputs or skip required nodes to hit throughput.

Wave boundaries can host gates: compare actual versus estimated resource use; check live service objectives; validate candidate quality; update remaining forecast; and stop on threshold breach. Continuous token/concurrency admission is also valid; “wave” denotes a bounded safety cohort, not necessarily a global barrier.

Group work only when it reduces overhead without losing per-key identity and disposition. Kubernetes Indexed Jobs can give parallel task indexes, but the data plan still maps each index to exact work keys and validates outputs. Dagster can launch partition backfills; Airflow exposes per-backfill active-run limits and ordering/reprocessing behavior. These controller features implement parts of admission, not target correctness.

### Design a representative pilot

Choose pilot cases across risk dimensions:

- oldest/newest historical formats and partition specs;
- smallest, typical, largest, and skewed units;
- empty, sparse, dense, quarantined, and corrected inputs;
- each schema/code/reference epoch and dependency branch;
- window/calendar/month/year/daylight-saving boundaries;
- sensitive/tenant-isolated paths using safe authorized data;
- stateful sequence start/resume; and
- publication, downstream consumption, rollback/forward-repair paths.

A pilot may include shadow-only runs first, then a low-risk production publication if required. It must use the same artifact, parameters, identity, validation, and publication machinery as the wider plan. A handcrafted notebook comparison outside the path gives useful analysis but not delivery evidence.

Define pass criteria before results: reconciliation tolerances, schema/key/multiplicity, performance envelope, cost, no live SLO breach, downstream compatibility, and rollback test. Review unexpected differences rather than tuning thresholds until green. Record pilot units in the immutable plan or approved revision.

### Define preflight and stop conditions

Preflight verifies frozen targets and closure still exist; input generations remain retained/readable; code/runtime signatures and schemas match; credentials/authority valid; target base/fences unchanged or rebase allowed; storage/capacity/quota available; candidate namespaces empty or reconciled; live incidents/maintenance compatible; monitoring/runbooks staffed; and consumer communication complete.

Stop conditions are executable thresholds, for example:

- live freshness or error objective breaches for sustained window;
- source/warehouse utilization, queueing, lock/log/replication, or throttling exceeds cap;
- actual bytes/runtime/cost exceed forecast ratio or total budget;
- validation failure/unknown-outcome/receipt-conflict rate exceeds bound;
- unexpected schema/spec/input generation appears;
- output differs outside ownership set;
- fencing/publication conflict with live correction occurs;
- retry amplification or backlog age exceeds policy;
- observability/evidence pipeline is unavailable; or
- security/privacy anomaly or authorization change is detected.

Stopping pauses new admission. It does not automatically kill running attempts, roll back committed work, or delete candidates. Signal cancellation where safe, fence publication, preserve evidence, reconcile outcomes, then decide resume, replan, forward repair, or abort.

### Coordinate with the live path

Protect the live head with explicit exclusion/guard band based on lateness and ownership, not “probably old enough.” Backfill and live runs can overlap upstream reads safely yet conflict on output keys, source quotas, catalogs, and downstream effects.

For each target key, define ownership arbitration. Options are serialize by partition/generation, conditional publish from expected base, use monotonic source/output versions, or create a shadow branch and rebase after comparison. A stale backfill must not replace a later live correction. Fencing is checked at publication, not trusted from scheduler timing.

Disable or suppress ordinary schedule/events only for the exact governed scope when needed. Record what accumulates and how catch-up resumes. Broadly pausing all ingestion can create a larger incident. If both paths remain active, they converge on the same idempotency/publication protocol and exact-generation arbitration.

Schema deployments, compaction, retention, and deletion can invalidate plan assumptions. Freeze them for the scope, coordinate a maintenance window, or allow only compatible changes verified by preflight at each wave. Retention must not delete frozen inputs or rollback base before plan expiry.

### Make pause, resume, cancel, and replan durable

Persist a plan state machine: drafted, previewed, approved, admitted, piloting, running, pausing, paused, cancelling, reconciling, blocked, completed, failed, superseded, expired, and archived. Define allowed transitions and authorities. Per-unit state remains separate.

Checkpoint after every authoritative transition, not only in worker memory. Store plan revision/digest, frozen sets, accepted/reused generation IDs, work states/attempts, candidates/receipts, budgets spent, next eligible time, stop triggers, overrides, and event sequence. Resume reconstructs from these records and target state.

Pause stops new admission and preserves retry timers/budgets according to policy; running work may finish or be cancellable. Resume rechecks preflight, live state, inputs, base generation, authority, and remaining capacity. It does not rerun the original selector or reset retries/cost.

Cancel expresses no further intended work under this revision. It cannot erase effects. Fence publication, signal attempts, reconcile accepted/candidate/external effects, notify consumers, and disposition every target/work unit. If desired outcome still matters, create a new forward-repair/replan rather than secretly un-cancel.

Replan when frozen assumptions change materially: target/closure, code/config/schema, input generations, semantic mode, base generation, capacity policy, or approval. New revision records diff, reason, inherited accepted work, compatibility proof, and supersession. Never edit a running plan in place.

### Handle failures and retries within plan semantics

Use DE-044 classification. Retry transient unchanged work under stable unit identity, exact input generations, attempt/age/deadline and fleet budgets, backoff/jitter, and candidate isolation. Deterministic data/code/schema errors stop/quarantine. Overload reduces admission. Unknown commit/publication queries receipts/target state before retry.

Plan-level retry budget accounts for correlated failures. If 1,000 units fail from one warehouse outage, three automatic retries each can consume the live reserve. Pause the affected failure domain, probe recovery with a bounded cohort, then ramp gradually.

Failure can block descendants while independent branches continue if risk policy permits. Calculate affected ready sets. Do not mark descendants skipped success; retain blocked-by exact node/evidence. An optional/fallback branch needs approved semantic output labeling.

Redrive or manual retry never changes key/fingerprint. Changed inputs or logic create new plan/work revision. Same key with different intent is conflict. External notifications/exports/payments require stable independent effect IDs or suppression for shadow/backfill mode.

### Track truthful progress

Choose denominators from frozen sets: target partitions, all planned work units, estimated cost/bytes, and critical-path gates. Report each separately. Percent targets accepted answers consumer outcome; percent attempts complete does not.

For target set $T$, classify each key as queued, blocked, running, candidate, validating, accepted, accepted-empty, failed-terminal, unknown, cancelled, superseded, skipped/waived, or expired. A completion policy states which non-success dispositions are allowed and whether they count in the headline denominator.

Weighted progress based on estimated cost can forecast time but may move when estimates are revised. Keep original and current forecast; never alter logical denominator. Track plan burn rate, remaining capacity/cost, estimate error, critical path, and live SLO impact.

Expose exact exceptions with pagination and authorization. Counts alone hide one sensitive or high-value missing partition. Preserve first/last failure, causal grouping, and block relationships to avoid thousands of duplicate alerts.

### Validate and publish in controlled units

Every candidate receives structural, schema, key/multiplicity, row/byte/file, aggregate, referential, business, privacy, and lineage checks appropriate to the asset. Compare against source controls and prior generation with expected-difference rules. Verify unchanged output outside $T$ when publication could touch shared state.

Publication unit may be one partition or an atomic group/snapshot. If consumers require all selected dates together, individual candidates remain shadow until a parent manifest selects the validated complete set. If per-partition visibility is safe, publish incrementally while recording plan generation and consumer implications.

Conditional publication checks expected base/current generation and fence. Conflict triggers rebase/replan or retains candidate; it must not “force overwrite.” Apache Iceberg branches/tags can support isolated snapshot workflows and retention, but domain acceptance, validation, and consumer cutover remain application policy.

Before final completion, reconcile target set to accepted intended generations, verify exact inputs/code/spec and quality, check outside-scope stability, resolve unknowns, confirm downstream invalidation/materialization, test representative consumer queries, record cache/catalog refresh, and capture rollback/forward-repair readiness.

### Audit, communicate, and clean up

Record request, selection expression and frozen enumeration/digest, plan DAG/revisions, estimates, approvals, actor/service identities, preflight, pilots, attempts, failures/retries, overrides, stop events, candidate/receipt/generation manifests, validation, publication, downstream actions, consumer verification, cost, and cleanup. Logs alone are not the durable plan ledger.

Communicate expected impact before execution: affected products/partitions, semantic change, availability/freshness, consumer action, publication mode, rollback limitations, and support channel. Notify again on pause, changed ETA, partial publication, completion, exception, rollback, or forward repair.

Cleanup candidates only after acceptance/rollback windows, outcome uncertainty, consumer verification, and audit/retention allow it. Delete exact manifest-listed objects under scoped credentials; never broad-prefix cleanup. Release reservations/pools, revoke temporary access, restore schedules, reconcile catch-up, and close incidents/change records.

Archive a final report comparing planned versus actual target/work counts, resources, cost, duration, failures, retries, validation differences, accepted/waived/failed keys, outside-scope evidence, downstream freshness, and lessons that change estimates or platform templates.

### Test the planner and operations

Unit/property test selection parsing, canonicalization, max expansion, encode/decode, graph operators, interval edges, calendars, authorization scope, mapping totality, closure, accepted-generation reuse, cycle detection, deterministic digest/order, and wave capacity constraints. Use independent simple oracles for bounded cases.

Integration test against actual catalogs/orchestrators/stores: enumerate partitions without truncation; pin generations; create plan/run identities; enforce pools/reservations/quotas; pause/resume across restart; retain counters; isolate candidates; reject stale fences; publish conditionally; and reconcile controller state with target state.

Fault inject crashes before/after work claim, input read, candidate seal, validation, receipt, publication request/acknowledgement, downstream event, and checkpoint. Add source throttling, warehouse overload, catalog lag, credential rotation/revocation, code mismatch, deleted input, schema change, live conflict, retry storm, monitoring loss, and cancellation delay.

Run tabletop/production-safe exercises for oversized selection rejection, emergency pause, unknown effect, replan after live correction, rollback unavailable, and legal hold during cleanup. Verify humans can interpret evidence and that privileged overrides require separation of duties where appropriate.

## Definitions and Notation

Let backfill request

$$
b=(id,purpose,mode,owner,authority,deadline,expiry,policy)
$$

and resolved selection

$$
S=(query,resolvedAt,graphVersion,partitionSpecs,T,X,digest),
$$

where finite $T$ is target output ownership and $X$ explicit exclusions. Execution uses $T$, not reevaluation of `query`.

Let directed dependency mapping yield transitive closure $C(T)$. Classify its items into planned work $W$, accepted reusable exact generations $R$, and blocked/unavailable prerequisites $H$:

$$
C(T)=W\uplus R\uplus H
$$

under a stated classification. Target keys are not removed from $W$ merely because old output exists when supersession is intended.

Plan revision

$$
P_j=(b,S,G_j,I_j,V_j,B_j,g_{base},approvals_j,digest_j)
$$

contains finite DAG $G_j=(W_j,E_j)$, immutable reused/input generations $I_j$, transformation/schema/config/runtime versions $V_j$, capacity/gate policy $B_j$, and expected base publication generation. Attempts reference $P_j$; changed meaning creates $P_{j+1}$.

For resource set $R_s$, estimated cost $c_r(w)\ge0$ and available wave capacity $b_{i,r}$, admitted wave $Q_i$ obeys

$$
Q_i\subseteq Ready_i,\qquad \forall r\in R_s:\sum_{w\in Q_i}c_r(w)\le b_{i,r}.
$$

If costs are uncertain, use high-confidence bound or adaptive gated cohorts and record estimate error. Scalar teaching cost is a simplification of this vector constraint.

Let target disposition function $d:T\rightarrow States$. Successful coverage set $A=\{t:d(t)\in\{accepted,acceptedEmpty\}\}$. Authorized non-success set $Z$ can include waiver/cancel/expired only under policy. Complete plan requires every $t\in T$ have a terminal disposition, $A$ match intended generation evidence, and unresolved/unknown be empty unless plan is explicitly failed/blocked rather than successful.

Use timestamps for request, resolution, approval, admission, attempts, pause/stop/cancel, validation, publication, consumer observation, and cleanup. Use monotonic elapsed clocks locally for durations and governed absolute time for deadlines. Plan sequence/revision and target generation/fence—not wall-clock finish order—govern authority.

## Mechanisms, Invariants, or Proof Structure

The assurance argument has nine layers.

**1. Intent is typed.** Purpose and semantic mode determine whether old or current source/reference/code meaning is required. Without this, identical date selection can yield incompatible valid-looking outputs.

**2. Selection is frozen and authorized.** A bounded typed query resolves to exact $T$, exclusions, versions, and digest. Approval applies to that enumeration. Relative/state predicates cannot drift during execution, and keys outside $T$ have no publication authority.

**3. Closure is complete.** Versioned mappings and observed/declared lineage derive required context, accepted reusable generations, planned prerequisites, and downstream impact. Window halos and historical references prevent same-date shortcuts.

**4. Plan is deterministic and acyclic.** Frozen inputs plus planner version yield finite nodes/edges and digest. Structural validation proves some topological order exists. Stateful work adds explicit predecessor epochs rather than hidden mutable sequence.

**5. Admission is capacity-safe by construction.** Only accepted-predecessor-ready work enters $Q_i$, and every resource component fits the available envelope. This proof depends on conservative estimates/enforced limits; feedback and stop conditions respond when reality differs.

**6. Execution preserves identity.** Every attempt binds one plan revision/work fingerprint and exact inputs, uses bounded retry, writes isolated candidates, and cannot broaden scope. Controller restart/resume reloads durable state rather than reselecting.

**7. Publication is fenced.** Validation precedes a conditional transition from expected base/fence to intended generation. Stale/live-conflicting plans fail closed or replan. Unowned keys remain unchanged; group publication selects exactly the required set.

**8. Progress and terminal evidence use logical denominators.** Every frozen target/work unit has explicit state; accepted output, not task count, proves completion. Unknown and cancellation cannot masquerade as failure rollback or success.

**9. Reconciliation closes control/data gaps.** Compare plan ledger, orchestrator attempts, receipts, candidates, accepted generations, physical manifests, downstream materializations, consumer freshness, budget/cost, and cleanup. Exceptions have authorized disposition.

Plan invariants include:

- frozen $T$ is finite, stable, canonical, and within caller/approval scope;
- every work node exists because it is a target, required prerequisite, validation/publication gate, or governed downstream action;
- every dependency is satisfied by an exact accepted reusable generation or predecessor work acceptance;
- no target/live key can be overwritten without expected-base and fence checks;
- waves never exceed enforced resource envelope and preserve live reserve;
- retries preserve plan/work identity and spend both per-unit and plan/failure-domain budgets;
- pilot gates use the production execution/validation/publication path;
- pause/resume/cancel/replan survive controller restart and never rerun mutable selection;
- progress denominators do not grow/shrink silently;
- every terminal claim reconciles logical, control-plane, target, and consumer evidence.

### Executable dependency-and-capacity planner

The finite model below demonstrates target freezing, dependency closure, reuse of one accepted prerequisite, deterministic topological waves under scalar capacity 8, and live-head exclusion. Scalar cost stands in for a multi-resource vector. It does not model storage, real schedules/calendars, dynamic graphs, optimization quality, concurrency, retries, publication, security, uncertainty, or production capacity enforcement.

<!-- bijux-verify: {"id":"backfill-dependency-capacity-plan","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"selected_targets=(\u0027roll:2026-09-03\u0027, \u0027roll:2026-09-04\u0027)\nplanned_units=(\u0027agg:2026-09-02\u0027, \u0027agg:2026-09-03\u0027, \u0027agg:2026-09-04\u0027, \u0027roll:2026-09-03\u0027, \u0027roll:2026-09-04\u0027)\nreused_units=(\u0027agg:2026-09-01\u0027,)\nwaves=((\u0027agg:2026-09-02\u0027, \u0027agg:2026-09-03\u0027), (\u0027agg:2026-09-04\u0027, \u0027roll:2026-09-03\u0027), (\u0027roll:2026-09-04\u0027,))\nwave_costs=(7, 8, 2)\ntotal_cost=17\nmax_wave_cost=8\ndependency_closed=True\nlive_head_excluded=True\n","stderr":""}} -->
```python
TARGETS = ("roll:2026-09-03", "roll:2026-09-04")
LIVE_HEAD = "2026-09-05"
ACCEPTED = {"agg:2026-09-01"}
DEPS = {
    "agg:2026-09-02": (),
    "agg:2026-09-03": (),
    "agg:2026-09-04": (),
    "roll:2026-09-03": (
        "agg:2026-09-01",
        "agg:2026-09-02",
        "agg:2026-09-03",
    ),
    "roll:2026-09-04": (
        "agg:2026-09-02",
        "agg:2026-09-03",
        "agg:2026-09-04",
    ),
}
COST = {
    "agg:2026-09-02": 4,
    "agg:2026-09-03": 3,
    "agg:2026-09-04": 6,
    "roll:2026-09-03": 2,
    "roll:2026-09-04": 2,
}
CAPACITY = 8


def closure(targets: tuple[str, ...]) -> set[str]:
    required = set(targets)
    pending = list(targets)
    while pending:
        node = pending.pop()
        for parent in DEPS[node]:
            if parent not in required:
                required.add(parent)
                if parent in DEPS:
                    pending.append(parent)
    return required


required = closure(TARGETS)
planned = tuple(sorted(required - ACCEPTED))
reused = tuple(sorted(required & ACCEPTED))
remaining = set(planned)
completed = set(ACCEPTED)
waves = []

while remaining:
    ready = sorted(
        node for node in remaining if set(DEPS[node]).issubset(completed)
    )
    assert ready
    wave = []
    used = 0
    for node in ready:
        if used + COST[node] <= CAPACITY:
            wave.append(node)
            used += COST[node]
    assert wave
    waves.append(tuple(wave))
    completed.update(wave)
    remaining.difference_update(wave)

closed = all(set(DEPS[node]).issubset(completed) for node in planned)
print(f"selected_targets={TARGETS}")
print(f"planned_units={planned}")
print(f"reused_units={reused}")
print(f"waves={tuple(waves)}")
print(f"wave_costs={tuple(sum(COST[node] for node in wave) for wave in waves)}")
print(f"total_cost={sum(COST.values())}")
print(f"max_wave_cost={max(sum(COST[node] for node in wave) for wave in waves)}")
print(f"dependency_closed={closed}")
print(f"live_head_excluded={all(LIVE_HEAD not in node for node in required)}")
```

The first rolling target needs September 1–3 aggregates and the second needs September 2–4. Accepted September 1 is reused, not recomputed; five units remain. Ready-set packing places aggregate days 2 and 3 in the first wave, aggregate day 4 plus now-ready rolling day 3 in the second, and rolling day 4 last. Every wave stays at or below capacity. A production planner must use resource vectors and conservative/feedback-aware admission rather than this scalar teaching heuristic.

## Alternatives and Trade-Offs

**Mutable query versus frozen enumeration.** Rerunning the query adapts to newly failed/missing partitions but changes approval and denominator. Frozen keys preserve audit/reproducibility; new findings become a plan revision or new request.

**Manual key list versus typed selector.** Lists are exact and reviewable for small repairs. Typed selectors scale and can compute closure, but require grammar, authorization, expansion caps, preview, canonicalization, and digest.

**Recompute ancestry versus reuse accepted generations.** Recompute can ensure one consistent new semantic epoch but multiplies cost and blast radius. Reuse saves work when compatibility/evidence is strong. Never infer reuse from a mutable asset name.

**Oldest-first versus newest-first.** Oldest-first is necessary for cumulative/stateful chains and simplifies history. Newest-first restores recent freshness for independent keys. Dependency topology and publication version rules decide, not operator preference.

**One partition per run versus batched runs.** One-to-one gives precise retry/state but large controller overhead. Batching amortizes startup while requiring per-key identity/outcomes and careful partial failure. One process can still publish separate logical generations.

**Static waves versus continuous adaptive admission.** Static waves are reviewable and make gates simple. Adaptive admission responds to actual capacity and skew. Both must enforce bounds, preserve ready semantics, and emit decisions.

**Dedicated reservation versus shared priority pool.** Dedicated capacity isolates live work and makes budget clear but may sit idle. Shared pools improve utilization but require strict priority/preemption/load controls and can still contend below the scheduler.

**Representative pilot versus random sample.** Random sampling estimates population behavior but may miss rare high-risk versions/boundaries. Stratified risk coverage deliberately tests them; combine both when statistical comparison matters.

**Shadow entire plan versus incremental production publication.** Full shadow supports global comparison/atomic cutover but costs storage and delays benefit. Incremental publication reduces recovery time but creates mixed generations consumers must tolerate and complicates rollback.

**Pause versus cancel.** Pause preserves intent and can resume after preflight; it may retain reservations/candidates. Cancel ends further intent but cannot undo effects and requires reconciliation. Do not implement both as one boolean.

**Rollback versus forward repair.** Pointer rollback is fast when prior generation remains valid and consumers can revert. External/downstream effects or semantic migrations may make rollback unsafe; forward correction is slower but honest. Decide before cutover.

**Native orchestrator backfill versus custom planner.** Native controls reduce implementation and integrate UI/state. A cross-asset/domain plan may need richer selection, versions, capacity vectors, approvals, and publication. Extend through governed metadata rather than bypassing native safety invisibly.

**Fail entire plan versus continue independent branches.** Fail-fast limits risk and simplifies outcome. Continuing yields useful progress when branches and publication are isolated, but complicates partial state/communication. Define risk domains and terminal success criteria.

## Failure Modes and Misconceptions

- **“A backfill is a date loop.”** Historical intent includes assets, partition specs, generations, dependencies, versions, capacity, and publication.
- **“Last month is exact.”** It depends on resolution time, calendar, zone, interval ends, and asset time role.
- **“Failed means select it at runtime.”** State changes; freeze exact keys and digest for execution.
- **“The selected outputs are all the inputs.”** Joins, windows, references, state, and downstream invalidation expand context.
- **“Every ancestor must rerun.”** Compatible accepted generations may be reused; prove exact identity and semantics.
- **“Current dimensions reconstruct history.”** As-was and as-now are different requests.
- **“The graph selector is obvious.”** Operator precedence and ancestor/descendant expansion need rendered review.
- **“No cycle means execution order is arbitrary.”** Stateful epochs and publication groups add semantic order.
- **“Concurrency equals capacity.”** Sources, slots, logs, metadata, storage, external quotas, cost, and live reserve differ.
- **“Autoscaling solves backlog.”** It can overwhelm the bottleneck and multiply retries.
- **“Three retries are harmless.”** Correlated unit failure creates plan-scale amplification.
- **“A recent tiny pilot is representative.”** Old formats, large/skewed keys, empties, boundaries, and sensitive branches remain untested.
- **“Pause stops effects.”** Running attempts can continue; fence publication and reconcile.
- **“Cancel rolls back.”** It only ends future intent; committed effects/candidates need disposition.
- **“Resume can rerun selection.”** That changes scope, approval, denominator, and possibly authority.
- **“Editing the plan saves time.”** Material changes require an auditable superseding revision.
- **“Task count is progress.”** Targets, work units, attempts, and publication units have different denominators.
- **“Green attempts mean complete.”** Accepted generations and consumer evidence determine outcome.
- **“Publish newest timestamp.”** Wall-clock finish order cannot defeat source/output versions and fences.
- **“One partition conflict can be forced.”** It may indicate live correction; rebase/replan rather than overwrite.
- **“Backfill events are ordinary events.”** Shadow or historical work can duplicate downstream effects unless identities/modes are explicit.
- **“Cleanup is just delete prefix.”** Exact manifests, uncertainty, rollback, holds, and authorization govern deletion.
- **“A native backfill button supplies semantics.”** Controller mechanics do not choose source cuts, correctness, or publication contract.
- **“Percent complete can improve by dropping failures.”** Frozen denominators and dispositions prevent cosmetic progress.
- **“Successful completion ends the job.”** Schedule restoration, downstream freshness, cleanup, evidence, and post-run review remain.

## Worked Examples

### Example 1

At approval, `last_30_days` resolves to 30 exact Europe/Stockholm business-date keys under calendar v7 and excludes a three-day live guard band. The stored digest covers those keys. A two-day approval delay does not shift execution scope.

### Example 2

A seven-day rolling metric targets September 10. Closure includes facts September 4–10. Facts 4–8 have compatible accepted generations; 9–10 require recomputation. The plan reuses five exact generations and schedules two fact nodes before the rolling target.

### Example 3

A cumulative balance model depends on the prior day's accepted state. Though 100 dates appear independent in a UI, its DAG is a chain. Oldest-first checkpoints preserve recurrence; launching all dates concurrently would read missing or stale predecessors.

### Example 4

A plan has capacity for 40 tasks, but the source replica allows 8 scans and the warehouse allows 16 writers while live work reserves half. Admission caps historical reads at 8 and writes at 8 even if 40 workers are idle.

### Example 5

A pilot samples one empty partition, typical and largest tenants, a schema transition, a daylight-saving boundary, and an old reference epoch. The largest tenant breaches shuffle budget, so planners reduce wave concurrency before broad execution.

### Example 6

Live ingestion publishes a corrected generation for one target key after plan approval. The backfill's expected-base compare fails. It retains its candidate and moves to `blocked_conflict`; an approved revision chooses whether to rebase inputs, accept live output, or supersede it.

### Example 7

One hundred units encounter the same warehouse throttle. The failure-domain stop condition pauses admission after a bounded probe cohort rather than allowing every unit's three retries. Live slot reservation remains intact.

### Example 8

A backfill process exits successfully for 50 partitions, but 3 candidate pointer acknowledgements were lost. Progress reports 47 accepted and 3 unknown, not 100% complete. Receipt/catalog reconciliation finds two accepted and one absent, so only the absent unit retries.

### Example 9

Cancellation arrives after a provider export was accepted but before its receipt update. The plan fences further publication, queries provider outcome with the stable effect key, records the accepted export, and marks remaining units cancelled. It does not describe the export as rolled back.

### Example 10

A plan publishes an Iceberg branch for consumer comparison, then promotes the approved snapshot after controls pass. The branch mechanism isolates table snapshots, while the plan ledger supplies domain selection, approval, quality, downstream communication, and cleanup evidence.

## Cross-Program Connections

[API-019](../../28-api-and-service-engineering/modules/019-bulk-and-batch-operations.md) covers bounded bulk selection, per-item outcomes, and asynchronous operation resources. [API-037](../../28-api-and-service-engineering/modules/037-idempotency-keys.md), [API-071](../../28-api-and-service-engineering/modules/071-timeout-and-deadline-budgets.md), [API-072](../../28-api-and-service-engineering/modules/072-retries-and-backoff.md), and [API-074](../../28-api-and-service-engineering/modules/074-api-level-load-shedding.md) support safe control-plane submissions and retry/load behavior.

[PLAT-043](../../29-platform-engineering/modules/043-batch-and-scheduled-workload-templates.md) and [PLAT-044](../../29-platform-engineering/modules/044-event-driven-workload-templates.md) provide workload golden paths; [PLAT-073](../../29-platform-engineering/modules/073-resource-quotas.md), [PLAT-077](../../29-platform-engineering/modules/077-admission-control.md), and [PLAT-055](../../29-platform-engineering/modules/055-idempotent-reconciliation.md) provide multi-tenant admission and recovery concepts. A platform supplies enforced pools, identities, fences, and evidence; data/domain owners approve semantic scope.

[SYSENG-072](../../26-systems-engineering/modules/072-verification-planning.md), [SYSENG-085](../../26-systems-engineering/modules/085-change-impact-analysis.md), and [SYSENG-095](../../26-systems-engineering/modules/095-emergent-risk.md) connect verification, change closure, and system-wide risk. Backfill planning is a socio-technical change operation, not only compute scheduling.

Within Data Engineering, [DE-037](037-backfills.md) owns backfill data semantics and [DE-038](038-late-corrections-and-restatement.md) owns correction policy. [DE-041](041-directed-acyclic-graphs-and-dependencies.md) through [DE-045](045-partitioned-assets.md) define the objects this planner compiles. DE-049 will deepen run metadata and operational state.

## References

1. Apache Airflow, [Backfill](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/backfill.html). Documents date-range backfill creation, reprocessing behavior, backwards ordering, dry-run, and maximum active runs. Accessed 2026-09-03.
2. Apache Airflow, [Pools](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/pools.html). Documents named task-slot pools, per-task slot use, queued/running accounting, and priority behavior for limiting parallelism. Accessed 2026-09-03.
3. Dagster, [Backfilling Data](https://docs.dagster.io/guides/build/partitions-and-backfills/backfilling-data). Documents launching and monitoring partition backfills and single-run versus multi-run policy concepts for partitioned assets. Accessed 2026-09-03.
4. Temporal Technologies, [Schedules: Backfill](https://docs.temporal.io/schedule#backfill). Documents schedule backfill as executing actions for specified historical intervals and describes overlap-policy interaction. Accessed 2026-09-03.
5. Kubernetes, [Jobs: Parallel Execution](https://kubernetes.io/docs/concepts/workloads/controllers/job/#parallel-execution-for-jobs). Documents parallelism, completions, indexed completion mode, and work-queue patterns for finite Jobs. Accessed 2026-09-03.
6. Apache Iceberg, [Branching and Tagging](https://iceberg.apache.org/docs/latest/branching/). Documents table branches/tags, snapshot references, retention, and isolated workflows relevant to shadow validation/publication. Accessed 2026-09-03.
7. Google Cloud, [Workload Management Using Reservations](https://cloud.google.com/bigquery/docs/reservations-workload-management). Documents BigQuery reservations, slot capacity, assignments, and workload-management relationships. Accessed 2026-09-03.
8. Google Cloud, [Deploy and Run Dataflow Pipelines](https://cloud.google.com/dataflow/docs/guides/deploying-a-pipeline#batch). Documents starting and monitoring batch pipelines and runtime parameters in Dataflow. Accessed 2026-09-03.
9. Google, [Site Reliability Engineering: Handling Overload](https://sre.google/sre-book/handling-overload/). Discusses overload, capacity, per-customer limits, request rejection, and graceful behavior under constrained resources. Accessed 2026-09-03.
10. dbt Labs, [Node Selection Syntax](https://docs.getdbt.com/reference/node-selection/syntax). Documents selection methods, graph operators, set operators, and selector composition relevant to previewing dependency-expanded work. Accessed 2026-09-03.

## Exercises

### Exercise 1

A request says “rebuild failed revenue for last quarter with the fixed model.” Convert it into a typed, frozen, reviewable backfill request. Identify every ambiguity, required version/input/selection field, approval, live-head protection, success criterion, and digest evidence.

### Exercise 2

Target rolling partitions days 8 and 9 each depend on the prior three daily facts. Facts 5 and 6 are accepted and compatible; facts 7–9 must be recomputed. Draw the dependency-closed plan, list reused and planned units, and give a valid oldest-first wave schedule if fact costs are 3 each, rolling costs 2 each, and scalar wave capacity is 8.

### Exercise 3

A plan has 10,000 units. Each estimates 4 source queries, 2 warehouse-slot-minutes, 1 GB read, and 0.2 GB write. Live reserves leave 80 source QPS, 200 warehouse slots, and 400 GB/hour read. Estimate maximum starts per second/minute from each constraint under stated assumptions, identify missing evidence, and propose a safe admission controller.

### Exercise 4

During wave 4, live output corrects 12 target partitions, actual scan bytes are 2.4× forecast, retry rate reaches 18%, and monitoring loses warehouse-lock telemetry. Define automatic decisions, durable states, reconciliation, replan choices, and evidence needed before resume.

### Exercise 5

Design completion and rollback/forward-repair evidence for a 500-partition backfill published incrementally. At the end, 490 nonempty generations are accepted, 3 are accepted valid empty, 2 are waived, 3 are terminal failures, and 2 have unknown publication outcomes. State whether the plan can be called successful and what happens next.

## Answers to the Exercises

### Answer 1

Resolve “last quarter” to exact asset partition keys using the asset's time role, zone, calendar, half-open bounds, partition-spec and resolution instant; enumerate and digest them. Define whether `failed` is observed at resolution and which states count, then freeze those keys. “Fixed model” needs immutable code artifact, build/runtime, schema/config/policy, changed-rule rationale, as-was/as-now/corrected reference semantics, source snapshots/log positions, target base generations, expected output difference, and downstream closure. Record owner, incident/change, tenants, consumers, exclusions/guard band for live head, maximum expansion, cost/capacity, pilot/gates, validation, publication, conflict/rebase, rollback/forward repair, deadline/expiry, credentials, separation-of-duties approvals, communication, and success as exact accepted generations plus reconciliation—not task green. Digest the frozen keys, graph/closure, inputs/versions, plan/policy, base, and approvals.

### Answer 2

Rolling day 8 needs facts 6–8; rolling day 9 needs facts 7–9. Reuse accepted facts 6 (and fact 5 is not actually in this stated three-day closure, so record it as examined but not required). Planned nodes are fact 7, fact 8, fact 9, rolling 8, and rolling 9. Edges are facts 6/7/8 to rolling 8 and facts 7/8/9 to rolling 9. With costs 3,3,3,2,2 and capacity 8, deterministic waves can be `(fact7,fact8)` cost 6; `(fact9,rolling8)` cost 5 after facts 7/8 and reused 6 are accepted; then `(rolling9)` cost 2. Fact 5 must not be added merely because it was listed as accepted; closure, not availability, determines relevance.

### Answer 3

If each unit issues four source queries over one second, source permits at most $80/4=20$ starts/s. If two slot-minutes means two slots occupied for one minute, 200 slots permit roughly 100 concurrent units and, at one-minute duration, 100 starts/min. A 1 GB read per unit under 400 GB/hour permits 400 starts/hour, about 6.67/min or 0.111/s, so read bandwidth is the tightest of these simplified averages. Total planned read is 10 TB and write 2 TB; total source queries are 40,000 and slot demand 20,000 slot-minutes. Missing evidence includes duration/distribution, peak versus average read/QPS, skew, retries, validation reads, cache/cold storage, write/metadata/network/log limits, quotas, cost, and live variation. Use conservative token buckets for source/read, slot concurrency, per-tenant fairness, live reservation, jittered bounded retry budget, small pilot waves, observed feedback, and stop thresholds rather than admitting at the arithmetic maximum.

### Answer 4

Stop new admission because scan ratio breaches forecast, retry amplification is high, and a required safety signal is unavailable. Signal/cancel only where safe; fence unpublished candidates; let or stop active attempts under declared policy; mark the plan pausing then paused/reconciling and units by actual outcomes. Resolve publication/receipts and identify the 12 live generations as expected-base conflicts, never overwrite them. Restore lock telemetry, diagnose scan/pruning/cardinality and retry causes, measure live impact, and update remaining forecast. A superseding revision can exclude/reuse the live-corrected outputs or recompute/rebase them under explicit semantic comparison, reduce concurrency/read tokens, alter wave/pilot gates, and receive required approval. Resume only after preflight validates inputs/artifact/base/fences/capacity/authority and the revision diff/digest is durable.

### Answer 5

The disjoint categories sum to 500. Accepted nonempty 490 plus accepted empty 3 gives 493 successful target outcomes, with 2 waivers, 3 failures, and 2 unknowns. The plan cannot claim full successful materialization while terminal failures and unknown publication remain; even if its preapproved success policy permits the two waivers, it must resolve unknowns because unknown counts as neither failure nor success. Query receipts/catalog for the two unknowns, retry only authoritative absence under the same identities, and retain unresolved state otherwise. Diagnose failures and create authorized retry/correction or record a failed/partial plan. Verify waiver authority and consumer impact. Completion evidence lists every key/disposition, accepted generations, inputs/quality, outside-scope stability, downstream freshness, cost, cleanup, and an honest overall terminal status rather than cosmetic 100%.
