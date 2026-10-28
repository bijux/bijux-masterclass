---
module_id: CONPAR-004
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 4
title: Safety, Liveness, and Progress
status: complete
last_verified: 2026-08-29
---

# Safety, Liveness, and Progress

## One-Page Review

### Governing question

Which concurrent correctness claims prohibit bad finite prefixes, which require desirable events eventually, and which guarantee that individual operations or the system continue despite interference?

### Essential definitions

- A **behavior** is a finite or infinite sequence of states or observations permitted by a specification.
- A **safety property** says that no bad thing happens; every violation has a finite bad prefix that cannot be repaired by extending it.
- An **invariant** is a state predicate true initially and preserved by every transition. Invariants prove many, but not all, safety properties.
- A **liveness property** says that some good event eventually happens; no finite prefix alone refutes pure liveness because it can still be extended favorably.
- **Termination** is eventual completion of a bounded computation. **Responsiveness**, **delivery**, and **recurrence** are other liveness forms.
- **Deadlock freedom** excludes a global state in which required work remains but no progress transition is possible.
- **Starvation freedom** requires each eligible operation or participant eventually to progress under stated assumptions.
- **Fairness** restricts infinite schedules. Weak fairness says a continuously enabled action eventually occurs; strong fairness says an action enabled infinitely often eventually occurs.
- A **progress condition** specifies who completes despite interference. Common nonblocking conditions include obstruction-freedom, lock-freedom, and wait-freedom.
- **Blocking progress** can depend on scheduler, lock holder, failure recovery, or external service behavior.
- A **response bound** strengthens eventuality with a stated time, step, or service constraint; ordinary liveness alone gives no deadline.

### Central model, mechanism, or theorem

For behavior property (P), safety means every behavior outside (P) has a finite prefix whose every extension remains outside (P). Liveness means every finite behavior prefix has some infinite extension in (P). Alpern and Schneider showed that every property can be decomposed into safety and liveness components under the trace model.

To prove invariant (I), establish (Init implies I) and, for every allowed step, (I and Next implies I'). To prove response (Request leads-to Grant), safety invariants alone are insufficient: one also needs a well-founded progress measure, enabledness argument, and explicit fairness or environment assumptions.

### Critical invariants

Every claim quantifies over a declared behavior set. Safety and liveness are properties, not testing labels. Invariant state includes monitor variables needed for history-sensitive safety. Liveness names the beneficiary, trigger, response, and fairness/environment assumptions. Stuttering is treated explicitly. Deadlock freedom does not imply starvation freedom. System-wide completion does not imply per-operation completion. Lock-free does not mean every call finishes; wait-free does not mean fast. Bounded finite search can find liveness counterexample cycles but a finite incomplete trace is not by itself starvation proof.

### Common failures

Teams call “the service usually responds” liveness; infer progress from no observed deadlock; hide scheduler fairness; assume enabled means scheduled; treat timeouts as proof of nontermination; prove mutual exclusion but not entry; prove some operation completes while one request starves; call lock use lock-free; call wait-free code latency-bounded; omit failures or cancellation; use average latency for universal response; or report a finite search horizon as an infinite-execution theorem.

### Compact example

Two clients request one critical section. Invariant (at most one owner) proves mutual exclusion. It says nothing about whether either client enters. A scheduler can stutter forever or repeatedly favor A. Weak fairness for B's continuously enabled acquire may establish eventual B entry if acquire stays enabled; if A repeatedly makes B enabled and disabled, strong fairness or a stronger queue discipline may be necessary.

### Connections

[Interleavings and State-Space Explosion](003-interleavings-and-state-space-explosion.md) supplied finite transition exploration. The [program roadmap](../ROADMAP.md) next refines races, deadlock/livelock/starvation, determinism, critical-section invariants, memory ordering, nonblocking progress, systematic testing, and failure containment.

## Governing Question

How should an engineer split “the concurrent program is correct” into claims that can be disproved by finite evidence, claims about infinite continuation, and guarantees about whose work advances?

The split determines both design and evidence. A safety violation can be a short trace. A liveness violation is often a reachable cycle or infinite unfair schedule. A progress guarantee depends on interference, scheduler, failures, resource admission, and the unit whose completion is promised. Mixing these creates impressive but irrelevant proofs.

## Why This Matters

Mutual exclusion can be perfect while no client ever enters. A queue can never lose an item yet permanently delay one producer. A lock-free stack can guarantee infinitely many completed operations while one unlucky thread retries forever. A timeout can preserve service responsiveness by abandoning work while violating a business obligation to complete it.

Lamport's 1977 multiprocess-program work made safety and liveness central generalizations of partial correctness and termination. Alpern and Schneider later gave trace-based characterizations and a decomposition result. These foundations remain useful because modern labels—async, actor, lock-free, reactive, distributed—do not alter the logical questions.

Operational reviews need both dimensions. Safety includes mutual exclusion, no duplicate commit, bounded inventory, type/state validity, and no use after cancellation. Liveness includes eventual response, queue drainage, retry success under recovery, heartbeat recurrence, and shutdown completion. Performance adds quantitative distributions and deadlines; it is not a substitute for either.

Fairness is where hidden assumptions accumulate. A program may prove entry only if a runnable task is eventually scheduled, a sent message is delivered, a lock holder does not crash, memory becomes visible according to its model, and the environment eventually responds. These are neither universal laws nor implementation details to omit. They are premises of the theorem and obligations of deployment.

## Prerequisites and Retrieval

Retrieve infinite sequences, prefixes, directed graphs, cycles, induction, well-founded orders, transition systems, enabled actions, scheduler choices, and state-space bounds. From CONPAR-003, distinguish a terminal state, deadlock state, finite trace, infinite cycle, context bound, and fairness assumption.

This chapter uses sequentially consistent abstract transitions. Memory-model progress and hardware forward-progress behavior require later modules and language/platform documentation.

## Learning Objectives

By the end of this module, you should be able to:

1. classify concrete correctness requirements as safety, liveness, quantitative, or mixed;
2. identify finite bad prefixes and construct monitor state for history-sensitive safety;
3. prove a state invariant through initiation and preservation;
4. express eventual response and recurrence over infinite behaviors;
5. distinguish weak fairness, strong fairness, scheduling policy, and probabilistic hope;
6. distinguish termination, deadlock freedom, livelock freedom, starvation freedom, and bounded response;
7. compare blocking, obstruction-free, lock-free, and wait-free progress scopes;
8. use ranking functions, leads-to chains, accepting cycles, and systematic scheduling appropriately;
9. state the limits of finite testing and timeout observations; and
10. connect formal properties to monitoring, SLOs, incident evidence, and authorized risk review.

## Core Exposition

A specification denotes behaviors. For transition system with initial predicate (Init) and next-state relation (Next), a behavior starts in an initial state and follows allowed steps, often including stuttering steps that leave modeled variables unchanged. A property selects acceptable behaviors. Program correctness is set inclusion: every implementation behavior, under stated assumptions, belongs to the property.

**Safety** is refutable by finite history. Once two clients occupy a one-owner critical section, later release cannot erase that violation from the trace. Once a non-idempotent charge is committed twice, later refund may compensate business harm but does not make “never double-charge” true. The finite bad prefix can include a property automaton or monitor state when the violation depends on event order.

Many safety properties are invariants. Mutual exclusion can be state predicate (owners <= 1). Conservation can compare balances plus in-flight value. Type-state validity can limit lifecycle combinations. Prove the predicate initially, then prove every allowed event preserves it. Concurrent proof must consider interference: an assertion established by one activity must survive another activity's steps.

Not every safety property is naturally a predicate over the application's raw state. “Never send acknowledgment before durable commit” depends on history. Add a ghost or monitor variable recording whether commit occurred, or transform the property into an automaton whose error state is invariantly unreachable. Monitor state is proof structure, not necessarily production storage.

**Liveness** requires infinite-behavior reasoning. “Every accepted request eventually receives success, declared failure, or cancellation” cannot be falsified by observing silence for any finite duration unless a deadline is part of the requirement. The request might complete next. A finite timeout is operational evidence and may violate a bounded-response property, but pure eventuality needs an infinite counterbehavior such as a reachable cycle with an outstanding request and no response.

Liveness includes different patterns. **Response** says every trigger is eventually followed by a result. **Persistence** says the system eventually reaches and remains in a condition. **Recurrence** says a condition occurs infinitely often. **Termination** says a particular computation eventually reaches a final state. These must identify correlation: “some response eventually occurs” is weaker than “every request receives its own response.”

Safety and liveness interact. A naive liveness repair can violate safety by granting two clients simultaneously. A safety repair can violate liveness by refusing all work. The decomposition theorem does not say designs may check the parts independently without shared assumptions; it says trace properties can be represented through the two categories.

Fairness removes certain infinite scheduler choices. Under **weak fairness**, if an action becomes enabled and remains enabled continuously, it eventually executes. Under **strong fairness**, if it is enabled infinitely often—even with gaps—it eventually executes. Strong fairness rules out more schedules and is harder to implement or justify. Round-robin queues, priorities, work stealing, and operating-system scheduling policies offer concrete but bounded approximations, not automatically mathematical fairness.

Fairness should attach to actions, not vague actors. A worker may be scheduled while a particular dequeue remains disabled. An actor may process messages while one low-priority mailbox entry starves. A network may deliver packets while one connection is continually reset. State exactly which action is enabled, what can disable it, and which scheduler or protocol guarantees selection.

Environment assumptions matter equally. An algorithm cannot guarantee completion if an essential remote service may fail forever, memory allocation may always fail, or a client never supplies required input. A conditional liveness claim takes the form: if request remains valid, required resources recover, messages are eventually delivered, and the scheduling action is fair, then response occurs.

Progress levels locate the beneficiary. **Deadlock freedom** says the system does not reach a global no-progress wait while obligations remain. **Livelock freedom** excludes infinite activity without relevant advancement. **Starvation freedom** says each qualifying operation or participant eventually advances. System throughput can remain high while one request starves.

Blocking algorithms may suspend behind an owner. They can be simple, efficient, and correct if ownership, priority inversion, failure, and scheduler behavior are managed. Nonblocking progress conditions describe execution under interference. An **obstruction-free** operation completes if it eventually runs alone long enough. A **lock-free** system guarantees that in a finite number of its own relevant steps, some operation completes, so global progress continues; one operation may starve. A **wait-free** operation completes within a finite bound on its own steps regardless of other participants, under model assumptions. Exact definitions vary in presentation, so code claims must cite their language and algorithm contract.

Progress in steps is not wall-clock latency. A wait-free algorithm can be delayed by an unscheduled thread, page fault, processor pause, resource exhaustion, or enormous step cost. Conversely, a blocking mutex implementation may meet excellent latency objectives under bounded contention. Formal progress and performance evidence answer different questions.

Progress proofs often use a **ranking function** into a well-founded order. Show that relevant progress transitions strictly decrease the rank and that fairness ensures one eventually occurs. Natural numbers cannot decrease forever, so the target is reached. Concurrent interference may increase one local measure; a lexicographic or global measure and supporting invariants may be required.

Leads-to reasoning composes progress: if (P leads-to Q) and (Q leads-to R), then (P leads-to R). Each link needs safety facts establishing enabledness and liveness premises establishing eventual transition. This explains why liveness proofs often depend on previously proved invariants.

Finite-state model checking searches cycles. A liveness monitor can mark an outstanding request and an accepting condition can identify a reachable cycle in which it remains outstanding. Fairness constraints remove unfair cycles. Bounds on state, actors, data, or depth still restrict the result. A long finite prefix without response is not by itself an infinite counterexample.

Systematic runtime testing can prioritize delay and progress bugs by controlling scheduling and virtual time. It can demonstrate a concrete deadlock, repeatable starvation within a bounded policy, or missed wakeup. It cannot observe literal infinity. A regression should turn the liveness obligation into a bounded test contract while preserving the separate unbounded argument.

The executable finite model below explores all sixteen length-four scheduler-choice words for two clients. A client acquires when waiting and the critical section is free, then releases and completes on its next selection. Every trace is safe, but only two complete both clients within the bound.

<!-- bijux-verify: {"id":"finite-safety-progress-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"schedules=16\nsafety_violations=0\nboth_done=2\nincomplete_by_bound=14\n","stderr":""}} -->
```python
schedules = [""]
for _ in range(4):
    schedules = [prefix + name for prefix in schedules for name in "AB"]

safety_violations = 0
both_done = 0

for schedule in schedules:
    phase = {"A": "waiting", "B": "waiting"}
    owner = None
    safe = True
    for name in schedule:
        if phase[name] == "waiting" and owner is None:
            phase[name] = "critical"
            owner = name
        elif phase[name] == "critical":
            phase[name] = "done"
            owner = None
        if sum(value == "critical" for value in phase.values()) > 1:
            safe = False
    if not safe:
        safety_violations = safety_violations + 1
    if all(value == "done" for value in phase.values()):
        both_done = both_done + 1

print(f"schedules={len(schedules)}")
print(f"safety_violations={safety_violations}")
print(f"both_done={both_done}")
print(f"incomplete_by_bound={len(schedules) - both_done}")
```

Execution proves finite counts for this synthetic transition model only. Fourteen incomplete prefixes are not liveness violations: each may extend to completion. The run does not establish fairness, infinite progress, real mutex behavior, weak-memory correctness, bounded latency, failure recovery, or production safety.

Cancellation changes the property. If cancellation is an allowed response, define who may request it, when commitment makes it too late, how children and resources are handled, and what the caller observes. “Eventually completes or cancels” is vacuous if the implementation may cancel every request immediately; useful liveness combines admissibility, service, and safety conditions.

Timeouts similarly add a safety-style deadline observation and a recovery protocol. A response after its deadline may be a finite violation of bounded response even though eventual response holds. Timeout must not create duplicate externally visible effects when retry overlaps the original.

Production monitoring observes proxies. Outstanding age, queue depth, oldest-item time, completion rate, scheduler delay, retry count, lock wait, cancellation latency, and heartbeat gaps can signal progress loss. An SLO gives a statistical population claim, not starvation freedom for every request. Retain identifiers so aggregate health cannot hide a permanently stuck operation.

## Definitions and Notation

Let (Sigma) be the state alphabet and (Sigma^omega) infinite behaviors. For finite prefix (u in Sigma^*), (Ext(u)) is the set of infinite extensions. Safety property (S) satisfies: for every behavior (b notin S), some finite prefix (u) of (b) has (Ext(u) intersect S = empty). Liveness property (L) satisfies: for every finite prefix (u), (Ext(u) intersect L != empty).

Temporal notation uses (always P), (eventually P), and response (P leads-to Q), meaning whenever (P) occurs, (Q) eventually follows under the specification. “Eventually always P” expresses stabilization; “always eventually P” expresses recurrence. These are distinct.

Weak fairness for action (A) excludes a behavior in which (A) remains enabled continuously from some point yet never occurs. Strong fairness excludes one in which (A) is enabled infinitely often but occurs only finitely often.

For operation set (O), lock-freedom concerns system-wide completion across continuing steps; wait-freedom additionally gives each operation a finite own-step completion bound. Both require declared atomic primitives and failure/scheduling model.

## Mechanisms, Invariants, or Proof Structure

Use this review sequence:

1. **Define behavior and observation.** Include stuttering, failures, cancellation, and environment steps.
2. **Decompose requirements.** Separate finite bad-prefix, eventual, recurrence, deadline, and statistical claims.
3. **Prove safety first.** Establish initialization, step preservation, and monitor completeness.
4. **Name progress beneficiary.** System, operation, client, queue item, or resource must be explicit.
5. **List enabling conditions.** State what can disable, retry, cancel, or supersede work.
6. **State fairness and environment premises.** Connect them to real scheduler, queue, network, and failure policy.
7. **Choose a well-founded argument.** Ranking functions or leads-to chains show that fair progress cannot postpone forever.
8. **Search cycles and finite failures.** Calibrate monitors and fairness on a small full state space.
9. **Test implementation boundaries.** Control schedule and virtual time; retain replayable evidence.
10. **Monitor deployment assumptions.** Detect old outstanding work, stalled rates, broken ownership, and premise violations.

Safety invariant proof requires (Init implies I) and preservation for every allowed transition, including failure and recovery. For response, find rank (rho) over outstanding states. Show nonnegative well-founded range, safety preservation of prerequisites, and that fair enabled progress eventually lowers (rho) or reaches response. If interference can reset rank indefinitely, the proof needs a stronger measure or stronger scheduling protocol.

Maintain these invariants:

- each requirement states subject, trigger, observation, and quantification;
- finite safety and infinite liveness evidence are not conflated;
- history-sensitive safety has monitor state;
- fairness is attached to concrete actions;
- environment recovery and delivery are explicit assumptions;
- global and per-operation progress are distinct;
- formal steps and wall-clock latency are distinct;
- cancellation and timeout preserve effect safety;
- finite tests report horizons and bounds; and
- safety-critical claims require named domain review.

## Alternatives and Trade-Offs

**Invariant safety** is local and inductive, but monitor design can be subtle. **Trace automata** express history directly but enlarge state. Use the smallest complete representation.

**Weak fairness** excludes continuous neglect with fewer assumptions. **Strong fairness** handles intermittent enablement but may be unrealistic or expensive. A FIFO admission protocol can provide a constructive starvation argument stronger than hoping for scheduler fairness.

**Blocking algorithms** often simplify state and perform well under low contention. They depend on owner scheduling and failure handling. **Nonblocking algorithms** avoid some owner stalls but add retry contention, reclamation, memory-order, and proof complexity.

**Wait-free guarantees** are strongest per operation but can cost helping, memory, and complex bounds. **Lock-free** designs may offer adequate system throughput while requiring explicit starvation mitigation. Choose by workload and consequence.

**Timeout-based service contracts** produce finite observable violations and operational control. Pure eventuality supports qualitative reasoning without a clock. Quantitative SLOs describe populations; none subsumes the others.

## Failure Modes and Misconceptions

- **“Nothing bad happened, so progress is proven.”** Safety does not entail liveness.
- **“The system is busy, so it is live.”** Livelock can consume resources without useful advancement.
- **“No deadlock means no starvation.”** Other operations may complete forever while one waits.
- **“Enabled means eventually scheduled.”** That is a fairness premise.
- **“Weak and strong fairness are interchangeable.”** Intermittent enabledness distinguishes them.
- **“A timeout proves infinite nontermination.”** It proves a deadline miss under one finite execution.
- **“Some operation completes means mine completes.”** Lock-free system progress permits individual starvation.
- **“Wait-free means fast.”** Own-step bounds do not bound scheduling or step duration.
- **“Using atomics makes code lock-free.”** The whole operation and retry protocol determine progress.
- **“Cancellation fixes liveness.”** Unrestricted cancellation can make a service obligation vacuous.
- **“Average latency proves every request progresses.”** Aggregates can hide permanent outliers.
- **“A passing bounded checker proves liveness.”** It covers only modeled states, fairness, and bounds.

## Worked Examples

### Example 1

**Question:** Is mutual exclusion safety or liveness?

**Reasoning:** Two simultaneous owners create a finite bad prefix that no extension repairs. Predicate (owners <= 1) can be inductive.

**Conclusion:** Mutual exclusion is safety.

### Example 2

**Question:** Is every accepted request eventually answered safety?

**Reasoning:** Any finite silence could be extended by an answer. A violating behavior requires infinite outstanding execution, often represented by a fair cycle.

**Conclusion:** Eventual response is liveness.

### Example 3

**Question:** What does a five-second response requirement add?

**Reasoning:** At five seconds without response, a finite deadline violation exists. Eventual response may still occur later, while the bounded property is already false.

**Conclusion:** Deadlines create quantitative finite obligations distinct from pure liveness.

### Example 4

**Question:** Why does “some dequeue always completes” not prevent starvation?

**Reasoning:** New high-priority items may complete indefinitely while one low-priority item remains. Global completion satisfies a lock-free-like property but not per-item response.

**Conclusion:** Name the beneficiary of progress.

### Example 5

**Question:** An action is enabled every other step but never chosen. Does weak fairness exclude this?

**Reasoning:** No; it is never continuously enabled from some point. Strong fairness excludes infinite re-enablement without eventual execution.

**Conclusion:** Intermittent enabledness separates fairness notions.

### Example 6

**Question:** A lock holder is descheduled forever. Is a correct mutex enough for entry liveness?

**Reasoning:** Mutual exclusion can still hold. Waiters depend on holder scheduling or robust recovery. That scheduler premise is external to the mutex safety proof.

**Conclusion:** Blocking progress exposes owner and scheduler dependencies.

### Example 7

**Question:** Does lock-free compare-and-swap guarantee one chosen caller finishes?

**Reasoning:** Repeated caller failure implies another conflicting operation may keep succeeding, so system progress continues while the chosen caller starves.

**Conclusion:** Lock-freedom is not per-operation wait-freedom.

### Example 8

**Question:** Why are fourteen incomplete finite prefixes in the executable model not liveness failures?

**Reasoning:** Each prefix can extend with selections completing both clients. No infinite unfair cycle was established, and no deadline was specified.

**Conclusion:** Finite incompletion is not pure-liveness refutation.

### Example 9

**Question:** Can immediate cancellation satisfy “every request completes or cancels”?

**Reasoning:** Literally yes, making the property weak. Add conditions stating when cancellation is admissible and what service must occur while prerequisites hold.

**Conclusion:** Prevent vacuous progress specifications.

### Example 10

**Question:** A railway controller proves collision freedom and eventual route grant under strong fairness. Is deployment justified?

**Reasoning:** Collision safety is valuable. Route liveness depends on whether strong fairness matches interlocking, scheduler, sensor, failure, and operating policy. Named railway safety, operations, systems, software, formal-methods, security, and regulatory reviewers must validate refinement and assumptions.

**Conclusion:** A theorem with unrealistic fairness does not authorize high-consequence use.

## Cross-Program Connections

- [Interleavings and State-Space Explosion](003-interleavings-and-state-space-explosion.md) supplies reachability and cycle evidence.
- The [CONPAR roadmap](../ROADMAP.md) applies these distinctions to races, deadlock, starvation, critical sections, atomics, lock-free algorithms, and testing.
- [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) supplies transition and observable-behavior foundations.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) adds failure, delivery, and distributed fairness assumptions.
- [Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) connects eventual properties to SLOs, alerts, and incident response.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) distinguishes safety invariants from availability and denial-of-service progress.

## References

1. Leslie Lamport, “Proving the Correctness of Multiprocess Programs,” *IEEE Transactions on Software Engineering* SE-3(2), 1977, [Microsoft Research record](https://www.microsoft.com/en-us/research/publication/proving-correctness-multiprocess-programs/).
2. Bowen Alpern and Fred B. Schneider, “Defining Liveness,” *Information Processing Letters* 21(4), 1985, [DOI](https://doi.org/10.1016/0020-0190(85)90056-0).
3. Leslie Lamport, “Proving Liveness Properties of Concurrent Programs,” *ACM TOPLAS* 4(3), 1982, [author-hosted paper](https://lamport.org/pubs/liveness.pdf).
4. Susan Owicki and Leslie Lamport, “Proving Liveness Properties of Concurrent Programs,” *ACM TOPLAS* 4(3), 1982.
5. Leslie Lamport, *A Science of Concurrent Programs*, Cambridge University Press, 2026, [official author page and errata](https://lamport.azurewebsites.net/tla/science-book.html).
6. Maurice Herlihy, Nir Shavit, Victor Luchangco, and Michael Spear, *The Art of Multiprocessor Programming*, 2nd ed., Morgan Kaufmann, 2020, [publisher record](https://shop.elsevier.com/books/the-art-of-multiprocessor-programming/herlihy/978-0-12-415950-1).
7. Nancy A. Lynch, *Distributed Algorithms*, Morgan Kaufmann, 1996.
8. Zohar Manna and Amir Pnueli, *The Temporal Logic of Reactive and Concurrent Systems: Specification*, Springer, 1992.
9. Edsger W. Dijkstra, *A Discipline of Programming*, Prentice Hall, 1976.
10. Leslie Lamport, “Safety, Liveness, and Fairness,” 2026, [author-hosted technical note](https://lamport.org/tla/safety-liveness.pdf).

## Exercises

### Exercise 1

Classify mutual exclusion, eventual grant, grant within 100 steps, and 99.9th-percentile grant latency under 50 ms. Explain the evidence each needs.

### Exercise 2

For a two-client lock, define an invariant proving safety and a ranking/fairness outline for starvation freedom.

### Exercise 3

Design a liveness monitor for “every accepted queue item eventually completes or receives an admissible terminal rejection.” Include correlation, cancellation, and cycle state.

### Exercise 4

Compare deadlock freedom, lock-freedom, and wait-freedom for a concurrent queue under a descheduled participant and continual interference.

### Exercise 5

A clinical alarm processor has no duplicate alarms in model checking and meets aggregate latency in load tests. Design the remaining safety, per-alarm progress, deadline, fairness, failure, monitoring, and human-review evidence.

## Answers to the Exercises

### Answer 1

Mutual exclusion is safety and needs invariant proof plus finite bad-prefix tests. Eventual grant is liveness and needs infinite-behavior reasoning, fairness premises, accepting-cycle search, or a well-founded proof. Grant within 100 steps is bounded response, refutable by a 100-step finite trace and checkable within a complete finite model. A percentile latency target is statistical and needs representative workload, environment, measurement method, population, confidence, and tail analysis. None of these four results establishes the other three.

### Answer 2

Use invariant: owner is none, A, or B; a client is critical exactly when it is owner; at most one client is critical. Prove initialization and preservation for request, acquire, release, cancellation, and failure recovery. For starvation freedom, use a FIFO ticket or queue position as rank for an outstanding client. Show earlier entries eventually release or cancel, no later entry overtakes, and weak fairness schedules the continuously enabled head acquisition. If a head owner may crash forever, add recovery or weaken the claim. An unfair scheduler invalidates the liveness conclusion without affecting mutual exclusion.

### Answer 3

Track each accepted item by stable identity and status: outstanding, completed, or terminally rejected with an allowed reason. Record whether cancellation is authorized and whether external effect committed. Safety rejects duplicate terminal outcomes, completion after incompatible cancellation, or item loss. Liveness marks an accepting bad condition when an eligible item remains outstanding through a cycle without terminal outcome. Include queue position, worker ownership, retry state, virtual time for deadlines, and fairness actions. Bound checks must report item/worker/fault/depth limits and cannot prove unbounded service.

### Answer 4

Deadlock freedom excludes a global state where unfinished operations have no possible progress, but permits livelock and starvation. Lock-freedom ensures system-wide completion under continuing relevant steps despite a delayed participant, so another operation can finish; one caller may retry forever. Wait-freedom gives every operation a finite own-step completion bound despite interference, though a descheduled thread gets no own steps and wall-clock completion is not implied. Correct classification requires exact algorithm, atomic primitives, memory model, allocation, reclamation, and failure assumptions.

### Answer 5

Retain duplicate-alarm safety evidence, then specify per-alarm correlation, acceptance, severity, required deadline, terminal outcomes, escalation, cancellation rules, and no-loss/no-suppression invariants. Prove or check queue ownership, retries, deduplication, failover, recovery, clock behavior, capacity, backpressure, and alarm-delivery acknowledgment. Analyze starvation under priority, fairness of worker and delivery actions, permanent dependency failure, and overload. Monitor oldest outstanding alarm and individual deadline misses rather than aggregates alone. Named clinical-safety, human-factors, systems, software, reliability, security, operations, privacy, quality, and regulatory authorities must review model fidelity and residual risk. No external review is claimed here.
