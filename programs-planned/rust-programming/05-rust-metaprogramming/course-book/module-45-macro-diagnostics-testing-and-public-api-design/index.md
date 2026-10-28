# Module 45 — Macro Diagnostics, Testing, and Public API Design

**Course 5 · Day 5 · Module 45 of 100**
`███████████░░░░░░░░░░░░░░` **45/100**

[Program](../../../README.md) · [Course 5](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-05-diagnostic-enum-macro/README.md) · [CommandForge guide](../capstone.md)

[← Module 44: Hygiene, Scope, Paths, and Cross-Crate Macros](../module-44-hygiene-scope-paths-and-cross-crate-macros/index.md) · [Module 46: Procedural Macro Execution and TokenStream Engineering →](../module-46-procedural-macro-execution-and-tokenstream-engineering/index.md)

## The question

> How do you prove that a macro accepts the intended language, rejects misuse for the intended reason, and remains an evolvable public API?

## Why this comes now

A macro is not complete when one valid example expands. Modules 42–44 established grammar, recursion, paths, and visibility. Module 45 turns those mechanisms into a public contract with evidence for success, failure, runtime behavior, downstream use, and future change.

This module is the midpoint of the course because procedural macros amplify every issue discussed here. A parser with excellent spans is still a weak API if its accepted language, generated surface, or compatibility policy is undefined.

### Prerequisite bridge

Module 44 established **Hygiene, Scope, Paths, and Cross-Crate Macros**. Before continuing, verify that you can explain why procedural macros require a different path strategy from `$crate`. This module preserves that capability and adds the ability to treat invocation grammar and generated rust as two related public apis. Module 46, **Procedural Macro Execution and TokenStream Engineering**, will rely on both when it asks: *What does the compiler actually give a procedural macro, what can the macro know, and how should tokens, spans, errors, and effects be handled?*

### Scope boundary

This module owns the reasoning for **macro diagnostics, testing, and public api design** inside Course 5. The course generates ordinary Rust but does not make macros the default abstraction. It avoids using generation for runtime policy, postpones low-level unsafe implementation, and treats third-party procedural-macro crates as compiler-phase dependencies with explicit version and reproducibility implications. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- Treat invocation grammar and generated Rust as two related public APIs.
- Design negative cases that fail for one intended cause.
- Distinguish matcher errors, deliberate `compile_error!`, generated-code errors, and runtime failures.
- Test expansion behavior without depending on unstable textual formatting.
- Build downstream fixtures for paths, visibility, and dependency boundaries.
- Classify changes to accepted syntax and generated surfaces by compatibility risk.
- Write diagnostics that identify the violated contract and the smallest repair.

## Core model

### A macro has four contracts

A production macro exposes at least four contracts.

#### 1. Input-language contract

This specifies:

- invocation position;
- delimiters;
- keywords;
- fragment categories;
- separators;
- cardinality;
- optional clauses;
- defaults;
- unsupported forms.

For a diagnostic catalog:

```rust
diagnostic_catalog! {
    pub enum ParseDiagnostic {
        MissingField = 1001 => "missing field";
        InvalidNumber = 1002 => "invalid number";
    }
}
```

The contract must answer whether empty catalogs, trailing semicolons, repeated codes, nonliteral codes, non-string messages, attributes, generic enums, and custom visibility are supported.

#### 2. Generated-surface contract

This lists everything downstream code can observe:

- enum and variant names;
- methods and associated constants;
- trait implementations;
- visibility;
- module placement;
- generated helper names;
- declaration order;
- trait bounds;
- path requirements;
- documentation behavior.

If a macro emits `pub enum ParseDiagnostic`, that type is public API even though it was generated.

#### 3. Diagnostic contract

This describes which invalid inputs are rejected by which phase and what causal message should appear.

A useful diagnostic says:

- what construct was being parsed;
- what was expected;
- what was found or missing;
- where the problem occurred;
- how to repair it.

A weak diagnostic merely reveals generator internals, such as “no rules expected token `=`” when the product concept is “diagnostic declarations require `Variant = integer => message;`.” Sometimes the built-in matcher diagnostic is already clearer than a custom fallback; test before replacing it.

#### 4. Runtime-semantics contract

Generated code still runs. The macro must state:

- expression evaluation count and order;
- duplicate policy;
- collection order;
- moves and borrows;
- panic behavior;
- allocation and effects;
- error conversion;
- control flow emitted into the caller.

A macro can pass every compile test and still violate this contract.

### Positive tests are necessary but weak alone

A positive test should prove more than “it compiles.” Assert the observable surface and behavior.

For the diagnostic catalog:

```rust
assert_eq!(ParseDiagnostic::MissingField.code(), 1001);
assert_eq!(ParseDiagnostic::MissingField.message(), "missing field");
assert_eq!(ParseDiagnostic::from_code(1002), Some(ParseDiagnostic::InvalidNumber));
assert_eq!(ParseDiagnostic::InvalidNumber.to_string(), "invalid number");
```

Also test declaration order if a generated table exposes it.

Test generative behavior at the level callers rely on. Exact token-string snapshots are fragile because formatting is not semantics. Snapshot a normalized model or assert compiled behavior instead.

### Negative tests require causal isolation

A negative specimen is useful only if one contract violation causes the failure.

Poor negative case:

```rust,compile_fail
diagnostic_catalog! {
    enum Bad {
        Missing = "not a number" => 99
    }
}

fn main() {
    nonexistent();
}
```

The file has several unrelated errors. A runner that observes a nonzero exit status cannot tell whether the macro rejected the intended misuse.

Strong negative case:

```rust,compile_fail
diagnostic_catalog! {
    pub enum Bad {
        Missing = "not a number" => "missing";
    }
}

fn main() {}
```

The only defect is that the code position requires an integer literal. The test contract records the expected cause.

#### Causal fields for every specimen

Course 5’s compiler manifest records:

- expected pass or fail;
- targeted rule;
- intended cause;
- principled repair;
- weak repair to reject;
- execution mode (`rustc` or Cargo fixture).

A mature compile-test harness should also match a stable diagnostic substring or structured output where practical. Do not overfit complete compiler wording, which can improve between releases.

### Matcher errors versus `compile_error!`

Let the matcher produce its own error when the grammar is already obvious.

```rust
macro_rules! one_or_more {
    ($( $name:ident ),+ $(,)?) => { /* ... */ };
}
```

Invoking `one_or_more!()` naturally fails. A specific empty arm can improve the message:

```rust
() => {
    compile_error!("one_or_more! requires at least one identifier")
};
```

But a universal catch-all may make errors worse:

```rust
($($tokens:tt)*) => {
    compile_error!("invalid invocation")
};
```

This discards information about the actual token mismatch. Add custom arms only for recognizable, common misuse with one clear repair.

### Generated-code errors can be intentional

Sometimes the best validation is a generated type constraint. A derive may emit:

```rust
impl<T> Render for Wrapper<T>
where
    T: std::fmt::Display,
{
    /* ... */
}
```

If `T` lacks `Display`, the type checker reports the unsatisfied bound. The procedural macro did not fail to validate. It delegated a semantic rule to the phase that knows trait implementations.

The generated bound should be close to the public contract so the error points to a meaningful obligation. Do not hide it behind pages of generated helper types.

### Test layers

Use multiple layers because no one test sees the whole system.

#### Unit-test ordinary helper logic

Procedural macro crates should keep parsing, validation, and model transformation in ordinary functions where possible. Test those functions with token streams or syntax nodes without compiling a whole downstream crate.

For `macro_rules!`, ordinary helper logic should remain ordinary functions rather than being duplicated inside expansion.

#### Compile-pass fixtures

Compile valid invocations covering:

- minimum and maximum useful cardinality;
- optional syntax present and absent;
- trailing separator behavior;
- generic types where supported;
- nested modules;
- cross-crate use;
- renamed dependencies where relevant.

#### Compile-fail fixtures

Cover one invalid condition per fixture:

- malformed grammar;
- unsupported item kind;
- duplicate declaration;
- forbidden attribute combination;
- invalid visibility;
- unsatisfied generated bound;
- inaccessible helper path;
- build input violation.

#### Runtime tests

Assert generated behavior:

- evaluation once;
- stable order;
- duplicate policy;
- error values;
- absence of panics;
- correct dispatch;
- deterministic output.

#### Documentation tests

A public macro’s smallest valid invocation belongs in rustdoc. A `compile_fail` block can demonstrate a key invalid use. Documentation tests keep examples synchronized with the actual API.

### Expansion inspection

Tools such as `cargo expand` are useful during development, but a course and library should not require them for basic understanding. Maintain a conceptual expansion in the chapter and test the resulting public behavior.

When inspecting expansion, ask:

- Are caller expressions repeated?
- Are paths fully intentional?
- Are helper names visible?
- Did generics and `where` clauses survive?
- Did attributes move or disappear?
- Did the expansion add bounds or public items?
- Is the generated code much larger than the source relationship warrants?

Do not commit enormous expansion snapshots unless the exact tokens are truly the contract. They are expensive to review and sensitive to formatting changes.

### Compatibility has two directions

Changing a macro can break callers even when ordinary function signatures are unchanged.

#### Input-language compatibility

Potential breaking changes include:

- reserving a token that was previously accepted;
- changing a fragment from `tt` to `expr`;
- requiring a separator previously optional;
- changing arm priority;
- rejecting an invocation that used to expand;
- interpreting an existing token sequence differently;
- changing edition and fragment acceptance.

Broad accepted syntax creates future constraints. If a macro accepts arbitrary tokens today and ignores them, you may be unable to assign meaning to them later without changing behavior.

#### Generated-surface compatibility

Potential breaking changes include:

- renaming generated items;
- changing visibility;
- changing generated trait bounds;
- altering evaluation order;
- changing duplicate semantics;
- changing table order;
- removing an implementation;
- changing helper paths used by downstream expansion;
- changing runtime error variants.

The generated code may be invisible in source review, but downstream crates compile against it.

### Reserve syntax deliberately

A public DSL should reject unknown fields rather than ignore them. Rejection keeps the syntax space available for future use and catches misspellings.

Weak attribute policy:

```text
unknown key → ignore
```

Strong policy:

```text
unknown key → error at that key with supported-key list
```

Likewise, distinguish omitted values from defaults. A default is a compatibility commitment. Adding a new optional clause with a default is usually easier than changing the meaning of an omitted existing clause.

### Error aggregation

`macro_rules!` often reports the first matching failure. Procedural macros can accumulate independent semantic errors by combining `syn::Error` values and emitting multiple `compile_error!` invocations.

Aggregation is useful when errors are independent, such as duplicate route keys and two unsupported attributes. Do not continue validation after a parse failure if later checks rely on a trustworthy AST.

The rule is:

- stop when the structure is not reliable;
- combine independent errors over a reliable structure;
- avoid cascading messages caused by one missing token.

### Public documentation should show the expansion contract

A macro page should include:

1. one minimal valid invocation;
2. one realistic invocation;
3. accepted grammar in prose or notation;
4. generated public surface;
5. evaluation and ownership semantics;
6. failure cases;
7. path and feature requirements;
8. compatibility notes;
9. when not to use the macro.

Examples alone are not a grammar. “Works like this” leaves callers guessing about omitted cases.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For treat invocation grammar and generated Rust as two related public APIs, construct one positive and one causal negative example. Mark the first decisive fact in the **diagnostic contract** and state which evidence could falsify the claim.

2. **Outcome 2.** For design negative cases that fail for one intended cause, construct one positive and one causal negative example. Mark the first decisive fact in the **diagnostic contract** and state which evidence could falsify the claim.

3. **Outcome 3.** For distinguish matcher errors, deliberate `compile_error!`, generated-code errors, and runtime failures, construct one positive and one causal negative example. Mark the first decisive fact in the **diagnostic contract** and state which evidence could falsify the claim.

4. **Outcome 4.** For test expansion behavior without depending on unstable textual formatting, construct one positive and one causal negative example. Mark the first decisive fact in the **diagnostic contract** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

CommandForge’s diagnostic catalog becomes a public-quality declarative macro in this module.

Required evidence:

- valid catalog with three entries;
- empty catalog rejection;
- malformed code rejection;
- missing semicolon rejection;
- generated `code`, `message`, `from_code`, `Display`, and ordered `ALL` behavior;
- nested-module invocation;
- no accidental caller imports;
- documentation example;
- explicit statement that duplicate numeric codes are not semantically rejected by `macro_rules!` in this design.

The independent [Diagnostic Enum Macro](../../labs/module-05-diagnostic-enum-macro/README.md) extends the idea with a complete public contract and a curated invalid-input suite.

At the end of Module 45, the declarative half of the course should feel complete. The next module moves to procedural execution because item inspection, structured attributes, duplicate detection, and precise spans require a different mechanism—not because procedural macros are inherently more advanced or more desirable.

## Practice sequence

1. Write the four contracts for a macro you already use.
2. Split one overloaded negative fixture into isolated causes.
3. Replace one vague catch-all diagnostic with either a targeted arm or the native matcher error.
4. Add runtime tests for evaluation count and ordering.
5. Test an exported macro in a renamed downstream dependency.
6. Classify five proposed macro changes by input-language and generated-surface compatibility.
7. Complete the diagnostic-enum laboratory.
8. Finish CommandForge’s declarative diagnostic layer and its compile cases.

## Ready to continue

Continue when you can provide evidence for:

- the complete accepted grammar;
- the generated public API;
- each important invalid form and its causal phase;
- runtime evaluation and ordering;
- downstream path behavior;
- compatibility constraints;
- the boundary between macro validation and generated type checking.

Do not continue if your test strategy is only “the crate builds” or if negative cases merely contain code that happens to be invalid.

## Primary Rust references

- Rust Reference, macros by example: <https://doc.rust-lang.org/reference/macros-by-example.html>
- Standard library `compile_error!`: <https://doc.rust-lang.org/std/macro.compile_error.html>
- Rustdoc documentation tests: <https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html>
- Cargo Book, tests: <https://doc.rust-lang.org/cargo/guide/tests.html>

## Continue

Continue to [Module 46 — Procedural Macro Execution and TokenStream Engineering](../module-46-procedural-macro-execution-and-tokenstream-engineering/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
