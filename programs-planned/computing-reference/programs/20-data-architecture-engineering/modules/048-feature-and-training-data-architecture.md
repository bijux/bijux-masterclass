---
module_id: DARCH-048
program: Data Architecture Engineering
level: 1
module_number: 48
title: Feature and Training Data Architecture
status: complete
last_verified: 2026-09-03
---

# Feature and Training Data Architecture

## One-Page Review

### Governing question

How should an organization architect features and training data so every model decision is grounded in temporally valid, reproducible, protected, and operable data products across experimentation, training, batch scoring, and online inference rather than trusting a feature-store label or a successful pipeline run?

### Essential definitions

- A **prediction decision** is the named use of a model output for an entity, actor, action, time, consequence, and fallback.
- A **feature** is a versioned, governed computation or observation used as a model input under declared entity, time, source, transformation, and serving semantics.
- A **label** is a versioned target observation with a horizon, maturity, attribution, correction, and policy contract.
- An **example** binds an entity and prediction cutoff to historically eligible feature values, a label state, population rules, and provenance.
- A **feature definition** declares semantic identity, source authority, keys, clocks, transformation, type, defaults, freshness, policy, owner, and compatibility.
- A **feature value history** retains time-versioned values needed to reconstruct what was knowable for past decisions.
- An **offline store** supports historical scans, point-in-time retrieval, correction, comparison, and training-dataset construction.
- An **online store** serves bounded, low-latency feature state for current inference under freshness and fallback contracts.
- **materialization** projects feature values from authoritative computation into a serving store with position, version, and reconciliation evidence.
- **point-in-time correctness** means an example uses only facts permitted and available at its prediction cutoff.
- **training-serving skew** is a relevant difference between the feature semantics, values, transformations, defaults, or populations used for training and inference.
- A **dataset manifest** gives a training-data generation immutable identity by binding sources, definitions, code, policy, splits, statistics, checksums, and lineage.

### Central model, mechanism, or theorem

Represent feature and training data architecture as:

`F = (decisions, entities, facts, features, labels, time, transformations, stores, datasets, retrieval, metadata, protection, service, ownership, evidence, lifecycle)`

For every model release, bind the prediction workflow, entity and cutoff semantics, feature and label definitions, source snapshots or positions, transformation artifacts, training-dataset generation, split policy, online materialization boundary, serving contract, and lineage. Historical retrieval must constrain both when a fact applies and when the organization could have known it. Offline and online systems may differ physically, but their observable feature contract must be shared or empirically shown equivalent.

### Critical invariants

- Every model use has an accountable decision, population, prediction instant, useful deadline, harm analysis, and non-model fallback.
- Feature and label identities bind meaning, entity, source authority, time, transformation, version, purpose, owner, and retirement.
- Event or effective time, availability time, ingestion time, materialization time, request time, and decision time remain distinct.
- Historical retrieval excludes future-effective and future-known values, post-decision actions, and immature labels.
- Offline and online paths share definitions or prove equivalence for keys, windows, precision, defaults, missingness, ordering, and fitted artifacts.
- Training datasets are immutable generations whose manifests bind populations, sources, code, policy, splits, content, validation, and lineage.
- Source corrections, consent changes, identity changes, deletions, and definition changes propagate through affected datasets, stores, models, and evidence.
- Capacity, freshness, partial lookup, timeout, online-store loss, replay, and backfill have bounded behavior and tested recovery.
- Protection follows raw facts, feature values, registries, training shards, statistics, serving logs, models, exports, and metadata.
- Retirement accounts for feature consumers, active models, datasets, online state, histories, jobs, notebooks, monitors, credentials, and retained evidence.

### Common failures

Common failures are starting with a feature store rather than a decision; using mutable natural identifiers as entity keys; joining by event time while ignoring knowledge availability; using today’s corrected history to evaluate yesterday’s decision; treating missing labels as negatives; leaking post-action outcomes into features; random-splitting related entities; fitting preprocessing on all splits; implementing offline and online transformations separately; using different defaults or time windows; writing older feature values over newer online state; treating registry metadata as executable truth; overwriting training datasets; training from mutable paths; recording a file hash without semantic lineage; monitoring average drift while missing harmed cohorts; logging protected feature vectors without purpose; retrying failed materialization without version guards; coupling every model to one universal feature platform; retaining features after purpose expires; and retiring definitions while active models still request them.

### Compact example

A retention model scores customer A at cutoff day 10. The feature history contains value 10, effective day 5 and available day 6, plus a correction to value 99, effective day 8 but available day 15. An event-time-only join leaks value 99 into training. A bitemporal point-in-time contract selects 10 because it was the latest eligible knowledge at day 10. The dataset manifest records the cutoff, source snapshot, feature definition, label maturity, split, transform artifact, code, policy, and content digest; online inference uses the same feature meaning and reports its value time and freshness.

### Connections

[DARCH-017](017-event-schemas-and-information-models.md), [DARCH-018](018-temporal-and-historical-modeling.md), [DARCH-043](043-lakehouse-architecture.md), [DARCH-045](045-semantic-and-metrics-layers.md), [DARCH-046](046-operational-data-stores.md), and [DARCH-047](047-streaming-analytics-architecture.md) establish semantic, temporal, analytical, operational, and streaming boundaries. Data Engineering [DE-095](../../19-data-engineering/modules/095-feature-and-training-dataset-pipelines.md) owns detailed dataset-pipeline implementation. This module defines architecture and prepares [DARCH-049](../ROADMAP.md) on self-service analytics boundaries.

## Governing Question

Feature platforms often begin as a response to duplicated SQL or slow online lookup. Those are real problems, but neither identifies which decisions deserve shared features, which historical knowledge is valid, which labels are mature, which consumers can tolerate stale or partial values, or which controls apply to derived data.

The governing question is therefore not “which feature store should we deploy?” It is which architecture makes model inputs attributable, temporally correct, reproducible, consistent enough across training and serving, protected, operable, economically justified, and removable across their full lifecycle.

## Why This Matters

Feast's [Architecture Overview](https://docs.feast.dev/getting-started/architecture/overview) separates sources, transformations, registry, online and offline stores, materialization, and retrieval. Its [Feature View](https://docs.feast.dev/getting-started/concepts/feature-view) documentation describes logical feature groups used in historical and online settings. These are useful component mechanisms; selecting them does not prove that feature meaning, historical joins, labels, splits, policy, or decisions are correct.

TensorFlow's [Data Validation](https://www.tensorflow.org/tfx/data_validation/get_started) documentation covers statistics, schema anomalies, drift, and training-serving skew. The [Transform component](https://www.tensorflow.org/tfx/guide/transform) describes reusable transformation graphs and fitted statistics. [ML Metadata](https://www.tensorflow.org/tfx/guide/mlmd) models artifacts, executions, events, and contexts for lineage. A complete architecture relates those mechanisms to source authority, immutable releases, serving behavior, and accountable outcomes.

The [OpenLineage object model](https://openlineage.io/docs/next/spec/object-model/) distinguishes datasets, jobs, runs, events, and facets. NIST's [AI Risk Management Framework 1.0](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10) addresses trustworthy and responsible AI risk management. NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) frames trustworthy secure systems across the lifecycle. Feature and training data are system elements with operational and societal consequences, not disposable inputs to an isolated algorithm.

## Prerequisites and Retrieval

You should understand source systems, data products, entities, schemas, effective and transaction time, batch and stream processing, materialized views, APIs, data quality, lineage, access control, model training, inference, monitoring, and recovery.

Retrieve prediction decision, entity, cutoff, feature, label, example, population, observation window, outcome horizon, maturity, effective time, availability time, feature view, registry, offline store, online store, materialization, point-in-time join, training-serving skew, fitted transform, split, dataset generation, manifest, lineage, drift, and deletion.

As a retrieval test, inspect “customer risk score.” Ask which customer identity, decision, request instant, feature set and versions, source authorities, time semantics, label horizon, historical population, transformations, online freshness, missing behavior, policy, owner, model releases, and retirement condition apply. A model name and a table path are not a data architecture.

## Learning Objectives

After completing this module, you should be able to:

1. frame feature and training data from accountable prediction decisions, populations, consequences, and alternatives;
2. define feature, label, example, dataset, registry, store, materialization, and serving contracts;
3. separate effective, availability, ingestion, materialization, request, and decision time;
4. design point-in-time retrieval, label maturity, split independence, and reproducible dataset generations;
5. align offline and online transformations, defaults, ordering, fitted artifacts, and freshness;
6. choose centralized, federated, embedded, offline-only, online, batch, streaming, and hybrid topologies;
7. establish lineage across sources, transformations, datasets, models, deployments, decisions, and corrections;
8. propagate purpose, consent, minimization, authorization, retention, deletion, licensing, and derived sensitivity;
9. set service objectives, capacity boundaries, recovery, migration, ownership, and verified retirement; and
10. evaluate feature architecture by decision value, correctness, reproducibility, reliability, protection, cost, and removable complexity.

## Core Exposition

**Start with the prediction workflow.** Name the entity, trigger, prediction instant, actor, model output, downstream action, useful deadline, error consequence, abstention, appeal, and fallback.

The data contract inherits these boundaries. A batch propensity ranking, an online fraud recommendation, and an offline capacity forecast should not share a topology merely because all use features.

**Define the population.** State which entities can be scored, why an example exists, which exposures or eligibility rules apply, and which entities are excluded.

Training on every known customer while serving only active sessions changes the population. Periodic examples overrepresent long-lived entities; event-triggered examples describe another estimand.

**Separate facts, features, and decisions.** Facts describe source-domain occurrences or states. Features transform facts for a prediction contract. Models combine features. Decisions interpret model outputs under policy.

Do not let a feature platform become an alternative system of record. Retain links to authoritative facts and make derived ownership explicit.

**Give entities stable scoped identity.** Define tenant, entity type, key authority, merge and split behavior, aliases, history, and collision rules.

Email addresses, device IDs, and mutable account numbers can change owners or connect people. Identity resolution is a governed dependency, not a convenient join.

**Treat each feature as a product contract.** Record name and stable ID, semantic version, description, entity, grain, type, unit, valid domain, source, transformation, time, window, freshness, default, missing reasons, policy, owner, cost, and compatibility.

The feature name `spend_30d` is incomplete without currency, qualifying transactions, refunds, event time, timezone, window endpoints, late corrections, and serving behavior.

**Distinguish definitions from values.** The registry holds or references feature meaning, ownership, schemas, dependencies, versions, and discovery metadata. Stores hold feature values or histories.

A valid registry entry does not prove that a computation ran, that its inputs were complete, or that an online value matches the declared definition.

**Assign source authority.** Identify which system owns each fact, how corrections and deletions appear, which positions or snapshots bound extraction, and how disputes resolve.

Copies may provide performance but must not silently become authorities. A training rebuild needs the exact historical source boundary or a declared restatement.

**Model multiple clocks.** Effective or event time says when a fact applies. Availability time says when it became knowable. Ingestion and processing time support operations. Materialization time records projection. Request and decision time describe consumption.

Using one `timestamp` field for all purposes invites leakage, stale inference, and irreproducible history.

**Design historical knowledge explicitly.** For each prediction cutoff, select feature values that both apply by the cutoff and were available by it under lookback, correction, and policy rules.

Today's corrected understanding of last month is not necessarily what last month's system knew. Decide whether an analysis needs historically available knowledge, corrected retrospective truth, or both as distinct products.

**Define label architecture.** Labels need source authority, target meaning, horizon, attribution, observation opportunity, maturity delay, correction, retraction, censoring, and unknown states.

No observed event is not a negative until the outcome window and source delay close. Model-influenced actions can alter labels and require exposure or policy context.

**Protect the decision boundary from leakage.** Exclude outcome facts, post-decision actions, future reference data, later corrections, and evaluation feedback from features unless the intended prediction could observe them.

Leakage is architectural when shared datasets, identity services, or reference tables expose forbidden knowledge across many pipelines.

**Define examples as first-class artifacts.** Each example binds entity, cutoff, decision context, feature-definition set, label state, population reason, split, and provenance.

An example spine makes missing features visible and preserves population accounting. Inner joins can silently remove the hardest cases.

**Design split independence around deployment.** Choose temporal, entity, household, session, location, campaign, document-family, or other grouping constraints that reflect future use.

Row-level randomness is insufficient when information crosses related entities or time. Fit preprocessing only from training evidence, not evaluation outcomes.

**Version fitted transformations.** Means, quantiles, vocabularies, encoders, embeddings, imputers, and selected features are data-derived artifacts.

Bind them to the training split and deploy the same artifacts where inference needs them. Recomputing current statistics changes the feature space without changing model code.

**Choose an offline history boundary.** Historical storage must support required retention, point-in-time retrieval, corrections, large scans, partitions, snapshots, access, and reproducible references.

It may be a warehouse, lakehouse, or specialized store. The important property is the contract and evidence, not the label “offline feature store.”

**Choose an online serving boundary.** Online storage needs keys, value versions, freshness, TTL, partial-read semantics, latency, concurrency, availability, regional behavior, and access control.

Many online stores keep only current values. Historical reconstruction therefore depends on another governed system.

**Design materialization as controlled projection.** Bind source snapshot or positions, definition and code version, entity-value sequence, target store, job run, validation, and reconciliation.

Use per-entity version guards so delayed older values do not overwrite newer state. Define precedence when batch and streaming writers meet.

**Choose pull, push, or hybrid computation.** Pull retrieval computes or joins on demand from sources; push computation precomputes and writes values; hybrid systems combine stored and request-time features.

Pull can reduce duplication but increase latency and source coupling. Push lowers lookup cost but adds staleness, materialization, storage, and replay responsibilities.

**Share transformations or prove equivalence.** Prefer one executable definition or generated realizations for historical, batch-scoring, streaming, and request paths.

When engines differ, compare golden cases and sampled production requests across types, precision, timezones, ordering, windows, defaults, missing reasons, and tolerances.

**Define online retrieval semantics.** State batch key behavior, absent entity, missing feature, expired value, partial groups, timeout, fallback, version response, freshness evidence, and consistency across requested features.

A zero may be a valid value, a default, a redaction, or a failure. Preserve the reason or models learn infrastructure behavior.

**Bind models to feature contracts.** A model release declares exact feature IDs and compatible versions, transform artifacts, input schema, expected defaults, freshness limits, serving interface, and rollback behavior.

Do not let deployed code resolve an unbounded “latest” feature definition. Compatibility is an explicit reviewed relationship.

**Make training datasets immutable releases.** A generation binds its example population, time interval, source snapshots or positions, identity map, feature and label definitions, transformations, splits, exclusions, policy, code, environment, schema, statistics, and content integrity.

Publish atomically after validation. A mutable folder of files is not a reproducible training product.

**Use manifests as admission evidence.** Trainers accept a dataset by stable manifest identity, verify checksums and schema, record the exact reference, and reject incomplete or superseded inputs under policy.

A checksum proves only the bytes examined. Semantic identity also requires definitions, source boundaries, policies, and construction context.

**Unify technical and decision lineage.** Connect authoritative facts to feature computations, dataset generations, experiments, models, deployments, prediction requests, actions, outcomes, corrections, and deletion obligations.

Lineage metadata must use stable identifiers and remain queryable during incidents. A graph with missing dynamic partitions or run versions can imply false completeness.

**Classify metadata as governed data.** Registries and lineage expose feature names, schemas, cohorts, model purpose, source locations, ownership, and possibly protected relationships.

Apply authorization, minimization, integrity, retention, and audit to metadata rather than making the entire catalog universally visible.

**Validate source and feature semantics.** Check schema, units, ranges, cardinality, grain, identity coverage, time order, completeness, missing reasons, duplicate and correction behavior, and protected slices.

Statistical similarity cannot prove semantic correctness. A stable distribution of values in the wrong unit remains wrong.

**Validate temporal correctness.** Test exact cutoff, availability boundary, tie-breaking, TTL edge, late correction, identity change, future clock, daylight-saving transition, label maturity, and reference-data version.

Use independent reconstruction for representative examples. Point-in-time SQL that executes successfully can still leak knowledge.

**Monitor offline-online equivalence.** Log a minimized, authorized sample or safe digest of served inputs with request cutoff, feature and model versions, value times, missing reasons, and outcome join identity.

Reconstruct those inputs offline at the same boundary. Compare values and reasons, not just aggregate distributions.

**Separate drift from skew.** Drift is change in data or relationships over time. Training-serving skew is a difference between training and inference paths or populations.

Both can matter, but they have different diagnoses and owners. Thresholds need decision and slice context.

**Set freshness at the feature boundary.** Broker lag or materialization success does not prove a requested value is useful.

Measure source occurrence to feature availability, online visible time, request observation, and decision use for named features and cohorts.

**Define degraded inference.** Specify which features are required, optional, substitutable, or stale-tolerant; when the model abstains; which fallback applies; and how the decision records degradation.

Silent defaults can preserve uptime while destroying model validity. Partial inference is a product policy, not only an availability tactic.

**Isolate workloads.** Historical joins, backfills, exploratory scans, online materialization, training, batch scoring, and low-latency lookup compete differently for compute, storage, network, and source capacity.

Use quotas, priorities, pools, admission, and source budgets so one experiment or rebuild cannot impair production inference.

**Design recovery across stores and metadata.** Back up or reconstruct registries, definitions, offline histories, online state, manifests, transformation artifacts, lineage, and policy decisions.

Recovery order matters. Rebuilt online values must use compatible definitions and source boundaries before model traffic resumes.

**Reconcile, do not merely replay.** After failure or backfill, compare keys, versions, event and availability times, values or digests, missing reasons, counts, source positions, and consumer observations.

Replay with present-day code or reference data can create a different product. Isolate outputs, compare, approve, and cut over.

**Propagate corrections and deletions.** A changed fact can affect feature histories, windows, examples, datasets, fitted artifacts, models, online values, logs, caches, and decisions.

Use lineage to identify scope, but pair it with policy. Deletion, suppression, retraining, model retirement, and retained legal evidence require qualified decisions.

**Design for derived sensitivity.** Aggregates, embeddings, risk features, missingness, and identity relationships can reveal sensitive attributes even when raw fields are absent.

Classify by inference and consequence, not column name alone. Protect feature discovery, statistics, values, training exports, and serving logs.

**Control experimentation.** Sandboxes use approved sources, bounded samples, isolated identities, expiry, cost budgets, and promotion gates.

Notebook success does not authorize production reuse. Promotion creates owned definitions, tests, lineage, protection, service objectives, and retirement obligations.

**Choose federation deliberately.** A central platform can standardize retrieval and evidence; domain teams retain source meaning and decision context. A federated model shares contracts while distributing feature ownership.

Centralization without domain authority creates a metadata bottleneck. Federation without interoperability creates duplicated, incompatible features.

**Limit feature reuse.** Reuse is valid only when entity, meaning, time, source, purpose, population, policy, and serving semantics fit the new decision.

A fraud signal approved for security may not be lawful or appropriate for marketing. Technical discoverability is not permission.

**Plan compatibility and migration.** Classify additive, semantic, policy, source, key, time, transform, and serving changes. Run old and new definitions against common inputs and named consumers.

Use shadow materialization, dual retrieval with bounded comparison, cohort migration, model compatibility declarations, rollback, and expiry.

**Measure architecture value.** Track decision improvement, time to trustworthy dataset, feature reuse with valid context, reproducibility, incident reduction, skew and leakage findings, serving performance, deletion completion, cost, and retired duplication.

Counting registered features rewards accumulation. Measure reliable decisions and removable complexity.

**Retire the whole dependency.** Inventory definitions, source extracts, histories, online values, datasets, models, endpoints, jobs, notebooks, monitors, logs, credentials, and downstream copies.

Stop new use, migrate or expire consumers, preserve required evidence, delete prohibited artifacts, revoke access, validate no backfill resurrects data, and record closure.

## Definitions and Notation

Represent the architecture as $F=(D,E,A,T,G,H,O,M,L,P,Q,R)$, where $D$ is decisions, $E$ entities, $A$ authoritative facts, $T$ temporal semantics, $G$ feature and label definitions, $H$ historical and online stores, $O$ orchestration and materialization, $M$ manifests and metadata, $L$ lineage, $P$ protection, $Q$ service qualities, and $R$ ownership and lifecycle.

For example $e=(k,c)$ with scoped entity key $k$ and prediction cutoff $c$, let feature record $r$ have effective time $t_e(r)$, availability time $t_a(r)$, source sequence $s(r)$, value $x(r)$, and definition version $v(r)$. Given lookback $B_f$, eligible records satisfy

$$
k(r)=k,\quad c-B_f<t_e(r)\le c,\quad t_a(r)\le c,\quad Policy(r,e)=allowed.
$$

The selected value is the deterministic maximum over declared effective time, availability time, and source sequence among eligible records. Absence produces a typed missing reason rather than an unexplained zero.

Let dataset generation identity be

$$
G=id(Population,Cutoffs,Features,Labels,Sources,Transforms,Splits,Code,Policy).
$$

Content checksums and statistics describe artifacts belonging to $G$; they do not replace its semantic and provenance bindings.

Define `FitFeature(F,d,t)` as a review predicate requiring a justified decision, authoritative and temporally valid inputs, governed labels and populations, reproducible datasets, compatible offline and online semantics, effective protection, capacity and recovery evidence, accountable ownership, viable alternatives, and lifecycle controls at time $t$.

## Mechanisms, Invariants, or Proof Structure

Use ten architecture gates.

**1. Decision gate.** Name the entity, prediction event, actor, action, consequence, population, deadline, fallback, value, and accountable approver.

**2. Authority gate.** Define feature and label meaning, source authority, identity, grain, corrections, quality, and ownership.

**3. Time gate.** Separate effective and availability time, cutoffs, horizons, maturity, windows, TTL, corrections, and restatements.

**4. Construction gate.** Bind examples, point-in-time retrieval, splits, fitted transformations, immutable generations, manifests, and validation.

**5. Serving gate.** Define offline and online stores, materialization, ordering, retrieval, freshness, missingness, consistency, and degraded inference.

**6. Lineage gate.** Connect sources, executions, artifacts, definitions, datasets, models, deployments, decisions, corrections, and deletion scope.

**7. Protection gate.** Apply purpose, authorization, minimization, derived sensitivity, retention, deletion, licensing, integrity, and audit.

**8. Service gate.** Bound capacity, latency, freshness, skew, backfills, failures, recovery, reconciliation, and incident response.

**9. Ownership gate.** Assign domain, feature, label, platform, model, consumer, protection, operations, and retirement decisions.

**10. Lifecycle gate.** Compare alternatives, manage compatibility and migration, measure outcomes and cost, and verify retirement.

Passing a gate means evidence supports a scoped claim. It does not mean a vendor component or platform is trustworthy by designation.

### Executable evidence

The executable example demonstrates bitemporal eligibility at one prediction cutoff.

<!-- bijux-verify: {"id":"feature-point-in-time-contract","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"entity=customer-A\ncutoff_day=10\nselected_effective_day=5\nselected_available_day=6\nselected_value=10\nexcluded_future_knowledge=99\ndataset_generation=retention-train-2026-09\nonline_contract=feature-v3\n","stderr":""}} -->
```python
entity = "customer-A"
cutoff_day = 10
records = [
    {"effective_day": 5, "available_day": 6, "sequence": 1, "value": 10},
    {"effective_day": 8, "available_day": 15, "sequence": 2, "value": 99},
]

eligible = [
    record
    for record in records
    if record["effective_day"] <= cutoff_day
    and record["available_day"] <= cutoff_day
]
selected = max(
    eligible,
    key=lambda record: (
        record["effective_day"],
        record["available_day"],
        record["sequence"],
    ),
)
excluded = next(record for record in records if record not in eligible)

print(f"entity={entity}")
print(f"cutoff_day={cutoff_day}")
print(f"selected_effective_day={selected['effective_day']}")
print(f"selected_available_day={selected['available_day']}")
print(f"selected_value={selected['value']}")
print(f"excluded_future_knowledge={excluded['value']}")
print("dataset_generation=retention-train-2026-09")
print("online_contract=feature-v3")
```

The result proves only the declared filtering and selection for two in-memory records. It does not prove source authority, production point-in-time joins, label correctness, split independence, offline-online equivalence, dataset reproducibility, protection, serving reliability, model fitness, or decision safety.

## Alternatives and Trade-Offs

**No shared feature platform.** Teams can own transformations within model products when reuse is low and decisions differ. This reduces central infrastructure while increasing duplication and local assurance work.

**Offline-only architecture.** Batch training and scoring can use warehouse or lakehouse products without an online store. This is often simpler when decisions tolerate scheduled releases.

**Centralized feature platform.** Shared registry, retrieval, stores, and controls can improve interoperability and evidence. It can also become a bottleneck, concentrate failure, and erase domain context.

**Federated feature products.** Domains own meaning and computation under shared contracts and platform services. This improves authority alignment but requires compatibility, discovery, and conformance governance.

**Compute on read.** Pulling current facts and transforming per request reduces materialized copies. It raises latency, source coupling, consistency, and capacity concerns.

**Precompute on write.** Push materialization enables fast lookup. It creates staleness, ordering, replay, storage, reconciliation, and deletion obligations.

**Shared code versus equivalent implementations.** One transform can reduce skew but may constrain engines. Separate optimized implementations need stronger tests and runtime comparison.

**Corrected retrospective truth versus historical knowledge.** Restated history supports current analysis; historically available knowledge supports honest evaluation. Mature architectures publish both when both questions matter.

**Broad reuse versus decision-specific features.** Reuse lowers duplication when semantics and policy align. Narrow features can preserve clearer purpose, time, and ownership.

**Build versus buy.** Managed and open-source systems can supply components. Architecture still owns contracts, integration, evidence, risk, migration, cost, and exit.

Choose by decision deadlines, populations, historical depth, correction behavior, online needs, scale, regulatory duties, team capability, failure consequences, cost, and retirement burden.

## Failure Modes and Misconceptions

1. **A feature store guarantees correct features.** Components cannot supply missing semantic, temporal, label, and decision contracts.
2. **Latest means appropriate.** Current online state may be wrong for a historical cutoff or stale for a live decision.
3. **Event time prevents leakage.** Later availability and corrections can still leak future knowledge.
4. **No label means negative.** The outcome may be immature, censored, unavailable, or unobservable.
5. **Random rows create independent tests.** Related entities, time windows, identities, and near duplicates can cross splits.
6. **A registry is the source of truth.** It describes definitions; sources own facts and executions produce values.
7. **One feature name has one meaning.** Entity, population, purpose, time, units, defaults, and policy qualify meaning.
8. **Shared SQL prevents skew.** Engines, states, fitted artifacts, precision, windows, ordering, and defaults can differ.
9. **Online success means fresh data.** A low-latency lookup can return an old or partial value.
10. **Defaulting preserves correctness.** Silent defaults can change model behavior and encode outages or cohort bias.
11. **A dataset hash proves reproducibility.** It omits source, code, policy, definitions, population, and construction meaning.
12. **Lineage events prove complete lineage.** Missing emitters, partitions, versions, or identifiers leave false gaps or joins.
13. **Aggregate drift protects every cohort.** Harm and missingness can concentrate in small populations.
14. **Replay restores the same dataset.** Inputs, code, reference data, identity, policy, or corrections may have changed.
15. **Hashing entity IDs anonymizes features.** Linkable behavior and derived signals can remain identifying and sensitive.
16. **Centralizing every feature maximizes reuse.** It can maximize coupling, unclear ownership, and blast radius.
17. **Unused feature definitions are harmless.** They retain data, permissions, cost, and resurrection paths.

## Worked Examples

### Example 1

A weekly credit review needs batch scores before Monday morning. An offline governed dataset and batch-scoring release meet the deadline, so the team rejects an online feature store. **Conclusion:** architecture follows decision latency, not fashion.

### Example 2

A churn cutoff at day 10 sees value 10 available on day 6; a value 99 effective on day 8 arrives on day 15. Historical evaluation selects 10 while a corrected retrospective product selects 99 under another identity. **Conclusion:** historical knowledge and current retrospective truth are distinct products.

### Example 3

A 30-day default label is built 12 days after prediction. The architecture marks it immature rather than negative and delays the dataset release until the horizon plus source allowance closes. **Conclusion:** label maturity is a release boundary.

### Example 4

Offline code treats a missing merchant category as `UNKNOWN`; online code emits integer zero. Golden cases and sampled serving comparison expose the difference before model promotion. **Conclusion:** missing and default semantics belong in compatibility tests.

### Example 5

A streaming writer delivers an older account aggregate after a newer batch materialization. Per-entity effective-time and sequence guards reject the stale overwrite and reconciliation records the conflict. **Conclusion:** multiple writers need declared precedence.

### Example 6

A training manifest records source snapshots, example and label definitions, split rule, fitted vocabulary, code image, schema, counts, checksums, policy, and lineage. A retry resolves the same generation rather than scanning a mutable directory. **Conclusion:** reproducibility is an admission contract.

### Example 7

An online store is unavailable. Fraud scoring may use one explicitly stale-tolerant feature but must abstain when device-risk evidence is missing; the decision log records degradation. **Conclusion:** partial lookup policy is model and product behavior.

### Example 8

A feature derived from medical-support interactions is discoverable to a marketing team. Purpose and sensitivity policy deny reuse even though the entity key and type are compatible. **Conclusion:** catalog visibility is not authorization.

### Example 9

A corrected identity merge affects historical features, two datasets, one fitted encoder, three models, serving caches, and audit samples. Lineage scopes the inventory; accountable owners choose rebuild, suppression, or retirement per consequence. **Conclusion:** lineage supports decisions but does not make them.

### Example 10

A feature is absent from new models but remains in an old endpoint, notebooks, online materialization, backfill code, and a monitoring job. Retirement waits until every dependency is migrated or expired and resurrection tests pass. **Conclusion:** registry deletion alone is not retirement.

## Cross-Program Connections

- **Data engineering:** point-in-time joins, label construction, immutable manifests, split controls, materialization, reconciliation, and deletion implement the contracts.
- **Machine learning:** feature utility, generalization, calibration, fairness, drift, evaluation, and model behavior depend on trustworthy data boundaries.
- **Platform engineering:** registries, stores, orchestration, tenancy, quotas, deployment, telemetry, and recovery provide reusable capabilities.
- **API and service engineering:** online retrieval and prediction interfaces require versioning, idempotency, freshness, partial response, authorization, and compatibility.
- **Security and privacy:** purpose, minimization, access, derived sensitivity, integrity, retention, deletion, audit, and supply-chain risk follow artifacts and metadata.
- **Software delivery:** definitions, transformations, schemas, policy, datasets, and models move through reviewed changes, tests, releases, rollback, and retirement.
- **Reliability engineering:** capacity isolation, service objectives, degraded modes, recovery, reconciliation, incident response, and error budgets bound operations.
- **Systems engineering:** stakeholder outcomes, lifecycle assurance, hazards, ownership, evidence, alternatives, and decommissioning keep the architecture accountable.
- **Economics and decision science:** timeliness value, false positives, sampling, feedback, uncertainty, feature cost, shared-platform externalities, and exit cost guide choices.

## References

1. Feast Project, *Architecture Overview*. <https://docs.feast.dev/getting-started/architecture/overview>
2. Feast Project, *Feature View*. <https://docs.feast.dev/getting-started/concepts/feature-view>
3. TensorFlow, *Get Started with TensorFlow Data Validation*. <https://www.tensorflow.org/tfx/data_validation/get_started>
4. TensorFlow, *The Transform TFX Pipeline Component*. <https://www.tensorflow.org/tfx/guide/transform>
5. TensorFlow, *ML Metadata*. <https://www.tensorflow.org/tfx/guide/mlmd>
6. OpenLineage, *Object Model*. <https://openlineage.io/docs/next/spec/object-model/>
7. NIST, *Artificial Intelligence Risk Management Framework 1.0*. <https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10>
8. NIST, *SP 800-160 Volume 1 Revision 1: Engineering Trustworthy Secure Systems*. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>

## Exercises

### Exercise 1

Design feature and training data architecture for an online payment-fraud recommendation. Define decision, entity, features, labels, clocks, offline and online stores, materialization, serving, protection, service, ownership, and lifecycle.

### Exercise 2

A historical evaluation joins features only by effective time. A correction effective before cutoff was not available until afterward, and chargeback labels mature 60 days later. Diagnose the errors and design two legitimate historical products.

### Exercise 3

Two teams compute the same merchant-risk feature: a warehouse batch path for training and a stream path for online inference. Define the evidence required to claim semantic compatibility and a safe migration to a shared definition.

### Exercise 4

An online store and metadata registry are lost while offline history remains. Describe recovery without serving incompatible or falsely fresh values.

### Exercise 5

Compare no shared platform, offline-only, centralized feature platform, and federated feature products for batch credit ranking, online fraud scoring, demand forecasting, and a sensitive health-support model. Recommend boundaries rather than one universal topology.

## Answers to the Exercises

### Answer 1

Define the decision as recommending review or additional authentication, not automatically rejecting payment unless separately authorized. The entity is a scoped payment instrument or transaction with stable identity and request cutoff. Feature contracts specify authoritative payment, device, merchant, account, and behavior facts; event and availability time; windows; types and units; missing reasons; fitted artifacts; purpose; owner; and compatible model versions. Labels define confirmed fraud, exposure, adjudication, maturity, correction, and unknown outcomes.

Keep immutable historical feature values and source boundaries offline for point-in-time datasets. Materialize bounded current values online using per-entity versions, batch-stream precedence, validation, and reconciliation. Retrieval exposes definition version, value time, freshness, and degradation. Protect raw and derived risk, registry metadata, shards, logs, models, and dead letters. Isolate training, replay, and online capacity; define abstention, fallback, SLOs, recovery, and incident roles. Bind datasets and models through manifests and lineage. Assign domain, fraud, feature, label, platform, model, operations, protection, and decision owners; review outcome value, bias, cost, corrections, migration, and verified retirement.

### Answer 2

The join leaks future knowledge because effective time alone does not show when a correction became available. Historical evaluation must require both effective time and availability time no later than the prediction cutoff, plus deterministic tie-breaking, lookback, identity, and policy. Labels observed before the 60-day horizon plus source delay are immature, not negative; correction and censoring remain explicit.

Publish a historically available dataset that reconstructs what the decision system could know at each cutoff and is suitable for honest backtesting. Publish a corrected retrospective dataset that applies later corrections under a new generation and supports present-day analysis or restatement. Give them distinct identities, purposes, manifests, statistics, and consumer restrictions. Never silently substitute one for the other or compare model metrics without noting the knowledge boundary.

### Answer 3

Define one contract for entity and key normalization, source authority, effective and availability time, aggregation window and endpoints, late events, corrections, ordering, type, precision, null and default reasons, fitted artifacts, TTL, policy, and version compatibility. Use golden cases covering boundary time, duplicates, gaps, out-of-order facts, deleted inputs, empty windows, timezone transitions, overflow, and missing sources. Compare historical recomputation with minimized samples of served values at identical cutoffs, versions, and source positions; publish mismatch rates by reason and cohort.

Create the shared executable or typed definition, run old and new paths in isolated namespaces, backfill common periods with pinned inputs, shadow materialization, and compare values, freshness, cost, and decision outcomes. Declare model compatibility, migrate consumers by cohort, retain rollback, reconcile online keys and versions, and expire old writers only after no active datasets, models, backfills, or notebooks depend on them.

### Answer 4

Stop or degrade inference according to feature criticality; do not label retained cache values fresh. Inventory model-to-feature contracts, definition versions, registry backup, offline snapshots and histories, source positions, materialization runs, online keys and versions, fitted artifacts, policies, credentials, and consumer traffic. Restore the registry and lineage from a trusted backup or reconstruct definitions through reviewed code releases, then validate identity, schema, ownership, and compatibility before use.

Rebuild online state in an isolated target from a declared offline cutoff or authoritative streams using compatible definitions, ordering, TTL, and per-entity version guards. Compare keys, values or digests, times, versions, missing reasons, counts, protected access, and representative model inputs. Record uncertainty where history is insufficient. Cut over only after reconciliation, load testing, protection checks, and accountable approval; establish new materialization lineage, rotate credentials if needed, and exercise the repaired recovery design.

### Answer 5

Batch credit ranking can use an offline governed warehouse or lakehouse product when its scheduled deadline is met; online infrastructure adds little value. Online fraud scoring justifies low-latency materialized features, explicit stale and partial behavior, strong identity, and tight reconciliation. Demand forecasting often favors immutable offline datasets and batch scoring, perhaps with a small streaming supplement for shocks. The sensitive health-support model needs purpose-limited domain ownership, restrictive discovery, qualified review, deletion and retention controls, and may reject broad feature reuse even if platform components are shared.

No shared platform fits low reuse and autonomous model products but duplicates assurance. Offline-only is simplest for scheduled decisions. A central platform can provide registries, retrieval, stores, lineage, controls, and operations when many compatible consumers exist, but concentrates coupling and failure. Federation keeps domain authority while using shared contracts and capabilities, at the cost of conformance work. Choose per decision deadline, temporal correctness, historical depth, reuse validity, policy, scale, recovery, skill, cost, and exit; share infrastructure without forcing one semantic or serving topology.
