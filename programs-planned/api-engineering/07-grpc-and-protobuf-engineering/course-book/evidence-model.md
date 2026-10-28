# Evidence model

| Evidence | Establishes | Does not establish |
|---|---|---|
| proto text inspection | declared schema and method shape | compiler acceptance or runtime behavior |
| descriptor comparison | machine-readable schema identity and selected compatibility | application behavior |
| golden binary vectors | encoding and old/new parsing for specific messages | network or transaction behavior |
| in-process service tests | deterministic application and protocol schedules | HTTP/2, TLS, proxies, real channel behavior |
| live Python gRPC tests | Python serialization, metadata, status, cancellation, and streams | TypeScript network parity or production infrastructure |
| TypeScript core tests | language-level policy and shared-vector parity | grpc-js transport behavior without dependencies |
| Buf/protoc proof | independent lint, compilation, generation, and breaking rules | security, idempotency, or operational correctness |
| TLS/load-balancer proof | configured network and identity behavior in that environment | every production topology |
| database-backed proof | durable idempotency, leases, and outbox semantics | public contract compatibility by itself |

The final report records `passed`, `failed`, `not-executed`, or `not-applicable`. A missing tool never becomes a synthetic pass.
