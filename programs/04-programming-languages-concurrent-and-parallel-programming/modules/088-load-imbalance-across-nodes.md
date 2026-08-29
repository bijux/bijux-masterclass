---
module_id: CONPAR-088
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 88
title: Load Imbalance Across Nodes
status: complete
last_verified: 2026-08-29
---

# Load Imbalance Across Nodes

## One-Page Review

### Governing question

How can a parallel program identify why some ranks reach synchronization later, distinguish true work imbalance from hardware, communication, and measurement effects, and rebalance only when predicted critical-path savings exceed migration and ongoing overhead?

### Essential definitions

- **load** is resource demand assigned to a worker over a stated interval; it can include compute, memory, communication, I/O, or accelerator work.
- **work imbalance** means required useful work differs across ranks.
- **time imbalance** means observed phase duration differs; it may reflect work, speed, contention, skew, or blocking.
- **arrival skew** is the distribution of times ranks reach a synchronization or collective.
- **imbalance factor** `I=max_r L_r / mean_r L_r` compares the critical rank with average modeled/observed load.
- **load-balance efficiency** `eta=mean/max=1/I` under a barrier-like phase model.
- **idle/wait area** sums `T_max-T_r` across ranks and exposes wasted rank-time under a common completion.
- A **weight model** predicts entity/task cost; **online timing** estimates it from measurements.
- **static balancing** chooses a mapping before an interval; **dynamic balancing** migrates work during execution.
- **migration cost** includes partitioning, synchronization, transfer, rebuilding, cache/device warming, and lost locality.
- **hysteresis** requires sustained benefit beyond a margin before remapping, preventing oscillation.
- **heterogeneous capacity** means equal work is not equal time across different cores/nodes/devices.

### Central model, mechanism, or theorem

For a barrier-delimited phase with per-rank duration `T_r`, critical time is `T=max T_r`; ideal equalized time cannot be below average work divided by effective capacity and other serial/communication constraints. Measured `I_T=max T/mean T` and `eta_T=mean/max` diagnose a bound, not a cause. A rebalance is economically justified over horizon H only if `(T_before-T_after)*H` exceeds measurement, partition, migration, rebuild, and added communication costs with uncertainty and risk margins, while ownership/numerical invariants remain unchanged.

### Critical invariants

All ranks measure the same named phase/generation; clocks and instrumentation limitations are known; useful work, communication wait, I/O, and synchronization are separated; counts/weights and timers use comparable units; critical/max and full distributions—not only averages—are retained; hardware allocation, affinity, frequency, NUMA, device, and co-tenant state are recorded; proposed remapping preserves unique ownership, dependencies, memory capacity, boundary conditions, and deterministic/numeric policy; migration is generation-atomic and validated; and rebalancing activates only with bounded frequency and positive measured amortized benefit.

### Common failures

Teams infer imbalance from barrier time alone, count entities with unequal costs, average away stragglers, synchronize timers in ways that create the skew being measured, compare ranks on heterogeneous devices as if identical, ignore network/I/O contention, fix compute balance while increasing cut/halo/FFT cost, rebalance on one noisy sample, migrate too often, retain stale ghosts and indexes, overwrite the last good mapping, or claim lower modeled imbalance as end-to-end speedup without full validated timing.

### Compact example

Phase times `[10,10,10,18,12,10,10,10]` ms have mean 11.25, maximum 18, imbalance 1.6, efficiency 0.625, and wait area 54 rank-ms (37.5% of an `8*18` rank-time rectangle). A candidate `[12,12,11,12,11,12,11,11]` has maximum 12 and imbalance 1.043478 despite slightly more aggregate work. With 36 ms migration cost and 6 ms saved per iteration, the nominal break-even is six future iterations.

### Connections

[Domain Decomposition](084-domain-decomposition.md) supplies weighted partitions and safe migration. [Communication-Computation Overlap](086-communication-computation-overlap.md) distinguishes exposed wait from useful work. [Parallel I/O](087-parallel-i-o.md) shows metadata/storage skew. The [program roadmap](../ROADMAP.md) next compares barrier-delimited bulk-synchronous iterations with bounded asynchronous alternatives.

## Governing Question

Which rank/resource lies on the critical path, which causal component makes it late, what mapping/schedule change can reduce that component without increasing another bottleneck or changing results, and over what measured horizon will the change repay its complete transition cost?

Balance is not equal entity count. It is a controlled reduction of critical-path resource demand under correctness, capacity, locality, and migration constraints.

## Why This Matters

At a barrier, collective, halo boundary, or output phase, fast ranks wait for the slowest. As scale grows, small variations in data, branches, adaptive refinement, particles, sparse degrees, device speed, memory placement, OS noise, network congestion, filesystem access, or co-tenancy can dominate efficiency.

Imbalance also moves over time. A shock front, active graph frontier, particle cluster, adaptive mesh, variable token sequence, or sparse nonlinear region shifts work among ranks. Static partitioning can be ideal initially and poor later.

Blind balancing can make performance worse and correctness fragile. Moving entities costs bandwidth and rebuilds halos, solver data, device state, and I/O layouts. Compact parts can become fragmented; a balanced compute phase can overload communication or memory. Sound engineering measures causal components, uses stable weights and hysteresis, validates migration, and evaluates full iterations over a repayment horizon.

## Prerequisites and Retrieval

Retrieve:

- stable identities, weighted graph/spatial partitions, ownership generations, migration, cut and memory objectives from [Domain Decomposition](084-domain-decomposition.md);
- halo/neighbor bytes, boundary time, generation validity, and conservation from [Halo Exchange and Stencil Computation](085-halo-exchange-and-stencil-computation.md);
- critical paths, arrival skew, progress, resource contention, and measurement from [Communication-Computation Overlap](086-communication-computation-overlap.md); and
- collective max/sum reductions and ordering from [Collective Communication](083-collective-communication.md).

Retrieval prompt: name the phase and generation; per-rank useful compute, communication, waiting, I/O, accelerator, and overhead; entity/task counts and cost features; hardware capacity/affinity/frequency/NUMA/device; neighbor bytes/degrees/cut; memory high water; arrival times; timer/trace method; candidate mapping and hard constraints; migration/rebuild cost; expected horizon/uncertainty; correctness oracle; and rollback trigger.

## Learning Objectives

After completing this module, a learner can:

1. distinguish work, time, communication, memory, I/O, hardware, and arrival imbalance;
2. compute max/mean imbalance, load-balance efficiency, wait area, distributions, and break-even horizons;
3. instrument phases without confusing collective waiting with causal work;
4. build and validate count-, feature-, history-, and capacity-weighted cost models;
5. choose static repartitioning, dynamic migration, task scheduling/stealing, replication, or algorithm changes;
6. preserve ownership, dependency, memory, numeric, and restart invariants across migration;
7. design thresholds, hysteresis, cooldowns, and bounded rebalancing frequency;
8. diagnose heterogeneous/NUMA/device/network/I/O and system-noise causes;
9. compare full validated before/after timelines over an amortization horizon; and
10. scope scientific, operational, security, and high-stakes human review.

## Core Exposition

### Define the phase and causal categories

Measure an interval with a clear start and end in the algorithm: local force computation, sparse traversal, halo exchange, reduction arrival, checkpoint write, or full iteration. If ranks start the interval at different times, a local duration may hide arrival history; if they end at a collective, elapsed time may include waiting. Trace both arrival and work where possible.

Decompose time into useful computation, packing/copies, communication progress/transfer, explicit synchronization/wait, I/O, runtime/scheduling, and instrumentation. “MPI time” is not automatically communication cost: an early rank in `Allreduce` may wait for late local computation. Conversely, compute time can include memory stalls, frequency throttling, page migration, or device queue waits.

Use multiple signals: entity/task counts and features, instructions/cycles, CPU/GPU active time, memory bandwidth/cache/NUMA traffic, bytes/messages, I/O requests, queue and device timelines, and phase traces. No single counter proves causality. A roofline or resource saturation analysis can show why equal operation counts take different time.

### Metrics and their limits

For nonnegative comparable loads `L_r`, average `L_bar=sum L_r/P`, maximum `L_max`, imbalance `I=L_max/L_bar`, and balance efficiency `eta=L_bar/L_max`. These emphasize the critical rank. Coefficient of variation, percentiles, min/max, histogram, spatial/node grouping, and temporal series reveal whether one outlier or a broad distribution dominates.

For a phase that finishes when all ranks reach a common end, wait area `A=sum_r(T_max-T_r)` is potential idle rank-time. Normalized `A/(P*T_max)=1-mean/max` under this simplified model. It is not automatically recoverable: dependencies, communication, heterogeneity, or indivisible tasks may prevent perfect balance.

The maximum possible speedup from perfect balancing of that isolated phase is bounded by `T_max/T_ideal`; using average as ideal yields I, but assumes conserved aggregate work, homogeneous capacity, no overhead, arbitrary divisibility, unchanged communication, and no other critical path. State those assumptions.

For heterogeneous capacity `c_r`, compare normalized work `L_r/c_r` or assign target load proportional to capacity, subject to memory and topology. Capacity can be phase-specific: one GPU is faster for dense kernels but slower for branches; one node has different memory bandwidth or thermal behavior.

### Executable imbalance model

This deterministic exact-data Python model computes timing imbalance, efficiency, wait area, and a nominal migration break-even for one before/after sample. It does not measure hardware, infer cause, migrate work, model uncertainty, or prove performance.

<!-- bijux-verify: {"id":"load-imbalance-metrics","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"before_times_ms=[10, 10, 10, 18, 12, 10, 10, 10]\nbefore_mean_ms=11.250000\nbefore_max_ms=18\nbefore_imbalance=1.600000\nbefore_efficiency=0.625000\nbefore_wait_area_rank_ms=54\nbefore_idle_fraction=0.375000\nafter_times_ms=[12, 12, 11, 12, 11, 12, 11, 11]\nafter_mean_ms=11.500000\nafter_max_ms=12\nafter_imbalance=1.043478\nafter_efficiency=0.958333\nafter_wait_area_rank_ms=4\nafter_idle_fraction=0.041667\ncritical_path_saved_ms=6\nmigration_cost_ms=36\nnominal_break_even_iterations=6\n","stderr":""}} -->
```python
before = [10, 10, 10, 18, 12, 10, 10, 10]
after = [12, 12, 11, 12, 11, 12, 11, 11]


def metrics(times):
    average = sum(times) / len(times)
    maximum = max(times)
    wait_area = sum(maximum - value for value in times)
    return average, maximum, maximum / average, average / maximum, wait_area, wait_area / (len(times) * maximum)


before_metrics = metrics(before)
after_metrics = metrics(after)
print(f"before_times_ms={before}")
print(f"before_mean_ms={before_metrics[0]:.6f}")
print(f"before_max_ms={before_metrics[1]}")
print(f"before_imbalance={before_metrics[2]:.6f}")
print(f"before_efficiency={before_metrics[3]:.6f}")
print(f"before_wait_area_rank_ms={before_metrics[4]}")
print(f"before_idle_fraction={before_metrics[5]:.6f}")
print(f"after_times_ms={after}")
print(f"after_mean_ms={after_metrics[0]:.6f}")
print(f"after_max_ms={after_metrics[1]}")
print(f"after_imbalance={after_metrics[2]:.6f}")
print(f"after_efficiency={after_metrics[3]:.6f}")
print(f"after_wait_area_rank_ms={after_metrics[4]}")
print(f"after_idle_fraction={after_metrics[5]:.6f}")
saved = before_metrics[1] - after_metrics[1]
migration_cost = 36
print(f"critical_path_saved_ms={saved}")
print(f"migration_cost_ms={migration_cost}")
print(f"nominal_break_even_iterations={(migration_cost + saved - 1) // saved}")
```

### Model work rather than count it blindly

Entity counts work when cost is nearly uniform. Stencil cells may differ at material interfaces; particles differ by neighbor count or force model; graph vertices differ by active degree; adaptive elements differ by polynomial order; sequences differ by length; rays differ by intersections. Choose features tied to the kernel's work and validate their predictive error.

Static weights come from known algorithmic complexity or calibrated microcosts. Online weights use recent phase time distributed back to entities/tasks, hardware counters, sampling, or exponentially weighted histories. Timing-derived per-entity weights can be confounded when a rank's time includes communication or all entities share one average. Avoid positive feedback: a slow node should not label its entities intrinsically expensive if the node is the cause.

Separate compute weights, memory footprint, communication edges, migration size, and device eligibility. Multi-constraint partitioners or schedulers can enforce per-rank capacities while minimizing cut. A scalar weighted sum hides hard constraints; reject mappings that exceed memory, require unsupported devices, split inseparable groups, or violate data placement.

Validate a weight model on held-out intervals/partitions: compare predicted and measured per-rank phase times, rank ordering, maximum, residuals by feature/node, and stability over time. Refit or choose a simpler robust proxy when it drifts.

### Diagnose hardware and system heterogeneity

Equal work can take unequal time because ranks are placed on different CPU generations, frequencies, NUMA domains, GPU models/MIG slices, network links, or storage paths. Even nominally identical nodes differ through thermal throttling, power caps, correctable errors, memory channel state, and background services.

Record scheduler allocation, hostname/node/rank mapping, CPU/GPU model, core/NUMA/device affinity, thread counts, frequency/power state, memory placement, NIC locality, and runtime settings. Run per-node calibrated kernels and bandwidth tests carefully; a diagnostic should not become the production workload. Compare repeated jobs and rank-to-node permutations.

Co-tenancy and OS noise create intermittent tails. One slow sample is insufficient. Use distributions and time series; correlate with scheduler/node telemetry when authorized. If the same physical node remains slow after data rotation, suspect capacity/system effects. If slowness follows data, suspect work.

NUMA imbalance occurs when one rank/thread reads remote pages or shares controllers. First-touch/allocation policy, migration, and affinity matter. GPU imbalance includes unequal kernel occupancy, copy staging, stream serialization, and device throttling. Hybrid MPI/thread mappings can reduce rank-level imbalance while creating thread imbalance inside ranks; trace both levels.

### Communication and synchronization imbalance

Different neighbor counts, bytes, path congestion, collective trees, and protocol thresholds can make equal compute arrive or finish differently. A partition that equalizes compute may increase separator, high-degree ranks, or all-to-all hot spots. Record per-peer bytes/messages and post/complete times, not only total MPI time.

Collectives reveal arrival skew. Before a blocking collective, record the end of causal local work; measure collective exit separately. A max reduction of phase time gives a global critical value, but a gather/distribution or trace is needed to locate shape and nodes. Avoid inserting a barrier solely for timing unless the production phase already has that semantics; it can alter schedules and conceal natural skew.

Asynchronous overlap can hide some communication but cannot remove a late producer on the critical dependency. Load balance often creates a larger useful-overlap window and less collective waiting. Conversely, aggressive dynamic scheduling can make message timing nondeterministic and reduce aggregation.

I/O imbalance arises from unequal bytes, chunk sharing, aggregators, metadata, compression ratio/CPU, and storage paths. Separate arrival at I/O, data processing, storage calls, sync, and close. A slow collective write can be a late-rank compute problem.

### Choose a balancing mechanism

Static spatial/graph repartitioning is best when the distribution is stable for many iterations. Adjust Cartesian cuts, recursive coordinate bisection, space-filling-curve ranges, or graph/hypergraph partitions using validated weights. Preserve compactness and communication objectives.

Dynamic repartitioning follows moving work but pays repeatedly. Use thresholds, consecutive-window confirmation, a benefit margin, cooldown/minimum residence time, and maximum frequency. Predict horizon until the next likely distribution change. If a front crosses rapidly, by the time migration completes the estimate may be stale.

Task queues, guided scheduling, and work stealing balance fine irregular tasks without moving the entire domain, provided tasks are movable and data locality/side effects permit. They add scheduler/synchronization/nondeterminism. Hierarchical scheduling first balances across nodes/devices, then within node.

Replicating read-only work/data can let any rank help but increases memory and merge/deduplication requirements. Overdecomposition creates more partitions/tasks than workers, improving scheduling flexibility at metadata/halo overhead. Algorithmic changes—sparse frontier compaction, communication avoidance, adaptive tolerance, local aggregation—may reduce imbalance at its source but require separate correctness/numerical review.

### Economic decision and hysteresis

Let measured/predicted critical times be `T_b` and `T_a`, one-time transition cost M, added steady overhead delta, and remaining horizon H. Benefit is roughly `H*(T_b-T_a-delta)-M`. Require a positive confidence lower bound and safety margin, not a point estimate. Include partition calculation, synchronization, migration, serialization, buffer allocation, halo/index/communicator/device rebuild, cache warming, checkpoint effects, and validation.

Break-even `ceil(M/(T_b-T_a-delta))` requires positive denominator and stationary estimates. Add hysteresis: trigger only above an upper imbalance/benefit threshold for k windows, and do not reverse until a lower threshold/cooldown. Cap migration bytes and keep the previous generation recoverable until validation.

Sometimes accept imbalance. A 3% tail may cost less than migration; an indivisible task sets a floor; changing a partition near job end cannot repay. Record the decision and evidence rather than chasing `I=1`.

### Migration correctness

Use the generation-atomic protocol from domain decomposition: freeze or version updates, calculate mapping, preflight capacities, transfer authoritative state and dependent metadata, validate global counts/ID digests/conservation, rebuild ghosts/adjacency/solver/device/I/O plans, then activate. Reject old-generation messages and deduplicate retries.

Changing the mapping can change floating reduction order, local iteration order, random stream consumption, and convergence. Preserve counter-based/global-ID randomness and define reproducibility/tolerance policy. Compare partition-independent outputs and continued trajectory. A performance improvement that changes the scientific problem is invalid.

Failure during migration must leave old committed state or a restart path. Ordinary MPI recovery may be unavailable; define abort/checkpoint/restart. External effects use generation/idempotency keys. Do not publish partial ownership.

### Measurement experiment

Establish a warm representative baseline across multiple repetitions and placements. Retain input/workload, P/nodes/threads/devices, decomposition, mapping, affinity, versions/config, and instrumentation. Measure phase per-rank distributions plus full iteration/end-to-end time and output.

Rotate mappings or replay fixed data to distinguish rank, data, and node. Use coordinate/entity IDs and deterministic test schedules where possible. Perturb density/frontier/adaptation, co-tenancy where controlled, network/I/O load, progress/polling, and device placement. Avoid optimizing one synthetic phase that is not the production critical path.

For candidates, report predicted versus measured weights, imbalance metrics, communication/cut/degree, memory, migration/rebuild cost, cooldown, break-even, and realized horizon. Plot/retain timeline distributions before, during, and after transition. Require the full validated objective to improve with uncertainty.

### Security, operations, and high-stakes limits

Load metrics may reveal sensitive activity, user populations, geographic density, patient cohorts, or anomalous events. Minimize labels, aggregate/redact, control traces/dumps, set retention, and secure migration/checkpoints. Weight inputs and partition requests are denial surfaces; validate bounds and quotas.

In production monitor phase maxima/distributions, arrival skew, wait area, per-rank work/memory/bytes, node/device health, migration frequency/bytes/failures, predicted/realized payback, and rollback. Alert on sustained causal evidence, not one outlier. Preserve reproducible mapping/config history for incident analysis.

High-stakes domains require domain/numerical/safety review of any dynamic mapping or algorithm change. Balanced execution cannot establish model validity, fairness, or safe decisions.

## Definitions and Notation

- `P`: participating ranks/workers.
- `L_r`: modeled useful load of rank r; `L_bar=sum L_r/P`.
- `T_r`: measured named-phase duration for rank r.
- `L_max`, `T_max`: critical maximum load/time.
- `I_L=L_max/L_bar`, `I_T=T_max/T_bar`: imbalance factors.
- `eta_L=1/I_L`, `eta_T=1/I_T`: simplified balance efficiencies.
- `A_wait=sum_r(T_max-T_r)`: wait/idle area under a common phase end.
- `c_r`: phase-specific capacity of worker r.
- `M`: complete one-time measure/partition/migrate/rebuild/validate cost.
- `delta`: added per-iteration overhead after balancing.
- `H`: remaining stable horizon.
- `g`: ownership/mapping generation.
- `pi_g`: entity-to-owner map for generation g.
- `Obs`: partition-independent result and performance objective.

Time imbalance is an observation; causal work imbalance is one hypothesis among several.

## Mechanisms, Invariants, or Proof Structure

### Measurement-validity proof

All ranks measure identical phase semantics/generation; timers and clock correlation are adequate for each derived metric; instrumentation overhead is bounded; arrival, useful work, communication/wait, I/O, and hardware state are separately observable. Max/distribution and mapping-to-node evidence are retained.

### Cause and weight proof

Rotate data/mapping or use controlled replays to test whether slowness follows entities, rank, node, device, or communication path. Validate weight predictions against held-out per-rank times and residuals. Do not infer intrinsic entity cost from confounded rank time.

### Candidate-constraint proof

New mapping covers every entity once, respects memory/device/placement/inseparable constraints, and bounds cut/neighbor/migration resources. Predicted critical time uses capacity-normalized weights and includes communication/overhead, not counts alone.

### Migration/equivalence proof

State and metadata move exactly once under g to g+1; ghosts/indexes/requests/restart layouts rebuild; global counts/digests/conservation and numerical/reference results pass; new generation activates atomically and stale traffic is rejected.

### Amortization evidence proof

Under stated horizon/stationarity assumptions, lower-confidence benefit `H*(T_b-T_a-delta)-M` is positive. Full before/transition/after validated measurements confirm realized payback; hysteresis/cooldown bound oscillation and failure risk.

## Alternatives and Trade-Offs

| Approach | Main benefit | Principal limitation |
|---|---|---|
| equal entity count | simple/static | ignores cost and capacity |
| static weighted partition | low runtime scheduling overhead | weights/distribution can drift |
| dynamic spatial/graph repartition | follows moving work | migration/rebuild and cut changes |
| overdecomposition + scheduler | flexible mapping | metadata/halo/scheduling cost |
| work sharing/stealing | balances unpredictable tasks | locality, synchronization, nondeterminism |
| heterogeneous target weights | matches capacity | phase-specific calibration |
| replication | any worker can serve work | memory and merge/deduplication |
| algorithm redesign | removes source of imbalance | correctness/numerical change |
| accept measured imbalance | avoids transition risk | leaves bounded idle time |

Choose against the complete critical path and stable horizon, with correctness/capacity constraints first.

## Failure Modes and Misconceptions

- **“Barrier time is communication time.”** it often includes arrival skew from prior work.
- **“Equal counts mean balance.”** costs, memory, degrees, and devices differ.
- **“Mean time represents scalability.”** the maximum controls a barrier-delimited phase.
- **“Imbalance factor proves cause.”** it measures dispersion under assumptions.
- **“All wait area is recoverable.”** dependencies and indivisible work set floors.
- **“One slow rank means bad data partition.”** hardware, placement, contention, and noise can follow the node.
- **“A barrier improves timing accuracy.”** it changes the schedule and can hide natural arrival.
- **“Measured per-rank time is an entity weight.”** shared/confounded costs require attribution.
- **“Perfect compute balance is optimal.”** communication, memory, I/O, and migration also matter.
- **“Dynamic balancing should run frequently.”** thrashing can erase gains.
- **“Lower modeled imbalance means speedup.”** complete validated iterations decide.
- **“Migration only moves primary data.”** ghosts, indexes, solvers, devices, and I/O plans rebuild.
- **“The new map preserves identical bits.”** reduction/order/random changes need policy.
- **“The fastest node should own equal work.”** capacity-proportional targets may be correct.
- **“Noise can be optimized away after one sample.”** use distributions and sustained evidence.
- **“Balanced execution proves model validity.”** scientific and safety validation remain independent.

## Worked Examples

### Example 1

**Count mismatch.** Ranks own equal cells, but one material region performs ten chemistry reactions per cell. Timing follows material, not count. Weight by validated reaction cost. **Conclusion:** choose features tied to work.

### Example 2

**Barrier misdiagnosis.** Rank 0 spends 20 ms in all-reduce, while rank 7 arrives 18 ms late from local work. The collective transfer is not 20 ms. **Conclusion:** trace arrival and completion separately.

### Example 3

**Node-following straggler.** Rotating partitions leaves the same host slow. Frequency telemetry shows throttling. Quarantine/remap the node or capacity-weight it. **Conclusion:** test whether slowness follows data or hardware.

### Example 4

**Cut regression.** Weighted repartition lowers compute max 30%, doubles halo bytes, and raises iteration time 5%. Reject or include edge weights. **Conclusion:** optimize the whole critical path.

### Example 5

**Indivisible floor.** One task costs 40 ms and all others total 80 ms across eight ranks. No mapping can reduce maximum below 40 without splitting the task. **Conclusion:** imbalance can be algorithmic/granularity-limited.

### Example 6

**Premature trigger.** One noisy sample crosses 1.2; migration costs 100 iterations of expected savings. Consecutive-window/horizon policy declines. **Conclusion:** require amortized sustained benefit.

### Example 7

**Oscillating front.** A moving hot region causes mappings to alternate every ten steps. Hysteresis, predictive motion weights, or overdecomposed tasks reduce thrash. **Conclusion:** balance dynamics, not snapshots.

### Example 8

**GPU heterogeneity.** Equal batches on different GPU models yield unequal time. Capacity-proportional batches equalize completion but memory limits cap the faster device. **Conclusion:** weights and hard capacities coexist.

### Example 9

**Numerical drift after migration.** Results differ within tolerance because reduction and iteration order changed; global-ID random streams remain stable. Record the policy and validate error/convergence. **Conclusion:** performance transformations include numerical evidence.

### Example 10

**Wildfire evacuation ensemble.** Dynamic work must preserve scenario/weather/road/population/time/model generations, units, uncertainty, privacy for mobility/health data, deterministic/bounded numeric policy, deadline and missing-member behavior, restart/audit, and publication gates. Named wildfire/meteorology, transportation/emergency-management, geospatial, statistics/numerical/HPC, privacy/security, operations, quality/regulatory, ethics, accessibility/human-factors, and independent validation reviewers must approve evidence; none is claimed here. **Conclusion:** balanced ensemble completion does not establish forecast quality, equitable evacuation policy, or safety.

## Cross-Program Connections

- **Algorithms:** scheduling, bin packing, graph partitioning, approximation, granularity, and work stealing formalize balance.
- **Architecture:** NUMA, bandwidth, frequency, accelerators, and power explain unequal time.
- **Operating systems:** affinity, scheduling, noise, co-tenancy, and telemetry create/diagnose tails.
- **Networks:** neighbor degree, congestion, topology, and collective arrival shape communication imbalance.
- **Distributed systems:** shard skew, hot keys, rebalancing, epochs, and migration recur.
- **Databases/data engineering:** skewed joins, adaptive execution, repartitioning, and stragglers are analogous.
- **Numerical computing:** adaptive refinement, nonlinear convergence, reduction order, and tolerance constrain movement.
- **Testing:** fixed replays, mapping rotation, perturbation, and fault injection distinguish cause.
- **Security/privacy:** density and timing telemetry can disclose sensitive activity.
- **Operations:** node health, sustained alerts, rollback, realized payback, and mapping provenance sustain jobs.

## References

1. MPI Forum, *MPI: A Message-Passing Interface Standard, Version 5.0*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report.pdf>
2. MPI Forum, *MPI-5.0: All-Reduce*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node138.htm>
3. MPI Forum, *MPI-5.0: Environmental Inquiries and MPI_WTIME_IS_GLOBAL*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node247.htm>
4. LAMMPS Project, *balance Command*, current documentation; retrieved 2026-08-29. <https://docs.lammps.org/balance.html>
5. LAMMPS Project, *fix balance Command: Dynamic Load Balancing*, current documentation; retrieved 2026-08-29. <https://docs.lammps.org/fix_balance.html>
6. LAMMPS Project, *Measuring Performance*, current documentation; retrieved 2026-08-29. <https://docs.lammps.org/stable/Speed_measure.html>
7. LAMMPS Project, *Distributed-Grid Remapping for Load Balancing*, current documentation; retrieved 2026-08-29. <https://docs.lammps.org/stable/Developer_grid.html>
8. PETSc Team, *PetscPartitionerDMPlexPartition*, PETSc 3.25 documentation; retrieved 2026-08-29. <https://petsc.org/release/manualpages/DMPlex/PetscPartitionerDMPlexPartition/>
9. PETSc Team, *DMPlex: Partitioning and Ordering*, PETSc 3.25 documentation; retrieved 2026-08-29. <https://petsc.org/release/manual/dmplex/>
10. p4est Project, *p4est_partition: Weighted Forest Partitioning*, current API documentation; retrieved 2026-08-29. <https://p4est.github.io/api/p4est-latest/p4est_8h.html>

## Exercises

### Exercise 1

For phase times `[8,9,9,10,20]` ms, compute mean, max/mean imbalance, efficiency, wait area, idle fraction, and the isolated perfect-balance speedup bound. State why it may be unattainable.

### Exercise 2

Design an experiment to distinguish whether a persistent slow rank is caused by its data, its physical node, NUMA placement, or communication degree. Include rotations, controls, and evidence.

### Exercise 3

A candidate reduces critical compute from 40 to 28 ms but raises communication from 8 to 14 ms. Migration/rebuild costs 600 ms; added monitoring costs 1 ms/iteration; 100 stable iterations remain. Decide using an explicit model and uncertainty caveats.

### Exercise 4

Design a dynamic load-balancing protocol for adaptive particles on heterogeneous CPU-GPU nodes, including cost/capacity features, thresholds/hysteresis, mapping constraints, migration, numeric/restart validation, and telemetry.

### Exercise 5

Transfer the framework to a multi-hospital outbreak-risk ensemble with uneven cohorts and strict deadlines. Specify causal measurements, balancing and privacy/clinical/failure invariants, validation, publication gates, and named human reviewers without claiming review.

## Answers to the Exercises

### Answer 1

Sum 56, mean `11.2`, maximum 20. `I=20/11.2=25/14≈1.785714`; efficiency `11.2/20=0.56`. Wait area is `(12+11+11+10+0)=44` rank-ms; idle fraction `44/(5*20)=0.44`, equal to `1-0.56`. If aggregate work were conserved/divisible on homogeneous workers with no communication/overhead, ideal time is 11.2 and phase speedup bound `20/11.2≈1.785714`. Indivisible tasks, dependencies, capacity differences, communication, migration, and changed work make this unattainable in general.

### Answer 2

Use a fixed deterministic workload and trace named phase, arrivals, useful compute, bytes/degree, hardware counters, affinity/frequency/NUMA/device state. Run: same mapping repeatedly; rotate data partitions across ranks/nodes; keep data fixed but rotate rank/node placement; bind memory locally versus deliberately remote; and replay a calibrated compute/memory kernel. Keep P, input, versions, threads, and network traffic comparable. Slowness following data/features supports work imbalance; following physical node supports hardware/system; following NUMA binding supports placement; correlating with neighbor bytes/paths supports communication. Use distributions and multiple allocations, quantify instrumentation overhead, and avoid claiming causality from one correlation.

### Answer 3

Before full phase is `40+8=48` ms; after is `28+14+1=43` ms, nominal saving 5 ms/iteration. Over 100 iterations gross saving 500 ms, less than 600 ms migration, so net is -100 ms; do not rebalance under point estimates. Break-even is `ceil(600/5)=120`, beyond the stable horizon. This assumes compute/communication add rather than overlap, estimates remain stationary, and no other phases/correctness costs change. Use confidence bounds and full iteration measurements; uncertainty only strengthens declining unless it plausibly creates a positive lower-bound benefit.

### Answer 4

Features include particle interaction/neighbor/model cost, memory and migration bytes, spatial edges, device eligibility, recent deconfounded time, and node CPU/GPU/bandwidth capacities. Hard constraints cover device memory, required models, spatial/placement/privacy groups, and maximum neighbors; objectives minimize capacity-normalized critical load plus communication/migration. Trigger after k windows whose lower-confidence projected benefit exceeds complete transition cost by a margin; enforce cooldown, upper/lower hysteresis, byte/frequency caps, and horizon prediction. Version/freeze state, compute g+1, preflight capacities, transfer stable-ID particle/model/random/control state, rebuild spatial/ghost/device/I/O plans, verify counts/digests/conservation/reference/numeric policy, then atomically activate or roll back/restart. Monitor per-node phases/arrivals/resources, predicted/measured load, cut/bytes/memory, migration/rebuild, mapping generations, payback, failures, and output validity.

### Answer 5

Measure separately cohort/model-feature work, accelerator time, communication/collective arrival, I/O, and site/network constraints; normalize for approved capacity without exposing patient attributes. Stable pseudonymized cohort/model/time/scenario IDs define work; constraints enforce consent/authorization/locality, minimum cohort/privacy rules, memory/deadline, and clinically approved algorithm. Migration or task reassignment must preserve schema/units/missingness/weights, random/numeric policy, model/consent generation, deduplicated aggregation, audit, encrypted channels, bounded telemetry, failure/partial-site and fallback behavior. Validate multiple skews/sites/failures/deadlines, independent statistical/clinical references, privacy attacks/access controls, restart, fairness/subgroup results, and complete before/after latency with uncertainty. Publication requires named epidemiology/infectious-disease, biostatistics, clinical, privacy/security, federated-systems/HPC, operations, data-governance, quality/regulatory, ethics, accessibility/human-factors, and independent validation reviewers. No external review, clinical validity, privacy guarantee, or approval is claimed.
