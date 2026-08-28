---
module_id: SEPAT-046
program: Software Engineering: Patterns
level: 1
module_number: 46
title: Double Dispatch
status: complete
last_verified: 2026-08-28
---

# Double Dispatch

## One-Page Review

### Governing question

How can behavior depend on the runtime types of two collaborating objects when the host language ordinarily dispatches only on one receiver, while pair coverage, symmetry, fallback, extensibility, effects, and language-specific overload rules remain explicit?

### Essential definitions

- **single dispatch** selects a method implementation primarily from one distinguished runtime receiver type.
- **double dispatch** performs two coordinated dynamic dispatches so the final behavior depends on two runtime object types.
- **multiple dispatch** is language/runtime support that selects a method from the runtime types of multiple arguments directly.
- **overloading** supplies same-named operations with different static parameter signatures; in many languages its selection occurs at compile time and is not double dispatch.
- A **pair matrix** lists left operand variants as rows, right operand variants as columns, and required behavior in each cell.
- **commutative interaction** satisfies (F(a,b)=F(b,a)); **directional interaction** intentionally distinguishes operand order.
- A **fallback** defines behavior for an unsupported/unknown pair, preferably a typed unsupported result rather than silent success.
- **open-world evolution** permits independently introduced variants; **closed-world evolution** coordinates exhaustive updates to a known variant set.
- **ambiguity** occurs when more than one applicable multi-method is equally specific and no deterministic precedence rule selects one.

### Central model, mechanism, or theorem

For runtime variants (A_i) and (B_j), desired operation is matrix (F:A\times B\to R\cup E). In a single-dispatch language, a conventional encoding is

\[
dispatch(a_i,b_j)=a_i.accept(b_j)=b_j.with_i(a_i)=F(A_i,B_j).
\]

The first call selects (A_i.accept); its type-specific callback name exposes (i), and the second receiver dispatch selects (B_j.with_i). This establishes pair selection only when every callback is mapped correctly; it proves neither semantic correctness nor completeness for future variants.

### Critical invariants

- The pair matrix and operand order are explicit; no cell is accidentally delegated to a semantically different pair.
- The first-stage method calls exactly the callback corresponding to its own concrete variant.
- Every supported second-stage receiver implements each required callback with one coherent result/error/effect contract.
- Symmetric pairs either share/canonicalize one implementation or are tested for commutativity; directional pairs retain order.
- Unknown/new variants produce an explicit compatible fallback or force exhaustive coordinated change—never silent omission.
- Nullability, subtype overlap, ambiguous specificity, proxies, version skew, and plugin trust are defined at the dispatch boundary.
- Pair behavior preserves domain invariants and external effects have explicit idempotency, order, transaction, and failure semantics.
- Dispatch success is only routing evidence; it does not establish physics, pricing, geometry, authorization, or safety correctness.

### Common failures

Common failures include confusing static overload resolution with runtime double dispatch, `instanceof` ladders duplicated across variants, a generic callback with casts, swapped row/column meaning, infinite callback recursion, defaults that silently ignore unknown types, missing reverse-order cases, assuming collision is symmetric when velocity/authority makes it directional, subclass ambiguity, quadratic boilerplate for rapidly changing variants, exposing private objects to untrusted plugins, effects executed twice under aliases/retry, and tests that cover types but not results/invariants.

### Compact example

Ship, Rock, and Station each perform a first dispatch that names their own variant and a second dispatch on the counterpart. Three representative pairs select `ship-damaged`, `station-shielded`, and `dock` without runtime type tests.

### Connections

[SEPAT-045](045-role-object.md) varies context-specific facets; [SEPAT-047](../ROADMAP.md) invokes registered listeners through callbacks. Double Dispatch connects to [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md), [Programming Languages: Object-Oriented Programming](../../02-programming-languages-object-oriented-programming/ROADMAP.md), and [Compilers and Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md).

## Governing Question

Does the domain truly own a binary behavior matrix whose correct cell depends on both runtime variants, and what dispatch mechanism makes that matrix complete, evolvable, and auditable in the chosen language?

Double dispatch is useful for collisions, comparison/coercion, export, rendering interactions, and Visitor-like operations. It is unnecessary when one operand owns the behavior, when a map/table is clearer, or when the language already offers safe exhaustive pattern matching or multiple dispatch.

## Why This Matters

In many object-oriented languages, `left.interact(right)` dynamically selects from `left` but an overloaded method for `right` may be chosen from its static type. Developers expecting both runtime types can silently call the generic overload.

A disciplined second dispatch represents the binary matrix without central type tests. The price is matrix growth, callback coupling, evolution pressure, and subtle symmetry/fallback rules. Production code needs the matrix and language semantics in plain sight.

## Prerequisites and Retrieval

You should understand overriding, overloading, subtyping, interfaces, Visitor, matrices, Boolean/error models, and effects. Retrieve these facts:

1. Dynamic method overriding and compile-time overload selection are different mechanisms.
2. A binary operation may be symmetric in value but asymmetric in implementation, authority, or effects.
3. (m) variants on both axes can require up to (m^2) ordered pair behaviors.
4. A base-class fallback trades evolution compatibility for exhaustive detection.
5. Multiple inheritance or overlapping abstract types can make “most specific” ambiguous.
6. Routing to a method does not validate that method's domain result.

## Learning Objectives

After completing this module, you should be able to:

- distinguish single, double, and multiple dispatch from overloading;
- derive a two-stage callback protocol from a pair matrix;
- preserve ordered versus commutative interaction semantics;
- define typed results, unsupported pairs, errors, and evolution rules;
- compare double dispatch with Visitor, pattern matching, multimethods, tables, and coercion graphs;
- handle subclass ambiguity, null/proxy/plugin boundaries, effects, and performance;
- test every matrix cell, callback mapping, symmetry law, version skew, and faults;
- limit correctness claims in geometry, finance, simulation, and high-stakes systems.

## Core Exposition

### Draw the ordered pair matrix

List concrete left variants as rows and right variants as columns. Name the semantic result for every supported ordered cell. Mark unsupported, symmetric, directional, and derived cells explicitly.

Do not start with callbacks. The matrix reveals whether behavior is genuinely binary and whether quadratic growth is acceptable. Sparse matrices often fit a registry/table with an explicit fallback better.

### Separate overriding from overloading

Overriding selects the runtime implementation for a receiver under a previously selected signature. Overload resolution in Java and ordinary C# calls generally selects a signature using compile-time types before runtime receiver dispatch.

Thus `shape.intersect(otherShape)` does not automatically choose `intersect(Circle)` when `otherShape` is statically `Shape`. Confirm exact language rules; `dynamic` in C# changes binding behavior and failure timing.

### Encode the first dispatch

Each concrete first operand implements `interact(other)` by calling the counterpart callback named for itself: `other.withCircle(this)` or `other.withRectangle(this)`. The concrete method body supplies statically precise `this` where overload rules require it.

A copy/paste error that calls `withRectangle` from `Circle.interact` routes every Circle pair incorrectly. A dispatch-matrix test must detect this.

### Encode the second dispatch

The counterpart's runtime class selects its implementation of `withCircle`, completing the pair. All variants implement the same callback family or an explicit versioned subset.

Keep naming/operand orientation consistent. Document whether `receiver.withCircle(circle)` implements `(circle, receiver)` or `(receiver, circle)`. Confusion produces correct-looking but transposed behavior.

### Define result and error types

Avoid unrelated returns such as boolean, mutation, and null across cells. Use one result algebra: `InteractionResult(outcome, effects, diagnostics)` or `Result<Value,InteractionError>`.

Unsupported pair, invalid object state, unavailable data, resource limit, and evaluator failure are distinct. A default callback should return typed unsupported with both stable variant identifiers, not empty success.

### Treat symmetry as a law, not an intuition

Geometric intersection may be symmetric as a set, while collision response is directional when one object is static, damage ownership differs, or normals reverse. Pricing/coercion and authorization are often ordered.

For a commutative operation, canonicalize `(minType,maxType)` or delegate one reverse cell to the authoritative implementation, then property-test (F(a,b)=F(b,a)) including result orientation. Avoid mutual delegation that recurses forever.

### Control the matrix growth

With (m) variants on both axes, an ordered square matrix has (m^2) cells. Symmetry reduces unique off-diagonal semantics but not automatically callback/interface surface. Separate families when most pairs are invalid.

If variants change weekly, a closed callback family imposes broad edits. Consider pattern matching over a sealed algebraic data type, a typed registry, multimethods, or a common representation/algorithm.

### Choose open or closed evolution

Closed-world exhaustive callbacks make a new variant break every implementation at compile/test time, valuable when omission is dangerous. Open-world defaults allow plugins to evolve independently but require explicit unsupported negotiation.

Version the variant vocabulary and protocol. Two plugins that each add a type cannot know their cross-pair semantics automatically; a central registry/adapter or unsupported result is necessary.

### Handle subtype specificity

A subtype may inherit a base callback that is semantically adequate or require its own cell. State whether dispatch distinguishes exact runtime variant or behavioral family. Adding a subtype can change resolution in true multiple-dispatch languages.

Multimethod systems need deterministic “most specific” rules and ambiguity detection. Test diamond/overlapping abstract signatures and do not resolve equal specificity by import order.

### Avoid null and proxy surprises

Null has no runtime receiver method; validate optional operands before dispatch or represent absence with a semantically valid explicit variant. Do not map missing/failed data to a universal fallback.

Lazy/remote proxies may dispatch on proxy class rather than represented domain type or perform surprise I/O in callbacks. Expose stable variant tags or explicit loading boundaries with typed failure and authorization.

### Separate selection from effects

Prefer pair selection that returns a pure decision/effect plan. Applying damage, charging, writing, or publishing inside callbacks couples retry and traversal to dispatch. Shared objects or repeated encounters can duplicate effects.

If cells perform effects, define identity, authorization, transaction, ordering, idempotency, partial failure, cancellation, cleanup, and replay semantics. Dispatch is not a workflow engine.

### Secure extensibility boundaries

Do not hand arbitrary live domain objects/capabilities to untrusted plugin callbacks. Use bounded validated data views and narrow capability interfaces. Allowlist variant/protocol versions and resource budgets.

External type tags are untrusted data, not class names to instantiate. Reject unknown versions or return unsupported; never route to reflection-based arbitrary methods.

### Compare Visitor precisely

Visitor is a structured double-dispatch encoding where the first axis is element variant and the second is visitor/operation implementation. In pair interactions, both axes are often peer domain variants rather than data versus operation.

The same matrix trade-off applies: adding operations/visitors is easy when element rows are stable; adding element variants updates every exhaustive visitor. A collision matrix may change on both axes simultaneously.

### Use language-native mechanisms

Julia selects methods using runtime types of all arguments, so direct multiple dispatch expresses the matrix. Python `singledispatch` dispatches on the first non-self argument, not every argument; stacking/manual tuples requires separate semantics.

Sealed types plus exhaustive pattern matching can represent pair cases centrally. A dictionary keyed by stable `(leftKind,rightKind)` is explicit and data-driven but loses some compiler exhaustiveness unless generated/validated.

### Test selection and semantics separately

Use one sentinel object per variant and make every matrix cell return a unique coordinate; assert exact routing for all ordered pairs. Then test each semantic implementation at its boundaries and invariants.

Test reverse order, same-type pairs, subtypes, unknown/versioned variants, null/absence, invalid state, exceptions, budgets, proxies, plugins, concurrent/reentrant calls, effect idempotency, and evolution. Mutation-test swapped callbacks and fallback-to-success.

## Definitions and Notation

Let runtime type sets (A=\{A_1,...,A_m\}) and (B=\{B_1,...,B_n\}), and ordered behavior matrix (F:A\times B\to R\cup E). Double dispatch encoding has first-stage functions (d_i) and second-stage callbacks (c_{j,i}):

\[
d_i(a_i,b_j)=c_{j,i}(b_j,a_i)=F(A_i,B_j,a_i,b_j).
\]

Coverage requires every supported ordered pair to map to exactly one intended cell. For a commutative domain operation, additionally verify (normalize(F(a,b))=normalize(F(b,a))) over its stated valid domain.

## Mechanisms, Invariants, or Proof Structure

### Double-dispatch design procedure

1. Draw the complete ordered pair matrix and mark support, symmetry, direction, and fallback.
2. Confirm the language's override, overload, multiple-dispatch, pattern-match, and ambiguity rules.
3. Define one first-stage method per concrete left variant and one callback family for right variants.
4. Fix operand orientation and a coherent result/error/effect contract.
5. Choose exhaustive closed evolution or versioned explicit unsupported behavior.
6. Address subtypes, null/proxies, plugins, budgets, authorization, and effect boundaries.
7. Generate or test every coordinate plus semantic boundaries and laws.
8. Reconsider a table, ADT match, multimethod, or common algorithm if matrix growth dominates.

### Executable finite model

The following three-variant interaction performs two dynamic calls for each pair and contains no runtime type tests. It demonstrates only three finite routes, not full matrix correctness, physical collision validity, concurrency, effects, or plugin evolution.

<!-- bijux-verify: {"id":"double-dispatch-interactions","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"ship-rock=ship-damaged\nrock-station=station-shielded\nstation-ship=dock\n","stderr":""}} -->
```python
class Ship:
    def encounter(self, other):
        return other.with_ship(self)

    def with_ship(self, other):
        return "formation"

    def with_rock(self, other):
        return "ship-damaged"

    def with_station(self, other):
        return "dock"


class Rock:
    def encounter(self, other):
        return other.with_rock(self)

    def with_ship(self, other):
        return "ship-damaged"

    def with_rock(self, other):
        return "deflect"

    def with_station(self, other):
        return "station-shielded"


class Station:
    def encounter(self, other):
        return other.with_station(self)

    def with_ship(self, other):
        return "dock"

    def with_rock(self, other):
        return "station-shielded"

    def with_station(self, other):
        return "link"


ship = Ship()
rock = Rock()
station = Station()
print("ship-rock=" + ship.encounter(rock))
print("rock-station=" + rock.encounter(station))
print("station-ship=" + station.encounter(ship))
```

For `ship.encounter(rock)`, runtime Ship selects `Ship.encounter`, which calls `rock.with_ship(ship)`; runtime Rock then selects `Rock.with_ship`. The other traces follow the same two-stage mapping.

## Alternatives and Trade-Offs

- **Single-dispatch virtual method:** simplest when one operand owns behavior and the other's runtime family is irrelevant.
- **Overloads:** clear for statically known argument types; easily mistaken for runtime pair dispatch.
- **Visitor:** organizes stable element variants against growing operations; more structured than peer-pair interactions.
- **Sealed ADT plus pattern matching:** central and exhaustive for closed variants; may form a large pair match.
- **Native multimethods:** directly express multi-argument runtime selection; require specificity/ambiguity/evolution discipline.
- **Typed pair registry/table:** good for sparse/open matrices and generated validation; runtime coverage replaces interface exhaustiveness.
- **Coercion to common representation:** reduces pair cases for numeric/geometry domains; can lose precision/semantics.
- **Strategy/service:** centralizes a family of algorithms and may use explicit type tags; useful when domain objects should stay ignorant.

Choose based on language semantics, change axes, matrix density, and domain ownership—not pattern prestige.

## Failure Modes and Misconceptions

- **“Overloads dispatch twice.”** Static overload selection usually precedes runtime receiver overriding.
- **“Two method calls guarantee correctness.”** A swapped callback can deterministically route to the wrong cell.
- **“Binary means symmetric.”** Ordering may affect ownership, direction, authority, effects, and result orientation.
- **“Defaults are forward compatible.”** Silent no-op/default can conceal a new billing, security, or safety case.
- **“All subtypes inherit safely.”** Exact/family semantics and multimethod ambiguity need explicit decisions.
- **“Visitor and double dispatch are identical.”** Visitor is one structured application with asymmetric data/operation axes.
- **“Plugins compose automatically.”** Independently added types lack cross-pair semantics and trust negotiation.
- **“Dispatch replaces transactions.”** It selects code; effect consistency and retry remain separate.
- **“Quadratic code is unavoidable.”** Common algorithms, symmetry, tables, or representation conversion may compress it.
- **“Passing route tests validates the model.”** Domain equations, constraints, and high-stakes evidence remain independent.

## Worked Examples

### Example 1

A Java variable statically typed `Shape` holds a Circle; an overloaded `intersect(Shape)` is selected before runtime overriding. **Conclusion:** Static argument type can defeat the expected pair selection.

### Example 2

`Circle.interact` mistakenly calls `withRectangle(this)`. Unique coordinate tests fail every Circle row cell. **Conclusion:** Test first-stage callback mapping exhaustively.

### Example 3

Geometric intersection is commutative, but collision normal reverses with operand order. Result normalization flips orientation. **Conclusion:** Define what symmetry means for the result.

### Example 4

Two reverse cells delegate to each other to avoid duplication and overflow the stack. One canonical implementation ends recursion. **Conclusion:** Share symmetry in one direction only.

### Example 5

A new `Drone` reaches an empty fallback and silently suffers no damage. Typed unsupported blocks the simulation/version. **Conclusion:** Unknown pair behavior must be explicit.

### Example 6

Two equally specific multimethod signatures match `(ColoredCircle, TexturedSquare)`. Registration order changes output. **Conclusion:** Ambiguity must fail deterministically.

### Example 7

A sparse conversion matrix has 50 types but only 70 supported edges. A validated pair registry is clearer than 2,500 callbacks. **Conclusion:** Matrix density influences representation.

### Example 8

A proxy's runtime type is `RemoteShapeProxy`, not Circle, and callback triggers network I/O. Explicit loaded shape/version prevents surprise routing. **Conclusion:** Proxies alter type and failure semantics.

### Example 9

Collision callback applies damage, then retry repeats it. Returning an idempotently applied effect plan separates selection from mutation. **Conclusion:** Route first; govern effects explicitly.

### Example 10

A medical compatibility matrix dispatches every donor/recipient type correctly but uses unreviewed clinical rules. **Conclusion:** Pair coverage is not clinical correctness.

## Cross-Program Connections

- **Programming Languages and Semantics:** operational dispatch, overload resolution, subtyping, ambiguity, and pattern matching define selection.
- **Object-Oriented Programming:** overriding, interfaces, Visitor, delegation, and runtime identity implement the encoding.
- **Functional Programming:** algebraic data types, exhaustive pair matches, type classes, and pure effect plans offer alternatives.
- **Compilers and Language Implementation:** method tables, specificity, inline caches, devirtualization, and ambiguity diagnostics implement dispatch.
- **Algorithms and Data Structures:** sparse matrices, pair registries, canonical ordering, and coercion graphs manage case growth.
- **Game and Simulation Engineering:** collision, damage, interaction, and event ordering are common binary domains.
- **Security Engineering:** plugin trust, type-tag validation, capabilities, authorization, and fail-closed unknowns bound extensibility.
- **Distributed Systems:** proxies, version negotiation, retries, idempotency, and partial failure complicate callbacks.
- **Testing and Quality Engineering:** matrix, mutation, property, differential, compatibility, and fault tests provide evidence.
- **Safety and High-Assurance Engineering:** compatibility/interactions need independently validated domain rules beyond routing.

## References

1. Erich Gamma et al., *Design Patterns: Elements of Reusable Object-Oriented Software*, Addison-Wesley, 1994, ISBN 978-0-201-63361-0. Defines Visitor and its double-dispatch collaboration.
2. Oracle, [Java Language Specification, Java SE 25, §15.12 Method Invocation Expressions](https://docs.oracle.com/javase/specs/jls/se25/html/jls-15.html#jls-15.12), accessed 2026-08-28. Defines compile-time method selection and runtime invocation behavior.
3. Microsoft, [C# Language Specification, §12 Expressions](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/language-specification/expressions), accessed 2026-08-28. Defines static/dynamic binding and overload resolution.
4. Julia Project, [Julia Manual: Methods](https://docs.julialang.org/en/v1/manual/methods/), accessed 2026-08-28. Defines method selection using runtime types of all function arguments and ambiguity concerns.
5. Python Software Foundation, [`functools.singledispatch`](https://docs.python.org/3/library/functools.html#functools.singledispatch), Python 3.14 documentation, accessed 2026-08-28. Defines generic functions dispatching on the first argument type.
6. Craig Chambers, [“Object-Oriented Multi-Methods in Cecil”](https://doi.org/10.1007/BF01049002), *ECOOP 1992*, LNCS 615. Provides a foundational treatment of symmetric multi-methods and method lookup.
7. Stefan Muschevici et al., [“Multiple Dispatch in Practice”](https://doi.org/10.1145/1809028.1809029), *OOPSLA 2008*. Empirically studies multiple-dispatch use and language designs.
8. Jeff Bezanson et al., [“Julia: A Fresh Approach to Numerical Computing”](https://doi.org/10.1137/141000671), *SIAM Review* 59(1), 2017. Describes Julia's multiple-dispatch-centered design and specialization.

## Exercises

### Exercise 1

Trace the executable example and state exactly which dispatch and semantic claims it establishes and does not establish.

### Exercise 2

Design a complete ordered pair matrix and callback protocol for three payment instruments with asymmetric transfer rules.

### Exercise 3

Compare double dispatch, sealed pair matching, native multimethods, and a pair registry for a changing plugin ecosystem.

### Exercise 4

Design tests and migration controls for adding one new variant to a versioned double-dispatch protocol.

### Exercise 5

Review a high-stakes compatibility matrix without claiming scientific, clinical, financial, safety, or regulatory correctness.

## Answers to the Exercises

### Answer 1

`ship.encounter(rock)` dynamically selects Ship's first-stage method, which names Ship in `rock.with_ship(ship)`; dynamic receiver Rock selects `Rock.with_ship`, yielding `ship-damaged`. Rock-to-Station calls `station.with_rock(rock)` and yields `station-shielded`. Station-to-Ship calls `ship.with_station(station)` and yields `dock`.

The run establishes three exact two-stage runtime routes and outputs in one Python runtime with no explicit type test. The nine methods suggest a matrix but the run does not cover all cells, wrong/unknown/null/subtypes, symmetry laws, ambiguity, concurrency, proxies/plugins, effects, performance, physical validity, or future compatibility.

### Answer 2

Define ordered types `Card`, `BankAccount`, and `Wallet`; matrix cell means transfer from left source to right destination. Specify every cell as supported rule or typed unsupported, including same-type transfers. Direction matters: card-to-bank might be cash advance, while bank-to-card is bill payment. Result is `TransferPlan(amount, currency, fees, settlement_rail, checks, idempotency_scope)` or typed validation/policy/unsupported error—not an applied transfer.

Each source's `plan_to(target, context)` calls `target.from_card(source,...)`, `from_bank`, or `from_wallet`. Callbacks remain pure over one versioned quote/policy/facts snapshot. Central workflow authenticates/authorizes, validates limits/beneficiary/AML requirements, locks/rechecks balances and rates, persists one idempotent transfer, and applies rail-specific effects. Test all nine coordinates, reversed amounts/fees, currencies/rounding, zero/maximum, insufficient funds, policy unavailable, stale quote, duplicate request, partial settlement, and unknown versions.

### Answer 3

Double dispatch gives interface-enforced callbacks and works in conventional OO code, but every plugin type expands all callback families and independent plugins cannot define mutual cases safely. A sealed pair match is centralized and compiler-exhaustive for a closed core set, but third parties cannot add variants without changing the owner. Native multimethods express open pair methods directly, yet specificity ambiguity, method-table evolution, world/version behavior, and untrusted extension remain governance concerns.

A pair registry keyed by stable versioned kinds fits a sparse plugin ecosystem: plugins declare supported pairs/capabilities, a trusted coordinator validates conflicts, specificity, schemas, resources, and signatures, and unknown pairs return unsupported. It sacrifices compile-time coverage, so startup audits enumerate required coordinates and compatibility tests exercise negotiated versions. Use bounded data views and effect plans; never expose arbitrary host capabilities or allow registration/import order to select conflicts.

### Answer 4

Add stable kind/schema/protocol version and first define its required old-new, new-old, and new-new cells. In a closed protocol, make callbacks exhaustive and update every implementation in one coordinated build; in an open protocol, deploy explicit unsupported negotiation before producers emit the kind. Never let generic success mask it.

Build unique-coordinate matrix tests for all ordered cells, reverse/symmetry properties where applicable, subtype/fallback/unknown-version tests, and semantic boundary/fault tests per new cell. Test mixed old/new binaries, serialized fixtures, plugin capability negotiation, rolling upgrade/downgrade, caches, observability, and effect idempotency. Use shadow/differential evaluation and metrics for unknown/unsupported pairs, controlled rollout and rollback; delete compatibility fallback only after version/support evidence shows it is unused.

### Answer 5

Define both variant taxonomies, ordered-cell meaning, source authorities, valid domains, units, uncertainty/indeterminate states, update cadence, consequences, fallback, timing/resource bounds, and exact claim. Trace every cell to a versioned rule/equation/data source and distinguish unsupported, unavailable evidence, no-match, incompatible, and evaluator error. Review symmetry/direction, specificity, boundary interactions, stale versions, and action-time revalidation.

Evidence requires independent source review/recomputation, full coordinate and boundary/property/metamorphic tests, comparison with authoritative/reference implementations or datasets, uncertainty/error analysis, representative and subgroup/out-of-distribution validation where relevant, adversarial/fault/resource tests, workflow/human-factors trials, monitoring/incident/rollback, and applicable quality/regulatory records. Named domain/scientific/clinical/financial, statistics, safety, security/privacy, verification, human-factors, quality/regulatory, and operations reviewers approve. Correct dispatch and matrix coverage establish no high-stakes correctness or fitness.
