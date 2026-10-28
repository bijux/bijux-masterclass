# Module 59 Solutions — Replayable SSE

## Prediction reasoning

A cursor older than retained history cannot receive complete replay; the server must report a gap. Registering after snapshot can lose an intervening event. Journal append may continue while a subscriber is pressured, but events for that subscriber need a bounded queue. Heartbeat proves only channel activity. Replay can redeliver an event the client processed but did not durably record, so clients need idempotent handling or cursor persistence.

## Repair reasoning

SSE events end with a blank line. Encode each data line separately. Sequence IDs come from one journal authority and do not depend on wall-clock behavior.

The journal compares cursor with oldest and latest retained IDs. Gap is reported before streaming headers commit.

Eliminate the race by registering under the same synchronous authority that captures replay/high-water. Queue live events while replay is written.

When `write()` is pressured, stop writing that subscriber and queue under its independent limit. Overflow closes only that subscriber.

Cleanup disposes subscription, heartbeat participation, response listeners, and queue. Shutdown closes all subscribers and waits for their terminal owners.

## Construction notes

Encoded byte size is the useful subscriber-pressure unit. Event count can hide one huge event. Bound event payloads and track queue bytes.

A shared heartbeat interval can iterate subscribers and enqueue comments, reducing timer count. The shared timer stops when no subscribers remain or service shuts down.

Tests can use a fake writable abstraction to force pressure deterministically rather than trying to fill a real kernel socket buffer.

## Laboratory evidence

Strong tests include:

- exact wire encoding;
- multi-line data;
- absent cursor;
- replay within history;
- replay gap;
- cursor equal to latest;
- invalid future cursor;
- event appended during opening;
- pressure and drain;
- queue overflow;
- heartbeat cleanup;
- server shutdown;
- one terminal cleanup despite repeated close signals.

## ServiceWire transfer

The event journal receives events from job state transitions. The SSE adapter uses request cursor, sends finite problem before streaming on gap, and closes during runtime shutdown. Event payloads contain IDs, state, revision, and bounded result metadata—not full request payloads.

## Independent transfer

The import feed includes import ID, phase, counts, and sequence. Clients recover by fetching an import snapshot then reconnecting. History is bounded; process restart loses it. Slow subscribers are removed. Heartbeats carry no progress meaning.

## Defense summary

SSE is a protocol over a long-lived response. Correctness depends on cursor semantics, bounded replay, race-free live attachment, pressure isolation, and complete resource cleanup—not merely on repeatedly calling `write()`.

## Replay-race solution

In the copy-then-register design, the replay snapshot may end at 41. Sequence 42 can be appended before listener registration, so it is in neither the snapshot nor future listener notifications. A synchronous journal method that validates the cursor, registers the listener, and returns replay from one sequence boundary removes that gap.

A deterministic test injects a hook between snapshot and registration in the flawed implementation, appends 42 through the hook, and proves it disappears. The corrected API has no externally interleavable boundary.

At 200 bytes per event and a 1,000-byte limit, the sixth queued event would exceed capacity, so the subscriber is disconnected before retaining it. Heartbeats consume transport capacity and should be governed by the same bounded write owner even though they do not consume event sequence. Reconnect uses the last fully processed event ID; replay succeeds only while that sequence remains in history.

## Replay-window solution

Thirty seconds at forty events per second requires at least 1,200 retained events. Payload bytes are roughly 216,000 before JavaScript object, string, array, and allocator overhead. Event-count and byte bounds should both be considered. If count capacity evicts history sooner than thirty seconds, the actual supported replay window is shorter and clients receive a gap; documentation must report configured evidence rather than promise a time window the workload can invalidate.
