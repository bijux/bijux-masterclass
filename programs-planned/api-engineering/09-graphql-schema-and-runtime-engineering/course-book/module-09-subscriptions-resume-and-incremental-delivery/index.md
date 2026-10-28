# Subscriptions, Resume, and Incremental Delivery

**Module 09 of 10**

> **Governing question:** How can real-time graph results remain authorized, bounded, and recoverable across disconnects?

## Place in the program

Courses 1–8 established the contract, durable implementation, security, operations, performance, asynchronous events, typed RPC, and distributed ownership. Module 09 applies those guarantees to the graph interface; none are reset at the GraphQL boundary.

## Learning outcomes

- map durable events to subscription responses

- resume by sequence

- re-evaluate long-lived authorization

- bound subscriber buffers

- classify incremental-delivery features honestly

## Capstone result

Deliver resumable run updates with gap and duplicate handling.

## A subscription maps a source stream to repeated execution

GraphQL subscriptions begin with one top-level field. The resolver creates a source event stream; each source event triggers execution of the subscription selection set and produces one response event. The GraphQL core specification deliberately leaves transport, acknowledgement, buffering, and replay to implementations.

Course 9 uses Analysis Events API 1.0 as the durable source. The graph subscription is a projection over that event contract, not a replacement broker.

## Resume is an application profile

The client supplies `afterSequence`. The subscription suppresses duplicates at or below that sequence and requires the next event to be exactly one greater. A gap stops delivery and directs the client to replay or refetch authoritative state. Silent skipping would make the stream appear complete when it is not.

Resume tokens bind subject, tenant, operation, and resource in a real deployment. The dependency-light core demonstrates sequence semantics; the database migration provides a place for subscriber checkpoints.

## Authorization changes during long-lived operations

Subscription authorization is checked when the stream starts, but credentials and permissions can expire while it remains open. A production profile must define re-evaluation, maximum connection lifetime, or token refresh. Removing a tenant role must eventually terminate access.

Each emitted event is filtered by tenant and resource. A shared broker topic is not a security boundary. The graph layer must not rely on obscured subscription IDs.

## Backpressure and slow clients

Every subscriber has a bounded buffer. When a client cannot consume fast enough, the runtime may close the stream with a resumable error rather than grow memory indefinitely. Source event retention determines how long resume remains possible.

Fan-out is controlled per principal and operation. One client opening thousands of subscriptions is a traffic and security problem, even if each selection is cheap.

## Incremental delivery frontier

Subscriptions represent events over time. Incremental delivery of one query response through `@defer` or `@stream` is a different mechanism. Those directives are not part of the released GraphQL September 2025 specification, so Analysis Graph API 1.0 does not require them.

A future profile may adopt an implementation-supported draft after capability testing. It must specify transport framing, cancellation, ordering, error semantics, caching, and client support. “Our library has a flag” is not sufficient release evidence.

## Subscription execution model

A GraphQL subscription has two conceptual stages. First, the subscription operation creates a source event stream. Second, each source event triggers execution of the selected response shape, producing a response stream. The GraphQL core specification does not choose WebSocket, Server-Sent Events, broker acknowledgements, replay retention, or quality-of-service semantics.

The course therefore defines an application subscription profile over Analysis Events API 1.0. It uses event sequence as the durable resume coordinate and treats the network transport as replaceable. A transport adapter must preserve cancellation, backpressure, authentication, and resume outcomes.

The selected subscription operation has exactly one top-level field. That field establishes the run and tenant scope before the event stream opens. For every event, the response selection executes against current policy and source data rather than blindly forwarding broker payloads.

## Resume, duplicates, and gaps

A client supplies `afterSequence` with the last sequence it processed durably. The server requests events strictly after that value. Three cases matter:

- **duplicate** — sequence is less than or equal to the last emitted value; suppress it;
- **next event** — sequence is exactly the expected successor; emit it;
- **gap** — sequence jumps forward; stop or enter an explicit recovery path rather than pretending continuity.

A gap can mean retention expiry, partition loss, projection defect, or an invalid resume token. The course returns a stable gap outcome that tells the client to refetch authoritative state and open a new subscription. It never silently continues because the client could miss a security-relevant or terminal transition.

Sequence values are opaque strings in the GraphQL contract so JavaScript clients do not lose 64-bit precision. The runtime compares them using the event profile's exact integer rules.

## Authorization over a long-lived operation

Authorization can change while a subscription is open. A token can expire, a tenant membership can be revoked, or a run can move to a classification the caller may no longer observe.

The subscription profile defines:

- authentication at connection or request establishment;
- authorization when the source stream is created;
- periodic or event-triggered reauthorization;
- maximum session lifetime;
- behavior on token expiry or revocation;
- concealment and audit behavior on denial.

Do not authorize only once and keep streaming indefinitely. Do not accept a new bearer token in arbitrary application messages without a documented transport profile. Reauthentication is a security protocol, not an implementation convenience.

## Backpressure and slow clients

A source can produce updates faster than a client can receive them. An unbounded per-connection queue turns one slow client into a memory leak. The host needs:

- bounded queue capacity;
- maximum message size;
- send deadline;
- overflow policy;
- connection and tenant concurrency budgets;
- cancellation propagation to source consumption;
- lag telemetry.

For state-transition updates, dropping intermediate messages may be unsafe because sequence continuity matters. The course closes the stream with an explicit resync-required outcome when the client falls behind, rather than silently dropping. For a high-frequency progress signal with replaceable intermediate values, a different coalescing profile could be justified, but it must be declared separately.

Backpressure must reach the event consumer boundary. Reading the entire retained stream into memory before sending does not preserve it. The dependency-light reference uses a bounded iterator and the environment-backed adapter uses a bounded asynchronous queue.

## Subscription source versus live query

A subscription is not “run this query every second.” Polling can be correct for low-frequency state and benefits from normal HTTP caching and deadlines. A subscription is appropriate when clients need timely changes, the platform has a durable event source, and the operational cost of long-lived connections is justified.

The response selection may resolve current fields from services for each event. That can amplify source traffic. The schema should keep subscription payloads focused and the runtime should batch or use event-carried facts where authority permits. A client that needs a large project overview after each update should receive a small run update and refetch a trusted query under normal admission policy.

## Incremental delivery is a separate frontier

`@defer` and `@stream` concern incremental delivery of one operation result. Subscriptions concern repeated execution over source events. They solve different problems.

The course baseline does not require draft incremental-delivery behavior. The frontier SDL and lab explain how a future profile would need to define:

- transport framing;
- patch identity and ordering;
- error paths across patches;
- cancellation;
- cache and retry semantics;
- interaction with non-null propagation;
- client capability negotiation.

Do not advertise incremental directives merely because a framework has an experimental flag. A production contract requires client and transport evidence.

## Operational model

Long-lived graph operations need separate metrics from short requests:

- active connections by bounded client class;
- admission and rejection counts;
- event-to-delivery lag;
- last emitted sequence;
- duplicate and gap outcomes;
- queue occupancy and overflow;
- reauthorization failures;
- session lifetime and closure reason.

A connection that remains open is not necessarily healthy. A stream with growing event lag has failed its purpose before it disconnects. Course 4 alert principles apply to lag and gap rates, and Course 5 capacity models include connection memory and event execution cost.

## Subscription review checklist

Verify:

- the source event is owned and retained under Course 6 policy;
- the GraphQL operation has one top-level subscription field;
- resume sequence is durable and precision-safe;
- duplicate, gap, and retention-expiry behavior is explicit;
- authorization is re-evaluated over time;
- queues and message sizes are bounded;
- slow clients cannot exhaust the process;
- cancellation stops source work;
- subscription payload cost is controlled;
- transport-specific behavior is labeled as a profile rather than core GraphQL.

## Worked capstone review

A subscriber resumes after sequence 3 and receives 4, 4, 5. Duplicate 4 is suppressed and 4–5 are delivered. If the source begins at 5, the runtime stops with a gap instead of pretending continuity. The client refetches or initiates Course 6 replay.

## Python and TypeScript implications

Both tracks implement duplicate suppression, strict next-sequence checks, and bounded buffers. Real transports must add disconnect cancellation and security-context lifetime handling.

## Evidence required before the next module

Complete the lab and checkpoint. The decisive artifact is the module report under `reports/module-09-*.json`; prose claims without its oracle do not pass.
