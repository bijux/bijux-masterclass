# Workbook — Module 27: Typestate and Capability-Oriented APIs

[Chapter](index.md) · [Laboratory](../../labs/module-07-typestate-publication/README.md) · [Review Engine guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Typestate and Capability-Oriented APIs** has become a usable model rather than remembered vocabulary. Its governing question is: *Which illegal operations can be removed from the API by representing protocol state and authority in types?* Preserve your first prediction and record decisive facts in a **typestate transition graph**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 26 — Composition and OOP-Style Design Without Inheritance that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **Which illegal operations can be removed from the API by representing protocol state and authority in types?**
3. Draw the smallest **typestate transition graph** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Typestate and Capability-Oriented APIs** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-typestate-transition.rs`](../../compiler-labs/module-07/01-typestate-transition.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-unavailable-state-method.rs`](../../compiler-labs/module-07/02-unavailable-state-method.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-private-marker-construction.rs`](../../compiler-labs/module-07/03-private-marker-construction.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-consumed-transition-value.rs`](../../compiler-labs/module-07/04-consumed-transition-value.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-single-use-capability.rs`](../../compiler-labs/module-07/05-single-use-capability.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-incomplete-builder.rs`](../../compiler-labs/module-07/06-incomplete-builder.rs) | Pass or fail? What exact rule decides? |
| 7 | [`07-state-erasure-enum.rs`](../../compiler-labs/module-07/07-state-erasure-enum.rs) | Pass or fail? What exact rule decides? |
| 8 | [`08-sealed-state-parameter.rs`](../../compiler-labs/module-07/08-sealed-state-parameter.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 03-rust-traits-generics-architectural-design
```

## Part 2 — Diagnose and repair

A builder encodes five independent optional settings as present/missing type parameters. Signatures are unreadable and users cannot collect validation errors.

Keep typestate only for two truly mandatory components, move optional settings into ordinary fields, and make external configuration validation return a structured error list. Quantify the reduced state space.

## Part 3 — Focused exercises

1. Encode a three-state protocol with consuming transitions.
2. Preserve the original value on transition failure.
3. Seal public marker states.
4. Store state-specific evidence in a marker value.
5. Create a single-use capability token.
6. Build a two-required-field typestate builder.
7. Replace an eight-axis typestate with a runtime validator.
8. Bridge typestates into a closed runtime enum.
9. Explain why deserialization must revalidate state.
10. Design the capstone builder and identify which checks remain runtime.

### Protocol model

Design an upload session with states `New`, `Authenticated`, `Streaming`, and `Committed`. Write the legal transition graph before types. Decide which transitions consume the session, which return a recoverable error with the original state, and whether cancellation is represented by `Drop` or an explicit consuming method.

### Method availability

Sketch:

```rust
struct Session<S> { /* shared fields */ state: PhantomData<S> }
```

Place methods only on states that can perform them. Explain why a public `set_state<S2>` method would destroy the protocol. Decide which marker types and fields should be public.

### Fallible transition

Authentication can fail without invalidating the new session. Compare these returns:

```rust
Result<Session<Authenticated>, AuthError>
Result<Session<Authenticated>, (Session<New>, AuthError)>
TransitionError<Session<New>, AuthError>
```

Choose based on whether retry is a product requirement. Explain the ownership consequence, not only ergonomics.

### Staged builder

A client requires endpoint and credentials but has optional timeout and label. Compare runtime `Option` checks with typestate builder parameters. Estimate the number of public states if three more independently required fields are added. State the point at which the type-level design becomes more complex than the failure it prevents.

: erase after validation

Review Engine uses typestate during construction but a non-generic engine after `build`. Explain why erasing construction state at the boundary improves storage and downstream signatures. Add an unseen optional component without multiplying states unnecessarily.

### Architecture clinic — decide what belongs in the type

A deployment client has these properties:

- endpoint and credentials are mandatory before connection;
- timeout, label, retry count, compression, telemetry, and proxy are optional;
- credentials may fail validation but should remain available for correction;
- a configured client is stored in a heterogeneous job queue;
- serialized configuration must be revalidated when loaded.

Produce three designs:

1. all state checked at runtime;
2. every property represented by a typestate parameter;
3. typestate only for missing/present endpoint and credentials, with ordinary validated fields for the rest.

For each design, count the public state combinations, show the type returned by the final construction step, and explain what happens to the caller’s value when credential validation fails. Select one design and state the exact invariant gained for each added type parameter.

Then add a single-use `DeployPermit` capability. Decide whether possession of the permit, a role enum, or a Boolean flag should authorize deployment. Your answer must cover construction authority, duplication, storage, serialization, and auditability. Finally, erase the builder state into a non-generic runtime client and explain why the protocol proof remains valid after erasure.

### Interleaved reasoning pass

1. For **Encode a finite protocol with marker states and consuming transitions**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the typestate transition graph.
2. For **Decide which invalid operations deserve compile-time prevention**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the typestate transition graph.
3. For **Prevent construction of forbidden states through visibility and sealed state markers**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the typestate transition graph.
4. For **Erase typestate at a dynamic boundary without corrupting invariants**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the typestate transition graph.

5. Identify one guarantee from an earlier course that a careless implementation of **Typestate and Capability-Oriented APIs** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Implement `Draft -> Reviewed -> Published` with state-specific evidence.

Requirements:

- only drafts can be edited;
- review consumes a draft and can return it on failure;
- publication requires a single-use permit;
- marker states cannot be forged downstream;
- a runtime enum stores draft and reviewed values for persistence preparation;
- tests and compile-fail examples prove unavailable operations;
- a memo compares typestate with one runtime enum design.

The executable starter and reference implementation are in [module-07-typestate-publication](../../labs/module-07-typestate-publication/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

### Laboratory acceptance trace

Before opening the reference implementation for **Typestate Publication**, record:

- the public behavior that demonstrates **Encode a finite protocol with marker states and consuming transitions**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Implement typestate construction for source, reporter, and validated policy. `build` and `run` must be unavailable until all required components exist.

Keep policy-file parse errors at runtime. Do not encode optional report settings as independent type parameters. The final engine type should expose meaningful `S` and `R`, not construction markers.

### Capstone invariant trace

For the Module 27 Review Engine increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Pass when you can prevent a real invalid protocol step, preserve ownership on failure, prevent marker forgery, and reject typestate for an overlarge state space.

Oral prompt: **“Which invalid operation became impossible, and which invalid conditions correctly remain runtime errors?”**
### Closed-book reconstruction

1. Which invalid operation is removed from the method set by typestate?
2. Why should transitions consume the old state?
3. How can a failed transition return surviving ownership?
4. How do private marker types prevent downstream state forgery?
5. When does typestate create an unmanageable product of states?

### Independent transfer

Model a three-stage import protocol in which configuration, validation, and commit occur in order. Preserve the configured value on validation failure, prevent commit before validation, and explain which environmental failures must remain runtime `Result` values rather than type states.

### Closed-book defense

In five minutes, answer “Which illegal operations can be removed from the API by representing protocol state and authority in types?” using the **typestate transition graph**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside Review Engine. A list of APIs without the deciding relationship is incomplete.
