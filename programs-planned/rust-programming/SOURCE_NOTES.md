# Primary source notes

The course books contain the required explanations. These links identify the normative or primary contracts used to verify the material and to maintain future revisions. Open them when you need exact wording, a complete API surface, or release-specific behavior—not because a chapter omitted the mechanism.

## Program baseline

- Rust release index: <https://blog.rust-lang.org/releases/>
- Rust 2024 Edition Guide: <https://doc.rust-lang.org/edition-guide/rust-2024/index.html>
- Rust Reference: <https://doc.rust-lang.org/reference/>
- Rust standard library: <https://doc.rust-lang.org/std/>
- Cargo Book: <https://doc.rust-lang.org/cargo/>
- rustdoc Book: <https://doc.rust-lang.org/rustdoc/>
- Clippy documentation: <https://doc.rust-lang.org/clippy/>

The repository pins Rust 1.97.1 and uses Rust 2024 Edition. The program changes that baseline only through an explicit, versioned maintenance revision.

## Course 1 — foundations

- The Rust Programming Language: <https://doc.rust-lang.org/book/>
- Cargo package layout: <https://doc.rust-lang.org/cargo/guide/project-layout.html>
- Testing: <https://doc.rust-lang.org/book/ch11-00-testing.html>
- Error handling: <https://doc.rust-lang.org/book/ch09-00-error-handling.html>

## Course 2 — ownership, lifetimes, and memory

- References and borrowing: <https://doc.rust-lang.org/reference/types/pointer.html>
- Destructors: <https://doc.rust-lang.org/reference/destructors.html>
- Type layout: <https://doc.rust-lang.org/reference/type-layout.html>
- Subtyping and variance: <https://doc.rust-lang.org/reference/subtyping.html>
- `std::pin`: <https://doc.rust-lang.org/std/pin/>
- Rustonomicon: <https://doc.rust-lang.org/nomicon/>

## Course 3 — traits, generics, and architecture

- Traits: <https://doc.rust-lang.org/reference/items/traits.html>
- Implementations and coherence: <https://doc.rust-lang.org/reference/items/implementations.html>
- Trait objects: <https://doc.rust-lang.org/reference/types/trait-object.html>
- `impl Trait`: <https://doc.rust-lang.org/reference/types/impl-trait.html>
- SemVer compatibility: <https://doc.rust-lang.org/cargo/reference/semver.html>

## Course 4 — functional Rust

- Closure expressions: <https://doc.rust-lang.org/reference/expressions/closure-expr.html>
- `Fn`, `FnMut`, and `FnOnce`: <https://doc.rust-lang.org/std/ops/trait.Fn.html>
- `Iterator`: <https://doc.rust-lang.org/std/iter/trait.Iterator.html>
- `IntoIterator`: <https://doc.rust-lang.org/std/iter/trait.IntoIterator.html>
- `FromIterator`: <https://doc.rust-lang.org/std/iter/trait.FromIterator.html>
- `ControlFlow`: <https://doc.rust-lang.org/std/ops/enum.ControlFlow.html>

## Course 5 — metaprogramming

- Macros by example: <https://doc.rust-lang.org/reference/macros-by-example.html>
- Procedural macros: <https://doc.rust-lang.org/reference/procedural-macros.html>
- `proc_macro`: <https://doc.rust-lang.org/proc_macro/>
- Cargo build scripts: <https://doc.rust-lang.org/cargo/reference/build-scripts.html>
- `syn` 3.0.3: <https://docs.rs/syn/3.0.3/syn/>
- `quote` 1.0.47: <https://docs.rs/quote/1.0.47/quote/>
- `proc-macro2` 1.0.107: <https://docs.rs/proc-macro2/1.0.107/proc_macro2/>

## Course 6 — systems programming

- Byte slices and conversion APIs: <https://doc.rust-lang.org/std/primitive.slice.html>
- Files and filesystem operations: <https://doc.rust-lang.org/std/fs/>
- Paths and native strings: <https://doc.rust-lang.org/std/path/> and <https://doc.rust-lang.org/std/ffi/>
- Processes: <https://doc.rust-lang.org/std/process/>
- Unsafe operations: <https://doc.rust-lang.org/reference/unsafe-keyword.html>
- Raw pointers: <https://doc.rust-lang.org/std/primitive.pointer.html>
- `MaybeUninit`: <https://doc.rust-lang.org/std/mem/union.MaybeUninit.html>
- Allocator functions and `Layout`: <https://doc.rust-lang.org/std/alloc/>
- FFI chapter of the Rustonomicon: <https://doc.rust-lang.org/nomicon/ffi.html>
- C ABI type layout: <https://doc.rust-lang.org/reference/type-layout.html#the-c-representation>

## Claim discipline

Technical statements in these courses belong to one of these categories:

- Rust language guarantee;
- standard-library or Cargo contract;
- representation-attribute guarantee;
- target-, operating-system-, or filesystem-conditioned behavior;
- foreign-code obligation;
- current tool observation;
- pedagogical model;
- explicitly rejected assumption.

When the category changes the engineering conclusion, the chapter labels it. A convenient observation from one machine is never promoted into a portable guarantee without a contract that supports it.
