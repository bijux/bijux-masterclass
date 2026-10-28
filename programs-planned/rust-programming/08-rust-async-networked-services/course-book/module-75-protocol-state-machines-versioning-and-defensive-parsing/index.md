# Module 75: Protocol State Machines, Versioning, and Defensive Parsing

**Course 8, day 5 · Module 75 of 80**

**75/80** · [Course overview](../index.md) · [Workbook](workbook.md) · [Solutions](solutions.md) · [JobWire guide](../capstone.md)

## The question

> Once frames arrive intact, how do they become legal protocol messages whose meaning depends on version, connection state, request identity, and error scope?

## Why this comes now

A bounded frame is not yet a valid request. The bytes may be invalid UTF-8, the command may be unknown, a field may be malformed, the message may be legal only after handshake, or the requested operation may violate domain policy. Mixing these layers into one `match` over strings makes errors vague and state transitions accidental.

Modules 73 and 74 established frame and connection lifecycles. This module adds the language spoken over that connection. The protocol becomes a typed state machine rather than a collection of commands that happen to arrive over TCP.

Versioning appears here because every public protocol creates future compatibility obligations. A version field is useful only when both peers define negotiation, unsupported versions, feature behavior, and the lifetime of compatibility. Request IDs and idempotency keys also appear here as distinct concepts: one correlates a response; the other prevents duplicate semantic effects.

## What you will be able to do

- separate framing, text decoding, syntax parsing, semantic validation, state legality, and application execution;
- design an explicit connection-state machine with typed transitions;
- distinguish connection-fatal errors from request-local rejections;
- negotiate protocol versions before accepting ordinary commands;
- define canonical message rendering and strict parsing;
- distinguish request identifiers, operation identifiers, and idempotency keys;
- prevent duplicate fields, ambiguous grammar, and uncontrolled extension points;
- state compatibility rules for unknown commands and fields;
- represent protocol errors without leaking internal implementation details;
- test state transitions and malformed messages independently of sockets.

## Core model

### Protocol layers answer different questions

Use this sequence:

```text
bytes
  ↓ framing: is one bounded message complete?
payload
  ↓ text/encoding: can the payload be interpreted?
tokens
  ↓ syntax: does it match the command grammar?
typed message
  ↓ semantics: are field values valid?
validated message
  ↓ connection state: is it legal now?
authorized action
  ↓ application: does the domain accept and commit it?
response
```

An error at each layer has different scope. A length above the frame maximum often closes the connection because synchronization cannot be trusted or the peer is abusive. A malformed command may produce a protocol error and close, or remain request-local if the grammar allows safe recovery. A domain rejection such as an unsupported job operation can preserve the connection.

Avoid one error variant called `InvalidRequest(String)`. It erases the layer, source location, response code, and connection policy.

### Connection state is explicit product state

For a simple service:

```text
Accepted
    └─ HELLO supported-version ─> Ready(version)
    └─ anything else ───────────> Closing(error)

Ready(version)
    ├─ SUBMIT ─> Ready(version)
    ├─ STATS  ─> Ready(version)
    ├─ PING   ─> Ready(version)
    ├─ QUIT   ─> Closing(normal)
    └─ HELLO  ─> Closing(state-error)
```

A state diagram should specify:

- legal inbound messages;
- generated responses;
- state transition;
- side effect or commit point;
- whether an error is local or connection-fatal;
- whether pipelining is allowed;
- whether responses may be reordered.

The code should make illegal transitions hard to express. This can use an enum state plus exhaustive matching, typestate for internal construction, or an actor whose receive loop owns the current state. Do not scatter `if handshaken` booleans across handlers.

### Version negotiation precedes version-dependent grammar

A first message such as `HELLO 1` establishes which grammar and semantics apply. The server responds with an accepted version or a supported range. Until negotiation completes, version-dependent commands are not interpreted.

Possible policies include:

- exact-version match;
- highest common version;
- major/minor compatibility;
- version plus feature advertisement.

Choose one and make it testable. Avoid “ignore unknown fields for forward compatibility” as a reflex. Ignoring an unknown field can silently discard security or semantic meaning. Extensibility requires designated extension positions and a rule for critical versus optional features.

### Grammar should be unambiguous and bounded

Suppose JobWire uses tab-separated text inside length-prefixed frames:

```text
HELLO\t1
SUBMIT\trequest-17\tkey-91\tuppercase\thello world
STATS\trequest-18
PING\trequest-19
QUIT
```

The frame layer bounds total bytes. The parser still needs:

- maximum field count;
- exact arity per command;
- identifier length and character policy;
- numeric range checks;
- no duplicate named fields if a named-field grammar is used;
- a clear escaping rule or a restriction that makes separators impossible inside fields;
- no trailing tokens unless explicitly allowed.

If payload text may contain tabs, the grammar needs escaping or a length for the final field. A simpler course protocol can define that the final payload consumes the remaining bytes and may contain spaces but not tab or line break. The restriction must be stated and validated.

### Parsing and validation are separate

Parsing answers “which syntax was written?” Validation answers “is this meaningful and permitted?” Keeping them separate improves diagnostics and version evolution.

```rust
struct RawSubmit<'a> {
    request_id: &'a str,
    idempotency_key: &'a str,
    operation: &'a str,
    payload: &'a str,
}

struct Submit {
    request_id: RequestId,
    idempotency_key: IdempotencyKey,
    operation: Operation,
    payload: String,
}
```

The raw form can borrow from the frame. Validation constructs owned domain values only after bounds and semantics pass. If the request must move to a broker task, ownership is required at that boundary.

### Request IDs are not idempotency keys

A request identifier correlates one response with one request, especially when pipelining or out-of-order responses exist. Reusing one may be a protocol error, but a unique request ID alone does not define duplicate-effect behavior across reconnects.

An idempotency key identifies one semantic operation within a documented scope and retention window. The server records:

```text
(scope, key) → request fingerprint + in-progress/completed outcome
```

If the same key and same fingerprint arrive again, return or await the same semantic outcome. If the key is reused with different content, reject it. Module 79 implements the retry policy, but the wire grammar must carry the key now.

### Error responses need stable public meaning

A protocol error should include a stable code and enough context for a client to act, without leaking internal paths, panic payloads, SQL text, or debug representations.

Example:

```text
ERR\trequest-17\tINVALID_ARGUMENT\toperation is not supported
ERR\t-\tPROTOCOL_STATE\tHELLO is required before SUBMIT
BUSY\trequest-17\t250
```

The dash represents no request correlation when parsing failed before an ID was trusted. Retry delay is a protocol field, not embedded in a human message.

Internally preserve causal errors and sources. Render a controlled external form at the boundary.

### Error scope preserves synchronization

A connection can continue only when both peers still agree on framing and state. Classify:

| Error | Likely scope |
|---|---|
| frame too large | connection-fatal |
| truncated frame | connection-fatal |
| invalid UTF-8 | usually connection-fatal or explicit error then close |
| unknown command in ready state | request-local or connection-fatal by policy |
| wrong arity | request-local only when correlation can be recovered |
| command before handshake | connection-fatal state violation |
| unsupported domain operation | request-local |
| internal broker failure | request-local or service-fatal depending authority |

The important point is not one universal table. It is that every error has an explicit response and next state.

### Pipelining changes the protocol

If a client may send several requests without waiting, the service needs:

- unique live request IDs;
- a maximum in-flight count per connection;
- response correlation;
- explicit response ordering policy;
- cancellation behavior when the connection closes;
- fairness between connections;
- bounded pending response storage.

Sequential request/response is simpler and appropriate for Course 8’s initial JobWire connection. The broker itself remains concurrent across connections. Later evolution can add pipelining as a versioned feature rather than an accidental side effect.

### Canonical rendering supports compatibility

A canonical renderer emits one representation for each message. It fixes command spelling, field order, numeric formatting, and escaping. Round-trip tests prove:

```text
parse(render(message)) == message
```

They do not prove that every accepted noncanonical input renders identically unless that is part of the contract. Decide whether the parser is strict or normalizing.

## Use the idea in a complete program

A small pure state machine can be tested without I/O:

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Version {
    V1,
}

#[derive(Debug, PartialEq, Eq)]
pub enum Message {
    Hello { version: u16 },
    Ping { request_id: String },
    Quit,
}

#[derive(Debug, PartialEq, Eq)]
pub enum Reply {
    Welcome { version: Version },
    Pong { request_id: String },
    Bye,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum State {
    Negotiating,
    Ready(Version),
    Closing,
}

#[derive(Debug, PartialEq, Eq)]
pub struct ProtocolError {
    pub code: &'static str,
    pub close: bool,
}

pub fn transition(
    state: State,
    message: Message,
) -> Result<(State, Reply), ProtocolError> {
    match (state, message) {
        (State::Negotiating, Message::Hello { version: 1 }) => {
            Ok((State::Ready(Version::V1), Reply::Welcome { version: Version::V1 }))
        }
        (State::Negotiating, Message::Hello { .. }) => Err(ProtocolError {
            code: "UNSUPPORTED_VERSION",
            close: true,
        }),
        (State::Negotiating, _) => Err(ProtocolError {
            code: "HANDSHAKE_REQUIRED",
            close: true,
        }),
        (State::Ready(_), Message::Ping { request_id }) => {
            Ok((state, Reply::Pong { request_id }))
        }
        (State::Ready(_), Message::Quit) => Ok((State::Closing, Reply::Bye)),
        (State::Ready(_), Message::Hello { .. }) => Err(ProtocolError {
            code: "ALREADY_NEGOTIATED",
            close: true,
        }),
        (State::Closing, _) => Err(ProtocolError {
            code: "CONNECTION_CLOSING",
            close: true,
        }),
    }
}
```

The state machine is total: every state/message combination has meaning. Parsing remains outside it. Application work remains outside it. This separation is what makes exhaustive tests possible.

## Practice sequence

1. Write the JobWire grammar without code.
2. Separate framing, syntax, semantics, state, and application errors.
3. Draw the negotiation and ready-state machine.
4. Decide sequential versus pipelined requests.
5. Define request-ID and idempotency-key policies separately.
6. Implement pure parse/render and transition functions.
7. Test every illegal state/message pair.
8. State version compatibility and unknown-field behavior.

## Ready to continue

Continue only when you can explain:

- why a complete frame can still be an invalid message;
- which layer owns each validation;
- how state determines command legality;
- why request IDs and idempotency keys are different;
- which errors preserve synchronization;
- what a version negotiation actually promises;
- why canonical rendering helps evolution.

## Primary Rust references

- Rust enums, exhaustive matching, `FromStr`, and error-source contracts;
- Tokio-util framing contracts from Module 73;
- protocol specifications you control, treated as normative product documents rather than inferred from implementation.

## Continue

Complete the [workbook](workbook.md), use the [reasoned solutions](solutions.md) only after freezing your own answer, build [Negotiated Command Protocol](../../labs/module-05-negotiated-command-protocol/README.md), and add the fifth [JobWire increment](../capstone.md#increment-5-freeze-the-wire-protocol). Then continue to [Module 76](../module-76-backpressure-admission-control-and-fair-work-distribution/index.md).
