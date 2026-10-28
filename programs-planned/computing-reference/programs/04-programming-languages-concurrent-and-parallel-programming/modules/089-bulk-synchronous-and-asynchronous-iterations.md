---
module_id: CONPAR-089
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 89
title: Bulk-Synchronous and Asynchronous Iterations
status: complete
last_verified: 2026-08-29
---

# Bulk-Synchronous and Asynchronous Iterations

## One-Page Review

### Governing question

When may a distributed iterative algorithm replace globally aligned rounds with overlapped or stale component updates without changing its fixed point, violating communication semantics, or declaring convergence while useful work and messages remain in flight?

### Essential definitions

- A **fixed-point iteration** seeks `x*` satisfying `F(x*)=x*` through repeated applications of F.
- A **bulk-synchronous superstep** consists of local computation, communication, and a logical synchronization boundary before the next generation consumes communicated state.
- **arrival skew** is the spread in times workers reach a synchronization boundary; it exposes idle time but does not itself prove that removing the boundary is correct.
- A **nonblocking synchronous iteration** overlaps communication with independent work while retaining the same generation boundary and mathematical recurrence.
- An **asynchronous iteration** updates components at different times using values whose component-specific versions may differ.
- **staleness** is the age, in logical updates or iterations, of a value relative to the newest version relevant to an update.
- **partial asynchronism** bounds update gaps and/or communication delay; **total asynchronism** permits unbounded finite delays but requires every relevant component to be updated and sufficiently fresh information eventually to arrive.
- **fairness** prevents a required component or message from being postponed forever.
- A **contraction** satisfies `||F(x)-F(y)|| <= q||x-y||` for some `0 <= q < 1`; under a complete metric space it has a unique fixed point and synchronous iteration converges.
- A **residual** measures failure to satisfy the target equation, such as `r=b-Ax` or `F(x)-x`; an implementation must specify whether it is exact, recursive, local, or globally reduced.
- **quiescence** means every worker is passive and no relevant work/message remains in transit; local inactivity alone is not distributed termination.

### Central model, mechanism, or theorem

The synchronous recurrence is `x^(k+1)=F(x^k)`. A componentwise asynchronous execution instead performs `x_i <- F_i(x_1^(tau_i1),...,x_n^(tau_in))`, where each `tau_ij` identifies the version actually read. The synchronous contraction proof gives `||x^k-x*|| <= q^k||x^0-x*||`. It does not automatically prove an arbitrary stale, reordered, dropped, duplicated, or racing implementation. An asynchronous completion claim requires a theorem whose assumptions match the mapping, norm/domain, update fairness, delay/freshness, atomicity, and error model, plus a protocol proving that the stopping predicate is globally sound.

### Critical invariants

Each state/message carries problem, epoch, iteration/version, partition, schema, and numeric-policy identity; each component has one authoritative update rule; reads and writes obey a documented atomicity/consistency model; messages are validated, deduplicated or algebraically safe, and old epochs cannot corrupt new ones; every dependency needed by the convergence theorem is eventually refreshed; residual and stopping rules match the proved quantity; no rank exits while another can generate relevant work; outstanding communication is completed or cancelled legally; failure behavior is explicit; and output publication occurs only after numerical, protocol, and domain validation.

### Common failures

Teams remove a barrier but retain code that assumes aligned buffers, call nonblocking operations and overwrite buffers before completion, confuse overlap with mathematical asynchronism, cite synchronous convergence for stale updates, let one hot component starve, accept unbounded stale state without a theorem, compare iteration counts instead of time and useful work, use a local residual as a global stopping test, run collectives in inconsistent order, allow delayed messages across epochs, assume floating reductions are reproducible, treat an idle queue as termination, or call ordinary MPI process failure recoverable.

### Compact example

For `F([x0,x1,x2,x3])=[8,max(x1,x0-1),max(x2,x1-1),max(x3,x2-1)]` from `[8,0,0,0]`, Jacobi-style bulk rounds propagate one edge per round: `[8,7,0,0]`, `[8,7,6,0]`, `[8,7,6,5]`. A fair in-place order 1,2,3 reaches the same least fixed point in one sweep. This finite monotone example demonstrates scheduling, not a general theorem: a different mapping, stale schedule, non-atomic race, or stopping rule may diverge or return an invalid result.

### Connections

[Communication-Computation Overlap](086-communication-computation-overlap.md) preserves request/buffer lifetimes while hiding latency. [Load Imbalance Across Nodes](088-load-imbalance-across-nodes.md) diagnoses stragglers that make global rounds costly. [Collective Communication](083-collective-communication.md) supplies global reductions and ordering constraints. The [program roadmap](../ROADMAP.md) next measures cross-node scaling rather than assuming that fewer barriers produces scale.

## Governing Question

What synchronization semantics does the algorithm actually require, which theorem covers the resulting update schedule, how will the implementation observe progress and global termination, and does the measured reduction in exposed waiting outweigh added messages, versions, contention, nondeterminism, and validation cost?

Synchronization is part of the algorithm's meaning. A barrier can be unnecessary overhead, a generation fence, a convergence reduction, a buffer-lifetime boundary, or all four. Remove only the properties that have explicit replacements.

## Why This Matters

Many scientific, graph, optimization, simulation, and learning workloads repeat local updates and exchange boundary or aggregate state. In a bulk-synchronous design, the slowest participant determines each superstep. Load skew, network tails, accelerators, operating-system noise, and heterogeneous nodes turn small delays into repeated global idle time.

Asynchronous execution can keep workers useful and tolerate variable arrival. It can also consume inconsistent cuts of distributed state, increase communication, amplify stale gradients, change floating-point order, obscure progress, and make termination a distributed-systems problem. Speed is not obtained merely by deleting `Barrier`: hidden collectives, dependencies, buffer reuse, and progress rules remain.

The engineering task is therefore a refinement proof plus an experiment. State the mathematical operator and synchronization contract; choose a synchronous, overlapped, bounded-stale, or asynchronous schedule; prove the schedule is admitted by a relevant theorem; implement versioned communication and termination; then measure time-to-valid-solution under representative imbalance and failure conditions.

## Prerequisites and Retrieval

Retrieve:

- communicator membership, collective order, nonblocking request/buffer lifetime, weak progress, and completion from [Collective Communication](083-collective-communication.md) and [Communication-Computation Overlap](086-communication-computation-overlap.md);
- owned/ghost state, partition generations, exchanges, and boundary validity from [Domain Decomposition](084-domain-decomposition.md) and [Halo Exchange and Stencil Computation](085-halo-exchange-and-stencil-computation.md);
- causal phase timing, arrival distributions, and amortization from [Load Imbalance Across Nodes](088-load-imbalance-across-nodes.md); and
- memory ordering, atomics, races, and progress from [Happens-Before Relations](023-happens-before-relations.md), [Atomic Read-Modify-Write Operations](025-atomic-read-modify-write-operations.md), and [Obstruction-Free, Lock-Free, and Wait-Free Progress](051-obstruction-free-lock-free-and-wait-free-progress.md).

Retrieval prompt: identify F, state domain/norm, fixed point and uniqueness assumptions; component ownership and update dependency graph; synchronous baseline; admissible delay/update model and theorem; message/version/duplicate rules; local and global residual definitions; termination protocol; communication progress; numeric precision/order and reproducibility policy; fault model; observability; representative skew; correctness oracle; and publication or rollback gate.

## Learning Objectives

After completing this module, a learner can:

1. distinguish BSP supersteps, nonblocking overlap, bounded-stale execution, and genuinely asynchronous iteration;
2. model component updates with explicit read versions and fairness/delay conditions;
3. prove synchronous contraction convergence and identify what an asynchronous theorem must additionally establish;
4. design message/version/epoch protocols that prevent stale cross-generation corruption;
5. separate local inactivity, local convergence, a consistent global residual, and distributed quiescence;
6. respect MPI collective order, completion, buffer lifetime, and weak-progress assumptions;
7. compare convergence per update, iteration, communication, and wall-clock time without misleading metrics;
8. test adversarial schedules, delays, duplicates, reordering, imbalance, and numerical sensitivity;
9. choose a synchronization regime using correctness, performance, operability, and failure evidence; and
10. scope security, scientific, operational, and high-stakes human review.

## Core Exposition

### Begin with the mathematical iteration

Let `X=X_1 x ... x X_n`, `F:X->X`, and seek `x*` such that `F(x*)=x*`. A Jacobi-style synchronous iteration reads a single immutable generation k and constructs all components of generation k+1. A Gauss-Seidel-style schedule exposes updates immediately in an order. Parallel block variants assign subsets to workers. These are different executions and may be different numerical algorithms even if source code shares one update formula.

State the domain, norm or order, existence/uniqueness assumptions, and error quantity before choosing runtime mechanics. Linear stationary iterations may be expressed `x^(k+1)=Bx^k+c`; their convergence depends on B, commonly through spectral-radius or norm conditions. Nonlinear fixed-point, gradient, coordinate, graph, and PDE methods each have different admissibility conditions. “Iterative” does not imply “safe asynchronously.”

For a contraction in a complete metric space, Banach's fixed-point theorem supplies unique x* and synchronous convergence. From `x^(k+1)=F(x^k)`,

`||x^(k+1)-x*|| = ||F(x^k)-F(x*)|| <= q||x^k-x*||`,

so induction gives `||x^k-x*|| <= q^k||x^0-x*||`. This compact proof depends on every update applying F to the stated x^k. It is not a license to substitute an arbitrary mixture of versions.

### Bulk-synchronous execution

Valiant's BSP model provides processors with local memory, communication, and global synchronization in supersteps. A practical iteration may compute owned interiors, exchange boundaries, reduce a residual, and cross a logical boundary before reusing buffers/state. The boundary establishes a consistent generation even when the underlying collective is not a literal barrier.

A simple superstep cost model is `T_s=max_r w_rs + g*h_s + l`, where `w_rs` is local work on rank r, h captures communicated volume under a machine-dependent gap/bandwidth parameter g, and l represents synchronization latency. Real systems add message counts, topology, contention, progress, memory, and imbalance. The model is explanatory, not a universal timing equation.

BSP strengths include reproducible generation structure, simple ownership, bounded live state, straightforward checkpointing, and easy global reductions. Costs include arrival waiting, repeated latency, sensitivity to one straggler, and possible over-synchronization when dependencies are sparse.

Do not equate a collective with a barrier. MPI says collective completion primarily frees the caller's buffer and does not generally prove all peers have completed. Nevertheless, all participants must issue matching collective operations in the required order. An iteration counter, communicator, and collective sequence are protocol state.

### Overlap without changing the recurrence

Nonblocking halo exchanges or reductions can start early, run while dependency-independent work proceeds, and complete before data is consumed or buffers reused. This can preserve `x^(k+1)=F(x^k)`. It is pipelining a synchronous algorithm, not automatically an asynchronous numerical method.

Document post, progress, completion, and first-use events. Assume only weak MPI progress unless implementation evidence justifies stronger behavior; periodically entering MPI or a progress mechanism may be required. Do not access a nonblocking collective buffer before completion, and preserve identical collective order per communicator. If pipelining carries several iterations, tag slots by epoch/iteration and bound the window so old completions cannot overwrite current state.

Overlap is often the lowest-risk response to exposed communication. It cannot eliminate a true dependency or a late producer, and progress threads can consume cores, alter affinity, or contend for memory. Validate actual overlap on a timeline and compare end-to-end time.

### Model asynchronous component updates

At logical event t, a worker may update component i using values with component-specific timestamps:

`x_i(t+1)=F_i(x_1(tau_i1(t)),...,x_n(tau_in(t)))`,

while components not selected retain their values. The functions `tau_ij(t)<=t` make the read history explicit. Partial-asynchronism assumptions often bound how long a component can go without an update and how stale a read may be. Total-asynchronism models may permit arbitrarily large finite delays while requiring infinite updates of each relevant component and `tau_ij(t)->infinity` along those updates.

The exact assumptions and result must come from the theorem used. Contraction in a suitable block-maximum norm, monotone nested-set arguments, diagonal dominance, step-size restrictions, or problem-specific Lyapunov functions are common routes. They are not interchangeable. Some optimization methods tolerate bounded delays only after reducing a step size; some converge with stale reads but not lost updates; some monotone graph computations need an inflationary/semilattice operation; some nonlinear solvers fail.

“Lock-free” and “asynchronous iteration” answer different questions. Lock-free describes system-wide operation progress under a shared-memory algorithm; asynchronous numerical convergence describes a sequence of possibly stale mathematical updates. A data-race-free atomic write can still implement a divergent update schedule. A convergent abstract schedule can still be implemented with undefined language-level races.

### Deterministic propagation model

This executable model compares immutable-round propagation with one fair in-place sweep for a finite monotone recurrence. It checks the fixed point exactly using integers. It does not model MPI, staleness bounds, floating arithmetic, performance, failures, or general asynchronous convergence.

<!-- bijux-verify: {"id":"synchronous-asynchronous-propagation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"initial=[8, 0, 0, 0]\nsynchronous_round_1=[8, 7, 0, 0]\nsynchronous_round_2=[8, 7, 6, 0]\nsynchronous_round_3=[8, 7, 6, 5]\nsynchronous_round_4=[8, 7, 6, 5]\nasynchronous_update_1=[8, 7, 0, 0]\nasynchronous_update_2=[8, 7, 6, 0]\nasynchronous_update_3=[8, 7, 6, 5]\nfixed_point=[8, 7, 6, 5]\nsame_fixed_point=True\n","stderr":""}} -->
```python
initial = [8, 0, 0, 0]


def bulk_step(state):
    result = state[:]
    for index in range(1, len(state)):
        result[index] = max(state[index], state[index - 1] - 1)
    return result


def is_fixed(state):
    return bulk_step(state) == state


print(f"initial={initial}")
synchronous = initial[:]
for round_number in range(1, 5):
    synchronous = bulk_step(synchronous)
    print(f"synchronous_round_{round_number}={synchronous}")

asynchronous = initial[:]
for update_number, index in enumerate([1, 2, 3], start=1):
    asynchronous[index] = max(asynchronous[index], asynchronous[index - 1] - 1)
    print(f"asynchronous_update_{update_number}={asynchronous}")

print(f"fixed_point={synchronous}")
print(f"same_fixed_point={asynchronous == synchronous and is_fixed(asynchronous)}")
```

### Version, consistency, and message protocol

Give each run immutable problem/configuration identity and an epoch. Give state updates component/block identity, owner generation, logical version, schema, precision, and payload integrity metadata. A receiver rejects wrong problem/schema/partition, quarantines future epochs, and discards or safely handles obsolete versions. Decide whether duplicate updates are rejected by ID, idempotent, or combined by an associative/commutative/idempotent operation. “Latest arrival wins” is unsafe when networks reorder messages and version order differs from arrival order.

Define atomicity. Shared-memory components may use atomic values, locks, versioned snapshots, or seqlocks; compound vectors require a consistency strategy. MPI point-to-point ordering is conditional on sender, destination, matching, and threading; wildcard receives and wait-any introduce nondeterminism. RMA ordering/atomicity has precise, limited scope. Application versions remain necessary.

Bound memory and backpressure. A fast producer must not retain unbounded snapshots or overwhelm a slow consumer. Coalesce only if intermediate updates are semantically redundant. If every delta matters, apply flow control or log with bounded recovery policy. Establish when send buffers can be reused and receive state becomes visible to computation.

### Residuals and stopping

Convergence and termination are distinct. A component can satisfy a local tolerance while another component later sends a value that reactivates it. An empty local queue says nothing about in-flight messages. A global reduction of local residuals is meaningful only if samples correspond to an admitted state/cut and the residual matches the theorem.

Specify stopping as a stable predicate. Examples include a globally reduced residual at a synchronization checkpoint; a snapshot/marker protocol; or termination detection that accounts for passive workers and messages/work credits in flight. Dijkstra-Scholten termination detection overlays acknowledgements/deficits on a diffusing computation so the initiator can establish global quiescence. Its assumptions must match channel/process failures and the computation shape; naming it does not implement fault-tolerant termination.

Residual semantics matter. Recursive residuals can drift from the true residual; delayed components make “current x” ambiguous; norms may require global reduction; relative tolerances need a reference scale; NaN/Inf must fail closed. Periodic synchronous validation can recompute an exact/global residual and create a checkpoint even when interior iterations are asynchronous.

Define maximum updates/time, stagnation/divergence, delayed-message drain, and cancellation. On stop, freeze the epoch, stop generating work, account for or reject late traffic, verify the final state, complete required requests collectively, and only then publish. A rank must not unilaterally leave an MPI collective protocol.

### Convergence and error evidence

A useful proof packet contains: operator/domain; fixed-point existence/uniqueness; norm/order/Lyapunov function; synchronous baseline proof; block decomposition; schedule model; update fairness; delay/freshness and loss/duplicate assumptions; atomic read/write model; inexact/floating errors; stopping theorem; and mapping from implementation events to mathematical indices.

For a block contraction with modulus q in an appropriate maximum norm, asynchronous convergence can be established under stated freshness/fairness models because sufficiently new updates move all component errors through successively smaller nested boxes. But rate in wall time depends on update frequency, delay, communication, and hardware. Repeating a stale update may count as work without meaningful contraction.

For monotone finite-domain propagation, prove updates are inflationary, bounded, and fair; then termination at a common fixed point can follow under the specific lattice/operator conditions. For optimization, identify convexity/smoothness and step-size restrictions. For linear solvers, state matrix splitting and spectral/norm/diagonal conditions. Never cite one case as universal.

Floating-point updates add non-associativity and possibly nondeterministic arrival/order. Define whether the requirement is bitwise reproducibility, deterministic schedule, bounded numerical difference, residual/backward error, or domain outcome. Use stable accumulation or reproducible reductions when required; compare against higher precision or trusted small problems. An empirical match is evidence for tested cases, not proof for all schedules.

### Performance model and experiment

Compare time-to-valid-solution, not merely seconds per local update. Record wall time, critical rank time, useful work, updates per component, attempted/discarded updates, staleness distribution, messages/bytes, queue depth, residual trajectory, convergence checks, progress overhead, energy/resource use, and final error. Report failed/diverged/timed-out runs.

A synchronous method may take fewer effective updates but wait at every round. An asynchronous method may use more stale work/messages yet finish earlier under skew. Bounded staleness offers a control between them. Periodic synchronization limits drift and simplifies checkpoints. The best regime is workload- and theorem-specific.

Use identical problem/configuration, stopping quantity, tolerance, precision, resource allocation, and output validation. Test balanced and representative skew, different placements/scales, slow workers, delayed/reordered/duplicated messages where the protocol permits, progress modes, queue limits, and multiple seeds/schedules. Include warm-up and distributions. Avoid comparing one synchronous iteration to one asynchronous update as equivalent work.

Measure synchronization removed versus shifted. A supposedly asynchronous algorithm may still perform global convergence reductions, allocator locks, checkpoint barriers, or serialized parameter-server updates. Trace dependencies. Account for versioning, atomics, polling, validation, and termination overhead.

### Failure, recovery, and operations

Ordinary process failure during conventional MPI communication is generally not an application-level recovery mechanism. Define abort/restart, checkpoint/replay, or a specifically supported fault-tolerant model. A lost worker can violate fairness; a lost message can violate freshness; replay can duplicate a non-idempotent update; restored partitions can accept pre-failure traffic. Epoch fencing and durable checkpoint identity are essential.

Checkpoint a coherent state admitted by the algorithm. BSP naturally provides boundaries. Asynchronous checkpointing needs a coordinated snapshot, message logging, or a proof that the captured mixture is restart-valid. Validate restore by IDs/digests, component coverage, versions, residual, and reference continuation.

Production telemetry should expose per-worker update age/rate, maximum/percentile staleness, queue/backpressure, residual/check latency, dropped/rejected/duplicate messages, epoch mismatches, progress calls/thread load, collectives, idle time, checkpoint age, and termination state. Alerts need sustained thresholds and a runbook: throttle, force validation barrier, roll back/restart, quarantine node, or abort safely.

### Security and high-stakes limits

Validate message lengths, versions, identities, numeric finiteness/ranges, and authorization before allocation or state mutation. Bound queues, outstanding requests, histories, and retry rates. Malicious or corrupted staleness metadata can bypass freshness policy; authenticate where the threat model requires it. Timing, residual, and component activity can reveal sensitive workload structure, so minimize labels and control trace access/retention.

In high-stakes simulation, control, medical, infrastructure, or policy work, asynchronous scheduling cannot establish model validity or decision safety. Require named domain, numerical, systems, safety, privacy/security, operations, quality/regulatory, ethics, accessibility/human-factors, and independent validation reviewers as applicable. Preserve a conservative synchronous/reference path and fail closed on unproved convergence, invalid residual, version ambiguity, or missing participants.

## Definitions and Notation

- `P`: workers/ranks; `i,j`: state components/blocks.
- `F:X->X`: iteration mapping; `F_i`: component mapping; `x*`: fixed point.
- `x^k`: state at synchronous generation k.
- `t`: logical asynchronous update event.
- `tau_ij(t)`: version/time of component j read for updating i at t.
- `q`: contraction modulus, `0<=q<1`, in a stated norm.
- `d_ij(t)=t-tau_ij(t)`: logical delay/staleness under a stated clock.
- `s`: maximum permitted staleness in a bounded-stale policy.
- `u_i(t)`: count/time of updates to component i; fairness constrains its gaps or limit behavior.
- `r(x)`: stated residual; `epsilon_abs`, `epsilon_rel`: stopping tolerances.
- `e`: run epoch; `g`: partition/ownership generation; `v_i`: component version.
- **active**: able to execute/generate relevant work; **passive**: currently unable to do so without receipt.
- **quiescent**: all participants passive and no relevant work/message remains in flight.

“Asynchronous” must always be qualified by the schedule, consistency, delay, failure, and stopping model.

## Mechanisms, Invariants, or Proof Structure

### Operator and synchronous proof

Define X, F, fixed point, norm/order, and assumptions. Prove existence/uniqueness as required and derive the synchronous error/residual bound. Check boundary cases `q=0`, `q` approaching 1, zero initial residual, invalid/NaN inputs, and nonunique fixed points.

### Schedule-admissibility proof

Map every implementation update to i, t, and read versions `tau_ij(t)`. Establish the theorem's atomicity, fairness, delay/freshness, loss/duplicate, step-size, and perturbation assumptions. Test that backpressure, failure, and repartition cannot silently break them.

### Protocol-safety proof

Epoch/partition/component/version identities prevent cross-run and stale-owner writes; ownership and update coverage hold; collective order and request/buffer lifetimes are legal; queue/resource bounds hold; duplicates/reordering obey the declared algebra; and numeric errors remain within the analysis.

### Stopping and quiescence proof

Show the evaluated residual represents an admitted global state and tolerance. Show no passive worker can later reactivate from an unaccounted message; termination credits/acknowledgements/snapshot invariants balance all generated work. Complete/cancel communication legally before exit/publication.

### Equivalence and performance evidence

On analytical and high-precision reference cases, validate fixed point/residual and allowed numerical difference across adversarial schedules. Then compare time-to-valid-solution, work, staleness, traffic, memory, energy, failures, and tails with identical goals. Roll back if evidence or assumptions fail.

## Alternatives and Trade-Offs

| Regime | Main benefit | Principal limitation |
|---|---|---|
| strict BSP | simple generations, residuals, checkpoints | straggler/latency waiting |
| nonblocking BSP | hides safe independent latency | progress and buffer complexity remain |
| pipelined iterations | several operations in flight | recurrence/numerical behavior may change |
| periodic synchronization | bounds drift and creates validation points | residual global stalls remain |
| bounded/stale synchronous | tolerates controlled stragglers | version/window and theorem required |
| fully asynchronous | maximum schedule flexibility | strongest proof/termination/operations burden |
| local asynchronous, global epochs | contains complexity by hierarchy | boundaries still bottleneck |
| task/dataflow runtime | activates only ready dependencies | runtime metadata/scheduling overhead |
| conservative synchronous fallback | auditable recovery/reference | may be slower |

Prefer the weakest synchronization that has a complete correctness and operations argument, not the least synchronization visible in source code.

## Failure Modes and Misconceptions

- **“A barrier is always waste.”** it may carry generation, lifetime, convergence, and checkpoint semantics.
- **“Nonblocking means asynchronous algorithm.”** overlap can preserve a synchronous recurrence.
- **“MPI collective completion is a barrier.”** completion semantics do not generally prove peer completion.
- **“Removing `Barrier` removes synchronization.”** dependencies and collectives may shift it elsewhere.
- **“Synchronous convergence proves asynchronous convergence.”** stale schedules need their own theorem.
- **“Bounded staleness is just a tuning parameter.”** it is a semantic assumption to enforce and observe.
- **“Atomic writes guarantee convergence.”** memory safety and mathematical convergence differ.
- **“Every component eventually runs, so the schedule is fair.”** required freshness and update-gap conditions may be stronger.
- **“Message arrival order is version order.”** networks, threads, retries, and epochs can reorder.
- **“Dropping intermediate updates is harmless.”** only if the operator/protocol proves coalescing safe.
- **“A local residual below tolerance means done.”** remote state or in-flight work can reactivate it.
- **“All queues empty means termination.”** observations are non-atomic and messages may be in flight.
- **“Lower iteration latency means faster convergence.”** measure time-to-valid-solution and total work.
- **“More updates mean more progress.”** stale or conflicting updates may add no contraction.
- **“Floating-point order only changes last bits.”** ill-conditioned/stopping-sensitive paths can amplify it.
- **“Ordinary MPI recovers a failed rank.”** failure semantics need an explicit supported design.
- **“Asynchrony tolerates unlimited memory.”** versions, queues, and requests require hard bounds.
- **“Tested schedules cover all schedules.”** testing complements, not replaces, proof assumptions.

## Worked Examples

### Example 1

**Synchronous contraction.** If `q=0.5` and initial error is at most 8, after k synchronous applications the bound is `8*(0.5)^k`; at k=4 it is 0.5. **Conclusion:** the bound follows from the specified recurrence and norm, not from iteration naming.

### Example 2

**Safe overlap.** A stencil posts generation-k halo receives/sends, computes cells independent of remote boundaries, waits, then computes boundaries into generation k+1. Buffers remain immutable until completion. **Conclusion:** latency is overlapped while generation semantics remain synchronous.

### Example 3

**Unsafe buffer reuse.** A rank starts a nonblocking all-reduce on `residual`, immediately stores the next local residual into the same buffer, and later waits. The buffer is accessed before completion. **Conclusion:** nonblocking syntax without lifetime discipline is incorrect.

### Example 4

**Bounded staleness.** Workers may be at most s=2 clocks apart. The runtime blocks a worker attempting clock k+1 while another remains below k-2 and reports observed age. **Conclusion:** the semantic bound must be enforced, not assumed from average latency.

### Example 5

**Starved component.** Components 1–9 update continuously while component 10 owns a necessary boundary and never runs. Queue throughput looks high but the fairness premise fails. **Conclusion:** system-wide activity is not convergence progress.

### Example 6

**Reordered epochs.** A delayed epoch-7 update arrives after restore has begun epoch 8. The receiver checks run/epoch/owner generation and rejects it. **Conclusion:** arrival freshness requires explicit identity.

### Example 7

**False local stop.** Rank 0 has residual zero and no queued work, but a message carrying rank 1's new boundary is in transit. A passive-plus-deficit protocol prevents termination. **Conclusion:** local silence is not quiescence.

### Example 8

**Misleading speed claim.** Async updates take 1 ms versus 4 ms synchronous rounds, but require 1,000 updates rather than 100 rounds and double messages. Compare complete validated wall time, resources, and error. **Conclusion:** normalize by the solved problem.

### Example 9

**Periodic validation.** An asynchronous solver pauses every 50 local updates, drains the epoch, recomputes a true residual collectively, checkpoints if valid, and resumes with a new epoch. **Conclusion:** strategic synchronization can bound operational risk.

### Example 10

**Regional power-grid state estimation.** Bounded-stale regional updates must preserve network/topology/measurement/time/units/calibration/model/partition epochs, observability, bad-data policy, residual meaning, numerical conditioning, deadline and missing-region behavior, cyber authorization, encrypted/audited traffic, rollback/reference comparison, and operator publication gates. Named power-systems/protection, numerical optimization, distributed/HPC, control/safety, cybersecurity/privacy, operations/site-reliability, data-quality/regulatory, ethics, accessibility/human-factors, and independent validation reviewers must approve the evidence; none is claimed here. **Conclusion:** faster convergence telemetry does not establish a valid grid state or safe control action.

## Cross-Program Connections

- **Algorithms:** fixed points, contraction, monotone dataflow, work-span, and adversarial schedules provide proof tools.
- **Architecture:** atomics, caches, NUMA, accelerators, and network offload determine update visibility and cost.
- **Operating systems:** scheduling tails, preemption, affinity, and progress threads shape delay/fairness.
- **Distributed systems:** epochs, snapshots, quiescence, duplicate suppression, and failure detectors recur.
- **Networks:** delay, reordering, loss, flow control, and collective topology influence staleness.
- **Numerical computing:** conditioning, residuals, step sizes, rounding, and convergence theory constrain schedules.
- **Databases/data engineering:** isolation, versioned state, streaming watermarks, and bounded lateness are close analogies.
- **Machine learning:** parameter servers and stale-synchronous policies trade waiting for controlled model age.
- **Testing/formal methods:** schedule exploration, invariants, model checking, and reference recomputation complement proofs.
- **Security/operations:** authenticated epochs, bounded queues, telemetry, checkpointing, and fail-closed publication make the method operable.

## References

1. Leslie G. Valiant, “A Bridging Model for Parallel Computation,” *Communications of the ACM* 33(8), 1990. <https://web.mit.edu/6.976/www/handout/valiant2.pdf>
2. Gérard M. Baudet, “Asynchronous Iterative Methods for Multiprocessors,” *Journal of the ACM* 25(2), 1978. <https://doi.org/10.1145/322063.322067>
3. Dimitri P. Bertsekas and John N. Tsitsiklis, *Parallel and Distributed Computation: Numerical Methods*, 1989. <https://www.mit.edu/~dimitrib/pdc.html>
4. Dimitri P. Bertsekas and John N. Tsitsiklis, “Convergence Rate and Termination of Asynchronous Iterative Algorithms,” 1989. <https://www.mit.edu/~jnt/Papers/C-89-rate_termination-Crete.pdf>
5. Paul Tseng, Dimitri P. Bertsekas, and John N. Tsitsiklis, “Partially Asynchronous, Parallel Algorithms for Network Flow and Other Problems,” *SIAM Journal on Control and Optimization* 28(3), 1990. <https://doi.org/10.1137/0328040>
6. Qirong Ho et al., “More Effective Distributed ML via a Stale Synchronous Parallel Parameter Server,” *NeurIPS 26*, 2013. <https://papers.nips.cc/paper_files/paper/2013/hash/b7bb35b9c6ca2aee2df08cf09d7016c2-Abstract.html>
7. Edsger W. Dijkstra and Carel S. Scholten, “Termination Detection for Diffusing Computations,” EWD687a, 1979. <https://www.cs.utexas.edu/~EWD/transcriptions/EWD06xx/EWD687a.html>
8. MPI Forum, *MPI: A Message-Passing Interface Standard, Version 5.0*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report.pdf>
9. MPI Forum, *MPI-5.0: Nonblocking Collective Operations*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node147.htm>
10. PETSc Team, *KSPSetConvergenceTest*, current documentation; retrieved 2026-08-29. <https://petsc.org/main/manualpages/KSP/KSPSetConvergenceTest/>

## Exercises

### Exercise 1

For a contraction with q=0.8 and initial error bound 10, derive the synchronous error bound after 8 iterations and the minimum k needed to make the bound at most 0.1. State which assumptions prevent directly applying this result to arbitrary stale execution.

### Exercise 2

Classify three designs: (a) nonblocking halo exchange followed by a wait before boundary use, (b) two generations of reductions in flight with exact version slots but unchanged recurrence, and (c) immediate component updates from bounded-age neighbor versions. Specify the extra proof and protocol obligations for each.

### Exercise 3

Design a distributed stopping protocol for an asynchronous graph propagation algorithm. Define local activity, messages/work in flight, residual/fixed-point validation, epochs, duplicates, reactivation, failure behavior, and publication.

### Exercise 4

Plan an experiment comparing strict BSP, periodic synchronization, and bounded staleness under heterogeneous nodes. Include fairness/delay enforcement, correctness oracles, schedules/faults, metrics, and a decision rule.

### Exercise 5

Transfer the framework to asynchronous multi-center radiotherapy dose optimization. Specify convergence, version, clinical-data, numeric, stopping, failure, privacy/security, validation, and publication invariants, plus named human review roles without claiming review.

## Answers to the Exercises

### Answer 1

The bound is `10*(0.8)^8=1.6777216`. Require `10*(0.8)^k<=0.1`, equivalently `0.8^k<=0.01`; `k>=ln(0.01)/ln(0.8)≈20.6377`, so minimum integer k is 21. This uses one stated contraction mapping, complete domain, fixed norm, exact synchronous applications, and initial bound. Arbitrary stale component mixtures may not equal F applied to x^k; fairness, freshness/delay, block norm, atomicity, and perturbation conditions need an asynchronous theorem.

### Answer 2

(a) is nonblocking BSP overlap if generation-k state remains immutable, requests progress/complete, buffers are not touched early, and all ranks preserve protocol order. The synchronous convergence proof remains, plus communication-lifetime evidence. (b) is pipelining: exact version slots prevent overwrite, but prove that initiation/completion order and any delayed reduced value preserve the intended recurrence; bound outstanding resources and drain on stop. (c) is a mathematically asynchronous iteration: map reads to `tau_ij`, enforce/measure age, atomicity and fairness, cite/prove convergence for F and the bound, version/deduplicate messages, and provide global residual/quiescence termination. All three need end-to-end numeric and performance validation.

### Answer 3

Assign immutable run and epoch plus component/owner versions. A worker is active while it has an unapplied admissible update or can generate one; it becomes passive only after emitting/accounting for all resulting work. Every sent work message creates a conserved credit/deficit cleared only after application or protocol-approved rejection/acknowledgement; duplicates carry IDs and cannot clear credit twice. A root/snapshot protocol declares candidate quiescence only when all workers are passive and total in-flight credit is zero. Freeze the epoch, drain/reject late traffic, then evaluate the declared global fixed-point/residual oracle; reactivation cancels the candidate. On process/channel failure, abort/restart from a validated checkpoint unless a separately proved recovery model restores credits, ownership, and fairness. Publish only after component coverage/version/digest and result validation.

### Answer 4

Use identical problem, F, precision, resources, initial state, tolerance, true/global residual, output oracle, and deadline. Implement strict rounds; periodic global validation every stated update window; and bounded-stale scheduling that blocks beyond s and records every component's age/update gap. Test balanced placement, calibrated slow workers, bursts/delays/reordering/duplicates allowed by the protocol, queue pressure, progress modes, and multiple schedules/seeds; include timeout/divergence. Measure time-to-valid-solution, useful and discarded updates, per-component fairness, staleness distribution, messages/bytes, memory/queues, synchronization/idle/progress/checkpoint time, residual trajectory, energy, failures, and numerical differences. Select only a regime whose theorem assumptions are enforced, all correctness/termination checks pass, and confidence-bounded wall-time/resource benefit exceeds complexity and recovery cost across representative cases.

### Answer 5

Fix patient/course/prescription/anatomy/contour/image/calibration/beam/model/optimizer/partition epochs, units and coordinate frames. State objective/constraints, conditioning, step-size and bounded-delay convergence theorem; enforce component fairness, atomic versioned updates, finite values/ranges, deterministic or bounded numeric policy, and true global dose/objective/constraint residual checks. Data access follows authorization/consent/locality/minimization, authenticated encrypted transport, bounded redacted telemetry, and audited retention. Termination requires globally validated residual/constraints and quiescence; missing centers, stale imaging, process/network failure, timeout, replay, checkpoint/rollback, and conservative synchronous fallback fail closed. Validate on independently curated reference cases, high-precision recomputation, adversarial schedules/delays/duplicates, restored runs, dose-volume and organ-at-risk constraints, uncertainty/sensitivity, security/privacy tests, and clinical workflow simulation. Publication/treatment use requires named radiation-oncology, medical-physics/dosimetry, numerical optimization, distributed/HPC, imaging/data-quality, privacy/security, operations, quality/regulatory, ethics, accessibility/human-factors, and independent validation reviewers. No external review, clinical validity, privacy guarantee, regulatory approval, or treatment authorization is claimed.
