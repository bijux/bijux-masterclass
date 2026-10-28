# Source Notes and Claim Discipline

The course books are self-contained explanations, but exact language and library contracts still have primary owners. Use these sources when a diagnostic, API, layout, version, or platform detail must be verified precisely.

## Toolchain baseline

This release pins Rust 1.97.1 and Rust 2024 Edition. Rust 2024 was stabilized with Rust 1.85.0. A pinned toolchain keeps examples and diagnostics stable during study; it does not make every compiler implementation detail a permanent language guarantee.

## Claim categories

Every technical claim in the program should be read as one of these:

1. **Language guarantee** — specified by the Rust Reference or edition rules.
2. **Standard-library contract** — promised by the documented API.
3. **Cargo or rustc tool contract** — promised by the relevant tool documentation for the pinned release.
4. **Crate API contract** — promised by the exact pinned dependency and enabled features.
5. **Target- or platform-conditioned fact** — true only for named targets, operating systems, filesystems, ABIs, or runtime configurations.
6. **Observed artifact fact** — measured for a named source revision, toolchain, profile, target, and workload.
7. **Pedagogical model** — a simplified explanation that supports reasoning without replacing the formal contract.
8. **Product policy** — a choice made by a lab or capstone, not by Rust itself.

Do not promote an observation into a guarantee. A measured layout, symbol count, latency, or syscall sequence may change with compiler, target, optimization, dependency, or environment.

## Primary Rust sources

- The Rust Book: <https://doc.rust-lang.org/book/>
- The Rust Reference: <https://doc.rust-lang.org/reference/>
- The Standard Library: <https://doc.rust-lang.org/std/>
- The Rust Edition Guide: <https://doc.rust-lang.org/edition-guide/>
- The Cargo Book: <https://doc.rust-lang.org/cargo/>
- The rustc development guide: <https://rustc-dev-guide.rust-lang.org/>
- The Rustonomicon: <https://doc.rust-lang.org/nomicon/>
- The Unstable Book, used only to identify unstable boundaries: <https://doc.rust-lang.org/unstable-book/>
- Clippy documentation: <https://doc.rust-lang.org/clippy/>
- rustdoc documentation: <https://doc.rust-lang.org/rustdoc/>

## Course-specific source families

| Course | Primary source families |
|---:|---|
| 1 | Book, standard library, Cargo targets/tests/profiles, rustdoc, Clippy |
| 2 | Reference lifetime and type rules, `Box`, `Rc`, `Weak`, `Cell`, `RefCell`, `Cow`, `Pin`, Rustonomicon where unsafe consequences are discussed |
| 3 | Reference trait rules, dyn compatibility, associated items, coherence, Cargo SemVer guidance, Rust API Guidelines |
| 4 | Closure traits, `Iterator`, `IntoIterator`, `FromIterator`, `Extend`, `Option`, `Result`, collection contracts |
| 5 | Reference macro chapters, procedural macro API, Cargo build scripts, exact `proc-macro2`, `quote`, and `syn` documentation |
| 6 | Standard I/O/process/path/allocator APIs, Reference ABI and representation rules, Rustonomicon, platform manuals for durability and FFI claims |
| 7 | `std::thread`, synchronization primitives, atomic ordering documentation, Rust memory-model discussions, exact Rayon documentation |
| 8 | `Future`, `Waker`, async language rules, exact Tokio, Bytes, Futures Util, Hyper, Hyper Util, and HTTP Body Util documentation |
| 9 | Cargo profiles and release behavior, exact Criterion, Tracing, Tracing Subscriber, Tokio, Bytes, Hyper, and platform measurement tools |
| 10 | rustc guide for HIR/MIR/codegen concepts, Reference trait/type rules, Rustonomicon, Miri and verification-tool documentation, Cargo SemVer/MSRV/features/workspaces |

## Dependency policy

Courses 1–4, 6, and 10 keep their core products in the standard library so the mechanism remains visible. Course 5 uses the standard procedural-macro ecosystem. Course 7 uses Rayon for data-parallel work. Course 8 uses Tokio and the Hyper stack. Course 9 uses Criterion, Bytes, Tokio, Tracing, and related pinned crates. Exact versions live in `Cargo.toml`; the course explains why each dependency exists and which behavior remains application policy.

## Verification boundaries

A source link does not prove the local code compiles. A passing local test does not prove a language claim. A successful Miri run does not prove the absence of every undefined behavior. A benchmark does not prove production performance. A security advisory scan does not prove the absence of abuse paths. A release digest does not prove that the artifact is safe to operate.

Use the smallest source and evidence capable of falsifying the claim, and keep residual uncertainty visible.
