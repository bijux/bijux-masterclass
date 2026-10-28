# Glossary

**Active operation** — a checked client document still used by a supported client release.

**Batch loader** — a request-scoped mechanism that collapses repeated keys and performs one batched source call.

**Connection** — a course pagination profile containing edges and page information around an ordered list.

**Execution error** — an error raised while resolving or completing a valid operation; it may produce partial data.

**Field coordinate** — a stable reference such as `AnalysisRun.artifacts`.

**Field source** — the service or composition function that supplies a field without changing fact ownership.

**Global identifier** — an opaque graph identifier carrying type and local identity; it is not authorization.

**Graph gateway** — the component that admits and executes graph operations over service-owned capabilities.

**Null bubbling** — propagation caused when a field declared non-null completes with null.

**N+1** — repeated source calls caused by resolving a nested field independently for each parent object.

**Persisted operation** — a pre-registered GraphQL document identified by a stable digest.

**Request error** — parse, validation, variable, or operation-selection failure that prevents execution.

**Resolver** — application code that obtains a field value from its source authority or performs explicit composition.

**Schema coordinate** — a type-system location used by ownership, policy, telemetry, and compatibility checks.

**Service fan-out** — the number and shape of downstream service calls caused by one graph operation.

**Source stream** — the event stream used to produce subscription response events.

**Trusted document** — a persisted operation admitted from a governed client catalogue; unlike APQ, it can restrict arbitrary documents.
