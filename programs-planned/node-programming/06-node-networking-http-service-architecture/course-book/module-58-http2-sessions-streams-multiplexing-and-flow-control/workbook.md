# Module 58 Workbook — HTTP/2 Sessions and Streams

## 1. Predict

1. Three streams share one session. One stream resets. Must the others fail?
2. A peer advertises a high concurrent-stream setting. May the application admit unlimited jobs?
3. GOAWAY is sent. Are all active streams complete?
4. Two streams each buffer the maximum body. What capacity equation matters?
5. A job commits, then its stream resets before response completion. Is the job rolled back?

## 2. Diagnose and repair

- Separate session and stream registries.
- Move application validation out of the raw stream handler.
- Add per-stream body bounds.
- Add global application request admission.
- Respect stream write pressure.
- Keep stream-local errors local.
- Implement GOAWAY, grace, and forced destruction.
- Remove completion-order assumptions from tests.

## 3. Focused construction

1. Start an h2c server.
2. Normalize pseudo-headers.
3. Build bounded request bodies.
4. Reuse the typed application dispatcher.
5. Open several concurrent client streams.
6. Reset one stream.
7. observe session and stream events separately.
8. Apply maximum concurrent streams.
9. Drain with GOAWAY.
10. Force close after grace.

## 4. Independent laboratory

Build the [Multiplexed HTTP/2 Service](../../labs/module-58-multiplexed-http2-service/README.md).

## 5. ServiceWire transfer

Add h2c finite endpoints without duplicating domain logic or problem-code behavior.

## 6. Independent transfer

Design a TLS-negotiated HTTP/2 client that requires ALPN `h2`, limits concurrent streams, and reconciles submission reset with idempotency.

## 7. Closed-book defense

1. What belongs to a session?
2. What belongs to a stream?
3. What are the three pressure layers?
4. What does GOAWAY do?
5. Why does application admission remain separate?

## 8. Multiplexing trace

Open one session with three streams: a fast health request, a slow request, and an oversized upload. Predict each stream’s terminal result and whether the session remains usable. Record stream IDs rather than completion positions.

Then initiate server shutdown while the slow request is active. Draw the sequence from quiesce through GOAWAY, stream completion or reset, session close, and listener close.

## 9. Capacity decomposition

Given limits of two sessions and four streams per session, list the outcomes for:

- a third session;
- a fifth stream on an existing session;
- a valid stream whose application job capacity is full;
- a body that exceeds the per-stream byte limit.

Explain which layer owns each rejection and why one shared “overloaded” flag is insufficient.

## 10. Stream-local versus session-wide failure

Classify these events: malformed application JSON, oversized stream body, stream reset, invalid connection preface, session error, GOAWAY, and job-capacity rejection. For each, identify whether the correct response is an application problem on one stream, a stream reset, graceful session action, or session destruction. Support every classification with the layer whose invariant was violated.
