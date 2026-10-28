# Reasoned Solutions — Module 74: TCP, UDP, DNS, and Connection Lifecycles

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the JobWire guide](../capstone.md)

The governing correction is that transport events are evidence with limited scope. Accept is not admission policy, write is not commit, address is not identity, and timeout is not rollback.

## Part 1 — Prediction solutions

1. No. The backlog concerns pending handshakes and is platform-dependent. Accepted sockets and spawned tasks remain unbounded without application policy.
2. No. It proves only that the local stack accepted the bytes for transmission under the socket contract.
3. The peer closed its sending direction. The local side may still write unless another failure closes the connection.
4. Up to roughly DNS plus four connect budgets plus handshake—about thirty seconds—rather than one five-second overall budget.
5. No. It fixes/defaults the peer and filters by address; UDP still permits loss, reordering, duplication, and address spoofing within the network threat model.
6. The service can spawn unbounded tasks and accept unbounded sockets that wait for permits.
7. It can send one byte before each timeout and never produce a complete valid frame. Count meaningful progress instead.
8. No. Reader, permit, cancellation, and join obligations remain.

## Part 2 — Repair reasoning

The transport repair creates one overall deadline, records resolution separately, attempts a defined candidate policy, and reports connect versus handshake failure. It does not claim that a timeout after write means “not committed.” That ambiguity survives until the protocol adds idempotency or status recovery.

## Part 3 — Focused exercise guidance

Permit-before-accept keeps accepted live sockets tightly bounded but can leave clients queued in the OS backlog. Accept-then-try-permit can return a deliberate busy response but must bound the accepted socket window. Neither choice is universally best; state the overload contract.

A half-close test proves directional semantics. The UDP design must make loss an accepted product behavior or add an explicit reliability layer. A complete connection ledger ends only after both I/O directions, children, and permits terminate.

## Part 4 — Laboratory comparison

A strong echo service uses a tracked task set and an admission permit owned by each connection. Timeouts are causal branches, not sleeps in tests. Shutdown stops admission, signals connections, and drains joins. The lab remains an echo product; it should not conceal framing assumptions behind convenient small writes.

## Part 5 — Capstone comparison

JobWire’s listener owns the accept loop, while a connection set owns child tasks. The permit must move into the child and release on every return or panic. Handshake timeout is distinct from later idle and request deadlines. Accept failures should not be retried in a tight unbounded loop.

## Part 6 — Reconstruction and defense

A complete defense names the transport guarantee precisely and then names the missing application guarantee. It distinguishes capacity before and after accept, directional EOF, overall deadline propagation, UDP datagram semantics, and the single lifecycle owner that coordinates split I/O halves.
