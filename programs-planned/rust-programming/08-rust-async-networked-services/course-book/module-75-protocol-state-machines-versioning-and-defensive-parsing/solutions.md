# Reasoned Solutions — Module 75: Protocol State Machines, Versioning, and Defensive Parsing

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-05-negotiated-command-protocol/README.md) · [JobWire guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 75: Protocol State Machines, Versioning, and Defensive Parsing**. Compare the reasoning against this question: *Once frames arrive intact, how do they become legal protocol messages whose meaning depends on version, connection state, request identity, and error scope?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Part 1 — Prediction solutions

1. Framing and syntax may accept it, but the connection-state layer rejects it because negotiation is incomplete.
2. No. Unsupported negotiation should produce a defined error and close or await another allowed negotiation message according to policy. Silent downgrade changes semantics.
3. They are different wire requests and may represent the same semantic operation. Correlation and idempotency are separate axes.
4. Reject key reuse because one key cannot safely name two different semantic requests.
5. Not always. Continuation depends on whether the grammar remains synchronized and the protocol defines unknown commands as request-local.
6. A future critical field may be silently discarded, changing authorization or behavior. Extension points must distinguish optional from required semantics.
7. Pending request state, response buffers, and broker waiters can grow without bound.
8. Internal representation and potentially sensitive details have crossed the public protocol boundary.

## Part 2 — Repair reasoning

The Boolean admits scattered transitions and incomplete cases. A state enum plus total transition function makes all legal and illegal combinations visible. Framing errors, handshake violations, and truncation are connection-fatal. A well-framed unsupported domain operation can be request-local. Internal broker failure has an explicit public code while preserving its source internally.

Parsing should produce a raw syntax form. Validation constructs bounded newtypes. State transition authorizes the message. Application execution occurs only after these stages. Rendering owns stable external text.

## Part 3 — Focused exercise guidance

The grammar should count bytes and fields, not rely on informal examples. The state matrix should include repeated `HELLO`, `QUIT` during negotiation, messages after closing, and unsupported versions. ID policy must state duration and scope. Canonical rendering should make numeric and command spellings stable.

## Part 4 — Laboratory comparison

A strong protocol lab can be tested entirely with byte payloads and typed messages. Socket timing is irrelevant. Every state/message combination has one outcome. Error codes are stable values, while explanatory text may evolve within documented limits.

## Part 5 — Capstone comparison

JobWire V1 should remain sequential per connection to keep response ordering and cancellation clear. Concurrency exists across connections and in broker jobs. Adding pipelining, changing separator escaping, or altering idempotency scope is a versioned protocol change, not an implementation detail.

## Part 6 — Reconstruction and defense

A complete defense separates framing, encoding, syntax, semantics, state, and application commit. It explains that version selects rules, request IDs correlate, idempotency keys stabilize effects, and continuation after error is safe only when both peers retain the same framing and state interpretation.

## Deep reasoning and transfer

### Decisive model

> Once frames arrive intact, how do they become legal protocol messages whose meaning depends on version, connection state, request identity, and error scope?

Build a **protocol transition table**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Separate framing, text decoding, syntax parsing, semantic validation, state legality, and application execution.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Design an explicit connection-state machine with typed transitions.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Distinguish connection-fatal errors from request-local rejections.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Negotiate protocol versions before accepting ordinary commands.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Define canonical message rendering and strict parsing.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Separate framing, text decoding, syntax parsing, semantic validation, state legality, and application execution.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the protocol transition table.

### Reference implementation comparison

For [Negotiated Command Protocol](../../labs/module-05-negotiated-command-protocol/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In JobWire, Module 75 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Protocol State Machines, Versioning, and Defensive Parsing**, which relationship decides this question: “Once frames arrive intact, how do they become legal protocol messages whose meaning depends on version, connection state, request identity, and error scope?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to JobWire?
