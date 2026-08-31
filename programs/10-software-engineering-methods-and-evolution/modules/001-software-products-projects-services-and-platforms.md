---
module_id: SEME-001
program: Software Engineering: Methods & Evolution
level: 1
module_number: 1
title: Software Products, Projects, Services, and Platforms
status: complete
last_verified: 2026-08-29
---

# Software Products, Projects, Services, and Platforms

## One-Page Review

### Governing question

When software persists beyond a delivery date, which product, project, service, and platform responsibilities must continue—and how should an organization align ownership, funding, evidence, and change around them?

### Essential definitions

- A **software product** is an intentionally bounded offering that creates outcomes for identified users or customers and evolves through evidence about value, quality, risk, and viability.
- A **project** is a temporary endeavor organized to produce a unique result, product, service, or change under explicit objectives and constraints.
- A **service** is an ongoing capability delivered by a provider to consumers under an operating relationship and agreed expectations for utility, quality, support, continuity, and change.
- A **platform** is a shared foundation that curates capabilities and interfaces for multiple user groups or products; an internal platform should be managed as a product and operated as one or more services.
- An **asset** is a durable artifact such as source code, data, documentation, model, executable, or configuration. Assets enable products and services but are not automatically products.
- A **lifecycle** spans conception, acquisition/development, introduction, operation, support, evolution, and retirement; activities can overlap, repeat, and occur recursively.
- An **operating model** assigns enduring decision rights, funding, work intake, engineering, operation, measurement, support, governance, and retirement responsibilities.
- An **outcome** is a change in stakeholder condition or capability; an **output** is a produced artifact or release; an **activity** is work performed.
- **total cost of ownership** includes acquisition/build, integration, operation, support, security, compliance, change, migration, and retirement costs—not only initial delivery.

### Central model, mechanism, or theorem

The categories answer different questions and may overlap:

$$
Work = Change_{temporary} + Stewardship_{continuing},
$$

$$
Value(t)=Outcomes(t)-LifecycleCost(t)-RiskExposure(t).
$$

A project can create or change a product, service, or platform; closure transfers accepted results and unresolved obligations to durable owners. A product defines for whom and why to evolve. A service defines how capability is continuously delivered and supported. A platform defines which reusable capabilities and interaction boundaries enable others. The invariant is continuity of ownership across every transition—not preservation of a particular team name or method.

### Critical invariants

- Identify users, customers, beneficiaries, operators, maintainers, funders, regulators, and people bearing externalities; they are not interchangeable.
- Give every live offering an accountable owner, operating owner, support route, funding horizon, evidence set, and retirement authority.
- Separate project completion from product outcome, service health, platform adoption, and lifecycle completion.
- Preserve traceability from needs and risks through changes, releases, operations, incidents, learning, and retirement.
- Fund and plan maintenance, security, dependencies, data stewardship, compatibility, support, observability, and decommissioning.
- Measure outcomes with quality, safety, equity, security, reliability, cost, and sustainability guardrails; activity or adoption alone is insufficient.
- Make project-to-operations/product transition an acceptance decision with evidence, not a ceremonial handoff.
- Treat internal users as real users and platform teams as accountable providers, while leaving domain decisions with domain owners.
- Maintain viable escape, migration, and retirement paths; perpetual operation is not the default.
- Do not infer external approval, product-market fit, safety, or public value from delivery metrics alone.

### Common failures

Common failures include calling a repository a product; treating a deadline as the lifecycle end; dissolving the team after launch; funding features but not operations; assigning product ownership without decision rights; confusing customers with users or beneficiaries; treating incident volume as the only service evidence; building a platform as a mandated tool catalog; centralizing domain authority in a platform; measuring releases, story points, utilization, or portal visits as value; letting projects optimize local scope while transferring unpriced obligations; keeping obsolete services because no one owns retirement; and applying accounting labels as engineering strategy.

### Compact example

A six-month project migrates a customer portal. The portal remains a product because customers still have outcomes and unmet needs; it remains an online service because availability, security, support, data, and incidents continue; it may consume an identity/deployment platform. Project success requires an accepted migration result, but product success requires improved customer outcomes, service success requires sustained operating evidence, and platform success requires reusable outcomes for multiple consuming teams. Four scorecards answer four different questions.

### Connections

[SDDM-001](../../09-software-engineering-software-design-and-domain-modeling/modules/001-distinguishing-the-problem-domain-from-the-solution-domain.md) separates problem and solution domains. [SEPAT-001](../../11-software-engineering-patterns/modules/001-recurring-problems-context-forces-and-consequences.md) frames reusable decisions by context and consequences. The successor [SEME-002](../ROADMAP.md) develops lifecycle activities and feedback loops; [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns internal-platform mechanisms in depth.

## Governing Question

How can an organization stop treating software as a one-time construction deliverable and instead govern temporary change together with enduring product, service, and platform obligations?

The answer begins by refusing a false classification exercise. “Is this a project or a product?” is often less useful than asking which temporary change system and which continuing stewardship system are both required. A consumer-facing application can simultaneously be a product, deliver a service, consume a platform, and undergo several projects. Each view exposes different obligations. Removing one label does not remove the obligation it represented.

## Why This Matters

Software rarely becomes inert after acceptance. Dependencies expire, threats change, regulations and user needs evolve, traffic and data grow, operators learn, organizations restructure, and surrounding systems alter their contracts. Even intentionally stable software requires monitoring, recovery, compatibility decisions, security response, knowledge preservation, and eventual retirement.

Project-centric governance is useful for bounded transitions: consolidate data centers, replace an identity provider, meet a statutory date, or launch an initial capability. It becomes dangerous when its temporary budget and team are mistaken for the lifetime of the resulting system. The project can finish on schedule while transferring fragile code, unresolved risks, no support capacity, and no authority to change the product.

Product thinking corrects attention toward users and outcomes, but it is not sufficient alone. A compelling roadmap without service operations fails at 03:00. A reliable service without product discovery can preserve an obsolete workflow perfectly. A platform with excellent infrastructure but no usable journeys shifts cognitive load to consumers. Durable software engineering coordinates all four views.

## Prerequisites and Retrieval

Retrieve these ideas before proceeding:

- stakeholder, user, customer, beneficiary, sponsor, owner, operator, and supplier;
- requirements, quality attributes, constraints, risks, assumptions, and evidence;
- deployment, operation, incident, maintenance, compatibility, migration, and retirement;
- fixed and variable cost, opportunity cost, total cost of ownership, and risk exposure;
- feedback loops and the distinction among activity, output, outcome, and impact;
- service level objective as a target, not a universal guarantee;
- software asset, system boundary, dependency, interface, and authoritative data source.

You should be able to explain why finishing code is not the same as releasing safely, why release is not adoption, why adoption is not value, and why value for one stakeholder can create harm or cost for another.

## Learning Objectives

After completing this module, you should be able to:

1. define product, project, service, platform, asset, lifecycle, outcome, and operating model precisely;
2. classify one software initiative under all applicable views instead of forcing one label;
3. identify temporary objectives and enduring obligations separately;
4. design a project-closure transition with acceptance evidence and named receiving owners;
5. construct product and service boundaries around users, outcomes, operations, dependencies, and risks;
6. distinguish a platform product from a tool collection or centralized domain owner;
7. select evidence for product value, project progress, service health, and platform effectiveness;
8. expose lifecycle costs and risks hidden by initial delivery budgets;
9. diagnose ownership, funding, metric, transition, and retirement failure modes;
10. transfer the model to a regulated or safety-critical unfamiliar domain without claiming automated authorization.

## Core Exposition

### Products organize continuing value decisions

A product is not synonymous with packaged software, a commercial SKU, an application, or a repository. It is a managed boundary around a value proposition and a set of users or customers. Product work asks: whose condition should improve, which problem matters, what behavior or capability changes it, how will evidence alter priorities, and when is continued investment no longer justified?

The boundary can be external or internal. Payroll software used only by employees can be a product if a durable owner studies user outcomes, makes trade-offs, supports change, and bears lifecycle consequences. Conversely, a public application with no outcome ownership may be operated as an asset or service but poorly managed as a product.

Product ownership requires decision rights, not merely backlog administration. The owner must reconcile user value, strategy, safety, security, quality, economics, legal constraints, technical sustainability, service health, and retirement. A product team needs engineering and discovery capabilities appropriate to the domain; “permanent team” is not a license to ignore governance or periodically rejustify investment.

Define a product boundary with:

- named user/customer/beneficiary groups and excluded groups;
- problems, desired outcomes, and harmful externalities;
- capabilities and authoritative responsibilities;
- interfaces, dependencies, data and policy boundaries;
- quality, safety, security and compliance constraints;
- outcome evidence and decision cadence;
- operating/support model and lifecycle funding;
- compatibility, migration, exit, and retirement policy.

### Projects organize temporary change

A project is temporary and produces a unique result. Temporary does not mean short, and unique does not mean every task is novel. A project has a chartered objective, sponsor, scope or outcome boundary, constraints, dependencies, risks, resources, governance, and completion/termination conditions.

Projects are appropriate when coordination must intensify around a bounded transition: establish a new service, perform a merger migration, remediate a regulatory gap, or retire a data center. Their strengths are explicit authorization, focus, dependency planning, risk management, and a closure decision. Their weakness is structural: temporary incentives can optimize declared scope, schedule, and budget while exporting lifecycle cost.

Project output can be accepted yet fail to produce intended outcome. A new claims portal may meet functional acceptance but reduce successful completion for users with assistive technologies. Therefore review both **delivery performance** (forecast, scope, cost, quality evidence, risk) and **outcome realization** after use. Benefits often mature after the project team would normally disband.

Closure requires more than “deployed.” The receiving product/service owners accept artifacts, configuration, data, licenses, security findings, operational readiness, support capacity, supplier commitments, recovery evidence, observability, documentation, unresolved risks, costs, roadmap obligations, and retirement consequences. If no durable owner can accept them, the result is not operationally complete.

### Services organize continuing delivery relationships

A service provides capability through a continuing provider-consumer relationship. It can be human-assisted, fully digital, internal, external, paid, public, synchronous, asynchronous, or batch. The service boundary includes utility—what consumers can accomplish—and warranty/quality expectations such as availability, capacity, continuity, security, support, accessibility, and data handling.

Operation is not merely keeping servers up. Service management includes demand/capacity, requests, incidents, problems, changes, releases, configuration, suppliers, continuity, security, knowledge, support communication, measurement, and improvement. Product changes and service operations share one system: incident evidence may change roadmap priorities; a product experiment must respect service risk; an architectural change alters operating cost.

Reliability is conditional. State the service, population, measurement window, indicator, target, exclusions, dependencies, escalation, and consequence. A 99.9% availability number does not describe correctness, data integrity, accessibility, customer support, recovery, or safety. Nor is an internal service exempt because no invoice crosses an organizational boundary.

### Platforms organize shared leverage

“Platform” has several meanings: technical execution foundation, business ecosystem connecting participant groups, or internal developer/data/ML capability surface. This module focuses on the operating distinction: a platform enables multiple consumers or products through reusable capabilities and stable interaction boundaries.

An internal platform should be treated as a product because it has users, journeys, alternatives, adoption friction, outcomes, and a roadmap. It is also operated as services with reliability, support, security, capacity, compatibility, and cost. It may be established or migrated through projects. The labels stack rather than compete.

A platform removes repeated accidental complexity while preserving essential domain decisions. It can own identity primitives, deployment workflows, artifact provenance, observability integrations, catalogs, templates, or policy mechanisms when these are genuinely reusable. It should not silently own customer eligibility, medical policy, pricing, or domain authorization merely because a gateway can technically enforce them.

Define platform capabilities through observed user journeys and contracts, not a vendor inventory. A paved road combines supported defaults, automation, documentation, feedback, and escape mechanisms. Mandates are justified only by explicit organizational invariants and accountable exceptions. Adoption without improved consumer outcomes can mean coercion, not value.

### Treat the categories as independent dimensions

Use a responsibility matrix rather than a single classification:

| View | Governing concern | Time horizon | Primary evidence | Completion/continuity question |
|---|---|---|---|---|
| Product | user/customer outcomes and viability | continuing while valuable | outcome, guardrail, learning, economics | should it evolve, pivot, or retire? |
| Project | bounded change objective | temporary | deliverables, risk, forecast, acceptance | can the endeavor close or stop? |
| Service | delivered capability and operating relationship | continuing while offered | service indicators, incidents, support, continuity | can consumers depend on it now? |
| Platform | reusable enablement across consumers | continuing while leveraged | journey success, adoption quality, load removed, service evidence | does shared leverage exceed imposed cost? |

One row cannot replace another. A “product operating model” may reduce temporary handoffs, but migrations and regulatory deadlines remain temporary endeavors worth governing explicitly. A project plan cannot decide product direction after closure. A service dashboard cannot determine whether the service solves a worthwhile problem.

### Establish lifecycle ownership

Modern lifecycle processes are not a one-way waterfall. Conception, acquisition, development, verification, transition, operation, maintenance, supply, and retirement can run concurrently, iteratively, recursively, and incrementally. A mature operating model makes these activities visible without requiring one named methodology.

At minimum assign:

- outcome/product decision authority;
- technical design and change ownership;
- service operation, on-call/support, continuity, and incident authority;
- data, security, privacy, safety, accessibility, compliance, and supplier ownership;
- financial ownership for build and continuing cost;
- project sponsorship and temporary coordination where applicable;
- platform capability ownership and consumer feedback;
- deprecation, migration, archival, and retirement authority.

One person can hold multiple roles in a small organization, but the decisions remain distinct. A RACI chart is not sufficient if “accountable” people lack budget, information, skills, or authority.

### Fund the whole economic lifecycle

Initial build cost is visible because it is concentrated. Continuing costs are distributed: hosting, support, incidents, security remediation, dependencies, licenses, data retention, audits, accessibility, vendor management, compatibility, observability, training, migration, and decommissioning. Estimate ranges and uncertainty rather than hiding them.

Total cost of ownership is decision-specific. Include costs borne by consumers and other teams: integration, waiting, workarounds, cognitive load, forced migrations, failed changes, and opportunity cost. A centralized platform may reduce duplicated engineering while creating a queue or lock-in. A cheap vendor license can be expensive after integration, data egress, compliance, and exit.

Do not turn capital-versus-operating accounting categories into engineering architecture. Accounting treatment depends on jurisdiction and policy; it does not determine whether stewardship is needed. Likewise, “run” work is not value-free overhead. Reliability, security, recovery and maintenance preserve or enable outcomes.

### Design transition and retirement explicitly

Transitions occur at initial launch, project closure, team/vendor changes, platform adoption, major upgrade, incident recovery, acquisition, and retirement. Each transition risks knowledge loss and orphaned obligations. Use acceptance criteria that cover outcomes and operations, not document presence alone.

A receiving owner should demonstrate that the artifact can be built, released, observed, supported, recovered, changed, secured, audited, and retired under known constraints. Exercise failure paths and access. Transfer decision history, not just current configuration. Unresolved risk must have owner, consequence, treatment, deadline/review trigger, and acceptance authority.

Retirement is a product and service outcome, often delivered through a project. Inventory consumers, dependencies, data/legal retention, contractual promises, alternatives, communications, migration evidence, access revocation, infrastructure deletion, archive integrity, monitoring removal, cost confirmation, and post-retirement incident route. “No traffic observed” is evidence only within the observation scope.

### Choose evidence that matches the view

Product evidence includes task success, adoption/retention where meaningful, user research, outcome movement, quality/safety guardrails, willingness or mandate context, lifecycle economics, and counterfactual uncertainty. Project evidence includes objective clarity, forecast ranges, dependency/risk state, accepted increments, cost/resource use, and transition readiness. Service evidence includes service-level indicators, correctness/data integrity, incidents, recovery exercises, capacity, support outcomes, change failure, vulnerability exposure and consumer communication. Platform evidence includes time/effort to first success, repeated work removed, supported-path success, consumer cognitive load, exception patterns, service quality, portability/exit and total organizational cost.

Metrics are interpretations, not facts without context. A rising ticket count can mean poor quality, growing adoption, easier reporting, or improved trust. Velocity is a team planning signal, not product value or cross-team productivity. Utilization near 100% can lengthen queues. Pair quantitative measures with qualitative investigation, segment distributions, preserve adverse outcomes, and record uncertainty.

### A small executable responsibility audit

This deterministic example checks that four different work views declare the minimum continuity fields required by their own contracts.

<!-- bijux-verify: {"id":"seme-001-responsibility-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"portal-migration project: ready\nclaims-portal product: ready\nclaims-api service: missing=continuity\ndeveloper-platform platform: missing=exit_path\nready=2 attention=2\n","stderr":""}} -->
```python
required = {
    "project": {"sponsor", "objective", "closure", "receiving_owner"},
    "product": {"users", "outcome", "owner", "retirement"},
    "service": {"consumers", "operator", "support", "continuity"},
    "platform": {"users", "capabilities", "owner", "support", "exit_path"},
}

work = [
    ("portal-migration", "project", {"sponsor", "objective", "closure", "receiving_owner"}),
    ("claims-portal", "product", {"users", "outcome", "owner", "retirement"}),
    ("claims-api", "service", {"consumers", "operator", "support"}),
    ("developer-platform", "platform", {"users", "capabilities", "owner", "support"}),
]

ready = 0
for name, kind, declared in work:
    missing = sorted(required[kind] - declared)
    if missing:
        print(f"{name} {kind}: missing={','.join(missing)}")
    else:
        ready += 1
        print(f"{name} {kind}: ready")
print(f"ready={ready} attention={len(work) - ready}")
```

The run proves only that declared sets satisfy this toy checklist and computes two incomplete records. It does not validate real ownership, outcomes, service continuity, platform value, project acceptance, legal duties, adequate staffing, or safety. Those require evidence and authorized human judgment.

## Definitions and Notation

Let (U) be users/beneficiaries, (O_t) observed outcomes at time (t), (Q_t) quality and risk guardrails, (C_t) lifecycle cost, and (R_t) residual risk. Let project $J=(g,b,\tau,a)$ contain goal (g), boundary/constraints (b), termination condition $\tau$, and acceptance/transition rule (a). Product (P=(U,v,B,E)) has users (U), value proposition (v), boundary (B), and evolution policy/evidence (E). Service (S=(c,p,w,o)) has consumers (c), provider (p), quality/continuity expectations (w), and operating model (o). Platform (F=(U_F,K,I,O_F)) has consumer groups, curated capabilities (K), interfaces (I), and platform outcomes (O_F).

These tuples are reasoning aids, not universal standards. `owner` means authority plus accountability and capacity. `ready` means a defined gate passed with evidence, not absence of future work. `retired` means obligations have been discharged or transferred, not merely traffic disabled.

## Mechanisms, Invariants, or Proof Structure

1. Inventory the actual system, assets, users, consumers, dependencies, obligations, work, and costs.
2. Apply all relevant views: product, project, service, platform; justify exclusions.
3. Define boundaries and authoritative decisions, including externalities and people carrying risk.
4. Assign durable owners with decision rights, funding, skills, evidence access, support and retirement authority.
5. Separate temporary objectives/closure from continuing outcomes/operations/evolution.
6. Establish lifecycle activities and transitions from conception through retirement; do not assume a single sequence.
7. Price build, operation, change, risk, consumer coordination, migration and exit.
8. Select outcome and operating evidence with safety, security, equity, reliability and cost guardrails.
9. Review dependencies, suppliers, platform/domain authority and escape paths.
10. Accept transitions explicitly; preserve open risks and decision history with named owners.
11. Reassess the boundary and investment as evidence changes.
12. Retire deliberately, verify consumer/data/access/infrastructure consequences, and retain required records.

The key review invariant is **no orphaned obligation**. For each obligation (o) across transition (t), establish either (Discharged(o,t)) or (Transferred(o,t,owner,evidence)). A project closure list that omits an obligation does not discharge it. An ownership field without authority, capacity, and acceptance is not a valid transfer.

## Alternatives and Trade-Offs

**Project-centered funding** concentrates authority and budget around a target, useful for bounded change; it can create handoffs, output incentives and maintenance cliffs.

**Persistent product teams** retain context and shorten feedback, useful for evolving outcomes; they can become permanent cost centers without portfolio review, service discipline, or retirement authority.

**Central operations organization** concentrates operational expertise and economies; handoffs and divided incentives can weaken change ownership. Product-aligned operations improve feedback but require distributed competence and governance.

**Shared platform** standardizes recurring capabilities and reduces cognitive load; it creates dependency, coordination, support, lock-in and blast-radius costs. Team-local ownership preserves autonomy but duplicates work and inconsistencies.

**Build** maximizes semantic/control fit at high lifecycle cost; **buy** accelerates capability but introduces supplier, integration, data, pricing and exit risk; **partner** shares capability and authority; **retire** removes cost/risk while requiring migration and obligation closure.

**Output contracts** are easy to specify and procure; they can reward feature completion without outcomes. **Outcome agreements** encourage learning but require measurement, guardrails, causal humility and fair allocation of uncontrollable risk.

**Mandatory paved roads** reduce variation for non-negotiable invariants; unjustified mandates suppress local context and hide platform failure. **Optional supported roads** earn adoption but must not make security/safety optional.

No model is universally superior. Choose per volatility, risk, regulation, coupling, operational criticality, supplier market, organizational capability and reversibility.

## Failure Modes and Misconceptions

- **“The codebase is the product.”** Users consume outcomes/capabilities; assets are only part of the boundary.
- **“A project ends when deployment succeeds.”** Acceptance, outcome realization, operations and transferred risk remain.
- **“Product means no projects.”** Bounded migrations, acquisitions and retirements still need temporary coordination.
- **“A permanent team guarantees product thinking.”** Without users, evidence and authority it can become a feature factory.
- **“Operations is maintenance after real development.”** Operation produces critical evidence and value continuity.
- **“A service is just an API.”** Provider, consumer, support, quality, continuity and change relationships matter.
- **“A platform is shared infrastructure.”** It needs curated journeys, contracts, ownership and consumer outcomes.
- **“Mandated adoption proves platform value.”** Measure consumer outcomes and imposed cost.
- **“Internal users do not need product research.”** Their time, cognition and alternatives are real costs.
- **“Project budget equals total cost.”** Continuing, consumer, supplier, risk and retirement costs remain.
- **“One owner field solves accountability.”** Authority, capacity, acceptance and escalation must exist.
- **“Availability proves service quality.”** Correctness, safety, security, accessibility, support and recovery remain.
- **“More releases mean more value.”** Release is output; outcome and harm require separate evidence.
- **“No observed usage means safe deletion.”** Observation coverage and latent/contractual/data dependencies matter.
- **“Lifecycle means a fixed waterfall.”** Activities can be concurrent, iterative, recursive and incremental.

## Worked Examples

### Example 1

**Situation.** A bank funds a six-month mobile-check-deposit project.

**Reasoning.** Project objective is safe launch and migration under constraints. Mobile banking remains a product with customer outcomes and fraud/accessibility guardrails, and a service with availability, correctness, support and incident duties. It consumes identity and observability platforms. Closure transfers runbooks, fraud models, unresolved risks and roadmap to durable owners.

**Conclusion.** One initiative legitimately has four operating views and four evidence sets.

### Example 2

**Situation.** An employee expense application has no external sales, so leadership calls it “just an internal tool.”

**Reasoning.** Employees are users, finance/compliance are stakeholders, and poor usability creates time, errors and delayed reimbursement. A durable product boundary and outcome evidence are useful even without revenue. It is also an operated internal service.

**Conclusion.** Product discipline depends on outcomes and evolution, not a commercial SKU.

### Example 3

**Situation.** A project reports green because 40 requested features shipped by the deadline; adoption is 8% and support has no owner.

**Reasoning.** Output/schedule evidence may support a narrow delivery claim, but outcome and transition failed. Investigate user need, alternatives, access, quality and measurement; assign or stop service ownership rather than declare success from scope completion.

**Conclusion.** Project efficiency cannot substitute for product effectiveness or service readiness.

### Example 4

**Situation.** A tax-filing service meets 99.95% availability but incorrectly rounds a rare credit.

**Reasoning.** Availability measures reachability, not result correctness. Add domain reconciliation, error/correction time, affected population, financial impact and appeal/support evidence. Product priorities and service controls must react to the incident.

**Conclusion.** Service quality is multidimensional and connected to product learning.

### Example 5

**Situation.** A developer platform launches a portal with 5,000 catalog entries and mandatory registration.

**Reasoning.** Counts prove inventory/adoption policy, not reduced cognitive load. Measure representative discovery-to-first-safe-deployment journeys, ownership freshness, failures, support handoffs, exceptions, service health, upgrade burden and exit. Remove features without a supported outcome.

**Conclusion.** A platform is a product/service, not a portal or tool count.

### Example 6

**Situation.** Platform team proposes deciding whether customers qualify for refunds because all requests pass its gateway.

**Reasoning.** Routing and identity primitives may be shared; refund eligibility is domain policy and changes with authoritative customer/order state. Centralization creates stale data and ownership ambiguity. Platform can enforce that a policy decision is authenticated/audited, not own its meaning.

**Conclusion.** Technical placement does not confer domain authority.

### Example 7

**Situation.** Organization adopts an open-source database and assumes “free” means no product or service ownership.

**Reasoning.** License price may be zero, but selection, integration, operation, upgrades, security response, data recovery, compatibility, expertise, contribution/fork strategy and exit cost remain. A temporary adoption project must transfer these duties.

**Conclusion.** Acquisition mode changes lifecycle work; it does not eliminate it.

### Example 8

**Situation.** Vendor SaaS replaces an internal scheduling system.

**Reasoning.** Vendor operates much of the service, but buyer retains outcome, configuration, identity, data governance, integration, support escalation, continuity, supplier and exit responsibilities. Migration project needs acceptance and rollback; product owner still decides whether scheduling outcomes improve.

**Conclusion.** Outsourcing implementation never outsources all accountability.

### Example 9

**Situation.** A legacy reporting service shows no calls for 90 days.

**Reasoning.** Validate telemetry coverage, batch/seasonal use, contracts, embedded dependencies, audit/legal retention, emergency procedures and consumers outside current identity. Announce deprecation, supply alternative, observe migration, archive/delete data correctly, revoke access and verify costs disappear.

**Conclusion.** Retirement is an evidence-driven lifecycle change, not server shutdown.

### Example 10

**Situation.** A public benefits eligibility system must be replaced under a statutory deadline.

**Reasoning.** Project governs migration/date; product view covers claimant/caseworker outcomes and appeal rights; service view covers correctness, availability, support, continuity and data; platform dependencies cover identity, payments and case integration. Guardrails must expose disparate harm, wrongful denial, privacy/security, accessibility, manual fallback and explainability. Deadline pressure cannot transfer silent risk to vulnerable people.

**Conclusion.** Named benefits-policy and casework owners, affected-community/accessibility representatives, legal/privacy/security specialists, service operations, data and software engineers, independent assurance/audit, and authorized public officials must review requirements, evidence, transition, exceptions and launch. Automated tests or schedule compliance cannot authorize eligibility decisions.

## Cross-Program Connections

- **Design and Domain Modeling:** defines authoritative domain language and boundaries inside product/service decisions.
- **Patterns:** recurring organizational and technical arrangements remain context-dependent trade-offs.
- **Software Architecture:** significant decisions structure product, service and platform evolution.
- **Testing and Quality:** supplies evidence techniques; quality claims must match populations and failure consequences.
- **Delivery and Reliability:** operationalizes build-to-deploy flow, service indicators, recovery and production learning.
- **Security Engineering:** threats, secure development, incident response and supply-chain duties span the lifecycle.
- **Systems Engineering:** stakeholder needs, system boundaries, acquisition, verification, transition and retirement extend beyond software.
- **Platform Engineering:** develops platform capabilities, user journeys, interfaces, paved roads and operations in depth.
- **Cloud Engineering:** provides external service/platform consumption models with shared-responsibility and exit concerns.
- **Engineering Economics:** cost of delay, optionality, TCO and risk-adjusted investment govern portfolios.

## References

- ISO/IEC/IEEE, [ISO/IEC/IEEE 12207:2026 — Software life cycle processes](https://www.iso.org/standard/90219.html), April 2026, retrieved 2026-08-29. Current lifecycle framework covering software systems, products and services from conception through retirement.
- Project Management Institute, [What Is a Project?](https://www.pmi.org/about/what-is-a-project), retrieved 2026-08-29. Current official project definition and lifecycle overview.
- ISO/IEC, [ISO/IEC 20000-1:2018 — Service management system requirements](https://www.iso.org/standard/70636.html), confirmed current in 2023, amended 2024, retrieved 2026-08-29. Service planning, design, transition, delivery and improvement framework.
- Ken Schwaber and Jeff Sutherland, [The Scrum Guide](https://scrumguides.org/docs/scrumguide/v2020/2020-Scrum-Guide-US.pdf), November 2020, confirmed as current official version 2026-08-29. Product boundary, product goal and empirical value-delivery framing.
- CNCF TAG App Delivery, [Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/), 2023, retrieved 2026-08-29. Current community guidance on internal platforms, product mindset, capabilities and user outcomes.
- NIST, [Secure Software Development Framework 1.1, SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final), February 2022, retrieved 2026-08-29. Outcome-based secure development practices integrated across lifecycle models; version 1.2 remained draft at retrieval.
- Meir M. Lehman, “Programs, Life Cycles, and Laws of Software Evolution,” *Proceedings of the IEEE*, 1980. Foundational evidence that long-lived real-world software changes with its environment.
- Mik Kersten, *Project to Product*, IT Revolution, 2018. Flow-oriented critique of project-only software governance and durable product value streams.
- Nicole Forsgren, Jez Humble, and Gene Kim, *Accelerate*, IT Revolution, 2018. Empirical treatment of delivery and organizational capabilities, with measurement and causal-scope limits.
- Frederick P. Brooks Jr., *The Mythical Man-Month*, anniversary edition, Addison-Wesley, 1995. Foundational analysis of software project coordination, schedule and conceptual-integrity limits.

## Exercises

### Exercise 1

Classify a subscription video-streaming application under product, project, service, platform, and asset views. State which views apply and one obligation exposed by each.

### Exercise 2

A twelve-month migration project has two weeks remaining. Derive a closure/transition acceptance set that prevents unfinished lifecycle obligations from disappearing.

### Exercise 3

Diagnose an internal platform whose adoption reached 95% after a mandate while deployment lead time, incidents and developer satisfaction worsened. Propose evidence and corrective decisions.

### Exercise 4

Compare build, buy and retire options for an aging employee scheduling capability using lifecycle cost, risk, product outcome, service and exit criteria.

### Exercise 5

Design the operating views and assurance transition for an unfamiliar autonomous-drone traffic coordination capability used by emergency services. Include named human review.

## Answers to the Exercises

### Answer 1

Product: viewers are users/customers; obligation is evidence that discovery/playback/content outcomes improve within accessibility, safety and economic guardrails. Service: provider continuously delivers catalog, playback, billing and support; obligation includes correctness, availability, continuity, incident response and consumer communication. Platform: if shared identity, media processing, experimentation or distribution capabilities enable multiple product surfaces/partners, each needs platform user journeys, contracts, support and exit; the streaming app alone is not automatically a platform. Projects: launch in a country, replace codec, or migrate billing are temporary changes with closure and receiving owners. Assets: clients, services, models, catalog metadata, media, infrastructure, tests and documentation. They require ownership/provenance but none alone equals the whole product. Views overlap; describe boundaries explicitly.

### Answer 2

Acceptance set names receiving product and service owners with authority/capacity; accepted build/release/recovery procedures exercised by them; complete asset/configuration/dependency/license inventory; target architecture and decision history; data migration/reconciliation and retention; security/privacy/accessibility/compliance evidence; monitoring, indicators, alerts, capacity and continuity exercises; support/on-call/escalation and supplier contacts; known defects/risks with consequence, owner, treatment/review date and acceptance authority; funding and staffing; customer/user communications; compatibility/deprecation roadmap; benefits/outcome measurement; rollback; and retirement/exit obligations. Test access and failure recovery rather than accepting document presence. If high-consequence obligations lack owners or evidence, escalate, reduce launch scope, extend transition, or explicitly accept risk through authorized governance; calendar pressure does not discharge them.

### Answer 3

Mandate explains adoption and invalidates it as voluntary value evidence. Segment deployment lead time into platform wait, consumer work, review and execution; inspect failure/rework, incident types/blast radius, support queues, exceptions, bypasses, upgrade burden, cognitive load, availability and clean-room first-success journeys. Compare cohorts and pre-mandate baselines cautiously; interview representative users and nonusers. Determine whether platform added a bottleneck, standardized a defective process, centralized domain decisions, underfunded operations, or omitted escape paths. Correct by removing low-value gates, automating repeated evidence, restoring domain authority, funding support/reliability, publishing stable contracts, offering justified alternatives, and testing changes with guardrails. Do not target satisfaction or lead time alone: faster unsafe deployments and satisfied privileged users can hide harm.

### Answer 4

Define scheduling outcomes first: correct coverage, employee fairness/control, manager effort, labor-rule compliance, accessibility and continuity. Build offers semantic/control fit but requires product discovery, engineering, security, operations and long-term evolution. Buy may accelerate baseline capability but adds configuration, identity/data integration, supplier availability/security, pricing, roadmap, auditability, data portability and exit risks. Retire is viable if work can stop or move to an acceptable existing capability; include migration, records, contracts and user harm. Estimate ranges for acquisition/build, integration, training/change, operation, support, incidents, compliance, upgrades, consumer work, migration and exit. Run prototypes and supplier due diligence against hard scenarios. Choose the option with defensible outcome, risk and lifecycle economics—not the lowest first-year price—and assign durable product/service owners regardless of acquisition route.

### Answer 5

Product view identifies emergency coordinators, pilots, dispatchers, affected public and aviation authorities; outcomes include timely conflict-free routing without degrading responder autonomy or public safety. Service view defines authorization, availability, latency, correctness, continuity, support, incident command, degraded/manual mode and data handling. Platform view applies if shared identity, airspace data, telemetry, simulation or integration capabilities enable multiple agencies; domain flight/safety decisions stay with authorized owners. Projects may establish a pilot, regional migration or retirement. Assets include maps, rules, models, software, keys, logs, interfaces and certified configurations.

Use versioned requirements/hazards, traceable architecture, independent simulation/model and implementation evidence, security/privacy analysis, fault injection, capacity/latency and communications-loss tests, hardware/operator exercises, configuration and supplier controls, signed releases, staged deployment, rollback/manual fallback, incident learning and explicit transition acceptance. Counterexamples include stale airspace, conflicting authorities, spoofed location, clock drift, network partitions, sensor disagreement, overload, inaccessible controls and unsafe automation bias. Named aviation/regulatory authorities, emergency-service operations and pilots, air-traffic/safety engineers, human-factors/accessibility experts, security/privacy specialists, communications/platform/software engineers, affected-community representatives and independent safety assessors must review assumptions, hazards, evidence, operating authority and rollout. No simulated or automated evidence independently authorizes live flight operations.
