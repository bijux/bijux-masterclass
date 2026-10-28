# Laboratory 59 — Opaque Foreign Session

**Course 6 · Module 59: Foreign Resources, Callbacks, and Wrapper Architecture**

[Chapter](../../course-book/module-59-foreign-resources-callbacks-and-wrapper-architecture/index.md) · [Workbook](../../course-book/module-59-foreign-resources-callbacks-and-wrapper-architecture/workbook.md) · [FrameVault guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Foreign Resources, Callbacks, and Wrapper Architecture**: How do you wrap a foreign handle so ownership, borrowing, destruction, callbacks, reentrancy, and error channels become ordinary Rust obligations? The product must make **Separate raw bindings, checked unsafe shims, and safe domain wrappers** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **foreign liveness graph** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How do you wrap a foreign handle so ownership, borrowing, destruction, callbacks, reentrancy, and error channels become ordinary Rust obligations?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Expose an opaque Rust-owned counter session through a C ABI. The interface creates one ownership obligation, supports synchronous callback enumeration, and consumes the session exactly once through a matching free function.

## Product-specific design pressure

This lab adds time to the FFI problem. A successful open creates one foreign ownership obligation; read operations borrow; callbacks receive temporary views; free consumes the handle. The opaque type hides Rust layout but cannot prevent a C caller from double-freeing or retaining borrowed pointers, so those obligations must be explicit and testable where possible.

## Contract

`counter_open(initial,out)` allocates a session. `counter_add`, `counter_get`, and `counter_visit` borrow it. `counter_free` consumes it and accepts null as a no-op. The visit callback is synchronous, may stop with nonzero status, may not retain pointers or free/reenter the session, and receives a caller context pointer.

## Required milestones

1. Keep the C-visible type opaque and the Rust representation private.
2. Write null to the out-handle before allocation.
3. Use `Box::into_raw` only after successful construction.
4. Reconstruct the box exactly once in free.
5. Define callback context and reentrancy rules.

## Adversarial cases

- null out-pointer
- null session borrow
- zero visits
- early callback stop
- context pointer collection
- null free
- checked arithmetic overflow
- double-free identified as caller violation rather than tested

## Evidence to produce

- an ownership trace for open failure, open success, metadata read, enumeration, early stop, and free;
- tests proving the output session is null on open failure;
- callback tests for deterministic order and nonzero early termination;
- null-free and exactly-once successful release tests;
- a contract forbidding pointer retention, active-session free, and concurrent access during traversal.

## Prohibited shortcuts

Do not reconstruct a `Box` more than once, treat a borrowed session pointer as owned, allow callbacks to retain stack views, free the active session from its callback, expose internal Rust layout, or hide ownership transfer behind an untyped success code. Null acceptance must be stated separately for each function rather than assumed globally.

## Transfer

Wrap the raw functions in a safe Rust owner with `Drop`, then expose a borrowed `SessionRef` that cannot outlive it.

## Comparing with the reference

Compare who owns the session after every branch. Verify that allocation occurs only after all fallible decoding succeeds, the output slot starts null, callbacks borrow from a live session for one invocation, and free is the only ownership-return operation. Then identify caller violations that no raw C API can reliably detect.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/` and do not open `solution/` until the contract, adversarial cases, and transfer are implemented or a precise blocker is written.

The laboratory is complete when the tests and documented failure paths pass, and you can answer this question without the chapter:

For **Laboratory 59 — Opaque Foreign Session**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Working route

1. Read the product contract and run the starter’s baseline checks for **Opaque Foreign Session**.
2. Draw the smallest **foreign liveness graph** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to FrameVault so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Separate raw bindings, checked unsafe shims, and safe domain wrappers.
- Represent owned and borrowed foreign handles as different Rust types.
- Pair acquisition with exactly one release and define destructor failure policy.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 59 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **foreign liveness graph**. Defend why your design is simpler than one plausible alternative under the new requirements.
