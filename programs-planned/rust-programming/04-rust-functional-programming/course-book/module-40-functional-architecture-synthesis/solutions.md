# Reasoned Solutions — Module 40: Functional Architecture Synthesis

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-10-route-analysis-engine/README.md) · [LedgerFlow guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 40: Functional Architecture Synthesis**. Compare the reasoning against this question: *How do closure, iterator, error, reduction, structural-sharing, and effect decisions compose into a readable whole system?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `case-01.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** an integrated pipeline can retain typed failure and deterministic order.
- **Causal explanation:** The specimen compiles because an integrated pipeline can retain typed failure and deterministic order.
- **Principled repair:** keep stages named where contracts differ
- **Weak repair to reject:** compress every stage into one unreadable chain

### 2. `case-02.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** consuming source values makes later source use invalid.
- **Causal explanation:** The compiler rejects the specimen because consuming source values makes later source use invalid.
- **Principled repair:** borrow if source must remain available or stop using it
- **Weak repair to reject:** clone without a product need

### 3. `case-03.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** fallible traversal can remain one explicit stage.
- **Causal explanation:** The specimen compiles because fallible traversal can remain one explicit stage.
- **Principled repair:** name the policy and output shape
- **Weak repair to reject:** filter_map errors into disappearance

### 4. `case-04.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** return-position impl Iterator requires one concrete iterator type.
- **Causal explanation:** The compiler rejects the specimen because return-position impl Iterator requires one concrete iterator type.
- **Principled repair:** use an enum adapter, box deliberately, or branch inside a common pipeline
- **Weak repair to reject:** add arbitrary collection solely to force one type

### 5. `case-05.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** deliberate iterator erasure can unify runtime-selected sources.
- **Causal explanation:** The specimen compiles because deliberate iterator erasure can unify runtime-selected sources.
- **Principled repair:** record the allocation/dynamic-dispatch tradeoff
- **Weak repair to reject:** box all ordinary iterator returns

### 6. `case-06.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** recoverable row errors can accumulate while state continues.
- **Causal explanation:** The specimen compiles because recoverable row errors can accumulate while state continues.
- **Principled repair:** use a named accumulator when try_fold short-circuiting is wrong
- **Weak repair to reject:** encode diagnostics as magic values in accepted output

### 7. `case-07.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** a returned closure cannot borrow a local owner that is about to be dropped.
- **Causal explanation:** The compiler rejects the specimen because a returned closure cannot borrow a local owner that is about to be dropped.
- **Principled repair:** add move so the closure owns text
- **Weak repair to reject:** return a reference to the local instead

### 8. `case-08.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** a functional core can transform supplied text without performing I/O.
- **Causal explanation:** The specimen compiles because a functional core can transform supplied text without performing I/O.
- **Principled repair:** keep file reading and printing at the caller boundary
- **Weak repair to reject:** read files inside parse for convenience

## Exercise reasoning

### Exercise 1 — Build the transformation map

A strong answer separates shell acquisition from core text processing, preserves physical line identity before filtering, keeps parse outcomes explicit, reserves duplicate identities under a stated policy, reduces accepted events through owned candidate state, exposes borrowed lazy queries over stable state, materializes only for sorting or report ownership, and returns structured exit classification. Every stage names its failure/diagnostic channel and order guarantee. There is no universal single implementation; grading follows the completeness and consistency of the map.

### Exercise 2 — Review a stage contract

The name implies validation but not diagnostic loss. The item type cannot represent failure. The hidden stderr effect depends on consumption and violates deterministic core isolation. `filter_map` conflates malformed data with intended absence. Redesign as a row-inspection iterator yielding `RowOutcome`, or consume into `Inspection { accepted, diagnostics }` under an explicit accumulation policy. Rendering diagnostics belongs after structured analysis, and the function name should state whether it is fail-fast or accumulating.

### Exercise 3 — Implement an unseen feature method

Clarify whether rejected/invalid events count, whether the limit is per physical source order or accepted order, what diagnostic is emitted, whether later events are still parsed, and whether queries/report counts include ignored events. Update the transformation map and accumulator invariant. Add boundary, zero, exact-limit, over-limit, multi-account, invalid-before-limit, and duplicate cases. Then implement at the stage that owns accepted-event count, not as an output filter, because state reduction must not apply ignored events. Re-run determinism, audit, and old regression tests.

### Exercise 4 — Detect semantic drift

The new code stops at the first error, so later diagnostics and accepted rows disappear. Side-effect/call-count behavior also changes. Existing tests may contain only zero or one error. Add multiple-error input, valid rows after an error, warning-plus-error, and visitation-ledger tests. If fail-fast is intended, rename the stage and update product contract; otherwise restore explicit accumulation.

### Exercise 5 — Architecture rejection record

Boxing every iterator hides concrete types and may add allocation/dynamic dispatch without runtime heterogeneity. Collecting after each stage adds traversal/storage and obscures which materialization is algorithmically required. One large effect trait couples unrelated capabilities, creates broad fakes, and permits the core to perform effects anywhere. Each record should state the tempting benefit, violated requirement, concrete cost/complexity, and condition that would make reconsideration rational.

### Exercise 6 — Course handoff

Macros may reduce repetitive implementations, generate adapters, derive parsing/reporting boilerplate, or enforce declarative schemas. They must not erase understanding of closure capture, iterator laziness, failure topology, accumulator invariants, effect boundaries, or public semantics. Before macro construction, the expanded behavior should be implementable and testable by hand. Course 4 hands off stable patterns; Course 5 must not use code generation to conceal unresolved design.

## Reference implementation comparison

The complete laboratory implementation is in [`module-10-route-analysis-engine/solution`](../../labs/module-10-route-analysis-engine/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Functional Architecture Synthesis**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Produce a transformation map that identifies source, shape, ownership, failure, state, and effect boundaries.
- Integrate closures, iterators, folds, error traversal, custom protocols, and effect isolation coherently.
- Refactor between loops and combinators without changing observable behavior.
- Implement an unseen feature across parser, transformation core, reducer, report, CLI, and tests.
- Defend the architecture, its rejected alternatives, and its remaining limits under oral review.

A complete explanation of **Functional Architecture Synthesis** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.

## Deep reasoning and transfer

### Decisive model

> How do closure, iterator, error, reduction, structural-sharing, and effect decisions compose into a readable whole system?

Build a **whole-pipeline architecture map**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Produce a transformation map that identifies source, shape, ownership, failure, state, and effect boundaries.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Integrate closures, iterators, folds, error traversal, custom protocols, and effect isolation coherently.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Refactor between loops and combinators without changing observable behavior.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Implement an unseen feature across parser, transformation core, reducer, report, CLI, and tests.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Defend the architecture, its rejected alternatives, and its remaining limits under oral review.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Produce a transformation map that identifies source, shape, ownership, failure, state, and effect boundaries.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the whole-pipeline architecture map.

### Laboratory transfer review

For [Route Analysis Engine](../../labs/module-10-route-analysis-engine/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In LedgerFlow, Module 40 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Functional Architecture Synthesis**, which relationship decides this question: “How do closure, iterator, error, reduction, structural-sharing, and effect decisions compose into a readable whole system?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to LedgerFlow?
