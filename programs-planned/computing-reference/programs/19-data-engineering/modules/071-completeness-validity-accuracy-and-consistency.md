---
module_id: DE-071
program: Data Engineering
level: 2
module_number: 71
title: Completeness, Validity, Accuracy, and Consistency
status: complete
last_verified: 2026-09-03
---

# Completeness, Validity, Accuracy, and Consistency

## One-Page Review

### Governing question

How can a team turn completeness, validity, accuracy, and consistency from attractive labels into reproducible measurements and operational decisions when expected populations, applicability, reference truth, semantics, time, uncertainty, and remediation differ across data products?

### Essential definitions

- **Fitness for purpose** means data quality is evaluated against a declared use, risk, population, and tolerance rather than an abstract demand for perfection.
- A **quality dimension** is a characteristic to assess; a **quality metric** is the exact procedure that produces evidence about that characteristic.
- A **quality rule** identifies its dimension, subject, expected behavior, scope, applicability, denominator, severity, owner, effective version, and disposition.
- The **measurement grain** is the unit assessed: value, field, record, entity, relationship, event, batch, partition, dataset, or aggregate.
- The **expected population** is the set of records or entities that should exist for a stated scope and time.
- **Applicability** says whether a field or rule is required for a particular member of the population; not-applicable is not missing.
- **Completeness** is the degree to which expected records and applicable values are present.
- **Validity** is the degree to which present data conforms to declared formats, types, domains, ranges, and business constraints.
- **Accuracy** is the degree to which data represents the real entity, event, or quantity it purports to describe.
- **Consistency** is the degree to which semantically equivalent or logically related observations do not contradict one another.
- A **reference source/procedure** supplies evidence for accuracy, with its own identity, effective time, lineage, uncertainty, and limitations.
- A **violation** is a measured failure of a rule; a **test execution failure** means the measurement itself did not complete and must not be reported as a passing rule.
- A **quality gate** maps evidence to actions such as publish, warn, quarantine, reject, hold, or escalate.
- A **quality incident** is a quality condition whose business impact, duration, or scope crosses an agreed threshold.
- **Provenance** records the dataset/version, rule/version, engine, time, counts, samples or digests, and decisions behind a quality result.

### Central model, mechanism, or theorem

For rule $r$ on observed population $O$ and expected population $E$, define an applicability predicate $A_r(x)$ and pass predicate $P_r(x)$. A dimension rate is

$$
q_r=\frac{\sum_{x\in U_r}\mathbf{1}[P_r(x)]}{|U_r|},
$$

where $U_r$ is the explicitly declared evaluation population. For record coverage, $U_r=E$ and passing means the expected entity is observed. For attribute completeness, $U_r=\{x\in O:A_r(x)\}$ and passing means the applicable value is present. For validity, missing values may be excluded and measured by completeness, or included as invalid, but the rule must say which.

Accuracy requires a reference mapping or measurement procedure $G$:

$$
Acc=\frac{|\{x\in U_G:d(value(x),G(x))\le\epsilon(x)\}|}{|U_G|}.
$$

Consistency compares aligned representations or checks logical constraints. If two sources disagree, inconsistency is proven; accuracy is not, unless independent evidence identifies truth.

### Critical invariants

- Every metric names a purpose, grain, subject, scope/window, population, denominator, exclusions, rule version, threshold, and owner.
- Missing records, missing applicable values, optional values, suppressed values, unknown values, defaults, and not-applicable values remain distinguishable.
- A valid value can be inaccurate; a complete dataset can be wrong; consistent sources can share the same error.
- Accuracy claims cite a reference source or measurement procedure and its time, coverage, uncertainty, and independence.
- Cross-source consistency aligns identity, schema semantics, units, timezone, currency, effective time, and aggregation grain before comparison.
- Numerators and denominators are stored with rates; ratios from different populations are not averaged without correct weighting.
- Failed test execution, partial scanning, late partitions, and unavailable references produce unknown/incomplete evidence, not success.
- Rules are versioned, reviewed, canaried, and evaluated on pinned data versions; historical results remain interpretable.
- Severity and disposition reflect business risk; not every violation blocks publication, and no critical failure is silently downgraded.
- Row samples are minimized and protected; metrics and digests are preferred where sensitive values are unnecessary.
- Remediation preserves raw evidence, avoids undocumented imputation, and fixes collection or transformation causes when possible.
- Quality is measured across cohorts and time; a global passing rate cannot hide a severe regional, tenant, source, or protected-group defect.
- Metric changes, exemptions, overrides, and manual corrections are attributable, time-bounded, and auditable.
- Downstream consumers receive quality status, coverage, caveats, version, and incident information alongside the data.
- Improvement is verified by remeasurement and recurrence monitoring, not by closing a ticket.

### Common failures

Common failures include treating non-null percentage as all completeness; using row count without an expected population; counting not-applicable fields as missing; treating regex or schema success as accuracy; calling two matching systems correct; comparing local dates to UTC timestamps; evaluating totals at different grains; dividing by zero or hiding the denominator; averaging percentages across unequal cohorts; converting test-engine failure to pass; sampling only easy records; tuning thresholds until a release passes; replacing unexpected values with defaults; deleting quarantined evidence; exposing failed rows containing sensitive data; blocking every defect equally; and publishing a single “quality score” that conceals the failed dimension and business impact.

### Compact example

Six customers are expected and five records arrive, so record coverage is $5/6$, independent of null fields. Email is applicable to all five observed customers; four values are present, so email completeness is $4/5$. Of four present emails, three satisfy the declared email rule; of five ages, four lie in the allowed range, giving seven valid results over nine evaluated present values. Four records can be checked against a dated authoritative age reference and three match within tolerance, so measured accuracy is $3/4$ for that covered subset. Four of five invoice totals equal their component sums, so internal consistency is $4/5$. These rates answer different questions and must not be collapsed into “80% quality.”

### Connections

[DE-008](008-schemas-nullability-and-type-fidelity.md) defines representation and null semantics, [DE-023](023-file-arrival-and-manifest-processing.md) identifies expected arrivals, [DE-030](030-designing-replayable-raw-ingestion.md) supplies immutable lineage, [DE-049](049-run-metadata-and-operational-state.md) identifies executions, [DE-060](060-handling-late-duplicate-and-out-of-order-events.md) distinguishes event-time anomalies, and [DE-066](066-time-travel-and-reproducible-reads.md) pins evidence. DE-072 turns these contracts into schema and constraint tests; DE-073 extends them to reconciliation.

## Governing Question

“The dataset is 99% good” is not an operational statement. It omits what was expected, what was checked, whether missing values were applicable, which rule defined good, how reality was observed, when sources were aligned, what the remaining one percent affects, and what action follows.

Quality is relational. A field may be complete for invoicing but insufficient for fraud analysis. A sensor reading can conform to type and range while calibration drift makes it inaccurate. Two warehouses can agree because both copied the same upstream error. A reference registry can be authoritative for identity but too stale for current address accuracy.

The four dimensions diagnose different mechanisms. Completeness asks whether required entities or values are present. Validity asks whether representation and business rules are satisfied. Accuracy asks whether representation corresponds to reality. Consistency asks whether observations that should agree actually agree. Their evidence and remediation differ.

The governing requirement is a versioned measurement contract and decision policy. The team must be able to reproduce every result from pinned data and rule versions, explain its denominator and uncertainty, trace violations to source, communicate fitness and caveats to consumers, and prove whether remediation improved the intended use.

## Why This Matters

Bad quality becomes costly when it crosses a decision boundary. Missing orders understate revenue; valid but incorrect addresses misroute shipments; contradictory customer status breaks eligibility; inaccurate labels bias a model. The same defect can be low risk in exploration and critical in payment, safety, or regulatory reporting.

Naive automation creates false confidence. Schema tests find representation failures but cannot usually compare data with reality. Row counts detect gross loss only when an expected count or source population exists. A green test over 40% of rows is not a green dataset if the excluded 60% were unavailable.

Distributed pipelines complicate denominators. Late events, replay, partition lag, slowly changing dimensions, timezone boundaries, deduplication, filtering, joins, and privacy suppression all change the population. The measurement must state whether it evaluates received, accepted, current, event-time, or expected entities.

Accuracy is expensive because truth is hard to observe. It may require source-system confirmation, physical measurement, human adjudication, or statistically designed sampling. Reference evidence also has error and latency. Honest uncertainty is more valuable than a precise-looking unsupported rate.

Quality controls influence privacy and fairness. Failure samples can expose sensitive values. Imputation can erase meaningful absence. Aggregate rates can hide systematic gaps in a region or group. Governance must control both the data and the evidence produced about it.

## Prerequisites and Retrieval

Retrieve the use contract: decision or product, users, critical entities/fields/relationships, materiality, loss function, regulatory duties, freshness, acceptable uncertainty, and consequences of false pass versus false fail.

Retrieve population semantics: source-of-truth inventory, expected entities/events/files, inclusion/exclusion rules, effective period, event/processing time, late-arrival allowance, duplicates, cancellations, privacy suppression, applicability conditions, and cohort dimensions.

Retrieve representation: schema and field IDs, types, nullability, defaults, sentinel/unknown codes, units, precision, timezone/calendar, encodings, controlled vocabularies, reference/master data, keys, relationships, and aggregation grain.

Retrieve lineage: source versions, extracts, transformations, joins, filters, deduplication, imputations, manual corrections, table snapshot/version, run ID, code/configuration, and publication state.

Retrieve rules: identifier, dimension, description, expression, subject/grain, applicability, denominator, tolerance, severity, owner, effective dates, version, exemptions, sampling plan, and expected action.

Retrieve accuracy evidence: reference source/procedure, independence, collection time, temporal alignment, coverage, match method, false-match risk, measurement error, calibration, adjudication, sample frame, sample size, and confidence interval.

Retrieve consistency pairs: entity resolution, canonical identifiers, field meaning, units, timezone, currency/exchange rate, version, effective interval, aggregation level, conflict precedence, and allowed transitional disagreement.

Retrieve execution evidence: engine/version, query/code digest, input version, scan coverage, start/end, success/error, numerator, denominator, excluded/unknown counts, result, samples/digests, gate decision, and notification.

Retrieve operations: pre-ingest checks, quarantine, publication gates, warnings, incident thresholds, owners, escalation, waivers, consumer notification, correction/backfill, revalidation, and recurrence monitoring.

Distinguish absent record from null attribute; null from empty/default/sentinel; invalid from inaccurate; inconsistent from incorrect; duplicate from legitimate repeated event; late from missing; reference match from truth; estimate from census; test failure from execution failure; issue occurrence from affected business value; and rule conformance from fitness for use.

Create a quality measurement contract:

| Concern | Required decision and evidence |
|---|---|
| Purpose | Consumer decision, criticality, harm, tolerance and owner |
| Subject | Dataset/version, entity/field/relation, grain, cohort and window |
| Population | Expected/observed sets, applicability, inclusions, exclusions and unknowns |
| Rule | Dimension, expression, reference, tolerance, severity, version and effective time |
| Measure | Numerator, denominator, rate/count, uncertainty, coverage and execution status |
| Action | Publish, warn, quarantine, reject, hold, escalate, waive or remediate |
| Evidence | Inputs, engine/code, timestamps, samples/digests, lineage and retention |
| Ownership | Producer, steward, consumer, reference owner and incident escalation |

Write a falsifiable claim: “For pinned snapshot S381 and event date 2026-09-02, manifest M9 defines 18,420 expected account entities; coverage is 18,401/18,420, required tax-country completeness is 18,390/18,401, present-value validity under rule V12 is 18,387/18,390, a stratified independently adjudicated sample estimates accuracy at 99.2% with its stated interval, and cross-ledger consistency is 18,399/18,401 after currency/time alignment; all critical cohorts meet gates G7, execution scanned 100%, 19 absent accounts are quarantined/escalated, and consumers receive the result and caveats.”

## Learning Objectives

After completing this module, you should be able to:

1. separate completeness, validity, accuracy, and consistency conceptually and operationally;
2. define expected populations, applicability, grains, windows, denominators, and unknowns;
3. measure record coverage and attribute completeness without confusing optional or late data;
4. encode versioned syntactic, semantic, domain, and relationship validity rules;
5. design reference-based or sampled accuracy assessments with uncertainty and temporal alignment;
6. compare observations for consistency only after identity, meaning, units, time, and grain align;
7. aggregate quality rates correctly across partitions and cohorts while preserving counts;
8. build gates that distinguish violations, execution failures, partial evidence, and risk severity;
9. diagnose root causes, remediate without hiding evidence, and communicate fitness to consumers; and
10. operate quality metrics, rules, incidents, exemptions, and improvements over time.

## Core Exposition

### Start with purpose and population

Quality begins with a use, not a tool. Identify the decision and the defect cost. A missing secondary phone number may be immaterial for billing but critical for emergency response. Thresholds follow risk and user needs; they should not be selected because current data happens to pass.

Define the expected population independently where possible. A source manifest, sequence range, control total, registry, schedule, or event contract can establish which entities, files, or events should exist. Counting only received rows cannot reveal entities that never arrived.

Separate record coverage from attribute completeness. For expected entities $E$ and observed identities $O$,

$$
C_{record}=\frac{|E\cap O|}{|E|}.
$$

For attribute $a$ applicable to observed members $A_a\subseteq O$,

$$
C_a=\frac{|\{x\in A_a:present(a,x)\}|}{|A_a|}.
$$

State whether duplicates count once, which version is current, how cancellations are handled, and when late arrivals become missing. Report unexpected extra entities separately; they do not compensate for absent expected ones.

Applicability must be executable. A spouse field can be not applicable for an unmarried person, unknown because marital status is missing, or applicable-but-missing. Collapsing those states distorts both quality and meaning. Preserve source null, blank, sentinel, suppressed, imputed, and not-applicable provenance.

### Measure validity without overstating it

Validity rules include parse/type, format, enumeration, numeric/text length, ranges, dates, checksums, cross-field implications, temporal order, referential integrity, and domain constraints. They should be deterministic for a pinned rule and data version.

A format rule is not necessarily a semantic rule. `2026-02-30` matches a date shape but is not a valid calendar date. A syntactically valid postal code can belong to the wrong country. A positive monetary amount can violate a refund contract. Layer rules and identify the dimension and intended protection.

Choose missing-value semantics explicitly. One useful convention evaluates validity only among present applicable values and measures absence separately. Another declares required-null invalid as well. Either can work if numerator/denominator and combined gates are explicit; silently changing conventions cannot.

Reference domains are versioned. Country codes, product identifiers, eligibility rules, and allowed transitions change over time. Validate against the version effective for the event, not automatically today's list. Retain the rule and reference snapshot with the result.

Declarative assertions improve review and portability, but tool success is not evidence unless the intended batch, columns, and rows were scanned. Record evaluation coverage and distinguish zero violations from zero evaluated rows.

### Earn accuracy claims

Accuracy connects recorded data to reality. Internal plausibility is weak evidence. A temperature of 20°C is valid, but a miscalibrated sensor may be reading five degrees high. An email can match a pattern but belong to another person.

Define the target property, reference procedure, match key, time, and tolerance. Exact equality suits stable identifiers; numeric observations may need absolute or relative error; locations may need distance; classifications may need an adjudicated label and confusion matrix.

Reference sources are not magical. Record authority scope, independence, collection method, latency, coverage, known error, and version. If target data produced the reference, agreement can be circular. When two operational systems disagree, the result is consistency evidence until a third procedure adjudicates accuracy.

Full verification may be impossible. Use a probability sample from a defined frame, stratify by important cohorts or risk, and report sample size, weights, nonresponse, estimated error, and confidence interval. A convenience sample of easy-to-contact cases cannot justify population-wide accuracy.

For numeric values $y_i$ and trusted references $g_i$, useful metrics include bias and absolute error:

$$
Bias=\frac{1}{n}\sum_i(y_i-g_i),\qquad MAE=\frac{1}{n}\sum_i|y_i-g_i|.
$$

A within-tolerance rate should publish the tolerance, reference uncertainty, and covered subset. High accuracy on 10% reference coverage says nothing directly about the unmatched 90%.

### Align before measuring consistency

Internal consistency checks relationships within a representation: start precedes end, invoice total equals line totals under rounding policy, status agrees with dates, child birth follows parent birth, and foreign keys resolve.

Cross-system consistency compares representations that should agree. First align entity identity, field definition, unit, currency and exchange-rate basis, timezone, effective time, update latency, and grain. Comparing an account's current balance with a daily ledger snapshot at another cutoff manufactures contradictions.

Define allowed transitions and tolerances. Eventual consistency may permit a documented lag, but the measurement should record the as-of times and age of disagreement. A perpetual “eventual” exemption is not a quality contract.

If A and B agree, both can still be wrong because they copied the same source or transformation. If they disagree, one, both, or their alignment may be wrong. Consistency triages contradictions; accuracy adjudication determines correspondence to reality.

For aligned pairs $(a_i,b_i)$ with tolerance $\epsilon_i$,

$$
Cons=\frac{|\{i:d(a_i,b_i)\le\epsilon_i\}|}{N_{aligned}}.
$$

Report unmatched identities, ambiguous matches, stale pairs, and excluded comparisons separately. Excluding hard cases can inflate the rate.

### Aggregate and interpret evidence correctly

Store successes $s$, failures $f$, unknowns $u$, and not-applicable $z$, not just a percentage. The primary evaluated rate is $s/(s+f)$; evidence coverage may be $(s+f)/(s+f+u)$. A high pass rate with low coverage is weak evidence.

Combine partitions by summing numerators and denominators:

$$
q_{all}=\frac{\sum_j s_j}{\sum_j(s_j+f_j)},

$$

not by taking the unweighted mean of rates unless partition denominators are equal and that estimand is intended. Preserve cohort breakdowns because a global rate can hide concentrated harm.

Avoid universal composite scores. Weights encode values, compensate defects across dimensions, and obscure action. If a score is required for prioritization, publish its component counts, scaling, weights, sensitivity, and non-compensable critical gates. Never let excellent validity cancel catastrophic record loss.

Baselines and anomaly detection complement fixed rules. Distribution shifts, sudden null increases, cardinality changes, or cohort divergence may reveal unknown defects, but seasonality and business change can cause legitimate shifts. An anomaly is a signal for investigation, not automatic proof of bad data.

### Put rules into the lifecycle

Place cheap structural and manifest checks before expensive ingestion. Validate schemas, files, counts, and control totals at entry; quarantine malformed units without losing raw evidence. Run business validity and referential checks after standardization. Run cross-source consistency and accuracy when aligned references become available.

Each result binds data snapshot/version, rule suite/version, reference versions, code/query digest, engine, scan scope, start/end, counts, exclusions, samples or digests, and gate decision. This turns a green badge into reproducible evidence.

Treat three states separately: rule passed, rule violated, measurement failed/unknown. Engine error, permission denial, timeout, missing partition, or malformed rule must fail the evidence gate according to risk; it must never default to pass.

Use severity and disposition. Critical identity loss may reject or hold publication. A small optional-field defect may warn. Suspect rows can quarantine while unaffected data publishes if consumer semantics support partial release. Record exactly what was released and how excluded records can be recovered.

Canary rule changes on historical good/bad fixtures and recent production snapshots. Review false positives/negatives with domain owners. Version thresholds and applicability. A temporary waiver names reason, approver, scope, expiry, compensating control, and repair owner.

### Diagnose, remediate, and communicate

Trace a violation backward through transformations to collection. Missing output may result from absent source events, filter predicates, inner joins, parsing, deduplication, partition lateness, or failed publication. Fix the earliest controlled cause rather than repeatedly patching outputs.

Preserve raw and failed evidence under access and retention policy. Do not silently coerce, default, impute, deduplicate, or discard. Corrections record original value/digest, corrected value/digest, method, actor, reason, time, and affected versions. Imputed values carry an indicator and uncertainty.

Backfills are versioned changes. Pin source/rule versions, define idempotency, assess downstream reprocessing, publish through normal transactional controls, and rerun the same quality contract. Validate both repaired records and unaffected controls.

Communicate quality with the data: measured version/window, dimension, counts/rates, coverage and uncertainty, cohorts, failed critical rules, caveats, known incidents, remediation state, and contact. Consumers need enough information to decide fitness for their own use.

Track quality service objectives such as critical-rule evaluation coverage, time to detect, time to acknowledge, time to contain, time to correct, recurrence, false gate rate, reference freshness, and affected business volume. Row violation count alone does not measure operational quality.

## Definitions and Notation

Let:

- $E$ be expected entities for a declared scope/window;
- $O$ be observed records or resolved entity identities;
- $A_r(x)$ indicate that rule $r$ applies to $x$;
- $present(a,x)$ indicate an applicable attribute has a meaningful observed value;
- $P_r(x)$ indicate that $x$ passes rule $r$;
- $U_r$ be the evaluation population for $r$;
- $s_r$, $f_r$, $u_r$, and $z_r$ be success, failure, unknown, and not-applicable counts;
- $G(x,t)$ be reference evidence for property of $x$ at effective time $t$;
- $d(a,b)$ be a declared difference function and $\epsilon(x)$ its tolerance;
- $N_{aligned}$ be semantically and temporally aligned pairs;
- $q_{r,c,t}$ be a rule result for cohort $c$ and window $t$; and
- $D=(dataset\_version,rule\_version,reference\_version,execution)$ be result provenance.

Record coverage and unexpected extras are

$$
Coverage=\frac{|E\cap O|}{|E|},\qquad Extra=|O\setminus E|.
$$

Attribute completeness is

$$
Completeness_a=\frac{\sum_{x\in O}\mathbf{1}[A_a(x)\land present(a,x)]}{\sum_{x\in O}\mathbf{1}[A_a(x)]}.
$$

When the denominator is zero, the result is not-applicable/undefined under policy, never silently 100%. Validity, accuracy, and consistency rates must state analogous populations and tolerances.

Evaluated quality and evidence coverage can be reported together:

$$
PassRate_r=\frac{s_r}{s_r+f_r},\qquad EvidenceCoverage_r=\frac{s_r+f_r}{s_r+f_r+u_r}.
$$

These are measurement models, not universal definitions for every standard or tool. The contract determines how duplicates, missingness, weighting, sampling, uncertainty, and applicability affect each result.

## Mechanisms, Invariants, or Proof Structure

Proof sketch that cross-source agreement cannot establish accuracy by itself:

1. Let sources $A$ and $B$ contain the same value $v$ for property $p$ of entity $x$.
2. Consistency evaluation observes $A(x,p)=B(x,p)=v$ and therefore no contradiction under equality.
3. Accuracy requires correspondence to reality/reference value $G(x,p)$ within tolerance.
4. Construct a possible state in which both $A$ and $B$ copied the same erroneous upstream value $v$ while $G(x,p)=g\ne v$.
5. The observed agreement in step 2 still holds in that state.
6. The accuracy predicate fails because $d(v,g)>\epsilon$.
7. Therefore agreement is insufficient to prove accuracy without additional trustworthy reference evidence.

Similarly, validity cannot prove accuracy: any in-domain value can be assigned to the wrong entity. Completeness cannot prove either: every required field can be populated with a wrong but valid value.

The executable calculates four rates on distinct populations and exposes defects rather than composing a score. It is a teaching abstraction, not a distributed test engine, entity-resolution system, statistical survey, reference registry, or publication gate.

<!-- bijux-verify: {"id":"quality-dimensions-distinct","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"record_coverage=5/6=0.833\nemail_completeness=4/5=0.800\nvalidity=7/9=0.778\naccuracy=3/4=0.750\nconsistency=4/5=0.800\ndefect_ids=('B', 'C', 'D', 'F')\nvalid_but_inaccurate=C\n","stderr":""}} -->
```python
expected_ids = {"A", "B", "C", "D", "E", "F"}
rows = [
    {"id": "A", "email": "a@example.com", "age": 30, "parts": (10, 20), "total": 30},
    {"id": "B", "email": None, "age": -2, "parts": (5,), "total": 5},
    {"id": "C", "email": "c@example.com", "age": 40, "parts": (4, 5), "total": 9},
    {"id": "D", "email": "bad", "age": 25, "parts": (3, 4), "total": 10},
    {"id": "E", "email": "e@example.com", "age": 50, "parts": (7, 5), "total": 12},
]
reference_age = {"A": 30, "C": 41, "D": 25, "E": 50}

observed_ids = {row["id"] for row in rows}
present_emails = [row for row in rows if row["email"] is not None]
valid_email = lambda value: value.count("@") == 1 and "." in value.split("@", 1)[1]
valid_email_count = sum(valid_email(row["email"]) for row in present_emails)
valid_age_count = sum(0 <= row["age"] <= 120 for row in rows)
accuracy_count = sum(row["age"] == reference_age[row["id"]] for row in rows if row["id"] in reference_age)
consistent_count = sum(row["total"] == sum(row["parts"]) for row in rows)

print(f"record_coverage={len(observed_ids & expected_ids)}/{len(expected_ids)}={len(observed_ids & expected_ids) / len(expected_ids):.3f}")
print(f"email_completeness={len(present_emails)}/{len(rows)}={len(present_emails) / len(rows):.3f}")
valid_denominator = len(present_emails) + len(rows)
valid_numerator = valid_email_count + valid_age_count
print(f"validity={valid_numerator}/{valid_denominator}={valid_numerator / valid_denominator:.3f}")
print(f"accuracy={accuracy_count}/{len(reference_age)}={accuracy_count / len(reference_age):.3f}")
print(f"consistency={consistent_count}/{len(rows)}={consistent_count / len(rows):.3f}")

defects = (expected_ids - observed_ids) | {
    row["id"]
    for row in rows
    if row["email"] is None
    or not (0 <= row["age"] <= 120)
    or (row["email"] is not None and not valid_email(row["email"]))
    or (row["id"] in reference_age and row["age"] != reference_age[row["id"]])
    or row["total"] != sum(row["parts"])
}
print(f"defect_ids={tuple(sorted(defects))}")
print("valid_but_inaccurate=C")
```

## Alternatives and Trade-Offs

**Reject versus quarantine versus warn.** Rejection protects consumers but can breach freshness and discard usable unaffected data. Quarantine preserves evidence and partial progress but complicates dataset semantics. Warning suits low-risk defects only when consumers receive it.

**Full scan versus sampling.** Full scans can prove conformance for executable rules over the scanned state. Sampling lowers cost and may be necessary for accuracy adjudication but adds sampling/nonresponse uncertainty and can miss rare critical defects.

**Source prevention versus downstream repair.** Source controls prevent recurrence and reduce ambiguity. Downstream repair may be faster under limited authority but must preserve raw evidence, corrections, and root-cause follow-through.

**Strict versus tolerant validity.** Strict rules simplify interoperability and catch drift. Tolerance supports noisy real processes but can normalize bad data; tolerances require domain justification and monitoring.

**Current versus event-time reference.** Current master data is accessible but may misjudge historical events. Effective-dated reference preserves historical meaning at versioning and storage cost.

**Exact versus probabilistic matching.** Exact identifiers minimize false matches but reduce coverage when identifiers are absent or dirty. Probabilistic linkage expands coverage while adding false-link uncertainty that accuracy estimates must include.

**Fixed thresholds versus adaptive baselines.** Fixed thresholds are interpretable and policy-aligned. Adaptive detection finds novel drift but can learn bad regimes and produces signals rather than domain truth.

**One score versus a quality profile.** A score is easy to rank but hides denominators and compensation. A profile preserves dimension, cohort, uncertainty, critical gates, and actionable causes.

**Central rules versus producer ownership.** Central governance improves consistency and guardrails. Producers know semantics and causes; a federated model can centralize contract/evidence standards while keeping accountable domain ownership.

**Detailed failure rows versus minimized evidence.** Rows accelerate diagnosis but leak sensitive values and grow costly artifacts. Counts, hashes, bounded samples, secure references, and access-controlled quarantine reduce exposure.

## Failure Modes and Misconceptions

1. **“Completeness is non-nullness.”** Missing expected entities are invisible to a null scan.
2. **“Every blank is missing.”** Blank, suppressed, unknown, and not-applicable can differ semantically.
3. **“Extra rows offset missing rows.”** They are separate coverage and duplication defects.
4. **“Late means absent forever.”** Completeness is relative to a stated cutoff and grace window.
5. **“A valid value is correct.”** Conformance does not establish reality.
6. **“A plausible value is accurate.”** Plausibility is weak validity evidence.
7. **“Two systems agree, so both are right.”** They may share an upstream error.
8. **“Disagreement identifies the wrong source.”** It establishes inconsistency until adjudication.
9. **“The master is always truth.”** Authority, effective time, coverage, and error still matter.
10. **“Reference matching covers all rows.”** Unmatched and ambiguous cases must be reported.
11. **“One sample proves accuracy.”** Frame, design, weighting, nonresponse, and interval matter.
12. **“Zero failures means 100%.”** Zero evaluated rows or partial scans provide no such proof.
13. **“Tool error is a pass.”** It is unknown evidence and may block by policy.
14. **“All percentages can be averaged.”** Denominators and estimands differ.
15. **“Global quality protects every cohort.”** Concentrated defects can disappear in aggregates.
16. **“More rules always improve quality.”** Redundant/noisy checks create cost and alert fatigue.
17. **“Thresholds describe truth.”** They encode fitness and risk decisions.
18. **“Rules never change.”** Semantics and reference domains are effective-dated.
19. **“A default repairs missing data.”** It may hide absence and introduce inaccuracy.
20. **“Cleaning fixes root cause.”** The upstream collection or transformation may continue failing.
21. **“Quarantine has no consumer effect.”** Partial release changes population semantics.
22. **“Failed-row logs are harmless.”** They may expose personal or confidential values.
23. **“A closed incident means improvement.”** Remeasurement and recurrence evidence are required.
24. **“One quality score is transparent.”** It often masks which dimensions and cohorts failed.
25. **“Quality belongs to the data team.”** Producers, stewards, platforms, and consumers share distinct duties.
26. **“Tests alone create trust.”** Contracts, provenance, communication, remediation, and recovery complete the system.

## Worked Examples

### Example 1

A manifest lists 10,000 expected files and 9,998 arrive before cutoff. File coverage is 99.98%; all received files can have perfect required-field completeness while two files remain wholly absent.

### Example 2

Emergency contact is required only for active minors. The denominator is active minors, not every customer. Records for adults are not-applicable; minors with unknown age remain unknown rather than automatically complete.

### Example 3

A value `blue` passes the eye-color domain but belongs to a person with brown eyes. Validity passes; independently verified accuracy fails. The rule outcomes are not contradictory.

### Example 4

Two ledgers disagree by cents because one rounds line items and the other rounds the final total. The consistency contract selects one documented rounding basis and tolerance before labeling either result defective.

### Example 5

Customer country agrees across CRM and billing because billing copied CRM nightly. An independent address verification finds both wrong. Agreement was consistency evidence, not accuracy evidence.

### Example 6

A validation job lacks permission to read one partition. The result records 80% evidence coverage and execution failure; it does not publish zero violations for the unread partition.

### Example 7

Four tenants have 100/100 valid rows and one has 0/10. The global validity rate is 97.6%, but the tenant cohort gate blocks the affected tenant and raises a concentrated-impact incident.

### Example 8

An accuracy audit samples records by region and risk, oversampling a rare high-risk class. The estimator uses design weights and publishes confidence intervals and nonresponse instead of treating the raw sample percentage as population accuracy.

### Example 9

A temporary waiver allows an outdated product code for one source through Friday with a warning and mapping control. It names an approver, expiry, impacted consumers, and repair owner; expiry automatically restores the gate.

### Example 10

An inner join caused absent orders downstream. The team corrects join semantics, backfills from pinned inputs, retains the failed snapshot, reruns identical rules, compares unaffected controls, and watches recurrence rather than filling missing orders manually.

## Cross-Program Connections

- **Statistics:** sampling frames, weighting, bias, confidence intervals, measurement error, estimands, and nonresponse govern accuracy evidence.
- **Database Systems:** constraints, keys, null logic, transactions, temporal data, isolation, and materialized views underpin rules and pinned results.
- **Software Engineering:** executable contracts, versioning, fixtures, mutation tests, CI gates, code review, and incident correction keep rules reliable.
- **API and Service Engineering:** request validation, schemas, idempotency, reference APIs, status models, error taxonomies, and SLOs shape quality interfaces.
- **Platform Engineering:** self-service rule registries, scalable execution, lineage, policy gates, quarantine, dashboards, and paved roads support many teams.
- **Security Engineering:** least privilege, evidence minimization, access controls, encryption, audit, and tamper resistance protect quality artifacts.
- **Privacy Engineering:** purpose, minimization, suppression, imputation, cohort analysis, correction, retention, and erasure affect both measures and remedies.
- **Machine Learning:** label quality, drift, class imbalance, leakage, feature validity, slice metrics, and ground-truth adjudication reuse these distinctions.
- **Reliability Engineering:** unknown states, coverage, alert quality, incident severity, MTTR, error budgets, and recurrence make quality operational.
- **Formal Methods:** predicates, domains, partial functions, invariants, temporal alignment, counterexamples, and proof obligations clarify what a check proves.

## References

1. UK Government Data Quality Hub. [The Government Data Quality Framework](https://www.gov.uk/government/publications/the-government-data-quality-framework/the-government-data-quality-framework). Accessed 2026-09-03. Primary government framework for fitness for purpose, lifecycle management, and the six core dimensions including completeness, consistency, validity, and accuracy.
2. UK Government Data Quality Hub. [Data Quality Framework guidance](https://www.gov.uk/government/publications/the-government-data-quality-framework/the-government-data-quality-framework-guidance). Accessed 2026-09-03. Primary guidance for quality rules, action plans, root-cause analysis, metadata, communication, and dimension-specific reporting.
3. UK Government Data Quality Hub. [Data quality action plan implementation guide](https://www.gov.uk/government/publications/implement-a-data-quality-action-plan/data-quality-action-plan-implementation-guide). Accessed 2026-09-03. Primary current guidance for purpose alignment, prioritized fields, lifecycle controls, ownership, measurement, and remediation.
4. UK Government Data Quality Hub. [Meet the data quality dimensions](https://www.gov.uk/government/news/meet-the-data-quality-dimensions). Accessed 2026-09-03. Primary explanatory guidance separating accuracy, completeness, consistency, timeliness, uniqueness, and validity with concrete counterexamples.
5. UK Office for National Statistics. [Quality defined](https://www.ons.gov.uk/methodology/methodologytopicsandstatisticalconcepts/qualityinofficialstatistics/qualitydefined). Accessed 2026-09-03. Primary statistical guidance for relevance, accuracy and reliability, timeliness, accessibility, and coherence/comparability dimensions.
6. United Nations Statistics Division. [United Nations National Quality Assurance Frameworks Manual](https://unstats.un.org/unsd/methodology/dataquality/un-nqaf-manual/). Accessed 2026-09-03. Primary international guidance for quality principles, assessment, indicators, risks, metadata, and communication in official statistics.
7. W3C. [Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/). Accessed 2026-09-03. Primary vocabulary for publishing quality dimensions, metrics, measurements, policies, annotations, provenance, and fitness evidence.
8. W3C. [Shapes Constraint Language](https://www.w3.org/TR/shacl/). Accessed 2026-09-03. W3C Recommendation for expressing graph constraints and producing explicit conformance/validation results and failures.
9. Great Expectations. [Create an Expectation](https://docs.greatexpectations.io/docs/core/define_expectations/create_an_expectation/). Accessed 2026-09-03. Primary tool documentation for verifiable assertions, thresholds, severity, metadata, and execution failure behavior.
10. Great Expectations. [Choose validation result format](https://docs.greatexpectations.io/docs/core/trigger_actions_based_on_results/choose_a_result_format/). Accessed 2026-09-03. Primary documentation for element, missing, unexpected, observed-value, and result-detail evidence.
11. Great Expectations. [Validate data integrity](https://docs.greatexpectations.io/docs/reference/learn/data_quality_use_cases/integrity/). Accessed 2026-09-03. Primary documentation for referential, cross-column, cross-table, and business-rule integrity checks.
12. dbt Labs. [Data tests](https://docs.getdbt.com/docs/build/data-tests). Accessed 2026-09-03. Primary documentation for reusable and singular assertions, failure rows, and built-in uniqueness, non-null, accepted-value, and relationship tests.
13. Schelter et al. [Automating large-scale data quality verification](https://www.vldb.org/pvldb/vol11/p1781-schelter.pdf). Accessed 2026-09-03. Peer-reviewed primary system paper for scalable analyzers, constraints, verification, metrics repositories, and incremental quality computation.
14. AWS. [AWS Glue Data Quality](https://docs.aws.amazon.com/glue/latest/dg/data-quality.html). Accessed 2026-09-03. Primary service documentation for rules, managed statistics, anomaly detection, recommendations, monitoring, and pipeline integration.

## Exercises

### Exercise 1

Write a quality measurement contract for daily insurance claims. Define expected population, record and field applicability, late/cancelled claims, four dimensions, reference sources, tolerances, cohorts, numerators/denominators/unknowns, thresholds, severity, actions, and owners.

### Exercise 2

Design an accuracy study for customer postal addresses when only 40% match a national registry and phone verification is expensive. Include estimand, frame, stratification, sample sizes, linkage uncertainty, nonresponse, adjudication, effective time, confidence reporting, privacy, and extrapolation limits.

### Exercise 3

Two financial systems report different daily balances. Specify a consistency workflow that aligns identities, currencies, exchange rates, timezones, cutoffs, pending transactions, rounding, aggregation grain, tolerances, unmatched records, adjudication, and evidence.

### Exercise 4

Design a quality gate that can publish, warn, quarantine, or reject. Cover critical versus advisory rules, partial scans, engine/reference failure, cohort thresholds, historical baselines, rule changes, waivers, sensitive failure evidence, notifications, and retries.

### Exercise 5

A pipeline reports 99.7% quality but a regulated cohort has missing records. Create an incident investigation and durable remediation plan including denominator reconstruction, lineage/root cause, impact, containment, backfill, corrections, consumer communication, revalidation, and recurrence monitoring.

## Answers to the Exercises

### Answer 1

Use a source manifest/sequence register to define expected claims by event date and cutoff; cancellations remain expected with explicit cancelled status, and late claims remain pending until grace expiry. Record coverage compares resolved claim IDs with expected IDs. Required fields use executable applicability by claim type/jurisdiction. Validity versions types, code sets, amount/date ranges, cross-field and relationship constraints. Accuracy checks sampled claimant/provider/amount facts against independent effective-dated procedures with tolerances and uncertainty. Consistency aligns claim/header/line totals and policy/provider systems at the same cutoff. Store success/failure/unknown/not-applicable counts by source, jurisdiction, product, and risk; define critical gates for absent/incorrect payment identity, warnings for low-risk optional fields, quarantine recoverable rows, and assign producer, steward, reference, platform, and incident owners.

### Answer 2

Define the estimand as the proportion of in-scope current customer addresses correctly identifying deliverable reality at a stated date. The frame includes matched, unmatched, ambiguous, and registry-uncovered records. Stratify by region, risk, match status, age, and material cohorts; sample every stratum and oversample rare/high-risk groups, then use design weights. Treat deterministic/probabilistic linkage error separately and manually adjudicate a blinded subset. Phone/postal verification uses a standardized procedure, repeated attempts, nonresponse reasons, temporal window, and dual review for ambiguous outcomes. Publish weighted estimate, confidence interval, reference/verification coverage, false-link study, nonresponse bounds, and cohort results. Minimize contact data and restrict evidence. Do not extrapolate the matched 40% to unmatched records without modeled assumptions and sensitivity analysis.

### Answer 3

Resolve accounts through stable crosswalks and report unmatched/ambiguous IDs. Convert both systems to the same currency using the named rate source/version and business-date rule; normalize units, timezone, cutoff, value/effective time, pending/posted status, reversals, and rounding. Aggregate from transaction grain to the same account/day definition, preserve component totals, and compare exact or justified tolerance. Classify mismatches as timing, missing/extra transaction, mapping, conversion, rounding, aggregation, or unexplained. Consistency proves disagreement only; an independent ledger/source-document procedure adjudicates accuracy. Evidence pins both versions, queries, crosswalk, rates, counts, excluded/unknown pairs, mismatch digests, and resolution owner.

### Answer 4

Evaluate a pinned batch with a pinned rule/reference suite and record scan coverage. Critical rules reject or hold; recoverable row-level failures may quarantine with an explicit partial-release manifest; advisory failures warn. Measurement timeout, permission, malformed rule, missing partition, or unavailable reference is unknown and fails closed for critical evidence, not pass. Apply both global and cohort gates plus non-compensable critical checks; baselines signal drift but do not replace domain thresholds. Canary rule/threshold changes on known fixtures and recent versions. Waivers name scope, reason, approver, expiry, compensating control, and repair owner. Store counts and protected digests or bounded access-controlled samples. Notifications include data/rule versions, impact, decision, owner, and retry path; retries are idempotent and never overwrite prior evidence.

### Answer 5

Discard the composite score as proof and reconstruct expected regulated-cohort entities from independent manifests/registries, including late/cancelled/applicability semantics. Pin the faulty output and trace absent IDs through collection, file arrival, parsing, filters, joins, deduplication, transformations, and publication. Quantify affected entities, decisions, money, dates, consumers, and regulatory duties. Contain by holding the cohort/product, quarantining partial output, or reverting consumers to a known version; notify with caveats. Correct the earliest controlled cause, backfill idempotently from pinned raw inputs, preserve originals/correction lineage, and validate repaired plus unaffected controls under the same contract. Republish with explicit version and reconciliation, support downstream reprocessing, and monitor coverage by cohort, execution coverage, time to detect/correct, and recurrence. Change the score/dashboard so a critical cohort cannot be averaged away.
