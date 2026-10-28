# Module 53 Solutions — UDP Reliability and Correlation

## Prediction reasoning

Two transmissions with the same nonce are attempts for one semantic request. A wrong-nonce response is unrelated and should normally be ignored, not treated as failure. A correct response after the deadline cannot satisfy the expired caller operation, though it may be counted as stale evidence. Connected UDP lacks handshake, retransmission, ordered stream delivery, congestion semantics, and peer lifecycle. A large response to a small spoofable request creates reflection/amplification risk.

## Repair reasoning

Correlation requires at least protocol version, message type, request identity, and peer policy. The completion guard must allow exactly one terminal settlement.

Retries share the same nonce because the client is asking again for the same semantic result. A new nonce would make late valid replies uncorrelatable and can duplicate effects in state-changing protocols.

Use one deadline object. Before scheduling or sending each attempt, calculate remaining time. Never schedule a delay that extends beyond it.

Malformed unrelated traffic is evidence about the environment, not necessarily the current operation. Ignore it under a bounded counter/log policy. A packet with the current nonce but an invalid required field can be treated as a peer protocol error if the peer itself is accepted.

A replay cache needs maximum entries and expiry. It should include peer identity when request IDs are only unique per client. Same ID with a different semantic fingerprint should be a conflict.

Discovery yields a candidate endpoint. The normal authenticated application protocol still verifies identity and authorization.

## Construction notes

Parsing should reject oversized bytes before UTF-8 decoding. `Buffer.toString()` replaces malformed sequences, so a strict decoder or byte-restricted ASCII grammar is preferable. The teaching discovery grammar uses ASCII tokens and hex, making strict byte validation simple.

A deterministic retry planner can produce attempt times from a start time and policy. The runtime executor then uses the same plan under one deadline. This separation makes timing tests independent of real delays.

The operation owner must remove:

- message listener;
- error listener;
- abort listener;
- attempt timers;
- deadline timer;
- socket when per-operation.

Repeated cleanup should be idempotent.

## Laboratory evidence

Strong tests inject a fake exchange or use local sockets with controlled behavior:

- drop first request;
- duplicate response;
- send stale response before correct one;
- send correct nonce from wrong peer;
- send malformed unrelated traffic;
- expire before second attempt;
- cancel while waiting;
- replay duplicate request at responder;
- overflow replay-cache capacity.

The final result must contain one endpoint or one terminal error, never several completions.

## ServiceWire transfer

The responder derives its payload from configured advertised URL and version. The server's wildcard bind must not leak into the discovery response. Discovery stops before the main runtime reports shutdown complete.

## Independent transfer

Telemetry messages need event IDs. Acknowledgments reference the ID. The sender can retry under one deadline. The receiver maintains a bounded deduplication window and must decide whether duplicate telemetry is ignored or acknowledged again. A late acknowledgment after local timeout is stale. Without authentication, endpoint and ID correlation do not prove sender identity.

## Defense summary

UDP makes message boundaries explicit while making reliability policy explicit too. A correct protocol treats loss, duplication, reordering, and unrelated traffic as ordinary possibilities and builds bounded correlation and lifecycle around them.

## Duplicate execution solution

Without a replay cache, the server executes every received attempt. The client may still observe one response. A completed-response cache prevents duplicate completed execution only after the first result is stored. Two duplicates arriving while the first is running can still execute twice unless an in-progress record reserves the nonce and lets later requests attach or wait.

A read-only status query tolerates repeated execution, so correlation plus bounded retries may be sufficient. A mutating command needs receiver-side idempotency if the product promises one semantic commit.

Malformed datagrams are classified and discarded without retaining payloads. Counters should use fixed labels such as `malformed`, `duplicate`, and `unrelated`; peer addresses should not become metric labels. The source tuple remains routing evidence, never authorization.

## Retry-schedule solution

One defensible schedule is sends at 0, 60, 160, and 300 ms with the overall deadline at 500 ms. Every timer is derived from that absolute deadline and cleared by one idempotent completion path. A LAN diagnostic may use short intervals because latency is predictably low and the operation is read-only. An internet-facing mutation needs receiver-side idempotency, authentication, amplification controls, and more conservative timing; using HTTP or another established reliable protocol is often the better design.
