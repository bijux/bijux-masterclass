---
module_id: CONPAR-084
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 84
title: Domain Decomposition
status: complete
last_verified: 2026-08-29
---

# Domain Decomposition

## One-Page Review

### Governing question

How should a global computational domain and its state be partitioned among ranks so that ownership is unique, dependencies are representable, work and memory are balanced, communication is controlled, and the original mathematical problem is preserved?

### Essential definitions

- A **domain** is the indexed, geometric, graph, particle, or application state over which a computation is defined.
- A **partition** is a family of owned subsets whose union is the global domain and whose interiors are disjoint.
- An **owner** is the rank authorized to update and publish a global entity in one decomposition generation.
- A **subdomain** is one rank's owned region plus metadata about its boundary and neighbors.
- A **ghost** or **halo** is a read-only local replica of remotely owned state needed by local work.
- A **separator** is a set of vertices or edges crossing between parts; its weighted size estimates communication.
- **surface-to-volume ratio** compares boundary data with owned work for a geometric part.
- A **process topology** maps logical partition adjacency to communicator ranks; it need not equal physical network topology.
- **static decomposition** remains fixed during a run; **dynamic repartitioning** changes ownership and migrates state.
- A **partition weight** estimates computation or memory; an **edge weight** estimates communication.
- A **global-to-local map** relates stable global identities to owned and ghost storage.

### Central model, mechanism, or theorem

Represent the application as a weighted dependency graph `G=(V,E)`. A partition `pi:V->{0,...,P-1}` must cover every vertex exactly once as owner. The load of rank r is the sum of vertex weights mapped to r; cut cost is the sum of weights on edges crossing ranks. Correctness requires ownership, adjacency, boundary-condition, migration, and reduction invariants. Performance seeks low maximum load, memory feasibility, compact/sparse communication, and locality, but graph partitioning is a multi-objective optimization: equal entity counts alone are neither necessary nor sufficient.

### Critical invariants

Every global entity has exactly one owner per generation; owned sets are disjoint and cover the active domain; every local dependency is owned or supplied by a version-matched ghost; global IDs survive rank reordering and migration; boundary conditions distinguish physical boundaries from inter-rank cuts; sends and receives derive from the same adjacency; counts, offsets, extents, and allocations are checked; global conservation and application constraints survive partitioning; no rank exceeds memory/resource limits; and repartition publication is atomic with respect to the next computation epoch.

### Common failures

Teams divide indices with truncation and lose the remainder, confuse rank with spatial coordinate, double-update interface entities, apply physical boundary conditions at partition cuts, use equal cells for unequal work, optimize cut count while overloading memory, replicate global metadata, build all-to-all neighbor discovery, retain stale ghosts after migration, change ownership without moving dependent state, compare different numerical problems, or call a balanced process grid proof of end-to-end scalability.

### Compact example

A `10 x 7` cell grid on a `3 x 2` process grid splits widths `[4,3,3]` and heights `[4,3]`. The six rectangles cover all 70 cells exactly once; their cell loads are `16,12,12,12,9,9`. The maximum-to-average entity imbalance is `16/(70/6)=1.371429`, and 24 grid edges cross cuts. The partition is correct but not perfectly balanced.

### Connections

[Collective Communication](083-collective-communication.md) supplies global agreement and aggregate checks. [Point-to-Point Message Passing](082-point-to-point-message-passing.md) supplies migration and neighbor protocols. [Work Partitioning and Granularity](045-work-partitioning-and-granularity.md) supplies local cost reasoning. The [program roadmap](../ROADMAP.md) next applies the ownership map to halo exchange and stencil computation.

## Governing Question

For a stated global problem, which entities does each rank own, which remote values does it need, which invariants make the distributed representation equivalent to the global one, and which measured partition best balances critical-path work, memory, and communication on the target system?

Domain decomposition is not merely array slicing. It is the durable contract between mathematical entities, storage ownership, communication topology, scheduling, I/O, restart, and validation.

## Why This Matters

Distributed memory removes a shared address space. Every value used locally must be owned locally, replicated deliberately, or communicated. The decomposition therefore determines most communication and much of the achievable concurrency before a message-passing routine is chosen.

A poor decomposition can be mathematically correct yet unusable: one rank owns the refined mesh, a thin three-dimensional slab has excessive surface area, particles migrate faster than they are computed, or root metadata exhausts memory. A fast decomposition can also be wrong if it loses cells, applies boundary rules at internal cuts, duplicates forces, or publishes state from mixed generations.

Modern production codes use structured Cartesian partitions, graph/hypergraph partitioners, space-filling curves, recursive coordinate bisection, mesh/forest libraries, and application-specific constraints. The lasting skill is to state the ownership problem, derive invariants and objective metrics, and validate the distributed result independently of a particular partitioner.

## Prerequisites and Retrieval

Retrieve:

- ranks, communicator identity, rank reordering, placement, and lifecycle from [Processes and Ranks in Distributed-Memory Programs](081-processes-and-ranks-in-distributed-memory-programs.md);
- envelope, signature, request, progress, flow-control, and migration protocol reasoning from [Point-to-Point Message Passing](082-point-to-point-message-passing.md);
- reductions, scans, neighborhood collectives, and numeric policies from [Collective Communication](083-collective-communication.md); and
- task weights, granularity, span, and scheduling overhead from [Work Partitioning and Granularity](045-work-partitioning-and-granularity.md).

Retrieval prompt: name the global entity set and stable IDs; dependency/adjacency relation; compute, memory, and edge weights; ownership function and generation; local/ghost maps; physical and partition boundaries; process and physical topology; migration payload/order; conservation/reference oracle; imbalance/cut/locality metrics; resource limits; and failure/restart policy.

## Learning Objectives

After completing this module, a learner can:

1. distinguish geometric, graph, particle, functional, and replicated decompositions;
2. derive quotient/remainder block bounds that cover irregular global sizes exactly;
3. prove unique ownership, coverage, adjacency, ghost, and boundary-condition invariants;
4. model load, memory, separator/cut, surface-to-volume ratio, and migration cost;
5. choose slabs, pencils, blocks, Cartesian grids, graphs, hypergraphs, or space-filling curves by dependency structure;
6. use logical MPI topologies without assuming physical placement or stable ranks;
7. design stable global-to-local identities and migration-safe data structures;
8. compare static, weighted, adaptive, and dynamically repartitioned designs;
9. validate partitions across sizes, rank counts, topologies, failures, and application oracles; and
10. scope numerical, security, operational, and high-stakes review claims.

## Core Exposition

### Begin with entities and dependencies

Define what is indivisible. It might be a grid cell, finite element, graph vertex, particle, ray, matrix row, key range, or task. Define which entities depend on which others during one computation epoch. Direction matters: a sparse matrix row reads columns; a particle interacts within a cutoff; a finite-volume cell uses faces and neighbors. This dependency structure, not a visualization alone, determines communication.

Assign stable global IDs independent of current rank. A rank-local dense index improves storage and iteration, but it is not a durable identity. Maintain maps `global -> (owner,local)` and local arrays of global IDs. Version the mapping by decomposition generation so stale messages, checkpoints, and ghosts cannot be mistaken for current state.

Some entities live on boundaries, faces, edges, or vertices shared by geometric cells. Choose an ownership rule such as lowest incident global cell ID, a mesh-library owner, or an explicit partition result. “Both ranks have it” describes replication, not update authority. Reads may be replicated; side effects and global assembly require an owner or an associative merge rule.

### Structured block decomposition

For N one-dimensional entities and P parts, let `q=floor(N/P)` and `r=N mod P`. Part k owns `q+1` entities when `k<r`, otherwise q. Its start is `k*q+min(k,r)` and its half-open end adds its size. These bounds cover `[0,N)` without gaps or overlap, including `P>N` if empty ranks are permitted by the application.

In d dimensions, choose process-grid dimensions `p_0...p_(d-1)` whose product is P, then apply the one-dimensional rule per coordinate. Slabs partition one dimension, pencils two, and blocks three. For local side lengths `n_i`, approximate owned volume by the product and one-cell face boundary by `2*sum_i product_(j!=i) n_j`. Cubic parts minimize surface for fixed rectangular volume, but physical anisotropy, stencil width, process topology, and unequal costs can justify non-cubic shapes.

MPI Cartesian topology attaches logical dimensions, periodicity, and optional rank reordering to a communicator. `MPI_Dims_create` proposes balanced factorization, not an application-optimal decomposition. `MPI_Cart_shift` can identify coordinate neighbors; a nonperiodic off-end yields `MPI_PROC_NULL`. Always compute coordinates from the returned communicator because `reorder=true` permits rank changes.

### Irregular graphs and meshes

An unstructured mesh or sparse graph has no rectangular coordinate cut that reliably predicts dependencies. Construct a weighted graph: vertices represent work/storage units and edges represent communication. Minimize maximum part load subject to capacity while reducing cut-edge weight, neighbor count, and possibly migration. A hypergraph can model one communication object shared by many vertices more faithfully than pairwise edges, at greater partitioning cost.

Partition objectives conflict. A minimum cut may form disconnected or elongated parts; perfect compute balance may exceed memory; fewer neighbors may increase bytes; preserving the old partition may sacrifice current balance. Express hard constraints separately from weighted objectives. Record the partitioner, version, seed/options, weights, input digest, result digest, and achieved metrics rather than treating a library call as self-validating.

Adaptive meshes complicate weights and adjacency. Refinement creates more cells and degrees of freedom; coarsening removes them. Space-filling curves linearize spatially nearby leaves and permit scalable contiguous ranges, but curve proximity is imperfect and application weights still matter. Forest-of-octree systems typically couple adapt, balance, partition, ghost rebuild, application-data transfer, and verification as one state transition.

### Particles, sparse interactions, and functional splits

Spatial particle decomposition assigns particles by position and maintains ghosts for interactions reaching across subdomains. The communication thickness follows the physical cutoff plus motion/list policy, not simply one cell. Fast particles can cross multiple parts; migration must locate the new owner without loss or duplication. Density variation makes equal volume unequal work, so weighted moving cuts or recursive coordinate bisection may help.

Graph computations can use vertex or edge ownership. Sparse matrices commonly own row ranges; off-process column indices define imports. Pipelines and multi-physics codes may decompose by function, with stages or fields on different ranks, but that creates bulk interfaces and unequal concurrency. Hybrid decompositions combine spatial ownership with replicated small metadata and task parallelism inside each rank.

Replication is justified only for bounded, read-mostly state whose consistency protocol is explicit. Replicating a mesh directory or parameter table can simplify lookup; replicating a growing global graph destroys memory scaling. Quantify replicated bytes per rank and total system memory.

### Ownership, ghosts, and boundary semantics

Owned state is authoritative for an epoch. Ghost state is a cached snapshot tagged with owner, global ID, field/schema, time/iteration, and decomposition generation. A computation may read a ghost only after the required exchange completes and may not publish ghost updates unless a defined accumulation routes them to owners.

Partition boundaries are not physical boundaries. A cell at the edge of a rank but inside the global domain receives neighbor data. A cell at a nonperiodic global edge receives the problem's boundary condition. Periodic global edges connect distant coordinates and may be neighbors in the logical topology. Encode boundary kind in topology metadata rather than infer it from missing local indices.

For conservative discretizations, each physical interface flux must contribute once with opposite signs to its incident control volumes, or be recomputed consistently under a proved rule. For particle pairs, use a documented full/half neighbor-list and Newton/update policy. Global conservation checks reveal double counting and omissions that local array bounds cannot.

### Executable partition model

The following exact-integer model decomposes a `10 x 7` cell grid over a `3 x 2` logical process grid and reports half-open boxes, cell loads, neighbor degrees, cut edges, and imbalance. It does not call MPI, partition an unstructured graph, model halos/physics, or prove performance.

<!-- bijux-verify: {"id":"uneven-cartesian-partition","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"x_sizes=[4, 3, 3]\ny_sizes=[4, 3]\nrank=0 box=x[0,4) y[0,4) cells=16 neighbors=2\nrank=1 box=x[4,7) y[0,4) cells=12 neighbors=3\nrank=2 box=x[7,10) y[0,4) cells=12 neighbors=2\nrank=3 box=x[0,4) y[4,7) cells=12 neighbors=2\nrank=4 box=x[4,7) y[4,7) cells=9 neighbors=3\nrank=5 box=x[7,10) y[4,7) cells=9 neighbors=2\ntotal_cells=70\ncut_edges=24\ncell_imbalance=1.371429\n","stderr":""}} -->
```python
def cuts(length, parts):
    quotient, remainder = divmod(length, parts)
    sizes = [quotient + (1 if index < remainder else 0) for index in range(parts)]
    starts = []
    cursor = 0
    for size in sizes:
        starts.append(cursor)
        cursor += size
    return sizes, starts


nx, ny = 10, 7
px, py = 3, 2
x_sizes, x_starts = cuts(nx, px)
y_sizes, y_starts = cuts(ny, py)
print(f"x_sizes={x_sizes}")
print(f"y_sizes={y_sizes}")

total = 0
rank = 0
for row in range(py):
    for column in range(px):
        cells = x_sizes[column] * y_sizes[row]
        total += cells
        neighbors = (column > 0) + (column + 1 < px) + (row > 0) + (row + 1 < py)
        x_end = x_starts[column] + x_sizes[column]
        y_end = y_starts[row] + y_sizes[row]
        print(
            f"rank={rank} box=x[{x_starts[column]},{x_end}) "
            f"y[{y_starts[row]},{y_end}) cells={cells} neighbors={neighbors}"
        )
        rank += 1

cut_edges = (px - 1) * ny + (py - 1) * nx
maximum = max(x_size * y_size for x_size in x_sizes for y_size in y_sizes)
imbalance = maximum / ((nx * ny) / (px * py))
print(f"total_cells={total}")
print(f"cut_edges={cut_edges}")
print(f"cell_imbalance={imbalance:.6f}")
```

### Mapping and storage design

Separate topology from field storage. A decomposition object should own global IDs, owner ranks, local owned/ghost ranges, adjacency, exchange plans, and generation. Field arrays use that layout but do not duplicate its logic. This permits multiple fields, derived datatypes, accelerators, solvers, and I/O to share one verified mapping.

Use checked wide integer arithmetic for global counts, prefix sums, byte extents, and displacements. Half-open ranges simplify coverage proofs. For irregular data, use compact sparse adjacency and deterministic ordering where reproducibility/debugging needs it. Stable IDs belong in checkpoint and migration payloads; raw addresses and old local indices do not.

Derive send lists from owners of required remote IDs and receive lists from local ghosts. Exchange counts first only when needed, or retain a reusable plan until topology changes. Verify reciprocity: for every planned import there is a compatible export. A distributed graph communicator can represent sparse directed adjacency and accept weights/hints, but its logical graph does not prove optimal physical mapping.

### Dynamic repartitioning and migration

Repartition only when expected savings exceed measurement, partitioning, synchronization, migration, cache/device rebuild, and lost-locality costs. Use hysteresis or a minimum residence interval so noise does not trigger oscillation. Separate compute weights, memory weights, and migration penalties; historical time per entity can be more useful than entity counts when measured carefully.

A safe transition freezes or versions updates, computes the new map, allocates destination capacity, transfers authoritative state and dependent metadata, verifies counts/digests/conservation, rebuilds ghosts/indices/communicators, and atomically activates the new generation. The old generation remains recoverable until validation succeeds. Deduplicate retries by `(generation,global_id,field_version)`.

Checkpoint semantics must state whether files use global canonical order or partition-specific shards. A restart at a different rank count needs stable IDs and a redistribution path. Never assume rank-local checkpoint files map directly after topology or scheduler changes.

### Measuring decomposition quality

Let rank load `L_r=sum_{v:pi(v)=r} w_v`. Report `max_r L_r`, average, coefficient/distribution, and imbalance `max/average`; critical path follows the maximum, not the mean. Also report memory high-water mark, cut weight, bytes/messages, neighbor degree, surface/volume, replicated memory, migration volume, locality, and partition/setup time.

Weights are hypotheses. Validate them against per-rank compute time, hardware counters, allocation, and communication traces. Normalize only comparable runs with identical global problem, discretization, convergence, accuracy, I/O, and failure policy. Strong scaling reduces work per rank until boundaries and fixed costs dominate; weak scaling can increase global distances, collectives, and congestion even with constant local volume.

### Verification and operations

Before physics, test the partition alone. Gather or hash owned global IDs to prove exact coverage and uniqueness; validate local bounds; check edge reciprocity; compare total weights/counts with a serial source; test global boundaries and periodic wraps; poison ghosts before exchange; and run with one, prime, non-power-of-two, and more ranks than entities where supported.

For application validation, compare partition-independent invariants, deterministic reference cases, conservation, residuals, error norms, and result digests under multiple valid partitions and rank reorderings. Floating results may differ by reduction/evaluation order, so define tolerance or reproducible mode instead of demanding incidental bit identity.

In production retain program/input/mesh/partition digests, rank/node mapping, weights/options/seeds, per-rank entities/work/memory/neighbors/bytes, migrations, generation, failed validation, and restart lineage. Avoid logging sensitive entity attributes or locations. Set quotas for metadata, neighbors, migration buffers, and replicated state; malformed graph input can otherwise cause memory or communication denial.

## Definitions and Notation

- `D` or `V`: global entity set; `N=|V|`.
- `E`: directed or undirected dependency edges.
- `P`: number of participating ranks.
- `pi(v)`: owner rank of entity v in one generation.
- `V_r={v | pi(v)=r}`: owned set of rank r.
- `w_v,m_v`: compute and memory weight of v.
- `c_e`: communication weight of dependency edge e.
- `L_r=sum_(v in V_r) w_v`: modeled load.
- `I=max_r L_r / ((sum_v w_v)/P)`: maximum-to-average imbalance.
- `cut(pi)=sum_(u,v in E, pi(u)!=pi(v)) c_(u,v)`: weighted cut.
- `H_r`: ghost entity set stored by rank r.
- `g`: decomposition generation.
- `G2L_r`: global-to-local map for owned and ghost entities.
- `B_phys`, `B_part`: physical and partition boundaries.

Entity count is a special weight, not a universal cost model. A logical process topology is metadata and may differ from physical placement.

## Mechanisms, Invariants, or Proof Structure

### Coverage and ownership proof

Show `union_r V_r=V` and `V_r intersect V_s=empty` for `r!=s`. For quotient/remainder blocks, starts are consecutive half-open ends and sizes sum to N. For a partitioner, independently count and hash global IDs and reject duplicates/missing owners.

### Dependency and ghost proof

For every dependency `(u,v)` needed by an owned computation, v is either owned locally or present in a ghost set sourced from `pi(v)`. Send/export and receive/import signatures agree. Ghost field, time, schema, and generation match the computation epoch.

### Boundary and conservation proof

Classify every missing local neighbor as physical, periodic, partition-remote, or invalid. Apply physical policy only to `B_phys`. Account for each interface contribution exactly once or by a proved symmetric accumulation; compare global conserved quantities with the undecomposed oracle.

### Capacity and cost proof

Checked sums/extents fit each rank's memory and API count types. Compute load, cut, degree, surface, replicated bytes, and migration metrics under declared weights. Performance conclusions remain hypotheses until measured on the target.

### Migration proof

Every old owner sends each migrating entity and required dependent state to exactly one new owner; stationary entities remain; totals/digests/conservation agree; new ghosts/maps are derived from the new partition; and generation g+1 is published only after validation. Retry identities prevent duplication.

## Alternatives and Trade-Offs

| Approach | Main benefit | Principal limitation |
|---|---|---|
| 1-D slabs | simplest indexing/exchange | high surface or limited P |
| 2-D pencils | better surface/scalability | transpose and neighbor complexity |
| 3-D blocks | compact local volume | complex layout and small dimensions |
| Cartesian logical topology | coordinates/periodicity/neighbors | not physical-placement proof |
| graph partitioning | models irregular adjacency | setup/global metadata/objective trade-offs |
| hypergraph partitioning | models multiway communication | higher complexity and cost |
| space-filling curve | scalable locality/order | imperfect cut and constraint modeling |
| recursive coordinate bisection | geometry-aware balance | may ignore true dependency weights |
| replicated state | simple reads | per-rank memory/consistency growth |
| dynamic repartitioning | adapts to changing work | migration, rebuild, and instability costs |

Prefer the least complex representation that captures the real dependencies and satisfies hard constraints; compare alternatives with identical correctness and workload evidence.

## Failure Modes and Misconceptions

- **“N/P bounds are enough.”** quotient/remainder and half-open endpoints prevent gaps.
- **“Equal cells means equal time.”** entity costs, solvers, branches, and devices differ.
- **“Rank is a coordinate.”** reordered and irregular topologies require explicit maps.
- **“A partition cut is a physical edge.”** remote neighbor data replaces boundary conditions.
- **“Ghosts may be updated normally.”** ownership and accumulation rules govern writes.
- **“Minimum edge cut is optimal.”** memory, degree, shape, migration, and topology also matter.
- **“Cartesian dimensions are automatically best.”** balanced factors ignore application anisotropy.
- **“Logical neighbors are physically close.”** placement must be queried and measured.
- **“Stable ranks are stable identities.”** global entity IDs survive remapping and restart.
- **“All metadata is small.”** replicated directories can dominate at scale.
- **“Repartitioning is free balance.”** measurement, migration, and rebuild lie on the path.
- **“Space-filling curves preserve all locality.”** one-dimensional order only approximates geometry.
- **“More parts always improve speed.”** surface, latency, collectives, and empty work grow.
- **“A partitioner proves correctness.”** independent coverage, adjacency, and application oracles remain required.
- **“Same result bits are always required.”** legal floating schedules need an explicit policy.
- **“A successful exchange validates physics.”** units, conservation, discretization, and domain review remain.

## Worked Examples

### Example 1

**Uneven one-dimensional block.** Split N=10 over P=3. `q=3,r=1`, so sizes are `[4,3,3]`, starts `[0,4,7]`, and ends `[4,7,10]`. The half-open ranges cover every index exactly once. **Conclusion:** distribute the remainder explicitly.

### Example 2

**More ranks than entities.** N=3 and P=5 gives sizes `[1,1,1,0,0]`. This is mathematically valid coverage but an application/library may forbid empty parts or waste collective resources. **Conclusion:** separate partition correctness from execution suitability.

### Example 3

**Slab versus block.** A `64^3` grid on 64 ranks can use 64 slabs of thickness 1 or `4x4x4` blocks of side 16. Thin slabs expose nearly the full two faces per rank; blocks are more compact and allow wider scaling. **Conclusion:** surface-to-volume ratio shapes communication.

### Example 4

**Rank reordering.** A program assumes rank 1 is the +x neighbor after creating a reordered Cartesian communicator. The runtime changes mapping. Querying coordinates and `Cart_shift` returns the correct neighbor. **Conclusion:** logical topology is explicit metadata.

### Example 5

**False physical boundary.** A local array ends at global x=31 but the global grid continues. Applying a wall condition there removes flux instead of importing x=32. **Conclusion:** classify global and partition boundaries separately.

### Example 6

**Weighted graph.** Four mesh cells have compute weights `[1,1,8,8]`. A two-and-two entity split can load ranks `2` and `16`; the weighted split `[1+8]` and `[1+8]` loads both `9`, possibly with a larger cut. **Conclusion:** optimize declared work, not counts alone.

### Example 7

**Replicated directory cliff.** A 200-byte record for one billion entities is “metadata.” Replicated on every rank it needs 200 GB per rank; distributed ownership plus a sparse lookup protocol scales with local entities. **Conclusion:** quantify replication.

### Example 8

**Migration generation.** Entity 42 moves from rank 2 to rank 5. A delayed generation-7 ghost update arrives after generation 8 activates. The receiver rejects `(g=7,id=42)` and retains generation-8 state. **Conclusion:** version topology and data together.

### Example 9

**Partition comparison.** Candidate A has imbalance 1.03 and 80 MB cut; B has 1.12 and 25 MB cut. On a compute-heavy kernel A wins; on a bandwidth-limited target B wins. Measure full iterations with identical answers. **Conclusion:** no scalar metric universally chooses a partition.

### Example 10

**Regional wildfire-risk simulation.** A decomposition must preserve coordinate reference systems, terrain/fuel/weather versions, units, physical boundaries, refinement interfaces, conservation/numerical error, uncertainty, privacy for household/health data, failure/restart lineage, and publication gates. Named wildfire science, meteorology, geospatial, numerical/HPC, emergency-management, privacy/security, operations, quality/regulatory, ethics, accessibility/human-factors, and independent validation reviewers must approve requirements and evidence; none is claimed here. **Conclusion:** balanced subdomains and matching checks do not establish forecast validity or safe operational decisions.

## Cross-Program Connections

- **Algorithms:** graph partitioning, separators, approximation, and space-filling curves formalize cuts.
- **Data structures:** sparse adjacency, stable IDs, maps, meshes, and spatial indices carry ownership.
- **Numerical computing:** discretization, conservation, conditioning, error, and adaptive refinement constrain partitions.
- **Databases:** sharding, consistent identity, range/hash partitioning, migration, and secondary indexes recur.
- **Distributed systems:** epochs, ownership transfer, deduplication, membership, and restart lineage recur.
- **Networks:** topology, bisection bandwidth, congestion, and message aggregation price separators.
- **Storage:** global layouts, checkpoint shards, and restart redistribution must follow stable identities.
- **Security/privacy:** placement and replication change disclosure and denial surfaces.
- **Performance engineering:** critical-path load, memory, cut bytes, locality, and setup require joint measurement.
- **Scientific computing:** structured/unstructured grids, particles, AMR, and multi-physics provide canonical uses.

## References

1. MPI Forum, *MPI: A Message-Passing Interface Standard, Version 5.0*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report.pdf>
2. MPI Forum, *MPI-5.0: Cartesian Constructor*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node226.htm>
3. MPI Forum, *MPI-5.0: Cartesian Convenience Function MPI_DIMS_CREATE*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node227.htm>
4. MPI Forum, *MPI-5.0: Distributed Graph Constructor*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node229.htm>
5. MPI Forum, *MPI-5.0: Topology Inquiry Functions*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node230.htm>
6. MPI Forum, *MPI-5.0: Subarray Datatype Constructor*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node101.htm>
7. PETSc Team, *DMDA: Structured Grids*, PETSc 3.25 documentation; retrieved 2026-08-29. <https://petsc.org/release/manualpages/DMDA/>
8. PETSc Team, *PetscPartitionerDMPlexPartition*, PETSc 3.25 documentation; retrieved 2026-08-29. <https://petsc.org/release/manualpages/DMPlex/PetscPartitionerDMPlexPartition/>
9. PETSc Team, *DMPlexDistributeOverlap*, PETSc 3.25 documentation; retrieved 2026-08-29. <https://petsc.org/release/manualpages/DMPlex/DMPlexDistributeOverlap/>
10. LAMMPS Project, *LAMMPS Overview: Spatial Decomposition*, current documentation; retrieved 2026-08-29. <https://docs.lammps.org/Intro_overview.html>

## Exercises

### Exercise 1

Derive exact half-open ownership ranges for N=23 entities over P=5 ranks. Prove coverage and report entity-count imbalance.

### Exercise 2

A nonperiodic `120 x 80` grid uses a `3 x 2` process grid with equal dimensions. Derive each local shape, total cut grid edges, neighbor degrees by position, and the effect of changing to `6 x 1`.

### Exercise 3

Diagnose a simulation that conserves mass on one rank but loses mass on four ranks. Logs show every local-array edge receives an outflow boundary condition and interface fluxes are computed by both ranks. Give invariants, tests, and a correction.

### Exercise 4

Design a repartition decision and migration protocol for an adaptive particle simulation whose density moves over time. Include weights, objectives, hysteresis, identities, generations, capacity, validation, rollback, and evidence.

### Exercise 5

Transfer the framework to a multi-institution radiation-dose optimization run containing sensitive patient geometry. Specify decomposition semantics, correctness/numerical/privacy invariants, failure/restart policy, validation matrix, evidence, publication gates, and required human reviewers without claiming external review.

## Answers to the Exercises

### Answer 1

`q=floor(23/5)=4`, `r=3`; sizes are `[5,5,5,4,4]`. Starts use `kq+min(k,r)`: `[0,5,10,15,19]`; ends are `[5,10,15,19,23]`. Consecutive starts equal prior ends, the first start is zero, the last end is 23, and positive half-open intervals do not overlap, proving exact coverage. Average is `23/5=4.6`, maximum 5, so maximum-to-average count imbalance is `5/4.6=25/23≈1.08696`.

### Answer 2

With `3 x 2`, every rank owns `40 x 40=1600` cells. Vertical cuts: `(3-1)*80=160` edges; horizontal cuts: `(2-1)*120=120`; total 280. Four corner parts have two neighbors and two non-corner parts have three. A `6 x 1` grid owns `20 x 80`; five vertical cuts cross `5*80=400` edges. End ranks have one neighbor and four interior ranks two. Both balance entity counts, but `3 x 2` has a smaller separator and less elongated parts; anisotropic physics/placement could still change the measured choice.

### Answer 3

The code confuses `B_part` with `B_phys` and likely double-counts interface flux. Establish exact coverage/ownership, classify edges by global coordinates/topology, and require one conservative interface rule: one owner computes a flux applied with opposite signs, or both compute an identical flux under a validated symmetric rule without duplicate global accumulation. Run a constant-field case, a two-part manufactured solution, poison/refresh ghosts, hash interface IDs, and compare per-step global mass with a serial oracle. Apply outflow only at true global boundaries; import remote state and account for each internal interface once.

### Answer 4

Measure per-particle/cell compute time, memory, interaction edges, neighbor bytes, and migration rate. Hard constraints are memory/capacity and exact ownership; objectives combine maximum predicted load, cut/degree, locality, and migration penalty. Repartition only when predicted savings over a residence horizon exceed partition+migration+rebuild cost by a margin, with hysteresis/minimum interval. Use stable particle IDs and generation g. Freeze/version updates, calculate g+1, preflight destination capacity, transfer authoritative state and neighbor-list inputs with deduplication keys, verify global counts/ID digests/conserved quantities, rebuild spatial indexes/ghosts, then atomically publish g+1. Retain g for rollback until validation. Record inputs, weights, options/seeds, mapping digest, bytes/time, imbalance, conservation, and full-iteration performance.

### Answer 5

Define stable anonymized voxel/beam/control-point IDs, owners, dose-influence dependencies, approved physical boundaries, units/coordinate frames, field/schema and decomposition generations, and authorized data placement. Prove exact coverage, unique updates, version-correct ghosts, checked extents, deterministic/reviewed accumulation or bounded numeric error, dose/objective equivalence to independent references, resource limits, and no unauthorized replication/logging. Encrypt and minimize migration/checkpoint data; bind restart to input/model/prescription/partition digests; reject partial or mixed-generation publication; use validated rollback and independent result gates. Test multiple P/topologies/partitions, tiny/irregular geometries, boundary organs, missing/corrupt messages, rank loss, restart at different P, numeric extremes, privacy access, audit completeness, and clinically approved reference cases. Required named reviewers include radiation oncologists, medical physicists/dosimetrists, numerical/HPC experts, imaging/geospatial specialists as applicable, privacy/security, operations, quality/regulatory, ethics, human-factors/accessibility, and independent clinical validation. No such external review is claimed by this answer.
