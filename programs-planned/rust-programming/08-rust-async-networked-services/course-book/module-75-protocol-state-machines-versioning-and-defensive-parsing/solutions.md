# Reasoned Solutions — Module 75: Protocol State Machines, Versioning, and Defensive Parsing

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the JobWire guide](../capstone.md)

The governing correction is that transport success does not imply protocol legality. Each layer validates a different claim and determines a different error scope.

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
