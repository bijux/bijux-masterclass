---
module_id: CONPAR-081
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 81
title: Processes and Ranks in Distributed-Memory Programs
status: complete
last_verified: 2026-08-29
---

# Processes and Ranks in Distributed-Memory Programs

## One-Page Review

### Governing question

How should a distributed-memory program name, partition, place, initialize, coordinate, observe, and terminate processes when each process owns private state and a rank has meaning only inside a communication context?

### Essential definitions

- A **process** is an executing program instance with a private address space and runtime resources.
- **Distributed memory** means one process cannot ordinarily dereference another process's ordinary pointers; data crosses processes through communication or explicit shared mechanisms.
- A **group** is an ordered set of processes.
- A **communicator** combines a group with a communication context that separates message spaces.
- A **rank** is a process's integer index in one communicator, from zero through size minus one.
- **SPMD** (single program, multiple data) runs the same program image across processes whose control/data may differ by rank.
- The MPI **World Model** initializes a process set containing `MPI_COMM_WORLD`; the **Sessions Model** explicitly constructs groups/communicators from process sets for component-scoped use.
- **Allocation** grants nodes/CPUs/memory/devices; **mapping** assigns processes to nodes; **ranking** orders their ranks; **binding** restricts processes/threads to processing resources.
- A **local index/domain** is owned by one rank; a **global index/domain** is the logical problem namespace.
- A **root** is a rank selected for one operation; rank zero is not universally a coordinator or authority.
- **Thread-support level** states which thread patterns may call MPI; it must be requested and checked.
- **Collective termination** means all relevant processes satisfy lifecycle requirements before finalization; failure of one process can affect the whole MPI job depending on implementation/error model.

### Central model, mechanism, or theorem

Define the application as processes with private state, communicator-relative identities, and an explicit global-to-local ownership function. For block partitioning N items over P ranks, quotient `q=floor(N/P)` and remainder `r=N mod P` assign `q+1` items to ranks `<r` and q to the rest; prefix starts create complete, nonoverlapping half-open intervals. Correctness additionally requires all ranks call valid MPI operations in a compatible lifecycle/order, communicate within matching contexts, preserve buffer lifetimes, and handle launch/resource/exit behavior explicitly. Process count and placement are inputs, not hidden constants.

### Critical invariants

Every MPI object is used only between its initialization/creation and release/finalization; every rank is interpreted with its communicator; global ownership covers each item exactly once or by a declared replication rule; ordinary pointers never cross address spaces as usable remote addresses; communicator construction and collective calls involve compatible participants/order; rank-conditional branches do not strand required collectives; thread support is at least the pattern used; local buffers remain valid through communication completion; mapping/binding and device selection respect allocated resources; paths, configuration, seeds, and outputs are rank-safe; errors/exit codes from every process are observed; and results do not depend on stdout order, rank-to-node accident, or simultaneous progress unless specified.

### Common failures

Teams treat rank as global identity, assume rank zero runs on a particular node, conflate ranks with cores/nodes/GPUs, hard-code process count, partition with dropped remainders, share raw pointers, let one rank skip a collective, call MPI from unsupported threads, initialize/finalize inside an uncoordinated library, free nonblocking buffers early, oversubscribe cores, assign every local rank to GPU zero, let all ranks overwrite one file, trust interleaved stdout, use hostnames as stable topology, ignore launcher exit aggregation, call ordinary MPI after finalization, or assume one failed rank can be retried independently without a fault-tolerance design.

### Compact example

Seventeen global items partitioned contiguously over four communicator ranks give counts `[5,4,4,4]` and half-open ranges `[0,5)`, `[5,9)`, `[9,13)`, `[13,17)`. The intervals cover every item exactly once regardless of which nodes host ranks. This proves the arithmetic mapping only—not MPI launch, communication, scheduling, or failure behavior.

### Connections

[Heterogeneous CPU-GPU Pipelines](079-heterogeneous-cpu-gpu-pipelines.md) distinguishes resource placement and task identity. [Work Partitioning and Granularity](045-work-partitioning-and-granularity.md) supplies decomposition principles. [Happens-Before Relations](023-happens-before-relations.md) supplies ordering vocabulary. The [program roadmap](../ROADMAP.md) next introduces point-to-point and collective communication.

## Governing Question

For each process, communicator, and logical datum, what identity and ownership apply, where is the process placed and bound, which runtime lifecycle governs it, and what evidence shows the application remains correct for supported process counts and launch environments?

Distributed programs fail when local facts are mistaken for global ones. A rank number has meaning only relative to a communicator; a pointer has meaning only in its process; a node allocation is not a rank ordering; and launcher completion is not automatically a scientifically valid result.

## Why This Matters

MPI-style process decomposition scales beyond one shared address space and provides isolation from ordinary data races. It also makes communication, data distribution, replicated state, environment, file output, failure, and process placement explicit engineering concerns.

The first distributed module establishes identity and lifecycle before send/receive. If ranks, communicators, ownership, or launch semantics are vague, later message matching and collectives become folklore. A rigorous program runs correctly at one rank, non-power-of-two counts, uneven data sizes, heterogeneous nodes, and changing placement—within its declared support.

## Prerequisites and Retrieval

Retrieve:

- liveness, termination, fairness, and progress from [Safety, Liveness, and Progress](004-safety-liveness-and-progress.md);
- task identity, CPU/NUMA/device placement, backpressure, and failure from [Heterogeneous CPU-GPU Pipelines](079-heterogeneous-cpu-gpu-pipelines.md);
- race freedom, ordering, and lifecycle edges from [Happens-Before Relations](023-happens-before-relations.md); and
- task identity and dependency structure from [Task Parallelism and Dependency Graphs](041-task-parallelism-and-dependency-graphs.md).

Retrieval prompt: for one planned run, record allocation, launcher, executable/config hash, process count, communicators, rank/group membership, host/local rank, CPU/memory/device binding, global-to-local ownership, thread-support request/result, working directory/environment, output namespace, error policy, and termination path. Which are MPI semantics, launcher policy, scheduler allocation, or application assumptions?

## Learning Objectives

After completing this module, a learner can:

1. distinguish processes, nodes, sockets, cores, hardware threads, accelerators, communicators, groups, and ranks;
2. explain private address spaces and why raw pointers are not portable cross-process references;
3. use communicator-relative rank/size to write process-count-parametric SPMD control;
4. derive block and cyclic global-to-local ownership including uneven and empty partitions;
5. distinguish World, Sessions, and dynamic-process concerns without mixing object families incorrectly;
6. manage MPI initialization, thread support, communicator/object lifetime, and finalization;
7. separate scheduler allocation from launcher mapping, ranking, binding, and local device selection;
8. design rank-safe configuration, files, logging, randomness, errors, and exit aggregation;
9. verify single/multiple/non-power-of-two ranks, placement, oversubscription, and failure boundaries; and
10. scope reproducibility, security, operations, and high-stakes review for distributed runs.

## Core Exposition

### Private processes and explicit communication

Each MPI process has ordinary language state—globals, heap, stack, file descriptors, threads—independent from other processes. Equal virtual addresses do not identify shared storage. Sending a pointer value normally sends an integer-like address meaningful only in the source process; communicate the pointed-to data or a stable logical identifier instead.

Processes can reside on one node or many. Same-node implementations may optimize messages with shared memory, but program semantics should use the communication contract. Hybrid programs may intentionally create MPI processes plus threads/shared windows/device memory; each layer needs its own ownership and synchronization proof.

SPMD does not mean identical execution. All processes start the same program, then rank, local data, configuration, and messages select work. Rank-conditional control is safe only when every collective/communication protocol retains compatible participants and order.

### Communicators make ranks meaningful

A communicator carries an ordered group and context. If communicator C has size P, each member has one rank `0..P-1` in C. The same process can have different ranks in C and a subcommunicator D, or be absent from D. Therefore store/transport the communicator with any rank-relative data; `(communicator,rank)` is the meaningful name.

Communication contexts prevent unrelated libraries/protocols from matching each other's messages even when source, destination, and tags resemble one another. Duplicate or split communicators to isolate components, teams, topology partitions, or algorithms. Release them collectively as specified and do not use `MPI_COMM_NULL`.

Rank zero has no intrinsic host, speed, storage, or leadership property. Selecting it as a root is conventional and sometimes convenient; ensure root-specific memory/work is bounded and supported. A subcommunicator's rank zero may be a different world rank.

Ranks are also poor durable identifiers for records, checkpoints, random streams, and external effects when process count or communicator construction may change. Prefer stable domain keys—global cell, sample, partition generation, or task identifier—and maintain an explicit mapping to current owners. Then a restart with a different P can repartition without renaming scientific/business objects. If an output format stores rank for provenance, also store run ID, communicator construction, world/local membership, P, partition function, and stable object identity.

Communicator reordering is legal in APIs that permit it and can improve topology placement. Code that assumes a Cartesian or graph communicator preserves world ranks defeats that flexibility. Query ranks and coordinates from the created communicator. Likewise, compare groups through MPI's group operations or recorded membership, not by comparing rank numbers from different contexts.

A protocol shared by libraries should accept a communicator parameter rather than capture `MPI_COMM_WORLD`. This supports subteams, tests, composed applications, and multiple independent instances. Duplicate the caller's communicator when private context isolation is needed, document collective construction/destruction, and return errors without unilaterally finalizing the caller's MPI environment.

### World and Sessions lifecycle

In the World Model, call `MPI_Init` or `MPI_Init_thread`, then use `MPI_COMM_WORLD` until `MPI_Finalize`. Check the provided thread level: single, funneled, serialized, or multiple according to the binding. Requesting a level does not guarantee it; code must reject, degrade, or adapt.

`MPI_Finalize` is not a substitute for application protocol completion, and after it only explicitly permitted queries/functions may be used. Ensure outstanding communications and MPI objects follow their completion/release rules. All required processes must reach a compatible shutdown path; an early ordinary process exit can disrupt peers.

Sessions let components initialize MPI resources and build groups/communicators from process sets without assuming `MPI_COMM_WORLD`. They address composability and initialization limits, but introduce explicit object provenance. Do not mix Sessions-derived and World/dynamic-derived objects in calls where the standard forbids it. Libraries should document ownership rather than secretly initializing/finalizing application-wide MPI.

MPI dynamic process functions can connect/spawn processes where supported, but resource allocation is largely external to MPI. They do not imply elastic scheduler capacity or transparent fault recovery.

### Partitioning global domains

For N items and P>0 ranks, write `N=qP+r`, `0<=r<P`. Give ranks k<r count `q+1`, otherwise q. Start is `kq+min(k,r)` and end=start+count. Starts are prefix sums, adjacent intervals meet, the first starts zero, and final end is N: exact complete nonoverlap.

When N<P, the first N ranks own one item and the rest zero. Zero-count ranks still participate in required communicators/collectives with valid buffer/count semantics. Do not exit early just because local work is empty.

Cyclic ownership assigns global i to rank `i mod P` with local index `floor(i/P)`. It can balance periodic/variable costs but hurts contiguous locality. Block-cyclic combines chunks with cycling. Graphs/meshes need domain decomposition, halos, and explicit ownership/replication. Record the function so checkpoints and outputs reconstruct global identity independent of placement.

### Executable block-partition model

This deterministic Python model enumerates a block distribution and reduction oracle. It does not start processes, call MPI, communicate, model topology, or establish distributed correctness/performance.

<!-- bijux-verify: {"id":"rank-block-partition","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"items=17\nranks=4\ncounts=[5, 4, 4, 4]\nstarts=[0, 5, 9, 13]\nrank_0=[0, 1, 2, 3, 4]\nrank_1=[5, 6, 7, 8]\nrank_2=[9, 10, 11, 12]\nrank_3=[13, 14, 15, 16]\nlocal_sums=[15, 30, 46, 62]\nglobal_sum=153\nreference_sum=153\ncomplete=True\nnonoverlapping=True\n","stderr":""}} -->
```python
items = 17
ranks = 4
quotient, remainder = divmod(items, ranks)
counts = [quotient + (1 if rank < remainder else 0) for rank in range(ranks)]
starts = [rank * quotient + min(rank, remainder) for rank in range(ranks)]
partitions = [list(range(start, start + count)) for start, count in zip(starts, counts)]
local_sums = [sum(index + 1 for index in partition) for partition in partitions]
flattened = [index for partition in partitions for index in partition]

print(f"items={items}")
print(f"ranks={ranks}")
print(f"counts={counts}")
print(f"starts={starts}")
for rank, partition in enumerate(partitions):
    print(f"rank_{rank}={partition}")
print(f"local_sums={local_sums}")
print(f"global_sum={sum(local_sums)}")
print(f"reference_sum={sum(range(1, items + 1))}")
print(f"complete={sorted(flattened) == list(range(items))}")
print(f"nonoverlapping={len(flattened) == len(set(flattened))}")
```

### Allocation, mapping, ranking, and binding

A scheduler grants resources; a launcher starts tasks within that allocation. Mapping chooses nodes, ranking assigns communicator ranks relative to mapped processes, and binding constrains processes/threads to CPUs or locality domains. Defaults vary with implementation, site configuration, allocation, and version. Record explicit launch options and reported placement.

One rank per node, core, socket, NUMA domain, or GPU are different designs. `--ntasks`, node count, CPUs-per-task, process placement, and binding must agree with local threading. A multithreaded rank bound to one CPU oversubscribes itself. Too many ranks can duplicate memory and contend; too few may underuse resources.

For GPUs, derive device choice from launcher-provided local rank plus visible-device mapping only under a documented policy; local rank names position among processes on a node, not a universal device ordinal. Check visible devices, affinity/topology, sharing policy, memory, and failures. Never let every process select physical device zero accidentally.

### Rank-safe configuration, files, and randomness

Launch environments may differ in working directory, filesystem visibility, environment propagation, network interfaces, limits, and temporary storage. Version the executable/config and validate consistent critical settings across ranks. Broadcast or collectively validate canonical configuration rather than allowing silent divergence.

All ranks opening one file with ordinary independent writes can corrupt it. Use rank-specific names with stable run/chunk identity, collective/parallel I/O, or one explicitly bounded aggregator. Write to temporary/versioned destinations and atomically publish a complete manifest. Capture which ranks succeeded.

Stdout/stderr from processes can interleave, buffer, arrive late, or be prefixed by launchers. It is diagnostic, not a total order. Structured per-rank logs use monotonic local sequence plus run/rank/host fields and a collection strategy. Clock timestamps across nodes need synchronization/error assumptions.

For randomness, derive independent reproducible streams from a master seed and stable logical identity, not rank alone if results should remain invariant under repartitioning. Record generator/version and avoid overlapping streams. Rank-dependent reduction/order can still change floating results.

### Errors, termination, and reproducibility

MPI error handlers and return codes have scopes and limitations; default handling may abort. Continuing after many MPI errors is not generally guaranteed. Define whether any rank error aborts the job, enters a collective cleanup, writes a failed checkpoint, or invokes a separately supported fault-tolerance mechanism. Avoid a failed rank waiting for collectives peers will never enter.

The launcher/resource manager determines signal propagation, timeout, stdout collection, and aggregate exit status. Test a nonzero exit and signal on every rank position. Monitor hangs via progress/heartbeats external to collectives where appropriate; force termination only after preserving useful diagnostics and respecting sensitive data.

Reproducibility records process count, communicator construction, partition function, mapping/binding, host topology, thread level, library/transport versions, environment, seeds, input/output manifests, and reduction/determinism policy. Bitwise invariance across P is a separate algorithmic requirement, not a property of ranks.

### Verification, security, and operations

Test P=1,2,3, non-power-of-two, P>N, uneven N, zero N, maximum sizes/counts, empty local partitions, subcommunicators, reordered ranks, multiple nodes, changed mapping/binding, threads, devices, and filesystem/environment variation. Validate coverage/ownership, communicator membership, collective control, buffer lifetime, outputs, and cleanup. Inject launch failure, one-rank error/signal, timeout, network/device/filesystem failure where supported.

Avoid secrets in command lines, environment dumps, process listings, rank logs, core dumps, and shared files. Apply least privilege, network/interface policy, authenticated scheduler access, isolated scratch, encryption where required, per-rank permissions, retention/erasure, and tenant/resource boundaries.

Operational handoff includes exact scheduler/launcher command, allocation assumptions, module/container/library/transport versions, placement report, expected rank/host map constraints, resources, time/memory limits, signals/checkpoint policy, output manifest, monitoring, and incident cleanup. High-stakes runs require named domain and independent review beyond MPI correctness.

## Definitions and Notation

- `P`: size of communicator C; `k in [0,P)`: rank in C.
- `N`: global logical item count.
- `q=floor(N/P)`, `r=N mod P` for P>0.
- `n_k=q+[k<r]`: block count owned by rank k.
- `s_k=kq+min(k,r)`: block start; `e_k=s_k+n_k`.
- `G_C`: ordered group associated with communicator C.
- `ctx(C)`: communication context distinguishing C's messages.
- `L_k`: rank-local state/domain.
- `owner(i)`: rank that owns global item i under the selected partition.
- `T_req,T_prov`: requested and provided MPI thread-support levels.
- `A,M,R,B`: allocation, mapping, ranking, and binding descriptions.

Rank k without communicator C is incomplete identity; local pointer equality across ranks conveys no shared object.

## Mechanisms, Invariants, or Proof Structure

### Block-partition proof

Counts are q or q+1 and nonnegative. Starts are prefix sums. For adjacent ranks, `e_k=s_{k+1}`; `s_0=0`; sum counts is `Pq+r=N`, so `e_{P-1}=N`. Half-open intervals are disjoint and cover `[0,N)` exactly, including N<P and N=0.

### Communicator isolation argument

All operations interpret source/destination ranks and matching inside one communicator context. Separate communicators prevent accidental cross-protocol matching. Membership/order is constructed compatibly; null/nonmember processes do not call through the communicator.

### Lifecycle/thread proof

Every MPI call/object belongs to a valid initialized World or Sessions provenance and lifetime. Required processes enter compatible collectives/finalization. `T_prov>=T_req` under the MPI support ordering, and calls obey funneled/serialized/multiple constraints. Outstanding buffers/requests complete before reuse/release.

### Placement-independence argument

Logical ownership depends on `(C,k,P,N)`, not hostname/core/device accident. Mapping/binding may change cost but not results. Hardware-specific device selection is capability/affinity-checked and recorded without changing global identity.

### Termination/evidence argument

Each rank reports structured terminal status; launcher status and output manifest distinguish full success, validation failure, timeout/signal, and incomplete ranks. External publication occurs only after expected ranks/results validate. Failure policy never mistakes partial output for a completed run.

## Alternatives and Trade-Offs

| Choice | Main benefit | Principal limitation |
|---|---|---|
| One process | simple debugging/reference | no distributed scale |
| Rank per core | simple SPMD capacity | memory/communication duplication |
| Rank per NUMA/socket | locality plus threading | hybrid thread complexity |
| Block partition | locality and simple I/O | skew for irregular costs |
| Cyclic/block-cyclic | balances patterned costs | fragmented locality/communication |
| `MPI_COMM_WORLD` | conventional whole-job context | global component coupling |
| Sessions | component-scoped resources | explicit provenance/support complexity |
| Subcommunicators | isolation/topology/team algorithms | construction/lifecycle coordination |
| Root aggregation | simple final assembly | bottleneck/memory/failure concentration |
| Distributed output | scalable ownership | manifest/atomic publication complexity |
| Explicit binding | reproducible locality | target/site-specific tuning |

Prefer logical identities and parameterized decompositions; treat placement as recorded policy.

## Failure Modes and Misconceptions

- **“Rank identifies a process globally.”** it is relative to a communicator.
- **“Rank equals node or core.”** launch mapping and binding decide placement.
- **“Rank zero is special hardware.”** it is only communicator index zero.
- **“Same pointer means shared memory.”** address spaces are private.
- **“SPMD means identical control.”** rank/data branches differ but protocols must match.
- **“World size is constant in source.”** supported P is a runtime input.
- **“Equal chunks require divisible N.”** quotient/remainder handles uneven data.
- **“No local data means exit.”** empty ranks may still owe collectives.
- **“Communicators are labels.”** group plus context controls identity/matching.
- **“The launcher is MPI.”** resource/process management is partly external.
- **“Requested thread support is granted.”** inspect the provided level.
- **“Finalize flushes every application effect.”** complete protocols and I/O explicitly.
- **“Stdout order is execution order.”** streams are independently buffered/merged.
- **“Hostname order is topology.”** query/record placement and affinity.
- **“Any rank can write the same file.”** ordinary concurrent writes need coordination.
- **“One rank failure is local.”** ordinary MPI jobs may lose global progress.
- **“More ranks always scale.”** communication, memory, contention, and imbalance grow.

## Worked Examples

### Example 1

**Communicator-relative rank.** World rank 6 joins a four-process subcommunicator as rank 1. **Conclusion:** persist communicator/group identity with ranks.

### Example 2

**Pointer mistake.** Rank 0 sends a heap pointer; rank 1 dereferences the numeric address and faults. **Conclusion:** send data or logical handles, not ordinary addresses.

### Example 3

**Uneven block.** Seventeen items over four ranks produce counts 5,4,4,4 with complete coverage. **Conclusion:** process-count-parametric arithmetic includes remainders.

### Example 4

**Empty owner.** Eight ranks process three items; five own zero but still join final reduction. **Conclusion:** local emptiness does not erase communicator obligations.

### Example 5

**Collective mismatch.** Only rank zero enters a broadcast because the call is inside the root-only branch. Peers never participate. **Conclusion:** root-specific buffer work surrounds, not excludes, collective calls.

### Example 6

**Thread-level mismatch.** A program requests serialized support but two worker threads call MPI concurrently. **Conclusion:** provided thread contract constrains local concurrency.

### Example 7

**Binding collapse.** Four two-thread ranks are each bound to one CPU. **Conclusion:** CPUs-per-task and binding must cover local workers.

### Example 8

**GPU collision.** Every rank uses device ordinal zero despite two GPUs. Local-rank-aware visible-device policy fixes placement. **Conclusion:** verify device affinity and sharing explicitly.

### Example 9

**File collision.** All ranks truncate `result.bin`; only a fragment survives. Rank-owned files plus a validated manifest avoid collision. **Conclusion:** output namespace is distributed state.

### Example 10

**Climate hazard projection.** Decomposition must preserve ensemble/member/scenario/grid/time identity, units, boundary/halo rules, missing data, reduction/reproducibility and uncertainty policy, model/input provenance, checkpoint/restart, partial-failure semantics, access controls, and published completeness. Named climate/domain, geospatial, numerical/statistical, MPI/runtime, data stewardship, security, operations, quality, policy/impact, and independent validation reviewers must approve requirements and evidence; none is claimed here. **Conclusion:** correct ranks and coverage do not establish scientific validity or policy fitness.

## Cross-Program Connections

- **Operating systems:** processes, private address spaces, affinity, signals, files, and exit status underpin ranks.
- **Networks:** later messages transport data between communicator members over selected interfaces/transports.
- **Distributed systems:** identity scope, partitions, membership, partial failure, manifests, and commit recur.
- **Algorithms:** decomposition, halos, reductions, and load balance map global domains to local work.
- **Programming languages:** object provenance, ownership, thread levels, and lifetimes constrain safe bindings/libraries.
- **Schedulers:** allocation, mapping, ranking, binding, limits, and placement are resource-manager policy.
- **Numerical computing:** reduction order and partition-dependent rounding affect reproducibility.
- **Storage:** parallel/rank-local output, checkpoints, and atomic manifests preserve global identity.
- **Security:** launch environments, logs, dumps, scratch, and interconnect policy cross nodes.
- **Operations:** commands, topology, versions, timeouts, failure aggregation, cleanup, and restart make runs reproducible.

## References

1. MPI Forum, *MPI: A Message-Passing Interface Standard, Version 4.1*, official PDF, 2023. <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report.pdf>
2. MPI Forum, *MPI-4.1 Standard: Terms and Conventions*, 2023. <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report/node8.htm>
3. MPI Forum, *MPI-4.1 Standard: Process Initialization, Creation, and Management*, 2023. <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report/node265.htm>
4. MPI Forum, *MPI-4.1 Standard: The Sessions Model*, 2023. <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report/node271.htm>
5. MPI Forum, *MPI-4.1 Standard: Environmental Management*, 2023. <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report/node237.htm>
6. Open MPI Project, *mpirun / mpiexec Manual*, current documentation; retrieved 2026-08-29. <https://docs.open-mpi.org/en/main/man-openmpi/man1/mpirun.1.html>
7. Open MPI Project, *Scheduling Processes Across Hosts*, current documentation; retrieved 2026-08-29. <https://docs.open-mpi.org/en/main/launching-apps/scheduling.html>
8. Open MPI Project, *Processor and Memory Affinity*, current documentation; retrieved 2026-08-29. <https://docs.open-mpi.org/en/main/tuning-apps/affinity.html>
9. SchedMD, *Slurm srun*, current documentation; retrieved 2026-08-29. <https://slurm.schedmd.com/srun.html>
10. SchedMD, *Slurm CPU Management User and Administrator Guide*, current documentation; retrieved 2026-08-29. <https://slurm.schedmd.com/cpu_management.html>

## Exercises

### Exercise 1

Prove the quotient/remainder block partition and instantiate it for N=3,P=8 and N=20,P=6, including empty ranks and starts.

### Exercise 2

Explain why `(communicator,rank)` rather than rank is process identity for communication. Design world, node-local, and even-world-rank communicators and trace one process's ranks.

### Exercise 3

Design lifecycle/thread rules for an application with a Sessions-aware library, World-model application, four local worker threads per rank, and nonblocking requests.

### Exercise 4

Specify and test a scheduler/launcher plan for two nodes, two sockets/node, four GPUs/node, eight ranks, and two threads/rank without oversubscription or GPU collision.

### Exercise 5

A regulated multi-site genomics run partitions samples across ranks and writes distributed outputs. Specify identity, partition, numeric, privacy, failure/restart, reproducibility, publication, and human-review evidence.

## Answers to the Exercises

### Answer 1

Write `N=qP+r`, counts `q+1` for k<r else q, starts `kq+min(k,r)`. Starts equal preceding prefix sums, adjacent end/start meet, total is `Pq+r=N`, so half-open ranges cover once. For N=3,P=8: q=0,r=3, counts `[1,1,1,0,0,0,0,0]`, starts `[0,1,2,3,3,3,3,3]`; ranges `[0,1),[1,2),[2,3)` then empty `[3,3)`. For N=20,P=6: q=3,r=2, counts `[4,4,3,3,3,3]`, starts `[0,4,8,11,14,17]`, final end 20. Empty ranks remain protocol participants.

### Answer 2

A communicator defines both ordered group and matching context; rank is the position in that group. Split world by shared-memory/node locality for node communicators; split world by color `world_rank mod 2` for even/odd groups. For a world process, record world rank, hostname/node group identity and node-local rank, and even communicator membership/rank if even; an odd process receives no even communicator. World rank 6 might be node-local rank 2 and even-group rank 3. Messages use ranks in the communicator passed; substituting world rank into a subcommunicator can address the wrong/nonexistent member. Context also isolates protocols with identical tags.

### Answer 3

Application owns World initialization/finalization and requests at least `MPI_THREAD_MULTIPLE` if all four workers call concurrently; otherwise use FUNNELED with only the initializing/main thread, or SERIALIZED with a lock and ensure the provided level meets it. The library owns its Session, process sets, groups, communicators, errors, and finalization, and never mixes Session-derived objects with World objects in forbidden calls. Document any implementation interoperability limits. Every nonblocking request and buffer completes before mutation/release; communicators remain live through requests. Coordinate shutdown so workers stop submitting, requests finish/cancel under allowed semantics, library releases Session objects/session, application releases World objects and collectively finalizes. Test provided-level downgrade and error paths.

### Answer 4

Allocate two nodes, eight tasks total/four per node, two CPUs per task (16 CPU workers total), and four GPUs per node. Choose mapping four ranks/node and binding each rank to two cores within an appropriate socket/NUMA domain; request enough memory and prevent implicit extra library threads. Expose or assign one GPU per local rank 0–3, verify topology/CPU affinity and memory, and prohibit unintended sharing. Report launcher mapping/bindings and within each rank record world/local rank, host, CPU affinity, visible/selected device UUID, thread count, and NUMA placement. Test reordered ranking, site defaults, hyperthreads, missing GPU, and mismatch between allocation and binding; correctness must not depend on physical rank ordering.

### Answer 5

Use stable run/site/patient/sample/library/read/reference/coordinate identities independent of rank; version input manifests, consent/access purpose, reference/build, algorithms, configuration, and partition function. Prove complete unique ownership or declared replication and reconstruct global order from IDs. Define exact integer and floating/reduction/statistical semantics, missing/duplicate/filter and uncertainty policy; validate P=1 and varied uneven P, placement, ranks, implementations, restarts, and order. Encrypt transfer/storage, isolate scheduler jobs/scratch/logs, minimize data, audit access, and enforce retention/erasure. Checkpoint immutable/versioned rank outputs with digests and a global manifest; on rank/node/storage failure resume idempotently from validated generations and never publish partial results. Record command, allocation/map/bind, hosts/devices, MPI/transport/thread level, seeds, outputs and terminal statuses. Named genomics, bioinformatics/statistics, clinical/laboratory and site governance, numerical, MPI/runtime, security/privacy, data stewardship, operations/SRE, quality/regulatory, human-factors, and independent validation reviewers approve validity, bias, limitations, and residual risk. Rank coverage alone establishes no biological or clinical validity.
