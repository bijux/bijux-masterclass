---
module_id: DE-038
program: Data Engineering
level: 1
module_number: 38
title: Late Corrections and Restatement
status: complete
last_verified: 2026-09-02
---

# Late Corrections and Restatement

## One-Page Review

### Governing question

How can a data system accept late and corrected evidence, distinguish what happened from when it became known, recompute every affected output, preserve prior published meaning, and communicate a governed restatement without double counting or silent history changes?

### Essential definitions

- A **late-arriving fact** is a previously unrepresented business occurrence whose event/valid time precedes its warehouse arrival/knowledge time.
- A **correction** supersedes a prior assertion about the same governed occurrence or valid-time state because that assertion was wrong or incomplete.
- A **retraction** invalidates a prior assertion/effect; a **reversal** is a new compensating occurrence whose signed effect offsets another under domain rules.
- **valid time** states when an assertion is true in the modeled world; **system/knowledge time** states when a particular assertion version is recorded/accepted by the data system.
- A **bitemporal assertion** carries both valid-time and system-time intervals so queries can ask “what is currently believed about then?” and “what was believed then about then?”
- A **revision chain** links immutable assertion versions through stable occurrence/entity identity, source version/order, supersedes/retracts relationships, reason, and authority.
- A **restatement** publishes a new version of previously released output under an approved correction/semantic policy while retaining the prior version and its lineage.
- A **prospective adjustment** recognizes a difference in a current/future period instead of changing a closed historical output; it is not the same answer as restatement.
- A **finality policy** defines open/provisional/final/reopened states, correction horizon, materiality/approval, residual risk, and consumer behavior.
- The **affected closure** is every source state, output key, aggregate/window, feature, cache, export, or report whose answer can change because of the revision.
- A **restatement manifest** binds cause, authority, original/new source and output versions, affected scope, before/after/delta evidence, approvals, publication, notification, and rollback.

### Central model, mechanism, or theorem

Let immutable assertions for business occurrence $q$ have valid-time interval $V(a)$, knowledge/system interval $K(a)$, source order/version, payload, and active/retracted state. The governed assertion selected for business time $t$ and knowledge cut $\tau$ is

$$
A(q,t,\tau)=winner\{a:q(a)=q,\ t\in V(a),\ \tau\in K(a)\},
$$

under an explicit authority/version/conflict policy. Two time coordinates support two distinct questions:

- current restated truth at $t$: evaluate $A(q,t,\tau_{now})$;
- as-published/as-known truth: evaluate $A(q,t,\tau_{publication})$ and the transformation/reference versions recorded then.

For prior published output $O_p=F_v(S_{\tau_p},R_{\tau_p})$ and newly governed assertions at cut $\tau_r$, restatement candidate over affected output set $U$ is

$$
B_U=F_{v'}(S_{\tau_r},R_{policy})\restriction_U.
$$

Publication creates a new output version and a key-level delta $D_U=B_U-O_p\restriction_U$; it does not rewrite the identity/evidence of $O_p$. Affected scope $U$ is the transitive influence closure of both old and new assertion states, including group moves, deletes, joins, windows, cumulative state, and downstream materializations.

### Critical invariants

- Every incoming item is classified as new-late occurrence, exact duplicate, stale version, correction, retraction, reversal, conflict, or unsupported—not merely “late.”
- Occurrence/entity identity, valid/event time, knowledge/ingestion/system time, source order/version/epoch, operation, payload, schema, reason, and authority are distinct.
- Revision links are immutable/auditable; equal authority/version with unequal semantics fails closed; older delivery cannot undo a newer correction or resurrect a retraction.
- Valid-time and system-time intervals use explicit half-open boundaries, time zone/precision, non-overlap rules, and transactionally coherent interval surgery.
- Original raw assertions and prior published outputs remain reconstructable for the required audit/comparability horizon.
- Restatement policy names open/final/reopened periods, automatic horizon, materiality, approval, prospective exceptions, consumer contract, and residual risk.
- Affected closure includes both before and after keys/categories/partitions plus transitive joins, aggregates, windows, state, and downstream consumers.
- Replacement/reversal logic cannot count original and replacement together, replay a compensating effect twice, or drop deletion evidence.
- Candidate computation uses pinned source/reference/code/schema/runtime and isolated output; publication is complete, conditional, versioned, and reversible where promised.
- Before/after key sets, multiplicities, versions, retractions, measures/components, group movements, and unchanged scope reconcile independently of aggregate totals.
- Consumers can distinguish as-published, as-was, current-restated, and prospective-adjustment views and receive version/change notification.
- Correction lag, backlog, conflicts, restatement churn/materiality, downstream propagation, finality exceptions, retention, privacy, and recovery are observable.

### Common failures

Common failures include calling every old-timestamp row late; treating a correction as an additional fact; overwriting raw evidence; ordering corrections by arrival time; using business event time as source version; changing a row without revision identity/reason; applying an old retry after a newer correction; closing one temporal interval and inserting another non-atomically; confusing valid-time history with knowledge history; assuming Type 2 alone is bitemporal; deleting a tombstone; correcting only the source row while aggregates/windows/caches remain stale; deriving affected scope only from the new category; restating a final period without approval; silently posting old differences into today; overwriting published reports in place; labeling current dimensions as historical truth; matching totals while category/key movements are wrong; expiring snapshots/raw history before audit; and sending correction details to unauthorized consumers.

### Compact example

At knowledge cut 5, published facts are `sale-1(day2)=100` and `sale-2(day4)=50`, total 150. Later evidence corrects `sale-1` to 80, introduces genuinely late `sale-3(day2)=40`, and retracts `sale-2`; current restated total becomes 120. The overall delta is −30, but day 2 moves +20 and day 4 moves −50. For a trailing three-day result, changed source days 2 and 4 affect output days 2–6, with deltas `(+20,+20,-30,-50,-50)`. Prior cut-5 output remains queryable; the new generation records revision/retraction lineage and notification.

### Connections

[DE-009](009-time-time-zones-and-event-timestamps.md) defines time roles, [DE-014](014-slowly-changing-dimensions.md) defines valid-time versions, [DE-015](015-snapshot-and-accumulating-fact-tables.md) defines periodic restatement, [DE-022](022-watermarks-and-high-water-marks.md) defines lateness/finality signals, [DE-026](026-database-change-data-capture.md) supplies operations/order, and [DE-035](035-incremental-models.md) through [DE-037](037-backfills.md) define affected sets, merge, and governed recomputation. DE-039 next treats deterministic transformations.

## Governing Question

What exactly changes when evidence arrives after expected processing, and how can the system revise current truth without destroying the ability to reproduce what consumers previously saw?

“Late data” describes timing, not semantics. An original invoice received a week late is a new occurrence. A revised invoice amount is a correction. A cancellation might retract the original assertion or be a distinct compensating business event. A duplicate retry is no new fact at all. Applying one generic upsert to all four corrupts at least one case.

Correction processing begins with identity and authority. Which occurrence or state is being revised? Does the source provide a monotone revision, transaction order, explicit retraction, or authoritative correction relationship? Can two authorities disagree? What should happen when a correction arrives before the original, or after another correction? Arrival order is evidence about transport, not necessarily precedence.

Time has two essential axes. Valid time answers when a fact/state applies in the business world. Knowledge/system time answers when the data system recorded a version. If a customer's region was valid from March 1 but learned on April 10, current restated March reports may use the region while an as-published March report must preserve what was known at publication. One `updated_at` field cannot represent both questions reliably.

Restatement is publication governance. The system does not merely recompute a partition; it issues a new version of a previously visible answer, identifies the prior version, explains why and where it changed, updates every affected derivative, informs consumers, and retains evidence for comparison or rollback. Period finality and materiality determine whether this happens automatically, by exception, or as a prospective adjustment.

## Why This Matters

Late and corrected evidence is normal: offline devices reconnect, claims adjudicate, orders cancel, reference classifications are repaired, source transactions replicate after outage, manual records are amended, and upstream bugs are fixed. A pipeline that assumes all business truth arrives once and in event-time order will silently drift.

The first risk is double counting. If an original sale of 100 is corrected to 80 and the pipeline appends 80 as another sale, reported revenue becomes 180. A replacement projection must select 80; an immutable accounting/event approach may append an authorized −100 reversal plus +80 replacement, whose net is 80. These representations are equivalent only when their identities and aggregation rules are explicit.

The second risk is invisible movement. Correcting a fact's region from west to east leaves global total unchanged while both regional totals are wrong until the system subtracts from west and adds to east. Validation that compares only global counts/totals will pass. Affected closure and reconciliation must include old and new keys/group values.

The third risk is report instability. Consumers may have exported, filed, billed, trained, or made decisions from version 1. Quietly mutating the table removes the ability to explain those decisions. Versioned outputs and bitemporal/raw evidence support both current-restated truth and as-published reproduction.

Watermarks and close schedules manage latency, not metaphysical truth. Apache Beam documents watermarks as estimates and provides allowed lateness/late firings; a watermark can trigger operational finality, but real evidence may still arrive later. The business policy must define drop, quarantine, correction, restatement, or prospective treatment beyond the automated horizon.

Corrections can expand work dramatically. A dimension interval change may reclassify millions of facts. A correction to an early cumulative balance affects every later snapshot. A single event can bridge two sessions. Resource, approval, and consumer-impact controls belong in the correction protocol.

Finally, retained history creates security and privacy obligations. Before-images, retracted records, prior addresses, and deleted-subject data may be more sensitive than current output. Audit requirements do not authorize indefinite unrestricted retention. Separate protected evidence from ordinary analytical visibility and apply purpose, access, encryption, minimization, deletion/legal-hold, and retention rules.

## Prerequisites and Retrieval

Retrieve business owner and source authority; target/report owner; occurrence/entity/business keys and namespaces; original assertion/event identities; correction/retraction/reversal identifiers and links; source system/epoch/transaction/order/version; before/after images; valid/event/effective time and interval; source commit/knowledge/ingestion/processing/publication times; time zones/calendars/precision; operation semantics; reason codes and actor/approval; schemas and canonical payload/digest; duplicate/conflict rules; source/reference/code/config/runtime histories; immutable raw records, CDC, snapshots, temporal tables, and retention; current and prior output generations; output grain/keys/measures; watermark/allowed-lateness/window/session/state policy; open/provisional/final/reopened periods; automatic correction horizon; materiality and prospective-adjustment policy; regulatory/contractual reporting rules; affected lineage/partition mappings; aggregates/features/caches/exports/reports; restatement/backfill mechanisms; live/concurrent writes; target merge/tombstone/version behavior; validation and control totals; consumer version APIs/contracts; notification/subscription; security classification/privacy/erasure/legal holds; observability/SLOs; rollback/forward repair; and disaster-recovery evidence.

Distinguish late occurrence from corrected occurrence; duplicate delivery from repeated business event; correction from reversal; reversal from deletion; retraction from privacy erasure; business identity from assertion-version identity; event time from source commit and arrival; valid time from system/knowledge time; system time from arbitrary worker clock; original truth from current accepted truth; as-was business validity from as-published knowledge; Type 1 overwrite from Type 2 valid history; valid-time SCD from bitemporal history; current dimension from event-time dimension; watermark from source checkpoint; operational finality from irrevocable truth; correction horizon from retention horizon; restatement from backfill execution; restated output from prospective adjustment; prior version from wrong/deletable artifact; and aggregate equality from exact key/group movement correctness.

Create a correction/restatement contract:

| Concern | Required decision and evidence |
|---|---|
| Classification | New-late, duplicate, stale, correction, retraction, reversal, conflict, unsupported |
| Identity/order | Occurrence/entity/assertion IDs, revises/retracts links, source epoch/version/transaction/order |
| Time | Valid interval, knowledge/system interval, event/commit/arrival/publication roles, zone/precision |
| Authority | Source/actor, reason, approval, conflicting-authority precedence, materiality |
| Finality | Open/provisional/final/reopened states, automated horizon, exceptions, prospective policy |
| Scope | Before/after keys/groups, affected output closure, downstream consumers, unchanged region |
| Semantics | Replace, interval surgery, retract, reverse, reclassify, current/as-was/as-published view |
| Execution | Immutable inputs, pinned versions, isolated candidate, idempotency, live fencing, resources |
| Assurance | Original/new/delta identities, counts, values, movements, controls, oracle, owner approval |
| Publication | New version/supersession, cutover, notifications, prior-version retention, rollback/repair |

## Learning Objectives

After completing this module, you should be able to:

1. classify late occurrences, duplicates, corrections, retractions, reversals, stale versions, and conflicts;
2. model valid time separately from system/knowledge time and explain current-restated versus as-published queries;
3. design immutable revision chains, authority/version ordering, tie/conflict handling, and tombstone retention;
4. apply replacement, reversal, interval repair, and prospective-adjustment semantics without double counting;
5. derive affected closure from both before and after states across joins, aggregates, windows, cumulative state, and downstream assets;
6. define open/provisional/final/reopened periods, materiality, approval, correction horizons, and residual risk;
7. build an isolated, versioned restatement generation with before/after/delta evidence and conditional publication;
8. communicate supersession and support as-published, as-was, and current-restated consumer contracts;
9. test out-of-order revisions, boundaries, conflicts, replay, concurrency, partial propagation, rollback, and privacy; and
10. operate correction lag/backlog/churn with lineage, security, retention, resource, and recovery controls.

## Core Exposition

### Classify before mutating

For every arrival, ask what new assertion it makes. A stable event ID and identical payload is an exact redelivery. A previously unseen event with old valid time is late-new. A new assertion ID that explicitly supersedes the same business occurrence is a correction. An explicit invalidation is a retraction. A distinct compensating transaction is a reversal. A lower source version is stale. Equal precedence with conflicting payload is a conflict.

Classification can be domain-specific. A refund is often a new occurrence linked to a sale, not a correction of the original sale. A typo repair changes an assertion. A canceled order may transition state rather than erase that the order existed. Record the domain relationship rather than infer it from negative amount or `deleted=true` alone.

Do not discard unknown/unsupported correction forms and advance progress. Quarantine with raw bytes, schema/source position, identity, reason, and ownership; stop or continue only under an explicit partial-progress policy whose downstream completeness is visible.

### Give assertions stable revision identity

Preserve immutable raw assertions. Each accepted version needs assertion ID, governed occurrence/entity key, source namespace/epoch, revision/order, operation, payload digest/schema, valid interval, knowledge position/time, revises/retracts link, reason, authority, and ingestion lineage.

Event identity and revision identity differ. A connector may deliver one revision twice under the same event identity; deduplicate it. Two distinct assertions may claim revision 4; if their semantic digests differ and neither authority outranks the other, fail closed. Do not select the last worker arrival.

Version comparison must be meaningful. Database log order can order committed changes within one source epoch. Source revision numbers may order one entity. Human corrections may need an approval sequence. Timestamps with coarse precision or mutable clocks are weak ordering evidence. Cross-source conflicts require a declared authority/merging policy, not numeric comparison of incomparable counters.

### Model valid and knowledge time

Represent business-valid intervals $V=[v_{from},v_{to})$ and system/knowledge intervals $K=[k_{from},k_{to})$. For each governed key, valid-time versions selected at one knowledge cut should meet declared non-overlap/gap/current-row rules. System intervals preserve when each belief/version was available.

A correction learned April 10 but valid March 1 may close the old assertion's system interval at April 10 and insert a new system version whose business-valid interval begins March 1. An as-known-April-1 query sees the old assertion; a current-restated March query sees the correction. If the correction changes only part of a valid interval, interval surgery splits unaffected left/right pieces and replaces the middle.

Make interval surgery atomic. Closing an old interval before inserting its replacement can expose a gap; inserting first can expose overlap. Build a candidate history or use a transaction/constraint protocol. Test exact-boundary instants, equal timestamps, open-ended sentinels, daylight-saving transitions, and precision truncation.

System-versioned temporal tables can retain database row versions and support point-in-system-time queries under documented semantics. They do not automatically supply business valid time, source correction authority, or every external publication version. Likewise, a valid-time Type 2 table does not preserve each prior warehouse belief unless system time is also retained.

### Choose the consumer time perspective

Expose and name the supported perspectives:

- **current-restated:** newest accepted assertions applied to their valid times;
- **as-was:** attributes/facts selected by business valid time, usually under a specified current knowledge cut;
- **as-known/as-published:** assertions, transformations, references, and output generation available at the historical knowledge/publication cut;
- **current view:** entity state at current valid time and current knowledge; and
- **prospective/adjusted:** closed historical output retained, with a separately identified current-period adjustment.

Do not call current-restated output “what the report showed then.” Do not call an as-published error “current truth.” APIs/tables/views need version or `as_of` parameters, default behavior, retention limits, and metadata so consumers can choose correctly.

Snapshot/time-travel systems preserve storage versions only while snapshots and files remain retained. Apache Iceberg documents snapshot/time-travel queries, history metadata, branches/tags, and schema-selection differences. Pin exact snapshot ID and schema behavior; a timestamp lookup alone can become ambiguous around retention/time precision or select a different schema than expected.

### Apply replacement, retraction, or reversal correctly

For a current-state projection, a winning correction replaces the logical occurrence/state. Retain old assertion in protected history but exclude it from current visible totals. A retraction makes the occurrence inactive/deleted under its winning version; retain tombstone/version so stale replay cannot resurrect it.

For an immutable ledger, do not update the original row. Append a correction protocol recognized by the fold: perhaps a retraction of original effect and a replacement effect, or a compensating reversal transaction linked to the original. Stable effect IDs and idempotent application prevent retrying −100 and +80 twice.

Correction and reversal may differ legally/domain-wise. Reversal records a new business event at its own valid/posting time; restatement asserts the original period/value was different. Prospective posting preserves a closed report but changes current period. The data platform implements the approved policy; it does not invent which is acceptable.

Patch payloads need field presence. Missing may mean unchanged, explicit NULL may correct to unknown/empty, and deletion may retract the whole occurrence. Canonical digest includes operation, presence semantics, schema, and relevant payload.

### Process out-of-order revision chains

Corrections can arrive before originals, after later corrections, or in batches with several revisions. Preserve them, order by authoritative source revision, validate chain links, and derive the winner/state independent of delivery order. If a referenced original is absent, hold an orphan correction or construct a tombstone/provisional state only under explicit rules.

For version sequence 1,3,2 delivered in that order, revision 2 must not overwrite 3. Revision 3 may depend on revision 2 as a patch; if so, the system needs complete chain replay rather than simple latest-row selection. Full-state after-images and patches have different fold requirements.

Key changes affect old and new identities. A correction that changes customer, account, region, date, or partition must retract/subtract from the old key and add/update the new key. Before image or prior assertion history is required; new state alone cannot discover where the old effect lives.

Debezium documents CDC envelopes, delete/tombstone behavior, key-change sequences, transaction metadata, and possible duplicate delivery during recovery. Preserve those mechanics as evidence, but map low-level row changes to governed business assertion/revision semantics deliberately.

### Interpret watermarks and finality correctly

Event-time watermark $W$ is an operational estimate that future elements earlier than $W$ are increasingly unlikely under a runner/source contract. It can close windows, emit results, and retire state after allowed lateness. It does not certify that no correction will ever be authorized.

Define automated handling by lateness age and period state. Within an open window, update normally. Within a provisional/restatement horizon, recompute automatically and emit a new version. Beyond the horizon or after finality, quarantine for materiality/approval. Some evidence may become a prospective adjustment; some may reopen and restate; some may be rejected under authoritative policy.

Keep extraction progress separate. A source-position checkpoint can capture a late event at today's log position even though its event time is last month. Resetting the checkpoint to the old business date is unnecessary and dangerous. Route the captured event through affected-set correction handling.

Allowed-lateness/state TTL must not be shorter than the automated correction guarantee unless a durable late path retains evidence elsewhere. Once streaming state expires, rebuild affected state from immutable history or hand off to batch restatement.

### Define period state and approval

Model period lifecycle explicitly: `open`, `provisional`, `final`, `reopened`, and perhaps `superseded/retired`. Transitions include authority, time, reason, materiality evaluation, approver, output version, and consumer notification. A boolean `closed` cannot explain exceptions or multiple restatements.

Materiality can include absolute/relative value, population affected, key/customer risk, regulatory/contractual category, downstream decisions, and cumulative effect. Thresholds require owner approval and should not silently discard individually small corrections whose cumulative total is material.

“Final” means automatic mutation is restricted, not that truth is immutable. Define residual-risk acceptance and where post-final evidence is retained. Reopening may require dual control, a new restatement request, frozen source/reference cut, impact preview, and sign-off before publication.

Never let compute cost define semantics alone. If accurate restatement is required but expensive, escalate capacity/timing; if policy permits prospective treatment, label it. Quietly ignoring evidence because an old partition is cold creates unmeasured debt.

### Derive the complete affected closure

Start from both before and after assertion states. For changed fact $x_{old}\rightarrow x_{new}$, affected direct groups include keys/partitions/dimensions referenced by either side. A west-to-east move changes west and east. A day-2-to-day-3 correction changes both days. A retraction affects old keys even when new state is absent.

Propagate influence through the transformation DAG. Aggregates need subtract-old/add-new or recomputation from canonical components. Distinct/min/max/quantiles/sketches may not support exact inverse. Windows require halos; sessions can merge/split; cumulative balances affect all later points; slowly changing dimension interval repair can re-key every fact in the interval.

Let direct changed assertion set be $\Delta$. If model/version influence maps are $I_v(x)$, affected output is

$$
U=\bigcup_{x\in\Delta}\left(I_v(x_{old})\cup I_v(x_{new})\right),
$$

extended transitively through downstream dependencies. If exact influence is unavailable, choose a conservative superset and validate unchanged regions; never choose a smaller convenient set.

External consumers count. Search indexes, caches, feature stores, extracts, reports, model training sets, notifications, invoices, and partner files may need invalidation/versioning/reissue. Some cannot be retracted; record forward correction and residual impact.

### Build and validate a restatement candidate

Create a restatement request from the accepted revision set and policy. Pin original output generation, new assertion/source cut, reference perspective, transformation/schema/runtime, affected closure, candidate destination, validation, approvers, notifications, rollback, and retention.

Use DE-037's governed backfill mechanism: exact output ownership, full context/halo, immutable units, stable operation keys, isolated attempts, resource limits, live fencing, candidate manifest, and conditional publication. A correction is semantic input; a backfill is one execution mechanism.

Validate the assertion layer first: identity/chain completeness, authority, source version/order, valid/system intervals, no unintended overlaps/gaps, retraction/reversal pairing, conflicts, and raw provenance. Then validate candidate outputs against old and new source controls.

Produce a before/after/delta ledger at the finest governed grain. Reconcile:

- removed, added, changed, unchanged, retracted, and conflicted occurrence IDs;
- old/new keys, versions, valid intervals, groups, partitions, and amounts;
- row/key/multiplicity/null/domain distributions;
- global and per-group count/sum components and conservation laws;
- affected-window/state boundaries and unchanged-outside-scope checks;
- prior/new output digests and independent full/differential oracle; and
- downstream version/refresh readiness.

Equal global totals do not prove correct reclassification. Expected nonzero difference is not a test failure when approved; unexplained difference is.

### Publish a new version, not silent mutation

Publish the entire validated affected generation atomically/conditionally from the expected base. The restatement manifest names prior and new output versions, assertion/correction set, reason/authority, policy/approval, affected scope, before/after/delta controls, source/reference/code/schema/runtime, publication receipt, and rollback/forward-repair path.

Retain prior outputs or sufficient reproducible snapshots for the contractual horizon. Mark supersession rather than rewriting lineage. W3C PROV-O supplies concepts such as revision, invalidation, derivation, generation, and activity/entity/agent relationships; map them to concrete dataset/run/assertion identities. OpenLineage Job/Run/Dataset and version facets can carry operational lineage.

Consumer interfaces should expose output version, `as_of`/perspective, restated-at, prior version, correction reason category, affected scope/materiality, and freshness/finality. Avoid leaking sensitive reason/payload details; publish the minimum metadata appropriate to each audience.

Notify subscribers before/with cutover when historical answers change. Include effective version/time, affected periods/datasets, magnitude/control summaries, required refresh/requery action, compatibility impact, and support owner. Machine-readable supersession events should be idempotent and versioned.

### Coordinate concurrent revisions and live data

Several corrections can target the same occurrence or output while restatement runs. Freeze the accepted correction set at cut $\tau_r$, then capture later revisions for the next candidate or rebase before publication. Do not let an older candidate overwrite a newer revision because it finished last.

Use source/assertion versions and target expected-generation/fencing checks. If current output advances, determine whether new changes are disjoint and composable; otherwise rebuild/reconcile affected closure. A restatement derived from reference generation R1 cannot silently publish after R2 changes overlapping facts.

Period reopening and schema migration may require serialization. An expand-contract schema can allow old/new readers while candidate builds. Avoid contracting or expiring old snapshots until live/backfill/restatement workers and rollback windows are complete.

Unknown commit outcomes require authoritative inspection of output pointer/snapshot and restatement receipt. Retrying a reversal or notification without idempotency can double effects. Treat timeout as unknown, not rollback.

### Operate correction and restatement lifecycle

Measure arrival-to-classification, classification-to-acceptance, acceptance-to-restated-publication, downstream propagation, and consumer notification latency separately. Monitor volume by class/source/age/period, stale/conflict/orphan revisions, interval violations, finality exceptions, materiality, affected fanout, restatement churn, rejected/ignored residuals, and as-published retention headroom.

Alert on missing authority/revision identity, equal-version conflict, tombstone resurrection, unexplained output delta, partial affected closure, final-period mutation without approval, output-version mismatch, downstream stale version, retention risk, and abnormal source correction spike. A surge may indicate upstream defect or abuse rather than ordinary lateness.

Keep a correction register: request/incident, owner, authority, occurrence/revision set, reason category, period state, original/new versions, impact, approvals, consumer notices, exceptions, residual risk, and closure. Avoid storing sensitive free-text reason where a controlled category/reference suffices.

Drill reconstruction of prior and current-restated views, replay of corrections in randomized delivery order, rollback/supersession, downstream refresh, consumer version query, and disaster recovery of revision/manifests. Correction capability is unproven if only the happy current table survives.

### Govern security, privacy, and retention

Authenticate correction sources and human approvers; authorize by dataset/tenant/field/period/action. A correction endpoint or staging table is a high-integrity mutation surface. Require strong audit, separation of duties for sensitive final-period restatement, rate limits, schema validation, and tamper-evident evidence.

Protect raw originals, before-images, prior addresses/classifications, reason text, assertion chains, quarantine, temporal history, snapshots, manifests, and notifications. Apply least privilege, encryption, tenant isolation, masked review views, and controlled export. Correction authority must not become cross-tenant reclassification authority.

Privacy correction/erasure and audit retention can conflict. Define legal basis, holds, cryptographic deletion/tokenization, restricted evidence, derived-output deletion, and notification obligations with domain experts. Retraction for analytical truth is not automatically physical erasure; physical erasure is not automatically permission to forget that a published aggregate version was superseded.

Retention must cover the maximum accepted late/correction/replay/audit/as-published horizon for raw assertions, schemas, reference history, tombstones, code/runtime, output versions, and receipts. If a required original is expired, state that exact reconstruction is impossible and use bounded evidence; do not fabricate history.

## Definitions and Notation

Let an immutable assertion be

$$
a=(id,q,r,op,payload,V,K,authority,reason,sourcePosition),
$$

where $id$ is assertion occurrence identity, $q$ is governed business occurrence/entity identity, $r$ is revision/order within an explicit source epoch, $V=[v_f,v_t)$ is business-valid interval, and $K=[k_f,k_t)$ is knowledge/system interval. The interval $k_t$ may be open until a later accepted assertion supersedes this belief.

Let $select(q,t,\tau)$ return the unique active assertion for business time $t$ known at knowledge cut $\tau$. Existence/uniqueness requires explicit authority/version ordering, valid/system interval rules, and conflict handling. Multiple equally authoritative assertions with equal revision and unequal semantics yield `conflict`, not a randomly selected row.

For point facts, $V$ may be a business instant/bucket rather than a duration. For entity state, $V$ is often an interval. Do not stretch a point occurrence into state or collapse an interval state into an event without a model decision.

Let $O^{(j)}$ be published output version $j$ with publication knowledge cut $\tau_j$, transformation $v_j$, reference policy/generation $R_j$, source assertion cut $S_j$, and contract/schema $C_j$. “As published” requires this whole tuple, not only historical source rows.

For old/new visible assertion maps $A_o,A_n$, direct assertion delta partitions identities into:

$$
Removed=keys(A_o)\setminus keys(A_n),
$$

$$
Added=keys(A_n)\setminus keys(A_o),
$$

$$
Changed=\{q\in keys(A_o)\cap keys(A_n):H(A_o(q))\ne H(A_n(q))\}.
$$

Use canonical semantic digest $H$ and compare old/new keys/groups from both records. Unchanged identity with changed grouping still belongs to `Changed`.

Let $I(x)$ be direct output influence of assertion state $x$. The affected set is conservatively

$$
U=\bigcup_{q\in Removed\cup Added\cup Changed}\left(I(A_o(q))\cup I(A_n(q))\right),
$$

where missing old/new states contribute an empty influence set. Then apply downstream influence maps transitively. The union of old/new influence is necessary for removals and group/partition/time-key moves.

For additive measure $m$, exact restatement delta over group $g$ is

$$
D_g=\sum_{x\in New_g}m(x)-\sum_{x\in Old_g}m(x).
$$

This formula is evidence, not always the execution method. Nonadditive measures and derived state may require recomputation.

Define finality state function $F(period,\tau)\in\{open,provisional,final,reopened,superseded\}$. A policy maps correction class, age, authority, magnitude/risk, and period state to `automatic restatement`, `approval required`, `prospective adjustment`, `quarantine`, or `reject`. Record the policy version used.

## Mechanisms, Invariants, or Proof Structure

Use this correction-to-restatement flow:

1. Land immutable source assertion/envelope before acknowledging source progress.
2. Validate schema, identity, source epoch/order, operation, valid time, and authority.
3. Deduplicate assertion delivery and classify new-late, stale, correction, retraction, reversal, conflict, or unsupported.
4. Update an isolated revision/temporal candidate, checking chain and interval invariants.
5. Evaluate finality/materiality policy and obtain required approval.
6. Compute old/new assertion diff and transitive affected closure from both states.
7. Build isolated restatement outputs with pinned source/reference/code/schema/runtime and governed backfill units.
8. Reconcile assertion, output, group movement, unchanged scope, and downstream readiness.
9. Conditionally publish a new version with supersession/provenance and idempotent notifications.
10. Observe consumer/downstream propagation, retain prior versions, and close or forward-repair residuals.

Idempotence requires stable assertion and restatement operation identities. Replaying the same accepted revision cannot create another logical revision; rebuilding the same output candidate cannot publish an indistinguishable duplicate as a new semantic version without an explicit policy. Same identity plus different digest fails closed.

The reference model below keeps point facts by business day and selects the highest consistent revision known at a system cut. It distinguishes correction, genuinely late-new occurrence, and retraction; computes as-was versus current-restated rows; derives changed source days from old and new states; and propagates them through a trailing three-day metric. It does not model intervals, source authority across systems, database transactions, streaming runners, physical snapshots, materiality, or consumer notification.

<!-- bijux-verify: {"id":"bitemporal-restatement-reference-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"as_was_rows=(('sale-1', 2, 100), ('sale-2', 4, 50))\nrestated_rows=(('sale-1', 2, 80), ('sale-3', 2, 40))\nas_was_total=150\nrestated_total=120\nrestatement_delta=-30\nchanged_source_days=(2, 4)\naffected_output_days=(2, 3, 4, 5, 6)\nrolling_deltas=((2, 20), (3, 20), (4, -30), (5, -50), (6, -50))\nreplay_stable=True\nconflict_detected=True\n","stderr":""}} -->
```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Assertion:
    assertion_id: str
    occurrence_id: str
    valid_day: int
    known_at: int
    revision: int
    amount: int | None
    retracted: bool = False

    def semantic(self):
        return (
            self.occurrence_id,
            self.valid_day,
            self.revision,
            self.amount,
            self.retracted,
        )


def deduplicate(assertions):
    by_id = {}
    for assertion in assertions:
        old = by_id.get(assertion.assertion_id)
        if old is not None and old.semantic() != assertion.semantic():
            raise ValueError("assertion identity conflict")
        by_id[assertion.assertion_id] = assertion
    return tuple(by_id[key] for key in sorted(by_id))


def as_known(assertions, knowledge_cut):
    grouped = {}
    for assertion in deduplicate(assertions):
        if assertion.known_at <= knowledge_cut:
            grouped.setdefault(assertion.occurrence_id, []).append(assertion)
    result = {}
    for occurrence, versions in grouped.items():
        latest_revision = max(version.revision for version in versions)
        tied = [version for version in versions if version.revision == latest_revision]
        if len({version.semantic() for version in tied}) != 1:
            raise ValueError("equal revision has conflicting semantics")
        winner = min(tied, key=lambda version: version.assertion_id)
        if not winner.retracted:
            result[occurrence] = winner
    return result


assertions = (
    Assertion("a1", "sale-1", 2, 3, 1, 100),
    Assertion("a2", "sale-2", 4, 4, 1, 50),
    Assertion("a3", "sale-1", 2, 10, 2, 80),
    Assertion("a4", "sale-3", 2, 12, 1, 40),
    Assertion("a5", "sale-2", 4, 13, 2, None, True),
)

old = as_known(assertions, 5)
new = as_known(assertions, 13)


def rows(state):
    return tuple(
        (occurrence, assertion.valid_day, assertion.amount)
        for occurrence, assertion in sorted(state.items())
    )


def daily(state):
    totals = {day: 0 for day in range(1, 7)}
    for assertion in state.values():
        totals[assertion.valid_day] += assertion.amount
    return totals


def rolling_three(daily_totals):
    return {
        day: sum(daily_totals.get(d, 0) for d in range(day - 2, day + 1))
        for day in range(1, 7)
    }


old_daily, new_daily = daily(old), daily(new)
changed_days = tuple(day for day in old_daily if old_daily[day] != new_daily[day])
affected = tuple(
    day
    for day in range(1, 7)
    if any(changed <= day <= changed + 2 for changed in changed_days)
)
old_rolling, new_rolling = rolling_three(old_daily), rolling_three(new_daily)
deltas = tuple((day, new_rolling[day] - old_rolling[day]) for day in affected)

try:
    conflicting = assertions + (Assertion("bad", "sale-1", 2, 11, 2, 90),)
    as_known(conflicting, 13)
    conflict = False
except ValueError:
    conflict = True

print(f"as_was_rows={rows(old)}")
print(f"restated_rows={rows(new)}")
print(f"as_was_total={sum(old_daily.values())}")
print(f"restated_total={sum(new_daily.values())}")
print(f"restatement_delta={sum(new_daily.values()) - sum(old_daily.values())}")
print(f"changed_source_days={changed_days}")
print(f"affected_output_days={affected}")
print(f"rolling_deltas={deltas}")
print(f"replay_stable={as_known(assertions + assertions, 13) == new}")
print(f"conflict_detected={conflict}")
```

At cut 5, only original sale assertions are known. At cut 13, `sale-1` revision 2 replaces 100 with 80, `sale-3` is a late-new 40, and `sale-2` revision 2 retracts 50. Treating all arrivals as inserts would produce 270 or another wrong total depending on deletion handling. The correct selected total is 120.

The changed daily inputs are day 2 (+20 net) and day 4 (−50). Their trailing-three-day influence unions to days 2–6. Day 4's rolling delta is −30 because its window includes both changes; totals alone do not identify this distribution. Duplicate replay leaves current state unchanged, and equal revision 2 with amount 90 conflicts rather than winning by arrival.

## Alternatives and Trade-Offs

| Strategy | Appropriate question | Strength | Main risk or obligation |
|---|---|---|---|
| Type 1/current overwrite | Only current accepted state matters | Simple serving/current queries | Erases prior belief unless separate history exists; historical reports silently move |
| Valid-time Type 2 | What state applied at business time? | Supports as-was validity | Does not by itself preserve when the warehouse learned/revised it |
| Bitemporal assertions | What applied when, and what was known when? | Supports current-restated and as-known analysis | More rows, interval constraints, query and correction complexity |
| Immutable event/revision ledger | Preserve every assertion/effect | Strong audit/replay | Correct fold, identities, reversals/retractions, serving projection required |
| Versioned output snapshots | Reproduce published report versions | Clear supersession and rollback | Storage/retention and consumer version selection |
| Automatic rolling restatement | High-frequency corrections in open horizon | Timely eventual accuracy | Churn, compute cost, consumer instability |
| Approval-gated final restatement | Closed/high-stakes periods | Governance and impact review | Slower correction, operational queue, residual stale output |
| Prospective adjustment | Policy forbids/rejects historical rewrite | Preserves closed version | Current period absorbs difference; not equivalent to historical truth |
| Dual as-published/restated views | Consumers need both comparison and current truth | Explicit perspectives | More contracts, storage, education, query/version discipline |
| Drop/ignore beyond lateness | Only when explicitly acceptable | Bounded streaming state/cost | Known inaccuracy and bias; requires residual-risk visibility |

Choose representation by required questions. If only current contact data matters and audit is elsewhere, Type 1 may suffice. If facts must join to business-valid dimension versions, valid-time history is needed. If prior reports/decisions must be reproduced after corrections, system/knowledge time and versioned outputs are needed.

Immutable ledgers avoid destructive history but do not automatically yield correct state. Every consumer must use the revision/retraction fold or consume a governed projection. Raw appends queried naively double count corrections.

Automatic restatement improves accuracy but can make dashboards change repeatedly. Finality stabilizes consumer expectations but delays known truth. A tiered policy—open automatic, provisional batched, final approval/prospective—often makes the trade visible.

Keeping every output snapshot can be expensive; keeping sufficient inputs/code/reference history for recomputation may be cheaper but slower and less certain. Retain exact snapshots for high-stakes publications and test reconstruction for others. Do not claim reproducibility from an untested archive.

## Failure Modes and Misconceptions

**“Late means corrected.”** A new occurrence can be late; a same-day arrival can be a correction. Classify semantic relationship separately from delay.

**“Newest arrival wins.”** Transport order may differ from source revision/authority and changes under replay. Use an authoritative order or conflict.

**“The timestamp on the event is its version.”** Event/valid time says when it applies, not which assertion supersedes another.

**“Append the corrected row and filter later.”** Consumers that miss the fold double count. Publish a governed current/restated projection or enforce revision semantics in every interface.

**“Delete the bad original.”** This destroys provenance and can make as-published reproduction impossible. Retract/supersede in protected history unless physical erasure is legally required.

**“Negative amount always reverses the original.”** It may be an independent event and needs explicit linkage/authority. Magnitude/sign alone does not establish relationship.

**“Type 2 is bitemporal.”** Valid-time versions do not necessarily record each knowledge/system revision.

**“Database system time is business valid time.”** It records database version intervals, not necessarily when the state was true in the domain.

**“Watermark means final.”** It is an estimate/processing policy. Business corrections may arrive after state cleanup and need a batch path.

**“Correct only the target row.”** Aggregates, old/new groups, windows, cumulative states, caches, and exports remain stale without affected closure.

**“Use the new key to find affected output.”** A moved/retracted row requires old key/partition/category from before-state too.

**“Global total matches, so restatement is correct.”** Group moves and offsetting missing/extra values can preserve total.

**“Final periods never change.”** Finality defines controlled handling, exceptions, and residual risk; it cannot prevent new evidence.

**“Post the difference today; users will understand.”** Prospective adjustment changes period semantics and must be separately labeled/approved.

**“Overwrite the report and update its timestamp.”** Consumers lose the prior version, reason, and reproducibility. Publish supersession lineage.

**“Time travel lasts forever.”** Snapshot/history retention and file cleanup bound availability; pin and protect required versions.

**“Retry after timeout.”** A correction, reversal, publication, or notification may already have committed. Reconcile receipts/pointers first.

**“Audit requires everyone to see old sensitive values.”** Retention and access are separate; protect/minimize historical evidence.

## Worked Examples

### Example 1

An offline device emits a new temperature observation for event time Monday on Thursday. No prior occurrence has its event ID, so this is late-new, not a correction. The raw event is appended once, Monday's affected windows are recomputed, and published outputs follow Monday's finality policy.

### Example 2

Invoice `i7` was 100 and revision 2 states 80 with explicit `revises=revision1`. A current-state projection selects 80. An immutable effect ledger records a governed retraction/replacement or domain reversal whose net is −20. It never sums both 100 and 80 as independent invoices.

### Example 3

A customer's valid region `[March 1,April 1)` changes from west to east, learned April 10. Current-restated March revenue subtracts the customer's facts from west and adds them to east. An as-published March report still uses the west assertion known at its publication cut.

### Example 4

A correction changes event day from 31 March to 1 April. Both monthly partitions, fiscal period controls, trailing windows, and downstream reports are affected. Recomputing only April adds the event without removing March.

### Example 5

Revisions arrive 1,3,2. Revision 3 is a complete after-image, so it remains winner after 2 arrives. If revision 3 were a patch based on 2, the fold would need revision 2 before applying 3; the schema contract must distinguish patch from after-image.

### Example 6

A period is final with an automatic threshold of 1,000 currency units, but 500 individually small corrections total 2,500. Policy aggregates cumulative materiality by period/source/reason and triggers approval rather than ignoring each one independently.

### Example 7

Streaming state allowed two days of lateness and has expired. A valid correction arrives after 30 days. The consumer persists it to raw revision history, emits a correction request, and uses a batch backfill from a trusted checkpoint; it does not reset the stream watermark.

### Example 8

A restatement changes only customer categories, so global revenue stays 10 million. Exact movement ledger shows −600,000 from category A, +550,000 to B, and +50,000 to C. Global-total-only validation would miss an accidental swap between B and C.

### Example 9

Two authorities submit equal revision numbers with different addresses. Their counters are not comparable and neither is globally superior. The system quarantines conflict, preserves both provenance records, blocks downstream restatement for the entity, and seeks governed resolution.

### Example 10

A new output snapshot is published and notification acknowledgement is lost. Before resending, the service queries notification idempotency receipt and dataset pointer. It avoids issuing duplicate partner exports and records whether consumers acknowledged version 12 superseding version 11.

## Cross-Program Connections

[Database Engineering](../../18-database-engineering/ROADMAP.md) supplies temporal/version tables, intervals, transactions, isolation, CDC/logs, constraints, snapshots, time travel, merges, indexes, and retention behavior.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) connects source epochs/order, at-least-once delivery, idempotence, version vectors/conflicts, event sourcing, stream time, checkpoints, consensus, and ambiguous commits.

[Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) connects interval surgery, partial maps, revision-chain folds, dependency/influence closure, incremental computation, graph reachability, and deterministic conflict detection.

[Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) connects event sourcing, audit logs, temporal patterns, commands, outbox/receipts, state machines, migrations, and compensating actions.

[Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) connects model-based temporal testing, metamorphic replay/order tests, differential oracles, mutation tests, boundary analysis, and audit evidence.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects change control, configuration baselines, finality/acceptance, hazards, human authority, verification, incident response, lifecycle records, and residual risk.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) connects stream/batch runtimes, temporal storage/catalog snapshots, workload admission, versioned publication, observability, policy, secrets, and recovery workflows.

[Security Engineering](../../25-security-engineering/ROADMAP.md) connects correction authorization, provenance integrity, least privilege, tenant isolation, privacy correction/erasure, legal holds, protected historical data, and notifications.

## References

1. Apache Beam, [Programming Guide](https://beam.apache.org/documentation/programming-guide/#watermarks-and-late-data). Documents event versus processing time, windows, watermark estimates, triggers, allowed lateness, late firings, and state garbage collection. Accessed 2026-09-02.
2. Debezium, [PostgreSQL Connector](https://debezium.io/documentation/reference/stable/connectors/postgresql.html). Documents source positions, event envelopes, updates, deletes/tombstones, key changes, transaction metadata, schemas, and duplicate delivery during recovery. Accessed 2026-09-02.
3. PostgreSQL Global Development Group, [Logical Decoding Concepts](https://www.postgresql.org/docs/current/logicaldecoding-explanation.html). Documents logical slots, ordered replay, crash-safe persistence, possible post-crash redelivery, and client progress responsibility. Accessed 2026-09-02.
4. dbt Labs, [Snapshots](https://docs.getdbt.com/docs/build/snapshots). Documents change capture for mutable tables, validity fields, unique keys, timestamp/check strategies, hard-delete modes, preserved history, and full-refresh behavior. Accessed 2026-09-02.
5. Microsoft, [Temporal Tables](https://learn.microsoft.com/en-us/sql/relational-databases/tables/temporal/overview?view=sql-server-ver17). Documents system-versioned current/history tables, engine-managed period columns, point-in-time reconstruction, and temporal use cases. Accessed 2026-09-02.
6. Apache Iceberg, [Spark Queries](https://iceberg.apache.org/docs/latest/spark-queries/). Documents snapshot/time-travel queries, schema selection, history/snapshot metadata, branches/tags, and inspection of rolled-back/non-current ancestry. Accessed 2026-09-02.
7. Apache Iceberg, [Branching and Tagging](https://iceberg.apache.org/docs/latest/branching/). Documents independent snapshot lineages/references, audit branches, validation before fast-forward, and reference/snapshot retention. Accessed 2026-09-02.
8. World Wide Web Consortium, [PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/). Defines provenance relationships for entities, activities, agents, generation, derivation, invalidation, revision, attribution, and association. Accessed 2026-09-02.
9. OpenLineage, [Object Model](https://openlineage.io/docs/spec/object-model/). Defines Job, Run, and Dataset identities plus source code, dataset version, lifecycle, partition, quality, and output-statistics facets useful for restatement lineage. Accessed 2026-09-02.

## Exercises

### Exercise 1

At knowledge cut 10, occurrence `a` is day 3 amount 70 and occurrence `b` is day 5 amount 30. By cut 20, `a` revision 2 corrects amount to 50, a late-new `c` adds day 3 amount 40, and `b` is retracted. Compute old/new totals, per-day deltas, and affected output days for a trailing four-day aggregate over days 1–9.

### Exercise 2

A customer region correction changes valid interval `[10,20)` from north to south, learned at system time 30. Explain results for current-restated valid day 15, as-known system cut 25/valid day 15, and current valid day 25. State the history required and why one `updated_at` cannot answer all three.

### Exercise 3

Revisions for one occurrence arrive in order 4,2,3. Revision 4 is a patch whose declared base is revision 3; revision 2 is a full after-image, and revision 3 is missing. Design classification/state behavior, checkpoint handling, and recovery evidence. Contrast with revision 4 as a complete after-image.

### Exercise 4

A final report total is unchanged after restatement, but 400 records move from group X to Y, 350 from Y to Z, and 50 from Z to X. Design validation and consumer communication. Explain why total equality and unchanged row count are insufficient.

### Exercise 5

A correction candidate version 8 has passed validation when another authoritative revision arrives and live output advances to version 9. Design fencing/rebase, supersession, notification idempotency, prior-version retention, and unknown-publication-outcome handling.

## Answers to the Exercises

### Answer 1

Old selected state is `a=70` on day 3 and `b=30` on day 5, total 100. New state is corrected `a=50` plus late-new `c=40` on day 3; `b` is retracted, total 90. Day 3 delta is +20 (`50+40-70`); day 5 delta is −30; overall delta is −10.

A source day affects a trailing four-day output ending on that day through three days later. Day 3 affects outputs 3–6; day 5 affects 5–8. Their union is `{3,4,5,6,7,8}`. Rolling deltas are day 3 +20, day 4 +20, days 5–6 −10 because both changes coexist, and days 7–8 −30. Recompute from canonical selected facts or verify equivalent subtract-old/add-new state.

### Answer 2

At current knowledge after time 30 and valid day 15, region is south. At system/knowledge cut 25 and valid day 15, the system still believed north. At current valid day 25, the `[10,20)` assertion does not apply; another interval/current state must determine the region.

Required evidence includes customer identity, immutable old/new assertions, business-valid intervals (including adjacent versions), system/knowledge intervals recording when each belief was accepted, source revision/authority/reason, and transactionally consistent interval surgery. A single `updated_at` cannot simultaneously encode the March-like business-effective interval and the later time the warehouse learned/corrected it, nor preserve the prior belief after overwrite.

### Answer 3

Revision 4 cannot be applied because its declared base revision 3 is missing. Preserve revision 4 as an orphan/pending patch, accept revision 2 into history if valid, alert/repair the gap, and do not manufacture revision 3 or apply patch 4 onto 2. Whether source progress can advance depends on policy: safest is to withhold the affected transaction/key checkpoint; a durable raw layer may advance source capture while the materialization checkpoint and completeness status remain behind/blocked.

Recovery evidence includes immutable envelopes for revisions 2/4, assertion IDs/digests, source epoch/positions/transactions, patch base link, schema, retention headroom, missing-position search, source reconciliation, raw/materialization checkpoints, and downstream affected outputs. When revision 3 arrives, replay 3 then 4 deterministically and restate affected closure. If revision 4 is a complete authoritative after-image, it can become current without 3 under the declared version policy, while the missing revision remains an audit/completeness issue if history requires it.

### Answer 4

Build exact before/after key-to-group mappings and movement matrix: X→Y 400, Y→Z 350, Z→X 50. Reconcile each source group's removals and destination's additions, occurrence identity/multiplicity, per-group counts and measure sums/components, global conservation, no unexpected movements, affected downstream filters/aggregates, and unchanged records. Compare prior/new output versions and sample/fully check representative records and boundaries.

Notify consumers that the global total and row count are unchanged but classifications and group results changed; provide prior/new versions, effective/restated time, affected periods/groups, movement counts/value impacts, reason/authority category, requery/refresh instructions, and support owner. Equal totals/counts can hide offsetting misclassification, missing/extra records, wrong destinations, and stale caches.

### Answer 5

Version-8 publication must carry expected output base and accepted correction cut. Once an authoritative revision arrives and live advances to 9, the stale conditional commit fails. Determine overlap: if the new revision affects the same assertion/output closure, rebuild/rebase version 8's candidate with the new revision and current reference/code/schema, validate a new candidate, then publish version 10 (or the next governed version) from expected 9. Do not publish 8 then 9 merely because 8 finished first.

The new manifest records which candidate/request was superseded and why. Notification uses stable `(dataset,new_version,prior_version)` identity and a receipt/outbox so retry cannot reissue exports/effects. Retain versions 8/9 or their reproducible evidence according to audit/rollback policy, even if 8 never became current; mark its terminal status accurately.

If publication acknowledgement is lost, inspect authoritative dataset pointer/snapshot history and publication receipt. If the candidate is current, adopt success and send/recover notification once. If prior version remains current and no receipt exists, retry conditionally. If another version is current, rebase. Never infer rollback from timeout or send a correction notice before confirming which version is visible.
