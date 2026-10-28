---
module_id: CONPAR-085
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 85
title: Halo Exchange and Stencil Computation
status: complete
last_verified: 2026-08-29
---

# Halo Exchange and Stencil Computation

## One-Page Review

### Governing question

How can a rank update owned stencil points using exactly the required, version-correct neighbor values while preserving ownership, boundary conditions, numerical semantics, memory safety, and progress across arbitrary decompositions?

### Essential definitions

- A **stencil** maps each output point from a fixed or data-dependent neighborhood of input points.
- A **halo/ghost region** stores read-only replicas of remotely owned input values.
- **stencil radius** is the maximum dependency distance in each direction; halo width must cover it for the scheduled update.
- A **face**, **edge**, or **corner** neighbor shares a codimension-one, -two, or -three boundary with a subdomain.
- A **star stencil** uses coordinate-direction neighbors; a **box stencil** may also use diagonal/corner neighbors.
- A **halo exchange plan** maps owned boundary slices to peer receive regions with exact counts, layouts, tags/collective slots, and generation.
- An **interior point** can be computed without current remote input; a **boundary point** depends on a halo or physical boundary value.
- **Jacobi/double-buffered update** reads one immutable generation and writes another; **in-place/Gauss-Seidel update** changes dependency order and mathematics.
- A **derived datatype** describes noncontiguous memory; **packing** explicitly copies it into contiguous messages.
- **neighborhood collective** exchanges with the logical topology's adjacent ranks.

### Central model, mechanism, or theorem

For time step t, rank r owns `V_r` and reads a snapshot `u^t`. For every dependency `(v,w)` of an owned output v, w is either local, a physical-boundary value, or a ghost copied from w's unique owner with matching field/schema, time t, and decomposition generation g. The exchange plan is reciprocal and buffers remain protected through completion. Only then may boundary outputs be computed into `u^(t+1)`. If these conditions hold and local arithmetic/order matches the stated numerical policy, the distributed update is extensionally equivalent to applying the same stencil to the global snapshot, within declared floating-point behavior.

### Critical invariants

Owned points are updated exactly once; ghosts are never treated as owners; every remote dependency has one compatible export/import; face/edge/corner coverage matches the stencil; physical, periodic, and partition boundaries remain distinct; send buffers contain time-t owned values and receive buffers target time-t ghosts; tags or collective neighbor slots cannot cross directions/fields/generations; counts/datatypes/extents fit; requests and datatype objects remain live; no output overwrites an input still required under snapshot semantics; boundary computation begins only after required receives complete; and global conservation/error oracles pass.

### Common failures

Teams allocate a one-cell halo for a radius-two stencil, exchange faces but omit diagonals, send newly updated rather than snapshot values, reverse `Cart_shift` source/destination, use the same tag for ambiguous peers, deadlock with blocking sends, unpack columns with the wrong stride, retain padding/uninitialized bytes, apply a wall at an internal cut, assume `MPI_PROC_NULL` fills a boundary buffer, update ghosts, reuse an active request, or benchmark communication without validating the numerical field.

### Compact example

Two ranks own `[1,2,3,4]` and `[5,6,7,8]` with fixed exterior zeros. Exchanging boundary values gives left rank's right ghost 5 and right rank's left ghost 4. Applying `y_i=u_(i-1)+2u_i+u_(i+1)` to the immutable snapshot yields `[4,8,12,16]` and `[20,24,28,23]`, exactly matching the global reference.

### Connections

[Domain Decomposition](084-domain-decomposition.md) supplies ownership, topology, and generations. [Point-to-Point Message Passing](082-point-to-point-message-passing.md) supplies request/buffer/matching semantics. [Collective Communication](083-collective-communication.md) supplies neighborhood collectives. The [program roadmap](../ROADMAP.md) next separates interior work from boundary completion to analyze communication-computation overlap.

## Governing Question

For each owned output and time generation, are all local, remote, periodic, and physical-boundary inputs the intended snapshot values, and does the communication/computation schedule preserve the mathematical stencil while remaining memory-safe and deadlock-free?

A halo is a distributed cache with a narrow consistency contract. Treating it as extra ordinary array storage obscures authority, freshness, and boundary semantics.

## Why This Matters

Stencil computations underlie finite differences, finite volumes, image filters, cellular automata, lattice methods, graph neighborhoods, and many iterative solvers. Their local arithmetic is often simple; correctness failures concentrate at partition boundaries, where index layouts, message matching, boundary conditions, and time generations meet.

Halo traffic can dominate strong scaling because owned volume shrinks faster than surface. It also interacts with vectorization, GPUs, derived datatypes, network topology, and overlap. A communication mechanism that is theoretically elegant may lose to packing; one that is fast may silently use stale or wrong-direction data.

The durable approach derives a halo plan from dependencies and ownership, proves snapshot equivalence, tests adversarial shapes and boundaries, and measures full verified iterations. MPI point-to-point, send-receive, neighborhood collectives, persistent requests, and mesh-library scatters are mechanisms within that proof.

## Prerequisites and Retrieval

Retrieve:

- owned/ghost sets, stable IDs, global-to-local maps, process topology, boundary classes, and migration generations from [Domain Decomposition](084-domain-decomposition.md);
- communicator context, exact envelopes/signatures, completion, requests, buffer lifetimes, progress, and deadlock from [Point-to-Point Message Passing](082-point-to-point-message-passing.md);
- collective order, neighborhood adjacency, nonblocking/persistent lifetime, and numeric policy from [Collective Communication](083-collective-communication.md); and
- data dependence and partition-independent update semantics from [Data Parallelism and Bulk Operations](042-data-parallelism-and-bulk-operations.md).

Retrieval prompt: record global/owned/ghost index bounds; field/schema/time/decomposition generation; stencil offsets/radius and star/box shape; neighbor order and boundary kind; per-peer send/receive slices/counts/datatypes/displacements/tags; buffer/request/object lifetime; update buffers/order; interior/boundary schedule; numeric/conservation oracle; device/host placement; progress/failure behavior; and evidence matrix.

## Learning Objectives

After completing this module, a learner can:

1. derive halo width and face/edge/corner neighbors from stencil offsets;
2. prove owner-to-ghost reciprocity, generation freshness, and physical-boundary correctness;
3. construct deadlock-free point-to-point, send-receive, or neighborhood exchange plans;
4. choose packing, derived datatypes, staged directional exchange, or direct device buffers;
5. distinguish Jacobi snapshot semantics from in-place order-dependent schemes;
6. handle periodic, nonperiodic, empty, thin, irregular, and multi-field subdomains;
7. establish safe request, buffer, datatype, and persistent-operation lifetimes;
8. validate distributed stencil results against serial/manufactured/conservation oracles;
9. measure halo bytes, latency, packing, arrival skew, boundary time, and verified iteration cost; and
10. scope numerical, privacy, operational, and high-stakes human review.

## Core Exposition

### Derive the halo from the operator

Write the stencil as an offset set `S subset Z^d`. A two-dimensional five-point star uses `(0,0),(±1,0),(0,±1)`; a nine-point box also uses `(±1,±1)`. A radius-two operator extends offsets to distance two. The halo is not guessed from code layout: for every owned point v and offset s, determine whether v+s is owned, remote, periodic, physical-boundary, or invalid.

For a rectangular subdomain and fixed radius h, faces need h layers. Edges and corners are required only when the offset set reaches them or when a staged exchange deliberately forwards previously received data. A direct box exchange can send faces, edges, and corners to all corresponding neighbors. A staged x-then-y exchange can make y messages include x halos, propagating corners; the order, extents, and generation must be proved. Exchanging only original face interiors in both stages leaves corners stale.

Data-dependent neighborhoods require an upper bound or a discovery protocol. Adaptive meshes may need coarse-fine interpolation/restriction, not a bytewise copy. Particles need a geometric ghost thickness derived from interaction cutoff, motion bound, and neighbor-list rebuild policy. The abstract obligation remains: every remote read has a documented owner and valid transformation.

### Snapshot semantics and update order

In a Jacobi-style step, all outputs at t+1 read the immutable global state at t. Use separate input/output arrays or equivalent versioning. Pack sends from owned `u^t`, post receives into halo `u^t`, compute safe interior from `u^t`, complete receives, compute boundary outputs into `v`, then swap only after all owned outputs and required global decisions finish.

Updating `u` in place can read a mixture of t and t+1. That may be intentional Gauss-Seidel/red-black mathematics, but rank scheduling and partition order then affect results unless explicitly coordinated. Do not call it an optimization of Jacobi. State the operator, ordering, convergence theory, and reproducibility policy anew.

Temporal blocking computes several local time steps per exchange by using a wider halo or redundant boundary work. For k steps of radius h, the dependence cone can require k*h layers. Boundary regions shrink per local substep. This trades bytes/messages for duplicate work and storage and must preserve boundary/time indexing.

### Build a reciprocal exchange plan

For each peer and field, define ordered global IDs or a geometric slice exported from owned input and the matching local ghost targets imported. Prove equal type signatures/counts and correct peer direction. Tag point-to-point messages by field, direction, time modulo a safe reuse window, and protocol generation, or isolate fields/generations with communicators. Avoid wildcard receives where direction/version is protocol state.

Post receives before sends for nonblocking protocols, then wait/test and validate statuses/counts. `MPI_Sendrecv` expresses one simultaneous send and receive and helps avoid cyclic blocking-send dependencies; its send and receive buffers must follow the API's disjointness/replacement rules. `MPI_PROC_NULL` makes off-end communications no-ops, but a receive from it does not fill the buffer—initialize/apply the physical boundary explicitly.

Cartesian `MPI_Cart_shift` returns the source from which data is received and destination to which data is sent for a direction/displacement. Draw a one-dimensional three-rank case and verify the orientation. Periodicity changes off-end neighbors. Ranks may be reordered, so use the returned topology communicator.

Neighborhood collectives derive peer order from Cartesian or graph topology. `Neighbor_alltoallw` supports per-neighbor counts, byte displacements, and datatypes, useful for faces with distinct layouts. Neighbor order can include repeated/self neighbors in small periodic dimensions; follow the standard's order and do not collapse entries casually. Blocking, nonblocking, and persistent variants have collective matching and protected-argument lifetimes.

### Pack or describe noncontiguous boundaries

A row-major horizontal row is contiguous; a vertical column is strided. Packing copies selected owned values to a contiguous buffer and unpacks received data. It costs memory traffic and code but offers explicit order, easy checksums, and predictable device staging. Derived vector/subarray/struct datatypes describe noncontiguous regions and can avoid application packing, but the MPI implementation may pack internally and datatype extent/lower-bound mistakes can corrupt layouts.

Check counts and displacements with wide arithmetic. Derived type signature compatibility concerns basic elements, while extent controls repetition and buffer reach. Commit datatypes before use and keep them live through nonblocking/persistent completion. Do not include uninitialized padding or sensitive adjacent fields. Benchmark complete verified exchanges, not just call overhead.

Multi-field structures may use array-of-structures boundaries, separate field messages, or structure datatypes. Combining messages amortizes startup but may send unused fields and couple lifetimes. Separate messages improve selectivity but increase request/tag pressure. A structure-of-arrays layout often helps stencil vectorization and field-specific communication.

### Executable snapshot model

This deterministic Python model represents two ranks, one exchanged interface value in each direction, fixed exterior zeros, and one radius-one Jacobi update. It does not call MPI, model asynchronous progress, derived datatypes, multidimensional corners, floating error, or performance.

<!-- bijux-verify: {"id":"two-rank-halo-stencil","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"rank0_owned=[1, 2, 3, 4]\nrank1_owned=[5, 6, 7, 8]\nrank0_ghosts=(left=0,right=5)\nrank1_ghosts=(left=4,right=0)\nrank0_next=[4, 8, 12, 16]\nrank1_next=[20, 24, 28, 23]\nglobal_next=[4, 8, 12, 16, 20, 24, 28, 23]\nreference_next=[4, 8, 12, 16, 20, 24, 28, 23]\nmatch=True\n","stderr":""}} -->
```python
rank0 = [1, 2, 3, 4]
rank1 = [5, 6, 7, 8]
rank0_left, rank0_right = 0, rank1[0]
rank1_left, rank1_right = rank0[-1], 0


def stencil(owned, left_ghost, right_ghost):
    extended = [left_ghost] + owned + [right_ghost]
    return [
        extended[index] + 2 * extended[index + 1] + extended[index + 2]
        for index in range(len(owned))
    ]


next0 = stencil(rank0, rank0_left, rank0_right)
next1 = stencil(rank1, rank1_left, rank1_right)
global_values = rank0 + rank1
reference = stencil(global_values, 0, 0)
result = next0 + next1
print(f"rank0_owned={rank0}")
print(f"rank1_owned={rank1}")
print(f"rank0_ghosts=(left={rank0_left},right={rank0_right})")
print(f"rank1_ghosts=(left={rank1_left},right={rank1_right})")
print(f"rank0_next={next0}")
print(f"rank1_next={next1}")
print(f"global_next={result}")
print(f"reference_next={reference}")
print(f"match={result == reference}")
```

### Physical and periodic boundaries

A no-neighbor result is a topology fact, not a boundary value. Apply Dirichlet, Neumann, Robin, reflective, inflow/outflow, or application-specific conditions with correct geometry, units, time, and order. A second-order condition may require multiple layers or one-sided formulas. Corners where conditions meet need an explicit precedence/compatibility rule.

Periodic boundaries map global off-end coordinates to the opposite side and exchange with the corresponding owner. In a process dimension of size one, a rank can be its own periodic neighbor; do not alias send and receive regions illegally or apply an exchange twice. In dimensions of size two, the negative and positive neighbor can be the same rank but occupy distinct topology slots and buffer regions.

For conservative finite-volume methods, compute or reconcile interface fluxes so adjacent cells receive equal-and-opposite contributions. Exchanging state alone does not guarantee identical flux if geometry, coefficients, or floating order differ. An owner-computes flux protocol or a proved deterministic shared formula can enforce conservation.

### Irregular meshes and sparse halos

For an unstructured mesh, halo plans are sparse global-ID lists derived from cell/face/degree-of-freedom adjacency. A ghost may be needed by multiple local entities but imported once per field/version. Sort/canonicalize lists where reproducibility helps, while preserving the peer's agreed order. Verify every import/export pair by IDs, not only byte counts.

Adaptive coarse-fine interfaces may exchange restriction, prolongation, flux correction, or constraint data. The transformation belongs in the numerical specification. Mesh changes invalidate exchange plans and datatype addresses; rebuild them under the new decomposition generation before use.

Graph neighborhood collectives can express sparse peers, including directed indegree/outdegree. Edge weights/topology hints do not validate application schemas. Very high-degree partitions create request and metadata pressure; reconsider decomposition, aggregate messages, and impose quotas.

### Devices, memory spaces, and progress

GPU-aware MPI may accept device buffers, but support depends on implementation, transport, allocation type, and synchronization. Ensure producing kernels complete before communication reads; ensure communication completes before consuming kernels; preserve stream/event/buffer lifetimes. If staging through host memory, include device-host copies and pinned-buffer capacity in the schedule and measurement.

Nonblocking initiation alone is not overlap. MPI may require calls or a progress thread; packing and boundary dependencies can consume the alleged overlap window. This module establishes the safe split—post exchange, compute independent interior, complete exchange, compute boundary. The next module measures whether it shortens the critical path.

Persistent neighborhood/point-to-point requests can amortize repeated setup for fixed topology/buffers. Initialization binds arguments; start activates; completion returns inactive; topology, datatype, count/displacement arrays, and buffers must remain valid as required. Repartitioning invalidates the bound plan.

### Verification and operations

Unit-test each direction with unique coordinate-encoded values so swaps/transposes are visible. Test one rank; P greater than cells; one-cell-wide/two-cell-wide parts; radius larger than local extent; non-square dimensions; star and box stencils; face/edge/corner paths; periodic/nonperiodic/self/repeated neighbors; reordered ranks; multiple fields/types; zero and huge counts; packed/derived/device paths; and generations across repartition.

Compare full distributed outputs with a direct global reference for small cases and manufactured analytical solutions for numerical codes. Poison halos before exchange, checksum per-peer ID/value sequences, verify statuses/counts, and test two consecutive time steps to catch stale/new-buffer confusion. Check conservation, symmetry, constant/linear field behavior, residual/error norms, and acceptable floating variation.

Inject delayed, duplicated-at-application-level, wrong-generation, wrong-tag, truncated, and missing peer behavior only in controlled tests with timeouts; ordinary MPI error recovery is not guaranteed. Define abort/checkpoint/restart or a separately supported fault model. Never publish partial-rank fields.

Retain runtime/compiler/MPI/transport/device versions, topology/placement, decomposition and exchange-plan digests, stencil/schema/time generations, per-peer counts/bytes, packing/copy/communication/interior/boundary timings, wait and arrival skew, request high-water mark, validation results, failures, and cleanup. Redact sensitive field values and coordinates; halos, traces, dumps, and checkpoints expand disclosure.

## Definitions and Notation

- `V_r`: owned points of rank r.
- `H_r`: ghost points stored by rank r.
- `S`: stencil offset set; `h`: maximum radius/halo width.
- `u^t`: immutable input field at time/iteration t.
- `v=u^(t+1)`: output field for a Jacobi-style step.
- `owner(w)`: unique owner of global point w.
- `g`: decomposition/exchange-plan generation.
- `B_phys`, `B_part`, `B_per`: physical, partition, and periodic boundaries.
- `E_(r->s)`: ordered export from rank r to rank s.
- `I_(s<-r)`: matching import/ghost targets on rank s.
- `Q`: request set; `D`: committed datatype set.
- `F(v,{u(w)})`: stated local stencil operator.
- `Obs`: partition-independent numerical/result contract.

Ghost freshness is the tuple `(global_id,field,schema,t,g)`, not merely “received.”

## Mechanisms, Invariants, or Proof Structure

### Dependency-coverage proof

For every owned v and offset s in S, classify w=v+s. If w is global, it is owned locally or appears exactly once in the required ghost map from `owner(w)`; otherwise an explicit physical condition supplies the value. Star/box and radius determine faces, edges, and corners.

### Reciprocity and matching proof

For every peer pair, ordered export IDs/basic type signature equal ordered import IDs/signature. Communicator, peer direction, tag or neighbor slot, field/schema, t, and g identify the exchange. Counts/extents/targets fit, and statuses validate actual receives.

### Snapshot and memory proof

All sends and local reads use protected `u^t`; receives populate only `H_r^t`; outputs write disjoint `v`. Requests, buffers, count/displacement arrays, communicators, and datatypes live through completion. Boundary outputs begin only after their required receives; swap occurs after all owned outputs finish.

### Extensional-equivalence proof

For each owned v, the distributed operand tuple equals the operand tuple of the global reference at t: local values by ownership, remote values by validated ghosts, off-domain values by identical boundary policy. Applying identical F yields identical exact output, or output within the declared floating/order policy.

### Conservation and evidence proof

Each partition interface flux/update is accounted once under the stated rule; global totals and manufactured/reference fields pass across partitions and P. Performance claims compare complete validated iterations and include packing, copies, progress, wait, boundary work, and instrumentation.

## Alternatives and Trade-Offs

| Mechanism | Main benefit | Principal limitation |
|---|---|---|
| blocking send/receive ordering | simple primitives | fragile deadlock/order protocol |
| `Sendrecv` directional shift | deadlock-resistant paired step | sequential directions and buffer rules |
| nonblocking point-to-point | flexible peers and overlap | request/tag/lifetime complexity |
| neighborhood collective | topology-derived sparse exchange | collective order/neighbor-slot complexity |
| persistent exchange | amortized repeated setup | bound state and invalidation complexity |
| explicit packing | transparent order/checksums | extra copies/buffers |
| derived datatypes | concise noncontiguous layout | extent/performance/debug complexity |
| direct face/edge/corner | one logical exchange stage | more peers/messages |
| staged directional exchange | fewer direct corner peers | forwards halos; order/extents matter |
| wider halo/temporal blocking | fewer exchange rounds | memory and redundant computation |

Choose from semantic clarity and target evidence; do not weaken snapshot, boundary, or validation contracts to reduce a timing.

## Failure Modes and Misconceptions

- **“Halo width equals one.”** derive width from offsets and local time blocking.
- **“Faces cover a box stencil.”** diagonal dependencies need corners or proved staging.
- **“Ghosts are extra owned cells.”** they are versioned read-only replicas.
- **“No neighbor means zero.”** physical conditions set values; `PROC_NULL` leaves receive buffers unchanged.
- **“Rank arithmetic finds neighbors.”** query the topology, especially after reordering.
- **“Same peer means one topology slot.”** small periodic dimensions may repeat neighbors.
- **“Same count means same data.”** global IDs, order, field, schema, t, and g must match.
- **“Derived datatypes eliminate packing.”** implementations may pack, and extents remain risky.
- **“In-place is just lower memory.”** it can change the numerical iteration.
- **“Waitall validates the message.”** inspect protocol/status/count and result oracles.
- **“Nonblocking automatically overlaps.”** progress and independent work are required.
- **“Persistent requests survive repartition.”** bound topology/buffers/plans can become invalid.
- **“Periodic self-neighbors need no care.”** aliasing and duplicate slots still matter.
- **“One correct time step is enough.”** stale/swap errors often appear on the next step.
- **“Matching global sum proves the field.”** permutations can preserve sums; compare local structure/reference.
- **“Fast halos prove simulation validity.”** discretization, units, convergence, and domain review remain.

## Worked Examples

### Example 1

**Radius mismatch.** A fourth-order one-dimensional derivative reads two points each side, but the code exchanges one layer. The first owned boundary uses an old second ghost. **Conclusion:** halo width follows the dependency radius.

### Example 2

**Missing corners.** A nine-point image filter exchanges north/south/east/west rows only. Four corner outputs read poison. Direct diagonal messages or staged extended faces supply them. **Conclusion:** derive neighbor classes from S.

### Example 3

**Wrong shift orientation.** Rank sends its west edge to the source returned for a +x shift instead of the destination, swapping semantics. Draw coordinates and pair `receive source` with `send destination`. **Conclusion:** name directions by data flow, not variable folklore.

### Example 4

**Physical off-end.** `MPI_PROC_NULL` completes a receive without modifying its target. The prior time step remains in the halo. Initialize/apply the Dirichlet value after classification. **Conclusion:** a no-op is not boundary initialization.

### Example 5

**Column extent.** A vector datatype selects one element per row, but repeating count 2 advances by its full extent and reaches the wrong second column. Use count 1 per boundary or a resized/verified type. **Conclusion:** signature and extent solve different problems.

### Example 6

**Snapshot violation.** Rank 0 updates its boundary before packing while rank 1 packs old state. The method becomes partition-order dependent. Pack/protect `u^t` and write `v`. **Conclusion:** buffer discipline is numerical semantics.

### Example 7

**Repeated periodic neighbor.** Two ranks in a periodic x dimension see the same peer in both directions. Collapsing two neighbor slots loses distinct left/right regions. **Conclusion:** peer identity does not replace topology position.

### Example 8

**Conservation failure.** Adjacent finite-volume ranks compute interface flux with different reconstructed geometry, causing unequal values. Assign a flux owner or exchange/reconcile the flux and check equal-and-opposite updates. **Conclusion:** state freshness alone does not prove conservation.

### Example 9

**Packing comparison.** A derived column type wins for large CPU grids; explicit pinned packing wins for a GPU path because device staging dominates. Both return identical fields. **Conclusion:** benchmark complete valid paths per target.

### Example 10

**Coastal storm-surge stencil.** Exchanges must preserve bathymetry/mesh/coordinate/vertical-datum versions, wet-dry state, boundary forcing, units, time and decomposition generations, conservative fluxes, uncertainty, privacy for critical infrastructure, failure/restart lineage, and publication gates. Named oceanography/coastal-engineering, meteorology, geospatial/datum, numerical/HPC, emergency-management, infrastructure, privacy/security, operations, quality/regulatory, accessibility/human-factors, and independent validation reviewers must approve evidence; none is claimed here. **Conclusion:** fresh halos do not establish forecast accuracy or decision safety.

## Cross-Program Connections

- **Numerical analysis:** discretization order, stability, convergence, conservation, and manufactured solutions govern stencil validity.
- **Compilers:** loop nests, tiling, vectorization, aliasing, and layout govern local kernels.
- **Networks:** message aggregation, topology, latency, bandwidth, and progress govern halo cost.
- **Distributed systems:** versioned caches, ownership, epochs, retries, and stale-message rejection recur.
- **Databases:** replicas, freshness, partition boundaries, and consistent snapshots are analogous.
- **GPU computing:** device buffers, streams, staging, and kernel dependencies extend lifetime proofs.
- **Geometry/meshes:** adjacency, periodicity, coarse-fine constraints, and coordinate systems define remote values.
- **Testing:** coordinate encodings, poison, manufactured solutions, faults, and multiple partitions expose boundary defects.
- **Security/privacy:** ghosting, packing padding, traces, dumps, and checkpoints expand disclosure.
- **Operations:** exchange-plan digests, wait skew, request pressure, failures, and restart lineage sustain jobs.

## References

1. MPI Forum, *MPI: A Message-Passing Interface Standard, Version 5.0*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report.pdf>
2. MPI Forum, *MPI-5.0: Blocking Send-Receive*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node64.htm>
3. MPI Forum, *MPI-5.0: Null MPI Processes*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node86.htm>
4. MPI Forum, *MPI-5.0: Topology Inquiry Functions*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node230.htm>
5. MPI Forum, *MPI-5.0: Nonblocking Neighborhood Communication*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node237.htm>
6. MPI Forum, *MPI-5.0: Persistent Neighborhood Communication*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node240.htm>
7. MPI Forum, *MPI-5.0: Neighborhood Communication Application Example*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node243.htm>
8. PETSc Team, *Vectors and Parallel Data: Local/Global and Ghost Communication*, PETSc 3.25 documentation; retrieved 2026-08-29. <https://petsc.org/release/manual/vec/>
9. PETSc Team, *DMDA Structured Grids*, PETSc 3.25 documentation; retrieved 2026-08-29. <https://petsc.org/release/manualpages/DMDA/>
10. LAMMPS Project, *LAMMPS Overview: Spatial Decomposition and Ghost Atoms*, current documentation; retrieved 2026-08-29. <https://docs.lammps.org/Intro_overview.html>

## Exercises

### Exercise 1

For a two-dimensional radius-two box stencil, enumerate required offset classes and state direct and staged halo strategies, including minimum width and corner handling.

### Exercise 2

Trace one Jacobi time step for three one-dimensional ranks owning `[1,2]`, `[3,4]`, and `[5,6]` with periodic boundaries and operator `y_i=u_(i-1)+u_i+u_(i+1)`. Give every ghost and output.

### Exercise 3

Diagnose a four-rank code whose first step matches a reference but second step differs only at partition boundaries. It packs after updating local interiors, receives into the input array, and swaps buffers immediately after `Waitall`. Provide a corrected schedule and tests.

### Exercise 4

Design and compare direct nonblocking point-to-point, `Sendrecv`, and persistent neighborhood-alltoallw plans for a repeated 3-D radius-one box stencil with CPU and GPU fields. Include correctness and measurement criteria.

### Exercise 5

Transfer the framework to a distributed radiotherapy dose-accumulation stencil over deforming patient images. Specify freshness, geometry/units/numeric/privacy/failure invariants, validation, evidence, publication gates, and named reviewer roles without claiming review.

## Answers to the Exercises

### Answer 1

Offsets are all `(dx,dy)` with `dx,dy in {-2,-1,0,1,2}`, including center: axial face directions, diagonal combinations, and two-layer reach. A direct plan exchanges width-two north/south/east/west regions and the four width-two corner blocks with eight neighbors (exact slice sizes depend on owned dimensions). A staged x-then-y plan first exchanges two x layers; the y exchange then includes the received x halos so its row width is `owned_x+4`, thereby forwarding corners. If y messages include only owned x, corners remain invalid. Both plans tag field,t,g, protect snapshot buffers, and separately apply physical/periodic conditions.

### Answer 2

Periodic global sequence is `[1,2,3,4,5,6]`. Rank 0 ghosts are left 6 from rank 2 and right 3 from rank 1; outputs are `6+1+2=9` and `1+2+3=6`. Rank 1 ghosts are 2 and 5; outputs `2+3+4=9`, `3+4+5=12`. Rank 2 ghosts are 4 and 1; outputs `4+5+6=15`, `5+6+1=12`. Concatenated `[9,6,9,12,15,12]` equals the periodic global reference. Direction slots remain distinct even if a tiny process topology repeats peers.

### Answer 3

The code violates snapshot/lifetime separation: sends can include t+1 interior values, receives overwrite t inputs, and swap may occur before boundary outputs or send-buffer release logic. Correct sequence: keep immutable `u^t`; post receives into dedicated `halo^t`; pack/post sends from owned `u^t`; compute only outputs whose complete dependency set is local into `v`; complete and validate receives; compute boundary outputs from `u^t+halo^t`; complete every request; validate owned result; then swap `u,v`. Tests use coordinate-encoded values, poisoned halos, two or more steps, varied P and narrow parts, delayed peers, message digests, and full global reference comparisons.

### Answer 4

All plans derive 26-neighbor box dependencies (fewer at physical boundaries), exact face/edge/corner slices, matching IDs/types, and snapshot generations. Point-to-point posts all receives then sends with direction/field/t/g-safe matching and is most flexible. `Sendrecv` pairs directions in a deadlock-resistant sequence but serializes stages and needs careful disjoint/replacement buffers. Persistent neighborhood-alltoallw binds per-neighbor counts, byte displacements, derived types, topology, and buffers; it may amortize setup but must be inactive before restart and rebuilt after layout changes. CPU candidates compare explicit pack with verified datatypes. GPU candidates qualify direct device support and streams versus pinned staging. Validate identical global fields, boundaries, conservation/error norms, and statuses under varied sizes/topologies; measure packing, copies, initiation, progress CPU, communication, wait skew, interior/boundary kernels, memory/request pressure, and complete iteration distributions.

### Answer 5

Key freshness is `(anonymized global voxel/control ID, dose field/schema, image/deformation/model/prescription version, fraction/time, decomposition generation)`. Prove unique ownership, exact dependency/halo coverage, coordinate-frame and length/dose units, approved interpolation and boundary behavior, protected snapshots, checked extents, conservative/reviewed accumulation, bounded numeric error, authorized placement, encryption, redacted telemetry, and no stale or partial publication. Bind checkpoints/restarts to image, registration, contour, plan, model, mapping, and exchange digests; abort or roll back mixed generations. Test manufactured fields, independent dose/registration references, multiple P/partitions, narrow/irregular organs, deformation extremes, missing/corrupt/delayed messages, rank loss/restart at changed P, numeric extremes, access controls, and audit completeness. Publication requires independent result validation and named radiation oncologist, medical physicist/dosimetrist, imaging/registration, numerical/HPC, privacy/security, operations, quality/regulatory, ethics, accessibility/human-factors, and safety reviewers. No external review or clinical validity is claimed.
