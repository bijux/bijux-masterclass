---
module_id: CONPAR-059
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 59
title: Contention Management in Nonblocking Algorithms
status: complete
last_verified: 2026-08-29
---

# Contention Management in Nonblocking Algorithms

## One-Page Review

### Governing question

How can retries, cache-line ownership, admission, locality, helping, and alternative execution paths be managed so a correct nonblocking algorithm remains productive under contention without changing its semantics or overstating fairness and progress?

### Essential definitions

- **contention** is simultaneous demand for a shared synchronization location, resource, or abstract transition.
- A **CAS storm** occurs when many participants repeatedly read one value, race to update it, and invalidate one another's cache copies while only one succeeds.
- **retry amplification** is total attempts divided by successful logical operations.
- **backoff** delays retry after conflict; **exponential backoff** expands a delay window after repeated failures, usually with randomization/jitter and a cap.
- **polite spinning** uses architecture/runtime pause or yield hints while waiting, reducing resource pressure without committing an operation.
- **admission control** bounds the number of contenders entering a hot retry region.
- **elimination** pairs complementary operations so they complete away from a central synchronization point.
- **combining** lets one participant execute or batch requests for others; flat combining commonly uses a combiner lock and is not intrinsically lock-free.
- **sharding** partitions state so independent operations contend on different locations.
- **fairness** concerns who progresses; aggregate throughput and lock-free system progress can coexist with starvation.

### Central model, mechanism, or theorem

Contention management is a policy around a proved logical kernel. After a failed conditional update, refresh the full witness, then choose when and where to retry or whether to use a semantics-preserving alternate path. Backoff can reduce simultaneous attempts and coherence traffic, but deterministic synchronized delays can preserve collisions; randomized capped delays spread arrivals probabilistically. Elimination, combining, sharding, or delegation may reduce the central bottleneck only when their own linearization, ownership, cancellation, and lifecycle proofs hold. No policy may turn a failed attempt into an abstract effect or weaken the original specification silently.

### Critical invariants

One logical operation has at most one committed effect and one result. Failed attempts repeat no non-idempotent side effects and refresh all derived state. Delay occurs before a new attempt, never while holding a resource needed by competitors. Backoff arithmetic is bounded and overflow-safe. Random seeds are independent enough for the stated model and controllable in tests. Elimination pairs complementary operations exactly once within both intervals. Helpers/combiner requests have explicit ownership and cancellation states. Admission tokens cannot leak. Shards preserve global semantics. Parking and fallback paths retain memory ordering. Progress, fairness, latency, power, and overload are measured separately.

### Common failures

Code retries immediately in a tight loop; all contenders use identical deterministic delay; exponential arithmetic overflows; sleeps while holding a hazard, epoch guard, allocator lock, or scarce token; caches a stale successor across delay; repeats logging/allocation/destruction in the CAS loop; interprets retry budget exhaustion as abstract failure; parks without lost-wakeup protection; calls a blocking combiner lock-free; lets elimination pair two pushes; completes a cancelled request later without reporting commitment; shards a globally ordered object without reconciliation; benchmarks only throughput; or tunes to one core count and topology.

### Compact example

Four threads fail one CAS at the same instant. Fixed one-slot delay makes all four retry together and collide again. Capped exponential windows with distinct deterministic test jitter choose slots 0, 1, 3, and 6; only actual slot collisions contend. This can reduce attempts, but it proves neither starvation freedom nor real-machine speed. The retry still reloads the shared state after waiting and commits only through the original CAS.

### Connections

[Compare-and-Swap Loops](026-compare-and-swap-loops.md) supplies safe retry structure. [False Sharing and Cache-Line Contention](029-false-sharing-and-cache-line-contention.md) explains coherence effects. [Obstruction-Free, Lock-Free, and Wait-Free Progress](051-obstruction-free-lock-free-and-wait-free-progress.md) supplies progress quantifiers. [Linearizability Proofs](058-linearizability-proofs.md) constrains every alternative path.

## Governing Question

How should an engineer diagnose and control contention in a nonblocking design while preserving linearizability, target-qualified progress, bounded resources, cancellation truth, and production observability?

The central lesson is that faster retry is often worse retry. The objective is completed useful work under a declared workload, not maximum atomic-instruction rate.

## Why This Matters

A lock-free algorithm can scale poorly. On one hot CAS word, every successful transition invalidates other cores' copies. Losing threads re-read, recompute, and try again, consuming interconnect bandwidth while making no abstract progress. Throughput can flatten or fall; per-thread latency and energy can worsen even as some operations continue completing.

Contention policy is workload- and topology-dependent. Short delays can let a winner finish and caches settle. Too much delay leaves hardware idle and inflates tail latency. Oversubscribed systems need different spin/park behavior from dedicated cores. NUMA makes remote ownership transfers expensive. Bursty traffic needs admission and capacity policy, not only a larger backoff cap.

Structural approaches can dominate tuning. Sharding removes shared ownership; elimination lets complementary operations cancel; combining amortizes synchronization; batching changes work granularity; a mutex may outperform a retry storm. Each changes proof and operational surfaces, so measurement and correctness evolve together.

## Prerequisites and Retrieval

Retrieve:

- retry witness refresh from [Compare-and-Swap Loops](026-compare-and-swap-loops.md);
- cache coherence and false sharing from [False Sharing and Cache-Line Contention](029-false-sharing-and-cache-line-contention.md);
- bounded queues/admission from [Thread Pools and Bounded Work Queues](019-thread-pools-and-bounded-work-queues.md);
- cancellation commitment from [Cancellation and Timeouts](036-cancellation-and-timeouts.md);
- progress levels from [Obstruction-Free, Lock-Free, and Wait-Free Progress](051-obstruction-free-lock-free-and-wait-free-progress.md); and
- one-effect proof obligations from [Linearizability Proofs](058-linearizability-proofs.md).

Retrieval prompt: place eight callers between load and CAS on one location, let one win, and account for useful transitions, failed RMWs, invalidations, repeated local work, and the worst-served caller.

## Learning Objectives

After completing this module, a learner can:

1. distinguish logical contention, cache-line contention, retry amplification, and overload;
2. instrument attempts, failures, ownership transfers, latency, and fairness;
3. design bounded randomized backoff without stale-state or overflow defects;
4. choose spin, yield, park, admission, or fallback by scheduler/topology assumptions;
5. explain elimination, combining, delegation, batching, and sharding trade-offs;
6. preserve linearizability and exact-once ownership across alternate paths;
7. qualify lock-free progress when allocation, parking, or locks enter the path;
8. test synchronized starts, skew, oversubscription, NUMA, cancellation, and shutdown;
9. compare throughput, tail, fairness, energy, and resource debt; and
10. decide when to replace rather than tune a nonblocking structure.

## Core Exposition

### Model the hot path

Let N active operations contend for atomic location X. Each attempt loads witness w, computes desired d(w), and conditionally updates X. At most one incompatible desired value can win for one observed version. Losers perform work and coherence traffic without an abstract effect.

Define attempts A, successful logical operations C, failed attempts F=A-C, and retry amplification `RA=A/C` when C>0. Track per-operation attempts, not only totals. Mean RA can look acceptable while one caller retries thousands of times.

Contention can also occur outside the visible CAS: allocator metadata, hazard records, retire queues, descriptors, global epochs, scheduler run queues, logging counters, or cache lines containing unrelated fields. Profile the whole operation and hardware counters where reliable; do not tune the line you guessed.

### Retry correctness before policy

Every retry starts from a coherent new observation. A delay does not preserve the old witness. After waiting, reload X and every proposal derived from it. Failed CAS commits nothing, so side effects such as allocation that cannot be reused, random external calls, billing, metrics counted as success, or destruction must not repeat accidentally.

Place backoff after conflict is established and before the next contested attempt. Do not sleep while holding a hazard/epoch guard if that can block reclamation, or while owning a resource that the winner needs. Long retry loops need cancellation checks, but a cancellation observed after commitment cannot change the result to “no effect.”

Contention management must preserve the sequential specification. A retry budget may return a distinct `busy/overloaded` result only if the API specifies it and no effect committed. Otherwise the budget selects a slower correct path or remains an internal performance limit.

### Why immediate retry collapses

With many synchronized contenders, one success changes X. All losers soon acquire the new cache line and attempt another exclusive operation. Another wins, invalidating the rest. The system repeatedly pays O(N) competing traffic for O(1) useful commits. Exact cost depends on cache protocol, topology, RMW implementation, and workload, but the amplification mechanism is durable.

Test-and-test-and-set reduced lock traffic by spinning on ordinary reads before an exclusive instruction; queue locks distributed waiting locations. These blocking-lock lessons transfer conceptually: local waiting and controlled ownership handoff reduce hot-line traffic. They do not automatically convert a nonblocking object into a queue lock.

### Backoff design

A common policy chooses delay uniformly or pseudo-randomly in `[0,W)`, where W grows after consecutive conflicts up to `W_max`, then resets or shrinks after success. Randomization breaks synchronized phase; a cap bounds latency and arithmetic. Saturating multiplication/shift avoids overflow. Jitter units can be pause iterations, scheduler yields, or time—each has different assumptions.

Deterministic tests inject a seeded delay chooser and virtual time. Production independence must be evaluated: identical per-thread seeds or correlated clocks can synchronize contenders. Cryptographic randomness is usually unnecessary; reproducible, fast, sufficiently decorrelated sequences are preferable.

Backoff is probabilistic contention reduction, not fairness. An unlucky caller can repeatedly choose crowded slots. Add age, queueing, handoff, helping, or fallback if per-operation service matters. Aging can itself create herds if every old caller becomes urgent together.

### Spin, yield, and park

Spinning is appropriate when the expected wait is shorter than scheduling/parking overhead, a core is available, and a competing owner is running. Use architecture/runtime pause hints to reduce pipeline and shared-resource pressure. A fixed spin count should be justified by measured wait distributions.

Yielding is a scheduler hint, not a guaranteed handoff. It can return immediately to the same task or delay it excessively. Parking saves CPU under long waits/oversubscription but introduces a wait/wake protocol; sequence counters or condition-style rechecks must prevent lost wakeups. Parking makes that path blocking even if the logical kernel uses CAS.

Adaptive policies observe conflict, queue length, CPU availability, or wait duration. Feedback can oscillate and instrumentation can contend. Use hysteresis, bounded states, and safe defaults. Target configuration and scheduler version belong in evidence.

### Admission control

When demand exceeds useful parallelism, bound the contenders allowed into the hot region. Others wait in a queue, perform alternate work, or receive explicit overload. A semaphore/front-end queue can make inner attempts efficient, though the end-to-end operation is then blocking and its queue needs fairness, cancellation, and capacity semantics.

Admission is often better than retrying until memory or latency collapses. Choose limits from service-time and topology measurements, not CPU count alone. Per-NUMA-node admission can preserve locality but must prevent global starvation.

Tokens require exact ownership. Cancellation/exception returns a token once; successful handoff cannot lose it; shutdown drains waiters. Overload before entry must be distinguishable from an operation that already committed.

### Elimination

For a stack, overlapping push(v) and pop can exchange v in an elimination arena without modifying the central head. The pair linearizes at the successful rendezvous within both intervals. Two pushes cannot eliminate; two pops cannot synthesize a value. A slot protocol must prevent duplicate matching, ABA, timeout races, and reuse defects.

Elimination excels when complementary operations overlap. A push-heavy workload still reaches the central stack. Arena width and wait time are adaptive parameters: too narrow collides, too wide misses partners. Each slot adds cache topology, memory ordering, and cancellation states.

An elimination-backoff stack can remain lock-free under its published proof, but a custom arena is not correct by resemblance. Verify the central and elimination paths together, including exact value ownership and a timeout concurrent with match.

### Combining, delegation, and batching

Flat combining publishes requests; one combiner acquires a lock, scans requests, applies several to a sequential structure, and publishes results. It reduces synchronization and cache traffic at the cost of serialization and combiner dependency. It is generally blocking unless a particular algorithm proves otherwise.

Delegation can use a dedicated owner thread, mailbox, or helper descriptors. Batching amortizes one ownership transfer across operations and can exploit locality/vectorization. It also increases queueing delay and makes cancellation after pickup subtle. Define the linearization of each request and whether batch failure is atomic or per-item.

A failed/stalled combiner can block everyone. Handoff, lease, or helping mechanisms may recover but enlarge proof scope. Never label a design lock-free because clients do not take the combiner lock directly.

### Sharding and distributed ownership

Partition counters, maps, pools, or queues by key/core/NUMA node so independent operations avoid one root. Sharding changes semantics when operations need global FIFO, exact total, uniqueness, resize, or snapshot. Aggregation can be approximate, delayed, locked, or transactional; choose explicitly.

Locality-aware routing can reduce remote cache-line migration. Hot keys can defeat even distribution. Dynamic reshaping needs safe migration and a stable routing/version protocol so an operation neither disappears nor executes twice.

Striping unrelated metadata is useful only if each shard/cache line owns an independent update domain. Padding a fundamentally single total does not remove the required global transition.

### Helping and priority

Helping turns observed incomplete work into useful progress rather than pure interference. Descriptors identify the target operation, required transition, and exact result. Helpers must finish one operation once; they cannot repeat external side effects. Helping can support lock-free progress but consume effort on work the owner no longer wants.

Priority systems are difficult. A high-priority caller can repeatedly lose CAS to low-priority traffic; aggressive high-priority retry can starve others and saturate the line. Priority-aware admission/delegation or a suitable lock may provide clearer bounded inversion. Scheduler priority does not automatically order atomics.

Real-time systems need step/latency bounds, not average backoff success. Random delay complicates worst-case analysis. Use a design with an analyzable bound and qualified platform rather than tuning a stochastic policy into a safety claim.

### Measurement methodology

Define operations, read/write mix, key distribution, burst pattern, duration, prefill, payload, allocation/reclamation, core affinity, SMT, NUMA placement, oversubscription, target atomics, and background load. Warm up where relevant and retain raw distributions.

Report throughput and useful commits, attempts/success, per-operation retries, p50/p95/p99/max latency, starvation/oldest age, CPU time, context switches, parking, migrations, cache/RFO traffic if available, energy, allocation, retired bytes, and fairness. Normalize by completed operations, not attempted loops.

Run low contention to catch backoff overhead, moderate contention for crossover, saturation, and overload. Test complementary and skewed mixes for elimination; small and large batches for combining; hot shards and migrations for partitioning. Compare to a well-engineered mutex/bounded queue baseline.

### Lifecycle, failure, and observability

Backoff timers, parked waiters, arena slots, request records, combiner ownership, admission tokens, and shards all need close/cancellation states. Close prevents new admission, wakes waiters, resolves unmatched elimination, stops combiners after queued ownership is settled, drains reclamation, and destroys state only after quiescence.

Expose conflict rate, RA histogram, longest retry/age, backoff window, spin/yield/park counts, admission queue/rejections, arena match/collision/timeout, combiner batch/hold time, shard skew/migration, cancellation-after-commit, and fallback use. Sample telemetry without creating a new hot atomic.

Policy can change at runtime only within verified bounds. Record version/configuration with evidence and roll back on tail, fairness, CPU, or debt regression—not merely throughput.

## Definitions and Notation

- `A`: total conditional-update attempts.
- `C`: completed logical operations/commits.
- `F=A-C`: failed attempts when each commit uses one successful attempt.
- `RA=A/C`: retry amplification for C>0.
- `k_i`: consecutive conflicts for operation i.
- `W_i=min(W_max, W_0·2^{k_i})`: illustrative capped window with saturating arithmetic.
- `D_i`: chosen delay in `[0,W_i)` under a declared chooser.
- `N`: admitted simultaneous contenders for one hot domain.
- `λ`: offered operation rate; `μ`: sustainable completion rate under the workload.
- **useful work**: state transition or computation needed by a completed operation.
- **wasted retry work**: discarded computation/traffic from an uncommitted attempt.

When `λ>μ`, a stable system must reject, defer with bounded queueing, reduce demand, or increase effective capacity. Backoff alone cannot make unbounded offered work disappear.

## Mechanisms, Invariants, or Proof Structure

### Safety preservation

Treat wait/yield/park as stuttering steps: they change no abstract object state. After them, refresh the complete witness. The original commitment event remains the linearization point. Any alternate elimination/combining/shard path must map to one legal abstract transition, and mutual exclusion between paths prevents duplicate effect. Cancellation checks are ordered relative to commitment.

### Progress qualification

For a pure bounded-computation backoff loop, if conflicts imply other successful transitions and an isolated caller eventually attempts, the logical kernel can retain lock-free reasoning. Sleeping/parking, admission queues, combiner locks, allocation, and scheduler dependence qualify end-to-end progress. Random collision probability is not a deterministic termination proof.

### Executable collision model

The model compares identical fixed retry slots with four distinct seeded choices in a capped window. It counts slot pairs that collide. The result demonstrates desynchronization in stipulated choices, not concurrent performance or randomness quality.

<!-- bijux-verify: {"id":"backoff-slot-collision-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"fixed_slots=[1, 1, 1, 1]\nfixed_colliding_pairs=6\nspread_slots=[0, 1, 3, 6]\nspread_colliding_pairs=0\nwindow=8\n","stderr":""}} -->
```python
fixed = [1, 1, 1, 1]
spread = [0, 1, 3, 6]

def colliding_pairs(slots):
    total = 0
    for left in range(len(slots)):
        for right in range(left + 1, len(slots)):
            if slots[left] == slots[right]:
                total += 1
    return total

print(f"fixed_slots={fixed}")
print(f"fixed_colliding_pairs={colliding_pairs(fixed)}")
print(f"spread_slots={spread}")
print(f"spread_colliding_pairs={colliding_pairs(spread)}")
print("window=8")
```

### Decision ladder

1. Prove the untuned operation and instrument actual conflict.
2. Remove false sharing and unrelated bottlenecks.
3. Bound overload/admission before micro-tuning retry.
4. Try bounded pause/backoff with deterministic tests.
5. Evaluate parking only with a correct wake protocol.
6. Consider elimination/combining/sharding when semantics fit.
7. Compare a simpler lock/delegated baseline.
8. Revalidate correctness, progress, lifecycle, and workload matrix.

## Alternatives and Trade-Offs

| Policy | Benefit | Cost or risk |
|---|---|---|
| Immediate retry | minimal low-contention delay | CAS storms and unfairness under load |
| Capped randomized backoff | spreads contenders cheaply | stochastic tail, tuning, no fairness proof |
| Spin then yield/park | adapts short versus long waits | scheduler and lost-wakeup complexity |
| Admission queue | bounds inner contention and overload | blocking/fairness/cancellation semantics |
| Elimination | removes complementary operations from hotspot | workload-specific arena proof |
| Flat combining | batches synchronization and improves locality | combiner lock/dependency and serialized tail |
| Helping/delegation | turns interference into useful completion | descriptor/ownership/cancellation complexity |
| Sharding | removes unnecessary sharing | global order/aggregation/migration costs |
| Mutex/queue lock | predictable ownership and often fairness | blocking, convoying, priority/failure policy |

Choose from workload and required guarantees. A “slower” primitive can yield higher service capacity and far simpler correctness at the actual contention level.

## Failure Modes and Misconceptions

- **“Lock-free scales.”** Progress classification is not a throughput theorem.
- **“More retries mean more progress.”** Failed RMWs create traffic without abstract effects.
- **“Backoff fixes overload.”** Offered load above capacity still needs admission/rejection.
- **“Exponential means unbounded.”** Production windows and arithmetic must cap safely.
- **“Random means fair.”** Probability does not guarantee an individual completion.
- **“Yield hands off.”** Scheduler behavior is platform- and load-dependent.
- **“Park is still lock-free.”** A parked path depends on wake/scheduler behavior.
- **“Sleep with the old witness.”** Shared state must be refreshed after delay.
- **“Elimination is just backoff.”** It adds an alternate linearization/value-transfer protocol.
- **“Combining is nonblocking delegation.”** A combiner lock can block all requests.
- **“Shards preserve FIFO.”** Partitioning changes global order unless reconciled.
- **“Average retries show fairness.”** Inspect per-operation tail and oldest age.
- **“One benchmark chooses the policy.”** Mix, topology, oversubscription, and allocator matter.
- **“Hardware counters prove causality.”** Counter meaning and attribution require controlled experiments.
- **“Tuning is outside correctness.”** cancellation, close, fallback, and alternate paths change proof scope.

## Worked Examples

### Example 1

**CAS-storm accounting.**

**Situation.** Eight threads read one version; one succeeds and seven fail.

**Reasoning.** One logical transition required eight attempts, so RA=8 and F=7 for that wave. If all seven immediately reload and race, the pattern repeats with fewer or renewed contenders. Aggregate completions do not reveal which thread repeatedly loses.

**Conclusion.** Count failed attempts and per-operation retries, not only throughput.

### Example 2

**Deterministic synchronized backoff.**

**Situation.** Every loser waits exactly 100 pause iterations.

**Reasoning.** Similar execution speeds keep phases aligned, so they return together. The delay consumes time without spreading attempts. Add bounded decorrelated jitter and test it deterministically; it still provides no fairness theorem.

**Conclusion.** Delay without phase dispersion can preserve contention.

### Example 3

**Overflowing window.**

**Situation.** Code computes `1 << failures` in a fixed-width integer after many failures.

**Reasoning.** Shift overflow/undefined behavior or wrap can produce zero/tiny delay exactly under extreme contention. Saturate before shifting, cap failures/window, validate units, and test boundaries.

**Conclusion.** Backoff arithmetic is correctness-relevant under adversarial load.

### Example 4

**Stale retry after sleep.**

**Situation.** A queue enqueuer caches last node L and `L.next=null`, sleeps, then CASes that cached link.

**Reasoning.** Other enqueues can link after L; dereference lifetime may also expire. The caller must refresh/protect/validate the queue snapshot after delay. A CAS failure is harmless only if its expected address is valid to access under the language/reclaimer.

**Conclusion.** Backoff delays attempts, not validation obligations.

### Example 5

**Elimination value transfer.**

**Situation.** Push A and pop overlap and meet in one arena slot.

**Reasoning.** The slot state machine pairs complementary operations once, transfers A, and linearizes within both intervals. Timeout must CAS the slot away; if matching wins first, the operation committed and cannot return timeout/no effect. Two pushes must never match.

**Conclusion.** Elimination reduces central contention through a separately proved abstract path.

### Example 6

**Flat-combining label.**

**Situation.** Clients publish requests and one lock-owning combiner executes them.

**Reasoning.** Batching may reduce cache transfers and improve throughput. If the combiner is descheduled while holding the lock, requests wait; the design is blocking absent a recovery proof. Each result must be published exactly once, and cancellation after pickup needs commitment semantics.

**Conclusion.** Delegated execution does not imply nonblocking progress.

### Example 7

**Admission under overload.**

**Situation.** The structure sustains 2 million ops/s while callers offer 5 million.

**Reasoning.** Backoff can reduce wasted attempts but cannot service all demand. Bound admitted contenders and queue, reject excess with explicit pre-commit overload, or shed upstream. Track queue age and tokens through cancellation/shutdown.

**Conclusion.** Stable overload behavior requires a capacity contract.

### Example 8

**NUMA shard skew.**

**Situation.** Four socket-local shards exist, but 80% of keys route to one shard.

**Reasoning.** Average load predicts false scalability. Measure per-shard traffic, remote access, and tails. Repartitioning/migration needs versioned routing and exact-once move; global totals may need a defined stale or locked aggregation.

**Conclusion.** Sharding succeeds only when ownership and workload distribution align.

### Example 9

**Priority-sensitive retry.**

**Situation.** A high-priority control thread repeatedly loses CAS to many low-priority workers.

**Reasoning.** Scheduler priority cannot reserve the cache-line transition. Aggressive spinning can worsen traffic. Use priority-aware admission/delegation or a priority-inheritance-capable lock with analyzable bounds if required; measure worst-case response on the target.

**Conclusion.** Lock-free system progress does not prevent priority inversion or starvation.

### Example 10

**Autonomous-braking command queue.**

**Situation.** Randomized backoff improves average throughput in a braking command queue. Is it acceptable for deployment?

**Reasoning.** Average improvement is insufficient. The safety case needs bounded command admission and age, analyzable worst-case progress, priority/emergency policy, exact cancellation/commit, memory/reclamation proof, target/scheduler/thermal evidence, fault and overload testing, independent fallback, and named automotive-safety, controls, real-time, compiler/architecture, security, operations, and regulatory review. Random trials cannot certify deadlines.

**Conclusion.** High-stakes contention policy requires deterministic safety bounds and human approval.

## Cross-Program Connections

- **Computer architecture:** coherence ownership, interconnect topology, SMT, pause hints, and NUMA shape retry cost.
- **Algorithms:** randomized backoff, elimination, combining, and sharding change expected work and proof structure.
- **Operating systems:** scheduling, preemption, parking, affinity, and priority determine end-to-end behavior.
- **Queueing theory:** offered load, capacity, admission, and waiting tails distinguish contention from overload.
- **Distributed systems:** jitter/backoff and admission recur in network retries, with different failure and state models.
- **Performance engineering:** workload design and per-operation distributions are part of the result.
- **Software engineering:** fallback, cancellation, configuration rollout, and observability must preserve API truth.
- **Safety engineering:** worst-case service and overload response require reviewed deterministic limits.

## References

1. Thomas E. Anderson, “The Performance of Spin Lock Alternatives for Shared-Memory Multiprocessors,” *IEEE TPDS* 1(1), 1990. <https://homes.cs.washington.edu/~tom/pubs/spinlock.pdf>
2. John M. Mellor-Crummey and Michael L. Scott, “Algorithms for Scalable Synchronization on Shared-Memory Multiprocessors,” *ACM TOCS* 9(1), 1991. <https://www.cs.rochester.edu/research/synchronization/pseudocode/ss.html>
3. Danny Hendler, Nir Shavit, and Lena Yerushalmi, “A Scalable Lock-Free Stack Algorithm,” SPAA 2004. <https://doi.org/10.1145/1007912.1007944>
4. Danny Hendler, Itai Incze, Nir Shavit, and Moran Tzafrir, “Flat Combining and the Synchronization-Parallelism Tradeoff,” SPAA 2010. <https://doi.org/10.1145/1810479.1810540>
5. Maurice Herlihy and Nir Shavit, *The Art of Multiprocessor Programming*, revised first edition, 2012. <https://www.elsevier.com/books/the-art-of-multiprocessor-programming/herlihy/978-0-12-397337-5>
6. Dave Dice, Virendra J. Marathe, and Nir Shavit, “Lock Cohorting: A General Technique for Designing NUMA Locks,” PPoPP 2012. <https://doi.org/10.1145/2145816.2145848>
7. Tudor David, Rachid Guerraoui, and Vasileios Trigonakis, “Everything You Always Wanted to Know About Synchronization but Were Afraid to Ask,” SOSP 2013. <https://doi.org/10.1145/2517349.2522714>
8. Intel, *64 and IA-32 Architectures Optimization Reference Manual*, current edition; retrieved 2026-08-29. <https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html>
9. Arm, *Arm Architecture Reference Manual for A-profile Architecture*, current documentation; retrieved 2026-08-29. <https://developer.arm.com/documentation/ddi0487/latest/>
10. Linux kernel documentation, scheduler and locking guidance, current; retrieved 2026-08-29. <https://docs.kernel.org/locking/index.html>

## Exercises

### Exercise 1

Define retry amplification and explain why throughput alone cannot reveal contention fairness or wasted work.

### Exercise 2

For four synchronized callers, compare immediate retry, identical fixed delay, and capped randomized delay. State what each can and cannot guarantee.

### Exercise 3

Audit a CAS loop that allocates/logs on every retry, sleeps with a hazard pointer, then reuses its cached expected pointer. Give a corrected structure.

### Exercise 4

Choose among backoff, admission, elimination, flat combining, sharding, and a mutex for a mixed push/pop stack under oversubscription with strict p99 but no nonblocking requirement. Design the benchmark and decision rule.

### Exercise 5

A medical telemetry aggregator uses sharded lock-free counters and adaptive parking. Design a review for exact totals, overload, cancellation, priority, topology, shutdown, and high-stakes alarms. Separate automation from human review.

## Answers to the Exercises

### Answer 1

With A conditional attempts and C committed logical operations, `RA=A/C` for C>0; failed work is `F=A-C` when one successful attempt implements each commit. Throughput reports C/time but not attempts, coherence cost, energy, or who waits. High throughput can coexist with one operation retrying indefinitely. Record attempts per completion, per-operation retry/age distributions, cache/CPU metrics, and oldest caller alongside throughput.

### Answer 2

Immediate retry minimizes isolated delay but can preserve a synchronized CAS storm. Identical fixed delay shifts the herd in time and may collide again. Capped randomized delay decorrelates attempts probabilistically while bounding the window, often reducing collision expectation. None guarantees fairness, starvation freedom, bounded wall time, or performance on a real scheduler/topology. All must refresh after waiting, use overflow-safe caps, and be tested with controlled seeds plus real workloads.

### Answer 3

Allocation and logging repeat non-idempotent/expensive work; a long sleep pins reclamation; cached pointer/link may be stale or reclaimed. Allocate/construct reusable private state outside the logical retry when possible. Load, protect, validate, derive, attempt CAS; on failure release or adjust protection, record retry in noncontended telemetry, choose bounded delay only after no needed resource is held, then reload/protect/validate everything. Emit success/logical outcome once after commitment. Cancellation before commit cleans private state; after commit reports the effect and completes retirement ownership.

### Answer 4

Start with a mature mutex/queue-lock stack because blocking is allowed and p99 matters; compare against Treiber plus bounded jitter, admission, and a published elimination-backoff implementation. Flat combining is a valid blocking/batched competitor. Test low/moderate/saturated/overload concurrency, oversubscription, push:pop ratios from balanced to one-sided, affinity/NUMA, payload/allocation/reclamation, bursts, and cancellation. Measure throughput, p50/p99/max, oldest age, CPU/context switches, RA, elimination matches, combiner batches, and memory debt. Select the simplest design meeting capacity and p99/fairness across the supported matrix; reject any win limited to one favorable balanced mix.

### Answer 5

Define whether totals must be exact at one instant or may be versioned/eventually aggregated. If exact alarm thresholds span shards, use one versioned snapshot/aggregation protocol or conservative per-shard alarm rules; plain summation can mix times. Bound admission and queue age, distinguish pre-commit overload/cancel from committed increments, and ensure parked waiters use lost-wakeup-safe close. Qualify priority and scheduler behavior; monitor shard skew, retry, parking, dropped samples, aggregation version, and alarm latency. Drain routing, waiters, shard migration, and reclamation before shutdown. Automation includes model/history tests for totals, forced skew/overload/cancel/wakeup, target topology benchmarks, sanitizers/weak-memory tests, and failover/restart evidence. Named clinical, safety, real-time, statistical, compiler/architecture, security, operations, and regulatory reviewers must approve alarm semantics, bounds, fallback, and residual risk. The tuning model does not certify patient monitoring.
