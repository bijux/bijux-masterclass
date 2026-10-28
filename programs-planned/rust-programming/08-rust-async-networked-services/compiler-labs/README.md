# Course 8 Compiler and Contract Investigations

This directory contains eighty isolated cases. Forty are expected to compile and forty are expected to fail. Each case targets one type-system, lifetime, async-state, task-boundary, or protocol-interface rule used in the course.

Before running a case, record:

1. whether it should compile;
2. the decisive phase;
3. the exact rule;
4. the smallest principled repair;
5. one repair that may compile but weakens the product design.

Run all cases from the course root:

```bash
make compiler-labs
```

A failed program counts only when it fails for the causal reason named in `manifest.json`. An unrelated typo is not evidence of the intended rule.


## How to use the cases

Each module contains eight isolated programs. Four are expected to compile and four are expected to be rejected. Do not read `manifest.json` before making your prediction; it is machine-readable verification metadata, not the learning route. For every case, record the expected outcome, the exact rule, the earliest compiler phase that can reject it, and the smallest repair that preserves the product requirement.

A negative case is useful only when it fails for the intended cause. An unrelated syntax error, unused-item warning, missing import, or type mismatch does not prove the target async rule. The runner compiles direct cases with Rust 2024 Edition and warnings denied. After execution, compare the decisive diagnostic with the causal contract in the manifest. If they differ, repair the specimen rather than rationalizing the mismatch.

The cases deliberately remain standard-library-only. They test the language-level boundaries underneath runtimes: future output types, `Send`, `'static`, pinning, ownership across async blocks, exhaustive protocol states, body types, and retry callback capability. Tokio- and Hyper-specific behavior belongs in the executable labs, where runtime and transport observations can be tested as behavior rather than mistaken for compiler rules.
