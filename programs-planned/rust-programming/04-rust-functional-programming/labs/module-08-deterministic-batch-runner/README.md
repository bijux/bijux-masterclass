# Laboratory 38 — Deterministic Batch Runner

**Course 4 · Module 38: Functional Core and Effect Isolation**

[Chapter](../../course-book/module-38-functional-core-and-effect-isolation/index.md) · [Workbook](../../course-book/module-38-functional-core-and-effect-isolation/workbook.md) · [LedgerFlow guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Functional Core and Effect Isolation**: Which decisions can remain pure, which effects must occur at the boundary, and what data should cross between them? The product must make **Separate deterministic domain decisions from filesystem, time, environment, and terminal effects** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **effect boundary map** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> Which decisions can remain pure, which effects must occur at the boundary, and what data should cross between them?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

The executable package is `labs/module-08-deterministic-batch-runner/README.md`. The laboratory separates decisions from effect execution and makes partial effects explicit.

### Boundary map

Classify each input or operation before writing code:

| Concern | Core input/value | Shell effect |
|---|---|---|
| current time | explicit `u64` | clock observation |
| generated ID | injected `FnMut` | external sequence/service |
| validation | deterministic decision | none |
| file write | `Action::Write` value | filesystem operation |
| notification | `Action::Notify` value | external delivery |
| dry run | rendering of actions | terminal write outside core |

The core may not read environment variables, call a clock, access files, or print.

### Planning contract

`plan` accepts inputs, an explicit `now`, and a stateful ID generator. Rejected records do not consume IDs. Accepted records produce both analysis data and ordered action values. Write a call-ledger test that places invalid and overdue records before a valid record and proves the first generated ID goes to the valid item.

The planner must remain deterministic for equal explicit inputs and equal generator output. This does not mean the injected generator is pure; it means its state is an explicit dependency at the boundary.

### Execution contract

`execute` processes action values in order through a fallible callback. On failure it reports the number of successfully completed actions and preserves the source error type. It does **not** claim rollback. Add tests for failure on the first action, a middle action, and success of all actions.

### Dry run

Render the plan without executing any callback. Use an execution-call counter to prove zero effects. The rendered order must match execution order. Match action variants explicitly; do not publish `Debug` output as a report contract, because a derived debugging representation is not a deliberately versioned user format.

### Replay questions

Document:

- whether repeating the same plan would repeat writes or notifications;
- which action types are idempotent under what external assumptions;
- how a production shell could record completion and resume;
- why a deterministic plan can still become stale before execution.

Do not solve these with hidden global state in the course lab.

### Rejected designs

- closure-valued actions that cannot be inspected;
- generating IDs before validation;
- swallowing the executor’s source error into `String`;
- describing a successful prefix as transactionality;
- reading `SystemTime::now()` inside `plan`;
- testing the core by capturing stdout.

Submit the boundary map, ID call ledger, effect-order tests, partial-failure report, dry-run proof, and replay note. Explain why `FnMut` is required for ID allocation, why action values are preferable to boxed one-shot callbacks here, and where operational I/O errors belong in a real CLI.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Deterministic Batch Runner**.
2. Draw the smallest **effect boundary map** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to LedgerFlow so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 38 — Deterministic Batch Runner**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Deterministic Batch Runner**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Separate deterministic domain decisions from filesystem, time, environment, and terminal effects.
- Inject small effect capabilities through parameters, closures, or narrow traits without building a framework.
- Represent intended effects as data when plan-then-execute improves safety or testability.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 38 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **effect boundary map**. Defend why your design is simpler than one plausible alternative under the new requirements.
