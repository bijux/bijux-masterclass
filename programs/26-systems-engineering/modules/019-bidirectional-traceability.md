---
module_id: SYSENG-019
program: Systems Engineering
level: 1
module_number: 19
title: Bidirectional Traceability
status: complete
last_verified: 2026-08-31
---

# Bidirectional Traceability

## One-Page Review

### Governing question

How can a team maintain trustworthy, bidirectionally navigable relationships from stakeholder intent through requirements, architecture, realization, verification, validation, operation, and change so that coverage and impact are reviewable without mistaking link presence or matrix percentages for semantic justification?

### Essential definitions

- **Traceability** is the ability to establish, use, and maintain discernible relationships among lifecycle artifacts and the reasoning that connects them.
- **Upward traceability** follows a requirement to its parent need, obligation, hazard, decision, or other authoritative source and explains why it exists.
- **Downward traceability** follows a source or requirement through decomposition, allocation, architecture, realization, and evidence and explains how it is addressed.
- **Bidirectional traceability** permits traversal and consistency review in both directions; it does not require two duplicate edges or imply logical equivalence.
- A **trace link/edge** is a typed, versioned relation between identified source and target artifacts with rationale, authority, status, and evidence.
- **Vertical traceability** relates abstraction or hierarchy levels; **horizontal traceability** relates peers, interfaces, hazards, budgets, or coordinated obligations at comparable levels.
- An **orphan** has no justified required upstream source; an **uncovered source** has no adequate downstream realization/evidence path; a **dangling link** points to a missing or unresolved artifact version.
- A **traceability matrix** is a tabular view of relationships; a **traceability graph** is the underlying many-to-many network.
- **Coverage** is a scoped measure of recorded relationships; **trace correctness** asks whether each relationship is semantically valid; **trace completeness** asks whether all required relationships are represented.
- **Impact analysis** uses trace and dependency evidence to identify potentially affected artifacts after change; the result is a review frontier, not proof that nothing else is affected.

### Central model, mechanism, or theorem

Represent the trace graph as \(G=(V,E)\), where each edge is:

\[
e=\langle sourceVersion,targetVersion,type,rationale,conditions,
authority,evidence,status,created,reviewed\rangle.
\]

For requirement \(r\), define bounded closure obligations:

\[
Upstream(r)=Needs\cup Parents\cup Constraints\cup Hazards\cup Decisions,
\]

\[
Downstream(r)=Children\cup Allocations\cup Design\cup Realization
\cup Verification\cup Validation.
\]

A navigable path is not a coverage proof. Require semantic review:

\[
ValidPath(a,b)\Rightarrow\bigwedge_{e\in path(a,b)} Valid(e)
\land CompositionRationale(path).
\]

Change candidates are a conservative graph reachability result:

\[
Candidates(change(x))=Reach_G(x,RelevantEdgeTypes,CurrentBaseline),
\]

which may omit undiscovered dependencies and may include unaffected artifacts.

### Critical invariants

- Every governed artifact has stable identity, version/baseline, type, owner, and lifecycle status.
- Every edge has a controlled relation type and rationale; a hyperlink or co-occurrence is not sufficient.
- Upward traces establish legitimate source and transformation intent; downward traces establish contribution, allocation, realization, and evidence paths.
- Many-to-many relations and intermediate rationale are preserved rather than forced into one-to-one parent trees.
- The source and target versions referenced by a link are current for the reviewed configuration or explicitly historical.
- Orphans, uncovered sources, dangling/stale edges, duplicate/conflicting links, and unjustified design elements are reviewed and dispositioned.
- Interface, budget, hazard/control, supplier, configuration, verification-result, anomaly, and change relationships are included where relevant.
- Coverage percentages always name denominator, required edge/path types, baseline, exclusions, and semantic-review status.
- Automated link inference remains proposed until competent review; confidence scores never replace authority or rationale.
- High-consequence trace claims require applicable independent review and direct evidence, not graph density.

### Common failures

Failures include links without relation type; `implements` edges that do not explain contribution; two reverse hyperlinks called bidirectional; tracing only requirements-to-tests; using file names instead of immutable artifact versions; one-to-one matrices that erase many-to-many coverage; auto-accepting similarity links; treating 100% row coverage as correctness; hiding derived requirements under fake parents; leaving interface and hazard traces horizontal and unmanaged; failing to update traces after change; tracing test cases but not results/configuration; and assuming graph reachability finds every real dependency.

### Compact example

A requirement says an emergency system must provide verified location during network loss. Upward edges link the responder need, operational scenario, privacy/safety constraints, and location-authority rationale. Downward edges link child functions, device/cache/interface allocations, uncertainty semantics, degraded-mode design, implementation configuration, verification procedures/results, and representative operational validation. A test named “location” is not adequate trace: the edge must explain which conditions and acceptance criteria it verifies and identify the exact result/configuration. Change to location provenance then produces a review frontier across interfaces, displays, records, hazards, tests, training, and deployed variants.

### Connections

Retrieve sources, decomposition, allocation, and verification concepts from SYSENG-011–018. Continue to requirement change/conflict. Later interfaces, configuration baselines, decision records, digital threads, verification matrices, anomaly evidence, change impact, safety cases, and systems-of-systems governance extend traceability across the lifecycle.

## Governing Question

Engineering artifacts multiply as a system matures. Needs become requirements; requirements drive models, interfaces, architecture, code, hardware, procedures, training, and tests; incidents and changes revise all of them. Without explicit relationships, a change board cannot tell what might break, a verifier cannot show why a test matters, and a reviewer cannot distinguish necessary design from historical accumulation.

The governing question is not how to fill a matrix. It is how to preserve meaning across transformations and time. A trace should answer why an artifact exists, how it contributes, which version it concerns, what evidence supports the relationship, and who accepted the rationale. Bidirectional traversal enables two complementary audits: “why is this here?” and “where is this addressed?”

## Why This Matters

Missing trace creates both underengineering and overengineering. An uncovered need may never be implemented. An orphan design feature adds cost, attack surface, and maintenance without authority. A changed interface may leave tests and supplier specifications stale. In safety work, a hazard control can appear implemented while no verification result covers the fault condition that justified it.

ISO/IEC/IEEE 29148:2018 defines requirements traceability as documenting upward derivation and downward allocation/flowdown paths and defines a traceability matrix as a structured relationship artifact. NASA requires lifecycle bidirectional traceability among expectations, requirements, component requirements, design, and verification artifacts, with self-derived requirements explicitly justified and reviewed. SEBoK 2.14 places traceability within requirements management and system-definition consistency.

Tools can make large graphs searchable, but scale increases the need for semantics. A generated edge from similar text may be useful triage; it cannot determine whether a child is sufficient for a parent or whether a test actually discriminates the requirement. Trace quality is an engineering assurance problem, not a database population problem.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. requirements trace to authoritative needs, parents, constraints, hazards, interfaces, or explicit derived rationale;
2. decomposition and allocation use many-to-many contribution and coverage arguments;
3. child and subsystem evidence does not automatically prove a parent/system outcome;
4. verification evidence includes method, configuration, conditions, oracle, result, uncertainty, and authority;
5. architecture, supplier, and interface decisions create dependencies beyond a requirements tree;
6. baselines and versions determine which artifacts can be meaningfully compared;
7. automated checks provide bounded observations and cannot establish semantic correctness.

As a retrieval test, consider a spreadsheet with every requirement linked to one test case. Ask whether requirements have legitimate upstream sources, designs and implementations are justified, interfaces/hazards are covered, tests match exact versions and conditions, results passed, and system-level evidence closes composition. One green cell per row proves none of those facts.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish upward, downward, bidirectional, vertical, horizontal, and lifecycle traceability;
2. define stable artifact identities, versions, edge types, rationale, authority, and evidence;
3. model many-to-many traceability as a governed graph with useful matrix views;
4. trace needs, requirements, decomposition, allocation, interfaces, design, realization, verification, validation, and operation;
5. detect and disposition orphans, uncovered sources, stale/dangling links, duplicates, and conflicts;
6. design semantic coverage queries and metrics without overclaiming percentages;
7. perform bounded change-impact analysis with edge types, configuration, and uncertainty;
8. govern derived requirements, supplier evidence, variants, anomalies, and waivers;
9. use automation and inferred links as review aids rather than accepted truth;
10. construct high-consequence trace evidence with appropriate independence and authority.

## Core Exposition

**Define trace purpose and scope.** Trace needed for concept review differs from trace needed for supplier acceptance, safety assurance, regulatory evidence, or field change. Name system boundary, lifecycle stages, artifact types, configurations, decisions, required edge/path types, owners, and review cadence. Avoid “trace everything” without decision value.

**Design trace around answerable decisions.** Write the queries before selecting tools: Which authorized needs lack validated system requirements? Which safety controls have no current fault-condition result? Which supplier versions support deployed configuration C? Which requirements depend on assumption A? Which interfaces and operational procedures change if threshold T moves? For every query define artifact population, edge/path semantics, status, baseline, and acceptable exceptions. This exposes whether the schema carries the needed reasoning and prevents a large repository from being mistaken for usable traceability.

**Give artifacts durable identity.** Assign stable IDs independent of file position or title. Record artifact type, owner, version/baseline, status, configuration applicability, source repository, and lifecycle dates. A paragraph number can be a locator, but if renumbering changes identity, links will silently lie. Use immutable revision references for evidence.

**Define a relation vocabulary.** Useful types include `derives-from`, `refines`, `contributes-to`, `allocated-to`, `constrained-by`, `satisfies`, `implements`, `interfaces-with`, `shares-budget`, `mitigates-hazard`, `verified-by`, `validated-by`, `affected-by`, `supersedes`, and `evidenced-by`. Define direction, allowed artifact types, required attributes, and semantics. Do not let teams invent near-synonyms without governance.

**Store rationale on the edge.** Nodes describe artifacts; the edge explains why they relate. A child may contribute timing while a sibling contributes correctness. A test may verify one condition but not another. Record contribution, scope, assumptions, exclusions, and authority. Edge rationale is what makes change analysis and review interpretable.

**Understand bidirectionality.** Store one directed typed relation and provide inverse traversal/query semantics. For example, `child derives-from parent` can be queried upward from child and downward as `parent has-child`. Duplicating an unmanaged reverse edge risks inconsistency. Bidirectional navigation does not mean the relation is symmetric or that parent and child are equivalent.

**Trace sources upward.** Every requirement reaches a baselined need, parent, applicable constraint, hazard/control rationale, interface agreement, or approved self-derived source. If multiple sources contribute, preserve all with distinct roles. Fake parenting hides gold plating; legitimate derived requirements identify analysis and concurrence explicitly.

**Trace realization downward.** Link requirements to child requirements, allocations, architecture/design decisions, interfaces, implementation artifacts, configuration items, procedures, training, and evidence as appropriate. Avoid jumping directly from a broad need to a code file when intermediate transformation reasoning matters. Granularity should support decisions without drowning in incidental lines.

**Trace verification beyond test cases.** Link requirement to verification concept, procedure/case, environment, test article/configuration, data, oracle, execution result, anomalies/deviations, reviewer, and acceptance disposition. A planned test is not a passing result. When one procedure covers several requirements, each edge states the exact observation and criterion.

**Trace validation to outcomes.** Requirements and design may be verified while stakeholder outcomes fail. Link representative operational scenarios, populations, measures, validation activities/results, dissent, and limitations back to needs. Preserve the difference between requirement coverage and outcome evidence.

**Trace interfaces horizontally.** Both sides of an interface need linked semantic, timing, quality, mode, failure, version, ownership, and verification obligations. Horizontal trace detects producer-consumer mismatches and coordinated change. An interface control document link alone does not show which clauses affect which requirements.

**Trace hazards, threats, and controls.** Connect hazardous/threat states to causal analysis, controls, allocated requirements, design mechanisms, common-cause assumptions, verification evidence, anomalies, and residual-risk decisions. A control without hazard source may be unnecessary; a hazard without verified controls is uncovered. Safety/security trace needs independent review proportional to consequence.

**Trace budgets as coupled relationships.** A system mass, power, timing, capacity, reliability, or error budget connects parent limit, allocations, predictions, margins, assumptions, and verification. A change to one share reaches siblings and reserve authority, not only its owning element. Type budget edges separately from derivation.

**Represent suppliers and external evidence.** Link contract clauses, supplier requirements, interface specifications, configuration/version, certificates/reports, assumptions, change notices, vulnerabilities/anomalies, and system acceptance. Supplier artifact opacity is a trace risk to govern, not a reason to claim the supplier owns system compliance.

**Handle variants and applicability.** Record which product, market, region, mode, customer, supplier, and release each node/edge applies to. A link valid for configuration A can be stale for B even if both nodes exist. Use shared core plus explicit variant edges and prevent unsupported cross-configuration evidence reuse.

**Review trace correctness.** Sample and risk-prioritize edges. Read source, target, and rationale together. Ask whether the relation type is correct, scope preserved, source authoritative, target actually contributes, assumptions valid, and evidence current. Link existence and text similarity cannot answer these questions.

**Review trace completeness.** Query required patterns: every approved requirement has upstream justification and downstream verification; every critical need has requirement/validation paths; every design/implementation element has a source or approved derivation; every interface has both-side obligations; every hazard has control/evidence; every executed verification has result/disposition. Define legitimate exceptions.

**Verify the trace system itself.** Check identity uniqueness, allowed edge endpoints, required attributes, inverse-query behavior, baseline reproducibility, access controls, import/export fidelity, history, and failure recovery. Seed known orphans, stale targets, prohibited relations, variant mismatches, and unauthorized changes to show controls detect them. Compare generated matrices and reports with the authoritative graph. Tool verification establishes repository behavior, not semantic truth of engineering edges; semantic sampling and artifact-owner review remain separate.

**Detect graph defects.** Orphans lack required incoming justification. Uncovered sources lack required outgoing paths. Dangling edges reference missing nodes. Stale edges reference superseded versions without historical intent. Duplicate/conflicting edges disagree on type, target, or applicability. Cycles can signal circular justification, though behavioral feedback loops are not automatically trace cycles.

**Use coverage metrics cautiously.** Define denominator and edge/path predicate. “95% requirements traced” might mean 95 of 100 have any test link, not that tests passed or sources are covered. Report separate syntactic presence, semantic review, evidence execution, pass/disposition, criticality, and variant coverage. Never average away a missing safety-critical path.

**Perform change-impact traversal.** Start with exact changed node/version and change semantics. Traverse relevant incoming/outgoing edge types to requirements, interfaces, budgets, design, suppliers, tests, operations, training, documentation, and deployed configurations. Review each candidate for actual impact and search beyond the graph using domain expertise, ownership, and dependency evidence. Record false positives and discovered missing edges.

**Close the loop after change.** Approved changes update nodes, edge rationale, baselines, verification/validation, status, and impacted operational artifacts together. Preserve historical snapshots for audit. A change is not complete when the requirement text changes while downstream evidence remains associated with the old version.

**Integrate anomalies and waivers.** Link failed/blocked verification, anomalies, deviations, waivers, risk acceptances, corrective actions, expiration, and retest evidence to affected requirements/configurations. A waived result does not become a pass; the disposition and authority remain visible.

**Assign trace governance.** Artifact owners own semantic edges they create; system/requirements authorities define schemas and coverage policy; interface and assurance authorities review crosscutting edges; configuration management preserves versions; change boards use impact results. A central trace librarian cannot invent engineering rationale for every team.

**Manage trace debt explicitly.** Deferred links, provisional rationale, inaccessible supplier evidence, migration gaps, and stale integrations are risks, not invisible clerical backlog. Record affected decisions/configurations, criticality, owner, deadline, compensating review, and consequence. Prevent release or acceptance when required high-consequence paths are unresolved; do not close debt by attaching generic links. Track debt age and semantic review separately from raw edge count so bulk-generated edges cannot manufacture apparent progress.

**Protect sensitive trace information.** Trace graphs can expose security architecture, hazards, vulnerabilities, personal data, supplier restrictions, and regulatory evidence. Apply least privilege, integrity controls, audit, retention, redaction/export policy, and resilient backup while preserving reviewer access. A sanitized external view must retain enough identity and rationale to support its decision without leaking restricted details; record when redaction limits independent review.

**Automate without auto-accepting meaning.** Tools can enforce schemas, detect missing nodes/fields, compute reachability, suggest links from identifiers/text, and diff baselines. Proposed links need reviewer, rationale, confidence context, and disposition. Machine-generated confidence is not evidence that the relation is correct.

**Use executable checks as bounded triage.** The following checker detects missing type, rationale, baseline, authority, current targets, and evidence fields in five declared edges. It cannot determine semantic validity, path sufficiency, or real impact.

<!-- bijux-verify: {"id":"traceability-edge-record-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"edges_total=5\nwell_formed_declared=1\nmissing_type=TE-002\nmissing_rationale=TE-003\nmissing_baseline=TE-004\nmissing_authority=TE-005\nstale_or_missing_target=TE-004\nmissing_evidence=TE-003\ntrace_set_ready=false\nevidence=declared_fields_only\n","stderr":""}} -->
```python
current_nodes = {"N-1@b1", "R-1@b3", "D-1@b7", "T-1@b4", "V-1@b4"}
edges = [
    {"id": "TE-001", "source": "R-1@b3", "target": "N-1@b1", "type": "derives-from",
     "rationale": "requirement transforms warning need", "baseline": "system-b3",
     "authority": "requirements-board", "evidence": ["source review"]},
    {"id": "TE-002", "source": "D-1@b7", "target": "R-1@b3", "type": "",
     "rationale": "design provides required behavior", "baseline": "design-b7",
     "authority": "architecture-board", "evidence": ["design review"]},
    {"id": "TE-003", "source": "T-1@b4", "target": "R-1@b3", "type": "verifies",
     "rationale": "", "baseline": "verification-b4", "authority": "verification-lead",
     "evidence": []},
    {"id": "TE-004", "source": "V-1@b4", "target": "R-1@b2", "type": "evidences",
     "rationale": "result covers response criterion", "baseline": "",
     "authority": "acceptance-board", "evidence": ["result record"]},
    {"id": "TE-005", "source": "R-1@b3", "target": "D-1@b7", "type": "constrains",
     "rationale": "requirement constrains design", "baseline": "system-b3/design-b7",
     "authority": "", "evidence": ["trace inspection"]},
]

required = ("source", "target", "type", "rationale", "baseline", "authority", "evidence")
complete = [e for e in edges if all(e[k] for k in required) and e["target"] in current_nodes]
print(f"edges_total={len(edges)}")
print(f"well_formed_declared={len(complete)}")
for field in ("type", "rationale", "baseline", "authority"):
    print(f"missing_{field}=" + ",".join(sorted(e["id"] for e in edges if not e[field])))
print("stale_or_missing_target=" + ",".join(sorted(e["id"] for e in edges if e["target"] not in current_nodes)))
print("missing_evidence=" + ",".join(sorted(e["id"] for e in edges if not e["evidence"])))
print(f"trace_set_ready={str(len(complete) == len(edges)).lower()}")
print("evidence=declared_fields_only")
```

## Definitions and Notation

Let artifact node \(v=(id,type,version,configuration,status,owner)\). Let edge \(e=(u,v,t,\rho)\), where \(t\) is relation type and \(\rho\) its rationale plus governance attributes.

For node set \(X\), define typed forward reachability \(Reach^+_T(X)\) and reverse reachability \(Reach^-_T(X)\) using allowed edge types \(T\). Bidirectional capability means both queries are supported over the same controlled edge semantics.

Define syntactic edge coverage for required node set \(S\):

\[
C_{edge}=\frac{|\{s\in S\mid RequiredEdgePredicate(s)\}|}{|S|}.
\]

This ratio says nothing about semantic correctness unless the predicate includes reviewed validity and evidence status. A **digital thread** is a governed lifecycle information flow/relationship network; a large graph alone is not a trustworthy digital thread.

## Mechanisms, Invariants, or Proof Structure

The mechanism has seven passes: define policy/schema; identify/version artifacts; create typed rationale-bearing edges during work; run structural queries; review semantics and coverage; use trace for impact/evidence decisions; update baselines and history after change.

Use a trace readiness predicate:

\[
Ready(G)=IdentityIntegrity\land SchemaValidity\land UpstreamJustification
\land DownstreamCoverage\land SemanticReview\land VersionConsistency
\land ChangeGovernance.
\]

This is a governance predicate. Graph queries can help establish schema and reachability; source fidelity, sufficiency, and completeness require engineering evidence and challenge.

Maintain five invariants. **Identity invariant:** edges refer to immutable artifact versions. **Semantic invariant:** type and rationale explain the transformation. **Bidirectionality invariant:** both why/upstream and where/downstream queries work. **Evidence invariant:** planned and executed/dispositioned evidence remain distinct. **Temporal invariant:** current configuration and historical baselines never blur.

## Alternatives and Trade-Offs

**Matrix versus graph.** Matrices are readable for two artifact classes; graphs support many types and paths. Generate focused matrices from a controlled graph and avoid manually divergent views.

**Coarse versus fine granularity.** Coarse traces reduce maintenance but weaken impact precision. Fine traces improve localization but create churn/noise. Trace at independently governed, changed, verified, or safety-significant boundaries.

**Manual versus inferred links.** Manual rationale is costly but meaningful; inference scales discovery but creates false links. Treat inference as a review queue and measure disposition quality.

**Central repository versus federated sources.** Centralization simplifies queries; federation preserves tool ownership and native semantics. Use stable identities, version contracts, and synchronized indexes when federated.

**Strict closure versus risk-based depth.** Universal deep trace can be wasteful; insufficient critical trace is dangerous. Define minimum lifecycle paths and stronger depth for high-consequence, volatile, supplier, and cross-boundary concerns.

**Live graph versus signed snapshots.** Live trace supports work; immutable snapshots support audit and acceptance. Maintain both through versioned baselines and reproducible exports.

## Failure Modes and Misconceptions

1. **“Bidirectional means two links.”** It means controlled traversal and review in both directions.
2. **“Trace means hyperlink.”** A useful edge needs type, rationale, version, scope, and authority.
3. **“One parent per child.”** Real transformations and crosscutting concerns are many-to-many.
4. **“100% traced means complete.”** The denominator or edge predicate may be weak, and semantics may be wrong.
5. **“A test link means verified.”** Procedure, result, configuration, anomaly, and disposition are separate artifacts.
6. **“Orphan means delete.”** Investigate legitimate derived source before removal.
7. **“Reachability proves impact.”** It yields candidates based on recorded dependencies and misses unknown links.
8. **“Similarity is rationale.”** Similar words can express unrelated obligations; different words can implement the same intent.
9. **“The matrix is current because files exist.”** Version/configuration mismatch creates stale evidence.
10. **“Traceability is clerical overhead.”** Poor schema can be overhead; decision-focused trace is lifecycle reasoning infrastructure.

## Worked Examples

### Example 1

**Situation.** A child requirement links to a parent with “related.” **Reasoning.** Read both and identify contribution: the child supplies degraded-mode status while siblings supply recovery. Change type to `contributes-to`, add conditions/rationale and coverage argument. **Conclusion.** Typed rationale makes the edge reviewable; vague adjacency does not.

### Example 2

**Situation.** A matrix stores parent-to-child and child-to-parent rows separately. **Reasoning.** One row is updated and the reverse becomes stale. Store one directed edge with inverse query semantics and version checks. **Conclusion.** Bidirectionality is a graph capability, not duplicated data.

### Example 3

**Situation.** Every requirement has a planned test. **Reasoning.** Query results show several tests never executed, one failed, and two cover old requirement versions. Separate `verified-by procedure` from `evidenced-by result` and disposition. **Conclusion.** Planned coverage is not verification status.

### Example 4

**Situation.** A cryptographic design has no parent requirement. **Reasoning.** It may be gold plating or a legitimate derived control from threat/risk, policy, or interface. Seek that source and concurrence; otherwise remove/reconsider it. **Conclusion.** Orphan analysis asks for justification before deletion or acceptance.

### Example 5

**Situation.** An interface schema changes a field unit. **Reasoning.** Typed traversal finds producer/consumer requirements, data models, budget calculations, supplier documents, tests, displays, training, and deployed variants. Domain review finds an unrecorded reporting dependency and adds it. **Conclusion.** Trace accelerates impact discovery but does not bound reality by itself.

### Example 6

**Situation.** A hazard control traces to code and one passing test. **Reasoning.** Add hazard/causal context, allocated requirements, interface/common-cause assumptions, configuration, fault conditions, test result, anomalies, and residual-risk decision. **Conclusion.** High-consequence trace must preserve the assurance argument, not just endpoints.

### Example 7

**Situation.** A supplier certificate is linked to “security compliance.” **Reasoning.** Type exact scheme/claim, product/version/configuration, environment, assumptions, expiration, integration requirements, and system acceptance. **Conclusion.** Bounded inherited evidence cannot justify a universal compliance edge.

### Example 8

**Situation.** A feature flag changes allocation by deployment. **Reasoning.** Record variant applicability for requirement, design, implementation, tests, operations, and rollback. Prevent a result from disabled configuration A evidencing enabled configuration B. **Conclusion.** Trace correctness is configuration-specific.

### Example 9

**Situation.** An AI system proposes similarity links automatically. **Reasoning.** Use confidence to prioritize review; reviewers select type, rationale, scope, and authority or reject. Measure false proposals and missed known edges. **Conclusion.** Automated inference supports discovery but cannot accept semantic trace.

### Example 10

**Situation.** A medication-allergy warning changes its clinical rule source. **Reasoning.** Traverse data definitions, requirements, model/rules, interfaces, user display, overrides, tests, validation populations, training, deployed versions, incidents, and safety case. Clinical authority reviews meaning beyond graph results. **Conclusion.** Trace supports controlled change but cannot establish clinical correctness or safety.

## Cross-Program Connections

- [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) supplies stable domain concepts and decision/event relations for semantic trace.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) links requirements and quality concerns to decisions, views, elements, and rejected alternatives.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) governs lineage, provenance, versioned evidence, and graph/query quality for trace data.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) connects assets, threats, controls, assurance, vulnerabilities, incidents, and risk decisions.
- [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) supplies versioned interface semantics and consumer/provider impact edges.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) supports federated trace infrastructure while preserving artifact-owner semantics and authority.

## References

1. ISO/IEC/IEEE. [ISO/IEC/IEEE 29148:2018 — Requirements engineering](https://www.iso.org/standard/72089.html), second edition, 2018. Consulted 2026-08-31.
2. ISO/IEC/IEEE. [ISO/IEC/IEEE 15288:2023 — System life cycle processes](https://www.iso.org/standard/81702.html), second edition, 2023. Consulted 2026-08-31.
3. NASA. [Crosscutting Technical Management](https://www.nasa.gov/reference/6-0-crosscutting-technical-management/), requirements management and bidirectional traceability. Consulted 2026-08-31.
4. NASA. [Technical Requirements Definition](https://www.nasa.gov/reference/4-2-technical-requirements-definition/), requirements metadata and trace guidance. Consulted 2026-08-31.
5. NASA Software Engineering Handbook. [Bidirectional Traceability](https://swehb.nasa.gov/pages/viewpage.action?pageId=16455241), traceability matrix and impact guidance. Consulted 2026-08-31.
6. SEBoK Editorial Board. [System Requirements Definition](https://sebokwiki.org/wiki/System_Requirements_Definition), requirements management and traceability, version 2.14. Consulted 2026-08-31.
7. INCOSE Requirements Working Group. [Traceability webinar](https://www.incose.org/wp-content/uploads/legacy/professional-development-portal/pdp-ppt-files/pdp-webinar-ppt-files/webinar_177_traceabillity_wheatcraft.pdf), allocation and child-requirement trace concepts. Consulted 2026-08-31.
8. Gotel, O. C. Z., and Finkelstein, A. C. W. [“An Analysis of the Requirements Traceability Problem”](https://doi.org/10.1109/ICRE.1994.292398), IEEE International Conference on Requirements Engineering, 1994. Consulted 2026-08-31.

## Exercises

### Exercise 1

Define a typed trace schema for needs, requirements, constraints, hazards, design decisions, interfaces, implementation, verification procedures/results, validation, and changes. State inverse query semantics.

### Exercise 2

Diagnose a trace matrix reporting 100% requirement-to-test coverage. Design queries that distinguish planned, executed, passed, waived, stale, semantically reviewed, and configuration-applicable evidence.

### Exercise 3

Perform change-impact analysis for a timestamp semantic changing from local time to UTC. Include requirements, interfaces, data, operations, suppliers, tests, migration, and evidence limits.

### Exercise 4

Compare manual, identifier-rule, text-similarity, model-derived, and runtime-observed trace creation. Recommend governance for a safety-critical system.

### Exercise 5

Build an assurance-oriented trace plan for a remotely supervised autonomous shuttle. Cover needs, hazards, cybersecurity, allocation, suppliers, software/hardware, human oversight, verification, validation, anomalies, variants, and external authority.

## Answers to the Exercises

### Answer 1

Nodes carry stable ID, artifact type, immutable version, configuration/variant, lifecycle status, owner, repository, and authority. Edges carry source/target versions, controlled type, rationale/contribution, conditions/scope, assumptions, authority, evidence, status, creator/reviewer, and dates. Types include `derives-from`, `refines`, `contributes-to`, `constrained-by`, `allocated-to`, `interfaces-with`, `shares-budget`, `mitigates-hazard`, `implemented-by`, `verified-by`, `evidenced-by`, `validated-by`, `supersedes`, and `affected-by`.

Store one directed semantic edge. Define inverses in the schema/query layer: `child derives-from parent` becomes upward “why/source” from child and downward “which children” from parent; `result evidences requirement` becomes requirement-to-results in reverse. Some relations such as `interfaces-with` may be symmetric only if defined so; contribution and derivation are not. Constrain allowed node types, required fields, multiplicity expectations, and baseline rules for each edge type.

### Answer 2

First inspect the denominator: approved requirements by baseline, criticality, and variant. Separate queries: requirement has a current verification concept; has an approved procedure; procedure covers exact acceptance criterion/conditions; applicable configuration has an execution; execution links immutable result/data/environment; result passed, failed, blocked, or unavailable; anomaly/deviation/waiver disposition exists; acceptance authority approved; semantic edge was reviewed; and evidence matches current requirement/configuration version.

Report counts and missing IDs for each state, not one percentage. Stratify safety/security/regulatory and system-level requirements. Review samples of green edges for oracle and scope correctness. Query test procedures/results with no requirement source and requirements whose only coverage is obsolete or excluded. A waived failure remains waived, not passed. Even full syntactic closure cannot prove the requirement set or test suite is semantically complete.

### Answer 3

Identify the exact time-definition artifact and old/new versions: UTC representation, offset, leap-second/clock-source policy, precision, ordering, serialization, display, retention, and ambiguity. Traverse to producer/consumer interface requirements, schemas, storage/index/partition logic, calculations, audit/signature rules, alerts, logs, APIs, user displays, reports, data exports, supplier contracts, monitoring, incident tooling, tests, training, privacy/records evidence, and every deployed variant.

Plan dual-read/write or conversion, historical-data interpretation, cutoff, reconciliation, rollback, and external coordination. Update semantic/unit edges, not only field names. Test boundary dates, daylight changes for display/local conversion, ordering, missing offsets, old clients, replay, migration, and audit continuity. Search beyond graph reachability with code/schema queries, domain owners, runtime lineage, and supplier review; record newly discovered dependencies as edges. Graph results are candidates and may both overinclude and miss unrecorded operational use.

### Answer 4

Manual creation yields strong contextual rationale but is costly and inconsistent without schema. Identifier rules are deterministic for governed annotations but can preserve wrong IDs. Text similarity finds candidates across wording but confuses shared vocabulary and misses semantically equivalent terms. Model-derived trace is reliable within well-governed transformations but inherits model errors and version drift. Runtime observation reveals actual calls/data flows but misses dormant, failure, manual, physical, safety, and intended behavior and cannot establish why a relation exists.

For safety-critical work, define authoritative artifact types/edge semantics and mandatory lifecycle paths. Generate deterministic edges where transformations are controlled; require authors to supply rationale; use similarity/runtime evidence only to propose or challenge edges. Independent competent reviewers approve critical hazard/control/verification paths. Baseline immutable graph snapshots with configurations and results; audit stale/orphan/uncovered edges; sample semantic correctness; and link anomalies/waivers/residual-risk decisions. No automated source may silently create accepted safety evidence.

### Answer 5

Trace stakeholder mobility/accessibility/safety needs and operational scenarios to system requirements; hazards for collision, unsafe stop, door, battery/fire, remote-control loss, and emergency interaction; threats/assets/trust boundaries; regulatory/road obligations; and human oversight authority/workload. Decomposition and allocation edges connect sensing, localization, planning, control, actuation, communications, remote supervision, passenger interaction, maintenance, infrastructure, and emergency services, with interface and common-cause rationale.

Supplier nodes include exact hardware/software/model/data/configuration, claims, certificates, limitations, change/vulnerability notices, and acceptance. Implementation traces reach software/hardware builds, calibration, datasets/models, procedures, training, and deployed variants. Verification links preserve procedures, environments, simulations/test articles, oracles, fault/adversarial cases, results, anomalies, waivers, and dispositions; validation links representative passengers, roads, weather, traffic, accessibility, remote-operator workload, and emergency outcomes.

Change traversal covers interfaces, safety/security cases, maps/models/data, suppliers, tests, operations, training, maintenance, regulators, and deployed fleets. Independent safety/security/human-factors/domain reviews validate critical paths and graph snapshots. Trace supports the assurance case but cannot prove shuttle safety, legal conformity, or ethical acceptability; affected stakeholders, road/transport, safety, cybersecurity, accessibility, emergency, labor/operations, supplier, and regulatory authorities must decide applicable claims. No external review is claimed.
