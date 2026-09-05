---
module_id: ALGE-073
program: Algorithm Engineering
level: 2
module_number: 73
title: Online Scheduling
status: complete
last_verified: 2026-09-05
---

# Online Scheduling

## One-Page Review

### Governing question

How should arriving work be admitted, assigned, ordered, preempted, or rejected before future jobs are known, and which guarantees survive the timing, machine, and objective assumptions of the real service?

### Essential definitions

- A **job** $j$ has release time $r_j$, processing requirement $p_j$, and possibly deadline $d_j$, weight $w_j$, and eligible machines.
- A schedule is **online** when a decision affecting job service must be made before later jobs are revealed.
- **Clairvoyant** scheduling knows a released job's processing requirement; **non-clairvoyant** scheduling learns it only through service or completion.
- **Preemption** pauses and later resumes a job; **migration** resumes it on another machine. Each may be forbidden or costly.
- Completion time is $C_j$; flow time is $F_j=C_j-r_j$; lateness is $L_j=C_j-d_j$; tardiness is $T_j=\max(0,L_j)$.
- **Makespan** is $C_{\max}=\max_j C_j$; total weighted flow is $\sum_j w_jF_j$.
- **List scheduling** assigns each arriving job to a currently least-loaded identical machine.
- **EDF** selects the ready job with earliest absolute deadline in a preemptive uniprocessor model.
- **Admission control** accepts, delays, degrades, or rejects work before overload destroys existing commitments.
- **Resource augmentation** gives the online schedule explicitly more speed, machines, or capacity than its comparator.
- A **competitive guarantee** compares online cost with a same-model offline optimum on every legal arrival sequence.
- **Stability** requires backlog not to diverge under a declared arrival and service model; finite-trace quality alone does not establish it.

### Central model, mechanism, or theorem

For identical parallel machines, jobs arrive in list order with processing times known on arrival, assignments are immediate and nonpreemptive, and the objective is makespan. List scheduling on $m\ge1$ machines satisfies

$$
C_{\max}^{LS}\le\left(2-\frac1m\right)OPT.
$$

Let $j$ be the job finishing last, with processing time $p_j$ and start time $S_j$. Because it was assigned to a least-loaded machine, every machine had load at least $S_j$ then, so work before $j$ is at least $mS_j$. With total work $P$,

$$
S_j\le\frac{P-p_j}{m},\qquad
C_{\max}^{LS}\le\frac Pm+\left(1-\frac1m\right)p_j.
$$

Both $P/m\le OPT$ and $p_j\le OPT$, giving the ratio. The proof does not cover unknown processing times, unrelated machines, deadlines, queueing arrivals, or a different objective.

### Critical invariants

- Decisions use only released information and authorized predictions.
- Every job has one identity and is never silently lost, duplicated, or executed twice.
- Machine eligibility, capacity, affinity, precedence, and safety constraints hold after every transition.
- Work conservation is explicit: idling with ready eligible work occurs only for a declared policy reason.
- Remaining work never becomes negative; preemption and migration preserve completed work exactly.
- Deadline, cancellation, retry, and completion timestamps have one clock and ordering convention.
- Online and offline schedules share machines, speed, initial state, costs, and allowed actions unless augmentation is declared.
- Rejection, setup, migration, checkpoint, cleanup, and failed-attempt work are charged.
- Overload behavior preserves higher-priority commitments and reaches a tested fallback.
- Telemetry reconstructs release, queueing, dispatch, service, preemption, completion, cancellation, and outcome.

### Common failures

Typical failures are optimizing makespan when users care about flow time; treating processing times as known when they are estimates; letting a simulator see future arrivals; comparing preemptive online with nonpreemptive offline; omitting setup or migration cost; assuming EDF is universally optimal; using utilization averages to claim stability; hiding rejected and timed-out jobs; allowing retries to duplicate execution; starving large jobs to improve median latency; reporting speed augmentation as equal-resource performance; and applying a deterministic theorem after a learned priority score changes the policy.

### Compact example

Two identical empty machines receive processing times $2,3,7,1,4$. List scheduling produces loads $(2,0)$, $(2,3)$, $(9,3)$, $(9,4)$, then $(9,8)$, so makespan is 9. Total work is 17, hence every schedule needs at least $8.5$ time; the largest job also gives lower bound 7. A partition with loads 9 and 8 proves 9 is optimal for this instance. That empirical equality does not strengthen the worst-case theorem.

### Connections

[ALGE-071](./071-online-decisions-and-competitive-analysis.md) supplies adversaries and competitive semantics; [ALGE-072](./072-caching-and-paging-algorithms.md) shows another online resource-allocation problem. Operating Systems owns processor-scheduler mechanisms, and Distributed Systems owns lease, retry, and coordination semantics.

## Governing Question

Given jobs revealed over time, how do we define the information and action protocol, choose a scheduling objective, prove what a causal policy guarantees, and deploy it safely under overload, uncertainty, cancellation, and partial failure?

“Schedule the work” is not one problem. Immediate assignment for makespan, preemptive deadline feasibility, non-clairvoyant flow time, weighted fairness, energy-aware speed scaling, and admission under overload have different feasible actions and incompatible objectives. An algorithm name without its model is incomplete.

The engineering discipline is to bind every guarantee to job information, release semantics, machine environment, preemption, migration, objective, and adversary. Then test implementation and workload behavior separately. A proof protects only the model it proves; a trace benchmark estimates only the workload and system it observes.

## Why This Matters

Schedulers mediate scarce compute, workers, links, beds, vehicles, and machines. Their choices affect latency, throughput, deadlines, cost, fairness, energy, and failure containment. Under light load many policies look equivalent. Under bursts or sustained overload, queue dynamics amplify small priority choices into starvation and missed commitments.

Production adds uncertainty. Processing requirements may be unknown, jobs may fail or retry, machine speed may vary, affinity constrains placement, and deadlines may encode unequal consequences. Dispatch overhead and preemption can consume the capacity the model assumes. A scheduler optimized for mean completion may harm tail latency or systematically defer large or low-weight work.

A rigorous design therefore separates model, theorem, estimator, implementation, and policy. It provides admission and fallback rather than assuming every arrival can be served.

## Prerequisites and Retrieval

Retrieve [ALGE-071](./071-online-decisions-and-competitive-analysis.md), greedy algorithms, lower bounds, induction, competitive ratios, priority queues, queueing basics, and experimental design. Familiarity with clocks, concurrency, idempotency, and resource isolation is useful.

This chapter owns the general online scheduling contract, list-scheduling theorem, deadline-model boundaries, overload, predictions, fairness, and deployment evidence. Detailed operating-system scheduling, distributed job execution, and domain-specific workforce or transportation constraints remain with their owning programs.

## Learning Objectives

After completing this module, you should be able to:

1. specify release, information, action, and completion timing;
2. choose and distinguish makespan, flow, lateness, tardiness, throughput, and fairness objectives;
3. derive the list-scheduling makespan guarantee;
4. test theorem hypotheses against a proposed implementation;
5. distinguish clairvoyant, non-clairvoyant, preemptive, migratory, and augmented models;
6. explain EDF's scope without universalizing it;
7. design admission and overload policies with explicit consequences;
8. evaluate predictions, retries, setup, and transition costs;
9. build leakage-resistant trace, simulation, and shadow evidence; and
10. define operational invariants, telemetry, guardrails, and rollback.

## Core Exposition

### Write the scheduling protocol before the priority rule

For each job, specify when $r_j$, $p_j$, $d_j$, $w_j$, dependencies, and eligibility become known. At a decision event, define whether the scheduler may queue, assign, preempt, migrate, reject, replicate, or change speed. Define whether processing is divisible, whether setup depends on predecessor, and what cancellation does to completed work.

Event order matters. If a completion and release share a timestamp, decide which is processed first. Use a monotonic scheduling clock; wall-clock correction must not make service negative. A deterministic event sequence and tie rule make replay possible. Randomized tie-breaking needs a recorded stream.

Immediate dispatch is an online commitment even if execution begins later. Queueing preserves flexibility but adds delay. A global dispatcher can coordinate machines but becomes a bottleneck; local queues improve scalability while losing global load information. These are architectural changes to information and action, not implementation trivia.

### Choose the objective that represents the obligation

Makespan measures completion of the last job in a finite batch. It can ignore terrible latency for individual jobs. Total flow time rewards early completion and often favors short jobs. Maximum lateness protects the worst deadline deviation; total tardiness measures aggregate late work; throughput before deadlines may reject or abandon jobs. Weighted objectives encode declared priority but can starve low-weight work.

Multiobjective slogans obscure trade-offs. Use lexicographic requirements, explicit constraints, or a justified scalar loss. Hard safety and legality should normally remain feasibility gates. Report per-class and tail outcomes even when the optimizer uses an aggregate.

For continuing services, finite makespan may be meaningless. Study response-time distributions, backlog, throughput, and stability under an arrival process or adversarial load envelope. Little's law $L=\lambda W$ relates long-run averages only under stability and consistent population and time boundaries; it is not a scheduling optimality theorem.

### Derive list scheduling for makespan

Consider $m$ identical unit-speed machines and a finite list of jobs. Processing time $p_j\ge0$ is revealed when job $j$ arrives. Assignment is immediate, jobs are nonpreemptive, all machines can run every job, and the objective is makespan. List scheduling assigns to a machine with minimum assigned load, using a fixed tie rule.

Let last-finishing job $j$ start at $S_j$. At its assignment, its chosen machine had minimum load $S_j$, so all $m$ machines had load at least $S_j$. Hence the previously assigned work $P-p_j\ge mS_j$. Therefore

$$
C_j=S_j+p_j\le\frac{P-p_j}{m}+p_j
=\frac Pm+\left(1-\frac1m\right)p_j.
$$

Every schedule requires at least total-work average $P/m$ and at least the longest single processing time $p_j$, so both are at most $OPT$. Substitution gives $(2-1/m)OPT$. Zero-size jobs do not break the inequality. When $m=1$, the factor is 1.

The bound is tight for list scheduling. For $m=2$, jobs $1,1,2$ assigned in that order produce loads $(3,1)$ and makespan 3; offline groups the two unit jobs and assigns the size-2 job alone, obtaining 2, ratio $3/2=2-1/2$.

### Verify the mechanism without inflating the evidence

<!-- bijux-verify: {"id":"identical-machine-list-scheduling","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"jobs=(2, 3, 7, 1, 4) assignments=(0, 1, 0, 1, 1) loads=(9, 8) makespan=9\nworst_jobs=(1, 1, 2) loads=(3, 1) makespan=3 offline=2 ratio=1.500\nzero_job_loads=(0, 0)\ninvalid_machine_count=rejected\n","stderr":""}} -->
```python
def list_schedule(processing_times, machine_count):
    if machine_count < 1:
        raise ValueError("machine_count must be positive")
    loads = [0] * machine_count
    assignments = []
    for processing_time in processing_times:
        if processing_time < 0:
            raise ValueError("processing time must be nonnegative")
        machine = min(range(machine_count), key=lambda index: (loads[index], index))
        assignments.append(machine)
        loads[machine] += processing_time
    return tuple(assignments), tuple(loads)


jobs = (2, 3, 7, 1, 4)
assignments, loads = list_schedule(jobs, 2)
print(f"jobs={jobs} assignments={assignments} loads={loads} makespan={max(loads)}")
worst = (1, 1, 2)
_, worst_loads = list_schedule(worst, 2)
print(f"worst_jobs={worst} loads={worst_loads} makespan={max(worst_loads)} offline=2 ratio={max(worst_loads) / 2:.3f}")
_, zero_loads = list_schedule((0,), 2)
print(f"zero_job_loads={zero_loads}")
try:
    list_schedule(jobs, 0)
except ValueError:
    print("invalid_machine_count=rejected")
```

The executable evidence verifies deterministic assignments and boundary handling on CPython. It does not prove the ratio or optimality for arbitrary instances; the preceding derivation and independent checks address those claims.

### Know when list scheduling no longer applies

Uniform machines have different speeds but common job scaling; unrelated machines give each job-machine pair its own processing time. Eligibility, affinity, sequence-dependent setup, memory, accelerators, network locality, and co-scheduling make assigned load an incomplete state. A least-load rule can choose an infeasible or extremely slow machine.

Unknown processing times remove clairvoyance. Predictions can restore estimates but not truth. Preemption can improve flow or deadline behavior yet adds checkpoint, cache, and migration costs. Release times mean assigned load may include idle gaps or future reservations. Each extension requires a new analysis or bounded empirical claim.

### Bound deadline claims to their model

On one preemptive processor with independent jobs whose release times and deadlines are known when released, EDF is feasibility-optimal in the classical model: if any schedule can meet all deadlines, EDF can. The exchange argument replaces service of a later-deadline ready job with an earlier-deadline one without making the earlier job later; repeated exchanges align a feasible schedule with EDF.

This statement does not make EDF optimal for multiple processors, nonpreemptive jobs, precedence, setup, overload, unknown execution, or arbitrary value. Under overload, EDF can spend capacity on jobs that will miss anyway and cause feasible jobs to fail. Admission, overload shedding, or value-aware degradation needs separate policy and evidence.

Periodic real-time analysis adds release patterns and utilization tests. A utilization bound is conditional on task assumptions, execution-time bounds, deadlines, and overhead. Measured mean runtime is not a safe worst-case execution requirement.

### Treat non-clairvoyance as an information constraint

A non-clairvoyant scheduler knows a job has arrived but not its remaining processing requirement. Round robin or processor sharing avoids trusting an unknown size and supports fairness, but context switching and cache loss matter. Shortest-processing-time policies are unavailable without estimates.

Estimate-aware scheduling should record prediction time, features, uncertainty, and errors. A robust baseline limits damage when estimates are wrong. Large jobs mislabeled small can monopolize service; small jobs mislabeled large can starve. Evaluate error-conditioned outcomes and adversarial misprediction, not only average accuracy.

Attained service is causal and can support policies that favor jobs with little received work. It is not equivalent to knowing remaining work. A job's eventual duration must never appear in features used before completion.

### Design for overload, not only nominal utilization

When offered work persistently exceeds capacity, no scheduler can keep every queue bounded. Define the overload envelope and response: reject at admission, shed low-value work, degrade quality, reserve capacity, cap per-tenant concurrency, or escalate. Queueing everything converts admission failure into unbounded latency and memory.

Admission decisions need idempotency and authority. A rejected job must not reappear through automatic retry without cost and backoff. Reservations need expiration and reclamation. Priority protects critical work only if lower-priority work cannot consume all nonpreemptible resources.

Stability claims require assumptions about arrivals and service. Utilization below one is necessary in simple single-server models but may not be sufficient with dependencies, blocking, vacations, or unstable routing. Test bursts, correlated failures, and capacity loss.

### Make fairness and starvation explicit

Priority can represent consequence, but indefinite postponement is usually a failure unless declared. Define service shares, maximum wait, slowdown, or per-class objectives. Aging increases priority with wait; reservations guarantee a floor; fair queueing divides capacity according to weights. Each can reduce aggregate efficiency.

Mean flow time can favor short jobs while a few large jobs wait indefinitely in an open system. Report tails and age distribution by class. A low-weight tenant may still require a contractual minimum. Fairness definitions are policy choices with domain and legal review, not consequences of a generic scheduler theorem.

### Account for transitions and failures

Preemption saves flexibility only if checkpoints are correct and affordable. Charge pause, serialization, transfer, cache warming, and lost work. Some jobs hold external locks or perform irreversible actions and cannot be safely preempted. Replication can cut tails but multiplies compute and side effects unless execution is idempotent.

Distinguish job attempt from logical job. A timeout may leave an attempt running; immediate retry can duplicate work. Use leases or fencing where appropriate, deduplicate completion, and define ownership after scheduler failover. Cancellation is a state transition whose acknowledgement may race with completion.

Machine failure changes available capacity and may invalidate processing-time estimates. A recovered scheduler must reconstruct committed, running, and completed state before dispatching more work. Safe uncertainty can mean stop, probe, or route to a bounded fallback.

### Evaluate the whole scheduling service

Preserve arrival chronology, job groups, machine states, failures, cancellations, and offered load. Randomly shuffling jobs destroys burst and online semantics. Separate tuning, validation, and later test periods. Use exact or bounded offline comparators on tractable samples and label best-known schedules honestly.

Report objective, deadline attainment, rejection, per-class flow and slowdown, queue age, utilization, preemptions, migration, wasted work, energy, scheduler overhead, and tails. Include every job and attempt. Averages conditioned on completion hide starvation and timeout.

Simulation supports controlled counterfactuals only after its arrival, service, contention, and failure models are validated. Shadow scheduling can compute actions without executing them, but resource interference and policy-dependent future arrivals limit inference. Staged rollout needs load, deadline, fairness, and duplicate-execution guardrails plus immediate rollback.

## Definitions and Notation

For job $j$, $r_j$ is release, $p_j\ge0$ processing requirement, $d_j$ deadline, $w_j\ge0$ weight, $S_j$ start, and $C_j$ completion. Flow $F_j=C_j-r_j$, lateness $L_j=C_j-d_j$, and tardiness $T_j=\max(0,L_j)$. Makespan is $C_{\max}=\max_jC_j$.

$m$ is the number of machines, $P=\sum_jp_j$ total work, and $OPT$ the feasible same-model offline objective. A schedule is preemptive if service may pause, migratory if a resumed job may change machine, clairvoyant if released processing requirements are known, and work-conserving if it does not idle while eligible ready work exists unless policy requires it.

An **attempt** is one execution of a logical job. **Slowdown** commonly normalizes response by service requirement, but zero-size jobs need an explicit convention. **Overload** means offered work exceeds sustainable service under the declared horizon or stochastic model. **Speed augmentation** $s>1$ gives online machines $s$ units of service per unit time against unit-speed offline machines.

## Mechanisms, Invariants, or Proof Structure

### List-scheduling proof obligations

The last-finishing job exists for a finite list. Its assigned machine was minimum load. Every previously assigned job contributes to exactly one machine load, so $P-p_j\ge mS_j$. Average work and longest job are valid lower bounds for every identical-machine schedule. Combining them yields the ratio without assuming an arrival distribution.

### EDF exchange structure

At the first time a feasible schedule runs a ready later-deadline job while EDF chooses an earlier-deadline job, exchange an equal amount of service. The earlier deadline cannot be harmed; later service formerly assigned to the earlier job can serve the later one before its later deadline. Iteration aligns schedules. Release, preemption, one-processor, and independent-job premises are essential.

### Conservation and uniqueness

For each logical job, released work equals completed work plus remaining work plus explicitly abandoned work. Exactly one authoritative attempt may commit non-idempotent effects. Machine capacity is not double-booked. These invariants must survive retry, cancellation, failover, and clock races.

### Causal evidence boundary

At dispatch time $t$, decisions may use only events and predictions available by $t$. Offline optimum and eventual processing requirements are evaluation data, not features. Simulator and shadow results remain separate from executed causal outcomes.

## Alternatives and Trade-Offs

| Policy or model | Strength | Risk | Suitable setting |
|---|---|---|---|
| List scheduling | Simple, online makespan guarantee | Ignores sizes beyond current load and other objectives | Immediate assignment on identical machines |
| EDF | Classical single-processor feasibility optimality | Can behave poorly under overload or changed model | Preemptive independent deadline jobs |
| Shortest-job priority | Low flow time with known sizes | Estimation error and large-job starvation | Size-aware batch or guarded service |
| Processor sharing | Non-clairvoyant fairness | Context and cache overhead | Unknown sizes and divisible service |
| Weighted fair scheduling | Contractual shares | Can sacrifice aggregate objective | Multi-class or multi-tenant service |
| Admission and shedding | Preserves bounded commitments | Rejects or degrades work | Sustained or burst overload |
| Prediction-augmented | Exploits workload structure | Drift, poisoning, and leakage | Forecast-rich systems with robust fallback |
| Speed augmentation | Enables stronger theory | Unequal resources and incident fragility | Explicitly provisioned headroom |

Hybrid policies are common: per-class admission, EDF within critical work, fair sharing across tenants, and size-aware ordering within a pool. Analyze and test the composed policy, because local guarantees need not compose.

## Failure Modes and Misconceptions

- **“Online means jobs arrive through an API.”** A decision must precede relevant future information.
- **“Least load is always balanced.”** Eligibility, speed, setup, and reservations can make scalar load wrong.
- **“The list-scheduling ratio covers any objective.”** It is a makespan theorem under identical-machine assumptions.
- **“EDF always meets deadlines best.”** Its classical optimality has strict one-processor, preemptive, feasibility premises.
- **“Estimated size is known size.”** Prediction error changes both behavior and evidence.
- **“Preemption is free.”** State transfer, lost work, cache warming, and side effects can dominate.
- **“Utilization below 100% prevents queues.”** Variability, blocking, dependencies, and capacity loss matter.
- **“Completed-job latency represents all arrivals.”** Dropped, timed-out, and starved jobs must remain in denominators.
- **“Retries are new independent jobs.”** They may duplicate one logical operation and consume hidden work.
- **“Priority proves importance.”** Weights require governed meaning and starvation protection.
- **“Offline optimum is automatically comparable.”** It must share machines, actions, constraints, and costs.
- **“Rollback cancels dispatched effects.”** Irreversible or unfenced work may continue after policy rollback.

## Worked Examples

### Example 1

**Situation.** Two machines receive jobs $2,3,7,1,4$ in order.

**Reasoning.** List scheduling assigns to machines $(0,1,0,1,1)$ with final loads $(9,8)$. Total work is 17, so $OPT\ge8.5$; integrality gives at least 9, and the produced schedule attains 9.

**Conclusion.** List scheduling is optimal on this instance, although its theorem is a worst-case bound.

### Example 2

**Situation.** Two machines receive $1,1,2$.

**Reasoning.** The unit jobs split, then the size-2 job joins a unit load, producing $(3,1)$. Offline puts size 2 alone and both units together for makespan 2. Ratio $3/2$ meets the bound $2-1/2$.

**Conclusion.** Arrival order can make the list-scheduling bound tight.

### Example 3

**Situation.** A job has zero processing requirement.

**Reasoning.** It can complete at release without increasing load. Longest-job lower bounds permit zero, and total-work reasoning remains valid. Slowdown $F_j/p_j$ is undefined, so metrics need a zero-size convention.

**Conclusion.** Algorithmic feasibility survives, but normalized telemetry needs explicit boundary semantics.

### Example 4

**Situation.** A GPU-only job reaches the least-loaded CPU machine.

**Reasoning.** Classical list scheduling assumes every identical machine is eligible. Assigning by global scalar load violates feasibility. Restrict the candidate set to eligible resources and seek analysis for that machine model.

**Conclusion.** Eligibility is a model premise, not a post-dispatch validation detail.

### Example 5

**Situation.** On one preemptive processor, ready jobs have deadlines 8 and 12; the later-deadline job is running when the earlier arrives.

**Reasoning.** EDF preempts and serves deadline 8. Under classical assumptions, exchanging this service with later service cannot hurt the deadline-8 job and leaves the deadline-12 job a later window. Preemption overhead must be zero in that theorem.

**Conclusion.** EDF's exchange logic follows deadline order only within its declared model.

### Example 6

**Situation.** Offered work is 120 CPU-seconds per second against capacity 100.

**Reasoning.** No priority rule can serve all work indefinitely; backlog grows at least 20 CPU-seconds per second before overhead. Admission, degradation, or added capacity is necessary. Queueing everything delays failure rather than solving it.

**Conclusion.** Persistent overload is a feasibility problem, not a tuning problem.

### Example 7

**Situation.** A shortest-predicted-job policy estimates a 100-second job as one second.

**Reasoning.** The job can block many true short jobs if nonpreemptive. Cap uninterrupted service, use uncertainty-aware priority, or fall back to time sharing. Evaluate results conditional on underprediction severity.

**Conclusion.** Prediction needs robustness and bounded authority.

### Example 8

**Situation.** A timeout retries a payment job while the first attempt still holds a lease.

**Reasoning.** Two attempts may commit the same logical side effect. Preserve logical identity, fence stale owners, make commit idempotent where possible, and charge both attempts' consumed work. Scheduler completion and business commit are distinct states.

**Conclusion.** Retry correctness is part of scheduling state.

### Example 9

**Situation.** Median completed-job flow improves 20%, but the oldest queued job waits six hours.

**Reasoning.** Conditioning on completion hides starvation. Report all arrivals, queue-age tails, per-class outcomes, and censored waits. Add aging or service guarantees if policy forbids indefinite postponement.

**Conclusion.** Aggregate latency can improve while fairness and liveness fail.

### Example 10

**Situation.** A shadow scheduler shows fewer late jobs but assumes its choices do not change retries or later demand.

**Reasoning.** Shadow state can reproduce mechanical scheduling, but production actions may alter future arrivals. Validate simulator feedback, use bounded rollout where authorized, and retain workload and causal limitations. Tuning on shadow results requires a new confirmation window.

**Conclusion.** Shadow evidence is valuable but not automatically causal.

## Cross-Program Connections

- **Operating Systems:** preemption, priorities, affinity, interrupts, context switches, and run queues implement processor scheduling.
- **Distributed Systems Engineering:** leases, fencing, retry, duplicate execution, failover, and partial failure govern remote jobs.
- **Platform Engineering:** quotas, autoscaling, admission, multi-tenancy, and observability turn policy into a shared service.
- **Software Delivery and Reliability Engineering:** deadlines, overload, load shedding, rollback, and incident behavior define service risk.
- **Data Engineering:** chronological traces, lineage, grouped splits, and complete outcome ledgers protect evaluation.
- **Security Engineering:** adversarial arrivals, priority abuse, resource exhaustion, and prediction poisoning change the threat model.
- **Data Architecture Engineering:** weights, deadlines, and rejection costs need governed domain meaning.
- **Algorithm Engineering:** [ALGE-071](./071-online-decisions-and-competitive-analysis.md) supplies general competitive reasoning; ALGE-074 and ALGE-075 shift from decisions to bounded-memory stream summaries.

## References

1. Ronald L. Graham, “Bounds for Certain Multiprocessing Anomalies,” *Bell System Technical Journal* 45(9), 1966, 1563–1581. DOI: [10.1002/j.1538-7305.1966.tb01709.x](https://doi.org/10.1002/j.1538-7305.1966.tb01709.x). Primary source for list-scheduling makespan bounds; publisher record checked 2026-09-05.
2. Ronald L. Graham, “Bounds on Multiprocessing Timing Anomalies,” *SIAM Journal on Applied Mathematics* 17(2), 1969, 416–429. DOI: [10.1137/0117039](https://doi.org/10.1137/0117039). Primary source for refined multiprocessor scheduling analysis; publisher record checked 2026-09-05.
3. Michael L. Dertouzos, “Control Robotics: The Procedural Control of Physical Processes,” in *Information Processing 74*, North-Holland, 1974, 807–813. Historical primary source for earliest-deadline scheduling; bibliographic record checked 2026-09-05.
4. C. L. Liu and James W. Layland, “Scheduling Algorithms for Multiprogramming in a Hard-Real-Time Environment,” *Journal of the ACM* 20(1), 1973, 46–61. DOI: [10.1145/321738.321743](https://doi.org/10.1145/321738.321743). Primary source for classical real-time scheduling models; ACM record checked 2026-09-05.
5. Rajeev Motwani, Steven Phillips, and Eric Torng, “Nonclairvoyant Scheduling,” *Theoretical Computer Science* 130(1), 1994, 17–47. DOI: [10.1016/0304-3975(94)90151-1](https://doi.org/10.1016/0304-3975(94)90151-1). Primary source for scheduling without known processing times; publisher record checked 2026-09-05.
6. Frances Yao, Alan Demers, and Scott Shenker, “A Scheduling Model for Reduced CPU Energy,” *FOCS 1995*, 374–382. DOI: [10.1109/SFCS.1995.492493](https://doi.org/10.1109/SFCS.1995.492493). Primary source for speed scaling and energy-aware scheduling; IEEE record checked 2026-09-05.
7. Bala Kalyanasundaram and Kirk Pruhs, “Speed Is as Powerful as Clairvoyance,” *Journal of the ACM* 47(4), 2000, 617–643. DOI: [10.1145/347476.347479](https://doi.org/10.1145/347476.347479). Primary source for explicit speed augmentation; ACM record checked 2026-09-05.
8. David B. Shmoys, Joel Wein, and David P. Williamson, “Scheduling Parallel Machines On-Line,” *SIAM Journal on Computing* 24(6), 1995, 1313–1331. DOI: [10.1137/S0097539793248317](https://doi.org/10.1137/S0097539793248317). Primary reference for online parallel-machine scheduling; publisher record checked 2026-09-05.

## Exercises

### Exercise 1

For each objective—makespan, total flow, maximum lateness, weighted throughput—state what it rewards and give one behavior it can hide or worsen.

### Exercise 2

Prove the $(2-1/m)$ list-scheduling bound from the last-finishing job. Identify every premise and handle $m=1$ and zero-size jobs.

### Exercise 3

A scheduler evaluates shortest-job-first using final observed runtimes, drops timed-out jobs, and compares against a preemptive offline optimum although production is nonpreemptive. Diagnose the evidence failures and specify a corrected experiment.

### Exercise 4

Design an overload policy for a multi-tenant compute service. Specify admission, priorities, fairness, retries, cancellation, capacity loss, metrics, guardrails, and a safe fallback.

### Exercise 5

A hospital schedules uncertain-duration procedures across specialized rooms. Design a rigorous online model and evidence plan covering eligibility, setup, predictions, emergencies, safety, fairness, human authority, simulation, rollout, and conditions that invalidate the policy.

## Answers to the Exercises

### Answer 1

Makespan rewards finishing the finite batch early but can hide long waits within it. Total flow rewards early completions and can starve large jobs. Maximum lateness protects the worst deadline deviation but may sacrifice aggregate completion and ignores how many jobs are late. Weighted throughput rewards completed declared value before deadlines but can reject low-weight classes systematically. A complete service review reports the chosen objective plus tails, rejection, starvation, and per-class outcomes.

### Answer 2

Let $j$ finish last at $S_j+p_j$. At its immediate assignment to a least-loaded one of $m$ identical machines, every machine has load at least $S_j$, so $P-p_j\ge mS_j$. Hence $C_{\max}^{LS}\le P/m+(1-1/m)p_j$. Any feasible schedule has makespan at least $P/m$ and at least $p_j$, yielding $C_{\max}^{LS}\le(2-1/m)OPT$. Premises are finite nonnegative jobs, processing sizes known on arrival, immediate nonpreemptive assignment, identical eligible unit-speed machines, no setup, and makespan objective. For $m=1$, the factor is 1. Zero-size jobs preserve all inequalities and need no service.

### Answer 3

Final runtimes are unavailable at dispatch, so the evaluated policy is clairvoyant unless production has valid predictions. Dropping timeouts creates survivor bias and understates both load and latency. A preemptive comparator has more power than nonpreemptive production. Preserve chronological arrivals and every outcome, use only prefix-available estimates with acquisition cost, compare against a certified nonpreemptive same-machine offline solution or bound, and report censored waits, rejection, wasted attempts, tails, and estimator error. Freeze tuning before a later source-group test and label any best-known comparator.

### Answer 4

Reserve capacity floors per tenant or class, admit only when bounded queue and deadline forecasts allow, and shed optional work before committed work. Use explicit priorities with aging or maximum-wait protection. Give retries one logical identity, backoff, attempt caps, and fenced execution; cancellation must be acknowledged and reconciled with completion. Recompute budgets after machine loss and reduce admission immediately. Report all arrivals, acceptance, rejection, queue age, flow, deadline attainment, per-class shares, wasted work, and tail scheduler overhead. Guard memory, queue length, critical capacity, fairness, and duplicate commits. Fallback to conservative quotas and simple work-conserving queues when state or predictions are invalid.

### Answer 5

Define release when a case is ready, which duration distribution or estimate is then available, room and staff eligibility, setup and cleaning, nonpreemptibility, emergency arrivals, and objectives subordinate to clinical safety. Use uncertainty intervals and retain a conservative schedule with emergency reserve; prediction cannot override eligibility or safety. Define fairness and urgency with clinicians and governance rather than inferred weights. Validate on grouped historical periods without future-duration leakage, then in a simulator that models overruns, setup, cancellations, emergencies, and staff constraints; report simulator error. Use human approval and shadow recommendations before a bounded rollout with stop criteria. Log inputs, estimates, overrides, assignments, outcomes, and versions under privacy controls. New procedures, staffing, rooms, guidelines, patient mix, prediction drift, or safety events invalidate evidence and require review or rollback.
