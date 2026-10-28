---
module_id: DSE-067
program: Data Structures Engineering
level: 2
module_number: 67
title: ABA Avoidance
status: complete
last_verified: 2026-08-30
---

# ABA Avoidance

## One-Page Review

### Governing question

When does a successful compare-and-exchange prove that an observed concurrent state is still the same state, and how should engineers choose, prove, and operate an ABA-avoidance strategy without confusing bit equality, object identity, lifetime, and memory ordering?

### Essential definitions

- **ABA** occurs when a shared representation is observed as A, changes to another state, and later compares equal to A even though an algorithmically relevant change occurred.
- **value equality** means the compared bits/values match; **logical identity** means they denote the same incarnation and relevant state.
- An **incarnation** is one lifetime or logical generation of storage at an address/index.
- A **tag**, **stamp**, or **version** is metadata changed with a value so CAS compares a larger state.
- **wraparound** occurs when a finite version cycles to a previously used value.
- **reclamation** determines when retired storage may be destroyed or reused; delayed reuse can prevent pointer ABA within a protected interval.
- A **hazard pointer** announces nodes a participant may access or compare; reclamation excludes announced nodes.
- An **epoch/grace-period scheme** delays reuse until all relevant earlier readers have quiesced.
- **LL/SC** (load-linked/store-conditional) conditionally stores based on an implementation-defined reservation, not only equality of a loaded value.

### Central model, mechanism, or theorem

CAS answers “does the atomic object currently equal expected?” It does not answer “has nothing relevant happened since I observed expected?” The latter implication is valid only when the algorithm establishes a no-harmful-ABA invariant. A Treiber pop can read address A and `A.next=B`; peers can remove A and B, reuse A for another node, and restore address A. Pointer-only CAS may then install stale B and corrupt the new chain.

Avoidance strategies change the proof premise. A stamped state compares `(address,generation)` and rejects A@0 versus A@3, provided the stamp cannot wrap during the observation window. Hazard pointers or epochs prevent the old address from being reused while an observation remains eligible. Garbage collection preserves physical lifetime but not every logical no-return invariant. LL/SC may detect intervening stores within its reservation semantics, but reservations can fail spuriously and do not replace lifetime protection before dereference. Algorithm redesign can avoid depending on A's uninterrupted identity.

### Critical invariants

1. Every CAS expected value contains all state whose uninterrupted identity the transition assumes, or another protocol preserves it.
2. A dereferenced node remains alive and of the expected incarnation throughout the access window.
3. Retired storage is not reused until every stale observer that could act on it is excluded.
4. Each successful structural change advances the compared generation when stamping is used.
5. Tag width and wrap horizon exceed the maximum possible relevant changes during any observation window, or wrap is explicitly prevented.
6. Tag/address packing respects alignment, provenance, canonical-address, and atomic-width rules of the target.
7. Protection publication is followed by validation before dereference or CAS reliance.
8. Clearing protection cannot precede the final access that depends on it.
9. Memory ordering publishes content and protection correctly; it is not treated as identity evidence.
10. Thread exit, cancellation, allocator pools, shutdown, and stalled participants preserve the reuse invariant.

### Common failures

- Assuming successful CAS proves no intervening changes.
- Calling any A→B→A history harmful without identifying the stale inference.
- Adding a finite counter without calculating wrap exposure.
- Incrementing the stamp separately from the pointer.
- Packing tags into pointer bits without target-language and architecture authority.
- Believing sequential consistency, `volatile`, or acquire/release prevents ABA.
- Believing garbage collection inherently prevents logical ABA.
- Announcing a hazard after load and dereferencing without revalidation.
- Reusing a node through an unprotected pool or freelist.
- Claiming LL/SC eliminates lifetime/reclamation requirements.

### Compact example

Pop P observes `(A,0)` and caches successor B. Other operations remove A and B, reuse A with a different successor, and publish `(A,3)`. Pointer-only equality says A matches and would install stale B. A stamped CAS expecting `(A,0)` rejects `(A,3)`. A hazard protocol instead forbids reuse of A while P's validated hazard is active. Neither result proves safety after a finite tag wraps or if protection was published incorrectly.

### Connections

[DSE-065](065-lock-free-stack-structure-and-invariants.md) supplies the vulnerable stack schedule. [DSE-066](066-michael-scott-queues.md) supplies counted-pointer and dummy-node context. The [program roadmap](../ROADMAP.md) next develops hazard pointers and epochs in depth, then RCU and reclamation testing.

## Governing Question

How can an engineer prove that CAS equality preserves the logical identity and state assumptions of a nonblocking transition across arbitrary interference, storage reuse, finite version wrap, memory-model behavior, and lifecycle events?

## Why This Matters

Compare-and-exchange is attractive because it makes one conditional transition indivisible. The comparison is narrower than the reasoning often built on it. If code loads pointer A, reads fields from the pointed object, and later CASes A, success establishes only that the atomic pointer again contains equal bits. An allocator can reuse the same address for a new object; a node can move away and back between containers; a state machine can cycle to the same enum. The cached fields and intended transition may belong to an obsolete state.

ABA is therefore not synonymous with “the value changed twice.” It is harmful when an operation uses equality as evidence that some unstated invariant—identity, adjacency, ownership, version, membership, or contents—remained valid. Cyclic counters whose operation depends only on the current numeric value may tolerate A→B→A. A Treiber pop using cached `A.next` generally does not. Diagnosis starts by naming the invalid inference.

The issue couples algorithm design to memory management. Reclamation makes addresses reusable, and unsafe dereference can occur before the final CAS. A tag may make CAS reject a recycled address but does not keep the old object alive while reading it. A hazard pointer may keep an address unreused while protected, but its load-publish-validate sequence and record lifetime must be correct. Epochs can delay all reuse but retain memory behind stalled participants. Garbage collection keeps objects alive, yet nodes deliberately moved out and back can still produce logical ABA.

Production choices depend on atomic width, address representation, allocator behavior, participant count, maximum pause, update rate, shutdown, and memory bounds. “Use a counter” or “use hazard pointers” is not a design until these parameters and failure modes are proved and observed.

## Prerequisites and Retrieval

Retrieve atomic load, CAS success/failure semantics, release/acquire, linearizability, lock-free versus wait-free progress, singly linked structures, allocation/reuse, and integer wraparound. From [DSE-065](065-lock-free-stack-structure-and-invariants.md), retrieve the stale-next Treiber schedule and private/live/retired/reclaimable states. From [DSE-066](066-michael-scott-queues.md), retrieve consistent pointer observations, counted pointers, helping, and the separation between logical removal and physical reclamation.

Be able to state exactly what an operation reads before CAS and which facts it assumes at success. The repository verifier excludes runtime threading primitives, so the executable artifact below is a finite identity/version model rather than evidence about real atomics, allocation, or reclamation.

## Learning Objectives

After completing this module, you can:

1. distinguish benign value cycling from harmful ABA;
2. construct an ABA counterexample from an algorithm's stale inference;
3. separate bit equality, logical identity, lifetime, and visibility;
4. derive the protection provided by tagged/stamped state and its wrap bound;
5. explain how hazards, epochs, garbage collection, and LL/SC alter the proof;
6. design the load-publish-validate sequence for protected observations;
7. audit pointer tagging for atomic width, alignment, provenance, and portability;
8. diagnose freelist, pool, cancellation, shutdown, and thread-exit violations;
9. choose an avoidance strategy using progress, memory, and workload evidence; and
10. build bounded-model, wrap, reuse, memory-safety, and operational tests.

## Core Exposition

**Define the harmful inference.** Suppose an operation performs:

1. `observed = top`;
2. `successor = observed.next`;
3. later, `CAS(top, observed, successor)`.

The intended proof is usually: if top still equals observed, then observed is still the same live node with the same successor and membership. CAS provides only the equality premise. A valid algorithm must establish the rest through immutable identity/lifetime, version comparison, delayed reuse, or redesign.

An A→B→A cycle is benign when the transition's legality depends solely on the present value A and all effects are recomputed from current state. It is harmful when cached auxiliary state came from the earlier A incarnation. The word “ABA” should name that second case; otherwise it becomes a vague synonym for contention.

**Trace the classic stack failure.** Initial stack is A→B→C. P loads top A and caches B. Q pops A, then B. Q or an allocator reuses A and pushes it as A′→C (or another chain). Top bits again equal address A. P's pointer-only CAS succeeds and writes stale B. B may be retired, reused, or no longer part of the current stack, so the chain is corrupted. Sequential consistency would order every atomic event clearly and still permit this history.

The same pattern appears in freelists, object pools, linked queues, reference counts, descriptors, index-slot tables, cyclic state machines, and lock words. With indices, removal and slot reuse can reproduce the same integer. With small counters, wrap can reproduce the whole packed word.

**Use stamped state conditionally.** Replace compared pointer `p` with atomic pair `(p,v)`. Every successful structural modification writes a new version. P observes `(A,7)`; after removals/reuse, state `(A,10)` does not match. Java's `AtomicStampedReference`, for example, exposes an atomic reference-plus-integer stamp contract. Native implementations may use double-width CAS, an index and version packed into one word, or a descriptor.

Finite tags detect rather than metaphysically eliminate ABA. With `b` tag bits, the arithmetic period is `2^b` increments. Safety requires fewer than `2^b` relevant successful changes between an observation and its last possible use—or an independent mechanism preventing the same address/state from reappearing at wrap. A 16-bit tag can wrap quickly at high update rates; even 64 bits is a quantitative engineering assumption, not a proof of infinity. Saturating instead of wrapping needs a policy for exhausted state.

Tags must change on every transition relevant to the stale inference. Updating pointer then stamp separately exposes torn logical state. Atomic pair width must actually be supported or correctly emulated. Pointer-bit stealing depends on alignment and architecture address rules; language pointer provenance may forbid integer masking/forging patterns even if hardware appears to accept them. Version comparison does not protect dereference: P can fault reading A before it ever performs the rejecting CAS.

**Delay reuse with hazard pointers.** A participant loads candidate A, publishes A in its hazard slot, then reloads/validates the shared pointer. If it changed, clear or replace the hazard and retry without dereferencing. A remover unlinks nodes but retires them; reclamation scans active hazards and reuses only nodes absent from all relevant slots. While P holds a validated hazard A, address A cannot be recycled, so equality can denote the same incarnation for algorithms that are otherwise ABA-safe under garbage collection.

Ordering and lifecycle matter. Publishing too late leaves a load-to-announcement race. Clearing before the last dereference/CAS reopens reuse. A thread that exits with a hazard set can retain memory unless deregistration is safe. Hazard records, scans, retire thresholds, and allocator integration need bounded-resource and progress analysis. Hazard pointers do not prevent a logical node already protected from being moved out and back if the algorithm relies on membership rather than physical incarnation.

**Delay reuse with epochs or grace periods.** A reader announces participation in an epoch/read-side critical section before accessing candidates. Removed nodes are retired with an epoch and reused only after every participant that could have observed them reaches a later quiescent state. This can amortize protection overhead and works well when critical sections are short. A preempted, dead, or forgotten participant can retain arbitrary retired memory; forced quiescence must not violate readers.

Epoch safety is global and temporal: it prevents reuse of a whole retirement cohort. It does not by itself validate that the shared pointer still equals the loaded pointer before dereference if removal can make fields inaccessible by another mechanism. Exact rules depend on the scheme. DSE-068 develops hazards and epochs as reclamation protocols; here they are viewed through the identity premise they can supply.

**Understand garbage collection.** Tracing GC normally prevents an object reachable from P's local reference from being physically reclaimed and allocated as another object at the same identity. This often removes address-reuse ABA. It does not prove that a mutable node was not removed, modified, and reinserted while retaining its identity. Algorithms that move the same objects between lists can still suffer logical ABA. Managed references also do not make non-atomic fields, publication, or linearization correct.

**Understand LL/SC carefully.** A load-linked establishes a reservation and store-conditional succeeds only if the architecture considers it still valid. Intervening stores to the reservation granule normally invalidate it, so an A→B→A store sequence tends to make SC fail even when final bits equal. But reservation granules, context switches, exceptions, unrelated writes, maximum instruction windows, and spurious failures are architecture-specific. LL/SC helps conditional-update identity but does not keep an object alive after loading its address or authorize dereferencing reclaimed storage.

**Redesign to remove the dependency.** Sometimes the strongest solution is not to preserve identity. Re-read and recompute all dependent state immediately before CAS; use immutable descriptors; make updates idempotent; use monotone states that never return; use a lock around the compound invariant; or choose an algorithm whose CAS expected word includes all relevant state. A lock can be more portable and auditable than a double-width atomic plus custom reclamation. Absence of ABA is not the same as lock-freedom, and avoiding CAS does not automatically remove stale-state races.

**Separate memory order from version order.** Release/acquire answers which writes become visible. A stamp answers whether the compared logical generation matches. Reclamation answers whether access remains valid. Linearizability answers whether operations admit a legal point history. Progress answers who completes. All five are needed in many lock-free objects, and none substitutes for another.

For example, a release CAS can publish `(A,8)` correctly but an undersized tag may wrap. A 128-bit stamped CAS can reject an old state while P already dereferenced freed A. A perfect epoch can preserve A's storage while a relaxed load fails to observe initialized fields. Proofs should have distinct lemmas for these concerns.

**Design protection ownership.** Document who acquires a hazard/epoch slot, whether operations can nest, what happens on exceptions/cancellation, and how thread-local records are released. State whether callbacks may retain pointers beyond protection, whether nodes can migrate between structures, and whether object destruction waits for all participants. Pooling must pass through the same retire/reuse gate; a private “fast freelist” can silently defeat the public reclamation proof.

**Quantify the tag horizon.** Let update rate be at most `r` relevant changes per second and maximum observation lifetime be `T` seconds. A simple necessary no-wrap condition is `rT < 2^b`, with margins for burst rate, paused threads, clock-independent execution, and shared use across structures. If `T` is unbounded because a thread may be suspended indefinitely, no finite `b` alone proves safety. Either bound/cancel observations safely or pair tags with delayed reuse/indirection.

The condition is not a performance estimate; it is a proof obligation. Measurement can estimate rates but cannot guarantee an adversarial maximum unless admission/resource bounds enforce it. Generation wrap tests should deliberately use tiny tags and controlled pauses rather than waiting years for production-width counters.

**Use a bounded model honestly.** The executable model reproduces a stale pointer and successor. Three structural changes bring address A back with stamp 3 and new successor null. Pointer-only comparison accepts; stamped comparison rejects; an active hazard would forbid A's reuse. It also reports the four-value period of a two-bit tag.

<!-- bijux-verify: {"id":"aba-identity-and-stamp-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"observed=A@0\ncurrent=A@3\npointer_only_match=True\nstamped_match=False\nstale_desired=B\ncurrent_next=None\ntag_bits=2\nwrap_period=4\nhazard_blocks_reuse=True\nall_invariants=True\nevidence=finite_aba_identity_model\n","stderr":""}} -->
```python
class TaggedTop:
    def __init__(self, address, stamp):
        self.address = address
        self.stamp = stamp

    def pointer_matches(self, expected_address):
        return self.address == expected_address

    def stamped_matches(self, expected):
        return (self.address, self.stamp) == expected

    def change(self, address):
        self.address = address
        self.stamp += 1


next_of = {"A": "B", "B": None}
top = TaggedTop("A", 0)
observed = (top.address, top.stamp)
stale_desired = next_of["A"]

top.change("B")       # Pop the first incarnation of A.
top.change(None)      # Pop B.
next_of["A"] = None  # Reuse address A for a different incarnation.
top.change("A")      # Publish the new A incarnation.

pointer_only_match = top.pointer_matches(observed[0])
stamped_match = top.stamped_matches(observed)
hazards = {"A"}
hazard_blocks_reuse = "A" in hazards
tag_bits = 2
wrap_period = 2 ** tag_bits
all_invariants = (
    pointer_only_match
    and not stamped_match
    and stale_desired == "B"
    and next_of["A"] is None
    and hazard_blocks_reuse
    and wrap_period == 4
)

print(f"observed={observed[0]}@{observed[1]}")
print(f"current={top.address}@{top.stamp}")
print(f"pointer_only_match={pointer_only_match}")
print(f"stamped_match={stamped_match}")
print(f"stale_desired={stale_desired}")
print(f"current_next={next_of['A']}")
print(f"tag_bits={tag_bits}")
print(f"wrap_period={wrap_period}")
print(f"hazard_blocks_reuse={hazard_blocks_reuse}")
print(f"all_invariants={all_invariants}")
print("evidence=finite_aba_identity_model")
```

The model assigns method calls indivisible effects, represents protection as a set, and never executes the corrupting pointer-only CAS. It verifies only this finite arithmetic/state trace. It does not run threads, allocate or free memory, implement atomics or hazards, explore wrap schedules, prove ordering, progress, reclamation, or performance.

**Verify in layers.** Start with sequential identity/ownership and reuse tests. Construct deterministic schedules that pause after load, field read, protection publication, validation, and before CAS. Force address/index reuse with a controlled allocator. Run tiny tag widths through wrap; test epoch/hazard thread exit, cancellation, nested operations, record exhaustion, and shutdown. Record histories and check linearizability, while race/sanitizer/model tools target lifetime and memory order.

Measure maximum and percentile observation lifetime, update/burst rate, CAS retries, hazard publications/validations, retire-list size, scan cost, epoch lag, unreclaimed bytes, tag-wrap distance, and per-thread starvation. Test under preemption, oversubscription, NUMA, allocator pressure, signals/panics, and maliciously stalled participants. No stress duration alone proves a finite tag cannot wrap in a longer or adversarial execution.

## Definitions and Notation

Let shared atomic representation be `X`. Operation P observes `a_0=X(t_0)` and later attempts a transition at `t_3`. An ABA history has `X(t_0)=A`, some `t_1<t_2` with `X(t_1)≠A`, and `X(t_2)=A`. It is **harmful** if P's transition uses a predicate `I` derived at or after `t_0` that is not guaranteed at `t_3` despite equality.

For pointers, write `A^i` for address A's incarnation `i`. Pointer comparison may report `A^i = A^j` at the bit level even when `i≠j`. Tagged representation is `(A,v)` with `v` incremented modulo `M=2^b`. No-wrap premise over one observation interval is `changes < M`; an engineering rate bound can be written `rT < M` only when `r` and `T` are enforced maxima.

Node lifecycle is allocated/private `P`, reachable `L`, retired `R`, reclaimable `C`, reused as new incarnation `P'`. A protection scheme must prevent `R→C→P'` while a qualified observer can dereference or compare the old incarnation.

`HP_p` is participant p's hazard set. A validated protected observation of A requires publish `A∈HP_p`, then reload/validate the shared source still identifies A, before dependent access. `E_p` is an epoch announcement; a grace period excludes readers whose earlier observations could reach retired nodes.

## Mechanisms, Invariants, or Proof Structure

### Harmful-ABA proof obligation

1. Enumerate every fact cached between load and conditional update.
2. Identify which facts CAS equality actually establishes.
3. Construct an intervening history returning the compared representation.
4. If a cached fact can differ, demonstrate the illegal transition or result.
5. Select a mechanism that makes equality imply the required fact or recompute the fact.

### Stamped-state proof

1. Read pointer and generation atomically as one expected state.
2. Change the generation on every relevant successful state transition.
3. CAS both fields atomically; separate updates are insufficient.
4. Prove no generation wrap can reproduce expected during an observation window.
5. Separately prove dereference lifetime, publication, atomic support, and representation legality.

### Delayed-reuse proof

1. Enter protection before relying on a candidate's lifetime.
2. Publish the candidate, then validate its source to close the race.
3. Keep protection until the last dependent read/CAS completes.
4. Retire on removal; reuse only after all qualifying observers are excluded.
5. Prove cancellation, thread exit, nesting, record exhaustion, and destruction preserve the protocol.

### Evidence ladder

1. Sequential ownership and incarnation specification.
2. Minimal stale-field ABA counterexample and legal-history review.
3. Bounded state model comparing pointer, stamp, and reuse protection.
4. Tiny-tag exhaustive wrap and forced allocator-reuse schedules.
5. Target memory-order, provenance, sanitizer, race, and model-checker evidence.
6. Hazard/epoch lifecycle, stalled participant, exhaustion, and shutdown faults.
7. Production-shaped update-rate, observation-lifetime, retry, retention, and fairness telemetry.

## Alternatives and Trade-Offs

| Strategy | What it establishes | Main advantage | Principal obligation/cost |
|---|---|---|---|
| Mutex/serialization | no concurrent compound transition | simplest identity/lifetime proof | blocking and convoying |
| Wide pointer + tag | detects generation mismatch | direct CAS integration | width, wrap, packing, dereference |
| Index + generation | stable packed handle | compact arenas, validation | slot lifecycle and wrap |
| Hazard pointers | protected nodes cannot be reused | precise native lifetime | publication/validation and scans |
| Epoch reclamation | cohort reuse waits for grace period | amortized fast reads | stalled readers retain memory |
| Tracing GC | reachable object not physically reused | simpler address lifetime | logical ABA and GC behavior remain |
| Reference counting | delays destruction while referenced | local ownership visibility | safe acquisition, cycles, atomic traffic |
| LL/SC | conditional store detects reservation loss | avoids equality-only CAS issue | architecture windows/spurious failure |
| Immutable descriptor | unique operation/state identity | compositional helping | allocation and descriptor reclamation |
| Recompute/redesign | removes stale dependency | may avoid metadata | extra reads or different algorithm |

Selection should start from the exact stale inference and progress/lifetime requirements. A tag is attractive when wide atomic support and strict observation bounds exist. Hazards fit few protected pointers and require precise reuse. Epochs fit short read sections and tolerate delayed bulk reclamation. A mutex is often superior when blocking is acceptable and object lifecycle is complex.

## Failure Modes and Misconceptions

- **“ABA means any value changed and returned.”** Harm requires an invalid stale-state inference.
- **“CAS success means unchanged.”** It means equal now under the CAS comparison rule.
- **“A large counter cannot wrap.”** It can; safety needs an enforced horizon or another invariant.
- **“The counter can update after the pointer.”** Separate updates expose states the proof does not cover.
- **“Pointer tagging is free space.”** Alignment, provenance, canonical addressing, sanitizers, and future platforms constrain it.
- **“A tag keeps the node alive.”** It can reject the final CAS after an earlier use-after-free.
- **“Sequential consistency prevents ABA.”** A fully ordered A→B→A history remains legal.
- **“Acquire/release proves identity.”** It orders visibility; it does not prevent incarnation reuse.
- **“GC always prevents ABA.”** The same live logical node can leave, mutate, and return.
- **“Hazard load then publish is safe.”** Publication must be followed by source validation before dereference.
- **“Epochs reclaim promptly.”** A stalled participant may retain unbounded retired storage.
- **“LL/SC is a portable drop-in CAS.”** Reservation behavior, windows, and availability are architecture-specific.
- **“A freelist is outside the proof.”** Reuse through any allocator/pool is exactly where address ABA enters.
- **“Stress testing establishes no-wrap.”** Sampling cannot prove a universal counter horizon.
- **“Solving ABA makes the structure correct.”** linearization, visibility, lifetime, progress, lifecycle, and capacity remain.

## Worked Examples

### Example 1

**Situation.** A cyclic state counter moves 0→1→0, and an operation wants only to increment the current value.

**Reasoning.** If the operation recomputes desired from the current 0 and no cached identity/state matters, the cycle can be benign. Calling it harmful ABA without an invalid inference adds no diagnosis.

**Conclusion.** Define the stale dependency before selecting an ABA remedy.

### Example 2

**Situation.** Treiber pop P caches `A.next=B`; peers remove A/B and reuse address A with `A.next=C`.

**Reasoning.** Pointer-only top equality accepts A, but P would install stale B instead of C. The cached adjacency belongs to an old incarnation.

**Conclusion.** Address equality does not establish node identity or immutable adjacency across reuse.

### Example 3

**Situation.** The top is `(A,41)` and three changes return the address as `(A,44)`.

**Reasoning.** CAS expecting the whole pair rejects. CAS comparing only A succeeds. The stamp works because every relevant change advanced it and no wrap occurred.

**Conclusion.** Atomic comparison must include the version whose invariant the proof uses.

### Example 4

**Situation.** A 2-bit stamp begins 0 and four relevant changes occur while P pauses.

**Reasoning.** Versions are 1,2,3,0; the complete stamped representation can repeat. With an unbounded pause, no finite tag alone excludes recurrence.

**Conclusion.** Tag width is a quantified proof parameter, not decorative metadata.

### Example 5

**Situation.** P loads A, Q removes and frees A, then P publishes hazard A and dereferences it.

**Reasoning.** The hazard arrived after reclamation. Correct P publishes after load, reloads the shared pointer, and accesses only if it still identifies A; otherwise it retries.

**Conclusion.** Hazard protection requires a load-publish-validate loop.

### Example 6

**Situation.** Managed objects A and B move between two live stacks; A leaves top and later returns unchanged in identity.

**Reasoning.** GC keeps A alive, but a pop that cached A's old successor can still be wrong after membership and links change.

**Conclusion.** GC prevents many address-reuse schedules, not every logical ABA schedule.

### Example 7

**Situation.** An epoch participant is suspended for an hour while peers retire millions of nodes.

**Reasoning.** Structural operations may remain lock-free, but the old epoch cannot reach grace; memory retention grows. Forced deregistration is unsafe unless the participant cannot resume/access protected nodes.

**Conclusion.** Reclamation progress and operation progress require separate bounds and telemetry.

### Example 8

**Situation.** A design packs a 16-bit tag into the high bits of a 64-bit pointer because current test machines ignore them.

**Reasoning.** Other architectures, address-width modes, language provenance, sanitizers, and future allocators may reject or reinterpret the pointer. The atomic word may also lack portable lock-free operations.

**Conclusion.** Tagged-pointer layout needs explicit target authority and fallback.

### Example 9

**Situation.** Close frees a pool after active-operation count reaches zero, but a cancelled thread still has a hazard record referencing a pool node.

**Reasoning.** Active-call count and protection lifetime diverged. Destruction must retire/deregister records under a protocol that proves no thread can resume a dependent access.

**Conclusion.** Lifecycle accounting must cover protection ownership, not only API calls.

### Example 10

**Situation.** A 64-bit tag passed a week-long stress run at average 10 million updates/second.

**Reasoning.** The run supports observed behavior but neither bounds burst rate nor maximum paused observation, and it does not test wrap. Use tiny-tag model tests plus enforced production bounds or delayed reuse.

**Conclusion.** Empirical longevity cannot replace a no-wrap or no-reuse proof.

## Cross-Program Connections

- **Concurrent and Parallel Programming:** CAS/LL-SC semantics, memory order, progress, hazard pointers, epochs, and model checking define the execution substrate.
- **Systems Programming:** pointer provenance, allocator reuse, ownership, unsafe dereference, panic cleanup, and target atomic widths govern soundness.
- **Operating Systems:** preemption, context switches, reservation granules, signals, and thread teardown affect observation and grace periods.
- **Security Engineering:** use-after-free, counter wrap, forged/tagged pointers, resource-retention attacks, and adversarial pauses are security boundaries.
- **Database Engineering:** generation numbers, slot reuse, transaction IDs, and optimistic validation exhibit analogous wrap and stale-identity hazards.
- **Distributed Systems:** fencing tokens prevent stale owners from acting after lease turnover; like stamps, finite tokens need monotonicity and scope.

## References

1. Maged M. Michael and Michael L. Scott, [“Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms”](https://www.cs.rochester.edu/u/scott/papers/1996_PODC_queues.pdf), PODC 1996. Primary counted-pointer and ABA discussion in a practical lock-free object.
2. Maged M. Michael, [“Hazard Pointers: Safe Memory Reclamation for Lock-Free Objects”](https://www.eecg.utoronto.ca/~amza/ece1747h/papers/hazard_pointers.pdf), *IEEE TPDS* 15(6), 2004. Primary ABA definition, GC qualification, hazard method, and reclamation proof.
3. R. Kent Treiber, [“Systems Programming: Coping with Parallelism”](https://books.google.com/books/about/Systems_Programming_Coping_with_Parallel.html?id=YQg3HAAACAAJ), IBM Research Report RJ 5118, 1986. Bibliographic record for the foundational CAS stack/free-list context.
4. Maurice P. Herlihy and Jeannette M. Wing, [“Linearizability: A Correctness Condition for Concurrent Objects”](https://www.cs.cmu.edu/~wing/publications/HerlihyWing90.pdf), *ACM TOPLAS* 12(3), 1990. Primary correctness framework.
5. Oracle, [`AtomicStampedReference`](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/util/concurrent/atomic/AtomicStampedReference.html), Java SE 26, accessed 2026-08-30. Official atomic reference-plus-integer-stamp contract.
6. Rust Project, [`AtomicPtr::compare_exchange`](https://doc.rust-lang.org/std/sync/atomic/struct.Atomic.html#method.compare_exchange), Rust 1.98 documentation, accessed 2026-08-30. Official pointer-equality/identity and ABA warning plus ordering rules.
7. ISO C++ working draft, [Atomics clause](https://eel.is/c++draft/atomics), current draft accessed 2026-08-30. Primary compare-exchange, atomic width, and memory-order specification.
8. Keir Fraser, [“Practical Lock-Freedom”](https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-579.pdf), University of Cambridge Technical Report UCAM-CL-TR-579, 2004. Primary epoch-based reclamation, descriptors, and practical nonblocking design account.

## Exercises

### Exercise 1

Define harmful ABA, value equality, logical identity, incarnation, stamp, wraparound, retirement, reclamation, hazard pointer, epoch, and LL/SC. State the no-harmful-ABA proof obligation.

### Exercise 2

Trace a Treiber stack A→B→C where P caches A/B, Q pops A and B, reuses A as A′→C, and P attempts its old CAS. Compare pointer-only, `(pointer,tag)`, and validated-hazard outcomes.

### Exercise 3

A packed handle uses a 12-bit generation. Relevant transitions are bounded at 500,000 per second and a participant may pause for 20 ms. Compute the simple horizon check, then identify assumptions that still prevent it from being a complete proof.

### Exercise 4

Design an ABA-safe native object pool for a lock-free stack. Specify protection acquisition, validation, retirement, reuse, thread exit, cancellation, pool shutdown, memory bounds, and the scope of the progress claim.

### Exercise 5

An unfamiliar platform offers pointer CAS and LL/SC but no double-width lock-free CAS. Choose an avoidance approach for a highly contended queue and provide a portability, verification, benchmark, and rollout plan.

## Answers to the Exercises

### Answer 1

Harmful ABA is an A→different→equal-A history in which an operation treats present equality as proof that cached identity/state remained valid and therefore makes an illegal transition. Value equality compares representation; logical identity denotes the same relevant object/state; an incarnation is one allocation/logical generation. A stamp changes with state; wrap returns finite metadata to an old value. Retirement removes reachability; reclamation permits destruction/reuse. A hazard announces protected nodes; an epoch delays cohort reuse until prior readers quiesce. LL/SC makes a conditional store depend on a reservation rather than equality alone.

The proof must enumerate cached facts, show that CAS equality plus the selected version/lifetime protocol implies every fact at the update point, preserve dereference lifetime, and cover all reuse paths, wrap, memory ordering, cancellation, thread exit, and destruction.

### Answer 2

P reads top A and `next=B`. Q CASes top A→B, then B→C, retires both, reinitializes address A as A′ with next C, and pushes it so top bits are A again. Pointer-only `CAS(top,A,B)` can succeed and installs stale/retired B, corrupting A′→C. With tags, P observed `(A,0)` while the current state has a later generation; the whole-pair CAS rejects unless the finite tag wrapped.

With hazards, P loads A, publishes hazard A, then validates top still A before reading B. Q may logically pop A, but cannot reclaim/reuse address A while P's validated hazard remains. P's CAS then either succeeds against the same incarnation before removal or fails after Q's update; it cannot see a recycled A. This assumes the algorithm is otherwise ABA-safe under nonreuse, hazards cover every dependent node, and P clears protection only after its final access.

### Answer 3

The arithmetic period is `2^12=4096`. The stated maximum changes during 20 ms are `500,000 × 0.020 = 10,000`, which exceeds 4096, so the simple no-wrap condition fails even without safety margin. The tag can complete more than two cycles during one allowed pause.

Even if the arithmetic passed, a proof would need enforced—not average—burst rate and pause bounds, a guarantee that every relevant transition increments the generation atomically with the handle, correct modulo semantics, no reset/copy/restore paths, legal packing and atomic support, safe node dereference before CAS, memory ordering, and lifecycle behavior. Use more bits plus enforced bounds, or delayed reuse/indirection/redesign rather than relying on the 12-bit tag.

### Answer 4

Give each participating thread registered hazard slots. A pop loads top, publishes the candidate, reloads/validates top, then safely reads next; failure updates/clears protection and retries. Successful CAS transfers ownership and retires the old node into a per-thread/global retire list. Scans collect active hazards and return only absent retired nodes to the pool. A push receives a reclaimed/private node, initializes it fully, and publishes with release ordering; consumers acquire before field use.

Cancellation handlers clear hazards only after dependent access ends and retire any unpublished/private node appropriately. Thread exit transfers retire lists and safely deregisters cleared records; abandoned live hazards cannot simply be erased if code may resume. Pool shutdown stops admission, waits for active operations/protections, drains/disposes stack nodes, performs final scans/grace, and frees records only at quiescence. Bound records, retire thresholds, scan work, pool capacity, and exhaustion policy. The structural CAS loop may be lock-free with preallocated nodes and a lock-free hazard implementation; allocation, exhaustion waiting, scans, shutdown, and reclamation completion need their own progress claims.

### Answer 5

Prefer a published single-word-CAS queue combined with hazard pointers or an epoch scheme if participant/quiescence assumptions fit; this avoids nonportable packed double-width state and supplies dereference lifetime as well as address-reuse prevention. LL/SC may implement the structural conditional transition on targets where reservation constraints are satisfied, but retain the reclamation scheme and a CAS fallback. If strict memory bounds and locality dominate, evaluate a bounded sequence-number ring instead; if blocking is acceptable, keep a mutex/two-lock queue as the baseline.

Document target atomic and LL/SC guarantees, pointer provenance, allocator reuse, tag/sequence wrap, hazard/epoch lifecycle, and fallback feature detection. Verify forced reuse, every pause boundary, tiny-counter wrap, history linearizability, race/sanitizer/model checks, stalled participants, cancellation, thread exit, close, and memory exhaustion. Benchmark realistic producer/consumer imbalance, NUMA, allocation, retry/reservation failures, protection/scan cost, retired bytes, tails, and fairness against the lock baseline. Canary behind one API, monitor correctness counters and retention, retain rollback, and reject rollout for any history, memory, lifecycle, portability, tail, or bounded-resource regression.
