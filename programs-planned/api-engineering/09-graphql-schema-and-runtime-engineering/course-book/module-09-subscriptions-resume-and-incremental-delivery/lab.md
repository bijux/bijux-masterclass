# Lab — Resume under duplicates, gaps, and slow consumption

> **Module 09:** Subscriptions, Resume, and Incremental Delivery

## Objective

Prove the application subscription profile over durable events: exact resume, duplicate suppression, gap detection, bounded buffering, cancellation, and reauthorization.

## Why this lab matters

This lab turns the module’s governing question—**How can real-time graph results remain authorized, bounded, and recoverable across disconnects?**—into a falsifiable experiment. The course therefore defines an application subscription profile over Analysis Events API 1.0. It uses event sequence as the durable resume coordinate and treats the network transport as replaceable. A transport adapter must preserve cancellation, backpressure, authentication, and resume outcomes.

It advances the cumulative Analysis Runs Platform by requiring this result: **Deliver resumable run updates with gap and duplicate handling**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Complete Module 8. Seed run events with monotonic sequence values and configure a small per-subscription queue. Use a principal whose permission can be revoked during the experiment.

## Hypothesis

The clean implementation should satisfy this claim: **resume begins strictly after the last processed sequence; duplicates are suppressed; gaps and retention expiry are explicit; sequence values remain precision-safe strings; buffer and message size remain bounded; slow consumption cannot exhaust the host; authorization changes terminate access; cancellation propagates to source work; no event is silently skipped while claiming continuity.** When the lab introduces this fault—**Expect delivery 4, 5; the duplicate must not produce a second response**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

### 1. Resume after a durable sequence

Open `RunUpdates` with `afterSequence: "3"` over source events `4, 4, 5`. Expect delivery `4, 5`; the duplicate must not produce a second response.

### 2. Detect a gap

Open after `3` over source events `5, 6`. The server must stop with a stable resync-required outcome before delivering a false continuous stream. Record the last durable sequence and recovery instruction.

### 3. Test retention expiry

Resume from a sequence older than the event-retention floor. Distinguish this from a transient transport failure. The client must refetch authoritative state and establish a new resume point.

### 4. Apply slow-consumer pressure

Produce sequences `4` through `110` while the client consumes slowly and queue capacity is deliberately small. The host must not grow memory without bound. Under the course state-transition profile, overflow terminates with resync required rather than silently dropping events.

### 5. Revoke authority

Open a healthy stream, deliver one event, revoke `RUN_READ` or tenant membership, then deliver another. The subscription reauthorization policy must close the stream and record an auditable bounded reason.

### 6. Cancel from the client

Cancel the operation and prove that source consumption and pending tasks stop. A closed network connection alone is not evidence if the broker consumer remains active.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Expect delivery 4, 5; the duplicate must not produce a second response**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Prove the application subscription profile over durable events: exact resume, duplicate suppression, gap detection, bounded buffering, cancellation, and reauthorization**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- resume begins strictly after the last processed sequence;
- duplicates are suppressed;
- gaps and retention expiry are explicit;
- sequence values remain precision-safe strings;
- buffer and message size remain bounded;
- slow consumption cannot exhaust the host;
- authorization changes terminate access;
- cancellation propagates to source work;
- no event is silently skipped while claiming continuity.

## Required evidence

Create `reports/module-09-subscriptions.json` containing source sequences, delivered sequences, duplicate count, gap category, retention floor, maximum queue occupancy, close reason, authorization revision, cancellation state, and last safe resume coordinate.

## Interpretation and defense

1. Which state or effect is authoritative for **Subscriptions, Resume, and Incremental Delivery**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Expect delivery 4, 5; the duplicate must not produce a second response** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Close all streams, cancel source consumers, restore permissions, and clear queue state. Confirm active-subscription and consumer counts return to zero.

## Completion gate

All sequence cases match the profile, memory remains bounded, revoked authority stops delivery, cancellation reaches the source, and both language tracks agree on duplicate/gap outcomes.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Subscriptions, Resume, and Incremental Delivery**. A green command without the negative case and causal explanation does not satisfy this gate.
