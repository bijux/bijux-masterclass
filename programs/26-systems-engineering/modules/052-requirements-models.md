---
module_id: SYSENG-052
program: Systems Engineering
level: 2
module_number: 52
title: Requirements Models
status: complete
last_verified: 2026-08-31
---

# Requirements Models

## One-Page Review

### Governing question

How can a requirements model preserve normative meaning, stakeholder intent, applicability, measurable acceptance, rationale, derivation, allocation, verification and change history as computable engineering knowledge—without confusing trace links or design assertions with evidence that a requirement is necessary, satisfied or verified?

### Essential definitions

- A **requirement** is a uniquely identified, authoritative statement of an obligation or constraint on a defined subject under stated conditions.
- A **requirement model** is a governed semantic collection of requirement objects, attributes, relationships, rules, configurations and concern-oriented views—not merely prose imported into a diagram.
- A **normative statement** expresses what the obligated subject shall do or be. Rationale, notes, examples and verification guidance are informative unless separately made normative.
- A **stakeholder requirement** states a validated stakeholder-needed outcome or constraint; a **technical requirement** translates the problem into design-to and verification-capable obligations at a product level.
- A **requirement pattern** separates subject, modal, action, object, condition, measure, threshold, tolerance and units so ambiguity and missing information can be detected.
- **Applicability** defines product/variant, lifecycle, mode/state, environment, population, interface, jurisdiction and effective configuration for which the obligation holds.
- A **source** is the authorized need, parent requirement, law, standard, interface agreement, hazard control, decision or other origin that justifies the requirement.
- **Rationale** explains why the obligation and its values exist, including assumptions, consequences and relevant decisions; it is not a second hidden requirement.
- **Derivation** creates a necessary lower-level requirement from higher-level intent, analysis or design context with an explicit argument. **Decomposition** partitions an obligation while preserving sufficiency.
- **Allocation** assigns responsibility for an obligation or budget to system elements, people or enabling systems. Allocation is not satisfaction.
- A **satisfaction claim** asserts that a design element or configuration is intended to meet a requirement. It needs supporting analysis and is not verification closure.
- A **verification relationship** connects a requirement to a verification case, method, article/configuration, conditions, success criteria and result evidence.
- **Bidirectional traceability** permits navigation from a requirement to justified upstream sources and accountable downstream realization/verification artifacts and back.
- A **baseline** is an approved configured set of requirements and relationships; edits after approval form proposed changes or later baselines, not silent corrections.

### Central model, mechanism, or theorem

Represent requirement $r$ at baseline $b$ as

\[
r_b=(id,subject,modal,action,object,condition,measure,threshold,tolerance,
unit,applicability,source,rationale,assumptions,status,version).
\]

Let the typed requirements graph be $G_R=(V,E_T)$, where vertices include needs, requirements, functions, architecture elements, interfaces, hazards, decisions and verification cases, and edge type $T$ includes `derives`, `decomposes`, `allocates`, `satisfies`, `verifies`, `conflicts-with`, `supersedes` and bounded generic `traces-to`.

For a parent $p$ decomposed into children $C_p$, adequacy requires an engineering argument—not graph shape alone:

\[
\bigwedge_{c\in C_p} c \land A \Rightarrow p,
\]

where $A$ exposes assumptions and composition rules. The implication must be reviewed and supported for the modeled context. A link count cannot prove completeness, feasibility, satisfaction or verification.

### Critical invariants

- Each requirement has one stable identifier, one controlling source/version, one normative obligation and an explicit product level and applicability.
- Normative text distinguishes subject, required action or property, condition, measurable outcome, threshold/tolerance and units as applicable.
- Needs, goals, objectives, assumptions, operational statements, requirements, design descriptions, rationale, verification procedures and results remain distinct model objects.
- Every requirement is necessary and traces to an authorized source; self-derived requirements expose the analysis, decision, interface or hazard that made them necessary.
- Parent-child derivation/decomposition is acyclic within a baseline, and each edge has a reason, transformation rule or adequacy argument.
- Children are neither arbitrary copies nor presumed collectively sufficient; gaps, overlap, budgets and crosscutting obligations are reviewed.
- Allocation names accountable system/enabling elements and shared responsibility; satisfaction remains a design claim, not a synonym.
- Verification information identifies method, level, article/configuration, environment, inputs, measures, success criteria and evidence/status without writing the procedure into the normative statement.
- Validation asks whether the modeled requirement set represents the right problem and stakeholder intent; verification asks whether the realized product satisfies approved requirements.
- Contradictions, duplicates, ambiguous terms, incompatible units, missing values, TBD/TBR items and inconsistent applicability are detected and governed.
- Requirement status, maturity and verification status are separate; approved does not mean implemented or verified.
- Changes preserve rationale, authority, impact, review, versions, prior baselines and downstream propagation.
- Views and generated specifications carry source baseline and remain consistent with the authoritative requirement objects.
- Automated checks are bounded structural/semantic evidence; human and domain review remain necessary for intent, correctness, feasibility and sufficiency.

### Common failures

Common failures include modeling paragraphs as single requirements; combining multiple “shall” clauses; omitting subject, condition, tolerance or units; encoding rationale in normative text; treating every stakeholder wish as contractual; using vague qualities such as “fast” or “user-friendly”; forcing design solutions into requirements without rationale; copying parents into children; assuming a tree proves complete flowdown; using generic trace links for every relationship; inferring satisfaction from allocation; inferring verification from a linked test name; treating a passed test against the wrong configuration as closure; duplicating an interface requirement on both sides; resolving conflict by last edit; hiding TBDs in model properties; assigning verification method without measurable success criteria; counting trace coverage as correctness; editing a baseline in place; and generating a clean document from semantically inconsistent objects.

### Compact example

An emergency-water system has one top-level delivery requirement and four derived requirements for pressure, response time, endurance and operating environment. Each object has one `shall`, quantitative measure/unit, rationale, applicability, allocation and verification case. Four acyclic parent edges connect the children to the parent; the adequacy record explains how hydraulic analysis and loss assumptions compose them. A checker confirms IDs, fields and link integrity, but reviewers still challenge whether the set covers water quality, maintenance, power/common-cause failure and actual stakeholder need.

### Connections

SYSENG-051 establishes authoritative model governance. SYSENG-052 applies it to requirements; SYSENG-053–055 connect behavior, structure and parametrics, and SYSENG-056–060 connect traceability, consistency, model reviews and tool boundaries. Earlier stakeholder, ConOps, interface, verification, risk and decision modules supply sources that prevent requirements modeling from becoming isolated text administration.

## Governing Question

Can an engineer traverse from a modeled obligation to the stakeholder or governing reason it exists, interpret exactly when and where it applies, see how lower-level obligations preserve it, identify responsible design elements and verification evidence, and determine what must be reconsidered if it changes?

If the answer is only “the model shows a trace,” the semantic work is unfinished. Traceability supports an argument; it is not the argument. Requirements models become valuable when their objects and relationships enable disciplined questions while keeping normative authority and empirical evidence distinct.

## Why This Matters

Prose specifications can be authoritative, but readers must reconstruct relationships, applicability and impacts manually. A requirements model can expose missing sources, duplicate identities, inconsistent units, unverified obligations and crosscutting effects early. It can also spread error faster: one ambiguous parent can generate dozens of apparently precise descendants, and generic links can make an unsupported design look fully traced.

NASA's Technical Requirements Definition guidance transforms baselined expectations and ConOps into complete, validated technical requirements, including functions, performance, interfaces, environments, safety, human factors and other crosscutting qualities. It calls for one-`shall` statements, rationale and assumptions, stakeholder validation, feasibility, verifiability, nonredundancy and controlled baselines. NASA Requirements Management adds identification, control, decomposition/allocation, bidirectional traceability and lifecycle change.

NASA-HDBK-1009A provides a current systems-modeling metamodel and examples connecting stakeholder expectations, system/subsystem requirements and verification statements. SysML 2.0 provides semantic constructs for requirement definitions/usages and verification cases. ISO/IEC/IEEE 29148:2018 governs lifecycle requirements-engineering processes and information items. These frameworks enable rigor, but projects must still define local meanings, ownership, profiles, acceptance and evidence.

## Prerequisites and Retrieval

Before building or repairing a requirements model, retrieve:

1. system boundary, product/configuration hierarchy, lifecycle, variants, ConOps, modes/states, scenarios, environments, stakeholders and decision/risk authorities;
2. baselined needs, goals, objectives, expectations, measures of effectiveness, mission success, laws/policies/standards, contracts, interface agreements, hazard/security/privacy controls and prior decisions;
3. current requirement sets with IDs, levels, owners, sources, rationale, assumptions, status, priority/criticality, applicability, change history and waivers;
4. functional/behavior, architecture, interface, budget/parametric, human-work, safety/security, verification and validation models;
5. requirement language/profile/metamodel, relationship semantics, identifier/naming rules, units/quantity library, patterns and validation rules;
6. verification methods/cases, success criteria, test articles/configurations, facilities/environments, results, anomalies, evidence and closure authority;
7. repository, branch/baseline, access, review/change workflow, imports/exports, generators, APIs, validation pipelines and audit history;
8. known TBD/TBRs, ambiguous terms, duplicates, orphans, conflicts, stale views, unverified requirements, shadow spreadsheets and supplier boundaries.

Use a retrieval test: “The service shall respond quickly and securely when needed.” Ask which service/configuration and requester, what request, state/load/threat/environment, measurable response percentile and time bound, failure behavior, security property and evidence, source/rationale, allocation and verification case. Splitting “quickly” and “securely” into two requirement objects is necessary, but not sufficient until the missing semantics are resolved.

## Learning Objectives

After completing this module, you should be able to:

1. represent requirements as governed semantic objects rather than unstructured diagram text;
2. separate normative statements from rationale, assumptions, operations, design and evidence;
3. model subject, action/property, condition, measure, threshold, tolerance, unit and applicability;
4. distinguish source, derivation, decomposition, allocation, satisfaction, verification, conflict and supersession relationships;
5. construct and challenge adequacy arguments for parent-child requirement sets;
6. integrate requirements with behavior, structure, interfaces, budgets, hazards and verification cases;
7. validate requirements and sets for intent, correctness, completeness, feasibility, consistency and verifiability;
8. automate bounded checks for IDs, fields, units, graph integrity, placeholders and link coverage;
9. govern baselines, changes, variants, waivers, generated views and supplier requirements;
10. audit evidence and outcome feedback without confusing model completeness with system compliance.

## Core Exposition

**Model the obligation, not the sentence container.** Give each requirement a stable identity and one normative obligation. Store statement fields and metadata separately so views can render a conventional sentence without hiding semantic structure. Preserve the original authorized wording where contracts demand it; map structured interpretation to it and govern discrepancies.

**Name the obligated subject.** “Shall provide” is incomplete without the product, interface or enabling system responsible. Use the approved product hierarchy and stable identity. Do not make a person the subject of a product requirement when the statement belongs in ConOps, procedure, staffing plan or contract.

**State condition and applicability.** Capture triggering event, mode/state, operating environment, load, user/population, interface, timing window, product variant and lifecycle. A requirement that applies during emergency mode may be harmful in maintenance mode. Avoid burying applicability in a document section title that disappears when objects are reused.

**Make performance interpretable.** Store quantity kind, measure, comparison operator, threshold, tolerance/margin, units, statistic/percentile, time horizon and measurement reference. “Latency < 100 ms” remains ambiguous without start/stop events, population, percentile, load and exclusions. Use controlled quantity/unit libraries and dimensional validation.

**Separate requirement classes without stereotyping away meaning.** Functional requirements state what function occurs; performance requirements state how well; interface and environmental requirements constrain interactions/conditions; safety, security, privacy, human-factor, reliability and maintainability requirements may cut across products. Project profiles can classify them, but a label does not make prose adequate.

**Preserve source and rationale.** Trace to a stakeholder expectation, parent, law, standard, interface agreement, hazard control or authorized decision. Record why the exact obligation/value exists, assumptions and consequence if absent. If no source can justify it, challenge necessity. Do not delete a locally derived requirement merely because no customer wrote it; expose its engineering derivation and authority.

**Distinguish assumption from requirement.** Assumptions are propositions treated as true for current reasoning and must be confirmed, monitored or converted. A requirement obligates a subject. Model each assumption, owner, evidence, expiry and affected requirements. A hidden assumption can invalidate an entire apparently complete subtree.

**Use TBD/TBR visibly.** Avoid fabricating precision. Represent unknown value, why it is unresolved, owner, resolution evidence/activity, deadline, decision impact and fallback. Block baseline or downstream use according to consequence. A placeholder token buried inside prose is not managed uncertainty.

**Model derivation as an argument.** A child can follow from a parent plus behavior, architecture, interface, hazard or budget analysis. Link inputs, transformation, assumptions and reviewer. “DeriveReq” does not prove logical implication. Where the relation is allocation or refinement rather than derivation, name it accordingly.

**Test decomposition adequacy.** Ask whether children jointly cover every parent condition/outcome, whether their interaction preserves the parent, whether overlaps create contradiction or unnecessary constraint, and whether budgets/margins compose. Use scenario, behavior, parametric and interface models. Retain an explicit coverage or sufficiency argument and its evidence limits.

**Manage crosscutting requirements.** Security, safety, timing, data, accessibility and environmental obligations often span product branches. Model shared responsibility and integration-level verification instead of duplicating altered prose under every component. Local derived requirements can allocate specific contributions while the crosscutting parent retains whole-system ownership.

**Keep allocation separate.** Allocation says which element has responsibility or receives a budget. It can be one-to-one, one-to-many or shared with an integrator. Record allocation rationale, interfaces and budget conservation. A box linked to a requirement has not demonstrated a feasible design.

**Treat satisfaction as a reviewable claim.** A design element or configuration may `satisfy` a requirement based on an architecture argument, analysis or implementation evidence. Name claimant, baseline and support. Satisfaction before realization is often prospective; do not turn it into verified status. Multiple elements may collectively satisfy one obligation.

**Model verification cases, not just methods.** “Test” is insufficient. Link requirement to verification objective/case, method, level, article/configuration, facilities/instrumentation, preconditions, stimuli, measurements, uncertainty, success criteria, independence and resulting evidence. Combined verification is acceptable when coverage and result attribution remain clear.

**Separate requirement validation and product verification.** Validate that requirements correctly and completely express stakeholder need, ConOps, mission success and constraints. Verify that a configured realized product satisfies them. A requirement can be well written yet wrong; a product can pass a test against the wrong requirement.

**Model conflicts explicitly.** Detect incompatible thresholds, units, modes, states, interface directions, standards and variant applicability. Preserve competing sources and authority; do not automatically choose stricter because stricter can be infeasible, unsafe or inconsistent. Record resolution and impacted baselines.

**Manage duplicates and equivalence.** Text similarity can propose candidates but cannot establish semantic duplication. Two identical sentences may apply to different products or authorities; different wording may impose the same obligation. Use stable IDs, semantic fields, sources and applicability, then merge/map/supersede through controlled decisions.

**Represent variants and reuse.** Define common requirements once where authority and semantics are truly shared; specialize applicability or values through controlled variant mechanisms. Avoid copying entire sets that later drift. Pin feature/variant configuration and evaluate contradictory combinations. Retain regulatory and market boundaries.

**Govern status dimensions.** Track proposed/reviewed/approved/superseded separately from implementation and verification status. Track maturity or risk without overloading approval. A failed verification result should not silently rewrite the requirement status; it creates nonconformance, analysis and possible change.

**Perform impact analysis before change.** Traverse sources, parents/children, behavior, allocated/satisfying elements, interfaces, budgets, hazards, verification cases, supplier contracts, plans and decisions. Assess whether changing a number alters stakeholder validity or risk acceptance. Authorize, baseline and propagate; preserve prior wording/rationale/evidence.

**Generate concern-oriented views.** Produce specifications, trees, matrices, verification maps, variant views and review change sets from the configured model. Stamp baseline and generation provenance. Generated layout supports communication; it does not substitute for graph/semantic audits or source access.

**Automate carefully.** Check unique IDs, required fields, controlled terms, one normative modal, units, unresolved values, graph cycles/orphans, invalid relationship types, cross-baseline links, missing verification cases and stale generations. Natural-language lint can flag ambiguity but cannot decide intent. False positives and waived rules need governance.

**Review the set as a system.** Inspect individual quality and set properties: completeness across scenarios/lifecycle, consistency, feasibility, necessary/sufficient scope, architecture neutrality where intended, interface closure, budget balance, crosscutting coverage and verification strategy. Include stakeholders, domain, design, operations, safety/security/privacy, integration and V&V reviewers.

**Reconcile outcomes.** Verification failures, incidents, operational data and stakeholder validation can reveal wrong implementation, wrong test, wrong model, wrong requirement or changed context. Preserve evidence, align configuration and investigate competing hypotheses. Update controlling objects only through authorized change and superseding baselines.

The following executable teaching model checks five quantitative requirements and four parent edges. It demonstrates structural consistency only; it cannot prove that the requirements are necessary, sufficient, feasible, correctly valued or actually satisfied.

<!-- bijux-verify: {"id":"requirements-model-integrity-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"requirements=5\nunique_ids=1\nparent_edges=4\norphan_parents=0\nderivation_cycle=0\nsingle_normative_statements=5\nquantified_requirements=5\nrationales=5\nallocations=5\nverification_links=5\nunresolved_placeholders=0\nstatus=requirements_model_consistent\nevidence=declared_model_only\n","stderr":""}} -->
```python
requirements = [
    {"id": "R-100", "parent": None, "shall": 1, "measure": "flow",
     "threshold": 1200, "unit": "L/min", "rationale": "emergency demand",
     "allocation": "water-system", "verification": "VC-100", "placeholder": False},
    {"id": "R-110", "parent": "R-100", "shall": 1, "measure": "pressure",
     "threshold": 300, "unit": "kPa", "rationale": "terminal pressure budget",
     "allocation": "pump", "verification": "VC-110", "placeholder": False},
    {"id": "R-120", "parent": "R-100", "shall": 1, "measure": "start-time",
     "threshold": 5, "unit": "s", "rationale": "response scenario",
     "allocation": "controller", "verification": "VC-120", "placeholder": False},
    {"id": "R-130", "parent": "R-100", "shall": 1, "measure": "endurance",
     "threshold": 60, "unit": "min", "rationale": "responder arrival bound",
     "allocation": "power-system", "verification": "VC-130", "placeholder": False},
    {"id": "R-140", "parent": "R-100", "shall": 1, "measure": "temperature-low",
     "threshold": -20, "unit": "degC", "rationale": "deployment environment",
     "allocation": "integrated-system", "verification": "VC-140", "placeholder": False},
]
ids = {requirement["id"] for requirement in requirements}
parents = [(requirement["id"], requirement["parent"])
           for requirement in requirements if requirement["parent"]]

def cycle(edges):
    parent = dict(edges)
    for start in parent:
        seen, node = set(), start
        while node in parent:
            if node in seen:
                return True
            seen.add(node)
            node = parent[node]
    return False

print(f"requirements={len(requirements)}")
print(f"unique_ids={int(len(ids) == len(requirements))}")
print(f"parent_edges={len(parents)}")
print(f"orphan_parents={sum(parent not in ids for _, parent in parents)}")
print(f"derivation_cycle={int(cycle(parents))}")
print(f"single_normative_statements={sum(r['shall'] == 1 for r in requirements)}")
print(f"quantified_requirements={sum(bool(r['measure'] and r['threshold'] is not None and r['unit']) for r in requirements)}")
print(f"rationales={sum(bool(r['rationale']) for r in requirements)}")
print(f"allocations={sum(bool(r['allocation']) for r in requirements)}")
print(f"verification_links={sum(bool(r['verification']) for r in requirements)}")
print(f"unresolved_placeholders={sum(r['placeholder'] for r in requirements)}")
consistent = len(ids) == len(requirements) and not cycle(parents)
consistent &= not any(parent not in ids for _, parent in parents)
consistent &= all(r["shall"] == 1 and r["measure"] and r["unit"] for r in requirements)
print("status=" + ("requirements_model_consistent" if consistent else
                   "requirements_model_needs_work"))
print("evidence=declared_model_only")
```

The root and children use comparable quantitative fields, but the checker does not establish that pressure, start, endurance and temperature jointly imply the delivery obligation. That requires hydraulic, power, behavior, environment and scenario evidence plus review of missing crosscutting constraints.

## Definitions and Notation

Let requirement state be $state(r,b)\in\{proposed,reviewed,approved,superseded,retired\}$ and verification state be separately modeled, for example $vstate(r,b)\in\{unplanned,planned,executed,passed,failed,accepted\}$. No transition in one set implies a transition in the other.

Typed trace matrix $T_{xy}$ records permitted relationships between source class $x$ and target class $y$. Coverage ratio

\[
C_{xy}=\frac{|\{x:\exists y,(x,y)\in E_T\}|}{|X|}
\]

is a completeness indicator for declared scope, not proof that links or artifacts are correct.

For quantitative budget parent $B$ and child contributions $b_i$, a composition rule may be additive, worst-case, probabilistic or nonlinear:

\[
B=f(b_1,\ldots,b_n,A,U),
\]

where $A$ is assumptions and $U$ uncertainty/correlation. The model must name $f$ rather than assuming child values sum.

## Mechanisms, Invariants, or Proof Structure

**Mechanism 1—semantic capture.** Model stable identity, normative fields, applicability, source, rationale, assumptions, authority, status and baseline.

**Mechanism 2—typed flowdown.** Distinguish derivation, decomposition, allocation, satisfaction, verification, conflict and supersession; attach adequacy arguments.

**Mechanism 3—integration.** Connect requirements to stakeholder/ConOps, behavior, structure, interfaces, budgets, hazards, decisions and verification cases.

**Mechanism 4—validation and control.** Review individual/set quality, uncertainty/placeholders, variants, conflicts, baselines, changes, supplier boundaries and generated views.

**Mechanism 5—evidence and learning.** Plan verification, preserve result configuration, audit structural and semantic integrity, investigate failures and update through governed history.

Graph integrity is necessary but insufficient. The proof obligation for a lower-level set depends on real semantics, assumptions, composition, evidence and domain judgment.

## Alternatives and Trade-Offs

**Structured requirement objects** enable validation and generation but can become rigid. **Rich narrative** preserves context but is harder to compute. Keep a concise normative object linked to rationale, scenarios and evidence.

**Specialist requirements repositories** support review/baselining. **Integrated system models** improve behavior/structure/verification trace. Federate with stable identities and declared authority instead of uncontrolled duplication.

**Formal constraints** permit executable checks and analysis. **Controlled natural language** remains accessible and contract-compatible. Use both when risk justifies it and state precedence.

**Deep derivation trees** show local ownership but can obscure crosscutting intent. **Shallow direct trace** reduces maintenance but may skip necessary product-level obligations. Tailor depth to design responsibility and verification.

**Reusable requirement libraries** improve consistency but risk context mismatch. Reuse patterns and concepts with explicit applicability, source authority and local validation; never inherit compliance automatically.

**Strict lint gates** catch common defects. They can encourage awkward text or waived warnings. Keep rules explainable, versioned and subordinate to semantic review.

## Failure Modes and Misconceptions

**“A requirement diagram proves flowdown.”** It shows declared edges; adequacy needs transformation and coverage reasoning.

**“Every requirement must be quantitative.”** Every requirement must be verifiable; some functional/logical obligations use observable conditions and outcomes rather than scalar thresholds.

**“Stricter is always safer.”** Overconstraint can create infeasibility, new hazards, cost or operational harm. Use justified values and margins.

**“Allocation means satisfied.”** Allocation assigns responsibility; satisfaction and verification require separate claims/evidence.

**“Traceability percentage is quality.”** Coverage can be 100 percent with wrong, generic or circular links.

**“A passed test validates the requirement.”** Test evidence verifies a configured product against criteria; stakeholder validation asks whether the obligation was right.

**“The model should eliminate prose.”** Normative statements, rationale and accessible views remain essential; modeling improves semantics and connections.

**“A parent can be deleted after decomposition.”** Preserve source intent and adequacy links for change, integration and validation.

**“Shared text should be copied to every variant.”** Copies drift. Govern common authority and explicit specialization.

**“Operational mismatch means change the requirement.”** First investigate product, test, model, evidence and context under correct authority.

## Worked Examples

### Example 1

**Split conjunction.** “The gateway shall authenticate and log requests” becomes two requirement objects with shared source and distinct security/log-retention verification, while the original authorized wording is preserved if contractually controlling.

### Example 2

**Derived response time.** A 30-second stakeholder outcome plus behavior and latency-budget analysis derives component deadlines. The model links the budget equation and uncertainty; `derive` alone is not the rationale.

### Example 3

**Allocation is not proof.** An availability requirement is allocated across service, network, power and operations. Joint architecture/recovery evidence supports prospective satisfaction; representative fault evidence supports verification later.

### Example 4

**Unit conflict.** Supplier pressure is in psi gauge while system requirement is kPa absolute. Typed quantities and reference conditions expose a false apparent match before interface approval.

### Example 5

**Crosscutting security.** One system-level identity requirement derives responsibilities for client, service, key management, audit and operations, plus an end-to-end verification case; prose is not duplicated inconsistently.

### Example 6

**Variant reuse.** A common environmental requirement applies to all variants, while temperature thresholds specialize by market/configuration. The baseline manifest prevents an Arctic value from leaking into a temperate build.

### Example 7

**Managed TBR.** An unresolved maximum user load has owner, measurement campaign, deadline, assumed design value, margin, affected requirements and decision trigger. It remains visible in review and analysis.

### Example 8

**Satisfaction versus verification.** A redundancy design claims to satisfy fault tolerance. Model checking supports logic, but physical common-cause and recovery tests remain open; the requirement is approved, implementation partial and verification not closed.

### Example 9

**Change impact.** Tightening response time traverses behavior budgets, interface rates, processor allocation, power/thermal models, supplier contract, tests, risks and cost/schedule before authorization.

### Example 10

**Outcome feedback.** A deployed accessibility requirement passed scripted inspection but users cannot complete a task with assistive technology. The team preserves evidence and investigates criteria, test population, implementation and requirement validity rather than rewriting history.

## Cross-Program Connections

**Platform engineering.** Platform capability, SLO, policy and adopter obligations need scoped requirements, ownership, golden-path/fallback applicability and runtime evidence.

**API and service engineering.** Interface schemas, compatibility, latency, availability, authentication and deprecation obligations benefit from typed versions, consumer/provider allocation and executable contract evidence.

**Data engineering.** Schema, quality, lineage, retention, privacy and freshness requirements need dataset/population/time semantics and pipeline-to-outcome verification.

**Object-oriented programming.** Class/module contracts allocate responsibilities but do not prove system requirements; code and tests need bidirectional, configuration-specific trace where consequence justifies it.

**Functional programming.** Types and properties can encode formal obligations and executable checks; they remain interpretations of stakeholder/system requirements under modeled assumptions.

## References

1. NASA, *Systems Engineering Handbook, Section 4.2: Technical Requirements Definition*, current web edition. <https://www.nasa.gov/reference/4-2-technical-requirements-definition/>
2. NASA, *Systems Engineering Handbook, Appendix C: How to Write a Good Requirement*, current web edition. <https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/>
3. NASA, *Systems Engineering Handbook, Section 6.2: Requirements Management*, current web edition. <https://www.nasa.gov/reference/6-2-requirements-management/>
4. NASA, *Systems Engineering Handbook, Section 4.3: Logical Decomposition*, current web edition. <https://www.nasa.gov/reference/4-3-logical-decomposition/>
5. NASA, *Systems Engineering Handbook, Appendix D: Requirements Verification Matrix*, current web edition. <https://www.nasa.gov/reference/appendix-d-requirements-verification-matrix/>
6. NASA, *NASA Systems Modeling Handbook for Systems Engineering*, NASA-HDBK-1009A, active 2025. <https://standards.nasa.gov/standard/NASA/NASA-HDBK-1009>
7. Object Management Group, *Systems Modeling Language Specification Version 2.0*, 2025. <https://www.omg.org/spec/SysML/2.0>
8. ISO/IEC/IEEE, *29148:2018 Systems and software engineering—Life cycle processes—Requirements engineering*. <https://www.iso.org/standard/72089.html>
9. NASA, *Systems Engineering Handbook, Section 4.1: Stakeholder Expectations Definition*, current web edition. <https://www.nasa.gov/reference/4-1-stakeholder-expectations-definition/>
10. NASA, *Systems Engineering Handbook, Section 6.5: Configuration Management*, current web edition. <https://www.nasa.gov/reference/6-5-configuration-management/>

## Exercises

### Exercise 1

Transform “The autonomous shuttle shall be safe, comfortable, arrive quickly, and support disabled passengers” into a requirements-model plan without inventing unjustified thresholds.

### Exercise 2

Audit a model with 240 requirements: 100-percent trace coverage, 28 generic trace links standing for derivation, 19 two-`shall` statements, 14 unitless thresholds, nine orphan children, six cyclic parent links, 31 test-method labels without success criteria and four hidden TBDs.

### Exercise 3

Design a derivation and adequacy argument from a system recovery objective to service, data, infrastructure and operator requirements, including correlated/common-cause failure.

### Exercise 4

Model one requirement family across standard, regulated and low-connectivity variants while avoiding copied requirement drift and invalid inherited verification.

### Exercise 5

A baselined latency requirement is tightened after a stakeholder complaint, but supplier hardware is contracted and verification is underway. Define impact analysis, authority, change, evidence and history.

## Answers to the Exercises

### Answer 1

Preserve the statement as an elicited expectation, not an approved technical requirement. Identify shuttle system/configuration, service boundary, passengers and subgroups, operational authority, accessibility/safety regulators, drivers/remote operators, maintainers, emergency services and communities. Build ConOps scenarios for nominal boarding/travel, wheelchair and mobility aids, sensory/cognitive needs, service animal, communication, peak load, traffic/weather, obstruction, degraded automation, emergency stop/evacuation, missed pickup and network/power loss.

Split values into outcome models before thresholds. Safety includes hazards, collision/injury exposure, safe state, detection/response and evacuation; comfort includes acceleration/jerk, climate, seating/noise and relevant populations; “quickly” includes request-to-pickup and origin-to-destination distributions under load/geography; disability support includes independent or assisted discovery, booking, boarding, securement, communication, travel and evacuation. Include privacy/security, operator workload and service availability where scenarios reveal them.

Trace each candidate to stakeholder evidence, law/standard, hazard analysis or authorized objective. Record measure definitions, events, populations, conditions, statistic, tolerance and units only after research, field evidence, simulation/prototype and authority establish defensible values. Separate mandatory constraints from preference targets. Model assumptions/TBRs with owners and resolution plans rather than guessing.

Derive product-level obligations through behavior, interface, human-work and architecture analysis; allocate across vehicle, station, application, communications, remote operations, maintenance and emergency procedures. Preserve adequacy arguments and crosscutting integration responsibility. Link verification cases with representative passengers, assistive technologies, environments, failure states and outcome criteria; validate the resulting set with affected groups. Baseline only after correctness, completeness, feasibility, consistency and verifiability review.

### Answer 2

Do not accept the 100-percent metric. Freeze the audited baseline and export IDs, types, endpoints, fields, source versions and validation results. Sample links to determine whether the generic relation means source, derivation, decomposition, allocation, satisfaction, verification or mere association. Re-type only with evidence and owner review; do not infer semantics from layout. Add arguments for derived/decomposed sets.

Split the 19 compound obligations while preserving source authority, shared rationale and downstream impact. For 14 thresholds, identify quantity kind, operator, reference, unit, tolerance, condition and source; quarantine unsafe interpretation. Recover nine missing parents or identify external authoritative sources; if truly unjustified, challenge necessity. Break six cycles by analyzing mistaken direction, duplicate identity, refinement versus derivation or real recursive constraint; preserve change history.

Replace 31 method labels with verification objectives/cases: level, article/configuration, conditions, instrumentation/inputs, measurements, uncertainty, success criteria, evidence and owner. Surface four TBDs as governed objects with reason, assumed value/margin, owner, deadline, resolution evidence and blocked decisions. Then audit unique IDs, single normative obligations, ambiguity, applicability, sources/rationale, units, conflicts, variants, allocations, verification coverage and baseline consistency.

Re-run structural checks, but perform stakeholder/domain/design/integration/V&V review of individual requirements and set completeness. Report corrected coverage by typed relationship and evidence strength. A clean graph is the start of semantic review, not proof that 240 requirements describe the right system.

### Answer 3

Define the system objective precisely: which essential services/data, failure scenarios, service level, recovery time and recovery point, operating mode/load/region, observation window and excluded catastrophic assumptions. Identify service owners, data owners, infrastructure/network/identity providers, operators, users, security/safety and risk authority. Separate availability, restoration and data-loss measures.

Build failure/behavior and dependency models. Derive service requirements for detection, degraded response, idempotent recovery and restoration deadline; data requirements for replication, consistency, backup immutability, recovery point and reconciliation; infrastructure requirements for capacity, isolation, failover and dependency recovery; operator requirements in procedures/training/staffing systems for decision, communication and manual action. Allocate budgets with an explicit critical-path/composition function rather than dividing time arbitrarily.

Model assumptions about independence, detection latency, provider availability, staffing and data state. Analyze shared identity/DNS/control-plane/network/region, software/configuration, supply, cyber and operator common causes. A redundant service on one shared failure path is not adequate. Include fallback/manual modes and restoration priority.

The adequacy argument maps every objective condition to child behavior and shows timing/data budgets under scenarios, uncertainty and margins. Verification combines analysis/model checking, component fault tests, backup restore, interface tests, representative end-to-end fault injection and operator exercises. Preserve evidence configuration and anomalies. Validate business/user outcomes, not recovery commands alone. Reopen on dependency, architecture, workload, threat, staffing, incident or failed exercise evidence.

### Answer 4

Create a common requirement namespace and baseline for genuinely shared mission, safety, core-function and interface obligations. Model variant features/configurations explicitly. Use applicability expressions tied to standard, regulated and low-connectivity configurations; specialize values or derive variant obligations under controlled relationships rather than cloning whole documents. A stricter regulated statement cites its law/jurisdiction and does not silently replace the common need.

For low connectivity, extend ConOps and behavior for offline duration, stale data, synchronization, conflict, local identity, safe fallback and recovery. Derive obligations with their evidence rather than weakening common service language informally. For the regulated variant, add audit, retention, approval, data, safety/security or reporting obligations and allocate them to architecture/enabling systems. Analyze incompatible feature combinations.

Pin variant baselines with requirements, architecture, interfaces, supplier components and verification configurations. Generate variant-specific views from authoritative objects. Validate no requirement has empty or contradictory applicability and no common parent loses coverage. Keep crosscutting ownership at integration level where appropriate.

Verification is configuration-specific: reuse a case/result only when requirement semantics, product configuration, environment, population, method and evidence applicability match. Record equivalence rationale; otherwise specialize/re-execute. Changes to common objects trigger impact across all variants, while local changes remain bounded. Preserve regulatory authority, waivers, verification status and released histories separately.

### Answer 5

Preserve the complaint, original requirement/baseline/rationale, actual user/context/configuration, observed latency distribution, instrumentation and consequences. Validate whether the issue is requirement validity, implementation nonconformance, verification weakness, workload/environment change or expectation outside scope. Do not edit the baseline or promise a new threshold before evidence and authority.

Define proposed threshold with measure events, percentile/population, load/mode/environment, tolerance and justification. Traverse stakeholder objectives/ConOps, behavior and end-to-end latency budgets, interfaces, compute/network/storage, power/thermal, architecture, safety/security, supplier specification/contract, verification cases/results, deployment, cost/schedule and risks. Recompute feasibility, margin, uncertainty and tradeoffs; consider architectural, staged or service alternatives and value of information.

Engage requirement owner/customer, technical authority, affected stakeholders, supplier/procurement, architecture, operations, V&V, safety/security and program authority. Determine contract change, waiver/deviation and risk-acceptance paths. Preserve dissent and distributional effects. If approved, create a new configured requirement version/baseline with source, rationale, authority, effective variants/releases and supersession link; never rewrite what the supplier and tests previously used.

Update derived requirements/budgets, allocations/satisfaction claims, interfaces, supplier contract, designs, test plans/cases/success criteria, risks, schedules and decision records. Keep old verification evidence valid only for its prior requirement/configuration. Re-verify affected components and end-to-end behavior under representative load, then validate complaint outcomes. Monitor percentiles, failures and user groups; reopen on feasibility, cost/schedule, regression, incident or outcome thresholds.
