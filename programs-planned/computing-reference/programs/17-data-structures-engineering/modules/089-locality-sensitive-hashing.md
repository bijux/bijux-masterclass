---
module_id: DSE-089
program: Data Structures Engineering
level: 2
module_number: 89
title: Locality-Sensitive Hashing
status: complete
last_verified: 2026-08-30
---

# Locality-Sensitive Hashing

## One-Page Review

### Governing question

How can randomized hash collisions generate high-dimensional similarity candidates with a quantified recall/false-candidate trade-off and an exact reranking boundary?

### Essential definitions

A locality-sensitive hash family $\mathcal H$ is designed so nearby objects collide more often than far objects. In the threshold form, a family is $(r,cr,p_1,p_2)$-sensitive when

$$
d(x,y)\le r\Rightarrow\Pr[h(x)=h(y)]\ge p_1,
$$

$$
d(x,y)>cr\Rightarrow\Pr[h(x)=h(y)]\le p_2,
$$

with $c>1$ and $p_1>p_2$. Concatenating $K$ independently sampled hashes creates one table key $g=(h_1,\ldots,h_K)$: near collision is at least $p_1^K$, far collision at most $p_2^K$. Using $L$ independent tables gives candidate probability

$$
1-(1-p^K)^L
$$

for a pair whose single-hash collision probability is $p$.

### Central model, mechanism, or theorem

AND amplification through $K$ reduces both good and bad collisions; OR amplification through $L$ restores near-neighbor recall while spending memory and probes. The classic exponent

$$
\rho=\frac{\ln(1/p_1)}{\ln(1/p_2)}<1
$$

governs idealized sublinear trade-offs in the Indyk–Motwani framework. It is not an end-to-end latency guarantee.

Random-hyperplane LSH hashes a vector by the sign of a random dot product; for angle $\theta$, collision probability is $1-\theta/\pi$. MinHash collision equals Jaccard similarity under the permutation model. p-stable families target $L_p$ distance. The family must match the similarity.

### Critical invariants

- Vectors/sets, normalization, metric, and similarity semantics are versioned.
- Each table's sampled functions and seed identities remain stable.
- Hash concatenation and table independence match the probability calculation.
- Candidate union is deduplicated before exact distance/ranking.
- Approximation or recall claims include thresholds, data/query distribution, $(K,L)$, probes, and failure definition.
- Empty buckets trigger a declared fallback rather than a fabricated neighbor.
- Online updates, deletions, and rebuilds keep every live ID's bucket membership consistent.

### Common failures

Failures include using ordinary hash uniformity as locality sensitivity, using hyperplane hashes on unnormalized vectors while promising cosine semantics, swapping Jaccard and cosine, treating hash equality as final similarity, tuning on the test set, assuming correlated bits are independent, merging indexes with different seeds, ignoring hot buckets, counting duplicate table hits as distinct candidates, and reporting only recall without memory, candidate count, build cost, or exact distance work.

### Compact example

Two teaching tables each concatenate three fixed hyperplane signs over eight three-dimensional vectors. Query $(92,8,0)$ has signature $(1,1,1)$ in both. Table zero returns A/B/C; table one A/B/G/H; union and deduplication yields five candidates. Exact squared-distance reranking returns B at distance 8, matching exhaustive search while avoiding three distance evaluations. Fixed planes demonstrate mechanics, not probability quality.

### Connections

[DSE-088](088-r-trees.md) supplies candidate/recheck boundaries and index-operational discipline. The roadmap successor is [DSE-090, “HNSW and Approximate Nearest-Neighbor Graphs”](../ROADMAP.md), which generates candidates through navigable graph search instead of randomized buckets. Vector Search, Information Retrieval, Security, and Data Engineering own feature semantics, evaluation, adversaries, and distributed index lifecycle.

## Governing Question

How should an LSH family and its amplified multi-table index be derived, built, queried, updated, and evaluated so that probabilistic candidates support a defensible approximate-neighbor service?

## Why This Matters

High-dimensional exact indexes often examine most data. LSH changes the goal: use a metric-specific randomized partition so nearby pairs share buckets with higher probability, then verify only candidates. It provides a principled route to sublinear approximate near-neighbor trade-offs for suitable spaces.

But an LSH “hash” is not a checksum and a bucket hit is not an answer. Amplification assumptions, feature normalization, table seeds, hot buckets, storage multiplication, exact reranking, filtering, updates, and evaluation all affect the service. The useful object is the whole candidate pipeline and its recall/cost curve.

## Prerequisites and Retrieval

Retrieve:

- conditional probability, independent repetition, logarithms, and union events;
- cosine/angle, Jaccard, $L_p$ distance, normalization, and approximate-neighbor contracts;
- hash-family seeds, canonical encoding, inverted bucket postings, and deduplication;
- candidate/exact-recheck separation from [DSE-088](088-r-trees.md);
- precision, recall, false candidates, latency distributions, and train/validation/test separation.

Ordinary cryptographic or hash-table hashes try to decorrelate similar inputs. LSH intentionally preserves a chosen locality relation probabilistically. A family valid for one metric does not become valid for another because both accept vectors.

## Learning Objectives

After this chapter, you should be able to:

1. state and interpret $(r,cr,p_1,p_2)$-sensitivity;
2. derive $K$-concatenation and $L$-table collision probabilities;
3. explain MinHash, random-hyperplane, and p-stable family/metric matches;
4. design candidate union, multiprobe, filtering, reranking, and fallback;
5. specify seed, feature, bucket, update, deletion, and rebuild invariants;
6. diagnose dependence, hot buckets, drift, adversarial collisions, and misleading evaluation;
7. measure recall/cost/latency across held-out and adversarial workloads.

## Core Exposition

### Near-neighbor promise and LSH family

The $(r,cr)$-near-neighbor decision problem asks: if some indexed point lies within distance $r$ of query $q$, return a point within distance $cr$ with stated probability. This promise form differs from always returning the exact nearest or a $(1+\epsilon)$-approximate nearest for every query. Conversions and repeated radii need their own analysis.

An LSH family supplies a random partition distribution. Nearby pairs collide with probability at least $p_1$; sufficiently far pairs collide with probability at most $p_2$. Points in the gap $(r,cr]$ have no threshold promise. The probability is over construction randomness for a fixed pair under stated preprocessing—not over an unspecified “typical request.”

Useful families require $p_1>p_2$. The ratio matters more than either value alone. A high $p_1$ with nearly equal $p_2$ creates huge buckets; a low $p_2$ with tiny $p_1$ misses neighbors. Feature representation and metric determine the collision curve.

### AND/OR amplification

Build one table key by sampling $K$ hashes and requiring all component values to match. Under independence, a pair with collision probability $p$ in one hash collides in the concatenated key with probability $p^K$. This sharply suppresses far pairs but also suppresses near pairs.

Build $L$ independently sampled tables and accept a pair if any table collides. The miss probability is $(1-p^K)^L$, hence candidate probability $1-(1-p^K)^L$. For near threshold, target recall $R$ suggests

$$
L\ge\frac{\ln(1-R)}{\ln(1-p_1^K)}.
$$

Ceil the result and re-evaluate with actual finite/randomness behavior. If component hashes or tables are correlated, these products are not justified. Generating many bits from one projection or reusing seed streams can reduce effective independence.

Larger $K$ yields smaller buckets and lower recall per table. Larger $L$ restores recall at proportional bucket storage and query lookups. Tuning jointly considers posting reads, deduplication, exact distances, cache, and tail hot buckets.

### Classic space-time exponent

The Indyk–Motwani framework chooses amplification so far candidates remain controlled while near collision survives across tables. The exponent $\rho=\ln(1/p_1)/\ln(1/p_2)$ lies between zero and one when $1>p_1>p_2>0$. Idealized query and space terms involve $n^\rho$ and $n^{1+\rho}$ in a classic regime.

These are asymptotic framework results, not direct capacity numbers. Constants, dimension, hash evaluation, bucket storage, skew, multiprobe, filters, updates, and reranking dominate many systems. Report observed candidate fraction and exact work.

### Random-hyperplane LSH

For nonzero vectors and angular/cosine similarity, sample a random vector $a$ from a rotationally symmetric distribution and define

$$
h_a(x)=\mathbf1[a\cdot x\ge0].
$$

The probability two vectors receive the same sign is $1-\theta(x,y)/\pi$, where $\theta\in[0,\pi]$ is their angle. Magnitude does not affect the sign, matching angular similarity; normalize vectors if the service reports cosine distance and handle zero vectors explicitly.

A concatenated signature is often called SimHash in applications, but a finite bit Hamming distance estimates angle; exact signature equality is a stricter bucket event. Quantized numeric precision, dot-product implementation, zero-dot tie policy, and projection generation/version must be stable across build and query.

### MinHash for set similarity

For sets $A,B$, Jaccard similarity is $|A\cap B|/|A\cup B|$. Under a uniformly random permutation, the probability their minimum permuted element agrees equals Jaccard similarity. Practical MinHash uses hash functions approximating min-wise independence. Empty sets need a convention; duplicate tokens should first become a set if Jaccard is intended.

Banding a MinHash signature is another AND/OR construction: require equality across rows in a band and accept any matching band. Weighted Jaccard needs consistent weighted sampling, not ordinary MinHash. Tokenization, shingles, stop words, and normalization often matter more than the index.

### p-stable LSH

For $L_p$ metrics where p-stable distributions apply, sample vector $a$ with p-stable coordinates and offset $b\sim\mathrm{Uniform}[0,w)$, then hash

$$
h_{a,b}(v)=\left\lfloor\frac{a\cdot v+b}{w}\right\rfloor.
$$

Bucket width $w$ trades collision selectivity. The collision probability decreases with $L_p$ distance according to the family. Euclidean $L_2$ uses Gaussian-stable projections; $L_1$ uses Cauchy-stable projections. Heavy-tailed draws, finite precision, overflow, and reproducible random generation need testing.

### Candidate pipeline

At build time, compute all $L$ table keys and append the record ID to each posting. At query time, compute keys, fetch postings, union and deduplicate IDs, apply metadata filters, compute the authoritative distance for candidates, and select results with deterministic ties. If the candidate set is empty or too large, apply a declared fallback or budget policy.

Multiprobe LSH inspects nearby buckets in a likelihood order rather than storing many tables. It trades extra probes for memory. Probe sequences are family-specific: flipping low-margin hyperplane bits or neighboring p-stable bins needs a probability rationale. A generic adjacent integer bucket is not universally meaningful.

Filters complicate recall. Post-filtering can remove all retrieved candidates; prefilter-specific indexes multiply state. Evaluation must define recall against eligible exact neighbors, not against the unfiltered universe.

### Bucket and lifecycle engineering

An index envelope includes feature/model/schema version, metric, normalization, family, $(r,c,p_1,p_2)$ calibration, $(K,L)$, projection/seed IDs, numeric/tie conventions, bucket encoding, ID namespace, generation, and checksum. A query must use the same transformation and tables.

Updates compute new memberships before publication. Feature changes remove old postings and add new ones atomically or version the record. Tombstones require compaction; stale IDs waste reranking and can leak deleted records. Rebuilds dual-write or replay a delta, validate recall, then atomically publish all table roots/configuration together.

Hot buckets threaten memory and latency. Cap postings only with an explicit recall policy, split by a secondary locality family, multiprobe narrower keys, or fall back. Attackers who know projections may craft collisions. Protect seeds where appropriate, validate dimensions/norms, limit bucket/query work, and monitor concentration.

### Evaluation

Build an exact held-out oracle. Measure recall@k, threshold success, approximation ratio, candidate fraction, unique candidates, posting bytes, probes, exact distance calls, build/update/delete cost, memory, and p50/p95/p99 latency. Stratify by density, norm, filter selectivity, time, language, and protected groups where relevant.

Avoid tuning on the test set. Use training/calibration for representation and $(K,L)$, validation for choices, and a held-out test for reporting. Test feature drift, adversarial near thresholds, duplicates, zero vectors, empty sets, hot buckets, corrupt tables, missing shards, and seed/version mismatch. Probability formulas calibrate; measurements validate the deployed pipeline.

The bounded model below uses two tables of three fixed hyperplanes over eight integer vectors. It demonstrates signatures, table union, deduplication, and exact reranking. Fixed planes are not random samples, the fixture does not estimate collision probabilities or recall distributions, and it is not a production cosine index.

<!-- bijux-verify: {"id":"hyperplane-lsh-pipeline","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"dimensions=3\nvectors=8\ntables=2\nhashes_per_table=3\nquery=(92, 8, 0)\nquery_signatures=[(1, 1, 1), (1, 1, 1)]\ntable_0_hits=['A', 'B', 'C']\ntable_1_hits=['A', 'B', 'G', 'H']\nunique_candidates=['A', 'B', 'C', 'G', 'H']\ncandidate_count=5\nexact_nearest=B\nexact_distance_squared=8\nreranked_nearest=B\nreranking_matches_bruteforce=True\nvalid=True\nevidence=hyperplane_lsh_model\n","stderr":""}} -->
```python
VECTORS = {
    "A": (100, 0, 0),
    "B": (90, 10, 0),
    "C": (70, 70, 0),
    "D": (0, 100, 0),
    "E": (-100, 0, 0),
    "F": (0, 0, 100),
    "G": (80, 0, 20),
    "H": (60, 10, 30),
}
TABLES = (
    ((1, -1, 0), (0, 1, -1), (1, 0, -1)),
    ((1, 1, -1), (1, -2, 0), (0, 1, 1)),
)


def dot(left, right):
    return sum(left[index] * right[index] for index in range(3))


def signature(vector, planes):
    return tuple(1 if dot(vector, plane) >= 0 else 0 for plane in planes)


def distance_squared(left, right):
    return sum(
        (left[index] - right[index]) ** 2
        for index in range(3)
    )


indexes = []
for planes in TABLES:
    buckets = {}
    for name, vector in VECTORS.items():
        key = signature(vector, planes)
        buckets[key] = buckets.get(key, []) + [name]
    indexes.append(buckets)

query = (92, 8, 0)
query_signatures = [
    signature(query, planes)
    for planes in TABLES
]
hits = [
    indexes[index].get(query_signatures[index], [])
    for index in range(len(TABLES))
]
unique_candidates = sorted(set(hits[0] + hits[1]))
reranked = min(
    (distance_squared(VECTORS[name], query), name)
    for name in unique_candidates
)
brute_force = min(
    (distance_squared(vector, query), name)
    for name, vector in VECTORS.items()
)
valid = reranked == brute_force and len(unique_candidates) == 5

print("dimensions=3")
print(f"vectors={len(VECTORS)}")
print(f"tables={len(TABLES)}")
print(f"hashes_per_table={len(TABLES[0])}")
print(f"query={query}")
print(f"query_signatures={query_signatures}")
print(f"table_0_hits={hits[0]}")
print(f"table_1_hits={hits[1]}")
print(f"unique_candidates={unique_candidates}")
print(f"candidate_count={len(unique_candidates)}")
print(f"exact_nearest={brute_force[1]}")
print(f"exact_distance_squared={brute_force[0]}")
print(f"reranked_nearest={reranked[1]}")
print(f"reranking_matches_bruteforce={reranked == brute_force}")
print(f"valid={valid}")
print("evidence=hyperplane_lsh_model")
```

## Definitions and Notation

- $(r,cr)$: near and sufficiently-far distance thresholds; $c>1$.
- $(p_1,p_2)$: lower near-collision and upper far-collision probabilities.
- $K$: hashes concatenated per table; $L$: independent tables.
- $\rho$: classic LSH space-time exponent.
- **Candidate recall**: fraction of exact eligible neighbors appearing before reranking.
- **Reranking**: authoritative metric evaluation and sorting over candidates.
- **Multiprobe**: querying multiple likely buckets per table.
- **Hot bucket**: posting list whose size dominates cost or risk.
- **Feature/index generation**: atomic version of transformation, projections, buckets, and postings.

## Mechanisms, Invariants, or Proof Structure

### Amplification proof

If $K$ hash events are independent with probability $p$, all collide with probability $p^K$. If $L$ table events are independent, none collide with probability $(1-p^K)^L$; complement gives candidate probability. Applying near lower and far upper bounds preserves the inequality directions.

### Family proofs

Random-hyperplane collision follows from rotational symmetry: a random separating plane falls in the angular wedge between two vectors with probability $\theta/\pi$. MinHash equality occurs precisely when the minimum permuted union element belongs to the intersection, probability Jaccard. p-stable projection differences scale with $L_p$ distance before shifted binning.

### Systems invariants

- build/query share feature, metric, numeric, family, seed, (K,L), and bucket encoding;
- every live ID appears in its computed buckets exactly once per table under posting semantics;
- candidate IDs are deduplicated and filtered before authoritative distance;
- budgets/fallbacks never silently masquerade as full recall;
- evaluation uses held-out exact oracles and reports missing/corrupt shards;
- generation publication and deletion prevent cross-version or stale results.

## Alternatives and Trade-Offs

Exact scans maximize recall and batch well on accelerators. k-d/ball trees work in lower intrinsic dimension. HNSW and other graphs often provide strong empirical vector recall but need mutable graph lifecycle and lack the same classic LSH probability structure. Inverted files with product quantization compress candidates and distances. Trees or prefix indexes suit sets/strings under other relations. Learned embeddings change the similarity problem before indexing.

Larger $K$ cuts candidates but needs more $L$ or probes. Larger $L$ spends memory and lookup fanout. Multiprobe spends query CPU instead of duplicate tables. MinHash suits Jaccard; hyperplanes suit angle; p-stable bins suit corresponding $L_p$. Data-dependent hashing can improve trade-offs but increases training, drift, and validation obligations. Use the simplest family whose theorem matches the metric and whose measured curve meets service constraints.

## Failure Modes and Misconceptions

- **Any hash can be locality sensitive.** The collision-distance relation must be proved or characterized.
- **One bucket hit proves similarity.** It creates a candidate for exact scoring.
- **More concatenated bits always improve search.** Recall can collapse without more tables/probes.
- **More tables are free recall.** They multiply memory, lookups, postings, and deduplication.
- **Projection bits are independent because seeds differ.** Generator or data correlations may remain.
- **Cosine and dot product are interchangeable.** Norm changes ranking unless normalization is part of the contract.
- **MinHash counts duplicate tokens.** Ordinary Jaccard is a set relation.
- **No candidate means no neighbor.** It may be an LSH miss and needs declared fallback.
- **Capping a hot bucket preserves guarantees.** It can delete the true neighbor.
- **Exact reranking restores missed recall.** It only orders generated candidates.
- **Offline recall survives feature drift.** Representation/model change shifts collision behavior.
- **Average latency describes bucket risk.** Tail postings and filters dominate p99.
- **Publishing table roots independently is safe.** Mixed generations change candidate probability and visibility.

## Worked Examples

### Example 1

**AND amplification.** With near single-hash probability $p_1=0.8$ and $K=4$, one table's near collision is $0.8^4=0.4096$. For far $p_2=0.2$, it is $0.0016$. **Conclusion:** concatenation strongly separates probabilities while discarding many near pairs per table.

### Example 2

**OR amplification.** With per-table near collision 0.4096 and $L=8$, candidate probability is $1-(1-0.4096)^8\approx0.9852$. Far candidate probability is $1-(1-0.0016)^8\approx0.0127$. **Conclusion:** tables restore recall and also accumulate false candidates.

### Example 3

**Table count.** If $p_1^K=0.25$ and desired recall is 0.95, $L\ge\ln(0.05)/\ln(0.75)\approx10.413$, so choose 11 tables before empirical calibration. **Conclusion:** integer sizing follows the miss budget.

### Example 4

**Hyperplane angle.** Orthogonal vectors have $\theta=\pi/2$, so one random-hyperplane bit collides with probability $1-1/2=0.5$. Opposite vectors have probability zero under a zero-tie-free model. **Conclusion:** signature equality reflects angular locality, not Euclidean magnitude.

### Example 5

**MinHash.** Sets $\{a,b,c,d\}$ and $\{b,c,e\}$ have intersection size two and union size five, so a MinHash component agrees with probability $2/5$. **Conclusion:** tokenization and set formation define the collision law.

### Example 6

**Deduplication.** Fixture candidate A appears in both tables but causes one exact distance calculation after set union. Counting both as candidates exaggerates work and can duplicate results. **Conclusion:** posting hits and unique candidates are different metrics.

### Example 7

**Empty bucket.** A query hits no posting at (K=16,L=4). The service probes likely neighbor buckets and, if still empty, uses a bounded exact shard scan; it records fallback. **Conclusion:** absence is an index event, not proof of isolation.

### Example 8

**Filter recall.** The unfiltered nearest candidate is in another tenant and removed. Recall must compare with the nearest eligible same-tenant point, which may never share a bucket. **Conclusion:** evaluate the actual filtered problem.

### Example 9

**Feature drift.** A new embedding model rotates vector space while old projections and postings remain. Query signatures no longer correspond to stored features. **Conclusion:** feature and index generation publish atomically or require dual indexes.

### Example 10

**Adversarial hot bucket.** Many crafted vectors share all positive signs and create a million-ID posting. Work limits protect latency, but truncation changes recall. Keyed/rotated projections, bucket monitoring, and fallback are required. **Conclusion:** probabilistic indexing needs abuse and resource policy.

## Cross-Program Connections

- **Vector Search:** LSH is a candidate generator compared with graph, quantization, and inverted-file indexes.
- **Information Retrieval:** MinHash, shingling, deduplication, and cosine features depend on document representation.
- **Machine Learning Engineering:** embedding normalization, model rollout, drift, and evaluation define the indexed metric.
- **Data Engineering:** distributed table builds, postings, deletes, compaction, and atomic generations own freshness.
- **Security Engineering:** seed exposure, collision attacks, hot buckets, and deleted-ID leakage require controls.
- **Experimentation:** held-out exact oracles, recall curves, tail latency, and stratification prevent misleading claims.

## References

1. Piotr Indyk and Rajeev Motwani, [Approximate Nearest Neighbors: Towards Removing the Curse of Dimensionality](https://www.cs.princeton.edu/courses/archive/spr04/cos598B/bib/IndykM-curse.pdf), *STOC*, 1998.
2. Aristides Gionis, Piotr Indyk, and Rajeev Motwani, [Similarity Search in High Dimensions via Hashing](https://sigmod.org/publications/dblp/db/conf/vldb/GionisIM99.html), *VLDB*, 1999.
3. Aristides Gionis, Piotr Indyk, and Rajeev Motwani, [Similarity Search in High Dimensions via Hashing](https://www.cs.columbia.edu/~verma/classes/uml/ref/nn_lsh_gionis_indyk_motwani.pdf), university-hosted paper copy.
4. Moses S. Charikar, [Similarity Estimation Techniques from Rounding Algorithms](https://courses.compute.dtu.dk/02289/2022/approxds/charikar.pdf), *STOC*, 2002.
5. Mayur Datar, Nicole Immorlica, Piotr Indyk, and Vahab S. Mirrokni, [Locality-Sensitive Hashing Scheme Based on p-Stable Distributions](https://people.csail.mit.edu/nickle/pubs/pstable.pdf), *SoCG*, 2004.
6. Tobias Christiani, [Fast Locality-Sensitive Hashing Frameworks for Approximate Near Neighbor Search](https://arxiv.org/abs/1708.07586), 2017.
7. Piotr Indyk, [Publication Record and LSH Resources](https://people.csail.mit.edu/indyk/p.html), accessed 2026-08-30.

## Exercises

### Exercise 1

For $p_1=0.75,p_2=0.25,K=5,L=12$, compute near and far per-table collision and any-table candidate probabilities.

### Exercise 2

Derive the minimum $L$ for target near recall 0.99 when $p_1=0.7,K=3$. State the independence assumption.

### Exercise 3

A cosine LSH service loses recall after an embedding rollout although (K,L) and seeds did not change. Diagnose and plan a safe migration.

### Exercise 4

Design a distributed LSH index envelope and publication workflow supporting updates, deletes, hot-bucket protection, multiprobe, filters, and fallback.

### Exercise 5

Choose candidate methods for document Jaccard deduplication, normalized image embeddings, and unnormalized Euclidean sensor vectors. Define theorem and empirical evidence.

## Answers to the Exercises

### Answer 1

Near per-table probability is $0.75^5=0.2373046875$; far is $0.25^5=0.0009765625$. Near any-table probability is $1-(1-0.2373046875)^{12}\approx0.9613$. Far any-table probability is $1-(1-0.0009765625)^{12}\approx0.01166$. These values assume independent component hashes and independent table keys.

### Answer 2

Per-table near collision is $0.7^3=0.343$. Require $1-(1-0.343)^L\ge0.99$, so

$$
L\ge\frac{\ln(0.01)}{\ln(0.657)}\approx10.97.
$$

Choose 11 tables. The product/complement calculation assumes independently sampled component hashes and table constructions for the fixed pair; measured dependence may require more.

### Answer 3

Check model/version, dimension, normalization, zero-vector policy, numeric precision, and whether stored postings were rebuilt from new vectors. Even a rotation preserving some semantic quality changes fixed projection signs. Build a new generation with new feature schema and calibrated projections; dual-write/replay updates; measure held-out exact recall, candidates, filters, and latency against the new metric. Atomically route queries to matching feature/index versions, retain rollback, and never query old postings with new embeddings.

### Answer 4

The envelope contains feature/model/schema, metric/normalization, family, thresholds/calibration, (K,L), projection and RNG versions/seeds, bucket encoding, ID namespace, filter scope, generation, shard/table IDs, payload checksum, and source offset. Builders emit immutable table shards; a manifest publishes a complete generation atomically after posting/count/checksum and exact-recall validation. Updates compute all new memberships and tombstone old generation entries transactionally; compaction removes stale IDs. Query deduplicates, applies eligible filters, reranks exactly, limits work with a reported policy, multiprobes family-specific buckets, and invokes a monitored fallback. Hot-bucket alarms trigger rebuild/secondary partitioning rather than silent truncation.

### Answer 5

For document set Jaccard, use MinHash plus bands after versioned shingling; verify component collision/Jaccard behavior and held-out duplicate recall. For normalized image embeddings under cosine/angle, use random-hyperplane or a stronger vector ANN baseline; verify $1-\theta/\pi$ bits, recall@k, candidates, and drift. For unnormalized Euclidean sensor vectors, use p-stable (L_2) hashing or an exact/tree/graph alternative; hyperplane signs would ignore magnitude. Across all three, report memory, build/update cost, posting skew, unique candidates, exact distances, recall/approximation, tail latency, filter behavior, adversarial inputs, and versioned rebuild results.
