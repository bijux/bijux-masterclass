---
module_id: DSE-050
program: Data Structures Engineering
level: 1
module_number: 50
title: Choosing Representations for Large Graphs and Text
status: complete
last_verified: 2026-08-30
---

# Choosing Representations for Large Graphs and Text

## One-Page Review

### Governing question

How should an engineer choose, combine, validate, and evolve large graph and text representations from explicit semantic, workload, byte, latency, mutation, snapshot, persistence, and security requirements?

### Essential definitions

- A **logical model** defines identities, relationships/sequences, multiplicity, properties, ordering, and update meaning before storage.
- A **capability matrix** maps required operations to representations that support them with stated costs and semantics.
- A **workload envelope** describes input sizes/distributions, operation mixes, concurrency, output sizes, tail objectives, and growth.
- A **byte model** accounts for final, allocated, temporary-build, update, cache, mapping, and retained-generation memory/storage.
- A **primary representation** owns canonical logical facts; a **derived representation** accelerates queries and must remain version-consistent.
- A **snapshot generation** binds canonical data, derived indexes, schema/analyzers/comparators, deletions, and provenance.
- **write amplification** is bytes/work rewritten per logical update; **read amplification** is sources/fragments/blocks examined per query.
- A **delta overlay** buffers mutations over an immutable base until merge/compaction.
- A **representative workload** preserves relevant size, skew, locality, query, update, and output behavior.
- An **architecture decision record (ADR)** captures requirements, alternatives, measurements, choice, consequences, and revisit triggers.

### Central model, mechanism, or theorem

Representation selection is a constrained multiobjective problem, not a slogan. First reject candidates that cannot preserve semantics or required operations. For remaining candidates, compute concrete bytes and modeled costs, then measure representative workloads under correctness evidence. A candidate that is asymptotically good but violates a tail, snapshot, durability, or authorization constraint is infeasible.

For a directed graph with `n` dense vertices and `m` edges, 64-bit CSR offsets plus 32-bit destinations use `8(n+1)+4m` structural bytes before properties. Storing CSR and CSC roughly doubles those arrays but supports both outgoing and incoming traversal. A bit adjacency matrix uses `ceil(n^2/8)` bytes before metadata and can be infeasible even when adjacency tests are fast. Pointer/hash adjacency needs actual allocator/capacity bytes, not only `O(n+m)`.

Text requirements commonly need multiple views. A positional inverted index supports analyzed term, Boolean, phrase, and ranked retrieval. A trie/FST supports dictionary/prefix navigation. A suffix array/tree supports arbitrary substring structure. Combining views is correct only when they share one text/analyzer/generation contract and publication boundary. Minimal bytes are not the goal if a required query is absent; maximal indexing is not the goal if cost, privacy, or operations cannot sustain it.

### Critical invariants

1. Graph/text logical identity, encoding, normalization, directedness, multiplicity, properties, document/field/analyzer, and coordinate semantics precede representation choice.
2. Every required operation has a declared result/order/snapshot/output contract and at least one feasible implementation path.
3. Byte calculations include widths, capacities, metadata, properties, mappings, temporary builds, deltas, caches, and retained generations.
4. Canonical and derived views represent the same logical generation; cross-view IDs/positions/properties map bijectively where required.
5. Updates publish atomically or expose one specified base-plus-delta snapshot; failures leave a recoverable prior generation.
6. Persistent formats validate bounds, order, topology, checksums, schema/comparator/analyzer versions, and provenance before use.
7. Access control and resource limits apply during candidate generation/traversal, not only after output truncation.
8. Benchmarks reproduce workload distributions, include build/refresh/merge/recovery, report latency distributions and bytes, and retain exact environments.
9. The ADR states limitations, unsupported operations, evidence strength, revisit thresholds, and migration/rollback path.

### Common failures

- Choosing “sparse graph means adjacency list” without direction, operations, bytes, skew, or update model.
- Choosing a suffix structure for analyzed term semantics or an inverted index for arbitrary raw substrings without acknowledging transformation.
- Counting final arrays but omitting peak old+new+temporary memory during rebuild.
- Maintaining CSR/CSC or text indexes independently and exposing mixed generations.
- Benchmarking uniformly random graphs/queries when production has hubs, long prefixes, rare/common terms, or large outputs.
- Treating successful construction/query as proof of semantic correctness, durability, authorization, or universal performance.
- Optimizing mean latency while ignoring p99/p99.9, cold pages, merges, stalled readers, and cancellation.
- Publishing internal vertex/doc/slot positions as stable business IDs.
- Adding every possible index and creating unsustainable write/storage/privacy amplification.
- Recording a decision without measurable revisit triggers or migration plan.

### Compact example

For `n=1,000,000`, `m=10,000,000`, 64-bit offsets and 32-bit endpoints, outgoing CSR costs 48,000,008 structural bytes; CSR+CSC costs 96,000,016; a bit matrix costs 125,000,000,000 bytes. A workload requiring outgoing and incoming enumeration rejects CSR-only despite its lower bytes. CSR+CSC is about 1,302 times smaller than the bit matrix by integer ratio and meets the capabilities. A text service requiring analyzed term/phrase plus prefix completion chooses a positional inverted index plus trie/FST dictionary rather than claiming one structure supplies both contracts.

### Connections

[DSE-041](041-adjacency-matrices-lists-and-edge-arrays.md) through [DSE-043](043-disjoint-set-forests.md) supply graph representation and connectivity foundations. [DSE-044](044-tries.md) through [DSE-049](049-inverted-indexes.md) supply text indexes and their distinct identities. [DSE-004](004-time-space-and-allocation-cost.md), [DSE-006](006-memory-locality-and-cache-behavior.md), [DSE-009](009-property-based-testing-of-data-structures.md), and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md) supply cost/evidence discipline. The [program roadmap](../ROADMAP.md) advances to Level II algorithms and production systems.

## Governing Question

Given exact semantics, required/optional operations, scale/distributions, service objectives, mutation and snapshot behavior, persistence/recovery, security boundaries, team/toolchain constraints, and measured evidence, which canonical and derived representations should be adopted and when must the choice be revisited?

## Why This Matters

Most representation failures are not isolated algorithm mistakes. They arise when a mathematical object, workload, and lifecycle are underspecified. A graph team chooses one outgoing adjacency format and later discovers reverse traversal is central. A search team tokenizes away information needed for exact phrases. A compact index builds successfully but requires three times available memory during compaction. A derived view updates after the canonical store and readers observe two generations.

Large data makes mistakes expensive. Rebuilding a billion-edge graph, reindexing a document corpus, changing vertex/doc IDs, or migrating a persistent format can consume days, double storage, and disrupt service. Decisions should therefore be explicit, reproducible, and reversible. A durable ADR connects semantic requirements to concrete byte models and measurements, then defines triggers for change.

Graphs and text expose complementary trade-offs. Graph queries follow relationships and are shaped by degree skew, direction, and topology. Text queries follow sequence identity, analyzed tokens, prefixes, and substrings. Both benefit from immutable packed arrays, alternate orientations, compression, partitions/segments, deltas, mappings, and snapshot publication. Both can also leak sensitive structure and amplify output.

This module is not a catalog recap. It supplies a repeatable selection workflow that rejects semantic mismatches early, quantifies actual resource envelopes, constructs cross-view invariants, demands evidence proportional to claims, and records operational consequences.

## Prerequisites and Retrieval

Retrieve invariants/contracts from [DSE-002](002-representation-invariants.md) and [DSE-003](003-operation-contracts.md), cost/allocation/locality from [DSE-004](004-time-space-and-allocation-cost.md) through [DSE-006](006-memory-locality-and-cache-behavior.md), and validation/measurement from [DSE-009](009-property-based-testing-of-data-structures.md) and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md). Retrieve graph layouts from [DSE-041](041-adjacency-matrices-lists-and-edge-arrays.md) and [DSE-042](042-compressed-sparse-graph-layouts.md); text choices from [DSE-044](044-tries.md), [DSE-047](047-suffix-arrays.md), [DSE-048](048-suffix-trees.md), and [DSE-049](049-inverted-indexes.md).

## Learning Objectives

After completing this module, you should be able to:

1. produce graph/text semantic and operation contracts before evaluating structures;
2. construct capability and workload matrices with hard versus soft requirements;
3. calculate structural, property, mapping, peak-build, delta, cache, and retained-generation bytes;
4. reject infeasible representations without confusing asymptotic compatibility with operational fitness;
5. design canonical-plus-derived views with stable logical IDs and atomic generations;
6. compare dynamic mutation, immutable rebuild, partition/segment, and base-plus-delta strategies;
7. design representative correctness, performance, failure, persistence, and security evidence;
8. evaluate tail latency, amplification, skew, output, and recovery rather than a single throughput number;
9. write an ADR with consequences, unsupported cases, revisit triggers, and migration/rollback; and
10. distinguish internal evidence from external academic, practitioner, security, relevance, or production review.

## Core Exposition

**Start with a semantic inventory.** For graphs, record vertex identity/domain, isolated vertices, directedness, loops, parallel edges, edge identity, property types, zero/absence meaning, temporal/version semantics, deletion, and stable external IDs. State whether `m` counts logical undirected edges, directed incidences, or physical slots.

For text, record raw encoding, Unicode/normalization/case/language policy, document/field identity, tokenization/analyzers, positions/offsets, separators, original-coordinate mapping, mutable versions, and stable external IDs. Distinguish exact raw substring from analyzed term and prefix completion. These are different relations even when demos use ASCII words.

Declare ordering. Graph neighbor order may be unspecified, by endpoint, edge ID, time, or weight. Text terms may use encoded byte order, Unicode scalar order, locale collation, score, or insertion order. Reproducible build and pagination need deterministic ties. Comparator/analyzer version belongs in persistence.

Declare failure and trust. Inputs may be governed internal data or hostile uploads. Define invalid endpoints/encoding/properties, duplicates, capacity/overflow, cancellation, partial output, and recovery. Authorization namespaces and tenant boundaries are part of identity. A representation cannot recover information discarded by an earlier model.

**Write an operation contract table.** Each operation states result, required ordering, snapshot, complexity objective, output limits, and priority. Graph examples: adjacency test, out/in neighbor enumeration, edge scan, degree, vertex/edge property lookup, BFS/PageRank/triangle-like kernels, batch insert/delete, snapshot, transpose, serialization, and recovery.

Text examples: exact term, Boolean, phrase/proximity, prefix autocomplete, raw substring, ranked top-k, occurrence/highlight positions, dictionary enumeration, document update/delete, refresh/commit, merge, and recovery. Mark hard requirements versus optional or offline. State target p50/p95/p99/p99.9, throughput, concurrency, refresh/durability, memory/storage, build window, and growth.

Capabilities precede scoring. An outgoing-only CSR cannot satisfy efficient incoming enumeration unless transpose construction is allowed within the objective. A document-only inverted index cannot answer exact phrase semantics without another source. A trie over analyzed terms cannot locate arbitrary raw substrings. Reject or explicitly add a derived view.

Output is an operation. Enumerating a hub's million neighbors, a prefix's million keys, a common term's postings, or all substring occurrences costs at least output size. APIs need limit/cursor/order/cancellation/access policy. A claim of constant/logarithmic lookup covers navigation, not unbounded reporting.

**Characterize the workload envelope.** Record `n`, `m`, degree distribution, directed/reciprocal/loop/parallel rates, property widths, partitions, update batches, query mix, frontier sizes, and topology families for graphs. Average degree alone hides hubs and isolated vertices.

For text, record documents, raw/indexed bytes, tokens, unique terms, term/document/collection-frequency distributions, positions/offsets/payloads, key/prefix lengths, substring repetition, language/script, query mix/selectivity/output, update/delete rate, segment count, and ranking/highlighting. A tiny English vocabulary cannot stand in for code/log/multilingual corpora.

Separate current, expected growth, and hard maxima. Capacity planning uses tail/burst and failure envelopes, not only average. Include cold startup, cache churn, NUMA placement, mapped-page faults, merge/rebuild overlap, slow readers, backups, and replication if relevant.

Preserve representative anonymized fixtures or generators with exact seeds and distribution summaries. Synthetic data isolates variables; real governed data captures correlations. Use both. Record corpus/graph digest, transformation version, and privacy constraints.

**Calculate bytes before benchmarking.** For CSR with `n+1` 64-bit offsets and `m` 32-bit destinations, structural bytes are `8(n+1)+4m`. Add weights/edge IDs/properties, alignment, incoming view, external-ID mapping, partition metadata, tombstones/deltas, allocator/mapping headers, and optional cross-position maps. Peak build may include COO input, counts, cursors, sorted buffers, old base, new base, and delta simultaneously.

A bit matrix uses `ceil(n^2/8)` for one bit per ordered pair, plus row alignment and metadata. A byte/word matrix multiplies further. Hash adjacency counts buckets, control bytes, capacities/load factor, entries, objects, pointers, allocators, and per-vertex containers. “Both are O(n+m)” says little about actual bytes.

For text, count term dictionary, postings doc gaps, frequencies, positions, offsets, payloads, norms, stored fields/doc values references, live masks, skips/block metadata, segment headers/checksums, analyzers/mappings, caches, and text. Trie/suffix structures count nodes/edges/labels/child capacity/leaf positions and authoritative text. Suffix arrays count SA/rank/LCP/RMQ/BWT/samples.

Report final logical bytes, allocated resident bytes, mapped/file bytes, peak build/merge bytes, temporary disk, update delta, cache budget, and retained generations separately. Compression ratio without decoder scratch and skip/block overhead is incomplete. A system can fit final data and still fail every rebuild.

Use checked arithmetic and declared widths. Graph `n^2`, text token/position counts, `(n+1)*width`, `m*property_width`, LCP sums, dictionary offsets, and decompressed sizes overflow at scale. Reject unsupported size before allocation/publication.

**Build a capability/feasibility matrix.** For graphs, compare adjacency matrix/bitset, vector/hash adjacency, edge arrays, CSR, CSR+CSC, blocked/partitioned variants, and immutable base plus delta. Columns include exact model support, out/in traversal, adjacency, edge scan, ordering, mutation, stable IDs, snapshot, accelerator/mapping, bytes, and build/merge.

For text, compare hash/B-tree dictionaries, tries/FSTs, inverted postings detail, suffix arrays/trees/automata, FM-index, n-gram indexes, and hybrids. Columns include analyzed term, Boolean, phrase, prefix, raw substring, ranking features, positions/highlighting, mutability, compression, snapshot, bytes, and rebuild.

Mark “supported with auxiliary” separately from native. An edge array plus sorted source index becomes CSR-like. CSR plus a hash for selected high-degree adjacency changes bytes/update. A suffix array can support prefix-of-suffix searches but not analyzer term semantics automatically. An inverted n-gram index can generate substring candidates but needs verification.

Reject any candidate that loses required loops/multiplicity/zero edges, raw spans, analyzer positions, stable identity, authorization namespace, or snapshot. Do not assign a favorable performance score to an invalid model.

Then identify dominated candidates: if one meets the same semantics/capabilities and is no worse on every measured hard dimension and better on one, the other can leave the shortlist. Evidence uncertainty may prevent domination. Keep qualitative risks visible instead of collapsing everything into one arbitrary weighted score.

**Combine views under one owner.** Often no single representation is enough. Choose a canonical owner: immutable edge records/object store/log for graphs, authoritative document/version store plus analyzer contract for text. Derived CSR/CSC, matrix/bitmap, inverted postings, trie/FST, suffix/n-gram, ranking/vector views reference stable logical IDs and one generation.

Define build lineage: input generation/digest, schema/comparator/analyzer, transformation tool/version, output checksum, validation. Cross-view invariants compare logical facts. Every live edge ID appears exactly in required CSR/CSC incidences with aligned properties. Every indexed document version and token occurrence matches authoritative analysis; prefix/suffix views map to the same canonical text positions.

Atomic publication can install one manifest pointing to all validated derived files. Readers pin it. If views refresh at different rates, expose named consistency/staleness contracts and never silently join incompatible IDs. A query needing both views chooses a common generation or a governed reconciliation layer.

Derived indexes can be rebuilt and discarded; canonical data and external mappings cannot be accidental caches. If a derived view becomes canonical operationally, its durability/recovery obligations must be promoted explicitly.

**Choose an update architecture.** Mutable adjacency containers or tries give local updates but require synchronization, fragmentation control, iterator/handle invalidation, WAL/recovery, and compaction. Packed CSR/suffix arrays/FST/inverted segments favor immutable reads and batch rebuilds.

Base-plus-delta combines an immutable compact base with mutable insert/delete overlays. Queries merge base and delta under one snapshot, suppress tombstones, and deduplicate by stable logical ID/version. Compaction builds a replacement. Read amplification, delta memory, write/space amplification, merge debt, and worst-row/term overlay size need thresholds.

Partition/segment by vertex range, graph partition, tenant, time, document shard, or immutable batch. This bounds rebuild and parallelizes, but cross-partition edges, multi-segment terms, global statistics, prefix dictionaries, and transactions add read/coordinator work. Partition identity and mapping persist.

Define visibility versus durability. Publishing a refreshed text segment or graph delta may make it queryable before durable commit/replication. State acknowledgment, WAL/log, fsync, manifest, recovery, and replica semantics. Failure injection tests every boundary.

Rebuild planning includes old+new+temporary capacity, I/O throttling, CPU/memory interference, cancellation/retry, checksum/validation, atomic switchover, reader drain, rollback retention, and garbage collection. A data structure benchmark excluding lifecycle can choose an unoperable design.

**Model then measure operations.** Use analytical models to eliminate infeasible candidates and formulate hypotheses. CSR out scan is degree-sized, adjacency matrix row scan is `n`, sorted CSR membership is logarithmic in degree, hash adjacency expected constant, and edge arrays scan `m`. But actual cache/vector/branch/NUMA behavior requires measurements.

Text term lookup includes dictionary seek, blocks decoded, deletions/ACL, scoring, stored/highlight, and output. Prefix includes expanded terms; substring includes suffix/n-gram navigation and candidates. Phrase includes positions. Query end-to-end, not an isolated container function only.

Use p50/p95/p99/p99.9 and distributions, not average alone. Report cold/warm, single/batch, concurrency scaling, cancellation, and overload. Separate construction, refresh, commit, merge, recovery, validation, and steady queries. Include background interference because users experience it.

Hardware/environment records include CPU/microarchitecture, memory/NUMA, storage/filesystem, accelerator, OS/kernel, compiler/runtime, allocator, library/codecs, thread pinning, frequency/power, page/cache state, and container limits. Store commands and raw evidence under `artifacts/`.

Measure counters that explain results: bytes allocated/resident/mapped, page faults, cache/TLB/branches, bandwidth, CPU cycles, decoded integers, traversed edges/nodes, blocks skipped, retry/contention, I/O and write amplification, retained generations. A faster result without explanation is fragile.

**Validate correctness before interpreting speed.** Graph reference models preserve vertex/edge IDs, direction, loops, parallel properties, and query results. Compare conversions, traversals, degrees, algorithms, updates/deletes, snapshots, and persistence. Use small exhaustive graphs and generated adversarial hubs/duplicates/invalid inputs.

Text references preserve raw/canonical document, analyzer tokens/positions/offsets, external IDs, term/phrase/prefix/substring occurrences, ranks/scores, deletion/ACL, and original spans. Compare every representation through logical outputs rather than internal bytes. Use Unicode/analyzer conformance and malformed codecs.

Metamorphic relations strengthen evidence: graph edge/vertex relabeling preserves isomorphic results; CSR transpose twice preserves edge multiset; text segment partition/merge preserves external results; order-preserving alphabet remap preserves suffix order; analyzer-equivalent inputs match; compression round trips; rebuild/serialize preserve generation digest.

Fault evidence covers allocation, parser, mapping, thread creation, temporary storage, checksum, fsync, manifest, crash, cache, cancellation, and corruption. Concurrency evidence checks point-operation linearizability or immutable snapshots, version pinning, reclamation, stalled readers, and background rebuild. Security evidence includes authorization at candidate time and resource budgets.

Do not infer pedagogical/semantic correctness from tests alone. Internal source, mathematical, conceptual, practitioner, and pedagogical review are separate. External academic/practitioner/security/relevance/operations review requires named human records.

**Write a durable ADR.** It states context and logical contract; hard/soft operations; workload and growth; alternatives; capability matrix; byte/peak models; correctness and benchmark evidence; selected canonical/derived views; update/persistence/security design; consequences; unsupported cases; limitations; deployment/migration/rollback; and owners.

Record exact evidence paths/commands and dates. Explain rejected alternatives without straw men. State uncertain assumptions. A decision can choose a simpler slower representation for verification, operations, or team ownership; those are legitimate dimensions when explicit.

Revisit triggers are measurable: `n/m/token/term` thresholds, p99, memory/disk utilization, delta/segment/partition count, merge debt/amplification, update rate, query mix, hub/common-term output, analyzer/schema change, new incoming/phrase/substring requirement, accelerator migration, incident, corruption, or library end-of-life.

Migration defines dual-build/shadow verification, backfill, cross-view diff, cutover generation, rollback window, external-ID mapping, capacity, and removal. Avoid permanent dual-write without reconciliation. A shadow representation can validate before serving.

**Graph decision patterns illustrate constraints.** Read-mostly directed analytics needing both directions often selects CSR+CSC with stable edge IDs/properties and batch rebuild. Edge-centric algorithms may retain canonical COO/edge arrays. High-update local neighborhoods may use per-vertex hash/vector/chunked adjacency with periodic compact snapshots. Dense bounded domains may justify bit matrices for intersections.

Hub skew can require split rows, bitmap hybrid for high degree, edge-balanced partitions, or block formats. GPU/GraphBLAS workloads require compatible widths/order/transfer. Incoming views double structure and synchronization but can transform reverse queries. Measure suite-level value.

Graph temporal/history semantics may require append logs/versioned edges rather than overwriting adjacency. Deletion may be tombstone plus compaction. Stable external vertex/edge IDs map to dense generation indices. Never let compaction slot positions leak as durable descriptors.

**Text decision patterns preserve query identity.** An analyzed search service generally uses inverted postings; add positions only where phrase/proximity/highlight needs justify bytes. Term dictionary FST/trie supports term/prefix enumeration. Doc values/columnar structures support sorting/aggregations. Vector indexes cover semantic similarity under separate model/evidence.

Autocomplete over a controlled dictionary favors trie/FST plus ranking metadata, not scanning all postings. Arbitrary raw substring search may use suffix array/FM-index/n-gram candidates with verification, often on selected fields because index/privacy costs are large. Code search may tokenize identifiers and also retain trigram/raw verification.

Analyzer upgrades commonly require reindex. Querying mixed generations can dual-analyze and merge with stated score limitations, but permanent ambiguity is costly. Original span mapping belongs with generation. Stop-word/synonym changes alter phrase graph and statistics.

Text indexes leak vocabulary/frequency/occurrence; adding prefix/substring/positions increases inference surface. Choose minimal necessary capabilities per field/tenant and control debug/backup/cache access. “Index everything” is not neutral.

**Security and resilience are decision dimensions.** For graph inputs, bound vertices/edges/degrees/properties, checked counts/offsets, parser topology, traversal/output, and chosen-ID hash attacks. For text, bound bytes/tokens/terms/positions, analyzer expansion, wildcard/regex/phrase, decode, scoring/highlight/output, and parser metadata.

Apply authorization before or during traversal/candidate/top-k. A hidden edge or document filtered only afterward can affect path/score/count and leak. Partition by tenant or attach visibility structures with proof. Multi-tenant shared derived indexes require noninterference analysis beyond functional results.

Immutable generations aid rollback and corruption isolation. Validate before publication, retain last-known-good, authenticate provenance, and rehearse restore/rebuild. Checksums detect bit changes, not semantic mismatch or malicious authorized generation.

Operational simplicity, observability, and repair matter. Expose generation/schema/analyzer, bytes, deltas/segments, merge state, validation result, corruption errors, query budgets/cancellation, and reader retention. Fail closed or fall back according to named product policy, not accidental exception handling.

The executable below performs a finite capability and structural-byte selection. It rejects outgoing-only CSR for a bidirectional graph workload, chooses the smallest modeled feasible graph candidate, and selects a text hybrid because analyzed phrase and prefix completion are distinct capabilities. It demonstrates checked formulas and requirement coverage only; it is not a benchmark, complete byte inventory, production design proof, or universal recommendation.

<!-- bijux-verify: {"id":"representation-decision-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"graph_vertices=1000000\ngraph_edges=10000000\ncsr_bytes=48000008\ncsr_csc_bytes=96000016\nbit_matrix_bytes=125000000000\ngraph_required=in,out,scan\ngraph_choice=csr_csc\ngraph_ratio_vs_matrix=1302\ntext_documents=1000000\ntext_tokens=100000000\ntext_required=phrase,prefix,term\ntext_choice=inverted+trie\nchange_policy=immutable_base_plus_delta\nall_requirements_covered=True\nevidence=finite_representation_decision_trace\n","stderr":""}} -->
```python
n = 1_000_000
m = 10_000_000
csr_bytes = 8 * (n + 1) + 4 * m
csr_csc_bytes = 2 * csr_bytes
bit_matrix_bytes = (n * n + 7) // 8

graph_required = {"out", "in", "scan"}
graph_candidates = {
    "csr": ({"out", "scan"}, csr_bytes),
    "csr_csc": ({"out", "in", "scan"}, csr_csc_bytes),
    "bit_matrix": ({"out", "in", "scan", "adjacency"}, bit_matrix_bytes),
    "hash_adjacency": ({"out", "in", "scan", "update", "adjacency"}, 400_000_000),
}
feasible_graph = [
    (bytes_used, name)
    for name, (capabilities, bytes_used) in graph_candidates.items()
    if graph_required <= capabilities
]
graph_choice = min(feasible_graph)[1]

text_required = {"term", "phrase", "prefix"}
text_candidates = {
    "inverted": {"term", "phrase", "rank"},
    "trie": {"prefix", "dictionary"},
    "suffix_array": {"substring", "prefix_of_suffix"},
    "inverted+trie": {"term", "phrase", "rank", "prefix", "dictionary"},
}
feasible_text = [name for name, capabilities in text_candidates.items() if text_required <= capabilities]
text_choice = sorted(feasible_text)[0]
covered = graph_required <= graph_candidates[graph_choice][0] and text_required <= text_candidates[text_choice]

print(f"graph_vertices={n}")
print(f"graph_edges={m}")
print(f"csr_bytes={csr_bytes}")
print(f"csr_csc_bytes={csr_csc_bytes}")
print(f"bit_matrix_bytes={bit_matrix_bytes}")
print("graph_required=in,out,scan")
print(f"graph_choice={graph_choice}")
print(f"graph_ratio_vs_matrix={bit_matrix_bytes // csr_csc_bytes}")
print("text_documents=1000000")
print("text_tokens=100000000")
print("text_required=phrase,prefix,term")
print(f"text_choice={text_choice}")
print("change_policy=immutable_base_plus_delta")
print(f"all_requirements_covered={covered}")
print("evidence=finite_representation_decision_trace")
```

## Definitions and Notation

Let a requirement set `R` contain semantic and operational capabilities; candidate `c` has capability set `C_c` and is feasible only if `R subset C_c` plus all non-capability constraints hold. `n,m` are graph vertices/stored edge entries; `D,T,V` can denote documents, tokens, and vocabulary. `B_final`, `B_peak`, `B_delta`, and `B_retained` are separately measured byte envelopes.

A canonical view owns logical facts; derived view `I_g` is built from generation `g`. A reader snapshot names one manifest `g` and permitted deletion/delta subgeneration. Amplification ratios name numerator/denominator and observation window. An ADR is evidence-linked, dated, owned, and revisitable rather than an eternal theorem.

## Mechanisms, Invariants, or Proof Structure

Decision correctness has four gates: semantic fidelity; hard capability/constraint feasibility; analytical resource feasibility; representative verified measurement. Only candidates passing earlier gates proceed. Cross-view correctness reconstructs the same canonical logical relation/sequence and maps stable IDs/coordinates under one generation. Lifecycle proof covers private build, validation, atomic publication, reader pinning, failure rollback, and reclamation.

Evidence strength is claim-specific: invariant tests prove finite/covered correctness; mathematical derivations prove scoped bounds; benchmarks support measured workload/platform behavior; crash/concurrency/security reviews cover their domains; external review requires named records. A numeric score cannot replace missing evidence.

## Alternatives and Trade-Offs

| Decision shape | Strength | Principal risk |
|---|---|---|
| one mutable representation | simple ownership/immediate updates | contention, fragmentation, missing alternate operations |
| one immutable packed view | compact fast reads | rebuild and unsupported queries |
| canonical plus derived views | workload-specialized queries | cross-view generations and amplification |
| base plus delta | read-mostly updates | merge cost/read amplification/debt |
| partitioned/segmented views | bounded parallel rebuild | fan-out, global statistics, cross-boundaries |
| universal over-indexing | future query flexibility | write/storage/privacy/operations explosion |
| minimal indexing | low cost/attack surface | expensive or impossible new queries |

Choose the smallest operationally sustainable set that proves every hard contract and has a migration path for plausible future needs.

## Failure Modes and Misconceptions

- Big-O filters candidates but does not provide byte, locality, tail, or lifecycle evidence.
- A representation can be fast and semantically infeasible.
- Derived-view eventual consistency is not acceptable unless named in query contracts.
- Final bytes do not prove rebuild fits.
- One average benchmark cannot cover skew, outputs, concurrency, background work, cold state, or growth.
- A stable logical ID is not an array slot or segment-local integer.
- Compression adds decoders/block metadata and a corruption boundary.
- Immutable structures simplify reads but still need publication/lifetime/recovery.
- Multiple views expand privacy and authorization proof surfaces.
- An ADR without evidence, triggers, owner, migration, and rollback is documentation theater.

## Worked Examples

### Example 1

An outgoing-only graph index is rejected when 30% of hard queries enumerate predecessors; lower bytes cannot compensate for missing capability. Add CSC, build transpose per query within SLO, or change the requirement explicitly.

### Example 2

At one million vertices, a one-bit directed matrix costs about 125 GB before row metadata, while structural CSR+CSC in the finite width model costs about 96 MB. Density and hardware could change a smaller graph's result.

### Example 3

A graph with one hub holding half of `m` defeats one-thread-per-vertex balance. Edge-balanced splits and segmented reduction become representation/scheduler requirements despite acceptable total bytes.

### Example 4

A term-only inverted index answers `data AND engineering` but cannot distinguish adjacent phrase from separated tokens. Positions or source verification are required, with different cost.

### Example 5

A trie over analyzed terms autocompletes dictionary prefixes but cannot find arbitrary raw substring crossing token boundaries. A suffix/n-gram view or bounded scan is a separate capability.

### Example 6

An immutable 80-GB base, 10-GB delta, 80-GB replacement, and 20-GB temporary buffers require roughly 190 GB peak before safety margin/readers, not the 80-GB final headline.

### Example 7

CSR generation 12 and CSC generation 11 use different dense vertex mappings after compaction. Joining their slots returns wrong edges even though both files validate independently; the manifest must prevent mixed views.

### Example 8

An ACL filter after text top-k removes hidden documents but fails to return lower-scoring visible ones. Authorization must participate in candidates/pruning or use a proven completeness strategy.

### Example 9

A benchmark's p50 improves 30% while p99.9 doubles during merge. If tail SLO is hard, the candidate fails or needs resource isolation/throttling despite throughput improvement.

### Example 10

An ADR revisits when incoming-query share exceeds 5%, delta exceeds 10% of base, p99 crosses 50 ms, analyzer changes, or rebuild peak exceeds 75% capacity. These triggers make evolution actionable.

## Cross-Program Connections

- **Database engineering:** canonical/secondary indexes, schemas, WAL, snapshots, compaction, query planning, and migration are direct analogues.
- **Data engineering:** governed transformations, distribution profiling, batch/stream deltas, lineage, manifests, backfills, and data-quality checks drive representations.
- **Software engineering:** ADRs, API contracts, ownership boundaries, observability, failure semantics, and incremental migrations make choices durable.
- **Cloud/platform engineering:** capacity, object/block storage, NUMA/accelerators, rollout/rollback, background isolation, and cost objectives constrain designs.
- **Security engineering:** namespace identity, parser bounds, authorization during traversal, amplification, provenance, and index leakage are first-class.
- **Concurrent/distributed systems:** immutable generations, atomic manifests, replication, consistency, reader pinning, reclamation, and partition fan-out shape lifecycle.
- **Research/QA:** formal invariants, differential references, representative benchmarks, named external review, and reproducible artifacts calibrate claims.

## References

1. [GraphBLAS Forum, *GraphBLAS C API Specification 2.1.0*](https://graphblas.org/docs/GraphBLAS_API_C_v2.1.0.pdf).
2. [Julian Shun and Guy E. Blelloch, *Ligra*](https://jshun.csail.mit.edu/ligra.pdf).
3. [Graph Based Benchmark Suite](https://paralg.github.io/gbbs/).
4. [NVIDIA, cuSPARSE storage formats](https://docs.nvidia.com/cuda/cusparse/storage-formats.html).
5. [Unicode Standard Annex #15, *Unicode Normalization Forms*](https://www.unicode.org/reports/tr15/).
6. [Christopher Manning, Prabhakar Raghavan, and Hinrich Schütze, *Introduction to Information Retrieval*](https://nlp.stanford.edu/IR-book/pdf/irbookonlinereading.pdf).
7. [Apache Lucene, maintained codec implementations](https://github.com/apache/lucene/tree/main/lucene/core/src/java/org/apache/lucene/codecs).
8. [PISA maintained source and documentation](https://github.com/pisa-engine/pisa).
9. [Princeton Algorithms, *Suffix Arrays*](https://algs4.cs.princeton.edu/63suffix/).
10. [Viktor Leis, Alfons Kemper, and Thomas Neumann, *The Adaptive Radix Tree*](https://db.in.tum.de/~leis/papers/ART.pdf).

## Exercises

### Exercise 1

Given a directed graph with 50 million vertices, 2 billion edges, both-direction scans, rare adjacency tests, daily 2% edge updates, 256 GB RAM, and an 8-hour rebuild window, produce a capability/byte/peak shortlist for CSR, CSR+CSC, hash adjacency, and base-plus-delta.

### Exercise 2

A service needs analyzed Boolean/phrase/ranked search, prefix autocomplete, exact raw substring on one small field, highlighting, hourly refresh, and stable external spans. Design canonical and derived text views with one generation contract.

### Exercise 3

Design a representative evidence matrix comparing two graph and two text candidates. Include correctness models, distributions, operations, failures, concurrency, persistence, security, metrics, and external-review boundaries.

### Exercise 4

Specify an atomic graph/text multi-view rebuild and cutover protocol. Include mapping, lineage, validation, peak capacity, shadow comparison, publication, pinned readers, rollback, recovery, and garbage collection.

### Exercise 5

Write the essential content of an ADR choosing representations for a multi-tenant graph-and-search product, including hard constraints, consequences, unsupported cases, revisit triggers, and migration plan.

## Answers to the Exercises

### Answer 1

With 64-bit offsets and 32-bit endpoints, one CSR structure is about `8*(50,000,001)+4*2,000,000,000`, roughly 8.4 GB before properties/mapping/alignment; CSR+CSC about 16.8 GB. Both-direction scans reject CSR-only unless transpose-on-demand meets the hard SLO. A one-bit matrix is infeasible (`50,000,000^2/8`, hundreds of terabytes). Hash adjacency needs measured buckets/capacity/entries and likely much more than packed arrays but supports updates. Shortlist immutable CSR+CSC plus a stable-ID delta/tombstone overlay: size delta for daily 2%, bound per-row skew, query merge, and compact within eight hours. Peak includes old 16.8 GB, new 16.8 GB, delta, COO/count/sort buffers, properties/mappings, reader retention, and safety margin; verify under 256 GB. Also measure whether chunked/hash adjacency is justified by update/tail workload rather than assume.

### Answer 2

Canonical store owns immutable raw document versions, external IDs, field schema, and analyzer/normalization plus indexed-to-original span mappings. A positional inverted segment owns term/frequency/position/offset/norm data for Boolean/phrase/ranked/highlight. A trie/FST dictionary with governed popularity metadata supports autocomplete. The small raw-substring field gets a suffix-array/FM/n-gram-plus-verification view over its exact canonical bytes and span map. One manifest names document/analyzer generation, all indexes, live masks, statistics, and checksums; hourly private builds validate and publish atomically. Queries pin it. Updates enter WAL/delta/new segments; deletes mask old versions. ACL/tenant filters apply during candidates. Rebuild on analyzer changes or explicitly dual-query only during migration; stable external IDs/spans never use internal term/doc/suffix slots.

### Answer 3

For graph candidates (for example CSR+CSC and chunked/hash base+snapshot), compare against an edge-ID multigraph reference across direction, loops, parallels, properties, out/in/adjacency/scan, update/delete, algorithms, conversion, corruption, crash, snapshot, authorization, and reclamation. Use uniform, skewed/hub, partitioned, temporal, sparse/dense-boundary real/synthetic graphs. For text candidates (positional inverted+trie and inverted+suffix/n-gram hybrid), compare raw/analyzed reference tokens/spans/terms/phrases/prefixes/substrings/ranks/deletes/ACLs under Unicode and malformed codec inputs. Measure final/peak/delta/cache/retained bytes; build/refresh/merge/recovery; p50 through p99.9 queries/output; counters, cold/warm, threads/NUMA/storage, cancellation, amplification. Fault/crash every publication step and pin readers. Internal evidence supports scoped claims only; named external academic/practitioner/security/relevance/operations reviews remain separate.

### Answer 4

Freeze canonical input generation and stable external IDs; derive dense graph/doc/text coordinate mappings with lineage and digests. Capacity-plan old+new+delta+temporary+slow-reader generations. Build every view privately from the same generation, record tool/schema/analyzer/comparator/version, and validate internal plus cross-view logical equality. Shadow queries/algorithms against current and reference, including ACL and coordinate mappings. Flush/checksum files and atomically publish one durable manifest referencing the complete view set and live delta/deletion generation. Readers acquire/pin manifest; new readers switch, old complete on old files. Keep previous manifest/files and delta replay point for rollback/recovery. On failure never modify active manifest. After observation window and reader drain, garbage-collect through audited references. Reconcile updates arriving during build through a bounded delta or restart/catch-up protocol.

### Answer 5

The ADR states tenants, graph/text identities, schemas/analyzers, stable IDs/coordinates, hard queries/SLOs/durability/ACL/capacity, workload distributions/growth, and candidate matrix. It records concrete final/peak/amplification models and reproducible correctness/benchmark/failure evidence. The choice names canonical stores, graph CSR+CSC/base-delta, positional inverted/trie and any restricted substring view, segment/partition layout, mappings, manifest snapshots, WAL/recovery, authorization and limits. Consequences include duplicate structures, rebuild/merge cost, staleness policy, unsupported fully dynamic graph/raw-substring fields or locale ordering, and ownership. Triggers name measurable size/query/update/p99/delta/merge/capacity/schema/analyzer/security/library thresholds. Migration uses dual private build, shadow cross-view diff, capacity gate, atomic generation cutover, rollback retention, and eventual old-view removal; no external review is claimed without named records.
