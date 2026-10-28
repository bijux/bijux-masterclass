# Laboratory 5 — Erased Validator Registry

[Course 10](../../README.md) · [Common laboratory method](../../../START_HERE.md#laboratory-method)

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

### Completion standard

You can justify erasure from an open heterogeneous requirement, keep normal behavior typed, and explain how trait evolution affects implementors and object users. A registry that downcasts every entry in order to do useful work has failed the design test.
