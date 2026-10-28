# Workbook — Module 21: Traits as Behavioral Contracts

[Chapter](index.md) · [Laboratory](../../labs/module-01-contract-boundaries/README.md) · [Review Engine guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Traits as Behavioral Contracts** has become a usable model rather than remembered vocabulary. Its governing question is: *What behavior truly belongs in a shared contract, and which laws must every implementation preserve?* Preserve your first prediction and record decisive facts in a **trait-law table**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 20 — Pinning and Address-Sensitive Design that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **What behavior truly belongs in a shared contract, and which laws must every implementation preserve?**
3. Draw the smallest **trait-law table** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Traits as Behavioral Contracts** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-trait-import.rs`](../../compiler-labs/module-01/01-trait-import.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-missing-generic-bound.rs`](../../compiler-labs/module-01/02-missing-generic-bound.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-default-method.rs`](../../compiler-labs/module-01/03-default-method.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-ambiguous-method.rs`](../../compiler-labs/module-01/04-ambiguous-method.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-self-sized-boundary.rs`](../../compiler-labs/module-01/05-self-sized-boundary.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-supertrait-obligation.rs`](../../compiler-labs/module-01/06-supertrait-obligation.rs) | Pass or fail? What exact rule decides? |
| 7 | [`07-conditional-implementation.rs`](../../compiler-labs/module-01/07-conditional-implementation.rs) | Pass or fail? What exact rule decides? |
| 8 | [`08-consuming-receiver.rs`](../../compiler-labs/module-01/08-consuming-receiver.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 03-rust-traits-generics-architectural-design
```

## Part 2 — Diagnose and repair

The supplied design has one trait with `load`, `validate`, `transform`, `save`, and `display`, then implements it for two unrelated domain types. Tests require large fake objects and every new display format modifies the persistence abstraction.

Your repair must:

1. identify the consumers of each operation;
2. split the contract by consumer capability;
3. keep domain validation on the domain type unless multiple external validators are an actual requirement;
4. use a free function where behavior combines two values rather than characterizes one type;
5. write one law test shared by at least two implementations;
6. explain why fewer traits would also be a credible design.

A repair that creates five one-method getter traits does not pass.

## Part 3 — Focused exercises

1. **Mechanism selection:** For logging a concrete `Order`, compare an inherent method, free function, enum strategy, and trait. Select one under two different change scenarios.
2. **Minimal bound:** Write a function that prints two values separated by a slash. Add only the required bound.
3. **Law extraction:** Define three semantic laws for a `Normalize` trait and identify one type that cannot honestly implement it.
4. **Receiver design:** Choose `self`, `&self`, or `&mut self` for `finish`, `peek`, `advance`, and `reset`; justify each.
5. **Default review:** Decide whether a default `retry` method belongs on a `Send` trait when implementations have different idempotence guarantees.
6. **Supertrait audit:** Replace a nominal `Entity: Named + Identified + Serializable` hierarchy with consumer-oriented capabilities.
7. **UFCS:** Resolve two traits with the same associated function and explain why method syntax cannot infer the intended implementation.
8. **Contract tests:** Write a reusable law test for two `BoundedScore` implementations.
9. **Trait deletion:** Given a trait with one implementation and one generic caller, produce a simpler concrete design and state what extensibility is lost.
10. **Public surface:** State whether downstream crates may implement your trait and how that decision affects future required methods.

### Contract workshop: a formatter is not yet a trait

A codebase has three report types with methods named `render`, but their promises differ. One returns a stable user-facing string, one emits debug detail, and one may redact fields depending on configuration.

1. Write the behavioral law you would require before placing any two of these types behind one `Render` trait.
2. Decide whether redaction belongs in the receiver, an argument, a separate strategy, or a wrapper. State what a caller may rely on after your choice.
3. Choose `self`, `&self`, or `&mut self` for each operation. For every receiver, name the ownership or mutation fact it communicates.
4. Design one default method that follows mechanically from required methods. Then give a counterexample showing why a different tempting default would be semantically unsafe.

### Bound derivation

Start with this desired function:

```rust
fn summarize<T>(items: &[T]) -> String {
    // one item per line, using the public display form
}
```

Derive the weakest sufficient bound from the body. Compare `T: Display`, `T: Debug`, `T: ToString`, and a custom `Summary` trait. Explain which are technically sufficient and which communicate the intended contract best. Then rewrite the signature with a `where` clause only if it improves readability.

### Law test design

Define a `Normalize` contract for identifiers. Its intended laws are idempotence and preservation of already-valid identifiers. Write concrete property-style tests over a small table without adding a property-testing dependency. Include at least one hostile Unicode input and one input that is invalid rather than normalizable. Decide whether failure belongs in the return type or in a separate validation operation.

### Method resolution diagnosis

Create a type with an inherent `describe` method and implement two traits that also define `describe`. Predict each call below before compiling:

```rust
value.describe();
TraitA::describe(&value);
TraitB::describe(&value);
<Type as TraitA>::describe(&value);
```

Explain when UFCS is only disambiguation and when it reveals an important contract choice to a reader.

: contract review

Choose one public trait from a project you know. Rewrite its documentation as a contract containing: purpose, required behavior, receiver semantics, laws, failure behavior, and one non-goal. If the trait has only one implementation and no plausible substitution point, argue whether an inherent API would be better.

### Interleaved reasoning pass

1. For **Define a trait whose methods express a coherent behavioral contract**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the trait-law table.
2. For **Distinguish inherent behavior, free functions, and trait behavior**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the trait-law table.
3. For **Apply bounds, `where` clauses, default methods, supertraits, and UFCS correctly**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the trait-law table.
4. For **Detect traits that merely rename data access or create false substitutability**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the trait-law table.

5. Identify one guarantee from an earlier course that a careless implementation of **Traits as Behavioral Contracts** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build a small pricing library for `Book`, `CourseLicense`, and `SupportPlan`.

The starter intentionally duplicates concrete pricing calls. Your task is not “add a trait.” First identify which operations are genuinely substitutable.

### Product requirements

- each product can produce a nonnegative base price in cents;
- promotional adjustment is a separate policy selected by the caller;
- invoice rendering must not become part of the pricing contract;
- a caller can price any product through one generic function;
- shared law tests verify that price values never exceed a declared domain limit;
- invalid discount percentages are rejected at construction.

### Required design record
- one narrow behavioral trait;
- one operation left as an inherent method or free function, with justification;
- a `where` clause containing only body-required bounds;
- one default method derived from a required primitive;
- one shared law test across all product implementations;
- a memo explaining why a trait object is unnecessary in this laboratory.

See `labs/module-01-contract-boundaries/README.md` for the executable contract.

The executable starter and reference implementation are in [module-01-contract-boundaries](../../labs/module-01-contract-boundaries/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

### Laboratory acceptance trace

Before opening the reference implementation for **Contract Boundaries**, record:

- the public behavior that demonstrates **Define a trait whose methods express a coherent behavioral contract**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Create the first concrete rules without trait objects:

- minimum score;
- required tag;
- title length.

Write each as a concrete type with an `evaluate` method. Then identify the shared contract and extract `Rule` only after the caller needs uniform evaluation.

The initial contract must define:

- stable rule identity;
- deterministic finding order for one rule;
- whether evaluation mutates the rule;
- how findings are emitted;
- whether evaluation can fail;
- which methods must remain dyn-compatible for Module 25.

Do not build the registry yet. The Day 1 evidence is the contract and its laws.

### Capstone invariant trace

For the Module 21 Review Engine increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

You pass Module 21 only if you can:

- explain why the laboratory trait represents one coherent contract;
- remove one proposed trait and improve the design;
- predict all eight compiler specimens with at least 85% causal accuracy;
- write a reusable semantic-law test;
- resolve method ambiguity with fully qualified syntax;
- explain the future compatibility cost of an open public trait.

The oral prompt is: **“Show one place where adding a trait made the program worse, and defend the concrete replacement.”**
### Closed-book reconstruction

1. What behavioral promise is not expressible in a trait signature alone?
2. How does receiver choice change the authority granted to an implementation?
3. When does a supertrait express a real prerequisite rather than hierarchy theater?
4. How do you distinguish method-resolution ambiguity from a missing implementation?
5. Which law test must every formatter implementation satisfy?

### Independent transfer

Design a contract for a storage-independent audit sink in a different domain. First write the concrete two-implementation version. Introduce a trait only if the implementations share one coherent law. Submit the receiver choice, required core, derived defaults, law tests, and one reason an enum or ordinary function might still be better.

### Closed-book defense

In five minutes, answer “What behavior truly belongs in a shared contract, and which laws must every implementation preserve?” using the **trait-law table**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside Review Engine. A list of APIs without the deciding relationship is incomplete.
