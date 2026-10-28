# Module 10 — Schema Evolution, Federation, Governance, and Final Defense

> **Program stage:** Course 9 of 10 — Compose governed client-shaped capabilities.

> **Central question:** How does the graph evolve without breaking clients, erasing service ownership, or becoming an ungoverned platform?

## Where this module fits

Module 09 produced **Deliver resumable run updates with gap and duplicate handling**. This final module consolidates the course by asking: **How does the graph evolve without breaking clients, erasing service ownership, or becoming an ungoverned platform?**

The capstone must now deliver **Approve Graph API 1.0, reject breaking candidates, and publish Course 10 handoff** while preserving every earlier module result. Successful completion establishes the outgoing boundary for the next course or final program defense: **Analysis Graph API 1.0, GraphQL September 2025 schema, persisted operation registry, resolver ownership, demand policy, resumable subscriptions, compatibility gates, and platform-publication metadata.**

## Learning outcomes

- Classify schema evolution by client direction.
- Govern field ownership.
- Evaluate federation without cargo culting.
- Run an operation-aware release gate.
- Publish a sanitized platform handoff.

## Capstone increment

Approve Graph API 1.0, reject breaking candidates, and publish Course 10 handoff.

## GraphQL evolution is operation-aware

A schema diff tells what changed; active-operation validation tells who is affected. Removing an unused field may be safe after proving no supported operation selects it. Adding a required argument breaks existing documents. Changing output from non-null to nullable breaks generated client assumptions. Adding enum or union members requires review because exhaustive clients may fail.

Deprecation is a lifecycle signal, not deletion permission. The registry tracks client versions and operation use so retirement has evidence.

## Schema ownership and review

Every field has a source authority and a graph owner responsible for naming, nullability, cost, and client behavior. Service teams review fields backed by their capabilities; the graph team reviews composition and global consistency. No central committee rewrites domain rules without the owner.

A schema coordinate is the review unit. Changes to `AnalysisRun.artifacts` must include Artifact Service compatibility, authorization, batching, and failure evidence.

## Federation is optional composition technology

Federation can let services publish subgraph schemas and compose a supergraph. It does not automatically create good service boundaries, prevent N+1 calls, or solve field authorization. Entity references add network and version-skew considerations.

The capstone includes optional subgraph sketches to compare ownership-aligned federation with one centrally authored gateway schema. The baseline remains executable without federation tooling. A service should not become a subgraph merely because it exists.

## Release gate

A candidate release passes only when the schema parses in an independent implementation, all active operations validate, field ownership is complete, cost budgets do not regress, authorization tests pass, old clients execute, and partial-response semantics remain truthful. Review-required changes pause for consumer evidence.

The course includes accepted additive, review-required enum, and rejected breaking candidates. The release report records exact reasons rather than one pass/fail flag.

## Course 10 handoff

The final handoff contains the schema, persisted operations, field ownership, client catalogue, query budget, release evidence, and platform boundary. These are the inputs for API discovery, scorecards, lifecycle governance, SDK generation, and developer onboarding.

Private resolver code and service credentials are not platform contracts. The handoff exposes what consumers and platform teams need while preserving implementation ownership.

## Compatibility is measured against operations

GraphQL schemas often evolve additively, but “the schema still validates” is not a complete compatibility claim. The release gate evaluates three populations:

1. the candidate SDL and type-system rules;
2. every active persisted operation from supported clients;
3. runtime behavior and policy for representative old operations.

Removing a field or changing an output type is clearly breaking. Making an input field required breaks callers that omit it. Changing a nullable output to non-null may look stricter but can increase null-bubbling blast radius and break error handling. Adding an output enum value is review-required because generated clients may use exhaustive switches. Changing cost or authorization policy can break operations even when SDL is identical.

The compatibility report therefore classifies:

- breaking schema changes;
- dangerous or review-required changes;
- operation-validation failures;
- policy regressions;
- source-ownership changes;
- runtime behavior changes.

## Deprecation is a managed lifecycle

Marking a field deprecated communicates intent; it does not remove client usage. A complete deprecation record includes:

- replacement capability and migration guidance;
- owning team;
- first deprecated release;
- active operation references;
- client release and support windows;
- usage telemetry;
- earliest removal release;
- final compatibility proof.

Do not deprecate without a replacement when the capability remains necessary. Do not remove based only on low aggregate traffic; a low-volume critical client may still depend on it. Persisted-operation ownership gives a better decision basis than anonymous field counts.

## Schema registry and governance

The capstone registry stores schema release, operation documents, ownership coordinates, cost profile, client declarations, and release decisions. It is a governance system only if ownership and review are real. A folder of SDL files with no release policy is not a registry.

Review responsibilities are distributed:

- source-service owners approve field semantics and authority;
- security owners approve sensitive exposure and policy;
- reliability and performance owners review fan-out and budgets;
- client owners register and retire operations;
- graph owners preserve type-system coherence;
- platform owners automate evidence and publication.

Governance should make the safe path easier, not require a committee for every description edit. Automated checks handle structural rules; humans decide semantic and architectural trade-offs.

## Federation is an optional deployment model

Federation can let multiple teams contribute subgraphs that compose into one graph. It does not create correct service boundaries. A subgraph per database table or per existing service can reproduce the distributed monolith at the schema layer.

Before federating, the platform needs:

- stable ownership of types and fields;
- entity identity and reference rules;
- composition compatibility;
- query planning and fan-out budgets;
- cross-subgraph authorization strategy;
- partial failure and observability policy;
- version-skew and rollout discipline;
- a reason centralized schema contribution is the bottleneck.

The course includes a frontier federation sketch, not a claim that federation is required. Analysis Graph API 1.0 can be implemented by one gateway over independently owned services. Course 10 can decide whether platform scale justifies subgraph publication.

## Avoid the graph-shaped distributed monolith

A graph can hide deep synchronous chains behind one convenient query. If `Project.analysisRuns.artifacts.owner.organization...` crosses many services, the client sees one request while the platform suffers multiplied latency and availability.

The release gate checks dependency depth, distinct services, nested cardinality, and field ownership. Some graph edges should be absent. Others should return identifiers or links rather than recursively compose. A client-shaped API is not a promise of unlimited traversal.

The graph gateway must also avoid becoming the universal workflow engine. Mutations delegate to owners, events remain owned by Course 6 contracts, and service boundaries remain governed by Course 8. GraphQL is an access and composition layer.

## Release sequence

A safe schema release follows:

```text
propose SDL and policy changes
  → validate type system
  → classify schema diff
  → revalidate active operations
  → evaluate cost and fan-out changes
  → run authorization and partial-failure suites
  → deploy runtime able to serve old and new operations
  → publish schema/registry release
  → observe old-client behavior
  → retire only with evidence
```

If a new field requires a source-service release, deploy the source capability before activating operations that select it. If old and new gateway versions overlap, persisted registry and schema routing must support that skew or the rollout must be coordinated explicitly.

The capstone release fixtures include one accepted additive change, review-required changes, and rejected candidates for removed fields, input requiredness, enum narrowing, ownership drift, and budget regression.

## Course 10 handoff

Course 10 receives a sanitized platform handoff, not private runtime state. It includes:

- released schema and schema catalogue;
- persisted-operation catalogue with owners and lifecycle state;
- field ownership and policy coordinates;
- demand-control profile;
- client catalogue;
- release and deprecation policy;
- evidence summary;
- platform-boundary brief.

The handoff makes clear that a developer portal or API platform may publish, discover, generate, score, and govern the graph, but it may not become the source of project, run, artifact, or delivery facts.

## Final architecture defense

The learner must defend one representative query, mutation, and subscription from client document to source authority. The defense must answer:

- why GraphQL is the right interface for this operation;
- which fields cross service boundaries;
- how authorization is enforced;
- how cardinality and cost are bounded;
- what happens under each source failure;
- which consistency model the client observes;
- how the operation is traced and measured;
- how the current and next schema release preserve it;
- what evidence would falsify the claim.

A successful final defense is not a schema tour. It is an argument that the graph remains a truthful, bounded, compatible interface over a distributed platform.

## Worked capstone review

A candidate adds `RunStatus.PAUSED`. Existing documents still validate, but generated clients may use exhaustive switches. The release is review-required until supported clients prove safe handling. Removing `AnalysisRun.status` is rejected immediately because active operations select it.

## Python and TypeScript implications

Both tracks classify changes identically and apply the same release gate. External schema registries and federation tools are additional evidence, not substitutes for old-operation execution.

## Evidence required before the next module

Complete the lab and checkpoint. The decisive artifact is the module report under `reports/module-10-*.json`; prose claims without its oracle do not pass.

## Module synthesis

You are ready to leave this module when you can **classify schema evolution by client direction, govern field ownership, and evaluate federation without cargo culting** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Inject source failure and retry cases** and requiring the following oracle: **invalidates a supported operation;; narrows accepted input unexpectedly;; increases null-bubbling blast radius without migration evidence;; creates unbounded demand or fan-out;.**

The cumulative platform now includes **Approve Graph API 1.0, reject breaking candidates, and publish Course 10 handoff**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Complete the course final defense and outgoing handoff described in [Capstone](../capstone.md). Course 10 may treat only the manifested handoff as settled.
