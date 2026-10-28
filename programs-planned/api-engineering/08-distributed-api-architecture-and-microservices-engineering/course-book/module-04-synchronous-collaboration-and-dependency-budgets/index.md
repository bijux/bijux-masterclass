# Module 04 — Synchronous Collaboration, API Composition, and Dependency Budgets

> **Program stage:** Course 8 of 10 — Distribute ownership deliberately.

> **Central question:** How do we keep synchronous service collaboration bounded so that fan-out, retries, and version skew do not make the public request path fragile?

## Where this module fits

Module 03 produced **Split authoritative data ownership, build versioned projections for cross-service reads, define staleness budgets, and prove reconciliation for missing, duplicate, and out-of-order updates**. This module extends that result by asking: **How do we keep synchronous service collaboration bounded so that fan-out, retries, and version skew do not make the public request path fragile?**

The new capstone increment is **Publish an acyclic synchronous dependency graph, one edge-owned deadline budget, bounded fan-out rules, and a gateway composition path that degrades truthfully**. It becomes the prerequisite for **Distributed Workflows, Sagas, Compensation, and Process Managers**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Model the complete synchronous dependency graph and detect cycles.
- Calculate compounded latency and availability across serial and parallel calls.
- Propagate one absolute deadline instead of multiplying independent timeouts.
- Place retries, hedging, and circuit behavior at one accountable layer.
- Design API composition without chatty per-row remote calls.
- Separate unavailable, stale, partial, and authoritative responses explicitly.

## Capstone increment

Publish an acyclic synchronous dependency graph, one edge-owned deadline budget, bounded fan-out rules, and a gateway composition path that degrades truthfully.

## Every synchronous edge consumes the public promise

A remote call is not an implementation detail. It spends user latency and availability. If a public request calls Analysis Control and then Artifact Service serially, the request succeeds only when both services, both client libraries, name resolution, routing, and the network cooperate inside one deadline.

For independent components with availability `A1`, `A2`, and `A3`, a serial path is approximately:

```text
Apath = A1 × A2 × A3
```

Three 99% components do not produce 99%; they produce about 97.03% before considering the network. This arithmetic is not a production SLO calculation, but it exposes the direction of risk.

## Draw the dependency graph

The course permits these synchronous edges:

```text
edge-gateway  -> analysis-control
edge-gateway  -> artifact-service
worker-plane  -> analysis-control
worker-plane  -> artifact-service
```

It forbids:

```text
analysis-control -> notification-service
artifact-service -> analysis-control for per-request authorization
notification-service -> analysis-control for delivery retry
```

The first set has clear caller need and owners. The second set recreates coupling that the extraction was meant to remove.

A synchronous cycle is especially dangerous. If Control calls Artifact and Artifact calls Control, deadlines and retries can amplify, deployments cannot proceed independently, and an outage in either service can deadlock the recovery path. The architecture fitness function rejects cycles before code review.

## One absolute deadline

The edge decides when the result loses value. Child calls receive remaining time, not fresh timeouts.

```text
edge deadline: 1000 ms
  60 ms authentication and parsing
  500 ms Analysis Control budget
  300 ms Artifact composition budget
  140 ms reserve for serialization and network return
```

If Control consumes 480 ms, the gateway cannot still grant Artifact a full 300 ms and keep the public promise. The caller either skips optional artifact enrichment, returns an explicit partial response, or fails according to policy.

## Retry ownership

Only one layer should own a given retry. A gateway, client library, sidecar, service mesh, and callee each retrying can create exponential attempt amplification.

For reads, a bounded retry may be safe if the remaining deadline supports it. For mutations, retry requires durable request identity and an owner that can replay the original outcome. Course 2 established idempotency; Course 8 preserves it across services.

Do not retry `CreateRun` in both gateway and Analysis Control client configuration. Choose one owner, publish the policy, and make attempts observable.

## API composition without remote N+1

A list of 100 runs with two artifacts each must not trigger 201 downstream calls. Options include:

- return run summaries without artifact detail;
- batch artifact identifiers in one request;
- use a local, versioned artifact summary projection;
- expose a separate artifact connection that the client requests deliberately;
- create a report outside the transactional path.

The gateway is a composition boundary, not a license for arbitrary graph traversal. Course 9 will make this constraint even more important.

## Truthful degradation

Consider a run that completed with two artifacts while Artifact Service is unavailable. Incorrect responses include:

```json
{"artifacts": []}
```

and a stale cached list presented as current. A truthful response can be:

```json
{
  "runId": "run-9",
  "state": "completed",
  "artifactIds": ["a-1", "a-2"],
  "artifacts": null,
  "warnings": ["artifactsUnavailable"]
}
```

The run remains authoritative. Artifact enrichment is partial. The contract must permit and describe this state; a gateway cannot invent it after release without compatibility review.

## Parallelism and fan-out

Parallel calls reduce elapsed time from the sum to approximately the maximum, but increase instantaneous demand and failure combinations. Bound concurrency. Prefer one batch call over hundreds of parallel calls. Propagate cancellation when the edge no longer needs the result.

Hedging can reduce tail latency for safe reads, but it duplicates demand and can worsen overload. This course treats hedging as an environment-backed experiment, not a default.

## Service discovery does not remove call semantics

DNS, a registry, Kubernetes Services, or a mesh can choose an instance. The application still owns:

- the method contract;
- deadline;
- idempotency;
- authorization;
- response interpretation;
- ambiguity after timeout;
- reconciliation.

Routing technology cannot decide whether a second attempt is safe.

## Python and TypeScript implications

The reference `DependencyGraph` detects cycles and calculates public depth. Both tracks implement health-aware instance selection. The examples keep routing separate from business decisions: a registry returns an instance, not an authorization result.

## Evidence required before Module 5

Produce an acyclic graph, public depth no greater than two, one absolute budget worksheet, one retry owner per edge, and a composition response that distinguishes partial from authoritative data.

## Latency and availability budgets belong to the caller

A caller knows the remaining objective for its operation. A callee knows only the budget it receives. Therefore the original caller establishes one absolute deadline and each layer derives a smaller child budget.

Suppose the gateway has 900 ms remaining for an artifact response:

```text
validation and routing reserve      50 ms
Control authorization context      150 ms
Artifact retrieval                  550 ms
serialization and response reserve  100 ms
safety margin                        50 ms
-----------------------------------------
total                               900 ms
```

If Control uses 220 ms rather than 150 ms, Artifact receives at most the remaining budget; it does not start a fresh 550 ms timer. Timeout multiplication is one of the most common ways a service graph violates a public objective.

Represent the budget as an absolute monotonic deadline where possible:

```python
remaining = deadline - monotonic_now()
if remaining <= safety_margin:
    raise DeadlineExceeded()
child_timeout = min(policy_cap, remaining - safety_margin)
```

Wall-clock timestamps can jump. Monotonic time is appropriate for local elapsed budgets; wire protocols may carry an agreed timeout or deadline representation.

## Required edges multiply failure exposure

If a public query requires Gateway, Control, Artifact, and Notification synchronously, each component and connection becomes part of the request’s success population. Even high individual availability can produce a weaker journey.

This does not mean every call chain is forbidden. It means the architecture must classify dependencies:

- **required** — failure makes the operation fail;
- **optional** — response may be partial with an explicit marker;
- **deferred** — work continues asynchronously;
- **cached** — bounded-stale data may substitute;
- **hedgeable** — a safe duplicate read may reduce tail latency under strict policy.

The capstone marks artifact enrichment as optional for the run view. Run authority remains available when artifact detail is temporarily unavailable. The response is partial, not silently successful as a complete representation.

## Retry ownership and amplification

Only one layer should normally own retries for a given operation. Imagine:

```text
gateway retries 3 times
client library retries 3 times
service mesh retries 3 times
provider retries database 3 times
```

A single request can create up to 81 attempts before concurrency and hedging. The platform’s Course 4 retry budget still applies after distribution.

A retry policy needs:

- classified transient conditions;
- remaining deadline;
- maximum attempts;
- backoff and jitter;
- idempotency or read-only semantics;
- one declared retry owner;
- attempt telemetry;
- overload suppression.

A gateway cannot infer that an arbitrary downstream mutation is safe to retry. Contract metadata and application effect identity are required.

## API composition without remote N+1

A naive composed endpoint may fetch one run and then call Artifact Service once per artifact. That converts collection size into network fan-out.

Bad:

```text
GET run
for each artifact id:
    GET artifact
```

Better options:

- one batch artifact lookup with bounded identifiers;
- a projection containing the exact summary fields;
- pagination at the owner;
- an asynchronous materialized view;
- a separate endpoint whose cost is explicit.

Batching is not automatically safe. Bound request size, preserve per-item authorization, and return item-level outcomes. A batch that hides one hundred unbounded calls merely moves the loop.

## Parallelism has a budget too

Parallel calls can reduce wall time but increase instantaneous load. Fan-out should be bounded by:

```text
maximum calls
maximum concurrent calls
maximum aggregate response bytes
maximum child budget
cancellation policy
partial result policy
```

When the parent is cancelled, outstanding child requests should be cancelled when the protocol and library support it. Work that must continue independently should have crossed an asynchronous boundary instead of being tied to the request.

## Dependency cycles are operational deadlocks

A synchronous cycle may not deadlock every request, but it creates circular availability and release dependencies.

```text
Control → Artifact → Control
```

Artifact might call Control for authorization while Control calls Artifact for details. During partial outage, both wait or fail together. During release, each needs the other’s new behavior.

Course 8 removes the reverse authorization call with a capability and forbids cycles in `dependency-graph.yaml`. A graph traversal can detect declared cycles, but runtime traces and code review are still needed to find undeclared calls.

## Truthful degradation

A fallback is correct only if it preserves the contract’s meaning. Returning an empty artifact list when Artifact Service is unavailable is misleading because “empty” means the authority has no artifacts. Returning stale authorization data may be unsafe. Returning a cached display label may be acceptable.

For every fallback, state:

- which field or outcome is degraded;
- whether the value is stale, absent, or estimated;
- maximum acceptable age;
- security implications;
- how the response communicates partiality;
- when the fallback is disabled.

Course 8’s `OperationResult` carries `authoritative`, `partial`, and `warnings`. Production APIs may encode these differently, but the semantic distinction must survive.

## Discovery and load balancing do not own call correctness

Kubernetes Services, DNS, client-side resolvers, proxies, and service meshes can locate healthy instances and balance traffic. They cannot decide whether a retry is safe, whether a partial response is truthful, or whether a deadline should be extended. Those remain application and contract decisions.

Discovery may also cache addresses. A client must handle connection failure and re-resolution according to its runtime. Treating a service name as an infallible local function recreates the fallacy distribution was supposed to expose.

## Design exercise: remove one edge

For each synchronous edge in the capstone, ask what would happen if it were removed:

- Gateway → Control is required for authoritative public commands.
- Gateway → Artifact is required only for direct artifact retrieval and optional for run enrichment.
- Worker → Control is required for lease and completion authority.
- Worker → Artifact is required for artifact upload under a bounded capability.

The forbidden reverse edges are as important as the allowed ones. Notification never blocks completion, Artifact does not call Control for each upload, and delivery retries do not require Control availability.

An architecture review should celebrate a removed edge at least as much as an added service.

## Module synthesis

You are ready to leave this module when you can **model the complete synchronous dependency graph and detect cycles, calculate compounded latency and availability across serial and parallel calls, and propagate one absolute deadline instead of multiplying independent timeouts** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **the lab introduces its declared planted defect** and requiring the following oracle: **The graph is acyclic, public depth is at most two, every edge has one deadline/retry owner, and dependency failure never becomes false business data.**

The cumulative platform now includes **Publish an acyclic synchronous dependency graph, one edge-owned deadline budget, bounded fan-out rules, and a gateway composition path that degrades truthfully**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Distributed Workflows, Sagas, Compensation, and Process Managers](../module-05-distributed-workflows-sagas-and-compensation/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
