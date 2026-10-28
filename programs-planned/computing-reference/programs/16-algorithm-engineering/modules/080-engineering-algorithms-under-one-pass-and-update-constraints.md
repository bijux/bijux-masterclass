---
module_id: ALGE-080
program: Algorithm Engineering
level: 2
module_number: 80
title: Engineering Algorithms Under One-Pass and Update Constraints
status: complete
last_verified: 2026-09-05
---

# Engineering Algorithms Under One-Pass and Update Constraints

## One-Page Review

### Governing question

How do we turn a streaming or dynamic algorithm into a trustworthy component when input can be read once, memory is bounded, updates may retract earlier facts, delivery can duplicate or reorder records, and recovery must reproduce a named result?

### Essential definitions

- A **logical stream** is an ordered sequence of updates; its delivery may contain retries, gaps, and reordering that must not silently change that sequence.
- A **one-pass algorithm** consumes each logical update at most once in sequence and retains bounded state rather than the input. It does not automatically provide exactly-once effects.
- In a **cash-register model**, updates are nonnegative. A **strict turnstile model** allows signed deltas but requires every item frequency to remain nonnegative. A general **turnstile model** may permit negative coordinates [1].
- A **summary** is state smaller than the full input. Its error contract includes target, parameters, probability, update model, query scope, and adversary assumptions.
- A **mergeable summary** combines states for valid partitions without rereading raw input; mergeability requires a proved algebra and compatible metadata [4].
- A **watermark** is an estimate or assertion about event-time progress, not proof that no earlier event can arrive [6].
- A **checkpoint** binds algorithm state to the last included logical sequence and all semantic metadata needed for replay.

### Central model, mechanism, or theorem

Treat processing as a deterministic or seeded transition

$$
(S_{j+1},o_j)=F(S_j,u_j;C),
$$

where $S_j$ is state after logical sequence $j$, $u_j$ is the next validated update, $o_j$ is optional output, and $C$ fixes schema, update model, budgets, numeric policy, hash family, seeds, and error parameters. Validate the entire precondition before mutating state, then atomically persist the new state and input position. Recovery loads a checksum-bound checkpoint $(S_k,k,C)$ and replays the contiguous suffix $u_{k+1},\ldots$.

Algorithmic bounds and operational semantics are separate obligations. Streaming lower bounds explain why exact answers may require large memory [2]; they do not decide retry identity, event-time windows, checkpoint atomicity, or overload policy. A correct component must satisfy both layers.

### Critical invariants

- Every committed logical sequence is applied exactly once to the published state.
- Rejected updates make no partial state or position change.
- State size, per-update work, numeric range, and error remain within declared budgets.
- Update-model invariants hold, such as nonnegative coordinates in strict turnstile processing.
- Merge combines compatible, disjoint logical partitions according to a proved operation.
- Checkpoint state, sequence, configuration, seed, schema, and checksum describe one recoverable version.
- Outputs name their input version, event-time completeness policy, and approximation contract.

### Common failures

Equating one pass with one delivery; deduplicating without stable identities; mutating before validation; accepting unsupported negative updates; counting only payload bytes; changing seeds across restore; merging overlapping partitions; assuming floating-point associativity; finalizing windows from wall-clock time; letting a checkpoint advance beyond state durability; dropping overload silently; and reporting an error bound outside its theorem's update or adversary model.

### Compact example

A strict-turnstile counter at sequence 3 holds `pear=2`. Update `(4, pear, -3)` is invalid. If code decrements first and validates later, state becomes `-1` even though the position may remain 3. Transactional validation computes the prospective value, rejects it, and leaves both state and sequence unchanged; a corrected sequence-4 update can then proceed.

### Connections

[ALGE-074](./074-streaming-frequency-estimation.md) through [ALGE-077](./077-reservoir-sampling.md) supply concrete summaries. [ALGE-078](./078-dynamic-connectivity.md) and [ALGE-079](./079-dynamic-shortest-path-and-reachability-concepts.md) supply dynamic-update semantics. ALGE-081 next begins parallel work/span analysis.

## Governing Question

Given an unbounded input, a limited pass and memory budget, a declared update algebra, and operational requirements for ordering, retries, recovery, latency, and audit, how should an engineer specify, implement, validate, and operate an algorithm so that every published result has defensible semantics and evidence?

## Why This Matters

Streaming algorithms are often introduced as elegant state updates: hash an item, increment counters, compact a buffer, or replace a sample. A production stream adds a second problem. Records are delivered by transports, decoded under evolving schemas, retried after failures, partitioned across workers, reordered by networks, assigned event times, checkpointed, merged, and exposed while new input continues. The theorem usually assumes a logical sequence; the system must construct that sequence.

“One pass” is a resource constraint, not a reliability guarantee. Processing the same logical event twice is still two updates even if each delivery was read once. Skipping a gap preserves throughput but changes the mathematical input. Restoring state with a different random seed changes the estimator. Merging summaries for overlapping partitions double-counts. Finalizing an event-time window because processing time advanced confuses two clocks.

The engineering objective is therefore traceability. For a result, we should be able to name which logical updates it contains, which model accepted them, which state transition processed them, which resource and error contract applies, and how the same state can be reconstructed. This chapter synthesizes the preceding online, streaming, sampling, and dynamic modules into that operating discipline.

## Prerequisites and Retrieval

Retrieve asymptotic and resource models from ALGE-003 through ALGE-006, randomized guarantees from [ALGE-068](./068-monte-carlo-and-las-vegas-algorithms.md), online information constraints from [ALGE-071](./071-online-decisions-and-competitive-analysis.md), frequency, distinct, quantile, and sampling summaries from [ALGE-074](./074-streaming-frequency-estimation.md), [ALGE-075](./075-distinct-counting.md), [ALGE-076](./076-streaming-quantiles.md), and [ALGE-077](./077-reservoir-sampling.md), and versioned updates from [ALGE-078](./078-dynamic-connectivity.md). You should be able to state an invariant, distinguish a logical event from a delivery, and interpret probabilistic error.

## Learning Objectives

After this module, you should be able to:

1. write a complete streaming algorithm contract across input, update, resource, accuracy, order, and failure dimensions;
2. distinguish cash-register, strict-turnstile, and general-turnstile semantics;
3. implement validation-before-mutation with contiguous sequence and bounded-state invariants;
4. explain why deduplication, ordering, checkpointing, and replay are outside a sketch theorem but inside component correctness;
5. prove or reject summary mergeability, including partition and metadata preconditions;
6. design event-time, late-data, retraction, overload, and publication policies;
7. construct exhaustive, differential, metamorphic, recovery, and adversarial checks; and
8. decide honestly when to approximate, spill, batch, rebuild, or reject work.

## Core Exposition

### Begin with a model matrix

Define the universe $U$, logical updates, query, number of passes $p$, state budget $M$, per-update budget $T_u$, and output budget. For a frequency vector $f\in\mathbb{Z}^{|U|}$, an update $(i,\Delta)$ means $f_i\leftarrow f_i+\Delta$. The cash-register model requires $\Delta\ge0$. Strict turnstile permits signed $\Delta$ while maintaining $f_i\ge0$ after every prefix. General turnstile permits negative coordinates. An algorithm proved for one model does not inherit correctness in another.

Then name accuracy. Exactness may force state proportional to the universe or distinct keys. An estimate needs parameters such as $\varepsilon$ and $\delta$, the inequality they govern, whether probability is per query or simultaneous, and the adversary's knowledge of randomness. Foundational frequency-moment results demonstrate that pass and memory restrictions materially change what is computable [2]. The contract must also say whether queries occur only at end or at arbitrary prefixes.

Finally define the physical envelope: serialization, integer widths, floating-point behavior, hash family and seeds, maximum keys or cells, metadata, allocation policy, external spill, parallel partitions, and failure response. “Uses 10 MB” must include object, allocator, index, seed, checkpoint, and temporary merge memory, not merely counter payload.

### Separate logical input from delivery

Let a stable event identity denote business meaning, while a delivery identity denotes one transport attempt. A retry of the same event should not become a new logical update unless the domain explicitly says so. Sequence numbers can establish a total order within one partition, but independent partitions have only a partial order until the query defines how to combine them.

Deduplication needs retained evidence. Remembering every event ID violates bounded memory on an unbounded stream. Alternatives include upstream transactional positions, finite idempotency windows, durable indexes, partition epochs, or accepting at-least-once semantics and using an idempotent update algebra. Each changes the contract. A probabilistic duplicate filter can reject new events falsely and therefore changes correctness; its error cannot be hidden as an implementation detail.

The phrase “exactly once” is best decomposed: each logical update contributes once to each committed output, despite replay. Achieving that outcome typically coordinates input position, state, and output commit. Merely configuring a consumer flag or writing idempotent code is insufficient evidence.

### Make a transition atomic

For logical sequence $j+1$, validate sequence, schema, identity, update model, capacity, numeric range, and configuration before mutating. Compute the prospective state or a mutation log. Commit state and last sequence atomically, or arrange replay so an interrupted transition is detectably repeated without double effect. Rejection leaves every invariant and the expected next sequence unchanged.

The following bounded exact counter is deliberately small. Its purpose is to expose transition semantics, not to solve high-cardinality frequency estimation. It supports strict-turnstile updates over at most three live keys, requires contiguous sequence numbers, removes zero coordinates, and creates a canonical checkpoint.

<!-- bijux-verify: {"id":"transactional-one-pass-updates","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"seq=1 state={'apple': 3}\nseq=2 state={'apple': 3, 'pear': 2}\nseq=3 state={'apple': 2, 'pear': 2}\nreject: strict-turnstile violation\nafter reject: seq=3 state={'apple': 2, 'pear': 2}\nreject: expected sequence 4\nseq=4 state={'apple': 2, 'pear': 2, 'plum': 1}\nreject: key capacity exceeded\ncheckpoint: {\"last_sequence\":4,\"max_keys\":3,\"model\":\"strict_turnstile\",\"state\":{\"apple\":2,\"pear\":2,\"plum\":1}}\n","stderr":""}} -->
```python
class StrictTurnstileCounter:
    def __init__(self, max_keys):
        self.max_keys = max_keys
        self.last_sequence = 0
        self.state = {}

    def apply(self, sequence, key, delta):
        if sequence != self.last_sequence + 1:
            raise ValueError(f"expected sequence {self.last_sequence + 1}")
        if not isinstance(delta, int) or delta == 0:
            raise ValueError("delta must be a nonzero integer")
        prospective = self.state.get(key, 0) + delta
        if prospective < 0:
            raise ValueError("strict-turnstile violation")
        live_after = len(self.state) + (key not in self.state and prospective > 0)
        if live_after > self.max_keys:
            raise ValueError("key capacity exceeded")
        # All fallible preconditions precede mutation.
        if prospective == 0:
            self.state.pop(key, None)
        else:
            self.state[key] = prospective
        self.last_sequence = sequence

    def checkpoint(self):
        # This exercise admits identifier-like keys; a real serializer must
        # escape arbitrary key bytes and version its canonical encoding.
        entries = ",".join(
            f'"{key}":{self.state[key]}' for key in sorted(self.state)
        )
        return (
            f'{{"last_sequence":{self.last_sequence},'
            f'"max_keys":{self.max_keys},'
            f'"model":"strict_turnstile","state":{{{entries}}}}}'
        )


counter = StrictTurnstileCounter(max_keys=3)
for update in [(1, "apple", 3), (2, "pear", 2), (3, "apple", -1)]:
    counter.apply(*update)
    print(f"seq={counter.last_sequence} state={counter.state}")
try:
    counter.apply(4, "pear", -3)
except ValueError as error:
    print("reject:", error)
print(f"after reject: seq={counter.last_sequence} state={counter.state}")
try:
    counter.apply(5, "plum", 1)
except ValueError as error:
    print("reject:", error)
counter.apply(4, "plum", 1)
print(f"seq={counter.last_sequence} state={counter.state}")
try:
    counter.apply(5, "kiwi", 1)
except ValueError as error:
    print("reject:", error)
print("checkpoint:", counter.checkpoint())
```

The exact dictionary can still exceed a realistic memory target when `max_keys` is large; a fixed capacity makes overload explicit. Production code also needs bounded key bytes, integer overflow checks, stable serialization, durable atomicity, and authentication. Successful local execution proves only this transition trace in the recorded environment.

### Choose approximation deliberately

If exact state cannot fit, decide which information may be lost. Count-Min estimates frequencies with one-sided additive error under its assumptions [3]; distinct counters, quantile sketches, and reservoir samples answer different questions. None is a generic “compressed stream.” Choose from the query and loss function, not from familiarity.

Budget errors across the system. If $q$ adaptive queries each have individual failure probability $\delta$, simply claiming system failure probability $\delta$ is wrong. A union bound may require per-query parameters near $\delta/q$, when its assumptions apply. Sampling error, hash collision, late-data omission, numerical rounding, and dropped overload are different mechanisms and should not be folded into one undocumented percentage.

Preserve seeds and configuration in checkpoints. Rotating a seed changes which collisions or sample priorities occur. Rotation may be valuable against adversaries, but it requires a new epoch, a rebuild or parallel state, and explicit query semantics across epochs.

### Prove mergeability instead of assuming it

For disjoint logical partitions $A$ and $B$, a summary is mergeable when an operation $\oplus$ satisfies a declared relation such as

$$
\Sigma(A\mathbin{\|}B)=\Sigma(A)\oplus\Sigma(B),
$$

perhaps in distribution rather than bit-for-bit. The identity state, associativity, partition requirements, parameter compatibility, and randomness coupling must be established. Fully mergeable summaries are studied as a property, not a default [4].

Overlap invalidates the equation unless updates carry invertible provenance. Merging the same shard twice double-counts even when $\oplus$ is associative. Order-sensitive summaries may permit only sequence-respecting concatenation. Floating-point addition is not mathematically associative in finite precision, so different merge trees can yield different bits; reproducibility requires a fixed tree, exact accumulator, or declared tolerance.

### Bound time as well as memory

A summary that fits memory can still fall behind. Measure decoding, hashing, allocation, state access, compaction, checkpointing, merge, and output. Average update time hides compaction spikes and adversarial keys. Define a maximum backlog and a response: backpressure, spill to a governed store, shed only explicitly optional data, degrade to a named estimator, or fail unavailable. Silent drop changes the logical stream and voids the theorem.

One-pass input does not ban external state by definition; it requires the cost model to name it. If an algorithm spills every record, it is not a sublinear-memory streaming solution in the usual internal-memory model even if its RAM counter is small. Count bytes read and written, random I/O, network calls, and recovery bandwidth.

### Distinguish event time from processing time

An event carries domain time; processing time records when a worker handles it. Network delay makes them diverge. Windows need a policy for membership, triggers, allowed lateness, retractions, and finality. The Dataflow model's separation of what, where in event time, when in processing time, and how refinements relate is a durable way to expose these choices [6].

A watermark is imperfect knowledge of event-time progress. If a late record arrives after an early result, the system may discard it, revise the output, emit a compensating retraction, or reopen state. Each policy changes observable semantics and retained memory. “Final” must mean something stronger than “the timer fired.”

Turnstile-capable algorithms can sometimes absorb retractions algebraically, but only if a retraction identifies the original contribution and the summary supports signed updates. A negative delta is not sufficient for noninvertible operations such as arbitrary minima, samples without retained priority, or lossy compression.

### Checkpoint and replay one version

A checkpoint should include state bytes, last logical position per partition, algorithm and schema version, update model, parameters, seeds, numeric policy, partition ownership, event-time frontier, and integrity checksum. State and positions must describe the same cut. Distributed snapshots formalize the need for a consistent global state rather than independently timed local copies [7].

Recovery checks compatibility, restores the checkpoint, and replays a contiguous suffix. Test failure before mutation, during mutation, after state persistence but before position commit, after position commit but before output publication, and during checkpoint replacement. A replay that produces semantically equal but byte-different floating state may still be acceptable only if the contract says so and queries remain within tolerance.

Schema changes need migration or a new epoch. Reinterpreting old bytes under a new key normalization can merge or split coordinates. Keep old code/readers long enough to validate migration, or rebuild from a durable source. An unbounded stream without retained input cannot be rebuilt; that is a deliberate recovery limitation, not an inconvenience to omit.

### Validate properties, prefixes, and recovery

For small universes, enumerate valid update sequences and compare every prefix with an exact oracle. Test rejected updates leave a byte-identical state and position. Metamorphic checks are powerful: splitting and validly merging disjoint partitions should match the declared merge relation; checkpoint-restore-replay should match uninterrupted processing; inserting then retracting an update should restore state only for an invertible model; permuting records should preserve results only for order-insensitive algorithms.

Exercise numeric boundaries, maximum key length, counter overflow, empty input, all-equal input, skew, hash collisions, duplicate delivery, gap, reordering, overlapping shards, seed mismatch, corrupt checkpoint, partial output, watermark regression, extremely late data, and overload. Random tests supplement, not replace, constructed counterexamples and exhaustive bounded domains.

Observe logical and delivered counts, duplicates, gaps, invalid updates, state bytes, allocation, update latency tails, backlog, compactions, approximation parameters, seed epoch, merge fan-in, checkpoint age and duration, replay lag, watermark, late records, retractions, overload actions, oracle discrepancies, and published version. These metrics make semantic drift diagnosable.

## Definitions and Notation

Let the logical stream be $u_1,u_2,\ldots$, and let $S_j$ be state after exactly the first $j$ accepted logical updates. Configuration $C$ contains immutable algorithm semantics for one epoch. The transition $F(S_j,u_{j+1};C)$ either returns a complete next state or rejects without mutation.

For keyed deltas, $f_i^{(j)}$ is coordinate $i$ after prefix $j$. Strict turnstile requires $f_i^{(j)}\ge0$ for every $i,j$. Let $M(S)$ measure complete resident state, $T_u$ update time, $P$ pass count, and $(\varepsilon,\delta)$ declared approximation parameters. Delivery count $D$ can exceed logical count $j$ because of retries.

A partition descriptor names its logical input set or interval. A checkpoint cut $K=(S_j,j,C)$ is consistent when state and positions include exactly the same prefixes. Event time $t_e$ and processing time $t_p$ are separate clocks. A published result is preliminary or final only under a named lateness and revision policy.

## Mechanisms, Invariants, or Proof Structure

### Four proof layers

**Algorithmic validity** proves the state invariant and error theorem for the declared logical model. **Transition validity** proves validation-before-mutation, sequence continuity, capacity, and numeric safety. **Recovery validity** proves a checkpoint and contiguous replay equal uninterrupted transitions. **Publication validity** proves every output corresponds to one committed state/version and declared event-time policy.

The layers compose only when their boundaries match. An excellent sketch fed duplicate logical updates computes an excellent estimate of the wrong vector. Perfect replay of a state whose seed metadata was lost is not the same randomized execution. Atomic state without atomic publication can expose a mixed result.

### Merge proof obligations

Prove that partition summaries cover each logical update exactly once. Establish parameter and seed compatibility. Show identity and associativity of merge at the semantic level, and commutativity only if order is irrelevant. Re-derive error after merge: correlated randomness and multiple queries can alter probability. Account for temporary memory during fan-in and for numeric variation across merge trees.

### Resource and degradation proof

Define a hard state envelope including metadata and temporary work. Demonstrate that every valid update stays within it or follows a documented transition to backpressure, spill, degraded estimator, or rejection. A fallback must preserve a stated guarantee; switching algorithms without changing result metadata is semantic corruption.

## Alternatives and Trade-Offs

**Exact bounded-universe state** offers straightforward answers and deletions but scales with universe or live keys. **Approximate sketches** bound memory and update work while accepting query-specific error. **Sampling** retains examples rather than aggregate answers. **External spill** preserves more exact data but changes I/O and recovery costs.

**Transport-position identity** can make replay efficient but couples state to partition epochs. **Business-event identity** survives repartitioning but requires durable deduplication. **At-least-once plus idempotent updates** is simple only when the update algebra truly is idempotent; increments are not. **Transactional coordination** strengthens outcomes at latency and availability cost.

**Local summaries plus merge** scale throughput if the summary is actually mergeable and partitions do not overlap. **Central ordered processing** simplifies semantics but limits throughput. **Fixed event-time finality** bounds state while dropping or compensating for late facts. **Unbounded correction** improves eventual inclusion but retains state and permits indefinite revisions.

## Failure Modes and Misconceptions

- **“Read once means applied once.”** Delivery retries can duplicate logical effects.
- **“Negative delta means deletion support.”** The algorithm must be proved for strict or general turnstile input and identify what is retracted.
- **“Memory is counters times word size.”** Keys, hash tables, seeds, allocators, buffers, checkpoints, and merge work count too.
- **“Associative on paper means reproducible.”** Finite-precision operations and randomized metadata can vary by merge tree.
- **“A watermark is complete.”** It is a progress signal governed by a late-data policy.
- **“Checkpointing state is enough.”** State, positions, schema, parameters, seed, frontier, and output boundary form one cut.
- **“Exactly once is a consumer setting.”** It is an end-to-end property of logical effect and publication.
- **“Drop on overload and recover later.”** Without a durable source, dropped input is irrecoverable; with one, lag and replay are part of the SLO.
- **“The theorem covers adaptive hostile keys.”** Hash-randomness guarantees depend on what the adversary observes and controls.
- **“One error percentage covers everything.”** Statistical error, lateness, duplicates, numeric rounding, and data loss require separate accounting.
- **“Final-state tests are enough.”** Prefix, rejection, crash-point, merge, and replay defects can disappear by the end.

## Worked Examples

### Example 1

**Situation.** A stream contains arbitrary 128-bit IDs and asks for exact distinct count using 1 MB forever.

**Reasoning.** Exactness must distinguish streams containing different ID sets; the number of possible sets grows beyond the fixed state's distinguishable configurations. A probabilistic distinct sketch can bound memory, or the system can retain external exact state, but neither preserves all three claims: one pass, fixed tiny state, and exactness over an unbounded universe.

**Conclusion.** Relax accuracy, bound the universe/input, or admit external storage; do not hide the impossibility behind compression language.

### Example 2

**Situation.** Frequencies are `a=2,b=1`. Update `(a,-3)` arrives under strict-turnstile semantics.

**Reasoning.** The prospective coordinate is $-1$, violating the prefix invariant. General turnstile might accept it, but changing models alters query meaning and compatible algorithms. Validation must occur before state or sequence mutation.

**Conclusion.** Reject atomically under strict turnstile; model choice is part of correctness.

### Example 3

**Situation.** Sequence 41 is processed, then delivery 41 retries, followed by 43 while 42 is delayed.

**Reasoning.** Applying both 41 deliveries double-counts; accepting 43 creates an unrecorded gap. A contiguous-position processor recognizes the retry and gap, but after repartitioning it also needs an epoch. Business-level deduplication may need stronger identities.

**Conclusion.** One-pass computation requires construction of a logical sequence from imperfect delivery.

### Example 4

**Situation.** A sketch advertises 8 MiB of 64-bit counters. The process limit is 10 MiB.

**Reasoning.** Counter payload already consumes 8 MiB. Two hash seeds, row pointers, object headers, allocator rounding, input buffers, a checkpoint copy, and a simultaneous merge can exceed 10 MiB. Peak resident state, not formula payload, controls survival.

**Conclusion.** Measure and budget the complete lifecycle, including temporary duplication.

### Example 5

**Situation.** Two workers summarize events 1–100 and 81–180, then merge by addition.

**Reasoning.** Events 81–100 occur in both inputs. Even a perfectly associative merge counts them twice. The summary cannot infer overlap without provenance that may defeat its size goal.

**Conclusion.** Mergeability requires exact-once partition coverage, not merely a merge function.

### Example 6

**Situation.** Three floating partial sums are $10^{16}$, $-10^{16}$, and $1$.

**Reasoning.** Under common binary floating arithmetic, $(10^{16}+(-10^{16}))+1$ yields 1, while $10^{16}+((-10^{16})+1)$ may yield 0 because the inner `+1` is rounded away. Both merge trees implement real addition but not bitwise associative machine addition.

**Conclusion.** Fix merge order, use a stronger accumulator, or declare numeric tolerance and nondeterminism.

### Example 7

**Situation.** State through sequence 900 is durable, but the input position checkpoint says 901.

**Reasoning.** Recovery resumes at 902 and permanently omits 901. The reverse mismatch—state through 901, position 900—replays and double-applies it for non-idempotent updates.

**Conclusion.** State and position must commit as one consistent checkpoint cut.

### Example 8

**Situation.** A window for event-time minute 12 emits when processing time reaches 12:02; an event timestamped 12:00:40 arrives at 12:03.

**Reasoning.** Processing-time delay says nothing logically conclusive about event time. The policy must drop, revise, retract-and-replace, or reopen. Each choice changes accuracy, state retention, and consumer behavior.

**Conclusion.** A timer is not event-time finality; lateness and revision are API semantics.

### Example 9

**Situation.** A public endpoint reveals sketch estimates, and an attacker adaptively chooses later keys to amplify collisions.

**Reasoning.** A guarantee proved for keys independent of a secret seed may not cover this adaptive interaction. Persisting one seed aids replay but extends exposure; rotating it creates epochs requiring explicit combination or rebuild.

**Conclusion.** State the adversary model and design seed secrecy, rotation, rate limits, and validation accordingly.

### Example 10

**Situation.** Update latency exceeds the arrival interval and backlog reaches its limit.

**Reasoning.** Silent discard computes over an undocumented subsequence. Backpressure preserves input if upstream retains it; spill changes the cost model; a coarser summary changes error; failure preserves honesty but availability drops. The correct response depends on a predeclared degradation contract.

**Conclusion.** Overload is a semantic branch, not only a performance incident.

## Cross-Program Connections

- **Data Engineering:** event identity, schemas, partitions, watermarks, retractions, and replay construct the logical stream consumed by the algorithm.
- **Database Engineering:** atomic state/position commits and snapshot publication mirror transaction and recovery obligations.
- **Systems Engineering:** capacity, backpressure, degraded modes, recovery objectives, and observability turn asymptotic state into an operable service.
- **Security Engineering:** hostile keys, seed exposure, unauthenticated updates, replay, and resource exhaustion can invalidate benign-input guarantees.
- **Concurrent and Parallel Programming:** merge trees, partial orders, atomic publication, and memory visibility determine whether local summaries compose.
- **Data Architecture Engineering:** retention and lineage decide whether an approximate or corrupted state can be rebuilt from authoritative data.

## References

1. S. Muthukrishnan, *Data Streams: Algorithms and Applications*, Foundations and Trends in Theoretical Computer Science 1(2), 2005, 117–236. DOI: [10.1561/0400000002](https://doi.org/10.1561/0400000002). Authoritative monograph for pass, memory, cash-register, and turnstile models; publisher and bibliographic records checked 2026-09-05.
2. Noga Alon, Yossi Matias, and Mario Szegedy, “The Space Complexity of Approximating the Frequency Moments,” *28th ACM Symposium on Theory of Computing*, 1996, 20–29. DOI: [10.1145/237814.237823](https://doi.org/10.1145/237814.237823). Primary source for foundational streaming space upper and lower bounds; ACM and author records checked 2026-09-05.
3. Graham Cormode and S. Muthukrishnan, “An Improved Data Stream Summary: The Count-Min Sketch and Its Applications,” *Journal of Algorithms* 55(1), 2005, 58–75. DOI: [10.1016/j.jalgor.2003.12.001](https://doi.org/10.1016/j.jalgor.2003.12.001). Primary source illustrating a model-specific one-pass error contract; publisher and author records checked 2026-09-05.
4. Pankaj K. Agarwal, Graham Cormode, Zengfeng Huang, Jeff M. Phillips, Zhewei Wei, and Ke Yi, “Mergeable Summaries,” *31st ACM Symposium on Principles of Database Systems*, 2012, 23–34. DOI: [10.1145/2213556.2213562](https://doi.org/10.1145/2213556.2213562). Primary source for mergeability as a proved summary property; ACM-linked and author records checked 2026-09-05.
5. Michael Stonebraker, Uğur Çetintemel, and Stanley Zdonik, “The 8 Requirements of Real-Time Stream Processing,” *ACM SIGMOD Record* 34(4), 2005, 42–47. DOI: [10.1145/1107499.1107504](https://doi.org/10.1145/1107499.1107504). Primary systems source for ordering, integration, predictability, and availability requirements; ACM-linked records checked 2026-09-05.
6. Tyler Akidau et al., “The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing,” *Proceedings of the VLDB Endowment* 8(12), 2015, 1792–1803. DOI: [10.14778/2824032.2824076](https://doi.org/10.14778/2824032.2824076). Primary source for event time, processing time, windows, triggers, watermarks, and refinements; official VLDB record checked 2026-09-05.
7. K. Mani Chandy and Leslie Lamport, “Distributed Snapshots: Determining Global States of Distributed Systems,” *ACM Transactions on Computer Systems* 3(1), 1985, 63–75. DOI: [10.1145/214451.214456](https://doi.org/10.1145/214451.214456). Primary source for consistent distributed cuts; ACM-linked and author records checked 2026-09-05.
8. IEEE, *IEEE Standard for Floating-Point Arithmetic*, IEEE 754-2019, published 2019. DOI: [10.1109/IEEESTD.2019.8766229](https://doi.org/10.1109/IEEESTD.2019.8766229). Official standard used for finite-precision engineering context; IEEE record checked 2026-09-05.

## Exercises

### Exercise 1

Define a logical stream, one pass, cash-register, strict turnstile, general turnstile, mergeable summary, watermark, and consistent checkpoint. Explain which pairs are commonly conflated.

### Exercise 2

For the executable counter, prove sequence continuity, strict-turnstile nonnegativity, capacity, rejection atomicity, and checkpoint determinism. Identify assumptions the Python demonstration does not prove for a production implementation.

### Exercise 3

A pipeline retries increments, accepts gaps, counts only counter payload for memory, merges overlapping shards, restores with fresh seeds, and finalizes windows from processing time. Diagnose each defect and give a focused test.

### Exercise 4

Design a one-pass service estimating per-tenant frequencies under 4 GiB RAM, 500,000 updates/s, signed corrections, adaptive queries, hourly checkpoints, ten-minute recovery, and late events. Specify model, error, partitioning, identity, merge, numeric, overload, publication, and validation contracts.

### Exercise 5

A medical-device fleet loses raw telemetry after ingestion but demands exact retrospective recalculation after algorithm upgrades. Assess feasibility and design the smallest honest change in retention, pass count, state, or guarantee. Include security, audit, recovery, and failure behavior.

## Answers to the Exercises

### Answer 1

A logical stream is the mathematical ordered update sequence; delivery attempts are how records arrive. One pass consumes each logical update at most once in sequence while retaining bounded state. Cash-register accepts nonnegative increments; strict turnstile accepts signed deltas but every coordinate stays nonnegative at every prefix; general turnstile may allow negative coordinates. A mergeable summary combines valid partition states under a proved operation. A watermark expresses event-time progress knowledge or estimate under a policy. A consistent checkpoint binds state, positions, and semantic metadata to one cut. Common conflations are one pass with exactly-once effect, negative-delta syntax with turnstile correctness, a merge method with mergeability, watermark with completeness, and independently saved state/positions with a consistent checkpoint.

### Answer 2

The sequence precondition requires exactly `last_sequence+1`; the field advances only after all checks, so accepted updates are contiguous. `prospective=current+delta` is checked nonnegative before assignment, preserving strict turnstile by induction from the empty state. `live_after` prevents a fourth positive coordinate, and zero removal cannot increase capacity. Every exception occurs before either dictionary or sequence mutation, establishing rejection atomicity for these synchronous checks. Sorting keys and fixing JSON separators and field values makes the checkpoint deterministic for the demonstrated value types and Python behavior. The example does not prove crash atomicity, thread safety, bounded key bytes, machine integer overflow, durable storage, authenticated input, filesystem atomic replacement, stable behavior across serializer versions, distributed sequence semantics, or full memory bounds. Those require additional implementation and evidence.

### Answer 3

Retrying increments double-counts because addition is not idempotent; replay the same event ID and compare against one application. Gaps omit logical updates; present sequences 1 and 3 and require rejection until 2 arrives. Payload-only accounting misses overhead and peaks; measure resident memory during update, checkpoint, and merge at maximum key sizes. Overlapping shard merge double-counts; label partitions and deliberately overlap a range. Fresh seeds change collisions or samples; checkpoint, restore, and require seed/config equality and matching queries. Processing-time finalization mishandles late event time; emit a window, inject an earlier-timestamped record later, and verify the declared drop or correction behavior. Each test checks an observable semantic promise, not merely process survival.

### Answer 4

Define keyed integer deltas under strict turnstile if true counts cannot be negative; reject or quarantine violations. Choose a Count-Min-like or other frequency summary only after specifying one-sided error, $\varepsilon$, simultaneous/adaptive query treatment, and hostile-key assumptions. Partition by authenticated tenant/key with epochs and nonoverlap; use stable business IDs or transactional positions so retries contribute once. Merge only compatible seeds, widths, depths, schemas, epochs, and disjoint ranges, and re-derive the global probability contract. Use checked integer counters or a documented saturation policy. Hourly consistent checkpoints include per-partition positions, seeds, schema, parameters, and event-time frontier; size replay retention and throughput to restore within ten minutes and test it. Define allowed lateness, trigger, corrections, and finality. At backlog limits apply backpressure or durable spill; any degraded estimator gets distinct metadata. Observe delivered/logical rates, duplicates, gaps, invalid corrections, bytes, update tails, lag, errors, seed epochs, merge coverage, checkpoint/replay, late data, retractions, and oracle samples. Validate exhaustive bounded traces, exact shadow samples, merge metamorphisms, crash points, adaptive-key tests, and capacity faults.

### Answer 5

The requirements conflict if discarded raw input contains information absent from bounded algorithm state: no later algorithm can reconstruct facts the retained state did not preserve. Exact retrospective recalculation after arbitrary upgrades therefore needs durable authoritative telemetry, a lossless sufficient statistic fixed in advance for the entire future query family, or a bounded input/universe small enough to retain exactly. The smallest generally honest change is encrypted, access-controlled, integrity-checked retention for a governed period plus replayable schema and event identity; this changes the system from one-pass-only computation to retained-input recomputation. If retention is legally or physically impossible, narrow the guarantee to queries supported by the stored exact state or disclose approximation and non-recalculability. Authenticate devices, protect keys, record consent and lineage, audit reads and transformations, test checkpoint and archive restoration, and define missing/corrupt segment behavior. On evidence gaps, return incomplete/unavailable with exact coverage rather than fabricating an exact result.
