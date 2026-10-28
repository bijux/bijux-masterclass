# Module 53 Workbook — UDP Reliability and Correlation

## 1. Predict

1. A client sends one datagram twice with the same nonce. Is that one semantic request or two?
2. A syntactically valid response arrives with the wrong nonce. Should it fail the operation?
3. A correct response arrives after the operation deadline. Can it complete the caller's promise?
4. A UDP socket is “connected.” Which TCP properties remain absent?
5. A 20-byte request causes a 20-kilobyte response. What security concern appears?

## 2. Diagnose and repair

- Replace “first datagram wins” with correlation and peer policy.
- Replace a new nonce per retry with stable semantic identity.
- Replace a full timeout per attempt with one deadline.
- Prevent unrelated malformed traffic from terminating the operation.
- Bound a replay cache and define same-ID/different-payload conflict.
- Separate discovery result from authorization.

## 3. Focused construction

1. Encode and decode versioned discovery messages.
2. Generate and validate a 128-bit hex nonce.
3. Implement a deterministic retry planner.
4. Correlate by nonce and accepted peer.
5. Ignore stale and duplicate responses.
6. Add a bounded replay cache.
7. Track attempts without changing semantic identity.
8. Close all timers, listeners, and sockets on every terminal path.

## 4. Independent laboratory

Build the [Reliable Datagram Protocol](../../labs/module-53-reliable-datagram-protocol/README.md).

## 5. ServiceWire transfer

Implement local discovery with strict bounds. Add tests for wrong nonce, malformed response, duplicate response, timeout, cancellation, and clean shutdown.

## 6. Independent transfer

Design a UDP telemetry acknowledgment protocol. State which messages can be retried, how duplicates are detected, how late acknowledgments are classified, and what remains unauthenticated.

## 7. Closed-book defense

1. Which guarantee does UDP add compared with TCP's byte stream?
2. Which guarantees does it not add?
3. Why should retransmissions retain request identity?
4. When should malformed traffic be ignored versus terminal?
5. What makes a replay cache bounded?

## 8. Duplicate execution analysis

Model a three-attempt UDP command where attempts one and two reach the server but only the third response reaches the client. Calculate the number of client-visible responses, server executions, replay-cache lookups, and semantic commits under:

- no replay cache;
- a completed-response cache;
- an in-progress record that duplicate requests attach to.

State which design is sufficient for a read-only query and which is required for a mutating command.

## 9. Malformed-traffic budget

Design a receiver that processes at most 512-byte datagrams and retains no malformed payload bytes after classification. Specify counters for ignored, malformed, new, duplicate, and replied datagrams. Explain how those counters can remain bounded-cardinality and why source address must not become authorization.

## 10. Retry-schedule construction

Construct retry times for a 500 ms deadline with at most four attempts. The schedule must leave time for a final response and must not create a timer after settlement. Show the absolute deadline, each send time, and the latest acceptable response time. Then alter the schedule for a high-loss LAN diagnostic versus an internet-facing mutating operation and explain why the latter should probably not use UDP without a stronger protocol.
