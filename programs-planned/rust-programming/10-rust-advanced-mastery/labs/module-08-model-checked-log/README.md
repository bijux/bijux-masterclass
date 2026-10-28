# Laboratory 98 — Model-Checked Log

**Course 10 · Module 98: Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration**

[Chapter](../../course-book/module-98-verification-beyond-examples-compile-fail-property-model-fuzz-miri-and-concurrency-exploration/index.md) · [Workbook](../../course-book/module-98-verification-beyond-examples-compile-fail-property-model-fuzz-miri-and-concurrency-exploration/workbook.md) · [AxiomStore guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration**: Which verification technique can falsify which kind of Rust claim, and how do you combine them without pretending that test volume equals proof? The product must make **Classify claims as type-level, functional, algebraic, state-machine, memory-safety, concurrency, compatibility, or performance claims** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **verification claim matrix** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Product

Build a compact mutation engine and an independent model, then exhaustively compare them across every operation sequence within a bounded state space. The engine should use a representation different from the model so the test does not reproduce the same defect twice.

The starter supplies a `BTreeMap` model for `Put`, `Remove`, and `Clear`. Implement the system under test with a sorted vector or another deliberately different representation. Compare state after every operation prefix, not only after the complete sequence.

### State space

Choose and document finite bounds for:

- keys;
- values;
- operation alphabet;
- maximum sequence length;
- optional capacity or transaction size;
- failure injection points.

The explorer must produce the shortest divergent prefix and show both states. A raw assertion after millions of cases is not a useful diagnostic.

### Engine invariants

For a sorted-vector implementation:

- keys are unique;
- items remain in key order;
- replacing a key does not create a duplicate;
- removing an absent key is a documented no-op or typed error;
- clear leaves the canonical empty state;
- failure does not partially reorder or mutate unrelated entries.

Add direct unit tests for representation invariants as well as model comparison.

### Independence review

List every helper shared by the model and engine. Shared domain operation types are acceptable; shared mutation algorithms are not. If both sides call one `apply` function, the comparison proves only that a function equals itself.

### Transfer

Add a bounded all-or-nothing transaction operation. The model may clone its small map; the engine should use a candidate representation or rollback strategy appropriate to its design. Enumerate transactions containing success, duplicate keys, removal, and capacity failure. Compare both the result and the post-failure state after every prefix.

### Using the reference

Complete the explorer from `starter/` before inspecting `solution/`. The reference demonstrates recursive enumeration but is intentionally compact. Improve its failure report and state-space accounting rather than copying its formatting.

### Mechanism-specific completion standard

You can explain why the model is simpler and independent, why the state space is finite, and why prefix comparison localizes the first divergence. If the explorer can consume unbounded memory or time from an input value, its verification claim is incomplete.

## Design record

Before implementation, complete this record for **Model-Checked Log**:

| Question | Required answer |
|---|---|
| Module decision | How does **Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration** answer its governing question in this product? |
| Authority | Which type or component decides the main rule? |
| Valid states | Which states may be observed through the public API? |
| Rejection | What exact input or transition is refused, and what remains unchanged? |
| Ownership | Who owns every resource before, during, and after the decisive operation? |
| Order and bounds | Which sequence, capacity, lifetime, or compatibility limit is promised? |
| Evidence | Which test, compiler case, model, trace, or review could falsify the claim? |

Use the **verification claim matrix** to answer the table. Then add at least three adversarial cases: one at the smallest boundary, one at the largest accepted or rejected boundary, and one that leaves partial work before failure. For each, state the final observable state before running the test.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Model-Checked Log**.
2. Draw the smallest **verification claim matrix** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to AxiomStore so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Whole-laboratory completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Classify claims as type-level, functional, algebraic, state-machine, memory-safety, concurrency, compatibility, or performance claims.
- Select compile-fail tests, examples, properties, model exploration, fuzzing, Miri, schedule exploration, or benchmarks according to the claim.
- Write generators and shrinkable models that preserve domain validity while reaching boundary and failure states.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 98 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **verification claim matrix**. Defend why your design is simpler than one plausible alternative under the new requirements.
