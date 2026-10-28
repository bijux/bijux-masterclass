# How to study the sixty-module program

## What counts as completing a module

A module is complete when you can:

1. state the mechanism and its boundary in plain language;
2. predict the decisive compiler, runtime, build, or platform consequence;
3. repair a broken design without deleting the difficult requirement;
4. build the independent laboratory from its contract;
5. integrate the matching capstone increment;
6. transfer the idea to a different product and defend the trade-off.

Reading is necessary but not sufficient. Passing tests is necessary but not sufficient. The finish line is working code plus a causal explanation.

## The daily sequence

### Morning — construct the model

Read the chapter in order and type the central examples. After each example, change one assumption: ownership, lifetime, input shape, receiver, bound, adapter order, generated syntax, byte length, error path, or target contract. Predict the result before compiling.

### Midday — predict and repair

Complete the workbook’s prediction table before running the specimen. For a repair task, preserve the original product contract. A clone, box, trait object, `RefCell`, macro, unsafe block, or lossy conversion is not automatically wrong; it is wrong when it hides an unexamined requirement.

### Afternoon — isolate the mechanism

Work from a copy of the lab starter. Write the smallest test that exposes the first broken assumption. The lab is intentionally smaller than the capstone so the mechanism remains visible.

### Evening — integrate and explain

Apply the capstone increment. Compare with the reasoned solution only after a serious attempt. End with a short reconstruction from memory: the invariant, decisive rule, one rejected shortcut, and one transfer case.

## Laboratory method

A laboratory is an independent product, not a fill-in-the-blank copy of the capstone. Work in a copy of `starter/`, run the baseline tests, and write the public contract and first adversarial case before opening `solution/`. Add one regression test before each design-changing repair. Compare with the reference only after your implementation works or you can state a precise blocker.

The reference is one defended implementation, not the grading key. Compare accepted inputs, rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and cost claims before comparing syntax.

## The course-book hierarchy

Within each course, use this order:

```text
course overview
    → ten-day plan
        → module chapter
            → workbook
                → lab
                    → capstone increment
                        → reasoned solutions
                            → reference and final review
```

The module chapter is authoritative. Reference pages compress material for later recall; they do not replace the derivation.

## Prediction records

For every compiler or boundary case, record:

- expected outcome;
- decisive line, token, state, or external action;
- governing contract;
- earliest phase that can know the result;
- smallest repair that preserves the requirement;
- tempting repair that weakens the product.

## When to stop and repair

Do not advance when:

- you make edits you cannot explain;
- three predictions fail for unrelated reasons;
- your design depends on a later-course mechanism to avoid understanding the current one;
- the success path works but failure leaves an unspecified state;
- a claim is stronger than the test, type, platform, or safety evidence behind it.

Reduce the problem to the smallest counterexample, rebuild the model, and return to the lab only when the cause is clear.

## Time and pacing

One course is ten focused days, normally five days per week for two weeks. A dense day is eight to ten focused hours including breaks. The weekend between weeks is for repair, closed-book reconstruction, and rest—not new material.

## Course-specific records

| Course | Keep this record beside your code |
|---:|---|
| 1 | type/state trace and ownership ledger |
| 2 | place/loan/lifetime graph and cleanup or liveness state machine |
| 3 | contract law table and variation/dispatch map |
| 4 | capture ledger, iterator stage map, failure policy, and cost ledger |
| 5 | source-of-truth, grammar, expansion, and phase ledger |
| 6 | representation, resource-state, boundary, safety, and ABI ledger |
