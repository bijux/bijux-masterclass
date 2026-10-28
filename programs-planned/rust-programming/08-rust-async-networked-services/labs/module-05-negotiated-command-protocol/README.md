# Laboratory 75 — Negotiated Command Protocol

This is the independent product for **Course 8, Module 75**. Read the [module chapter](../../course-book/module-75-protocol-state-machines-versioning-and-defensive-parsing/index.md) and complete its [workbook](../../course-book/module-75-protocol-state-machines-versioning-and-defensive-parsing/workbook.md) before consulting the reference implementation.

## Learning target

> How can a frame payload become a typed message whose legality, response, and next state are exhaustive and versioned?

The completed product must make the answer visible in its types, lifecycle, tests, failure behavior, and explanation. A successful happy-path run is not sufficient.

## Product

Build a pure negotiated protocol with `HELLO`, `PING`, `ECHO`, and `QUIT`. Parsing, semantic validation, transition, and rendering are separate. Version 1 is the only supported version and every state/message pair has a defined outcome.

## Why this laboratory exists

The lab removes sockets and brokers so protocol reasoning cannot hide behind transport code. It tests grammar, correlation, state, error scope, and canonical rendering directly.

## Contract

Payloads are UTF-8 and tab separated. `HELLO 1` is required first. Request IDs follow a bounded ASCII policy. `PING` and `ECHO` are legal only in Ready state. Repeated negotiation is fatal. Domain-valid unknown commands produce a stable error according to the declared close policy.

## Required milestones

1. Write the grammar and field bounds.
2. Implement pure parse and render.
3. Implement a total state transition function.
4. Define stable public errors and close policy.
5. Test every state/message combination and round trip.

## Adversarial cases

- empty payload
- invalid UTF-8
- unsupported version
- command before HELLO
- repeated HELLO
- invalid request ID
- unknown command
- QUIT followed by another message

## Evidence to produce

- a state matrix
- a layer-specific error table
- canonical round-trip tests
- all illegal transition tests
- a compatibility note for adding a version 2 command

## Prohibited shortcuts

- a Boolean handshaken flag scattered through handlers
- performing domain work in the parser
- one generic invalid-request error
- ignoring unknown fields automatically
- socket-based tests for pure protocol logic

## Transfer

Transfer the protocol to a key-value service where version 2 adds compare-and-swap. State which changes require negotiation and which are backward-compatible.

## Comparing with the reference

Compare totality and error scope first. The reference is not stronger merely because it has more enum variants; every variant must own one protocol distinction.

The `solution/` directory is a reference after independent work, not a sequence of blanks to copy. Compare invariants, task ownership, cancellation behavior, bounds, and tests before comparing line count.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Begin in `starter/`. Do not open `solution/` until the state diagram, failure cases, and transfer design are written or a precise blocker is recorded.

The laboratory is complete when its tests pass and you can answer the governing question without the chapter:

> How can a frame payload become a typed message whose legality, response, and next state are exhaustive and versioned?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```
