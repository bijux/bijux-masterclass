# Case 2 — The Service with zero usable endpoints

## Incident

`atlas-api.atlas-system.svc.cluster.local` resolves, and the Service ClusterIP accepts SYN packets on some Nodes but returns no application response. Operators inspect the Service YAML: the selector appears correct and three API Pods exist.

## Misleading evidence

The Service object contains no endpoint membership. Its selector is an input to a controller. The existence of matching-looking Pods in a human review is not the same as EndpointSlice state.

## Investigation

The team aggregates every EndpointSlice labeled for `atlas-api`. There are two slices because of address-family and size behavior. One slice contains old terminating endpoints; the other contains current Pod addresses, but all have `ready: false`.

The API Pods are Running, but the startup probe has not completed because a configuration mount contains an invalid value. The liveness probe is deliberately not killing the Pods, and readiness is truthful: the processes are not eligible for traffic.

One Node still has stale programmed endpoints from the previous generation, explaining why connection behavior differs by Node. New Nodes have zero usable endpoints and reject or drop according to implementation behavior. The issue is therefore twofold:

1. desired endpoint eligibility is zero because readiness is false;
2. one Node has not yet removed the old generation.

## Repair

The configuration defect is corrected through the Course 4 rollout process. The team waits for startup and readiness, then observes new EndpointSlice conditions and data-plane generation convergence on every Node. They do not set `publishNotReadyAddresses: true`, because that would bypass the application’s eligibility contract rather than fix it.

## Durable change

The platform records a four-stage Service SLI:

```text
matching Pods
→ Ready endpoint membership
→ programmed endpoint generation
→ successful new connection
```

An alert on “Service has zero Ready endpoints” is separated from “Node programming is stale.” The runbook requires aggregation across all EndpointSlices and address families.

## Lesson

Service existence, selector correctness, endpoint eligibility, and forwarding are different facts. A workaround that publishes unready endpoints can convert a visible outage into requests sent to a process that has declared itself unable to serve.
