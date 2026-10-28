# Reasoned solutions — Module 43: Recursive Macro Parsing and Token-Tree Techniques

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the CommandForge engineering guide](../capstone.md)

Use this file after freezing an independent attempt. In this module, compare whether every recursive branch consumes input or terminates, whether malformed sequences fail near the offending token, whether parsing and code generation are separated, whether the grammar can be stated without reading the implementation. A different implementation is valid only when those contracts survive; matching the reference token-for-token is irrelevant.

## Compiler specimen reasoning

### 1. `case-01.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** a TT muncher terminates when each recursive rule consumes input.
- **Causal explanation:** The specimen compiles because a TT muncher terminates when each recursive rule consumes input.
- **Principled repair:** retain a measurable progress invariant
- **Weak repair to reject:** recurse with the unchanged rest stream

### 2. `case-02.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** a recursive grammar must include a rule for every accepted token shape.
- **Causal explanation:** The compiler rejects the specimen because a recursive grammar must include a rule for every accepted token shape.
- **Principled repair:** use a literal or deliberately extend the grammar
- **Weak repair to reject:** add a catch-all that silently discards the token

### 3. `case-03.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** normalized accumulators separate parsing from final emission.
- **Causal explanation:** The specimen compiles because normalized accumulators separate parsing from final emission.
- **Principled repair:** keep parsing and emission conceptually separate
- **Weak repair to reject:** emit public items during every recursive step

### 4. `case-04.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** targeted compile_error rules can own malformed nearby syntax.
- **Causal explanation:** The compiler rejects the specimen because targeted compile_error rules can own malformed nearby syntax.
- **Principled repair:** write the required arrow
- **Weak repair to reject:** remove the diagnostic rule and accept unclear fallback errors

### 5. `case-05.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** a terminal rule may emit exhaustive state transition logic.
- **Causal explanation:** The specimen compiles because a terminal rule may emit exhaustive state transition logic.
- **Principled repair:** retain a bounded state-machine grammar
- **Weak repair to reject:** build a runtime string parser for fixed Rust identifiers

### 6. `case-06.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** generated duplicate items remain ordinary Rust errors.
- **Causal explanation:** The compiler rejects the specimen because generated duplicate items remain ordinary Rust errors.
- **Principled repair:** reject duplicates during semantic validation or remove the duplicate
- **Weak repair to reject:** let later declarations silently overwrite earlier ones

### 7. `case-07.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** specific recursive rules should precede generic fallbacks.
- **Causal explanation:** The specimen compiles because specific recursive rules should precede generic fallbacks.
- **Principled repair:** retain specific-first ordering
- **Weak repair to reject:** place a broad tt catch-all first

### 8. `case-08.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** explicit terminators make production boundaries part of the grammar.
- **Causal explanation:** The compiler rejects the specimen because explicit terminators make production boundaries part of the grammar.
- **Principled repair:** add the terminator
- **Weak repair to reject:** make terminators optional without specifying recovery

## How to review the compiler specimens

The machine-readable outcomes are in [`compiler-labs/manifest.json`](../../compiler-labs/manifest.json). For **recursive parser progress**, compare your prediction against five questions:

1. What token state does each internal rule consume, and what smaller input reaches the next rule?
2. Where is the accumulator stored, and does its shape preserve source order?
3. Which terminal rule ends successful parsing, and which malformed tails receive explicit errors?
4. Can any invocation recurse without consuming input or changing parser state?
5. Would a procedural parser communicate the grammar more safely once recursion or diagnostics grow?

Diagnostic prose may change between compiler releases. The isolated source shape and governing phase are the durable evidence.

## Broken-design repair

**Step 1.** Write the external grammar in plain text and identify its separators, terminators, and entry categories.

**Step 2.** Split the macro into a small public rule and private `@state` rules. Every recursive rule must consume input or transition to a terminal state.

**Step 3.** Carry an accumulator for normalized state and transition tokens. Do not emit the public item until parsing and local validation have reached the terminal rule.

**Step 4.** Place specific malformed-input rules before a generic fallback so missing arrows, separators, and terminators receive targeted `compile_error!` messages.

**Step 5.** Cap the grammar. If validation requires arbitrary lookup, rich spans, or many interacting states, move to a procedural macro rather than extending a TT muncher indefinitely.

The repaired design should make **recursive parser progress** smaller and more inspectable than the broken proposal. Judge it by whether one declaration owns the mechanical relationship, the expanded Rust remains readable, and each invalid input fails in the earliest phase that possesses the necessary information.

## Exercise reasoning

### Exercise 1 — Grammar before matcher

A defensible grammar names exact delimiters and separators, for example `state-list = "states" ":" "[" ident ("," ident)* "]" ";"` and `transition = ident "=>" ident ";"`. Explicit terminators let recursive rules know where one production ends and improve diagnostics.

### Exercise 2 — Progress proof

Every recursive edge must reduce remaining input or move to a state that cannot cycle back without consumption. A catch-all rule that forwards `$($rest:tt)*` unchanged is non-progressing. Repair it by consuming at least one token, emitting an error, or terminating.

### Exercise 3 — Accumulator shape

Normalized pairs separate parsing from generation. The terminal rule receives one regular representation and can emit match arms deterministically. Raw-token accumulation preserves ambiguity and forces the emitter to parse again.

### Exercise 4 — Duplicate limitations

Declarative macros have no general set data structure or semantic loop. A bounded recursive comparison can work for a very small language, but complexity and diagnostics degrade quickly. A procedural macro is justified when cross-entry uniqueness is a central requirement rather than an optional convenience.

### Exercise 5 — Targeted fallback

Specific patterns that recognize the nearby intended shape should precede the generic fallback. The fallback must consume or terminate with `compile_error!`. Since the first matching rule wins, a broad rule placed first would erase useful context.

### Exercise 6 — Complexity review

Classic TT munchers can exhibit quadratic matching because each recursive call matches a long remaining suffix. Grouping entries with repetition, using larger productions, or delegating a genuinely rich grammar to a procedural parser reduces repeated work. The answer should state that compile-time cost is part of API quality.

## Laboratory comparison

The reference implementation is in [`labs/module-03-state-machine-dsl/solution`](../../labs/module-03-state-machine-dsl/solution). Review it in this order:

1. whether every recursive branch consumes input or terminates;
2. whether malformed sequences fail near the offending token;
3. whether parsing and code generation are separated;
4. whether the grammar can be stated without reading the implementation;

Keep your implementation when its **recursive parser progress** contract is at least as precise with a clearer or smaller design. Revise it when the reference exposes an accepted input, failure phase, generated-name rule, evaluation effect, or determinism obligation missing from your tests.

## Capstone review

For the Module 43 increment, a strong result demonstrates **building recursive token-tree parsers whose state, progress, termination, and diagnostics are visible**. The capstone should still read primarily as ordinary Rust. Generated surfaces must be compact enough to inspect through tests or expansion tools, and runtime domain behavior must remain callable without understanding macro internals.

## What a strong explanation includes

A strong defense of this module explains:

- the progress argument for every recursive rule;
- why one catch-all rule would hide grammar defects;
- which facts are syntax and which are semantic;
- when a procedural parser would be clearer;
- how the generated ordinary Rust can be inspected and tested without trusting the generator blindly;
- which simpler non-macro design was considered and why it is insufficient for this exact source-of-truth relationship.
