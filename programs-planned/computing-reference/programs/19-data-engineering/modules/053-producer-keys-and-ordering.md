---
module_id: DE-053
program: Data Engineering
level: 2
module_number: 53
title: Producer Keys and Ordering
status: complete
last_verified: 2026-09-03
---

# Producer Keys and Ordering

## One-Page Review

### Governing question

How should producers choose stable keys and establish the smallest sufficient ordering relation so that related events route consistently, concurrent writers do not corrupt state, retries do not silently reorder history, and the stream can still scale?

### Essential definitions

- A **business key** identifies the domain entity or order scope whose events must meet a shared invariant, such as account, order, device, or tenant-and-account.
- A **routing key** is the canonical byte sequence supplied to a partitioning function. It may derive from a business key but is an explicit, versioned representation.
- A **partition key** is the key a particular messaging service uses to choose a partition/shard or ordering domain; its semantics are product- and configuration-specific.
- A **partitioner** is a versioned function $r_v(k,m)$ mapping canonical key bytes $k$ and topology metadata $m$ to a destination order domain.
- A **key schema** defines components, types, canonicalization, serialization, null behavior, privacy classification, cardinality, and evolution rules for routing keys.
- **Append order** is the order accepted by one broker partition/log; **send-call order**, **acknowledgement order**, **event time**, **business version order**, and **effect order** are distinct relations.
- A **producer session** is one logical writer instance with a stable identity and bounded lifetime; a **producer epoch** fences earlier sessions for the same writer role.
- A **producer sequence** is a monotone number scoped to a producer/session and destination domain, used by some protocols to detect duplicates or gaps.
- **Happens-before** is the partial order induced by local program order and causal communication; concurrent events need not have a truthful total order.
- A **business version** is an authority-issued monotone revision within a domain entity, often stronger for conflict detection than arrival time.
- **Idempotent production** prevents specified duplicate appends caused by producer retries within its documented scope; it does not deduplicate arbitrary application resends or downstream effects.
- **Fencing** rejects writes from a stale producer epoch or lease after a newer writer has authority.
- An **ordering key** requests a service-defined order for messages sharing that key under documented publication, region, subscription, and retry conditions.
- A **hot key** is one order domain whose offered work exceeds its sustainable serial capacity; adding unrelated partitions cannot split its required order.
- A **repartitioning migration** changes routing/key/topology semantics using named old/new epochs, cuts, state movement, validation, and stale-writer fencing.

### Central model, mechanism, or theorem

Let domain events have business keys $b(e)$ and let versioned canonicalization/serialization produce bytes

$$
k_v(e)=\operatorname{encode}_v(\operatorname{canonicalize}_v(b(e))).
$$

For topology $\tau$, producer partitioner $r_v$ selects

$$
p(e)=r_v(k_v(e),\tau).
$$

Co-location follows only when every relevant producer uses the same key bytes, routing version, and compatible topology view. If business invariant $I$ requires events $e_i,e_j$ to share an append order, the routing contract must ensure

$$
I(e_i,e_j)\Rightarrow p(e_i)=p(e_j),
$$

and the producer/broker protocol must preserve the intended order inside that partition. The converse is false: co-location does not prove correct causal/business order. The narrow design rule is therefore to choose the smallest domain that must be serialized, establish authority/version/fencing for concurrent writers, and leave unrelated domains concurrent.

### Critical invariants

- Business identity, routing key bytes, partition key, occurrence ID, producer identity/epoch/sequence, business version, event time, and broker coordinate remain distinct fields.
- Every producer uses the same versioned key schema, canonicalization, encoding, hash/partitioner, null policy, and topology generation before same-key co-location is claimed.
- The chosen order scope is no broader than the invariant requires and no narrower than the state transition requires; “global order” is never a default.
- Same-key append order is claimed only under explicit producer concurrency, retry, in-flight, idempotence, transaction, and broker acknowledgement conditions.
- Stale producer epochs cannot append authoritative transitions after a newer epoch begins; leases without fencing tokens do not establish exclusive authorship.
- A producer acknowledgement is not event identity, business acceptance, consumer processing, or external effect order.
- Producer retries preserve occurrence identity and use protocol-supported idempotence where available; application recreation/resubmission has a separate deduplication contract.
- A key change, normalization change, serializer/hash change, partitioner change, or partition-count change is a data/topology migration, not a client refactor.
- Null/missing/invalid keys have a deliberate policy: reject, quarantine, derive safely, or accept unordered distribution; silent fallback never inherits ordered semantics.
- Per-key load, bytes, event cost, state, burst, retry amplification, and downstream contention fit one order domain with recovery headroom.
- Multi-entity invariants use a named coordination strategy—transaction, command authority, saga, version/precondition, deterministic merge, or redesigned aggregate—rather than assuming adjacent records are atomic.
- Event time and physical clocks do not silently resolve concurrent writes; causality, source versions, and conflict rules remain explicit.
- Keys and headers are minimized, protected, auditable, and stable under tenant/security/privacy boundaries; sensitive raw identifiers are not copied merely for routing convenience.
- Tests include multiple languages/versions, canonical-equivalent inputs, producer crash/restart, timeout/unknown acknowledgement, retry, concurrent writers, stale epochs, metadata change, partition expansion, and hot-key overload.

### Common failures

Common failures include choosing a random event UUID as the routing key when entity order is required; using a low-cardinality country or tenant key that creates hotspots; relying on language-native `hash()`; hashing different serialized bytes across clients; trimming/case-folding/Unicode-normalizing inconsistently; treating null keys as ordered; assuming send invocation order equals append or acknowledgement order; running multiple producers for one entity without authority/version fencing; retrying at application level with a new occurrence ID; enabling retries with unsafe in-flight ordering configuration; sorting by producer timestamp; using broker offset as business version; claiming same-partition means causal correctness; widening to one global partition; expanding partition count without routing migration; and placing direct personal identifiers in keys, metrics, logs, and dead-letter metadata.

### Compact example

Two producers spell an account key as `" ACCT-17 "` and `"acct-17"`. Under key schema `key-v1`, both canonicalize to the same ASCII bytes and route by a specified SHA-256-derived function to partition 3 of eight. The active writer epoch is 7 with producer sequences 0, 1, and 2 and business versions 40, 41, and 42. A late record from epoch 6 is fenced. This demonstrates deterministic co-location and a local authority check; it does not prove broker durability, downstream exactly-once effects, global time order, or that SHA-256 modulo eight is the right production partitioner.

### Connections

[DE-051](051-streams-logs-and-unbounded-data.md) established event identity and finite log cuts. [DE-052](052-topics-partitions-and-offsets.md) defined partition-local coordinates, topology epochs, skew, and migrations. [DE-039](039-deterministic-transformations.md) supplies deterministic representation; [DE-044](044-retries-timeouts-and-idempotency.md) separates attempt identity from effects. DE-054 will cover consumer-group ownership, DE-055 delivery semantics, and DE-056 exactly-once effects.

## Governing Question

An event platform can preserve the order in which one partition accepts records. That fact is useful only after the system answers harder questions: which events belong in the same order, how every producer derives the same routing bytes, which concurrent producer is authoritative, what retries may do, and whether broker order corresponds to the business transition consumers need.

“Order the events” is usually underspecified. A total order over every event serializes unrelated work, reduces availability and throughput, and still may not reflect physical reality. Too little order can apply a cancellation before creation, overwrite a newer balance with an older snapshot, or split one entity's state across partitions. The correct target is the smallest order domain that protects the invariant.

Keys operationalize that domain. If all transitions for one order must be sequenced, the order ID is a natural business key. If account state spans subresources, account ID may be required. If identifiers collide across tenants, use tenant plus entity. A region, event type, or request UUID may distribute well but fail the state invariant.

Key text is not the routed object; bytes are. Two clients can disagree on casing, whitespace, Unicode normalization, numeric width, field order, delimiters, escaping, encoding, or null representation. They then send the “same” business entity to different partitions. A key is therefore a schema and algorithm with compatibility tests.

Even perfect co-location establishes only a broker-local append sequence. Concurrent producers can race. Network delay can invert request arrival. Retries can duplicate or reorder batches under some configurations. A stale leader can continue writing unless fenced. Business versions, command authority, producer epochs, idempotent protocols, and conflict detection close these gaps.

## Why This Matters

Many streaming computations maintain keyed state: account balances, inventory, device status, order lifecycles, user sessions, CDC rows, feature values, and fraud profiles. When related changes route together, one partition owner can update state without cross-partition coordination. This is a major source of stream-processing scalability.

The same property creates serial bottlenecks. One celebrity, enterprise tenant, payment account, sensor fleet, or empty/default key can dominate a partition. Because required order prevents arbitrary parallel processing, adding partitions or consumers may not help. Key design is simultaneously a correctness and capacity decision.

Ordering failures are subtle because every component may look healthy. Both records exist, schemas validate, lag is zero, and the consumer processed exactly what the broker exposed—but a stale update arrived after the new one. Without a business version or causality rule, the consumer cannot distinguish a correction from regression.

Multi-language systems magnify representation risk. Java, Python, Go, JavaScript, databases, and managed connectors have different default string, integer, JSON, and hashing behavior. Language-native hash functions may be randomized or implementation-dependent. An upgrade that changes a serializer or partitioner can move keys without changing topic names.

Retries create uncertainty. A timeout does not say whether the broker accepted a record. A client retry may append a duplicate. Multiple in-flight batches may make a later batch visible before an earlier retried batch under unsafe protocols. Broker-supported idempotent production narrows this uncertainty, but its scope, session identity, sequence window, acknowledgement, and fatal-error behavior matter.

Concurrent producers are a domain issue. Two services may legitimately emit changes for one customer, but their commands can conflict. Arrival order reflects networks and broker scheduling, not automatically business precedence. Central command ownership, optimistic versions, transactions, sagas, deterministic merge, or explicit conflict events are often more honest than pretending the log decided truth.

Keys are also governance data. Plain customer IDs in broker metadata, logs, traces, dashboards, and error messages broaden exposure. Hashing can still be linkable or brute-forced. Tenant composition, access control, minimization, encryption, retention, erasure lineage, and debugging procedures belong in the key contract.

## Prerequisites and Retrieval

Retrieve the business invariant: entity/aggregate whose transitions interact; legal state machine; allowed concurrency; authoritative command/event sources; correction/reversal; expected version; multi-entity operations; conflict outcome; and whether consumers need append, causal, business-version, event-time, or effect order.

Retrieve event identity: occurrence ID issuer/scope; command/request ID; entity key/version; producer service/instance/session/epoch/sequence; correlation/causation; transaction; schema; payload digest; event/ingest/append times; and source record/offset when relayed.

Retrieve the key schema: semantic components and tenant scope; source types; canonicalization; Unicode normalization/version if text is allowed; case/whitespace policy; numeric/date/UUID representation; delimiter/length framing; encoding; null/invalid behavior; maximum size; classification; rotation/evolution; and conformance vectors.

Retrieve producer implementation: client/library/version/language; serializer; partitioner and configuration; explicit-partition behavior; partition discovery/cache; batching/linger/compression; asynchronous concurrency; callback order; retry/backoff/timeout; acknowledgement; idempotence; maximum in-flight requests; transactional/fencing identity; error classes; and shutdown/restart behavior.

Retrieve topology: topic generation; partition count and epoch; routing metadata; partition availability; expansion history; mirrors/regions; per-key/partition rates and bytes; leader placement; and whether different producers can observe topology changes at different times.

Retrieve consumer assumptions without designing groups yet: state key; expected order/version checks; duplicate handling; gaps; buffering; reordering; poison/conflict quarantine; checkpoint/effect boundary; repartition step; joins; event-time use; and materialization revision.

Retrieve capacity evidence: largest keys/tenants; key cardinality and distribution; null/default fraction; records/bytes/transactions per key and partition; burst duration; batch size; serialization/hash cost; broker request limits; state size; consumer service; checkpoint/recovery; downstream lock/row/API contention; retries; and growth.

Retrieve governance: whether keys contain direct/pseudonymous identifiers; tenant isolation; producer authority; write ACLs; schema registry; key-encryption/tokenization service; metadata/log/metric exposure; retention/deletion; legal hold; audit; and break-glass diagnostics.

Distinguish business key from routing key; logical value from encoded bytes; key schema from payload schema; hash from partitioner; routing from placement; partition co-location from causality; append from event time; send call from acceptance; acceptance from acknowledgement; acknowledgement from downstream effect; occurrence ID from producer sequence; producer session from application instance; epoch from wall-clock deployment; idempotent broker retry from application resend; per-key order from per-producer order; total order from partial order; version from timestamp; monotonicity from uniqueness; fencing from lease expiry; batching from transaction; repartitioning from partition reassignment; and pseudonymization from anonymity.

Create a producer key and order contract:

| Concern | Required decision and evidence |
|---|---|
| Invariant | Exact events/state requiring shared serialization and why |
| Business key | Components, tenant scope, authority, cardinality, correction/evolution |
| Key bytes | Canonicalization, encoding, framing, Unicode/numeric/null policy, test vectors |
| Routing | Partitioner/hash/version, topology input, explicit/null behavior, compatibility |
| Order | Append/causal/business/event/effect relation, scope, non-guarantees |
| Producer | Identity, session, epoch, sequence, concurrency, callbacks, shutdown |
| Retry | Timeout/unknown result, idempotent protocol scope, application resend identity |
| Authority | Single writer, command owner, version precondition, transaction/merge, fencing |
| Scale | Key distribution, hot-key rate/cost/state, partition/broker/sink headroom |
| Evolution | Old/new key/routing/topology epochs, cutover, state/history, rollback |
| Observability | Per-producer/key-class/partition rates, errors, duplicates, gaps, stale epochs |
| Governance | Classification, access, tokenization, metadata exposure, deletion and audit |

Write a testable claim: “For topic generation `T`, topology $\tau$, and routing version $v$, every authoritative event derives canonical bytes from key schema $K_v$; all events sharing invariant domain $d$ map to one intended partition; active producer epoch and monotone sequence/version checks reject stale, duplicate, or conflicting transitions according to policy; retry/in-flight settings preserve the claimed append order; hot-domain load fits serial capacity; and any key/routing/topology change uses an auditable migration.”

## Learning Objectives

After completing this module, you should be able to:

1. choose a business order domain from domain invariants rather than throughput intuition;
2. distinguish business, routing, partition, occurrence, producer, transaction, and consumer-state identities;
3. define deterministic cross-language key canonicalization, serialization, hashing, null handling, and conformance vectors;
4. distinguish send, append, acknowledgement, event-time, causal, business-version, delivery, and effect orders;
5. reason about multiple producers, sessions, epochs, sequences, retries, idempotence, fencing, and unknown acknowledgements;
6. detect when co-location is necessary but insufficient for a correct state transition;
7. measure and mitigate hot-key, low-cardinality, null-key, tenant, partition, state, and sink skew;
8. design key, partitioner, partition-count, region, relay, and topology migrations without silently splitting order domains;
9. specify security, privacy, authorization, observability, test, and incident controls for producer keys; and
10. reject global-order claims and choose transactions, versions, causal metadata, merge rules, or redesigned aggregates when one key is insufficient.

## Core Exposition

### Begin with the invariant, not the hash

Ask which pairs of events can change the same protected state. If two transitions commute and consumers can merge them deterministically, they may remain concurrent. If applying them in opposite orders produces an invalid result, they need one serialization or an explicit conflict protocol.

For an order lifecycle, all transitions for `order_id` may require sequence. For an account ledger, posting facts can be commutative additions while holds and overdraft decisions require coordinated account authority. For inventory, a product-level key may be too broad if stock is independently owned per warehouse; a warehouse-product key may be correct. Domain modeling decides.

Choose the smallest key that contains the invariant. A global tenant key serializes all tenant traffic, increasing latency and blast radius. A subentity key may allow two updates that violate the parent aggregate. Document examples and counterexamples, including multi-entity commands.

Do not use event type as the key unless the invariant truly spans every event of that type. Do not use the occurrence UUID when entity changes must meet. Good distribution is irrelevant if related state is split.

### Specify canonical key bytes

Producers route bytes, not abstract domain values. Define a canonical function from typed business identity to bytes. Prefer a simple stable binary or length-framed representation over ambiguous string concatenation. `(tenant="ab", account="c")` and `(tenant="a", account="bc")` must not collide because both serialize as `abc`.

For text, define accepted character repertoire, normalization form/version, case sensitivity, whitespace, locale, and encoding. Unicode canonically equivalent strings can have different code-point sequences. The Unicode Normalization Forms standard provides defined transformations, but compatibility normalization may erase distinctions important to identifiers. Often the safer rule is to route an immutable ASCII/binary internal ID rather than a human name.

For numbers, define signedness, width, endian order, decimal scale, leading zero policy, and whether `1`, `1.0`, and `01` identify the same entity. For composite keys, use schema-aware fields or explicit length prefixes. For UUIDs, choose binary 16 bytes or one canonical textual form.

Publish golden vectors: typed input, canonical semantic form, exact hex bytes, hash, and expected partition for representative topology versions. Run them in every supported language and connector. Property tests cover boundary lengths, non-ASCII, nulls, invalid encodings, and collisions in composite framing.

### Version routing as a protocol

Model routing as $p=r_v(k,\tau)$. The function includes hash algorithm, seed, sign/modulo handling, partition availability rules, explicit-partition override, null-key policy, and topology count or ranges. The client/library default is part of the version, even if no application class is named.

Never use a language runtime's native hash unless its specification and seed are deliberately stable across processes, versions, and languages. Many runtimes randomize hashes for security. Use a named deterministic algorithm required by the platform or an application routing protocol.

Apache Kafka's current producer configuration describes default logic: with a key and no explicit partition, choose using a hash of the key; with neither, choose a sticky partition for batching. It also permits custom or round-robin partitioners and can be configured to ignore keys. Therefore “Kafka keys always co-locate” is too broad; inspect effective producer configuration.

Pulsar similarly exposes routing modes and hashing choices for partitioned topics. Google Pub/Sub ordering keys are not physical partition IDs and require ordering to be enabled under documented conditions. Kinesis maps partition keys into shard hash ranges. Abstract architecture should preserve these different contracts.

### Separate order relations

Program order is the order one thread issues operations. With asynchronous APIs, several threads/tasks can call `send` concurrently. Serialization, batching, connection scheduling, retry, broker leadership, and callbacks introduce other orders. Record what the library promises for calls to the same partition.

Append order is the order positions appear in one partition. It can be authoritative for consuming that log, but it says only which append the broker accepted first under its protocol. Two independent producers can observe business events in one order and reach the broker in another.

Acknowledgement order is when futures/callbacks complete. It may differ across partitions or requests. A callback completing first does not imply its event has earlier business time. Some client APIs promise callback order for records sent to the same partition; that remains a client-scoped statement.

Event time is supplied by the domain/producer. Clocks can skew, repeat, jump, or be assigned late. Processing/append time measures system observation. Neither is a complete conflict policy. DE-057 develops time semantics.

Business version order comes from an authority for one entity: expected revision 41 transitions to 42. Consumers can reject or quarantine 40 after 42 even if it appends later. Causal order records relationships such as command caused event; concurrent unrelated events need not be totally ordered.

Effect order is what downstream systems accept or expose. Consumers can retry, parallelize, time out, or partially commit. Same-partition append order does not automatically serialize external APIs. DE-055 and DE-056 treat delivery and effects.

### Model causality and concurrency honestly

Lamport's happens-before relation captures local process order plus message send-to-receive relationships and their transitive closure. If neither $a\to b$ nor $b\to a$, events are concurrent in this model. Assigning them broker offsets creates a total local append sequence but does not reveal a pre-existing causal truth.

If concurrent events commute, accept both and derive a deterministic state. If they conflict, use authority and versions: one command handler owns the aggregate; writes carry an expected version; a transaction selects one; a deterministic merge produces a new explicit result; or the product surfaces conflict for resolution.

Do not use last-write-wins on wall-clock timestamps without accepting its loss and clock assumptions. A later timestamp can come from a skewed or stale writer. If last-writer-wins is an explicit product rule, define the logical timestamp/tie-breaker, authority, tombstones, and recovery behavior.

Multi-entity invariants cannot generally be solved by choosing one of the entity keys. A transfer touches two accounts. Options include an authoritative transaction boundary, a transfer aggregate plus idempotent postings, reservations and saga compensation, or a database/service enforcing the invariant. Adjacent messages in a partition are not an atomic multi-system transaction.

### Establish producer identity, epoch, and sequence

Give every producer role a durable identity and each live session an epoch/incarnation. A monotone sequence within `(producer identity, epoch, destination partition)` helps the broker or application detect retry duplicates, gaps, and reordering. Exact scopes vary by protocol.

Fencing requires the receiver to compare epochs or tokens, not merely trust lease time. When epoch 7 becomes active, epoch 6 writes are rejected even if its process still runs after a network pause. A random new instance ID without shared authority cannot fence an old writer.

Business version is complementary. Producer sequence proves transport order from one producer session; it does not prove entity revision if several producers emit for that entity. Store both when needed. A source database log coordinate can be the authoritative revision for CDC, while a relay producer sequence protects transport.

On restart, determine whether the protocol restores identity/epoch/sequence safely. If idempotence is session-scoped, application resending old records through a new producer may create new appends. Preserve occurrence IDs and downstream deduplication/reconciliation policy.

Treat sequence errors, fencing errors, authorization failures, incompatible protocol/version, and exhausted timeouts by their documented severity. Continuing after lost sequence state can reorder pending records. Fail closed, rotate to a new fenced epoch when permitted, and reconcile uncertain outcomes.

### Configure retry and in-flight concurrency deliberately

A producer sends batches for efficiency. If batches A then B target one partition, A can time out while B succeeds. Retrying A afterward creates B-before-A append order unless the protocol prevents it or only one request is in flight. The risk depends on client idempotence, retry, and in-flight configuration.

Apache Kafka's producer configuration explicitly warns that retries with idempotence disabled and more than one in-flight request per connection can reorder records after a failed send. Current idempotence configuration constrains acknowledgements, retries, and maximum in-flight values to preserve its documented ordering/deduplication scope. Verify the deployed client version and effective values rather than memorizing defaults.

Reducing in-flight requests to one can preserve local batch order in a simpler protocol but reduces throughput and does not solve application resends, multiple producers, business conflict, or downstream effects. Idempotent production improves retry behavior but is not an end-to-end exactly-once claim.

A timeout is an unknown result. Do not mint a new occurrence ID and blindly resend. Query/reconcile if possible, retry with the same identity under the supported protocol, or record uncertainty for downstream deduplication. Bound delivery timeout, buffers, retries, and memory; indefinite retry can hide outage and reorder business decisions relative to later channels.

### Use acknowledgements as durability evidence, not order truth

Producer acknowledgements report a service-defined acceptance/durability point. Weak acknowledgement can reduce latency while accepting loss under leader failure. Stronger replica acknowledgement improves durability within configured in-sync/failure assumptions. It does not prove domain validity or consumer effects.

Do not advance an upstream source checkpoint merely because a send future returned unless the data contract accepts that broker durability and the source-to-output identity mapping is stored. If several destinations must be written, one acknowledgement does not make them atomic.

Capture topic generation, partition, assigned offset/sequence, producer identity/epoch/sequence, occurrence ID, attempt, timestamp, and acknowledgement/error class in bounded receipts. Avoid payload leakage. These receipts support uncertain-outcome investigation and source/output reconciliation.

Callbacks can be delayed by application code. A slow callback may stall producer I/O in some clients. Keep them bounded and move heavy work out of protocol threads while preserving receipt durability and order where required.

### Handle null, missing, and invalid keys explicitly

A missing key can mean the event has no ordering relation, the producer cannot determine it, or the schema is broken. These are different. For stateful domain events that require key order, reject or quarantine missing/invalid keys before publication.

Some producers distribute unkeyed records with sticky or round-robin behavior. That can improve batching/balance but gives no stable entity co-location. Do not let a fallback empty string create one global hot partition, and do not claim downstream per-key state safety.

Validate type, length, tenant scope, canonical form, and forbidden/sentinel values. Monitor null/default rates. A surge can signal upstream parsing failure and concentrate traffic. Preserve original evidence securely in quarantine with an explicit repair/republication identity.

Explicit partition selection bypasses normal routing. Restrict it to controlled infrastructure use cases with topology awareness. A stale partition number after expansion or migration can split keys. Record and test override semantics.

### Engineer hot-key capacity

Measure rates and work per semantic key, not only hashes or partitions. One key may carry many tiny events, large payloads, expensive validation, huge state, slow external effects, or long transactions. Use heavy-hitter sketches and bounded sampled diagnostics with privacy controls.

Let hot-key offered work be $\lambda_k$ and sustainable serial-domain service be $\mu_p$. If $\lambda_k\ge\mu_p$, partition count cannot restore stability while the key remains indivisible. Bursts additionally require bounded buffers and latency/retention margin.

Mitigations change a real constraint: batch/aggregate or coalesce safe updates; cache/reference rather than duplicate large context; isolate a tenant; increase per-partition consumer/sink capacity; apply quotas/admission; split the key into independent subdomains; or relax order with an associative/commutative merge. Document semantic impact.

Key salting spreads one logical key across partitions but destroys its single append order. It is safe only when operations commute or a second stage can correctly combine/resequence using versions and bounded state. Random salting is not a free scaling switch.

### Keep key changes and topology changes explicit

Changing account key from raw `account_id` to `(tenant_id,account_id)`, changing text normalization, serializer bytes, hash, partitioner, null policy, region endpoint, or partition count can move records. Old history remains in old domains. Treat each as a routing epoch.

A safe migration inventories producers, relays, connectors, consumers, state, mirrors, archives, and downstream assumptions. Capture the old terminal or overlap cut, version new key envelopes, shadow route, compare distributions and per-key sequences, rebuild/move state, and fence stale producers.

Dual writing can validate but creates duplicate/partial-write risks. Use one authoritative occurrence ID, receipts, isolated candidate sinks, and reconciliation. A new topic generation makes incompatible routing visible and usually simplifies rollback, at the cost of copy and consumer migration.

During rolling producer deployment, old and new clients can route the same key differently. Avoid an uncontrolled mixed epoch. Gate publication through a routing service/config epoch, use compatible virtual buckets, stop-the-world at a cut where feasible, or dual-read both with explicit merge until old producers are fenced.

### Relay events without erasing source order

A relay or mirror becomes another producer. Destination partition/offset, producer sequence, and append time are new coordinates. Preserve original topic generation, partition/offset or sequence, occurrence ID, source business version, and causation in the envelope.

If relays run concurrently, define assignment so one source order domain is not raced by multiple unfenced writers. If batching combines sources, do not imply a global order. Destination key derivation must use the same declared business invariant or document intentional repartitioning.

Cross-region active-active production needs explicit authority/conflict semantics. Same ordering key in two regions may not receive one service-defined order unless the product says so. Options include home-region authority per key, globally coordinated versions, CRDT-like merge for commutative state, or conflict events. Network arrival order is not a business policy.

Validate mirrors over source cut vectors and per-key sequences, not just counts. Duplicates can preserve counts after losses; equal materialized state can hide missing audit history. Choose evidence based on the consumer contract.

### Observe producer order as a chain of evidence

Expose publication attempts, accepted records, retries, timeouts/unknowns, errors by class, buffer exhaustion, batch size, request latency, throttle, acknowledgements, duplicate/sequence/fencing errors, and metadata refresh by producer identity/version.

Expose key validity/null/default fraction, distinct/estimated cardinality, heavy-hitter load, routed partition distribution, bytes/work/state, and skew. Do not place raw high-cardinality sensitive keys in metric labels. Use restricted lookup tooling from token/digest to approved identity when needed.

Trace one occurrence from source/command through canonical key version/hash result, producer epoch/sequence, topic generation/partition/offset, consumer state/version, and output receipt. Sampling must not be the only correctness record.

Alert on stale producer epochs, sequence gaps/out-of-order errors, partitioner/config drift, mixed routing versions, unexpected explicit partitions, null-key spikes, hot-key saturation, retry storms, acknowledgement latency, and uncertain outcomes approaching reconciliation/retention limits.

### Test order claims adversarially

Golden-vector tests run key canonicalization and routing in every supported language/client/version. Include visually identical Unicode forms, case/whitespace, composite ambiguity, signed/large numbers, nulls, invalid bytes, maximum lengths, tenant collisions, and topology sizes.

Model/property tests generate event partial orders, concurrent producers, duplicates, gaps, retries, stale epochs, and version conflicts. Assert legal state-machine transitions, same-domain routing, monotone accepted authority/version, deterministic merge, and failed-closed ambiguity.

Integration tests inject delayed/lost acknowledgements, leader changes, request timeout, retry with several in-flight batches, producer crash/restart, sequence error, fencing, metadata staleness, partition unavailability, schema/key-service failure, and client upgrade. Inspect actual log order and receipts.

Load tests use measured heavy hitters, not uniform random keys. Include bursts, large payloads, compression, batch/linger settings, broker throttle, concurrent recovery, consumer state, checkpoint, and sink contention. Measure the hottest serial path.

Migration tests run old and new routing simultaneously in an isolated environment, compare per-key destinations and ordered versions over exact cuts, rebuild state, test rollback, and prove stale producer rejection. Disaster tests include relay/region failover with source-coordinate preservation.

### Secure and govern producer keys

Authorize producers by domain event type and topic, not only broad cluster write. Validate that a producer may write the claimed tenant/entity and business version. A valid credential should not permit arbitrary tenant keys or explicit partitions.

Prefer stable internal pseudonymous identifiers over emails, names, phone numbers, or external account numbers. A plain unsalted hash of a small identifier space may be reversible by enumeration and remains linkable. Tokenization/HMAC can narrow exposure but creates key-service availability, rotation, and replay dependencies.

If tokenized routing keys rotate, the same entity may route differently. Separate stable routing token from periodically rotated display/transport encryption, or migrate routing/state explicitly. Preserve authorized historical resolution for replay and deletion without exposing raw identity broadly.

Audit schema/partitioner/config changes, producer identity/epoch issuance, explicit partition use, fencing, reset, and quarantine repair. Minimize keys in logs/traces/metrics and apply retention/deletion/legal rules across broker metadata, archives, receipts, state, and dead letters.

### Review the claim at the exact scope

A strong claim reads: “For aggregate `(tenant,order)`, all authoritative transition events use key schema `order-key-v3`, route under partitioner `rv5` and topology `orders-v7`, are issued by fenced command-owner epochs, carry monotone aggregate versions, and preserve same-partition append order under the deployed idempotent retry/in-flight configuration.”

Then state what it does not mean: no total order across orders, no guarantee that producer clocks match, no automatic atomicity across orders, no proof that every application resend is deduplicated, no automatic consumer/effect order, and no capacity proof without measurement.

Review evidence should join domain state-machine tests, golden key vectors, effective client configs, broker receipts/log inspection, concurrency/failure tests, per-key load, migration drills, and security/privacy approval. A documentation sentence saying “messages with the same key are ordered” is the beginning, not the end, of the argument.

## Definitions and Notation

Let $E$ be events and $D$ be business invariant domains. Function $d:E\to D$ selects the smallest domain requiring serialization. Business key representation version $v$ produces canonical bytes

$$
k_v(e)=\operatorname{encode}_v(\operatorname{canonicalize}_v(d(e))).
$$

Let topic/topology epoch be $\tau$ with partition set $P_\tau$, and partitioner

$$
r_v:K_v\times\tau\to P_\tau.
$$

The co-location obligation is

$$
d(e_i)=d(e_j)\land \operatorname{requiresOrder}(e_i,e_j)
\Rightarrow r_v(k_v(e_i),\tau)=r_v(k_v(e_j),\tau).
$$

It is necessary, not sufficient, for correct business order.

Define relations: $\prec_s$ send-call order, $\prec_a$ broker append order, $\prec_{ack}$ acknowledgement completion order, $\prec_h$ happens-before, $\prec_v$ authoritative business-version order, $\prec_t$ event-time order, and $\prec_x$ external effect visibility order. No equality among these is assumed without mechanism and proof.

Let producer record identity be $(w,\epsilon,s)$ for writer identity $w$, epoch $\epsilon$, and producer sequence $s$ in its documented scope. Fencing rule accepts a write only if

$$
\epsilon=\operatorname{activeEpoch}(w),
$$

and sequence/version predicates hold. The occurrence ID $u(e)$ remains independent so the same logical event can be recognized across retry, new sessions, relays, and destinations.

Let $\lambda_k$ be offered work for key $k$ and $\mu_{r(k)}$ sustainable serial service in its partition/end-to-end path. A necessary stability condition is

$$
\forall k:\quad \lambda_k<\mu_{r(k)},
$$

with variance, failure, retry, and recovery headroom. Aggregate throughput can pass while one key violates this condition.

For routing change $(v,\tau)\to(v',\tau')$, moved domains are

$$
D_\Delta=\{d:r_v(k_v(d),\tau)\ne r_{v'}(k_{v'}(d),\tau')\}.
$$

The migration records old/new cut vectors, occurrence coverage, state/effect mapping, validation, authority epoch, and retirement boundary for $D_\Delta$.

## Mechanisms, Invariants, or Proof Structure

Use this producer-order review chain:

1. **Prove the invariant domain.** Identify transitions that conflict or fail to commute and select the smallest business domain that must serialize them.
2. **Prove key identity.** Define component authority, tenant scope, types, canonicalization, exact bytes, null/invalid behavior, privacy classification, and compatibility.
3. **Prove routing equivalence.** Run golden vectors in every producer/connector version and show the same domain maps to one intended partition under one topology epoch.
4. **Prove order scope.** State send, append, acknowledgement, causal, business-version, event-time, delivery, and effect relations separately.
5. **Prove writer authority.** Establish producer identity, active epoch/fencing, sequence, business version/precondition, and multi-writer conflict mechanism.
6. **Prove retry behavior.** Inspect effective idempotence, acknowledgements, in-flight batches, retry/timeouts, fatal errors, application resend identity, and unknown-result reconciliation.
7. **Prove capacity.** Measure per-key/partition bytes/work/state/sink cost under peak, burst, retry, failure, and recovery; address indivisible hot keys.
8. **Prove evolution.** Treat key/schema/serializer/hash/partitioner/topology/region changes as epochs with cuts, state/history movement, validation, fencing, rollback, and retirement.
9. **Prove observability and governance.** Detect drift, nulls, skew, retries, sequence/fencing errors, uncertain outcomes, unauthorized writers, and sensitive metadata exposure.
10. **Prove downstream limits.** Show consumers validate versions/gaps and explicitly avoid extending producer append order into unproven effect or global order.

The key invariant is:

> Every event that must share a serialization domain derives the same canonical routing bytes and destination under one named key/routing/topology epoch.

The authority invariant is:

> No stale producer epoch, duplicate attempt, lower business version, or conflicting writer silently becomes an authoritative transition merely because the broker appended it.

The order invariant is:

> Every order claim names its relation, domain, endpoints, visibility, producer concurrency, retry/in-flight conditions, and non-guarantees.

The scale invariant is:

> The hottest indivisible order domain fits the demonstrated serial end-to-end capacity with failure/recovery headroom, or the semantics/admission are redesigned explicitly.

This executable demonstrates deterministic ASCII key canonicalization, versioned routing, and stale-epoch fencing. Its SHA-256-based partitioner is illustrative, not a Kafka, Pulsar, Kinesis, or Pub/Sub compatibility claim.

<!-- bijux-verify: {"id":"producer-key-routing-and-fencing","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"routing_version=key-v1\npartition_count=8\ncanonical_key_hex=((' ACCT-17 ', '616363742d3137'), ('acct-17', '616363742d3137'), ('acct-18', '616363742d3138'))\nrouted_partitions=(('evt-40', 3), ('evt-41', 3), ('evt-stale', 3), ('evt-42', 3), ('evt-other', 0))\naccepted_ids=('evt-40', 'evt-41', 'evt-42')\nrejected_ids=('evt-stale',)\nproducer_sequences=(0, 1, 2)\nbusiness_versions=(40, 41, 42)\nsame_canonical_key_same_partition=True\nstale_epoch_fenced=True\ncross_key_order_is_not_claimed=True\nevent_time_is_not_routing_order=True\n","stderr":""}} -->
```python
import hashlib

routing_version = "key-v1"
partition_count = 8
active_epoch = 7


def canonical_key(raw_key):
    return raw_key.strip().casefold().encode("utf-8")


def route(raw_key):
    key_bytes = canonical_key(raw_key)
    digest = hashlib.sha256(routing_version.encode("ascii") + b"\0" + key_bytes).digest()
    return int.from_bytes(digest[:8], "big") % partition_count


events = (
    ("evt-40", " ACCT-17 ", 7, 0, 40),
    ("evt-41", "acct-17", 7, 1, 41),
    ("evt-stale", "acct-17", 6, 99, 42),
    ("evt-42", "acct-17", 7, 2, 42),
    ("evt-other", "acct-18", 7, 0, 1),
)

routed = tuple((event_id, route(raw_key)) for event_id, raw_key, *_ in events)
active_account_events = tuple(
    event
    for event in events
    if canonical_key(event[1]) == b"acct-17" and event[2] == active_epoch
)
rejected = tuple(
    event_id
    for event_id, raw_key, epoch, _sequence, _version in events
    if canonical_key(raw_key) == b"acct-17" and epoch != active_epoch
)

print(f"routing_version={routing_version}")
print(f"partition_count={partition_count}")
print(
    "canonical_key_hex="
    + repr(tuple((raw, canonical_key(raw).hex()) for raw in (" ACCT-17 ", "acct-17", "acct-18")))
)
print(f"routed_partitions={routed}")
print(f"accepted_ids={tuple(event[0] for event in active_account_events)}")
print(f"rejected_ids={rejected}")
print(f"producer_sequences={tuple(event[3] for event in active_account_events)}")
print(f"business_versions={tuple(event[4] for event in active_account_events)}")
print(f"same_canonical_key_same_partition={route(' ACCT-17 ') == route('acct-17')}")
print(f"stale_epoch_fenced={rejected == ('evt-stale',)}")
print("cross_key_order_is_not_claimed=True")
print("event_time_is_not_routing_order=True")
```

The model has one active writer and already ordered input. It does not simulate concurrent calls, network retry, broker acknowledgement, partition expansion, Unicode normalization, downstream effects, or real load. Those require separate evidence.

## Alternatives and Trade-Offs

**Entity key versus occurrence ID.** Entity keys co-locate related transitions but can be hot. Occurrence IDs distribute well and identify retry duplicates but split entity state. Usually route by entity domain and carry occurrence ID separately.

**Narrow versus broad aggregate.** A narrow key increases concurrency but needs coordination for parent/multi-entity invariants. A broad key simplifies those invariants but serializes more work and increases blast radius. Model state transitions before choosing.

**Raw identifier versus stable internal token.** Raw IDs simplify debugging but increase exposure and can change formatting. Stable tokens reduce disclosure but introduce issuance, collision, resolution, rotation, deletion, and availability dependencies.

**Text versus binary key encoding.** Text is inspectable and interoperable when rigorously canonicalized. Binary schemas give type/framing precision but require tooling and compatibility. Either needs golden bytes, not merely logical examples.

**Default versus custom partitioner.** Defaults reduce code and follow supported client behavior but can change across versions/configuration. Custom partitioners express durable routing or virtual buckets but become critical protocol code requiring cross-language maintenance and tests.

**One in-flight request versus idempotent pipelining.** One in flight simplifies local ordering but reduces throughput. A supported idempotent protocol can preserve order with bounded concurrency and retries, but adds identity/sequence/configuration requirements and remains scope-limited.

**Single writer versus multi-writer versions.** Single authoritative ownership simplifies order/fencing but can add hops and availability dependency. Multi-writer improves locality/availability but requires versions, conflict detection/merge, or coordination and cannot use arrival order as truth.

**Total order versus partial/causal order.** Total order makes replay simple but serializes unrelated events and can imply false precedence. Partial/causal models preserve concurrency but need consumers capable of version/conflict handling.

**Hot-key salting versus serial processing.** Salting increases parallelism but abandons direct single-key order. Preserve serial processing when the invariant truly requires it; salt only with a correct associative/commutative or resequencing design.

**In-place routing change versus new topic generation.** In-place changes reduce endpoint churn but hide mixed routing and split history. New generations make cutover/rollback explicit but require dual infrastructure, backfill/state migration, and consumer coordination.

**Broker idempotence versus application deduplication.** Broker idempotence efficiently handles documented producer retry cases. Application occurrence identity spans new sessions, relays, topics, and effects but needs retained state and conflict policy. Robust designs often use both for different scopes.

## Failure Modes and Misconceptions

**“The key is the entity.”** It may be an inconsistent string representation or a payload field without authority. Define typed identity and exact bytes.

**“Same visible text means same bytes.”** Unicode form, case, whitespace, encoding, locale, and escaping can differ. Publish canonicalization/version and golden vectors.

**“The default hash is stable.”** Runtime and client defaults can change or randomize. Name and test the effective partitioner algorithm/configuration.

**“Any key guarantees ordering.”** Clients may ignore keys, use explicit/custom routing, or require subscription ordering configuration. Inspect the complete path.

**“Same partition means correct order.”** It supplies an append order, not source causality, business authority/version, event time, or effect order.

**“Send calls are synchronous sequence.”** Async/concurrent calls, batching, connection scheduling, retries, and callbacks can differ. Test the actual client contract.

**“Acknowledgement order is append order.”** Completion can vary across requests/partitions; acknowledgement only attests to a configured acceptance point.

**“Timestamps settle conflicts.”** Clocks skew and events arrive late. Use authoritative versions, causality, or explicit merge rules.

**“Offset is entity version.”** Offset is partition-local and advances for other keys; a replay or mirror gives different coordinates. Carry business version separately.

**“Idempotent producer means exactly-once business effect.”** Its duplicate suppression has a protocol/session scope and does not cover arbitrary resends or downstream effects.

**“Retry with a new event ID is harmless.”** It defeats occurrence deduplication and can double logical action. Preserve identity and reconcile unknown outcomes.

**“A lease prevents stale writes.”** A paused holder can resume. Receivers must fence lower epochs/tokens.

**“One producer per service is one writer.”** Multiple replicas, old deployments, relays, or regions can write the same key. Define domain authority.

**“A global partition solves correctness.”** It reduces throughput/availability and still orders by arrival, not necessarily business precedence or atomic effects.

**“More partitions fixes hot keys.”** The hot ordered key remains one serial domain. Change capacity, domain semantics, isolation, or admission.

**“Salting is transparent.”** It splits history and state. A correct second-stage merge/resequence is required.

**“Adding a tenant prefix cannot hurt.”** It changes bytes and routing, splits old/new history, and requires migration even if logically desirable.

**“Rolling out a new serializer is safe.”** Mixed producers can route the same identity differently. Gate routing epochs and fence old writers.

**“Hashing makes the key anonymous.”** Stable hashes remain linkable and low-entropy domains are enumerable. Apply privacy/security analysis.

**“Ordering survives a mirror automatically.”** Destination coordinates and concurrent relay timing differ. Preserve source order domains and validate coverage.

## Worked Examples

### Example 1

An order state machine permits `Created → Paid → Fulfilled` and `Created → Cancelled`. The invariant is per order, so `tenant_id + order_id` is the routing domain. Event UUID is carried separately for deduplication. Event type is not the key because all `Paid` events need not serialize with one another, while `Paid` and `Cancelled` for the same order do.

### Example 2

Java publishes customer key `Café` in NFC UTF-8 while another client emits `Cafe` plus a combining accent. Visual equality does not imply identical bytes or hashes. The team replaces display names with immutable customer IDs for routing, specifies byte encoding, and keeps Unicode names in the payload. Cross-language golden vectors prevent recurrence.

### Example 3

Two composite keys concatenate without framing: `(tenant=ab, account=c)` and `(tenant=a, account=bc)` both become `abc`. Length-prefixed fields or a stable schema eliminate ambiguity. A delimiter alone is unsafe unless escaping and forbidden characters are specified.

### Example 4

One producer sends batch A then B to a partition. A times out, B succeeds, and A is retried. With idempotence disabled and multiple requests in flight, B can append before A. The fix uses a supported idempotent configuration or a stricter in-flight limit, preserves occurrence IDs, and verifies the actual log under injected failure.

### Example 5

Writer epoch 12 owns inventory item 7. A network-paused epoch 11 resumes and submits version 44 after epoch 12 submitted version 45. The receiver rejects epoch 11; consumers also reject lower business version. Partition append position alone would otherwise make stale state look newest.

### Example 6

Two independent services emit address verification and marketing preference for one customer. The fields commute, so forcing one global customer order is unnecessary if the materialization merges versioned subdocuments. A legal-name change and KYC decision do not commute under the same rules and remain under one authoritative workflow.

### Example 7

A null-key rate jumps from 0.01% to 30% after a parser deployment. The default producer packs unkeyed records into sticky partitions, causing bursts and splitting entity state. A validation gate quarantines records missing required account IDs, alerts on the rate, and republishes repaired events with the original occurrence identity.

### Example 8

One enterprise tenant emits 12 MiB/s while a single ordered partition path sustains 8 MiB/s. Adding 100 partitions cannot split that key. The team creates subkeys by independent facility because inventory is facility-owned, retains a tenant-level reconciliation stream, and verifies that no cross-facility invariant was lost. If such an invariant existed, admission or stronger serial capacity would be required.

### Example 9

A migration changes from eight partitions and key `account_id` to sixteen partitions and `(tenant_id,account_id)`. The team creates a new topic generation, freezes old routing at a cut vector, dual-writes isolated candidates with one occurrence ID, rebuilds state, compares per-key business versions/digests, fences old producer epochs, cuts publication, and retains old history through rollback/replay objectives.

### Example 10

A regional relay preserves source topic generation, partition, offset, occurrence ID, key-schema version, producer epoch/sequence, and business version. Destination offsets differ. During failover, the new region accepts only higher home-epoch tokens per key and reconciles the source cut. It does not infer global order by comparing destination arrival times.

## Cross-Program Connections

Domain-driven design contributes aggregates, invariants, commands, events, entity identity, bounded contexts, and ownership. Routing keys should follow domain consistency boundaries rather than infrastructure convenience.

Distributed systems contributes happens-before, partial order, logical clocks, leader epochs, fencing, idempotent protocols, consensus, transactions, replication, and failure uncertainty. Broker arrival order is one protocol outcome inside this larger model.

Data structures and algorithms contribute canonical encoding, hash functions, consistent hashing, collision domains, heavy hitters, skew, commutative/associative operations, stable sorting, and merge algorithms.

Database systems contributes primary/composite keys, optimistic versions, transaction serialization, compare-and-set, write-ahead-log coordinates, CDC ordering, materialized state, and conflict resolution.

API and service engineering contributes idempotency keys, request identity, conditional writes, ETags/versions, retries/timeouts, rate limits, authentication, authorization, and asynchronous callback semantics.

Security engineering contributes producer identity, message integrity, fencing authority, least privilege, tenant separation, tokenization/HMAC key management, metadata protection, audit, and denial-of-service controls.

Privacy engineering contributes minimization, purpose limitation, pseudonymization/linkability, retention/deletion, identifier rotation, and lineage across topics, receipts, archives, dead letters, and state.

Formal methods contributes state machines, partial orders, invariants, refinement, model checking, commutativity proofs, and property tests for concurrent histories.

Performance engineering contributes batching, compression, asynchronous pipelines, service capacity, head-of-line blocking, hot-key analysis, tail latency, and recovery throughput.

Site reliability engineering contributes per-key/partition telemetry, retry-storm control, overload admission, config drift, incident reconciliation, migration drills, and evidence-scoped reliability claims.

## References

1. Apache Kafka. [Producer Configuration, Apache Kafka 4.3](https://kafka.apache.org/43/generated/producer_config.html). Accessed 2026-09-03. Primary configuration reference for key routing, partitioners, retries, acknowledgements, idempotence, and maximum in-flight requests.
2. Apache Kafka. [KafkaProducer API, Apache Kafka 4.3](https://kafka.apache.org/43/javadoc/org/apache/kafka/clients/producer/KafkaProducer.html). Accessed 2026-09-03. Primary client documentation for asynchronous sends, callbacks, idempotent/transactional producer scope, ordering, and error handling.
3. Apache Kafka. [ProducerRecord API, Apache Kafka 4.3](https://kafka.apache.org/43/javadoc/org/apache/kafka/clients/producer/ProducerRecord.html). Accessed 2026-09-03. Primary API documentation for topic, optional partition, key, value, headers, and timestamp fields.
4. Apache Kafka. [Design, Apache Kafka 4.3](https://kafka.apache.org/43/design/design/). Accessed 2026-09-03. Primary design documentation for partitioning, ordering, replication, message delivery, idempotence, and transactions.
5. Apache Kafka. [OutOfOrderSequenceException API, Apache Kafka 4.3](https://kafka.apache.org/43/javadoc/org/apache/kafka/common/errors/OutOfOrderSequenceException.html). Accessed 2026-09-03. Primary API documentation for sequence-state failure and reordering risk.
6. Apache Pulsar. [Messaging Concepts, Apache Pulsar 4.2](https://pulsar.apache.org/docs/4.2.x/concepts-messaging/). Accessed 2026-09-03. Primary documentation for message keys, sequence IDs, partitioned-topic routing modes, hashing, producer access, and ordering scopes.
7. Amazon Web Services. [Develop Producers Using the Amazon Kinesis Data Streams API](https://docs.aws.amazon.com/streams/latest/dev/developing-producers-with-sdk.html). Accessed 2026-09-03. Primary documentation for partition keys, assigned sequence numbers, ordered `PutRecord`, and batch behavior.
8. Amazon Web Services. [PutRecord API](https://docs.aws.amazon.com/kinesis/latest/APIReference/API_PutRecord.html). Accessed 2026-09-03. Primary API reference for partition-key mapping, explicit hash keys, sequence numbers, and `SequenceNumberForOrdering`.
9. Google Cloud. [Order Messages in Pub/Sub](https://cloud.google.com/pubsub/docs/ordering). Accessed 2026-09-03. Primary documentation for ordering-key scope, regional publication, subscription configuration, redelivery, and throughput considerations.
10. Unicode Consortium. [Unicode Standard Annex #15: Unicode Normalization Forms](https://www.unicode.org/reports/tr15/). Accessed 2026-09-03. Normative standard for canonical and compatibility normalization of Unicode strings.
11. Lamport, Leslie. [Time, Clocks, and the Ordering of Events in a Distributed System](https://lamport.azurewebsites.net/pubs/time-clocks.pdf). *Communications of the ACM* 21(7), 1978. Primary paper defining happens-before, concurrent events, and logical-clock ordering.

## Exercises

### Exercise 1

Choose routing domains for: order lifecycle transitions; warehouse-specific inventory; a transfer touching two accounts; immutable page-view facts; and customer profile fields independently owned by legal-name and marketing-preference workflows. State the invariant, whether operations commute, and what authority/version/coordination is required beyond co-location.

### Exercise 2

Define exact canonical bytes for composite `(tenant_id, account_number)` where tenant is an unsigned 32-bit integer and account number is a case-sensitive ASCII string up to 32 bytes. Show why delimiter-free concatenation is ambiguous, encode `(7,"A12")` in hex under your design, and list at least six cross-language golden-vector cases.

### Exercise 3

Producer batch A contains entity versions 10 and 11; batch B contains version 12 for the same partition. A times out, B succeeds, then A retries. Analyze possible append order when retries are enabled, idempotence disabled, and two requests can be in flight. Compare one-in-flight and supported idempotent configurations, and explain which business/end-to-end guarantees still remain unproven.

### Exercise 4

A hot account emits 9,000 events/s. Its partition path sustains 7,500 events/s normally and 5,000 during one-broker recovery. The topic overall has large spare capacity. Compute backlog growth over 20 minutes under normal and recovery capacity. Propose semantic and operational responses without claiming that more partitions alone solve it.

### Exercise 5

Design a migration from key schema `account-id-v1` on 12 partitions to tenant-scoped `tenant-account-v2` on 24 partitions across three producer languages and a regional mirror. Include golden vectors, routing epochs, old/new cuts, concurrent producers, state, occurrence IDs, fencing, validation, rollback, privacy, and retirement. State the exact order claim after migration.

## Answers to the Exercises

### Answer 1

Order lifecycle transitions use `(tenant,order)` because state transitions conflict; one authoritative command workflow or expected aggregate version/fencing supplements co-location. Inventory uses `(warehouse,product)` if warehouses own independent quantities and cross-warehouse totals are derived; a global reservation invariant needs separate coordination. A transfer cannot become atomic by choosing source or destination account: use a transaction authority or transfer aggregate with idempotent postings/reservations and compensation. Immutable page views normally commute and can use distribution-oriented keys while carrying occurrence identity; session order is added only if the product needs it. Legal-name and marketing preference fields can be versioned subdocuments that merge because they are independently owned; if policy couples them, a broader profile authority or explicit workflow is required. In every case append order is not itself business authority.

### Answer 2

Use a version byte, four-byte big-endian unsigned tenant, two-byte big-endian account length, then exact ASCII account bytes. For `(7,"A12")`, bytes are version `01`, tenant `00000007`, length `0003`, value `413132`, yielding hex `01000000070003413132`. Delimiter-free concatenation makes `(tenant="1",account="23")` and `(tenant="12",account="3")` both `123` in a textual scheme. Golden cases include tenant 0 and $2^{32}-1$, empty account if allowed/rejected, one/32/33-byte accounts, `A12` versus `a12`, delimiter characters, non-ASCII rejection, leading zeros, null/missing fields, invalid UTF-8 at boundaries, and known partition outputs for every supported topology. All languages must produce identical bytes, errors, hashes, and routes.

### Answer 3

With two batches in flight, B can append while A's result is unknown; retrying A can yield versions `12,10,11`, and the timeout can also create duplicates depending on whether A originally appended. Limiting to one in flight prevents B from overtaking unresolved A within that producer/connection but reduces concurrency and does not handle multiple writers or arbitrary application resends. A correctly supported idempotent configuration uses producer identity/sequences and compatible acknowledgement/retry/in-flight constraints to preserve its documented same-partition ordering and retry deduplication scope. None of these proves business authority/version validity, source occurrence uniqueness across new sessions, cross-partition/global order, consumer processing, external effect order, or end-to-end exactly-once outcomes; those require separate protocols and evidence.

### Answer 4

Normal deficit is $9{,}000-7{,}500=1{,}500$ events/s, so 20 minutes produces $1{,}500\times1{,}200=1{,}800{,}000$ queued events. During recovery the deficit is 4,000/s, producing 4,800,000 in 20 minutes. Aggregate spare capacity is unusable while the account is one ordered domain. Responses include admission/rate limits or degraded latency, improving demonstrated serial processing/sink capacity, coalescing safe updates, isolating the tenant, or redesigning the invariant into independent subaccounts/facilities with explicit reconciliation. Salting is valid only if operations commute or a correct resequencing/merge layer restores required semantics. Extend retention and monitor backlog age while recovery capacity is below arrival.

### Answer 5

Publish a typed `tenant-account-v2` specification with Unicode/text restrictions, framing, hash/partitioner versions, null rules, and golden input/hex/hash/partition vectors run in all three languages and mirror code. Create a new topic/topology generation with 24 partitions. Inventory old producers/consumers/state, issue a routing epoch, and capture the complete 12-partition old cut plus the new empty/start cut. Use one controlled cutover or dual-write with stable occurrence IDs and receipts; fence old producer epochs so mixed routing cannot persist. Rebuild/migrate keyed state from old source coordinates, shadow-consume new candidates, and compare per-entity business-version sequences, counts/digests/materializations, skew/capacity, and mirror source-cut coverage. Roll back by fencing the new epoch and resuming from preserved old state/cuts, not by guessing offsets. Use stable internal tenant/account tokens and govern lookup/deletion. Retain old topic, mappings, schemas, keys, state, and mirror lineage through rollback/replay obligations. The final claim is only that authoritative events for one `(tenant,account)` route to one partition and preserve the deployed producer protocol's same-partition append order within the new epoch; it is not global, event-time, delivery, or effect order.
