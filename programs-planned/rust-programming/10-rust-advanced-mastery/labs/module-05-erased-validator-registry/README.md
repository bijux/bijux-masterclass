# Laboratory 95 — Erased Validator Registry

**Course 10 · Module 95: Opaque and Erased Types: impl Trait, dyn Trait, Any, and Plugin Boundaries**

[Chapter](../../course-book/module-95-opaque-and-erased-types-impl-trait-dyn-trait-any-and-plugin-boundaries/index.md) · [Workbook](../../course-book/module-95-opaque-and-erased-types-impl-trait-dyn-trait-any-and-plugin-boundaries/workbook.md) · [AxiomStore guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Opaque and Erased Types: impl Trait, dyn Trait, Any, and Plugin Boundaries**: When should an API hide one concrete type, erase many concrete types behind a contract, or preserve explicit variants—and what information is lost at each boundary? The product must make **Distinguish opaque return types from trait objects and explain why different branches of `impl Trait` must share one hidden concrete type** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **open and erased variation map** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Product

Build a registry that stores heterogeneous validators behind one dyn-compatible contract. Validators are selected at runtime, have stable identities, execute in deterministic order, and return failures that preserve which validator rejected a record. The registry is an open extension boundary; the record model and ordinary validation path remain typed.

The starter provides one validator. Your task is to design the smallest useful erased interface and to keep type erasure at the registry boundary rather than spreading `Any`, strings, or downcasts throughout the product.

### Registry contract

The registry must:

- accept any `'static` implementation of `Validator`;
- reject duplicate stable names before changing state;
- preserve documented registration order;
- stop at the first failure or deliberately return all failures—choose and document one policy;
- retain validator identity in the failure value;
- expose names without exposing the internal `Vec<Box<dyn Validator>>`;
- validate without cloning the record.

Add at least three validators with different state: a maximum value length, a key-prefix policy, and a closure-backed adapter or configurable set membership rule.

### Dyn-compatibility review

For every method on `Validator`, explain why it is callable through `dyn Validator`. Construct one rejected redesign containing a generic method or a return of `Self`, and identify the dyn-compatibility rule that fails. Do not “repair” it by abandoning the runtime heterogeneous registry.

### `Any` boundary

Add an optional diagnostic capability only if you can justify it. If you use `Any`, it must be confined to an explicit opt-in method; ordinary validation must never branch on `TypeId`. Write one paragraph explaining why a `Box<dyn Any>` registry would be a bag of types rather than a behavioral architecture.

### Transfer

Add a validator versioning strategy. Pretend a future validator can supply a machine-readable code in addition to text. Compare an extension trait, a V2 trait plus adapter, and a required method added to the existing public trait. State the effect on downstream implementors and existing trait objects.

### Using the reference

Complete the registry and adversarial tests from `starter/`, then inspect `solution/`. Compare failure policy, deterministic order, duplicate handling, and public surface. The reference uses a minimal first-failure policy; an all-failures design is valid when it states ordering and allocation consequences.

### Mechanism-specific completion standard

You can justify erasure from an open heterogeneous requirement, keep normal behavior typed, and explain how trait evolution affects implementors and object users. A registry that downcasts every entry in order to do useful work has failed the design test.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Erased Validator Registry**.
2. Draw the smallest **open and erased variation map** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to AxiomStore so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Whole-laboratory completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Distinguish opaque return types from trait objects and explain why different branches of `impl Trait` must share one hidden concrete type.
- Derive dyn-compatibility requirements from the operations available through erased receivers.
- Choose borrowed, boxed, reference-counted, or inline-erased ownership according to registry and lifetime requirements.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 95 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **open and erased variation map**. Defend why your design is simpler than one plausible alternative under the new requirements.
