---
module_id: LSDS-063
program: Large-Scale Data Systems Engineering
level: 2
module_number: 63
title: Exchange Operators
status: complete
last_verified: 2026-09-04
---

# Exchange Operators

## One-Page Review

### Governing question

How should a distributed engine move rows or batches between producer and consumer fragments so required partitioning and ordering are correct, throughput and memory remain bounded, skew is visible, and retries never lose or duplicate committed data?

### Essential definitions

- An **exchange operator** changes execution location or data distribution between producer and consumer fragments.
- A **partition function** maps each exchange record to one or more destination partitions under a versioned key/type/null contract.
- A **hash exchange** routes equal compatible keys to the same destination; a **range exchange** routes ordered key intervals.
- A **broadcast exchange** replicates each input record to every relevant consumer; a **gather exchange** routes all records toward one logical consumer.
- A **round-robin exchange** balances records without preserving key co-location.
- A **local exchange** redistributes among threads or pipelines in one process; a **remote exchange** crosses worker or storage boundaries.
- A **pipelined exchange** lets consumers read while producers run; a **blocking exchange** exposes output only after a completion boundary.
- **credit-based flow control** permits a producer to send only within receiver-advertised byte or page capacity.
- An **exchange manifest** names complete, selected producer-attempt partitions and their integrity metadata.
- **skew** is materially unequal record, byte, work, or service distribution across exchange partitions.

### Central model, mechanism, or theorem

For record $x$ with key $k(x)$ and $q>0$ destinations, a hash exchange may assign

$$p(x)=h_v(k(x),\tau,\nu)\bmod q,$$

where $h_v$ is a versioned hash, $\tau$ is the key type/encoding contract, and $\nu$ is the null policy. A downstream local equality join or grouped aggregate is complete only if all records that must meet use compatible key expressions, types, hash version, null policy, partition count, and ownership epoch. Transport then maintains three independent obligations: each selected record is delivered exactly to its declared destinations, buffers remain bounded under backpressure, and consumers observe only compatible committed attempts. Distribution correctness does not imply balanced work, durable recovery, or global ordering.

### Critical invariants

- Query, exchange, producer partition, producer attempt, destination partition, protocol version, schema, and ownership epoch have stable identities.
- Hash/range peers agree on key expressions, types, comparison/hash semantics, null handling, partition count, and epoch.
- Hash or round-robin exchange assigns each selected record exactly once; broadcast assigns it once per declared destination.
- Local ordering is preserved only when the channel and merge contract explicitly guarantee it; arrival order is not global order.
- Sender and receiver buffering, in-flight credit, spill, and retry state have finite governed bounds.
- A slow or failed consumer eventually backpressures or cancels upstream instead of causing unbounded producer memory.
- Consumers read only one committed compatible attempt per logical producer partition.
- Checksums and manifests detect truncation, corruption, omission, and incompatible serialization before results commit.
- Cancellation, timeout, and query-generation fencing stop new writes/reads and collect data only after recovery retention permits.
- Metrics distinguish logical bytes/rows from transmitted, replicated, compressed, spilled, retried, and consumed quantities.

### Common failures

Common failures include treating “hash partitioned” as compatible without versions or counts; using round robin before a keyed aggregation; assuming local sorts yield global order; broadcasting underestimated data to every worker; creating one connection or buffer per producer-consumer pair without bounds; measuring compression savings but ignoring CPU; allowing a slow consumer to fill producer memory; mixing output from speculative attempts; deleting blocking shuffle before downstream recovery is impossible; retrying a pipelined producer without restarting consumers that saw partial data; hiding a hot key behind average partition size; rescaling partition count without an epoch boundary; and routing bulk exchange through the coordinator.

### Compact example

Six records with integer keys `0,3,1,4,2,3` are hash-routed by `key % 3`. Destination sizes are `(3,2,1)`: every record is assigned exactly once, equal key `3` meets in partition 0, and total output remains six. The assignment establishes co-location but is skewed. A real engine versions type-aware hashing, nulls, schema, attempts, and ownership rather than using an informal modulo rule.

### Connections

[LSDS-031](031-shuffle-architecture.md) introduces shuffle storage, [LSDS-054](054-data-local-task-placement.md) connects movement to locality, [LSDS-055](055-work-stealing-and-speculation.md) constrains attempts, [LSDS-061](061-distributed-logical-and-physical-plans.md) derives required distribution properties, and [LSDS-062](062-coordinator-and-worker-architecture.md) separates exchange data from coordinator control.

## Governing Question

An exchange sits where a local operator tree becomes a distributed graph. A join needs matching keys on the same consumer, an aggregation needs equal groups together, a global result needs gather or ordered merge, and downstream parallelism may differ from source partitions. Exchange provides these physical properties by moving, replicating, ordering, buffering, or materializing data.

Movement is not a transparent pipe. Producers and consumers run at different speeds, fail independently, and may be retried or speculated. Network paths reorder or truncate messages. Buffers consume memory; spill consumes disks or object storage; compression consumes CPU. A hot key can overload one destination even while total network throughput looks healthy.

The governing question is how to specify distribution semantics, channel topology, flow control, serialization, attempt visibility, recovery, and observability as one protocol. An exchange is correct only when downstream operators receive the required logical multiset and physical properties under both normal and failed execution.

## Why This Matters

Exchange is frequently the most expensive boundary in a distributed query. It serializes rows, traverses networks, creates buffers and files, changes parallelism, and couples fragment lifetimes. Join or aggregation choices that look inexpensive locally can produce terabytes of shuffle, tail latency from one partition, or memory failure from broadcast replication.

Exchange is also a correctness boundary. If partition functions disagree, matching keys never meet. If a retry's output is appended to an earlier attempt, rows duplicate. If partial output is mistaken for complete, rows vanish. If a range plan uses inconsistent comparison or boundaries, global ordering breaks. These defects can return plausible results rather than obvious failures.

The design affects recoverability. Pipelining reduces first-row latency but couples producer and consumer attempts. Blocking materialization delays consumers yet allows narrow retry and adaptive decisions from measured partition sizes. The right choice depends on query class, failure rate, storage, latency, and recovery objectives—not a universal preference.

## Prerequisites and Retrieval

Review shuffle mechanics in [LSDS-031](031-shuffle-architecture.md), partition ownership in the storage modules, placement in [LSDS-054](054-data-local-task-placement.md), speculation in [LSDS-055](055-work-stealing-and-speculation.md), resource isolation in [LSDS-057](057-memory-cpu-and-i-o-isolation.md), autoscaling in [LSDS-059](059-autoscaling-data-clusters.md), distributed plans in [LSDS-061](061-distributed-logical-and-physical-plans.md), and coordinator/worker protocols in [LSDS-062](062-coordinator-and-worker-architecture.md).

You should understand hashing, ranges, serialization, checksums, compression, flow control, backpressure, DAGs, joins, aggregation, ordering, partitions, retries, speculation, manifests, object stores, and network/disk performance.

## Learning Objectives

After this module, you should be able to:

1. select hash, range, broadcast, gather, round-robin, replicate, or local exchange by required property;
2. specify a compatible versioned partition contract across fragments;
3. design producer-consumer channels and bounded credit-based flow control;
4. choose page/batch, serialization, compression, checksum, and spill contracts;
5. compare pipelined, blocking, and hybrid exchange recovery boundaries;
6. commit one producer attempt per logical partition under retry and speculation;
7. diagnose skew by records, bytes, work, and service rather than averages;
8. adapt partition counts or split hot partitions at safe epoch boundaries;
9. secure, isolate, observe, and collect exchange data across tenants; and
10. validate distribution, ordering, backpressure, failure, and performance invariants.

## Core Exposition

### Derive exchange from required properties

Start with the consumer's physical requirement. A grouped aggregate requires equal grouping keys together. A partitioned equality join requires matching keys from both inputs together. A global limit may require gather. A global order may require range partitioning plus ordered merge. Load balancing without key semantics can use round robin.

Do not insert movement because a familiar plan shape contains it. If sources already deliver a proven compatible distribution, exchange may be redundant. Conversely, removing it because data “looks bucketed” is unsafe without exact current property evidence.

### Define the partition contract

For hash distribution, record key expressions and order, resolved types, canonical encoding, collation where relevant, hash algorithm/version, seed, null behavior, partition count, and ownership epoch. Equal logical keys must yield equal partition IDs across every producer.

For ranges, record comparison semantics, null placement, sampled or declared boundaries, inclusivity, partition count, and version. Validate boundaries are monotone, cover the domain, and do not overlap unintentionally. Schema evolution must not silently change the key representation.

### Distinguish exchange modes

Hash exchange sends one record to the key owner. Range exchange sends one record to an ordered interval. Round robin sends records across destinations without semantic co-location. Broadcast sends every record to every relevant consumer. Gather sends records toward one logical destination. Replicate-null-and-any patterns used by some joins need a precisely bounded semantic rule.

Local exchange reshapes parallel pipelines inside one worker and can still consume memory or impose ordering. Remote exchange crosses a failure and protocol boundary. A plan may combine remote hash exchange with local redistribution to match threads.

### Design channel topology

With $m$ producers and $q$ consumers, a naive all-to-all exchange exposes $m q$ logical flows. Do not require a dedicated connection, thread, or large buffer for each. Multiplex flows over bounded transports while retaining per-query/partition fairness and cancellation.

Choose push, pull, or hybrid transfer. Pull lets consumers express demand and naturally limit reads; push can reduce latency but needs receiver credits. Dedicated exchange services decouple worker lifetimes but add storage, metadata, and another operational plane.

### Batch rows into pages

Per-row messages waste headers, syscalls, encryption records, and scheduler work. Batch rows into pages or columnar record batches bounded by bytes and latency. Large pages improve throughput but increase head-of-line blocking, retry granularity, memory spikes, and first-row latency.

Represent variable-length values with governed offsets and buffer sizes. Keep logical row counts and uncompressed bytes alongside encoded bytes. A page accepted into a sender queue is not necessarily durable or visible to a consumer.

### Specify serialization semantics

The wire schema names fields by stable identity/order, physical types, null bitmaps, nested layout, dictionary semantics, endianness, alignment, and protocol version. Avoid relying on process-local object layouts. Validate sizes before allocation and reject incompatible or malicious frames.

Schema changes require negotiation or a query-scoped fixed version. Preserve decimal precision, timestamp/time-zone meaning, collation-sensitive keys, floating edge cases, and binary strings. Encoding equality must remain compatible with partition equality.

### Compress with full cost accounting

Compression reduces network and storage bytes when data is compressible, but adds CPU, buffers, latency, and sometimes worse tail behavior. Choose algorithms and levels by data shape, query class, available CPU, and bottleneck. Small pages may grow after framing.

Record raw, encoded, compressed, transmitted, and decompressed sizes plus CPU time. Negotiate codec/version and checksum scope. Never treat a successful decompression as proof that the full logical partition arrived.

### Bound memory with credits

Receiver grants credit in bytes or pages; sender transmits only within the available window. Credit is returned after the receiver frees the governed buffer, not merely after reading a header. Account for compressed versus decompressed sizes consistently to avoid memory amplification.

Bound sender queues, receiver queues, in-flight transport, reassembly, decompression, operator input, and spill metadata. Reserve control capacity for cancel, heartbeat, error, and credit messages so data saturation cannot deadlock recovery.

### Propagate backpressure

When a consumer blocks, its credits close. Producers eventually stop emitting to that destination, then their operator pipelines block, then split/source assignment slows. This chain prevents unbounded state but can spread one slow destination to upstream work.

Use fair multiplexing so one blocked partition does not monopolize connection buffers for healthy partitions. Observe blocked reason and duration at each edge. Distinguish useful backpressure from deadlock or lost credit.

### Avoid cyclic credit deadlock

In a DAG, bounded channels usually follow acyclic data dependencies. Iterative or bidirectional protocols can create cycles where every task holds buffers while waiting for credit downstream. Establish ordering, reserve escape credit, spill, or break the cycle with materialization.

Memory models must include concurrent operators and channels, not one buffer in isolation. Test minimum credit windows and extreme page sizes. Timeouts alone can convert deadlock into repeated failure without fixing the resource cycle.

### Compare pipelined and blocking exchange

Pipelined exchange exposes pages before producer completion. It reduces latency and overlaps stages, but consumer recovery depends on which producer attempt supplied already-consumed pages. Losing an upstream attempt may require restarting a connected downstream region.

Blocking exchange materializes complete producer partitions, validates them, commits a manifest, then permits consumption. It adds write/read/storage latency but supports narrow retry, measured adaptive planning, and decoupled worker lifetimes. Hybrid exchange spills under pressure or transitions at checkpoints.

### Design spill and durable storage

Spill when governed memory thresholds or execution mode require it, not only after allocation failure. Use query/tenant quotas, file/object identities, encryption, checksums, atomic manifests, lifecycle, and cleanup. Avoid millions of tiny objects through aggregation or partition-aware layout.

Local disks are tied to worker incarnation and failure domain. Remote durable stores outlive workers but add network, request, consistency, and cost constraints. “Written” is not “durably committed” until the declared storage and manifest conditions hold.

### Commit producer attempts

Identify output by query generation, exchange, logical producer partition, attempt, destination partition, and chunk. An attempt publishes a complete integrity-checked manifest. A fenced commit authority selects at most one compatible successful attempt for each logical producer partition.

Consumers resolve selected manifests and never concatenate speculative or retried attempts. Exact duplicate chunk requests are idempotent. Losing and partial outputs remain invisible and are collected only after recovery can no longer reference them.

### Preserve completeness and multiplicity

For single-destination modes, every selected input record appears in exactly one output destination. For broadcast, each appears once per declared destination. Sequence numbers or chunk ranges plus manifests help detect omission or duplication, but row-level exactly-once need not be tracked when attempt-level atomicity proves it.

Counts alone do not prove content correctness: two missing rows and two duplicates cancel. Use checksums/hashes at chunk and manifest boundaries, partition-property tests, and differential result tests.

### Handle ordering explicitly

Transport may preserve order within one producer channel while interleaving multiple producers arbitrarily. State whether ordering is absent, per producer, per partition, or global. A merge exchange needs each input sorted under compatible comparison and a correct multiway merge.

Range partitioning plus local sort yields global order only if ranges are nonoverlapping, ordered, and consumed in range order. Retry must not splice prefixes from one attempt with suffixes from another.

### Choose partition count

Too few destinations limit parallelism and create large buffers/files; too many increase channels, scheduling, metadata, small objects, connections, and downstream overhead. Choose from input bytes/rows, expected work, workers, operator memory, skew, storage limits, and query class.

Partition count is part of the property contract, not a cosmetic knob. Changing it requires a new exchange epoch or downstream plan boundary. Hash modulo changes ownership broadly when $q$ changes.

### Diagnose and mitigate skew

Measure rows, logical bytes, encoded bytes, CPU, spill, backpressure, and completion time per partition. A key with few large or expensive records can be skewed by work but not row count. Publish maximum, quantiles, and heavy hitters rather than only averages.

Mitigate with heavy-key splitting/salting, separate hot-key paths, adaptive partition split/coalesce, better keys, range boundaries, or broadcast where safe. Joins and aggregates require a recombination proof so replication or salting does not multiply results.

### Handle broadcast safely

Broadcast cost is approximately source bytes times consumer destinations plus per-worker decoded/build state. Guard on measured serialized and in-memory size, worker count, concurrent broadcasts, and receiver memory. Flow-control each destination independently.

Materialize/measure before broadcast when estimates are uncertain, and provide a repartition fallback at a safe boundary. One failed or slow consumer must not retain unlimited broadcast pages for every other consumer.

### Handle gather bottlenecks

Gather is necessary for some final results or singleton operators, but destination network, memory, CPU, and client speed cap throughput. Push partial aggregation, projection, filtering, and bounded partial limits before gather when semantics allow.

For ordered results, use distributed top-k or ordered merge rather than gathering unsorted full inputs blindly. Spool large client results and propagate client backpressure without consuming coordinator memory unboundedly.

### Adapt exchange at safe epochs

Blocking manifests reveal actual partition sizes and can support coalescing small partitions, splitting skewed ones, or switching join distribution. Adapt only before downstream consumers commit to the old mapping, or restart every affected consumer under a new epoch.

Record original and replacement mappings, evidence, sunk cost, and compatibility. Bound adaptation count to avoid oscillation. Old data remains until the new epoch commits or rollback no longer needs it.

### Isolate tenants and protect security

Authenticate producers and consumers and authorize query/exchange/partition access. Use scoped expiring credentials, encryption in transit and at rest, integrity checks, and tenant-specific quotas for memory, disk, objects, network, and requests.

Partition keys, statistics, and spill paths may expose sensitive values or cardinalities. Redact telemetry and names by role. Prevent one tenant's broadcast or blocked consumer from exhausting shared exchange capacity.

### Clean up without racing recovery

Cleanup begins after query terminal state, cancellation, expiry, or superseded attempt, but honors retry and audit retention. Use ownership manifests and idempotent deletion. Garbage collection must distinguish live queries whose coordinator is temporarily unavailable from abandoned data.

Record bytes/objects deleted, failures, age, tenant, and reason. Apply lifecycle policies as a safety net, not the only correctness mechanism. Avoid deleting a committed producer partition still needed for downstream retry.

### Observe exchange causally

Correlate query, plan/fragment, exchange, producer logical partition/attempt/worker incarnation, destination, chunk, consumer attempt, epoch, and manifest. Measure logical rows/bytes, encoded/compressed/transmitted/spilled/retried/consumed bytes, pages, credits, buffers, blocked time, throughput, checksums, and errors.

Show per-partition distributions and critical path. Distinguish producer blocked on consumer from network, disk, object store, CPU, or coordinator manifest latency. Keep high-cardinality forensic evidence governed while aggregating fleet metrics safely.

### Validate the exchange protocol

Property tests verify deterministic compatible routing, exact assignment multiplicity, range coverage, ordering, and schema round trips across versions. Differential queries compare exchange modes. Generate nulls, duplicates, empty/huge values, skew, compression edge cases, and partition-count boundaries.

Inject duplicate, lost, delayed, reordered, truncated, and corrupted chunks; producer/consumer/coordinator failure; speculation; stale epoch; credit loss; full disks; object-store errors; slow consumers; cancellation; and cleanup races. Load-test all-to-all cardinality, memory bounds, throughput, tail, fairness, and recovery.

## Definitions and Notation

Let producers be $U=\{u_1,\ldots,u_m\}$, destinations $V=\{v_0,\ldots,v_{q-1}\}$ with $q>0$, and records $X$. A distribution relation $D(x)\subseteq V$ gives destinations for record $x$. Hash exchange requires $|D(x)|=1$; broadcast requires $D(x)=V$.

Hash owner is $p(x)=h_v(k(x),\tau,\nu)\bmod q$. Range owner is the unique interval containing the comparison-normalized key under boundary vector $b$. Compatibility includes key expression/type, hash or comparator version, null policy, $q$, boundaries where applicable, and ownership epoch.

For destination $j$, define rows $n_j$, logical bytes $L_j$, transmitted bytes $T_j$, work $W_j$, and completion time $t_j$. Skew ratios such as $\max_j L_j/(\sum_jL_j/q)$ require a positive mean and reveal only one dimension. Broadcast transmission can approach $qL$ before protocol/compression effects; hash transmission approaches moved input $L$ when all input crosses the boundary.

Let sender queued bytes $S$, receiver queued/decompressed bytes $R$, in-flight credited bytes $I$, and spill bytes $Z$ be separately bounded. A committed manifest $M_{e,u,a}$ belongs to exchange epoch $e$, logical producer $u$, and selected attempt $a$, and enumerates complete destination chunks plus integrity evidence.

## Mechanisms, Invariants, or Proof Structure

Use this audit sequence:

1. Derive distribution, ordering, parallelism, locality, and recovery requirements from downstream physical operators.
2. Version key/schema/hash/range/null/count/epoch contracts and prove compatible producers and consumers.
3. Choose hash, range, broadcast, gather, round-robin, local, or hybrid mode with an explicit multiplicity invariant.
4. Design multiplexed topology, batch/serialization/compression, finite queues, credit, spill, and end-to-end backpressure.
5. Choose pipelined, blocking, or hybrid visibility and declare the connected failure/retry boundary.
6. Identify chunks and attempts, validate integrity/completeness, and atomically select one producer attempt per logical partition.
7. Measure and mitigate row/byte/work/time skew, broadcast/gather concentration, and partition-count overhead.
8. Authenticate and isolate exchange access, encrypt sensitive data, bound tenants, and redact governed metadata.
9. Correlate causal metrics across producer, transport/storage, manifest, consumer, retry, cancellation, and cleanup.
10. Property/differential test semantics, fault-inject protocol states, load-test bounds, canary versions, and retain rollback.

If compatible hash functions route equal join/group keys to the same destination and each input record is assigned exactly once, local consumers collectively see every key's complete multiset. This assumes selected attempt completeness and excludes semantic complications such as broadcast multiplicity or incorrect key extraction.

Credit bounds limit admitted in-flight data only if accounting uses the memory-amplifying representation and every buffering layer participates. A compressed-byte credit with unbounded decompression does not prove receiver memory safety.

Selecting one complete manifest per logical producer prevents attempt-level duplication when consumers read only selected manifests. It does not prove the producer's computation itself was correct; end-to-end differential and integrity validation remain.

## Alternatives and Trade-Offs

- **Hash exchange:** establishes key co-location; sensitive to skew and exact compatibility.
- **Range exchange:** supports ordered partitions; sampling/boundaries and hot ranges can fail balance.
- **Round robin:** balances record counts cheaply; destroys key grouping and may miss byte/work skew.
- **Broadcast:** avoids moving a large peer; multiplies network and memory by destinations.
- **Gather:** enables singleton/global result work; concentrates bottlenecks and failure.
- **Local exchange:** reshapes in-process parallelism; still adds queues, copying, and ordering concerns.
- **Direct worker transfer:** low extra storage; couples lifetimes and recovery.
- **Exchange service:** decouples workers and enables retry; adds storage, metadata, cost, and operations.
- **Pipelined exchange:** low first-row latency; wider failure domain and harder attempt replacement.
- **Blocking exchange:** narrow retries and adaptive evidence; higher materialization latency and I/O.
- **Large pages:** efficient throughput/compression; memory spikes and slow cancellation/first row.
- **Small pages:** responsive and fine retry; more framing, calls, and metadata.
- **Compression:** saves network/storage; consumes CPU and buffers and may worsen tails.
- **More partitions:** more parallelism and skew flexibility; more channels, files, scheduling, and overhead.
- **Durable remote shuffle:** survives workers; pays service/storage requests and cleanup complexity.
- **Local spill:** fast and cheap; tied to worker/incarnation and local capacity.

## Failure Modes and Misconceptions

- **“Exchange is just network I/O.”** it enforces distribution, ordering, multiplicity, and recovery properties.
- **“Both sides are hashed.”** versions, types, nulls, counts, keys, and epochs may disagree.
- **“Round robin is safe for aggregation.”** equal keys can land on different consumers.
- **“Local order becomes global order.”** range and merge contracts are also required.
- **“Broadcast size is the build size.”** transfer and decoded state multiply across destinations.
- **“Compression ratio is free throughput.”** CPU, buffers, latency, and incompressible frames count.
- **“TCP backpressure bounds the engine.”** application queues, decompression, spill, and multiplexing also need bounds.
- **“A credit measured in compressed bytes bounds memory.”** decompression can amplify it.
- **“One buffer per channel is small.”** all-to-all channel count grows as producer times consumer.
- **“Pipelining always wins.”** it can widen retries and couple failures.
- **“A completed producer means complete exchange.”** manifests, chunks, checksums, and commit still matter.
- **“Speculation only improves latency.”** unselected attempts can duplicate visible data without fencing.
- **“Counts detect correctness.”** omissions and duplicates can cancel numerically.
- **“Average partition size measures skew.”** tails arise from maximum bytes, work, or service.
- **“Changing partition count is dynamic tuning.”** it changes ownership and needs an epoch boundary.
- **“Object-store lifecycle is cleanup.”** it cannot decide live recovery references precisely.
- **“Coordinator relay simplifies everything.”** it creates a bulk-data bottleneck and blast radius.
- **“Encryption supplies integrity and authorization automatically.”** identities, scopes, replay, manifests, and checks remain.

## Worked Examples

### Example 1

Orders and customers both claim hash distribution on `customer_id`, but one side hashes a 64-bit integer and the other a decimal string. Equal displayed values route differently. Canonical coercion before a shared versioned hash or a new exchange restores compatibility.

### Example 2

Eight producers and 256 consumers imply 2,048 logical flows. Allocating a 1 MiB buffer per flow consumes 2 GiB before operator state. Multiplexed connections with global, tenant, query, and destination credits bound memory while preserving logical partition identity.

### Example 3

A 500 MiB compressed broadcast decodes to 2 GiB on each of 100 workers. A guard based only on compressed bytes admits 200 GiB of decoded state. Broadcast policy includes decoded/build memory and concurrency or falls back to repartition.

### Example 4

One consumer stops returning credits. Its channel blocks, but fair multiplexing continues healthy destinations until producer buffers reach per-destination bounds. Upstream eventually slows only work contributing to the blocked partition where execution architecture permits.

### Example 5

A pipelined producer fails after consumers processed half its pages. Starting a new producer and appending its full output duplicates the prefix. The engine restarts affected consumers under a new exchange epoch or uses a replay protocol with explicit offsets and identity.

### Example 6

Two speculative producer attempts finish. Each manifest has valid counts and checksums. A fenced selector commits one attempt; consumers resolve that selection, and the losing attempt remains invisible until garbage collection.

### Example 7

A range exchange samples stale data and assigns a hot current prefix to one interval. All ranges are correct and globally ordered, but one task dominates latency. New boundaries or hot-range splitting improve balance without confusing correctness with uniformity.

### Example 8

A gather destination feeds a slow client. Partial aggregation and projection reduce data first, while a spooling result service absorbs bounded output. Client backpressure stops production rather than expanding coordinator memory.

### Example 9

An adaptive planner coalesces 200 small blocking partitions into 20. It creates a new downstream mapping before consumers start, retains old manifests until the replacement commits, and records both epochs. In-place count mutation would misroute retries.

### Example 10

The fixture verifies exactly-once hash assignment and exposes skew across three destinations.

<!-- bijux-verify: {"id":"hash-exchange-assignment","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"partition_sizes=(3, 2, 1)\ntotal_output=6\nevery_record_once=True\n","stderr":""}} -->
```python
records = ((0, "a"), (3, "b"), (1, "c"), (4, "d"), (2, "e"), (3, "f"))
partitions = [[], [], []]

for record in records:
    key, _ = record
    partitions[key % len(partitions)].append(record)

sizes = tuple(len(partition) for partition in partitions)
flattened = [record for partition in partitions for record in partition]
print(f"partition_sizes={sizes}")
print(f"total_output={len(flattened)}")
print(f"every_record_once={sorted(flattened) == sorted(records)}")
```

Production routing substitutes a versioned type-aware hash and validates manifests, attempts, nulls, schema, ownership epoch, and consumer compatibility.

## Cross-Program Connections

- **Algorithms:** hashing, range partitioning, sampling, sorting, merging, checksums, heavy-hitter detection, and flow control shape exchange.
- **Distributed systems:** epochs, attempts, manifests, idempotency, backpressure, partial failure, and garbage collection define correctness.
- **Database systems:** joins, aggregation, windows, order, physical properties, and adaptive plans create movement requirements.
- **Data engineering:** shuffle, partitions, skew, spill, object storage, codecs, and schema evolution dominate pipelines.
- **Platform engineering:** network, memory, disk, identity, encryption, quotas, placement, and observability host the data plane.
- **Reliability engineering:** recovery boundaries, integrity, retry amplification, cancellation, lifecycle, fault injection, and rollback constrain design.
- **Security and governance:** tenant authorization, scoped credentials, sensitive keys/statistics, retention, and audit protect exchanged data.
- **Performance engineering:** batching, compression, throughput, critical path, buffers, blocking, skew, and replication determine cost.

## References

1. Trino. [Concepts.](https://trino.io/docs/current/overview/concepts.html) Current stage, task, split, driver, operator, and exchange terminology.
2. Trino. [Fault-Tolerant Execution.](https://trino.io/docs/current/admin/fault-tolerant-execution.html) Current task retry, spooling exchange, exchange manager, partitioning, storage, and memory behavior.
3. Trino. [Exchange Properties.](https://trino.io/docs/current/admin/properties-exchange.html) Current exchange client buffering, concurrency, response, and transport configuration.
4. Apache Spark. [RDD Programming Guide: Shuffle Operations.](https://spark.apache.org/docs/latest/rdd-programming-guide.html#shuffle-operations) Current repartitioning, disk/network I/O, files, serialization, and shuffle behavior.
5. Apache Spark. [Tuning.](https://spark.apache.org/docs/latest/tuning.html) Current serialization, memory, data structures, garbage collection, and performance guidance.
6. Apache Spark. [SQL Performance Tuning.](https://spark.apache.org/docs/latest/sql-performance-tuning.html) Current shuffle partitioning, broadcast, adaptive coalescing, and skew handling.
7. Apache Flink. [Network Memory Tuning.](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/memory/network_mem_tuning/) Current network buffers, debloating, backpressure, in-flight data, and timeout trade-offs.
8. Apache Flink. [Blocking Shuffle.](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/batch/blocking_shuffle/) Current blocking shuffle types, files, memory, compression, network, and deployment considerations.
9. Apache Flink. [Scheduling.](https://nightlies.apache.org/flink/flink-docs-stable/docs/internals/job_scheduling/) Current pipelined versus blocking data exchange and eager versus staged scheduling behavior.
10. Apache Arrow. [Columnar Format.](https://arrow.apache.org/docs/format/Columnar.html) Current type, buffer, validity, nested, alignment, and zero-copy columnar memory format.
11. Dean and Ghemawat. [MapReduce: Simplified Data Processing on Large Clusters.](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/) Primary map/shuffle/reduce, partitioning, locality, backup task, and fault-tolerance paper.
12. Melnik et al. [Dremel: Interactive Analysis of Web-Scale Datasets.](https://research.google/pubs/dremel-interactive-analysis-of-web-scale-datasets-2/) Primary distributed serving-tree, columnar, aggregation, and execution account.
13. Shute et al. [F1 Query: Declarative Querying at Scale.](https://research.google/pubs/f1-query-declarative-querying-at-scale/) Primary distributed operators, repartitioning, broadcast, sort, aggregation, and execution account.

## Exercises

### Exercise 1

Specify a hash-exchange compatibility contract for joining `DECIMAL(18,2)` keys across two plan fragments. Include expressions, coercion, nulls, hashing, partition count, schema, ownership, and upgrade behavior.

### Exercise 2

Design bounded credit and buffer accounting for 32 producers and 128 consumers when pages compress by a variable factor. Include multiplexing, decompression, fairness, control reserve, spill, and deadlock tests.

### Exercise 3

Compare pipelined, blocking, and hybrid exchange for a two-hour query with expensive scans and unreliable workers. Specify recovery scope, latency, storage, commits, and cleanup.

### Exercise 4

A join exchange has destination logical bytes `(1,1,1,17)` GiB. Diagnose skew and propose a semantics-preserving mitigation including evidence and adaptive boundaries.

### Exercise 5

Design an exchange protocol validation campaign covering routing, ordering, schemas, attempts, backpressure, corruption, failure, security, performance, canary, and rollback.

## Answers to the Exercises

### Answer 1

Resolve each join expression to the same decimal precision/scale and canonical representation before hashing; reject lossy implicit coercion. State equality and null semantics, canonical bytes, hash algorithm/version/seed, partition count, destination mapping, and exchange epoch. Fix the wire schema and decimal encoding, identify query/exchange/producer/attempt/destination, and commit one complete manifest per logical producer. Both consumers validate the contract fingerprint. During upgrade, use a mutually supported version for the whole exchange or create a new epoch and restart affected consumers; never mix hash versions because values display alike.

### Answer 2

Multiplex logical flows rather than allocating 4,096 large buffers. Bound total worker, tenant, query, destination, connection, sender, receiver, reassembly, operator, and spill bytes. Advertise credit in the representation that bounds peak receiver memory, including decompressed page and decoding workspace; cap page uncompressed size before allocation. Return credit only after governed memory is freed. Schedule destinations fairly, isolate a blocked consumer, reserve small control windows for credit/cancel/error/heartbeat, and spill under quota before exhaustion. Test worst compression amplification, minimum windows, all consumers blocked, lost/duplicate credits, cancellation, full disk, and cyclic pipelines.

### Answer 3

Pipelining overlaps scans and consumers for low latency but a producer loss can invalidate already-consumed downstream state, widening restart. Blocking writes complete checksummed partitions, commits selected attempt manifests, then runs consumers; expensive scans survive worker loss at the cost of remote/local storage, write/read latency, objects, and cleanup. Hybrid may pipeline while healthy but materialize at stage/checkpoint boundaries or spill under pressure; its exact transition and recovery contract must be explicit. For two-hour expensive scans with unreliable workers, durable blocking boundaries often reduce expected recomputation, while interactive prefixes may justify selective pipelining. Model failure probability, scan cost, storage bandwidth/cost, sink effects, and deadline. Retain old attempts until recovery/rollback no longer references them.

### Answer 4

Mean is 5 GiB and maximum/mean is 3.4, but inspect rows, CPU, spill, keys, and time because bytes alone do not locate cause. Identify heavy keys/ranges and verify the hash/type/count contract is correct. If one key dominates, route it through salted subpartitions, replicate only the matching build-side hot-key subset, join locally, then union results without duplicating pairs; or select a skew-join operator with that proof. If several divisible keys dominate, split the partition by a new mapping. Adapt after a blocking manifest measures sizes and before consumers commit, under a new epoch. Compare maximum task time/memory/spill and total extra replication, and retain repartition fallback.

### Answer 5

Property-test deterministic compatible hash/range routing, exact single/broadcast multiplicity, monotone complete ranges, local/global ordering contracts, and schema/codec round trips across supported versions. Generate nulls, duplicates, empty/huge/nested values, extreme compression, partition-count boundaries, and heavy hitters. Inject duplicate/lost/reordered/truncated/corrupted chunks, stale epochs, producer/consumer/coordinator failure, speculation, credit loss, full storage, object-store errors, slow consumers, cancellation, and cleanup races. Assert one selected complete attempt, bounded memory/queues/retries, integrity, authorization, encryption, tenant fairness, recovery, and no premature deletion. Load-test all-to-all flows, throughput, CPU, spill, tail, and cost; canary a bounded pool/protocol version, freeze on correctness/security/bound breach, and roll back by exchange epoch while preserving referenced manifests.
