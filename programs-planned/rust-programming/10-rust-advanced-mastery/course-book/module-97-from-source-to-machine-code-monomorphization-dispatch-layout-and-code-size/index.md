# Module 97 — From Source to Machine Code: Monomorphization, Dispatch, Layout, and Code Size

**Course 10 · Day 7 · Module 97 of 100**
`████████████████████████░` **97/100**

[Program](../../../README.md) · [Course 10](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-07-dispatch-observatory/README.md) · [AxiomStore guide](../capstone.md)

[← Module 96: Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits](../module-96-auditing-unsafe-abstractions-validity-provenance-drop-panic-and-auto-traits/index.md) · [Module 98: Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration →](../module-98-verification-beyond-examples-compile-fail-property-model-fuzz-miri-and-concurrency-exploration/index.md)

## The question

> How do type-level architecture and compiler decisions become concrete symbols, call paths, layouts, and artifact size—and which observations are stable enough to guide design?

## Why this comes now

Course 9 taught measurement discipline. Module 97 applies that discipline to generic and erased Rust architecture. Generics may duplicate code across instantiations, inlining may remove abstraction boundaries, dynamic dispatch may centralize code behind an indirect call, enums may compile into direct branches, and layout can affect cache behavior. None of these outcomes should be guessed from source syntax alone. You will connect semantic design to a named artifact through a reproducible observation route while keeping implementation observations separate from language guarantees.

Course 3 chose variation mechanisms and Course 9 taught causal measurement. This module connects those source-level choices to a pinned machine artifact without turning observations into language mythology.

Source elegance and machine efficiency are related only through a specific compiler artifact. This module teaches how to move from semantic equivalence to code-generation evidence without smuggling target observations back into language guarantees. The you must preserve a behavioral oracle while inspecting monomorphization, dispatch, layout, inlining, and size.

### Prerequisite bridge

Module 96 established **Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits**. Before continuing, verify that you can minimize unsafe reachability by placing a small mechanism behind a safe state machine and adversarial tests. This module preserves that capability and adds the ability to explain when generic functions are monomorphized and why source-level abstraction does not determine final code duplication. Module 98, **Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration**, will rely on both when it asks: *Which verification technique can falsify which kind of Rust claim, and how do you combine them without pretending that test volume equals proof?*

### Scope boundary

This module owns the reasoning for **from source to machine code: monomorphization, dispatch, layout, and code size** inside Course 10. The course selects stable mechanisms that serve real product requirements. It does not reward obscure syntax, nightly-feature collecting, unsafe code retained for display, or lower-level compiler output used where source-level reasoning is already decisive. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

After completing this module, you will be able to:

- explain when generic functions are monomorphized and why source-level abstraction does not determine final code duplication
- compare static dispatch, enum dispatch, and trait-object dispatch through behavior, extension model, call shape, and measured artifact cost
- inspect symbols, section sizes, assembly, and layout observations for one pinned target and profile without claiming portability
- identify where inlining, dead-code elimination, link-time optimization, and codegen units can obscure naïve source-to-symbol expectations
- use representation attributes only for documented interoperability or layout contracts rather than speculative micro-optimization
- record a code-generation claim with source revision, toolchain, target, profile, features, and measurement method

## Core model

### The governing model

Use a **source-to-artifact observation record**: semantic variants, fixed build identity, expected generated units, observed symbols or assembly, profile evidence, and scope of conclusion. Every cost statement is attached to one artifact and one workload; every semantic statement remains independent of optimization.

### 1. Monomorphization specializes reachable generic uses

A generic function is type checked once under its bounds, then concrete uses may produce specialized machine code. The compiler can share, merge, inline, or remove code where semantics permit, so “one type means one symbol” is not a reliable counting rule. The architectural consequence remains: public generic variation can increase compilation work and artifact diversity. Measure representative instantiations rather than extrapolating from syntax.

**Enumerate reachable instantiations.** For a generic function called with three types, identify which calls may produce distinct code before considering inlining or merging.

### 2. Dispatch mechanisms encode different authority

Static dispatch lets the caller and compiler know the concrete type. Enum dispatch keeps a closed set under the enum owner’s control. Trait objects let a runtime registry hold open implementations behind a stable dyn-compatible contract. Performance is only one axis. Diagnostics, separate compilation, plugin ownership, binary size, and API evolution often dominate. First choose the correct variation model; then measure whether its cost matters.

**Separate dispatch from ownership.** Compare `&T`, `&dyn Trait`, and `Box<dyn Trait>`; which differences are dispatch, allocation, and liveness?

### 3. Inlining changes where cost appears

A small generic adapter may disappear completely into its caller, while a dynamic call usually preserves an indirect boundary unless devirtualization becomes possible. Aggressive inlining can improve hot paths and increase code size or instruction-cache pressure. Preventing inlining for measurement can reveal call overhead but may no longer represent the shipping artifact. Report both the methodological intervention and the production profile.

**Track inlining.** If a helper symbol disappears, explain why that does not prove the source operation has zero cost.

### 4. Layout observations are target-conditioned

`size_of`, `align_of`, field offsets observed through supported tools, and enum sizes describe the compiled target and compiler choices subject to documented representation guarantees. Default `repr(Rust)` layout is not a stable serialization or FFI contract. `repr(C)` provides a C-oriented layout contract for compatible fields, not an optimization guarantee. Choose layout attributes for interoperability or a carefully reviewed unsafe abstraction, then measure secondary performance effects.

**Classify layout claims.** Distinguish `repr(C)` field-order guarantees from target-specific size, padding, and niche observations.

### 5. Artifact size needs attribution

A larger binary can come from monomorphized functions, debug information, panic strategy, unwinding tables, embedded data, dependencies, duplicated format strings, or target runtime support. Use section and symbol tools rather than blaming generics globally. Compare equivalent profiles and strip settings. A code-size budget should identify whether the deployed constraint concerns file size, mapped pages, instruction working set, or cold-start transfer.

**Attribute size.** Separate generic duplication, panic formatting, debug info, dependencies, and generated tables before blaming one abstraction.

### 6. Optimization evidence is artifact-specific

Record the exact source revision, Rust toolchain, target triple, Cargo profile, feature set, lockfile, linker, LTO setting, and inspection command. Keep raw symbol or assembly output. State the conclusion narrowly: “in this artifact, these four codec instantiations account for X text bytes,” not “generics are expensive.” Future compiler releases may change the observation while the language-level design remains valid.

**Pin the artifact.** Record toolchain, target, profile, features, LTO, codegen units, and input before comparing symbols.

### 7. A semantic oracle remains mandatory

Static, enum, and dynamic implementations must produce the same domain result before cost comparison. Add differential tests and a workload that exercises all variants. If the dynamic version changes allocation ownership or the enum version omits runtime extension, they are not interchangeable product candidates. Compare costs only inside the subset of designs that satisfy the required extension and compatibility model.

**Preserve the oracle.** State how static, enum, and dynamic implementations are tested for identical semantics before measuring them.

### Worked observation plan: generic codec versus erased validator

Suppose the final binary contains two `Store` instantiations with different record limits and four validator implementations. Before inspecting symbols, predict the possible sources of code:

```text
generic Store/MAX_RECORD methods
const-specialized codec paths
dynamic Validator call sites
validator concrete method bodies
formatting and error paths
standard-library and panic machinery
```

The prediction is not a guarantee that six obvious symbols will appear. Inlining may move code into callers, identical-code folding may merge functions, dead-code elimination may remove unused paths, and generic sharing decisions may change with the compiler. The useful question is narrower: under one pinned release configuration, which mechanism materially contributes to the artifact or hot path?

Create a semantic oracle first. Feed identical records and invalid cases through every candidate design and compare outputs and errors. Then freeze target, toolchain, profile, features, LTO, codegen units, and representative input. Use symbols or assembly to answer call-shape questions, a size tool to attribute sections or symbols, and a profile to determine whether the path matters under workload. One assembly excerpt without frequency evidence is not a performance conclusion.

Layout requires the same restraint. `size_of::<RecordView>()` on one target is an observation. The fact that a reference is non-null and aligned is a language/library validity concern; the exact width of a fat pointer or niche use is not a stable API unless documented. `repr(C)` may stabilize field order and C ABI expectations for a suitable type, but it does not promise smaller or faster representation. Keep representation promises, target observations, and cost measurements in separate columns. This separation prevents an attractive artifact detail from becoming an accidental compatibility promise.

### A decision table

| Design question | Principled evidence or mechanism | Weak substitute to reject |
|---|---|---|
| Does variation need open runtime extension? | trait object if the product requires it | generic specialization chosen solely for a presumed speed gain |
| Is code duplication material? | symbol and section evidence for representative instantiations | counting generic source uses |
| Does layout require a guarantee? | documented repr for FFI/unsafe contract | default layout observed once and serialized |
| Did optimization move or remove cost? | equivalent semantics plus profile and assembly evidence | one function-level timing without displaced-cost checks |

### A rigorous working procedure

1. Define the semantic oracle and prove all variants satisfy it.
2. State one narrow artifact claim: call indirection, instantiation count, layout, or binary contribution.
3. Freeze toolchain, target, profile, features, linker, and representative input.
4. Predict generated units from source reachability, then inspect symbols or assembly.
5. Attribute observed cost with profiles or section/symbol evidence; avoid reading source syntax as a cost model.
6. Record the conclusion with an expiry condition: artifact, configuration, or workload change.

### Failure patterns and principled repairs

Code-generation and layout mistakes arise when a source-level form is treated as proof of a machine-level property. Repair them by preserving a semantic oracle, fixing the exact artifact and build configuration, and measuring the specific claim—dispatch, instantiation count, layout, or code size—without generalizing beyond that evidence.

### Equating generic source with one symbol per type

Inspect the linked artifact; inlining, merging, and elimination can change symbol shape.

### Calling an indirect call inherently slow

Measure it inside the relevant workload and include code-size and extension requirements.

### Using `repr(C)` as a performance annotation

Apply representation attributes only where an interoperability or reviewed layout contract needs them.

### Publishing assembly without artifact metadata

Record source, toolchain, target, profile, features, linker, and inspection command.

### What the compiler cannot decide for you

Rust’s type system determines legality and many semantic guarantees. It does not promise one monomorphized symbol per call, permanent vtable layout, specific inlining, or a universal performance ordering between static and dynamic dispatch. `repr(C)` is an interoperability contract, not an optimization request.

An advanced engineer may choose dynamic dispatch to reduce code size or static dispatch to enable specialization, but the decision becomes credible only after semantic parity and artifact-specific measurement.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For explain when generic functions are monomorphized and why source-level abstraction does not determine final code duplication, construct one positive and one causal negative example. Mark the first decisive fact in the **source-to-artifact observation** and state which evidence could falsify the claim.

2. **Outcome 2.** For compare static dispatch, enum dispatch, and trait-object dispatch through behavior, extension model, call shape, and measured artifact cost, construct one positive and one causal negative example. Mark the first decisive fact in the **source-to-artifact observation** and state which evidence could falsify the claim.

3. **Outcome 3.** For inspect symbols, section sizes, assembly, and layout observations for one pinned target and profile without claiming portability, construct one positive and one causal negative example. Mark the first decisive fact in the **source-to-artifact observation** and state which evidence could falsify the claim.

4. **Outcome 4.** For identify where inlining, dead-code elimination, link-time optimization, and codegen units can obscure naïve source-to-symbol expectations, construct one positive and one causal negative example. Mark the first decisive fact in the **source-to-artifact observation** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

Run the same scoring behavior through a generic function, a closed enum, and a trait object. First prove equal outputs over a broad input set. Then inspect only the pinned artifact questions: reachable symbols, indirect calls, and size contribution.

```rust
trait Score {
    fn score(&self, input: u64) -> u64;
}

struct Add(u64);
struct Multiply(u64);

impl Score for Add {
    fn score(&self, input: u64) -> u64 { input + self.0 }
}
impl Score for Multiply {
    fn score(&self, input: u64) -> u64 { input * self.0 }
}

enum BuiltIn {
    Add(Add),
    Multiply(Multiply),
}

fn static_score<S: Score>(scorer: &S, input: u64) -> u64 {
    scorer.score(input)
}

fn dynamic_score(scorer: &dyn Score, input: u64) -> u64 {
    scorer.score(input)
}
```

### Trace the example

List every concrete `Score` type used by the static path and predict possible instantiations. For the enum path, identify the match and closed variants. For the trait-object path, identify the data and metadata pointers but do not assume a permanent vtable layout.

Build with two profiles and compare. If inlining removes all visible calls in one profile, retain the semantic explanation and write a narrower artifact note. Then add a large error-formatting path and observe why binary-size attribution must include more than dispatch.

### Use it in AxiomStore

AxiomStore provides three deliberately comparable paths: generic static codec calls, an enum over built-in archive versions, and a trait-object validator registry. The course supplies a code-generation observation script and a semantic parity test. You will decide which boundaries are architecture and which are optimization candidates, then record artifact-specific findings without rewriting the public model around one disassembly.

For AxiomStore, create one artifact record per claim:

```text
semantic variants compared
oracle and inputs
toolchain / target / profile / features
predicted code-generation effect
inspection command or report
observed effect
alternative explanation
narrow conclusion
expiry trigger
```

Use it to compare generic codec specialization, dynamic validator calls, and any code-size effect of const capacities. Do not expose internal representation merely to make inspection easier.

## Practice sequence

1. **Instantiation inventory.** Predict and then inspect generic instances for several types and const values.
2. **Dispatch parity.** Implement static, enum, and dynamic scoring with one exhaustive semantic oracle.
3. **Layout notebook.** Measure sizes and alignments on the current target while labeling each observation, then list only the guarantees supplied by representation attributes.
4. **Binary attribution.** Add and remove one feature or generated table and compare section/symbol evidence under identical profiles.
5. **Inlining interpretation.** Explain a vanished function without claiming the operation is free.

Complete the [workbook](workbook.md) and [Dispatch Observatory](../../labs/module-07-dispatch-observatory/README.md). Manual-review investigations must include artifact identity and a conclusion that does not outlive it.

## Ready to continue

Proceed when you can keep semantic proof separate from machine evidence, enumerate possible monomorphizations, distinguish dispatch from ownership, and label layout observations correctly. You should be able to reject the phrase “zero cost” unless it is replaced by a measured, scoped claim.

## Primary Rust references

- The rustc development guide: monomorphization and code generation
- Cargo reference: profiles and LTO
- The Rust Reference: type layout and representation attributes

Compiler output flags and symbol formats are tool interfaces, not language specifications. Record exact commands and versions beside every artifact observation; use the Reference for representation guarantees.

## Continue

Continue to [Module 98 — Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration](../module-98-verification-beyond-examples-compile-fail-property-model-fuzz-miri-and-concurrency-exploration/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
