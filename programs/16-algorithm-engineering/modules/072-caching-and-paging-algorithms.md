---
module_id: ALGE-072
program: Algorithm Engineering
level: 2
module_number: 72
title: Caching and Paging Algorithms
status: complete
last_verified: 2026-09-05
---

# Caching and Paging Algorithms

## One-Page Review

### Governing question

When fast storage cannot hold the working set and future requests are unknown, which objects should be retained or evicted, what can be guaranteed, and which real-system costs invalidate the unit-page model?

### Essential definitions

- A **request sequence** $\sigma=(p_1,\ldots,p_T)$ names pages or objects over time.
- A cache of **capacity** $k$ stores at most $k$ distinct unit pages.
- A **hit** finds the requested page resident; a **fault** or **miss** fetches a nonresident page and, when full, requires eviction.
- **LRU** evicts the resident page whose most recent request is earliest.
- **FIFO** evicts the resident page inserted earliest, independent of later hits.
- **MIN** or **Belady's offline rule** evicts the resident page whose next request lies farthest in the future, or never occurs.
- A **stack algorithm** has nested resident sets: for one trace, the cache at capacity $k$ is contained in that at capacity $k+1$.
- A **reuse distance** is the number of distinct pages requested since the previous request to the same page; a cold reference has infinite distance.
- A **phase** for cache size $k$ is a maximal contiguous subsequence containing requests to at most $k$ distinct pages.
- A **dirty** page has been modified and may require writeback on eviction.
- **Admission** decides whether a fetched object should enter the cache; **eviction** chooses a resident victim.
- **inclusive**, **exclusive**, and **non-inclusive** policies describe relationships among cache levels.

### Central model, mechanism, or theorem

In unit-cost paging with equal cache capacity $k$, LRU is $k$-competitive up to an additive initial-state constant. Partition the sequence into $k$-phases. LRU faults at most $k$ times per phase because it does not evict a page already requested in the current phase while fewer than $k$ distinct current-phase pages have appeared. Except for the first phase, each new phase plus the final request of the preceding phase contains $k+1$ distinct pages, so any cache of size $k$, including offline optimum, faults at least once across that boundary. Hence

$$
LRU(\sigma)\le k\,OPT(\sigma)+k.
$$

The factor is a worst-case guarantee for the declared page model. It is not a claim that production miss rates differ by factor $k$.

MIN is offline optimal for unit-cost paging. An exchange argument replaces an optimal policy's victim with the page whose next use is farthest away; this change causes no earlier fault and can be repeated to obtain MIN.

### Critical invariants

- Resident-page count never exceeds capacity, and a requested page is resident after service.
- A hit performs no fetch; a fault count increments exactly once per missing unit-page request.
- LRU order changes on every hit and insertion; FIFO order changes only on insertion and eviction.
- MIN uses only future positions in analysis or an oracle baseline, never in a deployed online policy.
- Online and offline comparisons share trace, capacity, initial state, request semantics, and cost model.
- Dirty writeback, variable size, latency, admission, prefetch, invalidation, and coordination costs are explicit when present.
- Cache keys include every semantic dimension needed to prevent false hits and isolation failures.
- Expiration, invalidation, and consistency policy can evict or reject entries independently of replacement ranking.
- Telemetry distinguishes requests, hits, misses, fills, evictions, writebacks, bypasses, stale rejections, and failures.
- Policy changes are shadowed or rolled out with bounded memory, latency, correctness gates, and rollback.

### Common failures

Common failures include using MIN in production by leaking the future; confusing FIFO with LRU; assuming larger caches always help FIFO; computing hit rate without cold misses; comparing capacities or traces that differ; treating a miss as unit cost when objects or backends differ; caching every fetched object; allowing a scan to evict a hot working set; omitting dirty-write costs; admitting stale or cross-tenant data under an incomplete key; double-counting coalesced misses; interpreting replay as causal when policy changes requests; and optimizing global hit rate while tail latency or fairness degrades.

### Compact example

With capacity 3 and requests $1,2,3,1,4$, LRU faults on 1, 2, and 3; the second 1 is a hit and becomes most recent; request 4 faults and evicts 2, the least recently used. The final recency order from least to most recent is $(3,1,4)$.

### Connections

[ALGE-071](./071-online-decisions-and-competitive-analysis.md) supplies the competitive model. [ALGE-073](../ROADMAP.md#block-08--online-streaming-and-dynamic-algorithms) treats job arrivals, while Operating Systems owns virtual-memory mechanisms and Computer Architecture owns hardware-cache coherence and microarchitecture.

## Governing Question

How do we move from the classical unit-page replacement problem to a correct and measurable caching service whose admission, eviction, freshness, consistency, and cost policies match the workload?

Paging isolates a hard online choice: after a miss in a full cache, evict one resident page without knowing the future. The abstraction supports clean optimality and competitive proofs. Real caches add object sizes, unequal fetch latency, writes, expiration, replication, hierarchy, prefetching, tenant isolation, and concurrency. These do not merely tune the classical algorithm; they can change the optimization problem.

The disciplined path is to begin with a precise model, prove or test the mechanism there, then record each production extension and the evidence it needs. A replacement policy cannot repair an invalid key, stale data, or an unsafe coherence protocol.

## Why This Matters

Caches trade scarce fast capacity for lower latency, bandwidth, energy, and backend load. They occur in processors, operating systems, databases, content delivery, storage, services, and applications. Under load, a small miss-rate shift can multiply backend traffic and create a feedback loop: more misses increase latency, longer requests occupy resources, and contention causes more timeouts.

Yet hit rate alone is a weak objective. Hitting a cheap object and missing an expensive one can be worse than the reverse. A large object may displace many small hot entries. Dirty eviction adds writeback. A stale hit can be a correctness defect. Shared-cache efficiency can conceal tenant starvation. Prefetch can improve apparent hits while consuming bandwidth and evicting demanded data.

Algorithm engineering therefore connects proof, trace behavior, data semantics, and system constraints. It treats the cache as a stateful service with explicit authority and failure modes.

## Prerequisites and Retrieval

Retrieve [ALGE-071](./071-online-decisions-and-competitive-analysis.md), amortized and competitive analysis, ordered maps, hashing, priority structures, probability, and experimental design. Familiarity with memory hierarchy, virtual memory, storage, and distributed consistency helps distinguish the abstract policy from system mechanisms.

This chapter owns replacement and admission reasoning, MIN optimality, LRU competitiveness, stack behavior, trace evaluation, and production extensions. Operating Systems owns page tables, faults, and kernel reclaim in depth; Computer Architecture owns physical cache organization and coherence; Distributed Systems owns cache-consistency protocols.

## Learning Objectives

After completing this module, you should be able to:

1. specify the classical paging model and its information boundary;
2. trace LRU, FIFO, and MIN exactly;
3. explain MIN's exchange argument and LRU's phase proof;
4. distinguish stack policies from policies that may exhibit Belady's anomaly;
5. derive hit behavior from reuse distance;
6. separate admission, eviction, expiration, invalidation, and prefetch;
7. extend the cost model for size, latency, writes, and hierarchy;
8. build leakage-free trace and shadow evaluations;
9. identify concurrency, keying, isolation, and observability failures; and
10. select a cache policy using objective, workload, guarantee, and operational risk.

## Core Exposition

### Fix the classical paging model

Let the universe contain page identifiers and let cache $C_t$ hold at most $k$ pages after request $t$. A request to $p_t\in C_{t-1}$ is a hit. Otherwise it is a fault: fetch $p_t$, evict one resident page if the cache is full, and set $p_t\in C_t$. Every fault costs one; hits cost zero; pages have equal size; requests are read-only; fetches complete before the next request; and capacity is fixed.

Those assumptions create the theorem. Initial cache contents affect an additive term. If bypass is allowed, admission becomes a choice. If fetching overlaps, latency is no longer the fault count. If objects have different sizes or retrieval costs, a unit-page ratio does not transfer automatically.

Tie semantics matter. LRU timestamps can tie under coarse clocks, so use a total logical order. Concurrent requests must be linearized for the abstract trace or analyzed under another model. A capacity change creates a different problem and must specify which pages are immediately removed.

### Trace LRU and FIFO as state machines

LRU maintains pages from least to most recently used. A hit moves its page to the most-recent end. A miss evicts the least-recent page when full, then inserts the request as most recent. An ordered dictionary implements expected constant-time membership and order updates under ordinary hashing assumptions.

FIFO maintains insertion order. A hit does not change it. FIFO is simple but lacks the stack property and can exhibit Belady's anomaly: increasing capacity can increase faults on some sequences. LRU is a stack algorithm under consistent tie semantics, so its fault count cannot rise as capacity grows on a fixed trace.

Frequency-based policies retain repeatedly requested objects but adapt slowly after workload change and require aging. CLOCK approximates recency with reference bits and a circular hand, reducing metadata and synchronization pressure. A policy name still leaves admission, dirty handling, tie-breaking, and concurrency unspecified.

### Use MIN as an offline comparator

On a miss with a full cache, MIN evicts the resident page whose next request occurs farthest in the future, treating no future request as infinity. It is not causal. It provides an optimal unit-page baseline for a fixed complete trace.

For the exchange argument, compare MIN with an optimal policy $O$ at the first point they evict different pages. MIN evicts $q$, whose next use is no earlier than $O$'s victim $r$. Modify $O$ to evict $q$ instead and retain $r$. Until $r$ is requested, the modified cache can mimic $O$ without an extra fault because $q$ is not requested earlier. At that point, swap identities or align states. The modified policy is no worse and agrees with MIN for one more decision. Repeating yields MIN.

The proof assumes unit sizes, unit fault costs, one cache, and complete future knowledge for the comparator. A production policy cannot compute MIN from a trace prefix. Using timestamps recorded after the eviction point as online features is future leakage.

### Execute and verify a reference trace

<!-- bijux-verify: {"id":"lru-and-min-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"lru_faults=7 opt_faults=5\n1:F:(1,)\n2:F:(1, 2)\n3:F:(1, 2, 3)\n1:H:(2, 3, 1)\n4:F:(3, 1, 4)\n1:H:(3, 4, 1)\n2:F:(4, 1, 2)\n3:F:(1, 2, 3)\n4:F:(2, 3, 4)\ninvalid_capacity=rejected\n","stderr":""}} -->
```python
from collections import OrderedDict


def lru_trace(requests, capacity):
    if capacity < 1:
        raise ValueError("capacity must be positive")
    cache = OrderedDict()
    faults, trace = 0, []
    for page in requests:
        hit = page in cache
        if hit:
            cache.move_to_end(page)
        else:
            faults += 1
            if len(cache) == capacity:
                cache.popitem(last=False)
            cache[page] = None
        trace.append((page, "H" if hit else "F", tuple(cache)))
    return faults, trace


def min_faults(requests, capacity):
    if capacity < 1:
        raise ValueError("capacity must be positive")
    cache, faults = set(), 0
    for index, page in enumerate(requests):
        if page in cache:
            continue
        faults += 1
        if len(cache) == capacity:
            def next_use(resident):
                try:
                    return requests.index(resident, index + 1)
                except ValueError:
                    return len(requests) + 1
            victim = max(cache, key=next_use)
            cache = cache - {victim}
        cache.add(page)
    return faults


requests = [1, 2, 3, 1, 4, 1, 2, 3, 4]
faults, trace = lru_trace(requests, 3)
print(f"lru_faults={faults} opt_faults={min_faults(requests, 3)}")
for page, outcome, state in trace:
    print(f"{page}:{outcome}:{state}")
try:
    lru_trace(requests, 0)
except ValueError:
    print("invalid_capacity=rejected")
```

The transcript verifies the stated trace on CPython. The simple MIN implementation is quadratic because it searches the suffix; preprocessing next positions can improve the oracle computation. Execution does not prove MIN optimal or LRU competitive; those are mathematical claims reviewed separately.

### Prove LRU's phase bound

Partition the trace greedily into maximal phases containing at most $k$ distinct pages. The next request begins a new phase precisely when it would introduce the $(k+1)$st distinct page.

Within one phase, once LRU has requested a page, that page is more recent than every resident page not yet requested in the phase. Before all $k$ phase pages have appeared, LRU evicts an old non-phase page when one exists. Therefore each distinct phase page causes at most one fault, and LRU incurs at most $k$ faults per phase.

For every phase after the first, take its first request and the preceding phase. Maximality provides $k+1$ distinct pages across the boundary. A cache of size $k$ cannot hold them all and must fault at least once in a suitable disjoint charging interval. Charging phases carefully gives one offline fault per completed boundary, while LRU pays at most $k$ per phase. Initial alignment contributes an additive term, yielding $LRU\le kOPT+k$ under a conventional empty-cache treatment.

This proof is robust to adversarial traces but coarse. On many workloads LRU is much closer to MIN. The bound also worsens with $k$, illustrating why competitive ratios and observed cache effectiveness answer different questions.

### Connect reuse distance to capacity

For a repeated request, count distinct pages since its previous occurrence. Under fully associative LRU, the request hits at capacity $k$ exactly when its reuse distance is less than $k$, subject to a consistent convention; cold references miss at every finite capacity. A reuse-distance histogram therefore derives the LRU miss-ratio curve for many capacities from one trace.

The stack property enables stack-distance algorithms and monotone capacity planning. FIFO lacks this nesting, so a single stack ordering cannot represent all capacities. Reuse distance describes reference locality, not object cost or semantic value. Sampling or approximate measurement must report error and treatment of cold accesses.

### Separate admission from eviction

Always admitting a miss lets one-time scans pollute the cache. An admission policy may bypass objects unlikely to repay insertion and displacement costs. It can use frequency sketches, reuse predictors, size, retrieval cost, or explicit directives. Evaluate predictor cost and false decisions.

Eviction ranks only admitted residents. Combining admission and eviction can outperform replacing the ranking alone because pollution and retention are different mechanisms. Compare ablations: existing eviction with new admission, new eviction with existing admission, and the full system under matched metadata and compute budgets.

Negative caching stores “not found” or failure results. It needs short, semantically sound expiration and invalidation because a stale negative can hide newly created data. Failed or unauthorized responses must not leak across principals through shared keys.

### Extend the objective deliberately

For variable object sizes $s_i$ and retrieval costs $w_i$, capacity is $\sum_{i\in C}s_i\le K$ and misses have unequal consequence. A value signal might combine reuse probability, latency saved, and size, but a heuristic score is not a theorem. Large objects can create fragmentation and long fill times.

Dirty pages add writeback cost and durability semantics. Evicting a clean cold page may be preferable to an older dirty page even when recency differs. Writeback can be asynchronous, but queue capacity, failure, ordering, and shutdown behavior must be modeled.

TTL expiration and explicit invalidation constrain eligibility. A replacement hit that returns stale data is not a valid hit. Consistency may demand version validation, leases, or coherence messages. Record stale rejections separately from ordinary misses.

### Engineer multilevel and shared caches

In inclusive hierarchies, a lower level contains copies of upper-level entries; lower eviction may invalidate upper copies. Exclusive hierarchies seek disjoint contents and require movement. Non-inclusive policies make no strict containment promise. The useful objective includes end-to-end latency and traffic across levels, not isolated hit rates.

Shared caches need tenant isolation and admission control. A high-volume tenant can evict another's working set. Partitioning gives predictability but can waste capacity; shared pools improve utilization but require quotas, weighted fairness, or protected segments. Keys must bind tenant, authorization context where relevant, representation, locale, model version, and other semantic dimensions.

Concurrent misses for the same key should often coalesce into one fill, but the waiters' deadlines and cancellation remain independent. Define whether coalesced requests count as misses, backend fetches, or both. Prevent a failed fill from poisoning the entry or causing an unbounded retry herd.

### Evaluate without fooling the cache

Preserve request order, key identity, object size, cost, writes, invalidations, and timestamps. Split traces by source and later time. Warm-cache and cold-cache experiments answer different questions; report warmup and initial state. Deduplicate retries only if production semantics do.

Use miss-ratio curves, byte hit rate, latency-weighted savings, backend requests, writebacks, memory, metadata CPU, tail latency, fairness, staleness, and failure. Compare with MIN only under the matching abstraction. When future requests depend on latency or recommendations, replay is not a causal experiment.

Shadow evaluation can compute alternative decisions without serving them. It must model counterfactual cache state independently; applying an alternative victim to the active cache contaminates both paths. Roll out with memory and backend guardrails, and retain immediate bypass or prior-policy fallback.

## Definitions and Notation

$\sigma=(p_1,\ldots,p_T)$ is a request sequence. $C_t^A(k)$ is algorithm $A$'s resident set after request $t$ at capacity $k$. $A(\sigma,k)$ is its fault count under the unit-page model. $OPT$ or MIN denotes the offline optimum. For a request at $t$, reuse distance $d_t$ counts distinct identifiers since its previous occurrence and is $\infty$ when none exists.

A $k$-phase is a maximal consecutive subsequence containing at most $k$ distinct pages. A stack algorithm satisfies $C_t^A(k)\subseteq C_t^A(k+1)$ for every $t$ and $k$ under coupled execution. In extended models, $s_i$ is object size, $w_i$ retrieval or miss cost, $K$ byte capacity, and dirty-state cost is separately charged.

**Replacement** chooses a victim, **admission** chooses whether to retain a fetched object, **expiration** rejects entries after policy time, **invalidation** removes entries after semantic change, and **prefetch** fetches before a demand miss. These mechanisms can interact but should not be conflated.

## Mechanisms, Invariants, or Proof Structure

### MIN exchange invariant

At the first disagreement with MIN, replace an optimal policy's nearer-future victim by MIN's farthest-future victim. The replacement policy retains every page the original needs until the nearer victim's request, so it incurs no earlier additional fault. State can then be aligned without greater cost. Repeating preserves optimality and increases the common decision prefix.

### LRU phase invariant

During a phase, a page already requested in that phase is newer than a resident not yet requested there. LRU therefore cannot fault twice on the same phase page before all phase-distinct pages have appeared. At most $k$ distinct pages implies at most $k$ faults.

### Stack invariant

Couple LRU caches of capacities $k$ and $k+1$ under one total recency order. Each contains the $k$ or $k+1$ most recent distinct pages, respectively, so the smaller set is contained in the larger. A larger LRU cache therefore cannot turn a smaller-cache hit into a miss.

### Service invariants

Every served hit passes key, version, authorization, and freshness checks. Capacity accounting includes value and metadata. Fills and evictions are failure-atomic. Dirty data has a durable owner. Each event has one request identity, while request miss, backend fetch, and waiter outcomes remain separate metrics.

## Alternatives and Trade-Offs

| Policy or mechanism | Strength | Risk | Useful setting |
|---|---|---|---|
| MIN | Offline-optimal unit-page baseline | Requires future; abstraction may mismatch | Trace lower bound and oracle comparison |
| LRU | Simple, stack property, $k$-competitive | Scan pollution; metadata synchronization | Temporal locality with manageable metadata |
| FIFO | Low update cost | Ignores hits; Belady anomaly | Constrained systems after trace validation |
| CLOCK | Approximate recency with compact state | Scan and hand behavior require tuning | OS and high-concurrency implementations |
| Frequency/admission | Resists one-time scans | Aging, sketch error, slower adaptation | Skewed object workloads |
| Cost/size-aware | Targets bytes or latency saved | Score instability; variable-size complexity | Web, storage, and service caches |
| Partitioned cache | Isolation and predictable quotas | Stranded capacity | Multi-tenant fairness and safety |
| Shared cache | Better aggregate utilization | Interference and information leakage | Trusted tenants with governed fairness |

No universal policy dominates because workloads and objectives differ. Prefer the simplest policy whose assumptions, metadata cost, and evidence satisfy the service contract.

## Failure Modes and Misconceptions

- **“LRU is offline optimal.”** MIN is offline optimal in the unit-page model; LRU is causal and competitive.
- **“A hit always helps.”** A stale, unauthorized, or incorrect-key hit is a defect.
- **“More capacity means fewer FIFO faults.”** FIFO can exhibit Belady's anomaly; LRU's stack property prevents it.
- **“Hit rate equals latency saved.”** Miss costs and object sizes vary, and hits still consume time.
- **“Eviction is the whole policy.”** Admission, expiration, invalidation, and prefetch shape contents.
- **“Future trace fields are harmless features.”** They turn an online policy into an oracle and leak evaluation outcomes.
- **“MIN is a fair baseline for any cache.”** Only when sizes, costs, capacity, and service semantics match its model.
- **“Warmup is preprocessing.”** Initial contents materially change results and must be reported.
- **“A shared cache is automatically efficient.”** Aggregate gains can conceal tenant interference or data leakage.
- **“Coalescing converts all waiters to hits.”** It saves backend fetches but waiters still experience a miss path.
- **“Replay proves rollout impact.”** Served policy can alter timing and future demand.
- **“Replacement can compensate for invalidation bugs.”** Correctness policy has authority over optimization.

## Worked Examples

### Example 1

**Situation.** Capacity is 3 and requests are $1,2,3,1,4$.

**Reasoning.** LRU faults on the first three requests, hits 1 and moves it newest, then faults on 4 and evicts 2. Least-to-most recent state becomes $(3,1,4)$.

**Conclusion.** Hits update LRU order even though they do not fetch.

### Example 2

**Situation.** FIFO sees the same prefix.

**Reasoning.** It inserts 1, 2, 3; the hit on 1 does not change insertion order. On request 4, it evicts 1, the oldest insertion, unlike LRU's eviction of 2.

**Conclusion.** FIFO and LRU diverge specifically because FIFO ignores hit recency.

### Example 3

**Situation.** On requests $1,2,3,1,4,1,2,3,4$ with capacity 3, LRU has 7 faults and MIN has 5.

**Reasoning.** MIN uses future positions to keep pages needed sooner. The executable trace verifies counts. The empirical ratio $7/5=1.4$ describes this trace only; LRU's theorem allows a larger worst case.

**Conclusion.** Oracle trace quality and competitive guarantee are different evidence.

### Example 4

**Situation.** A request for page $x$ has reuse distance 4.

**Reasoning.** Four distinct other pages have become more recent. Fully associative LRU misses at capacity 4 because $x$ has fallen below the top four, but hits at capacity 5, subject to the stated distance convention.

**Conclusion.** Reuse distance maps a trace to LRU behavior across capacities.

### Example 5

**Situation.** A one-pass scan of 10,000 unique objects follows repeated access to 100 hot objects in a capacity-100 LRU cache.

**Reasoning.** Always-admit LRU replaces the entire hot set during the scan, causing another 100 misses when hot traffic returns. A scan-resistant admission rule could bypass low-evidence objects, but must be tested against workloads where scan objects later become hot.

**Conclusion.** Admission addresses pollution that recency ranking alone cannot prevent.

### Example 6

**Situation.** Object A is 100 MB and saves 10 ms per likely hit; 100 one-MB objects each save 2 ms.

**Reasoning.** Unit-object hit rate treats A and each small object equally. Capacity and latency value do not. Retaining the small set can save up to 200 ms over one hit each versus 10 ms for A, though reuse probabilities and metadata must be included.

**Conclusion.** Variable size and miss cost require a different objective from unit-page faults.

### Example 7

**Situation.** LRU's oldest page is dirty and costs 50 ms to write; the next-oldest clean page costs 1 ms to refetch.

**Reasoning.** Pure recency chooses the dirty page, but the real objective may favor the clean victim. Deferring writeback consumes dirty-memory budget and needs failure semantics. Both online and comparator costs must include writes.

**Conclusion.** Dirty state changes victim cost and durability obligations.

### Example 8

**Situation.** A response is cached by URL but omits tenant and authorization scope from the key.

**Reasoning.** A request from another tenant can become a false “hit” and disclose data. Replacement quality is irrelevant. Bind the semantic and security context, reject unauthorized entries, and test isolation before measuring hit rate.

**Conclusion.** Cache correctness and isolation precede optimization.

### Example 9

**Situation.** One hundred concurrent requests miss the same key and trigger one coalesced backend fetch.

**Reasoning.** There are 100 request-level miss experiences but one backend fetch. Some waiters may time out while the fill succeeds. Reporting 99 hits invents semantics; report request outcome, coalescing, fetch, latency, and cancellation separately.

**Conclusion.** Metric denominators must follow event identity.

### Example 10

**Situation.** A shadow policy improves byte hit rate but doubles 99.9th-percentile metadata latency.

**Reasoning.** The service objective includes tail latency and CPU, not only bytes. Segment by tenant and object class, verify shadow-state fidelity, and roll out only within memory and latency guardrails. If shadow observations drive tuning, use a fresh confirmation interval.

**Conclusion.** Deploy on total service evidence, not a single cache metric.

## Cross-Program Connections

- **Operating Systems:** virtual memory adds page tables, working sets, dirty writeback, reclaim, and thrashing mechanisms.
- **Computer Architecture:** hardware caches add associativity, line granularity, coherence, prefetch, and replacement under tight metadata budgets.
- **Database Engineering:** buffer pools coordinate replacement with latches, transactions, write-ahead logging, and scan resistance.
- **Distributed Systems Engineering:** remote caches add consistency, invalidation, replication, stampedes, and partial failure.
- **Security Engineering:** keys, tenant isolation, timing, poisoning, and stale authorization expand the threat surface.
- **Platform Engineering:** quotas, shared-service objectives, observability, and rollout govern multi-tenant cache operation.
- **Data Structures Engineering:** hashing, ordered maps, heaps, sketches, and queues determine policy overhead.
- **Algorithm Engineering:** [ALGE-071](./071-online-decisions-and-competitive-analysis.md) provides the model; [ALGE-073](../ROADMAP.md#block-08--online-streaming-and-dynamic-algorithms) carries competitive reasoning into scheduling.

## References

1. László A. Belady, “A Study of Replacement Algorithms for a Virtual-Storage Computer,” *IBM Systems Journal* 5(2), 1966, 78–101. DOI: [10.1147/sj.52.0078](https://doi.org/10.1147/sj.52.0078). Primary source for offline optimal replacement and replacement anomalies; record checked 2026-09-05.
2. Daniel D. Sleator and Robert E. Tarjan, “Amortized Efficiency of List Update and Paging Rules,” *Communications of the ACM* 28(2), 1985, 202–208. DOI: [10.1145/2786.2793](https://doi.org/10.1145/2786.2793). Primary source for competitive paging analysis; ACM record checked 2026-09-05.
3. Richard L. Mattson, Jan Gecsei, Donald R. Slutz, and Irving L. Traiger, “Evaluation Techniques for Storage Hierarchies,” *IBM Systems Journal* 9(2), 1970, 78–117. DOI: [10.1147/sj.92.0078](https://doi.org/10.1147/sj.92.0078). Primary source for stack-distance evaluation; record checked 2026-09-05.
4. Peter J. Denning, “The Working Set Model for Program Behavior,” *Communications of the ACM* 11(5), 1968, 323–333. DOI: [10.1145/363095.363141](https://doi.org/10.1145/363095.363141). Primary source for working-set locality; ACM record checked 2026-09-05.
5. Amos Fiat, Richard M. Karp, Michael Luby, Lyle A. McGeoch, Daniel D. Sleator, and Neal E. Young, “Competitive Paging Algorithms,” *Journal of Algorithms* 12(4), 1991, 685–699. DOI: [10.1016/0196-6774(91)90041-V](https://doi.org/10.1016/0196-6774(91)90041-V). Primary source for randomized competitive paging; publisher record checked 2026-09-05.
6. Elizabeth J. O'Neil, Patrick E. O'Neil, and Gerhard Weikum, “The LRU-K Page Replacement Algorithm for Database Disk Buffering,” *SIGMOD 1993*, 297–306. DOI: [10.1145/170035.170081](https://doi.org/10.1145/170035.170081). Primary source for history-aware database replacement; ACM record checked 2026-09-05.
7. Song Jiang and Xiaodong Zhang, “LIRS: An Efficient Low Inter-reference Recency Set Replacement Policy to Improve Buffer Cache Performance,” *SIGMETRICS 2002*, 31–42. DOI: [10.1145/511334.511340](https://doi.org/10.1145/511334.511340). Primary source for reuse-distance-oriented replacement; ACM record checked 2026-09-05.
8. Nimrod Megiddo and Dharmendra S. Modha, “ARC: A Self-Tuning, Low Overhead Replacement Cache,” *FAST 2003*, 115–130. [USENIX paper](https://www.usenix.org/conference/fast-03/arc-self-tuning-low-overhead-replacement-cache). Primary source for adaptive replacement; official proceedings checked 2026-09-05.

## Exercises

### Exercise 1

Trace LRU and FIFO with capacity 3 on $A,B,C,A,D,B$. Give hit/fault outcomes, each final order, and the first request where their victim choices differ.

### Exercise 2

State the two cases in the LRU phase proof. Explain why LRU faults at most $k$ times per phase and why offline must fault across successive phase boundaries. Identify where the additive constant enters.

### Exercise 3

A cache reports a 95% hit rate but omits bypasses, stale rejections, coalesced waiters, and failed fills. Design an event schema and recompute-ready metrics that prevent misleading denominators.

### Exercise 4

Design a policy for variable-sized, unequal-latency, sometimes-dirty objects under a byte budget. Separate admission, eviction, writeback, expiration, and invalidation; state what is theorem-backed and what requires experiments.

### Exercise 5

A multi-tenant service wants to replace LRU with a learned policy. Design a leakage-resistant evaluation and rollout addressing keys, fairness, future features, shadow state, feedback, resource overhead, failures, drift, and rollback.

## Answers to the Exercises

### Answer 1

Both policies fault on A, B, C and hold them in insertion/recency order. The second A is a hit: LRU order becomes $(B,C,A)$ while FIFO remains $(A,B,C)$. D faults; LRU evicts B and becomes $(C,A,D)$, while FIFO evicts A and becomes $(B,C,D)$. Thus D is the first request with different victims. Final B faults for LRU, evicting C and ending $(A,D,B)$; it hits for FIFO, whose insertion order remains $(B,C,D)$. LRU has 5 faults and FIFO 4 on this short trace.

### Answer 2

Greedy maximal phases contain at most $k$ distinct pages. Within a phase, a requested phase page is newer than every resident not yet requested in that phase, so LRU cannot evict and refault that page while old non-phase pages remain; at most the $k$ distinct phase pages fault. A new phase starts with a page that would be the $(k+1)$st distinct across the preceding maximal phase boundary. A size-$k$ cache cannot contain all relevant distinct pages, so offline pays at least one fault per appropriately disjoint boundary interval. Multiplying those charged offline faults by $k$ covers all complete LRU phases. The initial phase or initial cache mismatch is uncharged and contributes an additive term no more than $k$ under the stated convention.

### Answer 3

Assign each client request an identity and record lookup eligibility, bypass reason, key/version, freshness and authorization result, resident outcome, coalescing group, backend-fetch identity, fill result, eviction, writeback, bytes, latency, timeout, and served outcome. Report request hit fraction over all eligible lookups, bypass rate over requests, stale-rejection rate, backend fetches per request, coalesced waiters, fill failure, byte hit rate, and latency distributions. Never relabel waiters as resident hits. Publish denominators and allow reconstruction from immutable events.

### Answer 4

Capacity sums resident bytes. Admission estimates whether expected latency or backend cost saved justifies object size and displacement. Eviction ranks admitted residents using size, retrieval cost, reuse evidence, and dirty-write consequence. Writeback has a bounded queue, durability owner, retry and shutdown semantics. Expiration and invalidation override ranking when freshness fails. Independently validate capacity, key, freshness, and dirty-state invariants. Classical LRU and MIN theorems do not directly cover this model; any new bound must be proved under its assumptions. Candidate scores, thresholds, and operational benefit require held-out traces, adversarial scans, write failures, tail measurements, and shadow or staged rollout.

### Answer 5

Bind keys to tenant and security semantics; define per-tenant service and capacity goals. Preserve chronological source-group trace splits and permit only prefix features available before eviction, charging feature cost. Run an independent shadow cache so alternative decisions do not mutate active state, and acknowledge that policy-induced future demand limits replay. Compare with LRU, simple admission, and oracle bounds under the same byte and metadata budgets. Retain stale, failed, timeout, and overload outcomes; report tenant tails and backend load. Gate rollout by correctness, isolation, memory, CPU, latency, and fairness; start with a small cohort and preserve instant bypass or LRU fallback. Monitor feature and outcome drift. If shadow or rollout data tune the model, require a fresh confirmation window before renewed claims.
