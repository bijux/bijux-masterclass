# Glossary

**Application outcome** — the domain result independent of transport representation.

**Backpressure** — a mechanism by which downstream capacity bounds upstream production.

**Call credentials** — per-call authentication material, distinct from channel credentials.

**Channel** — a client-side gRPC subsystem that manages resolution, connections, balancing, and call routing.

**Deadline** — the absolute point after which a result no longer has value.

**Descriptor set** — a language-neutral compiled representation of Protobuf files, messages, enums, services, and options.

**Field presence** — whether a field was explicitly supplied, distinct from the value observed after applying defaults.

**Half-close** — one side of a stream finishes sending while still receiving.

**Idempotency** — repeated execution of the same intended mutation produces one logical effect and stable result.

**Metadata** — transport headers associated with a gRPC call; not a replacement for business message fields.

**Method path** — a fully qualified gRPC route such as `/bijux.analysis.v1.AnalysisControlService/GetRun`.

**mTLS** — TLS where both channel peers authenticate with certificates.

**ProtoJSON** — the standardized JSON mapping for Protobuf messages, with compatibility concerns distinct from the binary wire format.

**Reflection** — a gRPC service that exposes descriptors of a running server to authorized tools.

**Retry throttling** — suppression of retries when recent failure indicates that retries would amplify the incident.

**Service config** — client-side configuration for policies such as balancing, health checks, and retries.

**Unknown field** — a serialized field not recognized by the current schema but potentially preserved by binary runtimes.

**Wire compatibility** — the ability of old and new schemas to parse binary data without unsafe reinterpretation.
