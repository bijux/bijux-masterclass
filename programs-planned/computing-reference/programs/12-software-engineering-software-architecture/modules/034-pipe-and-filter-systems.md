---
module_id: SARCH-034
program: Software Engineering: Software Architecture
level: 1
module_number: 34
title: Pipe-and-Filter Systems
status: complete
last_verified: 2026-09-06
---

# Pipe-and-Filter Systems

## One-Page Review

### Governing question

When does decomposing work into filters connected by pipes improve composition, concurrency, substitution, and observability, and how should architects control state, ordering, backpressure, failure, and end-to-end correctness?

### Essential definitions

- A **filter** consumes items from input ports, transforms, validates, enriches, aggregates, routes, or observes them, and emits items or terminal outcomes.
- A **pipe** carries data and coordination between filters under declared framing, ordering, capacity, delivery, and failure semantics.
- A **pipeline** is a directed composition of filters and pipes; it may be linear, branched, merged, cyclic, batch, streaming, in-process, or distributed.
- A **record** or **item** is the pipeline's unit of processing; **framing** determines where one item ends and another begins.
- **stateless** means output depends only on the current item and immutable configuration; **stateful** filters retain cross-item information such as windows, joins, or deduplication.
- **backpressure** is a mechanism by which downstream capacity constrains upstream production rather than allowing unbounded backlog.
- **watermark** or **progress marker** summarizes bounded knowledge about event-time progress; it is not a guarantee that no later item exists unless the source semantics establish that.
- **fan-out** sends work to multiple paths; **fan-in** merges paths and therefore needs explicit ordering and completion semantics.
- A **poison item** deterministically fails a stage and can block progress under naive retry.
- **end-to-end invariant** is a property of the composed pipeline, such as no unauthorized loss, not merely a local filter property.

### Central model, mechanism, or theorem

For a linear stateless pipeline with functions $f_1,\ldots,f_n$, ideal functional semantics are

$$
y=(f_n\circ f_{n-1}\circ\cdots\circ f_1)(x).
$$

Operational semantics additionally include pipe contracts $P_i$, filter state $S_i$, scheduling, capacity, and failures. If one worker at stage $i$ has mean service time $s_i$ and ideal independent steady operation, throughput cannot exceed

$$
X\le\min_i\frac{1}{s_i}=\frac{1}{\max_i s_i}.
$$

This bottleneck bound does not establish tail latency, burst capacity, stability, ordering, or correctness.

### Critical invariants

- define item identity, schema, framing, order, event/processing time, and end-of-stream;
- state each filter's input, output, state, side effects, determinism, and error behavior;
- state each pipe's capacity, buffering, delivery, acknowledgment, backpressure, and closure semantics;
- preserve end-to-end invariants across drop, duplicate, retry, reorder, split, merge, and restart;
- bound buffers and choose overload behavior; memory is not an infinite pipe;
- make state ownership, checkpoint, version, partition, and recovery explicit;
- distinguish item completion, stage acknowledgment, durable acceptance, and externally committed effect;
- make fan-out, fan-in, parallelism, and ordering keys visible;
- isolate poison items and prevent unbounded retry or head-of-line blocking;
- propagate cancellation and close resources exactly once;
- trace schema and configuration versions through the pipeline;
- measure stage service, queueing, utilization, backlog age, loss, duplicates, and end-to-end outcome.

### Common failures

Common failures include drawing arrows with no pipe semantics; assuming filters are stateless; using lines or JSON without framing; treating in-memory queues as durable; adding workers while requiring global order; retrying non-idempotent effects; buffering without bounds; dropping on overload silently; equating stage success with end-to-end success; hiding side effects in “transform” filters; allowing poison items to block a partition; losing cancellation; incompatible schema rollout; and optimizing average stage time while tail queue age grows.

### Compact example

A three-stage image pipeline decodes in 4 ms, classifies in 20 ms, and stores in 6 ms per item with one worker each. Under ideal assumptions, classification bounds throughput at $1/0.020=50$ items/s. At 60 arrivals/s, backlog grows despite average end-to-end work of 30 ms. Add classified parallelism if order permits, reduce demand, or shed with an explicit policy; a larger queue only delays overload.

### Connections

[SARCH-031](031-layered-architecture.md) orders static dependencies, while pipes and filters foreground data transformation and runtime flow. [SARCH-035](../ROADMAP.md) next broadens event-driven architecture. Compiler Engineering, Data Engineering, Operating Systems, Distributed Systems, and Concurrent Programming own deeper parsing, pipeline, IPC, delivery, and concurrency mechanisms.

## Governing Question

Many systems transform a flow through stages: a compiler lexes, parses, analyzes, optimizes, and emits; a Unix command chain reads and writes streams; a data pipeline validates, normalizes, enriches, aggregates, and publishes; a media pipeline decodes, filters, and encodes.

The style is attractive because each filter can have a narrow contract and stages can be composed or parallelized. But the neat chain hides operational questions. What is an item? Can it be replayed? Where is state? What happens when stage three is slow, stage two crashes, or two branches disagree? The governing question is how to preserve a meaningful end-to-end contract under those mechanisms.

## Why This Matters

Pipe-and-filter decomposition can support reuse, incremental processing, concurrency, independent stage reasoning, substitution, observability, and scale. It is especially useful when work naturally forms transformations over a sequence and intermediate representations have stable meaning.

It can also amplify latency, copying, serialization, coordination, and failure. A business transaction forced through generic filters can hide authority and make errors hard to explain. Stateful joins and external side effects weaken simple functional intuition. Distributed pipes introduce delivery, compatibility, and operational obligations.

Architectural value therefore depends on semantics, not box count. The system must specify both local filter contracts and global properties, then verify them with structural, mathematical, executable, and operational evidence appropriate to each claim.

## Prerequisites and Retrieval

Retrieve function composition, stream, record, message, framing, schema, filter, pipe, buffer, queue, throughput, service time, utilization, latency, backpressure, overload, ordering, partition, state, checkpoint, retry, idempotency, acknowledgment, duplicate, loss, poison item, cancellation, end-of-stream, side effect, and invariant.

From SARCH-023 and SARCH-024 retrieve runtime components, connectors, send/receive events, queues, concurrency, and scenario traces. From SARCH-025 retrieve deployment mapping and failure domains. From SARCH-026 retrieve information semantics, lineage, authority, and quality. Distinguish a source-code pipeline from a runtime data flow and a local function from a distributed stage.

## Learning Objectives

After completing this module, you should be able to:

1. identify when pipe-and-filter decomposition matches a problem's transformation structure;
2. specify filter and pipe contracts beyond input and output types;
3. distinguish functional composition from operational scheduling and failure;
4. derive bottleneck throughput and bounded-backlog conditions under stated assumptions;
5. reason about framing, ordering, parallelism, fan-out, fan-in, and completion;
6. design backpressure, overload, retry, poison-item, and cancellation behavior;
7. model stateful filters, partitioning, checkpointing, replay, and schema evolution;
8. place side effects and acknowledgments without claiming false exactly-once behavior;
9. test local stages and end-to-end invariants with fault and boundary cases;
10. evaluate a pipeline's production fit across performance, security, operations, and change.

## Core Exposition

**Start with the transformation.** The pipe-and-filter style fits when a problem can be expressed as a sequence or graph of transformations over identifiable items or streams. Each filter should have a cohesive responsibility and a contract meaningful outside its implementation.

Do not begin by turning every method into a stage. Identify intermediate representations, ownership, state, and reasons for change. If two steps share an invariant and must update atomically, separating them with a generic queue may harm the design. If one stage can be replaced or parallelized independently, the seam may be valuable.

**Define filter semantics.** A filter contract includes accepted item schema, preconditions, output schema, cardinality, order, state, determinism, side effects, errors, resource bounds, cancellation, and completion. A filter can emit zero, one, or many outputs per input, or combine many inputs into one.

Classify the operation: map, filter/select, validate, parse, enrich, aggregate, window, join, route, split, merge, encode, persist, or observe. The word “filter” in the architectural style includes more than boolean selection, so state the actual relation.

**Define pipe semantics.** A pipe can be an in-memory call, iterator, byte stream, bounded queue, file, operating-system pipe, broker topic, or database-backed work queue. These mechanisms differ in framing, copying, persistence, capacity, delivery, ordering, fan-out, acknowledgment, and failure.

An arrow labeled `records` is insufficient. State producer and consumer, schema and version, identity, maximum item size, order scope, capacity, blocking or nonblocking behavior, closure, replay, and ownership. If a pipe crosses trust or deployment boundaries, add authentication, authorization, confidentiality, integrity, and operational ownership.

**Learn from the historical forms without conflating them.** Unix pipelines made simple programs composable through byte streams and a common process interface [1]. Pipes and Filters was later described as an architectural pattern with incremental transformation and independent stages [2]. Kahn process networks provided a formal model of deterministic processes communicating through unbounded FIFO channels [3].

Production queues are bounded, scheduling is finite, and filters may be nondeterministic or side-effecting. Do not import mathematical properties from one model merely because the diagram looks similar. Name the applicable operational model.

**Separate functional and operational semantics.** For pure stateless functions, composition tells what output corresponds to input. It does not say when output appears, how much memory is used, which stages overlap, or what happens on failure.

Operational semantics add workers, queues, threads, processes, hosts, checkpoints, and retries. Two pipelines can implement the same transformation and differ radically in latency, failure, order, and resource behavior. Preserve both views and their correspondence.

**Define item identity and framing.** A byte stream has no inherent records. Newline-delimited data fails when unescaped newlines occur or the final record lacks a terminator unless the format defines behavior. Length prefixes fail if lengths are corrupt or unbounded. Self-describing formats still need stream boundaries.

Give replayable items stable identity. Distinguish source identity, processing attempt, output identity, and externally committed effect. Define maximum sizes and malformed input behavior before allocation. End-of-stream, empty input, partial final frames, and abrupt closure are protocol events, not implementation trivia.

**Reason about cardinality.** A one-to-one map preserves item count only if failures, drops, and duplicates are absent. A selector emits zero or one. A splitter emits several. An aggregator consumes many. A join may emit zero, one, or a multiplicative number depending on keys and windows.

Track cardinality explicitly to capacity-plan downstream stages and detect loss or explosion. Input and output counts alone can mislead when legitimate filtering or late corrections occur; reconcile by reason and identity.

**Derive throughput from stage capacity.** For one worker with mean service time $s_i$, ideal service capacity is $\mu_i=1/s_i$. In a stable linear pipeline with arrival rate $\lambda$, each required stage needs $\lambda<\mu_i$ under the stated average model.

The slowest stage limits steady throughput. Adding buffers does not change service capacity. Adding $k_i$ independent workers can raise ideal capacity toward $k_i/s_i$, but shared CPU, memory, I/O, locks, ordering, partition skew, and coordination reduce it. Measure distributions, not only means.

**Distinguish first-item latency and steady throughput.** Without queueing, first-item latency is approximately the sum of stage service and transfer times. Once stages overlap, steady throughput can approach the bottleneck rate while each item's latency still includes all stages and queue waits.

Batching improves throughput by amortizing setup but delays the first item and increases retry scope. Micro-batches introduce size/time triggers whose partial and shutdown behavior must be defined. Report p50, p95, p99, and maximum or bounded objectives where relevant.

**Bound every queue.** An unbounded queue converts overload into memory exhaustion and long recovery. A bounded queue forces a policy: block, signal demand, reject, shed, spill, sample, compress, or degrade.

Choose by semantics. Blocking can deadlock when producer and consumer share constrained resources. Dropping may be valid for redundant telemetry but not for financial instructions. Spilling changes durability, privacy, and disk-failure behavior. Record who sees rejection and how recovery works.

**Use backpressure end to end.** Backpressure is effective only if downstream scarcity reaches the true producer or admission point. A bounded stage that blocks while an upstream broker accumulates unlimited work has moved rather than solved backlog.

Demand signaling, credits, bounded queues, rate limits, and pull-based iteration are mechanisms. Ensure control messages themselves have capacity under overload. Monitor queue age and estimated recovery time, not only queue length.

For arrival rate $\lambda$ and sustainable service rate $\mu$, backlog grows roughly at $\lambda-\mu$ items per unit time while $\lambda>\mu$. A larger buffer delays rejection but increases memory and time-to-recover; it does not restore stability.

**Design parallelism with ordering scope.** Stateless filters can often process items concurrently. Global ordering restricts concurrency or requires resequencing. Per-key ordering allows different keys in parallel but suffers from hot-key skew.

State the order property: source order, event time, processing time, per-key sequence, causal order, or no order. A merge must define how it handles slow paths, missing items, duplicates, and end-of-stream. A sorting stage can restore one order at memory and latency cost only with a completeness boundary.

**Handle fan-out and fan-in.** Fan-out may broadcast every item, partition items, or route by predicate. Broadcast completion may require all branches, any branch, or a quorum; each produces different availability and semantics.

Fan-in can interleave, merge by key, zip corresponding items, union without order, or join under a window. Define branch identity and correlation. A slow optional observer should not block a critical path unless the business requirement says its acknowledgment is mandatory.

**Make state explicit.** Deduplication, aggregation, windows, joins, sequence detection, model inference, and rate limiting retain state. Define the key, ownership, partition, lifetime, eviction, schema, consistency, checkpoint, recovery, and rescaling behavior.

A “stateless service” backed by a shared cache is stateful at the architecture level. Moving state outside a process changes placement, not semantics. Checkpoint boundaries must correspond to input position and output effects or replay can lose or duplicate results.

**Distinguish time domains.** Processing time is when a stage handles an item; event time is when the represented event occurred; ingestion time is when the pipeline accepted it. Clocks can differ and items can arrive late or out of order.

Windows need membership, trigger, allowed lateness, update, and finality rules. A watermark is an estimate or contract about progress under a named source. Treating it as universal truth can drop valid late data. Data Engineering develops these mechanisms further.

**Design acknowledgment precisely.** A stage may acknowledge receipt, durable storage, completed transformation, published output, or externally committed effect. These are different milestones.

Acknowledging input before durable output risks loss. Acknowledging after output can produce duplicates when the acknowledgment is lost. Transactions can couple some local steps; idempotency, deduplication, and reconciliation handle remaining ambiguity. Avoid an unqualified “exactly once” claim.

**Make side effects visible.** Pure filters are easy to replay. A filter that charges a card, sends a message, writes a file, or changes a device is not. Place effects behind explicit contracts and stable request identities. Define retry, query, compensation, and unknown outcome.

Do not hide an effect in a stage called `enrich`. Observability emission can itself block, leak data, or fail; decide whether it is best-effort or required. External outputs need authority, audit, and reconciliation.

**Control retry and poison items.** Retry only failures likely to be transient and operations safe to repeat under a stable identity. Use bounded attempts, delay, jitter, and budgets. Preserve the original cause and processing history.

A poison item that always fails can block a partition indefinitely. Quarantine it with full provenance, alert an owner, continue according to order requirements, and provide a controlled correction/replay path. A dead-letter store is not resolution; it is deferred work with retention and security obligations.

**Propagate cancellation and closure.** When the consumer no longer needs output, upstream stages should stop work and release resources. Define whether already accepted items finish, roll back, or become resumable. Close output only after all producers have finished or a terminal error is declared.

Handle broken pipes, half-closed channels, abandoned branches, blocked writes, and process termination. Resource cleanup must close files, buffers, network streams, temporary storage, and permits exactly once.

**Version schemas and configuration.** Rolling changes can place old and new filters on either side of a pipe. Define compatible readers and writers, defaults, unknown fields, semantic changes, and rollback. Schema compatibility does not guarantee semantic compatibility.

Attach configuration and model versions when output depends on them. A correction may need to reprocess old input with new rules, producing a new output identity or superseding version rather than silently overwriting provenance.

**Design security and privacy across the graph.** Validate and normalize at trust boundaries, but keep domain validation with authoritative policy. Authenticate stages or processes where threat assumptions require it. Authorize access by data and operation, not merely pipeline membership.

Minimize sensitive fields before broad fan-out. Encrypt protected pipes and storage, manage secrets per stage, audit effects, and set retention for buffers, checkpoints, quarantines, and logs. A debug tap can become an uncontrolled data copy.

**Observe local and end-to-end behavior.** Record stage rate, service-time distribution, errors by reason, retry, saturation, queue length and age, backpressure, drops, duplicates, late items, checkpoint progress, and resource use. Correlate one item's path without placing secrets or unbounded identifiers in metric labels.

Local green status can coexist with end-to-end failure. Trace acceptance to required terminal outcomes and reconcile counts by semantic reason. Synthetic canaries and known test records can expose stuck branches, but remove or isolate them from business effects.

**Test the composition.** Unit-test pure transformations with properties, boundaries, and counterexamples. Contract-test pipe framing and adapter semantics. Test state recovery, replay, duplicates, reorder, late arrival, schema versions, poison items, cancellation, and end-of-stream.

Load-test representative distributions and skew. Fault-inject crash points around input acknowledgment, state checkpoint, output write, and external effects. Verify end-to-end invariants through reconciliation rather than relying on stage exit status.

**Know when another style fits better.** A request-response use case needing immediate coordinated policy may be clearer as a direct application operation. A shared-state algorithm with fine-grained interaction may suffer from serialization into stages. A transactional invariant should not be fragmented solely for concurrency.

Pipelines fit transformation flow. Combine them with layers, modular boundaries, event-driven components, repositories, and control planes where their distinct concerns require it. Styles are composable, not exclusive labels for a whole system.

## Definitions and Notation

Let a pipeline be directed graph $G=(F,P)$ with filters $F$ and pipes $P$. A pipe $p=(f_i,f_j,sigma,c,o,d)$ carries schema $\sigma$, capacity $c$, ordering rule $o$, and delivery/acknowledgment rule $d$ from producer to consumer.

For a linear pure pipeline, $y=(f_n\circ\cdots\circ f_1)(x)$. For operational filter $i$, let $s_i$ be mean service time and $k_i$ workers. Ideal capacity is $\mu_i=k_i/s_i$ under independent parallelism assumptions. Stability needs arrival rate $\lambda<\mu_i$ at each mandatory stage.

Let $B_i(t)$ be backlog at pipe $i$. During a sustained interval with arrival $\lambda_i$ and departure $\mu_i$, a fluid approximation is

$$
B_i(t+\Delta)\approx\max(0,B_i(t)+(\lambda_i-\mu_i)\Delta),
$$

subject to bounded capacity and overload policy. This approximation does not describe burst distributions, correlated service, retries, or discrete scheduling.

For input identities $I$ and required terminal outcomes $O$, end-to-end completeness requires every accepted $i\in I$ to map to an authorized terminal state such as committed, rejected with cause, quarantined, or explicitly pending. Counts without identity and reason cannot establish this invariant.

## Mechanisms, Invariants, or Proof Structure

**Composition invariant.** Every adjacent output is semantically compatible with the next input, including schema, units, identity, order, cardinality, time, and error. Type compatibility alone is insufficient.

**Bottleneck bound.** In a mandatory linear pipeline, every completed item requires service at every stage. Therefore throughput cannot exceed any stage capacity and is bounded above by their minimum. The bound assumes a defined item and excludes loss or bypass.

**Bounded-capacity invariant.** Each pipe has a finite capacity or an explicitly governed external backlog. When capacity is exhausted, one declared overload action occurs; silent unbounded growth is prohibited.

**Acknowledgment invariant.** An acknowledgment names the achieved durable or semantic milestone. Retry behavior is derived from that milestone and effect idempotency rather than from a generic success flag.

**State-recovery invariant.** Checkpointed state, consumed input position, and emitted effects correspond under the recovery protocol. After restart, every accepted item reaches an allowed outcome despite permitted duplicates or reprocessing.

**Ordering invariant.** Parallelism preserves the declared ordering scope or emits enough sequence information for a defined resequencing mechanism. Global order is never inferred from per-worker FIFO.

**Cancellation invariant.** Terminal cancellation or failure reaches all affected stages, stops new work, resolves accepted items according to policy, and releases resources without double close.

**Evidence invariant.** Pure-function tests prove examples under inputs; load tests observe a distribution and environment; fault tests exercise selected crash points; production telemetry observes deployed paths. End-to-end claims require corresponding evidence.

## Alternatives and Trade-Offs

**Synchronous pull versus asynchronous push.** Pull naturally propagates demand and can simplify backpressure. Push reduces source latency and supports independent stages but needs bounded buffering and demand control.

**In-process versus distributed pipes.** In-process calls and queues reduce serialization and operations but share failure and resources. Distributed pipes support isolation and independent scale while adding network, delivery, security, version, and observability cost.

**Fine-grained versus coarse filters.** Fine stages increase reuse, visibility, and parallel choices but add transfer, mapping, and coordination. Coarse stages reduce overhead but combine responsibilities and limit substitution. Split around stable representations and independent forces.

**Pure versus effecting filters.** Pure transformations are replayable and easy to test. Effects are unavoidable at system boundaries and need identity, acknowledgment, retry, audit, and reconciliation.

**Strict order versus parallel throughput.** Global order simplifies reasoning but constrains concurrency. Per-key or no-order processing increases capacity but needs partition, merge, and consumer semantics.

**Larger buffers versus early overload.** Buffers absorb bursts and decouple jitter. They consume resources, increase latency, hide saturation, and lengthen recovery. Size from explicit burst and recovery objectives.

**Fail-fast versus quarantine.** Fail-fast protects order and avoids silent partial results but can stop unrelated work. Quarantine preserves progress but requires provenance, review, correction, and downstream understanding of missing items.

## Failure Modes and Misconceptions

1. **“A pipe is just an arrow.”** Capacity, order, framing, delivery, and failure define the connector.
2. **“Filters are stateless.”** Joins, windows, deduplication, caches, and rate limits retain state.
3. **“Function composition describes production behavior.”** Scheduling, buffering, failure, and effects are additional semantics.
4. **“More stages mean more reuse.”** Weak intermediate representations create mapping and coordination without stable value.
5. **“A bigger queue fixes overload.”** It delays rejection while backlog and recovery time grow.
6. **“FIFO preserves order with many workers.”** Parallel completion can reorder unless scope and resequencing are defined.
7. **“Acknowledged means complete.”** It may mean only received or durably queued.
8. **“Retry fixes failure.”** Non-idempotent effects and poison items can duplicate harm or block progress.
9. **“Exactly once is a property of one queue.”** End-to-end effects span state, acknowledgment, replay, and external systems.
10. **“An in-memory event pipe is durable.”** Process crash loses unpersisted state and items.
11. **“Schema-compatible means semantically compatible.”** Units, defaults, and interpretation can change.
12. **“Stage dashboards prove end-to-end success.”** Local completion may not reach the required terminal effect.
13. **“Observability taps are harmless.”** They can block, leak, copy, or retain sensitive data.
14. **“Cancellation is a UI concern.”** Every stage and resource participates in termination.
15. **“Every workflow should be a pipeline.”** Tight invariants and interactive policy may need another structure.

## Worked Examples

### Example 1

**Situation.** A batch pipeline trims text, parses integers, rejects negatives, and sums the result.

**Reasoning.** Define line framing, whitespace, numeric range, malformed-line outcome, whether rejection stops the batch, and overflow behavior. The pure composition is simple only after those semantics are explicit. Test empty input, final line without newline, invalid UTF-8, minimum/maximum values, and overflow.

**Conclusion.** Even a small pure pipeline needs framing and error semantics before composition is meaningful.

### Example 2

**Situation.** Decode, classify, and store take 4, 20, and 6 ms per image with one worker each.

**Reasoning.** Ideal capacities are 250, 50, and about 166.7 items/s. Classification limits steady throughput to 50 items/s. First-item service time without queueing is about 30 ms, but this is not the sustainable inter-completion time after overlap. At 60 arrivals/s, backlog grows about 10 items/s under the fluid mean model.

**Conclusion.** Sum of stage times estimates ideal first-item work; the slowest required stage bounds throughput.

### Example 3

**Situation.** A queue holds 1,000 items. Arrival is 120/s and service is 100/s for 30 seconds.

**Reasoning.** Starting empty, the fluid approximation adds $(120-100)30=600$ items, within capacity. If overload continues another 20 seconds, it reaches 1,000. The design must then block, reject, shed, or spill. Recovery after arrival returns to 80/s occurs at 20 items/s and takes 50 seconds from full.

**Conclusion.** Buffer size follows a burst and recovery policy; it does not increase service capacity.

### Example 4

**Situation.** A broker holds millions of records while every in-process stage reports a short local queue.

**Reasoning.** Backpressure stops only local fetching, so backlog moved to the broker. Monitor source age and recovery, limit admission at the true producer where possible, and define retention and rejection. Ensure control and checkpoint traffic has reserved capacity.

**Conclusion.** Backpressure must be evaluated across the entire admission path.

### Example 5

**Situation.** Four workers process one ordered stream and emit results as soon as each finishes.

**Reasoning.** FIFO input assignment does not preserve completion order. If consumers require global order, add sequence numbers and a bounded resequencer, or reduce parallelism. If per-account order suffices, partition consistently by account and handle hot keys and repartitioning.

**Conclusion.** Parallelism is constrained by the declared ordering scope, not by queue branding.

### Example 6

**Situation.** A stage charges a card, crashes before acknowledging input, and retries.

**Reasoning.** The charge may have committed, so blind retry can duplicate it. Use a stable operation identity, provider idempotency or outcome query, durable local intent, and reconciliation for unknown results. A queue's redelivery guarantee cannot make the external effect exactly once by itself.

**Conclusion.** End-to-end effect safety requires identity and outcome semantics beyond stage acknowledgment.

### Example 7

**Situation.** One malformed item retries indefinitely at the head of an ordered partition.

**Reasoning.** Classify deterministic versus transient failure. After bounded attempts, quarantine the item with schema, source, cause, processing history, and security controls. Decide whether later items may pass or the partition must stop. Alert an owner and provide corrected replay.

**Conclusion.** A dead-letter destination prevents blocking only when ownership and ordering policy complete the design.

### Example 8

**Situation.** A producer changes distance from meters to centimeters without changing the numeric field type.

**Reasoning.** The schema is structurally compatible but semantically incompatible. Add an explicit unit or new field/version, deploy tolerant consumers, dual-write or translate during migration, and preserve source version in lineage. Test rollback and mixed-version pipes.

**Conclusion.** Pipeline compatibility includes meaning, not only parseability.

### Example 9

**Situation.** A user cancels a large export, but upstream database reads and temporary files continue for ten minutes.

**Reasoning.** Propagate cancellation through every pipe, stop new batches, cancel or drain active reads according to transaction semantics, close output once, and delete or retain temporary data by policy. Record whether accepted work is resumable and ensure cleanup works after abrupt disconnect.

**Conclusion.** Cancellation is an end-to-end resource and outcome protocol.

### Example 10

**Situation.** A clinical signal pipeline samples a sensor, filters noise, detects events, raises alarms, stores evidence, and displays trends.

**Reasoning.** Define sample identity, calibration, timestamps, missing data, filter delay, detection thresholds, alarm authority, operator acknowledgment, and storage provenance. Bound queues and worst-case latency; keep safety alarm capacity independent of trend export. Test boundary signals, sensor disconnect, clock error, overload, duplicate samples, restart, configuration version, and human interpretation.

**Conclusion.** High-consequence pipelines require timing, provenance, physical, and human evidence in addition to functional transforms.

## Cross-Program Connections

- **Compiler Engineering:** token, syntax, semantic, optimization, and code-generation stages illustrate stable intermediate representations and whole-program constraints.
- **Data Engineering:** batch/stream execution, event time, windows, joins, checkpoints, lineage, and schema evolution deepen pipeline mechanisms.
- **Operating Systems:** byte streams, process pipes, descriptors, blocking, signals, and IPC define local connector behavior.
- **Concurrent Programming:** bounded queues, scheduling, work distribution, cancellation, and memory visibility govern in-process stages.
- **Distributed Systems:** delivery, ordering, clocks, retries, state replication, checkpointing, and partial failure govern distributed stages.
- **Database Engineering:** transactions, logs, storage, isolation, and query execution constrain stateful and effecting filters.
- **Security Engineering:** trust boundaries, validation, credentials, data minimization, quarantine, and audit apply across the graph.
- **Testing and Quality Engineering:** property, contract, load, fault, recovery, compatibility, and reconciliation tests provide distinct evidence.

## References

1. Dennis M. Ritchie and Ken Thompson, “The UNIX Time-Sharing System,” *Communications of the ACM*, vol. 17, no. 7, pp. 365–375, 1974. https://doi.org/10.1145/361011.361061
2. Frank Buschmann et al., *Pattern-Oriented Software Architecture, Volume 1: A System of Patterns*, Wiley, 1996.
3. Gilles Kahn, “The Semantics of a Simple Language for Parallel Programming,” in *Information Processing 74*, North-Holland, 1974.
4. Mary Shaw and David Garlan, *Software Architecture: Perspectives on an Emerging Discipline*, Prentice Hall, 1996.
5. Gregor Hohpe and Bobby Woolf, *Enterprise Integration Patterns*, Addison-Wesley, 2003.
6. Edward A. Lee and Sanjit A. Seshia, *Introduction to Embedded Systems: A Cyber-Physical Systems Approach*, 2nd ed., MIT Press, 2017. https://ptolemy.berkeley.edu/books/leeseshia/
7. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021.
8. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly Media, 2017.

## Exercises

### Exercise 1

Precisely distinguish filter, pipe, item, framing, stateless, stateful, backpressure, acknowledgment, poison item, end-of-stream, and end-to-end invariant.

### Exercise 2

A four-stage pipeline has one worker per stage with mean service times 5, 8, 20, and 10 ms. Compute ideal stage capacities and the bottleneck. At 60 arrivals/s for 40 seconds from an empty queue, approximate backlog growth. State assumptions and limitations.

### Exercise 3

Diagnose a pipeline that uses unbounded in-memory queues, global-order output from eight workers, synchronous audit fan-out, unlimited retry, and acknowledgment before output persistence. Produce a coherent repair.

### Exercise 4

Compare an in-process pull pipeline, an in-process bounded push pipeline, and a distributed broker pipeline for document conversion. Address framing, backpressure, scale, order, effects, failure, security, deployment, and testing.

### Exercise 5

Transfer the style to a wildfire sensor system that ingests heat, smoke, wind, camera, and location observations over intermittent links, correlates evidence, raises alerts, stores provenance, and supports field and regional operators. Define semantics and assurance.

## Answers to the Exercises

### Answer 1

A **filter** performs a bounded transformation or observation. A **pipe** carries items and coordination under capacity, order, delivery, and failure rules. An **item** is the unit of processing; **framing** identifies its boundaries. A **stateless** filter depends only on the current item and immutable configuration; a **stateful** filter retains cross-item information.

**Backpressure** propagates downstream scarcity upstream. An **acknowledgment** names a reached milestone such as receipt, durable storage, or completed effect. A **poison item** repeatedly fails deterministically. **End-of-stream** declares no further input under a named source protocol. An **end-to-end invariant** constrains the whole path, such as every accepted identity reaching an authorized terminal outcome.

### Answer 2

Capacities are $1/0.005=200$, $1/0.008=125$, $1/0.020=50$, and $1/0.010=100$ items/s. Stage three is the ideal bottleneck, so pipeline throughput cannot exceed 50 items/s with one worker per stage.

At 60 arrivals/s, overload is 10 items/s. Over 40 seconds, the fluid approximation gives 400 queued items, assuming no initial backlog, every item visits every stage once, stable mean rates, no retry or loss, independent resources, sufficient pipe capacity, and downstream acceptance. It does not predict burst peaks, tail latency, service variance, shared-resource contention, discrete scheduling, or ordering cost. If capacity is below 400, the configured overload policy occurs earlier.

### Answer 3

Bound every queue and connect capacity to admission through demand or credit. Define block, reject, shed, or spill by item semantics and reserve control capacity. If global order is truly required, attach sequence identities and use a bounded resequencer or reduce parallelism; otherwise weaken order to a justified per-key scope.

Decouple optional audit from the critical completion rule, or give mandatory audit an independently provisioned durable path with explicit failure behavior. Classify errors, bound retry with delay and budget, quarantine poison items, preserve provenance, and assign resolution ownership. Acknowledge only after the declared durable output or effect milestone. Use stable identities, idempotent effects, and reconciliation for crash ambiguity.

Then load-test skew and bursts, fault-inject around input, state, output, and acknowledgment, test cancellation and closure, and reconcile accepted identities to terminal outcomes. A larger bounded queue alone is not the repair.

### Answer 4

An in-process pull pipeline offers simple composition, natural demand propagation, low transfer cost, and one failure domain. It suits sequential or lazily consumed conversion but may underuse concurrency. Define iterator cancellation, resource closure, malformed item behavior, and whether stages buffer.

An in-process bounded push pipeline supports overlapping stages and controlled parallelism. It needs queue capacities, worker and order rules, cancellation, shutdown, backpressure, and shared-resource analysis. Process crash loses nonpersistent accepted work unless input can replay.

A broker pipeline supports independent deployment, durable buffering, separate scale, and replay. It adds serialization, schema rollout, authentication, authorization, delivery ambiguity, duplicate handling, ordering scopes, poison-item operations, telemetry, and more failure modes. External file publication needs stable job and output identity under all three designs.

For sensitive documents, minimize intermediate copies, encrypt protected storage and transport, isolate credentials, control temporary files and quarantines, and audit access. Test pure conversion, framing, real libraries, malformed/adversarial files, cancellation, load, resource exhaustion, crash/replay, mixed versions, duplicate effects, and end-to-end output reconciliation. Choose the least distributed design satisfying scale, isolation, release, and recovery forces.

### Answer 5

Define observation identity, sensor and calibration identity, location reference, source time, ingestion time, units, precision, confidence, sequence, schema, and configuration. Pipes specify intermittent buffering, authentication, capacity, compression, order, duplicate, loss, replay, and closure. Validate representation at ingress while preserving raw signed provenance where policy permits.

Filters normalize units, assess quality, align time and location, derive features, correlate observations, classify risk, route alerts, store evidence, and create operator projections. Stateful correlation declares windows, lateness, partitions, checkpoints, model version, and correction. Alert effects use stable identity, authority, acknowledgment, escalation, and reconciliation. A single sensor cannot silently establish a regional fact.

Backpressure reaches field admission where possible; safety alerts have reserved capacity independent of bulk imagery and analytics. Poison data is quarantined without exposing sensitive locations or blocking unrelated sensors. Offline nodes retain bounded work and communicate data age. Cancellation and incident closure preserve audit and release resources.

Test boundary and adversarial signals, clock drift, false and missing observations, duplicates, reordering, partitions, backlog, hot regions, restart, checkpoint loss, model rollout, unauthorized sources, compromised data, alert delivery, degraded field operation, and operator comprehension. Measure stage and end-to-end timing and reconcile every accepted high-severity observation to an explained terminal outcome. Simulation and drills remain bounded evidence, not proof of all wildfire conditions.
