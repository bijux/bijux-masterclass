---
module_id: DE-018
program: Data Engineering
level: 1
module_number: 18
title: Data Vault Foundations
status: complete
last_verified: 2026-09-02
---

# Data Vault Foundations

## One-Page Review

### Governing question

When does an audit-oriented integration warehouse benefit from separating durable business identities, observed relationships and source-specific descriptive history—and which business-key, time, provenance, hashing, loading and delivery rules make that separation trustworthy?

### Essential definitions

- A **business key** is the stable domain identifier used by business processes to distinguish an instance, with scope and canonicalization explicitly governed.
- A **hub** records the unique business keys for one business concept plus technical load/provenance metadata; it does not hold descriptive payload.
- A **link** records a unique association among two or more hubs, or a deliberately modeled transaction/relationship occurrence, plus load/provenance metadata.
- A **satellite** records descriptive or contextual payload history for one hub or link parent, normally with load time, record source and change-detection metadata.
- The **Raw Vault** preserves source-oriented, auditable history while applying only structural or hard business rules needed to load safely.
- The **Business Vault** derives conformed, calculated or policy-driven interpretations from Raw Vault evidence under versioned soft business rules.
- An **information mart** reshapes vault content for consumer questions, often into dimensional, wide, aggregate or feature models.
- **Load date/time** records when the warehouse accepted a row. **Effective time** records when the source/domain says the represented state or relationship applied.
- A **hash key** is a deterministic surrogate derived from a canonical business-key tuple; a **hashdiff** fingerprints a canonical satellite payload for change detection.
- A **point-in-time (PIT) table** and a **bridge** are query-assistance structures that pre-resolve satellite versions or relationship paths for selected as-of instants.

### Central model, mechanism, or theorem

For a versioned canonical encoder $C_v$ and digest function $H$, derive a hub key

$$
HK=H(C_v(scope,business\_key)).
$$

Determinism gives equal keys for equal canonical inputs; it does not make $H$ collision-free or prove that two sources use the same business meaning. Preserve the canonical business key, normalization version and record source, and test collisions.

For satellite rows of one parent/source ordered deterministically by effective and load evidence, let $q_i=H(C_v(payload_i))$. A run-compressed history retains row $i$ when $i=1$ or $q_i\neq q_{i-1}$. This removes unchanged consecutive observations while preserving every observed payload transition. Out-of-order arrival requires rebuilding or inserting into the correct timeline; comparison only with the current latest row is insufficient.

### Critical invariants

- Each hub represents one business concept at one explicitly scoped business-key grain.
- Each link declares its participating roles and unique relationship/transaction grain.
- Each satellite has exactly one parent grain, source/provenance contract and deterministic ordering key.
- Business key and payload canonicalization are versioned and identical across parallel loaders.
- Hash collisions are detected or made operationally negligible under a documented algorithm and verification policy.
- Load time, effective time, source sequence and batch/run identity remain distinct.
- Raw Vault evidence is insert-oriented and traceable to immutable landing/staging inputs; corrections never erase unexplained history.
- Replays do not create duplicate hubs, links or satellite states.
- Raw source capture and Business Vault rules are separated so changing policy does not rewrite what sources supplied.
- Marts, PITs and bridges are rebuildable derivatives with declared as-of grain and freshness.

### Common failures

Choosing hubs from source table names; merging keys that merely look alike; omitting tenant/source scope; hashing inconsistent types, whitespace, case, nulls or column order; treating hashes as collision-proof; putting mutable descriptions in hubs; putting relationship effectivity directly in an immutable link without a temporal structure; mixing sources with incompatible satellite payload semantics; using load time as business effective time; loading only the latest extract and losing deletions; comparing a late row only with the latest satellite state; updating Raw Vault rows silently; applying volatile business rules during raw ingestion; exposing hubs/links/satellites directly as a friendly mart; and adopting hundreds of patterned tables without metadata automation or a measured need.

### Compact example

Five staged customer observations contain one exact delivery retry and one unchanged later payload. Two unique business keys produce two hub rows. Source-specific satellite change detection retains `bronze` then `gold` for customer `C001` and `silver` for `C002`, producing three satellite states and suppressing two redundant inputs. Replaying the same stage yields identical keys and rows because canonicalization, ordering and anti-duplication rules are fixed.

### Connections

[DE-011](011-grain-and-the-meaning-of-a-row.md) defines row propositions, [DE-014](014-slowly-changing-dimensions.md) distinguishes effective and system history, and [DE-017](017-wide-tables-and-denormalized-models.md) explains why consumer read models differ from integration storage. Planned DE-019 develops metric definitions and semantic consistency and appears in the [Data Engineering roadmap](../ROADMAP.md). Vault loading connects to [Database Engineering](../../18-database-engineering/ROADMAP.md), scalable history to [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md), and metadata automation to [Platform Engineering](../../29-platform-engineering/ROADMAP.md).

## Governing Question

Can an engineer trace any delivered metric row back through a versioned business rule to the exact source observations, while adding a new source, relationship or attribute without rewriting unrelated integrated history?

Data Vault addresses a specific problem: integrating changing, multi-source enterprise data with strong historical traceability. It decomposes identity, association and descriptive context so each can arrive and evolve independently. That structure favors auditable loading and extension; it is not optimized by itself for a dashboard author's shortest query.

The [Data Vault Alliance introduction](https://datavaultalliance.com/engineering/data-vault-2-0-an-introduction/) describes hubs for business keys, links for relationships/transactions and satellites for descriptive attributes, with dimensional delivery layered above. Google's [Data Vault white paper](https://services.google.com/fh/files/misc/google-cloud-data-vault_b.pdf) similarly separates staging, Raw Vault, Business Vault and information marts and emphasizes scalable ingestion versus evolving business interpretation.

The governing decision is therefore architectural, not merely a choice of table prefixes. A team must need the audit, integration and change-isolation properties enough to accept more relations, joins, metadata and automation. A small stable source feeding one report may be better served by a dimensional model. A vault earns its cost when source diversity, historical lineage and continual structural change are first-class requirements.

## Why This Matters

Warehouses fail in two opposite ways. Some transform source data immediately into today's business definitions, losing the evidence needed when definitions change. Others preserve raw files but provide no durable integrated structure, forcing every consumer to rediscover keys, relationships and change history.

Data Vault separates these concerns. Raw Vault structures retain where a business key, relationship or payload came from and when it was loaded. Business Vault structures can apply new rules without pretending those rules were source facts. Marts can then optimize for business questions.

The separation also localizes change. Adding a new descriptive feed can create a satellite without altering the hub identity. Adding a relationship can create a link without widening unrelated tables. Parallel loads become possible when keys are derived consistently from staged business keys.

But pattern names alone do not create auditability. An unstable business key, ambiguous source mapping, inconsistent hash encoding or latest-only satellite destroys the promised history. Table proliferation without automation makes even small changes slow. Raw Vault queries can be complex and expensive if PIT, bridge and delivery layers are neglected.

The practical objective is a reproducible chain from immutable source capture to governed integration to consumer model, with every layer owning a different kind of decision.

## Prerequisites and Retrieval

Retrieve the business concepts and vocabulary; candidate business keys and their domain owners; key stability, reuse and scope; tenant/legal-entity rules; source-system identifiers; cross-source key equivalence evidence; source primary/foreign keys; relationship roles and cardinalities; transaction identities; descriptive attributes and change rates; multi-valued attributes; source effective times; extract/arrival/load times; source sequence; CDC operation and deletion behavior; snapshot coverage; record-source granularity; immutable landing evidence; replay horizon; late/out-of-order distribution; correction rules; batch/run identity; data types, collations, Unicode normalization, whitespace/case rules, null/empty distinctions, decimal/timestamp formats; hash algorithm and output type; canonical component order; collision policy; hub/link/satellite grains; satellite splitting criteria; Raw/Business Vault boundary; hard and soft rules; required PIT/as-of dates; bridge paths; mart requirements; query workload; metadata registry; code generation; deployment dependencies; row/key/control totals; access classification; retention/deletion obligations; expected source/schema change; recovery point; backfill strategy; and ownership for every modeled object.

Distinguish business key from source surrogate and warehouse hash key; identity from description; entity from source table; relationship identity from relationship status/effectivity; relationship from transaction occurrence; raw observation from business correction; record source from business origin; load time from effective time and processing time; first-seen time from latest observation; hash key from hashdiff; deterministic equality from collision-free uniqueness; null from empty string and missing field; single-active history from coexisting multi-active values; source deletion from snapshot absence; link existence from active relationship; hard structural rules from soft interpretive rules; Raw Vault from landing/PSA; Business Vault from information mart; audit insert-only behavior from immutable storage claims; PIT from a source fact; and modeling methodology from one automation tool's macros.

Before schema work, build adversarial examples. Include two tenants sharing `C001`, two sources using different keys for the same customer, one source reusing a key, composite keys containing delimiters/nulls, Unicode/case differences, identical payload retries, A→B→A satellite changes, two payloads at one timestamp, out-of-order effective dates, late first-seen relationships, deleted snapshot rows, simultaneous phone numbers, corrected business rules and a hash-collision test fixture. Write expected hub, link, satellite, status, PIT and mart rows first.

## Learning Objectives

After completing this module, you should be able to:

1. decide when Data Vault is appropriate for an integration warehouse;
2. identify valid business concepts, keys, relationship roles and satellite grains;
3. separate hubs, links and satellites without losing source semantics;
4. distinguish load/system chronology from business-effective chronology;
5. design deterministic hash keys and hashdiffs with collision controls;
6. load raw structures idempotently under replay, retries and late data;
7. handle deletions, effectivity, multi-active attributes and corrections;
8. separate Raw Vault evidence, Business Vault rules and information marts;
9. use PIT/bridge assistance without mistaking derivatives for truth; and
10. automate, test, observe and evolve a vault as a governed product.

## Core Exposition

### Decide whether a vault fits

Strong candidates have many changing sources, long historical/audit horizons, evolving business rules and a need to integrate incrementally. The team should also be capable of metadata-driven automation and disciplined delivery-layer design.

A vault is weaker when source structure is stable, integration scope is small, latency demands require direct serving, or the team expects analysts to query raw hubs/links/satellites without curated outputs.

Compare alternatives against concrete change and audit scenarios rather than selecting a methodology by fashion.

### Separate architecture from table patterns

Data Vault is more than three table shapes. It includes an ingestion/staging path, Raw Vault, Business Vault, information delivery and an implementation methodology.

Hubs, links and satellites provide structural decomposition. Layer boundaries decide which transformations are evidence-preserving versus interpretive. Automation and testing make the many regular structures operable.

Copying naming conventions without those boundaries yields patterned tables, not a trustworthy vault.

### Identify business concepts before hubs

A hub represents something the business identifies durably: Customer, Account, Product, Order or Contract. A source table is not automatically a business concept; one table may contain several concepts, and several tables may describe one.

Use business processes and vocabulary to find candidate keys. Verify that the identifier remains stable when descriptive attributes change.

Do not create a hub for every code. Static country or status codes may be reference data or satellite attributes depending on analytical meaning.

### Define business-key scope

`C001` may be unique only inside tenant, region or source system. The canonical key tuple must include every scope component required for identity.

If two sources share an enterprise business key with genuinely identical meaning, they can feed one hub. If equality is uncertain, keep identities separate and model a governed same-as/equivalence assertion later.

Merging keys based on formatting or name similarity destroys auditability by inventing identity at ingestion.

### Model the hub grain

A hub has one row per canonical business-key tuple for one concept. Typical technical fields include the hash/surrogate key, retained business key components, first load timestamp and first record source.

The [AutomateDV hub documentation](https://automate-dv.readthedocs.io/en/latest/tutorial/tut_hubs/) illustrates a hub with primary/hash key, natural/business key, load timestamp and record source, including multiple source feeds when key meaning is truly identical.

Keep descriptive attributes, current status and source-specific labels out of the hub; their changes should not alter identity.

### Load hubs idempotently

Canonicalize staged key components, reject invalid required keys, derive the deterministic key, deduplicate the batch and insert only unseen keys.

Concurrent loaders must use unique enforcement, set-based anti-join under a safe transaction, or conflict-tolerant insert semantics. “Check then insert” without concurrency control can race.

Replaying the same staged input should add no hub rows. Record rejected/malformed keys separately with source lineage.

### Identify relationship semantics

A relationship statement needs participating concepts, role names and uniqueness. `Customer places Order` differs from `Employee approves Order` even if both connect a person-like hub to Order.

State whether the link records the first observed existence of a durable association, a transaction occurrence, hierarchy edge or another precise relation. Include a dependent/transaction identifier when repeated occurrences among the same hubs are distinct.

Do not encode changing descriptive state into link identity.

### Model the link grain

A link normally contains one row per unique ordered/role-aware combination of participating hub keys, plus its link key, first load time and record source. Roles must be stable in link-key component order.

The [AutomateDV link documentation](https://automate-dv.readthedocs.io/en/latest/tutorial/tut_links/) illustrates association keys derived from participating hub business/hash keys and technical load/source metadata.

Links can connect two or more hubs, but very high arity may hide several independent relationships. Model the business statement, not the source join table mechanically.

### Load links from staged keys

Derive participating hub keys with the same canonicalization used for hubs. This permits independent/parallel pattern loads from a common prepared stage, subject to platform constraint behavior.

Deduplicate link identity within and across batches. Preserve unresolved/invalid business-key evidence rather than silently substituting a generic identity that conflates entities.

Validate that every link role maps to the expected hub concept and scope.

### Separate relationship existence and effectivity

An immutable link states that a relationship was observed; it does not necessarily say when the relationship was active or ceased.

Track source-reported effective periods or active/inactive status in a satellite attached to the link. The [AutomateDV effectivity-satellite documentation](https://automate-dv.readthedocs.io/en/v0.9.6/tutorial/tut_eff_satellites/) describes using such a satellite to record when a link relationship starts and ends.

Define the driving-key and snapshot/deletion semantics carefully. Absence from an incomplete snapshot is not proof that a relationship ended.

### Identify satellite payloads

Satellites describe a hub identity or link relationship over time. Group attributes that share parent grain, source/provenance, privacy policy, change behavior and arrival cadence.

The [AutomateDV satellite documentation](https://automate-dv.readthedocs.io/en/v0.9.6/tutorial/tut_satellites/) describes point-in-time payload history related to a hub or link parent, using a hashdiff for change detection.

Avoid a single giant satellite mixing independent sources and rates; also avoid one-column satellites without a meaningful governance or loading reason.

### Declare the satellite grain

A basic satellite row represents one observed payload state for `(parent, source)` at a deterministic warehouse load position, optionally carrying source-effective time. Its uniqueness may require parent key, load timestamp and sequence/batch tie-break.

If several values are simultaneously valid, include a child-dependent key and use a multi-active design. If source deliveries contain several intra-batch states, preserve their order rather than arbitrarily taking one.

Write the proposition before choosing a macro or primary-key syntax.

### Separate load time and effective time

Load time answers when the warehouse learned the observation. Effective time answers when the source says it applied. These axes can disagree under late delivery or correction.

Retain both when effective-time questions matter. Load ordering needs enough precision and tie-breaking to remain deterministic under parallel batches.

Do not overwrite load time with source time. Doing so erases warehouse lineage and makes replay diagnosis impossible.

### Retain record source precisely

Record source identifies the feed/system/context that supplied the row. Its granularity should distinguish semantically different sources without becoming a volatile file path.

Keep batch/file/message lineage separately when needed. The first record source on a hub shows where the key was first encountered; satellites preserve the source of each payload state.

Record source is provenance, not proof of correctness or business ownership.

### Design canonical encoding

Before hashing, map typed components to an unambiguous byte sequence. Define Unicode normalization, case policy, whitespace, decimal scale, timezone, timestamp precision, null versus empty, component order, escaping/length-prefixing and character encoding.

Naive delimiter concatenation can collide: components `('A','B||C')` and `('A||B','C')` produce the same string without escaping. Null sentinel text can collide with a real value.

Version the encoding contract and use identical fixtures across languages/platforms.

### Use hash keys with safeguards

Hash keys can make composite keys fixed-width and independently derivable for parallel loads. They do not replace retained business keys or domain identity work.

Choose an algorithm/output size based on scale and risk, test collisions by comparing canonical inputs for equal hashes, and define remediation. The [AutomateDV hashing guidance](https://automate-dv.readthedocs.io/en/latest/best_practises/hashing/) distinguishes primary-key hashes from payload hashdiffs and warns that algorithm and component ordering matter.

Do not use an ordinary non-keyed hash as encryption or privacy anonymization.

### Estimate collision risk honestly

For a uniform $b$-bit hash and $n$ distinct inputs with $n$ much smaller than $2^{b/2}$, the birthday approximation is

$$
p_{collision}\approx\frac{n(n-1)}{2^{b+1}}.
$$

The approximation helps compare widths; actual safety also depends on correct implementation, adversarial inputs and operational collision detection.

A probability being small is not a database uniqueness proof. Retained canonical keys allow verification.

### Use hashdiffs for change detection

A hashdiff fingerprints the canonical payload (and any required identifying components) so the loader compares one value rather than every nullable column.

Component aliases/order, types, null handling and encoding are part of its definition. Adding a payload column changes the digest basis and can make every row appear changed unless migration/backfill policy is explicit.

A matching hashdiff is evidence of equal canonical payload under the chosen function, subject to collision risk.

### Suppress unchanged consecutive states

For each parent/source timeline, retain the first observation and later observations whose payload digest differs from the preceding effective/load-ordered state. This captures A→B→A as three changes; deduplicating on all-time distinct payload would incorrectly remove the return to A.

Preserve delivery/batch audit outside the compressed satellite if every arrival must be reconstructed. Satellite change history and raw message history are related but distinct grains.

Test multiple changes within one batch.

### Handle late and out-of-order satellites

Comparing an arriving row only with the latest warehouse state assumes arrival order equals history order. A late A state inserted between A and B may be redundant; a late C state may create two boundaries.

Recompute the affected parent/source timeline or use an ordering/tracking pattern designed for out-of-sequence loads. The current [AutomateDV extended-tracking documentation](https://automate-dv.readthedocs.io/en/latest/tutorial/tut_xts/) describes tracking satellite records for reconstruction, auditing and out-of-sequence loads.

Define whether reports use load-system chronology, source-effective chronology or both.

### Model multi-active attributes deliberately

Some payloads legitimately have several simultaneous members, such as phone numbers or contract parties. A basic single-active satellite cannot identify each concurrent value.

Use a child-dependent key at `(parent,member)` grain and historize each member. The [AutomateDV multi-active satellite documentation](https://automate-dv.readthedocs.io/en/stable/tutorial/tut_multi_active_satellites/) illustrates simultaneous child values identified by dependent keys.

Do not select an arbitrary primary value unless the business supplies a governed rule.

### Capture deletion and absence

CDC deletes are explicit observations. Full-snapshot absence may imply deletion only when the extract is complete for a known population and cutoff. Incremental absence means nothing.

Use status/tracking/effectivity structures or source-specific satellite attributes to preserve the observation without deleting prior Raw Vault rows.

Business Vault rules can interpret deleted, inactive, merged or superseded states for delivery.

### Correct without erasing evidence

If a source corrects a payload, append the new observation with its effective and load evidence. If the warehouse loaded malformed data, preserve auditable invalidation/supersession metadata and rebuild derivatives; do not silently rewrite history unless policy explicitly governs technical repair.

Erasure laws and prohibited-data remediation can require physical deletion or redaction. Auditability never overrides legal/privacy obligations; retain non-sensitive completion evidence where allowed.

Separate source correction from a new business state.

### Keep hard rules narrow in Raw Vault

Hard rules are deterministic structural necessities such as type alignment, canonical key derivation, technical deduplication and record-source assignment. They should not embed volatile management interpretation.

Do not filter a source row merely because today's business rule calls it irrelevant. Preserve valid evidence and apply eligibility downstream.

Document every transformation between landing and Raw Vault so “raw” is not mistaken for byte-identical.

### Apply soft rules in Business Vault

Business Vault models can conform cross-source descriptions, choose survivorship, calculate classifications, assert equivalence, derive effectivity and construct reusable interpretations.

Each rule has owner, version, effective/system times, inputs and tests. A new rule version should be replayable over preserved Raw Vault history.

Do not overwrite source satellites with conformed outputs; keep interpretation lineage visible.

### Handle cross-source identity

When CRM customer `17` and billing account `A9` refer to one party, the equivalence is not derivable from hash keys. Model a governed mapping/same-as assertion with evidence, confidence or authority and effective history.

Conflicting identifiers and split/merge events require reversible rules. Raw source identities remain traceable even when Business Vault creates a golden identity.

Avoid making personally identifying matching logic implicit in hub loading.

### Build PIT tables for as-of lookup

Joining several satellites as of a date repeatedly requires finding the latest eligible row from each history. A PIT structure can precompute the coordinates for selected as-of dates.

The [AutomateDV PIT documentation](https://automate-dv.readthedocs.io/en/v0.10.2/tutorial/tut_point_in_time/) describes a Business Vault query assistant that stores relevant satellite keys/load timestamps for each supplied date.

PIT grain, included satellites, time axis, calendar, watermark and rebuild policy must be explicit. It is a derivative index, not new source truth.

### Build bridges for relationship traversal

Vault queries can require many link/effectivity joins. A bridge can materialize valid relationship paths or aggregates for an as-of series.

The [AutomateDV bridge documentation](https://automate-dv.readthedocs.io/en/v0.9.6/tutorial/tut_bridges/) presents bridges as Business Vault query-assistance structures across hubs and links.

Prevent path fanout and double counting by declaring bridge grain, roles, traversal bounds, effectivity and allocation semantics.

### Deliver information marts

Most analysts should not assemble hubs, links and satellites for every question. Build requirements-driven dimensional facts/dimensions, wide models, aggregates, APIs or feature tables.

Marts own metric grain, current versus as-of semantics, dimensions and performance. They remain traceable to Business/Raw Vault inputs and rule versions.

Data Vault complements rather than replaces dimensional modeling.

### Reconcile each load pattern

For hubs, compare distinct valid canonical business keys in scope to inserted/existing hub keys. For links, compare distinct relationship identities and role completeness. For satellites, compare ordered payload transitions, not merely source row totals.

Track rejected, duplicate, unchanged, late and collision-candidate dispositions. Reconcile by source, batch and business-date partitions.

Grand totals cannot prove per-key history completeness.

### Automate from governed metadata

The repetitive structures suit generation, but metadata becomes production code. Store concept, key components/order, canonicalization version, parents/roles, satellite payload, source, times, algorithm, dependencies, ownership and classifications.

Generate DDL, load logic, tests, lineage and documentation from one validated model where practical. Review generated diffs and pin tool/template versions.

Automation magnifies both correct standards and incorrect metadata.

### Test deterministic loading

Test canonicalization across engines/languages, hub/link uniqueness, collision detection, parent referential integrity, satellite ordering, consecutive change suppression, A→B→A, same-timestamp ties, multi-active keys, replay, concurrent load, late insertion, deletions and schema changes.

Run the same input twice and compare exact rows/digests. Shuffle input order and require the same output under declared ordering.

Validate marts/PITs/bridges separately because Raw Vault correctness does not guarantee delivery correctness.

### Observe vault health

Monitor input, accepted, rejected, duplicate and unchanged counts; new hub/link rates; orphan roles; satellite changes per key; late/out-of-order rates; hash collisions; null business keys; record-source distribution; dependency watermarks; load duration; storage growth; PIT/bridge freshness; and mart reconciliation.

Unexpected zero new keys can mean stable business or broken ingestion. Compare source coverage and heartbeats.

Tie anomalies to schema/source releases and keep drill-through to batch evidence.

### Evolve without uncontrolled proliferation

Add satellites for new source-specific descriptions and links for genuinely new relationships. Do not create near-duplicate hubs because teams disagree on names; resolve concept/key semantics through governance.

Version canonicalization/hashdiff changes and plan migrations. Retain compatibility views or dual derivation for consumers while marts change.

Periodically review unused structures, table counts, join complexity and automation health. Extensibility should not become an excuse for orphaned objects.

## Definitions and Notation

Let a hub concept be $X$ with scoped business-key tuple $BK_X$. Let $C_v$ be canonical serialization version $v$, $H_a$ digest algorithm $a$, and

$$
HK_X=H_a(C_v(X,scope,BK_X)).
$$

Including concept/scope prevents identical text keys for different modeled namespaces from colliding semantically before hashing. Implementations may choose a different namespacing contract, but it must be consistent.

For link type $R$ with ordered role-labeled hub keys $(r_1:HK_1,\ldots,r_k:HK_k)$ and optional dependent transaction key $T$, define

$$
LK_R=H_a(C_v(R,r_1:HK_1,\ldots,r_k:HK_k,T)).
$$

Role order is semantic, not arrival or alphabetical accident.

For satellite parent $p$, source $s$ and payload vector $Y_i$ observed at effective time $t_i$ and loaded at $\ell_i$, let $q_i=H_a(C_v(Y_i))$. Define total order $(t_i,\ell_i,sequence_i)$ for effective history or $(\ell_i,sequence_i)$ for load-system history. Retain $i$ if it begins a timeline or $q_i\ne q_{i-1}$.

Let $R_b$ be staged valid business-key tuples, $H_b$ existing hub tuples and $N_b$ new hub tuples. A set-based idempotent load uses

$$
N_b=distinct(R_b)\setminus H_b.
$$

On replay after insertion, $distinct(R_b)\setminus(H_b\cup N_b)=\varnothing$.

For source coverage $U_t$ at snapshot cutoff $t$ and observed key set $O_t$, absence $x\notin O_t$ supports a deletion inference only if $U_t$ proves $x$ was eligible for complete observation. Otherwise absence is unknown.

## Mechanisms, Invariants, or Proof Structure

**Modeling mechanism.** Discover business concepts and scoped keys, identify role-aware relationships, assign source-specific payloads, define time/provenance/canonicalization, generate hub/link/satellite structures, load from immutable staging, reconcile, derive Business Vault rules and publish marts.

**Hub replay proof.** A hub load inserts $N_b=distinct(R_b)\setminus H_b$. After insertion the stored set is $H_b'=H_b\cup N_b$. Replaying the same input yields $distinct(R_b)\setminus H_b'=\varnothing$. This establishes set-level idempotence assuming deterministic canonicalization and atomic uniqueness enforcement.

**Run-compression proof sketch.** Partition an ordered payload sequence into maximal consecutive runs of equal canonical digest. Retaining the first element of every run produces exactly one representative for each observed transition. Removing any retained representative merges two different adjacent runs or loses the initial state; retaining any other element adds no new consecutive state. Collision-free equality for the observed inputs is an assumption checked operationally.

**A→B→A invariant.** Consecutive change detection retains all three states because each adjacent digest differs. Global `DISTINCT(parent,hashdiff)` would retain only A and B and is therefore not a valid history algorithm.

**Link-grain invariant.** One immutable link key represents exactly one declared role-aware relationship/transaction identity. Changing an active flag or descriptive attribute creates satellite history, not a new link, unless the relationship identity itself changed.

**Temporal invariant.** Warehouse load chronology is monotone per deterministic load order; business-effective chronology may receive late records. Neither axis is silently substituted for the other.

**Collision invariant.** If equal hash outputs occur for unequal canonical inputs, the load raises a collision disposition rather than merging identities/payloads. Hash equality is never the only retained evidence.

**Empirical evidence boundary.** Passing replay and hash fixtures proves observed implementation behavior for tested encodings and data. It does not prove business-key stability, cross-source identity or universal collision absence.

<!-- bijux-verify: {"id":"vault-idempotent-history","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"staged_rows=5\nhub_rows=2\nsatellite_rows=3\nsuppressed_rows=2\nc001_tiers=bronze>gold\nreplay_idempotent=True\n","stderr":""}} -->
```python
import hashlib

staged = (
    {"row_id": "r1", "source": "crm", "customer": "C001", "seq": 1, "name": "Ana", "tier": "bronze"},
    {"row_id": "r1", "source": "crm", "customer": "C001", "seq": 1, "name": "Ana", "tier": "bronze"},
    {"row_id": "r2", "source": "crm", "customer": "C001", "seq": 2, "name": "Ana", "tier": "gold"},
    {"row_id": "r3", "source": "crm", "customer": "C001", "seq": 3, "name": "Ana", "tier": "gold"},
    {"row_id": "r4", "source": "erp", "customer": "C002", "seq": 1, "name": "Bo", "tier": "silver"},
)

def digest(parts):
    encoded = "|".join(f"{len(value)}:{value}" for value in parts)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()

def load(rows):
    unique_deliveries = {}
    for row in rows:
        unique_deliveries.setdefault((row["source"], row["row_id"]), row)
    ordered = sorted(unique_deliveries.values(), key=lambda row: (row["customer"], row["source"], row["seq"], row["row_id"]))
    hubs = {}
    satellites = []
    latest_payload = {}
    for row in ordered:
        hub_key = digest(("customer", row["customer"]))
        hubs.setdefault(hub_key, row["customer"])
        payload = digest((row["name"], row["tier"]))
        timeline = (hub_key, row["source"])
        if latest_payload.get(timeline) != payload:
            satellites.append((hub_key, row["source"], row["seq"], row["tier"], payload))
            latest_payload[timeline] = payload
    return hubs, satellites

hubs, satellites = load(staged)
replay_hubs, replay_satellites = load(staged + staged)
c001_tiers = [row[3] for row in satellites if hubs[row[0]] == "C001"]
print(f"staged_rows={len(staged)}")
print(f"hub_rows={len(hubs)}")
print(f"satellite_rows={len(satellites)}")
print(f"suppressed_rows={len(staged) - len(satellites)}")
print(f"c001_tiers={'>'.join(c001_tiers)}")
print(f"replay_idempotent={hubs == replay_hubs and satellites == replay_satellites}")
```

## Alternatives and Trade-Offs

**Data Vault versus dimensional warehouse.** Vault structures optimize auditable integration and change isolation; star schemas optimize understandable analytical queries. A common architecture uses a vault upstream and dimensional marts downstream.

**Data Vault versus enterprise 3NF.** Both can integrate domains. A 3NF model centralizes current relational semantics and constraints; a vault decomposes keys, relationships and descriptive histories for insert-oriented change. Evaluate evolution, audit and query needs.

**Vault versus raw lake plus transformations.** Immutable files preserve source bytes cheaply, but without integrated keys/history every consumer repeats interpretation. A vault adds durable integration structure at table/automation cost. Many systems keep both landing evidence and vault.

**Natural/composite versus hash surrogate keys.** Natural keys preserve direct meaning and avoid collisions but can be wide and source-dependent. Hash keys are fixed-width and parallel-derivable but demand canonicalization, algorithm governance and collision handling.

**One versus several satellites.** One satellite reduces joins but mixes sources, rates and policies. Splitting improves independent loading and governance while multiplying tables and point-in-time joins.

**Load-time versus effective-time history.** Load time provides audit chronology and deterministic ingestion. Effective time answers business-as-of questions but can arrive out of order. Preserve both where both questions matter.

**Physical end dating versus derived intervals.** End dates make as-of queries direct but introduce updates and out-of-order repair. Deriving with ordered window logic preserves insert orientation but costs query/build work. PITs can cache results.

**Basic versus multi-active satellite.** Basic satellites assume one active payload per parent/source point. Multi-active designs preserve concurrent members but require a stable child-dependent key and more complex consumption.

**Raw Vault rule versus Business Vault rule.** Earlier application can simplify downstream use but risks losing source evidence when policy changes. Keep volatile interpretation in the Business Vault and only structural necessities in raw loading.

**Virtual versus persisted Business Vault/PIT/marts.** Views remain fresh to bases but repeat compute. Persisted derivatives improve predictable performance and require refresh, watermark, storage and rollback controls.

## Failure Modes and Misconceptions

- **“Data Vault is just hubs, links and satellites.”** Layering, methodology, automation and delivery are essential.
- **“Every source table becomes a hub.”** Hubs represent durable business concepts, not physical sources.
- **“Every code is a business key.”** Reference values and descriptive codes may not identify independent concepts.
- **“Same text key means same entity.”** Scope and business meaning may differ.
- **“Hashing solves identity integration.”** It only deterministically encodes already-governed identity inputs.
- **“A hash cannot collide.”** Finite digests can collide; retain inputs and detect conflicts.
- **“Hash order is cosmetic.”** Component order and serialization determine the output.
- **“Trimming and uppercasing are always safe.”** They can merge business-distinct keys.
- **“Hashdiff equals cryptographic security.”** It is change-detection metadata, not encryption.
- **“Descriptions belong in hubs for convenience.”** Mutable payload destabilizes identity structure.
- **“A link is a foreign-key table copy.”** It represents a governed role-aware business relationship grain.
- **“An active flag belongs in the link key.”** Effectivity/status changes belong in history attached to the relationship.
- **“One satellite per hub is simplest.”** It can mix incompatible source and rate semantics.
- **“One attribute per satellite is pure.”** Unbounded fragmentation creates unnecessary joins and operations.
- **“Load date is when the business state began.”** It records warehouse knowledge time.
- **“Latest arrival is latest effective state.”** Late data can invert arrival and business chronology.
- **“Distinct hashdiffs preserve history.”** A→B→A requires consecutive comparison.
- **“Snapshot absence means delete.”** Only complete governed coverage supports that inference.
- **“Insert-only means data is never removed.”** Legal erasure and technical remediation still apply.
- **“Raw Vault is byte-for-byte raw.”** Structural hard rules may transform, so landing evidence and lineage matter.
- **“Raw means no validation.”** Keys, types, provenance and canonicalization require strict checks.
- **“Business rules in raw save time.”** Volatile rules then erase or entangle source evidence.
- **“Analysts should query the Raw Vault.”** Consumer marts usually provide safer grains and semantics.
- **“PIT tables contain truth.”** They are rebuildable as-of query coordinates.
- **“Bridges remove fanout automatically.”** Their path grain and allocation still need contracts.
- **“Parallel load means no dependencies exist.”** Shared canonicalization, staging completeness and constraints remain dependencies.
- **“Automation removes modeling.”** It scales the metadata decisions, including mistakes.
- **“A vault is always more agile.”** Without expertise, automation and delivery discipline, table proliferation slows change.

## Worked Examples

### Example 1

CRM and billing both contain `C001`, but each tenant independently numbers customers. A hub key based only on `C001` merges unrelated parties.

The modeled key includes tenant scope and customer ID. If later evidence proves two scoped identities represent one party, a versioned Business Vault equivalence maps them while Raw Vault source identities remain traceable.

### Example 2

A customer changes name and risk tier. A proposed hub includes both fields, so each change creates a new “customer” identity.

The hub retains only stable customer business key and technical provenance. A source-specific customer satellite records name/tier payload transitions. The same hub anchors orders and later sources.

### Example 3

Orders `O7` and `O8` both belong to customer `C1`. A customer-order link key uses only the two hub keys and roles, yielding two distinct link rows because each order hub key differs.

If repeated transactions can occur between identical participants without an Order hub, the link identity includes a stable transaction/dependent key. Relationship grain is declared rather than inferred from column count.

### Example 4

An employee is assigned to Department A, then B. The base employee-department link preserves both observed relationship identities, while an effectivity/status satellite records their active intervals under a complete snapshot/CDC policy.

Deleting the A link would lose the historical association. Treating snapshot absence as end-of-effectivity without coverage evidence could create a false transfer.

### Example 5

A customer payload changes A→B→A. A loader inserts only globally unseen `(parent,hashdiff)` pairs and suppresses the second A.

The correct loader compares consecutive ordered states and retains all three observations. The return to A is a business transition even though the payload appeared earlier.

### Example 6

A source emits two active phone numbers for one customer at the same effective time. A basic satellite primary key collides or arbitrarily chooses one.

A multi-active satellite includes a stable phone/member child key and historizes each member. A downstream “primary phone” is a Business Vault rule only if authority/priority evidence exists.

### Example 7

A record effective January 5 arrives after the January 10 state. Comparing only to the latest state classifies it incorrectly and may create a redundant change.

The loader recomputes that parent/source effective timeline with deterministic tie-breaks, retaining only genuine adjacent transitions. Load chronology still records that the January 5 claim arrived later.

### Example 8

Marketing changes the definition of “active customer.” The old warehouse filtered inactive source rows before persistence, so last year's metric cannot be recomputed.

The vault preserves valid customer/activity observations in Raw Vault. Business Vault versions both active rules, and the mart publishes comparable historical series with rule identity.

### Example 9

Building a customer dimension requires the latest eligible row from four satellites for every month-end. Repeated window joins dominate processing.

A PIT table stores the parent and selected satellite load coordinates per month-end/as-of time. It is refreshed from declared watermarks and validated against direct as-of queries, then used to build the dimensional mart.

### Example 10

A team generates 600 vault tables but has no metadata ownership, source controls or marts. Analysts face long joins and duplicate definitions; schema changes require manual edits everywhere.

The recovery creates a governed metadata registry, validates key/link/satellite propositions, generates repeatable code/tests/lineage, retires unjustified fragments and prioritizes requirements-driven marts. Pattern count is not a success metric.

## Cross-Program Connections

- [Database Engineering](../../18-database-engineering/ROADMAP.md): uniqueness, temporal history, hashing, transactions and materialized query helpers underpin vault structures.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md): business concepts, identity, lineage, policy boundaries and information marts govern enterprise integration.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md): parallel loading, partitioning, history growth and graph-like joins shape physical performance.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): deterministic keys, retries, ordering, late arrival and replay determine idempotent ingestion.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md): domain identifiers, relationship events and contract versions supply durable vault inputs.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): metadata generation, orchestration, observability, access control and rollback make a patterned warehouse sustainable.

## References

1. Data Vault Alliance, [Data Vault 2.0: An Introduction](https://datavaultalliance.com/engineering/data-vault-2-0-an-introduction/). Introduces hubs, links, satellites and dimensional delivery in the methodology's own terminology.
2. Data Vault Alliance, [Suggested Object Naming Conventions](https://datavaultalliance.com/engineering/data-vault-2-0-suggested-object-naming-conventions/). Documents standard object families and the role of consistent metadata/naming.
3. Google Cloud, [Data Vault on BigQuery](https://services.google.com/fh/files/misc/google-cloud-data-vault_b.pdf). Describes staging, Raw Vault, Business Vault and information-mart layer responsibilities.
4. AutomateDV, [Hubs](https://automate-dv.readthedocs.io/en/latest/tutorial/tut_hubs/). Provides maintained implementation documentation for business keys, load time and record source.
5. AutomateDV, [Links](https://automate-dv.readthedocs.io/en/latest/tutorial/tut_links/). Documents relationship structures and their participating hub keys.
6. AutomateDV, [Satellites](https://automate-dv.readthedocs.io/en/v0.9.6/tutorial/tut_satellites/). Documents descriptive history, parent keys, payloads, load/effective metadata and hashdiffs.
7. AutomateDV, [Hashing](https://automate-dv.readthedocs.io/en/latest/best_practises/hashing/). Explains hash-key and hashdiff purposes, algorithm choices and component-order requirements.
8. AutomateDV, [Effectivity Satellites](https://automate-dv.readthedocs.io/en/v0.9.6/tutorial/tut_eff_satellites/). Describes tracking relationship start/end effectivity separately from the link.
9. AutomateDV, [Multi-Active Satellites](https://automate-dv.readthedocs.io/en/stable/tutorial/tut_multi_active_satellites/). Describes concurrent child-dependent payload members.
10. AutomateDV, [Point-in-Time Tables](https://automate-dv.readthedocs.io/en/v0.10.2/tutorial/tut_point_in_time/). Describes as-of satellite query-assistance structures.
11. AutomateDV, [Bridge Tables](https://automate-dv.readthedocs.io/en/v0.9.6/tutorial/tut_bridges/). Describes relationship-path query-assistance structures.
12. AutomateDV, [Extended Tracking Satellites](https://automate-dv.readthedocs.io/en/latest/tutorial/tut_xts/). Documents tracking support for audit, reconstruction and out-of-sequence loading.

## Exercises

### Exercise 1

Model customer, account and transaction data from CRM and billing as hubs, links and satellites. Define scoped business keys, relationship roles, source-specific payloads, load/effective times, deletions, cross-source equivalence and downstream mart boundaries.

### Exercise 2

Specify a cross-platform canonical hash contract for composite key `(tenant_id, customer_id)` and a customer-detail hashdiff. Address nulls, empty strings, Unicode, case, delimiters, types, ordering, algorithm migration, collisions and test fixtures.

### Exercise 3

Satellite observations for one parent arrive in warehouse order: `(effective 10,A)`, `(effective 30,C)`, `(effective 20,B)`, `(effective 25,B)`, `(effective 40,A)`. Derive effective-time change history and explain why latest-only and global-distinct algorithms fail.

### Exercise 4

Design idempotent incremental loading and reconciliation for hubs, links and satellites when batches retry, two loaders overlap, snapshots omit rows, CDC deletes arrive late and two source records share a load timestamp.

### Exercise 5

Design the Business Vault and information delivery for month-end customer reporting across three satellites and two relationship paths. Specify PIT/bridge grains, rule versions, freshness, performance validation, mart reconciliation and rollback.

## Answers to the Exercises

### Answer 1

Create Customer, Account and Transaction hubs only where each has a durable business identifier; include tenant/legal-entity/source namespace when identifiers are not enterprise-global. A customer-account link records role-aware association, and an account-transaction link or transactional relationship includes the transaction identity so repeats remain distinct.

Attach CRM and billing descriptive payloads to separate customer/account satellites because provenance, cadence and semantics differ. Retain warehouse load and source-effective times plus record source/batch evidence. Model explicit CDC delete or complete-snapshot status in tracking/effectivity history, never from incremental absence. Preserve source customer identities; Business Vault equivalence links them only under governed evidence. Deliver dimensional customer/account/transaction facts with explicit survivorship and as-of rules rather than exposing Raw Vault joins directly.

### Answer 2

Define a versioned typed encoder using UTF-8 after chosen Unicode normalization, length-prefix each component, distinguish null from empty, preserve or explicitly normalize case/whitespace only when the business declares equality, canonicalize numeric scale and timestamps, and fix tuple order as tenant then customer. Include concept/namespace if the hash space is shared. Store retained canonical components and encoding/algorithm version.

For the hashdiff, fix the payload aliases/order and typed encodings separately from the primary key. Use a documented digest width appropriate to scale, compare equal hashes against canonical inputs/payload in collision tests, and fail/quarantine conflicts. Publish fixtures for null/empty, delimiter text, Unicode equivalents/non-equivalents, case, leading zero, decimals and timezones across every engine. Algorithm or encoding migration uses dual keys/digests and comparison before cutover, never silent in-place reinterpretation.

### Answer 3

Sort by effective time with deterministic load/sequence tie-break: `(10,A),(20,B),(25,B),(30,C),(40,A)`. Consecutive compression retains `(10,A),(20,B),(30,C),(40,A)` because the second B is unchanged relative to the preceding effective state.

Latest-arrival comparison sees order A,C,B,B,A and can create the wrong boundaries or suppress the wrong row because arrival is not effective chronology. Global distinct keeps only one A, B and C, losing the return to A at 40. Preserve load chronology separately and rebuild the affected effective timeline when the late B observations arrive.

### Answer 4

Stage each immutable delivery with source event/file row identity, batch, source sequence and load tie-break. Deduplicate retries; derive keys/digests from one canonicalization version. Hubs and links use set-based distinct anti-joins plus atomic unique enforcement so overlapping loaders cannot double insert. Satellites partition by parent/source, order all intra-batch states deterministically, compare consecutive payloads and use a uniqueness key that survives same timestamps.

Treat a CDC delete as an explicit status observation and apply source order even when late. Infer snapshot disappearance only after proving full eligible coverage and cutoff. Reconciliation records input, rejected, duplicate, unchanged, inserted and late counts; compares distinct valid business keys to hubs, relationship identities to links, and expected transition sequences to satellites. Replay and shuffled-order tests must yield the same stored result; collision candidates and conflicting same-order states quarantine rather than pick arbitrary winners.

### Answer 5

Version Business Vault survivorship, equivalence, active-status and derived classification rules over preserved Raw Vault inputs. Build a customer PIT at `(customer_hk,month_end,rule/input_version)` that points to the latest eligible rows from each of three satellites under the chosen load/effective axis. Build a relationship bridge at `(customer_hk,month_end,path_member_or_aggregate,rule_version)` with explicit effectivity and allocation to prevent path fanout.

Record each source watermark, as-of calendar, code/schema version and publication time. Validate PIT coordinates against direct window queries, bridge paths against effective links and mart customer/fact keys/measures against governed controls. Benchmark the direct vault joins versus assistants including refresh/storage. Generate a dimensional or wide month-end mart for users, publish PIT/bridge/mart candidates atomically, retain the prior coherent version and roll back by switching the publication pointer. Never present newly published outputs with mismatched source cutoffs as one month-end snapshot.
