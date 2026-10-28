# Final review — Course 2: Ownership, Lifetimes, and Memory

## Part A — model reconstruction

1. Define a place and a move path.
2. Explain why two indexed mutable borrows require a different proof shape than two named fields.
3. Draw the loans created by a reborrow.
4. Derive a returned-reference lifetime from two unrelated inputs.
5. Explain a higher-ranked callback in terms of who chooses the lifetime.
6. Trace destruction order through nested scopes and temporary values.
7. Distinguish rollback guard, staged candidate, and consuming commit.
8. Explain what `Box` changes and what it does not.
9. Describe the metadata in a slice pointer and trait-object pointer without promising layout details not guaranteed.
10. Draw a graph with `Rc`, `Weak`, and borrowed edges and predict teardown.
11. Explain how a `RefCell` borrow panic can arise through reentrancy.
12. Classify a `size_of` result as observation or guarantee.
13. Derive variance from substitution rather than memorized labels.
14. Explain what `PhantomData` communicates.
15. State the promise of `Pin` and the role of `Unpin`.

## Part B — design incidents

Repair these without broadening authority:

- a function clones two records to avoid disjoint mutable borrowing;
- a parser uses one lifetime parameter for input and scratch storage that need not coincide;
- a callback returns a reference to a temporary buffer;
- a lease can be returned twice after an error;
- an `Rc` graph uses strong parent and child links;
- a cache invokes user code while holding a mutable `RefCell` guard;
- code serializes a struct by copying its in-memory bytes;
- an invariant marker is accidentally covariant;
- a pinning API exposes unrestricted `&mut T` to an address-sensitive value.

For each, name the invalid relationship and the narrowest mechanism that repairs it.

## Part C — independent construction

Build a versioned text-document arena with generational handles, borrowed views, staged replacement, immutable snapshots, weak observers, and a revision-aware cache. Add an address-sensitivity review that either justifies pinning with a concrete invariant or rejects it with a simpler design.

## Part D — defense

Explain every owner and liveness root, derive each public lifetime, trace cleanup after each error, classify every layout statement, and identify the exact point where runtime borrow enforcement begins. Course 2 is complete only if an unseen change can be made without replacing the design with `Rc<RefCell<_>>` everywhere.
