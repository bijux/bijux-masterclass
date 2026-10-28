# Final review — Course 3: Traits, Generics, and Architectural Design

## Part A — mechanism selection

For each requirement, choose an enum, generic, trait object, closure, free function, newtype, adapter, or typestate and defend the rejected alternatives:

1. a fixed set of export formats with variant-specific configuration;
2. a caller-selected compression algorithm used throughout one generic pipeline;
3. runtime-loaded validation rules in one ordered collection;
4. a one-operation clock boundary for deterministic tests;
5. adaptation of a foreign identifier type to a local display contract;
6. a builder that must receive credentials and endpoint before `connect` exists;
7. a public extension API whose downstream implementations must survive minor releases.

## Part B — contract reasoning

1. Write laws for a `Normalize` trait.
2. Separate primitive and derived methods.
3. Choose receivers for inspect, mutate, and consume operations.
4. Decide whether `Item` should be associated or generic.
5. Explain an orphan-rule failure and a newtype repair.
6. Show a blanket implementation that is too broad and narrow it.
7. Derive the minimum bounds for a generic function body.
8. Explain what return-position `impl Trait` hides and preserves.
9. Test a trait for dyn compatibility.
10. Choose the ownership container and object lifetime for a registry.
11. Explain why downcasting may reveal a missing contract.
12. Draw a typestate graph and identify where runtime data still belongs.
13. Analyze a public-trait change from caller and implementor perspectives.

## Part C — architecture repair

Given an engine with one giant `Engine` trait, boxed source/reporter/rules, public mutable fields, and a typestate parameter for every option, redesign it from a variation map. Preserve only boundaries with real substitution pressure. Add law tests and a compatibility note.

## Part D — independent construction

Build an inspection platform with a generic input source, associated error family, ordered dynamic inspectors, a closure adapter, typestate configuration, deterministic findings, and a stable public extension boundary. Add one new inspector after freezing the API and record which files and contracts change.

## Completion

Course 3 is complete when the architecture can be explained as a small set of owned responsibilities and variation mechanisms—not as “traits everywhere.”
