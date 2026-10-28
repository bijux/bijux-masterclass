---
module_id: DARCH-091
program: Data Architecture Engineering
level: 2
module_number: 91
title: Assessing Data Architecture Maturity
status: complete
last_verified: 2026-09-03
---

# Assessing Data Architecture Maturity

## One-Page Review

### Governing question

How can an organization assess the maturity of its data architecture as a contextual, evidence-backed capability profile that guides investment and risk reduction—without reducing diverse domains to one vanity score, confusing documentation with operation, or treating maximum maturity as the universal target?

### Essential definitions

- **Data architecture maturity** is the demonstrated capability, institutionalization, effectiveness, adaptability, and lifecycle control of named data-architecture practices for a defined scope, context, outcome, and time.
- A **maturity assessment** is a governed inquiry that compares scoped evidence with explicit capability descriptors and records ratings, confidence, exceptions, implications, and improvement choices.
- A **capability domain** is a coherent area being assessed, such as strategy alignment, semantic ownership, product contracts, platform services, integration, metadata, governance, security, quality, operations, evolution, or retirement.
- An **assessment unit** is the bounded organization, portfolio, domain, product, platform, value stream, jurisdiction, or architecture surface to which a finding applies.
- A **maturity profile** is the vector or matrix of capability findings across units and contexts. It preserves unevenness instead of collapsing it into one average.
- A **descriptor** states observable conditions associated with a capability level; it is not a vague adjective such as advanced or world-class.
- An **evidence claim** connects a descriptor to identified artifacts, observations, samples, people, configurations, versions, dates, and limitations.
- **Institutionalization** is the degree to which a capability has accountable ownership, resources, repeatable execution, controls, learning, and resilience beyond individual heroics.
- **Effectiveness** is the demonstrated contribution of a capability to intended user, operational, risk, compliance, or economic outcomes.
- **Coverage** is the bounded proportion of in-scope units, data, workloads, consumers, controls, or time for which evidence applies.
- **Confidence** is an explicit judgment about evidence sufficiency, independence, consistency, recency, and representativeness; it is not the maturity rating itself.
- A **target profile** declares the capability level and evidence needed for each scope according to outcomes, criticality, risk, cost, dependencies, and horizon.
- A **material gap** is a difference between current and target capability that threatens an outcome or constraint enough to justify intervention.
- An **assessment receipt** preserves scope, model version, participants, evidence, sampling, ratings, confidence, disagreements, decisions, owners, and reassessment triggers.
- **Closure** retires stale questionnaires, evidence copies, dashboards, access, exceptions, findings, actions, and assessment machinery while preserving required history and preventing obsolete ratings from governing current decisions.

### Central model, mechanism, or theorem

Represent an assessment as:

`M = (U, S, C, D, E, I, O, R, T, L)`

where `U` is users, decisions, and outcomes; `S` scope and context; `C` capability domains and descriptors; `D` dependencies and architecture topology; `E` evidence, sampling, coverage, and confidence; `I` institutionalization and execution; `O` observed performance and outcomes; `R` risk, criticality, and uncertainty; `T` target profiles, interventions, and reassessment; and `L` lifecycle and closure. A finding is valid only for its named unit, capability, descriptor, evidence window, context, assessor, and limitations. The assessment yields a profile and decision record, not an intrinsic scalar property of the enterprise.

### Critical invariants

- Assessment, model, version, capability, descriptor, unit, evidence, sample, claim, assessor, rating, confidence, exception, action, decision, and retirement have distinct stable identities.
- Purpose, scope, decision authority, affected stakeholders, model version, reference date, and intended use are fixed before evidence collection.
- Architecture design, implementation, adoption, operational performance, outcome, resilience, and closure are assessed separately.
- A policy, diagram, catalog entry, tool license, interview, dashboard, or isolated success cannot alone establish sustained capability.
- Each rating cites evidence, coverage, recency, exceptions, contradictory observations, confidence, and assessor rationale.
- Missing evidence remains unknown; it is not converted into the lowest level, a neutral midpoint, or evidence of absence without justification.
- Ratings are ordinal unless a model explicitly establishes stronger measurement properties; averages do not create interval-scale meaning.
- Enterprise aggregation never erases critical weak units, harmful variance, dependency bottlenecks, or minority stakeholder effects.
- Target maturity varies by outcome, criticality, risk, domain, workload, obligation, and horizon; highest everywhere is not the objective.
- Improvement actions trace from material gaps to mechanisms, owners, resources, evidence, outcome hypotheses, stop rules, and reassessment.
- Reassessment uses comparable definitions and evidence while preserving legitimate model, scope, and context change.
- Closure prevents obsolete ratings, exported evidence, dashboards, access, or restored assessment systems from controlling current decisions.

### Common failures

Common failures include buying a questionnaire before defining the decision; rating the entire enterprise as one unit; treating a maturity model as universally normative; assessing ambition instead of observed behavior; counting documents rather than their use; equating tool purchase with capability; using interviews as the only evidence; hiding missing evidence in averages; assigning decimal scores to ordinal descriptors; letting assessors rate their own incentives without challenge; selecting only showcase domains; averaging away a critical control failure; setting the highest level as every target; benchmarking organizations with different context; turning gaps into a generic transformation backlog; measuring action completion rather than changed capability and outcomes; repeating surveys without preserving evidence comparability; and retaining stale scores after architecture, regulation, ownership, or platforms change.

### Compact example

Ten invented capability findings are checked against six evidence gates. Four are substantiated; one each lacks an owner, a testable descriptor, an identified artifact, a runtime sample, current evidence, or an outcome link. The program also counts eight capability domains, five assessment scopes, five evidence kinds, ten assessment receipts, and ten decisions. It verifies declarations and counts only—not actual maturity, descriptor validity, evidence truth, target fitness, causal improvement, or organizational value.

### Connections

[DARCH-001](001-data-architecture-as-structure-flow-ownership-and-policy.md), [DARCH-002](002-business-strategy-and-data-outcomes.md), [DARCH-003](003-current-state-data-landscape.md), [DARCH-007](007-architecture-drivers-and-constraints.md), [DARCH-008](008-data-risk-and-criticality.md), [DARCH-009](009-architecture-views-and-stakeholders.md), [DARCH-010](010-writing-a-data-architecture-charter.md), [DARCH-021](021-business-capabilities-and-data-domains.md), [DARCH-070](070-connecting-technical-metadata-to-business-meaning.md), [DARCH-080](080-embedding-governance-into-data-flows-and-products.md), and [DARCH-090](090-evaluating-mesh-fabric-warehouse-and-hybrid-options.md) establish scope, evidence, topology, governance, and alternatives. [DARCH-092](../ROADMAP.md) next defines target-state architecture.

## Governing Question

An organization can answer hundreds of maturity questions, calculate a number to two decimal places, color a dashboard, and still know little about whether its data architecture helps a clinician, regulator, operator, scientist, customer, or product team make a better decision. One business unit may have excellent semantic ownership and weak recovery. A shared platform may have strong automation but poor adoption. A critical product may satisfy every policy on paper while runtime access bypasses enforcement. An enterprise average makes these conditions less visible.

The governing question is not “What level are we?” It is “Which capabilities, in which units and contexts, are sufficiently demonstrated for the outcomes and risks we own; where is evidence weak or contradictory; what target is warranted; and which intervention is most likely to improve the result?” A useful assessment is a decision instrument. It creates a defensible profile, directs scarce capacity toward material gaps, preserves uncertainty and dissent, and establishes how changed capability will be verified.

## Why This Matters

The UK Government's [Data Maturity Assessment for Government framework](https://www.gov.uk/government/publications/data-maturity-assessment-for-government-framework/data-maturity-assessment-for-government-framework-html) defines maturity as capability, effectiveness, and readiness to use data. It organizes ten topics across six themes and explicitly presents a matrix rather than a single score. It also warns that implementation can yield a deep or shallow, wide or narrow view. This supports profile-based assessment and careful scoping.

The accompanying [delivery objectives and resources](https://www.gov.uk/government/publications/delivering-a-data-maturity-assessment-objectives-and-resources) cover understanding, initiating, delivering, recording, and acting on an assessment. They reinforce that the assessment must be planned and actioned, but a government framework still requires tailoring to an organization's architecture decisions, obligations, and evidence.

The EDM Association's [DCAM framework](https://edmcouncil.org/frameworks/dcam/) describes capabilities, sub-capabilities, objectives, challenge questions, evidence artifacts, and scoring criteria. It distinguishes engagement, process, and evidence in assessment. The detailed framework is member-controlled, and claims on its public page are framework-provider claims; adoption or a score does not by itself establish local effectiveness.

The CMMI Institute's [Data Management Maturity model FAQ](https://stage.cmmiinstitute.com/getattachment/b1ec339f-7d79-4056-af31-8cfd9b03eaf7/attachment.aspx) presents a reference model for assessing data-management practices and developing improvement roadmaps aligned with business goals. It illustrates capability-oriented assessment. Its broad benefit claims remain contextual and cannot substitute for local causal or outcome evidence.

The OECD report [The Path to Becoming a Data-Driven Public Sector](https://www.oecd.org/content/dam/oecd/en/publications/reports/2019/11/the-path-to-becoming-a-data-driven-public-sector_9ed7e867/059814a7-en.pdf) connects leadership, rules, architecture, infrastructure, sharing, public value, ethics, privacy, security, and trust. It explicitly describes its framework as non-prescriptive rather than one-size-fits-all. This supports maturity targets derived from context and outcomes.

NIST's [CSF 2.0 guide for using tiers](https://www.nist.gov/publications/nist-cybersecurity-framework-20-quick-start-guide-using-csf-tiers) applies tiers to organizational profiles to characterize rigor in cybersecurity risk governance and management outcomes and monitor improvement. Security evidence should inform a data-architecture profile, but cybersecurity tiers are not a substitute for data semantics, quality, platform, interoperability, or lifecycle assessment.

NIST's [Privacy Framework 1.1](https://www.nist.gov/privacy-framework/using-privacy-framework-11) uses core outcomes, profiles, and implementation tiers for privacy-risk management. It shows why current and target states should be risk-informed. A mature architecture cannot treat privacy as a survey item isolated from actual collection, joining, access, retention, and deletion behavior.

W3C's [Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/) models quality measurements, metrics, dimensions, policies, annotations, and provenance. It provides a way to identify what was measured and how. A quality assertion still needs a relevant population, method, time, threshold, and consumer consequence.

OpenLineage's [object model](https://openlineage.io/docs/spec/object-model/) represents datasets, jobs, runs, events, namespaces, names, and facets. Runtime lineage can substantiate architecture execution and coverage, while absent instrumentation, inconsistent identity, or stale integrations must remain visible as evidence gaps.

The Bitol [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/) includes schema, quality, service, roles, support, and infrastructure sections. Contracts provide assessable artifacts across product and platform boundaries. Publication is design evidence; operational conformance, consumer use, and change behavior need separate evidence.

The Open Policy Agent [policy language documentation](https://www.openpolicyagent.org/docs/policy-language) describes decisions over structured inputs using Rego. Policy tests and decision logs can provide computational-governance evidence, provided authoritative inputs, enforcement points, coverage, exceptions, and outcomes are verified.

The OpenTelemetry [specification](https://opentelemetry.io/docs/specs/otel/) standardizes concepts and signals for telemetry. Comparable operational evidence depends on resource identity, semantic conventions, instrumentation coverage, sampling, versions, and retention; the presence of a collector is not evidence of useful observation.

The FinOps Foundation's [FinOps Framework](https://www.finops.org/framework/) connects engineering, finance, business, leadership, procurement, product, security, and sustainability with usage, cost, value, optimization, and governance capabilities. Data architecture maturity therefore includes accountable economics and value evidence, not merely technical sophistication.

Google's SRE book chapter [Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) distinguishes symptoms from causes and discusses latency, traffic, errors, saturation, precision, and actionability. Architecture operations should be assessed through consumer-visible service and diagnostic evidence rather than dashboard count.

DORA's [research program](https://dora.dev/research/) publishes research on software-delivery and organizational performance and emphasizes capabilities and outcomes over tool adoption. Its scope is not data architecture specifically, so mappings must remain hypotheses and local measurements must validate applicability.

NASA's [Technical Assessment](https://www.nasa.gov/reference/6-7-technical-assessment/) describes measuring technical progress and effectiveness, comparing actual status with plans, communicating risk, and taking corrective action throughout a lifecycle. It supports evidence-to-decision discipline without prescribing a data maturity ladder.

Together these sources support multidimensional profiles, explicit descriptors, scoped evidence, current and target states, capability and outcome measurement, security and privacy integration, operational observation, lifecycle assessment, and action. They do not provide one universal model, make self-ratings objective, transfer peer benchmarks, prove causality, set the right target, or establish that a higher number creates value. Those conclusions require local authority, evidence, moderation, sampling, stakeholder outcomes, counterfactual reasoning, and reassessment.

## Prerequisites and Retrieval

You should understand architecture scope, stakeholders, outcomes, capabilities, domains, data products, platform products, operating models, governance, metadata, lineage, quality, contracts, security, privacy, reliability, economics, risk, criticality, sampling, ordinal measurement, uncertainty, causal inference, roadmaps, migration, recovery, and closure.

Retrieve assessment purpose, assessment unit, capability domain, descriptor, maturity level, maturity profile, current profile, target profile, institutionalization, effectiveness, evidence claim, artifact, observation, runtime sample, coverage, confidence, recency, contradiction, moderation, assessor calibration, independence, aggregation, material gap, intervention, reassessment, receipt, and closure.

As a retrieval test, assess a catalog capability in a global enterprise. Ask which users and decisions require discovery; which regions, domains, products, stores, and classifications are in scope; whether an owner and service exist; whether registration is automated; whether metadata is correct and current; whether consumers find and understand products; whether access and policy paths work; which assets are absent; how samples were chosen; what incidents contradict the rating; whether recovery restores the catalog without stale routes; what target the risk justifies; and which evidence would show improvement. Counting catalog entries answers only one narrow question.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish maturity, capability, institutionalization, adoption, effectiveness, compliance, and outcome;
2. define assessment purpose, authority, scope, units, contexts, model version, evidence window, and intended decisions;
3. create architecture-specific capability domains and observable level descriptors without vague ladder language;
4. collect and triangulate document, configuration, runtime, interview, incident, consumer, cost, recovery, and outcome evidence;
5. record coverage, recency, contradiction, independence, confidence, exceptions, and limitations for every finding;
6. moderate ordinal ratings without false averages, precision, ranking, or benchmarking claims;
7. preserve uneven profiles, critical weak links, dependencies, and stakeholder differences during aggregation;
8. set fit-for-purpose target profiles from outcomes, obligations, criticality, risk, economics, and horizon;
9. translate material gaps into bounded interventions with hypotheses, owners, evidence, stop rules, and reassessment; and
10. retire obsolete assessment artifacts and prevent stale maturity claims from governing current architecture decisions.

## Core Exposition

**Begin with the decision.** State why the assessment exists: investment allocation, target-state preparation, regulatory assurance, platform planning, domain enablement, merger integration, risk treatment, or architecture governance. Name who decides, who is affected, what changes may follow, and what the assessment is forbidden to claim.

**Fix the reference context.** Record organization, business model, jurisdictions, obligations, strategy, critical outcomes, architecture topology, major transitions, reference date, evidence window, and model version. A maturity finding detached from context cannot be interpreted or compared later.

**Choose assessment units deliberately.** Enterprise, portfolio, business capability, domain, product, platform, region, value stream, and control surface answer different questions. Use units with accountable owners and observable boundaries. Preserve mappings between units rather than pretending one hierarchy is complete.

**Reject the single-score premise.** Data architecture is a system of heterogeneous capabilities. A matrix of units by capability domains retains unevenness, dependencies, and uncertainty. An aggregate may help navigation only when its method and loss are explicit; it cannot replace the underlying profile.

**Distinguish maturity from existence.** A capability can exist as a policy, team, process, tool, or service and still be weakly adopted, poorly operated, ineffective, fragile, or impossible to retire. Assess design, implementation, execution, adoption, effectiveness, resilience, evolution, and closure separately.

**Distinguish maturity from compliance.** Compliance asks whether stated requirements are met for a scope and time. Maturity asks how reliably and adaptively a capability produces appropriate outcomes. A compliant control may be manual and fragile; an advanced automated practice may violate an obligation.

**Distinguish maturity from sophistication.** More tools, layers, automation, models, and distributed ownership can increase complexity without capability. Prefer the simplest architecture that reliably meets outcomes and constraints. Mature teams deliberately avoid unnecessary capability.

**Select or tailor a model transparently.** Record source frameworks, licensed content boundaries, terminology mappings, omitted domains, added architecture concerns, changed descriptors, rationale, reviewers, and version. Never imply external certification or conformance from an internal adaptation.

**Make capability domains coherent.** Useful domains include strategy and outcomes; stakeholder and decision alignment; current-state knowledge; domain and semantic ownership; product and contract management; platform enablement; integration and interoperability; metadata and lineage; quality; governance and policy; security and privacy; reliability and operations; economics and value; evolution, migration, recovery, and closure.

**Avoid capability overlap.** If ownership, governance, accountability, stewardship, and operating model all ask the same question, their combined score overweights one condition. Define boundaries and dependency links. One item may supply evidence to several findings, but do not count it as independent confirmation.

**Write observable descriptors.** Replace “advanced governance” with conditions such as: named decision rights exist; policies have versioned owners; enforcement covers a measured population; exceptions expire; decision evidence is retained; incidents feed change; and recovery restores current policy. Each higher descriptor should add meaningful, observable capability rather than prestige words.

**Do not require a universal sequence.** Some capabilities develop in different orders. A product may have excellent runtime quality controls before an enterprise glossary exists. Descriptors may be cumulative where dependency requires it, but the assessor must record legitimate nonlinearity and local alternatives.

**Use a bounded level vocabulary.** A practical internal scale might distinguish unknown, ad hoc execution, owned repeatability, measured management, and adaptive outcome control. Names matter less than testable descriptors. Unknown is an evidence state, not the lowest maturity level.

**Define evidence before asking for ratings.** For each descriptor, specify acceptable artifacts, configurations, runtime observations, representative samples, decisions, incidents, consumer evidence, cost records, tests, recovery exercises, and outcomes. State which combinations are necessary and what can falsify a claim.

**Build an evidence register.** Give each item an identity, source, custodian, collection method, scope, population, sample, version, time, classification, integrity, retention, access, related claims, and limitations. Store safe references or digests when copying sensitive evidence would create risk.

**Triangulate evidence kinds.** A policy shows intent. A configuration shows implementation. Runtime telemetry shows observed execution. Interviews reveal interpretation and hidden work. Incidents reveal boundaries. Consumer evidence reveals use. Outcomes reveal effect. None is universally sufficient alone.

**Test documentation in operation.** Select representative and adversarial cases and trace them through actual ownership, contract, quality, access, policy, lineage, service, change, incident, recovery, and closure paths. A diagram that accurately describes only the happy path is partial evidence.

**Use interviews as claims, not proof.** Identify role, scope, experience, incentives, date, questions, and corroboration. Protect attribution where needed, but preserve whether opinions conflict. Seniority does not make a statement representative.

**Sample explicitly.** Define the population, sampling frame, method, strata, exclusions, sample size, time window, and likely bias. Include critical, ordinary, newly changed, legacy, failed, and low-visibility units. A convenience sample of showcase products inflates maturity.

**Weight risk in sampling, not truth.** Critical systems may deserve deeper evidence and more frequent assessment. That does not make their observed maturity count as the entire enterprise. Report risk-weighted decision views alongside unweighted coverage and unit findings.

**Measure coverage.** Record proportions of products with owned contracts, stores emitting lineage, policies enforced at tested points, recovery exercises passing, consumers meeting outcomes, and costs allocated. State denominators and exclusions. “Most” is not assessable.

**Measure recency and persistence.** A capability demonstrated once may not be institutionalized. Look across normal operation, changes, incidents, personnel turnover, demand spikes, and recovery. Set evidence expiry according to volatility and consequence.

**Seek contradictory evidence.** Search for bypasses, shadow copies, broken contracts, stale catalog entries, orphaned products, policy exceptions, unresolved quality incidents, failed restores, surprise bills, and consumer workarounds. An assessment designed only to confirm descriptors is advocacy.

**Separate absence from absence of evidence.** Missing telemetry may mean the capability is absent, unobserved, outside scope, intentionally manual, or unable to produce evidence. Record the distinction and its risk. Lack of assurance can itself create a material gap without proving operational failure.

**Rate with a claim ledger.** For every capability and unit, record candidate level, satisfied descriptors, failed descriptors, unknowns, evidence links, coverage, exceptions, contradictions, confidence, rationale, and implications. Avoid one cell containing an unexplained number.

**Rate to the highest fully supported descriptor.** If a required condition at a level is unproven, do not average it with stronger conditions. Record partial characteristics separately and decide whether a bounded exception is permissible. This preserves the meaning of ordinal levels.

**Keep confidence separate.** A high-maturity finding supported by a tiny or old sample can have low confidence. A clearly observed ad hoc practice can have high confidence. Conflating confidence with level hides both capability and evidence risk.

**Calibrate assessors.** Use shared examples, anchor evidence, independent ratings, rationale comparison, and reconciliation. Track systematic differences by assessor or unit. Calibration reduces drift; it does not remove judgment or create objectivity.

**Moderate material findings.** Bring capability owners, consumers, platform teams, security, privacy, operations, finance, and independent challenge where appropriate. Review evidence sufficiency, descriptor interpretation, conflicts, exceptions, risk, and affected parties. Preserve dissent and decision authority.

**Manage conflicts of interest.** People who fund, operate, transform, audit, or sell a capability have different incentives. Declare roles and interests, separate evidence custody from rating where consequence warrants, and commission independent review for high-stakes claims. Internal assessment must not claim external assurance.

**Protect assessment evidence.** Architecture evidence can reveal sensitive data locations, control gaps, credentials, dependencies, incidents, costs, and people. Classify access, minimize copies, redact safely, log use, constrain exports, preserve integrity, define retention, and include the assessment system in threat and privacy models.

**Report a profile, not a leaderboard.** Show capability by unit, target, confidence, coverage, criticality, dependency, and trend. Let users drill into evidence and exceptions. Do not publicly rank teams when context differs or when ranking creates incentives to hide problems.

**Treat aggregation as lossy.** Minimum can overstate one weak cell's relevance; maximum hides gaps; mean assumes intervals and compensation; median hides tails; weighted totals embed preferences. If an aggregate is used, show the full distribution and explicit decision rule beside it.

**Preserve critical weak links.** A portfolio with strong metadata, quality, and automation can still be unacceptable if identity, policy enforcement, semantic ownership, or recovery fails for a critical path. Use mandatory gates and dependency graphs before summary views.

**Compare like with like.** Trend comparisons require stable descriptor meaning, scope, sampling, evidence rules, and context—or an explicit bridge. Peer comparisons require comparable obligations, business models, topology, scale, and evidence methods. Rankings without these controls are storytelling.

**Beware Goodhart effects.** Once a maturity level becomes a funding, promotion, regulatory, or public target, teams optimize the observable artifacts. Monitor document proliferation, shallow automation, selective samples, incident suppression, and denominator changes. Pair indicators with direct outcome and countermetric evidence.

**Define targets from need.** For each unit and capability, derive target descriptors from user outcomes, obligations, criticality, threats, service, economics, planned architecture, dependency roles, and horizon. Some low-risk capabilities should remain simple; some critical controls require strong institutionalization before expansion.

**Do not maximize every cell.** Higher descriptors usually cost money, attention, process, platform capacity, and cognitive load. The target is sufficient, resilient capability for the context. Over-control can delay learning, centralize queues, or make safe local work impossible.

**Model dependencies.** A target for domain-owned contracts may depend on platform validation, catalog identity, policy services, domain capacity, and consumer migration. Record enabling and constraining relationships so roadmaps do not demand outcomes before prerequisites exist.

**Prioritize material gaps.** Combine outcome impact, risk exposure, obligation, dependency leverage, confidence, reversibility, information value, effort, and urgency. A large numerical gap in a low-value capability may matter less than a small control gap on a critical product.

**Translate gaps into mechanisms.** “Move from level two to four” is not an action. Specify a mechanism such as assign semantic authority, publish a versioned contract, automate conformance at release, instrument runtime decisions, exercise recovery, or retire an unsafe bypass. Name owner, consumers, resources, and failure behavior.

**Write an improvement hypothesis.** State how the mechanism should change observed behavior and outcomes, what assumptions it relies on, which population it affects, what adverse effects may appear, and what evidence would support, refute, or stop it. Maturity movement is not itself the business outcome.

**Choose bounded interventions.** Prefer a domain, product, platform path, control surface, or workload where evidence can be gathered safely and learning transfers plausibly. Establish baseline, comparison, time window, telemetry, qualitative feedback, stop rules, and reassessment.

**Fund operation, not artifact creation.** Include ownership, support, on-call, policy maintenance, evidence production, training, change, incidents, recovery, and closure. A project that leaves a document or tool without operating capacity may temporarily raise visible artifacts while lowering sustainability.

**Track leading and lagging evidence.** Training, contracts, automated checks, and adoption can predict capability. Consumer decision time, incident impact, regulatory outcomes, recovery, quality harm, and unit economics show effects later. Neither set alone establishes causal improvement.

**Use countermetrics.** Watch queue time, domain toil, exception growth, bypasses, duplicated data, consumer abandonment, false alerts, cost, staffing load, and concentration risk. An intervention can improve its target descriptor while harming the architecture system.

**Reassess after meaningful exposure.** Recheck capabilities after enough normal operation, change, incident, demand variation, and recovery to evaluate institutionalization. Immediate post-launch assessment mostly measures delivery intent.

**Version the assessment model.** Preserve descriptor text, evidence rules, mappings, tools, calculation logic, and governance. If the model changes, report restated and noncomparable results explicitly. Never rewrite history to fit the new ladder.

**Record an assessment receipt.** Include purpose, authority, model version, scope, units, context, participants, interests, evidence window, sample, claims, ratings, confidence, contradictions, moderation, dissent, target, actions, decisions, limitations, and triggers. Sign or otherwise protect integrity where consequence warrants.

**Monitor assessment quality.** Measure evidence coverage, stale items, contradiction resolution, assessor agreement, appeals, action traceability, closed-loop reassessment, decision use, and harm. A perfectly completed questionnaire can still be an ineffective assessment.

**Design correction and appeal.** Evidence can be wrong, scopes can be misunderstood, and ratings can harm teams or decisions. Define who can challenge a finding, what evidence is required, who adjudicates, how changes are versioned, and how downstream decisions are notified.

**Retire obsolete claims.** Mark ratings superseded when scope, ownership, regulation, architecture, evidence, or model changes materially. Remove them from current dashboards and automated decision paths while preserving required historical receipts.

**Close the assessment safely.** Revoke assessor and vendor access, delete unnecessary evidence copies, archive controlled receipts, expire exceptions, transfer open actions, retire dashboards and integrations, remove stale exports, and test that restored systems cannot republish obsolete ratings as current truth.

## Definitions and Notation

Let `M = (U, S, C, D, E, I, O, R, T, L)` be the maturity assessment defined in the review. Let `A` be assessment units, `C` capability domains, `Z` operating contexts or scenarios, and `V` the immutable assessment-model version.

Represent a finding as:

`F(a, c, z, V) = (l, e, k, q, x, n, r)`

where `l` is the ordinal level, `e` evidence identities, `k` coverage, `q` confidence, `x` exceptions and contradictions, `n` assessor rationale, and `r` reference date. A level without these companions is an unsupported label.

Define a claim `Claim(d, E, P, W)` where descriptor `d` is supported by evidence set `E` for population or scope `P` during window `W`. Support requires evidence appropriate to the descriptor; it does not establish causality or future persistence.

Let confidence be an ordered judgment from evidence sufficiency, independence, integrity, consistency, recency, and representativeness. It remains separate from maturity: `q != l`.

For an ordinal scale, `l_4 > l_3` means a descriptor ordering within model `V`. It does not imply that `l_4 - l_3` equals `l_2 - l_1`, that levels can be averaged meaningfully, or that one unit's level compensates for another's failure.

Represent the target profile as `T(a, c, z, h) = (l_t, evidence_t, rationale, owner, horizon, trigger)` for horizon `h`. A gap is material only when the difference between `F` and `T`, considering confidence, dependencies, outcomes, and risk, warrants action.

Define an intervention record `J = (gap, mechanism, hypothesis, population, owner, resources, measures, countermetrics, stop_rule, reassessment)`. Completion of `J` is activity evidence; improved capability and outcomes require new observations.

Define an assessment receipt `AR = (id, purpose, authority, V, scope, context, participants, interests, evidence, sampling, findings, moderation, dissent, targets, decisions, actions, limitations, triggers)`.

Define `Closed(AR)` to require that stale surveys, evidence copies, exports, dashboards, access grants, integrations, exceptions, and automated uses are removed or made nonoperable, required records remain controlled, and recovery cannot republish superseded findings as current.

## Mechanisms, Invariants, or Proof Structure

Use the following assurance gates.

**Purpose gate.** Name users, decisions, outcomes, authority, affected parties, allowed uses, prohibited claims, horizon, and success.

**Context gate.** Record business model, strategy, obligations, jurisdictions, architecture topology, transitions, threats, criticality, reference date, and evidence window.

**Scope gate.** Identify units, populations, capabilities, scenarios, inclusions, exclusions, owners, dependencies, and mappings between views.

**Model gate.** Version source frameworks, definitions, descriptor order, evidence rules, tailoring, omissions, mappings, licensed boundaries, and governance.

**Descriptor gate.** Require observable, discriminating, coherent, nonduplicative conditions with legitimate alternatives and falsifiers.

**Evidence gate.** Bind artifacts, configurations, runtime observations, samples, interviews, incidents, consumers, costs, recovery, and outcomes to identity, provenance, time, integrity, access, and limitations.

**Sampling gate.** Define population, frame, method, strata, exclusions, size, time, critical cases, failures, legacy, and bias.

**Finding gate.** Record rating, satisfied and failed descriptors, unknowns, evidence, coverage, confidence, contradictions, exceptions, rationale, and implications.

**Moderation gate.** Calibrate assessors, declare interests, include affected roles, challenge evidence, resolve or preserve disagreement, and identify authority.

**Aggregation gate.** Preserve distributions, critical weak links, dependencies, risk, confidence, and method loss before any summary view.

**Target gate.** Derive sufficient capability from outcomes, obligations, criticality, threats, service, economics, dependency roles, architecture direction, and horizon.

**Action gate.** Trace material gap to mechanism, hypothesis, owner, resources, measures, countermetrics, adverse effects, stop rule, and reassessment.

**Security and privacy gate.** Protect sensitive architecture, incident, control, cost, and personnel evidence through minimization, classification, authorization, integrity, audit, retention, and deletion.

**Comparison gate.** Establish stable definitions, scope, evidence rules, sampling, context, model bridges, and uncertainty before trend or peer claims.

**Outcome gate.** Separate delivery activity, adoption, operation, capability, risk, economics, and stakeholder outcomes; search for countereffects and alternatives.

**Reassessment gate.** Trigger on sufficient exposure, material architecture or context change, incident, failed recovery, model revision, evidence expiry, or decision need.

**Receipt gate.** Preserve purpose, authority, version, scope, evidence, sampling, findings, confidence, disagreements, targets, actions, decisions, limitations, and triggers.

**Closure gate.** Retire obsolete questionnaires, evidence copies, access, exports, dashboards, integrations, exceptions, and automated uses while preserving required history and testing nonactivation.

### Executable evidence: maturity-finding substantiation

The following program classifies ten invented capability findings against six required evidence gates.

<!-- bijux-verify: {"id":"maturity-finding-substantiation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"findings=10\nsubstantiated=4\nmissing_owner=1\nuntestable_descriptor=1\nmissing_artifact=1\nmissing_runtime_sample=1\nstale_evidence=1\nmissing_outcome_link=1\ncapability_domains=8\nassessment_scopes=5\nevidence_kinds=5\nassessment_receipts=10\ndecision_events=10\n","stderr":""}} -->
```python
findings = [
    {"domain": "architecture", "scope": "enterprise", "kinds": {"artifact", "interview", "runtime"}, "owner": True, "descriptor": True, "artifact": True, "runtime": True, "current": True, "outcome": True},
    {"domain": "governance", "scope": "domain", "kinds": {"policy", "runtime", "outcome"}, "owner": True, "descriptor": True, "artifact": True, "runtime": True, "current": True, "outcome": True},
    {"domain": "metadata", "scope": "platform", "kinds": {"artifact", "runtime", "outcome"}, "owner": True, "descriptor": True, "artifact": True, "runtime": True, "current": True, "outcome": True},
    {"domain": "quality", "scope": "product", "kinds": {"artifact", "runtime", "outcome"}, "owner": True, "descriptor": True, "artifact": True, "runtime": True, "current": True, "outcome": True},
    {"domain": "security", "scope": "portfolio", "kinds": {"policy", "runtime"}, "owner": False, "descriptor": True, "artifact": True, "runtime": True, "current": True, "outcome": True},
    {"domain": "platform", "scope": "platform", "kinds": {"artifact", "interview"}, "owner": True, "descriptor": False, "artifact": True, "runtime": True, "current": True, "outcome": True},
    {"domain": "interoperability", "scope": "domain", "kinds": {"interview"}, "owner": True, "descriptor": True, "artifact": False, "runtime": True, "current": True, "outcome": True},
    {"domain": "lifecycle", "scope": "portfolio", "kinds": {"artifact"}, "owner": True, "descriptor": True, "artifact": True, "runtime": False, "current": True, "outcome": True},
    {"domain": "metadata", "scope": "enterprise", "kinds": {"artifact", "runtime"}, "owner": True, "descriptor": True, "artifact": True, "runtime": True, "current": False, "outcome": True},
    {"domain": "quality", "scope": "product", "kinds": {"artifact", "runtime"}, "owner": True, "descriptor": True, "artifact": True, "runtime": True, "current": True, "outcome": False},
]

def evaluate(finding):
    if not finding["owner"]:
        return "missing_owner"
    if not finding["descriptor"]:
        return "untestable_descriptor"
    if not finding["artifact"]:
        return "missing_artifact"
    if not finding["runtime"]:
        return "missing_runtime_sample"
    if not finding["current"]:
        return "stale_evidence"
    if not finding["outcome"]:
        return "missing_outcome_link"
    return "substantiated"

results = [evaluate(finding) for finding in findings]
print(f"findings={len(findings)}")
for outcome in ["substantiated", "missing_owner", "untestable_descriptor", "missing_artifact", "missing_runtime_sample", "stale_evidence", "missing_outcome_link"]:
    print(f"{outcome}={results.count(outcome)}")
print(f"capability_domains={len({finding['domain'] for finding in findings})}")
print(f"assessment_scopes={len({finding['scope'] for finding in findings})}")
print(f"evidence_kinds={len(set().union(*(finding['kinds'] for finding in findings)))}")
print(f"assessment_receipts={len(findings)}")
print(f"decision_events={len(results)}")
```

The output reports ten findings, four substantiated and one of each declared failure, eight capability domains, five scopes, five evidence kinds, ten receipts, and ten decisions.

The evidence is deliberately narrow. Invented Booleans, labels, and sets establish deterministic gate order and counts only. They do not establish that a descriptor is valid, an owner has authority, artifacts are authentic, samples are representative, evidence is current, outcomes are caused by the capability, a rating is correct, a target is sufficient, or an intervention creates value. Production assessment requires governed model versions, evidence registers, sampling plans, direct observation, affected stakeholders, moderation, contradiction search, confidence judgments, security and privacy controls, outcome evidence, and reassessment.

## Alternatives and Trade-Offs

**No formal maturity model.** Architecture reviews stay close to decisions and avoid scoring bureaucracy. Cross-unit language, longitudinal evidence, gap visibility, and investment coordination may remain inconsistent.

**Adopt an external framework unchanged.** Definitions, training, benchmarking, and assessor ecosystems may improve. Context mismatch, licensing, framework incentives, missing architecture details, and false conformance claims can grow.

**Tailor an established framework.** Shared foundations combine with local outcomes and topology. Mapping, versioning, governance, comparability, and maintenance require explicit work.

**Build an internal capability model.** Descriptors can fit exact decisions and evidence. Blind spots, insularity, inconsistent terminology, maintenance cost, and lack of external challenge increase.

**Enterprise-wide assessment.** A broad profile reveals common dependencies and systemic gaps. Evidence load, shallow sampling, respondent fatigue, and averaging pressure increase.

**Risk-based scoped assessment.** Critical decisions receive deep evidence quickly. Hidden dependencies and low-visibility systemic weakness may be missed unless portfolio sampling complements it.

**Self-assessment.** Local knowledge, learning, and lower cost are strong. Incentives, inconsistent interpretation, optimism, and weak challenge reduce assurance.

**Independent internal assessment.** Calibration and challenge improve while context remains accessible. Capacity, trust, organizational politics, and perceived audit behavior can reduce candor.

**External assessment.** Independence, specialized experience, and peer context may improve. Cost, shallow local knowledge, evidence exposure, commercial incentives, and certification theater require control.

**Artifact-heavy evidence.** Findings are inspectable and repeatable. Documents can lag reality and reward bureaucracy.

**Runtime-heavy evidence.** Execution, coverage, and failure become visible. Instrumentation gaps, sampling, privacy, retention, and unobservable human practices limit conclusions.

**Interview-heavy evidence.** Tacit work, incentives, and exceptions surface. Recall, role, power, and confirmation biases require corroboration.

**One cumulative ladder.** Communication is simple and dependencies can be encoded. Legitimate nonlinear capability development and context-specific alternatives are obscured.

**Independent capability descriptors.** Profiles preserve diversity and local targets. Comparison, navigation, and roadmap dependencies are harder to communicate.

**Minimum-based aggregation.** Critical weak links stay visible. One irrelevant low cell can dominate unless scope and dependency are clear.

**Weighted summary.** Priorities can be represented compactly. Ordinal arithmetic, compensation, duplicated criteria, and hidden stakeholder preferences can mislead.

**Frequent automated assessment.** Drift and regressions surface quickly. Observable proxies can crowd out meaning, manual evidence, and outcomes.

**Periodic deep assessment.** Context, triangulation, and moderation improve. Findings age between assessments and impose concentrated effort.

**Target maximum maturity.** Ambition is simple to communicate. Cost, control burden, delay, complexity, and irrelevant capability expand.

**Target sufficient contextual capability.** Investment follows outcomes and risk. Decision authority must defend uneven targets and revisit them as context changes.

## Failure Modes and Misconceptions

1. **“Maturity is one property of the enterprise.”** Capabilities differ by unit, context, and evidence.
2. **“The assessment score is the outcome.”** It is an input to decisions and improvement.
3. **“A model is universally normative.”** Framework scope and assumptions require tailoring.
4. **“External terminology makes ratings objective.”** Descriptor interpretation and evidence still involve judgment.
5. **“The highest level is always best.”** Cost and control can exceed contextual value.
6. **“Every capability should share one target.”** Risk, criticality, obligation, and dependency differ.
7. **“Unknown means immature.”** It means evidence is insufficient for the claim.
8. **“No evidence proves absence.”** A capability may be unobserved, while lack of assurance remains a separate risk.
9. **“A policy proves capability.”** Intent may not be implemented, followed, or effective.
10. **“A diagram proves current architecture.”** Runtime routes and exceptions may contradict it.
11. **“A tool license proves adoption.”** Entitlement does not show use or outcome.
12. **“A catalog entry proves discoverability.”** Correctness, understanding, access, and consumer success matter.
13. **“A contract proves conformance.”** Runtime behavior and change need observation.
14. **“Lineage coverage is binary.”** Instruments, identities, fields, engines, paths, and time differ.
15. **“Automation is more mature than manual work.”** Unsafe automation can institutionalize harm.
16. **“Compliance equals maturity.”** Requirements and adaptive effectiveness answer different questions.
17. **“Technical sophistication equals maturity.”** Complexity can reduce operability and value.
18. **“Centralization is a higher level.”** Ownership topology is contextual, not ordinal.
19. **“Decentralization is a higher level.”** Nominal autonomy without capability is fragility.
20. **“Interview consensus proves reality.”** Shared belief may be wrong or incentive-shaped.
21. **“Executive evidence is representative.”** Operational and consumer experience can differ.
22. **“Showcase products represent the portfolio.”** Convenience samples inflate findings.
23. **“A large sample is unbiased.”** A flawed frame can exclude the most important cases.
24. **“Critical units should determine the average.”** Report risk views without erasing other units.
25. **“Evidence remains current until the next survey.”** Architecture and context can change immediately.
26. **“One successful execution proves institutionalization.”** Persistence through change and failure matters.
27. **“High maturity implies high confidence.”** Level and evidence confidence are independent.
28. **“Low maturity implies uncertain evidence.”** Ad hoc behavior can be observed clearly.
29. **“Assessors interpret descriptors consistently.”** Calibration and rationale comparison are needed.
30. **“Self-assessment has no conflict.”** Funding, reputation, and ownership create incentives.
31. **“External assessment has no conflict.”** Commercial and certification incentives remain.
32. **“More decimal places mean precision.”** Ordinal ratings do not support that arithmetic.
33. **“Averages preserve the profile.”** They hide variance, tails, and noncompensable gaps.
34. **“Weights are neutral.”** They encode authority and stakeholder preferences.
35. **“Peer rankings prove fitness.”** Context, scope, method, and obligations differ.
36. **“Trend lines are comparable across model changes.”** Descriptor and sampling drift can create false movement.
37. **“No score change means no improvement.”** Useful outcomes can change before a descriptor boundary is crossed.
38. **“A score increase proves an intervention worked.”** Selection, context, and measurement changes may explain it.
39. **“Completing actions closes gaps.”** Execution and outcomes require new evidence.
40. **“Training completion proves capability.”** Application, support, persistence, and effects remain.
41. **“Published product count proves adoption.”** Consumers may bypass, distrust, or misuse them.
42. **“More telemetry means better operation.”** Signals can be noisy, incomplete, or unactionable.
43. **“A clean dashboard proves resilience.”** Failure and recovery exposure are missing.
44. **“A passed recovery exercise proves every path.”** Scope, dependencies, data, and versions must be named.
45. **“Maturity gaps form the roadmap directly.”** Materiality, dependencies, mechanisms, and capacity must intervene.
46. **“One enterprise program can fix every gap.”** Bounded owners and mechanisms differ.
47. **“Public team rankings motivate honesty.”** They encourage gaming and hidden exceptions.
48. **“Assessment evidence is harmless metadata.”** It can expose sensitive systems, controls, incidents, and people.
49. **“A superseded score can remain on dashboards.”** Stale findings can govern current decisions incorrectly.
50. **“Deleting the survey closes the assessment.”** Exports, evidence copies, access, actions, and automated uses remain.

## Worked Examples

### Example 1

A global enterprise receives an overall catalog maturity score of four. Unit evidence shows two regulated regions missing half their critical products and relying on stale ownership. The profile preserves those gaps, disqualifies the aggregate for assurance, and funds identity and ownership correction before new discovery features.

### Example 2

A domain has a versioned data contract and release checks but no runtime consumer monitoring. Design and implementation rate as owned and repeatable; effectiveness and outcome remain unknown. The assessor does not lower confidence into the maturity level or award the higher descriptor based on documentation.

### Example 3

A platform portal publishes products in minutes, yet teams wait weeks for access approval and policy exceptions. Portal telemetry, ticket records, interviews, and consumer journey samples contradict the self-service claim. The improvement targets decision rights and policy automation rather than a new interface.

### Example 4

A critical finance pipeline passes quality checks during normal operation. Incident evidence reveals that late reference data bypasses the checks during month-end recovery. The finding records bounded normal coverage, a contradictory recovery path, and a material gap instead of averaging success and failure.

### Example 5

Two assessors independently rate semantic ownership differently. Calibration shows one counted a stewardship roster, while the descriptor requires authority over definitions, conflicts, and change. The moderated rating cites actual decisions and preserves the roster as partial evidence.

### Example 6

A small low-risk product deliberately uses a manual monthly contract review. It meets consumer outcomes, change volume is low, and incidents are absent across a long observation window. Its target does not require continuous automation merely because the model's highest descriptor contains it.

### Example 7

A company changes its maturity model to add recovery and closure. Historical scores are retained under the old version, overlapping evidence is restated where definitions match, and noncomparable cells are marked. The dashboard does not draw a false uninterrupted trend.

### Example 8

A platform team completes every improvement action but consumer decision time worsens. Countermetrics reveal additional approval queues and duplicated metadata. The reassessment records stronger artifact control but lower practical effectiveness and changes the intervention rather than celebrating action completion.

### Example 9

A merger assessment samples flagship products from both organizations and would miss orphaned legacy integrations. Risk-stratified sampling adds failed, rarely changed, externally shared, and recovery-critical paths. Those cases expose identity and retirement dependencies that shape the target architecture.

### Example 10

An assessment provider's access is revoked after moderation; sensitive evidence copies are deleted; controlled receipts and safe digests are archived; open actions transfer to owners; stale dashboards and exports are removed. An isolated restore proves the old integration cannot republish superseded ratings.

## Cross-Program Connections

- [Data Engineering](../../19-data-engineering/ROADMAP.md) supplies runtime evidence for pipelines, contracts, lineage, quality, orchestration, incidents, replay, migration, recovery, and retirement.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md) grounds capability claims in distributed storage, streaming, batch, query, metadata, consistency, scale, isolation, and failure behavior.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies evidence about schemas, constraints, transactions, physical design, performance, backup, restoration, change, and operational ownership.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) connects data-product maturity to contracts, compatibility, service objectives, client journeys, error behavior, support, and consumer outcomes.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) assesses self-service, paved paths, product adoption, cognitive load, policy, telemetry, cost, tenancy, support, incidents, recovery, and lifecycle.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns risk, identity, enforcement, evidence protection, threat modeling, assurance, incident response, and recovery findings.
- [Network Engineering](../../24-network-engineering/ROADMAP.md) supplies topology, flow, latency, throughput, access, segmentation, dependency, and failure evidence often absent from architecture diagrams.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) challenges ratings with partial failure, version skew, consistency, clocks, retries, recovery, and emergent behavior.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) connects capability models with architecture characteristics, fitness functions, boundaries, decisions, evolution, and technical debt.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies stakeholder, measurement, technical assessment, verification, validation, assurance, configuration, risk, lifecycle, and corrective-action discipline.

## References

1. UK Government, [Data Maturity Assessment for Government: Framework](https://www.gov.uk/government/publications/data-maturity-assessment-for-government-framework/data-maturity-assessment-for-government-framework-html), topics, themes, descriptors, evidence, and matrix-based assessment.
2. UK Government, [Delivering a Data Maturity Assessment: Objectives and Resources](https://www.gov.uk/government/publications/delivering-a-data-maturity-assessment-objectives-and-resources), planning, delivery, recording, and actioning assessment results.
3. EDM Association, [DCAM Framework](https://edmcouncil.org/frameworks/dcam/), capability, sub-capability, engagement, process, evidence, scoring, and roadmap provider context.
4. CMMI Institute, [Data Management Maturity Model FAQ](https://stage.cmmiinstitute.com/getattachment/b1ec339f-7d79-4056-af31-8cfd9b03eaf7/attachment.aspx), reference-model, practice-assessment, and improvement-roadmap context.
5. OECD, [The Path to Becoming a Data-Driven Public Sector](https://www.oecd.org/content/dam/oecd/en/publications/reports/2019/11/the-path-to-becoming-a-data-driven-public-sector_9ed7e867/059814a7-en.pdf), leadership, governance, architecture, infrastructure, value, ethics, privacy, security, and trust.
6. NIST, [Cybersecurity Framework 2.0: Using the CSF Tiers](https://www.nist.gov/publications/nist-cybersecurity-framework-20-quick-start-guide-using-csf-tiers), current and target profiles, risk-governance rigor, monitoring, and improvement.
7. NIST, [Privacy Framework 1.1](https://www.nist.gov/privacy-framework/using-privacy-framework-11), privacy outcomes, profiles, tiers, risk, and implementation context.
8. W3C, [Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/), quality dimensions, metrics, measurements, policies, annotations, and provenance.
9. OpenLineage, [Object Model](https://openlineage.io/docs/spec/object-model/), dataset, job, run, event, namespace, name, and facet evidence.
10. Bitol, [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/), machine-readable schema, quality, service, role, support, and infrastructure obligations.
11. Open Policy Agent, [Policy Language](https://www.openpolicyagent.org/docs/policy-language), structured policy decisions, rules, tests, and runtime context.
12. OpenTelemetry, [Specification](https://opentelemetry.io/docs/specs/otel/), telemetry signals, resources, context, semantic conventions, compatibility, and versioning.
13. FinOps Foundation, [FinOps Framework](https://www.finops.org/framework/), cross-functional ownership, usage and cost, value, optimization, and governance capabilities.
14. Google, [Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/), symptom and cause signals, latency, traffic, errors, saturation, precision, and actionability.
15. DORA, [Research](https://dora.dev/research/), capability- and outcome-oriented software-delivery and organizational-performance research context.
16. NASA, [Technical Assessment](https://www.nasa.gov/reference/6-7-technical-assessment/), technical measures, status, risk communication, effectiveness, corrective action, and lifecycle assessment.

## Exercises

### Exercise 1

Design a maturity assessment for a federated enterprise data architecture. Define purpose, authority, units, capability domains, contexts, model version, descriptor structure, evidence rules, sampling, confidence, moderation, security, outputs, and prohibited claims.

### Exercise 2

Write maturity descriptors and evidence requirements for semantic ownership, data contracts, metadata and lineage, computational governance, platform self-service, and recovery. Separate design, execution, adoption, effectiveness, resilience, and closure.

### Exercise 3

Plan evidence collection for 200 data products across five domains and three jurisdictions. Include population, stratification, critical and adversarial cases, evidence kinds, coverage, recency, contradictions, access, assessor calibration, and confidence.

### Exercise 4

Convert a maturity profile into a fit-for-purpose target profile and investment roadmap. Address outcomes, obligations, criticality, dependencies, material gaps, mechanisms, hypotheses, owners, resources, measures, countermetrics, stop rules, and reassessment.

### Exercise 5

Design reassessment and closure after a maturity model changes and an external assessor leaves. Cover version bridges, comparability, corrections, appeals, evidence retention and deletion, access revocation, dashboards, open actions, historical receipts, recovery, and stale-claim nonactivation.

## Answers to the Exercises

### Answer 1

State that the assessment supports target-state and investment decisions and cannot certify the enterprise or rank teams. Name executive decision authority, domain and platform owners, consumers, security, privacy, finance, operations, and independent challenge. Use enterprise, domain, product, platform, jurisdiction, and critical-path units linked by dependency maps. Assess strategy and outcomes, semantic ownership, products and contracts, platform enablement, integration, metadata, quality, governance, security and privacy, service, economics, evolution, recovery, and closure. Version the tailored model and source mappings. Require observable descriptors and triangulated artifacts, configurations, runtime samples, incidents, consumers, costs, recovery, and outcomes. Use risk-stratified sampling, separate confidence, moderate material findings, protect evidence, publish a profile with targets and receipts, and prohibit a single certification claim.

### Answer 2

For semantic ownership, require identified authority, actual conflict and change decisions, consumer understanding, persistence through turnover, and retirement of obsolete meanings. For contracts, distinguish publication, release conformance, runtime behavior, consumer adoption, compatibility incidents, and closure. For metadata and lineage, measure identified coverage, correctness, freshness, cross-platform continuity, incident use, recovery, and stale-route removal. For computational governance, require versioned policy authority, tests, enforcement coverage, decision evidence, expiring exceptions, safe rollout, incident correction, and restoration. For self-service, measure safe outcome lead time, cognitive load, support, adoption, error, cost, and recovery rather than portal existence. For recovery, require bounded objectives, dependency-ordered exercises, reconciliation, current authorization and semantics, consumer validation, evidence, correction, and proof that retired paths remain inactive.

### Answer 3

Define all 200 products as the population and construct a frame from contracts, catalogs, stores, access systems, lineage, cost records, and domain inventories, recording missing or conflicting identities. Stratify by domain, jurisdiction, criticality, data classification, workload, age, platform, external sharing, change rate, and ownership. Include every highest-criticality product plus randomized ordinary products, newly changed products, low-use legacy products, recent incidents, failed restores, exceptions, and products absent from the catalog. Collect policies, contracts, configurations, runtime traces, quality results, access decisions, incidents, consumer journeys, costs, and recovery evidence within declared windows. Protect sensitive evidence and minimize copies. Calibrate assessors on anchor cases, compare independent ratings, seek contradictions, and report coverage and confidence by stratum rather than generalizing a convenient sample.

### Answer 4

For each unit and capability, derive sufficient target descriptors from user outcomes, laws and policies, criticality, threat, service, economics, future architecture, and dependency roles. Preserve confidence and unknowns. Prioritize gaps using outcome impact, risk, obligation, dependency leverage, information value, reversibility, effort, and urgency rather than numerical distance alone. Translate each material gap into a mechanism such as assigned decision authority, versioned contracts, automated release checks, runtime policy evidence, recovery exercises, or retirement of bypasses. Write a causal hypothesis, affected population, owner, resources, measures, countermetrics, adverse effects, and stop rule. Order work by real prerequisites and capacity, establish baselines, expose critical paths, and reassess only after meaningful operational exposure.

### Answer 5

Freeze the old and new model versions, descriptor text, evidence rules, scope, samples, tools, and receipts. Map only genuinely equivalent descriptors and label restated, bridged, and noncomparable findings. Preserve original ratings rather than rewriting history. Offer a correction and appeal window with versioned evidence and adjudication. Revoke assessor identities, credentials, network paths, exports, and vendor integrations; delete unnecessary evidence copies under retention and privacy rules; retain controlled receipts and safe integrity proofs; and transfer open actions to named owners. Remove superseded findings from current dashboards and automated gates. In an isolated recovery exercise, restore old assessment components and prove stale ratings, access, exports, notifications, and decision integrations cannot reactivate as current truth.
