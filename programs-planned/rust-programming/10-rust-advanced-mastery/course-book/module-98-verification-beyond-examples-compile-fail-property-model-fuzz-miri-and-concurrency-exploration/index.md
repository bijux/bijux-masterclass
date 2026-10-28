# Module 98 — Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration

**98/100** · Course 10 · Module 98 of 100

[Course 10 overview](../index.md) · [Workbook](workbook.md) · [Solutions](solutions.md) · [AxiomStore guide](../capstone.md)

## The question

> Which verification technique can falsify which kind of Rust claim, and how do you combine them without pretending that test volume equals proof?

## Why this comes now

The first nine courses used unit, integration, compile-fail, deterministic schedule, and adversarial tests. Advanced mastery requires matching each claim to a verification instrument. Type-level misuse needs negative compilation evidence. Algebraic behavior needs property tests. Finite protocols can be explored as state machines. Parsers need malformed corpora and fuzzing. Unsafe code benefits from Miri on executed paths. Concurrency protocols need systematic schedule exploration where possible. None of these methods proves everything; together they create a layered argument whose gaps are visible.

Every earlier course used tests, but different claims need different falsification methods. This module organizes compile-time, runtime, state, unsafe, concurrency, compatibility, and performance evidence into one matrix.

A large test suite can still leave the most important property unexamined. Module 98 starts from claims, not tools. It assigns each claim to evidence with an appropriate failure model: the compiler for rejected API space, properties for broad input relations, models for transitions, fuzzing for hostile syntax, Miri for executed unsafe behavior, and concurrency exploration for schedules.

## What you will be able to do

After completing this module, you will be able to:

- classify claims as type-level, functional, algebraic, state-machine, memory-safety, concurrency, compatibility, or performance claims
- select compile-fail tests, examples, properties, model exploration, fuzzing, Miri, schedule exploration, or benchmarks according to the claim
- write generators and shrinkable models that preserve domain validity while reaching boundary and failure states
- construct a small reference model and compare implementation traces after every operation rather than only final output
- interpret a clean tool run as evidence for executed cases rather than universal proof
- build a verification matrix that names uncovered claims and the reason they remain manual review obligations

## Core model

### The governing model

The governing artifact is a **claim-to-evidence matrix**. Rows are product claims. Columns record failure mode, oracle, tool, generated state/input space, resource bound, artifact identity, and residual risk. Empty cells are visible uncertainty rather than hidden confidence.

### 1. Verification begins with claim classification

“This method is unavailable before commit” is a type-surface claim suited to compile-fail evidence. “Encode then decode preserves a record” is an algebraic property. “Every initialized slot is dropped exactly once after any operation sequence” is a state and memory claim. “No legal thread schedule loses an outcome” is a concurrency protocol claim. Tools become useful only after the claim is stated precisely.

**Classify the claim.** Is “a borrowed view cannot outlive its snapshot” best tested by examples, compile-fail evidence, or runtime assertions? Why?

### 2. Compile-fail tests protect negative API space

Documentation tests or dedicated fixtures can prove that selected misuse is rejected: views cannot outlive snapshots, a builder cannot commit twice, or incompatible const dimensions cannot compose. Match the intended diagnostic cause so an unrelated syntax error does not create false confidence. Negative tests are especially valuable for typestate, lifetimes, auto traits, and visibility boundaries.

**Design the generator.** For canonical archive round trips, which valid and invalid records must the property generator include?

### 3. Properties generalize examples but depend on generators

A round-trip property is only as strong as the generated records and the equality relation. Include empty, maximum, Unicode, malformed, duplicate, and near-overflow cases according to the contract. Generators should create both valid values and structured invalid bytes. Shrinking must preserve the relevant precondition; otherwise the minimal counterexample may leave the domain being tested.

**Keep the model independent.** If the implementation stores a sorted vector, use a `BTreeMap` model rather than copying the same algorithm.

### 4. Model-based testing compares transitions

Build a simple obviously correct model using safe owned collections. Generate operation sequences, apply each operation to the model and implementation, and compare observations after every step. Intermediate comparison localizes the first divergence and catches defects hidden by a later compensating operation. Keep the model semantically independent; copying the same algorithm into two types only duplicates the bug.

**Bound hostile exploration.** Set byte, depth, operation-count, and time limits before fuzzing a parser or transaction sequence.

### 5. Fuzzing explores parser and state boundaries

Coverage-guided fuzzing is effective for byte parsers, protocol machines, and migration readers because it mutates inputs toward new branches. Seed it with known valid and hostile corpora. Define crash, panic, excessive allocation, timeout, and semantic mismatch as failures according to the harness. Preserve minimized regressions as ordinary tests so future verification does not depend on rediscovery.

**Scope Miri evidence.** Name the unsafe paths executed by one Miri test and the paths that remain unvisited.

### 6. Miri checks executed unsafe behavior under an interpreter

Miri can detect many categories of undefined behavior in paths it executes, including some aliasing and uninitialized-memory mistakes. It is slower and does not model every platform behavior or prove unexecuted states. Use small exhaustive operation sequences, drop-counting values, and panic injection to increase state coverage. A clean Miri run complements the written safety dossier; it does not replace it.

**Explore schedules deliberately.** Identify shared-state transitions and synchronization points before choosing a concurrency exploration tool.

### 7. Concurrency exploration needs a schedule model

Stress loops under the operating-system scheduler are weak evidence. For small synchronization abstractions, use a tool or model that controls interleavings and records happens-before choices. For larger async services, inject deterministic task, time, and I/O boundaries. State which schedules and capacities were explored. Liveness beyond the finite model remains a review obligation.

**Record a gap.** Choose one compatibility or operational claim that remains manual review and state why automation is incomplete.

### 8. The verification matrix preserves uncertainty

Create rows for public invariants and columns for techniques. Record strong, partial, not applicable, or missing evidence. A safety invariant may have a proof note, model sequences, drop tests, and Miri evidence while still requiring manual review of auto traits. This matrix prevents a large green test count from concealing one untested migration or unsafe path.

**Reader check.** Explain this idea using the concrete boundary in Model-Checked Log and name one fact that remains outside the mechanism. Then change one assumption and predict whether the result becomes a type error, a runtime rejection, a compatibility problem, or only a measured implementation observation.

### Worked verification matrix: one transaction claim

Take the claim: “committing a transaction yields the same logical map as applying its operations in source order to the previous map, while every failure before replacement leaves the previous archive readable and post-install durability uncertainty is reported separately.” That sentence contains several properties and therefore several evidence forms.

A model-based test can represent the logical map with `BTreeMap`, generate short sequences of `Put`, `Remove`, and `Clear`, and compare AxiomStore after every committed sequence. It should include duplicate puts, removal of absent keys, clear followed by put, and capacity rejection. The model must not reuse AxiomStore’s internal candidate-building code, or both may share the same defect.

Failure-state evidence needs fault boundaries. Validation and capacity failures can be produced deterministically. I/O failures may require an injectable writer or platform-specific fixture; if the reference capstone does not model every write failure, record that gap rather than simulating success. Persistent-format compatibility requires golden AXIOM01 bytes, not only round trips generated by the current encoder.

The unsafe inline batch has a different claim: every initialized `T` is moved or dropped at most once, and no uninitialized slot is read. Destructor counters exercise several transitions; Miri can inspect executed pointer operations; a state model can enumerate push/pop/clear sequences. None alone proves every possible `T` behavior. Panic-capable tests and review of mutation order cover additional paths.

Finally, negative API space belongs to compile-fail evidence. A `RecordView` escaping its `Snapshot` should not be transformed into a runtime test because a valid executable cannot contain the rejected relationship. Matching evidence to claim is the skill; tool count is not.

### A decision table

| Design question | Principled evidence or mechanism | Weak substitute to reject |
|---|---|---|
| Is misuse supposed to be unrepresentable? | compile-fail evidence and visibility review | runtime test that never compiles the misuse |
| Is behavior algebraic over many values? | property or differential tests | a handful of happy examples |
| Is the component a finite transition system? | model exploration after every step | only checking the final state |
| Does the claim concern unsafe execution? | written proof plus adversarial tests and Miri where available | clean ordinary unit tests as a soundness proof |

### A rigorous working procedure

1. Write the claim in falsifiable form and classify it as type, transition, parser, unsafe, concurrency, compatibility, or artifact behavior.
2. Define an oracle independent of the implementation where possible.
3. Select the smallest tool whose model can expose the named failure.
4. Bound generated inputs, state depth, schedules, memory, and time.
5. Preserve failing seeds, minimized cases, and exact toolchain/configuration identity.
6. Record residual risk and the event that requires rerunning or redesigning the evidence.

### Failure patterns and principled repairs

Verification fails when one tool is asked to prove a property outside its model. Repair the evidence plan by naming the claim first, then assigning compile-fail checks, executable properties, state models, fuzzing, Miri, concurrency exploration, or review only to the failures each can actually expose.

### Counting tests instead of mapping claims

Create matrix rows from invariants and mark which evidence can falsify each one.

### Copying implementation logic into the model

Use a simpler representation and independent transition algorithm.

### Fuzzing without resource limits

Treat excessive allocation, unbounded time, and output growth as harness failures.

### Calling a clean Miri run a proof

Record executed state space and retain manual obligations for unvisited paths and platform contracts.

### What the compiler cannot decide for you

No single tool proves the whole system. Compile-fail tests establish rejection of listed misuses, not soundness of every implementation. Properties are only as strong as generators and oracles. Fuzzing demonstrates explored executions, Miri interprets executed unsafe paths under its model, and model checking explores the modeled state space.

A verification portfolio is strong because its limitations overlap less, not because its test count is high. Honest blank cells in the matrix are better than a universal “verified” label.

## Use the idea in a complete program

Treat the log engine and the `BTreeMap` model as two independent transition systems. Enumerate short operation sequences, compare after every prefix, and make a mismatch report include the minimal sequence that produced it.

```rust
#[derive(Clone, Debug, PartialEq, Eq)]
enum Op {
    Put(String, String),
    Remove(String),
    Clear,
}

fn apply_model(model: &mut std::collections::BTreeMap<String, String>, op: &Op) {
    match op {
        Op::Put(key, value) => { model.insert(key.clone(), value.clone()); }
        Op::Remove(key) => { model.remove(key); }
        Op::Clear => model.clear(),
    }
}

fn explore(ops: &[Op]) {
    let mut model = std::collections::BTreeMap::new();
    let mut implementation = Store::new();
    for op in ops {
        apply_model(&mut model, op);
        implementation.apply(op.clone()).unwrap();
        assert_eq!(implementation.snapshot(), model);
    }
}
```

### Trace the example

Define the operation alphabet, initial state, transition function, and observable snapshot. Explore sequences up to a fixed depth and compare after each operation, not only at the end. Add one implementation bug—such as failing to replace an existing key—and verify the explorer produces a short counterexample.

Then map other claims to different evidence: a compile-fail view escape, malformed-format fuzz targets, exact-drop tests under Miri, and golden migration fixtures. Explain why none of those substitutes for the model-based transition oracle.

### Use it in AxiomStore

AxiomStore’s verification matrix combines known binary vectors, encode/decode properties, malformed corpora, model-generated transaction sequences, compile-fail lifetime and capacity examples, drop-counting tests for `InlineBatch`, Miri-oriented unsafe tests, migration fixtures, public API tests, and CLI process tests. Each mechanism has an explicit evidence boundary; no single green command is presented as complete proof.

AxiomStore’s verification matrix contains at least these rows:

```text
borrowed view cannot escape
codec round trip is canonical
malformed bytes never panic or allocate beyond limits
transaction result matches BTreeMap model
InlineBatch drops exactly initialized values
AXIOM01 fixtures remain readable
migration preserves source on failure
CLI exit behavior remains stable
```

For every row, name evidence, input/state scope, failure artifact, and residual risk. Do not merge all rows into `cargo test`.

## Practice sequence

1. **Negative API space.** Write compile-fail examples for view escape, retained lending item, and forged witness construction.
2. **Round-trip properties.** Generate bounded records, encode/decode them, and verify canonical bytes after the second encoding.
3. **Independent state model.** Explore transaction operation sequences against a `BTreeMap` oracle and minimize failures.
4. **Parser fuzz design.** Define corpus seeds and resource limits before writing a fuzz target.
5. **Unsafe-tool map.** List which `InlineBatch` transitions Miri tests execute and add a missing path.

Complete the [workbook](workbook.md) and [Model-Checked Log](../../labs/module-08-model-checked-log/README.md). A successful submission includes one deliberately unsupported claim in the matrix rather than pretending full coverage.

## Ready to continue

Continue when you can map a claim to a tool by failure model, design an oracle that is not a copy of the implementation, bound exploration, and state precisely what a passing run leaves unknown. You should be able to turn one discovered bug into a permanent minimal regression artifact.

## Primary Rust references

- The Rust testing documentation and rustdoc compile-fail examples
- The Miri project documentation
- Rust fuzzing and model-checking tool documentation as optional verification instruments

Verification tools change quickly. Record exact versions, flags, targets, seeds, and model bounds. Use tool documentation for capabilities, but preserve the claim/evidence matrix as the stable engineering record.

## Continue

1. Complete the [workbook](workbook.md) without consulting answers.
2. Build [Model-Checked Log](../../labs/module-08-model-checked-log/README.md).
3. Apply Module 98 in the [AxiomStore engineering guide](../capstone.md).
4. Review the [solutions](solutions.md) only after preserving your own predictions and design record.
