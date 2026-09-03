---
module_id: LSDS-013
program: Large-Scale Data Systems Engineering
level: 1
module_number: 13
title: Replication and Erasure Coding
status: complete
last_verified: 2026-09-03
---

# Replication and Erasure Coding

## One-Page Review

### Governing question

How should a large-scale storage system create independent recovery information so that data remains available and durable under named failures, while controlling capacity, latency, repair bandwidth, and operational complexity?

### Essential definitions

- **Replication** stores `r` complete copies of a logical object or block.
- An **erasure code** transforms `k` data fragments into `n=k+m` total fragments containing `m` parity fragments.
- An **MDS code** in coding theory can reconstruct the original data from any `k` of its `n` fragments under its erasure assumptions; this does not mean metadata server.
- A **stripe** is one encoding group spanning its data and parity fragments.
- An **erasure** is a fragment known to be unavailable or invalid; an undetected wrong fragment is an error and needs stronger handling.
- A **failure domain** is a component set expected to fail together, such as device, host, rack, zone, power feed, software version, account, or key domain.
- **Degraded read** reconstructs requested data because a normally selected fragment/copy is unavailable.
- **Repair** reads valid recovery information, reconstructs a missing copy/fragment, verifies it, and installs it on an authorized target.
- **Storage amplification** is physical protected payload divided by logical payload under a stated layout.
- **Repair amplification** compares bytes read, transferred, or written during repair with the lost logical/fragment bytes restored.

### Central model, mechanism, or theorem

For full replication factor `r`, ideal payload amplification is `r` and any `r-1` lost copies remain recoverable if every surviving copy is correct, accessible, and independently placed. For a systematic `k+m` maximum-distance-separable erasure code with equal fragment size `c`, each full stripe holds `kc` logical bytes in `(k+m)c` protected bytes, has ideal amplification `(k+m)/k`, and can reconstruct from any `k` valid fragments—equivalently tolerate up to `m` erasures under the code and placement assumptions.

These counts are not durability probabilities. Correlated failures, latent corruption, placement mistakes, repair delay, unavailable keys/metadata, shared software faults, and simultaneous maintenance can invalidate independence. Protection is a time-varying state established by current verified fragments across real failure domains.

### Critical invariants

- Every copy/fragment binds object identity, version, stripe, index, length, code profile, and integrity metadata.
- No two fragments needed for the intended fault tolerance silently share a prohibited failure domain.
- Only current, compatible, verified recovery information counts toward protection.
- Writes become visible only under a declared acknowledgement and stripe-consistency rule.
- Repair never overwrites the last good information from an unverified source.
- Membership, placement, and protection-policy epochs fence stale writes and repairs.
- Code parameters, implementation, checksum, encryption, and padding are recoverable with the data.
- Policy migration preserves at least one valid old or new recoverable representation until cutover is verified.
- Durability, availability, consistency, integrity, and confidentiality remain separate claims.

### Common failures

Frequent failures are treating copy count as independent durability, placing replicas or fragments behind one rack/power/controller, applying `p^r` without independence or repair time, confusing parity with checksums, counting stale/corrupt fragments, acknowledging partial stripes without a recoverable commit record, ignoring small-write amplification, selecting erasure coding solely from capacity ratio, repairing from an unverified fragment set, deleting old encoding too early during migration, and testing only single-device loss.

### Compact example

A `10+4` code with 64-MiB fragments stores 640 MiB of logical payload in 896 MiB, ideal amplification `14/10=1.4`, and tolerates any four known missing fragments if the code is MDS and ten compatible valid fragments remain. Reconstructing one 64-MiB fragment with ordinary Reed–Solomon decoding may read ten 64-MiB fragments and write one, so saving capacity relative to triple replication can increase repair reads and fan-out.

### Connections

[LSDS-011](011-distributed-block-storage.md) supplies block identity, placement, inventory, integrity, and repair states. [LSDS-012](012-metadata-servers-and-namespace.md) supplies policy metadata, commit, epochs, snapshots, and recovery roots. [LSDS-014](../ROADMAP.md) develops read/write pipelines, and [LSDS-015](../ROADMAP.md) develops failure detection and re-replication.

## Governing Question

Storage devices, hosts, networks, racks, software, and operators fail. A system needs redundant information, but “three copies” or “ten plus four” is not yet a durability design. The copies may share power. A code stripe may place two fragments on one host. A latent error may be discovered only after other fragments disappear. A repair storm may compete with production traffic until the exposure window becomes dangerous.

Replication and erasure coding make different trades. Replication is operationally direct: any valid copy can serve a read, and repair can copy one source. It spends substantial capacity. Erasure coding reduces steady protected bytes but adds encoding, fragment fan-out, degraded-read work, partial-write complexity, and generally more repair reads. Local reconstruction codes add parity to reduce common repair fan-in while preserving capacity savings.

The governing question is how to select, place, verify, monitor, repair, and migrate a protection scheme under an explicit fault model and workload. The answer includes mathematics, but the code parameters are only one layer. Implementation, topology, integrity, metadata, acknowledgement, maintenance, and repeated recovery evidence determine whether the advertised tolerance is real.

## Why This Matters

At petabyte scale, a factor of three in capacity is expensive in devices, facilities, power, embodied carbon, and operations. Erasure coding can lower this factor substantially. Yet degraded reads or repairs can touch many devices, increasing network and I/O demand exactly when the cluster is impaired.

Protection also shapes latency. Replicated reads can choose the fastest nearby copy and hedge stragglers. Coded reads need a sufficient valid fragment set and may wait on a slow kth response or decode. Small overwrites can require reading old data/parity before writing a consistent stripe. Hot data, mutable data, sealed cold data, and archival data may therefore deserve different policies.

Durability cannot be inferred from nominal parameters. Four parity fragments do not survive four rack losses if several fragments share each rack. Triple replication does not survive a software bug that corrupts all copies. Encryption can make every byte unrecoverable when a shared key disappears. Metadata loss can make intact fragments uninterpretable.

Repair time creates risk exposure. The longer a stripe remains degraded, the more opportunity for another failure or latent error to exceed its tolerance. Efficient detection, prioritized repair, reserve capacity, topology-aware placement, and throttling are parts of the protection system rather than secondary operations.

## Prerequisites and Retrieval

Recall partitioning and placement epochs from [LSDS-002](002-horizontal-partitioning.md) and [LSDS-003](003-range-hash-and-consistent-partitioning.md), locality from [LSDS-004](004-data-locality.md), task and dependency graphs from [LSDS-005](005-distributed-task-graphs.md) through [LSDS-007](007-narrow-and-wide-transformations.md), failure assumptions from [LSDS-009](009-cluster-failure-assumptions.md), and resource accounting from [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md).

From [LSDS-011](011-distributed-block-storage.md), retrieve logical block identity, generations, placement, checksum scope, inventories, and repair ordering. From [LSDS-012](012-metadata-servers-and-namespace.md), retrieve authoritative commit, policy metadata, snapshots, fencing, and recovery. You should understand ratios, combinations, probability assumptions, finite-field intuition, checksums, encryption, quorums, failure domains, percentiles, and capacity headroom.

## Learning Objectives

After completing this module, you should be able to:

- distinguish replication, mirroring, erasure coding, checksums, and backups;
- calculate ideal storage amplification for `r` replicas and `k+m` codes;
- explain encoding stripes, systematic data fragments, parity, padding, and code profiles;
- state deterministic erasure tolerance without overstating probabilistic durability;
- map replicas/fragments across device, host, rack, zone, and administrative domains;
- distinguish known erasures from detected and undetected errors;
- reason about acknowledgement, stripe consistency, and partial writes;
- calculate repair read/write/fan-out costs and degraded-read paths;
- compare Reed–Solomon, local reconstruction, and replication trade-offs;
- prioritize repair using remaining margin, consequence, demand, and cost;
- design safe policy migration and garbage collection;
- specify observability, fault injection, restore tests, and consequence review; and
- recognize when protection metadata, keys, or software are shared failure points.

## Core Exposition

### Protection is recovery information

Redundancy stores enough independent information to recover a logical version after some components fail. Full replication repeats the complete byte string. Erasure coding computes additional fragments from groups of data fragments. Backups add historical or administrative separation and often different access paths. Checksums detect some corruption but usually do not reconstruct missing bytes.

Name the protected unit: block, object, extent, file, partition, or volume. Also name version and mutation model. Immutable sealed objects are easier to code consistently than arbitrary in-place sectors. A snapshot can retain an older protected version while the live object changes.

The protection record should include object/version, stripe ID, fragment index, logical and encoded lengths, code/profile ID and parameters, checksum scope, placement epoch, encryption/key reference, committed state, and repair history. Without that context, a fragment is uninterpretable bytes.

### Full replication

With factor `r`, store `r` full instances on authorized targets. Any one current valid accessible copy can normally satisfy a read. Repair reads one good copy and writes a replacement, making data movement intuitive. Multiple copies also enable locality, load balancing, and hedged reads.

Replication amplifies payload by `r` before metadata, checksums, temporary copies, snapshots, compression, and reserve. The deterministic erasure tolerance is at most `r-1` copy losses. This assumes distinct intended domains and a correct survivor; it says nothing about common-mode corruption or probability over time.

Write consistency is separate. A primary/backup protocol, chain, quorum, or synchronous-all policy determines which copies must persist before acknowledgement and how stale copies are fenced. A configured factor of three does not imply every acknowledged write reached three durable devices.

### Erasure-code model

A systematic `k+m` code divides a full stripe into `k` data fragments of equal encoded size `c` and produces `m` parity fragments. The original data fragments remain directly readable in the systematic representation. A maximum-distance-separable code can reconstruct from any `k` of `n=k+m` fragments.

Ideal protected bytes are `(k+m)c` for `kc` logical bytes, so amplification is `(k+m)/k=1+m/k`. Capacity efficiency is `k/(k+m)`. Padding, metadata, alignment, checksums, journals, partial stripes, temporary representations, and reserve change real capacity.

The phrase “tolerates `m` failures” is shorthand for up to `m` erasures in one stripe under code, integrity, compatibility, and placement assumptions. A system with fewer than `k` valid fragments cannot decode that stripe. An implementation-specific code may have different recoverable patterns.

### Encoding and finite-field intuition

Parity fragments are linear combinations of data fragments over a finite field or another defined coding construction. Encoding multiplies the data vector by a generator matrix. Decoding selects a sufficient surviving fragment set and inverts the corresponding transformation.

Practitioners do not need to derive field arithmetic to operate a code, but they must preserve the exact algorithm, field, matrix/profile, library/version compatibility, fragment order, padding, and checksums. Two systems both labeled `10+4` are not necessarily interoperable.

Systematic codes avoid decoding for healthy reads of data fragments. Parity still consumes CPU and memory bandwidth on writes. Hardware acceleration can move the bottleneck to memory, network, or storage queues; benchmark the complete path.

### Failure domains and placement

Place recovery information so a modeled fault removes no more fragments than the code can tolerate. One fragment per host protects against a host loss; one per rack protects against a rack loss but may require at least `k+m` racks. Real topologies include chassis, power, network, cooling, zone, maintenance, firmware, operator, account, and key dependencies.

Topology labels must match reality. A rack label copied incorrectly into inventory can produce an apparently valid but correlated stripe. Audit physical and administrative mappings, not merely the placement rule text.

Placement trades independence against locality and cost. Spanning zones survives a zone fault but adds latency and egress. Grouping fragments for local repair reduces network scope but can concentrate failures. State primary and secondary fault objectives explicitly.

### Probability models and their limits

If `r` copies fail independently with identical probability `p` over a fixed interval and there is no repair, the simplified all-lost probability is `p^r`. For an MDS `k+m` stripe with `n=k+m` independent identical fragment failures and no repair, the simplified loss probability is the binomial tail for more than `m` failures.

These formulas are teaching models, not production durability forecasts. Devices have heterogeneous age and firmware; failures correlate by rack, batch, power, load, upgrade, bug, and operator. Failures and repairs occur over time, latent errors are discovered imperfectly, and availability of metadata/keys matters.

Production modeling may use failure/repair processes, conditional hazards, correlated-domain events, scrubbing detection, rebuild contention, placement distributions, and empirical incident data. Report assumptions and uncertainty instead of converting a nominal code into many “nines.”

### Integrity: erasures versus errors

Erasure decoding assumes the system knows which fragments are missing or invalid. Checksums, authenticated encryption, version metadata, and trusted manifests turn many corruptions into known erasures. An undetected wrong fragment can poison decoding.

Some codes can correct a limited number of unknown errors, generally at a greater redundancy cost than erasures, but production behavior depends on the implementation. Do not assume an erasure-code library automatically detects Byzantine or silent errors.

Verify each fragment before using it as a repair source, verify reconstructed output against trusted end-to-end integrity metadata, install under a new authorized generation, then update inventory. Retain evidence when sources disagree rather than majority-voting incompatible versions blindly.

### Write paths and acknowledgement

Full-stripe immutable writes compute all fragments from one canonical payload, send them to distinct targets, collect durable acknowledgements under the policy, and publish the stripe metadata atomically. Idempotency and version-qualified tokens make timeout retry safe.

The write acknowledgement must state how many and which domains/fragments are durable. A system may allow degraded writes with fewer than the target count; then it starts with reduced protection and urgent repair debt. Never infer the acknowledged set from configured `k+m` alone.

Metadata publishing must not expose a stripe with incompatible fragment generations or an unrecoverable set. Conversely, orphan candidate fragments from an uncommitted write must not be attached merely because they exist.

### Partial writes and small objects

Changing part of a coded stripe changes parity. Read-modify-write reads old data/parity needed to compute deltas, then updates affected fragments consistently. Reconstruct-write reads enough fragments to reconstruct the old stripe, applies changes, and writes a new representation. Both can amplify small writes and complicate crash consistency.

Copy-on-write immutable stripes simplify atomicity: construct a new stripe, verify it, publish a new mapping, and later reclaim the old stripe. It spends temporary capacity and metadata. Journaling or intent records can protect in-place schemes.

Small objects may waste padding or create too many fragments and RPCs. Packing objects amortizes coding but couples their read, update, deletion, and repair. Many systems replicate hot or mutable data first and code sealed cold extents later; the transition itself needs a safe protocol.

### Degraded reads

A replicated read retries another current valid copy, potentially choosing by locality and load. A coded degraded read gathers a decodable fragment set, verifies inputs, reconstructs requested data, and may cache or schedule repair. Healthy systematic reads can avoid decoding.

Latency depends on the kth required valid response, not just average fragment latency. Parallel requests reduce waiting but increase fan-out. Hedging extra fragments can cut tails while consuming I/O and network. Cancel unnecessary work once decoding is possible.

Partial-range reads interact with fragment layout, checksum units, compression, and code strips. Reconstructing a few bytes may require reads from many fragments. Measure read amplification by request-size distribution and fault state.

### Repair cost and exposure

Ordinary Reed–Solomon reconstruction of one `c`-byte missing fragment can read `k` fragments, transfer `kc` bytes, decode, and write `c` bytes. The exact implementation may read or transfer less through sub-packetization, local aggregation, or advanced regenerating/local codes.

Replication repair of an `L`-byte copy normally reads and writes `L` bytes from one source. Coded repair saves steady capacity but can multiply source fan-out and read bandwidth. Many simultaneous repairs can overload healthy devices and make more fragments unavailable.

Exposure duration spans detection, scheduling, source selection, reads, decode, target write, verification, and authoritative registration. Track time by protection margin: a stripe missing one of four parity fragments differs from a stripe with exactly `k` valid fragments.

### Local reconstruction and code selection

Local reconstruction codes add structure so common single-fragment repairs read a smaller local group than all `k` data-equivalent fragments. They can reduce repair bandwidth and I/O while adding local parity, implementation complexity, or different multi-failure patterns.

Code selection includes `k`, `m`, locality, fragment size, field/profile, CPU/vector support, overwrite semantics, minimum write set, placement constraints, degraded-read behavior, repair bandwidth, object size, and upgrade compatibility. Capacity ratio alone is insufficient.

Large `k` improves efficiency for fixed `m` but increases stripe width, minimum healthy-read fan-in, placement demands, and repair sources. Large `m` improves erasure margin and spends more capacity. Small fragments improve range granularity and increase objects/metadata/RPCs.

### Repair scheduling and throttling

Prioritize irrecoverable risk: fewest remaining independent valid fragments, newly detected correlated-domain failure, valuable/irreplaceable data, and long predicted repair. Demand can influence availability repair, but popularity should not displace critical durability work without policy.

Choose verified sources across healthy domains, avoid repeatedly loading the same survivors, reserve destination space, and respect topology. Throttle foreground interference while maintaining a maximum exposure objective. Static low throttles can be unsafe after a major event; uncontrolled recovery can collapse the cluster.

Repair operations carry object/version/profile/placement epochs and idempotency IDs. Concurrent deletion, overwrite, snapshot, and policy migration must not resurrect or corrupt obsolete stripes.

### Scrubbing and latent faults

Scrubbing turns silent corruption into a detected erasure while sufficient recovery information remains. Verify fragment checksums and periodically reconstruct or validate stripe-level/end-to-end integrity. A checksum stored and corrupted with the same fragment may be weaker than an independently protected manifest.

Set scrub intervals from latent-error risk, code margin, repair duration, consequence, media, and workload. Cold data needs deliberate coverage because normal reads do not sample it. Coordinate scrub and repair to avoid synchronized I/O storms.

Record last successful verification per fragment/stripe, bytes scanned, failures, disagreement, repair source, reconstructed digest, and post-repair result. A “healthy device” does not prove every cold fragment is readable.

### Policy migration

Moving from triple replication to erasure coding is a data migration, not a configuration toggle. Select a committed source version, encode new fragments, place across domains, verify each fragment and full logical digest, atomically publish the new protection record, then retire old copies only after snapshot/rollback and grace policies permit.

Timeouts and retries need an idempotent migration identity. Crashes may leave both schemes or incomplete candidates. Inventory reconciliation classifies them by object version and migration state; it does not choose the newest pathname or largest fragment count.

Rolling software upgrades must preserve code compatibility. Canary decoding on old and new versions, retain profile definitions, test recovery across mixed versions, and prevent a new encoder from writing data that all eligible recovery binaries cannot decode.

### Capacity and performance accounting

Ideal ratios omit partial-stripe padding, metadata, checksums, journals, temporary encodings, snapshots, repair reserve, failed/draining devices, capacity skew, local filesystem reserve, compression, and deduplication. Report logical bytes, protected payload bytes, installed raw bytes, and usable-policy bytes separately.

Account foreground write bytes, parity computation, acknowledgements, degraded-read bytes, repair reads/writes/network, scrub reads, and rebalance. Failure mode changes load; benchmark healthy and degraded states at realistic concurrency.

Provision free space in each relevant failure domain. Aggregate cluster free space cannot repair a rack's fragments if eligible other racks lack capacity. Model the largest credible repair event plus production growth during repair.

### Security, governance, and evidence

Fragments can contain recoverable or directly readable sensitive data; parity is not anonymization. Encrypt at rest and in transit, authorize fragment access, isolate tenants, protect code/placement metadata and keys, and audit repair/migration. Deduplication or deterministic coding across tenants can leak equality.

Deletion must cover replicas, parity fragments, caches, temporary encodings, failed-device returns, snapshots, backups, and old policies. Cryptographic erasure depends on complete key-scope knowledge and reliable key retirement; one shared key can also be a catastrophic availability domain.

Durability evidence includes current topology-aware inventory, verified integrity, scrub age, protection margin, repair backlog/duration, correlated-fault exercises, restore results, software/profile compatibility, metadata/key recovery, and incident learning. Consequence-bearing data needs named domain, security, legal, records, ethics, and recovery reviewers.

## Definitions and Notation

Let logical stripe payload be `S=kc`, where `k>=1` is the data-fragment count and `c>0` is equal fragment size. Let parity count `m>=1` and total fragments `n=k+m`. Ideal coded payload bytes are `nc`, amplification `A_ec=n/k`, and efficiency `E_ec=k/n`.

For replication factor `r>=1` and logical length `L`, ideal replicated payload is `rL`, amplification `A_rep=r`, and deterministic copy-erasure tolerance is `r-1` under compatible valid survivors.

For an MDS code, let `V_s` be the set of current compatible verified accessible fragments for stripe `s`. The stripe is decodable when `|V_s|>=k` and the selected fragment indices satisfy the code's decoding requirements. It is fully policy-protected only when placement and count satisfy the declared target, not merely when decodable now.

Define remaining erasure margin `g_s=|V_s|-k`. It is nonnegative when currently decodable and zero at the edge of data loss. This simple count must be refined for correlated failure domains and codes with nonuniform recoverable patterns.

For simplified independent identical fragment-failure probability `p` over a no-repair interval, MDS stripe loss probability is `sum_{j=m+1}^{n} C(n,j)p^j(1-p)^(n-j)`. Replicated loss is `p^r`. These expressions are invalid as forecasts when independence, identical hazards, interval, or no-repair assumptions do not hold.

Let repair read bytes be `R`, write bytes `W`, and restored fragment bytes `c`. Read amplification is `R/c`, write amplification `W/c`, and source fan-out is the number of distinct sources. Network bytes can differ from reads when decoding or aggregation occurs near sources.

## Mechanisms, Invariants, or Proof Structure

To design or audit a protection policy:

1. Name logical version, protection unit, mutability, workload, and consequence.
2. State code/copy parameters, exact profile, acknowledgement, integrity, and compatibility.
3. Define device, host, rack, zone, software, administrative, and key failure domains.
4. Prove placement satisfies deterministic erasure goals for each modeled domain event.
5. Define healthy, degraded, decodable, protected, corrupt, stale, and irrecoverable states.
6. Specify healthy/degraded reads, full/partial writes, commit, retry, and cache behavior.
7. Calculate steady capacity plus degraded-read, scrub, repair, and migration resources.
8. Define verified-source repair, priority, throttling, fencing, and post-repair evidence.
9. Preserve recoverability through profile/software/key migration and garbage collection.
10. Test correlated faults, latent corruption, overload, full domains, crashes, and restores.

The following fixture compares ideal payload capacity for triple replication and a full-stripe `10+4` code, then calculates an ordinary one-fragment reconstruction. It does not forecast durability, model padding/metadata, or implement finite-field coding.

<!-- bijux-verify: {"id":"protection-capacity-repair","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"stripe_payload=671088640 encoded_stripe=939524096 ec_amplification=1.40\npayload_bytes=107374182400 stripes=160 replicated_bytes=322122547200 coded_bytes=150323855360\nec_saved_vs_replication=171798691840\nmissing_fragment=67108864 repair_read=671088640 repair_write=67108864 read_amplification=10.0 source_fanout=10\nerasure_margin_healthy=4 erasure_margin_degraded=0\n","stderr":""}} -->
```python
MIB = 1024 * 1024
GIB = 1024 * MIB
k = 10
m = 4
n = k + m
fragment = 64 * MIB
stripe_payload = k * fragment
encoded_stripe = n * fragment

payload_bytes = 100 * GIB
assert payload_bytes % stripe_payload == 0
stripes = payload_bytes // stripe_payload
replicated_bytes = 3 * payload_bytes
coded_bytes = stripes * encoded_stripe

print(
    f"stripe_payload={stripe_payload} encoded_stripe={encoded_stripe} "
    f"ec_amplification={encoded_stripe / stripe_payload:.2f}"
)
print(
    f"payload_bytes={payload_bytes} stripes={stripes} "
    f"replicated_bytes={replicated_bytes} coded_bytes={coded_bytes}"
)
print(f"ec_saved_vs_replication={replicated_bytes - coded_bytes}")

repair_read = k * fragment
repair_write = fragment
print(
    f"missing_fragment={fragment} repair_read={repair_read} "
    f"repair_write={repair_write} "
    f"read_amplification={repair_read / fragment:.1f} source_fanout={k}"
)
print(
    f"erasure_margin_healthy={n - k} "
    f"erasure_margin_degraded={k - k}"
)
```

The capacity comparison is exact only for 160 full stripes and omits every non-payload term. The repair assumes a conventional decoder reads ten complete fragments to regenerate one; an implementation or locally repairable code may differ. “Margin four” assumes every fragment is valid and independently placed under the modeled fault.

Deterministic proof checks fragment identity/profile, valid-set cardinality, recoverable index patterns, and topology placement. Probabilistic durability needs justified hazards and repair processes. Performance needs observed workloads and failure-state resource contention. Governance needs recovery and deletion across every representation.

## Alternatives and Trade-Offs

Triple replication offers simple reads and repair, locality choices, and strong tolerance to two independently placed copy erasures at `3x` ideal payload. Two copies cost less and leave no safety margin after one loss. Higher factors spend capacity and may suit small critical metadata.

Reed–Solomon-style MDS codes offer flexible `k,m` and optimal fragment count for arbitrary erasures under their model. They can require `k`-way repair reads. Local reconstruction codes spend or arrange additional parity to repair common losses with fewer sources while retaining broader multi-loss protection.

Small `k` reduces fan-out and placement width but has worse capacity efficiency for fixed `m`. Large `k` improves ratio and broadens stripes, increasing metadata, tail sensitivity, and repair sources. More parity increases margin and steady bytes.

Replicating mutable/hot data then coding sealed/cold data keeps the write path simple and saves long-term capacity. It temporarily stores both forms and needs a verified migration state machine. Direct coded overwrites avoid transition delay but add partial-write and crash-consistency work.

Cross-zone placement improves geographic fault tolerance and spends latency, bandwidth, and egress. In-zone rack diversity is faster and does not survive zone loss. Geo-replication plus local coding can layer objectives at still greater complexity.

Eager repair shortens exposure and can overload an already impaired cluster or duplicate work for transient faults. Delayed repair avoids churn and extends vulnerability. Use fault type, remaining margin, predicted duration, and resource budgets.

Checksums per fragment cheaply identify many corruptions. End-to-end logical digests validate reconstructed bytes. Authenticated encryption adds tamper evidence and key dependence. Layer them rather than expecting parity to detect every error.

Large fragments reduce metadata and favor throughput; small fragments improve ranges and individual repair units while multiplying objects and RPCs. Sub-fragment coding reduces repair transfer and adds layout complexity.

## Failure Modes and Misconceptions

- **“Three copies means three failure domains.”** Placement evidence must show distinct real domains.
- **“`k+m` survives any `m` failures.”** Only a compatible code and valid fragment set under its erasure and placement assumptions support that claim.
- **“Parity is a checksum.”** Parity provides recovery information; trusted integrity evidence identifies bad inputs.
- **“A readable stripe is fully protected.”** Exactly `k` valid fragments are decodable with zero remaining count margin.
- **“Erasure coding always saves installed capacity.”** Padding, small objects, reserve, metadata, and operational headroom can erase ideal savings.
- **“Repair writes only one fragment, so it is cheap.”** Source reads, fan-out, decode CPU, network, verification, and contention matter.
- **“The fragments fail independently.”** Shared rack, power, firmware, operator, key, network, and workload violate independence.
- **“More durability nines follow from the binomial formula.”** Only justified hazards and repair models support probabilistic forecasts.
- **“Any ten fragments from any profile can decode a `10+4` stripe.”** Algorithm, matrix, ordering, padding, version, and integrity must match.
- **“A majority chooses the right bytes.”** Replicas can be stale or commonly corrupted; use authoritative version and integrity metadata.
- **“Configured policy equals acknowledged protection.”** Record the actual durable set at commit and current verified state.
- **“Partial coded writes are ordinary overwrites.”** Parity consistency requires read-modify-write, reconstruct-write, or new-stripe commit.
- **“Systematic means unprotected.”** Data fragments are original-form pieces but protection comes from the whole code set.
- **“One lost fragment requires reading the whole object.”** Repair operates by stripe/fragment layout; exact sub-packet behavior is implementation-specific.
- **“A healthy device proves healthy fragments.”** Cold latent corruption requires scrub or read evidence.
- **“Repair should always use the nearest source.”** Source diversity, load, integrity, and correlated risk can dominate locality.
- **“Changing the pool policy instantly recodes existing data.”** Existing and new representations need explicit migration semantics.
- **“Deleting old replicas after encoding starts is safe.”** Cut over only after new decoding and integrity evidence are authoritative.
- **“Encryption is independent of durability.”** Key loss, rotation, and shared key scope are recovery domains.
- **“Internal tests certify archival or regulated durability.”** Named domain and assurance review remains required.

## Worked Examples

### Example 1

**Situation:** Three replicas sit on three devices in one host. **Reasoning:** They may tolerate two device erasures but not one host outage. Copy count is three; host-domain count is one. Move verified copies to distinct authorized hosts/racks before claiming host tolerance.

### Example 2

**Situation:** A `6+3` MDS stripe loses two fragments. **Reasoning:** Seven valid fragments remain, so it is decodable and has count margin one. It is below full target protection; repair promptly from verified compatible inputs across permitted domains.

### Example 3

**Situation:** A `10+4` stripe has ten reachable fragments, but one fails its trusted checksum. **Reasoning:** Only nine count as valid, so ordinary erasure decoding cannot be assumed. Do not feed the corrupt fragment into reconstruction; find another verified copy, backup, or recovery path and preserve incident evidence.

### Example 4

**Situation:** A 4-KiB overwrite targets a 640-MiB coded stripe. **Reasoning:** In-place parity must change consistently. Evaluate read-modify-write, reconstruct-write, or copy-on-write new stripe; measure read/write amplification and crash points rather than quoting 1.4 capacity amplification.

### Example 5

**Situation:** One 64-MiB fragment of the fixture is lost. **Reasoning:** The modeled decoder reads 640 MiB from ten sources and writes 64 MiB: read amplification ten, write amplification one, fan-out ten. A local code or sub-packet repair may lower those values.

### Example 6

**Situation:** Four fragments occupy four hosts but two hosts share each of two power units. **Reasoning:** Host diversity is four and power diversity is two. A single power loss removes two fragments. Evaluate the stripe against both domain events and place according to the stronger required policy.

### Example 7

**Situation:** A sealed object has triple replicas and is migrating to `10+4`. **Reasoning:** Bind a migration ID and source version, generate/place/verify all coded fragments, decode and compare the logical digest, publish the new profile atomically, retain old copies through rollback/grace, then reclaim idempotently.

### Example 8

**Situation:** A zone outage creates 100,000 degraded stripes and repair saturates survivor disks. **Reasoning:** Rank by remaining independent margin and consequence, cap per-source work, reserve network/destination space, adapt throttles to objectives, and avoid making overloaded survivors appear failed.

### Example 9

**Situation:** An operator estimates triple-copy loss as `p^3` using annual disk failure `p`. **Reasoning:** The expression assumes identical independent failures over a no-repair interval and ignores correlation, detection, repair, latent errors, and topology. It is not an annual durability forecast without a justified stochastic model.

### Example 10

**Situation:** An archive is byte-recoverable but its only profile file and decryption key are lost. **Reasoning:** The fragments are operationally unrecoverable. Protect and restore-test code profiles, metadata, binaries, credentials, keys, provenance, and procedures alongside bytes.

## Cross-Program Connections

[Theory of Computation and Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md) supplies formal models, information limits, and complexity reasoning behind coding guarantees. [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies matrix-based algorithms, implementation cost, benchmarking, and trade-off analysis. The required mathematical foundations include vectors, finite fields, combinations, conditional probability, dependence, uncertainty, and survival models.

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies memory bandwidth, vector instructions, accelerators, devices, controllers, and failure modes. [Network Engineering](../../24-network-engineering/ROADMAP.md) supplies topology, congestion, multicast/fan-out costs, cross-zone paths, and failure correlation.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns replica consistency, quorum/leader protocols, membership, consensus, and fault models. [Security Engineering](../../25-security-engineering/ROADMAP.md) owns authenticated integrity, encryption, keys, tenant isolation, tamper response, and secure deletion.

[Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns lifecycle classes, retention, residency, authoritative versions, and recovery policy. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns capacity, topology labels, service tiers, repair operations, upgrades, observability, and objectives.

GFS and HDFS illustrate rack-aware full replication. Current HDFS and Ceph documentation describe erasure-coded layouts, fragment parameters, recovery, and operational constraints. The Windows Azure Storage LRC work shows that code locality can reduce repair I/O and bandwidth while retaining lower capacity overhead than replication.

## References

- Sanjay Ghemawat, Howard Gobioff, and Shun-Tak Leung, [*The Google File System*](https://research.google/pubs/the-google-file-system/), SOSP, 2003. Primary replication, placement, checksum, mutation, re-replication, and garbage-collection design.
- Apache Hadoop Project, [*HDFS Architecture*](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html), checked 2026-09-03. Official current block replication, rack awareness, checksums, write pipeline, and replica-selection overview.
- Apache Hadoop Project, [*HDFS Erasure Coding*](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HDFSErasureCoding.html), checked 2026-09-03. Official current data/parity units, policies, storage overhead, reconstruction, and operational guidance.
- Ceph Foundation, [*Erasure Code*](https://docs.ceph.com/en/latest/rados/operations/erasure-code/), checked 2026-09-03. Official current `k`, `m`, chunks, profiles, overwrite behavior, and recovery documentation.
- Ceph Foundation, [*Pools*](https://docs.ceph.com/en/latest/rados/operations/pools/), checked 2026-09-03. Official replicated pool size, minimum I/O set, degraded operation, and recovery controls.
- Ceph Foundation, [*CRUSH Maps*](https://docs.ceph.com/en/latest/rados/operations/crush-map/), checked 2026-09-03. Official topology, weights, erasure-code failure domains, and placement rules.
- Cheng Huang et al., [*Erasure Coding in Windows Azure Storage*](https://www.microsoft.com/en-us/research/publication/erasure-coding-in-windows-azure-storage/), USENIX ATC, 2012. Primary Local Reconstruction Code capacity, locality, repair, placement, and deployment design.
- Muralidhar et al., [*f4: Facebook's Warm BLOB Storage System*](https://www.usenix.org/conference/osdi14/technical-sessions/presentation/muralidhar), OSDI, 2014. Primary erasure-coded warm storage, failure domains, rebuild, and operational design.
- Dean Hildebrand and Denis Serenyi, [*A Peek Behind Colossus, Google's File System*](https://cloud.google.com/blog/products/storage-data-transfer/a-peek-behind-colossus-googles-file-system), Google Cloud, 2021. Official replication/erasure-coding, metadata, custodians, and storage-tier context.
- Saurabh Kadekodi et al., [*Tiger: Disk-Adaptive Redundancy Without Placement Restrictions*](https://research.google/pubs/tiger-disk-adaptive-redundancy-without-placement-restrictions/), OSDI, 2022. Primary risk, placement-diversity, and disk-adaptive redundancy research.

## Exercises

### Exercise 1

For 24 TiB of full-stripe logical payload, compare ideal protected payload under triple replication, `8+3`, and `12+4`. Calculate amplification, protected TiB, and deterministic fragment-erasure tolerance under stated MDS assumptions.

### Exercise 2

A `10+4` stripe has fragments on 14 hosts across seven racks, two fragments per rack. Evaluate host and rack erasure tolerance and explain why “four failures” is ambiguous.

### Exercise 3

Design a safe partial-overwrite and timeout-retry protocol for a coded mutable object. Address version, parity consistency, commit, idempotency, stale fragments, and recovery.

### Exercise 4

Compare repair of a 256-MiB replicated block with reconstruction of one 64-MiB fragment from a `10+4` code when conventional decoding reads ten fragments. Calculate reads, writes, fan-out, and restored-byte amplification.

### Exercise 5

Specify protection and review evidence for a long-lived, irreplaceable human-subject research archive transitioning from replication to erasure coding.

## Answers to the Exercises

### Answer 1

Triple replication has amplification 3 and uses 72 TiB, tolerating two independently placed copy erasures. `8+3` has amplification `11/8=1.375`, uses 33 TiB, and tolerates any three fragment erasures per full stripe if it is MDS with compatible verified fragments. `12+4` has amplification `16/12=4/3`, uses 32 TiB, and tolerates four such erasures. These are ideal payload figures: stripe padding, metadata, checksums, migration, reserve, and real failure-domain placement are omitted.

### Answer 2

One host loss removes one fragment, so any four distinct host losses leave ten fragments and are decodable under the MDS assumptions. One rack loss removes two fragments; two rack losses remove four and remain decodable, while three rack losses remove six and exceed tolerance. “Four failures” must name the unit: four hosts, four racks, four fragment reads, or four correlated events produce different loss patterns. Placing one fragment per rack would require fourteen racks for direct four-rack tolerance.

### Answer 3

Bind the request to object generation, stripe version/profile, byte range, expected prior version, and idempotency ID. Either lock/reserve the stripe and use a journaled read-modify-write/reconstruct-write protocol with a durable commit decision, or build a complete copy-on-write stripe from verified old fragments and publish its manifest atomically. Fragment writes carry the new generation and cannot overwrite old authoritative fragments blindly. A timeout queries the operation ID and returns the committed result or safely resumes/aborts; it does not start an unrelated generation. Recovery uses the durable decision to finish or discard candidates, and repair counts only compatible committed fragments.

### Answer 4

Replication repair reads 256 MiB from one verified source and writes 256 MiB to one target: read and write amplification one relative to restored 256 MiB, source fan-out one. The modeled coded repair reads `10*64=640 MiB`, writes 64 MiB, and restores 64 MiB: read amplification ten, write amplification one, source fan-out ten. Network placement, sub-packet repair, aggregation, and local codes can change actual transfer.

### Answer 5

Inventory immutable archive versions, stripe/block identities, checksums and independent fixity manifests, replicas, snapshots, holds, keys, topology, and software/profile dependencies. Encode from a verified committed source; distribute fragments across justified physical and administrative domains; verify every fragment, decode samples and full logical digests, publish atomically, retain rollback copies through approved grace, and prove later reclamation. Exercise device/host/rack/zone and correlated software faults, latent corruption, missing metadata/key, degraded reads, repair storms, migration crash/retry, and disaster restore. Monitor margin, scrub age, repair exposure, compatibility, and deletion across all representations. Named review includes investigators/data stewards, participants or community representatives, research ethics/IRB, privacy/legal/records, cybersecurity/key management, archival/storage specialists, disaster recovery, accessibility, and independent research-integrity assurance. Internal coding tests do not constitute ethical, legal, or archival approval.
