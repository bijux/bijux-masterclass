---
module_id: DSE-092
program: Data Structures Engineering
level: 2
module_number: 92
title: Wavelet Trees
status: complete
last_verified: 2026-08-30
---

# Wavelet Trees

## One-Page Review

### Governing question

How can rank/select bit vectors recursively represent a sequence over a larger alphabet while supporting access, symbol rank/select, and range order statistics without materializing per-symbol position lists?

### Essential definitions

Let (S[0..n)) use ordered alphabet (Sigma), (|\Sigma|=\sigma). A balanced wavelet tree recursively partitions the alphabet. Each internal node stores, in original relative order, a bit indicating whether each routed symbol belongs to its left or right alphabet subset. Stable routing makes a prefix at a parent map to a prefix at its child using bit rank.

This chapter inherits [DSE-091](091-bit-vectors-with-rank-and-select.md): (operatorname{rank}_b(B,i)) counts (b) in (B[0..i)), and (operatorname{select}_b(B,t)) returns the position of zero-based occurrence (t). Sequence rank is (operatorname{rank}_c(S,i)); sequence select returns the zero-based (t)-th (c).

### Central model, mechanism, or theorem

For access at position (i), read the node bit (b=B[i]), append that branch to the symbol code, and map (i\leftarrow\operatorname{rank}_b(B,i)). For rank of known symbol (c), follow (c)'s branches and map prefix endpoint the same way. Select reverses from leaf to root via bit select.

A balanced binary shape has height (lceil\log_2\sigma\rceil), stores about (n\lceil\log_2\sigma\rceil) routing bits, and supports basic operations in (O(\log\sigma)) bit-vector queries. Entropy-shaped or compressed bit vectors can reduce space under stated models. Wavelet matrices store one bitmap per level with stable zero/one partitions and offsets, improving layout while changing navigation formulas.

### Critical invariants

- Alphabet order, symbol-to-code mapping, shape, code width, and generation are immutable query metadata.
- Routing is stable: relative order among symbols taking the same branch is preserved.
- Each node bitmap length equals the subsequence routed to that node; each level totals (n) bits for a full balanced shape.
- Prefix mappings use the same half-open rank convention at every level.
- Select reverses the exact forward path with correct node or level offsets.
- Range endpoints remain half-open and satisfy (0\le l\le r\le n) after every mapping.
- Padding codes for non-power-of-two alphabets never decode as live symbols.
- Serialized bitmaps, rank/select supports, offsets, alphabet, and checksums publish atomically.

### Common failures

Failures include unstable partitioning, mixing inclusive rank into child mapping, omitting zero offsets in a wavelet matrix, applying tree formulas to matrix layout, using lexical byte order when the domain requires numeric/collation order, decoding unused codes, confusing occurrence rank with position, reversing select levels incorrectly, reporting (n\log\sigma) bits without support metadata, using Huffman shape without storing the codebook, and mutating the sequence beneath static bitmaps.

### Compact example

With alphabet `[$,A,B,N]` coded `00,01,10,11`, sequence `BANANA$` produces wavelet-matrix bitmaps `1010100` then `1110011`; zero counts are `[4,2]`, and stable final order is `$BAAANN`. Access reconstructs `BANANA$`; rank totals are 1/3/1/2; select positions for A are `[1,3,5]`; and the zero-based third order statistic of `S[1..6)=ANANA` is N. A sorted subrange oracle agrees.

### Connections

[DSE-091](091-bit-vectors-with-rank-and-select.md) provides every navigation primitive. The roadmap successor is [DSE-093, “Succinct Trees and Graphs”](../ROADMAP.md), where bit encodings navigate topology. Wavelet trees also connect to FM-indexes, compressed suffix arrays, inverted indexes, columnar range analytics, geometric point grids, and graph labels.

## Governing Question

How should a wavelet tree or matrix be shaped, built, queried, compressed, serialized, and validated so that recursive rank/select composition remains correct and its space/time claims remain reproducible?

## Why This Matters

Storing a position list for every symbol answers select well but duplicates navigation state and handles range order statistics poorly. A wavelet tree factors the alphabet into binary decisions. At each level, rank translates coordinates into a smaller subsequence while preserving order; reversing with select returns to original coordinates.

The structure is versatile precisely because its invariants compose. One off-by-one or unstable partition at an early level silently redirects all later operations. Practical engineering must bind bit-vector conventions, alphabet encoding, layout variant, compression, and persistence into one testable contract.

## Prerequisites and Retrieval

Retrieve:

- bit-vector access/rank/select and inverse laws from [DSE-091](091-bit-vectors-with-rank-and-select.md);
- stable partition, binary codes, balanced/Huffman trees, prefix codes, entropy, and logarithms;
- half-open ranges, order statistics, quantiles, frequency, predecessor/successor, and range counting;
- packed arrays, level offsets, memory mapping, immutable generations, checksums, and overflow safety;
- differential/property testing with plain sequence and sorted-subrange oracles.

The mathematical “wavelet” name does not make this a numeric signal transform. It is a hierarchical sequence/index representation built from routing bitmaps.

## Learning Objectives

After this chapter, you should be able to:

1. construct balanced wavelet-tree node sequences by stable alphabet partition;
2. derive access, rank, and reverse-select mappings under half-open conventions;
3. implement range quantile and frequency/range counting by mapped endpoints;
4. distinguish pointer tree, levelwise tree, wavelet matrix, Huffman-shaped, and multiary layouts;
5. account for routing bits, rank/select supports, codebooks, offsets, padding, and build peak;
6. design static/dynamic construction, serialization, mapping, and corruption validation;
7. verify every operation against plain and sorted-range oracles across adversarial alphabets.

## Core Exposition

### Stable recursive partition

At a node owning alphabet interval (A), split it into ordered subsets (A_0,A_1). Scan the node subsequence. Emit 0 for a symbol in (A_0), 1 for (A_1), and stably append the symbol to the corresponding child subsequence. Repeat until a leaf names one symbol.

Stability is the key invariant. If the first (i) parent symbols contain (z) zeros, those symbols become exactly the first (z) items of the left child. Therefore the parent prefix endpoint maps to (operatorname{rank}_0(B,i)). Reordering equal-branch symbols may preserve counts at one node but destroys their coordinate identity downstream.

Balanced splitting by alphabet cardinality gives height (lceil\log_2\sigma\rceil); if (sigma) is not a power of two, some codes or leaves are unused/shallower. Splitting by value midpoint supports ordered queries naturally. Splitting by frequency/Huffman codes reduces average depth but complicates range-by-value traversal and requires a persisted code/tree.

### Access, rank, and select

For access, start at root position (i). At node bitmap (B), observe (b=B[i]), choose child (b), and set (i=\operatorname{rank}_b(B,i)). The leaf identifies the symbol. Inductively, (i) remains the ordinal of the original item among elements routed along that prefix.

For (operatorname{rank}_c(S,i)), the path is already determined by (c). Start with endpoint (i) and replace it by (operatorname{rank}_{b_c}(B,i)) at each node. At (c)'s leaf, the endpoint equals occurrences of (c) in the original prefix.

For (operatorname{select}_c(S,t)), start with occurrence ordinal (t) at (c)'s leaf. Walk upward. If the child is branch (b), set (t=\operatorname{select}_b(B,t)). At the root, (t) is the original position. Each reverse step uses the exact bitmap and code path used forward.

Conventions matter twice: bit-vector select occurrence numbering and sequence select numbering. Validity also requires (t<\operatorname{rank}_c(S,n)); a sentinel must not collide with position zero.

### Range quantile and counting

For range (S[l..r)), a node's zero count is

\[
z=\operatorname{rank}_0(B,r)-\operatorname{rank}_0(B,l).
\]

If zero-based desired order (k<z), descend left and map both endpoints with rank-zero. Otherwise set (k\leftarrow k-z), descend right, and map endpoints with rank-one. The leaf is the range quantile. The range must be nonempty and (0\le k<r-l).

Range frequency of symbol (c) is (operatorname{rank}_c(S,r)-\operatorname{rank}_c(S,l)). Counting values in an alphabet interval recursively accepts fully covered nodes, rejects disjoint nodes, and maps endpoints for partial children. Predecessor/successor and report operations similarly prune by value interval while maintaining sequence ranges.

These algorithms are order-sensitive. If alphabet codes use UTF-8 bytes, locale collation or numeric order is not implied. Persist a canonical domain order and normalization version.

### Wavelet matrix

A pointer wavelet tree stores separate bitmaps per node. A levelwise layout concatenates them. The wavelet matrix instead stores one bitmap per bit level and stably places all zeros before ones for the next level. It records zero count (Z_\ell). Mapping becomes

\[
i'=
\begin{cases}
\operatorname{rank}_0(B_\ell,i),&b=0,\\
Z_\ell+\operatorname{rank}_1(B_\ell,i),&b=1.
\end{cases}
\]

Access and rank descend these global level arrays. Select reverses and subtracts (Z_\ell) before select-one. Final stable code groups or per-symbol starts locate a symbol's occurrence interval. Matrix and tree bitmaps may look similar, but node boundaries and offsets differ; formulas are not interchangeable.

The matrix offers contiguous per-level storage and avoids many small node objects, especially for large alphabets. Code assignment, padding codes, final starts, and range-order semantics must match the implementation variant.

### Space and shape

For fixed-width balanced codes of (h=\lceil\log_2\sigma\rceil), every sequence item contributes one bit per level, so routing payload is (nh) bits. Succinct rank/select support adds lower-order redundancy per bitmap/level under its assumptions. Alphabet map, shape/codebook, level offsets, zero counts, symbol starts, headers, alignment, and construction workspace are additional.

Compressing node bitmaps can make the total approach (nH_0(S)) plus lower-order terms for suitable shapes/supports. The identity arises because binary partition entropies decompose the alphabet entropy. This is not a promise that every library configuration or small input is below plain (n\log\sigma) space.

Huffman-shaped trees give expected operation depth related to code lengths and can approach entropy with plain node bitmaps. Balanced shapes give worst-case logarithmic depth and simpler ordered range traversal. Multiary nodes reduce height but require rank/select over larger alphabets or multiple bitmaps and increase tables/branching.

### Construction and updates

A straightforward builder repeatedly stable-partitions arrays, using (O(nh)) time and potentially (O(n)) scratch per level. Ping-pong buffers bound scratch while streaming bitmap output. Histogram/prefix offsets can build matrix levels without node objects. Large external-memory builds partition runs, preserve global stability, and checksum every level before publication.

Record input snapshot and symbol dictionary before encoding. Parallel partitioning must compute per-worker zero/one offsets so concatenation remains globally stable; naïvely appending worker outputs in completion order is wrong. Measure final size and peak buffers independently.

Static wavelet structures cannot accept positional insertion without shifting routing sequences on a root-to-leaf path. Dynamic variants use dynamic bit vectors and maintain shape/dictionary metadata, paying extra space and polylogarithmic updates. Append-only systems can keep immutable segments plus a mutable tail and merge later; queries combine per-segment ranks/counts with explicit global ordering.

### Persistence and validation

A durable envelope includes schema, logical length, symbol count/order/encoding, shape/layout kind, code width/tree, level/node directory, bitmap and support sections, zero counts, final symbol starts, rank/select convention, byte/bit order, section bounds, totals, and checksums. Do not serialize pointers or native rank-support references.

Validate all checked offset arithmetic, level lengths, zero counts, final group sizes, code validity, padding, and support samples before mapping. Reconstruct sampled access positions and compare symbol histograms. A corrupted rank directory can stay in-bounds while returning plausible wrong answers, so checksum plus semantic sentinels are useful.

Publish all levels and metadata as one immutable generation after durable writes. Readers pin a generation. Crash tests cover each level, dictionary, support, checksum, and root-manifest boundary. Cross-version migrations rebuild or use an explicitly compatible reader; guessing layout from section sizes is unsafe.

### Performance and verification

Operation cost is height times bit-vector cost, but cache layout and branch behavior dominate constants. Benchmark access, rank by frequent/rare symbol, select by early/late ordinal, quantiles by range length/order, and value-range counts. Vary alphabet size, entropy, skew, runs, input size, cache state, mapping, batch order, and query distribution.

Use a plain sequence oracle: access indexes directly; rank scans prefixes; select enumerates positions; quantile sorts the requested subrange; range count filters it. Exhaust all short sequences over small alphabets, then fuzz skewed, missing-code, non-power-of-two, singleton, Unicode-normalized, minimum/maximum, and adversarial boundary cases.

Properties include full access reconstruction, rank totals equal histograms, select/rank inverses, range frequency equals rank difference, every quantile agrees with sorting, and tree/matrix variants agree under one code order. Round-trip serialization and independent readers must preserve these results.

The bounded model below constructs a two-level wavelet matrix over `BANANA$` with fixed sorted alphabet. Its rank/select helpers scan Python strings, so it demonstrates routing semantics rather than succinct space or constant-time bit operations.

<!-- bijux-verify: {"id":"wavelet-matrix-routing","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"sequence=BANANA$\nalphabet=['$', 'A', 'B', 'N']\ncode_width=2\nlevel_bits=['1010100', '1110011']\nzero_counts=[4, 2]\nfinal_order=$BAAANN\nreconstructed=BANANA$\nrank_totals={'$': 1, 'A': 3, 'B': 1, 'N': 2}\nselect_positions={'$': [6], 'A': [1, 3, 5], 'B': [0], 'N': [2, 4]}\nrange=(1, 6)\nrange_values=ANANA\nquantile_order=3\nquantile=N\nquantile_oracle=N\nrank_select_inverses=True\nvalid=True\nevidence=bounded_wavelet_matrix_model\n","stderr":""}} -->
```python
SEQUENCE = "BANANA$"
ALPHABET = sorted(set(SEQUENCE))
CODE = {symbol: index for index, symbol in enumerate(ALPHABET)}
CODE_WIDTH = 2


def rank_bit(bits, bit, position):
    return bits[:position].count(bit)


def select_bit(bits, bit, occurrence):
    positions = [
        index
        for index, value in enumerate(bits)
        if value == bit
    ]
    return positions[occurrence]


current = list(SEQUENCE)
level_bits = []
zero_counts = []
for shift in (1, 0):
    bits = "".join(
        str((CODE[symbol] >> shift) & 1)
        for symbol in current
    )
    level_bits.append(bits)
    zero_counts.append(bits.count("0"))
    current = (
        [symbol for symbol, bit in zip(current, bits) if bit == "0"]
        + [symbol for symbol, bit in zip(current, bits) if bit == "1"]
    )

final_starts = {
    symbol: current.index(symbol)
    for symbol in ALPHABET
}


def access(position):
    code = 0
    for bits, zeros in zip(level_bits, zero_counts):
        bit = bits[position]
        code = (code << 1) | int(bit)
        position = rank_bit(bits, bit, position)
        if bit == "1":
            position += zeros
    return ALPHABET[code]


def rank_symbol(symbol, position):
    left = 0
    right = position
    code = CODE[symbol]
    for level, (bits, zeros) in enumerate(zip(level_bits, zero_counts)):
        shift = CODE_WIDTH - 1 - level
        bit = str((code >> shift) & 1)
        left = rank_bit(bits, bit, left)
        right = rank_bit(bits, bit, right)
        if bit == "1":
            left += zeros
            right += zeros
    return right - left


def select_symbol(symbol, occurrence):
    position = final_starts[symbol] + occurrence
    code = CODE[symbol]
    for level in range(CODE_WIDTH - 1, -1, -1):
        shift = CODE_WIDTH - 1 - level
        bit = str((code >> shift) & 1)
        if bit == "1":
            position -= zero_counts[level]
        position = select_bit(level_bits[level], bit, position)
    return position


def range_quantile(left, right, order):
    code = 0
    for bits, zeros in zip(level_bits, zero_counts):
        left_zero = rank_bit(bits, "0", left)
        right_zero = rank_bit(bits, "0", right)
        zero_count = right_zero - left_zero
        if order < zero_count:
            left = left_zero
            right = right_zero
            code <<= 1
        else:
            order -= zero_count
            left = zeros + rank_bit(bits, "1", left)
            right = zeros + rank_bit(bits, "1", right)
            code = (code << 1) | 1
    return ALPHABET[code]


reconstructed = "".join(access(index) for index in range(len(SEQUENCE)))
rank_totals = {
    symbol: rank_symbol(symbol, len(SEQUENCE))
    for symbol in ALPHABET
}
select_positions = {
    symbol: [
        select_symbol(symbol, occurrence)
        for occurrence in range(SEQUENCE.count(symbol))
    ]
    for symbol in ALPHABET
}
left, right, order = 1, 6, 3
quantile = range_quantile(left, right, order)
quantile_oracle = sorted(SEQUENCE[left:right])[order]
inverses = all(
    SEQUENCE[position] == symbol
    and rank_symbol(symbol, position) == occurrence
    and rank_symbol(symbol, position + 1) == occurrence + 1
    for symbol, positions in select_positions.items()
    for occurrence, position in enumerate(positions)
)
valid = (
    reconstructed == SEQUENCE
    and rank_totals == {"$": 1, "A": 3, "B": 1, "N": 2}
    and quantile == quantile_oracle == "N"
    and inverses
)

print(f"sequence={SEQUENCE}")
print(f"alphabet={ALPHABET}")
print(f"code_width={CODE_WIDTH}")
print(f"level_bits={level_bits}")
print(f"zero_counts={zero_counts}")
print(f"final_order={''.join(current)}")
print(f"reconstructed={reconstructed}")
print(f"rank_totals={rank_totals}")
print(f"select_positions={select_positions}")
print(f"range={(left, right)}")
print(f"range_values={SEQUENCE[left:right]}")
print(f"quantile_order={order}")
print(f"quantile={quantile}")
print(f"quantile_oracle={quantile_oracle}")
print(f"rank_select_inverses={inverses}")
print(f"valid={valid}")
print("evidence=bounded_wavelet_matrix_model")
```

## Definitions and Notation

- (S[0..n)): sequence over ordered alphabet (Sigma), (|\Sigma|=\sigma).
- **Node subsequence:** stable projection of original symbols routed to one node.
- **Routing bitmap:** zero/one decisions for a node or matrix level.
- (operatorname{rank}_c(S,i)): occurrences of (c) in (S[0..i)).
- (operatorname{select}_c(S,t)): original position of zero-based occurrence (t) of (c).
- **Range quantile:** zero-based (k)-th smallest symbol of (S[l..r)).
- (Z_\ell): number of zeros in wavelet-matrix level (ell).
- **Stable partition:** preserves relative order within each branch.
- **Shape/codebook:** alphabet-to-root-path mapping for a tree variant.
- **Generation:** atomic sequence metadata, routing data, supports, offsets, and checksums.

## Mechanisms, Invariants, or Proof Structure

### Coordinate induction

At every depth, a mapped position is the ordinal of the original item among symbols sharing its path prefix. Stable partition and half-open rank preserve this invariant. Thus access reaches the correct leaf and known-symbol rank ends at the prefix occurrence count.

### Select inversion

Forward mapping sends parent ordinal (i) on branch (b) to (operatorname{rank}_b(B,i)), with a matrix zero offset for branch one. Bit select is the inverse on occurrences; reversing levels and offsets therefore returns the original coordinate.

### Range-order invariant

Mapped endpoints describe exactly the original range's items routed to a node. Their zero-rank difference counts left items. Subtracting that count only when choosing right preserves the desired order statistic.

System invariants require stable construction, valid codes, per-level length/totals, bounded offsets, convention agreement, and one immutable checksum-bound generation.

## Alternatives and Trade-Offs

Per-symbol position lists make select direct and rank searchable but duplicate dictionaries and do not naturally support range quantiles. Prefix-count tables are fast and large. Balanced wavelet trees offer worst-case (O(\log\sigma)) depth; Huffman shapes reduce expected depth; wavelet matrices improve level locality; multiary variants reduce height; compressed bitmaps exploit skew; dynamic variants support edits with more overhead.

Use exact arrays for small alphabets/data, inverted lists for posting-centric workloads, or range trees for multidimensional needs. Choose by required operations, order semantics, entropy, updates, mapping, and measured cache behavior.

## Failure Modes and Misconceptions

- Unstable partition destroys coordinate mapping.
- Inclusive rank shifts every child endpoint.
- Wavelet-tree and wavelet-matrix offsets are not interchangeable.
- Select must reverse levels and subtract matrix offsets.
- Code order defines quantile order; locale/numeric order is not automatic.
- Unused fixed-width codes must not decode as symbols.
- Huffman shape needs persisted canonical code metadata.
- (n\log\sigma) excludes supports, dictionaries, padding, and build peak.
- Compressed bitmaps are not smaller for every finite distribution.
- Static bitmaps cannot be edited underneath their supports.
- Correct access alone does not prove rank/select/range correctness.
- Deserialization success does not validate stable layout or offsets.

## Worked Examples

### Example 1

**Stable root.** `BANANA$` emits `1010100`; zeros stably become `AAA$`, ones `BNN`. **Conclusion:** branch order is preserved.

### Example 2

**Access.** Position 2 reads one at both levels, code `11`, hence N. **Conclusion:** rank-mapped ordinals reconstruct the symbol.

### Example 3

**Prefix rank.** In `BANAN`, N occurs twice, so (operatorname{rank}_N(5)=2). **Conclusion:** leaf endpoint is the occurrence count.

### Example 4

**Select.** A occurrence 1 maps back to original position 3. Rank-A before/through it is 1/2. **Conclusion:** reverse mapping satisfies both inverse checks.

### Example 5

**Quantile.** `ANANA` sorts to `AAANN`; zero-based order 3 is N. **Conclusion:** branch counts avoid sorting at query time.

### Example 6

**Range frequency.** A in `[1,6)` is (operatorname{rank}_A(6)-\operatorname{rank}_A(1)=3). **Conclusion:** two prefix mappings answer a range count.

### Example 7

**Missing power-of-two code.** Five symbols need three bits but leave three unused codes. **Conclusion:** decoder validates leaf/code membership.

### Example 8

**Huffman shape.** A frequent symbol gets a shorter path, lowering average query depth but complicating value intervals. **Conclusion:** shape changes workload cost and supported traversal.

### Example 9

**Parallel build.** Workers append stable partitions in completion order and scramble global order. Prefix-calculated worker offsets repair it. **Conclusion:** local stability is insufficient.

### Example 10

**Corrupt zero count.** One wrong (Z_\ell) keeps addresses in bounds yet redirects every one-branch query. **Conclusion:** recompute semantic totals, not only checksums.

## Cross-Program Connections

- **Information Retrieval:** BWT/FM-index and document arrays use sequence rank/select.
- **Database Engineering:** compact columns answer range counts and quantiles.
- **Graph Engineering:** label sequences and binary relations become searchable grids.
- **Systems:** mapped levels, offsets, ISA-aware bitmaps, and immutable publication govern deployment.
- **Algorithms:** entropy, stable partition, order statistics, and prefix codes determine bounds.
- **Verification:** access reconstruction, inverse laws, and sorted-range oracles provide strong evidence.

## References

1. Roberto Grossi, Ankur Gupta, and Jeffrey Scott Vitter, [High-Order Entropy-Compressed Text Indexes](https://pages.di.unipi.it/grossi/PAPERS/sodaconf03FINAL-LATEST.pdf), *SODA*, 2003.
2. Gonzalo Navarro, [Wavelet Trees for All](https://users.dcc.uchile.cl/~gnavarro/ps/cpm12.pdf), *CPM*, 2012.
3. Francisco Claude and Gonzalo Navarro, [Practical Rank/Select Queries over Arbitrary Sequences](https://users.dcc.uchile.cl/~gnavarro/ps/spire08.1.pdf), *SPIRE*, 2008.
4. Francisco Claude, Gonzalo Navarro, and Alberto Ordóñez, [The Wavelet Matrix](https://arxiv.org/abs/1405.1220), *Information Systems*, 2015.
5. Travis Gagie, Gonzalo Navarro, and Simon J. Puglisi, [New Algorithms on Wavelet Trees and Applications to Information Retrieval](https://arxiv.org/abs/1011.4532), 2010.
6. Gonzalo Navarro, [Compact Data Structures](https://users.dcc.uchile.cl/~gnavarro/CDSbook/), Cambridge University Press, 2016.
7. Simon Gog et al., [SDSL-lite](https://github.com/simongog/sdsl-lite), accessed 2026-08-30.

## Exercises

### Exercise 1

Construct balanced routing bitmaps for `ABRACADABRA` under sorted fixed-width codes; trace one access, rank, and select.

### Exercise 2

Prove access/rank coordinate induction and select inversion under half-open, zero-based conventions.

### Exercise 3

Trace zero-based range quantile 3 for `BANANA$[1..6)` and derive range frequency for A.

### Exercise 4

Compare balanced tree, Huffman shape, and matrix for a skewed large alphabet, accounting for operations, space, and order queries.

### Exercise 5

Design a portable mapped wavelet-matrix format, builder, validator, atomic publication protocol, and differential test campaign.

## Answers to the Exercises

### Answer 1

Map sorted symbols A/B/C/D/R to fixed three-bit codes and stably partition at each bit. Access follows observed bits with rank-mapped positions; rank follows the known symbol code; select reverses its leaf ordinal. Validate all eleven accesses and position lists against the source rather than trusting a hand trace; unused codes 5–7 remain invalid.

### Answer 2

Induct on depth. Stability makes the first (i) parent items taking branch (b) exactly the first (operatorname{rank}_b(B,i)) child items, preserving the original item's ordinal. Access therefore reaches its code leaf; known-symbol rank yields its prefix count. Bit select uniquely maps a child occurrence ordinal to its parent position, so reversing each path step (and matrix offset) proves select inversion.

### Answer 3

The subrange is `ANANA`, sorted `AAANN`; order 3 is N. A appears three times. Equivalently, (operatorname{rank}_A(6)-\operatorname{rank}_A(1)=3-0=3). Each quantile step counts zeros between mapped endpoints, chooses left if the order is smaller, otherwise subtracts and chooses right.

### Answer 4

A balanced tree gives predictable (O(\log\sigma)) basic and ordered-query depth. Huffman shape lowers frequency-weighted depth and can improve compressed space but complicates value-range decomposition and persists a codebook. A matrix provides contiguous levels and simpler large-alphabet layout with zero offsets/final starts. Benchmark actual access/rank/select/range mixes, entropy/skew, supports, code metadata, build peak, mapping, and cache/tail latency before choosing.

### Answer 5

Persist schema, length, canonical alphabet/order, code width, level count, bit convention, each bitmap/support section, (Z_\ell), final starts, bounds, and checksums. Build stable levels with deterministic worker offsets into private files; validate lengths, totals, starts, padding, sampled access/rank/select/quantiles, and source histograms; flush then atomically publish one manifest. Differential tests exhaust small sequences and fuzz skew, missing codes, boundaries, corruption, truncation, platforms, serialization round trips, and crash points against plain and sorted-range oracles.
