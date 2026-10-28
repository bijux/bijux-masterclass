# Final review — Course 1: Rust Foundations

Complete this review without the reference page. Use a fresh directory for the construction task.

## Part A — explain from memory

1. Distinguish package, crate, target, and module.
2. Explain how a semicolon changes the type of a block.
3. Choose an integer type and overflow policy for a bounded counter.
4. Trace ownership through assignment, function call, and return.
5. Explain `Copy` versus `Clone` without using “stack” as the definition.
6. Derive when a parameter should be `T`, `&T`, or `&mut T`.
7. Explain why `String` can be indexed by ranges only when UTF-8 boundaries are valid, not by arbitrary integer characters.
8. Replace contradictory status flags with a type model.
9. Distinguish `iter`, `iter_mut`, and `into_iter` by item and ownership.
10. Distinguish absence, recoverable failure, and invariant violation.
11. Explain what `?` does and does not do.
12. Explain why loading should complete validation before replacing live state.
13. Explain one justified generic function and one unjustified custom trait.
14. State what a basic lifetime annotation relates.
15. Distinguish unit, integration, CLI, and documentation tests.

## Part B — predict and repair

For each case, predict before compiling:

- a branch whose arms are `i32` and `()`;
- a moved `String` used after insertion into a vector;
- simultaneous iteration and mutation of a vector;
- a returned slice of a local `String`;
- a match missing one enum variant;
- collection into an ambiguous destination;
- `Option<&Task>` replaced by a sentinel identifier;
- a loader that maps every error to an empty board;
- a public struct whose fields bypass validation;
- a binary containing all domain logic while the library is empty.

Repair each while preserving the original requirement. Write why cloning, indexing, wildcard matching, `unwrap`, or making every field public would be a weak repair in the relevant case.

## Part C — independent construction

Build a persistent inventory CLI with commands to add, reserve, release, remove, list, and report stock. Requirements:

- typed identifiers and status;
- private fields and legal transitions;
- deterministic output;
- versioned text storage;
- malformed-line errors with line numbers;
- no mutation after a failed command;
- library/binary separation;
- unit, integration, and process-level tests.

Do not copy Taskboard types. The product vocabulary must drive the model.

## Part D — oral defense

Defend five signatures, three error variants, the state-transition representation, storage commit point, and public visibility. Course 1 is complete only when you can change one cross-layer requirement after the review without tutorial instructions.
