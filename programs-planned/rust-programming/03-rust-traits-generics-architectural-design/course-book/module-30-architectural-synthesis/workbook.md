# Workbook — Module 30: Architectural Synthesis

[Return to the chapter](index.md) · [Open the Review Engine engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether you can use **Architectural Synthesis** without relying on surface syntax. Keep the module question in view: *Given a real source of variation, how do you choose among enums, generics, trait objects, closures, functions, and ordinary composition?* For every task, identify the program point where the decisive type, ownership, dispatch, failure, or cost relationship is established. Compile only after committing to a prediction, and preserve the smallest counterexample that changes your model.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Architectural Synthesis** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-hybrid-dispatch.rs`](../../compiler-labs/module-10/01-hybrid-dispatch.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-hybrid-associated-type-mismatch.rs`](../../compiler-labs/module-10/02-hybrid-associated-type-mismatch.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-registry-dyn-compatibility.rs`](../../compiler-labs/module-10/03-registry-dyn-compatibility.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-builder-state-gate.rs`](../../compiler-labs/module-10/04-builder-state-gate.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-coherence-adapter-need.rs`](../../compiler-labs/module-10/05-coherence-adapter-need.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-opaque-report-view.rs`](../../compiler-labs/module-10/06-opaque-report-view.rs) | Pass or fail? What exact rule decides? |
| 7 | [`07-object-lifetime-in-registry.rs`](../../compiler-labs/module-10/07-object-lifetime-in-registry.rs) | Pass or fail? What exact rule decides? |
| 8 | [`08-sealed-integrated-extension.rs`](../../compiler-labs/module-10/08-sealed-integrated-extension.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 03-rust-traits-generics-architectural-design
```

## Part 2 — Diagnose and repair

An unseen branch replaces enums with traits, generic ports with trait objects, and domain constructors with a dependency container. It compiles but loses exhaustive state handling, typed reporter output, and local invariants.

Restore a requirement-shaped architecture. Every retained trait must have a variation map entry and every erased boundary an erasure ledger.

## Part 3 — Focused exercises

1. Build a variation map for an unfamiliar media-review system.
2. Select mechanisms for eight dimensions and name alternatives.
3. Find duplicated semantics across static and dynamic paths.
4. Perform contract, coherence, dispatch, state, ownership, and evolution reviews.
5. Write two ADRs with reconsideration triggers.
6. Add a cross-cutting requirement to a public trait and produce a migration plan.
7. Remove one abstraction from the capstone and measure conceptual simplification.
8. Implement an unseen rule category without changing engine execution.
9. Change reporter output type and show why static dispatch preserves caller knowledge.
10. Prepare a ten-minute oral architecture defense.

### Variation map

For Review Engine, enumerate every place behavior or type may vary: source, parsed item, rule set, rule implementation, report format, output destination, construction state, and CLI command. For each, record:

- closed or open set;
- compile-time or runtime selection;
- one or many concrete types at once;
- ownership and lifetime;
- downstream implementation requirement;
- likely evolution direction.

Choose enum, generic parameter, associated type, trait object, closure, ordinary function, or concrete composition for each row. A mechanism may appear more than once only when the variation conditions differ.

### Architecture failure review

Seed these defects one at a time and explain the smallest architectural repair:

1. every component becomes `Box<dyn Trait>`;
2. every rule becomes a generic parameter on `Engine`;
3. the builder exposes a public generic `set_state`;
4. a blanket `Rule` impl covers every closure and blocks a specialized adapter;
5. source errors are erased into strings before the application can classify them;
6. adding a built-in rule changes nondeterministic report order.

### Changed requirement

The system must now support warning-only rules that do not reject a submission, plus an explanation command that describes configured rules without loading submissions. Update the variation map before code. Identify which existing traits need no change, which domain data changes, and whether the dynamic registry remains justified.

### Independent build

Implement a small inspection platform from a fresh crate using the same reasoning but different domain names. It must contain one static family relationship, one genuine runtime heterogeneous collection, one composition wrapper, and one staged construction invariant. Add a public API test written as though from a downstream crate.

### Final defense

Prepare a ten-minute explanation beginning with product variation rather than Rust features. For every trait, state its law and extension policy. For every generic, state the relationship it preserves. For every trait object, state what is erased and why. For every typestate parameter, state which illegal operation disappears.

## Part 4 — Independent laboratory

Build a separate miniature inspection platform from a product brief only.

It must contain:

- one closed enum variation;
- one generic associated-type boundary;
- one heterogeneous dyn-compatible registry;
- one coherence-safe adapter;
- one short typestate protocol;
- one intentionally concrete collaborator;
- downstream-style compatibility tests;
- an architecture decision record for every polymorphism mechanism.

The domain must differ from Review Engine. Copying names and structure without re-deriving decisions fails transfer.

The executable starter and reference implementation are in [module-10-inspection-platform](../../labs/module-10-inspection-platform/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

## Part 5 — Capstone transfer

Complete all commands, tests, documentation, and deterministic reports. Then implement the unseen feature supplied by the practical assessment, such as rule explanations, warning-only policies, or a new reporter family.

You must update:

- variation map;
- public contract review;
- compiler evidence;
- behavioral tests;
- semver hazard register;
- one ADR;
- oral defense.

Passing code without updated reasoning evidence is incomplete.

## Part 6 — Reconstruct and defend

Final prompt: **“Show the architecture as a set of decisions. For each trait, explain why it is not an enum, ordinary function, or concrete type.”**
### Closed-book reconstruction

1. For every polymorphic boundary, can you name the actual variation pressure?
2. Which relationships are closed enough for enums?
3. Which boundaries retain concrete types through generics or opaque returns?
4. Which runtime extension point justifies erasure?
5. Which protocol steps are made impossible through typestate, and which remain runtime checks?

### Independent transfer

Redesign Review Engine for one unseen requirement: policy groups with “all”, “any”, and “at least N” semantics. Produce a variation map before code. Decide what remains concrete, what becomes recursive data, whether dynamic rules still belong, how errors compose, and which public contracts change.
