# BatchWeave

BatchWeave is the cumulative product for **Rust Concurrency and Parallelism**. It runs a bounded manifest of CPU-oriented jobs through a fixed worker group, records one terminal outcome for every accepted input row, and renders the final report in manifest order rather than completion order.

It exists to make concurrent product obligations visible. The interesting part is not that several threads run. The interesting part is that ownership, capacity, shutdown, failure, panic, visibility, ordering, and reporting all have explicit contracts.

## Commands

```text
batchweave inspect <manifest>
batchweave run <manifest> [--workers N] [--queue-capacity N] [--report-threads N] [--fail-fast]
batchweave demo
batchweave help
batchweave version
```

The exit status is:

```text
0  the command succeeded and every job completed
1  execution terminated cleanly but at least one job failed, panicked, or was cancelled
2  usage, input, configuration, or infrastructure failure
```

## Manifest format

```text
BATCHWEAVE-V1
# id<TAB>operation<TAB>payload
checksum-readme	checksum	reader-first concurrency
count-words	word-count	one two three four
sort-values	sort-integers	9,-4,7,0
count-primes	prime-count	100
```

Blank lines and lines beginning with `#` are ignored after the header. Job identifiers must be unique. A job receives a stable zero-based index from its accepted manifest order.

Supported operations:

| Operation | Result |
|---|---|
| `checksum` | FNV-1a checksum rendered as sixteen hexadecimal digits |
| `word-count` | Unicode-whitespace token count |
| `sort-integers` | comma-separated signed integers in ascending order |
| `prime-count` | number of primes at or below the supplied bounded integer |
| `panic` | injected panic used to prove panic containment and cancellation |

The checksum is a deterministic course operation, not a cryptographic integrity mechanism.

## Concurrency contract

BatchWeave promises:

- a fixed number of worker threads;
- a bounded blocking work queue;
- explicit queue closure and wakeup;
- complete worker joining before return;
- panic containment around each job operation;
- one indexed terminal outcome per accepted manifest job;
- typed distinction among completion, domain failure, panic, and cancellation;
- deterministic final ordering independent of worker schedule;
- a separately owned Rayon pool for parallel report aggregation;
- atomic live counters that are advisory rather than authoritative.

BatchWeave does **not** promise:

- fair operating-system scheduling;
- deterministic completion order;
- hard real-time deadlines;
- lock-free work distribution;
- an absolute process-memory ceiling;
- immunity from process abort or machine failure;
- optimal throughput on every workload.

## Resource bounds

The product limits manifest jobs, identifier bytes, per-job payload bytes, cumulative payload bytes, worker count, queue capacity, report threads, integer-list length, and prime-count input. The standard result channel is unbounded at the primitive level, but the manifest job limit bounds the maximum number of result messages and retained terminal outcomes.

The queue capacity limits waiting jobs, not the entire process. Active jobs, final outcomes, input text, and report text are separate accumulating dimensions and are documented separately in the engineering guide.

## Failure policy

`--continue` is the default. A domain failure records a failed outcome and allows unrelated jobs to continue.

`--fail-fast` closes the work queue after the first domain failure. A caught worker panic closes the queue under either policy. Closing the queue:

1. wakes blocked producers and consumers;
2. prevents later submission;
3. leaves already queued jobs available for workers to classify as cancelled;
4. permits the worker group to reach closed-and-empty termination;
5. lets the coordinator join every worker before reporting.

Fail-fast means “stop starting avoidable new work,” not “erase work already executing” and not “kill threads.”

## Determinism contract

Worker assignment, completion order, result-channel arrival, and Rayon partitioning may vary. Under continue policy, the complete logical report remains stable because every job owns a manifest index and the coordinator stores each outcome in that index’s slot. Summaries use ordered maps. The sequential report implementation remains the semantic oracle for the parallel reducer.

Fail-fast makes a narrower promise. The report order and exactly-once accounting are deterministic, but the frontier between an already-running completion and a cancellation can vary with the schedule. The product does not pretend that cooperative cancellation can retroactively stop pure work that has already begun.

Live atomic metrics can describe observations such as submitted or started work, but they do not determine completion. The indexed outcome vector is authoritative.

## Run the product

```bash
cargo run -- inspect examples/demo.batchweave
cargo run -- run examples/demo.batchweave --workers 4 --queue-capacity 2 --report-threads 2
cargo run -- demo
```

Run all tests and static checks from the course root:

```bash
make proof
```

## Read before modifying

The complete design, proof obligations, stage-by-stage build, testing strategy, and unseen extension exercise are in [`course-book/capstone.md`](../course-book/capstone.md).
