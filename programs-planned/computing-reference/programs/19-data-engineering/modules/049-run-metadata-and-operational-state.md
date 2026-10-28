---
module_id: DE-049
program: Data Engineering
level: 1
module_number: 49
title: Run Metadata and Operational State
status: complete
last_verified: 2026-09-03
---

# Run Metadata and Operational State

## One-Page Review

### Governing question

How can a data platform record enough authoritative, durable, and privacy-safe state to reconstruct what logical work was intended, which physical attempts occurred, what data was read and produced, which transitions were accepted, and what action is safe after crashes, duplicates, delays, or conflicting observers?

### Essential definitions

- A **workflow definition** is a versioned description of logical nodes, dependencies, parameters, contracts, and state-transition rules; a display name is not a version.
- A **logical run** is one invocation of a workflow definition for an exact trigger, scope, input cut, configuration, and intended output obligation.
- A **logical work unit** is one stable obligation inside a run, such as materializing one asset partition; retries do not create new logical work.
- An **attempt** is one physical execution of a logical work unit by a worker under a lease or fencing epoch.
- **Run metadata** describes identity, intent, versions, scope, causality, timing, actors, inputs, outputs, attempts, quality, publication, and disposition for a run.
- **Operational state** is the authoritative control-plane information used to decide scheduling, retry, cancellation, publication, recovery, and terminal disposition.
- An **event journal** is an append-only sequence of immutable facts about accepted commands and observations.
- A **projection** is a rebuildable current-state view derived deterministically from the journal and other authoritative receipts.
- A **state machine** defines allowed transitions and terminal states for a named entity; process exit codes and log messages are observations, not automatically authoritative transitions.
- A **lease** grants time-bounded execution authority; a **fencing token** is a monotonically ordered epoch used by resources to reject stale holders.
- A **heartbeat** is evidence that a particular attempt recently reported under a particular lease; its absence is suspicion, not proof that remote work stopped.
- A **dataset generation** is an immutable logical output identity bound to source/reference generations, code, configuration, and publication state.
- **Lineage** relates jobs/runs to input and output datasets; it complements rather than replaces control state.
- A **terminal disposition** records the final operational outcome, reason, evidence, and whether produced effects were accepted, quarantined, superseded, compensated, or unresolved.

### Central model, mechanism, or theorem

Let a logical run be

$$
r=(d,v,q,b,I,O,t),
$$

where $d$ is workflow identity, $v$ its immutable definition/artifact version, $q$ the trigger and logical scope, $b$ the effective binding, $I$ exact input/reference generations, $O$ expected output obligations, and $t$ the causal parent/trigger context. Let the run journal be an ordered sequence $J_r=(e_1,\ldots,e_n)$ whose accepted events have unique IDs and stream positions. Projection is a deterministic fold

$$
P_n=\operatorname{fold}(P_0,J_r),
$$

with transition preconditions, idempotent duplicate handling, schema versions, and fencing checks. A projection may answer current-state queries only together with its applied revision $n$; it is authoritative to that revision, not proof that no later event exists.

For logical work $w$, attempt $a$ may mutate guarded state only when its epoch equals the current authority:

$$
\operatorname{writeAllowed}(a,w)\iff
\operatorname{epoch}(a)=\operatorname{epoch}_{current}(w)
\land \operatorname{leaseValid}(a)
\land \operatorname{intent}(a)=\operatorname{intent}(w).
$$

Completion requires accepted evidence for every frozen output obligation, not merely successful attempts. A durable journal plus rebuildable projection supports recovery only if event identity, ordering, retention, schema evolution, external receipts, and dataset identities are complete enough for the decisions being made.

### Critical invariants

- Workflow definition, logical run, work unit, attempt, task/operator, trigger, trace/span, dataset, generation, and publication identities are distinct and explicitly related.
- Run identity binds the exact trigger/scope, definition/artifact, effective configuration, inputs, expected outputs, environment, tenant, and authorization context.
- Every accepted event has a globally or source-scoped unique event ID, entity/stream ID, schema/type version, durable stream position or concurrency token, producer, occurrence/recording times, and payload integrity controls appropriate to risk.
- Duplicate delivery is idempotent; same event ID with different content is a collision/error; gaps, conflicting positions, and unsupported schemas fail closed.
- Journal facts are immutable. Corrections append superseding or compensating facts rather than rewriting history silently.
- Projections record the journal revision they have applied and can be rebuilt and compared; caches, dashboards, search indexes, logs, traces, and metrics never silently become control authority.
- State transitions are legal, reasoned, actor-attributed, and fenced. Terminal state does not regress except through a separately identified repair/supersession protocol.
- Heartbeat, lease expiry, timeout, process loss, and cancellation request remain distinct from confirmed cancellation or absence of side effects.
- Attempts can fail while logical work succeeds through a later attempt; a run can have successful tasks yet fail data acceptance or publication.
- Progress uses a frozen logical denominator and accepted obligations; attempt counts, processed rows, discovered work, and scheduler task counts are separate diagnostics.
- Event occurrence, ingestion, start, heartbeat, deadline, completion, publication, and data-effective times are stored with explicit clocks/time zones and uncertainty.
- Sensitive parameters, secrets, raw records, personal identifiers, and unsafe SQL/log text are excluded, tokenized, redacted, or separately access-controlled under retention policy.
- Metadata schema and semantic changes are versioned, backward-read or migrated, replay-tested, and coordinated with journal/projection retention.
- Final reconciliation joins logical intent, attempts, receipts, accepted generations, publication state, consumer acknowledgement, cost, and cleanup without inferring missing facts from a green UI.

### Common failures

Common failures include using a scheduler-generated row ID as business run identity; creating a new logical run on retry; storing only the latest status; allowing workers to update rows after losing a lease; ordering distributed events by wall-clock timestamp; treating heartbeat absence as cancellation; marking success from process exit before dataset acceptance; calculating progress from task attempts or a changing denominator; overwriting failure with retry success and losing the failure history; recording table names without generation identities; storing mutable `latest` code/config references; mixing event time with ingestion time; assuming logs or traces are complete control state; accepting duplicate event IDs with different payloads; deleting event history before projections can be rebuilt; changing event schemas without old readers; placing secrets or row samples in broadly readable metadata; and showing terminal state without a reason, evidence link, or unresolved-effects disposition.

### Compact example

An orders run declares three daily output obligations. Day 1 succeeds on its first attempt; day 2 has one failed attempt and succeeds on a second; day 3 produces a valid accepted-empty generation. Events arrive out of order, one event is delivered twice, and a stale worker sends a heartbeat under epoch 6 after epoch 7 completed the run. The journal assigns positions 1–15, deduplicates the exact repeat, rejects the stale epoch from the projection, retains all attempt history, and reports progress `3/3`, four attempts, one failed attempt, three accepted generations, and terminal state `succeeded`. A dashboard built only from attempt exits could misclassify both the retry and accepted-empty output.

### Connections

[DE-041](041-directed-acyclic-graphs-and-dependencies.md) defines graph identity, [DE-042](042-tasks-jobs-assets-and-datasets.md) separates logical and physical entities, and [DE-043](043-scheduling-and-event-triggered-execution.md) defines trigger semantics. [DE-044](044-retries-timeouts-and-idempotency.md) supplies retry and fencing rules, while [DE-045](045-partitioned-assets.md) through [DE-048](048-data-aware-ci-cd.md) supply partition, backfill, environment, and release identities. DE-050 next composes these into an operable workflow.

## Governing Question

What durable record would let an operator, controller, consumer, auditor, and incident responder independently answer: what was intended; what version and data cut ran; which attempt currently had authority; what actually happened; which outputs became acceptable and visible; what remains unknown; and what transition is safe now?

Operational interfaces often expose a single colored status. That simplification is useful for scanning, but unsafe as a state model. “Failed” may mean no worker started, a worker exited after committing output, a quality gate rejected a candidate, publication conflicted, or a notification failed after data became visible. “Success” may mean every leaf scheduler task exited successfully while an intermediate dataset was stale or a cleanup task masked an upstream failure. The metadata contract must preserve the distinctions needed for action.

The run record is a nexus of identities. It connects a reviewed workflow definition to one trigger and scope, resolved configuration, source/reference generations, logical work, physical attempts, runtime telemetry, candidate outputs, validation, publication, and consumers. If identities float—`latest` image, current table, active config—reconstruction becomes guesswork. If identities collapse—run equals attempt, table equals generation—retry and historical reasoning become impossible.

State is distributed. Schedulers, workers, storage engines, catalogs, quality services, lineage emitters, and external systems observe different parts at different times. Messages duplicate, reorder, and arrive late. Clocks disagree. A task can time out locally while a warehouse query commits remotely. Consequently, a robust control plane records immutable observations and authoritative receipts, uses guarded transitions, and reconciles uncertainty instead of allowing last-writer-wins status strings.

The goal is not to store everything. Unbounded logs and payload dumps create cost, privacy, and security liabilities while still failing to answer control questions. Design metadata from decisions and invariants: scheduling, deduplication, retry, fencing, progress, acceptance, publication, recovery, lineage, cost attribution, audit, retention, and debugging. Keep large diagnostics in governed artifact stores with stable references.

## Why This Matters

Recovery begins from state. After scheduler failover, a replacement must distinguish unstarted work from active leased work, completed candidates awaiting validation from published outputs, and timed-out attempts with unknown external effects. If the durable record contains only “running,” the controller either waits forever or risks duplicate effects.

Retries expose identity errors. A logical partition should keep one work identity across attempts so receipts and idempotency controls can recognize prior effects. If every attempt gets a new logical identifier, a remote service sees new requests. If all attempts share one physical ID, operators lose causality, resource, failure, and timing evidence. Both levels are required.

Data outputs persist beyond processes. Recording `analytics.orders` is insufficient when many generations, partitions, schema versions, and candidate/published states exist. Incident response needs exact source and output generations plus the publication receipt. Without them, a responder cannot know whether a retry should reuse, replace, quarantine, or forward-repair.

Progress and service levels depend on correct denominators and time roles. A dynamic job may discover more partitions while it runs; retries inflate task counts; an accepted-empty partition contains zero rows but is complete. `completed attempts / observed attempts` is neither stable nor meaningful. Freeze logical obligations or version denominator expansion, then count accepted dispositions. Separately record scheduled time, event occurrence, ingestion, queue, execution, data interval, publication, and freshness.

Observability signals are lossy by design. Traces may be sampled, logs dropped or redacted, metrics aggregated, and dashboards cached. They are excellent diagnostic evidence but poor sole authority for retry or publication. The control state should link to them through trace/span/log/artifact identifiers while retaining its own minimal authoritative facts.

Metadata is sensitive. Parameters may contain tokens or customer identifiers; SQL can expose literals; schema names reveal projects; error messages and samples can contain personal data; lineage can reveal restricted relationships. A central metadata catalog often has broad readership and long retention, magnifying leakage. Classification and minimization belong in schema design.

Metadata also evolves. Long-lived runs, replayable event journals, restored backups, and audit retention mean readers encounter old versions years later. Renaming a state or changing its meaning can corrupt rebuilt projections. Schema evolution must preserve wire compatibility and semantic interpretation or supply deterministic migration.

Finally, trustworthy state improves automation. Controllers can safely claim leases, retry eligible failures, detect stale projections, publish conditionally, and reconcile unknown outcomes only when identity and transition evidence are precise. Better dashboards are a consequence; safer control is the purpose.

## Prerequisites and Retrieval

Retrieve the workflow definition and immutable compiled graph; definition/artifact digest; owners; logical nodes and dependencies; trigger event/request/schedule identity; scheduled interval and data interval; partition and tenant scope; input and reference generations; expected output obligations; effective configuration and environment binding; policies and approvals; and the semantic contract that distinguishes replay, retry, correction, restatement, and new run.

Retrieve runtime entities: logical run; work units; batches/maps; tasks/operators; attempts; worker/executor/queue/pool/host/container/process identities; leases and fencing epochs; deadlines/timeouts; retries/backoff; cancellation commands; checkpoints; idempotency keys; external-effect receipts; candidate outputs; validation/quality results; publication receipts; downstream notifications; and cleanup.

Retrieve existing metadata surfaces: scheduler database/API; workflow event history; manifest and result artifacts; catalog history; lineage events; trace context and spans; logs; metrics; audit records; object-store manifests; warehouse query/job history; incident records; cost/billing labels; and consumer acknowledgements. For each, identify authority, consistency, completeness, ordering, retention, schema version, access, and failure behavior.

Retrieve state-machine semantics: legal run/work/attempt transitions; terminal states; retryable reasons; accepted-empty; skip and upstream-blocked semantics; partial success; unknown outcome; quarantine; cancellation requested versus confirmed; pause/resume; supersession; repair; reprocessing; and whether history is mutable. Identify which system arbitrates each transition.

Retrieve event/journal semantics: event ID and collision rule; stream/entity key; producer identity; schema/type version; occurrence and ingestion time; stream position or resource version; deduplication window; ordering scope; partitioning; delivery guarantees; replay API; snapshots/checkpoints; compaction; corruption checks; retention; legal hold; and dead-letter/quarantine behavior.

Retrieve projection semantics: fold/version; applied journal position; snapshot identity; rebuild method; lag/freshness; indexes/search; query consistency; concurrency control; cache invalidation; reconciliation against journal and external systems; backup/restore; and disaster-recovery objectives.

Retrieve data-governance requirements: metadata field classification; secrets handling; parameter allowlist; tenant isolation; encryption; access roles; separation of duties; row samples and log references; retention/deletion; data residency; subject requests where applicable; audit access; and aggregation/cardinality limits.

Distinguish definition from run; trigger from run; logical work from attempt; task name from task instance; attempt ID from idempotency key; process from remote operation; desired state from observed state; command from accepted transition; occurrence time from ingestion/recording time; monotonic sequence from wall-clock order; heartbeat from lease; timeout from cancellation; terminal attempt from terminal logical work; run success from data acceptance/publication; empty output from missing output; dataset name from generation; lineage from control authority; trace context from business identity; event log from application log; append-only fact from rebuildable projection; resource version from business version; schema compatibility from semantic compatibility; and retention deletion from silent history rewriting.

Create an operational-state contract:

| Concern | Required identity, rule, and evidence |
|---|---|
| Definition | Logical workflow ID, immutable version/artifact, graph, contract and owner |
| Invocation | Run ID, trigger/causal parent, scope, inputs, binding, outputs, authorization |
| Work | Stable work key, partition/asset obligation, dependency and idempotency intent |
| Attempt | Attempt ID/number, executor, lease/epoch, timing, resources and terminal reason |
| State | Allowed transitions, preconditions, actor, command ID, authoritative receipt |
| Event | Event ID, stream, sequence/version, type/schema, producer, times, payload digest |
| Projection | Fold version, applied revision, snapshot, lag, rebuild and comparison |
| Data | Input/candidate/accepted generation IDs, schema, quality and publication receipts |
| Causality | Trigger, parent/child, retry-of, supersedes, trace/span and external effect links |
| Progress | Frozen denominator, accepted dispositions, blocked/unknown counts, confidence |
| Security | Field classification, redaction/tokenization, access, encryption and audit |
| Lifecycle | Retention, compaction, migration, legal hold, deletion, backup and restore |

Write a falsifiable reconstruction claim: “Run `r` binds definition `v`, trigger/scope `q`, binding `b`, inputs `I`, and output obligations `O`; journal positions `1..n` are present with no event-ID collision; projection `p` at revision `n` was rebuilt under fold version `f`; epoch `k` held execution authority; accepted generation receipts satisfy every obligation; publication receipt `u` names expected parent and current generation; diagnostics and unresolved external effects are explicitly referenced.”

## Learning Objectives

After completing this module, you should be able to:

1. design distinct, stable identities for workflow definitions, logical runs, work units, attempts, triggers, traces, and dataset generations;
2. model run, work, and attempt states as guarded machines with explicit reasons, terminal dispositions, and repair/supersession paths;
3. specify append-only event envelopes, ordering scope, duplicate/collision handling, schema versions, and replay behavior;
4. build versioned current-state projections that expose applied revision, lag, rebuildability, and reconciliation status;
5. use leases, heartbeats, fencing epochs, deadlines, and authoritative receipts without inferring cancellation from silence;
6. calculate progress from frozen logical obligations and accepted outputs while retaining attempt and row metrics separately;
7. bind input, candidate, accepted, and published dataset generations to code, configuration, quality, and lineage evidence;
8. correlate control state with logs, metrics, traces, lineage, query history, costs, and external effects without confusing telemetry with authority;
9. secure, minimize, retain, migrate, archive, delete, and restore metadata according to operational and governance needs; and
10. test state systems through duplicate, reorder, gap, race, stale-writer, schema-evolution, projection-rebuild, and disaster scenarios.

## Core Exposition

### Begin with decisions, not available fields

Inventory decisions the state system must support: admit or deduplicate a trigger; schedule ready work; claim or renew execution authority; decide whether a failure is retryable; resolve ambiguous remote outcomes; calculate progress; validate and publish candidates; stop stale publishers; notify consumers; restore after failover; attribute cost; answer an audit; and delete metadata lawfully. Each decision implies facts, freshness, authority, and retention.

Do not copy an orchestrator database wholesale into a warehouse and call it a model. Internal schemas can change and often reflect implementation rather than durable meaning. Use supported APIs/artifacts/events when available, normalize into repository-owned semantic contracts, and retain source identifiers for drill-down.

Separate a compact authoritative core from diagnostic extensions. Core fields identify intent, state transitions, authority, generations, and receipts. Logs, query plans, row samples, full configuration, stack traces, and performance profiles live in restricted artifact stores, referenced by immutable locator/digest and retention class.

Every optional field needs absence semantics. `null end_time` might mean running, never started, unknown, redacted, or old schema. Represent these states explicitly when they change decisions. Avoid magic values such as epoch zero or negative row count unless versioned contracts define them.

### Establish an identity hierarchy

A workflow definition has a stable logical name and an immutable version. The version should cover the compiled graph and behavior-bearing artifacts, not only source commit. A scheduled declaration may have its own version because changing cadence or interval semantics should not rewrite historical run meaning.

A trigger occurrence has identity independent of a run. One event may intentionally fan out to several workflows; deduplication may map repeated delivery to one logical run. A manual request, scheduled tick, dataset update, backfill plan, or recovery action supplies causal context and authorization.

A logical run binds the definition version, trigger, scope, configuration, environment/tenant, input/reference generations, and expected outputs. Its ID is stable across controller restart. Whether retry creates a new run depends on semantics: retry of unchanged intent remains the same logical run/work with another attempt; restatement under new code or inputs is a new run linked by `supersedes` or `corrects`.

Logical work identifies one obligation within the run, often `(asset, partition key, transformation version, input fingerprint)`. A scheduler task instance is a physical orchestration unit and may cover several work units or split one work unit across stages. Preserve the mapping rather than assume one-to-one.

Attempt identity names each physical execution. Record retry number as presentation, not identity, because concurrent or recovered attempts may make a simple counter ambiguous. Bind attempt to work, worker/executor, lease and epoch, artifact, effective configuration, resources, start/end, failure reason, candidate and external receipts.

Dataset identity has layers: logical dataset/asset, partition/spec, generation/version, physical location, and publication reference. Physical compaction may change files without changing logical content; correction changes generation meaning even at the same table name. Record both when operational decisions depend on them.

Trace and span IDs correlate distributed telemetry. OpenTelemetry defines immutable span context with trace and span identifiers and spans with parent, links, times, events, attributes, and status. These identifiers should not replace run/work identity: traces may be sampled, restarted, or span several business runs; retries may create separate spans for one work unit.

### Model state machines at each level

Define separate machines for run, work, attempt, candidate, migration, and publication. A useful attempt machine might include `created`, `leased`, `starting`, `running`, `succeeded`, `failed`, `cancelled`, `timed_out`, and `unknown`. A work machine adds `blocked`, `ready`, `candidate`, `accepted`, `quarantined`, `superseded`, and terminal failure. A run aggregates obligations but may retain `computation_succeeded`, `acceptance_failed`, or `publication_conflict` as distinct reasons.

Names are less important than legal transitions and postconditions. `running -> succeeded` might require a completion receipt and candidate manifest. `candidate -> accepted` requires quality and reconciliation. `accepted -> published` requires conditional publication. `cancellation_requested` is a command/condition, not proof of `cancelled`.

Record state, reason code, human message, actor/controller, command/event ID, occurrence and recording times, observed definition generation, evidence references, and prior transition. Reason codes are stable programmatic values; messages can evolve and may be redacted.

Terminal means no ordinary transition is allowed for that entity. Repair does not reopen history silently. Create a new repair/reconciliation entity or append a superseding disposition linked to the old terminal fact. This preserves what operators knew and did.

Aggregation policy must be explicit. Apache Airflow documents that a DAG run's terminal status is derived from leaf task states and associates each run with a data interval. That is a product-defined operational aggregation; a data platform may require additional acceptance and publication gates beyond the scheduler's run status. Store the source status and the governed data disposition separately.

### Use an append-only journal and rebuildable projections

Commands request changes; the authoritative state service validates preconditions and appends accepted events. Examples include `RunRegistered`, `WorkDeclared`, `AttemptLeased`, `AttemptStarted`, `HeartbeatObserved`, `AttemptFailed`, `CandidateRecorded`, `QualityAccepted`, `GenerationPublished`, and `RunDispositioned`. Rejected commands receive receipts but do not masquerade as state events.

CloudEvents defines a vendor-neutral event envelope with required identifiers including `id`, `source`, `specversion`, and `type`, plus optional context such as subject, time, data content type, and schema. It standardizes transport context, not workflow transition meaning, ordering, deduplication retention, or authority; define those extensions/contracts explicitly.

Partition journals by entity/stream so positions give a meaningful local order. A broker partition offset, database sequence, or resource version may serve as concurrency evidence within its documented scope. Never compare opaque tokens across scopes. Global ordering is usually unnecessary; causal links and per-entity order are more scalable.

Deduplicate by `(source,event_id)` or another specified domain. Exact repeat is safe to ignore while preserving delivery metrics. Same identity with different canonical content is corruption or producer violation and must quarantine/block. Deduplication retention must cover replay and maximum redelivery horizon.

Projection consumers fold events in stream order, apply schema upcasting/migration, enforce legal transitions, and checkpoint the last applied revision. Store `projection_version`, `applied_revision`, `built_at`, and error/gap state. Serve “current” together with revision and consistency semantics.

Rebuild projections from journal plus verified snapshots. A snapshot binds stream, through-revision, fold version, state digest, and creation provenance; replay starts after it. Periodically rebuild independently and compare hashes or semantic fields. If the full journal expires, the retained snapshot becomes an authoritative base and needs equivalent integrity, schema, backup, and migration controls.

### Handle ordering, duplication, gaps, and late facts

Wall-clock timestamps do not establish distributed order. Clocks skew, events buffer, and custom event times can precede or follow surrounding observations. OpenTelemetry explicitly permits span events with custom timestamps to be recorded out of timestamp order. Store occurrence time for analysis and ingestion/stream position for deterministic fold.

Require contiguous sequence when the source promises it. A gap may mean delayed delivery, retention loss, producer error, or unauthorized deletion. Mark the projection incomplete and stop decisions that need the missing fact. If sources cannot provide sequence, define commutative/idempotent merge semantics and represent unresolved conflicts; last-write-by-time is rarely sufficient.

Late facts can refine history without retroactively pretending observers knew them. Append a fact with original occurrence time and current recording time. Rebuild analytical timelines if needed, but preserve when the platform learned it. Incident and SLA analysis often need both.

Duplicate terminal reports from retries should converge only when identity and payload agree. Conflicting terminal outcomes require authoritative receipts: catalog publication, transaction receipt, remote idempotency record, or reconciliation. Do not pick whichever arrived last.

Temporal documents Workflow Execution Event History as the durable record used to recover workflow state through replay. That is a strong product example of history-driven recovery, but application-specific external effects still need deterministic/idempotent integration and receipts; a generic metadata design must state its own event and replay contracts.

### Coordinate leases, heartbeats, and fencing

A lease says an attempt may act until expiry under named conditions. Store work ID, holder/attempt, epoch or fencing token, issued/renewed/expires times, resource scope, and authority. Renew with compare-and-set so a stale holder cannot extend after replacement.

A heartbeat reports recent liveness/progress from an attempt. It may include checkpoint position, resource use, and health, but keep its volume bounded and sampling semantics explicit. Coalesce ordinary heartbeats in projections or a short-retention stream while retaining state-changing events longer.

On missed heartbeat or lease expiry, mark authority expired and investigate/reconcile. Remote compute may continue. A replacement obtains a higher epoch. Every mutable sink, checkpoint, candidate registration, and publication operation must reject the old epoch or use an equivalent uniqueness/conditional mechanism. A lease in the scheduler alone cannot fence a warehouse query or external API.

Store deadline and timeout by layer. Queue deadline, worker heartbeat timeout, query timeout, overall business deadline, and publication deadline answer different questions. Timeout event records who stopped waiting and what cancellation was requested; subsequent authoritative receipt resolves whether effects occurred.

### Record time without inventing order

Use explicit UTC instants with adequate precision and original time-zone/calendar context for business schedules. Store at least scheduled/trigger occurrence, trigger ingestion, run creation, queue entry, attempt lease/start/end, heartbeat observation, candidate completion, acceptance, publication, consumer visibility, and data-effective interval when applicable.

Durations should come from one monotonic clock inside a process where possible, while cross-system durations use timestamp pairs with clock-quality caveats. Negative queue time is a data-quality signal, not something to clamp silently. Record clock source/synchronization confidence where precise audit or latency claims matter.

Airflow's data interval distinguishes the time range a DAG run operates on from when it actually executes. Preserve this principle for all schedulers: logical data time, schedule time, and execution time are independent. A late run for yesterday can execute today and publish tomorrow.

For event-triggered pipelines, retain source event time, broker ingestion/offset, platform receipt, watermark if used, and run trigger time. Freshness can then be decomposed into source delay, trigger delay, queue, compute, validation, and publication instead of one misleading duration.

### Bind code, configuration, inputs, and outputs

Record immutable artifact/container/package/compiled-graph digests; definition and policy versions; effective nonsecret configuration digest; secret reference/version identity where policy permits; runtime/engine/adapter; and environment/tenant/account. Never store secret payloads. Capture enough provenance to reconstruct behavior without copying sensitive configuration indiscriminately.

Input lineage names logical dataset, partition/spec, generation/snapshot/object/log-offset ranges, schema/contract version, and read role. “Read table X” is insufficient when X changes during the run. For external mutable sources, record the strongest available cut and explicitly label reproducibility limits.

Candidate output records generation, logical keys, physical manifest/location, schema, row/byte/file counts where meaningful, content/control fingerprints, producer run/work/attempt, input set, creation time, and visibility. Acceptance adds test/reconciliation policy and result identities. Publication adds prior/current reference, fencing/precondition, actor, time, and receipt.

OpenLineage's object model relates Jobs, Runs, and Datasets; its API includes run/job/dataset event forms and extensible facets. Use standardized lineage to interoperate, but retain operational-state fields that are outside lineage scope, including leases, retry authority, gate decisions, and publication arbitration.

dbt's manifest artifact describes project resources and graph relations such as parent/child maps, while `run_results.json` records invocation metadata, per-resource results, status, timing, and adapter response. These artifacts are useful source evidence. Their completeness is command-specific, versioned, and product-scoped; normalize identities and retain artifact schema versions rather than assuming they are the platform's whole run record.

### Calculate progress from accepted obligations

Freeze the logical obligation set before execution when possible. Let $W_r$ be required work/output units and $A_r\subseteq W_r$ accepted terminal dispositions. Then

$$
\operatorname{progress}(r)=\frac{|A_r|}{|W_r|},
$$

with separate counts for ready, running, blocked, candidate, failed-retryable, failed-terminal, unknown, quarantined, superseded, and accepted-empty. Weighting by estimated cost can support capacity views but must not replace obligation completion.

Dynamic discovery requires denominator versions. Append `WorkSetExpanded` with provenance, authorization, old/new digest, and reason. Report `accepted/known as of revision n` and whether discovery is closed. A percentage that decreases after legitimate expansion is honest; hiding it by counting tasks is not.

Attempt success rate, rows processed, bytes scanned, and worker utilization are operational metrics. They can move independently of logical progress. One work unit might require four attempts; one attempt might write zero-row accepted output; one task might batch one thousand units. Preserve mappings.

Critical outputs may require weighted or milestone reporting: “inputs complete,” “candidates materialized,” “quality accepted,” “published,” “consumers verified.” Do not average incompatible stages into a precise-looking percent without a documented model.

### Correlate telemetry without granting it authority

Propagate run, work, and attempt references into structured logs, traces, metrics labels where cardinality permits, query tags, object manifests, and external requests. W3C Trace Context defines `traceparent` and `tracestate` propagation across systems; use it for distributed diagnostic correlation while keeping business identifiers in governed fields.

Avoid high-cardinality and sensitive metric labels. Aggregate metrics by workflow, state/reason class, environment, and bounded owner dimensions; query per-run detail from state stores. Logs may include exact IDs under access control. Traces can link retries or asynchronous causes rather than forcing an inaccurate parent tree.

Sampling must never remove authoritative state transitions. Tail sampling may retain interesting traces, but the control journal independently records minimal facts. When diagnostics are unavailable, metadata should say `not_collected`, `sampled_out`, `expired`, or `collection_failed`, not silently display an empty panel.

Link warehouse query IDs, storage transaction IDs, external idempotency keys/receipts, validation reports, and publication records. These anchors resolve ambiguous outcomes. Validate returned identities and tenants before attachment to prevent cross-run or cross-tenant confusion.

### Design query surfaces for operations and audit

Support point lookup by run/work/attempt/generation/event/trigger/external receipt; list by workflow, partition, status/reason, owner, environment, time role, input/output generation, and incident/change; dependency/causal traversal; current state at revision; state as-of journal position/time-known; and evidence export.

State query consistency must be visible. A cached search result may lag while a strong point lookup is current. Return projection revision, observed journal head if known, build time, and completeness/gap warnings. Kubernetes API documentation describes resource versions as opaque change/concurrency/watch tokens; the general lesson is to pass source tokens according to their scope, not parse them as business sequence.

Pagination needs a stable snapshot or continuation contract. If rows change between pages, operators can miss or duplicate results. Large event histories should stream with bounded pages and integrity checks; UI truncation must be explicit.

Provide timelines from immutable events, but also task/work matrices, generation lineage, state reasons, attempt details, leases, and unresolved effects. Human interfaces should never be the only export path. APIs and evidence bundles enable automation and audit reconstruction.

### Secure and minimize metadata

Classify each field. Public operational fields might include workflow and coarse status; internal fields include resource/cost metadata; restricted fields include tenant IDs, query text, error details, lineage, and object paths; secrets never belong in ordinary metadata. Apply column/field-level controls where one record mixes classes.

Use typed parameter schemas with safe allowlists. Store canonical nonsecret values only when needed; otherwise store digest and restricted reference. Redact secrets before logging, tracing, exception serialization, and event creation. A digest of a low-entropy secret can still be brute-forced, so do not hash payloads casually.

Tenant authorization applies to every query path, index, cache, export, trace link, and backup. Random IDs do not provide authorization. Test cross-tenant object references and indirect inference through counts, timing, lineage, and error messages.

Limit diagnostic payloads. Keep bounded failing-row samples in a dedicated governed store with purpose and expiry, referenced from metadata. Avoid unbounded SQL, plans, environment dumps, and stack traces in journal events because append-only retention makes later removal difficult.

Audit reads and state-changing commands. Separate operator, workflow identity, controller, and human approver. Sign or integrity-protect high-risk records and exports as required, while recognizing that cryptographic integrity does not make input claims truthful.

### Evolve schemas and semantics deliberately

Every event type and projection has a schema version. Prefer additive optional fields with explicit absence meaning. Preserve old enum values; consumers must handle unknown future values safely. A new status that old controllers interpret as success is dangerous even if the wire schema parses.

Use upcasters/adapters from immutable historical event versions to the current fold model, with golden replay fixtures. When semantics genuinely change, version the event type or fold and keep historical interpretation. Record migration provenance and compare old/new projections over representative and complete retained histories.

Coordinate writers and readers. Expand acceptance to new fields/types, deploy readers, then writers, backfill/migrate projections, measure old-version traffic, and contract only after retention and rollback windows. Long-running workflows may continue emitting an old schema; either support it or explicitly terminate/migrate them.

Projection migrations should be rebuildable and reversible where practical. Build a new projection side by side, replay to a fixed revision, compare invariants, catch up, switch readers conditionally, and retain rollback until confidence and retention policy permit cleanup.

State enum and reason taxonomy changes affect alerts, SLAs, automation, and audit. Treat them as contracts. Publish mappings and ensure aggregates do not silently shift historical dashboards.

### Retain, compact, archive, and delete safely

Set retention by decision horizon: maximum retry/redelivery, late-event window, backfill/replay, dataset retention, incident/audit, billing, legal hold, and disaster recovery. Attempt heartbeats may be short-lived; terminal transitions, receipts, generation lineage, and approvals often require longer retention.

Compaction must preserve semantics. Replacing repeated heartbeat events with a summary can be valid after lease/retry windows if exact history is not required. Replacing state transitions with only final status destroys causal evidence. Document which queries and reconstructions remain possible after each tier.

Archive events with schema registry, fold/upcaster code or reproducible version, checksums/manifests, encryption/key lifecycle, access controls, indexes, and restore procedures. Periodically restore and rebuild a projection. Backup success without replay verification is weak evidence.

Deletion can conflict with append-only audit and lineage. Minimize personal data at ingestion, separate erasable diagnostic payloads from durable pseudonymous operational facts, and consult applicable policy/legal owners. Tombstone or cryptographic erasure patterns have trade-offs and do not automatically satisfy requirements.

If history expires, preserve a verified state snapshot and the receipts needed for future control. Clearly mark the earliest reconstructable revision/time. Never imply full history when only compacted state remains.

### Reconcile and test the state system

Reconcile journal, projection, scheduler/executor, resource leases, warehouse queries, candidate manifests, catalogs, quality service, publication pointers, external receipts, and consumer acknowledgements. Differences become explicit cases: projection lag, orphan attempt, lost event, unknown remote outcome, unregistered candidate, published-without-acceptance, stale lease, or dangling diagnostic artifact.

Test duplicate exact events, same-ID/different-payload collisions, out-of-order delivery, gaps, replay from zero and snapshot, unsupported schema, writer/reader version skew, concurrent commands, stale epoch, lease renewal race, timeout then late success, cancellation then commit, retry success after attempt failure, accepted-empty, partial output, publication conflict, dynamic work expansion, clock skew, storage corruption, index lag, access-control bypass, retention boundary, backup restore, and projection cutover.

Property-test fold determinism: every permitted delivery permutation consistent with per-stream order and duplicate insertion yields the same projection; illegal sequences reject predictably. Model-check small state machines for terminal regression, double publication, lost obligations, and stale authority. Fault-inject journal/projection failover and external ambiguity.

Measure control health: append latency/error, sequence gaps, duplicate/collision count, projection lag/rebuild parity, stale lease writes rejected, unresolved unknown outcomes, orphan generations, metadata schema version distribution, query latency, storage growth, retention backlog, unauthorized-access attempts, restore time, and reconstruction drill success.

The following finite model demonstrates an out-of-order delivery batch, exact duplicate suppression, stream-sequence completeness, fenced stale-event rejection, attempt history, accepted-empty output, and obligation-based completion. It is not a distributed consensus protocol, durable journal, security control, or production lineage implementation.

<!-- bijux-verify: {"id":"run-journal-fold","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"run_id=run-orders-2026-09-03\ndefinition_version=orders@sha256:abc123\ningested_events=16\nunique_events=15\nduplicate_events_ignored=1\nsequence_complete=True\nstale_epoch_events_rejected=1\nattempts=4\nfailed_attempts=1\naccepted_work=(\u00272026-09-01\u0027, \u00272026-09-02\u0027, \u00272026-09-03\u0027)\naccepted_empty_work=(\u00272026-09-03\u0027,)\naccepted_outputs=((\u00272026-09-01\u0027, \u0027gen-901\u0027), (\u00272026-09-02\u0027, \u0027gen-902\u0027), (\u00272026-09-03\u0027, \u0027gen-903-empty\u0027))\nprogress=3/3\nterminal_state=succeeded\nprojection_revision=15\n","stderr":""}} -->
```python
RUN_ID = "run-orders-2026-09-03"
DEFINITION = "orders@sha256:abc123"
CURRENT_EPOCH = 7


def event(offset, event_id, kind, **fields):
    return {
        "offset": offset,
        "event_id": event_id,
        "kind": kind,
        "epoch": fields.pop("epoch", CURRENT_EPOCH),
        **fields,
    }


events = [
    event(1, "e01", "run_registered"),
    event(2, "e02", "work_declared", work=("2026-09-01", "2026-09-02", "2026-09-03")),
    event(4, "e04", "attempt_succeeded", work="2026-09-01", attempt="a1", generation="gen-901"),
    event(3, "e03", "attempt_started", work="2026-09-01", attempt="a1"),
    event(5, "e05", "output_accepted", work="2026-09-01", generation="gen-901", empty=False),
    event(6, "e06", "attempt_started", work="2026-09-02", attempt="a2"),
    event(8, "e08", "attempt_started", work="2026-09-02", attempt="a3"),
    event(7, "e07", "attempt_failed", work="2026-09-02", attempt="a2"),
    event(9, "e09", "attempt_succeeded", work="2026-09-02", attempt="a3", generation="gen-902"),
    event(10, "e10", "output_accepted", work="2026-09-02", generation="gen-902", empty=False),
    event(10, "e10", "output_accepted", work="2026-09-02", generation="gen-902", empty=False),
    event(11, "e11", "attempt_started", work="2026-09-03", attempt="a4"),
    event(12, "e12", "attempt_succeeded", work="2026-09-03", attempt="a4", generation="gen-903-empty"),
    event(13, "e13", "output_accepted", work="2026-09-03", generation="gen-903-empty", empty=True),
    event(14, "e14", "run_succeeded"),
    event(15, "e15", "heartbeat", work="2026-09-02", attempt="a2", epoch=6),
]


def canonical(item):
    return tuple(sorted((key, repr(value)) for key, value in item.items()))


seen = {}
duplicates = 0
for item in events:
    prior = seen.get(item["event_id"])
    if prior is not None:
        if canonical(prior) != canonical(item):
            raise ValueError("event_id_collision")
        duplicates += 1
    else:
        seen[item["event_id"]] = item

ordered = sorted(seen.values(), key=lambda item: item["offset"])
offsets = tuple(item["offset"] for item in ordered)
sequence_complete = offsets == tuple(range(1, len(ordered) + 1))
if not sequence_complete:
    raise ValueError("stream_gap_or_conflict")

expected = set()
started_attempts = set()
candidates = {}
accepted = {}
accepted_empty = set()
failed_attempts = 0
stale = 0
state = "pending"

for item in ordered:
    if item["epoch"] != CURRENT_EPOCH:
        stale += 1
        continue
    kind = item["kind"]
    if kind == "run_registered":
        state = "registered"
    elif kind == "work_declared":
        expected.update(item["work"])
    elif kind == "attempt_started":
        started_attempts.add(item["attempt"])
        state = "running"
    elif kind == "attempt_failed":
        failed_attempts += 1
    elif kind == "attempt_succeeded":
        candidates[item["work"]] = item["generation"]
    elif kind == "output_accepted":
        if candidates.get(item["work"]) != item["generation"]:
            raise ValueError("candidate_mismatch")
        accepted[item["work"]] = item["generation"]
        if item["empty"]:
            accepted_empty.add(item["work"])
    elif kind == "run_succeeded":
        if set(accepted) != expected:
            raise ValueError("incomplete_obligations")
        state = "succeeded"
    elif kind != "heartbeat":
        raise ValueError("unsupported_event")

print(f"run_id={RUN_ID}")
print(f"definition_version={DEFINITION}")
print(f"ingested_events={len(events)}")
print(f"unique_events={len(ordered)}")
print(f"duplicate_events_ignored={duplicates}")
print(f"sequence_complete={sequence_complete}")
print(f"stale_epoch_events_rejected={stale}")
print(f"attempts={len(started_attempts)}")
print(f"failed_attempts={failed_attempts}")
print(f"accepted_work={tuple(sorted(accepted))}")
print(f"accepted_empty_work={tuple(sorted(accepted_empty))}")
print(f"accepted_outputs={tuple(sorted(accepted.items()))}")
print(f"progress={len(accepted)}/{len(expected)}")
print(f"terminal_state={state}")
print(f"projection_revision={ordered[-1]['offset']}")
```

## Definitions and Notation

Let:

- $D$ be a stable workflow definition identity and $V$ an immutable definition/artifact version;
- $T$ be a trigger occurrence with causal and authorization context;
- $R$ be a logical run binding $(D,V,T,Q,B,I,O)$;
- $Q$ be the frozen logical scope, including partitions, tenants, or event ranges;
- $B$ be the effective environment/configuration binding identity;
- $I$ and $O$ be exact input generations and required output obligations;
- $W_R$ be the finite or revisioned set of logical work units for run $R$;
- $A_w=(a_1,\ldots,a_k)$ be physical attempts for work $w$;
- $\phi(w)$ be the canonical intent fingerprint/idempotency identity;
- $\lambda_a=(holder,epoch,expires,scope)$ be attempt authority;
- $J_R=(e_1,\ldots,e_n)$ be the accepted per-run event journal;
- $\operatorname{pos}(e)$ be a stream-local durable position;
- $P_R^f(n)$ be projection state after fold version $f$ consumes through position $n$;
- $G_x$ be a dataset generation and $U(G_{old},G_{new})$ a publication receipt;
- $H$ be diagnostic telemetry linked to but not authoritative over $R$; and
- $Z$ be terminal disposition, including reason and unresolved-effect status.

Identity uniqueness is scoped. An event is unique under $(source,eventId)$; a work key under $(run,asset,partition,intent)$; a generation under its dataset/version scheme. Write scope explicitly rather than saying “globally unique” without enforcement.

Define projection validity:

$$
\operatorname{valid}(P_R^f(n))\iff
\operatorname{contiguous}(J_R[1..n])
\land\operatorname{schemasSupported}(J_R[1..n],f)
\land\operatorname{legalTransitions}(J_R[1..n])
\land\operatorname{digestMatches}(P_R^f(n)).
$$

Define obligation completion:

$$
\operatorname{complete}(R,n)\iff
\forall w\in W_R(n),\ \exists! G_w:
\operatorname{accepted}(w,G_w,n),
$$

where an accepted-empty generation is a valid $G_w$ and a successful attempt without acceptance is insufficient.

Define safe retry after attempt uncertainty:

$$
\operatorname{retrySafe}(w)\iff
\operatorname{reconcile}(\phi(w),receipts)=absent
\land \operatorname{newEpoch}>\operatorname{oldEpoch}
\land \operatorname{sinksFence}(\operatorname{newEpoch}).
$$

If reconciliation returns committed, reuse/accept the receipt; if conflicting or unknown, fail closed or compensate under a separate protocol.

Time notation distinguishes $t_{occur}$, $t_{ingest}$, $t_{start}$, $t_{end}$, $t_{publish}$, and data interval $[t_{data0},t_{data1})$. Only positions or documented concurrency tokens determine journal application order.

## Mechanisms, Invariants, or Proof Structure

The operational-state assurance argument has nine layers.

1. **Intent identity.** Definition, trigger, scope, binding, inputs, outputs, tenant/environment, and authorization uniquely identify the logical run. Without this, duplicate triggers and new semantic work are confused.
2. **Work/attempt separation.** Stable work identity persists across physical attempts; every attempt has independent execution evidence. Without this, retries duplicate effects or erase causal history.
3. **Event integrity and order.** Accepted events have unique IDs, supported schemas, source/stream scope, positions, and collision rules. Without this, deterministic replay cannot be established.
4. **Guarded transition.** State machines validate prior state, intent, actor, lease, epoch, and receipts. Without this, stale or concurrent actors can regress terminal state or publish twice.
5. **Rebuildable projection.** Current state names fold version and applied revision and matches independent replay. Without this, a dashboard/cache can silently diverge from history.
6. **Data-generation evidence.** Inputs, candidates, quality, accepted outputs, publication, and consumers are joined by generation identities. Without this, scheduler success cannot establish data correctness or visibility.
7. **Uncertainty preservation.** Timeout, missing heartbeat, cancellation request, unknown external commit, and missing diagnostics remain distinct. Without this, automation guesses and may duplicate or lose effects.
8. **Governed observability.** Logs, metrics, traces, lineage, query IDs, costs, and artifacts correlate through safe identifiers under access/retention policy. Without this, diagnosis is incomplete or metadata becomes a leakage surface.
9. **Lifecycle recoverability.** Event/projection schemas, snapshots, retention, archive, deletion, backup, and restore preserve the decisions promised over their horizon. Without this, old runs become unreadable precisely when replay or audit is needed.

These layers justify a bounded conclusion: if intent fields are complete, journal semantics are correct, authoritative external receipts are available, state machines and fences are enforced, projections replay, and retention covers the decision horizon, the recorded state supports the named scheduling/recovery/publication decisions. They do not prove that producers report truthfully, clocks are synchronized, every external effect is instrumented, domain contracts are correct, or infrastructure is uncompromised.

State-machine invariants include:

- one logical run identity maps to one canonical intent; conflicting intent under the same ID is rejected;
- every attempt belongs to exactly one logical work unit and definition/binding/input intent;
- at most one current epoch has mutation authority for a work/resource scope;
- an accepted generation has one producing work/candidate identity and complete validation evidence;
- publication compares expected parent/current state and yields one authoritative receipt;
- journal position never decreases and event facts are not mutated in place;
- projection revision never exceeds a verified journal head and invalid/gapped state cannot claim completeness;
- terminal state does not regress through ordinary transitions;
- accepted progress never exceeds the frozen/revisioned obligation denominator; and
- secret payloads and ungoverned raw records are absent from the durable core.

Replay determinism requires pure transition logic over canonical events and explicit external lookups represented as facts. A fold must not read current time, mutable configuration, live catalogs, or random values. If a transition depends on a remote outcome, append the verified receipt as an event input before folding.

The executable example illustrates these properties on one finite stream: exact duplicate suppression precedes position checking; ordering uses offset rather than delivery order; a stale lower epoch cannot change state; all attempts remain countable; accepted-empty counts as obligation completion; and terminal success requires equality between expected and accepted work sets.

## Alternatives and Trade-Offs

**Mutable state row versus event journal.** A mutable row offers simple current reads and low storage. It loses transition history and can suffer last-writer races unless carefully versioned. A journal preserves causality and replay but adds schema, ordering, projection, compaction, and storage complexity. Many systems use an append-only authoritative core plus current projections.

**Database transaction versus event broker.** A relational transaction can atomically validate state and append within one store. A broker scales distribution and replay but may separate command validation, event persistence, and projections. Choose according to authority and consistency; an outbox can bridge transactional state to distribution.

**One global journal versus per-entity streams.** Global sequence simplifies total replay and audit but limits throughput and creates unnecessary ordering. Per-run/work streams scale and match causal needs but require cross-stream links and snapshots for global queries. Avoid inventing total order when only local order matters.

**Natural/deterministic IDs versus opaque IDs.** Deterministic identities aid deduplication when canonical inputs and namespace are correct; they can leak meaning and collide under incomplete fingerprints. Opaque IDs avoid leakage/coupling but need a uniqueness index on business intent. Often use opaque run IDs plus explicit canonical intent digest.

**Snapshot-only versus full retained history.** Snapshot-only is cheap and privacy-friendly but cannot reconstruct transitions or late facts. Full history supports audit/replay but costs storage and complicates deletion/schema evolution. Tier heartbeats and diagnostics aggressively while retaining terminal receipts and generation lineage for the required horizon.

**Polling/heartbeats versus event callbacks.** Polling tolerates missing callbacks but adds load/latency; callbacks are efficient but can be lost/duplicated. Combine callbacks with periodic reconciliation, and never infer remote nonexecution from silence.

**Lease by time versus epoch fencing.** Time leases support failover but clock/network delays let old work continue. Monotonic epochs let guarded sinks reject stale writers but require sink cooperation. Use both: lease for controller ownership and fencing/uniqueness at effect boundaries.

**Normalized relational model versus document/event payloads.** Normalization supports constraints and analytical joins; flexible payloads evolve faster and preserve source evidence. Keep critical identity/state fields typed and constrained while retaining versioned extensions or raw source references.

**Orchestrator-native model versus platform-neutral model.** Native fields preserve product detail and reduce translation. They lock consumers to implementation semantics and omit cross-system data state. Normalize durable concepts while retaining source-specific status/artifacts and mappings.

**Traces as run history versus separate control state.** Traces provide excellent causal diagnostics and standards-based propagation. Sampling, exporter failure, mutable attributes, and retention make them unsuitable as sole authority. Link traces to complete minimal control events.

**Strong current reads versus eventually consistent projections.** Strong reads simplify automation but can constrain scale/availability. Eventually consistent views serve dashboards/search efficiently but must expose revision/lag and route high-risk commands through authoritative compare-and-set APIs.

**Store parameters versus store digests/references.** Full parameters aid reproduction but increase leakage and schema coupling. Digests protect some content and reduce size but cannot reconstruct and may expose low-entropy secrets. Store governed nonsecret canonical values or restricted immutable references; never ordinary secret payloads.

## Failure Modes and Misconceptions

- **“Run ID and attempt ID are interchangeable.”** Retry and controller recovery require one stable logical identity plus distinct executions.
- **“A unique ID proves identical intent.”** Bind IDs to canonical intent fingerprints; reject same ID with changed scope, inputs, code, or configuration.
- **“Timestamps order events.”** Distributed clock skew and buffering invalidate that assumption. Fold by scoped sequence/concurrency tokens and retain time for analysis.
- **“At-least-once delivery means duplicates are identical.”** Verify canonical content. Same event ID with different content is corruption, not a harmless retry.
- **“Last status wins.”** Late stale reports can overwrite newer authority. Enforce legal transitions and epochs/resource versions.
- **“Heartbeat expiry means the job stopped.”** It means the controller lacks recent evidence. Fence and reconcile remote effects before retry.
- **“Cancellation requested equals cancelled.”** Record acknowledgement and effect disposition separately.
- **“Worker exit zero means the dataset succeeded.”** Candidate registration, quality, reconciliation, and publication can still fail.
- **“The orchestrator database is the source of all truth.”** Storage/catalog/external effects have their own authoritative receipts; product internals may change.
- **“Lineage is operational state.”** Lineage answers data-production relationships; it generally does not arbitrate leases, retries, acceptance, or publication.
- **“A trace contains the entire run.”** Sampling/export failures and retries break that assumption. Trace context is correlation evidence.
- **“Zero rows means nothing happened.”** A governed accepted-empty generation can satisfy an obligation; missing output cannot.
- **“Progress is completed tasks divided by total tasks.”** Tasks and retries are physical. Use accepted frozen logical obligations.
- **“Dynamic work cannot have meaningful progress.”** Version denominator expansion and report the revision/discovery-closed flag.
- **“One `failed` status is enough.”** Retryability and recovery depend on reason, phase, authority, candidate, remote effects, and evidence.
- **“Append-only means immutable storage alone.”** Producers can emit corrections, schemas can reinterpret, and compaction can erase semantics. Define the full contract.
- **“Event sourcing makes transactions unnecessary.”** Command validation, uniqueness, append, receipts, and projections still need concurrency/atomicity rules.
- **“Resource version is a timestamp.”** Treat concurrency tokens as opaque and scoped according to their source contract.
- **“Metadata is harmless.”** IDs, paths, SQL, errors, lineage, samples, and timing can be sensitive or cross-tenant.
- **“Retaining everything improves audit.”** Excess data increases leakage/cost and may violate policy; retain the minimal evidence that supports named decisions.
- **“Schema-compatible events are semantically compatible.”** New states, defaults, or reason meanings can cause old controllers to take unsafe actions.
- **“A successful backup proves recovery.”** Restore and replay projections, reconcile with external receipts, and measure the result.

## Worked Examples

### Example 1

A daily run scheduled for `2026-09-03T00:00Z` processes data interval `[2026-09-02,2026-09-03)`. It begins at 00:17 and publishes at 01:04. The record stores all four roles rather than one `run_date`. Freshness analysis attributes 17 minutes to trigger/queue and 47 minutes to compute/validation/publication. Reprocessing the same interval under corrected inputs is a new logical run linked to the earlier one, not a timestamp rewrite.

### Example 2

A broker redelivers trigger event `source-x/e77`. The trigger-intent uniqueness record already maps it to run `r10` with the same definition, scope, and input fingerprint, so the service returns `r10`. When another request reuses `e77` with a different tenant, it rejects an identity collision and raises an integrity alert. Randomly creating `r11` would duplicate the business obligation.

### Example 3

Attempt `a1` leases work at epoch 12 and starts a warehouse query. Heartbeats stop; epoch 13 is issued to `a2`. The old query later tries to register a candidate with epoch 12. The candidate registry rejects it. The query may still have consumed compute and left a temporary object, which reconciliation records and cleanup handles. Lease expiry enabled failover; the sink fence prevented stale authority.

### Example 4

A task call times out after submitting an external export. State becomes `outcome_unknown`, not `failed_no_effect`. The controller queries the remote idempotency key and finds a completed receipt. It appends `ExternalEffectConfirmed` and marks the logical work successful without resubmission. Had the lookup returned absent, a higher-epoch same-intent retry would be allowed.

### Example 5

A run declares 100 partitions. Ninety candidates are accepted, five are running, three are blocked, one failed terminally, and one accepted-empty. Progress is `91/100`; the empty generation counts. There are 118 attempt completions because retries occurred, but that number appears only as reliability diagnostics. Publication remains blocked by the terminal failure unless policy defines partial publication boundaries.

### Example 6

Events at positions 40 and 42 arrive while 41 is delayed. The projection stores them but reports `gap_at=41`, applies only through 40, and refuses a terminal publication decision. When 41 arrives, deterministic replay advances through 42. Sorting by occurrence timestamp would have hidden the missing authoritative transition.

### Example 7

An old producer emits event schema v2 after v4 readers deploy. The upcaster preserves v2's `failure` meaning and maps absent `retry_class` to `unknown`, not `retryable`. Golden history replay yields the same terminal dispositions as the old fold. A new reason code is added without redefining old records. After old long-running workflows finish, v2 write acceptance can be retired.

### Example 8

A trace sampler drops most successful spans, but every `AttemptStarted`, `CandidateRecorded`, and `GenerationPublished` control event remains. The state record stores trace IDs where present and says `sampled_out` where absent. Operators retain end-to-end diagnostics for failures while controllers never depend on trace export to know publication state.

### Example 9

An error includes a customer email and a query with a token literal. The event producer emits stable reason `SourceAuthenticationRejected`, tenant-scoped opaque source ID, and a reference to a restricted redacted diagnostic artifact. The secret payload never enters the journal, metric labels, trace attributes, or broad UI. Access to the diagnostic is separately audited and expires sooner.

### Example 10

After disaster restore, the platform loads a verified snapshot through journal revision 8,000 and replays 8,001–9,430 using fold version 6. It compares state digests with a side-by-side projection, then reconciles catalog pointers and external receipts. Three orphan candidates and one missing notification are found; neither is silently folded into success. Recovery completes only after disposition and an earliest-reconstructable-revision marker are recorded.

## Cross-Program Connections

Distributed systems provides message-delivery semantics, local versus global order, logical clocks, leases, fencing, consensus-backed logs, idempotency, outbox/inbox, and reconciliation. Operational metadata applies these to data work whose effects may live in warehouses, catalogs, object stores, and consumers beyond the scheduler transaction.

Database engineering contributes primary/unique/foreign keys, transactions, optimistic concurrency, append-only tables, change streams, indexing, temporal/as-of queries, partitioning, compaction, snapshots, backup, restore, and schema migration. The state model should exploit database guarantees while keeping business identities independent of storage internals.

Event-driven architecture contributes envelope standards, event IDs, source/type/schema, causal links, replay, dead letters, and consumer offsets. CloudEvents improves interoperability but intentionally does not define the application processing model; state-machine semantics remain a platform contract.

Observability engineering contributes structured logs, metrics, distributed traces, context propagation, sampling, exemplars, and correlation. Control state must remain complete even when these diagnostic signals are sampled, delayed, aggregated, or expired.

API and service engineering contributes idempotency keys, conditional requests, concurrency tokens, pagination snapshots, authentication, authorization, rate limits, error taxonomies, and backward compatibility. Operators and controllers are API consumers whose unsafe interpretation can mutate data.

Security engineering contributes least privilege, tenant isolation, integrity, nonrepudiation limits, secret redaction, audit access, supply-chain provenance, and incident evidence. Metadata is simultaneously a control surface and a sensitive asset.

Privacy engineering contributes minimization, purpose limitation, retention, erasure, pseudonymization limits, reidentification analysis, and access accountability. Durable append-only design must minimize personal data before it becomes hard to remove.

Formal methods contributes state machines, invariants, pre/postconditions, refinement, monotone revisions, deterministic folds, model checking, and property testing. These establish internal consistency under assumptions, not truthfulness of external observations.

Site reliability engineering contributes desired/observed-state reconciliation, health versus liveness, SLIs/SLOs, error budgets, incident timelines, runbooks, disaster recovery, and capacity. Data systems add generation acceptance and historical correctness to ordinary service availability.

## References

1. OpenLineage. [Object Model](https://openlineage.io/docs/next/spec/object-model/). Accessed 2026-09-03. Primary project documentation for Job, Run, Dataset, runtime, and design lineage entities/events.
2. OpenLineage. [OpenLineage API Docs](https://openlineage.io/apidocs/openapi/). Accessed 2026-09-03. Primary API specification for run, job, and dataset event envelopes and fields.
3. Apache Airflow. [Dag Runs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html). Accessed 2026-09-03. Primary documentation for DAG-run identity, data intervals, and task-derived terminal status.
4. dbt Labs. [Run results JSON file](https://docs.getdbt.com/reference/artifacts/run-results-json). Accessed 2026-09-03. Primary documentation for invocation and per-resource execution result metadata.
5. dbt Labs. [Manifest JSON file](https://docs.getdbt.com/reference/artifacts/manifest-json). Accessed 2026-09-03. Primary documentation for versioned project resource and dependency-graph artifacts.
6. Temporal Technologies. [Workflow Execution overview](https://docs.temporal.io/workflow-execution). Accessed 2026-09-03. Primary product documentation for Workflow Execution and durable Event History replay concepts.
7. OpenTelemetry. [Tracing API](https://opentelemetry.io/docs/specs/otel/trace/api/). Accessed 2026-09-03. Primary specification for span context, trace/span identity, times, links, events, and status.
8. W3C. [Trace Context](https://www.w3.org/TR/trace-context/). Accessed 2026-09-03. W3C Recommendation for `traceparent` and `tracestate` propagation.
9. Cloud Native Computing Foundation. [CloudEvents Specification 1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md). Accessed 2026-09-03. Versioned primary specification for interoperable event context attributes.
10. Kubernetes. [Kubernetes API Concepts: Resource Versions](https://kubernetes.io/docs/reference/using-api/api-concepts/#resource-versions). Accessed 2026-09-03. Primary documentation for opaque resource versions, change detection, concurrency, list, and watch semantics.

## Exercises

### Exercise 1

Design identities and relations for a weekly revenue restatement triggered manually after a source correction. The first compute attempt times out and a second succeeds. Specify which identifiers remain stable, which are new, and what distinguishes this restatement from retrying the original historical production run.

### Exercise 2

A state consumer receives positions 101 `AttemptStarted`, 103 `AttemptFailed`, 102 `CandidateRecorded`, and a duplicate of 103. Later it receives another event with the same ID as 102 but a different generation. Define safe ingestion/projection behavior and explain why timestamp sorting or last-write-wins is insufficient.

### Exercise 3

A run initially declares 20 partitions, then authorized discovery adds five. Eighteen original partitions and two new partitions are accepted; three are running, one is blocked, and one failed terminally. Report progress and the metadata needed to make the denominator honest.

### Exercise 4

Design a retention policy for heartbeats, state transitions, logs, failing-row samples, candidate manifests, publication receipts, and lineage when retry lasts 14 days, operational audit lasts one year, financial lineage lasts seven years, and sensitive row samples may remain only 30 days. Explain what snapshots or references preserve reconstruction.

### Exercise 5

An organization wants to use sampled traces as its only run database because spans already contain status, attributes, and events. Evaluate the proposal and design a minimal authoritative state core that still links to tracing without duplicating all telemetry.

## Answers to the Exercises

### Answer 1

Create a new trigger/request ID for the authorized manual correction and a new logical run because source generation and intended historical meaning differ from the original production run. Link it with `corrects` or `restates` to that run. Bind the new run to the chosen workflow/artifact, corrected source and reference generations, exact weekly scope, effective configuration, expected output generations, authorization, and publication base. Its logical work IDs and intent fingerprints remain stable across the two physical attempts. The timeout attempt and replacement have distinct attempt IDs, timing, worker/query/trace identities, and fencing epochs. Before retry, reconcile the first query/candidate receipt; timeout alone does not prove no effect. The restatement differs from retry because it intentionally changes input/meaning and therefore must not reuse the original run/work idempotency identity.

### Answer 2

Deduplicate the exact repeat of 103 while retaining a duplicate-delivery metric. Buffer 103 until position 102 arrives, apply 101–103 in position order only if transitions are legal, and expose a projection applied through 101 with a gap warning meanwhile. The same event ID at 102 with a different generation is an identity/content collision: quarantine it, mark the stream invalid, alert the producer/owner, and block state-dependent automation until authoritative evidence resolves corruption. Occurrence timestamps can skew or be supplied late and cannot detect a missing position. Last-write-wins would let the conflicting duplicate rewrite candidate identity and could make retry/publication unsafe.

### Answer 3

The current denominator is revisioned from 20 to 25 obligations. Twenty are accepted, so obligation progress is `20/25 = 80%`. Report three running, one blocked, and one terminal failure separately. Preserve both `WorkDeclared` and authorized `WorkSetExpanded` events, old/new ordered work-set digests, reason, discovering actor/run, authorization, revision/time, and `discovery_closed` status. Historical dashboards should show `18/20` before expansion and `20/25` after it rather than retroactively pretending the denominator was always 25. Attempt and row counts remain diagnostics, not the numerator.

### Answer 4

Keep ordinary heartbeat detail only long enough to cover active leases, the 14-day retry horizon, incident diagnosis, and bounded operational buffer; compact it into attempt timing/last-heartbeat summaries afterward. Keep authoritative state transitions, reasons, attempt dispositions, intent bindings, and candidate manifests for at least the one-year operational audit, with verified state snapshots that bind journal range, fold/schema version, and digest. Keep publication receipts and the minimal input/output generation lineage for seven years because they reconstruct financial provenance; archive them with schemas/upcasters, manifests/checksums, encryption/key lifecycle, access control, and restore tests. Put failing-row samples in a separate restricted store with automatic 30-day deletion; durable events retain only safe reason/count and an expiring reference, never copied values. Logs follow classified operational need and redact secrets/rows. After detailed transition expiry, state explicitly the earliest reconstructable revision and preserve a verified terminal snapshot plus receipts needed for future control/audit.

### Answer 5

Reject traces as the sole database because sampling can omit success paths, exporters fail, spans can be incomplete or duplicated, retention differs, status is instrumentation-defined, and trace parentage does not encode logical retry, acceptance, or publication authority. Keep a compact journal containing definition/run/work/attempt identities; canonical intent; trigger/scope/binding/input/output identities; legal state transitions and reasons; lease/epoch; candidate/quality/publication/external receipts; event ID/stream position/schema/producer/times; terminal disposition; and projection revision. Store trace/span IDs on attempts and external operations when present, plus explicit `sampled_out` or collection-failure status. Traces retain detailed timings/events/attributes for diagnosis, while the authoritative core remains complete enough for deduplication, scheduling, retry, fencing, progress, publication, recovery, and audit.
