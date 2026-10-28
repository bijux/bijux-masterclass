# Laboratory 18 — Layout Observatory

**Course 2 · Module 18: Memory Representation, Validity, and Layout**

[Chapter](../../course-book/module-18-memory-representation-validity-and-layout/index.md) · [Workbook](../../course-book/module-18-memory-representation-validity-and-layout/workbook.md) · [Memory Workspace guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Memory Representation, Validity, and Layout**: Is a claim a language guarantee, a standard-library contract, a target-conditioned fact, a current observation, or an unsupported assumption? The product must make **Separate semantic value, validity invariant, abstract layout guarantee, ABI promise, and measured observation** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **representation table** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> Is a claim a language guarantee, a standard-library contract, a target-conditioned fact, a current observation, or an unsupported assumption?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Build a safe executable/library that records layout observations while refusing to present them as universal guarantees.

```text
labs/module-08-layout-observatory/
├── starter/
└── solution/
```

### Required experiments

- primitive, array, tuple, and struct size/alignment;
- one `repr(C)` padding calculation;
- one `repr(transparent)` newtype;
- thin and wide pointer observations;
- `size_of_val` for slices and strings;
- `String`, `Vec`, `Box<[T]>`, and `Rc<str>` owner/payload distinctions;
- `Option` size observations with guarantee labels;
- zero-sized types and logical collection length.

### Output model

Each row contains claim, observed value, classification (`Guaranteed` or `Observed`), target architecture, and explanatory note. Tests assert semantic/guaranteed relationships only; observed exact sizes are snapshot output, not portable pass conditions unless target-gated explicitly.

### Prohibitions

No unsafe blocks, transmute, raw byte reads, field-offset macros, or serialization from memory representation.

### Acceptance

```bash
cargo test -p rust-olm-lab-08-layout-observatory --all-targets
cargo clippy -p rust-olm-lab-08-layout-observatory --all-targets -- -D warnings
```

### Report architecture

Represent classification in the type system rather than embedding words in free-form notes:

```rust
pub enum ClaimClass {
    Guaranteed,
    TargetConditioned,
    Observed,
}
```

Each observation records a stable claim identifier, measured values, the classification, target metadata available from safe standard APIs or compile-time configuration, and a concise rationale. Rendering must be deterministic so two reports from the same executable can be compared. Exact observed sizes must not become unconditional tests.

For the `repr(C)` specimen, calculate expected offsets on the active target from field size and alignment, then compare the resulting total size and alignment. Because safe Rust cannot directly read field offsets without additional facilities, do not pretend to verify each offset. State the boundary precisely. For default `repr(Rust)` structs, record size and alignment only as observations and never infer declaration-order offsets.

### Owner versus payload worksheet

For `String`, `Vec<u32>`, `Box<[u32]>`, and `Rc<str>`, report separately:

- inline owner or handle bytes;
- logical payload length;
- exposed capacity where the API provides one;
- whether payload ownership is exclusive or shared;
- whether multiple handles may refer to one allocation;
- what allocator overhead is excluded.

Use `size_of_val` on dynamically sized referents and explain why a wide reference remains a sized value even though its referent is not `Sized`.

### Acceptance checks
Tests must establish general relationships—alignment is nonzero and a power of two, array size scales by element count when arithmetic fits, transparent wrappers match the represented field under the documented conditions, and slice `size_of_val` reflects length. Generate a human-readable observation report as an artifact, but mark target-specific snapshots as informational. Include a paragraph rejecting direct memory serialization and explaining the separate semantic codec that would be required.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Layout Observatory**.
2. Draw the smallest **representation table** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Memory Workspace so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 18 — Layout Observatory**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Layout Observatory**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Separate semantic value, validity invariant, abstract layout guarantee, ABI promise, and measured observation.
- Reason about size, alignment, padding, field non-overlap, repr(Rust), repr(C), and repr(transparent) without overclaiming offsets.
- Explain thin and wide pointers, metadata, slices, str, trait-object previews, and unsized tails.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 18 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **representation table**. Defend why your design is simpler than one plausible alternative under the new requirements.
