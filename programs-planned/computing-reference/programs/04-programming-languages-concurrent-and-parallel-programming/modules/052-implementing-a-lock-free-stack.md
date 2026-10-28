---
module_id: CONPAR-052
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 52
title: Implementing a Lock-Free Stack
status: complete
last_verified: 2026-08-29
---

# Implementing a Lock-Free Stack

## One-Page Review

### Governing question

How can a Treiber-style concurrent stack implement linearizable LIFO push and pop with lock-free logical progress while preserving publication, pointer lifetime, exact ownership, ABA resistance, cancellation truth, bounded resources, and verifiable shutdown?

### Essential definitions

- A **Treiber stack** represents the stack by one atomic head reference to an immutable-next linked node and updates that head with compare-and-swap.
- A **linearization point** is the single abstract instant at which an operation takes effect in a legal sequential history.
- **Push preparation** initializes a private node and points its `next` to the observed head before attempting to publish it.
- **Pop protection** establishes that an observed head node cannot be reclaimed before reading its fields and attempting removal.
- **Retirement** removes a node from the abstract stack; **reclamation** makes its storage reusable or frees it after no observer can access it.
- **ABA** occurs when a compared representation changes from A to something else and back to A while a stale operation retains A.
- A **tagged reference** couples a pointer/reference with a generation, subject to atomic width and wrap assumptions.
- **Ownership transfer** moves the new node to the shared stack on successful push and moves a removed node/value to the successful pop on successful removal.
- **Retry** discards only an uncommitted proposal and recomputes it from the new head.
- A **quiescent shutdown** admits no new operations and waits until all possible observers have left before destroying remaining nodes.

### Central model, mechanism, or theorem

Push allocates and fully initializes private node `n`, repeatedly sets `n.next=observed_head`, and CASes `head` from the observation to `n`; the successful CAS linearizes the push. Pop repeatedly protects/validates non-null head `h`, reads `h.next`, and CASes head from `h` to that next; successful CAS linearizes nonempty pop, while a validated null observation linearizes empty pop. Strong-CAS failures caused by head changes can be charged to successful competing updates, giving a lock-free logical kernel under stated atomic and reclamation assumptions. This does not make each caller wait-free or make allocation/reclamation automatically lock-free.

### Critical invariants

The reachable list is finite, acyclic, and consists of initialized nodes; only `head` publication adds a private node. Published `next` is immutable until safe reclamation. Each reachable node appears once and belongs to the stack. A pop dereferences only a protected node and revalidates protection before using it. One successful CAS performs one push or pop; failed CAS commits nothing and refreshes every derived value. A removed node is retired once and reclaimed only after all stale observations are impossible. Values are moved/destroyed exactly once. Empty, cancellation, close, and allocation failure are distinct. Shutdown cannot race entry or reclamation. Target atomic representation supplies the assumed operation and progress.

### Common failures

Code reads `head.next` before protecting `head`; frees immediately after pop; assumes garbage collection semantics in a manual-memory language; reuses an address and ignores ABA; adds a small tag without bounding wrap; retries with a stale `next`; mutates a published link; publishes a partially initialized payload with relaxed ordering; reads the popped value after another thread can reclaim it; treats CAS failure as operation failure; performs I/O or destruction inside a retry loop; calls the stack wait-free; ignores blocking allocation/reclamation; returns cancelled after successful CAS; or destroys the stack while operations can still acquire head.

### Compact example

Push A, then B. Caller P1 observes B for pop. P2 removes B and pushes C. P1's CAS expecting B fails because head is C; it refreshes, removes C, and leaves A. Completed pop results are B then C, no node is duplicated, and the failed proposal changes nothing. Stable node identities and non-reuse intentionally exclude ABA. This deterministic history illustrates refresh and linearization, not concurrent memory safety.

### Connections

[Compare-and-Swap Loops](026-compare-and-swap-loops.md) supplies retry discipline. [Acquire and Release Ordering](027-acquire-and-release-ordering.md) supplies publication. [Obstruction-Free, Lock-Free, and Wait-Free Progress](051-obstruction-free-lock-free-and-wait-free-progress.md) supplies progress quantifiers. The next modules deepen queues, ABA, hazard pointers, and epoch reclamation.

## Governing Question

How should an engineer derive, implement, audit, test, and operate a lock-free stack so the compact CAS pseudocode remains correct under actual language memory, allocation, reclamation, lifecycle, and failure semantics?

The head CAS is the visible center of the algorithm; safe lifetime and ownership are most of the proof.

## Why This Matters

The Treiber stack is a canonical nonblocking data structure because one atomic root encodes a clear abstract transition. It teaches linearization, retry recomputation, publication, contention, and progress in a small algorithm. It also exposes the trap in “just use atomics”: the pop must dereference a node that a competitor can unlink, so the locally simple CAS loop is unsafe without a global reclamation protocol.

Stacks support freelists, pools, work caches, undo chains, and runtime internals. LIFO locality can be valuable, but fairness is poor and one hot head cache line can bottleneck. Many product queues require FIFO, blocking backpressure, closure, or bounded capacity instead. Learning the stack is not permission to replace every mutex-protected collection.

An implementation claim spans a language and target. A garbage-collected Java `AtomicReference` stack avoids manual node reclamation but still needs publication and progress analysis. C++ or Rust raw-pointer variants require explicit lifetime proof. Reference counting can itself be difficult to acquire safely from an unprotected pointer. Treat the memory-management strategy as part of the algorithm.

## Prerequisites and Retrieval

Retrieve:

- linearizable histories from [Safety, Liveness, and Progress](004-safety-liveness-and-progress.md);
- atomic ownership transitions from [Atomic Read-Modify-Write Operations](025-atomic-read-modify-write-operations.md);
- witness refresh and success/failure ordering from [Compare-and-Swap Loops](026-compare-and-swap-loops.md);
- payload publication from [Acquire and Release Ordering](027-acquire-and-release-ordering.md);
- weak-memory validation from [Reasoning About a Weak-Memory Program](030-reasoning-about-a-weak-memory-program.md);
- cancellation commitment from [Cancellation and Timeouts](036-cancellation-and-timeouts.md); and
- system-versus-operation progress from [Obstruction-Free, Lock-Free, and Wait-Free Progress](051-obstruction-free-lock-free-and-wait-free-progress.md).

Retrieval prompt: pause a pop after reading head, let another caller remove and reclaim that node, and identify the first invalid dereference; then repair the trace using a named protection-and-validation protocol.

## Learning Objectives

After completing this module, a learner can:

1. specify a Treiber stack's abstract LIFO and representation invariants;
2. locate linearization points for successful push, successful pop, and empty pop;
3. derive push publication and pop consumption ordering;
4. write CAS retry loops that refresh every head-derived proposal;
5. explain why immediate node freeing is unsafe and why logical deletion differs from reclamation;
6. construct ABA histories and assess tags, delayed reuse, and protected references;
7. scope lock-free progress across allocation, reclamation, target atomics, and destruction;
8. specify cancellation, allocation failure, close, drain, and shutdown truthfully;
9. design model, sanitizer, stress, and performance evidence for stack operations; and
10. decide when a mutex, bounded array, garbage-collected stack, or mature library is preferable.

## Core Exposition

### Abstract stack and representation

The abstract object stores a finite sequence `S`; `push(v)` changes it to `v::S`, `pop()` changes nonempty `v::S` to `S` and returns `v`, and pop on empty returns empty without change. Concurrent results must linearize to this LIFO specification while respecting real-time order between nonoverlapping operations.

The linked representation has atomic `head`. Each node contains value and `next`. From head, following next reaches every abstract element exactly once in top-to-bottom order and eventually null. The list is acyclic. A node is private during construction, shared/reachable after publication, retired after successful removal, and reclaimable only after no observer can dereference it.

Keep `next` immutable after publication in the basic algorithm. That reduces concurrent state to one atomic head and makes a successful head CAS the structural transition. Reusing nodes requires returning them through a separately proven protocol; rewriting links while stale readers exist invalidates the proof.

### Push construction and linearization

Push first obtains node storage and initializes its value privately. It reads head as `h`, writes `n.next=h`, and tries `CAS(head,h,n)`. If the CAS succeeds, that atomic event linearizes push. All later observers that acquire the publication must see the initialized value and link.

If CAS fails, another operation changed head or the primitive failed spuriously. The node remains private; no shared ownership transfer occurred. Refresh `h`, rewrite the still-private `n.next`, and retry. The value constructor, allocation, logging, billing, and other effects must not repeat inside the retry unless explicitly idempotent.

A release CAS/store on success commonly publishes prior node initialization; an acquiring pop/read consumes it. Exact success and failure orders follow the language API. Failure order must support the next read/retry but cannot be release-only. Strong versus weak CAS affects spurious retry, not abstract safety when coded correctly.

Allocation occurs before the logical retry loop when possible. If allocation can block, the complete `push` is not unqualified lock-free even if its publication kernel is. Preallocated bounded pools provide a different failure mode—capacity exhaustion—that must be part of the API.

### Pop: protection before dereference

Naive pop reads `h=head`, reads `next=h.next`, and CASes head. Another thread can remove `h` and reclaim it between the first two actions; reading next is then use-after-free. Atomics on head do not protect pointee lifetime.

A hazard-pointer outline is: read head; publish `h` in the caller's hazard slot; re-read head; if changed, clear/replace hazard and retry; after equality validation, read `h.next` and attempt CAS. The validation closes the race in which removal occurred before protection became visible. On successful pop, retire `h`; reclamation scans hazards and waits until no slot protects it. On failure, refresh rather than dereferencing stale derived state.

Epoch-based protection instead enters a read-side epoch before observation; removed nodes retire with an epoch and are reclaimed only after all earlier participants quiesce. Garbage collection keeps reachable local references alive under its model. Each approach changes costs, progress, thread registration, shutdown, and bounded-memory behavior.

### Pop linearization cases

For a protected non-null head `h`, successful `CAS(head,h,h.next)` linearizes pop. From then on, the caller owns the removed logical value subject to the reclamation strategy. It may return/move the value before freeing storage only when exclusive access and destructor rules are established.

For empty pop, the linearization point is a head observation of null with the ordering/validation required by the API. A concurrent push may linearize immediately afterward; the empty result remains legal because operations overlapped. Empty is a snapshot at one abstract instant, not a promise that the stack stays empty.

A failed CAS linearizes nothing. The caller must release/adjust protection and retry from a new observation. Do not return empty merely because a competitor removed the observed last node; another competitor may have pushed a node before the retry.

### Linearizability proof structure

Prove a representation invariant initially for null. A private node is not reachable. Successful push atomically makes it the unique head with its next pointing to the prior valid list, preserving finiteness, acyclicity, and LIFO order. Failed push changes no shared state.

Successful pop atomically replaces valid head with its immutable next, removing exactly the first abstract value. Protection ensures the proof's reads are well-defined; reclamation occurs after the abstract transition. Empty observation returns empty consistent with the list. Failed pop changes no state.

Order successful CAS events plus empty observations at their declared instants. Each maps to one sequential stack transition and lies between invocation and response. Real-time order for nonoverlapping calls is preserved by event time. This proof assumes correct atomic and memory semantics and does not prove progress.

### Lock-free progress argument

After allocation/protection succeeds, each push/pop retry attempts head CAS. A successful CAS completes one logical operation. A strong CAS failure due to mismatch means head changed through another successful push/pop CAS. Thus, if one active operation fails forever because competitors change head, system completions continue; if interference stops, its next valid attempt succeeds. This establishes the intuitive lock-free kernel under assumptions.

Weak CAS can fail spuriously, so either the platform/source progress assumption bounds such failures or the proof uses strong CAS. Hazard acquisition/scanning, epoch entry, allocation, destruction, and target atomic fallback must be audited separately. A reclaimer that blocks on a mutex qualifies the end-to-end claim.

Treiber stack is not wait-free: one caller can lose CAS indefinitely. Backoff may improve measured behavior but can add sleep/parking dependencies. A fair mutex stack may provide better per-caller service under load.

### ABA is identity failure

P1 observes head address A and next B. P2 pops A and B, then an allocator reuses A for another node whose address equals P1's expected value. P1's CAS can succeed even though A now denotes a different generation and its cached next is stale. Representation equality did not prove historical identity.

A tagged head compares `(pointer,generation)` and increments generation on every head transition. It works only when the pair is atomically compared and the tag cannot wrap during any live stale observation. Pointer packing has alignment, address-width, provenance, portability, and tool implications. A tiny tag delays rather than eliminates ABA.

Delayed reclamation/reuse can prevent the dangerous identity reuse while a stale reference remains. Hazard pointers and epochs therefore address both lifetime and many pointer-ABA traces when used correctly. Logical ABA can remain if mutable state cycles and the algorithm needs historical distinction.

### Reclamation choices are algorithms

Never reclaim until stack shutdown is safe but leaks/retains memory during operation. This can be acceptable for a finite short-lived batch with a proved node bound. Garbage collection is convenient but collector pauses and reachability rules remain.

Hazard pointers offer per-node protection and can support lock-free reclamation with bounded participant/hazard assumptions; scans and retire thresholds add overhead. Epoch schemes make read-side paths cheap but a stalled registered participant delays reuse and can cause unbounded retirement. Reference counting needs a safe way to acquire a count before the object disappears and can have destructor/cycle/progress costs.

Choose a mature implementation. The stack proof is inseparable from the exact reclaimer API: protection publication order, validation, retire ownership, scan, deregistration, thread exit, destructor, and shutdown.

### Memory ordering

Push must make private initialization visible before another thread consumes the node. A release success on head paired with an acquire observation commonly establishes this. Pop's successful acquisition must preserve access to value/next and synchronize with the publication chain as the language requires.

CAS failure order affects the refreshed observation. Over-strengthening to sequential consistency may simplify initial reasoning but does not repair lifetime or ABA, and it can cost performance. Weakening to relaxed without a complete happens-before proof can expose uninitialized fields or data races.

Head atomicity and node-field access must obey source-language rules. In C++/Rust unsafe code, a dangling-pointer read is invalid even if the CAS later fails. Java/managed runtimes avoid raw free but still require safe publication. Compiler provenance and reclamation rules can be stricter than hardware intuition.

### Ownership of values and destructors

On successful push, ownership of the node/value moves to the stack. On failed attempt, caller/operation retains it for retry. If push is cancelled before publication, destroy/return the private node once. After successful publication, cancellation cannot claim no effect.

On successful pop, stack ownership moves to the caller. Other observers may still hold protected pointers but must not access a moved/destroyed payload unless the algorithm separates logical value extraction from physical reclamation safely. Many implementations store immutable payload and defer node destruction.

Destructors can run arbitrary code, lock, throw/panic, or re-enter. Keep them out of atomic retry loops and reason about language-specific unwinding. If reclamation runs destructors on helper threads, document execution context and latency.

### Boundedness, close, and shutdown

The linked Treiber stack is normally unbounded subject to allocation. A product may need a hard item/byte limit. A separate atomic counter plus head CAS is not automatically one transaction: reservation and publication need a state protocol, rollback, cancellation, and recovery if a participant pauses between them. A bounded array stack may provide a smaller proof for fixed capacity.

“Close” is not inherent. If closed state shares a tagged head representation, push must atomically reject after close while existing nodes remain poppable under the declared drain policy. Separate close flag and head can expose races unless the specification permits them and the proof orders observations.

Shutdown first prevents new operation entry, then waits for all registered/in-flight observers, completes or cancels according to contract, drains or destroys reachable nodes, processes retired lists, deregisters protection records, and releases storage. Empty head alone is not quiescence: a pop can hold a protected retired node.

### Contention and alternatives

One head is a serialization point. Under contention, many cores invalidate the same line and discard proposals. LIFO access may concentrate hot nodes and starve older work. Elimination stacks allow complementary push/pop operations to exchange away from head, improving scalability under matched load, but add timeouts, slots, memory ordering, linearization cases, and progress complexity.

Per-thread local stacks with periodic transfer reduce contention but alter visibility/fairness. A mutex can batch changes and sleep rather than spin. An array-based bounded stack avoids allocation/reclamation per operation. A queue or work-stealing deque may fit workload semantics better.

Benchmark against a correct optimized lock-based baseline. Measure throughput, latency/retries per thread, starvation intervals, cache/coherence, allocation/reclamation, retained memory, energy, and topology. A lock-free proof predicts no speedup.

### Cancellation and failures

Allocation failure occurs before publication and can return a distinct error with caller retaining the value. Contention/CAS failure is internal retry, not stack-full or operation failure. Reclamation pressure may need backpressure or assistance but cannot silently discard nodes.

Cancellation before successful CAS can abandon a private push or protected pop after releasing resources. After successful CAS, the operation committed; return success, publish a durable result, or expose an ambiguous committed outcome. For pop, losing a returned value because the caller disappeared requires an ownership/cleanup protocol.

A process crash in shared persistent memory is outside ordinary volatile-thread Treiber assumptions. Partial persistence, allocator metadata, and recovery need a crash-consistent design. Lock-free across threads does not mean recoverable across process/power failure.

### Verification strategy

Use a sequential reference stack and history checker for bounded concurrent executions. Enumerate push/pop at empty, one, and multiple nodes; pause at every read/protect/validate/CAS/retire transition; inject spurious CAS failure; force last-node races; cancel before/after success; and test close/shutdown entry.

Force ABA by controlling allocation/reuse and generation near wrap. Delay protected readers while others retire and scan. Verify no premature free, duplicate value, loss, double destroy, or leaked protection. Sanitizers and language interpreters can detect some races/lifetime defects; they do not prove linearizability or progress.

Model-check the abstract protocol under a bounded reclaimer and weak-memory model. Stress on every target with affinity, oversubscription, preemption, and NUMA. Record operation identities, attempts, CAS outcomes, linearization evidence, retire/reclaim events, high-water retired memory, and watchdog symptoms without adding a serializing logger to the kernel.

## Definitions and Notation

Let `H` be atomic head and `null` the empty representation. Node `n` contains immutable-after-publication `value(n)` and `next(n)`. `Reach(H)` is the unique list reachable from head. Node states are `private`, `reachable`, `protected`, `retired`, and `reclaimable/reclaimed`, with protection possibly overlapping reachable/retired.

Push proposal from observation `h` is `CAS(H,h,n)` after `next(n)=h`. Pop proposal is `CAS(H,h,next(h))` after protection and validation. Successful CAS is the nonempty operation's linearization point. A validated null head observation linearizes empty pop.

Let `A`, `F`, and `C` be CAS attempts, failures, and successful commits; `A=F+C` for attempted transitions. One commit corresponds to one completed structural operation. Progress claims are scoped to the logical kernel unless allocation/reclamation/target support are included explicitly.

ABA uses a stale interval with representations `H=A`, then `H=B`, then `H=A`. A tag changes comparison to `(address,generation)` but needs atomicity and a no-wrap-during-staleness bound.

## Mechanisms, Invariants, or Proof Structure

Audit a lock-free stack in this order:

1. define LIFO specification, legal errors, close/drain, and cancellation semantics;
2. prove reachable-list finiteness, acyclicity, uniqueness, initialization, and immutable links;
3. assign private/shared/retired/reclaimed node and value ownership at every transition;
4. place push, nonempty-pop, and empty-pop linearization points;
5. derive success/failure memory orders from publication and consumption edges;
6. require pop protection before dereference and validation after protection publication;
7. recompute head, next, tags, and all derived proposals after CAS failure;
8. prove ABA/lifetime safety through the exact tagged/protection/reclamation mechanism;
9. scope lock-free progress across CAS, allocation, reclaimer, runtime, target atomic, and backoff;
10. define destructor, thread exit, close, cancellation, drain, quiescence, and shutdown;
11. model-check histories and adversarial reuse, then stress/sanitize every deployment target; and
12. benchmark against simpler alternatives while preserving identical semantics and outputs.

The executable model demonstrates a failed stale pop proposal, refresh, successful commits, and final LIFO/accounting.

<!-- bijux-verify: {"id":"treiber-stack-abstract-history","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"events=['push A commits', 'push B commits', 'P1 observes B', 'P2 pop B commits', 'push C commits', 'P1 stale CAS fails', 'P1 refreshes C', 'P1 pop C commits']\npop_results=[('P2', 'B'), ('P1', 'C')]\nfinal_stack=['A']\ncas_attempts=6\ncas_failures=1\ncommits=5\nall_values_accounted=True\nfailed_proposal_changed_nothing=True\n","stderr":""}} -->
```python
stack = []
events = []
pop_results = []
cas_attempts = 0
cas_failures = 0
commits = 0

def push(value):
    global cas_attempts, commits
    cas_attempts += 1
    stack.insert(0, value)
    commits += 1
    events.append(f"push {value} commits")

push("A")
push("B")
p1_observed = stack[0]
events.append(f"P1 observes {p1_observed}")

cas_attempts += 1
p2_value = stack.pop(0)
commits += 1
pop_results.append(("P2", p2_value))
events.append(f"P2 pop {p2_value} commits")

push("C")
before_failed_proposal = stack[:]
cas_attempts += 1
if stack[0] != p1_observed:
    cas_failures += 1
    events.append("P1 stale CAS fails")

p1_observed = stack[0]
events.append(f"P1 refreshes {p1_observed}")
cas_attempts += 1
p1_value = stack.pop(0)
commits += 1
pop_results.append(("P1", p1_value))
events.append(f"P1 pop {p1_value} commits")

all_values = [value for _, value in pop_results] + stack
print(f"events={events}")
print(f"pop_results={pop_results}")
print(f"final_stack={stack}")
print(f"cas_attempts={cas_attempts}")
print(f"cas_failures={cas_failures}")
print(f"commits={commits}")
print(f"all_values_accounted={sorted(all_values) == ['A', 'B', 'C']}")
print(f"failed_proposal_changed_nothing={before_failed_proposal == ['C', 'A']}")
```

Limitations: this sequential list model stipulates atomic commits and stable, never-reused value identities. It performs no threads, pointers, atomics, weak memory, protection, reclamation, ABA, allocation, destruction, cancellation, close, shutdown, or progress proof. It illustrates one legal abstract history only.

## Alternatives and Trade-Offs

- **Mutex stack:** simplest lifetime and compound lifecycle; a paused owner blocks peers.
- **Treiber stack with GC:** compact logical algorithm and managed lifetime; collector/runtime pauses and atomic support remain.
- **Treiber plus hazard pointers:** explicit per-node protection; publication/scan/registration overhead and careful reclamation proof.
- **Treiber plus epochs:** cheap read-side protection; stalled participants retain retired memory.
- **Reference counting:** familiar ownership; safe count acquisition, contention, cycles, and destructor progress are difficult.
- **Never reclaim until shutdown:** minimal operational lifetime proof; memory grows with removals until a known quiescent bound.
- **Tagged head:** detects bounded generations of ABA; requires atomic pair width, portability, and wrap proof.
- **Elimination stack:** scales matched push/pop contention; adds exchange slots, timeouts, more linearization cases, and semantics.
- **Bounded array stack:** no per-operation node allocation/reclamation; fixed capacity and index-wrap/state protocol.
- **Local stacks with transfer:** reduce hot-head contention; alter immediate visibility, balance, and fairness.
- **Mature library:** amortizes expert proof/testing; exact API, target, and lifecycle still require audit.

## Failure Modes and Misconceptions

1. **“The head CAS makes the stack safe.”** Dereference lifetime and reclamation are separate global protocols.
2. **“After unlink, the node is mine to free.”** Stale protected/unprotected observers may still hold it.
3. **“CAS equality proves identity.”** Address reuse creates ABA unless generations/lifetime prevent it.
4. **“Release/acquire prevents ABA.”** Ordering does not encode historical identity or preserve lifetime.
5. **“A failed pop CAS means empty.”** It means the proposal lost; refresh and reevaluate.
6. **“Garbage collection proves lock-freedom.”** It solves a lifetime class but collector/runtime progress remains.
7. **“A tag eliminates ABA forever.”** Finite tags wrap and may not be atomically supported.
8. **“Lock-free means fair and fast.”** one caller may starve and head contention can underperform locks.
9. **“Empty means safe to destroy.”** in-flight observers and retired nodes can remain.
10. **“Stress tests prove the implementation.”** rare reuse, weak memory, infinite progress, and target variation need explicit reasoning.

## Worked Examples

### Example 1

Push node N privately initializes value 7 and `next=A`, then release-CASes head from A to N. That successful CAS linearizes push and publishes initialization. A failed attempt retains private ownership, refreshes head, rewrites `next`, and makes no abstract change.

### Example 2

P1 reads head A. P2 pops A and reclaims it before P1 reads `A.next`; P1 dereferences freed storage. The repair publishes a hazard for A, revalidates head still A, then reads next. If P2 removed A before validation, validation fails and P1 never dereferences it as current.

### Example 3

P1 protects A and reads next B. P2 pushes C, so P1's CAS A-to-B fails. P1 cannot retry CAS with cached B; it refreshes/protects C and derives C's next. Failed attempts commit nothing, and protection for A is cleared only under the reclaimer protocol.

### Example 4

P1 observes `(A,7)`. Other operations remove/reuse address A but publish `(A,9)`. A double-width CAS rejects P1's stale pair. The argument is incomplete until the implementation proves atomic pair support and generation cannot wrap from 9 back to 7 during P1's maximum protected lifetime.

### Example 5

An epoch stack remains logically lock-free while one paused thread pins an old epoch. Ten million retired nodes accumulate and allocation fails. Operational requirements therefore include retirement high-water bounds, stalled-participant policy, memory admission, and separate logical/reclamation progress claims.

### Example 6

A push allocates before entering CAS. Cancellation before publication destroys/returns the private node and reports no effect. Cancellation after success reports committed success; it cannot free the now-shared node. Allocation failure returns the original value distinctly from contention.

### Example 7

A close flag separate from head races: push reads open, closer sets closed, then push publishes. Either specification permits already-admitted pushes, or close/head participate in one versioned state transition. “No push after close returns” requires an entry/commit protocol and proof.

### Example 8

A GC-managed Java stack avoids use-after-free, but a stalled pusher does not block system progress because its node remains private. CAS contention can starve that pusher. Collector stop-the-world pauses and `AtomicReference` target/runtime behavior prevent an unqualified end-to-end wait-free claim.

### Example 9

A model checker explores two pushes/two pops with pauses at observe, protect, validate, CAS, and retire. A controlled allocator forces A-B-A reuse. A history checker validates LIFO; a lifetime monitor rejects dereference after reclaim; liveness checks state fairness/model bounds. Target stress adds weak memory and real reclaimer behavior.

### Example 10

A lock-free stack holds commands in an autonomous surgical robot. Production requires named surgical, clinical, robotics/control, embedded/atomic, real-time, functional-safety, cybersecurity, human-factors, quality, independent verification, and regulatory reviewers; requirements/hazard traceability; target atomic and compiler validation; formal linearizability/lifetime/progress review; worst-case time/memory/reclamation analysis; simulation, hardware-in-the-loop, adversarial contention, fault-injection, fail-safe, recovery, environmental, and clinical evidence; independent interlocks; and signed residual-risk acceptance. This chapter supplies no deployment authorization.

## Cross-Program Connections

- **Algorithms:** LIFO representation, linearizability, retry ranks, and amortization define correctness/progress.
- **Programming languages:** atomics, memory models, pointer provenance, ownership, GC, destructors, and unsafe code shape proofs.
- **Operating systems:** preemption, affinity, priorities, allocation, and thread exit affect progress and tails.
- **Computer architecture:** CAS width, coherence, cache-line contention, NUMA, and ordering affect support/performance.
- **Formal methods:** history refinement, separation logic, temporal progress, and model checking validate protocols.
- **Memory management:** hazard pointers, epochs, reference counts, and tracing collection govern lifetime.
- **Reliability:** allocation failure, cancellation, close, quiescence, cleanup, and recovery govern service lifecycle.
- **Security:** contention and memory-retention attacks can turn retries/reclamation into denial of service.
- **Performance:** retry distributions, cache traffic, reclamation cost, fairness, and energy decide practical value.
- **Safety engineering:** bounded time/space and independent fail-safe review exceed a lock-free proof.

## References

1. R. K. Treiber. “Systems Programming: Coping with Parallelism.” IBM Research Report RJ 5118, 1986. <https://books.google.com/books/about/Systems_Programming_Coping_with_Parallel.html?id=YQg3HAAACAAJ>.
2. M. P. Herlihy and J. M. Wing. “Linearizability: A Correctness Condition for Concurrent Objects.” ACM TOPLAS 12(3), 1990. <https://doi.org/10.1145/78969.78972>.
3. M. Herlihy. “Wait-Free Synchronization.” ACM TOPLAS 13(1), 1991. <https://doi.org/10.1145/114005.102808>.
4. M. M. Michael. “Hazard Pointers: Safe Memory Reclamation for Lock-Free Objects.” IEEE TPDS 15(6), 2004. <https://doi.org/10.1109/TPDS.2004.8>.
5. T. Brown. “Reclaiming Memory for Lock-Free Data Structures: There Has to Be a Better Way.” PODC, 2015. <https://doi.org/10.1145/2767386.2767436>.
6. ISO C++ Working Draft. “Atomic Operations Library.” <https://eel.is/c++draft/atomics>.
7. Oracle. “Java Platform API: AtomicReference.” <https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/atomic/AtomicReference.html>.
8. Rust Project. “Atomic Types.” <https://doc.rust-lang.org/stable/core/sync/atomic/index.html>.
9. Crossbeam Project. “Crossbeam Epoch-Based Memory Reclamation.” <https://docs.rs/crossbeam-epoch/latest/crossbeam_epoch/>.
10. T. L. Harris. “A Pragmatic Implementation of Non-Blocking Linked-Lists.” DISC, 2001. <https://doi.org/10.1007/3-540-45414-4_21>.

## Exercises

### Exercise 1

Give a linearizability proof for Treiber push, successful pop, and empty pop, including representation preservation and failed CAS behavior.

### Exercise 2

Construct a use-after-free and an ABA history for naive pop. Repair them with a hazard-pointer outline and a tagged-head alternative, stating what each still leaves unproved.

### Exercise 3

Audit success/failure memory ordering for push/pop in one chosen language. Connect every ordering to initialization, link, value, and retry observations without relying on hardware folklore.

### Exercise 4

Design close, cancellation, allocation-failure, destructor, drain, and shutdown semantics for a production stack using epoch reclamation. Include progress and bounded-memory claims.

### Exercise 5

A railway-control stack is linearizable and passes stress tests. Explain why this is insufficient for deployment and enumerate required human evidence.

## Answers to the Exercises

### Answer 1

Invariant: head reaches one finite acyclic chain of initialized, unique nodes whose order equals abstract stack. Push constructs private N with next equal observed valid chain; successful head CAS uniquely adds N and linearizes `push`, preserving invariant/LIFO. Successful pop protects valid non-null H, reads immutable next, and CASes H to next; CAS uniquely removes first node and linearizes return of its value. A head-null observation satisfying the operation's ordering/validation linearizes empty pop. Failed CAS changes no shared state and therefore no abstract state; caller refreshes all derivatives. Ordering/lifetime/reclamation assumptions make reads defined, and CAS event order gives a legal sequential history respecting nonoverlap.

### Answer 2

Use-after-free: P1 reads A; P2 removes/frees A; P1 reads A.next. ABA: P1 reads A/next B; P2 removes A and B, reuses address A for another node; P1's pointer CAS can accept stale A. Hazard repair: P1 reads A, publishes hazard A, re-reads head and retries unless still A, then reads next/CAS; removed A is retired and reclaimed only after hazard scans exclude it. This needs registration, publication ordering, scan, thread-exit, bounded records, progress, and destructor proof. Tagged head distinguishes generations but needs atomic pair support, provenance/layout, increment on every transition, and a no-wrap-during-staleness bound; tags alone do not prevent dereferencing freed memory.

### Answer 3

For C++ as one example, initialize private node fields non-atomically, then use release semantics on successful push CAS so an acquiring observer of head sees value/next. Pop acquires the published head before reading fields; its successful CAS uses an order sufficient for acquiring payload and publishing structural head change to later operations. Failure order is a legal load order (never release-only) and must make the returned/current head suitable for validation/retry; derived next is recomputed after protection. Exact minimal orders depend on CAS API, reclamation synchronization, and whether failure updates expected. Sequential consistency is a conservative starting point, not a lifetime/ABA solution. Validate against the C++ model and implementation, not x86 intuition.

### Answer 4

Define an entry gate plus closed state: close prevents new admitted pushes at a declared linearization point; admitted operations may finish; pops drain until closed-empty. Allocation happens before publication and failure returns the value. Cancellation before CAS releases private/protection state; after CAS returns committed outcome. Epoch guards cover every head/node read; successful pop retires exactly once; destructors run only after grace and in documented context. Shutdown closes admission, waits for operation registry/quiescence, drains or destroys reachable nodes, advances/collects epochs, detects stalled participants, and joins cleanup. Logical kernel may be lock-free; allocator and epoch reclamation are separately qualified. Bound capacity/retired bytes or specify backpressure/stalled-participant policy—do not claim bounded memory merely from lock-freedom.

### Answer 5

Linearizability and finite stress do not establish lifetime under all schedules, target atomic support, ABA/wrap, reclamation/space bounds, system progress, fairness, WCET, scheduler behavior, faults, cancellation, cybersecurity, or safe physical action. Require named railway signalling/interlocking, functional-safety, real-time, hardware/atomic, compiler/runtime, systems, cybersecurity, human-factors, operations, quality, independent verification, and regulatory reviewers; requirements/hazard traceability; applicable-standard assessment; formal memory-safety/linearizability/progress review; target mapping and worst-case time/memory analysis; model checking plus hardware-in-the-loop, saturation, reuse/wrap, fault-injection, failover, recovery, environmental, and operational evidence; independent fail-safe interlocks; and signed residual-risk acceptance. This answer is not railway authorization.
