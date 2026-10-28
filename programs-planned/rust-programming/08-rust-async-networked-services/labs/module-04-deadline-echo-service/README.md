# Laboratory 74 — Deadline Echo Service

**Course 8 · Module 74: TCP, UDP, DNS, and Connection Lifecycles**

[Chapter](../../course-book/module-74-tcp-udp-dns-and-connection-lifecycles/index.md) · [Workbook](../../course-book/module-74-tcp-udp-dns-and-connection-lifecycles/workbook.md) · [JobWire guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **TCP, UDP, DNS, and Connection Lifecycles**: What lifecycle does each network transport actually provide, and where should connection admission, name resolution, deadlines, half-close, datagram loss, and peer identity be represented? The product must make **Distinguish bind, listen, accept, connect, resolve, read, write, half-close, and full close** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **connection lifecycle map** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

> How can a TCP service bound accepted connections, own every connection task, classify EOF, and terminate idle clients and shutdown without leaking permits?

The completed product must make the answer visible in its types, lifecycle, tests, failure behavior, and explanation. A successful happy-path run is not sufficient.

## Product

Build a loopback echo service for bounded byte chunks. It accepts at most a configured number of connections, tracks all tasks, applies idle and write-stall timeouts, and performs stop-admission, signal, drain, abort, and join shutdown.

## Product-specific design pressure

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

For **Laboratory 74 — Deadline Echo Service**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Working route

1. Read the product contract and run the starter’s baseline checks for **Deadline Echo Service**.
2. Draw the smallest **connection lifecycle map** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to JobWire so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Distinguish bind, listen, accept, connect, resolve, read, write, half-close, and full close.
- Acquire connection admission before spawning unbounded tasks.
- Explain the limits of socket backlog as application backpressure.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 74 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **connection lifecycle map**. Defend why your design is simpler than one plausible alternative under the new requirements.
