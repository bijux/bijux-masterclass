---
module_id: SYSENG-060
program: Systems Engineering
level: 2
module_number: 60
title: Establishing an MBSE Workflow Without Model Bureaucracy
status: complete
last_verified: 2026-08-31
---

# Establishing an MBSE Workflow Without Model Bureaucracy

## One-Page Review

### Governing question

How can a team make models the fastest trustworthy route from engineering uncertainty to an authorized decision, while retaining enough semantics, configuration, evidence, and review to avoid both document theater and model bureaucracy?

### Essential definitions

- **Model-based systems engineering (MBSE)** is the formalized use of models to support requirements, design, analysis, verification, and validation across the lifecycle. A tool license, diagram repository, or mandate to “model everything” is not an MBSE practice.
- A **decision product** is the smallest governed model view, analysis, trace, comparison, or evidence package needed by a named decision-maker for a stated decision.
- **Decision pull** starts modeling from recurring engineering decisions and uncertainties. **Artifact push** creates model content because a process or template asks for it, without a known consumer.
- A **minimum sufficient model** contains the semantics and evidence needed for its intended decisions, interfaces, analyses, changes, and assurance obligations—no less, and no unrelated completeness for its own sake.
- A **modeling increment** is a reviewable, configuration-controlled change that answers a question, retires risk, enables integration, or improves a governed decision product.
- A **model authority map** declares which source governs each kind of fact, who may change it, how derived views are generated, and how conflicts are resolved.
- A **working agreement** states scope, language subset, naming/identity, packages, ownership, branching, review, validation, integration, and done criteria for the modeling team.
- A **model gate** is an automated or human acceptance check tied to consequence: syntax, metamodel/profile conformance, unresolved references, configuration, invariants, analysis/tests, trace, review, or approval.
- **Model debt** is the future decision and change cost caused by unclear semantics, duplicate authority, stale links, weak modular boundaries, hidden assumptions, missing automation, or unsupported tool customizations.
- **Flow efficiency** is active value-adding time divided by total lead time. Low flow efficiency often reveals waiting, queues, handoffs, rework, and approval latency that more modeling effort alone cannot fix.
- A **review latency** is the elapsed time from a reviewable increment to useful disposition. Long latency increases batch size and makes feedback expensive.
- An **exit or adaptation criterion** states when a model/view/process should be retired, simplified, migrated, or changed because its decision value no longer justifies its cost.

### Central model, mechanism, or theorem

Treat each workflow item $w$ as a decision contract:

\[
w=(q,d,o,s,e,g,t),
\]

where $q$ is the question/uncertainty, $d$ the decision and decision owner, $o$ the minimum model outputs, $s$ the authoritative sources and configuration, $e$ the required evidence, $g$ the gates/acceptance rule, and $t$ the review-by time.

For a delivered increment, record active modeling/analysis time $A$, waiting and handoff time $W$, rework $R$, and total lead time $L=A+W+R$. Then

\[
FE=\frac{A}{L}.
\]

Do not optimize $FE$ alone. A useful workflow balances decision value $V_d$, evidence quality $Q_e$, latency $L$, lifecycle cost $C_l$, and change risk $R_c$:

\[
U=\frac{V_d\,Q_e}{L+C_l+R_c},
\]

with noncompensable gates for safety, security, configuration, and integrity. This is a prioritization model, not a universal economic law. Scores and weights must be local, visible, and accompanied by raw dimensions.

### Critical invariants

- Every durable model element or view has a consumer, decision/use, owner, source authority, configuration, freshness expectation, and retirement condition.
- Model scope is pulled by decisions, integration risks, analyses, interfaces, verification, and lifecycle needs—not by a demand to populate every language construct.
- One fact has one declared authority for a given domain/configuration/time; derived views expose provenance and cannot become silent duplicate authorities.
- Stable identity and modular boundaries survive team and repository reorganization. Display diagrams are views, not ownership containers.
- The language subset, semantics, units, naming, profile/extensions, and definition-of-done are teachable and automatically checked where practical.
- Changes are small, reviewable, configuration controlled, linked to intent, and integrated frequently. Long-lived private model branches are exceptional.
- Review checks meaning and decision consequences, not diagram cosmetics alone. Review evidence and unresolved dissent remain visible.
- Automation generates repetitive views/reports, validates invariants, and exposes failures; it does not invent missing engineering judgment.
- The workflow integrates requirements, analyses, software/hardware data, tests, configuration, and downstream users through controlled contracts rather than forced duplication.
- Metrics expose queues, rework, staleness, escaped defects, decision latency, adoption, and outcomes. Element count and diagram count are not value metrics.
- Tailoring is explicit and consequence-aware. “Lean” never means omitting required assurance; “compliant” never means retaining waste without a reason.
- The team periodically removes unused views, redundant approvals, brittle customization, and stale model content while preserving needed history.

### Common failures

Common failures include buying a tool before selecting decisions; modeling the whole system before delivering one useful question; forcing every discipline into one repository; copying source facts to make diagrams pretty; treating diagrams as the model; using one giant package; granting only modelers edit access; requiring specialists to translate every conversation; reviewing screenshots instead of semantics and diffs; customizing a metamodel faster than users can learn it; creating mandatory views without consumers; manually rebuilding reports; accepting broken references until a milestone; branching for months; measuring element counts; holding review boards that batch trivial changes; demanding full trace for low-consequence exploration while omitting high-consequence evidence; and retaining a workflow after its cost exceeds its decision value.

### Compact example

A synthetic queue contains four decision products. A small checker confirms every item has an owner, consumer, evidence, gate, and review target; all completed items meet their gates; work in progress stays at two; lead time totals 44 hours, active time 16 hours, rework 4 hours, flow efficiency is 36.4%, and one item is overdue. These declared numbers diagnose a waiting-time problem and one service breach. They do not prove model quality, determine root cause, set a universal WIP limit, or show that the resulting engineering decisions are correct.

### Connections

SYSENG-056 through SYSENG-059 supply language, validation, transformation, and digital-thread mechanisms. SYSENG-060 makes them operational through decision pull, ownership, small increments, automated gates, and evidence-aware flow. Platform engineering provides shared services and golden paths; API/data engineering provide integration contracts; object-oriented and functional programming provide modularity, invariants, immutability, testing, and review practices.

## Governing Question

Can the team show that each modeled fact and view reduces uncertainty or supports an owned lifecycle decision, reaches its consumer quickly, remains configuration-correct, and costs less to maintain than the avoidable rework or risk it prevents?

The goal is not fewer models. It is less accidental work around models: rekeying data, reconciling duplicate truth, waiting weeks for a specialist, reviewing enormous batches, repairing stale diagrams, or producing documents whose only consumer is a process checklist. A lean workflow can be rigorous because it moves verification and semantic checks earlier and makes the evidence path shorter.

## Why This Matters

MBSE adoption fails in two symmetric ways. Under-modeling leaves critical interfaces, assumptions, configurations, analyses, and evidence in disconnected documents or minds. Over-process creates a specialist bureaucracy: elaborate taxonomies, mandatory diagrams, large review boards, and slow tool workflows whose outputs no longer guide decisions. Both failures separate engineering work from decision feedback.

NASA's Systems Engineering Handbook describes systems engineering as systematic, disciplined, quantifiable, recursive, iterative, and repeatable. NASA-HDBK-1009A integrates SysML modeling with stakeholder expectations, technical requirements, product verification, and product validation, including planning, model organization, model building, and generation of work-product views. These sources support rigor and lifecycle integration; they do not require maximal modeling or one universal workflow.

SysML 2.0 provides more precise semantics, textual and graphical representations, and a standard API that can support automation and integration. Yet a better language cannot choose the team's decisions, resolve authority, create review capacity, or remove approvals. The workflow must make those social and operational mechanisms explicit.

GAO's Agile Assessment Guide emphasizes iterative delivery, customer feedback, team dynamics, and outcome-oriented measurement. Recent GAO work on weapon-system testing also highlights early tester input, iterative testing, and user feedback. These lessons apply beyond software: model increments should be evaluated by how quickly they expose consequential learning and improve decisions, not by the amount of repository content produced.

## Prerequisites and Retrieval

Before establishing or repairing an MBSE workflow, retrieve:

1. the top recurring decisions, unresolved risks, integration failures, late changes, verification gaps, and avoidable rework from recent work;
2. decision owners, model consumers, discipline owners, suppliers, operators, assurance roles, and their actual review availability;
3. authoritative sources, duplicated facts, manual transfers, interfaces, schemas, versions, configurations, effectivities, access constraints, and update rates;
4. applicable standards, contractual deliverables, safety/security/certification evidence, review gates, records obligations, and tailoring authority;
5. current modeling language/version, allowed subset, profiles/extensions, tools, licenses, repositories, APIs, automation, export formats, and longevity constraints;
6. package/module boundaries, ownership, dependencies, branch/merge practices, validation rules, baseline/release process, and recovery procedures;
7. examples of useful and unused models/views, stale content, review comments, escaped defects, queue times, rework, handoffs, and unavailable expertise;
8. team skills, onboarding time, editing/query access, support capacity, working locations, supplier constraints, and accessibility needs;
9. downstream analysis, software, manufacturing, test, operations, and document-generation contracts plus the provenance of each transformation;
10. candidate pilots, measurable outcome baselines, stop/adapt criteria, migration needs, and executive authority to remove redundant process.

Ask for one recent decision and reconstruct its path: question, evidence requested, sources changed, people waiting, manual conversions, reviews, corrections, approval, and downstream consequences. That value-stream trace is more revealing than a maturity survey answered in the abstract.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish disciplined MBSE from tool adoption, diagram production, document replacement, and centralized model bureaucracy;
2. formulate decision contracts and select minimum sufficient model content;
3. map authority, ownership, consumers, configurations, provenance, and retirement criteria;
4. design modular team/repository boundaries and a teachable modeling subset;
5. establish small-increment branching, review, validation, integration, baseline, and recovery practices;
6. automate semantic gates, views, reports, transformations, and feedback without hiding failures;
7. integrate non-modeling disciplines through stable contracts and fit-for-purpose views;
8. measure decision lead time, waiting, rework, staleness, defect escape, adoption, and outcome rather than artifact volume;
9. tailor rigor by consequence without weakening mandatory assurance;
10. run a bounded pilot, compare it with a baseline, and adapt or stop based on evidence.

## Core Exposition

**Start with a value-stream diagnosis.** Select several representative decisions and trace elapsed time, active effort, queues, handoffs, rework, sources, conversions, approvals, defects, and resulting action. Separate demand from failure demand: creating a trade is planned work; correcting a stale copied parameter is avoidable rework. Identify the longest feedback loops and most consequential ambiguity.

**Choose a narrow pilot.** Prefer a recurring cross-discipline decision with real pain, bounded scope, available users, and measurable baseline—for example interface-change impact or configuration-specific verification readiness. Avoid the easiest decorative diagram and the enterprise-wide hardest problem. Name a sponsor who can remove obstacles and a decision owner who will use the output.

**Write decision contracts.** For each output state the question, consumer and decision owner, due cadence, authoritative inputs/configuration, required semantics, evidence and acceptance gates, visualization/export, access, and retirement trigger. This turns “make an architecture model” into a testable obligation such as “by each interface review, compare incompatible units/directions and show unresolved owner/action.”

**Define the minimum sufficient model.** Work backward from decision and evidence. Include necessary identities, relationships, properties, units, states, constraints, configurations, assumptions, provenance, and uncertainty. Exclude unrelated detail unless it supports reuse with an identified consumer. Minimum sufficient is not minimal syntax; critical semantics may require substantial depth.

**Map authority before integration.** Declare which repository owns requirement text, design structure, analysis parameters, interface contracts, code, manufacturing state, test results, and approvals. Reference or transform instead of copying where possible. When caching is necessary, mark derived ownership, source/version, retrieval time, mapping, and staleness. Define conflict escalation.

**Design domain boundaries.** Partition by stable responsibility and change cadence rather than diagram type. Give each package/module an owner and published interface. Minimize cycles and shared write zones. A central integration model can assemble released contracts without making a small modeling office responsible for every discipline's facts.

**Choose a teachable language subset.** Publish allowed concepts, precise meanings, naming, units, identity, relationship direction, package imports, configuration, and stereotype/extension policy with short examples. Add concepts only for a decision need. Prefer standard semantics; every extension adds learning, mapping, validation, and migration cost.

**Offer multiple fit-for-purpose views.** Modelers may edit precise textual or graphical notation; reviewers may need tables, dependency maps, parameter comparisons, generated documents, or API queries. Generate views from authoritative content. A stakeholder should not need full tool proficiency to review a contract, but review feedback must link to stable model identities.

**Make small changes.** A useful increment answers one question, closes one inconsistency, adds one interface contract, or enables one analysis. Keep diffs reviewable. Integrate frequently to avoid semantic merge avalanches. Long-lived branches require explicit reason, reconciliation cadence, and owner.

**Define done.** A modeling increment is not done when a diagram looks complete. Done may require source/configuration declared; syntax/metamodel/profile validation; references resolved; units/cardinality/invariants passed; applicable analysis/tests passed; derived outputs regenerated; review comments disposed; provenance captured; consumer acceptance recorded; and baseline/change notes updated.

**Automate fast gates.** Run cheap structural and semantic checks on each proposed change. Run targeted analysis and integration checks from dependency impact. Keep error messages tied to element IDs and remediation. Do not automate approval of assumptions or safety judgments merely because a rule can inspect fields.

**Review semantics through diffs and views.** Show changed elements, relationships, properties, assumptions, interfaces, affected analyses/tests, configuration, and generated downstream changes. Assign reviewers by ownership and consequence. Time-box disposition, distinguish blocking from advisory feedback, and record unresolved dissent. Large milestone screenshots hide both change and reviewer overload.

**Manage work in progress.** Limit concurrent decision products to actual modeling and review capacity. Starting more work does not increase throughput when the bottleneck is an unavailable domain approver. Visualize ready, active, blocked, review, rework, and accepted states. Escalate aging work and reduce batch size.

**Integrate analysis continuously.** Parameter and behavior models should feed executable analyses with recorded inputs, versions, assumptions, diagnostics, outputs, and evidence limits. Compare model predictions with tests and operations. A one-click analysis without reproducible provenance is convenience, not trustworthy automation.

**Connect downstream work by contract.** Publish stable identities, schemas, APIs/exports, events, configuration rules, and compatibility promises. Let software, data, manufacturing, and test teams retain suitable native tools. Require controlled mappings and conformance tests at boundaries; do not force semantic loss into a single modeling tool.

**Generate documents deliberately.** Some contracts and authorities require documents. Generate them from controlled models with provenance, stable anchors, review status, and reproducible templates. Define whether the generated document or model is authoritative for each fact. Manual edits to derivatives must not create a shadow source.

**Provide an enablement service.** A small enablement group should maintain patterns, validation, integrations, training, office hours, and migration support. It should reduce dependency on itself by making common work self-service. Track time-to-first-useful-change, support wait, recurring questions, and ownership transfer—not only training attendance.

**Budget model health.** Regularly repair ambiguous semantics, cycles, duplicated facts, stale derived views, broken references, slow validation, brittle extensions, and inaccessible expertise. Reserve capacity based on decision impact. Do not create a generic cleanup backlog disconnected from consumers; link debt to risk, delay, or rework.

**Measure outcomes and flow.** Track decision lead time, review latency, active/wait/rework time, WIP/aging, change-failure/rollback, escaped interface/configuration defects, stale or orphaned content, analysis reproducibility, trace gaps by consequence, reuse with active consumers, and user decision satisfaction. Always define scope, numerator/denominator, collection method, and gaming risks.

**Protect exploration.** Early trade exploration may use lighter structure and provisional branches/sandboxes. Label assumptions and non-authoritative results. Promote useful content through normal identity, semantics, validation, review, and configuration gates. Do not make ideation wait for release rigor, and do not let an exploratory screenshot become an approved baseline.

**Tailor by consequence.** A low-consequence concept comparison may accept peer review and reproducible inputs. A safety-critical interface may require independent review, formal constraints, verified transformations, test evidence, signatures, and technical authority. Tailoring changes evidence depth, not the obligation to state assumptions and authority.

**Scale through federation and patterns.** Replicate proven decision contracts, modules, checks, and interfaces, not an entire pilot bureaucracy. Establish enterprise identity and interoperability principles while allowing domain-specific methods. Communities of practice share cases and evolve patterns; governance adjudicates cross-domain rules and exceptions.

**Run retrospectives with removal power.** Review whether outputs were used, which decisions improved, where users waited, what failed, and what no longer earns its cost. Delete or archive unused generated views, combine redundant reviews, simplify profiles, and retire metrics that drive gaming. Preserve governed history and contractual records while removing active workflow burden.

The following synthetic check makes waiting visible in a tiny decision-product flow. Values are declared teaching data, not observed project performance.

<!-- bijux-verify: {"id":"mbse-decision-flow-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"items=4\ncontract_complete=4\ncompleted=2\ncompleted_gates_passed=2\nwip=2\nwip_limit=2\nactive_hours=16\nwait_hours=24\nrework_hours=4\nlead_hours=44\nflow_efficiency_percent=36.4\noverdue_items=1\nstatus=declared_workflow_fixture_passed\nevidence=synthetic_flow_metadata_only\n","stderr":""}} -->
```python
items = [
    {"id": "interface-units", "owner": "systems", "consumer": "test", "evidence": "contract-check", "gate": True, "state": "done", "active": 5, "wait": 4, "rework": 1, "due": 12, "age": 10},
    {"id": "power-trade", "owner": "power", "consumer": "chief-engineer", "evidence": "trade-run", "gate": True, "state": "done", "active": 6, "wait": 8, "rework": 2, "due": 20, "age": 16},
    {"id": "thermal-margin", "owner": "thermal", "consumer": "design-review", "evidence": "analysis-run", "gate": False, "state": "review", "active": 3, "wait": 9, "rework": 1, "due": 11, "age": 13},
    {"id": "verification-impact", "owner": "verification", "consumer": "change-board", "evidence": "impact-query", "gate": False, "state": "active", "active": 2, "wait": 3, "rework": 0, "due": 8, "age": 7},
]
required = ("owner", "consumer", "evidence", "gate", "due")
complete_contracts = sum(all(key in item and item[key] not in (None, "") for key in required) for item in items)
completed = [item for item in items if item["state"] == "done"]
wip = sum(item["state"] in {"active", "review"} for item in items)
active = sum(item["active"] for item in items)
wait = sum(item["wait"] for item in items)
rework = sum(item["rework"] for item in items)
lead = active + wait + rework
overdue = sum(item["state"] != "done" and item["age"] > item["due"] for item in items)
print(f"items={len(items)}")
print(f"contract_complete={complete_contracts}")
print(f"completed={len(completed)}")
print(f"completed_gates_passed={sum(item['gate'] for item in completed)}")
print(f"wip={wip}")
print("wip_limit=2")
print(f"active_hours={active}")
print(f"wait_hours={wait}")
print(f"rework_hours={rework}")
print(f"lead_hours={lead}")
print(f"flow_efficiency_percent={100 * active / lead:.1f}")
print(f"overdue_items={overdue}")
print("status=declared_workflow_fixture_passed")
print("evidence=synthetic_flow_metadata_only")
```

The result suggests examining review capacity and the overdue thermal-margin item. It does not show whether waiting was avoidable, whether effort estimates are accurate, whether WIP two is optimal, or whether model content and decisions are sound.

## Definitions and Notation

Let $D$ be the set of governed decisions and $M$ the set of model content. Define $supports(m,d)$ only when model content $m$ has an identified use in decision $d$ or its required evidence. Content without current support may still be retained for contractual, historical, reuse, or risk reasons, but the reason and review date should be recorded.

For item $w$, define elapsed lead time $L_w=t_{accepted}-t_{ready}$, active time $A_w$, waiting time $W_w$, and rework $R_w$. Queues may overlap, so organizations must define measurement carefully; the additive teaching model is not automatic in real telemetry.

Let a gate result be one of $\{pass,fail,unknown,unavailable,not\ applicable\}$. Collapsing unknown or unavailable into pass destroys assurance; collapsing them into fail can hide infrastructure failures. Acceptance policy maps each result to action by consequence.

Define model freshness relative to its declared sources and decision, not wall-clock age alone. A stable baseline can remain fit for a historical audit, while a one-hour-old derived view can be stale if its source changed ten minutes ago.

## Mechanisms, Invariants, or Proof Structure

A pilot earns expansion through a bounded evidence argument:

1. **Baseline:** measure the existing decision path, defects/rework, lead time, active/wait time, evidence quality, and user outcome.
2. **Contract:** name decision, owner, consumer, minimum output, authorities/configuration, evidence, gates, cadence, and stop/adapt rule.
3. **Implementation:** establish boundaries, language subset, identities, source contracts, automation, review capacity, training, and recovery.
4. **Delivery:** produce small accepted increments and preserve model-to-decision provenance.
5. **Comparison:** compare the same decision class with baseline while reporting confounders, sample size, missing data, and adverse effects.
6. **Adoption:** confirm intended users actually use the product and can interpret/update it without unsustainable specialist dependency.
7. **Control:** verify mandatory assurance, configuration, security, records, and contractual obligations remain satisfied.
8. **Decision:** expand, adapt, hold, or retire. Do not scale on enthusiasm or artifact volume alone.

The key invariant is that reducing ceremony must not remove the evidence needed for consequence, and adding rigor must not add an artifact or approval without a stated control objective. When a control objective is valid but the mechanism is slow, redesign the mechanism rather than waiving the objective or defending the queue.

## Alternatives and Trade-Offs

**Central model versus federated models.** One repository simplifies traversal and common rules but creates ownership, scale, access, and tool-fit problems. Federation preserves domain autonomy but needs identities, contracts, mappings, configuration, and thread evidence. Use one logical authority map even when physical stores differ.

**Graphical versus textual authoring.** Graphical views support spatial understanding and stakeholder communication; text supports precise diffs, search, generation, and familiar code review. SysML 2.0 supports complementary representations. Choose by work and user, while keeping one underlying semantic authority.

**Trunk-based integration versus feature branches.** Frequent integration reduces divergence and exposes conflicts early; branches protect experiments and incomplete work. Keep branches short, validate continuously, and define baseline/release separately from merge. Safety evidence may need controlled approval after integration.

**Central modeling team versus embedded ownership.** Specialists accelerate startup and difficult semantics, but central ownership becomes a queue and knowledge bottleneck. Embedded domain owners improve fidelity. A hub-and-spoke model works when enablement supplies patterns/tools and domains own content.

**Strict profile versus flexible conventions.** A narrow profile improves consistency and automation but can exclude legitimate semantics and raise change friction. Flexibility speeds exploration but raises review and interoperability cost. Use a small governed core, explicit extensions, and promotion criteria.

**Synchronous boards versus asynchronous review.** Boards help cross-domain, high-consequence decisions; they batch work and consume scarce calendars. Automated gates and asynchronous owner review suit routine changes. Escalate by consequence, disagreement, or cross-boundary impact.

**Build versus buy.** Commercial tools may offer mature modeling, configuration, and support; open/custom stacks may offer automation and portability. Evaluate decision workflow, API/export fidelity, automation, licensing/access, supplier fit, performance, data rights, security, longevity, migration, and exit—not feature counts.

## Failure Modes and Misconceptions

- **“MBSE means replacing every document.”** Required and useful documents may remain generated decision/evidence views. The problem is duplicate manual authority.
- **“The most complete model wins.”** Completeness is relative to declared scope and use. Unused detail delays feedback and creates maintenance burden.
- **“All engineers must become expert modelers first.”** Domain owners need usable contribution/review paths; enablement should reduce specialist mediation.
- **“One tool ensures one truth.”** Authority is governance plus configuration and semantics. One tool can contain duplicates and conflicting versions.
- **“A green validator means the design is good.”** Automation establishes declared rules, not requirement validity, architecture merit, or stakeholder acceptance.
- **“Agile means no baselines or reviews.”** Small increments and feedback coexist with configuration control and consequence-aware assurance.
- **“Compliance requires every traditional meeting.”** Preserve control objectives and evidence; tailor redundant mechanisms through authorized governance.
- **“Model element count proves adoption.”** Counts reward bloat. Measure decisions, users, latency, defects, evidence and sustainable ownership.
- **“A pilot success proves enterprise scale.”** Scale changes performance, ownership, supplier, access, migration, support, and governance conditions.
- **“Automation removes people.”** It moves people toward semantics, exceptions, trade-offs and acceptance; it also creates code, mapping, infrastructure, and monitoring obligations.

## Worked Examples

### Example 1

A program starts with “build the full logical architecture.” No decision, consumer, or deadline is named, so modelers create hundreds of blocks and diagrams. Replace the mandate with an interface-readiness decision for the next integration event. The minimum model covers participating functions/components, interface identities, direction, units, rates, states, ownership, configuration, unresolved issues, and test hooks. Other architecture content is added only for known downstream use. The result is narrower but more defensible; it does not establish whole-system architecture completeness.

### Example 2

A central model copies requirement text from a governed requirements system so diagrams are self-contained. Copies drift. The authority map retains requirement ID/version/status in the requirements service and resolves text through an API/cache with provenance and staleness. The model owns allocations and design relationships. Generated review views join them at a snapshot. If the service is unavailable, the view reports stale/partial rather than letting the cache become silent authority.

### Example 3

Thirty modelers edit one package and merge monthly. Conflicts are semantic and reviewers cannot isolate intent. Partition by propulsion, power, thermal, guidance, and cross-system interface contracts, each with owner and published dependencies. Validate changes locally and integrate at least daily; baseline separately. Cycles and shared-write elements require explicit refactoring. Shorter integration reduces divergence, but a boundary design review must confirm the new modules reflect real ownership.

### Example 4

Every change waits for a weekly two-hour board, including spelling corrections and generated-view refreshes. The team defines tiers: automated validation plus owner approval for low-consequence changes; asynchronous affected-owner review for normal semantic changes; board review for baseline, safety-critical, disputed, or cross-program decisions. Audit samples check the tiering rule. Lead time falls without waiving the control objective. Whether risk remains acceptable needs observed defect and exception evidence.

### Example 5

A custom profile contains eighty stereotypes and mandatory tagged values. New users take months and use fields inconsistently. Usage analysis finds twelve concepts support current decisions. The team defines their semantics and checks, maps legacy content, retains rare mandatory regulatory extensions, and deprecates the rest with migration history. Smaller vocabulary improves consistency. It is not inherently superior if omitted semantics were consequential, so domain and assurance owners approve the reduction.

### Example 6

An analysis view is recreated manually before every review. Instead, controlled model parameters and assumptions feed a versioned script; results record input configuration, code/environment, diagnostics, digest, uncertainty, review, and validity. The report is generated with stable IDs and marks stale when inputs change. Automation removes transcription, not analyst responsibility. Verification still assesses formulation, implementation, applicability, and results.

### Example 7

Software engineers reject the modeling tool because code review and CI are faster. The workflow publishes interface/state contracts through a versioned API and generated test fixtures, while software remains authoritative in version control. Model changes trigger conformance tests; software discoveries create reviewed model updates. This preserves tool fit and feedback. Generated stubs are not proof that runtime timing, concurrency, failure, or integration behavior satisfies the system contract.

### Example 8

A dashboard claims 95% trace coverage, but the missing 5% includes a catastrophic hazard. Replace the scalar with coverage by consequence, unresolved critical paths, configuration applicability, stale links, evidence acceptance, and unknown/filtered sources. Keep the total for trend only. Release blocks on unresolved critical evidence even if the average rises. Metrics now support decisions but remain susceptible to classification errors and require sampling.

### Example 9

A pilot reduces interface-defect rework, but its champion personally resolves every tool and semantic problem. Expansion would multiply a hidden bottleneck. The team measures support wait and ownership, documents patterns, automates setup/checks, trains embedded domain maintainers, and runs the pilot during the champion's absence. If service degrades, the adoption claim fails. Sustainable capability—not one expert's heroics—is the scale criterion.

### Example 10

An exploratory trade sandbox generates a promising configuration. Management circulates its screenshot as if approved. The workflow labels sandbox content non-authoritative and records assumptions. Promotion assigns stable identity, resolves sources/configuration, runs required analyses and gates, obtains affected-owner review, and creates a controlled baseline. Exploration remains fast while approval is explicit. Promotion proves the declared evidence process, not that every stakeholder need or hidden risk is resolved.

## Cross-Program Connections

- **Platform engineering:** self-service repositories, identity, policy, validation, CI, artifact stores, observability and supported templates make the right modeling workflow easy without centralizing content ownership.
- **API and service engineering:** versioned contracts, partial failure, events, authorization, compatibility and SLOs enable federated models and generated decision views.
- **Data engineering:** lineage, quality, schema evolution, bitemporal history, reproducible pipelines and health measures keep integrations honest.
- **Object-oriented programming:** domain boundaries, encapsulated invariants, stable identity, repositories, adapters and explicit ownership inform modular models.
- **Functional programming:** immutable change, pure transformations, algebraic result types, composable checks and property-based testing improve reproducibility and validation.
- **Organizational design:** queues, cognitive load, review capacity, incentives, authority and communities of practice determine whether technical workflow changes persist.

## References

1. NASA, [Systems Engineering Handbook](https://www.nasa.gov/reference/systems-engineering-handbook/), current web edition, accessed 2026-08-31.
2. NASA, [NASA Systems Engineering Handbook, NASA/SP-2016-6105 Rev2](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf), 2016.
3. NASA, [NASA-HDBK-1009A, NASA Systems Modeling Handbook for Systems Engineering](https://standards.nasa.gov/standard/NASA/NASA-HDBK-1009), active standards record, 2025.
4. NASA, [NASA-HDBK-1004, NASA Digital Engineering Acquisition Framework Handbook](https://standards.nasa.gov/standard/nasa/nasa-hdbk-1004), active standards record, accessed 2026-08-31.
5. Object Management Group, [SysML v2 overview](https://www.omg.org/sysml/sysmlv2/), official language overview, accessed 2026-08-31.
6. Object Management Group, [Systems Modeling Language 2.0, Language Specification](https://www.omg.org/spec/SysML/2.0/Language/PDF), formal specification, 2026.
7. Object Management Group, [Systems Modeling API 1.0](https://www.omg.org/spec/SystemsModelingAPI/1.0/PDF), formal specification, 2025.
8. U.S. Government Accountability Office, [Weapon Systems Testing: DOD Needs to Update Policies to Better Support Modernization Efforts](https://files.gao.gov/reports/GAO-26-107009/index.html), GAO-26-107009, 2025.
9. National Institute of Standards and Technology, [Model-Based Enterprise Summit Report](https://www.nist.gov/publications/model-based-enterprise-summit-report), publication record, 2018.
10. National Institute of Standards and Technology, [Model-Based Enterprise Program](https://www.nist.gov/programs-projects/model-based-enterprise-program), program record, accessed 2026-08-31.

## Exercises

### Exercise 1

Create a decision contract and minimum sufficient model for approving a battery thermal interface before prototype integration. Include authorities, consumers, configuration, evidence, gates, cadence, and exit criteria.

### Exercise 2

Diagnose a workflow with 12 active model products, two modelers, one weekly reviewer, monthly merges, 70 mandatory stereotypes, and a target of 10,000 elements. Propose a safer operating model and measures.

### Exercise 3

Design an incremental review and CI policy for a federated safety-relevant model spanning requirements, SysML, software, analysis, and test services. Explain which judgments remain human.

### Exercise 4

An organization claims its pilot cut decision time by 40%. Define an evaluation that tests whether the workflow caused the improvement and can scale sustainably without weakening assurance.

### Exercise 5

Plan retirement of an unused manually maintained model view that appears in a contractual review package. Preserve authority, history, stakeholders, and auditability while removing duplicate work.

## Answers to the Exercises

### Answer 1

The decision is whether the battery-to-cooling-loop interface is ready for prototype integration for configuration P3 by a named integration authority. Consumers include battery, thermal, mechanical, electrical, safety, test, manufacturing, and integration owners. The minimum model covers stable interface/component identities; P3 geometry/attachment; heat loads and operating/fault envelopes; coolant type, flow, pressure, temperature, leakage and contamination constraints; sensors/controls; units, tolerances and reference frames; assumptions/uncertainties; ownership; applicable hazards; and verification hooks.

PLM governs released physical interface geometry/material; requirements management governs approved obligations; thermal analysis governs declared model/run results; safety governs hazard controls; test management governs procedures/results; configuration management governs P3 composition and deviations. The decision view resolves these sources at a snapshot rather than copying authority.

Evidence includes compatible mechanical/fluid/electrical contracts, reproducible worst-case analysis, uncertainty/margin, material/contamination assessment, fault/leak response, applicable prototype test readiness, unresolved issue list, and approvals. Automated gates check identities, units, ranges, unresolved references, configuration, constraint consistency, stale analyses, and trace. Humans assess assumptions, model validity, trade acceptability, safety, manufacturability, and residual risk.

Deliver reviewable increments as contracts mature; review latency target and escalation are stated. Exit occurs after integration approval and evidence baseline, with the active decision view retired or adapted into verification/operation use. The model cannot prove physical fit or thermal performance before applicable realization and test evidence.

### Answer 2

WIP 12 exceeds two modelers' and one reviewer's capacity, so items age and monthly merges amplify divergence. Seventy mandatory stereotypes raise learning and inconsistent-entry risk, while a 10,000-element target rewards volume rather than decisions.

Map the twelve products to decisions, consumers, consequence, due date, authority, current value, and remaining work. Stop starting low-value items; set an initial WIP limit based on observed throughput and review capacity, perhaps two active plus one review item, then adjust from data. Break products into small decision increments and integrate at least daily. Move routine changes to automated gates and asynchronous ownership review; reserve the weekly reviewer for high-consequence/disputed work or add qualified review capacity.

Analyze stereotype use and decision dependence. Retain a small governed core plus mandatory domain extensions, migrate with evidence, and deprecate unused fields. Replace the element target with decision lead/review latency, active/wait/rework, aging, accepted decision products, escaped interface/configuration defects, stale content, critical evidence gaps, sustainable ownership, and user usefulness. Audit metric gaming. Assurance gates remain consequence-based; faster flow cannot excuse missing safety evidence.

### Answer 3

Give each service an authority and stable identity/version contract. A change event or pull request names intent, configuration and affected decision products. Fast CI validates local syntax/schema/profile, IDs, references, units, cardinalities, naming and package boundaries. Impact traversal selects cross-service contract tests: requirement-to-design mappings, interface compatibility, generated API/test fixtures, analysis regeneration, code conformance, verification applicability, stale derivatives and security/access behavior.

Use reproducible source positions or baselines, versioned mappings, explicit unavailable/unknown results, and retained diagnostics/digests. Small compatible changes can merge after automated checks and affected-owner review; safety-significant changes additionally require independent reviewers, safety/assurance evidence and technical authority. Baseline approval is separate from merge. Periodic clean rebuild/reconciliation detects missed events and stale indexes; recovery can restore the last accepted baseline.

Humans still judge stakeholder intent, requirement validity, architecture/trade merit, model and analysis applicability, assumptions and uncertainty, safety argument sufficiency, unusual mapping loss, exception acceptance, conflicting owner views, and residual risk. Automation routes and tests evidence; it does not hold accountability.

### Answer 4

Define “decision time” from the same ready condition to authorized disposition for a named decision class. Establish pre-pilot distributions for lead, active/wait/rework, decision quality indicators, defect escape, reopen/rollback, assurance findings, user satisfaction, and support effort. Compare a sufficient set of similar pilot and non-pilot decisions or use time-series evidence, documenting complexity, staffing, urgency, tooling, review priority and policy changes. Report sample sizes, medians/distribution, missing data and adverse outcomes—not only 40%.

Trace mechanisms: did smaller increments reduce review wait, did automation remove rework, did authority mapping prevent reconciliation, and did users act on outputs? Check that work was not reclassified, started later, rushed, shifted downstream, or given privileged reviewer access. Independently sample content and assurance evidence.

For scalability, measure enablement/support wait, time-to-first-useful-change, domain ownership, performance with more repositories/users, supplier/access constraints, license/infrastructure cost, interoperability, recovery, and operation without the pilot champion. Define thresholds and stop/adapt rules. A causal claim remains bounded because organizational experiments have confounders; evidence may justify expansion without proving universal effect.

### Answer 5

First identify the contractual clause, control objective, approving authority, consumers, source facts, review history, retention need, and whether the view or underlying facts are authoritative. Demonstrate duplicate effort and propose a generated replacement or a contract amendment; do not silently delete a deliverable.

If the contract permits tailoring, obtain stakeholder and authority approval for a reproducible generated view from governed sources. Define template/version, snapshot/configuration, stable anchors, provenance, validation, review, access and archival output. Reconcile the last manual view against sources, disposition differences, and record the cutoff baseline. Freeze the manual artifact read-only with its history and link successors; remove edit obligations and monitoring jobs only after the generated path passes a representative review and recovery test.

Track preparation time, discrepancies, review usefulness, generation failures, staleness and audit retrieval. If the generated view cannot meet a needed control or legal format, simplify the manual workflow instead of falsely declaring success. Retirement removes duplicate active authority while preserving historical evidence and the contractual decision trail.
