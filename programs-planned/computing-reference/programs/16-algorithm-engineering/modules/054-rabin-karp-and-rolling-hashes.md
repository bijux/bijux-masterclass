---
module_id: ALGE-054
program: Algorithm Engineering
level: 2
module_number: 54
title: Rabin-Karp and Rolling Hashes
status: complete
last_verified: 2026-09-05
---

# Rabin-Karp and Rolling Hashes

## One-Page Review

### Governing question

How can a rolling fingerprint filter candidate windows in constant update time while exact verification, randomized parameters, and explicit arithmetic preserve honest correctness and probability claims?

### Essential definitions

- A **fingerprint** maps a long sequence to a smaller value; unequal sequences can collide.
- A **polynomial fingerprint** for $X[0:m]$ is $H(X)=\sum_{i=0}^{m-1}X[i]b^{m-1-i}\bmod q$.
- A **rolling hash** removes the outgoing symbol, shifts the remaining polynomial, and adds the incoming symbol in $O(1)$ arithmetic operations.
- A **candidate** is a text window whose fingerprint equals the pattern fingerprint.
- **Exact verification** compares the candidate window with the pattern symbol by symbol.
- A **false fingerprint hit** is a collision rejected by exact verification; a **false match** is an incorrect result returned when verification is omitted.
- A **Monte Carlo** matcher may return an incorrect result with bounded probability; a randomized, always-verified matcher remains exact but has input- and collision-dependent verification cost.
- A **universal hash family** randomizes the function so collision probability is bounded for any fixed unequal inputs.
- A **multi-pattern bucket** maps one fingerprint to every pattern with that value; exact verification must check all viable members.

### Central model, mechanism, or theorem

Let $h_s=H(T[s:s+m])$ and $p=H(P)$. With $a=T[s]$, $c=T[s+m]$, and $w=b^{m-1}\bmod q$,

$$
h_{s+1}=((h_s-aw)b+c)\bmod q.
$$

If $h_s\ne p$, the window cannot equal $P$ because equal sequences have equal fingerprints. If $h_s=p$, equality is only possible; verify the full window before reporting. The resulting matcher is deterministically exact for any parameters, runs in $O(n+m+C)$ arithmetic plus verification work, and can degrade to $O(nm)$ when many windows collide or match.

### Critical invariants

- Symbols have a stable integer encoding and equality semantics.
- The stored window hash equals the polynomial fingerprint of exactly the current $m$ symbols.
- Modular subtraction is normalized according to the language's remainder semantics.
- A hash mismatch rejects safely; a hash match never reports without the declared verification policy.
- Base, modulus, encoding, pattern length, and hash orientation are identical for pattern and windows.
- Random seeds and moduli are generated, scoped, and recorded according to the threat model.
- Output, retained window, preprocessing, and multi-pattern bucket costs are included separately.

### Common failures

Common failures include treating hashes as unique IDs; omitting exact verification; using floating-point powers; recomputing each window hash; applying the wrong outgoing power; mixing left- and right-oriented formulas; allowing negative remainder bugs; overflowing before reduction; choosing predictable fixed parameters against adversarial input; multiplying informal collision probabilities as if hashes were independent; forgetting pattern-length groups; losing windows across chunks; and using noncryptographic fingerprints for authentication.

### Compact example

With base $10$, modulus $101$, and three-digit sequences, $H(314)=314\bmod101=11$. Window `231` has hash $29$. Rolling removes $2\cdot10^2$, multiplies by 10, and adds 4: $((29-200)10+4)\bmod101=11$, the hash of `314`. The hash equality makes the new window a candidate; only direct equality proves the match.

### Connections

[ALGE-053](./053-boyer-moore-family.md) eliminates alignments with deterministic mismatch evidence; Rabin-Karp instead filters them by fingerprints. [ALGE-055](../ROADMAP.md#block-06--string-sequence-and-compression-algorithms) builds a reusable ordered text index. Security Engineering distinguishes randomized algorithmic hashing from cryptographic integrity, while Data Engineering governs canonical encodings and deduplication evidence.

## Governing Question

Given a pattern and a resident or streaming text, how can we maintain a compact fingerprint for every fixed-length window, use it to avoid most full comparisons, state exactly where probability enters, and prevent collisions, arithmetic, encoding, or adversarial choices from becoming silent correctness defects?

Rabin-Karp is not “compare hashes instead of strings” unless probabilistic error is deliberately accepted. The robust engineering pattern is **filter then verify**: a fingerprint mismatch is conclusive, while a fingerprint match is a request for exact evidence.

## Why This Matters

Rolling hashes support exact search, multiple-pattern filtering, plagiarism and similarity pipelines, chunked content processing, two-dimensional matching, and fast comparison of many overlapping windows. Their value comes from reusing nearly all arithmetic between adjacent windows.

They also invite category errors. A small hash cannot be injective over a larger sequence domain. Two independent-looking formulas may share parameters or implementation faults. A collision bound for a random seed does not describe a public fixed seed under adaptive attack. A cryptographic digest has different goals and usually does not provide the same simple rolling update.

The algorithm therefore connects algebra, randomized analysis, exact verification, representation policy, streaming state, and security review. Each layer needs its own claim and evidence.

## Prerequisites and Retrieval

Retrieve modular arithmetic, polynomial evaluation, the pigeonhole principle, probability and union bounds, hash-table collision handling, exact pattern semantics, resident versus streaming processing, and adversarial analysis. Complete [ALGE-051](./051-naive-and-prefix-based-pattern-matching.md), [ALGE-052](./052-knuth-morris-pratt.md), and [ALGE-053](./053-boyer-moore-family.md).

This chapter assumes a nonempty pattern for the rolling loop. Empty-pattern behavior remains an external API policy. Symbols are encoded as integers before hashing, but exact verification compares under the declared sequence equality.

## Learning Objectives

After completing this module, you should be able to:

1. define a polynomial fingerprint and its orientation;
2. derive the rolling-update equation step by step;
3. distinguish candidate filtering from exact equality;
4. state deterministic, expected, and probabilistic guarantees separately;
5. calculate collision bounds under explicit randomization assumptions;
6. implement modular arithmetic without floating point or overflow surprises;
7. construct and detect collision examples;
8. design streaming and multi-pattern variants with bounded state;
9. reject inappropriate cryptographic and deduplication claims; and
10. validate arithmetic, correctness, randomness, and performance independently.

## Core Exposition

### Encode the sequence deliberately

Let $P\in\Sigma^m$ and $T\in\Sigma^n$. Choose a deterministic encoding $e:\Sigma\to\mathbb{Z}$. Equality of symbols must imply equality of encodings; otherwise equal sequences could hash differently and a mismatch would no longer be safe evidence. Injective encoding over the admitted alphabet is the simplest policy.

Bytes can map to 0 through 255. Unicode code points can map to their scalar values after the normalization policy in ALGE-051. Structured records need a canonical field order, type tags, length framing, and stable version. Concatenating ambiguous field text such as `ab|c` without framing can make distinct records share the same encoded sequence before hashing even begins.

The exact matcher and hasher must operate over compatible units. Hashing UTF-8 bytes and then verifying code points is possible only with a carefully defined projection; it is usually simpler to hash and verify the same immutable representation.

### Define a polynomial fingerprint

Choose integer base $b$ and modulus $q>1$. For a length-$m$ integer sequence $X$ define

$$
H_{b,q}(X)=\left(\sum_{i=0}^{m-1}X[i]b^{m-1-i}\right)\bmod q.
$$

Compute it by Horner's rule:

$$
h_0=0,\qquad h_{i+1}=(h_i b+X[i])\bmod q.
$$

This needs $m$ multiply-add-reduce steps and avoids explicitly materializing large powers. The orientation matters: the leftmost symbol has coefficient $b^{m-1}$ here. A reverse-oriented implementation needs a different rolling formula.

Modulo $q$ bounds the stored value, so collisions are inevitable whenever the number of possible sequences exceeds $q$. The pigeonhole principle alone proves that a fingerprint is not identity.

### Derive the rolling update

Let

$$
h_s=\sum_{i=0}^{m-1}T[s+i]b^{m-1-i}\bmod q
$$

and precompute $w=b^{m-1}\bmod q$. The outgoing symbol $a=T[s]$ contributes $aw$. Subtract it:

$$
h_s-aw=\sum_{i=1}^{m-1}T[s+i]b^{m-1-i}.
$$

Multiplying by $b$ shifts every remaining coefficient one power higher. Adding incoming symbol $c=T[s+m]$ at power zero gives

$$
h_{s+1}=((h_s-aw)b+c)\bmod q.
$$

The update uses constant many arithmetic operations under a fixed-word model. In arbitrary-precision arithmetic, operand sizes remain bounded by reductions but are not literally free; in fixed-width arithmetic, intermediate multiplication can overflow unless the implementation uses a sufficiently wide type, safe modular multiplication, or intentional wrapping justified by a different modulus model.

### Filter, then verify

If $P=T[s:s+m]$, deterministic evaluation gives $H(P)=H(T[s:s+m])$. The contrapositive says unequal hashes prove unequal windows. Equal hashes do not imply equal sequences.

An exact Rabin-Karp matcher therefore follows:

1. compute pattern and first-window hashes;
2. at each shift, compare hashes;
3. when equal, compare the complete window with $P$;
4. report only if exact equality succeeds;
5. roll to the next window.

Exact verification makes correctness independent of collision probability. Randomization then controls expected verification work, not whether returned positions are correct.

If verification is deliberately omitted, the method is Monte Carlo: it can report false matches. The error budget must cover all comparisons, parameter generation, independence assumptions, and the consequences of a false result. “The hash is large” is not a proof.

### Analyze deterministic cost

Preprocessing costs $O(m)$. There are $n-m+1$ window fingerprints and $O(1)$ rolling arithmetic per transition. Let $c_s$ be the number of symbols compared when candidate $s$ is verified. Then exact running time is

$$
O\left(n+m+\sum_{s:h_s=H(P)}c_s\right).
$$

If few candidates occur, this is $O(n+m)$. In the worst case every window is a fingerprint candidate and each verification examines $m$ symbols, yielding $O(nm)$. Genuine matches can create the same cost even with a collision-free fingerprint on those inputs. Output time contributes $O(z)$ but is already bounded by successful verification work unless results have additional serialization cost.

The resident version stores constant rolling arithmetic plus inputs and outputs. A streaming exact version must retain the current $m$ symbols, or another representation sufficient for exact verification, so it uses $O(m)$ window state.

### State a polynomial collision bound

Let $X\ne Y$ be fixed equal-length sequences over the finite field $\mathbb{F}_q$, with prime $q$. Their fingerprint difference is a nonzero polynomial $D(b)$ of degree at most $m-1$. A nonzero degree-$d$ polynomial over a field has at most $d$ roots. If $b$ is chosen uniformly from a declared subset of field elements, then

$$
\Pr_b[H_{b,q}(X)=H_{b,q}(Y)]\le\frac{m-1}{|B|},
$$

where $B$ is the sampled base set and the bound assumes the leading difference remains nonzero modulo $q$. If all nonzero field elements are allowed, $|B|=q-1$.

For $W$ fixed unequal window comparisons, the union bound gives probability at most $W(m-1)/(q-1)$ that any collides under the same random base; cap the expression at one. This does not require collision events to be independent. It does require the inputs to be fixed independently of a hidden random choice, or a stronger adversarially robust construction.

Two hashes reduce risk only under a justified joint model. If parameters are independently sampled from suitable families, multiply per-pair bounds; if they reuse related moduli, bases, or code paths, independence cannot be assumed. Exact verification avoids making correctness depend on this calculation.

### Distinguish fixed and randomized parameters

A fixed public base and modulus define a deterministic function. Random-input heuristics may describe a benign corpus, but an adversary can search for collisions once parameters are known. Selecting a fresh secret base from a proven family can restore an input-independent probability statement for nonadaptive fixed inputs; adaptive adversaries and seed exposure need a stronger threat analysis.

Parameter randomness must come from an appropriate system source, avoid biased range mapping, and be scoped. Per-process secrets reduce setup cost but persist across many observations. Per-query secrets narrow exposure but complicate reproducibility. Evidence logs may record a seed digest or protected experiment seed without leaking production secrets.

Noncryptographic universal hashing is not a message authentication code. It does not establish origin, tamper resistance, or collision resistance against computationally capable attackers. Use reviewed cryptographic constructions for security boundaries.

### Reproduce exact search and a forced collision

The following dependency-free implementation accepts integer sequences, performs exact verification for every fingerprint candidate, and demonstrates a collision using deliberately tiny parameters.

<!-- bijux-verify: {"id":"rolling-hash-exact-verification","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"matches=(0, 2) candidates=2\ncollision_hash=True exact_equal=False\ncollision_matches=() candidates=1\n","stderr":""}} -->
```python
def polynomial_hash(values, base, modulus):
    value = 0
    for symbol in values:
        value = (value * base + symbol) % modulus
    return value


def rabin_karp(pattern, text, base=257, modulus=1_000_000_007):
    pattern, text = tuple(pattern), tuple(text)
    m, n = len(pattern), len(text)
    if m == 0:
        raise ValueError("rolling search requires a nonempty pattern")
    if m > n:
        return (), 0
    high_power = pow(base, m - 1, modulus)
    pattern_hash = polynomial_hash(pattern, base, modulus)
    window_hash = polynomial_hash(text[:m], base, modulus)
    matches = []
    candidates = 0
    for start in range(n - m + 1):
        if window_hash == pattern_hash:
            candidates += 1
            if text[start : start + m] == pattern:
                matches.append(start)
        if start < n - m:
            outgoing = text[start]
            incoming = text[start + m]
            window_hash = (
                (window_hash - outgoing * high_power) * base + incoming
            ) % modulus
    return tuple(matches), candidates


encoded_pattern = tuple(map(ord, "aba"))
encoded_text = tuple(map(ord, "ababa"))
matches, candidates = rabin_karp(encoded_pattern, encoded_text)
print(f"matches={matches} candidates={candidates}")

left, right = (0, 0, 0), (1, 0, 1)
left_hash = polynomial_hash(left, 10, 101)
right_hash = polynomial_hash(right, 10, 101)
print(f"collision_hash={left_hash == right_hash} exact_equal={left == right}")
collision_matches, collision_candidates = rabin_karp(left, right, 10, 101)
print(
    f"collision_matches={collision_matches} candidates={collision_candidates}"
)
```

The distinct sequences `000` and `101` both hash to zero under base 10 modulo 101. Exact verification rejects the candidate. The run establishes the implementation's behavior in the recorded environment; exhaustive and algebraic checks provide additional evidence.

### Handle language arithmetic correctly

Python's `%` with a positive modulus returns a nonnegative residue. Languages in which remainder can be negative require explicit normalization such as `((x % q) + q) % q`, or a branch adding $q$ after a bounded subtraction. Prove the bound before using one addition.

Avoid floating-point exponentiation for $w$. Use integer modular exponentiation or iterative multiplication. Define whether symbols may be negative and normalize their encoding. Validate $q>1$, base range, pattern length, and integer conversion.

Using machine overflow as arithmetic modulo $2^w$ can be fast, but it is a different hash family with different collision analysis. In languages where signed overflow is undefined, relying on it is a program defect. Name the unsigned width and prove every operation's semantics.

### Engineer streaming windows

Maintain a ring buffer or deque of exactly the last $m$ encoded symbols, its current hash, and an absolute consumed count. Until $m$ symbols arrive, build the initial window. Thereafter each incoming symbol evicts one outgoing symbol and applies the rolling equation. On a candidate, compare the pattern with the logical ring-buffer order.

Chunk boundaries must not reset the hash or window. Decoder and normalization state precede hashing and may span chunks. A checkpoint needs pattern and parameter identifiers, current residue, ordered window contents, absolute coordinate, encoder/normalizer version, and residual decoding state. Recomputing the hash from the persisted window on recovery provides an integrity check against state corruption.

Backpressure and result limits remain necessary. Pattern `a` in an all-`a` stream generates one result per symbol even though hashing is constant time.

### Extend to multiple patterns carefully

For patterns of one length $m$, compute each fingerprint and store a bucket from hash to a list of patterns and identities. At each text window, look up its fingerprint and exactly verify every member of that bucket. A collision must not overwrite another pattern.

Patterns of different lengths require separate rolling states or a more specialized method. Grouping by length makes ownership explicit but costs one rolling update per active length per symbol. Many lengths or many patterns can favor automata, suffix indexes, or other techniques developed elsewhere.

Deduplication systems sometimes treat a content fingerprint as identity. If false merging is unacceptable, confirm byte equality or use a documented cryptographic digest with an explicit residual-risk policy. Rabin-Karp's algebraic convenience does not authorize destructive deduplication.

### Validate four independent layers

1. **Arithmetic:** compare every rolling value with a freshly recomputed polynomial hash over exhaustive short sequences.
2. **Exactness:** compare reported positions with the naive matcher, including forced collisions.
3. **Probability:** test parameter sampling and analyze the selected family; empirical collision frequencies do not prove a bound.
4. **Performance:** record candidates, false hits, verified symbols, rolling operations, elapsed time, allocation, parameters, seed scope, representation, and corpus.

Include $m=1$, $m=n$, $m>n$, overlaps, no matches, all matches, zero-valued symbols, maximum encoded values, negative-intermediate arithmetic, repeated patterns, hash-bucket collisions, every chunk split, and maximum result volume. Mutation tests should change $b^{m-1}$ to $b^m$, omit normalization, skip verification, or update before checking and confirm the suite fails.

## Definitions and Notation

Let $P\in\Sigma^m$ be nonempty, $T\in\Sigma^n$, $e:\Sigma\to\mathbb{Z}$ a stable encoding, base $b$, and modulus $q>1$.

- $H_{b,q}(X)$ is the polynomial fingerprint of encoded sequence $X$.
- $h_s=H_{b,q}(T[s:s+m])$ is the hash at text shift $s$.
- $w=b^{m-1}\bmod q$ is the outgoing symbol's coefficient.
- A **residue** is the canonical representative used for a congruence class modulo $q$.
- A **candidate hit** satisfies $h_s=H(P)$.
- A **true hit** is a candidate with $T[s:s+m]=P$.
- A **false fingerprint hit** is a candidate whose window is unequal.
- $C$ is the number of candidates and $V=\sum c_s$ the total exact-verification comparisons.
- A **seed** selects randomized hash parameters from a declared family.
- A **collision bound** is a probability statement under named sampling and input assumptions.
- A **cryptographic collision-resistance claim** concerns computational adversaries and is not supplied by ordinary polynomial hashing.

Arithmetic-operation bounds assume fixed-width modular operations are constant time and correctly implemented. End-to-end bounds must include encoding, window retention, verification, output, and parameter generation.

## Mechanisms, Invariants, or Proof Structure

### Rolling invariant

Immediately before classifying shift $s$:

1. the logical window contains exactly $T[s:s+m]$;
2. `window_hash` equals $H_{b,q}(T[s:s+m])$;
3. the pattern hash uses the same $e,b,q,m$, and orientation;
4. every earlier shift has been classified exactly;
5. no candidate has been reported without exact verification.

The rolling derivation proves clauses 1 and 2 after eviction and insertion. The candidate branch preserves clauses 4 and 5. Initialization establishes the base case.

### Exactness theorem

**Theorem.** Filter-then-verify Rabin-Karp reports exactly every occurrence of $P$ in $T$ for any valid deterministic parameters.

**Proof.** If an occurrence exists at $s$, equal encoded sequences produce equal polynomial evaluations, so it becomes a candidate; exact verification succeeds and reports it. Conversely, every report follows exact comparison of the complete pattern and window, so it is an occurrence. Collisions can add verification work but cannot add or remove reports. $\square$

### Rolling-update theorem

**Theorem.** Given correct $h_s$ and $w=b^{m-1}\bmod q$, the rolling equation computes $h_{s+1}$.

**Proof.** Expand $h_s$, subtract the term $T[s]b^{m-1}$, multiply the remaining polynomial by $b$, and add $T[s+m]$. The resulting coefficients are precisely $b^{m-1}$ through $b^0$ for window $T[s+1:s+m+1]$. Congruence is preserved under subtraction, multiplication, and addition. $\square$

### Random-base collision lemma

**Lemma.** For fixed unequal length-$m$ sequences over $\mathbb{F}_q$, their polynomial fingerprints collide for at most $m-1$ bases in the field, unless their coefficient difference becomes the zero polynomial modulo $q$.

**Proof.** Subtract the two fingerprints to obtain a nonzero polynomial of degree at most $m-1$. A nonzero polynomial of degree $d$ over a field has at most $d$ roots. Each colliding base is a root. $\square$

The exceptional clause matters when integer encodings that differ become congruent modulo $q$. Restrict encoded symbols to distinct field elements or include that risk in the model.

### Cost decomposition

Exact cost is best recorded as

$$
T=\Theta(m)+\Theta(n-m+1)+\Theta(V)+\Theta(z_{\mathrm{emit}}),
$$

where $V$ is observed verification work. This distinguishes poor hashing from genuine frequent matches and from expensive output serialization.

### Evidence boundaries

- Algebra proves rolling equivalence and candidate soundness conditions.
- Exact verification proves returned-window equality under the declared representation.
- Probability bounds require the stated field, encoding, randomness, and adversary model.
- Exhaustive tests cover finite domains, not all lengths or parameters.
- Benchmarks describe one implementation and workload.
- No noncryptographic fingerprint establishes authenticity or safe destructive identity.

## Alternatives and Trade-Offs

| Design | Correctness | Typical filtering | State | Best fit | Main limitation |
|---|---|---|---|---|---|
| Single hash + verify | deterministic exact | parameter/workload dependent | $O(m)$ streaming | simple exact window filter | worst-case $O(nm)$ verification |
| Double hash + verify | deterministic exact | fewer candidates if independent | larger constant | expensive equality | independence must be justified |
| Hash only | probabilistic | no exact comparisons | small | explicitly error-tolerant systems | false matches possible |
| KMP | deterministic exact | no fingerprints | $O(m)$ | worst-case linear stream | no multi-pattern hash buckets |
| Boyer-Moore family | deterministic exact | skips alignments | pattern tables | resident random access | variant-specific worst cases |
| Cryptographic digest + verify | deterministic exact with verification | very low accidental collision | higher cost | integrity-oriented pipelines | not naturally rolling in this form |

Use KMP when deterministic linear comparison work matters more than flexible fingerprints. Use Rabin-Karp when adjacent windows, many same-length patterns, multi-dimensional generalization, or an existing rolling-fingerprint pipeline makes filtering valuable. Use a runtime built-in for ordinary single-pattern search when semantics and guarantees are adequate.

Double hashing can reduce verification frequency, but exact verification remains the cleanest correctness boundary. A faster hash with frequent collisions may lose to direct comparison; a slower high-quality hash may cost more than it saves. Measure the complete candidate and equality distribution.

## Failure Modes and Misconceptions

1. **“Equal hash means equal string.”** A smaller range cannot uniquely represent a larger domain.
2. **“Verification defeats hashing's purpose.”** It is performed only on candidates; a useful filter makes them rare.
3. **“With verification, collisions do not matter.”** They do not affect correctness, but can destroy performance.
4. **“A prime modulus makes collisions impossible.”** It enables field analysis; distinct sequences still collide.
5. **“Two hashes square the probability.”** Only an appropriate independence model permits multiplication.
6. **“A fixed random-looking base is randomized.”** Once fixed and public, it is a deterministic target.
7. **“Modulo works identically in every language.”** Negative remainder and overflow semantics differ.
8. **“Use $b^m$ for the outgoing symbol.”** Under this orientation its coefficient is $b^{m-1}$.
9. **“Streaming needs constant memory.”** Exact verification requires retaining or recovering the $m$-symbol window.
10. **“One rolling hash handles every pattern length.”** Each window length has different state and outgoing power.
11. **“Polynomial hash authenticates content.”** It is not a MAC or general collision-resistant digest.
12. **“Observed zero collisions proves the bound.”** Probability guarantees follow from the family and sampling assumptions, not a finite sample.

## Worked Examples

### Example 1

**Situation.** Compute $H(314)$ with base 10 and modulus 101.

Horner evaluation gives $h_1=3$, $h_2=(3\cdot10+1)=31$, and $h_3=(31\cdot10+4)\bmod101=314\bmod101=11$.

**Conclusion.** The fingerprint is 11; the unreduced decimal interpretation and modular Horner evaluation agree.

### Example 2

**Situation.** Roll window `231` to `314` with the same parameters.

$H(231)=231\bmod101=29$ and $w=10^2\bmod101=100$. Remove outgoing 2, shift, and add 4:

$$
((29-2\cdot100)10+4)\bmod101=-1706\bmod101=11.
$$

Fresh recomputation of `314` also gives 11.

**Conclusion.** The rolling invariant holds even though the unreduced intermediate is negative.

### Example 3

**Situation.** Force a collision under base 10 modulo 101.

Sequence `000` evaluates to 0. Sequence `101` evaluates to 101, also residue 0. They are unequal but share a fingerprint. An exact verifier compares the first symbols, sees 0 versus 1, and rejects.

**Conclusion.** Collision is an expected property of compression; verification converts it into extra work rather than an incorrect match.

### Example 4

**Situation.** Show why a mismatch is conclusive.

Assume a window actually equals the pattern symbol by symbol. Deterministic application of the same encoding, base, orientation, and modulus must perform the same arithmetic and produce the same residue. Therefore different residues contradict equality.

**Conclusion.** Hash mismatch safely filters a window only when both sides use identical fingerprint semantics.

### Example 5

**Situation.** Bound random-base collision probability for two unequal length-20 sequences with prime modulus $q=1{,}000{,}000{,}007$ and a base uniform over $q-1$ nonzero values.

The difference polynomial has degree at most 19, so the bound is

$$
\frac{19}{1{,}000{,}000{,}006}<1.9\times10^{-8}.
$$

This is for one fixed unequal pair and the stated random experiment.

**Conclusion.** A small numerical bound is meaningful only with its pair count, sampling domain, encoding, and adversary assumptions.

### Example 6

**Situation.** Apply a union bound to one million fixed candidate comparisons using the preceding parameters.

Multiplying the per-pair bound gives less than $0.019$. This is already about 1.9%, much larger than the per-comparison number. The union bound may be loose, but it shows why quoting only a single-pair probability is misleading.

**Conclusion.** Error budgets must cover the number of opportunities for collision; exact verification makes this error probability zero for returned equality.

### Example 7

**Situation.** A C implementation computes `(hash - outgoing*power)*base` in signed 64-bit arithmetic before applying a modulus.

Even if the final mathematical residue fits, the intermediate product may overflow. Signed overflow is not a portable modular operation. Use a wider supported type, checked modular multiplication, or an explicitly unsigned $2^w$ design with a separately proved hash family.

**Conclusion.** Mathematical reduction after an operation cannot repair undefined or unintended machine arithmetic before it.

### Example 8

**Situation.** Search three same-length patterns where two share a fingerprint.

Store the bucket as `hash -> [pattern_id_1, pattern_id_2]`, not one overwritten entry. When a text window has that hash, verify both pattern sequences and emit only exact identities. A third pattern in another bucket is never compared at that window.

**Conclusion.** Hash-table collision handling and fingerprint collision handling meet in the bucket; neither permits dropping a pattern.

### Example 9

**Situation.** A match begins in one input chunk and ends in the next.

If the matcher preserves its $m$-symbol ring buffer, residue, and absolute count, the new symbols roll through the same logical windows as a resident scan. Resetting at the chunk boundary loses cross-chunk windows. Persisting only the residue is insufficient for exact verification or safe recovery.

**Conclusion.** Chunk framing must not alter the logical window sequence, and exact streaming state is $O(m)$.

### Example 10

**Situation.** A storage service deletes “duplicate” objects whenever a rolling fingerprint matches.

A collision would destroy distinct data. The service must compare bytes before deletion or use a reviewed digest-and-verification protocol with quarantining, audit logs, and recovery. Randomized search bounds do not authorize irreversible identity decisions.

**Conclusion.** Consequence severity determines the evidence threshold; rolling fingerprints are filters, not destructive proof.

## Cross-Program Connections

- **Data Structures Engineering:** hash buckets, ring buffers, sparse length groups, and canonical encodings determine memory and lookup behavior. See the [Data Structures Engineering roadmap](../../17-data-structures-engineering/ROADMAP.md).
- **Database Engineering:** hash joins and indexes share the rule that hash equality selects candidates while key equality resolves collisions.
- **Data Engineering:** content fingerprints, deduplication, schema evolution, and exactly reproducible encodings require provenance and safe verification.
- **Security Engineering:** public fixed parameters, adaptive collision construction, seed management, MACs, and destructive actions belong to the threat model.
- **Concurrent and Parallel Programming:** parameter secrets and immutable pattern buckets may be shared; each stream window and absolute coordinate require isolated state.
- **API and Service Engineering:** error budgets, result truncation, checkpoint versions, and equality semantics must be explicit externally.
- **Algorithms:** [ALGE-052](./052-knuth-morris-pratt.md) provides a deterministic streaming alternative, [ALGE-053](./053-boyer-moore-family.md) uses deterministic skips, and [ALGE-055](../ROADMAP.md#block-06--string-sequence-and-compression-algorithms) indexes one stable text for repeated ordered queries.

## References

1. Richard M. Karp and Michael O. Rabin, “Efficient Randomized Pattern-Matching Algorithms,” *IBM Journal of Research and Development* 31(2), March 1987, pp. 249–260. [Primary paper and DOI 10.1147/rd.312.0249](https://doi.org/10.1147/rd.312.0249). Retrieved 2026-09-05.
2. J. Lawrence Carter and Mark N. Wegman, “Universal Classes of Hash Functions,” *Journal of Computer and System Sciences* 18(2), April 1979, pp. 143–154. [Primary paper and DOI 10.1016/0022-0000(79)90044-8](https://doi.org/10.1016/0022-0000(79)90044-8). Retrieved 2026-09-05.
3. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022, Chapter 32, “String Matching.” [Official publisher record](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/). Retrieved 2026-09-05.
4. Rajeev Motwani and Prabhakar Raghavan, *Randomized Algorithms*, Cambridge University Press, 1995. [Publisher record and DOI 10.1017/CBO9780511814075](https://doi.org/10.1017/CBO9780511814075). Retrieved 2026-09-05.
5. Dan Gusfield, *Algorithms on Strings, Trees, and Sequences*, Cambridge University Press, 1997, Part I. [Publisher record and DOI 10.1017/CBO9780511574931](https://doi.org/10.1017/CBO9780511574931). Retrieved 2026-09-05.

## Exercises

### Exercise 1

Using base 7 and modulus 13, compute the polynomial fingerprint of sequence $(2,4,1)$ by Horner's rule. State the outgoing coefficient for a length-three rolling window.

### Exercise 2

Window $(2,4,1)$ rolls to $(4,1,5)$. Starting from your first answer, derive the new hash with the rolling equation and confirm it by fresh recomputation.

### Exercise 3

An implementation reports a match whenever two 64-bit rolling hashes agree. Diagnose its correctness contract, state two distinct threat models, and give the minimum change that makes the result exact.

### Exercise 4

Design a same-length multi-pattern Rabin-Karp service. Specify bucket structure, parameter lifecycle, streaming state, collision handling, output bounds, and validation evidence.

### Exercise 5

A data lake wants rolling fingerprints for chunk discovery and cryptographic digests for object identity. Design a two-layer pipeline that survives adversarial input, schema upgrades, process restarts, and a false rolling hit without corrupting data.

## Answers to the Exercises

### Answer 1

Horner evaluation is $h_1=2$, $h_2=(2\cdot7+4)\bmod13=18\bmod13=5$, and $h_3=(5\cdot7+1)\bmod13=36\bmod13=10$. Thus the fingerprint is 10. The outgoing coefficient is $w=7^{3-1}\bmod13=49\bmod13=10$. A correct answer must use $b^{m-1}$, not $b^m$.

### Answer 2

Remove outgoing 2, shift, and add incoming 5:

$$
((10-2\cdot10)7+5)\bmod13=(-65)\bmod13=0.
$$

Fresh evaluation of $(4,1,5)$ is $4\cdot7^2+1\cdot7+5=208$, and $208\bmod13=0$. The two computations agree. In a language with negative remainder, normalize `-65` to the canonical residue zero explicitly.

### Answer 3

The implementation is Monte Carlo: it can return a false match when unequal windows collide. For accidental nonadaptive inputs with independently secret, well-sampled hash parameters, a proven family may make the probability small enough for a low-consequence filter. For adaptive untrusted input with public fixed parameters, an attacker can search for collisions and the informal random-collision estimate may not apply. Neither contract is deterministic equality.

The minimum exactness repair is to compare the complete candidate window with the pattern after both hashes agree and report only on equality. This makes collisions affect time rather than results. If authentication is required, exact comparison alone does not prove origin; add a reviewed cryptographic authentication protocol.

### Answer 4

Compile every immutable length-$m$ pattern under one versioned encoding and independently generated parameter set. Store `fingerprint -> immutable list of (pattern_id, pattern)` so collisions never overwrite entries. Per stream retain an $m$-symbol ring buffer, current residue, absolute consumed count, decoder/normalizer state, pattern-set digest, and output/backpressure state. At each candidate hash, exactly compare every bucket member and emit its stable ID and absolute start only on equality.

Bound pattern count, bucket length, $m$, concurrent streams, encoded expansion, candidate verifications, results, queues, and time. Rotate parameters by compiling a new pattern-set version; do not switch an active stream mid-window without a defined restart. Validate rolling hashes against fresh recomputation, all outputs against a naive per-pattern oracle, deliberate same-bucket collisions, duplicate patterns, all chunk partitions, all-match output, pattern-set upgrades, checkpoints, and resource-limit statuses. Probability analysis supports expected bucket quality but is not used for correctness.

### Answer 5

Use rolling fingerprints only to propose chunk boundaries or candidate existing chunks. Canonically frame raw bytes and metadata under a schema version. For each candidate, compute a versioned cryptographic digest and compare length and bytes before reusing or deleting stored content. Store object identity as an immutable record containing digest algorithm/version, byte length, schema, storage generation, and verified location; never use the rolling value as identity.

Choose rolling parameters from a documented randomized family with protected seed scope and cap candidate/bucket work so adversarial collisions cause bounded slowdown. Persist chunker version, rolling window, source offset, cryptographic state when safely serializable, and input generation at atomic checkpoints. On restart, verify the checkpoint and recompute a boundary region to avoid gaps or duplicates. Schema or algorithm upgrades write new identities alongside old ones and migrate only after byte verification.

A false rolling hit merely triggers digest and byte comparisons that reject reuse. Corruption, missing bytes, parameter-version mismatch, or unverifiable state produces quarantine or restart from a trusted boundary, never deletion. Validate with forced rolling collisions, cryptographic mismatch fixtures, restart at every boundary, schema-version mixtures, truncated data, concurrent writers, and recovery drills. This separation keeps fast discovery probabilistic while object identity and destructive actions require stronger verified evidence.
