---
module_id: CONPAR-063
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 63
title: Transactional Retry and Composition
status: complete
last_verified: 2026-08-29
---

# Transactional Retry and Composition

## One-Page Review

### Governing question

How can an atomic operation declare that its current observations do not permit progress, wait without missing a relevant change, and compose sequential and alternative blocking behaviors without exposing partial effects?

### Essential definitions

- **Semantic retry** is a transaction's program-requested result meaning “this attempt cannot proceed from the state I observed”; it differs from a concurrency-conflict abort.
- A **retry dependency set** contains transactional locations whose observed values justified retry and whose change can make re-execution useful.
- **Enrollment** registers a retrying transaction to be notified about relevant commits.
- A **missed wakeup** occurs when enabling state changes between checking a predicate and becoming a waiter, leaving the operation asleep despite enabled work.
- A **spurious or stale wakeup** resumes an operation although re-execution still cannot proceed; correct code rechecks its predicate.
- **Sequential composition** combines transactional actions into one larger atomic action whose intermediate writes remain tentative.
- **Alternative composition** tries one atomic action and, when it semantically retries, discards that branch and tries another.
- **left bias** means a successful first alternative is selected without evaluating the second, so alternative choice need not be fair or commutative.
- A **wake set** is the set of locations whose commits can make a blocked transaction eligible to rerun.
- **effect isolation** prevents observable nontransactional actions from escaping attempts or branches that retry or abort.

### Central model, mechanism, or theorem

On `retry`, an STM discards tentative writes, validates the observations, atomically enrolls the thread on the read-derived wake set, and blocks. Any commit changing a member can wake it; the transaction then reruns from the beginning and rechecks the predicate. For `p orElse q`, p runs in an isolated nested context. If p succeeds, its tentative effects become the alternative's result. If p retries, they are discarded and q begins from the enclosing transactional state. If both retry, the enclosing operation retries on the union of dependencies required by both branches. These rules make guarded operations compositional.

### Critical invariants

Retry publishes no transactional or external effects. Enrollment is ordered with validation so enabling commits cannot be lost. Waking grants only permission to recheck, not a resource or successful outcome. Each rerun recomputes dependencies. A failed alternative cannot leak writes into the next branch. If every alternative retries, the wake set covers each branch's enabling observations. Branch choice follows specified bias, not assumed fairness. Exceptions and cancellation are distinct from retry. Empty dependency sets, shutdown, timeout, overload, and resource lifetime have explicit behavior.

### Common failures

Programs poll instead of waiting; check then enqueue a waiter nonatomically; perform I/O inside retryable code; retain a first branch's tentative reservation while running the second; wait only on the final failed branch; assume one wake corresponds to one available item; use `orElse` as a fair scheduler; catch retry as an exception; read no transactional location before retry; encode timeout by reading wall time inside a transaction; create a wake storm on a hot variable; or leave wait registrations and deferred intents alive after cancellation.

### Compact example

`take(red) orElse take(blue)` first reads empty red and retries. Its red-side tentative work is discarded; blue contains B, so the combined transaction takes B and commits. If both queues are empty, it blocks on changes to either queue. An enqueue to blue cannot be missed between the empty check and sleep because validation and waiter enrollment form one protocol.

### Connections

[Software Transactional Memory](061-software-transactional-memory.md) defines atomic attempts and effects. [Optimistic Concurrency and Validation](062-optimistic-concurrency-and-validation.md) supplies validation-window reasoning. [Thread Pools and Bounded Work Queues](019-thread-pools-and-bounded-work-queues.md) and [Backpressure in Asynchronous Pipelines](040-backpressure-in-asynchronous-pipelines.md) provide production capacity contexts.

## Governing Question

What semantic and runtime rules let independently written transactional operations block and choose alternatives as larger atomic operations, while preserving safety, wakeup completeness, resource bounds, and honest progress?

The key is to treat “cannot proceed” as a first-class transactional outcome rather than an external condition-variable protocol or an ordinary exception.

## Why This Matters

Atomic updates alone do not compose blocking. A queue's `take` is useful only if it can wait when empty. A program may need “take from urgent or normal,” “acquire two resources together,” or “wait for completion or cancellation.” With locks and condition variables, each composed operation must coordinate lock ordering, predicate loops, notification, and cleanup across abstractions. A local correct implementation may expose too little information to compose safely.

Transactional retry derives notification dependencies from the reads already performed by the transaction. Tentative changes disappear when the transaction cannot proceed. Alternative composition can run guarded operations in isolation and combine their dependencies. This is an unusually strong form of modularity: a caller combines operations without opening their lock and waiter implementations.

The abstraction still has limits. Waking all observers of a popular variable can be expensive. Left-biased choice can starve a branch. A condition that depends on time or external I/O does not change a transactional variable by itself. A transaction can wait forever on an impossible predicate. Correct blocking is not a deadline, fairness, durability, or effect guarantee.

## Prerequisites and Retrieval

Retrieve:

- condition predicates from [Condition Variables and Predicate Waiting](013-condition-variables-and-predicate-waiting.md);
- queues and shutdown from [Thread Pools and Bounded Work Queues](019-thread-pools-and-bounded-work-queues.md);
- atomic attempt semantics from [Software Transactional Memory](061-software-transactional-memory.md);
- complete dependency validation from [Optimistic Concurrency and Validation](062-optimistic-concurrency-and-validation.md); and
- overload behavior from [Backpressure in Asynchronous Pipelines](040-backpressure-in-asynchronous-pipelines.md).

Retrieval prompt: for “wait until queue nonempty or cancellation requested,” identify the predicate, every enabling state change, the instant at which a missed wakeup could occur, and the state that must be rechecked after waking.

## Learning Objectives

After completing this module, a learner can:

1. distinguish semantic retry, conflict abort, exception, cancellation, timeout, and operation failure;
2. derive retry dependencies from transactional reads and predicates;
3. explain an atomic validate-enroll-block protocol that prevents missed wakeups;
4. derive sequential and alternative composition semantics;
5. trace branch-local tentative effects and union wake sets;
6. state useful algebraic laws and where bias/fairness prevents stronger laws;
7. design bounded queues, multi-resource acquisition, cancellation, and timeout using transactional state;
8. analyze wake amplification, starvation, empty dependency sets, and shutdown;
9. specify proof, test, and operational evidence for a retry runtime; and
10. require human review for high-consequence guarded actions.

## Core Exposition

### Four outcomes that must stay separate

A transaction can **commit** because its program completed and validation succeeded. It can suffer a **conflict abort** because concurrent interference invalidated the attempt; the runtime may rerun it immediately or under policy. It can invoke **semantic retry** because the currently observed state does not satisfy its program guard. It can raise an **exception** or receive **cancellation**, which follow language/API-specific propagation and cleanup rules.

Conflating them breaks contracts. An empty queue is not an exceptional runtime fault. A conflict does not mean the queue predicate is false. Cancellation is not permission to wait for a later queue change. A timeout may happen after another transaction committed the logical operation. Each terminal or suspended state needs an explicit result and owner.

In a Haskell-style STM, `retry` has no return value of any ordinary type: if executed, the current path cannot continue. The runtime abandons its tentative effects and may block until a transactional variable it read changes. “May” matters: the semantic guarantee is safe retry behavior, not one exact scheduling or notification implementation.

### Deriving the wake set

Consider `take(queue)`. It reads the queue. If nonempty, it writes the tail and returns the head. If empty, it retries. The queue variable belongs to the dependency set because its value justified the guard. A commit changing it can make rerun useful.

Now consider `withdraw(account,n)` guarded by `balance >= n` and `account.open`. Its retry depends on balance and open state. Recording only balance misses reopening. Recording every global transaction would wake correctly but cause unnecessary work. The semantic goal is a complete, reasonably precise set of versioned authorities whose change covers every way the guard can become true.

Derived and negative predicates follow the validation rules of module 062. If “any matching item exists” depends on an index or collection membership, reading only existing members is insufficient. The transaction must read an authority that changes when a matching item can appear.

Dependencies are attempt-local. On rerun the transaction may take another branch or read a different set, so old waiter entries cannot define the next wait. They must be removed, replaced, or made harmless by a correct generation protocol.

### Preventing missed wakeups

A broken implementation checks an empty queue, releases protection, then registers as a waiter. An enqueue between check and registration sees no waiter; the take sleeps indefinitely although the queue is nonempty. Condition-variable code prevents this by checking and sleeping under one monitor protocol.

STM needs the corresponding validate-enroll-block protocol. After `retry`, the runtime validates that the read observations remain current while it installs wait registrations under synchronization compatible with committing writers. If validation fails, it must not sleep; it reruns because a relevant change already occurred. If validation and registration succeed, any later relevant commit can observe or otherwise signal the waiter.

Blocking the operating-system thread can happen after registration because notification state already protects the gap. Implementations must handle a notification racing with the transition to sleep—commonly with a scheduler token, condition variable, futex state, or queue flag that remembers notification rather than requiring perfect timing.

Waking is advisory. Several waiters may wake for one item; another can consume it first. A stale wake can occur when state changes away and back before scheduling. Every awakened transaction re-executes its guard and can retry again. Code that assumes wake ownership reintroduces races.

### Sequential composition

Transactional bind/sequencing lets action A's tentative writes be visible to later action B within the same transaction but not to other transactions. If B retries, the enclosing transaction's entire tentative effect—including A—disappears. If B throws an exception, semantics decide whether an internal handler can observe tentative state, but uncaught failure cannot silently commit A.

This enables `transfer = withdraw(source,n); deposit(destination,n)` without a caller-visible intermediate state. It also enables `acquire(a); acquire(b)` to wait atomically rather than holding a while blocked for b. With locks, hold-and-wait could deadlock or monopolize a scarce resource. With retry, the tentative acquisition of a is discarded and the transaction can wait on state used by both guards.

Sequential composition can enlarge read and write sets, conflict windows, and wake dependencies. Semantic modularity does not eliminate performance analysis. A helper that reads a global statistics TVar can make every caller conflict or wake.

### Alternative composition

For `p orElse q`, execute p in a nested transactional context. If p returns, the combined action returns p's result and q is not selected. If p calls retry, discard p's tentative writes and evaluate q from the enclosing state. If q returns, its effects become the result. If q also retries, discard both branches and propagate retry with a wake set covering relevant reads from both.

Branch isolation is essential. Suppose p tentatively removes an item, then discovers a missing token and retries. q must not see the item as removed. This is not ordinary exception catch over a mutable log unless rollback and read/write views implement the specified nesting.

The union wake set is also essential. If p waits on red and q waits on blue, sleeping only on blue means a new red item may never wake the transaction. When either changes, rerun begins with p because selection is recomputed under left bias.

The following deterministic model records branch-local writes and read dependencies. It illustrates alternative selection and union waits; it is not a concurrent STM scheduler or implementation.

<!-- bijux-verify: {"id":"transactional-choice-retry","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"choice=blue:B\nstate={'red': [], 'blue': []}\nboth_status=retry\nboth_wake=['blue', 'red']\nrollback_choice=blue:C\nflag_after=False\n","stderr":""}} -->
```python
def take_branch(state, queue_name, writes):
    reads = {queue_name}
    queue = writes.get(queue_name, state[queue_name])
    if not queue:
        return {"status": "retry", "reads": reads, "writes": {}}
    writes[queue_name] = queue[1:]
    return {"status": "ok", "reads": reads, "writes": writes, "value": f"{queue_name}:{queue[0]}"}


def choose(state, first, second):
    left = take_branch(state, first, {})
    if left["status"] == "ok":
        return left
    right = take_branch(state, second, {})
    if right["status"] == "ok":
        return right
    return {"status": "retry", "reads": left["reads"] | right["reads"], "writes": {}}


state = {"red": [], "blue": ["B"]}
result = choose(state, "red", "blue")
for key, value in result["writes"].items():
    state[key] = value
print(f"choice={result['value']}")
print(f"state={state}")

empty = {"red": [], "blue": []}
blocked = choose(empty, "red", "blue")
print(f"both_status={blocked['status']}")
print(f"both_wake={sorted(blocked['reads'])}")

state = {"red": [], "blue": ["C"], "flag": False}
discarded_left_writes = {"flag": True}
left = take_branch(state, "red", discarded_left_writes)
result = take_branch(state, "blue", {}) if left["status"] == "retry" else left
for key, value in result["writes"].items():
    state[key] = value
print(f"rollback_choice={result['value']}")
print(f"flag_after={state['flag']}")
```

The explicit `discarded_left_writes` demonstrates the rule; real runtimes use nested logs. The model omits validation, concurrent enrollment, memory ordering, exceptions, and scheduling.

### Algebraic laws and observational limits

At the level of results and transactional effects, `retry orElse q` behaves like q. If p succeeds, `p orElse retry` behaves like p; if p retries, the whole expression retries. If both alternatives retry, associating a chain should preserve the combined dependency coverage, assuming the language's precise exception and evaluation semantics.

Alternative choice is not generally commutative: when both p and q can succeed, `p orElse q` selects p while `q orElse p` selects q. It is not a fair merge. Reassociation can also affect evaluation cost, exceptions, strictness, and which reads happen before success. Laws must state the observational model rather than treating `orElse` as Boolean disjunction.

Sequential composition distributes over alternatives only under carefully stated purity and transactional semantics. External effects, unsafe operations, exception behavior, or resource allocation can invalidate intuitive rewrites. Equational reasoning is valuable precisely because the effect boundary is constrained.

### Exceptions and catch

An exception communicates failure, not “wait for state to change.” Catching it can run a handler now; retry suspends/reexecutes. In GHC STM, transactional exception operations and catch rules have specific behavior, while asynchronous exceptions and `unsafeIOToSTM` require special care. Portable reasoning must cite the selected runtime rather than infer universal rules.

If a branch raises an exception rather than retrying, `orElse` does not ordinarily mean “try the other branch.” A separate transactional exception handler may be needed. Turning every error into retry can create permanent sleep because no relevant TVar change can repair invalid input or a programmer bug.

Allocation inside a transaction is runtime-specific. If an exception value contains a newly allocated transactional reference, semantics may preserve enough allocation to represent it even while rolling back ordinary writes. Do not generalize from “abort discards writes” to undocumented memory/resource behavior.

### Cancellation and shutdown alternatives

A robust blocking operation often composes work with shutdown:

`take(work) orElse (read(stopping); if stopping then return Closed else retry)`.

When work exists, left bias may keep selecting work even after shutdown. That can be desired draining or an error; put the policy into branch ordering and predicates. For immediate stop, test stopping in the work branch or prefer the stop branch. For drain, close admission then consume until empty before returning closed.

Thread cancellation must unregister or invalidate wait entries and release nested logs, retained objects, and tracing state. Cancellation racing wakeup and commit must have one terminal outcome. A blocked thread should not require another application-state change merely to notice cancellation unless cancellation itself is represented by a transactional variable included in the alternatives.

### Timeouts and time

Wall-clock or monotonic time does not become a transactional dependency by being read inside a transaction. If no TVar changes at the deadline, a retrying transaction will not wake. A common design creates a transactional timeout flag changed by a timer outside STM, then composes the guarded operation with a branch reading that flag.

The timer owns a lifecycle: creation, cancellation when work wins, race at deadline, and shutdown cleanup. The combined transaction determines a serialization order between work availability and the timeout flag. The public API must specify which wins if both are true; left bias makes that choice visible.

Do not allocate an unbounded timer/thread per wait without accounting. Shared timer wheels or cancellation scopes may be required at scale. Use monotonic deadlines for duration; civil-clock adjustments must not extend or shorten policy accidentally.

### Fairness and wake amplification

`orElse` left bias can starve a lower-priority branch whenever the first remains enabled. Reversing order per call, using an explicit transactional turn variable, weighted scheduling, or a fair queue can implement policy, but each adds shared state and conflict. Never claim fairness from composition alone.

When an enqueue wakes every waiter on one queue, one commits and the rest rerun and sleep: a thundering herd. Implementations can target waiters, use per-key/version queues, batch capacity, or rely on runtime scheduling, but notification selectivity must not miss a transaction whose composite predicate became true.

Measure wait-set size, wait registrations, wakeups per commit, useful wake ratio, reruns per success, queue delay, branch selections, oldest wait, cancellations, and retained memory. High cardinality labels can themselves become an overload path.

### Impossible and empty waits

Calling retry before reading any transactional location produces an empty dependency set. No transactional commit can be identified as enabling. A runtime may block forever, reject it, or require external interruption; the program must not treat it as a useful sleep.

Even a nonempty set can encode an impossible predicate: wait for a closed counter to increase when no writer remains. Model terminal state explicitly and compose it into the guard. Ownership/lifecycle proofs must show who can still make each wait condition true.

Deadlock freedom from lock ordering does not imply application progress. A cycle of logical dependencies—A waits for B's flag while B waits for A's—can persist without locks. Wait-for-state models and shutdown tests remain necessary.

### Effects and resource reservations

All code before possible retry must be transactionally rollbackable or pure. Logging, metrics increments, random generation, network calls, file writes, physical commands, and ordinary mutex acquisition can escape. Buffer diagnostic facts by logical attempt or emit after commit; operational tooling should distinguish blocked logical operations from every speculative run.

A transactional reservation is tentative until commit. If downstream work is external, commit a uniquely identified intent and let an owned dispatcher act afterward. Volatile STM does not close a crash window or make delivery exactly once. Durable queues/databases need their own recovery and idempotency protocol.

### Implementation and proof evidence

Specify operational semantics for return, retry, alternative, sequencing, exception, and cancellation. Prove branch isolation, union dependency completeness, validate-enroll atomicity, no missed notification, no abstract effect on retry, and one commit serialization. State what spurious wakes and duplicate notifications are allowed.

Test with deterministic barriers around predicate read, retry, validation, enrollment, notify, sleep, wake, cancellation, and commit. Include a writer before enrollment, during sleep transition, after enrollment, and before rerun. Use model checking for two branches and waiters, mutation tests dropping one dependency, randomized histories, exception/cancellation injection, leak tests, and shutdown.

Operational experiments cover empty/hot/disjoint queues, many waiters, one/many resources, left branch continuously enabled, both branches enabled, long dependency sets, oversubscription, timeout storms, cancellation, close/drain, and resource exhaustion. Correctness tests do not establish fairness; throughput does not establish missed-wakeup freedom.

## Definitions and Notation

- `P(s)`: guard predicate over transactional state s.
- `R(T)`: locations read by transaction attempt T.
- `D(T)`: retry dependencies derived from T's observations.
- `W(T)`: tentative writes, discarded on retry.
- `enrolled(T,x)`: T is registered for relevant commits to x.
- `wake(T)`: scheduler permission for T to rerun, not proof P is true.
- `p ⊕ q`: left-biased transactional alternative composition.
- `ret(v)`, `retry(D)`, `throw(e)`: distinct transactional outcomes.
- `sel(p,q,s)`: branch chosen by alternative semantics in state s.
- `A_w`: wake amplification, total wakeups divided by useful committed wakes.

For both-retry alternatives, the central dependency equation is `D(p ⊕ q) = D(p) ∪ D(q)` under the enclosing snapshot/log semantics. It does not say branch writes are unioned; both branches' tentative writes are discarded.

## Mechanisms, Invariants, or Proof Structure

### No-lost-wakeup proof

Take the last validation of observed state and successful enrollment as one logical interval protected against relevant commits. If a commit occurs before validation, validation fails and T reruns. If it occurs after enrollment, notification persists and T reruns. There is no third gap in which a relevant commit can occur unnoticed. Then prove scheduling/sleep state cannot erase an already-issued notification.

### Branch-isolation proof

Run p with a child log over the enclosing view. A successful p merges its permitted tentative state; a retrying p discards its child writes before q starts. Thus q observes the same enclosing transactional state it would have observed without p, except for explicitly specified allocation/evaluation effects. Assign the combined commit only after the selected branch and enclosing transaction validate.

### Dependency-completeness proof

For a retrying guard, any state transition capable of making the path return must change at least one authority in D. For two retrying alternatives, the union preserves that property for either branch. Conservative extra dependencies preserve wake completeness but can amplify wakeups.

### Progress scope

Safety permits endless retry. A liveness claim must state that some enabling writer exists, relevant commits notify, the scheduler eventually runs the waiter, validation can succeed, branch bias does not starve the needed path, and resources remain available. Fairness and bounded deadlines require additional mechanisms.

## Alternatives and Trade-Offs

| Mechanism | Advantage | Principal obligation |
|---|---|---|
| Condition variable/monitor | mature, explicit predicate and scheduling | shared lock discipline and manual composition |
| Semaphore/channel | ownership/capacity can be direct | multi-resource atomic choice is harder |
| STM retry | dependency-derived modular blocking | instrumentation, wake cost, effect restrictions |
| STM `orElse` | composes guarded alternatives | left bias, nested logs, union wake semantics |
| Polling | simple prototype | latency, load, timer lifecycle, no atomic composition |
| Async select over channels | composable events in suitable runtimes | cancellation ownership and event-versus-state semantics |
| Central owner/scheduler | explicit fairness and effects | queue/owner bottleneck and failure |
| Durable workflow/database | recovery and external coordination | latency, storage protocol, idempotency |

Choose state-based retry when the enabling condition is transactional and composition matters. Choose event/channel or owner designs when ownership and effects are primary. Use durable workflows when waits must survive process failure.

## Failure Modes and Misconceptions

- **“Retry means immediate loop.”** Semantic retry can suspend on observed transactional state.
- **“Conflict abort and retry are identical.”** One is concurrency control; one is program logic.
- **“Wake means success.”** Every wake must recheck the guard.
- **“Notify after check is close enough.”** The gap loses enabling commits.
- **“Only the last branch matters.”** Both-retry choice needs union dependencies.
- **“First-branch writes remain for the second.”** Retrying branch effects are isolated and discarded.
- **“Alternative is fair.”** Left bias can starve later branches.
- **“Exceptions try the next branch.”** Retry and throw have different semantics.
- **“Time passing wakes STM.”** A transactional authority must change.
- **“Empty read set sleeps efficiently.”** It has no application-state wake source.
- **“No locks means no logical deadlock.”** Impossible and cyclic conditions persist.
- **“One item should wake one waiter.”** Runtime notification may be broader.
- **“STM rollback undoes I/O.”** External effects escape attempts.
- **“Close is just another Boolean.”** Admission, drain, waiter release, and destruction need a state machine.
- **“Tests prove fairness.”** Schedules observed empirically do not prove universal service.

## Worked Examples

### Example 1

**Empty queue.** `take` reads `[]` and retries on the queue TVar. Enqueue commits `[J]`, wakes the waiter, and rerun removes J transactionally. **Conclusion:** retry derives waiting from the same state that defines the guard.

### Example 2

**Missed wakeup.** A broken runtime validates empty, an enqueue commits, then it registers and sleeps. Correct validate-enroll ordering either detects the enqueue and reruns or registers before it and receives notification. **Conclusion:** waiter timing is a correctness protocol.

### Example 3

**Acquire two resources.** A transaction tentatively decrements pool A, finds B empty, and retries. A's decrement disappears; it waits on dependencies for both guards rather than monopolizing A. **Conclusion:** sequential retry enables atomic multi-resource composition.

### Example 4

**Alternative queues.** Urgent is empty and normal has N. `take urgent orElse take normal` discards urgent's branch and commits N. If both empty, either enqueue can wake it. **Conclusion:** branch isolation plus union wakes implements composable choice.

### Example 5

**Left-bias starvation.** Urgent is perpetually nonempty, so the normal branch never runs even as normal ages. Add an explicit quota/turn policy or separate fair scheduler. **Conclusion:** alternative composition specifies choice, not fairness.

### Example 6

**Timeout branch.** A timer outside STM commits `expired=True`. `take q orElse checkExpired` wakes on q or expired; branch ordering specifies the simultaneous case. Cancel the timer when work wins. **Conclusion:** time must enter through transactional state with owned lifecycle.

### Example 7

**Exception is not retry.** Parsing a corrupt transactional message raises `InvalidMessage`. Retrying would sleep until an unrelated change and repeat the same bug. Abort/quarantine under a specified handler. **Conclusion:** permanent failure needs an error path, not a wait path.

### Example 8

**Thundering herd.** One enqueue wakes 1,000 waiters; one commits and 999 reread empty. Correctness holds, but `A_w` is high. Targeted notification, sharding, batching, or a different queue can reduce waste. **Conclusion:** wake completeness and selectivity are distinct.

### Example 9

**Shutdown choice.** `take work orElse stopped` with work first drains; stopped first terminates immediately. If admission stays open, drain may never finish. **Conclusion:** branch order belongs to a complete close/admission state machine.

### Example 10

**Emergency-power transfer.** A controller waits for either safe grid restoration or validated generator readiness before switching a critical facility. Transactional retry can compose sensor-state predicates but cannot itself establish sensor authenticity, physical breaker state, deadlines, fail-safe actuation, or durability. Named electrical-safety, controls, hardware, formal-methods, cybersecurity, human-factors, facilities operations, regulatory, and independent assurance reviewers must approve predicates, time bounds, fallback, tests, and residual risk; none is claimed here. **Conclusion:** composable waiting is only one reviewed component of a physical safety protocol.

## Cross-Program Connections

- **Programming languages:** monadic effects and operational semantics enable equational composition of guarded actions.
- **Operating systems:** futexes, scheduler tokens, cancellation, and timer ownership implement wait/wake behavior.
- **Distributed systems:** uncertain results and durable workflows show where volatile retry stops.
- **Databases:** predicate waits, transactional queues, and notification face isolation and recovery boundaries.
- **Performance engineering:** wake amplification, conflict, skew, and timer storms determine viability.
- **Software architecture:** shutdown, admission, drain, and effect dispatch need explicit owners.
- **Formal methods:** no-lost-wakeup and branch-isolation proofs connect semantics to runtime logs.
- **Safety engineering:** guarded state must be traced to authenticated evidence and physical action.

## References

1. Tim Harris, Simon Marlow, Simon Peyton Jones, and Maurice Herlihy, “Composable Memory Transactions,” PPoPP 2005. <https://doi.org/10.1145/1065944.1065952>
2. Tim Harris, Simon Marlow, Simon Peyton Jones, and Maurice Herlihy, “Composable Memory Transactions,” *Communications of the ACM* 51(8), 2008. <https://doi.org/10.1145/1378704.1378725>
3. GHC Project, `Control.Monad.STM` documentation for `atomically`, `retry`, and `orElse`, stm 2.5.1.0; retrieved 2026-08-29. <https://downloads.haskell.org/ghc/9.6.6/docs/libraries/stm-2.5.1.0/Control-Monad-STM.html>
4. GHC Project, “Software Transactional Memory,” GHC User's Guide, current development documentation; retrieved 2026-08-29. <https://ghc.gitlab.haskell.org/ghc/doc/users_guide/exts/stm.html>
5. Simon Marlow, *Parallel and Concurrent Programming in Haskell*, O'Reilly Media, 2013. <https://simonmar.github.io/pages/pcph.html>
6. Maurice Herlihy and Nir Shavit, *The Art of Multiprocessor Programming*, revised first edition, 2012. <https://www.elsevier.com/books/the-art-of-multiprocessor-programming/herlihy/978-0-12-397337-5>
7. Keir Fraser, *Practical Lock-Freedom*, University of Cambridge PhD thesis, 2004. <https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-579.pdf>
8. Butler W. Lampson and David D. Redell, “Experience with Processes and Monitors in Mesa,” *Communications of the ACM* 23(2), 1980. <https://doi.org/10.1145/358818.358824>
9. Andrew D. Birrell, “An Introduction to Programming with Threads,” DEC SRC Research Report 35, 1989. <https://www.microsoft.com/en-us/research/publication/an-introduction-to-programming-with-threads/>
10. IEEE and The Open Group, POSIX condition-variable wait specification, Issue 8, 2024; retrieved 2026-08-29. <https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_cond_wait.html>

## Exercises

### Exercise 1

Distinguish semantic retry, conflict abort, exception, cancellation, and timeout. For each, state whether immediate rerun, blocking, propagation, or an uncertain result may be appropriate.

### Exercise 2

Trace `take(A) orElse take(B)` when both are empty, then B receives one item before waiter enrollment. Show the required logs, dependency set, and no-missed-wakeup outcome.

### Exercise 3

A branch reserves one unit, writes an ordinary log, then retries; its alternative succeeds. Diagnose the transactional and external effects and redesign the instrumentation.

### Exercise 4

Design `acquire(cpu=2,memory=4) orElse stopped` for a bounded scheduler. Specify guards, branch ordering, wake dependencies, fairness, cancellation, close/drain, and overload evidence.

### Exercise 5

A rail system uses transactional retry to wait for a route or an emergency-stop state. Specify semantics, no-lost-wakeup proof, timing/failure boundaries, evidence, and mandatory human review.

## Answers to the Exercises

### Answer 1

Semantic retry says current transactional observations do not enable progress: discard tentative state and block/rerun when a dependency changes. Conflict abort says concurrent validation failed: recompute immediately, back off, or enter coordinated fallback. An exception reports a program/domain/runtime failure and propagates or enters an explicit handler; it should not silently wait. Cancellation asks the owner to stop and must release registrations/resources, though commitment before observation can yield an uncertain result. Timeout says a deadline expired; it requires a timer/state source and, if commitment raced the response, may also be uncertain. Eligibility, idempotency, and terminal status are specified separately.

### Answer 2

The A child log reads A and retries; its writes are discarded. The B child log reads B and retries. The enclosing retry uses `D={A,B}` and no branch writes. If B changes before enrollment, final validation of B's observed version fails, so the runtime does not sleep and reruns; B succeeds. If enrollment completes first, B's commit records notification, even if the thread has not yet physically slept, and rerun succeeds. Sleeping with neither validation failure nor durable notification would expose the forbidden gap.

### Answer 3

The transactional reservation belongs to the failed branch and must be discarded before the alternative runs. The ordinary log is irrevocable and incorrectly survives, describing a reservation that never committed; repeated reruns duplicate it. Record no external log inside the retryable branch. After the combined transaction commits, emit one logical outcome keyed by operation identity, or commit a transactional diagnostic/effect intent that an owned dispatcher processes. Runtime attempt tracing, if necessary, must label speculative attempts and remain bounded without altering transaction semantics.

### Answer 4

Read CPU availability, memory availability, and lifecycle state transactionally. The acquisition branch requires both quantities, tentatively decrements both, and otherwise retries on both authorities. Put `stopped` first for immediate termination or acquisition first for drain; document simultaneous truth. Admission closes before drain, and terminal stopped/closed must wake impossible resource waiters. Cancellation is another transactional alternative or runtime cancellation that unregisters safely. Fairness needs queued age/turn policy rather than `orElse`; bound retries and waiter count. Test all partial capacities, concurrent release, stop races, one/many waiters, starvation, thundering herd, cancellation, timeout, overload, retained registrations, and final resource accounting.

### Answer 5

Define route topology, occupancy, points, signal state, authority, emergency state, and a fail-safe invariant forbidding conflicting movement. Make emergency branch priority explicit; route retry dependencies must cover every state/predicate whose change can enable or invalidate the route. Prove validate-enroll atomicity: a change before enrollment invalidates and reruns, while one after enrollment leaves notification; prove branch isolation, union dependencies, serialization, and terminal cleanup. STM does not supply physical deadline, authenticated sensing, command acknowledgement, durable recovery, or fail-safe behavior, so specify bounded response, independent emergency path, idempotent commands, restart/reconciliation, hardware-in-loop faults, overload, and manual control. Named signaling-domain, functional-safety, real-time/runtime, formal-methods, hardware, cybersecurity, human-factors, operations/maintenance, quality/regulatory, and independent assurance reviewers must approve requirements, evidence, fallback, and residual risk. No internal exercise constitutes approval.
