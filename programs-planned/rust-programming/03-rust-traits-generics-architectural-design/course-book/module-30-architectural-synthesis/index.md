# Module 30 — Architectural Synthesis

**Course 3 · Day 10 · Module 30 of 100**
`████████░░░░░░░░░░░░░░░░░` **30/100**

[Program](../../../README.md) · [Course 3](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-10-inspection-platform/README.md) · [Review Engine guide](../capstone.md)

[← Module 29: Public API Evolution](../module-29-public-api-evolution/index.md) · [Module 31: Closures, Capture, and Callable Contracts →](../../../04-rust-functional-programming/course-book/module-31-closures-capture-and-callable-contracts/index.md)

## The question

> Given a real source of variation, how do you choose among enums, generics, trait objects, closures, functions, and ordinary composition?

## Why this comes now

The architectural course concludes by putting all variation mechanisms on one decision table. Enums, generics, trait objects, closures, functions, and ordinary composition solve different problems. The final task is to choose a hybrid architecture and defend each boundary under a changed requirement.

### Prerequisite bridge

Module 29 established **Public API Evolution**. Before continuing, verify that you can produce a semver hazard register and migration plan. This module preserves that capability and adds the ability to map axes of variation before selecting polymorphism mechanisms. Module 31, **Closures, Capture, and Callable Contracts**, will rely on both when it asks: *What does a closure capture, which callable traits does it implement, and what invocation contract should an API require?*

### Scope boundary

This module owns the reasoning for **architectural synthesis** inside Course 3. The course focuses on behavioral and architectural variation. It deliberately postpones iterator-centered functional architecture, macro generation, unsafe systems boundaries, and concurrent execution. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- Map axes of variation before selecting polymorphism mechanisms.
- Combine static and dynamic dispatch without duplicating domain semantics.
- Review an architecture for coherence, dyn compatibility, state validity, and evolution.
- Implement an unseen cross-cutting feature while preserving public contracts.
- Defend the selected architecture and identify a credible alternative.

## Core model

### Architecture begins with a variation map

Before choosing traits or generics, list every changing dimension in the system:

| Dimension | Alternatives | Selection time | Open or closed? | Must coexist? |
|---|---|---|---|---|
| input source | file, memory, standard input | startup | mostly closed | no |
| rule implementation | built-ins, third-party rules | runtime | open | yes |
| output report | text, structured data | startup | closed | no |
| command | check, list, explain | runtime input | closed | one at a time |
| builder state | missing/ready components | compile time | closed | no |

This table prevents “trait everywhere.” Different dimensions deserve different mechanisms.

- Closed commands → enum and exhaustive `match`.
- Fixed source and reporter types → generic parameters or ordinary concrete fields.
- Open heterogeneous rules → trait objects.
- Required construction steps → typestate builder if the complexity is justified.
- One ad-hoc rule operation → closure adapter.

Architecture is the composition of these decisions.

### Use a mechanism decision matrix

For each variation, ask:

#### Is the set of alternatives closed?

If yes, an enum is often the most honest model. It supports exhaustive matching, serialization, and variant-specific data.

#### Is one concrete type selected statically?

Use a generic parameter or `impl Trait`. This preserves associated types and static relationships.

#### Must different implementations coexist in one collection?

A trait object or enum is required. Choose an enum for a closed set; choose `dyn Trait` for an open set with a sufficient erased surface.

#### Does only one operation vary?

Use a function or closure before declaring a multi-method trait.

#### Is the issue protocol phase or authority?

Use typestate for compile-time phase control and capability tokens for authority. Use an enum when state is runtime data.

#### Is the problem foreign integration?

Use an adapter, newtype, conversion trait, or extension trait according to who owns the relationship.

### Combine static and dynamic boundaries deliberately

A review engine can be generic over its outer environment while dynamic internally:

```rust
pub struct Engine<S, R> {
    source: S,
    reporter: R,
    rules: Vec<Box<dyn Rule>>,
}
```

Why this mix?

- one engine instance has one source type and one reporter type;
- the source and reporter expose associated error families useful to the caller;
- rules must be registered from several concrete types and coexist in policy order;
- the rule object surface is small and dyn-compatible;
- construction can accept concrete rules through a generic `register` method and erase them at storage.

A fully generic rule tuple would make policy length and rule types part of the engine type. That may be excellent for a fixed compile-time pipeline but poor for a policy file. A boxed source and reporter would permit runtime switching but erase error families unnecessarily. The hybrid follows actual variation.

### Keep the domain model concrete

Do not abstract stable data merely because behavior varies. `Submission`, `Finding`, `RuleId`, and `EvaluationReport` can be concrete structs and enums with private invariants. Traits belong at behavior boundaries, not every noun.

A common failure is an `ISubmission` trait with getters for every field. It provides no meaningful substitution and makes domain validation harder. Use one validated `Submission` type and adapt external representations into it.

### Layer contracts by responsibility

A coherent engine can have four layers:

1. **Domain** — validated identifiers, submissions, findings, reports.
2. **Contracts** — `Source`, `Rule`, `Reporter`, and their laws.
3. **Application** — deterministic orchestration and ordering.
4. **Adapters** — files, command-line parsing, text rendering, closure rules.

Dependencies point inward. The domain does not import filesystem types. The application knows contracts but not concrete adapters. Adapters translate external errors and data into domain forms.

Do not split files merely to match the layers. Split when a module can own a coherent invariant and public surface.

### Review object surfaces before storage

For every `Box<dyn Trait>` ask:

- why is runtime heterogeneity required?
- which associated types must be fixed?
- what lifetime may implementations capture?
- what ownership pointer is correct?
- is mutation through `&mut self` required?
- should the object be `Send` or `Sync`?
- which methods are intentionally excluded with `Self: Sized`?
- would an enum preserve more useful information?

If the answers are vague, dynamic dispatch was probably selected as an escape from generic signatures rather than from a product requirement.

### Review generic surfaces for propagation

For every type parameter ask:

- who chooses it?
- how long does it remain part of the containing type?
- which bounds are truly required?
- must two parameters be the same concrete type?
- does the associated-type relationship belong to the implementation?
- will callers need to name or store the resulting type?
- would a closure parameter communicate one-operation variation better?

A six-parameter service is not automatically sophisticated. It may expose internal assembly details and make error messages dominate the public API.

### Review public extension policy

Each public trait must be labeled in the design:

- open extension point;
- sealed built-in vocabulary;
- internal implementation detail;
- dyn-facing erased contract;
- static extension trait.

For open traits, write contract tests and reserve coherence space. For sealed traits, explain why external implementation is unsupported. For dyn-facing traits, maintain compatibility fixtures. For static extension traits, keep defaults derived from smaller primitives.

### Handle unseen changes through impact tracing

Suppose the engine must add rule severity and allow filtering reports by minimum severity.

Trace the change:

1. **Domain:** add a severity enum; decide whether it is exhaustive.
2. **Rule contract:** should severity be a method, part of each finding, or policy configuration?
3. **Dynamic use:** does the method remain dyn-compatible?
4. **Defaults:** can existing rules receive a semantically valid default?
5. **Public evolution:** will external implementors break?
6. **Ordering:** where does filtering occur relative to evaluation and reporting?
7. **Adapters:** how is severity parsed and rendered?
8. **Tests:** update contract, compatibility, and deterministic-order tests.

Do not begin by editing whichever file the feature name suggests. Begin with the invariant and variation map.

### Record decisions in plain language

For each major abstraction, write four sentences:

1. **Requirement:** what variation or invariant exists?
2. **Choice:** which Rust mechanism represents it?
3. **Rejected alternative:** what simpler or more dynamic/static choice was considered?
4. **Consequence:** what ownership, dispatch, evolution, or cost follows?

Example:

> Policies contain an ordered, runtime-selected, open set of rule implementations. The engine stores `Vec<Box<dyn Rule>>`. An enum was rejected because third-party rules are an intended extension point. The object surface must remain dyn-compatible, rules are owned by the policy, and concrete rule-only operations are unavailable after registration.

This is enough to make architecture review concrete without producing internal paperwork.

### Final synthesis standard

You understand Course 3 when you can receive a new requirement and do all of the following before coding:

- map the source and timing of variation;
- choose ordinary concrete data where variation does not exist;
- identify who selects every generic and associated type;
- state which implementations may be added by which crate;
- decide whether heterogeneous storage is required;
- preserve protocol validity with an enum, typestate, capability, or runtime check for a stated reason;
- define adapter and error boundaries;
- predict how the public API can evolve;
- reject a more elaborate design when a function, enum, or concrete type is enough.

The goal is not to maximize use of traits. It is to make every abstraction earn its place.

#### Four coordinates

For every varying behavior, record:

1. **Dimension:** what changes?
2. **Selector:** who chooses?
3. **Time:** compile time, construction time, or run time?
4. **Openness:** closed set or downstream-extensible?

Example:

| Dimension | Selector | Time | Openness | Mechanism |
|---|---|---|---|---|
| input source | application constructor | construction | open internally | generic associated-type port |
| rule list | policy file | run time | open through factories | trait objects |
| severity | product domain | run time | closed | enum |
| engine readiness | library programmer | compile time | closed protocol | typestate builder |

The mechanism follows from the map. Starting with “we need a trait” reverses the reasoning.

#### Questions in order

1. Is there real variation?
2. Is the participant set closed?
3. Must values of different concrete types coexist?
4. Is selection known when constructing the caller?
5. Must callers retain associated types or concrete output?
6. Can the contract be dyn-compatible without losing meaning?
7. Who owns implementations under coherence?
8. Which future additions must remain possible?

#### Typical outcomes

- no variation: concrete function or inherent method;
- closed alternatives: enum;
- one implementation selected per instance: generic parameter;
- hidden single concrete return: `impl Trait`;
- runtime heterogeneous behavior: trait object;
- short compile-time protocol: typestate;
- foreign relationship: newtype or extension trait.

A matrix does not replace judgment. It makes the judgment inspectable.

#### Hybrid designs are normal

The capstone uses `Engine<S, R>` for static source/reporter types and `Vec<Box<dyn Rule>>` for runtime rules. This is not inconsistency. The dimensions have different selection times and information needs.

#### Keep domain semantics singular

Static and dynamic paths must not duplicate evaluation meaning. Both should call the same `Rule` contract or a clear adapter. Avoid parallel “generic engine” and “dynamic engine” implementations that drift.

#### Erase late

Validate and construct concrete values before erasure so type-specific errors and invariants remain available. Once erased, execute through the stable minimal contract.

#### Recover only explicit domain data

Do not downcast to reconstruct erased configuration. Preserve rule identity and explanations as contract methods or registry metadata when callers need them.

#### Contract lens

Are semantic laws documented and tested? Are traits coherent rather than method bags?

#### Coherence lens

Who owns each implementation? Do blanket impls overlap or reserve unreasonable space?

#### Dispatch lens

Is static or dynamic selection aligned with requirements? Is type erasure documented?

#### State lens

Can invalid states be constructed? Is typestate complexity justified? Are runtime bridges validated?

#### Ownership lens

Do adapters and trait objects have correct ownership and lifetimes? Are `'static`, `Clone`, or `Send` bounds added without evidence?

#### Evolution lens

Can public traits gain required behavior? Are downstream implementations supported? What changes break method resolution or dyn compatibility?

#### Pedagogy lens

Can a reader explain why the design exists, or only reproduce its syntax?

#### Record decisions while alternatives are visible

A concise ADR includes:

- context and requirement;
- considered mechanisms;
- selected mechanism;
- reasons tied to selection time, openness, and caller knowledge;
- consequences and lost options;
- evidence and tests;
- reconsideration trigger.

Example decision: use `Box<dyn Rule>` for policy-selected heterogeneous rules. Consequences: allocation and erasure at registry boundary; associated metadata must be fixed or moved; runtime extension is possible; exhaustive matching is lost.

#### Avoid victory narratives

An ADR should name a credible alternative and a condition under which it becomes better. This prevents architecture from turning into post-hoc justification.

#### Do not patch the first failing type

When given a new requirement:

1. state the new behavior and invariant;
2. update the variation map;
3. identify which public contract changes;
4. predict coherence and dyn-compatibility effects;
5. write a failing behavioral or compile-time test;
6. make the narrowest architectural change;
7. run the full proof route;
8. update the evolution register and ADR;
9. explain one rejected implementation.

#### Cross-cutting example

Adding rule explanations may affect factory metadata, `Rule`, trait objects, CLI output, tests, and semver. A default method returning an empty string compiles but may violate the product contract. The workflow prevents local convenience from hiding system-wide semantics.

#### A defense is causal

Weak: “We used traits for flexibility.”

Strong: “Policy files select a heterogeneous ordered set of rule implementations at run time. The executor needs only stable identity and evaluation, so `Rule` is dyn-compatible and stored as `Box<dyn Rule>`. Source and reporter are selected once at construction and expose useful associated output/error types, so they remain generic. An enum would improve exhaustive handling but would require modifying the core for every third-party rule.”

#### Required dimensions

- contract and laws;
- implementation ownership;
- selection time and dispatch;
- type erasure;
- invalid-state prevention;
- error and ownership behavior;
- compatibility and migration;
- testing evidence;
- credible alternative.

During a design review, another person may change one requirement during the defense. You must state which mechanism choice would change and why.

Review Engine receives a proposal to make every collaborator a `Box<dyn Trait>` so that “everything is pluggable.” The council rejects it:

- source output and error families are useful to callers and one source is selected per engine;
- reporter output is caller-visible and one reporter is selected;
- the rule list is genuinely heterogeneous and policy-selected;
- severity is a closed domain enum;
- builder states are a short programmer-facing protocol;
- parsing is a concrete adapter, not a replaceable domain capability.

The resulting mixed architecture is smaller and more extensible where extension is real.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For map axes of variation before selecting polymorphism mechanisms, construct one positive and one causal negative example. Mark the first decisive fact in the **architecture decision record** and state which evidence could falsify the claim.

2. **Outcome 2.** For combine static and dynamic dispatch without duplicating domain semantics, construct one positive and one causal negative example. Mark the first decisive fact in the **architecture decision record** and state which evidence could falsify the claim.

3. **Outcome 3.** For review an architecture for coherence, dyn compatibility, state validity, and evolution, construct one positive and one causal negative example. Mark the first decisive fact in the **architecture decision record** and state which evidence could falsify the claim.

4. **Outcome 4.** For implement an unseen cross-cutting feature while preserving public contracts, construct one positive and one causal negative example. Mark the first decisive fact in the **architecture decision record** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

The course capstone is **Review Engine**, a policy evaluation engine with static boundaries, a dynamic rule registry, and typestate construction. Implement an unseen Review Engine extension and update the variation map first. Defend why each boundary uses an enum, generic, trait object, closure, or concrete type. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-10-inspection-platform/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 31 when you can:

- answer the module question—“Given a real source of variation, how do you choose among enums, generics, trait objects, closures, functions, and ordinary composition?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Map axes of variation before selecting polymorphism mechanisms;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [Rust Reference: Traits](https://doc.rust-lang.org/reference/items/traits.html)
- [Rust Reference: Trait objects](https://doc.rust-lang.org/reference/types/trait-object.html)
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)

[← Module 29](../module-29-public-api-evolution/index.md) · [one-hundred-module map](../../../COURSE_MAP.md) · [Module 31 →](../../../04-rust-functional-programming/course-book/module-31-closures-capture-and-callable-contracts/index.md)

## Continue

Continue to [Module 31 — Closures, Capture, and Callable Contracts](../../../04-rust-functional-programming/course-book/module-31-closures-capture-and-callable-contracts/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
