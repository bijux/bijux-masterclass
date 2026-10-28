# Workbook — Module 75: Protocol State Machines, Versioning, and Defensive Parsing

[Return to the chapter](index.md) · [Open the solutions](solutions.md) · [Open the JobWire guide](../capstone.md)

## Part 1 — Predict

1. A frame is valid UTF-8 and contains `SUBMIT` before `HELLO`. Which layer rejects it?
2. A client sends `HELLO 2` to a server supporting only version 1. Should the server parse later fields using version 1 rules?
3. Two requests use different request IDs but the same idempotency key and same payload. Are they necessarily duplicate wire requests, duplicate semantic operations, or both?
4. The same idempotency key arrives with a different operation. What should the server do?
5. An unknown command arrives after a valid handshake. Can the connection always continue?
6. A parser ignores all unknown named fields “for forward compatibility.” What semantic risk appears?
7. A pipelined protocol has no maximum in-flight request count. Which resource is unbounded?
8. A public error response uses `format!("{internal_error:?}")`. What boundary has been violated?

## Part 2 — Diagnose and repair

A connection handler splits a line on spaces, matches the first token, performs domain work directly, and stores a Boolean `handshaken`. It returns the same `ERR invalid request` for every failure and continues the connection.

Repair the design into framing, parser, validator, transition, application, and renderer layers. Define at least three error scopes and one fatal state violation. Replace the Boolean with an exhaustive state enum.

## Part 3 — Focused exercises

### Exercise 1 — Grammar

Specify the exact syntax and bounds of `HELLO`, `PING`, `SUBMIT`, `STATS`, and `QUIT`. Define separator restrictions and maximum field lengths.

### Exercise 2 — State matrix

Create a table of every message against `Negotiating`, `Ready`, and `Closing`. Give response, next state, and close policy.

### Exercise 3 — IDs

Define syntax, uniqueness window, and collision behavior for request IDs. Separately define scope, fingerprint, and retention expectations for idempotency keys.

### Exercise 4 — Version policy

Choose exact match or highest common version. Add tests for no common version, repeated negotiation, and a feature legal only in a later version.

### Exercise 5 — Canonical round trip

Implement parse/render tests for every message and error. Add noncanonical input cases and state whether they are rejected or normalized.

## Part 4 — Independent laboratory

Build [Negotiated Command Protocol](../../labs/module-05-negotiated-command-protocol/README.md). Required evidence:

- pure parser and renderer;
- explicit state transition function;
- complete state/message matrix tests;
- version negotiation;
- stable public error codes;
- request and idempotency identities kept distinct;
- no socket dependency in protocol tests.

## Part 5 — Capstone transfer

Freeze JobWire V1. Write its frame-independent grammar, typed messages, canonical renderer, connection state machine, public error codes, and close policy. Use sequential requests per connection in V1. Add a compatibility note that states which changes require V2.

## Part 6 — Reconstruct and defend

1. What are the five protocol layers above bytes?
2. Why should state legality not be hidden in handlers?
3. What does version negotiation establish?
4. What problem does a request ID solve?
5. What additional problem does an idempotency key solve?
6. When may a connection continue after an error?

### Independent transfer

Design a two-version key-value protocol where V2 adds compare-and-swap. Specify negotiation, grammar, state, response correlation, duplicate semantics, and how a V1 client behaves when the server supports V2.
