# Workbook — Module 28: Boundary Traits and Adapters

[Chapter](index.md) · [Laboratory](../../labs/module-08-boundary-ports/README.md) · [Review Engine guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Boundary Traits and Adapters** has become a usable model rather than remembered vocabulary. Its governing question is: *How should a Rust program adapt external data, effects, closures, and foreign types without contaminating its core model?* Preserve your first prediction and record decisive facts in a **adapter boundary map**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 27 — Typestate and Capability-Oriented APIs that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **How should a Rust program adapt external data, effects, closures, and foreign types without contaminating its core model?**
3. Draw the smallest **adapter boundary map** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Boundary Traits and Adapters** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-blanket-extension.rs`](../../compiler-labs/module-08/01-blanket-extension.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-extension-import.rs`](../../compiler-labs/module-08/02-extension-import.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-fn-versus-fnmut.rs`](../../compiler-labs/module-08/03-fn-versus-fnmut.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-tryfrom-validation.rs`](../../compiler-labs/module-08/04-tryfrom-validation.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-generic-port-associated-error.rs`](../../compiler-labs/module-08/05-generic-port-associated-error.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-trait-object-associated-error.rs`](../../compiler-labs/module-08/06-trait-object-associated-error.rs) | Pass or fail? What exact rule decides? |
| 7 | [`07-behavioral-fake.rs`](../../compiler-labs/module-08/07-behavioral-fake.rs) | Pass or fail? What exact rule decides? |
| 8 | [`08-bound-placement.rs`](../../compiler-labs/module-08/08-bound-placement.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 03-rust-traits-generics-architectural-design
```

## Part 2 — Diagnose and repair

A codebase has traits for clock, ID generator, parser, validator, formatter, repository, logger, configuration, and every service. Most have one implementation and tests mock call order.

Remove abstractions that do not isolate independent variation. Replace call-order mocks with behavioral fakes and contract tests. Keep only boundaries whose alternative implementations change for a concrete reason.

## Part 3 — Focused exercises

1. Add a convenience method through a blanket extension trait.
2. Wrap a closure as a named domain strategy and choose `Fn`, `FnMut`, or `FnOnce`.
3. Classify conversions among `From`, `TryFrom`, `AsRef`, `Borrow`, or named method.
4. Design one consumer-owned persistence port.
5. Compare generic and dynamic port storage.
6. Write a reusable contract test for two implementations.
7. Replace a call-order mock with a behavioral fake.
8. Reject or justify repository, visitor, and service patterns in three scenarios.
9. Move text parsing out of a domain core through an adapter.
10. Audit all capstone traits for independently variable boundaries.

### Port extraction

A service currently depends directly on `SystemTime`, `std::fs`, and terminal printing. Extract only the seams needed to make its decisions deterministic. For each proposed trait, list at least two real implementations or explain why a closure/function parameter is enough.

### Closure adapter

Design a local adapter that turns `F: Fn(&Submission) -> Vec<Finding>` into a `Rule`. Derive whether the adapter needs `Fn`, `FnMut`, or `FnOnce` from the rule's invocation contract. Explain what changes if the rule stores mutable counters.

### Conversion contract matrix

For each pair, choose `From`, `TryFrom`, `AsRef`, `Borrow`, or an explicit method:

- validated `Email` from `String`;
- `&Path` view from a path wrapper;
- lookup key view from a case-normalized key type;
- lossy external status to domain status;
- consuming domain ID back to its raw integer.

State the law or failure behavior implied by the chosen trait.

### Fake versus mock

Build a small in-memory source fake that preserves the same ordering and error contract as the production source. Identify behavior a simplistic vector stub could accidentally omit. Write one reusable contract test that both implementations must pass.

: boundary budget

List every trait at Review Engine's outer boundary. For each, answer: what changes independently, who supplies the implementation, whether a generic or object is needed, and what concrete alternative would look like. Remove abstractions that fail the test.

### Boundary review — translate a concrete external API

An external object store exposes twenty methods, vendor-specific request builders, three retryable status families, and one streaming download handle. Your application needs only:

- fetch one immutable policy document by logical name;
- distinguish not-found, temporarily unavailable, invalid content, and permanent external failure;
- replace the production adapter with an in-memory fake in domain tests;
- keep the streaming handle entirely outside the core.

Design the smallest port. State whether its key parameter should be owned, borrowed, or a validated newtype. Define the associated output and error relationship, then write the adapter’s translation table from vendor errors to application errors. Identify at least three vendor details that must not cross the port.

Next, implement the same port for a closure. Select `Fn`, `FnMut`, or `FnOnce` from the promised invocation pattern and explain whether a `'static`, `Send`, or `Sync` bound is justified. Finally, write two contract tests that both the production adapter and fake must satisfy. One must cover not-found behavior; the other must cover deterministic interpretation of invalid content.

### Interleaved reasoning pass

1. For **Design extension traits, closure adapters, and conversion boundaries with precise contracts**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the adapter boundary map.
2. For **Use generic or dynamic ports according to ownership and deployment needs**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the adapter boundary map.
3. For **Build test doubles that preserve the production contract rather than mirror internals**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the adapter boundary map.
4. For **Recognize visitor, repository, and service abstractions that add more ceremony than leverage**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the adapter boundary map.

5. Identify one guarantee from an earlier course that a careless implementation of **Boundary Traits and Adapters** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build a small inspection service with a domain core independent from input and output mechanisms.

Requirements:

- one consumer-owned source port with associated item/error types;
- one generic in-memory implementation and one text adapter;
- a closure adapter for a local policy;
- a behavioral fake with controlled failure injection;
- reusable contract tests;
- no trait for the concrete orchestrator unless a real second implementation exists;
- a boundary map showing where conversion and error translation occur.

The executable starter and reference implementation are in [module-08-boundary-ports](../../labs/module-08-boundary-ports/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

### Laboratory acceptance trace

Before opening the reference implementation for **Boundary Ports**, record:

- the public behavior that demonstrates **Design extension traits, closure adapters, and conversion boundaries with precise contracts**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Add:

- `RuleExt` convenience methods;
- `RuleFn<F>` closure adapter;
- source and reporter contract tests;
- policy text adapter producing validated specs;
- an in-memory fake source with failure injection used only in tests.

Remove any trait that has become a pass-through abstraction without independent variation.

### Capstone invariant trace

For the Module 28 Review Engine increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Pass when you can defend each remaining abstraction by a concrete change scenario, implement a contract-preserving fake, and keep raw external representations outside the domain core.

Oral prompt: **“Which trait did you remove, and what evidence showed it was abstraction debt?”**
### Closed-book reconstruction

1. What concrete change pressure justifies a boundary trait?
2. How can a closure adapter remove a one-method implementation without weakening the contract?
3. Why must a fake satisfy the same semantic laws as a production adapter?
4. How do `From`, `TryFrom`, `AsRef`, and `Borrow` communicate different promises?
5. Which raw external representations should stop at the adapter boundary?

### Independent transfer

Design a narrow clock or identifier source for an application core, with one production adapter, one deterministic fake, and one closure adapter. Write shared contract tests and an abstraction budget explaining why each public trait, conversion, and wrapper remains necessary.

### Closed-book defense

In five minutes, answer “How should a Rust program adapt external data, effects, closures, and foreign types without contaminating its core model?” using the **adapter boundary map**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside Review Engine. A list of APIs without the deciding relationship is incomplete.
