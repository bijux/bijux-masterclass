# Module 70 — Integrated Concurrent Architecture, Testing, and Audit

**Course 7 · Day 10 · Module 70 of 100**
`██████████████████░░░░░░░` **70/100**

[Program](../../../README.md) · [Course 7](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-10-concurrent-verifier/README.md) · [BatchWeave guide](../capstone.md)

[← Module 69: Rayon, Work Stealing, and Deterministic Parallelism](../module-69-rayon-work-stealing-and-deterministic-parallelism/index.md) · [Module 71: Futures, Polling, Wakers, and Async State Machines →](../../../08-rust-async-networked-services/course-book/module-71-futures-polling-wakers-and-async-state-machines/index.md)

## The question

> How do ownership, bounded work, synchronization, liveness, panic, cancellation, atomics, deterministic reporting, and test evidence become one product whose strongest claims are reviewable?

## Why this comes now

The previous nine modules each isolated one proof technique. Production defects appear where those techniques meet: a bounded send under a lock, cancellation that sets a flag but does not wake a queue, live metrics mistaken for final truth, a panic that drops a result sender, a parallel report whose reduction changes order, or a lock-free component inserted without matching topology.

The final module builds an architecture review method and completes BatchWeave. It introduces no new primitive. Its standard is independent transfer: given a new cross-cutting requirement, you must update all affected ledgers, code paths, tests, resource bounds, and claims without weakening earlier contracts.

This module is not complete when you can name the primitive. It is complete when you can state the ownership transfer, the synchronization edge, the progress argument, the failure behavior, and the schedule-dependent facts that remain intentionally unspecified.

### Prerequisite bridge

Module 69 established **Rayon, Work Stealing, and Deterministic Parallelism**. Before continuing, verify that you can choose task granularity, custom pool size, and sequential cutoffs from a cost hypothesis that course 9 can measure. This module preserves that capability and adds the ability to construct one architecture diagram connecting coordinator, queue, workers, result channel, metrics, report pool, and cli boundaries;. Module 71, **Futures, Polling, Wakers, and Async State Machines**, will rely on both when it asks: *What exactly is an async computation before a runtime executes it, what must happen when it cannot complete, and what state remains when it is suspended or cancelled?*

### Scope boundary

This module owns the reasoning for **integrated concurrent architecture, testing, and audit** inside Course 7. The course uses operating-system threads and Rayon. Async runtimes, sockets, network protocols, and async cancellation remain Course 8 topics. Lock-free code is taught as a proof exercise, not as a default replacement for locks and channels. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- construct one architecture diagram connecting coordinator, queue, workers, result channel, metrics, report pool, and CLI boundaries;
- maintain ownership, synchronization, liveness, failure, determinism, and resource ledgers together;
- prove boundedness for jobs, payloads, queue slots, workers, result messages, report threads, and output storage;
- derive exactly one terminal outcome per manifest job under success, domain failure, panic, cancellation, and submission interruption;
- separate live advisory metrics from authoritative post-join summaries;
- design deterministic output over nondeterministic execution;
- build causal tests for blocked operations, cancellation, panic, and ordering without schedule sleeps;
- state portability, fairness, performance, and lock-free claims at their strongest honest level.

## Core model

### One architecture, six ledgers

A concurrent design review should keep six synchronized artifacts:

1. **ownership ledger:** who owns jobs, endpoints, handles, pools, and cleanup;
2. **synchronization ledger:** which lock, channel, atomic, or join publishes each fact;
3. **liveness ledger:** what each operation can wait for and what wakes or terminates it;
4. **failure ledger:** domain errors, panic, poison, disconnect, cancellation, and infrastructure faults;
5. **determinism ledger:** which orders may vary and which outputs are normalized;
6. **resource ledger:** maxima for input, queue, active work, threads, messages, and allocation.

A code change is incomplete until affected rows change. This is not internal bureaucracy; it is a main explanation of the product’s concurrency contract.

### BatchWeave topology

The final product has these components:

```text
manifest parser ──owned indexed jobs──▶ coordinator
                                      │
                                      ▼
                              bounded MPMC queue
                              ▲               │
                         close/wake           ▼
                                      fixed worker group
                                      │ typed indexed outcomes
                                      ▼
                              result receiver
                                      │
                                      ▼
                         deterministic reconciliation
                                      │ immutable outcomes
                                      ▼
                          Rayon report pool → rendering
```

The coordinator owns submission, queue closure, result assembly, worker handles, and final return. Workers own only one popped job at a time. Queue closure is shared lifecycle state. The result receiver is unique. Rayon sees only complete immutable outcomes.

### Bound every accumulating dimension

A bounded queue alone does not bound the product. State:

- maximum manifest jobs;
- maximum job ID and payload bytes;
- worker count range;
- queue capacity range;
- maximum active jobs equals workers;
- result message count at most accepted jobs;
- outcome payload/error length limits;
- report-pool thread count;
- final output size or truncation policy.

The standard result channel is unbounded, but accepted job count bounds total sends. That is an honest product-level bound. A hostile job cannot emit arbitrary output because operations return bounded summaries.

### Exactly-one outcome is the central invariant

For every manifest index `i`, final reconciliation yields exactly one:

```text
Completed | DomainFailed | Panicked | Cancelled
```

Worker events may arrive at most once for a popped job. The coordinator rejects duplicates and out-of-range indices. Jobs rejected by a closed push remain coordinator-owned and become cancelled. Jobs queued during cancellation are popped and labelled cancelled or remain missing until reconciliation labels them. A worker infrastructure fault cannot silently convert missing jobs to success.

The final vector—not channel length or metrics—is the authoritative run record.

### Shutdown order breaks dependency cycles

A robust fail-fast sequence is:

1. a worker observes domain failure or panic;
2. it records the job outcome;
3. cancellation state becomes true;
4. queue close wakes blocked submitter and workers;
5. coordinator stops submission and retains any unsent job;
6. queued jobs drain into cancelled outcomes;
7. workers exit at closed-empty;
8. all result senders drop;
9. receiver reaches disconnect;
10. coordinator joins every handle;
11. missing indices are reconciled;
12. reporting begins.

The exact implementation may interleave steps, but no operation waits on a component that only it can advance.

### Metrics never decide truth

Relaxed atomics can report submitted, started, completed, failed, panicked, and cancelled counts while work runs. Their snapshot may be temporarily inconsistent across fields. They are useful for observation, not for deciding whether all work finished.

After result-channel termination and joins, BatchWeave scans the indexed outcome vector to compute authoritative counts. Tests assert that final counts equal this scan even if live metrics were sampled at awkward moments.

### Determinism is constructed at boundaries

BatchWeave allows:

- worker assignment to vary;
- job completion order to vary;
- result message arrival to vary;
- Rayon task and reduction order to vary when laws preserve meaning.

It stabilizes:

- source index and job identity;
- one terminal slot per job;
- diagnostic ordering by index and category;
- report keys through ordered maps;
- CLI rendering and exit policy.

This is stronger and cheaper than forcing a deterministic schedule.

### Test protocols, not probability

The test suite uses:

- barriers to start contenders together;
- handshake channels to prove a producer/consumer reached a blocking operation;
- capacity-one queues to force backpressure;
- injected operations that return errors or panic;
- deterministic work gates rather than arbitrary sleep;
- sequential report oracles;
- repeated runs with varied worker/queue/report thread counts;
- subprocess tests for CLI and potential hangs.

A short harness timeout may prevent indefinite CI hangs, but assertions rely on causal events and final invariants.

### Separate correctness from performance

The course can claim bounded topology, data-race freedom in safe components, a documented unsafe SPSC proof, deterministic final output, and termination under stated assumptions. It cannot yet claim optimal throughput, fair scheduling, absence of starvation under every platform policy, or benchmark superiority. Course 9 measures allocations, contention, cache behavior, and scaling.

Rayon 1.12.0 and Rust 1.97.1 are pinned for reproducibility. Pinning does not freeze operating-system scheduling or hardware memory hierarchy.

### Review changes by invariant impact

When asked to add priorities, retries, deadlines, streaming input, or partial reports, do not patch one file. Ask:

- Does ownership change?
- Does queue capacity or fairness change?
- Can one job now produce several events?
- Does cancellation need another checkpoint?
- Does deterministic order change?
- Does the result bound change?
- Do atomic metrics acquire product meaning?
- Can a worker retain state after panic?

The final assessment gives an unseen feature and scores the completeness of this impact analysis before code style.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For construct one architecture diagram connecting coordinator, queue, workers, result channel, metrics, report pool, and CLI boundaries, construct one positive and one causal negative example. Mark the first decisive fact in the **concurrent architecture dossier** and state which evidence could falsify the claim.

2. **Outcome 2.** For maintain ownership, synchronization, liveness, failure, determinism, and resource ledgers together, construct one positive and one causal negative example. Mark the first decisive fact in the **concurrent architecture dossier** and state which evidence could falsify the claim.

3. **Outcome 3.** For prove boundedness for jobs, payloads, queue slots, workers, result messages, report threads, and output storage, construct one positive and one causal negative example. Mark the first decisive fact in the **concurrent architecture dossier** and state which evidence could falsify the claim.

4. **Outcome 4.** For derive exactly one terminal outcome per manifest job under success, domain failure, panic, cancellation, and submission interruption, construct one positive and one causal negative example. Mark the first decisive fact in the **concurrent architecture dossier** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

The final report should be derived from authoritative outcomes, not from execution timing or live counters:

```rust
use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum OutcomeKind {
    Completed(String),
    DomainFailed(String),
    Panicked,
    Cancelled,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct JobOutcome {
    pub index: usize,
    pub id: String,
    pub operation: String,
    pub kind: OutcomeKind,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FinalSummary {
    pub total: usize,
    pub by_status: BTreeMap<&'static str, usize>,
    pub by_operation: BTreeMap<String, usize>,
}

pub fn summarize(outcomes: &[JobOutcome]) -> FinalSummary {
    let mut by_status = BTreeMap::new();
    let mut by_operation = BTreeMap::new();

    for outcome in outcomes {
        let status = match &outcome.kind {
            OutcomeKind::Completed(_) => "completed",
            OutcomeKind::DomainFailed(_) => "failed",
            OutcomeKind::Panicked => "panicked",
            OutcomeKind::Cancelled => "cancelled",
        };
        *by_status.entry(status).or_default() += 1;
        *by_operation.entry(outcome.operation.clone()).or_default() += 1;
    }

    FinalSummary {
        total: outcomes.len(),
        by_status,
        by_operation,
    }
}
```

The production implementation may compute the maps with Rayon, but the sequential function remains the oracle. Ordered maps make rendering stable. Outcome indices are validated and ordered before this stage, so summary order is unrelated to worker schedule.

A final run result should also include live metrics for observability, but the API labels them separately. If a live counter disagrees with the authoritative summary because a send failed after increment, the summary wins and the discrepancy can be recorded as instrumentation drift.

The full capstone code keeps operation functions pure and bounded. The CLI maps accepted/rejected runs to explicit exit codes only after complete shutdown; it never exits while workers remain unjoined.

## Practice sequence

1. Build all six ledgers for BatchWeave from a blank page.
2. Trace success, fail-fast, explicit cancellation, and worker panic end to end.
3. Prove exactly-one terminal outcome for every manifest index.
4. Audit every accumulating resource dimension.
5. Derive deterministic rendering from nondeterministic events.
6. Replace sleep-based tests with causal coordination.
7. Complete Concurrent Verifier, then defend BatchWeave under an unseen change.

The corresponding independent product is [Concurrent Verifier](../../labs/module-10-concurrent-verifier/README.md). The same reasoning then changes one explicit invariant in [BatchWeave](../capstone.md).

## Ready to continue

Continue only when you can do all of the following without using the chapter as a script:

- explain the whole engine without naming primitives before invariants;
- prove shutdown under all documented failure paths;
- show where every job becomes one terminal outcome;
- separate live metrics from final authority;
- state exactly which performance and fairness claims remain unproved.

## Primary Rust references

- [`std::sync`](https://doc.rust-lang.org/std/sync/index.html)
- [`std::thread`](https://doc.rust-lang.org/std/thread/)
- [`std::sync::atomic`](https://doc.rust-lang.org/std/sync/atomic/)
- [Rayon 1.12.0](https://docs.rs/rayon/1.12.0/rayon/)
- [Rustonomicon: concurrency](https://doc.rust-lang.org/nomicon/concurrency.html)

The course book is self-contained. These references are for checking the exact library contract and following changes in the language or standard library; they are not substitutes for the reasoning developed above.

## Continue

Continue to [Module 71 — Futures, Polling, Wakers, and Async State Machines](../../../08-rust-async-networked-services/course-book/module-71-futures-polling-wakers-and-async-state-machines/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
