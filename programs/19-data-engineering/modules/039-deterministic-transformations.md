---
module_id: DE-039
program: Data Engineering
level: 1
module_number: 39
title: Deterministic Transformations
status: complete
last_verified: 2026-09-02
---

# Deterministic Transformations

## One-Page Review

### Governing question

What must a data transformation control, record, or deliberately abstract away so that the same governed inputs and semantic environment always yield the same promised output?

### Essential definitions

- A **deterministic transformation** produces one contract-equivalent output for every execution over the same complete input and environment envelope.
- The **determinism envelope** names every value that may affect the result: source and reference snapshots, code and configuration, schema, parameters, runtime, locale, collation, time-zone rules, clocks, randomness, external responses, partitioning, and arithmetic policy.
- **Observational equivalence** defines what “same output” means: equal keyed relation, equal ordered sequence, equal values within an approved numerical rule, or identical canonical bytes.
- **Reproducibility** is the ability to regenerate a contract-equivalent result later or elsewhere from retained evidence; it is related to, but not identical with, determinism.
- **Idempotence** means repeating a logical write has no additional logical effect; it does not prove that recomputing the value is deterministic.
- A **pure row transformation** depends only on its declared row arguments and has no clock, random, mutable-global, network, file, or database side input.
- A **total order** compares every pair relevant to output ordering and breaks all ties with stable, unique semantic keys.
- A **canonical representation** maps each equivalent abstract value to one agreed byte representation for hashing, signing, caching, or byte comparison.
- A **stable reduction** has an explicit input order and combination structure, or uses an operation whose result is invariant under every permitted reordering.
- **key-derived randomness** maps a pinned algorithm, namespace/seed, and stable business key to a pseudorandom-looking value without depending on traversal or worker draw order.
- An **output fingerprint** hashes a named canonical projection and algorithm; it is comparison evidence, not by itself proof that the projection is complete or correct.
- A **replay manifest** binds all semantic inputs and output identities required to attempt and assess reproduction.

### Central model, mechanism, or theorem

Let $S$ be an immutable governed source cut, $R$ the reference-data cut, $v$ the transformation version, $p$ the explicit parameters, and $E$ the semantic execution environment. Let $c$ range over allowed physical choices such as scan order, partitioning, worker assignment, retry order, and reduction tree. For observation function $O$ and declared equivalence relation $\equiv$, result determinism requires

$$
\forall c_1,c_2\in C(E):\quad
O(F_{v,p}(S,R,E,c_1))\equiv O(F_{v,p}(S,R,E,c_2)).
$$

The claim is only as strong as the envelope and comparator. If current time, a mutable exchange-rate table, collation version, or random draw order can influence the result but is absent from $E$, “same input” is false. If row sequence is contractual, set equality is too weak. A canonicalizer $K$ can make equivalent values byte-comparable when

$$
x\equiv y \Longrightarrow K(x)=K(y),
$$

but canonicalization cannot repair unequal values. Reproducibility additionally requires retained identities and artifacts sufficient to reconstruct $(S,R,v,p,E)$ and evaluate the same comparator.

### Critical invariants

- The output grain, key, schema, ordering promise, numerical policy, and equivalence comparator are explicit.
- Source and reference inputs resolve to immutable cuts or content identities, not mutable names alone.
- Code, compiled query/plan where relevant, configuration, parameters, schemas, dependencies, engine/runtime, and semantic environment are pinned.
- Business time enters as a field or parameter; processing clock, current date, and worker locale cannot leak into transformation meaning.
- Randomness is absent, recorded with stable draw assignment, or derived from stable keys under a pinned algorithm and namespace.
- Every ordering-sensitive operator has a complete stable order, including explicit null placement and a unique tie-breaker.
- Duplicate resolution and winner selection use identity and authoritative precedence, never incidental arrival or scan order.
- Aggregation documents exact/approximate arithmetic, overflow, rounding, null/NaN behavior, and permitted reduction order.
- Text normalization, comparison, collation, case mapping, encoding, and time-zone database/version are governed where semantically relevant.
- Canonical output bytes include a named schema/projection and serialization specification; presentation formatting is not confused with abstract equality.
- Parallelism, retries, optimizer changes, partition counts, and file layout may vary only where the comparator proves them unobservable.
- Repetition tests deliberately vary physical choices and compare both output and lineage against an independent oracle or invariant set.

### Common failures

Common failures include saying “same data” while reading a mutable table; using `now()`, current date, process locale, or ambient time zone inside business logic; selecting the first/last row without a complete order; relying on file or hash-map iteration order; seeding one shared generator while worker draw order changes; using random UUIDs as semantic identifiers; summing binary floating point through varying reduction trees and demanding byte equality; rounding each partition before global aggregation; accepting equal totals while keyed rows differ; serializing unordered objects and hashing the bytes; treating Unicode-equivalent strings as byte-identical without a normalization policy; assuming an `ORDER BY` with unresolved ties is total; mistaking repeatable local runs for universal determinism; pinning code but not reference data or tzdb; hiding meaningful sequence by sorting after the fact; and overwriting a trusted generation before the candidate comparison finishes.

### Compact example

Five deliveries contain three business events, one exact duplicate, and a revision. Two raw spellings of “Café” use composed and decomposed Unicode, while a governed upstream boundary supplies the same NFC-derived customer key. A deterministic model chooses the greatest authoritative revision by event ID, rejects equal-revision conflicts, sums decimal strings with exact decimal arithmetic, assigns a cohort by hashing a namespace plus customer key, sorts by that key, and emits a canonical tuple with an explicit `as_of`. Every permutation yields customers `Alice=5.00` and `Café=14.30`, total `19.30`, and the same digest. Replacing decimal addition with unordered binary-float reduction, shared random draws, or implicit current time would weaken that promise.

### Connections

[DE-010](010-designing-a-reproducible-data-boundary.md) defines captured source boundaries, [DE-027](027-idempotent-loads.md) distinguishes replay-safe effects, [DE-028](028-deduplication-and-record-identity.md) governs duplicate identity, and [DE-032](032-sql-transformation-pipelines.md) through [DE-038](038-late-corrections-and-restatement.md) define transformation, partition, incremental, merge, backfill, and correction semantics. DE-040 next turns these invariants into a multi-stage pipeline test strategy.

## Governing Question

When two runs receive “the same input,” which facts must truly be identical, which implementation choices may vary, and what evidence proves that the resulting outputs retain the same meaning?

A transformation is often written as if it were a mathematical function: input rows enter and output rows emerge. Production execution adds less visible arguments. The query may read a mutable reference table, call the clock, inherit a session time zone, compare strings under an upgraded collation, allocate random draws by traversal order, process floating-point values through a different reduction tree, or break equal sort keys according to a new plan. These are inputs whether or not the function signature admits them.

Determinism is also relative to observation. A SQL relation has no inherent presentation order, so two row sequences may denote the same relation. A report export may promise a sequence, making those outputs different. Two floating-point results may be accepted within a documented tolerance for scientific exploration but be unacceptable for ledger cents or a content-addressed artifact. A set comparator can hide duplicate-count errors; a checksum of arbitrary serialization can manufacture differences from harmless key order.

The engineering goal is not to force identical execution traces. It is to make every contractually meaningful choice explicit and stable while permitting harmless variation in worker placement, physical partitioning, file layout, or optimizer plan. This requires a semantic contract, an inventory of hidden inputs, deterministic operators or justified equivalence, and replay evidence.

## Why This Matters

Determinism makes incidents explainable. If a failed partition is retried against the same source cut and silently yields different rows, operators cannot tell whether the first or second answer is correct. If a historical backfill changes each time it runs, comparison to the published generation becomes inconclusive. Stable transformation meaning turns retries, backfills, correction restatements, and disaster recovery into controlled experiments.

It also protects incremental systems. An incremental result is expected to match a full transformation at the same cut. That differential oracle is useful only when the full transformation itself has one declared result. An arbitrary winner among duplicate keys can make both strategies alternate between plausible answers; repeated parity may then be accidental.

Content identities depend on canonical values. Caches, manifests, signatures, lineage receipts, and conditional publication often compare hashes. If two equal mappings serialize with different property or row order, they generate false cache misses and false drift alerts. If two unequal values collide because the hashed projection omitted a field, equal digests create false confidence. The canonical projection and algorithm are part of the contract.

Parallel execution exposes algebraic assumptions. Integer addition within bounded range is associative and commutative; binary floating-point addition generally is not associative. A distributed engine may combine partitions through different trees after a retry or scale change. The variation may be numerically tiny or materially amplified. Engineering must choose exact decimal/integer units, a fixed reduction, a stable summation method plus error bound, or an explicitly tolerant comparator according to the domain.

Text and civil time carry versioned semantics. Canonically equivalent Unicode sequences can have different bytes. Locale/collation changes can change comparison, grouping, and ordering. Governments revise civil-time rules; a named zone plus local timestamp may map differently under another time-zone database release, and ambiguous/nonexistent local times require a policy. Pinning only application source does not capture these dependencies.

Random sampling and assignment can be deterministic when designed carefully. A single seeded pseudorandom stream is stable only when algorithm, seed interpretation, number and order of draws, and version guarantees are fixed. In distributed work, partition or retry order can reassign draws to records. A keyed derivation gives each stable entity its own value independent of traversal, though it still needs a pinned algorithm, namespace, key encoding, and bias-aware mapping.

Finally, reproducibility is an audit and recovery capability. A manifest that names source snapshots, code digest, parameters, schemas, reference versions, runtime/container, locale/tzdb, arithmetic/canonicalization policy, and output fingerprint lets another execution attempt the same semantic computation. Missing artifacts, expired snapshots, mutable dependencies, or unavailable external responses bound the claim and must be visible.

## Prerequisites and Retrieval

Retrieve the target business contract; output grain, keys, multiplicity, ordering, schema, null/NaN/infinity policy, and accepted numerical equivalence; immutable source objects/snapshots/log intervals and checksums; reference/dimension snapshots; transformation source and compiled SQL/plan; parameters and feature flags; schema registry versions; engine/adapter/library/container/operating-system/architecture versions; optimizer and concurrency settings; locale, collation provider/version, character encoding, Unicode normalization and case policy; calendar, time zone, tzdb version, daylight-saving ambiguity policy, and timestamp precision; decimal scale/rounding/overflow and floating-point reduction policy; random algorithm/seed/namespace/key encoding; external service responses; UDF code and dependencies; input and output partition/file layout; duplicate/winner/tie rules; current-time and environment-variable use; canonical serialization/projection/hash; candidate generation and publication identities; lineage; prior reproducibility incidents; retention horizon; security and secret-handling boundaries; and recovery evidence.

Distinguish deterministic function from repeatable observation; deterministic result from deterministic trace; determinism from idempotence; replay from recomputation; source snapshot from mutable table name; business/event time from processing clock; stable sort implementation from total semantic order; row order from relational equality; set equality from multiset equality; key equality from payload equality; exact decimal from approximate binary float; stable sum from rounded display; pseudorandom stream from cryptographic randomness; seed from stable draw assignment; canonical value from pretty serialization; Unicode normalization from case/accent folding; collation equality from byte equality; named time zone from fixed UTC offset; code version from complete semantic environment; output digest from correctness proof; and reproducible artifact from recoverable publication.

Create a deterministic-transformation contract:

| Concern | Required decision and evidence |
|---|---|
| Observation | Grain, key, multiplicity, sequence/set semantics, schema, numerical comparator |
| Inputs | Immutable source/reference cuts, object/snapshot/log identities, completeness controls |
| Semantics | Code/compiled query, parameters, schema, UDFs, dependency and rule versions |
| Environment | Engine/runtime, locale/collation, Unicode, tzdb/calendar, architecture constraints |
| Effects | Clock, randomness, external I/O, environment variables, mutable globals, secrets |
| Ordering | Sort keys, directions, null placement, stable unique tie-breakers, ordered aggregates |
| Arithmetic | Types, scale, overflow, rounding point/mode, reduction tree or error/tolerance rule |
| Canonicalization | Text normalization, projection, row/property order, number encoding, hash algorithm |
| Execution | Partitioning, retry/speculation, concurrency, optimizer and resource variation allowed |
| Assurance | Repeated perturbation, reference/differential/metamorphic oracles, key-level diagnostics |
| Publication | Candidate identity, expected prior, output fingerprint, lineage, conditional promotion |
| Recovery | Retained envelope/artifacts, reconstruction procedure, retention limits, owner acceptance |

The contract should name deliberately irrelevant differences. File count, compression blocks, worker IDs, and physical row placement can vary if downstream meaning is a keyed relation and the canonical comparator ignores them. Do not promise byte identity unless consumers actually require it and every byte-producing dependency is governed.

## Learning Objectives

After completing this module, you should be able to:

1. define deterministic transformation results using a complete envelope, observation function, and equivalence relation;
2. distinguish determinism, reproducibility, replay, purity, idempotence, and canonicalization;
3. discover hidden inputs involving mutable reads, clocks, randomness, environment, locale, collation, time zones, and external services;
4. design complete ordering, duplicate-winner, window, and ordered-aggregate semantics with stable tie-breakers;
5. choose exact or approximate arithmetic and control reduction order, rounding, overflow, NaN, and tolerance behavior;
6. assign randomized cohorts or samples independently of traversal, partition, retry, and worker order;
7. canonicalize text and structured output without confusing byte stability with semantic correctness;
8. permit parallel and optimizer variation only where algebraic laws or the declared comparator make it harmless;
9. create replay manifests, output fingerprints, candidate comparisons, and conditional publication evidence; and
10. test determinism by perturbing physical choices, using independent oracles, and diagnosing the smallest divergent keys.

## Core Exposition

### Start with observable equality

Name the output abstraction before discussing engine settings. For a keyed customer balance table, equality may require the same schema, exactly one row per customer, the same decimal amount per key, and the same null meanings; row and file order may be irrelevant. For a ranked recommendation list, position is part of the key and sequence equality matters. For a signed export, identical canonical bytes may be required.

Set equality discards multiplicity. If one run emits an order twice and another once, converting both to a set hides the error. Use multiset equality where duplicate counts matter, keyed-map equality where keys must be unique, ordered equality where position matters, or a domain comparator that exposes all contractual dimensions.

Numerical tolerance is not a generic escape hatch. Define absolute or relative tolerance, units, magnitude behavior near zero, NaN/infinity/signed-zero handling, per-row versus aggregate scope, and cumulative materiality. A tolerance suitable for a visualization may be invalid for a regulatory amount. Record who owns the choice.

Representation equality is stronger than value equality. Canonical bytes may normalize property order, number spelling, string encoding, and row ordering. RFC 8785 defines one JSON canonicalization scheme using constrained JSON values, deterministic property sorting, and specified serialization. Ordinary `sort_keys=True` JSON is a useful local contract when fully specified, but it must not be mislabeled as RFC 8785 unless it meets that RFC.

### Make hidden inputs visible

Write the transformation as a function of its full semantic closure, not only the table named in `FROM`. Reference tables, lookup files, model weights, schema defaults, feature flags, tenant policy, exchange rates, calendars, and correction decisions are inputs. Pin each to an immutable version or content digest.

Ambient process state is input too. Environment variables, locale, collation, default encoding, session time zone, search path, library data files, floating-point mode, and current working directory may alter results. Secrets should never be copied into a replay manifest, but secret-independent endpoint identity, authorization scope, and response artifact can be recorded safely.

An external API called from a row UDF makes availability, response version, server state, and request timing part of the computation. Prefer acquiring external responses into a governed immutable boundary, then transform locally. If live calls are unavoidable, capture request identity, safe response digest/body under policy, version headers, error/retry behavior, and completeness; otherwise faithful replay may be impossible.

The query plan usually need not be identical when relational and arithmetic semantics guarantee the same observable. But engine/adapter changes can alter implicit casts, timestamp parsing, collation, overflow, optimizer treatment of volatile expressions, and approximate aggregates. Pin versions and test upgrades rather than assuming source-level SQL exhaustively defines behavior.

### Separate business time from execution time

Calling the wall clock inside historical logic means a retry tomorrow has a different input. Replace `current_date`, `now()`, file modification time, or process start time with an explicit `as_of`, knowledge cut, or evaluation instant recorded in the manifest. Use one governed value consistently rather than sampling the clock per row.

Some engines stabilize a clock only within a statement or transaction. PostgreSQL classifies functions as `VOLATILE`, `STABLE`, or `IMMUTABLE`; the classification is an optimizer contract, not a general proof of pipeline reproducibility. A transaction-stable timestamp still differs across two transactions. An incorrectly labeled function can yield stale plan-folded values.

Event time is data. Processing time is operational evidence. Ingestion time can support lineage and latency measurement. Do not substitute any of them silently. If “age at report date” is required, compute it from birth/event date and an explicit report date under a named calendar/time-zone rule.

Named civil zones require a time-zone ruleset. The IANA tz database publishes versioned code/data because rules change. Record the zone identifier, tzdb version, local-time ambiguity/nonexistence rule, and precision. Prefer canonical instants for storage while retaining original zone/offset evidence needed by the domain.

### Remove or parameterize side effects

A pure row function can be reasoned about locally: equal declared arguments produce equal return values and no external effects. Reading another table, generating a UUID, consulting a global cache, mutating state, logging values that later affect control flow, or making network calls breaks that simple model.

Move side inputs into explicit joined relations or immutable broadcast artifacts. Pass parameters such as exchange-rate cut and evaluation instant. Derive stable semantic identifiers from governed namespace and business identity where appropriate; do not use random UUIDs when the identifier must remain stable across recomputation.

Not every UDF can be made pure. Tokenization may depend on a pinned model; geocoding may need an external knowledge snapshot; privacy policy may intentionally prohibit retaining a response. State the reproducibility boundary honestly. A deterministic downstream transform cannot reconstruct an expired or deliberately erased upstream artifact.

Database function annotations help optimizers but do not replace review. PostgreSQL documents that `VOLATILE` functions may differ on successive calls, `STABLE` functions remain fixed within one statement snapshot, and `IMMUTABLE` promises the same result forever for the same arguments. Locale, configuration, or table-dependent logic must not be declared immutable merely to enable optimization.

### Define total ordering and winner rules

SQL results without an explicit `ORDER BY` have unspecified row order. Even with `ORDER BY event_time`, ties remain unless every tied row is contract-equivalent or further keys resolve them. Define direction and null placement for every key and end with a stable unique semantic identity when output sequence or “first/last” depends on it.

For winner selection, order by authoritative source revision, event/knowledge precedence as governed, and a deterministic conflict rule. A unique event ID can break representational ties only after equal-precedence conflicting payloads are detected. Picking `min(payload_digest)` makes execution repeatable but invents business authority; usually conflict quarantine is correct.

Window functions need the same care. `row_number() over (partition by account order by timestamp)` is unstable when timestamps tie. `lag`, `lead`, first/last, cumulative frames, and session boundaries can change. Add source transaction position or immutable occurrence identity and specify `ROWS` versus peer-sensitive range semantics.

Ordered aggregates must carry order inside the aggregate where the engine requires it. PostgreSQL notes that order-sensitive aggregates have unspecified input ordering by default; relying on a sorted subquery can fail if outer processing reorders rows. Consult the actual engine contract.

Sorting after an order-sensitive error is too late. If a string aggregation consumed elements in arbitrary order, sorting the final single string cannot recover the desired sequence. Canonicalize at the boundary where order becomes semantic.

### Treat relations, sequences, and files differently

A relation is conceptually unordered. An exported CSV is a byte sequence. A collection-valued column may be an array whose order matters or an encoded set whose order should be canonicalized. State which abstraction exists at every boundary.

Partition and file names are often physical. Repartitioning a relation may change file count, row placement, and object names without changing values. If consumers glob files and infer order or ownership from names, those physical details have become an accidental API. Replace that behavior with a manifest and logical keys, or govern layout as part of the output contract.

For byte-stable exports, define newline convention, encoding/BOM, header, column order, null token, quoting/escaping, decimal and timestamp format, row total order, compression format/settings/version where compressed bytes matter, archive entry order/metadata, and canonical manifest. Byte identity is expensive because every layer participates.

Do not hash a directory walk in incidental filesystem order. Build a manifest sorted by governed relative path, with object length, content digest, schema or role, and hash algorithm. Decide whether timestamps, permissions, storage metadata, and compression are semantic.

### Govern text equality, normalization, and collation

Unicode allows canonically equivalent strings with different code-point sequences. UAX #15 defines NFC, NFD, NFKC, and NFKD. Choose normalization according to domain semantics; compatibility forms can erase distinctions and must not be applied blindly. Preserve raw text when audit or round trip requires it, while deriving a normalized comparison key explicitly.

Normalization is not case folding, accent removal, transliteration, or locale-aware collation. Those are different policies. A customer name, security identifier, SKU, and search token may need different equality rules. Never apply a convenient text cleanup globally and call it canonical truth.

Collation controls equality/order for text and may be provided by an operating system or ICU version. PostgreSQL records collation provider/version information and distinguishes deterministic comparisons from nondeterministic collations that may treat byte-distinct strings as equal. Pin or record the provider, locale, rules, determinism setting, and version; reindex/regroup implications after upgrade require testing.

When canonical bytes matter, use a declared code-point/byte ordering or a versioned canonicalization specification rather than an ambient human collation. Human-friendly presentation can be produced separately from identity ordering.

### Control randomness by identity

Ask whether randomness belongs in the transformation. Cryptographic nonces, privacy noise, randomized experiments, sampling, and model algorithms may require it. If the output is meant to change, record the run-specific randomness identity. If the output must reproduce, pin the generator/algorithm, seed or protected key identity, version, and draw assignment.

A single shared pseudorandom stream couples results to traversal. If record A consumes the first draw in one run and record B consumes it after repartitioning, cohort assignments swap despite the same seed. Sorting globally before drawing can work but may be costly and brittle when records are inserted.

Key-derived randomness computes something like

$$
u(k)=H(\text{algorithm-version}\parallel\text{namespace}\parallel encode(k))
$$

and maps it to a range with a bias-aware method. Each key receives the same value independent of traversal, partition, retry, or neighboring records. Rotate the namespace when a genuinely new experiment is intended. Use HMAC or another approved keyed construction when assignments must not be guessable; never expose secret key material in lineage.

Python's `random` documentation gives bounded reproducibility guarantees for its `random()` sequence with a compatible seeder while warning that most algorithms and seeding functions can change across versions. That is a product-specific contract, not permission to assume every distribution method is forever stable. Record interpreter/library version or use a deliberately versioned algorithm owned by the data contract.

### Make arithmetic semantics deliberate

Binary floating-point cannot exactly represent many decimal fractions. Addition is generally non-associative:

$$
(a+b)+c \ne a+(b+c).
$$

Parallel engines may alter grouping through partitioning, shuffle, retry, or adaptive planning. DuckDB explicitly documents small nondeterministic variations for some multithreaded floating-point aggregates. Spark documents that shuffled element ordering is not guaranteed even when partition membership and partition order are deterministic.

For currency and other fixed-scale domains, use integer minor units or exact decimal with a governed scale, rounding mode, and overflow policy. Decide whether rounding occurs per transaction, group, day, or final report; these are not equivalent.

For scientific floating point, possible strategies include a fixed total input order and fixed reduction tree, compensated/pairwise summation with documented error behavior, reproducible numerical libraries, higher precision, or a domain-approved tolerance. Sorting solely to stabilize sums can be expensive and may still depend on representation/ties. The choice must match accuracy, throughput, and portability needs.

Min/max appear order-insensitive but NaN, signed zero, null policy, and comparator differences can matter. Average combines sum and count; variance algorithms differ in numerical stability. Approximate distinct counts, quantiles, sketches, and machine-learning operations need algorithm/version/merge-order/error contracts rather than an assumption of exact identity.

Overflow is part of determinism and correctness. One engine may raise, another wrap, and another widen. Cast deliberately and test boundary values. Decimal division scale and timestamp precision can also vary across engines/adapters.

### Preserve determinism under partitioning and retry

Physical partitioning should not choose business meaning. A key-based reduce must gather all values for a key or use a mergeable state with stated algebraic laws. If local combiners and global reducers may associate values differently, prove associativity/commutativity for exact types or define the permitted numerical difference.

Speculative and retried execution can deliver the same logical contribution more than once. Stable operation/event identities and idempotent sinks prevent duplicate effects. This is adjacent to, not identical with, deterministic values: a deterministic function can still be appended twice; an idempotent write can consistently publish a nondeterministically chosen winner.

Do not derive semantic IDs from partition number, attempt number, worker hostname, object listing position, or current file count. Those values can appear in operational lineage but should not define the business row. Derive IDs from stable namespace, business identity, governed version, and canonical semantic payload as appropriate.

Spark documents that shuffle element order is not guaranteed. `groupByKey` followed by “first value” is therefore unsafe unless values are contract-equivalent. Use an associative aggregation or a deterministic ordered winner after grouping. Similar reasoning applies across engines even when a small local run happens to retain input order.

### Build canonical output fingerprints

First validate the abstract output: schema, grain, key uniqueness, row multiplicity, nulls, referential constraints, business invariants, and source controls. Then map it to a canonical comparison projection. Exclude physical metadata only deliberately; include every semantic field and its type/encoding.

A robust keyed fingerprint can sort rows by canonical key, encode each field with type and length boundaries, normalize only under declared rules, and hash row records plus schema/version into a Merkle tree or manifest. This supports localized comparison and avoids concatenation ambiguity. Record the hash algorithm and canonicalization version.

One whole-output hash quickly detects a difference but does not locate it. Layer fingerprints by dataset, partition, key range, and row to narrow divergence. Compare counts, sums where meaningful, null distributions, min/max, key movements, and exact divergent records. Do not use weak commutative hashes without analyzing collisions and duplicate cancellation.

An equal digest proves only that the hashed byte sequences are equal assuming the hash's collision resistance. It does not prove the source cut was complete, the code was correct, the canonical projection included every contractual field, or the result was authorized. Bind the digest into a broader evidence record.

### Retain a replay manifest

Give every logical generation a stable identity. Its manifest should include source and reference snapshot/object/log identities; code repository and commit/content digest; compiled query or plan digest where needed; parameters/configuration/feature flags; input/output schemas; engine, adapter, libraries, container, OS/architecture constraints; locale/collation/Unicode/tzdb/calendar; arithmetic/random/canonicalization policies; UDF/model artifacts; secret-independent external-response identities; output comparator; fingerprints; validation; timestamps as evidence; and parent/superseded generation.

Store content-addressed immutable artifacts or durable resolvable versions. A Git commit does not capture untracked generated SQL, a mutable container tag, a database function changed outside the repository, or an expired source snapshot. Inventory the actual closure.

Retention defines the reproducibility horizon. If raw files, table snapshots, reference generations, images, model weights, tzdb packages, or decryption keys expire, record when reproduction becomes partial or impossible. Legal deletion may intentionally remove inputs; audit evidence should then state non-reproducibility rather than retaining prohibited data.

Separate evidence time from business meaning. Run start/end, host, and attempt ID help diagnose execution but should not leak into semantic output unless the contract explicitly includes them.

### Validate by perturbing physical choices

Run the same logical envelope under different input orders, partition counts, worker/thread counts, batch sizes, optimizer settings, file groupings, retry patterns, and where supported engine versions/architectures. Compare with the declared relation. A single difference refutes the claim for that envelope; many equal trials provide bounded empirical evidence, not a universal proof.

Use metamorphic properties. Permuting an unordered input should not change a relation result. Splitting and recombining exact additive groups should agree with a full aggregation. Adding an exact duplicate should leave a deduplicated result unchanged. Normalizing already normalized text should be idempotent. Replaying a candidate should preserve its canonical fingerprint.

Use an independent reference implementation for small fixtures. Differentially compare SQL and dataframe versions, incremental and full results, old and upgraded engines, or parallel and serial execution. Independence matters: two paths sharing the same unstable helper may agree on the same error.

Generate adversarial fixtures: equal timestamps with different IDs; null sort keys; canonical-equivalent Unicode; locale-sensitive letters; ambiguous/nonexistent civil times; decimal half-way rounding; huge and tiny floats; NaN/infinity/signed zero; overflow boundaries; duplicate/conflicting revisions; empty and singleton groups; skew; partition failures; external timeouts; and expired inputs.

On mismatch, retain both manifests and narrow by hierarchical fingerprints to the first divergent key/value and provenance. Do not simply rerun until outputs happen to match. The mismatch is valuable evidence that the envelope, operator, or comparator is incomplete.

### Publish a validated generation conditionally

Write to an isolated candidate identity. Validate its manifest and output against the expected source cut and current trusted parent. Publish by conditional pointer/catalog/metadata transition only if the expected parent is still current. Concurrent runs with different envelopes must not overwrite each other by finish order.

Unknown publication outcomes require lookup by stable operation/generation identity. Do not blindly retry an append or create a new random generation identity. Idempotent publication and deterministic computation reinforce each other but remain separate obligations.

Keep the prior generation through the rollback and evidence horizon. If a new runtime or collation changes results deliberately, classify it as a semantic migration, compare key-level differences, approve the new contract, and publish a new version. Do not relabel changed meaning as harmless nondeterminism.

Expose consumer metadata: generation ID, source/reference cuts, transformation version, as-of time, schema, comparator/canonicalization version, fingerprint, supersession, and known limitations. Consumers can then distinguish same logical answer in a new physical layout from an actual semantic change.

## Definitions and Notation

Let:

- $S_s$ be immutable source state at cut $s$;
- $R_r$ be immutable reference state at cut $r$;
- $v$ identify transformation source and compiled semantics;
- $p$ be explicit parameters, including governed evaluation time;
- $E$ be the semantic environment: runtime, schemas, locale/collation, Unicode/tzdb, arithmetic, randomness, and external-response artifacts;
- $c\in C(E)$ be a permitted physical choice vector: scan order, partitioning, worker schedule, retry, reduction tree, and plan;
- $F_{v,p}(S_s,R_r,E,c)$ be one execution result;
- $O$ project a result to the observable contract;
- $\equiv_Q$ be equivalence under comparator/version $Q$;
- $K_Q$ be canonicalization under specification $Q$; and
- $H_A$ be a cryptographic hash under named algorithm $A$.

Determinism for the declared envelope is

$$
D(S_s,R_r,v,p,E,Q) \iff
\forall c_1,c_2\in C(E),\quad
O(F_{v,p}(S_s,R_r,E,c_1))\equiv_Q
O(F_{v,p}(S_s,R_r,E,c_2)).
$$

This does not compare different source cuts or code versions. If $R$ or $E$ is unnamed and mutable, the premise “same envelope” cannot be established.

Canonicalization is sound for the chosen equivalence if

$$
x\equiv_Q y \Longrightarrow K_Q(x)=K_Q(y).
$$

It is complete for distinguishing nonequivalent values if

$$
K_Q(x)=K_Q(y) \Longrightarrow x\equiv_Q y.
$$

Many ad hoc canonicalizers are not complete because they omit fields, erase duplicates, coerce types, or round values. Hash comparison adds the collision-resistance assumption:

$$
fingerprint(x)=H_A(encode(Q)\parallel K_Q(x)).
$$

For a partitioned reduction of values $x_1,\ldots,x_n$ with operator $\oplus$, arbitrary grouping/order is harmless for exact equality when $\oplus$ is associative and commutative over all reachable values and has compatible identity/error behavior. Floating-point addition violates exact associativity; integer addition may overflow; decimal operations may round. Algebraic claims require the actual representation and domain.

For stable key-derived assignment into $m$ buckets, define

$$
b(k)=map_m(H_A(encode(namespace,k))),
$$

where key encoding is injective over the key domain and `map` handles modulo bias according to the application. The assignment is traversal-independent, not magically unbiased, secure, or permanent without the other premises.

A reproducibility manifest $M$ is sufficient only relative to a reconstruction procedure $P_M$ and retention state. The empirical claim after reproduction is

$$
O(P_M(M))\equiv_Q O_{published}.
$$

An equal trial supports this instance. It does not prove all permitted executions deterministic. A differing trial refutes the claimed comparator or exposes that the reconstructed envelope differs.

## Mechanisms, Invariants, or Proof Structure

Use the following assurance argument.

1. **Contract identity.** Prove that output grain, keys, multiplicity, order, schema, numerical rules, and comparator are named and owner-approved. Evidence includes contract version and fixtures.
2. **Input closure.** Prove that every result-affecting source, reference, parameter, clock, random/external value, schema, and semantic environment component is eliminated, immutable, or identified. Evidence includes manifests and dependency inventory.
3. **Operator determinism.** For filters, maps, joins, winners, windows, aggregations, and serialization, prove physical choices cannot change the observation, or constrain/record those choices. Evidence includes algebra, engine contracts, and adversarial tests.
4. **Canonical comparison.** Prove the comparison projection retains all contractual information and maps equivalent outputs consistently. Evidence includes schema-aware canonicalization tests and versioned encoding.
5. **Perturbation evidence.** Execute the same envelope across deliberately different orders, partitions, concurrency, retries, and relevant runtime variants. Evidence includes manifests, fingerprints, and localized diffs.
6. **Reconstruction evidence.** Rebuild from retained manifest artifacts in an isolated candidate and compare under the same $Q$. Evidence includes artifact availability and reproduction receipts.
7. **Publication integrity.** Prove the validated candidate, not another generation, became current conditionally on the expected parent. Evidence includes generation IDs and publication receipts.

The central proof obligation for a relational map/filter over pure functions is straightforward: each input row yields the same derived row, and unordered collection equivalence ignores traversal. Joins add cardinality and matching semantics. If each side is the same keyed multiset, equality/comparison is stable, and output multiplicity is defined, join results are the same multiset; output sequence still requires total ordering.

Winner selection is deterministic only if precedence is a total order over acceptable candidates or ties are contract-equivalent. Equal authoritative rank with different payload is not a harmless tie. Reject/quarantine it or resolve through domain authority outside the physical run.

For exact sums in bounded integer/minor units, partition-local sums combined by exact addition agree if no intermediate overflow occurs. Record range analysis or use checked/wider arithmetic. For decimal, include scale and rounding placement. For floating point, do not reuse this proof because associativity fails.

Canonicalization proves stable representation only after value equality. If two source runs choose different rows, sorting keys and property names merely gives stable encodings of two wrong/different answers. Validate semantics before representation.

Evidence is layered:

- **static evidence:** dependency inventory, pure-function review, explicit ordering, type/range analysis, canonicalization specification;
- **finite model evidence:** exhaustive permutations and edge cases for small fixtures;
- **differential evidence:** independent implementation, full/incremental, serial/parallel, old/new runtime comparison;
- **operational evidence:** real generation manifests, source controls, fingerprints, conditional publication receipts, drift alerts;
- **domain evidence:** owner-approved equality/tolerance, rounding, time, conflict, and retention policies.

Do not upgrade finite testing into proof of all data/engine schedules. Do not weaken a domain contract merely to make two runs compare equal.

The following executable model illustrates a narrow deterministic transformation contract. It uses the Python standard library, decimal strings, an explicit customer comparison key produced by a governed NFC boundary, stable revision selection, key-derived cohorts, a fixed `as_of`, sorted rows, and a documented tuple encoding. It is a teaching model, not an RFC 8785 implementation, distributed-engine proof, security review, or universal text/financial policy.

<!-- bijux-verify: {"id":"deterministic-transformation-reference-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"rows=(('Alice', '5.00', 2), ('Café', '14.30', 3))\ntotal=19.30\ndigest=098d41df901c006351ce499b49b56449ba84fb659f39a2cc132ad17308397020\npermutations_checked=120\nall_permutations_stable=True\nduplicate_replay_stable=True\nconflict_detected=True\n","stderr":""}} -->
```python
from decimal import Decimal
from hashlib import sha256
from itertools import permutations


def canonical_record(record):
    return {
        "amount": str(Decimal(record["amount"]).quantize(Decimal("0.01"))),
        "customer_key": record["customer_key"],
        "event_id": record["event_id"],
        "revision": int(record["revision"]),
    }


def payload_digest(record):
    row = canonical_record(record)
    payload = repr(
        (row["event_id"], row["revision"], row["customer_key"], row["amount"])
    ).encode("utf-8")
    return sha256(payload).hexdigest()


def cohort(customer, namespace="experiment-2026-09"):
    material = f"{namespace}\0{customer}".encode("utf-8")
    return int.from_bytes(sha256(material).digest()[:8], "big") % 4


def transform(deliveries, as_of="2026-08-31"):
    versions = {}
    for raw in deliveries:
        row = canonical_record(raw)
        versions.setdefault(row["event_id"], []).append(row)

    winners = []
    for event_id, candidates in versions.items():
        revision = max(row["revision"] for row in candidates)
        tied = [row for row in candidates if row["revision"] == revision]
        digests = {payload_digest(row) for row in tied}
        if len(digests) != 1:
            raise ValueError(f"conflicting revision for {event_id}")
        winners.append(tied[0])

    totals = {}
    for row in winners:
        customer = row["customer_key"]
        totals[customer] = totals.get(customer, Decimal("0.00")) + Decimal(
            row["amount"]
        )

    rows = tuple(
        (customer, format(totals[customer], ".2f"), cohort(customer))
        for customer in sorted(totals)
    )
    return (as_of, rows)


deliveries = (
    {"event_id": "e1", "revision": 1, "customer_raw": "Cafe\u0301", "customer_key": "Café", "amount": "10.10"},
    {"event_id": "e2", "revision": 1, "customer_raw": "Café", "customer_key": "Café", "amount": "2.20"},
    {"event_id": "e2", "revision": 2, "customer_raw": "Café", "customer_key": "Café", "amount": "4.20"},
    {"event_id": "e3", "revision": 1, "customer_raw": "Alice", "customer_key": "Alice", "amount": "5.00"},
    {"event_id": "e3", "revision": 1, "customer_raw": "Alice", "customer_key": "Alice", "amount": "5.00"},
)

baseline = transform(deliveries)
all_permutations_stable = all(transform(order) == baseline for order in permutations(deliveries))

try:
    transform(deliveries + ({
        "event_id": "e2",
        "revision": 2,
        "customer_raw": "Café",
        "customer_key": "Café",
        "amount": "7.00",
    },))
    conflict_detected = False
except ValueError:
    conflict_detected = True

print(f"rows={baseline[1]}")
print(f"total={sum(Decimal(row[1]) for row in baseline[1]):.2f}")
print(f"digest={sha256(repr(baseline).encode('utf-8')).hexdigest()}")
print(f"permutations_checked={len(list(permutations(deliveries)))}")
print(f"all_permutations_stable={all_permutations_stable}")
print(f"duplicate_replay_stable={transform(deliveries + deliveries) == baseline}")
print(f"conflict_detected={conflict_detected}")
```

The input has 120 traversal permutations because it has five deliveries, even though two are equal dictionaries. Every traversal selects `e2` revision 2, deduplicates equal `e3` revision 1, uses one explicit customer comparison key for both café spellings, and produces exact cents. The customer sort and canonical tuple encoding stabilize presentation. The cohort is derived per customer, so traversal does not consume or reassign a shared stream.

The conflict fixture adds another `e2` revision 2 with a different amount. Choosing the lower digest would be mechanically repeatable but semantically unjustified; the model rejects it. This demonstrates the difference between deterministic conflict detection and inventing deterministic authority.

The model's claim is intentionally bounded. Python/Unicode/decimal/JSON/hash behavior and the custom encoding are part of its envelope. It does not model source snapshot consistency, distributed joins, floating-point aggregates, tzdb, collation upgrades, external calls, cryptographic secret management, or atomic publication. Production evidence must cover those separately.

## Alternatives and Trade-Offs

**Semantic equality versus byte identity.** Keyed relation equality tolerates physical layout and serialization changes, improving portability and parallelism. Byte identity supports content addressing and signing but governs every encoding detail. Use the weakest comparator that fully protects consumers, not a weaker one chosen merely because it passes.

**Exact decimal/integer versus floating point.** Minor units and fixed decimal make many financial reductions exact but require scale, range, division, and rounding policy. Floating point offers wide dynamic range and hardware acceleration but needs stability/error semantics. Domain meaning decides.

**Global sort versus algebraic aggregation.** A total global order can stabilize order-sensitive logic but costs shuffle, memory, and latency. Associative/commutative exact operators scale better. Redesign an operator to be order-independent when the domain permits; otherwise pay for the required sequence.

**Fixed partitioning versus partition-independent design.** Pinning partition count/reduction tree can reproduce one environment but restrict elasticity and may still vary across failures or upgrades. Partition-independent algebra and keyed randomness provide a stronger result contract. Pin physical structure only when it is genuinely semantic or no practical order-independent method exists.

**Shared seeded stream versus key-derived assignment.** A shared stream is simple for serial simulations and preserves correlations defined by draw sequence. It couples distributed results to traversal. Key-derived assignment is stable under insertion and repartitioning but changes the statistical construction and needs careful hashing/range mapping.

**Current environment versus hermetic environment.** Reusing current libraries and reference data reduces artifact retention and security burden but reproduces only current-restated semantics. Hermetic images and immutable snapshots strengthen historical reproduction but cost storage, patch governance, and legal handling. Record the intended horizon.

**Engine-specific guarantees versus portable subset.** Using native collation, approximate functions, or optimizer features can improve functionality/performance. A portable explicit subset may be easier to reproduce across engines but can sacrifice capability. If engine behavior is part of the contract, name/version it and test upgrades.

**Normalize on write versus compare-time normalization.** Normalizing at ingestion gives stable keys and simpler joins but may erase original evidence or apply one policy to incompatible domains. Retaining raw plus a versioned derived normalized key supports audit and policy migration at added storage/complexity.

**Reject conflict versus deterministic arbitrary winner.** Rejecting equal-precedence disagreement preserves authority semantics but delays output. Picking a hash-minimum winner keeps pipelines moving but creates an unexplained business fact. Only an owner-approved tie policy can justify the latter.

**Record live external responses versus isolate acquisition.** Recording can enable replay but may retain sensitive or licensed data and still suffers partial-call consistency. A governed acquisition dataset creates a cleaner boundary. Some privacy/legal settings intentionally limit replay; state that limitation.

**Strict replay versus migration comparison.** Historical replay pins the old envelope and expects old contract equivalence. Migration recomputes under a new envelope and expects reviewed differences. Mixing them yields neither faithful reproduction nor a controlled migration.

## Failure Modes and Misconceptions

1. **“The SQL text is identical, so the output is deterministic.”** Mutable tables, session settings, functions, plans, engine versions, and external UDF state remain inputs.
2. **“A seed solves randomness.”** A seed without pinned algorithm and key/draw assignment does not survive traversal, partition, retry, or version changes.
3. **“`ORDER BY timestamp` is deterministic.”** Equal timestamps remain peers; add stable authoritative tie-breakers and explicit null order.
4. **“The database usually returns insertion order.”** PostgreSQL documents unspecified order without explicit sorting; physical plans and storage change.
5. **“Sorting the final output repairs nondeterminism.”** It only repairs representational order, not a different winner, ordered aggregate, window result, or float reduction.
6. **“Equal totals mean equal output.”** Misattributed groups, offsetting errors, duplicates, and missing rows can preserve totals.
7. **“Hash equality proves correctness.”** It proves equality of the hashed encoding under a collision assumption, not completeness, semantics, or authorization.
8. **“JSON with sorted keys is universally canonical.”** Number/string rules, Unicode, arrays, schema, and implementation details matter; use a named specification.
9. **“Unicode text that looks equal has equal bytes.”** Canonically equivalent sequences can differ; select a domain-appropriate normalization/equality policy.
10. **“Collation is presentation only.”** It can affect equality, uniqueness, grouping, joins, ordering, and indexes.
11. **“UTC solves all time determinism.”** Converting local civil input to an instant still requires zone rules and ambiguity policy; calendar meaning may remain local.
12. **“Floating-point addition is associative enough.”** The acceptable error is domain-specific, and varying trees can change low bits or more under cancellation.
13. **“Single-threaded execution proves the parallel result.”** It provides an oracle candidate; parallel operators still need algebraic/test evidence.
14. **“Pinning thread count is a semantic proof.”** Input splits, retries, optimizer plans, hardware, and library versions can still change order/behavior.
15. **“Idempotent writes make values deterministic.”** They prevent repeated logical effects; they do not choose a stable value.
16. **“A deterministic function guarantees a reproducible pipeline.”** Missing snapshots, dependencies, configuration, or retention can prevent reconstruction.
17. **“An arbitrary stable tie-breaker is valid.”** It can turn inconsistent evidence into a repeatable but unauthorized answer.
18. **“Reproducibility requires identical traces.”** Result equivalence may allow different workers, schedules, plans, and file layouts.
19. **“Every difference is a bug.”** A deliberate code/reference migration should differ; classify and approve it rather than forcing equality.
20. **“Repeated success proves determinism.”** Trials are bounded evidence. A counterexample refutes the envelope claim; universal assurance needs reasoning plus coverage.

## Worked Examples

### Example 1

Two updates for account A share `event_time=12:00` but have source revisions 8 and 9. `row_number` ordered only by event time can choose either. Order by authoritative revision descending and reject equal revision with different canonical payload. Arrival time is lineage, not authority.

### Example 2

Two warehouse runs produce the same 1,000 keyed rows in different physical orders. They are equal as keyed relations. A CSV consumer hashes bytes, so the export contract adds total row order, column order, encoding, null/decimal/timestamp formatting, newline, and canonical manifest.

### Example 3

Outputs `[x,y]` and `[x,x,y]` have equal sets but unequal multisets. If the grain promises one row per event, both uniqueness validation and multiset/keyed comparison are required. A fingerprint that omits multiplicity can hide this failure just as readily as an in-memory set comparison.

### Example 4

A historical customer model computes `days_since_signup = current_date - signup_date`. A retry next day changes every row. Pass `report_as_of=2026-08-31` as a recorded parameter and use a named date/calendar policy.

### Example 5

With seed 7, serial traversal assigns first draw to A and second to B. Repartitioning traverses B first, swapping assignments. Hash the pinned experiment namespace plus stable subject key, or precompute a governed assignment table.

### Example 6

For values $10^{16},1,-10^{16}$, left-to-right binary floating-point evaluation can yield 0 while grouping the extremes first yields 1. If the domain needs the exact unit, use exact decimal/integer or a governed stable method; a display rounding policy does not erase the reasoning obligation.

### Example 7

`Café` may use U+00E9 or `e` plus U+0301. Byte grouping yields two customers. A contract may retain both raw values while grouping on NFC-normalized key. It must not silently add case/accent folding unless the domain permits it.

### Example 8

Two status events share millisecond timestamp but have distinct source log positions. `lag(status)` ordered only by timestamp varies. Add source epoch/position and occurrence ID; if positions conflict, quarantine rather than sort by arbitrary payload.

### Example 9

Source facts and code are pinned, but country-to-region mapping is read from `region_current`. A rerun after a mapping correction changes history. Pin a reference snapshot and name whether the goal is original replay or current-restated output.

### Example 10

Amounts are validated integer cents with a proven bounded total. Partition-local maps sum by account; global maps merge by exact checked addition. Because addition is associative/commutative within the bound, partition order does not change account totals. Output row order remains a separate concern. The output fingerprint includes schema, key, amount, and currency; an engine migration that changes decimal or collation semantics is compared and approved as a new contract rather than mislabeled as replay.

## Cross-Program Connections

- **Programming Languages & Semantics:** determinism is a property of observations under an explicit semantic model; pure functions and referential transparency reduce hidden input.
- **Concurrent & Parallel Programming:** schedules and reduction trees may vary while results remain equivalent; race freedom alone does not guarantee one result.
- **Data Structures Engineering:** maps, sets, heaps, and hash tables expose different ordering guarantees, and stable canonical traversal requires explicit structure or sorting.
- **Algorithm Engineering:** associative decompositions, stable sorting, numerical analysis, hashing, and randomized algorithms determine scalable reproducibility.
- **Database Systems:** isolation snapshots, SQL ordering, function volatility, collation, types, query plans, and transaction publication shape the envelope.
- **Testing & Quality Engineering:** differential, metamorphic, property-based, adversarial, and perturbation testing reveal incomplete determinism assumptions.
- **Software Delivery & Reliability Engineering:** immutable builds, locked dependencies, provenance, deployment identity, rollback, and artifact retention support replay.
- **API & Service Engineering:** idempotency keys, versioned external responses, request canonicalization, and conditional writes govern effectful boundaries.
- **Platform Engineering:** runtime images, architecture, locale/tzdb packages, scheduling, object manifests, and secret-independent environment identity must be observable.
- **Security Engineering:** canonicalization errors affect signatures; predictable pseudorandom assignments can leak; replay evidence must respect secrets, privacy, deletion, and access control.
- **Systems Engineering:** assurance cases distinguish assumptions, invariants, finite evidence, residual uncertainty, and controlled semantic change.

## References

1. PostgreSQL Global Development Group, [Sorting Rows (`ORDER BY`)](https://www.postgresql.org/docs/current/queries-order.html). Documents that row order is unspecified without explicit sorting and how later expressions break earlier ties. Accessed 2026-09-02.
2. PostgreSQL Global Development Group, [Function Volatility Categories](https://www.postgresql.org/docs/current/xfunc-volatility.html). Defines `VOLATILE`, `STABLE`, and `IMMUTABLE` optimizer promises and clock/random examples. Accessed 2026-09-02.
3. PostgreSQL Global Development Group, [`CREATE COLLATION`](https://www.postgresql.org/docs/current/sql-createcollation.html). Documents deterministic versus nondeterministic comparisons, providers, locale/rules, and collation version metadata. Accessed 2026-09-02.
4. Apache Spark, [RDD Programming Guide: Shuffle operations](https://spark.apache.org/docs/latest/rdd-programming-guide.html#shuffle-operations). Documents that shuffled element ordering is not guaranteed even where partition membership/order is deterministic. Accessed 2026-09-02.
5. DuckDB Foundation, [Non-Deterministic Behavior](https://duckdb.org/docs/current/operations_manual/non-deterministic_behavior). Documents SQL set-order variation, platform-sensitive collection order, multithreaded floating-point variation, and scoped workarounds. Accessed 2026-09-02.
6. A. Rundgren, B. Jordan, and S. Erdtman, [RFC 8785: JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785.html), June 2020. Defines a constrained deterministic JSON representation for repeatable cryptographic operations. Accessed 2026-09-02.
7. Unicode Consortium, [Unicode Standard Annex #15: Unicode Normalization Forms](https://www.unicode.org/reports/tr15/). Defines canonical/compatibility equivalence, NFC/NFD/NFKC/NFKD, conformance, and stability boundaries. Accessed 2026-09-02.
8. Internet Assigned Numbers Authority, [Theory and Pragmatics of the `tz` Code and Data](https://data.iana.org/time-zones/theory.html). Describes versioned time-zone interfaces and the changing complexity of civil-time rules. Accessed 2026-09-02.
9. Python Software Foundation, [`random` — Notes on Reproducibility](https://docs.python.org/3/library/random.html#notes-on-reproducibility). States bounded sequence guarantees and version-change limits for Python's pseudorandom facilities. Accessed 2026-09-02.
10. Apache Iceberg, [Spark Queries: Time Travel](https://iceberg.apache.org/docs/latest/spark-queries/#time-travel). Documents snapshot/tag/branch/timestamp selection for versioned table reads and related schema behavior. Accessed 2026-09-02.

## Exercises

### Exercise 1

A source contains values $[10^{16},1,-10^{16}]$ as binary floats. Compute `((10^16 + 1) + -10^16)` and `((10^16 + -10^16) + 1)` in ordinary double precision. Explain why a distributed sum may vary and give two domain-dependent remedies.

### Exercise 2

A model chooses the latest status using `ORDER BY event_time DESC`. Rows `(id=a,time=12:00,revision=4,status=open)` and `(id=b,time=12:00,revision=5,status=closed)` exist for one order. Repair the winner contract and state how equal revision with different payload should behave.

### Exercise 3

Experiment assignment uses a shared generator seeded with 42 while subjects are traversed by partition. Explain why the seed is insufficient. Design a traversal-independent assignment for subject key `tenant_id || user_id`, including the metadata that must be versioned and one security caveat.

### Exercise 4

Two outputs contain the same keyed decimal rows but different file counts and row order. Define (a) a semantic comparator for a warehouse table and (b) a byte-identity export contract. Explain why hashing each directory directly is insufficient.

### Exercise 5

Design a determinism test matrix for a daily transformation that joins pinned orders to a country-region mapping, normalizes customer names, computes decimal revenue and an approximate quantile, and emits JSON. Include hidden-input controls, physical perturbations, edge fixtures, comparators, diagnostics, and publication evidence.

## Answers to the Exercises

### Answer 1

In common IEEE binary64 evaluation, `10^16 + 1` rounds to `10^16`, then adding `-10^16` gives 0. Grouping `10^16 + -10^16` gives 0, then adding 1 gives 1. A distributed reduction may choose either grouping as partitions/retries/plans change. For exact financial units, use checked integer minor units or fixed decimal with governed scale/rounding. For scientific values, use a fixed/stable reduction or compensated/reproducible method and an owner-approved error comparator. The remedy follows domain requirements rather than display formatting.

### Answer 2

Use authoritative revision as primary precedence, with event time only where the domain says it orders versions, and a stable occurrence/assertion ID for representational ties. Here revision 5 wins and status is `closed`. Before choosing, group candidates at maximal authority/revision and compare canonical semantic payloads. Equal revision with different payload is a source conflict: quarantine/fail closed or invoke an explicit owner-approved authority rule. Sorting by ID or digest would be deterministic but would invent meaning.

### Answer 3

A shared seed determines a stream, but partition traversal determines which subject consumes each draw; retries or new subjects can shift assignments. Define `u = HMAC-SHA-256(secret_key, versioned_namespace || length-delimited tenant_id || length-delimited user_id)` and map enough bits to the desired bucket with rejection sampling if exact uniformity matters. Version the algorithm, namespace/experiment, key encoding/normalization, bucket mapping, population eligibility, and secret-key identifier (not the secret). Caveat: an unkeyed public hash can make assignments predictable, while exposed secret material compromises isolation; approved cryptographic design and key management are required.

### Answer 4

For the warehouse table, require the same schema/contract version, unique keys, row multiset or keyed-map equality across every semantic field, exact decimal values, and declared null/text/time semantics; ignore file count/order. For byte identity, additionally define total row order, columns, encoding, Unicode policy, number/time/null formats, escaping, newline, compression/archive metadata if applicable, and a canonical manifest. A directory walk can vary in listing order and may hash names/metadata inconsistently; it also does not prove the included projection is complete. Sort a governed manifest and hash explicit typed content identities.

### Answer 5

Pin order and region snapshots, transformation/compiled query, schemas, parameters/`as_of`, Unicode policy/version, decimal scale/rounding, quantile algorithm/version/error contract, JSON canonicalization, engine/runtime, locale/collation, tzdb if time conversion occurs, and external artifacts. Vary input order, file grouping, partition/thread counts, join plan, retries, batch size, and relevant engine versions. Include duplicate/conflicting IDs, equal timestamps, nulls, composed/decomposed text, locale-sensitive strings, decimal rounding/overflow boundaries, empty/skewed groups, and quantile edge distributions. Compare exact keyed decimal/name/region results, sequence only if promised, JSON canonical bytes if required, and quantile values under a specified rank/value error rule. Use hierarchical fingerprints and key-level provenance to diagnose divergence, compare to a small independent reference, and retain both run manifests. Publish only the validated candidate through a conditional generation transition tied to the expected prior and record its source cuts, comparator, fingerprints, validation, and receipt.
