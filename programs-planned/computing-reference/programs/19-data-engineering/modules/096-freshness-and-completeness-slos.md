---
module_id: DE-096
program: Data Engineering
level: 2
module_number: 96
title: Freshness and Completeness SLOs
status: complete
last_verified: 2026-09-03
---

# Freshness and Completeness SLOs

## One-Page Review

### Governing question

How can a data product promise and measure that the right source information becomes usable by a named consumer within a bounded time and that the expected population is sufficiently represented—without confusing job success, table modification, maximum timestamps, watermarks, row counts, or available telemetry with end-to-end consumer truth?

### Essential definitions

- A **service level indicator (SLI)** is a precisely measured ratio or distribution representing a consumer-relevant aspect of service.
- A **service level objective (SLO)** is a target for an SLI over a defined reporting window and scope.
- **freshness** is the elapsed time between a governed source or event boundary and the consumer-visible product state that includes it under declared semantics.
- **staleness** is the age of the newest required usable state relative to the evaluation instant; it is not necessarily table update age.
- **completeness** is the observed eligible population, fields, partitions, or effects divided by a defensible expected population at a common boundary.
- A **coverage unit** is the denominator element—event, key, field, partition, source, tenant, or required artifact—whose good/bad outcome is evaluated.
- A **watermark** is a progress claim or estimate about event time; its meaning depends on the source and late-data contract.
- A **checkpoint** records processing position; it may not prove that a derived product is published or readable.
- A **measurement boundary** fixes source generation/offset/time, product generation, policy, scope, and observation time so numerator and denominator are comparable.
- An **unknown** is a coverage unit whose goodness cannot be established; it must not silently disappear from the denominator.
- An **error budget** is the allowed quantity or fraction of bad coverage units implied by the SLO target.
- **burn rate** is observed bad-event rate divided by the SLO’s allowed bad-event rate.
- A **correction horizon** is the period during which late or revised inputs may change a previously published result.

### Central model, mechanism, or theorem

For product $d$, scope $s$, coverage unit $i$, evaluation time $t$, source boundary $B_i$, and product evidence $P_i$, define

$$
good_i(t)=eligible_i\land published(P_i)\land age_i(t)\le F_s\land coverage_i(B_i,P_i)\ge C_s\land valid_i.
$$

The windowed SLI is

$$
SLI(W)=\frac{\sum_{i\in W}w_i\mathbf{1}[good_i]}{\sum_{i\in W}w_i},
$$

with every eligible unknown classified bad unless an explicit separately reported availability rule applies. For target $S$, allowed bad fraction is $1-S$ and burn rate is

$$
burn(W)=\frac{1-SLI(W)}{1-S}.
$$

A freshness SLO cannot prove completeness: a pipeline may publish one current row while losing the rest. A completeness SLO cannot prove freshness: every expected row may arrive days late. The contract needs independent indicators plus validity and accessibility gates.

### Critical invariants

- Every SLO names consumer decision, product/view, owner, coverage unit, scope, clocks, source boundary, product evidence, thresholds, reporting window, exclusions, correction behavior, and escalation.
- Freshness starts at the semantically relevant event/source availability boundary and ends only when the correct product generation is atomically published and usable by the consumer.
- Completeness numerator and expected denominator share the same grain, filters, policy, time interval, identity rules, and immutable boundary.
- The denominator comes from an independent or stronger contract, ledger, manifest, sequence range, reconciliation peer, or explicit statistical estimate with uncertainty—not the output being judged.
- Empty-but-valid, missing, idle, late, excluded, suppressed, deleted, and unknown states are distinguishable.
- A maximum event timestamp is accepted only with coverage evidence; a current timestamp from one record cannot certify missing partitions or keys.
- Watermark/checkpoint/run success remains scoped to its actual promise and is joined to downstream publication/read evidence.
- Backfills, corrections, schema changes, policy changes, and replay cannot overwrite historical SLO evidence or reset bad time silently.
- SLI instrumentation has its own availability, freshness, cardinality, retention, and correctness objectives; missing telemetry is observable.
- Alerts are tied to meaningful error-budget consumption and actionable ownership, with separate fast safety gates where a single missing item is intolerable.

### Common failures

Measuring schedule delay instead of data delay; using file or table modification time; subtracting `max(event_time)` without checking all partitions; measuring producer emission but not consumer-visible publication; treating a green job as a good data window; deriving expected count from the same incomplete output; comparing different filters or snapshots; averaging percentages across unequal tenants; excluding no-data intervals; treating source idleness as completeness; marking unknown telemetry good; resetting SLO history on redeploy or backfill; alerting on every threshold crossing; paging on low-volume statistical noise; reporting only fleet averages; allowing one high-volume tenant to hide another; accepting early panes as final; conflating late corrections with original delivery; and choosing 99.9% because it sounds mature rather than from consumer tolerance.

### Compact example

An hourly orders product has eight tenant-hour coverage units. Six are published within five minutes with at least 99% of independently acknowledged source events. One is current but contains 97%, and one is 12 minutes old but complete. The joint SLI is $6/8=75\%$. For an 87.5% target, one bad unit is allowed; two are bad, so the window consumes twice the allowed bad rate and has one unit of budget deficit. **Conclusion:** independent freshness and completeness gates prevent either defect from masking the other.

### Connections

[DE-049](049-run-metadata-and-operational-state.md) supplies run and attempt evidence, [DE-060](060-handling-late-duplicate-and-out-of-order-events.md) supplies event-time progress, [DE-073](073-reconciliation-tests.md) supplies common-boundary denominators, and [DE-074](074-freshness-and-timeliness.md) supplies latency decomposition. [DE-089](089-auditability-and-provenance.md) binds measurements to immutable identities; this module turns those foundations into consumer-facing objectives and budget policy.

## Governing Question

For each data-dependent decision, what is the latest tolerable source-to-usable delay, what fraction of the expected population must be present and correct, which independently observable coverage units form the denominator, and how will operators distinguish source silence, pipeline lag, incomplete inputs, publication failure, bad telemetry, and allowed correction?

## Why This Matters

Data products can be available and wrong. A dashboard may load instantly from yesterday’s cache. A feature lookup may return a current timestamp for a sparse subset. A daily table may have exactly the historical row count while the newest partition is missing. Traditional service availability sees successful requests; pipeline monitoring sees successful tasks; neither establishes that consumers received timely, sufficiently complete information.

Freshness is not one clock subtraction. An event occurs, becomes available to a source, is committed, extracted, processed, validated, published, cached, and observed. Different consumers care about different boundaries. A fraud decision needs event-to-feature latency. Finance close may care about source cutoff to certified report publication. A partner export may care about complete prior-day data by 06:00 in a named business timezone. Starting at schedule time can hide an hour of upstream delay; ending at task completion can hide failed publication.

Completeness is harder because “what should exist?” is often unknown. Counting output rows against yesterday assumes stable volume. Counting input and output without matching boundaries ignores filters, deduplication, joins, aggregation, deletion, and policy. A watermark estimates progress, not exact membership. The strongest denominators come from upstream sequence ranges, transaction ledgers, manifests, control totals, or reconciliation peers whose failure is independent enough to reveal loss.

SLOs force these semantics into a measurable promise. They also create an error budget: occasional bounded delay may be acceptable, while persistent or concentrated failures are not. A useful objective directs investment and incident response from consumer harm. A vanity percentage built from easy telemetry can instead institutionalize blind spots.

## Prerequisites and Retrieval

Retrieve the consumer decision: actor/service, product/view, query or feature set, business timezone/calendar, decision deadline, update frequency, tolerated age, required population, severity of stale/missing/wrong data, fallback, human review, downstream caches/copies, and owner/on-call.

Retrieve source semantics: event/effective time, source availability/commit time, partitions/shards/tenants, expected cadence, idle/closed periods, sequence or transaction IDs, manifests/control totals, late/reordered/corrected/deleted events, retention, replay, source SLO, clock authority/skew, and known blind spots.

Retrieve pipeline boundaries: extraction checkpoints, broker offsets, watermarks, batch data intervals, per-stage input/output counts and checksums, filters, deduplication, joins, quarantine, retries, skipped work, backfills, transformations, schema/policy versions, atomic publication, and cache invalidation.

Retrieve product evidence: immutable generation/snapshot, source boundary covered, row/key/partition/field statistics, validation status, publication/readability time, consumer-visible version, API response metadata, online-store version, export manifest, provenance, and correction horizon.

Retrieve telemetry: metric names/types/units, event versus collection timestamps, dimensions/cardinality, aggregation temporality, missing-series behavior, scrape/export delay, sampling, resets, retention, dashboards, alert rules, paging routes, incident annotations, and independent synthetic/read probes.

Retrieve governance: eligibility, tenant/region, row/field policy, consent/deletion/suppression, contractual deadlines, exclusions, maintenance, exceptions, approval, audit retention, and communication requirements. Policy exclusions must not be misclassified as pipeline loss, but an incorrectly applied exclusion is a validity failure.

Distinguish occurrence from availability; processing progress from consumer visibility; source inactivity from missing data; a watermark estimate from final completeness; schedule punctuality from data freshness; maximum timestamp from population coverage; row count from key/field completeness; deduplication from loss; early answer from final answer; correct empty from unknown empty; SLI from SLO; error budget from a permission to ignore harm; data-product failure from telemetry failure; and repair time from original good-event classification.

Create an SLO contract:

| Concern | Required evidence and decision |
|---|---|
| Consumer | Decision, product/view, scope, deadline, harm, fallback and owner |
| Unit | Event, key, field, partition, tenant-window or artifact; weight and eligibility |
| Freshness | Start/end boundaries, clocks, threshold, source idleness and publication evidence |
| Completeness | Expected denominator, numerator, grain/filter/boundary, uncertainty and validity |
| Objective | Target, reporting window, correction/finality, exclusions and budget policy |
| Telemetry | Instruments, dimensions, missing-data semantics, retention and validation |
| Response | Fast gates, budget alerts, diagnosis, escalation, communication and repair |
| Lifecycle | Backfill, evolution, exception, audit, consumer change and retirement |

Write a falsifiable claim: “For product D and eligible tenant-hour unit U, at least 99% of units over rolling 30 days publish generation G usable through consumer path C within five minutes of the authoritative source-close boundary; each generation reconciles at least 99.95% of eligible source transaction IDs from independently signed manifest M at the same cutoff; schema/policy checks pass; unknown telemetry is bad; excluded maintenance is predeclared; late correction is reported separately; and multiwindow burn alerts route to owner O with runbook R.”

## Learning Objectives

After completing this module, you should be able to:

1. distinguish schedule, ingestion, processing, publication, observation, event, and source-availability time;
2. define consumer-relevant freshness and completeness coverage units, SLIs, SLOs, windows, targets, and error budgets;
3. construct defensible expected denominators from ledgers, manifests, sequences, partitions, inventories, control totals, or statistical estimates;
4. separate row, key, field, partition, source, tenant, window, and semantic completeness;
5. use watermarks, checkpoints, counts, checksums, publication receipts, lineage, and probes without overstating their evidence;
6. aggregate ratios with correct weighting and expose tail, tenant, region, source, and low-volume behavior;
7. model empty, idle, late, corrected, deleted, suppressed, quarantined, excluded, and unknown states explicitly;
8. design instrumentation, budget dashboards, multiwindow burn alerts, fast safety gates, diagnosis, and error-budget policy;
9. preserve honest history through backfills, corrections, schema/policy evolution, telemetry outages, and SLO changes; and
10. negotiate SLOs from consumer harm, cost, source capability, and evidence rather than copying generic reliability targets.

## Core Exposition

### Start from a consumer-visible good event

Define one eligible coverage unit and its good outcome. Request-based services often use one request. Data products may use a tenant-hour, required partition-day, expected transaction, feature lookup, report generation, or consumer read. The unit should match harm and be countable without unbounded cardinality.

Example: “Each eligible region-hour is good when the certified inventory view contains every committed warehouse movement through hour end and is queryable by planners by five minutes past.” This binds population, cutoff, product, consumer and time. “Pipeline finishes by :05” does not.

Define scope and weighting. Equal tenant-hour weighting protects small tenants but may overstate impact relative to events. Event weighting reflects volume but lets high-volume tenants hide total failure for small ones. Publish both when decisions need both. Never average tenant percentages directly unless equal weighting is intentional; sum good and total weights.

Eligibility precedes outcome. Planned source closure, tenant not launched, and policy-valid exclusion can be ineligible if predeclared. A source unexpectedly silent is not retroactively excluded. Unknown and missing evidence are bad for the primary SLI or reported in a separate measurement-availability SLI whose failure still triggers action.

### Decompose freshness across clocks and boundaries

For event $e$, record occurrence $T_e$, source availability/commit $T_a$, ingestion $T_i$, processing completion $T_p$, atomic publication $T_u$, and consumer observation $T_o$. Useful lags include source delay $T_a-T_e$, ingestion lag $T_i-T_a$, processing lag $T_p-T_i$, publication lag $T_u-T_p$, delivery/cache lag $T_o-T_u$, and end-to-end $T_o-T_e$ or $T_o-T_a$.

Choose start boundary from the promise. If an upstream device can be offline for hours, event-to-product includes that reality when consumer harm starts at occurrence. If the data team contracts only from durable upstream commit, state the upstream dependency and report occurrence-to-commit separately. Do not hide external delay merely by narrowing ownership.

End at usable state. A write into staging, successful SQL statement, advanced checkpoint, or swapped table is insufficient if validation failed, catalog points to old state, API cache remains stale, permissions block reads, or online serving has not materialized. Use an immutable product generation plus a read probe through the actual consumer path.

Clocks need UTC instant semantics, precision, synchronization bounds, and monotonic duration handling. Client clocks may be untrusted. Negative lag indicates skew or bad timestamps and is a validity failure, not excellent freshness. Business deadlines such as “by 06:00 local” require timezone and daylight-saving rules.

### Define completeness with an independent denominator

Completeness has dimensions. Row completeness asks whether expected records arrived. Key completeness covers required entities. Field completeness covers required non-null or semantically populated fields. Partition/source completeness covers structural inputs. Semantic completeness asks whether values and relationships satisfy the business contract. A product can pass one and fail another.

Use the strongest available expected population. A source transaction ledger with stable IDs supports exact membership reconciliation. A producer manifest gives expected objects, records, bytes, sequence ranges and checksums. A closed partition inventory proves required shards. Domain control totals such as invoice count and amount detect loss beyond rows. A slowly changing entity registry supports expected-key coverage.

The denominator must not be derived from the same output defect. `observed / max(observed, expected)` or “100% of rows that arrived passed” says nothing about missing rows. Yesterday’s count is an anomaly baseline, not exact expectation. When only statistical expectation exists, report confidence/seasonality and call the indicator estimated completeness; do not present it as exact.

Align the comparison. Source and target share cutoff, eligibility, tenant, key normalization, deletion/suppression, deduplication, schema/policy generation and units. An upstream count before filtering cannot directly equal an aggregated target. Build conservation equations for each transformation: candidates = included + filtered by named reason + deduplicated + quarantined + late/pending + failed/unknown.

### Treat watermarks and checkpoints as scoped evidence

A watermark is a progress assertion or estimate over event time. In many stream models, it indicates the system believes earlier events are unlikely or contractually not expected; late events may still arrive and be dropped, updated, or accumulated. Record the generator, partition scope, lateness policy, idleness, and correction semantics.

Global progress is commonly bounded by the slowest non-idle input. Marking a partition idle can unblock computation, but it is a correctness choice: distinguish legitimately inactive from failed or disconnected. Watermark alignment can bound state growth by slowing fast sources; it does not create missing data.

A checkpoint or offset proves that a consumer recorded a position under its protocol. It may precede transformation effects, publication, downstream cache invalidation, or external writes. Join checkpoint evidence to per-boundary counts/IDs and final generation receipt. A job success proves only its coded success condition; validate content independently.

Early panes are intentionally incomplete. Mark them provisional, carry pane/version and completeness estimate, and do not mix them with final results. Define allowed lateness and corrections. A final marker under one engine configuration does not mean real-world data can never be corrected.

### Build freshness indicators that resist false green

For scheduled batches, measure the selected source boundary and publication time per expected partition/tenant, not only wall-clock run duration. A no-op run needs proof that the source boundary had no eligible change; otherwise fast completion can be total loss. Use source manifests or independent probes.

For streams, measure distributions of event-to-usable latency for accepted events and separate backlog age, watermark lag, latest source commit versus product coverage, and late/drop/correction rates. Sampling latency alone can miss dropped events because lost events produce no terminal observation. Completeness supplies the missing denominator.

For state products, report consumer observation age relative to the generation’s covered source boundary. `now - max(event_time)` is safe only when the maximum is representative and all required coverage is proven. Per-partition minima or required-source coverage prevents one fast partition from hiding one stuck partition.

For APIs and feature stores, include response generation, as-of/event boundary, policy/schema version and freshness reason. A low-latency response from stale cached data is not fresh. Synthetic reads through the same routing/cache/authorization path validate usability, while provenance ties the result to source progress.

### Measure completeness at multiple grains

Exact ID reconciliation gives missing, extra, duplicate, conflicted and unknown sets. Counts and sums are cheaper but can cancel: one missing $10 transaction and one duplicate $10 transaction preserve count and total. Use layered checks: structural partitions/files, record counts, distinct keys, domain control sums, hashes or sketches, and sampled/full keyed reconciliation according to risk.

Field completeness is contract-specific. Null may be valid, unknown, redacted, not applicable or missing. Measure required-state classification rather than raw non-null percentage. For nested/repeated fields, define parent eligibility and cardinality. A column can be populated but semantically defaulted to zero after parser failure.

Join completeness includes match classes. An inner join can make output appear perfect by dropping unmatched left rows. Preserve the driving population and measure unmatched, multi-match, fan-out and unknown identity. Aggregate outputs need group/domain coverage and conservation across groups.

Expose slices. Overall 99.99% can coexist with zero coverage for one country, new tenant or rare event type. Choose bounded dimensions tied to ownership and harm; avoid high-cardinality metric labels by storing detailed evidence in queryable tables and exporting aggregated metrics.

### Combine indicators without concealing failure

Define separate freshness $F_i$, completeness $C_i$, validity $V_i$ and accessibility $A_i$. A strict joint good event is their conjunction. Report each marginal indicator for diagnosis. A weighted average such as 50% freshness + 50% completeness lets total failure of one dimension appear acceptable and should not gate correctness.

Some products have graded utility. A dashboard may accept 98% complete by :05 and 99.99% by :30. Express this as multiple explicit objectives or a time-to-completeness distribution, not a vague blended score. Safety-critical keys may use an absolute zero-miss gate alongside fleet SLOs.

Define correction quality separately. Original delivery SLI remains bad if a row was late even after repair. Measure time to correct, final completeness at correction horizon, and residual unreconciled items. Rewriting history would eliminate the evidence needed for capacity and reliability decisions.

For low volume, ratios are noisy and error budgets discrete. One bad daily report may be substantial. Use event windows, longer reporting periods, exact counts, synthetic probes, or absolute gates. State uncertainty for sampled indicators.

### Instrument numerator, denominator and measurement health

Emit durable per-unit evidence before aggregating: product/generation, source boundary, tenant/scope, expected and observed identifiers/counts/control totals, coverage result/reason, relevant timestamps, policy/schema versions, run/attempt, publication/read probe, and correction state. Aggregated metric labels remain low-cardinality; exemplars or protected receipts link to detail.

Counters suit good and total coverage events when resets and temporality are understood. Gauges represent current lag/backlog but can go missing or stale. Histograms represent latency/time-to-completeness distributions when buckets align with objectives. Preserve units and event/collection timestamps. Do not average precomputed percentiles across shards.

Instrument the observer. Track last successful evaluation, evaluation duration, source/product query failures, missing expected units, late telemetry, dropped metric points, cardinality limits, exporter backlog and clock anomalies. Run synthetic fixtures with known missing/late/duplicate states and compare SLO computation with raw evidence.

Retain evidence for the reporting window, incident analysis and governed audit. Telemetry can reveal tenant volume, customer identity or sensitive operations; minimize dimensions, protect detailed receipts and apply retention/access controls.

### Set objectives and error-budget policy from harm

Begin with consumer tolerance and source capability. Identify the point at which stale or missing data changes decisions, creates financial/security/safety harm, violates contract or forces fallback. Measure current distributions and failure modes, then set an objective that is useful, affordable and tighter than the harm boundary where feasible.

An SLO target and window imply allowed bad units. For target 99% over 10,000 equal units, 100 may be bad; which 100 matters. Add per-tenant or consecutive-failure constraints when concentration causes disproportionate harm. Error budget is not permission to neglect known severe misses.

Write policy before exhaustion: who reviews burn, when risky releases/backfills pause, what reliability work is prioritized, how exceptions are approved, and when consumers are notified. Distinguish experimental product tiers and contractual commitments. An internal SLO should not accidentally promise more or less than an external obligation.

Revisit targets when consumer workflow, volume, source behavior, architecture or measurement changes. Preserve old series and annotate contract/version boundaries; never splice incomparable SLIs into one trend.

### Alert on actionable budget consumption

Page for significant fast error-budget burn with an actionable owner and runbook. Multiwindow, multiburn alerts combine a short window for detection with a longer window for significance, reducing pages for brief noise. Ticket or notify on slow burn before the long-window budget exhausts. Safety invariants may page immediately independent of budget.

Include absolute counts and measurement health in low-volume alerts. A ratio from one event is not stable, but one missed regulatory report can be critical. Require minimum traffic only where the missed units are individually low impact; otherwise use direct deadline/heartbeat probes.

Alert context should name product/scope, contract version, bad/good/total, thresholds, burn, top failure reasons/slices, first/last bad boundary, current source/product generations, telemetry health, likely stage, lineage and links to detailed protected evidence. Do not attach sensitive rows.

Symptoms page the product owner; cause alerts assist diagnosis and may ticket platform owners. Avoid paging separately for every failed task when one consumer SLO incident already owns response. Test alert precision, recall, detection and reset through injected delay/loss/telemetry faults.

### Diagnose and repair without erasing evidence

Classify failure: source late/silent; missing partition; extraction lag; queue backlog; processing failure; quarantine/schema/policy rejection; partial join; publication/catalog/cache failure; consumer access; observer failure; or definition mismatch. Compare source and product boundaries stage by stage using lineage and conservation receipts.

Stop destructive retries when completeness is uncertain. A rerun may duplicate effects or publish a partial generation as latest. Pin source boundary, create a repair generation, reconcile before cutover, publish atomically, invalidate caches, and verify consumer reads. Preserve original bad event plus correction time and generation.

Communicate impact in consumer language: affected periods/tenants/fields, stale-as-of boundary, missing population estimate or exact set, decisions affected, fallback, correction status and next update. “DAG failed” is implementation detail.

Run post-incident review against SLO evidence. Ask whether denominator, coverage units, slices, instrumentation and alerts represented actual harm. Fix measurement contracts when the incident was invisible or over-alerted.

### Evolve and retire SLOs safely

Changing source timestamp, expected-population logic, weights, eligibility, late policy, product view, timezone, target or window changes the SLI. Version it, dual-compute old/new over common boundaries, explain expected deltas, review with consumers and migrate dashboards/alerts. Do not backfill new logic into old history without labeling recomputation.

Schema or policy evolution can change completeness legitimately. Bind numerator and denominator to the same generation and retain reason counts. A newly redacted field is not missing if the product contract says redacted, but incorrect redaction is invalid.

Retirement inventories dashboards, alerts, paging routes, reports, contracts, APIs, exports and downstream derived SLOs. Stop measurement only after consumers and dependencies migrate or explicitly accept removal; retain historical evidence according to policy. An unused dashboard is not proof an SLO has no consumer.

## Definitions and Notation

Let $I_W$ be eligible coverage units in reporting window $W$, with nonnegative weight $w_i$. Let freshness lag $L_i=T_{usable,i}-T_{start,i}$ and threshold $F_i$. Let expected set $E_i$ and correctly observed set $O_i$ share boundary $B_i$; exact completeness is

$$
C_i=\frac{|E_i\cap O_i|}{|E_i|},
$$

with explicit convention for $|E_i|=0$. Extra and duplicate records are separate validity failures; they do not increase completeness above one.

Define component indicators $f_i=\mathbf{1}[L_i\le F_i]$, $c_i=\mathbf{1}[C_i\ge C_i^*]$, $v_i$ for schema/semantic validity and $a_i$ for consumer accessibility. Joint good is $g_i=f_ic_iv_ia_i$. Unknown component evidence sets $g_i=0$ for the primary objective unless the versioned contract says the unit is ineligible.

Then

$$
SLI_W=\frac{\sum_{i\in I_W}w_ig_i}{\sum_{i\in I_W}w_i},\qquad budget_W=(1-S)\sum_iw_i-\sum_iw_i(1-g_i).
$$

For fraction-based burn when $S<1$,

$$
burn_W=\frac{1-SLI_W}{1-S}.
$$

Negative budget means excess bad weight beyond allowance. Burn is undefined for a 100% target; absolute invariant handling is required.

Let watermark $M_p(t)$ be progress for partition $p$. A combined minimum $M(t)=\min_{p\in active}M_p(t)$ is meaningful only under declared active/idleness rules and watermark semantics. It is not an exact $E_i$ unless the protocol proves membership/closure.

## Mechanisms, Invariants, or Proof Structure

### SLO construction and operation mechanism

1. Name the consumer decision, product/view, owner, harm boundary, fallback and candidate coverage unit.
2. Define eligibility, scope, weighting, timezone/calendar, source start and consumer-usable end boundaries.
3. Specify freshness threshold and an independent expected-population source for completeness at a shared boundary.
4. Define field/key/partition/semantic validity, empty/idle/unknown/late/corrected/excluded states and finality horizon.
5. Choose target/reporting window, concentrated-harm constraints, fast invariants and error-budget policy.
6. Instrument durable per-unit numerator, denominator, timestamps, generations, provenance and consumer read evidence.
7. Aggregate good/total with correct weighting; expose marginal components, slices, tails, counts and measurement health.
8. Validate computation with fixtures, raw-evidence recomputation, fault injection and independent probes.
9. Alert on fast/slow budget burn and safety gates; route symptom ownership with diagnostic context and runbooks.
10. Repair through pinned boundaries and new generations; preserve original bad classifications and correction metrics.
11. Review incidents, false negatives/positives, target economics, source dependencies and consumer outcomes.
12. Version and dual-run definition changes; retire only after consumer and downstream measurement migration evidence.

### Conditional claim: independent joint gates prevent mutual masking

**Claim.** If every eligible unit is marked good only when both freshness and completeness predicates pass at the same boundary, then a unit failing either predicate cannot be counted good in the joint SLI.

**Proof sketch.** Joint goodness is logical conjunction $g_i=f_i\land c_i\land v_i\land a_i$. If $f_i=0$ or $c_i=0$, conjunction is zero regardless of the other components. Summation cannot add its weight to the numerator. The claim fails operationally if units disappear from the denominator, eligibility is changed after observation, unknown is treated good, component evidence uses different boundaries, or a blended average replaces conjunction.

### Conditional claim: exact membership reconciliation bounds missing records

**Claim.** For a finite independently known expected ID set $E$ and correctly normalized observed set $O$ at the same boundary, $|E\setminus O|=|E|-|E\cap O|$ exactly counts missing expected IDs.

**Proof sketch.** $E$ is the disjoint union of $E\cap O$ and $E\setminus O$; cardinality is additive. Extras $O\setminus E$ and duplicates require separate classification and do not reduce missing count. The claim fails if $E$ is incomplete/nonindependent, IDs collide/change, boundaries or eligibility differ, normalization is wrong, or multiplicity rather than set membership matters.

### Executable joint-SLO accounting illustration

This deterministic fixture evaluates eight equal tenant-hour units under five-minute freshness and 99% completeness thresholds, then calculates an 87.5% SLO budget. It illustrates ratio and burn arithmetic; it does not establish a trustworthy denominator, telemetry, weighting, low-volume policy, or production alert.

<!-- bijux-verify: {"id":"joint-freshness-completeness-slo","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"total=8\ngood=6\nbad=2\nsli=0.750\nallowed_bad=1.000\nerror_budget_remaining=-1.000\nburn_rate=2.000\nfreshness_failures=1\ncompleteness_failures=1\n","stderr":""}} -->
```python
units = [
    {"lag": 2, "coverage": 1.00},
    {"lag": 3, "coverage": 1.00},
    {"lag": 4, "coverage": 0.99},
    {"lag": 1, "coverage": 1.00},
    {"lag": 5, "coverage": 1.00},
    {"lag": 2, "coverage": 0.995},
    {"lag": 3, "coverage": 0.97},
    {"lag": 12, "coverage": 1.00},
]
fresh_limit = 5
complete_limit = 0.99
target = 0.875

freshness_failures = sum(unit["lag"] > fresh_limit for unit in units)
completeness_failures = sum(unit["coverage"] < complete_limit for unit in units)
good = sum(
    unit["lag"] <= fresh_limit and unit["coverage"] >= complete_limit
    for unit in units
)
total = len(units)
bad = total - good
sli = good / total
allowed_bad = (1 - target) * total
remaining = allowed_bad - bad
burn = (1 - sli) / (1 - target)

print(f"total={total}")
print(f"good={good}")
print(f"bad={bad}")
print(f"sli={sli:.3f}")
print(f"allowed_bad={allowed_bad:.3f}")
print(f"error_budget_remaining={remaining:.3f}")
print(f"burn_rate={burn:.3f}")
print(f"freshness_failures={freshness_failures}")
print(f"completeness_failures={completeness_failures}")
```

## Alternatives and Trade-Offs

- **Event-weighted versus tenant/window-weighted:** event weighting tracks volume impact; equal tenant/window weighting exposes small-customer outages. Report both when neither represents all harm.
- **Exact ledger versus statistical baseline:** exact membership is strongest but can be costly or unavailable; seasonal forecasts detect anomalies cheaply but require uncertainty and cannot certify exact completeness.
- **End-to-end versus stage SLO:** end-to-end matches consumer harm; stage indicators accelerate ownership and diagnosis. Stage success never substitutes for the product objective.
- **Event occurrence versus source commit start:** occurrence captures full user delay; commit creates a controllable boundary. Show upstream dependency rather than silently discarding it.
- **Maximum timestamp versus per-partition progress:** one maximum is cheap and fragile; minimum/coverage across required partitions resists masking but needs inventory and idle semantics.
- **Strict final versus provisional early results:** strict finality improves consistency; provisional outputs reduce latency when consumers understand versions and corrections.
- **Joint indicator versus separate objectives:** conjunction prevents masking and provides one budget; marginal objectives make diagnosis and differentiated promises clearer. Use joint plus marginals.
- **Rolling versus calendar window:** rolling windows show current reliability continuously; calendar windows align contracts/operations but have edge and reset behavior.
- **Ratio versus absolute deadline gate:** ratios tolerate bounded misses; an absolute gate protects singular high-impact reports/keys. Mixed criticality often needs both.
- **Fast page versus slow ticket:** paging limits response delay for rapid burn; tickets fit gradual reliability debt. Multiwindow rules and safety overrides allocate each.
- **Correction rewrite versus immutable history:** rewriting makes current truth neat; immutable SLO events preserve actual consumer experience and reliability evidence.
- **High-cardinality metrics versus detailed evidence table:** rich labels speed slicing but threaten telemetry cost/reliability; low-cardinality metrics linked to protected receipts preserve both uses.
- **Tight target versus cost/flexibility:** stronger objectives reduce tolerated harm but demand capacity, source guarantees and complexity. Derive from decision value and failure cost.
- **Common fleet SLO versus tiered products:** one standard simplifies governance; tiers reflect differing harm/cost but require explicit routing, measurement and consumer expectation.

## Failure Modes and Misconceptions

1. **“A successful job means fresh data.”** It may process old/no input or fail publication and cache refresh.
2. **“Table modification time is freshness.”** DDL, compaction or empty writes can move it; data may change without it representing consumer state.
3. **“`max(event_time)` proves freshness.”** One current record can hide missing sources, partitions and keys.
4. **“A watermark proves completeness.”** It is a scoped progress claim/estimate under lateness and idle rules.
5. **“A checkpoint proves the product includes the data.”** Downstream transformation, publication and reads may not be complete.
6. **“No input means nothing was expected.”** Source outage and legitimate idleness need independent evidence.
7. **“Output count is its own denominator.”** Lost data disappears from both numerator and inferred expectation.
8. **“Yesterday’s volume is exact expectation.”** Seasonality, growth and real events change; it is anomaly evidence only.
9. **“Equal row counts prove completeness.”** Missing and duplicate rows can cancel; fields/keys/semantics can still fail.
10. **“Null percentage measures field completeness.”** Null, unknown, redacted, inapplicable and parser-defaulted values differ.
11. **“Inner-join output proves matched inputs.”** Unmatched driving rows vanish unless explicitly accounted.
12. **“Average tenant percentages is the global ratio.”** Only if equal tenant weighting is the intended unit.
13. **“Fleet volume protects every tenant.”** Large tenants can mask total small-tenant outages.
14. **“Freshness and completeness can be averaged.”** A blended score can hide total failure in one dimension.
15. **“Unknown telemetry should be excluded.”** This creates false green precisely when observation fails.
16. **“A repaired interval was always good.”** Repair time is separate; historical user impact remains.
17. **“Backfill should reset the budget.”** It may fix state but must not erase original late/missing experience.
18. **“99.9% is intrinsically better.”** An unaffordable or unmeasurable target produces gaming and noise.
19. **“Error budget permits any misses.”** Concentrated or safety-critical failures can violate separate constraints.
20. **“Short-window threshold alerts are SLO alerts.”** They often page on insignificant noise or miss meaningful slow burn.
21. **“Low traffic makes SLOs impossible.”** Use exact counts, longer/event windows, deadline probes and severity-aware gates.
22. **“Metrics are ground truth.”** Collection, aggregation, reset, labels, sampling and observer outages can corrupt them.
23. **“Percentiles average across shards.”** Quantiles are not generally composable; merge distributions/histograms appropriately.
24. **“Changing the query preserves the SLI.”** Boundary, denominator, weight or eligibility changes create a new indicator version.
25. **“No dashboard viewer means no consumer.”** Alerts, contracts, automation and derived objectives may depend on it.

## Worked Examples

### Example 1

**Situation.** A daily report job finishes at 05:58, but its source boundary is prior-prior day. **Reasoning.** Schedule punctuality passes while source-to-certified publication freshness fails. The SLI reads the generation’s covered cutoff, not task time. **Conclusion.** Fast computation of old data is stale.

### Example 2

**Situation.** One shard emits a current event while three shards stop. **Reasoning.** Global `max(event_time)` looks current. Required-shard inventory plus per-shard progress marks three units missing and the product incomplete. **Conclusion.** Maximums need coverage evidence.

### Example 3

**Situation.** Source manifest expects 1,000 transaction IDs; target has 999 expected IDs plus one duplicate. **Reasoning.** Row count is 1,000, but set reconciliation reports one missing and a duplicate/extra occurrence. **Conclusion.** Counts can conserve while membership fails.

### Example 4

**Situation.** A store closes on Sundays and emits nothing. **Reasoning.** A signed calendar/source-close control marks the day legitimately empty; absence without that independent state is unknown and bad. **Conclusion.** Empty and missing require distinct evidence.

### Example 5

**Situation.** A stream marks an inactive partition idle, then late events arrive. **Reasoning.** Early windows were provisional under idleness/lateness policy; corrections emit new panes and original time-to-first/final-completeness remain. **Conclusion.** Unblocked watermarks do not erase correction semantics.

### Example 6

**Situation.** Overall key coverage is 99.99%, but a new region has 0%. **Reasoning.** Volume-weighted fleet SLO passes; a region-window SLO and zero-coverage gate expose concentrated harm. **Conclusion.** Weighting expresses whose failure counts.

### Example 7

**Situation.** Metrics exporter stops during a pipeline outage. **Reasoning.** Missing series would make a naïve query return no failures. Expected evaluation heartbeats mark units unknown/bad and a measurement-health alert fires. **Conclusion.** Observe the observer.

### Example 8

**Situation.** A backfill repairs yesterday’s missing partition. **Reasoning.** A new generation becomes complete and correction time is recorded, but yesterday’s original good/bad unit remains bad for the reliability SLO. **Conclusion.** Current correctness and historical reliability are different records.

### Example 9

**Situation.** A 99% objective over eight equal units permits 0.08 failures, so one failure creates high burn. **Reasoning.** The team uses a longer event window, exact counts and a report-deadline gate rather than suppressing the single severe miss with minimum traffic. **Conclusion.** Low volume needs discrete reasoning.

### Example 10

**Situation.** A team replaces source loaded-time with event-time freshness. **Reasoning.** It dual-computes both, finds systematic source delays, versions the SLI, updates ownership and preserves old history rather than splicing series. **Conclusion.** Measurement evolution is a contract migration.

## Cross-Program Connections

- [DE-049](049-run-metadata-and-operational-state.md), [DE-055](055-delivery-semantics-in-streaming-pipelines.md), and [DE-060](060-handling-late-duplicate-and-out-of-order-events.md) distinguish run, delivery, checkpoint, event-time and correction evidence.
- [DE-063](063-table-metadata-and-snapshots.md), [DE-066](066-time-travel-and-reproducible-reads.md), and [DE-073](073-reconciliation-tests.md) provide immutable boundaries, reproducibility and exact comparison.
- [DE-074](074-freshness-and-timeliness.md), [DE-076](076-data-contracts.md), and [DE-089](089-auditability-and-provenance.md) provide latency decomposition, consumer contracts and joined evidence.
- [DE-091](091-warehouses-query-engines-and-serving-stores.md), [DE-092](092-materialized-views-and-derived-tables.md), and [DE-094](094-data-apis.md) define the serving, publication and consumer-observation surfaces measured here.
- [DE-095](095-feature-and-training-dataset-pipelines.md) applies point-in-time availability and population completeness to training/serving features and labels.
- [API-071](../../28-api-and-service-engineering/modules/071-timeout-and-deadline-budgets.md), [API-074](../../28-api-and-service-engineering/modules/074-api-level-load-shedding.md), and [API-079](../../28-api-and-service-engineering/modules/079-consistency-and-read-after-write-expectations.md) connect deadline, overload, and consumer observation semantics.
- [PLAT-081](../../29-platform-engineering/modules/081-platform-service-level-objectives.md), [PLAT-084](../../29-platform-engineering/modules/084-platform-dependency-mapping.md), and [PLAT-087](../../29-platform-engineering/modules/087-incident-response-for-shared-platforms.md) connect objective portfolios, dependency ownership, and incident response.
- [DE-097](../ROADMAP.md) uses these measured lag/backlog/completeness demands to plan pipeline capacity and cost.

## References

- Google, “Implementing SLOs,” *Site Reliability Engineering Workbook*. <https://sre.google/workbook/implementing-slos/>
- Google, “Alerting on SLOs,” *Site Reliability Engineering Workbook*. <https://sre.google/workbook/alerting-on-slos/>
- Apache Beam project, “Basics of the Beam Model,” current documentation. <https://beam.apache.org/documentation/basics/>
- Apache Flink project, “Generating Watermarks,” current stable documentation. <https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/event-time/generating_watermarks/>
- OpenTelemetry project, “Metrics Data Model,” current specification. <https://opentelemetry.io/docs/specs/otel/metrics/data-model/>
- Prometheus project, “Histograms and Summaries,” current best-practice documentation. <https://prometheus.io/docs/practices/histograms/>
- OpenLineage project, “Facets and Extensibility,” current specification documentation. <https://openlineage.io/docs/spec/facets/>
- OpenLineage project, “Lineage Dataset Facet,” current specification documentation. <https://openlineage.io/docs/spec/facets/dataset-facets/lineage/>
- dbt Labs, “Source Freshness,” current documentation. <https://docs.getdbt.com/docs/deploy/source-freshness>
- Internet Engineering Task Force, *Date and Time on the Internet: Timestamps*, RFC 3339, 2002. <https://www.rfc-editor.org/rfc/rfc3339.html>

## Exercises

### Exercise 1

For eight tenant-hour units with the lags and completeness fractions in the executable, calculate component failures, joint good/bad, SLI, allowed bad weight, remaining budget and burn for an 87.5% target. Then compare event weighting when the stale tenant has 90% of events.

### Exercise 2

Design freshness and completeness SLOs for a daily finance report due at 06:00 local time from four sources. Include cutoff, manifests/control totals, timezone/DST, empty days, corrections, certification, publication/read probe, unit/weights, target/window, hard gates, and alerts.

### Exercise 3

A streaming product has 64 partitions, watermarks, checkpoints, late updates, idle detection, deduplication, quarantine, materialized views, and an API cache. Design stage evidence and an end-to-end good event that cannot be fooled by one fast partition, lost events, premature acknowledgment, or stale cache.

### Exercise 4

An upstream cannot provide exact expected counts. Design layered estimated completeness using partition inventory, seasonal volume ranges, distinct keys, control sums, producer heartbeats and downstream reconciliation. State uncertainty, blind spots, and when it must block publication.

### Exercise 5

An estate has 400 freshness checks based on table modification time, averages tenant percentages, excludes missing metrics, pages every threshold breach, resets dashboards after backfills, and has no consumer owners. Design a risk-prioritized recovery with measurable completion evidence.

## Answers to the Exercises

### Answer 1

Six units pass both thresholds. Unit seven has lag 3 but coverage 0.97, so it is the single completeness failure. Unit eight has coverage 1.00 but lag 12, so it is the single freshness failure. There is no overlap: joint good=6, bad=2, SLI=6/8=0.75. Target 0.875 permits `(1-0.875)*8=1` bad unit. Remaining budget is `1-2=-1`; bad fraction 0.25 divided by allowed 0.125 gives burn 2.0.

If the stale tenant carries 90% of event weight, an event-weighted SLI is at most about 10% even though equal tenant-hour SLI is 75%, depending on the remaining distribution. Conversely, if one failed small tenant carries almost no volume, event weighting can look nearly perfect. Neither is universally right: publish event impact and tenant fairness, then bind response to consumer harm. Never average already computed percentages without preserving weights.

### Answer 2

Define one business-date report as the primary unit, plus per-source-date diagnostic units. The source cutoff is certified close for all four sources, not job schedule. Each producer supplies a manifest with date, timezone, files/partitions, record IDs or counts, currency/control sums, schema and close signature. Business calendar declares closed days and DST: use a named IANA zone for deadline, represent instants in UTC, and test short/long transition days.

Freshness passes when a validated immutable report generation covering all four certified cutoffs is atomically published and a planner-role probe reads it by 06:00. Completeness passes when required manifests exist, all files/IDs reconcile, transformation conservation accounts for every record by reason, financial control totals balance under approved tolerance, required fields/groups exist, and certification succeeds. A legitimate closed day has an explicit zero manifest; silence is unknown/bad.

Use a hard 100% deadline gate for each report if one missing close is materially harmful, plus a rolling objective for on-time certified reports over a quarter. Corrections publish new generations, retain original delivery classification and measure correction time/final completeness. Page immediately near/past deadline for missing manifest, failed balance, publication/read failure or telemetry failure; ticket slow recurring source delay. Notify finance with covered cutoff, affected sources/accounts, estimated/exact impact and fallback. Do not call a technically published but uncertified report good.

### Answer 3

At each source partition record latest durable sequence, event-time distribution, producer manifest/range or accepted ID ledger, heartbeat and watermark with idle reason. Ingestion records received IDs/counts, duplicates, late events and durable checkpoint separately. Processing records per-boundary input, output, filtered, deduplicated, quarantined and failed counts/IDs; checkpoint occurs only at its documented milestone. Materialized generation records included source positions, validation, checksum, publication time and atomic pointer. API/cache reports served generation/as-of boundary and synthetic authorized reads.

One partition-window good event requires every required active partition or independently certified idle partition, complete membership/control reconciliation through boundary B, no unexplained gaps, allowed late/correction policy applied, transform accounting closed, schema/semantic checks passed, generation containing B published, and the API probe serving that generation within threshold. Combine progress uses the slowest required partition; a fast maximum cannot dominate. Lost events remain in expected-minus-observed. A checkpoint alone cannot close the unit. Cache generation mismatch fails accessibility/freshness.

Track provisional early results separately and update corrections without rewriting original good/bad. Diagnose source, ingestion, processing, quarantine, publication and cache marginals. Instrument expected evaluations so missing telemetry becomes an observer failure rather than disappearing.

### Answer 4

Build a hierarchy rather than manufacture an exact percentage. A source inventory declares required partitions/shards and expected cadence; heartbeats distinguish operating/closed from silent. Seasonal models predict count/byte/distinct-key ranges by tenant, weekday, holiday and release, with confidence intervals and anomaly scores. Domain control sums—amount, units, min/max sequence, first/last time—detect some offsetting loss. Compare distinct keys and sketches with independently observed operational samples or a downstream reconciliation peer.

Publish each component: partition coverage, heartbeat coverage, observed versus predicted volume with interval, key/cardinality anomaly, control-total difference, freshness and reconciliation sample. Label the composite `estimated completeness`, include model/version/uncertainty and retain raw evidence. Blind spots include correlated producer and manifest failure, real behavior shifts, missing and duplicate cancellation, new entities, biased samples, seasonality misspecification and semantic corruption within conserved totals.

Block when a required partition/heartbeat is absent without certified empty state, control totals violate hard domain invariants, uncertainty is too broad for the decision, observed state lies outside reviewed bounds, a high-risk source has no independent evidence, or downstream reconciliation finds actual gaps. Lower-risk provisional publication may be allowed with explicit status, consumer agreement, correction path and bounded duration; it must not be counted final-good.

### Answer 5

Inventory each check’s product/view, consumer/decision, owner, source boundary, consumer endpoint, unit/weight, denominator, threshold/window, telemetry and alert dependencies. Freeze new checks using modification time. Prioritize financial/security/safety/regulatory products, cross-tenant masking, externally consumed exports/features, unknown telemetry, singular deadlines and products with known incidents but green dashboards.

Replace modification time with source availability/event boundary plus immutable product-generation coverage and consumer-path probe. Add independent manifests/ledgers/partition inventories/control totals and reconciliation. Define empty/idle/unknown/excluded states. Compute ratios from summed good/total weights; publish both event-volume and tenant/window objectives where needed, plus worst slices and absolute critical gates. Add per-unit evidence and observer heartbeats; missing telemetry is bad/alertable.

Version new indicators and dual-run against old to explain deltas. Preserve historical bad events and record repair/correction time rather than resetting after backfill. Replace threshold pages with fast/slow burn alerts, low-volume absolute rules and symptom ownership; stage alerts aid diagnosis. Assign product owners, consumer-reviewed harm/fallback, runbooks, escalation and error-budget policy.

Completion evidence includes every active product mapped to a named consumer/owner and versioned SLO contract; consumer-visible start/end boundaries; defensible denominator or explicitly estimated uncertainty; raw-evidence recomputation passing; fixtures for late/missing/duplicate/idle/unknown/cache-stale cases; observer health coverage; correct weighted aggregation and slices; alert fault tests with measured detection/reset; backfill history preservation; no orphan paging routes; and time-bounded reviewed exceptions. A cleaner dashboard alone is not completion.
