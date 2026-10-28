# Workbook — Module 75: Protocol State Machines, Versioning, and Defensive Parsing

[Chapter](index.md) · [Laboratory](../../labs/module-05-negotiated-command-protocol/README.md) · [JobWire guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Protocol State Machines, Versioning, and Defensive Parsing** has become a usable model rather than remembered vocabulary. Its governing question is: *Once frames arrive intact, how do they become legal protocol messages whose meaning depends on version, connection state, request identity, and error scope?* Preserve your first prediction and record decisive facts in a **protocol transition table**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 74 — TCP, UDP, DNS, and Connection Lifecycles that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **Once frames arrive intact, how do they become legal protocol messages whose meaning depends on version, connection state, request identity, and error scope?**
3. Draw the smallest **protocol transition table** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

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

### Interleaved reasoning pass

1. For **Separate framing, text decoding, syntax parsing, semantic validation, state legality, and application execution**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the protocol transition table.
2. For **Design an explicit connection-state machine with typed transitions**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the protocol transition table.
3. For **Distinguish connection-fatal errors from request-local rejections**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the protocol transition table.
4. For **Negotiate protocol versions before accepting ordinary commands**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the protocol transition table.

5. Identify one guarantee from an earlier course that a careless implementation of **Protocol State Machines, Versioning, and Defensive Parsing** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Negotiated Command Protocol](../../labs/module-05-negotiated-command-protocol/README.md). Required evidence:

- pure parser and renderer;
- explicit state transition function;
- complete state/message matrix tests;
- version negotiation;
- stable public error codes;
- request and idempotency identities kept distinct;
- no socket dependency in protocol tests.

### Laboratory acceptance trace

Before opening the reference implementation for **Negotiated Command Protocol**, record:

- the public behavior that demonstrates **Separate framing, text decoding, syntax parsing, semantic validation, state legality, and application execution**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Freeze JobWire V1. Write its frame-independent grammar, typed messages, canonical renderer, connection state machine, public error codes, and close policy. Use sequential requests per connection in V1. Add a compatibility note that states which changes require V2.

### Capstone invariant trace

For the Module 75 JobWire increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

1. What are the five protocol layers above bytes?
2. Why should state legality not be hidden in handlers?
3. What does version negotiation establish?
4. What problem does a request ID solve?
5. What additional problem does an idempotency key solve?
6. When may a connection continue after an error?

### Independent transfer

Design a two-version key-value protocol where V2 adds compare-and-swap. Specify negotiation, grammar, state, response correlation, duplicate semantics, and how a V1 client behaves when the server supports V2.

### Closed-book defense

In five minutes, answer “Once frames arrive intact, how do they become legal protocol messages whose meaning depends on version, connection state, request identity, and error scope?” using the **protocol transition table**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside JobWire. A list of APIs without the deciding relationship is incomplete.
