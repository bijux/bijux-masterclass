# MetricRail Security Model

## Deployment limitation

The teaching service does not implement authentication or TLS. It must bind only to a trusted interface or operate behind an authenticated encrypted proxy. Exposing it directly to an untrusted network is outside the supported deployment model.

## Assets

- aggregate integrity;
- tenant separation;
- service availability;
- configuration and credentials;
- release artifact integrity;
- operational diagnostics.

## Boundaries and controls

### TCP input

Controls: line limit, UTF-8 validation, command grammar, identifier policy, finite numeric values, queue and connection bounds, public error redaction.

### Offline files

Controls: metadata size check, input byte limit, physical-line context, record count limit, no partial output.

### Operator environment

Controls: explicit configuration validation, no shell execution, no secrets in version output, trusted binding policy.

### Build and dependencies

Controls: lockfile, exact teaching-release versions, advisory review, feature review, build-script review, source and artifact digests.

## Residual risks

- no authentication or encryption inside MetricRail;
- no durable storage or replication;
- floating-point aggregation is not numerically exact;
- process-level denial of service remains possible within host and proxy limits;
- platform allocator and operating-system behavior are observations, not Rust guarantees.

These risks must be accepted by the deployment owner or addressed outside the course material.
