---
module_id: DSE-029
program: Data Structures Engineering
level: 1
module_number: 29
title: Hash-Flooding Resistance
status: complete
last_verified: 2026-08-30
---

# Hash-Flooding Resistance

## One-Page Review

### Governing question

How should an engineer prevent attacker-chosen keys from turning expected-constant-time hash-table operations into an availability failure, without confusing probabilistic resistance, deterministic bounds, and operational containment?

### Essential definitions

- A **hash flood** is a workload that forces many distinct keys into the same bucket, probe neighborhood, or otherwise expensive collision pattern.
- An **algorithmic-complexity attack** uses valid-looking input to trigger a data structure's expensive case and amplify attacker work into CPU, memory, or latency consumption.
- A **threat model** states which keys, timing observations, retries, process instances, hash implementations, and secrets the adversary can control or observe.
- A **keyed hash** maps a key under a secret seed; unpredictability can make collision construction computationally difficult while the seed remains secret.
- A **universal family** is a randomized family of functions with a bounded collision probability for each distinct key pair when the function is selected randomly.
- **Structural fallback** changes an overloaded collision container to a structure with a deterministic bound, such as a balanced tree when keys can be ordered safely.
- **work amplification** is defender resource consumed per unit of attacker-controlled input.
- **collision telemetry** measures chain length, probe work, equality calls, fallback conversions, or operation time rather than load factor alone.
- **reseeding** chooses a new secret and rebuilds placement; it is a recovery operation, not an unlimited retry strategy.
- A **resource envelope** caps accepted keys, bytes, nesting, CPU/work, memory, retries, or request rate before the table exhausts the service.

### Central model, mechanism, or theorem

For separate chaining, let bucket loads be `b_0,...,b_(m-1)` with `sum b_i=n`. A successful construction that checks equality through each existing chain can require work proportional to

`W = sum_i b_i(b_i+1)/2`.

Balanced loads make `W` near `Theta(n+n^2/m)`; one bucket with `n` distinct colliding keys makes `W=n(n+1)/2=Theta(n^2)`, while a later lookup may inspect `Theta(n)` entries. Resizing does not help if the same chosen keys collide under every new capacity.

A randomly selected universal hash family can bound the probability that any fixed distinct pair collides, and a secret keyed pseudorandom function can make useful collision construction difficult under a computational threat model. Neither yields a deterministic per-operation worst-case bound. A balanced collision container can provide such a bound for its own comparisons, but only when ordering, equality, conversion, memory, and concurrency semantics are sound. Production resistance is layered: unpredictable placement, structurally bounded fallback where appropriate, resource limits, detection, safe recovery, and evidence under adversarial workloads.

### Critical invariants

1. Equal keys always hash and compare consistently; distinct colliding keys remain distinct logical entries.
2. Hash seeds are initialized from an appropriate randomness source, scoped deliberately, kept out of logs/serialization, and never accepted from untrusted input.
3. Every operation has one defined collision-resolution path and remains reachable after seed changes, resize, fallback conversion, and recovery failure.
4. Fallback conversion preserves exactly the same key/value set and count; ordering used internally never changes semantic equality.
5. Collision detection counts actual work and cannot itself become an attacker-amplified scan.
6. Reseeding/rebuilding is failure-atomic, bounded in frequency, and does not expose a retry loop that an attacker can trigger indefinitely.
7. Request, key, byte, work, memory, and concurrency limits apply before irreversible resource exhaustion.
8. Claims distinguish expected, high-probability, computational, amortized, and deterministic guarantees.

### Common failures

- Calling average-case `O(1)` a worst-case or security guarantee.
- Adding a public or predictable salt to a weak hash and calling it secret-keyed.
- Using a fast seeded non-cryptographic hash whose seed can be recovered through timing or chosen queries.
- Resizing repeatedly while the attacker's keys keep the same collision relation.
- Treating a cryptographic digest with a public key—or no key—as sufficient against online bucket search.
- Treeifying without a total internal ordering, exact conversion proof, or protection from expensive comparison callbacks.
- Reseeding on every long probe and creating a rebuild-amplification attack.
- Measuring only load factor while one bucket or probe path dominates work.
- Reusing one seed across tenants, snapshots, forks, or long-lived trust boundaries without an explicit policy.
- Assuming a runtime's default map protects custom hashes or a replacement hasher equally.

### Compact example

Take 64 distinct permutations of the same eight ASCII characters. A toy byte-sum hash sends all of them to one of 64 buckets because every permutation has the same sum. Chained construction performs `1+...+64=2,080` units of modeled work. A fixed public member of an affine hash family distributes this finite set over 42 buckets, with maximum chain four and modeled work 92. This is reproducible evidence about one key set and one public parameter choice—not a security proof. A real deployment needs an unpredictable secret, a reviewed keyed algorithm, resource limits, and measurements against an adaptive adversary.

### Connections

[DSE-021](021-hash-functions-and-distribution.md) owns distribution and reduction; [DSE-022](022-separate-chaining.md) and [DSE-023](023-linear-probing.md) expose collision costs; [DSE-028](028-resizing-and-incremental-rehashing.md) supplies safe rebuild/reseed machinery. The [program roadmap](../ROADMAP.md) next integrates hashing, layout, and memory accounting into a memory-efficient map.

## Governing Question

Which threat model, hash-family guarantee, collision fallback, work detector, recovery protocol, resource envelope, and validation evidence make a hash table defensible when keys originate outside the trust boundary?

## Why This Matters

A hash table is often chosen because lookup and insertion are expected to be constant time. That expectation depends on placement not concentrating too much work. When a network parser, HTTP parameter collector, symbol table, cache, telemetry index, or deserializer inserts attacker-influenced keys, the attacker may choose exactly the input distribution that the average-case argument excludes.

The resulting attack can be asymmetric. A small request encodes many carefully selected keys; the service spends quadratic equality/probe work, blocks an event loop or worker, retains large intermediate state, and delays unrelated clients. The input may be syntactically valid, so memory safety, authentication, and conventional malformed-input checks do not stop it. MITRE classifies this broader condition as inefficient algorithmic complexity affecting availability.

Hash flooding is not solved by one magic function. A keyed algorithm may frustrate offline collision generation yet permit work exhaustion from sheer volume. A tree fallback bounds a bin but adds memory, branches, ordering requirements, and callback hazards. Input limits contain one request but must account for distributed requests and legitimate large workloads. Detection and reseeding can recover, but rebuilds themselves cost `Theta(n)` and can be weaponized. Engineering quality comes from matching layered controls to a precise adversary.

## Prerequisites and Retrieval

Retrieve abstraction, cost models, representation invariants, cache effects, generic callbacks, testing, and benchmarking from [DSE-001](001-abstract-data-types-and-concrete-representations.md) through [DSE-010](010-benchmarking-a-structure-without-misleading-results.md). Retrieve hash quality and reduction from [DSE-021](021-hash-functions-and-distribution.md), chained-bin costs from [DSE-022](022-separate-chaining.md), open-addressed probe behavior from [DSE-023](023-linear-probing.md) through [DSE-027](027-hopscotch-hashing.md), and failure-atomic reseeding from [DSE-028](028-resizing-and-incremental-rehashing.md).

## Learning Objectives

After completing this module, you should be able to:

1. derive collision-driven lookup and construction amplification for chained and open-addressed tables;
2. write a threat model that includes chosen keys, timing feedback, retries, seed lifetime, and multi-tenant scope;
3. distinguish ordinary distribution, universal hashing, keyed pseudorandom hashing, collision resistance, and deterministic fallback bounds;
4. select and initialize a reviewed keyed table hash without inventing a security primitive;
5. design balanced-bin or alternate-structure fallback with semantic and resource invariants;
6. detect pathological collision work using bounded per-operation accounting and useful telemetry;
7. make reseeding/rebuild recovery failure-atomic and resistant to repeated-trigger amplification;
8. layer entry, byte, depth, work, memory, time, concurrency, and rate limits at ingestion boundaries;
9. test seed independence, hostile custom hashes, adaptive workloads, failures, and concurrent recovery;
10. benchmark normal overhead and adversarial tails without claiming that one finite experiment proves security.

## Core Exposition

**Begin with the adversary, not the hash function.** Identify the concrete table and the path by which keys reach it. An HTTP framework may collect parameter names; a compiler may intern source identifiers; a proxy may index headers or destinations; a cache may accept user-selected object names. Determine whether the adversary can choose arbitrary bytes, repeat queries, measure latency, observe iteration order, crash/restart workers, share a process with another tenant, supply a custom hash callback, or inspect source and binaries.

Source secrecy is never a sound defense. Assume the layout and algorithm are known. What may remain secret is a randomly generated key with a defined scope and lifetime. If an attacker can query the table adaptively, timing and acceptance behavior become an oracle. If a seed is process-global, one tenant's observations may help target another table. If a virtual-machine snapshot, fork, deterministic test fixture, or serialized image clones the seed, nominally separate instances can share placement.

State the protected outcome. It may be bounded request CPU, bounded event-loop delay, bounded memory before rejection, acceptable p99 latency, or continued service for other tenants. “No collisions” is impossible when an unbounded key space maps to a finite table. The goal is to prevent predictable concentration or to bound its operational consequence.

**Collision amplification has a simple accounting proof.** In separate chaining, suppose insertion of a distinct key scans the resident bin to rule out equality before appending. If a final bin has `b` keys, those insertions perform at least `0+1+...+(b-1)` resident comparisons, and counting the append/terminal decision gives `b(b+1)/2` work units. Summing over bins gives the model in the review.

If all `n` keys collide, construction is quadratic and a miss scans `n` entries. With balanced loads, convexity makes the sum far smaller. The exact constant depends on cached hashes, equality cost, insertion order, allocator, and layout, but the asymptotic amplification does not. An attacker-controlled equality method can make each comparison expensive or reentrant, multiplying the damage beyond chain length.

Open addressing stores no explicit chain, yet the attack surface remains. Many equal full hashes can follow the same probe sequence. Chosen low bits can create primary clustering under some schemes; tombstones and high fill lengthen unsuccessful searches. Robin Hood, cuckoo, and hopscotch variants move the failure surface into displacement, relocation, stash, neighborhood, or rebuild work. Each design needs a representation-specific detector; “maximum bucket length” is meaningless for a flat table.

**Resizing is not collision resistance.** If the hash function returns the same full hash for every malicious key, any modulus or mask sends them through the same initial placement logic after growth. A larger table adds empty capacity but does not restore entropy. Repeated growth increases allocation and migration work and may worsen the denial of service.

A same-capacity rebuild with a genuinely new secret can change placement. [DSE-028](028-resizing-and-incremental-rehashing.md) explains how to preserve the logical map through that transformation. Security adds a trigger and retry budget: an attacker must not be able to force unlimited `Theta(n)` rebuilds. If the attack continues after one recovery, degrade, reject, isolate, or switch structure rather than spin through secrets.

**A good unkeyed distribution function solves a different problem.** Avalanche, bit diffusion, and low empirical collision rates help benign workloads. But an algorithm and its fixed parameters are public; an adversary can search offline for colliding reduced outputs or exploit algebraic weaknesses. Even a cryptographic hash without a secret maps many possible keys into every finite bucket. Offline precomputation and online sampling remain possible at costs determined by the visible output used for placement.

Adding a seed does not automatically fix this. A weak linear or otherwise invertible mixing function may leak its seed through chosen inputs, timings, returned hashes, iteration order, or other side channels. A 32-bit seed may be exhaustible. Review the security claim of the keyed construction rather than assuming any random integer creates a pseudorandom function.

**Universal hashing gives a mathematical probability statement.** Let `H` be a family selected randomly. A universal family commonly ensures that for any fixed distinct `x,y`, `Pr_h[h(x)=h(y)] <= 1/m` (or a stated family-specific bound) when `h` is drawn from `H`. Linearity of expectation then bounds expected colliding pairs for a fixed key set chosen independently of the secret function.

That quantifier order matters. The guarantee is over random function choice for fixed inputs; it is not “every selected function handles every set.” Stronger independence notions support stronger tail bounds. Adaptive attackers with observations, weak randomness, seed reuse, or implementation leakage require additional analysis. Universal hashing is information-theoretic in its defined model; it is not identical to a cryptographic pseudorandom function.

**A keyed pseudorandom function gives a computational statement.** SipHash was designed as a fast short-input PRF, explicitly including hash-table flood defense among its applications. The desired reasoning is that, without the secret, a computationally bounded attacker cannot predict collision behavior substantially better than against an appropriate random function, within the primitive's security and query limits.

This is not ordinary cryptographic collision resistance. A table often consumes only enough output bits to choose among `m` buckets, so bucket collisions are expected. The secret prevents efficiently choosing a concentrated set in advance; it does not prevent random collisions, huge input volume, key leakage, implementation flaws, or compromised seeds. Do not substitute a home-grown construction because it benchmarks faster.

Current runtimes illustrate scoped policies rather than a universal recipe. Python's PEP 456 introduced a keyed SipHash design for `str` and `bytes`; current CPython source defines the actual compiled hash choices and parameters. Rust documents that the default `HashMap` uses a randomly seeded algorithm selected for HashDoS resistance, while also warning that replacing its hasher or using a fixed non-random construction can remove that property. Go's current runtime map stores a per-map random seed, and the official `hash/maphash` package documents a separately seeded byte-sequence hash intended to resist adversarial collision construction. Exact algorithms are versioned implementation details unless the API promises them.

**Seed lifecycle is part of the invariant.** Generate the seed using the platform's suitable randomness facility before processing untrusted keys. Define whether it is per map, process, tenant, or security domain. Per-map seeds reduce cross-table learning but cost initialization/state and complicate deterministic snapshots. A process seed is simpler but widens the blast radius. Long-lived seeds provide more oracle observations; frequent rotation requires costly rebuild and coordination.

Never log, expose through diagnostics, serialize, or derive the seed from predictable timestamps, process IDs, addresses, or caller-controlled values. Handle early-boot entropy and initialization failure according to the platform contract. After fork, clone, restore, or sandbox duplication, decide whether to reseed safely. Tests may inject a fixed seed for reproducibility only through a clearly non-production path; the executable example's public key is therefore labeled test-only.

**Deterministic structural fallback addresses the residual worst case.** A chaining table can replace a long linked bin with a balanced search tree. If tree height remains `O(log b)`, lookup and insertion in that collision container need `O(log b)` comparisons rather than `O(b)`. OpenJDK's current `HashMap` source defines treeification, untreeification, and a minimum capacity threshold; those concrete constants and tie-breaking rules belong to that implementation.

Conversion needs a proof. Every node must move exactly once, cached hash/equality must remain consistent, size must not change, and lookup must route to the new bin representation only after publication. Conversion failure must preserve the old bin or a recoverable state. Deletion may untreeify with hysteresis to avoid repeated conversion. Resize must split or rebuild tree bins without losing their invariants.

Generic keys complicate ordering. Semantic equality may not have a compatible total order. User comparison can throw, recurse, mutate, block, or be adversarially slow. An implementation can order first by full hash and use a stable internal tie-break for unequal colliders, but that tie-break must not redefine key equality or leak sensitive placement. Garbage-collected identity, moving objects, serialization, and cross-run determinism add constraints. A balanced fallback bounds comparison count, not comparison cost, allocation, locking, or cache misses.

An ordered map, trie/radix tree for bounded strings, crit-bit tree, or sorted vector may be a better primary structure when deterministic bounds, prefix/range operations, or auditing matter more than average constants. The switch can be per bin, per request, or architectural. Each option changes memory locality, iteration order, key restrictions, mutation cost, and concurrency.

**Operational limits stop the work before theory is exhausted.** Cap the number of fields/keys per request, total decoded bytes, individual key length, nesting depth, duplicate policy, aggregate tenant entries, table capacity, allocation bytes, and concurrent builders. Apply limits during parsing and canonicalization, before constructing all keys. A post-hoc table-size check arrives after the expensive work.

Also cap work: hash bytes processed, equality/probe steps, fallback conversions, reseeds, rebuild bytes, and request CPU/deadline. Rate limits and admission control aggregate repeated small requests. Backpressure protects shared executors. Quotas should reflect authenticated tenant identity when available so a distributed attacker cannot evade a per-connection limit trivially.

Limits are product semantics. Return a typed rejection, partial-result policy, or shed-load response; do not silently drop arbitrary associations. Size caps alone do not cover a few extremely long keys or expensive user callbacks. CPU deadlines alone may be too late for memory pressure. Layer dimensions and document legitimate high-volume workflows.

**Detection measures collision work directly and cheaply.** For chaining, record maximum/percentile bin length, hash-equal-but-key-unequal comparisons, and tree conversions. For open addressing, record probe groups/slots, displacement, relocation attempts, stash occupancy, retries, and rebuild causes. Across designs, capture operation duration, keyed-hash bytes/cycles, equality callbacks, capacity/load/fill, rejected work, and affected tenant/request.

Update bounded counters along the normal operation path; do not scan the entire table on every insert. Sample high-cardinality labels and avoid logging raw untrusted keys or seeds. Alert on rates and tails, not one collision. Benign skew, tiny tables, bulk loading, poor custom hashes, and cold-cache events can trigger thresholds, so response should be graduated.

A useful state machine is NORMAL, SUSPECT, MITIGATING, and CONTAINED. SUSPECT may increase sampling or lower admission. MITIGATING can perform at most one failure-atomic reseed/rebuild or bin conversion under a budget. If the pathology remains, CONTAINED rejects excess work, isolates the tenant, or switches to a bounded structure. Cooldown and hysteresis prevent oscillation.

**Recovery must preserve availability and map correctness.** Allocate/build a reseeded destination while retaining the source, recompute every live key under the new secret, validate exact content/count, then publish and retire safely. If hashing, equality, allocation, comparison, or movement fails, retain the source and enter a bounded degraded policy. Never publish half a seed change: lookups computed with the new seed cannot find old placements.

Concurrent tables need a generation/authority protocol. Readers must know which seed/table generation to query; writers and migration cannot create ambiguous duplicates; helpers cannot initiate competing reseeds; old storage and old seed state remain until readers are excluded. A global stop-the-world lock is simpler but may violate the latency outcome being protected. Incremental recovery spreads work but extends the period of doubled memory and mixed authority.

Do not automatically replay attacker-controlled hashing/equality indefinitely after failure. Put a total budget on attempts. Preserve diagnostic counters without retaining sensitive keys. If containment changes response semantics, surface it to observability and callers.

**Key semantics can defeat otherwise sound defenses.** Equal keys must produce the same full hash under one table seed. Mutable keys, inconsistent `hash`/equality, locale-sensitive normalization, Unicode canonicalization mismatches, or cross-type equality can cause misses, duplicates, or unexpected collision sets. Canonicalizing attacker strings may itself have nonlinear behavior or expansion, so bound it before hashing.

Custom hashers move responsibility. Rust explicitly permits alternate `BuildHasher` choices; C++ unordered containers are parameterized by a hasher and specify average versus worst-case complexity rather than mandating secret defense. A library should document whether supplied hashers are trusted, wrap them with secret finalization where mathematically sound, reject unsafe modes at untrusted boundaries, or require callers to own the threat model.

**Validation must test claims at their actual strength.** Functional property tests generate colliding-but-unequal keys and compare the map with a reference model. Invariant tests cover insert/update/delete, resize, fallback conversion, reseed, exceptions, and serialization. Seed tests establish that independently initialized maps usually differ for the same keys without exposing production secrets; fixed-seed known-answer tests verify implementation stability only when the algorithm is promised.

Adversarial tests include constant custom hashes, same-low-bit hashes, same-full-hash objects, long common prefixes, equality bombs under controlled counters, tombstone-heavy histories, and adaptive query sequences. Fault tests fail randomness, allocation, hash/equality, conversion, and rebuild. Concurrency tests pause at detection, generation publication, transfer, fallback publication, and retirement, then check histories and reclamation.

Security tests do not claim proof from a few collision sets. Review the primitive and randomness source, analyze leakage and query budgets, fuzz parser-to-table paths, and have named humans review the threat model when making an external assurance claim. Track dependency/runtime changes because default algorithms and seed policies can change.

Benchmark normal overhead and hostile tails separately. Report runtime/version, CPU, compiler, seed policy, table layout, key distributions/lengths, request boundaries, sizes, load, repetitions, uncertainty, throughput, p50/p95/p99/max latency, comparisons/probes, allocations, peak memory, fallbacks, reseeds, rejections, and raw artifacts. Never publish secret seeds from production. Compare against a bounded alternative and include the cost of detection and recovery, not merely steady-state lookup.

The executable trace below verifies the finite accounting model. It encodes each short ASCII string as a field element and applies one fixed public affine-family member, then reduces to 64 buckets. Its public constants make output reproducible and make it unsuitable as a production secret or cryptographic construction. The result demonstrates that one family member disperses one constructed key set; it does not establish a universal-family theorem, SipHash behavior, secret unpredictability, adaptive resistance, or production fitness.

<!-- bijux-verify: {"id":"finite-hash-flood-accounting","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"keys=64\nweak_distinct_buckets=1\nweak_max_chain=64\nweak_build_work=2080\nfamily_distinct_buckets=42\nfamily_max_chain=4\nfamily_build_work=92\npublic_parameters_test_only=True\nevidence=finite_hash_family_trace\n","stderr":""}} -->
```python
from itertools import islice, permutations


BUCKETS = 64
PRIME = 1_000_000_007
MULTIPLIER = 6_364_136_223_846_793_005
OFFSET = 1_442_695_040_888_963_407


def weak_bucket(key):
    return sum(key.encode("ascii")) % BUCKETS


def field_encoding(key):
    value = 0
    for byte in key.encode("ascii"):
        value = (value * 257 + byte + 1) % PRIME
    return value


def family_bucket(key):
    field_value = field_encoding(key)
    return (
        (MULTIPLIER * field_value + OFFSET) % PRIME
    ) % BUCKETS


def profile(keys, bucket_function):
    loads = [0] * BUCKETS
    build_work = 0
    for key in keys:
        bucket = bucket_function(key)
        build_work += loads[bucket] + 1
        loads[bucket] += 1
    occupied = [load for load in loads if load]
    return len(occupied), max(occupied), build_work


keys = ["".join(p) for p in islice(permutations("abcdefgh"), 64)]
assert len(keys) == len(set(keys)) == 64
assert len({field_encoding(key) for key in keys}) == 64
weak_distinct, weak_max, weak_work = profile(keys, weak_bucket)
family_distinct, family_max, family_work = profile(keys, family_bucket)

print(f"keys={len(keys)}")
print(f"weak_distinct_buckets={weak_distinct}")
print(f"weak_max_chain={weak_max}")
print(f"weak_build_work={weak_work}")
print(f"family_distinct_buckets={family_distinct}")
print(f"family_max_chain={family_max}")
print(f"family_build_work={family_work}")
print("public_parameters_test_only=True")
print("evidence=finite_hash_family_trace")
```

## Definitions and Notation

- `n`: live logical keys inserted into the table.
- `m`: bucket count or effective initial-placement range.
- `b_i`: number of keys assigned to collision container `i`.
- `W`: modeled chained construction work, `sum_i b_i(b_i+1)/2`.
- `H`: family of hash functions from which one function is selected.
- `h_k(x)`: hash of key `x` under secret/random choice `k`.
- **chosen-key adversary**: adversary able to select table keys, possibly adaptively.
- **oracle**: observable timing, order, acceptance, or output that leaks placement information.
- **computational guarantee**: bound relying on adversary resources and a primitive's security assumption.
- **probabilistic guarantee**: bound over random choices such as selection from a universal family.
- **deterministic bound**: bound holding for every allowed input under stated callback/model assumptions.
- **containment**: policy that rejects, isolates, rate-limits, or changes structure after a work budget is reached.

## Mechanisms, Invariants, or Proof Structure

The attack proof chooses distinct keys that concentrate bucket/probe work. In chaining, summing the growing collision-container scan yields quadratic construction and linear individual operations. Resizing under unchanged collision relations preserves concentration.

Randomized defenses change quantifiers. Universal hashing bounds pair-collision probability over a random function for fixed distinct inputs. A keyed PRF aims to make placement computationally unpredictable while the key remains secret. These support expected or computational resistance, not a deterministic `O(1)` operation bound.

Structural fallback changes the collision container and can provide `O(log b)` comparison count when balance, ordering, and callback assumptions hold. Operational containment bounds accepted input and total work. Correct recovery preserves exact logical content across a seed/table generation change, publishes one authority, limits retries, and reclaims old state only after readers are excluded.

## Alternatives and Trade-Offs

| Defense | Strongest relevant benefit | Cost or unresolved obligation |
|---|---|---|
| Reviewed keyed short-input hash | frustrates predictable chosen collisions under a computational model | secret randomness/lifecycle, hash cost, leakage analysis |
| Universal hash family | explicit collision probability for stated independence/model | random choice, quantifier discipline, adaptive/tail analysis |
| Per-map seed | isolates placement learning between maps | state/init cost, snapshot/fork/reseed policy |
| Process-wide seed | simple and cheap initialization | broader cross-table/tenant exposure |
| Balanced tree bins | deterministic logarithmic comparison count per large bin | node memory, ordering/tie-break, conversion and callback costs |
| Trie/radix/ordered map | input-independent structural bounds for suitable keys | locality, memory, key restrictions, different operations |
| Entry/byte/work limits | caps one ingestion path before exhaustion | product semantics and distributed-rate aggregation |
| Detect then reseed | repairs a learned/unlucky placement | `Theta(n)` rebuild and repeated-trigger amplification |
| Reject/isolate after budget | protects shared availability | false positives and degraded caller semantics |

## Failure Modes and Misconceptions

- **“Hash tables are `O(1)`.”** that is normally expected/amortized, not a universal adversarial bound.
- **“A collision means broken correctness.”** correct tables preserve distinct keys; the attack targets work and availability.
- **“A random salt makes any mixer safe.”** predictable, recoverable, or algebraically weak seeding may not hide placement.
- **“A cryptographic hash has no collisions.”** finite outputs and finite buckets necessarily collide; secrecy and threat model matter.
- **“Public SHA-256 fixes flooding.”** an attacker can still search visible reduced buckets online/offline and send enough input.
- **“Resize disperses the keys.”** not when their full hashes or relevant probe paths remain concentrated.
- **“Reseed whenever a threshold fires.”** unbounded rebuild retries are another denial-of-service mechanism.
- **“Treeification makes the table secure.”** it bounds comparisons only under ordering, callback, memory, and implementation assumptions.
- **“Load factor detects attacks.”** severe local concentration can occur at a low global load.
- **“The runtime default covers replacements.”** custom/user hashers can discard default resistance.
- **“One seed fits every tenant forever.”** scope and observation lifetime affect attack and blast-radius analysis.
- **“The demonstration proves the defense.”** a finite public-parameter trace is reproducibility evidence, not a probability or security proof.

## Worked Examples

### Example 1

Sixty-four permutations of `abcdefgh` have identical byte sums. A sum-mod-64 hash maps all to one bucket. Conclusion: distinct and superficially varied strings can be constructed to collide under a public algebraic hash.

### Example 2

A chain receives 64 distinct colliders. Modeled construction work is `1+...+64=64*65/2=2,080`, and a miss can inspect 64 residents. Conclusion: a linear per-operation worst case produces quadratic batch amplification.

### Example 3

The same 64 keys pass through one fixed affine-family member and occupy 42 buckets with maximum load four. Conclusion: this one result supports only a finite regression test, not a family-wide probability or unpredictability claim because the parameters are public and fixed.

### Example 4

A server doubles from 1,024 to 2,048 buckets, but every hostile object's custom hash is zero. All keys retain the same initial bucket/probe sequence. Conclusion: added capacity is not new entropy.

### Example 5

A universal family promises `Pr[h(x)=h(y)] <= 1/m` for each fixed distinct pair and random `h`. An attacker chooses keys after learning `h`. Conclusion: the theorem cannot be applied without analyzing the changed quantifier/adaptive model.

### Example 6

A per-process secret protects built-in strings, but an API accepts objects whose custom hash always returns seven. Conclusion: the trusted callback boundary bypasses the runtime's string-hash defense.

### Example 7

A bin treeifies after sustained collision work. Its height is logarithmic, but every comparison invokes an attacker-defined comparator that sleeps. Conclusion: comparison-count bounds do not bound callback time.

### Example 8

Detection reseeds after a long probe; the attacker sends another batch that triggers detection by volume, causing repeated full rebuilds. Conclusion: recovery needs attempt, time, and allocation budgets plus containment.

### Example 9

An HTTP layer caps fields at 1,000 but permits 100 requests per millisecond from one tenant. Conclusion: per-request caps need tenant/rate/concurrency aggregation to protect shared capacity.

### Example 10

Two map instances receive the same strings but independent seeds. Their placement differs; tests that assert iteration order now fail. Conclusion: randomized placement is incompatible with depending on unspecified physical order, and reproducible tests should assert semantics instead.

## Cross-Program Connections

- **Algorithms:** adversarial analysis, convex collision cost, universal families, randomized algorithms, and tail bounds determine claim strength.
- **Security engineering:** threat models, key lifecycle, side channels, denial-of-service budgets, and tenant isolation turn a container choice into an availability control.
- **Programming languages:** custom hash/equality/comparison callbacks, exceptions, object identity, mutability, and runtime defaults define the trusted boundary.
- **Concurrent programming:** seed-generation publication, cooperative rebuild, generation routing, linearization, and reclamation govern live recovery.
- **Software engineering:** typed rejection, observability, cooldown state machines, dependency tracking, and incident evidence make defenses operable.
- **Database and data engineering:** ingestion cardinality limits, skew, partition hot spots, online reindexing, and multi-tenant quotas exhibit the same amplification pattern.
- **Computer architecture:** hash cost, branches, pointer-heavy tree bins, cache misses, memory bandwidth, and scheduler saturation determine practical thresholds.

## References

1. Scott A. Crosby and Dan S. Wallach, [Denial of Service via Algorithmic Complexity Attacks](https://www.usenix.org/conference/12th-usenix-security-symposium/denial-service-algorithmic-complexity-attacks). Primary attack model, measurements, and universal-hashing mitigation discussion.
2. Jean-Philippe Aumasson and Daniel J. Bernstein, [SipHash: a fast short-input PRF](https://eprint.iacr.org/2012/351.pdf). Primary design and security-goal source for a keyed short-input PRF aimed partly at hash-flood defense.
3. Python Enhancement Proposal 456, [Secure and interchangeable hash algorithm](https://peps.python.org/pep-0456/). Historical primary rationale, requirements, alternatives, and adoption record for keyed Python string/bytes hashing.
4. CPython Project, [`Python/pyhash.c`](https://github.com/python/cpython/blob/main/Python/pyhash.c). Current primary implementation source for compiled hash algorithms and parameters; it supersedes assumptions based only on the historical PEP.
5. Rust Project, [`std::collections::HashMap`](https://doc.rust-lang.org/std/collections/struct.HashMap.html). Current API documentation for random seeding, default HashDoS intent, entropy caveat, and replacement-hasher responsibility.
6. Go Project, [`hash/maphash`](https://pkg.go.dev/hash/maphash). Current official API documentation for independently seeded byte-sequence hashing intended to resist adversarial collision construction.
7. Go Project, [runtime maps `map.go`](https://go.dev/src/internal/runtime/maps/map.go). Current primary source showing per-map random seed ownership in Go's runtime representation.
8. OpenJDK Project, [`HashMap.java`](https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/java/util/HashMap.java). Current primary implementation source for treeification, untreeification, resize interaction, comparison/tie-breaking, and bin lookup.
9. ISO C++ working draft, [Unordered Associative Container Requirements](https://eel.is/c%2B%2Bdraft/unord.req.general). Current observable average/worst-case complexity and caller-supplied hash/equality contract without a mandated flood-defense algorithm.
10. MITRE, [CWE-407: Inefficient Algorithmic Complexity](https://cwe.mitre.org/data/definitions/407.html). Current authoritative weakness classification for attacker-triggerable worst-case resource consumption.

## Exercises

### Exercise 1

For a chained table with bucket loads `b_i`, derive construction and miss costs. Compare balanced placement with all `n` keys in one bucket, then explain why resizing under a constant full hash does not change the conclusion.

### Exercise 2

Write a threat model and seed-lifecycle policy for a multi-tenant service that parses user field names into maps. Include adaptive timing, process forks/snapshots, custom hashes, logs, recovery, and randomness failure.

### Exercise 3

Compare universal hashing, a keyed PRF, and balanced-bin fallback. State each guarantee with correct quantifiers/assumptions and show why no one mechanism alone proves bounded service latency.

### Exercise 4

Design a bounded NORMAL/SUSPECT/MITIGATING/CONTAINED response state machine. Specify metrics, thresholds, hysteresis, one failure-atomic reseed, fallback/rejection behavior, concurrency, and operator evidence.

### Exercise 5

Design functional, mathematical, fault, adversarial, concurrent, and benchmark evidence for a production map exposed to untrusted string keys. Include explicit non-claims.

## Answers to the Exercises

### Answer 1

For each final bucket of size `b_i`, sequential distinct insertion performs `0+...+(b_i-1)` resident comparisons; including one terminal/append unit per insert gives `b_i(b_i+1)/2`. Thus `W=sum_i b_i(b_i+1)/2`. If loads differ by at most one, `W` is on the order of `n+n^2/m`; if one bucket has all keys, `W=n(n+1)/2=Theta(n^2)`, and a later miss is `Theta(n)`. Doubling `m` changes reduction but a constant full hash, or any collision set preserved by the new reduction, still follows one bucket/probe origin. Only a placement-changing secret/function, structural fallback, or containment changes that attack argument.

### Answer 2

Treat arbitrary field bytes, request counts, timing observations, retries, and open-source implementation knowledge as attacker-controlled. Use the runtime's reviewed default keyed string hash or a reviewed keyed table hash, seed from the platform randomness facility before untrusted processing, scope at least per process/security domain and preferably per map when isolation justifies it, never log/serialize the seed, and define reseeding after fork/snapshot/restore. Reject unsafe custom hashers at this boundary or make their owners accept the threat. If randomness initialization fails, fail closed or use a documented contained mode rather than a predictable production seed. Cap fields, decoded bytes, key length, nesting, tenant rate/concurrency, entries, memory, hashing/equality work, and rebuild attempts. A single failure-atomic reseed retains the old map until validated publication; subsequent pathology switches to bounded fallback or tenant isolation/rejection. Tests inject fixed seeds only through a non-production seam.

### Answer 3

A universal family states a probability over random `h`, commonly `Pr_h[h(x)=h(y)]<=1/m` for every fixed distinct pair; stronger concentration requires stronger independence and non-adaptive assumptions. A keyed PRF states that a computationally bounded observer without secret `k` cannot distinguish/predict `h_k` enough to construct collisions beyond the named security/query advantage. Neither excludes random collisions or gives deterministic constant time. A balanced bin gives `O(log b)` comparison count for all admitted keys if balance, compatible internal order, conversion, and callback-cost assumptions hold, but adds memory and does not cap total `n`, hash bytes, allocation, locks, or request rate. Layer them with work/input/memory/time limits because service latency includes all those costs.

### Answer 4

NORMAL records bounded inline probes/comparisons, maximum local load, operation time, and tenant/request identity without raw keys. Crossing a rate-and-size-aware threshold enters SUSPECT, increases sampling, lowers admission, and confirms that work—not merely load—is abnormal. MITIGATING allows one serialized, capacity-budgeted, failure-atomic reseed/rebuild or bin conversion; readers/writers use an explicit generation/authority protocol and old state remains on failure. Continued pathology or exhausted time/memory/retry budget enters CONTAINED: reject excess fields/work, isolate/rate-limit the tenant, or route to a deterministically bounded structure. Cooldown and lower exit thresholds prevent oscillation. Evidence records trigger reason, seed generation identifier but never seed, work distribution, capacity/load, allocations, rebuild time/result, fallbacks, rejections, latency impact, and recovery age.

### Answer 5

Model-test insert/update/get/delete against a reference map using equal, unequal-colliding, mutable-rejected, and long keys; assert exact content/count through resize, treeify/untreeify, reseed, serialization, and recovery. Recompute the collision-work formula and any universal-family bounds independently with assumptions named. Inject randomness, allocation, hash, equality, comparison, conversion, rebuild, and publication failures. Exercise constant/same-low-bit/same-full-hash keys, long prefixes, bounded equality bombs, adaptive timing sequences, distributed requests, tombstones, and repeated triggers. Pause concurrent operations at detect/claim/copy/publish/retire boundaries; check linearizable histories, generation routing, races, and reclamation. Benchmark benign and hostile distributions over sizes/key lengths/load/request shapes, reporting versions, seed scope, throughput, p50/p95/p99/max, probes/comparisons/hash bytes, CPU, allocations/peak memory, conversions/reseeds/rejections, repetitions, uncertainty, and artifacts. Explicitly do not claim universal HashDoS immunity, cryptographic review, deterministic `O(1)`, bounded callback time, production latency, or external review from these tests alone.
