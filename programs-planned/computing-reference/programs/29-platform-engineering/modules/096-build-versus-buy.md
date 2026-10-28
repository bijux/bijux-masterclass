---
module_id: PLAT-096
program: Platform Engineering
level: 2
module_number: 96
title: Build Versus Buy
status: complete
last_verified: 2026-09-02
---

# Build Versus Buy

## One-Page Review

### Governing question

When should a platform capability be built internally, acquired as a managed product, adopted from open source, assembled from components, or deliberately not provided—and what evidence makes that choice reversible, secure and economically honest over its lifecycle?

### Essential definitions

- A **sourcing decision** selects who creates, operates, evolves and bears risk for a capability; “build versus buy” is shorthand for a spectrum, not a binary.
- **build** means the organization owns material product design, implementation, operation and evolution of the capability, even if it uses external components.
- **buy** means acquiring a commercial product or managed service under contractual rights and obligations; configuration and integration still remain organizational work.
- **adopt** means consuming and possibly contributing to an open-source project under its license and governance, without transferring outcome ownership to a vendor.
- **assemble** means composing internal, commercial and open components behind an owned platform contract.
- **differentiation** is capability-specific advantage that materially contributes to organizational strategy or user outcomes; uniqueness alone is not differentiation.
- **total cost of ownership** includes acquisition, people, integration, operation, support, assurance, change, migration, downtime, opportunity cost and retirement over a declared horizon.
- **switching cost** is the cost, delay, risk and lost capability incurred when changing a supplier, implementation or operating model.
- **exit readiness** is demonstrated ability to retrieve data, replace interfaces, transfer knowledge, revoke access and preserve service within a defined recovery objective.
- A **real option** preserves the right, but not obligation, to expand, replace or abandon an approach after bounded learning.

### Central model, mechanism, or theorem

For sourcing option $j$ over horizon $H$, let $A_j$ be acquisition cost, $L_j$ internal labor, $I_j$ integration, $O_j$ operation, $S_j$ support and assurance, $E_j$ expected loss from risk, and $X_j$ migration and exit cost, discounted by rate $r$:

$$
TCO_j(H)=A_j+\sum_{t=0}^{H}\frac{L_{j,t}+I_{j,t}+O_{j,t}+S_{j,t}+E_{j,t}}{(1+r)^t}+\frac{X_{j,H}}{(1+r)^H}.
$$

Cost is necessary but insufficient. A feasible option must satisfy capability fit, security, compliance, reliability, data rights, integration, operability and exit constraints. The lowest quoted price cannot be the best option when it fails a mandatory constraint or transfers unowned lifecycle work.

### Critical invariants

- The decision begins with an outcome and capability contract, not loyalty to a product, cloud, architecture or internal team.
- Every option is compared over the same horizon, demand scenarios, service boundary and fully loaded cost categories.
- Security, privacy, compliance, reliability, accessibility, data ownership, supply-chain provenance and operational responsibilities remain explicit before selection and throughout use.
- No supplier, maintainer or internal builder inherits the organization’s service-outcome accountability; escalation and failure ownership have named internal owners.
- Portability, data export, contractual termination, knowledge, fallback and retirement are designed and tested in proportion to switching consequence.
- The choice is reviewed when assumptions, scale, product fitness, supplier health, community health, risk, cost or strategy changes; sunk cost does not freeze it.

### Common failures

Treating the decision as binary; comparing license fee with engineer salary; calling internal labor free; buying before defining the problem; building for prestige; assuming managed means no operations; assuming open source means free or safe; customizing until upgrades become forks; accepting proprietary data without export tests; relying on procurement promises not contracts; ignoring egress, support and retirement; one proof of concept becoming permanent; counting vendor roadmap intent as committed capability; allowing one person to own integration knowledge; measuring nominal feature parity instead of critical journeys; and postponing exit design until failure.

### Compact example

A platform needs a policy-decision service. It defines latency, availability, audit, residency, integration, explainability and recovery contracts, then compares internal build, managed service and adopted open source over five demand scenarios. The managed quote is cheapest at current traffic, but private connectivity, evidence retention, premium support and egress double its fully loaded cost; its export cannot meet the exit recovery objective. Internal build offers control but consumes the only authorization specialists and delays higher-value identity work. An open implementation with paid support passes a bounded production trial, provides portable policy and decision logs, and keeps a replaceable adapter at the platform boundary. The team adopts and contributes upstream, contracts support, funds patch ownership, tests restore and export quarterly, and records triggers for managed reconsideration if scale and residency assumptions change.

### Connections

Build-versus-buy decisions consume platform discovery, contracts, reliability, cost, security, roadmap and support evidence from PLAT-001–095. Their supplier, interface, portability and exit choices determine capability lifecycle, outcome measurement, strategy defensibility, team autonomy and monopoly risk in PLAT-097–100.

## Governing Question

Which sourcing model best satisfies the platform outcome and non-negotiable constraints across plausible lifecycle scenarios, while preserving enough control, evidence and exit ability to change course responsibly?

The answer is rarely “build” or “buy” in isolation. A purchased control plane may run with internal adapters and operational automation. An open-source capability may depend on a commercial maintainer. An internally built user contract may delegate execution to several providers. The enduring design question is which responsibilities and risks the organization retains at each boundary.

Sourcing is therefore both a product decision and a systems decision. It determines opportunity cost, cognitive load, supply-chain exposure, incident control, negotiating leverage, evolution speed and the future set of available options.

## Why This Matters

Platform capabilities have unusually broad blast radius. A poor sourcing choice can place hundreds of services behind one unobservable contract, unsupported fork or untested vendor recovery path.

Quotes distort comparisons. Commercial prices omit integration, assurance, usage growth, support tiers and exit. Build estimates omit recruiting, interruption, on-call, documentation and opportunity cost. Open-source estimates omit evaluation, patching, governance and contribution. A common boundary and horizon are required for honest comparison.

Time matters. Buying can accelerate learning when the capability is understood and the product fits. It can also accelerate lock-in before the organization understands its requirements. Building can preserve control over a differentiating contract, or spend scarce specialists recreating commodity behavior.

External provision changes, but does not remove, accountability. Suppliers can miss objectives, communities can lose maintainers, licenses can change, acquisitions can alter direction and regions can fail. Internal owners still need evidence, escalation, fallback and user communication.

Exit is part of entry. Data formats, identity, network topology, workflow semantics and custom extensions can make a nominally replaceable product practically permanent. Testing portability early creates leverage and reveals whether reversibility is real.

## Prerequisites and Retrieval

Retrieve the platform strategy and roadmap; affected users and critical journeys; capability and interface requirements; current alternatives and pain evidence; workload demand, seasonality and growth scenarios; availability, latency, recovery and support objectives; data classification, residency and retention; threat model and compliance obligations; internal skills, hiring lead time and opportunity cost; architecture and dependency inventory; vendor proposals, contracts, pricing dimensions, service objectives and financial health; open-source licenses, releases, contributors, maintainers, security policy and governance; integration and migration estimates; incident and vulnerability history; unit economics; procurement and legal constraints; exit clauses, export formats and deletion evidence; and decision history.

Distinguish outcome from solution; capability from product; commodity from low consequence; differentiation from uniqueness; build from own-every-dependency; buy from outsource-accountability; open source from public repository; license from total cost; price discount from economic fitness; SLA from observed reliability; vendor roadmap from contractual commitment; configuration from customization; extension from fork; data export from usable portability; backup from recoverability; termination right from executable exit; reversible pilot from permanent precedent; sunk cost from future value; and supplier concentration from architecture concentration.

## Learning Objectives

After completing this module, you should be able to:

1. define an outcome-oriented capability contract before evaluating sourcing options;
2. generate build, buy, adopt, assemble, partner and do-nothing alternatives without false binaries;
3. compare options using common lifecycle boundaries, scenarios and fully loaded cost;
4. evaluate product, integration, operability, security, compliance and supply-chain fitness;
5. test vendor claims and open-source health with reproducible technical and governance evidence;
6. allocate ownership across internal teams, suppliers, maintainers and incident responders;
7. design stable platform interfaces that contain provider-specific coupling;
8. negotiate data, evidence, support, change, termination and portability rights;
9. run bounded trials with explicit success, stop and transition criteria; and
10. review sourcing choices using outcome, risk, cost, concentration and exit-readiness signals.

## Core Exposition

### Define the outcome and non-goals

Start with the user or service outcome, current baseline and consequence of doing nothing. State which parts of the journey the platform will own.

Describe non-goals so adjacent products do not win by offering irrelevant breadth. A policy service may need decision evaluation and evidence, not a complete application-development suite.

Set guardrails for reliability, security, accessibility, cost, support and team health. Sourcing is subordinate to these outcomes and constraints.

### Specify a capability contract

Define functional behavior, interfaces, workload, lifecycle, performance, availability, recovery, audit, data, identity, support, observability and retirement requirements.

Separate mandatory constraints from weighted preferences. A residency law cannot be traded for a dashboard score; a convenient user interface can.

Use critical journeys and failure modes rather than a long checkbox list. Nominal feature presence says little about safe operation.

### Generate the real option set

Consider build, commercial software, managed service, open-source adoption, supported open source, assembly, partnership, reuse from elsewhere and no capability.

Hybrid options are normal. Own the user contract and adapters while using external execution; buy a control plane but build recovery automation; adopt an open core with commercial support.

Avoid a fake shortlist constructed to justify a preferred product. Record exclusion reasons and missing evidence.

### Establish decision authority

Name product, architecture, security, privacy, legal, finance, procurement, operations and consuming-user roles. Clarify who advises, who vetoes mandatory failures and who accepts residual risk.

Prevent the builder, buyer or vendor from being sole evaluator of its preferred option. Include users and operators who bear downstream cost.

Record dissent and decision conditions. Consensus language should not erase material uncertainty.

### Choose horizon and scenarios

Evaluate a common horizon covering entry, growth, operation, at least one major change and exit. Short horizons systematically favor low entry prices.

Model current, expected, high-growth, degraded-supplier and exit scenarios. Include demand shape, regions, data, availability and support tiers.

Use sensitivity ranges rather than one forecast. Identify which assumption changes the ranking.

### Compute total cost of ownership

Include licensing or subscription, consumption, network and egress, integration, customization, platform labor, security review, compliance evidence, monitoring, support, incident response, training, migration and retirement.

Value internal labor at its real opportunity cost. Scarce engineers assigned to commodity reconstruction cannot deliver other roadmap outcomes.

Include expected loss carefully: probability ranges, consequence and mitigations. Do not pretend uncertain tail risk is a precise invoice.

### Measure unit economics

Select a unit connected to platform value, such as eligible deployment, protected workload or successful recovery evidence. Show fixed and variable cost behavior.

Vendor tier cliffs, minimum commitments and burst pricing matter. Internal platforms also have step costs, idle capacity and support scale effects.

Pair unit cost with outcome and guardrails. Cheap failed journeys are not efficient.

### Evaluate functional and experiential fit

Run representative critical journeys, policy cases, scale and accessibility tests. Observe users rather than accepting demonstrations.

Separate native capability, configuration, extension, customization and promised roadmap. Assign cost and upgrade risk to each gap.

Prefer the smallest fit that sustains the outcome. Unused feature breadth increases surface, cognitive load and commercial leverage.

### Evaluate architecture and integration

Inspect APIs, events, identity, tenancy, networking, data models, rate limits, versioning, observability and failure semantics.

Measure integration through a production-shaped slice. Slideware compatibility does not expose retries, backpressure, partial failure or identity edges.

Contain provider details behind an owned contract where replacement value justifies abstraction. Avoid lowest-common-denominator layers that erase useful capability.

### Evaluate reliability and operations

Compare service objectives with architecture, observed evidence, exclusions and compensation. An SLA credit does not restore user outcomes.

Define monitoring, incident command, paging, status, vendor escalation, maintenance, capacity and recovery ownership. Test an after-hours escalation before production.

Model correlated failures. Several “independent” products may depend on one cloud, identity provider, package registry or support organization.

### Evaluate security and privacy

Assess secure development, provenance, vulnerability handling, access control, tenant isolation, encryption, logging, incident notification and data deletion.

Request evidence proportional to consequence: attestations, audit scope, penetration results, SBOM, build provenance, patch objectives and subprocessor inventory.

Validate evidence rather than collecting documents. Map gaps to controls, owners, deadlines and residual-risk acceptance.

### Evaluate supply-chain health

For vendors, inspect ownership, financial viability, product investment, support staffing, acquisition history, subcontractors and concentration.

For open source, inspect maintainer diversity, release and review practice, security policy, responsiveness, governance, license and funding. Popularity is not health.

For internal build, inspect bus factor, recruiting, review independence, patch process and long-term product ownership. Internal supply chains can be fragile too.

### Inspect commercial and legal terms

Translate requirements into contract language: data ownership, security evidence, notification, audit, service levels, support, price changes, roadmap representations, termination, transition help and deletion.

Check order-of-precedence across proposal, master agreement and service schedules. A salesperson’s promise is not enforceable by memory.

Avoid commitments that destroy leverage before the trial proves fitness. Model renewal, true-up and termination dates.

### Design portability and exit

Define what must move: data, configuration, policy, identity links, logs, keys, workflows, knowledge and operating procedures.

Require documented, versioned export in usable formats and test import into a neutral or alternate path. An archive that cannot recreate behavior is not portability.

Set exit recovery and data-deletion objectives, capacity, trigger, authority and communication. Fund the minimum continuing readiness.

### Govern customization

Classify gaps as configuration, supported extension, adapter, vendor change or fork. Each has different upgrade and ownership cost.

Budget customizations across every upgrade. Require an owner and removal or upstream path.

Reject unique behavior that does not contribute to outcomes. If deep customization is essential, compare honest assembly or build alternatives.

### Run a bounded trial

Use production-shaped journeys, data classes, integrations, failure injection, operations and exit—not only a happy-path demo.

Predefine success, guardrail, stop, time, cost and transition criteria. Limit irreversible data and coupling.

Keep trials out of indefinite preview. The decision at the end is adopt, extend learning with new evidence, or retire safely.

### Make the decision auditable

Record options, common boundary, assumptions, evidence, TCO ranges, mandatory gates, sensitivity, residual risks, dissent, decision and review triggers.

Do not hide judgment behind a weighted score. Explain why the selected responsibility allocation best fits the outcome.

Set an expiry or review event. Decisions remain correct only while their premises hold.

### Plan implementation and ownership

Name platform product, integration, operating, security, procurement and supplier owners. Publish escalation and service boundaries to consumers.

Budget migration, documentation, support, reliability and retirement from the beginning. Acquisition completion is not capability completion.

Protect consuming teams from provider semantics where practical, but expose constraints they must understand.

### Monitor realized outcomes

Compare actual cost, usage, reliability, support, security, journey and integration evidence with the decision case. Segment by cohort and scale.

Track vendor and community change, vulnerabilities, pricing, roadmap gaps, concentration and contract dates.

Measure internal work transferred to consumers. A lower central cost can represent exported toil.

### Trigger review, replacement or exit

Review on outcome failure, guardrail breach, price or license change, acquisition, maintainer loss, repeated incident, control gap, scale shift or strategy change.

Use sunk cost only to understand transition consequence, never to justify future spend. Compare prospective alternatives from the current state.

Exercise exit before urgency. A failed portability test becomes owned roadmap work, not a reason to pretend the dependency is permanent.

## Definitions and Notation

Let $J$ be sourcing options and $H$ the evaluation horizon. For option $j$, define acquisition $A_j$ and time-indexed labor $L_{j,t}$, integration $I_{j,t}$, operation $O_{j,t}$, support/assurance $S_{j,t}$, expected loss $E_{j,t}$ and terminal exit $X_{j,H}$.

$$
TCO_j(H)=A_j+\sum_{t=0}^{H}\frac{L_{j,t}+I_{j,t}+O_{j,t}+S_{j,t}+E_{j,t}}{(1+r)^t}+\frac{X_{j,H}}{(1+r)^H}.
$$

Let $m_{j,k}\in\{0,1\}$ indicate whether option $j$ satisfies mandatory constraint $k$, so feasibility requires $\prod_k m_{j,k}=1$. Let $u_{j,s}$ be total cost in scenario $s$, $p_s$ a declared scenario weight and $Q_j$ a qualitative consequence vector that cannot responsibly be reduced to money.

For critical exit assets $a\in A$, let $e_{j,a}$ be verified export, $i_{j,a}$ verified import or reconstruction, and $d_{j,a}$ verified deletion where applicable. Exit readiness requires the selected checks for every critical asset within the declared recovery objective; a contractual right without executed evidence is not readiness.

## Mechanisms, Invariants, or Proof Structure

### Twelve-step sourcing mechanism

1. Define outcome, non-goals, users, baseline and consequence of no action.
2. Specify capability, operational, data, security, lifecycle and exit contracts.
3. Generate build, buy, adopt, assemble, partner, reuse and do-nothing options.
4. Set decision authority, mandatory gates, common horizon and demand scenarios.
5. Collect reproducible product, architecture, reliability and user-fit evidence.
6. Assess vendor, open-source and internal supply-chain health and concentration.
7. Compute fully loaded TCO, unit economics, opportunity cost and sensitivity.
8. Negotiate rights and design stable interfaces, portability, fallback and exit.
9. Run a bounded production-shaped trial with success, guardrail and stop criteria.
10. Record the decision, residual risk, ownership, assumptions and review triggers.
11. Operate and compare realized outcomes, costs, incidents and changes to the case.
12. Reassess, renegotiate, replace, internalize, externalize or exit when triggers fire.

### Outcome invariant

Every option is evaluated against the same outcome, critical journeys, service boundary and non-goals; a product cannot redefine the problem to win.

### Economic invariant

Comparisons use the same horizon and scenarios and include internal labor, opportunity, integration, operation, assurance, failure, migration and exit costs.

### Assurance invariant

Mandatory security, privacy, compliance, reliability, accessibility and data constraints are verified with proportionate evidence rather than offset by weighted preferences.

### Accountability invariant

Internal product and service owners remain accountable through supplier, maintainer, contractor and component boundaries, including incidents and retirement.

### Reversibility invariant

Critical data, interfaces, knowledge, access and operating behavior have tested transition paths proportional to switching consequence.

### Adaptation invariant

Outcome, scale, cost, risk, supplier/community health and strategy changes can reopen the decision; prior acquisition or development cost cannot veto review.

### Proof sketch: lowest purchase price cannot establish lowest lifecycle cost

Construct two options with the same required outcome. Option A has zero license price but requires integration, specialist operations, premium support and a costly proprietary-data exit. Option B has a positive license price but includes those services and a tested portable export. A can have the lower purchase price and the higher TCO. Therefore purchase price alone is insufficient to establish economic preference; a common lifecycle boundary is necessary.

### Executable sourcing gate

This synthetic audit compares three options on five-year undiscounted cost and mandatory gates. It illustrates consistent arithmetic and rejection of an infeasible cheap quote, not a universal decision formula.

<!-- bijux-verify: {"id":"sourcing-feasibility-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"options=3\nfeasible=2\nbuild_tco=1140\nbuy_tco=940\nadopt_tco=770\nlowest_quote=buy\nlowest_feasible_tco=adopt\nexit_ready=2/3\ngate=pass\n"}} -->
```python
options = {
    "build": {"quote": 300, "costs": [120, 260, 220, 160, 80], "gates": [1, 1, 1]},
    "buy": {"quote": 20, "costs": [120, 140, 160, 180, 320], "gates": [1, 1, 0]},
    "adopt": {"quote": 40, "costs": [190, 160, 140, 130, 110], "gates": [1, 1, 1]},
}
totals = {name: item["quote"] + sum(item["costs"]) for name, item in options.items()}
feasible = {name for name, item in options.items() if all(item["gates"])}
lowest_quote = min(options, key=lambda name: options[name]["quote"])
lowest_feasible = min(feasible, key=totals.get)

print(f"options={len(options)}")
print(f"feasible={len(feasible)}")
for name in options:
    print(f"{name}_tco={totals[name]}")
print(f"lowest_quote={lowest_quote}")
print(f"lowest_feasible_tco={lowest_feasible}")
print(f"exit_ready={sum(item['gates'][-1] for item in options.values())}/{len(options)}")
print(f"gate={'pass' if lowest_feasible == 'adopt' else 'fail'}")
```

### Verification strategy

Trace requirements to user and service evidence; reproduce trials from clean environments; recompute cost scenarios and sensitivity; inspect contracts against proposal claims; validate license and provenance; sample vulnerability response; exercise monitoring and vendor escalation; fail dependencies; test representative scale and accessibility; export, reconstruct and delete critical assets; audit customization and forks; compare realized unit cost and support load; verify current maintainers and internal owners; and rehearse transition without relying on the team or supplier being replaced.

## Alternatives and Trade-Offs

1. Internal build maximizes direct control but consumes scarce product, security and operating capacity.
2. Managed services accelerate entry but create provider, pricing, data and incident dependencies.
3. Commercial self-hosted products retain runtime control but leave upgrade and integration work internally.
4. Open-source adoption improves inspection and portability but requires funded ownership and governance attention.
5. Commercially supported open source adds escalation but can blur community and proprietary boundaries.
6. Assembly fits local contracts but multiplies integration, compatibility and incident surfaces.
7. Strategic partnership shares expertise but creates joint-governance and continuity risk.
8. Reuse from another internal team is fast but may import an unfunded, local contract.
9. Broad suites reduce procurement count but expand coupling and unused surface.
10. Best-of-breed products improve specialized fit but increase integration and vendor count.
11. Provider abstraction enables replacement but can suppress valuable native features.
12. Native integration accelerates value but raises switching cost.
13. Long contracts improve price predictability but reduce leverage under changing needs.
14. Short contracts preserve options but can increase price and renewal workload.
15. Deep customization closes immediate gaps but turns upgrades into internally owned development.
16. Upstream contribution reduces fork cost but follows community timelines and governance.
17. Redundant providers reduce some outages but multiply consistency, cost and operational complexity.
18. Doing nothing preserves capacity but leaves the existing problem and risk explicitly accepted.

## Failure Modes and Misconceptions

1. “Build versus buy is binary” ignores adoption, assembly and no action.
2. “Commodity means low risk” confuses prevalence with consequence.
3. “Strategic means build it” may confuse importance with differentiation.
4. “Unique means differentiating” rewards accidental complexity.
5. “Buying transfers accountability” leaves user outcomes internally owned.
6. “Managed means zero operations” ignores integration, incidents and governance.
7. “Open source is free” ignores ownership, assurance and support.
8. “Public code is healthy” ignores maintenance and governance.
9. “Internal code is trustworthy” ignores provenance and bus factor.
10. “The quote is the cost” omits the lifecycle boundary.
11. “Engineer salary is build cost” omits opportunity and operations.
12. “A discount proves value” may hide commitment and tier cliffs.
13. “Feature count proves fit” ignores critical journeys and failure behavior.
14. “A demo proves integration” omits production identity and degradation.
15. “The vendor roadmap is a commitment” mistakes intent for contract.
16. “An SLA guarantees reliability” confuses credits with restored outcomes.
17. “Compliance certification covers our use” ignores scope and configuration.
18. “An SBOM proves secure software” confuses inventory evidence with assurance.
19. “One cloud account means one dependency” misses shared control planes.
20. “Configuration is harmless” may create untested state and upgrade coupling.
21. “Forking gives control” creates full maintenance responsibility.
22. “Abstraction always prevents lock-in” can move lock-in into the abstraction.
23. “Data export proves portability” ignores semantics and reconstruction.
24. “A termination clause is an exit plan” omits execution and capacity.
25. “A pilot is reversible” may already contain durable data and identity coupling.
26. “Procurement completion is delivery” ignores integration and adoption.
27. “Current scale determines the choice” ignores growth and contraction.
28. “Past investment justifies renewal” mistakes sunk cost for future value.
29. “Multivendor always improves resilience” can add common dependencies.
30. “Once chosen, sourcing is settled” ignores changing premises.

## Worked Examples

### Example 1

A team compares a license quote with two engineer salaries. Adding on-call, integration, assurance, usage growth and exit reverses the apparent preference.

### Example 2

A managed database meets availability claims but cannot export encryption metadata within the exit objective. It fails a mandatory gate despite the lowest price.

### Example 3

An open project has many stars but one active maintainer and no disclosure process. The platform funds a supported alternative and limits adoption pending governance evidence.

### Example 4

An internal scheduler is called strategic. Research shows its behavior is standard and users value faster diagnosis, so specialists move to the owned diagnostic contract.

### Example 5

A commercial product needs twelve unsupported customizations. An assembled option with stable adapters has higher entry cost but lower upgrade and switching risk.

### Example 6

A vendor meets its SLA by issuing credits during an outage. Internal incident command still owns communication, workaround and recovery verification.

### Example 7

A proof of concept copies production data and becomes indispensable. New trial policy requires data limits, expiry, transition owner and rehearsed deletion before entry.

### Example 8

Two vendors run on the same identity and cloud control plane. Dependency mapping rejects the claim that vendor count alone supplies resilience.

### Example 9

A license changes after acquisition. A tested export, provider adapter and renewal trigger let the organization compare prospective options without panic.

### Example 10

A platform retires an internal build for a managed service but retains the user contract, audit data and migration tooling. Consumers change implementation without rewriting journeys.

## Cross-Program Connections

- Product Management contributes outcome framing, discovery, trials and product-market evidence.
- Finance contributes discounting, unit economics, scenario analysis and opportunity cost.
- Software Architecture contributes boundaries, coupling, adapters, data models and reversibility.
- Security Engineering contributes threat models, secure development and supply-chain assurance.
- Site Reliability Engineering contributes objectives, incidents, recovery and dependency analysis.
- Procurement contributes competition, due diligence, contractual rights and renewal governance.
- Legal and Privacy contribute licenses, data rights, subprocessors, residency and deletion duties.
- Open-Source Governance contributes project health, contribution, licensing and maintainer relations.
- Systems Engineering contributes lifecycle, trade studies, sensitivity and emergent concentration risk.
- Organizational Design contributes ownership, cognitive load, skill scarcity and bus-factor analysis.

## References

1. CNCF TAG App Delivery. [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/). Retrieved 2026-09-02.
2. CNCF TAG App Delivery. [Platform Engineering Maturity Model](https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/). Retrieved 2026-09-02.
3. DORA. [Platform Engineering](https://dora.dev/capabilities/platform-engineering/). Retrieved 2026-09-02.
4. NIST. [Cybersecurity Supply Chain Risk Management Practices for Systems and Organizations](https://csrc.nist.gov/pubs/sp/800/161/r1/upd1/final). Retrieved 2026-09-02.
5. NIST. [Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final). Retrieved 2026-09-02.
6. NIST. [Software Security in Supply Chains](https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity/software-supply-chain-security-guidance-13). Retrieved 2026-09-02.
7. NIST. [Software Cybersecurity for Producers and Purchasers](https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity/software-supply-chain-security-guidance-7). Retrieved 2026-09-02.
8. CISA. [Secure by Demand Guide](https://www.cisa.gov/resources-tools/resources/secure-demand-guide). Retrieved 2026-09-02.
9. CISA. [Software Acquisition Guide for Government Enterprise Consumers](https://www.cisa.gov/sites/default/files/2024-07/PDM24050%20Software%20Acquisition%20Guide%20for%20Government%20Enterprise%20ConsumersV2_508c.pdf). Retrieved 2026-09-02.
10. SLSA. [SLSA Specification](https://slsa.dev/spec/v1.2/). Retrieved 2026-09-02.
11. OpenSSF. [OpenSSF Scorecard](https://scorecard.dev/). Retrieved 2026-09-02.
12. FinOps Foundation. [FinOps Framework](https://www.finops.org/framework/). Retrieved 2026-09-02.
13. FinOps Foundation. [Unit Economics](https://www.finops.org/framework/capabilities/unit-economics/). Retrieved 2026-09-02.
14. Google SRE. [Service Best Practices](https://sre.google/sre-book/service-best-practices/). Retrieved 2026-09-02.
15. Google SRE. [Reliable Product Launches at Scale](https://sre.google/sre-book/reliable-product-launches/). Retrieved 2026-09-02.

## Exercises

### Exercise 1

Define a sourcing contract and option set for a platform secrets capability used by regulated and non-regulated services.

### Exercise 2

Option A costs 100 to acquire and 180 annually for three years, with exit cost 200. Option B costs 300 to acquire and 100 annually, with exit cost 50. At zero discount, compare TCO and state what the arithmetic omits.

### Exercise 3

A vendor is cheapest and passes every feature test but cannot provide usable audit export or a tested severity-one escalation. Design the decision response.

### Exercise 4

An open-source capability has been customized in a private fork for two years. Design a recovery path that restores upgrade and sourcing options.

### Exercise 5

Create review triggers and an exit exercise for a managed platform capability whose usage will grow tenfold.

## Answers to the Exercises

### Answer 1

Define secret creation, rotation, retrieval, revocation, audit and recovery journeys; identity and authorization; latency and availability; residency and encryption; break-glass; tenant isolation; evidence retention; support; migration and deletion. Mark regulatory control and recovery constraints mandatory, and segment demand and consequence.

Compare internal build, cloud-managed, commercial self-hosted, supported open source, assembly behind an owned API and improvement of the current path. Include key custody, network dependency, operator access, secure-development evidence, incident notification, per-secret/request economics, internal skill, import/export and retirement. Trial representative failures and rotation, not only retrieval.

### Answer 2

At zero discount, $TCO_A=100+3(180)+200=840$. For B, $TCO_B=300+3(100)+50=650$. B is lower by 190 under these inputs.

The calculation omits demand growth, internal integration and operations, assurance, opportunity cost, failure consequence, price tiers, tax, support, skill constraints, reliability, data rights and whether exit is executable. It also assumes equal outcomes and feasible mandatory constraints. Those must be evaluated before economic preference.

### Answer 3

Treat audit export and severity-one escalation as mandatory if required by the capability contract. The option is infeasible; do not compensate with feature or price scores. Give the supplier a bounded opportunity to demonstrate contract terms and production-shaped evidence, not a roadmap promise.

In parallel, evaluate an adapter or independent audit path only if it genuinely satisfies evidence and recovery needs without creating excessive risk. Compare other options, record the rejection and sensitivity, and preserve the outcome schedule rather than forcing a preselected product through assurance.

### Answer 4

Inventory fork differences, owners, consumers, data, interfaces, vulnerabilities and upgrade blockers. Classify each change as obsolete, configurable, generally useful, local adapter or irreducibly differentiating. Remove obsolete changes; move local integration behind an owned boundary; propose general changes upstream; and negotiate maintainership or support where justified.

Build automated conformance and migration tests, then advance through supported releases in bounded increments. Maintain fallback and incident ownership. Set a deadline and capacity for eliminating the private fork, while separately evaluating a replacement if upstream fitness or governance remains inadequate.

### Answer 5

Trigger review on volume and spend thresholds, price-tier crossing, latency or error guardrail breach, material incident, provider acquisition, region or subprocessor change, audit failure, export regression and renewal lead time. Model current, tenfold and burst scenarios including egress, support and rate limits.

Quarterly, export representative configuration, policy, audit and operational data; verify integrity; reconstruct critical behavior in an isolated alternate environment; measure recovery time; revoke access; and confirm deletion evidence for disposable test data. Assign owners and remediation dates. Run a fuller transition rehearsal before commitment or renewal, and keep sufficient documentation, adapter tests and qualified capacity to make exit credible.
