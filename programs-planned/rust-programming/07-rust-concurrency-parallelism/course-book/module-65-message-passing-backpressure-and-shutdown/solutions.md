# Reasoned solutions — Module 65: Message Passing, Backpressure, and Shutdown

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the BatchWeave guide](../capstone.md)

A channel solution is strong only when ownership transfer, capacity, endpoint topology, and terminal state form one protocol. Merely replacing a mutex with send/receive can hide unbounded memory or make shutdown dependent on an accidentally retained clone.

The answers below are reasoning models, not scripts to imitate. A different implementation can be stronger when it proves the same contract more directly. Compare ownership, synchronization, progress, failure, and determinism—not only surface syntax.

## Part 1 — Prediction solutions

### Prediction 1

The sender blocks on capacity while retaining the mutex; the receiver needs the mutex before it can drain, so progress stops. Finish and unlock the state transition before sending, or redesign the receiver not to require that lock.

### Prediction 2

The receiver never observes disconnect because one sender remains alive. Drop the coordinator and auxiliary clones at the defined phase boundary.

### Prediction 3

Disconnect only proves no senders remain. It does not prove every job produced an outcome. Join workers and reconcile indexed jobs with received terminal events.

### Prediction 4

Append order follows schedule. Carry source index and place or sort by that index before rendering.

### Prediction 5

The channel API does not impose a fixed queue bound; memory may grow toward a terabyte. Bound accepted jobs, payload bytes, or use a bounded queue with backpressure.

### Prediction 6

One worker consumes the sentinel; the other three can block forever. Use channel/queue closure as broadcast lifecycle state or send an exactly accounted terminal command per worker.

### Prediction 7

The sender still owns the job after failure. Discarding it loses the requirement to report, retry, cancel, or clean up that job explicitly.

### Prediction 8

The receiver is not clonable. Use one dispatcher, per-worker channels, a shared protected queue, or a third-party MPMC channel when the architecture justifies it.

## Part 2 — Repair reasoning

The two bounded channels create a cycle because the coordinator is both exclusive work producer and result consumer. A dedicated collector can drain results while submission continues, or an unbounded result channel can be acceptable when a strict input bound caps total result messages. Work remains bounded to apply backpressure. Shutdown should close work rather than rely on strings, drop every result sender, drain terminal events, join all workers, and reconcile missing outcomes.

## Part 3 — Focused construction guidance

### Construction 1

The topology document should show coordinator-owned work senders, worker-owned result clones, the unique result receiver, and exact drop points. No anonymous clone may survive shutdown.

### Construction 2

Capacity must bound queued ownership and interact safely with the result path. Payload limits and accepted-job limits complete the memory argument. A send cannot occur while holding a resource required by a receiver.

### Construction 3

Use distinct enum variants or typed outcome structures. Panic is not a domain error; infrastructure failure may affect multiple jobs; cancellation is a terminal outcome for reconciliation.

### Construction 4

Allocate `Vec<Option<Outcome>>`, validate each index, reject duplicates, fill slots, and convert missing slots into explicit faults or cancellations after workers terminate.

### Construction 5

Each path closes work, stops submission, ensures result senders eventually drop, drains what can arrive, joins all workers, and marks every unobserved job. Zero jobs still starts and shuts down cleanly or avoids workers by an explicit fast path.

## Part 4 — Laboratory comparison

Compare the topology rather than only the mapping result. A strong reference has bounded work, stable indices, no lock held during send, all handles joined, and a defined disconnect meaning. Test one failed worker and verify that missing results do not masquerade as success.

## Part 5 — Capstone comparison

BatchWeave’s result channel is intentionally unbounded at the library level but bounded at the product level by maximum manifest jobs and small outcome payloads. The documentation must state both facts. The coordinator rejects duplicate indices and does not infer completion from channel disconnect alone.

## Part 6 — Reconstruction and defense

The defense should identify every endpoint owner, the meaning of capacity, the cause of disconnect, and the complete shutdown sequence. It should show a wait-cycle analysis and explain how stable source identity produces deterministic output without constraining completion order.

A strong defense states what is guaranteed for every allowed schedule, what is merely likely on one machine, and what the design intentionally leaves unspecified.
