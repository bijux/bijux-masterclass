---
module_id: CONPAR-054
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 54
title: ABA Problems and Tagged References
status: complete
last_verified: 2026-08-29
---

# ABA Problems and Tagged References

## One-Page Review

### Governing question

When does an atomic comparison of equal representations fail to establish that shared state has remained unchanged, and which combination of versions, reservations, lifetime protection, and API design makes the intended history distinction valid?

### Essential definitions

- **ABA** is a history in which an observer reads representation A, other operations change it to B and back to A, and the observer incorrectly treats final equality as evidence of no relevant intervening change.
- A **stale observation** is a value and any derived facts retained while other operations may advance the shared state.
- **Pointer ABA** reuses the same address or reference representation for a different object generation; **logical ABA** cycles a value while history still matters even without reclamation.
- A **tagged reference** is one atomically observed and updated pair `(reference, tag)` whose tag changes on every relevant transition.
- **Tag wrap** occurs when a finite tag returns to an earlier bit pattern; a stale pair can then become equal again.
- **Lifetime safety** ensures that an object remains valid while it may be dereferenced; **change detection** determines whether a compared state has changed. Neither implies the other.
- **Delayed reuse** prevents an address or identifier from being reassigned while a stale observation can remain live.
- **load-reserved/store-conditional (LR/SC)** conditionally stores according to a reservation invalidated by relevant writes, subject to an architecture's reservation and progress rules.
- A **counted pointer** or **versioned state** atomically couples payload identity with a generation, counter, or state-machine revision.
- A **fencing token** lets a downstream authority reject an older actor; it is a distributed analogue of generation validation, not a memory-reclamation mechanism.

### Central model, mechanism, or theorem

CAS proves only that the compared representation equals the expected representation at the atomic event. It does not prove that no intervening transition occurred. If correctness depends on history, extend the compared state with a generation that changes on every relevant transition, and atomically compare the whole pair. This prevents a stale update only while no live observation can survive enough transitions for the finite generation to wrap. Separately, protect object lifetime before dereference or delay reuse until stale observations are impossible. A valid design states both the history-discrimination argument and the lifetime argument.

### Critical invariants

Every transition that can invalidate derived state advances the compared generation. Reference and generation are read and CASed as one atomic value. No stale observation survives a full tag cycle, or reuse is delayed until it cannot. A successful CAS uses only data derived from the exact pair it compares. Failure refreshes the entire snapshot. Tags are not silently truncated, torn, independently loaded, or stored in noncanonical pointer bits. A thread dereferences only a protected live object. Retirement precedes reclamation; reclamation precedes reuse. Cancellation after a successful CAS reports commitment. Target atomics provide the required width and progress rather than hidden locking.

### Common failures

Code compares only the pointer; increments the tag only on some transitions; loads pointer and tag separately; assumes 16 bits can never wrap; uses wall-clock time as a generation; packs bits without proving alignment, address width, provenance, or canonical form; treats garbage collection as protection from logical ABA; treats a tag as permission to dereference freed storage; protects after dereference; uses an atomic pair that falls back to a lock while claiming lock-freedom; assumes every LR/SC has ideal semantics or eventual success; retries with a stale successor; resets generations on restart; or lets cancellation contradict a committed update.

### Compact example

P1 reads stack head `(A,7)` and derives successor B. P2 removes A, changes the head twice, and later reuses address A, producing `(A,9)`. Pointer-only CAS sees A and may install stale B. Pair CAS expecting `(A,7)` rejects `(A,9)`. P1 must refresh both fields and re-establish lifetime protection. The tag detects this history only because updates advanced it atomically and 9 did not wrap to 7.

### Connections

[Compare-and-Swap Loops](026-compare-and-swap-loops.md) supplies witness refresh. [Implementing a Lock-Free Stack](052-implementing-a-lock-free-stack.md) and [Lock-Free Queues](053-lock-free-queues.md) provide concrete ABA sites. The next modules develop hazard-pointer and epoch reclamation protocols.

## Governing Question

How should an engineer recognize, prove, prevent, test, and operate against ABA without confusing bit-pattern equality, object identity, object lifetime, and abstract history?

ABA is not merely “the value changed twice.” The problem exists only when an algorithm infers a property it needs—usually unchanged identity or validity—from representation equality that does not establish that property.

## Why This Matters

Compare-and-swap makes a precise promise: at one atomic instant, compare the stored representation with an expected representation and, if equal, replace it. That promise is powerful but narrower than “nothing happened since I looked.” Lock-free stacks, queues, freelists, allocators, reference counters, state machines, work registries, and device rings can all retain facts derived from an old observation. If the compared representation cycles, a stale transition can appear current.

Pointer reuse is especially dangerous: one address can denote a later object generation after deallocation and allocation. Managed memory removes some physical reuse traces while a reference remains strongly reachable, but logical state can still cycle. Remedies alter layout, atomic width, memory management, progress, portability, and shutdown, so the response must be a layered proof.

## Prerequisites and Retrieval

Retrieve:

- linearization and safety/liveness distinctions from [Safety, Liveness, and Progress](004-safety-liveness-and-progress.md);
- atomic read-modify-write semantics from [Atomic Read-Modify-Write Operations](025-atomic-read-modify-write-operations.md);
- compare-exchange witness refresh from [Compare-and-Swap Loops](026-compare-and-swap-loops.md);
- publication ordering from [Acquire and Release Ordering](027-acquire-and-release-ordering.md);
- source-versus-hardware reasoning from [Reasoning About a Weak-Memory Program](030-reasoning-about-a-weak-memory-program.md);
- commitment-aware cancellation from [Cancellation and Timeouts](036-cancellation-and-timeouts.md); and
- concrete stale-successor histories from [Implementing a Lock-Free Stack](052-implementing-a-lock-free-stack.md) and [Lock-Free Queues](053-lock-free-queues.md).

Retrieval prompt: write the states seen by a paused stack pop while another thread removes two nodes and reuses the first address. Identify separately the invalid cached successor, the lifetime violation, and the CAS equality that fails to detect history.

## Learning Objectives

After completing this module, a learner can:

1. define ABA as a failed history inference rather than any repeated value;
2. distinguish representation equality, logical identity, generation, and lifetime;
3. construct pointer and logical ABA counterexamples with linearization events;
4. derive a tagged-reference invariant and quantify its finite-wrap assumption;
5. audit whether a pointer/tag pair is truly atomic and lock-free on a target;
6. explain why tags, hazard pointers, epochs, garbage collection, and LR/SC solve different obligations;
7. design retry, cancellation, restart, and shutdown semantics for versioned state;
8. test forced reuse, wraparound, stale snapshots, and weak-memory behaviors;
9. evaluate packed, double-width, indirection, delayed-reuse, and lock-based alternatives; and
10. transfer generation reasoning to handles, leases, devices, and high-stakes control.

## Core Exposition

### Equality is not history

Let an atomic location `X` hold a representation from set `R`. A caller reads `a`, computes proposal `d(a)`, and later executes `CAS(X,a,d(a))`. A successful CAS proves `X=a` at the CAS event. It does not prove that `X` continuously equaled `a` since the read. The missing property is temporal, whereas CAS compares current representations.

An A→B→A cycle is harmless when the algorithm needs only current value. Incrementing an integer from zero with a refreshed CAS loop is not wrong merely because another operation temporarily changed zero. ABA becomes a defect when `d(a)` contains facts invalidated by an intervening transition: a cached successor, ownership assumption, reference count, free-list link, state-machine authorization, or generation-specific resource.

This yields an audit question: what proposition does equality stand for? If the proposition is “the value is currently A,” equality suffices. If it is “this is the same object generation and none of the transitions that invalidate my proposal occurred,” the representation must encode or the protocol must otherwise establish that stronger fact.

### Pointer ABA in a Treiber stack

Suppose P1 reads head address A and reads `A.next=B`. It pauses. P2 pops A, pops B, retires both, and eventually storage at address A is reused for new node C. P2 pushes C, so head again contains address A. P1's pointer-only CAS expects A and desires cached B. It can succeed, disconnecting C and possibly installing a node no longer in the stack.

There are two independent failures. P1 may have dereferenced A after its lifetime ended, which is already invalid in manual-memory languages. Even if an artificial model keeps every node allocated forever, reusing a logical identity and retaining stale `B` can corrupt the abstract stack. Fixing comparison does not retroactively make the dereference valid; fixing lifetime without preventing the relevant history may still permit logical ABA.

### Logical ABA without reclamation

Consider a state machine with atomic state `AVAILABLE`. P1 reads available and prepares a transition whose payload assumes no intervening ownership. P2 changes it to `OWNED`, performs a generation-specific action, then releases it to `AVAILABLE`. If P1's proposal must not cross an intervening ownership epoch, a CAS from available can be semantically stale even though no memory was freed.

### Tagged references

A tagged reference stores `T=(p,g)`, where `p` is a reference-like payload and `g` is a generation. An operation reads the pair atomically, derives its proposal from both fields, and CASes the whole expected pair to `(p',next(g))`. Every transition that invalidates a retained proposal advances `g`, including transitions that leave `p` unchanged when their history matters.

In the stack trace, P1 expects `(A,7)`. Later reuse produces `(A,9)`, so equality fails. The failure is an ordinary retry: discard every value derived from generation 7, acquire a new snapshot, re-establish protection, and recompute. Comparing A separately from 7 is insufficient because a torn combination may never have existed.

Java 21's `AtomicStampedReference` exposes an atomic reference/stamp pair. Its finite integer and caller-defined updates do not prove a compound data structure correct.

### Finite tags and wraparound

A tag of `k` bits has `M=2^k` representations. If one relevant transition increments modulo M, an expected tag can recur after M transitions. Prevention therefore requires an assumption such as: while any observation remains live, fewer than M relevant advances can occur; or the corresponding reference cannot recur within that window; or an additional protection protocol prevents reuse until the observation ends.

At transition rate `r` per second, the shortest idealized wrap time is `M/r`. With 16 bits at one million transitions per second, `65,536 / 1,000,000 = 0.065536` seconds. Even a 32-bit tag wraps in about 4,294.967296 seconds, roughly 71.58 minutes, at that rate. These calculations are not reliability proofs: bursts, pauses, restart, per-location rate, and attacker influence matter.

Use specified unsigned modular arithmetic. “Practically impossible” requires quantified observation lifetime, transition rate, and consequences; a stopped thread can otherwise make lifetime unbounded.

### Atomic representation and target qualification

The pointer and tag must fit an atomic representation with the required semantics. Double-width CAS availability and lock-free status vary by ISA, ABI, compiler, alignment, and runtime. A library lock can preserve safety while invalidating lock-free progress.

Pointer packing steals alignment or address bits. Its proof must cover allocation alignment, address width, canonical form, authentication/tagging, sanitizers, provenance, and future targets. Integer round trips are not automatically portable; the whole packed word still needs atomic comparison.

Indirection compares immutable descriptor identity, but descriptors still require lifetime and non-reuse. It moves rather than erases the problem.

### Lifetime protection and delayed reuse

Before dereferencing a possibly removable node, a thread needs a lifetime protocol. Hazard pointers publish the observed pointer and validate that the root still matches before dereference; reclamation waits until no hazard protects a retired node. Epoch schemes prevent reuse of retired objects until all earlier read-side participants have quiesced. Garbage collection keeps strongly reachable objects live under its runtime semantics.

These protocols can suppress pointer ABA by delaying reuse beyond stale observations. Hazard publication/validation and scans still matter; a nonquiescent epoch participant trades reuse safety for retained memory.

Conversely, a tag can reject a stale CAS yet leave an earlier dereference illegal. Correct order is generally protect, validate, dereference, compute, compare-and-update, then retire/reclaim according to the protocol. The exact sequence depends on the algorithm. The next two modules make those reclamation proofs explicit.

### LR/SC and reservations

Load-reserved/store-conditional offers a different abstraction. LR reads and establishes a reservation; SC stores only if the reservation remains valid. RISC-V's atomic extension notes that LR/SC avoids the value-comparison ABA issue by monitoring writes rather than merely comparing the final value. That statement is scoped to the architecture's defined reservation behavior.

Real LR/SC is not an ideal history oracle. Reservation granules and invalidation permit failures; progress requires constrained-loop conditions or an equivalent guarantee. Success does not protect a pointee from reclamation.

### Memory ordering and retry discipline

Versioning is orthogonal to visibility. A release update may publish initialized payload; an acquiring observer may consume it. Relaxed ordering can be sufficient for the generation itself only when a complete happens-before proof covers dependent data. Sequential consistency does not prevent ABA when the representation lacks history.

On CAS failure, APIs such as C++ compare-exchange commonly replace the expected argument with the observed current representation. Refresh all derived state. Do not update only the tag while retaining an old successor or payload pointer. Weak CAS can fail spuriously; a loop must distinguish retry from externally visible failure and avoid repeating non-idempotent effects.

Advance generation in the same atomic update. Separate locations permit mixed snapshots unless another protocol proves consistency; seqlocks have different writer, retry, and wrap assumptions.

### Progress, contention, and performance

Adding bits can change the primitive. Check lock-free support on every target and inspect generated code where material. Wide CAS, descriptors, hazard scans, and epoch stalls add cache, allocation, tail, or space costs.

Tags do not improve starvation freedom. Backoff changes latency and may block. A mutex can be faster, easier to prove, and support explicit fairness.

Benchmark actual operation mix, reuse, topology, allocator, and pauses. Record failures, wrap margin, retirement backlog, per-thread latency, and fallback; throughput can conceal starvation or retained memory.

### Lifecycle, cancellation, and restart

Generation belongs to lifecycle. Resetting while stale actors survive reintroduces equality. Shared-memory peers, devices, persistent structures, or remote workers may outlive restart, so persist the epoch or replace object identity.

Before successful CAS, cancellation may abandon a private proposal and release its protection. After successful CAS, the transition committed; returning “cancelled with no effect” is false. Cleanup may require a compensating versioned transition. Shutdown closes admission, waits for operations that may hold observations, drains retirement, and only then destroys atomic state and storage.

Distributed fencing is analogous: after accepting token 43, a resource authority must reject token 42. Checking a lease service before writing leaves a race; enforcement must survive failover.

### Verification strategy

Begin with a model that forces A→B→A, finite wrap, and independent pointer/tag loads. The counterexample should disappear only under the stated generation and lifetime constraints.

For native code, combine deterministic schedule hooks, aggressive address reuse, sanitizers, model checking, and weak-memory tools. A test allocator that immediately recycles one address makes rare ABA reproducible. Verify the protection-before-dereference order separately from CAS rejection. Exercise thread pause, death, deregistration, cancellation, close, and shutdown.

Stress tests are empirical, not proof. Monitor observation age, update rate, tag headroom, CAS/reservation failures, retired bytes, stalled participants, and atomic fallback.

## Definitions and Notation

- `X`: the atomic compared location.
- `a`: an expected representation previously read from `X`.
- `d(a)`: a desired representation derived from observation `a`.
- `A→B→A`: at least two relevant transitions whose final representation equals the initial representation.
- `T=(p,g)`: tagged state containing reference/payload `p` and generation `g`.
- `M=2^k`: number of distinct tags for an unsigned `k`-bit generation.
- `next(g)=(g+1) mod M`: modular successor when finite wrap is explicit.
- `O`: maximum duration for which a stale observation may remain live.
- `r`: maximum relevant transition rate for the same compared location.
- `R`: reuse delay before one reference representation may denote a later generation.
- **relevant transition**: any transition that can invalidate facts derived from an observation.
- **retired**: removed from the abstract data structure but not necessarily reclaimable.
- **reclaimed**: storage may be freed or reused because no valid observer can access it.

A simple sufficient no-wrap condition under strict bounds is `r·O < M`; real proofs also cover bursts, integer rounding, restart, attacker control, and whether every relevant transition advances the tag. Delayed reuse instead aims for `R > O` for the protected representation, with protocol-specific definitions of both quantities.

## Mechanisms, Invariants, or Proof Structure

### Counterexample structure

1. P1 atomically reads state A and derives fact F.
2. P1 pauses without committing.
3. Other operations perform relevant transitions A→B→A that invalidate F.
4. P1 compares only A, succeeds, and applies a proposal whose proof depended on F.
5. Exhibit the violated representation, ownership, or abstract-state invariant.

Without steps 3–5, repeated values alone do not establish an ABA defect.

### Tagged-state safety argument

Assume every relevant transition atomically changes `(p,g)` and advances `g`; no live observation spans M advances; pair reads and CAS are atomic; failed CAS refreshes all derived data; and any dereference is independently lifetime-safe. Suppose P1 retains `(p,g)`. An intervening relevant transition changes the generation. Before M transitions, the generation cannot equal g again, so P1's pair CAS cannot accept the later state. If no relevant transition occurred, its proposal remains valid by the algorithm-specific invariant. Thus the tag rules out the stipulated stale-success case, not every possible algorithm defect.

### Obligation matrix

| Claim | Required evidence |
|---|---|
| History detection | every invalidating transition advances one atomically compared generation |
| No wrap while stale | quantified transition/observation bound or delayed reuse/protection argument |
| Lifetime safety | hazard, epoch, GC, ownership, or quiescence proof before dereference |
| Publication | source-language happens-before argument for payload fields |
| Linearizability | operation-specific abstract transition at successful CAS/observation |
| Lock-freedom | primitive, allocation, protection, reclamation, and target fallback progress |
| Restart safety | identity/generation continuity across every surviving observer |
| Operational safety | monitors and limits tied to proof assumptions |

### Executable finite model

The following sequential model is intentionally small. It demonstrates why pointer-only equality accepts A after a cycle, why a tag rejects the same short history, and why a two-bit tag can eventually wrap. It does not execute concurrent atomics, dereference memory, or prove a reclamation scheme.

<!-- bijux-verify: {"id":"aba-tag-and-wrap-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"plain_stale_accepts=True\ntagged_stale_accepts=False\nwrapped_pair=('A', 1)\nwrapped_stale_accepts=True\ntransitions_to_wrap=4\n","stderr":""}} -->
```python
plain_expected = "A"
plain_current = "A"
plain_current = "B"
plain_current = "A"

bits = 2
modulus = 2 ** bits
tagged_expected = ("A", 1)
tagged_current = tagged_expected
tagged_current = ("B", (tagged_current[1] + 1) % modulus)
tagged_current = ("A", (tagged_current[1] + 1) % modulus)
short_history = tagged_current

transitions = 2
while tagged_current != tagged_expected:
    next_pointer = "B" if tagged_current[0] == "A" else "A"
    tagged_current = (next_pointer, (tagged_current[1] + 1) % modulus)
    transitions += 1

print(f"plain_stale_accepts={plain_current == plain_expected}")
print(f"tagged_stale_accepts={short_history == tagged_expected}")
print(f"wrapped_pair={tagged_current}")
print(f"wrapped_stale_accepts={tagged_current == tagged_expected}")
print(f"transitions_to_wrap={transitions}")
```

## Alternatives and Trade-Offs

| Approach | What it establishes | Principal cost or limitation |
|---|---|---|
| Wide tagged CAS | detects relevant cycles before wrap | width/alignment/lock-free availability; finite counter |
| Packed pointer/tag | single-word comparison | few bits; provenance, canonical-address, portability risk |
| Hazard pointers | protects named objects and delays reuse | publication/scan cost; slots, registration, thresholds |
| Epoch reclamation | delays reuse across read-side epochs | stalled participants retain memory; lifecycle complexity |
| Garbage collection | keeps reachable objects live | logical ABA remains; collector/runtime costs |
| LR/SC | reservation detects relevant writes under ISA rules | spurious failure, reservation constraints, target dependence |
| Immutable descriptor | compares unique operation/state identity | allocation and descriptor reclamation |
| Never reuse until quiescence | simple identity argument | potentially unbounded memory and long shutdown |
| Mutex-protected state | serializes history and lifetime policy | blocking, convoying, priority/failure considerations |
| Redesign current-value semantics | makes cycles harmless | may change API or algorithm; requires new proof |

The strongest design is often not the most elaborate primitive. If the object can be placed behind a mutex with acceptable latency, the reduction in proof surface may dominate. If nonblocking progress is required, select a mature algorithm whose tagged representation and reclaimer are verified together on the target.

## Failure Modes and Misconceptions

- **“CAS means unchanged.”** It means equal at comparison, not unchanged throughout the interval.
- **“A tag solves use-after-free.”** A tag may reject CAS after an illegal dereference; lifetime needed protection earlier.
- **“A lifetime scheme eliminates all ABA.”** It can prevent address reuse while observed, but logical state may still cycle.
- **“Sixty-four bits never wrap.”** It is a risk statement requiring explicit rate, observation, restart, and consequence bounds.
- **“Incrementing most of the time is enough.”** One unversioned invalidating transition creates an indistinguishable history.
- **“Two atomic fields form an atomic pair.”** Independent atomicity permits mixed observations unless another validation protocol exists.
- **“Unused pointer bits are portable storage.”** Alignment, address width, provenance, authentication, and tooling can invalidate the scheme.
- **“Wide atomic means lock-free.”** The implementation may use a lock; query and qualify target support.
- **“LR/SC is ideal LL/SC.”** Real reservation granules, failure causes, loop restrictions, and progress rules apply.
- **“A failed CAS can retain cached links.”** All values derived from the failed expected state require revalidation.
- **“Managed memory removes ABA.”** It helps lifetime, but reference/state cycles can remain logically relevant.
- **“Restart resets the world.”** Shared-memory peers, devices, persistent data, and remote actors may retain stale generations.
- **“Cancelled means not committed.”** After the atomic transition, cancellation cannot erase history; report or compensate.

## Worked Examples

### Example 1

**A harmless cycle.**

**Situation.** An atomic gauge currently reads 10. P1 plans to display whatever value exists at its final load. P2 changes 10→11→10. Is this ABA corruption?

**Reasoning.** P1's contract depends only on current value, not continuous history. It performs a final atomic load and displays 10. No cached successor, ownership, or generation-specific effect is applied. The cycle is real but no required proposition was inferred from its absence.

**Conclusion.** Repetition is not enough; ABA is harmful only when equality is used as evidence for an invalidated historical fact.

### Example 2

**Treiber stack stale successor.**

**Situation.** P1 reads head A and `A.next=B`. P2 pops A and B, then pushes a new node at reused address A. P1 CASes head from A to cached B.

**Reasoning.** Pointer equality succeeds, but the new A is a different generation and B is no longer the successor of current head. P1 can remove the new node and install stale state. If nodes were freed, P1's read may also be a lifetime violation. A tag rejects the later A only if it advanced and did not wrap; lifetime still needs protection.

**Conclusion.** The history violates both change-detection and potentially lifetime obligations; repair them separately.

### Example 3

**Tagged short history.**

**Situation.** P1 observes `(A,12)`. Competitors change it to `(B,13)` and `(A,14)`. P1 proposes an update expecting `(A,12)`.

**Reasoning.** The pointer field matches, but the atomic pair does not. CAS fails and returns/permits loading `(A,14)`. P1 discards every generation-12-derived link, renews lifetime protection, and recomputes. Merely changing expected tag to 14 while keeping cached data would be wrong.

**Conclusion.** Atomic pair comparison converts the short ABA into a normal stale-snapshot retry.

### Example 4

**Quantifying tag wrap.**

**Situation.** A freelist uses a 16-bit tag and can advance one million times per second while a thread may pause for 100 milliseconds.

**Reasoning.** The tag space is 65,536. Idealized wrap time is 65.536 ms, less than the 100 ms pause. The bound `r·O = 100,000` exceeds M. A stale pair can recur, even before considering bursts or a stopped thread. More bits, bounded pauses, delayed reuse, or another scheme is required.

**Conclusion.** The proposed tag width does not establish the no-wrap assumption.

### Example 5

**Torn pointer and tag reads.**

**Situation.** Pointer and generation occupy separate atomics. P1 reads pointer A; P2 changes `(A,5)` to `(B,6)`; P1 then reads generation 6 and records `(A,6)`.

**Reasoning.** Each load is atomic, yet the combined snapshot never existed. A later validation can accept or reject for reasons unrelated to a coherent state. The design needs a single atomic pair or a proven snapshot protocol such as a sequence counter with retry and its own wrap/liveness rules.

**Conclusion.** Component atomicity is not snapshot atomicity.

### Example 6

**Tag rejection after illegal access.**

**Situation.** P1 reads address A, pauses, then dereferences `A.next`; only afterward it CASes `(A,4)` and sees that current state is `(A,6)`.

**Reasoning.** The tag successfully rejects the update, but A may have been reclaimed before the dereference. A later failed CAS cannot legalize an earlier access. A hazard-pointer outline publishes A, revalidates the root, and only then dereferences; the tag remains useful for history if needed.

**Conclusion.** Change detection at commit does not supply pre-commit lifetime safety.

### Example 7

**Wide atomic fallback.**

**Situation.** A C++ implementation stores a 64-bit pointer plus 64-bit counter in a 128-bit atomic. Tests pass on two machines, and the team calls the structure lock-free.

**Reasoning.** Safety may hold if the library implements atomicity with a hidden lock. Progress does not. The team must check alignment, `is_lock_free`/`is_always_lock_free`, compiler flags, runtime library, and every deployment target. A signal interruption or priority-sensitive system makes hidden locking material.

**Conclusion.** Atomic correctness and nonblocking progress are different target-qualified claims.

### Example 8

**LR/SC retry.**

**Situation.** An LR reads A, another hart writes B then A, and SC fails because the reservation was invalidated. A later SC also fails spuriously.

**Reasoning.** The first failure detects intervening write history despite final A. The second failure commits nothing and is safe if the loop refreshes. Liveness depends on the ISA's reservation and constrained-loop progress conditions. Any pointee accessed inside the sequence still needs valid lifetime.

**Conclusion.** LR/SC can avoid comparison ABA under its specified reservation model, but it is neither failure-free nor a reclaimer.

### Example 9

**Versioned cancellation and restart.**

**Situation.** A worker CASes `(READY,81)` to `(RUNNING,82)`, then observes cancellation. A process restart would normally initialize the counter to zero while an external device can still submit completion 82.

**Reasoning.** The worker must report committed-running or perform a compensating transition; it cannot truthfully report no effect. Resetting to zero may eventually collide with old actors and destroys ordering. Persist a monotonic epoch or replace the resource identity, and require the device authority to reject old epochs.

**Conclusion.** Versions participate in commitment and lifecycle; they are not transient debugging metadata.

### Example 10

**Infusion-pump command generation.**

**Situation.** A controller sends pump commands with an 8-bit generation. A failover controller can issue 300 updates while a delayed network path retains an old command. Can the team claim the tag prevents stale dosage commands?

**Reasoning.** No. Eight bits wrap after 256 advances, so the delayed command can share a current generation. Safety requires a system hazard analysis; durable nonrepeating session identity plus sufficiently wide monotonic sequence; authenticated binding of identity, command, and device; authoritative rejection at the pump; explicit failover/restart behavior; bounded replay storage; and tests forcing wrap, delay, duplication, loss, and power interruption. Human clinical, embedded, security, and regulatory reviewers must approve requirements and evidence. The model does not validate dosage logic or certify a device.

**Conclusion.** Small tags are inadequate for high-stakes stale-command prevention; use end-to-end generation authority and named human review.

## Cross-Program Connections

- **Programming languages and semantics:** ABA separates value equality from contextual or historical equivalence; source lifetime rules can forbid executions hardware appears to tolerate.
- **Algorithms:** tagged state changes the state space and proof invariant; finite wrap turns an unbounded proof into a bounded assumption.
- **Distributed systems:** lease epochs and fencing tokens reject stale actors only when the resource authority enforces them.
- **Databases:** optimistic concurrency versions detect stale writes; resetting or comparing incomplete versions recreates logical ABA.
- **Security:** replay resistance similarly binds actions to fresh sessions/nonces, but cryptographic authenticity and threat models add obligations beyond atomicity.
- **Safety engineering:** tag width and observation duration are hazard assumptions requiring human review, monitoring, and fail-safe response.

## References

1. Maged M. Michael, “ABA Prevention Using Single-Word Instructions,” IBM Research Report RC23089, 2004. <https://dominoweb.draco.res.ibm.com/4813d7c4e4c6b1a085256e2b00539e0f.html>
2. R. Kent Treiber, “Systems Programming: Coping with Parallelism,” IBM Research Report RJ 5118, 1986. <https://dominoweb.draco.res.ibm.com/58319a2ed2b1078985257003004617ef.html>
3. Maurice Herlihy and Jeannette Wing, “Linearizability: A Correctness Condition for Concurrent Objects,” *ACM TOPLAS* 12(3), 1990. <https://doi.org/10.1145/78969.78972>
4. Maged M. Michael, “Hazard Pointers: Safe Memory Reclamation for Lock-Free Objects,” *IEEE TPDS* 15(6), 2004. <https://doi.org/10.1109/TPDS.2004.8>
5. Trevor Brown, “Reclaiming Memory for Lock-Free Data Structures: There Has to Be a Better Way,” PODC 2015. <https://doi.org/10.1145/2767386.2767436>
6. ISO C++ working draft, “Atomic operations” and compare-exchange semantics, continuously maintained; retrieved 2026-08-29. <https://eel.is/c++draft/atomics>
7. Oracle, Java SE 21 API, `AtomicStampedReference`, retrieved 2026-08-29. <https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/atomic/AtomicStampedReference.html>
8. Rust Project, standard library `AtomicPtr` documentation, retrieved 2026-08-29. <https://doc.rust-lang.org/std/sync/atomic/type.AtomicPtr.html>
9. RISC-V International, *The RISC-V Instruction Set Manual, Volume I*, “A” extension for atomic instructions, current ratified specification; retrieved 2026-08-29. <https://docs.riscv.org/reference/isa/unpriv/a-st-ext.html>
10. Keir Fraser, *Practical Lock-Freedom*, PhD dissertation, University of Cambridge, 2004. <https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-579.pdf>

## Exercises

### Exercise 1

State the precise extra proposition that a pointer-only CAS fails to prove in a harmful ABA history. Why is a harmless A→B→A gauge cycle different?

### Exercise 2

A location uses a 24-bit modular tag, advances at at most 250,000 relevant transitions per second, and observations can remain live for 40 seconds. Test the simple `r·O < M` condition and interpret the result.

### Exercise 3

Audit this outline: load pointer; dereference `next`; load tag; CAS the pair; on failure, replace only the expected tag and retry. Identify at least four defects and give a corrected obligation sequence.

### Exercise 4

Choose between a 128-bit tagged CAS, packed pointer, hazard pointers, epoch reclamation, and a mutex for a portable plugin registry with rare writes, frequent reads, dynamically unloaded plugins, and no hard nonblocking requirement. Defend a design and verification plan.

### Exercise 5

An autonomous rail controller assigns movement-authority revisions modulo 65,536. Controllers can restart, radios can replay delayed messages, and trackside equipment may be offline for days. Design an unfamiliar-transfer review that prevents stale authority from becoming current after wrap or restart. State what can be automated and what requires named human review.

## Answers to the Exercises

### Answer 1

Pointer-only equality proves only that the current representation equals the expected pointer at CAS. The missing proposition is that it denotes the same relevant object generation and that no intervening transition invalidated the proposal's derived facts. The gauge reader needs only the current value at its final observation; it applies no history-dependent proposal. Therefore the same cycle is observable but harmless under that contract.

### Answer 2

`M=2^24=16,777,216`. The maximum advances during one observation are `r·O=250,000·40=10,000,000`, which is less than M, leaving 6,777,216 transitions of arithmetic margin. The simple condition passes under strict bounds. A real proof must ensure the rate is per same location, includes bursts and adversarial updates, bounds every pause including crashes, advances the tag on every relevant transition, and preserves generation across restart. Monitoring must alarm before assumptions fail.

### Answer 3

First, dereference occurs before lifetime protection and can access reclaimed storage. Second, separate pointer/tag loads may form a pair that never existed. Third, a failed CAS invalidates pointer-derived `next`, not just the tag. Fourth, the outline says nothing about tag wrap, atomic pair width, memory ordering, or target lock-free support. A corrected sequence obtains one coherent pair, publishes lifetime protection, revalidates the pair, dereferences only then, derives the proposal, CASes the entire pair with proper orders, and on failure discards all derived state and protection before retry. Retirement/reclamation, generation advance, wrap bounds, cancellation, and shutdown are separately specified.

### Answer 4

A mutex plus immutable/owned registry snapshots is the default choice: writes are rare, no nonblocking requirement exists, and dynamic unload makes lifetime the central hazard. The mutex serializes mutation and unload; readers can either hold a read lock or acquire a reference-counted immutable snapshot whose plugin code/data cannot unload until the reference drains. This avoids pointer packing and target-dependent wide atomics. Verify lock ordering, callback re-entry, unload quiescence, cancellation, shutdown, reference ownership, and old-snapshot behavior; use deterministic race tests and sanitizers. Benchmark read latency before considering a more complex scheme. Hazard/epoch designs are justified only by measured contention and must include plugin execution lifetime, not merely registry-node lifetime.

### Answer 5

Use a durable, nonreused infrastructure/session identity plus a sufficiently wide monotonic authority sequence, cryptographically bind both to route, limits, issuer, recipient, and expiry, and make trackside equipment the authority that rejects any identity/sequence not newer than its durable high-water state. Failover must obtain a fenced epoch from durable consensus; restart cannot reset it. Define offline expiry and a fail-safe state rather than accepting wrapped ambiguity. Automated evidence includes model checking reordering/duplication/loss/wrap, persistence and power-cut tests, protocol parsing, authentication tests, simulated long partitions, and high-water invariant monitoring. Named railway signaling, safety, embedded, security, operations, and regulatory reviewers must approve the hazard analysis, sequence bounds, fail-safe behavior, deployment target, test coverage, and residual risk. No chapter model or automated test certifies movement authority.
