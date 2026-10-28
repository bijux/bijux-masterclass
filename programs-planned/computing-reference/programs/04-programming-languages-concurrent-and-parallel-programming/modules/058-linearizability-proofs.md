---
module_id: CONPAR-058
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 58
title: Linearizability Proofs
status: complete
last_verified: 2026-08-29
---

# Linearizability Proofs

## One-Page Review

### Governing question

How can a concurrent implementation be proved observationally equivalent to a legal sequential object while respecting each operation's invocation-response interval and every nonoverlap real-time constraint?

### Essential definitions

- A **history** is a sequence of invocation and response events labeled by operation and process/client.
- An operation is **completed** when its matching response occurs and **pending** when invoked without a response.
- The **real-time order** `a <_H b` holds when response(a) precedes invocation(b) in history H; overlapping operations are not ordered by this relation.
- A **sequential specification** defines legal operation/result transitions on abstract states.
- A **completion** extends a history with responses for some pending invocations and discards the remaining pending invocations.
- A **linearization** is a legal sequential history equivalent per process to a completion of H and extending `<_H`.
- A **linearization point** is a proof witness—an instant between invocation and response assigned to an operation—not necessarily a source statement executed by that caller.
- A **representation invariant** relates concrete shared state to valid structure; an **abstraction relation** relates concrete states/histories to abstract object states.
- **helping** occurs when one operation/thread performs the event that commits another operation.
- **strong linearizability** additionally requires a prefix-preserving linearization function; ordinary linearizability does not automatically preserve adversarial/probabilistic reasoning.

### Central model, mechanism, or theorem

To prove linearizability, define the abstract sequential machine first. For every implementation history, construct a legal sequential history containing the same completed operations and any chosen completed pending operations, preserve each participant's operation order, and preserve nonoverlap real-time order. A common proof identifies a commitment event for each operation, proves that ordering those events yields legal abstract transitions, and proves every witness lies inside its operation interval. Fixed syntactic points are convenient but not required: helping, elimination, and future-dependent algorithms may need simulation, logical points, or prophecy/backward reasoning.

### Critical invariants

Every operation has at most one invocation, response, abstract effect, and returned result. Linearization lies after invocation and before response. Failed CAS and pure helping steps make no abstract change unless explicitly specified. Empty/not-found results linearize at a validated observation consistent with the abstract state. Successful updates preserve representation invariants and map to exactly one legal sequential transition. Real-time precedence is never reversed; overlap may be ordered only when results and specification permit it. Reclamation makes every proof read well-defined. Composition uses disjoint object histories and compatible client semantics. Testing never upgrades sampled histories into a universal theorem.

### Common failures

Proofs choose a point outside an operation interval; order by response time; ignore process order; omit empty, failure, timeout, or pending calls; call the first atomic instruction the point without deriving its abstract effect; treat failed CAS as commitment; place enqueue at advisory tail movement instead of link publication; forget helping; assume a point must be known online; prove representation safety but not returned values; use linearizability to claim fairness or durability; ignore use-after-free; accept a history after silently dropping completed operations; or present a checker pass as proof for all executions.

### Compact example

Enqueue A and enqueue B overlap. A dequeue returning A also overlaps both. Legal order can be `enq(A), enq(B), deq→A` or `enq(A), deq→A, enq(B)`, provided intervals permit both. A later nonoverlapping dequeue returning B must appear after all operations whose responses preceded its invocation. The history does not reveal one unique “true” order; a proof needs at least one legal order preserving real time.

### Connections

[Safety, Liveness, and Progress](004-safety-liveness-and-progress.md) separates this safety property from termination. [Lock-Free Queues](053-lock-free-queues.md) supplies link/help/head cases. [Read-Copy-Update as a Nonblocking Pattern](057-read-copy-update-as-a-nonblocking-pattern.md) shows that safe old-version lifetime does not itself imply linearizable multi-object reads. The next modules address contention policy and whether lock-free complexity is justified.

## Governing Question

How should an engineer turn an informal claim that operations “appear atomic” into a reviewable proof covering histories, return values, real-time precedence, pending operations, helping, memory models, and implementation lifecycle?

Linearizability is a refinement property. It connects concrete concurrent observations to a sequential specification; it is not a synonym for thread safety, atomic instructions, or successful stress tests.

## Why This Matters

Concurrent executions expose intermediate states and overlap. A queue may have a linked node while its tail pointer lags. A stack pop may retry after another thread changes the head. A read may overlap an update and legitimately return an old value. Application code should not need to reason about these mechanisms each time it calls the object.

Linearizability provides a local illusion: each operation takes effect once within its call interval, and nonoverlapping calls respect wall-clock precedence. The sequential specification then determines allowed results. This supports modular reasoning and is stronger than sequential consistency's freedom to reorder nonoverlapping operations.

The property remains limited. It says nothing by itself about completion, fairness, latency, memory reclamation, crash durability, cross-object transactions, or whether a stale but legal result is acceptable policy. A proof can be mathematically valid under sequential consistency and irrelevant to unsafe weak-memory source code. State every layer.

## Prerequisites and Retrieval

Retrieve:

- state-machine traces from [Interleavings and State-Space Explosion](003-interleavings-and-state-space-explosion.md);
- safety/progress separation from [Safety, Liveness, and Progress](004-safety-liveness-and-progress.md);
- atomic event semantics from [Atomic Read-Modify-Write Operations](025-atomic-read-modify-write-operations.md);
- CAS retry discipline from [Compare-and-Swap Loops](026-compare-and-swap-loops.md);
- weak-memory qualification from [Reasoning About a Weak-Memory Program](030-reasoning-about-a-weak-memory-program.md);
- helping/progress from [Obstruction-Free, Lock-Free, and Wait-Free Progress](051-obstruction-free-lock-free-and-wait-free-progress.md); and
- reclamation obligations from [Hazard Pointers](055-hazard-pointers.md) and [Epoch-Based Reclamation](056-epoch-based-reclamation.md).

Retrieval prompt: draw invocation and response intervals for two overlapping enqueues and one dequeue; list all orders allowed by real time, then remove orders rejected by FIFO return values.

## Learning Objectives

After completing this module, a learner can:

1. formalize histories, completions, process equivalence, and real-time order;
2. write a deterministic sequential specification including failure/empty results;
3. construct or reject candidate linearizations by constraint search;
4. prove fixed linearization points using representation and abstraction invariants;
5. handle failed CAS, read-only operations, validation, retries, and helping;
6. recognize future-dependent points and choose simulation/prophecy techniques;
7. apply locality/compositionality without inventing cross-object atomicity;
8. separate linearizability from progress, weak-memory safety, reclamation, and durability;
9. design history capture, checking, model, and source-level evidence; and
10. scope high-stakes correctness claims to human-reviewed specifications.

## Core Exposition

### Begin with the sequential object

A proof is relative to a specification. For a FIFO queue, abstract state is sequence Q. `enqueue(v)` changes Q to `Q·v` and returns success. `dequeue()` on `v·R` returns v and changes state to R; on empty sequence it returns empty without change. A bounded queue adds full/failure or blocking semantics. Close, timeout, and cancellation add distinct transitions.

Do not derive the specification from whatever the implementation happens to do. Decide duplicate handling, capacity, failure, and lifecycle at the abstract level. Nondeterminism is allowed when intentional, but vague results make almost any trace appear legal.

The sequential transition function is the checker and proof oracle. Each chosen operation/result pair must be enabled in the current abstract state and produce the next state. Returned values constrain order: a FIFO dequeue returning A cannot be placed before enqueue A or behind an earlier unmatched B.

### Histories and intervals

Represent invocation `inv_i(op,args)` and response `ret_i(result)` for operation identifier i. Well-formed per-process histories alternate appropriately or otherwise follow the declared client model. Operation interval begins at invocation and ends at response.

If response(a) occurs before invocation(b), then a must precede b in every linearization. If intervals overlap, real time imposes no order, even if one response happens first. Results and the sequential specification can still force an order. Ordering all operations by invocation or response is therefore generally wrong.

Pending calls require care. The standard definition may extend the history with responses for some pending invocations and discard the rest before comparing completed operations. A completed operation cannot be silently dropped. A pending operation whose effect another completed operation observes may need completion in the witness.

### Constructing a witness

For a finite history, form a precedence graph. Add edges for real-time order and per-client program order where not already implied. Search topological orders. Simulate each candidate against the sequential specification using the recorded results; prune when an operation is illegal. One legal order is a witness. Exhausting every candidate establishes non-linearizability for that finite history, assuming faithful capture and correct specification/checker.

Several linearizations may exist. The property is existential per history. A proof does not need to recover a metaphysically unique order. It must construct consistently legal witnesses for all possible implementation histories.

History checking can be computationally expensive, and incomplete calls, multi-key operations, clock skew, dropped events, duplicated IDs, and observer instrumentation complicate practice. Partitioning by independent keys can help only when operations truly commute/decompose.

### Fixed-point proof recipe

Many CAS structures admit a direct proof:

1. define concrete representation invariant I;
2. define abstract state and abstraction relation A;
3. classify every atomic implementation step;
4. designate one step per completed abstract operation as its linearization point;
5. prove non-point steps preserve the abstract state;
6. prove each point performs the declared legal abstract transition and determines the response;
7. prove the point lies inside the operation interval; and
8. show the points' order preserves real-time precedence.

For a Treiber push, successful head CAS publishes one new top and can linearize push. Failed CAS changes nothing and refreshes. A successful pop head CAS removes one top; an empty pop linearizes at a validated null observation. Safe reclamation is a premise because a proof cannot interpret an invalid dereference as a concrete state.

### Queues and helping

In the Michael-Scott queue, successful CAS that links a new node at the unique null `next` makes its payload part of abstract FIFO order. Advancing advisory tail changes representation only. A helper can advance tail for the enqueuer; the enqueuer's later tail CAS can fail after the enqueue already linearized.

Nonempty dequeue linearizes when head advances to the successor. Empty dequeue requires a validated state: head equals tail and head.next is null. Head equals tail with non-null next means tail lag, not empty. Each case maps to a different proof branch.

Helping means the thread executing a commitment event and the operation receiving the abstract effect can differ. Index proof obligations by operation descriptor/identity, not current thread. Ensure exactly one helper wins the effect and all observers agree on its result.

### Reads and validation

A read-only operation often linearizes at an atomic load or at the last validation that makes a set of prior reads coherent. A `contains` traversal may linearize at discovering an unmarked matching node or at validation showing absence. The chosen point must explain the returned value in the abstract state at that instant.

If a read collects multiple independent fields without a snapshot protocol, there may be no instant at which the combined result existed. Safe atomic field loads do not imply a linearizable aggregate. Use one immutable root, version/seqlock validation, a lock, or weaken the specification explicitly.

Empty and negative responses deserve first-class proof. “Not found” can be harder than success because it asserts absence across a search domain. Identify the observation/validation that rules out a concurrent insertion in the claimed interval.

### Future-dependent linearization

Some algorithms cannot assign every operation a fixed point from its local prefix. In elimination stacks, overlapping push and pop may pair without touching the central stack. In Herlihy-Wing-style queues, the order associated with reservations and later fills can depend on future dequeues. A proof that prematurely fixes order can fail even though the algorithm is linearizable.

Use an abstraction relation with multiple possible abstract states, backward simulation, interval-based reasoning, or prophecy variables that record a future choice for proof purposes. These are not runtime predictions. They let the proof relate a concrete prefix to every abstract future consistent with later observations.

Ordinary linearizability chooses a witness for each completed history. Strong linearizability demands prefix preservation: extending a history cannot revise the linearization chosen for its prefix. This matters when adversarial scheduling interacts with randomized clients. Do not claim strong linearizability from an ordinary proof.

### Forward and backward simulation

A forward simulation maps each concrete step to zero or more abstract steps while preserving a relation. It works naturally when the abstract effect is determined as execution proceeds. Stuttering concrete steps—failed CAS, helping-only tail movement, bookkeeping—map to zero abstract transitions.

Backward simulation reasons from later states/results toward an earlier abstract choice and can handle future-dependent commitments. Both require initialization, step correspondence, response matching, and treatment of pending operations. Mechanization adds confidence but still depends on faithful language/memory/reclamation models.

An abstraction function selecting one abstract state per concrete state can be too rigid. An abstraction relation permits several candidates. Pick proof machinery based on the algorithm rather than forcing a convenient point that does not exist.

### Locality and composition

Linearizability is local: if each object subhistory is linearizable to its sequential specification, the combined history can be linearized consistently for disjoint objects under the theorem's conditions. This makes concurrent objects modular.

Locality does not create a cross-object transaction. A transfer using two individually linearizable counters can expose an intermediate state. If the client specification requires atomic transfer, model the pair as one object/operation or add a transaction protocol.

Composition also assumes client-visible invocation/response boundaries and specifications align. Callbacks, reentrancy, nested operations, and external side effects can enlarge the object boundary. Define ownership of those effects before applying locality.

### Memory models and source correctness

An abstract proof often assumes sequentially consistent atomic events and valid non-atomic reads. A source implementation must establish that assumption. Publication ordering, atomic widths, compiler transformations, data-race rules, pointer provenance, and reclamation determine which executions exist.

A linearization point cannot repair undefined behavior. A relaxed implementation may require a weak-memory proof showing its concrete executions refine the abstract model. Conversely, using sequential consistency does not fix a wrong abstract transition or missing empty case.

Separate layers: source-language safety and memory ordering; representation/reclamation invariants; linearizability; progress; resource/lifecycle behavior; durability and external effects. A completion claim needs applicable evidence for each.

### Testing and checking

History checkers can find concrete violations and are valuable regression oracles. Generate adversarial overlaps, record unique invocation/response IDs, arguments, results, and trustworthy per-client order, then run an independent sequential model. Use logical barriers rather than relying only on timestamps; clocks across machines may not establish exact real-time precedence.

A checker pass says one captured finite history has a legal witness. It does not prove all schedules, faithful instrumentation, correct memory ordering, or the checker itself. A checker failure can be an implementation bug, specification mismatch, or capture defect; preserve the minimal witness and raw events.

Model checking explores bounded implementations and can verify all histories within bounds. Deductive proof covers parameterized behavior under assumptions. Stress, sanitizers, weak-memory litmus/model tools, and code review address complementary layers. Use several, not one green badge.

### Lifecycle and external effects

Timeout and cancellation need commitment semantics. If an operation linearized before timeout, returning “no effect” is false; use an indeterminate/committed result, idempotent query, or compensation protocol. If a pending operation is abandoned before commitment, prove helpers cannot later commit it unnoticed.

Crash durability is not implied. A write can linearize in volatile memory and vanish after power loss unless the durability specification adds persistence/replication events. Network clients also need invocation boundaries, duplicate suppression, and response-loss handling.

Shutdown closes admission, resolves or records pending operations, quiesces helpers, drains reclamation, and preserves enough evidence to interpret committed effects. The sequential specification should include close/drain rather than treating teardown as outside history.

## Definitions and Notation

- `H`: a concurrent history of invocation/response events.
- `op_i`: operation instance i with interval `[inv_i, ret_i]` when completed.
- `complete(H)`: completed operation instances in H.
- `pending(H)`: invoked instances without responses.
- `a <_H b`: `ret_a` occurs before `inv_b`.
- `S`: candidate legal sequential history/specification execution.
- `state(S_prefix)`: abstract state after a prefix of S.
- `LP(i)`: proof witness assigned to operation i within its interval.
- `C`: concrete implementation state.
- `A(C,s)`: abstraction relation between concrete C and abstract state s.
- `I(C)`: concrete representation/lifetime invariant.

H is linearizable when some completion H' is process-equivalent to legal sequential S and `<_H` is contained in S's order. “Process-equivalent” preserves each participant's observable operation sequence.

## Mechanisms, Invariants, or Proof Structure

### Direct proof obligations

Initiation establishes I and A for the initial empty/value state. Every concrete step preserves I. Stuttering steps preserve the abstract candidate. Each commitment step changes the abstract state according to exactly one enabled operation/result. Responses match the committed result, points lie within intervals, and commitment order respects `<_H`. Pending operations are either uncommitted and droppable or included with a justified completion.

### Counterexample obligations

To refute linearizability for a finite history, retain all completed operations, permitted completed pending operations, per-client order, and real-time edges; show every topological order violates the sequential transition/result rules. A mere surprising overlap is not enough. The smallest rejected prefix is usually the best diagnostic.

### Executable history checker

The deterministic model enumerates all orders of two overlapping enqueues and a dequeue returning A, followed by a later nonoverlapping dequeue returning B. Exactly two sequential FIFO witnesses satisfy real-time constraints and results. This proves only the stipulated history/model.

<!-- bijux-verify: {"id":"finite-linearization-search","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"linearizations=2\nfirst=enqA,deqA,enqB,deqB\nsecond=enqA,enqB,deqA,deqB\nreal_time_edges=3\n","stderr":""}} -->
```python
operations = {
    "enqA": (0, 4, "enq", "A"),
    "enqB": (1, 5, "enq", "B"),
    "deqA": (2, 6, "deq", "A"),
    "deqB": (7, 8, "deq", "B"),
}
edges = {(a, b) for a, av in operations.items() for b, bv in operations.items() if av[1] < bv[0]}
answers = []

def legal(prefix):
    queue = []
    for name in prefix:
        _, _, kind, value = operations[name]
        if kind == "enq":
            queue.append(value)
        elif not queue or queue.pop(0) != value:
            return False
    return True

def search(prefix, remaining):
    if not remaining:
        answers.append(prefix)
        return
    for name in sorted(remaining):
        if any(after == name and before not in prefix for before, after in edges):
            continue
        proposal = prefix + [name]
        if legal(proposal):
            search(proposal, [item for item in remaining if item != name])

search([], list(operations))
print(f"linearizations={len(answers)}")
print(f"first={','.join(answers[0])}")
print(f"second={','.join(answers[1])}")
print(f"real_time_edges={len(edges)}")
```

### Proof-review ledger

| Case | Required witness |
|---|---|
| successful update | one abstract transition and matching response |
| failed retry | no abstract change; refresh derived state |
| read success | observation/validation explaining returned value |
| empty/not found | instant and invariant establishing absence |
| helping | unique target operation and exact-once commitment |
| pending | justified completion or safe omission |
| cancellation/timeout | relationship to commitment |
| reclamation | every interpreted dereference is valid |

## Alternatives and Trade-Offs

| Proof/evidence approach | Strength | Limitation |
|---|---|---|
| Fixed linearization points | compact, reviewable direct argument | fails for future-dependent algorithms |
| Forward simulation | aligns concrete steps with abstract refinement | may need nondeterministic relation/helping metadata |
| Backward simulation/prophecy | handles future-dependent choices | harder to construct and mechanize |
| Separation/concurrent logic | modular ownership and interference reasoning | tool/logic expertise and model fidelity |
| Bounded model checking | exhaustive within declared bounds | state/data/thread bounds restrict theorem |
| History checking | finds concrete black-box violations | finite traces and capture/specification dependence |
| Stress plus invariants | exercises real implementation/toolchain | sampling cannot prove universal histories |
| Coarse-grained reference implementation | differential oracle and simpler proof | equivalence harness can hide timing/lifecycle gaps |

Prefer the simplest proof adequate for the algorithm. If a mutex design meets requirements, its linearization proof may be dramatically smaller. Nonblocking performance never compensates for an unreviewable correctness argument.

## Failure Modes and Misconceptions

- **“Atomic instruction means linearizable method.”** The instruction must implement the right abstract transition and response.
- **“Response order is linearization order.”** Overlapping calls can linearize in another order.
- **“Overlap means any order.”** Sequential legality and return values still constrain it.
- **“Completed calls may be dropped.”** Only unresolved pending invocations receive completion/omission treatment.
- **“Every point is in the caller.”** Helpers can commit another operation.
- **“The point must be fixed locally.”** Some proofs need future-dependent witnesses.
- **“Representation invariant proves behavior.”** It need not explain operation results/order.
- **“Empty is obvious.”** Negative results need a validated absence instant.
- **“Failed CAS is failure response.”** It normally commits nothing and triggers retry.
- **“Linearizable objects form a transaction.”** Locality gives per-object composition, not multi-object atomicity.
- **“Linearizable means wait-free.”** Safety and progress are orthogonal.
- **“Linearizable means durable.”** Volatile commitment can precede persistence.
- **“SC proof covers relaxed source.”** Language/memory refinement remains.
- **“Checker pass is a proof.”** It covers a captured finite history under one model.
- **“No observed violation means correct.”** Rare schedules and instrumentation gaps remain.

## Worked Examples

### Example 1

**Nonoverlap constraint.**

**Situation.** `push(A)` returns before `pop()` is invoked, and pop returns empty.

**Reasoning.** Real-time order forces push before pop. Sequential stack state then contains A, so empty is illegal absent a specified intervening removal. No overlap freedom can reorder the calls.

**Conclusion.** This two-operation completed history is non-linearizable to the ordinary stack specification.

### Example 2

**Overlapping queue operations.**

**Situation.** Enqueues A/B and dequeue→A overlap as in the executable model.

**Reasoning.** FIFO/results require A before dequeue A. B may appear before or after that dequeue because its interval overlaps. A later dequeue B is real-time-after the earlier completed operations. Two legal witnesses remain.

**Conclusion.** A history may be linearizable without a unique sequential order.

### Example 3

**Failed CAS.**

**Situation.** A stack pop reads A, loses CAS, refreshes to B, then succeeds and returns B.

**Reasoning.** The failed CAS makes no abstract change. The successful CAS removing B linearizes this pop and explains B. Treating the first read/CAS attempt as commitment would return the wrong abstract top.

**Conclusion.** Retry attempts stutter until the one successful abstract transition.

### Example 4

**Empty queue with tail lag.**

**Situation.** Dequeue observes head=tail but `head.next=N`.

**Reasoning.** N was already linked and its enqueue linearized. Tail is only advisory. Returning empty has no legal FIFO witness; dequeue must help/refresh. Empty can linearize only at validated null successor under the queue invariant.

**Conclusion.** Representation knowledge determines valid negative-result witnesses.

### Example 5

**Helping commitment.**

**Situation.** P publishes a descriptor; Q completes its CAS; P later notices completion and returns.

**Reasoning.** Q's CAS can be `LP(P)` because it lies after P invocation and before P response. The descriptor identifies P and records exact result. Q's thread identity is irrelevant; exact-once descriptor transition prevents duplicate abstract effects.

**Conclusion.** Linearization belongs to operation intervals, not executing threads.

### Example 6

**Pending operation observed by completion.**

**Situation.** Enqueue A has no response, but a completed dequeue returns A.

**Reasoning.** The witness cannot simply discard enqueue A because the dequeue result would be illegal. Complete the pending enqueue in the completion, order it before the dequeue at its commitment, and retain the completed dequeue.

**Conclusion.** Pending-effect observation constrains completion choices.

### Example 7

**Multi-register read.**

**Situation.** Reader loads x=0, writer sets x=1 then y=1, reader loads y=1 and returns pair (0,1), while specification allows only atomic pair versions (0,0)/(1,1).

**Reasoning.** Each atomic load is valid, but no allowed abstract version is (0,1). No point in the reader interval explains its return under that specification. Use one snapshot/version protocol or weaken semantics.

**Conclusion.** Component atomicity does not imply aggregate linearizability.

### Example 8

**Per-object composition gap.**

**Situation.** Transfer decrements account X then increments Y using individually linearizable counters; reader sees reduced total between calls.

**Reasoning.** Each counter history is legal. The transfer is two operations, so locality does not make it one atomic event. Model accounts as one transactional object or accept/guard the intermediate state.

**Conclusion.** Object boundary determines what linearizability promises.

### Example 9

**Timeout after commitment.**

**Situation.** Remote increment linearizes, response is delayed, and client times out/retries.

**Reasoning.** Timeout cannot truthfully mean no effect. Retry may double-increment unless operation identity/idempotency resolves the first result. History includes commitment even without observed response; crash/durability is a separate specification.

**Conclusion.** Client failure semantics must align with the linearization interval.

### Example 10

**Radiation-control command register.**

**Situation.** A concurrent command register passes sampled linearizability checking. Can it control therapy dosage?

**Reasoning.** No. Required evidence includes a human-approved sequential safety specification; source/memory/reclamation proof; exhaustive or mechanized refinement for relevant bounds; fault, timeout, duplicate, persistence, and restart semantics; target/toolchain evidence; independent history capture; fail-safe interlocks; and named clinical, controls, formal-methods, hardware/software, security, regulatory, and operations review. Linearizability does not validate dosage or certification.

**Conclusion.** A safety-critical deployment requires a layered safety case beyond a checker pass.

## Cross-Program Connections

- **Programming languages:** contextual refinement explains why clients can replace a proved concurrent object with its sequential specification under assumptions.
- **Algorithms:** representation invariants and commitment events bridge concrete steps to abstract transitions.
- **Formal methods:** simulations, prophecy, separation logic, and model checking address different proof shapes.
- **Distributed systems:** real-time histories underpin linearizable registers, but capture, crashes, and durability enlarge the model.
- **Databases:** serializability orders transactions without necessarily respecting real-time order; strict serializability is the closer analogue.
- **Testing:** history minimization and adversarial schedules turn violations into actionable regressions.
- **Software engineering:** APIs must expose cancellation, close, and failure results represented in the specification.
- **Safety engineering:** the sequential spec itself is a human-owned hazard-control artifact, not an automatically correct oracle.

## References

1. Maurice P. Herlihy and Jeannette M. Wing, “Linearizability: A Correctness Condition for Concurrent Objects,” *ACM TOPLAS* 12(3), 1990. <https://www.cs.cmu.edu/~wing/publications/HerlihyWing90.pdf>
2. Jeannette M. Wing and Chun Gong, “Testing and Verifying Concurrent Objects,” *JPDC* 17(1–2), 1993. <https://www.cs.cmu.edu/~wing/publications/WingGong93.pdf>
3. Nancy A. Lynch, *Distributed Algorithms*, Morgan Kaufmann, 1996, atomic-object chapters. <https://groups.csail.mit.edu/tds/distalgs.html>
4. Maurice Herlihy and Nir Shavit, *The Art of Multiprocessor Programming*, revised first edition, 2012. <https://www.elsevier.com/books/the-art-of-multiprocessor-programming/herlihy/978-0-12-397337-5>
5. Gavin Lowe, “Testing for Linearizability,” *Concurrency and Computation* 29(4), 2017. <https://doi.org/10.1002/cpe.3928>
6. Phillip B. Gibbons and Ephraim Korach, “Testing Shared Memories,” *SIAM Journal on Computing* 26(4), 1997. <https://doi.org/10.1137/S0097539794279614>
7. Ahmed Bouajjani, Michael Emmi, Constantin Enea, and Jad Hamza, “On Reducing Linearizability to State Reachability,” ICALP 2015. <https://doi.org/10.1007/978-3-662-47666-6_7>
8. Ivana Filipović, Peter O'Hearn, Noam Rinetzky, and Hongseok Yang, “Abstraction for Concurrent Objects,” *Theoretical Computer Science* 411(51–52), 2010. <https://doi.org/10.1016/j.tcs.2010.09.021>
9. Hagit Attiya and Constantin Enea, “Putting Strong Linearizability in Context,” DISC 2019. <https://doi.org/10.4230/LIPIcs.DISC.2019.2>
10. Anish Athalye, “Porcupine: A Fast Linearizability Checker in Go,” current project documentation; retrieved 2026-08-29. <https://github.com/anishathalye/porcupine>

## Exercises

### Exercise 1

Define real-time order and explain why response order alone cannot determine a linearization of overlapping operations.

### Exercise 2

For a stack, trace overlapping `push(A)`, `push(B)`, and `pop→A`. Enumerate the legal sequential orders, then add a later nonoverlapping `pop→B` and update constraints.

### Exercise 3

Audit a queue proof that assigns enqueue linearization to tail CAS, treats `head==tail` as empty, and omits failed CAS. Repair the proof cases.

### Exercise 4

Design an evidence strategy for an algorithm with helping and a future-dependent linearization order. Compare fixed points, forward/backward simulation, model checking, and history checking.

### Exercise 5

A distributed medication-inventory service claims linearizable decrement operations but loses acknowledged state on power failure and retries timed-out requests without IDs. Specify the expanded proof and human review required.

## Answers to the Exercises

### Answer 1

`a <_H b` when a's response precedes b's invocation; every linearization must place a before b. Overlapping intervals have no real-time edge even when one response is earlier, because either operation could have taken effect inside the overlap. Sequential legality and results may constrain them, but sorting by response time invents a restriction absent from linearizability and can reject legal histories.

### Answer 2

To return A, push A precedes pop A. Push B may precede push A only if pop A would then violate LIFO, so legal orders are `push(A), pop→A, push(B)` and, if intervals allow, `push(A), push(B), pop→A` is not legal because pop would return B. With later pop→B invoked after all three responses, real time places it last. Thus the sole complete four-operation witness is `push(A), pop→A, push(B), pop→B`. If push B's interval/order differs, recompute edges rather than assuming invocation order.

### Answer 3

Enqueue linearizes at the successful CAS linking its node into the unique null `next`; tail advancement is advisory helping and has no abstract effect. `head==tail` with non-null successor is tail lag, so dequeue helps/retries; empty requires validated null successor. Failed link/head/tail CAS commits nothing and refreshes all derived state. Nonempty dequeue linearizes at successful head advancement, with protected payload/lifetime. Prove representation preservation, FIFO link order, returned value, each point inside its operation interval, and exact effect under helpers.

### Answer 4

Use operation descriptors to identify invocation, helpers, one winning commitment, and response. Attempt a relational forward simulation that maps stuttering/help steps and abstract commits; if abstract order cannot be determined from a prefix, do not invent fixed points. Use backward simulation, prophecy, or an established logic to relate later results to earlier choices, ideally mechanized. Bounded model checking explores all schedules/data within declared limits and targets helping races. Independent history checking exercises the implementation and minimizes concrete violations. Stress, weak-memory, and reclamation evidence cover source layers. None alone proves unbounded correctness; together they provide complementary evidence tied to one sequential spec.

### Answer 5

The volatile decrement may linearize yet fail the required durable specification; an acknowledgment needs a named persistence/replication point and recovery invariant. Timed-out outcomes are indeterminate unless a durable operation ID supports exactly-once effect/query; blind retry can double-decrement. Specify inventory bounds, authorization, idempotency, crash histories, response-loss, cancellation, compensation, failover, audit, and cross-item transaction scope. Verify concurrent refinement plus durable state-machine/recovery behavior, fault injection, power-loss tests, history capture, and operational reconciliation. Named pharmacy/clinical-safety, distributed-systems, storage, formal-methods, security, operations, and regulatory reviewers must approve the specification, hazards, evidence, and residual risk. Linearizability alone is insufficient.
