# Module 10 Workbook

## A. Evidence selection

Choose the smallest useful boundary for each claim:

- a transition rejects completion from planned state;
- importing the library does not read a file;
- corrupted JSON reports the record path;
- `study-ledger help` exits zero and writes only stdout;
- a new command union member is handled everywhere;
- saved sessions appear in ID order;
- a failed save prevents success output.

## B. Architecture fault injection

For each defect, identify which test should catch it:

1. the domain reads `new Date()`;
2. `sort` mutates retained sessions;
3. storage catches all errors and returns empty state;
4. `main` prints success before awaiting save;
5. an internal module becomes a public export;
6. the CLI writes validation errors to stdout.

## C. Independent change plan

Write the authority and invariant impact map for one StudyLedger feature before editing code. Include storage compatibility and failure behavior.

## D. Process harness

Build a helper that spawns the compiled CLI with a temporary data path, captures stdout/stderr, and returns exit code. Ensure child process errors and nonzero exit are distinguishable.

## E. Independent laboratory

Complete [Reading Ledger](../../labs/module-10-reading-ledger/README.md). Its domain and commands differ from StudyLedger; derive rather than copy the architecture.

## F. Final StudyLedger transfer

Implement the selected unseen feature. Run all tests from a clean build. Review the emitted ESM graph and package contents.

## G. Oral defense

Answer the questions in [Final Review](../final-review.md) without source access. Then identify one claim your current evidence does not establish and design the next experiment or test.

## H. Evidence selection

For each claim below, choose the nearest evidence and explain why a more distant test alone is insufficient:

- search is case-insensitive;
- V1 rejects duplicate IDs;
- help writes to stdout;
- a domain transition does not mutate its input;
- the package has no accidental default export;
- a mutating command does not report success after save rejection.

## I. Independent change plan

Design `reopen <id>` or `rename <id> --topic <text>`. Produce an impact map across command grammar, domain types, validation, encoding compatibility, rendering, application orchestration, help, and tests. State which files do **not** need modification and why.

## J. Final reconstruction

From an empty directory, write the package metadata, strict configuration, domain model, parser, storage boundary, application function, binary, and tests in dependency order. You may consult official API signatures but not the course implementation. Finish by recording three non-contracts that remain for later courses.
