# Advanced TypeScript and Library API Design

TypeScript is most valuable when it states relationships that survive real use: one key selects one property type; one schema produces one validated output; one package export names one supported entry point; one deprecation leads to one migration route. It is least valuable when it creates an impressive type expression that cannot be explained, tested, emitted cleanly, or kept aligned with JavaScript.

This course teaches the type system as part of a complete Node.js library contract.

## The course story

```text
structural assignability
        ↓
generic relationships and inference
        ↓
conditional type computation
        ↓
mapped and template-derived surfaces
        ↓
variance and callback safety
        ↓
declarations as an artifact
        ↓
Node package entry points
        ↓
runtime schema inference
        ↓
compatibility and migration
        ↓
whole-library change
```

## What you build

Each module has three reader-facing documents:

- `index.md` — the authoritative explanation;
- `workbook.md` — prediction, repair, construction, laboratory, and capstone transfer;
- `solutions.md` — causal explanations and principled repairs.

The independent laboratories isolate one mechanism. SchemaKit combines all ten modules into an ESM library whose runtime and static surfaces are intentionally paired.

## How to proceed

1. Read [the outcomes](outcomes.md).
2. Follow [the ten-day study plan](study-plan.md).
3. Begin [Module 21](module-21-structural-typing-assignability-and-public-shape/index.md).
4. Keep [the reference desk](reference.md) nearby.
5. Use [the SchemaKit engineering guide](capstone.md) after each chapter.
6. Finish with [the final review](final-review.md) before opening its [solutions](final-review-solutions.md).

A module is complete only when you can reconstruct the governing rule and apply it in a different product. Reading is necessary; independent transfer is the evidence.
