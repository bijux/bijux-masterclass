# BatchWeave — a bounded deterministic concurrent batch engine

**Course 7 capstone** · [Course overview](index.md) · [Study plan](study-plan.md) · [Reference desk](reference.md) · [Implementation](../capstone/README.md)

BatchWeave is the cumulative product for Modules 61–70. It accepts a small manifest of CPU-oriented jobs, processes them through a fixed worker group, and returns a deterministic report. That sentence sounds ordinary. Making every word true under success, domain failure, cancellation, panic, queue closure, thread-spawn failure, and nondeterministic completion is the real project.

The capstone is not a tour of concurrency APIs. It is one product whose contract gradually becomes strong enough to survive concurrency. Each module contributes one new obligation. The final architecture uses ordinary safe Rust for the engine and Rayon for a separate data-parallel reporting stage. The unsafe SPSC ring from Module 68 remains an independent laboratory because inserting it into the product would weaken the design without solving a demonstrated bottleneck.

## 1. Product contract

BatchWeave reads this format:

```text
BATCHWEAVE-V1
# id<TAB>operation<TAB>payload
checksum-readme	checksum	reader-first concurrency
count-words	word-count	one two three four
sort-values	sort-integers	9,-4,7,0
count-primes	prime-count	100
```

For every accepted job it produces exactly one terminal outcome:

```text
Completed(value)
DomainFailed(message)
Panicked
Cancelled
```

Final output follows manifest order, even if later jobs finish first. A complete run returns only after every worker has terminated and been joined. A product-level failure exit status is distinct from a usage, parsing, configuration, or infrastructure error.

The central invariant is:

> For every accepted manifest index `i`, the final outcome vector contains exactly one outcome whose index and identity belong to `i`.

No live counter, channel length, queue length, or number of successful joins substitutes for that invariant.

## 2. Architecture at a glance

```text
UTF-8 manifest
      │ checked parser: unique IDs, stable indices, bounded payload
      ▼
coordinator owns Vec<Job>
      │ blocking push
      ▼
Arc<BoundedQueue<Job>> ───── close/cancel ─────┐
      │                                        │
      ├──────── fixed worker 0                 │
      ├──────── fixed worker 1                 │
      └──────── fixed worker N                 │
               │ one typed result per popped job
               ▼
        unique result receiver
               │ index validation
               ▼
       Vec<Option<JobOutcome>>
               │ join every worker
               │ reject protocol defects
               ▼
        Vec<JobOutcome> in source order
               │ immutable input
               ▼
       dedicated Rayon report pool
               │ associative merge
               ▼
        ordered summary and rendering
```

The coordinator owns lifecycle. Workers own one popped job at a time. The queue owns pending jobs. Result messages transfer completed terminal outcomes back to the coordinator. Rayon receives only immutable, fully reconciled outcomes and has no role in worker shutdown.

## 3. The six ledgers

Before changing the implementation, update six small reasoning artifacts.

### Ownership ledger

| Value or resource | Initial owner | Cross-thread mechanism | Final cleanup owner |
|---|---|---|---|
| parsed `Vec<Job>` | coordinator | jobs move one at a time into queue | worker or rejected-job reconciliation |
| bounded queue | coordinator | `Arc` shared among coordinator and workers | final `Arc` owner |
| cancellation state | coordinator | `Arc<AtomicBool>` | final `Arc` owner |
| result sender | coordinator | clone per worker, then original dropped | each worker drops clone |
| result receiver | coordinator only | never shared | coordinator |
| worker handles | coordinator | no transfer | coordinator joins all |
| reconciled outcomes | coordinator | immutable borrow into report pool | coordinator |
| report pool | report stage | owned by summary operation | report stage |

A job is never simultaneously coordinator-owned and queue-owned. A successful `push` transfers ownership into the queue. A failed push returns `Closed<Job>`, preserving the coordinator’s cleanup and cancellation responsibility.

### Synchronization ledger

| Published fact | Mechanism | Why it is sufficient |
|---|---|---|
| queue item is available | mutex-protected state plus `not_empty` notification | consumer rechecks predicate while holding same mutex |
| queue capacity is available | mutex-protected state plus `not_full` notification | producer rechecks full/closed predicate |
| queue is closed | same mutex state plus notify-all | all blocked operations wake and inspect authoritative state |
| job terminal outcome | ownership transfer through result channel | receiver obtains the complete owned value |
| worker completion/panic | `JoinHandle::join` | coordinator observes thread termination |
| advisory counts | relaxed atomic read-modify-write | no non-atomic state is published through counters |
| report result | Rayon task completion and pool install return | immutable input and reduction laws define meaning |

The cancellation atomic does not publish other memory. It is a prompt to stop avoidable work. `Relaxed` is therefore enough for the flag’s stated role. Queue closure provides the blocking wakeup path.

### Liveness ledger

| Operation that can wait | Predicate or event | Who can advance it | Shutdown wakeup |
|---|---|---|---|
| producer `push` | queue not full or closed | worker pop or queue close | close notifies all producers |
| worker `pop` | queue not empty or closed | producer push or queue close | close notifies all workers |
| result receive loop | next message or all senders dropped | workers send/drop | workers exit and drop senders |
| worker join | worker termination | worker reaches loop end | close makes blocked pop terminate |
| Rayon summary | report tasks finish | report pool threads | no external dependency cycle |

A design is not live merely because each primitive is individually correct. The dependency graph must not contain a cycle in which each participant waits for an event only it could cause.

### Failure ledger

| Failure | Representation | Product response |
|---|---|---|
| malformed manifest | `ManifestError` | no workers are spawned |
| invalid engine bounds | `RunError::InvalidConfiguration` | no workers are spawned |
| thread spawn failure | `RunError::ThreadSpawn` | close queue, join workers already created, return infrastructure error |
| operation domain error | `OutcomeKind::DomainFailed` | continue or close queue under policy |
| operation panic | `OutcomeKind::Panicked` | catch panic, close queue, cancel avoidable work |
| worker panic outside job boundary | `RunError::WorkerPanicked` | join all workers, return infrastructure error |
| duplicate/out-of-range outcome | protocol `RunError` | never silently overwrite or ignore |
| missing terminal slot | `RunError::MissingOutcome` | report incomplete protocol rather than invent success |
| report-pool construction failure | `RunError::ReportPool` | engine work is complete; return infrastructure failure |

Panic containment is deliberately local to the operation call. The worker loop itself remains ordinary code whose unexpected panic is treated as an engine defect.

### Determinism ledger

| Order | May vary? | Product normalization |
|---|---:|---|
| worker selected for a job | yes | not exposed |
| operation start time | yes | not exposed as semantic order |
| completion time | yes | terminal value indexed by manifest position |
| result-channel arrival | yes | slot reconstruction |
| map iteration | no in output | `BTreeMap` keys |
| parallel reduction tree | yes | associative integer-count merge |
| final rows | no | manifest index order |
| exit policy | no | derived from final terminal outcomes |

Deterministic output is constructed at the reconciliation boundary. It is not obtained by forcing workers to execute in order.

### Resource ledger

| Dimension | Bound |
|---|---:|
| manifest jobs | 4,096 |
| identifier bytes | 64 per job |
| payload bytes | 64 KiB per job |
| cumulative payload | 8 MiB |
| worker threads | 1–64 |
| queued jobs | configured 1–4,096 |
| active jobs | at most worker count |
| result messages | at most accepted jobs |
| retained outcomes | exactly accepted jobs after success |
| report threads | 1–64 |
| integer-sort items | 4,096 |
| prime-count limit | 250,000 |

The result channel is primitive-level unbounded. The job-count contract bounds its total sends and retained messages. This is not the same as a streaming memory bound, and the documentation says so.

## 4. Data model

`JobId` validates identity at construction. `Operation` is an enum, not an arbitrary worker function hidden behind dynamic dispatch. Course 7 is about concurrency protocols; the operation set remains deliberately small and statically known so that lifecycle reasoning is not obscured by plugin architecture.

```rust
pub struct Job {
    pub index: usize,
    pub id: JobId,
    pub operation: Operation,
    pub payload: String,
}
```

The index is assigned by the parser and validated again at the engine boundary. That duplication is intentional. Public callers may construct `Job` values without the parser, so `run_jobs` refuses gaps, reordering, and duplicate IDs before spawning threads.

`OutcomeKind` separates product outcomes from engine failures. An invalid integer belongs to one job. An out-of-range result index means the engine protocol itself is broken. Combining both into one string error would make recovery and exit policy ambiguous.

## 5. Manifest parsing before concurrency

The parser completes all structural checks before any worker exists:

- exact `BATCHWEAVE-V1` header;
- exact three-field tab grammar;
- unique validated identifiers;
- supported operation names;
- per-payload and cumulative payload bounds;
- maximum job count;
- stable contiguous indices.

This boundary turns untrusted text into an owned, validated input model. Concurrency begins after parsing, not during it. A streaming parser could reduce retained input but would introduce another lifecycle and backpressure problem. That is a valid future design, not an unacknowledged omission.

## 6. The bounded queue

The queue protects one state value:

```rust
struct State<T> {
    items: VecDeque<T>,
    closed: bool,
}
```

Its invariant is:

```text
items.len() <= capacity
closed never changes from true back to false
successful push occurs only while !closed and len < capacity
pop returns None only when closed && empty
```

A producer waits while the queue is full and open. A consumer waits while it is empty and open. Both use `while`, not `if`, because notifications are not ownership of a queue slot and wakeups may be spurious or stale by the time the mutex is reacquired.

Closing is idempotent and notifies both wait sets. A close must wake producers as well as consumers: under fail-fast policy the coordinator itself may be blocked trying to submit the next job.

The queue recovers poisoned mutex guards with `into_inner`. That is a deliberate product choice. The state invariant is simple and every mutation occurs under the same guard; an unexpected panic while holding the queue lock would still be an engine defect, but poisoning alone does not automatically make the queue unrecoverable. The architecture records outer worker panic separately.

## 7. Worker lifecycle

The coordinator creates a fixed worker set with named threads. It retains every handle. If spawn `k` fails, it closes the queue, drops the coordinator’s sender, joins workers `0..k`, and returns a typed error.

Each worker repeats:

1. pop one owned job;
2. if cancellation is already visible, produce `Cancelled`;
3. otherwise mark advisory `started`;
4. run the pure operation inside `catch_unwind`;
5. classify success, domain failure, or panic;
6. update advisory metrics;
7. trigger fail-fast close when required;
8. send exactly one owned terminal outcome;
9. exit when the queue is closed and empty or the receiver disappears.

`catch_unwind` is not a general recovery guarantee. It prevents an unwind-capable job operation from silently killing the worker and losing ownership of its job. Process abort, foreign unwinding, or violated unsafe invariants remain outside the promise.

The default panic hook may still print a panic message even when the unwind is caught. Product code that requires quiet contained panics would need a carefully scoped reporting policy; changing the global panic hook from worker code would create its own shared-state protocol.

## 8. Cancellation and fail-fast behavior

Cancellation is cooperative. Rust does not provide safe arbitrary thread termination, and BatchWeave does not pretend otherwise.

A domain failure under `--fail-fast`, or any contained job panic, performs two actions:

```text
cancelled.store(true, Relaxed)
queue.close()
```

The atomic flag lets a worker that has just popped a queued job classify it without starting expensive operation work. Queue closure prevents future pushes and wakes blocked threads. A job already executing may finish; the policy does not promise rollback or interruption inside pure operation code.

The coordinator retains jobs returned from a failed push and all not-yet-attempted iterator items. It later creates explicit cancelled outcomes for them. Queued jobs remain queue-owned and are popped by workers, which classify them as cancelled after observing the flag.

This division preserves ownership: no job is copied merely to make cancellation easier, and no job disappears when queue closure races with submission.

## 9. Result protocol and reconciliation

The result channel has one unique receiver and one sender clone per worker. The coordinator drops its original sender immediately after successful spawning. Therefore receiver disconnection means all worker sender clones have been dropped.

Each received outcome is checked before storage:

- index must be within the input range;
- the slot must be empty;
- duplicate results are protocol errors and never overwrite the first result.

The coordinator drains results before joining. In this architecture workers send at most one small bounded result per job and the result channel is not bounded, so a worker cannot block waiting for the coordinator to receive. Joining first would also work with this exact channel, but result-first makes sender disconnection an explicit completion event and prevents later changes to a bounded result channel from introducing a hidden join/send cycle.

After channel closure, the coordinator joins **every** worker and remembers the first outer panic without returning early. It then fills rejected coordinator-owned jobs as cancelled. Any remaining empty slot is an engine error. The product never fabricates a completed or failed outcome to conceal missing worker accounting.

## 10. Advisory atomics

`Metrics` uses `AtomicUsize` with relaxed updates and loads. The counters are:

- submitted;
- started;
- completed;
- failed;
- panicked;
- cancelled.

They are observational. No worker reads them to decide queue state, completion, cancellation, or result authority. No non-atomic memory is published through them. That narrow contract justifies `Relaxed`.

A multi-field snapshot is not globally atomic. A concurrent observer could temporarily see `started < completed` if fields are sampled around updates. The final returned snapshot is taken after joins, but even then it remains instrumentation: the indexed outcomes and derived summary define product truth.

This distinction is the reason the capstone does not use `SeqCst` “to be safe.” Stronger ordering would not make several counters one transaction or turn them into completion evidence.

## 11. Parallel reporting with Rayon

After reconciliation, outcomes are immutable and stable. That makes reporting a separate data-parallel problem.

The parallel summary computes a `PartialSummary` per partition and merges maps by addition. The merge has an identity and is associative over integer counts. Output key order is normalized by `BTreeMap`, so Rayon’s reduction tree does not alter rendered meaning.

A sequential implementation remains available as an oracle. Tests compare parallel output against it across thread counts. Small inputs use the sequential path because parallel scheduling overhead would dominate and because “use parallelism everywhere” is not an engineering requirement.

The report stage constructs a dedicated pool with the configured thread count. It does not rely silently on Rayon’s global pool, which would make resource ownership and interference with other library users less explicit.

## 12. CLI and exit policy

The CLI is intentionally narrow:

```text
batchweave inspect <manifest>
batchweave run <manifest> [--workers N] [--queue-capacity N] [--report-threads N] [--fail-fast]
batchweave demo
```

`inspect` parses and summarizes the manifest without spawning workers. `run` performs the complete lifecycle. `demo` executes a checked-in equivalent manifest in memory.

Exit status `1` means the engine terminated correctly but at least one job did not complete. Exit status `2` means the command itself could not establish or complete the engine contract. This separation is important in scripts: a domain rejection is not the same as malformed input or an infrastructure failure.

## 13. Ten-module build sequence

### Module 61 — Own the jobs and handles

Begin with one thread per bounded job. Move each job into its worker. Keep every `JoinHandle`. Return indexed outcomes and rebuild source order after joining. Do not share mutable output.

**New invariant:** every spawned job has one retained handle and one indexed return path.

### Module 62 — Borrow safely and join completely

Use `thread::scope` for a borrowed inspection path and compare it with the owned worker design. Add complete join accounting: do not return on the first panic while later threads remain unjoined.

**New invariant:** borrowed thread work cannot outlive its source, and all spawned work reaches a documented completion boundary.

### Module 63 — Introduce the queue invariant

Replace one-thread-per-job with a fixed group and a mutex-protected queue state. First implement nonblocking `try_push`/`try_pop` reasoning; then add the blocking layer in Module 64.

**New invariant:** pending jobs never exceed capacity and ownership is unique across coordinator, queue, and worker.

### Module 64 — Add predicate-driven waiting

Add `not_empty` and `not_full` condition variables. Define closed-and-empty termination. Ensure close wakes both producer and consumer waiters.

**New invariant:** every blocking wait is tied to an explicit state predicate and has a shutdown wakeup.

### Module 65 — Make result transfer and backpressure explicit

Send owned `JobOutcome` values to a unique receiver. Document the bounded work queue and the job-count bound on result messages. Drop the coordinator’s sender so disconnect has lifecycle meaning.

**New invariant:** every popped job attempts exactly one terminal result transfer.

### Module 66 — Add failure, panic, cancellation, and recovery

Distinguish domain failure from worker panic and engine failure. Add cooperative cancellation and fail-fast closure. Reconcile unsent jobs. Join all workers on every exit path.

**New invariant:** every accepted job reaches one terminal category under every documented failure policy.

### Module 67 — Add advisory atomic metrics

Record monotonic observations with relaxed atomics. Write down why they do not publish non-atomic state and why they cannot decide completion.

**New invariant:** instrumentation may drift temporarily but cannot change product decisions.

### Module 68 — Audit unsafe alternatives without importing them

Complete the SPSC ring laboratory and write its unsafe proof. Then evaluate whether BatchWeave satisfies the ring’s topology. It does not: the work queue has multiple producers/consumers and requires close plus blocking wakeups. Retain the safe queue.

**New invariant:** unsafe concurrency enters the product only when its topology and benefit are both demonstrated.

### Module 69 — Parallelize the lawful report stage

Keep lifecycle sequentially coordinated. Apply Rayon only to immutable terminal outcomes. Define identity, associativity, and output normalization. Compare with a sequential oracle.

**New invariant:** parallel task partitioning cannot change summary meaning or rendering order.

### Module 70 — Freeze the whole contract

Add full configuration bounds, protocol errors, subprocess tests, deterministic multi-configuration tests, explicit CLI exit semantics, and the six-ledger architecture defense.

**Final invariant:** a successful engine return proves complete worker shutdown, exactly-one terminal outcome per accepted job, and deterministic product output.

## 14. Testing without timing folklore

Concurrency tests should force protocol states rather than hope the scheduler creates them.

### Queue tests

Use a capacity-one queue. Push one item. Start another producer and receive a handshake immediately before its blocking push. Pop the first item, then assert that the second push completes. This proves the full-to-not-full transition without treating a sleep duration as evidence.

For consumer wakeup, start a consumer on an empty queue, close the queue, and assert `None`. For producer cancellation, fill the queue, block a producer, close, and assert the original item is returned in `Closed<T>`.

### Failure tests

Use deterministic operations:

- malformed integer for a domain failure;
- the explicit `panic` operation for contained panic;
- slow bounded prime work to create overlap without using its duration as an assertion;
- capacity-one submission to make close-vs-push ownership observable.

Assertions concern outcome identity, terminal category, total count, and completed joins—not which thread happened to run first.

### Determinism tests

Run the same manifest with configurations such as:

```text
workers=1 queue=1 report_threads=1
workers=2 queue=1 report_threads=2
workers=4 queue=3 report_threads=3
```

Compare the complete rendered report under `Continue` policy. This does not prove every possible schedule, but it checks the normalization boundary while the underlying invariant and design explain why the result should be stable.

Do **not** demand cross-configuration equality from fail-fast execution. Once cancellation begins, work that was already running may complete while work that had not started becomes cancelled; that frontier is schedule-dependent by contract. Fail-fast still guarantees one terminal row per source index, stable source-order rendering, bounded shutdown, and authoritative counts. This distinction prevents “deterministic output” from becoming a false claim that the scheduler cannot affect which avoidable jobs had already begun.

### Hang containment

A subprocess-level harness may impose a generous timeout to keep continuous integration from hanging forever. The timeout is a containment mechanism, not the proof. The test should still use handshakes or final-state assertions to identify the protocol condition that failed.

## 15. Weak designs and why they fail

### One mutex around the whole engine

This can prevent data races but serializes operation execution, queue management, result storage, and rendering. More importantly, it hides the ownership-transfer structure and encourages holding a guard across expensive work.

### Unbounded work channel

This removes producer blocking at the cost of admitting arbitrary queued work. For a finite checked manifest the total is still bounded, but the product’s backpressure lesson and future streaming extension become dishonest.

### Detached workers

Dropping handles makes shutdown, panic, resource release, and process exit timing ambiguous. A finite CLI engine has no reason to detach.

### Shared output vector under a mutex

Workers can push results into one vector, but arrival order becomes output order unless a later sort reconstructs identity. Sending owned outcomes to one coordinator keeps output mutation single-owner and result protocol explicit.

### `SeqCst` everywhere

Sequential consistency does not fix missing terminal outcomes, deadlocks, unbounded queues, or multi-counter snapshots. Use ordering derived from the actual publication relation. Here the counters need no publication relation.

### Lock-free queue by default

A lock-free MPMC queue with blocking shutdown and reclamation is much harder to prove than this product requires. The independent SPSC lab teaches the proof boundary; the capstone demonstrates the maturity to decline unnecessary unsafe complexity.

### Rayon for the worker service

Rayon is excellent for finite fork-join CPU work. BatchWeave needs an explicit bounded submission queue, fail-fast close, per-job panic classification, and lifecycle visibility. Using Rayon for report reduction is a better fit than hiding the service protocol inside a parallel iterator.

## 16. Independent extension — bounded retry

Add this requirement without copying a prepared implementation:

> A domain-failed job may be retried up to `R` times when its operation class is declared retryable. Final output still contains one row per manifest job. Metrics distinguish attempts from terminal jobs. Fail-fast applies only after retries are exhausted.

Before editing code, answer:

1. Does one job now produce several channel messages or one terminal message?
2. Who owns the payload between attempts?
3. Is retry immediate in the same worker or resubmitted through the queue?
4. Can resubmission deadlock when every worker tries to push into a full queue?
5. Does queue capacity count jobs or attempts?
6. How does cancellation interact with a pending retry?
7. Which operations are idempotent, and does retry require idempotence here?
8. What deterministic rule records intermediate diagnostics?
9. Which metrics are per-attempt and which are per-job?
10. Does the memory bound change?

A strong design may keep retries inside the worker to avoid worker-to-queue cycles, but it must bound attempt time and preserve cancellation checkpoints. Another valid design can give retry scheduling back to a unique coordinator. What is not acceptable is letting every worker recursively submit to the same bounded queue without a liveness proof.

## 17. Completion standard

The capstone is complete when you can establish all of these claims from code and tests:

- parsing validates structure and resource bounds before spawning;
- every worker thread has a retained handle;
- every handle is joined on every ordinary return path;
- work queue length never exceeds configured capacity;
- queue close wakes blocked producers and consumers;
- every accepted job has exactly one final outcome;
- duplicate, missing, and out-of-range outcomes are not hidden;
- panic is classified at the job boundary;
- fail-fast stops avoidable new work without pretending to kill threads;
- final output is independent of legal worker completion order;
- relaxed metrics are observational only;
- Rayon reduction preserves a sequentially specified meaning;
- resource bounds and excluded guarantees are documented honestly;
- the SPSC unsafe abstraction remains outside the product because its topology does not fit;
- CLI exit statuses distinguish product rejection from engine failure.

The final defense should begin with invariants and state transitions, not with `Arc`, `Mutex`, channels, atomics, or Rayon. Those are implementation mechanisms. The product contract is the reason they are present.

[Return to the course overview](index.md) · [Open the implementation](../capstone/README.md) · [Begin the final review](final-review.md)
