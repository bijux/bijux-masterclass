# Lab 09 — Resume under duplicates, gaps, and slow consumption

## Purpose

Prove the application subscription profile over durable events: exact resume, duplicate suppression, gap detection, bounded buffering, cancellation, and reauthorization.

## Prerequisites

Complete Module 8. Seed run events with monotonic sequence values and configure a small per-subscription queue. Use a principal whose permission can be revoked during the experiment.

## Procedure

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

## Correctness oracle

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

## Interpretation questions

- When would coalescing progress events be safe, and why is that a separate profile?
- Why is a GraphQL subscription not the durable event contract?
- Which metrics indicate an open but unhealthy subscription?
- How does trace context cross from an event into a response execution?

## Cleanup

Close all streams, cancel source consumers, restore permissions, and clear queue state. Confirm active-subscription and consumer counts return to zero.

## Completion gate

All sequence cases match the profile, memory remains bounded, revoked authority stops delivery, cancellation reaches the source, and both language tracks agree on duplicate/gap outcomes.
