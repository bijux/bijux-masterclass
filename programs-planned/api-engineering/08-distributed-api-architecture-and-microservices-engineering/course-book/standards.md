# Standards and source policy

Distributed architecture combines standardized protocols with system-specific ownership decisions. This course separates the two so that infrastructure vocabulary is not mistaken for an application guarantee.

## Normative inherited contracts

Course 8 preserves the following contracts from earlier courses:

- OpenAPI 3.1.2 executable public HTTP baseline;
- OpenAPI 3.2.0 standards frontier;
- AsyncAPI 3.1.0 Analysis Events API;
- CloudEvents 1.0 course profile;
- Protobuf/gRPC Analysis RPC API 1.0;
- W3C Trace Context propagation profile;
- HTTP semantics and Problem Details;
- OAuth/JWT resource-server and capability profiles;
- database migration history through revision 015.

Course 8 adds a **Distributed Architecture Profile 1.0**. This is a course-owned architecture policy, not an Internet standard. It defines service ownership, data authority, dependency depth, consistency, release skew, extraction, and reconciliation for the Analysis Runs Platform.

## Primary architecture and platform references

Use primary sources for platform behavior:

- NIST SP 800-204, *Security Strategies for Microservices-based Application Systems*;
- Kubernetes documentation for Services, DNS, NetworkPolicy, Deployments, and Gateway API concepts;
- OpenTelemetry documentation for context, traces, metrics, links, and baggage;
- gRPC documentation for deadlines, retries, health, service configuration, and graceful lifecycle;
- PostgreSQL documentation for transaction, locking, and migration behavior used in environment-backed labs.

The course avoids treating vendor blog posts as normative behavior.

## Local policy versus universal rule

Several course rules are deliberate local architecture constraints:

```text
public synchronous depth <= 2
one writer per authoritative fact
no cross-service application database reads
current and previous service version supported during rollout
Notification extracted before Artifact
Analysis Control retained as one authority
```

These are justified by the platform’s invariants and objectives. A different system may choose different limits, but it must supply equivalent evidence.

## Infrastructure does not create application semantics

Examples:

- Kubernetes Service and DNS can provide stable discovery; they cannot decide whether a mutation retry is safe.
- NetworkPolicy can restrict connectivity; it cannot prove tenant authorization.
- A service mesh can provide workload mTLS and traffic policy; it cannot compensate a failed business workflow.
- OpenTelemetry can correlate attempts; it cannot decide which database row is authoritative.
- A broker can redeliver events; it cannot produce exactly-once business effects without application identity and transaction design.
- A gateway can route and normalize; it cannot own run completion merely because every request passes through it.

Every chapter identifies whether decisive evidence belongs to the application, database, message system, network, platform, or operator.

## Citation and update policy

Course prose explains stable concepts. When a lab depends on tool-specific behavior, use the pinned `tool-versions.json` and the official documentation for that version. Do not silently replace a pinned tool with the latest release and assume identical behavior.

The final proof records unavailable environment-backed tools as not executed. A present YAML file is not evidence that a cluster accepted or enforced it.
