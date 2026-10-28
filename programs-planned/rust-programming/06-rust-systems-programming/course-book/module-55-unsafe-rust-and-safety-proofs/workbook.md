# Workbook — Module 55: Unsafe Rust as a Proof Boundary

[Return to the chapter](index.md) · [Open the FrameVault engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether the chapter has become an operational model. Freeze answers before compiling or reading the reference implementation. A correct result without the governing reason is incomplete.

## Part 1 — Predict

### Prediction 1

An unsafe block compiles. Has the compiler confirmed its pointer preconditions?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 2

A public function uses raw pointers internally but checks every precondition. Must it be `unsafe fn`?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 3

An `unsafe fn` dereferences a pointer without an inner unsafe block under the deny lint. What is missing?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 4

A private field becomes public. Why can unrelated unsafe code become unsound?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 5

A custom marker trait has no methods. Can its implementation still be unsafe?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 6

A test suite never crashes. Is undefined behavior excluded?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 7

A `no_mangle` export contains only safe arithmetic. Why is the attribute unsafe?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 8

A buffer length is incremented before element initialization, then initialization panics. What invariant fails?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

## Part 2 — Diagnose and repair

### Boundary trace

Create a safety ledger for each unsafe operation: exact operation, required preconditions, code establishing each precondition, validity duration, panic path, cleanup owner, and safe-caller protection. Keep the safe behavioral oracle beside the unsafe kernel.

For **Unsafe Rust as a Proof Boundary**, choose table columns that expose the actual states rather than copying a generic checklist. Every row must name the owner, the fact established, the fact still delegated, the visible failure effect, and the component responsible for cleanup or rollback.

### Weak repairs to reject

For each prediction, identify a superficially convenient repair that violates the module contract. Reject at least these module-specific shortcuts:

- placing an entire function in one broad unsafe block;
- using unsafe because a safe design feels verbose;
- copying a `SAFETY` comment without connecting it to code;
- assuming tests prove absence of undefined behavior;
- making a public function safe while leaving caller obligations undocumented;
- making a function public-unsafe merely because its body contains unsafe operations;

Replace each with the smallest repair that preserves the requirement and state what evidence would distinguish the two designs.

## Part 3 — Focused exercises

### Construction 1

Write the safety ledger for constructing a slice from a pointer and length.

Required evidence: Cover allocation, alignment, initialization, lifetime, and aliasing.

### Construction 2

Refactor an entire-function unsafe block into safe validation plus one unsafe expression.

Required evidence: Explain which checks establish each precondition.

### Construction 3

Decide whether three APIs should be safe or unsafe.

Required evidence: Base the decision on whether callers must provide unverifiable facts.

### Construction 4

Audit a type with raw pointer, length, and capacity fields.

Required evidence: Trace constructors, mutation, panic, drop, and auto-trait behavior.

### Construction 5

Transfer the proof method to a foreign callback receiving a context pointer.

Required evidence: State who creates it, how long it lives, and whether the callback may retain it.

## Part 4 — Independent laboratory

Build [Unsafe Slice Kernel](../../labs/module-05-unsafe-slice-kernel/README.md) from the starter. Freeze the public boundary and adversarial cases before opening the solution. Produce the evidence required by the lab:

- a safe reference implementation used as the behavioral oracle;
- a safety ledger for every raw-pointer construction, offset, and dereference;
- equivalence tests across empty, short, odd-length, and maximum test inputs;
- proof that loop bounds imply each pointer offset remains in the allocation;
- a review of every safe public route that can reach the unsafe kernel.

Also identify one feature deliberately excluded because it would enlarge the trust, portability, concurrency, or unsafe proof surface.

## Part 5 — Capstone transfer

Implement the matching increment from the [capstone engineering guide](../capstone.md). Add one regression test that fails if this module’s central contract is removed.

## Part 6 — Reconstruct and defend

Answer these questions without the chapter:

1. Which obligation does the compiler stop proving at the unsafe operation?
2. Which safe operation establishes each precondition?
3. How small is the reachable unsafe surface?
4. Can the same product contract be expressed in safe Rust instead?

End by naming the strongest honest claim after success and one claim the implementation deliberately does not make.

### Independent transfer

Choose one safe slice operation that the borrow checker cannot express directly without splitting or indexing indirection. Implement a safe reference version and a raw-pointer version. Before the unsafe block, write the full proof: allocation origin, bounds, distinctness, alignment, initialization, exclusive permission, owner lifetime, panic behavior, and returned lifetime. Use property-style tests to compare both implementations. Reject the raw version if it is not materially clearer or does not support a required abstraction boundary.
