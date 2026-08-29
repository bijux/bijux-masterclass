---
module_id: CONPAR-097
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 97
title: Systematic Concurrency Testing
status: complete
last_verified: 2026-08-29
---

# Systematic Concurrency Testing

## One-Page Review

### Governing question

How can a test harness take control of concurrency and nondeterminism, explore a precisely bounded set of legal executions, reproduce every reported failure, and state what remains outside the model?

### Essential definitions

- A **controlled operation** is an operation whose scheduling or nondeterministic result is chosen and recorded by the test runtime.
- A **transition** is one atomic step in the testing model, such as a modeled read, write, lock action, channel action, task completion, timer, or injected fault.
- An **enabled transition** may legally execute from the current modeled state.
- A **schedule** is an ordered sequence of transition choices, nondeterministic inputs, and modeled faults.
- A **preemption** switches away from an enabled operation; a nonpreemptive switch occurs because the current operation blocks, completes, or yields.
- **systematic exploration** selects schedules according to an explicit search strategy rather than relying only on operating-system timing.
- A **safety property** forbids a finite bad prefix, such as an assertion failure, invalid state, deadlock, or non-linearizable history.
- A **bounded liveness property** requires progress within stated steps, time advances, or fairness assumptions; an unbounded liveness theorem is not established by a finite test.
- **partial-order reduction (POR)** avoids redundant schedules when independent transitions commute without changing relevant behavior.
- **dynamic POR (DPOR)** discovers dependencies while executing and schedules alternative orders needed to cover dependent races.
- **state hashing** identifies previously explored modeled states; its projection must retain every fact relevant to enabledness and properties.
- A **replay trace** identifies exact binary, model, inputs, choices, and tool configuration needed to reproduce an execution.
- A **coverage claim** names the model, bounds, strategy, explored/pruned counts, properties, and unsupported behavior.

### Central model, mechanism, or theorem

Let a modeled state be `s = (P, Q, O, C, E)`: program data `P`, runnable/blocked operations `Q`, synchronization objects `O`, logical clocks `C`, and modeled environment `E`. The scheduler repeatedly chooses one enabled transition `t` and computes `s' = step(s,t)`. A reported trace is sound only if every transition was enabled and preserves the semantics of the chosen language/runtime model. Exploration is complete only relative to the declared state projection, transition semantics, nondeterministic choices, bounds, and reduction algorithm. DPOR may prune two orders only when its dependence relation conservatively classifies all pairs whose order can affect state, enabledness, or a checked property.

### Critical invariants

Every relevant concurrency operation is controlled or recorded as unsupported; initial state and nondeterministic inputs are reproducible; scheduler decisions select only enabled transitions; atomicity boundaries match the model; environment actions are modeled explicitly; replay detects divergence; state hashing includes property-relevant state; reduction never prunes a dependent alternative; bounds are immutable evidence; fairness assumptions are declared; time is logical; safety and liveness results are distinguished; weak-memory behavior uses an appropriate model; failures retain minimized and original traces; and no bounded run is described as a universal proof.

### Common failures

Teams leave a native thread, timer, random source, callback, I/O completion, or allocator outside scheduler control; place yield points only where the bug is already expected; model a compound operation as atomic; use wall-clock sleeps; hash too little state; assume sequential consistency covers relaxed atomics; declare liveness without fairness; prune using an unsound independence rule; replay against a different build; silently repair divergent event IDs; treat a timeout as deadlock; test an unrealistic mock; stop at the first shallow bound forever; discard schedule evidence; or say “all interleavings passed” without stating a finite model.

### Compact example

Two threads each perform a read and then a write for `x = x + 1`. Preserving each thread's order yields six sequentially consistent schedules: two produce `x=2`, while four lose an update and produce `x=1`. One ordinary run may see either result; systematic enumeration exposes both and preserves the failing schedule.

### Connections

[Determinism and Reproducibility](007-determinism-and-reproducibility.md) defines replay inputs. [Happens-Before Relations](023-happens-before-relations.md) defines ordering. [Designing for Replayable Concurrency](070-designing-for-replayable-concurrency.md) supplies stable event identity. [Race Detection and Concurrency Sanitizers](096-race-detection-and-concurrency-sanitizers.md) observes defects in explored executions. The [program roadmap](../ROADMAP.md) next turns traces into performance evidence.

## Governing Question

What execution model, control boundary, search strategy, reduction rule, oracle, bound, replay contract, and evidence ledger are sufficient to make a concurrency-test result reproducible and honestly scoped?

Systematic concurrency testing bridges ordinary tests and formal verification. It executes real or instrumented code under a controlled scheduler, but its conclusion remains conditional on modeled operations, search limits, and specification quality.

## Why This Matters

Concurrent defects depend on rare orderings. Stress testing gives the operating system many opportunities but little control: a billion repetitions can miss one decisive preemption, and a debugger can perturb the schedule. A systematic scheduler instead chooses the next operation, explores alternatives, and emits the choice sequence that caused a violation.

Control alone is insufficient. Real programs consult clocks, random generators, files, networks, kernels, devices, allocators, foreign runtimes, and weak-memory hardware. Hidden nondeterminism breaks replay and invalidates coverage. State spaces also grow combinatorially. A useful system therefore defines its semantic boundary, chooses sound reductions and pragmatic bounds, checks meaningful properties, and retains evidence.

The production objective is not “run every interleaving.” It is to establish: every explored trace was legal in the declared model; all executions within a precise bounded claim were explored or soundly represented; failures replay; unsupported behavior is visible; and deeper or complementary evidence is scheduled according to risk.

## Prerequisites and Retrieval

Retrieve:

- races, deadlock, progress, determinism, happens-before, atomics, and replay from [Race Conditions and Atomicity Violations](005-race-conditions-and-atomicity-violations.md), [Deadlock, Livelock, and Starvation](006-deadlock-livelock-and-starvation.md), [Determinism and Reproducibility](007-determinism-and-reproducibility.md), [Happens-Before Relations](023-happens-before-relations.md), [Acquire and Release Ordering](027-acquire-and-release-ordering.md), [Relaxed Atomics](028-relaxed-atomics.md), and [Designing for Replayable Concurrency](070-designing-for-replayable-concurrency.md);
- task graphs, work stealing, nonblocking progress, and reclamation from [Task Parallelism and Dependency Graphs](041-task-parallelism-and-dependency-graphs.md), [Work Stealing](047-work-stealing.md), [Obstruction-Free, Lock-Free, and Wait-Free Progress](051-obstruction-free-lock-free-and-wait-free-progress.md), [Hazard Pointers](055-hazard-pointers.md), and [Epoch-Based Reclamation](056-epoch-based-reclamation.md); and
- dynamic observations from [Race Detection and Concurrency Sanitizers](096-race-detection-and-concurrency-sanitizers.md).

Retrieval prompt: write the invariant and oracle; enumerate threads/tasks/processes, synchronization APIs, atomics and memory model; define controlled/uncontrolled operations; specify initial data, inputs, faults, time and environment model; record atomic transition boundaries; enabledness/dependence; safety/liveness/fairness; bounds/search/reduction/state projection; replay identity; minimization; toolchain; evidence retention; CI depth; and unsupported surfaces.

## Learning Objectives

After completing this module, a learner can:

1. distinguish stress, randomized, systematic, model-checking, and proof evidence;
2. define scheduler-visible transitions and an explicit state machine;
3. control tasks, timers, inputs, callbacks, faults, and external effects;
4. choose step, preemption, thread, queue, message, fault, and time bounds;
5. explain sound state hashing, cycle detection, POR, and DPOR obligations;
6. design assertion, invariant, deadlock, bounded-liveness, and linearizability oracles;
7. preserve and minimize replay traces without changing their semantics;
8. separate sequentially consistent exploration from weak-memory checking;
9. integrate bounded searches and sanitizer combinations into CI; and
10. review high-stakes systematic-test evidence without claiming certification.

## Core Exposition

### Define the execution model

Start with a finite test scenario and a transition system `(S, T, s0)`. `S` contains all modeled states, `T(s)` the enabled transitions at `s`, and `s0` the reproducible initial state. A transition has stable identity, actor, kind, object, precondition, state transformer, and observable events. The scheduler chooses; application code cannot consult native timing to influence modeled behavior.

Control thread/task creation and completion; lock, condition, semaphore, barrier, channel and future operations; atomic accesses at the granularity supported by the checker; yields; logical timers; cancellation; and selected allocation or fault points. Intercepting only explicit `yield()` is rarely sufficient because synchronization APIs and runtime callbacks introduce decisive choices.

The model must neither invent illegal behavior nor hide legal behavior within its claim. If a queue operation is modeled atomically, the claim covers the queue's specified operation, not bugs inside an unmodeled implementation. If production uses a foreign library that spawns uncontrolled threads, either instrument/model it, replace it with a validated deterministic abstraction for this property, or mark the surface unsupported.

### Make the environment deterministic

Reset static/global state for every schedule. Replace wall time with a logical clock advanced by scheduler decisions. Treat simultaneous timer expirations as alternative orders when either is legal. Seeded randomness is reproducible only if call order and generator/version are fixed; stronger control represents each permitted nondeterministic choice directly.

Model files, networks, services and devices as deterministic state machines that can return configured values, delays, disconnects, duplicates, reordering, partial operations, and failures. Record the fault alphabet and limits. A mock that always succeeds proves little; an overpermissive mock can create impossible failures. Validate abstraction fidelity against interface specifications, integration tests, and production traces stripped of sensitive data.

Side effects must not escape and repeat across schedules. Use isolated stores, transactional fixtures, idempotency keys, or a pure model. Never systematically explore code that can send real messages, charge accounts, actuate equipment, or mutate production state.

### Enumerate a small state space

This executable model lists all six interleavings that preserve each thread's read-before-write order. It demonstrates a lost update under sequential consistency only; it does not model native machine instructions, compiler transformations, weak memory, or a complete scheduler.

<!-- bijux-verify: {"id":"two-thread-lost-update-schedules","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"schedule=R0,W0,R1,W1 final=2\nschedule=R0,R1,W0,W1 final=1\nschedule=R0,R1,W1,W0 final=1\nschedule=R1,W1,R0,W0 final=2\nschedule=R1,R0,W1,W0 final=1\nschedule=R1,R0,W0,W1 final=1\nfinal_1_count=4\nfinal_2_count=2\n","stderr":""}} -->
```python
schedules = [
    ["R0", "W0", "R1", "W1"],
    ["R0", "R1", "W0", "W1"],
    ["R0", "R1", "W1", "W0"],
    ["R1", "W1", "R0", "W0"],
    ["R1", "R0", "W1", "W0"],
    ["R1", "R0", "W0", "W1"],
]
counts = {1: 0, 2: 0}
for schedule in schedules:
    shared = 0
    local = [0, 0]
    for event in schedule:
        actor = int(event[1])
        if event[0] == "R":
            local[actor] = shared
        else:
            shared = local[actor] + 1
    counts[shared] += 1
    print(f"schedule={','.join(schedule)} final={shared}")
print(f"final_1_count={counts[1]}")
print(f"final_2_count={counts[2]}")
```

For actors with transition counts `n1,...,nk`, the number of raw interleavings preserving actor-local order is `(sum ni)! / product(ni!)` before blocking, data, inputs, faults, or relaxed-memory choices. Even small scenarios explode. Design small tests around one invariant and use abstraction, reduction, and bounds deliberately.

### Choose search bounds honestly

A step bound limits transitions; a depth bound may miss long prefixes. A preemption bound limits switches away from an enabled actor and often prioritizes shallow concurrency bugs without cutting nonpreemptive progress. A context-switch bound may also count blocking switches. Thread/task, pending-operation, queue, allocation, message, fault, retry and logical-time bounds constrain other axes.

Use iterative deepening: finish bound 0 before 1, preserve completed-bound evidence, then deepen according to risk and budget. State the exact semantics because two tools may count preemptions differently. “Passed at preemption bound 2, maximum 1000 steps, three actors, one injected timeout” is reviewable; “systematically tested” is not.

Bounds can alter reachability. A too-small queue prevents the production state; a step cutoff may label slow progress as failure; a preemption limit may miss a bug requiring several forced switches. Record truncated/frontier states separately from passed terminal executions. Never infer completeness beyond the finished finite region.

### Reduce equivalent schedules soundly

Two enabled transitions are independent only if both orders remain enabled and lead to equivalent property-relevant states. Reads of disjoint immutable data may commute. Writes to the same location, send/receive on related channels, lock operations on the same lock, cancellation versus completion, timer versus timeout state, allocation/reclamation, or transitions affecting an oracle are dependent.

POR selects representative orders of independent transitions. DPOR observes conflicts in an execution and adds backtracking choices so dependent alternatives are explored. The reduction's soundness depends on instrumentation and dependence classification: an invisible shared access can make a pruned order decisive. Log explored executions, transitions, backtracks, pruned alternatives, cutoff reasons, and algorithm/tool version.

Stateful search hashes a canonical state and avoids revisiting it. Include program data, actor control locations, synchronization/object generations, pending messages/timers/faults, logical time where relevant, and monitor state. Excluding a retry counter can merge a state about to fail with one that can continue. Including raw addresses or irrelevant counters can prevent useful merging. Hash collisions need a defensible equality strategy.

Cycle detection can expose deadlock or liveness cycles, but a repeated projected state is meaningful only under declared fairness and environment behavior. A cycle in which a continuously enabled actor is never chosen may be unfair; a production scheduler may nevertheless provide no fairness guarantee. Report both assumption and counterexample.

### Specify useful oracles

Assertions check local facts; global invariants inspect modeled state after relevant transitions. Deadlock is a nonterminal state with no enabled transition, not merely elapsed wall time. Livelock has enabled steps but no required progress. Starvation concerns an operation under a stated scheduling/fairness condition. Define quiescence, success, expected blocking, and shutdown explicitly.

For concurrent objects, record invocation/response histories and check whether completed operations plus permitted pending-operation treatment can be ordered into a legal sequential specification while respecting real-time precedence. Linearizability testing needs unique operation IDs, arguments, results, object generations, and a complete enough history; a passing tiny history is not a proof for all clients.

Metamorphic and conservation properties help when exact outputs vary: no item is lost or duplicated, credits equal debits, ownership is unique, completed futures resolve once, sequence numbers remain monotone, and resources are eventually reclaimed within a declared horizon. Oracles must not depend on the same flawed implementation logic.

### Treat liveness separately

Finite systematic tests naturally refute safety: a finite bad trace is evidence. Liveness says something good eventually happens and requires infinite-execution reasoning or bounded surrogates. Define a progress event, horizon, environment assumptions, and scheduler fairness. For example: “every accepted request completes or is cancelled within 500 controlled transitions when the service model eventually responds and weak fairness schedules continuously enabled tasks.”

If the bound expires, classify incomplete, bounded-liveness violation, or resource cutoff according to policy; do not automatically call it deadlock. For stronger liveness claims use a model checker with cycle/fairness reasoning or a formal proof tied to implementation assumptions.

### Preserve exact replay

A trace header identifies source revision, binary digest, compiler/runtime/tool versions, model/schema version, platform, test and initial-state digest, search strategy, bounds, memory model, and environment/fault configuration. Each event records stable actor and operation IDs, enabled-set digest, chosen transition, nondeterministic value/fault, and relevant state/monitor digest.

Replay must verify that the recorded choice is enabled and the enabled-set/state digests agree. If code changes or hidden nondeterminism causes divergence, stop at the first mismatch and report it. Silently choosing a “similar” actor destroys evidence. Retain the original trace; derive minimized traces as linked artifacts with a proof that the same oracle and failure identity remain.

Minimization can remove actors, inputs, faults, operations, or preemptions, but each candidate must replay against the same build/model. A smallest trace is not necessarily the clearest; retain a readable causal slice and full execution metadata.

### Cover weak memory explicitly

An interleaving scheduler that treats memory operations as sequentially consistent cannot establish C/C++/Rust relaxed-memory correctness. Compilers and hardware allow behaviors not representable as a simple interleaving of source operations. Use a checker whose documented semantics cover the relevant language memory model and atomics, such as a suitable Loom or GenMC configuration, and pin its version/options.

Even then, audit unsupported intrinsics, assembly, foreign code, reclamation assumptions, allocation identity, and compiler lowering. Litmus tests validate intended ordering locally; sanitizers observe executed conflicts; architecture testing adds empirical evidence. None substitutes automatically for a language-model proof.

### Combine evidence and operate in CI

Run focused deterministic cases per change at low iterative bounds, retaining failures and coverage ledgers. Run deeper bounds, more scenarios, faults, platforms, weak-memory models, and sanitizer combinations periodically. Shard by immutable scenario/bound ranges and prevent duplicate or missing work. A job is not passed if it aborts before the target, truncates silently, loses traces, or uses an unsupported operation.

Track scenario/model versions; finished bound; explored terminal/failing/cutoff executions; transitions; backtracks; reductions; unique states; replay success; minimization; wall and CPU cost; and unsupported events. Trends reveal state explosion or lost control. Counts are evidence metadata, not quality scores.

When combining a controlled scheduler with a dynamic sanitizer, ensure the instrumentation/runtime combination is supported. A sanitizer finding gains a reproducible schedule; scheduler perturbation and tool blind spots still apply. Also run optimized production-like integration and stress tests because deterministic models intentionally replace parts of reality.

### Security, operations, and high-stakes limits

Schedule artifacts can contain inputs, identifiers, paths, state digests, message content, fault details, and architecture. Minimize sensitive payloads; use synthetic/deidentified cases; encrypt and restrict evidence; bound retention and volume; and isolate untrusted tests. Deterministic models must never connect to production actuators or customer systems.

High-stakes use requires named concurrency/memory-model, language/runtime/toolchain, domain, safety, security/privacy, operations, quality/regulatory, human-factors/accessibility, ethics, and independent validation reviewers. Systematic testing contributes counterexamples and bounded evidence; it does not certify a controller, establish clinical efficacy, or replace hazard analysis and independent verification.

## Definitions and Notation

- `s0`: reproducible initial modeled state.
- `T(s)`: enabled transitions at state `s`.
- `step(s,t)`: successor after enabled transition `t`.
- `sigma = <t0,...,tn>`: recorded schedule, including modeled choices/faults.
- `B`: vector of step, preemption, actor, resource, fault and logical-time bounds.
- `D`: conservative dependence relation used by reduction.
- `H(s)`: canonical state projection/hash with collision policy.
- `Phi`: safety oracle or monitor; `Psi_h`: liveness property within horizon `h`.
- `M`: declared language/runtime/environment semantics.
- `E`: evidence ledger: build/model/input digests, strategy, bounds, counts, traces, results, limitations and reviewers.
- **relative completeness**: all executions in `(M, s0, B)` are explored or soundly represented under the declared reduction; never an unqualified program proof.

## Mechanisms, Invariants, or Proof Structure

### Model and control proof

Inventory every source of concurrency/nondeterminism; map it to a controlled transition or explicit unsupported entry. Show atomic boundaries, enabledness, reset semantics, logical time, environment fidelity, weak-memory scope, and known abstraction gaps.

### Exploration proof

Pin search/reduction/state algorithms and bounds. For every choice, prove the transition was enabled; for every pruned alternative, justify independence; for every merged state, justify projection equality; preserve completed, failed and frontier counts.

### Property proof

Derive assertions/invariants/history specifications from requirements independently of implementation. Define deadlock/quiescence, liveness horizon and fairness. Validate the oracle with known-positive and known-negative cases and boundary/adversarial inputs.

### Replay and minimization proof

Bind trace to build/model/configuration; verify enabled-set and state digests; reject divergence; reproduce the original failure; minimize without changing oracle/failure identity; retain both traces and exact commands.

### Claim-boundary proof

The handoff names covered scenarios, finished bounds, explored/pruned/cutoff counts, memory/environment model, unsupported operations, unavailable toolchains/platforms, external review status, and complementary tests. Claims never exceed that ledger.

## Alternatives and Trade-Offs

| Method | Strength | Principal limitation |
|---|---|---|
| ordinary unit tests | fast deterministic functional cases | usually one incidental schedule |
| stress/random scheduling | realistic timing and broad sampling | rare paths missed; weak replay/coverage |
| systematic scheduler | controlled bounded schedules and replay | instrumentation/model/state explosion |
| stateless DPOR | avoids storing full state; dependency reduction | repeated prefixes; dependence must be sound |
| stateful model checking | cycle detection and state merging | canonical state capture cost/fidelity |
| weak-memory checker | language-model executions beyond SC | tool/language/intrinsic scope |
| sanitizer under schedules | reproducible observed dynamic defect | dynamic/tool coverage and perturbation |
| formal proof | unbounded theorem under assumptions | specification/model-code mapping effort |
| production tracing | real environment behavior | incomplete visibility and weak control |

## Failure Modes and Misconceptions

- **“Many repetitions equal systematic coverage.”** sampling does not enumerate a defined space.
- **“All interleavings passed.”** state the model, scenario, reductions and bounds.
- **“A controlled thread means a controlled program.”** clocks, callbacks, I/O and foreign runtimes also choose outcomes.
- **“Yield points are the only transitions.”** synchronization, atomics and completions matter.
- **“More yield points are always sounder.”** invented preemption inside an atomic operation can create illegal behavior.
- **“Sequential consistency covers relaxed atomics.”** weak-memory behaviors need an appropriate model.
- **“A timeout proves deadlock.”** cutoff, resource exhaustion or slow progress may explain it.
- **“No enabled transition always means a bug.”** declared quiescence or expected blocking may be correct.
- **“One cycle proves starvation.”** fairness and progress definitions are required.
- **“Hashing locals is unnecessary.”** a local control value can change future enabled transitions.
- **“POR is only optimization.”** an unsound dependence relation loses bugs and invalidates coverage.
- **“Replay can remap event IDs.”** silent remapping hides divergence.
- **“A minimized trace replaces the original.”** retain provenance and both artifacts.
- **“Mocks are specifications.”** validate environment-model fidelity.
- **“Linearizable means globally correct.”** it covers an object's history against a sequential spec, not all system requirements.
- **“A low preemption bound proves high confidence.”** it is a useful prioritization, not universal completeness.
- **“Systematic testing replaces stress tests.”** controlled models and real environments expose different defects.
- **“Systematic testing certifies safety.”** bounded executable evidence is one assurance layer.

## Worked Examples

### Example 1

**Lost update.** Six legal SC schedules for two read/write increments yield two distinct outcomes; four expose `x=1`. **Conclusion:** systematic choice reveals a reachable assertion failure and a replay trace.

### Example 2

**Preemption deepening.** A suite completes bounds 0 and 1 but exhausts budget at 2. **Conclusion:** claim completeness only through bound 1 and retain bound-2 frontier evidence.

### Example 3

**Hidden timer.** A native timer fires outside the controlled runtime, so replay diverges at event 18. Replace it with logical time or mark unsupported. **Conclusion:** all nondeterminism belongs in the model ledger.

### Example 4

**Unsound reduction.** Two transitions write different fields, but the invariant reads both as a pair. Treating them independent can prune an invalid intermediate state. **Conclusion:** property effects participate in dependence.

### Example 5

**State projection.** A hash omits an object's generation after reclamation and merges pre- and post-reuse states. Add generation identity. **Conclusion:** canonicalization must preserve future behavior and monitors.

### Example 6

**Linearizability.** Overlapping queue operations retain invocation, response, arguments and results; a checker finds no legal sequential order. **Conclusion:** history oracles catch semantic defects beyond final-state assertions.

### Example 7

**Bounded liveness.** A request must finish within 200 controlled steps under weak fairness and an eventually responding service model. A 201-step replay refutes that bounded requirement only. **Conclusion:** horizon and assumptions scope progress evidence.

### Example 8

**Weak memory.** An SC scheduler passes a relaxed-atomic publication test; a C11-aware checker finds the undesired observation. **Conclusion:** choose semantics that include production behaviors.

### Example 9

**Fault exploration.** The model injects one cancellation before, during, or after durable commit and checks idempotency/recovery. **Conclusion:** fault position is a controlled scheduling dimension.

### Example 10

**Railway interlocking controller.** The model must preserve route, point, signal, train-detection, command, acknowledgment, timing, degraded-mode and configuration generations; enumerate legal concurrency and supported equipment faults; forbid conflicting authorities; prove fail-safe state and bounded response under declared fairness; isolate all actuation; bind replay to target/runtime; and retain hazard-linked evidence. Named railway signaling/domain, real-time/concurrency/memory-model, compiler/runtime/hardware, functional safety/cybersecurity, operations/maintenance, quality/regulatory/assurance, human-factors/accessibility, ethics and independent validation reviewers must approve it; none is claimed here. **Conclusion:** bounded systematic testing cannot authorize railway operation.

## Cross-Program Connections

- **Programming languages:** memory, atomicity and runtime semantics define legal transitions.
- **Algorithms/formal methods:** graph search, state equivalence, POR, temporal properties and refinement justify coverage.
- **Software engineering:** test seams, stable identities, dependency injection and small scenarios make control durable.
- **Distributed systems:** messages, clocks, partitions, retries and faults become explicit choices.
- **Databases:** histories, serial specifications, commit points and idempotency create oracles.
- **Security:** adversarial schedules expose TOCTOU, authorization and lifecycle races.
- **Cloud/platform engineering:** CI sharding, artifact retention and environment fidelity operationalize searches.
- **Observability:** traces diagnose failures but must remain separate from scheduler causality.
- **Quality/release:** bounded claims and unsupported surfaces belong in release evidence.
- **Safety:** hazard analysis determines which scenarios, faults, bounds and reviewers are required.

## References

1. Madanlal Musuvathi et al., “Finding and Reproducing Heisenbugs in Concurrent Programs,” USENIX OSDI, 2008. <https://www.usenix.org/conference/osdi-08/finding-and-reproducing-heisenbugs-concurrent-programs>
2. Madan Musuvathi and Shaz Qadeer, “Iterative Context Bounding for Systematic Testing of Multithreaded Programs,” ACM PLDI, 2007. <https://www.microsoft.com/en-us/research/publication/iterative-context-bounding-for-systematic-testing-of-multithreaded-programs/>
3. Cormac Flanagan and Patrice Godefroid, “Dynamic Partial-Order Reduction for Model Checking Software,” ACM POPL, 2005. <https://users.soe.ucsc.edu/~cormac/papers/popl05.pdf>
4. Maurice P. Herlihy and Jeannette M. Wing, “Linearizability: A Correctness Condition for Concurrent Objects,” ACM TOPLAS, 1990. <https://www.cs.cmu.edu/~wing/publications/HerlihyWing90.pdf>
5. Brian Norris and Brian Demsky, *CDSChecker: A Model Checker for C11 and C++11 Atomics*, project and OOPSLA paper documentation; retrieved 2026-08-29. <https://github.com/computersforpeace/model-checker>
6. Microsoft, *Coyote: Controlled and Reproducible Testing*, current documentation; retrieved 2026-08-29. <https://microsoft.github.io/coyote/get-started/using-coyote/>
7. Tokio contributors, *Loom: Model Concurrent Programs*, version 0.7.2 documentation; retrieved 2026-08-29. <https://docs.rs/loom/0.7.2/loom/>
8. Michalis Kokologiannakis et al., *GenMC: Generic Model Checker for Concurrent Programs*, current project documentation; retrieved 2026-08-29. <https://github.com/MPI-SWS/genmc>
9. Sebastian Burckhardt et al., “A Randomized Scheduler with Probabilistic Guarantees of Finding Bugs,” ACM ASPLOS, 2010. <https://www.microsoft.com/en-us/research/publication/a-randomized-scheduler-with-probabilistic-guarantees-of-finding-bugs/>
10. Leslie Lamport, “Time, Clocks, and the Ordering of Events in a Distributed System,” *Communications of the ACM*, 1978. <https://lamport.azurewebsites.net/pubs/time-clocks.pdf>

## Exercises

### Exercise 1

Model two actors where A has three transitions and B has two. Compute raw order-preserving interleavings. Then define a state, enabled-transition rule, safety invariant, and exact replay event fields.

### Exercise 2

Design a bound and search ledger for a queue test with three producers, two consumers, capacity two, cancellations, and one injected allocation failure. Explain iterative deepening and cutoff classification.

### Exercise 3

Give a conservative dependence relation for lock, channel, timer, cancellation, and state-monitor transitions. Show one safe POR pruning and one tempting unsound pruning.

### Exercise 4

Design a linearizability and bounded-liveness test for a concurrent key-value map. Include history schema, sequential specification, pending operations, fairness, horizon, weak-memory scope, replay and CI tiers.

### Exercise 5

Transfer systematic concurrency testing to an infusion-pump control service. Specify control/model, dose and alarm invariants, fault/time assumptions, evidence, security/isolation, limitations, and named human reviewer roles without claiming review or deployment authorization.

## Answers to the Exercises

### Answer 1

There are `5!/(3!*2!) = 10` interleavings. A state can be `(pcA, pcB, shared, locals, monitor)`; A is enabled when its next operation's precondition holds, likewise B. Example safety invariant: ownership count remains one and shared balance never becomes negative. Each trace event records build/model/test digests, ordinal, stable actor/operation ID, enabled-set digest, chosen transition, nondeterministic value/fault, and before/after state plus monitor digests. Replay rejects a choice absent from the enabled set or any digest mismatch. This covers only the declared atomic transitions and initial/input model.

### Answer 2

Bound actors exactly at five, queue capacity two, item domain small but identity-preserving, at most one cancellation and one allocation failure, maximum pending operations five, logical-time advances explicitly, and use iterative preemption bounds 0, 1, 2, then higher under budget with a step ceiling sufficient for clean drain/shutdown. The ledger records model/build/input digests; bound vector; search/reduction versions; terminal pass/fail, unique states, transitions, backtracks/pruned alternatives; deadlocks; bounded-liveness failures; replay status; and step/preemption/resource frontiers. Complete each lower preemption bound before raising it. A state cut by a step/resource limit is incomplete, not passed; no-enabled nonterminal state is deadlock; a horizon breach is a bounded-liveness result only under the declared producer/consumer/fairness assumptions.

### Answer 3

Lock operations on the same lock are dependent; channel sends/receives are dependent when they share channel state or pairing/order; timer firing is dependent with cancellation, rescheduling, timeout-sensitive state and relevant monitor events; cancellation is dependent with target progress/completion/cleanup; every transition that changes an observed invariant is dependent where reordering changes monitor states. Two reads of disjoint immutable objects can be safely represented by one order. Pruning writes to separate fields is unsound if a monitor checks their joint consistency or either write enables a waiter. The relation must be conservative and versioned; missing instrumentation invalidates the reduction claim.

### Answer 4

Record unique operation/object/generation IDs, actor, invocation index, key/value, response index/result, cancellation and completion state. The sequential map specifies put/get/remove return values; linearizability search respects invocation-before-response and nonoverlap real-time precedence, while declaring treatment of pending/cancelled calls. Add invariants for unique completion and key/value conservation. Define bounded liveness: under weak fairness, available capacity, and a responsive storage model, every accepted call completes/cancels within `h` controlled transitions. Run an SC scheduler for locks/tasks and a documented language-aware weak-memory checker for atomics; list foreign storage/runtime gaps. Per-change CI runs small keys/actors at finished shallow bounds; periodic jobs deepen bounds, add faults/platforms, retain ledger and traces, and reject cutoff as pass. Replay is bound to binary/model/config digests and fails on divergence.

### Answer 5

Use an isolated simulator with no physical/network actuation and synthetic prescriptions/patient/device data. Control task creation, locks/channels, command/acknowledgment, logical clocks, sensor samples, occlusion/air/battery faults, cancellation, persistence and restart; identify prescription, concentration, patient, pump, line, dose, command, configuration, calibration and alarm generations. Invariants enforce authorized bounded dose/rate/volume/unit conversions, single active command, monotone delivered-volume accounting, stale/duplicate rejection, alarm priority, fail-safe stop, durable audit and bounded alarm/stop response under explicit fairness/device assumptions. Bind traces to requirements/hazards, target build/runtime/model, inputs, bounds and fault alphabet; replay/minimize with original evidence retained; combine with weak-memory, sanitizer, hardware-in-loop, integration and independent expected-dose tests. Encrypt/restrict/redact artifacts, bound retention, and prevent production credentials/routes. Record unsupported hardware physics, sensor fidelity, network stacks, unmodeled faults and incomplete bounds. Release requires named clinical/pharmacy and human-factors/usability, medical-device/software safety, concurrency/memory-model/toolchain, hardware/control, cybersecurity/privacy, operations, quality/regulatory, ethics/accessibility and independent validation reviewers. No external review, clinical efficacy, regulatory approval, safety certification or deployment authorization is claimed.
