---
module_id: DBE-045
program: Database Engineering
level: 1
module_number: 45
title: Deadlock Detection and Resolution
status: complete
last_verified: 2026-08-30
---

# Deadlock Detection and Resolution

## One-Page Review

### Governing question

How does a database distinguish a true cyclic wait from ordinary blocking, choose and roll back a victim safely, restore progress, and prevent retries from becoming a second incident?

### Essential definitions

A transaction is **blocked** when it cannot currently obtain a required resource but another transaction may release that resource without first depending on the waiter. A **deadlock** is a reachable state in which every member of a nonempty set waits for another member to act, so none can progress without external intervention. A **wait-for graph (WFG)** has active transaction/task nodes and directed edge `Ti -> Tj` when Ti's pending request cannot be granted until protection owned by Tj changes. A directed **cycle** identifies deadlock under the graph's stated single-site conjunctive-wait model and exact current grant policy. A **strongly connected component (SCC)** is a maximal set whose nodes mutually reach one another; an SCC of size greater than one, or a self-loop, contains a cycle. A **victim** is a transaction selected for abort/cancellation so its dependencies and locks can be removed. **Rollback cost** estimates work to undo and repeat. **Deadlock prevention** structurally excludes a necessary condition; **avoidance** admits work only when a safe completion state remains; **detection and recovery** permits cycles, finds them, and removes participants.

### Central model, mechanism, or theorem

When a lock request blocks, the lock manager derives edges to every owner or earlier queued request that truly prevents grant under its compatibility and queue policy. A cycle `T1 -> T2 -> ... -> Tk -> T1` means each transaction in that cycle is waiting and at least one required predecessor is another cycle member; no member can reach normal lock release. Detection may run on each wait, incrementally, periodically, or after a delay to trade detection CPU for victim latency.

Resolution is not “kill a query.” Under a lock-manager/recovery boundary, the system chooses an eligible victim using explicit priority, undo/restart cost, resources released, age/deadline, and starvation history; marks it doomed; stops further transactional work; rolls back the required scope; preserves recovery invariants; removes all owned/requested graph state; wakes waiters; and returns a classified error. The application retries the entire required transaction boundary only when its inputs, deadline, idempotency, and external effects make retry safe. Detection repeats because one victim need not break every cycle in a complex SCC.

### Critical invariants

- Every WFG edge represents a current, grant-blocking dependency under exact resource identity, compatibility, conversion, and queue rules.
- Transaction, parallel task, session, prepared transaction, and external-resource identities are mapped without merging unrelated owners or splitting one owner unsafely.
- Cycle conclusions state the resource model; stale monitoring snapshots and multi-instance/OR-wait models do not inherit the simple theorem automatically.
- Victim selection never overrides protected/system/prepared-transaction rules and has deterministic, auditable tie-breaking where policy permits.
- Victim rollback restores transactional state before protected writes become accessible and removes every held/requested dependency exactly once.
- Survivors are awakened/rechecked against current compatibility rather than assumed grantable from the old graph.
- Retry recreates the whole failed atomic unit, uses stable transaction intent/idempotency, obeys a deadline/budget, and adds backoff/jitter/admission control.
- Detection reports and metrics preserve enough normalized resource/order evidence to remove recurring causes without exposing sensitive values.

### Common failures

Failures include calling every long wait a deadlock; treating timeout as cycle detection; building edges from requests that are compatible or allowed to bypass; omitting lock conversions, predicate ranges, metadata, transaction-ID, parallel exchange, or advisory resources; using a racy dashboard snapshot as the detector; assuming any graph cycle is sufficient under every resource model; always killing the youngest/smallest transaction until it starves; releasing victim locks before rollback protection is safe; retrying only the failed statement when the transaction was aborted; retrying external side effects; immediate synchronized retry storms; deleting deadlock logs without signatures; and lowering isolation before proving the invariant still holds.

### Compact example

T1 holds A and waits for B held by T2; T2 holds B and waits for C held by T3; T3 holds C and waits for A held by T1. The WFG has `T1->T2->T3->T1`. T4 waiting for B adds `T4->T2` but is blocked, not a cycle member. Suppose T2 has already been a victim once, T1 has high undo cost, and T3 is cheaper without retry-starvation history. Abort/undo T3, remove `T2->T3` and `T3->T1`, wake T2, and re-evaluate grants. T4 may remain normally blocked. One resolved cycle does not mean the queue is empty.

### Connections

Retrieve [Two-Phase Locking](044-two-phase-locking.md), [Lock Modes and Granularity](043-lock-modes-and-granularity.md), and [ACID and Transaction Boundaries](041-acid-and-transaction-boundaries.md). Continue through the Database Engineering [roadmap](../ROADMAP.md) to DBE-046, Multi-Version Concurrency Control, and DBE-047, Snapshot Visibility.

## Governing Question

Which dependency graph faithfully represents the lock scheduler's current inability to grant work, and how can the system break cycles without compromising atomicity, recovery, fairness, or service stability?

## Why This Matters

Deadlock is expected in dynamic pessimistic concurrency control. Two transactions update the same objects in opposite order; two shared readers both convert to exclusive; a foreign-key check and parent update visit indexes differently; a parallel query owns workers while waiting for an exchange consumer; or application and database locks form a cross-layer cycle. Each operation can be locally correct while the group cannot progress.

Waiting alone is not failure. A reporting transaction may wait behind a short update and then proceed. A timeout may fire because the owner is slow, preempted, or waiting on I/O without any cycle. Conversely, an actual deadlock will persist forever if no participant aborts, even though each lock request is valid. Incorrect diagnosis produces either needless aborts or indefinite stalls.

Database engines therefore maintain dependency information closer to the scheduler than ordinary monitoring can. They detect cycles, pick a victim, and integrate cancellation with transaction recovery. Applications still own the final reliability contract: engines can abort a transaction but cannot safely repeat an email, payment request, or non-idempotent remote call; nor can they decide whether the caller's deadline has expired.

Frequent deadlocks are not merely random bad luck. They are workload evidence: inconsistent access order, overly broad plans, missing indexes, conversions, long transactions, excessive parallelism, or hot logical resources. A production-grade design makes individual deadlocks safe and bounded, then groups recurring graph signatures and removes the dominant causes without weakening invariants.

## Prerequisites and Retrieval

You should understand S/X/intention/range locks, lock queues and conversions, strict two-phase locking, transaction abort/undo, graphs, directed cycles, depth-first search, and idempotent retries. Retrieve blocking versus waiting, precedence graph, lock point, compatibility, queue fairness, predicate domain, WAL, savepoint, statement versus transaction rollback, timeout, deadline, and backpressure.

Do not confuse the WFG with DBE-044's precedence graph. A precedence edge records an already ordered read/write conflict and supports serializability reasoning. A wait-for edge records a current inability to obtain a resource and supports liveness reasoning. Their vertices may also differ when an engine models tasks, workers, exchanges, or prepared participants.

## Learning Objectives

After this module, you can:

1. distinguish ordinary blocking, deadlock, starvation, livelock, priority inversion, and slow work from causal evidence;
2. derive exact wait-for edges from granted modes, conversion requests, queues, and resource ownership;
3. find cycles and SCCs and state when cycle detection is necessary and sufficient;
4. compare immediate, incremental, periodic, and delayed detection costs;
5. design victim eligibility, priority, cost, fairness, and deterministic tie-breaking policy;
6. trace victim abort, undo, lock/request cleanup, wakeup, and grant re-evaluation safely;
7. compare detection/recovery with ordering, conservative acquisition, wait-die, wound-wait, no-wait, and timeout policies;
8. build transaction-level retry with idempotency, backoff, jitter, deadline, budget, and overload control;
9. interpret current PostgreSQL, MySQL InnoDB, and SQL Server deadlock evidence without false portability; and
10. test and observe deadlock handling using event-driven schedules, graph oracles, invariant checks, and normalized signatures.

## Core Exposition

**Separate liveness states.** Blocking means a request cannot be granted now. If the owner can complete without depending directly or indirectly on the waiter, this is ordinary blocking. Deadlock means a closed dependency set cannot progress. Starvation means a request remains eligible but repeatedly loses under scheduling/fairness. Livelock means participants change state—abort, retry, yield—but none completes. Priority inversion means high-priority work depends on lower-priority work delayed by other scheduling. Slow I/O/CPU work may resemble blocking but has no resource cycle.

These states need different remedies. Cycle detection resolves deadlock, not starvation. A timeout bounds latency but cannot identify cause. Backoff can reduce livelock/retry contention but does not repair a permanently inconsistent acquisition order. Faster hardware can shorten a slow owner while leaving the logical cycle possible.

**Construct the wait-for graph from grant semantics.** Let nodes be active transaction owners at the atomicity scope the lock manager can abort. When request R by Ti is queued, determine why it cannot be granted. Add `Ti -> Tj` for each other owner Tj whose granted incompatible protection must change before R can proceed. If the queue has fairness/conversion rules that forbid bypass, an earlier queued request can also create a dependency even when its mode is not currently granted. The detector must model the actual policy, not just the S/X matrix.

Resource identity matters. A row X request may wait on an index-key lock, a foreign-key check may wait on a parent key, a table request may depend on descendant intentions, and a predicate write may wait on a range/gap. Modern engines may protect writes through transaction-ID locks or version dependencies. A parallel request can involve exchange ports, worker threads, memory grants, or communication buffers in addition to data locks. If ownership is split among tasks but abort occurs at transaction scope, mapping must preserve both dependencies and the actionable victim.

Do not add edges to every holder indiscriminately. Compatible owners do not block. A conversion may be blocked by other holders while retaining its current mode. A waiter may depend on multiple owners. Queue-order dependencies can disappear if bypass is legal. Edges are a derived, mutable view of the lock table and scheduler state.

**When a cycle proves deadlock.** In the conventional centralized lock model, each waiting transaction needs its pending incompatible request granted before it can continue to normal release, and edges exactly name the blockers required to change. A directed cycle means every cycle member requires another member to release/change first; none can do so through normal execution. Conversely, a deadlocked set contains such circular dependency, so cycle detection is necessary and sufficient.

Qualify that theorem. With multiple interchangeable resource instances, a cycle may be necessary but not sufficient because an outside instance can satisfy a request. With OR waits—proceed when any alternative responds—a simple WFG cycle can overstate deadlock. Distributed observations may combine edges that never coexisted, producing phantom cycles. Conditional queues, leases, participant failure, and external systems need their own model. A database's internal detector can use atomic scheduler state or a proven algorithm; an operator assembling several DMV snapshots cannot assume equivalent consistency.

**Cycle and SCC algorithms.** Starting from a newly blocked transaction, depth-first search can ask whether a path returns to it. A full graph can be checked in `O(V+E)` using DFS coloring or Tarjan/Kosaraju SCCs. An SCC of size greater than one contains cycles; a singleton is deadlocked only with a self-loop. SCCs are helpful because several cycles may overlap. Selecting one arbitrary victim may not break every cycle in a complex SCC, so resolve, mutate the graph, and detect again.

Graph cost depends less on asymptotic notation than on hotspot shape, lock count, queue length, edge construction, and frequency. On a highly contended resource, every new waiter can create many blocker/queue relationships. Incremental detection reuses changes but complicates correctness. Full checks on every wait minimize detection latency but can consume CPU. Periodic/delayed checks amortize overhead but let real cycles persist longer.

PostgreSQL's current `deadlock_timeout` illustrates delayed checking: a waiter pauses before the relatively expensive deadlock check, trading needless checks against reporting latency. The value is not “time until something is declared deadlocked”; after the delay the engine checks causality. MySQL documents immediate/automatic InnoDB detection by default and allows disabling it on extreme hotspots in favor of lock-wait timeout, changing both cost and resolution latency. SQL Server documents periodic lock-monitor searches that accelerate after detections. These are implementation choices, not definitions.

**Detection scope determines blind spots.** An InnoDB detector cannot necessarily see locks owned by another storage engine or layer unless integration exposes them. A database detector cannot see an application mutex held while its transaction waits unless the application dependency enters the same graph. A service can deadlock across database lock -> connection pool slot -> application mutex -> database session while each individual subsystem sees no local cycle. Avoid holding one coordination domain while calling another, or build explicit cross-layer ordering/diagnostics.

Prepared distributed transactions deserve special treatment. After voting prepared in two-phase commit, a participant may hold locks while awaiting a durable coordinator decision and cannot safely choose itself as an ordinary local deadlock victim. An in-doubt wait can look like a stuck blocker rather than a locally resolvable cycle. Operators need coordinator/recovery evidence and protocol-specific resolution, not arbitrary lock killing.

**Victim selection is policy under constraints.** Detection produces one or more candidate cycle members. First apply eligibility: never choose recovery/system work, already rolling-back work, or a prepared participant if the protocol forbids unilateral abort. Respect explicit priority only when its semantics are documented. Then estimate rollback/restart cost: undo/log volume, rows changed, elapsed work, locks/resources released, downstream waiters, scarce worker/memory release, transaction criticality, and remaining deadline.

“Kill the smallest” is a useful heuristic, not a theorem. Aborting a tiny transaction can release few relevant resources and repeatedly victimize the same request. Aborting a long transaction wastes work but may unlock an entire convoy. Oldest/youngest policies trade wasted work against latency and starvation. User-provided priority can protect essential work but can also make low-priority jobs never finish.

Make fairness history explicit. Retain retry/deadlock-victim count or stable age across retries, cap repeated victimization, and use deterministic tie-breaking for reproducibility unless the engine defines otherwise. Never let clients spoof unrestricted priority across tenants. Record the actual engine's chosen victim and rollback cost; do not infer it from which error reached the application first.

The executable model below finds one deadlocked SCC. Its illustrative policy avoids a transaction already victimized once, then minimizes estimated undo plus lock-release bookkeeping and elapsed work. This is a transparent teaching policy, not a claim about any vendor.

<!-- bijux-verify: {"id":"wait-for-cycle-resolution","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"wait_for_edges=(('T1', 'T2'), ('T2', 'T3'), ('T3', 'T1'), ('T4', 'T2'))\ndeadlocked_sccs=(('T1', 'T2', 'T3'),)\nvictim=T3\nvictim_score=(False, 1300, 500, 'T3')\nremaining_edges=(('T1', 'T2'), ('T4', 'T2'))\nresolution_acyclic=True\ninvariants=True\n","stderr":""}} -->
```python
edges = {
    ("T1", "T2"),
    ("T2", "T3"),
    ("T3", "T1"),
    ("T4", "T2"),
}
transactions = {
    "T1": {"undo_bytes": 4000, "locks": 3, "age_ms": 800, "retries": 0},
    "T2": {"undo_bytes": 500, "locks": 2, "age_ms": 200, "retries": 1},
    "T3": {"undo_bytes": 900, "locks": 4, "age_ms": 500, "retries": 0},
    "T4": {"undo_bytes": 0, "locks": 0, "age_ms": 50, "retries": 0},
}

def strongly_connected_components(nodes, graph_edges):
    outgoing = {node: [] for node in nodes}
    for source, target in graph_edges:
        outgoing[source].append(target)
    for targets in outgoing.values():
        targets.sort()

    index = 0
    indices = {}
    lowlink = {}
    stack = []
    on_stack = set()
    components = []

    def visit(node):
        nonlocal index
        indices[node] = index
        lowlink[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)
        for target in outgoing[node]:
            if target not in indices:
                visit(target)
                lowlink[node] = min(lowlink[node], lowlink[target])
            elif target in on_stack:
                lowlink[node] = min(lowlink[node], indices[target])
        if lowlink[node] == indices[node]:
            component = []
            while True:
                member = stack.pop()
                on_stack.discard(member)
                component.append(member)
                if member == node:
                    break
            components.append(tuple(sorted(component)))

    for node in sorted(nodes):
        if node not in indices:
            visit(node)
    return tuple(sorted(components))

def deadlocked_components(nodes, graph_edges):
    components = strongly_connected_components(nodes, graph_edges)
    return tuple(
        component
        for component in components
        if len(component) > 1 or (component[0], component[0]) in graph_edges
    )

def victim_score(transaction):
    facts = transactions[transaction]
    estimated_cost = facts["undo_bytes"] + 100 * facts["locks"]
    was_already_victim = facts["retries"] > 0
    return (was_already_victim, estimated_cost, facts["age_ms"], transaction)

deadlocked = deadlocked_components(transactions, edges)
cycle_members = deadlocked[0]
victim = min(cycle_members, key=victim_score)
remaining = {edge for edge in edges if victim not in edge}
resolution_acyclic = not deadlocked_components(transactions, remaining)
invariants = (
    cycle_members == ("T1", "T2", "T3")
    and "T4" not in cycle_members
    and victim == "T3"
    and resolution_acyclic
)

print(f"wait_for_edges={tuple(sorted(edges))}")
print(f"deadlocked_sccs={deadlocked}")
print(f"victim={victim}")
print(f"victim_score={victim_score(victim)}")
print(f"remaining_edges={tuple(sorted(remaining))}")
print(f"resolution_acyclic={resolution_acyclic}")
print(f"invariants={invariants}")
```

**Resolution is a recovery operation.** After selection, atomically mark the victim unable to issue new transactional actions. Interrupt or signal its execution at a safe boundary. Undo the whole transaction or documented rollback scope using the recovery manager. Under strict protection, do not expose its uncommitted writes during undo. Remove its granted locks, conversion requests, queue entries, worker dependencies, and bookkeeping; wake affected waiters; then re-evaluate requests against the new state and queue policy.

The ordering prevents races: if locks disappear before the victim is doomed, it might continue and mutate without protection; if dirty data becomes readable before undo completes, survivors can consume state being erased; if one queue entry remains, a ghost edge can block progress; if the application gets success before outcome is known, retry/reconciliation breaks.

The engine returns a classified deadlock-victim error. Scope matters. Some systems roll back the entire transaction for deadlock but only a statement for a lock-wait timeout; savepoint behavior varies. Application code must inspect the current engine contract and explicitly reset/rollback the connection before reuse. A pooled connection carrying an aborted or open transaction is a correctness and capacity defect.

**Retry the transaction intent, not the last SQL line.** A deadlock victim's earlier statements have been undone. Reissuing only the statement that received the error can omit reads, checks, and writes that defined the atomic unit. Encapsulate the complete transaction in a retryable function with fresh snapshot/locks and stable business input.

Retry is safe only when effects outside the database are absent, idempotent, or coordinated through a durable pattern such as an outbox. Use an idempotency/business-operation key for externally visible intent. Bound attempts by an end-to-end deadline and retry budget; use exponential or decorrelated backoff plus jitter; stop on nonretryable errors; propagate cancellation; and rate-limit/admit retries so a hotspot does not amplify load. Keep the same deadlock-prevention timestamp across retries when a wait-die/wound-wait protocol depends on age.

**Prevent recurring cycles where economical.** A global resource order breaks circular wait when every path—including triggers, constraints, indexes, advisory locks, and maintenance—obeys the same durable order. Sort dynamic keys canonically before locking. Acquire the strongest needed mode early enough to avoid conversion cycles where the concurrency cost is acceptable. Narrow access paths and ranges through correct indexes. Move remote/human work outside the transaction. Reduce batch lock footprint only if each smaller commit is a valid restartable state.

Conservative 2PL acquires the full declared set all-or-none, avoiding lock-wait deadlock but requiring advance knowledge and early locking. **Wait-die** gives stable timestamps: an older requester waits for a younger holder; a younger requester aborts (“dies”) when blocked by older. **Wound-wait** lets an older requester abort (“wound”) a younger holder; a younger requester waits for older. Stable age across retry prevents starvation in the idealized protocol. Both reduce cycles but can increase aborts and need exact multi-holder policy.

No-wait aborts immediately on conflict; timeout aborts after elapsed wait whether or not a cycle exists. They bound resource occupancy but sacrifice completed work and do not diagnose deadlock. Banker's-style avoidance needs maximum future claims and is uncommon for dynamic database transactions. MVCC reduces reader/writer blocking but writers, constraints, predicates, metadata, and memory/worker resources can still deadlock.

**Observe graphs, not anecdotes.** A deadlock report should include timestamp, engine/version/configuration, victim and reason/cost/priority, every process/transaction/task, statement and plan identifiers, transaction age/isolation/state, resource type and normalized identity, held/requested mode, owner/waiter edges, queue/conversion state, input/bind signature (redacted), retry attempt, rollback duration, and outcome. Preserve full reports under controlled retention.

Normalize recurring signatures by transaction template plus resource class and acquisition-order edge, not volatile session IDs or literal customer keys. Track deadlocks per committed transaction, victim rate, retries-to-success, rollback work/time, lock wait p95/p99, affected endpoint/tenant class, and top signatures. A falling deadlock count with rising timeouts or invariant failures is not an improvement.

PostgreSQL warns that the exact victim is difficult to predict and recommends consistent lock order. MySQL exposes recent/all InnoDB deadlock evidence and documents whole-transaction rollback for deadlock versus configuration-dependent timeout scope. SQL Server's current deadlock graph captures victim/process/resource lists, and `system_health` collects detected graphs by default. Field names and victim rules are product-specific; build adapters into one conceptual schema without discarding original evidence.

**Test causal schedules.** Use separate explicit sessions and barriers/hooks, not sleeps, to establish: T1 owns A; T2 owns B; T1 is waiting for B; then T2 requests A. Assert exactly one classified victim, required rollback scope, survivor completion, final invariant, clean pooled connections, and bounded retry. Repeat with three-way cycles, conversions, row/range/metadata/advisory locks, victim priority, cancellation races, and deadlock during rollback where supported.

Test ordinary blocking without a cycle to reject false detection, a timeout without a cycle, a self-loop if the engine can represent it, multiple overlapping cycles requiring repeated victims, victim-selection ties, protected/ineligible participants, and stale monitoring samples. Stress with hot keys, skew, long/short transactions, plan changes, retries, and failover. Finite tests validate implementations and policies; they do not prove all schedules, so retain the graph/model argument and production monitoring.

## Definitions and Notation

- `W=(V,E)`: wait-for graph over actionable owners; `(Ti,Tj) in E` means Ti cannot progress until dependency owned by Tj changes.
- `Owner(R)`: owner(s) of granted protection on resource R.
- `Req(T,R,m)`: T's pending request for mode m on R, including conversion/queue state.
- `Blocks(Tj, Req_i)`: exact scheduler predicate that Tj prevents request i from being granted now.
- `SCC(W)`: maximal mutually reachable vertex set; size greater than one or a self-loop contains a cycle.
- **Victim:** selected transaction/task whose abort removes dependencies to restore progress.
- `cost(T)`: policy-specific estimate of undo, restart, released-resource benefit, deadline, and fairness impact.
- **Blocking:** current wait with a possible normal completion path.
- **Deadlock:** closed cyclic dependency requiring intervention.
- **Starvation:** indefinite denial despite repeated eligibility.
- **Livelock:** continuing state changes without useful completion.
- **Prevention:** structurally violate at least one necessary deadlock condition.
- **Avoidance:** grant only if the resulting state remains safe under declared future claims.
- **Detection/recovery:** allow waits, find actual deadlock under the model, abort/recover participants.
- **Deadlock signature:** normalized transaction/resource/order shape used to group recurring incidents.

## Mechanisms, Invariants, or Proof Structure

**Cycle proof in the conjunctive single-site model.** Assume every waiting transaction must receive its one pending request before reaching normal release; each edge names a blocker whose protection must change; transactions in the cycle cannot spontaneously abort or be externally preempted. For cycle `T1->...->Tk->T1`, T1 needs T2, T2 needs T3, and Tk needs T1. If any member were first to progress, its blocker immediately later in the cycle would have had to progress earlier, contradiction around the cycle. Thus intervention is necessary. Conversely, a finite deadlocked set has no member able to progress; following one required internal blocker repeatedly must revisit a node, yielding a cycle.

The proof fails if an edge is stale, the request can choose an outside alternative, an unmodeled lease expires, or a participant can normally release while waiting. State these assumptions before applying the result to distributed or multi-instance resources.

**Resolution invariant.** Let C be a detected cycle and v an eligible member. Mark v doomed, restore/undo its transactional effects under recovery protection, remove every held/requested dependency of v, and wake/re-evaluate waiters. At least the selected simple cycle is broken because both its incoming and outgoing v edges disappear. Other cycles can remain; run detection on the new graph. Correctness requires no uncommitted victim write becomes observable during the transition and no survivor is granted against incompatible remaining protection.

**Fairness invariant.** Victim policy should not choose the same logical operation indefinitely when alternatives exist. Preserve stable age or increase victim penalty across retries, bound retry admission, and test adversarial tie sequences. This is a policy guarantee, not implied by cycle removal.

**Independent verification plan.** Derive WFG edges from an explicit lock/queue table, calculate SCCs with a separate algorithm, enumerate simple cycles for small tests, apply documented eligibility/cost, remove all victim state, then recalculate graph and database invariant. Compare with engine deadlock reports and final transaction outcomes. Never use the implementation's own “deadlocked” flag as the only oracle.

## Alternatives and Trade-Offs

- **On-wait versus delayed detection:** immediate checks reduce deadlock duration but add work to every contention event; delay/periodic checks amortize cost while cycles hold resources longer.
- **DFS from waiter versus full SCC:** targeted reachability is cheap for a new edge; full SCC exposes overlapping cycles and supports analysis but touches the broader graph.
- **Cheapest rollback versus largest release:** minimizing wasted work may free little contention; aborting a larger blocker can unblock a convoy but waste more work.
- **Priority versus fairness:** protected work meets business criticality; unrestricted priority can starve other tenants and distort capacity.
- **Detection versus total order:** detection permits dynamic access and maximal opportunism with abort cost; a universal order removes circular wait but may require early/broader locking.
- **Detection versus wait-die/wound-wait:** detection finds realized cycles; timestamp prevention aborts before cycles but can increase restarts and needs stable timestamps.
- **Detector versus timeout:** a detector proves a modeled cycle and chooses a victim; timeout bounds individual waiting without causal proof.
- **Strict locking versus MVCC reads:** MVCC removes many read/write waits; write/write, predicate, metadata, worker, and cross-layer cycles remain.
- **Retry versus surfacing conflict:** transparent retry improves availability for short transient cycles; returning conflict may be safer when deadlines, external effects, or contention budgets are exhausted.
- **Local versus distributed detection:** local atomic state gives precise edges; distributed probes cover cross-node dependencies but pay message/state-consistency complexity and phantom-deadlock risk.

## Failure Modes and Misconceptions

- “A blocked query is deadlocked.” It may have a normal acyclic owner path.
- “The lock timeout detected the deadlock.” Elapsed time is not a graph proof.
- “Any cycle in any dependency graph proves deadlock.” The conclusion depends on conjunctive/current/single-instance assumptions.
- “Only granted lock holders create edges.” Conversion and queue policy can make earlier waiters causally blocking.
- “Every SCC needs exactly one victim.” One victim breaks its cycles only if it intersects them; detect again after mutation.
- “Abort the youngest every time.” Repeated deterministic sacrifice can starve one logical operation.
- “Release locks, then roll back.” Survivors must not observe victim state while undo is incomplete.
- “Retry the SQL statement that errored.” Deadlock commonly aborts the entire transaction boundary.
- “Retry immediately forever.” Synchronized retry can become livelock and overload.
- “MVCC eliminates deadlocks.” It removes some read locks, not every dependency.
- “Lower isolation fixes it safely.” It can trade visible deadlock for an invariant violation.
- “Consistent table order is sufficient.” Rows, indexes, ranges, constraints, triggers, advisory locks, and other resources also participate.
- “The database sees all dependencies.” Application mutexes, pools, remote services, and other engines can form invisible cross-layer cycles.
- “Victim error means rollback finished everywhere.” Verify transaction state, recovery scope, external effects, and connection reuse contract.
- “One captured graph is the root cause.” Normalize and compare recurring signatures with plan/workload evidence.

## Worked Examples

### Example 1

T1 holds A while T2 waits for A; T1 performs CPU work and will commit without waiting for T2. WFG has `T2->T1` and no cycle. Conclusion: this is ordinary blocking, even if a client timeout expires.

### Example 2

T1 holds A/waits B and T2 holds B/waits A. WFG cycle is `T1->T2->T1`. Conclusion: under exact conjunctive lock semantics neither can normally release; one must abort or be externally resolved.

### Example 3

T1 and T2 both hold S(A) and request X(A). Each conversion retains S and waits for the other. Conclusion: same-resource conversion can deadlock without opposite table order.

### Example 4

T1, T2, T3 form a cycle; T4 waits on T2 but owns nothing the cycle needs. T4 can reach the SCC but cannot be reached from it. Conclusion: T4 is blocked collateral, not a deadlock-cycle victim candidate.

### Example 5

Detector aborts cheap T2 for the third consecutive retry while expensive T1 always survives. T2 never commits. Adding stable age/victim history eventually protects T2 or rejects overload. Conclusion: cycle resolution without fairness can create starvation.

### Example 6

T3 is selected, marked doomed, undone under X protection, removed from queues/locks, and waiters are rechecked. T2 proceeds; T4 remains behind T2. Conclusion: resolution restores possible progress, not universal immediate grant.

### Example 7

Two transactions update accounts `{9,2}` in caller order and deadlock. Both instead sort stable account IDs and lock 2 then 9. Conclusion: a universally enforced total order removes this circular-wait shape without weakening atomicity.

### Example 8

A missing index makes each update scan and lock thousands of keys in plan-dependent order. Adding a correct selective index narrows and stabilizes footprints. Conclusion: physical design can remove deadlock frequency by changing actual resource traversal.

### Example 9

Victim transaction sent an email before its database commit; automatic retry sends it again. Moving intent to an outbox row committed atomically and deduplicating delivery makes transaction retry safe. Conclusion: database rollback does not undo external effects.

### Example 10

A service holds an application mutex, borrows a connection, and waits on a database lock; the database owner calls the service path and waits for that mutex. Neither subsystem's local graph contains the complete cycle. Conclusion: avoid nested coordination domains or instrument a cross-layer order/dependency model.

## Cross-Program Connections

- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies deadlock, starvation, livelock, lock ordering, and progress-proof concepts.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies directed graphs, DFS, SCCs, dynamic graph maintenance, and complexity analysis.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies resource allocation, scheduling, priority inversion, cancellation, and process recovery.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies distributed detection, stale observations, leases, prepared transactions, and coordinated recovery.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) supplies deadlines, idempotency, retry budgets, jitter, backpressure, and external-effect contracts.

## References

1. Philip A. Bernstein, Vassos Hadzilacos, and Nathan Goodman, [*Concurrency Control and Recovery in Database Systems*](https://www.microsoft.com/en-us/research/people/philbe/book/), Addison-Wesley, 1987, lock scheduling, wait-for graphs, prevention, detection, and recovery.
2. Edward G. Coffman Jr., M. J. Elphick, and Arie Shoshani, [“System Deadlocks”](https://doi.org/10.1145/356586.356588), *ACM Computing Surveys* 3(2), 1971, foundational deadlock conditions and treatment taxonomy.
3. K. Mani Chandy, Jayadev Misra, and Laura M. Haas, [“Distributed Deadlock Detection”](https://www.cs.utexas.edu/~misra/scannedPdf.dir/DistrDeadlockDetection.pdf), *ACM Transactions on Computer Systems* 1(2), 1983, distributed resource/communication deadlock algorithms and correctness.
4. PostgreSQL Global Development Group, [Explicit Locking: Deadlocks](https://www.postgresql.org/docs/current/explicit-locking.html#LOCKING-DEADLOCKS), current automatic detection, victim caveat, and consistent-order guidance.
5. PostgreSQL Global Development Group, [Lock Management](https://www.postgresql.org/docs/current/runtime-config-locks.html), current `deadlock_timeout` detection-cost/latency semantics.
6. Oracle, [MySQL 8.4 Deadlocks in InnoDB](https://dev.mysql.com/doc/refman/8.4/en/innodb-deadlocks.html), current automatic detection, timeout fallback, evidence, and retry guidance.
7. Oracle, [MySQL 8.4 Deadlock Detection](https://dev.mysql.com/doc/refman/8.4/en/innodb-deadlock-detection.html), current victim heuristic, graph limits, detector scope, and disabling tradeoff.
8. Oracle, [MySQL 8.4 InnoDB Error Handling](https://dev.mysql.com/doc/refman/8.4/en/innodb-error-handling.html), current deadlock versus lock-timeout rollback scope.
9. Microsoft, [SQL Server Deadlocks Guide](https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-deadlocks-guide?view=sql-server-ver17), current detector cadence, victim priority/cost, rollback, graph evidence, and handling.
10. Microsoft, [Use the `system_health` Session](https://learn.microsoft.com/en-us/sql/relational-databases/extended-events/use-the-system-health-session?view=sql-server-ver17), current default capture of detected deadlocks and deadlock graphs.

## Exercises

### Exercise 1

Given a lock table with granted S/X modes, two conversions, four queue entries, and one compatible bypass rule, derive the exact WFG. Classify ordinary blockers, cycle members, and collateral waiters.

### Exercise 2

Prove cycle necessity/sufficiency for the stated single-site conjunctive model. Give counterexamples showing why a stale distributed snapshot and an OR-wait/multiple-instance model need stronger analysis.

### Exercise 3

Implement a deterministic detector/resolver test harness with an independent SCC/cycle oracle, victim-policy oracle, rollback/cleanup assertions, and adversarial schedules.

### Exercise 4

Design victim and retry policy for short interactive transfers competing with a long batch. Compare rollback cost, released-resource benefit, priority, deadlines, fairness, and overload behavior.

### Exercise 5

Diagnose recurring production deadlocks spanning row/range locks, a plan regression, an application mutex, and a remote side effect. Produce a safe remediation and evidence plan across PostgreSQL, InnoDB, and SQL Server.

## Answers to the Exercises

### Answer 1

For each pending request, evaluate the exact current grant predicate. Add edges only to other owners whose incompatible granted mode must change, plus earlier queued/conversion requests when the documented fairness rule forbids bypass. A converter remains an owner of its original mode and a waiter for the stronger mode. Compatible holders produce no edge; a bypassable earlier waiter produces no causal edge. Run SCC: size>1 or self-loop nodes are cycle members under the model. A node with a path into the SCC but no path back is collateral blocking, not a candidate required to break the cycle. Annotate every edge with resource, held/requested modes, grant/queue basis, and observation generation so the derivation is auditable.

### Answer 2

Under the assumptions, follow each member of a deadlocked finite set to a blocker inside the set; repeated finite traversal revisits a node and yields a cycle. Conversely, in a cycle each member needs the next member's protection to change before progressing to normal release; choosing a hypothetical first progressor leads around the cycle to a predecessor that had to progress earlier, contradiction. A stale distributed collector can observe A waits B before B releases and B waits A only after that release: combined edges cycle but never coexist. In an OR-wait model, T1 may wait for T2 or an outside T3; an apparent T1/T2 cycle can dissolve when T3 responds. With multiple interchangeable instances, an outside release can satisfy a request despite the cycle. Use a consistent distributed/probe algorithm and a resource model capturing AND/OR/cardinality semantics.

### Answer 3

Represent atomic events for grant, wait, conversion, release, doom, undo, outcome, and wake with barriers controlling order. Derive edges from a lock-table snapshot in the scheduler, but have the test independently enumerate reachability/simple cycles for small graphs and compare with Tarjan SCC output. Verify no false cycle for a chain, exact cycles for two/three-way/conversion cases, self-loop policy, multiple overlapping cycles, and queue bypass. Compute victim eligibility/cost independently; inject ties/retry history/protected owners. After victim selection assert no further victim work, complete undo before exposure, all held/requested state removed once, survivors rechecked, graph recalculated, correct error scope, connection reset, and final data invariant. Bound the test externally to avoid hangs but never count timeout alone as detector success.

### Answer 4

Define nonspoofable priority classes and deadlines. Estimate undo/restart work from changed rows/log volume and elapsed work; estimate benefit from cycle edges, blocked dependents, scarce locks/workers, and remaining time. A short transfer is cheap but repeated sacrifice violates latency/fairness; preserve stable age or increase victim penalty per retry. A batch is expensive but may block a convoy and exceed its maintenance deadline; allow chunking only at valid restartable boundaries and use admission windows. Apply deterministic tie-breakers, cap attempts and total elapsed time, jitter/back off, and rate-limit retries. Favor ordering accounts/partitions identically and narrowing batch plans before relying on victim policy. Record chosen score components, rollback duration, retry-to-success, commits, and per-class starvation; policy success means bounded correct completion, not minimum single-victim cost.

### Answer 5

Collect complete native deadlock graphs plus engine/version/config/isolation, transaction templates, plans, exact row/key/range/metadata modes, conversions/queues, victim reason, rollback duration, retries, and final invariant. Normalize signatures. Reproduce with barriers and pinned plans. Repair the range invariant with a constraint, exact range/guard lock, or serializable validation; add/repair the index causing broad plan-dependent scans; impose canonical resource order across all database paths. The application-mutex/database cycle is invisible locally: remove nested holding, move database work outside the mutex, or establish one cross-layer order and tracing identity. Do not auto-retry a remote effect; put durable intent in an outbox/idempotency protocol and retry the complete database transaction within deadline/budget with jitter/admission. Verify separately on PostgreSQL delayed checking/SSI, InnoDB detector/scope/timeout rules, and SQL Server graph/victim/optimized-locking configuration. Compare deadlock, timeout, wait, rollback, retry, latency, commit, and invariant metrics; retain original graphs and state any cross-layer dependencies the engine cannot observe.
