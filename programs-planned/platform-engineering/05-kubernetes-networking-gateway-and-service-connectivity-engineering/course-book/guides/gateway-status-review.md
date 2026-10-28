# Guide — read Gateway API status as a reconciliation chain

Gateway API status is structured evidence about controller decisions. It is not proof of end-to-end reachability.

## GatewayClass

Confirm that the expected controller accepted the class. A class with no active controller leaves Gateways unprogrammed even though the API objects are valid.

## Gateway

For each listener, inspect:

- `Accepted` and reason;
- protocol, hostname, port, and TLS mode;
- certificate reference resolution;
- allowed Route kinds and namespaces;
- assigned addresses;
- `Programmed` status where reported.

A Gateway can be accepted before an external address exists.

## Route

For each parent reference, inspect:

- whether the parent was found;
- whether listener attachment rules permit the Route;
- hostname intersection;
- `Accepted`;
- `ResolvedRefs`;
- backend validity;
- programmed state.

Status is per parent. One Route can attach to one Gateway and fail on another.

## ReferenceGrant

For a cross-namespace backend or certificate, inspect the grant in the target namespace. The source namespace cannot grant itself access. Broad target grants should be treated as an authority expansion.

## Protocol proof

After status is correct, test the actual listener with the intended hostname, path, method, headers, TLS trust, and negative controls. Record the selected backend. Status without a request proves reconciliation intent only; a request without status can conceal unsupported or stale configuration.
