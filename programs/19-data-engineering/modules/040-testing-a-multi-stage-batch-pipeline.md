---
module_id: DE-040
program: Data Engineering
level: 1
module_number: 40
title: Testing a Multi-Stage Batch Pipeline
status: complete
last_verified: 2026-09-02
---

# Testing a Multi-Stage Batch Pipeline

## One-Page Review

### Governing question

How can a test strategy establish that every stage and boundary in a batch pipeline preserves the intended population, semantics, lineage, and publication guarantees across ordinary data, adversarial cases, retries, partial failures, and change?

### Essential definitions

- A **multi-stage batch pipeline** is a directed transformation graph whose nodes read governed dataset generations and emit new candidate generations under explicit contracts.
- A **stage contract** defines input population, schema, grain, keys, semantics, rejected-data disposition, output ownership, deterministic environment, and acceptance checks for one graph node.
- An **edge contract** defines what an upstream output guarantees to a downstream input, including version compatibility, completeness, ordering if any, and publication visibility.
- A **test oracle** decides whether an observed result is acceptable: exact expected rows, a reference implementation, an invariant, a metamorphic relation, a source control, or a domain-approved statistical rule.
- A **fixture** is a versioned input/reference/environment example with an explicit purpose and expected disposition; it is not a miniature production dataset chosen only for convenience.
- A **contract test** evaluates schema, grain, key, type, nullability, value domain, referential, temporal, and compatibility promises at a boundary.
- A **differential test** compares two implementations or execution modes over the same governed cut using a declared equivalence relation.
- A **metamorphic test** changes input in a way that should induce a known relation in output when an exact output oracle is hard to construct.
- A **fault-injection test** introduces a controlled failure such as a lost acknowledgement, partial write, retry, corrupt object, or concurrent publisher and evaluates recovery invariants.
- **mutation testing** deliberately changes transformation or test logic to see whether the assurance suite detects meaningful defects.
- A **quality gate** maps a versioned assertion result and severity to block, quarantine, warn, approve, or publish; a green run state is not itself a data acceptance decision.
- A **test evidence bundle** binds inputs, code, environment, oracle versions, results, failing examples, candidate identity, and publication receipt.

### Central model, mechanism, or theorem

Let the pipeline graph be $G=(V,E)$, with each stage $v_i$ implementing $f_i$ under contract $C_i$. For immutable source cut $S$, reference cut $R$, and environment $D$, the promised output is

$$
O=F_G(S,R,D).
$$

Testing one example per node does not establish $F_G$. For every stage, edge, and end-to-end obligation $b\in B$, choose data scenarios $x\in X$, physical execution variants $p\in P$, and failure/change scenarios $z\in Z$. Evidence matrix

$$
M\subseteq B\times X\times P\times Z
$$

should cover each risk-bearing interaction justified by impact and likelihood. A test observation $T(m)$ supports an obligation only when its oracle is independent enough, its input cut and environment are controlled, and its comparator matches the contract.

Composition is justified only if each stage satisfies its local contract, every adjacent output/input contract is compatible, rejected and empty populations are accounted for, and the end-to-end oracle checks properties not implied locally. Passing tests provide bounded evidence; they do not prove arbitrary data, schedules, engines, or future changes correct.

### Critical invariants

- The pipeline graph, stage ownership, source/reference cuts, output generation, and tested compiled semantics are identified.
- Every stage has explicit input/output grain, keys, schema, row disposition, and invariants; every edge has compatibility and completeness rules.
- Raw deliveries, logical occurrences, duplicates, superseded revisions, accepted records, quarantine, and rejected records reconcile without silent loss or double counting.
- Fixtures cover normal, boundary, adversarial, sparse/empty, skewed, duplicate, delete, late/corrected, schema-change, and invalid records with named intent.
- Oracles compare exact keyed rows or all contractual dimensions; totals and row counts alone cannot mask offsetting errors or group movement.
- Unit tests isolate transformation logic; integration tests exercise actual engine, types, storage, transactions, permissions, and publication behavior.
- Incremental, merge, backfill, restatement, and full-refresh paths are compared at the same governed source/reference/code cut.
- Partition boundaries, time zones, nulls, rounding, overflow, nondeterministic order, retries, and concurrency are deliberately perturbed.
- Expected failures prove the test ran and detected the intended violation; skipped, unavailable, warned, and errored assertions remain distinct.
- Candidate generations remain isolated until blocking gates pass and a conditional publication confirms the expected parent.
- Failing rows, manifests, logs, lineage, fingerprints, costs, durations, and recovery receipts are retained under security/privacy policy.
- Test selection and thresholds are risk-owned, versioned, observable, and periodically challenged with seeded defects and incidents.

### Common failures

Common failures include testing only the final row count; using production samples with no known oracle; asserting only happy paths; mocking away SQL engine, storage, permissions, or transaction semantics; comparing unordered data as an accidental sequence; treating equal totals as equal allocation; omitting quarantine from conservation; testing an incremental query without prior target state; replacing golden results whenever code changes; letting fixtures depend on current time or mutable reference data; running tests against different compiled code than production; ignoring skipped or failed-to-execute checks; setting thresholds from the incident data being judged; relying on one partition and one worker; never injecting partial writes or unknown commits; publishing before checks finish; and measuring test count rather than risk/defect detection.

### Compact example

Six deliveries represent four event identities: one exact duplicate and one superseded revision are present. Normalization selects three valid winning events and one unknown-currency quarantine. Enrichment converts `e1=8000 USD`, `e2=10000 EUR` at `6/5`, and `e3=5000 USD`; aggregation yields `A=20000`, `B=5000`, total 25000 minor USD units. Reversing delivery order and replaying all deliveries leave the result unchanged; an equal-revision conflict fails. A corrupt output `A=19000`, `B=6000` preserves total 25000, so a total-only check passes while the exact keyed oracle detects the defect.

### Connections

[DE-030](030-designing-replayable-raw-ingestion.md) supplies trusted replay inputs, while [DE-031](031-extract-transform-load-and-extract-load-transform.md) through [DE-039](039-deterministic-transformations.md) define stage placement, SQL/dataframe semantics, partitioning, incrementality, merge, backfill, correction, and deterministic equivalence. This capstone tests that block as a coherent system. DE-041 next introduces dependency graphs and orchestration operations.

## Governing Question

What evidence would convince a skeptical owner that a change to one stage cannot silently lose, duplicate, misclassify, misattribute, or partially publish data anywhere across the batch pipeline?

A green process exit proves that an engine finished a submitted computation. It does not prove that all expected source units arrived, the intended compiled query ran, rejected records were preserved, joins had correct cardinality, amounts were assigned to the right groups, the incremental path matched full recomputation, or readers saw one coherent generation. Test strategy begins with these obligations rather than a framework command.

A multi-stage pipeline amplifies boundary defects. A parser converts missing to zero; a normalization stage accepts the value; an aggregate produces plausible totals; a report formats them cleanly. A final not-null test passes because the lossy decision happened upstream. Stage-local and edge assertions must make the earliest semantic loss observable, while end-to-end oracles check composition and publication.

No single oracle is sufficient. Exact expected rows are powerful for small fixtures but cover only enumerated cases. Generic uniqueness/null/reference checks expose structural violations but may accept wrong business logic. Source controls detect loss or duplication but can miss misallocation. Differential tests can share the same bug. Statistical thresholds find drift but require history and tolerate some deviations. Combine independent evidence according to risk.

Testing also includes failure and recovery. Batch pipelines write large mutable surfaces, retry after ambiguous outcomes, overlap with live loads, and publish through metadata. A suite that validates values only after an ideal run says little about partial partitions, duplicate retry, stale writers, corrupt candidate manifests, or a failed notification. Recovery invariants belong in the design.

## Why This Matters

Data defects are often valid software executions. A join can multiply rows without throwing. A timestamp cast can shift a reporting day. A merge can retain a deleted entity. A partition filter can omit the final boundary. The engine faithfully computes the wrong specification, so conventional exception monitoring remains green.

Errors compound across stages. If one duplicate is introduced before a many-to-many join, it may multiply again, inflate aggregates, and become difficult to trace from the final report. Early stage controls reduce diagnostic distance; later reconciliation proves that local checks did not miss a cross-stage interaction.

Real data has a much larger state space than a few handwritten rows. Nulls interact with joins and predicates. Equal timestamps expose tie behavior. Daylight-saving changes expose civil-time assumptions. Huge values expose overflow. Skew changes execution. Deletes and corrections exercise negative paths. Property-based and generated fixtures can explore combinations, but generation distributions and shrinking behavior are themselves part of the evidence.

Change is continuous. Source schemas evolve, reference mappings are corrected, SQL compilers and engines upgrade, partition layouts change, and cost controls adjust parallelism. A regression suite preserves deliberate behavior while differential and migration tests expose intended versus accidental change. Blindly refreshing snapshots turns the suite into an approval mechanism for whatever the new code emitted.

Production data quality differs from pre-deployment correctness. Static fixtures cannot predict a new source value, missing daily file, distribution shift, or tenant-specific anomaly. Runtime assertions and reconciliation are necessary, but they should validate an isolated candidate or route bad records safely rather than discover corruption only after publication.

Testing has operational cost. Full exact comparison can scan terabytes; exhaustive fault injection consumes environments; retained failing rows may be sensitive. Risk-tier the checks, use hierarchical fingerprints and sampled diagnostics where justified, run expensive full/differential checks on a schedule or change trigger, and never label a sampled result as full proof.

Finally, evidence must be reconstructable. A test report without source snapshot, code/compiled query, reference cut, engine, parameters, assertion version, and candidate identity cannot answer which result was tested. If tests run on one artifact and publication promotes another, the checks are irrelevant.

## Prerequisites and Retrieval

Retrieve the business/output contract and owner; complete pipeline graph and stage/edge ownership; sources, immutable cuts, expected manifests, raw receipts, schemas, source controls, and retention; reference/dimension versions; transformation source and compiled SQL/plans; parameters, feature flags, macros, UDFs, dependencies, engine/adapter/container/runtime; stage inputs/outputs, grain, keys, multiplicity, null/value domains, temporal semantics, join cardinalities, filters, rejected/quarantine routes, and output ownership; partitions, boundaries, calendars/time zones/tzdb, ordering/tie rules, decimal/floating arithmetic, overflow/rounding; incremental checkpoints, prior target state, merge/delete/tombstone behavior; backfill/restatement scope; deterministic envelope; candidate and publication mechanism; current unit/contract/integration/end-to-end/runtime tests; fixtures/generators/golden datasets; exact/reference/differential/metamorphic/statistical/source-control oracles; severity/threshold/waiver policies; test selection and dependency mapping; fault-injection facilities; staging/isolation; security/privacy masking; resource/performance baselines; observability/lineage; incidents and escaped defects; rollback/restore; and disaster-recovery exercises.

Distinguish source completeness from row validity; delivery from logical occurrence; schema compatibility from semantic compatibility; stage test from edge contract test; pure logic test from actual-engine integration; exact oracle from invariant; reference implementation from duplicated logic; golden fixture from production baseline; expected failure from test execution error; warning from acceptance; test flakiness from legitimate nondeterminism; sample comparison from population comparison; count conservation from key-level correctness; statistical anomaly from known invalidity; data drift from code regression; incremental delta from final merged state; candidate validation from publication; process success from dataset acceptance; rollback test from destructive production rollback; test coverage from test count; and retained diagnostic evidence from uncontrolled sensitive-data duplication.

Create a pipeline assurance contract:

| Concern | Required decision and evidence |
|---|---|
| Graph | Stage and edge identities, owners, dependencies, critical outputs, tested selection closure |
| Boundary | Source/reference cuts, expected units, schemas, grain/keys, completeness and compatibility |
| Disposition | Duplicate/superseded/accepted/quarantined/rejected/deleted counts and identities |
| Semantics | Code/compiled artifact, parameters, join/filter/window/aggregate rules, deterministic envelope |
| Oracles | Exact rows, reference/differential/metamorphic rules, controls, tolerances, owner/version |
| Fixtures | Named risks, minimal cases, boundaries, invalid forms, expected stage and final outcomes |
| Execution | Actual engines/storage, partition/concurrency variants, permissions, resources, retries |
| Change | Schema/code/reference/runtime migration, incremental/full parity, golden approval process |
| Failure | Fault point, expected partial state, retry/recovery behavior, unknown-outcome reconciliation |
| Runtime | Candidate assertions, drift/freshness, severity, waiver/expiry, failing-record handling |
| Publication | Isolated generation, blocking evidence, expected parent, atomic/conditional transition |
| Evidence | Manifests, results, failures, lineage, fingerprints, cost/duration, security and retention |

Write each high-risk obligation as a falsifiable sentence. “For manifest `m`, every winning order identity is either represented exactly once in accepted stage `a` or named exactly once in quarantine `q`; aggregate `g` conserves accepted signed minor units by account/currency policy; only candidate `g` tested under bundle `t` may replace expected parent `p`.”

## Learning Objectives

After completing this module, you should be able to:

1. model a multi-stage batch pipeline as stage and edge contracts with explicit end-to-end obligations;
2. derive a risk-based assurance matrix across data scenarios, execution variants, failure/change modes, and oracle types;
3. design minimal fixtures for boundaries, joins, duplicates, deletes, corrections, nulls, time, arithmetic, skew, and empty populations;
4. choose exact, reference, differential, metamorphic, control-total, structural, and statistical oracles without overstating them;
5. test SQL/dataframe logic separately from actual-engine, storage, permission, transaction, and publication integration;
6. reconcile deliveries, identities, accepted/quarantined records, stage totals, group movement, and final keyed output;
7. verify incremental, merge, backfill, correction, retry, partition, concurrency, and full-refresh behavior at identical cuts;
8. inject partial writes, lost acknowledgements, corrupt artifacts, stale publishers, resource exhaustion, and recovery actions safely;
9. govern runtime quality gates, warning/blocking severity, waivers, evidence retention, privacy, and diagnostic access; and
10. demonstrate test effectiveness through mutations, escaped-defect analysis, coverage traceability, and periodic recovery rehearsal.

## Core Exposition

### Draw the tested graph and its contracts

Start from the logical dataflow, not the scheduler screen. Name source datasets, transformation stages, quarantine paths, reference inputs, candidate outputs, validation nodes, publication pointer, and downstream contracts. Include dynamically selected partitions and external table functions that might be invisible in static SQL.

For each stage, document input grain and expected population, output grain and ownership, primary/business keys, duplicate and correction semantics, schema/type/null rules, join cardinality, ordering/window rules, arithmetic, rejected-data disposition, deterministic dependencies, and lineage. An edge contract states what the consumer can rely on and which versions are compatible.

Graph structure itself is testable. Missing an edge in selection logic can run a downstream stage against an old parent. An extra broad dependency can cause unnecessary work but is usually safer than a false dependency that still does not ensure a matching generation. Test declared graph shape, dynamic expansion, selection closure, and the exact dataset generations bound at runtime.

Stage contracts must compose. If normalization emits one row per logical occurrence but enrichment assumes one row per delivery, multiplicity disagrees. If a producer treats empty output as successful absence while a consumer treats a missing partition as empty, loss becomes invisible. Review adjacent contracts together.

### Build an obligation inventory before cases

List what can go wrong by semantic surface: source population, decode/schema, identity/order, filtering, joins, time, arithmetic, aggregation, partitioning, incremental state, target mutation, quarantine, lineage, publication, notification, and recovery. Map each obligation to owner, impact, existing control, oracle, fixture, execution level, and evidence artifact.

An assurance matrix is more useful than a count of test functions. One uniqueness test may cover thousands of columns poorly; one carefully designed end-to-end fixture may cover a high-risk correction and group move. Trace coverage to claims and escaped incidents.

Prioritize by consequence and uncertainty. A public financial dataset, entitlement mapping, or training label deserves exact key-level and failure-path evidence. A disposable exploratory table may use lighter gates. Risk tier changes frequency and depth, not the need to state what is untested.

Include negative obligations. Prove that invalid records are rejected or quarantined with reason and lineage, stale writers cannot publish, duplicate retries add no effect, and warnings do not silently become passes. A suite that checks only desired output may ignore forbidden output.

### Layer tests by what they can observe

**Static and compile checks** validate parseability, references, graph cycles, configuration, schema declarations, policy rules, and generated/compiled artifacts. They are fast and can fail before data execution, but they cannot prove runtime semantics.

**Pure logic tests** feed small values into deterministic parsing, mapping, classification, interval, or business-rule functions. They localize defects and support exhaustive boundaries. They miss engine casts, SQL three-valued logic, distributed order, storage, and permissions if those are mocked.

**Model/stage tests** run one transformation with fixed direct-parent fixtures and exact expected rows. dbt documents unit tests using small static inputs before materializing a full SQL model. These are valuable for complex case logic, windows, regex, and date behavior, while product/version limitations remain relevant.

**Dataset contract tests** run against built stage outputs. They check unique/not-null/accepted/reference constraints, custom failing-row queries, distributions, freshness, and business invariants. dbt data tests express assertions as queries returning failing records; Great Expectations describes Expectations as verifiable data assertions. Neither vocabulary automatically supplies the correct domain oracle.

**Integration tests** use the actual engine, adapter, storage format, catalog, transactions, credentials/roles, UDF/runtime, and representative scale. They expose behavior that local in-memory substitutes cannot. Keep destinations isolated and verify cleanup without using destructive broad targets.

**End-to-end tests** bind known versions for every source and reference, execute the complete selected graph, replace production sinks with candidate/test sinks, and compare every final output and quarantine path. Apache Beam documents testing individual functions, transforms, and entire pipelines with known static input and expected collections; the general layering principle applies beyond Beam.

**Runtime assurance** validates real candidate data, source manifests, reconciliations, drift, lineage, and publication conditions. It catches novel production input but should never mutate the expected answer to fit observed data automatically.

**Recovery tests** inject failures and prove restart, replay, rollback/forward repair, and restore. They require stateful infrastructure and stable operation identities. Run safely in dedicated environments or isolated generations.

No layer dominates. A perfect isolated function can be wired to the wrong table. An end-to-end happy path may not diagnose a boundary error. Runtime monitoring cannot replace pre-deployment edge cases.

### Design fixtures from partitions of behavior

Derive equivalence classes and boundaries from the contract. For a half-open date range $[a,b)$, include $a-\epsilon$, $a$, $b-\epsilon$, and $b$ at actual timestamp precision. For a join, include one-to-one, missing reference, duplicate reference, null key, key change, validity-boundary overlap/gap, and unexpected many-to-many cases.

For identity, include exact redelivery, same identity/different payload, legitimate repeat under different identity, stale revision, equal-version conflict, out-of-order revisions, delete/tombstone, and resurrection attempt. State the expected stage disposition of every row.

For numeric logic, include zero, sign changes, maximum/minimum, overflow, scale differences, halfway rounding, division remainder, NaN/infinity/signed zero where allowed, cancellation, and aggregation order. Use exact minor units when the domain is exact.

For text, include empty versus null, whitespace policy, composed/decomposed Unicode, case/accent/locale-sensitive characters, invalid encodings, long values, and separator/control characters. For time, include UTC offsets, leap-day/calendar boundary, daylight-saving gap/fold, period close, precision truncation, late arrival, and correction.

For partitioning, include empty, singleton, sparse, full, skewed/hot-key, first/last unit, adjacent partitions, key/date movement, window context beyond ownership, and a missing/corrupt input unit. Test different physical grouping without changing logical content.

Minimize fixtures so each failure explains a rule, but include interaction cases. A null join key plus duplicate reference may follow a different path than either alone. Property-based generation can explore combinations and shrink failures; constrain generators to meaningful domain states and retain the minimal reproduced example, seed/database, library version, and settings.

Never use raw production data casually. Create synthetic or policy-approved masked/subset fixtures with referential and distribution properties retained as needed. Validate masking determinism and leakage risk; a hashed direct identifier may remain linkable personal data.

### Choose strong and independent oracles

An exact row oracle is strongest for a small deterministic result. Compare schema, types, keys, multiplicity, nulls, values, and order only when contractual. PySpark provides dataframe and schema equality utilities with row-order and numerical tolerance options; those options still need deliberate domain settings.

A reference oracle computes expected results by a separately reviewed implementation, perhaps simple standard-library code over a tiny fixture. Copying the production SQL expression into the test duplicates the same mistake. Favor clarity and different mechanisms over speed.

Source controls reconcile independent source facts: expected files/positions, occurrence counts, signed amounts, hash totals, and business control reports. A count can detect loss/duplication but not field swaps. Combine controls at meaningful dimensions such as tenant/date/currency/account and compare exact keys for critical populations.

Metamorphic relations work when full expected output is difficult. Examples:

- permuting unordered input leaves keyed output unchanged;
- duplicating an exact delivery leaves deduplicated output unchanged;
- splitting an exact additive group and recombining preserves totals;
- adding a zero-effect record changes only documented counts;
- shifting all event times and boundaries by an allowed translation shifts output periods correspondingly;
- full recomputation equals incremental application at the same cut;
- backfill units in different execution order publish the same generation; and
- changing one classification moves value from old group to new with global conservation.

Differential tests compare SQL versus dataframe, old versus new engine, serial versus parallel, full versus incremental, or current versus proposed code. Agreement is strong when implementations are independent and the comparator is complete. Shared source corruption, ambiguous requirements, or copied helpers can make both paths agree wrongly.

Statistical and distribution oracles detect unexpected drift in counts, null rates, distinctness, quantiles, category frequencies, and relationships. Pin the reference window, segmentation, seasonality, multiple-comparison policy, minimum volume, threshold derivation, and response. A statistically unusual value is not necessarily invalid; a stable distribution can still encode a systematic semantic defect.

Golden snapshots preserve complex expected results. Every update needs a human-readable key-level diff, reason, contract/source/reference version, owner approval, and separation between intended changes and unexplained drift. Never regenerate and approve in one opaque command.

### Assert stage conservation and disposition

Track both deliveries and logical identities. Let $N_D$ be delivered records. After stable identity/revision classification,

$$
N_D=N_{exact\ duplicate}+N_{superseded}+N_{winning\ assertions},
$$

under a precisely defined counting convention. Winning assertions then reconcile as

$$
N_{winning\ assertions}=N_{accepted}+N_{quarantined}+N_{rejected},
$$

where categories are disjoint and every identity has lineage. Do not add counts from different grains.

Value conservation applies only across semantics that should conserve. For accepted signed exact amounts, enrichment may convert units/currencies under pinned rates and rounding; compare by original and converted controls. Filters, fees, allocations, and corrections may intentionally change totals. Encode an expected equation with named components rather than assume input equals output.

At every stage, record input population identity, output population identity, reason counts, rejected records, duplicates, schema, and controls. A later aggregate cannot recover a dropped record's identity. Persist failure samples or full failing rows according to volume/security policy, with deterministic lookup from assertion result.

Conservation does not prove allocation. A corrupt output can subtract 1,000 from account A and add it to B while preserving global total. Compare at the finest critical key, use movement matrices for key/category changes, and include referential/cardinality checks.

### Test joins, filters, windows, and aggregates

For joins, test input uniqueness on the expected side, output multiplicity bounds, unmatched populations, null semantics, validity intervals, and old/new keys. An inner join may silently discard unmatched facts; a left join may preserve them with null attributes that later filters remove. Test the composition.

For filters, create one fixture on each boundary and explain inclusivity. SQL `WHERE predicate` discards both false and unknown; nullable booleans and comparisons need explicit expectations. Check that filters apply at the intended grain and time perspective.

For windows, use complete total order with ties and null placement. Include context rows outside owned output partitions, frame boundaries, sparse dates, session bridges, and partition changes. Compare both per-row values and owned key set.

For aggregates, test empty and all-null groups, duplicate inputs, group-key normalization, exact counts, distinctness, rounding placement, overflow, nonadditive metrics, and floating reduction tolerance. Averages require sum/count; ratios need denominator-zero policy; approximate algorithms need version and error contracts.

For pivots and dynamic schemas, include new/missing categories, ordering, collision after normalization, and column-count limits. A green fixed-column assertion may ignore a novel category routed nowhere.

### Test incremental and mutable-target paths

An incremental model test needs prior trusted target state, a bounded source change interval, and expected final state—not merely expected rows emitted by a select. Some frameworks distinguish the materialization delta from the final merged table; test both semantics deliberately.

Include new insert, update, delete/tombstone, key change, late event, correction, exact duplicate, stale/out-of-order revision, empty interval, lookback overlap, and source epoch change. Verify checkpoint advances only with accepted publication and retry produces no additional effect.

Differentially compare incremental result with a full recomputation over the identical source/reference/code cut. Test destination pruning so an old matching key just outside the scan boundary cannot be misclassified as new. Test schema addition/removal/type change across historical and new rows.

For merge/upsert, verify unique source/target match, all operation branches, tombstone retention, target constraints, transaction isolation, concurrent writers, and ambiguous timeout recovery. Test the actual target engine because merge syntax and semantics vary.

For backfills and restatements, test output ownership versus read context, overlapping units, live-write fencing, candidate completeness, exact before/after/key movement, supersession, consumer version metadata, and rollback/forward repair. A historical execution should not be declared safe because its transformations pass isolated unit tests.

### Test the actual integration boundary

Local doubles should isolate logic, not impersonate every production guarantee. Run a representative suite against the actual SQL engine/version, dataframe runtime, storage format, catalog, object-store conditional behavior, transaction mode, collation/time-zone settings, and identity/permissions.

Verify schemas as the engine sees them after implicit casts and serialization. Round-trip timestamps, decimals, nested structures, nulls, binary/text encodings, and partition values through actual storage. Compare logical values and physical metadata that the contract exposes.

Use dedicated namespaces/accounts/buckets/catalog branches and least-privilege test credentials. Generate unique stable run destinations under an explicit safe prefix; validate targets before cleanup. Never point a destructive test at a mutable production root or infer deletion scope from an unresolved variable.

Test denied permissions and tenant boundaries, not only success. Confirm a stage cannot read another tenant, overwrite raw/trusted data, bypass quarantine, publish without approval, or expose failing sensitive rows. Avoid embedding secret values in fixtures and reports.

Scale matters. A tiny fixture may choose a broadcast join while production shuffles; one partition hides race/order behavior; low cardinality avoids spill; small output never exercises multipart commit. Add representative integration datasets or configurable stress tests while keeping exact manifests and bounded cost.

### Inject failures at commit boundaries

Enumerate durable state transitions: acquire input manifest, write candidate objects, persist stage receipt, validate, write catalog/snapshot metadata, conditionally publish pointer, acknowledge source/progress, notify consumers, and clean obsolete candidates. Inject failure before and after each transition.

For each injection, assert visible state, durable orphan state, retry identity, checkpoint, expected parent, candidate discoverability, reader view, cleanup eligibility, and recovery action. A timeout is an unknown outcome, not proof of rollback. Query the authoritative receipt/pointer before retry.

Inject partial partition write, corrupt/truncated object, missing manifest member, duplicate delivery, worker retry, engine process loss, dependency timeout, quota/disk exhaustion, credential expiry, stale lock/lease, concurrent candidate, parent-version advance, catalog failure, and lost publication/notification acknowledgement.

Readers should see the complete old generation or complete new generation, never a mixture. Attempt reads during publication in the integration environment. Validate snapshot/pointer semantics under real concurrent access rather than assuming atomic rename on an object store.

Recovery tests should prove idempotent retry, deterministic recomputation, orphan quarantine/garbage-collection safety, rollback when permitted, forward repair, and disaster restore. Retain the injected-fault identity and observations. Do not run destructive fault experiments on production without explicit authority and containment.

### Test change and compatibility

Classify a proposed change: refactor with same semantics, bug repair, source/reference correction, schema-compatible extension, breaking contract, engine/runtime migration, or performance-only plan change. Each class has a different expected differential result.

For same-semantics changes, run old and new code over identical immutable cuts and demand declared equivalence. For bug fixes, construct a fixture that fails before and passes after, then characterize historical affected scope. For intentional semantic change, compare all differences, obtain owner approval, version the contract, and retain old/new generations.

Schema contract tests should cover producer-old/consumer-new and producer-new/consumer-old where coexistence is promised. Test added nullable/default fields, removed/renamed fields, type widening/narrowing, nested evolution, unknown enum/category values, and physical partition/schema interaction.

Runtime upgrades need engine-specific differential tests for casts, decimals, timestamps, collation, ordering, UDFs, approximate functions, file readers/writers, query plans, and resource behavior. A clean compile is necessary but not sufficient.

Test selection by dependency/changed columns can accelerate CI, but selection correctness becomes an obligation. Periodically run the full suite and seed changes outside the predicted closure. Missing lineage must widen selection or fail safely, not silently skip affected tests.

### Govern runtime assertions and thresholds

Attach assertions to exact dataset generation, partition, column or cross-dataset scope, code/assertion version, observed/expected values, severity, and outcome. OpenLineage defines dataset quality assertion facets that preserve success separately from severity; this prevents a warning violation from appearing as a pass.

Blocking rules should reflect consequence. Structural corruption, missing expected input, primary-key duplication, failed reconciliation, unauthorized schema, or unverified candidate identity commonly blocks. Distribution deviations may warn, quarantine a segment, or require approval. The data owner—not the framework default—owns the policy.

Thresholds need units, denominator, scope, seasonality, minimum volume, aggregation window, comparator, and version. “Less than 1% null” is incomplete without saying per tenant/day/column, how empty sets behave, and whether known exceptions are excluded.

Waivers are versioned decisions with assertion, scope, reason, owner, evidence, start/expiry, compensating controls, and removal criterion. An unbounded ignore rule converts a detector into documentation of accepted blindness. Alert on expired and accumulating waivers.

If an assertion fails to execute, report error/unavailable separately from a passed zero-failure query. Store failing rows or safe samples with source keys and lineage so operators can reproduce; redact/tokenize sensitive fields and restrict access.

### Measure effectiveness, not volume

Trace every critical contract obligation and known incident class to one or more independent checks. Track escaped defects, detection stage, time to localization, false positives/negatives, flaky/errored/unavailable assertions, runtime/cost, waiver age, full-comparison recency, and recovery exercise results.

Mutation testing challenges whether assertions can detect meaningful faults. Examples include changing `<` to `<=` at a partition boundary, removing a join predicate, switching inner/left join, dropping deduplication, ignoring tombstones, changing rounding, omitting a group key, advancing a checkpoint early, or publishing without expected-parent comparison. Exclude equivalent mutants through review.

For non-equivalent seeded defects set $U$, mutation detection score is

$$
score=\frac{|\{u\in U:\text{suite detects }u\}|}{|U|}.
$$

The score is evidence about this defect set, not general correctness. Analyze surviving mutants: add an oracle, explain irrelevance, or record residual risk. Never optimize the score with unrealistic changes disconnected from real failure modes.

Use production incidents as durable regression fixtures after privacy-safe minimization. Record the original violated obligation and why earlier controls missed it. A test name based only on an incident number ages poorly; name the enduring behavior.

Flaky tests are defects in the evidence system. Classify nondeterministic transformation, unstable fixture, eventual-consistency wait, shared state, resource shortage, clock dependence, or overly strict approximate comparator. Quarantine may temporarily protect the delivery path, but assign owner/expiry and do not count quarantined tests as passing.

### Bind evidence to the candidate and publication

Each test run records source/reference manifests, transformation source and compiled artifact digests, configuration/parameters, schema, runtime/engine, fixture/generator versions, test selection, assertion/oracle versions, candidate output identity, results, failing examples, fingerprints, duration/cost, and operator/automation identity.

OpenLineage quality metrics/assertion facets can transport row/file/column metrics and test outcomes, but emitted metadata must be bound to the exact dataset generation and retained by trustworthy storage. Observability format does not create correctness.

Build into an isolated candidate. Run blocking assertions there. Verify the candidate fingerprint and metadata immediately before conditional publication. Publish only if the current parent equals the expected parent and the evidence bundle names that exact candidate.

After publication, perform safe read-after-publish verification from the consumer path: pointer/catalog resolution, schema, row/key controls, permissions, caches/replicas, and lineage. If this fails, follow predeclared rollback or forward-repair policy; do not silently edit the published generation.

Retain evidence and failing data according to audit, privacy, security, legal-hold, and cost requirements. Test artifacts can contain production-like identifiers and sensitive bad records. Encrypt, isolate tenants, minimize, control access, and honor deletion policy without falsely claiming indefinite replay.

## Definitions and Notation

Let:

- $G=(V,E)$ be the pipeline dataflow graph;
- $C_v$ be the input/output/behavior contract for stage $v$;
- $C_e$ be the compatibility/completeness contract for edge $e$;
- $S_s$ and $R_r$ be immutable source and reference cuts;
- $D$ be code, configuration, schema, engine/runtime, and deterministic environment;
- $F_G(S_s,R_r,D)$ be the intended end-to-end transformation;
- $B$ be stage, edge, end-to-end, publication, and recovery obligations;
- $X$ be data scenarios and boundary/adversarial fixtures;
- $P$ be physical variants such as partitioning, engine plan, concurrency, and order;
- $Z$ be fault, retry, schema/code/reference, and recovery scenarios;
- $Q_b$ be the oracle/comparator for obligation $b$; and
- $E_m$ be the evidence recorded for assurance case $m=(b,x,p,z)$.

The intended evidence matrix is a risk-selected subset

$$
M\subseteq B\times X\times P\times Z.
$$

Coverage function $cov(b)$ records justified cases for obligation $b$; it is not a raw percentage unless the finite universe and weighting are defensible. A critical obligation is uncovered if no case in $M$ exercises it with a capable oracle.

For a linear graph $f_n\circ\cdots\circ f_1$, local contract satisfaction supports composition only when each produced value belongs to the next stage's accepted domain and edge semantics agree:

$$
f_i(x)\models C_{v_i}^{out}
\quad\land\quad
C_{v_i}^{out}\Rightarrow C_{(v_i,v_{i+1})}\Rightarrow C_{v_{i+1}}^{in}.
$$

This implication is an assurance structure, not a claim that tests prove it universally. Branches, quarantines, state, and side effects expand the graph and obligations.

For delivery accounting, define disjoint classified sets $D_{dup}$, $D_{sup}$, and winning assertions $W$ under a fixed source cut and identity/revision policy:

$$
|D|=|D_{dup}|+|D_{sup}|+|W|,
$$

then partition $W=A\uplus Q\uplus R$ into accepted, quarantined, and rejected identities. Counts are valid only when each set uses the declared grain and unclassified/conflict handling is explicit.

For an exact signed measure $m$ transformed by governed conversion $g$, stage conservation may be

$$
\sum_{a\in A}g(m(a))=
\sum_{o\in O}m_O(o)+\sum_{k\in K}adjustment(k),
$$

where the equation includes every intentional fee, allocation, rounding residual, or exclusion. Omitted components turn a control into a false expectation.

A metamorphic relation is a pair of input/output relations $(R_{in},R_{out})$ such that

$$
x\ R_{in}\ x' \Longrightarrow F_G(x)\ R_{out}\ F_G(x').
$$

For example, permutation of an unordered delivery multiset should preserve keyed output; adding an exact duplicate should preserve a deduplicated result. The relation itself must be justified from the business contract.

For a differential test of implementations $F$ and $F'$, compare

$$
F(S_s,R_r,D)\equiv_Q F'(S_s,R_r,D').
$$

An observed mismatch refutes equivalence for that case. Observed equality does not prove either implementation matches the intended specification, especially when dependencies or logic are shared.

For quality assertion $a$, keep observed outcome $o_a\in\{pass,fail,error,skip,unavailable\}$ separate from severity/decision function

$$
decision(a,o_a,context)\in\{block,quarantine,warn,approve\}.
$$

A failure configured as warning remains a detected failure. An assertion error never becomes pass because no failing rows were returned.

## Mechanisms, Invariants, or Proof Structure

Use this assurance chain:

1. **Graph identity.** Establish that the selected stages, edges, source/reference cuts, code/compiled artifacts, and candidate generation match what will publish.
2. **Contract traceability.** Map each critical stage, edge, end-to-end, security, publication, and recovery obligation to a named owner and capable oracle.
3. **Fixture sufficiency.** Cover contract partitions, boundaries, negative forms, interactions, production incidents, and representative scale with explicit expected disposition.
4. **Oracle diversity.** Combine exact/reference results, invariants, controls, differential/metamorphic relations, and governed statistical evidence so no single blind spot dominates.
5. **Execution fidelity.** Exercise pure logic, actual engines/storage/permissions, complete graph composition, runtime candidates, and recovery transitions at proportionate depth.
6. **Stateful-path evidence.** Compare full/incremental/merge/backfill/retry outcomes at the same cut; test prior state, checkpoints, tombstones, and live-write fencing.
7. **Fault and change evidence.** Inject boundary failures and seed realistic semantic defects; verify detection, containment, idempotent recovery, and compatibility decisions.
8. **Publication binding.** Prove blocking evidence names the exact candidate and expected parent; conditionally publish and verify consumer-visible generation.
9. **Lifecycle learning.** Analyze escaped defects, flaky/unavailable checks, waivers, costs, retention, and restore results; revise the enduring obligation set.

The following executable model is a finite reference pipeline and embedded assurance suite. It selects the greatest consistent revision, quarantines unknown currencies, enriches with exact rational conversion, aggregates by account, and checks conservation. It then exercises reorder, duplicate replay, an equal-revision conflict, and a corrupt keyed output whose global total is unchanged. It does not model schemas, distributed engines, storage commits, time, security, statistical thresholds, or production publication.

<!-- bijux-verify: {"id":"multi-stage-batch-assurance-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"accepted=(('e1', 'A', 8000), ('e2', 'A', 12000), ('e3', 'B', 5000))\nquarantine=(('e4', 'unknown_currency'),)\noutput_usd_minor=(('A', 20000), ('B', 5000))\ntotal_usd_minor=25000\nstage_conservation=True\nreordered_stable=True\nduplicate_replay_stable=True\nmasked_total_corruption=True\nkey_oracle_detects_corruption=True\nconflict_detected=True\n","stderr":""}} -->
```python
from fractions import Fraction


def meaning(row):
    return (
        row["event_id"],
        row["revision"],
        row["account"],
        row["currency"],
        row["amount_minor"],
    )


def run_pipeline(deliveries, rates):
    grouped = {}
    for row in deliveries:
        grouped.setdefault(row["event_id"], []).append(row)

    accepted = []
    quarantine = []
    for event_id in sorted(grouped):
        candidates = grouped[event_id]
        revision = max(row["revision"] for row in candidates)
        tied = [row for row in candidates if row["revision"] == revision]
        if len({meaning(row) for row in tied}) != 1:
            raise ValueError(f"conflicting revision for {event_id}")
        winner = tied[0]
        rate = rates.get(winner["currency"])
        if rate is None:
            quarantine.append((event_id, "unknown_currency"))
            continue
        converted = winner["amount_minor"] * rate
        if converted.denominator != 1:
            quarantine.append((event_id, "non_integral_conversion"))
            continue
        accepted.append((event_id, winner["account"], converted.numerator))

    totals = {}
    for _, account, amount in accepted:
        totals[account] = totals.get(account, 0) + amount
    output = tuple(sorted(totals.items()))
    return tuple(accepted), tuple(quarantine), output


rates = {"USD": Fraction(1, 1), "EUR": Fraction(6, 5)}
deliveries = (
    {"event_id": "e1", "revision": 1, "account": "A", "currency": "USD", "amount_minor": 10000},
    {"event_id": "e2", "revision": 1, "account": "A", "currency": "EUR", "amount_minor": 10000},
    {"event_id": "e2", "revision": 1, "account": "A", "currency": "EUR", "amount_minor": 10000},
    {"event_id": "e3", "revision": 1, "account": "B", "currency": "USD", "amount_minor": 5000},
    {"event_id": "e4", "revision": 1, "account": "B", "currency": "GBP", "amount_minor": 1000},
    {"event_id": "e1", "revision": 2, "account": "A", "currency": "USD", "amount_minor": 8000},
)

baseline = run_pipeline(deliveries, rates)
accepted, quarantine, output = baseline
corrupt_output = (("A", 19000), ("B", 6000))
try:
    run_pipeline(
        deliveries
        + (
            {
                "event_id": "e1",
                "revision": 2,
                "account": "A",
                "currency": "USD",
                "amount_minor": 9000,
            },
        ),
        rates,
    )
    conflict = False
except ValueError:
    conflict = True

print(f"accepted={accepted}")
print(f"quarantine={quarantine}")
print(f"output_usd_minor={output}")
print(f"total_usd_minor={sum(amount for _, amount in output)}")
print(
    "stage_conservation="
    f"{sum(amount for _, _, amount in accepted) == sum(amount for _, amount in output)}"
)
print(f"reordered_stable={run_pipeline(tuple(reversed(deliveries)), rates) == baseline}")
print(f"duplicate_replay_stable={run_pipeline(deliveries + deliveries, rates) == baseline}")
print(
    "masked_total_corruption="
    f"{sum(amount for _, amount in corrupt_output) == sum(amount for _, amount in output)}"
)
print(f"key_oracle_detects_corruption={corrupt_output != output}")
print(f"conflict_detected={conflict}")
```

The fixture contains six deliveries. At the delivery grain, one repeated `e2` row is an exact duplicate and `e1` revision 1 is superseded. The four winning event identities split into three accepted and one quarantined. Those are two different conservation equations and should not be mixed.

The EUR rate $6/5$ converts 10,000 minor units to exactly 12,000; accepted stage values sum to 25,000 and account aggregation conserves them. Reversing deliveries and replaying duplicates preserve the result. The conflict fixture adds a different payload at the same maximal revision and fails closed.

The intentionally corrupt aggregate moves 1,000 from A to B. Both correct and corrupt results total 25,000, proving the total-only oracle incapable for this fixture. Exact keyed comparison detects the defect. The example therefore supplies evidence about specific invariants, not every multi-stage behavior.

## Alternatives and Trade-Offs

**Many small stage tests versus fewer end-to-end tests.** Small tests are fast and diagnostic; end-to-end tests expose wiring and composition. Use both, weighted by risk. Replacing either class entirely leaves a distinct blind spot.

**Handwritten fixtures versus generated cases.** Handwritten examples encode domain intent and readable regressions. Property-based generators explore combinations and shrink surprises but require good domains, reproducibility, and review of found cases. Promote important minimized failures into durable named fixtures.

**Exact oracle versus invariant.** Exact rows detect subtle differences but are costly to author/maintain at scale. Invariants generalize but permit many wrong outputs. Combine exact small models with broad invariants and production reconciliation.

**Golden snapshot versus independent reference.** Goldens cover large structured results cheaply after creation but can fossilize mistakes or be refreshed blindly. Independent references explain expected semantics but also need maintenance. Require readable diffs and owner approval for either change.

**Mocked dependency versus real integration.** A mock gives speed, deterministic errors, and isolation; it cannot establish engine/storage/permission behavior. Contract-test the double itself and retain a representative real-boundary suite.

**Full comparison versus fingerprints/sampling.** Full keyed comparison gives strongest population evidence at high scan cost. Hierarchical fingerprints localize cheaply if canonical projection is complete. Sampling estimates only sampled properties and must expose confidence/selection limitations.

**Block versus quarantine versus warn.** Blocking protects consumers but can harm freshness; quarantine preserves valid portions but complicates completeness; warning preserves availability but exposes risk. Map severity to domain impact, scope, and compensating evidence, with explicit waivers.

**Production shadow versus staging.** Staging enables controlled faults and isolation but may differ in scale/configuration. Shadow candidates use real inputs/environment but increase cost and require strict write isolation. Neither should be mistaken for consumer-visible production proof.

**Pin old runtime versus test migration.** Pinning supports historical replay but accumulates security/support burden. Migration testing compares new semantics and performance deliberately. Retain a bounded reproducibility horizon and an approved transition plan.

**Test selection versus full suite.** Dependency-aware selection shortens feedback and cost; incomplete lineage can skip impacted checks. Widen on uncertainty and periodically run the complete suite to evaluate selector recall.

**Synthetic data versus masked production subset.** Synthetic fixtures give exact intent and lower privacy risk but miss emergent distributions. Approved masked subsets add realism but may leak or break relationships. Use layered, governed data with clear limitations.

**Rollback versus forward repair.** Immutable-generation pointer rollback is fast when contracts and downstream effects permit it. Some corrections, external exports, or schema changes require forward repair. Test the actual chosen policy and notification consequences.

## Failure Modes and Misconceptions

1. **“The job succeeded, so the data is correct.”** Process completion and dataset acceptance are separate outcomes.
2. **“A final row count is enough.”** Count equality permits wrong keys, values, duplicates offset by omissions, and group movement.
3. **“Unit tests prove the pipeline.”** They isolate logic but not graph wiring, engine behavior, storage, permissions, or publication.
4. **“End-to-end tests make stage assertions redundant.”** A final failure can be hard to localize, and lossy upstream decisions may still yield plausible output.
5. **“A production sample is a test fixture.”** Without governed cut and oracle, it is merely input.
6. **“The current output can be the expected output.”** This encodes existing corruption and makes regression self-referential.
7. **“Refresh the golden after every intended change.”** Review exact differences and separate intended semantics from unexplained drift.
8. **“Zero failing rows means pass.”** Query execution error, wrong dataset, empty unintended scope, or skipped assertion must not masquerade as zero violations.
9. **“Warnings passed.”** Success/failure of the assertion and severity/decision are independent.
10. **“Mocks are safer and therefore sufficient.”** They omit the very boundary semantics many data failures inhabit.
11. **“Random generation covers edge cases automatically.”** Generator domains/distributions can avoid critical boundaries; name and force them.
12. **“A single engine mode is representative.”** Partition count, join plan, spill, retry, ordering, and scale can change behavior.
13. **“Global conservation proves correctness.”** Offsetting key/category/currency movements can preserve totals.
14. **“Quarantine is outside the pipeline.”** It is a governed output requiring identity, reason, durability, replay, security, and reconciliation.
15. **“Incremental tests need only the new rows.”** Prior state, deletes, merges, checkpoint, and final-table semantics determine correctness.
16. **“Retry testing means rerun after a clean failure.”** Inject ambiguous outcomes and partial durable state, then reconcile before retry.
17. **“Staging equals production.”** Configuration, permissions, data scale, concurrency, topology, and services may differ; record parity gaps.
18. **“A hash makes comparison complete.”** Only a complete canonical projection and appropriate collision assumption support that claim.
19. **“More tests mean more assurance.”** Duplicated weak checks can leave one critical obligation uncovered.
20. **“Testing proves future correctness.”** Evidence is scoped to cases, versions, data cuts, environments, and oracles; monitoring and revalidation remain necessary.

## Worked Examples

### Example 1

A parser converts invalid empty amount to zero. A downstream not-null test passes, and total deviation is small. A parser-stage fixture expects invalid amount in quarantine with raw lineage, catching the earliest semantic loss.

### Example 2

An orders-to-customer join expects one customer version valid at each order time. Fixture includes overlapping versions and proves the stage fails cardinality rather than doubling revenue. A final total-only check would detect inflation but not explain the interval defect.

### Example 3

A range processes `[2026-08-01,2026-09-01)`. Fixtures at exactly both boundaries prove August 1 is included and September 1 excluded at source precision. A mutation changing `< end` to `<= end` must be detected.

### Example 4

An incremental interval contains insert, correction with old event time, delete tombstone, and duplicate delivery. Expected final keyed table is compared to a full rebuild at the same log/reference cut; checkpoint advances only after candidate publication.

### Example 5

Two account outputs differ by −1,000 and +1,000. Global total and row count remain equal. Keyed exact comparison and a before/after movement matrix identify the misallocation and its source lineage.

### Example 6

A worker writes four of five partition objects and crashes before manifest publication. Readers retain the old generation. Retry reuses the logical candidate identity, verifies existing object digests, writes the missing object, validates the full manifest, then conditionally publishes once.

### Example 7

A property generator creates lists of exact delivery duplicates and randomizes order. Metamorphic oracle requires stable deduplicated keyed output. The smallest counterexample reveals winner selection used first arrival rather than authoritative revision.

### Example 8

An engine upgrade changes decimal division scale. Old/new differential run over a pinned cut finds 37 keyed differences. Owners classify them as an intentional contract migration, approve rounding, add boundary fixtures, and publish a new version instead of updating the golden blindly.

### Example 9

A null-rate threshold is 1% globally, but one small tenant has 80% null while large tenants dilute it below 1%. Segment-level assertion with minimum-volume and critical-tenant policy blocks only the affected candidate scope and preserves explicit completeness status.

### Example 10

Publication response is lost. The harness queries the generation pointer and receipt: the tested candidate is already current. It records success and retries notification with a stable idempotency identity, rather than publishing a second generation or rolling back by assumption.

## Cross-Program Connections

- **Testing & Quality Engineering:** test levels, oracle design, property-based/metamorphic/differential/mutation testing, coverage, flakiness, and evidence quality underpin the assurance matrix.
- **Programming Languages & Semantics:** compositional reasoning, purity, equivalence, undefined/implementation-dependent behavior, and counterexamples clarify what a test can establish.
- **Algorithm Engineering:** boundary partitions, generators/shrinking, exact comparison, hashing, numerical stability, and complexity shape effective data tests.
- **Database Engineering:** isolation, constraints, SQL null/order semantics, query plans, transactions, temporal state, merge behavior, and catalog publication require real-engine integration.
- **Distributed Systems Engineering:** retries, duplicate delivery, partial writes, leases, concurrent publishers, ambiguous outcomes, atomic visibility, and recovery drive fault injection.
- **Software Delivery & Reliability Engineering:** immutable artifacts, CI selection, staging, canary/shadow validation, provenance, rollback, and change classification bind tests to releases.
- **API & Service Engineering:** external-response contracts, idempotency, schema compatibility, mocks, error injection, and consumer notification appear at pipeline boundaries.
- **Platform Engineering:** isolated environments, runtime parity, permissions, workload scale, telemetry, resource budgets, and recovery facilities make assurance executable.
- **Security Engineering:** test-data minimization, tenant isolation, secret hygiene, authorization negatives, diagnostic access, retention, and safe fault containment are essential.
- **Systems Engineering:** assurance cases, requirement traceability, risk-weighted verification, configuration baselines, acceptance authority, and residual risk prevent test-count theater.

## References

1. dbt Labs, [Add Data Tests to Your DAG](https://docs.getdbt.com/docs/build/data-tests). Documents reusable and custom assertions over sources/models, failing-row query semantics, built-in uniqueness/null/value/reference checks, severity, and stored failures. Accessed 2026-09-02.
2. dbt Labs, [Unit Tests](https://docs.getdbt.com/docs/build/unit-tests). Documents small static-input SQL model tests before materialization, complex-logic/edge-case uses, adapter limitations, and incremental modes. Accessed 2026-09-02.
3. Apache Beam, [Test Your Pipeline](https://beam.apache.org/documentation/pipelines/test-your-pipeline/). Documents testing individual functions, transforms, and complete pipelines using known static inputs, expected collections, `TestPipeline`, and `PAssert`. Accessed 2026-09-02.
4. Apache Spark, [Testing PySpark](https://spark.apache.org/docs/latest/api/python/getting_started/testing_pyspark.html). Documents built-in dataframe/schema assertion utilities, approximate comparison parameters, and integration with test frameworks. Accessed 2026-09-02.
5. Great Expectations, [Define Expectations](https://docs.greatexpectations.io/docs/core/define_expectations/). Defines Expectations as verifiable assertions and suites as collections describing ideal dataset state. Accessed 2026-09-02.
6. Hypothesis, [Hypothesis Documentation](https://hypothesis.readthedocs.io/en/latest/). Describes property-based tests over generated ranges, edge-case exploration, failure replay, strategies, settings, and stateful testing. Accessed 2026-09-02.
7. OpenLineage, [Data Quality Assertions Facet](https://openlineage.io/docs/spec/facets/dataset-facets/data_quality_assertions/). Defines dataset-bound assertion outcome, expected/actual/body/parameters, and independent success versus severity fields. Accessed 2026-09-02.
8. OpenLineage, [Data Quality Metrics Facet](https://openlineage.io/docs/spec/facets/dataset-facets/data_quality_metrics/). Defines dataset row/file/byte and column metric fields for lineage events. Accessed 2026-09-02.
9. E. Breck, N. Polyzotis, S. Roy, S. E. Whang, and M. Zinkevich, [Data Validation for Machine Learning](https://proceedings.mlsys.org/paper_files/paper/2019/file/928f1160e52192e3e0017fb63ab65391-Paper.pdf), SysML 2019. Presents a production data-validation system and motivates treating pipeline data as a production asset. Accessed 2026-09-02.
10. Apache Airflow, [Best Practices: Testing a Dag](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#testing-a-dag). Documents loader/structure/operator tests, self-checks, staging, dependency/environment parity, and mocked variables/connections. Accessed 2026-09-02.

## Exercises

### Exercise 1

A pipeline receives 12 deliveries representing 9 logical events: two exact redeliveries and one superseded revision are present. Of the 9 winning assertions, 7 are accepted, 1 is quarantined, and 1 is rejected by authorized policy. State both conservation equations, explain their grains, and name evidence needed to prove the classifications.

### Exercise 2

A correct output has `(north=400,south=600)`. A defect yields `(north=450,south=550)`. Row count and global total both match. Design a minimum oracle set that detects and localizes the defect without merely copying production logic.

### Exercise 3

An incremental daily pipeline updates orders, joins valid-time customer regions, and writes tenant/day partitions. Design fixtures and comparisons for an order correction that changes customer, event day, and amount after the original period was published. Include prior state, affected closure, full-refresh oracle, quarantine, and publication.

### Exercise 4

Candidate generation `g8` has written all objects and passed tests when publication times out. Concurrent generation `g9` may have advanced the pointer. Describe fault-injection assertions and recovery for each authoritative state: `g8` current, old parent current, or `g9` current.

### Exercise 5

Create a risk-based assurance matrix for a three-stage `decode → enrich → aggregate` pipeline. Include at least four data scenarios, three physical variants, three failures/changes, oracle assignments, severity decisions, mutation checks, evidence binding, and one explicitly deferred risk.

## Answers to the Exercises

### Answer 1

At delivery grain, $12=2\ exact\ duplicates+1\ superseded+9\ winning\ assertions$. At winning logical-event grain, $9=7\ accepted+1\ quarantined+1\ rejected$. The equations cannot be collapsed without labeling categories because duplicates/superseded entries are deliveries while the second equation partitions winning identities. Evidence includes immutable delivery manifest/coordinates, event and assertion identities, payload digests, source revision/authority/order, exact-duplicate rule, winner/conflict rule, stage receipts linking every delivery to disposition, quarantine/rejection reason and policy version, and set-level reconciliation proving disjointness and completeness.

### Answer 2

Use an exact keyed expected map `{north:400,south:600}` derived from a small independently reasoned fixture; it immediately detects both ±50 differences. Add source-to-group membership or a movement ledger so the divergent event IDs can be traced to their expected region, plus per-region accepted-input control sums under the same reference cut. Assert global conservation as a complementary invariant, not the decisive oracle. If production code joins country to region, make the reference oracle a simple literal mapping/hand calculation rather than copying the same join/helper. Compare schema, unique group keys, exact values, and unexpected/missing keys; retain divergent keys and provenance.

### Answer 3

Fixture includes immutable original and correction assertions with stable occurrence/revision identity, source positions, before/after customer/day/amount, both customers' valid-time region versions at event times, and prior published target/checkpoint. Test exact redelivery, stale revision, missing/overlapping region, and equal-revision conflict. Affected closure includes old and new tenant/day partitions, old/new customers and regions, aggregates/windows influenced by both days, downstream caches/reports, and prior/current output versions. Run incremental correction into an isolated candidate and independently full-recompute the same closure from the identical source/reference/code cut; compare exact keyed rows, deletes, group movements, amounts, quarantine, schema, and controls. Verify original partition loses the old effect, new partition gains corrected effect once, checkpoint advances only with a conditionally published new generation, prior version remains reproducible, and consumer supersession metadata is emitted idempotently.

### Answer 4

Inject timeout after the publication request and withhold its acknowledgement. Query the authoritative pointer/history and operation receipt by stable generation/publication identity. If `g8` is current, adopt success, verify its tested fingerprint/metadata from the consumer path, and retry only idempotent downstream notification. If the old expected parent remains current and no committed receipt exists, retry the same conditional publish of `g8`; if a receipt is indeterminate, continue reconciliation rather than creating a new identity. If `g9` is current, `g8` must not overwrite it: mark/supersede the stale candidate, compare whether its intent is already included, and rebase/recompute against `g9` if still required. Assertions cover one visible complete generation, no mixed objects, unchanged checkpoint until the corresponding commit, safe orphan retention/cleanup, and exact evidence binding.

### Answer 5

Data scenarios can include normal exact rows; null/invalid encoding sent to quarantine; duplicate/stale/equal-revision conflict; missing/duplicate reference; numeric rounding/overflow; and empty/skewed partitions. Physical variants include reversed/file-repacked input, one versus many partitions/workers, and serial versus production join/reduction plans. Failure/change scenarios include partial candidate write plus retry, lost publication acknowledgement with concurrent writer, and schema/reference/runtime upgrade; add resource exhaustion if impact warrants. Use exact rows for small decode/enrich fixtures, schema/uniqueness/referential checks at edges, source and disposition conservation, keyed aggregate controls, permutation/duplicate metamorphic relations, and full-versus-incremental or old-versus-new differentials. Block corrupt schema, identity conflict, missing expected input, failed exact reconciliation, or stale publication; quarantine row-local invalidity under completeness policy; warn on governed distribution drift. Seed mutations that skip quarantine, remove a join predicate, alter a boundary/rounding rule, omit a group key, or publish without expected-parent comparison. Bind source/reference manifests, compiled code, environment, oracle versions, candidate fingerprint, outcomes, failures, and publication receipt. A defensible deferred risk might be cross-architecture floating-point portability when this pipeline uses exact minor units except one noncritical approximate metric; record owner, impact, comparator, compensating monitoring, review date, and conditions that trigger a dedicated test.
