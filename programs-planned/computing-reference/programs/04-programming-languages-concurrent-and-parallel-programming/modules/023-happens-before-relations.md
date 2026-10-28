---
module_id: CONPAR-023
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 23
title: Happens-Before Relations
status: complete
last_verified: 2026-08-29
---

# Happens-Before Relations

## One-Page Review

### Governing question

Which exact within-thread and synchronization edges prove that one action's effects are ordered before and visible to another action?

### Essential definitions

- **sequenced-before/program order** orders relevant actions within one thread according to its language semantics.
- **synchronizes-with** is a cross-thread edge created only by operations satisfying a language rule.
- **happens-before (hb)** is the transitive closure of within-thread order and specified synchronization edges.
- Two actions are **concurrent** in this model when neither happens-before the other.
- **transitivity** means A hb B and B hb C imply A hb C.
- A **release** publishes preceding effects; a matching **acquire** can import them under the source model's rules.
- A **conflict** involves the same memory location with at least one write.
- A **data race** generally requires conflicting ordinary accesses that are not hb-ordered; exact language definitions govern.
- A **publication path** connects initialization through synchronization to every dependent read.
- A **happens-before graph** records actions as vertices and justified order edges.

### Central model, mechanism, or theorem

For a producer writing payload P, then performing release S, and a consumer whose acquire A observes the matching publication before reading payload R:

(P ->sb S ->sw A ->sb R),

so by transitivity (P ->hb R). This is a partial-order proof: an unrelated action U can remain unordered with all four. If the acquire observes a different value or the primitive lacks the required semantics, the synchronizes-with edge is absent and the publication conclusion does not follow.

### Critical invariants

Every graph edge cites a source-language rule. Within-thread order is not automatically cross-thread visibility. Synchronizes-with requires the specified matching event, such as the lock acquisition following an unlock or an acquire reading the relevant release. Transitive paths may cross several threads. Acyclicity is required for a strict hb relation. Conflicting ordinary accesses are either hb-ordered or treated according to the language's race rules. Condition notification is not the protected predicate and normally must be joined with mutex order. Thread start and join, task completion, channels, futures, and once-initialization count only when their specifications provide edges. Wall-clock timestamps and logging order are not substitutes.

### Common failures

Teams draw an edge merely because one event occurred earlier; assume every acquire matches every release; treat relaxed atomic access as publication; confuse modification order with happens-before; infer payload visibility from a flag value not read from the publishing write; use notification without the predicate lock; assume sleep creates order; omit startup or join edges; treat approximate telemetry as authoritative; or conclude that hb establishes atomicity, fairness, deadlines, durability, or external-effect order.

### Compact example

Thread A initializes object fields, unlocks mutex m, and Thread B later locks m before reading them. Initialization is sequenced-before unlock; that unlock synchronizes-with the later successful lock; the lock is sequenced-before reads. The transitive path publishes the fields. A lock on unrelated mutex n supplies no such path.

### Connections

[Sequential Consistency in Shared Memory](022-sequential-consistency-in-shared-memory.md) uses one total order; happens-before retains only required partial order. [Condition Variables and Predicate Waiting](013-condition-variables-and-predicate-waiting.md) supplies mutex/predicate protocols. The [program roadmap](../ROADMAP.md) next applies hb to visibility/publication, atomic read-modify-write, and memory-order modes.

## Governing Question

How can an engineer prove a cross-thread observation using only order edges guaranteed by the programming language, while leaving genuinely independent actions unordered?

The answer is an edge ledger. Name the data to protect, the within-thread predecessors, the exact synchronization event and its match, the dependent successors, and the transitive path. If one edge lacks a rule, the proof is incomplete.

## Why This Matters

Sequential consistency offers a convenient global story, but production algorithms often need less: payload initialization must precede consumption; a critical-section write must precede a later critical-section read; a worker's effects must precede the thread that joins it. Happens-before captures these obligations without imposing one total order on everything.

This precision enables optimization and diagnosis. Independent counters can remain unordered. Publication can use release/acquire rather than unexplained global ordering. A race report can point to two conflicting actions with no hb path. A shutdown audit can distinguish “stop requested” from “worker termination observed.”

The relation is also easy to misuse. Physical time is not hb. A signal that arrives later is not automatically synchronization. An acquire operation creates no useful cross-thread edge unless the model connects it to the relevant release. Strong vocabulary without an explicit path merely hides the gap.

## Prerequisites and Retrieval

Retrieve:

- partial orders and linear extensions from [Interleavings and State-Space Explosion](003-interleavings-and-state-space-explosion.md);
- race definitions from [Race Conditions and Atomicity Violations](005-race-conditions-and-atomicity-violations.md);
- ownership transfer from [Message Passing and Ownership Transfer](009-message-passing-and-ownership-transfer.md);
- start/join lifetime from [Creating and Joining Threads](011-creating-and-joining-threads.md);
- mutex and condition semantics from [Mutexes and Mutual Exclusion](012-mutexes-and-mutual-exclusion.md) and [Condition Variables and Predicate Waiting](013-condition-variables-and-predicate-waiting.md);
- component publication obligations from [Designing a Correct Multithreaded Component](020-designing-a-correct-multithreaded-component.md); and
- total-order reasoning from [Sequential Consistency in Shared Memory](022-sequential-consistency-in-shared-memory.md).

Retrieval prompt: draw initialization -> unlock(m) -> later lock(m) -> read as four vertices, label edge kinds, and state which edge disappears if the consumer locks n instead.

## Learning Objectives

After completing this module, a learner can:

1. distinguish sequenced-before, synchronizes-with, happens-before, modification order, and wall-clock precedence;
2. compute transitive closure and identify unordered action pairs;
3. construct mutex, release/acquire, channel, start, join, and completion paths;
4. determine when a synchronization match is absent;
5. diagnose conflicting accesses with no hb ordering;
6. explain condition-variable ordering without treating notification as state;
7. derive lifecycle and publication guarantees across multiple threads;
8. audit language-specific rules without transferring folklore; and
9. state what hb does not prove about atomicity, progress, external systems, or safety.

## Core Exposition

### A partial order, not a timeline

Happens-before is a mathematical relation defined by a language execution model. It is not “happened at an earlier UTC timestamp,” “printed first,” or “the debugger displayed it first.” A hb B means the model orders A before B for the relevant semantic guarantees.

A strict form is irreflexive and transitive: no A hb A, and paths compose. Some specifications present a reflexive convention; follow the exact source vocabulary. In either presentation, unrelated actions can be incomparable. That incomparability is valuable because it represents concurrency without inventing order.

### Base edges and transitive closure

Begin with intra-thread order. C++ commonly says sequenced-before; Java specifies program order for inter-thread actions; Go uses sequenced-before in its formal execution account. The details differ, but the proof role is to connect earlier actions in one agent to its later synchronization event.

Add synchronizes-with edges only from rules. Examples can include:

- an unlock on mutex m to a later successful lock on m;
- a release atomic operation to a qualifying acquire that observes its release sequence;
- a channel send to the corresponding receive as specified;
- thread start to actions of the started thread;
- actions in a terminated thread to a successful join/termination observation;
- completion of one-time initialization to later observations; and
- future/promise completion to a specified successful wait or result retrieval.

Then take transitive closure. No source rule means no edge.

### Publication is a path

Suppose producer initializes fields f1 and f2, then release-stores READY. Consumer acquire-loads READY and, after observing the publishing value, reads f1 and f2.

Initialization is sequenced-before release. The release synchronizes-with the observing acquire under the language rule. Acquire is sequenced-before reads. Therefore each initialization write happens-before each dependent read.

The flag is a carrier, not the payload. If consumer reads an old READY from another generation, uses relaxed ordering, reads payload before acquire, or the release occurs before initialization finishes, the path fails. Draw each field or invariant whose visibility is claimed.

### Reads-from matters

An acquire load does not synchronize with a release merely because both touch the same atomic. It must satisfy the model's reads-from/release-sequence condition. With multiple writers and repeated values, the integer alone may not identify which release supplied it.

Use generation-tagged states or unique transitions where ambiguity matters. Record the source write in formal analysis. An acquire that observes the initial value creates no edge from a later release.

### Mutexes carry prior effects

Thread A writes protected state under m and unlocks. Thread B's subsequent successful lock of m imports the preceding critical-section effects. The proof is:

write ->sb unlock(m) ->sw lock(m) ->sb read.

Mutual exclusion and visibility are related but distinct benefits. Locking a different mutex supplies neither the matching sw edge nor protection of the same invariant. Reading the state before locking is outside the path.

Unlock must occur after restoring the protected invariant. Calling foreign code while locked can preserve hb but introduce deadlock, unbounded delay, or reentrancy failure; ordering correctness is not a complete component proof.

### Condition variables add control, not state

A condition wait atomically releases a mutex and later reacquires it before returning. Notification makes waiters eligible according to the API; the protected predicate decides whether work is available. The producer changes predicate state while holding the mutex, then notifies according to the protocol. The consumer waits in a loop and examines the predicate after reacquisition.

The hb path for protected data commonly travels through unlock/lock synchronization, not through a mystical property of “signal occurred first.” Notification can race before waiting, wake spuriously, or be consumed by another waiter, while persistent predicate state remains authoritative.

### Start and join edges

Fully initialize thread input before start. A specified thread-start edge publishes preceding setup to the new thread. Starting from a partly initialized constructor can expose state before the path's source actions exist.

At the other end, successful join or a specified termination observation imports the worker's preceding actions. Merely checking a non-synchronized boolean “probably done” does not. Join is also a lifetime boundary: resources cannot be destroyed while worker access remains possible.

Joining while holding a lock needed by the worker can deadlock even though the intended visibility edge would be valid if join returned. Liveness remains separate.

### Channels and ownership transfer

A channel operation can carry both value ownership and synchronization. The exact send/receive or close/receive rules depend on language and channel type. Do not assume every observation of channel closure publishes every unrelated producer action.

For a bounded work queue, submission may publish job contents to dequeue, and completion may publish results to a waiter. Those are two different paths. Queue thread safety does not automatically publish data stored elsewhere after enqueue.

### Transitivity across threads

Paths can cross agents. Thread A writes data then release-publishes to B. B acquire-observes, derives a summary, and releases to C. C's matching acquire can observe both A's preceding data and B's summary through transitivity.

This relay is powerful but fragile: if B publishes before finishing the summary, or C's acquire observes a different generation, the chain breaks. A graph makes the missing edge visible.

### Data races as missing order

Two ordinary accesses conflict when they address the same location and at least one writes. Many modern language models define a data race when such accesses occur in different threads without the required hb ordering, with details for atomics, lifetimes, and signal handlers.

If W(x) and R(x) are unordered, do not guess that the read sees “old or new.” In C++/Rust unsafe code, the race can yield undefined behavior; Java and Go impose different constraints but still classify races as incorrect or surprising. Apply the exact language.

Race freedom alone does not prove the invariant. Two hb-ordered operations can implement the wrong state transition. A check and later action under separate critical sections may be individually race-free yet logically stale.

### Modification order is not hb

Atomic modifications to one object have a modification order. That order does not by itself publish ordinary data or produce hb between arbitrary operations. Relaxed atomics can supply atomicity and per-location ordering without a cross-location visibility path.

Conversely, hb may relate actions on different locations through mutexes, channels, or release/acquire. Keep the relations separately labeled and use only formal composition rules.

### Time, logs, and observability

If event A has an earlier timestamp than B, clock sampling shows an operational chronology subject to clock and buffering behavior; it does not create a language hb edge. Logging often takes locks or queues and can add synchronization, perturbing the bug.

Distributed Lamport “happened-before” relates process order and message send/receive in a distributed event system. It shares partial-order structure but is not automatically the same relation as a C++ or Java memory model. Map the system boundary explicitly.

Telemetry counters can be relaxed and approximate when they publish no correctness-critical state. Final reconciliation must use authoritative synchronized state. Observability should report the proof events—generation, source write, state transition, join—without becoming the proof mechanism.

### Fences and mixed orderings

Fences can participate in hb paths only through language-specific rules involving surrounding atomic operations. A fence placed between ordinary accesses is not a universal edge. Mixed relaxed, acquire/release, and seq_cst operations require reads-from, modification-order, fence, and happens-before analysis together.

Prefer high-level primitives when they express the needed ownership and lifecycle. When using atomics, derive ordering from the payload relation rather than a table saying one mode is “fast” and another “safe.”

### What happens-before guarantees—and does not

An hb path can establish ordering/visibility and eliminate a conflicting-access race under the source model. It can justify safe publication and lifecycle handoff.

It does not make a group of operations indivisible, select the right business state, guarantee progress, wake a waiter, bound resources, roll back side effects, ensure durability, or order a device. It does not prove a deadline, security property, or safety case.

The relation is a necessary proof tool inside a larger design, not a synonym for correctness.

### Verification workflow

Create a ledger with columns: source action, destination action, edge kind, matching identity/generation, specification citation, protected data, and failure if absent. Compute transitive closure and query every conflicting pair and publication claim.

Static review finds missing or mislabeled edges. Race detectors discover executed unordered conflicts. Model checkers explore read-from choices and schedules. Litmus tools validate language/architecture behavior. Deterministic hooks force publish/acquire, cancel/finish, close/submit, and join races.

All are scoped. A race detector cannot prove every execution; graph closure cannot prove its base edges correspond to code; stress cannot prove an outcome forbidden; and a language proof does not cover DMA or remote storage.

## Definitions and Notation

Let A be actions. Sequenced-before (sb) orders relevant same-thread actions. Synchronizes-with (sw) contains specified cross-thread pairs. Happens-before is the transitive closure:

(hb = (sb union sw)+).

Write A ->hb B when A precedes B. Actions A and B are unordered when neither A ->hb B nor B ->hb A. For conflict relation cf, a candidate ordinary-access race is a pair in cf that is hb-unordered, subject to the language's exact rules.

Reads-from rf relates a write to the read taking its value. Modification order mo_x orders atomic modifications of x. These relations interact under source rules but are not interchangeable.

A path certificate lists vertices and labeled edges from source to destination. A missing-edge counterexample removes one claimed base edge and demonstrates the dependent hb conclusion is unreachable.

## Mechanisms, Invariants, or Proof Structure

Use this derivation:

1. **Name the protected fact.** Field, invariant, generation, result, or lifetime.
2. **Name source and destination actions.** Avoid vague thread-level arrows.
3. **Add same-thread edges.** Confirm source occurs before release and acquire before use.
4. **Prove the synchronization match.** Same mutex, observed release, corresponding receive, start, join, or specified completion.
5. **Compute transitive closure.** Preserve incomparability where no path exists.
6. **Audit conflicts.** Every ordinary conflicting pair needs required order.
7. **Test negative cases.** Old generation, initial value, unrelated lock, relaxed operation, missed notification, early publication.
8. **Separate other relations.** rf, mo, SC order, real time, wait-for, and device order.
9. **Validate implementation mapping.** Language, library, compiler, and target versions matter.
10. **State residual obligations.** Atomicity, liveness, bounds, failure, external effects, and assurance.

The executable graph contains a four-action publication chain plus one unrelated action.

<!-- bijux-verify: {"id":"happens-before-transitive-closure","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"actions=5\ndirect_edges=3\nhappens_before_pairs=6\npublished_payload=True\nreverse_order=False\nunordered_action_pairs=4\n","stderr":""}} -->
```python
actions = ("payload_write", "release", "acquire", "payload_read", "unrelated")
count = len(actions)
reachable = []
for row in range(count):
    reachable.append([False] * count)

reachable[0][1] = True
reachable[1][2] = True
reachable[2][3] = True
direct_edges = 3

for middle in range(count):
    for source in range(count):
        for destination in range(count):
            if reachable[source][middle] and reachable[middle][destination]:
                reachable[source][destination] = True

happens_before_pairs = 0
unordered_action_pairs = 0
for source in range(count):
    for destination in range(source + 1, count):
        if reachable[source][destination] or reachable[destination][source]:
            happens_before_pairs += 1
        else:
            unordered_action_pairs += 1

print(f"actions={count}")
print(f"direct_edges={direct_edges}")
print(f"happens_before_pairs={happens_before_pairs}")
print(f"published_payload={reachable[0][3]}")
print(f"reverse_order={reachable[3][0]}")
print(f"unordered_action_pairs={unordered_action_pairs}")
```

Limitations: this computes reachability in one fixed five-action directed graph. It assumes all three base edges are valid, contains no reads-from alternatives, language execution, threads, compiler, hardware, data values, progress, or device behavior, and does not prove the graph matches an implementation.

## Alternatives and Trade-Offs

**Mutex paths** combine exclusion and publication with simple proofs, at blocking and contention cost.

**Release/acquire atomics** express narrow publication efficiently, but matching values, generations, and lifetime require care.

**Sequentially consistent atomics** add a global order among specified operations and can simplify some proofs, without repairing missing ownership or compound atomicity.

**Channels and structured tasks** package ownership and completion edges, while requiring bounded capacity and lifecycle semantics.

**Immutable data before publication** reduces post-publication conflicts, though the publication edge and lifetime remain necessary.

**Thread confinement and partitioning** eliminate many cross-thread edges by design, at the cost of message routing or reduced sharing.

**Formal weak-memory models** capture rf, mo, fences, and hb precisely, with greater modeling and review burden.

## Failure Modes and Misconceptions

1. **Earlier in time means happens-before.** Only specified semantic edges compose.
2. **Same atomic means synchronize.** The acquire must satisfy the model's matching rule.
3. **Acquire makes all memory fresh.** It imports effects connected through its actual publication path.
4. **Relaxed atomic publishes payload.** Atomicity and modification order are not hb publication.
5. **Notification is the predicate.** State plus mutex discipline survives missed and spurious wakes.
6. **Any lock publishes any state.** The matching lock and protected invariant must align.
7. **Sleep creates order.** Delay is neither synchronization nor progress proof.
8. **Join is only cleanup.** A specified successful join is also a visibility and lifetime edge.
9. **Race-free means logically atomic.** Multi-step protocols can be stale while fully hb-ordered.
10. **Logs prove order.** Logging buffers and synchronization can reorder or perturb evidence.
11. **Modification order equals hb.** They are distinct relations with explicit composition rules.
12. **Transitivity repairs a missing base edge.** Every path depends on justified edges.
13. **A graph proves the code.** Mapping actions and matches to implementation is a separate review.
14. **HB guarantees liveness.** Deadlock, starvation, and missed work remain.
15. **Language hb orders devices and remote effects.** Those require additional specifications.

## Worked Examples

### Example 1

**Situation.** A writes payload, unlocks m; B locks m, reads payload.

**Reasoning.** Write sb unlock, unlock sw later lock on m, lock sb read. Transitivity gives write hb read.

**Conclusion.** The matching mutex carries protected effects.

### Example 2

**Situation.** B locks n instead of m before reading.

**Reasoning.** No unlock(m)-to-lock(n) rule supplies sw. Same-thread edges remain but cannot cross threads.

**Conclusion.** Unrelated synchronization does not publish the payload.

### Example 3

**Situation.** Consumer acquire-loads READY but sees the initial value.

**Reasoning.** It did not observe the producer's release publication, so that release/acquire sw edge is absent. It must not read the payload as published.

**Conclusion.** Operation mode alone is insufficient; the read source matters.

### Example 4

**Situation.** A publishes to B, which computes and publishes to C.

**Reasoning.** A's write hb B's acquire/use; B's use is before its release; that release sw C's acquire. Transitivity carries A's write to C.

**Conclusion.** Valid relays extend visibility across multiple threads.

### Example 5

**Situation.** Producer notifies before consumer begins waiting.

**Reasoning.** Notification may be lost as an event, but producer's predicate update persists under the mutex. Consumer checks the predicate before waiting and proceeds.

**Conclusion.** Correctness rests on predicate state and lock ordering, not remembered notification.

### Example 6

**Situation.** Main initializes input then starts worker.

**Reasoning.** Initialization precedes start; the language's start edge precedes worker actions. The transitive path publishes input.

**Conclusion.** Finish initialization before exposing the thread.

### Example 7

**Situation.** Worker writes result and exits; owner successfully joins then reads.

**Reasoning.** Worker write precedes termination, termination synchronizes as specified with successful join, and join precedes read.

**Conclusion.** Join establishes completion visibility as well as lifetime closure.

### Example 8

**Situation.** Two threads relaxed-increment an atomic metric.

**Reasoning.** Updates are atomic and ordered for that location, but they need not publish unrelated request state. If the counter is telemetry only, no payload hb edge is required.

**Conclusion.** Do not strengthen independent metrics by superstition.

### Example 9

**Situation.** All accesses are mutex-protected, but check and use occur in different critical sections.

**Reasoning.** There is no data race, yet another thread can change state between the sections. HB orders the actual accesses but does not make the pair indivisible.

**Conclusion.** Race freedom is weaker than protocol atomicity.

### Example 10

**Situation.** A clinical alarm pipeline uses a release/acquire flag and claims safe end-to-end delivery.

**Reasoning.** The edge may publish in-memory payload, but it does not prove queue bounds, alarm priority, device I/O, network delivery, persistence, deadlines, human response, or hazard controls.

**Conclusion.** Named clinical, systems, hardware, real-time, security, regulatory, and safety reviewers need end-to-end evidence; this chapter gives no deployment approval.

## Cross-Program Connections

- **Programming languages:** each language defines base edges, race consequences, and atomic composition.
- **Graph algorithms:** transitive closure, reachability, reduction, and cycle detection implement hb audits.
- **Formal methods:** execution graphs combine sb, rf, mo, sw, and hb constraints.
- **Operating systems:** start, join, mutexes, futexes, signals, and devices cross abstraction layers.
- **Distributed systems:** message causality has related partial-order mathematics but different failure semantics.
- **Software engineering:** an edge ledger turns concurrency assumptions into reviewable contracts.
- **Safety engineering:** visibility is one claim inside a broader hazard and timing argument.

## References

1. Leslie Lamport. “Time, Clocks, and the Ordering of Events in a Distributed System.” *Communications of the ACM* 21(7), 1978.
2. Leslie Lamport. “How to Make a Multiprocessor Computer That Correctly Executes Multiprocess Programs.” *IEEE Transactions on Computers* C-28(9), 1979.
3. Hans-J. Boehm and Sarita V. Adve. “Foundations of the C++ Concurrency Memory Model.” PLDI, 2008.
4. Mark Batty et al. “The C11 and C++11 Concurrency Model.” POPL, 2011.
5. Daniel J. Sorin, Mark D. Hill, and David A. Wood. *A Primer on Memory Consistency and Cache Coherence*, second edition. Morgan & Claypool, 2022.
6. Oracle. *Java Language Specification, Java SE 26*, Sections 17.4.4–17.4.5, 2026. Accessed 2026-08-29.
7. ISO C++ working draft. “Multi-threaded executions and data races; order and consistency.” Current draft accessed 2026-08-29.
8. Rust Project. “`std::sync` and `core::sync::atomic::Ordering`, Rust 1.98.0.” 2026. Accessed 2026-08-29.
9. The Go Authors. “The Go Memory Model,” version of 2022-06-06. Accessed 2026-08-29.
10. IEEE and The Open Group. *POSIX.1-2024, Threads and Memory Synchronization*, 2024.

## Exercises

### Exercise 1

Define sequenced-before, synchronizes-with, happens-before, and hb-unordered without using wall-clock language.

### Exercise 2

Construct the complete path for producer payload initialization, release READY, consumer acquire READY, and payload read. State two observations that would break the path.

### Exercise 3

Diagnose a condition-variable program that writes a predicate without the mutex, notifies, and whose consumer tests once with `if` before waiting. Repair its state, wake-up, and hb protocol.

### Exercise 4

Compare mutex, release/acquire atomic, channel, and start/join paths for publishing immutable configuration to workers and collecting results. Choose a design and list residual obligations.

### Exercise 5

A railway sensor gateway uses hb-safe in-memory buffers but DMA, network transmission, and shutdown remain separate. Build the proof boundary and identify required human review.

## Answers to the Exercises

### Answer 1

Sequenced-before orders relevant actions within one thread under its language semantics. Synchronizes-with is a cross-thread relation created by a specified matching synchronization pair. Happens-before is the transitive closure of those base relations. Two actions are hb-unordered when neither reaches the other through that closure. Physical timestamps neither define nor substitute for these relations.

### Answer 2

For payload write P, release S, acquire A, and read R:

(P ->sb S ->sw A ->sb R),

therefore P ->hb R. The path breaks if A observes the initial/other-generation state rather than S, or if S/A use orderings that do not create sw. It also fails if P occurs after S or R before A.

### Answer 3

Writing the predicate outside its mutex races with the consumer or disconnects the state from the wait protocol. Notification is transient, and `if` fails under spurious wake-up or a competing consumer.

Repair by acquiring m, changing the predicate and associated payload, releasing m, and notifying according to the API's safe placement rules. Consumer acquires m and loops while the predicate is false; wait atomically releases m and reacquires it before rechecking. The producer unlock to consumer lock/reacquisition carries protected effects. Close/cancellation must also change persistent state and wake all relevant waiters.

### Answer 4

A mutex path is simplest for mutable shared configuration: initialize/update under m, unlock, workers lock before copying, then operate on immutable snapshots. Release/acquire works for a one-way READY generation but needs exact reads-from and lifetime proof. A channel naturally transfers immutable configuration ownership and can collect result messages, but needs bounded capacity and close semantics. Start publishes pre-start immutable input, and join imports final worker results, but neither alone handles mid-run updates.

Choose pre-start immutable configuration plus start edges, bounded result channels during execution, and join for final lifetime closure. Residual obligations include channel bounds, unique result identity, task failure, cancellation, worker dependency cycles, close/wake/drain, join deadlines, and final reconciliation.

### Answer 5

The language hb proof covers CPU writes to normal memory, synchronization that publishes buffer ownership, and CPU readers that acquire it. It does not automatically cover DMA coherence/cache maintenance, MMIO doorbells, device completion, kernel-driver mappings, network acknowledgement, durable receipt, or physical sensor validity.

Specify separate ownership states and ordering rules for CPU-to-DMA handoff, device-to-CPU completion, network delivery, retry/idempotency, shutdown quiescence, and buffer reuse. Verify exact platform barriers and memory attributes, hardware-in-the-loop faults, timing, lost/duplicate data, power failure, and final reconciliation. Named railway-domain, driver, hardware, real-time, networking, cybersecurity, regulatory, and functional-safety reviewers must approve system claims. This answer does not establish deployment fitness.
