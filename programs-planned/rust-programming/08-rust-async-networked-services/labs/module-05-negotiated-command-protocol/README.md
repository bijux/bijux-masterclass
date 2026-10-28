# Laboratory 75 — Negotiated Command Protocol

**Course 8 · Module 75: Protocol State Machines, Versioning, and Defensive Parsing**

[Chapter](../../course-book/module-75-protocol-state-machines-versioning-and-defensive-parsing/index.md) · [Workbook](../../course-book/module-75-protocol-state-machines-versioning-and-defensive-parsing/workbook.md) · [JobWire guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Protocol State Machines, Versioning, and Defensive Parsing**: Once frames arrive intact, how do they become legal protocol messages whose meaning depends on version, connection state, request identity, and error scope? The product must make **Separate framing, text decoding, syntax parsing, semantic validation, state legality, and application execution** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **protocol transition table** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

> How can a frame payload become a typed message whose legality, response, and next state are exhaustive and versioned?

The completed product must make the answer visible in its types, lifecycle, tests, failure behavior, and explanation. A successful happy-path run is not sufficient.

## Product

Build a pure negotiated protocol with `HELLO`, `PING`, `ECHO`, and `QUIT`. Parsing, semantic validation, transition, and rendering are separate. Version 1 is the only supported version and every state/message pair has a defined outcome.

## Product-specific design pressure

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

For **Laboratory 75 — Negotiated Command Protocol**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Working route

1. Read the product contract and run the starter’s baseline checks for **Negotiated Command Protocol**.
2. Draw the smallest **protocol transition table** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to JobWire so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Separate framing, text decoding, syntax parsing, semantic validation, state legality, and application execution.
- Design an explicit connection-state machine with typed transitions.
- Distinguish connection-fatal errors from request-local rejections.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 75 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **protocol transition table**. Defend why your design is simpler than one plausible alternative under the new requirements.
