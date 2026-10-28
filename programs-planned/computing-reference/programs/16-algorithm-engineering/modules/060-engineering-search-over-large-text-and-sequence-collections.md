---
module_id: ALGE-060
program: Algorithm Engineering
level: 2
module_number: 60
title: Engineering Search over Large Text and Sequence Collections
status: complete
last_verified: 2026-09-05
---

# Engineering Search over Large Text and Sequence Collections

## One-Page Review

### Governing question

How should an engineer turn exact and approximate string-search algorithms into a collection-scale system whose representation, index, query plan, update model, resource bounds, and evidence match the promised search semantics?

### Essential definitions

- A **collection** is a set or ordered family of documents or biological sequences with stable identities and explicit boundaries.
- An **inverted index** maps a term to a sorted postings list of document identifiers, optionally positions and payloads.
- A **positional posting** records where a term occurs, enabling phrase and proximity predicates.
- A **suffix index** supports substring search over symbols rather than tokenized terms.
- An **FM-index** combines the Burrows-Wheeler transform, rank queries, and sampled locations to support compressed full-text search.
- **Seed-and-verify** retrieves candidates from exact seeds, then applies a more expensive exact or heuristic verifier.
- A **segment** is an immutable or append-oriented index unit combined with others at query time.
- **Recall** is the fraction of relevant results retrieved; **precision** is the fraction of retrieved results that are relevant, under a declared relevance definition.

### Central model, mechanism, or theorem

For sorted postings lists $P_1$ and $P_2$, a two-pointer intersection advances the smaller document identifier and costs $O(|P_1|+|P_2|)$ comparisons. Phrase search first finds common documents, then intersects shifted positions: a phrase $t_0\ldots t_{k-1}$ occurs at position $p$ exactly when $p+i$ is in the positional list for $t_i$ for every $i$.

For a suffix array or FM-index over a byte sequence with explicit collection separators, exact pattern matching returns a suffix interval. Locating occurrences may require sampled-position recovery, and each location must be mapped back to a document without allowing a match to cross a boundary. Approximate retrieval adds candidates; only a declared verifier can establish the promised distance or score condition.

### Critical invariants

- Document identity, byte encoding, normalization, tokenization, alphabet, and boundary policy are versioned.
- Every posting is sorted by one global identifier order; positions are sorted within a document.
- Published segments are immutable and paired with a consistent metadata snapshot.
- Deletions and replacements have explicit visibility semantics; no stale version is silently returned.
- Candidate generation cannot be mistaken for verification.
- Query budgets cover postings decoded, candidates verified, bytes read, memory, time, and output.
- Evaluation preserves a frozen corpus/query/judgment snapshot and reports tail latency and quality together.

### Common failures

Common failures include indexing one normalization and querying another; concatenating documents without unique separators; ordering conjunctions by syntax rather than selectivity; storing document postings when phrase semantics need positions; treating Bloom filters or seeds as proof of absence or similarity outside their guarantees; merging segments without snapshot isolation; benchmarking a warm toy corpus; hiding candidate caps that reduce recall; and reporting top-$k$ latency without defining relevance or tie policy.

### Compact example

For `red fox`, intersect the document postings for `red` and `fox`. In each surviving document, take every `red` position $p$ and test whether `fox` contains $p+1$. A document containing both terms in reverse order passes Boolean AND but fails the phrase predicate. The index answers only the semantics encoded in its payloads.

### Connections

[ALGE-059](./059-dictionary-compression.md) explains compact phrase representation and access trade-offs. [ALGE-061](../ROADMAP.md#block-07--approximation-heuristics-and-randomized-algorithms) introduces approximation guarantees; search heuristics must not borrow such guarantees without proof. Data Engineering owns collection lifecycle and provenance, while Distributed Systems and Platform Engineering own replicated execution and fleet operation.

## Governing Question

Given a corpus too large or too frequently queried for repeated scanning, how do we choose and build indexes, plan exact and approximate queries, manage updates and compression, and demonstrate that observed speed has not silently changed result semantics?

The answer begins with the query contract. Token conjunction, exact phrase, arbitrary substring, edit-distance threshold, local alignment, and ranked retrieval are distinct problems. A data structure optimized for one can be incomplete, wasteful, or misleading for another.

## Why This Matters

At collection scale, asymptotic CPU time is only one cost. Index bytes compete with source bytes and caches; postings are compressed and decoded in blocks; storage reads dominate some plans; updates create multiple searchable versions; and one frequent term can turn a plausible query into a resource incident.

Text and biological sequence systems also have different representations. Human-language retrieval often tokenizes and normalizes. Genomic search retains alphabet positions and reference coordinates. Both need stable document identity, boundaries, provenance, and precise claims about exactness, ranking, or sensitivity.

An index is a materialized claim about a particular collection snapshot. If construction, metadata, or query normalization drift, a fast result can be wrong without crashing. Durable systems make those dependencies explicit and auditable.

## Prerequisites and Retrieval

Retrieve [ALGE-051](./051-naive-and-prefix-based-pattern-matching.md) through [ALGE-059](./059-dictionary-compression.md): exact matching, prefix functions, rolling hashes, suffix arrays, LCP, suffix automata, edit distance, alignment, and compressed representation. Also retrieve external-memory cost models, set intersection, probability, stable identifiers, snapshot isolation, and benchmark design.

This chapter covers index selection and query execution for large text and sequence collections. It does not teach linguistic ranking models, biological interpretation, cluster consensus, or storage-engine recovery in full; it states their interfaces and evidence boundaries.

## Learning Objectives

After completing this module, you should be able to:

1. turn a search requirement into an explicit result contract;
2. choose among inverted, positional, suffix-array, FM, and seed indexes;
3. derive postings intersection and phrase-query mechanisms;
4. preserve document boundaries in whole-collection indexes;
5. separate candidate generation from exact or heuristic verification;
6. plan conjunctions and verification work using safe statistics;
7. design immutable segments, tombstones, merges, and snapshots;
8. reason about compression, block size, cache, and I/O amplification;
9. enforce adversarial query and output budgets; and
10. evaluate latency, throughput, memory, index size, freshness, recall, and precision honestly.

## Core Exposition

### Specify the result relation first

Let collection snapshot $C=\{(id_i,S_i,m_i)\}$ contain stable identifier $id_i$, sequence $S_i$, and metadata $m_i$. A query is not just a string. It includes a query type, representation version, filters, score or distance rule, tie policy, result limit, and snapshot or freshness requirement.

For exact substring search, the result relation may be

$$
R(P,C)=\{(id_i,j):S_i[j:j+|P|]=P\}.
$$

For token search, normalization $N$ and tokenizer $T$ are part of the function. For approximate search, declare edit operations, threshold, scoring model, completeness guarantee, and how truncation is represented. “Relevant” ranked results require judgments or a domain proxy; string equality alone does not define relevance.

Stable identities matter because array offsets change under rebuilds. A stored location should identify snapshot, document, coordinate system, and strand or field when applicable. If normalization changes character counts, retain a mapping to original coordinates or admit that exact highlighting is unavailable.

### Build inverted and positional indexes

An inverted index stores a dictionary from term to sorted postings. A document-only posting supports membership and Boolean operations. A positional posting stores ordered positions within each document and supports phrase, proximity, and highlighting semantics.

To process $A\land B$, merge the sorted document lists. At each comparison, emit equal identifiers and advance both; otherwise advance the smaller. Each pointer advances at most through its list, giving $O(|P_A|+|P_B|)$ time. For many terms, begin with selective lists and preserve a common document order. Skip data, block maxima, bitmaps, or galloping searches may reduce work for skewed lengths, but their benefit is workload- and representation-dependent.

Phrase search performs a positional join. For phrase terms $t_0,ldots,t_{k-1}$, a start $p$ qualifies when the same document contains $t_i$ at $p+i$ for every $i$. Stop-word removal may therefore make exact phrase semantics impossible unless positions or an alternative structure retain the missing information.

This dependency-free example builds an immutable positional index and distinguishes conjunction from ordered adjacency.

<!-- bijux-verify: {"id":"positional-index-phrase-query","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"and_fox_jumps=('d1',)\nphrase_red_fox=(('d1', 0), ('d2', 0), ('d3', 1))\nphrase_fox_red=(('d3', 0),)\nphrase_missing=()\n","stderr":""}} -->
```python
def build_index(documents):
    index = {}
    for document_id, text in sorted(documents.items()):
        for position, term in enumerate(text.lower().split()):
            index.setdefault(term, {}).setdefault(document_id, []).append(position)
    return index


def and_query(index, terms):
    if not terms or any(term not in index for term in terms):
        return ()
    documents = set(index[terms[0]])
    for term in terms[1:]:
        documents.intersection_update(index[term])
    return tuple(sorted(documents))


def phrase_query(index, terms):
    answers = []
    for document_id in and_query(index, terms):
        later = [set(index[term][document_id]) for term in terms[1:]]
        for start in index[terms[0]][document_id]:
            if all(start + offset in positions for offset, positions in enumerate(later, 1)):
                answers.append((document_id, start))
    return tuple(answers)


index = build_index(
    {"d1": "red fox jumps", "d2": "red fox sleeps", "d3": "fox red fox"}
)
print(f"and_fox_jumps={and_query(index, ('fox', 'jumps'))}")
print(f"phrase_red_fox={phrase_query(index, ('red', 'fox'))}")
print(f"phrase_fox_red={phrase_query(index, ('fox', 'red'))}")
print(f"phrase_missing={phrase_query(index, ('blue', 'fox'))}")
```

The tokenizer is intentionally minimal and recorded in code. A production tokenizer must define Unicode decoding, normalization, case handling, language rules, invalid bytes, field boundaries, and version transitions. Changing it changes the searchable relation.

### Index arbitrary substrings

Token indexes cannot generally find arbitrary substrings. A suffix array over a text orders suffix starts; two binary searches find the interval whose suffixes begin with pattern $P$. An LCP structure accelerates related comparisons and supports other queries. A suffix tree or automaton makes other time/space trade-offs.

An FM-index stores a Burrows-Wheeler-based representation with cumulative symbol counts and rank support. Backward search refines an interval one pattern symbol at a time. Counting occurrences can be compact; locating each original position requires suffix-array samples or equivalent recovery, adding time and space.

To index multiple documents by concatenation, introduce boundary symbols or a representation that cannot create cross-document matches. One shared sentinel is insufficient if its semantics allow a pattern to cross boundaries or if suffix identity becomes ambiguous. Map every global coordinate to a stable document and local coordinate, and prohibit queries containing internal sentinels.

Compression and search can cooperate. FM-index space adapts to compressibility while supporting queries, whereas a general compressed file may require decompression from a checkpoint. Measure index plus samples, dictionaries, metadata, and source retention—not the headline structure alone.

### Retrieve candidates, then verify

Approximate search usually avoids aligning a query against every location. It selects exact or hashed seeds, retrieves candidate regions, clusters or chains them, and verifies candidates with edit distance or alignment. Each stage needs a separate claim.

A seed filter can be **lossless for a declared threshold** only if a proof covers seed selection, errors, boundaries, and candidate caps. Otherwise it is heuristic and may reduce recall. Hash matches require byte verification when collisions would violate the result contract. Bloom filters can safely reject absence only under their construction assumptions; their positive result is a candidate, not membership proof.

Verification can itself be exact, banded with a proven threshold condition, or heuristic. Return whether the search was exhaustive, truncated, timed out, or approximate. A top-$k$ interface must define tie handling; stopping after $k$ discovered candidates is not equivalent to returning the globally best $k$.

Sequence database tools illustrate the evidence boundary. The original BLAST paper describes a fast approach that approximates local-alignment objectives using word hits and extension. BWT/FM-index-based read aligners use compressed reference indexing and bounded search strategies. Their mapping result is conditional on scoring, seed, quality, repeat, and reporting policies; it is not proof of biological origin or uniqueness.

### Plan queries by expected work

Collection statistics guide planning: document frequency, postings length, term frequency, block summaries, seed frequency, and region complexity. For a conjunction, intersecting rare terms first often shrinks intermediate candidates. But statistics can be stale, adversarially skewed, or correlated; the engine needs a safe fallback and runtime caps.

Cost should approximate resource work, not just comparison count:

$$
cost(q)=\alpha B_{read}+\beta P_{decoded}+\gamma V_{candidates}+\delta O_{results},
$$

where coefficients depend on measured storage, CPU, and cache behavior. This is an engineering model, not an invariant. Validate it against traces and update it when hardware or encodings change.

Negative queries and very common terms are dangerous because their complement approaches the collection size. Apply filters in an order that preserves semantics while bounding expansion. Require a selective positive clause where policy permits, use bitmaps for dense sets when suitable, and make rejected or truncated outcomes visible.

### Construct beyond memory

When term/posting pairs exceed memory, build sorted runs or in-memory inverted blocks, write them sequentially, then multiway merge. The relevant bound counts block transfers as well as CPU work. Choose buffers so active streams fit memory, and persist checksums and length metadata for each immutable artifact.

Whole-text suffix structures likewise need construction strategies matched to RAM, storage, and parallelism. The build must preserve deterministic symbol order, sentinel policy, and coordinate mapping. Record source snapshot digest, builder version, parameters, and output digests so a query result can be traced to its indexed corpus.

Index compression changes query behavior. Gap-encoded document IDs exploit sorted postings; blocked codes permit skipping and local decoding. Larger blocks improve compression and sequential throughput but may increase bytes decoded for selective queries. Benchmark cold and warm caches, realistic concurrency, and both common and rare terms.

### Make updates snapshot-safe

Immutable segments simplify publication: build a complete segment, validate it, then atomically add it to a snapshot manifest. Queries search the set of segments visible at their chosen snapshot. Replacements and deletions use versions or tombstones until compaction removes obsolete entries.

Compaction merges segments and rewrites identifiers or offsets. Publish new data and metadata atomically, keep old files until no reader can observe them, and validate counts and digests before reclamation. A crash between file upload and manifest publication must not expose a half-built index.

Duplicates across segments require a deterministic winner, commonly highest visible version for a stable document key. This is distinct from search-score ties. Freshness metrics should measure ingestion-to-visible delay and tombstone lag, not merely segment-build duration.

### Bound and observe every query

Set limits on query bytes, tokens, wildcard expansion, automaton states, postings decoded, candidate regions, verification cells, memory, storage bytes, time, and returned locations. Cancellation must reach storage reads and verification loops. Avoid allocating directly from untrusted term, automaton, or result counts.

Expose structured outcomes: complete, no match, unsupported query, malformed query, resource limit, timeout, partial/truncated, stale snapshot, and internal failure. Cache keys include normalization/index version, filters, snapshot, permissions, result limit, and scoring parameters. Otherwise a correct cached result for one contract becomes incorrect for another.

Observability should not leak sensitive queries or sequence data. Record aggregate costs, hashed or classified features where justified, plan choice, segment versions, truncation, and latency. Apply access control before returning postings or snippets; an index can reveal that content exists even when the source object is protected.

### Evaluate quality and systems behavior together

Freeze a representative corpus snapshot, query set, relevance or truth labels, configuration, and hardware. For exact search, compare results with an independent oracle on a tractable sample and use metamorphic properties such as adding a nonmatching document. For approximate or ranked search, report recall, precision, rank metrics, and the judgment process.

Measure build throughput, peak build memory, temporary storage, final index bytes, cold/warm latency percentiles, throughput under concurrency, bytes read, postings decoded, verification work, freshness, and failure outcomes. Stratify queries by frequency, length, language/alphabet, repeat content, result cardinality, and adversarial pattern.

A mean latency can hide catastrophic tails. A speedup produced by candidate truncation can hide recall loss. Publish both systems and quality metrics with confidence intervals or run distributions where variability matters.

## Definitions and Notation

Let $D$ be the number of documents, $N=\sum_i|S_i|$ total symbols, $V$ vocabulary size, $df(t)$ document frequency of term $t$, and $P_t$ its postings list. Let $occ$ be occurrence count, $k$ requested result count, and $B$ the storage-transfer block size.

- A **posting** is an indexed occurrence record, often document ID plus positions or payloads.
- A **lexicon** maps indexed terms to postings metadata and storage locations.
- A **candidate** passes a cheap filter but not necessarily the result predicate.
- A **verifier** decides or scores the declared predicate on a candidate.
- A **tombstone** suppresses an older visible record until compaction reclaims it.
- **Write amplification** is total bytes written divided by logical bytes ingested under a named interval and scope.
- **Query amplification** is extra index/data work relative to the logically necessary result, under a stated metric.
- A **snapshot** is an immutable mapping from logical collection identity to index segments and metadata versions.

## Mechanisms, Invariants, or Proof Structure

### Proof of linear postings intersection

Maintain pointers $i,j$. If identifiers match, emit once and advance both. If $P_A[i]<P_B[j]$, that identifier cannot occur later in sorted $P_B$, so advancing $i$ cannot lose an intersection; the symmetric case advances $j$. Each step advances at least one pointer, and neither retreats, giving at most $|P_A|+|P_B|$ advances. Sortedness and a common identifier order are premises.

### Proof of positional phrase correctness

If the positional join emits $(d,p)$, each term $t_i$ occurs in document $d$ at $p+i$, so the token sequence equals the phrase: soundness. Conversely, if the phrase begins at $p$, every required positional list contains $p+i$, so document intersection retains $d$ and the positional test emits $(d,p)$: completeness. Both directions assume the indexed token stream and query use identical boundary and normalization rules.

### Snapshot invariant

A query resolves one manifest version before reading segments. Every returned posting belongs to a segment named by that manifest, and version/tombstone resolution is evaluated against the same snapshot. New segment publication changes the manifest atomically; reclamation waits until no reader can hold the old snapshot. This prevents mixed-generation results even though physical files are built and deleted asynchronously.

### Candidate-verification invariant

Every reported exact result must pass the exact predicate. A filter may discard a candidate only when a proof establishes that discarded candidates cannot satisfy the declared predicate. Caps, sampling, heuristic seeds, or timeouts that can discard true results force a partial or heuristic outcome label.

## Alternatives and Trade-Offs

| Structure or policy | Strong use | Cost or limitation | Required evidence |
|---|---|---|---|
| Document inverted index | Boolean term membership | No phrase positions | Set oracle and sorted-posting checks |
| Positional inverted index | Phrase/proximity and highlighting | Larger postings | Coordinate replay and boundary tests |
| Suffix array + LCP | Exact substring and suffix order | Source-size index and random reads | Naive substring oracle on bounded corpora |
| FM-index | Compressed substring counting/search | Rank structure and locate sampling costs | Interval and locate differential tests |
| $q$-gram/seed index | Candidate generation for approximate search | Frequent seeds and possible recall loss | Filter proof or measured recall label |
| Immutable segments | Atomic publish and simple readers | Query fan-out and compaction | Snapshot/crash/reclamation tests |
| Large compressed blocks | Better ratio and throughput | More decode for selective queries | Cold/warm workload benchmarks |
| Aggressive candidate cap | Bounded tail latency | Can reduce completeness or recall | Explicit partial status and quality curve |

## Failure Modes and Misconceptions

- **“The index searches the original text.”** It searches a versioned representation of it.
- **“AND and phrase are nearly the same.”** Document co-occurrence does not establish adjacency or order.
- **“A suffix interval is a list of answers.”** Location sampling and document mapping still matter.
- **“Separators solve boundaries automatically.”** Their alphabet, uniqueness, query exclusion, and coordinate mapping must be correct.
- **“A seed hit is an alignment.”** It is a candidate until the declared verifier runs.
- **“No seed hit proves no approximate match.”** Only a proven lossless filter supports that conclusion.
- **“Rare-first is always optimal.”** Decode format, skips, filters, correlations, and storage locality affect cost.
- **“Compaction is invisible.”** Without snapshot publication and deferred reclamation it can mix versions or lose reads.
- **“Compression only saves disk.”** It trades I/O, cache occupancy, decode CPU, and access granularity.
- **“Top ten means best ten.”** Global ranking requires a scoring and termination guarantee plus a tie rule.
- **“Exact search is objective.”** Encoding, normalization, tokenization, boundaries, and snapshot determine exactness.
- **“Benchmarking latency demonstrates relevance.”** Systems performance and result quality need separate oracles.

## Worked Examples

### Example 1

**Situation.** Sorted postings are $P_a=[1,4,7,11]$ and $P_b=[2,4,7,9,11]$.

Compare 1 with 2 and advance $P_a$; compare 4 with 2 and advance $P_b$; emit 4 and advance both; emit 7; compare 11 with 9 and advance $P_b$; emit 11. The intersection is $[4,7,11]$. Seven pointer-advance events remain within the sum of list lengths.

**Conclusion.** Monotone pointers exploit sortedness and never need to rescan a posting.

### Example 2

**Situation.** Document 9 contains `red` at positions $[2,10]$ and `fox` at $[3,8]$.

Boolean `red AND fox` returns document 9. Phrase `red fox` tests successors $[3,11]$ against fox positions; only start 2 succeeds. Phrase `fox red` tests $[4,9]$ against red positions and has no result.

**Conclusion.** Positional payloads distinguish membership, order, and adjacency.

### Example 3

**Situation.** Documents `AB` and `CD` are naively concatenated as `ABCD`; query is `BC`.

Substring search finds a match starting at global position 1, but it crosses the document boundary and is absent from both source documents. Encoding as `AB#CD$` with excluded unique sentinels, or storing explicit boundary ranges checked at locate time, rejects it.

**Conclusion.** Collection concatenation must prevent cross-document false matches.

### Example 4

**Situation.** Three conjunction terms have document frequencies 900,000, 40,000, and 120 in a one-million-document collection.

Starting with 120 and 40,000 bounds the first intermediate by 120. Starting with 900,000 and 40,000 can produce up to 40,000 candidates before the selective term is considered. Actual correlation and block costs may change the best physical plan, but syntax order is unjustified.

**Conclusion.** Safe selectivity statistics reduce intermediate work while runtime budgets handle estimation error.

### Example 5

**Situation.** An FM backward search returns interval $[120,125)$ for pattern `GATA`.

The interval proves five suffixes share that prefix under the indexed text and alphabet. To return coordinates, recover five sampled suffix-array positions, map each global position to a reference sequence and local coordinate, and reject any boundary crossing. Counting can therefore be cheaper than locating.

**Conclusion.** Search, count, locate, and document mapping are distinct operations with distinct costs.

### Example 6

**Situation.** A seed index retrieves 80 candidate regions for an edit-distance-at-most-two query; a cap allows verification of only 50.

All 50 verified hits may be correct, so precision among returned results can be high. Yet any of the 30 omitted candidates may be a true match. Unless candidate ordering plus a proof excludes them, the system must return truncated/heuristic status and cannot claim complete recall.

**Conclusion.** Verification establishes sound returned hits; candidate truncation can still destroy completeness.

### Example 7

**Situation.** An index has segments S1 with document `x` version 4, S2 with version 5, and a tombstone for version 5 in S3.

A snapshot containing all three must suppress both data versions. A snapshot containing only S1 and S2 returns version 5. Choosing one segment per term independently could mix states; version resolution applies after the query fixes one segment manifest.

**Conclusion.** Logical visibility is a snapshot rule over physical segments, not “return the newest posting encountered.”

### Example 8

**Situation.** A postings block holds 128 KiB uncompressed. Compression shrinks it to 32 KiB, but a rare-term query needs 300 bytes from it.

If the code requires whole-block decoding, the query reads 32 KiB and expands 128 KiB to inspect 300 bytes. Smaller independently decodable blocks could reduce amplification but add headers and lose compression context. Only workload measurements resolve the trade-off.

**Conclusion.** Index compression must be evaluated with access granularity, not size alone.

### Example 9

**Situation.** A wildcard expands to 200,000 terms, each with a short postings list.

Although each list is cheap, lexicon expansion, file seeks, decompression, union state, and output can exceed budgets. Check expansion incrementally, cap automaton states and postings work, cancel outstanding reads, and return an explicit resource-limit result rather than an empty set.

**Conclusion.** Adversarial query shape matters independently of result count.

### Example 10

**Situation.** A new search build is 3× faster at p50 latency but caps candidates; exact truth labels show recall fell from 0.98 to 0.81, while p99 improved only 5%.

The median speedup does not justify equivalence. Report the quality/latency curve, p95/p99, cap-hit frequency, query strata, and confidence across runs. Deployment requires a stated acceptable quality floor and tail target, not a single aggregate.

**Conclusion.** Search evaluation joins result quality with resource distributions; neither substitutes for the other.

## Cross-Program Connections

- **Algorithms:** [ALGE-055](./055-suffix-arrays-and-lcp.md), [ALGE-056](./056-suffix-trees-and-automata.md), and [ALGE-059](./059-dictionary-compression.md) supply the indexed sequence and compression mechanisms.
- **Data Structures:** owns postings layouts, bitmaps, tries, rank/select support, filters, and cache-aware representation.
- **Database Engineering:** owns access-path selection, cost estimation, snapshots, compaction, and query-result consistency.
- **Data Engineering:** owns collection snapshots, normalization lineage, backfills, deletions, and quality datasets.
- **Distributed Systems:** owns shard routing, replication, partial failure, global top-$k$, and consistency across nodes.
- **Security Engineering:** owns authorization, query abuse, sensitive-term leakage, and untrusted parser boundaries.
- **Platform Engineering:** owns capacity, rollout, observability, cancellation propagation, and index artifact distribution.

## References

1. Christopher D. Manning, Prabhakar Raghavan, and Hinrich Schütze, [*Introduction to Information Retrieval*](https://nlp.stanford.edu/IR-book/), Cambridge University Press, 2008; online edition 2009. Author-hosted text; inverted indexes, positional postings, construction, intersection, and evaluation sections checked 2026-09-05.
2. Paolo Ferragina and Giovanni Manzini, “Opportunistic Data Structures with Applications,” *41st IEEE Symposium on Foundations of Computer Science*, 390–398, 2000, [doi:10.1109/SFCS.2000.892127](https://doi.org/10.1109/SFCS.2000.892127). Primary FM-index source; bibliographic record and stated compressed-search bounds checked 2026-09-05.
3. Alok Aggarwal and Jeffrey Scott Vitter, “The Input/Output Complexity of Sorting and Related Problems,” *Communications of the ACM* 31(9), 1116–1127, 1988, [doi:10.1145/48529.48535](https://doi.org/10.1145/48529.48535). Primary external-memory model source.
4. Ricardo Baeza-Yates and Berthier Ribeiro-Neto, *Modern Information Retrieval: The Concepts and Technology behind Search*, 2nd ed., Addison-Wesley, 2011, ISBN 978-0321416919. Retrieval models, indexing, and evaluation reference.
5. Stefan F. Altschul, Warren Gish, Webb Miller, Eugene W. Myers, and David J. Lipman, “Basic Local Alignment Search Tool,” *Journal of Molecular Biology* 215(3), 403–410, 1990, [PubMed 2231712](https://pubmed.ncbi.nlm.nih.gov/2231712/), doi:10.1016/S0022-2836(05)80360-2. Primary seed-and-extension sequence-search source; NCBI record checked 2026-09-05.
6. Heng Li and Richard Durbin, “Fast and Accurate Short Read Alignment with Burrows-Wheeler Transform,” *Bioinformatics* 25(14), 1754–1760, 2009, [PubMed 19451168](https://pubmed.ncbi.nlm.nih.gov/19451168/), doi:10.1093/bioinformatics/btp324. Primary BWT-based read-alignment source; NCBI record checked 2026-09-05.
7. Gonzalo Navarro, “A Guided Tour to Approximate String Matching,” *ACM Computing Surveys* 33(1), 31–88, 2001, [doi:10.1145/375360.375365](https://doi.org/10.1145/375360.375365). Survey of exact and filtering approaches to approximate matching.
8. Dan Gusfield, *Algorithms on Strings, Trees, and Sequences*, Cambridge University Press, 1997, [doi:10.1017/CBO9780511574931](https://doi.org/10.1017/CBO9780511574931). Foundational suffix, matching, and biological sequence algorithms.

## Exercises

### Exercise 1

Define separate contracts for token conjunction, exact phrase, exact byte substring, edit-distance-at-most-two search, and ranked top-10 retrieval. Identify the representation and evidence each contract requires.

### Exercise 2

Given positional postings `a: {d1:[1,4], d2:[0]}`, `b: {d1:[2,7], d2:[1]}`, and `c: {d1:[3], d2:[4]}`, compute results for `a AND c`, phrase `a b`, and phrase `a b c`. Show the positional tests.

### Exercise 3

An exact substring service concatenates documents with byte zero, permits byte-zero queries, locates only every 64th suffix-array position, and returns global offsets. Diagnose its semantic and interface defects and propose a correct design.

### Exercise 4

Design an update architecture for 20 TB of text receiving 100 GB daily while queries require snapshot consistency and deletions visible within ten minutes. Compare immediate in-place mutation with immutable segments and compaction; state metrics and failure tests.

### Exercise 5

A protein-search system must answer within two seconds and claims complete results above a score threshold. Its seed stage may cap common seeds and its verifier may time out. Redesign the contract and algorithm so the claim is honest, or state what resources are required to retain completeness.

## Answers to the Exercises

### Answer 1

Token conjunction returns documents containing all normalized terms and needs a versioned tokenizer plus document postings. Exact phrase returns positions with adjacent ordered tokens and needs positional postings plus boundary rules. Exact byte substring returns document/local offsets whose indexed bytes equal the pattern and needs a suffix-style or equivalent exact index with encoding and sentinel rules. Edit-distance-at-most-two returns every location under declared insert/delete/substitute costs and needs a lossless filter plus exact verifier, or exhaustive evaluation. Ranked top-10 returns ten highest scores under a fixed scoring, filter, snapshot, tie, and termination rule and needs relevance judgments to assess quality. Full credit requires five distinct relations rather than one vague “search” API.

### Answer 2

`a AND c` returns both d1 and d2 because each has at least one position for both terms. For `a b`, d1 start 1 succeeds because 2 is in b; start 4 fails because 5 is absent. d2 start 0 succeeds because b contains 1, so results are `(d1,1)` and `(d2,0)`. For `a b c`, d1 start 1 succeeds because b has 2 and c has 3; d1 start 4 fails. d2 start 0 fails because c lacks 2. The sole result is `(d1,1)`.

### Answer 3

Byte zero is not an excluded sentinel if documents or queries may contain it, so matches can cross boundaries or sentinel matches can be reported. Use symbols outside the query alphabet, escape and distinguish per-document boundaries, or validate every located interval against explicit ranges. Sampling every 64th location is acceptable only if LF steps or another recovery method reconstruct every suffix position with bounded cost; otherwise results are incomplete. Global offsets are unstable and ambiguous, so return snapshot ID, stable document ID, and local byte coordinate. Specify whether patterns containing boundary symbols are rejected and verify every returned substring against original bytes.

### Answer 4

In-place mutation reduces segment fan-out but makes atomic publication, reader isolation, crash recovery, and rollback difficult at this scale. Prefer frequent immutable delta segments published through an atomic snapshot manifest, versioned tombstones visible within ten minutes, and background leveled or size-tiered compaction. Resolve duplicate keys and tombstones against the fixed query snapshot; defer deletion until old readers finish. Measure ingest-to-visible lag, segment count, query fan-out, compaction write amplification, temporary space, peak memory, latency tails, and tombstone age. Test crashes before and after manifest publication, retry idempotence, concurrent readers, duplicate versions, delete/reinsert, corrupt segments, and reclamation safety.

### Answer 5

The current system cannot promise completeness because either cap or timeout can discard a true hit. One honest contract returns verified hits plus `complete=false`, truncation reason, examined candidate count, snapshot, scoring model, and resource budget; evaluate recall against an exhaustive oracle sample. To retain completeness, derive a seed scheme proven lossless for the score threshold, remove lossy caps, reserve enough time/memory to enumerate and exactly verify every candidate, and return a resource error rather than a partial set when the bound cannot be met. A hybrid may offer a strict asynchronous endpoint and a two-second heuristic endpoint, but their guarantees and result types must differ.
