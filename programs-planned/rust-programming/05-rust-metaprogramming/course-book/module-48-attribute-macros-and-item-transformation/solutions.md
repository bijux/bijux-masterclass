# Reasoned solutions — Module 48: Attribute Macros and Item Transformation

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the CommandForge engineering guide](../capstone.md)

Use this file after freezing an independent attempt. In this module, compare byte-for-byte preservation of unrelated item properties, causal rejection of unsupported signatures, generated metadata naming, runtime behavior remaining ordinary Rust. A different implementation is valid only when those contracts survive; matching the reference token-for-token is irrelevant.

## Compiler specimen reasoning

### 1. `case-01/`

- **Outcome:** `compile-pass`
- **Governing rule:** an attribute macro may validate and preserve a supported public function.
- **Causal explanation:** The specimen compiles because an attribute macro may validate and preserve a supported public function.
- **Principled repair:** retain item preservation
- **Weak repair to reject:** replace the function body with generated behavior

### 2. `case-02/`

- **Outcome:** `compile-fail`
- **Governing rule:** attribute validation can reject a private function at its name span.
- **Causal explanation:** The compiler rejects the specimen because attribute validation can reject a private function at its name span.
- **Principled repair:** make it public or remove an attribute whose contract requires public API
- **Weak repair to reject:** have the macro silently change visibility

### 3. `case-03/`

- **Outcome:** `compile-fail`
- **Governing rule:** closed attribute grammars should reject unknown arguments.
- **Causal explanation:** The compiler rejects the specimen because closed attribute grammars should reject unknown arguments.
- **Principled repair:** remove the unsupported argument
- **Weak repair to reject:** ignore all attribute input

### 4. `case-04/`

- **Outcome:** `compile-fail`
- **Governing rule:** an attribute parser may restrict the attached item kind.
- **Causal explanation:** The compiler rejects the specimen because an attribute parser may restrict the attached item kind.
- **Principled repair:** attach it to a function or define a separate derive
- **Weak repair to reject:** string-search for fn tokens

### 5. `case-05/`

- **Outcome:** `compile-pass`
- **Governing rule:** attribute expansion may generate a typed companion item.
- **Causal explanation:** The specimen compiles because attribute expansion may generate a typed companion item.
- **Principled repair:** retain typed generated metadata
- **Weak repair to reject:** store the function name only as a string

### 6. `case-06/`

- **Outcome:** `compile-fail`
- **Governing rule:** generated companion names participate in the ordinary value namespace.
- **Causal explanation:** The compiler rejects the specimen because generated companion names participate in the ordinary value namespace.
- **Principled repair:** choose or configure a unique generated name
- **Weak repair to reject:** assume attribute-generated names cannot collide

### 7. `case-07/`

- **Outcome:** `compile-pass`
- **Governing rule:** ordinary attributes and function behavior survive item re-emission.
- **Causal explanation:** The specimen compiles because ordinary attributes and function behavior survive item re-emission.
- **Principled repair:** preserve the parsed ItemFn
- **Weak repair to reject:** regenerate a simplified signature

### 8. `case-08/`

- **Outcome:** `compile-fail`
- **Governing rule:** attribute arguments are parsed according to their declared syntax category.
- **Causal explanation:** The compiler rejects the specimen because attribute arguments are parsed according to their declared syntax category.
- **Principled repair:** supply an identifier or redesign the grammar deliberately
- **Weak repair to reject:** accept any tokens and generate an invalid identifier

## How to review the compiler specimens

The machine-readable outcomes are in [`compiler-labs/manifest.json`](../../compiler-labs/manifest.json). For **attribute ownership and item preservation**, compare your prediction against five questions:

1. Does the attribute validate only the item contract it owns and preserve unrelated visibility, ABI, safety, generics, and attributes?
2. Are generated companion names deterministic and protected from collisions?
3. Does the wrapper preserve argument evaluation, return behavior, and panic/error semantics?
4. Are unsupported item kinds and malformed attribute keys rejected at their authored spans?
5. Could an ordinary helper function or derive express the same relationship with a smaller public syntax surface?

Diagnostic prose may change between compiler releases. The isolated source shape and governing phase are the durable evidence.

## Broken-design repair

**Step 1.** Parse the attribute arguments with a closed grammar and reject unknown, duplicate, or malformed keys.

**Step 2.** Parse the attached item into the exact supported Rust item type. Reject other items and unsupported qualifiers with errors at their source spans.

**Step 3.** State preservation obligations before generation: original attributes, visibility, signature, generics, ABI, unsafety, asyncness, and body are preserved unless the attribute explicitly owns a transformation.

**Step 4.** Emit the original function unchanged and generate companion metadata or a deliberately named wrapper. Avoid duplicate evaluation and name collisions.

**Step 5.** Test public/private functions, generic signatures, unsupported async or unsafe functions, malformed metadata, and interaction with ordinary attributes.

The repaired design should make **attribute ownership and item preservation** smaller and more inspectable than the broken proposal. Judge it by whether one declaration owns the mechanical relationship, the expanded Rust remains readable, and each invalid input fails in the earliest phase that possesses the necessary information.

## Exercise reasoning

### Exercise 1 — Preservation ledger

A strong ledger explicitly preserves ordinary attributes, documentation, visibility, name, generics, where clause, ABI, return type, and body; validates the supported parameter and result shape; transforms nothing unless wrapping is required; and rejects qualifiers such as `async`, `const`, `unsafe`, variadic, or methods when the generated runtime cannot honor them.

### Exercise 2 — Attribute grammar

`about` accepts one nonempty string literal, `hidden` is a flag, unknown keys are errors, and duplicates are errors. Omitted `about` may default to a normalized function name only if documented; otherwise require it. Parse all arguments before generation.

### Exercise 3 — Signature validation

It can check syntactic arity, receiver absence, ownership form, explicit return presence, and perhaps that the outer written path ends in `Result`. It cannot prove alias semantics or trait implementations. Generated assignment to a typed function pointer can let Rust establish the exact callable type.

### Exercise 4 — Name collision

Use a deterministic transformation such as upper snake case plus a reserved suffix, and emit it in a controlled visibility. A user can still define the same name. Better designs allow an explicit metadata name or use a generated private module when stable access is not required. Collision behavior must be tested.

### Exercise 5 — Wrapper semantics

“After” behavior may not run on panic and may need a guard if cleanup is required. The wrapper must call the original exactly once, pass arguments once, preserve return and error values, and not change evaluation order. Logging is an effect and should be part of the attribute contract, not incidental output.

### Exercise 6 — Attribute ordering

Attribute macros receive and replace items in expansion order; one macro may see the output of another rather than the original item. Generated names and validation assumptions can interact. Public documentation should state supported composition or reject unsupported combinations rather than assuming commutativity.

## Laboratory comparison

The reference implementation is in [`labs/module-08-checked-handler-attribute/solution`](../../labs/module-08-checked-handler-attribute/solution). Review it in this order:

1. byte-for-byte preservation of unrelated item properties;
2. causal rejection of unsupported signatures;
3. generated metadata naming;
4. runtime behavior remaining ordinary Rust;

Keep your implementation when its **attribute ownership and item preservation** contract is at least as precise with a clearer or smaller design. Revise it when the reference exposes an accepted input, failure phase, generated-name rule, evaluation effect, or determinism obligation missing from your tests.

## Capstone review

For the Module 48 increment, a strong result demonstrates **validating and augmenting attached items without accidentally changing visibility, signature, attributes, generics, or runtime behavior**. The capstone should still read primarily as ordinary Rust. Generated surfaces must be compact enough to inspect through tests or expansion tools, and runtime domain behavior must remain callable without understanding macro internals.

## What a strong explanation includes

A strong defense of this module explains:

- why replacing the item gives the macro greater responsibility than derive;
- which item properties the attribute may change;
- what information remains unavailable before type checking;
- how generated companion names avoid collisions;
- how the generated ordinary Rust can be inspected and tested without trusting the generator blindly;
- which simpler non-macro design was considered and why it is insufficient for this exact source-of-truth relationship.
