# Lab — Reproduce acknowledgement loss and per-partition ordering

## Objective

Use the deterministic broker to prove redelivery, settlement, ordering, group independence, and bounded terminal handling without timing flakiness.

## Setup conditions


1. Run `make contract-proof` and select `AnalysisRunCompleted`.
2. Create a deterministic clock starting at a fixed UTC instant.
3. Create a four-partition channel and three consumer groups.
4. Publish at least six events for three run IDs, including multiple events for one run.
5. Store the expected partition/offset trace in `work/module-03/expected-trace.json`.


## Failure action and investigation


Poll one notification delivery, perform a mock effect, and intentionally omit acknowledgement. Advance the
clock beyond the deadline and poll again. Confirm the same record appears with a higher attempt and new
token.

In parallel, process another partition and show that unrelated work can advance. Negative-acknowledge one
transient failure with delay. Terminate one deliberately poison record after the declared attempt limit.
Attempt to settle an already-settled token and require a failure.



### Investigation notes

Before editing, write a one-sentence hypothesis answering: **What do acknowledgement, redelivery, ordering, partitioning, lag, and consumer groups actually guarantee?** Record the first observation that contradicts the expected model. After the repair, explain why the capstone can now claim: Implement deterministic delivery attempts, partition order, group independence, acknowledgement expiry, negative acknowledgement, and redelivery. A passing command without this causal explanation is insufficient.

## Operational oracle


Per-partition offsets are monotonic, the same run never overtakes its unacknowledged predecessor, other
partitions can progress, group positions remain independent, ack expiry redelivers the same record, and
token reuse is rejected. The poison event reaches the terminal path only after the configured attempts.


## Required evidence


- `work/module-03/delivery-trace.json`
- `work/module-03/failure-window-table.md`
- `work/module-03/lag-snapshots.json`
- the redelivery attempt identities
- the token-reuse failure
- output from `make delivery-proof`
- optional NATS comparison clearly labeled as live or not executed


## Cleanup and reset


Acknowledge or terminate all remaining test deliveries, reset the deterministic clock and broker state, stop
the optional NATS process, and remove generated streams. Retain only evidence and source changes.


## Completion gate


The lab passes when every delivery transition is explained from durable/group state, not from sleep-based
observation. The learner must identify the crash-after-effect-before-ack duplicate that remains unsolved
until Module 04.
