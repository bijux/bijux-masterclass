# Laboratory 94 — Bounded Matrix

**Course 10 · Module 94: Const Generics, Witness Types, and Compile-Time Invariants**

[Chapter](../../course-book/module-94-const-generics-witness-types-and-compile-time-invariants/index.md) · [Workbook](../../course-book/module-94-const-generics-witness-types-and-compile-time-invariants/workbook.md) · [AxiomStore guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Const Generics, Witness Types, and Compile-Time Invariants**: Which numeric and state facts belong in types, which remain runtime data, and how do you avoid turning a library into an unusable type-level calculator? The product must make **Use const parameters when a numeric fact changes representation, layout, or legal composition** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **const witness proof** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Product

Build a fixed-shape matrix whose row and column counts are part of its type. Matrix multiplication should compile only when the left inner dimension and right row dimension are equal. Indexing through the public checked path uses a witness that proves an index is within the corresponding const-generic bound.

The laboratory separates three classes of fact: shape known statically, indices validated at runtime into a witness, and arithmetic properties that remain runtime or trait obligations. Do not claim that const generics make every matrix invariant compile-time decidable.

### Required surface

Implement:

- `BoundedIndex<N>::new(usize) -> Option<BoundedIndex<N>>`;
- `Matrix<T, R, C>::new([[T; C]; R])`;
- checked `get` using `BoundedIndex<R>` and `BoundedIndex<C>`;
- multiplication from `Matrix<T, R, K>` and `Matrix<T, K, C>` to `Matrix<T, R, C>`;
- a read-only view or iterator that preserves row-major order.

State the numeric trait requirements precisely. If you choose `Default` as the additive identity, document that assumption; a more general design may accept an explicit zero value or algebraic policy.

### Boundary cases

Test zero rows, zero columns, and zero inner dimension wherever Rust’s array types permit construction. `BoundedIndex<0>::new(0)` must fail. Multiplication with an empty inner dimension must produce the documented additive identity rather than panic. Include maximum valid and first invalid indices for more than one dimension.

Create a compile-fail case for multiplying incompatible shapes. The error should be a type mismatch between const parameters, not an intentional syntax failure.

### Witness analysis

Explain what the private witness field protects and why exposing a public tuple constructor would let callers forge invalid indices. Show where runtime validation ends and compile-time reuse begins: once constructed, the witness can be used repeatedly without another bounds check in the public model.

### Transfer

Introduce a runtime-configured matrix imported from a file. Decide where the const-generic representation stops being appropriate. Provide a conversion into one of a finite supported shape set or retain a dynamic matrix; justify the choice through caller requirements rather than a preference for type-level programming.

### Using the reference

After your own shape and witness tests pass, inspect `solution/`. Compare numeric assumptions, zero-dimensional behavior, and API visibility. A more elaborate implementation is not stronger unless its additional abstraction removes a real invalid state.

### Mechanism-specific completion standard

You can identify which dimensions belong in type identity, construct unforgeable runtime witnesses, and avoid encoding configuration values as const generics merely because the syntax is available.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Bounded Matrix**.
2. Draw the smallest **const witness proof** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to AxiomStore so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Whole-laboratory completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Use const parameters when a numeric fact changes representation, layout, or legal composition.
- Construct witness types only through checked functions and preserve their proof through private fields.
- Distinguish compile-time capacity from runtime length and enforce both without off-by-one ambiguity.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 94 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **const witness proof**. Defend why your design is simpler than one plausible alternative under the new requirements.
