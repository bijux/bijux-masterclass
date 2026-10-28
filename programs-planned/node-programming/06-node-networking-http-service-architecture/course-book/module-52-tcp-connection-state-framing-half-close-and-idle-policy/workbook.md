# Module 52 Workbook — TCP Framing and Connection State

## 1. Predict

1. A client performs two `write()` calls. List three legal read partitions.
2. The decoder has received two bytes of a four-byte prefix when EOF arrives. Is this clean close?
3. A peer half-closes its write direction after sending a complete request. May the server still write a response?
4. `socket.write(frame)` returns false. Should the frame be written again?
5. The listening server closes while two accepted sockets remain open. Is shutdown complete?

## 2. Diagnose and repair

- Replace code that treats each `'data'` chunk as one message.
- Move a length check before allocation.
- Add finalization that rejects partial prefix and partial payload.
- Separate peer EOF from local write completion.
- Replace a timeout listener that logs and leaves the socket open.
- Add a registry that removes sockets only on observed close.

For each repair, state the exact product property restored.

## 3. Focused construction

1. Implement `encodeFrame(payload)`.
2. Implement an incremental decoder with a four-byte big-endian prefix.
3. Support several frames per chunk and frames split across many chunks.
4. Enforce `maxFrameBytes` before allocation.
5. Define empty-frame behavior.
6. Implement `finish()` with precise truncation errors.
7. Build a server that returns a framed uppercase response.
8. Add a connection limit and idle policy.
9. Track all sockets through shutdown.

## 4. Independent laboratory

Build the [Bounded TCP Frame Server](../../labs/module-52-bounded-tcp-frame-server/README.md). Generate chunk partitions rather than trusting ordinary localhost packetization.

## 5. ServiceWire transfer

Add connection tracking and bounded body accumulation to the HTTP server skeleton. Document which TCP terminal facts later become HTTP request failures and which remain transport diagnostics.

## 6. Independent transfer

Design a protocol with one fixed header and two variable sections. Show how your state machine rejects arithmetic overflow, truncation, and an over-limit second section before allocation.

## 7. Closed-book defense

1. What does TCP preserve?
2. What must framing add?
3. What does EOF mean in each decoder state?
4. What is half-close?
5. What does writable pressure prove?
6. Who owns accepted sockets after the listener closes?

## 8. Exhaustive chunk-partition test

Encode three frames: empty payload, one-byte payload, and a multibyte UTF-8 payload. For every split point in the complete wire bytes, feed the left and right chunks separately and prove that output is identical. Extend the test to every pair of split points. Record how many partitions are exercised and why this remains tractable for a small fixture.

## 9. Connection-state defense

Given a peer that sends one complete frame, half-closes, and reads slowly, draw the socket’s read state, write state, decoder state, and response-queue state until close. Identify the exact owner that may destroy the socket if the response queue fails. Explain why `end`, `finish`, and `close` are not interchangeable evidence.

## 10. Memory-retention investigation

Compare three decoder designs:

- repeatedly concatenate pending bytes;
- keep a list of chunks and consume through offsets;
- keep subarray views into one large input buffer.

For each design, state copying cost, retained backing memory, implementation complexity, and the maximum memory claim you can honestly make. Choose one for a 64 KiB teaching protocol and one for a high-throughput production parser. The answer must include the workload assumptions that justify the choice.
