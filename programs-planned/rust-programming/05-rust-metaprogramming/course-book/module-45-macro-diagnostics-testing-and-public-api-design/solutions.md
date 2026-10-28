# Reasoned solutions — Module 45: Macro Diagnostics, Testing, and Public API Design

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the CommandForge engineering guide](../capstone.md)

Use this file after freezing an independent attempt. In this module, compare whether each negative case fails for one intended cause, whether diagnostics identify the caller-owned token, whether valid expansions are tested as public behavior, whether a syntax extension would be backwards-compatible. A different implementation is valid only when those contracts survive; matching the reference token-for-token is irrelevant.

## Compiler specimen reasoning

### 1. `case-01.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** positive tests should assert observable expansion semantics.
- **Causal explanation:** The specimen compiles because positive tests should assert observable expansion semantics.
- **Principled repair:** retain an evaluation-count assertion
- **Weak repair to reject:** test only the final value with a pure expression

### 2. `case-02.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** targeted compile_error output makes rejected syntax intentional.
- **Causal explanation:** The compiler rejects the specimen because targeted compile_error output makes rejected syntax intentional.
- **Principled repair:** fix the declaration to the documented grammar
- **Weak repair to reject:** delete the negative test

### 3. `case-03.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** a diagnostic catalog can generate deterministic forward and reverse mappings.
- **Causal explanation:** The specimen compiles because a diagnostic catalog can generate deterministic forward and reverse mappings.
- **Principled repair:** retain one source declaration
- **Weak repair to reject:** maintain independent handwritten tables

### 4. `case-04.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** duplicate generated numeric match patterns should be rejected as a catalog defect.
- **Causal explanation:** The compiler rejects the specimen because duplicate generated numeric match patterns should be rejected as a catalog defect.
- **Principled repair:** validate uniqueness or remove the duplicate
- **Weak repair to reject:** allow first-match runtime behavior to hide the conflict

### 5. `case-05.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** negative and positive contracts can coexist in ordered matcher rules.
- **Causal explanation:** The specimen compiles because negative and positive contracts can coexist in ordered matcher rules.
- **Principled repair:** retain specific-first rule order
- **Weak repair to reject:** put the catch-all first

### 6. `case-06.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** generated stronger trait bounds are a compatibility surface.
- **Causal explanation:** The compiler rejects the specimen because generated stronger trait bounds are a compatibility surface.
- **Principled repair:** remove the unnecessary bound or satisfy a justified contract
- **Weak repair to reject:** clone token text instead of the value

### 7. `case-07.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** small semantic assertions are more stable than full token snapshots.
- **Causal explanation:** The specimen compiles because small semantic assertions are more stable than full token snapshots.
- **Principled repair:** assert normalized contract surfaces
- **Weak repair to reject:** snapshot compiler debug formatting

### 8. `case-08.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** malformed public syntax should fail during compilation rather than at runtime.
- **Causal explanation:** The compiler rejects the specimen because malformed public syntax should fail during compilation rather than at runtime.
- **Principled repair:** use the documented comma-separated grammar
- **Weak repair to reject:** capture arbitrary tt and parse a string at runtime

## How to review the compiler specimens

The machine-readable outcomes are in [`compiler-labs/manifest.json`](../../compiler-labs/manifest.json). For **diagnostic causality and compatibility**, compare your prediction against five questions:

1. What invalid form should be rejected by the macro rather than by a later type error?
2. Does the diagnostic point at the token the caller can actually change?
3. Can a malformed input accidentally match a permissive fallback and produce a misleading cascade?
4. Are positive expansion behavior and negative diagnostic behavior both covered by stable tests?
5. Would broadening the accepted grammar create an API compatibility promise the design cannot maintain?

Diagnostic prose may change between compiler releases. The isolated source shape and governing phase are the durable evidence.

## Broken-design repair

**Step 1.** Write the accepted grammar and the intentionally rejected near-misses as part of the public contract.

**Step 2.** Create positive tests for representative valid forms, expansion-behavior tests for evaluation count and order, and negative compiler fixtures for each important misuse.

**Step 3.** Use targeted fallback rules or span-aware procedural errors. Test the intended cause, not merely nonzero compiler status.

**Step 4.** Treat newly accepted syntax, changed expansion paths, generated item names, evaluation changes, and diagnostic movement as compatibility-relevant decisions.

**Step 5.** Prefer semantic assertions over one giant token snapshot. Snapshot only small normalized surfaces whose exact shape is itself the contract.

The repaired design should make **diagnostic causality and compatibility** smaller and more inspectable than the broken proposal. Judge it by whether one declaration owns the mechanical relationship, the expanded Rust remains readable, and each invalid input fails in the earliest phase that possesses the necessary information.

## Exercise reasoning

### Exercise 1 — Test matrix

Each quadrant needs a distinct proof. Positive compile tests cover accepted forms; generated trait bounds can be exercised by downstream type-check failures; invalid syntax needs compile-fail cases with intended diagnostic causes; runtime tests must verify evaluation order, side effects, and output. One snapshot cannot cover all four.

### Exercise 2 — Diagnostic ownership

A procedural semantic validator sees all literal route declarations during compilation and can point at the duplicate. Runtime rejection is too late and allows an invalid catalog to compile. Parser rejection is the wrong layer because each entry is syntactically valid.

### Exercise 3 — Weak negative test

The fixture may fail for a missing import, typo, outdated dependency, or unrelated type mismatch. A trustworthy negative case records the intended rule and inspects stable diagnostic text or uses a carefully isolated source shape so incidental failure cannot satisfy the test.

### Exercise 4 — Compatibility surface

Examples include changed generated item names or visibility, changed evaluation count or order, different path resolution, stronger generated trait bounds, moved error spans, altered expansion category, and changes to whether arguments are moved or borrowed. Macro compatibility includes expanded semantics, not syntax alone.

### Exercise 5 — Fallback design

The specific matcher recognizes the nearby malformed shape and emits `compile_error!("expected `Variant = CODE => MESSAGE`")`. The generic fallback reports unsupported diagnostic syntax. First-match semantics require the specific case to precede the catch-all.

### Exercise 6 — Snapshot discipline

Normalize and snapshot the route model or help table when ordering and text are contract. Generated public constants may receive focused assertions. Full AST debug output and compiler prose are unstable implementation details. Test diagnostic cause through stable substrings or structured tools rather than entire messages.

## Laboratory comparison

The reference implementation is in [`labs/module-05-diagnostic-enum-macro/solution`](../../labs/module-05-diagnostic-enum-macro/solution). Review it in this order:

1. whether each negative case fails for one intended cause;
2. whether diagnostics identify the caller-owned token;
3. whether valid expansions are tested as public behavior;
4. whether a syntax extension would be backwards-compatible;

Keep your implementation when its **diagnostic causality and compatibility** contract is at least as precise with a clearer or smaller design. Revise it when the reference exposes an accepted input, failure phase, generated-name rule, evaluation effect, or determinism obligation missing from your tests.

## Capstone review

For the Module 45 increment, a strong result demonstrates **treating accepted syntax, rejected syntax, diagnostics, expansion behavior, and compatibility as one macro API**. The capstone should still read primarily as ordinary Rust. Generated surfaces must be compact enough to inspect through tests or expansion tools, and runtime domain behavior must remain callable without understanding macro internals.

## What a strong explanation includes

A strong defense of this module explains:

- why compile failure alone is not sufficient negative evidence;
- which errors the macro should emit directly;
- which errors should remain ordinary Rust type errors;
- how diagnostic and grammar changes affect versioning;
- how the generated ordinary Rust can be inspected and tested without trusting the generator blindly;
- which simpler non-macro design was considered and why it is insufficient for this exact source-of-truth relationship.
