---
module_id: PLAT-043
program: Platform Engineering
level: 1
module_number: 43
title: Batch and Scheduled Workload Templates
status: complete
last_verified: 2026-09-02
---

# Batch and Scheduled Workload Templates

## One-Page Review

### Governing question

How should a platform turn batch and schedule intent into owned, repeatable workload paths that preserve business-period identity, tolerate duplicate execution, meet explicit deadlines, expose partial results, share capacity fairly, and retire every runtime and external effect without implying exactly-once behavior?

### Essential definitions

- A **batch execution template** is a versioned contract for one bounded run-to-completion operation, including identity, input, output, retry, capacity, evidence, and cleanup.
- A **schedule template** is a versioned contract that materializes recurring execution intents from calendar or interval rules; it composes a batch template rather than replacing it.
- An **operation identity** names the business work intended, such as `close-ledger/2026-08`; an **execution identity** names one attempt to perform it.
- A **business period** is the domain interval or partition being processed, independent of the wall-clock instant when an execution starts.
- An **input binding** is an immutable snapshot or versioned reference from which an execution derives its work.
- A **result manifest** is durable evidence enumerating expected and produced outputs, checksums, partitions, status, errors, and producer revision.
- A **commit point** is the application-defined transition after which an external effect counts as accepted and replay must reconcile rather than repeat blindly.
- A **checkpoint** is durable progress from which compatible code can resume; a log line or surviving local file is not necessarily a checkpoint.
- A **missed run** is a scheduled intent that was not started within its admitted window; it is not the same as a failed execution.
- **concurrency policy** specifies whether schedule materializations may overlap, be withheld while a prior run is active, or replace a prior run.

### Central model, mechanism, or theorem

Let operation $o=(k,I,O,D,P)$ bind idempotency key $k$, immutable input $I$, expected-output contract $O$, deadline $D$, and policy $P$. Execution $e=(r,a,v,t,s)$ binds run identity $r$, attempt $a$, implementation revision $v$, timing $t$, and observed state $s$. A schedule maps a business period $b$ to operation identity $k=f(b)$ and may create zero, one, or multiple executions. Correct acceptance requires an application predicate $C(o,e,M)$ over domain effects and result manifest $M$; controller completion alone is insufficient. Safe replay requires either effects keyed by $k$, a fenced commit, or reconciliation that can distinguish absent, committed, and ambiguous outcomes.

### Critical invariants

- Operation identity, execution identity, attempt, business period, input revision, code digest, and output manifest remain distinct and correlatable.
- Inputs are immutable or version-bound before execution; retries never silently read a different dataset or configuration.
- Duplicate starts are expected. `parallelism: 1`, one completion, one CronJob, and one controller do not prove unique execution or unique effects.
- Retry and backoff apply only to classified failures; ambiguous external commits are observed or reconciled before replay.
- Success means the declared domain result and manifest are complete, not merely that a Pod terminated with exit code zero.
- Deadlines include admission, startup, execution, checkpoint, commit, and validation according to the published contract; each timing state is observable.
- Parallelism is bounded by partition independence, critical path, downstream capacity, quota, placement, and cost—not only available CPUs.
- Cancellation, suspension, replacement, eviction, and deadline termination can leave partial effects; checkpoints and cleanup are explicit.
- Schedule timezone, daylight-saving behavior, missed-start window, overlap policy, catch-up, manual rerun, and backfill semantics are declared.
- Quota admission and priority preserve multi-tenant fairness; admission does not guarantee immediate placement or deadline completion.
- Runtime-object retention is separate from external output, logs, audit, checkpoints, leases, credentials, and privacy retention.
- Template revisions have conformance tests, consumer inventory, migration, deprecation, and retirement; creating new runs is only one lifecycle stage.

### Common failures

Treating CronJob as exactly once; deriving business identity from actual start time; allowing retry to charge twice; reading mutable `latest` input; setting `parallelism: 1` instead of fencing a singleton mutation; scaling beyond database capacity; measuring duration only after a Pod starts; assuming `Forbid` queues every period; using `Replace` without checkpoint-safe termination; allowing daylight-saving time to duplicate or omit a domain period; declaring partial output complete; deleting Job objects while retaining unowned external data; storing credentials in parameters; granting every batch run the same broad identity; and retiring a template while schedules, queues, leases, or outputs remain.

### Compact example

A monthly ledger-close schedule maps `Europe/Stockholm` calendar period August 2026 to operation key `ledger-close/2026-08`; the period does not change if admission delays execution into September. The schedule uses `Forbid`, a starting deadline, and an explicit manual backfill API, but does not assume a missed period is queued. The batch execution binds a sealed ledger snapshot, code digest, resource profile, deadline, fenced ledger commit, and expected shard set. Each shard writes immutable staging output keyed by operation and shard. The coordinator validates counts and checksums, atomically publishes one result manifest, and records commit status. A duplicate execution discovers the committed operation and verifies rather than charges again. Runtime objects expire after operational retention; financial results and audit evidence follow separate policies.

### Connections

This module specializes the batch and schedule archetypes from [PLAT-041](041-workload-archetypes.md) and applies the template lifecycle and supply-chain controls from [PLAT-042](042-service-templates.md). It relies on workload scheduling, autoscaling, storage, configuration, secrets, telemetry, and data access from earlier platform modules; event-triggered workers are developed further in the next workload-template modules.

## Governing Question

What maintained platform contract lets a team submit one bounded operation or recurring business schedule and receive trustworthy identity, admission, execution, result, evidence, recovery, and retirement semantics without mistaking orchestration for business correctness?

Batch work is often described as “run this container.” That description omits the facts that determine safety: which work, against which input, under whose authority, how repetition behaves, what counts as complete, where partial output lives, and who removes it.

Schedules add another layer. A clock rule produces intent; it does not complete business work. Controller outages, daylight-saving transitions, long executions, policy choices, and manual reruns can produce zero, one, or multiple attempts for the same domain period.

The platform path therefore has two related products. The batch template contracts one operation and its attempts. The schedule template maps calendar or interval occurrences to batch operation identities and governs overlap, lateness, catch-up, and pause. Keeping them separate makes on-demand reruns and backfills use the same correctness contract as automatic starts.

## Why This Matters

Batch workloads routinely hold concentrated authority. A migration changes schema, a reconciliation modifies accounts, an export releases sensitive data, and a training run consumes expensive accelerators. A short-lived process can have a longer-lived blast radius than a continuously serving application.

Orchestrators deliberately retry and replace failed processes. Kubernetes documents that a Job may start the same program more than once even with one requested completion and parallelism of one. An application that interprets process start as a unique business operation can duplicate payments, messages, deletions, or irreversible migrations.

Scheduled work combines distributed systems with calendars. The phrase “daily at 02:30” is incomplete without timezone, daylight-saving handling, business-period mapping, late-start tolerance, overlap policy, and manual repair. Operational start time is a poor business key: the August close may begin in September, and a rerun must still mean August.

Capacity is also a product concern. A hundred parallel shards can reduce compute time while overwhelming a database, saturating a network link, exhausting an API quota, or starving request services. A useful template exposes safe resource profiles, admission state, quota, deadline risk, and cost rather than merely a `parallelism` knob.

Finally, termination is not cleanup. A Job object may disappear while object-store fragments, checkpoint volumes, leases, credentials, exported personal data, and audit obligations remain. Lifecycle ownership must follow every effect beyond the controller namespace.

## Prerequisites and Retrieval

Retrieve processes and exit status, signals and graceful termination, immutable data, content addressing, transactions, compare-and-swap, leases and fencing, idempotency, deduplication, retries and exponential backoff, partial failure, reconciliation, checkpoints, partitioning, critical paths, queueing, deadlines, resource requests and limits, placement and topology, quotas and priority, schedules and timezones, daylight-saving transitions, observability, data retention, privacy deletion, supply-chain provenance, Kubernetes Pods and Jobs, and platform product lifecycle.

You should distinguish operation from execution; attempt from retry policy; requested parallelism from useful concurrency; controller success from domain acceptance; process checkpoint from business commit; input reference from immutable binding; schedule occurrence from business period; missed run from failed run; suspension from safe cancellation; runtime retention from data retention; admission from placement; placement from start; start from completion; event-triggered Job from long-running queue consumer; and current conformance from template ancestry.

## Learning Objectives

After completing this module, you should be able to:

1. specify separate batch-execution and recurring-schedule contracts;
2. model operation, execution, attempt, period, input, output, checkpoint, and commit identities;
3. design idempotency, fencing, reconciliation, retry, cancellation, and ambiguous-outcome handling;
4. select fixed, work-queue, or indexed completion semantics and validate partition results;
5. reason about deadlines, parallelism, bottlenecks, quota admission, placement, and cost;
6. define timezone, missed-start, overlap, catch-up, pause, rerun, and backfill behavior;
7. bind least-privilege identity, configuration, secrets, telemetry, result manifests, and retention;
8. test normal, duplicate, partial, late, cancelled, capacity-constrained, and recovery paths; and
9. version, migrate, deprecate, and retire templates, schedules, executions, and external effects.

## Core Exposition

### Start with the business operation

Name the domain work before selecting a controller. Examples include “reconcile inventory snapshot 481,” “close ledger period 2026-08,” “transcode asset digest X,” and “apply schema migration 173.” The name should survive retries, delayed starts, controller replacement, and runtime migration.

Specify requester, accountable owner, input binding, expected outputs/effects, validity window, deadline, authorization, data class, downstream limits, recovery, retention, and terminal acceptance. State whether work is safely repeatable, conditionally repeatable, fenced singleton, or non-repeatable after an ambiguous effect.

An operation key identifies intended business work. An execution ID identifies an orchestration attempt. Attempt numbers identify retry history within or across executions. Combining them into one opaque Job name makes reconciliation and audit difficult.

State non-guarantees: creation does not promise placement, a started Pod does not promise progress, exit zero does not promise correct output, Job completion does not promise a unique effect, and controller retention does not retain or erase external data.

### Define the batch template contract

A batch template declares stable identifier and revision; supported operation types and user cohorts; input and output schemas; identity and policy; code/image digest; resource and placement profiles; completion mode; parallelism bounds; retry/backoff and failure classification; deadline; checkpoint and cancellation; result validation; telemetry; retention; support; cost attribution; compatibility; and retirement.

Expose intent, not provider internals. Users may choose “deadline-sensitive CPU backfill” or “single GPU training” from tested profiles. Raw scheduler annotations, arbitrary commands, unrestricted images, host paths, or unbounded resource values bypass the supported contract.

Validate cross-field combinations. An indexed job needs a finite index domain. Replacement requires termination and checkpoint semantics. Retry requires idempotency or a reconciliation gate. Sensitive export requires an authorized destination and retention. A deadline shorter than measured startup plus minimum useful execution should be rejected.

Pin executable inputs: image by digest, command/arguments under the approved template, configuration revision, dependency references, policy revision, and immutable dataset snapshot. Record them without secret values.

### Bind input before starting

Mutable input destroys replay meaning. If `source=latest/orders`, the first attempt may see one dataset and retry another. Resolve a snapshot ID, transaction boundary, object version, manifest digest, log offsets, or query-as-of timestamp before execution.

For partitioned work, publish an input manifest containing the complete expected partition set, location/version, size or count where useful, checksum, schema revision, and authorization scope. Workers consume assigned entries; they do not rediscover an evolving directory independently.

Validate that the snapshot remains readable for the maximum queue, execution, retry, and investigation window. If input retention is shorter than the operation lifecycle, reproducible recovery is impossible.

Secret references remain references. A broker delivers narrowly scoped, short-lived credentials to the execution identity. Do not place database passwords, export tokens, or private keys in schedule objects, template parameters, Job manifests, environment snapshots, labels, logs, or result manifests.

### Separate control, process, and domain state

Controller state answers whether desired Pods were created and observed. Process state answers whether a program started, checkpointed, exited, or was terminated. Domain state answers whether the intended effect is absent, staged, committed, rejected, or ambiguous.

These states do not advance atomically. A process can commit an external transaction and crash before reporting success. A controller then retries a completed business effect. Conversely, a process can exit zero after writing only nine of ten partitions because its validation was incomplete.

Model status with at least requested, admission-pending, admitted, placement-pending, starting, running, checkpointing, validating, committing, succeeded, failed-retryable, failed-terminal, cancelled-clean, cancelled-partial, deadline-expired, and unknown-effect where applicable. Provider states can be mapped into this contract without pretending they are identical.

Expose timestamps for request, admission, first placement, process start, last progress, commit, validation, and terminal state. This separates queue delay from startup and execution and allows meaningful deadline diagnosis.

### Design for duplicate execution

Assume the same operation may execute more than once due to Pod replacement, lost acknowledgements, controller races, human rerun, schedule catch-up, disaster recovery, or independent Job creation. Idempotency is an application property supported by platform identity, not a checkbox on the controller.

Prefer effects naturally keyed by operation identity: upsert a result under a unique operation key, insert with a unique constraint, write immutable objects then compare-and-swap one manifest pointer, or send downstream requests with enforced idempotency keys.

For singleton mutation, acquire a lease with monotonically increasing fencing token and require the authoritative store to reject writes from older tokens. A lease without fencing can leave a paused old worker writing after a new holder begins.

When an effect returns an ambiguous timeout, query authoritative state by operation key. If observation cannot distinguish committed from absent, stop in an unknown-effect state and require reconciliation. Blind replay turns uncertainty into duplication.

### Choose completion and partition semantics

A singleton job runs one logical worker but still needs duplicate safety. A fixed-completion job requires a number of successful completions, but unindexed successes do not identify which domain partitions were processed. A work-queue job lets workers claim tasks from an external authority; correctness depends on lease, acknowledgement, poison-item, and drain behavior.

An indexed job gives each completion a stable index. Bind each index deterministically to one input-manifest entry or partition range. Index identity helps coordination but does not validate data, prevent duplicate execution of an index, or publish a complete result.

Define per-index retry and terminal behavior. Some partitions may be allowed to fail for approximate analytics; financial reconciliation may require all. A success policy that accepts a subset must be reflected in the domain result contract and not merely tuned to stop remaining Pods sooner.

For distributed computations containing several related Jobs, a higher-level coordinator such as JobSet may express grouping and startup dependencies. It still does not implement application barriers, algorithmic consistency, durable checkpoints, or correct output commit unless those mechanisms are explicitly supplied.

### Bound retries and classify failure

Classify errors as retryable transient, retryable after dependency recovery, non-retryable input, non-retryable policy, poisoned partition, deadline-exhausted, cancelled, and ambiguous-effect. Exit code alone may be too coarse; structured termination/result status can carry bounded classifications without leaking secrets.

Use exponential backoff with jitter where it protects dependencies, but cap attempts and total retry time. Fast retry of authorization failure, corrupt input, deterministic schema mismatch, or invalid command wastes capacity and obscures the real defect.

Kubernetes Job backoff and Pod failure policy can count, ignore, fail the Job, or fail an index for selected failures. Configure them as orchestration mappings of the application contract. They do not decide whether an external transaction is safe to repeat.

Retain enough history to explain repeated failure while respecting data sensitivity. Aggregate high-cardinality attempt telemetry and keep detailed evidence under scoped access.

### Make deadlines end to end

A business deadline should be measured from the agreed origin—often request acceptance or scheduled-period release—not only from Pod start. Decompose total time as

$$
T_{total}=T_{admission}+T_{placement}+T_{startup}+T_{work}+T_{checkpoint}+T_{commit}+T_{validate}.
$$

Publishing each component shows whether more compute can help. If quota admission consumes three hours of a four-hour window, optimizing worker code by ten percent is not a solution.

For divisible work amount $W$, effective per-worker service rate $\mu$, $n$ workers, and fixed startup/coordination overhead $s$, an optimistic lower estimate is

$$
T_{work}\gtrsim s+\frac{W}{n\mu}.
$$

The estimate assumes balanced independent partitions and no shared bottleneck. Actual time is bounded by the critical path, largest shard, downstream throughput, quota, placement, retries, stragglers, and commit/validation.

Active-runtime deadlines may terminate Pods. Decide whether queue/admission time consumes that provider deadline and maintain a separate business deadline if semantics differ. Alert before the point at which no feasible capacity can finish, not only after termination.

### Govern parallelism, admission, and placement

Maximum useful concurrency is the minimum of independent work, quota, schedulable resources, downstream capacity, partition limit, license/API rate, cost budget, and any ordered critical path. More Pods can increase contention and tail time.

Offer measured resource classes and controlled parallelism ranges. Record CPU, memory, ephemeral storage, accelerator, network, and topology requirements. Requests that are too low cause eviction or throttling; requests that are too high cause fragmentation and queueing.

Batch should enter a workload admission system when scarce shared capacity needs quota, borrowing, cohorts, priority, or preemption. Kueue models a workload for admission and ClusterQueues for shared quota policy. Local submission alone is not capacity acceptance.

Distinguish admitted from placed and running. Even an admitted workload may wait for nodes, images, volumes, devices, topology, or preemption completion. Priority should represent business policy rather than whoever asks for the largest value.

Preemption can waste work and create partial effects. Checkpoint-capable workloads may be cheaper to preempt, but checkpoint write time and compatibility belong in the deadline and recovery design. Protect interactive capacity and define batch cost attribution.

### Treat checkpoints as versioned durable state

A checkpoint records sufficient progress and state to resume without corrupting or repeating accepted work. It has operation identity, partition scope, sequence or offset, producer code/schema revision, input revision, checksum, creation time, and retention.

Write checkpoints atomically or through immutable data plus a committed pointer. A half-written checkpoint that appears latest can be worse than none. Validate compatibility on resume; a new image must not deserialize old state merely because the path exists.

Checkpoint cadence trades lost recomputation against IO, storage, and coordination overhead. Align it with preemption probability, task cost, deadline, and external commit boundaries.

Do not call ordinary output a checkpoint unless replay semantics are defined. A generated file may be partial, non-atomic, or already visible to consumers.

### Define cancellation, suspension, and replacement

Cancellation is a state transition request. The platform stops admitting new work, signals active processes, waits a bounded grace period for checkpoint and cleanup, then may terminate. Provider actions or external effects may complete after the request.

Suspension preserves intent for later resume but may delete active Pods. Local memory and ephemeral files disappear. The contract specifies whether elapsed business deadline continues, which controller deadline resets, and how external leases and partially completed partitions are reconciled.

Schedule `Replace` is cancellation plus a new operation attempt or period intent. It is safe only when the old run can be fenced or checkpointed and the new run knows what to resume. Killing a process does not undo its database or object-store effects.

Report cancelled-clean only after domain state and owned resources meet the clean predicate. Otherwise report cancelled-partial with inventory and remediation ownership.

### Publish and validate results

Workers write staged immutable outputs under operation/execution/partition identities. They never overwrite the canonical published result in place. Each partition result records input and code revisions, checksum, record count or other validation metrics, status, and error class.

A coordinator compares produced results with the expected input manifest, validates schema and domain constraints, and publishes one result manifest through an atomic or fenced commit. Consumers read only committed manifests, not directory listings of worker fragments.

Define whether partial success is invalid, useful but incomplete, or a formally accepted approximation. Record missing partitions and confidence/error rules. Never label a result complete because some success policy ended remaining workers unless the domain contract permits it.

Result acceptance may trigger irreversible downstream effects. Separate computation from publish/commit where possible, and make the commit idempotent by operation key.

### Design the schedule contract

A schedule declares stable identity, owner, batch-template revision, calendar expression, timezone, business-period mapping, release time, starting deadline, overlap policy, catch-up policy, pause, manual rerun/backfill, maximum duration, stale-success alert, input resolution, change control, and retirement.

Kubernetes CronJob creates Jobs approximately according to its schedule. Current documentation explicitly advises idempotent Jobs because creation can be missed or duplicated. Treat CronJob as a materializer of execution intent, not a business guarantee.

Use an explicit timezone rather than controller-local assumptions. Test daylight-saving gaps and repeated local times. Prefer business-period keys derived from a calendar service or explicit domain mapping, not actual Pod start time.

For each materialization, carry scheduled timestamp, schedule revision, business period, and operation key into the Job and domain status. Manual reruns use a new execution identity but normally the same operation/period identity so deduplication and reconciliation remain consistent.

### Choose missed-start and overlap behavior

A starting deadline bounds how late a schedule occurrence may be started. If it expires, record the missed business intent and alert or route it to backfill policy. Do not assume the controller retains every missed occurrence indefinitely.

`Allow` permits overlapping Jobs and requires independent or coordinated operation semantics. `Forbid` withholds a new start while the previous Job is active; it does not by itself create a durable queue of all intended periods. `Replace` ends the old Job to begin the new one and requires safe cancellation/fencing.

Compare worst-case duration $T$ with schedule interval $P$. If $T>P$, steady overlap pressure exists under `Allow`, while `Forbid` or `Replace` sacrifices occurrences or progress. Even when mean $T<P$, tail duration may overlap; size with distributions and business consequences, not averages alone.

Define catch-up explicitly: none, latest-only, every missed period within a bound, or domain-composed range. A large backfill should usually be an authorized batch operation with capacity planning rather than a burst of uncontrolled CronJob creations.

Schedule change semantics matter. Changing 02:00 to 03:00 must not create a second operation for the same day. Version the schedule and map both rules to stable business periods.

### Distinguish scheduled, event-triggered, and continuous workers

A scheduled template materializes work from time/calendar intent. An event-triggered Job materializes bounded work from external demand. KEDA ScaledJob can create Jobs based on scaler observations and is useful when each unit or group should run to completion.

Metrics-based creation does not define broker acknowledgement, lease, ordering, duplicate delivery, poison work, or external-effect commit. Those remain in the application and event contract.

A continuously running consumer is often better for high-throughput streams, connection reuse, partition ownership, low latency, and controlled draining. ScaledJob is better when isolation, bounded execution, resource shape, or terminal result is central. Choose from workload behavior, not because both can “scale from a queue.”

### Secure each execution

Authorize template discovery, submission, schedule creation/change/pause, manual rerun, backfill range, cancellation, logs, results, and cleanup. Derive owner and data access from trusted identity rather than free-form labels.

Use workload-specific service accounts and brokered credentials scoped to input, output, and operation duration. Separate schedule-controller authority to create Jobs from worker authority to read data or commit results.

Restrict images, commands, network destinations, volumes, host access, devices, and privileged modes by supported profile. Batch convenience must not become arbitrary cluster command execution.

Preserve audit links among actor, approver where required, schedule revision, operation/execution IDs, image digest, input/output manifests, policy, credential grants, and terminal evidence. Redact sensitive filenames, query values, records, and secret material.

### Observe progress and outcomes

Emit low-cardinality metrics for requests, admission delay, placement delay, startup, progress age, throughput, retry, checkpoint, commit, validation, terminal status, cost, cleanup backlog, and stale scheduled success. Use traces or correlated events across controller, worker, data store, and result publication.

Progress is workload-specific: partitions validated, bytes processed, records committed, epochs completed, or migration step fenced. Heartbeats without advancing progress can conceal livelock.

Alert on no feasible deadline, unknown effect, exhausted retries, poisoned index, missing result partitions, checkpoint failure, excessive queue age, repeated schedule misses, overlap, stale last successful business period, orphan output, and retention failure.

Logs are evidence but not the status database. Retain structured status and result manifests after Pods disappear, with access and privacy controls.

### Test the entire failure surface

Test schema/defaults, identity/policy, deterministic input binding, rendering, image provenance, normal execution, duplicate start, retryable and terminal errors, ambiguous commit, index duplication, poisoned shard, straggler, quota delay, placement failure, eviction, preemption, checkpoint/resume, cancellation, forced termination, partial output, validation failure, cleanup, and retirement.

Schedule tests include timezone, daylight-saving gap/repetition, controller outage, starting deadline, `Allow`/`Forbid`/`Replace`, long run, manual rerun, bounded backfill, pause/resume, schedule revision, and stale success.

Mocks test logic but not cluster admission, credentials, storage atomicity, signals, provider races, or downstream throttling. Use isolated integration environments and controlled fault injection for representative profiles.

Conformance fixtures should exercise current template, controller adapter, policy, image, and result validation. Existing consumers need current-state checks; ancestry from an old template does not prove safety.

### Retain and clean up by resource class

Define separate retention for Job/CronJob objects, Pods, events, logs, traces, result manifests, outputs, failed fragments, checkpoints, input snapshots, leases, temporary credentials, approvals, and audit evidence. Each has owner, policy, deletion evidence, and legal/privacy constraints.

Kubernetes TTL-after-finished can remove eligible finished workload objects and dependents. It does not delete arbitrary object-store output, database rows, external queues, secrets, cloud resources, or exported data.

Cleanup is idempotent and inventory-driven. Deleting partial output must respect whether it is evidence, resumable state, or user-visible value. Quarantine uncertain data rather than silently destroying it.

Retirement stops new schedule creation, disables materialization, inventories active and suspended runs, resolves unknown effects, migrates schedules, drains executions, revokes identities, expires checkpoints/outputs by policy, removes adapters, and preserves required evidence.

### Operate templates as products

Maintain template/revision owner, supported profiles, controller mappings, consumers, schedules, active operations, conformance, SLOs, costs, exceptions, security review, dependencies, and deprecation. Publish status and support routes.

Measure terminal business outcomes and user effort: time from accepted intent to validated result, deadline success, duplicate-effect prevention, recovery time, schedule freshness, failed cleanup, cost predictability, and migration uptake. Job creation count is not value.

Canary revisions on platform-owned operations with realistic data shapes and failure tests. Roll back new admission without losing status or recovery for already running revisions.

Deprecation identifies replacements and compatibility, tests checkpoint/result migration, changes schedules deliberately, and removes authority last. A retired UI button is not a retired workload path.

The following executable inventory is synthetic design-review evidence. It counts declared controls; it does not prove business idempotency, deadline feasibility, capacity availability, checkpoint correctness, schedule delivery, external cleanup, or production reliability.

<!-- bijux-verify: {"id":"batch-template-control-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"templates 10\nidentity_input_bound 10\nidempotency_retry 9\ndeadline_capacity 9\ncheckpoint_cancel 8\noutput_manifest 9\nquota_placement 8\nschedule_semantics 7\ntelemetry_retention 9\nretirement_owned 8\n","stderr":""}} -->
```python
templates = [
    ("singleton-migration", 1, 1, 1, 1, 1, 1, 0, 1, 1),
    ("indexed-backfill", 1, 1, 1, 1, 1, 1, 0, 1, 1),
    ("ledger-close", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("daily-export", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("gpu-training", 1, 1, 1, 1, 1, 1, 0, 1, 1),
    ("event-transform", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("weekly-compaction", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("legacy-report", 1, 1, 1, 0, 1, 1, 1, 1, 0),
    ("bulk-notification", 1, 1, 1, 1, 1, 0, 1, 1, 1),
    ("experimental-simulation", 1, 0, 0, 0, 0, 0, 1, 0, 0),
]
fields = [
    "identity_input_bound", "idempotency_retry", "deadline_capacity",
    "checkpoint_cancel", "output_manifest", "quota_placement",
    "schedule_semantics", "telemetry_retention", "retirement_owned",
]
print("templates", len(templates))
for index, field in enumerate(fields, start=1):
    print(field, sum(row[index] for row in templates))
```

## Definitions and Notation

Let operation $o=(k,I,O,D,P)$ contain stable operation key $k$, immutable input binding $I$, expected-output contract $O$, deadline $D$, and policy context $P$. Let execution $e=(r,a,v,t,s)$ contain run ID $r$, attempt $a$, implementation/template vector $v$, timestamps $t$, and observed state $s$.

For schedule $S$, mapping $g(S,z,b)=o$ converts schedule revision $S$, timezone/calendar context $z$, and business period $b$ into an operation. Materialization count $m(b)$ may be zero, one, or more; schedule safety cannot assume $m(b)=1$.

Let input manifest partition set be $Q={q_1,\ldots,q_N\}$ and produced valid result set be $R\subseteq Q$. Complete acceptance commonly requires $R=Q$ plus domain predicates, although an explicitly approximate contract may define threshold $A(R,Q)$.

Let $c(k)$ be authoritative commit state: absent, staged, committed, rejected, or unknown. Replay is safe when it observes $c(k)$ and either returns the committed result, resumes compatible staging, or creates one fenced commit; it must not convert unknown directly to absent.

For work $W$, effective worker rate $\mu$, parallelism $n$, and overhead $s$, $s+W/(n\mu)$ is an optimistic sizing estimate. Define schedule interval $P_s$ and execution duration random variable $T$; $T>P_s$ indicates overlap for that observation, while tail probability $\Pr[T>P_s]$ informs policy better than the mean alone.

## Mechanisms, Invariants, or Proof Structure

The assurance chain is:

1. define the domain operation, accepted result, owner, authority, business period, and non-guarantees;
2. bind stable operation identity, immutable input manifest, code/template/policy revisions, and expected output before admission;
3. authorize submission and obtain narrowly scoped execution identity without persisting secret values;
4. admit against quota, priority, topology, downstream capacity, deadline feasibility, and cost policy;
5. execute singleton, fixed, indexed, work-queue, or coordinated jobs with bounded retry and explicit duplicate semantics;
6. checkpoint durable compatible progress and handle cancellation, suspension, replacement, preemption, and unknown effects;
7. stage partition outputs, validate completeness/domain constraints, and publish one fenced result manifest;
8. map schedules through timezone and business periods with explicit lateness, overlap, catch-up, rerun, and backfill;
9. retain correlated status, telemetry, outputs, audit, and cleanup evidence under distinct policies; and
10. test, observe, migrate, deprecate, drain, revoke, clean, and retire every template and external effect.

The central safety argument is conditional. If every execution uses the same operation key for the same intended work, input is immutable, authoritative effects enforce that key or a fence, unknown outcomes are reconciled, and acceptance validates the complete result manifest, then duplicate orchestration need not cause duplicate accepted effects. Violation of any premise invalidates the argument.

The invariants are identity separation, immutable inputs, duplicate tolerance, classified retry, domain-level acceptance, end-to-end timing, capacity-bounded parallelism, explicit interruption effects, calendar-complete scheduling, observable admission, retention separation, and governed lifecycle.

## Alternatives and Trade-Offs

**One execution template versus separate schedule template:** one resource feels simpler but entangles calendar changes with processing correctness. Composition lets manual runs and backfills reuse one operation contract while requiring stable interfaces between products.

**Singleton versus partitioned execution:** singleton coordination and validation are simpler but may miss deadlines. Partitioning improves throughput and failure isolation while introducing skew, duplicate partitions, aggregation, and commit complexity.

**Fixed completions versus indexed completions versus work queue:** fixed completions express quantity; indexed completions give deterministic shard identity; a work queue adapts to uneven cost. The queue adds an external lease/acknowledgement authority.

**Retry versus fail fast:** retry masks transient infrastructure faults but can amplify deterministic errors and duplicate effects. Fail-fast preserves evidence and capacity but increases operator intervention if classification is weak.

**Idempotent upsert versus fenced singleton:** upsert is robust for keyed convergent effects. Fencing protects non-concurrent mutation but requires authoritative token enforcement and availability.

**Frequent versus sparse checkpoints:** frequent checkpoints reduce rework and preemption cost but increase IO, storage, and synchronization. Sparse checkpoints favor throughput but can make deadlines unrecoverable after failure.

**Allow versus Forbid versus Replace:** Allow preserves every attempted occurrence while permitting contention; Forbid prevents overlap but may miss periods; Replace favors freshness but discards progress unless resumption is safe.

**Every-period catch-up versus latest-only:** every-period preserves per-period accounting but can create a capacity storm. Latest-only restores current state quickly but is invalid when each period has independent effects.

**Cron materialization versus calendar workflow service:** CronJob is simple and close to Kubernetes operations. A calendar-aware service can own business periods, approvals, holidays, and durable catch-up at the cost of another critical control plane.

**Scaled Jobs versus continuous consumers:** isolated Jobs suit finite expensive work and terminal artifacts. Continuous consumers reduce startup and coordination overhead for streams but need long-running drain, lease, and rollout semantics.

**Automatic TTL versus explicit archival cleanup:** TTL controls cluster-object growth. Explicit workflows coordinate external evidence and privacy but add inventory and failure modes; most systems need both at different boundaries.

## Failure Modes and Misconceptions

- **“One completion means one execution.”** a controller may start replacement or duplicate Pods.
- **“Exit zero is business success.”** outputs can be missing, corrupt, unpublished, or already duplicated.
- **“Cron means exactly once.”** a scheduled controller can miss or duplicate Job creation.
- **“Actual start time identifies the period.”** admission delay and reruns move wall-clock time.
- **“Forbid queues missed runs.”** it prevents overlap; durable catch-up needs a separate contract.
- **“Replace rolls back the old run.”** termination does not reverse external state.
- **“Retry after timeout is safe.”** the timed-out external effect may have committed.
- **“Parallelism one enforces singleton mutation.”** another Job or stale lease holder can overlap.
- **“A lease guarantees exclusivity.”** without fencing, an old holder may continue writing.
- **“Indexed Jobs prevent duplicate shards.”** index identity does not prevent repeated execution or effects.
- **“More workers always finish sooner.”** skew, critical path, quota, data, and downstream bottlenecks dominate.
- **“Admission means running.”** placement, image, volume, and device waits remain.
- **“Runtime deadline equals business deadline.”** admission and validation may be excluded.
- **“Suspension pauses memory.”** active Pods may be removed and ephemeral progress lost.
- **“A checkpoint is any output file.”** compatible atomic resume semantics are required.
- **“Success policy proves completeness.”** only the domain result contract can permit partial completion.
- **“ScaledJob gives exactly-once event processing.”** metric-triggered creation does not own acknowledgement or effects.
- **“TTL cleans the workload.”** external data, credentials, logs, leases, and audit remain.
- **“Template version proves conformance.”** current runtime, schedule, policy, and consumer state require evidence.
- **“Deleting a schedule retires it.”** active runs, backfills, outputs, identities, and obligations survive.

## Worked Examples

### Example 1

A schema migration uses one Job with `parallelism: 1`. An operator submits the same manifest twice, so two Job objects run. Both read version 172; one applies 173 while the other fails halfway. The corrected design uses operation key `schema/173`, database advisory authority, and a monotonically fenced migration ledger. A duplicate observes committed 173 and verifies checksum instead of applying it. Conclusion: singleton is a domain-coordination property, not a replica setting.

### Example 2

An indexed backfill has 100 partitions and parallelism 20. Partition 47 is started twice after a node loss. Both workers write immutable fragments, but only a conditional manifest entry keyed `operation/47` may commit. The second compares checksum and returns the existing result. The coordinator requires all indices 0–99 before publish. Conclusion: index identity plus conditional result commit tolerates duplicate Pods.

### Example 3

A nightly billing Job charges a provider, receives a network timeout, and exits retryable. The provider actually accepted the charge. Blind retry charges again. With operation key `invoice/8842`, the provider or a local outbox enforces uniqueness; an ambiguous response enters reconciliation and queries by key. Conclusion: timeout is unknown effect, not proof of failure.

### Example 4

A workload has $W=12{,}000$ items, effective rate $\mu=10$ items/second/worker, $n=20$, and overhead $s=120$ seconds. The optimistic estimate is $120+12{,}000/(20\cdot10)=180$ seconds. A single shard contains half the work and the database caps aggregate throughput at 80 items/second, so observed time exceeds 270 seconds. Conclusion: ideal parallel math is a lower estimate; skew and shared bottlenecks govern reality.

### Example 5

A four-hour export spends 150 minutes awaiting quota, 15 minutes placing and starting, 60 minutes computing, 5 minutes committing, and 10 minutes validating. Total is 240 minutes exactly. A Pod-only dashboard reports 75 minutes and calls the deadline healthy. The platform records every timestamp and alerts when admission leaves insufficient feasible time. Conclusion: deadlines must begin at the contractual origin.

### Example 6

A daily schedule at 02:30 Europe/Stockholm encounters the spring daylight-saving gap. No such local instant exists that day. The domain calendar still defines one date period and policy releases it at the next valid instant; operation key uses the date, not start timestamp. In autumn, two 02:30 instants map to the same period key and duplicate materialization reconciles. Conclusion: timezone rules and business identity must be explicit.

### Example 7

A 10-minute reconciliation often runs 14 minutes. `Forbid` prevents overlap, so some occurrences are not started; it does not preserve a durable queue. `Replace` would repeatedly kill before commit. The team chooses an hourly domain-composed reconciliation plus an event-driven repair stream, with stale-state SLO. Conclusion: no overlap switch can repair a schedule whose interval contradicts workload duration.

### Example 8

A GPU training run is preempted. It wrote a checkpoint pointer before the data objects finished uploading. Resume reads corrupt state. The corrected protocol writes immutable checkpoint objects, verifies their checksums, then compare-and-swaps the latest pointer with code/schema/input metadata. Incompatible code starts from the prior compatible checkpoint. Conclusion: atomic publication and compatibility make checkpoints resumable.

### Example 9

Nine of ten export partitions finish, and a success policy stops the straggler. Directory listing looks substantial, so a consumer imports it. The result contract requires all partitions, record totals, schema checks, and a committed manifest; no manifest is published, and the partial set remains quarantined. Conclusion: orchestration success policy cannot redefine domain completeness implicitly.

### Example 10

TTL removes finished Jobs and Pods after seven days. Six months later an audit finds abandoned exports, checkpoints, a cloud credential, and an unexpired lease. The platform adds an external-resource inventory keyed by operation, distinct retention rules, deletion evidence, and retirement reconciliation. Conclusion: cluster garbage collection is only one layer of lifecycle cleanup.

## Cross-Program Connections

- **Distributed systems:** operation keys, retries, ambiguous outcomes, leases, fencing, and reconciliation apply partial-failure reasoning to short-lived work.
- **Data structures and algorithms:** partition balance, work stealing, critical paths, external sorting, and checkpoint representation determine useful parallelism.
- **Operating systems and concurrency:** process signals, scheduling, resource isolation, starvation, and race conditions shape cancellation and execution.
- **Databases:** snapshot isolation, unique constraints, transactions, compare-and-swap, manifests, and migration ledgers provide authoritative commit mechanisms.
- **API and service engineering:** idempotency keys, long-running operations, status resources, cancellation, and problem details define the submission surface.
- **Data engineering:** backfills, watermarking, partition completeness, late data, lineage, and data-quality gates specialize the result contract.
- **Security engineering:** workload identity, least privilege, credential brokering, export control, audit, and artifact provenance bound concentrated authority.
- **Reliability engineering:** SLOs, error budgets, queue delay, stragglers, failure classification, and recovery tests turn controller events into outcomes.
- **Systems engineering:** lifecycle inventory, interfaces, hazards, assurance cases, and retirement prevent local automation from hiding whole-system obligations.
- **Economics and governance:** quota, priority, preemption, accelerator allocation, cost attribution, and retention encode contested resource policy.

## References

1. Kubernetes Authors, “Jobs,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/workloads/controllers/job/
2. Kubernetes Authors, “CronJob,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/
3. Kubernetes Authors, “Job v1 API Reference,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/job-v1/
4. Kubernetes Authors, “CronJob v1 API Reference,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/cron-job-v1/
5. Kubernetes Authors, “TTL-after-finished Controller,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/workloads/controllers/ttlafterfinished/
6. Kubernetes SIG Scheduling, “Kueue Workload,” current documentation, retrieved 2026-09-02. https://kueue.sigs.k8s.io/docs/concepts/workload/
7. Kubernetes SIG Scheduling, “Kueue ClusterQueue,” current documentation, retrieved 2026-09-02. https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/
8. Kubernetes SIG Apps, “JobSet Overview,” current documentation, retrieved 2026-09-02. https://jobset.sigs.k8s.io/docs/overview/
9. KEDA Authors, “Scaling Jobs,” documentation version 2.20, retrieved 2026-09-02. https://keda.sh/docs/2.20/concepts/scaling-jobs/
10. CNCF Platforms Working Group, “Platforms White Paper,” April 2023. https://tag-app-delivery.cncf.io/whitepapers/platforms/
11. Backstage Project, “Software Templates,” current documentation, retrieved 2026-09-02. https://backstage.io/docs/features/software-templates/
12. SLSA, “Provenance,” specification version 1.2, retrieved 2026-09-02. https://slsa.dev/spec/v1.2/provenance
13. NIST, “Secure Software Development Framework (SSDF) Version 1.1,” SP 800-218, February 2022. https://csrc.nist.gov/pubs/sp/800/218/final

## Exercises

### Exercise 1

Define operation identity, execution identity, attempt, business period, input binding, result manifest, commit point, checkpoint, missed run, concurrency policy, admission, and terminal acceptance. For each, give one nearby concept it must not be confused with.

### Exercise 2

Trace an indexed 24-partition backfill from request through immutable input binding, quota admission, placement, duplicate index, checkpoint, partition validation, manifest commit, retention, and cleanup. Show the state after a worker commits output but loses its completion response.

### Exercise 3

A daily 02:30 local-time billing CronJob uses `Replace`, reads `latest`, sends charges without idempotency keys, sets a two-hour active deadline after Pod start, writes directly to a shared output file, treats exit zero as complete, and relies on Job TTL for deletion. Diagnose at least fifteen defects and design corrections.

### Exercise 4

Design a platform portfolio for singleton migrations, CPU backfills, GPU training, scheduled exports, and queue-triggered transforms. Define shared contracts, distinct profiles, quota/priority, controller choices, security, telemetry, conformance tests, and escape conditions without creating one template per team.

### Exercise 5

A timezone rule changes, the schedule controller was unavailable for six hours, one old run has an ambiguous database commit, the replacement template cannot read its checkpoint, and the output contains regulated data nearing its retention limit. Produce a safe recovery and migration decision sequence.

## Answers to the Exercises

### Answer 1

Operation identity names intended domain work and differs from an orchestration run. Execution identity names one run and differs from its business effect. Attempt numbers retry history and is not a new operation by default. Business period names the domain interval and differs from actual start time. Input binding fixes a snapshot/version and differs from a mutable location. A result manifest proves enumerated accepted outputs and differs from directory contents. A commit point is the authoritative acceptance transition and differs from process exit. A checkpoint enables compatible resume and differs from arbitrary partial output. A missed run is unmaterialized or too-late schedule intent and differs from a failed started run. Concurrency policy governs overlap and differs from durable catch-up. Admission grants quota/policy placement eligibility and differs from a running Pod. Terminal acceptance evaluates the domain predicate and differs from controller completion.

### Answer 2

The requester receives operation key bound to the backfill range, 24-entry immutable input manifest, code/template/policy digests, expected result set, owner, deadline, and output location. Authorization issues a scoped execution identity. Admission records queue time and grants a resource profile within quota; placement and process-start times remain separate. Each index deterministically maps to one input entry and writes immutable staged output with checksum/count. Suppose index 11 conditionally commits its manifest entry, then its response disappears and the Pod is replaced. The replacement observes operation/index 11 already committed, verifies matching input/code/checksum, and reports success without rewriting. Other workers checkpoint only compatible progress. The coordinator requires all 24 unique valid entries and domain totals, then compare-and-swaps one committed result manifest keyed by operation. Consumers read only that manifest. Runtime objects expire under operational policy; logs, result, failed fragments, checkpoints, input snapshot, credential, audit, and deletion evidence each follow separate owned retention. Any checksum conflict becomes terminal ambiguity, not last-writer-wins.

### Answer 3

The design confuses local clock with business identity; omits explicit timezone and daylight-saving policy; omits stable period key; uses replacement without safe checkpoint, fencing, or cleanup; reads mutable input; lacks an input manifest; sends non-idempotent charges; treats timeout as replayable; has no authoritative commit observation; measures deadline after queue, placement, and startup; omits feasibility alert; writes non-atomic shared output; permits overlapping writers during termination; lacks partition/expected-result manifest; treats exit zero as domain acceptance; omits structured state and unknown effect; lacks least-privilege execution identity and secret-reference policy; has no manual rerun/backfill semantics; omits stale-success alert; and assumes TTL deletes external output, logs, credentials, leases, and audit. Correct it with an explicit timezone/calendar mapping to operation `billing/<period>`, immutable ledger snapshot, same operation key across retries, unique/fenced charge commit or transactional outbox, reconciliation after ambiguity, end-to-end deadline timestamps, a concurrency policy compatible with measured duration, checkpoint-safe cancellation if replacement remains, immutable staged outputs and atomic validated manifest, scoped identity, structured telemetry, explicit repair APIs, and resource-specific retention/cleanup evidence.

### Answer 4

Create one versioned batch-operation contract for identity, immutable input/output manifests, image provenance, policy, admission/status, retry, deadline, checkpoint, result validation, telemetry, retention, support, and retirement; compose one schedule contract for timezone, period, lateness, overlap, catch-up, rerun, pause, and revision. Profiles specialize behavior: migrations use fenced singleton authority and narrow database identity; CPU backfills use indexed or work-queue partitions and database throughput caps; GPU training uses accelerator topology, long admission visibility, checkpoint compatibility, and cost bounds; exports add schedule/calendar, regulated destinations, manifest publication, and privacy retention; queue transforms use ScaledJob only when each event group is bounded, otherwise a continuous consumer archetype. Kueue-style admission governs shared CPU/GPU quota, cohorts, priority, and preemption policy without promising placement. Common telemetry correlates operation/execution/attempt and timing stages. Tests cover duplicate effects, ambiguity, partition completeness, capacity, preemption, cancellation, daylight saving, catch-up, and cleanup. Escape review handles distributed frameworks, special hardware, non-checkpointable long jobs, stronger calendar workflows, or effects the platform cannot fence. Team ownership is an input and policy relationship, never a template fork reason.

### Answer 5

First pause new materializations and preserve read-only status; do not kill the active old run blindly. Freeze the affected business-period mapping under both schedule revisions and inventory intended, materialized, active, missed, and completed operations for the six-hour outage. Resolve the ambiguous database commit through authoritative operation key, transaction ledger, result records, and fencing state; if it remains unknowable, escalate to domain reconciliation and forbid retry. Assess the checkpoint format and old image trust. If the replacement cannot read it, either resume the old trusted revision under constrained identity to reach a safe commit/checkpoint or abandon only after proving partial effects fenced and inventoried; never deserialize incompatibly. Quarantine regulated partial/output data, apply access controls, and prioritize validation, authorized publish, or deletion before retention expiry while preserving required audit. Generate bounded catch-up operations by stable business period rather than replaying wall-clock ticks, capacity-plan them, and avoid overlap with the uncertain operation. Test the new timezone mapping across gap/repetition and prove it maps each domain period once by key even if materialization duplicates. Migrate schedules only after active-state reconciliation, checkpoint/result compatibility decision, credential review, and dry-run inventory. Resume canary periods, verify terminal business outcomes and cleanup, then drain old schedules, revoke old authority, remove incompatible artifacts by policy, and retain the incident/migration evidence.
