# Ten-Day Study Plan

Course 8 is designed as ten dense days across two weeks. Each day assumes roughly eight to ten focused hours, including breaks. The schedule is demanding because async and network correctness deteriorate when concepts are sampled casually without constructing and testing complete protocols.

## Daily operating method

| Time | Work |
|---|---|
| 08:30–09:00 | Closed-book reconstruction of yesterday’s model |
| 09:00–10:30 | Read the authoritative chapter and reproduce its diagrams |
| 10:45–12:15 | Freeze compiler, runtime, and protocol predictions |
| 13:15–14:45 | Diagnose and repair the worked defect |
| 15:00–17:00 | Build the independent laboratory |
| 17:15–18:30 | Implement the JobWire increment |
| 19:30–20:15 | Run causal tests and inspect failure paths |
| 20:15–20:45 | Write guarantees, non-guarantees, and tomorrow’s retrieval questions |

Do not extend the day by replacing sleep with more reading. Suspension, ordering, and lifecycle reasoning degrade quickly under fatigue, and timing-based intuition becomes especially unreliable.

**Week 1**

## Day 1 — Module 71

Construct a future-state ledger. Implement a one-shot signal future and prove that `Pending` stores the latest waker without waking unconditionally. Add JobWire’s protocol-independent async vocabulary.

## Day 2 — Module 72

Build a task nursery that observes success, domain failure, panic, and cancellation. Add JobWire’s owned task tree and isolate blocking work.

## Day 3 — Module 73

Implement a bounded length-delimited codec and test every split point. Add JobWire’s incremental framing layer.

## Day 4 — Module 74

Build a deadline-aware echo service with bounded admissions and explicit close behavior. Add JobWire’s TCP listener and connection lifecycle.

## Day 5 — Module 75

Implement a negotiated command protocol whose legal messages depend on connection state. Add JobWire’s handshake, version, request, and response models.

### Weekend consolidation

Do not add new mechanisms. Rebuild the one-shot future and codec from a blank file. Draw JobWire’s task tree and connection state machine without notes. Re-run frame tests under one-byte input chunks. Explain why TCP completion, protocol completion, and application commit are three different events.

**Week 2**

## Day 6 — Module 76

Build a bounded relay broker and calculate its complete resource envelope. Add JobWire’s admission, broker queue, active-job permits, and overload responses.

## Day 7 — Module 77

Build a graceful task tree with cancellation tokens, deadlines, drain, abort, and join phases. Add JobWire’s shutdown controller and cancellation-safe request handling.

## Day 8 — Module 78

Build a small Hyper health surface with bounded bodies and explicit response types. Add JobWire’s `/health` and `/stats` endpoints without mixing HTTP and broker logic.

## Day 9 — Module 79

Build an idempotent retry client against a deterministic scripted server. Add JobWire’s idempotency records, retry classification, and paused-time tests.

## Day 10 — Module 80

Complete the JobWire service dossier, adversarial test matrix, and final architecture defense. Build the independent service-audit laboratory without copying the capstone.

## When to stop and repair

Do not continue to the next module when any of these remain vague:

- which event causes another poll;
- who owns and joins a spawned task;
- how many bytes may be buffered;
- which protocol states exist;
- where overload is rejected;
- what dropping a future leaves behind;
- whether a timed-out operation may already have committed;
- whether a health response is authoritative or advisory.

Use the workbook’s reconstruction questions to locate the missing model, then return to the exact chapter section. More API examples will not repair an unclear contract.

## Daily deliverables

Do not measure a day only by pages read or tests made green. Preserve these artifacts in a course notebook or beside the code:

| Day | Required written artifact | Required executable evidence |
|---:|---|---|
| 1 | future-state table with every wake source and terminal path | producer-first, receiver-first, replacement-waker, and cancellation tests |
| 2 | task tree naming each join owner and panic boundary | one terminal outcome for every accepted child |
| 3 | byte grammar and buffer-state trace at every split point | exhaustive partition and truncated-EOF tests |
| 4 | connection lifecycle from accept through final close | bounded admission, idle deadline, write deadline, and shutdown tests |
| 5 | protocol transition table and error-scope table | total transition tests for every state/message pair |
| 6 | capacity ledger with units, bounds, and overload behavior | saturation tests that place work at mailbox, queue, and active limits |
| 7 | cancellation ledger for every selected or timed operation | cooperative drain, grace expiry, abort, and complete join tests |
| 8 | HTTP layer map from listener to application snapshot | body-bound, method/path, health-state, and connection-drain tests |
| 9 | failure classification and idempotency state table | ambiguous-commit, cached-result, key-conflict, deadline, and retry-count tests |
| 10 | complete service dossier and one end-to-end request trace | independent service build plus adversarial shutdown and overload runs |

The written artifact is not decoration. It gives you something precise to compare against the implementation when a test exposes a mistaken assumption.

## End-of-week gates

At the end of Day 5, stop unless you can reconstruct all of the following from a blank page:

1. a future that stores the latest waker and completes under either producer order;
2. a task owner that distinguishes domain failure from join failure;
3. a frame decoder that consumes nothing until a complete bounded frame exists;
4. a TCP connection lifecycle that names all close and timeout paths;
5. a protocol state machine whose parser and transition function have separate responsibilities.

At the end of Day 10, stop unless you can trace one request through:

```text
socket admission
→ frame buffering
→ syntax parsing
→ protocol-state validation
→ broker admission
→ semantic commit
→ active execution
→ terminal record
→ response write
→ connection or retry outcome
```

At every arrow, state who owns the data, what is bounded, what cancellation can destroy, and whether the semantic operation may already have committed.

## Working with virtual time

Paused time is useful only after the event that arms a timer has definitely occurred. A reliable test sequence is:

1. start the operation;
2. use a channel, notification, snapshot, or explicit yield to prove it reached the intended state;
3. advance time by a controlled amount;
4. assert both what has happened and what has not happened;
5. join the task and inspect the semantic outcome.

Advancing time immediately after spawning a task can test the scheduler accident rather than the protocol. Real sleeps remain acceptable as an outer hang detector, but they should not be the evidence that a deadline or retry policy is correct.

## How to use reference implementations

Open a reference only after writing your own invariant and a precise blocker. Compare in this order:

1. public contract and bounds;
2. ownership of tasks, buffers, sockets, and reply channels;
3. commit and cancellation points;
4. terminal accounting;
5. adversarial tests;
6. syntax and convenience methods.

A shorter implementation is not automatically better. An implementation that makes overload, failure, and shutdown impossible to explain is weaker even when its happy-path output is correct.
