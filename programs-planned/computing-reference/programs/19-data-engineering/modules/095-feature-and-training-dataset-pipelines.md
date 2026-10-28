---
module_id: DE-095
program: Data Engineering
level: 2
module_number: 95
title: Feature and Training Dataset Pipelines
status: complete
last_verified: 2026-09-03
---

# Feature and Training Dataset Pipelines

## One-Page Review

### Governing question

How can a team construct features, labels, examples, splits, and training datasets that reproduce what would have been knowable at each prediction decision, match the serving computation, remain attributable to immutable inputs and code, and can be corrected, deleted, rebuilt, or compared without silently leaking future or evaluation information?

### Essential definitions

- An **entity** is the subject about which a prediction is made; its join key must be stable and scoped.
- A **prediction time** or **cutoff** is the instant at which a feature set must represent available knowledge.
- A **feature** is a versioned computation yielding a model input with declared type, entity, time, source, owner, and serving behavior.
- A **feature value event** records entity, feature, event/effective time, availability time, value, and version.
- **Point-in-time correctness** means each example uses only feature information permitted and available by its cutoff.
- A **label** is the observed target for an example, defined over an outcome window and subject to maturity, censoring, correction, and policy.
- An **example** binds entity, prediction cutoff, feature vector, label/weight, definition versions, and provenance.
- A **training dataset** is an immutable, versioned population of examples constructed under a declared observation window, eligibility policy, sampling/splitting rule, and feature/label contract.
- **data leakage** occurs when training or evaluation uses information unavailable in the intended prediction workflow or information from a held-out outcome influences fitted choices.
- **training-serving skew** is a relevant difference between the features or transformations used for offline training/evaluation and online prediction.
- An **offline store** retains historical feature values for dataset construction; an **online store** serves bounded low-latency feature state for prediction.
- A **dataset manifest** binds content or snapshot identities, schema, statistics, splits, code/environment, provenance, policy, and integrity evidence.

### Central model, mechanism, or theorem

For example $e=(k,t_e)$ and feature $f$, let candidate records have entity key $k$, event/effective time $t_f$, and availability time $a_f$. Under lookback $L_f$ and versioned eligibility policy $P$, the point-in-time feature is

$$
x_f(e)=arg\max_{r}\ (t_f(r),a_f(r),v(r))
$$

subject to

$$
k(r)=k,\quad t_e-L_f<t_f(r)\le t_e,\quad a_f(r)\le t_e,\quad P(r,e)=eligible.
$$

The availability constraint prevents a late correction or backfill describing an earlier event from leaking knowledge that did not exist at decision time. A reproducible dataset identity must also bind source snapshots, feature and label definitions, example population, split/sampling seeds and rules, transformation artifacts, policy, and code/runtime—not merely an output path.

### Critical invariants

- Every example has a stable entity/scope, prediction cutoff, selection reason, feature-definition set, label definition, split assignment, and source boundary.
- Feature event time, availability/created time, ingestion time, and processing time are distinguished and have deterministic tie-breaking and lateness rules.
- Historical retrieval never selects a feature effective after cutoff or unavailable at cutoff; label outcome and post-decision effects are excluded from features.
- Labels define trigger, horizon, maturity delay, censoring, correction, ambiguity, and negative construction; immature absence is not automatically a negative.
- Split and sampling occur before any fitted preprocessing, feature selection, vocabulary, imputation, normalization, or target encoding can observe held-out outcomes.
- Split rules prevent entity, household, session, campaign, location, near-duplicate, and temporal contamination according to the deployment claim.
- Offline and online computations share a definition or prove semantic equivalence with logged serving-value comparison, including defaults, windows, precision, and missingness.
- Dataset builds are immutable and idempotent for one contract; late changes create a new generation with lineage rather than mutating evidence invisibly.
- Every train/evaluate run resolves one manifest and verifies schema, counts, checksums, feature/label versions, split disjointness, policy, and environment.
- Consent, purpose, retention, deletion, licensing, representativeness, safety, and subgroup evidence are evaluated across sources, examples, artifacts, models, and downstream copies.

### Common failures

Joining each label to the latest feature today; filtering only feature event time while admitting later backfills; using processing time as prediction time; deriving labels from model-influenced behavior without exposure context; treating unlabeled or immature examples as negatives; random row splits across the same user or future; deduplicating after splitting; fitting scalers, imputers, vocabularies, feature selection, or target encodings on the full dataset; implementing offline and online transforms separately; using different default/null/window/timezone semantics; materializing newest events into online state without version guards; overwriting a dataset path; recording a file hash without source/code/policy identity; validating only averages; dropping anomalous or protected cohorts silently; replaying historical pipelines with present-day reference tables; failing to propagate deletion; and comparing models trained on different populations as though only algorithms changed.

### Compact example

A churn example for customer A has cutoff day 10. Feature history includes value 10 with event day 5/available day 6 and corrected value 99 with event day 8/available day 15. A join constrained only by event time chooses 99 and leaks a correction learned after prediction. The correct bitemporal join chooses 10 because both event and availability precede day 10. Its 30-day churn label is not final until day 40 plus ingestion allowance. **Conclusion:** event-time point-in-time logic, knowledge availability, and label maturity are separate correctness conditions.

### Connections

[DE-035](035-incremental-models.md) supplies versioned change processing, [DE-060](060-handling-late-duplicate-and-out-of-order-events.md) supplies temporal disorder, [DE-073](073-reconciliation-tests.md) supplies common-boundary comparison, and [DE-089](089-auditability-and-provenance.md) supplies evidence. [DE-092](092-materialized-views-and-derived-tables.md) and [DE-094](094-data-apis.md) supply versioned materialization and governed retrieval; this module specializes them for prediction-time knowledge and leakage-free evaluation.

## Governing Question

For each model decision, what entity and decision time define the example, which facts and transformations were genuinely available then, when is the target observable, what population does the dataset claim to represent, and which immutable evidence would let an independent run reproduce or invalidate every feature, label, split, and exclusion?

## Why This Matters

A model consumes numbers, categories, tokens, images, or embeddings, but its behavior is bounded by how those inputs became examples. A highly accurate learner trained on leaked future information will fail when deployed. A fair-looking aggregate can conceal missingness or label quality failures concentrated in one group. A reproducible training script is not enough when the source tables, reference data, feature definitions, and split populations have changed.

Ordinary analytical joins answer “what do we now know about this historical entity?” Training construction often needs the harder question “what could the system have known at this historical decision?” Those answers diverge when corrections, late events, slowly changing dimensions, identity merges, manual reviews, and outcome labels arrive after the decision. Point-in-time correctness is therefore bitemporal: feature effective time and knowledge availability both matter.

The training/evaluation boundary creates another temporal constraint. Evaluation data represents evidence about future generalization. If its outcomes influence feature selection, imputation, normalization, vocabulary, sampling, hyperparameters, or repeated manual choices, the resulting metric is optimistically biased. Splitting files after feature engineering does not restore independence.

Serving adds a second implementation. Offline batch systems can scan history and compute wide windows; online systems must resolve current entity state under tight latency. Different code, precision, defaults, window closure, source arrival, and update ordering produce skew. A feature store can organize definitions and retrieval, but no product name proves point-in-time correctness, label integrity, split independence, privacy, or business validity.

Data engineering owns the evidence path: immutable source boundaries, feature history, temporal joins, labels, examples, manifests, quality, lineage, backfills, deletion, online materialization, and comparison. Model metrics become interpretable only after that path is trustworthy.

## Prerequisites and Retrieval

Retrieve the prediction workflow: entity/object, decision/action, prediction instant, request context, serving latency, feature availability, model outputs, downstream intervention, exposure/selection, feedback loops, business objective, harms, abstention/manual review, owner, and retraining cadence.

Retrieve each feature contract: stable ID and semantic version, entity/join keys and scope, value type/shape/unit/domain, source product, event/effective/availability/ingestion times, aggregation window and closure, lateness, TTL, null/default, freshness, transformation, fitted artifact, offline/online implementation, owner, classification, consent/purpose, retention, cost, and deprecation.

Retrieve label contract: target event, positive/negative/unknown states, observation horizon, maturity delay, source and availability, attribution, repeated outcomes, competing events, censoring, adjudication, correction/retraction, model intervention, selection/exposure, human annotation, confidence, policy, and owner.

Retrieve example/population logic: eligibility, unit, trigger/cadence, lookback and forecast horizons, observation dates, cohort, geographic/product scope, exclusions, sampling probability/weight, duplicate/identity rules, class balancing, split unit, temporal gaps, random seed, grouping constraints, and representativeness claim.

Retrieve pipeline state: source snapshots/offsets, feature registry/definitions, code and dependency image, parameters, credentials, orchestration run/attempt, checkpoints, backfill ranges, output generation, manifest/checksums, schema/stats, quarantine, validation decisions, reviewer/approval, model/experiment references, and deletion lineage.

Retrieve serving evidence: online keys and TTL, source-to-online materialization boundary, per-entity version guards, online schema/defaults, freshness/availability, logged feature vectors, request/model/feature versions, shadow comparisons, latency/error/missingness, rollback, and incident records.

Distinguish entity time from ingestion time; feature effective time from availability; present historical truth from historically available knowledge; feature definition from stored value; offline history from online latest state; label event from label availability and maturity; missing label from negative; prediction population from observed outcome population; random row split from independent evaluation; deterministic code from reproducible inputs; dataset hash from semantic identity; drift from skew; correlation from leakage; deletion from exclusion; and feature-store capability from verified end-to-end correctness.

Create a training dataset contract:

| Concern | Required evidence and decision |
|---|---|
| Decision | Entity, cutoff, action, population, exposure and harm |
| Features | IDs/versions, sources, event/availability time, windows, transforms and defaults |
| Labels | Definition, horizon, maturity, censoring, correction and intervention |
| Examples | Eligibility, exclusions, duplicates, weights, sampling and stable identity |
| Splits | Temporal/group unit, gaps, seed/rule, fitted-transform boundary and disjointness |
| Execution | Source snapshots, code/runtime, point-in-time plan, budgets and idempotency |
| Evidence | Manifest, schema, statistics, checksums, lineage, tests and review |
| Lifecycle | Online materialization, skew monitoring, backfill, deletion, migration and retirement |

Write a falsifiable claim: “Dataset generation G constructs one example per `(tenant,customer,prediction_time)` for eligible decisions in interval I; joins feature set F using effective and availability time under versioned TTL/tie rules; attaches label L only after horizon H and maturity M with explicit censored/unknown states; assigns grouped temporal splits by rule S before fitting transformation artifacts T; validates content, subgroups, leakage sentinels and offline/online equivalence; publishes immutable manifest D with source/code/policy identities and checksums; and propagates corrections/deletions through models and artifacts under process R.”

## Learning Objectives

After completing this module, you should be able to:

1. define entities, prediction cutoffs, feature value histories, labels, examples, datasets, and their stable identities;
2. implement bitemporal point-in-time joins with lookbacks, TTLs, tie-breaking, missingness, late data, corrections, and backfills;
3. design label horizons, maturity, censoring, exposure, attribution, ambiguity, retraction, and negative construction;
4. prevent target, future, preprocessing, duplicate, identity, group, temporal, reference-table, and feedback leakage;
5. choose split and sampling rules aligned with the intended deployment and preserve probabilities/weights;
6. share or prove equivalent offline/online feature transformations, state, precision, defaults, windows, and version ordering;
7. build immutable manifests binding source snapshots, code/runtime, definitions, fitted artifacts, populations, splits, statistics, checksums, policy, and provenance;
8. validate schema, semantics, point-in-time behavior, split independence, subgroup coverage, drift/skew, online materialization, and reproducibility;
9. operate incremental builds, backfills, feature/label evolution, retraining, rollback, retention, consent withdrawal, and deletion safely; and
10. evaluate feature pipelines by correctness, freshness, representativeness, reliability, cost, and downstream outcomes—not model accuracy alone.

## Core Exposition

### Begin with the prediction event

Name what is being predicted, for which entity, at what instant, before which action, and for what decision. “Customer churn features” is incomplete. “At the weekly renewal review, predict whether an active subscription will voluntarily terminate within 30 days before any retention contact” defines cutoff, population, horizon, intervention boundary, and label.

Use a stable example key such as `(tenant,subscription_id,prediction_time,example_definition_version)`. Entity keys must be immutable or historically resolvable; email, device IDs, and mutable account aliases can merge people or change owners. Model many-to-one and one-to-many relationships deliberately. A household feature for a user needs scope and leakage review because related entities can cross splits.

Record why each example exists. Periodic snapshots overrepresent long-lived entities; event-triggered examples represent a different population. If serving predicts only after a user opens a page, training on every registered user creates a population mismatch. Eligibility and exposure are first-class definitions, not cleanup filters.

### Model feature time as more than one timestamp

A feature record needs entity key, feature ID/version, value, event or effective time, availability/created time, ingestion/processing time, and deterministic sequence. Event time says when the fact applies. Availability says when the prediction system could have learned it. Ingestion/processing supports operations but is not automatically either semantic time.

For each example cutoff, choose the latest eligible record whose effective time is within the feature lookback and no later than cutoff, and whose availability is no later than cutoff. Tie-break using stable source version/sequence. A correction written today for an event last month belongs to present historical truth; it must not rewrite the knowledge state of a model decision made last month unless the evaluation explicitly studies corrected omniscient history.

Define window endpoints precisely. “Last seven days” needs timezone, calendar versus duration, `(cutoff-7d,cutoff]` or another interval, event-time attribution, lateness, and whether the triggering event itself is visible. Features computed from the outcome window are leakage. TTL is a semantic eligibility rule when it expresses staleness; it is not merely online cache eviction.

Use left joins from the example spine so missing history remains observable. Inner joins silently change the population to entities with data. Distinguish no record, stale record, source unavailable, redacted value, computation error, and genuine zero. Missing indicators can be useful but may encode infrastructure or protected-group differences and require review.

### Define labels as delayed governed data

A label is a pipeline, not a convenient column. Define the outcome event, horizon relative to cutoff, attribution, positive/negative/unknown, repeated events, competing outcomes, and when observation is mature. A 30-day churn negative cannot be finalized on day 12. Add source delay and correction allowance to the horizon or mark it censored/immature.

Separate label event time, availability, adjudication, and finality. Fraud chargebacks, diagnoses, human reviews, and returns can arrive or reverse months later. Version and retract labels. Retraining after corrections creates a new dataset generation; do not overwrite the evidence used by a released model.

Account for exposure and interventions. A click is observable only for an item shown. Defaulting unshown candidates to “not clicked” confounds selection with preference. A retention offer caused by an earlier model changes churn outcomes. Log policy/model version, action, assignment probability, position, eligibility, and outcome opportunity so qualified causal or counterfactual methods can be applied; ordinary supervised joins do not remove feedback bias.

For human labels, capture rubric/version, annotator or protected pseudonymous identity, adjudication, disagreement, confidence, source context, and quality controls. Avoid leaking annotator identifiers or post-outcome notes as model features. Licensing, consent, labor, and safety obligations follow the labels and raw content.

### Split before learning from data

The split rule must match the generalization claim. Random examples may estimate performance on interchangeable future samples only when examples are sufficiently independent and stationary. For future deployment, train on earlier time, validate on a later interval, and test on a final untouched interval. Add temporal gaps when windows or delayed labels overlap boundaries.

Group entities that can share information: user, household, patient, session, device, merchant, campaign, document family, location, or near-duplicate content. One person in train and test lets identity-specific features or repeated events leak. Deduplicate and cluster before splitting, or assign clusters deterministically; deduplicating each split afterward does not prevent cross-split twins.

Fit all learned preprocessing on training only: imputation statistics, normalization, quantile buckets, vocabularies, encoders, feature selection, dimensionality reduction, learned embeddings, target encoding, resampling, and even manual choices informed by labels. Apply the frozen artifact to validation/test. Cross-validation repeats fitting inside each fold. Keep the final test set outside repeated experimentation; otherwise it becomes validation by human feedback.

Sampling changes the estimand. Record inclusion probability and weights, stratification, class balancing, downsampling, and exclusions. Preserve unsampled counts and population metadata. A balanced classifier dataset does not represent production prevalence; calibration and decision thresholds require appropriate weighting/evaluation.

### Make feature definitions executable and versioned

A feature definition includes semantic name, entity, type/shape/unit, source, transformation, window, time fields, TTL, missing/default behavior, owner, policy, offline and online realization, dependencies, and compatibility. Version meaning changes, not every materialization run. A registry helps discovery but must be backed by executable code and tests.

Prefer one transform representation usable in batch and serving, or generate both paths from one typed intermediate definition. Some transforms require dataset-wide fitted state: means, quantiles, vocabularies, embeddings, or category maps. Fit that state from the training split, version it as an artifact, and deploy the same artifact with the model. Recomputing “current” normalization online changes the feature space.

When separate implementations are unavoidable, define semantic equivalence over golden cases and logged production samples. Compare presence, type, shape, exact/canonical value or tolerance, default reason, event/availability time, and version. Decimal/float precision, integer overflow, timezone, Unicode, library versions, and ordering can produce subtle skew.

Feature reuse is not automatically safe. A fraud feature derived from chargebacks may leak into an earlier credit-decision problem if availability differs. A feature approved for operational security may not be permitted for marketing. Reuse the governed definition only when entity, time, purpose, population, policy, and serving semantics match.

### Separate historical construction and online serving

Offline history supports point-in-time scans, backfills, corrections, and large training joins. Online storage supports low-latency current lookup, usually one or a bounded number of versions per entity. The two projections serve different workloads and need a common definition, identity, and reconciliation boundary.

Materialize online records with per-entity feature version/event sequence guards. A late older event must not overwrite newer state unless the feature's semantics explicitly recompute it. Batch and streaming producers need one ordering/conflict policy. Record source boundary and value availability; “latest write” is not necessarily latest event.

Online lookup defines key normalization, missing/expired behavior, timeout fallback, partial feature groups, batch consistency, and freshness. Defaults can be model inputs and must be identical offline. Failing open to zero online while dropping missing rows offline is skew. If multiple feature groups are read, state whether their versions form one snapshot or an allowed mixed-freshness envelope.

Log a sampled, policy-approved serving feature vector or safe digest with request/entity, model, feature-service/definition versions, value times, default reasons, and outcome join identity. Compare it later with offline reconstruction at the same cutoff. Logging is empirical evidence and sensitive data; minimize, encrypt, retain, and restrict it.

### Build immutable training datasets

Resolve all inputs before execution: source table snapshots or event offsets, example spine, feature definitions, label version, identity map, reference data as-of rules, policy, split/sampling rule, code commit, container/dependencies, parameters, and secrets by reference. Reject floating “latest” dependencies for a reproducible generation.

Use a staged build. Validate source boundaries and completeness; generate examples; perform point-in-time joins; attach only mature labels; apply eligibility, consent, and exclusions; assign splits; fit training-only artifacts; transform each split; calculate content and subgroup statistics; run leakage/skew/invariant tests; write immutable shards; verify checksums and counts; publish manifest atomically.

Dataset identity should bind canonical contract and immutable inputs. A content hash is helpful but not sufficient: noncanonical order may change it, collisions/partial hashing can mislead, and identical bytes under a changed meaning/policy are a different governed object. Store both content integrity and semantic/provenance identity.

Manifest fields include dataset ID/generation, purpose/owner, example/feature/label/split versions, observation and outcome intervals, source snapshot/offset identities, code/runtime, transformations and fitted artifacts, schema, per-split rows/bytes, checksums, sampling weights, statistics, missingness, class balance, subgroup coverage, exclusions/quarantine, policy/classification/license, creation/expiry, parent generation, validation/review, and known limitations.

Training accepts only published manifests. It verifies files, checksums, schema, split identities, and policy, then logs the exact dataset reference into the model/experiment lineage. Never let a trainer glob a mutable directory whose contents can change between retries.

### Validate correctness beyond schema

Schema checks types, shapes, requiredness, domains, and ranges. Semantic tests verify entity grain, uniqueness, units, sign, relationship constraints, temporal order, window behavior, label maturity, forbidden fields, and stable examples. Distribution statistics find unexpected missingness, cardinality, quantiles, category changes, class balance, and slice failures, but thresholds need domain ownership.

Build leakage sentinels. Assert no selected feature has effective or availability time after cutoff; no feature dependency reaches label/outcome/post-decision actions; no fitted artifact reads validation/test; train/test group identities and near-duplicate clusters are disjoint; reference tables use historical versions; and performance collapses appropriately when synthetic future signals are removed. Extremely predictive features deserve causal/temporal investigation, not celebration alone.

Recompute a sample through an independent or simpler oracle. Inspect temporal edge cases: exact cutoff, TTL boundary, tied events, late correction, deleted value, identity merge/split, daylight-saving/calendar transition, label just immature, and missing source partition. Reconcile row accounting from candidate population to eligible, excluded by reason, immature/censored, quarantined, and each split.

Evaluate slices aligned with product risk and data collection: geography, language, device, acquisition channel, tenure, accessibility, protected classes where lawful/ethical, missingness patterns, and rare conditions. Aggregate pass rates can hide a completely missing cohort. Quality gates should quarantine or stop with explicit owner/expiry, not silently delete difficult examples.

### Operate increments, backfills, and evolution

Incremental builds need stable example identity and versioned dependencies. A new feature value, corrected label, identity change, consent withdrawal, or feature-definition change determines an affected example interval. Windowed features propagate source changes forward across their lookback influence; labels propagate across outcome windows. Track dependency intervals rather than rebuilding arbitrary recent days.

Backfills are migrations. Pin code, definitions, source/history availability, policy, and target generation; estimate cost; isolate from recurring/online workloads; dry-run affected counts; canary representative periods/entities; compare against old generation; publish atomically; retain rollback; and prevent an older backfill from overwriting newer online values.

Classify evolution. Adding an optional feature can change model inputs, cost, policy, missingness, and strict schemas. Changing a window or default is semantic. Renaming while retaining meaning needs aliases and lineage. Label revisions invalidate comparisons. Build old/new datasets from common source boundaries, produce per-feature and per-slice diffs, retrain/evaluate under controlled experiment, and migrate named consumers.

Do not compare model A on dataset generation 7 with model B on generation 9 and attribute the metric delta solely to the model. Factor changes in population, labels, features, splits, and code. Maintain benchmark/evaluation datasets with their own governance, but refresh them deliberately when they cease representing deployment; permanence can also create overfitting and staleness.

### Govern privacy, deletion, and retirement

Feature pipelines multiply sensitive data into offline history, online state, training shards, caches, notebooks, experiment artifacts, models, logs, and exports. Classification and purpose flow through derivations. Hashing entity IDs supports joins but does not anonymize linkable behavioral histories. Restrict discovery metadata and statistics that reveal sensitive cohorts.

Consent or deletion requests need a lineage-driven process: identify raw records, feature histories, online state, examples, datasets, caches, embeddings, model influence where policy/law requires, serving logs, and external copies. Decide whether to delete, retrain, suppress, quarantine, or retain under a valid exception/hold, with qualified governance. Record tombstones so backfills do not resurrect removed data.

Retire a feature only after registry consumers, active dataset manifests, models, online services, training jobs, notebooks, monitoring, and backfills have migrated or expired. Stop new publication, remove online materialization, preserve required historical reproducibility under access/retention rules, delete prohibited artifacts, and verify no fallback silently restores the old feature.

## Definitions and Notation

Let example $e=(k,t_e,d_e)$ contain scoped entity key $k$, prediction cutoff $t_e$, and decision context $d_e$. Feature record $r=(k,f,v,t_f,a_f,i_f,x)$ contains feature $f$, definition/value version $v$, event/effective time $t_f$, availability time $a_f$, ingestion time $i_f$, and value $x$.

For lookback/TTL $L_f$, point-in-time selection is

$$
J_f(e)=arg\max_{r\in R_f}(t_f(r),a_f(r),v(r))
$$

over records satisfying entity/scope, $t_e-L_f<t_f(r)\le t_e$, $a_f(r)\le t_e$, and policy. Define $x_f(e)=missing(reason)$ when no eligible record exists; absence is not coerced to zero.

For label horizon $H$ and maturity allowance $M$, label query observes outcomes in $(t_e,t_e+H]$ but is final only at build knowledge boundary $b\ge t_e+H+M$, subject to label-specific corrections/censoring. Thus `no positive observed` before maturity is `immature`, not negative.

Let split function $S(e,g,time,seed)\in\{train,validation,test,excluded\}$ operate on a stable group $g$ and time before fitted transform $T_{train}$ is learned. Required independence is scoped to the deployment claim; formally disjoint row IDs alone are insufficient when information crosses groups or time.

Let dataset manifest identity be

$$
D=id(E,F,L,S,T,I,C,P),
$$

binding example rule $E$, feature set $F$, label $L$, split/sampling $S$, fitted transforms $T$, immutable source inputs $I$, code/runtime $C$, and policy $P$. Content checksums verify artifacts associated with $D$ but do not replace these semantic bindings.

For logged online vector $x^{on}_f(e)$ and offline reconstruction $x^{off}_f(e)$, skew is evaluated under feature-specific equivalence $\equiv_f$ and missing/default reason. Match rate without time/version agreement can conceal incorrect equality.

## Mechanisms, Invariants, or Proof Structure

### Dataset build and publication mechanism

1. Freeze prediction/example, feature, label, eligibility, sampling, split, policy, and quality contracts.
2. Resolve immutable source snapshots/offsets, identity/reference histories, code, dependencies, parameters, and runtime.
3. Validate source completeness, temporal fields, keys, duplicates, deletion state, and expected population.
4. Construct the example spine with stable IDs, scoped entities, prediction cutoffs, exposure/context, and selection reasons.
5. Retrieve each feature using entity, effective-time, availability-time, TTL, policy, and deterministic tie-breaking.
6. Attach label states only under outcome-window, availability, maturity, censoring, attribution, and correction rules.
7. Cluster/deduplicate information-sharing units; assign temporal/grouped splits and sampling probabilities deterministically.
8. Fit preprocessing/selection artifacts on training only; freeze them and transform validation/test/serving-compatible outputs.
9. Validate schema, semantic invariants, point-in-time constraints, leakage sentinels, split disjointness, distributions, subgroups, and offline/online equivalence.
10. Reconcile all candidate examples into terminal inclusion/exclusion/quarantine/maturity/split categories.
11. Write immutable shards, statistics and manifest; verify counts/checksums and publish one complete generation atomically.
12. Bind training/model lineage to that generation; monitor online values, outcomes, corrections, drift/skew, deletion and consumer use.

### Conditional claim: bitemporal selection prevents direct future-record leakage

**Claim.** For an example cutoff $t_e$, if every feature dependency is represented by records with truthful effective and availability times, the join admits only $t_f\le t_e$ and $a_f\le t_e$, and transformations use only admitted dependencies and training-fitted artifacts, then no directly selected feature record contains information first available after $t_e$.

**Proof sketch.** Every selected record satisfies the availability predicate by construction, and closure of transformations over admitted dependencies cannot introduce a later record. The claim fails if timestamps are false/coarse, a reference table is read at present state, a transform reaches outcomes or future aggregates, identity resolution uses later knowledge, preprocessing observes held-out data, or information leaks through selection/exposure. Point-in-time joins are necessary, not sufficient, for total leakage freedom.

### Conditional claim: train-only fitting preserves direct test exclusion

**Claim.** Suppose split assignment is fixed before fitting, related/duplicate information units are grouped according to the evaluation claim, and every data-dependent transform/model/hyperparameter choice in one evaluation is fitted without test inputs or outcomes. Then the test set has no direct computational path into the fitted pipeline for that evaluation.

**Proof sketch.** By the pipeline dependency graph, every fitted artifact's ancestors lie in training (or explicitly permitted external fixed artifacts), while test nodes are descendants only through transform and scoring. The claim fails through repeated human test inspection, global preprocessing, group/temporal dependence, benchmark memorization, external artifacts trained on test-correlated data, or feedback. Statistical independence and real-world validity require stronger assumptions than graph exclusion.

### Executable point-in-time availability illustration

This deterministic fixture contrasts “latest value today” with selection constrained by entity, feature event time, and knowledge availability at each example cutoff. It demonstrates one leakage mechanism; it does not prove timestamp truth, dependency closure, label quality, split independence, identity correctness, or online equivalence.

<!-- bijux-verify: {"id":"bitemporal-feature-selection","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"naive_values=99,22,30\ncorrect_values=10,20,missing\nfuture_or_late_excluded=3\nall_selected_available=true\n","stderr":""}} -->
```python
examples = [
    {"entity": "a", "cutoff": 10},
    {"entity": "b", "cutoff": 10},
    {"entity": "c", "cutoff": 10},
]
features = [
    {"entity": "a", "event": 5, "available": 6, "value": 10},
    {"entity": "a", "event": 8, "available": 15, "value": 99},
    {"entity": "b", "event": 6, "available": 7, "value": 20},
    {"entity": "b", "event": 12, "available": 12, "value": 22},
    {"entity": "c", "event": 9, "available": 11, "value": 30},
]


def latest(records: list[dict[str, int | str]]) -> dict[str, int | str] | None:
    return max(records, key=lambda row: (row["event"], row["available"])) if records else None


naive = []
correct = []
excluded = 0
selected_records = []
for example in examples:
    entity_records = [row for row in features if row["entity"] == example["entity"]]
    naive_record = latest(entity_records)
    naive.append(str(naive_record["value"]) if naive_record else "missing")

    eligible = [
        row
        for row in entity_records
        if row["event"] <= example["cutoff"] and row["available"] <= example["cutoff"]
    ]
    excluded += len(entity_records) - len(eligible)
    selected = latest(eligible)
    correct.append(str(selected["value"]) if selected else "missing")
    if selected:
        selected_records.append((selected, example["cutoff"]))

print(f"naive_values={','.join(naive)}")
print(f"correct_values={','.join(correct)}")
print(f"future_or_late_excluded={excluded}")
print(
    f"all_selected_available={all(row['event'] <= cutoff and row['available'] <= cutoff for row, cutoff in selected_records)}".lower()
)
```

## Alternatives and Trade-Offs

- **Compute on read versus materialize features:** read-time computation centralizes current logic and avoids duplicated state; materialization meets latency and historical reuse needs but adds ordering, freshness, storage, and reconciliation.
- **Log served features versus reconstruct:** logging best captures actual prediction inputs; reconstruction reduces sensitive duplication but depends on complete history and semantic equivalence. Sampled protected logs plus reconstruction comparison often complement each other.
- **One transform implementation versus equivalent paths:** shared code reduces skew; distinct batch/online implementations may optimize their workloads but require extensive golden, shadow, and production comparison.
- **Event-time-only versus bitemporal history:** event time is simpler and can represent corrected truth; availability time is required to reproduce historical knowledge but increases storage, join, and source-instrumentation demands.
- **Random versus temporal split:** random splits use data efficiently under exchangeability; temporal splits better model future deployment and drift but can reduce sample balance and expose decay.
- **Row versus group split:** row splits maximize mixing; group splits reduce identity/relationship leakage at the cost of fewer independent units and harder stratification.
- **Fixed benchmark versus rolling evaluation:** fixed sets improve comparability; repeated tuning overfits them and they age. Rolling sets improve relevance but complicate longitudinal attribution.
- **Drop missing versus preserve missingness:** dropping simplifies tensors but changes population; preserving reasoned missingness exposes serving behavior and supports explicit imputation while potentially adding features correlated with infrastructure.
- **Backfill corrected truth versus preserve historical knowledge:** corrected datasets answer omniscient retrospective questions; availability-constrained datasets reproduce decisions. Keep the purposes and generations distinct.
- **Full rebuild versus affected-range repair:** rebuild is a strong oracle and simplifies reasoning; targeted repair saves cost but needs accurate temporal dependency propagation and reconciliation.
- **Mutable tables versus immutable dataset generations:** mutation saves storage and gives one “latest”; immutable generations enable audit, comparison, rollback, and model lineage.
- **Feature reuse versus task-specific definition:** reuse reduces duplication; differing cutoffs, purposes, populations, TTLs, and labels can make a shared feature unsafe or misleading.
- **Aggressive quality rejection versus quarantine:** stopping prevents bad training; quarantining can preserve unaffected work and evidence, but exceptions need ownership, expiry, and bias analysis.
- **Frequent retraining versus gated retraining:** frequency reacts to change; every build consumes resources and can amplify noisy labels. Trigger from measured freshness, drift, performance, correction, and policy needs.

## Failure Modes and Misconceptions

1. **“Historical event time guarantees point-in-time correctness.”** Late availability and present-day corrections can still leak.
2. **“The latest row is the best feature.”** It may be future relative to prediction or an older event delivered later.
3. **“Created time is always availability.”** It must reflect when the prediction path could use the value, not an arbitrary warehouse write.
4. **“TTL is only caching.”** In historical retrieval it can define semantic staleness and missingness.
5. **“Inner joining improves data quality.”** It silently excludes entities without feature history and changes the population.
6. **“Missing means zero.”** No event, stale value, suppression, outage, and true zero are different states.
7. **“No positive outcome means negative.”** The label may be immature, censored, unexposed, delayed, or unknown.
8. **“Labels are ground truth.”** They can reflect measurement, policy, intervention, annotator, selection, and correction processes.
9. **“Random split prevents leakage.”** Related entities, repeated users, near duplicates, overlapping windows, and future information can cross it.
10. **“Deduplication after splitting is enough.”** A twin can remain in another split; cluster before assignment.
11. **“Preprocessing is not training.”** Fitted means, vocabularies, selection, target encoding, and imputation learn from data.
12. **“The test set stays valid indefinitely.”** Repeated inspection and decisions adapt to it.
13. **“A common schema prevents training-serving skew.”** Values, transforms, defaults, windows, precision, sources, and timing can differ within one schema.
14. **“A feature store guarantees correctness.”** Capabilities require truthful timestamps, definitions, policies, joins, tests, and operations.
15. **“Same feature name means same meaning.”** Entity, window, source, version, units, availability, purpose, and defaults may differ.
16. **“Code version reproduces a dataset.”** Source snapshots, dependencies, policy, seeds, fitted artifacts, and runtime also matter.
17. **“A dataset hash captures semantics.”** It verifies selected bytes under a method, not meaning, policy, completeness, or lineage.
18. **“Overwriting corrected data improves reproducibility.”** It destroys evidence of what trained earlier models.
19. **“Aggregate validation protects every cohort.”** Rare or protected slices can fail while totals pass.
20. **“High predictive power proves a good feature.”** It may reveal label leakage, identity memorization, selection, or prohibited proxies.
21. **“Drift and skew are the same.”** Drift compares populations over time; skew compares relevant pipeline/environments and can exist without temporal drift.
22. **“Sampling only changes dataset size.”** It changes prevalence, estimands, calibration, variance, and coverage unless weighted appropriately.
23. **“Old backfills cannot affect serving.”** Unversioned last-write-wins materialization can overwrite current online state.
24. **“Deleting the raw row removes it everywhere.”** Derived features, datasets, models, logs, caches, and exports need lineage-guided handling.
25. **“Higher offline accuracy completes the pipeline.”** Reliability, fairness, freshness, cost, serving equivalence, policy, and real outcomes remain.

## Worked Examples

### Example 1

**Situation.** A corrected balance has event day 8 but becomes available day 15; prediction cutoff is day 10. **Reasoning.** Event-time-only retrieval leaks the correction. Bitemporal selection chooses the prior eligible value and records later correction for a new dataset generation. **Conclusion.** Reproducing knowledge needs availability as well as effective time.

### Example 2

**Situation.** A 30-day default model builds examples every night. **Reasoning.** Cutoffs younger than 30 days plus source-delay allowance receive `immature`, not negative. Competing closure and missing follow-up become explicit censored states. **Conclusion.** Label maturity protects both correctness and calibration.

### Example 3

**Situation.** The same shopper appears in thousands of train and test rows. **Reasoning.** A random row split lets identity history cross the boundary. The team assigns customer/household groups to temporal splits and measures the lower but honest score. **Conclusion.** Split unit follows information dependence, not row convenience.

### Example 4

**Situation.** A standardizer is fitted before the train/test split. **Reasoning.** Test distribution influences mean/variance and evaluation. The corrected pipeline splits first, fits only on train, freezes the artifact, and applies it unchanged to validation/test/serving. **Conclusion.** Preprocessing belongs inside the fitted boundary.

### Example 5

**Situation.** Offline `age_days` uses UTC floor while online uses local calendar and defaults missing signup to zero. **Reasoning.** Golden cutoff cases and sampled served vectors expose discrepancies. One versioned transform and explicit missing reason replace both implementations. **Conclusion.** Matching columns do not prove matching features.

### Example 6

**Situation.** A feature stream receives version 12 then delayed version 11. **Reasoning.** Online storage conditionally applies the greater per-entity semantic version and records the rejection; offline history retains both for audit. **Conclusion.** Arrival order must not silently define current feature state.

### Example 7

**Situation.** Only shown recommendations can be clicked. **Reasoning.** Treating unshown items as negatives learns the old ranking policy. Examples capture candidate eligibility, exposure, position, serving model, assignment probability, and observed outcome opportunity. **Conclusion.** Labels inherit the decision policy that generated them.

### Example 8

**Situation.** A training directory is overwritten after a label correction. **Reasoning.** The old model can no longer be reproduced. The repair publishes a child generation with pinned sources, code, label version, manifests and checksums; the model registry retains the old identity. **Conclusion.** Corrections create lineage, not invisible mutation.

### Example 9

**Situation.** Overall missingness is 2%, but it is 70% for one language. **Reasoning.** Per-slice gates quarantine the affected interval, identify an upstream parser, and prevent silent removal that would erase the group. **Conclusion.** Aggregate quality can conceal representational failure.

### Example 10

**Situation.** A user deletion arrives after five models used their examples. **Reasoning.** Lineage locates feature history, online values, datasets, logs and models; qualified policy decides deletion/retraining/suppression or documented hold, writes tombstones, and tests that backfill cannot resurrect data. **Conclusion.** Dataset lifecycle extends beyond files.

## Cross-Program Connections

- [DE-035](035-incremental-models.md), [DE-049](049-run-metadata-and-operational-state.md), and [DE-060](060-handling-late-duplicate-and-out-of-order-events.md) provide incremental identity, run evidence, version ordering, corrections and lateness.
- [DE-063](063-table-metadata-and-snapshots.md), [DE-066](066-time-travel-and-reproducible-reads.md), and [DE-073](073-reconciliation-tests.md) provide immutable source identity, reproducible reads, and common-boundary recovery patterns.
- [DE-074](074-freshness-and-timeliness.md), [DE-076](076-data-contracts.md), and [DE-082](082-dataset-and-column-lineage.md) provide temporal SLOs, product definitions and dependency evidence.
- [DE-085](085-classification-and-sensitive-data.md), [DE-086](086-access-control-for-analytical-data.md), [DE-088](088-retention-and-deletion.md), and [DE-089](089-auditability-and-provenance.md) govern features, labels, training artifacts, use and lifecycle.
- [DE-092](092-materialized-views-and-derived-tables.md) provides immutable generations and atomic publication; [DE-094](094-data-apis.md) provides governed historical/online retrieval and exact result contracts.
- [API-021](../../28-api-and-service-engineering/modules/021-api-contracts-and-behavioral-guarantees.md), [API-024](../../28-api-and-service-engineering/modules/024-request-and-response-modeling.md), and [API-082](../../28-api-and-service-engineering/modules/082-additive-and-breaking-changes.md) connect feature contracts, typed representations and evolution.
- [API-067](../../28-api-and-service-engineering/modules/067-idempotent-consumers.md) and [API-070](../../28-api-and-service-engineering/modules/070-designing-an-asynchronous-api-for-replay-and-evolution.md) connect duplicate ingestion, ordered effects, replay and versioned pipeline state.
- [PLAT-073](../../29-platform-engineering/modules/073-resource-quotas.md), [PLAT-077](../../29-platform-engineering/modules/077-admission-control.md), and [PLAT-089](../../29-platform-engineering/modules/089-cost-allocation-and-efficiency.md) connect bounded backfills/training, workload isolation and cost ownership.
- [DE-096](../ROADMAP.md) turns freshness and completeness for these feature, label, dataset and serving boundaries into explicit SLOs.

## References

- Feast project, “Point-in-Time Joins,” current project documentation. <https://github.com/feast-dev/feast/blob/master/docs/getting-started/concepts/point-in-time-joins.md>
- TensorFlow, “TensorFlow Data Validation: Checking and Analyzing Your Data,” current TFX guide. <https://www.tensorflow.org/tfx/guide/tfdv>
- TensorFlow, “The Transform TFX Pipeline Component,” current TFX guide. <https://www.tensorflow.org/tfx/guide/transform>
- Amazon Web Services, “Feature Store Concepts,” current SageMaker AI documentation. <https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-concepts.html>
- Amazon Web Services, “Feature Store Offline Store Data Format,” current SageMaker AI documentation. <https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-offline.html>
- MLflow project, “ML Dataset Tracking,” current documentation. <https://mlflow.org/docs/latest/dataset/>
- scikit-learn project, “Common Pitfalls and Recommended Practices,” current documentation. <https://scikit-learn.org/stable/common_pitfalls.html>
- Google, “Rules of Machine Learning,” current engineering guidance. <https://developers.google.com/machine-learning/guides/rules-of-ml>
- Google Research, Sculley et al., “Hidden Technical Debt in Machine Learning Systems,” 2015. <https://research.google/pubs/hidden-technical-debt-in-machine-learning-systems/>
- Google Research, Breck et al., “The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction,” 2017. <https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/>
- National Institute of Standards and Technology, “AI Risk Management Framework,” current resource. <https://airc.nist.gov/airmf-resources/airmf/>

## Exercises

### Exercise 1

For three examples all cut off at time 10, reproduce the executable feature histories for entities A, B, and C. Derive naive latest and bitemporal selections, missing reason, excluded counts, and the effect of omitting availability time. Add a TTL of five and state endpoint semantics.

### Exercise 2

Design labels for “voluntary subscription churn within 30 days.” Include cutoff, outcome window, source availability, maturity, cancellation/restart, involuntary payment failure, censoring, retention intervention, corrections, negative state, and example rebuild behavior.

### Exercise 3

An application has repeated users, households, sessions, near-duplicate documents, seven-day feature windows, weekly seasonality, and a future deployment. Design train/validation/test split, temporal gaps, grouping/deduplication, sampling/weights, preprocessing, and final test governance. Explain the claim it can and cannot support.

### Exercise 4

Design offline and online handling for a 24-hour purchase-count feature fed by batch and streaming sources. Specify identity, event/availability/ingestion time, ordering, late data, correction/retraction, window closure, TTL, defaults, materialization, version guards, retrieval, logging, reconciliation, and backfill.

### Exercise 5

An organization has 600 features, duplicate names, undocumented labels, random row splits, mutable training folders, separate Python/Java transforms, no served-value logs, and models whose source datasets are unknown. Design a risk-prioritized recovery with measurable completion evidence.

## Answers to the Exercises

### Answer 1

Naive latest ignores cutoff and yields A=99, B=22, C=30. For A, value 10 has `(event=5,available=6)` and value 99 has `(8,15)`; cutoff 10 excludes 99 by availability and selects 10. For B, `(6,7,value=20)` qualifies while `(12,12,value=22)` is future, so select 20. For C, `(9,11,value=30)` is effective but unavailable, so output `missing(not_yet_available)`. Three records are excluded and every selected record satisfies both times.

Omitting availability would choose A=99 because event 8 precedes cutoff, leaking a correction learned at 15, and choose C=30 despite its not being knowable until 11. With TTL five and interval `(cutoff-5,cutoff]`, A's event 5 lies at the excluded lower endpoint under the stated convention and becomes missing; B's event 6 remains; C remains unavailable. If the intended endpoint is inclusive, use `[cutoff-5,cutoff]` and document/test it—never let SQL defaults decide.

### Answer 2

Create one example at the pre-action renewal-review cutoff for an active subscription. Observe voluntary customer-initiated termination in `(cutoff,cutoff+30d]`. Record event and source availability, then wait 30 days plus the measured ingestion/correction allowance before final negative. Before then the state is immature. Loss of observation, account migration, or study end creates censored/unknown, not negative.

Define restart: either any termination is positive, or termination followed by restart inside a grace interval is a distinct/transient class. Treat involuntary payment failure separately because its mechanism and intervention differ. Version these choices. A cancellation requested before cutoff must either make the example ineligible or be an available feature; it cannot become a surprise label.

Log whether the customer received a retention intervention, which policy/model assigned it, time, offer and assignment probability. Outcomes under intervention do not directly estimate no-intervention risk. Corrections or reversed cancellations retract the label and publish a child dataset generation identifying affected examples/models. Do not mutate the old artifact. Mature no-voluntary-churn under complete observation is negative; every other state keeps its reason.

### Answer 3

Cluster near-duplicate documents before splitting and define an information group at least as broad as household, containing its users, sessions and related duplicates where leakage is plausible. Assign groups deterministically. Use training on earlier weeks, validation on later weeks, and a final test interval after validation. Place at least a seven-day gap—or a stronger domain-derived gap—where feature windows or label horizons would cross boundaries. Preserve weekly cycles in each sufficiently long interval and report seasonal coverage.

Sample only after defining the target population; record inclusion probabilities and apply weights for metrics/calibration when sampling is unequal. Do not balance test away from deployment prevalence. Fit deduplication models requiring learned thresholds, imputers, normalizers, vocabularies, feature selection, target encodings, embeddings and resampling only within training/folds. Validation drives hyperparameters; the final temporal grouped test remains sealed until the pipeline is fixed. Repeated test inspection requires a new honest test.

This estimates performance on later examples from previously unseen defined groups under the observed collection/policy regime and covered seasons. It does not prove behavior under new geography, product changes, interventions, distribution shifts, unobserved groups, bad labels, or much later time. Grouping reduces identified dependence but cannot establish statistical independence from hidden relationships.

### Answer 4

Define feature ID/version, scoped customer key, integer count/unit, `(cutoff-24h,cutoff]`, qualifying purchase semantics, refund/cancel treatment, event time, source availability, ingestion time, sequence, owner and policy. Retain event/change history offline. Deduplicate stable purchase IDs, order revisions by source version, apply retractions for cancellations/refunds, and bound allowed lateness. Window output records its effective cutoff and availability.

Batch and stream use one aggregation specification or prove equivalence. Online updates use per-customer/window/definition version guards so delayed older batches cannot overwrite newer state. A correction recomputes affected windows and emits a higher semantic version. TTL states when a value becomes stale; missing distinguishes no history, expired, suppressed and source failure. Online lookup returns value, cutoff/version and default reason under a latency/freshness contract.

Historical retrieval selects only window values effective and available by each prediction cutoff. Sampled serving logs bind entity/request, model/feature version, value, feature cutoff/availability and default under privacy controls. Reconstruct the same requests offline and compare exact counts plus reason/time/version, not only distributions. Reconcile offline newest eligible state with online per key at a common source boundary.

For backfill, pin source range, definition and target generation; derive the forward influence interval of each changed purchase; isolate workload, canary keys/periods, compare old/new, publish offline history immutably, and update online only when the recomputed semantic version is newer and still current. Preserve correction and rejection receipts.

### Answer 5

Inventory model-to-dataset-to-feature/label/source lineage from registries, orchestration, object metadata, code, logs and owners. Freeze deployment/retraining for high-impact models whose data cannot be attributed, while maintaining bounded critical service. Prioritize sensitive/protected data, regulated decisions, direct target/future leakage, cross-split identity leakage, known online/offline divergence, mutable overwritten evidence, deletion/consent risk, and high-volume serving features.

Create canonical feature IDs with entity, type/unit, source, effective/availability times, window/TTL, missing/default, owner, policy, definition version and consumers; resolve duplicate names through semantic comparison rather than merging blindly. Version label contracts with horizon/maturity/censoring/intervention. Reconstruct example populations and grouped temporal splits; move fitted preprocessing inside training. Publish immutable datasets with source/code/runtime/definition/split/policy identities, manifests, checksums, statistics and model references.

Choose a shared transform representation or build conformance fixtures for Python/Java. Add historical point-in-time tests, availability/backfill sentinels, cutoff/TTL ties, label maturity, split group/duplicate disjointness, per-slice schema/distribution/coverage, and independent sample recomputation. Log a protected sample of actual served features and compare with offline reconstruction; add online version guards and common-boundary reconciliation. Tombstone deletions through history, online values, datasets and governed model handling.

Completion evidence includes an owner and nonambiguous definition for every active feature/label; every production model resolving one immutable verified dataset; zero unexplained split identity/near-duplicate intersections; all fitted artifacts train-only; point-in-time and maturity tests passing; measured offline/online exact-or-tolerance match by feature/slice; bounded feature freshness/missingness; manifests and checksums verified; source-to-model lineage coverage; deletion exercises; old transforms/features retired with no active consumers; and time-bounded owned exceptions for anything unresolved. Model accuracy alone closes none of these controls.
