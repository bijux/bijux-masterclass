---
module_id: CONPAR-060
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 60
title: Deciding When Lock-Free Code Is Justified
status: complete
last_verified: 2026-08-29
---

# Deciding When Lock-Free Code Is Justified

## One-Page Review

### Governing question

When do explicit progress requirements or measured whole-system benefits justify the proof, memory-model, reclamation, portability, lifecycle, observability, and maintenance cost of lock-free code over a simpler synchronized design?

### Essential definitions

- A **hard requirement** is a non-negotiable property whose absence rejects a candidate, such as no dependence on a paused peer in a defined execution context.
- A **preference** is an optimizable objective such as throughput, p99 latency, CPU, memory, energy, or simplicity.
- A **progress scope** names the operation, participant set, interference model, primitives, scheduler/resource assumptions, and beneficiary of a nonblocking claim.
- A **qualified atomic** is an operation whose width, ordering, alignment, and lock-free status are verified on every supported target.
- A **proof budget** is the sustained capacity for specification, refinement, weak-memory, reclamation, lifecycle, and review work.
- **operational debt** is retained memory, retries, delayed destruction, stuck descriptors, or other work created by the concurrency mechanism.
- **maintenance risk** is the chance that later modification invalidates assumptions reviewers cannot see or reproduce.
- A **mature implementation** has a stable contract, relevant production use, owned maintenance, source/release evidence, and compatibility with the required language/target—not merely popularity.
- A **fallback** is an explicitly specified alternative for unsupported targets or overload; hidden locks invalidate an unqualified lock-free claim.
- A **decision record** binds requirements, candidates, evidence, rejected alternatives, limitations, owners, and reevaluation triggers.

### Central model, mechanism, or theorem

Apply gates before scores. First specify abstract behavior and hard progress/environment constraints. Reject any candidate that cannot meet them with verifiable evidence. For survivors, compare measured end-to-end behavior and total lifecycle cost under representative low, typical, saturation, failure, and shutdown workloads. Prefer a mature library or simpler lock when it meets requirements. A custom lock-free algorithm is justified only when a hard constraint excludes simpler designs or reproducible evidence shows a material system benefit, and the organization can own every correctness and operational obligation for the supported lifetime.

### Critical invariants

The sequential/API contract is identical across candidates or differences are explicit. Progress is claimed per path and target, including allocation, reclamation, waiting, callbacks, and fallback. Every unsafe/raw-pointer access has a lifetime proof. Memory ordering maps to source-language rules. Cancellation, timeout, close, restart, and destruction align with commitment. Benchmarks reproduce the declared workload and compare optimized baselines. No score compensates for a failed safety/hard-requirement gate. Evidence is versioned with toolchain/hardware. Owners and rollback exist. Reassessment occurs when workload, targets, dependencies, or invariants change.

### Common failures

Teams choose lock-free for prestige; equate atomic with lock-free; use average microbenchmark throughput as the only gate; compare tuned nonblocking code with a naive mutex; omit oversubscription/NUMA/payload/allocation; ignore fairness and memory debt; depend on a wide atomic that uses a hidden lock; copy an algorithm without its reclaimer; invent weaker semantics to win; treat garbage collection as no cost; lack a failure/close model; have no reviewer who understands the proof; or let an experiment become permanent unowned infrastructure.

### Compact example

A registry is read 99.9% of the time, updates hourly, and readers may block. A mutex-protected immutable shared handle meets correctness and p99; an RCU prototype is 8% faster in a microbenchmark but retains 2 GB behind a delayed reader and complicates unload. No hard nonblocking requirement exists. The justified choice is the simpler handle/lock, with RCU reconsidered only if end-to-end profiling shows a material bottleneck and protected regions can be bounded.

### Connections

[Obstruction-Free, Lock-Free, and Wait-Free Progress](051-obstruction-free-lock-free-and-wait-free-progress.md) supplies precise claims. [Hazard Pointers](055-hazard-pointers.md), [Epoch-Based Reclamation](056-epoch-based-reclamation.md), and [Read-Copy-Update as a Nonblocking Pattern](057-read-copy-update-as-a-nonblocking-pattern.md) expose lifetime trade-offs. [Linearizability Proofs](058-linearizability-proofs.md) and [Contention Management in Nonblocking Algorithms](059-contention-management-in-nonblocking-algorithms.md) supply proof and measurement obligations.

## Governing Question

How should technical leaders decide whether to adopt, buy, retain, or remove a lock-free component based on requirements and reproducible evidence rather than fashion, isolated benchmarks, or fear of locks?

“Can we write it?” is not the decision. The decision is whether the complete system, organization, and supported target set are better and remain auditable.

## Why This Matters

Lock-free algorithms solve real problems. They can prevent a paused thread from blocking system-wide logical progress, avoid lock-holder preemption or failure modes, scale particular hot paths, and support contexts where blocking primitives are forbidden. Mature concurrent queues, allocators, runtimes, and kernels rely on them.

They also concentrate risk. A short CAS loop can depend on a long proof about memory ordering, ABA, object lifetime, allocation, helper ownership, cancellation, and shutdown. A platform may implement an atomic with a lock. A stalled epoch participant can exhaust memory while operations remain logically lock-free. A future maintainer can add a destructor or log statement that invalidates progress.

Simple synchronization is not automatically slow. A tuned mutex can avoid waste, park under contention, provide fairness/priority facilities, and be far easier to operate. Delegation, immutable snapshots, sharding, batching, and bounded queues can remove the bottleneck without custom raw-pointer algorithms. The best design is the smallest proof surface meeting the actual requirement.

## Prerequisites and Retrieval

Retrieve:

- bounded queues and overload from [Thread Pools and Bounded Work Queues](019-thread-pools-and-bounded-work-queues.md);
- atomic/target qualification from [Atomic Read-Modify-Write Operations](025-atomic-read-modify-write-operations.md);
- weak-memory audit from [Reasoning About a Weak-Memory Program](030-reasoning-about-a-weak-memory-program.md);
- overload containment from [Backpressure in Asynchronous Pipelines](040-backpressure-in-asynchronous-pipelines.md);
- progress scope from [Obstruction-Free, Lock-Free, and Wait-Free Progress](051-obstruction-free-lock-free-and-wait-free-progress.md);
- lifetime trade-offs from modules 055–057; and
- proof/contention evidence from [Linearizability Proofs](058-linearizability-proofs.md) and [Contention Management in Nonblocking Algorithms](059-contention-management-in-nonblocking-algorithms.md).

Retrieval prompt: name one precise failure caused by a paused lock holder that the proposed operation must survive, then list every allocator, reclaimer, scheduler, runtime, and target dependency that could reintroduce waiting.

## Learning Objectives

After completing this module, a learner can:

1. convert vague “performance” or “reliability” desires into hard gates and weighted preferences;
2. define exact progress scope and target-qualified atomic assumptions;
3. compare mutexes, queues, delegation, snapshots, sharding, libraries, and custom nonblocking code fairly;
4. enumerate linearizability, memory-order, reclamation, ABA, progress, and lifecycle evidence;
5. design representative benchmarks and reject misleading comparisons;
6. quantify maintenance, observability, portability, security, and operational costs;
7. define build/runtime fallback without false progress claims;
8. produce a durable decision record with owners and reevaluation triggers;
9. plan incremental adoption, shadow validation, rollback, and retirement; and
10. apply stricter human review to real-time, medical, financial, and safety-critical contexts.

## Core Exposition

### Start from the contract

Write the sequential behavior before choosing synchronization. Define values, ordering, capacity, empty/full, cancellation, timeout, close, drain, ownership, errors, and persistence. Candidate implementations must refine the same contract for a fair comparison. If one uses relaxed ordering or approximate counts, label it a different product choice.

Define workload operations and the object boundary. A per-key map need not offer a global snapshot. A transfer across counters is not one atomic operation. Overbroad contracts can force needless synchronization; weakened contracts can hide correctness loss.

Define consequences. A telemetry cache can retry or return stale data; a command queue may not. Recovery, audit, and safety needs determine evidence depth before code style.

### Identify hard progress needs

A valid hard requirement sounds like: “an interrupt-context enqueue must not sleep or acquire a lock that can be held by preempted normal context,” or “if one worker is indefinitely paused after invocation, other queue operations must continue completing without its cooperation, assuming lock-free atomics and available preallocated nodes.”

“Low latency,” “scalable,” and “modern” are preferences, not progress specifications. Translate them into distributions, workloads, targets, and thresholds. A lock-free algorithm gives step progress, not a wall-clock deadline. A wait-free core can still page fault or remain unscheduled.

Audit the entire path. Allocation, descriptor acquisition, hazard record pools, epoch advancement, callbacks, logging, backoff parking, and fallback libraries may block. If the hard requirement covers the public method, a lock-free inner CAS is insufficient.

### Candidate set

Include at least:

- a well-engineered mutex or reader-writer lock;
- a bounded queue or single-owner/delegated design;
- immutable copy-on-write/shared ownership for read-mostly data;
- sharding/partitioning that removes sharing;
- a mature library implementation with documented semantics;
- a custom nonblocking design only when gaps remain.

Also ask whether the shared object should exist. Data ownership, batching, partitioned actors, or local aggregation can eliminate the hot operation. Architectural removal is often more durable than atomic tuning.

The baseline must be competent: correct lock scope, suitable primitive, no avoidable allocation/logging, and comparable semantics. Comparing a custom lock-free structure to deliberately poor locking is not evidence.

### Gate one: semantic and safety feasibility

For each candidate, map every API result and lifecycle state. Require a linearizability/refinement argument where appropriate, representation invariant, memory-order proof, ownership and reclamation protocol, ABA treatment, exception/panic behavior, and exact cancellation/timeout commitment.

Rejected safety evidence cannot be offset by throughput. If a custom structure lacks a credible proof reviewer or a library cannot satisfy payload/lifecycle semantics, it is ineligible. “Tests pass” is not a substitute for universal claims.

Security belongs here. Pointer reuse, speculative accesses, denial via retirement debt, address leakage, malformed callback records, and unsafe foreign interfaces expand the attack surface. Threat-model the concurrency mechanism.

### Gate two: progress and target feasibility

Build a target matrix: architecture, operating system, compiler and flags, language/runtime version, atomic width/alignment, `is_lock_free` or equivalent evidence, allocator/reclaimer, scheduler/preemption context, sanitizers, and fallback. Test every supported release target.

Some APIs guarantee atomicity but not lock-freedom. Wide compare-exchange may call a library routine with a lock. Garbage collector safepoints, runtime suspension, allocator locks, and kernel fallback affect the public claim. Scope or reject accordingly.

If an unsupported target uses a mutex fallback, expose capability at build/deploy time and state that target's different progress. Never silently market the union as lock-free.

### Gate three: resource and lifecycle feasibility

Derive bounds for nodes, descriptors, hazard records, retired objects/bytes, epoch or RCU debt, retries, admission queues, callbacks, and shutdown time. A crashed or paused participant may make an otherwise fast reclaimer unbounded. Define containment without unsafe forced reclamation.

Walk allocation failure, cancellation before/after commitment, thread registration/exit, close, drain, restart, fork/signals where relevant, dynamic unload, and destruction. A component that cannot be safely stopped or upgraded is not production-ready.

Destructors may lock, block, panic, re-enter, or require thread affinity. Deferred deletion context is part of feasibility. So are memory budgets under stalled readers and overload.

### Gate four: organizational ownership

Name maintainers able to review unsafe code, memory models, proof changes, target code generation, and incidents. Define review rules: which files require concurrency owners, what evidence updates with changes, and how releases qualify new hardware/toolchains.

Estimate proof and maintenance cost over years, not implementation week. Documentation must preserve assumptions near owned code without copying workspace meta policy. A design that only its author understands has unacceptable key-person risk for critical infrastructure.

Dependencies need active ownership, release/security policy, and an upgrade plan. Mature means suitable and maintained for this contract, not merely high download count.

### Measure end-to-end candidates

Benchmark the real operation with payload, allocation, reclamation, callbacks, telemetry, and application scheduling. Cover low contention, representative steady load, bursts, saturation, overload, oversubscription, affinity/NUMA, SMT, hot-key skew, long/paused participants, cancellation, and shutdown.

Measure throughput, p50/p95/p99/max, per-operation attempts, oldest age/starvation, CPU, context switches, cache/remote traffic where trustworthy, energy, memory/debt, allocation, callback lag, fairness, and failure recovery. Compare confidence intervals or repeated distributions, not one best run.

End-to-end application impact matters. A data structure 20% faster while consuming 1% of request time cannot justify large complexity. A 5% whole-service improvement may still matter at scale, but record cost and objective.

### Interpret results conservatively

Require a material margin larger than measurement noise and expected maintenance regression. Look for crossovers: mutex wins at low/oversubscribed load while nonblocking wins only at dedicated high contention; choose per actual environment.

Do not average away a catastrophic tail or starvation. A lock-free candidate with more throughput but unbounded retired memory fails a bounded service requirement. A simpler candidate that meets every SLO has already won unless a hard progress gate excludes it.

If candidates trade semantics, present separate decisions. Relaxed/approximate structures can be excellent, but their benefit is partly from a weaker contract, not synchronization alone.

### Prefer buy before build

A mature library can amortize proof, testing, portability, and maintenance across users. Inspect source, documentation, version history, open defects, license, target matrix, reclaimer integration, panic/destructor policy, and progress wording. Run your workload and failure tests.

Wrapping a library can destroy its guarantee: returning raw pointers beyond guards, adding blocking callbacks, mixing domains, or hiding capability fallback. Preserve its lifetime types and error semantics.

Custom code is justified when the hard contract is not available, the benefit is material, the algorithm/proof is understood, and sustained ownership exists. Forking an abandoned implementation makes you the maintainer.

### Decision record

Record problem and object contract; hard gates; workload/targets; candidates; evidence; verification commands/artifacts; quantitative results; rejected options; chosen design; limitations; security/safety review; owners; rollout/rollback; and reevaluation triggers.

Triggers include operation mix or concurrency shift, new architecture/compiler/runtime, library upgrade, incident, retry/debt alarm, SLO change, new cancellation/persistence requirement, maintainer loss, or a simpler alternative becoming available.

The decision can be “not lock-free.” That is an engineering outcome, not failure. Also record conditions that could reopen the choice.

### Incremental adoption and rollback

Introduce behind an internal interface preserving the sequential contract. Run differential tests against a coarse-grained reference, bounded model/history checks, sanitizers/weak-memory tools, and shadow/canary workloads. Compare results and resource accounting.

Feature flags cannot safely switch representations without a migration/quiescence protocol. Prefer selecting implementation at construction or process rollout. Rollback drains operations and reclamation before destroying the old instance.

Define kill criteria: correctness discrepancy, unsupported atomic fallback, p99/fairness regression, debt growth, CPU/energy regression, callback/shutdown failure, or missing observability. Do not wait for a crash.

### Removing unjustified lock-free code

Existing code receives the same audit. If no hard requirement remains and measured benefit is marginal, replacing it can reduce risk. Preserve contract, build differential/history evidence, migrate atomically/quiescently, and remove obsolete unsafe/reclaimer infrastructure.

Avoid sunk-cost reasoning. A sophisticated algorithm is not an asset when it consumes ownership without buying a requirement. Deletion can be the highest-value concurrency improvement.

## Definitions and Notation

- `R_h`: set of hard requirements; every eligible candidate must satisfy all.
- `C`: candidate implementations.
- `E(c,r)`: evidence that candidate c satisfies requirement r on the declared target/workload.
- `eligible(c)`: true only if every hard gate has sufficient evidence.
- `B(c,w)`: measured benefit/cost vector for candidate c under workload w.
- `T`: supported target matrix.
- `O`: named ownership/review capacity.
- `K(c)`: lifecycle/maintenance cost and risk, not reducible to one universal number.
- `Δ`: material end-to-end benefit margin required by the decision.

A weighted score may compare eligible candidates, but it must never compensate for missing hard evidence. Unknown is not pass. Quantitative weights are policy and sensitivity should be reported.

## Mechanisms, Invariants, or Proof Structure

### Gate proof

For candidate c, eligibility is conjunction over hard requirements and targets: for every r in `R_h` and t in T, suitable evidence establishes c meets r on t. One false or missing conjunct rejects c or narrows supported T. Preference optimization begins only over eligible candidates.

### Benefit proof structure

Define representative workload set W and application metric vector. Reproduce candidate/baseline runs with the same semantics/environment. Require correctness gates pass, then show benefit exceeds Δ across required W without violating tail, fairness, resource, power, or lifecycle constraints. State cases where it does not.

### Executable decision-gate model

The following model demonstrates noncompensatory gates. A mutex fails the stipulated no-block gate, a custom algorithm lacks proof evidence, and only a qualified library passes. The labels are illustrative inputs, not a universal recommendation or scoring formula.

<!-- bijux-verify: {"id":"lock-free-decision-gates","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"eligible=['qualified_library']\nselected=qualified_library\nrejected_mutex=['no_block']\nrejected_custom=['reviewed_proof']\nscore_selected=8\n","stderr":""}} -->
```python
hard = ["semantics", "no_block", "qualified_atomic", "reviewed_proof", "bounded_resources"]
candidates = {
    "mutex": {"semantics": True, "no_block": False, "qualified_atomic": True, "reviewed_proof": True, "bounded_resources": True, "score": 10},
    "custom": {"semantics": True, "no_block": True, "qualified_atomic": True, "reviewed_proof": False, "bounded_resources": True, "score": 12},
    "qualified_library": {"semantics": True, "no_block": True, "qualified_atomic": True, "reviewed_proof": True, "bounded_resources": True, "score": 8},
}
eligible = [name for name, facts in candidates.items() if all(facts[item] for item in hard)]
selected = max(eligible, key=lambda name: candidates[name]["score"])
print(f"eligible={eligible}")
print(f"selected={selected}")
print(f"rejected_mutex={[item for item in hard if not candidates['mutex'][item]]}")
print(f"rejected_custom={[item for item in hard if not candidates['custom'][item]]}")
print(f"score_selected={candidates[selected]['score']}")
```

### Minimum evidence ledger

| Claim | Evidence |
|---|---|
| semantics | sequential spec, proof/review, history/model tests |
| source safety | language memory model, unsafe/lifetime/reclamation review |
| progress | algorithm proof plus complete-path and target qualification |
| resources | worst-case/stall bounds and overload policy |
| performance | reproducible application-relevant workload matrix |
| lifecycle | failure, cancellation, close, drain, restart, unload tests |
| maintainability | owners, docs, change gates, dependency/upgrade plan |
| safety/security | named human review and threat/hazard evidence |

## Alternatives and Trade-Offs

| Candidate | Typical advantage | Principal obligation/risk |
|---|---|---|
| Mutex/reader-writer lock | small proof surface, tooling, fairness options | blocking, holder preemption/failure, contention |
| Bounded queue/delegation | ownership and overload become explicit | owner/queue latency and shutdown |
| Immutable shared snapshot | simple read lifetime/version consistency | copy/refcount/retained-version cost |
| Sharding | removes global contention | global operations, skew, migration |
| Mature lock-free library | amortized expertise and portability | contract fit, dependency, target/reclaimer limits |
| Custom lock-free | exact specialized contract/progress | maximal proof, unsafe, lifecycle, owner risk |
| Wait-free specialized algorithm | per-operation step bound under model | complexity, space, constants, target assumptions |
| Remove shared state | eliminates synchronization class | architectural redesign and aggregation semantics |

The default is the simplest eligible candidate, not the simplest code snippet. Sometimes a mature nonblocking library is simpler overall than a bespoke locked protocol; sometimes one mutex is simpler than an entire reclamation domain.

## Failure Modes and Misconceptions

- **“Locks are always slow.”** Modern locks can spin/park adaptively and win under real workloads.
- **“Lock-free means low latency.”** Starvation, retry storms, allocation, and scheduling remain.
- **“Atomic means lock-free.”** Atomicity can use hidden locks.
- **“One CAS loop is simple.”** Lifetime and lifecycle may dominate the proof.
- **“GC solves reclamation for free.”** It changes lifetime but adds runtime/debt/pause behavior.
- **“A benchmark is the requirement.”** Start from product/progress semantics.
- **“Highest throughput wins.”** Tail, fairness, CPU, memory, energy, and failure can reject it.
- **“Scores can trade safety for speed.”** Hard gates are noncompensatory.
- **“Popular library means suitable.”** Inspect exact contract, target, maintenance, and defects.
- **“Fallback is implementation detail.”** A hidden mutex changes progress.
- **“Tests prove lock-freedom.”** Progress is a universal conditional theorem, not observed luck.
- **“Proof never changes.”** Payloads, destructors, logging, compiler, target, and close can invalidate it.
- **“Feature flag makes rollback safe.”** Concurrent representation migration needs a protocol.
- **“Built means owned.”** Maintenance/reviewer capacity must persist.
- **“Removing clever code wastes investment.”** Sunk cost is not a requirement.

## Worked Examples

### Example 1

**Vague latency request.**

**Situation.** A team says a cache “must be lock-free because latency matters.”

**Reasoning.** Convert this to workload and p99/max objectives. If a tuned mutex meets them under saturation/oversubscription, no hard gate excludes it. Lock-free becomes a preference candidate, not mandate.

**Conclusion.** Performance language must become measurable thresholds before choosing progress machinery.

### Example 2

**Interrupt-context hard gate.**

**Situation.** An enqueue runs in a context where sleeping and acquiring a lock held by preemptible normal code are forbidden.

**Reasoning.** A normal mutex fails a hard gate. Consider a platform-qualified nonblocking/bounded ring or defer minimal work to an owned queue designed for that context. Preallocation, atomic support, overflow, memory order, and consumer failure remain.

**Conclusion.** Explicit execution-context constraints can genuinely justify nonblocking design.

### Example 3

**Hidden wide-atomic lock.**

**Situation.** A pointer/tag implementation uses 128-bit atomic operations, but one supported target reports not lock-free.

**Reasoning.** Safety may hold through a runtime lock, while the progress claim fails. Drop that target, expose a blocking fallback with different contract, or choose another representation/library. Do not average target evidence.

**Conclusion.** Progress qualification is per supported target and full path.

### Example 4

**Microbenchmark without application benefit.**

**Situation.** A stack is 30% faster but accounts for 2% of request CPU.

**Reasoning.** Ideal whole-request gain is below 0.6% before integration effects. Compare actual service metrics and maintenance cost. Unless scale economics or a hard progress need makes that material, simpler synchronization wins.

**Conclusion.** Optimize the system bottleneck, not the most interesting primitive.

### Example 5

**Epoch debt rejection.**

**Situation.** EBR gives high throughput but a paused thread lets retirement reach 6 GB above a 2 GB budget.

**Reasoning.** The candidate fails a hard resource gate even if logical operations remain lock-free. Bound protected duration, adopt hazard/shared ownership, add safe containment/admission, or reject EBR.

**Conclusion.** Resource boundedness is independent of logical progress.

### Example 6

**Library wrapper breaks lifetime.**

**Situation.** A mature hazard-pointer map returns a raw value pointer after its guard is dropped for API convenience.

**Reasoning.** The wrapper discards the library's core lifetime proof. Return copied/owned data or a guard-borrowed handle. Library maturity cannot protect an unsound adapter.

**Conclusion.** Preserve evidence-bearing types across the integration boundary.

### Example 7

**Custom owner gap.**

**Situation.** A custom queue is correct today, but its only memory-model reviewer is leaving.

**Reasoning.** Organizational feasibility fails unless ownership transfers with training, independent review, durable proof/evidence, and change gates. A mature library or locked replacement may be lower risk even if slightly slower.

**Conclusion.** Review capacity is a production dependency.

### Example 8

**Fair baseline comparison.**

**Situation.** Lock-free queue preallocates nodes; mutex queue allocates/logs inside its critical section.

**Reasoning.** The comparison measures allocation/logging placement as well as synchronization. Give both equivalent pooling, payload, telemetry, capacity, and semantics; test low through overload and report tails/resources.

**Conclusion.** Benchmark design must isolate or explicitly attribute differences.

### Example 9

**Safe rollback.**

**Situation.** A canary reveals growing retired memory and operators flip a flag while operations use the old structure.

**Reasoning.** Direct switching can split ownership and lose/duplicate items. Stop admission to the instance, drain/quiesce and transfer state through a verified migration, then route new operations to the baseline; process-level rollout may be safer.

**Conclusion.** Rollback is a concurrency lifecycle protocol, not a Boolean branch.

### Example 10

**Pacemaker event buffer.**

**Situation.** A custom wait-free buffer is proposed because blocking is unacceptable. What justifies deployment?

**Reasoning.** A named timing/safety requirement and target model must exclude simpler qualified designs. Evidence must cover sequential/timing spec, bounded-step proof, memory model, preallocated resources, wrap, fault/cancellation, interrupt interaction, power/reset/persistence, toolchain/hardware, worst-case measurement, independent fallback, maintenance owners, and named clinical, embedded, formal, real-time, hardware, cybersecurity, regulatory, and operations review. A high benchmark score is irrelevant without this case.

**Conclusion.** High-stakes nonblocking code is justified only by a complete independently reviewed safety and ownership argument.

## Cross-Program Connections

- **Software engineering:** architecture decision records, ownership, review gates, dependency policy, and rollback determine sustainability.
- **Performance engineering:** end-to-end attribution and workload matrices prevent microbenchmark-driven complexity.
- **Computer architecture:** atomic widths, cache topology, NUMA, and fallback determine actual progress and cost.
- **Formal methods:** specifications, refinement, memory-model, and liveness proofs make claims reviewable.
- **Operating systems:** execution context, preemption, priority, signals, and scheduling can create genuine hard gates.
- **Reliability engineering:** resource debt, overload, containment, upgrade, and shutdown determine service survival.
- **Security:** unsafe memory and adversarial stalls/retries expand threat models.
- **Safety engineering:** noncompensatory gates and named human review control high-consequence adoption.

## References

1. Maurice Herlihy and Nir Shavit, *The Art of Multiprocessor Programming*, revised first edition, 2012. <https://www.elsevier.com/books/the-art-of-multiprocessor-programming/herlihy/978-0-12-397337-5>
2. Maurice P. Herlihy and Jeannette M. Wing, “Linearizability: A Correctness Condition for Concurrent Objects,” *ACM TOPLAS* 12(3), 1990. <https://www.cs.cmu.edu/~wing/publications/HerlihyWing90.pdf>
3. Maged M. Michael, “Hazard Pointers: Safe Memory Reclamation for Lock-Free Objects,” *IEEE TPDS* 15(6), 2004. <https://doi.org/10.1109/TPDS.2004.8>
4. Trevor Brown, “Reclaiming Memory for Lock-Free Data Structures: There Has to Be a Better Way,” PODC 2015. <https://doi.org/10.1145/2767386.2767436>
5. Tudor David, Rachid Guerraoui, and Vasileios Trigonakis, “Everything You Always Wanted to Know About Synchronization but Were Afraid to Ask,” SOSP 2013. <https://doi.org/10.1145/2517349.2522714>
6. ISO C++ working draft, atomic operations and lock-free queries, continuously maintained; retrieved 2026-08-29. <https://eel.is/c++draft/atomics>
7. Rust Project, standard library atomic module documentation, retrieved 2026-08-29. <https://doc.rust-lang.org/std/sync/atomic/>
8. Oracle, Java SE 21 `java.util.concurrent` package documentation, retrieved 2026-08-29. <https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/package-summary.html>
9. Intel, *64 and IA-32 Architectures Optimization Reference Manual*, current edition; retrieved 2026-08-29. <https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html>
10. Arm, *Arm Architecture Reference Manual for A-profile Architecture*, current documentation; retrieved 2026-08-29. <https://developer.arm.com/documentation/ddi0487/latest/>

## Exercises

### Exercise 1

Distinguish a hard progress requirement from a latency preference. Give one precise example of each and the evidence needed.

### Exercise 2

A library atomic is safe but not lock-free on one target. Enumerate honest product choices and what may not be claimed.

### Exercise 3

Audit a decision based on one high-contention microbenchmark that omits allocation, reclamation, low load, oversubscription, tails, and a tuned mutex. Design a valid comparison.

### Exercise 4

Create a gate-based decision for a read-mostly registry whose readers may block, updates are rare, and dynamic unload must be deterministic. Compare RCU, hazards, atomic shared ownership, and a lock.

### Exercise 5

A railway interlocking team proposes custom lock-free route state to avoid priority inversion. Specify decision gates, implementation evidence, rollout/rollback, and mandatory human review.

## Answers to the Exercises

### Answer 1

A hard requirement: an interrupt-context ring insertion must not sleep or wait for a lock held by preempted normal code; evidence includes exact context rules, full-path progress proof, preallocation, qualified target atomics, bounded capacity/overflow, and worst-case target tests. A preference: request p99 below 2 ms at 100k operations/s; evidence is reproducible end-to-end distributions under declared workload/topology, compared against competent baselines. A preference cannot silently become “lock-free required” when simpler designs meet it.

### Answer 2

The product can exclude the target; expose a documented blocking fallback and make progress capability target-visible; choose a narrower/native representation; select another algorithm/library; or weaken the hard progress requirement through an explicit product decision. It may still claim atomic safety if verified, but cannot claim the operation or all supported targets are lock-free. CI/deployment must detect the capability and tests must cover both lifecycle paths.

### Answer 3

The experiment confounds synchronization with missing production costs and samples only a favorable saturation point. Give every candidate the same contract, capacity, payload, allocation/pooling, reclamation, telemetry, compiler, affinity, and prefill. Include optimized mutex/delegation/library candidates. Run low, representative, burst, saturation, overload, oversubscription, NUMA/SMT, skew, stalled participant, cancellation, and shutdown. Report end-to-end throughput, p50/p99/max, retries/fairness, CPU/context/cache metrics, energy, bytes/debt, callbacks, and failures with repeated runs. Correctness/progress/resource gates precede performance selection.

### Answer 4

No hard nonblocking requirement exists and readers may block, making coarse RCU/EBR debt risky. Atomic shared ownership of an immutable registry snapshot is the leading candidate: acquire a handle briefly, permit reader blocking, and unload only after handles drain. A lock can protect handle acquisition/update but should not be held across reader work. Hazards can pin individual objects across blocking but add domain/unload complexity without a demonstrated need. Gate on exact lifetime, writer semantics, bounded retained snapshots, deterministic close/unload, destructor context, and target support; measure reference traffic. Choose the simplest eligible design meeting p99 and unload limits.

### Answer 5

First require a human-approved route-state sequential and timing specification, hazard analysis, and a precise statement of which lock-holder/preemption failure must be avoided. Gates cover linearizability, bounded/wait-free or qualified progress as actually required, target atomics, memory/reclamation and ABA, bounded descriptors/debt, priority/scheduler behavior, cancellation/commit, persistence/failover, startup/shutdown, cybersecurity, and sustained ownership. Compare priority-inheritance locks, delegation, partitioning, mature qualified libraries, and custom code with worst-case target evidence. Roll out behind a stable interface using formal/model/history, weak-memory, fault, overload, hardware-in-loop, and shadow evidence; rollback uses admission close and quiescent state transfer, not live flag switching. Named signaling-domain, functional-safety, real-time, formal-methods, compiler/hardware, cybersecurity, operations, independent assurance, and regulatory reviewers must approve requirements, evidence, fallback, and residual risk. No score can compensate for a failed safety gate.
