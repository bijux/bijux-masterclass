# Module 52 Solutions — TCP Framing and Connection State

## Prediction reasoning

Two writes may arrive as one combined read, several partial reads, or one read containing the end of the first and part of the second. Order remains stable. The transport does not expose write boundaries.

EOF with a partial prefix is truncation. The peer promised the beginning of a message but did not complete enough bytes to determine its length.

A half-closed peer may still receive. Whether the server writes the response depends on the application protocol. For a one-request protocol, this is often valid.

A false `write()` return does not authorize writing the same frame again. The bytes were accepted into the write path. Wait for pressure relief before producing additional bytes.

Closing the listener stops new accepts; established sockets remain separate resources. Shutdown is incomplete until they finish or are destroyed and observed closed.

## Repair reasoning

A correct decoder owns pending state independent of chunks. It should consume bytes in a loop and emit zero or more frames. A limit check belongs immediately after decoding the prefix and before allocating or accumulating the declared payload.

Finalization must branch on state:

- empty prefix state: clean protocol boundary;
- partial prefix: truncated-prefix error;
- payload state with insufficient bytes: truncated-payload error.

Peer EOF changes readable state. It does not prove writable completion. Conversely, local `end()` initiates write completion and does not prove the peer has ended its read direction.

A timeout handler must choose and perform a terminal action, usually destroy or orderly end under protocol policy. It must also remove listeners and settle the connection owner once.

## Construction notes

A simple decoder can keep one `Buffer` of pending bytes when `maxFrameBytes` is modest and explicit. After appending a chunk, parse as many frames as possible. For large bounds, repeated concatenation may become expensive; a piece list or capacity-managed buffer avoids quadratic copying. Optimize only after correctness and bounds are established.

Structured errors should include stable codes such as:

```text
FRAME_TOO_LARGE
TRUNCATED_PREFIX
TRUNCATED_PAYLOAD
CONNECTION_IDLE
```

Do not include entire peer payloads in errors.

The server's uppercase operation should transform bytes only if the protocol defines text. If it accepts UTF-8 text, decode strictly and separate framing failure from text-decoding failure.

## Laboratory evidence

Strong tests include:

- every split position for two canonical frames;
- one chunk containing three frames;
- zero-length frame if supported;
- declared length exactly at limit and one byte above;
- EOF at every prefix position;
- EOF at several payload positions;
- client half-close followed by server response;
- slow partial frame triggering the declared policy;
- listener shutdown with active sockets;
- forced abort after grace.

No test should depend on the operating system coincidentally grouping writes.

## ServiceWire transfer

HTTP parsing is performed by Node's HTTP implementation, but ServiceWire still owns request-body bounds, connection admission, idle policy, and shutdown. TCP errors before a complete HTTP request may not have an application request ID. Preserve them as transport diagnostics. Errors after a request is identified can be associated with the request while still retaining transport cause internally.

## Independent transfer

For two variable sections, decode and validate fixed header fields first. Use checked addition and independent section limits. Reject a first or second length before allocating its section. At EOF, report which section was incomplete and how many bytes were expected versus received.

## Defense summary

TCP gives ordered delivery of bytes, not messages or commits. The application adds a bounded parser, independent directional state, explicit time policy, and a connection owner. Every shortcut that treats a chunk, EOF, write acceptance, or listener close as a stronger fact than it is creates a lifecycle bug.

## Chunk-partition solution

The invariant is that concatenating the emitted payloads and boundaries is independent of chunk partition. Every split position tests a different division between retained and newly supplied bytes. Testing two split positions covers three chunks and catches bugs where a prefix or payload spans more than one boundary.

For the half-close case, EOF moves the read side to ended while the write side remains open. The decoder must first prove that no prefix or payload is incomplete. Parsed work already placed on the response chain remains owned by that connection. The response chain is the only writer; on rejection it destroys the socket. `end` expresses intent to finish writes, `finish` reports that writable data was handed off, and `close` reports resource termination. None alone proves the other two.

The weak repair is to destroy immediately on readable EOF. That makes the test pass only by deleting the requirement to send final responses after peer half-close.

## Memory-retention solution

Repeated concatenation is simple but copies pending bytes repeatedly. A chunk queue avoids repeated copying but needs careful offset and release logic. Subarray views are cheap yet can retain a large backing allocation after most bytes are consumed. For a 64 KiB bounded teaching protocol, copying pending bytes is acceptable and easy to audit. A high-throughput parser may use a chunk queue, but only after profiling demonstrates copy cost and tests prove released chunks no longer remain reachable.
