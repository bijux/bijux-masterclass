# Compiler investigations — Rust Foundations

Compiler investigations train prediction before repair. They are not quizzes about memorizing diagnostic wording. Each specimen isolates one language rule, runtime failure, or design defect from the corresponding course chapter.

## Outcome vocabulary

- **compile-pass** — the program must type-check under the pinned toolchain;
- **compile-fail** — the compiler must reject it for the intended primary cause;
- **run-pass** — it must compile and terminate successfully;
- **run-fail** — it must compile and then terminate unsuccessfully on the demonstrated path;
- **manual-review** — it compiles, but the design or product contract is intentionally unacceptable.

Do not inspect `manifest.json`, module solutions, or a compiler diagnostic before recording a prediction. The manifest is machine-readable answer metadata used by the runner.

## Investigation record

For every specimen, write five short statements:

1. predicted outcome category;
2. decisive phase: parsing, expansion, name resolution, type checking, borrow checking, execution, or design review;
3. first causal rule, not the last cascade diagnostic;
4. smallest repair that preserves the intended product behavior;
5. a tempting repair that compiles but weakens ownership, type information, invariants, portability, or API clarity.

Run the complete course set from the course root:

```bash
make compiler-labs
```

For a direct Rust specimen, compile into a temporary directory rather than leaving binaries in the course tree. Cargo fixtures are checked with their own manifests. After observing the result, revise the causal explanation before reading the corresponding solution.

## Module sets

- [Module 1: Compilation, Expressions, and Types](module-01/README.md)
- [Module 2: Control Flow, Functions, and Invariants](module-02/README.md)
- [Module 3: Ownership, Moves, Copying, and Destruction](module-03/README.md)
- [Module 4: Borrowing, References, Slices, and Strings](module-04/README.md)
- [Module 5: Structs, Enums, Methods, and Pattern Matching](module-05/README.md)
- [Module 6: Collections, Iterators, and Closures](module-06/README.md)
- [Module 7: Errors, Parsing, Files, and Persistence](module-07/README.md)
- [Module 8: Generics, Traits, Conversions, and Lifetime Basics](module-08/README.md)
- [Module 9: Crates, Modules, Public APIs, Tests, and Documentation](module-09/README.md)
- [Module 10: Integration and Independent Change](module-10/README.md)
