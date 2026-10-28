# Laboratory 76 — Bounded Relay Broker

**Course 8 · Module 76: Backpressure, Admission Control, and Fair Work Distribution**

[Chapter](../../course-book/module-76-backpressure-admission-control-and-fair-work-distribution/index.md) · [Workbook](../../course-book/module-76-backpressure-admission-control-and-fair-work-distribution/workbook.md) · [JobWire guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Backpressure, Admission Control, and Fair Work Distribution**: When demand exceeds service capacity, where may work wait, which bound is authoritative, and how does overload become an explicit product outcome instead of memory growth, latency collapse, or starvation? The product must make **Find every accumulation point in an async service** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **capacity and admission ledger** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

> How can an async broker bound queued and active work, remain responsive to control messages, and give every accepted request one terminal outcome?

The completed product must make the answer visible in its types, lifecycle, tests, failure behavior, and explanation. A successful happy-path run is not sufficient.

## Product

Build an actor-owned relay broker. Callers submit indexed integer work through a bounded mailbox and receive a terminal reply through `oneshot`. The broker keeps a bounded FIFO waiting queue, starts at most a configured number of jobs, answers snapshots while jobs run, and rejects overload before commitment.

## Product-specific design pressure

The lab isolates end-to-end capacity from sockets and protocol parsing. It demonstrates that mailbox capacity, committed waiting work, active jobs, reply waiters, and slow consumers are separate resources.

## Contract

The mailbox, waiting queue, and active-job count are independently bounded. A request commits only when entered into the broker-owned queue or active set. Overload before commit returns `Busy`. Job permits release before a slow reply receiver can affect execution capacity. Shutdown rejects queued work and drains active tasks.

## Required milestones

1. Define request, reply, snapshot, and limits.
2. Implement one actor as state authority.
3. Keep waiting jobs in one bounded structure.
4. Run active jobs in a tracked set.
5. Add saturation, snapshot, slow-receiver, and shutdown tests.

## Adversarial cases

- zero capacity rejected
- exact queue boundary
- one request beyond capacity
- snapshot while all workers busy
- reply receiver dropped
- job domain failure
- broker cancellation with queued and active work

## Evidence to produce

- a complete capacity ledger
- exact accepted/queued/active counts
- proof that no waiting task is spawned per request
- one terminal outcome per committed request
- a test proving slow replies release active capacity

## Prohibited shortcuts

- unbounded mpsc
- task per waiting request
- holding active capacity while sending a reply
- blocking the broker receive loop on job completion
- returning no reply for cancelled queued work

## Transfer

Transfer the broker to two job classes with separate queue limits and one shared worker budget. Define fairness and starvation behavior.

## Comparing with the reference

Compare where waiting work lives and when commitment occurs. A reference with a bounded channel but unbounded spawned waiters is weaker.

The `solution/` directory is a reference after independent work, not a sequence of blanks to copy. Compare invariants, task ownership, cancellation behavior, bounds, and tests before comparing line count.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Begin in `starter/`. Do not open `solution/` until the state diagram, failure cases, and transfer design are written or a precise blocker is recorded.

The laboratory is complete when its tests pass and you can answer the governing question without the chapter:

For **Laboratory 76 — Bounded Relay Broker**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Working route

1. Read the product contract and run the starter’s baseline checks for **Bounded Relay Broker**.
2. Draw the smallest **capacity and admission ledger** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to JobWire so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Find every accumulation point in an async service.
- Distinguish connection admission, queue capacity, active-work permits, response buffering, and retry budgets.
- Choose between waiting, rejecting, shedding, degrading, and disconnecting under overload.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 76 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **capacity and admission ledger**. Defend why your design is simpler than one plausible alternative under the new requirements.
