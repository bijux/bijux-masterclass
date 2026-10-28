---
module_id: DE-079
program: Data Engineering
level: 2
module_number: 79
title: Root-Cause Analysis with Lineage
status: complete
last_verified: 2026-09-03
---

# Root-Cause Analysis with Lineage

## One-Page Review

### Governing question

How can investigators use dataset-, field-, run-, and version-level lineage to narrow candidate causes and affected consumers, then build reproducible causal evidence without mistaking graph reachability, temporal correlation, a recent deployment, or a successful repair for proof of one unique root cause?

### Essential definitions

- **Lineage** represents declared, observed, or inferred dependencies among data entities, processing activities/jobs, agents, fields, and versions.
- **Provenance** records how a particular entity/version was generated, derived, attributed, used, or influenced by activities and agents.
- **Declared lineage** describes intended dependencies; **observed lineage** is emitted from an actual run; **inferred lineage** is reconstructed and carries uncertainty.
- A **lineage edge** is a dependency claim with source, target, type, scope, collection method, time/version, confidence, and provenance.
- **Dataset-level lineage** connects products/tables/topics/files; **field-level lineage** connects attributes and transformation roles.
- A **backward slice** traverses ancestors of an affected node to find candidate inputs, jobs, code, configuration, and references.
- A **forward slice** traverses descendants from a suspected node to bound potentially affected products and consumers.
- A **runtime instance graph** binds abstract lineage to actual data snapshots, run IDs, code/config/reference versions, partitions, and times.
- A **symptom** is observed wrong behavior; a **proximate failure** is the immediate mechanism producing it.
- A **causal factor** is a condition whose change/removal would have prevented or altered the incident under the stated context.
- A **contributing condition** increases likelihood or impact without being sufficient alone; a **latent control weakness** allowed creation, escape, or propagation.
- A **hypothesis** predicts additional observations; a **disconfirming test** seeks evidence that would refute it.
- **Differential replay** holds most inputs constant while changing one candidate input/code/config/reference version and compares outputs.
- A **counterfactual substitution** asks whether replacing one candidate with its known-good version removes the defect under a pinned experiment.
- A **root-cause record** links evidence, experiments, confidence, alternative explanations, contributing factors, control gaps, corrective actions, and verification.

### Central model, mechanism, or theorem

Let runtime lineage graph $G_t=(V_t,E_t)$ bind concrete versions. For symptom node $y$, candidate ancestors are

$$
Cand(y)=Ancestors_{G_t}(y).
$$

This is a search-space reduction, not a causal conclusion. For candidate $x$, a controlled counterfactual experiment compares

$$
Y_{bad}=F(X_{-x},x_{bad}),\qquad Y_{good}=F(X_{-x},x_{good}).
$$

If the defect disappears only under qualified substitution of $x$, causal support increases, subject to fidelity, interaction, and path-dependence limits. A lineage graph with inputs `orders_source` and `pricing_reference` feeding `revenue_model` makes both ancestors candidates. Only replacing the faulty pricing reference repairs the output; reachability alone cannot select it.

### Critical invariants

- Every graph node and edge uses stable identity plus data/run/code/config/reference/schema/contract versions and effective times.
- Declared, observed, parsed/inferred, manually curated, and unknown lineage remain distinguishable with collection provenance and confidence.
- Dataset, field, row/key/cohort, control-flow, reference, policy, and serving dependencies are not collapsed into one generic edge.
- Backward lineage proposes candidates; forward lineage proposes possible impact; runtime and consumer evidence confirm actual use.
- Investigation begins from a reproducible symptom and expected-versus-observed contract, not from a favored recent change.
- Hypotheses record predictions, tests, results, and disconfirming evidence; negative results remain in the incident record.
- Experiments pin inputs, code, configuration, references, engine, environment, seeds/clocks where relevant, and output comparator.
- Correlation, temporal precedence, reachability, repair success, and owner intuition are labeled evidence, not universal causal proof.
- Multiple causal factors, interactions, path dependence, and latent conditions remain representable; one “root” is not forced for narrative simplicity.
- Lineage gaps, stale edges, dynamic SQL, UDFs, external systems, exports, manual edits, caches, models, and decisions are explicit unknowns.
- Field-level impact distinguishes direct value derivation from indirect filter/join/group/order/control influence.
- Containment and recovery can proceed before complete root-cause proof, while preserving evidence and experiment safety.
- Corrective actions address creation, escape/detection, propagation/containment, and recovery weaknesses—not only the proximate bad value.
- The repaired version is independently reconciled and downstream consumers are verified; the original failure is immutable.
- Postmortem claims cite evidence strength, alternatives, reviewers, owners, deadlines, and recurrence measures.

### Common failures

Common failures include treating a catalog graph as exact runtime truth; using names instead of stable identities; ignoring versions and partitions; calling every ancestor a cause; blaming the most recent deployment; stopping at “bad source data”; assuming one root cause; overlooking reference/config/policy changes; treating field lineage as direct when it only filtered rows; ignoring UDF/dynamic SQL opacity; following declared lineage after an untracked export; editing data before replay capture; changing multiple variables in one experiment; testing only confirming cases; discarding negative results; declaring cause because rollback helped; repairing the symptom without explaining escape; and generating action items that say only “be more careful.”

### Compact example

`orders_source` and `pricing_reference` both feed `revenue_model`, whose output should be 100 but is 200. Backward lineage returns all three upstream candidates. Replaying with the same orders and good reference rate changes 200 to 100; replaying with the known-good orders version but retaining the bad rate remains 200. The evidence supports the pricing reference as the proximate causal input for this fixture, while separate analysis asks why the bad reference was published, why contract tests missed it, and which descendants consumed it.

### Connections

[DE-030](030-designing-replayable-raw-ingestion.md) preserves reproducible inputs, [DE-049](049-run-metadata-and-operational-state.md) binds runs, [DE-060](060-handling-late-duplicate-and-out-of-order-events.md) explains path-dependent disorder, [DE-066](066-time-travel-and-reproducible-reads.md) pins versions, [DE-073](073-reconciliation-tests.md) supplies differential evidence, [DE-076](076-data-contracts.md) defines expected behavior, [DE-077](077-producer-and-consumer-responsibilities.md) assigns action ownership, and [DE-078](078-data-incident-detection-and-triage.md) supplies the incident/evidence handoff. DE-080 converts lessons into gates.

## Governing Question

Lineage is often sold as an answer graph: click the red table, see the upstream source, and find the cause. Real systems are less cooperative. A dataset can have many ancestors, only one affected partition, multiple code and reference versions, inferred edges, invisible exports, and consumer-local transformations.

The graph is still powerful. It turns unbounded search into structured hypotheses, supports backward candidate discovery and forward impact analysis, and joins evidence around stable versions. Its value depends on identity, runtime fidelity, field/control semantics, and honest gaps.

Root-cause analysis is a causal investigation, not a traversal. Investigators specify expected behavior, reproduce the symptom, generate competing hypotheses, predict observations, test them under pinned conditions, retain negative evidence, and update confidence. Sometimes the strongest support remains “probable contributing factors,” not one definitive cause.

The governing requirement is a versioned evidence graph plus disciplined experiments that explain creation, escape, propagation, and recovery. The output must support durable controls rather than a convenient person or component to blame.

## Why This Matters

Data defects propagate silently. A wrong reference rate can alter thousands of aggregates, features, reports, and decisions while all jobs succeed. Lineage finds the shared ancestor and bounds consumers faster than manual repository and warehouse searches.

Weak lineage can mislead more efficiently than no lineage. A declared edge may not have run; a table name may refer to a newer snapshot; a column mapping may omit filter influence; a dashboard export may sever observation. Confidence and provenance must travel with the graph.

Premature causal stories produce fragile fixes. Rolling back the latest release may coincide with source recovery. Replacing an input may also invalidate caches. A rerun may pass because time/reference state changed. Controlled replay distinguishes hypotheses and exposes interactions.

“Root cause” language can encourage a single stopping point. Complex incidents commonly include a triggering defect, permissive interface, missing test, incomplete monitor, slow containment, and unsafe recovery path. Corrective action should reduce recurrence and impact across layers.

Lineage and evidence can reveal sensitive fields, systems, owners, queries, and consumer behavior. Access, minimization, masking, retention, and secure investigation environments remain necessary.

## Prerequisites and Retrieval

Retrieve incident: ID, symptom, expected contract, affected/safe versions/cohorts/intervals, impact, timeline, containment, live record, evidence inventory, hypotheses, and owners.

Retrieve graph: dataset/job/field/agent stable IDs, edge types, direction, source, declared/observed/inferred status, confidence, collection time, version scope, transformations, masking, and known gaps.

Retrieve runtime: source/target snapshots, run IDs, manifests, partitions, offsets/checkpoints, code commit/image, config/feature flags, reference/master versions, schema/contract, engine/library, environment, clocks, and publish/serve versions.

Retrieve changes: deployments, schema/contracts, source systems, reference data, permissions, infrastructure, schedules, dependencies, manual corrections, experiments, and effective intervals.

Retrieve data evidence: quality/reconciliation/freshness/volume results, row/key/cohort differences, output statistics, logs/traces/metrics, query plans, errors, and unaffected controls.

Retrieve consumers: runtime reads, query/subscription/access evidence, caches, exports, models, reports, decisions, criticality, owner acknowledgment, and off-platform lineage.

Retrieve experiment capability: immutable input versions, replay environment, deterministic seeds/clocks, old/new artifacts, comparator, privacy controls, cost, side-effect isolation, and review.

Retrieve control history: intended gates, actual coverage, test mutations, waivers, alerts, response timeline, rollback, correction, and prior similar incidents.

Distinguish intended from observed lineage; logical dataset from version; ancestor from causal factor; direct value transformation from control influence; proximate failure from latent condition; trigger from root/contributing cause; repair from proof; temporal correlation from counterfactual evidence; missing edge from no dependency; and human error from system conditions enabling escape.

Create an investigation record:

| Concern | Required evidence and decision |
|---|---|
| Symptom | Falsifiable expected/observed result, pinned versions, comparator |
| Graph | Stable nodes/edges, type, runtime scope, source, confidence and gaps |
| Candidates | Backward slice prioritized by changes, anomalies and mechanisms |
| Impact | Forward slice confirmed by runtime reads, exports and consumers |
| Hypotheses | Predicted observations, falsifiers, test owner and status |
| Experiments | Pinned factors, substitution, environment, output and limitations |
| Causality | Supported factors, interactions, alternatives and confidence |
| Controls | Creation, escape, propagation and recovery gaps |
| Actions | Correction/prevention/detection/containment owners, dates and proof |

Write a falsifiable claim: “For incident DI-42 symptom S on product P/V81, observed run lineage G17 binds source O/V9 and pricing reference R/V6 through revenue-model commit M8/config C3 to output V81; replay E4 reproduces S, substituting R/V5 alone removes S while substituting O/V8 does not, mutation E7 reintroduces S, unaffected cohorts remain stable, forward runtime evidence confirms consumers U2/U5, and the record separately identifies R publication validation, contract coverage, and containment gaps with confidence and alternative explanations.”

## Learning Objectives

After completing this module, you should be able to:

1. distinguish lineage, provenance, declared/observed/inferred edges, and runtime instance graphs;
2. model stable dataset/job/field/agent identities with versions, times, edge types, and confidence;
3. use backward slicing to generate candidate causes and forward slicing to propose impact;
4. distinguish graph reachability and temporal correlation from causal evidence;
5. define reproducible symptoms, competing hypotheses, predictions, falsifiers, and negative results;
6. design differential replay and counterfactual substitution with pinned factors and safe comparators;
7. reason about multiple factors, interactions, path dependence, and incomplete observability;
8. confirm field-level direct and indirect dependencies plus off-platform consumers;
9. turn findings into correction, prevention, detection, containment, and recovery controls; and
10. write evidence-linked, reviewed, blameless root-cause records with verifiable actions.

## Core Exposition

### Build a trustworthy runtime lineage graph

Use stable namespaces and IDs for systems, datasets, jobs, fields, and agents. Friendly names and physical locations change. Every runtime node binds an actual snapshot/version, and every activity binds run, code, configuration, reference, engine, environment, and time.

Type edges. A value may be directly copied, transformed, aggregated, masked, filtered by another field, joined on a key, ordered/limited, generated from reference/config, or merely co-read. Dataset-level input/output edges cannot express all field influence.

Record edge provenance: emitted by runtime integration, parsed from SQL, declared in code, inferred from access, or manually curated. Include collector/version, event/run, collection time, scope, and confidence. Merge conflicts visibly rather than choosing an unlabeled truth.

Continuously measure lineage coverage. Dynamic SQL, stored procedures, UDFs, notebooks, APIs, files, manual uploads, caches, exports, and models create blind spots. Unknown lineage is a triage input, not an empty graph.

### Start from a reproducible symptom

Translate the incident into a comparator: exact missing keys, wrong aggregate, schema/contract failure, freshness frontier, distribution change, unauthorized field, or consumer decision. Pin bad version and a known-good/expected reference when available.

Reproduce with immutable inputs before searching for causes. If the symptom no longer reproduces, investigate moving references, nondeterminism, clock/timezone, late data, cache, environment, and incomplete capture. Record that uncertainty.

Establish earliest affected and latest known-good versions by binary search or cohort/time comparison where feasible. Diff data, schema, code, configuration, reference, infrastructure, and permissions across the boundary.

Do not anchor on the latest deployment. List all relevant changes and “no change” evidence, including upstream behavior and manual operations.

### Slice lineage to generate hypotheses

Backward traverse from the exact output field/cohort/version. Stop at boundaries with sufficient independent evidence or known-good controls. Rank candidates by mechanism plausibility, correlated anomaly/change, temporal/version alignment, edge confidence, and ease/safety of falsification.

Include non-data dependencies: code, configuration, feature flags, reference/master data, schema/contract, secrets/permissions, engine/runtime, timezone/calendar, and manual actions. A table-only graph misses frequent causes.

Forward traverse from each supported suspect to possible descendants. Intersect with actual run/read/access versions and incident time. Contact critical/off-platform consumers. A descendant is potentially affected until its own evidence confirms or rejects impact.

Create multiple hypotheses. For each, state mechanism, predicted differences, unaffected observations it explains, observations that would contradict it, experiment, owner, and current confidence. Prioritize cheap discriminating tests over broad data dumps.

### Test hypotheses with pinned experiments

Compare observed state against mechanism predictions first. A wrong currency reference predicts changes only for matching currency/effective dates, not all values. A duplicate replay predicts key multiplicity and offset patterns. Disconfirming cohorts are valuable.

Use differential replay: same inputs with old/new code; same code with old/new reference; same source with old/new config; bad versus good partition. Change one factor when possible and compare exact keys/rows/aggregates plus unaffected controls.

Counterfactual substitution supports causality only if the replacement is faithful and no coupled state changes. Document environment differences, caches, external calls, nondeterminism, seeds, clocks, and sample coverage. Production experiments need containment and approval.

Use positive reproduction and negative controls. Reintroducing the candidate defect should reproduce the symptom; replacing unrelated candidates should not fix it. Retain negative results so other responders do not repeat work and postmortems show alternatives considered.

### Reason about causality carefully

Temporal precedence is necessary for many causes but insufficient. Correlated changes may share a third cause. Lineage reachability says influence is possible, not that this version/field caused this symptom. A repair may change several factors or merely coincide with recovery.

Prefer mechanism plus interventions: explain how candidate state flows through transformations to the observed value, demonstrate version/time alignment, predict scope, reproduce, substitute, and validate. State confidence and limits when full reproduction is unsafe or impossible.

Represent multiple sufficient or jointly necessary factors. A malformed record plus parser bug plus disabled quarantine may jointly cause failure. Path-dependent state can require a specific event order. “Root cause: bad data” omits why it entered, escaped, and propagated.

Distinguish trigger/proximate defect, contributing conditions, latent organizational/control weaknesses, detection gaps, containment gaps, and recovery gaps. Avoid infinite regress; stop where actionable system boundaries and accountable controls are clear.

### Validate impact and correction

Use forward lineage to enumerate potential descendants, then query actual version use and consumer outcomes. Column lineage narrows fields, but indirect filter/join/group/order influence can affect rows without direct value derivation.

Track exports, caches, feature stores, notebooks, manually downloaded files, and decisions beyond automated lineage. Ask owners to acknowledge affected/safe state. Record discovery coverage.

Correction publishes a new version with provenance; it does not overwrite the bad one. Reconcile corrected source-to-target output, rerun contract/quality/freshness, compare unaffected controls, and ensure checkpoints/late updates are sound.

Critical consumers invalidate/replay/rebuild and validate their outcomes. A causal claim gains support when predicted correction removes the symptom across affected scope without unexplained collateral changes, but long-term recurrence tests remain necessary.

### Convert findings into durable controls

Actions span creation prevention, escape detection, propagation containment, and recovery. Validate reference publication; add semantic contract fixtures; enforce version binding; monitor cohort reconciliation; make lineage coverage fail visible; add a targeted kill switch; rehearse replay.

Each action has an accountable owner, concrete artifact/change, priority, due date, verification method, and completion evidence. “Improve monitoring,” “add tests,” and “be careful” are not verifiable.

Prioritize systemic leverage and match the supported cause. A test for this exact row may prevent recurrence only narrowly. A typed unit contract and reference activation gate may remove the entire failure class.

Review completed actions and mutate the control to ensure it catches the incident fixture. Monitor recurrence and near misses. Update lineage collectors and contracts when the investigation found blind spots.

### Write and review the root-cause record

Include executive impact, precise timeline, symptom, architecture/runtime graph, evidence inventory, hypotheses and negative tests, causal/contributing/control findings, containment/recovery, consumer impact, actions, and lessons. Link protected evidence rather than copying sensitive rows.

Use blameless language focused on conditions, incentives, interfaces, and controls. Human action can be causal evidence, but “operator error” is not an adequate stopping point if the system permitted irreversible unsafe action without detection.

Separate facts, inferences, and counterfactual claims. Name confidence and alternatives. Peer reviewers challenge depth, experimental validity, consumer scope, and whether actions would have prevented or reduced the incident.

Preserve the graph and record as versioned artifacts. Search across incidents for repeated components, controls, change types, blind spots, and action effectiveness.

## Definitions and Notation

Let:

- $G_t=(V_t,E_t)$ be a lineage/provenance graph instantiated for incident time/version scope $t$;
- $y\in V_t$ be the symptom output node/version;
- $A(y)$ and $D(x)$ be ancestors of $y$ and descendants of candidate $x$;
- $m(e)$ be edge metadata: type, source, run/version scope, collector, confidence;
- $X=(x_1,\ldots,x_n)$ be pinned causal factors supplied to transformation $F$;
- $\phi(Y)$ be the defect predicate over output $Y=F(X)$;
- $do(x_j\leftarrow x_j')$ denote a controlled substitution in an investigation model; and
- $E_x^+,E_x^-$ be supporting and disconfirming evidence for hypothesis $x$.

Candidate generation is

$$
Cand(y)=\{x\in A(y):VersionAligned(x,y)\land EdgeUsable(x\leadsto y)\}.
$$

A successful intervention pattern is

$$
\phi(F(X_{-j},x_j^{bad}))=true,\qquad
\phi(F(X_{-j},x_j^{good}))=false.
$$

This increases support for $x_j$ under experiment fidelity; it does not prove absence of interactions, upstream causes of $x_j$, or alternative sufficient factors. Impact candidates are $D(x_j)$ intersected with compatible runtime versions and the incident interval.

## Mechanisms, Invariants, or Proof Structure

Proof sketch that lineage reachability does not identify a unique cause:

1. Let `orders_source` and `pricing_reference` both feed `revenue_model`, which produces the erroneous report.
2. Backward lineage therefore marks both inputs and the model activity as candidate ancestors.
3. With orders amount 100 and faulty rate 2, output is 200 rather than expected 100.
4. Replacing `orders_source` with its known-good but identical version leaves output 200.
5. Replacing `pricing_reference` rate 2 with known-good rate 1 changes output to 100.
6. Both inputs are graph-reachable, but only the reference substitution repairs this controlled fixture.
7. Therefore reachability reduces the candidate set but does not uniquely determine cause.

The counterexample supports a proximate causal-input claim under the fixture. It does not explain why the reference became wrong, prove every production row, or rule out additional factors.

The executable reproduces backward candidates and the differential substitutions. It is a teaching abstraction, not a lineage collector, causal-inference engine, query planner, replay system, or universal root-cause proof.

<!-- bijux-verify: {"id":"lineage-guided-counterfactual","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"lineage_candidates=('orders_source', 'pricing_reference', 'revenue_model')\nlineage_identifies_unique_cause=False\nobserved_revenue=200\nreplace_orders_source_repairs=False\nreplace_pricing_reference_repairs=True\nsupported_root_cause=pricing_reference\n","stderr":""}} -->
```python
edges = {
    "revenue_model": {"orders_source", "pricing_reference"},
    "report": {"revenue_model"},
}

def ancestors(node):
    result = set()
    frontier = list(edges.get(node, set()))
    while frontier:
        current = frontier.pop()
        if current not in result:
            result.add(current)
            frontier.extend(edges.get(current, set()))
    return result

def revenue(order_amount, rate):
    return order_amount * rate

candidates = tuple(sorted(ancestors("report")))
observed = revenue(100, 2)
replace_orders = revenue(100, 2) == 100
replace_reference = revenue(100, 1) == 100

print(f"lineage_candidates={candidates}")
print(f"lineage_identifies_unique_cause={len(candidates) == 1}")
print(f"observed_revenue={observed}")
print(f"replace_orders_source_repairs={replace_orders}")
print(f"replace_pricing_reference_repairs={replace_reference}")
print("supported_root_cause=pricing_reference")
```

## Alternatives and Trade-Offs

1. **Declared versus runtime lineage:** declared graphs aid design/impact before runs; runtime evidence reflects actual execution but may be incomplete.
2. **Dataset versus field lineage:** dataset graphs scale discovery; field/control lineage narrows scope at greater collection complexity.
3. **Static parsing versus instrumentation:** parsing covers historical SQL cheaply; runtime instrumentation sees dynamic execution but adds integration overhead.
4. **Backward versus forward traversal:** backward finds candidate causes; forward finds possible impact. Incidents normally need both.
5. **Broad graph search versus mechanism-first hypotheses:** search prevents tunnel vision; mechanism ranking reduces expensive irrelevant tests.
6. **Production experiment versus isolated replay:** production has fidelity but risk; replay is safer but may miss state/environment interactions.
7. **One-factor substitution versus multivariate replay:** isolation clarifies effects; real failures may require interactions and path-dependent sequences.
8. **Rollback evidence versus explicit counterfactual:** rollback is operationally valuable but changes many factors; targeted substitution supports a narrower claim.
9. **Single root versus causal-factor set:** one label communicates simply; factor/control sets better represent complex systems and actionable defenses.
10. **Manual curation versus automated capture:** humans supply semantics and off-platform edges; automation gives scale/freshness but can encode parser gaps.
11. **Full evidence retention versus minimization:** rich artifacts aid reproduction; sensitive data and costs require governed references and expiry.
12. **Immediate action versus complete proof:** containment/recovery protects consumers; durable preventive actions require sufficient causal support.

## Failure Modes and Misconceptions

- **“Lineage shows the root cause.”** It shows candidate dependency paths whose evidence must be tested.
- **“Every ancestor is causal.”** Many inputs are irrelevant to the affected field/cohort/version.
- **“A direct edge means direct value copy.”** It may describe dataset dependency without transformation semantics.
- **“Field lineage captures every influence.”** Filters, joins, grouping, ordering, UDFs, and control data may be indirect or opaque.
- **“The catalog graph is runtime truth.”** Declared or stale lineage may not match the incident run.
- **“No edge means no dependency.”** Collection gaps and off-platform movement exist.
- **“Table names identify the data.”** Versions, snapshots, partitions, environments, and aliases matter.
- **“Latest deployment caused the incident.”** Temporal proximity is hypothesis evidence, not proof.
- **“No deployment means no change.”** Data, config, reference, permissions, infrastructure, and external behavior change.
- **“Rollback success proves cause.”** It can alter multiple factors or coincide with external recovery.
- **“Repair success proves uniqueness.”** Another sufficient factor or interaction may remain.
- **“Correlation across cohorts proves propagation.”** A shared external cause can affect both.
- **“Reproduction in current production is enough.”** Moving state and side effects undermine control and safety.
- **“Change many inputs to speed replay.”** The result cannot isolate which change mattered.
- **“Only confirming tests are useful.”** Falsifiers and negative results prevent anchoring and repeated work.
- **“Nonreproduction means false incident.”** Nondeterminism, retention, clock, cache, and missing capture can erase conditions.
- **“Known-good means latest passing.”** It must be versioned and comparable under the same contract.
- **“Root cause is bad source data.”** Explain origin, acceptance, escape, propagation, and controls.
- **“Root cause is human error.”** Investigate interface, authority, review, automation, reversibility, and detection conditions.
- **“There must be one root.”** Joint causes and multiple sufficient paths occur.
- **“Five whys always finds depth.”** Linear questioning can miss branching interactions and evidence.
- **“Impact equals all descendants.”** Runtime version use and consumer evidence narrow potential impact.
- **“Only direct field descendants matter.”** Filters and joins can change rows without copying values.
- **“Correction can overwrite the bad version.”** Preserve incident evidence and publish lineage-linked correction.
- **“Producer validation ends recovery.”** Consumers, caches, models, reports, exports, and decisions need verification.
- **“The postmortem should name a culprit.”** It should explain causal/control conditions and prevention.
- **“Actions can say improve testing.”** Actions need artifacts, owners, dates, and verification.
- **“A test for the exact row prevents the class.”** It may only memorialize one fixture.
- **“Completed action means effective action.”** Mutation/incident replay and recurrence monitoring verify it.
- **“More lineage edges always help.”** Untyped, stale, conflicting edges increase false paths without provenance.

## Worked Examples

### Example 1

A missing target partition has ancestors in raw manifest, compaction, and publication. Runtime lineage shows compaction never read the partition because a configuration date filter changed. Same raw input with old config restores it; a source replay alone does not.

### Example 2

A dashboard metric is wrong only for GBP. Backward field lineage identifies amount, rate reference, and grouping. The GBP effective-date rate changed; unaffected EUR is a negative control supporting the reference mechanism.

### Example 3

A recent code rollback clears the symptom, but replay shows both old code and new code pass once a transient malformed source record disappears. The record plus parser state—not commit recency alone—remains the supported factor set.

### Example 4

Declared lineage lists an old source table, while observed run input facets show a replacement view. The incident uses runtime edge/version; catalog drift becomes a separate detection/control gap.

### Example 5

Column `customer_tier` is not copied to revenue output, but it filters eligible rows. Lineage marks indirect conditional influence, preventing investigators from excluding it based on value-only mapping.

### Example 6

A notebook exports a CSV later loaded manually into a regulatory report. Automated forward lineage ends at the notebook. Access/export evidence and owner attestation add a curated, lower-confidence edge and expand impact.

### Example 7

A duplicate incident requires retry plus non-idempotent sink plus checkpoint/data split. Removing any one factor prevents the symptom. The record describes a causal set and adds controls at all three layers.

### Example 8

A differential replay uses the bad source snapshot with old/new code, fixed engine image, config, reference, and seed. Exact row/key diffs isolate a join change while unaffected control cohorts remain identical.

### Example 9

The correction fixes V91, but one feature store remains on V90-derived state. Forward lineage and serving probes keep recovery open until cache invalidation and model-feature validation pass.

### Example 10

A postmortem action adds a semantic unit fixture and reference activation gate. A mutation test swaps cents/dollars and confirms both block. Recurrence monitoring checks all unit-bearing products, extending beyond the original row.

## Cross-Program Connections

- **Causal Inference:** interventions, counterfactuals, confounding, interactions, identification, and uncertainty clarify what lineage can and cannot prove.
- **Graph Algorithms:** reachability, backward/forward slicing, strongly connected components, paths, edge typing, and incremental graph updates power analysis.
- **Reliability Engineering:** troubleshooting, incident containment, postmortems, contributing factors, action verification, and recurrence turn evidence into resilience.
- **Distributed Systems:** partial observability, mixed versions, clocks, nondeterminism, retries, state, and path dependence complicate reproduction.
- **Software Engineering:** program slicing, source control, build provenance, feature flags, differential tests, debugging, and mutation testing support experiments.
- **Platform Engineering:** metadata capture, catalogs, event schemas, query parsers, run integrations, evidence stores, and developer workflows scale lineage.
- **Security Engineering:** forensic preservation, provenance integrity, access, supply-chain attestations, tamper evidence, and restricted investigations overlap.
- **Privacy Engineering:** field lineage, purpose propagation, deletion, masking, minimization, protected evidence, and derivative tracking constrain use.
- **Systems Engineering:** fault trees, causal chains, barriers, common-cause failures, configuration control, verification, and corrective action broaden analysis.
- **Organizational Design:** blameless learning, ownership, review, incentives, handoffs, and action accountability determine whether findings persist.

## References

1. OpenLineage. [Object model](https://openlineage.io/docs/spec/object-model/). Accessed 2026-09-03. Primary specification documentation for run, job, dataset, namespace, version, event, and facet identities.
2. OpenLineage. [Run cycle](https://openlineage.io/docs/spec/run-cycle/). Accessed 2026-09-03. Primary documentation for event-based run lifecycle states and runtime operational evidence.
3. OpenLineage. [Lineage Dataset Facet](https://openlineage.io/docs/spec/facets/dataset-facets/lineage/). Accessed 2026-09-03. Primary current specification documentation for dataset/job inputs, field relationships, and transformation descriptors.
4. OpenLineage. [Column Level Lineage Dataset Facet](https://openlineage.io/docs/spec/facets/dataset-facets/column_lineage_facet/). Accessed 2026-09-03. Primary documentation for fine-grained input-field dependencies and direct/indirect transformations.
5. W3C. [PROV Overview](https://www.w3.org/TR/prov-overview/). Accessed 2026-09-03. Authoritative overview of the PROV family for entities, activities, agents, provenance models, constraints, interchange, and access.
6. W3C. [PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/). Accessed 2026-09-03. Authoritative ontology for representing and interchanging provenance across systems and domains.
7. W3C. [PROV-DM: The PROV Data Model](https://www.w3.org/TR/prov-dm/). Accessed 2026-09-03. Authoritative conceptual model for provenance entities, activities, agents, generation, use, derivation, and attribution.
8. Google. [Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/). Accessed 2026-09-03. Primary SRE guidance for hypothetico-deductive investigation, telemetry, hypothesis testing, negative results, controlled treatment, and multiple factors.
9. Google. [Postmortem Culture](https://sre.google/sre-book/postmortem-culture/). Accessed 2026-09-03. Primary guidance for impact/timeline/root-cause records, contributing factors, blameless learning, review, and preventive actions.
10. dbt Labs. [Manifest JSON](https://docs.getdbt.com/reference/artifacts/manifest-json). Accessed 2026-09-03. Primary documentation for node, source, exposure, metric, semantic model, parent/child map, and invocation metadata in a versioned build artifact.
11. dbt Labs. [Exposures](https://docs.getdbt.com/docs/build/exposures). Accessed 2026-09-03. Primary documentation for describing downstream dashboards, applications, owner, maturity, dependencies, and lineage use.
12. OpenTelemetry. [Trace data model](https://opentelemetry.io/docs/reference/specification/trace/api/). Accessed 2026-09-03. Primary specification for trace/span identity, parent relationships, events, links, status, and attributes supporting correlated execution evidence.
13. Delta Lake. [Table utility commands](https://docs.delta.io/delta-utility/). Accessed 2026-09-03. Primary documentation for table history, operation/version metadata, detail, restore, and vacuum considerations in version investigations.
14. Apache Iceberg. [Spark queries and metadata tables](https://iceberg.apache.org/docs/latest/spark-queries/). Accessed 2026-09-03. Primary documentation for snapshots, history, files, manifests, entries, partitions, and change-query evidence.

## Exercises

### Exercise 1

Design a versioned runtime lineage model for a batch-plus-CDC product. Include datasets, fields, runs, code/config/reference/schema/contract, snapshots/offsets, edge types, collector provenance, confidence, and coverage.

### Exercise 2

Investigate a wrong currency aggregate using backward/forward slices. Write at least three competing hypotheses, predictions, disconfirming evidence, differential replays, controlled substitutions, and impact confirmation.

### Exercise 3

Analyze an incident involving duplicate replay, non-idempotent merge, and split checkpoint/data commits. Decide whether there is one root or a causal factor set, and produce controls for creation, escape, propagation, and recovery.

### Exercise 4

Design impact analysis when automated lineage stops at notebooks and exports. Include runtime validation, consumer discovery, field/control influence, confidence, sensitive evidence, and acknowledgment.

### Exercise 5

Write a root-cause/postmortem record and action plan that separates facts, hypotheses, causal factors, contributing conditions, control gaps, corrections, preventive actions, reviewers, verification, and recurrence.

## Answers to the Exercises

### Answer 1

Represent stable namespaced entity IDs with snapshot/table/topic/file version and partition; activities with run, code commit/image, configuration, reference/master, schema/contract, engine/environment and times; agents with producer/evaluator identity. Edges distinguish read/write, direct value, transform, join/filter/group/order/control, reference, publish/serve, correction and consumer use. Every edge stores declared/observed/parsed/curated source, collector/version, run/time scope, confidence and evidence link. CDC binds source positions and target committed checkpoint; batch binds manifests and logical interval. Report expected/instrumented nodes and edges, unsupported UDF/dynamic paths, off-platform exports and conflicts as coverage/unknowns.

### Answer 2

Pin bad output/source/rate/code/config and reproduce exact wrong keys/totals. Backward slice yields transaction inputs, effective-dated rate, currency mapping, timezone/date selection, aggregation code and reference join. H1 wrong rate predicts only GBP effective window and is falsified by correct raw/reference values. H2 join multiplicity predicts duplicate keys/count inflation and is falsified by unique join/reconciliation. H3 timezone selects next-day rate and predicts boundary-only defects. Replay identical source with good/bad rate, identical rate with old/new code/config, and boundary fixtures while checking unaffected EUR. Forward-slice supported factor, then confirm actual output/consumer versions, caches and exports. Record negative experiments and remaining uncertainty.

### Answer 3

Treat retry, non-idempotent sink, and non-atomic checkpoint protocol as a jointly sufficient causal set under the recovery sequence; the retry is expected behavior, not adequate blame. Creation control makes mutations idempotent by stable event identity; protocol atomically couples applied data/checkpoint or makes replay safe. Escape controls reconcile key multiplicity and checkpoint/data state. Propagation controls gate publication and expose suspect versions. Recovery retains source log, fences writes, rebuilds from pinned checkpoint, reconciles exact state, publishes a new version, and drives consumer replay. Mutation and crash-point tests verify each barrier and recurrence monitors duplicates plus checkpoint divergence.

### Answer 4

Forward lineage gives potential notebook descendants, then combine access/query history, notebook versions, export/object audit, shared-account resolution, dashboard/model/report inventories, network/service dependencies, and owner attestations. Add curated export edges labeled collector, time window, lower confidence and gaps. Field analysis includes direct values and indirect filters/joins. Protect sensitive rows with key/digest references and restricted workspace. Contact critical owners with exact affected/safe versions; record acknowledgment and actual cache/report/decision use. Scope remains bounded/unknown where exports cannot be traced, which influences containment and communication rather than being reported as no impact.

### Answer 5

Record impact and exact timeline; architecture plus versioned runtime graph; reproducible expected/observed symptom; evidence inventory and coverage; each hypothesis, prediction, falsifier, experiment and negative result; supported trigger/proximate and interacting factors; latent creation/escape/propagation/recovery conditions; alternative explanations/confidence; containment, correction and end-to-end consumer validation. Actions name concrete code/contract/gate/collector/runbook artifacts, owner, due date, priority and proof such as mutation/replay. Reviewers challenge causal depth, experiment fidelity, impact completeness and whether actions would have prevented/reduced recurrence. Preserve protected evidence, avoid person-blame as endpoint, track completion plus effectiveness, and search future incidents/near misses for recurrence.
