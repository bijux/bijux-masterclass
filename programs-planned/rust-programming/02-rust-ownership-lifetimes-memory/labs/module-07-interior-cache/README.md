# Laboratory 17 — Revisioned Interior Cache

This is the independent product for **Course 2, Module 17: Interior Mutability and Runtime Borrows**. Read the [module chapter](../../course-book/module-17-interior-mutability-and-runtime-borrows/index.md) and complete its [workbook](../../course-book/module-17-interior-mutability-and-runtime-borrows/workbook.md) before consulting the reference implementation.

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

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/`, add the first adversarial test before the design-changing repair, and complete the workbook’s transfer problem before reading the reference implementation.

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

> Which logically hidden mutation justifies runtime enforcement, and how can guard scope and reentrancy remain controlled?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Revisioned Interior Cache**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
