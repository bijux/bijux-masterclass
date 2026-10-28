# Course 5 study plan — Rust Metaprogramming

This plan turns ten chapters into ten days of deliberate practice. A day is complete only when the model, independent laboratory, and CommandForge increment agree. If the lab passes while the explanation remains vague, repair the model before moving on.

## Daily rhythm

| Time | Work | Required output |
|---|---|---|
| 08:30–09:00 | closed-book reconstruction | one page of the previous mechanism from memory |
| 09:00–11:00 | authoritative chapter and typed examples | annotated model and changed-assumption predictions |
| 11:15–12:30 | compiler or boundary specimens | frozen predictions and causal comparison |
| 13:30–15:00 | repair and focused construction | smallest principled repair plus rejected shortcut |
| 15:15–17:30 | independent laboratory | working behavior, adversarial tests, design record |
| 18:30–20:00 | CommandForge increment | integrated change and regression evidence |
| 20:00–20:30 | explanation and retrieval | invariant, decisive rule, failure state, transfer case |

Take real breaks. Dense work is not continuous screen time. The weekend between Days 5 and 6 is for repair, reconstruction, and rest rather than new material.

## Day 1 — Metaprogramming Boundaries and the Expansion Model

**Governing question:** Which facts deserve generation, and what exactly happens between macro input and the Rust program that finally runs?

### Morning: derive the model

Read [Module 41](module-41-metaprogramming-boundaries-and-expansion-model/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-41-metaprogramming-boundaries-and-expansion-model/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 41 — Decision Table Generator](../labs/module-01-decision-table-generator/README.md). Build a small mechanism-selection library for a design review. The product receives a concrete requirement and returns the least powerful mechanism that can honestly own it: ordinary Rust, `macro_rules!`, custom derive, attribute macro, function-like procedural macro, or build script.

### Evening: integrate the course product

CommandForge begins with an ordinary handwritten command registry. Before adding generation, write the reference behavior, identify the single authoritative declaration, list every surface that would be generated, and assign each possible failure to the earliest phase that can know it.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- an ordinary-Rust reference design;
- a precise source of truth;
- a generated-surface list;
- a phase-aware failure table;

## Day 2 — Declarative Macros: Matchers, Fragments, and Repetition

**Governing question:** How do you design a `macro_rules!` invocation as a precise grammar while preserving ownership, evaluation order, and expression semantics?

### Morning: derive the model

Read [Module 42](module-42-declarative-macros-matchers-fragments-and-repetition/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-42-declarative-macros-matchers-fragments-and-repetition/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 42 — Typed Map Macro](../labs/module-02-typed-map-macro/README.md). Implement an expression macro that constructs a typed `BTreeMap`, accepts an empty or repeated entry list, evaluates every key and value exactly once in source order, and documents the duplicate-key policy.

### Evening: integrate the course product

CommandForge’s first generated layer is a declarative diagnostic catalog. One invocation now owns each diagnostic variant, numeric code, and message; the expansion must preserve declaration order and produce both forward and reverse lookup without duplicating the table.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- its grammar and cardinality;
- the role of every separator;
- the fragment class of every metavariable;
- the repetition depth of every capture;

## Day 3 — Recursive Macro Parsing and Token-Tree Techniques

**Governing question:** How can a declarative macro process a nontrivial token language with explicit parser state, guaranteed progress, and bounded complexity?

### Morning: derive the model

Read [Module 43](module-43-recursive-macro-parsing-and-token-tree-techniques/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-43-recursive-macro-parsing-and-token-tree-techniques/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 43 — State Machine DSL](../labs/module-03-state-machine-dsl/README.md). Define a bounded declarative grammar for states and transitions, implement recursive internal rules with a visible accumulator and decreasing token measure, and reject malformed tails at the first token that cannot continue the grammar.

### Evening: integrate the course product

CommandForge does not need recursive `macro_rules!` parsing for its final command catalog; Module 49 will use a typed procedural DSL because duplicate detection and cross-entry diagnostics are required. That rejection is itself part of the capstone.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- a finite set of parser states;
- a public grammar and internal state grammar;
- a decreasing measure;
- a base case;

## Day 4 — Hygiene, Scope, Paths, and Cross-Crate Macros

**Governing question:** Whose names should generated code resolve, and how do you make exported macros survive nesting, imports, and dependency renaming?

### Morning: derive the model

Read [Module 44](module-44-hygiene-scope-paths-and-cross-crate-macros/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-44-hygiene-scope-paths-and-cross-crate-macros/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 44 — Exported Registry Macro](../labs/module-04-exported-registry-macro/README.md). Create a library macro that downstream crates use to declare a static registry. Prove it under dependency renaming, nested modules, shadowing of helper names, empty input, and the defining crate’s visibility rules.

### Evening: integrate the course product

CommandForge’s declarative diagnostic macro will expand inside the `commandforge` runtime crate. It uses `$crate` for the generated support table type and standard absolute paths for formatting traits where appropriate. Later procedural macros will be re-exported from the runtime crate and generate paths through `::commandforge` under a documented integrated-crate assumption.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- where it originates;
- where it resolves;
- whether dependency renaming affects it;
- whether privacy permits access;

## Day 5 — Macro Diagnostics, Testing, and Public API Design

**Governing question:** How do you prove that a macro accepts the intended language, rejects misuse for the intended reason, and remains an evolvable public API?

### Morning: derive the model

Read [Module 45](module-45-macro-diagnostics-testing-and-public-api-design/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-45-macro-diagnostics-testing-and-public-api-design/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 45 — Diagnostic Enum Macro](../labs/module-05-diagnostic-enum-macro/README.md). Generate a typed diagnostic catalog from one declaration, including stable codes, messages, deterministic iteration, reverse lookup, and targeted rejection of duplicate or malformed entries.

### Evening: integrate the course product

CommandForge’s diagnostic catalog becomes a public-quality declarative macro in this module.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- the complete accepted grammar;
- the generated public API;
- each important invalid form and its causal phase;
- runtime evaluation and ordering;

## Day 6 — Procedural Macro Execution and TokenStream Engineering

**Governing question:** What does the compiler actually give a procedural macro, what can the macro know, and how should tokens, spans, errors, and effects be handled?

### Morning: derive the model

Read [Module 46](module-46-procedural-macro-execution-and-tokenstream-engineering/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-46-procedural-macro-execution-and-tokenstream-engineering/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 46 — TokenStream Inspector](../labs/module-06-token-stream-inspector/README.md). Implement a function-like procedural macro that renders groups, delimiters, identifiers, literals, punctuation, and joint spacing deterministically without pretending token text has already been name-resolved or type-checked.

### Evening: integrate the course product

CommandForge introduces its `commandforge-macros` crate with the smallest useful procedural boundary: parse a narrow input, preserve caller spans, emit deterministic tokens, and convert every malformed form into compiler input rather than panicking inside the macro process.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- when the macro executes;
- what token structure it receives;
- what spans can and cannot establish;
- why token text is not a resolved AST;

## Day 7 — Custom Derive Macros and Structural Generation

**Governing question:** How do you inspect a Rust item, preserve its generics and constraints, and generate a lawful implementation without pretending to perform type checking?

### Morning: derive the model

Read [Module 47](module-47-custom-derive-macros-and-structural-generation/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-47-custom-derive-macros-and-structural-generation/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 47 — Field Names Derive](../labs/module-07-field-names-derive/README.md). Implement a custom derive that exposes named-field metadata, preserves lifetimes, type and const parameters, and where clauses, supports a documented helper-attribute grammar, and rejects unsupported item shapes deliberately.

### Evening: integrate the course product

CommandForge’s `CommandArgs` derive uses the struct fields as the source of truth for command-line flags.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- exactly which item shapes the derive accepts;
- what structural facts it can know;
- which semantic facts remain for type checking;
- how helper attributes are parsed and validated;

## Day 8 — Attribute Macros and Item Transformation

**Governing question:** How do you validate and transform an attached item while preserving the parts of its public contract that the attribute does not own?

### Morning: derive the model

Read [Module 48](module-48-attribute-macros-and-item-transformation/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-48-attribute-macros-and-item-transformation/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 48 — Checked Handler Attribute](../labs/module-08-checked-handler-attribute/README.md). Implement an attribute that validates the supported function signature, preserves unrelated visibility and attributes, emits typed companion metadata with collision-resistant names, and reports malformed arguments at the authored span.

### Evening: integrate the course product

CommandForge’s handler functions remain ordinary domain code. The attribute owns only signature validation, metadata, and the invocation adapter; arithmetic, text normalization, limits, and domain failures stay in testable runtime functions.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- which transformation mode the attribute uses;
- which item kinds and signatures it supports;
- which original surfaces are preserved or rejected;
- which generated names and visibility are introduced;

## Day 9 — Function-Like Procedural Macros and Typed DSLs

**Governing question:** How do you turn custom syntax into an AST, validate cross-entry semantics, normalize the model, and generate compact typed Rust?

### Morning: derive the model

Read [Module 49](module-49-function-like-procedural-macros-and-typed-dsls/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-49-function-like-procedural-macros-and-typed-dsls/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 49 — Route Table DSL](../labs/module-09-route-table-dsl/README.md). Parse a written route grammar into an AST, detect duplicate method/path pairs with both declaration spans, normalize a validated model, and generate deterministic typed lookup code as a separate final phase.

### Evening: integrate the course product

CommandForge’s command catalog now uses a typed function-like DSL. The parser owns syntax, semantic validation owns duplicate command names and cross-entry relationships, and generation renders only the already validated normalized catalog.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- a written grammar;
- syntax AST types;
- semantic invariants;
- a normalized model;

## Day 10 — Build Scripts, Generated Code, and Compile-Time Architecture

**Governing question:** How do you integrate macros and build generation into a deterministic architecture with one source of truth and no overlapping authority?

### Morning: derive the model

Read [Module 50](module-50-build-scripts-generated-code-and-compile-time-architecture/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-50-build-scripts-generated-code-and-compile-time-architecture/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 50 — Generated Code Build](../labs/module-10-generated-code-build/README.md). Read `schema/commands.tsv` during compilation, validate it, and generate typed Rust under Cargo’s `OUT_DIR`. The checked-in table is the only owner of command name, numeric code, and help text.

### Evening: integrate the course product

The final CommandForge increment completes the exit-code generator and then performs the full architecture review.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- every source of truth;
- every generated surface;
- every compile-time dependency;
- every environmental input;


## Mid-course reconstruction

After Day 5, rebuild the five-module dependency chain without notes. Select the two compiler specimens that changed your model most, rerun them, and explain why the wrong prediction was plausible. Repair every incomplete lab before opening Day 6; later mechanisms assume that the earlier contract is stable.

## Final consolidation

After Day 10, use the [course reference](reference.md) to compress the material, not to relearn it. Complete the [final review](final-review.md) from an empty directory. Then defend CommandForge by tracing one successful operation and one adversarial failure through every layer touched by the course.
