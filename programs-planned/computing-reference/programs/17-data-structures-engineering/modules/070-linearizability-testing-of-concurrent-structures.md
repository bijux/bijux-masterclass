---
module_id: DSE-070
program: Data Structures Engineering
level: 2
module_number: 70
title: Linearizability Testing of Concurrent Structures
status: complete
last_verified: 2026-08-30
---

# Linearizability Testing of Concurrent Structures

## One-Page Review

### Governing question

How can engineers record, decide, minimize, and interpret linearizability of observed concurrent histories without letting instrumentation errors, incomplete specifications, search timeouts, or sampled schedules masquerade as correctness evidence?

### Essential definitions

- A **history** is a sequence of operation invocation and response events, including process/thread identity, object, method, arguments, result or exception, and event order.
- An operation is **completed** when invocation has a matching response; otherwise it is **pending**.
- Operation A **precedes in real time** operation B when A's response occurs before B's invocation.
- Operations **overlap** when neither precedes the other and may be ordered either way if the sequential specification permits.
- A **sequential specification** is an executable or mathematical state machine defining legal operation results and next states.
- A **linearization** is a legal sequential ordering of completed/chosen pending operations that preserves real-time precedence.
- A **checker** searches for such an ordering; a negative result is a counterexample only if history and specification are faithful and the decision completed.
- **state-space explosion** is combinatorial growth in candidate orderings/specification states.
- **memoization/pruning** avoids revisiting equivalent search states; **P-compositionality** partitions a history when the specification permits independent checking.
- A **witness** is one legal linearization; a **minimal counterexample** is a reduced still-invalid history.

### Central model, mechanism, or theorem

For each completed operation `o`, build predecessor set `Pred(o)` containing every operation whose response occurred before `o`'s invocation (plus per-process order already implied by well-formed histories). Begin from the sequential specification's initial state. Repeatedly choose an unplaced operation whose predecessors are placed; apply its method to the current spec state and require the recorded result/exception to match. Backtrack on mismatch. The history is linearizable iff some branch places all required operations legally.

This decision concerns one recorded history and one specification. It does not prove the implementation linearizable for unobserved schedules, inputs, memory models, failures, or environments. A completed exhaustive search can refute a history; a timeout or resource limit is **unknown**, not failure or pass. History capture must not omit, duplicate, reorder, or fabricate effects. Pending operations must be handled according to the formal completion rule rather than silently discarded whenever inconvenient.

### Critical invariants

1. Every invocation/response pair has a unique operation and participant identity.
2. Per-participant event order and response-before-invocation real-time order are preserved.
3. Arguments, results, exceptions, timeouts, and cancellation outcomes reflect the actual API boundary.
4. The sequential specification is independent, deterministic where assumed, and matches documented semantics.
5. Candidate operations are applied only after all real-time predecessors.
6. Spec state is copied/restored exactly across backtracking; failed branches cannot leak mutations.
7. Pending, duplicate/retried, and externally committed operations follow an explicit completion policy.
8. Checker outcomes distinguish linearizable, not linearizable, unknown/timeout, malformed, and unsupported.
9. Decomposition/pruning preserves satisfiability under proved independence/equivalence.
10. Test generation covers adversarial operations, keys, boundaries, contention, failures, and target memory/runtime conditions.

### Common failures

- Sorting operations only by invocation or response time.
- Demanding response order be sequential order for overlapping calls.
- Using the implementation itself as the sequential oracle.
- Omitting exceptions, empty results, capacity failures, or cancellation.
- Treating wall-clock timestamps from unsynchronized machines as a total order.
- Dropping pending operations that may have taken effect.
- Treating checker timeout as “not linearizable” or, worse, a pass.
- Partitioning by key when operations such as size, clear, range, or capacity couple keys.
- Replaying a minimized history without preserving its concurrency constraints.
- Claiming repeated passing histories prove universal correctness.

### Compact example

Register starts at 0. W1 writes 1 over interval `[0,5]`; W2 writes 2 over `[1,2]`; R reads 2 over `[3,4]`. W2 must precede R, but W1 overlaps both. Ordering `W1,W2,R` is legal, so the history is linearizable even though W1 responds last. Conversely, completed W1 `[0,1]` followed by R `[2,3]` returning 0 is invalid: real time requires W1 before R, so no legal sequential register returns 0.

### Connections

[DSE-062](062-fine-grained-locking.md) through [DSE-069](069-read-copy-update-structures.md) provide points, helping, ABA, reclamation, and weak-iteration cases. [DSE-017](017-queues.md) supplies a sequential FIFO oracle. The [program roadmap](../ROADMAP.md) next moves into external-memory structures, whose concurrent implementations retain these evidence obligations.

## Governing Question

What trustworthy pipeline—from operation contract and history capture through complete decision, counterexample reduction, schedule generation, and independent proof—can determine whether an observed concurrent structure behaves like its sequential abstraction in real time?

## Why This Matters

Concurrent data-structure bugs often produce plausible final states. Two dequeues may return the same item while the final queue looks empty. A map `put` may disappear only when resize overlaps removal. A lock-free stack can preserve element count while violating LIFO. Final-state assertions and race detectors address different properties; neither asks whether every completed call could have taken effect atomically between invocation and response.

Linearizability testing asks that question for observed histories. It is powerful because the checker need not know an implementation's internal linearization points. It needs an externally recorded history and a sequential specification. When no legal ordering exists, the history is a concrete semantic counterexample that can guide schedule reconstruction and proof repair.

The method also has hard limits. Search is exponential in overlapping operations. Instrumentation can perturb schedules or record events at the wrong boundary. A sequential oracle can encode the same bug or omit capacity/exception semantics. Distributed clocks cannot be treated as a trustworthy total order without assumptions. A pass covers only histories actually generated and fully checked. Wing and Gong explicitly frame testing and verification as complementary: tests find exercised failures and validate assumptions; proof/model verification addresses universal claims within a model.

Production-grade use therefore treats the checker as one evidence layer. It gives precise outcomes, preserves raw histories, minimizes failures, validates the harness, and reports unknowns. It combines deterministic schedule tests, random/adversarial stress, memory-model tools, invariants, and proof review.

## Prerequisites and Retrieval

Retrieve sequential state machines, invocation/response events, partial orders, depth-first search, backtracking, memoization, property-based testing, linearization points, and concurrency progress. From [DSE-065](065-lock-free-stack-structure-and-invariants.md) and [DSE-066](066-michael-scott-queues.md), retrieve operation-specific points and pending helping. From [DSE-068](068-hazard-pointers-and-epoch-reclamation.md), retrieve failures that may be memory-safe or unsafe independent of abstract history. From [DSE-069](069-read-copy-update-structures.md), retrieve weak traversal that may intentionally not satisfy a snapshot specification.

The executable artifact below decides two small complete single-object register histories. It is pedagogical search code, not a scalable production checker or a test of runtime threads.

## Learning Objectives

After completing this module, you can:

1. formalize a well-formed concurrent history and real-time precedence;
2. implement a small sequential state-machine oracle;
3. derive a backtracking linearizability decision procedure;
4. handle overlapping, pending, exceptional, cancelled, and retried calls;
5. distinguish valid, invalid, unknown, malformed, and unsupported outcomes;
6. apply sound memoization, locality, and P-compositionality conditions;
7. design faithful low-perturbation instrumentation;
8. minimize and replay counterexamples without erasing causality;
9. generate high-value schedules, inputs, faults, and memory conditions; and
10. combine sampled checking with model checking, sanitizers, and proof.

## Core Exposition

**Specify the object first.** A checker needs a sequential model independent of concurrency. For a register with state `v`, `write(x)` returns its documented acknowledgment and sets `v=x`; `read()` returns v unchanged. For a stack, push prepends and pop removes/returns head or empty. For a bounded queue, enqueue can fail/full and dequeue can return empty; capacity and close are part of state. Exceptions and null policy are observable behavior, not harness noise.

The model should be simpler than the implementation and use different code paths. Reusing the same concurrent algorithm under one thread can reproduce semantic bugs. Validate the oracle against hand-written sequential cases and, where possible, a second mathematical/reference model.

**Record events at the API boundary.** For each call, emit an invocation before entering the object and a response after the implementation returns/throws. Record unique operation ID, participant ID, object/key domain, method, normalized arguments, normalized result/exception, and a monotonic event sequence assigned by a trustworthy recorder. Avoid invoking `toString`, equality, logging callbacks, or mutable argument inspection inside the critical timing path if they can change behavior.

Copy mutable inputs/outputs at the defined boundary so later mutation does not rewrite history. Redact secrets without collapsing distinct values needed by the model. Ensure logging buffers do not drop events; backpressure/drop must make the history invalid/unknown rather than invisible. Crashes require durable or externally captured events if effects before failure matter.

**Construct the partial order.** For completed operations A and B in one history, if `response(A)` occurs before `invocation(B)`, every linearization must order A before B. If intervals overlap, either order may be legal regardless of invocation or response order. Per-process well-formedness normally means a process does not invoke its next operation before the previous response; asynchronous clients may have multiple logical process IDs.

Do not invent ordering from nanosecond values alone. In one process, an atomic event-sequence recorder can establish event order, though it perturbs execution. Across machines, synchronized clocks have uncertainty; only causal/client session order and provable nonoverlap should constrain the history. Linearizability for distributed services also needs a clear operation boundary and completion semantics.

**Search legal sequentializations.** Start with sequential state `s_0`, empty placed set, and all completed operations. At each step choose any remaining operation whose real-time predecessors are already placed. Apply its input to a copy of current spec state. If modeled result matches recorded result, recurse with the next state. If not, prune. Success places all operations; exhaustion proves no legal order for this finite history/spec.

The branch choice represents a candidate linearization point within each operation interval. Explicit times are not assigned; respecting precedence guarantees a topological ordering can choose points for the finite history under the standard model. Operation-specific internal points may help debugging but are not required for black-box checking.

**Handle pending operations formally.** A history may end after invocation without response. In the formal definition, one may extend the history by completing some pending invocations and discard remaining pending invocations, then check the completed projection. A pending write could already have taken effect and influence later completed reads; dropping it unconditionally can create false violations. Conversely, assuming every pending operation took effect can create false passes.

A checker can explore: omit a pending operation, or assign a permitted result/effect consistent with the spec and place it before the end, subject to its invocation and observed later effects. The allowed completion domain must be finite or symbolically represented. For APIs with external side effects, timeouts/retries, exactly-once tokens, or cancellation, specify whether the operation can commit after client timeout and how duplicate IDs behave.

**Normalize results exactly.** Equality must follow the contract. A map returning two different object identities with equal values may or may not be equivalent. Floating-point NaN, signed zero, unordered collections, iterators, exceptions, and partial/bulk results need canonical comparison. If the API permits nondeterministic sequential results, the oracle returns a set/relation of allowed outcomes, expanding search; a deterministic checker cannot silently choose one.

**Distinguish malformed and unsupported.** Unmatched response, duplicate operation ID, overlapping calls attributed to a sequential participant, missing argument, corrupted event order, or dropped logs should yield malformed. An unmodeled method or result should yield unsupported. Resource exhaustion should yield unknown. Only completed exhaustive search yields linearizable/not-linearizable for the supplied interpretation.

This outcome taxonomy belongs in reports:

- `linearizable` with witness and checker/version/spec digest;
- `not_linearizable` with counterexample and completed search evidence;
- `unknown_timeout` or `unknown_resource_limit`;
- `malformed_history`;
- `unsupported_operation/specification`.

**Control state explosion soundly.** With `n` mutually overlapping operations, candidate orders can approach `n!`, though result mismatches and precedence prune many. Memoize equivalent nodes `(remaining/history frontier, canonical spec state)`; reaching the same node again need not repeat search. Canonicalization must preserve all spec distinctions—hash collision cannot be treated as state equality without confirmation.

Linearizability is local across independent objects: a system history is linearizable iff each object subhistory is linearizable under the standard assumptions. P-compositionality partitions operations within one type using a property such as independent keys, but only if the specification decomposes. Per-key map get/put/remove can often partition; `size`, `clear`, range queries, capacity, global ordering, resize-visible behavior, and multi-key operations couple partitions.

Windowing long histories is dangerous. A violation can span the boundary, and the initial state of a later window may be unknown. Use overlap/context summaries or formally justified incremental methods. Sampling only “busy” intervals can miss empty/full/close boundaries.

**Minimize failures causally.** Given an invalid history, delta-debug by removing operations and rechecking until no further allowed reduction preserves invalidity. Preserve invocation/response pairs, participant well-formedness, real-time constraints, initial state, and required pending effects. Minimize arguments/keys separately when the model permits. Store both raw and minimized histories; minimization can make a bug legible but may remove the scheduling pressure needed to reproduce the implementation failure.

A checker witness/counterexample is not automatically a concrete thread schedule. Multiple event timings can induce the same partial order, and instrumentation changed timing. Add schedule hooks at algorithmically relevant points—load, validate, CAS, lock, mark, resize, reclaim—and write a deterministic regression reproducing the causal order.

**Generate adversarial histories.** Uniform random operations often spend too little time at dangerous boundaries. Bias toward empty/singleton/full, same-key hash collisions, resize thresholds, duplicate values, equal priorities, min/max counters, close/cancel, allocation failure, stalled participants, ABA reuse, and reclamation. Vary thread count, operation count, CPU placement, preemption, backoff, payload sizes, and read/write mix.

Use short histories frequently because checkers decide them completely and minimize easily. Mix with longer partitionable histories. Seed and record the generator, workload, toolchain, platform, implementation commit, and scheduler/fault configuration. Re-run known bad seeds and mutation of counterexamples.

**Account for instrumentation effects.** A global logging lock can serialize calls and hide races. Per-thread buffers reduce contention but need a reliable merge order for cross-thread events. Timestamp calls outside the implementation yet after argument snapshot/before invocation. Response logging occurs after the API result is fixed. Compiler optimization and weak memory can differ between instrumented/debug and release builds; test representative optimized binaries and use trace mechanisms designed for the runtime.

History logging must not dereference nodes after the API's lifetime ends. Avoid observing internal state unless a white-box verifier explicitly proves the probe safe. If logger allocation can fail or block, preallocate bounded buffers and fail the test as incomplete on overflow.

**Separate abstract and memory correctness.** A use-after-free execution might accidentally yield a linearizable history. A data race can be undefined even if returned values fit the spec. Conversely, a memory-safe implementation can be non-linearizable. Combine history checking with race detectors, memory sanitizers, model/litmus tools, invariant assertions, ABA/reclamation tests, and proof review.

Similarly, linearizability is safety, not liveness. A history containing only completed calls says little about starved operations. Pending duration, retry counts, fairness, deadlock, and progress classes need separate monitoring/tests. Timeouts can make histories incomplete and checker interpretation more complex.

**Use formal verification where risk warrants.** Linearizability testing samples executions. Model checking can explore bounded schedules systematically; refinement proofs, simulation relations, rely-guarantee, or mechanized proof can cover parameterized behavior under assumptions. Tests validate implementations/toolchains/environment assumptions and discover counterexamples; proof establishes universal claims within its model. Neither deserves to be replaced by the other.

**Use a finite checker honestly.** The model below checks two complete register histories. It constructs response-before-invocation predecessor sets, performs depth-first spec search, and reports one witness for the valid history. It refutes a later read of 0 after a completed write of 1.

<!-- bijux-verify: {"id":"bounded-register-linearizability-checker","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"valid_history=True\nvalid_linearization=W1,W2,R2\ninvalid_history=False\ninvalid_linearization=none\nvalid_explored=3\ninvalid_explored=2\nreal_time_preserved=True\nsequential_spec=atomic_register\nall_invariants=True\nevidence=finite_history_search_model\n","stderr":""}} -->
```python
def check_register(history):
    predecessors = {}
    by_id = {operation["id"]: operation for operation in history}
    for operation in history:
        predecessors[operation["id"]] = {
            other["id"]
            for other in history
            if other["response"] < operation["invocation"]
        }
    explored = [0]

    def search(placed, remaining, state):
        if not remaining:
            return placed
        for operation_id in remaining:
            if not predecessors[operation_id].issubset(set(placed)):
                continue
            operation = by_id[operation_id]
            explored[0] += 1
            next_state = state
            legal = True
            if operation["method"] == "write":
                next_state = operation["argument"]
                legal = operation["result"] == "ok"
            elif operation["method"] == "read":
                legal = operation["result"] == state
            else:
                legal = False
            if legal:
                next_remaining = [item for item in remaining if item != operation_id]
                witness = search(placed + [operation_id], next_remaining, next_state)
                if witness is not None:
                    return witness
        return None

    operation_ids = [operation["id"] for operation in history]
    witness = search([], operation_ids, 0)
    return witness, explored[0], predecessors


valid = [
    {"id": "W1", "method": "write", "argument": 1, "result": "ok", "invocation": 0, "response": 5},
    {"id": "W2", "method": "write", "argument": 2, "result": "ok", "invocation": 1, "response": 2},
    {"id": "R2", "method": "read", "argument": None, "result": 2, "invocation": 3, "response": 4},
]
invalid = [
    {"id": "W1", "method": "write", "argument": 1, "result": "ok", "invocation": 0, "response": 1},
    {"id": "R0", "method": "read", "argument": None, "result": 0, "invocation": 2, "response": 3},
]

valid_witness, valid_explored, valid_predecessors = check_register(valid)
invalid_witness, invalid_explored, invalid_predecessors = check_register(invalid)
real_time_preserved = valid_predecessors["R2"] == {"W2"}
all_invariants = (
    valid_witness == ["W1", "W2", "R2"]
    and invalid_witness is None
    and valid_explored == 3
    and invalid_explored == 2
    and real_time_preserved
    and invalid_predecessors["R0"] == {"W1"}
)

print(f"valid_history={valid_witness is not None}")
print("valid_linearization=" + ",".join(valid_witness))
print(f"invalid_history={invalid_witness is not None}")
print("invalid_linearization=none")
print(f"valid_explored={valid_explored}")
print(f"invalid_explored={invalid_explored}")
print(f"real_time_preserved={real_time_preserved}")
print("sequential_spec=atomic_register")
print(f"all_invariants={all_invariants}")
print("evidence=finite_history_search_model")
```

The checker accepts only complete deterministic single-register operations, assumes trustworthy integer event order, rebuilds small states directly, and returns the first witness. It has no memoization, pending/nondeterministic support, malformed-history checks, concurrency, arbitrary object model, timeout, decomposition, weak-memory reasoning, or proof of the implementation that produced a history.

**Operate the evidence pipeline.** CI should preserve raw input, normalized history, spec/version digest, decision/witness or counterexample, search statistics, limits, seed, platform, and tool versions under artifacts. A timeout is visible and fails a completion gate when linearizability evidence is required. Maintain known-valid and known-invalid checker fixtures, including pending and malformed cases, to prevent checker regressions.

For every production concurrent structure, pair narrow deterministic schedules with generated histories. Review coverage by semantic boundary rather than run count. A billion redundant successful operations do not replace one forced resize-delete or reclaim-reuse schedule. Completion claims should say exactly which histories, configurations, and proofs exist.

## Definitions and Notation

History `H` is a finite sequence of invocation/response events. Completed operation `o=(inv(o),res(o))`; pending invocation lacks `res`. Projection `H|p` retains events for process p; well-formed sequential p alternates invocation/response. `complete(H)` removes pending invocations after an allowed extension policy.

Real-time order `o_1 <_H o_2` iff `res(o_1)` precedes `inv(o_2)`. Overlap means neither relation holds. Sequential history `S` is legal for specification state machine `(Σ,s_0,δ)` when each transition `δ(s,method,args)` admits the recorded result and yields next state.

`H` is linearizable iff it can be extended by responses to zero or more pending invocations such that `complete(H')` is equivalent per process/object to legal S and `<_H ⊆ <_S`. A checker state can be `(R,s)`, remaining operations R and sequential state s, plus pending/nondeterministic metadata where supported.

Let N be operations, C maximum mutually overlapping calls, B explored branches, M memoized states, `T_c` checker time, `U` unknown/timeouts, and `F` invalid histories. These are empirical/search values. Worst-case permutation space can be factorial; actual pruning depends on precedence/results/spec.

## Mechanisms, Invariants, or Proof Structure

### History fidelity proof

1. Invocation is recorded before implementation entry and response after outcome fixation.
2. Unique IDs pair exactly one invocation/response; per-participant order is valid.
3. Arguments/outcomes are immutable normalized copies matching API semantics.
4. Recorder ordering is sufficient for claimed real-time edges and loss/overflow is detected.
5. Crash, timeout, cancellation, retry, and external effects follow explicit completion rules.

### Decision proof

1. Build exactly the mandatory real-time predecessor relation.
2. Start from independently validated sequential initial state.
3. Extend only with predecessor-ready operations whose modeled result matches.
4. Backtracking restores/copies all spec state; memo/pruning merges only equivalent problems.
5. Full placement witnesses linearizability; exhaustive branch exhaustion proves this finite interpreted history invalid.

### Scope proof

1. Identify completed search versus timeout/resource unknown.
2. Justify object/key decomposition and history windows from specification independence.
3. Preserve pending effects and nondeterministic outcomes where applicable.
4. Separate abstract-history results from data-race, memory-safety, and progress evidence.
5. State sampled inputs/schedules/configurations and retain independent proof obligations.

### Evidence ladder

1. Independent sequential model and hand-checked valid/invalid fixtures.
2. History recorder fidelity/overflow/malformed tests.
3. Finite search witness/counterexample model.
4. Deterministic schedule hooks and minimized causal regressions.
5. Generated adversarial histories with complete decisions and unknown accounting.
6. Bounded model checking, memory litmus/race/lifetime tools, and invariant assertions.
7. Linearization/progress/reclamation proof review plus production-shaped telemetry.

## Alternatives and Trade-Offs

| Technique | Evidence produced | Main strength | Principal limitation |
|---|---|---|---|
| Final-state tests | postcondition | cheap baseline | misses returned-history violations |
| History checker | finite linearizability decision | black-box semantic counterexamples | exponential, sampled histories |
| Deterministic scheduler | controlled interleaving | reproducible causal traces | chosen hook/model coverage |
| Stateless model checking | systematic bounded schedules | broad schedule exploration | bounds/state explosion |
| Linearization-point assertions | internal point validation | precise debugging | prophecy/helping/points can be subtle |
| Refinement/mechanized proof | universal result in model | strongest formal scope | model/assumption/proof cost |
| Race/lifetime sanitizer | exercised memory defects | finds data race/UAF classes | no abstract semantic guarantee |
| Stress/fuzz testing | diverse empirical schedules | easy continuous pressure | weak completeness/reproducibility |
| Differential oracle | compare with reference | broad semantic coverage | ordering and shared-bug risk |

Use multiple layers. The history checker is the semantic center for observed executions, not a replacement for memory-safety tools or proof. A mature checker library is preferable to a bespoke search once the object model exceeds educational scale.

## Failure Modes and Misconceptions

- **“Linearization follows invocation order.”** overlapping calls may linearize oppositely.
- **“Last response means last effect.”** response can be delayed after an earlier point.
- **“Final state is enough.”** duplicate/lost return values can cancel in state.
- **“Race-free means linearizable.”** synchronization can implement the wrong atomic semantics.
- **“Linearizable means memory-safe.”** undefined/free memory can coincidentally return legal values.
- **“Passing one history proves the object.”** it proves only existence of one ordering for that history/spec.
- **“No witness before timeout means invalid.”** search incompletion is unknown.
- **“Drop every pending call.”** a pending call may explain later completed observations.
- **“Clock timestamps totally order a cluster.”** uncertainty and skew invalidate invented edges.
- **“Per-key partition always works for maps.”** global operations/capacity/ranges couple keys.
- **“Minimized history is the exact schedule.”** it preserves semantic constraints, not necessarily implementation timing.
- **“The production object is a good oracle.”** shared defects can produce false confidence.
- **“Weak iterator should pass snapshot spec.”** test against documented weaker semantics or a snapshot API.
- **“More logging improves fidelity.”** instrumentation can serialize/perturb or introduce unsafe access.
- **“Linearizability implies lock-freedom.”** safety says nothing about completion/fairness.

## Worked Examples

### Example 1

**Situation.** W1 responds after W2, but their intervals overlap and final register value is W2's value.

**Reasoning.** Response order is not mandatory for overlapping calls. If the spec permits `W1,W2`, the history is legal even when W1's caller returns later.

**Conclusion.** Only response-before-later-invocation creates real-time precedence.

### Example 2

**Situation.** Queue enqueues A then completes before enqueue B starts; later dequeues return B then A.

**Reasoning.** Real time fixes enqueue A before B. FIFO sequential spec then requires A before B among those items absent intervening effects. No ordering of overlapping dequeues can justify B first if both are present.

**Conclusion.** A short history can refute FIFO despite a plausible empty final queue.

### Example 3

**Situation.** Pending write 1 overlaps a completed read returning 1.

**Reasoning.** Dropping the pending write makes the read impossible from initial 0. Completing/linearizing the pending write before read may make history legal. Checker must explore the formal extension policy.

**Conclusion.** Pending operations can be semantically necessary.

### Example 4

**Situation.** Checker reaches its 10-second limit without finding a witness.

**Reasoning.** Unexplored branches may contain one. Outcome is unknown-timeout with search statistics and raw history, not invalid and not pass. Reduce/partition soundly or increase resources.

**Conclusion.** Resource exhaustion is a first-class third outcome.

### Example 5

**Situation.** Map operations are partitioned by key, but history includes `size()` returning 1.

**Reasoning.** Size couples all keys; independent per-key witnesses can disagree on its point/result. Keep the coupled history together or use a proved decomposition including global state.

**Conclusion.** P-compositionality requires specification-level independence.

### Example 6

**Situation.** A global mutex protects history logging around every call.

**Reasoning.** It serializes invocations/responses and may eliminate the races under test. Move to bounded per-thread event capture with reliable event sequencing/merge and explicit overflow failure.

**Conclusion.** Recorder fidelity includes noninterference.

### Example 7

**Situation.** A weakly consistent iterator sees A and new C but misses concurrently removed B.

**Reasoning.** This may violate snapshot spec yet satisfy documented iterator semantics. Model the actual allowed relation or test a snapshot operation separately.

**Conclusion.** A checker is only as correct as its sequential/observation contract.

### Example 8

**Situation.** A failed history shrinks from 40 operations to two, but no longer reproduces under normal scheduling.

**Reasoning.** The two-operation partial order proves semantic impossibility for the recorded outcomes; scheduling pressure that created those outcomes was removed. Add hooks guided by raw trace and minimized causal constraint.

**Conclusion.** Keep raw and minimized evidence and build deterministic replay.

### Example 9

**Situation.** History passes while a sanitizer reports use-after-free in one operation.

**Reasoning.** Returned values happened to match a legal sequential order, but implementation behavior is memory-unsafe/undefined. The module fails overall regardless of history result.

**Conclusion.** Abstract safety and memory safety are independent gates.

### Example 10

**Situation.** One thread's pop remains pending for minutes while peers complete millions of legal operations.

**Reasoning.** Completed subhistories may all be linearizable and the structure lock-free, yet victim starvation violates a fairness/service objective. Measure pending age/retries and test progress separately.

**Conclusion.** Linearizability testing cannot certify liveness.

## Cross-Program Connections

- **Concurrent and Parallel Programming:** schedules, memory models, atomics, progress, model checking, and deterministic execution shape histories.
- **Software Engineering:** executable specifications, property-based generation, delta debugging, artifact provenance, CI limits, and regression design operationalize evidence.
- **Distributed Systems:** client histories, pending timeouts, retries, clock uncertainty, and consistency models require careful operation boundaries.
- **Database Engineering:** serializability and strict serializability are related transaction conditions but differ in object/composition scope and histories.
- **Security Engineering:** malformed logs, secret redaction collisions, adversarial state explosion, dropped events, and checker denial-of-service require controls.
- **Performance Engineering:** logging perturbation, checker complexity, schedule diversity, retry/starvation telemetry, and production topology affect conclusions.

## References

1. Maurice P. Herlihy and Jeannette M. Wing, [“Linearizability: A Correctness Condition for Concurrent Objects”](https://www.cs.cmu.edu/~wing/publications/HerlihyWing90.pdf), *ACM TOPLAS* 12(3), 1990. Primary definition, histories, locality, and queue examples.
2. Jeannette M. Wing and Chun Gong, [“Testing and Verifying Concurrent Objects”](https://www.cs.cmu.edu/~wing/publications/WingGong93.pdf), *Journal of Parallel and Distributed Computing* 17, 1993. Primary history-search testing and complementary verification account.
3. Gavin Lowe, [“Testing for Linearizability”](https://www.cs.ox.ac.uk/people/gavin.lowe/LinearizabiltyTesting/paper.pdf), *Concurrency and Computation: Practice and Experience* 29(4), 2017. Primary testing algorithms, performance, and practical framework.
4. Alex Horn and Daniel Kroening, [“Faster Linearizability Checking via P-Compositionality”](https://www.kroening.com/papers/forte2015-li.pdf), FORTE 2015. Primary specification-driven decomposition optimization.
5. Sebastian Burckhardt, Chris Dern, Madanlal Musuvathi, and Roy Tan, [“Line-Up: A Complete and Automatic Linearizability Checker”](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/pldi015-burckhardt.pdf), PLDI 2010. Primary systematic checker for deterministic components.
6. Anish Athalye, [Porcupine linearizability checker](https://github.com/anishathalye/porcupine), current project accessed 2026-08-30. Maintainer implementation of a practical P-compositional checker and model/history API.
7. Maged M. Michael and Michael L. Scott, [“Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms”](https://www.cs.rochester.edu/u/scott/papers/1996_PODC_queues.pdf), PODC 1996. Primary operation points/progress example used by queue histories.
8. OpenJDK Project, [JCStress](https://github.com/openjdk/jcstress), current project accessed 2026-08-30. Official JVM concurrency stress harness illustrating complementary outcome-based testing and environment/toolchain concerns.

## Exercises

### Exercise 1

Define history, completed/pending operation, real-time precedence, overlap, sequential specification, linearization, witness, state-space explosion, and unknown outcome. State the finite-history decision condition.

### Exercise 2

For a stack initially empty: P pushes A `[0,4]`; Q pushes B `[1,2]`; R pops B `[3,5]`; S pops A `[6,7]`. Derive mandatory precedence and one legal linearization, or explain impossibility.

### Exercise 3

Audit a harness that records only response timestamps, uses the concurrent map itself as oracle, drops pending calls and exceptions, partitions by key despite `clear`, and marks timeout as pass. Give corrections and outcome taxonomy.

### Exercise 4

Design a production-ready history-testing pipeline for a bounded closeable MPMC queue, including model, capture, pending/cancellation, generators, checker limits, minimization/replay, memory/progress tools, and artifacts.

### Exercise 5

A distributed key-value API has per-client sessions, retries with idempotency IDs, server failover, uncertain clocks, range scans, and timed-out writes that may commit. Define a defensible linearizability-testing scope and say what remains outside it.

## Answers to the Exercises

### Answer 1

A history orders invocation/response events. Completed operations have matching responses; pending do not. A precedes B in real time when A responds before B is invoked; otherwise overlapping calls may be ordered either way. A sequential specification maps state plus call to allowed result/next state. A linearization is a legal sequential history equivalent to an allowed completion of the concurrent history and preserving real-time order. A witness is one such sequence. State-space explosion is combinatorial candidate growth. Unknown means the decision did not complete or inputs/spec are insufficient.

For a complete deterministic finite history, build mandatory predecessors and search sequential-model transitions. It is linearizable iff at least one full predecessor-respecting placement reproduces every result. Exhaustion proves invalid only with faithful history/model and sound search; resource cutoff is unknown.

### Answer 2

Q's push B responds at 2 before R's invocation at 3, so Q<B-before-R is mandatory. P push A overlaps Q and R. Both pushes respond before S invokes at 6, and R responds at 5 before S, so all three precede S. Choose `push(A), push(B), pop()->B, pop()->A`. This respects Q before R, every operation before S as required, and LIFO results. P may linearize before Q even though P responds later because they overlap.

Thus the history is linearizable. Ordering `push(B),push(A)` would make R's B result problematic unless another operation intervened, but existence of one witness suffices.

### Answer 3

Response timestamps cannot reconstruct intervals/mandatory order; record invocation and response events with unique operation/participant IDs and reliable monotonic event sequence/causal order. The concurrent map shares bugs and concurrency behavior; implement/validate an independent sequential state model. Pending calls need formal omit-or-complete exploration, especially when later reads observe them. Exceptions/cancellation/full/empty are modeled outcomes. `clear` couples all keys, so per-key partition is unsound for histories containing it. Timeout is `unknown_timeout`, never pass.

Validate malformed histories (unmatched/duplicate/lost events) and unsupported methods explicitly. Report `linearizable`, `not_linearizable`, `unknown_timeout/resource`, `malformed_history`, or `unsupported`, retaining raw history, spec/checker digest, limits, witness/counterexample, and search statistics.

### Answer 4

Sequential model state is bounded FIFO sequence plus capacity and lifecycle (`open/closed`): enqueue appends or returns full/closed; dequeue removes oldest or returns empty/closed according to drain policy; close changes admission at one specified point. Record copied arguments/results/exceptions and invocation/response with IDs in bounded non-dropping per-thread buffers; overflow invalidates the run. Model timed/cancelled calls: before linearization no effect; after effect return/recovery policy must expose committed outcome or idempotent operation ID. Explore pending calls that may have acted.

Generate empty/singleton/full, simultaneous producers/consumers, close during calls, timeout boundaries, duplicate payloads, allocation failure, wrap/index boundaries, stalled threads, ABA/reclamation, thread counts/topologies, and known bug mutations. Use complete short-history checks plus sound partitioning only where queue spec permits (usually not by element). Unknowns fail the required evidence gate. Preserve raw/normalized history, seed, platform/toolchain/commit, spec/checker versions, witness/counterexample, search limits/stats, and minimized history. Build deterministic hook-based replay from raw/minimized constraints. Run race/use-after-free and memory-model tools, capacity/lifecycle invariants, starvation/retry/deadlock tests, and proof review. Do not claim universal correctness from pass counts.

### Answer 5

Define one logical operation per idempotency ID, with client invocation before first attempt and response when the API declares final success/failure; retries are transport attempts, not new writes. Preserve per-client session order causally. Timed-out writes remain pending if the contract permits later commit; checker explores omit/commit with allowed result/effect and uses later reads to constrain it. Failover events are workload metadata. Do not derive mandatory cross-client order from uncertain clocks; establish real-time edges only through trusted client recorder/causal barriers or intervals whose uncertainty proves nonoverlap.

Start with single-key get/put/delete if keys are independent. Range scans, transactions, global revision, quotas, and clear couple keys and need one multi-key specification or a separate declared consistency model. Record server acknowledgments, idempotency handling, exceptions, and values durably enough to survive failover. Checker can decide finite captured histories under this model. Outside it remain unobserved executions, clock/recorder assumptions, durability across crashes unless modeled, replica/consensus correctness, weak range semantics, data races/memory safety, liveness/availability, exactly-once external side effects, and universal proof. Pair with fault injection, model checking/protocol proof, durability audits, and progress telemetry.
