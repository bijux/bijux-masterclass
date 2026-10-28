# Compiler and boundary investigations

These eighty cases train causal prediction before you rely on a compiler message or observed schedule. They are not a substitute for the module workbooks. Use the workbook first, record your prediction, then run the isolated case.

## Outcome categories

```text
compile-pass  the source should type-check successfully
compile-fail  the source should be rejected for the recorded cause
run-pass      compilation and execution should both satisfy the contract
run-fail      compilation succeeds and execution demonstrates a recorded failure
manual-review compilation is not the decisive proof; inspect the design contract
```

Course 7 currently contains forty `compile-pass` and forty `compile-fail` cases. Modules 61–68 and 70 use direct `rustc` cases. Module 69 uses Cargo fixtures because Rayon is an external crate and the dependency boundary is part of the exercise.

## Method

For each case, write down:

1. whether it should compile;
2. the first line whose type or lifetime contract decides the result;
3. whether the issue concerns ownership transfer, shared-reference capability, guard lifetime, endpoint ownership, atomic type use, unsafe auto-trait claims, or parallel trait bounds;
4. the smallest repair that preserves the product requirement;
5. one repair that may compile but weakens lifecycle, determinism, capacity, or safety.

Then run:

```bash
make compiler-labs
```

The runner reads `manifest.json`, checks each declared outcome, and isolates Cargo fixtures from one another. A negative case passes only when compilation fails. During review, compare the actual diagnostic with `intended_cause`; an unrelated syntax or import error does not prove the target rule.

## What these cases do not prove

Successful compilation does not prove freedom from deadlock, starvation, schedule-dependent output, incomplete shutdown, weak cancellation, or incorrect atomic ordering. Several modules therefore pair compiler cases with runtime protocols in their workbooks and laboratories. The case metadata records the boundary honestly instead of calling every concurrency defect a compiler failure.
