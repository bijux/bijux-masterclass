---
module_id: LSDS-030
program: Large-Scale Data Systems Engineering
level: 1
module_number: 30
title: Tracing a Batch Job Through a Cluster Engine
status: complete
last_verified: 2026-09-03
---

# Tracing a Batch Job Through a Cluster Engine

## One-Page Review

### Governing question

How can an engineer reconstruct the causal path of one batch run from submission through planning, scheduling, attempts, shuffle, and output commit, while preserving logical identity across retries and fan-out, separating waiting from work, and avoiding telemetry that is incomplete, misleading, prohibitively expensive, or unsafe?

### Essential definitions

- A **trace** is a causally related set of spans representing one execution or selected portion of it.
- A **span** is a timed operation with an identity, trace identity, parent or links, attributes, events, status, and resource context.
- A **run identity** identifies one submitted execution; a **logical work identity** identifies a stage or partition independent of attempts; an **attempt identity** identifies one physical try.
- A **parent edge** represents a dominant nested causal relationship; a **span link** relates work with multiple or non-nesting causes.
- **context propagation** transfers trace identity and controlled correlation fields across process, queue, RPC, and storage boundaries.
- **fan-out** creates many descendants from one operation; **fan-in** waits for multiple prerequisites before downstream work becomes ready.
- The **critical causal path** is the longest dependency-respecting path that determines observed completion, not the sum of all parallel span durations.
- **queue time** is ready-but-not-running delay; **service time** is time spent executing an admitted attempt; **blocked time** waits on a dependency or resource.
- **sampling** selects which trace data to retain; head sampling decides early, while tail sampling can consider later outcomes if the collection path survives.
- A **commit winner** is the single accepted attempt whose output becomes authoritative for a logical partition or run.

### Central model, mechanism, or theorem

A trustworthy batch trace joins several identity domains. The run links source snapshot, code/configuration, logical plan, optimized plan, physical DAG, stages, logical partitions, physical attempts, shuffle blocks, and committed output. Parent-child trees describe ordinary nesting, while links express retry, speculation, batch consumption, and fan-in that do not fit one tree.

For a dependency DAG with operation duration $d(v)$, earliest finish time is $F(v)=d(v)+\max_{u\in pred(v)}F(u)$, with the maximum over an empty predecessor set equal to zero. Job critical-path duration is $\max_v F(v)$. This recurrence attributes elapsed time without adding parallel work twice. Physical work, however, sums attempt durations and includes failed or losing speculative attempts. Both measures matter: critical path explains latency; total work explains resource cost.

### Critical invariants

- Every span resolves to exactly one run and one immutable plan/configuration/input identity.
- Logical stage and partition identities remain stable across physical retries, executor replacement, and speculation.
- Every attempt has a unique identity, terminal outcome, resource identity, and explicit relationship to its logical work.
- A downstream dependency names the accepted predecessor result, not merely the first completion event observed.
- Exactly one eligible attempt wins each committed logical output; losers cannot publish later.
- Span durations use a monotonic local clock; cross-host wall times are treated as approximate ordering evidence.
- Queue, execution, blocked, transfer, spill, fetch, and commit intervals have explicit semantics and do not silently overlap in aggregates.
- Sampling and telemetry loss are visible; an absent span is never interpreted automatically as zero time or no work.
- Attributes use bounded cardinality and exclude secrets, raw records, unrestricted queries, and unnecessary personal data.
- Traces correlate with durable engine event history, metrics, logs, manifests, and storage metadata rather than replacing them.

### Common failures

Common failures include using a job name as a unique run ID, attaching every retry directly to the job root, overwriting a logical task with its latest attempt, treating span trees as the execution DAG, summing parallel durations as latency, measuring queue time from submission rather than readiness, trusting cross-host wall clocks as exact causality, tracing the successful path but dropping failures, sampling before a late failure becomes known, creating one span per record, placing customer identifiers or SQL text in baggage, using high-cardinality metric labels, declaring output success before atomic commit, and relying on an interactive UI after its volatile history has expired.

### Compact example

One run is admitted at time 3. Two map partitions become ready at time 5. Partition 0 fails after six seconds, waits two seconds, and succeeds on a five-second retry; partition 1 succeeds in five seconds. Shuffle cannot start until both winning map outputs exist at time 18, then takes four seconds; reduce takes eight; commit takes two. End-to-end time is 32 seconds. Map attempt work is 16 seconds, including six failed seconds, but the map frontier completes at 18. The causal critical path passes through the failed and retried partition, while the other map runs in parallel. A trace that retained only winning attempts would hide both the delay and the wasted work.

### Connections

[LSDS-024](024-directed-acyclic-graph-execution.md) defines dependency structure, [LSDS-025](025-lazy-evaluation-and-plan-construction.md) separates logical and physical plans, [LSDS-026](026-stage-scheduling.md) explains readiness and admission, [LSDS-027](027-task-retry-and-speculation.md) supplies logical-versus-attempt identity, [LSDS-028](028-intermediate-data-materialization.md) defines intermediate artifacts, and [LSDS-029](029-checkpointing-long-computations.md) provides recovery boundaries. The trace binds those mechanisms into one inspectable execution narrative.

## Governing Question

A cluster engine converts a declarative request into thousands of distributed actions. The submission client sees one command. The driver may analyze and optimize several plans. A scheduler splits the physical graph at exchanges, creates logical tasks, waits for resources, launches attempts, retries failures, and accepts speculative winners. Workers read, compute, spill, transfer, merge, and report. A committer finally makes output visible.

When a run is slow or wrong, “the job took 47 minutes” is not a diagnosis. Did planning take ten minutes? Was a stage ready but queued? Did one partition read a pathological input split? Did a failed executor force a retry? Did shuffle fetch wait on missing blocks? Did the sink commit pause after all computation finished? Did telemetry omit the decisive attempt?

The governing question is therefore about causal reconstruction, not decorative timelines. A sound trace must preserve identity across abstraction levels, represent concurrency and retry honestly, distinguish observed evidence from inference, and remain useful under the very failures it is supposed to explain.

## Why This Matters

Batch engines amplify small causes. One skewed key can hold thousands of completed partitions behind a fan-in. A scheduler quota can leave all workers idle while a run appears “active.” A speculative copy can reduce latency but double remote reads. A late output commit can dominate wall time even though every compute metric looks healthy.

Diagnosis without causal structure encourages wasteful remedies. Adding executors does not repair a serialized planning bottleneck. Increasing memory does not fix queue policy. Raising retry limits can lengthen an outage caused by deterministic corruption. Turning on universal fine-grained tracing can overload collectors and add more latency than it explains.

Tracing also supports correctness. It can connect a published output manifest to the accepted task attempts and exact input snapshot, expose duplicate sink publication, and show whether a retry used compatible code and configuration. This evidence is useful for incident response, audit, capacity planning, performance regression analysis, and user-facing freshness explanations.

Telemetry itself creates risk. Span attributes can contain file paths, tenant names, queries, keys, record fragments, or infrastructure topology. A trace ID propagated through untrusted boundaries can become a tracking handle. Retention and access must match purpose. Observability is an engineered data product with accuracy, security, cost, and deletion obligations.

## Prerequisites and Retrieval

Retrieve distributed graphs, partition identity, data locality, failure domains, and work/state/movement accounting from [LSDS-005](005-distributed-task-graphs.md) through [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md). Retrieve block identity, metadata authority, checksums, and atomic publication from [LSDS-011](011-distributed-block-storage.md) through [LSDS-018](018-consistency-of-listings-and-metadata.md).

Review DAG execution, lazy planning, stage scheduling, retries/speculation, materialization, and checkpointing in [LSDS-024](024-directed-acyclic-graph-execution.md) through [LSDS-029](029-checkpointing-long-computations.md). You should understand partial orders, longest paths in DAGs, monotonic versus wall clocks, structured events, histograms, cardinality, sampling, immutable manifests, and idempotent commit.

## Learning Objectives

After this module, you should be able to:

1. distinguish traces, spans, logs, metrics, profiles, event histories, and audit records;
2. define stable run, plan, stage, logical task, attempt, artifact, and commit identities;
3. propagate context through drivers, schedulers, workers, queues, storage, shuffle, and sinks;
4. model fan-out, fan-in, retry, speculation, and batching with parent edges and span links;
5. compute and interpret critical-path latency, total physical work, failed work, and queue delay;
6. separate planning, readiness, admission, execution, blocking, transfer, spill, fetch, and commit time;
7. design useful bounded-cardinality attributes, events, and resource metadata;
8. choose head, tail, deterministic, failure-biased, and cohort sampling policies with explicit limitations;
9. validate trace completeness and reconcile traces with event logs, metrics, manifests, and storage evidence; and
10. govern telemetry access, redaction, retention, residency, deletion, and incident use.

## Core Exposition

### Begin with the questions the trace must answer

Instrumentation should start from operational questions. Examples are: why did this run miss its deadline; which dependency controlled completion; how much work was wasted by retry; which output files came from which winning attempts; why did a cohort of runs slow after an engine upgrade; and where did telemetry disappear?

Each question implies granularity. A stage-level trace can reveal admission delay but not partition skew. Attempt spans reveal skew and retry but may be too numerous to retain universally. Storage-operation spans help isolate throttling but can explode when a task reads many blocks. Record-level spans are almost never appropriate for a batch engine; aggregate counters, sampled exemplars, or profiles are safer.

Write the evidence contract before adding spans. Name the required identities, clocks, outcomes, cardinality limits, retention, sampling, and authoritative external records. Otherwise teams collect abundant timestamps that cannot be joined.

### The identity ladder

One human-facing job name may refer to a scheduled definition, many submissions, or many retries of an orchestrator workflow. Give each submitted cluster run a globally unique run ID. Bind it to the upstream workflow attempt, requester or service principal, code artifact digest, configuration digest, engine version, input snapshot, and intended output namespace.

Planning introduces more identities: unresolved request, analyzed logical plan, optimized logical plan, and selected physical plan. Store stable digests rather than whole queries or plans in ordinary span attributes. Keep full plans in controlled artifacts and link by digest and governed locator.

Execution introduces stage IDs and logical task IDs. A logical task usually corresponds to a partition in one stage. Attempts are children or linked executions of that logical work. Executor, process, host, container, and allocation IDs describe resources, not logical identity. An executor replacement changes resource identity but must not change which partition is being computed.

Artifacts also need identity. An accepted map attempt may produce multiple shuffle blocks. A reducer consumes blocks from many accepted producers. Candidate output files belong to attempts; a commit manifest names the winners. This ladder prevents a ubiquitous error: treating the latest attempt record as if it were the logical task.

### Trace, spans, events, metrics, and logs

A trace provides causal navigation. A span represents an operation with start and end, attributes, events, status, resource data, and relationships. Events are useful for discrete occurrences inside a span: allocation granted, spill started, fetch retry, cancellation requested, or commit won.

Metrics aggregate populations efficiently: queue-time distributions by pool, retry counts, spill bytes, fetch failure rates, collector drops, and run latency. Logs retain detailed statements and exception context. Profiles attribute CPU or allocation within executing code. Engine event histories often provide durable, replayable lifecycle records. Audit logs record controlled access and administrative changes.

No signal is universally authoritative. A trace may be sampled; a metric loses individual causality; a log may be duplicated; a UI may expire; a profile lacks scheduler state. Good instrumentation uses common identities so an investigator can move from an anomalous metric exemplar to a trace, then to attempt logs, event history, and output manifest.

### Submission and planning spans

Start the root run span when the engine accepts responsibility, while recording client-side submission separately if network or authentication delay matters. Mark transitions such as received, validated, admitted to planning, physical plan selected, scheduling begun, and terminal commit.

Plan spans should separate parsing/resolution, catalog access, analysis, optimization, physical selection, serialization, and broadcast. Capture plan digests, rule-set/configuration versions, counts of operators/stages/exchanges, and bounded reason codes. Do not attach raw SQL, literal predicates, secrets, full schemas, or unrestricted table paths by default.

If adaptive execution changes the plan, record a new physical plan version and the evidence frontier that caused it. Attempts must identify the plan version they executed. A single mutable “plan” field makes before-and-after work impossible to reconstruct.

### Scheduling and queueing spans

For each stage, record dependency-ready time, submission-to-scheduler time, admission time, first-launch time, all-partitions-complete time, and terminal stage outcome. These landmarks distinguish dependency wait, scheduler queue, launch ramp, active execution, and completion drain.

Queue time begins when work is eligible under dependency and policy constraints, not when the whole job was submitted. A downstream stage waiting for shuffle parents is blocked on dependencies, not queued for compute. Once ready, it may wait on quota, locality, resource shape, fairness, or unavailable executors. Use bounded reason codes plus changing resource demands and allocation observations.

Scheduler actions should carry the run context through internal queues. If the queueing system cannot preserve an ambient context, serialize a minimal signed or validated carrier containing trace identity and sampling decision. Never assume thread-local context survives asynchronous callbacks, process boundaries, or persisted work queues.

### Task and attempt spans

A logical task is not necessarily a timed physical operation, so it can be represented as a structured entity or lightweight coordination span. Each physical attempt gets its own span. Required fields include logical task ID, attempt ID, stage and partition, launch reason, resource identity, code/plan version, input identity, terminal outcome, failure classification, and winner/loser status.

Retry creates a sequence related to the same logical task. A retry may link to the failed attempt and the scheduler decision that launched it. Speculative attempts are concurrent siblings or linked executions. The accepted result event points to exactly one attempt; cancellation or late completion marks losers. This structure keeps wasted work visible.

Do not mark every canceled speculative attempt as an error. Status should reflect the operation contract. A healthy losing copy can be “canceled because another attempt committed,” while a corrupt input is a failure. Stable outcome classes support aggregation; exception strings belong in controlled events or logs.

### Worker execution

Within an attempt, useful child spans or timed events may include input open/read, deserialization, fused operator pipeline, aggregation, sort, spill, merge, compression, shuffle write, output staging, and acknowledgment. Granularity should follow diagnostic value and budget.

Counters belong on the attempt or in correlated metrics: input/output records and bytes, CPU time, wall time, blocked time, peak memory, allocation or garbage-collection pause, spill bytes/files, local versus remote bytes, fetch retries, and checksum failures. Clearly define whether bytes are logical, compressed, transmitted, or stored.

Nested span durations cannot simply be summed. Input reads may overlap decompression; asynchronous fetch may overlap compute; garbage collection pauses may be reflected in several observations. Use explicit mutually exclusive state accounting when a complete decomposition is required, and keep spans as causal evidence rather than pretending they automatically partition wall time.

### Shuffle and fan-in

Shuffle breaks ordinary call-stack intuition. One reducer consumes blocks from many map winners, often in batches and through shared fetch services. Making every producer span the parent of one reducer is impossible in a tree. Use a stable shuffle/exchange identity, artifact identities, and span links from reducer fetch or merge spans to selected producer attempts or block batches.

At very large fan-in, one link per block can be excessive. Retain aggregate counts and bytes, a digest or controlled manifest locator, all anomalous links, and a deterministic sample of ordinary links. The full shuffle service event history can remain the source of exhaustive block relationships.

Record map-output registration, fetch scheduling, connection wait, transfer, validation, decompression, merge, and missing-output recovery separately when the engine exposes them. A “shuffle took 12 minutes” label otherwise mixes producer delay, network, storage, receiver backpressure, and retry.

### Output staging and commit

Computation completion is not job completion. Attempts write candidate objects under unique attempt identities. The committer validates candidates, selects winners, creates or updates a manifest, atomically publishes the committed generation, and cleans losers. Trace each meaningful boundary.

The run’s success event must refer to durable commit identity and output manifest digest. A worker’s successful close is insufficient: another attempt may win, a checksum may fail, or publication may be rejected. Late attempts are fenced by run/generation and cannot overwrite committed output.

Capture candidate bytes/files, validation duration, object-store requests, conflicts, cleanup backlog, and visibility verification. Keep object names controlled because paths can reveal tenants, datasets, or personal identifiers.

### Context propagation across engine boundaries

Propagation moves trace context from submission gateway to driver, scheduler, allocation service, worker command, shuffle service, storage request, and sink. The carrier may be HTTP headers, RPC metadata, message attributes, task descriptors, or controlled manifest fields. Extraction validates format, size, trust boundary, and allowed fields.

Trace context is not authorization. Receiving a trace ID never grants access or establishes tenant identity. Baggage propagates application-defined properties and therefore deserves stricter allowlists; propagated values may reach logs and downstream services. Prefer opaque cohort or policy IDs over names and raw identifiers.

Shared services often handle work from many traces in one batch. A storage or shuffle batch span may link to multiple consumers rather than becoming the child of whichever request arrived first. Preserve the service’s own resource identity and do not falsify ownership for a prettier tree.

### Time and ordering

Use a monotonic clock for duration inside one process. Wall-clock timestamps help align hosts and external events but can skew, step, or have uncertain synchronization. A child appearing to start before its remote parent ends is not automatically impossible; asynchronous handoff and clock error are alternatives.

Causal relationships come from identifiers and recorded send/receive or produce/consume events. When exact cross-host latency matters, record both ends and clock uncertainty or use protocols designed to estimate it. Negative derived durations should be flagged as telemetry-quality problems, not clamped silently to zero.

Trace viewers often sort by timestamp, which can imply a total order that the distributed execution does not possess. Investigators should reason from the partial order: dependency readiness, command issuance, attempt acceptance, artifact registration, consumption, and commit.

### Critical path and work accounting

Given a dependency DAG, compute earliest finish by dynamic programming. Each node’s finish is its own duration plus the maximum predecessor finish. Backpointers recover one critical path. Retry backoff and failed attempts that must precede a successful retry are part of the causal path; concurrent speculative losers contribute work but not necessarily completion latency.

Compare several quantities:

- end-to-end elapsed time from accepted submission to durable commit;
- critical-path duration under the modeled dependencies;
- total physical attempt work, including failure and losing speculation;
- admitted resource-seconds, which can exceed active attempt work;
- CPU-seconds, blocked-seconds, bytes moved, and storage operations;
- queue and dependency wait by explicit readiness intervals.

Differences are informative. A large total-work-to-critical-path ratio may be healthy parallelism or waste. Large allocated-resource-seconds with low CPU and I/O can indicate admission mismatch or blocking. A computed critical path shorter than observed elapsed time signals missing nodes, incomplete dependencies, gaps, or clock problems.

### Sampling and retention

Head sampling chooses at trace start using information then available. It is cheap and consistent when propagated, but it can discard a trace that fails late. Tail sampling can retain errors, slow runs, rare cohorts, retries, or commit anomalies after observing more spans, but it requires buffering, timely arrival, and enough collector capacity.

Combine deterministic run-ID sampling for unbiased cohorts with mandatory or elevated retention for failures, deadline breaches, novel versions, recovery events, and security-relevant outcomes. Record the policy/version and whether each trace is complete, partial, or reconstructed. Failure-biased data cannot estimate population rates without selection weights or parallel metrics.

Span limits, event limits, attribute truncation, collector drops, export failures, and late arrivals must be observable. Telemetry backpressure should degrade instrumentation safely rather than stall core job execution. Durable engine events can support later reconstruction when live trace export fails.

### Cardinality and cost

Trace attributes may tolerate more uniqueness than metric labels, but neither is free. Run IDs are useful on spans and logs yet dangerous as metric dimensions. Partition and attempt IDs help inspect a selected trace; aggregate dashboards should use program, pool, engine version, bounded outcome, and controlled reason codes.

Budget spans per run, bytes per span, retained traces, collector CPU/memory/network, backend indexing, and query cost. Test worst-case fan-out, retry storms, and error events containing large stack traces. Use truncation that preserves hashes and explicit “truncated” flags rather than silently changing meaning.

### Validation and reconciliation

Test instrumentation with deterministic miniature jobs that include fan-out, retry, speculation, shuffle, and commit. Assert unique identities, parent/link validity, terminal outcomes, one winner, artifact lineage, and expected causal path. Inject collector loss, clock skew, executor death, duplicate delivery, and late events.

Reconcile trace-derived counts with authoritative engine event history: stages created, tasks expected, attempts launched, failures, accepted winners, shuffle blocks, and output files. Reconcile bytes and durations with metrics within declared tolerances. Validate manifest digests and plan/configuration identities.

A completeness score should describe evidence, not correctness. Examples include observed attempts divided by authoritative launched attempts, linked output files divided by committed files, and spans with valid resource identity divided by all attempt spans. Report the denominator and source.

### Security, privacy, and governance

Classify the telemetry schema. Prohibit credentials, authorization tokens, raw records, arbitrary queries, and unrestricted stack locals. Hashing a low-entropy customer name is not anonymization. Apply field allowlists, structured redaction before export, encryption, tenant isolation, access logs, and short purpose-based retention.

Propagated fields cross services and possibly regions. Enforce residency and purpose at collectors and backends. Support deletion or cryptographic erasure where required, while preserving nonidentifying aggregate operational evidence. Restrict trace-search APIs because rich correlations can reconstruct behavior even without payloads.

Document who can activate higher-detail tracing, for how long, under which incident, with which approval and automatic expiry. Emergency observability must not become permanent surveillance. Include platform operators, data owners, security/privacy reviewers, and affected service owners in schema and retention review.

## Definitions and Notation

Let $R$ denote one submitted run and $P_k$ its physical plan version $k$. Let $S_i$ be logical stage $i$, $T_{i,j}$ logical partition $j$ of that stage, and $A_{i,j,a}$ physical attempt $a$. Let $O_{i,j}$ be the single accepted output of logical task $T_{i,j}$ when successful.

For operation node $v$, $d(v)\ge 0$ is its measured or modeled duration, $pred(v)$ its causal predecessors, and $F(v)$ its earliest finish. Define:

$$
F(v)=d(v)+\max_{u\in pred(v)}F(u),
$$

where the maximum is zero when $pred(v)$ is empty. The modeled critical-path length is $L=\max_v F(v)$. Backtracking the maximizing predecessor yields one critical path; ties can yield several.

Let $W=\sum_a d(A_a)$ be total physical attempt wall-time work. Let $W_f$ sum failed attempts and $W_l$ sum losing speculative attempts. These sums are not job latency because attempts overlap. CPU work and allocated resource-seconds require separate measures.

For a logical task that becomes ready at $r$, is admitted at $m$, launches at $l$, and ends at $e$, dependency wait precedes $r$, scheduler queue is $m-r$ under the chosen admission semantics, launch delay is $l-m$, and attempt elapsed time is $e-l$. Exact engine definitions must be recorded.

A trace identifier groups spans; a span identifier names one span. Parent references express primary nesting, and links express additional causal associations. Resource attributes identify the producing service/process/container. Baggage is propagated application context and is not span data unless explicitly copied.

## Mechanisms, Invariants, or Proof Structure

Use this audit sequence for a batch trace:

1. Pin run, workflow, code, configuration, engine, input snapshot, plan version, and output generation identities.
2. Define the authoritative lifecycle events and the questions each trace element supports.
3. Model logical stages/tasks separately from attempts, resources, and candidate artifacts.
4. Propagate minimal validated context through every asynchronous and cross-process handoff.
5. Record readiness, admission, launch, execution, blocking, transfer, and commit with explicit interval semantics.
6. Represent fan-out and ordinary nesting with parents; represent batching, retry, speculation, and fan-in with links and artifact identities.
7. Fence attempts and prove exactly one accepted output per logical task and one durable run commit.
8. Compute critical path on the causal DAG and total work on physical attempts; never substitute one for the other.
9. Record sampling, truncation, dropped telemetry, clock uncertainty, and reconstruction status.
10. Reconcile against event history, metrics, logs, manifests, and storage metadata; then review access, retention, and deletion.

The critical-path recurrence follows by induction over a topological ordering. A source node finishes after its own duration. For any other node, it cannot start until every prerequisite is complete, so the earliest feasible start is the maximum predecessor finish. Adding its duration gives $F(v)$. The maximum terminal finish therefore gives the dependency-constrained completion time for the modeled graph.

This is a conditional proof, not proof that telemetry captured reality. Missing dependencies, inaccurate durations, resource contention not represented as nodes, asynchronous overlap, and clock error can invalidate the model. Compare computed $L$ with independently observed elapsed time and explain the residual.

Attempt fencing supports output uniqueness. Every candidate carries run, stage, partition, and attempt identity. The coordinator accepts at most one eligible attempt under an atomic decision and records it in authoritative metadata. Commit validates that every required logical output has one accepted candidate. Late or losing attempts cannot mutate the committed generation. A trace provides evidence of these transitions; the commit protocol enforces them.

## Alternatives and Trade-Offs

**Engine-native event history versus generic distributed tracing.** Native history understands stages, tasks, shuffle, and commit and may be durable. Generic tracing connects schedulers, storage, and upstream/downstream services. A joined design is strongest, but schema mapping and duplicate events require discipline.

**Coarse versus fine spans.** Run and stage spans are affordable and stable but hide partition skew. Attempt and I/O spans enable diagnosis at much higher volume. Use adaptive detail, anomaly events, profiles, and deterministic exemplars.

**Parent trees versus link-rich DAGs.** Trees render simply and support common trace tools. Links represent real many-to-many causality but can overwhelm storage and viewers. Preserve exhaustive relationships in manifests/event history and link selected or aggregated evidence.

**Head versus tail sampling.** Head sampling bounds ingestion early and preserves a consistent propagated decision. Tail sampling retains late failures and slowness but needs buffers and can lose decisions during collector failure. Metrics and durable histories remain necessary under both.

**Wall-clock alignment versus causal ordering.** Synchronized clocks give intuitive timelines. Explicit produce/consume and command/acknowledgment edges withstand skew. Use both, and expose uncertainty.

**Ambient propagation versus explicit task descriptors.** Ambient context is convenient inside synchronous call stacks. Explicit serialized carriers survive queues and process boundaries and are easier to validate. Cluster engines usually need both.

**Full identifiers versus privacy-preserving correlation.** Rich identifiers speed incidents but raise disclosure and access risk. Use opaque scoped IDs, controlled lookup services, short retention, and role-based reveal rather than raw customer or dataset names.

**Always-on detail versus incident activation.** Always-on traces support baselines and rare-event capture. Activated detail controls cost and exposure but misses pre-activation history. A coarse always-on layer plus bounded, approved high-detail windows is often defensible.

## Failure Modes and Misconceptions

**“The trace tree is the batch DAG.”** A span tree permits one parent; shuffle and batched services have many causes. Use links and artifact/dependency metadata.

**“One task has one span.”** Retries and speculation create multiple attempts. Logical identity and physical attempt identity must be distinct.

**“The longest span is the bottleneck.”** Completion follows a chain of dependencies. Several shorter sequential spans can dominate; one long parallel loser may not affect completion.

**“Sum of spans equals latency.”** Parallel and nested spans overlap. Sum measures neither elapsed time nor necessarily resource work.

**“Queue time starts at job submission.”** Work is not queued for resources until dependencies and policy make it eligible. Record readiness explicitly.

**“Timestamps establish causality.”** Remote clocks can skew, and asynchronous work can overlap. Use propagated identities and send/receive or produce/consume edges.

**“Success means worker output closed.”** Only accepted and durably committed output is authoritative. Candidate creation, winner selection, and publication differ.

**“No span means no work.”** Sampling, truncation, late arrival, exporter failure, and collector drop produce absence. Record completeness.

**“Tail sampling captures every failure.”** It depends on receiving enough spans and keeping state until the decision. Collector or network failure can defeat it.

**“A trace ID is safe baggage.”** Correlation identifiers and baggage can cross trust boundaries, appear in logs, and enable tracking. Scope and govern them.

**“High cardinality is only a metrics problem.”** Unique attributes also drive trace index cost, retention, and query exposure. Choose indexed fields deliberately.

**“Tracing replaces event logs.”** Durable engine history and manifests remain critical for exhaustive lifecycle and correctness reconciliation.

## Worked Examples

### Example 1

A nightly run has workflow definition `sales-daily`, workflow attempt 812, and cluster run `r-7f3`. The root span stores `r-7f3`, code digest, configuration digest, engine version, input snapshot, and output generation. Dashboards aggregate by stable program and outcome, not the unique run ID. An investigator can still join the run to controlled plan and manifest artifacts.

### Example 2

Stage 4 is submitted at time 20 but its last parent finishes at 41. Quota admission happens at 47 and its first attempt launches at 49. Dependency wait is 21 seconds, ready queue is 6, and launch ramp is 2. Calling all 29 seconds “scheduler queue” would send operators toward the wrong policy.

### Example 3

Partition 9 has attempt 0 on executor 12, fails checksum validation, and retries as attempt 1 on executor 33. Both share one logical task ID. Attempt 1 wins; the commit manifest points to its candidate. Keeping only the latest attempt would erase the checksum failure and six seconds of wasted work.

### Example 4

Two speculative attempts run concurrently. The slower original consumes 40 CPU-seconds before cancellation; the copy consumes 25 and wins. Logical latency is 25 seconds after speculation launch, physical CPU cost is 65 seconds, and losing work is 40. Neither number substitutes for the other.

### Example 5

A reducer fetches 50,000 map blocks. The trace records exchange ID, total blocks/bytes, fetch batches, every failed block link, and a deterministic sample of normal producer links. A governed shuffle manifest preserves the exhaustive mapping without placing 50,000 links on one span.

### Example 6

Host A records command send at wall time 10.020; host B records attempt start at 10.011. Rather than inventing negative network latency, the trace shows the command/attempt identity edge, local monotonic durations, and clock uncertainty. Time synchronization is repaired separately.

### Example 7

A head sampler keeps one percent of runs. A rare commit failure appears after 45 minutes, but that run was discarded at submission. Failure metrics and durable events still count it. A tail policy could improve retention only if the collector receives and buffers the relevant evidence.

### Example 8

An engineer adds `run_id` and `partition_id` as metric labels. Series count explodes. The corrected design keeps those values on sampled spans and logs, while metrics aggregate by pool, engine version, stage class, and bounded outcome, with exemplars linking selected observations.

### Example 9

All compute attempts finish by minute 18, yet the run completes at minute 27. Commit spans show eight minutes validating 400,000 candidates and one minute publishing a manifest. Adding compute workers cannot improve this critical path; reducing candidate count or redesigning commit might.

### Example 10

The following local fixture computes attempt work and a dependency-constrained completion path for a small retried batch. It models causal arithmetic, not a real tracer, scheduler, or distributed clock system.

<!-- bijux-verify: {"id":"batch-trace-critical-path","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"winner_attempts=(('map-0', 'attempt-1'), ('map-1', 'attempt-0'))\nmap_attempt_work=16 failed_work=6\ncritical_path=('admit', 'readiness', 'map-0/attempt-0', 'retry-backoff', 'map-0/attempt-1', 'shuffle', 'reduce', 'commit') duration=32\n","stderr":""}} -->
```python
nodes = {
    "admit": (3, ()),
    "readiness": (2, ("admit",)),
    "map-0/attempt-0": (6, ("readiness",)),
    "retry-backoff": (2, ("map-0/attempt-0",)),
    "map-0/attempt-1": (5, ("retry-backoff",)),
    "map-1/attempt-0": (5, ("readiness",)),
    "shuffle": (4, ("map-0/attempt-1", "map-1/attempt-0")),
    "reduce": (8, ("shuffle",)),
    "commit": (2, ("reduce",)),
}

finish = {}
previous = {}
for name, (duration, predecessors) in nodes.items():
    predecessor = max(predecessors, key=finish.get) if predecessors else None
    finish[name] = duration + (finish[predecessor] if predecessor else 0)
    previous[name] = predecessor

path = []
cursor = max(finish, key=finish.get)
while cursor is not None:
    path.append(cursor)
    cursor = previous[cursor]
path.reverse()

winners = (("map-0", "attempt-1"), ("map-1", "attempt-0"))
map_work = 6 + 5 + 5
failed_work = 6
print(f"winner_attempts={winners}")
print(f"map_attempt_work={map_work} failed_work={failed_work}")
print(f"critical_path={tuple(path)} duration={max(finish.values())}")
```

The toy graph separates three seconds to admission from two seconds to map readiness. A production model would further distinguish submission, planning, dependency readiness, queueing, launch, and resource contention.

## Cross-Program Connections

- **Distributed systems:** trace context and causal edges operationalize partial orders, message causality, retries, and failure domains without assuming a global clock.
- **Algorithms and graph theory:** topological dynamic programming recovers critical paths; graph compression and sampling preserve selected evidence under extreme fan-out.
- **Operating systems:** queue, service, blocked, CPU, I/O, memory pressure, and scheduling states explain attempt behavior below the engine abstraction.
- **Networking:** propagation, RPC metadata, batching, retries, connection queues, congestion, and clock uncertainty shape cross-service observations.
- **Storage systems:** shuffle blocks, candidate files, checksums, manifests, atomic publication, listings, and cleanup connect spans to durable facts.
- **Databases:** stable query/plan digests, transaction identity, commit fencing, idempotency, and lineage distinguish candidate effects from visible outcomes.
- **Software engineering:** semantic conventions, versioned schemas, bounded attributes, compatibility tests, and fixture-based validation make instrumentation maintainable.
- **Security and privacy:** telemetry is sensitive correlated data requiring minimization, isolation, access control, redaction, retention, residency, and audit.
- **Reliability engineering:** traces complement SLO metrics and event histories to identify critical delays, wasted retries, incomplete recovery, and collector failure.
- **Human factors:** a visualization can imply false order or certainty; explicit completeness, clock uncertainty, and evidence provenance support responsible incident decisions.

## References

1. OpenTelemetry, [Traces](https://opentelemetry.io/docs/concepts/signals/traces/), accessed 2026-09-03.
2. OpenTelemetry, [Context Propagation](https://opentelemetry.io/docs/concepts/context-propagation/), accessed 2026-09-03.
3. OpenTelemetry Specification, [Tracing API](https://opentelemetry.io/docs/specs/otel/trace/api/), accessed 2026-09-03.
4. OpenTelemetry Semantic Conventions, [Trace Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/general/trace/), accessed 2026-09-03.
5. OpenTelemetry, [Sampling](https://opentelemetry.io/docs/concepts/sampling/), accessed 2026-09-03.
6. OpenTelemetry, [Baggage](https://opentelemetry.io/docs/concepts/signals/baggage/), accessed 2026-09-03.
7. Apache Spark, [Monitoring and Instrumentation](https://spark.apache.org/docs/latest/monitoring.html), accessed 2026-09-03.
8. Apache Spark, [Job Scheduling](https://spark.apache.org/docs/latest/job-scheduling.html), accessed 2026-09-03.
9. Apache Flink, [Metrics](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/metrics/), accessed 2026-09-03.
10. Apache Hadoop, [MapReduce Tutorial](https://hadoop.apache.org/docs/stable3/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html), accessed 2026-09-03.
11. Dask, [Diagnosing Performance](https://distributed.dask.org/en/stable/diagnosing-performance.html), accessed 2026-09-03.
12. Benjamin H. Sigelman et al., [Dapper, a Large-Scale Distributed Systems Tracing Infrastructure](https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/), 2010.

## Exercises

### Exercise 1

A stage is submitted at second 0, becomes dependency-ready at 14, is admitted at 23, launches its first attempt at 25, completes all accepted partitions at 61, and commits stage metadata at 64. Compute dependency wait, ready queue, launch delay, active-to-accepted completion, and commit tail. Explain which intervals can be improved by more executors.

### Exercise 2

Design identities and span/link relationships for a logical partition with one failed attempt followed by two concurrent speculative attempts, one of which wins. Include candidate artifact and commit evidence, and state how each loser terminates.

### Exercise 3

Given nodes `plan=4`, `queue=7` after plan, parallel maps `m0=12` and `m1=20` after queue, `shuffle=6` after both maps, `reduce=9`, and `commit=3`, compute the critical path and duration. Compute total listed operation work and explain why it differs.

### Exercise 4

Propose a sampling and reconciliation policy for 200,000 daily batch runs where one percent exceed 30 minutes, failures are rare, and attempt spans would exceed the telemetry budget if universally retained. Address unbiased analysis, late failures, collector loss, and completeness.

### Exercise 5

Specify a telemetry governance review for a multi-tenant batch platform whose current spans contain raw SQL, object paths with customer names, user emails in baggage, unique run IDs as metric labels, and 400-day retention. Include immediate controls and durable validation.

## Answers to the Exercises

### Answer 1

Dependency wait is 14 seconds, ready queue is $23-14=9$, launch delay is $25-23=2$, active-to-accepted completion is $61-25=36$, and commit tail is $64-61=3$. More executors may reduce the nine-second queue if compute capacity rather than quota, locality, or resource shape is binding; they may also reduce launch ramp and active work if tasks parallelize and are not bottlenecked elsewhere. They cannot reduce the 14-second parent dependency merely by being added to this stage, and they do not directly repair a serialized three-second metadata commit. Evidence about allocation, task parallelism, skew, and committer behavior is required.

### Answer 2

Assign one run ID, physical plan version, stage ID, and logical task ID. Create unique attempt IDs `a0`, `a1`, and `a2`; link `a1` and `a2` to the failed `a0` and the scheduler’s retry/speculation decisions. Record `a0` as failed with bounded cause. Both speculative attempts use the same logical input identity but distinct resource and candidate artifact identities. An atomic winner decision accepts, for example, `a2`; the manifest maps the logical output to `a2` and its checksum. Mark `a1` canceled or completed-loser according to observation, with a winner reference. Fence both `a0` and `a1` from publication and retain their work/cost evidence.

### Answer 3

The critical path is `plan → queue → m1 → shuffle → reduce → commit` because `m1` is the slower prerequisite. Duration is $4+7+20+6+9+3=49$ seconds. Total listed work is $4+7+12+20+6+9+3=61$ seconds. The 12-second `m0` operation overlaps `m1`, so it consumes work but adds no time beyond the slower fan-in predecessor in this model. If queue represents waiting rather than executing work, even the 61-second sum is not resource consumption; CPU, allocation, and I/O need their own measures.

### Answer 4

Keep low-volume run/stage lifecycle evidence and authoritative engine events for all runs. Deterministically sample runs by a stable hash at a known rate for unbiased population analysis, preserving selection probability. Use tail sampling to retain deadline breaches, failures, retries, new engine/configuration cohorts, and commit anomalies, with enough buffering for expected duration. Metrics independently count all outcomes and latencies. Export sampling-policy version, truncation and drop counters, and per-trace completeness. Reconcile sampled attempt counts against event history and committed manifests. If collector loss prevents a tail decision, mark reconstruction and rebuild selected evidence from durable history rather than calling the trace complete.

### Answer 5

Immediately stop exporting raw SQL, emails, and customer-bearing paths; replace them with governed digests or opaque scoped IDs and revoke broad trace access. Remove run ID from metric dimensions and cap retention according to incident and operational purpose while legal/privacy owners determine deletion. Define an allowlisted versioned schema, redaction at instrumentation and collector boundaries, baggage allowlists, encryption, tenant/region isolation, role-based lookup, access audit, break-glass detail with expiry, and deletion procedures. Test fixtures containing secrets and identifiers, cardinality budgets, cross-region routing, authorization, retention expiry, erasure, and collector failure. Named review includes platform and engine owners, data/service owners, security, privacy/legal/records, identity/access, observability operators, and representatives responsible for affected tenants. Re-audit sampled exports and backend indexes continuously rather than trusting configuration alone.
