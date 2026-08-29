---
module_id: CONPAR-027
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 27
title: Acquire and Release Ordering
status: complete
last_verified: 2026-08-29
---

# Acquire and Release Ordering

## One-Page Review

### Governing question

When does a release operation actually publish earlier effects to an acquire operation, and how can the resulting happens-before path be proved without assuming more ordering than the language guarantees?

### Essential definitions

- A **release operation** is a language-defined atomic or synchronization operation that can order earlier actions before a matching observer.
- An **acquire operation** can order actions after it following effects published by a matching release.
- **Reads-from** identifies the write whose value a read observes.
- **Synchronizes-with** is a cross-thread edge created only by rules of the language model, not by timing intuition.
- **Happens-before (hb)** is the transitive closure of sequenced-before and synchronizes-with.
- A **release sequence** is a language-specific modification-order sequence through which an acquire may synchronize with its release head.
- An **acquire-release RMW** has acquire semantics on its read side and release semantics on its write side when it succeeds.
- A **fence** orders surrounding operations under stricter pairing rules than an acquire load or release store.
- **Publication** makes initialized state safely observable; **lifetime** keeps that state valid while observed.
- **SC atomics** add a language-defined common order beyond acquire/release constraints.

### Central model, mechanism, or theorem

Producer actions `W(payload) sb→ S_release(flag=ready)` and consumer actions `L_acquire(flag)==ready sb→ R(payload)` establish `W hb→ R` only when the acquire observes the release, or a value covered by the language's release-sequence rule. Sequenced-before plus synchronizes-with plus sequenced-before forms the path. Merely executing release and acquire on the same object is insufficient.

### Critical invariants

Payload initialization precedes publication. The acquire checks the exact value/generation that denotes publication before reading payload. The reads-from source is identified. All conflicting ordinary payload accesses are hb-ordered. Reuse has a new epoch. An RMW's load and store sides use the required ordering. A failed CAS has no release side. Fences satisfy the language's pairing rules. Publication does not substitute for ownership, lifetime, bounds, or multi-object atomicity. API guarantees are checked per language and version.

### Common failures

A consumer reads payload after an acquire that observed the old flag; publication uses one atomic but consumption checks another; the release occurs before initialization; a relaxed RMW breaks a release sequence; release is assigned to a pure load or acquire to a pure store; a failed CAS is assumed to publish; a fence is treated as a global flush; a flag is reused without generation; a pointer is published safely but freed too early; or x86 success is mistaken for source-language proof.

### Compact example

Producer writes `payload=42` then release-stores `ready=1`. Consumer acquire-loads `ready`, observes that store's one, then reads payload. The hb path is `W(payload) sb→ S_release sw→ L_acquire sb→ R(payload)`, so the ordinary accesses are ordered. If the load observes zero, no such edge exists and payload must not be read.

### Connections

[Happens-Before Relations](023-happens-before-relations.md) defines hb; [Visibility and Publication](024-visibility-and-publication.md) provides the lifecycle context; [Compare-and-Swap Loops](026-compare-and-swap-loops.md) separates successful and failed CAS ordering. The [program roadmap](../ROADMAP.md) next examines relaxed atomics.

## Governing Question

How should engineers derive the weakest sufficient acquire/release protocol from an ownership or publication invariant, prove its reads-from-dependent hb path, and recognize when fences, release sequences, object reuse, or cross-language APIs invalidate an attractive shortcut?

Acquire/release is not “make memory visible.” It is a conditional relation in an abstract memory model.

## Why This Matters

Acquire and release ordering supports safe immutable publication, queue slots, reference-count transitions, once initialization, handoff state machines, lock implementations, work descriptors, and nonblocking data structures. It can avoid the global constraints of sequential consistency while preserving the causal order a protocol needs.

The optimization opportunity brings proof risk. A release store does nothing for a consumer that reads an older value. An acquire load does not bless every earlier write by every thread. Two different atomic variables do not automatically pair. A fence is not a broadcast. An RMW can have different ordering on its read and write halves. A current language may not even expose C++-style per-operation orderings.

Correctness therefore comes from a graph: identify the producer actions, publication operation, reads-from edge, consumer observation, and protected accesses. If that graph is unclear, use a higher-level primitive with a documented memory-consistency contract.

## Prerequisites and Retrieval

Retrieve:

- compiler/processor transformation boundaries from [Compiler and Processor Reordering](021-compiler-and-processor-reordering.md);
- SC executions from [Sequential Consistency in Shared Memory](022-sequential-consistency-in-shared-memory.md);
- sb, sw, and hb from [Happens-Before Relations](023-happens-before-relations.md);
- construction/lifetime phases from [Visibility and Publication](024-visibility-and-publication.md);
- RMW read/write roles from [Atomic Read-Modify-Write Operations](025-atomic-read-modify-write-operations.md); and
- success/failure paths from [Compare-and-Swap Loops](026-compare-and-swap-loops.md).

Retrieval prompt: draw the smallest graph that lets one ordinary write be read safely by another thread. Label the two same-thread edges, the cross-thread edge, and the observation that creates it.

## Learning Objectives

After completing this module, a learner can:

1. distinguish ordering, atomicity, visibility, coherence, and lifetime;
2. construct a release/acquire synchronizes-with path from reads-from;
3. prove ordinary payload accesses are ordered by hb;
4. diagnose old-value, wrong-object, early-publication, and reuse failures;
5. derive ordering for loads, stores, RMWs, and failed CAS operations;
6. explain release sequences without overgeneralizing across language versions;
7. use fences only with a proven language-defined pairing;
8. compare C++, Rust, Java, and Go ordering interfaces; and
9. select a mutex, channel, once cell, or immutable message when lower-level ordering is unjustified.

## Core Exposition

### Start from the protected fact

Do not start by choosing `Acquire` or `Release`. State the fact that must cross threads:

> After a consumer observes slot generation g as READY, it may read the fully initialized payload for generation g.

This statement identifies payload, generation, publication state, and consumer condition. Translate it into events:

- `W`: producer's ordinary payload writes;
- `S`: release publication of READY,g;
- `L`: acquire observation of READY,g;
- `R`: consumer's ordinary payload reads.

The target proof is `W hb→ R`. If `W sb→ S`, `S sw→ L`, and `L sb→ R`, transitivity supplies it. Each edge has a separate justification.

### Release and acquire are directional

A release operation constrains relevant earlier operations relative to publication. It does not generally constrain later operations as an acquire would. An acquire operation constrains relevant later operations relative to consumption. It does not publish earlier work as a release would.

For a pure load, release ordering has no write side to publish. For a pure store, acquire ordering has no read result to consume. Language APIs therefore restrict meaningful orderings. An RMW has both sides: acquire on its load portion, release on its store portion, and acquire-release for both roles.

These are source-model guarantees. Compilers and processors implement them with instruction selection, dependencies, barriers, or no additional instruction on a strong target. The absence of a visible fence in assembly does not mean absence of source ordering.

### Reads-from is decisive

Same atomic object is not enough. Suppose producer release-stores `ready=1` but consumer acquire-loads zero from initialization. The acquire did not observe the publication and supplies no sw edge from it. The consumer must branch away without reading payload.

Suppose two producers publish generations one and two. A consumer that observes generation one receives only the causal history guaranteed through that observation; it cannot assume generation two's payload is ready.

Record the value and generation in tests and traces. “The load happened later in wall-clock time” is not a memory-model proof.

### The message-passing derivation

Initial state is `ready=0`. Producer:

1. writes all payload fields using ordinary accesses;
2. completes validation;
3. release-stores `ready=1`.

Consumer:

1. acquire-loads ready;
2. reads payload only if the result is one;
3. otherwise waits, retries, or returns absent.

When the load reads the release store's one, the source model creates sw. Together with sb, all producer payload writes happen-before all protected consumer payload reads. Those ordinary accesses are not concurrent data races under the stated one-writer/immutable-payload design.

Acquire does not create a snapshot of unrelated future writes. If the producer mutates payload again after release without another protocol, those mutations are not ordered by this publication.

### Modification order and coherence

Atomic modifications of one object participate in a per-object modification order. The consumer's observation must be consistent with the language's coherence rules, but coherence is not publication of other locations by itself.

Release/acquire uses an atomic object as a carrier for an hb edge. The carrier's value often needs an epoch or state transition so the consumer knows which payload version the edge protects. A boolean can safely publish a one-time immutable object; it is usually insufficient for repeated slot reuse.

Do not infer a coherent multi-object snapshot from acquiring one carrier. If a producer updates two independent versioned roots, a consumer can legitimately observe different generations unless a combined root, lock, validation protocol, or snapshot mechanism relates them.

### Release sequences

In C++ terminology, an acquire operation can synchronize with a release operation when it takes its value from a side effect in the release sequence headed by that release. The precise membership rules are standard-version-specific. Current definitions must be read rather than recalled from older summaries.

The durable idea is causal relay through one atomic modification order. For example, a release publication may be followed by an RMW that carries the state forward; an acquire that reads the covered value can inherit the head's prior effects under the applicable rule.

Do not assume an arbitrary relaxed store by another thread preserves the relay. Do not port the phrase “release sequence” into a language whose model specifies atomics differently. Draw every modification and identify the current normative rule.

### RMW split semantics

An RMW both observes an old value and publishes a new one. Consider a work-state CAS that consumes a published descriptor and installs CLAIMED:

- acquire on success can make descriptor initialization available to the winner;
- release on success can publish the winner's earlier state to later observers;
- acquire-release covers both when both are needed.

In Rust, documentation notes that acquire ordering on a read-modify-write makes its store side relaxed, while release makes its load side relaxed. Similar conceptual separation applies in C++.

Failure performs only a load. It cannot release. Its ordering is relaxed if the witness is merely a retry candidate, or acquire if the failure result itself publishes data the caller reads. The success/failure combination must satisfy exact API constraints.

### Locks are acquire/release protocols with more contract

A mutex unlock typically performs a release-like handoff; a later successful lock performs an acquire-like observation under the primitive's documented contract. The mutex also provides exclusion, ownership, queueing/parking behavior, and a place to maintain compound invariants.

Reimplementing a lock with atomics requires more than setting a flag. It needs mutual-exclusion proof, acquire on successful entry, release on exit, contention management, ownership policy, wakeup correctness, target support, and failure handling.

Higher-level primitives expose semantic edges directly. A channel send/receive, once cell, thread join, future completion, or queue enqueue/dequeue may better express the event being transferred.

### Fences are relational, not global

An acquire fence or release fence has no value of its own. It participates in synchronization only through language-defined relationships with atomic operations and reads-from/modification-order facts. Placing a fence “near” ordinary accesses does not make them safe.

A common transformation is a relaxed load that observes a publication value followed by an acquire fence, but it is correct only if the model's fence rule connects the observed release to that fence and protected reads occur after it. Similarly, a release fence before an atomic store needs the corresponding normative rule.

Fences are harder to review because the value observation and ordering operation are split. Prefer an acquire load or release store unless measurement and a precise proof justify separation.

### Transitivity and relay

Happens-before composes. Thread A initializes payload and releases state. Thread B acquires it, computes derived state, then releases another carrier. Thread C acquires the second carrier. If each reads-from/synchronization edge is valid, A's initialization can happen-before C's consumption.

This relay is not automatic because B executed acquire and release. B must acquire the published value before using it, sequence its derived writes before its release, and C must observe that release. A missing condition breaks the chain.

Transitivity is useful for pipelines and work queues. It also makes proof graphs scale better than hardware narratives: reason about documented edges at each boundary.

### Initialization and repeated reuse

One-time publication is the simplest case:

`UNINITIALIZED → READY`, with immutable payload thereafter.

Repeated slots require a generation:

`EMPTY,g → WRITING,g → READY,g → READING,g → EMPTY,g+1`.

The consumer's acquire must observe the matching READY generation, and ownership must prevent reading during overwrite. If generation wraps while an old observer remains live, a stale READY can be mistaken for the new cycle. Use sufficient width, bounded lifetime, nonreuse, or a different protocol.

Ordering cannot compensate for an ambiguous state machine. Encode legal transitions and prove slot ownership separately.

### Publication does not prove lifetime

A release store can safely publish an initialized pointer. An acquire load can make initialization visible. Neither prevents another thread from freeing the object while the consumer uses it.

Lifetime can be protected by immutable ownership transfer, reference counting with safe acquisition, hazard pointers, epochs, garbage collection, a lock, or another documented mechanism. Reclamation actions themselves need ordering. Pair the hb publication proof with a “remains alive until” proof.

Similarly, publication does not validate array bounds, type invariants, authorization, or device state. It orders memory effects under the model; it is not a universal validation barrier.

### Language interfaces are not interchangeable

**C++** exposes `memory_order_relaxed`, acquire, release, acquire-release, and sequential consistency, with normative reads-from, release-sequence, fence, and data-race rules.

**Rust** exposes a closely related set of orderings for its atomic APIs and documents the split behavior of RMWs. Rust safety and ownership reduce some invalid aliasing, but `unsafe`/atomic protocols still require a memory-model proof and valid lifetime.

**Java** provides volatile and VarHandle plain, opaque, acquire, release, and volatile access modes with Java Memory Model guarantees. Method names and supported modes are part of the API; do not map them mechanically to C++ syntax.

**Go** intentionally specifies `sync/atomic` operations as synchronizing and sequentially consistent. It does not expose a per-call relaxed/acquire/release selector. Channels, mutexes, and other primitives document their own synchronized-before rules.

The same hardware may therefore receive different source constraints. Write and review against the selected language specification.

### Hardware and compiler mapping

On x86-64, many release stores and acquire loads can use ordinary load/store instructions because the architecture already supplies relevant ordering, while compiler constraints preserve source semantics. On Arm or RISC-V, acquire/release instructions or fences may be required. RMW mappings add exclusives or atomic extensions.

This is not permission to write relaxed code on a “strong” machine. The compiler optimizes under the source model, deployments change, devices have separate ordering domains, and mixed-language boundaries can invalidate assumptions.

Inspect optimized target assembly to verify cost and support, not to replace the language proof. Benchmark across actual architectures and toolchains before claiming a performance gain from weakening order.

### Device and persistent memory boundaries

Language atomics generally order ordinary program memory according to their model. Memory-mapped I/O, DMA, accelerators, noncoherent devices, persistent memory, and cross-process shared mappings may need platform-specific barriers, cache maintenance, flushes, or protocols.

A release store does not necessarily ensure data reached a device or durable medium. Use the platform and storage specifications. Separate:

- CPU visibility to another language thread;
- device visibility/coherence;
- durability after power loss; and
- remote/distributed acknowledgement.

Each boundary needs its own evidence.

### Verification

Review positive and negative litmus tests: consumer observes publication; consumer observes old state; publication precedes payload; acquire uses wrong carrier; repeated generation; RMW relay; broken store in a supposed release sequence; failed CAS; fence pairing; destruction during use.

Use model checkers/litmus tools for allowed outcomes, race detectors for ordinary conflicting accesses, stress for integration bugs, optimized assembly for mappings, and target measurements for performance. Race-detector silence does not prove the intended hb graph, and a forbidden result that never appears in stress is not proof it is impossible.

Instrument carrier value/generation, source transition identity, retries, timeouts, and lifecycle state. Avoid debug synchronization that changes the execution under study.

## Definitions and Notation

Let `sb` be sequenced-before within an agent, `rf` reads-from, `sw` synchronizes-with, and `hb=(sb ∪ sw)^+`, the transitive closure.

For producer events `W` and `S` and consumer events `L` and `R`:

`W sb→ S ∧ S sw→ L ∧ L sb→ R ⇒ W hb→ R`.

The sw premise is conditional: `L` must observe `S` or an operation covered by the exact language-defined synchronization rule. Same location and wall-clock order do not prove it.

Write `mo_x` for modification order of atomic `x`. A release sequence, where the language defines it, is a qualifying portion of `mo_x` headed by a release. “Acquire” and “release” name source-level semantics, not universal machine instructions.

## Mechanisms, Invariants, or Proof Structure

For every ordering boundary:

1. **Name the protected effects.** Payload fields, generation, ownership, and allowed readers.
2. **Choose the carrier.** One atomic state whose value identifies the published version.
3. **Order construction.** All protected writes are sb-before release.
4. **Prove observation.** Identify the exact rf or release-sequence relation.
5. **Guard consumption.** Protected reads occur only after the matching acquire.
6. **Close hb.** Compose sb, sw, and sb explicitly.
7. **Check all conflicts.** Every ordinary conflicting pair is hb-ordered or excluded by ownership.
8. **Handle RMW halves.** Derive read-side and write-side ordering independently.
9. **Handle reuse and lifetime.** Epochs, wrap bounds, ownership, retirement, and reclamation.
10. **Validate language/target.** Use current normative/API guarantees and inspect mappings only as implementation evidence.
11. **Test negative paths.** Old value, wrong carrier, early publication, failed CAS, timeout, and destruction.
12. **Prefer documented primitives when this proof is not local and stable.**

The executable graph model compares a valid publication path with an acquire that observes an old initialization value.

<!-- bijux-verify: {"id":"acquire-release-happens-before-graph","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"events=4\npositive_edges=3\npositive_payload_happens_before=True\nold_value_synchronizes=False\nold_value_payload_happens_before=False\nordinary_payload_safe=True\n","stderr":""}} -->
```python
events = 4
write_payload = 0
release_ready = 1
acquire_ready = 2
read_payload = 3

positive = [[False] * events for row in range(events)]
positive[write_payload][release_ready] = True
positive[release_ready][acquire_ready] = True
positive[acquire_ready][read_payload] = True

for middle in range(events):
    for source in range(events):
        for target in range(events):
            if positive[source][middle] and positive[middle][target]:
                positive[source][target] = True

old_value = [[False] * events for row in range(events)]
old_value[write_payload][release_ready] = True
old_value[acquire_ready][read_payload] = True
for middle in range(events):
    for source in range(events):
        for target in range(events):
            if old_value[source][middle] and old_value[middle][target]:
                old_value[source][target] = True

print(f"events={events}")
print("positive_edges=3")
print(f"positive_payload_happens_before={positive[write_payload][read_payload]}")
print(f"old_value_synchronizes={old_value[release_ready][acquire_ready]}")
print(f"old_value_payload_happens_before={old_value[write_payload][read_payload]}")
print(f"ordinary_payload_safe={positive[write_payload][read_payload]}")
```

Limitations: this model computes transitive reachability after stipulating edges. It does not execute atomics, determine reads-from, formalize a specific language's release sequences/fences, explore allowed weak-memory executions, detect races, inspect compiler/hardware mappings, prove lifetime, or establish device/durability ordering.

## Alternatives and Trade-Offs

**Sequentially consistent atomics** add a common order that can simplify multi-atomic reasoning, but they still require a correct state protocol and do not make ordinary races safe.

**Mutexes and read-write locks** provide documented acquisition/release edges plus exclusion and compound-state ownership. They may be clearer and faster under contention.

**Channels and ownership transfer** attach synchronization to the message that carries the payload, reducing carrier/payload mismatch.

**Once cells/futures** express one-time initialization or completion and often handle waiting, failure, and publication together.

**Immutable values** reduce post-publication conflicts, though their pointer/root publication and lifetime still need a protocol.

**Acquire/release atomics** minimize ordering when one carrier and one causal path suffice. Their advantage depends on target cost and proof maintainability.

**Fences** can separate observation from ordering for specialized algorithms, at substantial review risk.

**SC-only language atomics** trade fine-grained weakening for a simpler documented model; use the language as specified rather than simulating unavailable modes.

## Failure Modes and Misconceptions

1. **Release pushes every write globally.** It creates no universal broadcast.
2. **Acquire pulls the latest state.** It orders effects only through a qualifying observation.
3. **Same atomic object guarantees pairing.** The acquire must read the relevant value/history.
4. **Later wall-clock time means reads-from.** Source models do not use that inference.
5. **Acquire makes a wrong branch safe.** Payload must be read only after matching publication.
6. **Release before initialization is close enough.** Later writes are not published by that release.
7. **A boolean safely supports endless reuse.** Old and new cycles need identity.
8. **Acquire/release creates a multi-object snapshot.** It supplies a causal edge, not a transaction.
9. **Every RMW is fully acquire-release.** Its ordering and success/failure path determine its sides.
10. **Failed CAS can release.** It performs no desired write.
11. **Any intervening atomic preserves a release sequence.** Exact current language rules decide membership.
12. **A fence flushes all caches.** Fences participate in specific model relations.
13. **Publication protects lifetime.** Visibility and reclamation are distinct.
14. **x86 observations prove portable code.** Source semantics and other targets still govern.
15. **Java, Rust, C++, and Go modes are interchangeable.** Their APIs and formal models differ.
16. **A race detector proves the protocol.** It cannot certify the intended observation graph.
17. **CPU ordering proves device or durability order.** Those boundaries need platform protocols.
18. **Weaker ordering is automatically faster.** Measure generated code and workloads.

## Worked Examples

### Example 1

**Situation.** Producer writes payload 42 and release-stores ready one; consumer acquire-loads that one.

**Reasoning.** Payload write sb release, release sw acquire by reads-from, and acquire sb payload read. Transitivity gives hb.

**Conclusion.** The consumer may read the initialized immutable payload.

### Example 2

**Situation.** The same consumer acquire-loads zero.

**Reasoning.** It observed initialization, not the release publication. No sw edge exists from the producer.

**Conclusion.** It must not read payload; acquire is conditional on observation.

### Example 3

**Situation.** Producer release-stores ready before writing the second payload field.

**Reasoning.** The second write is not sb-before publication. Even a matching acquire does not put that later write before the consumer read.

**Conclusion.** Complete construction and validation before release.

### Example 4

**Situation.** Producer release-stores `payload_ready`; consumer acquire-loads unrelated `workers_started`.

**Reasoning.** No documented reads-from/synchronization relation connects these operations.

**Conclusion.** Publication and observation need one proven carrier chain.

### Example 5

**Situation.** A successful RMW consumes an initialized descriptor and publishes CLAIMED.

**Reasoning.** Acquire is needed on the read half to consume descriptor initialization; release is needed on the write half only if CLAIMED publishes earlier winner effects.

**Conclusion.** Derive RMW halves from their separate causal roles.

### Example 6

**Situation.** Failed CAS returns a READY pointer that the caller dereferences.

**Reasoning.** Failure cannot release but its read may need acquire because the returned witness carries publication. Reclamation must still keep the object alive.

**Conclusion.** Failure ordering and lifetime follow from actual witness use.

### Example 7

**Situation.** A ring slot reuses boolean ready after each consumer clears it.

**Reasoning.** A delayed observer cannot distinguish cycles. Add generation and ownership transitions; bound wrap and match acquire to READY,g.

**Conclusion.** Ordering needs unambiguous version identity.

### Example 8

**Situation.** Engineers replace an acquire load with relaxed load plus acquire fence.

**Reasoning.** Correctness depends on whether the language's fence rule connects the observed release value to the fence. Physical proximity is irrelevant.

**Conclusion.** Keep acquire on the load unless a normative proof and measurement justify the fence.

### Example 9

**Situation.** Go code attempts to select relaxed ordering for a hot counter.

**Reasoning.** Go's `sync/atomic` API specifies SC behavior and exposes no per-call relaxed mode. A C++ optimization cannot be transliterated.

**Conclusion.** Optimize within the selected language's documented model.

### Example 10

**Situation.** A surgical device release-publishes a command buffer and claims the actuator has safely received it.

**Reasoning.** CPU hb does not prove DMA coherence, device barriers, command identity, acknowledgement, timing, persistence, authorization, or hazard response.

**Conclusion.** Named controls, hardware, real-time, clinical, security, quality, and functional-safety reviewers need platform evidence; this chapter grants no approval.

## Cross-Program Connections

- **Programming languages:** memory models define sb, rf, sw, data races, and permitted transformations.
- **Computer architecture:** cache coherence and barrier instructions implement but do not define source guarantees.
- **Operating systems:** locks, futexes, joins, and scheduler interactions expose higher-level edges.
- **Data systems:** version publication resembles commit visibility, while durability and recovery add different boundaries.
- **Distributed systems:** message delivery and acknowledgement are not shared-memory acquire/release.
- **Security:** premature publication, stale generations, and use-after-free can become confidentiality or control-flow defects.
- **Embedded systems:** MMIO, DMA, and noncoherent devices require platform-specific ordering.
- **Software engineering:** explicit lifecycle states and documented primitive contracts reduce proof drift.

## References

1. Hans-J. Boehm and Sarita V. Adve. “Foundations of the C++ Concurrency Memory Model.” PLDI, 2008.
2. Mark Batty et al. “Mathematizing C++ Concurrency.” POPL, 2011.
3. Jade Alglave, Luc Maranget, and Michael Tautschnig. “Herding Cats: Modelling, Simulation, Testing, and Data Mining for Weak Memory.” TOPLAS 36(2), 2014.
4. Maurice Herlihy and Nir Shavit. *The Art of Multiprocessor Programming*, revised first edition. Morgan Kaufmann, 2012.
5. ISO C++ working draft. “Multi-threaded executions and data races; atomic order and consistency.” Current draft accessed 2026-08-29.
6. Oracle. *Java Language Specification*, Java SE 26, section 17.4, and `VarHandle` API. 2026. Accessed 2026-08-29.
7. Rust Project. “`std::sync::atomic` and `Ordering`, Rust 1.98.0.” 2026. Accessed 2026-08-29.
8. The Go Authors. “The Go Memory Model” and “Package `sync/atomic`.” Accessed 2026-08-29.
9. ARM Ltd. *Arm Architecture Reference Manual for A-profile Architecture*. Current edition accessed 2026-08-29.
10. Intel. *Intel 64 and IA-32 Architectures Software Developer's Manual*, version 092, 2026. Accessed 2026-08-29.

## Exercises

### Exercise 1

Define release, acquire, reads-from, synchronizes-with, and happens-before, then state the condition under which release/acquire publishes payload.

### Exercise 2

Given `W(payload)`, `S_release(flag=1)`, `L_acquire(flag)`, and `R(payload)`, derive the positive hb path and explain the outcome when L observes zero.

### Exercise 3

Diagnose a reusable slot whose producer release-stores boolean ready before its last field, whose consumer reads payload even after observing false, and whose storage can be freed concurrently. Repair state, ordering, and lifetime.

### Exercise 4

Compare acquire/release atomics, SC atomics, a mutex, a channel, and a once/future abstraction for publishing configuration once and for repeatedly handing off mutable buffers.

### Exercise 5

A flight-control process publishes DMA command descriptors using language atomics. Specify what the hb proof establishes, which CPU/device/lifetime/durability claims remain, how to verify them, and the human-review boundary.

## Answers to the Exercises

### Answer 1

Release is a source-model operation that can order earlier actions before a qualifying observer. Acquire can order later actions after effects carried by its qualifying observation. Reads-from identifies the write observed by a read. Synchronizes-with is the language-defined cross-thread relation created by that observation; happens-before is the transitive closure of sequenced-before and synchronizes-with.

Payload is published when its writes are sequenced before the release, the acquire observes that release or an operation covered by the exact release-sequence/fence rule, and payload reads are sequenced after the acquire and guarded by the matching value/generation. Lifetime and ownership remain separate.

### Answer 2

In the positive case, `W sb→ S` because construction precedes publication. When L reads S's one, `S sw→ L`. The guarded read gives `L sb→ R`. Transitivity yields `W hb→ R`, ordering the ordinary conflict.

If L reads initialization zero, `S sw→ L` is absent. Acquire alone supplies no path from W. The consumer must not execute R; it waits, retries, or reports not ready. Wall-clock timing cannot restore the missing edge.

### Answer 3

Publishing before the last field leaves that write outside the hb path. Reading after false ignores the precondition and can race. Concurrent free violates lifetime even after correct publication.

Use a generation-bearing state machine such as EMPTY,g→WRITING,g→READY,g→READING,g→EMPTY,g+1. Initialize and validate all fields before release-publishing READY,g. Acquire-load and verify the matching generation before any payload read. Give one consumer ownership or otherwise synchronize mutable access. Keep storage alive through ownership transfer, reference counting with safe acquisition, hazards, epochs, GC, or a lock, and retire only after readers quiesce. Bound generation wrap.

### Answer 4

For one-time immutable configuration, a once cell or future is clearest because it combines one-time transition, waiting/failure semantics, and publication. A release store plus guarded acquire load is valid when the state and lifetime are simple. SC atomics may simplify review with little extra target cost. A mutex is appropriate when construction, error state, and later metadata form a compound invariant.

For repeated mutable-buffer handoff, a channel naturally transfers ownership and synchronizes payload. A mutex/condition can manage a reusable pool and shutdown. Raw acquire/release atomics require generation, exclusive ownership, capacity, wakeup, cancellation, and lifetime proofs. SC does not remove those protocol obligations. Choose based on the full lifecycle, not one load/store benchmark.

### Answer 5

The language hb proof can establish that CPU writes to an in-memory descriptor are ordered before a CPU consumer's protected reads when the exact release/acquire observation occurs. It can also prove source-level absence of conflicting ordinary CPU accesses under stated ownership.

It does not by itself prove compiler extensions for MMIO, cache cleaning, DMA coherence, IOMMU mapping, device-visible barrier domains, descriptor format, doorbell ordering, actuator receipt, bounded latency, persistent logging, restart recovery, authorization, or storage lifetime. Use the processor and device manuals, driver/platform APIs, target assembly inspection, cache/barrier tests, hardware-in-loop traces, fault injection, race/model checking for CPU state, and end-to-end acknowledgement/reconciliation.

Named concurrency/language, kernel/driver, CPU architecture, hardware/device, controls, real-time, cybersecurity, avionics/domain, quality, regulatory, and functional-safety reviewers must approve system-specific claims with hazard and target evidence. This answer is not flight or deployment approval.
