# Course 1 — Rust Foundations

## Values, Ownership, and Complete Programs

Learn to read Rust as a typed language, make ownership and failure visible, model valid states, and finish a complete tested program without depending on framework magic.

This directory is one ten-day course in the [sixty-module Rust program](../README.md). The [course book](course-book/index.md) is the primary learning path. The labs isolate one mechanism at a time, compiler specimens train causal prediction, and **Taskboard** tests whether the ten mechanisms can coexist in one product.

## Begin here

1. Read the [course overview](course-book/index.md).
2. Follow the [ten-day study plan](course-book/study-plan.md).
3. Work through each module in order: chapter, workbook, lab, capstone increment, then solutions.
4. Use the [course reference](course-book/reference.md) for recall after learning the derivation.
5. Finish with the [independent final review](course-book/final-review.md).

## Course outcome

By the end, you can design, implement, test, document, and change a small Rust application while explaining every ownership transfer, borrow, domain state, failure path, and public boundary.

## Practice surfaces

```text
course-book/    authoritative chapters, workbooks, solutions, capstone guide, reference
labs/           ten independent products with starter and reference implementation
compiler-labs/  isolated compile, runtime, and design-review investigations
capstone/       complete Taskboard implementation and tests
```

## Verification commands

From this directory:

```bash
make audit
make links
make compiler-labs   # requires Rust/Cargo
make test            # requires Rust/Cargo
make starters        # requires Rust/Cargo
make docs            # requires MkDocs
make proof
```

The commands support learning; they do not replace the explanation and transfer work in the course book.

[Open the course book](course-book/index.md) · [Return to the program start](../README.md)
