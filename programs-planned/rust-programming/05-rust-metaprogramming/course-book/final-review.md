# Final review — Course 5: Rust Metaprogramming

## Part A — refuse unnecessary generation

For each proposal, choose ordinary Rust, `macro_rules!`, derive, attribute, function-like procedural macro, or build script. State the source of truth, generated surface, decisive phase, deletion test, and strongest rejected mechanism.

- normalize runtime strings;
- keep enum variants, stable codes, and messages synchronized;
- implement one trait from named struct fields;
- validate and augment a handler function;
- define a route table with duplicate method/path detection;
- turn checked-in protocol codes into constants.

## Part B — declarative grammar

Design a `macro_rules!` invocation with explicit fragment kinds, repetition, optional trailing separator, single evaluation, and `$crate`-safe paths. Predict failures for fragment mismatch, repetition-depth mismatch, local ambiguity, and invocation-position mismatch.

## Part C — procedural pipeline

For a custom derive and a function-like DSL, draw:

```text
input tokens → syntax AST → semantic validation → normalized model → emitted Rust
```

State what the macro cannot know before ordinary type checking. Preserve generics, where clauses, visibility, unrelated attributes, and useful spans. Combine independent errors.

## Part D — diagnostics and compatibility

Test accepted syntax, malformed grammar, semantic duplicates, and valid expansion rejected by Rust. Explain why exact compiler wording is a fragile contract. Identify which syntax choices become public compatibility obligations.

## Part E — build architecture

Design a build script that validates a tabular source, emits deterministic Rust under `OUT_DIR`, declares rerun inputs, preserves physical line context, and writes the destination safely. List environmental inputs that would make the build non-reproducible.

## Part F — independent construction

Build a compile-time event catalog combining one declarative relationship, one derive, one attached-item validator, one typed DSL, and one generated external table. Delete any layer whose source-of-truth argument is weak. Runtime event behavior must remain ordinary Rust.

Course 5 is complete when you can reason about the expanded program more clearly than the macro invocation and can identify the first phase responsible for every failure.
