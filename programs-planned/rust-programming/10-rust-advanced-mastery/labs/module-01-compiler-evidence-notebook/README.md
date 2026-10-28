# Laboratory 91 — Compiler Evidence Notebook

**Course 10 · Module 91: Reading Rust Through the Compiler: HIR, MIR, Borrow Checking, and Codegen**

[Chapter](../../course-book/module-91-reading-rust-through-the-compiler-hir-mir-borrow-checking-and-codegen/index.md) · [Workbook](../../course-book/module-91-reading-rust-through-the-compiler-hir-mir-borrow-checking-and-codegen/workbook.md) · [AxiomStore guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Reading Rust Through the Compiler: HIR, MIR, Borrow Checking, and Codegen**: When difficult Rust code surprises you, which compiler representation and which proof obligation actually decide the result? The product must make **Separate parsing, name resolution, type checking, trait solving, borrow checking, monomorphization, optimization, and linking as distinct explanatory phases** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **compiler-phase record** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Product

Build an executable evidence notebook that prevents four different kinds of statement from collapsing into one another: a Rust language rule, a rustc diagnostic, a runtime observation, and a code-generation observation. The starter already names a few compiler phases. Your task is to turn that vocabulary into a small but rigorous classification tool and to demonstrate it with ownership and destruction traces.

The product is not a compiler simulator. It is a disciplined record of **which representation can answer which question**. A borrow error may be decided during borrow checking; the choice of a better domain model is not. A destructor counter can show what one execution dropped; it cannot describe optimized instruction layout. A symbol table can reveal one artifact; it cannot redefine Rust semantics.

### Required behavior

Add the missing expansion, trait-solving, runtime, and code-generation categories. `classify` must return a structured record containing the claim, decisive phase, kind of evidence, justified conclusion, and a statement of what remains unknown. Include at least these cases:

- overlapping mutable borrows;
- an unsatisfied associated-type equality;
- observed drop order;
- symbol or section size in one release artifact;
- an unknown claim that requires further isolation.

Add a `DropProbe`-style experiment that proves exactly which owned values are destroyed after normal return, explicit `drop`, early return, and movement into an aggregate. Keep the output deterministic; do not print from `Drop` and then treat scheduling or buffered output as the proof.

### Investigation dossier

For every case, write a short dossier with:

1. the smallest source program that exposes the question;
2. the first phase capable of deciding it;
3. the evidence you would collect;
4. the conclusion the evidence supports;
5. one conclusion it does **not** support.

The decisive negative test is a deliberately misleading statement such as “MIR proves the API is semantically correct” or “the assembly shows Rust moves always copy bytes.” Your implementation must classify why the statement exceeds its evidence.

### Transfer

Add a closure-capture case and a partial-move case. The closure case must distinguish type checking from runtime invocation behavior. The partial-move case must distinguish source ownership rules from a later artifact observation. A successful transfer changes the claim and the decisive representation; merely adding two more strings to a match does not count.

### Using the reference

Work from `starter/` until your classification table and drop experiments pass. Then inspect `solution/`. Compare the **boundaries of each conclusion**, not enum names. Record one place where your notebook is stricter and one place where the reference communicates uncertainty more clearly.

### Mechanism-specific completion standard

Another reader should be able to take an unfamiliar compiler message, reduce it to a causal specimen, identify the earliest deciding phase, and state what must still be tested or measured elsewhere. If the notebook encourages claims stronger than the evidence, the laboratory is incomplete.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Compiler Evidence Notebook**.
2. Draw the smallest **compiler-phase record** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to AxiomStore so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Whole-laboratory completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Separate parsing, name resolution, type checking, trait solving, borrow checking, monomorphization, optimization, and linking as distinct explanatory phases.
- Translate source constructs into a control-flow and place-oriented model suitable for borrow, move, and drop reasoning.
- Identify when an observation is a language guarantee, a compiler implementation detail, or generated machine-code evidence.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 91 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **compiler-phase record**. Defend why your design is simpler than one plausible alternative under the new requirements.
