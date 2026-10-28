# Laboratory 17 — Revisioned Interior Cache

**Course 2 · Module 17: Interior Mutability and Runtime Borrows**

[Chapter](../../course-book/module-17-interior-mutability-and-runtime-borrows/index.md) · [Workbook](../../course-book/module-17-interior-mutability-and-runtime-borrows/workbook.md) · [Memory Workspace guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Interior Mutability and Runtime Borrows**: Which logically hidden mutation justifies runtime enforcement, and how can guard scope and reentrancy remain controlled? The product must make **Explain UnsafeCell as the primitive behind interior mutability while remaining within safe APIs** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **runtime-borrow trace** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> Which logically hidden mutation justifies runtime enforcement, and how can guard scope and reentrancy remain controlled?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Build `IndexedText`, an editable string with a lazily computed line-start index.

```text
labs/module-07-interior-cache/
├── starter/
└── solution/
```

### Required topology

- text and revision mutate only through `&mut self`;
- cache is private interior state reachable through `&self`;
- cache stores the revision it was computed from;
- hit/miss counters use `Cell<u64>`;
- no cache guard escapes the public API;
- public queries return copied ranges or borrowed slices tied to `&self`, not `Ref` unless explicitly justified.

### Required behavior

- line lookup by index;
- cold computation and hot reuse;
- invalidation after append/replace;
- UTF-8-safe ranges;
- no reentrant borrow panic;
- fallible `try_*` diagnostic route for a deliberately held internal borrow in tests;
- metrics excluded from semantic equality.

### Acceptance

```bash
cargo test -p rust-olm-lab-07-interior-cache --all-targets
cargo clippy -p rust-olm-lab-07-interior-cache --all-targets -- -D warnings
```

### Cache state machine

Model the private cache as `Empty` or `Ready { revision, line_starts }`, not as unrelated optional fields whose combinations can contradict one another. A query first checks whether a ready entry matches the current source revision. A miss computes line starts from immutable text without holding a cache guard, then installs the complete result in one mutation phase. Source mutation increments the revision and invalidates the cache before returning.

Line starts are byte offsets, because Rust string slicing operates at UTF-8 boundaries. Tests must contain multibyte characters and verify that every returned range is accepted by `str::get`. Do not claim character-index access unless you actually define and implement character counting.

### Failure and reentrancy tests
Add a private test hook or narrowly scoped diagnostic method that holds a cache borrow while invoking a supplied closure. Use it to prove that the fallible `try_*` route reports `CacheBusy` rather than panicking. The ordinary public query should not expose this hook. Also create a test in which an expensive computation helper calls a read-only source method; it must remain safe because computation occurs outside the mutable cache guard.

Required assertions cover cold miss, hot hit, append invalidation, full replacement, empty text, trailing newline, Unicode text, out-of-range line number, and metric behavior. Counters must not alter equality or the document revision.

### Design note
Provide a borrow timeline for one cache miss and one hit. Mark exactly when each `Ref` or `RefMut` guard is created and dropped. Then justify the public return type: state what callers can retain, what mutation it blocks, and what allocation it requires. The review rejects a design whose safety depends on callers remembering to drop an undocumented guard early.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Revisioned Interior Cache**.
2. Draw the smallest **runtime-borrow trace** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Memory Workspace so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 17 — Revisioned Interior Cache**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Revisioned Interior Cache**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Explain UnsafeCell as the primitive behind interior mutability while remaining within safe APIs.
- Choose Cell for replaceable Copy state and RefCell for single-threaded dynamically checked borrowed state.
- Treat Ref and RefMut as runtime loan guards whose scope is part of the API protocol.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 17 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **runtime-borrow trace**. Defend why your design is simpler than one plausible alternative under the new requirements.
