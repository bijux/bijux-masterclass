---
module_id: DSE-065
program: Data Structures Engineering
level: 2
module_number: 65
title: Lock-Free Stack Structure and Invariants
status: complete
last_verified: 2026-08-30
---

# Lock-Free Stack Structure and Invariants

## One-Page Review

### Governing question

Under what assumptions does a Treiber-style compare-and-exchange loop implement a linearizable lock-free stack, and which publication, failure-order, ABA, reclamation, progress, capacity, and operational obligations remain outside the elegant two-operation pseudocode?

### Essential definitions

- A **stack** is a last-in, first-out abstract sequence with push and pop operations.
- **compare-and-exchange** (CAS) atomically compares a shared word with an expected value and, on equality, replaces it with a desired value while reporting success/failure.
- A **Treiber stack** represents the sequence as an immutable-next singly linked chain whose top pointer is changed by CAS loops.
- A **linearization point** is the successful top CAS for push or successful nonempty pop; an empty pop linearizes at a validated/acquire observation of null.
- **lock-free** means that in an infinite system execution, operations complete system-wide; one particular operation can starve.
- **wait-free** means each operation completes in a bounded number of its own steps under the model.
- **spurious failure** is permitted by weak CAS even when the compared values match; callers must retry correctly.
- **safe publication** makes a privately initialized node's payload and next link visible before another thread follows the published pointer.
- **ABA** occurs when a compared value changes from A to something else and back to an equal-looking A, hiding intervening identity/state changes.
- **retirement** removes a node from the structure; **reclamation** permits its storage to be reused or destroyed after no reader can access it.

### Central model, mechanism, or theorem

For push of private initialized node `n`, repeatedly load top `t`, set immutable `n.next=t`, and CAS top from `t` to `n`. The successful CAS linearizes push; a failure means top differed (or weak CAS failed spuriously), so retry with a current observation. For pop, acquire-load `t`; if null, return empty at that observation. Otherwise, while `t` is lifetime-safe, read `u=t.next` and CAS top from `t` to `u`. Success linearizes removal and returns `t`'s value only after ownership/lifetime rules permit it.

Assuming genuine atomic top operations, correct memory ordering, immutable next links while reachable, no harmful ABA, and safe reclamation, the successful CAS order yields a legal LIFO history. For strong CAS, every failure caused by a changed top witnesses some successful interfering top modification; persistent failure therefore entails system progress. Weak-CAS spurious failures require a proof that the primitive/loop still meets the claimed progress model. This proves neither wait-freedom nor bounded latency.

### Critical invariants

1. Top is null or points to one live, fully initialized reachable node.
2. Following immutable next links from top yields one finite acyclic chain with no node repeated.
3. The abstract stack sequence is exactly the payload sequence along that chain from top downward.
4. Only successful atomic top transitions publish or remove nodes from the abstract stack.
5. A node being pushed is privately owned until publication; failed attempts do not create multiple reachable copies.
6. A pop may dereference its observed top only while a reclamation protocol guarantees the node remains alive.
7. Success ordering publishes initialization and pop acquisition observes it under the target memory model.
8. CAS failure reloads or consumes the actual current top correctly; stale desired links are recomputed.
9. A popped node/value is returned or reclaimed by exactly one winning operation under the ownership contract.
10. Capacity, allocation, retry/backoff, shutdown, bulk observation, and reclamation pressure have explicit policy and evidence.

### Common failures

- Reading top and assigning a new top with separate non-atomic operations.
- Publishing a node before initializing payload and next.
- Reusing a failed push candidate's stale next pointer without recomputing it.
- Dereferencing `top.next` after another pop has freed top.
- Assuming pointer equality proves the same node instance after an ABA cycle.
- Using a release-only pop CAS and then reading payload without an acquire path.
- Choosing an invalid failure memory order or treating a failed CAS as a write.
- Calling the algorithm wait-free because each uncontended operation uses one CAS.
- Returning empty based on an unsynchronized/stale observation outside the language contract.
- Ignoring allocator locks, callbacks/destructors, unbounded retries, hot-top contention, and retired-memory growth.

### Compact example

A finite CAS schedule models two pushes that race from empty: node 2 wins, node 1 fails then retries above 2. A pop observes node 1, but push 3 wins first, so the pop fails, retries, and removes 3. Final stack is `[1,2]`; four CAS operations succeed and two fail. The executable checks reachability/acyclicity but runs no threads, atomics, memory model, ABA, or reclamation.

### Connections

[DSE-016](016-stacks.md) supplies the sequential LIFO specification. [DSE-062](062-fine-grained-locking.md) supplies linearization and lifetime framing. [DSE-064](064-concurrent-skip-lists.md) supplies marking/helping/progress distinctions. The [program roadmap](../ROADMAP.md) next studies Michael–Scott queues, ABA avoidance, hazard pointers, epoch reclamation, and linearizability testing.

## Governing Question

Can one atomic top pointer, immutable node links, and retrying CAS implement a production-credible linearizable lock-free stack once the memory model, node ownership, ABA, reclamation, progress, capacity, failure, and measurement assumptions are made explicit?

## Why This Matters

The Treiber stack is the smallest important nonblocking linked structure. Its algorithm fits on a slide, yet a correct native implementation depends on nearly every hard shared-memory topic: CAS semantics, release/acquire publication, linearization, progress classes, spurious failure, ABA, lifetime, allocator behavior, and adversarial contention. It is therefore a diagnostic instrument for concurrency reasoning.

Stacks appear in freelists, pools, schedulers, work transfer, graph traversal, undo state, runtimes, and internal caches. A lock-free stack can avoid blocking behind a preempted mutex holder and can perform well when top contention is moderate. It also funnels every operation through one cache line. Under heavy contention, repeated failed CAS and coherence traffic can produce poor tails and unfairness. Elimination or combining can spread complementary push/pop traffic, but changes proof and complexity.

The abstract algorithm is not memory management. A pop reads a pointer and then `next`; another pop can remove and reclaim that node between those actions. A garbage-collected environment may keep the object alive but still faces logical ABA if nodes are reused or mutable links change. Native systems need hazard pointers, epochs, reference/lifetime schemes, tagged pointers, or another verified design. DSE-067 through DSE-070 develop these mechanisms; this module must expose the dependency rather than pretending `delete` follows CAS.

Language atomics are not interchangeable syntax. CAS often accepts success and failure orderings with restrictions. Release on successful push publishes prior initialization. Pop needs acquisition before consuming node fields, frequently through acquire load or acquire/acq_rel success. Failure semantics determine what observation can seed retry. Sequential consistency is a conservative starting point, not a substitute for lifetime or ABA reasoning; weaker orders require a target-language proof and tests.

Finally, “lock-free” is a formal progress property, not a performance adjective. It allows starvation and says nothing about deadlines, fairness, allocation, page faults, signals, callbacks, or the reclamation subsystem unless included in the model. Production adoption requires both proof and workload evidence.

## Prerequisites and Retrieval

Retrieve [DSE-016](016-stacks.md): abstract sequence `S`, `push(x)` yielding `x::S`, and `pop()` returning/removing the head or empty. Retrieve singly linked nodes, ownership, data races, atomic read-modify-write, release/acquire, linearizability, lock-free versus wait-free progress, finite histories, allocator lifetime, and percentile latency.

From [DSE-061](061-thread-safe-wrappers-and-coarse-grained-locks.md), retrieve the correct coarse baseline. From [DSE-062](062-fine-grained-locking.md), retrieve operation-specific points and logical-removal/reclamation separation. From [DSE-064](064-concurrent-skip-lists.md), retrieve CAS retry, helping, ABA, and progress-evidence cautions. Understand that the repository's executable verifier intentionally excludes runtime threading primitives, so the artifact below is a bounded state model rather than concurrent-runtime evidence.

## Learning Objectives

After completing this module, you can:

1. derive Treiber push and pop from the sequential stack specification;
2. identify linearization points for successful push, nonempty pop, and empty pop;
3. prove chain, ownership, uniqueness, and LIFO invariants under stated assumptions;
4. explain why failed strong CAS can witness system progress;
5. distinguish lock-free, wait-free, starvation-free, and fast in practice;
6. choose and justify target-language publication/acquisition orderings;
7. diagnose spurious failure, stale desired values, ABA, and use-after-free;
8. integrate a reclamation dependency without claiming it is solved by CAS;
9. design capacity, shutdown, bulk, allocator, and overload policy; and
10. build history, memory, progress, fault, and workload evidence.

## Core Exposition

**Specify the sequential object.** Abstract state is a finite sequence `S`. `push(x)` changes `S` to `x::S` and returns according to API policy. `pop()` on `x::S` returns `x` and changes state to `S`; on empty it returns an absence result and leaves state unchanged. Define whether null values are permitted, whether pop blocks, timeout/cancellation, ownership transfer, maximum capacity, close behavior, and bulk/snapshot operations.

Treiber's usual stack is nonblocking and empty pop returns immediately; it is not a blocking stack with a condition. Adding `wait_pop` requires a separate notification/wait protocol that cannot miss wakeups. `size` and iteration are not inherent. An exact snapshot cannot be constructed by independently popping/reading without changing semantics or adding versioning/wider synchronization.

**Represent one immutable chain.** Each heap node stores payload and `next`. Shared `top` is atomic. Before publication, the pushing thread exclusively owns a node and may set both fields. Once reachable, `next` remains immutable in the basic algorithm; only top changes. This makes every successful top transition replace one chain prefix:

- push: `T → N → T` in representation terms—new top `N` whose next is prior chain `T`;
- pop: `N → T` changes top from `N` to `T`, logically removing exactly `N`.

Immutability is conditional on node identity/lifetime. Recycling a popped node and changing its next while an old reader retains it violates the premise unless reclamation/ABA defenses exclude that reader.

**Derive push.** Allocate/initialize private node `n` with payload. Load top into `observed`. Set `n.next = observed`. Attempt CAS `(top, observed, n)`. On success, release semantics make preceding initialization visible to a reader that acquires this publication, and push linearizes. On failure, top is no longer the expected state or weak CAS failed spuriously. Update/reload `observed`, reset `n.next`, and retry.

The desired link must be recomputed. Suppose push A prepared `A.next=null`; push B then installed B. If A retries CAS against B but leaves `A.next=null`, it discards B on success. Correct retry sets `A.next=B`. A private candidate may be reused across attempts because no other thread can see it until success, but allocator/cancellation cleanup must dispose it if push aborts.

**Derive pop.** Acquire-load `observed=top`. If null, return empty; that acquire observation is the empty operation's candidate point. Otherwise protect/pin `observed` before dereferencing, and validate that top still equals it according to the reclamation protocol. Read `next=observed.next`. CAS top from observed to next. On failure, release the protection as required, take the returned/current top or reload, and retry. On success, the CAS linearizes removal; transfer payload ownership and retire the node. Do not immediately reclaim unless the lifetime protocol permits it.

The ordering must make node fields visible before they are read. A common shape is release CAS for push, acquire load for pop, and acq_rel or acquire-on-success where pop's successful RMW also participates in other ordering. Exact choices depend on language, reclamation, and other node accesses. CAS failure is a load, so languages often forbid release/acq_rel failure orders. Use official semantics rather than translating mnemonic code mechanically.

**Prove linearizability.** Consider all successful top CAS events in their atomic modification order. A push CAS changes abstract sequence from `S` to `x::S`; its candidate next was the exact top it compared successfully. A pop CAS changes `x::S` to `S` and returns `x`; only one CAS can win for that exact top state under the no-ABA identity premise. An empty acquire read observes null at a moment within its call. Order operations at these points. Each effect is legal and nonoverlapping real-time calls retain order.

Failed CAS attempts have no abstract effect. Pending operations without a successful point can be omitted/completed as allowed by the formal definition. Cancellation after successful CAS cannot pretend the operation did not occur; API policy must deliver/record the result or make retries idempotent. Exceptions should occur before publication where possible. Destructors/callbacks after pop happen after the stack effect and can fail independently.

**Prove lock-freedom carefully.** In the abstract strong-CAS algorithm, a failed CAS due to mismatch means top changed since observation. Top changes only at another successful push/pop CAS, hence another operation made progress. If one operation takes infinitely many steps and continually fails because of interference, infinitely many system operations succeed. If it eventually runs without interference, its CAS succeeds. This is lock-free under scheduling, atomic, memory, and reclamation assumptions.

This is not wait-free: one unlucky thread can repeatedly lose. It is not starvation-free or fair. Weak CAS may fail spuriously without another success; its documented platform/compiler implementation and retry loop require separate progress reasoning. Atomics may be unavailable or emulated; Rust, for example, documents availability/lock-free properties separately and does not promise wait-free atomic methods.

Allocation can block or fail, so “push including allocation is lock-free” needs a lock-free allocator/pool or a narrower claim covering only insertion of a preallocated node. Hazard scanning or epoch advancement can delay reclamation. The OS can preempt a thread after it protects a node, retaining memory. State the boundary of the progress theorem.

**ABA breaks the identity inference.** Pop P reads top address A and `A.next=B`, then pauses. Other operations pop A and B, later reuse A at the same address with a different next, and restore top address A. P's CAS comparing only address A can succeed and install stale B, corrupting the current chain. The word is equal but the logical state/identity differs.

Possible defenses include tagged/versioned top values wide enough for the threat horizon, hazard pointers preventing reuse while observed, epochs delaying reuse beyond prior readers, garbage collection plus no node reuse/mutable-next assumptions, reference counting with safe acquisition, or architecture-specific double-width CAS. Each has wraparound, portability, progress, memory, and lifecycle trade-offs. The next modules treat them in depth. This module's proof is explicitly conditional on no harmful ABA.

**Reclamation protects the dereference window.** It is insufficient to atomically load top and then announce a hazard without validation: removal can occur between load and publication. A hazard-pointer pop typically loads top, publishes it in the thread's hazard slot, then reloads/validates top; only a match makes dereferencing safe. After successful removal, retire rather than free; periodically scan hazards before reclaiming unprotected nodes.

Epoch systems enter a read-side epoch before accessing top and reclaim only after all pre-retirement participants quiesce. A stalled participant can retain memory even if stack operations remain lock-free. Reclamation bounds and observability are therefore production requirements.

**Capacity and lifecycle must be designed.** An unbounded stack can exhaust memory. Exact capacity with lock-free push may require a reservation counter whose linearization and rollback compose with top CAS; a simple precheck races. Approximate/admission policies may be acceptable if stated. A pool/freelist is itself a concurrent reclamation-sensitive stack and cannot be assumed safe circularly.

`close` must prevent new pushes, define whether pops drain existing nodes, coordinate in-flight operations, and wait for lifetime quiescence before destruction. A tagged state can combine closed/top only with appropriate atomic width/protocol; a separate flag creates histories that need proof. Copy, fork, serialization, and process-shared use are not automatically supported.

Bulk pop/push may change an entire linked prefix with one CAS, but must validate order, ownership, failure cleanup, and reclamation. An iterator that follows current links is exposed to removals and cannot be promised a snapshot without protection/versioning. Debug traversal must obey lifetime rules.

The executable model below simulates CAS as an indivisible state transition and deliberately schedules interference. It records success/failure and checks the final chain.

<!-- bijux-verify: {"id":"treiber-cas-schedule-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"final_stack=1,2\npopped=3\ncas_successes=4\ncas_failures=2\ntop=1\nreachable_nodes=2\nunique_reachable=True\nacyclic=True\nall_invariants=True\nevidence=finite_treiber_cas_schedule_model\n","stderr":""}} -->
```python
class TreiberScheduleModel:
    def __init__(self):
        self.top = None
        self.next_of = {}
        self.successes = 0
        self.failures = 0

    def prepare_push(self, node):
        self.next_of[node] = self.top
        return self.top

    def compare_exchange(self, expected, desired):
        if self.top == expected:
            self.top = desired
            self.successes += 1
            return True
        self.failures += 1
        return False

    def reachable(self):
        result = []
        seen = set()
        node = self.top
        while node is not None and node not in seen:
            seen.add(node)
            result.append(node)
            node = self.next_of[node]
        return result, node is None


model = TreiberScheduleModel()
a_expected = model.prepare_push(1)
b_expected = model.prepare_push(2)
assert model.compare_exchange(b_expected, 2)
assert not model.compare_exchange(a_expected, 1)
a_expected = model.prepare_push(1)
assert model.compare_exchange(a_expected, 1)

pop_expected = model.top
pop_desired = model.next_of[pop_expected]
d_expected = model.prepare_push(3)
assert model.compare_exchange(d_expected, 3)
assert not model.compare_exchange(pop_expected, pop_desired)
pop_expected = model.top
pop_desired = model.next_of[pop_expected]
assert model.compare_exchange(pop_expected, pop_desired)
popped = pop_expected

reachable, acyclic = model.reachable()
unique_reachable = len(reachable) == len(set(reachable))
all_invariants = (
    reachable == [1, 2]
    and popped == 3
    and model.successes == 4
    and model.failures == 2
    and acyclic
    and unique_reachable
)

print("final_stack=" + ",".join(str(node) for node in reachable))
print(f"popped={popped}")
print(f"cas_successes={model.successes}")
print(f"cas_failures={model.failures}")
print(f"top={model.top}")
print(f"reachable_nodes={len(reachable)}")
print(f"unique_reachable={unique_reachable}")
print(f"acyclic={acyclic}")
print(f"all_invariants={all_invariants}")
print("evidence=finite_treiber_cas_schedule_model")
```

The model verifies retry recomputation and finite abstract transitions. Integer node IDs are never reused, methods are indivisible, and dereference is always safe; therefore it cannot evidence real atomics, weak-CAS spurious behavior, memory visibility, ABA, reclamation, arbitrary schedules, progress, or performance.

**Test correctness in layers.** Sequential tests cover empty, one item, LIFO, many items, null policy, ownership, close, and capacity. Deterministic schedules cover racing pushes, racing pops, push versus pop, empty observation, failed retry, cancellation before/after CAS, and stalled threads. History tests record invocation/response and check linearizability. Memory tools target data races/use-after-free; model checking explores bounded CAS interleavings; reclamation tests pause readers across removal/reuse.

Progress tests deliberately suspend a thread before/after load, hazard publication, and CAS. Confirm other operations complete, then measure victim retries/starvation and retired memory. Fault injection covers allocation, hazard-record exhaustion, thread exit with protection, panic/exception in payload handling, and shutdown. Tool success does not prove all histories or the theorem assumptions.

**Measure the hot top.** Compare against a correct mutex stack and platform concurrent alternatives with equal allocation/ownership semantics. Vary push/pop balance, empty rate, threads, preallocation, payload size, CPU/NUMA placement, allocator, and backoff. Report throughput and latency percentiles, CAS attempts/failures, retries per operation, top cache-line coherence, scheduler preemption, allocation time, hazard/epoch scans, retired bytes, and per-thread fairness.

Exponential/randomized backoff can reduce futile CAS traffic but can hurt latency/fairness and changes empirical behavior, not abstract correctness. Elimination stacks let a push and pop exchange values without touching central top; they require collision slots, timeouts, linearization/progress proofs, and workload evidence. Optimize only after the simple stack and reclamation system are correct.

## Definitions and Notation

Let abstract stack be sequence `S=<s_0,...,s_{n-1}>`, where `s_0` is top. Concrete `top` is atomic pointer/value `T`; `next(x)` is immutable while `x` is reachable. `Reach(T)` is the sequence obtained by following next until null. Representation requires `Reach(T)` finite/acyclic/unique and payload projection equal `S`.

`CAS(A,E,D)` atomically reads atomic object `A`; if current equals expected `E`, it writes desired `D` and succeeds, otherwise leaves `A` unchanged and reports/returns the observed value according to the API. Weak CAS can fail spuriously. The atomic **modification order** totally orders writes/read-modify-writes to one atomic object under the language model.

For push node `n`, successful transition is `CAS(top,t,n)` with `next(n)=t`. For pop node `t`, transition is `CAS(top,t,next(t))`. `lp(op)` denotes a linearization point. Empty pop's point is the qualifying null load; successful operations' points are their winning CAS.

Progress classes: **blocking** permits one delayed holder to prevent others; **lock-free** guarantees system-wide completion in an infinite execution; **wait-free** bounds every operation's own steps; **obstruction-free** guarantees completion when eventually running alone. Fairness/starvation and real-time deadlines are additional properties.

Let node states be private `P`, reachable/live `L`, retired `R`, and reclaimable `Q`. Valid transitions are `P→L` by successful push; `L→R` by successful pop; `R→Q` only after the lifetime protocol. Re-push/reuse needs a separate identity/ABA rule.

For evidence, let `A_op` be CAS attempts, `F_op` failures, `R_op=A_op-1` retries for a successful simple attempt sequence, `B` retired bytes, `X_q` latency percentile, and `T(p)` throughput at concurrency `p`. These are empirical quantities under named conditions.

## Mechanisms, Invariants, or Proof Structure

### Push proof

1. Allocate and completely initialize private node/payload under exclusive ownership.
2. Acquire/load observed top as required; assign candidate next to that exact observation.
3. Successful release-capable CAS publishes one new chain prefix and linearizes push.
4. Failure has no abstract effect; consume/reload current top, recompute next, and retry or cancel safely.
5. Candidate is freed only if never published and no other reference can exist.

### Pop proof

1. Enter/publish the reclamation protection before relying on a top dereference; validate after protection.
2. A qualifying acquire null observation linearizes empty pop.
3. For nonnull top, safely read immutable next/payload under publication/lifetime guarantees.
4. Successful CAS to next linearizes exactly one removal; failure removes nothing and retries with new protection.
5. Winner transfers payload once, retires node, and reclaims only after the protocol permits.

### LIFO/linearizability proof

Order successful top CAS and qualifying null reads at their points. A successful push's expected top equals the entire chain immediately before its point, so it prepends one payload. A successful pop's expected node is immediately top at its point, so it removes/returns the first payload. Competing CAS on the same expected identity have at most one winner absent ABA. This yields a legal sequential stack history preserving real-time order.

### Lock-freedom proof boundary

In the strong-CAS abstract algorithm, a mismatch failure implies another successful top modification; repeated interference implies repeated system completions. In isolation, the current observed transition succeeds. The claim assumes scheduled steps, nonblocking available atomic operations, bounded local work, safe dereference/reclamation participation, and no comparator/callback. Allocation and full reclamation are excluded unless independently proven lock-free. Weak spurious failure requires an additional primitive-level progress argument.

### Evidence ladder

1. Sequential specification, ownership, capacity, and lifecycle tests.
2. Chain/uniqueness/acyclicity assertions and differential LIFO tests.
3. Controlled CAS schedules for push/push, pop/pop, push/pop, empty, failure, cancellation, and stalled threads.
4. Bounded linearizability/model checking over recorded histories.
5. Target memory-order, race, sanitizer, ABA, and reclamation tests/tools.
6. Progress experiments with preemption, weak failure, allocator/reclaimer pressure, and fairness telemetry.
7. Capacity, node-reuse, thread-exit, shutdown, and memory-exhaustion faults.
8. Production-shaped throughput, tails, CAS/coherence, allocation, reclamation, and retained-memory evidence.

## Alternatives and Trade-Offs

| Design | Central mechanism | Progress/semantic advantage | Principal cost |
|---|---|---|---|
| Mutex stack | protected sequential list/vector | simple ownership/snapshot/capacity | holder blocking/convoy |
| Treiber stack | one atomic top CAS | compact lock-free core | hot word, ABA/reclamation |
| Tagged Treiber stack | pointer plus generation | detects bounded ABA cycles | width/alignment/wraparound |
| Hazard-pointer stack | announced protected nodes | portable safe reuse and ABA aid | scans, records, per-pop protocol |
| Epoch stack | read-side epochs | cheap common access | stalled reader retains memory |
| GC/no-reuse stack | managed stable nodes | simpler physical lifetime | GC cost; logical ABA still conditional |
| Elimination stack | top plus exchange arena | scales balanced push/pop | complex timeout/progress proof |
| Combining/flat combining | delegate/batch operations | amortizes hot top; bulk semantics | combiner delay and blocking model |
| Per-thread stacks | local ownership plus stealing | low local contention | not one global strict LIFO order |

A mutex stack can outperform under low contention and is easier to bound, close, snapshot, and debug. Lock-free is justified by a required progress property or measured workload benefit, not sophistication. A mature library usually dominates bespoke unsafe atomics unless the exact API/progress/layout differs materially.

Treiber top is a scalability ceiling because every operation writes it. Backoff reduces collisions; elimination exploits complementary operations; sharding weakens global LIFO; combining changes who performs work. Each optimization must preserve the intended abstract order or explicitly change it.

## Failure Modes and Misconceptions

- **“CAS alone makes the list safe.”** It protects one word transition, not node initialization, dereference lifetime, or reuse.
- **“A failed push can retry unchanged.”** Desired node next must match the new expected top.
- **“Sequential consistency solves ABA.”** Ordering cannot distinguish reused identity represented by the same bits.
- **“GC solves every ABA.”** Only if node identity is not reused/mutated in a harmful way; logical protocols still matter.
- **“Pop can free immediately after winning.”** Another reader may have loaded the node before removal.
- **“Hazard publication after load is enough.”** Reload/validate top after publishing protection to close the race.
- **“Release push means pop can use relaxed loads.”** Payload/next consumption needs a valid acquire path.
- **“CAS failure can use release ordering.”** Failure is a load; target APIs restrict valid orderings.
- **“Weak CAS failure proves interference.”** It may be spurious, so the strong-CAS progress proof cannot be copied verbatim.
- **“Lock-free means wait-free or fair.”** A victim can retry forever while others finish.
- **“One atomic instruction means constant latency.”** Retries, coherence, allocation, preemption, and reclamation create variable tails.
- **“Allocation is outside push by definition.”** Only if the API/proof explicitly accepts preallocated nodes or narrows its progress claim.
- **“Capacity can be checked before CAS.”** Concurrent pushes race; exact bounds require reservations that compose with top.
- **“Iteration is read-only and harmless.”** It needs lifetime safety and a declared consistency model.
- **“Benchmark throughput proves lock-freedom.”** Progress is a universal execution property under a formal model; tests are supporting evidence only.

## Worked Examples

### Example 1

**Situation.** Push A reads null and sets `A.next=null`. Push B wins first. A retries CAS expecting B but does not update its next.

**Reasoning.** A's successful retry installs A with null next, losing reachable B. Correct A sets `A.next=B` before CAS `(B,A)`.

**Conclusion.** Every push attempt's desired chain must extend its exact expected chain.

### Example 2

**Situation.** Two pops load top X and next Y.

**Reasoning.** Only one CAS `(X,Y)` can succeed absent harmful ABA. Winner removes/returns X. Loser has no abstract effect and must protect/reload the new top; it cannot return the value it read.

**Conclusion.** CAS winner uniqueness implements single-consumer ownership of the top node.

### Example 3

**Situation.** Pop reads null while a push overlaps and succeeds just afterward.

**Reasoning.** Empty pop linearizes at its qualifying null observation, before the push CAS. Both calls overlap, so that sequential order is legal.

**Conclusion.** Empty is linearizable without waiting for future pushes.

### Example 4

**Situation.** Push initializes payload and next, then publishes top with release CAS; pop acquire-loads top and wins removal.

**Reasoning.** Release/acquire synchronization makes pre-publication initialization visible before pop consumes fields, subject to the target language. A relaxed consumer without another acquire path lacks this proof.

**Conclusion.** Publication ordering connects private initialization to shared dereference.

### Example 5

**Situation.** Pop P loads A; Q pops A and B, reuses A with another next, and top becomes address A again.

**Reasoning.** P's address comparison can succeed although its cached next belongs to the old A incarnation, corrupting the chain. Lifetime-delayed reuse, tags, or another proven protocol is required.

**Conclusion.** Bitwise equality of top is insufficient when identity can cycle.

### Example 6

**Situation.** One thread fails CAS 1,000 times while peers complete operations.

**Reasoning.** This observation is consistent with lock-freedom and starvation. It does not prove lock-freedom for all executions, and it signals a tail/fairness problem. Measure interference and consider backoff/elimination or a fair blocking design.

**Conclusion.** Formal system progress and per-thread service quality are different.

### Example 7

**Situation.** A hazard-pointer pop loads A, publishes hazard A, and immediately dereferences without reloading top.

**Reasoning.** A remover could unlink/free A before hazard publication. The pop must publish then validate top still equals A; otherwise clear/retry without dereference.

**Conclusion.** Protection acquisition itself needs a race-closing protocol.

### Example 8

**Situation.** Exact capacity is 100. Two pushes both read size 99 and proceed.

**Reasoning.** A non-atomic precheck admits both. Use an atomic reservation with rollback on failed/aborted publication, combine count/state in a wider protocol, serialize capacity admission, or document approximate capacity.

**Conclusion.** Cross-field invariants do not arise from an atomic top alone.

### Example 9

**Situation.** Stack close sets a flag, observes no active operation, and frees nodes while a push loaded the flag earlier but has not published.

**Reasoning.** The entrant was not accounted for; it can access freed state or publish after close. Lifecycle needs an entrant/refcount/epoch/gate protocol ordering admission, close, in-flight completion, drain, and reclamation.

**Conclusion.** Object destruction is a concurrent operation with its own proof.

### Example 10

**Situation.** Treiber beats a mutex at 32 threads with preallocated nodes, but production allocates variable payloads and runs on two NUMA sockets.

**Reasoning.** The test omitted allocator/reclaimer, payload ownership, cross-socket top-line bouncing, imbalance, empty pops, and tails. Reproduce the service mix and equal semantics, measuring CAS, coherence, allocation, retired memory, and fairness.

**Conclusion.** A hot-word algorithm must be evaluated as a complete memory/lifecycle system.

## Cross-Program Connections

- **Concurrent and Parallel Programming:** atomic memory order, compare-exchange, progress, ABA, hazard pointers, and epoch reclamation form the language-level foundation.
- **Operating Systems:** preemption, cache coherence, NUMA, allocator locks, signals, and lifecycle determine behavior beyond the abstract algorithm.
- **Programming Languages and Systems Programming:** unsafe pointer validity, ownership transfer, destructors, and panic/exception cleanup govern sound implementations.
- **Security Engineering:** unbounded allocation, retry amplification, retained memory, malformed lifecycle use, and use-after-free are denial-of-service or corruption surfaces.
- **Performance Engineering:** CAS failure, cache-line transfer, backoff, allocator/reclaimer cost, per-thread tails, and fairness must be observed together.
- **Distributed Systems:** lock-free local progress gives no durability, replication, consensus, or exactly-once external effect.

## References

1. R. Kent Treiber, [“Systems Programming: Coping with Parallelism”](https://books.google.com/books/about/Systems_Programming_Coping_with_Parallel.html?id=YQg3HAAACAAJ), IBM Research Report RJ 5118, 1986. Bibliographic record for the primary source of the CAS stack algorithm.
2. Maurice P. Herlihy and Jeannette M. Wing, [“Linearizability: A Correctness Condition for Concurrent Objects”](https://www.cs.cmu.edu/~wing/publications/HerlihyWing90.pdf), *ACM TOPLAS* 12(3), 1990. Primary correctness framework.
3. Maurice Herlihy, [“Wait-Free Synchronization”](https://cs.brown.edu/people/mph/Herlihy91/p124-herlihy.pdf), *ACM TOPLAS* 13(1), 1991, pp. 124–149. Primary progress/universality framework.
4. Maged M. Michael, [“Hazard Pointers: Safe Memory Reclamation for Lock-Free Objects”](https://www.eecg.utoronto.ca/~amza/ece1747h/papers/hazard_pointers.pdf), *IEEE TPDS* 15(6), 2004, pp. 491–504. Primary reclamation and ABA treatment.
5. Rust Project, [`std::sync::atomic`](https://doc.rust-lang.org/std/sync/atomic/), Rust 1.98 documentation. Official atomic portability, lock-free versus wait-free scope, memory model, and operation guidance.
6. Oracle, [`AtomicReference`](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/util/concurrent/atomic/AtomicReference.html), Java SE 26. Official reference CAS operations and memory effects through the atomic package contract.
7. ISO C++ working draft, [Atomics clause](https://eel.is/c++draft/atomics), current draft accessed 2026-08-30. Primary atomic object, ordering, and compare-exchange specification text.
8. The Go Project, [The Go Memory Model](https://go.dev/ref/mem), accessed 2026-08-30. Official synchronization and race-free programming requirements.

## Exercises

### Exercise 1

State the sequential stack specification and define CAS, linearization point, lock-free, wait-free, spurious failure, ABA, retirement, and reclamation. List the core Treiber representation invariants.

### Exercise 2

Trace this schedule from empty: P prepares push A; Q pushes B; P retries; R and S both prepare pop; R wins; S retries and wins. Give every successful transition, returned values, final stack, and linearization order.

### Exercise 3

Review a pop using relaxed top load, dereferencing next immediately, strong CAS with release success/failure order, then freeing the node. Identify every correctness/API defect and give a safe high-level outline using hazard pointers.

### Exercise 4

Design a bounded closeable Treiber-based stack API with exact capacity 1,000. Specify admission reservation, push/pop points, failure rollback, empty/closed behavior, in-flight tracking, drain/destruction, and which parts retain lock-free progress.

### Exercise 5

A scheduler uses a Treiber stack for work but reports extreme starvation and cross-socket coherence traffic under balanced push/pop load. Propose an alternative and a verification/migration plan without weakening the required semantics silently.

## Answers to the Exercises

### Answer 1

Abstract `S` is a sequence: push prepends; nonempty pop returns/removes head; empty pop reports absence unchanged. CAS atomically replaces one word only if it equals expected. A linearization point is the effect event inside the call. Lock-free guarantees system-wide progress; wait-free bounds each operation's own steps. Weak CAS may fail spuriously. ABA hides intervening changes behind equal bits. Retirement follows logical removal; reclamation permits reuse after no access remains.

Top is null or a fully initialized live node; next traversal is finite, acyclic, and unique; its payload projection equals `S`; reachable next is immutable; only successful top CAS changes membership; candidate is private until push; pop dereference is lifetime-protected; release/acquire publishes fields; failure recomputes desired state; one winner owns each popped node/value.

### Answer 2

P prepares `A.next=null`. Q prepares `B.next=null` and wins `CAS(null,B)`, so Q push linearizes first and stack is `[B]`. P's old CAS fails; it sets `A.next=B` and wins `CAS(B,A)`, linearizing next; stack `[A,B]`. R and S both observe A/next B. R wins `CAS(A,B)`, returns A, and linearizes. S's CAS fails; it protects/reloads B, reads null, wins `CAS(B,null)`, returns B, and linearizes last.

Final stack is empty. One legal order is `push(B), push(A), pop()->A, pop()->B`, exactly LIFO. Failed attempts have no abstract effect. Nodes cannot be freed before the losing S safely abandons old A/B observations under the reclamation protocol.

### Answer 3

Relaxed load provides no publication-acquire proof for payload/next. Dereferencing immediately has no lifetime protection; another pop may free/reuse the node. Release is invalid as a CAS failure order in common APIs because failure is a load; release-only successful pop also may not acquire initialization. Immediate free races with readers and enables ABA/use-after-free.

High-level hazard outline: enter with a hazard record; acquire-load top; if null, clear/exit and return empty. Publish top in the hazard slot with required ordering, then acquire-reload/validate top unchanged. On mismatch clear/retry. Only after validation read immutable next/payload. CAS top with a valid success order (commonly acquire/acq_rel as the complete proof requires) and allowed failure order; on failure clear/update/retry. On success transfer payload, clear hazard, retire node, and reclaim only after scanning shows no hazard can reference it. The exact orders must be derived from the language and hazard-pointer implementation.

### Answer 4

Expose `tryPush`, `tryPop`, `close`, and `drain/awaitQuiescence`; define pushes after close as closed, pops after close as draining until empty then closed. An atomic admission state reserves one of 1,000 slots before node publication; reservation failure returns full. Allocation/private initialization follows reservation. If allocation/cancellation occurs before top CAS, release reservation. A successful push top CAS linearizes membership. A successful pop top CAS linearizes removal, then releases one capacity reservation exactly once. Empty pop linearizes at null observation consistent with close state.

Close must atomically stop new admission and register/wait for entrants that may already hold reservations. It does not free until in-flight operations finish, the stack is drained/disposed by policy, and reclamation quiesces. Combining closed flag, reservation count, and entrant state may require a packed wide atomic or a small lifecycle gate/lock. The top CAS core can remain lock-free with preallocated nodes and a lock-free reclamation/reservation design; exact capacity, allocation, close waiting, and destruction are not automatically lock-free. State the narrower guarantee rather than mislabel the whole API.

### Answer 5

Balanced push/pop suggests an elimination stack: operations first attempt bounded exchanges in a randomized arena so complementary push/pop pairs linearize by exchanging the value without central top; fallback uses Treiber. If strict global LIFO across all overlapping operations is required, elimination can still be linearizable because overlapping pairs may be ordered appropriately, but the exact published algorithm must be proved. If service requires fairness/per-thread bounds, a fair mutex/queueing stack or different scheduler policy may be preferable; sharded local deques/work stealing changes strict global LIFO and needs explicit approval.

Keep the coarse correct stack and original Treiber as oracles. Verify elimination slot states, timeout/withdraw races, value single ownership, point histories, ABA/reclamation, cancellation, close/capacity composition, race/memory tools, and stalled participants. Benchmark production topology/mix with throughput, tails per thread, starvation, CAS/slot collisions, coherence, allocation, and retired bytes. Canary behind one API, maintain a runtime rollback to the simpler implementation, and roll back for any history defect, memory anomaly, capacity/lifecycle violation, tail/fairness regression, or insufficient measured benefit.
