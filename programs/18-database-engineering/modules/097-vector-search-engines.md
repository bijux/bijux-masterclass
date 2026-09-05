---
module_id: DBE-097
program: Database Engineering
level: 2
module_number: 97
title: Vector Search Engines
status: complete
last_verified: 2026-09-05
---

# Vector Search Engines

## One-Page Review

### Governing question

How should a database retrieve semantically or geometrically similar items from high-dimensional vectors while making distance, approximation, filtering, freshness, model lineage, transactions, distribution, and evaluation explicit?

### Essential definitions

- An **embedding** is a vector produced by a named model and preprocessing pipeline; its coordinates have meaning only within that contract.
- A **distance** or **similarity** function orders candidates. Euclidean distance, inner product, and cosine similarity are not interchangeable without assumptions.
- **Exact $k$-nearest-neighbor search** evaluates enough candidates to guarantee the true top $k$ under the declared metric and tie rule.
- **Approximate nearest-neighbor (ANN) search** trades accuracy/completeness for latency, memory, build cost, or scale.
- **Recall@k** compares returned relevant true neighbors with an exact or governed ground truth; it is not application relevance by itself.
- An **HNSW graph** is a layered proximity graph navigated heuristically; build/search breadth and graph degree trade resources for recall.
- An **inverted-file (IVF) index** assigns vectors to coarse regions and probes selected regions at query time.
- **Product quantization (PQ)** compresses subvectors using learned codebooks and approximates distances.
- **Pre-filtering** constrains eligible candidates before/vector-during search; **post-filtering** removes ANN results afterward and can return too few or biased results.
- A **hybrid search** combines vector and lexical/structured signals under an explicit calibration and ranking contract.

### Central model, mechanism, or theorem

Let stored item $i$ have identity $id_i$, vector $x_i\in\mathbb{R}^d$, model contract $m_i$, metadata $a_i$, and visibility version $q_i$. A query vector $y$ may be compared only under compatible model, dimension, normalization, and distance semantics. The eligible exact answer is the $k$ smallest distances (or greatest similarities) among visible items satisfying filter $F(a_i)$, with deterministic tie-breaking.

ANN indexes return a candidate-dependent approximation. Correct engineering therefore reports quality and system behavior together: recall/relevance, p50 through tail latency, throughput at offered load, memory, index/build cost, update/delete visibility, filter selectivity, shard fan-out, and recovery.

### Critical invariants

- each vector records item identity, dimension, scalar encoding, model/version, preprocessing, normalization, and distance contract;
- non-finite values and dimension mismatches are rejected before indexing;
- eligibility filtering, authorization, deletion, and tenant boundaries cannot be bypassed by ANN approximation;
- returned IDs map to the same visible base-record versions used for filtering and scoring, or staleness is explicit;
- index updates, tombstones, rebuilds, and swaps cannot resurrect deleted or unauthorized items;
- distributed top-k merging uses comparable scores and enough shard candidates for the stated completeness/recall claim;
- benchmark ground truth, dataset split, queries, filters, ties, and metric are reproducible;
- model migration never compares incompatible vector spaces as if scores were calibrated.

### Common failures

- storing vectors without model and preprocessing lineage;
- using cosine distance on unnormalized data while assuming dot-product ranking equivalence;
- reporting recall against a flawed or differently filtered ground truth;
- tuning on the evaluation queries and leaking test distribution;
- post-filtering a top-10 ANN result when only 1% of items are eligible;
- treating vector similarity as factual, causal, safe, or authorized relevance;
- updating the base row and vector index on different consistency timelines without surfacing it;
- rebuilding an index in place and serving a mixture of generations;
- merging shard-local top-k without score comparability or sufficient overfetch;
- benchmarking a warm static index while production has deletes, model drift, churn, and failure.

### Compact example

For nonzero unit vectors $u$ and $v$, $\|u-v\|_2^2=\|u\|^2+\|v\|^2-2u\cdot v=2-2\cos(u,v)$. Thus minimizing squared Euclidean distance is equivalent to maximizing cosine similarity only after normalization. Without unit norms, magnitude changes the Euclidean and inner-product rankings.

### Connections

The previous module, [Graph Databases](096-graph-databases.md), covers explicit relationships; proximity indexes build algorithmic neighborhood structures over vector space. The roadmap's next module, [Database Observability and Capacity](../ROADMAP.md), evaluates the operational evidence needed for these indexes. Prerequisites include [Full-Text and Inverted Indexes](038-full-text-and-inverted-indexes.md), [Cost Models](065-cost-models.md), [Vectorized and Pipeline Execution](059-vectorized-and-pipeline-execution.md), and [Sharding and Data Placement](086-sharding-and-data-placement.md).

## Governing Question

A product wants semantic retrieval over documents, images, products, code, or events. Exact scanning every vector is simple and correct but may exceed latency and cost. Approximate indexes can search billions of vectors quickly but may miss the true neighbors, interact poorly with filters, lag updates, and expose model bias. What must be specified and measured before “similarity search” becomes a dependable database feature?

The answer treats embedding generation, vector identity, distance, candidate generation, filtering, ranking, versioning, transactions, distribution, and evaluation as one reproducible system. An index algorithm is only one component.

## Why This Matters

Vector search supports retrieval-augmented generation, recommendations, deduplication, anomaly detection, image/audio search, entity matching, and scientific similarity. It can find useful candidates where exact keywords or rigid schemas do not.

Its output is inherently model- and data-dependent. A high cosine score is not a probability unless separately calibrated. Approximate search adds another error source beyond embedding relevance. Metadata filters can change the search problem. Updating the embedding model creates a new coordinate system. Sensitive attributes can be inferred from neighborhoods.

Database engineering makes these limitations operationally explicit: durable identity, versioned index generations, consistent eligibility, correct deletion, bounded resource use, reproducible ground truth, and failure-safe rollout.

## Prerequisites and Retrieval

Retrieve vectors, norms, dot products, Euclidean distance, cosine, metric properties, heaps, graphs, clustering, quantization, inverted indexes, cache behavior, transactions, sharding, and ranking evaluation. Be able to distinguish mathematical nearest neighbor from human relevance.

Retrieve exact top-k selection: compute scores, apply eligibility, impose deterministic ties, and retain the best $k$. This supplies a ground-truth oracle for manageable datasets. Approximation must be compared to the same filter, metric, vector representation, and tie policy.

For a deployed engine, record version; vector type/dimension/precision; metric/operator; normalization; index family and parameters; build training sample; memory/disk layout; update/delete path; transaction visibility; filtering; replicas/shards; concurrency; model/preprocessing version; and query settings. Current behavior must be checked against official documentation.

## Learning Objectives

After completing this module, you should be able to:

1. define vector identity, compatibility, distance, eligibility, top-k, and tie semantics;
2. derive relationships among cosine, inner product, and Euclidean distance under stated assumptions;
3. explain HNSW, IVF, and PQ mechanisms and their recall/resource trade-offs;
4. design filtered and hybrid retrieval without authorization or completeness gaps;
5. evaluate recall, relevance, latency, throughput, memory, freshness, and recovery reproducibly;
6. migrate embedding/index generations without comparing incompatible spaces;
7. reason about distributed top-k, skew, overfetch, replication, and partial failure;
8. diagnose numerical, adversarial, privacy, and operational failure modes.

## Core Exposition

**Define the vector contract.** A stored vector needs dimension $d$, scalar type and endian/serialization, model artifact/version, tokenizer or feature extractor, preprocessing, truncation/windowing, pooling, normalization, and intended distance. The same model name with different preprocessing can yield incompatible vectors.

Reject wrong dimensions, NaN, positive/negative infinity, corrupt encodings, and unreasonable norms before they enter index state. Define whether zero vectors are permitted; cosine is undefined when a norm is zero. Record source content version so stale embeddings can be found and repaired.

**Separate item and vector identity.** One item may have title, body, image, or chunk embeddings; one source document may split into many chunks. Use a stable vector identity such as `(item_id, field, chunk_id, model_generation)`. Deleting the item must tombstone every active vector and derived candidate cache.

Chunking creates retrieval semantics. Boundaries, overlap, position, parent ID, language, and access policy affect results. A returned chunk is not automatically sufficient context, current, or authorized.

**Choose distance precisely.** Euclidean distance is $D_2(x,y)=\sqrt{\sum_j(x_j-y_j)^2}$. Squared Euclidean gives the same ranking without square root. Inner product is $x\cdot y=\sum_jx_jy_j$ and is a similarity, not generally a metric distance. Cosine similarity is $(x\cdot y)/(\|x\|\|y\|)$ for nonzero vectors.

For unit-normalized vectors, maximizing dot product, maximizing cosine, and minimizing squared Euclidean are equivalent rankings. For arbitrary norms they differ. If magnitude encodes confidence or popularity, normalization discards that signal; if magnitude is accidental, inner product may overfavor large norms.

**Define exact top-k.** First select visible authorized candidates satisfying metadata predicate $F$. Compute the declared score in sufficient precision, then order by score and stable ID tie-breaker. Exactness is relative to the stored representation and metric; floating implementations can differ at near ties.

For $N$ vectors of dimension $d$, brute-force scoring is $O(Nd)$ arithmetic with strong sequential/vectorized/GPU opportunities. Top-k selection can use a heap or partial selection. Exact scan can outperform an index on small, heavily filtered, or batch-friendly datasets.

**Define approximation quality.** If $T_k(y)$ is exact top-k and $A_k(y)$ approximate returned set, recall@k is $|T_k\cap A_k|/k$ under simple no-tie set semantics. With tied ground truth, define acceptable tie sets. Also report result count, distance ratio, precision or task relevance, and per-query distribution—not only mean recall.

ANN recall is not semantic relevance. Exact nearest embeddings can still be wrong for the user's task. Evaluate retrieval against both exact vector ground truth and human/domain judgments or downstream task outcomes, with separate metrics.

**Understand HNSW.** Hierarchical Navigable Small World indexes connect vectors in layered proximity graphs. Search begins in sparse upper layers and descends, maintaining a candidate frontier. Parameters controlling graph connections and construction/search breadth trade memory, build/update cost, latency, and recall.

HNSW is data-dependent and mutable implementations vary. Insert order can affect graph shape; deletes may be logical until cleanup; filters may require specialized traversal; high update churn fragments quality or memory. Current product parameters and transactional behavior must be sourced, not assumed from the paper.

**Understand IVF.** An inverted-file index trains coarse centroids, assigns vectors to one or more lists, then probes selected lists near the query. More probes generally improve recall and cost more. Poor training samples, distribution drift, or imbalanced clusters create long lists and missed regions.

Training and serving preprocessing must match. Empty/small clusters and heavy hitters need observation. Re-training creates a generation migration, not a silent parameter edit.

**Understand product quantization.** PQ partitions a vector into subvectors, quantizes each with a codebook, and stores compact code indices. Query-time lookup tables approximate distances cheaply. More bits/codebooks improve representation at memory/build cost; residual or optimized variants change assumptions.

Quantization error can reorder close neighbors and affect groups unequally. Validate exact vector retention, reranking, and rebuild options. Compression claims exclude metadata, centroids, graph/list structures, replicas, WAL, and free-space headroom unless explicitly included.

**Compose index families carefully.** IVF-PQ combines coarse pruning with quantized scoring. HNSW can route centroids or store full vectors. Disk-oriented graphs trade memory for storage I/O and caching. Names do not define identical behavior across libraries.

Choose a candidate generator, candidate budget, optional exact reranker, and stopping rule from measured quality/resource curves. A fixed parameter can behave differently by query density, filter, tenant, and drift.

**Filter as part of search.** Pre-filtering constructs or consults only eligible candidates, protecting correctness but possibly leaving sparse/disconnected ANN structures. Integrated filtering can traverse through ineligible nodes while returning only eligible items, which raises authorization questions: can forbidden vectors influence path/timing? Post-filtering top $k$ candidates is incomplete when eligibility is rare.

If eligible fraction is $p$ and candidates were independent uniform samples, expected eligible count among $n$ is $np$. To expect 10 eligible at $p=0.01$ requires 1,000 candidates, but ANN candidates are not independent or uniform. This is a warning model, not a correctness prescription.

Authorization is non-negotiable. A search must never return forbidden IDs, and cross-tenant vectors must not leak through caches, scores, counts, timing, or training. Prefer tenant/visibility-aware partitions or cryptographically/policy-isolated indexes when risk requires it.

**Combine hybrid signals explicitly.** Lexical retrieval handles exact terms, identifiers, rare names, and negation differently from embeddings. Hybrid search can union candidates and combine scores through normalization, rank fusion, or learned ranking. Raw BM25-like and cosine scores are not naturally calibrated.

Record each candidate source, version, score, normalization, weight, tie, and reranker. Evaluate ablations. A reranker can improve relevance while adding cost, nondeterminism, model drift, and external-service failure.

**Preserve base/index consistency.** The authoritative item, metadata, and vector may update atomically in one database or asynchronously across systems. Define read behavior for base-new/index-old, index-new/base-old, metadata filter changes, and deletion. Stable source version lets reads reject stale candidates or repair them.

Within one transactional engine, verify whether vector index changes share MVCC visibility and rollback. Extension support does not imply every index build/update has identical transactional semantics. Across systems, use durable change identity, idempotent application, replay position, dead-letter repair, and reconciliation.

**Handle deletes completely.** Remove logical eligibility immediately under the contract, even if graph/list bytes remain until vacuum/rebuild. Candidate verification against current authorized base state can prevent stale returns. Physical removal must include replicas, snapshots, caches, backups, and derived training sets under retention policy.

Deletion-heavy indexes may lose graph connectivity, accumulate tombstones, or waste list scans. Observe dead fraction and rebuild thresholds, but do not rebuild by exposing deleted items in a new generation.

**Version index generations.** An index generation binds vector model/preprocessing, metric, dimension, training/codebooks, algorithm parameters, source frontier, format, and build software. Build new generations immutably where practical, validate them, then atomically switch routing. Keep rollback while base changes can be replayed into both or recovered.

Never compare scores across incompatible embedding generations as if they shared geometry. During migration, query each generation with its corresponding query model and fuse calibrated ranks, or migrate all vectors before one-generation cutover.

**Plan distributed top-k.** Shards search local eligible vectors and a coordinator merges candidates. For exact search with comparable global scores, each shard's local top $k$ is sufficient to form global top $k$ because any omitted local item has at least $k$ local items no worse. Approximate search, filters, score calibration, replicas, and early termination complicate that statement.

Shard-local ANN may need overfetch. Report fan-out and partial failures. Returning results from 7 of 8 shards is not the same query unless the API marks partiality. Replicas must deduplicate stable vector IDs and agree on visible generation.

Partition by tenant, hash, coarse vector region, or hybrid. Tenant partitioning isolates policy but skews size; hashing balances identities but fans every query; vector partitioning prunes queries but shifts with model/data drift and can hotspot dense regions. Measure recall across shard boundaries.

**Account for memory and build.** Full vectors cost roughly $Ndb$ bytes for $b$ bytes per scalar, before IDs, metadata, graph edges, lists, codebooks, allocator overhead, replicas, and build workspace. One billion 768-dimensional float32 vectors alone require about $1{,}000{,}000{,}000\times768\times4=3.072$ TB decimal.

HNSW edges and construction can add substantial memory. PQ reduces vector bytes but needs training and may keep originals for reranking. Capacity includes simultaneous old/new generations, recovery replicas, page/cache working set, compaction/vacuum, and free headroom.

**Measure latency under offered load.** Query breadth parameters, top-k, filter selectivity, batch size, cache, CPU vector instructions, GPU transfer, storage, concurrency, and updates affect latency. Report p50, p95, p99, p99.9, timeout/cancel, queue time, throughput, and recall together.

Closed-loop clients can hide overload through coordinated omission. Use a stated load model, warm and cold runs, query classes, and steady state. Quality may degrade under adaptive time budgets; capture actual search effort and recall by latency bin.

**Build valid ground truth.** Freeze dataset/version, query set, eligibility filters, distance and precision, exact computation method, tie policy, and top-k. Verify exact calculations independently on a sample. Keep training/tuning queries separate from held-out evaluation.

Stratify by tenant, language, norm, density, filter selectivity, freshness, protected group, and hard/rare queries. Aggregate mean can hide catastrophic recall for one slice. ANN-Benchmarks provides comparative infrastructure, but production conclusions require production-shaped vectors and operations.

**Evaluate relevance and safety.** Human judgments need instructions, assessor agreement, sampling, and privacy. Offline relevance can fail online from presentation, feedback loops, or changing inventory. A/B tests need guardrails and causal design; click-through is not universal quality.

Embeddings can encode bias, copyrighted/sensitive content, secrets, and membership signals. Test adversarial queries, poisoning, prompt or content injection in retrieved documents, nearest-neighbor privacy, and abuse. Vector similarity is a candidate signal, not authorization or factual verification.

**Recover the whole pipeline.** Backup base records, vector/model generation, index generation or deterministic rebuild inputs, parameters/codebooks, metadata/authorization state, tombstones, routing, and replay coordinates. If rebuilding is chosen, estimate duration/capacity and preserve exact model artifacts.

Restore in isolation. Verify vector counts and dimensions, keyed hashes/sample values, model lineage, exact-search samples, ANN recall curves, filters/authorization, deletion, shard merge, update replay, and application relevance canaries. Matching index file count proves little.

**Observe causal metrics.** Record accepted/rejected embeddings, dimensions/norm/non-finite values, model/source lag, active/dead vectors, index generations, build/rebuild progress, memory/disk, graph/list/cluster statistics, query parameters, eligible/candidate/returned counts, filter selectivity, recall probes, score/norm distributions, shard fan-out, queues, latency, updates, deletes, and reconciliation mismatches.

Avoid logging raw vectors, queries, document text, or tenant identifiers without policy. Use sampled secured traces and bounded labels. Monitor quality with a stable canary set while avoiding overfitting operations to it.

The executable fixture below performs exact cosine ranking over three finite nonzero two-dimensional vectors after eligibility filtering. It is not ANN, an embedding model, a numerical-stability benchmark, an index, a transaction test, or a relevance evaluation.

<!-- bijux-verify: {"id":"finite-exact-vector-search","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"eligible=2\nranked_ids=a,b\ntop_score=1.000000\nsecond_score=0.707107\nforbidden_excluded=true\ndeterministic_ties=true\nevidence=finite_exact_vector_search\n","stderr":""}} -->
```python
items = [
    ("a", [1.0, 0.0], True),
    ("b", [1.0, 1.0], True),
    ("c", [0.0, 1.0], False),
]
query = [1.0, 0.0]

def cosine(left, right):
    dot = sum(x * y for x, y in zip(left, right))
    left_norm = sum(x * x for x in left) ** 0.5
    right_norm = sum(y * y for y in right) ** 0.5
    return dot / (left_norm * right_norm)

scored = [(cosine(query, vector), item_id) for item_id, vector, allowed in items if allowed]
ranked = sorted(scored, key=lambda pair: (-pair[0], pair[1]))
print(f"eligible={len(scored)}")
print(f"ranked_ids={','.join(item_id for _, item_id in ranked)}")
print(f"top_score={ranked[0][0]:.6f}")
print(f"second_score={ranked[1][0]:.6f}")
print(f"forbidden_excluded={str(all(item_id != 'c' for _, item_id in ranked)).lower()}")
print(f"deterministic_ties={str(ranked == sorted(ranked, key=lambda pair: (-pair[0], pair[1]))).lower()}")
print("evidence=finite_exact_vector_search")
```

## Definitions and Notation

- $x_i\in\mathbb{R}^d$ is stored vector for stable identity $id_i$; $y$ is a query vector; $d$ is dimension.
- $a_i$ is structured metadata, $F(a_i)$ an eligibility predicate, $q_i$ visibility/source version, and $m_i$ model/preprocessing contract.
- $\|x\|_2$ is Euclidean norm; $D_2(x,y)$ is Euclidean distance; $x\cdot y$ is inner product; cosine is normalized inner product for nonzero vectors.
- **Exact top-k** returns the true best $k$ eligible visible identities under metric and tie semantics.
- $T_k(y)$ is exact top-k set and $A_k(y)$ an approximate returned set under a simple recall definition.
- **ANN** intentionally permits missed/reordered true neighbors for resource benefits.
- **HNSW** is a layered navigable proximity graph; **IVF** partitions by learned coarse regions; **PQ** quantizes vector subvectors.
- A **candidate** is an item considered by later scoring/filtering; a **reranker** applies a more expensive ranking to candidates.
- **Pre-filter**, **integrated filter**, and **post-filter** differ by when eligibility constrains candidate search.
- A **generation** binds model, vectors, index/training parameters, source frontier, and format.
- **Recall@k** measures overlap with governed exact neighbors; **task relevance** measures usefulness/correctness for an application.
- **Overfetch** requests more local/candidate results than final $k$ to compensate for approximation, filtering, or distribution.
- **Drift** is change in vector/query distribution or meaning relative to build/training evidence.

## Mechanisms, Invariants, or Proof Structure

**Unit-vector equivalence.** For unit $u,v$, expanding squared Euclidean gives $\|u-v\|^2=\|u\|^2+\|v\|^2-2u\cdot v=2-2u\cdot v$. Since cosine equals dot product for unit vectors, smaller squared distance exactly corresponds to larger cosine. The result fails without nonzero normalization.

**Exact filtered top-k.** Let eligible visible set be $S_F$. Score every member under one compatible metric and stable tie order, then select first $k$. Any implementation omitting a member without a safe bound cannot claim exactness. Authorization/filtering must define $S_F$ before the answer, even if execution interleaves filtering and search.

**Recall calculation.** Under unique exact top-k and equal result budget, recall@k is intersection size divided by $k$. Missing returned items lower recall. Ties require an equivalence-aware ground-truth definition; otherwise arbitrary exact tie ordering can mark an equally valid ANN result wrong.

**Shard top-k argument.** In exact comparable scoring, an item outside a shard's local top $k$ has at least $k$ items in that shard no worse, so it cannot enter the global top $k$. Therefore merging local top $k$ from every complete shard suffices. Approximation, partial shards, inconsistent visibility, and incomparable scores invalidate premises.

**Post-filter risk.** Under an intentionally unrealistic independent candidate model with eligible fraction $p$, expected eligible among $n$ is $np$. This does not guarantee even one result, and ANN neighborhoods correlate with metadata. Correct filtered top-k requires eligibility-aware search or exhaustive fallback, not expected-count arithmetic.

**Generation switch invariant.** Build generation $g+1$ from a declared source frontier, replay later source mutations idempotently, validate quality/filter/deletion, then atomically route queries with matching query model to $g+1$. Fence $g$ updates or retain recoverable dual application until rollback ends. Mixed model spaces cannot share raw scores without calibration.

**Deletion invariant.** Once deletion is committed at version $q$, no query at or after $q$ may return the identity, regardless of stale ANN bytes, cache, replica, or reranker. Candidate verification or transactional index visibility enforces logical deletion while physical reclamation follows retention policy.

## Alternatives and Trade-Offs

**Exact scan versus ANN.** Exact scan gives ground truth and handles selective filters/batches well but costs $O(Nd)$. ANN reduces candidate work at quality, memory, build, and lifecycle cost. Keep an exact fallback/oracle for small scopes and evaluation.

**HNSW versus IVF.** HNSW often offers strong recall/latency with substantial memory and graph maintenance. IVF offers controllable probes and compact structures but needs representative training and balanced regions. Workload and update pattern decide.

**Full precision versus quantization.** Full vectors preserve stored-space distances and enable exact reranking at high bytes. PQ or scalar quantization saves memory/bandwidth with approximation error. Retaining originals elsewhere supports audit/rebuild at extra cost.

**Local versus external index.** An in-database index can share transactions, filters, backup, and SQL, depending on implementation. An external service can specialize and scale independently but needs change/reconciliation and cross-system authorization consistency.

**Pre-filter versus post-filter.** Pre/integrated filtering protects eligibility completeness but can reduce navigability or require per-filter structures. Post-filtering is simple but incomplete under selective predicates. Adaptive fallback can choose exact search for small eligible sets.

**Single versus dual model migration.** Stop-and-rebuild simplifies semantics but delays rollout. Dual generations allow online evaluation and rollback but double storage/build/update and require separate query embeddings and rank fusion.

**Vector versus lexical retrieval.** Vectors capture learned similarity; lexical finds exact rare tokens and supports explainable term matching. Hybrid often improves coverage but adds calibration and two failure surfaces.

**Central versus sharded search.** Central indexes avoid merge and cross-shard recall issues but limit scale/fault domains. Sharding scales while adding fan-out, skew, overfetch, replica consistency, and partial-result semantics.

## Failure Modes and Misconceptions

- **“Nearest means relevant.”** Distance reflects one model space, not domain truth.
- **“Cosine and dot product are equivalent.”** Only with appropriate nonzero normalization.
- **“ANN recall is model quality.”** It measures approximation against stored-vector ground truth.
- **“A high average recall is sufficient.”** Tails, protected slices, filters, and hard queries can fail.
- **“Post-filtering preserves top-k.”** It can omit eligible neighbors never retrieved.
- **“More overfetch guarantees correctness.”** Only exhaustive eligible evaluation or safe bounds do.
- **“An index parameter has universal meaning.”** Implementations and data distributions differ.
- **“Index build is a one-time cost.”** model drift, deletes, corruption, and upgrades require rebuilds.
- **“Vector deletion removes sensitive data.”** replicas, caches, backups, source content, and training sets remain.
- **“Scores compare across models.”** coordinate systems and calibration change.
- **“Local top-k merge always works.”** Exact proof premises fail under ANN and partial shards.
- **“Static benchmarks predict production.”** updates, filters, churn, failure, and resource contention matter.
- **“Embedding dimensions are independent features.”** learned coordinates generally lack standalone domain meaning.
- **“Similarity is authorization.”** A close vector can still be forbidden.
- **“An extension shares every database guarantee.”** verify exact index transaction, WAL, replication, and restore behavior.

## Worked Examples

### Example 1

**Situation.** Vectors A=(1,0), B=(10,1), query Q=(1,0). Compare inner product and cosine.

Inner products are 1 for A and 10 for B, so B ranks first. Cosine for A is 1; cosine for B is $10/\sqrt{101}\approx0.995$, so A ranks first. Magnitude changes inner-product ranking.

**Conclusion.** Distance choice is a semantic contract, not a harmless index option.

### Example 2

**Situation.** A zero vector enters a cosine index.

Its norm is zero, so cosine divides by zero and is undefined. Choosing score zero silently invents semantics and affects ties. Reject it, route through a defined missing-embedding policy, or use another metric with explicit meaning.

**Conclusion.** Validate finiteness, dimension, and norm before indexing.

### Example 3

**Situation.** Exact top-10 and ANN top-10 overlap in 8 identities.

Under unique no-tie set semantics, recall@10 is $8/10=0.8$. This says nothing about whether either list is relevant to a person, and mean recall across queries can hide a zero-recall slice.

**Conclusion.** Recall needs a ground-truth and aggregation contract and remains separate from relevance.

### Example 4

**Situation.** Only 1% of items satisfy tenant and date filters; the service retrieves ANN top 100 globally and post-filters.

The simplistic independent expectation is one eligible result, far short of requested 10, and correlation may make it zero. Search within an eligible structure, overfetch adaptively with no completeness claim, or exact-scan the bounded eligible set. Authorization filters must still apply before return.

**Conclusion.** Selective filters change candidate-generation design.

### Example 5

**Situation.** One billion 768-dimensional float32 vectors are proposed in memory.

Raw scalar bytes are $10^9\times768\times4=3.072$ TB decimal. IDs, graph edges/lists, metadata, allocator overhead, replicas, build workspace, and old/new generations add substantially. PQ can reduce vector bytes but adds codebooks/error and perhaps original-vector storage.

**Conclusion.** Capacity begins with raw vectors and ends with complete index lifecycle.

### Example 6

**Situation.** A base document becomes private at version 52, but an external index still marks it public at version 51.

If search trusts index metadata, it leaks. Verify candidates against current authoritative authorization or make visibility updates atomic/fail-closed. Track source version and repair lag. Cache keys must include tenant/policy context and invalidate on restriction.

**Conclusion.** Eligibility consistency is a security invariant, not a relevance tweak.

### Example 7

**Situation.** A new embedding model is deployed only for query vectors while stored vectors remain old-model.

Coordinates are from incompatible spaces, so scores are meaningless even if dimension matches. Query old index with old query model while building the new generation; validate and cut over together, or query both with their matching model and fuse ranks under evidence.

**Conclusion.** Dimension equality does not imply embedding compatibility.

### Example 8

**Situation.** Four exact shards each return local top 5 for global top 5.

With complete shards, identical score semantics, and consistent visibility, merging 20 candidates is exact: anything omitted has five same-shard items no worse. If one shard uses quantized approximate scores or times out, the proof fails; mark partial or retry under policy.

**Conclusion.** Distributed top-k correctness depends on comparability, exactness, and completeness premises.

### Example 9

**Situation.** HNSW latency improved after lowering search breadth, but average recall fell from .97 to .94.

The decision needs per-query/slice recall, p99 latency, throughput/queue, memory, filters, update load, and application impact. If rare-language recall fell to .40, the mean conceals harm. Plot the Pareto curve and retain a rollback generation.

**Conclusion.** Tune quality and resources jointly, stratified by risk.

### Example 10

**Situation.** A restored index has expected vector count but recall canary collapses.

Possible causes include wrong model/preprocessing, metric, normalization, codebooks, graph/list files, parameters, source frontier, or corrupt vectors. Verify keyed vector samples/hashes and exact scores first, then index generation and recall/filter/deletion behavior before serving.

**Conclusion.** Count equivalence does not prove geometric or operational restore equivalence.

## Cross-Program Connections

[Algorithms Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies nearest-neighbor search, graphs, clustering, quantization, approximation, selection, and evaluation complexity. Database engineering adds mutation, transaction, recovery, distribution, and policy.

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) connects heaps, inverted files, proximity graphs, compression, and cache-aware layout. ANN structures are data-dependent indexes with lifecycle costs.

[Machine-learning concerns in Data Engineering](../../19-data-engineering/ROADMAP.md) connect model artifacts, feature/preprocessing lineage, drift, replay, and evaluation datasets. Embeddings are derived data, not opaque source truth.

[Search and API concerns](../../28-api-and-service-engineering/ROADMAP.md) connect pagination, filters, authorization, ranking explanations, budgets, cancellation, and partial results. A similarity endpoint must expose stable semantics.

[Security Engineering](../../25-security-engineering/ROADMAP.md) connects cross-tenant isolation, inference, poisoning, sensitive content, deletion, and retrieved-content injection. Approximation cannot weaken policy.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects offered load, tail latency, memory/disk capacity, failure, observability, and rollback. Recall is one axis in a production evidence matrix.

## References

- Jeff Johnson, Matthijs Douze, and Hervé Jégou, [Billion-scale similarity search with GPUs](https://arxiv.org/abs/1702.08734), arXiv 2017. Primary source for Faiss-oriented exact/approximate vector search and GPU implementation.
- Yu. A. Malkov and D. A. Yashunin, [Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs](https://arxiv.org/abs/1603.09320), *IEEE TPAMI* 42(4), 2020; preprint retrieved 2026-09-05. HNSW mechanism and evaluation.
- Subramanya et al., [DiskANN: Fast Accurate Billion-point Nearest Neighbor Search on a Single Node](https://papers.nips.cc/paper_files/paper/2019/hash/09853c7fb1d3f8ee67a61b6bf4a7f8e6-Abstract.html), NeurIPS 2019. Primary source for storage-oriented graph ANN.
- Ruiqi Guo et al., [Accelerating Large-Scale Inference with Anisotropic Vector Quantization](https://proceedings.mlr.press/v119/guo20h.html), ICML 2020. Primary ScaNN/quantization source.
- pgvector, [pgvector](https://github.com/pgvector/pgvector), current repository documentation checked 2026-09-05. Concrete exact, HNSW, IVFFlat, distance, filtering, and PostgreSQL integration behavior.
- PostgreSQL Global Development Group, [Indexes](https://www.postgresql.org/docs/current/indexes.html), current documentation checked 2026-09-05. General planner, index, concurrency, partial, expression, and index-only foundations for in-database vector extensions.
- Qdrant, [Filtering](https://qdrant.tech/documentation/concepts/filtering/), current documentation checked 2026-09-05. Concrete payload-filter and condition behavior in a vector engine.
- OpenSearch, [Vector search](https://docs.opensearch.org/latest/vector-search/), current documentation checked 2026-09-05. Concrete approximate/exact, engine, filtering, and vector workload features.
- ANN-Benchmarks, [ANN-Benchmarks](https://ann-benchmarks.com/), current project site checked 2026-09-05. Reproducible comparative ANN benchmarking framework and datasets.
- Pinecone, [Indexing overview](https://docs.pinecone.io/guides/index-data/indexing-overview), current documentation checked 2026-09-05. Concrete vector identity, metadata, namespace, upsert, and deletion considerations in a managed vector service.

## Exercises

### Exercise 1

Define embedding contract, exact top-k, ANN, cosine similarity, HNSW, IVF, PQ, recall@k, eligibility filter, and index generation. Explain why one recall value is insufficient.

### Exercise 2

For A=(3,0), B=(2,2), and query Q=(1,0), compute dot product, cosine, and squared Euclidean rankings. Then normalize A and B and verify the unit-vector equivalence.

### Exercise 3

A vector service returns stale deleted items during a rolling rebuild. Base rows are authoritative, indexing is asynchronous, and caches retain results for ten minutes. Diagnose every visibility gap and design a no-resurrection generation switch.

### Exercise 4

Design filtered hybrid search for a multi-tenant legal corpus with exact citation IDs, semantic passages, jurisdiction/date filters, immediate revocation, and explainable ranked results. State index, transaction, authorization, and evaluation choices.

### Exercise 5

One billion vectors must migrate from a 768-dimensional model to a 1,024-dimensional model with no search outage, limited to 5 TB temporary storage, ongoing updates, shard failures, and a rollback requirement. Produce a capacity-aware migration and validation protocol.

## Answers to the Exercises

### Answer 1

An **embedding contract** binds model, preprocessing, dimension, scalar type, normalization, and metric. **Exact top-k** returns true best eligible visible identities; **ANN** permits misses for resources. **Cosine** is normalized dot product for nonzero vectors. **HNSW** is a layered proximity graph; **IVF** probes learned coarse lists; **PQ** stores quantized subvector codes. **Recall@k** is overlap with governed exact neighbors. An **eligibility filter** defines which items may participate; a **generation** binds model, index settings, source frontier, and format. One recall mean omits latency, resource, update/filter conditions, ties, query slices, tails, relevance, and failure.

### Answer 2

Dot products with Q are A=3 and B=2, so A wins. Cosines are A=1 and B=$2/\sqrt8\approx0.7071$, so A wins. Squared Euclidean distances are A: $(3-1)^2=4$; B: $(2-1)^2+2^2=5$, so A wins. Normalize A to (1,0) and B to $(1/\sqrt2,1/\sqrt2)$. Squared distances to unit Q are 0 and $2-2/\sqrt2\approx0.5858$; cosines are 1 and $1/\sqrt2$. The orders correspond by $D^2=2-2\cos$. The initial agreement was contingent; arbitrary magnitudes can produce different rankings as Example 1 showed.

### Answer 3

Gaps include base delete before index tombstone, old index generation serving during rebuild, replay missing/ordering, replicas on different generations, result cache retaining IDs, reranker/document cache retaining content, and routing switching before validation. Commit deletion with stable source version and make query candidate verification consult current authoritative eligibility or a transactionally consistent tombstone service. Build the new generation from snapshot/frontier, replay later mutations idempotently including deletes, reconcile every active ID/version, and test deletion canaries. Switch routing atomically by generation with replicas ready; invalidate/version caches by policy and generation; fence old writes; retain rollback only if it also receives deletes. Physical cleanup follows separately, but no post-delete query may return the ID.

### Answer 4

Use tenant/policy-isolated namespaces or indexes, stable document/chunk IDs, and versioned model/chunk lineage. Lexical search owns exact citation and rare-term candidates; vector search owns semantic passage candidates; structured pre/integrated filters enforce tenant, jurisdiction, date, and current access. Verify every candidate against authoritative revocation/version before return and key caches by tenant/policy/generation. Fuse ranks with documented normalization or reciprocal-rank method, then expose source channel, exact citation, passage, score class, model/index generation, and freshness—not a truth probability. Update base and tombstones transactionally where possible; otherwise replay durable versioned changes and reconcile. Evaluation includes exact ANN recall under filters, legal relevance judgments, citation accuracy, revocation tests, protected slices, p99/cost, and shard/partial failures.

### Answer 5

First account for raw old vectors: 3.072 TB decimal; new float32 vectors alone are 4.096 TB, so simultaneous raw copies exceed 5 TB before indexes. The stated temporary limit makes naive dual full-precision generations impossible. Choose evidence-backed quantization/disk layout, staged shard replacement, or additional capacity; do not begin until old plus bounded in-flight new shard, index/build workspace, WAL, replicas, and reserve fit. Build new vectors shard-by-shard from a fixed base frontier with the exact new model, replay ongoing mutations/deletes into both generations, validate keyed samples and exact scores, ANN/filter recall, relevance, authorization, capacity, and recovery. Query old with old query embeddings and canary new with new embeddings; never cross-score. Switch only ready replicas via generation routing, retain rollback shards receiving all changes, and reclaim old shards progressively after the rollback window. A shard failure retries from checkpoint or replica without mixed authority; partial results are explicit. If no design fits 5 TB safely, extra capacity is the honest blocker.
