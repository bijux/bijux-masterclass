# Module 52 — TCP: Connection State, Framing, Half-Close, and Idle Policy

**Progress: 52/100**

## The governing question

> How do you recover bounded application messages and honest terminal states from a bidirectional byte stream that can split, combine, delay, half-close, or terminate at any point?

## Why this module comes now

Module 51 established how a logical endpoint becomes a connected socket under one time budget. A socket, however, is not yet an application protocol. TCP preserves byte order while a connection exists; it does not preserve the boundaries of the writes that produced those bytes. It also has independent read and write directions. A peer can finish sending while remaining able to receive. A local write can be accepted into Node's buffers before the peer receives or processes it.

This module turns the connection into a stateful protocol boundary. The same reasoning later applies to HTTP request bodies, HTTP/2 streams, and long-lived event channels.

## Observable outcomes

By the end of the module, you can:

- distinguish TCP transport guarantees from application-message guarantees;
- implement bounded length-prefixed framing over arbitrary chunk partitions;
- reject oversized lengths before allocation;
- classify clean EOF, truncated prefix, truncated payload, reset, local abort, and protocol error;
- reason about independent readable and writable state;
- define half-close policy instead of relying on defaults accidentally;
- obey writable pressure and await terminal completion;
- define idle activity in protocol terms;
- track and close every accepted socket during shutdown.

## The connection-state ledger

For each connection, track at least:

| Dimension | Questions |
|---|---|
| read state | open, EOF, errored, or destroyed? |
| write state | open, ending, finished, errored, or destroyed? |
| frame state | reading prefix, reading payload, or between frames? |
| pending bytes | how many bytes are retained and under which bound? |
| admitted messages | how many complete frames have entered application logic? |
| activity | which protocol event resets idle policy? |
| owner | which scope closes the socket and observes terminal events? |
| terminal cause | peer EOF, protocol error, timeout, cancellation, reset, or local shutdown? |

Avoid a single Boolean called `closed`. It hides which direction ended, whether pending protocol state remained, and who caused termination.

## TCP is an ordered byte stream

Suppose a client performs three writes:

```text
write A: [01 02]
write B: [03]
write C: [04 05 06]
```

The server may read:

```text
[01]
[02 03 04 05]
[06]
```

or any other partition that preserves order. It cannot infer the original write boundaries. Every application protocol must add framing.

Common framing strategies include:

- fixed-size records;
- delimiter-terminated records;
- length-prefixed records;
- self-describing syntax with a bounded parser;
- connection-close as message boundary for a one-message protocol.

Length-prefix framing is useful for the laboratory because it exposes several separate states: incomplete prefix, validated length, incomplete payload, complete frame, and EOF.

## Bound before allocation

A four-byte unsigned prefix can describe more than four billion bytes. The parser must compare the declared length with `maxFrameBytes` before allocating or retaining that payload.

A safe progression is:

```text
1. retain at most prefix width
2. decode length
3. reject if length > maxFrameBytes
4. allocate or accumulate only within the accepted bound
5. emit exactly one complete payload
6. return to prefix state
```

Checking the limit after `Buffer.alloc(length)` defeats the purpose. The attack occurs before validation.

Checked arithmetic also matters when calculating combined sizes such as `prefixBytes + payloadBytes`. JavaScript numbers can represent these small bounded values exactly, but the product should still reject negative, non-integer, and unsafe configuration values.

## A decoder is a state machine

A useful explicit model:

```ts
type DecodeState =
  | { readonly kind: 'prefix'; readonly buffered: Buffer }
  | { readonly kind: 'payload'; readonly length: number;
      readonly pieces: readonly Buffer[]; readonly received: number };
```

An implementation can use one compact mutable buffer for efficiency, but the conceptual states should remain visible. Every chunk drives zero or more transitions. One chunk may complete several frames.

The parser must make progress. A loop that neither consumes bytes nor emits a frame is an infinite loop. Tests should include empty payloads when the protocol permits them because zero-length frames often expose progress bugs.

## EOF is protocol input

EOF between frames can be a clean connection end. EOF while retaining one or more prefix bytes is a truncated prefix. EOF after a validated length but before the full payload is a truncated frame. These are different terminal outcomes.

A weak decoder discards pending bytes on `'end'` and reports success. That turns corruption into normal closure.

The connection owner should ask the decoder to finalize at EOF:

```ts
decoder.finish();
```

`finish()` either confirms that no partial frame remains or throws a structured truncation error.

## Half-close is two directions, not one connection state

TCP permits one peer to signal that it will send no more bytes while continuing to receive. Node exposes this through events and options such as `allowHalfOpen`.

Consider a request/response protocol:

1. client sends one request;
2. client half-closes its write direction;
3. server computes response;
4. server writes response and ends.

If the server treats peer EOF as immediate destruction, it may lose the response. Conversely, a long-lived protocol may define peer EOF as full termination.

The correct behavior belongs to the application protocol, not a universal TCP rule.

Document:

- whether read EOF permits pending writes to finish;
- whether the local side automatically ends after peer EOF;
- whether new application messages are allowed after either direction closes;
- how shutdown interacts with half-open connections.

## Backpressure still applies

A framed protocol can parse input correctly and still create unbounded output. `socket.write()` returns a Boolean indicating whether the internal writable queue remains below its high-water threshold. A false return means the producer should wait for `'drain'` before continuing.

It does not mean the write failed. It also does not mean the peer received the data.

A helper can bridge the callback and pressure signals:

```ts
import type net from 'node:net';

export async function writeBuffer(
  socket: net.Socket,
  bytes: Uint8Array,
): Promise<void> {
  await new Promise<void>((resolve, reject) => {
    const onError = (error: Error) => {
      cleanup();
      reject(error);
    };
    const cleanup = () => socket.off('error', onError);
    socket.once('error', onError);
    socket.write(bytes, (error) => {
      cleanup();
      if (error) reject(error);
      else resolve();
    });
  });
  if (socket.writableNeedDrain) {
    await new Promise<void>((resolve, reject) => {
      socket.once('drain', resolve);
      socket.once('error', reject);
    });
  }
}
```

A production helper must avoid listener races and double settlement; the example exposes the two separate concerns: write callback completion and queue pressure.

## Idle policy must name meaningful activity

`socket.setTimeout(ms)` measures inactivity according to socket I/O. A peer can send one byte before every timeout and keep a connection alive while never completing a frame. If the product needs protection against slow partial frames, define a frame-progress or message deadline in addition to byte-level idle time.

Possible policies:

- no bytes for N milliseconds;
- no complete frame for N milliseconds;
- incomplete frame may exist for at most N milliseconds;
- no application heartbeat for N milliseconds;
- total connection age limit.

These policies have different false-positive and abuse properties. ServiceWire will use HTTP-specific request and keep-alive policies later; this module makes the distinction visible at the TCP level.

## Socket ownership and shutdown

A server must track accepted sockets because stopping the listener does not necessarily close established connections. A registry usually needs:

```ts
const sockets = new Set<import('node:net').Socket>();

server.on('connection', (socket) => {
  sockets.add(socket);
  socket.once('close', () => sockets.delete(socket));
});
```

Shutdown phases can then:

1. stop accepting new connections;
2. request orderly end where the protocol permits it;
3. wait under one grace deadline;
4. destroy remaining sockets;
5. confirm the registry is empty.

Do not delete a socket from the registry merely because shutdown requested closure. Delete it on observed terminal close.

## Worked case — length framing under arbitrary chunks

Wire format:

```text
4-byte unsigned big-endian length
payload bytes
```

Input:

```text
00 00 00 03 61 62 63 00 00 00 02 78 79
```

Possible chunks:

```text
[00]
[00 00 03 61 62]
[63 00 00]
[00 02 78 79]
```

The decoder must emit `abc` and `xy`. After consuming the first prefix it knows the length is 3. It may have two payload bytes already. After the next chunk it completes the first frame and immediately begins the next prefix from the same chunk.

The same canonical byte sequence must yield the same frames for every partition. A powerful test generates every split position and several multi-split combinations.

## Terminal taxonomy

Use a structured terminal result:

```ts
type ConnectionTerminal =
  | { readonly kind: 'peer-eof' }
  | { readonly kind: 'protocol-error'; readonly code: string }
  | { readonly kind: 'idle-timeout' }
  | { readonly kind: 'deadline' }
  | { readonly kind: 'cancelled' }
  | { readonly kind: 'reset'; readonly code?: string }
  | { readonly kind: 'server-shutdown' };
```

Not every product must expose this exact union, but the design should preserve causal distinctions internally. Flattening them into “socket closed” destroys operational evidence.

## Common wrong models

### “One write equals one read”

It may appear true in tiny local tests. It is not a TCP guarantee.

### “EOF means success”

EOF is clean only when the protocol parser is between messages and the application permits peer completion.

### “A false `write()` return means failure”

It means writable pressure is high. The producer must wait, not retry the same bytes blindly.

### “Timeout closes the socket”

The timeout event requires an application terminal action.

### “Closing the server closes clients”

The listening server and accepted sockets have separate lifecycles.

## Decision procedure

Before accepting TCP traffic:

1. Define framing.
2. Define maximum prefix, frame, and connection counts.
3. Define empty-frame policy.
4. Define EOF in every decoder state.
5. Define read and write half-close behavior.
6. Define idle and incomplete-frame time policy.
7. Define output pressure behavior.
8. Track accepted sockets.
9. Define shutdown escalation.
10. Test every chunk partition around boundaries.

## ServiceWire increment

ServiceWire does not expose its own raw TCP application protocol, but its HTTP adapters still depend on these facts. Add:

- connection registry;
- actual accepted-connection bounds;
- request-body accumulation that never assumes chunk boundaries;
- explicit idle and shutdown policy;
- helper functions that end or destroy sockets under one owner.

## Deep reasoning — the parser is a resource state machine

A four-byte length prefix looks simple until input is split at every possible byte boundary. The decoder must represent at least two states:

```text
NeedPrefix(buffered 0..3)
NeedPayload(expected, buffered 0..expected)
```

The state is not merely parsing convenience. It determines how much memory may be retained, which error exists at EOF, and whether another chunk can be accepted safely. After reading a declared length, validate the length before allocating or waiting for that payload. A hostile peer can declare four gigabytes and then send nothing. The protocol limit must reject the declaration at the prefix boundary.

Consider this wire sequence:

```text
00 00 00 03 61 62 63 00 00 00 00
```

It contains the frame `abc` followed by an empty frame. A decoder that treats zero as EOF loses a legal message. A decoder that returns only one frame per chunk loses the second frame when both arrive together. A decoder that keeps subarray views into a large accumulation buffer may retain far more memory than the visible pending bytes suggest.

The correct invariant is stronger than “eventually emits frames”:

- all emitted payloads are exactly the declared length;
- output order equals wire order;
- no payload is emitted twice;
- no bytes are skipped or reinterpreted;
- retained pending bytes remain below a declared bound;
- EOF classifies incomplete prefix separately from incomplete payload;
- an oversized declared frame is rejected before proportional allocation.

### Half-close changes the terminal question

When the peer half-closes its write side, your process receives EOF on the readable side. That does not necessarily forbid writing a final response. A request/response protocol can use half-close as “I have sent all requests; now finish responses.” This is why connection state needs separate read and write dimensions.

```text
read open / write open
read ended / write open
read open / write ended
read ended / write ended
socket destroyed
```

Do not rely on one Boolean named `closed`. It cannot represent the states needed to reason about `allowHalfOpen`, `end`, `finish`, and forced destruction.

### Backpressure belongs to framed servers too

A frame decoder may produce ten responses from one incoming chunk. Calling `socket.write()` ten times does not mean the operating system accepted ten responses. Once `write()` returns `false`, the response owner must wait for `drain` before continuing. Otherwise the application converts peer slowness into unbounded buffered output.

The ordering requirement creates a useful pattern: one per-socket response chain. Parsed frames may be discovered synchronously, but response work is appended to an owned promise chain that respects `drain`. The chain’s rejection destroys the socket and remains observed.

### Failure matrix

| Event | Decoder state | Correct terminal action |
|---|---|---|
| clean EOF with no pending bytes | prefix/0 | finish normally |
| EOF with 2 prefix bytes | prefix/2 | truncated-prefix failure |
| EOF with 4 of 9 payload bytes | payload/9, buffered/4 | truncated-payload failure |
| declared length over limit | immediately after prefix | protocol rejection and close |
| UTF-8 decoding failure | complete payload | application-frame rejection |
| idle timeout | any | destroy under idle-policy owner |
| server shutdown grace expires | any | destroy and observe close |

The test suite should force every row. Normal-path echo tests alone cannot establish the framing contract.

## Ready to continue

You are ready for UDP when you can explain every decoder state at EOF and can show why transport ordering does not imply application framing.

## Primary Node.js references

- [Net](https://nodejs.org/docs/latest-v24.x/api/net.html)
- [Stream](https://nodejs.org/docs/latest-v24.x/api/stream.html)
- [Buffer](https://nodejs.org/docs/latest-v24.x/api/buffer.html)

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory brief](../../labs/module-52-bounded-tcp-frame-server/README.md)
- [ServiceWire engineering guide](../capstone.md)
