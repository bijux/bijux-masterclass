---
module_id: SEPAT-034
program: Software Engineering: Patterns
level: 1
module_number: 34
title: Iterator
status: complete
last_verified: 2026-08-28
---

# Iterator

## One-Page Review

### Governing question

How can clients traverse a collection or computed sequence without depending on its representation, while order, multiplicity, mutation, lifetime, failure, consistency, and cost remain explicit?

### Essential definitions

- An **aggregate** owns elements or a rule for producing them; an **iterator** owns traversal state.
- A **cursor** is the iterator state identifying what can be produced next; it is not necessarily an integer index.
- An **external iterator** lets the client request each step; an **internal iterator** owns the loop and invokes client behavior.
- A **single-pass iterator** cannot be assumed to restart or support an independent second traversal; a **multi-pass iterator** can under its stated equality/lifetime rules.
- A **lazy iterator** defers production until demand; an adapter transforms one iterator into another without necessarily materializing results.
- A **snapshot iterator** traverses one fixed logical version; **fail-fast** detects some invalidating mutation; **weakly consistent** traversal permits documented concurrent change without promising a snapshot.
- **invalidation** means an operation makes an iterator, cursor, or yielded reference unusable under the protocol.
- A **distributed continuation token** resumes a versioned query/order context; it is not a raw trusted array position.

### Central model, mechanism, or theorem

Represent a pull iterator as state machine (I=(S,s_0,step)), where

$$
step(s)=End\quad\text{or}\quad step(s)=(x,s').
$$

Correct traversal is relative to a declared logical source version, encounter order, and mutation policy. If a finite snapshot has (n) elements, every successful step advances a rank (r) from 0 toward (n), emits the element at that rank exactly once for that iterator, and exhaustion occurs at (r=n). This local argument does not establish thread safety, freshness, bounded latency, cleanup, or exactly-once processing effects.

### Critical invariants

- Aggregate representation is hidden; the iterator exposes only the promised element/reference and traversal operations.
- Encounter order, multiplicity, direction, and end behavior are defined rather than inferred from storage.
- Each successful advance changes iterator state monotonically; exhaustion and post-exhaustion behavior follow the language protocol.
- Single-pass versus multi-pass, borrowing/ownership, yielded-reference lifetime, and aliasing are explicit.
- Mutation policy is exactly one documented model: prohibited/undefined, iterator-mediated, fail-fast, snapshot, or weakly consistent.
- Lazy adapters preserve order and cardinality according to their laws and do not repeat hidden effects accidentally.
- Resource-owning traversal has deterministic close/cancel/error paths; abandoned iteration cannot silently leak scarce resources.
- Remote cursors bind query, sort/tie-breaker, scope, version/expiry, and integrity while bounding page size and work.

### Common failures

Common failures include returning the backing array, conflating aggregate and iterator, sharing one cursor across loops, promising restart for a generator, using `hasNext` with an intervening mutation/race, swallowing end-of-stream as `null`, exposing mutable keys, invalidating references unexpectedly, claiming fail-fast is synchronization, materializing an infinite sequence, hiding database/network work behind cheap-looking `next`, leaking cursors on early exit, retrying after partial side effects, offset pagination under concurrent writes, unsigned client-editable tokens, missing a stable tie-breaker, parallel splitting of an unsplittable source, and benchmarking only full consumption.

### Compact example

A versioned sequence creates a snapshot iterator over `(10,20,30)` at version zero. Appending 40 advances the aggregate to version one, but the iterator still yields exactly the three snapshot values. The semantics are clear because snapshot creation, version capture, order, ownership, and exhaustion are explicit.

### Connections

[SEPAT-033](033-interpreter-as-an-object-pattern.md) traverses syntax trees; [SEPAT-035](../ROADMAP.md) coordinates collaborators. Iterator connects to [Object-Oriented Programming](../../02-programming-languages-object-oriented-programming/ROADMAP.md), [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md), and [Database Engineering](../../18-database-engineering/ROADMAP.md).

## Governing Question

What traversal contract lets an algorithm consume elements without seeing representation, and what must it say about order, progress, mutation, ownership, effects, failure, and cost?

Iterator separates “how to visit” from “how elements are stored or produced.” That small interface becomes a semantic boundary when traversal is lazy, mutable, concurrent, resource-owning, asynchronous, parallel, or remote.

## Why This Matters

Arrays, trees, hash tables, database plans, directory streams, parsers, event feeds, and generated sequences require different traversal machinery. Algorithms should often depend on an element protocol rather than every representation.

The abstraction also hides danger. One step may be constant-time memory access, tree navigation, decompression, a database fetch, or a blocking network request. Production-quality iteration makes those costs and lifetimes observable enough to use safely.

## Prerequisites and Retrieval

You should understand encapsulation, collections, references/ownership, asymptotic cost, mutation, concurrency, transactions, pagination, exceptions/results, and resource cleanup. Retrieve these facts:

1. Traversal order is an API property only when specified; physical storage order is not a substitute.
2. A value, borrowed reference, mutable reference, and handle have different lifetime and aliasing obligations.
3. A stateful object reused by two consumers creates interference unless sharing is explicitly synchronized and meaningful.
4. Laziness changes when work, failure, and side effects occur.
5. Concurrent modification requires a consistency model, not merely a defensive exception.
6. Remote result sets add query identity, authorization, expiry, consistency, and retry concerns.

## Learning Objectives

After completing this module, you should be able to:

- derive the Iterator pattern from representation independence;
- specify pull, push, synchronous, asynchronous, and split traversal protocols;
- distinguish single-pass, multi-pass, fused, sized, exact-size, and double-ended properties;
- select and enforce a mutation/consistency policy;
- reason about laziness, composition, complexity, side effects, and termination;
- design cleanup, cancellation, error, and retry behavior for resource-owning traversal;
- design stable integrity-protected continuation tokens for remote collections;
- test order, multiplicity, exhaustion, invalidation, resource release, and adversarial costs.

## Core Exposition

### Separate aggregate state from traversal state

The aggregate owns representation and domain invariants. Each iterator normally owns an independent cursor, direction, filters/adapters, source version, and resource handle. Calling `iterator()` twice should create independent traversal state unless the API explicitly returns a one-shot stream.

Do not expose a backing array merely to enable a loop. That leaks mutation and representation choices and prevents changing from contiguous storage to a tree, compressed segment, or generated source.

### Specify the smallest honest protocol

A pull protocol needs an advance operation whose result distinguishes element, end, and failure when failure is possible. Some languages separate `hasNext` and `next`; others return optional/result values or use a distinguished exhaustion signal.

`hasNext` followed by `next` is safe only under the protocol's mutation/concurrency assumptions. It should not be read as an atomic reservation unless the interface says so. Prefer a single advance result when races or expensive lookahead make the split misleading.

### Define encounter order and multiplicity

Sequences usually promise index order. Trees may promise preorder, inorder, postorder, breadth-first, or no order. Hash collections often provide no stable order unless documented. Queries require an explicit total ordering if resumable pagination must avoid ambiguity.

Define whether duplicates are retained, whether filtering is stable, and whether a map view yields keys, values, or entries. Clients must not infer determinism from one run.

### State traversal category

A single-pass iterator supports one consumption history. Copying it may alias the same cursor, be forbidden, or produce a second handle with source-specific behavior. A multi-pass iterator supports independent copies/restarts under defined equality and lifetime rules.

Additional capabilities should be advertised, not guessed: exact or estimated remaining size, double-ended traversal, random access, sorted/distinct/non-null properties, stable references, and ability to split. Algorithms can select valid optimizations from these traits.

### Make exhaustion precise

The end condition is not an ordinary data value when the element domain can contain that value. Protocols use an option, tagged result, exception/sentinel outside the domain, or callback completion.

Some protocols guarantee fused exhaustion: once ended, every later advance remains ended. Others do not. Unless the contract promises resumption, consumers should stop at end and not probe indefinitely.

### Choose mutation semantics deliberately

There are several legitimate models:

- prohibit or leave external mutation undefined while iterating;
- permit a narrow iterator-owned mutation with precise cursor adjustment;
- detect version change and fail fast as a debugging aid;
- copy or pin a snapshot and traverse its fixed logical contents;
- provide a weakly consistent concurrent view that may reflect some changes under documented no-corruption/no-duplication bounds.

Fail-fast is best-effort detection, not a lock, transaction, memory barrier, or correctness proof. Snapshot traversal costs memory/version retention and may be stale. Weak consistency improves availability but complicates reasoning about omission and duplication.

### Protect yielded references

An iterator may yield copied values, immutable references tied to aggregate lifetime, mutable references with exclusive borrowing, or handles requiring later resolution. State when an advance invalidates the previous item, when aggregate mutation invalidates all items, and whether consumers may retain them.

Never yield mutable map/set keys if mutation can violate hashing or ordering invariants. A safe API may expose immutable entries or controlled update operations instead.

### Compose lazily with laws

`map`, `filter`, `take`, `skip`, `zip`, `chain`, `flatMap`, and `fold` form traversal pipelines. Laziness avoids intermediate materialization and can terminate on an infinite source when bounded by `take`.

For pure function (f), mapping preserves order and cardinality: (map(f,[x_0,...])=[f(x_0),...]). Filtering preserves relative order but not cardinality. `zip` usually ends when either source ends. `flatMap` can amplify work and may never reach later outer elements if one inner iterator is infinite.

### Expose effects and evaluation timing

Lazy pipelines run predicates, mapping functions, I/O, and errors only when pulled. Reiterating a replayable source repeats those actions; consuming a one-shot source does not replay it. Avoid hidden non-idempotent effects in adapters or document exactly-once-within-one-traversal scope and partial-failure behavior.

Memoization trades memory and freshness for replay. It also needs bounds, exception policy, thread safety, and cleanup.

### Account for complexity

Advertise meaningful per-step and total bounds. Linked-list advance can be (O(1)); a poorly implemented indexed iterator over a linked list can become (O(n^2)). Tree traversal may use (O(h)) stack. Filtering has variable work per emitted item. Remote iteration may fetch pages, so calls, bytes, and latency matter alongside CPU.

Size hints are contracts with different strength: lower bound, upper bound, estimate, or exact remaining count. Treating an estimate as exact can cause overflow, under-allocation assumptions, or premature termination.

### Own scarce resources

Database cursors, file/directory streams, decompression contexts, and subscriptions need close semantics. Exhaustion, explicit close, early loop exit, exception, cancellation, and object abandonment must have defined behavior.

Use lexical/resource scopes where available. Finalizers are fallback mechanisms, not timely release. Bound open iterators per principal, idle lifetime, page/buffer size, and server work.

### Distinguish pull from push and async demand

External pull gives the consumer control over pacing. Internal iteration or push invokes consumer code and must define reentrancy, exception, cancellation, and whether producer speed can overwhelm the consumer.

Asynchronous iteration makes waiting explicit. A demand-aware stream adds a protocol for requested capacity, delivery, terminal completion/error, and cancellation. A synchronous iterator whose `next` secretly blocks on a network is difficult to time out and operate.

### Split only with valid algebra

Parallel traversal needs a splitting operation that partitions remaining elements without overlap or loss under stated order. Balanced splitting, cheap partition discovery, source immutability/concurrency, and associative reduction determine benefit.

Even a correct split can yield a different floating-point result or side-effect order. Ordered parallel output may require buffering. Do not mark an iterator splittable because the type system permits it.

### Treat remote cursors as protocols

Offset pagination is simple but work can grow with offset, and concurrent inserts/deletes can shift positions. Keyset/seek pagination resumes after a stable ordered key and unique tie-breaker, but it still needs a consistency policy.

An opaque token should bind query/filter, total sort and last key, tenant/principal or safe scope, snapshot/version if offered, page-size policy, schema/protocol version, and expiry. Integrity-protect or store it server-side; validate all fields and never turn decoded client bytes directly into SQL. Tokens are resumable capabilities and may be sensitive.

### Test the protocol, not only a loop

Property-test emitted order/multiset against a reference model for empty, singleton, duplicate, and large sources. Test independent iterators, partial consumption, exhaustion and repeated end, adapter composition, exceptions, cancellation, early release, and source mutation under every supported policy.

For concurrent/remote sources, test races, snapshot expiry, duplicate/missing boundaries, equal sort keys, authorization change, token tampering/replay, schema migration, timeouts, partial pages, retry, backpressure, and resource quotas. Benchmark first item, partial consumption, full traversal, and abandoned traversal.

## Definitions and Notation

Let source (A) define logical sequence (L_v=(x_0,...,x_{n-1})) at version (v). A snapshot iterator state is (s=(v,r)), where $0\le r\le n$:

$$
step(v,r)=
\begin{cases}
(x_r,(v,r+1)) & r<n,\\
End & r=n.
\end{cases}
$$

For a filter predicate (p), `filter(p,I)` repeatedly advances (I) until it finds (x) with (p(x)), reaches end, or returns failure. Thus one emitted step can consume multiple source steps.

Let continuation token (t=Protect(q,o,k,v,e,s)): query digest (q), total order specification (o), last emitted key/tie-breaker (k), protocol or snapshot version (v), expiry (e), and authorization-safe scope (s). `Protect` means authenticated integrity or an opaque server-side reference, not reversible encoding alone.

## Mechanisms, Invariants, or Proof Structure

### Iterator design procedure

1. Define logical elements, encounter order, duplicates, and end/failure values.
2. Separate aggregate representation from per-traversal cursor state.
3. Declare single/multi-pass, ownership/borrowing, reference lifetime, and capabilities.
4. Select one mutation/consistency policy and specify invalidation.
5. State laziness, side effects, complexity, blocking, and size guarantees.
6. Define error, cancellation, close, retry, and abandoned-traversal behavior.
7. For remote traversal, bind and protect query/order/scope/version/expiry.
8. Test laws, boundaries, mutation, failures, cleanup, concurrency, and costs.

### Executable mechanism

This example copies a finite snapshot and records the aggregate version at creation. It demonstrates independent traversal state, monotone rank, and stable snapshot contents; it does not model concurrency, large-copy cost, borrowed references, I/O, or remote cursors.

<!-- bijux-verify: {"id":"iterator-versioned-snapshot","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"created=0 current=1 remaining=3\nitems=[10, 20, 30] aggregate=[10, 20, 30, 40]\nended=True remaining=0\n","stderr":""}} -->
```python
class SnapshotIterator:
    def __init__(self, values, source_version):
        self.values = tuple(values)
        self.source_version = source_version
        self.position = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.position == len(self.values):
            raise StopIteration
        value = self.values[self.position]
        self.position += 1
        return value

    def remaining(self):
        return len(self.values) - self.position


class VersionedSequence:
    def __init__(self, values):
        self.values = list(values)
        self.version = 0

    def append(self, value):
        self.values.append(value)
        self.version += 1

    def snapshot_iterator(self):
        return SnapshotIterator(self.values, self.version)


sequence = VersionedSequence([10, 20, 30])
iterator = sequence.snapshot_iterator()
sequence.append(40)
print(f"created={iterator.source_version} current={sequence.version} remaining={iterator.remaining()}")
print(f"items={list(iterator)} aggregate={sequence.values}")
print(f"ended={iterator.position == len(iterator.values)} remaining={iterator.remaining()}")
```

### Finite snapshot argument

Initially (r=0). Each successful step emits (x_r) and changes rank to (r+1), so rank strictly increases and no rank is emitted twice. Since $r\le n$, after exactly (n) successful steps rank equals (n) and the next step is `End`. Induction establishes ordered, complete, duplicate-free traversal of this fixed sequence.

The argument assumes finite immutable snapshot contents, a private cursor, correct indexed access, no exceptions, and arithmetic capable of representing ranks. It proves neither uniqueness of equal-valued elements nor exactly-once downstream effects.

### Review obligations

Review protocol laws, element/reference lifetime, mutation model, cost and termination, effect timing, resource release, concurrency/splitting, and cursor security separately. Empirical tests complement but do not prove all interleavings or remote consistency.

## Alternatives and Trade-Offs

| Approach | Strength | Cost or limitation | Prefer when |
|---|---|---|---|
| Expose representation | Minimal machinery | Breaks encapsulation and evolution | Private local code with stable ownership |
| Index/range loop | Simple and often optimizable | Requires indexed stable sequence | Contiguous/random-access data |
| External pull iterator | Consumer controls pace and composition | Stateful, often single-threaded | General algorithms and lazy pipelines |
| Internal `forEach`/Visitor | Producer controls traversal | Reentrancy/cancellation and early exit harder | Traversal invariants must remain internal |
| Generator/coroutine | Directly expresses suspended control | One-shot lifetime and cleanup can be subtle | Stateful lazy production |
| Materialized collection | Replayable and simple failures | Memory, latency, staleness | Bounded results reused often |
| Snapshot iterator | Stable logical view | Copy/MVCC retention and staleness | Repeatable traversal matters |
| Weakly consistent iterator | Concurrent availability | May observe changing contents | Concurrent structures with explicit semantics |
| Reactive/push stream | Async demand/backpressure | Larger protocol and callback concurrency | Unbounded or event-driven sources |
| Protected continuation token | Stateless/scalable resume | Versioning, expiry, confidentiality, consistency | Remote ordered pagination |

## Failure Modes and Misconceptions

- **“Iterator means one `next` method.”** Order, end, failure, ownership, mutation, cost, and cleanup are the real contract.
- **“Iterable and iterator are interchangeable.”** One creates traversals; the other is a particular traversal state. Some objects are deliberately one-shot.
- **“Fail-fast makes mutation safe.”** It detects some violations and may race; synchronization/consistency require separate mechanisms.
- **“Snapshot means current.”** It is internally stable for a declared version, possibly stale relative to later writes.
- **“Lazy means faster.”** It can reduce work/memory but adds deferred failure, repeated effects, retention, and per-step overhead.
- **“Every iterator can be counted first.”** Counting may consume, block, be infinite, or cost as much as traversal.
- **“End can be represented by null.”** Only if null is excluded from the element domain and the protocol says so.
- **“A copied iterator is independent.”** That is true only for a multi-pass/copy contract; copies may share cursor or resource state.
- **“Parallel iteration preserves behavior.”** Order, reductions, side effects, resource access, and floating-point results may change.
- **“Offset is a cursor.”** It identifies a position only relative to changing order and may be expensive to reach.
- **“Base64 makes a token safe.”** Encoding supplies no integrity, authorization, confidentiality, or expiry.
- **“Successful enumeration proves processing.”** Consumer effects can fail, repeat, or commit independently of traversal.

## Worked Examples

### Example 1

Two loops share one iterator over `[A,B,C]`: loop one consumes A, loop two gets B, and loop one then gets C. Creating two iterators yields two independent A-to-C traversals. **Conclusion:** The iterable/iterator distinction prevents accidental cursor sharing.

### Example 2

An empty iterator starts at rank (r=n=0); its first advance is `End`. A one-element iterator emits rank zero once and ends at rank one. **Conclusion:** Empty and singleton cases expose off-by-one errors directly.

### Example 3

Filtering `[1,2,3,4]` for even values emits 2 after consuming two source steps and 4 after two more. Per-output cost is variable though total source work is four steps. **Conclusion:** Adapter complexity must be stated relative to source advances, not only emitted elements.

### Example 4

`take(3)` over an infinite natural-number iterator yields `0,1,2` and terminates; collecting the unbounded source never terminates and grows memory. **Conclusion:** Laziness needs an explicit termination boundary.

### Example 5

A fail-fast list iterator observes version 8, then an external append advances version 9. The next call raises rather than returning a mixed view, but a concurrent undetected race is not ruled out. **Conclusion:** Fail-fast is diagnostics, not synchronization.

### Example 6

A tree iterator yields references to nodes while a rotation frees/reuses nodes. Without pinning, ownership, epoch protection, or prohibited mutation, retained references dangle. **Conclusion:** Element lifetime is part of traversal correctness.

### Example 7

A database iterator opens a cursor and the consumer stops after ten rows. Lexical cleanup closes it immediately; garbage-collection-only cleanup leaves transaction state and server resources until an unpredictable time. **Conclusion:** Early termination needs deterministic resource release.

### Example 8

Pages ordered only by nonunique timestamp end with `(12:00,id=7)` while another row has the same timestamp. Resuming with `timestamp > 12:00` omits it; ordering and seeking by `(timestamp,id)` removes the tie ambiguity under the chosen consistency model. **Conclusion:** Resumable order needs a unique tie-breaker.

### Example 9

A client changes an unsigned token from tenant A's last key to tenant B's key. Binding query, scope, key, version, and expiry under authenticated integrity makes alteration fail, while authorization is still rechecked. **Conclusion:** Continuation tokens are capabilities, not trusted offsets.

### Example 10

A spliterator divides 1,000 array elements into disjoint halves and combines integer sums associatively. Splitting a stateful network stream or order-dependent side-effecting fold cannot preserve the same contract. **Conclusion:** Parallel traversal requires a valid partition and reduction algebra.

## Cross-Program Connections

- **Object-Oriented Programming:** protocols, generics, ownership, variance, and collection abstractions shape iterator APIs.
- **Programming Languages and Semantics:** generators, coroutines, effects, laziness, and operational state machines formalize traversal.
- **Functional Programming:** folds, unfolds, lazy lists, transducers, and fusion reframe iterator composition.
- **Algorithms:** traversal category and complexity determine which algorithms are legal and efficient.
- **Data Structures Engineering:** representation invariants, invalidation, cache behavior, and concurrent structures govern implementations.
- **Database Engineering:** Volcano operators, cursors, MVCC snapshots, ordering, and keyset pagination are iterator-like protocols.
- **Distributed Systems Engineering:** continuation tokens, retries, partial failure, expiry, and consistency appear across boundaries.
- **Concurrency and Parallelism:** borrowing, synchronization, weak consistency, partitioning, and associative reduction constrain use.
- **API Engineering:** pagination envelopes, token versioning, limits, and error schemas expose traversal remotely.
- **Testing and Quality:** model/property tests, fault injection, resource-leak tests, and adversarial benchmarks provide evidence.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Canonical Iterator intent, structure, applicability, and consequences.
2. Python Software Foundation, [Python Data Model: Iterator Types](https://docs.python.org/3/reference/datamodel.html#object.__iter__), Python 3.14.7, accessed 2026-08-28. Defines iterable/iterator protocol, exhaustion, and generator integration.
3. Oracle, [`java.util.Iterator`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Iterator.html), Java SE 25, accessed 2026-08-28. Defines advance, exhaustion, optional mutation, and concurrent-modification boundaries.
4. Oracle, [`java.util.Spliterator`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Spliterator.html), Java SE 25, accessed 2026-08-28. Defines sequential advance, partitioning, size estimates, and traversal characteristics.
5. Rust Project, [`std::iter`](https://doc.rust-lang.org/std/iter/), Rust 1.98.0 documentation, accessed 2026-08-28. Documents ownership forms, laziness, adapters, iterator traits, and post-panic limits.
6. Goetz Graefe, [“Volcano—An Extensible and Parallel Query Evaluation System”](https://doi.org/10.1109/69.273032), *IEEE Transactions on Knowledge and Data Engineering* 6(1), 1994. Develops iterator-style query operators and parallel execution mechanisms.
7. PostgreSQL Global Development Group, [`DECLARE` cursor documentation](https://www.postgresql.org/docs/current/sql-declare.html), PostgreSQL 18, accessed 2026-08-28. Defines database cursor lifetime, transaction, scrolling, and holdability behavior.
8. Reactive Streams, [Reactive Streams specification](https://www.reactive-streams.org/), version 1.0.4, accessed 2026-08-28. Defines asynchronous stream processing with non-blocking demand and interoperability scope.

## Exercises

### Exercise 1

Trace the executable iterator and prove its finite snapshot order, count, and exhaustion. State precisely what is not proved.

### Exercise 2

Specify laws for `map`, `filter`, `take`, and `zip` over single-pass iterators, including failure and infinite-source cases.

### Exercise 3

Design mutation and lifetime semantics for iterating over a mutable ordered map whose keys must preserve its ordering invariant.

### Exercise 4

Design a production continuation-token protocol for a multi-tenant API listing records by update time under concurrent writes.

### Exercise 5

Evaluate whether a synchronous Iterator is appropriate for a remote, unbounded event feed; propose and justify an alternative.

## Answers to the Exercises

### Answer 1

At creation the copied tuple is `(10,20,30)`, source version is zero, and rank is zero. Appending 40 mutates only the aggregate list and advances its version to one; the tuple remains unchanged. Three calls through `list` emit tuple ranks zero, one, and two as 10, 20, and 30, moving rank to three. Since tuple length is three, remaining is zero and the next protocol step is exhaustion. Induction on rank establishes fixed order and one emission per position.

This proves behavior of one finite copied tuple with a private cursor in one Python run. It does not prove thread safety, atomic snapshot acquisition, element deep immutability, large-copy feasibility, reference lifetime, exception cleanup, arbitrary adapters, remote I/O, distributed consistency, or exactly-once consumer effects.

### Answer 2

For pure total `f`, `map(f,I)` consumes one source item per emitted item, preserves source order/cardinality, propagates source failure, and ends when source ends. `filter(p,I)` preserves relative order and emits exactly source items satisfying total predicate `p`; it may consume any finite number before one emission and may never emit/end on an infinite all-false source. Predicate failure terminates with failure under the chosen result protocol.

`take(k,I)` for nonnegative `k` emits at most the first `k` source items, consumes no more than needed, ends immediately for zero, and can make an infinite source finite. `zip(I,J)` emits pairs in lockstep and ends at the shorter source; specify whether it probes left first and may consume one unmatched left item when right ends. All remain single-pass unless their sources and adapter state explicitly support independent replay. Side-effecting functions weaken algebraic rewrite laws and must not be silently duplicated.

### Answer 3

Expose immutable key/value entry views or copied entries; never yield a mutable key reference because changing it could violate tree order. Give each iterator a captured structural version and private traversal stack. Permit value replacement through a controlled map operation only if it leaves key order/structure intact; either allow it with defined value visibility or count it as a version change. Structural insertion, deletion, rekeying, or rebalancing outside iterator-mediated operations causes fail-fast at the next checked operation, or is prohibited by exclusive borrowing.

If removal through the iterator is supported, allow it once after a successful advance, update the cursor so the successor is neither skipped nor repeated, update/capture the new structural version, and define yielded-entry invalidation. Tests cover empty/root/leaf/two-child removal, duplicate-policy boundaries, forward order, external mutation, two iterators, retained references, and exception safety. For concurrency, replace fail-fast with locking, snapshot, or a specifically proven concurrent-map traversal contract.

### Answer 4

Use a total descending order `(updated_at,id)` with a unique immutable ID tie-breaker. The token contains a digest of canonical filters and order, last timestamp/ID, tenant-safe scope or server-side cursor ID, API/token schema version, page-size ceiling, consistency/snapshot identifier if promised, and expiry. Authenticate integrity and encrypt if fields are sensitive, or store opaque random handles server-side. Recheck authentication/authorization and token scope every request; reject tampering, expiry, unsupported version, query mismatch, and excessive page size.

Under read-committed keyset semantics, seek strictly after the last pair and document that concurrent updates can move records, causing omission or repetition relative to a changing dataset. If repeatable listing is required, bind a database snapshot or high-water mark with retention/expiry and specify which later writes are excluded. Bound rows, bytes, query time, token lifetime, and active snapshots. Test equal timestamps, insert/update/delete around boundaries, token replay/tamper/cross-tenant use, authorization revocation, expiry, schema migration, empty/final pages, retries, and database plan cost.

### Answer 5

A synchronous `next` is misleading if it can block indefinitely, has no item yet rather than true end, reconnects, buffers without bound, or needs asynchronous cancellation. End, temporary absence, failure, timeout, and cancellation cannot be represented honestly by a simple finite collection protocol. A resource-owning synchronous iterator can work for a bounded blocking stream with explicit deadlines/close, but not as the default abstraction for an unbounded remote feed.

Prefer an asynchronous iterator returning awaited item/end/error with cancellation and timeout, or a demand-aware reactive stream when producer and consumer rates differ materially. Specify subscription identity, requested capacity, bounded buffering, ordering/partition keys, heartbeat/idle behavior, delivery/acknowledgment semantics, retry/resume cursor, duplicate policy, terminal error/completion, authorization refresh, and cleanup. Load/fault tests must cover slow consumers, disconnects, cancellation races, redelivery, cursor expiry, partition reorder, backpressure, memory bounds, and server resource release; traversal success still does not prove consumer-effect delivery exactly once.
