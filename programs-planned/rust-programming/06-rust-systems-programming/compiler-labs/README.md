# Compiler investigations — Rust Systems Programming

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

- [Module 51: Binary Data Contracts](module-01/README.md)
- [Module 52: Files, Durability, and Transactional Replacement](module-02/README.md)
- [Module 53: Paths, Names, and Platform Boundaries](module-03/README.md)
- [Module 54: Processes, Environments, and Standard Streams](module-04/README.md)
- [Module 55: Unsafe Rust as a Proof Boundary](module-05/README.md)
- [Module 56: Raw Pointers, Provenance, and Uninitialized Memory](module-06/README.md)
- [Module 57: Manual Allocation and Owning Unsafe Abstractions](module-07/README.md)
- [Module 58: C FFI: ABI, Strings, Pointers, and Errors](module-08/README.md)
- [Module 59: Foreign Resources, Callbacks, and Wrapper Architecture](module-09/README.md)
- [Module 60: Integrated Systems Design, Testing, and Audit](module-10/README.md)
