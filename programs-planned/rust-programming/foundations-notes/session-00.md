# Rust Foundations Course: 12-Session Comparative Program (Final Version)

A standalone, intensive Rust foundations course that covers the *modern* Rust language (Rust 2024 edition and later) from first principles to practical, real-world patterns — including ownership, lifetimes, traits, smart pointers, testing, basic concurrency, async, and interop.

The course is **comparative** by design: every major concept is positioned against **C/C++** and **Python** so experienced programmers can map Rust ideas onto what they already know.

---

## 0. Course Model

**Target audience**

- Strong background in at least one of: C, C++, Python, Java.
- Comfortable with functions, types, basic data structures, and control flow.
- Motivated to reason about memory, correctness, and performance.
- Familiarity with basic memory models (e.g., stack/heap, pointers/references, GC internals) and command-line tools.

**Rust version**

Course runs on Rust Edition 2024 with a pinned stable toolchain: rustc 1.91.0 (2025-10-30) / cargo 1.91.0. A rust-toolchain.toml is provided. We do not guarantee a global MSRV. Some notes reference features historically tied to older MSRVs (e.g., GATs ≥1.65), but all code compiles on the pinned toolchain.

**Per-session structure (~60–90 minutes)**

Each session contains:

- Setup checklist with verification steps and optional dependencies.
- Conceptual sections with diagrams, tables, and comparative trade-offs.
- Core concepts with definitions, mental models, compilable examples, and analyses.
- Debugging mini-labs, self-assessments, and tiered exercises with solutions (including compile-fail labs).
- Recap, synthesis reflection, self-quiz, glossary, error code index, references, concept map, and deep dive appendix.
- Cumulative project increment in the shared workspace.

**Tooling & workflow used throughout**

- `rustup`, `cargo`, `rust-analyzer` (VS Code or equivalent).
- `cargo test` and `#[test]`.
- `dbg!`, `cargo run`, `cargo check`.
- `cargo fmt`, `cargo clippy`.
- Optional: `cargo bench`, `flamegraph` for performance; `trybuild` for compile-fail tests; `proptest` for property-based testing.

**Error Handling Policy (Consistent Across Sessions)**

- Library returns task_core::Result<T> with typed thiserror errors.
- CLI uses anyhow + .context().

**Safety & Lints (Consistent Across Sessions)**

```rust
#![forbid(unsafe_code)]
#![deny(unused_must_use, missing_docs)]
// In CI via clippy:
// -D clippy::unwrap_used -D clippy::expect_used -D clippy::panic -D clippy::missing_errors_doc
```

**Cumulative mini-project**

- You maintain one evolving codebase (a multi-crate "Task Manager" CLI workspace) across sessions:
  - Session 1: Safe arithmetic CLI v0 with ownership mindset.
  - Session 2: Multi-Op Calculator v1 as a type-safe expression engine.
  - Session 3: Evolve to Task Manager v2 with heap-owned state like Vec<T>.
  - Session 4: Refactor to v3 using borrows for efficient access.
  - Session 5: Elevate to v4 with lib/bin split, richer types (structs/enums/newtypes), explicit errors, and tests.
  - Session 6: Enhance to v5 with generics for flexible storage and traits for command handling.
  - Session 7: Introduce multi-crate workspace (task_core, task_store_mem, etc.) and iterator-driven queries.
  - Session 8: Add lifetime annotations for safe references in TaskQuery<'a>.
  - Session 9: Use smart pointers like Box for recursive tasks and Rc<RefCell<Config>> for shared mutable config.
  - Session 10: Add concurrency with threads and channels for parallel queries.
  - Session 11: Introduce async with Tokio for non-blocking IO like file loading.
  - Session 12: Finalize as capstone with interop (C FFI or PyO3), profiling, security, and reflection.

---

## Session 1: Rust's Mindset – Correctness Through Ownership and Compile-Time Guarantees

**Goals**

- Shift thinking from ‘who frees memory’ to ‘who owns data and when.’
- Understand compile-time ownership/borrowing checks with no runtime cost.
- Install Rust and verify your setup.
- Create and run a basic project with Cargo.
- Trace ownership transfers and predict compiler rejections for dangling refs, double frees, and data races.

**Core coverage**

- Problem space: C/C++ manual memory/UB vs Python GC/dynamic typing vs Rust ownership/borrowing.
- Tooling: rustup, cargo new/build/run/check, rust-analyzer.
- Program anatomy: fn main, println!, dbg!, expressions vs statements.
- Basic ownership: moves, borrows, Drop determinism.

**Comparative angle**

- Ownership & Moves: C++ double free/aliases vs Python GC overhead.
- Borrowing & Lifetimes: C++ dangling refs vs Python runtime ref counting.
- Mut Exclusivity: C++ data races vs Python GIL.

**Debugging / tooling emphasis**

- Use dbg! to inspect values; cargo check for quick feedback.

**Security / performance note**

- Rust’s guarantees prevent memory safety vulnerabilities like buffer overflows and UAF.

**Mini-project (start of cumulative project)**

- Safe arithmetic CLI v0, applying ownership to prevent common bugs.

---

## Session 2: Rust’s Building Blocks – Types, Control Flow, and Pattern Matching

**Goals**

- Grasp memory-safe arithmetic with checked ops.
- Use compounds like tuples/arrays with ownership.
- Unify flow with expressions; type safety.
- Integrate ownership: Destructuring moves if not ref.
- Use types with safety awareness; expression flow with if/loop/for; exhaustive match with guards/or.

**Core coverage**

- Scalar types: iN/uN/f32/f64/bool/char; overflow safety.
- Compound types: tuples, arrays, slices &[T], &str.
- Control flow: if/loop/while/for as expressions.
- Pattern matching: match exhaustive, guards, or patterns.

**Comparative angle**

- Scalar Overflow: C/C++ UB vs Python big int perf hit.
- Slices: C/C++ pointer overrun vs Python copy O(n).
- Match Exhaustive: C/C++ fall-through vs Python no compile check.

**Debugging / tooling**

- Use dbg! in branches; cargo fmt for style.

**Mini-project (build on Session 1)**

- Extend to type-safe expression engine with structs and Option.

---

## Session 3: Ownership, Moves, Copy/Clone, and RAII – Enforcing Safety Through Single Ownership

**Goals**

- Trace ownership moves and predict compiler errors.
- Distinguish Copy (implicit) from Clone (explicit).
- Implement Drop for custom cleanup and understand RAII's deterministic nature.

**Core coverage**

- Ownership laws: single owner, moves invalidate old binding.
- Copy types duplicated; Clone explicit.
- Drop at scope end; RAII for resources.

**Comparative angle**

- Ownership & Moves: C++ double free/aliases vs Python GC overhead.
- Drop Determinism: C++ memory leaks vs Python nondeterministic GC.

**Debugging / tooling**

- Use dbg! to inspect ownership; cargo clippy for lints.

**Mini-project (extend cumulative project)**

- Evolve CLI to Task Manager v2 with heap-owned state like Vec<T>, showing move/clone trade-offs.

---

## Session 4: Borrowing, References, Slices, Lifetime Intuition – Safe and Efficient Data Access

**Goals**

- Understand borrowing rules and aliasing.
- Use &T/&mut T; slices &[T]/&str.
- Build lifetime intuition.
- Refactor owning APIs to borrowed.

**Core coverage**

- Borrowing laws: many &T or one &mut T; no outlive.
- Slices as views; &self sugar.
- Lifetime visualization.

**Comparative angle**

- Borrowing: C/C++ dangling pointers vs Python runtime-managed.
- Aliasing Rule: C/C++ races vs Python GIL.

**Debugging / tooling**

- Write tests for borrowed fns; fix borrow errors.

**Mini-project (extend cumulative project)**

- Refactor Task Manager to v3 using borrows for efficient access without transfer.

---

## Session 5: Structs, Enums, Option/Result, Error Handling + Testing – Type-Safe Data Modeling

**Goals**

- Model domain data with structs/enums/newtypes for invariants.
- Use Option/Result for absence/errors; propagate with ?.
- Write unit tests with assert macros, table-driven, integration.

**Core coverage**

- Structs: fields, methods; enums: variants.
- Option: map/and_then; Result: ?, thiserror/anyhow.
- Testing: #[test], table-driven, property-based.

**Comparative angle**

- Structs/Invariants: C/C++ manual checks vs Python runtime errors.
- Option/Result: C/C++ null/codes vs Python None/exceptions.

**Debugging / tooling**

- Fix type mismatch/unhandled errors; use proptest for properties.

**Mini-project (extend cumulative project)**

- Elevate to v4 with lib/bin, typed parsing, TaskStore trait, explicit errors, comprehensive tests.

---

## Session 6: Generics and Traits – Reusable and Extensible Code

**Goals**

- Define generics in functions/types.
- Define/implement traits; apply bounds/where.
- Design polymorphic code with traits.

**Core coverage**

- Generics: <T>, bounds :Trait.
- Traits: impl, defaults, associated types.
- Static vs dynamic dispatch teaser.

**Comparative angle**

- Generics: C/C++ template errors vs Python dynamic no checks.
- Traits: C/C++ virtual overhead vs Python duck typing.

**Debugging / tooling**

- Fix bound not satisfied (E0277); test generics with mocks.

**Mini-project (extend cumulative project)**

- Enhance to v5 with generics for storage and traits for command handling.

---

## Session 7: Modules, Crates, and Iterators – Organizing and Streaming Data

**Goals**

- Structure with modules/crates; pub/use.
- Compose iterator adaptors for pipelines.
- Implement Iterator; diagnose visibility/dependency errors.

**Core coverage**

- Modules: mod/pub/use; crates: lib/bin; workspaces.
- Iterators: impl Iterator, adaptors (map/filter/collect).
- Collections: Vec/String/HashMap interplay.

**Comparative angle**

- Modules: C/C++ header mess vs Python dynamic import.
- Iterators: C/C++ verbose loops vs Python eager lists.

**Debugging / tooling**

- Cargo test across crates; fix E0603 private access.

**Mini-project (extend cumulative project)**

- Split into multi-crate workspace; add iterator-driven queries and stable public API.

---

## Session 8: Lifetimes – Ensuring References Live Long Enough

**Goals**

- Internalize lifetime syntax/intuition for safe references.
- Understand subtyping/variance/'static.
- Annotate lifetimes; fix outlived borrows.

**Core coverage**

- 'a in fns/structs/traits; elision rules.
- NLL/reborrowing; HRTB for<'a>.
- Variance/subtyping.

**Comparative angle**

- Lifetimes: C/C++ dangling at runtime vs Python GC hides issues.

**Debugging / tooling**

- Fix E0515 dangling; use trybuild for compile-fail.

**Mini-project (extend cumulative project)**

- Add lifetime params to TaskQuery<'a>; borrowed iterator APIs.

---

## Session 9: Smart Pointers & Interior Mutability – Sharing Without Leaks

**Goals**

- Use Box/Rc/Arc/RefCell for heap/shared/mut.
- Apply Deref/Drop with smart pointers.
- Handle interior mutability safely.

**Core coverage**

- Box<T>: heap/recursive.
- Rc/Arc<T>: shared; Weak for cycles.
- RefCell/Mutex: runtime borrows.

**Comparative angle**

- Smart Pointers: C/C++ unique/shared_ptr vs Python refs.
- Interior Mut: C/C++ manual vs Python mutable everywhere.

**Debugging / tooling**

- Fix E0505 move out borrowed; test RefCell panics.

**Mini-project (extend cumulative project)**

- Use Box for recursive Task deps; Rc<RefCell<Config>> for shared mutable config.

---

## Session 10: Concurrency – Threads & Channels

**Goals**

- Spawn/join threads; use channels for communication.
- Grasp Send/Sync for thread safety.
- Choose threads for CPU-bound work.

**Core coverage**

- std::thread::spawn; crossbeam channels.
- Arc<Mutex<T>> for shared state.
- Scoped threads.

**Comparative angle**

- Threads: C/C++ races vs Python GIL.
- Channels: C/C++ manual sync vs Python queues.

**Debugging / tooling**

- Fix E0277 non-Send; test with barriers.

**Mini-project (extend cumulative project)**

- Add threads/channels for parallel queries; share with Arc<Mutex>.

---

## Session 11: Async – Non-Blocking Concurrency with Tokio

**Goals**

- Write async fns with tokio; use async/await.
- Design async APIs; fix async lifetime errors.
- Choose async for IO-bound work.

**Core coverage**

- Tokio runtime; async fn/await.
- tokio::spawn; mpsc channels.
- Select/timeout/join.

**Comparative angle**

- Async: C/C++ manual polling vs Python asyncio GIL-limited.

**Debugging / tooling**

- Fix E0728 await outside async; tokio::test.

**Mini-project (extend cumulative project)**

- Add async IO with Tokio (e.g., file load); use tokio::sync::mpsc.

---

## Session 12: Capstone Project, Concurrency, and Interop – Building Real-World Applications

**Goals**

- Integrate concepts into cohesive app.
- Apply concurrency/async; implement basic FFI/PyO3.
- Profile/secure code; reflect on Rust vs C/C++/Python.

**Core coverage**

- Capstone options: Advanced CLI, service stub, data tool, simulation.
- Interop: extern "C", PyO3 bindings.
- Perf: cargo bench, flamegraph; security: clippy, forbid(unsafe).

**Comparative angle**

- Concurrency: C/C++ races/leaks vs Python GIL/slow.
- Interop: C ABI mismatches vs Python ctypes overhead.

**Debugging / tooling**

- Fix Send/Sync bounds; integration tests for interop.

**Mini-project (extend cumulative project)**

- Finalize Task Manager with interop (C plugin/Py binding), concurrency/async, profiling, and reflection.

---

## Fast-Track and Extension Paths

- **Fast-track (6–8 sessions)**:
  - For experienced C++/systems devs, compress Sessions 1–2 and 5–6.
- **Deep-dive paths** after this course:
  - Advanced concurrency & async (Tokio, rayon, crossbeam).
  - Unsafe Rust & FFI in depth.
  - Web backends (Axum), CLI tooling (Clap), or embedded / no_std.
  - Formal verification / property-based testing (e.g., proptest, quickcheck).
