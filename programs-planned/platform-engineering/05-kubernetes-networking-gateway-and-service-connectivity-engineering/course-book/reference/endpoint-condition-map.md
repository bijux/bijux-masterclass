# EndpointSlice condition map

| Condition | Operational meaning | What it does not prove |
|---|---|---|
| `ready` | endpoint is eligible for ordinary new traffic under normal interpretation | every Node has programmed it; application will remain healthy |
| `serving` | endpoint is still serving, useful during termination semantics | endpoint should receive all new traffic |
| `terminating` | backing endpoint is terminating | connections are already drained or gone |

Aggregate all EndpointSlices for the Service and address family. Record desired generation, slice resource versions, conditions, topology, and data-plane programming generation.

Readiness withdrawal and packet cessation are separated by controller and programming propagation. Existing connections can survive endpoint removal. Measure each interval in the target environment.
