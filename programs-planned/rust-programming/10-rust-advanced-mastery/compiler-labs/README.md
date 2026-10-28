# Course 10 Compiler and Design Investigations

Course 10 contains eighty isolated cases, eight per module. Freeze the predicted outcome before running a case. For every case record the earliest decisive phase, the exact relationship that permits or rejects the program, the smallest requirement-preserving repair, and one tempting change that would weaken the product contract.

The outcome categories are `compile-pass`, `compile-fail`, and `manual-review`. A manual-review case compiles because the disputed claim concerns compatibility, release policy, artifact scope, or architecture rather than Rust legality. Compilation is therefore only the beginning of the answer.

Run the complete set from the course directory:

```bash
make compiler-labs
```

A negative case counts only when it fails for the intended cause. Missing imports, syntax errors, unrelated warnings, and stale APIs do not prove the target rule. Positive cases must exercise the relevant capability rather than compile because the operation is unused.
