## Slurm Deep Dive

## Module 01: Foundations — Scheduling Semantics, Requests, and the Debug Loop

### 01. Mental Model: Jobs, Steps, Allocations, Partitions, TRES

**Materials**

* Slurm as allocator + scheduler; allocations are the unit of truth
* Job vs step: `sbatch` creates an allocation; `srun` creates steps within it
* Partitions/QOS/accounts/constraints as policy surfaces
* TRES as the common language for requests, enforcement, and accounting
* Hierarchical resource accounting (including mode-style aggregation where enabled)

**Lab**

* Objective: map workloads → correct allocation model
* Tools: `sinfo`, `squeue`, `scontrol show job`
* Outcome: 6 minimal “correct request” recipes (CPU, GPU, MPI, array, interactive, mixed)

### 02. Observability: Pending → Root Cause → Fix

**Materials**

* Minimal toolkit: `sinfo`, `squeue`, `sprio`, `sacct`, `scontrol show job/node`
* Pending reasons and priority components; backfill and walltime economics
* Runtime triage signals when exposed by the site (controller/node readiness probes)

**Lab**

* Objective: diagnose pending/slow/wrong-placement jobs from scheduler evidence only
* Tools: `squeue -o …`, `sprio -j`, `scontrol show job`, `sacct -j`
* Outcome: a “reason → fix” table for 8 common failure modes

### 03. Correct Requests: CPU, Memory, Time, GPUs, Segments

**Materials**

* CPU semantics: `--ntasks` vs `--cpus-per-task` vs `--nodes`
* Memory semantics: `--mem` vs `--mem-per-cpu`; interpreting OOM and MaxRSS
* Time realism: why over-requesting hurts scheduling outcomes
* GPUs: `--gpus*` / `--gres=gpu` / `--gpus-per-task`; TRES reservations and common traps
* Segmented/spread/consolidate-style behaviors where supported
* Energy/power-related TRES if the site tracks it

**Lab**

* Objective: repair incorrect requests and justify every flag
* Tools: `sacct --format=AllocTRES,Elapsed,MaxRSS,State,…`
* Outcome: 5 rewritten requests + a short “why this is minimal and correct” note each

### 04. Placement and Binding: CPU/GPU Affinity, NUMA, Topology

**Materials**

* CPU binding: `--cpu-bind`, `--hint`, `--distribution`, `--exclusive`
* NUMA locality: memory bandwidth cliffs; multi-socket pitfalls
* GPU locality: CPU↔GPU pairing; multi-GPU placement
* Topology diagnostics using site-exposed cache/NUMA settings when available

**Lab**

* Objective: prove a placement issue and fix it
* Tools: `srun` + a micro-benchmark; `sacct` for CPUTime/MaxRSS; optional topology tools if available
* Outcome: before/after measurements and the minimal binding change that explains them

### 05. Interactive vs Batch: Debug → Harden

**Materials**

* `salloc` + `srun` for interactive runs that respect allocations
* Converting interactive success into a hardened `sbatch` template
* Interactive hygiene: cgroup behavior, startup checks, deterministic environment snapshots

**Lab**

* Objective: debug interactively, then ship a production script
* Tools: `salloc`, `srun`, `scontrol show job`
* Outcome: a clean batch template + reproducibility footer (env + key Slurm vars)

---

## Module 02: Job Engineering — Scripts, Steps, Arrays, Containers, Reliability

### 01. `sbatch` Script Anatomy (Auditable, Deterministic)

**Materials**

* Strict mode, explicit failure policy, atomic outputs, cleanup discipline
* Logging: job-id keyed logs + metadata footer (AllocTRES, account/QOS, limits)
* Environment discipline: modules, `--export`, `--chdir`, stable paths

**Lab**

* Objective: turn a brittle script into a reviewable template
* Tools: shellcheck (optional), `sacct` fields for footer validation
* Outcome: a “gold standard” script template used as team baseline

### 02. Containers in Slurm (Apptainer/Singularity + Site Isolation)

**Materials**

* Containers as the environment contract
* Binds, caching, I/O mounts, GPU enablement; permission and path contracts
* Site isolation mechanisms (namespaces/container plugins) and implications
* Optional GPU IMEX/channel-style considerations if your site uses them

**Lab**

* Objective: run a containerized GPU job that is provably correct
* Tools: `apptainer exec`, `srun`, `nvidia-smi` (if GPUs), `sacct AllocTRES`
* Outcome: verified CPU pinning + GPU visibility + correct binds + clean logs

### 03. Steps and Coordination (`srun` Inside Jobs)

**Materials**

* Why `srun` matters: cgroups, affinity, GPU binding, accounting, step isolation
* Multi-step jobs: stage → compute → collect without races
* Coordination patterns; async/fast reply behaviors where supported

**Lab**

* Objective: refactor a pipeline into resource-correct steps
* Tools: `srun` step boundaries + per-step logs; `sacct -j <job>.batch,<job>.<step>`
* Outcome: step-structured job with measurable resource separation

### 04. Arrays at Scale (Throughput Without Cluster Damage)

**Materials**

* Deterministic sharding via `SLURM_ARRAY_TASK_ID`; idempotent outputs
* `%` concurrency controls; fairshare and filesystem pressure implications
* Per-task logs; rerun subsets; stable manifests

**Lab**

* Objective: build an array runner that supports partial reruns safely
* Tools: `--array`, `%`, per-task logs; `sacct` to detect stragglers
* Outcome: array template + manifest + “rerun failed IDs only” procedure

### 05. Failure Handling: Signals, Timeouts, Requeue, Checkpointing

**Materials**

* `SIGTERM` handling; early warning via `--signal`; safe checkpoint writes
* Requeue strategy: when to requeue, when not to; expedited modes where available
* Accounting/limits interactions with retries; avoiding infinite failure loops

**Lab**

* Objective: simulate termination and prove restart safety
* Tools: `--signal`, forced termination, `--requeue` policies, checkpoint files
* Outcome: checkpoint-aware template + proof of no corruption/duplication

---

## Module 03: Performance + Policy + Production Operations

### 01. Performance Model: Granularity, Scaling, Oversubscription

**Materials**

* Throughput vs latency workloads; arrays vs big allocations
* Scheduler overhead economics: job explosion, micro-tasks, step inflation
* Measuring inefficiency via `sacct` and cluster telemetry exports when available (OpenMetrics/Prometheus)

**Lab**

* Objective: tune granularity using evidence, not guesses
* Tools: `sacct` + (optional) metrics queries
* Outcome: a sizing heuristic (tasks/partition sizes/steps) justified by measured results

### 02. Composability: Slurm as Backbone for Distributed Systems

**Materials**

* Launching Dask/Ray inside allocations: lifecycle, teardown, failure modes
* Choosing the right layer: pure Slurm vs workflow engine vs distributed framework
* Config distribution patterns (how code/config reaches every node/task)

**Lab**

* Objective: bootstrap a small distributed cluster from one allocation
* Tools: `salloc`/`sbatch`, hostlists, per-node logs
* Outcome: a “bootstrap + run + teardown” template with failure-safe cleanup

### 03. MPI and Multi-Node Jobs: Correct Launch, Correct Debug

**Materials**

* `srun` launcher patterns; rank/task mapping and host distribution
* Failure modes: rank mismatch, environment mismatch, PMIx/fabric issues, port conflicts
* Debug method: reduce → isolate → scale; logging discipline

**Lab**

* Objective: run minimal MPI, inject one failure, produce a clean postmortem
* Tools: `srun`, `scontrol show hostnames`, `sacct`, per-rank logs
* Outcome: MPI template + a diagnostic checklist that works under pressure

### 04. I/O Under Load: Data Locality and Staging

**Materials**

* Shared FS bottlenecks: metadata storms, tiny files, contention
* Node-local scratch staging: stage-in/out patterns; cleanup guarantees
* Compression tradeoffs; per-job I/O limits if enforced by the site

**Lab**

* Objective: reduce FS pressure and prove it with measurements
* Tools: staging scripts + `sacct` elapsed/CPU + FS counters if available
* Outcome: staging template + “when to compress” rule-of-thumb

### 05. Policy, Accounting, Security, Telemetry, Templates

**Materials**

* Fairshare/QOS/backfill/preemption: interpreting `sprio` + pending reasons
* Enforcement: OOM/time limits/cgroups; reading evidence via `sacct`
* Security hardening realities: auth boundaries, isolation categories where present, safe secrets
* Telemetry standards: metrics export, job completion hooks, dashboards, alerting basics
* Upgrade/migration hygiene: deprecations, site changes, template stability
* Federated/multi-cluster awareness (what changes conceptually, what doesn’t)

**Deliverables**

* Team-grade templates: CPU, GPU, MPI, array, containerized, distributed bootstrap
* Triage checklists: pending, OOM, slow, wrong placement, node failure, FS meltdown
* Example metric queries + a minimal “job efficiency” dashboard spec
