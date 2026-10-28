# Reasoned Solutions — Module 65: Message Passing, Backpressure, and Shutdown

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-05-bounded-map-pipeline/README.md) · [BatchWeave guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 65: Message Passing, Backpressure, and Shutdown**. Compare the reasoning against this question: *Which values cross ownership boundaries, how is capacity bounded, and which explicit protocol event proves that every sender, receiver, and worker can terminate?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

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

## Deep reasoning and transfer

### Decisive model

> Which values cross ownership boundaries, how is capacity bounded, and which explicit protocol event proves that every sender, receiver, and worker can terminate?

Build a **channel topology**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Model channel operations as ownership transfer rather than shared access.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Choose bounded, zero-capacity, or unbounded channels from an explicit resource and latency policy.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Draw sender/receiver topology and identify which endpoints are clonable.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **State whether disconnect is normal completion, cancellation, or infrastructure failure.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Design typed messages whose terminal states cannot be confused with ordinary work.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Model channel operations as ownership transfer rather than shared access.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the channel topology.

### Reference implementation comparison

For [Bounded Map Pipeline](../../labs/module-05-bounded-map-pipeline/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In BatchWeave, Module 65 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Message Passing, Backpressure, and Shutdown**, which relationship decides this question: “Which values cross ownership boundaries, how is capacity bounded, and which explicit protocol event proves that every sender, receiver, and worker can terminate?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to BatchWeave?
