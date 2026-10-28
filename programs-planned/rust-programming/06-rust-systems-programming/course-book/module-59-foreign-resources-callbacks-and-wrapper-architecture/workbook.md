# Workbook — Module 59: Foreign Resources, Callbacks, and Wrapper Architecture

[Chapter](index.md) · [Laboratory](../../labs/module-09-opaque-foreign-session/README.md) · [FrameVault guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Foreign Resources, Callbacks, and Wrapper Architecture** has become a usable model rather than remembered vocabulary. Its governing question is: *How do you wrap a foreign handle so ownership, borrowing, destruction, callbacks, reentrancy, and error channels become ordinary Rust obligations?* Preserve your first prediction and record decisive facts in a **foreign liveness graph**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 58 — C FFI: ABI, Strings, Pointers, and Error Boundaries that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **How do you wrap a foreign handle so ownership, borrowing, destruction, callbacks, reentrancy, and error channels become ordinary Rust obligations?**
3. Draw the smallest **foreign liveness graph** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

### Prediction 1

Two `Session` wrappers are created from one raw handle. What ownership defect follows?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 2

A borrowed descriptor is wrapped with `from_raw_fd` as owned. What can happen?

For **Prediction 2**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 3

A callback stores the entry-name pointer after return. Is the name still live?

For **Prediction 3**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 4

The callback frees the session during enumeration. Which pointer becomes invalid?

For **Prediction 4**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 5

A close error is handled by panicking in `Drop`. What failure can compound?

For **Prediction 5**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 6

The foreign function fails and `errno` is read after another call. Is the value reliable?

For **Prediction 6**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 7

An opaque pointer is copied by C. Is copying the address itself forbidden?

For **Prediction 7**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 8

A raw-pointer wrapper is manually marked `Sync`. What proof is required?

For **Prediction 8**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

## Part 2 — Diagnose and repair

### Boundary trace

Trace successful open as a transfer of one allocation obligation to the foreign caller. Then trace accessor borrows, callback-scoped views, early stop, error status, and exactly-once free. Mark forbidden reentrancy, retention, concurrent access, and post-free use.

For **Foreign Resources, Callbacks, and Wrapper Architecture**, choose table columns that expose the actual states rather than copying a generic checklist. Every row must name the owner, the fact established, the fact still delegated, the visible failure effect, and the component responsible for cleanup or rollback.

### Weak repairs to reject

For each prediction, identify a superficially convenient repair that violates the module contract. Reject at least these module-specific shortcuts:

- returning an opaque pointer without a matching free contract;
- reconstructing `Box` during a borrowing accessor;
- allowing callbacks to retain temporary pointers;
- freeing or mutating the active session from inside a callback;
- treating null and freed pointers as the same state;
- making concurrent use claims without synchronization;

Replace each with the smallest repair that preserves the requirement and state what evidence would distinguish the two designs.

## Part 3 — Focused exercises

### Construction 1

Design raw, shim, and safe layers for a mock foreign counter.

Required evidence: Keep ABI names in one module and expose ordinary Rust methods at the top.

### Construction 2

Implement `into_raw` and unsafe `from_raw` for an owner.

Required evidence: Show how drop responsibility transfers.

### Construction 3

Write a callback contract for synchronous enumeration.

Required evidence: Cover context validity, temporary data lifetime, early stop, reentrancy, and panic.

### Construction 4

Design explicit close plus fallback drop behavior.

Required evidence: Preserve close errors without double release.

### Construction 5

Transfer the architecture to an OS file descriptor accepted by a foreign library.

Required evidence: Prefer borrowing and identify the exact point where raw form is needed.

### Interleaved reasoning pass

1. For **Separate raw bindings, checked unsafe shims, and safe domain wrappers**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the foreign liveness graph.
2. For **Represent owned and borrowed foreign handles as different Rust types**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the foreign liveness graph.
3. For **Pair acquisition with exactly one release and define destructor failure policy**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the foreign liveness graph.
4. For **Design context-pointer callbacks with explicit lifetime, reentrancy, and retention rules**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the foreign liveness graph.

5. Identify one guarantee from an earlier course that a careless implementation of **Foreign Resources, Callbacks, and Wrapper Architecture** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Opaque Foreign Session](../../labs/module-09-opaque-foreign-session/README.md) from the starter. Freeze the public boundary and adversarial cases before opening the solution. Produce the evidence required by the lab:

- an ownership trace for open failure, open success, metadata read, enumeration, early stop, and free;
- tests proving the output session is null on open failure;
- callback tests for deterministic order and nonzero early termination;
- null-free and exactly-once successful release tests;
- a contract forbidding pointer retention, active-session free, and concurrent access during traversal.

Also identify one feature deliberately excluded because it would enlarge the trust, portability, concurrency, or unsafe proof surface.

### Laboratory acceptance trace

Before opening the reference implementation for **Opaque Foreign Session**, record:

- the public behavior that demonstrates **Separate raw bindings, checked unsafe shims, and safe domain wrappers**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Implement the matching increment from the [capstone engineering guide](../capstone.md). Add one regression test that fails if this module’s central contract is removed.

### Capstone invariant trace

For the Module 59 FrameVault increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Answer these questions without the chapter:

1. Who owns the allocation after open succeeds?
2. Which operations borrow and which consume?
3. How long may callback-derived views live?
4. What rules prevent double free, use after free, and reentrant invalidation?

End by naming the strongest honest claim after success and one claim the implementation deliberately does not make.

### Independent transfer

Wrap an owned Rust counter as an opaque foreign session. Provide open, get, checked update, synchronous visit callback, and free. Initialize the output session pointer to null before allocation. Define whether null free is allowed, whether callbacks may reenter or free the session, and whether callback pointers may be retained. Test complete lifecycle, overflow, early callback stop, and null rules. Identify the exact call after which the foreign pointer becomes unusable.

### Closed-book defense

In five minutes, answer “How do you wrap a foreign handle so ownership, borrowing, destruction, callbacks, reentrancy, and error channels become ordinary Rust obligations?” using the **foreign liveness graph**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside FrameVault. A list of APIs without the deciding relationship is incomplete.
