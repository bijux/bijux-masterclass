# Laboratory 78 — Hyper Health Surface

**Course 8 · Module 78: HTTP Services with Hyper: Requests, Bodies, and Connections**

[Chapter](../../course-book/module-78-http-services-with-hyper-requests-bodies-and-connections/index.md) · [Workbook](../../course-book/module-78-http-services-with-hyper-requests-bodies-and-connections/workbook.md) · [JobWire guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **HTTP Services with Hyper: Requests, Bodies, and Connections**: How do you build a small HTTP service while keeping transport ownership, HTTP connection driving, request-body policy, routing, application state, and health semantics separate? The product must make **Distinguish accepted transport, HTTP connection future, request future, body stream, and application service** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **HTTP boundary map** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

> How can a small Hyper service expose honest operational state without hiding body limits, connection ownership, or shutdown behind framework defaults?

The completed product must make the answer visible in its types, lifecycle, tests, failure behavior, and explanation. A successful happy-path run is not sufficient.

## Product

Build an HTTP/1 service with `GET /health` and `GET /stats`. Routing is testable without sockets. Request bodies are bounded and must be empty. Connection admission is bounded, connection futures are tracked, and shutdown drains or aborts keep-alive clients.

## Product-specific design pressure

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

For **Laboratory 78 — Hyper Health Surface**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Working route

1. Read the product contract and run the starter’s baseline checks for **Hyper Health Surface**.
2. Draw the smallest **HTTP boundary map** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to JobWire so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Distinguish accepted transport, HTTP connection future, request future, body stream, and application service.
- Serve HTTP/1 connections with Hyper over Tokio I/O.
- Construct stable response body types and status codes.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 78 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **HTTP boundary map**. Defend why your design is simpler than one plausible alternative under the new requirements.
