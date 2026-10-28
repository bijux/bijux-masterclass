# Module 88 Workbook — Security and Supply-Chain Engineering

[Chapter](index.md) · [MetricRail guide](../capstone.md) · [Solutions](solutions.md)

Rust memory safety removes important vulnerability classes, but it does not authorize users, bound resource use, protect secrets, secure dependencies, or make build inputs trustworthy. This workbook treats security as explicit assets, trust boundaries, attacker capabilities, controls, and residual risk.

## Part 1 — Predict

### 1. Assets

List at least eight MetricRail assets. Include more than data confidentiality: consider integrity, availability, release identity, operational credentials, tenant boundaries, and diagnostic evidence.

### 2. Trust boundaries

Draw boundaries for TCP clients, offline files, operator commands, build scripts, dependencies, CI, release storage, runtime filesystem, and operational endpoints. For each, state what untrusted input or privilege crosses.

### 3. Validation versus authorization

A tenant name is syntactically valid and below the length limit. Does that authorize the caller to write that tenant’s metrics? Explain the separate decisions and where each belongs.

### 4. Resource exhaustion

A declared length is checked only after allocating a vector of that size. Diagnose the flaw even in safe Rust. Generalize the rule to lines, queues, cardinality, decompression, retries, and logs.

### 5. Secret exposure

A token wrapper redacts `Debug`, but an error stores the raw token in a `String`. Is the system safe? Trace every representation and sink that must follow the secret policy.

### 6. Dependency surface

Two crates offer the same feature. Crate A has 20 transitive dependencies, default features, and a build script. Crate B has two dependencies and no build script but is less widely used. What evidence belongs in the choice beyond popularity?

## Part 2 — Diagnose and repair

### Case A — Cross-tenant confusion

The aggregate map key uses only metric name, not tenant. Data from two tenants combines correctly according to the type system. Identify the security property violated and repair the domain identity.

### Case B — Unbounded diagnostics

Malformed input is rejected, but the complete line is copied into every error event. Explain confidentiality and availability consequences. Design bounded causal context.

### Case C — CI credential exposure

A pull-request build can execute dependency build scripts while a publishing token is present. Redesign the pipeline using trust levels and least privilege.

### Case D — “Pinned” dependency

The manifest uses an exact direct version, but transitive dependencies and lockfile are ignored. Explain what is and is not pinned, and design a review/update policy.

## Part 3 — Focused exercises

### Exercise 1 — Threat register

For five threats, record asset, actor/capability, entry boundary, precondition, impact, prevention, detection, recovery, and residual risk. Include one availability attack and one build-chain attack.

### Exercise 2 — Input-control order

Design the order for accepting one line: byte bound, UTF-8/grammar, field bounds, numeric parse, authorization, capacity/admission, commit. Explain why expensive work follows cheap rejection.

### Exercise 3 — Dependency policy

Write rules for exact versions/lockfile, feature review, build scripts, native code, licenses, advisories, update cadence, and removal. Distinguish evidence from absolute safety claims.

### Exercise 4 — Secret-safe errors

Design types and tests that preserve diagnostic usefulness without exposing token, payload, path, or tenant data beyond policy.

### Exercise 5 — Abuse-case review

Choose one valid-but-hostile input that passes syntax: maximum line length, high-cardinality identifiers, repeated connection attempts, or a large diagnostic-triggering request. Trace every resource it can consume before rejection or completion. Add preventive bounds, bounded signals, and a recovery action. State the residual kernel, allocator, dependency, or network cost that remains outside the application’s strict control.

### Exercise 6 — Build-chain trust path

Trace one released binary backward through package storage, release job, CI runner, source revision, dependency lockfile, registry sources, build scripts, and toolchain. At every arrow, state what identity or integrity check exists, which credential is present, and what compromise remains possible. Choose the highest-value missing control rather than proposing every security tool at once.

## Part 4 — Independent laboratory

Build the [Attack Surface and Supply-Chain Audit](../../labs/module-08-attack-surface-and-supply-chain-audit/README.md). Review named boundaries and dependencies. Reject duplicate/empty subjects, missing critical controls, non-exact version strings, unreviewed build scripts, and unexamined default features. Findings must be deterministic and severity summaries ordered.

## Part 5 — Capstone transfer

Create a threat model covering listener, parser, tenant/metric identity, store, snapshot, observability, offline input, load generator, build, CI, artifact storage, and runtime permissions. Implement the highest-value controls:

- bound before allocation;
- explicit authorization boundary or explicit single-tenant assumption;
- redacted diagnostics;
- bounded cardinality and queues;
- least-privilege filesystem/network use;
- reviewed exact dependency set and lockfile;
- unprivileged PR checks separated from release credentials;
- deterministic artifact identity.

## Part 6 — Reconstruct and defend

1. What security properties remain outside memory safety?
2. Distinguish validation, authentication, and authorization.
3. Why must bounds be checked before allocation/work?
4. How can observability become an attack surface?
5. Why are build scripts privileged code?
6. What does an exact direct dependency version fail to prove?
7. How do prevention, detection, and recovery complement each other?
8. Defend one residual risk you document rather than claim to eliminate.

### Exercise 6 — Produce a boundary-specific threat review

Choose MetricRail’s TCP ingest boundary. Enumerate assets, attacker-controlled inputs, trust transitions, parser and allocation limits, authentication assumptions, abuse cases, and observable security failures. Include at least one availability attack, one data-isolation failure, one log or metric disclosure, and one dependency or build compromise. For each, state prevention, detection, containment, and residual risk. Separate what the current course product actually implements from controls that would belong to a deployment environment.

### Supply-chain acceptance gate

Record every direct dependency’s exact version, purpose, enabled features, license evidence, advisory status, and update owner. Trace which transitive capabilities enter the binary and which build scripts execute. A clean vulnerability scan is time-bounded evidence, not a permanent safety certificate. The release decision must also consider provenance, reviewability, maintenance status, feature minimization, and the consequences of a compromised build dependency.

