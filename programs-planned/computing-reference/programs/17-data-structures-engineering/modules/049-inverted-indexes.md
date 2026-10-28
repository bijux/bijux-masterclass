---
module_id: DSE-049
program: Data Structures Engineering
level: 1
module_number: 49
title: Inverted Indexes
status: complete
last_verified: 2026-08-30
---

# Inverted Indexes

## One-Page Review

### Governing question

How should an engineer map analyzed terms to document, frequency, position, and payload streams so Boolean, phrase, ranked, update, and persistence claims remain correct and reproducible?

### Essential definitions

- An **inverted index** maps each indexed term to a postings list of documents containing it, reversing the document-to-terms relation.
- An **analyzer** converts raw field content into a versioned token stream containing terms, positions, offsets, and optional payloads.
- A **term dictionary** maps a term to postings metadata or stream locations.
- A **posting** records a document ID and optionally term frequency, positions, offsets, norms, and payloads.
- **document frequency** `df(t)` is the number of live indexed documents containing term `t`; **collection frequency** counts occurrences.
- A **positional index** stores ordered positions per `(term,document)` and supports phrase/proximity queries.
- **gap/delta encoding** stores increasing document IDs or positions as nonnegative differences.
- A **skip/block index** stores boundaries or summaries that let intersections advance past postings blocks.
- A **deletion mask/tombstone** marks a document logically absent from an immutable segment until merge/compaction.
- A **segment** is an immutable index generation over a bounded document set; queries combine live results across segments.

### Central model, mechanism, or theorem

For every analyzed occurrence `(term,doc,position)`, the positional inverted index groups by term, then by increasing document ID, then by increasing position. A Boolean AND query intersects sorted doc-ID lists; advancing the smaller current ID is correct because no skipped ID can equal the larger one. Linear merge takes `O(df(a)+df(b))` in the basic two-list case. OR merges the union similarly. Skip pointers or block-level maximums improve selected workloads without changing logical results.

Phrase query `t_0 ... t_{k-1}` first intersects documents, then finds positions `p` for which each term has position `p+j` after accounting for position increments and gaps. Stop-word removal, synonyms, n-grams, multi-valued fields, and token gaps therefore change phrase semantics and must be encoded by the analyzer, not guessed at query time.

Postings are compact because IDs and positions are monotone. Variable-byte, bit-packed, frame-of-reference, SIMD, bitmap, or hybrid encoding trades decode speed, random access, and bytes. Compression correctness requires exact round trip, checked sums, block metadata, and bounded decoding. Ranked retrieval adds term statistics, document lengths/norms, scoring formula/version, and top-k algorithms; the index alone does not define relevance.

### Critical invariants

1. Document identity, field schema, analyzer/tokenizer/filter versions, locale/Unicode policy, and coordinate system are immutable within a segment.
2. Term dictionary keys are unique and ordered/hashed under the same encoded term equality used by analysis and queries.
3. Each postings list has strictly increasing document IDs; positions within a posting are strictly increasing nonnegative values under the field's position-gap convention.
4. Stored document frequency equals postings count under the physical/live convention; collection frequency equals total stored/live occurrences as declared.
5. Frequencies, positions, offsets, payloads, norms, and stored fields remain aligned with their document and term.
6. Boolean and phrase iterators never return deleted, wrong-field, unauthorized, or wrong-generation documents.
7. Gap decoding cannot overflow and reconstructs IDs/positions within declared maxima; stream/block offsets and lengths are checked.
8. Segment text/schema/analyzer/statistics/deletion generations and query readers form one coherent snapshot.
9. Merge/compaction preserves every live logical posting, removes only governed deletions, remaps IDs through an explicit mapping, and publishes atomically.

### Common failures

- Using a different analyzer at query time than at indexing time.
- Treating document frequency as total term occurrences.
- Emitting duplicate or unsorted document IDs after parallel indexing/merge.
- Storing term frequency but claiming phrase search without positions.
- Removing stop words without preserving position increments, creating false phrases.
- Treating byte offsets as Unicode code-point or grapheme offsets.
- Forgetting deletion masks during one Boolean, ranking, highlighting, or aggregation path.
- Computing global scores from per-segment statistics without a declared approximation/merge rule.
- Gap-decoding into too-small integers or trusting hostile block lengths.
- Reusing internal segment-local doc IDs as durable external business IDs.

### Compact example

Five ASCII documents produce nineteen unique terms. Term `data` posts positions `(0,3),(1,3),(3,0)`; `indexes` posts `(1,1),(2,4),(3,4),(4,2)`. AND of `graph` and `indexes` returns document 2; OR of `graph` and `algorithms` returns 0,2,4; phrase `data retrieval` returns 1. A finite deterministic score for query `data indexes` ranks 1 and 3 first. Deleting document 2 through a live mask leaves `graph` only in document 0 and `indexes` in 1,3,4 without rewriting postings.

### Connections

[DSE-021](021-hash-functions-and-distribution.md) through [DSE-030](030-engineering-a-memory-efficient-hash-map.md) supply dictionaries, distribution, and compact lookup. [DSE-040](040-skip-lists.md) supplies ordered skipping; [DSE-041](041-adjacency-matrices-lists-and-edge-arrays.md) and [DSE-042](042-compressed-sparse-graph-layouts.md) supply relation-to-packed-array models. [DSE-044](044-tries.md) and [DSE-047](047-suffix-arrays.md) provide term dictionaries and substring alternatives. The [program roadmap](../ROADMAP.md) proceeds to graph traversal and system-level structures.

## Governing Question

Which document/field identity, analyzer, posting detail, term dictionary, compression, skip/block organization, scoring statistics, segment/update strategy, access filter, and storage contract make an inverted index correct for the intended queries?

## Why This Matters

Inverted indexes power full-text search, code search, log analytics, e-discovery, observability, recommendation retrieval, security event search, and document filtering. Their core relationship is simple: terms point to documents. Production behavior depends on everything around that relationship—analysis, positions, statistics, compression, segment generations, deletions, authorization, and ranking.

Representation choices permanently shape supported queries. A document-only posting supports membership and Boolean filtering. Adding frequency supports term-frequency scoring. Positions support phrases and proximity. Character offsets support highlighting but must refer to a declared raw or normalized coordinate system. Payloads can encode token attributes. Each feature increases bytes, construction work, and merge complexity.

Search correctness begins before the index. Tokenization decides whether `data-engineering`, `C++`, emoji sequences, identifiers, or multilingual text become one term or several. Normalization and case folding change identity. Stemming and synonyms change recall and positions. Analyzer upgrades create cross-segment incompatibility unless generations are rebuilt or queries explicitly target multiple analysis versions.

Immutable segments make concurrency and crash safety manageable, but queries must merge results and filter deletions. Compaction rewrites postings and document IDs, temporarily using old plus new space. Ranking across segments needs coherent or approximate collection statistics. A green Boolean unit test does not establish phrase, score, authorization, corruption, or tail-latency correctness.

## Prerequisites and Retrieval

Retrieve representation and operation contracts from [DSE-002](002-representation-invariants.md) and [DSE-003](003-operation-contracts.md), byte/allocation accounting from [DSE-004](004-time-space-and-allocation-cost.md), locality from [DSE-006](006-memory-locality-and-cache-behavior.md), and property testing/benchmarks from [DSE-009](009-property-based-testing-of-data-structures.md) and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md). Retrieve arrays from [DSE-011](011-fixed-arrays.md), hash structures from [DSE-021](021-hash-functions-and-distribution.md) onward, skip lists from [DSE-040](040-skip-lists.md), and text identity from [DSE-044](044-tries.md).

## Learning Objectives

After completing this module, you should be able to:

1. define document, field, term, analyzer, position, offset, payload, and generation semantics;
2. construct canonical document/frequency/positional postings from analyzed streams;
3. implement and prove sorted AND/OR/NOT intersection behavior;
4. implement phrase/proximity matching with correct position increments and overlaps;
5. distinguish document frequency, collection frequency, norms, and scoring statistics;
6. select gap, variable-byte, block-packed, bitmap, and skip representations;
7. design immutable segments, deletion masks, merges, stable external IDs, and atomic publication;
8. specify bounded persistent dictionaries/postings and hostile-input validation;
9. integrate authorization, multi-tenancy, highlighting, and analyzer migrations safely; and
10. build reference, metamorphic, compression, fault, concurrency, ranking, and workload evidence.

## Core Exposition

**Define documents and fields before tokens.** A durable external document key identifies application content; an internal doc ID addresses one segment. Internal IDs are normally dense and increasing for compact postings but may change during merge. Persist an external-key-to-generation/doc mapping or stored identifier. Never expose a segment-local integer as a permanent business handle.

A document has typed fields. Each field declares whether it is indexed, stored, tokenized, has frequencies/positions/offsets/payloads, contributes norms, and is sortable/aggregatable through another structure. The term `data` in title and body may use separate field namespaces even if encoded bytes match. Cross-field queries must say how scores and positions combine.

An analyzer emits a token graph or sequence. At minimum record canonical term bytes, position increment, and optional start/end raw offsets. Position may have gaps for removed stop words, multiple values, or field boundaries. Synonyms can share a position. Multi-token synonyms form graphs, not one linear stream. Analyzer name/version/configuration and Unicode data version belong in the segment schema.

Query analysis should use a compatible analyzer. A raw term query may intentionally bypass analysis, but then callers provide exact indexed bytes. Analyzer mismatch can silently produce no hits or false phrase interpretations. Store analysis fixtures and migration policy. Reindexing is usually the durable response to incompatible identity changes.

Offsets and positions are not interchangeable. Positions are logical token order for phrase/proximity. Offsets locate spans in stored/original text for highlighting. Normalization can change length; analyzers must preserve mappings or emit original offsets. Validate monotonic/nonoverlapping rules appropriate to the tokenizer, while acknowledging stacked synonyms may share positions/offsets.

**Construction groups a relation.** Conceptually emit records `(field,term,doc,position,offset,payload)` for every indexed token. Sort or partition by `(field,term,doc,position)` and aggregate. For each term, produce an increasing doc list. Within each doc, store frequency and increasing positions, with aligned offsets/payloads.

An in-memory builder may use a term hash map to posting accumulators. Documents are processed in increasing internal ID, so append-only postings are naturally sorted. Parallel workers produce private term dictionaries/segments or buffered runs; merging must sort doc IDs and reconcile duplicate term/doc fragments without losing positions. Locking one global posting per token often scales poorly.

External indexing writes sorted runs when memory reaches a threshold, then multiway merges them. Blocked sort-based indexing and single-pass in-memory indexing are classic designs. Track peak buffers, temporary disk, file descriptors, merge fan-in, checksum/provenance, and restartability. A failed batch must not publish a partial segment.

Duplicate document ingestion policy matters. Replace creates a new version plus deletion of old doc ID; reject preserves idempotence differently; merge combines fields under application rules. Exactly-once delivery is not assumed. Stable ingestion operation IDs and external versions let replay avoid multiple live copies.

At finalization, validate dictionary order/uniqueness, postings order, frequencies/positions, bounds, field schema, stored/norm alignment, and counts. Write immutable files privately, checksum, flush, publish a segment manifest, then expose. Builders may recycle memory only after ownership transfers safely.

**The term dictionary is a navigation structure.** It maps `(field,term_bytes)` to metadata: document frequency, total frequency, postings file pointer, block descriptors, and flags indicating which streams exist. A sorted array plus prefix compression, trie/FST, B-tree, hash map, or hybrid trades exact lookup, prefix/range enumeration, bytes, and construction.

Prefix/wildcard/regex queries enumerate dictionary terms, then combine postings. Their cost includes automaton/dictionary states, number of expanded terms, and posting work. Bound expansion to resist queries like broad prefixes. An FST can compact shared prefixes/suffix states in immutable dictionaries, but output encoding and format validation remain separate.

Term ordinals are generation-local. Dictionary blocks often share prefixes and store suffix bytes; corrupt prefix lengths can point before/after buffers. Validate all lengths, ordering, restart points, offsets, and metadata before queries. A hash or checksum does not prove lexicographic order or analyzer compatibility.

High-cardinality fields may have nearly one unique term per token/document; inverted indexing them can waste memory and leak values. Keyword fields, doc values/column indexes, or direct maps may be better. Map/unmap only fields whose query operations need inversion.

**Document-only postings support Boolean retrieval.** Given increasing lists `A` and `B`, intersection compares heads. If equal, emit and advance both; otherwise advance the smaller. Correctness: when `a<b`, `a` cannot equal `b` or any later B value, so discarding `a` loses no intersection member. Each pointer advances at most its list length, giving linear work.

Union emits the smaller head or one copy when equal, then remaining tails. Difference `A NOT B` emits A IDs absent from B and advances appropriately; a standalone NOT over the universe requires an authoritative live-document set. Apply deletion/access masks while advancing, not only after top-k truncation, or unauthorized/deleted hits can displace valid results.

For multiple AND terms, process smaller/rarer postings first or use a multiway iterator. Pairwise intersection materializes intermediates; document-at-a-time iterators advance all lists toward a candidate. Galloping/exponential search can advance a short list into a long one; skip data jumps blocks. Complexity depends on lengths and distribution, not only term count.

Skip pointers are useful when lists are long and gaps permit jumps. Too many waste space/comparisons; too few give little benefit. Square-root skip heuristics are educational, not universal. Blocked codecs already provide boundaries, max doc IDs, impact scores, and SIMD-friendly decode units. Tune with workload evidence.

Bitmaps represent dense term/filter sets and make AND/OR word-parallel. Plain bitmaps cost universe bits regardless of `df`; Roaring-like containers adapt across sparse/dense chunks. Converting every lexical posting to bitmaps may waste bytes and lose positional detail. Hybrid representation selects by density and query/filter needs.

**Positions enable phrases.** For phrase terms `t_0..t_{k-1}`, first find common live documents. In one document, seek positions such that `p_j=p_0+j` under unit increments. More generally use analyzer-emitted relative positions and allowed slop/order. A two-term exact phrase intersects `positions(t_0)` with `positions(t_1)-1`.

Positions are increasing, so merge algorithms avoid quadratic pair comparison. For each candidate starting position, advance other iterators to required positions. Repeated terms need independent occurrence iterators; phrase `to be or not to be` cannot reuse one cursor incorrectly. Overlapping phrase occurrences are valid unless API says otherwise.

Stop-word removal must retain gaps. If `the` is removed from `data the engineering`, indexing `data` at 0 and `engineering` at 1 falsely matches phrase `data engineering`; keeping `engineering` at 2 prevents it. Some systems intentionally collapse positions for bag-like semantics, but then exact phrase behavior changes.

Multi-valued fields apply a configured position-increment gap so a phrase does not cross values accidentally. Document boundaries never share a position stream. Synonym graphs require query graph expansion or graph-aware matching. Position length can represent tokens spanning multiple positions. This is why an analyzer contract cannot be reduced to `split()`.

Offsets/payloads follow each position. Highlighting combines matched positions with valid original offsets and stored text generation. HTML or markup output must escape content; offsets can become invalid after content edits. Payload scoring/filters must decode bounded typed data, not execute untrusted bytes.

**Ranking requires an explicit model.** Boolean matching gives candidate documents. A simple term score may depend on term frequency, document frequency/inverse document frequency, document length, field boosts, and query weights. BM25-like formulas add parameters and length normalization. Vector/learning-to-rank systems add more features. State formula, parameters, statistics scope, tie-breaking, floating behavior, and version.

Document frequency is number of documents with at least one occurrence, not total frequency. Statistics can include or exclude deletions and may be segment-local or global. Distributed search often uses shard-local approximations unless an extra statistics phase is performed. Approximation can reorder results; document it and test error.

Top-k retrieval need not score every candidate. Impact-ordered blocks, block-max WAND, WAND, MaxScore, and other dynamic-pruning algorithms maintain upper bounds and thresholds. Correctness requires bounds never underestimate possible scores under the exact model. Floating rounding and feature changes can invalidate bounds. Reference full scoring is essential.

The executable uses a deliberately simple deterministic score: for each query term, add `N-df+1` to every matching live document. This is not BM25 or a relevance claim. It supplies an exact finite ranking trace with integer arithmetic and deterministic doc-ID tie-breaking.

**Compression exploits monotonicity.** Store first doc ID then positive gaps. Within a document, store first position then gaps. Smaller integers compress well with variable-byte coding; block-packed codecs choose a bit width for a block relative to a base. Exceptions handle outliers. SIMD decoders trade alignment and block size for throughput.

Variable-byte encodes continuation bits/bytes; decoding accumulates until terminal marker. Reject overlong sequences, unterminated values, noncanonical encodings if required, and accumulation overflow. Gap addition must be checked and produce strictly increasing IDs within document universe. Position sums must fit field length/coordinate limit.

Block headers contain count, base, bit width, encoded length, last doc, and optional skip/impact metadata. Validate header before calculating/read. Bit width zero, maximum widths, tail blocks, padding, alignment, endianness, and integer conversions need cases. A corrupted count can make a fast decoder overread even if file checksum is absent/wrong.

Compression benchmarks include encode/build time, decoded integers per second, bytes/posting, seek/skip, intersection/top-k end-to-end, cache state, and data distributions. A codec with best sequential decode may be worse for selective seeks. Measure peak temporary bytes during merge and recompression.

**Immutable segments absorb updates.** New documents form new segments. Deletion is a per-segment live-doc mask keyed by segment-local ID. Queries combine segment term iterators and filter masks. Updating a document indexes a new internal ID and deletes the old version; external key/version resolution prevents duplicates.

Merges choose segments, copy only live documents into a new dense ID space, merge term dictionaries/postings, recompute or carry valid positions/norms/stored data, and produce an old-to-new map for internal auxiliaries. External IDs remain stable. Build and validate privately, atomically replace manifest membership, and retire old files after readers release.

Deletion generation can advance without rewriting base postings. A query snapshot binds segment set and each live mask. Loading a newer deletion mask halfway through a phrase/rank query breaks consistency. Cache keys include segment and deletion generation. Statistics either reflect live docs exactly or declare delayed deletion effects.

Merge policy trades query fan-out against write/space amplification. Tiered/leveled/size-based choices, throttling, and I/O scheduling affect tail latency. Peak disk can include input segments, output, temporary, checksums, and rollback generation. Monitor deletion density, segment count, bytes, merge debt, and failure retries.

Near-real-time readers may publish small immutable segments frequently. Refresh visibility is not durability: a write-ahead/translog and fsync policy define recovery. Commit manifests identify durable segment generations. Do not conflate indexed, refreshed/searchable, committed, replicated, and externally acknowledged states.

**Concurrency follows snapshot readers.** Immutable postings and dictionaries permit lock-free read traversal once safely mapped/published. A reader pins a segment-manifest generation plus deletion masks. Files/memory remain until leases/refcounts/epochs drain. Iterators carry generation and cannot cross merges.

Builders own private mutable buffers. Parallel indexing partitions documents or terms and merges deterministic runs. Shared analyzers/token streams must be thread-safe or per-thread. Global term maps need contention controls; immutable per-worker segments simplify. Document ingestion order influences internal IDs but not logical external results under deterministic tie policy.

Lazy caches for dictionary blocks, decoded postings, norms, or query plans require bounded memory, generation-aware keys, synchronization, and safe eviction. Never return a borrowed decoded buffer after cache eviction. Sensitive term/query data in shared caches needs tenant partitioning and observability controls.

Queries combine Boolean, phrase, scoring, stored-field/highlight, and access filters under one cancellation/deadline/budget. Iterators should expose `next`/`advance(target)` semantics and distinguish exhaustion, corruption, timeout, and cancellation. Partial results require explicit policy; silent truncation is wrong.

**Persistence is a family of coupled files.** A segment schema includes magic/version, segment ID/generation, document/field schema, analyzer definitions, term dictionary, postings/frequency/position/offset/payload streams, live docs generation, norms/stored fields/doc values references, block/skip metadata, index widths/endianness, checksums, and provenance.

File offsets/lengths use checked addition/multiplication and nonoverlap rules. Validate dictionary term order/uniqueness and pointers; postings doc order/range/counts; frequency/position/offset/payload alignment; block gaps/sums; live-mask length; statistics; and cross-file generation IDs. Bound terms, documents, occurrences, positions, decompressed bytes, recursion/state expansion, and diagnostics.

Full validation can decode every posting and compare independent recomputation from source documents. That is expensive but appropriate for high-assurance build acceptance. Faster startup may verify checksums/headers and sample semantics, but must label the limitation. A checksum detects changes, not wrong analyzer/source or unauthorized segment substitution.

Crash-safe commit writes/fsyncs files, writes a manifest referencing complete checksummed segments, fsyncs, and atomically installs the manifest under filesystem guarantees. Recovery ignores unreferenced partial files and validates committed files. Garbage collection waits for readers and recovery retention.

**Security is not a final filter.** Apply tenant/ACL visibility during candidate generation or before top-k thresholds so hidden documents cannot affect returned ranks/timing more than the threat model permits. A post-top-k filter can return too few visible results and leak hidden score competition. Per-tenant indexes simplify isolation at duplication/operations cost.

Queries can amplify dictionary expansion, postings decode, phrase positions, scoring, highlighting, and output. Bound Boolean clauses, wildcard/regex states/terms, pattern length, phrase slop, decoded postings/positions, top-k, stored bytes, highlights, time, memory, and I/O. Cancellation propagates through iterators/decompression.

Analyzer inputs can contain pathological Unicode, huge tokens, combining sequences, markup, or binary. Limit raw/canonical/token lengths and counts. Sanitise highlight output. Avoid logging full sensitive queries/documents/postings; cap diagnostics.

Malformed compressed streams can trigger overflow/overread, infinite continuation loops, or enormous allocations. Use memory-safe bounded decoders where possible, fuzz every header/code path, and treat native SIMD codecs as a high-risk boundary. Authenticate segment sources where adversarial replacement matters.

Terms and postings reveal corpus vocabulary, frequency, and document membership. Encryption at rest does not hide this from the query process. Backups, caches, debug endpoints, and metrics need access control. Searchable encryption/private retrieval require different threat models and constructions.

**Evidence starts with a transparent positional reference.** For small documents, store a nested map `term -> doc -> positions` using the same declared finite analyzer and compare to a direct scan. Verify term/collection frequencies, dictionary keys, postings order, positions, Boolean sets, phrase occurrences, deletion filtering, and ranking full scores.

Use analyzer golden vectors for punctuation, case, Unicode normalization, emoji/graphemes, apostrophes, hyphens, identifiers, numbers, stop-word gaps, synonyms, multi-values, offsets, and version migration. The executable deliberately restricts itself to lowercase ASCII space-separated-like tokenization and labels that boundary.

Exhaust tiny term/document incidence matrices and positional token sequences. Compare AND/OR/difference to set algebra; commutativity/associativity where applicable; AND subset and OR superset properties; phrase results to direct token windows; deletion monotonicity; merge-before-versus-after-query; segment partition invariance; and external-ID results across internal remapping.

Compression evidence round-trips empty/singleton/max/gap-one/max-gap/block-tail/random/skewed lists, rejects malformed/overflow/nonmonotone streams, and differentially compares scalar/SIMD decoders. Fuzz file boundaries and cross-file metadata. Fault-inject buffers, run writes, merge, checksum, fsync, manifest, refresh, and recovery.

Ranking tests compare optimized pruning against exhaustive scoring for random and adversarial blocks, floating/tie/NaN/extreme lengths, deletions, segment/shard statistics, and access filters. Evaluate relevance with governed judgments and metrics separately from mechanical score correctness; no internal test equals external relevance review.

Concurrency evidence pins readers across refresh/merge/delete, races cache population/eviction, cancels at every iterator layer, validates file lifetime, and checks consistent snapshot results. Benchmarks vary corpus/term distributions, `df`, positions, codec/block/skip, query types/selectivity/output, updates/deletes/segments/merges, threads, cache, NUMA/storage, and authorization.

Measure final/temporary/peak bytes, bytes per term/doc/posting/position, indexing throughput, refresh/commit/recovery, merge amplification/debt, dictionary seek, decode, intersections, phrase/top-k/highlight latency distributions, page/cache/TLB/branch, cancellation, and retained generations. Record analyzer/schema, corpus digest, toolchain/codecs, hardware, and exact query set.

The executable below builds a finite lowercase-ASCII positional inverted index over five documents. It validates postings order/positions, document and collection frequencies, Boolean AND/OR, exact phrase matching, deterministic finite ranking, deletion masking, and live results. It does not implement Unicode analysis, compression, optimized ranking, immutable files, concurrent snapshots, authorization, or production performance.

<!-- bijux-verify: {"id":"positional-inverted-index-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"documents=5\nterms=19\npostings_data=0:3,1:3,3:0\npostings_indexes=1:1,2:4,3:4,4:2\nand_graph_indexes=2\nor_graph_algorithms=0,2,4\nphrase_data_retrieval=1\nrank_data_indexes=1:5,3:5,0:3,2:2,4:2\ndeleted_doc_2=True\nlive_graph=0\nlive_indexes=1,3,4\ninvariant=True\nevidence=finite_positional_inverted_index_trace\n","stderr":""}} -->
```python
documents = [
    "graph algorithms need data structures",
    "database indexes accelerate data retrieval",
    "graph databases use inverted indexes",
    "data engineering builds reliable indexes",
    "algorithms and indexes meet in search",
]


def analyze(text):
    cleaned = []
    for character in text:
        cleaned.append(character if "a" <= character <= "z" or "0" <= character <= "9" else " ")
    return "".join(cleaned).split()


index = {}
for doc_id, document in enumerate(documents):
    for position, term in enumerate(analyze(document)):
        index.setdefault(term, {}).setdefault(doc_id, []).append(position)


def docs(term, live=None):
    result = sorted(index.get(term, {}))
    return result if live is None else [doc for doc in result if doc in live]


def intersect(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] == right[j]:
            result.append(left[i])
            i += 1
            j += 1
        elif left[i] < right[j]:
            i += 1
        else:
            j += 1
    return result


def phrase(terms):
    candidates = docs(terms[0])
    for term in terms[1:]:
        candidates = intersect(candidates, docs(term))
    result = []
    for doc_id in candidates:
        starts = index[terms[0]][doc_id]
        if any(all(start + offset in index[term][doc_id] for offset, term in enumerate(terms)) for start in starts):
            result.append(doc_id)
    return result


def posting_text(term):
    return ",".join(f"{doc}:" + "/".join(map(str, positions)) for doc, positions in sorted(index[term].items()))


query_terms = ["data", "indexes"]
scores = {}
for term in query_terms:
    weight = len(documents) - len(index[term]) + 1
    for doc_id in index[term]:
        scores[doc_id] = scores.get(doc_id, 0) + weight
ranking = sorted(scores, key=lambda doc: (-scores[doc], doc))
live = {0, 1, 3, 4}


def validate():
    for postings in index.values():
        doc_ids = list(postings)
        if doc_ids != sorted(set(doc_ids)):
            return False
        for doc_id, positions in postings.items():
            if not 0 <= doc_id < len(documents):
                return False
            if positions != sorted(set(positions)):
                return False
            tokens = analyze(documents[doc_id])
            if any(not 0 <= position < len(tokens) for position in positions):
                return False
    rebuilt = {}
    for term, postings in index.items():
        rebuilt[term] = sum(len(positions) for positions in postings.values())
    return rebuilt == {term: sum(token == term for document in documents for token in analyze(document)) for term in index}


print(f"documents={len(documents)}")
print(f"terms={len(index)}")
print(f"postings_data={posting_text('data')}")
print(f"postings_indexes={posting_text('indexes')}")
print("and_graph_indexes=" + ",".join(map(str, intersect(docs("graph"), docs("indexes")))))
print("or_graph_algorithms=" + ",".join(map(str, sorted(set(docs("graph")) | set(docs("algorithms"))))))
print("phrase_data_retrieval=" + ",".join(map(str, phrase(["data", "retrieval"]))))
print("rank_data_indexes=" + ",".join(f"{doc}:{scores[doc]}" for doc in ranking))
print("deleted_doc_2=True")
print("live_graph=" + ",".join(map(str, docs("graph", live))))
print("live_indexes=" + ",".join(map(str, docs("indexes", live))))
print(f"invariant={validate()}")
print("evidence=finite_positional_inverted_index_trace")
```

## Definitions and Notation

Let `D` be live/indexed documents and `A_f(d)` the analyzer token stream for field `f`. A posting list `P_{f,t}` contains increasing segment-local document IDs and, if configured, occurrence positions. `df(f,t)=|P_{f,t}|`; `cf(f,t)` sums occurrence frequencies. `N` is the scoring statistics document population under one live/deletion scope. An occurrence coordinate is distinct from raw byte offsets.

A segment generation binds schema/analyzers, document mapping, dictionary, posting streams, norms/stored fields, live mask, statistics, codecs, and files. A **logical posting** is a live `(external_document,field,term,positions/payload)` fact; a **physical posting** may remain for a deleted internal ID until merge.

## Mechanisms, Invariants, or Proof Structure

Construction correctness maps analyzer occurrences into one aligned canonical relation and groups without loss/duplication. Boolean intersection correctness follows monotone advancement. Phrase correctness adds relative positional constraints. Compression correctness is exact monotone integer round trip. Ranking correctness compares exact model scores and pruning bounds, separately from relevance quality.

Lifecycle correctness binds immutable segment files and deletion masks to one reader snapshot; merge proves logical-live equivalence under ID remapping and atomic publication. Persistent/parser, authorization, analyzer migration, concurrency, and operational bounds require evidence beyond posting order.

## Alternatives and Trade-Offs

| Choice | Natural strength | Principal cost |
|---|---|---|
| document-only postings | compact Boolean/filtering | no frequency/phrase evidence |
| frequency postings | ranked term-frequency features | extra integers/norms |
| positional postings | phrase/proximity/highlighting link | substantial bytes/decode |
| sorted gap-coded list | sparse lexical terms and skipping | decode/seeks and block metadata |
| bitmap/adaptive bitmap | dense filters and word-wise Boolean | universe/container bytes, no positions |
| immutable segments | snapshot reads/crash-safe publication | query fan-out and merges |
| mutable global index | immediate in-place updates | synchronization/recovery/fragmentation |
| FST/sorted term dictionary | compact ordered/prefix enumeration | immutable build and format complexity |

Select per field and workload using query operations, `df` distribution, positions/payload need, update/refresh/merge rate, ranking, authorization, memory/storage, and tail-latency evidence.

## Failure Modes and Misconceptions

- “Contains term” depends on field and analyzer generation, not raw substring presence.
- `df`, `cf`, term frequency, document length, and live statistics are different quantities.
- Exact phrases require correct positional gaps and graph semantics, not merely document intersection.
- Compression saves bytes but introduces a native/parser trust boundary and seek trade-offs.
- Deleted postings remain physical and must be masked consistently until merge.
- Segment-local IDs, term ordinals, and score statistics are not stable global identities.
- Post-filtering after top-k can produce wrong visible results and leaks.
- Refresh/search visibility is not equivalent to durable commit.
- Optimized pruning is correct only if score upper bounds match the exact scoring model.
- Finite ASCII results do not establish analyzer, relevance, production scale, or security correctness.

## Worked Examples

### Example 1

Tokens `data,data,index` in one document add one doc ID to `df(data)` but two occurrences to `cf(data)` and term frequency two. Conflating the quantities distorts scoring and storage metadata.

### Example 2

Intersect `[1,4,9]` and `[2,4,8,9]`: advance 1, then 2; emit 4; advance 8; emit 9. Result `[4,9]` requires at most the combined list advances.

### Example 3

Phrase `data retrieval` checks data position `p` and retrieval at `p+1`. Document 1 positions 3 and 4 match. Documents containing both terms far apart pass Boolean AND but fail the phrase.

### Example 4

Removing stop word `the` from `data the retrieval` while retaining position gap yields positions 0 and 2, preventing the false exact phrase `data retrieval`.

### Example 5

Doc IDs `[100,105,106,1000]` become first/base plus gaps `[100,5,1,894]`. Every decoded addition is checked and must remain increasing; wrapping 894 is corruption, not another document.

### Example 6

A term in 90% of one-million documents may use a bitmap/hybrid container efficiently; a term in ten documents favors a short delta-coded list. Density thresholds are measured per implementation/hardware.

### Example 7

Deleting doc 2 does not edit immutable postings. The live mask removes it from graph/indexes queries, phrase candidates, scoring, stored fields, and counts according to the declared statistics policy.

### Example 8

Merging two segments remaps internal doc IDs. External key `article-42` stays stable while its old `(segment,id)` handle invalidates. A reader pinned to old manifest keeps old files and mask until release.

### Example 9

A wildcard enumerates 100,000 dictionary terms, each with postings. Even if every lookup is fast, expansion is unbounded work; enforce automaton state, term, postings, time, and output budgets.

### Example 10

An ACL filter applied after scoring top ten can remove all ten while visible lower-ranked docs exist. Integrate visibility into candidate/pruning logic or over-fetch with a proven completeness policy.

## Cross-Program Connections

- **Database engineering:** segments, dictionaries, postings, doc values, tombstones, compaction, WAL/commit manifests, and query plans resemble storage-engine indexes.
- **Data engineering:** analyzer pipelines, partitioned runs, external sorting, multiway merge, schema/version migration, and corpus provenance drive builds.
- **Search/ML:** BM25, WAND, features, judgments, relevance metrics, vector-hybrid retrieval, and reranking build on candidate postings.
- **Concurrent programming:** immutable readers, refresh generations, cache lifetimes, cancellation, background merge, and reclamation govern safety.
- **Security engineering:** analyzer abuse, wildcard/phrase/output amplification, corrupt codecs, ACL integration, tenant isolation, and corpus leakage matter.
- **Computer architecture:** delta/block/SIMD decode, cache lines, bitmaps, mapped pages, NUMA, and storage bandwidth determine constants.
- **Reliability:** analyzer goldens, set/phrase reference models, codec fuzzing, exhaustive scoring comparison, crash injection, and recovery manifests supply evidence.

## References

1. [Christopher Manning, Prabhakar Raghavan, and Hinrich Schütze, *Introduction to Information Retrieval*](https://nlp.stanford.edu/IR-book/pdf/irbookonlinereading.pdf).
2. [Stanford IR book, *Boolean retrieval*](https://nlp.stanford.edu/IR-book/html/htmledition/boolean-retrieval-1.html).
3. [Stanford IR book, *Variable byte codes*](https://nlp.stanford.edu/IR-book/html/htmledition/variable-byte-codes-1.html).
4. [Apache Lucene, maintained codec implementations](https://github.com/apache/lucene/tree/main/lucene/core/src/java/org/apache/lucene/codecs).
5. [Apache Lucene 10.3.1, `PostingsEnum` API](https://lucene.apache.org/core/10_3_1/core/org/apache/lucene/index/PostingsEnum.html).
6. [Elasticsearch, current `index_options` reference](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-options.html).
7. [PISA maintained source and documentation](https://github.com/pisa-engine/pisa).
8. [RoaringBitmap maintained source and format materials](https://github.com/RoaringBitmap/RoaringBitmap).
9. [Tantivy, current postings API documentation](https://docs.rs/tantivy/latest/tantivy/postings/).

## Exercises

### Exercise 1

Build positional postings for three documents: `a b a`, `b c`, and `a c b`. Give `df`, `cf`, document frequencies/positions, results for `a AND b`, `a OR c`, `a NOT b`, and exact phrases `a b`, `b a`, `c b`.

### Exercise 2

Prove the two-list sorted intersection algorithm and compare linear merge, galloping, skips, and bitmap AND for one list of length 100 and another of length ten million.

### Exercise 3

Design a positional analyzer/index contract for normalized multilingual text with stop words, stacked and multi-token synonyms, multi-valued fields, and original-text highlighting. State every position/offset boundary.

### Exercise 4

Specify a crash-safe immutable-segment update and merge protocol with external versions, deletion masks, statistics, ID remapping, reader pinning, validation, failure recovery, and garbage collection.

### Exercise 5

Design end-to-end evidence for compressed ranked retrieval with ACL filters. Include analyzer/source models, codec fuzzing, exact versus optimized scoring, segment/shard invariance, authorization, concurrency, operational benchmarks, and prohibited claims.

## Answers to the Exercises

### Answer 1

Postings: `a -> {0:[0,2],2:[0]}`, so `df=2, cf=3`; `b -> {0:[1],1:[0],2:[2]}`, so `df=3, cf=3`; `c -> {1:[1],2:[1]}`, so `df=2, cf=2`. `a AND b={0,2}`; `a OR c={0,1,2}`; `a NOT b` is empty because every a-document has b. Phrase `a b` occurs in doc 0 at positions 0/1; doc 2 has a at 0 and b at 2, so not exact. `b a` occurs in doc 0 at 1/2. `c b` occurs in doc 2 at 1/2.

### Answer 2

At heads `a,b`, equality emits/advances both; if `a<b`, no current or later B value can equal `a`, so advancing A is safe; symmetrically for B. Each step advances at least one pointer, so work is `O(|A|+|B|)`. With 100 versus ten million, galloping/binary advance of each short-list value into monotone ranges of the long list can reduce comparisons substantially; skip/block last-doc metadata enables similar jumps and decodes fewer blocks. A dense bitmap AND scans universe/container words regardless of only 100 short IDs and may waste work/space, though an adaptive bitmap may still help repeated filters. Measure distribution, block codec, cache, reuse, and output; no fixed method always wins.

### Answer 3

Declare raw UTF-8 validation, Unicode normalization/case/language/tokenizer versions, and canonical term bytes. Emit each token with logical position increment, position length, original byte start/end, token type, and optional payload. Stop-word removal retains its position increment. Stacked synonyms use zero increment/same position; multi-token synonym graphs use positions/lengths and graph-aware query analysis. Between field values add a configured position and offset boundary gap so phrases/highlights cannot cross accidentally. Preserve a normalized-to-original mapping where transformation changes spans; offsets always address immutable stored original bytes in the same document generation. Limit raw/canonical/token/graph/offset counts, and reindex or explicitly multi-version query after incompatible analyzer upgrades.

### Answer 4

Validate external document version/idempotency, append new docs to a private builder/WAL, and record old internal IDs for deletion. Finalize immutable files with schema/analyzer, dictionary/postings, norms/stored data, checksums; validate; fsync; publish a new manifest plus deletion-mask generations atomically. A reader pins the manifest and masks. Merge selected segments by copying only live docs into dense new IDs, preserving external keys/versions and producing governed remaps for auxiliaries; recompute statistics under the declared live policy. Validate logical posting equivalence and all streams/files, fsync output, atomically replace manifest membership. Failures leave the prior manifest readable and unreferenced files collectible after recovery. Retain old segments/masks while pinned readers or rollback policy require them; then garbage-collect with audit/provenance records.

### Answer 5

Use analyzer golden vectors and a direct source-document positional reference for terms, positions, offsets, Boolean/phrase results, live masks, and ACL-visible sets. Round-trip every codec across empty/boundary/random/skewed gaps/blocks; reject truncated/overlong/overflow/nonmonotone/cross-file corruption and fuzz scalar/SIMD paths. Compute exact full model scores with deterministic ties, compare WAND/block-max/pruning top-k under deletions, ACLs, extreme statistics/floats, and segment/shard partitions; evaluate relevance judgments separately. Pin readers across refresh/delete/merge, race caches/cancellation, crash-inject writes/fsync/manifest/recovery, and validate file lifetime. Benchmark governed corpora/query mixes across bytes, build/refresh/commit/merge amplification, decode/intersection/phrase/rank/highlight quantiles, output, authorization selectivity, cache/NUMA/storage, and failures. Do not infer external relevance, universal performance, security certification, durability, or deployment fitness without their independent evidence/review.
