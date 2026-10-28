---
module_id: DSE-047
program: Data Structures Engineering
level: 1
module_number: 47
title: Suffix Arrays
status: complete
last_verified: 2026-08-30
---

# Suffix Arrays

## One-Page Review

### Governing question

How can all suffixes of one encoded text be represented by a sorted position array that supports verified substring search, LCP analytics, compact persistence, and production-scale construction?

### Essential definitions

- For text `T` of length `n`, suffix `T[i..n)` begins at position `i`.
- A **suffix array** `SA[0..n)` is a permutation of positions `0..n-1` such that suffixes `T[SA[r]..)` are in increasing lexicographic order.
- The **inverse suffix array/rank** satisfies `rank[SA[r]]=r`.
- The **LCP array** stores longest-common-prefix lengths of adjacent sorted suffixes; this module uses `LCP[0]=0` and `LCP[r]=lcp(SA[r-1],SA[r])` for `r>0`.
- A **sentinel** is a unique symbol ordered below every text symbol and normally appended once.
- A **prefix-doubling construction** repeatedly sorts suffixes by rank pairs for prefixes of length `2^k`.
- **induced sorting** classifies suffixes and derives order from selected suffixes, enabling linear-time families such as SA-IS under stated models.
- A **search interval** `[lo,hi)` is the contiguous suffix-array range whose suffixes begin with a pattern.
- The **Burrows–Wheeler transform (BWT)** lists the character preceding each suffix/rotation in suffix order with a unique sentinel.
- A **longest repeated substring** corresponds to a maximum adjacent LCP value.

### Central model, mechanism, or theorem

Suffix-array correctness is a permutation plus order contract: every valid start appears exactly once, and adjacent suffixes compare strictly increasingly when the full suffixes are distinct. A unique sentinel makes every suffix distinct, bounds comparisons, and simplifies cyclic/BWT relationships; its encoded order must be explicit.

Pattern search compares a pattern `P` with suffixes and finds the first suffix not less than `P` and the first suffix greater than all strings having prefix `P`. Matching suffixes are contiguous because lexicographic order groups a common prefix. Straight binary search takes `O(|P| log n)` symbol comparisons; LCP-aware search can reuse matched prefixes for stronger bounds, but implementation and preprocessing matter.

Kasai's LCP algorithm uses inverse ranks. When scanning text positions from left to right, if suffix `i` shares prefix length `h` with its lexicographic predecessor, suffix `i+1` shares at least `h-1` symbols with the appropriate neighboring suffix before extension. Since `h` increases at most `n` total beyond decrements, LCP construction is `O(n)` after SA/rank.

For a length-`n` text without sentinel in substring counts, there are `n(n+1)/2` substring occurrences. Suffix `SA[r]` contributes `n-SA[r]` prefixes, of which `LCP[r]` were already prefixes of the preceding suffix. Therefore distinct substrings equal `n(n+1)/2 - sum(LCP)`.

### Critical invariants

1. Text alphabet, encoding unit, normalization, sentinel identity/order, and index-width convention are explicit and immutable for an index generation.
2. `SA` length is `n`, every entry is in `0..n-1`, and entries form a permutation.
3. Adjacent suffixes in `SA` are strictly lexicographically ordered under the declared symbol order.
4. `rank` is the exact inverse permutation.
5. `LCP[0]=0`; for `r>0`, `0<=LCP[r]<=min(n-SA[r-1],n-SA[r])` and symbols/mismatch boundaries agree.
6. Pattern lower/upper bounds return one half-open contiguous range containing exactly all occurrences, including overlaps.
7. Sentinel appears exactly once where required and is excluded/included consistently in occurrence, substring, BWT, and serialization claims.
8. Construction ranks, buckets, counts, offsets, and temporary indices cannot overflow supported sizes and are not published partially.
9. Mapped arrays, text, sampling, child indexes, and handles belong to the same version and pass structural/semantic validation.

### Common failures

- Sorting suffix strings by copying them, accidentally using quadratic memory/time.
- Returning suffix-array ranks as occurrence positions without converting/sorting as the API promises.
- Using an upper-bound comparison that misses patterns whose match suffix has extra trailing symbols.
- Excluding overlapping matches.
- Mixing byte offsets with Unicode code-point or grapheme positions.
- Choosing a sentinel that already occurs or is not globally smallest under the actual encoding/comparator.
- Building LCP with the wrong neighbor convention or reading past text end.
- Counting sentinel-containing substrings as user-text substrings.
- Storing 32-bit positions for `n` or temporary products that exceed the range.
- Loading a permutation-valid but incorrectly ordered suffix array and trusting binary search results.

### Compact example

For `banana$`, with `$` unique and smallest, `SA=[6,5,3,1,0,4,2]` orders `$`, `a$`, `ana$`, `anana$`, `banana$`, `na$`, `nana$`. The adjacent LCP array is `[0,0,1,3,0,0,2]`. Pattern `ana` occupies ranks `[2,4)` and occurs at text positions 1 and 3. Maximum LCP 3 yields repeated substring `ana`. Excluding the sentinel, `banana` has `21-(1+3+2)=15` distinct substrings. Its BWT with sentinel is `annb$aa`.

### Connections

[DSE-005](005-contiguous-and-linked-layouts.md), [DSE-006](006-memory-locality-and-cache-behavior.md), [DSE-011](011-fixed-arrays.md), and [DSE-012](012-dynamic-arrays-and-geometric-growth.md) provide array/locality foundations. [DSE-044](044-tries.md) through [DSE-046](046-patricia-tries.md) provide string identity and alternative indexes. [DSE-037](037-fenwick-interval-and-segment-trees.md) supplies range-query structures used with LCP. The [program roadmap](../ROADMAP.md) continues with suffix trees/automata and graph algorithms.

## Governing Question

Which text identity, suffix definition, sentinel, construction algorithm, rank/LCP auxiliary data, query contract, index width, storage layout, mutability strategy, and evidence justify a suffix array for the workload?

## Why This Matters

A suffix array turns substring questions into ordered-array questions. It stores one starting position per suffix rather than a pointer-heavy suffix tree. Binary search finds exact pattern intervals. Adjacent LCP values expose repetitions and distinct-substring counts. Range-minimum queries over LCP answer LCP of arbitrary suffixes. BWT and FM-index structures derive from suffix order and support compressed full-text indexing.

The abstraction is compact, but construction and boundaries are not trivial. Naïvely materializing each suffix copies `Theta(n^2)` symbols. Comparison sorting can inspect long equal prefixes repeatedly. Efficient algorithms rank prefixes, radix-sort integer pairs, induce suffix classes, or use difference covers. Temporary memory may exceed final `n` positions. Text encoding and sentinel order can silently change every result.

Suffix arrays are normally immutable. One inserted character can change many suffix starts and the global order. Production systems build new immutable segments/snapshots, maintain several indexes, or use another dynamic structure. Search results are positions into one exact text generation; applying them to changed text is unsafe.

Correctness must go beyond “array is a permutation.” A corrupted or mismatched `SA` can contain every index once yet be out of order; binary search then returns plausible omissions. LCP and BWT can be self-consistent with the wrong text version. Persistent metadata must bind text digest, encoding, sentinel, position width, arrays, and algorithm version.

## Prerequisites and Retrieval

Retrieve representation and operation contracts from [DSE-002](002-representation-invariants.md) and [DSE-003](003-operation-contracts.md), complexity/byte accounting from [DSE-004](004-time-space-and-allocation-cost.md), locality from [DSE-006](006-memory-locality-and-cache-behavior.md), fixed/dynamic arrays from [DSE-011](011-fixed-arrays.md) and [DSE-012](012-dynamic-arrays-and-geometric-growth.md), binary search and ordering from [DSE-031](031-binary-search-trees.md), and interval/range structures from [DSE-037](037-fenwick-interval-and-segment-trees.md). Retrieve Unicode/canonicalization distinctions from [DSE-044](044-tries.md).

## Learning Objectives

After completing this module, you should be able to:

1. specify text symbols, positions, suffixes, sentinel, and index generation;
2. validate suffix-array permutation and full adjacent ordering;
3. derive prefix-doubling construction and its rank-pair invariant;
4. explain induced-sorting and difference-cover construction families without overclaiming one implementation;
5. build inverse ranks and the LCP array using Kasai's amortized scan;
6. implement correct lower/upper pattern bounds with overlapping occurrences;
7. derive longest-repeat and distinct-substring formulas;
8. connect suffix order to BWT, LCP RMQ, and compressed indexes;
9. design bounded, versioned, hostile-input-safe persistent arrays; and
10. create reference, metamorphic, failure, construction, search, and workload evidence.

## Core Exposition

**Freeze text identity and positions.** Let `T[0..n)` be a finite sequence over a totally ordered alphabet. The suffix at `i` is `T[i..n)`. Decide whether the empty suffix at `n` is indexed. This module indexes only positions `0..n-1`; when a sentinel is appended, its one-symbol suffix is included at `n_original`.

A byte-oriented suffix array uses byte positions and byte lexicographic order. UTF-8 byte order can support exact encoded substring search, but result offsets are bytes, not code points or graphemes. Arbitrary pattern bytes might cut encoded scalars unless API validation prevents it. A code-point array needs decoded storage or an offset mapping. Locale collation generally does not preserve substring semantics. Apply the versioned canonicalization policy before indexing and return positions in an explicitly named coordinate system.

The alphabet comparator must be total and stable. For compact construction, remap symbols to dense nonnegative ranks while preserving order. Reserve rank zero for a unique sentinel smaller than all data symbols. Check that the sentinel does not occur in the text. For arbitrary binary data containing every byte value, widen the alphabet or use a virtual sentinel rather than assume byte zero is absent.

Appending a unique smallest sentinel makes no suffix a prefix ambiguity except at the sentinel boundary and yields a unique lexicographically first sentinel suffix. It connects suffix order with sorted cyclic rotations for BWT. But sentinel-containing results are not user substrings. Track original and indexed lengths separately.

**The suffix array is a semantic permutation.** `SA[r]=i` means suffix at position `i` has rank `r`. Validation first checks length, bounds, and uniqueness. Then compare every adjacent pair `T[SA[r-1]..)<T[SA[r]..)` under full order. This straightforward check can be quadratic on highly repetitive text, so production validators may use independently recomputed ranks/hashes/LCP or rebuild with a trusted algorithm. State assurance versus cost.

Construct `rank` by `rank[SA[r]]=r`. Verify both directions: `SA[rank[i]]=i` and `rank[SA[r]]=r`. Rank is useful for LCP and suffix-to-order queries. Neither array alone owns the text; generation/digest binding is mandatory.

Storage is `n*w` bytes for SA positions plus optional `n*w` rank and `n*w_lcp` LCP before headers/alignment/text. `w` must represent `0..n-1`; temporary counts, pair keys, byte sizes, and sentinel-extended `n+1` may need wider types. A 32-bit array saves half the position bytes when valid, but a file or corpus crossing `2^32-1` cannot be truncated.

**Naïve construction clarifies correctness but not scale.** Generate all positions and sort with a comparator that walks text symbols. It stores only positions, but comparison sorting performs `O(n log n)` comparisons and each may inspect `O(n)` common prefix, giving `O(n^2 log n)` worst-case symbol work. Materializing suffix strings also uses quadratic total symbols. This is appropriate only as a tiny independent oracle.

Prefix doubling assigns ranks to length-one prefixes, then repeatedly sorts suffixes by the pair `(rank_k[i],rank_k[i+2^k])`, using a sentinel rank for beyond end. Equal pairs receive the same new rank; unequal pairs receive increasing ranks. After the round, ranks describe prefixes of length `2^(k+1)`.

Inductive proof: a `2L` prefix is the concatenation of two length-`L` blocks. By induction their ranks preserve lexicographic/equality order. Sorting the pair orders `2L` prefixes. Once `L>=n`, each prefix covers the full remaining suffix, so ranks are unique and order is the suffix array. Early stop when class count equals `n`.

Comparison sorting pairs gives `O(n log^2 n)` in a direct implementation. Because pair components are integers in bounded rank range, stable counting/radix sorting makes each round `O(n)`, for `O(n log n)` time and linear auxiliary space. Cyclic-shift formulations with a sentinel are common; their modular indices, sentinel removal, and beyond-end rank conventions must be consistent.

Doubling is practical, understandable, and parallelizable, but temporary arrays include SA, ranks, new ranks, pairs/keys or counting buffers. In-place optimizations complicate failure safety. Build privately and publish only after permutation/order validation. Memory-map or stream decisions depend on `n` and storage bandwidth.

**Linear-time families require stronger machinery.** Difference-cover/DC3/skew algorithms recursively sort a subset of suffixes, derive ranks, then merge remaining suffixes using bounded tuples. SA-IS classifies suffixes into S/L types, sorts LMS substrings, names/reduces them, recursively orders names if needed, and induces remaining suffixes from bucket boundaries.

The high-level `O(n)` claim assumes an integer alphabet and RAM model with bounded operations; an implementation must validate alphabet remapping, bucket counts, sentinel, recursion/stack, index arithmetic, and temporary memory. Linear asymptotics do not guarantee faster performance at every size. Libraries such as libdivsufsort and libsais provide engineered implementations with specific types, APIs, threading, and memory behavior; consult their exact contracts and test your build.

Construction choice depends on text length, alphabet, repetitiveness, memory cap, threads, platform, external memory, and whether BWT/LCP are also needed. A simpler doubling implementation may be easier to verify for moderate inputs. A production linear-time library may be superior when its supported width and memory model match. Never label a wrapper linear merely because the underlying paper is.

**Kasai builds LCP by reusing one-symbol shifts.** Define `LCP[r]=lcp(T[SA[r-1]..],T[SA[r]..])` for `r>0`, `LCP[0]=0`. Given inverse `rank`, scan positions `i=0..n-1`. If `rank[i]=0`, no predecessor and reset/continue. Let `j=SA[rank[i]-1]`. Starting from retained `h`, extend while `T[i+h]=T[j+h]` in bounds. Store `h` at `LCP[rank[i]]`, then set `h=max(h-1,0)`.

Why can comparison start at `h-1` on the next text suffix? If `T[i..]` and its predecessor share `h`, then shifted suffixes `T[i+1..]` and `T[j+1..]` share at least `h-1`. The lexicographic predecessor of `i+1` may be different, but standard ordering reasoning ensures its LCP is at least that lower bound for the relevant computation. Each successful extension increments `h`; each iteration decrements at most once, so total extensions are `O(n)`.

Bounds checks precede symbol reads. Sentinel can simplify but not authorize reading beyond allocation. LCP width must represent suffix length; sum of LCP for counting distinct substrings may require a wider accumulator. Validate each LCP by direct comparison in tiny tests and sampled/hashed independent checks at scale.

An LCP range-minimum query answers LCP of any suffix ranks `a<b`: the minimum of `LCP[a+1..b]`. Build a segment tree, sparse table, Cartesian tree/RMQ encoding, or other static RMQ with its own space/query trade-off. LCP-accelerated binary search retains matched-prefix bounds to avoid rescanning pattern prefixes; implementation is subtler than plain search.

**Pattern search is two boundaries, not one hit.** Define comparison between suffix and pattern carefully. For lower bound, find first suffix lexicographically not less than the pattern under normal sequence order. For upper prefix bound, find first suffix whose initial `|P|` symbols are greater than `P`, treating every suffix beginning with `P` as equal for this boundary.

A safe alternative finds lower bound for `P`, then another boundary with a comparator returning “match-prefix” as not greater until the common-prefix range ends. Constructing `P` plus a maximal sentinel is unsafe for arbitrary alphabets unless a true out-of-alphabet upper symbol and overflow-free encoding exist. Specify empty pattern: it matches every suffix position or is rejected by API policy.

All suffixes beginning with `P` are contiguous. If two ordered suffixes share prefix `P`, any suffix between them cannot differ below/above within the first mismatching symbol without violating order, so it also begins with `P`. The half-open range permits zero matches and overlapping occurrences. Text-order results require sorting or an auxiliary position index; suffix-rank order is lexicographic-context order.

Plain binary search performs `O(log n)` suffix-pattern comparisons, each up to `|P|`, hence `O(|P| log n)` plus output. It may inspect less on early mismatches. LCP-aware variants can approach `O(|P|+log n)` comparisons under supporting structures. Cache misses to scattered text positions can dominate.

Case-insensitive/normalized searching must index the same transformed text and map result positions back to originals if required. Transformations can change lengths, many-to-one identity, and boundaries. Maintain an offset map and define whether matches correspond to raw spans. Suffix arrays do not solve tokenization or collation.

**LCP turns suffix order into substring analytics.** Longest repeated substring length is `max LCP`; one witness starts at the corresponding suffix position. Ties need a deterministic policy and occurrences may overlap. A substring appearing at least `k` times corresponds to a window of `k` suffixes whose minimum adjacent LCP is its shared length; sliding-window RMQ/deques can find candidates.

The distinct-substring formula follows by adding suffixes in SA order. Suffix at `SA[r]` has `n-SA[r]` prefixes. Exactly its first `LCP[r]` prefixes already occurred as prefixes of the preceding suffix; any substring repeated earlier has its relevant neighboring boundary captured through lexicographic grouping. Sum new prefixes: `sum(n-SA[r]-LCP[r])=n(n+1)/2-sum LCP`.

Use the original text without appended sentinel for this formula, or exclude the sentinel suffix and all prefixes containing it consistently. Accumulator `n(n+1)/2` can overflow even when positions fit. A 64-bit unsigned result overflows for sufficiently large `n`; use checked/wider arithmetic or document limit.

Other applications include longest common substring across documents by concatenating with distinct separators and finding large LCPs between suffixes from different documents. Separators must be unique/ordered and not cross boundaries; ownership labels and privacy constraints matter. Repeated-pattern analytics can amplify output and expose text content.

**BWT and compressed search build on exact suffix order.** With one unique sentinel, BWT at suffix rank `r` is the symbol preceding position `SA[r]`, wrapping position zero to sentinel. For `banana$`, suffix order yields `annb$aa`. BWT is reversible with sentinel/primary-index information because sorted rotations and stable occurrence ranks define the LF mapping.

An FM-index combines BWT with cumulative symbol counts and rank/occurrence queries to backward-search a pattern in space related to compressed text. Locating original positions needs sampled SA and LF steps; extracting text needs more support. Wavelet trees/matrices or bitvectors implement rank/select. These are not “free” properties of SA and require separate invariants and evidence.

Suffix arrays can construct BWT without materializing rotations. A library might produce BWT directly with different sentinel/primary-index conventions. Validate round trip and known vectors. BWT compression effectiveness depends on text; transformation itself is not compression.

**Mutability favors immutable generations.** Inserting or deleting one text symbol changes positions of later suffixes and may reorder most suffixes. Updating SA in place is rarely appropriate. Build immutable segment indexes, use an LSM-like collection of text segments, batch rebuild, or choose suffix trees/automata/dynamic indexes. Querying multiple segments adds merge/deduplication and tombstone/version logic.

An index handle includes text generation/digest, coordinate system, sentinel/encoding, and array generation. Returned positions cannot be applied to a mutated buffer. Copy-on-write text without a rebuilt SA is inconsistent even if old bytes remain. Publish text, SA, rank, LCP, and auxiliaries atomically as one version.

Read-only arrays support concurrent searches with shared immutable text. Protect mapping/lifetime through references, epochs, or file leases. Lazy LCP/RMQ caches need synchronized one-time construction or private publication. A “const” search may still write metrics/cache state; keep that outside semantic arrays or synchronize it.

Parallel construction partitions sorting/counting/induction work but must preserve stable bucket boundaries and avoid races. NUMA placement and large temporary buffers matter. Parallel searches are embarrassingly read-only but can contend on memory bandwidth and page faults. Benchmark cold/warm and batch effects.

**Persistence is a coupled-array schema.** Store magic/version, text or text digest/reference, original/indexed lengths, alphabet/normalization/sentinel, coordinate/index widths, SA and optional rank/LCP/RMQ/BWT regions, algorithm/build metadata, byte order, and checksums/authentication. File-relative offsets and sizes use checked arithmetic.

On load, bound `n`, file regions, allocation/mapping, and validation. Check SA permutation and entries; rank inverse; LCP length/bounds and semantics; sentinel count/order; text digest; optional BWT/RMQ consistency. Validate region nonoverlap/alignment per format. A checksum does not prove the index belongs to authorized text or is semantically sorted.

Full adjacent-order validation can be expensive. A high-assurance ingest can rebuild or compare with an independent algorithm, verify suffix ranks using rolling hashes plus collision-safe fallbacks, or sample with documented limitation. Never claim full semantic validation from permutation alone. Store a cryptographic text digest for binding, but authenticate provenance separately.

Crash-safe rebuild writes private arrays, validates, flushes, and durably publishes a generation manifest/root. Old files remain until readers release and recovery no longer needs them. Avoid overwriting a live mapped SA. Generated reports/logs stay outside governed index artifacts.

**Security is dominated by size and comparison work.** Untrusted `n` can overflow `n*w`, `n(n+1)/2`, bucket counts, sentinel extension, or allocation. Check every conversion/add/multiply. Validate positions before text indexing. A malicious LCP can induce out-of-range RMQ or extraction if trusted.

Long repetitive texts make naive suffix comparison/build quadratic and can be denial-of-service input. Select algorithms with defended bounds, cap inputs/time/temp memory, and measure worst patterns such as all-equal symbols and long periodic strings. Pattern output can be `Theta(n)`; paginate and authorize. Empty patterns need explicit limits.

Indexes reveal substrings, repetitions, and positions. Access control applies to search and analytics; multi-document concatenation needs document boundary/tenant filters. Timing and page access can leak query/text locality. Suffix arrays are not privacy-preserving indexes.

Parser fuzzing mutates lengths, offsets, widths, permutations, ranks, LCPs, sentinel, and region overlaps. Construction failure injection covers symbol remap, SA/rank/LCP/temp allocations, sorting, thread creation, disk writes, validation, and publication. The old generation must remain usable on failure.

**Evidence starts with naïve suffix strings on tiny texts.** A reference oracle may materialize/sort suffixes because tiny bounds make it independent and transparent. Compare SA, rank, LCP, pattern ranges/positions, longest repeat, distinct count, and BWT. Use another construction (doubling versus library) for larger differential tests.

Exhaust tiny alphabets/texts: empty (if supported), one symbol, all equal, all distinct, periodic, sentinel-adjacent symbols, embedded zero, maximum symbol, and every short text. Patterns include empty, longer than text, absent before/between/after alphabet, full text, suffix, prefix, repeated/overlapping, and sentinel-forbidden. Verify every substring by brute force.

Metamorphic properties include SA/rank inversion; adjacent order; LCP symmetry/bounds; pattern interval contiguity; occurrences equal brute force; appending a uniquely minimal sentinel places it first; alphabet order-preserving remapping preserves SA; distinct count equals set enumeration; BWT inversion returns indexed text; and rebuild/serialize round trips preserve generation content.

For construction, assert each doubling round's ranks equal ordering of bounded prefixes on small texts. For induced sorting, validate type classification, bucket counts/heads/tails, LMS naming, recursive reduction, and induction separately. Fuzz library wrappers across 32/64-bit widths and allocation failures.

Benchmarks vary `n`, alphabet, entropy/repetition/periodicity, suffix common prefixes, text source, pattern length/hit rate/occurrences, query batches, construction algorithm/threads, index widths, LCP/RMQ, storage, and cache state. Measure final/temporary/peak bytes, build time, comparisons/scans, query latency distributions, output, page faults, cache/TLB/branch, mapping/reload, validation, and publish/reclaim. Record toolchain/library versions and exact corpus digests.

The executable below uses a deliberately naïve suffix sort as a finite oracle for `banana$`, builds inverse ranks and adjacent LCP, performs correct prefix-range search, checks overlapping occurrences, derives longest repeat/distinct count, computes BWT, and inverts BWT independently by sorted rotations. It is not evidence of scalable construction, Unicode mapping, fixed-width safety, concurrency, persistence, security, or production performance.

<!-- bijux-verify: {"id":"suffix-array-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"text=banana$\nsa=6,5,3,1,0,4,2\nlcp=0,0,1,3,0,0,2\nsuffix_order=$|a$|ana$|anana$|banana$|na$|nana$\nana_range=2,4\nana_positions=1,3\nmissing_xyz=True\nlongest_repeat=ana\ndistinct_substrings_banana=15\nbwt=annb$aa\ninverse_ok=True\ninvariant=True\nevidence=finite_suffix_array_trace\n","stderr":""}} -->
```python
text = "banana$"
sa = sorted(range(len(text)), key=lambda position: text[position:])
rank = [0] * len(text)
for order, position in enumerate(sa):
    rank[position] = order


def common_prefix(a, b):
    length = 0
    while a + length < len(text) and b + length < len(text) and text[a + length] == text[b + length]:
        length += 1
    return length


lcp = [0] + [common_prefix(sa[r - 1], sa[r]) for r in range(1, len(sa))]


def prefix_range(pattern):
    low, high = 0, len(sa)
    while low < high:
        middle = (low + high) // 2
        fragment = text[sa[middle]:sa[middle] + len(pattern)]
        if fragment < pattern:
            low = middle + 1
        else:
            high = middle
    first = low
    low, high = first, len(sa)
    while low < high:
        middle = (low + high) // 2
        fragment = text[sa[middle]:sa[middle] + len(pattern)]
        if fragment <= pattern:
            low = middle + 1
        else:
            high = middle
    return first, low


low, high = prefix_range("ana")
positions = sorted(sa[low:high])
missing_low, missing_high = prefix_range("xyz")
repeat_rank = max(range(len(lcp)), key=lambda r: lcp[r])
longest_repeat = text[sa[repeat_rank]:sa[repeat_rank] + lcp[repeat_rank]]
distinct = 6 * 7 // 2 - sum(lcp)
bwt = "".join(text[position - 1] if position > 0 else text[-1] for position in sa)
table = [""] * len(bwt)
for _ in bwt:
    table = sorted(bwt[i] + table[i] for i in range(len(bwt)))
inverse = next(row for row in table if row[-1] == "$")
invariant = (
    sorted(sa) == list(range(len(text)))
    and all(text[sa[r - 1]:] < text[sa[r]:] for r in range(1, len(sa)))
    and all(sa[rank[position]] == position for position in range(len(text)))
    and lcp == [0, 0, 1, 3, 0, 0, 2]
)

print(f"text={text}")
print("sa=" + ",".join(map(str, sa)))
print("lcp=" + ",".join(map(str, lcp)))
print("suffix_order=" + "|".join(text[position:] for position in sa))
print(f"ana_range={low},{high}")
print("ana_positions=" + ",".join(map(str, positions)))
print(f"missing_xyz={missing_low == missing_high}")
print(f"longest_repeat={longest_repeat}")
print(f"distinct_substrings_banana={distinct}")
print(f"bwt={bwt}")
print(f"inverse_ok={inverse == text}")
print(f"invariant={invariant}")
print("evidence=finite_suffix_array_trace")
```

## Definitions and Notation

Text `T` has `n` indexed symbols and suffix `S_i=T[i..n)`. `SA[r]` is position of rank `r`; `rank[i]` is rank of suffix `i`. This module defines `LCP[0]=0` and `LCP[r]=lcp(SA[r-1],SA[r])`. Pattern result ranks form `[lo(P),hi(P))`. `w` is stored position width. Original length excludes an appended sentinel; indexed length includes it.

A **symbol** is the declared encoded unit, not automatically a character. A **generation** binds text/digest, encoding/canonicalization, sentinel, SA, rank, LCP, RMQ/BWT auxiliaries, and coordinate mapping. A construction theorem's RAM/alphabet assumptions are distinct from one library's API, memory, threading, and supported widths.

## Mechanisms, Invariants, or Proof Structure

Correctness layers are: valid text/sentinel; SA permutation; strict full adjacent suffix order; inverse rank; adjacent LCP semantics; binary-search comparison and contiguous prefix interval; derived formula boundaries. Doubling proves bounded-prefix ranks inductively. Kasai proves linear total extension by retaining/decrementing `h`. Distinct-substring counting adds only prefixes not shared with the preceding suffix.

Production layers add remapping, overflow/allocation, construction-specific buckets/induction, atomic generations, coordinate mapping, persistence/provenance, concurrency/lifetime, and resource/security limits. None follows merely from sorting one finite suffix list.

## Alternatives and Trade-Offs

| Construction/index | Strength | Principal cost/assumption |
|---|---|---|
| naïve suffix comparator | independent tiny oracle | quadratic-like repeated comparisons |
| prefix doubling + comparison sort | simple proof/implementation | `O(n log^2 n)` direct form |
| prefix doubling + radix/count sort | practical `O(n log n)` | integer ranks and linear buffers |
| SA-IS/induced sorting | linear-time family | classification/buckets/recursion complexity |
| DC3/difference cover | linear-time/parallel ideas | recursive tuple/merge machinery |
| engineered library | optimized widths/threads/BWT | dependency contracts and platform evidence |
| suffix tree/automaton | richer online/path states | pointer/state memory and complexity |
| FM-index | compressed backward search | rank/select and sampled locating |

Choose from text size/alphabet/repetition, memory and temporary budget, construction frequency, query/analytics suite, position width, platform/threads, mutability, and assurance requirements.

## Failure Modes and Misconceptions

- SA permutation does not prove suffix ordering or text-version agreement.
- A unique sentinel must be unique and correctly ordered in the actual encoded alphabet.
- LCP index conventions differ; formulas must use the declared neighbor.
- Binary searching one match and scanning carelessly can miss range boundaries or overlaps.
- Suffix-rank order is not text-position order.
- Unicode byte offsets are not code-point/grapheme offsets.
- Linear-time papers do not make every wrapper/build linear or memory-optimal.
- BWT is reversible transformation, not compression by itself.
- One text edit generally invalidates the generation rather than locally shifting positions.
- Tiny `banana` evidence validates examples, not scalable build/query/security claims.

## Worked Examples

### Example 1

For `aba$`, suffixes are `$`, `a$`, `aba$`, `ba$`, so `SA=[3,2,0,1]`. Checking only `[0,1,2,3]` as a permutation would not detect an incorrectly swapped pair.

### Example 2

In a doubling round with length `L`, suffix `i` has pair `(rank[i],rank[i+L])`, using a below-all rank beyond end. Equal pairs mean equal prefixes of length `2L`; stable integer sorting and reranking prepare the next round.

### Example 3

For `aaaa`, naïve suffix comparisons repeatedly scan long equal prefixes. Its SA is `[3,2,1,0]` and LCP `[0,1,2,3]`, making it a necessary worst-pattern construction/query test.

### Example 4

Pattern `ana` in `banana` occurs at positions 1 and 3, which overlap. The suffix interval contains both. Filtering future searches by advancing `|P|` would change the occurrence contract.

### Example 5

Ranks `[lo,hi)` are lexicographic suffix order. Returning `[3,1]` may be valid rank order, while an API promising text order must sort to `[1,3]` or maintain another index.

### Example 6

Maximum adjacent LCP in `banana$` is 3 between `ana$` and `anana$`, yielding `ana`. Equal maximums require a policy such as lexicographically first or earliest position.

### Example 7

`banana` has 21 substring occurrences by lengths; sum LCP is 6, so 15 are distinct. Including `$` changes both `n` and allowed substrings and must not be mixed into the user result.

### Example 8

LCP of suffix ranks `a<b` is the minimum adjacent LCP over `a+1..b`. One LCP array plus RMQ answers arbitrary suffix-pair LCP without re-reading their full common prefix.

### Example 9

A mapped SA contains every index once but was built for a different same-length text. Permutation validation passes. Text digest and semantic adjacent-order validation catch the mismatch.

### Example 10

Pattern `""` is a prefix of every suffix under mathematical semantics, producing `n` outputs. A service may reject it or require a bounded page, but cannot silently call the unbounded result constant-time.

## Cross-Program Connections

- **Algorithms:** binary search, stable integer sorting, RMQ, repeated substrings, and string matching derive directly from suffix order/LCP.
- **Data engineering:** batch text normalization, symbol remapping, immutable segment construction, manifests, checksums, and rebuild publication mirror pipelines.
- **Database engineering:** suffix arrays are immutable secondary indexes with version binding, mapped columns, range searches, and compaction-style replacement.
- **Search/information retrieval:** BWT/FM-index, rank/select, sampled locating, document separators, and corpus access control extend the core arrays.
- **Concurrent programming:** read-only generations simplify queries while private parallel construction and lifetime-safe atomic publication handle rebuilds.
- **Security engineering:** repetitive worst cases, hostile offsets/permutations/LCP, output amplification, corpus leakage, and authorization require controls.
- **Computer architecture:** integer widths, sequential arrays, scattered text comparisons, memory bandwidth, cache/TLB, NUMA, and mapping dominate scale.

## References

1. [Princeton Algorithms, *Suffix Arrays*](https://algs4.cs.princeton.edu/63suffix/).
2. [`libdivsufsort` maintained source and API](https://github.com/y-256/libdivsufsort).
3. [`libsais` maintained source and API](https://github.com/IlyaGrebnov/libsais).
4. [Stanford CS97SI, *Suffix Array* lecture notes](https://web.stanford.edu/class/cs97si/suffix-array.pdf).
5. [Juha Kärkkäinen, Peter Sanders, and Stefan Burkhardt, *Linear Work Suffix Array Construction*](https://www.cs.helsinki.fi/u/tpkarkka/publications/icalp03.pdf).
6. [Carnegie Mellon University, *Suffix Arrays* lecture notes](https://www.cs.cmu.edu/~ckingsf/bioinfo-lectures/suffixarrays.pdf).
7. [Rust `suffix` crate documentation](https://docs.rs/suffix/latest/suffix/).
8. [Carnegie Mellon University, *Burrows-Wheeler Transform* lecture notes](https://www.cs.cmu.edu/~ckingsf/bioinfo-lectures/bwt.pdf).

## Exercises

### Exercise 1

Construct SA, inverse rank, and this module's LCP array for `mississippi$`. Give the suffix-rank interval and text-order occurrence positions for pattern `issi`.

### Exercise 2

Prove one prefix-doubling round: if ranks correctly order/equate length-`L` prefixes, sorting rank pairs correctly orders/equates length-`2L` prefixes. State beyond-end and sentinel assumptions.

### Exercise 3

Derive Kasai's retained-`h` rule and explain why total symbol extensions are linear. Identify all bounds and LCP-index conventions an implementation must test.

### Exercise 4

Design a persistent suffix-index generation for normalized UTF-8 documents that must return original byte spans. Specify mapping, separators, widths, digest/provenance, arrays, atomic publication, validation, and access control.

### Exercise 5

Specify differential and benchmark evidence comparing doubling, SA-IS/library construction, and a naïve oracle. Cover input families, invariants, failures, widths, temporary/final bytes, threads, queries, and prohibited conclusions.

## Answers to the Exercises

### Answer 1

For `mississippi$`, sorted suffix starts are `SA=[11,10,7,4,1,0,9,8,6,3,5,2]`, spelling `$`,`i$`,`ippi$`,`issippi$`,`ississippi$`,`mississippi$`,`pi$`,`ppi$`,`sippi$`,`sissippi$`,`ssippi$`,`ssissippi$`. Thus `rank[11]=0, rank[10]=1, rank[7]=2, rank[4]=3, rank[1]=4, rank[0]=5, rank[9]=6, rank[8]=7, rank[6]=8, rank[3]=9, rank[5]=10, rank[2]=11`. Adjacent LCP is `[0,0,1,1,4,0,0,1,0,2,1,3]`. Pattern `issi` matches suffix ranks `[3,5)` at starts 4 and 1; text-order positions are `[1,4]`.

### Answer 2

Write a length-`2L` prefix as first block `T[i..i+L)` and second block `T[i+L..i+2L)`, padding/bounding beyond end with a rank below real symbols consistent with the unique sentinel. By hypothesis, `rank_L` equality/order exactly represents each block. Lexicographic comparison of concatenations first compares the first-block ranks; when equal it compares second-block ranks. Therefore pair comparison gives precisely length-`2L` equality/order. Stable/counting/radix sorting must sort the pair lexicographically. Reassign equal consecutive pairs the same new rank and others increasing. When `2L>=n` with sentinel/beyond-end convention, prefixes determine full suffixes.

### Answer 3

If suffix `i` and its predecessor share `h` symbols, deleting their first symbols gives suffixes beginning at `i+1` and `j+1` sharing at least `h-1`. Lexicographic ordering guarantees the relevant predecessor comparison for `i+1` cannot have a smaller usable lower bound in the standard Kasai argument. Start the next extension at `max(h-1,0)`. Across the outer scan, `h` decreases by at most one per position and never exceeds `n`; every successful symbol comparison increments it, so total increments/extensions are `O(n)`. Check `rank[i]=0`, both `i+h<n` and `j+h<n` before reads, `LCP[0]=0`, storage width, and whether LCP is stored at the later rank or earlier neighbor; test empty/singleton/repetitive/sentinel cases.

### Answer 4

Create a versioned canonicalization that maps raw document bytes to indexed symbol bytes/code points and a monotone span map back to original byte ranges, retaining document IDs and unique separators that cannot match patterns or cross documents. Store original/indexed lengths, normalization/Unicode version, separator alphabet, coordinate system, 32/64-bit widths, document table, text or authenticated text digest/reference, SA/rank/LCP/RMQ/BWT regions, build tool/version, checksums and provenance. Build/validate privately; atomically publish one manifest generation; pin old generations for readers and reclaim later. Validate regions with checked arithmetic, SA permutation/order, inverse rank, LCP, separators/boundaries, mapping monotonicity/ranges, and text digest. Authorize corpus/document access before search/output and map only permitted matches; bound pattern, empty query, occurrences, analytics, and diagnostics.

### Answer 5

Use a naïve materialized-suffix oracle only for bounded texts, an independently written doubling implementation, and the selected SA-IS/library wrapper. Exhaust tiny alphabets/texts and test random, all-equal, all-distinct, periodic, de Bruijn-like, natural/binary/Unicode-normalized, embedded zero, and width-boundary inputs. Compare SA, adjacent full order, rank inverse, LCP, every small pattern interval/overlap, repeats, distinct count, and BWT round trip. Inject remap/count/temp/allocation/thread/I/O/publication failures and fuzz 32/64-bit interfaces. Measure final and peak temporary bytes, build/validation time, scaling, page/cache behavior, and downstream plain/LCP-aware queries across cold/warm states. Record exact versions/hardware/corpus digests. Results cannot establish universal fastest/smallest behavior, linearity of a wrapper, Unicode/security correctness, crash safety, or deployment fitness beyond the tested contracts.
