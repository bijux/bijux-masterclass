---
module_id: API-075
program: API & Service Engineering
level: 2
module_number: 75
title: Backpressure Across Service Boundaries
status: complete
last_verified: 2026-09-02
---

# Backpressure Across Service Boundaries

## One-Page Review

### Governing question

How can a slower receiver communicate finite demand through transports, APIs, queues, fan-out, and asynchronous workers so every buffer stays bounded and no layer converts waiting into hidden overload?

### Essential definitions

- **backpressure** is feedback from a constrained downstream that causes upstream production or delivery to slow, pause, or stop.
- **demand** or **credit** is bounded permission to send elements, bytes, messages, or work.
- A **window** is outstanding credit over a scope such as stream, connection, consumer, partition, or tenant.
- **flow control** regulates transmission over a protocol hop; it may not regulate application processing or the complete call graph.
- **prefetch** is delivery granted before individual processing acknowledgements.
- An **acknowledgement** confirms a precisely defined milestone such as receipt, durable acceptance, or completed processing.
- A **buffer** decouples temporary rate mismatch; a **backlog** is retained uncompleted work.
- **pressure translation** maps one boundary's capacity signal into bounded demand at the next boundary.

### Central model, mechanism, or theorem

For one receiver, let cumulative granted demand be $D(t)$, delivered elements $N(t)$, and cancelled/expired unused credit $X(t)$. A credit protocol preserves

$$
0\le N(t)\le D(t),\qquad O(t)=D(t)-N(t)-X(t)\le W,
$$

where $O(t)$ is outstanding usable credit and $W$ its configured bound. Across a pipeline, every hop needs its own bounded window, buffer, deadline, and acknowledgement semantics. A bound on transport bytes does not prove a bound on decoded objects, database work, fan-out, or durable backlog.

### Critical invariants

The receiver controls future demand, the sender never exceeds granted credit, and credit scope/unit/expiry are explicit. Every buffer has a count or byte bound plus age/deadline policy. Cancellation revokes interest and releases resources. Acknowledgement is issued only at its documented milestone and does not imply downstream completion unless the contract says so.

Pressure crosses every asynchronous boundary: network, runtime, executor, broker, database, and downstream call. Fan-out consumes downstream capacity rather than duplicating one upstream credit into unlimited work. Control messages remain processable while data is paused. Recovery replenishes credit gradually and fairly.

### Common failures

“Async” means unbounded queue; transport windows are mistaken for application backpressure; byte credit ignores object expansion; writes return after local buffering and are treated as sent; demand is granted in unlimited batches; acknowledgements precede processing; pause arrives after an unbounded in-flight burst; consumers stop polling and lose leases; fan-out multiplies one item into hundreds of calls; merge takes unlimited input from a fast source; all tenants share one credit pool; both duplex peers wait to read until writes finish; control frames are blocked behind data; cancellation leaves producer work running; restart forgets outstanding ownership; and recovery releases the entire backlog at once.

### Compact example

A consumer processes 200 messages/s with 100 ms mean service time, so about 20 messages are concurrently useful. Prefetch 1 underuses a high-latency broker link; unlimited prefetch can fill heap. A tested prefetch of 40 bounds delivered-but-unacknowledged messages while overlapping delivery and work. If processing slows to 50/s, acknowledgements replenish credit more slowly and broker delivery naturally falls. **Conclusion:** receiver-issued credit turns processing rate into upstream pacing without an unbounded client queue.

### Connections

[Delivery and Acknowledgment](066-delivery-and-acknowledgment.md) defines milestone truth, [Timeout and Deadline Budgets](071-timeout-and-deadline-budgets.md) removes obsolete demand, and [API-Level Load Shedding](074-api-level-load-shedding.md) rejects when upstream cannot or will not slow. The next modules treat cache invalidation, fan-out tails, and hedging.

## Governing Question

For every producer-consumer boundary, who owns the demand signal, in what unit and scope, how is it replenished or revoked, where may work wait, and what happens when the source cannot slow or the signal cannot propagate end to end?

## Why This Matters

Distributed systems routinely connect components with different and changing rates. A network can deliver faster than an application decodes; an API can accept faster than a database commits; a broker can push faster than a consumer processes; a service can read one event and fan out 100 calls. Without feedback, the mismatch accumulates in memory, socket buffers, executor queues, broker lag, or downstream retries until a limit fails abruptly.

Backpressure changes the contract from “send and hope” to “send within receiver-advertised capacity.” Reactive Streams requires a publisher never to signal more elements than a subscriber requested. HTTP/2 uses receiver-controlled byte windows at stream and connection scope. gRPC flow control uses transport feedback for streaming messages and warns that a completed write call need not mean bytes have gone on the network. RabbitMQ prefetch bounds unacknowledged deliveries. Each is valuable, and each has a narrower scope than an end-to-end service workflow.

A system is only bounded if pressure is translated across all boundaries. A proxy may stop reading network bytes but have already buffered bodies. An application may request one event then issue 1,000 parallel downstream calls. A consumer may pause delivery while an unbounded executor queue continues growing. Inspect the complete path rather than checking a protocol feature box.

Backpressure also affects correctness. Acknowledgements determine redelivery; cancellation determines whether effects continue; pausing partitions can affect leases and ordering; changing windows can race with in-flight work. Capacity feedback must preserve identity, deadlines, order, fairness, and outcome semantics.

## Prerequisites and Retrieval

Retrieve [Unary and Streaming gRPC](053-unary-and-streaming-grpc.md), [Delivery and Acknowledgment](066-delivery-and-acknowledgment.md), [Idempotent Consumers](067-idempotent-consumers.md), [Timeout and Deadline Budgets](071-timeout-and-deadline-budgets.md), [Circuit Breaking and Bulkheads](073-circuit-breaking-and-bulkheads.md), and [API-Level Load Shedding](074-api-level-load-shedding.md).

Retrieve transport and library flow-control defaults; stream/connection windows; write-buffer behavior; maximum message and decoded size; publisher/consumer rate distributions; broker prefetch, acknowledgement, lease, poll, retention, and partition semantics; every runtime/executor/driver queue; fan-out factors; concurrency/cost limits; deadlines/cancellation; ordering/idempotency; autoscaling/rebalancing; tenant priority; and metrics for credit, buffer, lag, pause, acknowledgements, redelivery, and blocked time.

## Learning Objectives

After completing this module, you can:

1. distinguish backpressure, hop flow control, admission, load shedding, rate limiting, and durable buffering;
2. specify credit unit, scope, lifetime, replenishment, cancellation, and acknowledgement semantics;
3. find every buffer and asynchronous boundary in an end-to-end path;
4. translate transport capacity into application processing and downstream demand;
5. size windows/prefetch to balance bounded memory, latency, and throughput;
6. prevent fan-out, merge, retries, and batching from violating demand conservation;
7. handle sources that cannot slow using bounded drop, sample, coalesce, spill, or rejection policies;
8. preserve fairness, order, leases, idempotency, and truthful acknowledgements;
9. observe pressure propagation, blocked time, lag, buffer age, and useful throughput; and
10. verify deadlock freedom, bounds, failure, cancellation, restart, rebalance, and recovery.

## Core Exposition

### Separate feedback from rejection and storage

Backpressure asks the producer to reduce future delivery because the receiver lacks current capacity. Load shedding rejects excess work when reduction is too late or impossible. Rate limiting constrains arrivals over time. Admission decides whether work may consume a resource. A durable queue stores accepted responsibility for later processing.

Blocking a synchronous caller is implicit backpressure only if it does not consume a scarce resource indefinitely and the caller responds by slowing. If the caller spawns another thread/request, blocking merely relocates the queue. A `503` is rejection with optional pushback, not proof that the client will slow.

Backpressure does not create capacity. It propagates the bottleneck toward a point where production can pause, work can be deferred durably, or excess can be shed intentionally. If the ultimate source is a human click, device interrupt, market feed, or external webhook that cannot slow, an explicit terminal policy is required.

### Define credit as a protocol

Specify who grants credit, which sender may spend it, its unit (elements, bytes, cost, concurrency), scope (subscription, stream, connection, tenant, partition), maximum, expiry, and behavior across reconnect/restart. Specify whether credit is cumulative or incremental and how overflow is prevented.

In a demand protocol, delivery never exceeds granted demand. Reactive Streams states this as total `onNext` signals no greater than requested elements. Credit can be replenished one at a time or in batches. Larger batches amortize feedback latency but allow more outstanding work; smaller batches tighten bounds but can underutilize the path.

Credit is permission, not reservation of successful completion. A publisher can terminate early or fail. A receiver can cancel. Duplicate, delayed, or reordered control signals need sequence/generation rules when the protocol does not already guarantee them.

Avoid “unlimited” sentinels unless resource safety is proven elsewhere. A signed integer overflow in cumulative demand can turn a bound into permission for arbitrary delivery. Saturating arithmetic and protocol conformance tests are required.

### Distinguish units and expansion

HTTP/2 flow control is byte-oriented, directional, and hop-specific at stream and connection levels. It controls `DATA` transmission, not all frames and not decoded application objects. A compressed 1 MB body can inflate to 100 MB; one 1 KB message can trigger a million-row query.

Element credit is only meaningful when element cost is bounded. Apply maximum encoded/decoded sizes, decompression ratios, parse depth, batch cardinality, fan-out, and cost gates. For heterogeneous messages, use cost-weighted demand or multiple resource gates rather than assuming ten elements have ten equal costs.

Transport and application windows can coexist. Keep enough transport credit to use the bandwidth-delay product while limiting application delivery based on processing capacity. Too-small byte windows throttle healthy throughput; too-large windows allow memory commitment. Measure rather than copy defaults.

### Inventory every hidden buffer

Trace from producer to final effect: client queue, kernel send buffer, proxy body buffer, transport window, kernel receive buffer, decoder, framework channel, event-loop mailbox, executor queue, broker prefetch, application batch, driver pool, database queue, downstream client, response buffer, and retry scheduler.

For each, record maximum count/bytes, ownership, age, deadline, priority/order, cancellation, observability, and overflow action. “Bounded upstream” does not bound a downstream queue created after acknowledgement or decoding.

Library calls often return after copying to a local buffer. gRPC notes that a stream write handed to the framework has not necessarily left over the network. Treat writability/readiness callbacks as capacity hints with documented semantics, not delivery or processing acknowledgements.

Measure total in-system work, not only each queue separately. Ten layers each buffering 1,000 items create 10,000-item latency and memory potential. Prefer few intentional queues near the component able to schedule fairly.

### Translate pressure across a synchronous call graph

For unary request/response, bound caller concurrency and propagate deadlines/cancellation. A saturated downstream reduces upstream admission permits; the upstream then stops accepting or sheds rather than queueing unlimited tasks. The response time itself is a weak, delayed signal and can trigger retries.

Do not hold upstream resources while waiting without a bound. Use bulkheads and deadline-aware acquisition. If service A can handle 1,000 requests but calls B, whose safe concurrency is 100, A must expose or absorb that smaller capacity—ideally by limiting B-dependent admissions rather than filling 900 waiters.

Pushback should reach the origin without losing scope. B's tenant-specific quota must not become A's global outage; B's global overload should not be translated as caller validation. Preserve reason, retryability, delay window, and original deadline.

When upstream cannot slow, A sheds or degrades before expensive work. Backpressure and load shedding form a control loop, not competing designs.

### Control streams end to end

Streaming transports can bound network bytes while the application eagerly requests/dequeues messages into an unbounded channel. Connect receiver consumption to application readiness: grant more demand only after buffer space or processing capacity becomes available.

Use separate stream and connection accounting. One large/slow stream must not consume all connection credit and stall unrelated control or interactive streams. HTTP/2 retains control-frame progress outside `DATA` flow control, but implementations still must read frames promptly to avoid deadlock.

For bidirectional streams, read while writing. gRPC warns that both peers using synchronous/manual flow control can deadlock if each performs many writes and waits without reading. Dedicate concurrent read/control progress, bound writes, and test both windows reaching zero.

Cancellation stops future demand, clears queued unsent messages, propagates upstream, and terminates downstream work where safe. Define what happens to messages already delivered and effects already admitted. Stream resumption preserves sequence/offset and does not replay beyond idempotency guarantees.

### Use acknowledgement and prefetch correctly

Broker prefetch is a credit window for delivered but unacknowledged messages. RabbitMQ documents that reaching the configured prefetch count stops further delivery until acknowledgements replenish the window. Prefetch 0 in that protocol means no limit, not zero delivery.

Set acknowledgement at the contract milestone. Ack-after-receive maximizes flow but can lose work on consumer failure. Ack-after-durable handoff can be safe if that store owns redelivery. Ack-after-effect bounds outstanding processing but requires idempotent redelivery and lease/visibility management. Never ack merely to obtain more credit while work remains only in volatile memory.

Prefetch balances throughput against memory, fairness, and recovery. With mean processing rate $\mu$ and round-trip/control delay $R$, at least roughly $\mu R$ items may be needed to keep the consumer busy, plus measured concurrency headroom. Large prefetch hoards work from other consumers and delays priority/rebalance; prefetch one may serialize a long-latency path.

When changing prefetch or pausing, allow already in-flight delivery races. The effective bound includes preexisting outstanding messages and protocol behavior. Measure actual maximum rather than assuming a configuration applies retroactively.

### Preserve leases, ordering, and rebalances

Some pull consumers must poll or heartbeat to retain partition ownership even while application processing is paused. Separate control-plane liveness from data demand. If processing exceeds lease/visibility timeout, renew within policy or allow redelivery; do not hide stuck work forever.

Pause/resume by partition or key when order is local. A hot partition can stop without blocking all unrelated partitions, but unbounded broker lag still has retention and recovery cost. Track oldest age, not only count.

On rebalance, stop new demand, drain or cancel bounded in-flight work, commit only completed positions according to delivery semantics, and transfer ownership. An offset commit is not proof that external effects committed unless the design couples them.

Large prefetch weakens broker priority because lower-priority messages already reside at consumers. Keep enough work at the scheduler/broker to preserve fair or priority choice.

### Conserve demand through fan-out and merge

One upstream item can expand into $F$ downstream calls. If $I$ upstream items are concurrent, worst downstream demand is $IF$ absent another cap. One element of upstream credit cannot authorize unlimited fan-out. Acquire downstream permits incrementally, cap parallel branches, or reduce upstream credit based on expected/worst expansion.

For joins, avoid reading one fast input without bound while waiting for a slow counterpart. Bound per-key/window state, apply watermarks/timeouts, spill durably with retention, or shed incomplete joins. Backpressure each source independently while respecting correctness.

For merge, distribute downstream demand fairly across sources. A fast source must not consume every credit before a sparse high-priority source arrives. For broadcast, the slowest subscriber can stall all if delivery is coupled; choose whether to isolate buffers, drop slow subscribers, replay from durable log, or use independent offsets.

Batching trades efficiency for latency and credit granularity. A credit of one batch must include a maximum batch size/cost. Flush on size or time/deadline, and do not retain an incomplete batch forever during low traffic.

### Handle sources that cannot slow

Clock ticks, sensors, market data, logs, user actions, and third-party callbacks may continue regardless of demand. Choose an explicit bounded policy: drop newest, drop oldest, sample, coalesce by key, retain latest state, aggregate, spill to a capacity-governed durable log, or reject at ingress.

The policy follows semantics. Dropping intermediate temperature samples may be acceptable if the latest value and gap are visible; dropping financial commands is not. A durable log defers processing but is not infinite—bound retention, partitions, disk, recovery rate, and producer admission.

Expose loss/gaps and sequence. Silent dropping makes downstream conclusions false. For commands, preserve idempotency and return acceptance only after durable responsibility transfers.

Backpressure hostile/uncooperative sources with quotas and shedding. Do not let a well-behaved receiver's pause become an unbounded ingress queue controlled by an attacker.

### Avoid feedback instability and deadlock

Signals have delay. Granting large credit from stale capacity creates oscillation; cutting to zero everywhere can idle the pipeline. Use bounded windows, low/high watermarks, hysteresis, gradual adjustment, and local safety limits.

Credit cycles can deadlock. A waits for B to read before granting response credit; B waits for A's response before reading. Control traffic may require reserved capacity and concurrent processing. Draw the wait-for graph for duplex streams, transaction callbacks, and nested queues.

Do not perform blocking demand callbacks while holding locks needed by completion or cancellation. Reactive-style protocols require nonblocking asynchronous signaling for this reason. Avoid recursive synchronous request/delivery loops that overflow stacks or violate serialization.

Recovery is a pressure event. After pause, a large durable backlog and many producers may resume together. Increase credit in cohorts, prioritize age/criticality fairly, cap retries/fan-out, and monitor downstream saturation.

### Allocate pressure fairly

Use per-tenant, operation, priority, partition, or stream windows plus a bounded shared pool. One slow tenant must not reduce every consumer to zero; one fast tenant must not spend all shared credit. Borrow unused capacity only under explicit reclaim rules.

Credit should follow processing capacity when workers scale, but per-instance windows multiply. One hundred consumers each prefetching 1,000 create 100,000 in-flight messages. Autoscaling may increase memory and broker pressure before adding useful processing.

Priority metadata is authenticated and cannot increase across service boundaries. Reserve control traffic without an unlimited internal bypass. Age or floor lower-priority work to prevent indefinite starvation.

Account for cost, not only messages. Large payloads, expensive keys, and high fan-out consume weighted permits. Report fairness in both count and resource units.

### Observe the control loop

At every boundary record demand granted/used/outstanding; window and configuration generation; buffer count/bytes/oldest age; producer blocked time; consumer idle/processing time; pause/resume duration; acknowledgement latency and milestone; delivery/redelivery; cancellation; drops/spills; lag; and control errors.

Correlate these with throughput/goodput, deadline misses, memory, connection windows, executor queues, downstream permits, retry/fan-out amplification, autoscaling, partition rebalances, and tenant fairness. A zero queue can mean perfect matching or a starved receiver; interpret it with utilization and blocked time.

Trace one item's credit, delivery, processing, child work, acknowledgement, and cancellation without unbounded labels. Surface invisible library buffers and transport stalls through runtime diagnostics.

Alert on monotonically growing backlog, oldest age near retention/deadline, full windows with idle workers, zero windows without saturation, publishers blocked beyond deadline, ack-before-effect, redelivery loops, slow-subscriber isolation failure, and synchronized resume.

### Verify bounds and recovery

Test fast producer/slow consumer, slow producer/fast consumer, sudden stop, oscillating capacity, heterogeneous sizes/costs, decompression expansion, fan-out, join skew, slow subscriber, broker partition, network loss, cancellation, deadline, retry, and process crash at every acknowledgement boundary.

Fill every window and buffer. Prove observed maxima include races and in-flight work. Test credit overflow, duplicate/delayed control, reconnect, restart, rebalance, lease expiry, consumer scaling, and recovery from a retention-sized backlog.

For duplex streams, force both sides to exhaust send credit while control/read processing continues. Verify no lock/resource cycle. For sources that cannot slow, validate exact drop/coalesce/spill semantics and gap visibility.

Check invariants automatically: delivered never exceeds granted demand; buffers and age stay bounded; cancellation stops new delivery; ack never precedes its milestone; fan-out stays within downstream permits; control progresses under data pressure; tenant reserve holds; and reducing production allows every queue to drain without restart.

## Definitions and Notation

Let $D(t)$ be cumulative demand granted, $N(t)$ cumulative elements delivered, $X(t)$ unused credit revoked by cancellation/expiry, $O(t)=D(t)-N(t)-X(t)$ outstanding credit, and $W$ its bound. Let $B_j$ be buffer occupancy at boundary $j$ with bound $K_j$.

Let producer rate be $\lambda$, consumer service rate $\mu$, feedback/control round-trip $R$, prefetch $P$, mean service time $S$, upstream concurrency $I$, and fan-out $F$. Stable long-run operation requires effective admitted $\lambda<\mu$ or a terminal shedding/storage policy. Approximate pipeline fill $\mu R$ is only a starting estimate; variability, concurrency, batch, and cost require measurement.

A **push** source initiates delivery; a **pull** consumer requests/fetches work. A **watermark** is a buffer threshold that changes demand. A **slow consumer** cannot keep up with delivered work. A **credit leak** loses usable permission; **overdelivery** violates it.

## Mechanisms, Invariants, or Proof Structure

**Credit-bound argument.** If delivery atomically spends one unit of valid credit, the sender never creates delivery without credit, and cancellation subtracts unused credit, then $0\le O(t)\le W$ and $N(t)\le D(t)$. This bounds the credited unit only; byte/object/cost expansion can violate resource safety.

**Pipeline-bound argument.** If each boundary $j$ enforces $B_j\le K_j$, then buffered items across $m$ boundaries are at most $\sum_{j=1}^{m}K_j$, plus explicitly bounded in-service and transport work. One unbounded hidden queue invalidates the end-to-end bound.

**Fan-out counterexample.** With $I=50$ upstream items and $F=20$ branches, naive fan-out creates 1,000 downstream calls although upstream concurrency is only 50. A downstream semaphore of 100 and incremental scheduling bounds calls but can increase upstream residence, so deadlines and admission must also shrink upstream demand.

**Rate mismatch argument.** If $\lambda>\mu$ indefinitely and the source cannot slow, backlog grows at average $\lambda-\mu$ until storage fills. Backpressure alone cannot stabilize the source; drop, coalesce, shed, or durable bounded retention is necessary.

Operational invariants are: demand precedes delivery; every unit/scope is explicit; all queues are bounded and expiring; acknowledgements mean one milestone; cancellation propagates; fan-out spends downstream capacity; order/leases survive pause; control cannot be blocked by data; fairness is bounded; and recovery replenishes credit gradually.

## Alternatives and Trade-Offs

Push with credit can minimize latency and preserve receiver bounds; pull makes demand explicit but polling can waste work and complicate latency/leases. Hybrid long polling and streaming amortize requests while keeping receiver control.

Small windows reduce memory and improve fairness/cancellation but can underutilize high-latency links. Large windows improve throughput but hoard work, delay priority, magnify restart/redelivery, and consume memory. Cost-weighted credit is safer for heterogeneous work but more complex than element count.

Blocking propagates pressure simply in synchronous code but can exhaust threads or deadlock. Nonblocking demand preserves resources but requires careful serialization, cancellation, and lifecycle design.

Memory buffers are fast but volatile and finite. Durable logs decouple rates and survive failure but add storage, lag, retention, replay, ordering, and recovery obligations. Dropping/coalescing is efficient only when semantics permit loss.

End-to-end protocols provide stronger control but require shared semantics. Hop-by-hop translation fits heterogeneous systems yet every adapter can overbuffer, acknowledge early, or lose priority/deadline.

## Failure Modes and Misconceptions

- “HTTP/2/gRPC gives end-to-end backpressure.” Transport flow control is hop-local and does not price application work.
- “A returned write means delivered.” It may mean copied into a framework buffer.
- “Async means scalable.” An unbounded asynchronous queue is delayed failure.
- “Credit in messages bounds memory.” Encoded/decoded size and cost can vary drastically.
- “Pause is instantaneous.” In-flight deliveries and signal delay remain.
- “Ack means processed.” Only the documented milestone determines meaning.
- “Unlimited prefetch maximizes throughput safely.” It can exhaust consumers and hoard work.
- “Prefetch one is always safest.” It can leave a high-latency consumer idle and reduce useful throughput.
- “Broker backlog solves overload.” Retention and recovery capacity are finite.
- “One upstream permit equals one downstream permit.” Fan-out multiplies demand.
- “A slow subscriber should stall everyone.” Broadcast policy may isolate, replay, or drop it explicitly.
- “Stop polling when paused.” Some systems require heartbeats/polls to preserve ownership.
- “More consumers reduce lag.” Per-consumer windows multiply and partitions/resources may not scale.
- “Blocking both duplex writers is safe.” Neither side may read the credit needed for progress.
- “Cancellation only affects the caller.” Producers, queues, and child operations must release interest.
- “Queues are bounded individually, so latency is bounded.” Bounds add across layers and service time varies.
- “Resume at full speed after recovery.” Backlog release can recreate the incident.

## Worked Examples

### Example 1

A subscriber requests 32 elements. The publisher delivers 20; outstanding demand is 12. The subscriber cancels and revokes the unused 12. A delayed producer cannot deliver element 21 under the old generation. The trace preserves $N\le D$ and prevents post-cancellation buffer growth.

### Example 2

A consumer processes 200 messages/s and feedback round-trip is 100 ms, so $\mu R=20$ messages approximate the minimum pipeline fill. Engineers test prefetch 40 for variance. When processing drops to 50/s, acknowledgements slow and delivery follows; at most the effective window plus documented race remains outstanding.

### Example 3

HTTP/2 grants 1 MB of byte credit. Ten compressed 100 KB messages each expand to 10 MB, creating 100 MB of objects. A 1 MB transport window did not bound heap. The application adds decoded-byte and element-cost gates before granting further reads.

### Example 4

Service A admits 50 events and each creates 20 calls to B, yielding $50\times20=1{,}000$ potential calls. B is safe at 100 concurrent calls. A schedules branches under a 100-permit bulkhead, reduces event demand, and checks event deadlines while branches wait.

### Example 5

A broker consumer prefetches 500 messages, immediately acknowledges them, then enqueues them in volatile memory for slow processing. A crash loses the queue. Moving acknowledgement after durable handoff or completed idempotent effect restores truth; prefetch now bounds genuinely outstanding responsibility.

### Example 6

Two bidirectional peers each write until its outbound window is zero, then synchronously waits for write completion before reading. Each has the other's `WINDOW_UPDATE` waiting in its receive path. Concurrent read/control loops break the cycle, and a test exhausts both windows to prove progress.

### Example 7

A sensor emits 1,000 readings/s; the consumer handles 100/s and the sensor cannot slow. Backlog grows 900/s. For a latest-state display, the adapter coalesces per sensor into one bounded slot and exposes skipped sequence ranges. It does not pretend backpressure stabilized the physical source.

### Example 8

Ten consumer instances each prefetch 1,000 messages, creating up to 10,000 delivered outstanding items. Autoscaling to 100 instances raises that to 100,000 before processing capacity warms. The platform caps aggregate/partition credit and ramps instance windows after readiness.

### Example 9

A consumer pauses a hot partition but stops polling entirely. Its lease expires, a rebalance redelivers in-flight records, and effects duplicate. The corrected loop continues heartbeats/control polling, pauses data fetch, drains bounded work, and commits only completed positions with idempotent effects.

### Example 10

A pipeline has four buffers capped at 100, 200, 50, and 150 items. The explicit buffered bound is 500, not 200. With 50 in service and 30 in transport, up to 580 items exist. Designers reduce redundant buffers and calculate worst age under the slowest credible service rate.

## Cross-Program Connections

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) provides asynchronous causality, failure, leases, ordering, delivery, feedback, and coordination models.

[Operating Systems](../../22-operating-systems/ROADMAP.md) explains kernel buffers, schedulers, threads, event loops, memory pressure, blocking, wakeups, and deadlock.

[Network Engineering](../../24-network-engineering/ROADMAP.md) covers TCP, HTTP/2 windows, congestion versus flow control, multiplexing, bandwidth-delay product, and intermediary hops.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns standard client/runtime/broker adapters, safe window defaults, autoscaling integration, priority propagation, and diagnostics.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes queues, bottlenecks, feedback delay, stability, conservation, and recovery analysis.

[Data Engineering](../../19-data-engineering/ROADMAP.md) connects broker lag, partitions, watermarks, joins, replay, retention, and consumer scaling to end-to-end pressure.

## References

1. Reactive Streams, [Reactive Streams Specification for the JVM](https://github.com/reactive-streams/reactive-streams-jvm).
2. IETF, [RFC 9113: HTTP/2](https://www.rfc-editor.org/rfc/rfc9113.html).
3. gRPC, [Flow Control](https://grpc.io/docs/guides/flow-control/).
4. gRPC, [Cancellation](https://grpc.io/docs/guides/cancellation/).
5. RabbitMQ, [Consumer Acknowledgements and Publisher Confirms](https://www.rabbitmq.com/docs/confirms).
6. Apache Kafka, [Design](https://kafka.apache.org/42/design/design/).

## Exercises

### Exercise 1

Audit an HTTP/2 streaming upload that decompresses, parses, batches, and writes to a database. Define transport and application credit units, every buffer, cancellation, and proof obligations.

### Exercise 2

A consumer processes 400 messages/s, has 50 ms feedback latency, uses 8 workers, and messages range from 1 KB to 2 MB. Propose a prefetch/credit strategy and explain why one count is insufficient.

### Exercise 3

Design backpressure for service A consuming events and calling B with fan-out between 1 and 50. Include downstream concurrency, upstream demand, deadline, ordering, retry, and overload behavior.

### Exercise 4

Design a bidirectional protocol that cannot deadlock when both sides are saturated. State separate windows, control progress, read/write concurrency, cancellation, generations, and tests.

### Exercise 5

A source cannot slow and emits security events faster than processing during an incident. Compare drop, coalesce, sampling, durable spill, and load shedding; choose a truthful bounded policy with recovery and observability.

## Answers to the Exercises

### Answer 1

Use HTTP/2 stream/connection byte windows for encoded data, then bound compressed and decoded bytes, parser objects, batch count/bytes/age, database concurrency, and response state. Grant transport credit only as the application envelope frees, while continuing to process control frames. Enumerate proxy/runtime/kernel buffers. Cancellation stops reads, discards uncommitted batches, cancels database work where safe, and preserves committed outcome. Prove peer byte limits, decoded expansion bounds, queue maxima, exactly-once permit release, no acknowledgement before durable milestone, and drain/recovery under a slow database.

### Answer 2

Pipeline fill starts near $\mu R=400\times0.05=20$ messages, while eight workers require at least eight available items. Test a count window around 24–40, but add a decoded-byte/cost cap because 40 two-megabyte messages differ from 40 one-kilobyte messages. Grant whichever count/byte/concurrency limit is exhausted first, replenish after the documented processing/durable milestone, and use per-partition/tenant fairness. Measure tail service, memory, broker latency, redelivery, and throughput; do not treat 20 as a production optimum.

### Answer 3

Give B a tested concurrency/cost bulkhead and schedule branches incrementally. Estimate or discover fan-out before granting A event demand; cap per-event and aggregate branches so $I\times F$ cannot materialize blindly. Preserve per-key order where required, check the event's original deadline before each branch, and cancel remaining optional branches when usefulness ends. Retries reacquire permits and spend budgets. When B pushes back, reduce A demand; if the broker/source cannot slow or event expiry approaches, defer durably or shed under explicit semantics. Ack the event only after its effect milestone.

### Answer 4

Maintain directional per-stream and connection data windows, with control frames/read loops always serviced from bounded reserved capacity. Reads and writes progress concurrently; neither waits for its full outbound batch before reading. Credit updates carry stream/generation identity and use saturating bounds; cancellation revokes future demand and releases queued writes. Tests exhaust both directional windows simultaneously, delay/duplicate controls, cancel mid-message, restart one peer, fill control queues, and confirm bounded memory plus eventual progress or explicit timeout rather than deadlock.

### Answer 5

Security events generally cannot be silently dropped or coalesced if each may be evidence. Sampling is appropriate only for separately labeled telemetry, not authoritative events. Use bounded ingress validation and quotas against abuse, then durably append accepted events with partitioning, retention, checksums, sequence, and explicit acceptance. When durable capacity reaches a protected threshold, reject upstream where possible and trigger a declared emergency spill/fail-closed policy; expose gaps if any source loss is unavoidable. Prioritize critical event classes fairly, cap recovery consumer credit/fan-out, preserve idempotent processing, and monitor ingest, rejected/lost ranges, oldest age, disk, lag, and estimated drain time.
