# Module 09 — Runtime Control Plane, Usage Intelligence, and Support Operations

> **Program stage:** Course 10 of 10 — Operate APIs as an organizational platform.

> **Central question:** How can platform metadata remain connected to the running system and to consumer outcomes without becoming a new domain owner or surveillance system?

## Where this module fits

Module 08 produced **Publish Python and TypeScript client artifacts with contract identity, SBOM, and bounded provenance evidence**. This module extends that result by asking: **How can platform metadata remain connected to the running system and to consumer outcomes without becoming a new domain owner or surveillance system?**

The new capstone increment is **Publish runtime desired state, drift proof, product metrics, and support routing evidence**. It becomes the prerequisite for **Federated Governance, Platform Operations, and Final Defense**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Reconcile approved releases with runtime routes.
- Keep edge and domain policy boundaries explicit.
- Measure onboarding, adoption, migration, and support outcomes.
- Route support through authoritative ownership.
- Apply privacy and cardinality limits to platform analytics.

## Capstone increment

Publish runtime desired state, drift proof, product metrics, and support routing evidence.

## Desired state and runtime truth

The catalog and registry define approved releases; the gateway and runtime expose traffic. The platform generates desired routes from active releases and compares them with current state. Missing, extra, or changed routes are drift. The runtime may temporarily diverge during release, but the change must be associated with a known rollout state rather than becoming invisible configuration.

## Edge policy boundary

The gateway may terminate TLS, authenticate callers, enforce coarse rate and size limits, route by approved release, and attach bounded correlation metadata. It must not decide project ownership, analysis transitions, or tenant resource access. Moving domain authorization to the edge creates duplicated stale policy and makes the gateway a business service.

The capstone route records say `domainAuthz: owner-service` or `graph-and-owner-services`, making the boundary explicit and machine-checkable.

## Platform runtime inventory

A platform view should connect route, release, environment, component, owner, and support path. Runtime discovery can reveal undocumented routes or missing instances, but observed traffic does not define the contract. Reconciliation reports drift and requests owner action; it does not automatically publish observed endpoints as supported APIs.

## Product analytics

Measure active consumers, time to first success, publication lead time, expired exceptions, deprecation traffic, search zero-result rate, support response, and failed handoffs. Segment by API and lifecycle while protecting privacy and metric cardinality.

Avoid using portal visits, entity count, or SDK downloads as primary success. A consumer can download a package and never succeed. Repeated portal visits may indicate confusion. An API count can rise while ownership quality falls.

## Deprecated usage and impact

The analytics fixture identifies one use of Analysis HTTP 1.1. This supports the lifecycle block from Module 05. It is not the only source; consumer registration and owner confirmation remain necessary. Platform data should improve a decision, not create an illusion of complete observation.

## Support as a platform surface

Support categories route differently. Portal, registry, template, and sandbox defects go to the platform team. Contract semantics go to the API owner. Runtime outage follows the component owner. Security incidents escalate to the program authority. These routes have response expectations and can be measured for handoff quality.

## Privacy and bounded evidence

Developer experience analytics can become surveillance if tied to individual performance or retained without purpose. Collect the minimum data needed for product improvement, document access and retention, aggregate where possible, and allow teams to challenge interpretations. The platform exists to reduce friction, not monitor people.

## Worked drift case

Suppose the gateway still exposes Analysis HTTP 1.1 after the registry marks it retired. `route_drift` reports an extra or changed route. The platform blocks completion of retirement until the route is removed and monitored. Conversely, an observed emergency route does not become supported simply because traffic exists.

## Implementation review

The runtime core validates that domain authorization remains with owner services and computes desired/current drift. The analytics core calculates active consumers, median time to first success, and deprecated-version use. The support core resolves a category through explicit routes and catalog ownership.

## Runtime control-plane model

Maintain a mapping from approved API release to environments and routes:

```text
API release digest
→ deployment release
→ environment
→ gateway or broker/RPC endpoint
→ component instances
→ owner and runbook
```

This graph supports rollout, incident, and retirement. A route should never point
at an ambiguous mutable contract. Deployment and API versions remain separate;
one service release can implement several compatible API releases.

## Reconciliation states

Classify drift rather than returning only true or false:

- **planned rollout:** desired and current differ within an approved window;
- **stale runtime:** old release remains after completion;
- **shadow exposure:** route exists without approved catalog release;
- **missing exposure:** active API has no expected route;
- **policy drift:** edge controls differ from approved profile;
- **ownership drift:** runtime component has no current owner.

Route each state to an owner and deadline. An emergency route can be allowed by
incident policy, but it must become declared or be removed.

## Runtime metadata safety

Do not place secrets, complete network topology, or sensitive tenant identifiers
in the broad developer catalog. The platform can hold restricted operational
views and publish safer derived metadata. Audience views should preserve API
identity and owner while redacting sensitive implementation details.

## Product analytics data model

Separate event classes:

- onboarding events: search, sandbox, credential, first success;
- publication events: candidate, failure category, approval, lead time;
- consumption events: active consumer, version, environment, bounded usage;
- lifecycle events: deprecation contact, migration state, retirement;
- support events: category, handoff, response, resolution;
- platform reliability events: catalog freshness, registry latency, sandbox
  creation, portal errors.

Give each event a purpose and retention. Avoid raw request bodies and personal
identifiers when aggregate evidence is enough.

## Outcome definitions

Define success precisely. `first_success` for Analysis HTTP API means an
authorized request produced the documented accepted result and a usable monitor.
A 401 or a syntactically valid 400 is not success. For events, first success may
mean validated consumption and durable checkpoint. For SDK publication, success
means a consumer can install and execute a smoke workflow.

## Cohorts and baselines

Compare similar consumers: new external partner, internal experienced team,
public SDK user, or worker-service owner. A median across unlike cohorts hides
problems. Record platform and contract versions, because improvements may come
from docs, SDK, identity, sandbox, or service behavior.

Course fixtures produce one baseline, not a performance claim. Operational
analytics require enough users and time to avoid overreacting to noise.

## Support operations

A support request should carry API reference, release, environment, consumer,
correlation evidence, category, and urgency. Platform triage can validate
metadata and route the case. Domain teams receive semantic or behavioral issues;
platform teams retain portal, registry, sandbox, and template issues.

Measure wrong-owner handoffs, time to first qualified response, reopen rate, and
repeated issue categories. Repeated questions should improve docs or golden
paths. Support data is a product input, not merely ticket throughput.

## Platform SLO candidates

Examples include:

- 99% of valid catalog changes searchable within five minutes;
- 99.9% of registry reads available monthly;
- 95% of sandbox sessions created within 30 seconds;
- 99% of policy decisions returned within two minutes of evidence arrival;
- 90% of platform support tickets routed correctly on first assignment.

Specify populations and exclusions. Invalid owner descriptors should not count as
catalog ingestion failures, but delayed rejection should count against feedback
latency.

## Cost and capacity

Track registry storage, portal search load, sandbox resource consumption, build
minutes, and support effort. Cost evidence informs product choices. It should not
encourage teams to bypass security or stop collecting essential evidence. Show
both cost and value of a capability.

## Runtime change workflow

Tie runtime changes to release workflow:

```text
approved API release
→ deployment candidate
→ environment rollout
→ health and contract smoke evidence
→ gateway or broker route update
→ traffic observation
→ desired/current reconciliation
→ completion or rollback
```

The platform should know which step is active. Otherwise expected canary drift
looks identical to accidental stale configuration.

## Multi-protocol runtime inventory

HTTP and GraphQL may use gateways and routes. Events use brokers, channels,
consumer groups, and schema identifiers. gRPC uses service endpoints, resolvers,
and method health. The runtime control plane should preserve these native models
while linking each to one catalog API and release digest.

A generic list of URLs cannot describe event retention or RPC reflection. As in
the registry, normalization stops at common identity and ownership.

## Analytics correctness

Deduplicate product events and define event-time rules. A retry should not count
as a second consumer success. A credential reissue should not reset onboarding
unless a new journey begins. Late events may revise a cohort. Version analytics
must use the actual resolved release rather than a client-declared string where
possible.

Publish metric definitions alongside results. If time-to-first-success starts at
portal visit for one cohort and credential issue for another, comparison is
invalid.

## Experiment design

When improving quickstart or sandbox flow, compare representative cohorts and
preserve security and correctness guardrails. A faster flow that grants broader
credentials is not an improvement. Measure support tickets and downstream
integration defects, not only first-call speed.

## Support knowledge base

Convert repeated resolved tickets into task documentation, known-error guidance,
or template fixes. Link articles to API versions and owners. Retire stale support
content with the API lifecycle. Search should distinguish current guidance from
historical incident records.

## Executive portfolio view

A useful high-level view can show:

- active, experimental, deprecated, and retired APIs;
- ownerless or stale evidence blockers;
- active consumers on deprecated releases;
- publication and review lead time;
- onboarding outcome trends;
- platform SLO health and support burden;
- major residual risks.

It should not expose individual developer rankings or reduce unlike APIs to one
league table.

## Evidence before progression

Complete the module laboratory and checkpoint. The evidence must show the decision and its consequences; screenshots of a portal or a green status badge are not sufficient.

## Control plane and data plane

The platform control plane publishes approved routes, authentication modes,
rate classes, and release references. The gateway or runtime data plane applies
those edge controls. Domain services still decide ownership, tenant membership,
workflow legality, and field authorization. Moving those decisions into gateway
configuration would couple the platform to changing business state and recreate
a distributed authorization monolith.

Desired state and observed state have different authorities. The release and
runtime policy produce desired routes. Deployment and gateway systems report
observed routes. Reconciliation compares them and raises missing, extra, or
changed records. It should not silently overwrite either side: an unexpected
observed route may be an incident, while a missing route may be an incomplete
deployment.

## Safe runtime rollout

A platform-generated route change follows the release evidence. Stage it,
validate host and path collisions, apply to a limited environment, observe
errors and authorization behavior, then promote. Rollback restores the previous
route configuration, but cannot undo consumer-visible writes or contract
changes. The runtime layer should retain enough history to explain which release
was active during an incident.

Treat platform outages deliberately. Existing routes should generally continue
from verified configuration if the registry or portal is unavailable. New
publication and unsafe changes fail closed. A read-only snapshot can support
incident lookup, clearly showing its age.

## Product analytics without surveillance

Collect events needed to improve user journeys: discovery query, sandbox
creation, credential issuance, first successful workflow, active version use,
migration progress, and support outcomes. Use stable consumer or team identity
only when necessary, minimize retention, and avoid evaluating individual
developer productivity. State the purpose before collection.

The capstone reports five active consumers, a four-minute median from credential
issuance to first success in its fixture, one deprecated-version use, and search
improvement. These small deterministic numbers prove calculations, not
organizational performance. Production decisions require representative windows,
confidence, segmentation, and qualitative review.

## Support as product evidence

Support routes distinguish contract semantics, platform mechanisms, security
incidents, and runtime outages. Routing through catalog ownership keeps the
accountable domain team visible. The platform team owns portal, registry, and
template failures; it should not become the default queue for every API problem.

Measure first response, resolution, recurrence, transfers, and self-service
avoidance. Repeated questions may indicate missing documentation, confusing
policy, a broken template, or a poor interface. Convert patterns into product
work. A low ticket count can mean excellent self-service or that users have
abandoned the platform; interpret it with adoption and outcome data.

## Implementation drill: explicit runtime drift

Desired and observed state remain separate maps. Reconciliation reports change;
it does not silently make either side authoritative for the other.

```python
def route_drift(desired: list[dict], current: list[dict]) -> dict[str, object]:
    wanted = {item["id"]: item for item in desired}
    seen = {item["id"]: item for item in current}
    missing = sorted(set(wanted) - set(seen))
    extra = sorted(set(seen) - set(wanted))
    changed = sorted(key for key in wanted.keys() & seen.keys() if wanted[key] != seen[key])
    return {"missing": missing, "extra": extra, "changed": changed,
            "inSync": not (missing or extra or changed)}
```

```typescript
function routeDrift(desired: Array<{id: string}>, current: Array<{id: string}>) {
  const wanted = new Map(desired.map(item => [item.id, item]));
  const seen = new Map(current.map(item => [item.id, item]));
  const missing = [...wanted.keys()].filter(key => !seen.has(key)).sort();
  const extra = [...seen.keys()].filter(key => !wanted.has(key)).sort();
  const changed = [...wanted.keys()].filter(key => {
    return seen.has(key) && JSON.stringify(wanted.get(key)) !== JSON.stringify(seen.get(key));
  }).sort();
  return { missing, extra, changed, inSync: !(missing.length || extra.length || changed.length) };
}
```

Production comparison should use canonical structured values rather than
`JSON.stringify`; the compact snippet emphasizes the state model. The complete
course vectors require identical canonical route records.

## Module synthesis

You are ready to leave this module when you can **reconcile approved releases with runtime routes, keep edge and domain policy boundaries explicit, and measure onboarding, adoption, migration, and support outcomes** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Then route one contract question and one portal failure through support** and requiring the following oracle: **Runtime drift is visible. Gateway-owned domain authorization is rejected. Deprecated use appears in migration impact. Support reaches the domain owner for semantics and the platform owner for portal failure.**

The cumulative platform now includes **Publish runtime desired state, drift proof, product metrics, and support routing evidence**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Federated Governance, Platform Operations, and Final Defense](../module-10-federated-governance-and-final-defense/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
