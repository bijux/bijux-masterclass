# Reasoned solutions — Module 42: Declarative Macros: Matchers, Fragments, and Repetition

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the CommandForge engineering guide](../capstone.md)

Use this file after freezing an independent attempt. In this module, compare exact accepted and rejected syntax, single evaluation of every key and value, source-order preservation, use of `$crate` or fully qualified paths where appropriate. A different implementation is valid only when those contracts survive; matching the reference token-for-token is irrelevant.

## Compiler specimen reasoning

### 1. `case-01.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** expr and ty fragments delegate Rust grammar parsing.
- **Causal explanation:** The specimen compiles because expr and ty fragments delegate Rust grammar parsing.
- **Principled repair:** retain narrow fragments
- **Weak repair to reject:** replace all fragments with tt

### 2. `case-02.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** literal fragments reject nonliteral expressions.
- **Causal explanation:** The compiler rejects the specimen because literal fragments reject nonliteral expressions.
- **Principled repair:** change the public grammar to expr only if arbitrary expressions are intended
- **Weak repair to reject:** wrap the expression in tokens and parse it later

### 3. `case-03.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** repetition can generate ordered statements from ordered input.
- **Causal explanation:** The specimen compiles because repetition can generate ordered statements from ordered input.
- **Principled repair:** keep one repetition depth
- **Weak repair to reject:** manually duplicate each insertion arm

### 4. `case-04.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** metavariables must appear at compatible repetition depth.
- **Causal explanation:** The compiler rejects the specimen because metavariables must appear at compatible repetition depth.
- **Principled repair:** emit name inside matching repetition or capture one name outside
- **Weak repair to reject:** select an arbitrary repeated element

### 5. `case-05.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** macro matching performs no arbitrary lookahead to resolve local ambiguity.
- **Causal explanation:** The compiler rejects the specimen because macro matching performs no arbitrary lookahead to resolve local ambiguity.
- **Principled repair:** add a separator or distinct keyword boundary
- **Weak repair to reject:** reorder rules without changing the ambiguous grammar

### 6. `case-06.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** one repetition can support an optional trailing separator.
- **Causal explanation:** The specimen compiles because one repetition can support an optional trailing separator.
- **Principled repair:** retain a single unambiguous grammar
- **Weak repair to reject:** add overlapping no-comma and comma rules

### 7. `case-07.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** expr fragments have restricted safe followers.
- **Causal explanation:** The compiler rejects the specimen because expr fragments have restricted safe followers.
- **Principled repair:** use a permitted delimiter such as comma or semicolon
- **Weak repair to reject:** capture the whole input as tt and ignore future compatibility

### 8. `case-08.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** caller expressions can be bound once before repeated use.
- **Causal explanation:** The specimen compiles because caller expressions can be bound once before repeated use.
- **Principled repair:** retain single evaluation
- **Weak repair to reject:** duplicate $value in generated code

## How to review the compiler specimens

The machine-readable outcomes are in [`compiler-labs/manifest.json`](../../compiler-labs/manifest.json). For **matcher grammar and evaluation semantics**, compare your prediction against five questions:

1. Which fragment specifier consumes each metavariable, and what grammar can legally follow it?
2. Do nested repetitions bind and expand metavariables at matching depths?
3. Is every argument expression evaluated exactly once and in the promised order?
4. Could two matcher arms accept the same token prefix and create local ambiguity?
5. Does the expansion remain a valid expression, type, pattern, or item in its invocation position?

Diagnostic prose may change between compiler releases. The isolated source shape and governing phase are the durable evidence.

## Broken-design repair

**Step 1.** Define one invocation grammar before writing matchers: a key type, a value type, then zero or more `expr => expr` entries separated by commas with an optional trailing comma.

**Step 2.** Use the narrowest fragments that preserve the required syntax. Use `ty` for declared types and `expr` for evaluated entries; do not use `tt` as a universal escape hatch.

**Step 3.** Bind each key and value once inside the repetition before insertion. This makes evaluation count inspectable and protects expressions with side effects.

**Step 4.** Expand to one block expression whose final value is the map. Keep temporary names inside the block and choose paths that do not depend on caller imports.

**Step 5.** Write positive and negative cases for empty input, trailing commas, malformed entries, duplicate runtime keys, and expressions with observable evaluation.

The repaired design should make **matcher grammar and evaluation semantics** smaller and more inspectable than the broken proposal. Judge it by whether one declaration owns the mechanical relationship, the expanded Rust remains readable, and each invalid input fails in the earliest phase that possesses the necessary information.

## Exercise reasoning

### Exercise 1 — Fragment selection

Use `vis`, `ident`, `ty`, `expr`, `literal`, `meta`, and `tt` respectively. A broad `tt` matcher may accept syntax that later fails far from the invocation or require fragile recursive parsing. Narrow fragments delegate Rust grammar validation to the compiler and make the public language clearer.

### Exercise 2 — Repetition invariant

A metavariable must appear in the transcriber at a compatible repetition depth. A repeated capture represents many occurrences, not one value. Emit it inside a matching repetition, collect it into a generated array/table, or change the input grammar so a single name is captured outside the repeated group.

### Exercise 3 — Evaluation audit

Introduce block-local bindings within the repeated expansion: `let key = $key; let value = $value; map.insert(key, value);`. Rust executes the repeated statements in source order. A duplicate-key policy may replace an earlier value, but it must not reevaluate either expression.

### Exercise 4 — Follow-set diagnosis

Fragment followers are restricted so a matcher remains unambiguous as Rust grammar evolves. A bracket could become part of a trailing expression form, while comma is an established expression separator. Follow-set restrictions protect macro compatibility across future language changes.

### Exercise 5 — Opaque forwarding

Forwarded fragments other than `ident`, `lifetime`, and `tt` are opaque AST fragments to the receiving matcher. The helper cannot inspect the literal tokens inside an `expr`. Match a compatible `expr` in the helper, or capture as `tt` when literal token discrimination is genuinely the grammar requirement.

### Exercise 6 — Trailing separators

Use one repetition such as `$( $key:expr => $value:expr ),+ $(,)?`. The first operator requires at least one entry; the optional final comma is structurally separate. If empty maps are required, use `*` and specify the empty behavior explicitly.

## Laboratory comparison

The reference implementation is in [`labs/module-02-typed-map-macro/solution`](../../labs/module-02-typed-map-macro/solution). Review it in this order:

1. exact accepted and rejected syntax;
2. single evaluation of every key and value;
3. source-order preservation;
4. use of `$crate` or fully qualified paths where appropriate;

Keep your implementation when its **matcher grammar and evaluation semantics** contract is at least as precise with a clearer or smaller design. Revise it when the reference exposes an accepted input, failure phase, generated-name rule, evaluation effect, or determinism obligation missing from your tests.

## Capstone review

For the Module 42 increment, a strong result demonstrates **designing `macro_rules!` grammars with exact fragments, repetition depth, evaluation order, and ownership behavior**. The capstone should still read primarily as ordinary Rust. Generated surfaces must be compact enough to inspect through tests or expansion tools, and runtime domain behavior must remain callable without understanding macro internals.

## What a strong explanation includes

A strong defense of this module explains:

- why each fragment is narrower than `tt`;
- how matcher repetition corresponds to transcriber repetition;
- where caller expressions move or borrow;
- which punctuation is now part of the public API;
- how the generated ordinary Rust can be inspected and tested without trusting the generator blindly;
- which simpler non-macro design was considered and why it is insufficient for this exact source-of-truth relationship.
