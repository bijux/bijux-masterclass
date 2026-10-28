---
module_id: CONPAR-006
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 6
title: Deadlock, Livelock, and Starvation
status: complete
last_verified: 2026-08-29
---

# Deadlock, Livelock, and Starvation

## One-Page Review

### Governing question

How can an engineer distinguish deadlock, livelock, starvation, and ordinary delay, then prove that a prevention, detection, or recovery mechanism addresses the right progress failure under explicit scheduling assumptions?

### Essential definitions

- **Deadlock** is a reachable state in which a set of unfinished participants can make no required progress because each waits for an event that only another participant in the set can cause.
- A **wait-for graph** represents current dependencies as directed edges. An actor-to-resource edge means the actor waits; a resource-to-actor edge records ownership or the participant whose action can release capacity.
- **Mutual exclusion**, **hold and wait**, **no preemption**, and **circular wait** are the four Coffman conditions necessary for classical reusable-resource deadlock.
- **Livelock** occurs when relevant participants continue taking transitions but fail indefinitely to advance the required outcome.
- **Starvation** occurs when one continuously or repeatedly eligible participant is denied service indefinitely while other work may progress.
- **Priority inversion** is delay of a higher-priority participant by a lower-priority owner, often extended by medium-priority work. It is not itself deadlock.
- **Fairness** is an assumption or mechanism governing eventual service. Weak fairness concerns actions continuously enabled; strong fairness concerns actions enabled infinitely often.
- A **ranking function** maps states to a well-founded set and must decrease on designated progress transitions; it can support a termination or no-livelock argument.
- **Bounded waiting** places a finite upper bound on how many competing admissions may bypass an eligible participant.
- **Cancellation completeness** requires a cancellation state, a wake path for every relevant blocking site, and a checkpoint that consumes cancellation.

### Central model, mechanism, or theorem

For state (s), let (Enabled(s)) be the transitions permitted by the operational model and let (Done_P(s)) mean obligation (P) has completed. A deadlocked set (D) is unfinished and closed under its blocking dependencies: every member waits, and every event that could discharge those waits depends on another member that cannot run the required event.

In a single-instance reusable-resource model, a reachable directed cycle in the resource-allocation graph characterizes deadlock for the actors on that cycle. With multiple instances, conditions, message capacity, joins, callbacks, or incomplete observations, a cycle may be necessary evidence but not a sufficient production verdict. Reachability and edge meaning must be established.

### Critical invariants

Every wait has a named releaser or termination rule. Ownership and wait edges describe one coherent instant or declare snapshot uncertainty. A global acquisition order is strict and applied to every participating path. Recovery preserves state invariants even when a victim is cancelled or rolled back. Livelock arguments measure semantic progress, not CPU activity. Starvation claims state scheduler and queue fairness assumptions. Timeouts bound observation or initiate recovery; they do not prove deadlock. Cancellation reaches all blocking paths. Detection scope and unsupported resources are explicit.

### Common failures

Teams call any timeout a deadlock; treat a wait-for cycle assembled from different moments as proof; ignore queues, joins, conditions, callback reentrancy, and pool capacity; acquire “mostly” in order; add try-lock loops that livelock; claim random backoff guarantees completion; equate throughput with fairness; assume a fair scheduler makes an unfair lock fair; recover by killing an owner without repairing protected state; set a cancellation flag without waking sleepers; or use a test timeout as the only evidence.

### Compact example

Worker A owns lock A and requests lock B. Worker B owns lock B and requests lock A. The current graph is A → B-lock → B → A-lock → A. If both locks are single-instance, neither owner can be preempted, and no external action releases either lock, the reachable cycle is a deadlock. Requiring all paths to acquire A-lock before B-lock makes such a cycle impossible because a strict order cannot increase around a cycle and return to its starting point.

### Connections

[Safety, Liveness, and Progress](004-safety-liveness-and-progress.md) supplies temporal vocabulary; [Race Conditions and Atomicity Violations](005-race-conditions-and-atomicity-violations.md) explains the atomic updates needed by coordination mechanisms. The [program roadmap](../ROADMAP.md) next develops determinism, critical sections, ownership transfer, locks, atomics, happens-before, and structured concurrency.

## Governing Question

When a concurrent system stops delivering useful outcomes, which exact progress property failed, which dependency or scheduling assumption caused the failure, and what evidence justifies the proposed remedy?

A rigorous answer separates state from motion. Deadlock is blocked motion caused by a closed dependency. Livelock contains motion without semantic advancement. Starvation is participant-specific denial despite system progress. Ordinary overload, slow external service, and a long but finite critical section may resemble all three in a dashboard. Diagnosis therefore needs a model, a trace, and declared assumptions rather than a duration threshold.

## Why This Matters

Progress failures are among the hardest production defects to reproduce because the final symptom is usually far from the causal decision. A service queue grows because its worker pool is exhausted; the workers are blocked on callbacks scheduled into the same pool. A user request times out because two transactions wait on conflicting rows. A control loop consumes an entire core because two polite agents repeatedly yield to each other. A low-priority owner is preempted while a high-priority control task waits for its mutex. Each incident looks like “nothing completes,” but prevention and recovery differ.

Misclassification creates unsafe remedies. Increasing a timeout does not break a deadlock. Retrying immediately can amplify livelock. Killing a lock owner can expose inconsistent state. Adding a global lock can prevent one race while introducing circular wait elsewhere. A FIFO queue may prevent starvation but raise tail latency for urgent work. Random backoff can improve expected contention behavior without supplying a deterministic bound.

The scope is broader than mutexes. Dependencies arise through bounded channels, connection pools, thread pools, futures, joins, barriers, condition variables, database locks, distributed leases, memory allocators, device queues, and callback reentrancy. An actor that blocks while retaining scarce capacity creates the same hold-and-wait structure even when no source-level `lock` appears.

Progress is part of a contract. A safety property says prohibited outcomes never occur. A liveness property says a desired outcome eventually occurs under stated environment and fairness assumptions. Operational objectives add finite time or percentile bounds. These claims are related but not interchangeable: a system can be deadlock-free yet starve one request, starvation-free yet miss a deadline, or meet throughput goals while allowing unbounded individual delay.

## Prerequisites and Retrieval

Before this module, retrieve:

- reachable states, transitions, schedules, invariants, safety, liveness, weak fairness, and strong fairness from [Safety, Liveness, and Progress](004-safety-liveness-and-progress.md);
- event traces and the limitation of bounded exploration from [Interleavings and State-Space Explosion](003-interleavings-and-state-space-explosion.md);
- atomic regions and serialization authority from [Race Conditions and Atomicity Violations](005-race-conditions-and-atomicity-violations.md);
- directed graphs, paths, cycles, strongly connected components, and topological order;
- preconditions, postconditions, contradiction, induction, and well-founded order; and
- practical familiarity with locks, queues, futures, cancellation, and scheduler priorities.

Retrieval prompt: draw a graph with actors A and B and resources X and Y. Add edges showing A owns X and waits for Y while B owns Y and waits for X. Explain which facts are observations and which are assumptions. Then remove one edge and state why the original deadlock conclusion no longer follows.

## Learning Objectives

After completing this module, a learner can:

1. classify a trace as deadlock, livelock, starvation, priority inversion, slow execution, or insufficient evidence;
2. build a typed wait-for or resource-allocation graph across locks, queues, joins, conditions, and capacity pools;
3. apply the Coffman conditions within their valid classical resource model;
4. prove why a strict global resource order excludes circular wait;
5. use ranking, fairness, and bounded-waiting arguments to analyze livelock and starvation;
6. compare prevention, avoidance, detection, timeout, cancellation, rollback, and restart;
7. design deterministic tests and production evidence without treating bounded observation as universal proof;
8. evaluate recovery effects on protected state, external actions, and compatibility; and
9. identify high-consequence decisions that require authorized domain review.

## Core Exposition

### Start with obligations and dependencies

Choose the unit whose progress matters: operation, request, actor, transaction, control cycle, or whole service. Record its unfinished obligation and the event that would discharge it. If worker A waits for queue space, space may depend on consumer B dequeuing. If B waits for A's future, the dependency returns to A. The graph must represent those semantic dependencies, not merely thread states.

A resource-allocation graph commonly uses actor-to-resource request edges and resource-to-actor assignment edges. A wait-for graph collapses resources and draws actor-to-actor edges: A → B means A needs an action by B. Keep resource nodes when capacity, ownership, or multiple instances matter. Type the edges so “owns,” “waits for,” “needs capacity from,” and “joins” are not confused.

A graph is time-indexed. Combining A's old wait with B's later ownership can manufacture a cycle that never existed. Prefer one consistent runtime snapshot, a coordinated trace reconstruction, or intervals with uncertainty. Also establish reachability: a syntactic lock-order inversion shows risk, while a concrete concurrent state shows an occurrence. Mutually exclusive branches may make a static cycle unreachable.

For single-instance reusable resources, a reachable cycle is decisive when every request on the cycle blocks and only cycle members can release the resources. With multiple instances, a cycle can coexist with an available instance that lets someone proceed. Conditions and messages require still more care: a participant outside the cycle might signal, add capacity, cancel, or fail. State the theorem's model rather than exporting a textbook shortcut to every system.

### Deadlock and the Coffman conditions

Coffman, Elphick, and Shoshani organized classical resource deadlock around four necessary conditions:

1. **Mutual exclusion:** at least one resource cannot be used in the required mode by multiple actors simultaneously.
2. **Hold and wait:** an actor retains one resource while requesting another.
3. **No preemption:** the system cannot safely take the held resource and reassign it before voluntary release.
4. **Circular wait:** a directed cycle exists in which every actor waits for the next actor's held resource.

Breaking any condition prevents deadlock in that model. Make resources shareable or immutable to remove mutual exclusion. Acquire all resources as one reservation to remove hold and wait. Support safe rollback or revocation to permit preemption. Impose a strict resource order to remove circular wait. Each remedy has cost, and the four conditions do not fully model arbitrary message protocols or failures.

The ordering proof is compact. Assign each resource (r) a rank (rho(r)) in a strict total order. Require an actor holding resources to request only a resource with greater rank. Assume a wait cycle exists. Following its requests gives (rho(r_1) < rho(r_2) < ... < rho(r_k) < rho(r_1)), contradicting irreflexivity and transitivity. The proof fails if any path uses a different order, ranks can change while held, reentrant callbacks acquire an unranked resource, or a hidden subsystem reverses the order.

All-at-once acquisition prevents hold and wait but can reserve idle resources, reduce concurrency, and require an atomic allocator. Try-lock plus release avoids permanent holding, yet synchronized contenders may repeatedly acquire, fail, release, and retry together: deadlock becomes livelock. Random jitter reduces correlation probabilistically; a queue or arbitrator can make turns explicit.

Avoidance admits a request only if the resulting allocation remains in a state from which all actors can finish under declared maximum demands. The Banker's algorithm is the canonical finite-resource model. Real services often cannot declare maximum future demand, so avoidance may be impractical even though its safe-state reasoning remains useful.

### Detection and recovery

Detection reconstructs dependencies and finds cycles or closed blocked components. Runtime support can be narrow: Java SE 26 `ThreadMXBean.findDeadlockedThreads` finds cycles among platform threads waiting for object monitors or ownable synchronizers, not arbitrary database locks, network protocols, virtual-thread pinning patterns, or application queues. A detector's negative result is therefore scoped evidence.

For large graphs, depth-first search detects a cycle in linear time in vertices plus edges; strongly connected components identify mutually reachable regions. A cycle still needs semantic validation: are all edges blocking now, is every needed release controlled inside the component, and can cancellation or failure resolution intervene? Preserve actor IDs, resource IDs, ownership, requested modes, timestamps, stacks, queue positions, and snapshot provenance.

Recovery selects a victim, preempts or rolls it back, repairs invariants, releases resources, and controls retry. Victim choice may consider work lost, priority, deadlines, retries, transaction age, external effects, and recurrence. A robust mutex can report that an owner died, but the next owner must make the protected state consistent before normal use. Restarting a process releases process-owned resources but can strand leases or duplicate non-idempotent effects.

Timeouts are observation and policy mechanisms. A timeout says completion did not occur before a chosen deadline. It can trigger a graph capture, cancellation, rollback, circuit breaking, or failover. It does not distinguish deadlock from overload, a paused runtime, packet loss, or slow legitimate work, and it does not prove that the underlying cycle was broken.

### Livelock and semantic ranking

In livelock, transitions continue. CPU usage, log volume, retry counts, or lock acquisitions may rise while the required obligation stays unchanged. Classic examples include two agents repeatedly stepping aside in symmetry, two transactions aborting each other in synchronized retry, and workers consuming and immediately requeuing an item none can handle.

Define a semantic rank rather than counting instructions. It may be remaining obligations, unresolved conflicts, distance to a committed state, or a lexicographic tuple. A termination proof identifies a well-founded domain and shows every relevant cycle contains a transition that strictly decreases rank, while no transition increases an earlier tuple component without a later bounded compensation. If an infinite transition cycle leaves rank unchanged, the trace is a livelock counterexample.

Backoff changes scheduling probabilities. Exponential backoff with independent jitter often reduces repeated collision, but unless the model supplies probability-one termination and its assumptions, it is not a deterministic no-livelock proof. Serialized admission, a FIFO waiter queue, a circulating token, monotonic winner election, or deterministic tie-breaking can provide a stronger structural argument.

### Starvation, fairness, and priority inversion

Starvation is local. The service may complete millions of operations while one eligible waiter never wins. Demonstrating throughput therefore cannot prove starvation freedom. Record eligibility intervals, queue position, bypass count, service policy, priority changes, cancellations, and scheduler decisions.

Weak fairness says a transition continuously enabled from some point is eventually taken. Strong fairness says a transition enabled infinitely often is eventually taken. Neither holds automatically. An unfair mutex may repeatedly admit newcomers ahead of an old waiter even on a generally fair CPU scheduler. Conversely, FIFO admission can bound lock bypass while the owner is indefinitely descheduled. Proof obligations compose scheduler, primitive, queue, and application assumptions.

Bounded waiting is operationally sharper: after an actor requests entry, no more than (B) other admissions may occur before it enters, provided it remains eligible and participants release correctly. Ticket locks offer a simple admission order but can convoy behind a stalled owner. Reader-preference locks can starve writers; writer preference can delay readers; phase-fair policies balance classes with added state and handoff cost.

Priority inversion occurs when a high-priority actor waits for a resource held by a lower-priority actor. Medium-priority work can delay the owner, indirectly delaying the high-priority actor. Priority inheritance temporarily raises the owner's effective priority; priority-ceiling protocols constrain locking and can bound blocking under their task model. POSIX.1-2024 specifies optional `PTHREAD_PRIO_INHERIT` and `PTHREAD_PRIO_PROTECT` mutex protocols. These mechanisms require platform support and do not repair arbitrary circular wait.

### Cancellation is a progress protocol

A cancellation flag alone cannot wake an actor asleep on a condition, queue, socket, or semaphore. For every blocking site, design three elements: cancellation state becomes visible; a wake or interrupt makes the site runnable; and a checkpoint observes cancellation and unwinds ownership safely. If a wait can miss the wake between checking and sleeping, combine predicate observation and enrollment atomically under the primitive's protocol.

Structured concurrency narrows lifetime and propagates cancellation, but cleanup can itself deadlock. Do not join a child while holding a resource the child needs to terminate. Make terminal accounting explicit: every accepted operation becomes succeeded, failed, or cancelled exactly once, and every resource is released or transferred according to an invariant.

## Definitions and Notation

Let a transition system be (M = (S, T, →, s_0)). For state (s), (Enabled(s)) is the set of transitions with an outgoing step. Participant (p) has obligation predicate (Done_p(s)).

A **blocked** participant has no locally executable transition that advances its obligation until an external dependency event occurs. A set (D) is **deadlocked** in reachable state (s) when every (p in D) is unfinished and every transition capable of enabling completion for a member depends on an unavailable action by another member of (D). State the closure rule for environment failures and cancellation.

A typed graph (G_s = (V,E)) represents state (s). Edge (p → r) is a blocking request; (r → p) is assignment or release dependence. In a collapsed wait-for graph, (p → q) says progress of (p) currently requires an action by (q).

An infinite execution (pi = s_0 t_0 s_1 t_1 ...) is a **livelock** for obligation (P) when infinitely many relevant transitions occur yet (P) never completes and the execution does not merely remain blocked. Participant (p) **starves** when it remains continuously or recurrently eligible under the chosen fairness definition but never receives the required service while the system can serve others.

A ranking function (R: S → W) maps into a well-founded order (W, prec). A termination argument shows designated progress steps decrease (R) and other steps cannot sustain an infinite nondecreasing cycle. A bounded-waiting property can be written: request by (p) at admission count (n) implies service by count at most (n+B), subject to explicit eligibility and failure assumptions.

## Mechanisms, Invariants, or Proof Structure

Use the following proof-oriented workflow:

1. **Name the obligation.** Define completion, failure, cancellation, and deadline separately.
2. **Capture a coherent state or trace.** Include actors, resources, capacity, ownership, waits, queue positions, priorities, and time.
3. **Type dependency edges.** State which exact action can discharge each wait and who controls it.
4. **Classify the failure.** No transitions suggests blocking or deadlock; infinite non-progress transitions suggest livelock; repeated bypass of one eligible actor suggests starvation.
5. **Apply a theorem only inside its model.** Check resource multiplicity, reachability, edge consistency, preemption, and external actors before using a cycle result.
6. **Select a mechanism.** Prevention, avoidance, fair admission, ranking discipline, cancellation, detection, rollback, or redesign must target the classified failure.
7. **Prove the key invariant.** Use acyclic rank, safe-state sequence, decreasing semantic measure, bounded bypass, or complete cancellation paths.
8. **Test a minimal counterexample.** Control admission points and record the shortest failing trace.
9. **Exercise recovery.** Inject owner failure, cancellation, timeout, and rollback; assert protected and external state.
10. **Bound the claim.** Document scheduler, environment, tool, runtime, and observation limitations.

The principal invariants are:

- every blocking edge has a named discharge event;
- wait and ownership observations are contemporaneous or uncertainty is represented;
- every acquisition follows one immutable rank policy;
- no actor blocks or joins while retaining an undeclared dependency needed by the awaited work;
- retry changes an asymmetry, rank, turn, or probability distribution rather than repeating the identical collision schedule;
- service policy exposes a fairness or bounded-bypass contract;
- priority protocols cover every lock and scheduler assumption in their analysis;
- cancellation can wake and unwind every blocking site;
- recovery restores protected invariants before resource reuse;
- timeouts remain evidence of elapsed time, not proofs of causality; and
- finite tests establish observed counterexamples or bounded absence only.

## Alternatives and Trade-Offs

**Global resource ordering** prevents circular wait and supports a short proof. It can conflict with encapsulation, force early acquisition of high-ranked resources, and become difficult across plugins or external systems. Centralize ranks, validate them, and include callback and cleanup paths.

**Atomic all-or-none reservation** removes hold and wait. It may reduce utilization and requires an authority that sees the full resource set. **Banker-style avoidance** preserves a safe completion sequence but needs credible maximum claims and stable resource counts.

**Timeout and retry** bound caller waiting and can restore availability when operations are cancellable. Poorly chosen timeouts abandon healthy work, synchronize retries, and duplicate effects. Add jitter for collision reduction, retry budgets for overload control, and idempotency for effect safety; do not call the result deadlock prevention.

**Deadlock detection plus victim rollback** permits optimistic concurrency and is common in transactional systems. It spends work, complicates victim fairness, and requires rollback-safe effects. A fixed “youngest loses” rule can repeatedly victimize one operation; age or retry count may need promotion.

**FIFO or ticket admission** gives visible order and bounded bypass under owner progress. It can convoy behind a stalled waiter and may conflict with priority deadlines. **Priority inheritance** bounds a particular inversion under a scheduler model but adds bookkeeping and may propagate through dependency chains.

**Message ownership** removes shared lock acquisition from callers by sending decisions to one owner. It introduces queue capacity, backpressure, owner failure, and response correlation; a bounded inbox plus synchronous callback can recreate circular wait.

**Lock-free algorithms** remove mutex-owner deadlock and may guarantee system-wide progress, but lock-free does not imply per-thread starvation freedom. Memory reclamation and retry contention add proof obligations. **Wait-free algorithms** provide per-operation step bounds under their model but are substantially harder and can have higher constants.

**Process isolation and restart** can contain a stuck component and release operating-system resources. It needs durable state recovery, lease expiry, duplicate suppression, and supervision. Restart is recovery policy, not evidence that root cause was deadlock.

## Failure Modes and Misconceptions

- **“It exceeded the timeout, so it deadlocked.”** The observation is compatible with overload, slow I/O, suspension, or lost work.
- **“Any wait-for cycle proves deadlock.”** Confirm one coherent reachable state, resource multiplicity, blocking semantics, and possible external release.
- **“No cycle means no deadlock.”** The detector may omit queues, conditions, pool capacity, distributed waits, or requested modes.
- **“Acquire locks alphabetically.”** The useful rule is one complete strict rank applied on every path, including callbacks and cleanup.
- **“Try-lock and release cannot hang.”** They can livelock if contenders repeat the same collision pattern.
- **“Random backoff guarantees success.”** It usually changes probability; a guarantee needs a probabilistic theorem and assumptions.
- **“High throughput proves fairness.”** One request can starve while aggregate throughput remains excellent.
- **“The operating-system scheduler is fair.”** Fairness is policy- and workload-dependent and does not automatically compose with lock admission.
- **“Priority inversion is deadlock.”** Inversion is priority-mediated delay; it can be bounded, unbounded, or part of a cycle.
- **“Priority inheritance solves all inversion.”** It applies only to supported primitives and task assumptions and adds transitive bookkeeping.
- **“Cancellation means setting a Boolean.”** A blocked participant also needs a wake path and a safe checkpoint.
- **“Kill the owner and continue.”** Protected state may be inconsistent and external effects may already have escaped.
- **“Deadlock-free means live.”** Livelock, starvation, unbounded queues, or missed deadlines may remain.
- **“A passing stress test proves absence.”** It covers observed schedules and instrumentation scope only.

## Worked Examples

### Example 1

**Question:** A owns X and waits for Y; B owns Y and waits for X. Both resources have one instance. No timeout, preemption, or outside releaser exists. What is the classification?

**Reasoning:** The state is reachable, both actors are unfinished, every request blocks, and the dependency cycle is closed. All four Coffman conditions hold.

**Conclusion:** A and B are deadlocked.

### Example 2

**Question:** The same graph has two interchangeable instances of Y, one available. Does the visible cycle prove deadlock?

**Reasoning:** A can acquire the available instance, finish, and release X. The allocation model has capacity not represented by a simple actor cycle.

**Conclusion:** No. Resource multiplicity invalidates that inference.

### Example 3

**Question:** Two workers repeatedly acquire their left resource, fail to acquire the right, release, and retry in synchrony.

**Reasoning:** Transitions and releases continue, so the state is not permanently blocked. Neither obligation advances because the retry cycle preserves symmetry.

**Conclusion:** This is livelock. A queue, asymmetric turn, or suitable randomized protocol can break it.

### Example 4

**Question:** A reader-preference read/write lock continually admits arriving readers while a queued writer remains eligible.

**Reasoning:** The resource is active and readers progress, but the writer is bypassed without a finite bound.

**Conclusion:** The writer starves under that execution. Aggregate throughput does not refute it.

### Example 5

**Question:** A high-priority control thread waits for a mutex held by a low-priority logging thread while medium-priority computation repeatedly preempts the owner.

**Reasoning:** The high-priority thread depends on the low-priority owner, whose completion is delayed by unrelated intermediate priority work.

**Conclusion:** This is priority inversion. Priority inheritance can bound the inversion only under supported scheduler and locking assumptions.

### Example 6

**Question:** Why does a strict resource rank prevent circular wait?

**Reasoning:** Each blocking acquisition must move from a held lower rank to a requested higher rank. A cycle would require a strictly increasing chain to return below or equal to its first rank, contradicting strict order.

**Conclusion:** Circular wait is impossible if every relevant acquisition follows the immutable rank.

### Example 7

**Question:** A detector reports no Java platform-thread monitor or ownable-synchronizer cycles. Can the application be declared deadlock-free?

**Reasoning:** The official `ThreadMXBean` operation has a defined resource and thread scope. Application queues, database waits, network peers, or capacity pools may be outside it.

**Conclusion:** The result excludes only detected cycles within the supported observed scope.

### Example 8

**Question:** A shutdown sets `cancelled = true`, but a worker remains asleep indefinitely on a condition variable.

**Reasoning:** The cancellation state is present, but no wake makes the worker runnable. The checkpoint cannot execute.

**Conclusion:** Cancellation is incomplete. Update state under the condition protocol, wake the waiter, and make cleanup release ownership safely.

### Example 9

**Question:** What does this executable wait-for analysis establish?

<!-- bijux-verify: {"id":"bounded-wait-graph-cycle","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"nodes=5\nedges=4\ncycle=True\ncycle_path=worker_a->lock_b->worker_b->lock_a->worker_a\n","stderr":""}} -->
```python
waits = {
    "worker_a": ["lock_b"],
    "lock_b": ["worker_b"],
    "worker_b": ["lock_a"],
    "lock_a": ["worker_a"],
    "observer": [],
}
color = {node: "white" for node in waits}
parents = {}
found = []

def visit(node):
    color[node] = "gray"
    for target in waits[node]:
        if color[target] == "white":
            parents[target] = node
            if visit(target):
                return True
        elif color[target] == "gray":
            path = [target]
            cursor = node
            while cursor != target:
                path.append(cursor)
                cursor = parents[cursor]
            path.append(target)
            found.extend(reversed(path))
            return True
    color[node] = "black"
    return False

for candidate in waits:
    if color[candidate] == "white" and visit(candidate):
        break

print(f"nodes={len(waits)}")
print(f"edges={sum(len(targets) for targets in waits.values())}")
print(f"cycle={bool(found)}")
print(f"cycle_path={'->'.join(found)}")
```

**Reasoning:** The deterministic depth-first search finds one directed cycle in the explicitly supplied five-node graph and records its path.

**Conclusion:** It proves the expected result for this finite graph only. It does not establish that the edges were observed coherently, that they represent blocking waits, that the state is reachable, or that a real application is deadlocked.

### Example 10

**Question:** A railway interlocking controller sometimes stops granting routes. May a bounded wait-for trace and passing recovery test justify automatic cancellation in service?

**Reasoning:** Route release, fail-safe states, timing constraints, hardware interfaces, independent hazards, certification evidence, and operational authority exceed this chapter's model. Incorrect cancellation could create a safety consequence.

**Conclusion:** No completion or deployment claim is justified without a named, authorized railway safety reviewer and the applicable assurance process. This chapter supplies analytical questions, not external review or operational approval.

## Cross-Program Connections

- **Algorithms:** directed-cycle detection, strongly connected components, topological order, and well-founded ranking turn traces into analyzable structures.
- **Operating systems:** scheduling, mutex protocols, process failure, and resource allocation determine the semantics behind dependency edges.
- **Distributed systems:** partial observation, leases, failure detectors, transactions, and message capacity complicate the coherent-state assumption.
- **Databases:** lock managers commonly detect cycles and abort victims; transaction rollback and external effects determine recovery safety.
- **Real-time systems:** priority inheritance, ceiling protocols, bounded blocking, and response-time analysis replace vague fairness with explicit bounds.
- **Software engineering:** ownership boundaries, structured cancellation, observability, and deterministic test seams make progress behavior maintainable.
- **Security:** an adversary may intentionally exhaust pools or force retry collisions, converting progress weaknesses into denial of service.
- **Formal methods:** temporal logic, model checking, fairness, ranking functions, and refinement establish claims beyond sampled executions.

## References

1. Edward G. Coffman Jr., Melanie Elphick, and Arie Shoshani, “System Deadlocks,” *ACM Computing Surveys* 3(2), 1971, [doi:10.1145/356586.356588](https://doi.org/10.1145/356586.356588).
2. Richard C. Holt, “Some Deadlock Properties of Computer Systems,” *ACM Computing Surveys* 4(3), 1972, [doi:10.1145/356603.356607](https://doi.org/10.1145/356603.356607).
3. Edsger W. Dijkstra, “Hierarchical Ordering of Sequential Processes,” *Acta Informatica* 1, 1971, [doi:10.1007/BF00289519](https://doi.org/10.1007/BF00289519).
4. Leslie Lamport, “Proving the Correctness of Multiprocess Programs,” *IEEE Transactions on Software Engineering* SE-3(2), 1977, [doi:10.1109/TSE.1977.229904](https://doi.org/10.1109/TSE.1977.229904).
5. Lui Sha, Ragunathan Rajkumar, and John P. Lehoczky, “Priority Inheritance Protocols: An Approach to Real-Time Synchronization,” *IEEE Transactions on Computers* 39(9), 1990, [doi:10.1109/12.57058](https://doi.org/10.1109/12.57058).
6. Maurice Herlihy, Nir Shavit, Victor Luchangco, and Michael Spear, *The Art of Multiprocessor Programming*, second edition, Morgan Kaufmann, 2020.
7. IEEE and The Open Group, *POSIX.1-2024*, “pthread_mutexattr_getprotocol,” current Issue 8 interface for mutex priority protocols, [official specification](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_mutexattr_getprotocol.html) (retrieved 2026-08-29).
8. Oracle, *Java SE 26 & JDK 26 API*, “ThreadMXBean,” current deadlock-detection and synchronization-monitoring scope, [official API](https://docs.oracle.com/en/java/javase/26/docs/api/java.management/java/lang/management/ThreadMXBean.html) (retrieved 2026-08-29).
9. Nancy A. Lynch, *Distributed Algorithms*, Morgan Kaufmann, 1996.
10. Leslie Lamport, *Specifying Systems*, Addison-Wesley, 2002, [author-hosted edition](https://lamport.azurewebsites.net/tla/book.html).

## Exercises

### Exercise 1

A service has two worker pools. Request handlers in pool H hold a database connection while synchronously submitting parsing work to pool P. Each parser needs to call back into pool H before returning. At the incident state, every H worker waits for P, every P worker waits for H, and all connections are held by H. Construct a typed dependency graph, classify the failure, and name two structurally different preventions.

### Exercise 2

Prove by contradiction that assigning every resource an immutable strict rank and allowing acquisition only in increasing order prevents circular wait. List three implementation details that can invalidate the proof even if most call sites appear ordered.

### Exercise 3

Two agents use the rule “if the other requests the resource, yield and retry immediately.” Produce a four-transition repeating trace, define a semantic rank that exposes failure, and compare randomized backoff with queued turn-taking.

### Exercise 4

A lock test completes 100,000 critical sections, but one waiter enters none. Explain why throughput evidence is insufficient. Define a bounded-bypass assertion and identify the scheduler and owner-progress assumptions needed to interpret it.

### Exercise 5

A medical infusion controller's watchdog cancels a blocked dosing operation after 200 milliseconds and restarts its worker. Specify what the timeout proves, the cancellation and state-recovery evidence required, and the boundary at which named authorized human review is mandatory.

## Answers to the Exercises

### Answer 1

Use actor nodes H and P plus capacity nodes for each pool and the database pool. H → P-capacity means handlers wait for parser admission or completion while H-capacity → H records occupied worker slots. P → H-capacity and P-capacity → P close the worker dependency; database-capacity → H records retained connections. In the stated reachable snapshot no worker can execute the callback that releases the cycle, so this is capacity deadlock, not merely slow parsing. Prevention options include making the parser operation asynchronous so H releases its worker and connection before waiting, or reserving end-to-end capacity under one admission authority. A dedicated callback executor may also break the cycle if its capacity and failure behavior are independently guaranteed.

### Answer 2

Assume a circular wait over resources (r_1,...,r_k). Because each actor holds one resource and requests the next only upward, (rho(r_1) < rho(r_2) < ... < rho(r_k) < rho(r_1)). Transitivity gives (rho(r_1) < rho(r_1)), contradicting irreflexivity. Therefore no circular wait exists. The proof can fail when a callback acquires a lower-ranked hidden lock, a cleanup/error path reverses order, or ranks change while resources remain held. Unranked external resources and conditional aliases are additional hazards.

### Answer 3

One repeating trace is A observes B requesting and yields; B observes A requesting and yields; A retries; B retries, returning to the equivalent conflict state. Let rank be the number of successfully committed owners, or lexicographically `(unresolved_request, committed_owner_exists)` with an order that improves only when one request is resolved. Every cycle leaves the rank unchanged, exposing livelock. Independent randomized backoff reduces synchronized retries probabilistically but needs assumptions for a probability-one claim. A FIFO queue or monotonic ticket deterministically selects a next owner, at the cost of queue management and convoying.

### Answer 4

Throughput aggregates successful actors and says nothing about one waiter's outcome. Record an admission counter when waiter (p) becomes continuously eligible and assert that its eventual admission occurs before more than (B) competing admissions. Interpret the assertion only if (p) remains eligible, owners eventually release, the scheduler eventually runs runnable owners and (p), queue state is not reset, and cancellation or priority policy does not legitimately remove (p). A finite test can exhibit a bound violation but cannot prove an unbounded execution property universally.

### Answer 5

The watchdog proves only that the observed operation did not finish within 200 milliseconds. Evidence must show cancellation becomes visible, wakes every possible blocking primitive, reaches a checkpoint, stops or accounts for device commands, releases or consistently repairs owned state, records exactly one terminal outcome, and makes restart idempotent. Tests must cover cancellation races before enrollment, during device interaction, and after effect commitment. The chapter cannot authorize a clinical timing threshold, dose-state recovery rule, hardware fail-safe behavior, or deployment. Those decisions require a named, authorized medical-device safety and clinical reviewer operating under the applicable assurance process; no such external review is claimed here.
