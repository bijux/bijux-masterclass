---
module_id: DSE-080
program: Data Structures Engineering
level: 2
module_number: 80
title: Balancing Read, Write, and Space Amplification
status: complete
last_verified: 2026-08-30
---

# Balancing Read, Write, and Space Amplification

## One-Page Review

### Governing question

How can engineers select and tune a storage data structure when reducing read, write, or space amplification tends to consume another resource, and when every metric depends on workload and measurement boundary?

### Essential definitions

- **Read amplification (RA)** compares physical read work with logical read work. It may count sources, blocks, bytes, device operations, or CPU/cache probes; those definitions are not interchangeable.
- **Write amplification (WA)** compares physical bytes written with accepted logical mutation bytes over the same interval and durability boundary.
- **Space amplification (SA)** compares occupied physical bytes with logical live data under a declared snapshot, retention, compression, replication, and temporary-space policy.
- **Memory amplification** accounts for indexes, filters, caches, allocator overhead, metadata, and buffered state relative to logical data or a fixed budget.
- A **measurement boundary** states included layers: application encoding, database, WAL, compaction, filesystem, RAID, device firmware, replicas, backups, and caches.
- A **service objective** is a hard admissibility constraint such as p99 latency, ingest rate, recovery time, free-space reserve, endurance, or cost.
- A **Pareto frontier** contains candidates for which no other candidate is at least as good in every objective and strictly better in one.
- **Workload weighting** expresses preferences only after units are normalized; it cannot repair an infeasible candidate or establish universal optimality.

### Central model, mechanism, or theorem

There is no context-free scalar “amplification.” Define an observation interval I and logical baseline before forming ratios. Example database-layer write amplification is

`WA_db(I) = bytes_written_by_WAL_flush_compaction(I) / accepted_logical_mutation_bytes(I)`.

Device WA may divide NAND bytes programmed by host bytes written and therefore captures a different layer. Space may be steady-state resident bytes, peak bytes during compaction, or reserved provisioned bytes. Reads may be cache hits, logical block probes, device reads, or bytes. Report a vector, not a single unnamed number.

Optimization order is:

1. preserve correctness and durability;
2. reject candidates that violate hard service/capacity constraints;
3. remove dominated candidates;
4. compare remaining candidates with normalized workload cost, sensitivity analysis, and measured uncertainty;
5. validate steady state, bursts, failures, and migration before adoption.

The RUM conjecture frames a broad read–update–memory trade-off for access methods: improving two dimensions generally taxes the third, subject to model assumptions. LSM policy adds space and background rewrite behavior; hardware and caching add more dimensions. Such models guide design-space search but do not replace measurement.

### Critical invariants

1. Every ratio declares numerator, denominator, layer, interval, cache state, compression, and logical-live-data semantics.
2. Correctness, durability, recoverability, and data-retention requirements are hard constraints, never weighted preferences.
3. Candidates are compared on the same workload trace, data state, hardware allocation, warm-up, and measurement boundaries.
4. Steady-state results include background debt; ending before deferred compaction/reclamation completes cannot hide costs.
5. Peak and tail behavior remain visible; averages cannot conceal stalls, temporary doubling, or latency violations.
6. A claimed improvement reports displaced costs across reads, writes, space, memory, CPU, network, endurance, recovery, and operations.
7. Selection retains uncertainty, sensitivity, reproducible configuration, and rollback evidence.

### Common failures

- Dividing storage writes by operations rather than logical bytes, then comparing records of different sizes.
- Mixing database WA with filesystem/device WA or steady-state SA with peak compaction space.
- Calling cache hits “zero read amplification” while ignoring CPU, memory, and cache displacement.
- Benchmarking fresh ingest before the compaction debt and overwrite distribution reach steady state.
- Optimizing average point lookup while negative reads, ranges, writes, recovery, or p99 regress.
- Collapsing milliseconds, bytes, and endurance into an unnormalized weighted sum.
- Treating a Pareto frontier, analytical lower bound, or vendor configuration as a production recommendation.
- Choosing an infeasible low-score candidate because a weighted objective compensates for a hard limit.

### Compact example

Three fixture designs expose different measured triples `(p99 ms, WA, SA)`: leveled `(5.0,10,1.15)`, tiered `(9.0,4,1.45)`, and hybrid `(6.5,6,1.25)`. None dominates another. Hard constraints `p99<=7` and `SA<=1.30` reject tiered. Under balanced normalized weights, hybrid scores lower than leveled. Without constraints, a read-heavy weighting chooses leveled and a write-heavy weighting chooses tiered. These fixture values demonstrate decision mechanics, not engine performance.

### Connections

DSE-071 defines page/I/O boundaries; DSE-072–075 contrast in-place and copy-on-write trees; DSE-076–079 develop LSM runs, filters, and compaction. Database Engineering supplies MVCC and recovery baselines; Data Engineering adds distributed shuffle, object-store requests, replicas, and retention; Performance Engineering supplies experimental design and capacity modeling.

## Governing Question

How do we turn competing amplification metrics into a reproducible, constraint-aware engineering decision instead of tuning by folklore or a single benchmark number?

## Why This Matters

Data structures move work across time and resources. A B-tree may read and rewrite a page for a small mutation but offer a short point path. An LSM buffers writes and creates sequential runs, then spends later reads, compaction I/O, and temporary space. Copy-on-write preserves snapshots elegantly but retains old nodes and increases publication/reclamation work. Value separation avoids rewriting large values while adding indirection and garbage collection.

The word “amplification” makes these effects sound comparable, yet teams often measure different things. One dashboard reports database SSTable bytes; another reports host filesystem writes; SSD telemetry reports NAND programs. A scan's bytes may be appropriate, while point lookup I/O count matters elsewhere. Logical live size changes with snapshots, replicas, tombstone grace, and compression. A ratio without its boundary can mislead more confidently than no metric.

This module supplies a disciplined decision method. The objective is not zero amplification—often impossible and sometimes meaningless—but an admissible operating envelope with visible trade-offs, stable background work, controlled tails, and evidence that survives replay.

## Prerequisites and Retrieval

Retrieve:

- page-oriented B/B+ trees, copy-on-write publication, LSM flushes/levels, Bloom filters, compaction, snapshots, and tombstones;
- probability, expectation, quantiles, confidence intervals, sensitivity analysis, dominance, and constrained optimization;
- caches, compression, filesystems, SSD flash translation/garbage collection, RAID, remote/object storage, and replication;
- workload characterization: operation mix, key/value sizes, hit ratio, skew, ranges, updates, deletes, TTL, burstiness, concurrency, and dataset growth;
- benchmark hygiene: warm-up, steady state, coordinated omission, background debt, resource accounting, reproducibility, and rollback.

Diagnostic retrieval: lowering physical writes by keeping more runs can increase reads and resident obsolete bytes; adding filters can lower negative point I/O while consuming memory/CPU and doing little for long ranges. The cost moves rather than vanishes.

## Learning Objectives

After this module, you can:

1. specify reproducible read, write, space, and memory amplification metrics at multiple system layers;
2. distinguish steady-state, peak, tail, and recovery costs from interval averages;
3. construct and interpret a Pareto frontier without claiming a universally optimal point;
4. enforce correctness and service objectives before applying workload-weighted scoring;
5. derive simplified B-tree and LSM cost intuitions while retaining their assumptions;
6. design sensitivity studies for workload, memory, level ratio, file/block size, filters, compression, and value separation;
7. measure displaced costs across database, OS, device, network, replica, and operational layers;
8. produce decision evidence with uncertainty, provenance, rollback, and ongoing drift detection.

## Core Exposition

**Begin with semantics.** Define accepted write, durable write, visible state, supported snapshots, deletion/TTL horizon, and logical live bytes. A policy that discards required history or relaxes durability is not a low-SA or low-WA optimization; it is a different contract. Put correctness, recovery, retention, and privacy constraints outside the weighted objective.

**Name the layers.** Application amplification includes serialization and batching. Database WA includes WAL, flush, compaction, index/filter, and perhaps blob-log writes. Host WA includes filesystem metadata, copy-on-write, RAID, and encryption. Device WA includes flash erase-block behavior. Network WA includes replicas, quorum/repair, and remote compaction. Measure adjacent boundaries to localize cost; do not add ratios from different denominators.

**Define read work by query class.** For an unsuccessful point read, source probes and false-positive data blocks are useful. For a successful point read, cache/index/data path and version resolution matter. For a range, bytes read, blocks touched, runs merged, records filtered, and useful returned bytes matter. Report CPU/cache probes separately from device I/O. Aggregate by hit/miss, range size, consistency mode, and cache state before workload weighting.

**Define writes over a complete interval.** Let accepted logical mutation bytes include a reproducible key/value/metadata encoding. Count WAL, flush, compaction, index/filter, blob, manifest, and database-managed writes as declared. Start and end at equivalent steady-state conditions; otherwise the numerator may omit debt created by the denominator. Report read-for-compaction separately because storage bandwidth and energy include both directions even if WA counts writes only.

**Define logical and physical space.** Logical live data may mean latest visible key/value bytes at one snapshot, all retained snapshots, or billable application encoding. Physical resident space can include WAL, memtable, SSTables, indexes, filters, blob files, manifests, obsolete-but-pinned inputs, temporary outputs, filesystem allocation, replicas, and reserved free-space headroom. Report steady-state resident, peak during maintenance, and provisioned capacity separately. Compression belongs in both numerator description and CPU accounting.

**Use a constrained Pareto decision.** The following bounded model has three fixture candidates, hard p99/space constraints, normalized targets, and three weightings. Lower normalized score is preferred only among relevant candidates.

<!-- bijux-verify: {"id":"constrained-amplification-tradeoff-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"candidates=3\npareto_frontier=leveled,tiered,hybrid\nconstraints=p99<=7.0,space<=1.30\nfeasible=leveled,hybrid\nrejected=tiered\nleveled_balanced_score=0.9091\ntiered_balanced_score=1.0159\nhybrid_balanced_score=0.8816\nconstrained_best=hybrid\nread_heavy_best=leveled\nwrite_heavy_best=tiered\nlower_score_is_better=True\nvalid=True\nevidence=constrained_amplification_tradeoff_model\n","stderr":""}} -->
```python
from typing import NamedTuple


class Candidate(NamedTuple):
    name: str
    p99_ms: float
    write_amplification: float
    space_amplification: float


candidates = (
    Candidate("leveled", 5.0, 10.0, 1.15),
    Candidate("tiered", 9.0, 4.0, 1.45),
    Candidate("hybrid", 6.5, 6.0, 1.25),
)
targets = (7.0, 8.0, 1.30)


def dominates(left, right):
    left_values = left[1:]
    right_values = right[1:]
    return all(a <= b for a, b in zip(left_values, right_values)) and any(
        a < b for a, b in zip(left_values, right_values)
    )


def score(candidate, weights):
    values = candidate[1:]
    return sum(weight * value / target for weight, value, target in zip(weights, values, targets))


frontier = [
    candidate for candidate in candidates
    if not any(dominates(other, candidate) for other in candidates if other != candidate)
]
feasible = [candidate for candidate in candidates if candidate.p99_ms <= 7.0 and candidate.space_amplification <= 1.30]
rejected = [candidate for candidate in candidates if candidate not in feasible]
balanced = (0.5, 0.3, 0.2)
read_heavy = (0.7, 0.2, 0.1)
write_heavy = (0.2, 0.6, 0.2)
best = lambda choices, weights: min(choices, key=lambda candidate: score(candidate, weights)).name
valid = len(frontier) == 3 and len(feasible) == 2 and best(feasible, balanced) == "hybrid"
print(f"candidates={len(candidates)}")
print("pareto_frontier=" + ",".join(candidate.name for candidate in frontier))
print("constraints=p99<=7.0,space<=1.30")
print("feasible=" + ",".join(candidate.name for candidate in feasible))
print("rejected=" + ",".join(candidate.name for candidate in rejected))
for candidate in candidates:
    print(f"{candidate.name}_balanced_score={score(candidate, balanced):.4f}")
print(f"constrained_best={best(feasible, balanced)}")
print(f"read_heavy_best={best(candidates, read_heavy)}")
print(f"write_heavy_best={best(candidates, write_heavy)}")
print("lower_score_is_better=True")
print(f"valid={valid}")
print("evidence=constrained_amplification_tradeoff_model")
```

The three candidates are deliberately all non-dominated: each gains something while losing something. The score divides each metric by a target before weighting, so milliseconds are not directly added to ratios. Yet the targets, weights, and fixture measurements are judgments. No confidence interval, cache, workload trace, durability work, memory/CPU, peak space, device WA, recovery, or cost is modeled. The lambda is a finite scoring convenience, not an optimizer. This execution proves only exact selection for these fixtures.

**Interpret Pareto dominance first.** Candidate A dominates B only if A is no worse in every declared minimization metric and better in at least one. A dominated candidate needs a missing objective, lower uncertainty, migration benefit, or other explicit reason to remain. Non-dominated does not mean good: every frontier point may violate p99 or capacity. Apply hard constraints before preferences.

**Normalize before weighting.** Ratios such as `metric/target` are dimensionless and express distance relative to a chosen reference. Weights should reflect workload frequency, business value, or constrained resource cost—not convenient numbers chosen after seeing results. Use separate query classes instead of one average. Report results over plausible weight/target ranges; if the winner flips easily, the decision is fragile.

**Use models as maps, not measurements.** A B+ tree point lookup is often described as height-proportional page reads; caching upper levels changes physical I/O. A small update can dirty/write a page plus WAL and later filesystem/device work. An LSM with fanout T and L levels is often modeled with different leveled/tiered bounds on runs and rewrite work. Bloom-filter false positives can reduce negative point data reads. These formulas omit skew, compression, file overlap, snapshots, deletion, batching, cache, concurrency, and implementation policy unless explicitly incorporated.

**Recognize the RUM trade-off.** The RUM conjecture argues access methods cannot simultaneously minimize read overhead, update overhead, and memory overhead in a general model. Extra indexes and filters spend memory/update work to accelerate reads; buffering updates spends read or merge work later. It is a design principle under stated abstractions, not permission to label any observed regression “inevitable.” A better implementation may reduce waste and improve several measured axes without violating a lower-bound framing.

**Co-tune memory.** More memtable memory reduces flush frequency and number of levels but delays durability only if WAL policy changes; do not conflate them. More Bloom-filter memory lowers eligible negative-point false positives but displaces block cache or other processes. More block cache reduces physical reads but not logical lookup work and can suffer compaction pollution. Index/filter partitioning, cache admission, and memory ownership must be measured together.

**Co-tune geometry.** Larger fanout generally reduces level count while changing leveled rewrite overlap, tiered run count, level capacity, and space behavior. Larger blocks reduce index overhead and may improve scans/compression, but amplify point-read bytes. Larger files reduce metadata yet coarsen compaction and caching. Smaller values make page rewrite WA look worse relative to logical bytes; batching can amortize metadata. Sweep parameters jointly because local one-at-a-time tuning misses interactions.

**Separate keys from values when justified.** A key/value-separated design keeps keys and value pointers in the ordered structure and appends large values elsewhere. Compaction rewrites smaller index entries, potentially reducing database WA. Reads add value-log indirection, scans can become random, and garbage collection rewrites live values and needs crash-safe pointer/version handling. Report key-index and value-log WA/RA/SA plus GC debt; value separation does not erase cost.

**Treat compression as a vector transformation.** Compression can reduce physical read/write bytes and space while increasing CPU, latency variance, memory, and rewrite computation. Different levels may use different codecs. Compute logical, pre-compression, post-compression, and device bytes where available. A lower physical WA ratio caused by compressible new data is not necessarily a better compaction policy.

**Include hardware amplification.** Filesystem copy-on-write, RAID parity, thin provisioning, encryption blocks, flash translation, erase blocks, and device garbage collection can magnify or reshape database I/O. Database sequential writes may still trigger device cleaning under low spare area. Conversely, device telemetry can combine unrelated tenants. Correlate time windows and isolate workloads; never attribute device WA entirely to one engine without evidence.

**Account for replication and remote storage.** A logical mutation may produce quorum writes, WAL copies, compaction on each replica, repair traffic, backup/object uploads, and cross-region egress. Object storage turns small reads into requests/range bytes and rewrite into new immutable objects plus catalog commits. Report per-replica and fleet amplification, request count, network bytes, and retained versions. Local optimization can increase global cost.

**Reach representative steady state.** Precondition the dataset to realistic occupancy and key distribution. Run enough overwrite/TTL/compaction cycles that level sizes, run count, obsolete fraction, and debt stop trending. Preserve workload arrival rather than coordinated omission during stalls. Drain or explicitly account for end debt. Repeat with recorded seeds/configuration and uncertainty. Test warm/cold cache, hit/miss points, ranges, bursts, deletes, snapshots, and failures.

**Protect tails and peaks.** Average WA can be acceptable while compaction bursts violate p99. Average SA can fit while full compaction temporarily doubles storage. Average RA can hide negative misses or large ranges. Track percentile latency, stall time, bandwidth peaks, oldest debt, free-space minimum, output/input pinning, recovery duration, and endurance rate. Admission and backpressure belong in the supported envelope.

**Adopt with reversible evidence.** Record candidate version, schema/comparator, data format, options, hardware/firmware, dataset generator, trace, cache warm-up, command, raw counters, derived formulas, and confidence intervals. Validate rolling upgrade/downgrade and policy migration. Canary on representative shards, compare logical results, set abort thresholds, and preserve a rollback path that does not require unsafe format reversal.

## Definitions and Notation

For interval I, let `L_w` be accepted logical mutation bytes, `D_w` database-managed durable bytes, `H_w` host bytes, and `N_w` device-programmed bytes. Candidate ratios are `WA_db=D_w/L_w`, `WA_host=H_w/L_w`, and `WA_device=N_w/H_w`; multiplying is meaningful only when counters cover aligned data and intervals.

For query class q, define logical result bytes `L_r(q)`, sources `S(q)`, blocks `B(q)`, device operations `IO(q)`, and physical bytes `P_r(q)`. Report the appropriate vector rather than dividing by zero for a negative lookup. Let `P_resident`, `P_peak`, and `P_provisioned` be distinct space quantities; `D_live(snapshot,retention)` is the declared logical denominator.

Candidate x dominates y for minimization when every `m_i(x)<=m_i(y)` and at least one is strict. A normalized score `C(x)=sum_i w_i*m_i(x)/t_i` assumes positive targets `t_i`, nonnegative weights summing to one, comparable evidence, and prior satisfaction of hard constraints.

## Mechanisms, Invariants, or Proof Structure

### Metric-integrity proof

1. Define logical operation/data semantics and every included physical layer.
2. Align numerator and denominator over the same interval, tenant, durability, replication, and data population.
3. Record cache, compression, snapshots, retention, temporary outputs, and background debt.
4. Reconcile engine counters with OS/device/network counters without assuming equality.
5. Preserve raw counters and derive named ratios reproducibly.
6. Reject comparisons whose boundaries or denominators differ materially.

### Decision proof

1. Enumerate correctness, durability, recovery, capacity, latency, endurance, and cost constraints.
2. Measure each candidate under the same controlled workload/hardware protocol with uncertainty.
3. Reject infeasible candidates, then identify the non-dominated set over declared objectives.
4. Normalize remaining metrics by preregistered targets and apply justified workload weights.
5. Run sensitivity analysis over weights, targets, workload drift, and measurement uncertainty.
6. Choose only if the result remains operationally supportable; otherwise gather evidence or preserve multiple profiles.

### Steady-state evidence proof

1. Precondition realistic dataset size, occupancy, distribution, retained history, and cache state.
2. Run through repeated foreground/background cycles until debt and structure shape are stationary within declared tolerance.
3. Maintain offered load during stalls and record completed plus rejected/delayed work.
4. Account for pending work and peak temporary state at interval boundaries.
5. Repeat seeds/runs and report distributions/confidence, not one favorable trace.
6. Validate bursts, failures, recovery, migration, and rollback against the same hard constraints.

## Alternatives and Trade-Offs

| Design lever | Likely gain | Displaced cost | Required evidence |
|---|---|---|---|
| More aggressive leveling | fewer overlapping stable runs, lower resident obsolete data | compaction rewrite I/O/CPU and foreground interference | steady-state point/range tails, WA, endurance, debt |
| Tiering/lazier merge | lower rewrite frequency, higher ingest capacity | more runs, read merge work, resident/peak space | negative/range reads, filters/cache, SA and stalls |
| More Bloom memory | fewer negative point data probes | memory, hashes, cache displacement; little long-range help | per-level FPR, saved reads, CPU/cache and workload mix |
| Larger blocks/files | less metadata, improved sequential efficiency/compression | point-read bytes, coarse compaction/cache/recovery | per-query bytes/tails and maintenance peaks |
| Larger memtable | fewer/larger flushes and possibly fewer levels | memory, recovery replay/checkpoint pressure, burst flushes | memory isolation, WAL/recovery, debt and stalls |
| Value separation | smaller compaction payload | indirection, scan randomness, value-log GC/space | value-size distribution, read mix, GC and crash tests |
| Stronger compression | lower physical I/O and space | CPU, latency variance, migration/rewrite cost | logical/pre/post-codec bytes, CPU and tail profiles |
| Extra replicas/indexes | availability/read/query capability | write, network, storage, repair, consistency work | fleet-level bytes, failure objectives, repair/rebuild |

A single fixed configuration may not serve multiple tenants or phases. Separate column families/shards/profiles can isolate incompatible workloads, but multiply operations and reduce resource pooling. Adaptive tuning can follow drift but risks oscillation, invalid analytical assumptions, and unreviewed migrations. Use bounded parameter ranges, hysteresis, canaries, and audit logs.

## Failure Modes and Misconceptions

**“WA is bytes written divided by number of writes.”** The denominator must be logical bytes (or another named unit); operation sizes make raw counts incomparable.

**“Device WA equals database WA.”** Device WA commonly divides NAND writes by host writes; database WA uses logical mutation bytes. Filesystem and device behavior sit between.

**“A negative lookup returns zero bytes, so byte RA is infinite.”** For zero-result queries, use sources, blocks, I/O, or bytes per query rather than a meaningless division by result bytes.

**“SA below 1 is impossible.”** Physical compressed bytes divided by uncompressed logical bytes can be below one. State compression and denominator; do not redefine the ratio silently.

**“The lowest weighted score wins.”** Not if it violates correctness, p99, disk reserve, recovery, or endurance. Constraints precede scoring.

**“Every Pareto-frontier point is acceptable.”** Non-dominance only compares listed metrics. A frontier can consist entirely of infeasible or uncertain candidates.

**“Analytical optimal means production optimal.”** Optimality holds within a model, assumptions, parameter domain, and objective. Implementations and workloads add omitted costs.

**“More cache removes read amplification.”** It moves physical I/O toward memory/CPU and consumes capacity that might serve filters, memtables, or other tenants.

**“Compression improves all amplification.”** It often reduces byte-based I/O/space, but may increase CPU, latency, and rewrite work; ratio changes can reflect data compressibility.

**“A benchmark ends when clients stop.”** Deferred compaction, garbage collection, repair, and upload debt remains part of the writes it accepted.

**“Averages capture capacity.”** Burst buffers, p99 stalls, peak temporary outputs, and free-space minima can fail while averages look healthy.

**“One workload mix is enough.”** Sensitivity to hit rate, negative reads, ranges, value size, skew, updates, deletes, TTL, cache, and growth determines whether a choice is robust.

## Worked Examples

### Example 1

An engine accepts 100 GiB of logical mutations and writes 100 GiB WAL, 100 GiB flush output, and 600 GiB compaction output during an aligned steady-state interval. With those components declared, `WA_db=(100+100+600)/100=8`. If 200 GiB of debt remains at the end, the interval is not comparable to one that drains debt unless the debt is incorporated.

### Example 2

The host writes 800 GiB for Example 1, while device telemetry reports 1,200 GiB NAND programs. `WA_device=1200/800=1.5`; end-to-end NAND/logical amplification is `1200/100=12`. It equals `WA_db*WA_device` here only because boundaries and intervals align and no other host writer exists.

### Example 3

A negative point lookup checks six filters in memory, one index block, and one data block due to a false positive. Report sources=6, logical cache probes=7 or 8 under the stated counting convention, device I/O according to cache state, and physical bytes. Dividing by zero returned bytes would not describe useful read work.

### Example 4

Latest logical values total 500 GiB uncompressed. Compressed resident engine files total 420 GiB, so that named ratio is 0.84. During compaction, old pinned inputs plus outputs peak at 700 GiB, giving peak ratio 1.40. Provisioning 900 GiB gives 1.80. All three are valid different questions.

### Example 5

In the executable fixture, leveled beats hybrid on read p99 and space but loses on WA; hybrid beats tiered on read and space but loses on WA; tiered beats leveled on WA but loses on read and space. No candidate dominates. Hard constraints reject tiered, and balanced normalized cost selects hybrid among feasible choices.

### Example 6

Changing weights from balanced `(0.5,0.3,0.2)` to read-heavy `(0.7,0.2,0.1)` selects leveled across all fixture candidates. Write-heavy `(0.2,0.6,0.2)` selects tiered if hard constraints are ignored. The flip is evidence that workload preference matters; tiered remains inadmissible under the original p99/SA limits.

### Example 7

A 64 KiB value is stored beside a 32-byte key. Rewriting the combined record ten times moves roughly 640 KiB plus metadata. Value separation can rewrite a small key/pointer while retaining the value, but a later value-log GC may copy the 64 KiB and point reads add indirection. Measure the entire lifecycle and actual pointer/index sizes.

### Example 8

A candidate lowers compressed database writes 20%, while compression CPU raises p99 from 8 to 13 ms against a 10 ms limit. It is infeasible even if weighted byte cost is excellent. Try a faster codec, different levels, hardware, or target; do not weight away the violation.

### Example 9

A test accepts writes for 30 minutes and stops with L0 count and compaction debt rising. Report offered/accepted/completed load, debt delta, and predicted drain work. Extending the run until shape/debt are stationary or charging the remaining debt prevents artificially low WA and high throughput.

### Example 10

Two candidates differ by 2% in weighted score, but run-to-run confidence intervals overlap by 6%, and plausible read weights reverse the order. Evidence does not support a unique winner. Preserve both profiles, increase repetitions/trace fidelity, or choose using migration risk and headroom while labeling uncertainty.

## Cross-Program Connections

- **Database Engineering:** transaction logs, MVCC snapshots, indexes, vacuum, recovery, replicas, and query plans define logical work and retained state.
- **Data Engineering:** shuffle, compaction of immutable tables, object-store requests, partition pruning, checkpoints, and retention create fleet-level amplification.
- **Distributed Systems:** quorum writes, repair, anti-entropy, consensus logs, erasure coding, and cross-region replication move amplification into network and replicas.
- **Operating Systems:** page cache, filesystem copy-on-write, writeback, direct I/O, RAID, and scheduling mediate host counters and latency.
- **Computer Architecture:** cache hierarchy, memory bandwidth, compression CPU, SSD erase blocks, endurance, and device garbage collection shape physical cost.
- **Performance Engineering:** trace design, steady state, quantiles, uncertainty, coordinated omission, capacity, and sensitivity make comparisons defensible.
- **Economics and Sustainability:** provisioned capacity, energy, device replacement, network egress, and operator complexity convert amplification into total cost.

## References

1. Manos Athanassoulis, Michael Kester, Lukas Maas, Radu Stoica, Stratos Idreos, Anastasia Ailamaki, and Mark Callaghan, [Designing Access Methods: The RUM Conjecture](https://openproceedings.org/2016/conf/edbt/paper-12.pdf), *EDBT*, 2016.
2. Niv Dayan, Manos Athanassoulis, and Stratos Idreos, [Monkey: Optimal Navigable Key-Value Store](https://nivdayan.github.io/monkeykeyvaluestore.pdf), *SIGMOD*, 2017.
3. Niv Dayan and Stratos Idreos, [Dostoevsky: Better Space-Time Trade-Offs for LSM-Tree Based Key-Value Stores via Adaptive Removal of Superfluous Merging](https://nivdayan.github.io/dostoevsky.pdf), *SIGMOD*, 2018.
4. Subhadeep Sarkar et al., [Constructing and Analyzing the LSM Compaction Design Space](https://www.vldb.org/pvldb/vol14/p2216-sarkar.pdf), *PVLDB* 14(11), 2021.
5. RocksDB Project, [RocksDB Tuning Guide](https://github.com/facebook/rocksdb/wiki/RocksDB-Tuning-Guide), official amplification definitions and tuning guidance.
6. RocksDB Project, [Universal Compaction](https://github.com/facebook/rocksdb/wiki/Universal-Compaction), official tiered read/write/space trade-off documentation.
7. Apache Cassandra Project, [Unified Compaction Strategy](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/compaction/ucs.html), official parameterized leveled/tiered trade-off documentation.
8. Lanyue Lu, Thanumalayan Sankaranarayana Pillai, Hariharan Gopalakrishnan, Andrea Arpaci-Dusseau, and Remzi Arpaci-Dusseau, [WiscKey: Separating Keys from Values in SSD-Conscious Storage](https://www.usenix.org/system/files/conference/fast16/fast16-papers-lu.pdf), *FAST*, 2016.
9. RocksDB Project, [Performance Context and I/O Statistics Context](https://github.com/facebook/rocksdb/wiki/Perf-Context-and-IO-Stats-Context), official measurement instrumentation.

## Exercises

### Exercise 1

A steady-state interval accepts 250 GiB logical mutations. The engine writes 250 GiB WAL, 250 GiB flushes, 1,000 GiB compaction output, and 50 GiB metadata/blob GC. Host writes total 1,700 GiB; device NAND writes total 2,210 GiB. Compute database WA for the declared engine components, device WA, and aligned NAND/logical amplification. State why multiplying ratios may fail in another deployment.

### Exercise 2

Logical latest data is 800 GiB uncompressed. Resident compressed engine files are 680 GiB; pinned obsolete inputs add 120 GiB; an active compaction adds 300 GiB; provisioned capacity is 1,400 GiB. Compute named resident-latest, peak-latest, and provisioned-latest ratios. Explain why none alone answers “Will the disk fill?”

### Exercise 3

Candidates A `(p99=4, WA=12, SA=1.1)`, B `(7,7,1.25)`, and C `(10,5,1.5)` are minimized. Find the Pareto frontier. Apply constraints `p99<=8` and `SA<=1.3`. With targets `(8,8,1.3)` and weights `(0.5,0.3,0.2)`, compute feasible scores and select the lower one.

### Exercise 4

Design a measurement matrix that distinguishes positive point, negative point, short range, long range, inserts, updates, deletes, and TTL expiry across warm/cold cache and steady/burst load. Name raw counters, derived ratios, background-debt checks, and tail/peak constraints.

### Exercise 5

A team proposes value separation because median values are 32 KiB and compaction WA is high. Write an adoption argument that includes benefits, disqualifying constraints, value-log GC, point/range reads, crash consistency, snapshots, device/space effects, experiment design, migration, and rollback.

## Answers to the Exercises

### Answer 1

Declared engine writes are `250+250+1000+50=1550 GiB`, so `WA_db=1550/250=6.2`. `WA_device=2210/1700=1.3`. Aligned end-to-end NAND/logical amplification is `2210/250=8.84`. `6.2*1.3=8.06`, not 8.84, because host writes include 150 GiB not in the declared database numerator. Multiplication requires adjacent ratios whose numerator/denominator exactly cancel over aligned intervals with no omitted/co-tenant work.

### Answer 2

Using latest uncompressed logical data, resident engine ratio is `680/800=0.85`; including pinned inputs and active output, peak is `(680+120+300)/800=1.375`; provisioned is `1400/800=1.75`. Capacity risk also depends on filesystem allocation/reserve, future growth, simultaneous jobs, WAL/checkpoints, replicas, garbage-collection progress, debt, emergency thresholds, and whether the 300 GiB peak can grow. The ratios answer compression/residency, observed maintenance peak, and purchased headroom respectively.

### Answer 3

All three are on the Pareto frontier: moving A→B improves WA but worsens p99/SA; B→C does likewise. Constraints retain A and B and reject C. A score is `0.5*(4/8)+0.3*(12/8)+0.2*(1.1/1.3)=0.25+0.45+0.16923=0.86923`. B is `0.5*(7/8)+0.3*(7/8)+0.2*(1.25/1.3)=0.4375+0.2625+0.19231=0.89231`. Under these declared fixtures and weights, A has the lower feasible score despite higher WA; uncertainty and sensitivity still need review.

### Answer 4

Cross each query/mutation class with cache state and load regime, using fixed data distributions, sizes, hit ratios, range selectivity, and offered arrival. Record accepted logical key/value bytes; WAL/flush/compaction/blob/metadata reads and writes; source/filter/index/data/cache probes; device operations/bytes; CPU; memory; resident/pinned/temporary/provisioned space; run/level shape; debt arrival/service/age; stalls/rejections; and recovery/repair work. Derive named per-class RA vectors, layer-specific WA, resident/peak SA, throughput, and cost. Require stationary debt, aligned boundaries, p50/p95/p99/p999, free-space minimum, endurance, recovery time, and repeated-run uncertainty.

### Answer 5

The proposal should hypothesize that rewriting small keys/pointers instead of 32 KiB values lowers database and device bytes. Reject it if added point indirection, range randomness, GC peak space, recovery, or p99 violates hard objectives. Model live/dead value distribution, pointer/index overhead, snapshot-pinned values, GC selection/copy/install/reclaim, checksums, torn writes, and key-to-value publication. Replay representative point/range/update/delete/TTL workloads to steady state; report index and value-log WA/RA/SA, CPU/cache/device/network, debt, peaks, failures, and uncertainty. Canary a format-compatible migration with logical-result comparison, abort thresholds, capacity reserve, and a rollback or dual-read plan that does not discard old values prematurely.
