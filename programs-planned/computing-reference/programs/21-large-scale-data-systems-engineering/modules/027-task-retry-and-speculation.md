---
module_id: LSDS-027
program: Large-Scale Data Systems Engineering
level: 1
module_number: 27
title: Task Retry and Speculation
status: complete
last_verified: 2026-09-03
---

# Task Retry and Speculation

## One-Page Review

### Governing question

How should a large-scale data system recover failed task attempts and duplicate suspected stragglers without changing results, multiplying external effects, amplifying overload, accepting corrupt output, or hiding the real cause of slow work?

### Essential definitions

- A **task** is one logical partition of work; an **attempt** is one execution of that task.
- A **retry** launches a new attempt after failure or loss under a bounded policy.
- **failover scope** is the set of tasks or regions invalidated and restarted after a failure.
- **backoff** delays retries, commonly increasing after repeated failure; **jitter** decorrelates many clients.
- A **retry budget** bounds attempts or retry work over a task, job, failure domain, or time window.
- A **straggler** progresses materially slower than comparable tasks for a reason not yet known.
- **speculative execution** launches a duplicate attempt before the original has definitively failed.
- The **commit winner** is the one authorized attempt whose isolated output becomes authoritative.
- A **deterministic task** reproduces the declared result from the same immutable inputs and environment contract.
- A **poison record** or deterministic defect fails again under unchanged conditions; retries cannot repair it.

### Central model, mechanism, or theorem

Logical task identity is stable across attempts: `T=(job,stage,partition,plan,input)`, while attempt identity adds an attempt number or unique token. Retrying is safe only when each attempt reads compatible immutable inputs and cannot expose competing output before one winner is committed. Speculation obeys the same rule because original and duplicate overlap.

An exponential backoff can be modeled as `delay_i=min(cap,base*factor^(i-1))`, then randomized within a declared jitter policy. A straggler detector should compare comparable cohorts after minimum runtime and minimum completed-task evidence, using progress or remaining-time estimates rather than duration alone. Expected benefit must exceed duplicate CPU, memory, I/O, network, cache, and sink contention. No detector proves the original is faulty.

### Critical invariants

- Task and attempt identities are distinct, globally unambiguous, and preserved through scheduler recovery.
- Retry classification separates transient infrastructure, input/data, deterministic code, resource, policy, cancellation, and ambiguous external-effect failures.
- Attempts consume the exact approved input/schema/code/configuration or are treated as a new run.
- Candidate output is attempt-isolated, validated, and invisible until an atomic commit winner is chosen.
- Losing, canceled, and late attempts cannot overwrite, append to, or resurrect committed output.
- Retry/backoff/budget limits apply across correlated workers and failure domains, not merely one process counter.
- Speculation uses comparable cohorts, bounded caps, minimum runtime, progress, and resource-health guards.
- Duplicate attempts are charged to quotas, fair share, rate limits, metrics, and cost.
- External effects use idempotency, transactions, outbox/reconciliation, or are excluded from speculative/retryable regions.
- Logs retain root cause, every attempt, invalidated work, winner, cleanup, and final output identity.

### Common failures

Frequent failures are retrying deterministic exceptions indefinitely, synchronizing retry storms, resetting budgets after scheduler restart, retrying on the same broken host or stale input, judging stragglers against incomparable partitions, speculating before enough evidence, duplicating a hot task that is slow because of intrinsic data, letting duplicates contend for the same bottleneck, writing candidates to one final path, using last-writer-wins, incrementing external counters per attempt, accepting a late canceled result, and reporting eventual success without the failed-attempt cost or data loss.

### Compact example

A bounded policy with base 2, factor 2, and cap 8 yields retry delays 2, 4, and 8 seconds. Completed comparable peers have median duration 10, so a 1.5 multiplier gives a 15-second minimum straggler threshold. Of three running partitions, only partition 7 has both elapsed time above the threshold and estimated remaining work above 10; it receives one duplicate. The speculative attempt finishes first and wins a stable commit token. Both attempts remain charged. This arithmetic illustrates policy, not proof that speculation helps production.

### Connections

[LSDS-021](021-mapreduce-execution-model.md) supplies task attempts and output commit. [LSDS-024](024-directed-acyclic-graph-execution.md) supplies lineage/failover scope. [LSDS-026](026-stage-scheduling.md) supplies resource admission and fairness. [LSDS-028](../ROADMAP.md) and [LSDS-029](../ROADMAP.md) cover materialization and checkpoints that bound recomputation.

## Governing Question

Failures are ordinary at scale: processes crash, hosts disappear, disks and networks time out, credentials expire, dependencies throttle, and schedulers restart. Retrying a pure partition computation is often cheaper than making every component failure-free. Speculation addresses a different problem: a still-running task may be so slow that duplicating it elsewhere shortens the job tail.

Both mechanisms deliberately execute one logical task more than once. That fact must shape identity, state, output, effects, accounting, and observability. If an attempt appends directly to a final file or charges an account, a retry can corrupt or duplicate the result. If output is isolated and a coordinator atomically chooses one valid winner, attempts can race without changing the logical output.

The governing question is how to distinguish repairable failures and genuine stragglers from deterministic defects, skew, and overload, then spend bounded duplicate work only when correctness and expected value justify it.

## Why This Matters

Without retry, one transient machine loss can fail hours of work. With uncontrolled retry, the same incident becomes a retry storm that saturates the dependency preventing recovery. A five-attempt local limit multiplied by thousands of partitions can create tens of thousands of extra executions.

Long-tail tasks govern stage completion. Speculation can mask a noisy host or transient slow read. It cannot make one indivisible hot key cheaper. Duplicating that group often doubles its network and CPU pressure. A detector based only on elapsed duration also penalizes partitions that are legitimately larger.

Correctness risks are subtle. Counters may count every attempt while output includes one. A failed attempt may have emitted external messages before its output was discarded. A scheduler restart may forget a winner and accept a late duplicate. A retry may resolve a mutable path to newer files and produce a different partition under the same task label.

Recovery is therefore an end-to-end protocol, not a loop around a function. It joins failure classification, scheduler state, immutable inputs, attempt isolation, commit, cleanup, fairness, rate limiting, and human-visible evidence.

## Prerequisites and Retrieval

Recall immutable inputs, partition identity, and locality from [LSDS-003](003-range-hash-and-consistent-partitioning.md) and [LSDS-004](004-data-locality.md); stages and dependency width from [LSDS-005](005-distributed-task-graphs.md) through [LSDS-007](007-narrow-and-wide-transformations.md); serialization from [LSDS-008](008-serialization-across-workers.md); and scale accounting from [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md).

Retrieve MapReduce task/attempt/commit semantics from [LSDS-021](021-mapreduce-execution-model.md), deterministic partitioning/combination from [LSDS-023](023-partitioners-and-combiners.md), DAG lineage from [LSDS-024](024-directed-acyclic-graph-execution.md), lazy capture from [LSDS-025](025-lazy-evaluation-and-plan-construction.md), and resource/fairness controls from [LSDS-026](026-stage-scheduling.md).

You should understand percentiles/medians, exponential functions, randomized jitter, idempotency, atomic publication, leases, immutable snapshots, critical paths, and the difference between logical results and observed execution work.

## Learning Objectives

After this module, you should be able to:

1. distinguish tasks, attempts, retries, speculation, failover scope, and commit winners;
2. classify failures by retryability and choose bounded backoff/budget policy;
3. model deterministic recomputation over immutable input and pinned execution context;
4. design attempt-isolated output and atomic winner selection;
5. estimate stragglers using comparable cohorts, minimum evidence, progress, and remaining work;
6. explain when skew, congestion, external limits, or deterministic code make duplication harmful;
7. protect external effects with idempotency, transactions, or a separate publisher;
8. account duplicate work in scheduling, quotas, cost, metrics, and governance;
9. test scheduler loss, late attempts, commit races, retry storms, and ambiguous effects; and
10. evaluate recovery by correctness, tail improvement, added work, load amplification, and affected cohorts.

## Core Exposition

### Identity before policy

A logical task key includes job/run, physical-plan version, stage, partition, input snapshot, and relevant configuration. Each attempt adds a unique identity and generation. Scheduler recovery must reconstruct which attempts are live, invalid, successful candidates, and committed.

Do not use a process ID or worker-local counter as durable attempt identity. A restarted coordinator can reuse it. Commit and cleanup APIs should require task identity, attempt identity, generation, and expected artifact metadata.

### Failure classification

Classify before retry:

- **transient infrastructure**: lost worker, temporary network failure, unavailable service;
- **resource**: memory, disk, descriptors, network buffers, quota, or timeout caused by sizing;
- **data/input**: corrupt object, missing partition, poison record, incompatible schema;
- **deterministic code/configuration**: assertion, type error, missing dependency, invalid parameter;
- **policy/security**: denied authorization, expired or wrong-scope credential, residency violation;
- **cancellation/preemption**: intentional termination, not necessarily failure;
- **ambiguous external effect**: timeout after a request may have committed remotely.

Retrying can help the first category and some one-off resource/location failures. Identical retries rarely repair deterministic data/code/policy errors. An ambiguous effect requires reconciliation, not blind repetition. Classification can evolve as correlated evidence accumulates.

### Retry scope

Task retry re-executes one partition when its upstream inputs remain valid. Pipelined operators may co-fail as a region because an unmaterialized producer output is lost. Shuffle loss may invalidate downstream consumers or require upstream recomputation. Coordinator failure can require state reconstruction, not just task restart.

Choose the smallest safe scope whose required artifacts and state remain valid. Too broad wastes work; too narrow mixes incompatible state. Record why each task was invalidated and the checkpoint/materialization boundary used.

### Backoff, jitter, and budgets

Immediate retry is reasonable for a rare isolated loss when capacity exists. Correlated outages require backoff. Fixed delay is predictable; exponential delay reduces repeated pressure; jitter decorrelates a fleet. Cap delay and total elapsed recovery so users receive a terminal result.

Budgets may bound attempts per task, failures per stage/job, retry CPU/bytes/cost, or failures per domain/time window. Persist budgets across coordinator restarts. A successful attempt may reset a consecutive-failure counter in a particular engine, but operators still need total failed-work evidence.

Retry elsewhere when host/disk/rack evidence implicates placement. Conversely, local state can make same-node recovery much faster if the node is healthy. Use quarantine/blacklisting cautiously: correlated workload defects can falsely condemn many workers.

### Deterministic recomputation

Recovery assumes the same logical task can be reconstructed. Pin input file/object/table snapshots, schema, partition boundaries, side inputs, code/dependencies, locale/timezone, numeric behavior, seed, clock policy, environment, and authorization/purpose context.

Nondeterminism can be acceptable if the output contract allows it, but retry then may choose a different valid result. State that explicitly and ensure downstream comparison/commit tolerates it. For reproducible randomness, derive per-record streams from stable seed and record identity rather than attempt number.

### Attempt-isolated output and commit

Every attempt writes to a unique location or transaction. It produces metadata: task/attempt/generation, schema, partition, record/byte counts, checksum, input/plan identity, and validation state. A commit coordinator atomically associates one valid candidate with the logical task or final manifest.

Losers receive cancellation but may continue briefly. The final namespace must reject late writes and stale generations. Cleanup is idempotent and never deletes the winner. Last-writer-wins is not an atomic task-output protocol because arrival order says nothing about validity.

### External effects

A retryable transform must not assume per-attempt effects run once. Counters/metrics should label attempt versus committed logical counts. For database changes, messages, payments, or notifications, use stable idempotency keys, transactions, an outbox, or a separate commit-aware publisher consuming immutable results.

Ambiguous timeouts require querying the remote effect by idempotency key before retry. If the dependency offers no idempotency or reconciliation, exclude that operation from speculation and require an explicit manual/compensating protocol.

### Straggler detection

Compare tasks only within a meaningful cohort: same stage/operator, input type/size band, resource shape, locality, attempt generation, and relevant key distribution. Wait for a minimum number/fraction of peers and minimum runtime. Medians and robust quantiles resist outliers better than means.

Elapsed duration alone is incomplete. Use progress rate or estimated remaining time, while recognizing that progress counters can be nonlinear or misleading. A reduce task may appear stalled during a long final group. A partition with twice the bytes is not anomalous merely because it takes twice as long.

### Speculation decision

Launch a duplicate only when estimated remaining time saved, multiplied by probability the duplicate wins, exceeds launch/locality/cache cost and added contention/risk. Cap speculative tasks globally, per job/stage/host, and by resource. Disable or tighten it for scarce accelerators, rate-limited dependencies, non-idempotent effects, or saturated shuffle/storage.

Place the duplicate in a distinct suspected failure domain when possible. Duplicating on the same slow disk or rack learns little. Preserve data locality without recreating the same bottleneck.

### Skew versus bad luck

Intrinsic skew follows the task's data: a hot key, huge partition, expensive values, output amplification, or pathological algorithm. Both attempts will likely be slow. Infrastructure stragglers follow placement: noisy CPU, failing disk, packet loss, throttling, garbage collection, or cold cache.

Compare input bytes, records, groups, largest group, CPU, spill, network, output, host history, and peer-normalized progress. Skew needs repartitioning, salting/second merge, adaptive splitting, or algorithm change—not duplication alone.

### Cancellation and late results

After one attempt wins, cancel others cooperatively and enforce hard stale-generation rejection at commit. A canceled process may ignore interruption, finish an RPC, or report success after coordinator failover. Authoritative state, not the worker's belief, decides acceptance.

Track time from winner to loser termination and resource release. Speculation that saves one second but leaves duplicates running for minutes can worsen cluster tails.

### Failure amplification

Retry load is feedback. If dependency capacity falls by half while clients double attempts, recovery recedes. Coordinate backoff, jitter, concurrency limits, circuit breakers, admission control, and dependency health. A retry budget is a resilience control, not merely cost optimization.

Different layers can multiply: SDK, task runner, scheduler, service client, proxy, and database may each retry. Document the combined worst case. Prefer one layer owning end-to-end policy or propagate budgets/deadlines.

### Observability and evaluation

Record failure classification/cause chain, task and attempt IDs, worker/failure domain, inputs/code/config, start/progress/end, resource and I/O metrics, backoff, budget, retry trigger, speculation cohort/threshold/estimate, candidate artifacts, winner decision, cancellation, cleanup, and effects.

Measure task success after retries, terminal failures, attempt distribution, retry CPU/bytes/cost, recovery time, speculative launch/win rate, useful time saved, duplicate work, loser lifetime, bottleneck load, p50/p95/p99 stage/job completion, output equivalence, and results by tenant/data cohort. Compare against retry-only and speculation-off baselines.

### Security, governance, and human impact

Attempts need scoped credentials and should not extend privilege or data retention. Temporary outputs, logs, poison-record samples, and failure payloads can expose sensitive data. Encrypt, minimize, redact, authorize, expire, and audit them; deletion must cover losers.

Retry policy can delay time-critical public or regulated outcomes and concentrate failures in underrepresented data. Examine deterministic error/quarantine and tail rates by relevant cohort. Provide correction, appeal, incident escalation, and named domain/affected-party review without hiding failures through tolerance thresholds.

## Definitions and Notation

- `T`: logical task identity; `A_i`: attempt `i` for `T`.
- `g`: scheduler/attempt generation used to reject stale reports.
- `d_i`: retry delay after failure `i`; `b`: base delay; `f`: factor; `c`: cap.
- `d_i=min(c,b*f^(i-1))`: capped exponential delay before jitter.
- **retryability**: classification that another attempt under changed time/place/resources may succeed safely.
- **failover scope**: invalidated task/region set needed to restore consistent execution.
- **cohort**: tasks comparable for straggler estimation under declared features.
- `elapsed`: current attempt runtime; `progress`: bounded declared completion estimate.
- **estimated remaining**: policy estimate, not guaranteed time to finish.
- **speculation cap**: maximum concurrent/total duplicates in a declared scope.
- **candidate artifact**: isolated validated attempt output not yet authoritative.
- **commit token**: stable logical output identity used to select or idempotently publish one winner.

## Mechanisms, Invariants, or Proof Structure

Audit retry and speculation in this order:

1. Pin logical task, attempt, generation, input, plan, code, configuration, security, and output identities.
2. Classify failure and decide whether time, placement, resources, or dependencies can change the outcome.
3. Determine the smallest safe failover scope from materialized artifacts and coupled state.
4. Apply persistent attempt/work/time budgets with bounded backoff, jitter, deadline, and dependency-health gates.
5. Isolate attempt state/output; validate candidate metadata, content, and lineage before winner selection.
6. Define atomic commit, stale rejection, cancellation, loser cleanup, and coordinator recovery.
7. Identify every external effect and make it transactional/idempotent/reconciled or remove it from duplicate execution.
8. Build comparable straggler cohorts with minimum evidence, progress/remaining estimates, and skew diagnostics.
9. Bound duplicate resources and place outside suspected failure domains while charging fairness/cost.
10. Test correlated faults, poison data, skew, late reports, commit races, scheduler restart, ambiguous effects, and policy drift; evaluate both correctness and net benefit.

The retry proof requires semantic reproducibility plus publication uniqueness. Either every valid attempt produces an equivalent candidate under the declared contract, or allowed nondeterminism is explicit; then atomic commit exposes at most one authoritative candidate. This does not make arbitrary external effects safe.

The speculation argument is empirical and conditional. A threshold detects candidates, not faults. Compare saved critical-path time with duplicate resource work and externalized bottleneck harm under representative/adversarial loads.

<!-- bijux-verify: {"id":"retry-and-speculation-policy","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"backoffs=(2, 4, 8)\npeer_median=10 threshold=15.0\nspeculate=('partition-7',)\nwinner=attempt-1 commit_token=job42-stage3-part7\nattempts_charged=2\n","stderr":""}} -->
```python
from statistics import median


def backoffs(base, factor, cap, failures):
    return tuple(min(cap, base * factor**index) for index in range(failures))


peers = (8, 9, 10, 11, 12)
peer_median = median(peers)
threshold = 1.5 * peer_median
running = {
    "partition-7": {"elapsed": 16, "progress": 0.4},
    "partition-8": {"elapsed": 14, "progress": 0.3},
    "partition-9": {"elapsed": 20, "progress": 0.9},
}


def remaining(sample):
    return sample["elapsed"] * (1 - sample["progress"]) / sample["progress"]


speculate = tuple(
    name
    for name, sample in running.items()
    if sample["elapsed"] >= threshold and remaining(sample) > 10
)
attempt_finishes = {"attempt-0": 40, "attempt-1": 26}
winner = min(attempt_finishes.items(), key=lambda item: item[1])[0]

print(f"backoffs={backoffs(2, 2, 8, 3)}")
print(f"peer_median={peer_median} threshold={threshold}")
print(f"speculate={speculate}")
print(f"winner={winner} commit_token=job42-stage3-part7")
print(f"attempts_charged={len(attempt_finishes)}")
```

The linear progress estimator is intentionally simple and can be wrong for nonlinear phases. The stable commit token names the logical partition, while attempt identities distinguish candidates.

## Alternatives and Trade-Offs

**No retry versus bounded retry.** No retry surfaces deterministic defects quickly but sacrifices resilience to transient loss. Bounded retry recovers common faults while limiting amplification.

**Fixed versus exponential backoff.** Fixed delay is predictable. Exponential backoff reduces pressure during long outages but can delay recovery; cap, jitter, and deadline it.

**Local versus remote retry.** Local retry can reuse cache/state. Remote retry escapes a bad host/domain. Health and locality evidence decide.

**Task versus region/job failover.** Narrow scope saves work when boundaries are valid. Broader scope restores consistency when pipelined or stateful tasks co-fail.

**Retry-only versus speculation.** Retry-only avoids concurrent duplicate work. Speculation can shorten straggler tails but requires output/effect safety and resource headroom.

**Duration versus progress-based detection.** Duration is robust and cheap but ignores partition size. Progress/remaining models are more specific but can be nonlinear, manipulable, or noisy.

**Immediate cancellation versus graceful loser shutdown.** Immediate kill frees capacity but can interrupt cleanup. Graceful shutdown preserves invariants but must be bounded and stale commits rejected.

**Lineage recomputation versus checkpoint/materialization.** Lineage reduces eager I/O. Materialization bounds recovery and nondeterminism at storage/cost and governance expense.

## Failure Modes and Misconceptions

**"Retry fixes failure."** It changes attempt time/place; unchanged deterministic data or code usually fails again.

**"Four attempts means four retries."** Often the initial attempt counts, so retries equal attempts minus one; verify the concrete engine.

**"A successful retry erases the incident."** Output may be valid, but failed work, latency, cost, and correlated risk remain evidence.

**"Speculation is retry after a timeout."** Speculation overlaps a still-running original; both can complete and race.

**"The slowest task is defective."** It may own more bytes, a hot group, expensive values, or required output.

**"A duplicate elsewhere is independent."** It may share storage, rack, service, key hotspot, or global rate limit.

**"Only the winner counts."** All attempts consume resources and can emit metrics/effects; accounting must distinguish logical and physical work.

**"Last writer wins is fine."** It can publish stale, incomplete, or incompatible output and cannot explain authority.

**"Cancellation prevents late output."** Processes and RPCs can outlive cancellation; commit fencing must reject stale generations.

**"Idempotent means safe forever."** Key scope, retention, payload equality, concurrency, and replay horizon must be defined.

**"More retries improve availability."** During correlated overload they can reduce it; budgets, backoff, jitter, and admission are essential.

**"Failure tolerance permits dropping bad records."** Skipping changes semantics and can create cohort harm; it needs explicit policy, accounting, and review.

## Worked Examples

### Example 1

A worker disappears halfway through a pure map task. Its attempt output is isolated and incomplete, inputs are immutable, and another healthy worker exists. Retry elsewhere under the same task/plan/input identity is safe; the failed candidate is never committed.

### Example 2

A parser throws on the same malformed record across two workers. Further identical retries waste capacity. Quarantine or fail according to an explicit data-quality contract, preserving encrypted/minimized evidence and affected-cohort counts. Silent skip is not recovery.

### Example 3

Ten thousand tasks hit an unavailable service. Immediate synchronized retries double load. Exponential full-jitter backoff, a global dependency retry budget, circuit breaker, and admission reduction let the service recover. Per-task limits alone miss aggregate amplification.

### Example 4

A pipelined consumer fails after its producer output was never materialized. Restarting only the consumer cannot recover the missing stream. The failover region includes co-failing producer/consumer tasks from the last valid boundary.

### Example 5

Peers of similar input size finish near 10 seconds. Partition 7 runs 16 seconds at 40 percent, implying 24 estimated seconds remaining under a linear model. Partition 9 runs 20 seconds at 90 percent, implying about 2.2 remaining. Speculate 7, not 9, subject to resource health and caps.

### Example 6

A hot key forms one 500-GiB reduce group. Every duplicate reads and computes the same huge group. Both are slow and storage load doubles. Use a semantically mergeable fanout plus second merge, or change the algorithm; speculation only masks unrelated host variance.

### Example 7

Original and duplicate write unique objects with digests. Duplicate finishes first; coordinator commits its object in the manifest under the logical task token. Original finishes late and its stale commit is rejected. Cleanup deletes only the losing object after retention/debug policy.

### Example 8

A task sends a payment and times out before receiving the response. A retry queries by stable payment idempotency key. If committed, it records/reuses that result; if absent, it safely submits. Changing the idempotency key per attempt can double-charge.

### Example 9

Speculation wins 40 percent of launches but saves only 0.5 percent p99 latency while adding 18 percent shuffle read and worsening other tenants' slowdown. Win rate alone is misleading; disable or retune using net critical-path, bottleneck, fairness, and cost evidence.

### Example 10

A benefits pipeline retries more often for records from one region because an external address service has poor coverage. Overall success hides delayed decisions for that cohort. Preserve retry/error rates and elapsed outcomes by region, involve domain/affected-party reviewers, and provide correction/appeal rather than lowering evidence standards.

## Cross-Program Connections

- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies partial failure, leases, fencing, idempotency, consensus, and recovery.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies process failure, signals, resource exhaustion, and scheduling.
- [Network Engineering](../../24-network-engineering/ROADMAP.md) supplies timeouts, correlated loss, congestion, backoff, and retry storms.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies transactions, idempotency keys, outboxes, and commit records.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) applies retries to pipelines, data quality, lineage, backfills, and publication.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies robust statistics, online detection, randomized jitter, and adversarial analysis.
- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) connects duplicate attempts to races, cancellation, futures, and side effects.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies scheduler state, quotas, observability, isolation, and incident control.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies scoped credentials, temporary artifact protection, fencing, and audit.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies feedback loops, coupled failure, emergent overload, and risk review.

## References

1. Apache Spark. [Configuration: Task Failure and Speculation](https://spark.apache.org/docs/latest/configuration.html). Accessed 2026-09-03.
2. Apache Spark. [RDD Programming Guide: Fault Tolerance and Persistence](https://spark.apache.org/docs/latest/rdd-programming-guide.html). Accessed 2026-09-03.
3. Apache Hadoop. [JobConf API](https://hadoop.apache.org/docs/current/api/org/apache/hadoop/mapred/JobConf.html). Accessed 2026-09-03.
4. Apache Hadoop. [TaskAttemptContext API](https://hadoop.apache.org/docs/current/api/org/apache/hadoop/mapreduce/TaskAttemptContext.html). Accessed 2026-09-03.
5. Apache Hadoop. [MapReduce Tutorial](https://hadoop.apache.org/docs/stable3/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html). Accessed 2026-09-03.
6. Apache Flink. [Task Failure Recovery](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/task_failure_recovery/). Accessed 2026-09-03.
7. Apache Flink. [RestartBackoffTimeStrategy API](https://nightlies.apache.org/flink/flink-docs-stable/api/java/org/apache/flink/runtime/executiongraph/failover/RestartBackoffTimeStrategy.html). Accessed 2026-09-03.
8. Apache Flink. [Batch Job Progress Recovery](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/batch/recovery_from_job_master_failure/). Accessed 2026-09-03.
9. Apache Flink. [High Availability](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/ha/overview/). Accessed 2026-09-03.
10. Apache Beam. [Execution Model](https://beam.apache.org/documentation/runtime/model/). Accessed 2026-09-03.
11. Jeffrey Dean and Sanjay Ghemawat. [MapReduce: Simplified Data Processing on Large Clusters](https://research.google.com/archive/mapreduce-osdi04.pdf). OSDI 2004. Accessed 2026-09-03.
12. Jeffrey Dean and Luiz André Barroso. [The Tail at Scale](https://research.google/pubs/the-tail-at-scale/). Communications of the ACM 2013. Accessed 2026-09-03.

## Exercises

### Exercise 1

Run the compact policy by hand. Recompute backoffs, threshold, remaining estimates, speculation choice, winner, and accounting.

### Exercise 2

Classify and design responses for worker loss, poison input, memory exhaustion, expired credentials, dependency timeout, preemption, and ambiguous payment response.

### Exercise 3

Specify an attempt-isolated object-output protocol robust to speculation, scheduler restart, late results, checksum failure, and cleanup retry.

### Exercise 4

Design an experiment distinguishing intrinsic skew from infrastructure stragglers and deciding whether speculation has net benefit.

### Exercise 5

Specify named review and evidence for retries in a regulated pipeline whose failures and delays differ across affected populations.

## Answers to the Exercises

### Answer 1

Capped exponential delays are `min(8,2*2^0)=2`, then 4 and 8. Peer median is 10 and multiplier 1.5 gives threshold 15. Partition 7 has elapsed 16 and linear remaining `16*(0.6/0.4)=24`, so it qualifies. Partition 8 is below minimum elapsed; partition 9 has remaining `20*(0.1/0.9)` about 2.2, so neither qualifies. Speculative attempt 1 finishes at time 26 before original attempt 0 at 40 and wins stable logical token `job42-stage3-part7`. Both attempts count toward resources, fairness, metrics, and cost; only one candidate becomes authoritative.

### Answer 2

Worker loss is transient: retry on a healthy domain with immutable input. Poison input is deterministic: fail/quarantine under explicit semantics rather than repeat. Memory exhaustion needs repartitioning, larger request, spill/algorithm change, or bounded same/different-node retry based on evidence. Expired credentials may be refreshed only if scope/purpose remains authorized; denial is not bypassed. Dependency timeout uses idempotency, reconciliation, health-gated backoff/jitter/budget. Preemption is an intentional canceled attempt and can retry when admitted. Ambiguous payment response is queried by stable idempotency key; blind retry is unsafe.

### Answer 3

Each attempt writes an immutable unique object plus metadata binding task/attempt/generation, plan/input/schema/partition, length/count, checksum, and validation. The coordinator durably reconstructs task state, validates candidates, and conditionally creates one manifest association under a stable commit token. Commit is idempotent for the same winner and rejects other attempts, stale generations, or metadata mismatch. After restart it reads authoritative commit records before accepting reports. Late attempts cannot address final names. Cleanup lists only recorded losers, honors diagnostic retention, verifies not referenced by any manifest, and is idempotent; checksum failure invalidates that candidate and may trigger a classified retry.

### Answer 4

Stratify tasks by stage, input bytes/records/groups/largest group, operator, resource shape, locality, and attempt generation. Capture CPU, memory, GC, spill, disk/network/service latency, host/rack history, progress, output, and retries. Inject noisy hosts/network loss separately from hot keys and unequal partitions. Compare speculation off, duration-only, and progress/remaining policies under identical traces with global/per-job caps. Measure output equality, p50/p95/p99 committed latency, critical-path time saved, launch/win rate, duplicate CPU/bytes/cost, loser lifetime, bottleneck load, other-tenant slowdown, and false positives. Skew follows the partition across hosts; infrastructure delay follows placement.

### Answer 5

Pin retry/speculation code/config, task/input/plan/schema identities, classification, budgets/backoff/jitter, cohort features, thresholds, placement domains, output/effect protocol, credentials/purpose, retention/deletion, and incident overrides. Report attempts, failures, quarantines, elapsed decisions, terminal outcomes, and errors by relevant population/jurisdiction, including small groups and missing data; compare to independent correctness and service baselines. Named review includes domain owners, data stewards, privacy/legal/records/jurisdiction authorities, affected communities or ethics oversight, fairness/statistics, security/identity, platform/runtime/network/dependency operators, accessibility, incident recovery, and independent assurance. Retry success cannot hide disparate delay, dropped records, unsafe effects, or absent correction/appeal.
