---
module_id: API-089
program: API & Service Engineering
level: 2
module_number: 89
title: API Product Ownership
status: complete
last_verified: 2026-09-02
---

# API Product Ownership

## One-Page Review

### Governing question

Who is accountable for an API’s consumer outcomes, coherent contract, service levels, security, economics, support, evolution, and retirement, and what evidence and decision rights let that ownership persist beyond one team, implementation, or release?

### Essential definitions

- An **API product** is the governed capability offered through a contract plus access, documentation, tooling, reliability, support, lifecycle, and operating commitments.
- A **consumer** is an accountable application/workflow depending on outcomes; an **end user** may experience those outcomes without integrating directly.
- A **product owner** is accountable for value, scope, priorities, consumer evidence, service offer, and lifecycle decisions within explicit authority; ownership is not unilateral technical control.
- A **service owner** is accountable for the live service’s operability, reliability, support, risk, and continuity; one person/team may hold both roles, but duties remain explicit.
- A **capability boundary** describes the durable outcome owned by the API, not its current database, deployment, gateway, or organizational chart.
- A **service offer** states eligibility/access, contract, limits, security/privacy, SLO/support, documentation/tooling, change policy, pricing/cost expectations, and exit.
- A **product outcome** is a consumer/business result; requests, registrations, SDK downloads, and traffic are supporting signals rather than value by themselves.
- A **decision right** names who proposes, advises, approves, accepts risk, operates, and is informed for a bounded decision.

### Central model, mechanism, or theorem

Let product obligations be consumer/value evidence $C$, contract/design integrity $K$, security/privacy $S$, live operations/reliability $O$, and lifecycle/economics $L$. A launch or major evolution is ready only when all applicable obligations have accountable current evidence:

$$
\operatorname{ready} \Rightarrow C\land K\land S\land O\land L.
$$

No average adoption, traffic, roadmap, or checklist score compensates for a missing fatal obligation. The ownership record maps every obligation/decision to accountable roles, authorities, evidence, escalation, and succession; one named product owner coordinates the whole without erasing specialist authority.

### Critical invariants

Every production API has one discoverable accountable product/service ownership chain, a stable capability boundary, known consumer segments/outcomes, and an explicit offer. Technical, product, security, privacy, reliability, support, data, finance, and legal decision rights are clear. Ownership transfers preserve history, commitments, credentials, artifacts, on-call/support, and consumer contacts.

Roadmaps balance value, risk, reliability, security, compatibility, cost, and retirement. Metrics segment consumers and effects, disclose sampling/unknowns, and pair leading with outcome/guardrail measures. Internal APIs receive product discipline proportional to their consumers and switching cost. Deprecation, migration, and retirement are funded product work, not abandoned engineering cleanup.

### Common failures

Owning a repository but not an outcome; product owner as ticket sorter; platform/API team as default owner of every domain; one employee email as ownership; business owner without technical authority; engineering owner without consumer mandate; roadmap driven by loudest client or aggregate traffic; registrations called adoption; requests called value; availability without correct outcomes; p50 hiding tail consumers; public docs with hidden support/limits; internal API treated as free/private; chargeback without cost transparency; SLO copied from infrastructure; compatibility debt unfunded; breaking cleanup for consistency; deprecation without consumer inventory; ownership transfer loses obligations; orphaned APIs stay reachable; and success measured by launch rather than sustained use and safe exit.

### Compact example

An internal payments API handles 99.9% of requests successfully, but three of 120 consumer workflows cannot complete month-end settlement after an error-semantics change. Request success looks excellent; confirmed consumer outcome success is at most $117/120=97.5\%$. Product ownership blocks retirement of the old behavior, funds a compatibility adapter and migration, and adds settlement-effect/SLO evidence. **Conclusion:** high traffic health does not prove consumer value or lifecycle readiness.

### Connections

[Outside-In Requirements](011-outside-in-api-requirements.md) discovers jobs and outcomes. [Contracts](021-api-contracts-and-behavioral-guarantees.md) define the offer’s behavioral core. [Compatibility](081-backward-and-forward-compatibility.md), [Deprecation](084-deprecation-and-sunset.md), [Consumer Inventory](085-consumer-inventory-and-usage-evidence.md), [Style Guides](086-api-style-guides.md), [Design Reviews](087-design-reviews.md), and [Schema Registries](088-schema-registries-and-contract-governance.md) supply lifecycle controls.

## Governing Question

How should product and service ownership define the API product boundary and offer, discover and prioritize consumer outcomes, allocate decision rights and funding, measure service/value/economics, support adoption, govern change, and retire safely throughout a long-lived interface lifecycle?

## Why This Matters

An API can be technically correct and still fail as a product. Consumers may not discover it, obtain access, understand errors, generate a usable client, know limits, receive change notices, diagnose incidents, or reach accountable support. A contract without an operating offer transfers coordination cost to every consumer.

An API outlives implementation projects. Teams reorganize, vendors change, databases migrate, and gateways are replaced while consumer dependencies persist. If ownership is attached only to a repository or original author, decisions become orphaned precisely when compatibility, incidents, or retirement require authority.

APIs also distribute costs and risks. Provider convenience can create consumer migration work; a powerful general endpoint can create security and capacity exposure; a strict quota can protect service health while breaking critical workflows. Product ownership makes these cross-boundary effects visible and funds the full lifecycle rather than optimizing only provider delivery.

“Internal” does not remove product concerns. Internal consumers may be numerous, independently deployed, business-critical, and unable to switch cheaply. The appropriate ceremony may be lighter than for a public API, but accountability, offer, evidence, reliability, support, and evolution remain necessary.

## Prerequisites and Retrieval

Retrieve [Outside-In API Requirements](011-outside-in-api-requirements.md), [Designing from Consumer Tasks](020-designing-an-api-from-consumer-tasks-rather-than-database-tables.md), [API Contracts and Behavioral Guarantees](021-api-contracts-and-behavioral-guarantees.md), [Rate Limits and Quotas](039-rate-limits-and-quotas.md), [Choosing an Interface Style](060-choosing-an-interface-style-from-interaction-semantics.md), [Backward and Forward Compatibility](081-backward-and-forward-compatibility.md), [Deprecation and Sunset](084-deprecation-and-sunset.md), [Consumer Inventory](085-consumer-inventory-and-usage-evidence.md), [API Style Guides](086-api-style-guides.md), [Design Reviews](087-design-reviews.md), and [Schema Registries](088-schema-registries-and-contract-governance.md).

Retrieve organization/product strategy; stakeholder/user research; consumer identity/use evidence and support history; service catalog/ownership; contracts/specifications and generated SDK/docs; SLO/SLI/SLA and incidents; security/privacy/data classification; costs/capacity/quotas/pricing; roadmap/backlog/decisions; compatibility/deprecation records; access/onboarding journey; support/escalation/on-call; dependencies/suppliers; regulatory/legal commitments; adoption/outcome metrics with sampling/lineage; and lifecycle funding.

## Learning Objectives

After completing this module, you can:

1. define an API product by capability, consumers, offer, outcomes, and lifecycle rather than implementation;
2. distinguish product, service, engineering, domain/data, security/privacy, support, and executive accountabilities;
3. map decision rights, escalation, risk acceptance, succession, and ownership transfer explicitly;
4. discover and segment consumer jobs, criticality, alternatives, cadence, and total integration experience;
5. write a complete service offer covering access, contract, reliability, limits, support, change, economics, and exit;
6. prioritize value, risk, compatibility, reliability, security, cost, and lifecycle without scalar-score theater;
7. define user-centered SLOs and product metrics that resist traffic/adoption vanity and aggregation bias;
8. operate onboarding, documentation, SDKs, support, incidents, feedback, and communication as product surfaces;
9. fund and govern compatibility, migration, deprecation, ownership succession, and retirement; and
10. evaluate internal and external API portfolios using evidence, outcomes, obligations, and sustainable economics.

## Core Exposition

### Define the API product boundary

Name the durable capability and outcomes: “initiate and track a settlement,” not “expose settlement table”; “evaluate eligibility,” not “call service X.” Map operations/events, data authority, state, consumers, dependencies, and excluded responsibilities.

Separate product, service, and deployment. One product may have REST, event, webhook, SDK, sandbox, and portal surfaces; several deployments/regions serve one contract; one gateway hosts many products. Ownership follows the capability/offer, not the infrastructure box.

Record portfolio relationships: predecessor/replacement, composition, shared schemas, upstream/downstream, bundled offers, and overlapping capabilities. Duplicate APIs can be deliberate for exposure or lifecycle, but ambiguity needs an owner and convergence/positioning decision.

State lifecycle and audience: experimental, private/internal, partner, public; discovery, beta, general availability, deprecated, sunset, retired. Each state changes entitlement and commitments explicitly.

### Establish accountable ownership and decision rights

Create a durable ownership record: product owner, service/engineering owner, business/domain owner, data steward, security/privacy contacts, reliability/on-call, support/documentation/developer experience, finance/cost, legal/regulatory, executive escalation, and succession group.

Do not reduce this to a committee with no accountable integrator. One role is answerable for a coherent product and for routing/closing cross-domain decisions. Specialist authorities retain nondelegable decisions: product urgency cannot waive object authorization; engineering preference cannot break entitled consumers; security cannot invent product priority alone.

For recurring decisions, name who proposes, supplies evidence, approves, accepts residual risk, implements/operates, and must be consulted/informed. Cover boundary, contract, exposure, access, SLO, quota/pricing, roadmap, exception, incident, compatibility, deprecation, retirement, supplier, and ownership transfer.

Use role/group contacts rather than one person, with named deputies and escalation. Audit acknowledgement and periodic attestation. Unknown or stale ownership is an operational risk with deadline and escalation.

### Discover consumers, users, and jobs

Segment direct integrators, accountable applications/workflows, tenants, end users, partners, internal teams, SDK/tool builders, operators/support, auditors, and downstream relays. Do not equate credential, user, tenant, request, or trace with a logical consumer.

Research desired outcomes, current workaround, frequency/cadence, criticality, data/security constraints, environments, latency/reliability, volume/cost, error/recovery, SDK/language, support, purchasing/access, and switching/migration cost. Include dormant, batch, disaster, offline, replay, and failed-call paths.

Observe the whole journey: discover, assess fit, request access, authenticate/authorize, explore sandbox, integrate, test, deploy, monitor, debug, obtain support, learn changes, migrate, and exit. Provider implementation milestones are not consumer outcomes.

Keep a consumer advisory mechanism but avoid capture by the loudest or largest client. Pair interviews/support with inventory/telemetry/contract evidence and seek nonusers/lost consumers.

### Define the value proposition and offer

State which outcome is improved, for whom, compared with which alternative, and under what constraints. Validate that an API is the right interface; sometimes event, bulk export, product UI, shared library, or no new capability is better.

The offer includes capability/scope, eligibility/audience, access and identity, contract/protocol/version, security/privacy/data handling, service tier/SLO/support hours, quotas/limits/fairness, pricing/chargeback/cost expectations, environments/sandbox, docs/examples/SDKs, ownership/contact, change/compatibility policy, deprecation/support window, and exit/data portability.

OpenAPI’s Info/contact fields can publish useful metadata but cannot make an owner accountable or describe the whole offer. Keep catalog, portal, specification, status page, contract, billing, and support views consistent and provenance-linked.

Express exclusions and shared responsibilities. Consumers need to know retry/idempotency, credential rotation, local validation, data retention, incident reporting, and migration duties; providers own their corresponding guarantees and signals.

### Shape strategy and roadmap

Connect organizational outcomes to consumer problems and API capability changes. A roadmap contains discovery/learning, reliability/security/operability, compatibility/migration, platform/tooling, cost/capacity, documentation/support, and retirement—not only new endpoints.

Evaluate proposals as a vector: consumer value/coverage, strategic fit, risk reduction, urgency/time criticality, compatibility/externalized cost, reliability/security/privacy, evidence confidence, delivery/operating cost, dependencies, reversibility, and opportunity cost. A single weighted score can hide a mandatory control or uncertain assumption.

Use explicit hypotheses and smallest credible experiments: prototype, mock/contract exploration, design review, consumer test, shadow traffic, beta cohort, or operational rehearsal. Do not expose unstable public contracts merely to “learn quickly” without lifecycle expectations.

Reserve capacity for product health and lifecycle. If every period funds only feature demand, reliability, docs, migrations, stale consumers, and retirement become crises.

### Govern design and contract quality

Product ownership supplies consumer outcome/scope and accepts coherent product trade-offs; engineering/domain/protocol/security reviewers supply specialist judgment. Use style guides and registries as controls, not substitutes for ownership.

Maintain one governed contract record across specification, runtime behavior, generated SDK/docs/examples, service offer, SLO, and lifecycle. Ambiguous errors, defaults, ordering, limits, authorization, or timing are product defects even if syntax validates.

Record decisions and alternatives with evidence. Prevent one consumer-specific workaround from silently becoming global semantics. Decide when segmentation, a new operation/profile, adapter, or separate product is justified.

Treat compatibility as a product commitment. Semantic diff, consumer inventory, generated artifacts, rollout/rollback, and direct communication belong in change planning.

### Define service levels from user outcomes

Choose service-level indicators from behavior consumers need: valid authorized requests yielding correct timely outcomes, accepted jobs completing within bound, events delivered/processed within freshness, consistent reads after promised action, or successful settlement effects. Infrastructure uptime alone can be green while the API is useless.

Segment by operation/tier/region/consumer criticality where aggregation hides harm. Define eligible events, good condition, measurement point, exclusions, window, objective, data quality, and consequence. Google SRE emphasizes defining the service behavior that matters to users and measuring/evaluating it.

Set objectives from user need, dependency feasibility, cost, and risk; do not copy 99.9%. For a 30-day window, 99.9% permits about $0.001\times30\times24\times60=43.2$ minutes of bad eligible time only under a time-based model—request/event objectives behave differently.

Use error budgets as decision input with agreed policy, not permission to spend harm arbitrarily. Pair availability/latency with correctness, freshness, durability, security, and support where relevant.

### Make onboarding and developer experience part of the product

Measure time and failure from discovery to first meaningful production-like outcome, not merely first HTTP 200. Provide audience/fit, prerequisites, access workflow/SLO, secure credential guidance, quickstart, conceptual model, contract reference, realistic examples, SDKs, sandbox/mocks, testing, errors/troubleshooting, limits, observability, status/support, changelog, and migration.

Test examples and generated SDKs against current approved contracts. Cover multiple languages/environments only where owned; an abandoned SDK is worse than a clearly unsupported one.

Design self-service for safe common paths and human help for high-risk/ambiguous paths. Capture where access approvals, networking, identity, quota, docs, or errors delay consumers.

Accessibility and localization can apply to portals/docs and end-user effects. Security controls should be understandable and automatable, not undocumented rituals.

### Operate support, feedback, and incidents

Publish support channels, scope, hours, severity, response/communication expectations, escalation, status, and emergency/security reporting. Route by product/operation/tenant impact using safe correlation, not by which team happens to receive a ticket.

Unify feedback from support, incidents, docs search, onboarding drop-off, design reviews, telemetry, consumer attestations, surveys/interviews, sales/partner channels, and deprecation work. Preserve source/segment so high-volume noise does not erase rare critical pain.

During incidents, product ownership helps classify consumer/business effects, prioritizes communication/workarounds, and coordinates dependent owners; service/incident command retains operational authority. Follow-up turns recurring product/system causes into funded work.

Close feedback loops visibly where appropriate. Explain accepted, deferred, or rejected proposals and constraints without exposing sensitive internals.

### Manage security, privacy, trust, and compliance

Product ownership ensures threats, data uses, access, abuse economics, privacy/legal basis, retention/deletion, audit, residency, supplier risk, and incident duties are included in the offer and roadmap. Specialists define/verify controls and accept risks within authority.

Avoid growth metrics that reward excessive data collection or broad scopes. Minimize telemetry while retaining ownership/outcome evidence. W3C Trace Context enables cross-system correlation but carries privacy/security considerations; it is not consumer identity.

Keep examples, logs, support tooling, analytics, and portals free of secrets/unnecessary personal data. Define who can see consumer inventory, contracts, usage, and cost.

Security changes can require urgent lifecycle action, but urgency still needs scope, consumer impact, communication, safe terminal behavior, rollback/recovery, and recorded authority.

### Own economics, capacity, quotas, and fairness

Model total cost: product discovery/design, build, infrastructure/dependencies, platform/shared allocations, operations/on-call, security/compliance, docs/SDK/support, consumer integration/migration, and retirement. Provider unit cost alone externalizes the largest burdens.

Understand demand distribution, concurrency, payload, fan-out, storage/egress, retries, failure amplification, tier/region, and growth uncertainty. Connect forecasts to capacity, dependency contracts, quotas, load shedding, and roadmap.

Pricing/chargeback can shape behavior but must be predictable, explainable, measurable, and compatible with public/internal incentives. “Free internal API” still consumes scarce capacity/support and can create lock-in.

Quotas protect fairness/reliability and communicate entitlement. Product owners decide tiers and consumer consequences with reliability/security/finance input; arbitrary low quotas or surprise enforcement are product defects.

### Measure adoption, value, health, and sustainability

Separate discoverability/interest (views, registrations), activation (first meaningful outcome), adoption (repeated production use by target consumers), value/outcomes (business/user effects), service health (correctness/latency/freshness), experience (integration/support effort), lifecycle (version/migration/unknowns), and sustainability (cost/capacity/toil).

Count logical operations/effects and consumers, not only attempts. Segment distributions and critical cohorts. Record sampling, telemetry gaps, identity confidence, seasonality, and denominators. A high-volume client can hide many failing low-volume consumers.

Use balanced leading/lagging and guardrail measures. A target for call volume can encourage chatty designs; SDK downloads can be bots/unused; registration can be abandoned; low tickets can mean no adoption or inaccessible support.

Pair quantitative evidence with consumer research and concrete case outcomes. Publish performance appropriate to exposure while protecting sensitive consumer/business data.

### Govern change, migration, and retirement

Classify every change structurally and behaviorally across client/server, SDK/docs, operations, security, quotas, timing, and consumer expectations. Product roadmap funds compatibility adapters, dual operation, telemetry, communication, and support.

Deprecation states exact scope, replacement, dates, reasons, migration guidance, contacts, signals, and support. RFC 9745 defines HTTP deprecation signaling for resources but does not replace direct consumer communication or alter behavior by itself.

Track migration per required consumer and outcome, not aggregate requests. Test dormant, partner, batch, offline, replay, failover, backup/restore, support tools, and rollback paths. Exceptions have owner, risk, scope, expiry, and removal condition.

Retirement verifies replacement value/service/capacity/security, consumer migration or accepted exception, old-use cessation with healthy evidence, state/data/support/incident readiness, terminal response, cleanup, and preserved audit/replay artifacts. Exit is part of the original offer.

### Transfer ownership and manage the portfolio

Ownership transfer inventories contracts, consumers, commitments, decisions/exceptions, roadmap, SLOs/incidents, dependencies/suppliers, credentials/access, costs/capacity, docs/SDKs, support/on-call, deprecations, regulatory records, and known unknowns. Both parties acknowledge; catalogs/contact/escalation update atomically.

Reorganization does not reset promises or evidence. Maintain stable product identity and ownership history. If no owner accepts obligations, restrict new adoption and escalate retirement/transfer rather than leave an orphan live.

Portfolio review identifies overlaps, gaps, shared dependencies, inconsistent offers, systemic migration, critical concentration, orphan/stale products, and investments best supplied by platform capabilities. Avoid forcing distinct domains into one API for catalog neatness.

Retire unused/redundant products deliberately. A smaller owned portfolio is healthier than a large discoverable graveyard.

## Definitions and Notation

Let $C,K,S,O,L$ denote adequate current evidence for consumer/value, contract/design, security/privacy, operations/reliability, and lifecycle/economics obligations. Readiness requires their conjunction when applicable; it is not an average score.

Let credible required consumers be $U$, consumers achieving the defined outcome be $G$, and consumer outcome ratio $g=G/U$ for $U>0$. Let transport attempts be $Q$, logical operations $J$, and business effects $E$; each answers a different product/operations question.

Let total lifecycle cost $T=B+R+D+M+X$, where $B$ is build/change, $R$ run/infrastructure, $D$ documentation/developer/support, $M$ consumer migration/externalized work, and $X$ exit/retirement. These are accounting categories, not universal estimation formulas.

## Mechanisms, Invariants, or Proof Structure

**Obligation conjunction.** If consumer value is evidenced but object authorization is absent, or design is sound but no live owner/rollback exists, the product is not ready. Since each obligation can independently cause unacceptable harm, readiness requires all applicable obligations rather than an average.

**Traffic counterexample.** One healthy migrated consumer can generate 99.9% of requests while several critical low-volume consumers fail. Thus request-weighted success does not imply consumer- or outcome-complete success.

**Ownership continuity argument.** Consumer commitments attach to the offered capability/contract, not an employee or deployment. A team transfer that loses decisions, contacts, SLOs, or exceptions leaves commitments unchanged but evidence/authority absent. Therefore transfer must preserve the obligation graph and history.

**Lifecycle-cost argument.** A design with lower provider build cost can require every consumer to implement retries, adapters, or migrations. Omitting $M$ and $X$ biases prioritization toward externalizing cost. Sustainable ownership evaluates total lifecycle effects, even when exact monetary valuation is uncertain.

Operational invariants are: capability/offer explicit; consumer outcomes evidenced; one accountable ownership chain; specialist authorities preserved; contract/runtime/docs coherent; SLO user-centered; costs and externalities visible; roadmap balances health/lifecycle; metrics segmented/provenanced; compatibility funded; transfer complete; and exit governed.

## Alternatives and Trade-Offs

Central API product management creates consistency/portfolio visibility but can detach decisions from domains and bottleneck teams. Fully domain-owned APIs preserve context but fragment offers/tooling. Keep domain product accountability with shared platform/governance capabilities and portfolio standards.

One owner provides clarity but risks overload/single-person fragility. Committee ownership spreads expertise but diffuses accountability. Use one answerable role backed by explicit multidisciplinary authorities, groups, deputies, and escalation.

Public roadmaps help planning/trust but create implied commitments and expose sensitive strategy. Opaque roadmaps preserve flexibility but surprise consumers. Publish confidence/time horizons and committed lifecycle notices separately from discovery ideas.

Broad general APIs maximize reuse but increase complexity, authorization, quota, and evolution coupling. Narrow APIs fit tasks but proliferate surfaces. Choose from capability coherence and consumer evidence; compose where ownership remains clear.

Strict SLOs improve trust but cost capacity/complexity; weak SLOs reduce cost but may destroy consumer outcomes. Segment tiers and price/fund commitments transparently rather than silently underdeliver.

Self-service reduces marginal support but can make complex/high-risk onboarding unsafe. Human review improves context but delays consumers. Automate common safe paths with measurable escalation for exceptions.

## Failure Modes and Misconceptions

- “The repository owner owns the API.” Code custody is only one obligation.
- “The product owner decides everything.” Specialist authority and evidence still govern.
- “Internal APIs do not need product management.” Internal consumers still bear switching and failure cost.
- “Traffic is adoption.” Retries, probes, one client, or failed calls can dominate.
- “Availability is value.” Correct timely consumer outcomes matter.
- “Registration means activation.” A consumer may never achieve a production outcome.
- “The loudest customer is the market.” Segment evidence and strategic fit matter.
- “Roadmap means features.” Reliability, security, docs, migration, cost, and retirement require capacity.
- “OpenAPI contact establishes ownership.” Metadata does not create authority or continuity.
- “Platform owns every API.” Platform owns enabling capabilities; domains own their offered semantics.
- “A 99.9% average is enough.” Critical tail consumers/effects may fail.
- “Quotas are purely technical.” They define entitlement, fairness, and consumer outcomes.
- “Breaking cleanup reduces debt.” It can transfer much larger cost to consumers.
- “Deprecation is engineering cleanup.” It is a funded consumer/product migration.
- “Reorganization resets promises.” Contracts and lifecycle commitments persist.
- “Launch completes ownership.” Operation, evolution, support, and exit dominate lifetime.

## Worked Examples

### Example 1

A team owns gateway configuration but cannot define settlement semantics. Catalog ownership moves to the payments capability team; platform remains responsible for gateway controls and SLO dependencies.

### Example 2

Five thousand SDK downloads produce only 40 registered consumers and 12 repeated production outcomes. Product reporting separates interest, activation, adoption, and value instead of claiming 5,000 adopters.

### Example 3

One client produces 99.9% of calls successfully while three of 120 workflows fail month-end. Request health masks consumer outcome ratio $117/120=97.5\%$.

### Example 4

A 99.9% time-based objective over 30 days permits 43.2 bad minutes under its exact model. A settlement completion SLI is added because uptime minutes cannot detect wrong financial effects.

### Example 5

An internal API is “free,” but each of 30 consumers builds a custom retry adapter. Funding a standard idempotency/retry contract lowers total lifecycle cost despite provider work increasing.

### Example 6

A large partner requests a bespoke global field meaning. Research shows it conflicts with other consumers; product ownership offers a scoped operation/profile rather than corrupting common semantics.

### Example 7

Support tickets fall after a documentation change, but production activation also falls. Funnel and interview evidence reveals access approval broke; low ticket count was not improved experience.

### Example 8

A security vulnerability forces accelerated deprecation. Owner maps consumers, publishes exact signals/guidance, supplies an adapter, validates replacement capacity, records exceptions, and rehearses terminal behavior.

### Example 9

During reorganization, code transfers but on-call, partner commitments, exceptions, and signing keys do not. Transfer gate remains incomplete until the whole ownership record and access are acknowledged.

### Example 10

Portfolio review finds two overlapping eligibility APIs. Evidence shows distinct regulated and low-latency domains; they remain separate products with clear positioning and a shared schema/platform component.

## Cross-Program Connections

[Software Design & Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) supplies capability boundaries, ubiquitous language, stakeholder discovery, and durable domain ownership.

[Software Methods & Evolution](../../10-software-engineering-methods-and-evolution/ROADMAP.md) supplies product discovery, prioritization, feedback, stakeholder governance, roadmaps, organizational change, and lifecycle economics.

[Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) supplies SLOs, error budgets, incidents, operational readiness, capacity, safe delivery, and reliability ownership.

[Security Engineering](../../25-security-engineering/ROADMAP.md) supplies decision authorities, trust, abuse, privacy, compliance, risk acceptance, supply chain, and incident duties.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies stakeholder needs, lifecycle management, interface ownership, configuration/decision control, verification, suppliers, risk, and retirement.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies catalogs, portals, paved paths, access, templates, registries, telemetry, cost visibility, and self-service used by API product owners.

## References

1. OpenAPI Initiative, [OpenAPI Specification](https://spec.openapis.org/oas/latest.html).
2. Google Cloud, [Cloud API Design Guide](https://cloud.google.com/apis/design).
3. GOV.UK, [Service Standard](https://www.gov.uk/service-manual/service-standard).
4. Google, [Service Level Objectives](https://sre.google/sre-book/service-level-objectives/).
5. IETF, [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html).
6. IETF, [RFC 9745: The Deprecation HTTP Response Header Field](https://www.rfc-editor.org/rfc/rfc9745.html).
7. W3C, [Trace Context](https://www.w3.org/TR/trace-context/).

## Exercises

### Exercise 1

Define the product boundary, offer, ownership roles, and decision rights for an internal customer-profile capability exposed through REST, events, SDKs, and a portal across 80 consumer teams and regulated regions.

### Exercise 2

Build a balanced outcome/service/experience/lifecycle/economic measurement model for an API currently reporting only request volume, p50 latency, registrations, and ticket count. Identify gaming and aggregation risks.

### Exercise 3

An API reports 99.9% successful requests, 117 of 120 consumers achieving their outcome, a 99.9% 30-day time-based SLO, and three failed month-end workflows. Recompute the consumer outcome ratio and time allowance, then make a product decision.

### Exercise 4

Prioritize a roadmap containing a popular new filter, object-authorization remediation, reliability toil, SDK onboarding, a breaking naming cleanup, partner migration, and retirement of an orphaned predecessor. Explain authority and funding.

### Exercise 5

Design an ownership-transfer and eventual-retirement evidence package for an API whose team is dissolving, whose replacement exists, and whose consumers include partners, quarterly jobs, disaster recovery, and generated clients.

## Answers to the Exercises

### Answer 1

Define the capability as governed profile retrieval/change outcomes, not its database or gateway. Bundle REST resource/operations, change events, supported SDKs, portal/access, identity/data classifications, region behavior, SLO/support, quotas/cost, compatibility, deprecation, and exit; declare exclusions and source-of-truth/state responsibilities. Product owner is answerable for segments/value/offer/roadmap/lifecycle; domain/data owner for meaning/authority; engineering/service owner for implementation/live operation; platform for portal/gateway/event/runtime capabilities; security/privacy/legal for access, regulated data/residency/retention/risk; reliability/on-call/support/SDK owners for named surfaces. Map proposal/evidence/approval/risk/operation for boundary, fields/events, regional exposure, access/scopes, SLO, quota, changes, incident, exceptions, and retirement. Use role groups/deputies/escalation. Inventory all 80 consumers by use/cadence/region/criticality and keep downstream relay/unknown risk visible.

### Answer 2

Add funnel measures: eligible target consumers, discovery, qualified access requests, access lead/failure, first meaningful sandbox and production outcome, repeated active workflows, retention/exit. Outcome measures count correct business effects and consumer segments, not attempts. Service measures include correctness, availability, latency tails, freshness/consistency, error/retry/limit behavior and dependency/region/tier distributions with SLO eligibility/data quality. Experience measures time-to-first-outcome p50/p95, integration rework, docs search/failures, support resolution and qualitative research. Lifecycle measures version/SDK distribution, unknowns, migration confirmation, deprecation acknowledgement, exceptions, ownership freshness. Economics include logical-operation/effect unit cost, fan-out/egress, capacity headroom, toil/support, migration/externalized and retirement cost. Guard against chatty volume, unused downloads/registrations, hidden p50 tails, tickets suppressed by inaccessible support, sampled rare consumers, retries counted as demand, and teams omitting artifacts; publish provenance/denominators.

### Answer 3

Consumer outcome ratio is $117/120=0.975=97.5\%$. A 99.9% time-based objective over 30 days allows $0.001\times30\times24\times60=43.2$ bad minutes, assuming the stated eligibility and time model; it does not authorize three failed settlements or describe request-based budgets. The evidence contradicts aggregate request success: the dominant consumers/ordinary traffic mask a critical cadence. Block retirement or major evolution affecting the old behavior, investigate all three workflows and telemetry health, restore/adapter/migrate them, verify settlement business effects and target path, and add a segmented month-end completion SLI. Record exception only through proper risk authority. Aggregate request SLO may remain a supporting signal, not the readiness verdict.

### Answer 4

Treat object authorization as non-compensable security work with security authority and product/engineering delivery; it is not outscored by feature popularity. Reliability toil competes based on SLO/error-budget/incident/capacity evidence and protects the offer. SDK onboarding is product adoption work if target consumers demonstrably fail there. Fund partner migration and predecessor retirement together because compatibility/support/cost/risk persist until exit. Reject in-place breaking naming cleanup; freeze new bad use and use additive/versioned migration only if lifecycle value exceeds consumer cost. The filter proceeds when consumer outcome evidence, strategic fit, security/capacity/compatibility, opportunity cost, and delivery readiness support it. Maintain a vector decision record, reserved health/lifecycle capacity, named authorities, hypotheses, sequencing/dependencies, and outcome/reversal criteria rather than one score or loud-client vote.

### Answer 5

Inventory exact contracts/runtime/generated SDKs/docs, all logical consumers/owners/use cases and identity mappings, partner agreements/contacts, quarterly schedules, DR/replay/backup/rollback, regions, SLO/incidents, security/privacy/data obligations, dependencies/suppliers, costs/capacity/quotas, decisions/exceptions, credentials/access/signing, portal/support/on-call, and known unknowns. Map old and new accountable product/service/domain/security/support roles with deputies/escalation; both sides attest, access and catalog/contact update atomically, and history remains. For each consumer prove replacement contract/access, generated client/config, representative semantic/security/limit/recovery tests, target business effect, old-use cessation after full cadence, and notice/acknowledgement; rehearse quarter-end and DR. Validate replacement SLO/capacity/cost, state/data migration, rollback, terminal behavior, incident/support, telemetry health, reference/artifact retention, revoked credentials/routes, and audit. Unresolved partner/dormant/unknown paths receive explicit bounded risk or block retirement.
