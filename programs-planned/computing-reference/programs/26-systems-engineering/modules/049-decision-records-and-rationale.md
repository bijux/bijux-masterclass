---
module_id: SYSENG-049
program: Systems Engineering
level: 1
module_number: 49
title: Decision Records and Rationale
status: complete
last_verified: 2026-08-31
---

# Decision Records and Rationale

## One-Page Review

### Governing question

What durable record lets a future engineer reconstruct what was decided, by whom, for which configured system and objectives, from which alternatives and evidence, under what uncertainty and constraints, with which accepted consequences—and know when to reopen it?

### Essential definitions

- A **decision need/question** is the precise choice, commitment, authorization, exception, or deferral requiring accountable resolution.
- A **decision authority** is the role/person empowered and accountable to make the decision within a defined scope; analysts and recommenders may differ.
- A **decision record** is a durable, uniquely identified, configuration-controlled account of context, alternatives, evaluation, recommendation, final decision, rationale, consequences, authority, implementation, and lifecycle.
- **Rationale** is the explicit reasoning that links objectives, evidence, assumptions, criteria, tradeoffs, uncertainty, risks, values, and constraints to the selected action.
- A **decision log/register** indexes records and their status, authority, scope, dependencies, implementation, and supersession; it is not a substitute for each substantive record.
- A **decision baseline** is the exact system/configuration, requirements, interfaces, ConOps, lifecycle, data date, stakeholder set, evidence, models, preferences, and policies to which the decision applies.
- An **alternative** is a feasible or considered course of action, including status quo/no action, defer/information acquisition, staged/reversible options, and recorded rejected/pruned options where relevant.
- A **constraint** is a mandatory boundary; a **criterion** differentiates alternatives; an **assumption** is a claim accepted for analysis and subject to evidence/change.
- A **recommendation** is the analyst/team's proposed action. The **final decision** is the authority's choice and can differ, with rationale.
- A **decision consequence** includes intended outcomes and accepted adverse tradeoffs, residual risks, obligations, costs, schedule, stakeholder impacts, and option loss.
- **Dissent/nonconcurrence** is a preserved, attributable disagreement about framing, evidence, analysis, recommendation, authority, or consequence; disposition does not erase it.
- **Supersession** links a later authorized decision that replaces or changes an earlier decision under new evidence/context. The earlier record remains historical evidence.
- A **reopening trigger** is an observable change in evidence, assumptions, constraints, configuration, outcomes, risks, stakeholder values, or environment that requires reassessment.

### Central model, mechanism, or theorem

Represent a decision record at time $t$ as

$$
D_t=(id,Q,A,B,O,C,X,E,M,U,R,\delta,J,K,I,H),
$$

where $Q$ is question, $A$ authority, $B$ baseline, $O$ objectives, $C$ criteria/constraints, $X$ alternatives, $E$ evidence, $M$ evaluation method/model, $U$ uncertainty/sensitivity, $R$ risks, $\delta$ the selected decision, $J$ rationale/dissent, $K$ consequences/conditions, $I$ implementation/monitoring, and $H$ history/supersession.

Traceability forms a directed argument graph:

$$
objectives\rightarrow criteria\rightarrow evidence/model\rightarrow alternative\ outcomes
\rightarrow recommendation\rightarrow authority\ decision\rightarrow implementation/effects.
$$

The graph supports reconstruction and challenge; it does not make the decision objectively true. A later decision $D_{t+1}$ may supersede $D_t$, but must preserve the prior node and state the changed premises and resulting delta.

### Critical invariants

- Every consequential decision has a stable unique identifier, exact question, scope, owner, decision authority, date/deadline, status, and applicable baseline/configuration.
- Objectives, affected stakeholders/risk takers, constraints, criteria, preference authority, and success/acceptance conditions are explicit.
- Alternatives considered, generated, screened, pruned, rejected, deferred, and selected retain comparable descriptions and reasons; status quo is included when meaningful.
- Evidence and analysis link to immutable/versioned sources, methods, data dates, configurations, results, uncertainty, sensitivity, limitations, and reviewers.
- Facts, estimates, assumptions, value judgments, policy constraints, recommendations, and authority decisions remain distinguishable.
- Final rationale explains why the selected option fits objectives under current knowledge, including why close/higher-scoring alternatives were not selected.
- Accepted tradeoffs, residual risks, safety/security/legal/ethical implications, stakeholder distribution, dissent, and evidence gaps are visible rather than backfit into scores.
- Implementation owner, resources, conditions, actions, verification/validation, monitoring, decision effectiveness, and reopening triggers are part of the record.
- Approval/signature/authentication, access classification, retention, and links to formal configuration/risk/safety/security systems follow governing policy.
- Records are append-only in meaning: corrections and status changes have audit history; supersession never overwrites the original context or rationale.
- Linked requirements, architecture, interfaces, risks, waivers, changes, tests, and downstream decisions can be traversed in both directions.
- Emergency/rapid decisions may compress analysis, but the record is reconstructed promptly with evidence limits and after-action review.

### Common failures

Common failures include recording only “approved”; relying on meeting minutes or slide decks without a canonical record; omitting the question or authority; recording a decision for “the system” without configuration; documenting only the chosen option; inventing reasons for alternatives after selection; citing mutable dashboards/URLs without snapshots; mixing facts, assumptions, and values; hiding uncertainty and dissent; treating a weighted score as rationale; changing weights after a lower-scoring option is selected; omitting affected groups and noncompensatory constraints; recording recommendation as decision; excluding implicit risk acceptance in release/waiver/delivery; failing to name implementation conditions; declaring success from implementation rather than outcomes; editing old decisions to match current architecture; deleting rejected/superseded records; and never triggering review when premises fail.

### Compact example

Decision DR-017 selects a distributed control architecture for configuration B3. It names the authority, requirements and care settings; compares centralized, distributed, hybrid, status quo, and staged-pilot options; links safety, latency, reliability, cost, schedule, security, human-workload, and maintenance evidence with uncertainty; preserves clinical/operations dissent; and explains why distributed resilience outweighs higher lifecycle burden under approved values. Conditions require a pilot, interface verification, staffing, rollback, residual-risk acceptance, and six-month outcome review. A later supplier change produces DR-024, which supersedes—not rewrites—DR-017 and identifies changed assumptions/evidence.

### Connections

SYSENG-041–048 produce objectives, trade evidence, forecasts, uncertainty, readiness and risk decisions. This module preserves their logic and accountability. SYSENG-050 uses that record discipline for architecture choice. Every later requirement, interface, verification, configuration, supplier, operations and lifecycle decision depends on recoverable rationale rather than organizational memory.

## Governing Question

Could a competent reviewer who was absent from the project reproduce the decision frame and reasoning, identify what was known and unknown, distinguish recommendation from authority choice, understand consequences and dissent, and determine whether today's changed conditions still satisfy the original rationale?

If not, the team owns a decision artifact but not a durable decision record. Screenshots, minutes, emails, chat, issue comments, models, and approvals can be evidence, but each has different authority and persistence. The canonical record binds them to one decision and preserves its lifecycle.

## Why This Matters

Systems outlive teams. Without rationale, engineers repeat analyses, retain constraints whose reasons vanished, remove essential controls, or treat obsolete decisions as permanent truth. Investigators and operators cannot distinguish bad implementation from changed assumptions or a deliberately accepted trade. Governance becomes personality-dependent.

NASA's current Decision Analysis guidance calls for a report containing mission/system context, decision need and intended outcomes, criteria, alternatives, methods/tools, assumptions, uncertainty/sensitivity, evaluation results, recommendation, final decision and rationale, and lessons. Technical Assessment similarly calls for key decisions, supporting rationale, assumptions and lessons to be captured. Configuration and technical-data management preserve identity, change, access, integrity and lifecycle records.

GAO analysis-of-alternatives work emphasizes a single understandable record of methods, assumptions/constraints, alternatives, results, recommendation and detailed rationale that independent reviewers can reconstruct without a predetermined solution. SEI architecture-documentation guidance treats rationale and rejected alternatives as essential because future teams otherwise revisit decisions or misimplement them. The durable principle extends beyond software: record enough to preserve legitimate change, not enough to freeze history.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. decision policy, authority/RACI, forums, thresholds, technical authority/dissent, signatures, records retention, access/security, emergency and escalation rules;
2. exact decision question, deadline, reversibility, system/lifecycle/configuration boundary, ConOps, objectives, requirements, constraints, stakeholders/risk takers, and decision criteria;
3. alternatives and generation/pruning history, status quo, staged/defer/information/fallback options, architectures/interfaces, maturity and implementation descriptions;
4. raw evidence and provenance, models/code/data, measurements/tests, cost/schedule, performance, uncertainty/sensitivity, risks/readiness, reviews and conflicts;
5. recommendation, final authority action, meeting/approval evidence, conditions, waivers, accepted residual risks, dissent, and commitments;
6. implementation/change/configuration plan, owners/resources/schedule, verification/validation, outcome measures, monitoring, contingency/rollback and reopening triggers;
7. existing decision log, requirements/model repositories, data/configuration management, risk/hazard/security records, issues/changes and prior/superseding decisions.

As a retrieval test, inspect “Decision: use vendor X—approved 12 May.” Ask for decision question, authority, baseline, alternatives, criteria, conflicts, comparable supplier evidence, uncertainty, recommendation, why X, accepted lock-in/security/continuity risks, contract/configuration, implementation conditions, dissent and reopen triggers. If these live only in memory, the record is incomplete.

## Learning Objectives

After completing this module, you should be able to:

1. identify which choices require durable records and tailor rigor without losing core accountability;
2. define a canonical decision-record schema and lifecycle;
3. separate context, evidence, assumptions, values, analysis, recommendation, authority decision and rationale;
4. preserve considered/rejected/deferred alternatives and pruning logic fairly;
5. bind evidence and models to exact versions/configurations with uncertainty and limits;
6. document accepted tradeoffs, residual risks, stakeholder distributions, dissent and implicit acceptance;
7. connect decisions bidirectionally to requirements, architecture, interfaces, risks, changes, tests and implementation;
8. govern review, approval, authentication, access, correction, retention, supersession and emergency capture;
9. define implementation/outcome evidence and reopening triggers;
10. audit decision history for completeness, consistency, orphan links, stale premises and realized effectiveness.

## Core Exposition

**Decide what deserves a record.** Record choices with material lifecycle cost, safety/security/privacy, architecture/interface, requirement, supplier, operational, stakeholder, regulatory, risk acceptance, waiver, irreversibility, or cross-team consequence. Small local choices can use lighter templates; high-stakes decisions need analysis packages and formal approval. A decision log should reveal omissions without creating paperwork for every line of code.

**Assign stable identity and authority.** Use a unique durable ID, descriptive title, decision owner, record custodian, authority role/person, required concurrences, forum, date/deadline, status and scope. Never reuse IDs. Authenticate approval according to policy. “The team decided” obscures accountability and whether authority existed.

**State the question as a choice.** Describe what must be decided now, why, by when, what commitments follow, and what is out of scope. Separate decision from problem statement and desired answer. Record whether deferral/no action is feasible and the consequence of missing the deadline.

**Fix the decision baseline.** Identify system/product/version/configuration, lifecycle, mission/use context, architecture/interfaces, quantities, environment, operations/support, stakeholder population, requirements, evidence cutoff and analysis versions. The same choice under a different scale, supplier, patient group, workload or threat is a different decision or supersession.

**State objectives and constraints before results.** Trace stakeholder outcomes, mandatory requirements, laws/policies, safety/security/ethical boundaries, affordability/schedule, and enhancing criteria. Record operational definitions, value/utility functions and preference authority where used. Do not backfit a new objective after a favored alternative loses.

**Preserve stakeholder and role structure.** Identify affected groups, evidence producers, analysts, domain/independent reviewers, recommenders, technical authority, decision authority, implementers and risk takers. Record conflicts and participation gaps. Consultation is not decision authority, and authority does not make technical claims true.

**Describe alternatives comparably.** For each option record boundary, functions, architecture/interfaces, lifecycle/operations, maturity, cost/schedule, risks, dependencies, assumptions and evidence strength. Include status quo, do nothing, defer/information, staged/reversible and fallback when meaningful. Avoid a detailed preferred design against vague competitors.

**Record generation and pruning.** Explain how the trade space was searched and why options were screened, rejected, combined or deferred. Name mandatory criterion, evidence, uncertainty, authority and reconsideration trigger. Preserve promising rejected alternatives: later evidence may change feasibility.

**Bind evidence immutably.** Link controlled requirement/model/data/test/report/code/configuration identifiers, versions, hashes or archival snapshots as appropriate. Record source, date, owner, method, quality, applicability, uncertainty, conflicts and limitations. A link to a mutable dashboard does not preserve what the authority saw.

**Describe methods and calculations.** Record analysis plan, scales, weights, models, formulas/code, scenarios, cost/schedule horizons, discounting, normalization, dependencies, sensitivity, validation/review and reproducible outputs. Summary prose should link to drill-down evidence. Hidden spreadsheet formulas or undocumented expert scores cannot support future reconstruction.

**Separate epistemic layers.** Label measured facts, model estimates, assumptions, forecasts, expert judgments, stakeholder values, legal/policy constraints and authority choices. A final decision can legitimately use value or portfolio considerations outside a technical score; record them rather than altering technical evidence.

**Report uncertainty and robustness.** Show ranges/distributions/scenarios, evidence gaps, correlations, sensitivity, break-even boundaries, close rankings, value of information, model disagreement and applicability. State what could change recommendation or decision. “Best” is conditional on current evidence and values.

**Write the recommendation independently.** Name recommender/team, preferred action, evidence/rationale, alternatives considered, assumptions, conditions, residual risks and confidence. If no robust winner exists, recommend information, staging or present close options. Preserve recommendation even if authority chooses differently.

**Record the final decision verbatim enough.** State selected/rejected/deferred action, authority, date, effective scope/configuration, conditions, required concurrences, funding/resource or schedule limits, waivers, and review date. Attach signed minutes/directive/approval as evidence while keeping the canonical statement readable.

**Explain why.** Rationale traces the selected option to objectives, constraints, evidence and values; compares key alternatives; identifies decisive factors and uncertainty; and explains deviations from recommendation or score. Avoid “best balance” without naming the balance. Do not sanitize political, portfolio or schedule constraints when they legitimately governed authority choice.

**Record consequences and obligations.** Capture expected benefits, sacrifices, residual risks, safety/security/privacy/legal/ethical effects, affected stakeholder distribution, technical debt, supplier/lock-in, lifecycle cost, option loss, assumptions, follow-on decisions, and commitments. Link formal risk acceptance and waivers to proper authority systems.

**Preserve dissent and nonconcurrence.** Record who disagreed (subject to appropriate protections), basis/evidence, consequence, response/disposition, escalation and final authority rationale. Do not rewrite dissent as consensus. Sensitive personnel/security detail can use controlled linked records while preserving decision significance.

**Define implementation.** Name owners, work products, resources, dependencies, milestones, configuration changes, interface/contract updates, transition, contingency/rollback, communication and downstream records. A decision not translated into controlled action is not complete governance.

**Define success and monitoring.** Distinguish implementation verification (“we built/contracted/deployed the decision”) from outcome validation (“it achieved intended objectives without unacceptable consequences”). Specify measures, populations/scenarios, evidence, cadence, owner, thresholds and review. Feed actual outcomes back into models and lessons.

**Predeclare reopening triggers.** Include requirement/objective/value change; assumption invalidation; evidence/model update; risk/readiness threshold; cost/schedule overrun; supplier/technology/configuration/interface/environment change; adverse outcome/incident; new stakeholder/legal obligation; failed validation; or superior alternative. Define who monitors and who can reopen.

**Use explicit statuses.** Example lifecycle: proposed, under analysis, recommended, decided/accepted, implementing, validated, deferred, rejected, superseded or withdrawn. Tailor terms, define transitions/authority, and keep decision status separate from implementation status. “Accepted” should not ambiguously mean risk acceptance.

**Supersede; do not rewrite.** A new record cites the prior decision, changed premises/evidence, delta analysis, new authority choice, migration and affected downstream artifacts. Mark prior status with a link but retain its content and historical validity. Correct factual errors through versioned errata/audit trail, not silent edits.

**Manage decisions as a graph.** Link parent/child and prerequisite decisions, requirements, architecture elements, interfaces, risks, hazards, changes, tests, suppliers and records. Detect circular dependencies and orphan decisions. A decision impact analysis traverses downstream implementation and evidence before change.

**Protect and retain records.** Apply classification, privacy, procurement, export-control, legal privilege, safety/security and retention rules. Provide a decision-capable summary to appropriate stakeholders while restricting exploit/personnel detail. Ensure format/tool longevity, export and repository ownership.

**Handle emergency decisions.** Capture authority, situation, options considered, immediate evidence/uncertainty, chosen action, safety constraints, communication and review time even if analysis is compressed. Reconstruct the complete record promptly, validate consequences and conduct after-action review. Urgency shortens cycle; it does not erase accountability.

**Audit records and rationale.** Sample high-impact, rejected, emergency and superseded decisions. Check required fields, source immutability, alternatives, reproducibility, authority, dissent, risk acceptance, conditions, implementation/outcome evidence, trigger monitoring, stale assumptions, supersession links, orphaned downstream artifacts and actual effectiveness. A complete template with empty reasoning is not a good record.

The following checker validates the structural history of two declared records. It cannot judge whether their rationale or decisions are substantively correct.

<!-- bijux-verify: {"id":"decision-record-history-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"decision_count=2\nunique_ids=1\nrequired_fields_complete=2\nevidence_links=4\nrejected_alternatives_recorded=2\nauthorities=2\ndissent_fields=2\nreopen_triggers=2\nsupersession_edges=1\norphan_supersession=0\ncycle_detected=0\nstatus=decision_history_consistent\nevidence=declared_records_only\n","stderr":""}} -->
```python
required = ("question", "baseline", "alternatives", "evidence", "decision",
            "rationale", "authority", "dissent", "implementation", "reopen")
records = [
    {"id": "DR-017", "status": "superseded", "question": "choose control allocation",
     "baseline": "B3", "alternatives": ["central", "distributed", "hybrid"],
     "rejected": ["central"], "evidence": ["EV-41", "TS-09"],
     "decision": "distributed", "rationale": "fault isolation under approved values",
     "authority": "architecture board", "dissent": "operations workload concern",
     "implementation": "pilot and interface verification", "reopen": "supplier change",
     "supersedes": None},
    {"id": "DR-024", "status": "decided", "question": "revise control allocation",
     "baseline": "B4", "alternatives": ["distributed-v2", "hybrid"],
     "rejected": ["distributed-v2"], "evidence": ["EV-63", "TS-14"],
     "decision": "hybrid", "rationale": "changed supplier and workload evidence",
     "authority": "architecture board", "dissent": "migration timing concern",
     "implementation": "controlled migration and rollback", "reopen": "pilot threshold breach",
     "supersedes": "DR-017"},
]
ids = {record["id"] for record in records}
edges = [(record["id"], record["supersedes"]) for record in records if record["supersedes"]]

def has_cycle(edges):
    parent = {child: prior for child, prior in edges}
    for start in parent:
        seen, node = set(), start
        while node in parent:
            if node in seen:
                return True
            seen.add(node)
            node = parent[node]
    return False

print(f"decision_count={len(records)}")
print(f"unique_ids={int(len(ids) == len(records))}")
print(f"required_fields_complete={sum(all(record.get(field) for field in required) for record in records)}")
print(f"evidence_links={sum(len(record['evidence']) for record in records)}")
print(f"rejected_alternatives_recorded={sum(bool(record['rejected']) for record in records)}")
print(f"authorities={sum(bool(record['authority']) for record in records)}")
print(f"dissent_fields={sum('dissent' in record for record in records)}")
print(f"reopen_triggers={sum(bool(record['reopen']) for record in records)}")
print(f"supersession_edges={len(edges)}")
print(f"orphan_supersession={sum(prior not in ids for _, prior in edges)}")
print(f"cycle_detected={int(has_cycle(edges))}")
complete = len(ids) == len(records) and all(all(r.get(f) for f in required) for r in records)
complete &= not any(prior not in ids for _, prior in edges) and not has_cycle(edges)
print("status=" + ("decision_history_consistent" if complete else "decision_history_needs_work"))
print("evidence=declared_records_only")
```

The checker counts nonempty dissent fields but does not establish that dissent was candid, fairly dispositioned, or accessible to the correct authority.

## Definitions and Notation

Let record graph $G_D=(V_D,E_D)$ have vertices for decisions, requirements, evidence, models, risks, architecture elements, changes and outcomes. Typed edges include supports, contradicts, assumes, constrains, selects, rejects, implements, verifies, affects and supersedes.

Decision record identity:

$$
D=(id,version,status,scope,baseline,authority,date,content,links,history).
$$

Rationale can be represented as claims $c$, evidence $e$, warrants/assumptions $w$, counterarguments $q$, and authority/value premises $v$:

$$
J=(c,e,w,q,v,limitations).
$$

This structure improves challenge; it does not eliminate judgment.

Supersession:

$$
D_j\xrightarrow{supersedes}D_i,qquad date(D_j)>date(D_i),
$$

with an acyclic historical relation and explicit premise/configuration delta. Corrections retain version history without changing the original authority event silently.

The decision-validity predicate at current time $t$ is an assessment:

$$
Valid_t(D)=baseline\ compatible\land assumptions\ hold\land conditions\ met
\land no\ reopening\ trigger.
$$

It is never inferred from status alone.

## Mechanisms, Invariants, or Proof Structure

**Mechanism 1—identity and framing.** Decide record threshold; fix question, authority, baseline, objectives, stakeholders, constraints, deadline and repository.

**Mechanism 2—alternative/evidence preservation.** Describe comparable options and pruning; bind controlled data/models/methods, assumptions, uncertainty, risk and independent review.

**Mechanism 3—recommendation and authority rationale.** Preserve analyst recommendation, final choice, decisive reasoning, dissent, accepted tradeoffs/risks, conditions and authentication.

**Mechanism 4—implementation and validation.** Link work/configuration/resources, verify implementation, assess outcomes, monitor premises and triggers.

**Mechanism 5—history and change.** Protect/retain, audit graph integrity, supersede rather than rewrite, propagate impacts and learn from effectiveness.

A record supports accountability and reuse only under truthful, complete-enough inputs and functioning governance. Documentation cannot make biased analysis, illegitimate authority or unethical values acceptable.

## Alternatives and Trade-Offs

**Lightweight templates** lower friction and fit local reversible choices. **Formal decision reports/boards** support high-consequence accountability but cost time. Tailor rigor to consequence, uncertainty, cross-boundary impact and reversibility.

**Central registers** improve discovery and portfolio linkage. **Local repository-near records** improve use by implementers. Federate stable IDs/metadata and preserve one canonical source.

**Structured fields** enable validation/search/graphs. **Narrative** captures nuance, uncertainty and dissent. Use both; a schema is not rationale.

**Append-only history** protects truth. **Correctable records** handle errors. Use auditable versions/errata and supersession, not silent immutability or silent mutation.

**Broad transparency** improves trust/review. **Restricted records** protect security/privacy/procurement. Provide tiered views and accountable access.

**Automation** can validate fields, links, staleness and cycles. **Human review** evaluates evidence, fairness, reasoning and authority. Neither replaces the other.

## Failure Modes and Misconceptions

**“Meeting minutes are the decision record.”** They may omit baseline, alternatives, evidence, authority rationale, consequences and lifecycle.

**“The highest score is the rationale.”** Scores are conditional model outputs; rationale explains scale, uncertainty, constraints, tradeoffs and authority judgment.

**“Only the chosen alternative matters.”** Rejected options and reasons prevent repetition and enable reopening under changed premises.

**“Recommendation equals decision.”** Preserve both roles and any divergence.

**“Consensus means no dissent field is needed.”** Record absence, participation and unresolved concerns; silence may reflect incentives.

**“Approved means permanently valid.”** Approval applies to a baseline and premises; triggers can invalidate it.

**“Updating the old record keeps docs clean.”** It destroys historical truth; supersede with explicit deltas.

**“Implementation proves the decision worked.”** Validate outcomes and adverse consequences.

**“Sensitive means undocumented.”** Use controlled records and decision-capable summaries.

**“More prose means better rationale.”** Traceable decisive reasoning beats volume without evidence.

## Worked Examples

### Example 1

**Recommendation differs.** Analysis recommends A; authority selects B because portfolio cash constraint excluded from the model is legitimate. Record both, quantify constraint/trade, update model for future use, and preserve residual risk. Do not change weights until B wins.

### Example 2

**Status quo rejection.** Status quo fails a new legal constraint on a stated date. Record the requirement/source and transition consequence; do not silently omit it from alternatives.

### Example 3

**Pruned option reopens.** Option C was rejected because no qualified supplier existed. A supplier later qualifies. The trigger creates a new decision/reassessment linked to C's prior rationale, rather than pretending C was never considered.

### Example 4

**Evidence snapshot.** A capacity decision uses dashboard data and simulation commit. Store dataset/query/time window/configuration/hash, model version and report output; a future live dashboard cannot reconstruct the evidence.

### Example 5

**Dissent.** Safety authority argues testing omitted a rare boundary. Record evidence, consequence, response and escalation. Final authority can defer, test, accept under policy, or reject; minutes cannot convert dissent into consensus.

### Example 6

**Implicit risk acceptance.** Release proceeds without two planned tests. Link waiver, affected risk scenarios, technical concurrence, risk-taker conditions, monitoring/rollback and accountable rationale. “Schedule approved” is insufficient.

### Example 7

**Implementation versus outcome.** Vendor migration completes, but latency and operator workload exceed decision thresholds. Record implementation verified but outcome not validated; trigger reassessment/rollback instead of marking the decision successful.

### Example 8

**Supersession.** DR-024 changes DR-017 after supplier and workload changes. The new record lists premise/evidence delta, migration and downstream impact; DR-017 remains valid history for B3.

### Example 9

**Emergency action.** During an incident, authority isolates a subsystem from three rapid options under uncertain telemetry. Capture immediate rationale/constraints and review deadline; reconstruct evidence and effects after stabilization.

### Example 10

**Orphan audit.** A requirement cites DR-031, but the record is missing; a superseded architecture remains in an interface document. Stop change approval, recover/authorize rationale and propagate current decision links before claiming traceability.

## Cross-Program Connections

**Platform engineering.** Record platform/vendor, tenancy, SLO, migration, security, developer experience and governance choices with workload evidence, adopters, exit costs and reopen triggers.

**API and service engineering.** Protocol, consistency, versioning, decomposition, retry, auth and deprecation decisions need consumer/provider evidence, compatibility and migration obligations.

**Data engineering.** Format, schema, storage, orchestration, retention, quality, privacy and lineage decisions require workload/data snapshots and recovery/migration consequences.

**Object-oriented programming.** Pattern, framework, inheritance/composition, dependency and module-boundary decisions should link code/configuration, quality scenarios, rejected designs and evolution evidence.

**Functional programming.** Effect/type/runtime, state/concurrency, evaluation, library and migration choices require benchmark/workload/team/operations evidence and explicit formal-versus-empirical claims.

## References

1. NASA, *Systems Engineering Handbook, Section 6.8: Decision Analysis*, current web edition. <https://www.nasa.gov/reference/6-8-decision-analysis/>
2. NASA, *Systems Engineering Handbook, Section 6.6: Technical Data Management*, current web edition. <https://www.nasa.gov/reference/6-6-technical-data-management/>
3. NASA, *Systems Engineering Handbook, Section 6.5: Configuration Management*, current web edition. <https://www.nasa.gov/reference/6-5-configuration-management/>
4. NASA, *Systems Engineering Handbook, Section 6.7: Technical Assessment*, current web edition. <https://www.nasa.gov/reference/6-7-technical-assessment/>
5. NASA, *Systems Engineering Handbook, Section 4.4: Design Solution Definition*, current web edition. <https://www.nasa.gov/reference/4-4-design-solution-definition/>
6. NASA, *NASA Risk-Informed Decision Making Handbook*, NASA/SP-2010-576. <https://ntrs.nasa.gov/citations/20100021361>
7. NASA, *Systems Engineering Processes and Requirements*, NPR 7123.1D, current directive. <https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_7123_001D_&page_name=Chapter6>
8. U.S. GAO, *DOE and NNSA Project Management: Analysis of Alternatives Could Be Improved by Incorporating Best Practices*, GAO-15-37. <https://www.gao.gov/products/gao-15-37>
9. U.S. GAO, *Joint Intelligence Analysis Complex: DOD Partially Used Best Practices for Analyzing Alternatives*, GAO-16-853. <https://www.gao.gov/products/gao-16-853>
10. Carnegie Mellon Software Engineering Institute, *Creating and Using Software Architecture Documentation Using Web-Based Tool Support*, CMU/SEI-2004-TN-037. <https://resources.sei.cmu.edu/asset_files/TechnicalNote/2004_004_001_14351.pdf>

## Exercises

### Exercise 1

Transform “Approved cloud provider A because it is best” into a complete decision-record outline covering question, baseline, authority, alternatives, evidence, criteria, uncertainty, rationale, dissent, consequences, implementation and reopening.

### Exercise 2

A weighted analysis ranks A=0.73 and B=0.70, but authority selects B due to a binding portfolio constraint excluded from the charter. Explain how to record the recommendation, decision and model consequence without manipulating scores.

### Exercise 3

Design a supersession record when a previous component-selection decision assumed supplier availability, operating temperature and annual volume that have all changed. Include impact propagation and historical handling.

### Exercise 4

Audit a repository containing 80 records where 20 link live dashboards only, 15 omit rejected alternatives, 12 say “team consensus” without authority, 10 have no reopen trigger, five superseded records were overwritten, and three safety dissents exist only in email.

### Exercise 5

Design a decision record for selecting a flood-warning and evacuation communication architecture across sirens, mobile alerts, radio, social/community networks and door-to-door support. Cover authorities, communities, hazards, power/network failure, languages/accessibility, privacy, uncertainty, tradeoffs, implementation, drills, residual risks, dissent and reopening.

## Answers to the Exercises

### Answer 1

Use a stable ID/title/status and state: “Which cloud/service architecture should host workloads W under configuration/release B, regions/users, lifecycle and migration deadline?” Name decision owner, accountable authority, technical/security/privacy/procurement concurrences, forum/date/deadline, reversibility and record custodian.

Baseline exact workloads, data classes/residency, traffic/tails, regions, integrations, identity/network, SLO/RTO/RPO, threat/compliance, team/operations, contract horizon, current provider, architecture/configuration and evidence cutoff. Define mandatory constraints and criteria: reliability/common cause, latency/capacity, security/privacy, portability/exit, developer/operations, support, sustainability and lifecycle cost/schedule under legitimate preference authority.

Comparably describe provider A, B, multi-provider, self-host/status quo, staged pilot/defer and fallback. Preserve generation/pruning and conflicts. Link controlled workload datasets/queries, benchmarks, incidents, architecture/security/privacy/legal assessments, cost models/quotes, contract terms, migration pilots, staffing evidence, provider reports, assumptions, model/code versions, uncertainty/sensitivity and independent review.

Record analyst recommendation separately; authority's selected option and verbatim conditions; rationale naming decisive evidence/values and why close/rejected options lose; dissent and disposition; accepted lock-in, provider concentration, migration, outage, security/privacy, cost, skill and exit tradeoffs; waivers/risk acceptance; and affected stakeholders.

Implementation includes contract, landing zone, controls, observability, data migration, testing, training, staged cutover, rollback/exit, owners/resources/dates and downstream configurations. Validate SLO/cost/security/developer/operations/migration outcomes. Reopen on workload/data/legal/threat/provider/price/SLO/incident, acquisition, support, region, architecture, exit-test or stakeholder-value change. Retain signed approval and evidence snapshots; supersede rather than edit.

### Answer 2

Preserve the analysis exactly: charter, scales, weights, evidence, uncertainty, A=0.73, B=0.70, close margin, recommendation and limitations. Record that the analysis team recommends A under the chartered objective model. The authority selects B because the binding portfolio constraint—name amount, timing, source, authority and evidence—was outside the study model but governs the actual decision.

Explain the trade: what benefit A loses, what B satisfies, residual risks/conditions, whether the excluded factor should have been a constraint/criterion, and implications for future studies. Do not change weights or cells after selection. If the constraint legitimately changes the decision frame, run a versioned supplementary analysis while retaining the original. Record dissent, acceptance, implementation, monitoring and trigger if the portfolio constraint relaxes or A/B evidence changes.

### Answer 3

Create a new ID that cites/supersedes the prior ID; do not edit prior content. State old and new baselines: supplier identity/capacity/status, temperature profile/range/cycles/environment and annual/lifecycle volume, plus affected component/version/system/interface. Preserve original validity for its date/configuration.

Describe triggers and exact premise/evidence delta; identify requirements, architecture, thermal/power/mechanical/electrical/software interfaces, qualification, manufacture/yield, quality, spares/maintenance, cost/schedule, contract, risks, verification and operational documents affected. Reopen old alternatives and generate new ones: alternate component/supplier, redesign, derating/environment control, inventory, volume/process change, staged qualification or requirement relief.

Run controlled comparison with current evidence/uncertainty and dependency/lead-time analysis. Record recommendation, authority decision/rationale, dissent, accepted risks, fallback and migration/cut-in/lot traceability. Propagate changes through requirements/configuration/BOM/drawings/code/ICDs, supplier/contract, tests/qualification, WBS/schedule/cost/risk, operations/spares and downstream decisions. Verify implementation and target-temperature/volume outcomes; define triggers for supplier/process/temperature/volume/anomaly/obsolescence change.

### Answer 4

Freeze destructive edits and inventory record IDs/status/authority/scope. For live-dashboard-only records, recover immutable snapshots or reconstruct the exact query/time window/data/configuration/model reviewed; label irrecoverable evidence gaps and reassess material decisions. Add considered/rejected alternatives and contemporaneous reasons from source evidence without fabricating rationale; where unavailable, mark unknown and reopen if consequential.

Resolve “team consensus” by finding formal authority/approval or obtaining ratification/redecision; distinguish consultation, recommendation, concurrence and decision. Add monitored, observable reopening triggers tied to assumptions/evidence/outcomes. Restore overwritten records from version control/backups/audit logs; create explicit supersession edges/deltas and correct downstream statuses. Move safety dissents into governed decision/safety systems with appropriate protection, preserve original text/evidence/date/disposition/escalation and ensure accountable authority review.

Then automate structural checks for required fields, immutable evidence, unique IDs, authorities, alternatives, triggers, access, orphan/cyclic supersession and stale review, while humans audit reasoning, fairness, bias, conflicts, stakeholder coverage, uncertainty, risk acceptance, implementation/outcome evidence and actual effectiveness. Prioritize safety/security/legal and irreversible/high-impact decisions; record remediation as new audited history, not silent cleanup.

### Answer 5

Frame which architecture and governance will issue actionable warnings/evacuation support for specified river/coastal/pluvial hazards, zones/populations, lead times and lifecycle. Name emergency/public-safety decision authority, meteorological/hydrological evidence roles, municipal/regional coordination, telecom/media/operators, disability/language/community representatives, privacy/security/legal concurrence and actual risk-taker/public authority. Define trigger and urgent-decision processes.

Baseline hazard scenarios/uncertainty, maps/topography, power/cellular/radio availability, siren coverage, device ownership, hearing/vision/cognitive/mobility needs, languages/literacy, trust, visitors, institutions, transport/shelters, night/weather, network congestion, misinformation and door-to-door staffing. Objectives include timely reach/comprehension/action, geographic/demographic equity, reliability/common cause, privacy/security, responder safety, maintainability, drills, cost and recovery. Preserve noncompensatory life-safety/access requirements.

Compare siren-only, mobile alert, broadcast radio, social/community relays, door-to-door, and layered combinations with status quo, staged pilots and fallback. Link propagation/coverage tests, alert delivery/congestion, power/network models, human-factors/accessibility/language studies, exercises, community evidence, privacy/security threat analysis, staffing/transport/shelter, cost/schedule, uncertainty/sensitivity and common-cause scenarios. Avoid averaging away unreached groups.

Record recommendation and final choice/rationale, decisive tradeoffs, rejected options, dissent, residual false-negative/false-positive, outage, privacy, misinformation, accessibility, staffing and responder risks, and formal acceptance. Conditions include redundant authority/authentication, accessible multilingual templates, backup power/radio, community/door-to-door protocols, monitoring and safe escalation.

Implementation specifies ownership, infrastructure, data protection, maintenance, training, drills by conditions/community, communication, contingency/rollback and configuration. Validate end-to-end warning-to-action outcomes, not message transmission alone. Reopen on hazard/map/climate, population/language/accessibility, infrastructure/provider, power/network, regulation/privacy/threat, drill/incident/near-miss, coverage inequity, trust, staffing, technology or cost changes. Preserve controlled sensitive security detail and public decision-capable rationale.
