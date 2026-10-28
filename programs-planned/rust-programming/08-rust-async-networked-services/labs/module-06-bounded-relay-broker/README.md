# Laboratory 76 — Bounded Relay Broker

This is the independent product for **Course 8, Module 76**. Read the [module chapter](../../course-book/module-76-backpressure-admission-control-and-fair-work-distribution/index.md) and complete its [workbook](../../course-book/module-76-backpressure-admission-control-and-fair-work-distribution/workbook.md) before consulting the reference implementation.

## Learning target

> How can an async broker bound queued and active work, remain responsive to control messages, and give every accepted request one terminal outcome?

The completed product must make the answer visible in its types, lifecycle, tests, failure behavior, and explanation. A successful happy-path run is not sufficient.

## Product

Build an actor-owned relay broker. Callers submit indexed integer work through a bounded mailbox and receive a terminal reply through `oneshot`. The broker keeps a bounded FIFO waiting queue, starts at most a configured number of jobs, answers snapshots while jobs run, and rejects overload before commitment.

## Why this laboratory exists

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

> How can an async broker bound queued and active work, remain responsive to control messages, and give every accepted request one terminal outcome?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```
