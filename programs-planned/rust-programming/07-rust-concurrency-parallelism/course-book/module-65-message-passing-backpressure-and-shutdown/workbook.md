# Workbook — Module 65: Message Passing, Backpressure, and Shutdown

[Chapter](index.md) · [Laboratory](../../labs/module-05-bounded-map-pipeline/README.md) · [BatchWeave guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Message Passing, Backpressure, and Shutdown** has become a usable model rather than remembered vocabulary. Its governing question is: *Which values cross ownership boundaries, how is capacity bounded, and which explicit protocol event proves that every sender, receiver, and worker can terminate?* Preserve your first prediction and record decisive facts in a **channel topology**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 64 — Coordination: Condvars, Barriers, and Phase Protocols that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **Which values cross ownership boundaries, how is capacity bounded, and which explicit protocol event proves that every sender, receiver, and worker can terminate?**
3. Draw the smallest **channel topology** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

### Prediction 1

A bounded work send occurs while holding a mutex the receiver needs to process work. Predict the wait cycle.

Record: **resource graph and smallest repair**.

### Prediction 2

The coordinator retains one unused `Sender` clone while looping on `recv` until disconnect. Predict termination.

Record: **endpoint ownership and lifecycle**.

### Prediction 3

A worker panics and drops its result sender. The coordinator interprets disconnect as successful completion. Predict the missing evidence.

Record: **disconnect cause and outcome accounting**.

### Prediction 4

Two workers send completed values without source indices. The receiver appends them. Predict output stability.

Record: **schedule-dependent order and identity repair**.

### Prediction 5

An unbounded channel accepts one million 1 MiB messages faster than consumers process them. What is bounded?

Record: **queue and payload resource analysis**.

### Prediction 6

One `Stop` sentinel is sent to four workers sharing an MPMC queue. Predict shutdown.

Record: **terminal-message cardinality and closure alternative**.

### Prediction 7

A failed send returns `SendError<Job>`. The code discards the error. Which product obligation is lost?

Record: **ownership recovery and missing outcome**.

### Prediction 8

The standard MPSC `Receiver` is cloned for four workers. Predict the API result and viable topologies.

Record: **receiver topology**.

## Part 2 — Diagnose and repair

Review a worker pool with one bounded work channel and one bounded result channel. The coordinator submits every job before receiving results. Each worker sends a result before receiving another job. Both channels have capacity equal to worker count, and some jobs are slow. Shutdown sends one string `"STOP"` per worker, while an extra sender clone remains in a metrics object.

Draw the wait-for graph and endpoint graph. Show the schedule that fills both channels. Replace the topology with either a concurrent result collector or a bounded work queue plus result channel whose total messages are bounded by accepted jobs. Replace string sentinels with closure or typed lifecycle state and prove all clones are dropped.

### Weak repairs to reject

Reject each of these shortcuts and replace it with the smallest repair that preserves the product requirement:

- increasing channel capacities until the deadlock is harder to reproduce;
- using an unbounded channel without bounding accepted message count or payload size;
- sending magic strings as shutdown markers;
- treating disconnect as success without worker and outcome accounting;
- discarding unsent messages returned by a failed send;
- sorting values without carrying stable identity through the protocol;

For every repair, identify which of the six review dimensions it restores: ownership, visibility, exclusion, progress, failure, or determinism. A repair that improves one dimension may damage another; record both effects.

## Part 3 — Focused exercises

### Construction 1

Design endpoint ownership for a four-worker finite pipeline.

Required evidence: Name every sender clone, the unique receiver owner, drop point, and join point.

### Construction 2

Choose work and result channel capacities for a bounded product.

Required evidence: State maximum jobs, payload size, in-flight work, blocked send behavior, and why no wait cycle forms.

### Construction 3

Define typed messages for jobs, completed outcomes, domain errors, panic containment, and infrastructure failure.

Required evidence: Do not encode terminal states as ordinary payload values.

### Construction 4

Implement deterministic assembly from out-of-order `(index, outcome)` messages.

Required evidence: Detect duplicate, missing, and out-of-range indices.

### Construction 5

Prove shutdown for zero jobs, all successes, first-job cancellation, and one worker panic.

Required evidence: List endpoint closure and join actions for each path.

### Interleaved reasoning pass

1. For **Model channel operations as ownership transfer rather than shared access**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the channel topology.
2. For **Choose bounded, zero-capacity, or unbounded channels from an explicit resource and latency policy**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the channel topology.
3. For **Draw sender/receiver topology and identify which endpoints are clonable**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the channel topology.
4. For **State whether disconnect is normal completion, cancellation, or infrastructure failure**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the channel topology.

5. Identify one guarantee from an earlier course that a careless implementation of **Message Passing, Backpressure, and Shutdown** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Bounded Map Pipeline](../../labs/module-05-bounded-map-pipeline/README.md) from the starter. Before opening the solution, produce:

- an endpoint topology diagram with all clone owners and drop points;
- a capacity argument covering work and result memory;
- stable indexed output independent of completion order;
- complete joins on success and failure;
- a test for disconnect caused by worker loss rather than normal completion;

Your submission must also identify one schedule that the implementation handles correctly and one product claim it deliberately does not make.

### Laboratory acceptance trace

Before opening the reference implementation for **Bounded Map Pipeline**, record:

- the public behavior that demonstrates **Model channel operations as ownership transfer rather than shared access**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Add BatchWeave’s result channel and `WorkerEvent` protocol. Workers must send one indexed terminal outcome for every job they accept. The coordinator must be able to distinguish completed, domain-failed, panicked, and cancelled jobs from worker infrastructure faults. Use an unbounded standard result channel only because the manifest imposes a strict maximum job count; document that bound.

Required capstone evidence:

- a result-message enum and endpoint ownership diagram;
- a proof that at most one terminal outcome exists per accepted job;
- duplicate and out-of-range result detection;
- deterministic assembly by source index;
- a complete normal-shutdown sequence including sender drops and joins;

Add at least one regression test that fails if this module's governing contract is removed. Tests that merely sleep and hope for a schedule do not count as causal evidence.

### Capstone invariant trace

For the Module 65 BatchWeave increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Answer without the chapter:

1. What ownership change occurs after a successful send?
2. What does bounded capacity guarantee, and what can remain unbounded?
3. Why can cloned senders prevent receiver termination?
4. How can a bounded work and bounded result channel deadlock?
5. How does stable identity separate result order from completion order?

### Independent transfer

Design a bounded document-conversion service with one dispatcher, three format-specific workers, and one result collector. Some formats have no worker. State what happens to unsupported documents, failed sends, worker panics, and cancellation. Bound every queue and payload, preserve request order in the final report, and prove that all receivers terminate when the dispatcher fails halfway through input.

### Closed-book defense

In five minutes, answer “Which values cross ownership boundaries, how is capacity bounded, and which explicit protocol event proves that every sender, receiver, and worker can terminate?” using the **channel topology**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside BatchWeave. A list of APIs without the deciding relationship is incomplete.
