# Review Engine

## Course role

Review Engine evaluates submissions against ordered policies. Generic source and reporting ports, a heterogeneous rule registry, coherence-safe adapters, typestate construction, and deterministic results make the choice of variation mechanism visible.

Review Engine is not a showcase of ten independent features. It is the place where the course’s mechanisms must coexist without creating a second owner for state, validation, order, failure, compatibility, or resource policy.

## Invariants carried through the product

- Every trait states a behavioral contract and its unencoded laws have contract tests.
- Generic source and reporter boundaries preserve precise associated type families.
- Dynamic rule order is runtime data and remains deterministic after type erasure.
- Coherence-safe adapters own their local implementation rights explicitly.
- Typestate removes incomplete engine construction from the callable API.
- Public evolution accounts separately for downstream callers and implementors.

## Module-to-product map

| Module | Mechanism added | Acceptance criterion |
|---:|---|---|
| 21 | Traits as Behavioral Contracts | Define a trait whose methods express a coherent behavioral contract |
| 22 | Associated Types and Type Families | Choose between generic parameters and associated types from relationship cardinality |
| 23 | Coherence and Implementation Ownership | Predict whether an implementation satisfies coherence and orphan rules |
| 24 | Static Polymorphism and Opaque Types | Design generic functions and types with the weakest sufficient bounds |
| 25 | Trait Objects and Dynamic Polymorphism | Derive whether a trait is dyn-compatible and repair it without erasing its meaning |
| 26 | Composition and OOP-Style Design Without Inheritance | Model encapsulation, substitution, and delegation without class inheritance |
| 27 | Typestate and Capability-Oriented APIs | Encode a finite protocol with marker states and consuming transitions |
| 28 | Boundary Traits and Adapters | Design extension traits, closure adapters, and conversion boundaries with precise contracts |
| 29 | Public API Evolution | Classify public trait changes by downstream source-compatibility risk |
| 30 | Architectural Synthesis | Map axes of variation before selecting polymorphism mechanisms |

## Reading route

1. Read the Review Engine contract and non-goals in the [engineering guide](../course-book/capstone.md).
2. Locate the type or component that owns each invariant above.
3. Run the baseline tests and one end-to-end demonstration before changing code.
4. Implement only the current module increment and its adversarial test.
5. Trace success, rejection, partial failure, cleanup, order, and capacity through the public surface.
6. Re-run the complete course route, then explain which claims remain conditioned on a compiler, target, scheduler, peer, workload, or operating system.

Review Engine evaluates ordered submissions against an ordered runtime policy. It is the Course 3 capstone and a complete standard-library-only library and CLI.

## Architecture

| Boundary | Mechanism | Reason |
|---|---|---|
| submission source | generic `Source` with associated item/error | one source selected per engine; associated errors remain precise |
| reporter | generic `Reporter` with associated output/error | caller retains concrete report output |
| policy rules | `Vec<Box<dyn Rule>>` | heterogeneous ordered rules selected from policy text at run time |
| built-in construction | `RuleFactory` registry | typed validation occurs before rule erasure |
| severity | enum | closed product domain with exhaustive rendering |
| engine construction | typestate builder | library callers cannot build without source, reporter, and policy |
| closure rule | local `RuleFn<F>` newtype | coherence-safe adaptation plus stable rule identity |
| built-in marker | sealed trait | downstream code may implement `Rule`, but cannot claim built-in status |

## Input format

`submissions.tsv` contains five tab-separated columns:

```text
id    owner    score    comma-separated-tags    title
```

Example:

```text
S-001	ada	92	rust,cli	A dependable command-line tool
S-002	root	55	prototype	Unreviewed draft
```

## Policy format

```text
min-score	70
require-tag	rust
title-length	5	80
deny-owner	root
```

Blank lines and lines beginning with `#` are ignored.

## Commands

```bash
review-engine check submissions.tsv policy.txt
review-engine list-rules
review-engine explain min-score
review-engine demo
```

Exit status:

- `0`: command succeeded and policy accepted all submissions;
- `1`: evaluation succeeded but at least one error-severity finding rejected a submission;
- `2`: usage, input, policy, or I/O failure.

## Verification

```bash
cargo fmt --manifest-path Cargo.toml -- --check
cargo clippy --manifest-path Cargo.toml --all-targets -- -D warnings
cargo test --manifest-path Cargo.toml --all-targets
cargo test --manifest-path Cargo.toml --doc
cargo build --manifest-path Cargo.toml --release
bash scripts/demo.sh
```
