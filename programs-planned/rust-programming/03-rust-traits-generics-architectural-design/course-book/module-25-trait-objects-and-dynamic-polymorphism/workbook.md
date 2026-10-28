# Workbook — Module 25: Trait Objects and Dynamic Polymorphism

[Chapter](index.md) · [Laboratory](../../labs/module-05-dynamic-command-bus/README.md) · [Review Engine guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Trait Objects and Dynamic Polymorphism** has become a usable model rather than remembered vocabulary. Its governing question is: *When is run-time heterogeneity real, what information does a trait object erase, and what must remain dispatchable?* Preserve your first prediction and record decisive facts in a **dynamic-dispatch map**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 24 — Static Polymorphism and Opaque Types that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **When is run-time heterogeneity real, what information does a trait object erase, and what must remain dispatchable?**
3. Draw the smallest **dynamic-dispatch map** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Trait Objects and Dynamic Polymorphism** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-explicit-dyn.rs`](../../compiler-labs/module-05/01-explicit-dyn.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-generic-method-dyn-incompatibility.rs`](../../compiler-labs/module-05/02-generic-method-dyn-incompatibility.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-self-return-dyn-incompatibility.rs`](../../compiler-labs/module-05/03-self-return-dyn-incompatibility.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-associated-constant-dyn-incompatibility.rs`](../../compiler-labs/module-05/04-associated-constant-dyn-incompatibility.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-associated-type-specification.rs`](../../compiler-labs/module-05/05-associated-type-specification.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-self-sized-escape.rs`](../../compiler-labs/module-05/06-self-sized-escape.rs) | Pass or fail? What exact rule decides? |
| 7 | [`07-borrowed-object-lifetime.rs`](../../compiler-labs/module-05/07-borrowed-object-lifetime.rs) | Pass or fail? What exact rule decides? |
| 8 | [`08-heterogeneous-registry.rs`](../../compiler-labs/module-05/08-heterogeneous-registry.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 03-rust-traits-generics-architectural-design
```

## Part 2 — Diagnose and repair

A team made a trait dyn-compatible by deleting typed errors, generic writer support, and configuration validation. The resulting `fn run(&self, input: &str) -> String` hides every failure and semantic distinction.

Repair it by separating:

- typed construction;
- stable dyn execution;
- generic convenience methods in an extension trait;
- caller-visible domain errors.

The final design must explain each erased capability and why it is not needed at runtime.

## Part 3 — Focused exercises

1. Audit ten methods for dyn compatibility and cite the decisive rule.
2. Move a generic writer method to a `Self: Sized` extension surface.
3. Replace a `Self` return with a dyn-compatible clone-box contract, then explain its cost.
4. Form a trait object with fixed associated types.
5. Correct an unnecessary `'static` bound on a borrowed rule.
6. Build a heterogeneous registry with deterministic iteration.
7. Compare enum, generic, and dyn designs for four change scenarios.
8. Replace downcasting with explicit domain introspection.
9. Separate factory construction from erased execution.
10. Complete the capstone erasure ledger.

### Dyn-compatibility clinic

Review this trait for use behind `dyn Plugin`:

```rust
trait Plugin {
    fn name(&self) -> &str;
    fn parse<T: FromStr>(&self, input: &str) -> Result<T, T::Err>;
    fn create() -> Self;
}
```

Identify each dyn-incompatible member and explain the reason in terms of erased receiver type and vtable-callable behavior. Redesign the boundary around a concrete domain request and response rather than merely adding `where Self: Sized` everywhere.

### Ownership of the object

Compare these registry entries:

```rust
&dyn Rule
Box<dyn Rule>
Rc<dyn Rule>
Arc<dyn Rule>
```

For each, state who owns the implementation, how long it may live, whether sharing is single- or multi-threaded, and which extra trait bounds a threaded registry would need. Choose the narrowest representation for a single-threaded CLI that owns its configured rules.

### Object lifetime

Design a rule object that borrows configuration text. Write the explicit object lifetime in `Box<dyn Rule + 'a>` and explain why `Box<dyn Rule>` often implies a `'static` object bound in that position. Decide whether borrowing configuration is worth propagating the lifetime through the registry.

### Enum or trait object?

A policy currently has four closed rule variants. Compare an enum-based reviewer with a trait-object registry under these future scenarios: adding variants only in the same crate, loading third-party plugins, exhaustive reporting per variant, and serializing configuration. Produce a decision table.

: registry defense

For Review Engine, document the exact point at which concrete rule types are erased, the operations still available afterward, and the information that cannot be recovered without an explicit downcasting design. Add one test proving deterministic registration order.

### Interleaved reasoning pass

1. For **Derive whether a trait is dyn-compatible and repair it without erasing its meaning**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the dynamic-dispatch map.
2. For **Use borrowed and owned trait objects with correct object lifetimes**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the dynamic-dispatch map.
3. For **Build a heterogeneous runtime collection behind one behavioral interface**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the dynamic-dispatch map.
4. For **Compare enum, generic, and trait-object designs against explicit change scenarios**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the dynamic-dispatch map.

5. Identify one guarantee from an earlier course that a careless implementation of **Trait Objects and Dynamic Polymorphism** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build a command bus that owns heterogeneous command handlers behind a dyn-compatible interface.

Requirements:

- a stable command envelope and typed execution result;
- at least three concrete handlers;
- deterministic registration and dispatch;
- no downcasting in ordinary execution;
- a separate factory or constructor surface for handler-specific configuration;
- borrowed-handler support demonstrated through an explicit object lifetime;
- a comparison with a closed command enum.

The executable starter and reference implementation are in [module-05-dynamic-command-bus](../../labs/module-05-dynamic-command-bus/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

### Laboratory acceptance trace

Before opening the reference implementation for **Dynamic Command Bus**, record:

- the public behavior that demonstrates **Derive whether a trait is dyn-compatible and repair it without erasing its meaning**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Replace the homogeneous rule set with `Vec<Box<dyn Rule>>`. Keep `Source` and `Reporter` generic.

Acceptance points:

- `Rule` is dyn-compatible;
- construction errors remain typed before erasure;
- rule and finding order is deterministic;
- no downcasting is used for identity;
- borrowed rules can be expressed where useful without forcing all rules to `'static`;
- a policy parser constructs concrete built-ins and erases only after validation.

### Capstone invariant trace

For the Module 25 Review Engine increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

You must derive dyn compatibility from signatures, explain object lifetimes, build a heterogeneous registry, and defend enum/generic/dyn choices for three boundaries.

Oral prompt: **“What information did this trait object erase, and what evidence shows the caller does not need it?”**
### Closed-book reconstruction

1. What information is erased behind `dyn Trait`?
2. Which method shapes make a trait unavailable through a trait object?
3. Where does an omitted trait-object lifetime bound come from?
4. Why is a heterogeneous registry a stronger justification than “the type is long”?
5. When is a closed enum more informative than dynamic dispatch?

### Independent transfer

Design a runtime-loaded validation registry for three unrelated validators. Then redesign the same closed set as an enum and as a generic pipeline. State which changes each version supports, which operations remain exhaustive, what is erased, and why the selected boundary deserves runtime dispatch.

### Closed-book defense

In five minutes, answer “When is run-time heterogeneity real, what information does a trait object erase, and what must remain dispatchable?” using the **dynamic-dispatch map**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside Review Engine. A list of APIs without the deciding relationship is incomplete.
