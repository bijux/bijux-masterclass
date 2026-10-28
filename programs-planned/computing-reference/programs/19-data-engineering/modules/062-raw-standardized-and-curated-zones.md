---
module_id: DE-062
program: Data Engineering
level: 2
module_number: 62
title: Raw, Standardized, and Curated Zones
status: complete
last_verified: 2026-09-03
---

# Raw, Standardized, and Curated Zones

## One-Page Review

### Governing question

How should a data platform divide raw, standardized, and curated responsibilities so every transition has a testable contract, immutable lineage, compatible security and retention, deterministic replay, owned exceptions, and consumer fitness—without turning the zones into duplicate dumps, sequential folders, or vague claims that data becomes universally “better” as it moves right?

### Essential definitions

- A **zone/layer** is a governed data-product boundary with named entry criteria, allowed transformations, exit guarantees, owners, readers, retention, and recovery behavior.
- The **raw zone** preserves source observations and acquisition evidence with minimal semantic reinterpretation so ingestion can be audited and replayed.
- A **landing zone** is a restricted, often transient intake boundary used for transfer, scanning, decryption, or masking before governed raw admission.
- The **standardized zone** contains validated, typed, canonical, deduplicated, conformed, and traceable records under reusable technical/domain contracts.
- The **curated zone** contains consumer- or decision-oriented data products with explicit grain, measures, dimensions, service levels, and change policy.
- **Fidelity** means the platform can reproduce what was received, including source identity, coordinates, bytes or canonical envelope, and acquisition metadata.
- **Truth** is an authoritative domain claim. Raw fidelity does not make a source observation correct.
- A **conformance rule** maps source-specific names, types, units, codes, identities, and temporal meanings to a versioned canonical contract.
- A **quality gate** is a deterministic predicate with a version, severity, disposition, evidence, and owner—not merely a score.
- **Quarantine** is an access-controlled, durable exception product for invalid, conflicting, unsafe, or unprocessable records with repair disposition.
- **Promotion** is the publication of a new downstream snapshot after its input cut and contract checks pass; it is not a file move.
- **Lineage** records exact input dataset snapshots, transformation/code/config identities, run, output snapshot, quality results, and environment.
- A **data product** is an owned, discoverable interface with semantics, access policy, quality/freshness objectives, versioning, and support obligations.
- **Grain** states what one row/entity represents. Curated measures are invalid when grain and additivity are ambiguous.
- **Restatement** republishes affected downstream snapshots or correction facts when late data, source correction, rule change, or defect changes an earlier result.

### Central model, mechanism, or theorem

For one finite source cut $I$, raw dispositions partition observations into admitted raw $R$, landing rejection $J$, and intake quarantine $Q_0$:

$$
|I|=|R|+|J|+|Q_0|.
$$

Standardization maps each raw occurrence to exactly one primary outcome—accepted standardized $S$, exact duplicate $D$, or quarantine $Q_1$—under contract version $v$:

$$
T_v:R\rightarrow S\uplus D\uplus Q_1,
\qquad |R|=|S|+|D|+|Q_1|.
$$

Curated product $C_{p,r}$ is a deterministic function of pinned standardized snapshots, business-rule version, and declared exceptions:

$$
C_{p,r}=F_{p,r}(S_{g_1},\ldots,S_{g_n},E_r).
$$

The layers form a lineage graph, not a universal promotion ladder. A curated product can have multiple standardized inputs; a standardized product can serve many curated products; raw evidence remains independently retained. Correctness requires deterministic identity and contracts at edges, not physical adjacency.

### Critical invariants

- Raw data preserves received evidence and source coordinates; normalization never overwrites the only retained source representation.
- Raw is faithful but not automatically valid, complete, safe, current, unique, or authoritative.
- Every zone has explicit admission, guarantees, owner, access, retention, publication, and deprecation rules.
- Zone transitions publish new immutable/table snapshots; they do not destructively move the only copy forward.
- Standardization is deterministic for a pinned input cut, transformation version, reference-data snapshot, configuration, and execution semantics.
- Occurrence identity and semantic fingerprint distinguish exact duplicates from conflicting reuse and legitimate repeated events.
- Rejected or quarantined records remain counted, traceable, access-controlled, owned, and repairable; no silent drop creates false completeness.
- Canonical types, units, time zones, null/missing meanings, identifiers, and schema evolution rules are versioned.
- Curated products state grain, dimensions, measure formulas/additivity, population, effective/system time, refresh/finality, and intended decisions.
- A “gold” label never substitutes for consumer acceptance, reconciliation, certification, or a service objective.
- Lineage names exact input and output snapshots plus code, rules, reference data, run, and quality evidence.
- Security classification, residency, consent, purpose, retention, legal hold, and erasure propagate or become stricter; copying zones does not relax policy.
- Backfills and restatements use isolated generations and atomically publish rather than mixing with current results.
- Reconciliation covers counts, identities, amounts, and exceptions at compatible cuts; total inputs equal mutually exclusive dispositions.

### Common failures

Common failures include calling an uncontrolled bucket “raw”; treating raw as unquestionable truth; parsing and dropping fields before preserving evidence; storing secrets or personal data broadly because the layer is internal; writing analysts directly to ingestion tables; using bronze/silver/gold as folder colors without contracts; copying identical data into every zone; treating quarantine as a dead-letter graveyard; deduplicating by payload equality; conforming timestamps without time-zone/source authority; silently mapping unknown codes to “other”; joining mutable reference data during replay; declaring standardized data business-ready for every consumer; building curated metrics without grain or additivity; allowing curated logic to become an undocumented semantic layer; promoting in-place; mixing backfill with live snapshots; deleting raw before the correction/replay horizon; granting downstream readers upstream raw permissions; counting only accepted rows; and measuring layer success by dataset count instead of trustworthy use and obligations.

### Compact example

A source cut contains five order observations: one valid order, its exact retry, one malformed amount, one second valid order, and a conflicting reuse of the second event ID. Raw retains all five envelopes and coordinates. Standardization emits two canonical orders, records one exact duplicate, and quarantines two records with reasons and fingerprints. A curated daily-country product aggregates exactly the two accepted occurrence IDs. Its snapshot records raw cut, standardization rules, reference-data snapshot, curated metric version, and quality reconciliation `5 = 2 + 1 + 2`. Repairing the malformed record creates a new standardized and curated snapshot; it does not mutate the historical raw observation.

### Connections

[DE-028](028-deduplication-and-record-identity.md) defines record identity, [DE-037](037-backfills.md) establishes foundational backfill semantics, [DE-038](038-late-corrections-and-restatement.md) defines correction, [DE-046](046-backfill-planning.md) defines isolated replay, and [DE-061](061-object-storage-as-a-data-substrate.md) supplies immutable object/manifest publication. DE-063 adds table snapshots; DE-064/065 govern schema and partition evolution; DE-066 provides reproducible reads; DE-071 through DE-080 deepen quality, contracts, lineage, freshness, incident, and observability practice.

## Governing Question

Layered lake architecture is often summarized as raw/bronze, standardized/silver, and curated/gold. The names are convenient; the contracts are the architecture. A folder called `gold/` can hold undocumented, stale, privacy-violating data. A well-owned raw event product can be more trustworthy for forensic use than an aggregated “gold” table.

The governing task is to define what each product preserves, changes, guarantees, and exposes. Raw protects the ability to answer “what did we receive?” Standardized answers “what canonical records satisfy this reusable contract?” Curated answers “what product is fit for this named consumer and decision?”

These are not claims that uncertainty monotonically disappears. Standardization can reject evidence, introduce mapping error, or depend on wrong reference data. Curated aggregation can hide important variation or encode contested definitions. Each downstream representation should be more suitable for its declared use while retaining lineage and exceptions, not more universally true.

Zones may be implemented as catalogs/schemas, separate storage accounts/buckets, table namespaces, access domains, or combinations. Sensitive landing may require a separate security boundary. Physical design follows access, blast radius, lifecycle, and operational needs; three folders are not mandatory.

Nor must every dataset traverse three materializations. A valid pass-through may promote a raw format directly into a carefully contracted product, and some standardized products have no curated derivative. The architecture should justify each copy, transformation, and contract.

## Why This Matters

Replay requires preserved evidence. If ingestion parses a CSV with today's defaults, discards unknown columns, normalizes timestamps, and retains only the output, tomorrow's corrected parser cannot reconstruct the source cut. Raw fidelity makes transformation defects recoverable.

Shared analytics requires conformance. If every team independently interprets country code, currency, customer identity, deletion, and event time, curated metrics disagree even when formulas look identical. A standardized contract concentrates reusable technical and domain decisions while exposing their version.

Decision products require purpose. A canonical order event is not automatically the right sales metric. Revenue may exclude tax, refunds, tests, fraud, or unrecognized performance obligations. Curated products own these definitions, grain, temporal behavior, and service expectations.

Security risk often increases with copying. Raw may contain unmasked identifiers and unexpected fields; standardized data can make identities easier to join; curated products may expose sensitive inferences. Each boundary needs classification and authorization, not an assumption that downstream data is safer.

Silent drops corrupt trust. If malformed records disappear between layers, the curated total can reconcile internally while undercounting source activity. Quarantine plus disposition accounting makes incomplete results visible and repairable.

Operationally, layering isolates change. A source schema incident can stop one standardization product without invalidating immutable acquisition evidence. A business-rule change can rebuild curated products from pinned standardized snapshots without rereading proprietary source APIs. Isolation works only when lineage and retention horizons are compatible.

Layering can also waste money and attention. Unbounded duplicate copies, transient intermediates retained forever, tiny files, unused products, and repeated transformations increase storage, compute, catalog, security, and support costs. Every materialization needs a consumer, recovery, performance, or governance reason.

## Prerequisites and Retrieval

Retrieve source semantics: producer owner, system of record, export/CDC/API contract, occurrence identity, entity key/version, schema, deletion representation, timestamp authority, source coordinates, completeness boundary, late/correction behavior, replay limits, and known defects.

Retrieve acquisition evidence: landing location, file/message identity, original bytes or canonical envelope, transport headers, checksums, encryption, source path/topic/partition/offset/LSN, extraction window, ingestion clock, connector version, attempt, and manifest.

Retrieve raw contract: admitted formats, allowed envelope additions, immutability, partition/key design, versioning, schema drift capture, corrupt/unsafe handling, discoverability, readers, retention, residency, legal hold, and permanent-delete policy.

Retrieve standardization contract: canonical schema and field IDs, types, null/missing/default meanings, units, time zones, code mappings, identity/fingerprint, duplicate/conflict policy, validation predicates, severity, quarantine, reference datasets, late/upsert/delete semantics, and deterministic rule version.

Retrieve curated contract: data-product owner, consumers and decisions, grain, population, dimensions, measures, additivity, effective/system time, slowly changing behavior, aggregation window, freshness, completeness/finality, privacy, sharing, performance, certification, and deprecation.

Retrieve transition mechanics: pinned input snapshot/cut, job/run, code/container/package digest, configuration, reference-data snapshot, engine/runtime, output snapshot, atomic publish, retry identity, checkpoint, backfill generation, reconciliation, and rollback.

Retrieve exception workflows: landing rejection, malware/secret scan failure, parse failure, unknown schema, invalid fields, identity conflict, unmatched reference, policy violation, manual adjudication, repair SLA, replay path, and evidence access.

Retrieve security: source classification, tenant, purpose/consent, residency, encryption/KMS, service principals, row/column/masking policy, raw access, catalog access, cross-account sharing, audit, break-glass, retention, hold, and erasure propagation.

Retrieve operational/cost evidence: ingress bytes/records, accepted/duplicate/quarantined counts, transformation latency, backlog, file count/size, snapshot count, compute, storage copies, scan bytes, access frequency, reference lookup, compaction, failed runs, repair age, freshness, and consumer queries.

Distinguish landing from raw; raw fidelity from source truth; parse success from validity; technical standardization from business curation; conformance from aggregation; quarantine from discard; exact duplicate from identity conflict; current snapshot from historical evidence; event time from ingest time; completeness from freshness; validation score from gate; publication from file movement; and lineage from a job-name string.

Create a zone contract:

| Zone/edge | Admission | Guarantees | Primary readers | Retention and exceptions |
|---|---|---|---|---|
| Landing | Authenticated transfer, scan/decrypt scope | Receipt evidence only; not analytical | Intake/security operations | Short, explicit TTL; rejected/unsafe route |
| Raw | Source cut admitted with identity/checksum | Immutable fidelity, coordinates, envelope, discoverability | Ingestion, audit, replay, restricted investigation | Covers replay/audit/legal/privacy; parse/quarantine evidence |
| Standardized | Pinned raw cut and rule/reference versions | Canonical types/IDs/time/units, validation, dedup/conflict, reusable detail | Data engineering, analytics, science, downstream products | Rule-specific quarantine, history/correction horizon |
| Curated | Pinned standardized inputs and product contract | Declared grain, metrics, population, quality/freshness, consumer fitness | Named BI/ML/application consumers | Product SLA, restatement, deprecation and erasure |

Write a falsifiable claim: “Orders raw v4 preserves every source envelope and coordinate for 400 days under restricted access; standardized orders v7 deterministically maps schema, UTC event time, ISO currency, cents, tenant-scoped occurrence identity, exact duplicate/conflict/invalid dispositions, and reference snapshot IDs; revenue-daily v12 publishes one row per business date/country under formula and finality contracts; every snapshot records exact inputs, code/rules, quality results, and exceptions; daily reconciliation partitions all raw records with no unexplained residue; and backfills publish isolated snapshots with rollback.”

## Learning Objectives

After completing this module, you should be able to:

1. define raw, standardized, curated, landing, and quarantine as governed contracts rather than folders;
2. preserve source fidelity and acquisition evidence without claiming raw observations are authoritative truth;
3. design deterministic canonicalization for identity, schema, types, units, time, nulls, codes, and references;
4. partition exact duplicates, identity conflicts, invalid records, and accepted records with reconciliation;
5. specify curated data-product grain, population, measures, dimensions, temporal semantics, and service objectives;
6. capture snapshot-level lineage sufficient for replay, audit, correction, and impact analysis;
7. apply least privilege, classification, residency, retention, legal hold, and erasure across every zone;
8. publish, backfill, restate, roll back, and deprecate products without in-place partial visibility;
9. model the storage, compute, request, catalog, repair, and support cost of materialized layers; and
10. fault-test zone transitions against finite source cuts and consumer acceptance criteria.

## Core Exposition

### Define boundaries by contract, not color

Organizations use raw/standardized/curated, bronze/silver/gold, landing/stage/analytics, or domain-specific names. Official AWS, Microsoft, and Databricks guidance describes related multi-layer patterns but differs in terminology and physical recommendations. Preserve the intent and document the local mapping.

A zone contract answers: what enters; what transformations are allowed; what properties are guaranteed; who owns it; who may read/write/administer it; how publication works; how long data and exceptions remain; and what evidence proves the claims.

Do not infer “higher quality” from location alone. Catalog status should identify contract version, last successful snapshot, validation/reconciliation, freshness, owner, classification, and certification. A broken curated product must be visibly broken even if its path contains `gold`.

Zone boundaries can be logical. Separate catalogs or schemas may share an object bucket if authorization, lifecycle, and blast radius remain enforceable. Conversely, sensitive landing may need a separate account and encryption administration even before raw. Choose physical isolation from policy and failure domains.

### Preserve raw fidelity without sanctifying the source

Raw answers what arrived. Preserve original bytes when lawful/practical, or a canonical lossless envelope when transport constraints require it. Record source identity, coordinate, extraction window, event and ingest timestamps, checksum, schema/header, connector, run/attempt, encryption, and acquisition outcome.

Minimal transformation can include encryption, compression packaging, malware handling, transport decompression with preserved original, and envelope metadata. Any lossy parse, field drop, type coercion, timezone conversion, deduplication, or correction belongs in a traceable downstream output unless explicitly part of the source contract.

Raw is not “anything goes.” Admission can require authenticated producer, permitted classification/residency, checksum, envelope syntax, size/rate bounds, and safe content handling. A landing zone can isolate untrusted bytes until scanning, decryption, or masking succeeds.

Nor is raw the ground truth. Source systems contain duplicates, missing rows, invalid clocks, bugs, unauthorized values, and retrospective corrections. Call it authoritative evidence of receipt within a cut; name the domain authority separately.

Use immutable keys/snapshots from DE-061. Never overwrite the only raw representation with a parsed form. If schema drift prevents parsing, preserve bytes and route the parse outcome so a corrected rule can replay.

### Make source cuts and completeness explicit

A raw batch needs a finite boundary: manifest, high-water mark, export snapshot, transaction/log range, or object inventory cut. “All files seen by 02:00” is only defensible if the producer's delivery and closure semantics define it.

For stream acquisition, raw can remain append-oriented while periodic snapshots name partition/offset or source positions. Record gaps, resets, truncation, and late source behavior. Processing time is not source completeness.

Reconcile intake using counts and stronger controls where appropriate: file/object identities, record identities, source sequence ranges, bytes, monetary/control totals, partition coverage, checksums, and rejected/quarantined counts. A count match alone can hide duplicate-plus-missing cancellation.

Late arrivals and source corrections should enter new raw observations with source identity and correction relation. Do not mutate history invisibly. Downstream restatement decides which standardized and curated snapshots change.

### Standardize types and meanings deterministically

The standardized zone makes reusable detail consistent. Typical work includes parsing; canonical field IDs/names; explicit types; UTC plus retained source zone/offset; unit/currency normalization; code mapping; identifier normalization; deletion/tombstone handling; exact duplicate/conflict classification; validation; and conformance across sources.

Every mapping has a version. Preserve raw value, parsed value, rule ID, and failure reason where audit or repair requires it. Never map an unknown enum silently to a valid category; use explicit unknown/unmapped semantics or quarantine according to contract.

Null, missing, empty, redacted, not applicable, unknown, and zero are distinct states unless the contract proves equivalence. Defaulting a missing amount to zero can turn absence into a financial fact.

Time normalization requires source authority. Preserve source text, parsed instant, zone/offset, precision, ambiguity resolution, and parser/rule version. A date without zone is not automatically UTC. Event, effective, transaction, ingest, and processing times serve different decisions.

Units and currency require reference/effective dates and rounding rules. Store canonical integer minor units only when the currency/domain scale is defined; not every currency has two decimals. Record original amount/unit and conversion-rate snapshot where conversion occurs.

### Resolve identity, duplicates, and conflicts

Define tenant/source/type/generation-scoped occurrence identity. Pair it with a canonical semantic fingerprint. When identity and fingerprint match, the later observation can be classified as an exact duplicate under the retained horizon. When identity matches but fingerprint differs, it is a conflict, not a duplicate to discard.

Legitimate repeated business events may have identical payloads and distinct occurrence IDs. Payload-wide `DISTINCT` is therefore unsafe. Entity identity also differs from occurrence identity: many order events can refer to one order.

State whether standardized tables represent events, current entities, version history, or bitemporal facts. A current-state upsert must not erase the standardized event/history product that replay and audit require unless another retained authority supplies it.

Receipt state, source cut, accepted output, and dispositions must recover coherently. Backfill cannot reuse short live dedup horizons blindly. Use pinned raw identities and an isolated generation, then reconcile against the authoritative historical output.

### Operate quarantine as a product

Quarantine preserves records that cannot enter the claimed downstream contract: unsafe content, parse failure, invalid type/range, unknown required code, identity conflict, unmatched reference, prohibited classification, or ambiguous correction.

Each entry records raw identity/version, rule and version, failure code, observed safe context, first/last occurrence, owner, severity, retryability, repair deadline, access classification, and disposition. Avoid copying sensitive payloads when a protected reference suffices.

Distinguish permanent rejection, retryable infrastructure error, source remediation, rule defect, reference-data lag, manual adjudication, and accepted exception. One dead-letter bucket with no owner is silent loss with storage cost.

Repair creates evidence: corrected source event, approved mapping, revised rule, or adjudication record. Re-run from the immutable raw identity into a new standardized snapshot and propagate restatement. Never edit quarantined bytes to make history appear valid.

Track quarantine rate, age, reason, source, affected products, repair throughput, reoccurrence, and expired obligations. Alert on absolute count and denominator-aware rate; a zero rate may indicate the validation path is broken.

### Build curated products for named decisions

Curated is not a universal enterprise truth layer. Each product identifies consumers, decisions, owner, support, intended/non-intended use, grain, population, dimensions, measures, time, freshness, completeness/finality, quality objectives, access, and change/deprecation policy.

For every table, finish the sentence “one row represents …”. For every measure, state formula, unit, allowed dimensions, additive/semi-additive/nonadditive behavior, exclusions, rounding, and late/correction policy. Ratios should normally be derived from additive numerator/denominator at compatible grain rather than summed.

Curated products may be dimensional facts/dimensions, wide feature tables, aggregates, semantic models, exports, or application-serving datasets. “Gold” does not mean aggregated: detailed consumer-ready facts can be curated when their contract is purpose-specific.

Business definitions need stable identifiers and review. A column named `revenue` without recognition policy, tax/refund handling, currency basis, and effective version is not curated merely because a dashboard uses it.

Consumer acceptance is evidence. Validate representative queries, totals, freshness, access/masking, performance, explainability, and backfill/restatement behavior with the owning consumer. Certification expires or changes when dependencies/contracts change.

### Capture lineage at snapshot and field meaning

Record exact input dataset/table/object snapshot IDs, transformation code/package/image digest, configuration, schema/rule version, reference-data snapshots, engine/runtime, run/attempt, output snapshot, quality results, exceptions, and publication time.

A lineage edge should be reproducible: `raw orders snapshot 44 --standardize v7/ref-country-9--> standardized orders snapshot 31`. “Job orders_etl ran Tuesday” is not enough because job code, inputs, and outputs can vary.

Column/field lineage matters when meaning changes, but do not fabricate precision. Generated SQL plans can show syntactic dependency while a business rule or UDF hides semantics. Mark inferred versus declared lineage and test critical measures explicitly.

Lineage enables impact analysis but is also sensitive metadata: dataset names, tenant paths, queries, and ownership can disclose information. Apply access, retention, and integrity controls to lineage and audit evidence.

### Publish transitions atomically

Each transition reads pinned inputs and creates a new output snapshot. Validate it before changing the discoverable pointer/catalog entry. Readers resolve one published snapshot, not a mutable directory receiving files.

The run state machine is `planned -> acquiring -> transforming -> validating -> publishable -> published`, with explicit failed/quarantined/superseded states. A retry adopts or replaces only its own unpublished generation; it never mutates a published snapshot silently.

Promotion is logical publication, not physical movement. Raw remains raw after standardized succeeds. Standardized remains available after curated publication according to retention. Copy/delete between folder names adds risk without creating semantic assurance.

For multi-input curated products, pin all input snapshots and reference versions. “Latest of each” at different observation times can create a combination that never existed. If synchronized business time matters, define compatible cuts.

### Handle backfill, correction, and rule change

Classify change: new late source fact, source correction, parser defect, standardization rule update, reference-data correction, curated metric change, or platform/runtime difference. Each has a distinct affected range and communication obligation.

Backfill into isolated raw/standardized/curated generations. Compare identities, counts, amounts, quality, and consumer queries with current snapshots. Publish atomically when acceptance passes; retain the old snapshot and code/config/key authority through rollback.

Restatement scope follows lineage and time. A country-code mapping correction may affect standardized rows and every curated product using that dimension. A metric definition change may require a new product contract/version rather than rewriting historical meaning under the same name.

Make finality explicit. “Preliminary through watermark/date X” and “closed subject to adjustment” are different. Late data may revise current snapshots, create adjustment facts, or await the next reporting cycle according to business/regulatory rules.

### Apply governance across, not after, layers

Classification follows data. Standardization can reduce exposure by tokenizing or removing fields, but joins can also increase identifiability. Curated aggregation can reduce risk only when small groups, drill-through, and auxiliary information are considered.

Separate service roles by edge: source-to-landing, landing-to-raw, raw-reader/standardized-writer, standardized-reader/curated-writer, publisher, analyst, steward, quarantine repair, lifecycle, and permanent delete. Consumers should not automatically receive raw access.

Enforce catalog and underlying storage permissions coherently. Provider governance tools may offer row/column/cell or tag-based control, but direct object access can bypass a catalog policy if storage permissions remain broad. Test every access path.

Propagate purpose, consent, residency, retention, legal hold, and erasure identifiers through lineage. A derived product needs a policy for deleting or recomputing affected rows and snapshots. Retention is not simply longer upstream and shorter downstream; legal and operational horizons interact.

### Model cost and avoid layer theater

For raw, standardized, curated, quarantine, historical snapshots, and replicas, approximate stored bytes as

$$
S_{total}=S_R+S_S+S_C+S_Q+S_H+S_{replica}.
$$

Total cost also includes ingestion/transform compute, scans, requests, catalogs, lineage, quality evaluation, compaction, encryption, transfer, repair, operations, and consumer support. A reusable standardized product can reduce repeated compute even while adding storage.

Materialize when it supplies recovery, reuse, performance, governance, isolation, or stable interface value. Virtualize or combine edges when recomputation is cheap and contracts remain observable. Never retain an intermediate forever because its path has an official-sounding layer name.

Track product usage, dependent products, last access, recompute cost, storage/compute/request cost, incident load, and owner. Deprecate unused products through dependency evidence and retention policy rather than accumulating abandoned “gold.”

### Observe and reconcile the whole flow

For every compatible cut, report source/landing input, raw admitted/rejected/quarantined, standardized accepted/duplicate/conflict/invalid, curated included/excluded, and unexplained residue. Diagnostic labels may overlap; primary dispositions must not.

Measure freshness separately at acquisition, standardization, and curated publication. A fresh raw feed can coexist with stale curated output. Completeness, validity, uniqueness, consistency, and accuracy require separate evidence.

Operational metrics include bytes/records/snapshots; input/output ratios; schema drift; rule failures; duplicate/conflict rate; quarantine count/age; reference misses; job lag/retry/failure; publish conflicts; lineage gaps; consumer SLO; access denials; erasure backlog; file shape; and cost per product/use.

Use control totals beyond counts when stakes justify them: sum of signed minor units, sequence ranges, distinct occurrence identities, partition coverage, null profiles, and source-provided totals. Reconcile at named snapshots and document expected exclusions.

## Definitions and Notation

For one finite processing scope, define:

- $I$: authenticated intake observations at a declared source cut.
- $R$: observations admitted to governed raw.
- $J$: landing rejections that never qualify for raw admission.
- $Q_0$: intake-security or envelope quarantine.
- $S$: standardized accepted occurrences.
- $D$: exact duplicate dispositions.
- $Q_1$: standardization invalid/conflict quarantine.
- $C_{p,r}$: curated snapshot revision $r$ for product $p$.
- $T_v$: standardization function under rule contract $v$.
- $F_{p,r}$: curated transformation under product-rule revision $r$.
- $g_i$: exact input snapshot identifiers.
- $E_r$: declared exception/exclusion policy and evidence.
- $L$: lineage graph of dataset snapshots and transformation executions.

Intake accounting is

$$
|I|=|R|+|J|+|Q_0|.
$$

Standardized primary dispositions form a disjoint union:

$$
T_v:R\rightarrow S\uplus D\uplus Q_1,
$$

so

$$
|R|=|S|+|D|+|Q_1|.
$$

Curated output is reproducible only when inputs and rules are pinned:

$$
C_{p,r}=F_{p,r}(S_{g_1},\ldots,S_{g_n},E_r).
$$

For aggregate group $a$ and accepted standardized occurrence $x$ with measure $m(x)$:

$$
count(a)=\sum_{x\in S}\mathbf{1}[group(x)=a],
$$

$$
total(a)=\sum_{x\in S}\mathbf{1}[group(x)=a]m(x).
$$

This is valid only when $m$, group, grain, inclusion, time, unit, and duplicate/correction semantics are defined.

Layer storage is approximately

$$
S_{total}=S_R+S_S+S_C+S_Q+S_H+S_{replica}.
$$

The fidelity invariant is:

> For every admitted raw identity, the platform can retrieve the received bytes or declared lossless envelope and its acquisition coordinates under applicable retention and access policy.

The conformance invariant is:

> The same pinned raw cut, rule/reference versions, configuration, and deterministic runtime semantics produce the same standardized identities, values, and dispositions.

The product invariant is:

> Every curated value traces to pinned standardized identities and a versioned product contract that defines grain, formula, population, time, exceptions, and owner.

## Mechanisms, Invariants, or Proof Structure

Use this review sequence:

1. **Map local layers.** Name landing/raw/standardized/curated/quarantine concepts and physical/catalog/security boundaries.
2. **Define cuts and identity.** Record source closure, positions, object versions, occurrence/entity identity, fingerprints, and correction relation.
3. **Protect raw fidelity.** Preserve bytes/envelope and acquisition evidence; declare permitted transformations, admission, retention, and restricted readers.
4. **Version conformance.** Specify schemas, types, nulls, time, units, codes, references, duplicates/conflicts, deletes, and quality dispositions.
5. **Own exceptions.** Give quarantine reason, evidence, access, owner, SLA, repair/replay path, and reconciliation denominator.
6. **Contract curated products.** State consumer, decision, grain, population, measures, dimensions, time, SLOs, access, and deprecation.
7. **Pin lineage/publication.** Record exact snapshots/code/config/references/results and publish new outputs atomically.
8. **Plan change.** Isolate backfill/restatement, compute affected lineage/range, compare, approve, publish, communicate, and roll back.
9. **Govern and cost.** Propagate classification/retention/erasure and justify each materialization with use, recovery, performance, or control value.
10. **Reconcile and fault-test.** Partition every input, verify control totals, and inject schema, reference, identity, partial publish, access, and replay failures.

Proof sketch for no silent standardization loss:

1. Fix raw snapshot $R_g$ and transformation contract $T_v$.
2. Assign every raw observation one canonical occurrence identity and semantic fingerprint or an explicit identity-invalid reason.
3. Evaluate validation and retained-identity rules in deterministic precedence.
4. Emit exactly one primary disposition: accepted standardized, exact duplicate, or quarantine.
5. Commit accepted output, disposition ledger, and source cut under one published run result.
6. Reconcile identities and counts, requiring $|R_g|=|S|+|D|+|Q_1|$.
7. Any missing or multiply classified raw identity violates publication and prevents promotion.

This proves accounting under the declared classification and atomic-publication assumptions. It does not prove the source is complete, the rules are correct, a quarantined obligation is repaired, or the curated product is fit for every use.

The following executable models immutable raw observations, canonical standardization, exact duplicate versus identity conflict, quarantine, curated country totals, lineage, and disposition reconciliation. Its supplied payloads and rules are illustrative; it does not prove real source completeness, currency semantics, storage atomicity, access control, or business fitness.

<!-- bijux-verify: {"id":"zone-disposition-lineage","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"decisions=((10, 'e1', 'standardized'), (11, 'e1', 'exact_duplicate'), (12, 'e2', 'invalid_amount'), (13, 'e3', 'standardized'), (14, 'e3', 'identity_conflict'))\nstandardized=(('e1', 'o1', 'US', 1250), ('e3', 'o2', 'CA', 700))\nquarantine=(('e2', 'invalid_amount'), ('e3', 'identity_conflict'))\ncurated=(('CA', 1, 700), ('US', 1, 1250))\nlineage=(('CA', ('e3',)), ('US', ('e1',)))\ncounts=(('exact_duplicate', 1), ('identity_conflict', 1), ('invalid_amount', 1), ('standardized', 2))\nraw_count_reconciles=True\n","stderr":""}} -->
```python
raw = (
    {"position": 10, "event": "e1", "order": "o1", "country": " us ", "amount": "12.50"},
    {"position": 11, "event": "e1", "order": "o1", "country": " us ", "amount": "12.50"},
    {"position": 12, "event": "e2", "order": "o-bad", "country": "GB", "amount": "twelve"},
    {"position": 13, "event": "e3", "order": "o2", "country": "ca", "amount": "7.00"},
    {"position": 14, "event": "e3", "order": "o2", "country": "ca", "amount": "8.00"},
)


def fingerprint(record):
    return tuple((key, record[key]) for key in ("event", "order", "country", "amount"))


def parse_cents(text):
    pieces = text.split(".")
    if len(pieces) not in (1, 2) or not all(piece.isdigit() for piece in pieces):
        raise ValueError("invalid_amount")
    fraction = "00" if len(pieces) == 1 else pieces[1]
    if len(fraction) != 2:
        raise ValueError("invalid_amount")
    return int(pieces[0]) * 100 + int(fraction)


seen = {}
standardized = []
quarantine = []
decisions = []
for record in raw:
    event = record["event"]
    observed = fingerprint(record)
    if event in seen:
        decision = "exact_duplicate" if seen[event] == observed else "identity_conflict"
        if decision == "identity_conflict":
            quarantine.append((event, decision))
        decisions.append((record["position"], event, decision))
        continue
    seen[event] = observed
    try:
        cents = parse_cents(record["amount"])
        country = record["country"].strip().upper()
        if len(country) != 2 or not country.isalpha():
            raise ValueError("invalid_country")
    except ValueError as error:
        decision = str(error)
        quarantine.append((event, decision))
    else:
        decision = "standardized"
        standardized.append((event, record["order"], country, cents))
    decisions.append((record["position"], event, decision))

groups = {}
for event, _, country, cents in standardized:
    count, total, events = groups.get(country, (0, 0, ()))
    groups[country] = (count + 1, total + cents, events + (event,))
curated = tuple((country, values[0], values[1]) for country, values in sorted(groups.items()))
lineage = tuple((country, values[2]) for country, values in sorted(groups.items()))
counts = {}
for _, _, decision in decisions:
    counts[decision] = counts.get(decision, 0) + 1

print(f"decisions={tuple(decisions)}")
print(f"standardized={tuple(standardized)}")
print(f"quarantine={tuple(quarantine)}")
print(f"curated={curated}")
print(f"lineage={lineage}")
print(f"counts={tuple(sorted(counts.items()))}")
print(f"raw_count_reconciles={sum(counts.values()) == len(raw)}")
```

The model counts the malformed first occurrence as invalid and a later conflicting reuse as quarantine. A production contract must decide whether exact retries of invalid records share the first disposition, remain separate attempts, or await source correction.

## Alternatives and Trade-Offs

**Three layers versus domain-specific products.** Three named layers teach responsibilities and create shared operations. Domain product graphs avoid forced copies and central bottlenecks but require strong interoperable contracts, catalogs, and governance.

**Separate buckets/accounts versus schemas/namespaces.** Physical separation strengthens access, lifecycle, billing, and blast-radius boundaries. Logical separation simplifies sharing and operations. Sensitive landing/raw or permanent-delete authority may justify stronger isolation.

**Preserve original bytes versus canonical envelope.** Original bytes maximize forensic fidelity but add format, security, and storage burden. A lossless envelope improves queryability only if its transformation is fully reversible and the original transport evidence is not required.

**Schema-on-read raw versus parsed raw tables.** Byte-oriented raw tolerates unexpected change and enables parser replay. Parsed raw improves immediate discovery but can freeze lossy interpretations. Retain evidence and make parsing versioned either way.

**Strict reject versus permissive capture.** Strict admission protects downstream contracts but risks losing novel fields/records. Permissive raw capture preserves evidence but increases security and operational risk. Separate safe intake from semantic validation.

**Drop duplicates versus retain dispositions.** Suppression reduces downstream work. A durable receipt/disposition preserves evidence for reconciliation, conflict detection, horizon change, and audit.

**Quarantine versus nullable acceptance.** Quarantine protects a strong contract but delays partial utility. Explicit nullable/unknown semantics can preserve valid portions when consumers tolerate them. The product contract, not convenience, chooses.

**Global canonical model versus domain conformance.** One enterprise model encourages interoperability but can become slow and semantically weak. Domain models preserve ownership and evolution but need mappings for cross-domain products.

**Materialized standardized layer versus transformation-on-read.** Materialization improves reuse, isolation, quality evidence, and predictable performance at storage/compute cost. Virtualization avoids copies but repeats work and can make reproducibility/failure boundaries harder.

**Shared curated layer versus consumer products.** Shared metrics reduce duplication when definitions truly align. Consumer-owned products allow purpose-specific grain and SLOs but require governance to avoid contradictory unnamed definitions.

**Mutable current tables versus immutable snapshots.** Mutable tables offer convenient latest state. Immutable snapshots/history enable reproducibility and rollback. Transactional table metadata can provide both views when operated correctly.

**Recompute versus incremental promotion.** Full recompute is simple and strong for bounded datasets. Incremental work reduces cost/latency but needs change identity, deletes, late corrections, checkpoints, and reconciliation.

**Long raw retention versus minimization.** Long retention improves replay/audit and model rebuilding. It increases cost, privacy exposure, and breach impact. Derive duration from source replay, correction, recovery, legal, and erasure obligations.

## Failure Modes and Misconceptions

1. **“Raw means ungoverned.”** Raw needs the strongest fidelity, access, retention, and provenance controls because it contains unexpected source content.
2. **“Raw is truth.”** It proves receipt under a cut, not correctness, completeness, authority, or lawful use.
3. **“Landing and raw are identical.”** Landing may contain unauthenticated, encrypted, unsafe, or transient transfers that have not met raw admission.
4. **“Bronze/silver/gold paths implement architecture.”** Names without contracts, ownership, tests, lineage, access, and publication are decoration.
5. **“Every record must move through three folders.”** Logical products can remain in place; movement is not promotion and unnecessary copies add risk.
6. **“Parsing is harmless.”** Type, encoding, timezone, decimal, and default decisions can be lossy. Preserve source evidence and version rules.
7. **“Unknown equals null.”** Missing, invalid, redacted, not applicable, and unknown carry different semantics and obligations.
8. **“Payload equality means duplicate.”** Equal legitimate occurrences exist; conflicting reuse of one ID also exists. Use canonical occurrence identity plus fingerprint.
9. **“Quarantine means handled.”** Without an owner, SLA, repair path, metrics, and reconciliation, it is delayed silent loss.
10. **“A quality score is a gate.”** An average score can hide critical invalid records. Record predicate-level dispositions and thresholds.
11. **“Standardized means business-ready.”** Canonical detail may lack consumer grain, formulas, finality, performance, or decision context.
12. **“Curated means aggregated.”** Detailed purpose-built facts can be curated; arbitrary aggregates can remain untrustworthy.
13. **“Gold is universally correct.”** Fitness is scoped to named consumers, versions, time, assumptions, and acceptance evidence.
14. **“Latest reference data is fine on replay.”** It makes results time-dependent. Pin reference snapshots or define as-of semantics.
15. **“A job name is lineage.”** Reproduction needs exact input/output snapshots, code/config/rules/references, run, and quality evidence.
16. **“Counts reconcile correctness.”** Duplicate/missing cancellation and wrong amounts can preserve counts. Add identities and control totals.
17. **“Downstream is less sensitive.”** Conformance and joins can make records more identifiable; curated inferences can be sensitive.
18. **“Catalog policy protects object storage automatically.”** Direct storage permissions may bypass row/column controls. Test integrated and direct paths.
19. **“Backfill can write into current partitions.”** Live and historical attempts can interleave. Use isolated generations and atomic publication.
20. **“Deleting raw after curation saves harmlessly.”** It can destroy replay, correction, audit, or evidence before the required horizon.
21. **“Keep every layer forever.”** Unused duplicates increase cost and attack surface. Retain by explicit recovery, legal, reuse, and product needs.
22. **“Freshness is end-to-end.”** Each edge can lag independently; report source, raw, standardized, and curated freshness separately.

## Worked Examples

### Example 1

A CSV source adds an unexpected column. Raw stores the original versioned object, header, checksum, and extract manifest. Standardization v4 quarantines affected records as unsupported schema. Parser v5 later replays the same raw snapshot and preserves a complete audit of both outcomes.

### Example 2

A CDC feed sends create, update, and delete records with log positions. Raw retains every envelope. Standardized history preserves typed changes and tombstones; a separate current-state table applies entity versions. Curated active-customer counts use the current-state snapshot but trace to history.

### Example 3

Two identical $10 purchases have different occurrence IDs and both enter standardized facts. One retry repeats an ID and fingerprint and becomes an exact-duplicate disposition. A reuse of that ID with $100 becomes an identity conflict, not a winner chosen by arrival.

### Example 4

A timestamp `2026-11-01 01:30` arrives without offset in a region with a daylight-saving fold. Standardization cannot infer one instant. It retains the raw text and source zone evidence and quarantines or applies a documented source-specific ambiguity rule rather than silently assuming UTC.

### Example 5

Country code `UK` appears where the contract accepts ISO alpha-2 codes. The mapping reference version explicitly maps it to `GB` for a stated source and effective period. An unknown `ZZ` remains unmapped/quarantined; it is not converted to a valid “other” category silently.

### Example 6

A curated daily revenue product declares one row per recognition date, legal entity, and currency; amount excludes tax and includes approved refund adjustments. Because grain and formula are explicit, consumers do not sum a ratio or mix order-date and recognition-date semantics.

### Example 7

Raw receives 1,000 records. Standardization accepts 970, suppresses 12 exact duplicates, quarantines 15 invalid and 3 conflicts. The equality `1000 = 970 + 12 + 18` holds; identity and amount controls then catch a missing-plus-duplicate cancellation a count alone would miss.

### Example 8

A correction to customer-region reference snapshot 8 affects standardized customers and three curated products. Lineage finds exact dependent snapshots. Backfill uses reference snapshot 9 in isolation, compares totals and cohort movement, publishes approved revisions, and retains rollback.

### Example 9

Raw contains direct identifiers under restricted access. Standardized tokenizes customer identity but remains linkable. Curated publishes aggregates, yet cells with tiny cohorts could reidentify people. Access and disclosure controls become stricter rather than assuming gold is public.

### Example 10

An unused standardized copy costs storage and daily compute but has no dependents or recovery value. Dependency, query, incident, and recompute evidence supports deprecation. The team freezes publication, communicates, retains through rollback, removes catalog access, and expires data under policy.

## Cross-Program Connections

- **Database Systems:** schemas, constraints, MVCC snapshots, dimensional grain, temporal tables, transactions, catalogs, and materialized views ground layer contracts.
- **Distributed Systems:** source cuts, idempotence, partial failure, immutable publication, retries, concurrency, checkpoints, and replay determine edge correctness.
- **Information Security:** classification, least privilege, data minimization, tokenization, key administration, tenant isolation, and audit apply to every copy.
- **Privacy Engineering:** purpose limitation, consent, residency, retention, erasure, linkage risk, and small-cohort inference propagate through lineage.
- **Software Engineering:** versioned interfaces, adapters, pure transformations, test fixtures, dependency graphs, semantic versioning, and deprecation make products maintainable.
- **Product Management:** curated products need consumers, decisions, owners, adoption evidence, SLOs, support, and lifecycle—not only technical completion.
- **Data Structures Engineering:** identifiers, fingerprints, disjoint disposition sets, lineage DAGs, indexes, and reachability support reconciliation and impact analysis.
- **Reliability Engineering:** fault injection, finite oracles, backlog/freshness SLOs, recovery horizons, rollback, and incident ownership prevent silent degradation.
- **Economics:** materialization trades storage and maintenance for reuse, isolation, recovery, performance, and reduced repeated compute.
- **Statistics and ML:** population, sampling, leakage, feature time, label correction, aggregation bias, and reproducible training cuts depend on zone semantics.

## References

1. Databricks. [What is the medallion lakehouse architecture?](https://docs.databricks.com/aws/en/lakehouse/medallion). Accessed 2026-09-03. Primary product documentation for bronze/raw, silver/validated, gold/enriched responsibilities and multi-layer quality progression.
2. Amazon Web Services. [Recommended data layers](https://docs.aws.amazon.com/prescriptive-guidance/latest/defining-bucket-names-data-lakes/data-layer-definitions.html). Accessed 2026-09-03. First-party guidance for landing, raw, stage, and analytics layers plus separation and lifecycle considerations.
3. Amazon Web Services. [Data architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/aws-caf-platform-perspective/data-arch.html). Accessed 2026-09-03. First-party guidance for custom raw, curated/domain, product/mart, and externally exposed data zones with governance.
4. Microsoft. [Understand medallion architecture for Fabric with OneLake](https://learn.microsoft.com/en-us/fabric/onelake/onelake-medallion-lakehouse-architecture). Accessed 2026-09-03. Primary documentation for bronze/raw, silver/enriched, and gold/curated responsibilities and deployment boundaries.
5. Microsoft. [What is a data lake?](https://learn.microsoft.com/en-us/azure/architecture/data-guide/scenarios/data-lake). Accessed 2026-09-03. First-party architecture guidance comparing lake and warehouse use and describing raw, cleansed, and curated layers.
6. Amazon Web Services. [What is AWS Lake Formation?](https://docs.aws.amazon.com/lake-formation/latest/dg/what-is-lake-formation.html). Accessed 2026-09-03. Primary documentation for governance, catalog/storage access, audit, row/column/cell controls, and sharing scope.
7. Amazon Web Services. [Methods for fine-grained access control](https://docs.aws.amazon.com/lake-formation/latest/dg/access-control-fine-grained.html). Accessed 2026-09-03. Primary documentation distinguishing catalog/data controls, IAM interaction, and fine-grained permission models.
8. Amazon Web Services. [AWS Lake Formation: How it works](https://docs.aws.amazon.com/lake-formation/latest/dg/how-it-works.html). Accessed 2026-09-03. Primary documentation for metadata authorization, temporary storage credentials, integrated engines, and direct-storage policy interaction.
9. OpenLineage. [About OpenLineage and its specification](https://openlineage.io/docs/). Accessed 2026-09-03. Primary project documentation for job, run, dataset, event, and extensible lineage facets.
10. Debezium. [Change event values](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-change-event-value). Accessed 2026-09-03. Primary connector documentation illustrating before/after, source metadata, operation, and timestamp evidence in CDC envelopes.
11. Apache Iceberg. [Reliability](https://iceberg.apache.org/docs/latest/reliability/). Accessed 2026-09-03. Primary project documentation for atomic table changes, snapshot isolation, optimistic concurrency, and retry behavior above object storage.
12. Apache Iceberg. [Branching and tagging](https://iceberg.apache.org/docs/latest/branching/). Accessed 2026-09-03. Primary project documentation for retained snapshots, audit branches, tags, and write-audit-publish workflows relevant to isolated promotion.

## Exercises

### Exercise 1

Write a complete zone contract for orders from a batch export and CDC feed. Define landing/raw admission, source cuts, immutable evidence, standardization schema/time/identity/delete rules, quarantine, curated product grain/metrics, publication, lineage, access, retention, and reconciliation.

### Exercise 2

For a raw cut of 2,000,000 observations, standardization accepts 1,942,000, classifies 21,000 exact duplicates, 7,000 identity conflicts, and 29,500 invalid records. Reconcile the cut, calculate unexplained residue, and state why a zero residue would still not prove accuracy or source completeness.

### Exercise 3

Design deterministic standardization for timestamps, monetary amounts, country codes, null/missing values, and occurrence identity across three sources. List every rule/reference version required for exact replay and show how unknown or ambiguous values are handled.

### Exercise 4

A reference-data correction changes 18 months of customer regions. Design impact analysis, isolated backfill, validation, consumer acceptance, atomic publication, communication, rollback, and historical semantic-version policy across standardized and curated products.

### Exercise 5

Design a fault and governance test for the complete layer graph. Include partial raw intake, schema drift, duplicate/conflicting IDs, reference lag, quarantine outage, partial output publication, stale catalog, unauthorized direct object access, erasure request, backfill/live collision, and finite reconciliation criteria.

## Answers to the Exercises

### Answer 1

Landing accepts authenticated transfers into a restricted bucket, verifies manifest/checksum and scans content, then expires quickly. Raw publishes immutable batch-manifest and CDC offset-range snapshots containing original bytes/envelopes, source coordinates, schema/header, checksum, connector, run, and classification. Standardized v1 parses explicit field IDs/types, preserves source time plus UTC interpretation, represents cents/currency under named rules, merges batch/CDC by tenant-scoped occurrence and entity versions, retains tombstones, and partitions accepted/exact-duplicate/conflict/invalid. Quarantine has reason, owner, SLA, protected raw reference, and replay. Curated daily recognized revenue declares row grain `(recognition_date, legal_entity, currency)`, formula/exclusions/finality, named consumers, and SLOs. Every edge pins snapshots/code/config/references and atomically publishes. Roles separate intake, raw, transforms, publish, query, repair, lifecycle, and delete. Retention covers source replay/correction/legal/privacy. Counts, identities, source sequences, bytes, and monetary totals reconcile at compatible cuts.

### Answer 2

Classified output is $1{,}942{,}000+21{,}000+7{,}000+29{,}500=1{,}999{,}500$. Unexplained residue is $2{,}000{,}000-1{,}999{,}500=500$, so publication must fail or explicitly account for those identities. If residue were zero, rules could still accept invalid values, misclassify legitimate repeats as duplicates, apply the wrong source cut, use incorrect reference mappings, or omit records never delivered by the source. Validate identity, amounts/control totals, rule semantics, and source completeness independently.

### Answer 3

Preserve each raw value. Pin schema/parser version; timezone source and daylight-fold/gap rule; decimal syntax, currency scale, rounding and conversion-rate snapshot; ISO/code mapping with effective interval; null/missing/empty/redacted vocabulary; tenant/source/type/generation occurrence-ID construction; canonical fingerprint version; and reference snapshots. Emit canonical values only when rules decide unambiguously. Unknown codes remain explicit unmapped or quarantine; local timestamps in a fold require source offset/adjudication; malformed amount is invalid rather than zero; missing is not null unless the source contract equates them; identity reuse with changed fingerprint is conflict. Exact replay includes engine/runtime and deterministic configuration in lineage.

### Answer 4

Use snapshot/column lineage to enumerate standardized customer history and all curated dependents over the affected effective range. Freeze reference snapshot 9 and transformation versions in a separate backfill generation. Recompute, then compare identities, before/after regions, counts, control totals, affected measures, quarantine, representative queries, and privacy/access. Product owners accept expected cohort movement and SLO impact. Publish new standardized and curated snapshot pointers atomically in dependency order or under a coordinated release contract, communicate semantic impact and restatement dates, and retain old snapshots/code/reference/key access through rollback. If region meaning changed rather than incorrect data being repaired, issue a new semantic product version instead of rewriting the old definition invisibly.

### Answer 5

Inject each failure at the edge and assert: incomplete intake never becomes a closed raw cut; drifted bytes remain recoverable; exact duplicate/conflict dispositions are deterministic; missing reference creates owned exception rather than invented value; quarantine unavailability stops or durably buffers according to policy; partial files remain unpublished; catalog readers resolve only accepted snapshots; direct storage access is denied consistently with catalog policy; erasure traces all snapshots/derivatives/replicas subject to holds; and backfill cannot mutate live generations. For compatible finite cuts, require every source/intake identity to have one primary disposition, every accepted downstream identity to trace to pinned input, count and control-total equations to hold, all exceptions to have owners/states, no unauthorized access path, and no unexplained published or missing object/table snapshot.
