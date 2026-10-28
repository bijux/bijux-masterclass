---
module_id: DE-073
program: Data Engineering
level: 2
module_number: 73
title: Reconciliation Tests
status: complete
last_verified: 2026-09-03
---

# Reconciliation Tests

## One-Page Review

### Governing question

How can a team demonstrate that data crossing a pipeline, migration, replication stream, model rewrite, or system boundary preserved the intended population and values when source and target schemas, grains, clocks, duplicates, transformations, and commit mechanisms differ?

### Essential definitions

- **Reconciliation** compares independently identified source and target states under a declared mapping and equivalence relation.
- A **reconciliation cut** is a coordinated source boundary and target version/checkpoint representing the same intended logical work.
- A **transformation contract** defines how source records, reference data, filters, deduplication, joins, currency/unit conversion, aggregation, and defaults produce target records.
- **Exact reconciliation** proves equality under a specified canonical representation; **tolerant reconciliation** permits declared differences such as rounding or bounded lateness.
- A **control total** is an independently obtained count, sum, or other aggregate associated with a population or batch.
- **Record-count reconciliation** compares counts at aligned grains/cohorts; equal counts alone do not prove equal membership.
- **Key-set reconciliation** finds identities present on only one side; **key-multiset reconciliation** also preserves duplicate multiplicity.
- **Row/field reconciliation** aligns records by a trustworthy key and compares canonicalized values or derived invariants.
- A **canonicalization profile** fixes field order, types, encodings, Unicode, timezone, decimal/float treatment, null markers, arrays/maps, duplicates, and digest algorithm.
- A **reconciliation vector** combines schema, population, key, aggregate, row/field, and continuity evidence rather than relying on one scalar.
- A **high-water mark/checkpoint** records the greatest source position included in a target state under a named ordering.
- A **barrier** establishes a boundary between snapshot and change processing so gaps and overlaps can be detected or deduplicated.
- A **pending difference** may be explained by a documented propagation window; a **mismatch** remains after alignment and tolerance.
- A **difference classification** distinguishes missing source, missing target, extra, duplicate, conflicting value, schema/mapping, pending, excluded, and unknown.
- A **reconciliation ledger** stores immutable run identity, cuts, versions, rules, counts, differences, disposition, corrections, and approvals.

### Central model, mechanism, or theorem

Let source snapshot $S_a$, target snapshot $T_b$, and versioned transformation $F_c$ be pinned. The desired relation is

$$
T_b\equiv_M F_c(S_a),
$$

where $M$ defines grain, scope, key, canonicalization, tolerances, and expected exclusions. A reconciliation vector may be written

$$
R=(SchemaDiff,CountDiff,KeyDiff,AggregateDiff,RowDiff,ContinuityDiff,Coverage).
$$

A passing component proves only its covered property. Equal row count and equal sum do not prove row equality: source amounts $(40,60)$ and target amounts $(50,50)$ have count two and sum 100 but disagree at both keyed rows. Exact keyed canonical comparison is stronger, provided cuts, keys, mappings, canonicalization, and evaluation are correct and complete.

### Critical invariants

- Every run pins source identity/version/cut, target identity/version, transformation/code/configuration, references, and reconciliation specification.
- Source and target represent the same business scope, effective interval, timezone, grain, filters, and completion boundary before comparison.
- Counts and sums are segmented by meaningful cohorts so offsetting errors cannot disappear in global totals.
- Keys are present, canonicalized, unique at the declared grain, and compared as multisets when duplicates matter.
- Row canonicalization is deterministic, versioned, cross-engine tested, and keeps absent, null, empty, default, and not-applicable distinct.
- Hashes accelerate equality checks but never remove the need for algorithm/profile identity, collision policy, exact drill-down, and protected inputs.
- Numeric tolerances specify units, rounding order/mode, absolute/relative bounds, and treatment of NaN, infinities, and signed zero.
- Snapshot-plus-CDC reconciliation proves a gap-free/overlap-safe handoff and continuous source-position coverage.
- Incremental reconciliation includes late updates, deletes, corrections, affected aggregates, and source/target checkpoint state.
- Pending, mismatch, excluded, and unknown states remain distinct; elapsed time alone does not turn unknown into pass.
- Reconciliation execution failure or partial coverage cannot produce a successful result.
- Automated resync/correction is idempotent, scoped, authorized, attributable, and followed by a fresh comparison.
- Raw evidence and target history are preserved; differences are not hidden by overwriting both sides or changing tolerances.
- Sensitive row differences are minimized, encrypted, access-controlled, and retained under policy.
- Periodic full reconciliation re-anchors incremental evidence and validates its maintained state.

### Common failures

Common failures include comparing a live source with a stale target; using extraction time as event cutoff; reconciling different grains; filtering one side only; joining before checking duplicate keys; using an inner join that hides missing records; treating equal counts or sums as equality; allowing positive and negative errors to cancel; hashing without canonicalization; concatenating fields ambiguously; ignoring null/default differences; using approximate counts for a zero-loss claim; sampling rare missing keys; omitting deletes from CDC; losing the snapshot-to-log boundary; trusting a checkpoint whose target commit failed; repairing the target before preserving evidence; and continually adjusting tolerance until the test passes.

### Compact example

Source cut S17 has order A for 40 and B for 60. Target version T22 has A for 50 and B for 50. Both contain two rows, their key sets match, and both amount totals equal 100. A full outer keyed comparison nevertheless finds conflicting values for A and B. After a supported repair publishes T23 with 40 and 60, exact canonical rows match. The initial aggregate checks were useful smoke tests, but only the drill-down located the offsetting defects.

### Connections

[DE-023](023-file-arrival-and-manifest-processing.md) establishes source control totals, [DE-030](030-designing-replayable-raw-ingestion.md) preserves raw lineage, [DE-036](036-merge-and-upsert-semantics.md) defines key and mutation behavior, [DE-049](049-run-metadata-and-operational-state.md) identifies executions, [DE-060](060-handling-late-duplicate-and-out-of-order-events.md) handles stream disorder, [DE-066](066-time-travel-and-reproducible-reads.md) pins versions, and [DE-071](071-completeness-validity-accuracy-and-consistency.md) plus [DE-072](072-schema-and-constraint-tests.md) define quality evidence. DE-074 adds freshness semantics.

## Governing Question

A pipeline can finish successfully while silently losing, duplicating, filtering, truncating, or misassigning data. Task completion proves that code ran, not that the target represents the intended source population. Reconciliation closes that gap by comparing independently identified states.

The comparison is rarely raw table equality. A migration may preserve rows exactly; a dimensional model intentionally joins and aggregates; a CDC sink retains only current state; a currency model converts units; a privacy pipeline suppresses fields. The transformation contract defines what equality means.

Timing is the hardest source of false alarms and false passes. A live source changes while a target catches up. Snapshot rows overlap streamed events. Late corrections affect past dates. A target checkpoint can advance before its data commit or vice versa. A credible test establishes a cut both systems can prove.

The governing requirement is a reproducible reconciliation vector over pinned evidence, followed by classified differences and controlled remediation. Operators must know which property each component proves, where it is approximate, what remains pending or unknown, and when incremental assurance must be reset by a full comparison.

## Why This Matters

Reconciliation detects classes of defect that local validation misses. Every target row can satisfy its schema while an entire partition is absent. Counts can match while identities differ. Totals can balance while values move between customers. CDC can preserve event syntax while skipping a log interval.

Financial systems institutionalize control totals because conservation matters, but reconciliation is broader than accounting. Orders, inventory, entitlements, telemetry, model features, and regulatory reports all have quantities or identities that should survive specific transformations.

Large datasets create pressure to accept cheap evidence. Counts, sums, sketches, and hashes reduce scan and transfer cost. Used in layers, they localize work efficiently. Used as universal proof, they conceal collisions, cancellation, canonicalization bugs, and uncovered cohorts.

Repair can compound damage. A resync based on a changing source can overwrite legitimate target changes. Replaying CDC without idempotency can duplicate effects. Correcting before evidence capture destroys the trail needed to explain impact. Reconciliation and repair need transactional boundaries and ownership.

Difference artifacts are sensitive. They can include identifiers, financial amounts, health facts, deleted records, or security state. The evidence system must minimize values while retaining enough information for authorized drill-down and audit.

## Prerequisites and Retrieval

Retrieve purpose: migration/replication/model/rewrite being verified, consumers, business invariants, materiality, zero-loss requirements, tolerances, regulatory duties, freshness window, escalation, and owners.

Retrieve source: system/dataset/table identity, schema and semantics, snapshot/version/log position, transaction boundaries, extraction query, filters, expected manifests, keys, duplicates, deletes, effective times, control totals, and retention.

Retrieve target: stable identity, snapshot/version/commit, schema, load job/transaction, write mode, keys, deduplication, partitions, indexes, visibility, history, and concurrent writers.

Retrieve transformation: code/configuration/dependencies, field mapping, normalization, filters/exclusions, joins, reference/master versions, aggregations, units/currency, rounding, null/default/imputation, late-data policy, error/quarantine paths, and nondeterminism.

Retrieve cut semantics: snapshot acquisition, log/checkpoint/LSN/offset range, event/processing/commit time, inclusive/exclusive endpoints, watermark, source and target barriers, clock/timezone, propagation allowance, and proof of completion.

Retrieve reconciliation specification: grain, key and canonicalization, cohorts, count definitions, aggregates, row fields, tolerances, hash algorithm/profile, sample/exact method, coverage, severity, and disposition.

Retrieve CDC state: connector/task identity, source slot/publication or log, offsets, snapshot mode, transaction/event IDs, topic/partition offsets, sink checkpoints, deduplication, tombstones/deletes, schema history, retries, and retention gaps.

Retrieve execution: engine/library/version, queries/plans, input versions, partitions/bytes/rows scanned, spill/resources, timeouts, permissions, result caps, retries, and failures.

Retrieve repair: source-of-truth authority, resync mechanism, conflict with target-owned fields, batch scope, idempotency, pause/fence procedure, approval, rollback, downstream replay, and post-repair test.

Distinguish source from system of record; extract cut from wall-clock time; set from multiset; entity from event grain; source row from transformed expected row; missing target from target-intended exclusion; pending from mismatch; exact compare from hash evidence; operational consistency from real-world accuracy; offset stored from data committed; and resync from proof.

Create a reconciliation contract:

| Concern | Required decision and evidence |
|---|---|
| Identity | Source/target UUIDs and versions, run ID, transform/reference/spec versions |
| Cut | Snapshot and change boundaries, clocks, endpoints, barrier, completion and retention |
| Semantics | Grain, keys, filters, mapping, units, rounding, null/default and exclusions |
| Vector | Schema, counts, key multiset, aggregates, row/field, continuity and coverage |
| Tolerance | Exact/absolute/relative, cohort materiality, propagation window and severity |
| Differences | Missing/extra/duplicate/conflict/pending/excluded/unknown classification |
| Action | Gate, alert, quarantine, investigate, resync, correct, revalidate and notify |
| Evidence | Queries/digests, counts, protected samples, approvals, history and retention |

Write a falsifiable claim: “Reconciliation run R81 compares source snapshot S17 plus WAL interval $(L100,L145]$ with target snapshot T22 at committed sink checkpoint L145 using transformation C9/reference X4; schema, row counts, key multisets, six control totals, and canonical rows match in every tenant/day cohort with zero pending/unknown records and 100% scan coverage; snapshot/log overlap deduplicates by transaction-key identity, deletes are included, SHA profile H3 is cross-engine qualified and exact drill-down is available, and quarterly full runs validate daily incremental state.”

## Learning Objectives

After completing this module, you should be able to:

1. define source/target identities, pinned cuts, transformation versions, and intended equivalence;
2. design layered schema, count, key, aggregate, row, and continuity reconciliation;
3. distinguish sets from multisets and validate key uniqueness before keyed comparison;
4. specify deterministic canonicalization and safe uses and limits of hashes;
5. align grains, filters, clocks, units, currencies, nulls, rounding, and references;
6. prove gap-free, overlap-safe snapshot-to-CDC handoff and checkpoint/data atomicity;
7. design incremental reconciliation that handles updates, deletes, late data, and affected aggregates;
8. classify differences and unknowns for efficient diagnosis without hiding evidence;
9. automate bounded idempotent repair with authorization, fencing, and post-repair validation; and
10. operate reconciliation with coverage, SLOs, privacy, periodic full anchors, and auditability.

## Core Exposition

### Establish independently identifiable cuts

Pin both sides. A source database snapshot may be identified by transaction snapshot, SCN, LSN, timestamp plus isolation guarantee, or exported version. A lake table uses a snapshot/log/timeline version. The target uses its committed table version and sink checkpoint. Store stable system and dataset identities as well as friendly names.

A timestamp alone is weak: source and target clocks differ, transactions span time, and commit visibility is discrete. Prefer source-native positions and atomic snapshots. State endpoint inclusion, such as $(L_{start},L_{end}]$.

For snapshot plus CDC, record the source position associated with the snapshot. Start retaining changes before or at that boundary, load the snapshot, then apply changes with a deterministic overlap rule. If the boundary is exclusive on both sides, a gap loses events; inclusive on both without deduplication duplicates them.

Checkpoint and target commit must form one recoverable protocol. A checkpoint ahead of data skips work after restart. Data ahead of checkpoint replays work and therefore needs idempotency. Reconciliation should compare committed target evidence with the exact recorded source interval, not connector process status.

If a live comparison is unavoidable, introduce a barrier or classify expected propagation as pending. Re-evaluate after the window. Do not make the tolerance so broad that permanent loss is forever “still catching up.”

### Define expected transformation semantics

Write $F_c$ as a versioned contract, not “the ETL.” Identify input/output grain and mapping for every target field. Record filters, rejected/quarantined rows, deduplication winner, joins and cardinalities, reference versions, aggregations, units, timezone, currency/rate date, rounding, defaults, and late corrections.

The expected side should be derived independently enough to find production defects. Reusing the same materialized target, buggy helper, or unchecked generated query can reproduce the error on both sides. Independent implementation, source control totals, and invariant diversity reduce common-mode failure.

Intentional differences must be enumerable. Privacy suppression, test accounts, cancellations, and invalid quarantined records should appear in an exclusion ledger with rule/version/count, not disappear from a WHERE clause. Reconcile source = target + quarantine + approved exclusions where applicable.

Align types before values. Normalize character encoding and Unicode only under business semantics. Convert timestamps to a named instant/timezone and preserve ambiguity policy. Quantize decimals after specifying rounding order/mode; avoid silently casting exact decimal to float.

### Build a layered reconciliation vector

Start with schema and metadata: fields/IDs/types, partitions, table version, transformation and reference identities. A mismatch can invalidate every downstream comparison.

Compare row and distinct-key counts globally and by cohorts such as tenant, source, event date, partition, status, and currency. Let

$$
\Delta N_c=N_T(c)-N_{F(S)}(c).
$$

Global zero can hide one missing and one extra cohort. Preserve both counts and the definition of a row after deduplication/aggregation.

Control totals use conserved or predictably transformed measures: amount, quantity, debit/credit, min/max sequence, event-count by type. Compare multiple independent aggregates and cohort them. Signed sum can cancel, so include absolute amounts, positive/negative components, counts, and key evidence where useful.

Compare key multisets. For unique keys, a full outer join classifies source-only, target-only, and matched. First test uniqueness; otherwise joining duplicate groups can multiply rows and corrupt mismatch counts. For event streams, composite identity may include source partition/offset or transaction/sequence.

Then compare rows/fields for matched keys. Produce per-column mismatch counts and bounded protected examples. Exact relations can use a multiset difference in both directions. Transformed relations compare mapped values/invariants rather than raw bytes.

### Canonicalize and hash deliberately

A row digest is meaningful only after canonicalization. Specify schema/field IDs and order, length framing or structured serialization, encoding, Unicode normalization, case, whitespace, numeric representation, decimal scale, float edge cases, timestamp/timezone, null/absent/default markers, arrays/maps ordering, binary values, and schema/profile version.

Naive concatenation is ambiguous: `('ab','c')` and `('a','bc')` collide before hashing without lengths or separators that cannot appear unescaped. Use canonical structured encoding with explicit types and boundaries.

Record the cryptographic hash algorithm and implementation. A digest has collision risk; a noncryptographic sum/XOR can permit cancellation or duplicate parity effects. Salt/key decisions affect cross-system reproducibility and security. Never expose stable unsalted hashes of low-entropy sensitive values as if anonymized.

Use hierarchical hashes: row digest, bucket/partition digest, then table summary. A differing bucket narrows exact comparison. A matching digest provides high-confidence evidence under the algorithm/profile and complete scan; it does not correct wrong cuts or shared canonicalization bugs.

Cross-engine golden fixtures must match exact digest bytes for nulls, Unicode, decimals, timestamps, arrays/maps, and boundaries. Retain exact drill-down or replay access for mismatches.

### Reconcile duplicates, deletes, and change streams

Snapshot equality loses event history. Two sequences can end at the same current state while one omitted and later compensated for a change. If audit/event completeness matters, reconcile the change log as well as endpoint state.

CDC events need stable identity, source transaction/order, operation, before/after semantics, and schema version. Include inserts, updates, and deletes/tombstones. Reconcile source log-position coverage per partition/slot and target-applied checkpoints, then key/event multisets and materialized endpoint state.

At-least-once recovery can duplicate events. Deduplicate by stable source event/transaction identity, not target arrival time. Exactly-once claims are bounded by source connector, transport, sink transaction, and checkpoint protocol; retrieve behavior during failure.

Incremental queries can expose latest changed state rather than every change. Delta change data feed only records after enablement and follows retention. Hudi distinguishes latest-state incremental and CDC semantics. Select the feed that matches the reconciliation claim and retain it long enough to cover outages.

Late events and corrections affect past cohorts and aggregates. Track affected keys/windows and reopen reconciliation states. A daily “closed” result is provisional if the business accepts later effective-dated changes; version each result rather than overwriting it.

### Design full and incremental reconciliation

Full comparison establishes a baseline and tests all retained scope. It is expensive but catches drift in maintained indexes, missed changes, and old rows affected by new mapping. Run it at migration gates, after recovery/config/rule changes, periodically, and when incremental evidence becomes suspect.

Incremental comparison consumes committed changes since a trusted checkpoint. For each interval, reconcile event continuity, source changes, transformed expected effects, target changes, deletes, and resulting aggregates. Update the reconciliation state atomically after the target and evidence commit.

Maintain exact per-key or cohort states where feasible. If a reference or transformation changes, determine affected historical keys; “no new source rows” does not mean no changed expectation. Rebuild when the dependency cannot enumerate impact.

Sampled row comparisons help monitor very large populations but cannot prove zero loss. Approximate distinct counts/sketches can detect divergence within error but cannot satisfy an exact key-set invariant. Label probability/error and escalate anomalies to exact scoped comparison.

Use a tiered schedule: per-batch manifest/control totals, continuous offset and cohort checks, daily exact changed-key comparison, and periodic full multiset reconciliation. Each tier has a detection SLO and escalation boundary.

### Classify and investigate differences

Use a full outer model and classify before repair:

- `missing_target`: expected source-derived key absent from target;
- `extra_target`: target key not justified by source/mapping/exclusion;
- `missing_source`: target record remains but source authority no longer contains it;
- `duplicate`: multiplicity exceeds declared grain;
- `value_mismatch`: matched key with non-equivalent fields/invariants;
- `pending`: within proven propagation/late-parent window;
- `excluded`: matched approved rule and exclusion ledger;
- `unknown`: comparison could not be completed; and
- `schema_or_mapping`: definitions cannot be aligned safely.

Record counts by cohort and field, first/last observed time, source/target versions, and protected sample references. Preserve the raw mismatch before re-querying live systems, because the evidence can disappear as they advance.

Common diagnoses include wrong cut, missing partition/file, filter drift, join multiplicity, key normalization collision, target overwrite, truncated/cast values, timezone/rate mismatch, dropped delete, duplicate replay, stale reference, schema evolution, uncommitted target, and reconciliation query bug.

Use bidirectional lineage to identify affected upstream inputs and downstream products. Reconciliation is a safety control; its own code, credentials, and reference data require testing and monitoring.

### Gate, repair, and communicate

Define severity by business impact and evidence strength. A zero-tolerance missing-payment key may block. A bounded rounding difference may warn. Unknown execution on a critical run should hold rather than pass. Pending has an expiry that converts unresolved differences to mismatch.

Automated repair is a privileged writer. Fence competing changes or use conditional/idempotent updates. Define authoritative fields because the target may own enrichments absent at source. Bound records/bytes/time, dry-run, approve destructive changes, and retain before/after versions.

Resync from pinned source evidence where possible. If the source remains live, use version/transaction preconditions so repair does not overwrite a newer legitimate state. Never delete target-only rows until mapping, retention, legal hold, and ownership prove they are invalid.

After repair, run a new reconciliation against new pinned versions, verify unaffected controls, restart/advance checkpoints safely, and notify consumers about corrected versions and replay needs. Do not change the original failed result.

Operate dashboards for last successful cut, checkpoint lag, pending age, counts by classification/cohort, aggregate deltas, full-run age, scan coverage, execution failures, repair volume, recurrence, cost, and SLO. Owners include source, transformation, target, platform, and business steward.

## Definitions and Notation

Let:

- $S_a$ be source state at cut $a$;
- $T_b$ be target state/version $b$;
- $F_c$ be transformation plus configuration/reference version $c$;
- $M$ be mapping, grain, canonicalization, tolerance, and exclusion semantics;
- $K(X)$ be a key multiset, not merely a set;
- $N_X(g)$ be record count in cohort $g$;
- $A_X^j(g)$ be control aggregate $j$ for cohort $g$;
- $Canon_M(x)$ be canonical bytes for row $x$;
- $H_p(x)$ be a digest under profile $p$;
- $L_s$ and $L_t$ be source included and target applied positions;
- $D_R$ be classified reconciliation differences; and
- $Coverage_R$ be evaluated versus intended scope.

For unique keyed exact reconciliation:

$$
Missing_T=K(F_c(S_a))\setminus K(T_b),\qquad Extra_T=K(T_b)\setminus K(F_c(S_a)).
$$

For matched key $k$:

$$
Mismatch(k)\iff Canon_M(F_c(S_a)[k])\ne Canon_M(T_b[k]).
$$

An aggregate residual is

$$
\Delta A_j(g)=A_{T_b}^j(g)-A_{F_c(S_a)}^j(g).
$$

A full exact pass requires no missing/extra multiplicity, no mismatched canonical rows, complete evaluation, and satisfied continuity/cut requirements. Hash equality substitutes probabilistic digest evidence for exact byte comparison and must be labeled accordingly.

These definitions do not make a live operational source immutable, prove transformation correctness, or choose authoritative truth. Those are contract and system premises.

## Mechanisms, Invariants, or Proof Structure

Proof sketch that equal count and one sum do not prove keyed row equality:

1. Let source keyed values be $S=\{A\mapsto40,B\mapsto60\}$.
2. Let target keyed values be $T=\{A\mapsto50,B\mapsto50\}$.
3. Both contain exactly two keyed rows, so their row counts agree.
4. The source total is $40+60=100$ and target total is $50+50=100$, so the chosen aggregate agrees.
5. Yet $S[A]\ne T[A]$ and $S[B]\ne T[B]$.
6. Therefore count equality conjoined with this sum equality does not imply keyed row equality.
7. A full keyed comparison exposes both differences; additional independent aggregates can improve detection but do not generally replace exact equality.

The counterexample does not diminish control totals: they are efficient necessary conditions for many contracts and localize failures when cohortized. It establishes their proof limit.

The executable reproduces the counterexample, key-set agreement, field-level differences, and repaired exact equality. It is a teaching abstraction, not a database snapshot, CDC validator, distributed hash, migration service, or financial control system.

<!-- bijux-verify: {"id":"layered-reconciliation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"row_count_match=True\namount_total_match=True\nmissing_target=()\nextra_target=()\nvalue_mismatch_keys=('A', 'B')\nexact_match=False\nrepaired_exact_match=True\n","stderr":""}} -->
```python
source = {"A": 40, "B": 60}
target = {"A": 50, "B": 50}

source_keys = set(source)
target_keys = set(target)
missing_target = tuple(sorted(source_keys - target_keys))
extra_target = tuple(sorted(target_keys - source_keys))
mismatches = tuple(sorted(key for key in source_keys & target_keys if source[key] != target[key]))

print(f"row_count_match={len(source) == len(target)}")
print(f"amount_total_match={sum(source.values()) == sum(target.values())}")
print(f"missing_target={missing_target}")
print(f"extra_target={extra_target}")
print(f"value_mismatch_keys={mismatches}")
print(f"exact_match={not missing_target and not extra_target and not mismatches}")

repaired_target = {"A": 40, "B": 60}
repaired_exact = tuple(sorted(source.items())) == tuple(sorted(repaired_target.items()))
print(f"repaired_exact_match={repaired_exact}")
```

## Alternatives and Trade-Offs

**Live versus pinned comparison.** Live checks provide rapid signals but mix propagation and mutation. Pinned cuts yield reproducibility and stronger claims at snapshot/coordination cost.

**Counts/totals versus row comparison.** Aggregates are cheap and localize large failures. Row comparison is diagnostic and stronger but expensive, sensitive, and dependent on keys/canonicalization.

**Exact compare versus hashing.** Exact comparison avoids digest collision assumptions but transfers/joins more data. Hierarchical cryptographic hashes scale well while adding canonicalization, algorithm, collision, and secrecy concerns.

**Set versus multiset semantics.** Sets simplify identity comparison but erase duplicates. Multisets preserve multiplicity and are required when repeated identical events/rows matter.

**Full versus incremental reconciliation.** Full runs reset assurance and catch drift at high cost. Incremental runs reduce latency/cost but depend on continuous positions, deletes, maintained state, and periodic anchors.

**Zero tolerance versus materiality.** Exactness is appropriate for identities and conserved integer quantities. Domain tolerances accommodate rounding/noise but can normalize systematic error; publish residual distributions and cohorts.

**Source-authoritative resync versus bidirectional ownership.** Simple replicas can repair from source. Targets with owned enrichments or accepted corrections need field-level authority and conflict resolution to avoid destructive overwrite.

**Block versus publish with caveat.** Blocking protects critical correctness but harms freshness. Conditional publication can preserve availability when differences are bounded, isolated, visible, and semantically safe.

**Independent implementation versus shared logic.** Shared mappings reduce drift and maintenance. Independent control logic reduces common-mode bugs; use simple independent invariants alongside reviewed shared canonicalization.

**Detailed differences versus minimized evidence.** Full values speed repair but expose sensitive data. Counts, digests, secure pointers, redaction, and access-controlled samples balance diagnosis with protection.

## Failure Modes and Misconceptions

1. **“The job succeeded, so data reconciles.”** Execution success is not population/value evidence.
2. **“Current source and target are comparable.”** They may represent different commits/cuts.
3. **“Same timestamp means same state.”** Clocks and transaction visibility differ.
4. **“Snapshot plus CDC cannot lose rows.”** The handoff boundary can gap or overlap.
5. **“Stored checkpoint means applied data.”** Checkpoint/data commit ordering determines safety.
6. **“Same row count means same rows.”** Missing and extra identities can offset.
7. **“Same total means same values.”** Positive and negative differences can cancel.
8. **“Global equality covers cohorts.”** Regional/tenant errors can cancel globally.
9. **“Distinct key count proves key equality.”** Different key sets can share cardinality.
10. **“A set comparison preserves duplicates.”** Multiplicity disappears.
11. **“Joining duplicates is harmless.”** Many-to-many multiplication distorts evidence.
12. **“An inner join finds missing rows.”** It removes one-sided keys.
13. **“A hash defines equality automatically.”** Canonicalization and collision assumptions define the claim.
14. **“Concatenation is canonical.”** Field boundaries and types can be ambiguous.
15. **“Hashes anonymize identifiers.”** Low-entropy values can be guessed.
16. **“Float equality just needs a large tolerance.”** Unit, scale, rounding, NaN, and error direction matter.
17. **“Source equals target byte-for-byte.”** Intentional transformation may define different representation.
18. **“Approved exclusions need no totals.”** They must reconcile as a separately governed population.
19. **“Endpoint snapshot proves event completeness.”** Missing events can cancel in current state.
20. **“Incremental feeds always contain every change.”** Feed mode, enablement, schema, and retention differ.
21. **“At-least-once duplicates are random.”** Stable source identity enables deterministic deduplication.
22. **“Approximate distinct proves zero loss.”** Error bounds cannot support exact absence claims.
23. **“A sample proves full reconciliation.”** Rare or concentrated failures may be missed.
24. **“Pending can remain pending indefinitely.”** It requires evidence, expiry, and recheck.
25. **“Unknown is equivalent to zero differences.”** Partial/failed comparison provides no pass.
26. **“Resync is always safe.”** Authority, concurrent changes, and target-owned fields matter.
27. **“Repair can overwrite failed evidence.”** Immutable results are required for audit and diagnosis.
28. **“One full run proves future increments.”** Continuity and maintained state can drift afterward.

## Worked Examples

### Example 1

A migration freezes source at transaction snapshot X91 and compares target commit T14. Counts match globally, but tenant cohorts show one missing and one extra row in different tenants; the global count had canceled the defect.

### Example 2

A snapshot captures through LSN 500 inclusive and CDC begins after 500. The boundary is gap-free. Another pipeline begins after 501 and silently loses the event at 501; a continuity check detects the missing interval.

### Example 3

Source has two identical legitimate events and target one. Set equality passes; key-multiset equality reports multiplicity difference. Event identity includes partition and source offset.

### Example 4

Orders rejected for invalid currency are absent from the curated target. The contract reconciles `source = target + quarantine + approved exclusions`, with separate counts and immutable rule IDs rather than pretending source equals target.

### Example 5

Two engines serialize decimal scale and timestamps differently. Golden canonicalization fixtures fail before production hashing, preventing thousands of false row mismatches.

### Example 6

A daily ledger's signed amount sums agree despite one +100 and one -100 misassignment. Per-account sums, absolute totals, counts, and keyed row comparison expose the cancellation.

### Example 7

A Delta change feed was enabled after table creation. Reconciliation uses a full baseline at the enabling version, then retained CDF intervals; it does not claim earlier changes exist in the feed.

### Example 8

A Debezium connector re-emits events after recovery. The sink deduplicates stable source transaction/LSN identities, and reconciliation checks both log-position continuity and endpoint state.

### Example 9

A critical run times out after scanning 70% of partitions. It records unknown with coverage 70%, holds publication, and safely retries. It never emits a zero-mismatch pass.

### Example 10

An automated resync sees target-only rows. Because the target owns a fraud-review field and legal holds exist, the job quarantines candidates for approval instead of deleting them; a new pinned reconciliation follows any correction.

## Cross-Program Connections

- **Database Systems:** snapshots, transaction logs, keys, joins, multiset semantics, aggregates, isolation, replication, and constraints ground reconciliation.
- **Distributed Systems:** consistent cuts, barriers, offsets, checkpoints, exactly/at-least-once delivery, idempotency, clocks, and partial failure shape evidence.
- **Algorithms and Data Structures:** sorting, merge joins, hashing, Merkle-style hierarchies, sketches, multisets, and external-memory algorithms control scale.
- **Software Engineering:** differential testing, golden masters, property tests, independent oracles, versioning, mutation tests, and reproducible builds strengthen controls.
- **API and Service Engineering:** idempotency keys, pagination snapshots, ETags, webhooks, retries, partial responses, and versioned schemas affect cross-system comparisons.
- **Platform Engineering:** reusable control planes, lineage, rule registries, evidence storage, quotas, gates, dashboards, and repair workflows scale practice.
- **Security Engineering:** integrity, cryptographic digests, key management, least privilege, separation of duties, tamper evidence, and audit protect reconciliation.
- **Privacy Engineering:** minimization, pseudonymization limits, protected differences, correction, retention, deletion, and legal holds constrain evidence and repair.
- **Reliability Engineering:** SLOs, detection lag, unknown states, backpressure, bounded automation, incident response, recovery, and recurrence make controls operable.
- **Formal Methods:** refinement, equivalence relations, invariants, conservation, bisimulation intuition, counterexamples, and proof obligations bound claims.

## References

1. AWS. [AWS DMS data validation](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Validating.html). Accessed 2026-09-03. Primary service documentation for row-level source/target comparison, pending/mismatched/suspended/error states, missing-source/target classification, and validation statistics.
2. AWS. [Data validation task settings](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.CustomizingTasks.TaskSettings.DataValidation.html). Accessed 2026-09-03. Primary documentation for validation modes, full-load/CDC behavior, thread/partition controls, delays, records, and engine-specific comparison behavior.
3. AWS. [AWS DMS data resync](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Validating.DataResync.html). Accessed 2026-09-03. Primary documentation for applying source values to repair target inconsistencies found by validation.
4. dbt Labs. [dbt audit helper](https://github.com/dbt-labs/dbt-audit-helper). Accessed 2026-09-03. Primary project documentation for schema, count, key, column, full-row, classification, and quick hash-based relation comparisons.
5. dbt Labs. [dbt utils generic tests](https://github.com/dbt-labs/dbt-utils). Accessed 2026-09-03. Primary project documentation for equal row-count and relation-equality tests, group comparisons, and numeric precision options.
6. Great Expectations. [Validate data integrity](https://docs.greatexpectations.io/docs/reference/learn/data_quality_use_cases/integrity/). Accessed 2026-09-03. Primary documentation for referential, cross-table, cross-column, and multi-source equality validation.
7. OpenLineage. [Object model](https://openlineage.io/docs/spec/object-model/). Accessed 2026-09-03. Primary specification documentation for run, job, dataset, version, lineage, quality, and output-statistics evidence.
8. OpenLineage. [Dataset metrics](https://openlineage.io/docs/integrations/spark/dataset_metrics/). Accessed 2026-09-03. Primary integration documentation for input/output row, byte, file, scan, and commit metrics plus their limitations.
9. Debezium. [PostgreSQL connector](https://debezium.io/documentation/reference/stable/connectors/postgresql.html). Accessed 2026-09-03. Primary documentation for snapshots, LSN offsets, replication slots, transaction/source metadata, duplicate recovery events, and data-loss hazards.
10. Delta Lake. [Change data feed](https://docs.delta.io/delta-change-data-feed/). Accessed 2026-09-03. Primary documentation for row changes, commit versions, enablement boundary, retention, schema-evolution limits, and downstream use.
11. Apache Hudi. [SQL queries](https://hudi.apache.org/docs/sql_queries/). Accessed 2026-09-03. Primary documentation distinguishing incremental latest-state and CDC queries, checkpoints, completion time, and table versions.
12. Apache Iceberg. [Spark queries and metadata tables](https://iceberg.apache.org/docs/latest/spark-queries/). Accessed 2026-09-03. Primary documentation for snapshots, history, files, manifests, entries, partitions, and change-query evidence.
13. NIST. [Secure Hash Standard (FIPS 180-4)](https://csrc.nist.gov/pubs/fips/180-4/upd1/final). Accessed 2026-09-03. Authoritative specification record for SHA algorithms used within explicitly versioned digest profiles.
14. UK Government Data Quality Hub. [The Government Data Quality Framework](https://www.gov.uk/government/publications/the-government-data-quality-framework/the-government-data-quality-framework). Accessed 2026-09-03. Primary framework for consistency, accuracy, completeness, lifecycle controls, communication, action plans, and root-cause improvement.

## Exercises

### Exercise 1

Design a reconciliation contract for a full database migration followed by CDC. Include source snapshot/log boundary, target version/checkpoint, keys, schema mapping, counts, totals, canonical rows, overlap/gap handling, deletes, coverage, gate, and evidence.

### Exercise 2

Specify a cross-engine canonicalization and hierarchical hashing profile for nested order rows. Cover schema/field identities, types, Unicode, null/absent/default, decimals/floats, timestamps, arrays/maps, length framing, algorithm, salting, golden fixtures, collision policy, and drill-down.

### Exercise 3

Build a reconciliation vector for a source order/event model transformed into daily customer/currency aggregates. Define grain, keys, filters, quarantine, joins, exchange rates, rounding, cohorts, conserved totals, late corrections, tolerances, and exact versus approximate evidence.

### Exercise 4

Design daily incremental and monthly full reconciliation for a lakehouse pipeline. Include change-feed retention, checkpoints, deletes, affected historical windows, maintained state, transactionality, sampling/sketch limits, execution coverage, SLOs, and rebuild triggers.

### Exercise 5

Create an incident and automated-resync runbook for missing-target, extra-target, value-mismatch, pending, and unknown states. Cover evidence preservation, source authority, target-owned fields, fencing, idempotency, approvals, privacy, post-repair validation, consumer replay, and recurrence.

## Answers to the Exercises

### Answer 1

Acquire source snapshot X and its exact log position L before releasing/while retaining WAL. Start CDC at an endpoint that overlaps or follows X with explicitly tested inclusive/exclusive semantics; deduplicate overlap by stable transaction/event identity. Pin target full-load commit T and atomically associate sink checkpoint with applied data. Version schema/transformation/reference/filter/null/timezone mappings. Validate source manifest, schema, row/distinct/multiset-key counts, cohort totals, source-only/target-only keys, and canonical matched rows at X/T, then reconcile every CDC interval for continuity, inserts/updates/deletes and endpoint state. Unknown/partial execution holds the gate; pending has a bounded expiry. Evidence records identities, queries/digests, counts, coverage, difference classes, protected samples, and decisions. A full reconciliation after catch-up establishes the baseline.

### Answer 2

Use a schema-versioned structured encoding keyed by stable field IDs in deterministic order with explicit type tags and length framing. Distinguish absent, null, default-derived, empty, NaN/infinities/signed zero; define decimal scale/rounding and prohibit lossy float conversion where exactness is needed. Normalize Unicode only to the named form, convert instants to a named epoch/unit while preserving local-time semantics separately, sort map keys by canonical bytes, and preserve array order unless contract says multiset. Select and version a cryptographic algorithm; use keyed/salted profiles for sensitive low-entropy fields and control who can compare them. Cross-engine fixtures assert exact canonical bytes/digests. Compute row then bucket/partition summaries with multiplicity-safe construction. Any mismatch drills down exactly; matching hashes remain algorithm/profile-bounded probabilistic evidence, not anonymity or cut correctness.

### Answer 3

Pin source events and target aggregate versions. Define event identity, customer/currency/day grain, accepted statuses, cancellations, deduplication winner, quarantine/exclusion ledger, customer join cardinality, effective-dated exchange-rate version, timezone day boundary, decimal scale, and round-after-sum policy. Reconcile source accepted/quarantined/excluded counts; event-key multiset; per source/tenant/day/currency event counts; original-currency signed and absolute amounts; converted pre-round total; target customer/day totals; and customer key coverage. Late/corrected events reopen affected days and version results. Integer/native-currency invariants are exact; converted values use justified minor-unit tolerance with residual distribution. Approximate/sketch evidence only prioritizes drill-down and never substitutes for zero-loss event/key checks.

### Answer 4

Retain change feeds beyond maximum outage plus recovery margin and pin every interval $(L_i,L_{i+1}]$. Daily runs validate continuity, source changes, deletes/tombstones, transformed expected changes, target-applied checkpoint, changed-key canonical values, and all aggregates/windows affected by late events or reference changes. Commit target, checkpoint, and reconciliation state in one recoverable protocol or make replay idempotent. Track intended/scanned partitions/rows/bytes; failures become unknown. Sketches detect drift and samples monitor noncritical fields with error labels. Monthly full runs compare complete key multisets and canonical rows by cohorts and rebuild exact state. Trigger early full rebuild on gaps, retention crossing, state/digest-version changes, corruption, recovery, unexplained residuals, or repeated incremental mismatch. SLOs cover cut lag, pending age, run completion, mismatch detection, and full-anchor age.

### Answer 5

Freeze run/source/target/transformation/reference/checkpoint identities and preserve differences before live re-query. Classify wrong cut/mapping separately. Missing target may replay pinned authoritative source; extra target is never deleted until ownership, history, holds, and exclusions are checked; mismatched fields follow field-level authority; pending waits only to a documented expiry; unknown holds critical action and reruns after execution repair. Fence or use conditional writes, assign idempotent repair IDs, cap rows/bytes/time, dry-run destructive effects, and require separation-of-duty approval. Protect values with counts/digests and controlled quarantine access. Publish corrections as new history, rerun full scoped reconciliation plus unaffected controls, advance checkpoints only after committed proof, notify consumers of versions and replay semantics, and monitor root cause, time to contain/correct, repair volume, and recurrence. Original failed evidence remains immutable.
