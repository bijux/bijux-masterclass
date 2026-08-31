---
module_id: SEPAT-028
program: Software Engineering: Patterns
level: 1
module_number: 28
title: Module and Package Facades
status: complete
last_verified: 2026-08-28
---

# Module and Package Facades

## One-Page Review

### Governing question

How can a library expose a small, stable, coherent public namespace over evolving internals while preventing accidental API expansion, dependency leakage, initialization hazards, and compatibility claims that its language tooling cannot enforce?

### Essential definitions

- A **module/package facade** is a deliberately curated public namespace that re-exports or wraps owned capabilities from internal modules.
- The **public API** is every name, type, behavior, error, side effect, import path, and compatibility promise external consumers may rely on.
- A **re-export** makes an item defined elsewhere available through another public path.
- An **export list** is an explicit declaration of intended public names.
- **type leakage** occurs when a public signature exposes an internal or third-party type, coupling consumers to it.
- A **deep import** reaches through the supported facade into internal paths.
- **import-time behavior** is work performed while a module/package is loaded, before an ordinary operation is called.
- **semantic compatibility** preserves supported meaning, not merely successful compilation or import.
- An **API diff** compares public surface between releases; a **consumer contract test** exercises behavior a named consumer relies on.
- An **architecture rule** mechanically restricts forbidden dependency directions or imports.

### Central model, mechanism, or theorem

Let internal implementation graph be (G=(V,E)), curated public symbols be (A\subset V), and consumer dependency edges be (E_c\subset Consumer\times V). The facade objective is

$$
\forall(c,v)\in E_c:\ v\in A,
$$

while implementation nodes (V\setminus A) may evolve subject to preserving the semantic contracts of (A). Export syntax can constrain reachability, but only tests, review, and version policy address behavioral compatibility. A stable path is useful only when ownership, types, errors, initialization, and dependencies behind it also remain coherent.

### Critical invariants

- Every exported symbol is intentional, documented, owned, and covered by compatibility policy.
- Public signatures use stable boundary types and do not leak internal/provider representation accidentally.
- Internal modules depend toward owned abstractions; the facade does not create cycles or a catch-all dependency hub.
- Import/load performs bounded deterministic work and avoids network, filesystem, secret, thread, and process side effects.
- Exported names, documented names, runtime-accessible names, and generated declarations are reconciled for the language/toolchain.
- Deep imports are prevented where possible, detected otherwise, and migrated explicitly.
- Deprecation preserves a reviewable compatibility window with telemetry or known-consumer evidence.
- API surface size, fan-out, import cost, and change frequency remain bounded and audited.

### Common failures

Common failures include wildcard re-exports, treating an underscore as access control, exposing dependency DTOs or exceptions, circular imports caused by a root facade, import-time registration/network calls, ambiguous duplicate names, re-exporting experimental APIs as stable, maintaining two canonical paths indefinitely, breaking serialization/reflection names, claiming SemVer without an API baseline, letting internal tests become external contracts, and creating a universal `common` package whose facade owns nothing coherently.

### Compact example

A rules package exports only `create_rule` and `evaluate`. It returns an immutable tuple boundary instead of its private `_Rule`. Consumers can change neither engine state nor implementation path, and the explicit export list contains exactly two stable names.

### Connections

[SEPAT-025](025-facade.md) defines a task-oriented subsystem interface; this module applies facade reasoning to language namespaces and build boundaries. [SEPAT-029](../ROADMAP.md) defines application ports, while [SEPAT-030](../ROADMAP.md) controls structural indirection. It also connects to [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md), [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md), and [Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md).

## Governing Question

Which names and semantics should consumers depend on for years, and how can language, build, tests, and release policy keep every other implementation detail replaceable?

A package root is not automatically a facade. The pattern exists when the public namespace is deliberately smaller and more stable than the implementation graph, with enforceable dependency and compatibility rules.

## Why This Matters

Consumers compile knowledge into import paths, type annotations, exception handling, serialized names, reflection, mocks, and operational expectations. Once published, an accidental export can be more expensive to remove than the implementation it exposed.

A curated facade reduces cognitive and change coupling. It can also hide ownership, slow imports, form cycles, and become a release bottleneck. Good boundaries therefore combine language visibility with semantic contracts and evidence.

## Prerequisites and Retrieval

You should understand modules/packages, imports, visibility, type systems, dependency graphs, semantic versioning, testing, and release processes. Retrieve these facts:

1. Public reachability rules differ across Python, Java, Rust, Go, and other languages.
2. A re-export creates another supported path unless policy explicitly says otherwise.
3. Public function signatures include parameter, return, error, generic, callback, and serialization types.
4. Import execution can fail, block, mutate global state, or create cycles.
5. Source compatibility, binary compatibility, behavioral compatibility, and data compatibility are different.
6. Documentation hiding does not necessarily prevent runtime access.

## Learning Objectives

After completing this module, you should be able to:

- inventory the effective public surface of a package;
- design a cohesive facade namespace with stable boundary types;
- compare export/re-export mechanisms across languages;
- prevent deep imports and dependency cycles with architecture checks;
- eliminate harmful import-time side effects;
- plan compatibility, deprecation, and path migration;
- test API shape, behavior, consumer contracts, and packaging artifacts;
- split a facade whose scope or ownership has become incoherent.

## Core Exposition

### Begin with consumer capabilities

List supported consumer goals and group them by one domain owner. Export the smallest vocabulary that expresses those goals without exposing call sequences or storage/provider mechanics.

Do not copy every internal name to the root. A flat namespace can improve discovery only while collisions, unrelated concepts, and ownership remain bounded.

### Inventory the effective API

Inspect explicit exports, public declarations, re-exports, generated bindings, documentation, type stubs/declarations, reflection, serialization names, command entry points, environment variables, exceptions, and examples. Search real consumer imports when available.

The advertised API and technically reachable surface may differ. Record both and decide which is supported; silence is not a compatibility policy.

### Use language mechanisms precisely

Python executes regular-package `__init__.py` and binds its names; conventions such as leading underscores influence intent but do not create a strong security boundary. Java modules export packages and distinguish compile-time/run-time access from reflective opening. Rust items are private by default and `pub use` creates public re-export paths. Go exports identifiers by Unicode uppercase initial.

These rules constrain name access, not semantic stability or authorization. Document the exact supported toolchain behavior and verify packaged artifacts.

### Stabilize boundary types

Return owned value types, protocols/interfaces, or durable primitives. If `public()` returns `vendor.internal.Response`, the vendor API has escaped through the facade even if its import path is hidden.

Translate provider errors into stable categories while preserving internal cause. Avoid lossy “failed” exceptions; consumers need documented retry, validation, and conflict semantics.

### Keep dependency direction inward

The facade may depend on application/domain abstractions and compose internal implementations. Internals should not import the facade merely to reuse its names; that creates cycles and reverses ownership.

Place shared boundary types in an owned contract module when necessary, not a vague common bucket. Enforce allowed edges with compiler modules, package visibility, dependency analysis, or import tests.

### Make import boring

Import/load should define names and inexpensive immutable metadata. Avoid connecting to services, reading mutable configuration, discovering plugins across a network, starting threads, acquiring locks, registering global handlers repeatedly, or constructing large graphs.

Provide explicit initialization/configuration at the composition root. If lazy import is used to reduce cost or cycles, preserve error timing and thread safety deliberately rather than using it to conceal architecture problems.

### Control re-export ambiguity

Each public concept should have one canonical path. Aliases used for migration need a deprecation schedule. Reject collisions rather than letting import order choose a winner.

Re-exporting a type can affect its documented module path, pickling/serialization, reflection, generated client names, and diagnostics. Test observations consumers actually use.

### Govern deep imports

In languages with enforceable privacy/modules, make internals unreachable. Where runtime access remains possible, use internal naming plus static lint/architecture tests, packaging exclusions where appropriate, documentation, and migration telemetry.

Do not claim a deep import is impossible merely because it is undocumented. Known consumers need a measured migration path before internal relocation.

### Define compatibility dimensions

Track source/import, binary/ABI, behavior, error, performance, data/wire, serialization, and operational compatibility. A method that still imports but changes default timeout or ordering may be behaviorally breaking.

Adopt a published version/deprecation policy, but do not treat version numbers as proof. Compare API baselines, run old/new consumer contracts, and inspect release artifacts.

### Test the built package

Test from outside the package using only supported paths. Assert exact exports where the language permits, documentation/type-stub agreement, forbidden deep imports, initialization idempotence, import cost, optional-dependency behavior, and clean-environment installation.

Run compatibility checks against the previous supported release and representative consumers. Source-tree tests can miss missing package data, generated declarations, or build metadata.

### Keep the facade cohesive

Measure exported symbol count, dependency fan-out, owner count, import time, release conflicts, deprecation backlog, and consumer change amplification. Split by durable domain capability when one facade accumulates unrelated concepts.

Do not split solely to meet a numeric threshold. Cohesion and change ownership matter more than an arbitrary number of names.

## Definitions and Notation

Let (A_t) be the supported API symbol set at release (t), with contract (C_t(a)) for each (a\in A_t). A removal is (A_t\setminus A_{t+1}); an addition is (A_{t+1}\setminus A_t). Compatibility cannot be inferred from set equality because (C_t(a)\ne C_{t+1}(a)) may change behavior without changing names.

Let implementation graph (G=(V,E)), public facade set (A\subset V), and permitted dependency relation (E_p). An architecture violation is any actual edge (e\in E\setminus E_p), including internal-to-facade cycles and consumer-to-internal deep imports.

Define facade fan-out (F=|\{v:(a,v)\in E, a\in A\}|), import time distribution (T_{import}), and public-surface growth (\Delta A=|A_{t+1}|-|A_t|). These are diagnostic measures, not universal quality thresholds.

## Mechanisms, Invariants, or Proof Structure

### Boundary design procedure

1. Identify supported consumers, goals, and domain owner.
2. Inventory advertised and technically reachable surface.
3. Choose canonical names and owned boundary types.
4. Define allowed dependency graph and initialization behavior.
5. Implement explicit exports/re-exports for the target language.
6. Add external API-shape, architecture, import, and artifact tests.
7. Establish compatibility baseline, version, and deprecation policy.
8. Measure surface/fan-out/import cost and review every addition.

### Executable mechanism

This single-file Python demonstration uses an explicit export list and functions that return an owned tuple boundary instead of the private implementation object. A real package would place private implementation and public facade in separate modules and test the built distribution.

<!-- bijux-verify: {"id":"package-facade-exports","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"exports=create_rule,evaluate\nrule=minimum:10\n8=False 12=True\n","stderr":""}} -->
```python
__all__ = ["create_rule", "evaluate"]


class _Rule:
    def __init__(self, name, threshold):
        self.name = name
        self.threshold = threshold


def create_rule(name, threshold):
    if threshold < 0:
        raise ValueError("threshold must be nonnegative")
    return (name, threshold)


def evaluate(rule, value):
    implementation = _Rule(rule[0], rule[1])
    return value >= implementation.threshold


public_names = sorted(__all__)
minimum = create_rule("minimum", 10)
print("exports=" + ",".join(public_names))
print("rule=" + minimum[0] + ":" + str(minimum[1]))
print("8=" + str(evaluate(minimum, 8)) + " 12=" + str(evaluate(minimum, 12)))
```

The tuple is intentionally simple, not a universal API design. Production code would use a validated immutable owned type, richer errors, separate modules, type declarations, and compatibility tests.

### Proof obligations

Prove public-surface claims against the built artifact and language rules, not directory naming. Prove dependency restrictions by analyzing all relevant compile/import/runtime paths. Behavioral compatibility still requires specifications and tests; identical export sets are insufficient.

The snippet proves exact local output only. It does not prove Python access restriction, packaging correctness, binary compatibility, or long-term semantic stability.

## Alternatives and Trade-Offs

| Approach | Benefit | Main risk |
|---|---|---|
| Curated root facade | simple discovery and stable path | collisions and root coupling |
| Explicit subpackage APIs | domain ownership and scalable namespaces | more paths for consumers |
| Direct implementation imports | full capability and less wrapper code | high structural coupling |
| Generated facade | consistency for large schemas | generator becomes compatibility authority |
| Service/API boundary | stronger deployment separation | network failure and operational cost |
| Plugin/service-provider interface | extensibility without direct implementations | lifecycle/version discovery complexity |
| Monorepo internal visibility | coordinated evolution | false assumptions when extraction occurs |

Choose the narrowest boundary that matches real ownership and deployment. A facade should not conceal a missing domain decomposition.

## Failure Modes and Misconceptions

### “Everything in the root is public”

That may be technically true in some runtimes but is poor governance. Declare, document, and test the supported set explicitly.

### “Underscore means private”

It is often a convention, not enforcement. Use tool-supported boundaries and architecture checks, and avoid security claims based on naming.

### “Re-exporting hides the dependency”

Provider types, exceptions, behavior, and serialization can still leak. Translate to owned contracts.

### “Import cycles require lazy imports”

Sometimes laziness is appropriate, but cycles often expose reversed dependency or misplaced shared types. Correct ownership first.

### “No removed names means compatible”

Defaults, side effects, ordering, errors, timing, serialization, and performance can break consumers while the same names remain.

### “SemVer proves safety”

A version communicates intent. Only baselines, contract review, tests, and consumer evidence support compatibility claims.

### “One facade improves every library”

Small cohesive packages may already have a clear public surface. An extra forwarding layer can add only indirection.

## Worked Examples

### Example 1

A Python package uses explicit `__all__`, but a consumer deep-imports `_engine`. Static checks detect it; migration introduces a supported operation before relocating internals. **Conclusion:** Export intent and reachability require separate controls.

### Example 2

A Java module declares `exports api` but not `impl`; a public API method returns `impl.Record`. Compilation reveals an unusable leaked type. An owned exported interface replaces it. **Conclusion:** Package export alone cannot repair signature leakage.

### Example 3

A Rust crate keeps implementation modules private and `pub use`s two stable types at its root. API diffing detects a newly public generic bound after refactoring. **Conclusion:** Re-export paths still carry full type contracts.

### Example 4

A Go package capitalizes an experimental helper, unintentionally exporting it. Consumers adopt it before documentation. A review gate compares exported identifiers and requires stability classification. **Conclusion:** Language naming can make accidents durable.

### Example 5

Package import reads secrets and connects to a database. Documentation builds and command completion fail offline. Explicit `configure` and injected clients make import deterministic. **Conclusion:** Public namespaces should be cheap and side-effect-light to load.

### Example 6

Two wildcard re-exports publish `Config` from unrelated modules; order selects one in a dynamic environment. Qualified domain names and collision tests remove ambiguity. **Conclusion:** Flat discovery must not destroy meaning.

### Example 7

A facade returns a vendor exception. A dependency upgrade changes its hierarchy and breaks consumer catches. Stable owned error categories retain causes internally. **Conclusion:** Errors are part of the public type surface.

### Example 8

A symbol keeps the same name but changes a default timeout from 30 seconds to one. API shape passes while batch consumers fail. Behavioral contract tests and release notes classify the change. **Conclusion:** Surface equality is weaker than semantic compatibility.

### Example 9

A root package grows to 300 exports owned by nine teams and imports every subsystem. Domain subpackage facades reduce fan-out; a small root offers only navigation-level entry points. **Conclusion:** Facade cohesion must evolve with ownership.

### Example 10

A medical library re-exports an unvalidated dose-conversion helper as stable. The export is withdrawn from the release candidate pending dimensional, clinical, and regulatory review. **Conclusion:** Namespace convenience cannot establish high-stakes correctness.

## Cross-Program Connections

- **Programming Languages and Semantics:** name resolution, module systems, visibility, linking, and initialization define enforcement.
- **Object-Oriented Programming:** stable interfaces, value types, substitutability, and encapsulation shape exports.
- **Software Design and Domain Modeling:** bounded contexts and ubiquitous language determine facade cohesion.
- **Software Methods and Evolution:** consumer discovery, deprecation, compatibility, and migrations govern change.
- **Software Architecture:** dependency direction, modularity, build boundaries, and cycles determine replaceability.
- **Testing and Quality:** API baselines, external tests, consumer contracts, and artifact tests provide evidence.
- **Delivery and Reliability:** packaging, release versions, rollback, deprecation telemetry, and supply chain matter.
- **Security Engineering:** visibility is not authorization; deep paths, reflection, plugins, and unsafe initialization expand attack surface.
- **API and Service Engineering:** schema evolution and generated clients share compatibility disciplines.
- **Platform Engineering:** internal developer platforms often need curated SDK facades with clear team ownership.

## References

1. David L. Parnas, [“On the Criteria To Be Used in Decomposing Systems into Modules”](https://dl.acm.org/doi/10.1145/361598.361623), *Communications of the ACM* 15(12), 1972. Establishes information-hiding decomposition around design decisions likely to change.
2. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Provides the Facade pattern's intent and consequences.
3. Python Software Foundation, [The import system](https://docs.python.org/3/reference/import.html), Python 3.14 language reference, accessed 2026-08-28. Documents regular package initialization and namespace binding.
4. Oracle, [Java Language Specification, Java SE 25, Chapter 7](https://docs.oracle.com/javase/specs/jls/se25/html/jls-7.html), 2025. Defines packages, modules, exports, qualified exports, opens, and accessibility.
5. Rust Project, [Visibility and privacy](https://doc.rust-lang.org/stable/reference/visibility-and-privacy.html), Rust Reference, accessed 2026-08-28. Defines private-by-default items and public re-export behavior.
6. Go Project, [The Go Programming Language Specification](https://go.dev/ref/spec), accessed 2026-08-28. Defines packages, import dependencies, and exported identifiers.
7. Tom Preston-Werner, [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html), 2013. Defines version-number rules relative to a declared public API.

## Exercises

### Exercise 1

For the executable example, identify advertised, technically reachable, and semantically supported surface. Explain why `__all__` is not access control.

### Exercise 2

Design a module facade for a rules library with parsing, validation, evaluation, persistence adapters, and experimental optimization. Specify owned types and dependency direction.

### Exercise 3

Create a language-neutral compatibility audit covering source, binary, behavior, data, serialization, documentation, and initialization.

### Exercise 4

Plan migration from widespread deep imports to two cohesive public subpackage facades without breaking known consumers or freezing internals forever.

### Exercise 5

Review a package-facade proposal for an unfamiliar clinical calculation library without claiming correctness or regulatory suitability.

## Answers to the Exercises

### Answer 1

Advertised surface is `create_rule` and `evaluate`, as listed in `__all__`. The tuple shape, validation error, threshold comparison, and output behavior are also semantic contracts if documented/supported. Technically reachable names in the same module additionally include `_Rule`, `public_names`, and imported/built-in bindings depending on runtime inspection; leading underscore and `__all__` guide import/discovery conventions but do not prevent explicit access.

The snippet establishes exact list and evaluation output only. It does not establish separate-module privacy, package artifacts, type-stub/docs agreement, compatibility, or security. External package tests and architecture tooling must define and verify supported versus reachable paths.

### Answer 2

Expose `parse(source)->RuleDraft`, `validate(draft, context)->ValidatedRule|ValidationErrors`, and `evaluate(validated, facts, context)->Decision` through an owned `rules.api` facade. Make boundary values immutable, versioned where serialized, and free of parser AST, database records, or optimizer types. Stable error categories retain internal causes and source locations.

Domain validation/evaluation owns rule semantics. Parser implements an inbound adapter to `RuleDraft`; persistence implements a port owned by the application/domain boundary. The facade orchestrates but does not import a concrete database. Experimental optimization remains private behind an evaluator interface and must be observationally checked against the reference semantics before activation. Internals depend on owned contracts, never on facade re-exports. Architecture tests reject facade-to-provider leaks, internal-to-root cycles, and consumer deep imports; external contract tests use only public paths.

### Answer 3

Record a versioned baseline of public names, paths, signatures, generic/trait bounds, constants, error types, visibility, and platform/architecture binaries. Compare compiled ABI where applicable. Behavioral contracts cover defaults, ordering, error mapping, side effects, concurrency, deadlines, determinism, and performance budgets. Data/wire checks cover schema, unknown fields, migrations, encodings, and backward/forward readers. Serialization checks include stable type/name tags and old fixtures.

Build documentation and type declarations from the release artifact and compare them with runtime/compiler exports. Test clean install/import, import idempotence/cost, optional dependencies, offline behavior, and supported platforms. Run prior and current representative consumer suites against the candidate. Classify every difference, require owner approval and version/deprecation action, and retain reports. Equal symbol sets never waive behavioral review.

### Answer 4

Inventory actual deep imports from source search, build telemetry where lawful, dependency graphs, support cases, and named consumer outreach. Cluster them into cohesive capabilities and establish two owned public subpackages with stable boundary types. Add characterization/consumer tests for existing behavior before moving implementations.

Introduce public paths first; keep old paths as thin deprecated aliases where feasible, with warnings that do not break production logs and a documented removal release. Provide automated rewrites and migration examples. Prevent new deep imports through lint/architecture rules, while allowing an explicit temporary exception ledger with owner and expiry. Migrate internal consumers, then external cohorts; compare behavior and packaged artifacts. Remove aliases only after the stated compatibility window and evidence that known consumers moved. Do not expose internals merely to preserve every accidental use; classify unsupported paths honestly and provide goal-level replacements.

### Answer 5

Define each calculation's clinical purpose, inputs with units/reference ranges, patient/population applicability, contraindications, provenance/version, rounding, uncertainty, output interpretation, and failure behavior. Keep internal formulas and vendor structures behind owned validated boundary types, but do not use hiding to prevent independent inspection. Import must not load mutable clinical policy or contact services implicitly; configuration/formulary/version selection is explicit and auditable.

Evidence requires authoritative clinical requirements and traceability, independent dimensional/numerical recomputation across boundaries, reference datasets with provenance, property/metamorphic tests, floating/decimal and rounding analysis, missing/extreme/conflicting inputs, population limitations, version/migration validation, static analysis, independent code/formula review, usability/human-factors review, cybersecurity/privacy analysis, and controlled release/rollback. Named clinicians, pharmacists/laboratory specialists as applicable, clinical informaticists, statisticians, software verification, quality, regulatory, security/privacy, and operations authorities approve. The facade, tests, and chapter establish no clinical validity, patient safety, or regulatory fitness.
