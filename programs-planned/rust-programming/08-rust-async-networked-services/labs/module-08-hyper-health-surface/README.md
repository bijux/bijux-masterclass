# Laboratory 78 — Hyper Health Surface

This is the independent product for **Course 8, Module 78**. Read the [module chapter](../../course-book/module-78-http-services-with-hyper-requests-bodies-and-connections/index.md) and complete its [workbook](../../course-book/module-78-http-services-with-hyper-requests-bodies-and-connections/workbook.md) before consulting the reference implementation.

## Learning target

> How can a small Hyper service expose honest operational state without hiding body limits, connection ownership, or shutdown behind framework defaults?

The completed product must make the answer visible in its types, lifecycle, tests, failure behavior, and explanation. A successful happy-path run is not sufficient.

## Product

Build an HTTP/1 service with `GET /health` and `GET /stats`. Routing is testable without sockets. Request bodies are bounded and must be empty. Connection admission is bounded, connection futures are tracked, and shutdown drains or aborts keep-alive clients.

## Why this laboratory exists

The lab isolates a standard HTTP surface from the custom JobWire protocol. It teaches which responsibilities Hyper owns and which remain application policy.

## Contract

Health reports `starting`, `ready`, `shutting-down`, or `failed` from a snapshot. Stats use deterministic plain text. Unknown routes return 404, wrong methods 405, nonempty bodies 400, and bodies above the inspection maximum 413. No route waits behind a work queue.

## Required milestones

1. Define the status snapshot and stable rendering.
2. Implement pure method/path routing.
3. Enforce body policy.
4. Drive HTTP/1 over Tokio I/O.
5. Track connections and implement shutdown.

## Adversarial cases

- ready and nonready health
- wrong method
- unknown route
- one-byte body
- oversized body
- slow keep-alive client
- shutdown with active connection
- saturated connection admission

## Evidence to produce

- pure route tests
- exact status/content type/body tests
- a written health-semantics statement
- connection task ledger
- proof no application lock survives response return

## Prohibited shortcuts

- collecting an unbounded body
- debug-formatted public state
- health through the saturated work queue
- detached Hyper connection futures
- holding application permits through network drain

## Transfer

Transfer the surface to a readiness endpoint that depends on two downstream snapshots. Define stale, unknown, degraded, and failed states.

## Comparing with the reference

Compare semantic honesty before HTTP syntax. A reference that returns 200 for every state or ignores body limits is weaker.

The `solution/` directory is a reference after independent work, not a sequence of blanks to copy. Compare invariants, task ownership, cancellation behavior, bounds, and tests before comparing line count.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Begin in `starter/`. Do not open `solution/` until the state diagram, failure cases, and transfer design are written or a precise blocker is recorded.

The laboratory is complete when its tests pass and you can answer the governing question without the chapter:

> How can a small Hyper service expose honest operational state without hiding body limits, connection ownership, or shutdown behind framework defaults?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```
