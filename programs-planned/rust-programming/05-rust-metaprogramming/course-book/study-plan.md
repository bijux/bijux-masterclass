# Course 5 Study Plan — Rust Metaprogramming

Ten dense study days fit into two calendar weeks. The goal is not to maximize reading time; it is to make **Which facts deserve one compile-time source of truth, which generation mechanism is the least powerful adequate choice, and how can expanded code remain diagnosable ordinary Rust?** answerable through construction and explanation.

## Daily rhythm

Use a **generation authority and reproducibility record** across the course. Each day begins by reconstructing yesterday’s decisive relationship and ends by tracing one capstone invariant. Preserve the first prediction, the observed result, the principled repair, and the shortcut you rejected.

## Day 1 — Module 41: Metaprogramming Boundaries and the Expansion Model

**Question:** Which facts deserve generation, and what exactly happens between macro input and the Rust program that finally runs?

**Retrieval:** Without notes, restate the invariant carried from Module 40 — Functional Architecture Synthesis. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 41](./module-41-metaprogramming-boundaries-and-expansion-model/index.md) with a **mechanism-selection record** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-41-metaprogramming-boundaries-and-expansion-model/workbook.md) before observation. The day’s minimum result is: **Separate runtime abstraction from compile-time generation.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Decision Table Generator](../labs/module-01-decision-table-generator/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 41 in the [CommandForge guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Separate runtime abstraction from compile-time generation.** End with one simpler design that would be preferable under a narrower requirement.

## Day 2 — Module 42: Declarative Macros: Matchers, Fragments, and Repetition

**Question:** How do you design a `macro_rules!` invocation as a precise grammar while preserving ownership, evaluation order, and expression semantics?

**Retrieval:** Without notes, restate the invariant carried from Module 41 — Metaprogramming Boundaries and the Expansion Model. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 42](./module-42-declarative-macros-matchers-fragments-and-repetition/index.md) with a **matcher and fragment trace** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-42-declarative-macros-matchers-fragments-and-repetition/workbook.md) before observation. The day’s minimum result is: **Read a matcher as a grammar rather than as textual substitution.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Typed Map Macro](../labs/module-02-typed-map-macro/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 42 in the [CommandForge guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Read a matcher as a grammar rather than as textual substitution.** End with one simpler design that would be preferable under a narrower requirement.

## Day 3 — Module 43: Recursive Macro Parsing and Token-Tree Techniques

**Question:** How can a declarative macro process a nontrivial token language with explicit parser state, guaranteed progress, and bounded complexity?

**Retrieval:** Without notes, restate the invariant carried from Module 42 — Declarative Macros: Matchers, Fragments, and Repetition. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 43](./module-43-recursive-macro-parsing-and-token-tree-techniques/index.md) with a **recursive grammar state** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-43-recursive-macro-parsing-and-token-tree-techniques/workbook.md) before observation. The day’s minimum result is: **Model recursive macro rules as parser states and transitions.** Keep one positive case and one causal negative case.

**Laboratory:** Build [State Machine DSL](../labs/module-03-state-machine-dsl/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 43 in the [CommandForge guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Model recursive macro rules as parser states and transitions.** End with one simpler design that would be preferable under a narrower requirement.

## Day 4 — Module 44: Hygiene, Scope, Paths, and Cross-Crate Macros

**Question:** Whose names should generated code resolve, and how do you make exported macros survive nesting, imports, and dependency renaming?

**Retrieval:** Without notes, restate the invariant carried from Module 43 — Recursive Macro Parsing and Token-Tree Techniques. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 44](./module-44-hygiene-scope-paths-and-cross-crate-macros/index.md) with a **hygiene and path map** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-44-hygiene-scope-paths-and-cross-crate-macros/workbook.md) before observation. The day’s minimum result is: **Distinguish textual scope, path-based scope, and expansion-site lookup for declarative macros.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Exported Registry Macro](../labs/module-04-exported-registry-macro/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 44 in the [CommandForge guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Distinguish textual scope, path-based scope, and expansion-site lookup for declarative macros.** End with one simpler design that would be preferable under a narrower requirement.

## Day 5 — Module 45: Macro Diagnostics, Testing, and Public API Design

**Question:** How do you prove that a macro accepts the intended language, rejects misuse for the intended reason, and remains an evolvable public API?

**Retrieval:** Without notes, restate the invariant carried from Module 44 — Hygiene, Scope, Paths, and Cross-Crate Macros. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 45](./module-45-macro-diagnostics-testing-and-public-api-design/index.md) with a **diagnostic contract** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-45-macro-diagnostics-testing-and-public-api-design/workbook.md) before observation. The day’s minimum result is: **Treat invocation grammar and generated Rust as two related public APIs.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Diagnostic Enum Macro](../labs/module-05-diagnostic-enum-macro/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 45 in the [CommandForge guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Treat invocation grammar and generated Rust as two related public APIs.** End with one simpler design that would be preferable under a narrower requirement.

## Midpoint reconstruction

Do not add a sixth topic on the recovery day. Reconstruct **Metaprogramming Boundaries and the Expansion Model, Declarative Macros: Matchers, Fragments, and Repetition, Recursive Macro Parsing and Token-Tree Techniques, Hygiene, Scope, Paths, and Cross-Crate Macros, Macro Diagnostics, Testing, and Public API Design** as one dependency chain, rerun the two investigations that changed your model most, and describe the current CommandForge state from an empty page. Repair incomplete work, then take a real break; consolidation is part of the course rather than unused time.

## Day 6 — Module 46: Procedural Macro Execution and TokenStream Engineering

**Question:** What does the compiler actually give a procedural macro, what can the macro know, and how should tokens, spans, errors, and effects be handled?

**Retrieval:** Without notes, restate the invariant carried from Module 45 — Macro Diagnostics, Testing, and Public API Design. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 46](./module-46-procedural-macro-execution-and-tokenstream-engineering/index.md) with a **token-stream phase map** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-46-procedural-macro-execution-and-tokenstream-engineering/workbook.md) before observation. The day’s minimum result is: **Explain when and how a procedural macro executes.** Keep one positive case and one causal negative case.

**Laboratory:** Build [TokenStream Inspector](../labs/module-06-token-stream-inspector/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 46 in the [CommandForge guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Explain when and how a procedural macro executes.** End with one simpler design that would be preferable under a narrower requirement.

## Day 7 — Module 47: Custom Derive Macros and Structural Generation

**Question:** How do you inspect a Rust item, preserve its generics and constraints, and generate a lawful implementation without pretending to perform type checking?

**Retrieval:** Without notes, restate the invariant carried from Module 46 — Procedural Macro Execution and TokenStream Engineering. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 47](./module-47-custom-derive-macros-and-structural-generation/index.md) with a **derive expansion ledger** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-47-custom-derive-macros-and-structural-generation/workbook.md) before observation. The day’s minimum result is: **Parse `DeriveInput` and distinguish structs, enums, and unions.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Field Names Derive](../labs/module-07-field-names-derive/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 47 in the [CommandForge guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Parse `DeriveInput` and distinguish structs, enums, and unions.** End with one simpler design that would be preferable under a narrower requirement.

## Day 8 — Module 48: Attribute Macros and Item Transformation

**Question:** How do you validate and transform an attached item while preserving the parts of its public contract that the attribute does not own?

**Retrieval:** Without notes, restate the invariant carried from Module 47 — Custom Derive Macros and Structural Generation. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 48](./module-48-attribute-macros-and-item-transformation/index.md) with a **attribute preservation table** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-48-attribute-macros-and-item-transformation/workbook.md) before observation. The day’s minimum result is: **Parse attribute arguments independently from the attached item.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Checked Handler Attribute](../labs/module-08-checked-handler-attribute/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 48 in the [CommandForge guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Parse attribute arguments independently from the attached item.** End with one simpler design that would be preferable under a narrower requirement.

## Day 9 — Module 49: Function-Like Procedural Macros and Typed DSLs

**Question:** How do you turn custom syntax into an AST, validate cross-entry semantics, normalize the model, and generate compact typed Rust?

**Retrieval:** Without notes, restate the invariant carried from Module 48 — Attribute Macros and Item Transformation. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 49](./module-49-function-like-procedural-macros-and-typed-dsls/index.md) with a **DSL syntax-to-model map** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-49-function-like-procedural-macros-and-typed-dsls/workbook.md) before observation. The day’s minimum result is: **Design a bounded custom grammar with explicit compatibility space.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Route Table DSL](../labs/module-09-route-table-dsl/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 49 in the [CommandForge guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Design a bounded custom grammar with explicit compatibility space.** End with one simpler design that would be preferable under a narrower requirement.

## Day 10 — Module 50: Build Scripts, Generated Code, and Compile-Time Architecture

**Question:** How do you integrate macros and build generation into a deterministic architecture with one source of truth and no overlapping authority?

**Retrieval:** Without notes, restate the invariant carried from Module 49 — Function-Like Procedural Macros and Typed DSLs. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 50](./module-50-build-scripts-generated-code-and-compile-time-architecture/index.md) with a **generation authority and reproducibility record** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-50-build-scripts-generated-code-and-compile-time-architecture/workbook.md) before observation. The day’s minimum result is: **Explain the Cargo build-script lifecycle and communication protocol.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Generated Code Build](../labs/module-10-generated-code-build/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 50 in the [CommandForge guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Explain the Cargo build-script lifecycle and communication protocol.** End with one simpler design that would be preferable under a narrower requirement.

## Final integration

After Day 10, complete the [final review](final-review.md), run the strongest available course route, and implement this unseen capstone change: **Add a new CommandForge field policy and command kind, tracing the change through grammar, semantic validation, expansion, runtime behavior, tests, and compatibility.**

Seven days later, rebuild the ten-module sequence and the core **generation authority and reproducibility record** without the book. Write a fresh example for every relationship you cannot recover. Re-reading a solution without recreating the model does not count as retained learning.
