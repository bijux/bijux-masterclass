---
module_id: DE-044
program: Data Engineering
level: 1
module_number: 44
title: Retries, Timeouts, and Idempotency
status: complete
last_verified: 2026-09-03
---

# Retries, Timeouts, and Idempotency

## One-Page Review

### Governing question

How should a data workflow repeat failed attempts, stop waiting, and recover uncertain outcomes without duplicating, omitting, regressing, or partially publishing the logical data effect?

### Essential definitions

- A **logical work unit** is one stable data obligation, such as materializing one asset partition from exact input generations under one transformation contract.
- An **attempt** is one physical execution of a logical work unit. Retries create new attempts, not new logical meaning.
- A **retry** is a policy-authorized later attempt after a classified failure or uncertain outcome.
- A **timeout** bounds how long an observer waits for an operation or phase. It is evidence about waiting, not proof that remote work stopped or rolled back.
- A **deadline** is the latest useful instant for an enclosing operation; every nested timeout, wait, and retry must fit within its remaining budget.
- **Backoff** delays retries; **jitter** randomizes delay so correlated failures do not produce synchronized retry waves.
- **Idempotence** means repeating the same logical operation produces the same intended observable effect within an explicitly named boundary.
- An **idempotency key** is a stable identifier for a logical effect, scoped and bound to a canonical intent fingerprint.
- A **receipt** is durable authoritative evidence mapping a logical identity to its accepted intent and outcome.
- An **ambiguous outcome** means the caller cannot distinguish committed success from non-execution, commonly after timeout or lost acknowledgement.
- A **candidate generation** is attempt-produced output that remains invisible until validation and fenced publication accept it.
- **Reconciliation** compares intended work and authoritative effects/receipts to resolve uncertainty without guessing from an attempt error.

### Central model, mechanism, or theorem

Let logical work be

$$
w=(n,k,h,v,I,O,D),
$$

where $n$ is scope, $k$ stable work/effect key, $h$ canonical intent digest, $v$ transformation contract version, $I$ exact inputs, $O$ expected outputs, and $D$ the business deadline. Attempt $a_i$ may run only when its failure class is retryable, identity remains unchanged, load/attempt budgets permit it, and

$$
t + delay_i + setup_i + useful_i + reconcile_i \le D.
$$

For authoritative state $S$ and intended transition $F_w$, bounded idempotence requires

$$
F_w(F_w(S))=F_w(S)
$$

over the declared observable boundary. A timeout never establishes which side of $F_w$ occurred. The recovery protocol first queries the receipt or target state for $(n,k,h,v)$; matching success is reused, absence permits a safe same-key attempt, and conflict or unresolved uncertainty fails closed. Candidate output is published by one conditional transition, so losing attempts cannot overwrite the winner.

### Critical invariants

- Every attempt preserves logical work identity, exact inputs, canonical intent digest, contract version, tenant/environment scope, deadline, and expected outputs.
- Attempt ID, worker, start time, retry number, and candidate location are physical metadata and never replace the logical key.
- Failure classification distinguishes transient, permanent, overload, cancellation, deadline, deterministic data, capacity, conflict, and ambiguous-outcome states.
- A timeout bounds waiting at a named layer and phase; it does not assert remote cancellation, rollback, or absence of side effects.
- One owner coordinates retries across orchestrator, task code, SDK, database driver, broker, and service mesh; aggregate attempts remain bounded.
- Attempts, total elapsed retry window, backoff, jitter, business deadline, workload age, and fleet retry load have independent limits.
- Same key plus different fingerprint is an identity conflict, never an accepted retry.
- Durable uniqueness, compare-and-set, transactional receipt coupling, or equivalent arbitration protects concurrent first attempts.
- Each non-transactional external effect has its own stable effect identity and outcome lookup, outbox/inbox boundary, or explicit reconciliation/compensation protocol.
- Attempt outputs stay isolated as candidates; publication is validated, atomic for its named boundary, fenced against stale attempts, and observable.
- Completion requires application/data acceptance evidence, not merely process exit zero, worker acknowledgement, or orchestrator success.
- Receipt, input, candidate, checkpoint, and deduplication retention cover the maximum retry, replay, correction, and audit horizon or have a safe rebuild/migration protocol.

### Common failures

Retry every exception; retry deterministic bad data; set a new work key on each attempt; infer rollback from timeout; restart a full deadline for every attempt; let nested layers multiply attempts; use deterministic backoff across a fleet; sleep in scarce worker slots; retry overload without pushback or budget; claim idempotence because a function is named `upsert`; check then insert without uniqueness; record a success marker before the effect or after it in a separate commit; publish directly to a shared mutable destination; let a timed-out stale attempt publish after its replacement; reuse a key for different inputs; expire receipts while retries remain possible; rerun an entire batch when only item outcomes are known; perform email, billing, export, or message effects inside a retried database transaction; treat broker exactly-once as a universal end-to-end guarantee; count attempt success rather than accepted output; and delete failure evidence before reconciliation.

### Compact example

Four partition work units use a 400 ms deadline, capped deterministic demonstration delays, stable effect keys, and receipt lookup. Unit A fails transiently then succeeds. Unit B commits its effect but loses the acknowledgement; reconciliation finds its receipt and does not call the effect again. Unit C has invalid data and stops after one attempt. Unit D fails twice, then suppresses a third attempt because delay plus minimum useful time cannot fit. Six calls create two accepted publications, zero duplicate effects, one recovered ambiguous outcome, and one deadline-suppressed retry. **Conclusion:** retry success is governed by stable meaning and authoritative outcome evidence, not by repeating code until it stops raising errors.

### Connections

[DE-027](027-idempotent-loads.md) establishes durable load receipts; [DE-041](041-directed-acyclic-graphs-and-dependencies.md) and [DE-042](042-tasks-jobs-assets-and-datasets.md) define logical graph/run objects; [DE-043](043-scheduling-and-event-triggered-execution.md) creates run intent. DE-045 specializes partition generations, DE-046 governs historical plans, and DE-049 develops operational state. API and Platform Engineering provide dependency-level deadline/retry and workload-controller mechanisms, but this module owns data-effect correctness.

## Governing Question

For one data obligation, which failures permit another attempt, what evidence resolves uncertain commits, how do all waits fit one deadline and retry-load budget, and what mechanism guarantees that overlapping or repeated execution produces exactly one accepted logical effect within a declared boundary?

The question deliberately separates availability from correctness. Another attempt may recover from a dead worker, leader change, lock conflict, transient connection failure, or temporary dependency unavailability. The same attempt can amplify an overloaded warehouse, repeat an additive load, regress a corrected partition, send a duplicate notification, or allow a stale worker to publish after a newer one.

The orchestrator usually sees incomplete evidence. A task timeout says its observer stopped waiting. A lost heartbeat says the worker is not currently proving liveness. A process exit code says what that process reported. A broker acknowledgement says something about delivery state. None alone proves whether a database transaction committed, an object became visible, a remote export was accepted, or consumers observed a publication.

Therefore the retry decision must be made against one stable logical work record and a declared effect protocol. The record binds input generations, code/schema/config versions, output identity, tenant, authority, deadline, retry policy, and acceptance rule. Each attempt has separate operational identity. Durable receipts, target constraints, candidate manifests, external provider keys, and reconciliation provide the evidence that turns ambiguous execution into a safe decision.

## Why This Matters

Data systems routinely execute work whose duration and blast radius exceed a synchronous request. A partition may scan terabytes, write many objects, update catalog state, notify consumers, and trigger downstream jobs. Transient failure is inevitable across that path. A blanket “no retries” rule converts recoverable infrastructure faults into missing data. A blanket “retry three times” rule converts ambiguous or deterministic failures into corruption and load amplification.

The most dangerous interval is commit uncertainty. Suppose an attempt commits a warehouse transaction and loses its response. The orchestrator records timeout. Retrying an append doubles rows; marking failed omits a successful partition from lineage. The attempt result is not authoritative enough to choose. A target-side receipt coupled to the transaction, or a queryable published generation under a stable key, can distinguish success from absence. Where the effect is external and not queryable, the system must preserve an `unknown` state and reconcile or require manual adjudication rather than invent certainty.

Retries also change capacity dynamics. When a database slows, tasks time out and release retries. Those retries add connections, scans, writes, locks, and metadata calls to the impaired system. Multiple retrying layers multiply work. If an orchestrator allows four attempts, a client library three, and a database wrapper three, a logical unit can cause up to $4\times3\times3=36$ deepest attempts. A thousand failing partitions can therefore become 36,000 calls unless ownership and fleet budgets constrain the system.

Timeouts can create overlap. Cancellation is cooperative in many runtimes and remote systems. A timed-out attempt may continue after the controller starts its replacement. If both write to the final partition, “last finisher wins” can publish old code or incomplete input. Candidate isolation plus publication fencing makes the accepted generation a deliberate transition. The losing attempt may finish physically, but it cannot become logically visible.

Idempotency makes retries operationally ordinary, yet the claim must be bounded. Repeating a transformation may leave target rows unchanged while duplicating audit records, downstream events, provider charges, storage cost, or notifications. Conversely, attempt logs should record every physical attempt even when the business/data effect occurs once. State the observable boundary and prove each side effect or explicitly exclude it.

Well-designed retry state improves audits and incident response. Operators can answer which work was intended, which attempts ran, why each failed, whether an ambiguous effect was found, which candidate won, what was published, and why further retries stopped. Without that evidence, “rerun it” is not a recovery strategy; it is a wager.

## Prerequisites and Retrieval

Retrieve [Idempotent Loads](027-idempotent-loads.md), [Testing a Multi-Stage Batch Pipeline](040-testing-a-multi-stage-batch-pipeline.md), [Directed Acyclic Graphs and Dependencies](041-directed-acyclic-graphs-and-dependencies.md), [Tasks, Jobs, Assets, and Datasets](042-tasks-jobs-assets-and-datasets.md), and [Scheduling and Event-Triggered Execution](043-scheduling-and-event-triggered-execution.md). Distinguish a planned run request from a physical attempt and a successful attempt from an accepted materialization.

Inventory every retrying layer: scheduler/orchestrator, queue or broker, worker runtime, task wrapper, HTTP/RPC SDK, service mesh/proxy, database driver, transaction wrapper, storage SDK, and provider. Record defaults, total-attempt interpretation, retryable codes, hidden transparent retries, delays, jitter, timeout phase, deadline propagation, connection reuse, and telemetry. “The task retries twice” is incomplete when its SDK silently retries five calls per attempt.

Retrieve the work and effect contract: stable work key; tenant/environment/target namespace; exact input manifests and generations; canonical intent fingerprint; transformation artifact, schema, configuration, and policy versions; output partition/generation identity; row/event keys and version rules; transaction/isolation/conditional-write semantics; target uniqueness; candidate storage; publication pointer or catalog transaction; receipt store; checkpoints; external side effects; downstream events; acceptance controls; rollback/retraction; and consumer freshness expectation.

Retrieve failure evidence and recovery semantics: process exit and signal meanings; heartbeat/liveness; orchestrator task states; database error classes; serialization/deadlock semantics; object-store write/list consistency assumptions; API status/application codes; `Retry-After` or pushback; provider idempotency/outcome lookup; broker acknowledgement and redelivery; cancellation behavior; commit uncertainty; stale-attempt fencing; reconciliation queries; manual override authority; and incident runbooks.

Retrieve temporal and capacity constraints: logical work deadline/expiry; phase timeouts; connection/setup cost; minimum useful attempt duration; cleanup and reconciliation reserve; maximum attempts; total retry age; backoff cap; jitter algorithm; concurrency pools; per-tenant/source/warehouse limits; fleet retry budget; source and sink rate limits; catch-up/backfill capacity; queue age; and overload shedding. Time and attempt caps solve different problems and both are necessary.

Retrieve retention/security controls: receipt and idempotency horizon; input reproducibility; checkpoint lifetime; candidate cleanup; attempt-log retention; audit/legal holds; sensitive error redaction; tenant isolation; authorization on manual retry/cancel/override; service identity lifetime; secret refresh; output encryption and access; and deletion requirements. An expired credential can be refreshed under policy; a revoked authorization cannot be bypassed merely because the original attempt once started.

Before implementation, write a retry contract table:

| Concern | Required decision and evidence |
|---|---|
| Logical identity | Namespace, stable key, fingerprint, exact inputs and versions |
| Attempts | Owner, total limit, attempt IDs, worker/candidate identity |
| Failure classes | Retry, stop, reconcile, replan, quarantine, or operator action |
| Time | Original deadline, phase timeouts, reserves, cancellation semantics |
| Load | Backoff, jitter, concurrency, retry tokens, overload pushback |
| Primary effect | Transaction/uniqueness/CAS, receipt coupling, outcome query |
| Publication | Candidate isolation, validation, fencing token, accepted pointer |
| External effects | Provider key, outbox/inbox, lookup, compensation, unknown state |
| Evidence | Attempts, causes, receipts, candidates, controls, lineage, final disposition |
| Retention | Retry/replay horizons, cleanup, audit, rebuild and key migration |

## Learning Objectives

After completing this module, you should be able to:

1. distinguish logical work, physical attempts, retries, redelivery, replay, recomputation, correction, and new intent;
2. classify deterministic, transient, overload, capacity, conflict, cancellation, deadline, and ambiguous-outcome failures;
3. allocate phase timeouts and attempt budgets within one immutable business deadline;
4. design capped backoff, jitter, pushback, concurrency, and fleet retry-load controls;
5. define idempotence for a named observable boundary and bind a stable key to canonical intent;
6. recover timeout-after-commit using receipts, target lookup, or explicit reconciliation rather than inference;
7. isolate candidates and fence publication so stale or overlapping attempts cannot become visible;
8. extend retry safety across database, object, broker, and external-provider boundaries without claiming impossible global atomicity;
9. test crash points, duplicate delivery, hidden retries, timeouts, concurrency, stale attempts, receipt expiry, and overload; and
10. operate retry queues using evidence, metrics, runbooks, retention, and authorized manual controls.

## Core Exposition

### Separate logical work from physical attempts

Create the logical work unit before execution. A useful immutable record includes the job/asset definition and version, partition or bounded scope, exact input generation manifest, parameters, canonical intent digest, output contract, tenant/environment, request provenance, deadline, and retry-policy version. Its key must survive controller restart, worker replacement, failover, and replay in a recovery environment.

Each physical attempt gets its own attempt ID, attempt ordinal, worker/runtime identity, admission/start/end timestamps, code artifact, credential reference, lease/fencing token, checkpoint, candidate output location, resource usage, structured failure, and disposition. Attempts can be numerous; logical meaning remains one.

Do not derive the logical key from start time, scheduler try number, random attempt UUID, pod name, or output temporary path. Those change precisely when retry occurs. Conversely, do not collapse a correction into a retry: changed input generation, transformation contract, authorized parameter, or expected effect usually creates a new work fingerprint and often a new logical generation linked to the prior one.

A retry is not the same as backfill or replay. Retry repeats one unchanged logical obligation because prior completion is absent or uncertain. Replay may redeliver recorded events. Backfill plans many historical obligations. Recompute may use changed code or inputs. Preserve provenance because approval, capacity, lineage, and consumer interpretation differ.

### Build a failure decision matrix

Classify with structured evidence rather than exception text alone. Include phase—admission, setup, read, transform, candidate write, validation, commit, publication, notification, cleanup—because the same transport error has different ambiguity after a possible effect.

Typical decisions are:

- invalid schema, corrupt input, violated invariant, unsupported version, missing required partition after deadline, or deterministic code error: quarantine/fail and correct meaning; unchanged retry is waste;
- authentication expiry with valid continuing authority: refresh once under policy; invalid credentials or revoked authority stop;
- authorization/policy rejection: terminal until a newly authorized operation is created, not a hidden retry;
- resource request too large or incompatible placement: replan capacity/configuration; immediate identical retry is not recovery;
- transient connection, leader election, worker loss before effect, deadlock, or serialization abort: potentially retry with unchanged identity and bounded backoff;
- rate limit/overload: honor pushback, spend retry/load budget, reduce concurrency, or defer; more immediate work can deepen failure;
- precondition/version conflict: reread and decide whether unchanged work is obsolete, must be recomputed as new intent, or can repeat after transaction rollback;
- timeout/reset after possible commit: mark outcome unknown and query receipt/target/provider before another effect;
- cancellation: stop admission and signal attempts, but reconcile because cancellation acknowledgement may not imply rollback;
- candidate validation failure: terminal for that candidate; retry only if evidence suggests nondeterministic infrastructure rather than deterministic data/code;
- cleanup failure after accepted publication: record cleanup obligation separately; do not republish the partition.

Machine-readable failure records should carry stable class, phase, retryability decision, ambiguity flag, dependency, provider code, bounded diagnostic fingerprint, first/last occurrence, attempt, remaining budget, and recommended next action. Redact secrets and sensitive row values. Operators need enough detail to distinguish one recurring cause from a fleet-wide incident.

### Treat timeouts as observation boundaries

A timeout is local to an observer and phase. Connect timeout bounds establishment; read timeout bounds a period of waiting for data; statement timeout may request database interruption; task execution timeout bounds orchestration waiting; heartbeat timeout detects missing liveness evidence; business deadline bounds usefulness. Name each one.

Timeout does not mean cancellation. A client can stop waiting while a server continues. A worker can lose its lease while its process remains alive. A database may receive cancellation after commit. A subprocess can ignore graceful termination. Therefore a controller that starts replacement work must assume overlap unless authoritative evidence proves the old attempt cannot affect the target.

Use an absolute deadline $D$ for the logical operation. At time $t$, remaining budget is $B=D-t$. Before a later attempt, require room for chosen delay, setup, minimum useful work, response/commit evidence, and reconciliation/cleanup reserve. Do not restart the original duration on every attempt. Clock representation and propagation must be explicit; use monotonic elapsed measurement locally and a governed wall-clock/deadline representation across processes.

Timeout values come from service objectives and measured distributions, not arbitrary round numbers. A timeout below normal cold-start or query duration causes self-inflicted retry load. One above the usefulness window wastes resources and allows stale publication. Examine tail latency by workload class and phase, while preserving enough reserve to determine outcome safely.

### Bound retries across every dimension

Set total attempts including the initial attempt. If a product exposes `max_retries`, translate it explicitly to total attempts. Also cap elapsed retry age, work deadline, queue age, per-attempt duration, and repeated identical failure count. A cap on attempts alone can wait for days; a time cap alone can spin thousands of times.

Use capped exponential backoff for failures whose recovery probability changes with time:

$$
d_i=\min(c,bg^i),
$$

where $b$ is base, $g>1$ multiplier, $c$ cap, and $i$ retry index. Add jitter to desynchronize correlated failures. Full jitter samples $J_i\sim U(0,d_i)$; other algorithms have different minimum delay and correlation behavior. State the algorithm, seed behavior, duration units, cap, and reset rule. Jitter spreads work but does not reduce total demand.

Honor valid server or platform pushback as policy input without exceeding the original deadline. A suggested retry time that arrives after expiry means stop or persist work for a newly authorized asynchronous window; it is not permission to extend business intent silently.

Retry budgets must include fleet load. Per-work-unit `three attempts` still triples a million-unit incident. Limit retry rate and concurrency by dependency, warehouse, tenant, workload class, and global failure domain. Spend tokens on retries, reserve capacity for new useful work and recovery probes, and replenish based on sustained health rather than process restart. Autoscaling must not manufacture retry tokens.

### Assign one retry owner

List all retry-capable layers, then assign ownership for the logical operation and for each dependency call. The logical-work owner knows identity, deadline, data semantics, and final evidence. A selected dependency client may safely retry calls whose method/effect and commit point are understood. Disable or sharply constrain unknown nested policies.

Worst-case call amplification is the product of total attempts at nested layers. Observability must expose physical dependency attempts, not only outer task attempts. gRPC, storage clients, database drivers, proxies, and brokers may perform transparent recovery according to their own rules. Version upgrades can change defaults; pin and test policy.

Database transaction retry should wrap the entire aborted transaction from stable inputs. Retrying only the failed statement can retain invalid application assumptions. External calls must not occur inside a transaction retry loop unless they have independent stable identity and outcome recovery, because the database can roll back while the external effect cannot.

Sleeping inside a scarce worker can hold memory, connection pools, leases, or concurrency slots. For long delays, persist `next_attempt_at` and release the worker. The scheduler re-admits work under the same identity and budget. Short in-process dependency backoff can be reasonable when bounded and cancellation-aware.

### Define the idempotency claim

For target state $S$ and logical transition $F_w$, sequential idempotence is $F_w(F_w(S))=F_w(S)$. State what equality includes: published data generation, catalog pointer, effect ledger, downstream event identity, provider operation, audit semantics, and consumer-visible state. Attempt logs may differ because recording attempts is intended.

Idempotence is not commutativity. Two different work units can each be idempotent while their order changes state. It is not exactly-once execution: many attempts may run. It is not payload deduplication: equivalent or conflicting records need defined semantics. It is not guaranteed by HTTP method, `MERGE`, UPSERT, a broker label, or a deterministic function alone.

Construct a scoped identity $(n,k)$ and canonical fingerprint $h$. Namespace $n$ includes tenant/security domain, environment, target asset, operation kind, and source epoch as needed. Key $k$ names the logical partition/effect. Fingerprint $h$ binds exact inputs, parameters, transformation/schema/config policy, and expected output semantics. A matching retry reuses prior state. Same $(n,k)$ with unequal $h$ is a conflict; never return an unrelated cached success or overwrite the binding.

Retention is part of correctness. If a receipt expires while delayed delivery, operator retry, disaster replay, or provider reconciliation remains possible, the old operation can be accepted as new. Either retain minimal identity evidence for the full horizon, bound/expire intent cryptographically and operationally, or migrate keys into a new namespace with explicit rules.

### Couple effect and receipt where possible

For a transactional data target, apply data changes and terminal receipt in one sufficient transaction. A common flow is: atomically claim or observe the key; verify fingerprint; stage deterministic candidates; apply effects under target uniqueness/version rules; record counts, digest, commit/snapshot identity and success receipt; then commit once.

Do not commit `success` before effects or in a separate transaction afterward. The first ordering can suppress missing work; the second can duplicate committed work after a crash. An `in_progress` row is not success. If used as a lease, it needs owner, expiry, fencing generation, and recovery; the terminal effect/receipt coupling still determines correctness.

Concurrent first attempts require target arbitration. `SELECT` then `INSERT` races. Use a unique constraint, conditional put, compare-and-set, serializable conflict, or equivalent atomic primitive. PostgreSQL documents `ON CONFLICT` as an alternative action when a uniqueness/exclusion violation occurs; exact behavior depends on statement, constraint, and isolation, so reproduce target-version semantics rather than treating syntax as a proof.

On timeout after commit begins, query by stable key. Matching terminal receipt returns the recorded outcome. Absence, when the store's read/consistency contract makes absence authoritative, permits retry. A different fingerprint is conflict. Nonterminal or unavailable evidence remains unknown. Never convert `unknown` to `failed` merely to make dashboards simpler.

### Isolate candidates and fence publication

Many outputs cannot be updated atomically as one database transaction. Write each attempt to an immutable candidate namespace containing logical key, fingerprint, attempt ID, fencing token, files, checksums, schema, counts, quality results, and lineage. Candidate existence is not publication.

After validation, publish by one conditional metadata transition: create the generation pointer if absent, or compare expected predecessor/fencing generation and swap. The accepted record binds exactly one candidate and receipt. A retry that sees the same accepted fingerprint returns it. A competing candidate loses and is cleaned later. A changed-input correction uses new generation semantics rather than stealing the old retry key.

Fencing protects against zombies. A lease alone says who is believed current; an old holder can continue after pause, clock skew, or network partition. A monotonically increasing fencing token checked by the publication authority rejects stale attempts. If the sink cannot check a token or conditional version, do not grant overlapping writers access to the shared final destination.

Never let attempts write directly to `.../partition/current/*` and then mark success. Partial listings and last-writer behavior cannot prove a coherent generation. Immutable objects plus a manifest/pointer make readers observe either the prior accepted generation or the complete new one, subject to the storage/catalog consistency contract.

### Handle checkpoints and partial progress

A checkpoint is reusable only when it binds logical work identity, fingerprint, code/schema/config versions, input positions, output candidate, completed subunits, and integrity evidence. A new attempt validates compatibility before resuming. Worker-local files or mutable offsets without lineage are hints, not authoritative checkpoints.

Checkpoint granularity trades repeated work against state complexity. Row-level checkpointing can overwhelm metadata and violate cross-row invariants. Whole-partition restart is simple but expensive. Choose stages or independently committable shards whose outputs are immutable and whose aggregation/publication remains deterministic.

Resuming is not automatically idempotent. If an attempt wrote 700 of 1,000 external objects but checkpointed 600, restart may encounter 100 existing objects. Stable per-object effect keys or immutable content addresses must make those observations safe. If object names are random per attempt, cleanup and duplicate suppression become ambiguous.

Treat checkpoint corruption, partial write, incompatible version, missing input, and stale lease as explicit states. Fall back to clean candidate recomputation when safe. Never splice outputs from incompatible attempts simply because doing so saves compute.

### Cross transaction boundaries deliberately

A data workflow often touches warehouse, object store, catalog, broker, and external API. A local transaction cannot make all of them atomic. Decompose the workflow into recoverable state transitions with stable identities and evidence.

For database state plus downstream message, use a transactional outbox when both can share the database commit. A publisher may emit more than once; stable event identity and an idempotent consumer contain redelivery. If broker transaction semantics coordinate a broker read/process/write path, keep the claim within that supported boundary. Kafka explicitly scopes exactly-once processing to its transaction and cooperating read-process-write design; an arbitrary external database or email effect needs its own protocol.

For an external provider, persist effect intent and provider idempotency key before the call. On unknown response, query provider outcome. If confirmed, record it; if absent under authoritative semantics, retry the same provider key; if unresolved, retain unknown and reconcile/manual review. Stripe documents saving the first result for an idempotency key and rejecting mismatched parameters, but its retention and endpoint semantics are provider-specific—your receipt horizon and business controls must match them.

Compensation is a new authorized effect, not proof the first never happened. A reversed payment, deletion tombstone, or retraction event remains part of history. Design effect and compensation identities separately and avoid automated compensation while the original outcome is unknown unless the business protocol can tolerate both orders.

### Coordinate retries with orchestration state

Model attempt states separately from logical run state. Useful attempt states include admitted, running, heartbeat-lost, cancellation-requested, timed-out, failed-retryable, failed-terminal, outcome-unknown, succeeded-candidate, publication-lost, and superseded. Logical work can remain reconciling while no worker runs.

Airflow documents retries and task timeouts as task behavior; Kubernetes Jobs document pod retries/backoff and an overall active deadline. These mechanisms are execution controls, not a complete data-effect protocol. Map controller states to your receipt, candidate, publication, and acceptance evidence. Controller `Succeeded` without output validation is insufficient; controller `Failed` after an acknowledgement loss may coexist with a committed effect.

When retry is due later, persist the scheduled instant, failure class, policy version, attempt count, first-attempt time, and remaining logical deadline. Controller restart must not reset counters or backoff. Pause freezes admission according to policy but does not erase outstanding uncertainty. Cancel signals active attempts and blocks future admission while reconciliation determines effects.

Manual retry requires authorization, reason, actor, exact scope preview, current receipt/candidate state, cost estimate, and whether it reuses the same logical fingerprint or creates correction intent. An operator button must not bypass tenant, deadline, idempotency, or publication constraints.

### Preserve dependency and graph semantics

A retried task must use the same upstream generations recorded in its run manifest. Looking up `latest` again can silently change meaning and turn a retry into recomputation. If an input was retracted or access revoked, fail/reconcile according to policy rather than substituting another generation under the same fingerprint.

Downstream readiness follows accepted upstream materialization, not an intermediate attempt state. Do not trigger children from candidate creation, temporary object existence, or worker exit. An accepted publication event uses stable generation identity; duplicate event delivery must not create duplicate downstream effect.

If task B consumed candidate A before A was fenced and A later lost publication, the graph has exposed invalid lineage. Either publish each dependency boundary before consumption or place the entire fused computation inside one declared candidate/commit boundary. Performance fusion must not erase acceptance semantics.

Retry policy can differ by node, but end-to-end deadline and critical path matter. A low-value optional enrichment should not consume all remaining time and prevent essential publication. Reserve budget by phase and propagate cancellation. Replanning a graph after a permanent failure creates a new authorized plan/version, not an invisible retry.

### Observe useful work and amplification

Measure logical work units separately from attempts. Core metrics include initial attempts, retries by index/class/phase, retry success, terminal failure, outcome unknown, reconciliation duration/outcome, deadline/attempt/budget suppression, backoff time, queue age, active zombie/superseded attempts, candidates created/accepted/rejected/orphaned, receipt hits/conflicts, duplicate effects prevented, and publication conflicts.

Calculate attempt amplification

$$
A=\frac{\text{all physical attempts or dependency calls}}{\text{initial logical work units}}
$$

by dependency and workload class. Pair it with goodput: accepted fresh outputs per unit capacity. A high recovery percentage can still be harmful if retries consume most capacity or miss consumer freshness. Record success-after-retry while preserving the initial-failure signal.

Trace one logical work ID across attempts, dependency calls, receipt lookup, candidate manifest, publication, and downstream event. Attempt span IDs remain distinct. Cardinality-heavy partition or tenant identifiers belong in logs/traces or bounded exemplars rather than unbounded metric labels.

Alert on rate and age: sudden transient failures, growing retry queue, unknown outcomes, budget suppression, repeated deterministic signatures, stale active leases, candidates without terminal disposition, receipt conflicts, and accepted output freshness. Do not page merely because a designed first retry occurred.

### Test the recovery protocol

Use deterministic fault injection at every boundary: before/after work claim, input read, checkpoint, data mutation, receipt write, commit request, commit acknowledgement, candidate completion, validation, pointer swap, downstream event, and cleanup. Kill workers and controllers; drop responses; delay cancellation; deliver duplicates; overlap attempts; reorder events; and restart state stores.

Assert authoritative outcomes, not only task status. For the same work key/fingerprint, repeated and concurrent attempts yield one accepted generation/effect; mismatched fingerprint conflicts; a timeout-after-commit is recovered from receipt; an absent receipt permits one safe replay; a stale fencing token cannot publish; downstream logical event/effect occurs once under its protocol; and all attempts remain auditable.

Test temporal boundaries using a fake clock: no attempt starts after expiry; delay plus useful reserve fits; retry counters survive restart; jitter lies in its specified distribution/range; cancellation interrupts waiting; pushback is clamped; and receipt retention exceeds allowed retry age. Test storm behavior at fleet scale or in a model: budget and concurrency hold even when thousands fail together.

Test target-specific concurrency and isolation with the actual engine/version. Verify unique constraints, conditional writes, transaction retries, object visibility, metadata compare-and-set, provider idempotency expiry, and broker transactions. A unit test of the loop cannot prove those deployed semantics.

### Operate retention, security, and change

Retry records can contain source paths, partition values, tenant identities, error fragments, parameters, and lineage. Apply least privilege, encryption, field minimization, access audit, and retention. Do not copy raw rejected rows or secrets into general logs. Separate permission to observe, retry, cancel, override, publish, compensate, and delete.

Long retries cross credential rotation. Prefer workload identity and scoped short-lived credentials refreshed under continuing authority. Bind tenant and target scope independently of caller-provided parameters. Reauthorization policy must distinguish an accepted durable job from a new privileged effect; revocation and legal holds may require stopping even if technical retry remains possible.

Version retry policy. Changing failure classifications, timeouts, attempt caps, fingerprint canonicalization, receipt schema, or publication protocol mid-run can alter outcomes. Existing work either retains its admitted policy or migrates under an explicit, audited rule. Never reinterpret an old key with a new fingerprint algorithm silently.

Before decommissioning, stop new intent, drain/cancel active attempts, reconcile unknown outcomes, disposition retry queues and candidates, ensure consumers see final accepted state, retain or migrate receipts through the replay horizon, revoke credentials, and verify cleanup. Deleting controller state while effects remain possible destroys exactly the evidence safe recovery needs.

## Definitions and Notation

Let $W$ be logical work units. A unit

$$
w=(n,k,h,v,I,O,D,p)
$$

contains identity namespace $n$, stable key $k$, canonical intent digest $h$, contract/artifact version $v$, exact input manifest $I$, expected output contract $O$, absolute deadline $D$, and admitted retry policy $p$. The identity tuple is $id(w)=(n,k)$; equivalence requires the same $h,v,I,O$ under the declared canonicalization.

Let $A_w=(a_0,a_1,\ldots)$ be physical attempts. Each

$$
a_i=(id_i,i,t_i^{adm},t_i^{start},t_i^{end},worker_i,fence_i,candidate_i,result_i)
$$

has distinct physical identity and telemetry. Retrying preserves $w$ and changes $a_i$. A correction $w'$ differs in governed meaning and is linked by supersession rather than smuggled in as $a_{i+1}$.

Let failure classifier

$$
C(result_i,phase,state)\in\{retry,reconcile,stop,replan,quarantine\}.
$$

Retry admission at time $t$ requires all of:

$$
C=retry,\quad i+1<M,\quad t+J_i+U_i+R_i\le D,\quad tokens(scope)>0,
$$

where $M$ is total-attempt limit, $J_i$ backoff/jitter, $U_i$ minimum useful next-attempt budget, and $R_i$ reserved outcome/cleanup time. Concurrency and authorization predicates are also required even when omitted from the compact formula.

Let $Receipt(n,k)$ be absent, in-progress with lease/fence, terminal success bound to fingerprint/outcome, terminal rejection, or conflict. `Unknown` is an observer/workflow state, not necessarily a stored target state. Authoritative lookup function $Q(w)$ maps available receipts/target/provider evidence to `succeeded`, `absent`, `conflict`, or `unresolved` under a declared consistency contract.

Let attempt $i$ produce immutable candidate $G_i$ with manifest $m_i$. Publication is a conditional transition

$$
P(asset,partition,expected,fence_i,G_i)\rightarrow accepted\;generation\;g
$$

or a rejection. Acceptance—not candidate completion—defines the visible generation. A fencing token is a monotonic authority generation checked by the publication boundary; it is stronger than a lease timestamp alone.

For observable projection $\pi$ over declared business/data effects, work is idempotent when

$$
\pi(F_w^m(S))=\pi(F_w(S))\quad\text{for every integer }m\ge1.
$$

This bounded statement may exclude per-attempt logs only when explicitly declared. It does not imply $F_uF_v=F_vF_u$ for distinct work, nor that only one physical attempt executes.

Important clock variables are logical eligibility, admission, attempt start/end, timeout observation, next-attempt time, deadline/expiry, receipt commit, candidate seal, publication, and consumer observation. Store their semantics and uncertainty; do not order remote effects by unsynchronized wall clocks when source versions, transaction IDs, or fencing tokens exist.

## Mechanisms, Invariants, or Proof Structure

The assurance argument has seven layers.

**1. Meaning is immutable.** The run request creates $w$ with stable scope, inputs, versions, output, fingerprint, deadline, and policy. Each attempt references it. If an attempt rereads mutable `latest`, changes parameter defaults, refreshes nondeterministic time, or writes a different output contract, the equivalence premise fails and retry safety is unproved.

**2. Retry admission is bounded.** A classifier permits retry only for plausible transient failure with safe unchanged identity, or after reconciliation proves the prior effect absent. Total attempts, elapsed age, deadline fit, concurrency, authorization, and fleet tokens are conjunctive gates. Backoff/jitter reduces correlated timing; it is not evidence of effect safety.

**3. Concurrent attempts cannot both own the same target transition.** A uniqueness constraint, transactional key claim, conditional update, or publication compare-and-set arbitrates. Proof sketch: if every accepted transition for $(n,k)$ must create/update one uniquely constrained binding to $h$, at most one incompatible claimant commits. Matching claimants observe/reuse the same result. This depends on actual store isolation and on coupling the protected effect to the binding.

**4. Commit uncertainty is queried.** After timeout, the system does not infer absence. If $Q(w)=succeeded$, it returns the prior result; if `absent` is authoritative, it may retry; if conflict, it stops; if unresolved, it remains reconciling. Thus response loss cannot by itself create a second intended effect. The proof fails when reads are stale or the receipt does not cover the external side effect.

**5. Candidates are not visible effects.** Attempts write immutable $G_i$. Validation computes acceptance evidence. Publication uses current expected version and fencing token. Only accepted $G_i$ becomes consumer-visible. A stale attempt can finish but its old fence cannot swap the pointer. This protects replacement overlap when all consumers resolve through the governed publication boundary.

**6. Every crossed atomic boundary has a protocol.** Local data plus receipt share a transaction; data plus message uses outbox and idempotent consumer; provider effects use stable keys and outcome lookup; uncompensatable ambiguous effects retain `unknown`. No component label is promoted into a global exactly-once claim.

**7. Reconciliation closes gaps.** Compare intended logical work, attempt terminal states, target receipts, candidate manifests, accepted publications, downstream events, and consumer freshness. Find intent without effect, effect without intent, unknown without lookup progress, accepted generation without valid controls, orphan candidate, duplicate external effect, and stale active attempt. Repair is authorized and identity-preserving.

An operational invariant set follows:

- one canonical fingerprint is permanently bound to a live idempotency key namespace;
- every admitted attempt references an extant logical work record and its policy version;
- no attempt after deadline can newly publish unless a separately authorized policy says the output remains useful;
- every retryable failure has a bounded next action; every permanent failure has owner/disposition;
- logical success has one accepted output/effect identity and its evidence;
- attempt success without accepted publication cannot satisfy downstream readiness;
- losing/stale attempts cannot mutate accepted state;
- reconciliation never assumes non-existence from a weak/stale read;
- receipts and keys outlive all possible duplicate arrival/retry paths;
- manual actions produce the same audit, identity, authorization, and publication evidence as automation.

### Executable bounded-retry model

The following finite model is design-review evidence. It demonstrates four fixed work units, deterministic demonstration delays, receipt-first recovery after ambiguous commit, deadline admission, stable effect keys, and single publication. It does not model real clocks, random jitter distribution, concurrency, database isolation, cancellation, storage consistency, external providers, authentication, or production capacity.

<!-- bijux-verify: {"id":"bounded-retry-receipt-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"logical_units=4\nattempt_calls=6\nrecovered_units=2\nfailed_units=2\npublished_effects=2\nduplicate_effects=0\nunknown_reconciled=1\ndeadline_suppressed=1\nretry_waits_ms=(100, 100)\nstable_effect_keys=True\n","stderr":""}} -->
```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Work:
    key: str
    fingerprint: str
    outcomes: tuple[str, ...]


WORK = (
    Work("sales/2026-09-01", "h1", ("transient", "success")),
    Work("sales/2026-09-02", "h2", ("commit_then_timeout",)),
    Work("sales/2026-09-03", "h3", ("invalid_data",)),
    Work("sales/2026-09-04", "h4", ("transient", "transient")),
)

DEADLINE_MS = 400
ATTEMPT_MS = 80
RECONCILE_RESERVE_MS = 20
MAX_ATTEMPTS = 3
receipts: dict[str, tuple[str, str]] = {}
effect_keys: list[str] = []
retry_waits: list[int] = []
attempt_calls = 0
unknown_reconciled = 0
deadline_suppressed = 0
recovered = 0
failed = 0

for work in WORK:
    elapsed = 0
    complete = False
    for attempt, outcome in enumerate(work.outcomes, start=1):
        prior = receipts.get(work.key)
        if prior is not None:
            assert prior == (work.fingerprint, "published")
            complete = True
            break
        attempt_calls += 1
        elapsed += ATTEMPT_MS
        if outcome in {"success", "commit_then_timeout"}:
            receipts[work.key] = (work.fingerprint, "published")
            effect_keys.append(work.key)
            if outcome == "success":
                complete = True
                break
            observed = receipts.get(work.key)
            assert observed == (work.fingerprint, "published")
            unknown_reconciled += 1
            complete = True
            break
        if outcome == "invalid_data":
            break
        assert outcome == "transient"
        delay = min(200, 100 * (2 ** (attempt - 1)))
        if (
            attempt >= MAX_ATTEMPTS
            or elapsed + delay + ATTEMPT_MS + RECONCILE_RESERVE_MS
            > DEADLINE_MS
        ):
            deadline_suppressed += 1
            break
        retry_waits.append(delay)
        elapsed += delay
    if complete:
        recovered += 1
    else:
        failed += 1

print(f"logical_units={len(WORK)}")
print(f"attempt_calls={attempt_calls}")
print(f"recovered_units={recovered}")
print(f"failed_units={failed}")
print(f"published_effects={len(receipts)}")
print(f"duplicate_effects={len(effect_keys) - len(set(effect_keys))}")
print(f"unknown_reconciled={unknown_reconciled}")
print(f"deadline_suppressed={deadline_suppressed}")
print(f"retry_waits_ms={tuple(retry_waits)}")
print(f"stable_effect_keys={set(effect_keys) == set(receipts)}")
```

The second unit records its receipt/effect before the simulated acknowledgement loss. Receipt lookup resolves it without a second call. The fourth unit spends 80 ms, waits 100 ms, spends another 80 ms, then rejects the next 200 ms delay because $260+200+80+20>400$. It does not exhaust CPU in a doomed attempt. In production, ambiguous lookup can itself fail; the correct state would remain unresolved rather than taking the model's always-readable receipt for granted.

## Alternatives and Trade-Offs

**No automatic retry versus bounded retry.** No retry minimizes amplification and accidental duplication but turns transient faults into manual work. Bounded semantic retry improves recovery when identity and outcome evidence are strong. Keep permanent and ambiguous failures out of blind retry.

**Fixed versus exponential backoff.** Fixed delay is easy and can fit known periodic recovery, but correlated clients remain synchronized. Exponential delay reduces frequency during sustained failure. Both require jitter, cap, attempt/age limits, and capacity budget.

**Full jitter versus equal/decorrelated jitter.** Full jitter offers broad spreading and can select near-zero delays. Equal jitter enforces part of the exponential delay. Decorrelated algorithms react to prior delay. Choose from dependency recovery and fleet behavior; document and simulate the exact formula.

**Worker sleep versus persisted delayed admission.** Sleeping is simple for millisecond-scale dependency retry but occupies resources and loses state on restart. Persisted scheduling releases capacity and survives restart, at the cost of durable state and clock semantics.

**Whole-partition retry versus resumable shards.** Whole retry has a small state model and strong coherence but repeats expensive work. Sharded checkpoints reduce recomputation while multiplying identity, partial-state, and aggregation concerns. Choose only independently verifiable units.

**Natural versus constructed idempotence.** Setting a row to an exact versioned value can be naturally repeatable. Adds, appends, provider calls, and publications need uniqueness, effect ledgers, keys, or conditional transitions. Even natural core state may need constructed handling for events and audit.

**Transactional receipt versus immutable candidate publication.** A single database transaction gives a strong local proof. Large files/multi-system output often require candidates plus a metadata commit. Use both where a warehouse transaction records the accepted immutable manifest.

**Pessimistic lock versus optimistic CAS/fencing.** Locks can serialize ownership but may block, expire, or be lost during partitions. CAS and fences allow concurrent computation while admitting one result, at the cost of discarded work. A lease without sink validation is insufficient.

**Exactly-once-labeled transport versus application idempotency.** Broker transactions can reduce duplicates within a documented boundary. Application keys and receipts cover business/data effects across stores. Use transport features, but keep the claim scoped.

**Retry full batch versus failed items.** Full-batch retry is safe only if every item/effect is idempotent under stable identity or the batch is atomic. Per-item retry saves work but needs authoritative item outcomes and may change ordering/aggregate semantics.

**Compensation versus reconciliation.** Compensation can restore a business invariant after confirmed effect but creates a new effect and history. Reconciliation is safer while outcome is unknown. Some irreversible effects require human adjudication rather than automatic reversal.

**Long versus short receipt retention.** Long retention protects delayed duplicates and audits but costs storage and may preserve sensitive metadata. Minimize stored fields, partition/tier evidence, and align retention with replay/legality. Short retention requires demonstrably shorter intent and delivery horizons.

**Fail closed versus accept best-effort output.** Strict publication protects correctness but can miss freshness objectives. A degraded result can be allowed only as a distinct generation with explicit completeness/quality metadata, consumer contract, and later correction—not by weakening retry rules invisibly.

## Failure Modes and Misconceptions

- **“Three retries means three attempts.”** Many systems count retries after the initial attempt; report total attempts explicitly.
- **“Timeout means it failed.”** Timeout means one observer stopped waiting; effect may have committed.
- **“Cancellation killed it.”** Cancellation can be delayed, ignored, or arrive after commit; fence later effects.
- **“Retrying the task preserves meaning.”** Mutable `latest`, current time, random defaults, or changed code can make each attempt different.
- **“Every 5xx or exception is transient.”** Phase, error code, dependency state, and effect ambiguity determine action.
- **“Bad data might work next time.”** Deterministic schema and invariant failures require quarantine/correction, not capacity consumption.
- **“Exponential backoff prevents storms.”** Without jitter and fleet budget, retries still synchronize or exceed spare capacity.
- **“Jitter lowers total load.”** It changes timing; budgets, shedding, and attempt caps change amount.
- **“Per-task limits protect the warehouse.”** Millions of bounded tasks can still overload one dependency.
- **“The orchestrator is the only retry layer.”** SDKs, proxies, drivers, brokers, and transaction wrappers may retry invisibly.
- **“A random attempt ID is an idempotency key.”** A new ID per attempt guarantees deduplication cannot recognize the same intent.
- **“Same key is enough.”** The key must be scoped and bound to an immutable fingerprint; mismatches are conflicts.
- **“UPSERT means idempotent.”** Additive clauses, nondeterministic source matches, events, and external effects can still repeat.
- **“Check then insert prevents duplicates.”** Concurrent checkers race unless the target arbitrates atomically.
- **“Success marker plus data is eventually fine.”** A crash between separate commits creates missing or duplicate effects.
- **“Exactly-once broker means exactly-once workflow.”** Claims do not automatically cross external stores/providers or non-cooperating consumers.
- **“Lease ownership stops old workers.”** A zombie can act after lease loss unless the effect boundary checks a fence.
- **“Attempt output can go straight to final.”** Overlap and partial failure can expose mixed generations.
- **“Checkpoint exists, so resume is safe.”** Compatibility, completeness, integrity, and effect identities must be verified.
- **“Exit zero means data is good.”** Acceptance needs manifest, schema, counts, controls, lineage, and publication evidence.
- **“A successful retry erases the incident.”** Record initial failures, amplification, latency, cost, and suppressed work.
- **“Delete receipts after success.”** Delayed duplicates and disaster replay can then recreate effects.
- **“Manual retry is harmless.”** It can bypass policy, race automation, change inputs, and repeat irreversible effects.
- **“Compensation proves rollback.”** Compensation is another effect and may itself fail or be observed out of order.
- **“Unknown is just failed.”** Collapsing uncertainty encourages blind retry or duplicate operator action.

## Worked Examples

### Example 1

A daily partition attempt loses its database commit response. The orchestrator records `outcome_unknown`, queries the receipt keyed by asset, partition, and input fingerprint, finds terminal success, and marks the logical unit accepted without rerunning SQL. The timeout did not prove failure; the receipt resolves it.

### Example 2

A transformation fails because a required column is absent from an input generation. Five workers would reproduce the same failure. The classifier quarantines the input and stops automatic retry. A corrected source generation creates new logical work rather than changing the fingerprint under the old key.

### Example 3

An orchestrator permits four total attempts, its HTTP client permits three, and a storage SDK permits two. One task can issue 24 deepest calls. The team makes the orchestrator own logical retry, keeps only proven safe SDK transport recovery, and exposes all physical calls in amplification metrics.

### Example 4

Two workers start the same new partition after a heartbeat timeout. Both create immutable candidates. Worker B has fencing token 18 and publishes first; worker A's token 17 is rejected by the conditional pointer update even though A finishes later. Candidate cleanup does not affect the accepted generation.

### Example 5

A thousand partitions encounter warehouse overload. Per-task three-attempt limits could produce two thousand retries. A dependency-scoped retry token pool, concurrency reduction, server pushback, and jitter admit only recovery probes while leaving capacity for interactive and already-near-complete work.

### Example 6

A batch writes 700 of 1,000 provider objects before worker death. Each object name is derived from logical work plus shard and content digest. Resume verifies the checkpoint at 600, observes matching receipts for objects 601–700, and continues at 701 without duplicating provider effects.

### Example 7

A task updates a warehouse row and sends an event directly, then its transaction aborts. Consumers see an event for absent state. The corrected design writes state and an outbox record in one transaction; a publisher can retry emission under stable event ID, and consumers apply their own inbox/effect protocol.

### Example 8

A provider request times out after possible acceptance. The workflow keeps the same provider idempotency key and queries outcome. The provider is unavailable, so the state remains `unknown` and an operator is prevented from issuing a new key. Availability is lower temporarily, but duplicate irreversible action is avoided.

### Example 9

A logical deadline has 500 ms remaining. Proposed jitter is 250 ms, minimum useful query time 220 ms, and reconciliation reserve 80 ms. Because $250+220+80=550>500$, the retry is suppressed even though its error class is transient. Starting it would consume load without a credible completion path.

### Example 10

Receipt retention is seven days, but a disconnected edge producer can redeliver for thirty. On day twenty it repeats an old effect key whose receipt has vanished, creating a duplicate. The system extends minimal receipt retention beyond the delivery horizon and expires producer authority for requests outside that horizon.

## Cross-Program Connections

[API-008](../../28-api-and-service-engineering/modules/008-idempotency-and-safety.md) defines bounded intended-effect idempotence. [API-037](../../28-api-and-service-engineering/modules/037-idempotency-keys.md) develops key/fingerprint/outcome contracts. [API-067](../../28-api-and-service-engineering/modules/067-idempotent-consumers.md), [API-071](../../28-api-and-service-engineering/modules/071-timeout-and-deadline-budgets.md), and [API-072](../../28-api-and-service-engineering/modules/072-retries-and-backoff.md) supply message, deadline, retry-load, and dependency-call foundations. Data workflows reuse those mechanisms but add immutable input generations, large candidates, quality acceptance, and partition publication.

[PLAT-043](../../29-platform-engineering/modules/043-batch-and-scheduled-workload-templates.md) exposes workload retries, deadlines, candidates, and operational evidence in a platform golden path. [PLAT-055](../../29-platform-engineering/modules/055-idempotent-reconciliation.md) explains repeatable desired-state control. Platform mechanisms should expose fencing, policy, and telemetry without pretending to know a domain partition's correctness.

[SEP-055](../../11-software-engineering-patterns/modules/055-unit-of-work.md) and [SEP-081](../../11-software-engineering-patterns/modules/081-retry-with-bounded-backoff.md) provide unit-of-work and resilience patterns. Their application here requires data-generation identity, receipt retention, and publication semantics.

Within this program, [DE-027](027-idempotent-loads.md) covers target-side data-load identity in depth; [DE-036](036-merge-and-upsert-semantics.md) and [DE-038](038-late-corrections-and-restatement.md) protect row/version correctness. [DE-043](043-scheduling-and-event-triggered-execution.md) creates deterministic run requests; DE-045 and DE-046 next develop partitioned assets and backfill planning. DE-047 through DE-050 will add orchestration deployment, sensors/deferrable work, operational state, and a complete production workflow.

## References

1. RFC Editor, [RFC 9110: HTTP Semantics, Section 9.2.2 Idempotent Methods](https://www.rfc-editor.org/rfc/rfc9110.html#name-idempotent-methods). Defines idempotent request-method intent and why clients must know whether a non-idempotent request can be repeated. Accessed 2026-09-03.
2. Amazon Web Services, [AWS SDK Retry Behavior](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html). Documents standard/adaptive retry modes, retry-token and request-rate token buckets, maximum attempts, and truncated exponential backoff with jitter. Accessed 2026-09-03.
3. Amazon Web Services, [Ensuring Idempotency in Amazon EC2 API Requests](https://docs.aws.amazon.com/ec2/latest/devguide/ec2-api-idempotency.html). Documents client-token idempotency, parameter matching, mismatch errors, and regional/zonal scope for supported EC2 operations. Accessed 2026-09-03.
4. Kubernetes, [Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/). Documents Job retry/backoff controls, pod failure policy, active deadlines, completion behavior, and controller recreation realities. Accessed 2026-09-03.
5. Apache Airflow, [Tasks](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html). Documents task instances, retries, execution timeouts, sensor timeouts, and task states in Airflow's execution model. Accessed 2026-09-03.
6. gRPC Authors, [Retry](https://grpc.io/docs/guides/retry/). Documents transparent/configured retries, commitment, retry policy, backoff, throttling, and server pushback within gRPC. Accessed 2026-09-03.
7. Temporal Technologies, [Retry Policies](https://docs.temporal.io/encyclopedia/retry-policies). Documents retry intervals, backoff coefficients, maximum intervals/attempts, non-retryable errors, and workflow/activity policy distinctions. Accessed 2026-09-03.
8. Stripe, [Idempotent Requests](https://docs.stripe.com/api/idempotent_requests). Documents provider-specific idempotency keys, saved outcomes, parameter comparison, and key lifecycle behavior. Accessed 2026-09-03.
9. PostgreSQL Global Development Group, [INSERT](https://www.postgresql.org/docs/current/sql-insert.html). Documents `ON CONFLICT`, unique/exclusion arbitration, and statement behavior relevant to target-side idempotency mechanisms. Accessed 2026-09-03.
10. Apache Kafka, [Design: Message Delivery Semantics](https://kafka.apache.org/40/design/design/#message-delivery-semantics). Scopes at-most-once, at-least-once, and transactional exactly-once behavior, including cooperation required for read-process-write guarantees. Accessed 2026-09-03.

## Exercises

### Exercise 1

A task has a 12-minute logical deadline. Setup takes at least 45 seconds, useful processing at least 150 seconds, and outcome reconciliation reserves 30 seconds. The first attempt fails transiently after 240 seconds. Proposed retry delays are 30, 60, and 120 seconds. Decide which later attempts can be admitted if each consumes its minimum setup and processing time. State assumptions and show the deadline calculation.

### Exercise 2

A partition writer commits data, then writes its success receipt in a second transaction. A crash occurs between them and the orchestrator retries. Explain the ambiguity and design both a transactional-target protocol and an object-store candidate/publication protocol that close the gap.

### Exercise 3

An orchestrator permits four total attempts, an RPC library permits three total attempts, and a database wrapper permits two transaction attempts. Compute worst-case deepest calls per logical work unit and for 2,500 simultaneously failing units. Redesign retry ownership and load budgets.

### Exercise 4

Two concurrent attempts have fencing tokens 41 and 42. Attempt 42 publishes candidate B, then attempt 41 finishes candidate A with a nominally later wall-clock timestamp. Specify the publication condition, final accepted state, attempt dispositions, and evidence retained. Explain why lease time and finish time are insufficient.

### Exercise 5

A workflow writes a warehouse transaction, calls an email provider, and publishes a broker event. Design stable identities, atomic boundaries, receipts/outbox/inbox handling, unknown-outcome recovery, retry classification, and reconciliation. State the strongest honest idempotency claim.

## Answers to the Exercises

### Answer 1

After the first failure, $720-240=480$ seconds remain. One later attempt needs delay plus 45 seconds setup, 150 seconds useful work, and 30 seconds reconciliation. Retry 1 needs $30+45+150+30=255$ seconds and fits, leaving 225 seconds if it consumes the minimum. If it fails only after the full 195 seconds of setup/work, retry 2 would need $60+45+150+30=285$ seconds and cannot fit in 225, so it is suppressed; retry 3 is unreachable. This assumes the deadline starts with the first attempt, failure consumed exactly 240 seconds, delay is sequential, and reconciliation reserve is not already spent. Actual elapsed time, cancellation, queue delay, and measured minimum usefulness must be recomputed before admission.

### Answer 2

Data without receipt makes target success indistinguishable from “not processed” to a receipt-only controller; replay can duplicate additive effects. In a transactional target, atomically claim/validate `(namespace,key,fingerprint)`, apply deterministic effects under target constraints, and write terminal receipt with commit/result identity in the same transaction. On timeout, query that receipt under an authoritative read contract. For object output, each attempt writes an immutable candidate manifest and files; validation precedes one conditional/fenced metadata pointer transition that binds the accepted candidate and receipt. Matching retries return the accepted generation, losing/stale candidates cannot publish, and cleanup is separate.

### Answer 3

Worst-case deepest attempts are $4\times3\times2=24$ per logical unit and $2{,}500\times24=60{,}000$ during a correlated incident. Make the orchestrator own logical-work retry and retain only narrow transparent RPC recovery for provably pre-commit failures or disable it; wrap only a fully aborted deterministic database transaction when required. Enforce one propagated deadline, dependency-scoped concurrency, a retry token/rate budget shared across workers, jittered backoff, overload pushback, and telemetry for every physical call. The exact remaining multiplier must be stated, not hidden.

### Answer 4

Publication requires a compare-and-set from the expected prior generation and acceptance of the current fencing token 42. Candidate B becomes the accepted generation. Token 41 is lower than the publication authority's accepted/current fence and is rejected regardless of its later finish timestamp. Record both attempt manifests, tokens, validation results, the successful conditional transition, A's superseded disposition, and eventual exact candidate cleanup. Lease or wall-clock time describes belief/timing; a partitioned zombie may outlive its lease and clocks may skew. Only a fence checked at the effect boundary prevents stale mutation.

### Answer 5

Use one logical work key/fingerprint for exact inputs and output. Commit warehouse changes, terminal local receipt, and an outbox event identity atomically. A publisher may retry the event under that stable ID; consumers use inbox/effect identity or an atomic local checkpoint/effect transaction. Before email, persist a separate email-effect intent and stable provider idempotency key. On timeout, query provider outcome; matching success is recorded, authoritative absence permits same-key retry, and unresolved state remains unknown for reconciliation/manual review. Permanent data/policy errors stop; transient pre-effect failures use bounded retry; overload honors budgets/pushback. The honest claim is one warehouse effect and one logical event under their transactional/idempotent boundaries, plus at-most-one intended email where the provider durably enforces the retained key and outcome lookup; no universal exactly-once physical execution or cross-system atomic commit is claimed.
