---
module_id: DE-078
program: Data Engineering
level: 2
module_number: 78
title: Data Incident Detection and Triage
status: complete
last_verified: 2026-09-03
---

# Data Incident Detection and Triage

## One-Page Review

### Governing question

How can a team detect and declare a data incident early, determine its consumer impact and urgency under incomplete evidence, contain propagation without destroying forensic state, and coordinate an efficient handoff to diagnosis and recovery without letting row counts, alert volume, or organizational boundaries distort priority?

### Essential definitions

- A **signal** is raw evidence such as a failed rule, anomaly, late frontier, consumer report, lineage event, or monitor failure.
- An **observation** binds a signal to a product/version, cohort, interval, rule, evaluator, and collection status.
- A **suspected data incident** is an observation that may threaten a data product or decision and warrants time-bounded validation.
- A **declared data incident** activates named command, communication, evidence, containment, and escalation procedures.
- **Detection** discovers a potentially harmful condition; **triage** rapidly establishes impact, scope, urgency, confidence, propagation, and next action.
- **Impact** is realized or credible harm to consumers, decisions, money, safety, compliance, security, privacy, or trust.
- **Scope** identifies affected products, versions, fields, rows/entities, cohorts, intervals, regions, and consumers; unknown scope is recorded explicitly.
- **Severity** is an operational priority derived from the highest material impact and urgency dimensions, not merely defect volume.
- **Confidence** expresses evidence strength that the suspected condition exists and has the stated scope/cause; low confidence is not low impact.
- **Propagation** is the movement of faulty, stale, missing, or unauthorized data through downstream products, caches, models, reports, exports, and decisions.
- **Containment** limits new harm while preserving evidence: hold publication, quarantine, revoke, fence, pause, fail closed, or serve labeled last-known-good.
- An **incident commander** maintains overall state, priorities, roles, decisions, and handoffs; command is distinct from causal blame.
- A **live incident record** is the authoritative timeline of facts, hypotheses, decisions, actions, owners, timestamps, and open questions.
- **Time to detect/declare/contain/recover** are distinct intervals whose start/end semantics and clock sources must be defined.
- A **false positive** is a completed evaluation showing the signal did not represent the asserted incident; **unknown** means evidence remains insufficient.

### Central model, mechanism, or theorem

For suspected incident $i$, define a triage vector

$$
T(i)=(Impact,Scope,Urgency,Propagation,Reversibility,Regulatory,Confidence,Coverage).
$$

Severity should be a monotone policy over material risk dimensions: increasing credible safety, financial, regulatory, privacy, or irreversible impact must not reduce priority. Confidence and coverage govern evidence handling and escalation; they do not safely average away high potential impact.

Affected-row count alone cannot order incidents. One incorrect settlement total consumed for an irreversible high-value transfer can be critical, while 10,000 malformed rows in an isolated reversible development dashboard can be moderate. Triage preserves the multidimensional vector and applies explicit policy rather than a single anomaly scalar.

### Critical invariants

- Every observation pins product/contract/data/evaluator versions, cohort/interval, collection time, source, raw evidence, and monitoring coverage.
- Signal, observation, suspected incident, declared incident, expected change, pending, false positive, monitor defect, and unknown remain distinct states.
- Declaration criteria favor early coordination when harm may be material; closing a benign incident does not erase the original evidence.
- Severity uses consumer impact, criticality, time sensitivity, propagation, reversibility, and regulatory/security/privacy exposure—not failed-row count alone.
- Confidence and scope uncertainty are reported separately from impact; unknown critical scope can increase urgency.
- One incident commander and live record are authoritative; operational, communication, planning, and subject-matter roles are explicitly delegated.
- Triage begins from consumer-visible symptoms while retaining internal signals for localization.
- Data, manifests, offsets, checkpoints, contract results, lineage, queries, logs, alerts, releases, and consumer examples are preserved before mutation.
- Containment acts at the narrowest reliable boundary but fails closed where critical harm cannot be bounded.
- Last-known-good use is pinned, labeled with `as_of` and caveats, and permitted by the consumer's degradation policy.
- Notifications state known facts, unknowns, affected versions/cohorts, consumer action, owner, and next update time; hypotheses are labeled.
- Parallel responders coordinate writes and experiments; no one “fixes forward” on live evidence without command visibility and rollback.
- Security/privacy indicators route to the applicable restricted response process without oversharing sensitive incident data.
- Recovery is not declared from producer health alone; critical consumers and downstream versions must be verified.
- Incident metrics support learning and capacity, not blame, concealment, or incentives to delay declaration.

### Common failures

Common failures include paging on every rule warning; treating no alert as healthy; declaring severity from row count; waiting for root cause before declaring; assuming low confidence means low risk; collapsing monitor failure into pass; querying moving tables without pinning versions; repairing before capturing evidence; allowing many responders to mutate production; creating separate incident channels with conflicting state; using a stale target as last-known-good without consumer approval; notifying “data issue” without exact products/versions; listing hypotheses as facts; closing when a pipeline turns green; overlooking exports and caches; leaking sensitive sample rows into chat; and judging teams by incident count so they suppress detection.

### Compact example

Incident A affects one row: a wrong settlement aggregate already supplied to an irreversible regulated payment process. Incident B affects 10,000 rows in an isolated development dashboard that can be regenerated. Sorting by row count puts B first. A risk vector puts A at critical due to consumer criticality, irreversibility, propagation, and regulation; B is moderate. The one-row incident declares immediately, freezes the transfer or invokes financial containment, preserves the exact version, and pages the appropriate owners.

### Connections

[DE-049](049-run-metadata-and-operational-state.md) identifies runs, [DE-060](060-handling-late-duplicate-and-out-of-order-events.md) distinguishes expected disorder, [DE-066](066-time-travel-and-reproducible-reads.md) preserves versions, [DE-071](071-completeness-validity-accuracy-and-consistency.md) through [DE-075](075-volume-and-distribution-monitoring.md) generate detection evidence, [DE-076](076-data-contracts.md) defines breach conditions, and [DE-077](077-producer-and-consumer-responsibilities.md) assigns response roles. DE-079 uses lineage for deeper root-cause analysis.

## Governing Question

An alert is not an incident, and an incident need not begin with an alert. A quality test can fail because its evaluator crashed. A distribution shift can be an expected launch. A consumer can discover a wrong decision while every producer dashboard is green. Detection converts heterogeneous evidence into observations; triage decides whether and how to mobilize.

The first minutes are information-poor and consequence-rich. Responders may know that one cohort is wrong without knowing whether the cause is source, transformation, platform, contract, monitor, or consumer. Waiting for certainty increases propagation. Acting destructively on a weak hypothesis can erase evidence or worsen the defect.

Data incidents differ from simple service outages because old, wrong, or unauthorized data persists after compute recovers. It may be cached, exported, embedded in features, used in decisions, or certified in reports. Recovery therefore spans versions and consumers, not only processes.

The governing requirement is a disciplined state machine and live incident record that supports early declaration, multidimensional severity, conservative evidence handling, bounded containment, targeted communication, and a clean handoff to root-cause and recovery work.

## Why This Matters

Fast detection limits decisions made on bad data. Contract, quality, freshness, reconciliation, volume, distribution, lineage, and consumer-outcome signals each see different failures. Combining them improves coverage but also creates duplicate pages and correlated symptoms that require grouping.

Poor triage wastes the detection advantage. Teams investigate the loudest metric instead of highest harm, debate ownership, or rerun pipelines before pinning the failed state. By the time scope is understood, consumers may have copied or acted on the data.

Severity errors cut both ways. A million invalid debug rows may be harmless; one incorrect entitlement or payment may be catastrophic. A low-frequency privacy leak can be urgent. A broad stale dashboard may be tolerable if clearly labeled. Business context is part of technical triage.

Early communication lets consumers contain locally. A producer may not be able to recall an export, stop a model decision, or invalidate a cache. Consumers need precise version/cohort/status information and a next update, even when root cause is unknown.

Incident records are sensitive. They may include personal data, vulnerabilities, customer names, financial exposure, and staff actions. Use restricted channels and protected evidence while keeping operational facts accessible to authorized responders.

## Prerequisites and Retrieval

Retrieve signal: alert/report ID, source, observed/expected values, threshold, first/last occurrence, product/contract/data/evaluator versions, cohort/interval, query, sample reference, and collection coverage.

Retrieve product: purpose, owner/on-call, contract, critical consumers, SLOs, classification, freshness/finality, last-known-good, publication/rollback, retention, and dependencies.

Retrieve consumer impact: profiles, versions read, decision/use, criticality, money/entities affected, reversibility, deadline, regulatory/security/privacy exposure, downstream products, caches, exports, and contacts.

Retrieve execution: source cut, manifests, partitions, offsets/checkpoints, job/task attempts, code/config/reference versions, releases, feature flags, infrastructure, logs/traces/metrics, and recent changes.

Retrieve data evidence: schema, quality results, reconciliation, freshness, volume/distribution, quarantines, row/key difference references, historical baseline, and comparable unaffected cohorts.

Retrieve response capability: incident criteria, severity policy, incident commander/on-call, operational/communication/planning roles, command channel, evidence store, safe containment, last-known-good policy, rollback/replay, and out-of-band access.

Retrieve governance: notification deadlines, breach processes, legal holds, evidence access, disclosure authority, retention, third parties, and regulated reporting.

Retrieve monitoring health: evaluator last success, intended/scanned coverage, telemetry delay, missing-series behavior, alert grouping/inhibition, clock/skew, and monitor dependencies.

Distinguish symptom from cause; breach from monitor failure; pending from late; anomaly from harm; row count from materiality; scope from confidence; unknown from false positive; containment from correction; process recovery from data recovery; last attempted from last-known-good; and incident command from causal ownership.

Create a triage record:

| Concern | Required evidence and decision |
|---|---|
| Identity | Incident/signal/product/contract/data/evaluator versions and timestamps |
| State | Suspected/declared/pending/expected/unknown/contained/recovering/resolved |
| Impact | Consumers, decisions, money/safety/compliance/privacy, reversibility |
| Scope | Products, versions, cohorts, intervals, rows/entities and unknown bounds |
| Propagation | Downstream lineage, caches, exports, models, reports and decisions |
| Command | IC, ops, communication, planning, SMEs, channel and handoff |
| Evidence | Pinned data, results, manifests, offsets, changes, samples and coverage |
| Containment | Hold/quarantine/revoke/fence/rollback/last-good and side effects |
| Communication | Facts, hypotheses, unknowns, consumer action and next update |
| Exit | Root-cause handoff, recovery criteria, validation and follow-up owners |

Write a falsifiable claim: “Incident DI-42 was declared at 10:08 UTC from reconciliation signal S9 for product P/V81/C12; one regulated settlement cohort is confirmed wrong, five downstream products and two exports are potentially affected, propagation after V81 is fenced, V80 is the pinned permitted last-known-good, evidence E1–E14 is immutable with 100% source scan coverage, IC/Ops/Comms/Planning roles are assigned, critical consumers received version-specific actions by 10:15, and recovery requires corrected V82 plus acknowledgment and replay validation from both settlement consumers.”

## Learning Objectives

After completing this module, you should be able to:

1. distinguish signals, observations, suspected incidents, declarations, expected changes, false positives, and unknowns;
2. combine contract, quality, freshness, reconciliation, volume, lineage, and consumer signals without duplicate paging;
3. triage impact, scope, urgency, propagation, reversibility, regulatory exposure, confidence, and coverage;
4. assign severity from consumer harm rather than anomaly or row volume alone;
5. establish incident command, delegated roles, live records, and reliable handoffs;
6. preserve reproducible evidence and protect sensitive incident material before mutation;
7. choose bounded containment and last-known-good behavior by product/consumer policy;
8. communicate precise facts, hypotheses, unknowns, actions, and update times;
9. define end-to-end recovery criteria spanning producer and critical consumers; and
10. measure detection/triage performance without incentives that suppress declaration or learning.

## Core Exposition

### Build a layered detection surface

Use black-box consumer outcomes and white-box pipeline evidence. Black-box signals include wrong reports, unavailable versions, stale `as_of`, decision anomalies, and consumer boundary failures. White-box signals include contract checks, schema/constraint results, completeness/reconciliation, freshness, volume/distribution, offsets, job state, and infrastructure saturation.

Every signal becomes a versioned observation. Store what was intended to run and what actually ran. A missing metric or failed quality query is monitor failure/unknown, not healthy zero. Keep signal timestamps distinct from data event, publication, detection, and declaration times.

Group correlated signals by product/version, lineage, cohort, interval, change, and likely common dependency. One missing upstream partition may trigger 100 downstream freshness alerts. Page the actionable shared symptom while retaining child evidence.

Set declaration conditions before incidents: credible material consumer harm; customer-visible wrong/unavailable data; security/privacy/regulatory concern; cross-team coordination; uncontrolled propagation; or unresolved high-risk suspicion beyond a short limit. Declare early and downgrade/close transparently if benign.

### Validate the signal without destroying it

First verify monitor identity, evaluator health, coverage, current contract, and time alignment. Compare raw observation with an independent narrow query or consumer example. Do not rerun a mutating pipeline or overwrite the target just to see whether the alert disappears.

Pin source/target versions, files/manifests, offsets/checkpoints, transformations/config/reference data, quality results, lineage, query plans, deployment events, and protected difference samples. Snapshot live state where lawful and feasible. Record hashes/locations and access rather than pasting sensitive rows.

Ask falsifying questions: could lateness still be within policy? Did schema/profile change? Is the cohort expected? Did the monitor scan everything? Is the baseline comparable? Can another independent signal reproduce it? A result can be confirmed, expected, pending, false positive, monitor defect, or unknown.

If evidence is incomplete and potential impact is high, preserve the high-priority state. Confidence is not a discount that permits irreversible harm.

### Triage impact and scope

Start from consumers and decisions. Identify who read the affected version, what they did, whether the result propagated, and whether it can be reversed. Assess money, safety, entitlements, compliance, privacy/security, external reporting, customer experience, and time deadlines.

Bound scope in dimensions: earliest/latest affected source event and publication; products/versions; tenants/regions/sources; fields/rules; identities/counts; consumers; derived products; caches; models; reports; exports; decisions. State lower/upper bounds and unknown areas.

Use lineage as a hypothesis graph, then confirm runtime/version use. Declared lineage may be stale; column lineage may miss dynamic logic; exports leave the graph. Combine registry, access, query/subscription, artifact inventories, and owner contact.

Assess whether the incident is still producing or propagating bad data, whether consumers are continuing decisions, and how quickly evidence or rollback windows expire. Urgency can be high even before realized impact is known.

### Assign severity and declare command

Define a severity matrix using the maximum credible dimension or policy rules, not an average. A critical safety/privacy/regulatory/irreversible financial condition should not be reduced by small row count or low aggregate percentage.

Record severity, rationale, confidence, scope coverage, and next reassessment time. Severity changes as evidence improves; retain history. Separate operational severity from public/regulatory classifications whose criteria and authority may differ.

Assign an incident commander. Delegate operations, communication, planning/scribe, and domain/consumer/security/privacy subject-matter roles. IC maintains priorities and the live record; Ops controls production mutations; Comms publishes updates; Planning tracks resources, hypotheses, follow-ups, and handoff.

Use a recognized command channel and an out-of-band fallback. Keep the top of the live record current: status, impact, versions, containment, commander, next actions/owners, unknowns, and next update. Explicitly transfer command across shifts.

### Contain propagation safely

Contain the narrowest proven scope: stop a producer version, hold publication, quarantine one cohort, revoke a view, fence a writer, pause a consumer decision, invalidate a cache, disable a model feature, or block an export. If scope cannot be bounded and harm is critical, fail closed more broadly under policy.

Rollback only to a pinned validated version compatible with current consumers and source semantics. Label last-known-good with version, `as_of`, known caveats, and expected next update. Availability does not make stale data safe for every purpose.

Avoid uncontrolled live repair. Multiple responders issuing updates, deletes, reruns, and backfills can create a second incident and destroy causal evidence. Route production writes through Ops with change IDs, dry runs, limits, observation, and rollback.

Security/privacy indications require restricted handling, least disclosure, legal/security authority, and preservation obligations. Do not delay protective containment while debating whether the event is “a data quality issue” or “a security issue.”

### Communicate for consumer action

Initial notice names the product and exact affected/safe versions, first known time, confirmed impact, possible scope, current containment, consumer action, contact/channel, and next update. Distinguish facts, hypotheses, and unknowns.

Use targeted machine-readable status plus human updates. Critical consumers need acknowledgment, not merely delivery. Public wording follows authorized communication policy; internal precision must still enable safe local decisions.

Update on schedule even when there is no new root-cause finding. Report changed scope/severity, actions/results, new risks, and next decisions. Avoid speculative blame, raw sensitive samples, and optimistic recovery estimates without evidence.

Notify when a safe version exists, but state whether consumers must invalidate, replay, rebuild, reissue, or inspect decisions. “Pipeline recovered” is not an actionable correction notice.

### Hand off to diagnosis and recovery

Triage produces a bounded problem statement, evidence inventory, timeline, impact graph, hypotheses, containment state, and prioritized owners. Root-cause analysis can then proceed without rediscovering versions or mutating evidence.

Recovery criteria are predeclared: corrected producer version passes contract/quality/reconciliation/freshness; checkpoints and publication are sound; unaffected controls pass; critical consumers ingest and validate; caches/models/reports/exports are corrected; decisions are remediated; backlog stabilizes; and status communicates.

Resolve only when the incident's required outcomes pass. Continue follow-up for root cause, contributing factors, escaped controls, monitor gaps, and durable actions. An incident may be contained long before it is recovered, and recovered before all long-term remediation completes.

Preserve original failed observations, corrections, notices, decisions, and acknowledgments. The historical record should answer what consumers could know at each time.

### Measure and rehearse the process

Define time origins carefully: defect introduced, bad version published, first consumer exposure, first detectable signal, detection, acknowledgment, declaration, containment, corrected publication, critical-consumer recovery, and closure. Report censored/unknown origins rather than inventing precision.

Measure signal coverage and precision, consumer-before-monitor detection, alert grouping, time to acknowledge/declare/contain, scope convergence, update cadence, handoff quality, correction adoption, recurrence, and overdue actions. Break down by criticality without ranking individuals.

Avoid targets that discourage early declaration or encourage premature closure. More incidents may indicate improved detection. Short recovery can reflect low severity. Use metrics to find control and staffing gaps.

Run tabletop and technical exercises with missing telemetry, partial lineage, stale owners, unavailable primary tools, sensitive evidence, and cross-timezone handoff. Practice command roles, not only technical rollback.

## Definitions and Notation

Let:

- $s$ be a raw signal and $o=(s,P,C,D,E,c,t)$ its versioned observation;
- $i$ be an incident candidate or declared incident;
- $H(i)$ be confirmed and credible potential consumer harms;
- $S(i)$ be scope dimensions and bounds;
- $G_i=(V,E_d)$ be the downstream dependency/propagation graph;
- $q(i)$ be confidence in the asserted condition/scope;
- $k(i)$ be evidence/monitoring coverage;
- $t_p,t_d,t_a,t_c,t_r$ be bad publication, detection, acknowledgment/declaration, containment, and recovery times; and
- $T(i)$ be the full triage vector.

Example operational intervals are

$$
TTD=t_d-t_p,\qquad TDeclare=t_a-t_d,\qquad TTC=t_c-t_a,\qquad TTR=t_r-t_a.
$$

These are meaningful only when endpoints and clocks are named; if bad-publication time is bounded rather than known, TTD is an interval. Severity policy $\sigma(T)$ should be monotone in material risk dimensions:

$$
T_1\preceq_{risk}T_2\implies \sigma(T_1)\le\sigma(T_2).
$$

No assumption is made that row count orders risk, that confidence equals probability of harm, or that declared lineage proves runtime propagation.

## Mechanisms, Invariants, or Proof Structure

Proof sketch that affected-row count does not determine incident severity:

1. Incident A affects one settlement aggregate used for an irreversible regulated transfer.
2. Incident B affects 10,000 presentation rows in an isolated reversible development dashboard.
3. Row-count ordering ranks B above A because $10{,}000>1$.
4. A has critical decision, irreversibility, propagation, and regulatory dimensions.
5. B has moderate internal impact, no production propagation, and straightforward regeneration.
6. Under a monotone maximum-material-risk policy, A is critical and B is moderate.
7. Therefore affected-row count alone does not determine or safely order incident severity.

The counterexample does not make row count irrelevant. It is essential scope evidence when combined with grain, value, consumers, and use.

The executable reproduces the reversed rankings under row-count and risk-vector policies. It is a teaching abstraction, not a financial decision system, legal classifier, incident platform, probability model, or universal severity matrix.

<!-- bijux-verify: {"id":"risk-aware-triage","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"incident_a_affected_rows=1\nincident_b_affected_rows=10000\nrow_count_orders_a_first=False\nincident_a_severity=critical\nincident_b_severity=moderate\nseverity_orders_a_first=True\n","stderr":""}} -->
```python
incident_a = {
    "affected_rows": 1,
    "consumer_criticality": 4,
    "irreversibility": 4,
    "propagation": 4,
    "regulatory": 4,
}
incident_b = {
    "affected_rows": 10_000,
    "consumer_criticality": 2,
    "irreversibility": 1,
    "propagation": 1,
    "regulatory": 1,
}

def severity(incident):
    risk = max(value for key, value in incident.items() if key != "affected_rows")
    return {4: "critical", 3: "high", 2: "moderate", 1: "low"}[risk]

print(f"incident_a_affected_rows={incident_a['affected_rows']}")
print(f"incident_b_affected_rows={incident_b['affected_rows']}")
print(f"row_count_orders_a_first={incident_a['affected_rows'] > incident_b['affected_rows']}")
print(f"incident_a_severity={severity(incident_a)}")
print(f"incident_b_severity={severity(incident_b)}")
priority = {"critical": 4, "high": 3, "moderate": 2, "low": 1}
print(f"severity_orders_a_first={priority[severity(incident_a)] > priority[severity(incident_b)]}")
```

## Alternatives and Trade-Offs

1. **Early declaration versus extended validation:** early command limits propagation; unnecessary incidents cost attention but can close transparently.
2. **Symptom-based versus cause-based paging:** symptoms reflect harm and are actionable; cause signals localize earlier but can be noisy.
3. **Maximum-risk versus weighted severity:** maximum protects catastrophic dimensions; weighting expresses trade-offs but can average them away.
4. **Central command versus team-local response:** central command coordinates broad impact; local response is faster for bounded incidents.
5. **Narrow quarantine versus broad fail-closed:** narrow action preserves availability; broad containment protects when scope is unknown and harm is high.
6. **Rollback versus forward correction:** rollback restores known behavior quickly; schema/state changes may make it incompatible, while forward fixes require stronger validation.
7. **Last-known-good versus unavailable:** stale service helps tolerant consumers; absence is safer for decisions with strict recency or correctness.
8. **Live query versus pinned snapshot:** live queries answer current state; pinned evidence preserves the historical failure and reproducibility.
9. **Automated grouping versus human correlation:** automation reduces alert storms; incorrect grouping can hide independent incidents.
10. **Broad transparency versus restricted response:** broad visibility improves coordination; security/privacy/legal details require compartmentalization.
11. **Fixed update cadence versus event-driven updates:** cadence maintains trust during uncertainty; event-driven reduces noise but creates silence.
12. **Fast process metrics versus outcome metrics:** times expose response friction; end-to-end consumer recovery better represents harm but is harder to observe.

## Failure Modes and Misconceptions

- **“Every alert is an incident.”** Signals require stateful validation and policy-based declaration.
- **“No alert means healthy data.”** Monitor failure, missing coverage, and consumer-only defects exist.
- **“Wait for root cause before declaring.”** Coordination and containment often must begin under uncertainty.
- **“Low confidence means low severity.”** Potential irreversible harm with weak evidence can demand urgent validation/containment.
- **“High anomaly score means critical.”** Statistical magnitude is not consumer harm.
- **“More affected rows means higher severity.”** Grain, value, use, reversibility, and regulation dominate in some incidents.
- **“Average impact is enough.”** One critical cohort can be hidden by a large benign population.
- **“Severity never changes.”** Scope and impact evidence evolve; retain reassessment history.
- **“The first symptom identifies cause.”** Downstream failure may have many upstream or local explanations.
- **“Lineage proves impact.”** Declared graphs need runtime/version and off-platform confirmation.
- **“Query logs list every consumer.”** Exports, caches, shared identities, dormant jobs, and decisions remain.
- **“Pipeline green means recovered.”** Wrong data and downstream effects persist after compute succeeds.
- **“Rerun first, investigate later.”** Mutation can erase evidence, duplicate effects, and spread a defect.
- **“Live table state is good enough evidence.”** It changes while responders compare it.
- **“Everyone can help by editing production.”** Parallel writes destroy coordination and rollback.
- **“Rollback is always safe.”** Consumer/schema/source state may have moved beyond the old version.
- **“Last-known-good is safe for all.”** Staleness and compatibility are consumer-purpose constraints.
- **“Quarantine the whole platform.”** Narrow containment preserves unaffected service when scope is reliable.
- **“Narrow containment is always best.”** Unknown critical scope can require broad fail-closed action.
- **“Silence until certainty avoids panic.”** Consumers continue harmful use without actionable notice.
- **“Send all raw rows for transparency.”** Incident evidence may expose regulated or sensitive data.
- **“Notification is a generic outage message.”** Data consumers need exact versions, cohorts, actions, and correction semantics.
- **“Hypotheses belong in the facts section.”** Label uncertainty to prevent speculative action.
- **“No news means skip the update.”** Scheduled updates maintain shared state and trust.
- **“The technical lead must command.”** IC manages priorities/coordination and may delegate diagnosis.
- **“Incident command assigns blame.”** It assigns response authority; causal learning comes later from evidence.
- **“Producer fix closes every consumer.”** Caches, models, reports, exports, and decisions need verification.
- **“False positives should be deleted.”** They inform monitor quality and declaration policy.
- **“Fewer incidents prove reliability.”** Suppressed detection or delayed declaration can lower counts.
- **“Fast closure proves good response.”** Premature closure and low-impact incidents distort time metrics.

## Worked Examples

### Example 1

A completeness test fails because its warehouse query times out at 40% scan coverage. The observation is monitor failure/unknown, not proof of missing rows or a pass. Because the product is a critical settlement input, the incident is declared for urgent evidence restoration and publication holds.

### Example 2

Global row count drops 0.01%, but all missing rows belong to one sanctions-screening cohort. Cohort impact makes severity critical despite tiny aggregate change.

### Example 3

A launch doubles transaction volume and changes category mass. Deployment/calendar evidence and source controls confirm expected change. Triage closes the suspected incident, records the baseline decision, and retains the original signal.

### Example 4

One missing upstream file triggers freshness, row-count, reconciliation, and 70 downstream alerts. Grouping identifies a shared product/version while child observations preserve each affected consumer and objective.

### Example 5

A producer cannot bound which versions contain incorrect exchange rates. It fences new publication, while critical consumers fail closed and tolerant dashboards serve labeled V40. Broad containment remains until version scope is proven.

### Example 6

An analyst notices a report discrepancy before monitors. Their query and report version become first-class evidence. The incident review treats consumer detection as a coverage signal rather than an embarrassment to suppress.

### Example 7

A privacy monitor finds one unauthorized plaintext identifier in an export. Row count is one, but disclosure and onward-copy risk invoke restricted high-severity response, revoke access, preserve evidence under legal policy, and limit broad chat details.

### Example 8

At shift change, the outgoing IC verbally summarizes but retains command until the incoming IC acknowledges and the live record names them. Ops actions continue under one authority.

### Example 9

Producer V52 passes after correction, but a feature store still serves V51-derived values. Recovery remains incomplete until serving cache invalidation, model feature validation, and critical consumer acknowledgment pass.

### Example 10

A quarterly exercise removes the primary dashboard and makes lineage stale. Responders use out-of-band communication, manifests, contract registry, access inventory, and consumer attestations, exposing gaps before a real incident.

## Cross-Program Connections

- **Reliability Engineering:** actionable alerts, incident command, severity, containment, recovery, handoffs, postmortems, and exercises provide the operating discipline.
- **Security Engineering:** evidence preservation, restricted response, incident classification, least disclosure, chain of custody, and notification authority overlap strongly.
- **Platform Engineering:** monitors, catalogs, lineage, status propagation, evidence stores, feature flags, rollback, and command tooling enable response.
- **Distributed Systems:** partial failure, stale views, clocks, retries, propagation, independent signals, and eventual consistency create uncertainty.
- **Systems Engineering:** hazard severity, consequence, detectability, barriers, fault propagation, configuration control, and mission impact structure triage.
- **Statistics:** anomaly thresholds, false positives/negatives, confidence, multiple signals, baselines, and censoring bound detection evidence.
- **Software Engineering:** debugging, version control, release correlation, feature flags, immutable artifacts, rollback, and test coverage aid isolation.
- **API and Service Engineering:** status/version metadata, client impact, cached responses, deprecation, incident communication, and correction APIs connect consumers.
- **Privacy Engineering:** breach assessment, minimization, purpose, deletion, restricted evidence, notification, and derivative tracking affect procedure.
- **Organizational Design:** command authority, role separation, escalation, communication, handoff, incentives, and psychological safety determine response quality.

## References

1. Google. [Managing Incidents](https://sre.google/sre-book/managing-incidents/). Accessed 2026-09-03. Primary SRE guidance for incident command, operations, communication, planning, live state records, declaration, handoff, evidence preservation, and rehearsal.
2. Google. [Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/). Accessed 2026-09-03. Primary SRE guidance for actionable symptom/cause monitoring, latency, traffic, errors, saturation, and human notification.
3. Google. [Emergency Response](https://sre.google/sre-book/emergency-response/). Accessed 2026-09-03. Primary SRE incident examples and guidance for preparedness, coordination, out-of-band access, rollback, communication, and alert storms.
4. Google. [Postmortem Culture](https://sre.google/sre-book/postmortem-culture/). Accessed 2026-09-03. Primary guidance for impact/timeline/response/root-cause records, blameless learning, and durable follow-up.
5. NIST. [SP 800-61 Rev. 3: Incident Response Recommendations and Considerations](https://csrc.nist.gov/pubs/sp/800/61/r3/final). Accessed 2026-09-03. Authoritative current recommendations integrating preparation, detection, response, recovery, and improvement with risk management.
6. PagerDuty. [Incident Response Documentation](https://response.pagerduty.com/). Accessed 2026-09-03. Primary practitioner documentation for response roles, severity, command, communication, operations, and process preparation.
7. Prometheus. [Alerting rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/). Accessed 2026-09-03. Primary documentation for expressions, pending duration, keep-firing behavior, labels, annotations, and alert states.
8. OpenTelemetry. [Logs data model](https://opentelemetry.io/docs/specs/otel/logs/data-model/). Accessed 2026-09-03. Primary specification for timestamped event records, observed time, trace context, severity, attributes, and resource identity.
9. OpenLineage. [Object model](https://openlineage.io/docs/spec/object-model/). Accessed 2026-09-03. Primary specification for run, job, dataset, version, event-time, lifecycle, and lineage evidence.
10. OpenLineage. [Run cycle](https://openlineage.io/docs/spec/run-cycle/). Accessed 2026-09-03. Primary documentation for run lifecycle states and event-based operational observations.
11. Great Expectations. [Data quality use cases](https://docs.greatexpectations.io/docs/reference/learn/data_quality_use_cases/dq_use_cases_lp/). Accessed 2026-09-03. Primary documentation for distribution, freshness, integrity, missingness, schema, uniqueness, and volume signals.
12. AWS. [Monitoring AWS DMS tasks](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Monitoring.html). Accessed 2026-09-03. Primary service documentation for source/target CDC latency, throughput, backlog, task state, and table statistics used in triage.
13. Bitol. [Open Data Contract Standard](https://github.com/bitol-io/open-data-contract-standard). Accessed 2026-09-03. Primary contract specification project for product identity, ownership, support, schemas, quality, service levels, and lifecycle context.
14. UK Government Data Quality Hub. [The Government Data Quality Framework](https://www.gov.uk/government/publications/the-government-data-quality-framework/the-government-data-quality-framework). Accessed 2026-09-03. Primary framework for ownership, quality dimensions, lifecycle controls, communication, action planning, and root-cause improvement.

## Exercises

### Exercise 1

Design a detection and declaration policy for a regulated daily product. Include signals, observation identity, monitor coverage, declaration criteria, expected/pending/unknown states, grouping, severity, command, and consumer notification.

### Exercise 2

Triage three simultaneous signals: a million invalid test rows, one wrong payment aggregate, and a failed freshness evaluator on an entitlement feed. Produce impact/scope/urgency/propagation/reversibility/regulatory/confidence/coverage vectors and actions.

### Exercise 3

Create an evidence-preservation and containment plan for a live CDC pipeline with mutable source/target, caches, exports, sensitive rows, concurrent responders, and uncertain affected offsets.

### Exercise 4

Write initial, scheduled, and recovery communications for an incident with partial lineage and evolving scope. Include facts, hypotheses, unknowns, exact versions/cohorts, consumer actions, acknowledgment, and next update.

### Exercise 5

Design incident metrics and an exercise program that improve detection and triage without discouraging early declaration, consumer reporting, or honest scope uncertainty.

## Answers to the Exercises

### Answer 1

Convert every alert/report to an observation with signal/product/contract/data/evaluator versions, cohort/interval, query/evidence, collection clock, and intended/scanned coverage. States include pending lateness, expected change, suspected, declared, false positive, monitor defect, and unknown. Declare for credible material consumer harm, regulated/security/privacy concern, uncontrolled propagation, cross-team coordination, or unresolved high-potential suspicion; do not wait for cause. Group by shared lineage/version while retaining child impacts. Severity uses maximum material dimension and unknown critical scope. Assign IC/Ops/Comms/Planning, create protected live record, hold publication or serve permitted labeled last-good, and notify critical consumers with actions and acknowledgment.

### Answer 2

The million invalid test rows have no production consumers, reversible regeneration, high confidence and complete coverage: moderate or lower by policy, quarantine without broad page. The single payment aggregate has confirmed regulated financial use, irreversible transfer risk, active propagation, high urgency and strong evidence: critical and immediate command/containment. The entitlement freshness evaluator failure proves unknown evidence, not stale data; because denied/granted access may be safety/security critical, assign high potential impact, low condition confidence, zero measurement coverage, urgent independent validation and fail-closed/last-good behavior per policy. Do not average confidence into severity or order by row count.

### Answer 3

Fence new target publication and pause destructive consumer actions at a recoverable boundary. Record source system/snapshot/log slot and current positions, connector/sink checkpoints, target versions, manifests, contract/results, code/config/reference, caches/exports, access, and clocks. Snapshot or retain WAL/change feed before expiry. Store protected key/digest references rather than raw sensitive rows in chat; apply legal/security preservation. Route all writes through Ops with change IDs, dry-run, row/offset bounds, idempotency, observation, and rollback. If offset scope is unknown and harm critical, contain the full suspect interval; once exact gap/cut is proven, narrow. Pin and label any last-good version and notify export owners because recall is not automatic.

### Answer 4

Initial: name incident/product, confirmed affected version/cohort/time, possible scope, containment, safe/unsafe versions, required stop/fallback action, owner/channel, and next update; label cause unknown. Scheduled updates repeat current impact, expand or narrow scope with evidence, separate hypothesis from fact, list completed/in-progress actions and risks, state consumer acknowledgments, and keep the promised cadence even without cause. Recovery notice names corrected version and validations, but also exact consumer duties—cache invalidation, replay, rebuild, report reissue or decision review—plus caveats and support. Resolve after critical acknowledgments/outcome checks, not merely pipeline success.

### Answer 5

Measure defect-publish to first detectable signal where knowable, signal-to-acknowledge/declare, declare-to-contain, scope-bound convergence, corrected publish and critical-consumer recovery; observation and evaluator coverage; duplicate/grouped alerts; consumer-before-monitor detection; update/handoff timeliness; correction adoption; recurrence; and overdue actions. Preserve bounded/unknown time origins. Segment by severity and practice context without ranking individuals. Reward early accurate escalation, consumer reports, evidence quality, and durable action rather than low incident count or fast closure. Exercises rotate roles and include monitor failure, stale lineage, sensitive evidence, unavailable dashboards, dormant exports, clock uncertainty, and cross-timezone handoff; track discovered control gaps to owners and completion.
