---
module_id: DSE-094
program: Data Structures Engineering
level: 2
module_number: 94
title: Compressed Suffix Arrays
status: complete
last_verified: 2026-08-30
---

# Compressed Suffix Arrays

## One-Page Review

### Governing question

How can a suffix array's text-order permutation and pattern-search functionality be represented near text-compressed space while preserving locate, extract, and suffix-order semantics under explicit sampling and alphabet contracts?

### Essential definitions

Let text (T[0..n)) end in a unique sentinel `$` that is lexicographically smaller than every other symbol and occurs nowhere else. The suffix array (SA[i]) is the start position of the (i)-th lexicographically smallest suffix; inverse suffix array (ISA[p]) is its rank, so (ISA[SA[i]]=i).

For the cyclic sentinel model,

$$
\Psi(i)=ISA[(SA[i]+1)\bmod n],
\qquad
LF(i)=ISA[(SA[i]-1)\bmod n].
$$

(Psi) advances one text position and (LF) moves backward; they are inverses. The Burrows–Wheeler transform is (BWT[i]=T[(SA[i]-1)\bmod n]). Compressed suffix arrays (CSA) are a family of representations using compressible structure in (Psi), BWT, alphabets, and sampled (SA/ISA), rather than storing every (SA) value in (lceil\log_2n\rceil) bits.

### Central model, mechanism, or theorem

Suffixes beginning with the same character occupy a contiguous SA interval, and within such groups (Psi) has structured/monotone behavior exploited by CSA encodings. A sampled SA stores selected ranks or text positions. To locate an unsampled rank (i), follow (Psi) until a sampled rank (j); if (d) advances occurred, (SA[i]=(SA[j]-d)\bmod n). Sampling density trades space for locate time.

FM-indexes represent BWT with rank support and use backward (LF)-style interval updates; Sadakane/Grossi–Vitter CSAs often foreground (Psi). These are related compressed self-index families, not synonyms for one concrete layout. Count, locate, extract, suffix-array access, and inverse access have distinct structures and bounds.

### Critical invariants

- Text normalization, symbol encoding/order, sentinel identity, and (n) are immutable metadata.
- `$` occurs exactly once and compares below all live symbols; suffixes and cyclic formulas use the declared model.
- (SA) and (ISA) are inverse permutations of (0..n-1).
- (Psi) and (LF) are inverse permutations and advance/retreat the corresponding text position.
- BWT, cumulative alphabet counts, rank supports, samples, and text generation agree.
- A locate walk reaches a compatible sample within its documented bound; modular reconstruction handles the sentinel.
- Pattern intervals are half-open and all reported positions are verified under original-text semantics.
- Serialized sections, sampling strategies, alphabets, dictionaries, and checksums publish atomically.

### Common failures

Failures include omitting or duplicating the sentinel, ordering the sentinel incorrectly, sorting suffix bytes under a different normalization, confusing suffix rank with text position, using noncyclic formulas at sentinel boundaries, assuming any periodic rank sampling bounds a (Psi) walk, mixing SA-order and text-order samples, treating count as locate, reporting a BWT interval without document/text coordinates, accepting padding/corrupt rank supports, measuring only final index and not construction peak, and calling a plain bit-packed SA “compressed” relative to text entropy.

### Compact example

For `banana$`, (SA=[6,5,3,1,0,4,2]), (ISA=[4,3,6,2,5,1,0]), (Psi=[4,0,5,6,3,1,2]), (LF=[1,5,6,4,0,2,3]), and BWT is `annb$aa`. Sampling even SA ranks gives `{0:6,2:3,4:0,6:2}`. Repeated (Psi) reconstructs every SA value; pattern `ana` occupies interval `[2,4)` and locates positions `[1,3]`, matching a direct oracle.

### Connections

[DSE-092](092-wavelet-trees.md) supplies compressed BWT rank/access, and [DSE-093](093-succinct-trees-and-graphs.md) supplies compressed suffix-tree topology. The roadmap successor is [DSE-095, “Dynamic Fenwick and Segment Structures”](../ROADMAP.md). Information Retrieval, Bioinformatics, Databases, Compression, and Storage Engineering own normalization, multi-document sentinels, construction, persistence, and query workloads.

## Governing Question

How should a CSA define its text model, permutation functions, compressed representation, sampling, pattern operations, construction, serialization, and validation so its space/time claims and located occurrences are reproducible?

## Why This Matters

A plain suffix array stores (n) integers, usually (Theta(n\log n)) bits, in addition to text. It supports binary-search pattern intervals and is cache-friendly, but its memory can dominate large corpora. A compressed full-text index exploits the suffix permutation's relationship to the text, potentially replacing both raw SA and text while supporting search and extraction.

The difficulty is compositional. An index can count correctly but locate incorrectly because samples mismatch; it can locate but decode symbols under a stale alphabet; it can serialize a valid BWT with a corrupt rank directory. Exact identities and a plain oracle are therefore first-class production evidence.

## Prerequisites and Retrieval

Retrieve:

- suffixes, lexicographic order, suffix arrays, inverse permutations, binary search, LCP, and unique sentinels;
- BWT, stable sorting, cumulative symbol counts, LF mapping, (Psi), and modular text positions;
- [wavelet-tree rank/access](092-wavelet-trees.md), compressed bit vectors, entropy, run length, and sampling;
- half-open intervals, count/locate/extract APIs, Unicode/byte normalization, and multi-document boundaries;
- immutable generations, mapped sections, checked arithmetic, construction peak, checksums, and differential tests.

The chapter uses suffixes of the terminated text for searching, but (Psi/LF) formulas wrap cyclically through the unique sentinel. Mixing terminated and cyclic interpretations without stating the boundary rule is incorrect.

## Learning Objectives

After this chapter, you should be able to:

1. derive (SA), (ISA), BWT, (Psi), and (LF) and verify their inverse identities;
2. explain how structured (Psi) or BWT rank supports a CSA/self-index;
3. design SA/ISA sampling and derive locate/extract walks and their bounds;
4. distinguish count, locate, extract, SA access, inverse access, LCP, CSA, and FM-index capabilities;
5. specify sentinel, alphabet, normalization, multi-document, construction, and persistence invariants;
6. detect mismatched generations/samples, corrupt intervals, adversarial walks, and misleading space results;
7. validate against plain suffix/text oracles and benchmark full space/time/build curves.

## Core Exposition

### Suffix array and inverse

For each (p\in[0,n)), suffix (T[p..n)) participates exactly once. Sorting these suffixes yields permutation (SA); assigning ranks yields inverse (ISA). Pattern (P) matches a contiguous SA interval because all strings with prefix (P) are contiguous lexicographically. Two boundary searches find lower/upper suffixes; locating reads SA values in the interval.

The unique sentinel makes every suffix distinct, defines a single smallest suffix, and makes rotations/BWT invertible. For byte indexes reserve a byte not present or remap alphabet to an integer domain. For multiple documents, use distinct logical terminators or a collection construction that prevents matches crossing boundaries and maps global positions back to documents.

Plain SA access is direct; compression introduces navigation/sample work. Plain text may be retained for verification or extraction, but a *self-index* can reproduce text and may replace it. State which object is authoritative and whether positions count bytes, code points, tokens, or normalized symbols.

### Psi and LF identities

If rank (i) names suffix starting at (p=SA[i]), (Psi(i)) names suffix at (p+1\bmod n). Therefore repeated (Psi) walks forward through text positions in suffix-rank space. (LF) names (p-1\bmod n); each is the other's inverse:

$$
LF(\Psi(i))=i=\Psi(LF(i)).
$$

BWT stores the character preceding each suffix. LF can be computed from BWT using (C[c]), the count of symbols smaller than (c), and occurrence rank of (c=BWT[i]). Convention details decide whether rank includes position (i); with half-open rank use (LF(i)=C[c]+\operatorname{rank}_c(BWT,i)).

(Psi) can be derived from the first column/symbol groups and select over BWT. CSA families compress (Psi)'s increasing runs or differences within character groups; FM families compress BWT and rank. Both exploit text regularity through different primary interfaces.

### Sampling and locating

Storing one SA value every (s) *ranks* does not automatically bound distance along the (Psi) permutation by (s); the fixture's walk happens to reach even-rank samples, but arbitrary rank sampling needs analyzed coverage. A common strategy samples by text position modulo (s): when a walk reaches a suffix whose text position is sampled, at most (s-1) forward/backward text steps are required. The support must recognize sampled ranks and map them to values.

If (Psi^d(i)=j) and (SA[j]) is known, then (SA[i]=(SA[j]-d)\bmod n). With LF steps, signs reverse accordingly. ISA samples support inverse access/extraction by anchoring text positions to suffix ranks. Sample identifiers, density, direction, and order must be persisted with the compressed function.

Larger sampling intervals reduce sample space and increase locate/extract work. Count may not need SA samples at all. A product should tune sampling against occurrence distributions: a frequent pattern can make locate output dominate even if count is fast.

### Pattern search and counting

A CSA may search with ordinary suffix comparisons or expose BWT backward search. Ordinary search performs two binary searches over suffix order. If the original text is absent, each comparison must obtain characters through the compressed index, so the advertised search bound must include that access cost. Prefix comparison also needs an explicit end-of-text rule; the sentinel is an index symbol, not an ordinary pattern symbol.

Backward search starts with interval ([0,n)) and consumes (P) right to left. For next symbol (c), it maps ([l,r)) to

$$
[C[c]+\operatorname{rank}_c(BWT,l),\ C[c]+\operatorname{rank}_c(BWT,r)).
$$

The interval is empty exactly when its endpoints meet. Otherwise its length is the occurrence count. Each row represents one matching suffix, but converting rows into original positions is a separate locate operation. A production API should therefore return a typed interval or count, not an unlabelled pair that callers may mistake for positions.

Differential validation constructs a plain suffix array from the exact indexed symbol stream. For each test pattern, it compares lower/upper bounds, backward-search intervals, counts, and sorted located positions. Include absent patterns, the empty pattern under a documented policy, repeated symbols, prefixes reaching the sentinel, and symbols outside the alphabet. Random tests are useful only after deterministic boundary fixtures pass.

### Extraction and inverse access

Extraction asks for original symbols over a text interval, while inverse access asks for (ISA[p]), the suffix rank beginning at position (p). A structure with sampled ISA can start from a nearby text position and navigate with (Psi) or LF; a BWT self-index can recover text by following LF from the sentinel row. These are related operations, not identical complexity guarantees.

Specify whether extraction can cross a document terminator, whether it returns normalized index symbols or source bytes, and how it reports an out-of-range interval. If source offsets must survive normalization, store a separately versioned mapping. Reconstructing normalized text does not magically recover discarded capitalization, Unicode composition, or token boundaries.

### Where compression comes from

Within suffixes sharing the same first symbol, (Psi) values occur in increasing order. CSA encodings exploit these monotone subsequences using gaps, runs, or succinct predecessor/select structures. FM-style indexes instead exploit the compressibility of BWT and supply rank, often with wavelet trees or run-length structures. High-order entropy and repetitive-text bounds require specific encodings and models; they do not follow from bit-packing permutation integers.

Report all owned space: compressed navigation, rank/select supports, samples, alphabet dictionaries, cumulative counts, document maps, offset maps, LCP data, checksums, allocator overhead, and retained text. Bits per input symbol should state whether (n) includes sentinels and whether the denominator is raw bytes or normalized symbols. Compare at equal functionality: an index supporting locate and extract is not fairly compared with a counter-only structure.

### Construction, persistence, and recovery

Index construction may consume substantially more memory than the finished index. The build specification names suffix-array/BWT construction algorithm, input mutability, temporary storage, parallelism, peak resident memory, external-memory traffic, and reproducibility controls. Collection ingestion freezes document order, normalization, symbol remapping, and terminator policy before building any dependent component.

A persisted generation should bind text-model metadata, alphabet map, (n), sentinel row, compressed (Psi) or BWT, rank/select directories, (C), SA/ISA samples, document map, and checksums. Each section has a length and version; readers use checked arithmetic before mapping offsets. Publication writes a complete generation, validates it, then atomically advances a small manifest or pointer. Recovery ignores incomplete generations rather than assembling sections from different builds.

Loading validates permutation-dependent identities on deterministic probes, sample ranges and uniqueness, monotone offsets, padding bits, alphabet cardinality, and sentinel count. Full permutation verification can be expensive, so build-time evidence should record exhaustive checks while load-time probes defend against corruption. A checksum detects accidental damage; it is not a substitute for semantic invariants or an authenticity mechanism.

### Evaluation and operational boundaries

Benchmark count, locate, extract, SA access, and construction separately. Workloads should include absent and frequent patterns, long common prefixes, low-entropy runs, high-entropy inputs, repetitive version collections, Unicode normalization cases, small inputs, and near-limit sizes. Report latency distributions, throughput, bytes read, peak construction space, final owned space, sample density, and output cardinality.

Adversarial callers can request a pattern with millions of matches or repeated small extractions that maximize sample walks. APIs need result caps, pagination or iterators, cancellation, checked allocation, and work accounting. Parsing untrusted serialized indexes also requires bounded sections and validation before dereference. A CSA is an indexing structure, not an access-control boundary: located substrings can reveal sensitive text even when raw source files were deleted.

The following executable model is deliberately finite. It constructs all suffixes directly, so it proves the stated identities and fixture behavior but makes no compression or scalable-construction claim.

<!-- bijux-verify: {"id":"compressed-suffix-array-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"text=banana$\nlength=7\nsuffix_array=[6, 5, 3, 1, 0, 4, 2]\ninverse_suffix_array=[4, 3, 6, 2, 5, 1, 0]\npsi=[4, 0, 5, 6, 3, 1, 2]\nlf=[1, 5, 6, 4, 0, 2, 3]\nbwt=annb$aa\npsi_lf_inverse=True\nsample_stride=2\nsamples={0: 6, 2: 3, 4: 0, 6: 2}\nlocated=[6, 5, 3, 1, 0, 4, 2]\nlocate_matches=True\npattern=ana\ninterval=(2, 4)\noccurrences=[1, 3]\noracle=[1, 3]\nvalid=True\nevidence=bounded_compressed_suffix_array_model\n","stderr":""}} -->
```python
TEXT = "banana$"
PATTERN = "ana"
STRIDE = 2

n = len(TEXT)
sa = sorted(range(n), key=lambda position: TEXT[position:])
isa = [0] * n
for rank, position in enumerate(sa):
    isa[position] = rank

psi = [isa[(position + 1) % n] for position in sa]
lf = [isa[(position - 1) % n] for position in sa]
bwt = "".join(TEXT[(position - 1) % n] for position in sa)
inverse = all(psi[lf[rank]] == rank and lf[psi[rank]] == rank for rank in range(n))

samples = {rank: sa[rank] for rank in range(0, n, STRIDE)}
located = []
for start in range(n):
    rank = start
    distance = 0
    while rank not in samples:
        rank = psi[rank]
        distance += 1
        assert distance <= n
    located.append((samples[rank] - distance) % n)

matching_ranks = [
    rank for rank, position in enumerate(sa)
    if TEXT[position:].startswith(PATTERN)
]
interval = (min(matching_ranks), max(matching_ranks) + 1)
occurrences = sorted(sa[rank] for rank in range(*interval))
oracle = [
    position for position in range(n)
    if TEXT.startswith(PATTERN, position)
]

print(f"text={TEXT}")
print(f"length={n}")
print(f"suffix_array={sa}")
print(f"inverse_suffix_array={isa}")
print(f"psi={psi}")
print(f"lf={lf}")
print(f"bwt={bwt}")
print(f"psi_lf_inverse={inverse}")
print(f"sample_stride={STRIDE}")
print(f"samples={samples}")
print(f"located={located}")
print(f"locate_matches={located == sa}")
print(f"pattern={PATTERN}")
print(f"interval={interval}")
print(f"occurrences={occurrences}")
print(f"oracle={oracle}")
print(f"valid={inverse and located == sa and occurrences == oracle}")
print("evidence=bounded_compressed_suffix_array_model")
```

The model's even-rank samples are fixture evidence only. Its bounded loop detects a sample-free cycle but does not establish a stride-derived bound for arbitrary texts. A production implementation should test its documented sampling construction across exhaustive small permutations and adversarial repetitive texts.

## Definitions and Notation

- (T) is the normalized symbol sequence ending in one unique smallest sentinel; (n=|T|).
- (SA[i]) is the starting text position of the suffix with lexicographic rank (i); (ISA) is its inverse.
- (Psi(i)=ISA[(SA[i]+1)\bmod n]) advances one text position in suffix-rank space.
- (LF(i)=ISA[(SA[i]-1)\bmod n]) retreats one text position and is inverse to (Psi).
- (BWT[i]=T[(SA[i]-1)\bmod n]) is the preceding symbol for suffix-array row (i).
- (C[c]) counts indexed symbols strictly smaller than (c); (rank_c(BWT,i)) counts (c) in (BWT[0..i)).
- A suffix-array interval ([l,r)) contains exactly the suffix ranks matching a pattern; its count is (r-l).
- **Locate** maps matching ranks to original text positions; **extract** reconstructs an indexed text range.
- A **sample** stores selected SA or ISA values plus a support mapping navigated ranks/positions to stored values.
- A **self-index** supports pattern search and text reconstruction without retaining a separate indexed-text copy.
- A **generation** is one immutable, mutually consistent set of index sections and text-model metadata.

## Mechanisms, Invariants, or Proof Structure

### Permutation identities

Because SA is a permutation, ISA exists and (ISA[SA[i]]=i). Substituting definitions gives (LF(Psi(i))=ISA[((SA[i]+1)-1)\bmod n]=i); the symmetric substitution proves (Psi(LF(i))=i). Exhaustive validation checks every row at build time, not merely a few successful queries.

### Sample-based reconstruction

If (Psi^d(i)=j), each step advances the represented text position once, so (SA[j]=(SA[i]+d)\bmod n). Rearranging yields (SA[i]=(SA[j]-d)\bmod n). A termination bound needs a sampling-set proof: sampling positions congruent to zero modulo (s) ensures a forward text walk reaches one in at most (s-1) steps; sampling arbitrary suffix ranks does not.

### Backward-search correctness

All rows beginning with (c) form the first-column block starting at (C[c]). Stable correspondence between first and last columns preserves the relative order of equal (c) symbols. Ranks at (l) and (r) select exactly those (c)-preceded rows whose remaining suffix lies in the old interval, establishing the update formula and interval count.

### Evidence ladder

The model recomputes arrays independently from sorted suffix strings, checks every inverse identity, compares located values with SA, and compares pattern positions with a direct oracle. Production evidence adds exhaustive small texts, property tests, reference implementations, corrupted-image tests, deterministic rebuilds, and measured space/time curves. None of these alone proves a stated entropy bound; that claim requires a reviewed derivation for the exact representation.

## Alternatives and Trade-Offs

**Plain suffix array plus text.** Direct SA access, simple construction choices, excellent scan locality, and straightforward differential testing make this a strong baseline. Space remains linear in integer words plus text; long-prefix comparisons can be expensive without LCP acceleration.

**Suffix tree or compressed suffix tree.** A suffix tree makes branching and many locus operations explicit. Succinct topology plus CSA navigation can compress it, but implementation, constants, and persistence become more complex. Choose it when tree operations are actual requirements, not because it is theoretically general.

**FM-index.** The FM-index centers BWT rank and backward search. It often offers a clearer count path and uses SA samples for locate. A CSA centered on compressed (Psi) can provide natural suffix-array navigation. Implementations frequently combine ideas, so capability and measured representation matter more than labels.

**Run-length indexes and r-indexes.** Highly repetitive collections can be better described by BWT run count than by empirical entropy alone. Run-length indexes can dominate versioned-document workloads, but their construction, locate supports, and worst cases require separate evaluation.

**Inverted indexes.** Token-level retrieval, ranking, field constraints, and document updates usually favor inverted indexes. They do not replace exact arbitrary-substring search. Systems may maintain both, accepting duplicate ingestion and consistency costs.

**Suffix automata, suffix-array variants, and hashes.** Suffix automata recognize substrings and support occurrence aggregates with different position trade-offs. Enhanced suffix arrays add LCP/RMQ functionality. Rolling hashes accelerate candidate comparison but need collision handling and are not a full ordered suffix index.

**Retained versus self-indexed text.** Retaining source text can make extraction and verification simpler and may be cheaper operationally than aggressive compression. A self-index is valuable when index navigation also reconstructs text, but the space claim must include any source-offset or document metadata still required by the product.

## Failure Modes and Misconceptions

1. **Sentinel ambiguity:** a missing, repeated, or nonminimal sentinel invalidates cyclic identities and inversion assumptions.
2. **Coordinate confusion:** suffix rank, normalized text position, source-byte offset, and document-local position are returned as if interchangeable.
3. **Rank convention drift:** an inclusive BWT rank implementation is used with a half-open LF formula, producing off-by-one navigation.
4. **Direction error:** a (Psi) walk adds distance when reconstructing the earlier SA value, or an LF walk applies the opposite sign.
5. **Unproved sample bound:** periodic suffix ranks are assumed to guarantee a stride-length permutation walk.
6. **Count/locate conflation:** interval length is correct but rows are exposed as source positions without SA reconstruction.
7. **Generation mixing:** compressed navigation, samples, alphabet, or document maps come from different builds.
8. **Normalization mismatch:** queries and construction use different case folding, Unicode normalization, tokenization, or byte order.
9. **Boundary leakage:** collection search admits matches spanning logical document terminators.
10. **Space undercounting:** samples, supports, dictionaries, retained text, temporary build space, or allocator overhead are omitted.
11. **Compression overclaim:** bit-packed integers or one favorable corpus are presented as a general entropy-bounded index.
12. **Construction blindness:** the final structure fits memory, but peak construction space fails on production input.
13. **Output explosion:** fast counting hides an unbounded locate response for a frequent pattern.
14. **Unsafe deserialization:** unchecked offsets, products, or sample values reach mapped memory before validation.
15. **Checksum overtrust:** byte integrity is treated as proof of semantic consistency or authenticity.
16. **Fixture overgeneralization:** the model's even-rank sample reachability is claimed as a theorem for arbitrary texts.

## Worked Examples

### Example 1

Sort suffixes of `banana$`: `$` at 6, `a$` at 5, `ana$` at 3, `anana$` at 1, `banana$` at 0, `na$` at 4, and `nana$` at 2. Thus (SA=[6,5,3,1,0,4,2]). The ordering makes every `ana`-prefixed suffix contiguous.

### Example 2

Invert Example 1 by writing each rank at its text position. Positions 0 through 6 have ranks ([4,3,6,2,5,1,0]), so (ISA=[4,3,6,2,5,1,0]). Both compositions, (SA[ISA[p]]=p) and (ISA[SA[i]]=i), hold for all seven entries.

### Example 3

For row 0, (SA[0]=6); advancing cyclically reaches position 0, whose rank is 4, so (Psi(0)=4). Retreating from position 6 reaches 5, whose rank is 1, so (LF(0)=1). Repeating gives (Psi=[4,0,5,6,3,1,2]) and (LF=[1,5,6,4,0,2,3]); the arrays are inverse permutations.

### Example 4

Preceding each suffix start cyclically yields characters `a n n b $ a a`, hence BWT `annb$aa`. Its single sentinel is at row 4 because that row's suffix begins at text position 0 and is preceded cyclically by the terminal symbol.

### Example 5

Suppose even suffix ranks store `{0:6,2:3,4:0,6:2}`. To locate row 3, follow (Psi(3)=6), where sample value is 2. Since one forward step was taken, reconstruct (SA[3]=(2-1)\bmod7=1). The subtraction direction follows from (Psi) advancing text positions.

### Example 6

For pattern `ana`, lower/upper suffix boundaries are rows 2 and 4. Interval ([2,4)) has count 2. Locating rows 2 and 3 returns positions 3 and 1; sorting source positions produces ([1,3]), equal to direct substring scanning.

### Example 7

A service answers `count("a")=3` from an interval of length three without reading SA samples. A request for all positions must locate three rows and may take three sample walks. For a million matches, output and navigation dominate even when backward search took only a few rank operations.

### Example 8

Indexing two documents as if their concatenation were ordinary text can find a pattern whose prefix is at the end of document one and suffix at the start of document two. Logical terminators and a result filter prevent that false match. The global-to-document map must be built from the same normalized generation.

### Example 9

With stride four, sampling suffix ranks 0, 4, 8, and so on says nothing about their arrangement along the (Psi) cycle. The next sampled rank might be many steps away. Sampling suffixes whose *text positions* are multiples of four guarantees a forward text walk reaches a sampled position in at most three steps.

### Example 10

A crash occurs after writing new compressed navigation but before new samples. If readers discover sections by filename, they may combine generations and return plausible wrong positions. Publishing immutable, checksummed sections behind one atomically replaced generation manifest makes the incomplete build unreachable.

## Cross-Program Connections

- **Algorithms:** lexicographic search, permutations, predecessor/rank/select, entropy, and construction bounds supply the formal basis.
- **Information Retrieval:** query normalization, result enumeration, collection boundaries, and ranking determine whether exact substring indexing is appropriate.
- **Database Engineering:** immutable generations, mapped layouts, checksums, atomic publication, and recovery turn an index into a durable storage component.
- **Data Engineering:** deterministic ingestion and offset lineage keep batch rebuilds and source mappings reproducible.
- **Bioinformatics:** long repetitive sequences and exact-pattern workloads motivate compressed and run-length indexes, while ambiguous alphabets require explicit modeling.
- **Security Engineering:** bounded parsing, cancellation, response caps, and sensitive-substring policy constrain untrusted queries and index images.
- **Performance Engineering:** cache behavior, sample density, output cardinality, construction peak, and full owned space decide the useful operating point.

## References

1. Roberto Grossi and Jeffrey Scott Vitter, [“Compressed Suffix Arrays and Suffix Trees with Applications to Text Indexing and String Matching”](https://pages.di.unipi.it/grossi/PAPERS/sicomp05.pdf), *SIAM Journal on Computing*, 2005. Primary paper for compressed suffix arrays and suffix trees.
2. Paolo Ferragina and Giovanni Manzini, [“Opportunistic Data Structures with Applications”](https://pages.di.unipi.it/ferragina/Libraries/fmindex/FM-pages/Abs_focs00.html), *FOCS*, 2000. Author-maintained page for the primary FM-index paper connecting BWT compression and full-text search.
3. Veli Mäkinen and Gonzalo Navarro, [“Compressed Full-Text Indexes”](https://www.cs.helsinki.fi/u/vmakinen/papers/nm06acmcompsurv.pdf), *ACM Computing Surveys*, 2007. Technical survey of CSA/FM representations and operations.
4. Roberto Grossi, Ankur Gupta, and Jeffrey Scott Vitter, [“High-Order Entropy-Compressed Text Indexes”](https://pages.di.unipi.it/grossi/PAPERS/sodaconf03FINAL-LATEST.pdf), *SODA*, 2003. Primary source for high-order compressed-index bounds.
5. Simon Gog, [SDSL `csa_wt` implementation](https://github.com/simongog/sdsl-lite/blob/master/include/sdsl/csa_wt.hpp), Succinct Data Structure Library. Official implementation evidence for a wavelet-tree-backed compressed suffix array.
6. Simon Gog et al., [Succinct Data Structure Library](https://github.com/simongog/sdsl-lite), official repository. Implementation and benchmark context for succinct text indexes.
7. Gonzalo Navarro, [*Compact Data Structures: A Practical Approach*](https://users.dcc.uchile.cl/~gnavarro/CDSbook/), Cambridge University Press companion page, 2016. Author-maintained material covering compressed text indexes and supporting structures.

## Exercises

### Exercise 1

For (T=`aba$`), compute SA, ISA, (Psi), LF, and BWT. Verify both permutation inverse identities and identify the suffix-array interval and source positions for pattern `a`.

### Exercise 2

Prove the sample reconstruction formula for a (Psi) walk. Then explain why sampling every (s)th suffix-array rank does not imply an (s-1)-step bound, while sampling suffixes whose text positions are multiples of (s) does.

### Exercise 3

Using BWT `annb$aa` for `banana$`, define (C) and half-open rank precisely. Execute backward search for `ana`, showing the interval after consuming `a`, `n`, and `a`. State the count and located source positions.

### Exercise 4

Design a persisted CSA generation for a normalized multi-document collection. Name the sections, invariants, publication protocol, corruption checks, and recovery behavior needed to prevent cross-document matches and mixed generations.

### Exercise 5

Design an evaluation that chooses between a plain suffix array, a wavelet-tree CSA/FM-index, and a run-length index for a versioned source-code corpus. Define datasets, operations, baselines, space accounting, correctness oracles, and decision criteria.

## Answers to the Exercises

### Answer 1

The sorted suffixes are `$` at 3, `a$` at 2, `aba$` at 0, and `ba$` at 1, so (SA=[3,2,0,1]). Inverting gives (ISA=[2,3,1,0]). Advancing starts cyclically gives (Psi=[2,0,3,1]); retreating gives (LF=[1,3,0,2]). They are inverses entry by entry. Preceding characters are `a`, `b`, `$`, `a`, so BWT is `ab$a`. Pattern `a` occupies ([1,3)) and locates positions ([2,0]), or ([0,2]) in source order.

### Answer 2

Each (Psi) step increments the represented position modulo (n). Thus if (Psi^d(i)=j), then (SA[j]=(SA[i]+d)\bmod n), and rearrangement gives (SA[i]=(SA[j]-d)\bmod n). Suffix rank is unrelated to position along the (Psi) cycle, so ranks congruent modulo (s) can be arbitrarily far apart on that cycle. If samples instead satisfy (SA[j]\equiv0\pmod s), each forward step increments the position residue; one of the next (s) residues is zero, giving at most (s-1) steps, with the sentinel wrap handled modulo (n) under the documented sampling convention.

### Answer 3

Alphabet order is `$ < a < b < n`, so counts before each symbol are (C[$]=0), (C[a]=1), (C[b]=4), and (C[n]=5). Define (rank_c(BWT,i)) over positions ([0,i)). Start ([0,7)). Consuming final `a` yields ([1,4)); consuming `n` yields ([5,7)); consuming leading `a` yields ([2,4)). The count is 2. Locating those rows gives positions 3 and 1, sorted as ([1,3]). Every endpoint follows the same half-open convention.

### Answer 4

Freeze collection identifier, ordered document table, normalization/version, alphabet remap, distinct logical boundary policy, (n), and coordinate semantics. Store section descriptors and checksums for compressed (Psi) or BWT, rank/select support, (C), sentinel metadata, SA/ISA samples, document boundaries, normalized-to-source offsets, and optional LCP data. Validate lengths with checked arithmetic, sentinel uniqueness, sample ranges, monotone document offsets, padding, checksums, and deterministic navigation probes. Build an immutable generation, validate it fully, then atomically replace a small manifest pointer. Readers open only sections named by one manifest; recovery ignores an incomplete generation. Search rejects or filters any interval occurrence whose span crosses a logical boundary.

### Answer 5

Use exact normalized production samples plus synthetic high-entropy, long-common-prefix, and increasingly repetitive version collections. Measure count for absent/common patterns, bounded and full locate, short/long extract, SA access if required, build time, peak resident and temporary space, final total owned bytes, latency distributions, and bytes touched. Compare all results with a plain suffix-array/direct-scan oracle and test serialization corruption and deterministic rebuilds. The plain SA wins when simplicity and direct access fit memory; CSA/FM wins when broad text compression and balanced operations reduce total cost; a run-length index wins when BWT runs remain small and repetitive-workload locate performance satisfies the service limit. Choose from Pareto curves under explicit memory, p99 latency, build-window, and functionality constraints rather than from compressed size alone.
