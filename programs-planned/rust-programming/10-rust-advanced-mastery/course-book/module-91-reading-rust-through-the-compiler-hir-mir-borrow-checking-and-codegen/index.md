# Module 91 — Reading Rust Through the Compiler: HIR, MIR, Borrow Checking, and Codegen

**Course 10 · Day 1 · Module 91 of 100**
`███████████████████████░░` **91/100**

[Program](../../../README.md) · [Course 10](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-01-compiler-evidence-notebook/README.md) · [AxiomStore guide](../capstone.md)

[← Module 90: Production Readiness, Capacity Planning, Rollouts, and Incident Learning](../../../09-rust-performance-production-engineering/course-book/module-90-production-readiness-capacity-planning-rollouts-and-incident-learning/index.md) · [Module 92: Advanced Trait Solving: Goals, Projections, and Type Equality →](../module-92-advanced-trait-solving-goals-projections-and-type-equality/index.md)

## The question

> When difficult Rust code surprises you, which compiler representation and which proof obligation actually decide the result?

## Why this comes now

The first ten courses taught you to reason from source-level contracts. Advanced work requires one additional discipline: knowing when the source syntax is no longer the best level of explanation. Method calls are resolved, patterns are lowered, implicit borrows are inserted, control flow is made explicit, drops are scheduled, and generic code is instantiated before machine code exists. A compiler-shaped explanation does not mean memorizing rustc internals. It means choosing the representation that exposes the decisive fact without inventing folklore about what “the compiler probably does.”

Course 1 supplied ownership and control-flow vocabulary; Course 2 supplied drop and lifetime reasoning; Courses 6 and 9 taught proof boundaries and artifact-scoped observations. This module joins those habits into one compiler-facing investigation method.

Course 10 begins by changing the reader’s debugging habit. Earlier courses could usually be explained directly from source contracts. Here, the same source may hide receiver adjustments, temporary scopes, lowered control flow, drop edges, and generic instantiations. The aim is not to memorize rustc internals. It is to select the earliest representation that can answer the question and to stop the conclusion exactly where that evidence stops.

### Prerequisite bridge

Module 90 established **Production Readiness, Capacity Planning, Rollouts, and Incident Learning**. Before continuing, verify that you can turn incidents and near misses into corrected models, tests, limits, and architecture rather than blame or one-off patches. This module preserves that capability and adds the ability to separate parsing, name resolution, type checking, trait solving, borrow checking, monomorphization, optimization, and linking as distinct explanatory phases. Module 92, **Advanced Trait Solving: Goals, Projections, and Type Equality**, will rely on both when it asks: *How do you design and debug APIs when the compiler must prove nested trait goals and normalize associated types before ordinary operations become legal?*

### Scope boundary

This module owns the reasoning for **reading rust through the compiler: hir, mir, borrow checking, and codegen** inside Course 10. The course selects stable mechanisms that serve real product requirements. It does not reward obscure syntax, nightly-feature collecting, unsafe code retained for display, or lower-level compiler output used where source-level reasoning is already decisive. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

After completing this module, you will be able to:

- separate parsing, name resolution, type checking, trait solving, borrow checking, monomorphization, optimization, and linking as distinct explanatory phases
- translate source constructs into a control-flow and place-oriented model suitable for borrow, move, and drop reasoning
- identify when an observation is a language guarantee, a compiler implementation detail, or generated machine-code evidence
- use compiler diagnostics, expanded code, MIR-oriented reasoning, and assembly inspection without treating any single view as the complete semantics
- explain non-lexical lifetimes, temporary scopes, partial moves, and destructor placement through explicit control-flow points
- construct a compiler-evidence notebook that records the question, representation, observation, and justified conclusion

## Core model

### The governing model

Use a **source-to-artifact evidence ladder**. Begin with the language-level claim, descend only as far as necessary—resolution and typing, trait goals, place-and-control-flow reasoning, borrow checking, runtime observation, or code generation—and record what each layer cannot establish. A lower layer is not automatically more authoritative; it is authoritative only for the question that layer represents.

### 1. Source is a specification surface, not the final execution graph

Rust source deliberately compresses decisions. Autoderef, autoref, coercions, pattern lowering, desugaring, and implicit drop scopes make code readable, but they can hide the exact place or control-flow edge that matters. Begin with source because the public contract lives there. Move to a lower representation only when the source leaves a concrete question unanswered. The goal is not to worship compiler output; it is to prevent a vague source metaphor from replacing the actual rule.

**Check the boundary.** Take `for item in collection` and write its source contract before considering desugaring. Which facts about ownership are language-level, and which exact iterator method selected is a type-resolution question?

### 2. HIR-style reasoning answers name and type questions

After parsing and macro expansion, the compiler works with a representation where many surface forms have been normalized and names are resolved. At this level, ask which item a path denotes, which receiver adjustment a method call requires, which closure captures exist, and which type obligations were introduced. This is the right level for explaining why an apparently available method is not selected, why a coercion happens in one position but not another, or why an opaque type must remain one hidden concrete type.

**Resolve before lowering.** For `value.process()`, list the receiver adjustments and candidate traits that must be known before MIR-like control flow can explain anything. What evidence would distinguish an inherent method from a trait method?

### 3. MIR-style reasoning answers place, move, drop, and control-flow questions

Mid-level reasoning exposes basic blocks, explicit branches, places such as `records[index].field`, moves, borrows, assignments, and drop points. You do not need unstable compiler output to use the model. Draw the places touched by each operation, the control-flow edge on which each value becomes initialized, and the exits that require cleanup. This is especially useful for partial initialization, `match` guards, early returns, unwind cleanup, and borrows whose source-level lexical block is larger than their actual use.

**Draw the places.** In `records[i].payload.push_str(suffix)`, name every projected place and each read or write. Which projections could be split, and which share the same base loan?

### 4. Borrow checking is a proof over accesses, not a punishment for syntax

The borrow checker asks whether the inferred loans and accesses can coexist on every relevant control-flow path. A rejected program may have a correct product idea but an API that hides disjointness or extends a loan through an unnecessarily large return value. A compiler-level analysis should locate the conflicting place, access kind, and live region. The principled repair changes that relationship: split the place, shorten the returned borrow, sequence effects, or move ownership. Cloning everything merely abandons the proof.

**Locate the conflict.** Given a mutable borrow returned from a lookup helper, mark its last use and the later access it blocks. Repair the access relationship rather than inserting a clone.

### 5. Drop elaboration is part of semantics

Values are destroyed on normal exits and, where unwinding is supported, cleanup paths. Partial moves create partially initialized aggregates; initialized fields still require destruction. Temporaries have scopes that may be shorter or longer than an intuitive reading suggests. When resource behavior matters, write a drop timeline for normal return, early return, and panic. Do not infer destructor timing from one optimized assembly listing, because optimization may inline or remove observable-free code while preserving language semantics.

**Trace all exits.** For a partially initialized tuple followed by `?`, draw normal-return, early-return, and unwind cleanup. Which fields are live on each edge?

### 6. Monomorphization and code generation answer cost questions, not source legality

Generic source can produce several machine-code instances, one shared instance, or code that disappears under optimization. Dynamic dispatch adds an indirect call but may reduce duplication. These are code-generation questions after the program is already well typed. Use symbol, size, and assembly evidence for a named artifact and profile. Do not turn an x86-64 release observation into a portable Rust guarantee, and do not use “zero cost” as a substitute for measurement.

**Constrain the cost claim.** If two generic call sites produce one visible symbol after optimization, what does that establish about this artifact, and what does it not establish about Rust generics?

### 7. A compiler-evidence notebook keeps conclusions honest

For each difficult question, record four columns: the claim, the representation capable of answering it, the observation, and the narrowest justified conclusion. Add a fifth column for what remains unknown. A borrow diagnostic may establish that one source program is rejected; it does not prove every alternative is sound. MIR-like control flow may establish where drops are required; it does not establish exact machine instructions. Assembly may establish one artifact’s code shape; it does not define future compiler behavior.

**Write the uncertainty column.** For one compiler diagnostic, state the narrow conclusion it supports and two architectural questions it leaves unanswered.

### A decision table

| Design question | Principled evidence or mechanism | Weak substitute to reject |
|---|---|---|
| Why is this method selected? | resolved receiver, autoderef/autoref, and trait candidates | machine code before type selection |
| Why does this borrow conflict? | place projections, access kinds, and loan liveness across control flow | a lexical-scope slogan |
| When is a value destroyed? | initialization state and normal/unwind exit edges | one optimized build’s visible calls |
| Did abstraction add runtime cost? | equivalent artifact, symbols, assembly, and profile evidence | source syntax alone |

### A rigorous working procedure

1. Write one falsifiable question: method selection, move legality, drop obligation, or generated cost. Do not write “what does the compiler do?”
2. Mark the earliest phase with enough information. A borrow question needs places and control flow; an assembly question needs a fixed artifact; a name-resolution question does not need machine code.
3. Rewrite the relevant source into an explicit ledger: receiver adjustments, projected places, initialization states, branch edges, or generic instances.
4. Construct a positive and a causal negative program that differ in one relationship. Record the first phase at which their paths diverge.
5. Compare the explanation with a compiler diagnostic or artifact inspection, but keep tool output subordinate to the stable language contract.
6. Record the conclusion and the remaining unknowns in the Compiler Evidence Notebook. If the conclusion mentions performance, include target, profile, features, and toolchain.

### Failure patterns and principled repairs

These failures share one pattern: the explanation begins at the phase where the symptom appears instead of the earliest phase that made the result inevitable. Repair the explanation before repairing the code. Name the source construct, the compiler representation that makes the decisive relationship visible, and the later artifact that merely reports the consequence.

### Reading a late error as an early-phase failure

Locate the earliest phase that has enough information. A linker error cannot explain trait selection; a runtime panic cannot prove borrow rejection.

### Treating MIR-like reasoning as a stable public format

Use the place/control-flow model, but label specific rustc dumps and flags as compiler-tool observations.

### Explaining temporary lifetime by indentation

Write the temporary-producing expression, its enclosing statement or control-flow scope, and the actual last use.

### Using assembly to redefine semantics

First preserve the language-level oracle. Assembly can support a cost claim only for the recorded artifact.

### What the compiler cannot decide for you

Rustc can reveal why a particular program is accepted, rejected, or lowered in a particular build. It cannot choose the product redesign after a borrow conflict, decide whether a destructor’s side effect is a sound API contract, or tell you whether an observed instruction sequence matters under the real workload. Those decisions require the ownership, compatibility, and measurement methods from earlier courses.

The mature habit is to explain from the **earliest decisive layer**. Starting too high produces folklore; starting too low buries the governing contract in implementation detail. A compiler dump is evidence, not curriculum magic and not a permanent public format.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For separate parsing, name resolution, type checking, trait solving, borrow checking, monomorphization, optimization, and linking as distinct explanatory phases, construct one positive and one causal negative example. Mark the first decisive fact in the **compiler-phase record** and state which evidence could falsify the claim.

2. **Outcome 2.** For translate source constructs into a control-flow and place-oriented model suitable for borrow, move, and drop reasoning, construct one positive and one causal negative example. Mark the first decisive fact in the **compiler-phase record** and state which evidence could falsify the claim.

3. **Outcome 3.** For identify when an observation is a language guarantee, a compiler implementation detail, or generated machine-code evidence, construct one positive and one causal negative example. Mark the first decisive fact in the **compiler-phase record** and state which evidence could falsify the claim.

4. **Outcome 4.** For use compiler diagnostics, expanded code, MIR-oriented reasoning, and assembly inspection without treating any single view as the complete semantics, construct one positive and one causal negative example. Mark the first decisive fact in the **compiler-phase record** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

Read the program twice. First predict ownership and destruction only from Rust semantics. Then lower it into three control-flow paths—`Ok`, `Err`, and cleanup—and account for both `Probe` values. Only after that should you run it and compare the printed order with the semantic prediction.

```rust
use std::cell::Cell;

struct Probe<'a> {
    name: &'static str,
    drops: &'a Cell<usize>,
}

impl Drop for Probe<'_> {
    fn drop(&mut self) {
        self.drops.set(self.drops.get() + 1);
        println!("drop {}", self.name);
    }
}

fn choose<'a>(flag: bool, drops: &'a Cell<usize>) -> Result<Probe<'a>, Probe<'a>> {
    let left = Probe { name: "left", drops };
    let right = Probe { name: "right", drops };
    if flag { Ok(left) } else { Err(right) }
}

fn main() {
    let drops = Cell::new(0);
    let outcome = choose(true, &drops);
    drop(outcome);
    assert_eq!(drops.get(), 2);
}
```

### Trace the example

Create a table with one row for `left`, one for `right`, and columns for construction, movement into the enum, branch-local ownership, return, and final destruction. Explain why returning `Ok(left)` does not leak `right`, and why the total drop count is two even though only one value appears in the returned variant.

Now change `choose` so one `Probe` is stored in an `Option` and conditionally taken. Predict the initialization state at every exit. Finally, inspect an optimized artifact and record only an artifact-scoped statement: for example, whether the `println!` calls prevent elimination. Do not let the artifact redefine the source-level drop obligation.

### Use it in AxiomStore

In AxiomStore, compiler-shaped reasoning is used before adding advanced abstractions. You will trace a borrowed record view from the input buffer through decoding, validation, iteration, and release; identify the exact place that owns each byte; draw the drop paths for partially built transactions; and state which later measurements concern semantics versus code generation. The result is an evidence notebook that becomes the foundation for every design decision in Modules 92–100.

Before changing AxiomStore, add a compiler-evidence page containing:

```text
question
source-level contract
earliest decisive phase
explicit places or control-flow states
positive case
causal negative case
observed diagnostic or artifact
justified conclusion
remaining unknowns
```

Trace one `RecordView` from snapshot bytes into the lending cursor and back out of scope. Separately trace one failed transaction through operation staging, candidate construction, validation, encoding, temporary-file creation, and cleanup. These two traces become the baseline against which every later abstraction is reviewed.

## Practice sequence

1. **Method selection audit.** Build two traits with the same method name plus one inherent method. Predict each call using fully qualified alternatives, then verify the selected receiver adjustments.
2. **Place-and-loan diagram.** Diagnose a conflict involving two fields, an indexed element, and a returned mutable reference. Produce a repair that changes the access geometry rather than ownership policy.
3. **Drop-state table.** Use a type with an observable destructor in a function containing partial moves, `?`, and an early `return`. Account for every initialized field on every edge.
4. **Temporary-scope experiment.** Compare a temporary created in a statement, a `match` scrutinee, and a `let` binding. State the semantic lifetime before observing output.
5. **Artifact-limited cost note.** Compare one static and one dynamic call in a pinned release artifact. Include the semantic oracle, build identity, observed symbols, and a sentence prohibiting generalization.

Complete the [workbook](workbook.md), then build the [Compiler Evidence Notebook](../../labs/module-01-compiler-evidence-notebook/README.md). The module investigations are successful only when the predicted phase and causal rule are correct; a coincidental compiler error earns no credit.

## Ready to continue

Continue only when you can take an unfamiliar diagnostic and produce four things without guessing: the source contract, the earliest decisive phase, an explicit place/control-flow or goal model, and the narrow conclusion. You should also be able to explain why an optimized artifact cannot prove borrow legality and why a clean compile cannot prove a product architecture is appropriate.

## Primary Rust references

- The Rust Reference: expressions, destructors, and type coercions
- The rustc development guide: compiler overview and MIR
- The Rustonomicon: drop checking and advanced ownership caveats

Use the Reference and rustc development guide as maps, not as stable serialization formats for compiler internals. When a flag or dump format is unstable, record the toolchain identity beside the observation.

## Continue

Continue to [Module 92 — Advanced Trait Solving: Goals, Projections, and Type Equality](../module-92-advanced-trait-solving-goals-projections-and-type-equality/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
