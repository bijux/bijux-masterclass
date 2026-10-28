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


## Course 7 — concurrency and parallelism

- Threads and scoped threads: <https://doc.rust-lang.org/std/thread/>
- Synchronization primitives: <https://doc.rust-lang.org/std/sync/>
- `Send`: <https://doc.rust-lang.org/std/marker/trait.Send.html>
- `Sync`: <https://doc.rust-lang.org/std/marker/trait.Sync.html>
- `Mutex`: <https://doc.rust-lang.org/std/sync/struct.Mutex.html>
- `Condvar`: <https://doc.rust-lang.org/std/sync/struct.Condvar.html>
- Message passing: <https://doc.rust-lang.org/std/sync/mpsc/>
- Atomic types and ordering: <https://doc.rust-lang.org/std/sync/atomic/>
- Rust Reference memory model note: <https://doc.rust-lang.org/reference/memory-model.html>
- Rustonomicon atomics chapter: <https://doc.rust-lang.org/nomicon/atomics.html>
- Rayon 1.12.0: <https://docs.rs/rayon/1.12.0/rayon/>


## Course 8 — async and networked services

- `Future`, `Poll`, `Context`, and `Waker`: <https://doc.rust-lang.org/std/future/trait.Future.html> and <https://doc.rust-lang.org/std/task/>
- Pinning: <https://doc.rust-lang.org/std/pin/>
- Standard-library networking: <https://doc.rust-lang.org/std/net/>
- Tokio 1.53.1: <https://docs.rs/tokio/1.53.1/tokio/>
- Tokio Util 0.7.19: <https://docs.rs/tokio-util/0.7.19/tokio_util/>
- Bytes 1.12.1: <https://docs.rs/bytes/1.12.1/bytes/>
- Futures Util 0.3.33: <https://docs.rs/futures-util/0.3.33/futures_util/>
- Hyper 1.8.0: <https://docs.rs/hyper/1.8.0/hyper/>
- Hyper Util 0.1.20: <https://docs.rs/hyper-util/0.1.20/hyper_util/>
- HTTP Body Util 0.1.4: <https://docs.rs/http-body-util/0.1.4/http_body_util/>


## Course 9 — performance and production engineering

- Cargo profiles: <https://doc.rust-lang.org/cargo/reference/profiles.html>
- Cargo features: <https://doc.rust-lang.org/cargo/reference/features.html>
- Criterion 0.8.2: <https://docs.rs/criterion/0.8.2/criterion/>
- Criterion user guide: <https://bheisler.github.io/criterion.rs/book/>
- Rust Performance Book: <https://nnethercote.github.io/perf-book/>
- Bytes 1.12.1: <https://docs.rs/bytes/1.12.1/bytes/>
- Tracing 0.1.44: <https://docs.rs/tracing/0.1.44/tracing/>
- Tracing Subscriber 0.3.23: <https://docs.rs/tracing-subscriber/0.3.23/tracing_subscriber/>
- Tokio 1.53.1: <https://docs.rs/tokio/1.53.1/tokio/>
- RustSec advisory database: <https://rustsec.org/>
- `cargo-audit`: <https://docs.rs/cargo-audit/>
- `cargo-deny`: <https://embarkstudios.github.io/cargo-deny/>

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
