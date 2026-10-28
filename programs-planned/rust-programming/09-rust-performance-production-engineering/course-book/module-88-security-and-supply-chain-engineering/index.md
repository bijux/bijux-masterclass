# Module 88 — Security and Supply-Chain Engineering

**Course 9 · Day 8 · Module 88 of 100**
`██████████████████████░░░` **88/100**

[Program](../../../README.md) · [Course 9](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-08-attack-surface-and-supply-chain-audit/README.md) · [MetricRail guide](../capstone.md)

[← Module 87: Reliability Under Load: SLOs, Load Shedding, Retries, and Degradation](../module-87-reliability-under-load-slos-load-shedding-retries-and-degradation/index.md) · [Module 89: Cargo Profiles, Binary Size, Packaging, CI, and Reproducible Releases →](../module-89-cargo-profiles-binary-size-packaging-ci-and-reproducible-releases/index.md)

## The question

> Which assets, trust boundaries, dependencies, build inputs, and operational capabilities could be abused, and which controls reduce that risk without relying on hidden assumptions?

## Why this comes now

Performance and reliability mechanisms create attack surfaces: parsers allocate, queues retain work, observability stores data, build scripts execute, dependencies expand trust, and operational endpoints reveal state. Rust removes many memory-safety failure modes, but it does not decide authorization, resource limits, secret handling, dependency trust, or deployment privilege.

Module 88 treats security as a system property that spans source, build, artifact, runtime, and operations. Threat modeling is used to prioritize controls, not to produce a ceremonial list.

### Prerequisite bridge

Module 87 established **Reliability Under Load: SLOs, Load Shedding, Retries, and Degradation**. Before continuing, verify that you can test recovery, hysteresis, retry amplification, cold restart, and partial dependency loss. This module preserves that capability and adds the ability to identify assets, actors, trust boundaries, entry points, privileges, and abuse cases for a rust service. Module 89, **Cargo Profiles, Binary Size, Packaging, CI, and Reproducible Releases**, will rely on both when it asks: *How is one reviewed source state transformed into a tested, traceable, appropriately optimized artifact that can be installed and reproduced without hidden local assumptions?*

### Scope boundary

This module owns the reasoning for **security and supply-chain engineering** inside Course 9. The course teaches measurement and operational reasoning, not folklore optimization. It does not promise universal performance rankings, complete security proof, or production readiness from one green pipeline. Every conclusion is scoped to a workload, artifact, environment, and time. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

After completing this module, you will be able to:

- identify assets, actors, trust boundaries, entry points, privileges, and abuse cases for a Rust service
- connect validation, authentication, authorization, confidentiality, integrity, and availability to specific boundaries
- enforce size, time, concurrency, recursion, and decompression limits before expensive work
- design secret handling and diagnostic redaction as lifecycle contracts
- audit direct and transitive dependencies, features, build scripts, licenses, advisories, and provenance
- minimize runtime and build-time privileges through least authority
- create security tests for traversal, injection, resource exhaustion, confused-deputy behavior, and unsafe defaults

## Core model

### The governing model

Security review is a structured adversarial model. Use `asset → actor → boundary → capability → abuse case → control → evidence → residual risk`. Rust removes many memory-safety defects in safe code, but it does not authenticate users, bound allocations, prevent logic abuse, secure dependencies, choose permissions, or redact secrets. Controls must attach to the boundary before the expensive or privileged operation.

### 1. Assets and trust boundaries

Assets include telemetry integrity, tenant isolation, service availability, credentials, release artifacts, and diagnostic data. Boundaries include the network listener, file inputs, environment variables, dependency build scripts, CI credentials, container runtime, and operator endpoints. A diagram is valuable because controls belong at crossings.


### 2. Validation is not authorization

Syntactically valid input may still be forbidden. Authentication establishes identity; authorization decides whether that identity may perform the operation on the named resource. Keep tenant or capability identity separate from user-provided resource names. Avoid confused-deputy designs where the service’s authority is used on behalf of untrusted input without policy checks.


### 3. Resource exhaustion

Safe Rust can allocate until the process dies. Enforce frame, line, field, record, batch, queue, concurrency, retention, and response limits before allocation or expensive parsing. Bound decompression ratios and recursive structures. Apply deadlines to external work and rate or quota policy at the correct identity boundary.


### 4. Secrets and diagnostics

Secrets should have minimal scope, avoid cloning, and never appear in `Debug`, logs, panic messages, metrics, or error responses. Environment variables are convenient but inherited by child processes and sometimes visible through diagnostics. Prefer explicit secret providers in production and test redaction. Zeroization claims require careful scope and do not erase copies outside the wrapper.


### 5. Dependency and feature surface

Every dependency adds code, maintainers, features, build logic, and transitive packages. Review why it exists, which features are enabled, whether defaults are needed, advisories, license policy, MSRV, and update cadence. Build scripts and procedural macros execute during the build and deserve a stronger trust review than ordinary linked code.


### 6. Release provenance and least privilege

A secure source tree is insufficient if artifacts cannot be traced to reviewed inputs. Record source revision, lockfile, toolchain, target, features, and artifact digest. CI credentials should be scoped, short lived where possible, and unavailable to untrusted contributions. Runtime identities should have only required network, filesystem, and operating-system capabilities.

A threat model connects assets to actors through trust boundaries. Each abuse case must name a capability, an affected asset, a precondition, and a control that can be tested or reviewed. Residual risk remains explicit; the absence of a known advisory is not proof that a dependency or configuration is safe.

### A module-specific decision table

| Boundary | Representative abuse | Control and evidence |
|---|---|---|
| network input to parser | oversized or malformed line | pre-allocation length checks and adversarial tests |
| validated record to store | cardinality or identifier-memory exhaustion | independent series and byte limits |
| snapshot request to renderer | amplification and memory peak | bounded output and explicit rejection |
| domain values to diagnostics | secret or payload leakage | redacted `Debug`, bounded codes, log tests |
| dependency resolution to build | compromised or unexpected code | exact versions, lockfile review, feature minimization |
| CI to artifact store | credential or provenance misuse | least privilege, isolated jobs, artifact digests |
| operational endpoint to caller | information disclosure or control abuse | authentication boundary and network policy |

### Working procedure

1. List assets and the damage caused by loss of confidentiality, integrity, or availability.
2. Identify actors, including accidental operators and compromised dependencies.
3. Draw trust boundaries from source through build and runtime.
4. Enumerate abuse cases using attacker capability and product limit, not generic labels.
5. Assign preventive, detective, and recovery controls with tests or review evidence.
6. Minimize dependencies, features, privileges, and diagnostic data.
7. Record residual risks, assumptions, owners, and the event that would require redesign.

### Failure patterns and principled repairs

#### Treating memory safety as a complete security argument.

Memory safety closes one class of exploits; it does not authorize callers or bound resource exhaustion. Complete the threat model at the product boundary.

#### Validating a resource name and assuming the caller is authorized to access it.

A syntactically valid name can still identify a forbidden resource. Keep validation and authorization as separate decisions.

#### Applying limits after allocating from an untrusted declared length.

Checking after allocation lets hostile metadata choose memory consumption. Validate lengths and checked arithmetic before ownership promotion.

#### Deriving `Debug` on structures containing tokens, payloads, or personal data.

Automatic `Debug` can turn internal payloads into persistent logs. Redact domain identifiers and expose only bounded public diagnostics.

#### Adding a dependency because it is popular without reviewing features, build scripts, transitive surface, or maintenance.

Popularity is not dependency review. Inspect features, transitive crates, build scripts, maintenance, advisories, and removal cost.

#### Giving CI and runtime processes broad credentials because isolation is expected elsewhere.

Broad CI or runtime credentials convert one compromise into a larger blast radius. Give each stage only the capabilities it needs.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For identify assets, actors, trust boundaries, entry points, privileges, and abuse cases for a Rust service, construct one positive and one causal negative example. Mark the first decisive fact in the **threat and dependency dossier** and state which evidence could falsify the claim.

2. **Outcome 2.** For connect validation, authentication, authorization, confidentiality, integrity, and availability to specific boundaries, construct one positive and one causal negative example. Mark the first decisive fact in the **threat and dependency dossier** and state which evidence could falsify the claim.

3. **Outcome 3.** For enforce size, time, concurrency, recursion, and decompression limits before expensive work, construct one positive and one causal negative example. Mark the first decisive fact in the **threat and dependency dossier** and state which evidence could falsify the claim.

4. **Outcome 4.** For design secret handling and diagnostic redaction as lifecycle contracts, construct one positive and one causal negative example. Mark the first decisive fact in the **threat and dependency dossier** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

```rust
#[derive(Clone)]
struct Secret(String);

impl std::fmt::Debug for Secret {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        formatter.write_str("Secret([REDACTED])")
    }
}

impl Secret {
    fn expose(&self) -> &str {
        &self.0
    }
}

fn main() {
    let secret = Secret("test-token".to_owned());
    assert_eq!(format!("{secret:?}"), "Secret([REDACTED])");
    assert_eq!(secret.expose(), "test-token");
}
```

For the example, draw the trust boundary before reading code. Mark every value derived from untrusted input and every allocation, lookup, log field, or file path it can influence. Then ask which checks occur before the influenced operation.

A strong repair does more than reject malformed syntax. It bounds valid-but-expensive input, prevents secrets from entering diagnostics, and leaves a stable public error that does not help an attacker infer internal state unnecessarily.

### MetricRail consequence

MetricRail’s threat model covers line-size exhaustion, connection exhaustion, broker saturation, series cardinality, retained identifier bytes, snapshot amplification, malformed numbers, log injection, and supply-chain compromise. The store has separate series and identifier-byte limits because an attacker can exploit either dimension.

Tenant and metric values use redacted debug output. Network errors return stable codes and do not echo input. The load client bounds responses from the server so a testing tool does not become an unbounded allocation path.

The teaching service intentionally omits authentication and TLS. That is a declared deployment boundary, not an invisible assumption: it must run on a trusted interface or behind an authenticated encrypted proxy. The operations security document records this residual risk and the controls required outside the process.

### Prioritize controls by exploit path, not by checklist order

Suppose the threat review identifies three findings: an unauthenticated operational endpoint on a private subnet, a maximum valid snapshot that allocates 7 MiB, and a build dependency with a historical advisory that does not affect enabled features. Severity cannot be assigned from labels alone.

For each finding, trace capability, reachability, impact, and existing controls. The operational endpoint may become critical if the network boundary is weak or if it exposes sensitive state. The snapshot may be acceptable for one request but dangerous when many requests execute concurrently; its risk depends on admission and memory headroom. The advisory requires version and feature analysis before it is called exploitable or dismissed.

Rank work by the complete path. A high-impact issue with no reachable actor may be monitored while a moderate per-request allocation with trivial remote amplification is fixed immediately. Record why the order was chosen, what evidence could change it, and which residual assumption belongs to infrastructure rather than Rust code. This keeps threat modeling connected to actual product decisions.

### Boundary case: a valid input that exhausts a different dimension

MetricRail may enforce `max_series = 100_000` and still be vulnerable if every series uses maximum-length tenant and metric names. A cardinality limit bounds entries, not identifier storage. Conversely, an identifier-byte limit alone does not bound map nodes, aggregate values, or per-entry allocator overhead. Resource security requires independent limits for independent growth dimensions.

The same reasoning applies to snapshots. A request may be syntactically valid and authorized while causing output proportional to the entire store. Limit rendered bytes, bound concurrent snapshot work, and decide whether snapshot pressure degrades only that operation or threatens ingestion. Test maximum valid state, not only one-byte-over parser inputs.

Extend the threat model to the build path. An exact direct dependency version does not freeze transitive dependencies without a reviewed lockfile, and a build script executes with the build user’s capabilities. The release process must record dependency resolution, minimize features, isolate credentials, and distinguish advisory scanning from review of actual exploitability and build behavior.

## Practice sequence

1. Build an asset, actor, boundary, abuse-case, and control table for MetricRail.
2. Complete the Attack Surface and Supply-Chain Audit with both runtime and build-path threats.
3. Test maximum valid and one-byte-over-limit inputs before allocation.
4. Search diagnostic output for raw identifiers, payloads, absolute paths, and credentials.
5. Review every dependency feature and build-time execution path.
6. Write residual risks and deployment assumptions in language an operator can act on.

Use the [workbook](workbook.md) to freeze predictions and complete the causal repairs. Build the module laboratory before reading its reference implementation, then transfer the mechanism into the [MetricRail engineering guide](../capstone.md).

## Ready to continue

Continue only when you can:

- explain why Rust memory safety is not a complete security argument;
- separate validation, authorization, and resource policy;
- identify checks that must occur before allocation or expensive work;
- design redacted bounded diagnostics;
- review dependency, feature, build-script, and CI trust surface;
- state MetricRail’s authentication/TLS limitation and required deployment boundary.

## Primary Rust references

- The RustSec advisory database and `cargo-audit` documentation
- `cargo-deny` documentation for advisories, bans, licenses, and sources
- Cargo documentation for features, build scripts, lockfiles, and package metadata
- OWASP guidance for threat modeling, authentication, authorization, input validation, and resource exhaustion

These references are for verification and deeper lookup after the chapter’s model is understood. The course-book chapter remains the complete learning route for the required concepts.

## Continue

Continue to [Module 89 — Cargo Profiles, Binary Size, Packaging, CI, and Reproducible Releases](../module-89-cargo-profiles-binary-size-packaging-ci-and-reproducible-releases/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
