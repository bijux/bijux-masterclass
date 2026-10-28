# Gateway API role map

| Resource | Typical owner | Responsibility |
|---|---|---|
| GatewayClass | platform infrastructure | select controller/class and class-level policy |
| Gateway | cluster/edge operator | listeners, addresses, allowed Routes, certificate references |
| HTTPRoute/GRPCRoute/TCPRoute/TLSRoute | application or service owner | host/path/protocol matches and backend selection |
| ReferenceGrant | target namespace owner | authorize narrow cross-namespace references |
| BackendTLSPolicy | backend/namespace owner with platform review | backend TLS authentication policy |

RBAC and admission must support the intended separation. Status conditions are part of the contract; object existence alone is not completion.
