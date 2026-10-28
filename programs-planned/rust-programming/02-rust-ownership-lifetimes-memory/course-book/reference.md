# Course 2 reference — Ownership, Lifetimes, and Memory

This reference compresses the resource-topology tools used in Modules 11–20.

## Place and loan trace

For every disputed operation, record:

```text
place | current initialization | owner | active shared loans | active exclusive loan | next use
```

A place may be a variable, field, index, dereference, or projection. Moves and initialization are tracked per move path where Rust can prove the paths are distinct. Index expressions are harder to decompose statically; use standard split operations when you need two disjoint mutable regions.

## Lifetime derivation

A lifetime annotation names relationships; it does not extend storage.

1. Identify the owner of every reference.
2. For every returned reference, identify which input owner it comes from.
3. Keep unrelated inputs on unrelated lifetime parameters.
4. Let reborrowing shorten access whenever possible.
5. If output cannot be tied to an existing owner, return owned data.

Higher-ranked callback bounds are useful when the callee creates a temporary borrow and the callback must work for whichever short lifetime the callee chooses:

```rust
F: for<'a> FnOnce(&'a T) -> R
```

The callback may use the reference during the call but cannot choose a longer lifetime and make it escape.

## Cleanup and failure atomicity

Map every resource to one cleanup owner. Then trace normal return, early error, and unwinding.

| Pattern | Strong use |
|---|---|
| ordinary owned value | cleanup at scope exit |
| guard object | temporary protocol whose abandonment must restore state |
| consuming transition | prevent an old state from remaining usable |
| staged candidate | validate and build privately, then commit once |
| `Drop` | unconditional best-effort cleanup, not fallible business logic |

A destructor may not be relied on to run when the process aborts or memory is deliberately leaked. `Drop` is a local resource protocol, not a universal durability guarantee.

## Indirection and conditional ownership

- `Box<T>` provides owned indirection and gives recursive types a finite outer size.
- `&T` borrows; it does not own or extend lifetime.
- `Cow<'a, B>` expresses “borrow when unchanged, allocate when normalization requires ownership.”
- a fat pointer carries data address plus metadata such as slice length or trait-object metadata.
- `Deref` should model transparent access, not arbitrary conversion or expensive work.

## Shared ownership graph

Draw nodes and label edges:

- `Rc<T>`: strong liveness edge;
- `Weak<T>`: non-owning observation/backlink;
- `&T`: scoped borrow whose lifetime is tied to an existing owner.

Every strongly connected component of strong edges can leak. Parent-to-child ownership and weak child-to-parent links are a common acyclic topology. Count observations are diagnostic, not a substitute for the graph model.

## Interior mutability

Use `Cell<T>` for copy-like replace/get operations and `RefCell<T>` when runtime-checked borrows are the narrowest honest solution. Keep guards short. Never invoke unknown callbacks while a mutable `RefCell` guard is live. A runtime borrow panic indicates a protocol defect, not ordinary business failure.

## Representation claim ladder

Classify every memory statement:

1. Rust language guarantee;
2. standard-library contract;
3. representation attribute guarantee;
4. target-conditioned fact;
5. observation of one compiler/target/build;
6. unsupported assumption.

`size_of` does not establish field offsets, ABI compatibility, serialization layout, or future stability. Validity is stricter than “some bytes of the right size.”

## Variance and markers

Variance asks whether `Wrapper<MoreCapable>` may substitute for `Wrapper<LessCapable>`. Derive it from how the parameter is used; do not memorize labels without the substitution story. `PhantomData<T>` communicates semantic ownership, lifetime, variance, drop-check, and auto-trait relationships for a type parameter not stored directly.

## Pinning decision

Use pinning only when an invariant truly depends on stable address after initialization. Separate:

- the pointer being pinned;
- whether the pointee is `Unpin`;
- which fields are structurally pinned;
- how drop preserves the invariant.

Prefer handles, indices, owned indirection, or rebuilding when address sensitivity is avoidable.

## Course 2 readiness

You are ready for Course 3 when you can derive a borrowed API from provenance, prove cleanup on every exit path, draw a shared-ownership graph, control interior-borrow scope, classify layout claims, derive why a marker is variant or invariant, and reject unnecessary pinning with a concrete alternative.
