---
module_id: ALGE-074
program: Algorithm Engineering
level: 2
module_number: 74
title: Streaming Frequency Estimation
status: complete
last_verified: 2026-09-05
---

# Streaming Frequency Estimation

## One-Page Review

### Governing question

How can a bounded-memory, one-pass system estimate item frequencies or discover frequent items, and exactly which error, probability, update-model, and operational assumptions support its answers?

### Essential definitions

- A stream is a sequence of updates $(i,\Delta)$ to coordinates of a frequency vector $f$ over universe $U$.
- In the **insertion-only** model, $\Delta\ge0$; in a **strict-turnstile** stream, signed updates are allowed but every true frequency remains nonnegative; a **general-turnstile** stream may have negative coordinates.
- A **point query** asks for one coordinate $f_i$; a **frequent-item** or **heavy-hitter** query asks for identities whose frequencies cross a threshold.
- For an insertion-only stream, $F_1=\sum_i f_i$ is total update mass; for unit updates it is stream length $n$.
- An **additive-error** guarantee bounds $|\widehat f_i-f_i|$ by a fraction of a global norm such as $\varepsilon F_1$.
- A **one-sided estimate** never underestimates or never overestimates under a stated update model.
- A **candidate generator** retains possible heavy identities; a **frequency estimator** answers counts for supplied identities. These are different interfaces.
- A **mergeable summary** combines partitions into the same summary that their concatenated updates would produce, under compatible parameters and seeds.
- A guarantee is **pointwise** when it applies to one fixed query; answering many adaptive queries requires stronger analysis or a declared failure-budget composition.
- A **logical event identity** distinguishes intended occurrences from retries, duplicates, and replayed transport records.

### Central model, mechanism, or theorem

Misra–Gries with parameter $k\ge2$ keeps at most $k-1$ item counters. For each unit insertion: increment the item if tracked; insert it with count one if space exists; otherwise decrement every counter and delete zeros. If $D$ global decrement steps occur, then for every item $i$,

$$
0\le f_i-\widehat f_i\le D\le\left\lfloor\frac nk\right\rfloor.
$$

Each decrement can be viewed as cancelling the untracked arrival with one occurrence from each of $k-1$ distinct tracked items: a group of $k$ distinct occurrences. These groups are disjoint, so $kD\le n$. Item $i$ loses at most one occurrence per group, proving the error bound. Therefore every item with $f_i>n/k$ must be among the final candidates. The counters are lower bounds, not exact counts; a second pass can verify candidates when the stream is replayable.

Count–Min gives a different randomized point-query contract. In a nonnegative insertion-only stream, it adds each update to one hashed counter in each of $d$ rows and returns the row minimum. With $w=\lceil e/\varepsilon\rceil$, $d=\lceil\ln(1/\delta)\rceil$, pairwise-independent hashing within rows, and independent rows, a fixed item satisfies

$$
f_i\le\widehat f_i\le f_i+\varepsilon F_1
$$

with probability at least $1-\delta$. This is not a simultaneous guarantee over an unbounded adaptive query sequence.

### Critical invariants

- The update model, weight domain, universe encoding, and window semantics are fixed before selecting a sketch.
- Each accepted logical update is applied exactly once, or duplicates are explicitly part of the measured stream.
- Counter arithmetic cannot silently overflow, wrap, saturate, or lose signedness.
- Hash family, seeds, width, depth, key encoding, and algorithm version travel with persisted summaries.
- Merges occur only between summaries with compatible semantics, parameters, and seeds.
- Candidate discovery is not claimed from a point-query structure that cannot enumerate identities.
- Error is stated against the correct norm and denominator, with strict versus non-strict threshold conventions.
- Probability scope names fixed, simultaneous, repeated, and adaptive queries and accounts for every reported answer.
- Resets, lateness, retractions, expiry, and replay preserve declared window meaning.
- Exact audits retain raw or independently aggregated evidence rather than treating the sketch as its own oracle.

### Common failures

Common failures are calling approximate counters exact; omitting insertion-only assumptions; using Count–Min after negative updates while retaining its one-sided theorem; confusing candidate discovery with point estimation; reporting a per-query probability as a dashboard-wide guarantee; choosing seeds after seeing errors; merging incompatible sketches; allowing counter overflow; losing item identities during canonicalization; double-counting retries; comparing sketch counts with an oracle built from the same flawed ingestion; hiding false positives near a threshold; and interpreting low absolute error as low relative error for rare items.

### Compact example

For the unit stream $a,b,a,c,a,b,d,a,e,a$ with $k=4$, Misra–Gries first fills three counters, cancels the distinct group containing $d$, and ends with candidates including $a$. The stream length is 10, so every frequency estimate is at most $\lfloor10/4\rfloor=2$ below truth, and every item occurring more than 2.5 times must appear. The theorem guarantees inclusion of $a$; it does not certify the stored counter as $a$'s exact frequency.

### Connections

[ALGE-068](./068-monte-carlo-and-las-vegas-algorithms.md) supplies randomized error semantics, and [ALGE-071](./071-online-decisions-and-competitive-analysis.md) supplies causal evaluation discipline. [ALGE-075](../ROADMAP.md#block-08--online-streaming-and-dynamic-algorithms) treats distinct counting, while ALGE-076 treats quantiles; neither is interchangeable with frequency estimation.

## Governing Question

When an event stream is too large, too fast, or too distributed to retain exact per-key state, how should an engineer define the frequency problem, select a deterministic counter summary or randomized sketch, derive its guarantee, and operate it without overstating what bounded memory proves?

“Count the common keys” conceals several problems. The caller may supply an identity and ask for its count, may need every identity above a threshold, may ask for the top $q$, or may need large positive and negative changes. Updates may only insert, may retract while counts stay nonnegative, or may form a fully signed vector. A lifetime stream, tumbling window, event-time sliding window, and decayed history are different objects.

The correct design begins with that contract. Misra–Gries provides deterministic candidates and lower estimates for unit insertion streams. Count–Min provides compact randomized point estimates with one-sided error for nonnegative updates. Count Sketch supports signed-noise reasoning under a different norm. None fixes duplicate ingestion, undefined identity, window disorder, or a dishonest probability budget.

## Why This Matters

Frequency summaries support network telemetry, database planning, abuse detection, cache admission, observability, market aggregation, and feature pipelines. Exact maps grow with distinct cardinality and can become the memory bottleneck even when updates are individually trivial. Bounded summaries exchange exactness for explicit error while preserving one-pass speed and often mergeability.

The exchange is useful only when its units match the decision. An additive error of $\varepsilon F_1$ can be excellent for heavy items and meaningless for rare ones. A false positive in a diagnostic dashboard differs from a false positive that blocks a user. A point-query guarantee does not identify which keys to query. An estimate of transported records is not an estimate of logical events if retries duplicate records.

Production also changes the mathematics: updates arrive concurrently, partitions merge, counters persist across versions, hash seeds can be adversarially targeted, and event-time windows revise earlier state. The summary must be treated as a versioned state machine with evidence boundaries, not a magical compression primitive.

## Prerequisites and Retrieval

Retrieve hashing, linearity of expectation, Markov's inequality, union bounds, vector norms, and integer arithmetic. Review [ALGE-066](./066-randomized-selection-and-sampling.md) for sampling design, [ALGE-068](./068-monte-carlo-and-las-vegas-algorithms.md) for randomized guarantees, and [ALGE-071](./071-online-decisions-and-competitive-analysis.md) for prefix-only evaluation.

This chapter owns point frequencies, frequent-item candidates, Misra–Gries, Count–Min, update-model boundaries, mergeability, and operational evidence. [ALGE-075](../ROADMAP.md#block-08--online-streaming-and-dynamic-algorithms) owns distinct counting, ALGE-076 owns quantiles, and Data Engineering owns transport, event-time, and pipeline architecture.

## Learning Objectives

After completing this module, you should be able to:

1. specify insertion-only, strict-turnstile, and general-turnstile frequency problems;
2. distinguish point queries, frequent-item discovery, and top-$q$ reporting;
3. derive the Misra–Gries candidate and additive-error guarantees;
4. derive Count–Min's pointwise one-sided error bound;
5. allocate width, depth, counter bits, and a probability budget;
6. explain why deletions, rare-item relative error, and adaptive queries alter the contract;
7. verify deterministic and randomized implementations with exact oracles;
8. design compatible partition merges and versioned persisted state;
9. diagnose overflow, replay, duplication, window, and identity failures; and
10. define guardrails and downstream decisions proportional to the evidence.

## Core Exposition

### Specify the vector and stream semantics

Let universe $U$ consist of canonical item identifiers. Each update $(i,\Delta)$ changes $f_i\leftarrow f_i+\Delta$. Unit insertion has $\Delta=1$; weighted insertion permits nonnegative mass. A strict-turnstile stream permits negative updates but requires $f_i\ge0$ after every prefix. A general-turnstile stream permits signed coordinates. These models admit different estimators and proofs.

Define whether frequency means record count, logical-event count, bytes, money, duration, or another weight. Define the population boundary and clock. A lifetime prefix is append-only; a tumbling window resets; an event-time sliding window may retract expired or late updates. Exponential decay changes weights continuously. Never simulate a window by silently clearing a lifetime theorem.

Canonical identity is part of correctness. Unicode normalization, case folding, composite-key order, tenant namespace, schema version, and privacy transformation must be stable before hashing. Two representations of one entity split its frequency; two entities mapped to one key merge their frequency before any sketch collision is considered.

### Separate query interfaces and error units

A point query takes $i$ and returns $\widehat f_i$. It need not store identities and therefore cannot necessarily answer “which keys are heavy?” A frequent-item structure returns candidates for all $i$ satisfying $f_i>\phi F_1$, often with a gray zone in which false positives are allowed. A top-$q$ interface must define ties and whether it returns approximate order, candidates, or certified membership.

Additive error $\varepsilon F_1$ scales with total mass. If $F_1=10^9$ and $\varepsilon=10^{-4}$, the error allowance is 100,000 even for an item whose true count is 3. Relative error to each $f_i$ is a much stronger and often impossible demand at sublinear space for all coordinates. Choose the metric from the decision threshold, not from familiar notation.

Threshold boundaries must be literal. “Heavy” may mean $f_i>\phi F_1$ or $f_i\ge\phi F_1$. A deterministic guarantee that includes every item above $F_1/k$ says nothing automatic about equality. For estimated thresholds, report a gray zone or verify candidates exactly.

### Derive Misra–Gries by cancellation

For unit insertions and integer $k\ge2$, retain at most $k-1$ pairs. An arrival already represented increments its counter. An unrepresented arrival uses an empty slot when available. If all slots are occupied, decrement every stored counter and delete zeros instead of storing the arrival [1].

Interpret each global decrement as deleting a group of $k$ distinct occurrences: the current untracked occurrence and one occurrence of each of $k-1$ distinct tracked items. Let $D$ be the number of such groups. The groups are disjoint, so $kD\le n$ and $D\le\lfloor n/k\rfloor$.

After all cancellations, a stored count $\widehat f_i$ is the number of uncancelled occurrences of $i$. It cannot exceed $f_i$. At most one occurrence of $i$ is removed per cancellation group, so $f_i-\widehat f_i\le D$. If $f_i>n/k$ and $i$ were absent at the end, all its occurrences would have been cancelled, requiring $f_i\le D\le n/k$, a contradiction. Thus every such item is a candidate.

The candidate set may contain items below the threshold. If a second pass or exact side table is available, count only candidates and filter exactly. In a one-pass service, return bounded intervals $[\widehat f_i,\widehat f_i+D]$ or use the stated global $n/k$ bound. Weighted positive updates require a correct weighted variant; expanding huge weights into unit events is not an implementation plan.

### Derive Count–Min's pointwise guarantee

Count–Min stores a $d\times w$ array initialized to zero [2]. Row $r$ uses hash $h_r:U\to\{0,\ldots,w-1\}$. A nonnegative update $(i,\Delta)$ adds $\Delta$ to every counter $(r,h_r(i))$. The estimate is

$$
\widehat f_i=\min_r C[r,h_r(i)].
$$

Every selected counter contains $f_i$ plus nonnegative collision mass, hence $\widehat f_i\ge f_i$. For a fixed row, let $X_r$ be collision mass from other items. With pairwise-independent uniform hashing,

$$
\mathbb E[X_r]
=\sum_{j\ne i} f_j\Pr[h_r(j)=h_r(i)]
\le\frac{F_1}{w}.
$$

Choose $w=\lceil e/\varepsilon\rceil$, so $\mathbb E[X_r]\le\varepsilon F_1/e$. Markov's inequality gives $\Pr[X_r>\varepsilon F_1]\le1/e$. If rows are independent, all $d$ rows are bad with probability at most $e^{-d}$. Choosing $d=\lceil\ln(1/\delta)\rceil$ makes this at most $\delta$. Taking the minimum yields the stated pointwise upper bound.

The probability is over hash selection for a fixed item and appropriate stream model. To promise $Q$ predetermined point answers together, one simple union-bound allocation uses per-query failure at most $\delta/Q$, increasing depth. Adaptive queries, adversarial keys that learn seeds, or public fixed hashes require a threat-specific analysis.

### Verify mechanics without treating code as proof

The following deterministic hashes make the trace reproducible; they illustrate collisions but are not evidence that this fixed family resists adversarial keys.

<!-- bijux-verify: {"id":"frequency-summary-mechanics","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"mg_counters={'a': 5, 'b': 2, 'e': 1} decrements=1 max_error=1 heavy_over_3=['a']\ncount_min_true_1=4 estimate_1=4\ncount_min_true_2=2 estimate_2=2\ncount_min_absent_6=4\none_sided_on_present=True\nnegative_update=rejected\n","stderr":""}} -->
```python
from collections import Counter


def misra_gries(stream, k):
    if k < 2:
        raise ValueError("k must be at least two")
    counters = {}
    decrements = 0
    for item in stream:
        if item in counters:
            counters[item] += 1
        elif len(counters) < k - 1:
            counters[item] = 1
        else:
            counters = {key: count - 1 for key, count in counters.items() if count > 1}
            decrements += 1
    return counters, decrements


class CountMin:
    def __init__(self, width, hashes):
        if width < 1 or not hashes:
            raise ValueError("invalid dimensions")
        self.width = width
        self.hashes = tuple(hashes)
        self.rows = [[0] * width for _ in hashes]

    def _bucket(self, item, coefficients):
        a, b = coefficients
        return ((a * item + b) % 101) % self.width

    def update(self, item, delta=1):
        if delta < 0:
            raise ValueError("this implementation is insertion-only")
        for row, coefficients in zip(self.rows, self.hashes):
            row[self._bucket(item, coefficients)] += delta

    def estimate(self, item):
        return min(
            row[self._bucket(item, coefficients)]
            for row, coefficients in zip(self.rows, self.hashes)
        )


stream = tuple("abacabdaeaba")
truth = Counter(stream)
counters, decrements = misra_gries(stream, 4)
max_error = max(truth[item] - counters.get(item, 0) for item in truth)
heavy = sorted(item for item, count in truth.items() if count > len(stream) / 4)
print(f"mg_counters={counters} decrements={decrements} max_error={max_error} heavy_over_3={heavy}")

numeric_stream = (1, 2, 1, 3, 1, 2, 4, 1)
numeric_truth = Counter(numeric_stream)
summary = CountMin(5, ((1, 0), (2, 1)))
for item in numeric_stream:
    summary.update(item)
print(f"count_min_true_1={numeric_truth[1]} estimate_1={summary.estimate(1)}")
print(f"count_min_true_2={numeric_truth[2]} estimate_2={summary.estimate(2)}")
print(f"count_min_absent_6={summary.estimate(6)}")
print(f"one_sided_on_present={all(summary.estimate(i) >= count for i, count in numeric_truth.items())}")
try:
    summary.update(1, -1)
except ValueError:
    print("negative_update=rejected")
```

The exact oracle checks this trace, and later finite exhaustive checks can cover small universes and streams. Neither proves Count–Min's probability theorem; that depends on the hash assumptions and derivation. The absent key estimating four demonstrates that one-sidedness does not mean absence certification.

### Match the algorithm to update semantics

Negative updates destroy the simple Count–Min argument because collision mass is no longer nonnegative. Taking a minimum of signed contaminated counters can understate a coordinate. A strict-turnstile promise about true coordinates does not make every collision contribution nonnegative. Do not retain the insertion-only one-sided claim after adding deletion support.

Count Sketch hashes each update to buckets with independent random signs and commonly takes a median estimate; its error is analyzed through signed noise and an $F_2$-related tail rather than Count–Min's one-sided $F_1$ error [3]. It is suitable for different point, change, and heavy-hitter constructions. Algorithm names and parameter symbols are not interchangeable evidence.

Sliding windows require expiry. Exact bucket rotation, exponential histograms, smooth histograms, or other window structures impose additional approximation and boundary rules. Late event-time updates may revise closed windows. State whether answers reflect arrival order, processing time, or event time and how watermarks make results provisional or final.

### Budget memory, probability, and arithmetic together

Count–Min's nominal counter count is $wd$. With $\varepsilon=10^{-3}$ and $\delta=10^{-6}$, $w=2719$ and $d=14$, totaling 38,066 counters. Eight-byte counters consume 304,528 bytes before row objects, seeds, alignment, serialization, and metadata. Multiplying a per-tenant sketch by a million tenants plainly changes the design.

Counter width must cover maximum accumulated bucket mass between resets or use checked wider arithmetic. Saturation preserves monotonicity but invalidates the numerical bound unless modeled. Wraparound violates one-sidedness catastrophically. Floating weights add rounding and non-associative merge order; specify acceptable numerical error separately from sketch error.

Allocate one failure budget to the product surface. If a dashboard presents one million predetermined queries and needs joint failure at most $10^{-6}$, configuring each query at $10^{-6}$ does not supply that claim. A union bound would require per-query failure at most $10^{-12}$, absent stronger structure. Repeated refreshes and multiple retained windows also consume budget.

### Merge only compatible state

Count–Min arrays with identical dimensions, coordinate encoding, hash functions, seeds, counter semantics, and algorithm version merge by elementwise addition. Linearity then represents the multiset sum of partition streams. Different seeds map keys to different cells; adding their arrays creates no valid Count–Min summary.

Misra–Gries summaries can be merged through a correctly weighted reduction of their retained candidates, with error accounting from each input. Simply adding same-key counters and keeping the largest $k-1$ without reduction or accumulated error reasoning is not automatically valid. Test merge results against concatenated streams and the theorem, including empty partitions and skew.

Persist a state envelope containing version, parameters, seeds or seed identifiers, key schema, update model, window, counter type, creation and closure times, source partitions, and checksum. Reject incompatible merge rather than coercing it. Version migration is a semantic operation, not a byte-copy convenience.

### Build evidence around decisions and failures

For deterministic summaries, compare every returned interval and candidate guarantee against exact counts on generated, exhaustive-small, skewed, uniform, bursty, and adversarial-order streams. For randomized sketches, run preregistered independent seeds, report the full error distribution and empirical failure count, and retain theoretical probability scope. Freeze seeds before a held-out test.

Use an exact oracle independent of the ingestion path when testing end-to-end correctness. If sketch and oracle both consume the same duplicated, dropped, or mis-keyed records, their agreement proves only common-input consistency. Reconcile against source offsets, logical identities, or another trusted ledger.

Measure update and query throughput, latency tails, memory including metadata, merge cost, serialization, recovery, and contention. Include counter overflow boundaries, corrupted state, missing partitions, seed mismatch, late data, replay, reset races, and rolling-version coexistence. A fast isolated loop is not a service benchmark.

### Operate the summary as fallible infrastructure

Expose algorithm, parameters, window, last complete offset or watermark, and error semantics with every answer. Downstream decisions need threshold hysteresis or exact verification near consequential boundaries. A summary that may overestimate should not independently trigger irreversible punishment.

Guard update lag, rejected updates, duplicate rate, counter headroom, saturated cells, query volume, empirical audit error, incompatible merges, state age, and recovery parity. Rotate seeds under a designed migration protocol if adversarial collision risk changes; uncoordinated rotation breaks merges and comparisons.

Fallback may route critical keys to exact counters, widen an uncertainty band, disable automatic action, rebuild from retained logs, or declare results unavailable. Rollback must name what happens to already persisted state and mixed-version partitions. Never silently reinterpret old counters under new hashing or identity rules.

## Definitions and Notation

- $U$: canonical item universe; $i,j\in U$ are item identities.
- $(i,\Delta)$: update adding weight $\Delta$ to coordinate $i$.
- $f_i$: true frequency or accumulated weight of item $i$ in the declared population.
- $\widehat f_i$: summary estimate for $f_i$.
- $F_1=\sum_i|f_i|$: vector $L_1$ norm; in a nonnegative insertion stream it is total mass.
- $F_2=(\sum_i f_i^2)^{1/2}$: vector $L_2$ norm.
- $n$: number of unit insertions when that special case is used.
- $k$: Misra–Gries cancellation-group size, leaving at most $k-1$ counters.
- $D$: number of Misra–Gries global decrement or cancellation steps.
- $\phi$: frequent-item threshold fraction.
- $\varepsilon$: additive-error parameter.
- $\delta$: declared probability that a randomized guarantee fails.
- $w,d$: sketch width and depth.
- $h_r$: bucket hash for row $r$.
- **Pointwise probability:** probability statement for one query fixed independently of the random sketch.
- **False positive:** reported candidate below the required true threshold.
- **False negative:** required heavy item omitted from the report.

## Mechanisms, Invariants, or Proof Structure

### Misra–Gries obligations

Show at most $k-1$ counters, one group of $k$ distinct occurrences per decrement, disjoint groups, $kD\le n$, lower estimates, per-item loss at most $D$, and inclusion for $f_i>n/k$. State whether stored estimates or a second pass determine final output.

### Count–Min obligations

Show nonnegative collision mass, no underestimation, expected row noise at most $F_1/w$, Markov's row failure, independent-row amplification, minimum aggregation, and the exact scope of fixed-query probability. State the hash-family assumptions rather than merely saying “random hash.”

### State obligations

Check canonical keys, exactly-once logical update semantics, checked arithmetic, window transitions, compatible parameters and seeds, deterministic serialization, atomic checkpoints, and provenance-preserving merges.

### Evidence obligations

Separate proof from executable traces, finite exhaustive tests, seeded simulations, end-to-end reconciliation, and production monitoring. Each answers a different question and has a declared limitation.

## Alternatives and Trade-Offs

| Method | Primary contract | Strength | Principal boundary |
|---|---|---|---|
| Exact hash map | Exact point counts and enumeration | No sketch error | Memory scales with distinct keys |
| Misra–Gries | Deterministic frequent candidates in unit insertion streams | No random failure; simple proof | Lower estimates and threshold gray zone |
| Space-Saving | Frequent and top-$q$ candidates | Often strong practical ranking | Different counter/error semantics require their own proof [6] |
| Count–Min | Randomized nonnegative point estimates | Fast, compact, linear merge | One-sided $F_1$ error; identities not enumerable |
| Count Sketch | Signed-noise point estimation | Supports turnstile-style analysis | Two-sided randomized error under another norm [3] |
| Sampling | Estimated frequencies from retained events | Preserves inspectable examples | Rare items and weights need sampling-specific analysis |
| Exact hot set plus sketch | Precision for critical keys, bounded tail state | Aligns memory with consequence | Promotion, demotion, and double-count rules add state |

An exact map is best when cardinality is bounded and correctness cost dominates memory. Misra–Gries is compelling when deterministic heavy-candidate inclusion is the real need. Count–Min fits supplied-key point estimates under nonnegative updates. Hybrid designs can verify consequential candidates exactly, but their handoff rules become part of correctness.

## Failure Modes and Misconceptions

- **“The counter is the frequency.”** Misra–Gries stores a lower estimate; Count–Min can overestimate.
- **“A point sketch finds heavy keys.”** Without identities or a candidate mechanism, there is nothing to enumerate.
- **“$1-\delta$ covers every query.”** The basic Count–Min derivation is pointwise for a fixed query.
- **“Strict turnstile preserves Count–Min's minimum proof.”** Negative collision contributions can cause underestimation.
- **“Small additive error means small relative error.”** Rare items can have enormous relative error.
- **“More rows reduce collision magnitude.”** Width controls row noise; depth amplifies success probability.
- **“More width reduces failure probability directly.”** Width and depth have different roles in the standard analysis.
- **“Compatible dimensions imply mergeability.”** Seeds, identity, version, counters, update model, and windows must also match.
- **“Agreement with an exact map proves ingestion correctness.”** A shared input defect can fool both.
- **“A fixed public hash is random forever.”** Adaptive or malicious keys can target exposed structure.
- **“Saturation is a harmless implementation detail.”** It changes arithmetic and invalidates the bound.
- **“A retry is another occurrence.”** Only the domain definition decides whether duplicate transport is new logical mass.

## Worked Examples

### Example 1

**Situation.** A stream contains at most 200 known keys and memory is ample.

**Reasoning.** An exact map gives counts, enumeration, and arbitrary threshold checks without approximation. A sketch would add collision, probability, seed, and audit complexity without relieving a real constraint.

**Conclusion.** Bounded-memory approximation is justified by a resource boundary, not by fashion.

### Example 2

**Situation.** Misra–Gries with $k=4$ processes `a,b,a,c,a,b,d,a,e,a,b,a`.

**Reasoning.** Before `d`, counters are `a:3,b:2,c:1`; the untracked arrival cancels one from all four distinct identities, leaving `a:2,b:1`. Later updates yield `a:5,b:2,e:1`. True counts are 6, 3, 1, 1, 1; $D=1$, so every underestimate is at most one.

**Conclusion.** Cancellation explains both compressed state and a checkable error certificate.

### Example 3

**Situation.** A unit stream has $n=1{,}000{,}000$ and Misra–Gries uses $k=101$.

**Reasoning.** At most 100 candidates are stored, $D\le\lfloor1{,}000{,}000/101\rfloor=9{,}900$, and every item with frequency greater than $1{,}000{,}000/101\approx9{,}900.99$ is present. An item at exactly 9,900 has no inclusion guarantee.

**Conclusion.** Space, additive error, and strict threshold follow from one parameter.

### Example 4

**Situation.** A Misra–Gries candidate's stored count is below the reporting threshold.

**Reasoning.** The stored count is a lower bound, not proof that the true count is low. Add $D$ to form an upper bound. If the interval crosses the threshold, retain it as uncertain or count that candidate exactly in a second pass.

**Conclusion.** Candidate generation needs an explicit verification or gray-zone policy.

### Example 5

**Situation.** The executable Count–Min trace estimates absent item 6 as four.

**Reasoning.** Under both illustrative hashes, item 6 collides with item 1, whose frequency is four. Every relevant bucket therefore contains collision mass four; taking the minimum cannot remove a collision shared by all rows.

**Conclusion.** One-sided error permits false positive mass and does not prove membership.

### Example 6

**Situation.** Configure Count–Min with $\varepsilon=0.001$ and $\delta=10^{-6}$.

**Reasoning.** Width is $\lceil e/0.001\rceil=2719$ and depth is $\lceil\ln10^6\rceil=14$, giving 38,066 counters. At eight bytes each the array alone uses 304,528 bytes, about 297.4 KiB.

**Conclusion.** The theorem's counter count is not the whole process memory budget.

### Example 7

**Situation.** One million predetermined dashboard queries must all satisfy a joint failure budget $10^{-6}$.

**Reasoning.** Giving each query failure $10^{-6}$ permits a union-bound total up to one, not $10^{-6}$. A simple allocation uses $10^{-12}$ per query, requiring depth $\lceil\ln10^{12}\rceil=28$; adaptive use may need more careful analysis.

**Conclusion.** Probability must be budgeted over the product's answer surface.

### Example 8

**Situation.** A Count–Min implementation accepts `+5` then `-5` for an item and retains the insertion-only theorem.

**Reasoning.** Other keys' negative collision mass can make some queried bucket smaller than the target's true frequency. The minimum no longer has a nonnegative-noise interpretation even if every true coordinate happens to stay nonnegative.

**Conclusion.** Supporting a deletion syntax does not preserve the insertion-only proof.

### Example 9

**Situation.** Two partitions use width 1000 and depth 8 but different seeds.

**Reasoning.** Coordinate $(r,c)$ represents different key sets in the two arrays. Elementwise addition cannot represent the union stream under either seed set. Replaying updates, retaining separate sketches, or rebuilding is required.

**Conclusion.** Equal dimensions are necessary but insufficient for a valid merge.

### Example 10

**Situation.** A source retries 1% of records, and both the sketch and its “exact” test map consume the duplicated transport stream.

**Reasoning.** They can agree perfectly while overcounting logical events by workload-dependent amounts. Reconcile stable event IDs or committed source offsets against an independent ledger, and define whether repeats are domain events or transport duplicates.

**Conclusion.** Sketch accuracy cannot compensate for an incorrect population.

## Cross-Program Connections

- **Data Structures Engineering:** hash tables, arrays, heaps, counters, and serialization implement summary state.
- **Data Engineering:** offsets, event time, watermarks, replay, deduplication, and partitioning define the input stream.
- **Database Engineering:** approximate query processing and optimizer statistics consume estimates with decision-specific costs.
- **Distributed Systems Engineering:** compatible merges, checkpoints, retries, fencing, and recovery preserve summary semantics.
- **Security Engineering:** chosen-key collisions, tenant exhaustion, poisoning, and threshold actions define adversarial risk.
- **Platform Engineering:** quotas, state versioning, telemetry, rollout, and fallback make summaries operable.
- **Data Architecture Engineering:** canonical identity and metric meaning determine what a “frequency” denotes.
- **Algorithm Engineering:** [ALGE-068](./068-monte-carlo-and-las-vegas-algorithms.md) supplies probability discipline; ALGE-075 and ALGE-076 develop distinct-count and quantile summaries.

## References

1. Jayadev Misra and David Gries, “Finding Repeated Elements,” *Science of Computer Programming* 2(2), 1982, 143–152. DOI: [10.1016/0167-6423(82)90012-0](https://doi.org/10.1016/0167-6423(82)90012-0). Primary source for deterministic cancellation counters; publisher record checked 2026-09-05.
2. Graham Cormode and S. Muthukrishnan, “An Improved Data Stream Summary: The Count-Min Sketch and Its Applications,” *Journal of Algorithms* 55(1), 2005, 58–75. DOI: [10.1016/j.jalgor.2003.12.001](https://doi.org/10.1016/j.jalgor.2003.12.001). Primary source for Count–Min point-query analysis; publisher record checked 2026-09-05.
3. Moses Charikar, Kevin Chen, and Martin Farach-Colton, “Finding Frequent Items in Data Streams,” *Theoretical Computer Science* 312(1), 2004, 3–15. DOI: [10.1016/S0304-3975(03)00400-6](https://doi.org/10.1016/S0304-3975(03)00400-6). Primary source for Count Sketch frequent-item estimation; publisher record checked 2026-09-05.
4. Noga Alon, Yossi Matias, and Mario Szegedy, “The Space Complexity of Approximating the Frequency Moments,” *Proceedings of STOC 1996*, 20–29. DOI: [10.1145/237814.237823](https://doi.org/10.1145/237814.237823). Primary source for the streaming model and frequency-moment bounds; ACM record checked 2026-09-05.
5. S. Muthukrishnan, *Data Streams: Algorithms and Applications*, Foundations and Trends in Theoretical Computer Science 1(2), 2005, 117–236. DOI: [10.1561/0400000002](https://doi.org/10.1561/0400000002). Research monograph for stream models and algorithmic foundations; publisher record checked 2026-09-05.
6. Ahmed Metwally, Divyakant Agrawal, and Amr El Abbadi, “Efficient Computation of Frequent and Top-k Elements in Data Streams,” *Proceedings of ICDT 2005*, 398–412. DOI: [10.1007/978-3-540-30570-5_27](https://doi.org/10.1007/978-3-540-30570-5_27). Primary source for the Space-Saving algorithm; proceedings record checked 2026-09-05.
7. Graham Cormode and Marios Hadjieleftheriou, “Finding the Frequent Items in Streams of Data,” *Communications of the ACM* 52(10), 2009, 97–105. DOI: [10.1145/1562764.1562789](https://doi.org/10.1145/1562764.1562789). Comparative review of frequent-item methods; ACM record checked 2026-09-05.
8. Graham Cormode and Marios Hadjieleftheriou, “Finding Frequent Items in Data Streams,” *Proceedings of the VLDB Endowment* 1(2), 2008, 1530–1541. DOI: [10.14778/1454159.1454238](https://doi.org/10.14778/1454159.1454238). Empirical comparison and baseline implementations; official VLDB record checked 2026-09-05.

## Exercises

### Exercise 1

Distinguish point frequency, frequent-item discovery, and top-$q$ reporting. For each, state the required input and one output guarantee that must be explicit.

### Exercise 2

Derive the Misra–Gries error and candidate guarantees for $k-1$ counters. Explain strict threshold equality, zero-length streams, and what a second pass adds.

### Exercise 3

A Count–Min service uses $\varepsilon=0.002$, $\delta=10^{-5}$, eight-byte counters, and 50,000 predetermined queries under one joint $10^{-5}$ failure budget. Compute standard per-query dimensions, explain why they do not meet the joint claim, and give a union-bound configuration.

### Exercise 4

Design a mergeable frequency-summary service across 200 partitions. Specify update semantics, identity, algorithm choice, parameters, seeds, state envelope, merge validation, arithmetic, probability budget, oracle tests, and incompatible-state behavior.

### Exercise 5

A fraud team wants an approximate stream summary to freeze accounts whose hourly count exceeds a threshold. Design a safer decision system covering approximation direction, gray zones, adversarial keys, late events, duplicates, exact verification, human authority, auditing, rollback, and invalidation conditions.

## Answers to the Exercises

### Answer 1

A point query receives an item identity and returns an estimate or interval for its frequency; it must state additive or relative error, probability scope, update model, and window. Frequent-item discovery receives a threshold and must return identities, stating false-negative protection and the false-positive or gray zone. Top-$q$ reporting returns identities and perhaps estimates or ordering; it must define ties and whether membership or order is approximate. A point-only sketch without retained identities cannot enumerate either candidate set by itself.

### Answer 2

Each full-table miss cancels the arriving identity and one occurrence from each of $k-1$ distinct tracked identities. If $D$ cancellations occur, their disjoint groups consume $kD$ of $n$ unit occurrences, so $D\le\lfloor n/k\rfloor$. Stored count $\widehat f_i$ is uncancelled mass, hence $0\le f_i-\widehat f_i\le D$. If $f_i>n/k$ but $i$ were absent, all its occurrences would have been cancelled, contradicting $f_i\le D\le n/k$. Equality is not covered by the strict contradiction and may be omitted. For $n=0$, $D=0$ and the empty summary is exact. A second pass counts the at most $k-1$ candidates exactly and removes false positives.

### Answer 3

Standard pointwise dimensions are $w=\lceil e/0.002\rceil=1360$ and $d=\lceil\ln10^5\rceil=12$, giving 16,320 counters or 130,560 bytes before overhead. Reusing per-query failure $10^{-5}$ across 50,000 answers permits a union-bound joint failure up to 0.5. Allocate per-query failure at most $10^{-5}/50{,}000=2\times10^{-10}$; then $d=\lceil\ln(5\times10^9)\rceil=23$, width remains 1360, and the array has 31,280 counters or 250,240 bytes. This covers predetermined queries by a union bound, not arbitrary adaptive querying.

### Answer 4

Define nonnegative logical-event weights over a canonical tenant-qualified key and an event-time window with explicit lateness. Count–Min is suitable for supplied-key point estimates; add a candidate structure if enumeration is required. Give every partition identical width, depth, checked counter type, the same independently generated row-seed suite, key schema, algorithm version, and probability allocation. Persist those fields plus window, source offsets, creation and closure times, partition IDs, checksum, and provenance. Merge only matching envelopes by elementwise addition, rejecting mismatches. Test each partition and merges against independent exact ledgers on exhaustive-small, skewed, replay, duplicate, overflow, empty, and missing-partition cases. Report incomplete windows rather than fabricating zeroes, and rebuild or retain separate incompatible summaries.

### Answer 5

Treat sketch output as screening evidence, not autonomous proof. Define logical transactions and deduplicate stable event IDs; use event-time windows with visible watermark and correction policy. Because Count–Min overestimates in its insertion model, establish a gray band around the threshold and verify candidate accounts from an independent exact ledger before restriction. Protect seeded hashes and rate-limit chosen-key abuse; audit empirical collisions and key normalization. Require policy-authorized human or rules-based confirmation proportional to harm, log evidence and overrides, and offer appeal. Rollback disables new automated actions but must separately release or review existing freezes. Duplicate spikes, late-data surges, seed exposure, saturation, missing partitions, schema or policy change, audit-bound breach, drift, or exact-ledger disagreement invalidate automation and trigger conservative fallback or rebuild.
