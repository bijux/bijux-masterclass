---
module_id: CONPAR-003
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 3
title: Interleavings and State-Space Explosion
status: complete
last_verified: 2026-08-29
---

# Interleavings and State-Space Explosion

## One-Page Review

### Governing question

How can we reason about every execution order permitted by a concurrent program when the number of schedules and reachable states grows far faster than ordinary testing can enumerate?

### Essential definitions

- An **event** is one modeled execution step whose precondition, state effect, and observation boundary are explicit.
- A **schedule** is a sequence of event selections; it is legal when it selects only enabled events and preserves required order.
- An **interleaving model** represents concurrent execution as an order of atomic events that preserves each activity's local and synchronization constraints.
- A **global state** combines shared data, each activity's program counter and local data, pending communication, synchronization, and relevant environment state.
- A **state-transition system** is a directed graph whose vertices are global states and whose labeled edges are enabled events.
- The **reachable state space** contains states reachable from an initial state under the modeled transition relation.
- **State-space explosion** is combinatorial or exponential growth in schedules or states as activities, steps, values, buffers, timers, inputs, and failures grow.
- Two events are **independent** in a state when either enabled order remains possible, reaches an equivalent state, and preserves the property being checked.
- A **partial-order trace** groups schedules that differ only through adjacent swaps of independent events.
- **Partial-order reduction (POR)** explores representatives of such equivalence classes while preserving a stated property under stated conditions.
- A **preemption**, **context**, **depth**, or **data bound** restricts exploration and therefore restricts the resulting claim.

### Central model, mechanism, or theorem

For activities with fixed chain lengths (n_1,...,n_k) and no cross-dependencies, let (N=sum_i n_i). The legal interleaving count is

(N!/(n_1! ... n_k!)).

This counts schedules, not necessarily distinct states or observations. If adjacent events commute and do not affect enabledness or the property, their two orders can represent one trace class. Reduction is sound only relative to a justified dependency relation and precise property; treating conflicting events as independent can delete the only failing execution.

### Critical invariants

Every schedule preserves per-activity and synchronization order. Event boundaries match the language and memory model; a source statement is not assumed atomic. A state includes every local, shared, communication, and environment component relevant to future behavior or the property. Exploration records bounds, fairness, environment, and reductions. Deduplication uses semantic state. POR swaps only justified independent events. A counterexample is replayable as a concrete trace. Exhaustion proves only the finite modeled scope.

### Common failures

Teams count threads rather than event steps; sample one scheduler repeatedly; use sleeps to force an order; model a read-modify-write as atomic; omit program counters or locals; hash only shared variables; merge states whose pending messages differ; reduce dependent accesses; confuse schedule coverage with state coverage; ignore cycles and fairness; or present a bounded search as universal verification.

### Compact example

Two activities increment shared counter (x), each through `read`, local `compute`, and `write`. Their six events admit (6!/(3!3!)=20) program-order-preserving schedules. Only the two schedules in which one increment finishes before the other reads finish at (x=2). The other eighteen let both reads observe zero before conflicting writes and finish at (x=1). One friendly schedule conceals most legal behavior.

### Connections

[Concurrency, Parallelism, and Asynchrony](001-concurrency-parallelism-and-asynchrony.md) introduced partial orders; [Processes, Threads, Tasks, and Fibers](002-processes-threads-tasks-and-fibers.md) identified scheduling units. The [program roadmap](../ROADMAP.md) next separates safety, liveness, races, deadlock, determinism, invariants, message passing, and systematic testing.

## Governing Question

What finite evidence can establish that a concurrent design behaves correctly across schedule variation, and exactly where does that evidence stop?

The answer has three parts. Define events, state, enabledness, and properties precisely. Explore schedules systematically and reduce only equivalences justified by independence. Attach every result to bounds, assumptions, tool semantics, and replayable traces. Without all three, a large test count can still mean little.

## Why This Matters

Sequential tests choose inputs while a main control order is fixed. Concurrent tests choose inputs and inherit scheduling choices: which thread, task, callback, interrupt, message, or completion advances next. These choices expose stale reads, missed signals, duplicated effects, invalid intermediate states, deadlocks, starvation, and cancellation races.

Stress testing samples this space indirectly through a production scheduler. It is valuable for integration and resource behavior, but it is not controlled coverage. A failure can disappear under logging. A million runs can repeat the same few orders because runtime, processor, workload, and timing remain stable. A rare schedule may require only one preemption at a boundary the deployed scheduler seldom chooses.

Systematic exploration controls or models scheduling. It advances one enabled event at a time, records alternatives, and revisits decisions. Microsoft Research's CHESS work used deterministic, progressively broader schedule exploration for multithreaded tests. SPIN and other model checkers explore explicit transition systems. Dynamic partial-order reduction observes dependencies during executions and introduces backtracking where alternative conflicting orders matter.

Scale is the obstacle. Ten activities with ten steps each have (100!/(10!)^10) unconstrained interleavings. Each variable, queue entry, timer, input, retry, allocation result, and failure can multiply states. The engineering question is not whether every concrete event can be tried, but which abstractions, bounds, equivalences, and proofs preserve the required property.

State-space thinking helps even without a checker. It forces a team to name scheduling boundaries, distinguish states, justify commutation, model failures, and define violating observations. Those questions improve APIs, tests, traces, and reviews.

## Prerequisites and Retrieval

Retrieve finite sequences, factorials, combinations, directed graphs, partial orders, mutable state, program counters, transition systems, and assertions. Module 001 established schedules as linear extensions; Module 002 separated tasks from execution contexts.

The operational examples assume sequential consistency. Modules 021–030 later address compiler, processor, and language memory models. Under weak memory, source-level read/write interleavings alone may not explain every permitted behavior.

## Learning Objectives

By the end of this module, you should be able to:

1. define atomic events, enabledness, global state, schedule, trace, and reachable space;
2. enumerate legal interleavings and derive multinomial counts;
3. distinguish schedule, path, state, trace-class, and outcome counts;
4. model a non-atomic operation through local and shared transitions;
5. explain growth from concurrency, data, environment, and liveness dimensions;
6. implement bounded graph exploration with semantic state deduplication;
7. distinguish dependent from independent transitions;
8. explain POR, DPOR, symmetry, abstraction, and context bounding with their obligations;
9. design reproducible counterexample traces and regression schedules; and
10. bound claims from systematic exploration, stress, and model checking.

## Core Exposition

An interleaving semantics begins by choosing **event granularity**. An event is not automatically a source line, expression, bytecode, machine instruction, or transaction. It is the modeled indivisible step. For a shared increment, reading (x), computing a local value, and writing (x) may be separate. For a mutex-protected increment, acquisition, protected transition, and release may be appropriate. The language memory and synchronization model determines whether the abstraction is valid.

Each activity has local state: program counter, locals, status, and owned resources. Global state additionally contains shared variables, lock owners and waiters, channel buffers, pending callbacks, timers, failures, and external inputs relevant to the property. An event has an enabling predicate and a transition effect. If several events are enabled, the scheduler selects one.

A **schedule** records chosen activities or event identities. An **execution trace** can also record states, values, messages, and observations. The same activity schedule may produce several traces because inputs or failures differ. Different schedules may converge to the same state.

Program order restricts merging. If A has (A_1 before A_2) and B has (B_1 before B_2), legal activity words are AABB, ABAB, ABBA, BAAB, BABA, and BBAA. Choosing A's two positions among four derives six. For more chains, selecting positions for each yields the multinomial formula.

The formula assumes each step is enabled except by its predecessor and events are distinguishable. Locks, joins, bounded channels, condition predicates, and data-dependent branches remove schedules. Inputs and failures add branches. Combinatorics is therefore an exact result for a stated chain model, not arbitrary programs.

Path, state, and outcome counts differ. Diamond transitions create two schedules that merge to one state. One state can have many predecessor paths. Several final states can share a public outcome. A visited-state search explores a semantic state once, while history-sensitive checking needs monitor state. If the property says acknowledgment never precedes durable commit, a key that forgets earlier acknowledgment can merge good and bad histories unsoundly.

Two unsynchronized increments show **atomicity refinement**. At a coarse level, `increment` might be one event and both serial orders end at two. Refinement into read, compute, and write exposes lost updates. Each activity's captured local value belongs in state because it controls a later write. Omitting locals makes distinct futures appear equal.

Exploration is graph search. From initial state, compute enabled transitions, apply each, record predecessor plus event, and add unseen successors to a stack or queue. Depth-first search stores a smaller frontier and supports cycle algorithms. Breadth-first search finds a shortest transition-count counterexample but can retain a wide frontier. Neither prevents combinatorial growth.

A state key captures semantic future behavior and property truth. Incidental timestamps, addresses, or log text can prevent useful merging. Omitting queue order, cancellation, local values, or monitor status can merge states incorrectly. Canonicalization may rename symmetric workers or sort genuinely unordered values only when this preserves enabledness and observation.

Finite safety asks whether any reachable state violates an invariant. A counterexample is a finite path to a bad state. Liveness asks whether something desirable eventually happens and involves cycles or infinite executions. A request may remain enabled forever without selection. Liveness needs fairness assumptions and cycle analysis; no bad state below a depth bound does not establish progress.

**Independence** enables POR. Suppose transitions (a) and (b) are both enabled at (s). A useful condition says neither disables the other and both orders reach an equivalent successor: (b(a(s))=a(b(s))). Access to disjoint immutable values may commute. Writes to different state may commute if the property does not observe their order. Writes to one variable, lock operations, send/receive pairs, and events affecting enabledness are normally dependent.

Independence is state- and property-sensitive. Two log appends may commute for a final-set property but not ordered audit evidence. Two distinct counters can interact through a later guard on their sum. Time, random values, exceptions, cancellation, allocation, and external calls need models before being declared independent.

Schedules related by adjacent independent swaps form partial-order trace classes. **Static POR** approximates dependencies from structure. **Dynamic POR** observes executions, detects dependent concurrent events, and places backtracking points to try relevant alternative orders. Sound methods also handle cycles, sleep sets, fairness, and property classes. Skipping events that appear unrelated is not a reduction proof.

Reduction preserves a question, not all questions. A method preserving safety and deadlock reachability may require different conditions for liveness. If a property observes event order, previously invisible actions become relevant. Reports must name dependency relation, algorithm, preserved property, and provisos.

**Symmetry reduction** treats interchangeable actors as equivalent. Permuting four identical workers can yield the same relevant state. Assigned partitions, credentials, priorities, and history break symmetry. Canonical renaming is valid only while those distinctions are absent from enabledness and property.

**Data abstraction** maps large domains to finite categories, such as zero/one/many or empty/nonempty. For safety, an abstract model intended to prove absence must not omit relevant concrete transitions. Over-approximation can create spurious counterexamples, which require validation and possible refinement.

**Bounds** make testing progressive. Limit preemptions, context switches, depth, actors, queue capacity, loop iterations, timers, retry count, data, or injected faults. A context switch away from a blocked activity differs from preempting one that could continue. Absence under bound (b) means only no modeled violation within (b).

Randomized schedule perturbation and stress complement systematic search. Load tests expose timing, capacity, and integration omitted by small models. Race detectors observe instrumented memory interactions in executed runs. Combine these with deterministic models, schedule control, static analysis, code review, and production observability rather than treating one technique as exhaustive.

The executable model enumerates every program-order-preserving schedule for two three-event increments and interprets each.

<!-- bijux-verify: {"id":"lost-update-interleaving-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"schedules=20\nfinal_1=18\nfinal_2=2\nsafe_fraction=2/20\n","stderr":""}} -->
```python
steps = {
    "A": ["read", "compute", "write"],
    "B": ["read", "compute", "write"],
}
schedules = []

def enumerate_schedules(prefix, positions):
    if all(positions[name] == len(steps[name]) for name in steps):
        schedules.append(prefix)
        return
    for name in steps:
        index = positions[name]
        if index < len(steps[name]):
            next_positions = dict(positions)
            next_positions[name] = index + 1
            event = (name, steps[name][index])
            enumerate_schedules(prefix + [event], next_positions)

enumerate_schedules([], {"A": 0, "B": 0})
outcomes = {1: 0, 2: 0}

for schedule in schedules:
    shared = 0
    local = {}
    for name, action in schedule:
        if action == "read":
            local[name] = shared
        elif action == "compute":
            local[name] = local[name] + 1
        else:
            shared = local[name]
    outcomes[shared] = outcomes[shared] + 1

print(f"schedules={len(schedules)}")
print(f"final_1={outcomes[1]}")
print(f"final_2={outcomes[2]}")
print(f"safe_fraction={outcomes[2]}/{len(schedules)}")
```

Execution proves enumeration and counts only for this six-event sequentially consistent model. It does not prove real language atomicity, weak-memory behavior, synchronization correctness, larger executions, or production counter safety.

Counterexamples must be operational. Record initial state, inputs, model and tool versions, bounds, seeds, event choices, values, injected faults, and failure. Use stable logical event identities rather than wall-clock timing. A replay scheduler stops if an expected event is unavailable; silently choosing another destroys reproducibility.

Minimization removes irrelevant inputs and choices while retaining failure. Preserve the original and minimized traces and their mapping to runtime events. The shortest schedule is not always the clearest cause.

Coverage has several dimensions: schedules, unique states, transitions, trace classes, maximum depth, bounds, reduction ratio, terminal states, deadlocks, failures, and replay success. None is a universal percentage of all concurrency; every denominator belongs to a model.

Compositional reasoning controls scope through contracts. An environment supplies an assumption and a component supplies a guarantee. Rely-guarantee reasoning bounds permitted interference. Linearizability maps object histories to legal sequential operations. These avoid whole-system enumeration only when assumptions and refinement mappings are valid.

Evidence should be layered. Small models can exhaust event orders. Systematic runtime tests exercise implementation code within bounds. Static analyses remove behavior classes. Stress, sanitizers, and fault injection cover environment details. Proof review addresses unbounded arguments. Production traces test modeling assumptions. Each supports a bounded claim.

## Definitions and Notation

Let transition system (M=(S,S_0,T,->)) contain global states (S), initial states (S_0), labels (T), and relation (s -t-> s'). Enabled transitions are (En(s)={t | exists s'. s -t-> s'}). A finite execution is (s_0,t_1,s_1,...,t_n,s_n) following that relation. A schedule projects selected labels or activities; a trace retains state and observation.

The reachable set is the least set containing (S_0) and closed under successors. Safety invariant (I) holds in the finite model exactly when every reachable state satisfies it. One reachable state satisfying (not I) is a counterexample.

For fixed event chains of lengths (n_i), let (N=sum_i n_i). Their unconstrained interleaving count is (N!/product_i(n_i!)). Let dependency relation (D subseteq T times T) be symmetric and reflexive. Labels outside (D) are candidates for independence, subject to enabledness, commutation, and property visibility. Adjacent independent swaps generate schedule equivalence.

A **context switch** changes activity. A **preemption** switches away from an activity that could continue. A **terminal state** satisfies completion obligations. A **deadlock state** has unfinished obligations but no enabled progress under the environment assumptions. A **cycle** is a nonempty path returning to equivalent state and matters to liveness.

## Mechanisms, Invariants, or Proof Structure

Use this workflow:

1. **State the property.** Define the bad state, temporal obligation, or acceptable outcome before reductions.
2. **Choose boundaries.** Map language, synchronization, and environment actions to transitions.
3. **Construct state.** Include program counters, locals, shared values, synchronization, messages, time/fault abstraction, and monitors.
4. **Validate tiny traces.** Manually enumerate small cases and compare with implementation traces.
5. **Search without reduction.** A tractable full search becomes an oracle for reduced search.
6. **Define dependency.** Justify enabledness preservation, commutation, and property invisibility.
7. **Apply named reductions and bounds.** Record algorithms, provisos, exclusions, and coverage.
8. **Replay failures.** Preserve schedule, state evidence, versions, and assertion.
9. **Cross-check evidence.** Compare models, systematic runs, stress, sanitizers, and production.
10. **Review generalization.** Identify claims needing induction, refinement, fairness, or domain authority.

For the multinomial result, choose positions for the first activity, then the second from remaining positions, and continue. Local order fixes events in those positions. Multiplying combinations and cancelling factorials yields (N!/product_i(n_i!)).

For POR's diamond, suppose (a) and (b) are enabled at (s), neither disables the other, and both orders reach equivalent state (u). Any suffix from (u) follows either `ab` or `ba`. For a state property insensitive to the swapped labels, both prefixes are redundant. A complete algorithm also needs cycle and temporal-property provisos.

Maintain these invariants:

- every transition is enabled in its predecessor;
- local and synchronization order remain intact;
- state identity retains every future- and property-relevant component;
- bad-history monitors survive deduplication;
- reduced and full searches agree on calibration models;
- independent transitions do not disable, conflict, or alter relevant observation;
- bounds and fairness are evidence fields;
- counterexamples replay or are marked stale;
- finite exhaustion claims only its model; and
- high-consequence use requires named authorized human review.

The safety argument is graph induction. Initial states are reachable. Whenever an explored state is reachable, every generated enabled successor is reachable. If search exhausts the finite graph and checks (I) in every state, (I) holds for that graph. The argument fails if transitions are omitted, the key merges distinct futures, search is incomplete, or model and implementation differ.

## Alternatives and Trade-Offs

**Explicit-state checking** gives exact finite graph exploration and strong traces, but memory grows with states and models can diverge from code. **Stateless checking** repeatedly executes controlled program code, trading state memory for re-execution and environment-control demands.

**Depth-first search** uses a small frontier and supports cycles. **Breadth-first search** finds shortest-depth failures but can exhaust memory. Heuristics can find defects sooner without strengthening completeness.

**Static POR** reuses dependency information but may be conservative. **DPOR** learns conflicts from executions and can reduce more precisely, at the price of instrumentation and intricate backtracking.

**Bounding** creates progressive real-code tests but gives bounded results. **Abstraction** can represent infinite domains finitely, but proof-oriented abstraction needs a sound simulation and may produce spurious failures.

**Deterministic control** gives replay and accounting. **Random stress** reaches realistic scale but provides weak schedule guarantees. **Whole-system search** sees interactions but explodes; **composition** scales through assumptions that integration must monitor.

## Failure Modes and Misconceptions

- **“Two threads mean two schedules.”** Count depends on modeled steps and constraints.
- **“A source statement is atomic.”** Language and synchronization rules define atomicity; compound operations expose substeps.
- **“Parallel execution cannot be modeled through interleaving.”** Sequential consistency permits suitable atomic interleavings; weak memory needs more.
- **“Exploring schedules equals exploring states.”** Many schedules merge, and one schedule visits many states.
- **“A million stress runs cover a million useful orders.”** Schedulers can repeat near-identical traces.
- **“Sleep makes a race deterministic.”** Timing perturbs probability; event control is stronger.
- **“Different variables imply independence.”** Guards, invariants, environment, or observation can connect them.
- **“POR drops arbitrary schedules.”** Sound POR preserves named properties under dependency and cycle conditions.
- **“No failure under a bound proves correctness.”** It proves absence only in the bounded model.
- **“A model trace proves a product defect.”** Mapping and replay must connect model to code.
- **“Safety checks establish liveness.”** Infinite unfair paths and cycles require separate analysis.
- **“More hardware solves explosion.”** Growth requires reduction, abstraction, composition, and proof.

## Worked Examples

### Example 1

**Question:** How many interleavings combine chain A of length three and chain B of length two?

**Reasoning:** Choose A's three positions among five. Local order fixes all events. The count is (5!/(3!2!)=10).

**Conclusion:** Two short chains already produce ten schedules.

### Example 2

**Question:** Why do two three-step increments have twenty schedules but two final values?

**Reasoning:** The merge count is twenty. Interpretation yields eighteen lost-update schedules ending at one and two serialized schedules ending at two.

**Conclusion:** Schedule and outcome counts differ.

### Example 3

**Question:** May an increment model key state only by shared counter and program counters?

**Reasoning:** No. Each captured read controls a later write. Equal shared/program states with different local snapshots have different futures.

**Conclusion:** State includes relevant local values.

### Example 4

**Question:** Two events write disjoint metrics. May their orders be reduced?

**Reasoning:** Only if neither affects enabledness and the property ignores order. Ordered audit evidence or a later guard over both restores dependence.

**Conclusion:** Independence is state- and property-relative.

### Example 5

**Question:** What may a two-preemption search claim?

**Reasoning:** It may report no violation under declared inputs, depth, environment, memory, and preemption bound. It cannot exclude a three-preemption defect.

**Conclusion:** Bounds belong inside claims.

### Example 6

**Question:** How can deduplication hide acknowledgment-before-commit?

**Reasoning:** A key holding only current database and queue state may merge different histories. Add monitor state such as `ack_seen_without_commit`.

**Conclusion:** History properties need history-relevant state.

### Example 7

**Question:** Why is deadlock not ordinary termination when neither enables an event?

**Reasoning:** Termination discharged required outcomes. Deadlock retains unfinished obligations whose waits cannot be satisfied.

**Conclusion:** Obligations define terminal meaning.

### Example 8

**Question:** A reduced search passes but its full calibration search fails. What follows?

**Reasoning:** Dependency, property visibility, cycle handling, or implementation is unsound. The reduced result is invalid pending correction.

**Conclusion:** Full small searches are reduction oracles.

### Example 9

**Question:** Why can replay become stale after code changes?

**Reasoning:** Event identities, enabledness, or paths change. Strict replay reports the first unavailable expected event rather than silently choosing another.

**Conclusion:** Replay is a checked protocol, not sleeps.

### Example 10

**Question:** A medical infusion model passes all schedules for two pumps, one command, and depth forty. Is production approved?

**Reasoning:** It covers that model only. Device refinement, timing, interrupts, memory, failures, alarms, capacity, security, liveness, and larger configurations remain. Named clinical, safety, systems, software, verification, security, and regulatory reviewers must judge residual risk.

**Conclusion:** Bounded exhaustion is not unbounded proof or domain approval.

## Cross-Program Connections

- [Concurrency, Parallelism, and Asynchrony](001-concurrency-parallelism-and-asynchrony.md) supplies partial orders.
- [Processes, Threads, Tasks, and Fibers](002-processes-threads-tasks-and-fibers.md) distinguishes work from execution contexts.
- The [CONPAR roadmap](../ROADMAP.md) develops safety, liveness, races, deadlock, determinism, invariants, memory models, and testing.
- [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) contributes transition semantics.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) owns scheduler mechanisms.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) extends state reasoning to messages and failures.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) uses adversarial schedules for protocol claims.

## References

1. Leslie Lamport, “Time, Clocks, and the Ordering of Events in a Distributed System,” *Communications of the ACM* 21(7), 1978, [Microsoft Research record](https://www.microsoft.com/en-us/research/publication/time-clocks-ordering-events-distributed-system/).
2. Gerard J. Holzmann, *The SPIN Model Checker: Primer and Reference Manual*, Addison-Wesley, 2004.
3. Edmund M. Clarke, Orna Grumberg, and Doron A. Peled, *Model Checking*, MIT Press, 1999.
4. Patrice Godefroid, *Partial-Order Methods for the Verification of Concurrent Systems*, Springer, 1996, [bibliographic record](https://dblp.org/rec/books/sp/Godefroid96.html).
5. Cormac Flanagan and Patrice Godefroid, “Dynamic Partial-Order Reduction for Model Checking Software,” *POPL 2005*, [DOI](https://doi.org/10.1145/1047659.1040315).
6. Madan Musuvathi, Shaz Qadeer, Thomas Ball, et al., “Finding and Reproducing Heisenbugs in Concurrent Programs,” *OSDI 2008*, [USENIX paper](https://www.usenix.org/legacy/event/osdi08/tech/full_papers/musuvathi/musuvathi.pdf).
7. Sebastian Burckhardt et al., “Predictable and Progressive Testing of Multithreaded Code,” *IEEE Software* 28(3), 2011, [Microsoft Research record](https://www.microsoft.com/en-us/research/publication/predictable-and-progressive-testing-of-multithreaded-code/).
8. Pierre Wolper and Patrice Godefroid, “Partial-Order Methods for Temporal Verification,” *CONCUR 1993*, [DOI](https://doi.org/10.1007/3-540-57208-2_28).
9. Nancy A. Lynch, *Distributed Algorithms*, Morgan Kaufmann, 1996.
10. Leslie Lamport, *Specifying Systems*, Addison-Wesley, 2002, [author-hosted book](https://lamport.azurewebsites.net/tla/book.html).

## Exercises

### Exercise 1

Compute the unconstrained interleaving count for three activities with two events each. Explain every assumption behind the result.

### Exercise 2

Model two unsynchronized transfers, each with read-source, read-destination, compute, write-source, and write-destination events. Identify required global state and a schedule shape that can lose an update.

### Exercise 3

Design a finite explicit-state explorer for a two-worker queue of capacity two. Specify the state key, enabled transitions, terminal and deadlock predicates, predecessor evidence, and resource bounds.

### Exercise 4

Compare stress testing, stateless systematic testing, explicit-state model checking, and DPOR for a thread-safe cache. Give one strong use and one limitation of each.

### Exercise 5

A railway signaling component passes a reduced search for three trains, two track segments, depth 100, and one sensor fault. Define the evidence and review required before widening the claim or deploying.

## Answers to the Exercises

### Answer 1

The count is (6!/(2!2!2!)=720/8=90). This assumes six distinguishable events, fixed order within each activity, no cross-activity dependencies, no blocking or data-dependent branches, and feasibility of every merge. It counts schedules, not unique states, paths after merging, or outcomes. Synchronization can remove schedules; inputs and failures can add branches.

### Answer 2

State includes both program counters; shared balances and versions; each transfer's captured source/destination values, amount, computed values, and completion status; synchronization or transaction state; and monitors for conservation and overdraft. A lost-update schedule lets A read, then B read the same balances, A compute and write, and B overwrite with stale computations. Exact feasibility depends on atomicity and transaction validation, which the model must represent rather than assuming the whole transfer is one event.

### Answer 3

The conceptual key contains ordered queue contents, producer and consumer program counters and local values, worker statuses, completion counts, and monitor flags. Enable enqueue only below capacity and dequeue only when nonempty; include local processing, completion, and modeled cancellation. Terminal means all required items were produced and consumed exactly once, workers completed, and the queue is empty. Deadlock means obligations remain with no enabled progress. Store semantic keys plus predecessor state/event links for replay. Bound item domain/count, workers, capacity, depth, cancellations, and transitions, and include every bound in the report.

### Answer 4

Stress runs realistic code, workload, scheduler, and resources, but samples schedules unpredictably and replays poorly. Stateless systematic testing controls real-code schedules and produces replay traces, but requires finite bounds and controlled nondeterminism. Explicit-state checking can exhaust a finite abstraction and analyze cycles, but faces model-fidelity and memory limits. DPOR collapses independent permutations and can make systematic testing tractable, but soundness depends on conflict detection, property visibility, and algorithmic provisos. A cache benefits from all four when their claims remain separate.

### Answer 5

Retain the exact model, implementation mapping, properties, state key, dependency relation, reduction algorithm and provisos, tool/version, fairness and memory assumptions, environment model, bounds, state/transition/class counts, unreduced calibration, sensor-fault semantics, and replay procedure. Add asymmetric layouts, multiple and correlated faults, timing and communication failures, recovery cycles, liveness, hardware integration, and independent model review. Automation can establish finite reachability results and regression differences. It cannot decide model fidelity, acceptable hazard, operating procedure, compliance, or deployment authority. Named railway-domain, safety, formal-methods, systems, software, hardware, cybersecurity, operations, independent-assurance, and regulatory reviewers must decide. No external review is claimed here.
