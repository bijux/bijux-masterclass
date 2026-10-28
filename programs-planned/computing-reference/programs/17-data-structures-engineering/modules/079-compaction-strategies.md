---
module_id: DSE-079
program: Data Structures Engineering
level: 2
module_number: 79
title: Compaction Strategies
status: complete
last_verified: 2026-08-30
---

# Compaction Strategies

## One-Page Review

### Governing question

How should an LSM-based system choose, execute, and publish compactions so that it controls read, write, and space amplification without violating version, tombstone, snapshot, or crash-consistency semantics?

### Essential definitions

- **Compaction** merges immutable sorted inputs, resolves entries only when visibility rules permit, writes new immutable outputs, and atomically replaces the input set in metadata.
- A **trigger** decides when work is eligible; a **picker** chooses the exact files and key range; a **scheduler** assigns resources and ordering; an **installer** publishes validated outputs.
- **Leveled compaction** maintains bounded overlap in stable levels and commonly rewrites a selected run with all overlapping files in the next level.
- **Tiered** or **size-tiered compaction** combines several similarly sized sorted runs, reducing rewrite frequency while retaining more runs.
- **Universal compaction** is RocksDB's tiered family; names are implementation-specific and must not replace an explicit policy description.
- **FIFO/time-based compaction** removes or groups old files under cache, TTL, or mostly immutable time-series assumptions.
- **Overlap closure** is the complete set of files required by a selected key interval and policy. Partial closure can leave duplicate versions split across old and new structures.
- **Compaction debt** is pending rewrite work. If arrivals create debt faster than sustained compaction capacity removes it, the system is unstable without throttling or admission control.
- **Write/read/space amplification** measure physical bytes written, sources consulted, and physical storage relative to a stated logical baseline and workload.

### Central model, mechanism, or theorem

A durable design separates correctness from optimization. The correctness kernel is:

1. pin a manifest/version and select a policy-valid, overlap-complete input set;
2. merge in internal-key order while applying snapshot, tombstone, range-deletion, TTL, and merge-operator rules conservatively;
3. produce checksummed, bounded, non-overlapping outputs with declared key ranges;
4. durably publish one metadata edit that adds all outputs and removes all inputs;
5. reclaim inputs only after readers and recovery no longer reference them.

Leveled and tiered policies choose different points in a workload-dependent trade space. In a simplified hierarchy with size ratio T and L disk levels, leveling often offers roughly one sorted run per nonzero level but can rewrite data against much larger overlapping levels; tiering retains up to roughly T runs per tier and usually rewrites each item less often. These are asymptotic intuitions, not portable performance promises. File sizes, overlap, updates, deletes, skew, caching, filters, compression, storage, concurrency, and implementation details determine measured results.

For stability over a measurement interval, useful compaction service capacity must exceed debt creation on average, with enough burst headroom. Queue length alone is insufficient: track pending bytes, estimated rewrite bytes, oldest debt age, L0/run pressure, throughput, stalls, and temporary space.

### Critical invariants

1. Selection includes every file required by the policy's transitive overlap rules in the affected levels/range.
2. Inputs remain immutable and pinned throughout the job; concurrent jobs have conflict-free input/output ranges or explicit coordination.
3. Entry elimination is justified by complete coverage plus visibility, snapshot, tombstone, TTL, merge, and replication/repair constraints—not merely age.
4. Outputs are sorted, internally valid, checksummed, bounded, and non-overlapping where the target level promises non-overlap.
5. A single durable manifest edit installs all outputs and retires all inputs; readers see a valid pre- or post-compaction version.
6. Input deletion waits for successful installation, recovery durability, and reader/reference release.
7. Scheduling is bounded and observable; foreground work retains required I/O, CPU, memory, cache, file-descriptor, and space headroom.

### Common failures

- Compacting a seed file without all required overlaps, then exposing duplicate or hidden versions across old and new files.
- Dropping a tombstone before every older covered value is unreachable to reads, snapshots, repair, or replication.
- Treating TTL expiry, file age, or a time window as proof that every contained record is obsolete.
- Publishing outputs one by one or deleting inputs before the manifest edit is durable.
- Optimizing only write amplification while read fan-out, temporary space, or tail latency becomes unacceptable.
- Scheduling only the largest score, starving old or small ranges and accumulating localized debt.
- Running too many compactions, exhausting bandwidth/cache/CPU, and making foreground latency worse.
- Measuring completed bytes instead of useful debt removed, so repeated rewrites appear productive.

### Compact example

Four equal-sized L0 files and four non-overlapping L1 files illustrate two legal selections. Oldest-first leveled selection starts at `f0[10,19]`; overlapping L0 `f1` expands the interval, so complete L1 closure is `g0[0,14]` and `g1[15,29]`. The four selected files contain 20 fixture byte-units. A tiered picker instead selects the four equal-sized L0 runs, totaling 8 units. This demonstrates selection shape only; declared output sizes do not prove real amplification.

### Connections

DSE-076 supplies LSM visibility and manifest foundations, DSE-077 immutable sorted-run format, DSE-078 probabilistic read pruning, and DSE-080 amplification analysis. Database Engineering adds MVCC, recovery, replication, and query service objectives; Data Engineering adds lake-table compaction, streaming state, late data, and distributed scheduling.

## Governing Question

How can compaction policy reduce accumulated immutable-run debt while preserving the exact logical history required by concurrent readers and recovery?

## Why This Matters

Flushing converts random updates into sequential immutable files, but it postpones work. Without compaction, run count grows, negative and range reads inspect more sources, obsolete versions and tombstones occupy space, metadata expands, and eventually file or level limits stall writes. Compaction pays that deferred cost by reading, merging, and rewriting data.

The policy is consequential because no strategy minimizes every amplification simultaneously. Aggressive leveling can make reads predictable and reclaim overwritten data promptly, yet rewrite hot ranges repeatedly. Tiering can sustain write-heavy ingestion with fewer rewrites, yet leaves more overlapping runs and temporary duplicate storage. Time-window organization can cheaply expire immutable TTL data, yet late updates and tombstones can cross windows. FIFO can be excellent for a disposable cache and catastrophically wrong for authoritative durable data.

Correctness and operations meet at publication. A logically correct merge is still unsafe if output files are partially installed, input files are removed too early, or a concurrent reader loses its pinned version. An elegant cost model is operationally irrelevant if compaction cannot keep up with arrivals or consumes all I/O bandwidth. Production engineering therefore needs a proof obligation, a resource controller, and evidence tied to a defined workload.

## Prerequisites and Retrieval

Retrieve:

- internal versus user keys, sequence order, point/range tombstones, merge operands, TTL, and snapshot visibility;
- immutable SSTables, key ranges, checksums, indexes, filters, manifests/version sets, write-ahead recovery, and file lifecycle;
- multiway merge, priority queues, intervals, transitive closure, partitioning, and external-memory cost;
- write, read, and space amplification with explicit logical/physical denominators;
- queue stability, service rate, backpressure, starvation, fairness, tail latency, and resource isolation;
- property testing, crash injection, fault simulation, model checking, workload replay, and steady-state benchmarking.

Diagnostic retrieval: choosing compaction inputs is not merely an optimization. If target-level files overlap the selected interval, they are part of the semantic context needed to decide which older entries can disappear and to preserve the target level's overlap invariant.

## Learning Objectives

After this module, you can:

1. decompose compaction into trigger, selection, merge, output partitioning, installation, reclamation, and scheduling;
2. derive overlap closure and detect incomplete leveled selections;
3. compare leveled, tiered/universal, hybrid/unified, FIFO, and time-window strategies under stated workloads;
4. state safe conditions for dropping versions, tombstones, expired entries, and merge operands;
5. design crash-atomic publication and reader-safe input reclamation;
6. estimate and measure compaction debt, service capacity, temporary space, and foreground interference;
7. design fair, conflict-aware scheduling and bounded subcompaction;
8. validate a policy with structural, semantic, recovery, adversarial, and steady-state evidence.

## Core Exposition

**Separate the control plane from the merge kernel.** A trigger observes pressure: number of L0 files, bytes over a level target, overlapping runs, tombstone density, expired files, oldest debt, or manual intent. A picker turns that pressure into an exact input set and output level/range. A scheduler admits nonconflicting jobs under resource budgets. The merge kernel produces output entries. An installer commits one version edit. Keeping these interfaces explicit prevents a heuristic score from silently changing correctness.

**Define the compaction unit.** A file-only picker is often insufficient. Under leveled organization, selecting one source file requires all target-level files overlapping its range. Overlapping source files may expand that range, which may require more target files, until a fixed point is reached. Some implementations use clean cuts, grandparents, sublevel boundaries, or compaction pointers; each must state its closure rule. The proof obligation is that no unselected file in a level whose non-overlap is being restored intersects the final output interval in a forbidden way.

**Model bounded selection.** The following deterministic model compares an overlap-closed leveled selection with an equal-size tiered selection. Its byte units and obsolete-byte estimates are fixtures, not observations from a storage engine.

<!-- bijux-verify: {"id":"compaction-selection-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"files=8\nleveled_seed=f0\nleveled_selection=f0,f1,g0,g1\nleveled_input_bytes=20\nleveled_output_bytes=18\nleveled_overlap_complete=True\ntiered_selection=f0,f1,f2,f3\ntiered_input_bytes=8\ntiered_output_bytes=7\ntiered_size_ratio=1.0\noldest_first=True\ninputs_immutable=True\nvalid=True\nevidence=bounded_compaction_selection_model\n","stderr":""}} -->
```python
from typing import NamedTuple


class File(NamedTuple):
    name: str
    level: int
    low: int
    high: int
    size: int
    age: int


files = (
    File("f0", 0, 10, 19, 2, 4),
    File("f1", 0, 15, 24, 2, 3),
    File("f2", 0, 40, 49, 2, 2),
    File("f3", 0, 70, 79, 2, 1),
    File("g0", 1, 0, 14, 8, 4),
    File("g1", 1, 15, 29, 8, 3),
    File("g2", 1, 30, 59, 8, 2),
    File("g3", 1, 60, 89, 8, 1),
)


def overlaps(file, low, high):
    return not (file.high < low or high < file.low)


seed = max((file for file in files if file.level == 0), key=lambda file: file.age)
selected = {seed.name}
while True:
    chosen = [file for file in files if file.name in selected]
    low = min(file.low for file in chosen)
    high = max(file.high for file in chosen)
    expanded = selected | {
        file.name for file in files if file.level in (0, 1) and overlaps(file, low, high)
    }
    if expanded == selected:
        break
    selected = expanded

leveled = [file for file in files if file.name in selected]
final_low = min(file.low for file in leveled)
final_high = max(file.high for file in leveled)
closure = {
    file.name for file in files if file.level in (0, 1) and overlaps(file, final_low, final_high)
}
overlap_complete = closure == selected
tiered = [file for file in files if file.level == 0 and file.size == seed.size]
ratio = max(file.size for file in tiered) / min(file.size for file in tiered)
leveled_names = ",".join(file.name for file in leveled)
tiered_names = ",".join(file.name for file in tiered)
oldest_first = seed.name == "f0"
inputs_immutable = isinstance(files, tuple) and all(isinstance(file, tuple) for file in files)
valid = overlap_complete and ratio == 1.0 and oldest_first and inputs_immutable
print(f"files={len(files)}")
print(f"leveled_seed={seed.name}")
print(f"leveled_selection={leveled_names}")
print(f"leveled_input_bytes={sum(file.size for file in leveled)}")
print("leveled_output_bytes=18")
print(f"leveled_overlap_complete={overlap_complete}")
print(f"tiered_selection={tiered_names}")
print(f"tiered_input_bytes={sum(file.size for file in tiered)}")
print("tiered_output_bytes=7")
print(f"tiered_size_ratio={ratio:.1f}")
print(f"oldest_first={oldest_first}")
print(f"inputs_immutable={inputs_immutable}")
print(f"valid={valid}")
print("evidence=bounded_compaction_selection_model")
```

The closure includes `g0` because the selected source interval reaches key 10, and `g1` because it reaches key 24. It excludes `g2`; inclusive intervals 0–29 and 30–59 do not overlap. The model has no records, sequences, tombstones, snapshots, output builder, filesystem, crash, concurrency, cache, or I/O. Frozen Python objects approximate input immutability only within this process. The declared 18- and 7-unit outputs assume removable obsolete bytes; execution does not derive their semantic safety. The run proves only the stated finite selection properties.

**Leveled compaction bounds overlap.** Stable nonzero levels are usually divided into sorted, non-overlapping files, and each level has a byte target larger than the preceding one. When a level exceeds target, a picker selects source data and overlapping data in the next level. Reads then consult at most one file per stable nonzero level for a point key, plus overlapping L0 files. The price is repeated rewriting: a small source range may overlap much more target data. Compaction pointers or round-robin selection can spread work and prevent repeatedly choosing only hot score winners.

**Tiered compaction delays rewriting.** A size-tiered picker waits for several similarly sized runs and merges them into a larger run. Because inputs have comparable sizes, an item is not immediately rewritten against an entire much-larger next level. The system retains more sorted runs, so negative reads, range merge width, metadata, and temporary space can grow. “Universal” is RocksDB terminology for its tiered strategy; it includes size-amplification and run-count controls rather than meaning a universally optimal policy.

**Use hybrid policies deliberately.** Real systems mix behaviors. L0 is naturally tiered because flushes add overlapping runs; higher levels may be leveled. A unified policy can parameterize the continuum per hierarchy region. Hybrid selection should be described through trigger, layout, granularity, and movement rules rather than only a product label. A migration must tolerate existing files and prove that each intermediate layout is readable and recoverable.

**Restrict FIFO to disposable semantics.** FIFO drops oldest files to satisfy a size or age policy. This can suit caches where eviction is part of the contract. It does not merge away shadowed values and does not by itself establish TTL expiration for every record. A file with a new value in an old file, or an old value in a new file, defeats file-age assumptions. State whether loss is permitted and how clocks, snapshots, replication, and late writes affect eligibility.

**Use time windows when data aligns with time.** Time-window compaction groups SSTables whose records belong to a window, compacts within windows, and can later remove wholly expired windows. It works best for TTL-heavy, mostly immutable time series whose late updates and tombstones are bounded. Mixing old timestamps into current files, repairing old data, or issuing deletes that must suppress values across windows complicates reclamation. Partitioning by event time is not enough: use authoritative maximum expiration/repair metadata and conservative grace rules.

**Merge by internal order, resolve by semantics.** The merge heap orders internal keys by user key and descending sequence/type according to the comparator. The output builder cannot simply keep the first entry. It must honor pinned snapshots, point and range tombstones, merge operators, TTL semantics, compaction filters, bottommost/coverage knowledge, and corruption policy. An old version may be dropped only if no supported reader can require it and no unselected older source can resurrect it. A tombstone may be dropped only when its suppression obligation is complete.

**Do not confuse age with safe deletion.** A tombstone's timestamp older than a grace interval is only one condition. Safety may require that all replicas received it, repair cannot reintroduce older data, every overlapping older value has been compacted or is otherwise excluded, and no snapshot can observe a pre-delete state. A compaction picker should provide coverage evidence to the merge kernel; otherwise the safe default is retention.

**Partition outputs at semantic-safe boundaries.** Target file size is a heuristic, not permission to split identical user-key versions, range-tombstone fragments, or atomic metadata incorrectly. Output partitions need ordered disjoint key ranges, validated smallest/largest keys, indexes, filters, checksums, properties, and unique file numbers. Avoid tiny tails where possible, but never sacrifice invariants for an exact size target.

**Install atomically.** Finish and sync output contents as required, validate them, then append/sync a manifest edit that adds every output and deletes every input. Only after the version edit becomes current may new readers choose outputs. Existing readers retain their pinned version and files. Crash recovery must distinguish unreferenced output orphans, committed outputs, and still-live inputs. Garbage collection consults live versions and pending outputs rather than directory age alone.

**Coordinate concurrent jobs.** Mark input files as being compacted and reserve affected output ranges/levels. Jobs that would share an input or violate target-level non-overlap cannot run independently. Disjoint ranges may proceed concurrently. Subcompaction partitions one selected merge by key boundaries and runs partitions in parallel, but all outputs still belong to one logical installation. Boundary computation must carry range tombstones and equal user keys correctly.

**Control resources explicitly.** Compaction consumes sequential and random reads, writes, decompression/compression CPU, merge memory, block cache, page cache, file descriptors, checksumming, encryption, and temporary disk space. Limit jobs, bytes per second, memory, open files, subcompactions, and reserved disk. Give flush and recovery-critical work priority while protecting foreground latency. More threads can reduce one job's duration yet lower total service by contention or cause latency spikes.

**Make stability a service objective.** Let `a(t)` be estimated compaction debt created per second and `s(t)` useful debt removed per second under current resource limits. A necessary long-run condition is `E[s] > E[a]`; bursts additionally require queue and space headroom. Debt is not raw input bytes alone because policies rewrite different overlapping volumes. Estimate remaining read plus write bytes by candidate class, report oldest age and L0/run thresholds, and throttle before hard limits. Backpressure is a correctness-preserving capacity response, not a substitute for tuning.

**Schedule for urgency and fairness.** A score may combine level bytes/target, L0 count, overlap, oldest debt, tombstone/TTL benefit, read heat, estimated cost, free space, and deadline. Pure ratio scores can starve expensive ranges. Add age, bounded priority classes, round-robin compaction pointers, and explicit emergency modes. Avoid oscillation with hysteresis. Manual compaction enters the same conflict/resource controller unless operators explicitly accept impact.

**Measure amplification with declared denominators.** Write amplification might mean storage bytes written divided by logical user bytes accepted, or compaction bytes written divided by flush bytes; these are not interchangeable. Read amplification might count files, blocks, bytes, or I/O operations per query. Space amplification requires a logical-live-data definition and may include snapshots, WAL, obsolete-but-pinned files, and temporary outputs. Report interval, cache state, compression, workload mix, and whether warm-up/ingest are included.

**Validate from local proof to steady state.** Unit-test interval closure, scoring, version retention, tombstone coverage, partition boundaries, and manifest edits. Property-test merge results against a simple logical reference over generated histories and snapshots. Inject truncated inputs, checksum failures, no-space, killed processes before/after every sync, manifest replay, and reader pinning. Exercise concurrent conflicting/disjoint jobs. Benchmark long enough to reach steady state and include overload, skew, updates, deletes, ranges, late data, cache states, storage fullness, and recovery.

## Definitions and Notation

Let an SSTable file `F` have level `ell(F)`, inclusive user-key range `[lo(F), hi(F)]`, physical size `size(F)`, sequence bounds, creation/order metadata, and immutable identity. `Overlap(F,G)` holds when their intervals intersect. For seed set S and participating levels P, overlap closure is the least fixed point C containing S such that every policy-required file in P overlapping the current C interval is also in C.

Let `D` be logical live bytes under a declared visibility baseline, `W_p` physical bytes written, `R_p` physical reads or bytes, and `S_p` physical occupied bytes. Then candidate measures are `WA=W_p/W_logical`, `RA=R_p/R_logical` or sources consulted, and `SA=S_p/D`; every report must define numerator and denominator. Let `Q(t)` be estimated debt bytes/work, `a(t)` debt arrival, and `s(t)` service, with `dQ/dt=a-s` away from bounds.

A **compaction version edit** is the atomic metadata transition `V' = (V - Inputs) union Outputs`. “Atomic” means recovery and readers select a complete valid version, not that filesystem operations are magically indivisible.

## Mechanisms, Invariants, or Proof Structure

### Selection and level-shape proof

1. Pin current version V and choose a seed using the declared trigger and fairness state.
2. Compute the policy-required transitive overlap closure across source and target structures.
3. Reject any input already reserved by another job and reserve the complete set/range.
4. Prove every required overlapping file is selected and every selected identity belongs to V.
5. Merge and partition outputs so target-level ordering/non-overlap and key-boundary rules hold.
6. Validate output metadata against actual first/last internal and user keys before installation.

### Logical-equivalence proof

1. Define the pre-compaction logical read result for every key and supported snapshot from V.
2. Multiway-merge complete inputs in comparator/internal-sequence order.
3. Retain every entry required by a supported snapshot, merge operator, tombstone/range-deletion obligation, TTL rule, repair/replication rule, or unselected overlapping source.
4. Drop an entry only with explicit dominance, coverage, and visibility evidence.
5. Show reads over `(V - Inputs) union Outputs` equal reads over V for every supported key/snapshot.
6. Treat uncertain coverage or corrupt input as retention/error, never speculative deletion.

### Crash-publication proof

1. Allocate unique output identities without shadowing any live or pending file.
2. Write, finish, checksum, and durably persist outputs according to the filesystem contract.
3. Append and durably persist one version edit containing the complete input deletion/output addition set.
4. Publish the new in-memory version only after durable metadata success.
5. Recovery before the edit uses old inputs and discards unreferenced outputs; recovery after it uses complete outputs.
6. Delete retired inputs only when no live version/reader/recovery obligation references them.

### Stability and scheduling evidence

1. Define debt units that estimate useful remaining read/write work rather than counting jobs alone.
2. Measure arrival, useful service, resource consumption, oldest age, L0/runs, and temporary space by class.
3. Demonstrate steady-state `service > arrival` at the supported ingest envelope with foreground objectives met.
4. Demonstrate controlled throttling before file-count or free-space emergency thresholds.
5. Show age/fairness bounds for cold, hot, small, and expensive ranges.
6. Re-run under failures, restarts, skew changes, and policy migration; retain rollback and conservative fallback.

## Alternatives and Trade-Offs

| Strategy | Selection tendency | Primary advantage | Primary cost/risk | Best-fit evidence |
|---|---|---|---|---|
| Leveled | source range plus complete next-level overlap | bounded stable-level point fan-out, prompt consolidation | repeated target rewrites, high write I/O | read-heavy/update-heavy steady-state tails within write budget |
| Tiered/size-tiered | several similarly sized runs | fewer rewrites and strong ingest throughput | more runs, read merge width, temporary space | write-heavy workload with filters/cache and acceptable read/space bounds |
| Hybrid/unified | parameterized tiered and leveled regions | workload-specific continuum | tuning/implementation complexity and migration states | sensitivity study across read/write/space objectives |
| Time-window | compact within event/TTL windows | whole-window expiry for aligned immutable data | late writes/deletes/repair cross windows | bounded lateness, TTL, repair, and expiry validation |
| FIFO | remove oldest files by size/age policy | minimal work for disposable data | intentional loss; no general obsolete-version merge | explicit cache/retention contract and loss tests |
| Full/manual | all files or an operator range | maximal consolidation or repair action | huge temporary space/I/O/tail disruption | capacity plan, checkpoints, cancel/recovery, postcondition audit |

Larger files reduce metadata and number of outputs but make jobs, recovery, cache granularity, and tail latency coarser. Smaller files improve parallelism and range targeting but increase metadata, seeks, filters, and file descriptors. Subcompaction shortens wall time only when CPU/storage bandwidth and safe boundaries permit it. Compression lowers physical I/O/space but costs CPU and can make rewritten-byte metrics incomparable unless both compressed and logical bytes are reported.

Picking by tombstone density may reclaim space but can repeatedly rewrite a hot range. Picking by read heat improves latency but starves cold debt. Picking oldest-first improves fairness but may ignore an imminent L0 stall. A robust scheduler combines urgency, expected benefit/cost, age, and hard resource constraints, then validates actual rather than predicted benefit.

## Failure Modes and Misconceptions

**“Compaction is background housekeeping.”** It is part of the write path's deferred work and read semantics. Falling behind eventually changes latency, space, and admission.

**“One overlapping target file is enough.”** The selected interval can expand through source and target overlaps. Compute the declared fixed point or use proven clean-cut boundaries.

**“The newest entry always wins, so older entries can disappear.”** Pinned snapshots, merge operands, range tombstones, repair, and unselected sources can require history.

**“An old tombstone is garbage.”** Age is not coverage. Dropping it can resurrect an older value from another file or replica.

**“Leveled means exactly one file read.”** It generally means bounded overlap per stable level; L0, filters, range queries, snapshots, and file partitioning still matter.

**“Tiered has low write amplification.”** Relative to a stated leveled design under compatible assumptions, often yes; a poor threshold, skew, full merge, compression, or backlog can still rewrite heavily.

**“Time-window storage makes TTL deletion automatically safe.”** Only wholly expired, semantically closed windows with late-data, repair, snapshot, and tombstone constraints satisfied are removable.

**“More background threads clear debt faster.”** They may contend for the same disk, CPU, cache, memory, and locks, reducing useful service and harming foreground tails.

**“A successful output file means compaction committed.”** Until the atomic version edit is durable, outputs are orphans and inputs remain authoritative.

**“Bytes compacted measures progress.”** Rewriting the same range repeatedly can increase the counter while debt grows. Measure estimated debt removed, level/run state, and oldest age.

**“Major compaction fixes a bad policy.”** It may create a temporary clean state while consuming enormous resources; unchanged arrival/service dynamics recreate the debt.

**“Benchmarking an empty or freshly loaded tree predicts production.”** Compaction behavior emerges over cycles. Use steady state, updates/deletes, skew, failures, and storage occupancy representative of service.

## Worked Examples

### Example 1

Seed `f0[10,19]` overlaps source `f1[15,24]`, expanding the selected interval to `[10,24]`. Target files `g0[0,14]` and `g1[15,29]` overlap that interval; adding them expands the union to `[0,29]`. No other source or target file intersects `[0,29]`, so the fixed point is `{f0,f1,g0,g1}`. Selecting only `f0,g0` would be incomplete.

### Example 2

The model's leveled inputs total `2+2+8+8=20` byte-units and declared output is 18; per-job output/input is `18/20=0.9`. The tiered inputs total 8 and declared output is 7; `7/8=0.875`. These ratios report this fixture's rewrite, not total system WA: user-ingest bytes, prior rewrites, WAL, compression, and future compactions are absent.

### Example 3

Suppose policy estimates debt arrival at 180 MiB/s while bounded compaction removes 150 MiB/s over a representative hour. Debt grows near 30 MiB/s, or about 105.5 GiB/hour (`30*3600/1024`). A temporary empty queue does not make the system stable. Reduce supported ingest, increase useful service within latency limits, or change policy/data layout.

### Example 4

File A holds `k@90=value-new` and `k@40=value-old`; a snapshot at sequence 50 remains active. Even though sequence 90 dominates current reads, compaction must retain a representation yielding `value-old` at snapshot 50. It can remove `k@40` only after that snapshot is unsupported and no other rule requires it.

### Example 5

Level 1 contains `k@80=DELETE`; an unselected lower-level file may contain `k@20=value`. If compaction removes the tombstone without proving complete coverage of every older value and relevant replica/snapshot obligation, a later read can resurrect `value`. The safe output retains the tombstone or expands selection and proves reclamation conditions.

### Example 6

Files of 98, 101, 103, and 99 MiB fall within a declared similar-size band and meet a minimum merge width of four; a 430 MiB file does not. The candidate totals 401 MiB. The exact band and thresholds are implementation policy. Before admission, account for input reads, output write, temporary disk, and concurrent foreground demand.

### Example 7

A 12:00–13:00 event-time window was compacted and appears expired, but repair writes an entry for 12:30 into a current physical file. File creation time and window label now disagree. Safe expiry requires per-file authoritative time/expiration bounds and a lateness/repair contract; blindly deleting the old window or retaining the new file forever are both policy failures.

### Example 8

A job writes outputs O1/O2 and syncs them, then crashes before the version edit. Recovery reads the last durable manifest, where inputs I1/I2 remain live. O1/O2 are unreferenced orphans and can be removed after a live-file audit. Deleting I1/I2 when output creation finished would have lost data.

### Example 9

One 800 GiB merge is partitioned into four disjoint key ranges. If each worker can consume 300 MiB/s read plus write bandwidth, four workers may demand 1.2 GiB/s before foreground traffic. On an 800 MiB/s device, additional workers add contention. Choose parallelism from measured total capacity and safe key/range-tombstone boundaries, not CPU count alone.

### Example 10

Candidate A has level score 1.3, age 2 minutes, estimated cost 20 GiB. Candidate B has score 1.2, age 90 minutes, cost 5 GiB. Always choosing the maximum score can starve B under continuous hot arrivals. An age boost or bounded round-robin rule selects B before its deadline while hard L0 emergency priority still protects write availability.

## Cross-Program Connections

- **Database Engineering:** MVCC snapshots, recovery, catalog/version edits, transactions, replicas, repair, and tombstone semantics determine safe elimination and publication.
- **Data Engineering:** lakehouse small-file consolidation, clustering, streaming state compaction, TTL retention, event-time windows, and backfills reuse selection and atomic-snapshot principles.
- **Distributed Systems:** replicas can reintroduce old state; epochs, leases, consensus metadata, anti-entropy, and garbage-collection horizons constrain deletion.
- **Operating Systems:** page cache, direct I/O, filesystem sync/rename guarantees, scheduling, writeback, and storage queues determine actual interference and durability.
- **Algorithms:** multiway merge, interval closure, amortized analysis, priority scheduling, bin packing, and external-memory models shape pickers and kernels.
- **Performance Engineering:** queue stability, tail latency, resource isolation, workload replay, and steady-state experimental design turn policy claims into evidence.
- **Security and Reliability:** checksums, authenticated storage, corruption handling, bounded parsing, crash injection, and audit trails prevent compaction from amplifying faults.

## References

1. Patrick O'Neil, Edward Cheng, Dieter Gawlick, and Elizabeth O'Neil, [The Log-Structured Merge-Tree](https://doi.org/10.1007/s002360050048), *Acta Informatica*, 1996.
2. RocksDB Project, [Compaction](https://github.com/facebook/rocksdb/wiki/Compaction), official strategy overview.
3. RocksDB Project, [Leveled Compaction](https://github.com/facebook/rocksdb/wiki/Leveled-Compaction), official leveled policy documentation.
4. RocksDB Project, [Universal Compaction](https://github.com/facebook/rocksdb/wiki/Universal-Compaction), official tiered-policy documentation.
5. RocksDB Project, [FIFO Compaction Style](https://github.com/facebook/rocksdb/wiki/FIFO-compaction-style), official FIFO/TTL policy documentation.
6. RocksDB Project, [Subcompaction](https://github.com/facebook/rocksdb/wiki/Subcompaction), official parallel compaction documentation.
7. Apache Cassandra Project, [Compaction Overview](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/compaction/overview.html), official strategy and operational documentation.
8. Apache Cassandra Project, [Unified Compaction Strategy](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/compaction/ucs.html), official leveled–tiered continuum documentation.
9. Subhadeep Sarkar et al., [Constructing and Analyzing the LSM Compaction Design Space](https://www.vldb.org/pvldb/vol14/p2216-sarkar.pdf), *PVLDB* 14(11), 2021.
10. Niv Dayan and Stratos Idreos, [Dostoevsky: Better Space-Time Trade-Offs for LSM-Tree Based Key-Value Stores via Adaptive Removal of Superfluous Merging](https://nivdayan.github.io/dostoevsky.pdf), *SIGMOD*, 2018.

## Exercises

### Exercise 1

L0 files are A `[5,12]`, B `[11,20]`, C `[40,50]`. L1 files are X `[0,9]`, Y `[10,17]`, Z `[18,30]`, W `[31,60]`. Starting from A and applying transitive overlap closure across L0/L1 with inclusive intervals, list the final selected files and interval. Explain each expansion.

### Exercise 2

A proposed compaction drops `k@70=DELETE` because its wall-clock age exceeds grace. An unselected level may contain `k@20=value`, a snapshot at sequence 60 is pinned, and one replica has not completed repair. Decide whether deletion is justified and enumerate the evidence required before it could be.

### Exercise 3

During a four-hour steady-state test, estimated debt arrival averages 240 MiB/s and useful service averages 270 MiB/s, but one 20-minute burst arrives at 600 MiB/s while service remains 270 MiB/s. Compute average surplus, burst debt, and minimum burst buffer ignoring preexisting debt. Name three operational limits that can still invalidate a stability claim.

### Exercise 4

Compare a read-heavy update workload with strict p99 point latency against a mostly immutable TTL time-series workload with bounded 24-hour lateness. Recommend a starting compaction family for each. State assumptions, risks, and the measurements that could reverse your choice.

### Exercise 5

Design a compact preproduction verification matrix for a new compaction picker. Include selection structure, logical equivalence, crash publication, concurrency, resource limits, steady-state performance, and policy migration. For each category, state an oracle or observable; do not use “tests pass” as evidence.

## Answers to the Exercises

### Answer 1

Start with A `[5,12]`. It overlaps B `[11,20]`, X `[0,9]`, and Y `[10,17]`; the union becomes `[0,20]`. That expanded interval overlaps Z `[18,30]`, so the union becomes `[0,30]`. With inclusive intervals W `[31,60]` and C `[40,50]` do not overlap `[0,30]`; the fixed point is `{A,B,X,Y,Z}` over `[0,30]`. C and W would form another connected region. A production picker must apply its exact level/clean-cut rules, but partial `{A,X,Y}` is not closed under the exercise rule.

### Answer 2

Removal is unjustified. Age does not prove coverage; the unselected `k@20` can be resurrected, and incomplete repair means another replica may reintroduce it. The sequence-60 snapshot does not see the sequence-70 tombstone and therefore also requires correct older-history handling. Required evidence includes complete overlap/replica coverage for older values, repair/anti-entropy and replication horizons, every supported snapshot/reader horizon, range-tombstone/merge interactions, authoritative grace/clock rules, and atomic publication. Until all applicable obligations hold, retain the tombstone or expand/restructure the operation.

### Answer 3

Average surplus outside the burst is `270-240=30 MiB/s`. During the burst debt grows at `600-270=330 MiB/s`; over 1,200 seconds that is 396,000 MiB, about 386.7 GiB using 1,024 MiB/GiB. Ignoring preexisting debt and any contemporaneous free-space loss, the queue needs at least that capacity. A stability claim can still fail because temporary output plus pinned-input disk space is insufficient, foreground p99 exceeds its objective, or L0/file-count hard thresholds stall before byte capacity fills. CPU, cache, file descriptors, recovery, and nonstationary bursts are further constraints.

### Answer 4

Start the read-heavy update workload with leveled or a read-biased unified configuration: bounded stable-level overlap favors point-read predictability and consolidation, assuming rewrite bandwidth and SSD endurance are adequate. Measure files/blocks per read, p99/p999, WA, debt age, stalls, and space under skew/deletes; high rewrite interference could favor a hybrid. Start the mostly immutable TTL workload with time-window or a tiered time-aware configuration, assuming event timestamps, TTLs, repair, and 24-hour lateness are enforced. Measure cross-window writes, whole-file expiry, range reads, space, repair, and late/delete correctness; frequent updates or strict read tails could favor leveled/unified behavior.

### Answer 5

Use: generated interval graphs with a fixed-point reference oracle for selection closure; generated version/tombstone/snapshot histories compared against a simple logical map for equivalence; kill points around output sync and manifest sync with recovery choosing exactly pre/post versions; conflicting and disjoint jobs checked for shared-input/range reservations and final level shape; injected no-space, checksum, bandwidth, memory, descriptor, and cancellation limits with bounded failure/fallback; long workload replay reporting debt arrival/service, oldest age, runs, amplification denominators, free space, and foreground tails; and old/new-policy manifests replayed across rollback/upgrade with identical logical reads. Record seeds, versions, configurations, commands, and artifacts so each failure is reproducible.
