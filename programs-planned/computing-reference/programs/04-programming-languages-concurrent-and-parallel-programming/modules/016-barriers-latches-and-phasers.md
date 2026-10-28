---
module_id: CONPAR-016
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 16
title: Barriers, Latches, and Phasers
status: complete
last_verified: 2026-08-29
---

# Barriers, Latches, and Phasers

## One-Page Review

### Governing question

How can a program coordinate completion and repeated phase boundaries without letting a participant enter a later phase before every required predecessor arrives, and how should failure, cancellation, membership change, memory visibility, and termination alter that protocol?

### Essential definitions

- A **barrier** is a rendezvous at which a fixed set of parties arrives and waits until the generation advances.
- A **cyclic/reusable barrier** repeats the rendezvous with a generation number that separates arrivals from different rounds.
- A **latch** is a one-shot gate whose nonnegative count decreases to zero and does not reset.
- A **phaser** coordinates numbered phases while supporting registration, arrival, waiting, deregistration, and often hierarchical composition.
- A **party** is one registered unit of participation; it need not be permanently identical to one thread.
- A **generation/phase** identifies one synchronization round.
- A **barrier action/completion function** runs at the phase transition under API-specific execution and failure rules.
- A **broken barrier** is a failed generation from which normal successful passage is disallowed.
- **arrive-and-deregister** both satisfies the current obligation and removes the party from later phases.
- **phase skew** is the distance between fastest and slowest participant progress.
- A **sense-reversing barrier** distinguishes consecutive generations by toggling a local/global sense.
- A **hierarchical barrier** aggregates arrivals in a tree to reduce centralized contention.

### Central model, mechanism, or theorem

For fixed generation (g), let registered parties be (P_g) and arrivals be (A_g subseteq P_g). Maintain (A_g subseteq P_g). The phase may advance to (g+1) only when (A_g=P_g), unless an explicit break/termination transition occurs. On successful advance, no party observes post-phase work before all required pre-phase arrivals.

A latch instead maintains (C>=0), monotonically changing (C to max(0,C-1)); waiting succeeds when (C=0). A phaser makes (P_g) dynamic but must serialize registration and deregistration with generation boundaries.

### Critical invariants

Every registered party arrives exactly once per required phase. No arrival is counted for the wrong generation. Fixed-barrier party count matches control flow. Latch countdown represents completed obligations and occurs exactly once even on failure paths where “finished” includes failure. Phase data is published before arrival and consumed only after successful advance according to the API memory model. Cancellation cannot strand peers silently. Deregistration satisfies the current obligation and changes later membership atomically. Barrier actions are bounded and propagate failure. Reuse never confuses old wakeups with a new generation.

### Common failures

Teams count threads rather than logical parties; omit a coordinator that also waits; let one worker take fewer loop iterations; count down only on success; count down twice on retry; reuse a one-shot latch; reset while parties wait; ignore broken state; time out one waiter but leave peers blocked; perform unbounded work in the completion action; register after a phase has effectively closed; deregister without arriving; treat an observed count as control state; use a process-local barrier across machines; or place a global barrier inside an imbalanced hot loop.

### Compact example

Three workers compute disjoint rows for generation 7. Arrivals progress from empty to {A}, {A,C}, then {A,B,C}. Only the third arrival advances generation 8 and releases the others. If B fails before arrival, A and C cannot distinguish “slow” from “gone” without an explicit cancellation/break protocol; merely waiting preserves safety but destroys liveness.

### Connections

[Condition Variables and Predicate Waiting](013-condition-variables-and-predicate-waiting.md) supplies predicate-loop foundations; [Semaphores and Resource Counting](014-semaphores-and-resource-counting.md) supplies conserved obligations; [Read-Write Locks](015-read-write-locks.md) separates exclusion from progress policy. The [program roadmap](../ROADMAP.md) next develops thread-safe queues, lock ordering, thread pools, and thread-local state.

## Governing Question

How do we select and prove one-shot completion, fixed repeated rendezvous, or dynamic phased participation so that every transition has the right parties, data visibility, failure semantics, and termination behavior?

The key abstraction is a generation-indexed obligation ledger. “Everyone waited” is a consequence of correct registration, arrival, failure, and advancement—not a sufficient design statement.

## Why This Matters

Many parallel algorithms alternate local work with a global transition: simulation timesteps, iterative solvers, graph frontiers, stencil updates, batched aggregation, and deterministic race tests. A barrier prevents a fast participant from consuming incomplete results. A latch lets a coordinator await independent completions without forcing completing workers to wait. A phaser handles evolving task sets and multi-stage pipelines.

These primitives create group fate. One omitted arrival can suspend every other party. One double countdown can release a latch before work finishes. Reusing state without a generation identifier lets a late wake from round (g) corrupt round (g+1). Cancellation and timeouts are therefore protocol transitions affecting peers, not private return choices.

They can also impose costly synchronization. A barrier's completion time is determined by its slowest required party plus arrival and wake overhead. Frequent global barriers amplify load imbalance and operating-system noise. Centralized counters cause cache-line contention; tree barriers reduce fan-in at extra complexity. Good parallel decomposition reduces unnecessary global coordination.

Current APIs differ. POSIX.1-2024 defines fixed-party reusable thread barriers, a distinguished serial-thread return, memory synchronization, and process-sharing attributes. Java SE 26 distinguishes one-shot `CountDownLatch`, fixed `CyclicBarrier` with all-or-none breakage, and flexible `Phaser` with dynamic parties and tiering. Rust 1.98 `Barrier` is reusable with a leader result. Exact interruption, timeout, reset, termination, action, and visibility guarantees belong to the selected API.

## Prerequisites and Retrieval

Retrieve:

- predicate waiting, spurious returns, deadlines, cancellation, and shutdown from [Condition Variables and Predicate Waiting](013-condition-variables-and-predicate-waiting.md);
- conserved acquire/release obligations and lifecycle from [Semaphores and Resource Counting](014-semaphores-and-resource-counting.md);
- safety/liveness separation and starvation from [Safety, Liveness, and Progress](004-safety-liveness-and-progress.md);
- task lifetime and joining from [Creating and Joining Threads](011-creating-and-joining-threads.md); and
- sets, monotone counters, induction, partial orders, happens-before, load balance, exceptions, and tree reductions.

Retrieval prompt: for parties A, B, and C over two generations, list the six required arrivals. Show why A's second-generation arrival before C's first-generation arrival violates a reusable barrier even though six total arrivals eventually occur.

## Learning Objectives

After completing this module, a learner can:

1. distinguish latches, fixed reusable barriers, and dynamic phasers by obligation shape;
2. formalize generation state and prove no early phase advance;
3. prevent cross-generation arrival confusion with a generation or sense;
4. design exactly-once countdown and arrival across success, failure, and cancellation;
5. specify barrier breakage, timeout, reset, and completion-action semantics;
6. manage dynamic registration and deregistration without stranding parties;
7. reason about memory visibility across successful phase transitions;
8. compare centralized, tree, dissemination, and asynchronous alternatives; and
9. identify safety-critical phase claims requiring named authorized review.

## Core Exposition

### Choose the obligation shape

Use a latch when (N) completion events open a one-shot gate. Counters may be decremented by workers that do not wait. A start gate of one and completion latch of (N) are different objects.

Use a cyclic barrier when a stable set of parties repeatedly rendezvous. Each party normally both arrives and waits. Use a phaser when tasks can register/deregister, some parties arrive without waiting, or hierarchical composition is needed.

Do not emulate reuse by resetting a latch visible to old waiters. Do not use a barrier when a reduction, future aggregation, queue, or structured join directly represents the dependency.

### Fixed barrier state machine

For generation (g), store expected count (N), arrived count (a), broken/terminated state, and generation identity. Arrival increments (a) once for that party and generation. If (a<N), the caller waits while generation and terminal state remain unchanged. If (a=N), one transition:

1. runs the completion action if any;
2. records its outcome;
3. resets arrival accounting for the next generation;
4. increments generation; and
5. wakes the old generation's waiters.

Waiters must test the generation, not only (a=0), because zero is also the initial state of the next round. A sense-reversing barrier gives each participant a local sense and flips the shared sense at completion.

<!-- bijux-verify: {"id":"barrier-generation-schema","mode":"schematic","language":"text","toolchain":"none","reason":"Language-neutral pseudocode describes a reusable generation protocol; atomic operations, waiting, and failure behavior are API-specific."} -->
```text
my_generation = generation
arrive_once(my_generation)
if this_is_last_arrival:
    run_bounded_completion_action()
    advance_generation_and_wake_all()
else:
    wait_while(generation == my_generation and not broken)
```

The schema is not an implementation: correct atomicity, lost-wakeup avoidance, memory ordering, overflow, destruction, and cancellation require a real supported primitive or rigorously verified construction.

### Latch accounting

A latch count represents unfinished obligations, not worker existence. Define one countdown unit precisely: “one submitted task has reached a terminal outcome and published its result.” Put countdown in cleanup after submission succeeds. If submission fails, either never create the obligation or compensate exactly once.

Waiting for zero does not by itself report which tasks failed. Results need a separate indexed structure or failure channel published before countdown. Once zero, later waits normally pass immediately; the latch cannot represent a new batch.

Reading the count is useful for diagnostics, not for check-then-act. Another participant can decrement immediately. Extra countdown after zero may be ignored by an API, hiding double completion; application tokens should detect duplicates.

### Phase data and memory visibility

The semantic dependency is: every party's pre-arrival writes become available to permitted post-advance reads under the API's documented synchronization rule. Java specifies happens-before chains for its latches and cyclic barriers. POSIX lists barrier wait among memory-synchronizing operations.

The barrier does not resolve concurrent writes before arrival. Each party must own disjoint state or use synchronization. Nor does it make an object immutable after advance; later writes require another protocol. A completion action can safely aggregate only the data whose publication conditions are met.

### Failure and all-or-none breakage

If one fixed party times out, is interrupted, is cancelled, or throws before arrival, peers cannot complete normally. A robust API may break the generation and wake every waiter with a terminal result. Java `CyclicBarrier` documents this all-or-none model. Other primitives may require explicit cancellation state.

Choose whether failure means:

- abort the entire computation;
- contribute a failure result and still arrive;
- deregister from future phases after satisfying the current obligation; or
- replace the failed party under a controlled membership protocol.

Never let one caller return privately while peers wait forever. One absolute monotonic deadline should govern the operation; resetting relative time per generation or spurious wake extends the budget.

### Completion actions

A completion action runs once at the transition. It can swap current/next buffers, aggregate local convergence flags, increment an epoch, or decide termination. Keep it bounded, nonblocking, and free of callbacks that can reenter the barrier.

Specify which participant runs it, what state is visible, whether others remain blocked, and how exceptions propagate. If it fails, the generation must not look successfully complete. Long serial actions impose an Amdahl-style bottleneck at every phase.

### Dynamic registration and deregistration

A phaser records registered, arrived, and unarrived parties for a phase. Registration must define which phase gains the obligation. Arrival-and-deregister both completes the current obligation and removes future obligations. Forgetting deregistration leaks membership; deregistering without satisfying the current phase can advance prematurely if not one atomic operation.

Child tasks should register before a parent can arrive and allow the phase to close. If registration races with advance, follow the API's specified returned phase and retry/participate accordingly. Prevent count overflow and reject registration after termination.

Dynamic membership helps recursive parallelism but makes ownership harder. Pair registration with a scoped token that must arrive/deregister exactly once. Observe party counts, phase, termination, and maximum wait age.

### Unequal iteration counts and termination

A fixed barrier inside a loop requires every party to execute the same number of waits in the same generation order. Local early exit strands others. Instead, contribute a local “done” flag, arrive, compute global termination in the completion action, then let all parties exit after the same transition. A phaser can use arrive-and-deregister when independent parties legitimately finish, provided the algorithm tolerates shrinking membership.

Separate “phase advanced” from “computation succeeded.” Record one terminal outcome and wake all waiters. Phase-number wraparound, where relevant, requires comparison rules that do not confuse ancient and current generations.

### Scaling and topology

A centralized barrier updates one shared counter or queue and can become a cache-coherence hotspot. A tree barrier combines arrivals locally and propagates release downward in (O(log P)) depth. A dissemination barrier exchanges signals in logarithmic rounds. Tournament and combining-tree designs offer other topology trade-offs.

Hierarchical phasers aggregate child parties into parents, reducing contention. They add failure propagation, registration, and termination boundaries. Choose topology using participant count, NUMA layout, arrival variance, phase frequency, and runtime support. The slowest required arrival remains a lower bound regardless of algorithm.

### Lifecycle and tests

Construct before publishing and destroy only after all generations, waiters, completion actions, and possible accessors terminate. Reset only under the API's safe preconditions; reset is not recovery unless every participant agrees on the new computation epoch.

Test missing, duplicate, early, late, and wrong-generation arrivals; unequal loops; action failure; timeout/interruption races; break and reset; registration at advance; deregistration; zero/one party boundaries; phase wrap; shutdown; and destruction. A barrier can deliberately align test actors near a race, but the test still needs a logical oracle such as state cardinality or version—not merely “both returned.”

### Arrival without waiting

Some phaser and C++-style barrier APIs separate arrival from waiting. This can overlap independent work: a party publishes phase (g) output, arrives, performs work that does not depend on phase completion, then waits before consuming phase (g+1) input. The proof must name that independent interval.

Arrival is irrevocable for the generation. After arriving, a party must not modify data promised complete at that boundary. A returned phase token identifies what the later wait observes. Reusing a stale token, waiting for the wrong phase, or consuming dependent state before return breaks the protocol even when the party count is correct.

Arrive-and-drop is different: it satisfies the current arrival and reduces expected participation in later generations. Use it only where the algorithm no longer needs that party's future contributions.

### Reset, recovery, and computation epochs

A broken barrier records that one generation did not complete normally. Resetting its count cannot undo partial writes, compensate external effects, resurrect failed parties, or tell survivors which work to discard. Recovery needs an application computation epoch above the barrier generation.

On failure, stop new phase work, wake or cancel every participant, establish quiescence, classify partial results, and create a new epoch with explicit membership and clean state. Only then reset or replace the primitive if its contract permits. This prevents an old participant from arriving in a restarted computation. Double buffers, version tags, or immutable snapshots can keep aborted output distinct from committed input.

### Process-local versus distributed coordination

A thread barrier assumes a shared failure domain and synchronization memory model. It cannot coordinate machines through a partition: a remote participant may be slow, failed, or unreachable, and local memory edges do not publish remote state.

A distributed phase protocol needs durable membership, epoch fencing, message identity, retry/deduplication, failure assumptions, quorum or consensus rules, and coordinator recovery. Calling a network counter a “barrier” does not import thread-barrier semantics. “All frozen members reported” and “a safe quorum reported” are different predicates.

### Barrier-based concurrency tests

A test barrier is a placement tool. It can align two operations before a compare-and-update point, improving reproducibility over sleeps. It cannot force an exact scheduler interleaving after release, and instrumentation can alter timing.

Pair it with a causal oracle: exactly one conditional update succeeds, one durable row exists, a version increments once, or an invariant remains true. Bound every test wait so a defect yields a diagnostic instead of hanging CI. Timeout reports should include participant identities, generation, arrivals, and stacks.

## Definitions and Notation

For phase (g), let registered party set be (P_g), arrivals (A_g subseteq P_g), and unarrived set (U_g=P_g\A_g). Successful advance requires (U_g=empty). Broken flag (B_g) and terminated flag (T) define abnormal passage.

A latch has initial count (C_0=N) and current (C>=0), monotonically nonincreasing. Completion event (d_i) decrements at most once until zero.

For performance, participant arrival times are (t_i); release cannot precede (max_i t_i). Phase duration includes useful work, imbalance, arrival overhead, completion action, and wake cost.

## Mechanisms, Invariants, or Proof Structure

Use this workflow:

1. **Name each party and obligation.** Count logical participants, including coordinators.
2. **Choose one-shot, fixed, or dynamic membership.**
3. **Index generations.** Reject duplicate and cross-generation arrival.
4. **Publish before arriving.** Scope the data protected by the phase edge.
5. **Define abnormal fate.** Break, abort, contribute failure, or deregister.
6. **Bound actions and waits.** Use one monotonic deadline.
7. **Coordinate termination.** Keep fixed parties in identical phase order.
8. **Select topology.** Measure centralized versus hierarchical cost.
9. **Own lifecycle.** Prevent reset/destruction races.
10. **Test with oracles.** Force adverse schedules and assert state.

Maintain (A_g subseteq P_g); advance only on complete arrivals or explicit failure; one arrival per registered party per phase; latch count never increases or crosses below zero; every created obligation reaches one terminal countdown/arrival; phase data precedes successful consumption; deregistration atomically resolves current and future membership; one completion action outcome governs the generation; and no participant survives termination/destruction.

The executable model enumerates all order-preserving two-arrival histories for three parties and rejects any history in which a second-generation arrival precedes completion of generation one.

<!-- bijux-verify: {"id":"two-generation-barrier-histories","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"candidate_histories=90\nphase_safe_histories=36\nrejected_cross_generation=54\nparties=3\n","stderr":""}} -->
```python
parties = ("A", "B", "C")
histories = []


def extend(prefix, progress):
    if len(prefix) == 2 * len(parties):
        histories.append(tuple(prefix))
        return
    for party in parties:
        phase = progress[party]
        if phase < 2:
            progress[party] += 1
            extend(prefix + [(party, phase)], progress)
            progress[party] -= 1


extend([], {party: 0 for party in parties})
safe = 0
for history in histories:
    first_phase_arrivals = 0
    valid = True
    for _, phase in history:
        if phase == 0:
            first_phase_arrivals += 1
        elif first_phase_arrivals != len(parties):
            valid = False
    safe += int(valid)

print(f"candidate_histories={len(histories)}")
print(f"phase_safe_histories={safe}")
print(f"rejected_cross_generation={len(histories) - safe}")
print(f"parties={len(parties)}")
```

Limitations: this program enumerates a finite event order. It does not implement blocking, threads, wakeups, memory ordering, failure, dynamic registration, hierarchy, or a production barrier.

## Alternatives and Trade-Offs

**Structured join/futures** directly represent task completion and propagate results/failure; they are preferable for one parent awaiting child tasks.

**Latches** decouple countdown from waiting and suit one-shot gates, but duplicate/missing countdown can be hard to diagnose and reuse is invalid.

**Cyclic barriers** make fixed repeated rendezvous explicit and can run a phase action; one slow or failed party affects the group.

**Phasers** support evolving parties and arrival without waiting, at substantially greater membership and termination complexity.

**Queues/dataflow** release consumers when particular data is ready instead of globally synchronizing unrelated work.

**Asynchronous iterative algorithms** reduce barrier cost and straggler sensitivity but need convergence and consistency proofs under stale information.

**Tree/dissemination barriers** scale better than centralized counters while increasing topology, allocation, and failure complexity.

## Failure Modes and Misconceptions

- **“Count threads.”** Count logical parties and every coordinator that waits.
- **“Six arrivals cover two rounds.”** Generation identity, not totals, separates obligations.
- **“Timeout is private.”** A missing fixed party changes every peer's liveness.
- **“Countdown means success.”** It means a defined terminal obligation; report result separately.
- **“Reset repairs a barrier.”** Old waiters and state require coordinated epoch recovery.
- **“The action can do anything.”** It serializes the phase and its failure affects passage.
- **“A barrier prevents races.”** Pre-arrival writes still need ownership or synchronization.
- **“Dynamic registration is just increment.”** It must bind to a specified phase.
- **“Early exit is harmless.”** Fixed parties must execute matching phase sequences.
- **“More barriers improve determinism.”** Unnecessary global synchronization reduces scalability and can hide design defects.
- **“Observed counts control admission.”** Diagnostic snapshots race with state transitions.
- **“A local barrier coordinates replicas.”** Process failure and partitions require a distributed protocol.

## Worked Examples

### Example 1

**Question:** Four workers and the coordinator all call a barrier initialized to four.

**Reasoning:** Five logical parties arrive, so one crosses into the next generation or receives an invalid protocol outcome.

**Conclusion:** Initialize from actual participants, including the coordinator.

### Example 2

**Question:** A latch of three has two tasks succeed and one fail before countdown.

**Reasoning:** If countdown means terminal completion, the failed task still owes it; otherwise the waiter blocks forever.

**Conclusion:** Count down exactly once in terminal cleanup and publish failure separately.

### Example 3

**Question:** Worker A reaches phase two before C reaches phase one.

**Reasoning:** A reusable barrier must retain A at the first boundary; total future arrivals cannot repair early consumption.

**Conclusion:** Advance by generation completeness, not cumulative count.

### Example 4

**Question:** One cyclic-barrier waiter times out.

**Reasoning:** The remaining fixed parties can no longer complete that generation normally.

**Conclusion:** Apply the API's break/terminal propagation to every peer.

### Example 5

**Question:** A worker finishes early after phase seven in a fixed ten-phase loop.

**Reasoning:** Other parties wait for its phases eight through ten.

**Conclusion:** Coordinate global termination at a common boundary or atomically deregister from a suitable phaser.

### Example 6

**Question:** A parent spawns a child after other parties may close the phase.

**Reasoning:** Registration after closure either joins a later phase or misses the current obligation.

**Conclusion:** Register before publishing/spawning, or follow the API's phase-return protocol.

### Example 7

**Question:** The barrier action performs a remote request.

**Reasoning:** All parties remain delayed by unbounded network time, and action failure may break the generation.

**Conclusion:** Keep transition actions bounded; schedule remote effects after passage.

### Example 8

**Question:** What does the executable model prove?

**Reasoning:** Of 90 order-preserving histories, 36 place all three first-phase arrivals before any second-phase arrival; 54 violate that boundary.

**Conclusion:** It recomputes a finite phase-order property, not an implementation.

### Example 9

**Question:** A 128-core loop spends half its time at one centralized barrier.

**Reasoning:** load imbalance, shared-counter traffic, and wake cost dominate useful work.

**Conclusion:** reduce rendezvous frequency, rebalance work, or benchmark hierarchical/dataflow alternatives.

### Example 10

**Question:** Can a barrier alone approve synchronized commands in a radiation-therapy controller?

**Reasoning:** Arrival does not establish dose physics, device timing, sensor validity, fail-safe behavior, or certification.

**Conclusion:** No. Named authorized clinical, medical-physics, controls, hardware, real-time, functional-safety, verification, cybersecurity, human-factors, and regulatory reviewers must approve the real system. No external review is claimed.

## Cross-Program Connections

- **Algorithms:** iterative solvers, graph frontiers, reductions, and stencils create phase dependencies.
- **Operating systems:** parking, wake storms, scheduling, priority, and NUMA shape barrier cost.
- **Distributed systems:** replica barriers require durable membership, failure detectors, and consensus semantics.
- **Testing:** controlled rendezvous places actors near races but requires a logical oracle.
- **Formal methods:** generation invariants, monotonicity, temporal progress, and failure transitions support proofs.
- **Performance:** stragglers, skew, topology, completion actions, and synchronization frequency bound scaling.

## References

1. P. C. Yew, N. F. Tzeng, and D. H. Lawrie, “Distributing Hot-Spot Addressing in Large-Scale Multiprocessors,” *IEEE Transactions on Computers* 36(4), 1987.
2. J. M. Mellor-Crummey and M. L. Scott, “Algorithms for Scalable Synchronization on Shared-Memory Multiprocessors,” *ACM TOCS* 9(1), 1991, [doi:10.1145/103727.103729](https://doi.org/10.1145/103727.103729).
3. Jun Shirako et al., “Phasers: a Unified Deadlock-Free Construct for Collective and Point-to-Point Synchronization,” ICS 2008, [doi:10.1145/1375527.1375568](https://doi.org/10.1145/1375527.1375568).
4. IEEE and The Open Group, *POSIX.1-2024*, “pthread_barrier_wait,” [official specification](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_barrier_wait.html) (retrieved 2026-08-29).
5. Oracle, “CountDownLatch,” Java SE 26 API, [official API](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/util/concurrent/CountDownLatch.html) (retrieved 2026-08-29).
6. Oracle, “CyclicBarrier,” Java SE 26 API, [official API](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/util/concurrent/CyclicBarrier.html) (retrieved 2026-08-29).
7. Oracle, “Phaser,” Java SE 26 API, [official API](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/util/concurrent/Phaser.html) (retrieved 2026-08-29).
8. Rust Project, “Barrier,” Rust 1.98 standard library, [official API](https://doc.rust-lang.org/std/sync/struct.Barrier.html) (retrieved 2026-08-29).
9. Gregory R. Andrews, *Foundations of Multithreaded, Parallel, and Distributed Programming*, Addison-Wesley, 2000.
10. Maurice Herlihy et al., *The Art of Multiprocessor Programming*, second edition, Morgan Kaufmann, 2020.

## Exercises

### Exercise 1

Define barrier, latch, and phaser state and give one use for each.

### Exercise 2

Prove no second-phase arrival is admitted before all first-phase arrivals in the fixed model. Explain why a generation field is necessary.

### Exercise 3

Diagnose a five-worker loop where one worker exits early, one times out privately, and the completion action performs I/O.

### Exercise 4

Design a dynamically expanding computation whose child tasks participate in the current or next phase. Specify registration, terminal failure, deregistration, and memory visibility.

### Exercise 5

A flight-control simulation uses a barrier between sensor fusion and actuator calculation. State what chapter verification proves and what needs named review.

## Answers to the Exercises

### Answer 1

A fixed barrier stores generation (g), registered set (P_g), arrivals (A_g), and terminal state; it suits repeated timesteps with stable workers. A latch stores monotone count (C) and opens permanently at zero; it suits one coordinator awaiting a batch. A phaser stores phase plus dynamic registered/arrived/unarrived parties and termination; it suits recursive or evolving task sets. Selection follows obligation shape, not convenience.

### Answer 2

Base state has no arrivals in generation zero. Each legal phase-zero arrival adds one distinct party. A phase-one arrival is enabled only after the third distinct phase-zero arrival advances generation; therefore no legal trace contains phase one earlier. After advance, arrival state resets under a new generation identity. Without identity, reset count zero is indistinguishable from initial zero, and a delayed wake or arrival can be charged to the wrong round.

### Answer 3

Early exit removes required future arrivals and strands peers. Private timeout has the same group effect; it must break/abort the generation or use agreed deregistration. Remote I/O in the completion action makes every phase depend on unbounded latency and failure. Repair by deciding global termination at a shared boundary, propagating one terminal state to all waiters, using one monotonic deadline, and moving I/O after passage. Test unequal loops, timeout races, broken state, and shutdown.

### Answer 4

The parent acquires a scoped party token for each child before publishing or starting it. The registration operation determines its phase; the child never assumes. It publishes phase output before arrive. Normal completion uses arrive-and-deregister exactly once. Failure publishes a terminal result and either arrives/deregisters if the algorithm tolerates loss or atomically terminates the computation and wakes peers. Registration is rejected after termination. The coordinator advances only when current unarrived count is zero and consumes outputs through the API's documented synchronization edge.

### Answer 5

Internal verification can check generation invariants, 90-history counts, exactly-once arrival reasoning, cited API behavior, local links, examples, and exercises. It cannot establish sensor models, flight dynamics, actuator timing, numeric stability, hardware faults, fail-safe modes, operational hazards, certification, or deployment fitness. Named authorized aerospace systems, controls, numerical, hardware, real-time, functional-safety, verification, cybersecurity, human-factors, and certification reviewers must approve the real model, code, evidence, and use. This chapter claims no external review.
