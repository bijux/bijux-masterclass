# Worked Answers — Module 09: Runtime Control Plane, Usage Intelligence, and Support Operations

Use these solutions to audit your reasoning for **Runtime Control Plane, Usage Intelligence, and Support Operations**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why must gateway state derive from approved releases?

Otherwise runtime routes can expose versions or paths the catalog and registry do not recognize. Desired-state synchronization makes drift visible and ties deployment to governance.

The chapter’s decisive distinction is this: The catalog and registry define approved releases; the gateway and runtime expose traffic. The platform generates desired routes from active releases and compares them with current state. Missing, extra, or changed routes are drift. The runtime may temporarily diverge during release, but the change must be associated with a known rollout state rather than becoming invisible configuration.

## 2. Which policies belong at the edge?

Transport security, authentication, coarse request size and rate limits, routing, and bounded metadata. Domain ownership, resource authorization, workflow state, and business retries belong to owning services.

In the cumulative capstone, the rule becomes concrete: The gateway may terminate TLS, authenticate callers, enforce coarse rate and size limits, route by approved release, and attach bounded correlation metadata. It must not decide project ownership, analysis transitions, or tenant resource access. Moving domain authorization to the edge creates duplicated stale policy and makes the gateway a business service.

## 3. Why is route drift dangerous?

Consumers may reach a retired version, an undocumented endpoint, or a route with stale security policy. Drift also makes incidents hard to assign to a release.

A useful way to reason about the boundary is: Suppose the gateway still exposes Analysis HTTP 1.1 after the registry marks it retired. route drift reports an extra or changed route. The platform blocks completion of retirement until the route is removed and monitored. Conversely, an observed emergency route does not become supported simply because traffic exists.

## 4. What is the difference between usage and value?

Usage counts interactions. Value measures successful consumer outcomes, reduced effort, safety, or business results. High usage can reflect retries, errors, or confusing documentation.

The implementation consequence is: The analytics fixture identifies one use of Analysis HTTP 1.1. This supports the lifecycle block from Module 05. It is not the only source; consumer registration and owner confirmation remain necessary. Platform data should improve a decision, not create an illusion of complete observation.

## 5. Why measure deprecated-version traffic?

It identifies migration impact and verifies whether deprecation communication is working. It must be combined with registered consumers because telemetry can miss dormant use.

The important nuance is: Measure active consumers, time to first success, publication lead time, expired exceptions, deprecation traffic, search zero-result rate, support response, and failed handoffs. Segment by API and lifecycle while protecting privacy and metric cardinality.

**Evidence.** Combine contract compatibility, usage and declared-consumer evidence, migration status, notice, owner approval, and rollback before advancing lifecycle.

## 6. What is support routing from catalog metadata?

The platform uses the API or component owner relation to choose the accountable domain team, while platform-specific categories route to the platform team.

Under concurrency or failure, the distinction becomes: Support routes distinguish contract semantics, platform mechanisms, security incidents, and runtime outages. Routing through catalog ownership keeps the accountable domain team visible. The platform team owns portal, registry, and template failures; it should not become the default queue for every API problem.

## 7. Why avoid per-consumer high-cardinality metrics in the runtime data plane?

They can create cost, privacy, and performance risk. Product analytics can use bounded event pipelines or sampled records with retention and access controls.

The design remains honest only if: The platform control plane publishes approved routes, authentication modes, rate classes, and release references. The gateway or runtime data plane applies those edge controls. Domain services still decide ownership, tenant membership, workflow legality, and field authorization. Moving those decisions into gateway configuration would couple the platform to changing business state and recreate a distributed authorization monolith.

## 8. How can a metric become surveillance?

Collecting individual developer behavior beyond a declared product purpose, retaining it unnecessarily, or using it for performance ranking changes an improvement signal into surveillance.

The consumer-facing consequence is: Collect events needed to improve user journeys: discovery query, sandbox creation, credential issuance, first successful workflow, active version use, migration progress, and support outcomes. Use stable consumer or team identity only when necessary, minimize retention, and avoid evaluating individual developer productivity. State the purpose before collection.

## 9. What is a platform SLO?

An objective for the platform service itself, such as catalog freshness, registry publication latency, sandbox creation success, or portal availability. It is distinct from the APIs’ own SLOs.

The operational consequence is: Support categories route differently. Portal, registry, template, and sandbox defects go to the platform team. Contract semantics go to the API owner. Runtime outage follows the component owner. Security incidents escalate to the program authority. These routes have response expectations and can be measured for handoff quality.

## 10. Why track support handoff failures?

They reveal unclear ownership or broken catalog relations. A ticket bouncing between teams is a platform defect even if the underlying API eventually works.

The strongest engineering interpretation is: A support request should carry API reference, release, environment, consumer, correlation evidence, category, and urgency. Platform triage can validate metadata and route the case. Domain teams receive semantic or behavioral issues; platform teams retain portal, registry, sandbox, and template issues.

**Evidence.** Compare desired and observed routes, exercise portal/control-plane outage, inspect product outcomes and deprecated use, and route an incident to the accountable platform or domain owner.

## 11. How should cost allocation be used?

To reveal platform operating trade-offs and high-cost workflows, not to incentivize teams to bypass safety controls. Allocation needs context and transparent methodology.

The defect-oriented view is: Track registry storage, portal search load, sandbox resource consumption, build minutes, and support effort. Cost evidence informs product choices. It should not encourage teams to bypass security or stop collecting essential evidence. Show both cost and value of a capability.

**Evidence.** Require exact catalog, contract, policy, consumer, runtime, documentation, and outcome evidence rather than feature count or portal appearance.

## 12. What does the capstone time-to-first-success metric show?

The reference consumer reaches success 240 seconds after credential issue. This is useful as a baseline; it is not representative production evidence until measured across real users and environments.

Across the Python and TypeScript tracks, the invariant is: The capstone reports five active consumers, a four-minute median from credential issuance to first success in its fixture, one deprecated-version use, and search improvement. These small deterministic numbers prove calculations, not organizational performance. Production decisions require representative windows, confidence, segmentation, and qualitative review.
