---
module_id: DSE-091
program: Data Structures Engineering
level: 2
module_number: 91
title: Bit Vectors with Rank and Select
status: complete
last_verified: 2026-08-30
---

# Bit Vectors with Rank and Select

## One-Page Review

### Governing question

How can a bit vector retain direct bit access while answering prefix counts and occurrence positions quickly with rigorously bounded auxiliary space?

### Essential definitions

For (B[0..n)in\{0,1\}^n), this chapter uses half-open, zero-based conventions:

\[
\operatorname{rank}_b(i)=|\{j:0\le j<i\land B[j]=b\}|,
\qquad 0\le i\le n,
\]

and (operatorname{select}_b(t)) is the position of the zero-based (t)-th occurrence of bit (b). It is defined only for (0\le t<\operatorname{rank}_b(n)). Thus `rank` counts *before* a position, while `select` returns a position.

A plain bit vector takes (n) bits. A succinct static rank/select representation targets (n+o(n)) total bits while supporting `access`, `rank`, and `select` in constant time on a stated word-RAM model. A compressed bit vector instead targets space related to density or entropy, such as (log_2\binom{n}{m}) for (m) one-bits, with its own time/space contract.

### Central model, mechanism, or theorem

Jacobson-style rank uses a two-level directory. Store global counts at superblocks of (s=\Theta(\log^2 n)) bits, within-superblock counts at blocks of (b=\Theta(\log n)) bits, then answer the residual block with a word operation or universal lookup. The auxiliary terms are (o(n)), so the original (n) bits plus the directory are succinct.

Select is harder because occurrence spacing is irregular. Designs sample selected positions, classify sparse/dense regions, use subdirectories or tables, or reduce to rank-guided search with a weaker time bound. Practical structures use broadword instructions, hierarchical inventories, or compressed encodings. Every claim depends on conventions, machine word size, serialized layout, and density.

### Critical invariants

- Length, bit order within bytes/words, endianness, padding, and rank/select convention are versioned.
- (operatorname{rank}_1(0)=0), (operatorname{rank}_1(n)) equals total one-bits, and rank is nondecreasing with unit increments.
- (operatorname{rank}_0(i)=i-operatorname{rank}_1(i)) under the half-open convention.
- For valid (t), (B[\operatorname{select}_b(t)]=b) and (operatorname{rank}_b(\operatorname{select}_b(t))=t).
- Directory counters equal recomputed prefixes and fit their serialized widths.
- Padding bits never contribute to logical rank/select.
- Static supports are rebuilt or atomically versioned when bits change; dynamic supports update every affected summary.

### Common failures

Failures include mixing inclusive and half-open rank, mixing one-based and zero-based select, calling (O(n)) machine words “(O(n)) bits,” ignoring directory/table space, using population-count instructions unavailable on the target, counting word padding, overflowing counters, serializing native structs, selecting past the last occurrence, claiming static bounds for mutable structures, using sparse compression on dense unpredictable bits, and benchmarking only cache-hot uniform queries.

### Compact example

For the 32-bit fixture `10110010100011101001011000101101`, superblocks are eight bits and blocks four. Global superblock counts are `[0,4,8,12,16]`; within-superblock block counts are `[0,3,0,1,0,2,0,1,0]`. The model computes (operatorname{rank}_1(17)=9), (operatorname{select}_1(7)=14), and (operatorname{select}_0(7)=15), then verifies rank/select inverses for all bits. Its tiny parameters demonstrate mechanics, not asymptotic succinctness.

### Connections

[DSE-090](090-hnsw-and-approximate-nearest-neighbor-graphs.md) concluded approximate vector indexes; rank/select begins the succinct block. The roadmap successor [DSE-092, “Wavelet Trees”](../ROADMAP.md) composes rank/select bit vectors recursively to support sequence queries over larger alphabets. Succinct trees, FM-indexes, inverted indexes, column stores, and graph representations all reuse these primitives.

## Governing Question

How should rank/select semantics, static or compressed representation, construction, serialization, validation, and performance be engineered so downstream succinct structures can trust every bit position?

## Why This Matters

Bit vectors encode membership, nullness, delimiters, tree topology, graph boundaries, postings, and routing decisions. Access alone is insufficient. Prefix count maps a physical position to an occurrence number; select maps an occurrence number back to its physical position. Together they replace many pointer or integer arrays with compact navigation.

The theoretical result is striking: keep the (n) data bits and add only lower-order space while supporting constant-time queries on the word RAM. Production reality is less automatic. Word layout, cache misses, instruction sets, sparse/dense distributions, select engineering, construction memory, persistence, and updates decide whether a representation is actually correct and useful.

## Prerequisites and Retrieval

Retrieve:

- binary strings, sets of positions, prefix sums, logarithms, binomial coefficients, and little-(o) notation;
- machine words, population count, shifts, masks, alignment, byte/bit order, and integer overflow;
- half-open ranges, zero/one-based APIs, sentinels, and partial final words;
- cache hierarchy, memory mapping, serialization schemas, checksums, and immutable generations;
- binary search, sampling, two-level directories, and property-based differential tests.

Distinguish the logical length (n) from allocated word capacity. A 65-bit vector may occupy two 64-bit words, but the last 63 physical padding bits are not data.

## Learning Objectives

After this chapter, you should be able to:

1. define `access`, half-open `rank`, and zero-based `select` without ambiguity;
2. derive the space bound of a two-level static rank directory;
3. explain why select needs sampling, classification, tables, or rank-guided search;
4. choose plain, RRR-style, sparse, run-length, or dynamic representations by workload;
5. specify word layout, padding, counter widths, serialization, mapping, and update invariants;
6. validate every query against a simple oracle and test boundary/adversarial cases;
7. benchmark space and latency across density, clustering, size, and cache regimes.

## Core Exposition

### Contract before representation

Let `access(i)` return (B[i]) for (0\le i<n). This chapter's (operatorname{rank}_1(i)) counts ones in (B[0..i)), so rank accepts the endpoint (n). Select uses zero-based occurrence numbering. Other libraries may count through position (i) or number occurrences from one. Neither convention is inherently wrong; undocumented mixing is.

The identities become executable specifications:

\[
\operatorname{rank}_0(i)=i-operatorname{rank}_1(i),
\]

\[
\operatorname{rank}_b(\operatorname{select}_b(t))=t,
\qquad
\operatorname{rank}_b(\operatorname{select}_b(t)+1)=t+1.
\]

Rank increments by (B[i]): (operatorname{rank}_1(i+1)-\operatorname{rank}_1(i)=B[i]). Select results strictly increase with (t). Define out-of-domain behavior—error, option, or sentinel—without colliding with a valid position.

### Succinct, compact, and compressed space

There are (2^n) arbitrary length-(n) bit vectors, so any injective representation needs (n) bits in the worst case. A structure using (n+o(n)) bits is succinct relative to that baseline. Saying “linear space” is weaker: (n) 64-bit counters use (64n) bits.

When exactly (m) bits are one, there are (inom{n}{m}) possible sets, giving information bound (log_2\binom{n}{m}) bits. Compressed rank/select structures aim near this density-sensitive bound plus redundancy. The bound excludes external labels, allocator metadata, process overhead, and sometimes construction workspace. State what is counted.

An implicit representation uses the baseline plus (O(1)) bits; a succinct representation permits lower-order redundancy; a compact implementation may simply use much less space in practice without attaining a formal bound. Do not exchange these terms casually.

### Two-level rank directory

Choose superblock size (s=\Theta(\log^2 n)) and block size (b=\Theta(\log n)). At each superblock boundary store the total ones before it, requiring (lceil\log_2(n+1)\rceil) bits. At each block boundary store ones since its superblock start, requiring (lceil\log_2(s+1)\rceil) bits.

For query position (i), add its superblock count, within-superblock block count, and population count in the residual bits from block boundary through (i). With (s=\log^2 n), the first directory costs

\[
O\!\left(\frac{n}{\log^2 n}\log n\right)
=O\!\left(\frac{n}{\log n}\right)=o(n).
\]

With (b=\tfrac12\log n), the second costs

\[
O\!\left(\frac{n}{\log n}\log\log n\right)=o(n).
\]

If the residual fits a word, masked population count is constant time under the word-RAM/instruction model. The classical universal table alternative stores answers for all (2^b=\sqrt n) block patterns and local positions; its polylogarithmic factor times (sqrt n) remains (o(n)). Real implementations normally use word operations because a global table and cache traffic have different constants.

Counter widths must be derived. A superblock count can reach (n); a block-relative count can reach (s). Bit packing narrower fields saves space but complicates unaligned loads and portability. Using full machine words simplifies access but may change the measured redundancy for finite (n).

### Select structures

Select cannot be answered from a fixed position directory alone because equal occurrence intervals can span one bit or millions. A simple reduction binary-searches positions using rank in (O(\log n)); it is valuable as an oracle and fallback but not the constant-time succinct result.

Classical select samples every (q)-th occurrence. Samples delimit regions containing equal numbers of target bits. A region spanning many positions is sparse and can store explicit positions within a bounded total space; a short dense region can use subblocks and a lookup table. Multi-level sampling or broadword selection reduces constants. The proof accounts separately for sparse exceptional regions, dense subdirectories, and universal tables.

Practical select structures often maintain an inventory of sampled positions plus subinventories encoding offsets, then locate a word and select a set bit using processor operations. Select-zero may use a separate support or complement-aware computation. A one-bit structure does not automatically supply equally fast zero selection.

### Word-level implementation

Pack bits into fixed-width unsigned words and declare whether logical position zero maps to the least- or most-significant bit. Rank loads a directory count, masks the partial word, and applies population count. Avoid undefined shifts by the word width; handle aligned endpoints separately. Mask padding in the final word before totals or select.

Broadword select uses arithmetic/masks to count subwords and locate a target set bit. Hardware `popcnt`, count-trailing-zero, vector instructions, and BMI variants improve constants but need feature detection and portable fallbacks. Compilers, flags, and runtime dispatch belong in benchmark evidence.

Layout directories near query data when locality helps, or separate them for streaming scans. Huge pages, prefetch, memory mapping, and NUMA placement can dominate theoretical operation counts. Measure random and batched query patterns.

### Compressed representations

RRR-style bit vectors partition bits into fixed-size blocks. A block's *class* is its number of ones; its *offset* identifies the block among all patterns in that class. Encoding offsets near (log_2\binom{b}{c}) bits approaches zero-order entropy while rank/select directories navigate class and offset streams. Decoding tables and variable offsets add cost and implementation complexity.

Sparse bit vectors can store sorted one positions or their gaps. Elias–Fano-style representations split monotone values into high and low parts; a unary high-part bit vector itself uses select. Sparse dictionaries can approach (log\binom{n}{m}) space and support position/ordinal mapping efficiently. For density near one, represent zeros sparsely or choose adaptively.

Run-length compression is strong when bits form long runs even if density is near one half. Roaring-like chunked bitmaps trade formal succinctness for practical intersections and updates. No representation dominates: density, clustering, operations, construction, updates, SIMD, and downstream composition decide.

Compressed size is distribution-dependent. An all-zero vector needs almost no payload in a specialized form, while an unpredictable half-dense vector is essentially incompressible. Include index redundancy and alignment in the measured bits-per-bit or bits-per-one.

### Dynamic rank and select

Static packed bits and directories cannot absorb insertion/deletion cheaply because positions and later prefix counts shift. A dynamic representation commonly uses a balanced tree of bit chunks with subtree length and one-count summaries. Access/rank/select descend by lengths or counts; insert/delete split, merge, and repair summaries.

The cost is typically logarithmic or polylogarithmic rather than the static constant-time bound, with extra pointer/allocator space. Append-only workloads can combine immutable segments with a mutable tail, then compact. Copy-on-write trees or immutable generations simplify readers and snapshots.

An in-place bit flip does not shift positions but changes every later prefix count unless summaries are hierarchical. Concurrent updates require atomic or locked summary propagation and consistent reader snapshots. Never mutate raw bits underneath static supports.

### Construction, serialization, and mapping

Streaming construction can emit packed words and directory entries as positions advance, avoiding a second full prefix array. Select supports may need totals or a second pass. Compressed formats often need block classes, prefix offsets, and allocation planning; track peak construction memory independently of final size.

A durable header binds schema version, logical length, total zeros/ones, bit order, word width, rank/select convention, representation kind, block parameters, section offsets/lengths, counter widths, instruction-independent encoding, and checksums. Serialize integers in declared byte order rather than dumping native structs with padding.

Validate every offset and multiplication before mapping, ensure sections fit the file, mask final padding, recompute sampled directories, and reject totals inconsistent with length. Corrupt counters can send select outside mapped memory. Publish payload and all supports as one immutable generation after checksums are durable.

### Applications

In a wavelet tree, a node bit vector routes symbols left/right. Rank translates a prefix position into a child prefix; select translates a child position back to its parent. An error at one level compounds through the path. [DSE-092](../ROADMAP.md) develops this composition.

Balanced-parentheses and LOUDS tree encodings use rank/select plus excess/search primitives to navigate parents, children, and siblings without pointers. Succinct graph encodings mark adjacency-list boundaries; select finds a vertex's segment and rank maps an edge position to its owner.

FM-indexes use rank over a transformed text to update suffix-array intervals. Bitmap indexes use rank to map a filtered bit position into a compact payload array. Null bitmaps use rank to locate the dense non-null value ordinal. These consumers often require billions of queries, making conventions and cache behavior more important than an isolated microbenchmark.

### Verification and benchmarking

The simplest oracle stores the bits plainly. For every (i\in[0,n]), recompute rank by scanning (B[0..i)). Enumerate zero and one positions for select. Exhaustive small-vector tests should cover all (2^n) patterns for feasible (n); larger tests generate uniform, sparse, dense, clustered, alternating, periodic, and adversarial boundary patterns.

Properties include rank endpoints, unit increments, rank-zero complement, select monotonicity, access at select, both inverse identities, total counts, and agreement before/after serialization. Test lengths around word, block, superblock, page, and counter-width boundaries. Corrupt headers, offsets, counters, and padding deliberately.

Benchmark access/rank/select-zero/select-one separately across hit ordinals, densities, clustering, sizes, warm/cold caches, random/batched/sequential queries, mapped/resident data, platforms, and compiler flags. Report payload, directories, tables, allocator/file bytes, build peak, construction/load time, throughput, and latency distributions. Compare against a plain bit vector plus simple prefix counts under equal semantics.

The bounded model below builds explicit two-level directories for a 32-bit string. Rank uses directory counts plus a residual scan; select binary-searches rank. Those residual and select methods are intentionally not constant-time succinct implementations. The model verifies semantics and directory accounting only.

<!-- bijux-verify: {"id":"rank-select-directory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"bits=10110010100011101001011000101101\nlength=32\nones=16\nzeros=16\nsuperblock_size=8\nblock_size=4\nsuperblock_counts=[0, 4, 8, 12, 16]\nblock_counts=[0, 3, 0, 1, 0, 2, 0, 1, 0]\nrank1_0=0\nrank1_8=4\nrank1_17=9\nrank1_32=16\nrank0_17=8\nselect1_0=0\nselect1_7=14\nselect1_15=31\nselect0_0=1\nselect0_7=15\ninverses_hold=True\nvalid=True\nevidence=two_level_rank_select_model\n","stderr":""}} -->
```python
BITS = "10110010100011101001011000101101"
SUPERBLOCK_SIZE = 8
BLOCK_SIZE = 4

prefix_ones = [0]
for bit in BITS:
    prefix_ones.append(prefix_ones[-1] + (1 if bit == "1" else 0))

superblock_counts = [
    prefix_ones[offset]
    for offset in range(0, len(BITS) + 1, SUPERBLOCK_SIZE)
]
block_counts = [
    prefix_ones[offset]
    - prefix_ones[(offset // SUPERBLOCK_SIZE) * SUPERBLOCK_SIZE]
    for offset in range(0, len(BITS) + 1, BLOCK_SIZE)
]


def rank1(position):
    superblock = position // SUPERBLOCK_SIZE
    block = position // BLOCK_SIZE
    block_start = block * BLOCK_SIZE
    residual = sum(
        1
        for bit in BITS[block_start:position]
        if bit == "1"
    )
    return superblock_counts[superblock] + block_counts[block] + residual


def rank(bit, position):
    if bit == "1":
        return rank1(position)
    return position - rank1(position)


def select(bit, occurrence):
    target = occurrence + 1
    left = 0
    right = len(BITS) - 1
    while left < right:
        middle = (left + right) // 2
        if rank(bit, middle + 1) >= target:
            right = middle
        else:
            left = middle + 1
    return left


ones = rank1(len(BITS))
zeros = len(BITS) - ones
inverses_hold = all(
    BITS[select(bit, occurrence)] == bit
    and rank(bit, select(bit, occurrence)) == occurrence
    and rank(bit, select(bit, occurrence) + 1) == occurrence + 1
    for bit, total in (("0", zeros), ("1", ones))
    for occurrence in range(total)
)
valid = (
    prefix_ones[-1] == ones
    and superblock_counts == [0, 4, 8, 12, 16]
    and block_counts == [0, 3, 0, 1, 0, 2, 0, 1, 0]
    and inverses_hold
)

print(f"bits={BITS}")
print(f"length={len(BITS)}")
print(f"ones={ones}")
print(f"zeros={zeros}")
print(f"superblock_size={SUPERBLOCK_SIZE}")
print(f"block_size={BLOCK_SIZE}")
print(f"superblock_counts={superblock_counts}")
print(f"block_counts={block_counts}")
print(f"rank1_0={rank1(0)}")
print(f"rank1_8={rank1(8)}")
print(f"rank1_17={rank1(17)}")
print(f"rank1_32={rank1(32)}")
print(f"rank0_17={rank('0', 17)}")
print(f"select1_0={select('1', 0)}")
print(f"select1_7={select('1', 7)}")
print(f"select1_15={select('1', 15)}")
print(f"select0_0={select('0', 0)}")
print(f"select0_7={select('0', 7)}")
print(f"inverses_hold={inverses_hold}")
print(f"valid={valid}")
print("evidence=two_level_rank_select_model")
```

## Definitions and Notation

- (B[0..n)): logical bit vector of length (n), excluding physical padding.
- `access(i)`: bit (B[i]), valid for (0\le i<n).
- (operatorname{rank}_b(i)): count of bit (b) in half-open prefix (B[0..i)).
- (operatorname{select}_b(t)): position of zero-based occurrence (t) of bit (b).
- (m=operatorname{rank}_1(n)): number of one-bits; (n-m): zero-bits.
- **Redundancy:** bits beyond the chosen information baseline needed to support operations.
- **Superblock/block:** coarse/fine rank-directory regions.
- **Inventory/sample:** stored select position for a periodic occurrence ordinal.
- **Class/offset:** RRR block population and identifier among same-population patterns.
- **Word RAM:** model with word size (w=\Omega(\log n)) and declared constant-time word operations.
- **Generation:** immutable logical bits, supports, layout parameters, and checksums published together.

## Mechanisms, Invariants, or Proof Structure

### Rank-space derivation

Superblock counters use (O((n/s)\log n)=O(n/\log n)) bits for (s=\Theta(\log^2n)). Block-relative counters use (O((n/b)\log s)=O(n\log\log n/\log n)) bits for (b=\Theta(\log n)). A residual universal table with (2^{(\log n)/2}=\sqrt n) patterns and polylogarithmic metadata is (o(n)). Each term divided by (n) tends to zero.

### Semantic inverses

If (p=\operatorname{select}_b(t)), exactly (t) occurrences precede (p), (B[p]=b), and exactly (t+1) occur before (p+1). Conversely, if (B[i]=b), then (operatorname{select}_b(\operatorname{rank}_b(i))=i). These statements depend on half-open rank and zero-based select.

### Systems invariants

- logical length and final-word mask exclude padding from counts;
- every directory entry equals the oracle prefix at its boundary;
- counters and offsets cannot overflow or address outside their declared section;
- mapped/query code interprets byte order, bit order, widths, and conventions identically;
- data and supports share one checksum-bound immutable generation;
- dynamic edits atomically preserve subtree lengths/counts or remain invisible to readers.

## Alternatives and Trade-Offs

A plain packed vector plus no support minimizes static payload but makes rank/select scan. A full prefix-count array offers constant-time rank with large word-level space and does not directly solve select. Two-level plain supports preserve (n+o(n)) theory and often fast rank. RRR reduces space near density entropy but decodes blocks. Sparse/Elias–Fano forms excel when one bit value is rare; run-length forms excel on clustering; chunked bitmap formats favor mutation and set algebra; balanced chunk trees support dynamic rank/select.

Select-heavy and rank-heavy workloads may choose different supports over the same bits. A downstream wavelet tree may use representation per node based on density. Favor the simplest measured format satisfying total space, construction, mapping, mutation, and tail-latency constraints.

## Failure Modes and Misconceptions

- **Rank at (i) always includes (B[i]).** This chapter uses (B[0..i)); verify every API.
- **Select occurrence one is the first.** This chapter's first occurrence is zero.
- **(O(n)) space means succinct.** The hidden unit may be machine words.
- **The source bits are the whole footprint.** Directories, tables, padding, headers, and build peak count.
- **Little-(o) means small at every practical (n).** Constants and field rounding can dominate.
- **Rank automatically provides constant-time select.** Rank-guided binary search is (O(\log n)).
- **Population count is universally constant and available.** Model and target ISA must be stated.
- **Padding zeros are logical zeros.** They are outside (B[0..n)).
- **Native serialization preserves layout.** ABI padding, byte order, and word size differ.
- **A static support tolerates bit flips.** Its later directory counts become stale.
- **Compressed means smaller for every distribution.** Metadata can exceed savings.
- **Correct random queries cover boundaries.** Word/block/superblock endpoints need directed tests.
- **A checksum proves semantics.** A consistently written but wrongly interpreted convention can still pass.

## Worked Examples

### Example 1

**Convention.** For `10110`, (operatorname{rank}_1(3)=2) because positions 0–2 contain two ones. One positions are 0, 2, 3, so (operatorname{select}_1(2)=3). **Conclusion:** writing the prefix and ordinal convention prevents an off-by-one argument.

### Example 2

**Inverse.** At (p=14) in the fixture, bit 1 is occurrence (t=7). Therefore (operatorname{rank}_1(14)=7) and (operatorname{rank}_1(15)=8). **Conclusion:** both sides of the selected position are useful test oracles.

### Example 3

**Padding.** A 65-bit vector stored in two 64-bit words has 63 unused high positions in its final word. Counting the raw second word without masking can invent zeros or ones. **Conclusion:** logical length governs every operation.

### Example 4

**Directory query.** Fixture rank at 17 uses superblock count 8 at position 16, block-relative count 0, and residual bit `1`, yielding 9. **Conclusion:** coarse count, fine count, and residual partition the prefix without overlap.

### Example 5

**Sparse information.** A million-bit vector with ten ones has a tiny density-sensitive information bound compared with one million raw bits. Explicit 64-bit positions take only 640 bits before headers, though select/rank trade-offs remain. **Conclusion:** choose by distribution and operations, not raw length alone.

### Example 6

**Dense complement.** A vector with ten zeros among a million positions should often store zero positions and derive (operatorname{rank}_1(i)=i-operatorname{rank}_0(i)). **Conclusion:** sparse value choice can be inverted.

### Example 7

**Counter overflow.** A 32-bit global rank counter wraps after (2^{32}-1) ones even if file offsets are 64-bit. **Conclusion:** counter width follows logical maximum, not address type by association.

### Example 8

**Static mutation.** Flipping position 12 from zero to one requires every later global prefix summary to increase. A raw-bit-only write makes rank silently wrong. **Conclusion:** rebuild, dynamic propagation, or immutable delta is required.

### Example 9

**Mapped corruption.** A select inventory offset points beyond its section but within the mapped file. Bounds-free arithmetic reads another structure as positions. **Conclusion:** validate section-relative offsets before query publication.

### Example 10

**Null bitmap.** A row column has non-null bits `10110`; rank-one before row 4 is three, so row 4's value, if non-null, maps to dense payload ordinal three. **Conclusion:** a rank convention defines physical column addressing.

## Cross-Program Connections

- **Algorithms and Theory:** information bounds, word-RAM assumptions, lower-order redundancy, and predecessor search frame guarantees.
- **Database Engineering:** null maps, bitmap indexes, column selection, mapped files, checksums, and snapshots use rank/select.
- **Information Retrieval:** FM-indexes, compressed postings, document arrays, and suffix structures compose the primitives.
- **Graph Engineering:** LOUDS, balanced parentheses, and adjacency delimiters replace pointers with bit navigation.
- **Systems Programming:** ISA dispatch, masks, overflow, endianness, ABI layout, NUMA, and memory mapping control correctness/performance.
- **Testing and Verification:** exhaustive small patterns and algebraic inverse properties offer unusually strong differential evidence.

## References

1. Guy Jacobson, [Succinct Static Data Structures](https://csd.cs.cmu.edu/academics/doctoral/degrees-conferred/guy-jacobson), PhD thesis, Carnegie Mellon University, 1988.
2. Rajeev Raman, Venkatesh Raman, and Srinivasa Rao Satti, [Succinct Indexable Dictionaries with Applications to Encoding k-ary Trees, Prefix Sums and Multisets](https://arxiv.org/abs/0705.0552), *ACM Transactions on Algorithms*, 2007.
3. Gonzalo Navarro, [Compact Data Structures: A Practical Approach](https://users.dcc.uchile.cl/~gnavarro/CDSbook/), Cambridge University Press, 2016.
4. Gonzalo Navarro and Eliana Providel, [Fast, Small, Simple Rank/Select on Bitmaps](https://www.dcc.uchile.cl/~gnavarro/ps/sea12.1.pdf), *SEA*, 2012.
5. Florian Kurpicz, [Engineering Compact Data Structures for Rank and Select Queries on Bit Vectors](https://arxiv.org/abs/2206.01149), *SPIRE*, 2022.
6. Simon Gog, Timo Beller, Alistair Moffat, and Matthias Petri, [From Theory to Practice: Plug and Play with Succinct Data Structures](https://arxiv.org/abs/1311.1249), *SEA*, 2014.
7. Simon Gog et al., [SDSL-lite: Succinct Data Structure Library](https://github.com/simongog/sdsl-lite), accessed 2026-08-30.

## Exercises

### Exercise 1

For `B=011010011`, compute (operatorname{rank}_1(i)) for (i=0,4,9), all (operatorname{select}_1(t)), and all (operatorname{select}_0(t)) under this chapter's convention. Verify inverses.

### Exercise 2

Derive why superblocks of (Theta(\log^2n)), blocks of (Theta(\log n)), and residual tables for half-logarithmic blocks add (o(n)) bits. State the computational-model assumptions.

### Exercise 3

For one billion bits, compare 125 MB of packed payload with a 64-bit prefix counter per bit. Estimate packed two-level directory bytes using 4,096-bit superblocks with 64-bit counts and 64-bit blocks with 13-bit relative counts. Ignore ceilings for the estimate and list omissions.

### Exercise 4

Choose representations for: uniform half-dense static bits, ten thousand ones among a billion positions, long alternating runs, and a bitmap with frequent inserts/deletes. Define required benchmarks.

### Exercise 5

Design a portable immutable rank/select file format and its validation, atomic publication, corruption testing, and cross-implementation differential suite.

## Answers to the Exercises

### Answer 1

Prefixes give (operatorname{rank}_1(0)=0), (operatorname{rank}_1(4)=2) for `0110`, and (operatorname{rank}_1(9)=5). One positions are `[1,2,4,7,8]`; zero positions are `[0,3,5,6]`. For each list position (p) at ordinal (t), the bit matches, rank before (p) is (t), and rank before (p+1) is (t+1).

### Answer 2

There are (n/\Theta(\log^2n)) global counters of (Theta(\log n)) bits, totaling (O(n/\log n)). There are (n/\Theta(\log n)) local counters of (O(\log\log n)) bits, totaling (O(n\log\log n/\log n)). With residual length (b=\tfrac12\log n), (2^b=\sqrt n); storing polylogarithmic answers per pattern remains (o(n)). All ratios to (n) tend to zero. Constant query time assumes a word RAM with (w=\Omega(\log n)), constant-time indexed word access/arithmetic/masking and either population count or a shared addressable table whose space is included.

### Answer 3

A counter per bit costs (10^9\cdot8=8) GB, 64 times the 125 MB payload. Superblock counts cost approximately ((10^9/4096)\cdot8=1.953125) MB. Relative block counts cost ((10^9/64)\cdot13/8\approx25.390625) MB. The approximate directory is 27.34375 MB, so payload plus these two terms is about 152.34 MB. Omitted terms include ceilings/sentinels, residual implementation/tables, select supports, section alignment, headers/checksums, allocator or file-system rounding, construction workspace, and mappings.

### Answer 4

Use a plain packed vector with practical rank/select support for unpredictable half density; a sparse monotone-position/Elias–Fano-style form for ten thousand ones; run-length or hybrid blocks for long runs; and a balanced chunk tree or chunked mutable bitmap for frequent positional updates. Benchmark access/rank/select for both bits, iteration and set operations if required, final and peak build/update space, update latency, random/batched/cache-cold queries, density/run distributions, serialization/load, and downstream end-to-end operations. Compare with plain packed and simple prefix baselines under identical conventions.

### Answer 5

The header declares magic/schema, logical length, totals, bit/byte order, representation, word-independent encoding, rank/select convention, block/sample parameters, counter widths, section offsets/lengths, and per-section/root checksums. Readers checked-arithmetic every range, reject overlap/out-of-file offsets and unsupported features, mask final padding, recompute totals and sampled directories, validate select monotonicity/range, then run boundary probes before publication. Writers construct private files, flush payload/supports and checksums, and atomically replace one generation manifest with rollback. Tests flip every header class, truncate sections, corrupt counters/offsets/padding, and simulate crashes before/after publication. Differential tests enumerate small bit patterns and compare large randomized/adversarial vectors across the simple oracle, writer, independent reader, serialization round trip, platforms, and supported ISA paths.
