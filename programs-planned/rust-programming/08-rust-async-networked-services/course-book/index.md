# Course 8: Rust Async and Networked Services

**Modules 71–80 · Ten dense days · Futures, Tokio, protocols, and resilient service design**

Async Rust is often taught from the outside in: write `async fn`, call `.await`, spawn some tasks, and use a web framework. That route produces working demos quickly but leaves the reader unable to explain why a task stalled, why a timeout corrupted a frame, why memory grew under load, why a retry duplicated work, or why shutdown never completed.

This course proceeds from the inside out. You first learn the polling contract that makes async execution possible. You then place futures inside a runtime with explicit task ownership. Only after that do you cross byte-stream and socket boundaries, design protocol state machines, enforce capacity, define cancellation behavior, build an HTTP surface, and reason about retry and idempotency. The final module audits the whole service as a collection of explicit contracts.

## The course question

> How do you build a networked Rust service whose suspension, ownership, framing, protocol, capacity, cancellation, failure, retry, shutdown, and observability behavior can be explained before production traffic discovers it?

## What changes after Course 7

A thread normally blocks at a blocking operation. An async task suspends by returning `Poll::Pending`, allowing its executor thread to run other tasks. This improves scalability for waiting-heavy workloads, but it introduces a new class of design obligations:

- local variables may become state stored across suspension points;
- cancellation often occurs by dropping a future at an arbitrary suspension point;
- a spawned task may outlive the function that created it unless ownership is retained;
- one TCP read may contain half a message, one message, or several messages;
- timeouts can abandon an in-progress operation without rolling it back;
- a disconnected client may not reveal whether the server committed a request;
- an unbounded async queue can exhaust memory without blocking any OS thread;
- scheduling freedom can make timing-based tests pass or fail unpredictably.

Course 7’s ledgers remain useful, but they need async-specific extensions. This course uses:

| Ledger | Records |
|---|---|
| future-state ledger | states, stored values, wake sources, completion, and drop behavior |
| task-tree ledger | parent, child, join owner, cancellation source, and shutdown phase |
| frame ledger | buffered bytes, required bytes, maximum size, decode state, and EOF meaning |
| connection ledger | accepted socket, admission permit, protocol state, reader/writer ownership, and close path |
| capacity ledger | every place work or bytes can wait and its explicit bound |
| cancellation ledger | each suspension point, abandonability, cleanup, and commit boundary |
| retry ledger | failure class, attempt limit, deadline, idempotency key, and ambiguous-commit policy |
| service dossier | public guarantees, non-guarantees, tests, compatibility, and operational limits |

## Readiness diagnosis

You are ready when you can answer these without searching:

1. Why is `Arc<Mutex<T>>` not by itself a complete concurrency protocol?
2. What does dropping a `JoinHandle` do, and what does it not do?
3. Why can a bounded worker count still coexist with unbounded memory growth?
4. How does a condition-variable predicate loop differ from waiting for a notification?
5. What information must a binary frame length be checked against before allocation?
6. Why is a peer socket address not a durable authenticated identity?
7. What is the difference between a request identifier and an idempotency key?
8. Why can a timeout be a correctness boundary rather than only a latency setting?
9. What must be true before `unsafe impl Send` or `Sync` is defensible?
10. Which product results must remain deterministic even when completion order is not?

A weak answer to 1–4 means revisit Course 7. A weak answer to 5–6 means revisit Course 6. A weak answer to 7–10 is expected; this course develops those models.

## What you will be able to do

By the end of Course 8 you will be able to:

- derive a future’s state machine from its suspension points and stored values;
- explain `Poll`, `Context`, `Waker`, pinning, wake coalescing, and cancellation by drop;
- construct bounded Tokio task trees and observe every terminal task outcome;
- isolate blocking or CPU-heavy work from async runtime workers;
- implement bounded, incremental frame codecs over arbitrary byte chunking;
- design TCP and UDP lifecycles without inventing guarantees the transports do not provide;
- represent a protocol as explicit framing, syntax, semantics, and connection-state layers;
- calculate an end-to-end resource envelope rather than bounding only one queue;
- identify cancellation-unsafe operations and move commit points into explicit protocols;
- implement deadline propagation and phased graceful shutdown;
- construct a small Hyper service without hiding transport and body behavior behind a framework;
- define retry policy from failure classification and idempotency semantics;
- test async time, chunking, cancellation, and shutdown causally rather than probabilistically;
- defend a complete service architecture through explicit ledgers and non-guarantees.

## Ten-day route

Follow [the study plan](study-plan.md). Each day has one required chapter, one workbook, one independent laboratory, and one JobWire increment. The [reference desk](reference.md) is for recall after attempting the explanation yourself. The [final review](final-review.md) is an independent construction and defense, not a recap quiz.

## Evidence of mastery

A module is complete only when you can provide all of the following:

- a correct mechanism model in your own words;
- compiler or runtime predictions made before execution;
- a principled repair that preserves the product requirement;
- a passing independent laboratory;
- a coherent JobWire increment;
- a short defense naming guarantees, bounds, failure behavior, and non-guarantees.

Reading the chapter is preparation. The ability to reconstruct the model and apply it to an unfamiliar service is the result.

## Primary references

The course is self-contained, but it identifies primary references so claims can be checked against the language and library contracts:

- Rust standard-library `Future`, `Poll`, `Context`, `Waker`, and `Pin` documentation;
- Tokio runtime, task, synchronization, I/O, time, signal, and testing documentation;
- `bytes`, `tokio-util`, `futures-util`, Hyper, `hyper-util`, and `http-body-util` crate documentation;
- relevant Rust RFCs and standard-library network documentation where a guarantee belongs to Rust itself.

References confirm contracts. They do not replace the course’s explanation or exercises.

## Begin

Start with [Module 71: Futures, Polling, Wakers, and Async State Machines](module-71-futures-polling-wakers-and-async-state-machines/index.md).
