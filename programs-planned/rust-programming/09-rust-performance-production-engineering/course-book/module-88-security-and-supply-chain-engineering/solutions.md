# Reasoned Solutions — Module 88: Security and Supply-Chain Engineering

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-08-attack-surface-and-supply-chain-audit/README.md) · [MetricRail guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 88: Security and Supply-Chain Engineering**. Compare the reasoning against this question: *Which assets, trust boundaries, dependencies, build inputs, and operational capabilities could be abused, and which controls reduce that risk without relying on hidden assumptions?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Part 1 — Threat reasoning

### 1. Assets

Assets include telemetry confidentiality, aggregate integrity, tenant isolation, service availability, operator credentials, release signing/publishing credentials, source and dependency integrity, artifact provenance, configuration integrity, audit evidence, and recovery capability. Security is broader than secret bytes; corruption or unavailability can be equally damaging.

### 2. Trust boundaries

TCP and files introduce hostile bytes. Operator commands cross an authorization boundary. Dependencies/build scripts execute code during build. CI crosses from untrusted contributions to trusted artifacts. Release storage must preserve integrity and identity. Runtime filesystem/network permissions grant capabilities. Operational endpoints may reveal state. Each boundary needs input, identity, privilege, and resource policy.

### 3. Validation versus authorization

Syntax proves only that the name is well formed. Authentication establishes caller identity. Authorization decides whether that identity may write the named tenant. The parser validates; an application/security boundary authorizes before commit. Conflating the two creates cross-tenant writes with perfectly valid data.

### 4. Resource exhaustion

Safe allocation can exhaust memory. The declared length must be checked against a product maximum and arithmetic limits before reservation. Apply the same rule to decompression ratios, line sizes, nested structures, queue admission, series cardinality, retry counts, and diagnostic payloads: reject cheaply before committing scarce resources.

### 5. Secret exposure

Redacted `Debug` is one layer only. Raw secret values must not enter general errors, traces, metrics, panic text, crash reports, filenames, or persisted diagnostics. Secret types should minimize conversion to ordinary `String`, and sinks should use allowlists. Tests need to exercise all formatting and event paths.

### 6. Dependency surface

Review maintenance, release provenance, advisories, required features, transitive graph, build/native code, unsafe surface, license, update history, MSRV, and whether the dependency is necessary. Popularity is neither proof nor irrelevant; it is one weak signal. Prefer the smallest reviewed capability that meets the contract.

## Part 2 — Repairs

### Case A

The violated property is tenant isolation/integrity. The semantic key must include tenant and metric as validated domain types. Authorization must check the tenant before mutation. Tests should prove identical metric names in different tenants remain distinct and unauthorized writes fail without partial state change.

### Case B

Full-line errors leak customer data and allow attackers to amplify storage/CPU through repeated large invalid lines. Store bounded field/offset/error code and perhaps a short redacted excerpt. Cap event rate/size and keep raw payload only in a separately authorized diagnostic path if policy requires it.

### Case C

Untrusted PR jobs receive no publishing secrets and run in a constrained environment. Release credentials are available only to protected, reviewed refs and narrowly scoped jobs. Build dependencies are still code; cache/artifact promotion crosses a trust boundary and needs digest/provenance checks. Separate validation from publication.

### Case D

An exact direct version constrains Cargo’s direct requirement, while the lockfile resolves the full graph for an application. Features, target-specific dependencies, and build inputs still matter. Commit and review the lockfile, automate advisory checks, inspect diffs and feature changes, test updates, and record why each dependency remains.

## Part 3 — Model answers

### Exercise 1

Example availability threat: attacker sends maximum legal lines at high concurrency. Prevention: connection/line/queue/cardinality bounds and admission. Detection: bounded overload and rejection metrics. Recovery: shed, drain, scale, and investigate source. Residual risk: network bandwidth and kernel resources may still be consumed before application admission. Build threat: malicious build script exfiltrates credentials. Prevention: no secrets in untrusted builds, dependency review, sandboxing. Detection: provenance and egress monitoring. Recovery: rotate credentials and revoke artifacts.

### Exercise 2

Check transport/frame length before allocation, then UTF-8/grammar and per-field lengths, then numeric ranges, then authenticated identity/authorization, then product capacity, then commit. Cheap structural rejection precedes hashing, allocation, dependency calls, and mutation. The exact order may vary, but no expensive or irreversible step should precede the facts needed to justify it.

### Exercise 3

Applications commit a lockfile and pin direct teaching dependencies when reproducibility demands it. Every feature and build script is reviewed; native code and licenses are recorded; advisories are monitored; updates occur on a scheduled route with diff, tests, and rollback; unused dependencies are removed. This policy reduces and makes visible risk; it does not prove dependencies are vulnerability-free.

### Exercise 4

Use newtypes whose `Debug`/`Display` redact, typed error codes with bounded metadata, and explicit `expose_secret` only at the narrow consuming boundary. Tests inject sentinel secrets/payloads, format all public errors/events, and assert the sentinel never appears. Keep detailed sensitive diagnostics behind separate authorization and retention.

## Part 4 — Laboratory review

The review should be deterministic and reject ambiguous inventory. Untrusted boundaries need input/resource controls; privileged boundaries need authorization/least privilege; critical assets need explicit controls. Dependency versions must match the declared exact shape, build scripts require review, and default features require conscious acceptance. A finding is a decision aid, not proof of exploitability.

## Part 5 — MetricRail transfer

The threat model should state whether MetricRail is single-tenant or where authorization occurs. All untrusted sizes are bounded before allocation. Store identity includes tenant and metric. Observability uses redacted bounded fields. CI separates untrusted checks from credentialed release. Artifact manifests bind source, lockfile, toolchain, target, and digest. Runtime permissions are no broader than listener, configuration, and required output.

## Part 6 — Defense

Memory safety does not provide authorization, availability, confidentiality policy, dependency trust, or correct business identity. Validation checks form; authentication checks identity; authorization checks permission. Bounds precede resource commitment. Signals can leak or amplify data. Build scripts execute with build privileges. Direct pins do not describe the full graph or features. Prevention lowers likelihood, detection shortens discovery, and recovery limits duration. Residual risk should be documented when the system cannot fully control an upstream/kernel/network boundary.

## Deep reasoning and transfer

### Decisive model

> Which assets, trust boundaries, dependencies, build inputs, and operational capabilities could be abused, and which controls reduce that risk without relying on hidden assumptions?

Build a **threat and dependency dossier**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Identify assets, actors, trust boundaries, entry points, privileges, and abuse cases for a Rust service.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Connect validation, authentication, authorization, confidentiality, integrity, and availability to specific boundaries.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Enforce size, time, concurrency, recursion, and decompression limits before expensive work.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Design secret handling and diagnostic redaction as lifecycle contracts.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Audit direct and transitive dependencies, features, build scripts, licenses, advisories, and provenance.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Identify assets, actors, trust boundaries, entry points, privileges, and abuse cases for a Rust service.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the threat and dependency dossier.

### Reference implementation comparison

For [Attack Surface and Supply-Chain Audit](../../labs/module-08-attack-surface-and-supply-chain-audit/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In MetricRail, Module 88 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Security and Supply-Chain Engineering**, which relationship decides this question: “Which assets, trust boundaries, dependencies, build inputs, and operational capabilities could be abused, and which controls reduce that risk without relying on hidden assumptions?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to MetricRail?
