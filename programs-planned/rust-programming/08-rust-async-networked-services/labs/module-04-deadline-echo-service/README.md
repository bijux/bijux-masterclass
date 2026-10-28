# Laboratory 74 — Deadline Echo Service

This is the independent product for **Course 8, Module 74**. Read the [module chapter](../../course-book/module-74-tcp-udp-dns-and-connection-lifecycles/index.md) and complete its [workbook](../../course-book/module-74-tcp-udp-dns-and-connection-lifecycles/workbook.md) before consulting the reference implementation.

## Learning target

> How can a TCP service bound accepted connections, own every connection task, classify EOF, and terminate idle clients and shutdown without leaking permits?

The completed product must make the answer visible in its types, lifecycle, tests, failure behavior, and explanation. A successful happy-path run is not sufficient.

## Product

Build a loopback echo service for bounded byte chunks. It accepts at most a configured number of connections, tracks all tasks, applies idle and write-stall timeouts, and performs stop-admission, signal, drain, abort, and join shutdown.

## Why this laboratory exists

The lab isolates transport lifecycle before command protocol. It demonstrates that backlog, accepted sockets, tasks, deadlines, and half-close are distinct concerns.

## Contract

At most 16 connections are admitted. Each connection owns one permit. A zero-byte read is clean peer EOF. Any read bytes are written fully under a write deadline. Shutdown stops accept, signals children, drains for a finite grace, aborts leftovers, and joins the task set.

## Required milestones

1. Bind an ephemeral listener and expose its address.
2. Acquire capacity before spawning connection work.
3. Implement idle read and write-stall deadlines.
4. Track all connection tasks.
5. Implement bounded shutdown and lifecycle tests.

## Adversarial cases

- zero connections
- maximum admitted clients
- one extra blocked client
- peer half-close
- idle client
- slow/nonreading client
- shutdown with idle clients
- accept error path

## Evidence to produce

- a connection ledger
- permit-count assertions
- tests using explicit gates or paused time
- proof that every connection task is joined
- an explicit statement that echo chunks are not messages

## Prohibited shortcuts

- one task per accept without a permit
- detaching connection handles
- treating EOF as retryable no-data
- resetting an overall shutdown budget per task
- using a sleep as the only lifecycle oracle

## Transfer

Transfer the lifecycle to a chat transport with split read and write halves. Define the single connection owner and bounded outbound queue.

## Comparing with the reference

Compare permit ownership, task joins, and shutdown first. A shorter accept loop that leaks detached tasks is not equivalent.

The `solution/` directory is a reference after independent work, not a sequence of blanks to copy. Compare invariants, task ownership, cancellation behavior, bounds, and tests before comparing line count.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Begin in `starter/`. Do not open `solution/` until the state diagram, failure cases, and transfer design are written or a precise blocker is recorded.

The laboratory is complete when its tests pass and you can answer the governing question without the chapter:

> How can a TCP service bound accepted connections, own every connection task, classify EOF, and terminate idle clients and shutdown without leaking permits?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```
