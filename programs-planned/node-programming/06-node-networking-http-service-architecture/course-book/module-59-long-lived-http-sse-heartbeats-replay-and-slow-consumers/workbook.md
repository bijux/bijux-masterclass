# Module 59 Workbook — Replayable SSE

## 1. Predict

1. A client reconnects after an event older than the journal's oldest retained ID. Can the server provide complete replay?
2. An event is appended between replay snapshot and subscriber registration. What failure occurs?
3. `response.write()` returns false. May the journal continue appending events?
4. A heartbeat arrives. Does it prove a job is progressing?
5. The client processed an event but disconnected before persisting its cursor. Can replay deliver it again?

## 2. Diagnose and repair

- Add blank-line event termination.
- Split multi-line data correctly.
- Replace timestamp IDs with monotonic sequence IDs.
- Detect replay gaps.
- Close the replay-to-live race.
- Add per-subscriber queued-byte limits.
- Wait for `'drain'`.
- Remove all subscription and heartbeat resources on close.
- Integrate server shutdown.

## 3. Focused construction

1. Implement SSE encoding.
2. Build a bounded event journal.
3. Select replay after a cursor.
4. Make subscription opening race-free.
5. Implement heartbeat comments.
6. Bound subscriber count.
7. Bound queued bytes.
8. Remove slow subscribers.
9. Test reconnect and deduplication.
10. Close all subscribers.

## 4. Independent laboratory

Build the [Replayable SSE Channel](../../labs/module-59-replayable-sse-channel/README.md).

## 5. ServiceWire transfer

Publish bounded job transition events and expose `/v1/events`. Keep SSE out of HTTP/2 in the base capstone.

## 6. Independent transfer

Design an SSE progress feed for a file import. Define event schema, snapshot recovery, replay window, slow subscriber policy, heartbeat, and restart limitations.

## 7. Closed-book defense

1. What commits an SSE event on the wire?
2. What does an event ID mean?
3. How is replay gap detected?
4. How is the replay-to-live race removed?
5. Why are journal and subscriber bounds separate?

## 8. Replay race

An event with sequence 42 is appended while a reconnecting subscriber requests events after 40. Compare two implementations:

1. copy replay events, then register listener;
2. validate cursor, register listener, and derive replay under one synchronous journal authority.

Show exactly how implementation one can lose sequence 42. Specify a test that forces the race without relying on random timing.

## 9. Slow-consumer budget

Assume each encoded event is 200 bytes, the queue limit is 1,000 bytes, and `write()` remains backpressured. Determine when the subscriber must be disconnected. Explain whether heartbeats count toward the same queue and what evidence remains for reconnect and replay.

## 10. Replay-window sizing

Given an event rate of 40 events per second, an average encoded size of 180 bytes, and a desired 30-second reconnect window, calculate minimum retained events and approximate payload bytes. Add array/object overhead as an explicit unknown rather than pretending the byte estimate is total process memory. Then decide what happens when the configured event-count bound is reached before the desired time window.
