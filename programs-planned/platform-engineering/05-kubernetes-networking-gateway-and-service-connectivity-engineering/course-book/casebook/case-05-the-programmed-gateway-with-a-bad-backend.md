# Case 5 — The programmed Gateway with a bad backend

## Incident

The public load-balancer address exists. The Gateway listener reports Accepted and Programmed. The HTTPRoute reports Accepted. TLS for `atlas.example.invalid` succeeds. Requests return `503`.

## The misleading conclusion

Because the Gateway and Route conditions are positive, the application team assumes the Gateway implementation is healthy and blames the API. The infrastructure team assumes that Programmed means the backend path has been validated.

## Investigation

The Route’s parent-specific status is read in full. `Accepted` is true, but `ResolvedRefs` is false for the current generation. The Route references `atlas-api` in another namespace after a refactor, and no matching ReferenceGrant exists in the target namespace.

An older Route generation had a same-namespace backend and was programmed successfully. The `Programmed` condition still refers to an older observed generation during convergence. The public listener is healthy, which explains successful TLS. No authorized backend is available for the current Route.

A second negative request with the wrong hostname correctly fails to attach, proving the listener is not routing everything through a catch-all rule.

## Repair

The target namespace owner evaluates the reference and creates a narrow ReferenceGrant for the exact source namespace, Route kind, Service kind, and target. The team verifies the new `observedGeneration`, `ResolvedRefs`, and backend request. They do not create a cluster-wide grant or move the Service merely to avoid the ownership check.

## Durable change

The release gate now requires:

- all parent-specific conditions current for the Route generation;
- backend reference authorization;
- positive and negative hostname/path matrix;
- Gateway-to-backend NetworkPolicy evidence;
- backend readiness and request evidence;
- no assumption that public listener health proves backend health.

## Lesson

Gateway status describes several negotiated relationships. Programmed infrastructure can coexist with an unresolved backend. Read conditions with generation and ownership context, then prove the backend path separately.
