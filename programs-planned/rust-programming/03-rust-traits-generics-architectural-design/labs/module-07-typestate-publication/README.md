# Laboratory 27 — Typestate Publication

This is the independent product for **Course 3, Module 27: Typestate and Capability-Oriented APIs**. Read the [module chapter](../../course-book/module-27-typestate-and-capability-oriented-apis/index.md) and complete its [workbook](../../course-book/module-27-typestate-and-capability-oriented-apis/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> Which illegal operations can be removed from the API by representing protocol state and authority in types?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Implement `Draft -> Reviewed -> Published` with state-specific evidence.

Requirements:

- only drafts can be edited;
- review consumes a draft and can return it on failure;
- publication requires a single-use permit;
- marker states cannot be forged downstream;
- a runtime enum stores draft and reviewed values for persistence preparation;
- tests and compile-fail examples prove unavailable operations;
- a memo compares typestate with one runtime enum design.

## Design focus

Model a short publication protocol with consuming transitions such as draft, validated, and published. Methods that are illegal in a state must be absent from that state’s method set; they must not merely return a late Boolean error. Keep marker types and fields private enough that callers cannot forge readiness. Preserve useful data when a transition fails by returning an error that carries the surviving state where appropriate.

Do not encode external uncertainty in typestate. File availability, network response, and user-provided content remain runtime concerns. Tests should cover the valid transition path, validation failure, compile-fail attempts to publish too early, and the inability to reuse a consumed state. Explain why an enum state machine would be preferable if states must be stored heterogeneously or selected entirely at run time.

## Working route

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/`, add the first adversarial test before the design-changing repair, and complete the workbook’s transfer problem before reading the reference implementation.

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

> Which illegal operations can be removed from the API by representing protocol state and authority in types?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Typestate Publication**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
