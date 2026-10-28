# Ten-Day Study Plan

This is a dense course. A day is not complete when the chapter has been read. It is complete when you can predict the mechanism, build the independent laboratory, transfer it into ServiceWire, and explain the resulting contract without notes.

A sustainable day contains approximately eight focused hours plus breaks. Stop when reasoning quality collapses. Network lifecycle bugs are often created by continuing after the reader can no longer track ownership or state.

## Daily rhythm

Use this rhythm unless a module's laboratory requires a different experiment:

| Time block | Work |
|---|---|
| 60–90 min | Read the authoritative chapter and create the module ledger |
| 45 min | Make written predictions before running any specimen |
| 60 min | Complete diagnosis and repair tasks |
| 2–3 h | Build the laboratory from `starter/` |
| 60–90 min | Transfer the mechanism into ServiceWire |
| 45 min | Compare with `reference/` and record one justified difference |
| 30 min | Closed-book reconstruction and next-module readiness check |

Do not let the capstone consume the laboratory. The lab is a smaller product that makes one mechanism observable. ServiceWire tests whether that mechanism survives contact with the rest of the architecture.

## Day 1 — Names, addresses, and time

Read Module 51. Draw a chain from service URL to resolver answer to connection candidate to actual socket endpoints. Write down which values are logical names and which are observations of one connection.

Build the Address Resolution Observatory. Test several injected candidate sets, including mixed IPv4/IPv6 results, an empty result, and a first candidate that fails within the overall deadline.

ServiceWire transfer: define its endpoint configuration, actual bound-address report, resolver boundary, and absolute connection-budget helper.

Readiness question: can you explain why setting a timeout independently on each candidate can multiply the caller's promised budget?

## Day 2 — TCP as a stateful byte stream

Read Module 52. Draw separate read and write state for both peers. Trace a message split at every byte boundary and several messages coalesced into one read.

Build the Bounded TCP Frame Server. It must reject oversized prefixes before allocation and distinguish clean EOF between frames from truncated EOF inside a frame.

ServiceWire transfer: define a reusable bounded-body/framing discipline and a socket registry that can quiesce, drain, and destroy.

Readiness question: what does successful `socket.write()` prove, and what does it not prove?

## Day 3 — UDP and application-level reliability

Read Module 53. Create a table for request identity, retry attempt, peer endpoint, deadline, duplicate cache, and response correlation.

Build the Reliable Datagram Protocol. Use a controlled local socket or injected exchange to test loss, duplication, stale responses, wrong peers, and one total retry budget.

ServiceWire transfer: add optional discovery with a random nonce and an explicit trust boundary. Keep discovery out of service authorization.

Readiness question: why can a duplicate response be valid transport behavior yet invalid for the current request?

## Day 4 — HTTP message semantics

Read Module 54. Trace a request from parsed start line and headers through body consumption to response completion. Keep message framing separate from application validation.

Build the Strict HTTP Message Server. Cover `HEAD`, unsupported methods, unsupported media types, bounded bodies, malformed JSON, and response completion.

ServiceWire transfer: add the finite HTTP/1.1 adapter and stable problem-detail rendering.

Readiness question: why is “the socket closed” not an HTTP success criterion?

## Day 5 — Application protocol and idempotency

Read Module 55. Build a route table that names method, path shape, body contract, response status, and idempotency policy. Draw the idempotency record state machine.

Build the Typed HTTP Router. Test route precedence, exact path parsing, same-key/same-request replay, same-key/different-request conflict, ETags, and conditional reads.

ServiceWire transfer: implement job submission, job lookup, stats, health, idempotency fingerprints, revisions, and problem details.

Readiness question: which component is allowed to declare a submission committed?

## Day 6 — Client ownership and ambiguous commit

Read Module 56. Draw the resources owned by one client operation: agent slot, request, response, body buffer, redirect state, deadline timer, retry delay, and abort listeners.

Build the Deadline-Aware HTTP Client. Test slow headers, oversized bodies, redirects, network failure before headers, and a response that arrives after the deadline.

ServiceWire transfer: add the supported client with one total deadline, bounded response retention, idempotency-aware retries, and explicit agent shutdown.

Readiness question: when a POST times out after its bytes were sent, what fact is missing?

## Day 7 — TLS identity

Read Module 57. Create a layered table: encryption, chain trust, hostname identity, negotiated protocol, and application authorization.

Build the Local TLS Identity Lab. Test trusted localhost, wrong hostname, untrusted CA, required ALPN, and orderly TLS close. Never repair a failing identity test by disabling verification.

ServiceWire transfer: add HTTPS using checked fixture configuration and report the negotiated protocol.

Readiness question: why does trusting the issuing CA not by itself prove that the certificate names the requested service?

## Day 8 — HTTP/2 sessions and streams

Read Module 58. Draw one session containing several independently terminating streams. Mark shared session failure separately from stream-local failure.

Build the Multiplexed HTTP/2 Service. Exercise concurrent streams, body limits, stream reset, maximum concurrent streams, GOAWAY, and session closure.

ServiceWire transfer: adapt the finite application protocol to h2c for local study while keeping one domain authority.

Readiness question: why can multiplexing remove one form of head-of-line blocking while leaving capacity and flow-control problems?

## Day 9 — Long-lived HTTP delivery

Read Module 59. Trace event append, bounded retention, replay selection, subscriber registration, heartbeat, queueing, disconnect, and cleanup.

Build the Replayable SSE Channel. Test reconnect after a known event ID, replay gaps, heartbeats, slow subscribers, and server shutdown.

ServiceWire transfer: publish job transitions through the event journal and expose `/v1/events`.

Readiness question: why is a heartbeat evidence of connection activity rather than evidence that domain state is fresh?

## Day 10 — Whole-service architecture

Read Module 60. Build a complete capacity map and shutdown state machine before changing code.

Complete the Network Service Audit, then finish ServiceWire. Run the full test route and the CLI demonstration.

Finally implement the independent cancellation extension. It must preserve:

- state-machine legality;
- idempotency behavior;
- job revisions and entity tags;
- HTTP/1.1 and HTTP/2 behavior;
- SSE publication;
- client behavior;
- quiesce and shutdown semantics.

Completion question: can another engineer reconstruct the service's admission, commit, retry, replay, and terminal rules from your public types, tests, and documentation?
