---
module_id: CONPAR-051
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 51
title: Obstruction-Free, Lock-Free, and Wait-Free Progress
status: complete
last_verified: 2026-08-29
---

# Obstruction-Free, Lock-Free, and Wait-Free Progress

## One-Page Review

### Governing question

Under what execution, scheduler, atomicity, memory, and component assumptions can a concurrent operation be called obstruction-free, lock-free, or wait-free, and what does each claim leave unproved?

### Essential definitions

- A **safety property** says nothing bad occurs; a **progress property** says some desired event eventually occurs.
- An implementation is **nonblocking** in the formal sense when suspension or failure of one participant cannot indefinitely prevent all others from completing; API documentation also uses “nonblocking” merely to mean “returns without waiting,” so define the term.
- **Obstruction-freedom** guarantees an operation completes if it takes sufficiently many steps without interference.
- **Lock-freedom** guarantees system-wide progress: in every sufficiently long execution with active operations, some operation completes.
- **Wait-freedom** guarantees every operation completes within a finite bound on its own steps, usually parameterized by algorithm/input/participants.
- **Starvation-freedom** guarantees every continuously enabled/requesting participant eventually completes under stated fairness; a lock-based algorithm can be starvation-free.
- A **step** is one atomic transition in the specified computation model, not necessarily one source line or fixed wall-clock duration.
- **Helping** lets one operation advance or complete another operation's published descriptor.
- **Interference** is another operation changing relevant shared state so a pending operation must retry or adapt.
- A **scheduler assumption** states which continuously enabled participants receive steps; no algorithm completes an unscheduled thread's local call.

### Central model, mechanism, or theorem

For deterministic total operations in a conventional asynchronous shared-memory model, wait-free implies lock-free, and lock-free implies obstruction-free. The converses do not hold: a lock-free CAS loop may let one caller lose forever, and an obstruction-free algorithm may livelock under perpetual interference. The hierarchy concerns progress only. Linearizability, memory safety, correct publication, bounded memory, fairness, response time, and performance require separate arguments. Randomization, blocking allocators, reclamation, target atomics, cancellation, and scheduler behavior must be included in an end-to-end claim.

### Critical invariants

The operation's abstract safety specification and linearization/commitment points are fixed before progress analysis. Invocation, response, pending, active, and completed states are unambiguous. Every retry either observes/causes relevant abstract advancement or is accounted as spurious/environmental; an infinite failed-CAS argument cannot silently assume success elsewhere. Step bounds cover every loop, help path, retry, allocation, reclamation, and nested operation in scope. A paused participant cannot retain a resource that invalidates the claimed class. Cancellation after commitment cannot erase the operation. Hardware/runtime atomics used by the proof provide the stated lock-free behavior on the target.

### Common failures

Code contains no mutex and is called lock-free; a method returns `try_again` immediately and is called wait-free despite never completing its logical request; CAS failure is treated as proof another operation completed; lock-free is called starvation-free; wait-free is translated into a wall-clock deadline; a randomized expected bound is presented as deterministic; an allocator or reference counter with hidden locks is ignored; memory reclamation waits for a paused reader; a 128-bit atomic silently falls back to a lock; backoff sleeps while holding an essential reservation; helping recursively creates an unbounded chain; or stress-test success is presented as a universal liveness proof.

### Compact example

In six rounds, caller A attempts six updates and loses each time while caller B completes six. The history witnesses system progress and possible individual starvation, consistent with lock-freedom but not wait-freedom for A. A separate helping schedule completes A, B, and C within three own/help-accounted steps under a stipulated bound. These abstract traces illustrate quantifiers; they do not prove an implementation or hardware primitive.

### Connections

[Atomic Read-Modify-Write Operations](025-atomic-read-modify-write-operations.md) supplies atomic transitions. [Compare-and-Swap Loops](026-compare-and-swap-loops.md) supplies retry witnesses. [Acquire and Release Ordering](027-acquire-and-release-ordering.md) supplies publication. [Work Stealing](047-work-stealing.md) contrasts scheduler-level progress. Subsequent modules construct stacks, queues, ABA defenses, and reclamation.

## Governing Question

How should a researcher or engineer state, prove, compose, test, and operationalize nonblocking progress without confusing global advancement, individual completion, fairness, bounded response time, or raw performance?

Progress classes are quantified claims over executions, not adjectives inferred from syntax.

## Why This Matters

Locks couple participants: an owner that is descheduled, crashes, or suffers priority inversion can delay waiters. Nonblocking algorithms replace that dependency with atomic coordination and retry/helping. This can improve resilience and tails in particular workloads, but it expands the proof surface to memory ordering, lifetime, ABA, interference, and scheduler assumptions.

The vocabulary guides requirements. A telemetry counter may tolerate one caller starving while aggregate updates continue. A real-time control operation may need a verified per-operation step and time bound. A user-facing `try_send` may be operationally non-waiting but says nothing about whether a repeatedly retried logical send ever succeeds.

Misclassification is not academic. Calling a lock-free subsystem wait-free can invalidate a deadline analysis; ignoring a blocking allocator can make an end-to-end lock-free claim false; calling a starvation-free mutex inferior because it “uses locks” can sacrifice fairness, energy, and auditability for no measured benefit.

## Prerequisites and Retrieval

Retrieve:

- safety, liveness, and histories from [Safety, Liveness, and Progress](004-safety-liveness-and-progress.md);
- fairness and starvation from [Deadlock, Livelock, and Starvation](006-deadlock-livelock-and-starvation.md);
- atomic transitions from [Atomic Read-Modify-Write Operations](025-atomic-read-modify-write-operations.md);
- retry semantics from [Compare-and-Swap Loops](026-compare-and-swap-loops.md);
- publication from [Acquire and Release Ordering](027-acquire-and-release-ordering.md);
- weak-memory reasoning from [Reasoning About a Weak-Memory Program](030-reasoning-about-a-weak-memory-program.md); and
- cancellation commitment from [Cancellation and Timeouts](036-cancellation-and-timeouts.md).

Retrieval prompt: construct one history in which the system completes infinitely many operations while one named caller never completes, and explain why this can satisfy lock-freedom but violate wait-freedom and starvation-freedom.

## Learning Objectives

After completing this module, a learner can:

1. state obstruction-, lock-, wait-, and starvation-freedom using correct quantifiers;
2. distinguish progress from safety, linearizability, fairness, deadlines, and performance;
3. derive the wait-free-to-lock-free-to-obstruction-free implication hierarchy;
4. construct histories separating the three classes;
5. audit CAS-retry and helping arguments for hidden assumptions;
6. include atomics, allocation, reclamation, backoff, scheduling, and cancellation in end-to-end progress;
7. distinguish deterministic, randomized, probabilistic, amortized, and expected bounds;
8. specify compositional progress for nested library operations;
9. design model, stress, and latency evidence without overstating proof; and
10. decide when a lock-based or specialized design better satisfies product requirements.

## Core Exposition

### Progress begins after safety is specified

A fast-completing wrong operation is not useful. First define the abstract object, legal histories, linearization or commitment events, memory ownership, and failure outcomes. Then ask which pending invocations complete. Linearizability is a safety property: every completed concurrent history corresponds to a legal sequential order respecting real-time precedence. It does not guarantee any call completes.

Conversely, a loop can always return “success” and be wait-free while corrupting state. Progress classification never substitutes for atomicity, visibility, representation invariants, or reclamation. Review safety and progress as separate proof obligations and then show they compose in the implementation.

### Execution model and quantifiers

Let a history contain invocation, internal step, linearization, and response events. An operation is pending after invocation and before response/terminal cancellation. A process is active when it continues taking algorithm steps. Define which reads, writes, RMWs, allocation calls, and runtime operations count as steps.

The asynchronous model permits arbitrary relative speeds and pauses. A scheduler can stop a thread forever. Wait-freedom bounds an operation in its own executed steps, not the time until the scheduler supplies them. A wall-clock guarantee additionally needs scheduling, preemption, interrupt, memory, device, and worst-case execution bounds.

Progress statements often quantify over admissible fair or unfair executions. State whether participants can crash, whether a crashed descriptor may be helped, whether spurious weak-CAS failures are bounded, and whether memory is finite. Changing admissibility changes the theorem.

### Obstruction-freedom

An obstruction-free operation completes if, after some point, it executes alone for sufficiently many of its steps. It tolerates a participant paused without holding a conventional lock, but concurrent interference can keep everyone restarting forever. Contention management—backoff, ownership tokens, randomized delay—may make solo windows likely, yet the base guarantee remains conditional.

Transactional-memory algorithms may be obstruction-free: a transaction commits when run without conflicting updates, but synchronized adversarial transactions can repeatedly abort each other. A mutex fallback can guarantee progress operationally while making the combined path blocking rather than purely obstruction-free.

Obstruction-freedom is useful when contention is rare or an external contention manager supplies stronger scheduling. Do not shorten the definition to “does not use locks.”

### Lock-freedom

Lock-freedom is system-wide. Informally, an infinite execution in which active operations continue taking steps cannot contain only finitely many completions. Equivalently in many finite-state arguments, within a finite amount of aggregate algorithm activity some operation must complete. One operation may starve forever while others repeatedly win.

A typical CAS-loop proof argues: if my CAS succeeds, my operation advances/completes; if it fails because the compared state changed, another successful transition occurred, so the system advanced. This argument requires that failures truly witness relevant change and that advancement cannot cycle forever without a completion. Weak CAS may fail spuriously. Helping/descriptor transitions can advance without completing and need a well-founded measure.

Lock-free does not mean contention-free. A single atomic cache line can serialize modifications and generate unbounded retries. It does not mean fair, low-latency, bounded-memory, energy-efficient, or robust against process death outside the modeled shared address space.

### Wait-freedom

Wait-freedom gives each invocation a finite bound on its own steps independent of other participants' speeds. The bound can depend on number of participants, object capacity, or input size; state it. “Eventually” without a bound is closer to starvation-freedom under fairness, not the standard bounded-step wait-free claim.

Simple fixed-width atomic load/store/fetch-add operations may be wait-free at the abstract machine level if the target implements them directly with bounded steps. A CAS retry loop is not automatically wait-free because one caller may lose indefinitely. Wait-free constructions commonly use helping: an operation publishes a descriptor, and participants complete pending operations in a bounded order before their own.

Helping moves rather than eliminates cost. It introduces descriptor lifetime, sequence numbers, idempotent state transitions, bounded scanning, and ownership of response publication. An unbounded participant registry or recursively nested helping graph can destroy the step bound.

### The implication hierarchy

If every active operation completes within its finite own-step bound, then whenever any active operation takes enough steps, at least one completes: wait-free implies lock-free. If an implementation is lock-free, an operation running alone cannot take infinitely many steps without any completion; with only that operation active, system-wide completion must be its completion: lock-free implies obstruction-free.

Converses fail. For obstruction-not-lock-free, two operations can continually invalidate one another yet each completes during a solo interval. For lock-not-wait-free, schedule B to win every contested update while A repeatedly retries; completions continue but A starves. These are separation witnesses under the stated model, not performance measurements.

Some literature distinguishes **bounded wait-free** explicitly or uses nuanced randomized definitions. Quote the source definition instead of assuming terminology is identical across papers.

### Starvation-freedom, deadlock-freedom, and locks

Deadlock-freedom for a blocking algorithm means some participant eventually makes progress under appropriate scheduling; starvation-freedom means each persistent participant eventually succeeds. A fair queue lock can be starvation-free while a lock-free stack can starve a thread. The axes are not a simple quality ladder.

Blocking algorithms depend on lock owners being scheduled and eventually releasing. Priority inheritance, robust locks, leases, or watchdogs address specific failure modes. In exchange, locks can provide bounded queueing, fairness, simpler multi-field invariants, lower retry traffic, and easier observability.

Select by requirement: crash/preemption tolerance, per-thread fairness, deadlines, contention, critical-section size, memory bounds, energy, platform support, and audit cost.

### CAS retries need a variant

Consider a loop: read `e`, compute `d`, CAS, retry on failure. Safety needs pure recomputation and a valid linearization point. Lock-free progress needs a well-founded system measure. If every failed strong CAS observes a successful modification and every bounded number of modifications completes an operation, infinite failures imply infinite completions elsewhere.

That second clause matters. A protocol can flip descriptor states or help cyclically without completing. Define a rank such as remaining descriptor phases, number of unfulfilled announcements before the selected operation, or monotonic sequence advancement. Prove steps decrease rank or complete an operation.

Backoff does not automatically preserve a formal class. Bounded local delay adds bounded steps/time under a model; unbounded sleep or parking depends on wakeup/scheduler progress. Randomized backoff yields probabilistic/expected statements against an adversary model, not deterministic wait-freedom.

### Helping and universal constructions

In a helping protocol, each participant announces an operation with unique sequence. Helpers choose a pending descriptor, compute/attempt the transition, and publish its response exactly once. If all participants help in a bounded round and each descriptor has bounded phases, every announced operation can obtain a bound.

Proof obligations include descriptor immutability after publication; unique generation to prevent ABA; linearization chosen once; helpers agree on result; response becomes visible; completed descriptors are not mistaken for new ones; a paused owner is not needed; and reclamation never frees a descriptor still observable.

Universal constructions demonstrate broad possibility from strong primitives, but their space, copying, helping, and contention costs may be impractical. A theorem of computability/progress is not a performance recommendation.

### Randomized and probabilistic progress

Random choices can break symmetric livelock. Claims may be “terminates with probability one,” “expected steps bounded,” or “high-probability bound against an oblivious/adaptive adversary.” These are distinct from a deterministic per-execution bound. Record independence and entropy assumptions.

Probability-one termination allows arbitrarily long executions with nonzero probability. Expected latency can coexist with unacceptable tails. A safety-critical deadline needs a deterministic or otherwise accepted worst-case assurance, not only expected wait-freedom.

Random seeds derived from shared schedule or predictable adversarial input may violate the analysis. Empirical retry histograms support implementation behavior but cannot prove the distribution for all schedules.

### Composition and hidden blocking

An operation is only as nonblocking as its transitive dependencies. It may call an allocator, reference counter, logger, clock, thread-local initializer, language runtime, signal handler, or reclamation scheme. If any can wait on a paused owner, an unqualified end-to-end lock-free claim is false.

Qualify the surface: “the update kernel is lock-free after successful allocation on targets where atomic X is lock-free.” Preallocation or bounded pools can remove allocator dependency but introduce exhaustion outcomes. Garbage collectors can pause all application threads even if the data structure algorithm is lock-free.

Hardware support varies by width/alignment. A source `atomic` may use an internal lock. Query target guarantees where APIs expose them, inspect generated/runtime behavior as needed, and test supported deployment architectures. Lock-freedom at one layer does not imply process-failure tolerance across machines.

### Reclamation changes progress

Removing a node logically does not make it safe to free. Hazard pointers, epochs, quiescent-state schemes, reference counting, and tracing GC impose different progress. A paused epoch participant can prevent reclamation indefinitely, producing unbounded retired memory even while operations remain lock-free. Memory exhaustion can then invalidate operational progress.

Hazard scanning cost can depend on participants/retired nodes; acquiring a reference count safely can require retry; destructors may block. State whether the progress theorem covers logical operations, reclamation, allocation, and destructors. Later modules develop these mechanisms separately.

Progress and bounded space are independent properties but production viability often needs both. “Lock-free until memory is exhausted” is an incomplete service claim.

### Memory ordering and compiler semantics

Progress assumes safety of observations. Relaxed ordering that exposes uninitialized payload can produce undefined behavior rather than merely a slower retry. Compiler transformations follow the language memory model. Atomics must have correct width, alignment, lifetime, modification order, and success/failure ordering.

Coherence is not fairness: a cache protocol can serialize atomic updates without guaranteeing which core wins. Acquire/release publication does not make a CAS loop wait-free. Sequential consistency simplifies ordering reasoning but alone supplies no progress.

If data races invoke undefined behavior, execution traces outside the language model cannot support a progress proof. First establish a well-defined program.

### Cancellation, timeouts, and bounded attempts

A wait-free method can still be cancelled by an API policy; distinguish algorithm completion from caller abandonment. Before linearization, cancellation may withdraw an unpublished request. After commitment, returning “cancelled with no effect” is false. Helping may complete an operation after its owner times out, so the outcome needs stable lookup or an ambiguous/committed result.

Adding “retry CAS at most ten times” makes the method bounded-step but not necessarily a wait-free implementation of the original total operation. It may return `contention` without performing the requested update. Wait-freedom concerns completing the specified operation, including its allowed failure preconditions, not merely returning control.

Cleanup must remain bounded/in-scope. Cancellation that leaves a descriptor requiring an unbounded rescuer can violate lifecycle and progress even if the foreground call returns.

### Performance and real-time behavior

Lock-free algorithms can outperform locks under preemption or moderate contention; they can also lose through coherence storms, redundant work, helping, reclamation, and cache footprint. Wait-free algorithms can have larger constants or worst-case helping. Measure throughput, latency distribution, per-operation retries/steps, fairness, energy, cache traffic, memory retention, and tail under placement/preemption.

A step bound is not a worst-case execution time. Convert steps to time only with bounded instruction/cache/memory/bus behavior, preemption/interrupt analysis, platform atomic timing, and all nested operations. Hard real-time qualification requires system and domain review.

Priority is another axis. A low-priority operation can be helped by high-priority callers, which may improve completion but charge high-priority work unpredictably. Conversely, a high-priority caller can starve in a lock-free race. Account for budgets and priority inversion-like effects.

### Verification strategy

Write formal histories for each operation and identify linearization, pending, response, and help transitions. Prove safety invariants separately. For progress, define active operations, scheduler/adversary, steps, and a ranking/charging argument. Model-check small participants with adversarial interleavings, pauses, spurious failures, cancellation, and descriptor reuse.

Stress tests measure millions of schedules, retry distributions, starvation intervals, preemption, affinity, oversubscription, and target atomics. Instrument without adding locks to the measured kernel. Watchdog timeouts find symptoms but do not distinguish scheduler starvation from algorithm livelock automatically.

Static inspection finds hidden blocking dependencies. Target checks establish atomic availability. Reclamation tests pause readers across retire/reuse and measure retained memory. Finite tools cannot prove every infinite liveness property unless their model and fairness reduction justify it; report model bounds and assumptions.

## Definitions and Notation

Let execution `H` contain operations `o`, each with invocation `inv(o)`, zero or more algorithm steps, optional linearization `lin(o)`, and response `res(o)`. `pending(o,H)` means invoked without terminal response. `steps(o,H)` counts own steps under the declared model.

Obstruction-free: each operation completes after a bounded/sufficient solo suffix. Lock-free: every infinite admissible execution with infinitely many active steps contains infinitely many operation completions. Wait-free: for every operation `o`, a finite bound `B(parameters)` exists such that after at most `B` of its relevant own/help-accounted steps it completes.

Let `C(H)` be completed operations and `R_o` retries of `o`. A CAS-failure charging proof maps failures to distinct or boundedly reused system advancements leading to completions. A step bound is not a wall-time bound.

Definitions vary in formal detail across models. Every proof must state invocation discipline, total/partial operations, crashes, fairness, random adversary, primitives, memory size, and what helpers' steps count toward a bound.

## Mechanisms, Invariants, or Proof Structure

Audit a progress claim in this order:

1. define abstract object, legal outcomes, linearization, and memory-safety invariants;
2. define invocations, responses, pending/active operations, algorithm steps, and admissible executions;
3. state scheduler, crash, interference, spurious-failure, randomness, and memory assumptions;
4. classify the exact operation/kernel/system surface rather than source syntax;
5. construct separation histories for solo interference, system progress, and individual starvation;
6. give a well-founded rank or bounded charging argument for every retry/help transition;
7. derive per-operation bound for wait-free claims, including scans, helping, and nested calls;
8. audit allocation, reclamation, destructors, runtimes, atomics, backoff/parking, and target support;
9. specify cancellation before/after commitment and abandoned descriptor cleanup;
10. model-check adversarial schedules and inspect histories with explicit fairness bounds;
11. stress retry/latency/fairness/memory under preemption, topology, and contention; and
12. state separately what is proven, model-checked, observed, unavailable, or externally reviewed.

The executable model records one lock-free starvation witness and one stipulated bounded-help trace.

<!-- bijux-verify: {"id":"progress-quantifier-witnesses","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"lock_free_attempts={'A': 6, 'B': 6}\nlock_free_completions={'A': 0, 'B': 6}\nsystem_progress=True\nindividual_starvation_witness=True\nwait_free_step_counts={'A': 3, 'B': 2, 'C': 3}\nwait_free_bound=3\nall_within_bound=True\nimplications=['wait-free=>lock-free', 'lock-free=>obstruction-free']\n","stderr":""}} -->
```python
lock_free_attempts = {"A": 0, "B": 0}
lock_free_completions = {"A": 0, "B": 0}

for _ in range(6):
    lock_free_attempts["A"] += 1
    lock_free_attempts["B"] += 1
    lock_free_completions["B"] += 1

wait_free_step_counts = {"A": 3, "B": 2, "C": 3}
wait_free_bound = 3
system_progress = sum(lock_free_completions.values()) > 0
individual_starvation_witness = lock_free_attempts["A"] > 0 and lock_free_completions["A"] == 0

print(f"lock_free_attempts={lock_free_attempts}")
print(f"lock_free_completions={lock_free_completions}")
print(f"system_progress={system_progress}")
print(f"individual_starvation_witness={individual_starvation_witness}")
print(f"wait_free_step_counts={wait_free_step_counts}")
print(f"wait_free_bound={wait_free_bound}")
print(f"all_within_bound={all(value <= wait_free_bound for value in wait_free_step_counts.values())}")
print(f"implications={['wait-free=>lock-free', 'lock-free=>obstruction-free']}")
```

Limitations: this sequential dictionary model stipulates outcomes; it contains no threads, atomics, scheduler, interference, CAS, helping implementation, linearization, memory ordering, allocation, reclamation, cancellation, failures, timing, or proof over infinite histories. It illustrates quantifiers only.

## Alternatives and Trade-Offs

- **Mutex/monitor:** simple compound invariants and possible fairness; paused owner can block others.
- **Obstruction-free kernel:** simple optimistic solo progress; needs contention management for sustained interference.
- **Lock-free algorithm:** tolerates individual pauses for system progress; permits starvation and retry storms.
- **Wait-free algorithm:** bounded per-operation steps; often adds descriptors, helping, space, and constants.
- **Starvation-free queue lock:** eventual per-caller service under fairness; remains blocking on owner/scheduler.
- **Try operation:** bounded return latency; can fail indefinitely without completing the logical request.
- **Helping:** converts paused-owner work into shared responsibility; complicates identity, accounting, reclamation, and priorities.
- **Backoff/parking:** reduces contention/energy; may weaken formal progress or add wakeup dependencies.
- **Preallocation:** removes allocator blocking; introduces fixed capacity and explicit exhaustion.
- **Garbage collection:** simplifies reachability lifetime; pauses and collector progress remain part of the system claim.
- **Randomization:** breaks symmetric schedules with probabilistic bounds; cannot be reported as deterministic wait-freedom.
- **Mature library:** concentrates proof and testing; target/API guarantees still require verification.

## Failure Modes and Misconceptions

1. **“No locks means lock-free.”** Hidden locks, algorithms, and target fallbacks determine progress.
2. **“Lock-free means every thread progresses.”** System completions can coexist with one starving caller.
3. **“Wait-free means fast.”** A finite step bound can be large and each step can be slow.
4. **“Returning failure is wait-free success.”** It must be a legal completion of the original specification.
5. **“CAS failure proves completion elsewhere.”** It proves at most mismatch/spurious failure unless a rank argument connects change to completion.
6. **“Sequential consistency provides liveness.”** Ordering strength is separate from scheduling and progress.
7. **“Backoff strengthens progress.”** Unbounded sleep/parking may introduce blocking and wake dependencies.
8. **“Epoch reclamation is automatically lock-free.”** A paused participant can retain memory indefinitely.
9. **“Stress tests prove lock-freedom.”** Finite schedules cannot establish all infinite executions.
10. **“Wait-free is always better than a mutex.”** fairness, cost, complexity, space, and product semantics decide.

## Worked Examples

### Example 1

Two optimistic transactions repeatedly read the same version and both abort when detecting conflict. Each would commit during a solo suffix, so the kernel can be obstruction-free. An adversarial synchronized schedule can cause infinite mutual interference with no commits, separating it from lock-freedom unless a contention manager supplies more.

### Example 2

A CAS increment has callers A and B. In every round B updates after A reads, A's CAS fails, and B completes. Infinitely many operations complete, satisfying the intuitive lock-free condition; A can starve, so the history refutes per-operation wait-freedom and starvation-freedom.

### Example 3

A wait-free snapshot announces each request in a fixed participant array. Every operation scans at most `N` descriptors and performs at most `K` bounded phases per descriptor, so a proposed bound is expressed in `N` and `K`. The proof must include descriptor publication, helping, response, generation, and reclamation—not only the final CAS.

### Example 4

A C++ atomic update is proved lock-free assuming a native 128-bit CAS. On a target where the library implements that width with a process-local mutex, the source algorithm's unqualified end-to-end claim fails. Runtime/compile-time lock-free support is a deployment gate, not a benchmark detail.

### Example 5

A lock-free linked set logically deletes nodes, but epoch reclamation cannot free them while one registered thread is paused. Operations continue, yet retired memory grows until exhaustion. Report logical-operation lock-freedom separately from reclamation progress and bounded-space/operational availability.

### Example 6

A method stops after ten CAS failures and returns `contention`. The API call returns within a bound, but an operation specified as “increment unless at maximum” was not completed or rejected on its abstract predicate. It is a bounded try operation, not a wait-free implementation of total increment.

### Example 7

A randomized backoff algorithm has finite expected retries against an oblivious adversary. A rare arbitrarily long run remains possible. Report expected/probabilistic progress, adversary and entropy assumptions, and measured tails; do not convert the expectation into a deterministic deadline.

### Example 8

Cancellation arrives after a helper linearizes another caller's operation but before its owner reads the response. The owner must observe committed success (or query stable descriptor outcome), not return “cancelled without effect.” Cleanup/reclamation waits until no helper can still access the descriptor.

### Example 9

Verification models three participants, bounded descriptors/generations, strong and spurious CAS failure, arbitrary pauses, and help transitions. It checks safety plus ranks between completions under explicit fairness. Stress testing then measures retry/starvation and memory retention on deployment targets. Neither evidence alone is universal proof.

### Example 10

A wait-free braking-control queue claims bounded operations. Deployment requires named vehicle-control, functional-safety, real-time, hardware/atomic, compiler/runtime, systems, cybersecurity, human-factors, quality, independent verification, and regulatory reviewers; requirements/hazard traceability; target lock-free and worst-case step-to-time analysis; memory/reclamation bounds; model checking and proof review; hardware-in-the-loop, interference, preemption, fault-injection, degraded-mode, recovery, and environmental evidence; independent fail-safe controls; and signed residual-risk acceptance. This chapter grants no road authorization.

## Cross-Program Connections

- **Algorithms:** adversarial schedules, ranking functions, universal constructions, and lower bounds formalize progress.
- **Programming languages:** atomic APIs, memory models, undefined behavior, runtimes, and type/lifetime systems constrain proofs.
- **Operating systems:** scheduling, priorities, preemption, page faults, and wakeups turn steps into operational latency.
- **Computer architecture:** atomic width, coherence, cache contention, NUMA, and memory ordering affect availability/cost.
- **Formal methods:** temporal logic, refinement, linearizability, fairness, and model checking separate safety and liveness.
- **Real-time systems:** bounded algorithm steps require WCET and scheduling analysis before deadlines.
- **Reliability:** crashed/paused participants, cleanup, memory exhaustion, and recovery qualify nonblocking claims.
- **Security:** adversarial contention and denial-of-service can exploit retry and helping costs.
- **Performance:** throughput, tails, fairness, retries, energy, and retained memory must be measured independently.
- **Safety engineering:** progress is one component of a reviewed hazard-control argument, never deployment authorization.

## References

1. M. Herlihy. “Wait-Free Synchronization.” ACM Transactions on Programming Languages and Systems 13(1), 1991. <https://doi.org/10.1145/114005.102808>.
2. M. Herlihy, V. Luchangco, and M. Moir. “Obstruction-Free Synchronization: Double-Ended Queues as an Example.” ICDCS, 2003. <https://doi.org/10.1109/ICDCS.2003.1203503>.
3. M. P. Herlihy and J. M. Wing. “Linearizability: A Correctness Condition for Concurrent Objects.” ACM TOPLAS 12(3), 1990. <https://doi.org/10.1145/78969.78972>.
4. D. Cederman et al. “Lock-Free Concurrent Data Structures.” Programming Multicore and Many-core Computing Systems, 2014. <https://doi.org/10.1002/9781119332015.ch7>.
5. M. M. Michael. “Hazard Pointers: Safe Memory Reclamation for Lock-Free Objects.” IEEE TPDS 15(6), 2004. <https://doi.org/10.1109/TPDS.2004.8>.
6. T. Brown. “Reclaiming Memory for Lock-Free Data Structures: There Has to Be a Better Way.” PODC, 2015. <https://doi.org/10.1145/2767386.2767436>.
7. ISO C++ Working Draft. “Lock-free Property.” <https://eel.is/c++draft/atomics.lockfree>.
8. Oracle. “Java Platform API: VarHandle.” <https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/invoke/VarHandle.html>.
9. Rust Project. “std::sync::atomic.” <https://doc.rust-lang.org/std/sync/atomic/>.
10. Linux Kernel Documentation. “Memory Barriers.” <https://docs.kernel.org/core-api/wrappers/memory-barriers.html>.

## Exercises

### Exercise 1

Write formalized quantifiers for obstruction-, lock-, and wait-freedom in one declared asynchronous model. Prove the implication hierarchy and state every necessary caveat.

### Exercise 2

Given a CAS loop with weak spurious failure and descriptor helping, design a valid lock-free progress rank/charging proof or explain what missing facts prevent one.

### Exercise 3

Audit an alleged wait-free queue whose enqueue allocates, scans a growable participant list, uses epoch reclamation, and returns `busy` after 20 retries. Classify each surface precisely.

### Exercise 4

Design verification and empirical evidence for a lock-free operation across x86-64 and ARM targets, including memory safety, progress, target atomic support, reclamation, cancellation, and starvation.

### Exercise 5

A railway interlocking component uses a “wait-free” state update and meets average latency. Explain why this is insufficient and enumerate required human review and evidence.

## Answers to the Exercises

### Answer 1

Define active operations as invoked and taking steps, with deterministic total methods and admissible atomic shared-memory executions. Obstruction-free: for each pending operation, a finite solo-step suffix bound under unchanged interference suffices for its completion. Lock-free: any infinite execution with infinitely many active algorithm steps has infinitely many completions. Wait-free: each invocation completes within finite `B(parameters)` relevant own/help-accounted steps regardless of other speeds. Wait-free implies lock-free because an active operation receiving its bound completes; lock-free implies obstruction-free because with one active solo operation any required completion is its own. Caveats include scheduler supplying steps, total/partial outcomes, crashes, randomness, finite memory, primitives, and definition variants.

### Answer 2

Separate weak-CAS spurious failures from mismatches; either use strong CAS for the liveness argument or prove spurious failures cannot continue indefinitely under the primitive model. For mismatch, identify a successful state transition. Define a well-founded global rank—such as lexicographic remaining phases for the oldest announced descriptor plus bounded announcements ahead—and show every nonspurious failure can be charged only boundedly before rank decreases or an operation completes. Helping transitions must be idempotent, acyclic/bounded, and descriptor generations protected. Without bounded spurious failure, a rank connecting state changes to completions, bounded participants/phases, and reclamation progress, lock-freedom is unproved.

### Answer 3

Returning `busy` is bounded as an API try-call but not a wait-free completion of a total enqueue unless `busy` is a legal capacity predicate outcome. The CAS kernel may be lock-free only with a rank argument. Allocation can block, so end-to-end enqueue is not unqualified lock-free. A growable participant scan has no fixed bound; even finite-at-invocation needs a declared parameter/bound. Epoch reclamation may permit logical lock-free operations while a paused participant prevents bounded reclamation/space. The composition is at best a qualified kernel claim, not the alleged wait-free queue.

### Answer 4

Specify abstract histories, linearization, representation/lifetime and acquire/release invariants; prove a retry/completion rank with scheduler/spurious assumptions. Model-check bounded adversarial interleavings, pauses, cancellation before/after commitment, descriptor generations, ABA, retire/reuse, and weak-memory litmus cases. On each target verify atomic width/alignment and lock-free implementation, compiler/runtime versions, generated/runtime mappings, and reclamation dependencies. Stress with affinity, oversubscription, preemption, contention, delayed readers, wrap/reuse, and failures; record attempts, own/help steps, completion/starvation intervals, tails, cache traffic, retained memory, output histories, and instrumentation impact. State model bounds and unsupported targets.

### Answer 5

The label and mean omit actual target atomic fallback, full transitive step bound, WCET, scheduler/preemption, memory/reclamation exhaustion, rare contention, hardware faults, cancellation, cyberattack, and safe physical response. Require named railway signalling/interlocking, functional-safety, real-time, hardware, compiler/runtime, systems, cybersecurity, human-factors, operations, quality, independent verification, and regulatory reviewers; requirements/hazard traceability; applicable-standard assessment; formal safety/progress and target mapping review; worst-case time/resource analysis; bounded memory; simulation, hardware-in-the-loop, saturation, adversarial scheduling, fault-injection, failover, recovery, environmental, and operational evidence; independent fail-safe interlocks; and signed residual-risk acceptance. This answer is not authorization for railway operation.
