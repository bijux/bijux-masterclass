---
module_id: DSE-008
program: Data Structures Engineering
level: 1
module_number: 8
title: Iterators and Traversal Protocols
status: complete
last_verified: 2026-08-29
---

# Iterators and Traversal Protocols

## One-Page Review

### Governing question

How can a data structure expose ordered, lazy traversal while specifying state, ownership, mutation, exhaustion, errors, resource cleanup, and parallel partitioning precisely enough for safe composition?

### Essential definitions

- An **iterable/range** can produce traversal state; an **iterator/cursor** holds a position and produces successive items.
- An **external iterator** is advanced by the consumer; an **internal iterator** invokes consumer behavior while the producer controls traversal.
- A **single-pass** traversal may be consumed only once and copies can share progress; a **multipass** traversal supports independent repeated passes under stated equality rules.
- A **bidirectional iterator** can move forward and backward; **random-access** adds offset/difference operations; **contiguous** traversal exposes adjacent element storage under a language contract.
- A **lazy adapter** defers transformation, filtering, or flattening until a consumer requests items.
- **exhaustion** is the terminal state in which no further item is available; it must be distinguishable from yielding a valid sentinel-like value.
- **invalidation** makes traversal state or yielded references unusable after an operation or source change.
- A **snapshot iterator** traverses a fixed source view; a **live** or **weakly consistent** iterator can observe changes under documented rules.
- **early close** terminates traversal before exhaustion and releases or transfers owned resources according to protocol.
- A **spliterator/partitionable traversal** can divide remaining work while reporting order, size, and safety characteristics.

### Central model, mechanism, or theorem

Model iterator state as

\[
I=(source\_id,source\_version,position,mode,status,resources).
\]

Advancement is a transition

\[
next:I\to Yield(value,I')\mid Done(I')\mid Error(error,I').
\]

For finite sequence (S=\langle s_0,\ldots,s_{n-1}\rangle), a correct snapshot traversal yields each (s_i) exactly once in promised order, then remains terminal if fused exhaustion is promised. A fail-fast live iterator additionally checks an expected modification version before each access; detecting mismatch is a diagnostic policy, not synchronization or a proof that every mutation is detected.

### Critical invariants

- Iterable identity and iterator identity are distinct unless the protocol explicitly makes an iterator self-iterable.
- Traversal order, multiplicity, filtering, and duplicate/cycle policy are part of the abstract contract.
- End-of-traversal is represented separately from any admissible element value.
- Position advances monotonically according to the selected traversal and never yields an element twice unless promised.
- Item ownership is explicit: value, shared borrow/reference, mutable borrow, handle, or proxy.
- Source mutation behavior is explicit: forbidden, invalidating, fail-fast, snapshot, live, or weakly consistent.
- Every yielded reference/view has a lifetime and invalidation relation to source and iterator.
- Lazy adapters preserve or deliberately change order, pass category, size knowledge, errors, side effects, and cleanup.
- Early termination releases iterator-owned external resources deterministically where the protocol promises it.
- Parallel splitting preserves coverage, nonoverlap where required, ordering constraints, and safe element access.

### Common failures

Common failures are returning the same exhausted iterator from a supposedly reusable collection; using a sentinel element as EOF; claiming multipass behavior for a stream; storing references across mutation; calling fail-fast iteration thread-safe; letting a filter predicate mutate its source; hiding I/O errors as ordinary exhaustion; leaking files on early break; assuming lazy means no allocation or low retention; exposing unspecified hash order as stable output; splitting work with overlap or lost elements; and using exact-size hints as untrusted allocation authority.

### Compact example

A versioned array iterator captures `(source, expected_version, index)`. `next` checks the version, yields `source[index]`, and increments. Appending changes the version, so the iterator reports invalidation rather than reading a moved or shifted representation. A snapshot iterator copies or freezes the original logical sequence and remains valid. The policies have different cost and freshness; neither is universally correct.

### Connections

[DSE-003](003-operation-contracts.md) supplies invalidation and failure semantics, [DSE-005](005-contiguous-and-linked-layouts.md) supplies positions/views, [DSE-006](006-memory-locality-and-cache-behavior.md) supplies traversal-access behavior, and [DSE-007](007-genericity-and-type-constraints.md) supplies capability categories and variance. DSE-009 tests protocols and DSE-010 benchmarks them.

## Governing Question

What exactly does a consumer own and observe when it asks for “the next element,” and how does that promise survive laziness, mutation, borrowed values, exceptions, early exit, infinite sources, concurrency, and parallel execution?

Loop syntax often hides the protocol. Underneath are source identity, traversal state, a completion channel, item ownership, and possibly cleanup. If those are unspecified, concise iteration code can retain gigabytes, expose dangling references, skip or repeat data, hide failures, or leak descriptors.

## Why This Matters

Iterators decouple algorithms from representations. One `fold` can consume arrays, lists, trees, database cursors, generated values, files, and network streams. That reuse is safe only when capability and effect differences remain visible. A file cursor is single-pass and fallible; an array range may be multipass and random-access; a concurrent map iterator may be weakly consistent.

Traversal is also a correctness boundary. Order affects deterministic output, floating aggregation, user interfaces, persistence, and replicated operations. Early termination affects resource release. Mutation affects identity and lifetime. Parallel partitioning affects coverage and races. These are ADT semantics, not loop implementation trivia.

## Prerequisites and Retrieval

You should understand finite sequences, state machines, ownership/borrowing, errors, callbacks, and DSE-001 through DSE-007. Retrieve:

1. A collection's iteration order is observable if clients can compare outputs.
2. A pointer/reference into a representation can be invalidated by mutation or relocation.
3. Generic capability bounds should match operations actually used.
4. Laziness changes when work, errors, side effects, and allocation occur.
5. Concurrency safety and fail-fast diagnostics are different properties.
6. A finite test trace cannot establish all-source traversal correctness.

## Learning Objectives

After completing this module, you should be able to:

- model an iterator as a state machine with yield, done, error, and close transitions;
- distinguish iterable/range factories from one-shot iterator objects;
- specify single-pass, multipass, bidirectional, random-access, contiguous, and exact-size capabilities;
- define item ownership, borrowing, proxy, and invalidation behavior;
- compare forbidden-mutation, fail-fast, snapshot, live, and weak consistency policies;
- reason about lazy adapter order, effects, errors, retention, and short-circuiting;
- guarantee cleanup under exhaustion, early close, exceptions, and abandonment;
- specify tree/graph traversal order, cycle, duplicate, and frontier behavior;
- validate partitioned/parallel traversal coverage and safe access;
- derive model, property, fault, and concurrency tests from traversal contracts.

## Core Exposition

**Separate iterable from iterator.** A reusable collection usually provides a factory operation that creates fresh traversal state. Calling it twice yields two positions that can advance independently. A generator object, stream cursor, or database result may itself be a one-shot iterator; requesting iteration again can return itself or fail.

Do not infer repeatability from syntax. Document whether the source can be replayed, regenerated, rewound, or consumed. A supposedly reusable iterable backed by a one-shot network body must buffer, reopen under an idempotent protocol, or expose one-shot semantics honestly.

**The iterator state machine.** Initial state precedes the first item. Each successful advance returns an item and successor position. Terminal exhaustion is separate from item value: `None`, null, zero, or `undefined` may be legitimate elements. Tagged results, a `done` flag, an exception dedicated to end, or a Boolean-plus-output protocol preserve the distinction.

Errors are also separate. A file read error must not silently appear as normal EOF. A parsing iterator can yield result values per item or terminate with an error channel; choose according to whether consumers can continue. State what happens after error: terminal, retryable, partially advanced, or recoverable.

After `Done`, many protocols require or strongly expect later `next` calls to remain done (fused exhaustion). If resurrection is allowed, ordinary loops and adapter assumptions can break. Declare it rather than relying on custom behavior.

**Traversal order.** Sequence traversal usually follows index order. Sets/maps may promise insertion, sorted, hash-dependent unspecified, or another order. Tree traversals include preorder, inorder, postorder, breadth-first, and domain-specific pruning. Graph traversal additionally needs start roots, neighbor order, directedness, duplicate-visit policy, and cycle handling.

“Unspecified order” grants implementation flexibility but is still a contract: clients must not persist/golden-test it as stable. If reproducibility matters, use an ordered structure or sort a snapshot under a defined comparator. Hash randomization and resizing can change order across runs or operations.

**Single-pass and multipass.** A single-pass iterator can read a stream or mutate shared traversal state. Copying it may copy a handle to the same progress, not create an independent traversal. Algorithms must not compare positions or traverse twice unless promised.

A multipass/forward traversal supports independent copies and consistent repeated dereference under its protocol. Bidirectional adds predecessor movement. Random-access adds constant-cost offset/difference/index operations under a cost contract. Contiguous traversal further exposes address adjacency and is much stronger than random access.

Capabilities form semantic requirements, not only speed labels. An algorithm selecting the midpoint by arithmetic needs random access; one that scans needs input iteration. Requiring contiguous iteration excludes linked or generated sources unnecessarily.

**Ownership of yielded items.** An iterator can yield owned values, shared references, mutable references, handles, views, or proxy objects. Owned iteration may consume/remove elements from the source. Shared traversal normally prevents conflicting mutation for the borrow lifetime in ownership-checked languages. Mutable traversal must ensure yielded mutable references do not alias unlawfully.

A proxy can represent packed bits, decoded fields, database rows, or computed values and may not be an ordinary reference. Generic algorithms should constrain and use the documented item type rather than assume addressability or independent lifetime.

If items borrow the source, they cannot outlive the backing representation. Some streaming parsers reuse one buffer, so an item may be valid only until the next advance. That “lending iterator” relationship needs stronger lifetime expression or explicit copying; a conventional item type may be insufficient.

**Mutation policies.** One option forbids structural mutation while an iterator exists, enforced by ownership, locks, runtime guards, or documentation. Element mutation in place may still be allowed if it does not break traversal and alias rules.

Fail-fast iteration captures a modification counter and checks it. On mismatch it reports invalidation. It is best-effort bug detection unless every relevant mutation reliably updates a nonwrapping/versioned counter under synchronization. It does not make concurrent access safe and usually does not promise deterministic detection of races.

Snapshot traversal freezes logical contents at creation. It provides stable order and mutation independence but costs copying, persistence, reference retention, or version management. A shallow snapshot still shares mutable element objects.

Live traversal defines how current changes affect future yields. Weakly consistent concurrent traversal may reflect some updates, never throw concurrent-modification errors, and promise no duplicates or only bounded properties depending on API. State exact guarantees; “eventually sees changes” is usually too vague.

**Invalidation granularity.** Array growth can invalidate all references/iterators; insertion can invalidate positions at/after the point; node-based insertion may preserve existing-node iterators; removal invalidates the removed node. Compacting/reclamation can broaden rules. DSE-005 supplies representation mechanisms, but the iterator API publishes the observable contract.

End/sentinel positions also have validity rules. A past-end iterator can change meaning after append; comparing positions from different containers is often invalid. Version/source identity should be checked in safe handles.

**Lazy adapters.** `map`, `filter`, `take`, `skip`, `flat_map`, `zip`, and similar adapters wrap upstream state. Construction often performs little work; advancement pulls enough upstream items to produce the next output. This changes when callbacks execute, errors arise, and side effects occur.

Laziness can avoid materializing results and short-circuit infinite/large inputs. It can also retain the source, closures, caches, buffers, or prior items longer than expected. `tee`/memoizing repeatability may buffer an unbounded gap between consumers. Measure reachability and worst-case buffering.

Adapter laws require side-effect assumptions. `map(f).map(g)` may be equivalent to `map(g∘f)` for pure total functions, but exceptions, mutation, logging, timing, and floating behavior can distinguish execution. Optimizers must preserve the declared effect semantics.

Filtering can call the predicate multiple times only if protocol permits; ordinary iterators should specify at-most-once per examined element. If predicates mutate source, invalidate traversal, or reenter the iterator, behavior must be prohibited or explicitly supported.

**Short-circuiting.** `find`, `any`, `all`, `take`, and bounded folds can stop before exhaustion. This is a semantic/performance feature for infinite or expensive sources. It creates cleanup duties and means unvisited callbacks/effects do not occur.

Consumers should not accidentally traverse twice through length probing, logging, or retry. Size hints are estimates unless exactness is a capability. Never allocate attacker-controlled hinted size without bounds; a dishonest/malformed iterator can overstate it.

**Cleanup and early close.** An iterator over memory may own no external resource. A file/database/network iterator may own descriptor, transaction, lock, buffer, or task. Specify cleanup on normal exhaustion, early break/close, adapter error, callback exception, cancellation, and abandonment.

Language constructs such as context managers, deterministic destructors, `finally`, generator `return`, or explicit `close` help, but garbage collection/finalization timing is not generally a prompt-release guarantee. Prefer structured scopes and explicit close for scarce resources.

Closing a composed pipeline should propagate upstream once and release buffers. Close errors need precedence/aggregation rules relative to the triggering error. Idempotent close simplifies recovery, but must be promised and tested.

**Internal versus external iteration.** External iteration lets consumers pull, pause, interleave sources, and short-circuit. It exposes traversal state/lifetime. Internal iteration (`for_each(visitor)`) keeps control and invariants inside the structure, can optimize traversal, but callback effects/reentrancy and early-exit/error signaling require design.

Push-based streams deliver items when producers are ready; pull iterators deliver on demand. Async iteration adds awaiting, cancellation, backpressure, and task/resource ownership. This module establishes synchronous contracts; concurrent/async programs develop scheduling in their owning courses.

**Cursors.** A cursor can represent a location between elements and support insert/remove/navigation. Unlike a read iterator, it may hold mutation authority and update its position through edits. Text editors, linked structures, and trees use cursors to avoid repeated search. State whether other cursors remain valid.

Zippers represent a focus plus reconstruction context for immutable trees. Updates return a new structure while preserving old versions. Their traversal/order semantics still require explicit contracts.

**Tree and graph traversal state.** Depth-first traversal stores a stack proportional to depth; breadth-first stores a frontier that can grow to width. Recursive DFS also consumes call stack. A lazy traversal does not eliminate this state.

Graphs need a visited policy. “Yield vertices” can mean once per identity, once per path, or once per edge occurrence. Cycle detection requires a lawful identity/equality/hash relation and consumes space. Neighbor iteration order influences output and reproducibility.

Mutation can introduce/remove edges during traversal. Snapshot adjacency, version checks, locks, persistent graph versions, or weak policies are alternatives. Never traverse untrusted links without node/edge/step budgets and validation.

**Partitioning and parallel traversal.** A splittable traversal divides a remaining domain into subtraversals. Correctness can require union coverage equal to original remainder and pairwise nonoverlap, unless duplicates are meaningful. Encounter order may constrain merge.

Size estimates, sorted/distinct/nonnull/immutable/concurrent characteristics enable optimization only when truthful. A false exact-size claim can cause wrong indexing or unbounded allocation. Splitting cost and balance affect performance; tiny partitions create overhead, skewed partitions create idle workers.

Parallel mutable traversal must give each partition disjoint mutation authority or synchronize. Read-only element references can still observe mutable shared subobjects. Reductions require associative operations for schedule-independent regrouping; floating arithmetic and side effects can make order observable.

**Infinite and fallible sources.** Infinite iterators never exhaust, so `collect`, full sort, count, or equality can diverge or exhaust memory. APIs should expose bounded `take`, deadlines, cancellation, or consumer budgets. “Lazy” does not make an unbounded terminal operation safe.

Fallible iterators can yield `Result<Item,Error>` so consumers choose skip/retry/stop, or return an error from advancement. Partial output and source position after failure matter. Network retry can duplicate items without identity/checkpoint semantics.

**Testing protocols.** Build model traces over empty, singleton, multiple, exhaustion, repeated done, two independent iterators, partial consumption, mutation at every position, element mutation, close, exception, cancellation, infinite prefix, corrupt graph, and stale handles.

Properties include yielded sequence equality, no loss/duplication, order, exact coverage, fused completion, snapshot independence, expected invalidation, cleanup-once, adapter equivalence under pure functions, and split union/nonoverlap. Fault-inject callbacks and upstream errors. Concurrent histories need schedule exploration and memory-safety tools.

The executable example below distinguishes fail-fast live traversal from a snapshot and demonstrates stable exhaustion. It is one finite protocol trace, not a concurrency or lifetime proof.

<!-- bijux-verify: {"id":"versioned-iterator-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"first=10\nmutation=iterator invalidated\nsnapshot=(10, 20, 30)\nnew_remaining=(20, 30, 40)\nexhausted=stable\nevidence=finite_protocol_trace\n","stderr":""}} -->
```python
class VersionedSequence:
    def __init__(self, values):
        self._values = list(values)
        self._version = 0

    def append(self, value):
        self._values.append(value)
        self._version += 1

    def __iter__(self):
        return VersionedIterator(self)

    def snapshot_iterator(self):
        return iter(tuple(self._values))


class VersionedIterator:
    def __init__(self, source):
        self._source = source
        self._expected_version = source._version
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._expected_version != self._source._version:
            raise RuntimeError("iterator invalidated")
        if self._index == len(self._source._values):
            raise StopIteration
        value = self._source._values[self._index]
        self._index += 1
        return value


source = VersionedSequence((10, 20, 30))
live = iter(source)
snapshot = source.snapshot_iterator()
print(f"first={next(live)}")
source.append(40)
try:
    next(live)
except RuntimeError as error:
    print(f"mutation={error}")
print(f"snapshot={tuple(snapshot)}")
fresh = iter(source)
next(fresh)
print(f"new_remaining={tuple(fresh)}")
try:
    next(fresh)
except StopIteration:
    print("exhausted=stable")
print("evidence=finite_protocol_trace")
```

## Definitions and Notation

Let source abstract sequence be (S), iterator state space (Q), and transition

\[
\delta:Q\to Yield(E,Q)\uplus Done(Q)\uplus Error(X,Q).
\]

For snapshot iterator created at version (v), yielded trace is a prefix then all of (S_v) according to consumption. For fail-fast source with modification counter (m), `expected=m` is checked before source access; wraparound, unsynchronized races, and untracked mutations limit detection.

Single-pass means prior positions/copies need not remain independently dereferenceable. Multipass requires protocol-specific equality and that equal positions advance to equal positions/values while source validity holds. Exact-size iterator has trusted remaining count (r(q)) satisfying each yield decrements by one and done iff zero.

For split operation (split(q)=(q_1,q_2)), coverage requires (Trace(q)=merge(Trace(q_1),Trace(q_2))) under the declared encounter-order/merge relation, with nonoverlap when each source occurrence must appear once.

## Mechanisms, Invariants, or Proof Structure

**Sequence correspondence.** Induct over successful transitions: position (i) yields promised source occurrence (S[i]), increments once, and preserves valid state; terminal position yields done.

**Fused exhaustion.** Show `Done` transitions only to `Done`, with close idempotence if promised and no source access after terminal state.

**Fail-fast check.** Every tracked structural mutation changes version before publication; each advance compares expected/current before dereference. This proves detection only under counter/synchronization assumptions.

**Snapshot independence.** Snapshot owns or persistently references version (v); later source mutations cannot change its abstract yielded sequence, though shallow element aliases may still mutate.

**Adapter composition.** Relate output transitions to upstream transitions and callback results; account for skipped inputs, short-circuit, errors, and close propagation.

**Split coverage.** Prove partitions cover every remaining occurrence exactly once, maintain required order, and grant compatible element access.

**Finite evidence boundary.** The snippet covers one mutation and finite source. It does not prove thread safety, counter completeness/wraparound, borrowed lifetime, cleanup, parallel splitting, or arbitrary traces.

## Alternatives and Trade-Offs

**External versus internal iteration.** External pull offers control/interleaving; internal traversal retains invariants/optimization. Callback reentrancy and early-exit channels complicate internal forms.

**Single-pass versus multipass.** Single-pass supports streams and low state. Multipass enables repeated algorithms and independent positions, often requiring stable storage or buffering.

**Fail-fast versus snapshot versus weak consistency.** Fail-fast diagnoses mutation cheaply, snapshot guarantees stable content at copy/version cost, and weak consistency supports concurrency with fewer freshness/order guarantees.

**Owned values versus references/proxies.** Owned yields simplify lifetime and may copy/move; references avoid copying and constrain source mutation/lifetime; proxies support packed/computed storage and complicate generic assumptions.

**Lazy versus eager adapters.** Lazy pipelines short-circuit and avoid result materialization but defer effects/errors and retain state. Eager results stabilize errors/ownership at allocation cost.

**Recursive versus explicit traversal state.** Recursion is concise and uses call stack; explicit stacks/queues expose memory bounds, pausing, serialization, and iteration.

**Sequential versus split traversal.** Splitting enables parallel work but requires truthful characteristics, coverage proof, balance, safe access, and deterministic merge where needed.

## Failure Modes and Misconceptions

1. **“Iterable and iterator are the same.”** A reusable source normally creates fresh traversal state.
2. **“None/null means end.”** It may be a valid element; completion needs a separate channel.
3. **“Single-pass just means slower.”** It restricts copying, replay, equality, and algorithms.
4. **“Fail-fast means thread-safe.”** It is a mutation diagnostic, not synchronization.
5. **“Snapshot means deep copy.”** Element references can remain shared and mutable.
6. **“Lazy means no memory.”** Suspended state, buffering, closures, and sources can be retained.
7. **“Iterator chains are always faster.”** Dispatch, optimization, callbacks, allocation, and workload decide.
8. **“Early break needs no cleanup.”** Iterators may own external resources or locks.
9. **“Unspecified order is stable enough.”** Clients cannot rely on accidental order.
10. **“A size hint is trustworthy.”** Estimates or hostile sources require bounds.
11. **“Graph traversal yields each vertex once automatically.”** Identity/visited/cycle policy is required.
12. **“Splitting in half proves parallel correctness.”** Coverage, overlap, mutation, order, and merge remain.
13. **“Parallel reduce preserves sequential results.”** Nonassociativity and effects make regrouping observable.
14. **“Passing one traversal test proves the protocol.”** Mutation, errors, close, aliases, concurrency, and infinite sources remain.

## Worked Examples

### Example 1

**Question:** Why should a range create a fresh iterator each pass?

**Reasoning:** Consumers expect two loops to start independently; returning one shared cursor makes the second begin at partial/exhausted state.

**Conclusion:** Reusability belongs to iterable factory semantics.

### Example 2

**Question:** Can an iterator yield `None`?

**Reasoning:** Yes, when `None` is in the element domain; a tagged `Yield(None)` remains distinct from `Done`.

**Conclusion:** Never overload an admissible value as exhaustion without an exclusion contract.

### Example 3

**Question:** Why can two copies of an input iterator not be traversed independently?

**Reasoning:** They may share an underlying stream/cursor; advancing one consumes data for both.

**Conclusion:** Algorithms requiring multipass must constrain for it.

### Example 4

**Question:** What does fail-fast mutation detection guarantee?

**Reasoning:** Under tracked synchronized version changes, the next check rejects a mismatched iterator. Untracked changes, races, or wraparound may escape.

**Conclusion:** It localizes bugs but is not a concurrency contract.

### Example 5

**Question:** Why can a lazy filter retain large memory?

**Reasoning:** The adapter holds upstream iterator/source and predicate closure until dropped/closed, even if few results are consumed.

**Conclusion:** Laziness avoids eager output but not necessarily retention.

### Example 6

**Question:** What must happen when a file iterator loop breaks?

**Reasoning:** A structured close path releases descriptor/buffer according to protocol; relying on eventual garbage collection can exhaust resources.

**Conclusion:** Early termination is a resource transition.

### Example 7

**Question:** Why does breadth-first tree traversal use more space on a wide tree?

**Reasoning:** Its queue retains the frontier, whose width can be large; DFS retains depth-sized path/stack state.

**Conclusion:** Lazy traversal still has topology-dependent auxiliary memory.

### Example 8

**Question:** Can a parallel split duplicate work?

**Reasoning:** If partition ranges overlap or shared cursor state races, the same occurrence can appear twice; union/nonoverlap proof prevents it.

**Conclusion:** Split correctness is an abstract coverage obligation.

### Example 9

**Question:** What does the executable snapshot establish?

**Reasoning:** It retains original three integer references/values while the source appends 40, and its tuple output remains the original sequence.

**Conclusion:** This finite shallow snapshot does not prove deep immutability or concurrent safety.

### Example 10

**Question:** A lazy traversal streams medication orders. What exceeds iterator correctness?

**Reasoning:** Engineers verify ordering, duplicate identity, checkpoints, errors/retries, cancellation, cleanup, backpressure, authorization, audit, concurrency, and implementation identity. Clinical/safety reviewers validate order semantics, omission/duplication hazards, deadlines, overrides, and human workflow; security, quality, and regulatory reviewers validate their scopes. This chapter claims none.

**Conclusion:** A correct traversal protocol cannot establish clinical or deployment safety.

## Cross-Program Connections

- [Functional Programming](../../03-programming-languages-functional-programming/ROADMAP.md) develops folds, laziness, streams, fusion, and effectful traversal.
- [Object-Oriented Programming](../../02-programming-languages-object-oriented-programming/ROADMAP.md) develops protocol objects, subtyping, and collection interfaces.
- [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) owns borrowed iterators, lifetimes, unsafe traversal, and resource cleanup.
- [Concurrent & Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) owns parallel iteration, cancellation, backpressure, and memory safety.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) uses iterator capabilities and traversal costs.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) applies streaming/fallible traversal to files, records, and pipelines.

## References

1. Python Software Foundation, [Iterator Types](https://docs.python.org/3/library/stdtypes.html#iterator-types). Current iterator protocol, exhaustion, generators, and container iteration behavior.
2. Python Software Foundation, [Data model: `object.__iter__`](https://docs.python.org/3/reference/datamodel.html#object.__iter__). Iterable/iterator integration and sequence fallback.
3. Rust Project, [`std::iter::Iterator`](https://doc.rust-lang.org/std/iter/trait.Iterator.html). Current advancement, adapters, consumers, size hints, fused/exact-size/double-ended behavior.
4. Rust Project, [`std::iter::IntoIterator`](https://doc.rust-lang.org/std/iter/trait.IntoIterator.html). Conversion from values/references into traversal state.
5. ISO C++ working draft, [Iterator concepts](https://eel.is/c++draft/iterator.concepts). Input/output/forward/bidirectional/random-access/contiguous concepts.
6. ISO C++ working draft, [Iterator requirements](https://eel.is/c++draft/iterator.requirements). Traversal, sentinel, ranges, and invalidation requirements.
7. Oracle, [Java SE 25 `Iterator` API](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Iterator.html). Advancement, removal, exhaustion, and default traversal behavior.
8. Oracle, [Java SE 25 `Spliterator` API](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Spliterator.html). Partitioning, characteristics, size estimates, ordering, and parallel traversal.
9. Ecma International, [ECMAScript Iteration](https://tc39.es/ecma262/multipage/control-abstraction-objects.html#sec-iteration). Normative iterator records, results, closing, generators, and async iteration foundations.
10. Go Project, [Go Specification: `for` statements with `range`](https://go.dev/ref/spec#For_statements). Current iteration values and per-source traversal semantics.

## Exercises

### Exercise 1

Specify a reusable sequence iterable and its iterator state machine, including exhaustion, errors, two independent iterators, and item ownership.

### Exercise 2

Compare forbidden-mutation, fail-fast, snapshot, and weakly consistent traversal for a map. State guarantees, costs, concurrency limits, and appropriate uses.

### Exercise 3

Derive contracts for `map`, `filter`, `take`, and `zip`: order, calls, errors, sizes, termination, cleanup, single/multipass category, and infinite inputs.

### Exercise 4

Design and prove a spliterator over array range `[lo,hi)`, including coverage, nonoverlap, order, exact size, mutation, and parallel writes.

### Exercise 5

Prepare a verification plan for a fallible streaming iterator over durable records with checkpoint/retry. Cover duplicates, omission, corruption, resources, concurrency, hostile inputs, evidence, and human review.

## Answers to the Exercises

### Answer 1

The iterable owns immutable or version-controlled sequence `S` and each `iter()` returns fresh state `(source_id,version,index=0,open)`. `next` verifies source validity; for `index < len(S)` it returns the item under declared owned/shared-reference policy and increments once; at length it enters `done`, and later calls remain done. Source/access errors are distinct from completion and state after error is declared. Two iterators have independent indices and yield the same sequence while source contract remains valid. Yielded references cannot outlive or survive mutations beyond the source's invalidation policy.

### Answer 2

Forbidden mutation uses ownership/lock/runtime exclusion and gives stable traversal with low copying but blocks updates. Fail-fast allows changes but reports tracked version mismatch on later advance; it is diagnostic, not race safety. Snapshot fixes logical contents at creation through copying/persistence/versioning; it supports mutation independence at memory/retention cost and can shallow-share elements. Weak consistency permits concurrent traversal and defines limited observations—such as no failure and perhaps no duplicates—without a single frozen instant; freshness/order may vary. Use based on correctness needs, mutation frequency, memory, latency, and synchronization; never infer unspecified guarantees.

### Answer 3

`map(f)` preserves encounter order/cardinality, calls `f` lazily once per yielded upstream item, propagates upstream/callback errors and close. `filter(p)` preserves relative order, may consume many inputs per output, calls `p` once per examined item, and has only upper-bound size unless stronger facts exist. `take(k)` yields at most first `k`, short-circuits and closes/releases upstream according to protocol; it makes an infinite source finite for nonnegative bounded `k`. `zip` yields pairs in order until the shortest source ends and must define probing/close of remaining sources. Each adapter inherits single-pass unless stronger source/callback contracts establish multipass; error/side effects occur on consumption, and early termination cleanup propagates once.

### Answer 4

State is immutable range `[lo,hi)` over fixed source version. Exact remaining size is `hi-lo`; advance yields source at `lo` then increments. Split at `mid=lo+(hi-lo)//2` returns `[lo,mid)` and `[mid,hi)`: intervals are disjoint, ordered, and their concatenation exactly covers the original range. Recursive induction proves all source occurrences appear once. Structural mutation is prohibited or version-invalidating. Parallel read is safe under shared-read element policy; parallel writes require disjoint mutable ownership of the two ranges and no shared mutable subobjects or conflicting side effects. Small ranges stop splitting to control overhead.

### Answer 5

Define record identity, total order, checkpoint meaning, transaction/visibility, EOF versus corruption/I/O error, and whether delivery is at-most-once, at-least-once, or exactly-once under stated system assumptions. A checkpoint must advance atomically with acknowledged processing or duplicates/omissions are reconciled through idempotency/deduplication. Validate lengths/checksums/schema before allocation/use; bound records, buffers, retries, time, diagnostics, and decompression. Specify descriptor/transaction cleanup on exhaustion, close, cancellation, exception and crash; version and authenticate checkpoints. Model/fault-test truncated/corrupt/reordered/duplicate records, crash at every boundary, stale checkpoints, retry storms, concurrent consumers, backpressure and recovery; compare against a reference log and retain exact artifact/tool evidence. Domain/data owners validate record meaning and retention; systems, security, reliability, privacy, quality and any safety/regulatory reviewers approve their scopes. Finite replay tests do not prove end-to-end exactly-once or deployment fitness.
