## Python Typing + Pydantic Deep Dive

## Module 01: Foundations — Typing as an Engineering Contract

### 01. Mental Model: Guarantees, Tradeoffs, Tool Roles

* Static types as contracts; what types can/can’t prove
* Checker authority: mypy vs pyright; strictness ladder and adoption policy
* Gradual typing: strict boundaries, pragmatic core
* **Lab:** refactor an untyped module to typed boundaries; eliminate obvious `Any`

### 02. Type Algebra: Unions, Literals, Narrowing

* `X | Y`, `Optional[T]`, `Literal`, `Final`, `ClassVar`
* Narrowing: `isinstance`, pattern matching, guard functions
* `TypeGuard` vs `TypeIs`; exhaustiveness with `assert_never`
* **Lab:** implement a parser + narrowing helpers; verify with `reveal_type`

### 03. Function Typing: Callable, Overload, ParamSpec, Concatenate

* `Callable`, `overload`, kw-only correctness, default typing pitfalls
* Signature preservation with `ParamSpec`; context injection with `Concatenate`
* Type parameter defaults for reusable generics
* **Diagram:** decorator signature flow (before/after)
* **Lab:** type a decorator/middleware that preserves signature + return type

### 04. Protocols and Structural Typing

* Nominal vs structural typing; `Protocol` as typed duck typing
* Attribute vs method protocols; optional members; `@runtime_checkable` limits
* Generic protocols, `Self`, composition vs inheritance
* **Diagram:** inheritance vs shape-matching
* **Lab:** replace an inheritance “interface” with a `Protocol` boundary

### 05. Typed Data Shapes: dataclasses, TypedDict, ReadOnly

* `dataclass` patterns (frozen/slots); immutability and value semantics
* `TypedDict`: total/partial, payload modeling, read-only keys
* Enums + `Literal` for finite-state modeling
* **Lab:** model an API payload with `TypedDict` + immutability constraints

---

## Module 02: Advanced Typing — Expressiveness Without Any Leakage

### 01. API Design: Boundaries, Errors, Precision

* “Untrusted input → validated typed domain” boundary adapter pattern
* Typed error modeling: exceptions vs Result-like values
* `Never`/`NoReturn`, precise error contracts, caller-facing strictness
* **Lab:** design a boundary layer that prevents `Any` from entering the core

### 02. Iteration and Async Typing

* `Iterable` vs `Iterator` vs `Generator` contracts; variance implications
* Async types: `Awaitable`, `Coroutine`, `AsyncIterator`, async generators
* Cancellation-safe signatures and typed concurrency interfaces
* **Lab:** type an async pipeline stage end-to-end (inputs/outputs/errors)

### 03. Context Managers, Descriptors, and Hard Protocols

* `ContextManager[T]` / `AsyncContextManager[T]`; yield-based patterns
* Properties/descriptors; `classmethod`/`staticmethod` typing traps
* Resource lifecycles as typed contracts
* **Lab:** implement + type a resource manager (sync + async)

### 04. Stubs, Packaging, and Publishing Typed Code

* `.pyi` stubs, `py.typed`, when to stub vs inline types
* Forward references under deferred annotations; introspection-safe patterns
* Typed public APIs and compatibility expectations
* **Lab:** publish a minimal typed package; stub a dynamic module cleanly

### 05. Ecosystem Reality: ORMs and Scientific Stack

* Django typing strategy (stubs/plugins, typical failure modes)
* SQLAlchemy typing strategy (`Mapped[]`, typed declarative base, query typing)
* Typed repository boundaries to isolate ORM dynamism
* Scientific boundaries: arrays/dataframes (realistic typed interfaces)
* **Lab:** isolate an ORM behind typed repositories + DTOs

---

## Module 03: Modern Annotation Semantics — Introspection, Deprecation, Migration

### 01. Deferred Annotations: Runtime Impact and Migration

* Deferred evaluation model and its effect on reflection-heavy code
* Forward ref handling without brittle `eval` patterns
* Migration strategies for libraries and frameworks
* **Lab:** fix a reflection-based feature to be deferred-annotation safe

### 02. Annotation Introspection with `annotationlib`

* Safe evaluation/inspection of annotations; formats and resolution
* Security/correctness pitfalls of naive introspection
* Building robust registries/DI from annotations
* **Lab:** rewrite an annotation-driven registry using `annotationlib`

### 03. Typed Deprecation and Compatibility Discipline

* Deprecation decorators as part of the type contract
* Enforcing migration warnings in CI and during refactors
* Versioned APIs and compatibility shims
* **Lab:** deprecate an API and enforce usage policy via type checking

### 04. Checker Mastery: Debugging, Performance, Monorepos

* `reveal_type`, narrowing failures, stub gaps, plugin boundaries
* Baseline/ratchet adoption; per-module strictness; error-code hygiene
* Monorepo roots, namespace packages, caching, CI runtime control
* **Lab:** take a legacy package to “strict on public API, pragmatic inside”

### 05. Runtime Type Checking (Optional, Boundary-Only)

* Hybrid enforcement: runtime checks only where types cannot protect you
* Tradeoffs vs Pydantic; avoiding double validation
* Profiling runtime checks and setting budgets
* **Lab:** add boundary runtime checks; measure overhead; keep them minimal

---

## Module 04: Pydantic v2 — Runtime Validation as a Boundary Contract

### 01. Typing vs Validation: Division of Responsibility

* Static typing vs runtime validation: complementary roles
* Choosing BaseModel vs TypeAdapter for boundary parsing
* Error shaping as part of the external contract
* **Diagram:** untrusted input → validation → typed domain core
* **Lab:** parse external JSON into typed domain safely (no `Any`)

### 02. Models and Serialization: Stable External Interfaces

* Fields, defaults, aliasing; strict vs permissive parsing
* `model_dump*`, include/exclude discipline; versioned outputs
* Performance cost centers: validation vs transformation
* **Lab:** stable API serialization + contract tests

### 03. Validators and Computed Fields (Error UX Included)

* `field_validator` / `model_validator`: ordering and invariants
* `computed_field`, caching boundaries, determinism requirements
* Human-grade error messages and structured error reporting
* **Lab:** enforce invariants with clear, stable error outputs

### 04. Discriminated Unions and Versioned Schemas

* Tagged unions as real ADTs; safe branching
* Schema evolution: versioned models, “accept old / emit new”
* Compatibility strategies for long-lived APIs
* **Lab:** implement v1/v2 models + migration layer + tests

### 05. Integration Patterns: Avoiding Double Validation

* Validate once at the boundary; keep core pure/typed
* Typed pipeline specs: config → validate → execute
* Lightweight parsing with TypeAdapter where full models are overkill
* **Lab:** build a typed config-driven pipeline spec

---

## Module 05: Typed Architecture — Systems That Stay Typed

### 01. Domain Modeling with ADTs and Exhaustiveness

* Product/sum types via dataclasses + unions + discriminators
* Pattern matching + exhaustiveness discipline (`assert_never`)
* State machines as typed states (Pending/Running/Done, etc.)
* **Lab:** encode a workflow state machine with exhaustive handling

### 02. Typed Interfaces: FastAPI, CLI, Background Jobs

* Typed request/response models; dependency typing and error shapes
* Typed CLI configs and command contracts
* Typed job payloads/results; event schemas
* **Lab:** shared models across API + CLI + job runner

### 03. Security-Oriented Typing and Validation

* Constrained strings/URLs/paths; explicit trust boundaries
* Preventing injection via constrained domains + validation
* “Do not pass raw strings” patterns
* **Lab:** redesign a boundary to prevent unsafe input propagation

### 04. Performance and Ergonomics: Typed but Not Overengineered

* When to relax types: hot paths, churn-heavy areas, complex generics
* Controlled debt: `cast`, `Any`, `type: ignore[code]` with ownership
* Validation budget: where Pydantic cost is acceptable
* **Lab:** simplify an over-typed area into safer, smaller contracts

### 05. Testing Typed Systems

* Contract tests for schemas/serialization; regression discipline
* Property testing with typed strategies (optional but recommended)
* CI gates: ruff + typecheck + tests as one coherent system
* **Lab:** generate valid/invalid payloads; lock invariants

---

## Module 06: Capstone — Mastering the Full Typing Stack

### 01. Publishing-Grade Typed Library

* Stable public API typing; `py.typed`; compatibility/versioning rules
* Deprecation and migration playbook for users
* **Deliverable:** publish-ready typed library skeleton

### 02. Typed Decorator/Plugin System (ParamSpec Showcase)

* Signature-preserving decorators; middleware correctness
* Protocol-based plugin interfaces; typed registries and dispatch
* **Diagram:** plugin dispatch contract
* **Deliverable:** typed plugin registry with safe invocation

### 03. Typed ETL/Data Pipeline with Pydantic Boundaries

* Parse → validate → transform (pure typed core) → serialize
* Error reporting as data; versioned schema strategy
* **Deliverable:** pipeline with typed boundaries and reproducible outputs

### 04. Typed Persistence Boundary

* ORM isolation behind repositories/DTOs
* Typed query/result contracts; limiting dynamism exposure
* **Deliverable:** persistence module with clean typed interfaces

### 05. Reference Pack: Recipes and Templates

* Recipes: Protocol, ParamSpec/Concatenate, TypeGuard/TypeIs, ReadOnly TypedDict
* Templates: mypy/pyright configs, strictness ladder, monorepo layout rules
* Migration playbook: baseline/ratchet adoption, stub strategy, suppression budgets
