# Module 41 — Metaprogramming Boundaries and the Expansion Model

**Course 5 · Day 1 · Module 41 of 100**
`██████████░░░░░░░░░░░░░░░` **41/100**

[Program](../../../README.md) · [Course 5](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-01-decision-table-generator/README.md) · [CommandForge guide](../capstone.md)

[← Module 40: Functional Architecture Synthesis](../../../04-rust-functional-programming/course-book/module-40-functional-architecture-synthesis/index.md) · [Module 42: Declarative Macros: Matchers, Fragments, and Repetition →](../module-42-declarative-macros-matchers-fragments-and-repetition/index.md)

## The question

> Which facts deserve generation, and what exactly happens between macro input and the Rust program that finally runs?

## Why this comes now

The first forty modules gave you ordinary mechanisms for almost every common form of reuse: functions, generics, traits, enums, builders, iterators, closures, modules, and data-driven tables. Course 5 starts by making those mechanisms the default. A macro is justified only when ordinary Rust cannot own a relationship without duplicated declarations or a separate unchecked language.

Beginning with syntax would teach the wrong reflex. The first skill is refusal: identify proposals that should remain functions, values, traits, or parsers. Only then is it useful to learn how expansion works.

### Prerequisite bridge

Module 40 established **Functional Architecture Synthesis**. Before continuing, verify that you can reusable law. This module preserves that capability and adds the ability to separate runtime abstraction from compile-time generation. Module 42, **Declarative Macros: Matchers, Fragments, and Repetition**, will rely on both when it asks: *How do you design a `macro_rules!` invocation as a precise grammar while preserving ownership, evaluation order, and expression semantics?*

### Scope boundary

This module owns the reasoning for **metaprogramming boundaries and the expansion model** inside Course 5. The course generates ordinary Rust but does not make macros the default abstraction. It avoids using generation for runtime policy, postpones low-level unsafe implementation, and treats third-party procedural-macro crates as compiler-phase dependencies with explicit version and reproducibility implications. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- Separate runtime abstraction from compile-time generation.
- Identify the source of truth and generated surface of a proposed macro.
- Explain expansion as a staged production of ordinary Rust tokens.
- Distinguish matcher, parser, name-resolution, type-checking, build, and runtime failures.
- Choose among ordinary Rust, `macro_rules!`, a derive, an attribute, a function-like procedural macro, and a build script.
- Apply a deletion test before accepting a generator into a production design.

## Core model

### A macro is not a faster function

A function receives values after the program has compiled. A macro receives syntax before the expanded program has been fully checked. That distinction determines what each mechanism can own.

Consider repeated validation behavior:

```rust
fn require_nonempty(value: &str) -> Result<&str, &'static str> {
    if value.is_empty() {
        Err("value must not be empty")
    } else {
        Ok(value)
    }
}
```

Turning this into a macro would not centralize anything important. The repeated relationship is runtime behavior over a value. A function already gives one implementation, normal type checking, ordinary tests, predictable evaluation, and clear error flow.

By contrast, suppose one declaration must define an enum variant, a stable numeric code, a display message, and a reverse lookup. Handwritten Rust can express all four, but it must repeat the same association in several places:

```rust
pub enum Diagnostic {
    MissingField,
    InvalidNumber,
}

impl Diagnostic {
    pub const fn code(self) -> u16 {
        match self {
            Self::MissingField => 1001,
            Self::InvalidNumber => 1002,
        }
    }

    pub const fn message(self) -> &'static str {
        match self {
            Self::MissingField => "missing field",
            Self::InvalidNumber => "invalid number",
        }
    }
}
```

A declarative macro may be justified because one token declaration can own a mechanical relationship across multiple Rust surfaces. The macro does not replace the diagnostic behavior; it prevents the variant/code/message mapping from drifting.

The decision is therefore not “Is the code repetitive?” Most programs contain harmless repetition. Ask instead:

> Does one fact need to appear in multiple syntactic positions that ordinary Rust cannot derive from one value or type?

#### Four kinds of repetition

Classify the duplication before choosing a mechanism.

| Repetition | Example | Prefer |
|---|---|---|
| runtime behavior | normalize ten strings | function or iterator |
| type-independent behavior | serialize several types through one contract | trait or generic |
| runtime data | command names and descriptions read at startup | value or table |
| Rust syntax relationship | enum variants plus generated match arms | macro or derive |
| external checked data | protocol codes maintained in a TSV file | build script or separate generator |

The last two are candidates for metaprogramming. They are not automatic approvals.

### The two-program model

When you write a generator, reason about two programs separately.

#### Program A: the generator

The generator:

- receives tokens, an attached Rust item, or external data;
- parses an input language;
- validates rules it can know;
- emits Rust tokens or a generated source file;
- reports errors during compilation.

It may run many times, in a build environment rather than at runtime, and with permissions to read files or environment variables. Its determinism and security matter.

#### Program B: the expanded program

The emitted Rust then goes through ordinary language processing:

- parsing of the emitted tokens;
- name resolution;
- visibility checking;
- type and trait checking;
- borrow checking;
- monomorphization and code generation;
- linking;
- runtime execution.

A macro can emit a call to a nonexistent function. Expansion succeeded; name resolution did not. A derive can emit an implementation requiring `T: Display`. Procedural parsing succeeded; generated type checking may fail because the user’s `T` does not satisfy the bound. A build script can generate syntactically valid Rust with the wrong table order. The crate compiles, but the product contract fails.

Do not collapse these stages into “the macro worked” or “the macro failed.”

### Expansion positions

A macro invocation occurs in a syntactic position, and the generated tokens must be valid there.

```rust
macro_rules! make_answer {
    () => { 42 };
}

let answer: i32 = make_answer!();
```

The invocation is in expression position, so the expansion must parse as an expression.

An item-producing macro belongs where items are legal:

```rust
macro_rules! declare_marker {
    ($name:ident) => {
        #[derive(Debug, Clone, Copy, PartialEq, Eq)]
        pub struct $name;
    };
}

declare_marker!(Ready);
```

The same output cannot be dropped arbitrarily into expression position. Token generation is constrained by the surrounding grammar.

This gives the first expansion audit:

1. Where can the invocation appear?
2. What syntactic category does it produce?
3. Does it introduce names?
4. Does it evaluate caller expressions?
5. Does it produce one item, many items, a pattern, a type, a statement, or an expression?

A public macro should document those answers as part of its API.

### Phase-local knowledge

A generator knows syntax, not every semantic fact the compiler will later establish.

A declarative matcher can distinguish an identifier fragment from a literal fragment. It cannot ask whether that identifier names a type implementing `Display`.

A derive using `syn` can see that a field is written as `Vec<T>`. It does not know which `Vec` that path resolves to after imports, whether a type alias hides a different structure, or whether `T` implements a trait unless it emits a bound and lets type checking decide.

A build script can read `TARGET` and `CARGO_CFG_TARGET_OS`; it should not use the host process’s `cfg!` result as if it described the compilation target.

Place each rule in the earliest phase that can know it honestly:

| Rule | Correct owner |
|---|---|
| comma is missing from invocation | declarative matcher or procedural parser |
| two DSL routes have the same literal key | procedural semantic validator |
| generated field type implements `FromStr` | generated trait bound / type checker |
| external table has duplicate numeric codes | build script validator |
| user supplied an unavailable file path at runtime | runtime code |

Checking too late produces poor diagnostics. Pretending to check too early produces brittle syntax inspection that mistakes spelling for meaning.

### The mechanism ladder

Choose the least powerful mechanism that owns the relationship.

#### Ordinary function, trait, or value

Use ordinary Rust when inputs are values or types and the repeated relationship can be expressed through calls, trait implementations, or data.

```rust
const COMMANDS: &[(&str, &str)] = &[
    ("list", "list all records"),
    ("show", "show one record"),
];
```

A macro is unnecessary if this table is already the single source of truth and runtime iteration can produce every required output.

#### `macro_rules!`

Use a declarative macro when:

- the input grammar is token-local and bounded;
- the output is mechanical Rust syntax;
- no semantic analysis beyond matching and repetition is required;
- dependencies and compile time should remain minimal.

Examples include repeated item families, small embedded declarations, and local syntax patterns.

#### Custom derive

Use a derive when an existing struct or enum is the source of truth and you need to generate an implementation or associated metadata from its shape. A derive should not silently replace the item. It adds behavior to a declared type.

#### Attribute macro

Use an attribute when one attached item is the source of truth and the transformation must validate, preserve, augment, or wrap that item. Attributes are powerful because they receive both configuration tokens and the complete item. That power makes preservation rules essential.

#### Function-like procedural macro

Use a function-like procedural macro when a custom grammar coordinates several entries or items and `macro_rules!` would become ambiguous, recursively fragile, or unable to perform semantic checks such as duplicate detection.

#### Build script

Use a build script when the source of truth is external to Rust source and must be validated or translated before compilation. Build scripts can read the filesystem and environment, so they must declare inputs, write only to `OUT_DIR`, and produce deterministic output.

### The deletion test

For every proposed generator, perform this exercise before implementation:

1. Write the ordinary Rust version.
2. Count the facts that must be repeated, not merely the lines.
3. Identify the drift that tests cannot easily prevent.
4. Estimate the new input grammar, generated API, error surface, dependency cost, and compile-time execution.
5. Delete the generator from the design.
6. Ask whether the remaining repetition is actually more expensive than the generator’s permanent complexity.

A macro that saves fifteen straightforward lines but introduces a new language, unusual diagnostics, and a proc-macro dependency usually fails the test.

A derive that keeps thirty field declarations synchronized with a stable metadata trait may pass.

A build script that converts an authoritative protocol registry into checked constants may pass. A build script that computes a timestamp for every build fails reproducibility and often fails the product requirement.

### Source-of-truth ownership

A production compile-time system needs one authority for each fact.

Suppose a command name appears in:

- an attribute on a handler;
- a catalog DSL;
- a help table;
- a build-generated exit table;
- a runtime match.

That is not metaprogramming discipline. It is five declarations connected by hope.

Choose one owner. For CommandForge:

- the handler attribute owns the handler’s local description and signature contract;
- the catalog DSL owns command names, uniqueness, and deterministic order;
- the derive owns flag decoding from a struct’s fields;
- the build table owns exit-code names and numbers;
- runtime functions own command behavior.

No layer should re-declare another layer’s fact merely to make generation convenient.

### Evaluation semantics remain ordinary Rust

Macros can accidentally evaluate an expression more than once.

```rust
macro_rules! bad_double {
    ($value:expr) => {
        $value + $value
    };
}
```

`bad_double!(next_value())` calls `next_value` twice. The invocation looks like a function call but does not have function-call evaluation semantics.

A repaired expansion binds once:

```rust
macro_rules! double_once {
    ($value:expr) => {{
        let value = $value;
        value + value
    }};
}
```

The block contains generated runtime code. Ownership still matters: `value + value` may be invalid for non-`Copy` types. The macro’s contract must state the accepted type behavior rather than imply universal duplication.

Every expression-accepting macro should answer:

- Is each expression evaluated exactly once?
- In what order?
- Is the result moved, borrowed, or copied?
- Are temporaries scoped differently from a function call?
- Does the expansion introduce an early `return`, `break`, or `?`?

### Failure is a topology, not one event

Use a phase table when diagnosing a compile-time system.

| Phase | Example failure | Best repair location |
|---|---|---|
| invocation matching | missing separator | matcher grammar |
| procedural parsing | expected string literal | parser with source span |
| semantic validation | duplicate route | normalized model validation |
| generated parsing | emitted malformed Rust | generator tests |
| name resolution | wrong crate path | hygiene/path design |
| type checking | generated bound not satisfied | generated contract or source type |
| build execution | malformed external row | build validator |
| runtime | command rejects domain value | ordinary handler code |

The same visible compiler output may contain errors from several phases. Find the earliest causal failure. Later errors may be consequences.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For separate runtime abstraction from compile-time generation, construct one positive and one causal negative example. Mark the first decisive fact in the **mechanism-selection record** and state which evidence could falsify the claim.

2. **Outcome 2.** For identify the source of truth and generated surface of a proposed macro, construct one positive and one causal negative example. Mark the first decisive fact in the **mechanism-selection record** and state which evidence could falsify the claim.

3. **Outcome 3.** For explain expansion as a staged production of ordinary Rust tokens, construct one positive and one causal negative example. Mark the first decisive fact in the **mechanism-selection record** and state which evidence could falsify the claim.

4. **Outcome 4.** For distinguish matcher, parser, name-resolution, type-checking, build, and runtime failures, construct one positive and one causal negative example. Mark the first decisive fact in the **mechanism-selection record** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

CommandForge begins with an ordinary handwritten command registry. Before adding any macro, write:

```rust
pub struct CommandSpec {
    pub name: &'static str,
    pub about: &'static str,
    pub invoke: fn(&[String]) -> Result<String, CommandError>,
}
```

Then handwrite two command specs and a lookup function. Record:

- how arguments are decoded;
- how the handler is called;
- which errors are returned;
- which order commands are listed;
- which names are public;
- what a duplicate command would mean.

Only after this reference behavior is tested may later modules generate pieces of it. The ordinary version remains the semantic oracle.

The independent laboratory, [Decision Table Generator](../../labs/module-01-decision-table-generator/README.md), asks you to classify ten realistic proposals and generate only the mechanical decision-table surface. The lab is intentionally conservative: the strongest solution is the one that leaves runtime policy in ordinary Rust.

## Practice sequence

1. For five abstractions in an existing Rust project, classify the repeated relationship.
2. Rewrite one proposed macro as a function or table.
3. For one justified generator, write the source-and-expansion ledger.
4. Hand-expand three expression macros and trace evaluation count and ownership.
5. Classify ten failures by phase.
6. Complete the compiler predictions before running them.
7. Build the decision-table laboratory.
8. Establish the handwritten CommandForge registry and its behavioral tests.

## Ready to continue

Continue when you can take an unfamiliar macro proposal and produce:

- an ordinary-Rust reference design;
- a precise source of truth;
- a generated-surface list;
- a phase-aware failure table;
- an evaluation-order statement;
- a deletion-test conclusion.

Do not continue if your reason for a macro is “less typing,” “looks cleaner,” or “the type is complicated.” Those may be outcomes, but they are not ownership of a compile-time relationship.

## Primary Rust references

- Rust Reference, macros by example: <https://doc.rust-lang.org/reference/macros-by-example.html>
- Rust Reference, procedural macros: <https://doc.rust-lang.org/reference/procedural-macros.html>
- Cargo Book, build scripts: <https://doc.rust-lang.org/cargo/reference/build-scripts.html>
- Standard library `proc_macro`: <https://doc.rust-lang.org/proc_macro/>

These sources define language and tool contracts. The chapter supplies the decision model needed to use those contracts coherently.

## Continue

Continue to [Module 42 — Declarative Macros: Matchers, Fragments, and Repetition](../module-42-declarative-macros-matchers-fragments-and-repetition/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
