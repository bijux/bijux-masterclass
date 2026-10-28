# Lab — Reproduce acknowledgement loss and per-partition ordering

> **Module 03:** Delivery Semantics, Ordering, Partitioning, and Acknowledgement

## Objective

Use the deterministic broker to prove redelivery, settlement, ordering, group independence, and bounded terminal handling without timing flakiness.

## Why this lab matters

This lab turns the module’s governing question—**What do acknowledgement, redelivery, ordering, partitioning, lag, and consumer groups actually guarantee?**—into a falsifiable experiment. Two runs use different partition keys. run-B completed is observed before run-A started, and a dashboard labels the stream corrupt. There was no cross-run ordering promise. The projection must order within each subject or use event time and explicit aggregation semantics.

It advances the cumulative Analysis Runs Platform by requiring this result: **Implement deterministic delivery attempts, partition order, group independence, acknowledgement expiry, negative acknowledgement, and redelivery**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

1. Run `make contract-proof` and select `AnalysisRunCompleted`.
2. Create a deterministic clock starting at a fixed UTC instant.
3. Create a four-partition channel and three consumer groups.
4. Publish at least six events for three run IDs, including multiple events for one run.
5. Store the expected partition/offset trace in `work/module-03/expected-trace.json`.

## Hypothesis

The clean implementation should satisfy this claim: **Per-partition offsets are monotonic, the same run never overtakes its unacknowledged predecessor, other partitions can progress, group positions remain independent, ack expiry redelivers the same record, and token reuse is rejected. The poison event reaches the terminal path only after the configured attempts.** When the lab introduces this fault—**Attempt to settle an already-settled token and require a failure**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

Poll one notification delivery, perform a mock effect, and intentionally omit acknowledgement. Advance the
clock beyond the deadline and poll again. Confirm the same record appears with a higher attempt and new
token.

In parallel, process another partition and show that unrelated work can advance. Negative-acknowledge one
transient failure with delay. Terminate one deliberately poison record after the declared attempt limit.
Attempt to settle an already-settled token and require a failure.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Attempt to settle an already-settled token and require a failure**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Use the deterministic broker to prove redelivery, settlement, ordering, group independence, and bounded terminal handling without timing flakiness**, and identify one attractive implementation that would pass the happy path while failing the oracle.

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

## Interpretation and defense

1. Which state or effect is authoritative for **Delivery Semantics, Ordering, Partitioning, and Acknowledgement**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Attempt to settle an already-settled token and require a failure** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Acknowledge or terminate all remaining test deliveries, reset the deterministic clock and broker state, stop
the optional NATS process, and remove generated streams. Retain only evidence and source changes.

## Completion gate

The lab passes when every delivery transition is explained from durable/group state, not from sleep-based
observation. The learner must identify the crash-after-effect-before-ack duplicate that remains unsolved
until Module 04.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Delivery Semantics, Ordering, Partitioning, and Acknowledgement**. A green command without the negative case and causal explanation does not satisfy this gate.
