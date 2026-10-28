# Worked Answers — Module 09: Subscriptions, Resume, and Incremental Delivery

Use these solutions to audit your reasoning for **Subscriptions, Resume, and Incremental Delivery**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. What does GraphQL core define for subscriptions?

Source stream creation, mapping each source event through execution, response stream behavior, cancellation, and completion—not transport QoS.

**Decisive evidence.** Inspect the core specification algorithms and the course transport profile separately. Core evidence covers source and response streams; SSE framing, replay, and buffering belong to the local profile.

The chapter’s decisive distinction is this: GraphQL subscriptions begin with one top-level field. The resolver creates a source event stream; each source event triggers execution of the subscription selection set and produces one response event. The GraphQL core specification deliberately leaves transport, acknowledgement, buffering, and replay to implementations.

## 2. Why use Course 6 events as the source?

They are durable, versioned, tenant-aware integration facts with replay policy. An in-memory pub/sub alone cannot support reliable resume.

**Decisive evidence.** Trace `AnalysisRunUpdated` back to Analysis Events API 1.0. The graph subscription must consume retained authoritative events rather than create a competing event history.

In the cumulative capstone, the rule becomes concrete: The course therefore defines an application subscription profile over Analysis Events API 1.0. It uses event sequence as the durable resume coordinate and treats the network transport as replaceable. A transport adapter must preserve cancellation, backpressure, authentication, and resume outcomes.

## 3. What does afterSequence mean?

Deliver only events after the last confirmed sequence while requiring continuity from the next value.

**Decisive evidence.** Resume after sequence 3 and deliver 4 onward. The checkpoint is exclusive, scoped to the run and subscriber context, and never interpreted as an array offset.

A useful way to reason about the boundary is: The client supplies afterSequence. The subscription suppresses duplicates at or below that sequence and requires the next event to be exactly one greater. A gap stops delivery and directs the client to replay or refetch authoritative state. Silent skipping would make the stream appear complete when it is not.

## 4. How are duplicate events handled?

Sequences already delivered or repeated in the source are suppressed idempotently.

**Decisive evidence.** Provide sequences 4, 4, and 5 after checkpoint 3. The client receives 4 and 5 once, while duplicate attempts remain observable operationally.

The implementation consequence is: A subscriber resumes after sequence 3 and receives 4, 4, 5. Duplicate 4 is suppressed and 4–5 are delivered. If the source begins at 5, the runtime stops with a gap instead of pretending continuity. The client refetches or initiates Course 6 replay.

## 5. Why is a gap an error?

Skipping a missing event would make the client state silently incomplete. The stream pauses and requires replay or authoritative refetch.

**Decisive evidence.** Provide sequence 5 after checkpoint 3 with 4 missing. Delivery must stop and require replay; continuing would present an unprovable state transition history.

The important nuance is: A gap can mean retention expiry, partition loss, projection defect, or an invalid resume token. The course returns a stable gap outcome that tells the client to refetch authoritative state and open a new subscription. It never silently continues because the client could miss a security-relevant or terminal transition.

## 6. When should authorization be rechecked?

At start and according to credential expiry, permission changes, maximum stream lifetime, or event-level policy.

**Decisive evidence.** Expire or revoke the credential during a long stream. Recheck at connection start and at the policy-defined freshness/event boundary, then close without leaking later events.

Under concurrency or failure, the distinction becomes: Subscription authorization is checked when the stream starts, but credentials and permissions can expire while it remains open. A production profile must define re-evaluation, maximum connection lifetime, or token refresh. Removing a tenant role must eventually terminate access.

## 7. What happens when a client is too slow?

A bounded buffer fills, the server closes or degrades under a documented resumable policy, and the client reconnects from its last sequence.

**Decisive evidence.** Exceed the per-subscriber buffer while the source continues. The profile must apply bounded disconnect, backpressure, or replay—not unbounded memory growth.

The design remains honest only if: Every subscriber has a bounded buffer. When a client cannot consume fast enough, the runtime may close the stream with a resumable error rather than grow memory indefinitely. Source event retention determines how long resume remains possible.

## 8. Why is a broker topic not tenant isolation?

Topic naming or obscurity does not prove authorization. Every subscription and emitted event must enforce tenant policy.

**Decisive evidence.** Subscribe two tenants to the same broker subject in a controlled test. Application authorization and event filtering must still prevent cross-tenant delivery.

The consumer-facing consequence is: Authorization can change while a subscription is open. A token can expire, a tenant membership can be revoked, or a run can move to a classification the caller may no longer observe.

## 9. How do subscriptions differ from @defer/@stream?

Subscriptions produce repeated executions from events; incremental delivery splits one query response over time.

**Decisive evidence.** Compare one long-lived event source with incremental chunks from a single query execution. They have different lifetime, replay, cancellation, and consistency semantics.

The operational consequence is: Subscriptions represent events over time. Incremental delivery of one query response through @defer or @stream is a different mechanism. Those directives are not part of the released GraphQL September 2025 specification, so Analysis Graph API 1.0 does not require them.

## 10. Are @defer and @stream in the September 2025 release?

No. The course treats them as separately versioned ecosystem frontier features.

**Decisive evidence.** Validate the released schema against the September 2025 baseline. Keep `@defer` and `@stream` in the separately versioned frontier file and capability matrix.

The strongest engineering interpretation is: Subscriptions represent events over time. Incremental delivery of one query response through @defer or @stream is a different mechanism. Those directives are not part of the released GraphQL September 2025 specification, so Analysis Graph API 1.0 does not require them.

## 11. What should disconnect do to the source stream?

Cancel observation and release buffers, loaders, service calls, and trace state.

**Decisive evidence.** Cancel the client connection and verify the response stream, source iterator, broker subscription, heartbeat, and request resources are all released.

The defect-oriented view is: A GraphQL subscription has two conceptual stages. First, the subscription operation creates a source event stream. Second, each source event triggers execution of the selected response shape, producing a response stream. The GraphQL core specification does not choose WebSocket, Server-Sent Events, broker acknowledgements, replay retention, or quality-of-service semantics.

## 12. What evidence proves resume correctness?

Fixtures for duplicates, exact continuation, gaps, bounds, tenant filtering, and cancellation plus a live transport test when available.

**Decisive evidence.** Replay duplicate, gap, late authorization, slow-consumer, and disconnect schedules. Exact delivered sequences and cleanup counters are the decisive evidence.

Across the Python and TypeScript tracks, the invariant is: A future profile may adopt an implementation-supported draft after capability testing. It must specify transport framing, cancellation, ordering, error semantics, caching, and client support. “Our library has a flag” is not sufficient release evidence.
