---
module_id: SEPAT-026
program: Software Engineering: Patterns
level: 1
module_number: 26
title: Flyweight
status: complete
last_verified: 2026-08-28
---

# Flyweight

## One-Page Review

### Governing question

When can a system replace many logically distinct objects with references to shared immutable representations, and how must identity, canonical keys, concurrency, lifetime, and measurement be specified so sharing remains correct and worthwhile?

### Essential definitions

- A **flyweight** is a shared object representing state common to many logical occurrences.
- **intrinsic state** is context-independent state stored in the shared flyweight.
- **extrinsic state** belongs to one occurrence or operation and is supplied by the client.
- A **flyweight factory** returns a canonical shared instance for a declared key.
- **canonicalization** maps equivalent inputs to one representative key or value.
- **interning** canonicalizes and shares values, commonly strings or symbols.
- **logical identity** distinguishes domain occurrences; **representation identity** asks whether references point to the same flyweight.
- A **strong pool** retains entries independently of clients; a **weak pool** permits collection when no strong client references remain.
- A **cardinality budget** bounds the number and size of canonical entries.
- **admission** and **eviction** policies control what may enter or leave a bounded pool.

### Central model, mechanism, or theorem

For (N) logical objects, suppose each unshared object stores intrinsic bytes (I), extrinsic bytes (E), and per-object overhead (O). If canonicalization yields $K\le N$ flyweights and each occurrence stores a reference of (R) bytes, idealized memory is

$$
M_{plain}=N(I+E+O),\qquad
M_{fly}=K(I+O)+N(E+R)+P,
$$

where (P) is pool/index overhead. Sharing helps only when measured (M_{fly}<M_{plain}) after allocator, key, synchronization, cache-locality, and lifetime costs. Correctness additionally requires immutable intrinsic state and a key function (k) that merges only semantically equivalent values.

### Critical invariants

- Equal canonical keys denote substitutable intrinsic state for every supported operation.
- Intrinsic state is immutable after publication, or mutation is safely versioned rather than shared silently.
- Extrinsic occurrence state never leaks into a shared flyweight.
- Canonical publication is linearizable where callers rely on one representative identity.
- Domain identity and authorization are never inferred from representation identity.
- Strong/weak retention, eviction, and resurrection behavior is explicit and tested.
- Untrusted cardinality, key size, construction cost, and contention are bounded.
- Memory and latency benefit is established with representative measurement, not object-count intuition.

### Common failures

Common failures include sharing mutable style/state, omitting locale or policy version from keys, using object address as domain identity, normalizing text with the wrong equivalence, racing check-then-create, holding strong values forever, assuming weak pools return the same identity across time, interning attacker-controlled unique strings, pooling scarce resources rather than immutable values, making eviction invalidate live references, ignoring hash-collision attacks, and spending more on keys, locks, or cache misses than sharing saves.

### Compact example

Four glyph occurrences have independent characters and coordinates but reuse two immutable styles keyed by `(font, size, color)`. The factory contains two styles; two red glyphs share one style reference while their positions remain distinct.

### Connections

[SEPAT-025](025-facade.md) simplifies a subsystem boundary; Flyweight reduces repeated representation. [SEPAT-027](../ROADMAP.md) controls access through a surrogate, and [SEPAT-030](../ROADMAP.md) evaluates structural combinations. Flyweight connects to [Object-Oriented Programming](../../02-programming-languages-object-oriented-programming/ROADMAP.md), [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md), and [Computer Architecture](../../23-computer-architecture/ROADMAP.md).

## Governing Question

Which state is truly identical across occurrences, what equivalence creates its canonical key, and does measured sharing improve the system after pool overhead and contention?

Flyweight is a representation optimization with semantic preconditions. It is justified by repeated immutable state and high cardinality of logical occurrences—not merely by a desire to use a cache.

## Why This Matters

Editors, compilers, renderers, games, databases, and language runtimes may represent millions of similar values. Duplicating fonts, symbols, schemas, coordinates, or transition tables can dominate memory and degrade cache locality.

Sharing introduces global coordination and surprising identity/lifetime behavior. A wrong key can merge distinct security or domain meanings. Therefore the optimization must begin with equivalence and ownership, then be validated by measurement.

## Prerequisites and Retrieval

You should understand immutable values, equality/hash contracts, dictionaries, references, garbage collection, synchronization, Unicode, and benchmarking. Retrieve these facts:

1. Value equality and reference identity answer different questions.
2. Hash equality narrows candidates; equality must still decide key equivalence.
3. Safe publication is required even when the published value will be immutable.
4. Weak references do not keep referents alive and therefore do not promise persistent identity.
5. Unicode canonical and compatibility equivalence are different relations.
6. Retained heap, allocation rate, cache locality, and contention are distinct metrics.

## Learning Objectives

After completing this module, you should be able to:

- separate intrinsic from extrinsic state;
- define and test a canonical key/equivalence relation;
- derive a memory break-even model and identify omitted costs;
- build a concurrency-safe flyweight factory;
- choose strong, weak, bounded, or scoped retention;
- protect pools against untrusted cardinality and collision pressure;
- distinguish Flyweight from caching, object pooling, prototypes, and value objects;
- validate correctness, memory, latency, contention, and lifecycle empirically.

## Core Exposition

### Find repeated immutable state

Profile allocations and retained heap. Group logical objects by candidate common fields and count unique combinations. State is intrinsic only if it has the same meaning independent of occurrence, caller, tenant, time, and operation context.

Coordinates, selection, owner, request context, and transient status are usually extrinsic. Font family and size may be intrinsic only if shaping engine, locale/script policy, rendering parameters, and version do not change their semantics.

### Define semantic equivalence

Write a key function before a pool. Require reflexivity, symmetry, and transitivity for equality, plus consistency with hashing. Include every dimension that affects supported behavior; exclude observationally irrelevant representation noise.

Canonicalization can lose information. Unicode NFC preserves canonical equivalence; NFKC applies compatibility mappings that may erase distinctions. Choose a normalization only when the domain's identity rules justify it, and version those rules where upgrades matter.

### Make shared state immutable

Construct completely before publication and expose no mutation path through aliases. Defensive-copy mutable inputs or convert them to immutable values. Return new versioned flyweights when intrinsic state changes.

Do not hide a mutable cache, lazy field, or statistics counter inside an allegedly immutable flyweight without a synchronization and observational contract.

### Keep occurrence state outside

Clients hold a small occurrence record containing logical identity, extrinsic state, and a flyweight reference. Operations receive remaining context explicitly.

If every call passes dozens of fields, the intrinsic/extrinsic split may harm cohesion. Reconsider the abstraction rather than forcing Flyweight.

### Publish canonically under concurrency

A naive `if key not in pool: pool[key]=create()` can build and publish several instances. That may be harmless if only value equality matters, but violates a one-identity promise and can duplicate expensive construction.

Use an atomic map primitive, lock, actor, or immutable snapshot appropriate to the runtime. Avoid invoking arbitrary user constructors while holding a global lock; handle constructor failure without poisoning the key.

### Choose lifetime deliberately

A strong pool gives stable identity while retained but can grow without bound. A weak-value pool permits collection, so two requests separated by collection may receive different representatives. A bounded pool limits memory but eviction means canonical identity is scoped to residency.

Often the best scope is an arena, document, compilation, request batch, or tenant rather than a process-wide singleton. Scope makes lifetime and cardinality easier to reason about.

### Bound hostile and accidental cardinality

Do not globally intern arbitrary user strings. Limit key length, canonical entry count, construction cost, and admission rate. Consider allowlists, per-tenant quotas, TinyLFU-like admission, or no sharing for one-hit values.

Use runtime-provided hardened hashing where appropriate, but still test collision behavior. Never place secrets directly in observable pool keys or telemetry.

### Preserve identity semantics

Reference equality may be an implementation optimization only. Domain entities still use their own stable IDs, authorization ownership, and lifecycle. Serialization sends values/keys, not memory addresses; deserialization may re-intern under local rules.

If public clients observe canonical object identity, changing pool scope or eviction becomes a compatibility change. Prefer value semantics unless identity sharing is essential.

### Measure the whole trade-off

Measure retained bytes, allocated bytes/op, collection time, lookup/construction latency, hit ratio, lock wait, cache misses, and tail latency. Use representative key distributions and warm/cold phases.

Heap profilers may count shared retained objects differently depending on roots. Document measurement method and compare against a non-flyweight baseline under identical workloads.

### Know when to remove it

Remove or narrow Flyweight when $K\approx N$, intrinsic state is tiny, keys duplicate the saved state, mutation/versioning dominates, contention rises, locality worsens, or the runtime already interns efficiently.

An optimization that no longer pays should not survive as architectural folklore.

## Definitions and Notation

Let occurrences be $o_1,\ldots,o_N$. Each has extrinsic state (e_i) and refers to flyweight (f_{k_i}), where canonical key function $k:Intrinsic\to Key$. Correct merging requires

$$
k(x)=k(y)\Rightarrow x\equiv_{ops}y,
$$

where $\equiv_{ops}$ means no supported operation can distinguish intrinsic semantics. The reverse implication is desirable for maximal sharing but not required for correctness.

Let empirical hit ratio (h=hits/lookups), unique cardinality (K), pool occupancy (K_t), and saved bytes estimate

$$
S=M_{plain}-M_{fly}.
$$

Positive (S) is necessary but insufficient: added CPU, latency, contention, and complexity must also fit budgets.

For a weak or evicting pool, canonical identity is interval-scoped: simultaneous live lookups may share, but `intern(x) is intern(x)` need not remain true after all strong references disappear or the entry is evicted.

## Mechanisms, Invariants, or Proof Structure

### Design procedure

1. Profile the baseline and identify repeated candidate state.
2. Specify supported observations and semantic equivalence.
3. Define canonical keys, normalization, and versions.
4. Make flyweights immutable and occurrence state explicit.
5. Choose publication, scope, retention, admission, and eviction.
6. Bound untrusted inputs and define telemetry.
7. Test equivalence, identity assumptions, races, and lifecycle.
8. Benchmark against the baseline and retain removal criteria.

### Executable mechanism

This deterministic example shares immutable style objects while keeping glyph character and position extrinsic. It does not estimate Python object memory or establish concurrent publication.

<!-- bijux-verify: {"id":"flyweight-glyph-styles","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"styles=2\nred-shared=True\npositions=10,20|30,20\n","stderr":""}} -->
```python
class GlyphStyle:
    def __init__(self, font, size, color):
        self.font = font
        self.size = size
        self.color = color


class StyleFactory:
    def __init__(self):
        self.styles = {}

    def style(self, font, size, color):
        key = (font, size, color)
        existing = self.styles.get(key)
        if existing is None:
            existing = GlyphStyle(font, size, color)
            self.styles[key] = existing
        return existing


factory = StyleFactory()
red_a = factory.style("Inter", 12, "red")
blue = factory.style("Inter", 12, "blue")
red_b = factory.style("Inter", 12, "red")
glyph_a = ("A", 10, 20, red_a)
glyph_b = ("B", 30, 20, red_b)
glyph_c = ("C", 50, 20, blue)

print("styles=" + str(len(factory.styles)))
print("red-shared=" + str(glyph_a[3] is glyph_b[3]))
print("positions=" + str(glyph_a[1]) + "," + str(glyph_a[2]) + "|" + str(glyph_b[1]) + "," + str(glyph_b[2]))
```

Production code would prevent style mutation, normalize/version keys deliberately, use safe concurrent publication, bound retention, and measure real object graphs.

### Proof obligations

For every merged pair, prove or test substitutability under declared operations. For publication, specify a linearization point or state that multiple equal representatives are allowed. For memory, validate model inputs empirically rather than treating nominal field sizes as allocator truth.

## Alternatives and Trade-Offs

| Approach | Reuses | Typical lifetime | Main distinction |
|---|---|---|---|
| Flyweight | immutable representation | shared/scoped | extrinsic occurrence state stays outside |
| Cache | computed result | policy-bound | hits improve recomputation/access cost |
| Object pool | reusable mutable resource | checkout/return | lifecycle and reset are central |
| Prototype | copied configured object | per clone | creates independent instances |
| Value object | semantic immutable value | ordinary ownership | sharing is optional implementation detail |
| Columnar/dictionary encoding | repeated field values | dataset/batch | representation is data-layout oriented |
| Arena/index table | indexed objects | explicit scope | bulk lifetime and compact indices |

Flyweight may use a cache-like factory, but eviction and identity promises differ. Choose the simplest representation meeting measured constraints.

## Failure Modes and Misconceptions

### “Identical-looking means equivalent”

Rendering, locale, normalization, policy, version, and permissions can distinguish values. Define semantic observations before merging.

### “The shared object can mutate carefully”

Mutation becomes nonlocal behavior for every occurrence. Prefer immutable replacement; otherwise specify synchronization, version visibility, and invalidation explicitly.

### “A dictionary makes construction thread-safe”

Individual map operations may be safe while check-create-publish is not atomic. Define the whole protocol and runtime guarantee.

### “Weak references solve leaks”

They change lifetime and identity and may cause churn. Keys or auxiliary metadata can still be retained strongly.

### “Intern everything”

Unique untrusted values turn sharing into a memory-denial vector. Admission and cardinality budgets are part of correctness.

### “Fewer objects always means faster”

Hashing, indirection, synchronization, poor locality, and collection behavior can outweigh allocation savings. Measure.

### “Flyweight identity is domain identity”

Canonical representation neither owns data nor grants authorization. Domain IDs and access rules remain separate.

## Worked Examples

### Example 1

One million glyphs use 24 measured styles. Positions and characters stay per occurrence; immutable shaping/render style is shared. Heap profiling confirms material retained-byte reduction. **Conclusion:** High (N/K) plus measured intrinsic size motivates Flyweight.

### Example 2

Every image has a unique 40-byte metadata key and a 32-byte intrinsic value. Pool/index/reference overhead exceeds saved data. **Conclusion:** High uniqueness and large keys fail the break-even test.

### Example 3

A style object exposes `set_color`; changing one selected glyph recolors thousands. Replacing mutation with a new interned style restores independence. **Conclusion:** Shared intrinsic state must be immutable.

### Example 4

A text pool applies NFKC when the domain requires canonically equivalent but compatibility-distinct identifiers. Two distinct identifiers merge. NFC with versioned domain rules is selected. **Conclusion:** Canonicalization relation is a domain decision.

### Example 5

Two threads miss one key and construct twice. `compute-if-absent`-equivalent publication yields one live representative; constructor failure leaves no poisoned entry. **Conclusion:** Canonical identity needs an atomic publication protocol.

### Example 6

A weak pool's only strong client releases a value; collection removes it, and a later lookup creates an equal but nonidentical object. Tests assert value equality, not timeless reference identity. **Conclusion:** Retention defines the identity interval.

### Example 7

An attacker submits millions of unique labels to a global strong pool. Per-tenant cardinality, key-length limits, admission frequency, and bounded eviction contain memory. **Conclusion:** Untrusted cardinality needs policy and quotas.

### Example 8

A compiler interns symbols per compilation arena rather than process-wide. Bulk release bounds lifetime and avoids cross-tenant vocabulary retention. **Conclusion:** Narrow scope often beats a singleton pool.

### Example 9

Profiling finds lock contention at a global flyweight factory. Sharded pools reduce contention but permit equal representatives across shards; clients already use value equality. **Conclusion:** Relax identity only when the public contract permits it.

### Example 10

A flight-control proposal shares mutable calibration objects across channels to save memory. Independent versioned immutable calibration snapshots and channel isolation are retained; memory optimization requires safety review. **Conclusion:** Sharing must not create common-mode hazards.

## Cross-Program Connections

- **Object-Oriented Programming:** equality, immutability, aliasing, identity, and encapsulation determine safety.
- **Functional Programming:** persistent immutable values and hash-consing provide related sharing models.
- **Concurrent Programming:** atomic publication, contention, memory visibility, and reclamation govern factories.
- **Data Structures Engineering:** hash tables, tries, collision behavior, and compact indices determine cost.
- **Database Engineering:** dictionary encoding and deduplication share values at storage/layout boundaries.
- **Computer Architecture:** cache locality, pointer chasing, allocation, and memory hierarchy shape performance.
- **Security Engineering:** cardinality attacks, tenant separation, secrets, and collision pressure constrain keys.
- **Compilers:** symbol interning, types, constants, and hash-consed syntax trees are classic applications.
- **Testing and Quality:** equivalence properties, race tests, heap profiles, and adversarial distributions provide evidence.
- **Systems Engineering:** common-mode failure and independent-channel requirements can prohibit sharing.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Canonical Flyweight intent, participants, applicability, and consequences.
2. Python Software Foundation, [`sys.intern`](https://docs.python.org/3/library/sys.html#sys.intern), Python 3.14 documentation, accessed 2026-08-28. Documents string interning and identity-based dictionary comparison optimization.
3. Python Software Foundation, [`weakref`](https://docs.python.org/3/library/weakref.html), Python 3.14 documentation, accessed 2026-08-28. Documents weak references and weak mappings whose entries disappear when referents lack strong references.
4. Oracle, [`String.intern`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/String.html#intern()), Java SE 25 API, accessed 2026-08-28. Specifies the canonical string representation returned from the intern pool.
5. Unicode Consortium, [Unicode Standard Annex #15: Unicode Normalization Forms](https://unicode.org/reports/tr15/), Unicode 17.0.0, revision 57, 2025. Defines canonical/compatibility equivalence and normalization behavior.
6. Robert Seacord, [SEI CERT Java Coding Guideline OBJ56-J: Provide sensitive mutable classes with unmodifiable wrappers](https://wiki.sei.cmu.edu/confluence/display/java/OBJ56-J.+Provide+sensitive+mutable+classes+with+unmodifiable+wrappers), Carnegie Mellon SEI, accessed 2026-08-28. Provides mutation/aliasing guidance relevant to shared representations.
7. Brian Goetz et al., *Java Concurrency in Practice*, Addison-Wesley, 2006, ISBN 978-0-321-34960-6. Provides safe publication, immutability, synchronization, and concurrent-map foundations.

## Exercises

### Exercise 1

Using the memory model, derive the break-even inequality and evaluate (N=1{,}000{,}000), (K=100), (I=64), (E=12), (O=16), (R=8), and (P=20{,}000) bytes.

### Exercise 2

Specify canonical keys for text styles across font, size, script, locale, shaping engine, features, color, and device scale. Justify each intrinsic/extrinsic decision.

### Exercise 3

Design a concurrent bounded weak flyweight factory. State its identity guarantee, linearization behavior, admission/eviction, and failure tests.

### Exercise 4

A global symbol pool grows without bound in a multitenant compiler service. Diagnose it and propose a measurable migration with compatibility safeguards.

### Exercise 5

Assess flyweight sharing of configuration/calibration data across redundant control channels in an unfamiliar safety-critical system without claiming suitability.

## Answers to the Exercises

### Answer 1

Sharing helps in the byte model when (K(I+O)+N(E+R)+P<N(I+E+O)), equivalently (N(I+O-R)>K(I+O)+P). Plain memory is (1{,}000{,}000(64+12+16)=92{,}000{,}000) bytes. Flyweight memory is (100(64+16)+1{,}000{,}000(12+8)+20{,}000=20{,}028{,}000) bytes. The modeled saving is 71,972,000 bytes.

This is not a heap measurement. It omits key objects, hash-table capacity, allocator rounding, references inside styles, fragmentation, GC metadata, synchronization, locality, and workload lifetime. Validate inputs with retained-heap profiling and compare throughput/tail latency with an identical nonshared workload.

### Answer 2

The key includes normalized font identity/version, size in an exact declared unit, script, language/locale when shaping differs, direction, shaping-engine/version, variation axes, feature set, and any rendering parameters that change reusable glyph metrics or output. Sort unordered feature entries canonically and reject duplicates/conflicts. Unicode normalization must match the identifier/domain contract rather than visual similarity.

Color is intrinsic if the shared object is a paint/render style and many occurrences repeat it; it is extrinsic if geometry/shaping is shared independently of paint. Device scale is intrinsic only for rasterized/device-specific artifacts; keep it extrinsic for scale-independent vector/style descriptions. Position, selection, document owner, request authorization, deadline, and animation time stay extrinsic. Property tests vary every key dimension and confirm that merging occurs exactly for declared observational equivalence.

### Answer 3

Use a lock or atomic concurrent-map operation per key to publish a fully constructed immutable value. Do not execute an unbounded/user callback under a global lock. Construction failure publishes nothing; waiters receive the original failure or retry by documented policy. A weak value entry does not guarantee identity after collection, while a bounded policy also permits identity change after eviction; guarantee only that overlapping live successful lookups for one key obtain an equivalent value, and promise same reference only if the mechanism can enforce it.

Bound keys and values, apply per-scope quotas, and admit only after repeated observation or explicit allowlisting. Eviction removes only the index reference and never mutates live values. Clean dead weak entries safely and avoid key retention. Tests cover same-key races, different keys, constructor failure/cancellation/reentrancy, collection, eviction with live clients, hot/cold skew, hostile uniqueness, hash collisions, quota fairness, and shutdown. Measure hit rate, occupancy, churn, retained bytes, construction, lock wait, and p99 latency.

### Answer 4

First profile retained paths, per-tenant unique cardinality, key/value bytes, hit frequency, age, and contention. Determine whether callers observe reference identity and whether symbols contain tenant-sensitive names. The likely defects are process-wide strong retention, admission of one-hit untrusted values, and missing tenant/scope boundaries.

Introduce per-compilation or per-tenant arenas with size/key limits and value-based equality. Add compatibility tests before relaxing reference identity; if public clients depend on it, migrate the contract explicitly. Reject conflicting normalization/version rules, redact metrics, and bulk-release arenas after compilation. Roll out behind a flag, shadow-count hits and estimated savings, compare heap/GC/latency, cap early cohorts, and retain rollback. Success requires bounded occupancy with unchanged compiler semantics and improved measured resource cost—not merely fewer nominal objects.

### Answer 5

Classify each datum by authority, version, update protocol, integrity protection, channel independence, and failure consequence. Immutable verified configuration snapshots may be referenced by several objects within one channel, but sharing mutable memory or one update/cache path across redundant channels can create common-mode failure. Preserve independent validation, storage, timing, and fallback where the hazard analysis requires independence; use content/version identifiers rather than pointer identity.

Evidence requires traceable requirements and hazard/common-cause analysis, immutable-data and publication review, formal/state analysis where tractable, integrity/authenticity and rollback protection, race/fault-injection tests, corrupted/stale/partial update cases, power-loss/restart, resource-exhaustion and timing analysis, simulator and hardware-in-the-loop validation, and controlled deployment/recovery exercises. Named controls/domain, functional-safety, hardware, real-time, cybersecurity, quality, regulatory, operations, and independent verification authorities decide acceptance. This chapter establishes no safety, redundancy, timing, or regulatory suitability.
