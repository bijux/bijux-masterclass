---
module_id: CONPAR-024
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 24
title: Visibility and Publication
status: complete
last_verified: 2026-08-29
---

# Visibility and Publication

## One-Page Review

### Governing question

How does a producer make a fully initialized value—and the complete reachable state it promises—safely observable to another thread without exposing partial construction, stale generations, later races, or invalid lifetime?

### Essential definitions

- **visibility** is the source model's guarantee that a read may or must observe writes ordered before it.
- **publication** transfers a reference/value into a location or operation another thread can observe.
- **safe publication** combines complete construction, a specified synchronization path, correct matching, and valid lifetime.
- **escape** occurs when a reference becomes reachable outside its intended confinement boundary.
- **construction confinement** keeps an object private until initialization is complete.
- An **immutable object** has no logically mutable reachable state after publication.
- A **publication carrier** is the lock, atomic state, channel, start, join, future, or once-initializer carrying visibility.
- A **generation** distinguishes one publication epoch from earlier values or recycled identities.
- **snapshot publication** installs a new immutable version rather than mutating a shared version in place.
- **reclamation** decides when an old published object can no longer be accessed.

### Central model, mechanism, or theorem

For object graph G and publication token T:

(initialize(G) ->sb publish_release(T) ->sw observe_acquire(T,g) ->sb read(G)).

The proof requires initialization before publication, the consumer observing the intended generation g, no unsynchronized mutation of G during use, and lifetime extending through the last read. A safely published reference does not make later mutation safe. A carrier publishes only state connected before its release side; writes after publication require another protocol.

### Critical invariants

The reference does not escape during construction. Every promised reachable field is initialized before publication. The publication carrier has a documented source-language edge. Consumer use follows the matching observation, including generation/version checks. Mutable state is protected separately or excluded by immutability. The same object is not recycled while readers may retain it. Failed initialization publishes no success token. Once initialization defines retry/poison/panic semantics. Replacement preserves old/new snapshot integrity. In-process visibility is not file durability, network delivery, device coherence, or business-effect commitment.

### Common failures

Teams start a thread or register a callback from a constructor; assign a new object to a plain global; release-publish before nested objects finish; acquire an unrelated or old generation; treat `final`, `const`, or `readonly` as universal deep immutability; mutate collections after publishing an immutable wrapper; reuse an address and confuse generations; double-check a singleton with plain accesses; let failed initialization appear complete; reclaim a snapshot while readers hold it; or claim a visible file rename is durable storage.

### Compact example

A producer constructs configuration C, validates every field, then sends ownership through a channel. A worker receives C before reading it. The channel specification supplies publication and C remains immutable. If the producer retains an alias and later mutates C, safe initial publication no longer protects the later conflict.

### Connections

[Happens-Before Relations](023-happens-before-relations.md) supplies the visibility path; [Creating and Joining Threads](011-creating-and-joining-threads.md) supplies start/join publication; [Message Passing and Ownership Transfer](009-message-passing-and-ownership-transfer.md) supplies channel handoff. The [program roadmap](../ROADMAP.md) next develops atomic read-modify-write and compare-and-swap protocols.

## Governing Question

What complete proof allows a consumer to treat a value as initialized, current for the intended generation, stable during use, and alive for the required lifetime?

Publication is not one store instruction. It is a protocol spanning construction, escape control, synchronization, version selection, post-publication mutation, and reclamation.

## Why This Matters

Many concurrency bugs occur before or after the synchronization event programmers focus on. A release store cannot publish fields written afterward. A mutex cannot protect a reference leaked from a constructor before the mutex exists. A channel can transfer a reference while an undisclosed alias continues mutating its contents. An atomic pointer can be visible while its old target is already freed.

Correct publication supports configuration snapshots, caches, routing tables, worker inputs, service registries, read-mostly indexes, singleton initialization, and result delivery. Immutable published graphs are especially powerful: readers require no per-field locking because all mutation finishes before the edge.

The same word “visibility” is used in storage and distributed systems, where it means different things. A renamed file may be visible to another process but not durable after power loss. A message accepted by a local queue may not have reached a broker. Precise boundaries prevent an in-process memory proof from becoming an unsupported end-to-end claim.

## Prerequisites and Retrieval

Retrieve:

- ownership and aliasing from [Message Passing and Ownership Transfer](009-message-passing-and-ownership-transfer.md);
- start/join edges and constructor hazards from [Creating and Joining Threads](011-creating-and-joining-threads.md);
- mutex publication from [Mutexes and Mutual Exclusion](012-mutexes-and-mutual-exclusion.md);
- condition predicates from [Condition Variables and Predicate Waiting](013-condition-variables-and-predicate-waiting.md);
- component lifetime from [Designing a Correct Multithreaded Component](020-designing-a-correct-multithreaded-component.md);
- reordering from [Compiler and Processor Reordering](021-compiler-and-processor-reordering.md); and
- partial-order proofs from [Happens-Before Relations](023-happens-before-relations.md).

Retrieval prompt: draw object construction, nested-field initialization, release publication, matching acquire, and consumer reads. Then move one nested-field write after release and state exactly which claim fails.

## Learning Objectives

After completing this module, a learner can:

1. distinguish reachability, visibility, publication, safe publication, and durability;
2. prevent constructor escape and partial object-graph exposure;
3. derive publication through locks, atomics, channels, start/join, futures, and once primitives;
4. audit immutable and mutable reachable state separately;
5. use generations to prevent stale publication matches;
6. specify one-time initialization failure, recursion, retry, and poisoning;
7. design immutable snapshot replacement and safe reclamation;
8. test construction/publication/use/lifetime races; and
9. identify device, persistence, distributed, and safety boundaries requiring additional evidence.

## Core Exposition

### Visibility is relational

A value is not globally “visible” as a permanent property. Ask: which write, which read, which execution relation, and which language guarantee? The same object may be safely visible to one consumer through a lock and raced by another consumer through a plain global.

Happens-before provides the usual proof shape. Producer initialization precedes a release-side operation; a consumer's matching acquire-side operation precedes use. Transitivity orders initialization before use. The consumer need not see every wall-clock-latest write—only values consistent with the model and established relations.

### Publication begins with confinement

During construction, one thread should own the object graph exclusively. Do not store `this` or an equivalent self-reference in a global registry, start owned threads, submit callbacks, invoke overridable methods that escape the reference, or register event handlers before invariants hold.

Constructor escape can expose default field values, absent dependencies, invalid indexes, or locks not yet assigned. Later synchronization does not retroactively make the earlier observation safe. Use a factory: allocate, initialize, validate, then publish after construction returns.

Partial failure also stays confined. If validation or resource acquisition fails, clean up and return failure without installing the reference or success token.

### Define the published graph

Publishing a root reference makes reachable objects relevant. If configuration points to a mutable list, map, credential, parser table, or callback, readers depend on those objects too. Freeze, copy, transfer, or protect the entire promised graph.

<!-- bijux-verify: {"id":"published-object-graph","mode":"schematic","language":"text","toolchain":"none","reason":"The diagram states reachability and aliasing obligations rather than executable behavior."} -->
```text
published root -> immutable configuration -> immutable route table
                                      \-> credential snapshot
producer alias --------------------------> mutable route table  (unsafe)
```

Shallow unmodifiable wrappers do not make elements immutable. A final pointer can refer to mutable contents. Language qualifiers such as `const` or `readonly` have exact, often shallow or alias-dependent meanings.

### Lock-based publication

Producer constructs value C privately, locks m, installs C in protected state, unlocks. Consumer locks the same m, copies or uses C according to the invariant, then unlocks. Installation is before unlock; unlock synchronizes with the later lock; lock is before use.

The lock must cover both the reference and rules for its mutable contents. Returning a mutable alias then unlocking can move later use outside protection. Copy an immutable snapshot or keep all mutation under the lock.

Lock-based publication is often the clearest choice when installation is one of several coupled state changes or when consumers also mutate the object.

### Release/acquire publication

A common narrow protocol constructs payload P and then release-stores state READY with generation g. A consumer acquire-loads state, verifies READY and g, then reads P. The acquire must observe the qualifying release under the language rules.

Publication state is a state machine, not a boolean habit. Example states might be EMPTY(g), BUILDING(g), READY(g), FAILED(g), and RETIRED(g). Only the owner of BUILDING may write P. READY publishes a complete immutable P. Failure publishes an error object or returns to EMPTY according to a specified retry policy.

A relaxed readiness load can be atomically correct yet lack payload publication. An acquire reading READY from the wrong release/generation may import a different graph. Reused integer values make write identity harder to audit; monotonically tagged generations clarify it.

### One-time initialization

Use language/library once primitives rather than home-grown double-checked locking. They coordinate one initializer and publish its completed effects to passive callers according to the specification.

Failure semantics differ. C++ `call_once` retries after an exceptional active execution until one returns successfully; its returning execution synchronizes with passive returns. Go `Once.Do` considers a panicking call returned for future invocations, and recursive Do deadlocks. Rust `Once` exposes poisoning behavior and `OnceLock` associates initialization with a value. Java class initialization and holder idioms have their own rules.

Specify:

- whether failure is cached, retried, or poisons;
- whether recursive initialization is rejected/deadlocks;
- whether cancellation can interrupt construction;
- which arguments win when callers disagree;
- whether reset/reload is supported; and
- how resources from failed attempts are cleaned.

“Exactly once” is an execution and failure contract, not merely a performance optimization.

### Thread start, join, and task completion

Initialize worker input before start; the language's start relation publishes it to the worker. Prefer moving owned values or immutable shared configuration. Starting inside a constructor can expose the owner before construction completes.

Worker results become usable through a specified completion edge: join, a future/promise result, or a result-channel receive. Writing a plain `done` flag and polling it is not equivalent. Result data must be written before the completion publication.

Thread pools need a per-task boundary. Worker creation publishes pool construction to workers, but it does not automatically publish arbitrary caller writes made long afterward. Queue submission/dequeue or executor contracts must carry each task and its input.

### Channel and ownership-transfer publication

Send/receive can transfer a value and create a visibility edge. This is strongest when the sender gives up mutable aliases. The receiver becomes the sole mutable owner or treats the value as immutable.

If several receivers share a pointer, channel delivery publishes initial state but does not serialize later mutation. Add internal synchronization or retain immutable snapshots. Queue close publishes only what the channel specification says; it is not a universal barrier over all producer state.

Bound the channel and payload bytes. Safe publication does not prevent memory exhaustion or blocked-producer deadlock.

### Immutable snapshots

For read-mostly data:

1. load current snapshot through its publication protocol;
2. construct the next graph privately;
3. validate all invariants;
4. atomically install/publish the new root;
5. let existing readers finish on the old immutable graph; and
6. reclaim only when no reader can retain it.

Readers see an internally coherent version, though different readers may see different generations. If an operation needs several roots to agree, publish one aggregate root or use a version-validation protocol.

Copy-on-write simplifies read synchronization but costs allocation, copying, cache pressure, and reclamation. Structural sharing is safe only when shared subgraphs remain immutable.

### Mutable after publication

Initial safe publication freezes only the construction-to-first-use relationship. Later writes need their own lock, atomic protocol, ownership transfer, or replacement publication.

Consider C with immutable field name and mutable counter. A release-published pointer makes initial name/counter values visible, but concurrent plain counter increments still race. Separate the immutable core from synchronized mutable state and document both contracts.

Do not mutate a collection “because everyone already saw it.” Publication is not permanent coherence for unsynchronized updates.

### Generation and identity safety

Suppose address p once referenced generation 7, is reclaimed, and later stores generation 8. A delayed consumer that retained p or READY=true may mistake the new object for the old obligation. This resembles the ABA problem.

Use generation-tagged handles, stable identities, leases, epochs, or nonreuse until quiescence. Validate generation after acquiring publication and before side effects. A generation tag reduces ambiguity but must not wrap within the retained-observer horizon without a proof.

Reloadable singleton designs must decide whether existing readers may continue with old snapshots, whether updates are linearizable, and how callbacks/results are attributed to a generation.

### Lifetime and reclamation

Visibility without lifetime is unsafe. A consumer can correctly acquire a pointer and then dereference freed memory. Garbage-collected runtimes preserve memory lifetime while references remain reachable but not necessarily resource lifetime or logical freshness.

Manual-memory systems need ownership, reference counting, epochs, hazard pointers, read-copy-update, locks, or another reclamation proof. Publish, acquire, use, announce quiescence, retire, and reclaim are distinct transitions.

Reference counting itself must be acquired before the target can disappear; incrementing through an already-dangling pointer is not a repair. Reclamation protocols appear later in the course.

### Java final-field semantics

Java SE 26 gives correctly constructed `final` fields special visibility semantics when the object does not escape during construction. Correct use supports immutable objects even when a reference is passed through a data race; referenced objects/arrays receive carefully defined guarantees.

This is language-specific and not permission to publish arbitrary mutable non-final state racy. The JLS example distinguishes guaranteed final field x from potentially default-valued non-final y. Reflection/special modification and constructor escape complicate the rules. Prefer normal safe publication even for immutable objects unless relying on final semantics deliberately and narrowly.

Do not transfer Java `final` guarantees to C++ `const` or Rust immutability vocabulary.

### Failed and partial publication

Never publish READY before validation, checksums, indexes, callbacks, and owned resources needed by the contract are complete. If construction fails, publish a stable FAILED result with cause and generation or leave no installed object according to policy.

Readers must not interpret non-null as valid. The publication state and payload must transition atomically enough that READY identifies exactly one complete graph. Cleanup of a failed unpublished graph remains constructor-owner responsibility.

If publication succeeds but a later external registration fails, the system may need a compensating state or rollback protocol. In-memory visibility does not create a distributed transaction.

### Persistence, network, and devices

CPU publication orders memory for participating threads under a language/platform model. It does not guarantee:

- buffered file data reached stable storage;
- rename metadata survives a crash;
- a broker durably accepted a message;
- a remote consumer observed it;
- a DMA device sees cacheable memory;
- an MMIO doorbell is ordered after descriptors; or
- a business effect committed exactly once.

Each boundary needs its own operation, acknowledgement, durability, cache-maintenance, or reconciliation contract. Use different terms: memory-published, process-visible, filesystem-installed, synchronized/durable, broker-accepted, remotely acknowledged.

### Verification

Force constructor escape, early READY, old generation, acquire of initial state, failed initializer, recursive once, cancellation during build, mutable alias, simultaneous reload, reader-retire race, result-before-completion, and shutdown during publication.

Use race detectors for executed conflicts, model checking for publication states and read-from choices, sanitizers for lifetime defects, fault injection for failed construction, and stress for operational behavior. Inspect optimized mappings for low-level atomics.

Assertions should bind root identity, generation, validation status, source publication event, reader lifetime, and terminal/reclamation state. No single tool proves the complete protocol.

## Definitions and Notation

Let object graph G_g have generation g. Construction actions C_g initialize every promised node. Publication action P_g installs the root/token; observation A_g is the matching acquire; use U_g reads the graph; retirement T_g forbids new acquisition; reclamation F_g ends lifetime.

Safe use requires:

(C_g ->hb P_g ->hb A_g ->hb U_g),

no unsynchronized mutation conflicting with U_g, and:

(U_g completes before F_g).

If a reader may span retirement, its ownership/epoch protects G_g until release. Publication status S_g belongs to a state machine such as EMPTY, BUILDING, READY, FAILED, RETIRED, RECLAIMED.

Deep immutability means no reachable state observable through the published contract changes after P_g. Shallow immutability constrains only the root/field binding.

## Mechanisms, Invariants, or Proof Structure

Use this proof:

1. **Define the graph.** List root, reachable mutable nodes, resources, callbacks, and aliases.
2. **Confine construction.** Prove no escape before all invariants and validation hold.
3. **Choose a carrier.** Same mutex, release/acquire token, channel, start, future, join, or once.
4. **Prove matching.** Record source write/operation and generation observed.
5. **Constrain later mutation.** Immutable, locked, atomic, owned, or replaced snapshot.
6. **Specify failure.** No false READY; retry, poison, cached error, and cleanup are explicit.
7. **Protect lifetime.** Acquire ownership before retirement/reclamation can win.
8. **Test negative schedules.** Early escape, old generation, failure, reload, and reclamation.
9. **Separate external visibility.** Storage, network, device, and business effects get new contracts.
10. **Reconcile.** Every generation becomes READY/FAILED, then safely RETIRED/RECLAIMED.

The executable evidence classifies eight publication routes against construction, synchronization, generation, stability, and lifetime requirements.

<!-- bijux-verify: {"id":"publication-route-classification","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"publication_routes=8\nsafe_routes=5\nunsafe_routes=3\nmissing_construction=1\nmissing_sync_edge=1\nwrong_generation=1\n","stderr":""}} -->
```python
routes = (
    ("constructor_escape", False, True, True, True, True),
    ("plain_global", True, False, True, True, True),
    ("wrong_generation", True, True, False, True, True),
    ("mutex_handoff", True, True, True, True, True),
    ("release_acquire", True, True, True, True, True),
    ("channel_transfer", True, True, True, True, True),
    ("once_initialization", True, True, True, True, True),
    ("join_result", True, True, True, True, True),
)
safe_routes = 0
missing_construction = 0
missing_sync_edge = 0
wrong_generation = 0

for route in routes:
    _, constructed, synchronized, generation, stable, lifetime = route
    safe = constructed and synchronized and generation and stable and lifetime
    if safe:
        safe_routes += 1
    if not constructed:
        missing_construction += 1
    if not synchronized:
        missing_sync_edge += 1
    if not generation:
        wrong_generation += 1

print(f"publication_routes={len(routes)}")
print(f"safe_routes={safe_routes}")
print(f"unsafe_routes={len(routes) - safe_routes}")
print(f"missing_construction={missing_construction}")
print(f"missing_sync_edge={missing_sync_edge}")
print(f"wrong_generation={wrong_generation}")
```

Limitations: the table is a deterministic classification of eight stipulated abstract routes. It assumes stability and lifetime for all listed routes, does not execute threads or model read-from choices, aliasing, failure timing, compiler/hardware behavior, or reclamation, and cannot prove a real publication implementation safe.

## Alternatives and Trade-Offs

**Mutex installation** is explicit and composes with coupled state, but readers contend and must not leak mutable aliases.

**Release/acquire root publication** supports fast read-mostly paths, with generation, immutability, and reclamation proof burden.

**Channels** combine visibility and ownership transfer, while adding capacity, scheduling, close, and backpressure behavior.

**One-time initialization** is ideal for permanent values, but failure, recursion, and reset semantics vary.

**Thread start/join and futures** give clear scoped input/result boundaries, but do not handle arbitrary mid-lifecycle replacement.

**Copy-on-write snapshots** isolate readers from mutation at allocation and reclamation cost.

**Read-copy-update, epochs, and hazard pointers** support scalable replacement in manual-memory systems with substantial lifetime complexity.

**Always-lock mutable objects** trade read performance for a smaller proof and can be the better production choice.

## Failure Modes and Misconceptions

1. **A non-null reference is initialized.** Construction can escape before invariants hold.
2. **One release publishes later writes.** Only preceding connected effects travel on that edge.
3. **Any acquire sees the publication.** It must observe the qualifying release/generation.
4. **Final pointer means immutable graph.** Reachable nodes and aliases may mutate.
5. **Safe publication makes later mutation safe.** Each later conflict needs a protocol.
6. **A thread-safe collection publishes external state.** Only data covered by its specified operations is carried.
7. **Once means identical failure semantics everywhere.** Retry, panic, poison, and recursion rules differ.
8. **Double-checked locking is an optimization detail.** Incorrect outer reads can race or observe partial state.
9. **Atomic pointer solves lifetime.** Readers can acquire an address after its target is reclaimed.
10. **Address equality proves identity.** Reuse needs generations or nonreuse guarantees.
11. **Garbage collection solves resource lifetime.** Files, connections, and logical retirement remain.
12. **Immutable snapshots guarantee one current view.** Concurrent readers may legitimately hold different generations.
13. **Visible file means durable file.** Installation, synchronization, and crash survival are distinct.
14. **Race-detector silence proves publication.** Only executed instrumented conflicts are covered.
15. **Memory publication proves safety-critical delivery.** Timing, devices, networks, and hazards remain.

## Worked Examples

### Example 1

**Situation.** A constructor registers `this` in a global callback list before assigning its route table.

**Reasoning.** Callback execution can observe the reference before construction completes. Later assignment or synchronization cannot repair that earlier exposure.

**Conclusion.** Register only after a factory returns a validated complete object.

### Example 2

**Situation.** Producer installs configuration under mutex m; consumer reads it after locking m.

**Reasoning.** Construction precedes install/unlock; unlock synchronizes with later lock; lock precedes read. The graph is published.

**Conclusion.** Same-lock installation is a complete initial visibility carrier.

### Example 3

**Situation.** Consumer acquire-loads READY for generation 8 while retaining a handle for generation 7.

**Reasoning.** The acquire may publish G8, not resurrect G7. Using the G7 handle is invalid unless its lifetime remains protected and identity matches.

**Conclusion.** Publication tokens and handles must agree on generation.

### Example 4

**Situation.** Root is immutable but points to a list the producer later edits.

**Reasoning.** Safe publication covers initial list contents. The retained producer alias creates unsynchronized later mutation against readers.

**Conclusion.** Deep-freeze/copy the list or synchronize its later access.

### Example 5

**Situation.** Several threads call C++ `call_once`; the first initializer throws.

**Reasoning.** That active call is exceptional; another active attempt can run. Only a returning execution publishes to passive calls according to the specified ordering.

**Conclusion.** “Attempted once” and “successfully initialized once” are different contracts.

### Example 6

**Situation.** Main builds immutable input, starts a worker, joins it, then reads the result.

**Reasoning.** Start publishes input to worker; worker writes result before termination; successful join publishes completion to main.

**Conclusion.** Start and join form two directional publication boundaries.

### Example 7

**Situation.** A channel sends a mutable map, but sender edits it after send.

**Reasoning.** Send/receive publishes initial state, but retained alias mutation can race with receiver. Transfer ownership or send an immutable copy.

**Conclusion.** Visibility and exclusive ownership must agree.

### Example 8

**Situation.** An atomic root swaps from snapshot G1 to G2 while a reader uses G1.

**Reasoning.** Replacement can be valid, but G1 cannot be reclaimed until that reader releases its reference/epoch/hazard. Root atomicity alone is insufficient.

**Conclusion.** Snapshot publication requires a reclamation protocol.

### Example 9

**Situation.** A configuration file is atomically renamed and another process sees it.

**Reasoning.** Namespace visibility can be established, while crash durability may still require file and directory synchronization under platform rules.

**Conclusion.** State “installed/visible” separately from “durable after crash.”

### Example 10

**Situation.** A medical device publishes commands safely between CPU threads and claims actuator safety.

**Reasoning.** The memory edge does not establish DMA/MMIO order, device acceptance, physical response, worst-case timing, hazard mitigation, security, or regulatory compliance.

**Conclusion.** Named clinical, controls, driver, hardware, real-time, security, regulatory, and functional-safety reviewers need target evidence; this chapter grants no approval.

## Cross-Program Connections

- **Programming languages:** construction, final/const semantics, atomics, and once primitives define publication guarantees.
- **Data structures:** persistent/immutable graphs and copy-on-write snapshots reduce synchronization.
- **Operating systems:** start, join, MMIO, DMA, and filesystem synchronization cross visibility domains.
- **Databases:** commit visibility, snapshot versions, and durability distinguish related but different contracts.
- **Distributed systems:** publication becomes delivery, acknowledgement, replication, and reconciliation.
- **Security:** partial initialization and stale generations can expose invalid authorization state.
- **Software engineering:** factories, immutable APIs, generations, and ownership make the proof reviewable.

## References

1. Brian Goetz et al. *Java Concurrency in Practice*. Addison-Wesley, 2006.
2. Jeremy Manson, William Pugh, and Sarita V. Adve. “The Java Memory Model.” POPL, 2005.
3. Hans-J. Boehm and Sarita V. Adve. “Foundations of the C++ Concurrency Memory Model.” PLDI, 2008.
4. Maurice Herlihy and Nir Shavit. *The Art of Multiprocessor Programming*, revised first edition. Morgan Kaufmann, 2012.
5. Paul E. McKenney. *Is Parallel Programming Hard, And, If So, What Can You Do About It?* 2023 edition.
6. Oracle. *Java Language Specification, Java SE 26*, Sections 17.4–17.5, 2026. Accessed 2026-08-29.
7. ISO C++ working draft. “`call_once` and order and consistency.” Current draft accessed 2026-08-29.
8. Rust Project. “`Once`, `OnceLock`, `Arc`, and atomic Ordering, Rust 1.98.0.” 2026. Accessed 2026-08-29.
9. The Go Authors. “The Go Memory Model” and “Package sync.” Accessed 2026-08-29.
10. IEEE and The Open Group. *POSIX.1-2024, Memory Synchronization and File Operations*, 2024.

## Exercises

### Exercise 1

State the five requirements checked by the executable publication classification and explain why synchronization alone is insufficient.

### Exercise 2

Trace construction, release publication, matching acquire, use, retirement, and reclamation for two generations. Identify where a stale generation can fail.

### Exercise 3

Diagnose a double-checked singleton using a plain global pointer, a constructor that registers callbacks, and a mutable nested map. Give a coherent repair.

### Exercise 4

Compare mutex publication, release/acquire immutable snapshots, channels, and once initialization for reloadable service configuration. Choose a design and specify failure/reclamation semantics.

### Exercise 5

A railway gateway publishes validated schedules in memory, replaces a file, sends them to a device, and reports “committed.” Split this claim into precise boundaries, evidence, and required human review.

## Answers to the Exercises

### Answer 1

The requirements are complete construction before escape, a specified synchronization edge, matching identity/generation, stability during use, and valid lifetime through use. Synchronization can order the producer and consumer yet still publish a partially built graph, the wrong generation, a graph concurrently mutated through aliases, or an already reclaimed target.

### Answer 2

For generation 7: privately construct C7, publish P7, consumer acquire A7 matching P7, use U7, mark retired T7 to prevent new acquisitions, wait until every G7 reader releases protection, then reclaim F7. Generation 8 can be built concurrently but publishes through P8 and requires A8.

A stale consumer fails if it retains token 7 but acquires root 8, if address reuse makes G8 appear identical to G7, if it begins acquisition after T7, or if F7 occurs before U7 completes. Tags plus an ownership/epoch/refcount protocol must arbitrate these cases; tags alone do not extend lifetime.

### Answer 3

The plain outer pointer read races or lacks publication; callback registration escapes the object during construction; and the nested map remains mutable after the pointer appears.

Use a language once/value primitive or lock for singleton initialization. A factory constructs and validates the object without external registration, deep-freezes or privately owns the map, then the once/lock publishes success. Register callbacks only after the object is complete, with callback lifetime accounted. If reload is needed, replace the singleton model with generation-tagged immutable snapshots and safe reclamation. Cache initializer failure or retry according to an explicit policy.

### Answer 4

Mutex publication supports reload and coupled mutable metadata with the smallest proof, but every read contends. Release/acquire root swapping gives cheap reads over immutable snapshots but needs generation and reclamation. Channels are strong for single-owner configuration consumers but broadcasting and late joiners need design. Once is appropriate only for no-reload permanent configuration.

Choose release/acquire aggregate immutable snapshots when reads dominate and reload is required. Construct/validate privately, publish one generation-tagged root, cache/reject failed builds without replacing the last valid root, let active readers retain reference/epoch protection, retire old generations, and reclaim after quiescence. Serialize publishers or use compare-and-swap to prevent lost reloads. Operationally bound snapshot size, reload frequency, and retained generations.

### Answer 5

Split “committed” into: CPU-memory published generation; file namespace installed; file data and directory metadata synchronized for the stated crash model; device descriptor visible under DMA/cache/MMIO rules; device acceptance acknowledged; schedule activated physically; and system outcome reconciled. A failure can occur between every boundary, so each needs identity, generation, retry/idempotency, timeout, rollback or outcome-unknown behavior, and evidence.

Verify language hb and reclamation; file fault injection and crash tests; exact platform flush/barrier rules; hardware-in-the-loop device faults and timing; network/driver acknowledgements; security authorization; and final reconciliation. Named railway-domain, driver, hardware, filesystem, real-time, cybersecurity, regulatory, and functional-safety reviewers must approve the system-specific claims. This answer does not establish deployment fitness.
