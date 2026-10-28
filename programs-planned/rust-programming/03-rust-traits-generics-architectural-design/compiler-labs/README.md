# Course 3 Compiler and Design Investigations

These investigations train causal prediction. They are not quizzes about memorizing diagnostic wording. Each specimen isolates one language, runtime, build, schedule, or design relationship from Traits, Generics, and Architectural Design.

## Method

1. Read the specimen without compiling.
2. Classify the expected result: compile pass, compile fail, run pass, run fail, or manual design review.
3. Draw the smallest trait-law table, associated-type relationship map, coherence ownership map, dispatch map, typestate transition graph, adapter boundary, and compatibility matrix capable of deciding it.
4. State the intended cause and the earliest decisive phase or event.
5. Compile or run only after the prediction is fixed.
6. Apply the smallest principled repair.
7. Record one tempting repair that weakens the product contract.

A correct pass/fail guess with the wrong cause is not a successful investigation. When several diagnostics appear, identify which one would remain after unrelated mistakes were removed.

Run every course specimen with:

```bash
make compiler-labs
```

or run only this course from the program root:

```bash
python3 tools/run_compiler_labs.py 03-rust-traits-generics-architectural-design
```

Direct `rustc` cases compile into temporary directories. Cargo fixtures use isolated target directories. Negative cases are successful only when they fail for the intended relationship, not merely because the file contains some unrelated error.
