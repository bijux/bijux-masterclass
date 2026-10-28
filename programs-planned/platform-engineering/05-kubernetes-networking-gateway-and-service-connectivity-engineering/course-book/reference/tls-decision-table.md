# TLS decision table

| Path | Accepted Atlas baseline | Identity proved | Remaining boundary |
|---|---|---|---|
| client → Gateway | HTTPS with hostname verification | public `atlas.example.invalid` listener | client authentication/authorization belongs elsewhere |
| Gateway → API | plaintext HTTP on controlled cluster path | no TLS backend identity | NetworkPolicy/workload controls; backend TLS deferred |
| workload → external dependency | HTTPS with hostname and peer validation | approved external service name | egress owner, redirects, response limits |

A future backend TLS release must add hostname, CA, SNI, rotation, health, and failure policy. Do not apply a BackendTLSPolicy to a backend that does not expose the corresponding TLS contract.
