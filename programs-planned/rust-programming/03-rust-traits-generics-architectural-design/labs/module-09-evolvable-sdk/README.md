# Laboratory 29 — Evolvable SDK

This is the independent product for **Course 3, Module 29: Public API Evolution**. Read the [module chapter](../../course-book/module-29-public-api-evolution/index.md) and complete its [workbook](../../course-book/module-29-public-api-evolution/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How can a public trait-based API evolve when downstream crates may both call it and implement it?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Start from a small public plugin contract and evolve it through two versions.

Requirements:

- downstream-style fixture crate implementing V1;
- a proposed breaking change and hazard analysis;
- a nonbreaking extension trait where semantics permit;
- a V2 trait where new required semantics cannot be defaulted;
- a newtype adapter from V1 to V2 with explicit information loss;
- a sealed internal trait and one open public trait;
- compile-positive and compile-negative compatibility evidence.

## Design focus

Treat the package as a public SDK with two downstream audiences: callers and implementors. Build one open extension trait, one sealed internal trait, and one non-exhaustive public data model. For every public item, record whether adding a method, variant, bound, blanket implementation, or supertrait would affect callers, implementors, or both.

Create a small downstream-style test crate that uses only the public API. Preserve it while making one compatible addition and deliberately demonstrate one breaking change in an isolated negative example. Avoid promising object safety or downstream implementation unless the product needs it; both promises restrict future evolution. The final README must state the extension policy in ordinary product language, not in semver slogans alone.

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

> How can a public trait-based API evolve when downstream crates may both call it and implement it?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Evolvable SDK**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
