# Course 8 Study Plan — Rust Async and Networked Services

Ten dense study days fit into two calendar weeks. The goal is not to maximize reading time; it is to make **How do suspension, wakeup, task ownership, framing, protocol state, capacity, cancellation, retry, and shutdown remain explicit when peers and timing are only partly observable?** answerable through construction and explanation.

## Daily rhythm

Use a **async service dossier** across the course. Each day begins by reconstructing yesterday’s decisive relationship and ends by tracing one capstone invariant. Preserve the first prediction, the observed result, the principled repair, and the shortcut you rejected.

## Day 1 — Module 71: Futures, Polling, Wakers, and Async State Machines

**Question:** What exactly is an async computation before a runtime executes it, what must happen when it cannot complete, and what state remains when it is suspended or cancelled?

**Retrieval:** Without notes, restate the invariant carried from Module 70 — Integrated Concurrent Architecture, Testing, and Audit. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 71](./module-71-futures-polling-wakers-and-async-state-machines/index.md) with a **future state and wake-source table** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-71-futures-polling-wakers-and-async-state-machines/workbook.md) before observation. The day’s minimum result is: **Explain why a future is inert until polled.** Keep one positive case and one causal negative case.

**Laboratory:** Build [One-Shot Signal](../labs/module-01-one-shot-signal/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 71 in the [JobWire guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Explain why a future is inert until polled.** End with one simpler design that would be preferable under a narrower requirement.

## Day 2 — Module 72: Tokio Runtimes, Tasks, and Structured Async Lifecycles

**Question:** Once futures are understood as poll-driven state machines, how should a runtime own, schedule, observe, cancel, and finish the tasks that execute them?

**Retrieval:** Without notes, restate the invariant carried from Module 71 — Futures, Polling, Wakers, and Async State Machines. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 72](./module-72-tokio-runtimes-tasks-and-structured-async-lifecycles/index.md) with a **task ownership tree** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-72-tokio-runtimes-tasks-and-structured-async-lifecycles/workbook.md) before observation. The day’s minimum result is: **Distinguish a runtime, worker thread, task, future, reactor, and blocking pool.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Task Nursery](../labs/module-02-task-nursery/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 72 in the [JobWire guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Distinguish a runtime, worker thread, task, future, reactor, and blocking pool.** End with one simpler design that would be preferable under a narrower requirement.

## Day 3 — Module 73: Async I/O, Buffers, Streams, and Framing

**Question:** How do arbitrary, partial byte transfers become complete bounded messages without confusing readiness, reads, buffers, frames, or protocol meaning?

**Retrieval:** Without notes, restate the invariant carried from Module 72 — Tokio Runtimes, Tasks, and Structured Async Lifecycles. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 73](./module-73-async-io-buffers-streams-and-framing/index.md) with a **buffer and frame ledger** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-73-async-io-buffers-streams-and-framing/workbook.md) before observation. The day’s minimum result is: **Distinguish readiness from transfer completion.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Bounded Length Codec](../labs/module-03-bounded-length-codec/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 73 in the [JobWire guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Distinguish readiness from transfer completion.** End with one simpler design that would be preferable under a narrower requirement.

## Day 4 — Module 74: TCP, UDP, DNS, and Connection Lifecycles

**Question:** What lifecycle does each network transport actually provide, and where should connection admission, name resolution, deadlines, half-close, datagram loss, and peer identity be represented?

**Retrieval:** Without notes, restate the invariant carried from Module 73 — Async I/O, Buffers, Streams, and Framing. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 74](./module-74-tcp-udp-dns-and-connection-lifecycles/index.md) with a **connection lifecycle map** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-74-tcp-udp-dns-and-connection-lifecycles/workbook.md) before observation. The day’s minimum result is: **Distinguish bind, listen, accept, connect, resolve, read, write, half-close, and full close.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Deadline Echo Service](../labs/module-04-deadline-echo-service/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 74 in the [JobWire guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Distinguish bind, listen, accept, connect, resolve, read, write, half-close, and full close.** End with one simpler design that would be preferable under a narrower requirement.

## Day 5 — Module 75: Protocol State Machines, Versioning, and Defensive Parsing

**Question:** Once frames arrive intact, how do they become legal protocol messages whose meaning depends on version, connection state, request identity, and error scope?

**Retrieval:** Without notes, restate the invariant carried from Module 74 — TCP, UDP, DNS, and Connection Lifecycles. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 75](./module-75-protocol-state-machines-versioning-and-defensive-parsing/index.md) with a **protocol transition table** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-75-protocol-state-machines-versioning-and-defensive-parsing/workbook.md) before observation. The day’s minimum result is: **Separate framing, text decoding, syntax parsing, semantic validation, state legality, and application execution.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Negotiated Command Protocol](../labs/module-05-negotiated-command-protocol/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 75 in the [JobWire guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Separate framing, text decoding, syntax parsing, semantic validation, state legality, and application execution.** End with one simpler design that would be preferable under a narrower requirement.

## Midpoint reconstruction

Do not add a sixth topic on the recovery day. Reconstruct **Futures, Polling, Wakers, and Async State Machines, Tokio Runtimes, Tasks, and Structured Async Lifecycles, Async I/O, Buffers, Streams, and Framing, TCP, UDP, DNS, and Connection Lifecycles, Protocol State Machines, Versioning, and Defensive Parsing** as one dependency chain, rerun the two investigations that changed your model most, and describe the current JobWire state from an empty page. Repair incomplete work, then take a real break; consolidation is part of the course rather than unused time.

## Day 6 — Module 76: Backpressure, Admission Control, and Fair Work Distribution

**Question:** When demand exceeds service capacity, where may work wait, which bound is authoritative, and how does overload become an explicit product outcome instead of memory growth, latency collapse, or starvation?

**Retrieval:** Without notes, restate the invariant carried from Module 75 — Protocol State Machines, Versioning, and Defensive Parsing. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 76](./module-76-backpressure-admission-control-and-fair-work-distribution/index.md) with a **capacity and admission ledger** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-76-backpressure-admission-control-and-fair-work-distribution/workbook.md) before observation. The day’s minimum result is: **Find every accumulation point in an async service.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Bounded Relay Broker](../labs/module-06-bounded-relay-broker/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 76 in the [JobWire guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Find every accumulation point in an async service.** End with one simpler design that would be preferable under a narrower requirement.

## Day 7 — Module 77: Cancellation Safety, Deadlines, and Graceful Shutdown

**Question:** When an async operation loses a race, exceeds a deadline, or receives shutdown, what state survives, which effects may already have committed, and how does every task reach a terminal joined state?

**Retrieval:** Without notes, restate the invariant carried from Module 76 — Backpressure, Admission Control, and Fair Work Distribution. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 77](./module-77-cancellation-safety-deadlines-and-graceful-shutdown/index.md) with a **cancellation and shutdown trace** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-77-cancellation-safety-deadlines-and-graceful-shutdown/workbook.md) before observation. The day’s minimum result is: **Derive cancellation behavior from future-owned state and external side effects.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Graceful Task Tree](../labs/module-07-graceful-task-tree/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 77 in the [JobWire guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Derive cancellation behavior from future-owned state and external side effects.** End with one simpler design that would be preferable under a narrower requirement.

## Day 8 — Module 78: HTTP Services with Hyper: Requests, Bodies, and Connections

**Question:** How do you build a small HTTP service while keeping transport ownership, HTTP connection driving, request-body policy, routing, application state, and health semantics separate?

**Retrieval:** Without notes, restate the invariant carried from Module 77 — Cancellation Safety, Deadlines, and Graceful Shutdown. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 78](./module-78-http-services-with-hyper-requests-bodies-and-connections/index.md) with a **HTTP boundary map** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-78-http-services-with-hyper-requests-bodies-and-connections/workbook.md) before observation. The day’s minimum result is: **Distinguish accepted transport, HTTP connection future, request future, body stream, and application service.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Hyper Health Surface](../labs/module-08-hyper-health-surface/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 78 in the [JobWire guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Distinguish accepted transport, HTTP connection future, request future, body stream, and application service.** End with one simpler design that would be preferable under a narrower requirement.

## Day 9 — Module 79: Network Failure, Idempotency, Retries, and Deterministic Testing

**Question:** When a network operation fails without revealing whether the remote side committed it, how do idempotency, retry budgets, failure classification, and deterministic tests preserve one semantic outcome?

**Retrieval:** Without notes, restate the invariant carried from Module 78 — HTTP Services with Hyper: Requests, Bodies, and Connections. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 79](./module-79-network-failure-idempotency-retries-and-deterministic-testing/index.md) with a **retry and commit matrix** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-79-network-failure-idempotency-retries-and-deterministic-testing/workbook.md) before observation. The day’s minimum result is: **Classify failures by phase, scope, retryability, and commit ambiguity.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Idempotent Retry Client](../labs/module-09-idempotent-retry-client/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 79 in the [JobWire guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Classify failures by phase, scope, retryability, and commit ambiguity.** End with one simpler design that would be preferable under a narrower requirement.

## Day 10 — Module 80: Integrated Async Service Architecture, Testing, and Audit

**Question:** Can the complete service be explained as one coherent set of lifecycle, protocol, capacity, cancellation, failure, compatibility, and operational contracts rather than as a pile of async APIs?

**Retrieval:** Without notes, restate the invariant carried from Module 79 — Network Failure, Idempotency, Retries, and Deterministic Testing. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 80](./module-80-integrated-async-service-architecture-testing-and-audit/index.md) with a **async service dossier** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-80-integrated-async-service-architecture-testing-and-audit/workbook.md) before observation. The day’s minimum result is: **Construct a complete async service dossier.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Async Service Audit](../labs/module-10-async-service-audit/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 80 in the [JobWire guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Construct a complete async service dossier.** End with one simpler design that would be preferable under a narrower requirement.

## Final integration

After Day 10, complete the [final review](final-review.md), run the strongest available course route, and implement this unseen capstone change: **Add one streaming JobWire operation with an explicit per-stream capacity and cancellation contract while preserving protocol versioning and service shutdown.**

Seven days later, rebuild the ten-module sequence and the core **async service dossier** without the book. Write a fresh example for every relationship you cannot recover. Re-reading a solution without recreating the model does not count as retained learning.
