---
module_id: DE-082
program: Data Engineering
level: 2
module_number: 82
title: Dataset and Column Lineage
status: complete
last_verified: 2026-09-03
---

# Dataset and Column Lineage

## One-Page Review

### Governing question

How can a data platform capture, reconcile, query, secure, and validate dataset- and column-level lineage across declared plans and actual executions, including indirect filter/join/group/order/control influence, without treating names as identities, static parsing as runtime truth, missing edges as independence, or graph reachability as proof of causality or actual impact?

### Essential definitions

- **Dataset lineage** records typed dependencies among versioned tables, topics, files, APIs, models, reports, feature sets, and other data products, usually mediated by activities/jobs/runs.
- **Column lineage** records how input fields influence output fields or output existence/order, with transformation semantics and scope.
- **Direct value lineage** means an input value is copied, transformed, combined, aggregated, masked, or otherwise contributes to an output value.
- **Indirect lineage** means an input controls which rows/groups/order/window/branch are produced without necessarily contributing its value to the output.
- A **lineage entity** is a stably namespaced dataset, field, activity/job, run, code/config/reference artifact, consumer, or version.
- A **lineage edge** is a directional dependency assertion with type, endpoints, run/version/time scope, source, collector, confidence, and evidence.
- **Declared lineage** expresses intended dependency before execution; **observed lineage** comes from actual runtime evidence; **parsed lineage** is statically extracted; **inferred lineage** is probabilistic or heuristic; **curated lineage** is asserted by an authorized human/workflow.
- A **runtime lineage graph** binds abstract jobs/datasets to concrete runs and input/output versions.
- **Transformation metadata** describes direct/indirect behavior such as identity, cast, expression, aggregate, join, filter, group, order, window, pivot, lookup, or opaque code.
- **Coverage** compares observed or supported lineage against an eligible scope of jobs, runs, datasets, fields, and transformations.
- A **lineage gap** is a known missing, unsupported, stale, inaccessible, ambiguous, or conflicting dependency region.
- A **backward slice** finds possible ancestors of a selected version/field; a **forward slice** finds possible descendants.
- **Potential impact** is graph-reachable compatible scope; **observed impact** requires runtime use and consumer evidence.
- **Row/cohort/partition lineage** narrows dependency below a dataset version but increases cost, volume, and privacy risk.
- **Lineage provenance** records who/what produced an edge, from which plan/event/artifact, with which parser/integration and time.

### Central model, mechanism, or theorem

Represent lineage for scope $t$ as a typed property graph $G_t=(V_t,E_t)$ where

$$
e=(u,v,kind,transform,run,versions,source,collector,confidence,time,scope).
$$

For output field $y$, direct inputs $D(y)$ and control inputs $C(y)$ are distinct. Complete influence is $I(y)=D(y)\cup C(y)$. In query `SUM(amount) WHERE region='EU'`, `amount` has direct value lineage and `region` has indirect filter lineage. Changing only `region` can change the aggregate, so a value-only graph is unsound for impact questions involving row membership.

### Critical invariants

- Dataset and field endpoints use stable namespace plus logical/physical identity, environment/tenant, schema and version—not display name alone.
- Activities/jobs are distinct from run instances; every observed edge binds exact run and input/output versions.
- Edge direction, type, direct/indirect semantics, source method, collector version, time/effectivity, confidence, and evidence are preserved.
- Dataset-level edges are not presented as field-level proof; field edges are not presented as row-level proof.
- Filters, joins, group keys, ordering, limits, windows, branches, references, policies, and configuration can create indirect influence.
- Declared, parsed, observed, inferred, and curated edges remain distinguishable and may coexist or conflict.
- Static parsing resolves dialect, catalog, search path, aliases, stars, views, macros/templates, CTEs, scopes, and schema versions—or marks uncertainty.
- Runtime capture records actual plan/input/output and dynamic behavior, but missing instrumentation remains a coverage gap.
- Schema evolution preserves field identity/mapping through add/drop/rename/type change and positional or star expansion.
- Logical cycles are permitted where iterative, recursive, self-updating, or periodic systems require them; runtime instances remain ordered by execution/version evidence.
- Edge ingestion is idempotent; corrections supersede or retract prior assertions without deleting provenance.
- Backward and forward traversal applies version, time, environment, field, edge-kind, confidence, and access constraints.
- Hidden nodes and edges do not leak through paths, counts, timing, autocomplete, or error messages.
- Query text, literals, predicates, field names, transformations, and access/use evidence are classified and minimized.
- Coverage measures expected versus captured jobs/runs/datasets/fields/edges and separately reports unsupported/unknown scope.
- Lineage is validated with fixtures, plan/event reconciliation, known transformations, mutations, and downstream observations.
- Potential descendants are confirmed with actual execution/read/consumer evidence before claiming observed impact.
- Offline exports, spreadsheets, notebooks, APIs, caches, reports, features, models, and decisions remain explicit terminal/gap/curated edges.

### Common failures

Common failures include joining by unqualified names; merging dev and production; omitting versions; modeling jobs and runs as one node; flattening every dependency to dataset level; recording only copied values; missing join/filter/group/order/window influence; expanding `SELECT *` against today's schema for yesterday's query; losing aliases and scope; assuming a successful parser understood dynamic SQL; calling declared edges observed; ignoring stored procedures and UDFs; treating no edge as no dependency; overwriting conflicts; collapsing cycles incorrectly; exposing restricted nodes through a visible path; storing secrets/literals from queries; measuring edge count instead of coverage; and telling every reachable consumer it was definitely affected.

### Compact example

`eligible_revenue` sums `orders.amount` only where `orders.region='EU'`. Direct value lineage maps `orders.amount → eligible_revenue`. A value-only graph omits `orders.region` because its text never appears in the aggregate value. Yet changing one row's region from `US` to `EU` changes revenue from 100 to 150 with all amounts unchanged. Correct column lineage records `orders.region` as indirect filter influence, enabling safe impact analysis for region-definition changes.

### Connections

[DE-032](032-sql-transformation-pipelines.md) supplies compiled SQL structure, [DE-041](041-directed-acyclic-graphs-and-dependencies.md) supplies dependency graphs, [DE-049](049-run-metadata-and-operational-state.md) distinguishes jobs/runs, [DE-060](060-handling-late-duplicate-and-out-of-order-events.md) supplies event/version disorder, [DE-066](066-time-travel-and-reproducible-reads.md) pins data versions, [DE-076](076-data-contracts.md) defines interfaces, [DE-078](078-data-incident-detection-and-triage.md) consumes impact evidence, [DE-079](079-root-cause-analysis-with-lineage.md) tests causal hypotheses, [DE-080](080-building-quality-gates-for-a-data-product.md) consumes dependency coverage, and [DE-081](081-technical-operational-and-business-metadata.md) provides the assertion model. DE-083 builds the catalog surface.

## Governing Question

Lineage diagrams are deceptively simple: boxes connected by arrows. Production evidence is not. One logical product can have many physical versions; one job can have thousands of runs; one SQL statement can use fields directly in expressions and indirectly in filters; one parser can misunderstand a dialect or template; one notebook can export a file outside the observed platform.

Different lineage questions need different fidelity. Discovery may need stable dataset dependencies. A schema-change review needs column and indirect-control influence. Incident analysis needs exact runtime versions. Privacy deletion may need row/cohort derivation and off-platform exports. One universal unlabeled edge cannot answer all four.

Collection sources disagree. Contracts and code declare intended dependencies, parsers extract likely relationships, runtime integrations observe executions, access logs infer use, and stewards add manual edges. Disagreement is evidence of drift or limited coverage, not a reason to keep whichever edge arrived last.

The governing requirement is a versioned, provenance-bearing, typed influence graph whose query answers state granularity, scope, confidence, coverage, authorization, and limits. Its purpose is safer discovery and decisions, not decorative completeness.

## Why This Matters

Dataset lineage accelerates discovery, change planning, incident response, governance, cost analysis, and retirement. It shows which products depend on a source, which activities produced an output, and where ownership/quality evidence should propagate.

Column lineage prevents overbroad and underbroad decisions. A renamed field may affect only three outputs, while a control field used in a filter can change every downstream aggregate without being copied. Correct semantics reduce unnecessary freezes and missed harm.

Runtime versioning makes lineage reproducible. A current catalog graph may reflect code deployed after an incident. Without run, snapshot, code/config/reference, and schema versions, investigators traverse a plausible architecture instead of the execution that produced the data.

Lineage is also a security and privacy map. It can reveal protected attributes, hidden systems, query logic, consumer behavior, and high-value paths. Broad catalog visibility can turn helpful context into reconnaissance or inference leakage.

Finally, false certainty is worse than visible uncertainty. A graph with untyped, stale, or inferred edges can automate incorrect policy, delete too little, notify the wrong consumers, or attribute cause without evidence. Coverage and provenance must be first-class output.

## Prerequisites and Retrieval

Retrieve identity: dataset/job/field/run namespaces, logical and physical IDs, environment/tenant, aliases, schema IDs, snapshot/version, partition/cohort, code/config/reference/contract, and rename/move/split/merge history.

Retrieve declared sources: contracts, build manifests, dependency declarations, orchestration graphs, schemas, model configurations, owners, exposures, reports, feature definitions, and API/topic subscriptions.

Retrieve parse sources: raw and compiled SQL, dialect/engine/catalog/search path, macro/template inputs, view definitions, stored procedures, query plans, schema at parse time, parser/version, warnings, and unresolved references.

Retrieve runtime sources: run lifecycle events, input/output facets, query/job IDs, plans, snapshots, manifests, offsets, task attempts, code/image, configuration, reference data, engine version, timestamps, and publication receipts.

Retrieve inferred/curated sources: query/access/subscription logs, network/object audit, exports, notebooks, files, reports, dashboards, models, owner attestations, manual workflows, confidence, and expiry/review.

Retrieve transformation semantics: direct copy/cast/expression/aggregate/mask, join key/type, filter/branch, group/window/partition/order/limit, lookup/reference, explode/pivot, UDF/procedure/opaque, and row/cohort mapping where needed.

Retrieve coverage: eligible/captured jobs and runs, datasets, fields, statements, edges, unsupported syntax, dynamic paths, permission gaps, event/source lag, reconciliation age, parser errors, dead letters, and conflicts.

Retrieve serving/security: backward/forward/as-of queries, depth/path limits, field/edge filters, confidence thresholds, pagination, consistency, authorization, hidden-node behavior, query/literal redaction, audit, retention, and bulk export.

Distinguish logical job from run; dataset from dataset version; dataset edge from field edge; value derivation from control influence; declared from observed; parsed from certain; inferred from verified; ancestor from cause; descendant from affected; path from actual runtime flow; no edge from no dependency; unknown coverage from zero; and graph visibility from authorization to underlying data.

Create a lineage edge record:

| Concern | Required evidence and decision |
|---|---|
| Endpoints | Stable source/target entity, field, environment and versions |
| Activity | Logical job plus run/attempt/code/config/reference/contract |
| Semantics | Direct/indirect and copy/expression/aggregate/join/filter/group/order/etc. |
| Scope | Dataset/field/row/cohort/partition, valid interval and runtime interval |
| Origin | Declared/parsed/observed/inferred/curated source artifact/event |
| Method | Collector/parser/integration identity and version |
| Evidence | Plan/query/event/manifest/attestation reference and digest |
| Confidence | Method, score or categorical certainty and unresolved ambiguity |
| Protection | Classification, visibility, redaction, purpose and retention |
| State | Active/superseded/retracted/conflicting/stale plus review owner |

Write a falsifiable claim: “Run R91 of job J8 binds input snapshots O/V9 and Ref/V6 through code C4/config K2/schema S7 to output P/V81; observed dataset edges E1/E2 and parsed field edges F1–F12 agree for 11 direct mappings, `region → eligible_revenue` is retained as indirect filter influence, unresolved UDF output F13 is opaque, collector coverage is 100% of expected run events and 92% of eligible fields with stated denominator, authorized backward query Q5 reproduces the graph as of incident time, and actual consumer reads confirm U2 while two exports remain unknown rather than unaffected.”

## Learning Objectives

After completing this module, you should be able to:

1. distinguish dataset, column, row/cohort, declared, parsed, observed, inferred, and curated lineage;
2. design stable namespaced identities for jobs, runs, datasets, versions, schemas, fields, environments, and consumers;
3. model direct value and indirect filter/join/group/order/window/control influence;
4. extract lineage from SQL/plans/artifacts while preserving dialect, catalog, schema, parser, and ambiguity context;
5. bind runtime edges to concrete input/output/code/config/reference/contract versions;
6. reconcile multiple collection sources without erasing conflicts or overstating confidence;
7. handle schema evolution, stars, aliases, dynamic SQL, UDFs, cycles, and off-platform edges;
8. measure lineage coverage, freshness, correctness, stability, and query usefulness;
9. secure path traversal, query metadata, hidden entities, exports, retention, and active actions; and
10. validate lineage with fixtures, mutations, source reconciliation, as-of queries, and actual consumer evidence.

## Core Exposition

### Choose the graph grain from the decision

Model datasets when the question is broad discovery, product dependency, owner routing, or coarse blast radius. Add fields for schema compatibility, privacy propagation, precise impact, transformation review, and metric reasoning. Add partitions/cohorts/rows only when the consequence justifies collection cost and sensitive linkage.

Do not claim a finer grain than the evidence. A dataset input/output event proves that the activity related two dataset versions, not that every source column affected every target column. A parsed column map does not prove which branch executed or which rows flowed. Label projections accordingly.

Use job/activity nodes to mediate dataset transformations. A direct dataset-to-dataset convenience edge can be derived for traversal, but preserve which job/run/code performed the operation. Otherwise two independent transformations between the same tables collapse into one ambiguous arrow.

Separate logical topology from runtime instances. The logical graph supports design and selection; the runtime graph connects concrete runs and versions. Query APIs should let callers choose declared/current/as-of/run-specific perspectives.

### Establish stable endpoint and version identity

Namespace IDs by platform authority and environment/tenant. Preserve logical product identity, physical distribution/incarnation, schema version, and field identity. A name such as `public.orders.amount` is not globally unique and may be reused after recreation.

For file/object data, identify logical dataset plus manifest/snapshot and object versions. For topics, bind cluster, topic, schema, partition/offset interval. For APIs, bind service/environment/resource/contract and response field. For reports/features/models, bind artifact and serving version.

Represent rename separately from drop/add when continuity is known. Record mapping evidence and valid intervals. Positional writes and `SELECT *` require the source and target schema versions used at execution; expanding against today's schema corrupts historical lineage.

Use aliases and symlink/equivalence relationships cautiously. Two names may resolve to one version in one interval but diverge later. Do not merge identities permanently because one crawler observed a shared location once.

### Capture dataset lineage from intent and execution

Declared lineage comes from contracts, build manifests, orchestration, code annotations, and product/exposure definitions. It supports review before execution and highlights missing runtime capture. It can be stale or conditional.

Observed lineage comes from engine hooks, query/job APIs, execution plans, run events, file manifests, input/output facets, and publication receipts. Bind lifecycle events to one run and retain exact inputs/outputs. Capture failed and partial attempts separately; a failed run may still write data.

Static parsing extracts dependencies from raw/compiled SQL, view definitions, procedures, notebooks, and transformation code. Bind dialect, engine behavior, catalog/search path, schema versions, macro/template expansion, session settings, and parser version. Store unresolved identifiers and unsupported syntax.

Inferred lineage from access logs, temporal correlation, name matching, or model output can find gaps, but it carries method, confidence, scope, and review state. Curated edges add semantics and off-platform paths; they require owner, evidence, effective interval, review/expiry, and conflict handling.

### Model column transformations and control influence

For each target field, record direct input fields and transformation categories. Identity/copy, cast, arithmetic/expression, concatenation, aggregate, mask/tokenization, lookup, conditional, window, pivot/unpivot, explode and opaque UDF have different impact and explainability.

Record indirect dependencies that affect existence or arrangement: WHERE/HAVING predicates, join keys and join type, GROUP BY keys, window partition/order fields, ORDER BY/LIMIT, CASE conditions, deduplication/survivorship order, policy filters, configuration/reference fields, and branch predicates.

An output row can depend on a field without containing its value. A left join's right-side key influences match/null outcomes. A region filter controls membership. A timestamp order chooses the survivor. A privacy policy changes visibility. Calling these “no lineage” breaks impact analysis.

Avoid one unbounded transformation string as semantics. Store normalized categories and references to protected expressions/query text where authorized. Raw SQL can contain secrets, literals, personal data, or sensitive system names.

### Parse SQL and plans defensibly

Resolve lexical scopes, aliases, CTEs, nested/subqueries, correlated references, views, temporary objects, functions, stars, ordinal GROUP/ORDER, set operations, DDL/DML, MERGE, multi-statement scripts, and dialect-specific constructs. Preserve ambiguity rather than guessing silently.

Compiled SQL is usually closer to execution than templates, while source templates preserve developer intent. Store both linkage and digests. Query plans may reveal engine-resolved objects and expressions but can omit high-level names or change under optimization.

Schema context is required for `*`, NATURAL/USING joins, unqualified fields, implicit casts, and positional inserts. Bind catalog snapshot and search path. If schema is unavailable, emit a dataset edge and an explicit unresolved field gap instead of invented column edges.

Test the parser with golden fixtures and differential comparisons against engine plans/events. Include quoting/case, nested types, repeated field names, schema changes, macros, dynamic object names, UDFs, stored procedures, failures, and malicious input. Parser success means it returned a graph, not that the graph is correct.

### Reconcile evidence into versioned edges

Ingest each assertion idempotently using source record/event identity and collector version. Preserve raw evidence under governance. Normalize endpoint IDs and edge types without erasing origin. Corrections supersede or retract assertions with reason and time.

Multiple sources may confirm an edge, disagree on endpoint version, or supply different granularity. Keep a source-evidence set. A parsed field edge and observed dataset edge can jointly support a field mapping for a run when code/schema versions align; do not label the field edge directly observed unless runtime evidence actually contains it.

Define claim-specific precedence and reconciliation. Runtime inputs may override stale declared input for that run. Contract declaration remains authoritative for intended dependency. A curator may document a manual export. Conflicts trigger review when they affect critical impact or policy.

Track edge status, confidence, freshness, and coverage independently. High-confidence edges do not imply full graph coverage. A graph can be exact for captured SQL while missing all notebooks.

### Handle time, cycles, state, and granularity

Logical graphs may contain cycles: daily tables read prior versions; recursive queries iterate; feedback systems consume downstream signals; jobs update in place. Do not force acyclicity by deleting edges. Bind versions and runs so the execution graph reflects causal/temporal order where known.

For self-updates, distinguish input version from output version and transaction. For streaming, bind offset/watermark intervals and checkpoint/output commits. For mutable stores without snapshots, state the weaker time bounds and uncertainty.

Row lineage can be exact through stable record identities or approximate through partitions/cohorts. It can explode storage and expose relationships. Prefer the coarsest sufficient scope, use compressed mappings/manifests when possible, and enforce purpose, access, retention, and deletion.

Schema evolution changes lineage semantics. Additions may be harmless until star propagation exposes them. Dropped/renamed fields need successor mapping. Type or unit changes can preserve identity but break compatibility. Historical queries resolve the schema and edge version valid for the run.

### Serve traversal without overstating the answer

Backward queries accept target dataset/field/version, time/run, edge kinds, confidence/method filters, maximum depth, and stop boundaries. Forward queries accept the same constraints plus consumer type and criticality. Return paths with edge provenance, granularity, version, time, status and gaps.

Distinguish reachable, version-compatible, observed-in-run, actually-read, and confirmed-affected. A current logical descendant may not have consumed the incident version. A runtime reader may use only unaffected fields. A manual export may remain unknown.

Authorization applies during graph expansion. Simply removing hidden nodes can falsely connect visible endpoints or reveal that a secret intermediate exists. Use policy-defined redacted boundary nodes or state that paths are incomplete without disclosing protected identity. Filter counts, facets, timing, autocomplete and errors.

Bound traversal cost and denial-of-service risk. Use depth/path/result limits, pagination, cancellation, quotas, snapshot consistency, and cycle detection. Cache by principal/tenant/policy/graph version and invalidate safely.

### Measure and verify lineage quality

Define eligible scope: supported platforms/jobs/runs/datasets/fields/statements and required critical paths. Measure event capture, parse success, endpoint resolution, field mapping, indirect-dependency support, version binding, conflict rate, freshness and full-reconciliation age.

Validate known transformations end to end. Generate fixtures with copy, cast, expression, join, filter, group, window, star, rename, nested fields, DML, failures and UDF opacity. Mutate one input/control field and verify forward results. Reconcile declared versus observed jobs and catalog edges versus engine plans.

Measure usefulness through correct change impact, incident narrowing, deletion trace, owner routing, and consumer confirmation—not edge count or attractive diagrams. Sample edges with independent source evidence and investigate false positive/negative patterns by collector/dialect.

Operate collectors, queues, graph store, search/index, APIs and policy filters as production services. Alert on missing expected events, lag, dead letters, schema incompatibility, coverage drops, stale inferred/curated edges, unresolved critical conflicts and authorization anomalies.

## Definitions and Notation

Let:

- $G_t=(V_t,E_t)$ be the lineage graph constrained to version/time/runtime scope $t$;
- $e=(u,v,k,m,r,z,s,c,\tau,\sigma)$ be an edge with endpoints, kind, transformation, run, versions, source, confidence, time and granularity/scope;
- $D(y)$ be direct value inputs to output field $y$;
- $C(y)$ be indirect control inputs through filter/join/group/order/window/branch/policy;
- $I(y)=D(y)\cup C(y)$ be the full represented influence set;
- $Anc_t(y)$ and $Desc_t(x)$ be scoped ancestors and descendants;
- $Obs_t(x,y)$ mean compatible runtime evidence observes the dependency; and
- $Cov(S,X,t)=|Captured(S,X,t)|/|Eligible(S,X,t)|$ be method/source coverage when eligibility is known.

Potential field impact is

$$
PotentialImpact_t(x)=\{y:x\in I(y)\land y\in Desc_t(x)\}.
$$

Observed impact requires additional evidence; reachability alone supplies candidates. When eligibility is unknown, $Cov$ is reported unknown. Confidence in individual edges and completeness of the eligible graph are separate dimensions.

## Mechanisms, Invariants, or Proof Structure

Proof sketch that direct-value column lineage is insufficient for impact analysis:

1. Define `eligible_revenue = SUM(amount)` over rows satisfying `region='EU'`.
2. Direct-value mapping includes `orders.amount → eligible_revenue` because amounts contribute to the sum.
3. A value-only mapping omits `orders.region` because its literal value is not copied into the numeric output.
4. Baseline rows `(100, EU)` and `(50, US)` yield eligible revenue 100.
5. Change only the second row's region from `US` to `EU`; amount values remain unchanged.
6. Eligible revenue becomes 150, so region influenced the output by controlling membership.
7. Therefore sound impact lineage for this query includes `orders.region` as indirect filter influence.

The counterexample does not mean every control field changes every run. It proves that excluding control dependencies makes the graph unable to represent a real possible influence; exact observed impact still requires version, row/cohort, and runtime evidence.

The executable reproduces the counterexample. It is a deterministic teaching model, not a SQL parser, query engine, lineage collector, graph database, authorization service, or causal inference system.

<!-- bijux-verify: {"id":"indirect-column-lineage","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"direct_value_inputs=('orders.amount',)\ncontrol_inputs=('orders.region',)\nvalue_only_predicts_region_influence=False\nbaseline_revenue=100\nafter_region_change=150\nregion_has_indirect_lineage=True\n","stderr":""}} -->
```python
def eligible_revenue(rows):
    return sum(row["amount"] for row in rows if row["region"] == "EU")

baseline_rows = [
    {"amount": 100, "region": "EU"},
    {"amount": 50, "region": "US"},
]
changed_rows = [
    {"amount": 100, "region": "EU"},
    {"amount": 50, "region": "EU"},
]

direct = ("orders.amount",)
control = ("orders.region",)
baseline = eligible_revenue(baseline_rows)
changed = eligible_revenue(changed_rows)

print(f"direct_value_inputs={direct}")
print(f"control_inputs={control}")
print(f"value_only_predicts_region_influence={'orders.region' in direct}")
print(f"baseline_revenue={baseline}")
print(f"after_region_change={changed}")
print(f"region_has_indirect_lineage={'orders.region' in control and changed != baseline}")
```

## Alternatives and Trade-Offs

1. **Dataset versus column lineage:** dataset graphs scale broad discovery; column graphs improve precision but require schema/expression resolution and more storage.
2. **Column versus row/cohort lineage:** column influence suits most change analysis; row/cohort mapping narrows incidents/deletion at major cost and privacy exposure.
3. **Declared versus observed:** declared lineage supports design-time policy; observed lineage binds execution but depends on instrumentation coverage.
4. **Static parse versus runtime plan:** parsing covers history and intent; plans resolve actual engine objects but may be inaccessible, optimized, or incomplete semantically.
5. **Raw query storage versus normalized transforms:** raw text aids reproduction; normalization enables query and minimization. Protected references can combine them.
6. **Direct-only versus indirect influence:** direct maps are simpler; indirect control edges are essential for membership, match, grouping, ordering and policy impact.
7. **Graph materialization versus query-time derivation:** materialized edges make traversal fast; derivation avoids stale projections but costs latency and repeat work.
8. **Single merged edge versus evidence assertions:** merged edges simplify UI; evidence sets preserve conflict, method, confidence and audit.
9. **Exact confidence versus categorical evidence class:** numeric scores rank uncertainty but can imply false precision; labeled methods are interpretable but coarser.
10. **Full visibility versus redacted paths:** visibility improves discovery; redaction protects sensitive topology but can reduce explanation and completeness.
11. **Current graph versus temporal graph:** current state is easier to browse; temporal/run-specific lineage is necessary for reproducibility and incident correctness.
12. **Automated versus curated lineage:** automation supplies scale/freshness; curation captures business/off-platform paths but needs ownership, evidence and review.

## Failure Modes and Misconceptions

- **“An arrow is enough.”** It needs endpoints, semantics, versions, source, time, scope and evidence.
- **“Table names uniquely identify datasets.”** Namespace, environment, tenant, incarnation and version matter.
- **“A job node represents every run.”** Runtime attempts and data versions differ.
- **“Dataset lineage implies all-column lineage.”** It proves no field mapping by itself.
- **“Column lineage means copied values.”** Control fields influence rows, groups, matches, order and branches.
- **“Join keys are not outputs, so they do not matter.”** They determine match and null-extension behavior.
- **“Filters cannot affect aggregates.”** They determine aggregate membership.
- **“ORDER BY is cosmetic.”** With LIMIT, windows or survivorship, it changes selected output.
- **“A parser returned success, so lineage is correct.”** Dialect, schema, scope and unsupported constructs can be wrong.
- **“Raw SQL is execution truth.”** Templates, session state, dynamic SQL and optimizer resolution intervene.
- **“Compiled SQL is sufficient.”** External calls, UDFs, procedures and runtime branching may remain opaque.
- **“Expand stars with the current schema.”** Historical execution used a specific schema version.
- **“Unqualified columns are obvious.”** Repeated names, search paths and correlated scopes create ambiguity.
- **“Declared lineage is runtime lineage.”** Intent may be stale, conditional or bypassed.
- **“Observed dataset inputs prove observed field mappings.”** Finer mappings may still be parsed/inferred.
- **“Inferred edges can fill gaps silently.”** Method, confidence, scope and review must remain visible.
- **“No edge proves independence.”** Instrumentation, permission and platform gaps exist.
- **“More edges mean better lineage.”** False/untyped/stale edges damage precision and trust.
- **“A DAG cannot contain cycles.”** Logical/temporal systems can recur; versions/runs clarify order.
- **“Self-update is self-dependency without time.”** Input and output versions must differ.
- **“Every descendant consumed the bad version.”** Runtime/read and field/cohort evidence narrow actual impact.
- **“Reachability proves cause.”** It supplies possible influence, not causal identification.
- **“Row lineage is always best.”** It can be costly, unstable, and privacy-sensitive.
- **“Access logs complete off-platform lineage.”** Exports, caches, shared identities and retention gaps remain.
- **“Curated edges are low quality.”** They may be the authoritative evidence for manual paths when governed.
- **“Conflicting edges should be deduplicated away.”** Conflict may reveal drift or collector defects.
- **“Lineage metadata is harmless.”** It can expose systems, fields, predicates, users and protected relationships.
- **“Hide nodes after traversal.”** Paths, counts and timing can still leak hidden topology.
- **“One coverage percentage is enough.”** Break it down by source, platform, run, dataset, field, transform and criticality.
- **“A beautiful graph proves operational value.”** Validate real change, incident, deletion and consumer decisions.

## Worked Examples

### Example 1

A build manifest declares model A reads source S. Runtime input events for run R show replacement view V instead. Both edges remain: observed R uses V, and declared drift from S opens a contract/catalog issue.

### Example 2

`SELECT *` executed before a sensitive column was added. Historical lineage expands against schema S4, not current S5, avoiding a false claim that the old output propagated the new field.

### Example 3

A LEFT JOIN uses customer ID. The key indirectly affects whether right-side attributes are populated even when the key is not emitted. Edge semantics record join-key influence and join type.

### Example 4

A deduplication window orders by `updated_at DESC, source_priority`. Both fields control which record survives; downstream value lineage includes them as selection/order influences.

### Example 5

A UDF returns risk tier. Runtime captures datasets and columns, while transformation is labeled opaque UDF with code artifact/version. The system does not invent internal dependencies.

### Example 6

A streaming job reads offsets 100–199 and publishes checkpoint/output V9. Runtime lineage binds that interval; logical topic lineage alone cannot answer which events affected V9.

### Example 7

A daily table reads yesterday's published version. Logical graph has a self-cycle; runtime graph connects D41 → run R42 → D42, preserving temporal order.

### Example 8

A notebook downloads CSV and emails it. Object audit plus owner attestation adds a time-bounded curated export edge with lower coverage. The email recipient remains protected and off-platform impact unknown.

### Example 9

A restricted intermediate lies between two visible datasets. The API returns a policy-defined redacted boundary and incomplete-path marker instead of connecting endpoints directly or revealing the hidden name.

### Example 10

A golden SQL suite passes direct mappings but mutation of a filter field fails to appear downstream. The new indirect-influence test catches the false negative before collector rollout.

## Cross-Program Connections

- **Graph Algorithms:** reachability, paths, cycles, temporal graphs, transitive reduction, indexing, pagination, and bounded traversal implement lineage queries.
- **Programming Languages:** parsing, name/scope resolution, intermediate representations, data/control dependence, program slicing, macros, and opaque calls inform extraction.
- **Database Engineering:** catalogs, query plans, schemas, transactions, temporal versions, recursive queries, access logs, and snapshot isolation supply evidence.
- **Distributed Systems:** events, clocks, retries, idempotency, partial failure, eventual consistency, reconciliation, and causal order shape runtime graphs.
- **API and Service Engineering:** stable identifiers, versioned contracts, authorization, pagination, filtering, bulk export and subscriptions govern lineage services.
- **Platform Engineering:** collectors, paved integrations, catalogs, policy hooks, self-service impact, SLOs and repair workflows scale adoption.
- **Security Engineering:** graph authorization, least privilege, query protection, tenant isolation, audit, inference resistance and supply-chain provenance protect topology.
- **Privacy Engineering:** field/row derivation, purpose, minimization, deletion, export tracing, access, retention and protected relationships drive use cases and limits.
- **Reliability Engineering:** coverage telemetry, missing-event alerts, incident slicing, collector recovery, failure injection and consumer confirmation keep lineage useful.
- **Causal Inference:** influence paths generate candidates; interventions, counterfactuals, confounding and uncertainty distinguish causality from reachability.

## References

1. OpenLineage. [Object model](https://openlineage.io/docs/spec/object-model/). Accessed 2026-09-03. Primary specification documentation for run, job, dataset, namespace, version, event, and facet identities.
2. OpenLineage. [Run cycle](https://openlineage.io/docs/spec/run-cycle/). Accessed 2026-09-03. Primary documentation for event-based run lifecycle states and runtime inputs/outputs.
3. OpenLineage. [Lineage Dataset Facet](https://openlineage.io/docs/spec/facets/dataset-facets/lineage/). Accessed 2026-09-03. Primary current specification for dataset/job inputs, exact fields, relationships, source types, and direct/indirect transformations.
4. OpenLineage. [Column Level Lineage Dataset Facet](https://openlineage.io/docs/spec/facets/dataset-facets/column_lineage_facet/). Accessed 2026-09-03. Primary documentation for fine-grained input-field dependencies and direct/indirect transformation categories.
5. OpenLineage. [Schema Dataset Facet](https://openlineage.io/docs/spec/facets/dataset-facets/schema/). Accessed 2026-09-03. Primary specification for dataset field names, types, descriptions, nested fields, and additional schema properties.
6. OpenLineage. [Job Type Job Facet](https://openlineage.io/docs/spec/facets/job-facets/job-type/). Accessed 2026-09-03. Primary specification for job processing/integration/job-type classification.
7. W3C. [PROV-DM: The PROV Data Model](https://www.w3.org/TR/prov-dm/). Accessed 2026-09-03. Authoritative conceptual model for entities, activities, agents, generation, usage, derivation, attribution, specialization, and provenance bundles.
8. dbt Labs. [Manifest JSON](https://docs.getdbt.com/reference/artifacts/manifest-json). Accessed 2026-09-03. Primary documentation for versioned nodes, sources, tests, exposures, metrics, semantic models, parent/child maps, and invocation metadata.
9. DataHub. [Lineage](https://docs.datahub.com/docs/features/feature-guides/lineage). Accessed 2026-09-03. Primary project documentation for upstream/downstream dataset and column lineage, visualization, editing, impact analysis, and path exploration.
10. OpenMetadata. [Data Lineage](https://docs.open-metadata.org/latest/how-to-guides/data-lineage). Accessed 2026-09-03. Primary project guidance for viewing, adding, editing, and managing table/pipeline and column-level lineage.
11. Apache Atlas. [Architecture](https://atlas.apache.org/2.0.0/Architecture.html). Accessed 2026-09-03. Primary project documentation for type/entity metadata, ingestion, graph storage, search, lineage, classifications, and notification integration.
12. Google Cloud. [About data lineage](https://cloud.google.com/data-catalog/docs/concepts/about-data-lineage). Accessed 2026-09-03. Primary product documentation for lineage information models, processes, sources/targets, entry identity, and supported collection behavior.
13. Amazon Web Services. [Data lineage in Amazon DataZone](https://docs.aws.amazon.com/datazone/latest/userguide/data-lineage.html). Accessed 2026-09-03. Primary product documentation for OpenLineage-compatible lineage events, dataset/job/run entities, upstream/downstream views, and API-enabled capture.
14. OpenTelemetry. [Trace API](https://opentelemetry.io/docs/specs/otel/trace/api/). Accessed 2026-09-03. Primary specification for trace/span identity, parent relationships, links, events, attributes, status, and context relevant to correlating runtime activities.

## Exercises

### Exercise 1

Design a dataset/column lineage model for batch SQL plus streaming CDC. Include IDs, versions, runs, offsets/snapshots, transformation and control types, provenance, confidence, time, coverage, conflicts, and correction.

### Exercise 2

Derive column lineage for a query with CTEs, LEFT JOIN, WHERE, GROUP BY, windowed deduplication, CASE, ORDER BY/LIMIT, and `SELECT *`. Separate direct and indirect inputs and list required schema/dialect context.

### Exercise 3

Design a collector validation program covering parser fixtures, runtime events, declared-versus-observed reconciliation, dynamic SQL/UDF gaps, schema evolution, cycles, missing/out-of-order events, and coverage reporting.

### Exercise 4

Design an authorized forward-impact API for a restricted multi-tenant graph. Include versions/time, field/control filters, confidence, hidden nodes, path/depth limits, pagination, consistency, caches, errors, audit, and bulk export.

### Exercise 5

Investigate an incident where a renamed reference field, stale declared lineage, a notebook export, and a current catalog graph disagree with the incident run. Produce bounded candidate/impact claims and corrective actions.

## Answers to the Exercises

### Answer 1

Represent logical jobs separately from run/attempt; logical datasets/distributions separately from snapshot/manifest/topic-offset versions; fields by schema-scoped stable identity. Edges bind source/target versions through run, code/config/reference/contract and record dataset/field/partition grain; direct copy/cast/expression/aggregate and indirect join/filter/group/window/order/branch semantics; declared/parsed/observed/inferred/curated source; collector/parser/event evidence, confidence, valid/runtime time and protection. CDC edges bind source offset interval, checkpoint and atomic output; batch binds source/output snapshots. Idempotent assertion IDs permit replay, while supersession/retraction preserves history. Reconcile evidence sets and retain conflicts. Report eligible/captured jobs/runs/datasets/fields/edge kinds, unsupported paths and unknown denominators separately.

### Answer 2

Resolve dialect, catalog/search path, raw and compiled SQL, schema versions, aliases/scopes and star expansion. Direct inputs include fields copied or used in CASE/value expressions and aggregate arguments. Indirect inputs include LEFT JOIN keys/type for match/null extension; WHERE/HAVING membership; GROUP BY grouping; window PARTITION/ORDER and dedup rank; CASE predicates; final ORDER BY/LIMIT selection. CTEs and views preserve intermediate mappings but can be collapsed into derived paths with provenance. `*` expands only against execution schema. Repeated/unqualified names remain unresolved if scope cannot prove them. UDF calls identify input/output fields and opaque code version without invented internals.

### Answer 3

Build golden fixtures per dialect for quoting, aliases, nested CTE/subqueries, correlated references, stars, joins, filters, groups, windows, sets, DDL/DML/MERGE, schema evolution, dynamic names and expected opacity. Compare normalized parser edges with engine-resolved plans and runtime events. Inject missing/duplicate/out-of-order run events, partial writes, collector restarts, stale schemas and parser upgrades; require idempotent replay and temporal state. Include version-unrolled self/recursive cycles. Reconcile declared eligible jobs with observed runs and captured inputs/outputs; sample edges against source artifacts. Report event, endpoint, dataset, field, indirect-kind and critical-path coverage with denominators, lag, errors, dead letters, unsupported syntax, conflicts and unknowns.

### Answer 4

Require tenant/principal/purpose and authorize before traversal. Query target/source stable ID plus version/run/as-of time, direct/indirect kinds, field scope, method/confidence and maximum depth. Return provenance-bearing paths and gap markers under snapshot-consistent pagination with quotas/cancellation. During expansion, filter protected nodes/edges; use policy-approved redacted boundaries or incomplete markers without reconnecting visible endpoints or leaking via counts, timing, facets/errors. Cache by tenant/principal/policy/graph version and invalidate on entitlement/edge change. Audit query and result scope; protect query text. Bulk export requires separate authority, size/rate/retention controls and receipt. Test cross-tenant IDs, hidden cycles, inference probes and stale caches.

### Answer 5

Pin incident output/run/code/config/reference/schema and rebuild its runtime graph, not today's catalog view. Map old/new reference field identity using schema/evolution evidence; treat stale declaration as intent/drift and runtime events/plans as run evidence. Backward slice includes direct and indirect use of the renamed field with confidence/gaps. Forward slice yields potential compatible descendants, then intersect actual reads and affected fields/cohorts. Add notebook/export as curated/audit-supported edge and mark untraceable recipients unknown. State candidates rather than cause until controlled evidence supports mechanism; state potential rather than observed impact until consumers confirm. Correct collector rename mapping, refresh declaration, add evolution fixtures/coverage alert, govern exports, preserve incident graph, verify corrected generation and downstream consumers, and review recurrence.
