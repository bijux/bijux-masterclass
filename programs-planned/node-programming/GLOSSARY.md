# Node.js Programming Glossary

## Runtime and package terms

**ECMAScript module (ESM)** — A module whose imports and exports participate in the ECMAScript module system and Node's ESM resolution rules.

**Package entry point** — A supported module specifier exposed through package metadata. A file existing under `dist` is not automatically an entry point.

**Type erasure** — The removal of TypeScript-only syntax and contracts before JavaScript executes.

**Runtime validation** — Code that inspects an external value and establishes a trusted application representation.

## Object-model terms

**Own property** — A property present directly on an object rather than found through its prototype chain.

**Descriptor** — The data or accessor record controlling a property's value/getter/setter, enumerability, configurability, and writability.

**Receiver** — The original object supplied to an internal property operation or function call; inherited accessors can observe it.

**Private brand** — The runtime identity check associated with JavaScript private fields and methods.

**Protocol** — A language-recognized operation, often symbol keyed, such as iteration or primitive conversion.

## Type-system and library terms

**Structural assignability** — Compatibility based on members and relationships rather than nominal declaration identity.

**Excess-property check** — An additional TypeScript check applied in selected fresh object-literal contexts; it is not runtime exactness.

**Generic relationship** — A connection among caller-visible types represented by one or more type parameters.

**Indexed access type** — A type such as `T[K]` that selects the property type associated with key `K` in `T`.

**Conditional type** — A type-level branch `T extends U ? X : Y`; it may distribute over unions when the checked side is a naked type parameter.

**Mapped type** — A type that derives properties by iterating over a key set.

**Key remapping** — The `as` clause in a mapped type, used to rename or filter derived keys.

**Template-literal type** — A string-literal type computed by interpolating finite literal unions.

**Variance** — The safe direction of generic substitution derived from whether a type parameter is produced, consumed, or both.

**Declaration file** — A `.d.ts` artifact describing a JavaScript module's static consumer contract. It does not prove runtime behavior.

**Consumer fixture** — A separate package that imports the built public surface to test real declarations, resolution, and execution.

**Schema** — A runtime parser or validator associated with one trusted static output type.

**Compatibility surface** — One independently breakable contract: source, type, declaration, runtime, behavior, package path, error, or stored data.

**Migration** — An explicit semantic conversion from one versioned representation to another.


## Async execution and lifecycle terms

**Ready** — Eligible for execution according to the runtime scheduler; readiness is not execution or completion.

**Promise owner** — The component responsible for observing settlement, preserving rejection, requesting cancellation when applicable, joining cleanup, and translating the terminal result.

**Cancellation request** — A one-way signal asking cooperative work to stop; it does not roll back completed effects or forcibly terminate arbitrary JavaScript.

**Deadline** — An absolute point in a monotonic time domain after which an operation should no longer continue waiting or starting new work.

**Event authority** — The component that commits the state transition reported by an event. Listeners normally observe the fact; they do not author it.

**Async context** — Small run-scoped diagnostic metadata propagated across supported asynchronous descendants. It is not implicit authorization.

**Admission bound** — The maximum work a component accepts into its ownership before execution capacity becomes available.

**Active-work bound** — The maximum operations allowed to execute concurrently.

**Terminal accounting** — The requirement that every accepted identity reaches exactly one documented terminal category.

**Quiesce** — Stop accepting new work while retaining ownership of already accepted work.

**Drain** — Wait for accepted work to complete cooperatively.

**Abort phase** — Request or enforce the documented stronger termination policy after drain or a grace deadline fails.

**Complete join** — Observe every owned task and cleanup action reaching a terminal state before reporting lifecycle completion.

## Streams, bytes, and pipeline terms

**Backing store** — The underlying memory region referenced by a `Buffer`, `Uint8Array`, or related view. Multiple views may expose the same bytes.

**Byte view** — A typed-array or Buffer window defined by a backing store, byte offset, and byte length. A view is not automatically an owned copy.

**Byte mode** — Stream operation where capacity is measured in bytes and chunks carry binary or text bytes.

**Object mode** — Stream operation where capacity is measured in JavaScript values rather than bytes.

**High-water mark** — A stream queue threshold used to signal pressure. It is a scheduling and buffering parameter, not a complete memory limit.

**Backpressure** — The protocol by which a consumer communicates temporary capacity exhaustion so an upstream producer pauses rather than growing queues without bound.

**Drain** — The writable-side signal that capacity has returned after `write()` reported pressure. The chunk that caused `write()` to return `false` was already accepted.

**Pipeline owner** — The promise or component responsible for the complete connected graph: pressure, errors, teardown, cancellation, and terminal completion.

**Framing** — The rule that turns a byte or text sequence into complete messages or records. Transport chunk boundaries are not frame boundaries.

**Incremental decoder** — Stateful decoding that preserves incomplete multibyte sequences or frames across arbitrary input chunks.

**Canonical representation** — One deliberately stable byte encoding of a logical value. A canonical digest identifies those bytes, not every equivalent runtime object.

**Digest domain** — The exact representation consumed by a hash, such as raw input, canonical NDJSON, compressed output, or child stdout.

**Stage file** — A candidate file written beside a destination and kept non-authoritative until the publication protocol succeeds.

**Publication point** — The operation after which readers may treat the new product as authoritative, commonly a rename or committed manifest update.

**Pre-commit failure** — Failure before publication; the previous visible product should remain authoritative and the candidate should be cleaned up.

**Post-commit failure** — Failure after publication, such as a later durability step. It must not be reported as if publication never occurred.

**Fan-out** — One source feeding multiple branches. Required branches need coordinated pressure, failure, terminal completion, and publication policy.

**Child stdio ownership** — Responsibility for concurrently driving stdin, draining stdout and stderr, interpreting exit and signal state, and waiting for close before reporting completion.


## Networking and service terms

**Logical service identity** — the name and scheme the application intends to reach, such as `https://service.example`; it is not interchangeable with one resolved IP address.

**Address candidate** — one socket address returned by resolution and considered under a declared connection-order and fallback policy.

**Bound address** — the local address and port actually assigned to a listening socket. With port zero, the operating system selects the port and the program must read it back.

**Peer address** — the remote socket address observed for one connection or datagram. It is transport evidence, not authentication by itself.

**Half-close** — the state in which one direction of a TCP connection has ended while the other may still carry bytes.

**Framing** — the application rule that reconstructs messages from a byte stream, for example a length prefix or delimiter with explicit limits.

**Datagram correlation** — a request identifier or equivalent rule that lets a UDP client associate a response with a current attempt and reject stale or unrelated datagrams.

**Semantic commit** — the point at which application state becomes authoritative, regardless of whether the response has reached the client.

**Idempotency key** — client-supplied semantic identity reused across retries so that several attempts can refer to one operation.

**Entity tag (ETag)** — an HTTP representation validator. In ServiceWire it is derived from job identity and revision and supports conditional reads and preconditions.

**SNI** — Server Name Indication, the TLS extension carrying the requested logical server name during handshake so a shared endpoint can select identity material.

**ALPN** — Application-Layer Protocol Negotiation, the TLS mechanism used by peers to agree on an application protocol such as HTTP/1.1 or HTTP/2.

**HTTP/2 session** — one multiplexed connection-level protocol state containing several independent streams and shared flow-control and failure state.

**HTTP/2 stream** — one bidirectional request/response exchange within a session, with its own lifecycle and flow-control state.

**SSE replay gap** — the condition where a reconnecting client's last known event predates the oldest retained event, so complete replay is impossible.

**Admission** — the decision to accept an operation into a bounded product responsibility. Listener acceptance, body parsing, application commit, and active execution may have separate admission points.

**Quiesce** — stop new admission and report not-ready while preserving owned accepted work for drain.

**Drain** — allow accepted work to reach terminal state under a bounded grace period before forced cancellation.
