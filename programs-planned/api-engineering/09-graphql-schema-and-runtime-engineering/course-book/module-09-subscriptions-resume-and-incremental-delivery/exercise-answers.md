# Worked answers — Subscriptions, Resume, and Incremental Delivery

Compare the decision rule and evidence, not just wording.

## 1. What does GraphQL core define for subscriptions?

Source stream creation, mapping each source event through execution, response stream behavior, cancellation, and completion—not transport QoS.

**Decisive evidence.** Inspect the core specification algorithms and the course transport profile separately. Core evidence covers source and response streams; SSE framing, replay, and buffering belong to the local profile.

## 2. Why use Course 6 events as the source?

They are durable, versioned, tenant-aware integration facts with replay policy. An in-memory pub/sub alone cannot support reliable resume.

**Decisive evidence.** Trace `AnalysisRunUpdated` back to Analysis Events API 1.0. The graph subscription must consume retained authoritative events rather than create a competing event history.

## 3. What does afterSequence mean?

Deliver only events after the last confirmed sequence while requiring continuity from the next value.

**Decisive evidence.** Resume after sequence 3 and deliver 4 onward. The checkpoint is exclusive, scoped to the run and subscriber context, and never interpreted as an array offset.

## 4. How are duplicate events handled?

Sequences already delivered or repeated in the source are suppressed idempotently.

**Decisive evidence.** Provide sequences 4, 4, and 5 after checkpoint 3. The client receives 4 and 5 once, while duplicate attempts remain observable operationally.

## 5. Why is a gap an error?

Skipping a missing event would make the client state silently incomplete. The stream pauses and requires replay or authoritative refetch.

**Decisive evidence.** Provide sequence 5 after checkpoint 3 with 4 missing. Delivery must stop and require replay; continuing would present an unprovable state transition history.

## 6. When should authorization be rechecked?

At start and according to credential expiry, permission changes, maximum stream lifetime, or event-level policy.

**Decisive evidence.** Expire or revoke the credential during a long stream. Recheck at connection start and at the policy-defined freshness/event boundary, then close without leaking later events.

## 7. What happens when a client is too slow?

A bounded buffer fills, the server closes or degrades under a documented resumable policy, and the client reconnects from its last sequence.

**Decisive evidence.** Exceed the per-subscriber buffer while the source continues. The profile must apply bounded disconnect, backpressure, or replay—not unbounded memory growth.

## 8. Why is a broker topic not tenant isolation?

Topic naming or obscurity does not prove authorization. Every subscription and emitted event must enforce tenant policy.

**Decisive evidence.** Subscribe two tenants to the same broker subject in a controlled test. Application authorization and event filtering must still prevent cross-tenant delivery.

## 9. How do subscriptions differ from @defer/@stream?

Subscriptions produce repeated executions from events; incremental delivery splits one query response over time.

**Decisive evidence.** Compare one long-lived event source with incremental chunks from a single query execution. They have different lifetime, replay, cancellation, and consistency semantics.

## 10. Are @defer and @stream in the September 2025 release?

No. The course treats them as separately versioned ecosystem frontier features.

**Decisive evidence.** Validate the released schema against the September 2025 baseline. Keep `@defer` and `@stream` in the separately versioned frontier file and capability matrix.

## 11. What should disconnect do to the source stream?

Cancel observation and release buffers, loaders, service calls, and trace state.

**Decisive evidence.** Cancel the client connection and verify the response stream, source iterator, broker subscription, heartbeat, and request resources are all released.

## 12. What evidence proves resume correctness?

Fixtures for duplicates, exact continuation, gaps, bounds, tenant filtering, and cancellation plus a live transport test when available.

**Decisive evidence.** Replay duplicate, gap, late authorization, slow-consumer, and disconnect schedules. Exact delivered sequences and cleanup counters are the decisive evidence.
