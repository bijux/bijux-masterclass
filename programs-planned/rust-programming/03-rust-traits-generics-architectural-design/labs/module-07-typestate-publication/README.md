# Laboratory 27 — Typestate Publication

**Course 3 · Module 27: Typestate and Capability-Oriented APIs**

[Chapter](../../course-book/module-27-typestate-and-capability-oriented-apis/index.md) · [Workbook](../../course-book/module-27-typestate-and-capability-oriented-apis/workbook.md) · [Review Engine guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Typestate and Capability-Oriented APIs**: Which illegal operations can be removed from the API by representing protocol state and authority in types? The product must make **Encode a finite protocol with marker states and consuming transitions** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **typestate transition graph** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> Which illegal operations can be removed from the API by representing protocol state and authority in types?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Implement `Draft -> Reviewed -> Published` with state-specific evidence.

Requirements:

- only drafts can be edited;
- review consumes a draft and can return it on failure;
- publication requires a single-use permit;
- marker states cannot be forged downstream;
- a runtime enum stores draft and reviewed values for persistence preparation;
- tests and compile-fail examples prove unavailable operations;
- a memo compares typestate with one runtime enum design.

## Design focus

Model a short publication protocol with consuming transitions such as draft, validated, and published. Methods that are illegal in a state must be absent from that state’s method set; they must not merely return a late Boolean error. Keep marker types and fields private enough that callers cannot forge readiness. Preserve useful data when a transition fails by returning an error that carries the surviving state where appropriate.

Do not encode external uncertainty in typestate. File availability, network response, and user-provided content remain runtime concerns. Tests should cover the valid transition path, validation failure, compile-fail attempts to publish too early, and the inability to reuse a consumed state. Explain why an enum state machine would be preferable if states must be stored heterogeneously or selected entirely at run time.

## Design record

Before implementation, complete this record for **Typestate Publication**:

| Question | Required answer |
|---|---|
| Module decision | How does **Typestate and Capability-Oriented APIs** answer its governing question in this product? |
| Authority | Which type or component decides the main rule? |
| Valid states | Which states may be observed through the public API? |
| Rejection | What exact input or transition is refused, and what remains unchanged? |
| Ownership | Who owns every resource before, during, and after the decisive operation? |
| Order and bounds | Which sequence, capacity, lifetime, or compatibility limit is promised? |
| Evidence | Which test, compiler case, model, trace, or review could falsify the claim? |

Use the **typestate transition graph** to answer the table. Then add at least three adversarial cases: one at the smallest boundary, one at the largest accepted or rejected boundary, and one that leaves partial work before failure. For each, state the final observable state before running the test.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Typestate Publication**.
2. Draw the smallest **typestate transition graph** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Review Engine so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 27 — Typestate Publication**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Typestate Publication**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Encode a finite protocol with marker states and consuming transitions.
- Decide which invalid operations deserve compile-time prevention.
- Prevent construction of forbidden states through visibility and sealed state markers.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 27 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **typestate transition graph**. Defend why your design is simpler than one plausible alternative under the new requirements.
