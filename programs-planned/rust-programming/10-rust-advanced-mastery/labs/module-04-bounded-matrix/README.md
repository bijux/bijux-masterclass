# Laboratory 4 — Bounded Matrix

[Course 10](../../README.md) · [Common laboratory method](../../../START_HERE.md#laboratory-method)

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

### Completion standard

You can identify which dimensions belong in type identity, construct unforgeable runtime witnesses, and avoid encoding configuration values as const generics merely because the syntax is available.
