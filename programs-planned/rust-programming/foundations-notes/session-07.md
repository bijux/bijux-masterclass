# Session 7: Modules, Crates, and Iterators – Organizing and Streaming Data

**Target Audience & Scope:** This series assumes familiarity with C/Python, basic memory models (e.g., stack/heap, pointers/references, GC internals), and command-line tools. It targets programmers with systems or dynamic language experience new to Rust. Tone balances explanation for beginners in Rust but avoids over-simplifying semantics for intermediates.

No prior sessions required; basic Rust comfort helps.

**Conceptual Learning Goals:**  
- Structure code with modules and crates for clear boundaries and reuse.  
- Use iterators for lazy, efficient data processing.  
- Compose iterator adaptors to express pipelines without manual loops.  

**Mechanical Learning Goals:**  
- Define modules (mod/use/pub), enforce hierarchy and visibility.  
- Build lib/bin crates; run a Cargo workspace.  
- Implement Iterator and use adaptors like map/filter/collect.  
- Diagnose visibility, dependency, and iterator type errors.  

**Design Learning Goals:**  
- Promote Task Manager with a clean multi-crate workspace, a stable public API, iterator-driven queries.  
- Keep a strict facade; hide internals; test across crates.  

**By the End of This Session, You Can:**  
- Organize with modules/crates; apply pub/use correctly.  
- Create workspaces; compose iterator pipelines; implement custom iterators.  
- Fix visibility/dependency issues; extend the CLI with iterator-based flows.  

**Project Narrative:** Introduce modules and crates into a small ‘Task Manager’ example. Use a multi-crate workspace with a stable public API and iterator-driven queries.

**Error Handling Policy:** Library returns task_core::Result<T> with typed thiserror errors. CLI uses anyhow + .context().

**Safety & Lints:**  
```rust
#![forbid(unsafe_code)]
#![deny(unused_must_use, missing_docs)]
// In CI via clippy:
// -D clippy::unwrap_used -D clippy::expect_used -D clippy::panic -D clippy::missing_errors_doc
```

**MSRV Note:** This session uses GATs (Generic Associated Types). Add rust-version = "1.65" to Cargo.toml and create rust-toolchain.toml with:  
```
[toolchain]
channel = "stable"
```

**Decision Framework: Module vs Crate**  
- Small, related functions/types → module (mod).  
- Independent library/bin → crate (lib.rs or main.rs).  
- Multi-crate project → workspace (Cargo.toml [workspace]).  
- Public API → pub items; internal → no pub.  

**Anti-Patterns to Avoid**  
- Flat module structure; use hierarchies.  
- Over-public items; restrict with pub(crate).  
- Manual loops; prefer iterators.  
- Owning iterators when borrows suffice (& vs into_iter).  

**Public API Policy**  
- Use pub for exported items; pub(crate) for internal.  
- Avoid leaking internals; use re-exports (pub use).  
- No unnecessary generics in public APIs.  

**Dispatch Policy**  
- Static (<T: Trait>) inside crates.  
- Dynamic (dyn Trait) at boundaries if needed.  

**Perf and Binary Size Guidance**  
Iterators are zero-cost abstractions; prefer them for efficiency. Crates reduce compile times; workspaces for large projects.

**Architecture: Split into task_core (domain + traits), task_store_mem, task_store_fs, task_cli, optional task_prelude.**  
Workspace & Module Layout (Actionable)  
```
task-workspace/
├─ Cargo.toml # [workspace]
├─ task_core/ # lib crate: domain + traits + errors
│ ├─ src/
│ │ ├─ lib.rs // pub facade + prelude + modules
│ │ ├─ prelude.rs // curated re-exports
│ │ ├─ domain/{mod.rs, task.rs, id.rs, status.rs}
│ │ ├─ store/{mod.rs, traits.rs, iter.rs} // GAT-based iter types
│ │ └─ query/{mod.rs, filter.rs, sort.rs}
│ └─ tests/ // integration tests (public API only)
├─ task_store_mem/ # lib crate: in-memory store impl
│ └─ src/lib.rs
├─ task_store_fs/ # lib crate: file-backed store impl (optional)
│ └─ src/lib.rs
├─ task_cli/ # bin crate: CLI wiring, dyn boundary
│ └─ src/main.rs
└─ xtask/ # optional automation bin for dev tasks
```
Cargo (top-level)  
```toml
[workspace]
members = ["task_core", "task_store_mem", "task_store_fs", "task_cli"]
[profile.release]
lto = "thin"
codegen-units = 1
```
Visibility & Facade  
- Internal modules: pub(crate) or pub(super); never pub by default.  
- Public surface: task_core::prelude with re-exports:  
  ```rust
  // task_core/src/prelude.rs
  pub use crate::domain::{Task, TaskId, Status};
  pub use crate::store::TaskStore;
  pub use crate::query::{TaskQuery, Filter, SortKey};
  pub use crate::{Error, Result};
  ```
- lib.rs only re-exports prelude and stable modules. No deep paths leaking.

**Iterator Design (Production-Grade)**  
Goal: Borrowing iterators by default; owning variants when needed.  
```rust
// task_core/src/store/traits.rs
pub trait TaskStore {
    type Iter<'a>: Iterator<Item = &'a Task> where Self: 'a;
    type IterMut<'a>: Iterator<Item = &'a mut Task> where Self: 'a;
    fn insert(&mut self, t: Task) -> Result<()>;
    fn get(&self, id: &TaskId) -> Option<&Task>;
    fn get_mut(&mut self, id: &TaskId) -> Option<&mut Task>;
    fn iter(&self) -> Self::Iter<'_>;
    fn iter_mut(&mut self) -> Self::IterMut<'_>;
}
impl<'a, S: TaskStore> IntoIterator for &'a S {
    type Item = &'a Task;
    type IntoIter = S::Iter<'a>;
    fn into_iter(self) -> Self::IntoIter { self.iter() }
}
impl<'a, S: TaskStore> IntoIterator for &'a mut S {
    type Item = &'a mut Task;
    type IntoIter = S::IterMut<'a>;
    fn into_iter(self) -> Self::IntoIter { self.iter_mut() }
}
```
**Query Pipelines (no temp allocations)**  
```rust
// task_core/src/query/filter.rs
#[derive(Clone, Copy)]
pub enum SortKey { ByIdAsc }

#[derive(Clone, Copy)]
pub struct Filter { status: Option<Status> }

impl Filter {
    pub fn all() -> Self { Self { status: None } }
    pub fn status(s: Status) -> Self { Self { status: Some(s) } }
    pub fn matches(&self, t: &Task) -> bool {
        self.status.map(|s| t.status == s).unwrap_or(true)
    }
}
impl SortKey {
    pub fn sort_in_place<'a>(&self, v: &mut Vec<&'a Task>) {
        match self { SortKey::ByIdAsc => v.sort_by_key(|t| t.id.0) }
    }
}

pub struct TaskQuery<'a, S: TaskStore> {
    store: &'a S,
    filter: Option<Filter>,
    sort: Option<SortKey>,
}
impl<'a, S: TaskStore> TaskQuery<'a, S> {
    pub fn new(store: &'a S) -> Self { Self { store, filter: None, sort: None } }
    pub fn filter(mut self, f: Filter) -> Self { self.filter = Some(f); self }
    pub fn sort_by(mut self, k: SortKey) -> Self { self.sort = Some(k); self }
    pub fn collect(self) -> Vec<&'a Task> {
        let it = self.store.iter();
        let it = if let Some(f) = self.filter { it.filter(move |t| f.matches(t)) } else { it };
        let mut v: Vec<&Task> = it.collect(); // local vector for sorting when needed
        if let Some(k) = self.sort { k.sort_in_place(&mut v); }
        v
    }
}
```
**Ergonomic CLI usage (borrowed pipeline)**  
```rust
// task_cli/src/main.rs
use task_core::prelude::*;
use task_store_mem::MemStore;

fn main() -> anyhow::Result<()> {
    let mut s = MemStore::new();
    s.insert(Task { id: TaskId(2), title: "write".into(), status: Status::Doing, due_at: None })?;
    s.insert(Task { id: TaskId(1), title: "plan".into(),  status: Status::Done,  due_at: None })?;
    let q = TaskQuery::new(&s)
        .filter(Filter::status(Status::Done))
        .sort_by(SortKey::ByIdAsc);
    for t in q.collect() {
        println!("{} {}", t.id.0, t.title);
    }
    Ok(())
}
```
**Avoid these iterator mistakes**  
- Anti-pattern: collect::<Vec<_>>() mid-pipeline “just to make it easier”. Only collect at boundaries (e.g., for sorting or output).  
- Use iter() (borrow) vs into_iter() (move) deliberately; call .cloned() only when you must.  
- Use adaptors like by_ref, peekable, inspect for debugging without allocation.  

**Compile-Fail Mini-Labs (Retention + Rigor)**  
1. Visibility (E0603)  
   ```rust,compile_fail
   mod utils { fn hidden() {} }
   let x = utils::hidden(); // expect: E0603: function `hidden` is private
   ```  
   Fix: pub(crate) if it must be shared within the crate; pub only if part of public API.  
2. Unresolved Import (E0432/E0433)  
   ```rust,compile_fail
   use crate::internal::not_exported; // expect: failed to resolve
   ```  
   Fix: Re-export via pub use in the facade or stop reaching into internals.  
3. Iterator Item Mismatch (E0308)  
   ```rust,compile_fail
   struct BadIter;
   impl Iterator for BadIter {
       type Item = i32;
       fn next(&mut self) -> Option<u64> { None } // expect: E0308
   }
   ```  
4. Object Safety (E0038) when moving toward dyn at CLI boundary  
   ```rust,compile_fail
   trait Bad { fn f<T>(&self, _x: T); } // generic method -> not object-safe
   fn needs_obj(_: &dyn Bad) {}
   ```  
   Fix: Put any generic methods behind associated types or move them out of trait used as trait object.  
5. Orphan Rule (E0117)  
   ```rust,compile_fail
   // tests/compile_fail/orphan_rule/foreign_foreign_impl.rs
   // ❌ Implementing a foreign trait for a foreign type (disallowed)
   impl std::fmt::Display for std::net::Ipv4Addr {
       fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result { write!(f, "{:?}", self) }
   }
   ```  

Automate these with trybuild in task_core/tests/compile_fail/.  

**Testing Plan (Real, Not Token)**  
Unit (inside crates):  
- task_core: domain invariants, TaskQuery filters/sorts, iterator borrowing properties.  
- task_store_mem: insert/get/iter; ordering and stability (e.g., BTreeMap vs HashMap expectations).  
Integration (task_core/tests):  
- Treat task_core::prelude as only import path.  
- Black-box: construct store impl from task_store_mem, run queries via prelude API.  
Property Tests (proptest):  
- Generate random task sets; assert SortKey yields non-decreasing IDs; Filter::status never leaks other statuses.  
- Custom shrinkers; proptest strategies for Status, titles, due dates.  
- Determinism: stable order via BTreeMap or sort-before-assert.  
Compile-Fail (trybuild):  
- Private symbol access, import of non-re-exported module, object-safety violations, orphan rule.  
Doc Tests (doctest):  
- Every public function/trait in prelude has a doctest demonstrating correct imports and iterator usage.  
Optional Benchmarks (criterion):  
- Naive loops vs iterator pipelines; confirm zero-cost (or explain any regressions).  

**Public API Policies (Enforced)**  
- No deep module paths in examples. Only use task_core::prelude::*;  
- impl Trait in parameters for functions; associated types inside traits.  

**“Done Means Done” Checklist**  
Architecture  
- Workspace split with task_core, task_store_mem, task_cli compiling clean.  
- task_core::prelude exists and examples use it exclusively.  
API  
- No unintended pub items; CI denies missing_docs.  
- Iterator API exposes naive iterators (Iter<'a>) and optional owning variants.  
Quality Gates  
- cargo clippy -- -D warnings passes.  
- RUSTDOCFLAGS="-D missing-docs" docs build.  
- trybuild compile-fail tests in place (visibility/object safety).  
- proptest properties for filters and sorts.  
- All examples/doctests compile with only the prelude.  
Performance  
- No mid-pipeline collect unless required; comments justify it.  
- Benchmarks show iterator pipelines are not slower than manual loops for core paths.  

**Targeted Code Triples (keep your series pattern)**  
**Rust (Lazy iterator):**  
```rust
use chrono::{DateTime, Utc};
pub fn overdue<'a, S: TaskStore>(s: &'a S, now: DateTime<Utc>) -> impl Iterator<Item = &'a Task> + 'a {
    s.iter().filter(move |t| t.due_at.map(|d| d < now).unwrap_or(false))
}
```  

**C++ (Ranges pseudo):**  
```cpp
// views::filter(due_at < now); returns a lazy view
```  

**Python (Generator):**  
```python
def overdue(tasks, now):
    for t in tasks:
        if t.due_at is not None and t.due_at < now:
            yield t
```

**Common Pitfalls (Call Them Out Explicitly)**  
- Leaky Facade: Letting consumers import task_core::store::traits::TaskStore. Fix: re-export in prelude and mark internals pub(crate).  
- Iterator Ownership Confusion: Using into_iter() on Vec<&T> unexpectedly yields &T (fine) vs on Vec<T> moving T (not fine). Educate with one crisp example and a test.  

**Ownership Matrix (Explicit & Testable)**  
| Collection | Call | Item | Moves? | Common Pitfall |
|------------|------|------|--------|----------------|
| Vec<T> | iter() | &T | No | Expecting ownership |
| Vec<T> | iter_mut() | &mut T | No | Borrow rules block nested iteration |
| Vec<T> | into_iter() | T | Yes | Use only when you mean to consume |
| Vec<&T> | into_iter() | &T | No | Surprising: “into” still yields references |

```rust
#[test]
fn ownership_matrix_smoke() {
    let mut v = vec![1, 2, 3];
    let sum_borrow = v.iter().copied().sum::<i32>();
    let sum_mut = { v.iter_mut().map(|x| { *x += 1; *x }).sum::<i32>() };
    let sum_move = v.into_iter().sum::<i32>(); // v consumed
    assert_eq!(sum_borrow, 6);
    assert_eq!(sum_mut, 9);
    assert_eq!(sum_move, 9);
}
```

**.cargo/config.toml Hardening (Workspace-Wide)**  
```toml
[target.'cfg(all())']
rustflags = ["-Dwarnings"]
rustdocflags = ["-Dwarnings", "-Drustdoc::broken_intra_doc_links"]
```

**Feature Flags + Rayon Example (Gated, MSRV-Safe)**  
```toml
[features]
default = []
fs-store = []
rayon = ["dep:rayon"]

[dependencies]
rayon = { version = "1", optional = true }
```

```rust
// task_core/src/query/parallel.rs
#[cfg(feature = "rayon")]
use rayon::prelude::*;
#[cfg(feature = "rayon")]
pub fn sum_done_ids_parallel<'a, S: TaskStore>(s: &'a S) -> u64
where
    S: Sync,
{
    s.iter().par_bridge()
        .filter(|t| t.status == Status::Done)
        .map(|t| t.id.0 as u64)
        .sum()
}
```

**C++ (Parallel pseudo):**  
```cpp
// std::execution::par + std::reduce on filter view
```  

**Python (Concurrent):**  
```python
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor() as executor:
    sum(executor.map(lambda t: t.id if t.done else 0, tasks))
```

**Criterion Bench (Prove “Zero-Cost” Claim)**  
```rust
// benches/iter_vs_loop.rs
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn manual_loop(xs: &[u64]) -> u64 {
    let mut acc = 0;
    for &x in xs { if x % 2 == 0 { acc += x * 2 } }
    acc
}
fn iterator_chain(xs: &[u64]) -> u64 {
    xs.iter().copied().filter(|x| x % 2 == 0).map(|x| x * 2).sum()
}
fn bench(c: &mut Criterion) {
    let xs: Vec<u64> = (0..100_000).collect();
    c.bench_function("manual_loop", |b| b.iter(|| manual_loop(black_box(&xs))));
    c.bench_function("iterator_chain", |b| b.iter(|| iterator_chain(black_box(&xs))));
}
criterion_group!(benches, bench);
criterion_main!(benches);
```

```toml
# task_core/Cargo.toml
[dev-dependencies]
criterion = { version = "0.5", default-features = false }
[[bench]]
name = "iter_vs_loop"
harness = false
```

**File-Backed, Streaming Store (Borrowed View Example)**  
```rust
// task_store_fs/src/lib.rs (sketch)
pub struct FsStore {
    path: std::path::PathBuf,
    buf: String,
    lines: Vec<std::ops::Range<usize>>,
}
impl FsStore {
    pub fn open(path: impl Into<std::path::PathBuf>) -> Result<Self> {
        let path = path.into();
        let buf = std::fs::read_to_string(&path).map_err(Error::Io)?;
        let mut start = 0;
        let mut lines = Vec::new();
        for (i, b) in buf.bytes().enumerate() {
            if b == b'\n' { lines.push(start..i); start = i + 1; }
        }
        Ok(Self { path, buf, lines })
    }
}
impl TaskStore for FsStore {
    type Iter<'a> = std::iter::Map<std::slice::Iter<'a, std::ops::Range<usize>>, fn(&'a std::ops::Range<usize>) -> &'a Task> where Self: 'a;
    type IterMut<'a> = std::iter::Empty<&'a mut Task> where Self: 'a; // read-only demo
    fn insert(&mut self, _t: Task) -> Result<()> { Err(Error::Parse("write not impl".into())) }
    fn get(&self, _id: &TaskId) -> Option<&Task> { None }
    fn get_mut(&mut self, _id: &TaskId) -> Option<&mut Task> { None }
    fn iter(&self) -> Self::Iter<'_> { self.lines.iter().map(|r| {
        let line = &self.buf[r.clone()];
        Task::from_line(line).unwrap() // sketch; use Result in real
    }) }
    fn iter_mut(&mut self) -> Self::IterMut<'_> { std::iter::empty() }
}
```

impl Task {
    pub fn from_line(line: &str) -> Result<Task> {
        // sketch parse; real impl would handle errors
        Ok(Task { id: TaskId(0), title: line.to_string(), status: Status::Todo, due_at: None })
    }
}

**C++ (File stream):**  
```cpp
std::ifstream f; std::string line; while (std::getline(f, line)) { parse(line); }
```

**Python (File iter):**  
```python
with open('file') as f: for line in f: parse(line)
```

**Enforce Prelude-Only Import Rule (Compile-Fail Doctest)**  
```rust
// task_core/tests/compile_fail/prelude_only.rs
#[test]
fn deep_imports_rejected() {
    let t = trybuild::TestCases::new();
    t.compile_fail("tests/compile_fail/prelude_only/*.rs");
}
```

```rust
// task_core/tests/compile_fail/prelude_only/deep_path.rs
use task_core::store::traits::TaskStore; // Should not be publicly reachable
fn main() {}
```

**Advanced Iterators & Streaming**  
Fallible pipelines: Iterator<Item = Result<T,E>>, try_fold, flatten_ok, early error exit.  

```rust
/// Turn a fallible task stream into a collected Vec, short-circuiting on first error.
pub fn collect_checked<'a, I>(it: I) -> Result<Vec<&'a Task>>
where
    I: Iterator<Item = Result<&'a Task>>,
{
    it.try_fold(Vec::new(), |mut acc, t| {
        acc.push(t?);
        Ok(acc)
    })
}
```

Marker traits: ExactSizeIterator, FusedIterator (implement safely), when not to promise TrustedLen.  

```rust
#[derive(Clone)]
pub struct SliceIter<'a, T> { inner: std::slice::Iter<'a, T> }

impl<'a, T> Iterator for SliceIter<'a, T> {
    type Item = &'a T;
    fn next(&mut self) -> Option<Self::Item> { self.inner.next() }
    fn size_hint(&self) -> (usize, Option<usize>) { self.inner.size_hint() }
}
impl<'a, T> ExactSizeIterator for SliceIter<'a, T> {}
impl<'a, T> std::iter::FusedIterator for SliceIter<'a, T> {}
```

In-place transforms: map_while, by_ref, peekable, inspect (debugging without allocation).  

Optional parallel path: rayon’s ParallelIterator, and boundary Send + Sync constraints.  

**API Evolution & Semver Control**  
Public-surface policy: avoid generic params in public data types unless they model domain; deprecate with #[deprecated].  

Feature flags: e.g., fs-store, bench, rayon; keep MSRV stable.  

Breaking-change checklist: associated types vs. generic methods, object safety.  

Version-gated examples: #[cfg(feature = "rayon")] guarding parallel listing.  

**Workspace Engineering & CI Hardening**  
Cargo graph hygiene: task_cli depends only on the facade; forbid deep dev-deps.  

.cargo/config.toml: global -D warnings; rustdoc lints (rustdoc::broken_intra_doc_links).  

trybuild layout: UI tests for E0603/E0038/E0117 and an orphan-rule fail (E0117).  

Criterion harness: naive loop vs iterator chain; notes on noise control and CI tolerances.  

**Common Error Box:** Proxy? Fix config or manual download.

**Self-Assessment:**  
[ ] Verified Rust installation and ran first project.  
[ ] Completed the lab and reflected on macro errors.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

**Appendix: Platform-Specific Notes**  
- Windows: Run installer as admin for PATH setup; verify in new PowerShell.  
- Unix: Ensure curl uses HTTPS; manual download if needed.

---

## Part I: Modules – Granular Code Organization

**You Will Be Able To:**  
- Define modules with mod and use statements.  
- Apply pub, pub(crate), pub(super) for visibility.  
- Contrast with C/C++ headers and Python modules.  

### Core Concept: Case 1 – Basic Modules and Visibility

**Problem / Motivation:** Scattered code; C/C++ headers separate; Python modules dynamic.

**Definition (Formal):** Module: Group related items; visibility with pub.

**Mental Model (Simplified):** Namespaces; control access.

**Example (Compilable):** Simple module.  
```rust
mod domain {
    pub struct Task { /* ... */ }
}
use domain::Task;
```

**Code Triple:**  
**Rust (Visibility):**  
```rust
mod utils { pub fn helper() {} }
```  

**C/C++ (Header):**  
```cpp
// utils.h
void helper();
```  

**Python (Import):**  
```python
# utils.py
def helper(): pass
```

**Rust Failure Variant:** Private access.  
```rust
mod utils { fn hidden() {} }
let x = utils::hidden();
```

**Compiler Output (Key lines; messages may vary):**  
```
error[E0603]: function `hidden` is private
 --> src/main.rs:3:13
  |
3 | let x = utils::hidden();
  |             ^^^^^^ private function
```

Error code: E0603.

**Compiler Reasoning Steps:**  
- Checks visibility.  
- Rejects private access.

**Analysis:**  
- Ownership impact: None direct.  
- Performance: Compile only.  
- Typical compiler error: E0603.

**ASCII Diagram: Module Hierarchy**  
```
crate
├── main.rs
└── domain
    └── task.rs
```

**Micro-Challenge Variations:** Predict: Access pub(crate) from same crate.  

**Solution to Micro-Challenge:** Allowed.  

**Contrast:** C++ linkage; Python runtime.  

**Takeaway:** Modules enforce boundaries.

> **Lab – Try This:** Create domain module; use Task.  
> **Solution:** mod domain; use domain::Task;

[Design] **Reflection – Think:** Why pub(crate)?  
[Answer] **Model Answer:** Crate-internal sharing.

[Semantics] **Think like the Compiler:** What for pub(in path)? (Answer: Limit to subtree.)

### Core Concept: Case 2 – Granular Visibility and Facades

**Problem / Motivation:** Leaky internals; over-exposure.

**Definition (Formal):** pub(super): Parent module; pub(in path): Path.

**Mental Model (Simplified):** Limit scope.

**Example (Compilable):** Granular.  
```rust
mod store {
    pub(in crate::store) trait PrivateExt { /* ... */ }
    pub(crate) trait TaskStoreCore { /* ... */ }
    pub use public::TaskStore;
    mod public { pub trait TaskStore { /* ... */ } }
}
```

**Code Triple:**  
**Rust (Re-export):**  
```rust
pub use domain::Task;
```  

**C/C++ (Include):**  
```cpp
#include "domain/task.h"
```  

**Python (From):**  
```python
from domain import Task
```

**Rust Failure Variant:** Deep import.  
```rust
use crate::internal::not_exported;
```

**Compiler Output:** E0433 (failed to resolve).

**Compiler Reasoning Steps:**  
- Resolves path.  
- Rejects missing.

**Analysis:**  
- Ownership impact: None.  
- Performance: None.  
- Typical compiler error: E0433.

**Takeaway:** Facades stabilize APIs.

> **Lab – Try This:** Re-export in prelude.  
> **Solution:** pub use crate::domain::Task;

[Design] **Reflection – Think:** Why seal traits?  
[Answer] **Model Answer:** Block external impls.

**Part I Checkpoint:** Visibility for?  
**Answers:** Control access.

**You Can Now:**  
- Use granular visibility.  
- Build facades.

**Part I Quiz:** (5 MCQs + 1 open conceptual question)  
1. pub(super) visible to? (a) Crate (b) Parent (c) All  
   Answer: (b)  
2. True/False: Re-exports hide paths.  
   Answer: True  
3. E0603 cause? (a) Private access (b) Type mismatch (c) Lifetime  
   Answer: (a)  
4. Facade purpose? (a) Leak internals (b) Stabilize API (c) Performance  
   Answer: (b)  
5. True/False: Modules affect ownership.  
   Answer: False  
Open Conceptual: Explain granular visibility.  
Answer: Limits scope to prevent leaks.

**Self-Assessment:**  
[ ] Created modules.  
[ ] Fixed E0603.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part II: Crates and Workspaces – Modular Projects

**You Will Be Able To:**  
- Create lib/bin crates.  
- Set up workspaces.  
- Manage dependencies.  

### Core Concept: Case 1 – Lib and Bin Crates

**Problem / Motivation:** Monolith; separation for reuse.

**Definition (Formal):** Crate: Compilation unit; lib or bin.

**Mental Model (Simplified):** Packages; workspace groups.

**Example (Compilable):** Lib crate.  
```rust
// task_core/src/lib.rs
pub mod prelude;
```

**Code Triple:**  
**Rust (Crate):**  
```rust
// Cargo.toml [lib]
```  

**C/C++ (Lib):**  
```cpp
// CMakeLists.txt
add_library(task_core ...)
```  

**Python (Package):**  
```python
# setup.py
setup(name='task_core'...)
```

**Rust Failure Variant:** Missing dep.  
```toml
[dependencies]
missing_crate = "1.0"
```

**Compiler Output:** E0463 (can't find crate).

**Analysis:**  
- Ownership impact: None.  
- Performance: Faster compiles.  
- Typical: E0463.

**ASCII Diagram: Workspace**  
```
workspace
├── task_core
└── task_cli
```

**Micro-Challenge Variations:** Predict: Root cargo test.  

**Solution to Micro-Challenge:** Tests all members.  

**Contrast:** C++ build systems; Python pip.  

**Takeaway:** Crates modularize.

> **Lab – Try This:** Create workspace; add crates.  
> **Solution:** [workspace] members = [...]

**Part II Checkpoint:** Workspace for?  
**Answers:** Multi-crate management.

**You Can Now:**  
- Build crates.  
- Use workspaces.

**Part II Quiz:** (5 MCQs + 1 open conceptual question)  
1. Lib crate file? (a) main.rs (b) lib.rs (c) mod.rs  
   Answer: (b)  
2. True/False: Workspaces share deps.  
   Answer: False  
3. E0463 cause? (a) Missing crate (b) Private (c) Type  
   Answer: (a)  
4. Bin crate for? (a) Library (b) Executable (c) Test  
   Answer: (b)  
5. True/False: Crates reduce compile time.  
   Answer: True  
Open Conceptual: Explain lib vs bin.  
Answer: Reuse vs entry point.

**Self-Assessment:**  
[ ] Set up workspace.  
[ ] Fixed dep errors.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part III: Iterators – Lazy Data Processing

**You Will Be Able To:**  
- Implement Iterator trait.  
- Use adaptors like map/filter.  
- Handle fallible iterators.  

### Core Concept: Case 1 – Basic Iterators

**Problem / Motivation:** Manual loops; inefficient.

**Definition (Formal):** Iterator: next() -> Option<Item>.

**Mental Model (Simplified):** Lazy sequence.

**Example (Compilable:** Custom iter.  
```rust
struct SliceIter<'a, T> { inner: std::slice::Iter<'a, T> }
impl<'a, T> Iterator for SliceIter<'a, T> {
    type Item = &'a T;
    fn next(&mut self) -> Option<Self::Item> { self.inner.next() }
}
```

**Code Triple:**  
**Rust (Lazy):**  
```rust
(1..10).filter(|&x| x % 2 == 0).collect::<Vec<_>>()
```  

**C/C++ (STL):**  
```cpp
std::vector<int> v; for(int i=1;i<10;i++) if(i%2==0) v.push_back(i);
```  

**Python (List Comp):**  
```python
[x for x in range(1,10) if x % 2 == 0]
```

**Rust Failure Variant:** Item mismatch.  
```rust
impl Iterator for BadIter {
    type Item = i32;
    fn next(&mut self) -> Option<u64> { None }
}
```

**Compiler Output:** E0308 (mismatched types).

**Analysis:**  
- Ownership impact: Borrow vs own.  
- Performance: Zero-cost.  
- Typical: E0308.

**ASCII Diagram: Iterator Chain**  
```
iter -> filter -> map -> collect
```

**Micro-Challenge Variations:** Predict: size_hint on exact.  

**Solution to Micro-Challenge:** (len, Some(len))  

**Contrast:** C++ verbose; Python eager.  

**Takeaway:** Lazy efficient.

> **Lab – Try This:** Chain filter/map.  
> **Solution:** .filter(...).map(...)

### Core Concept: Case 2 – Advanced and Fallible Iterators

**Problem / Motivation:** Errors in streams; ownership confusion.

**Definition (Formal):** Fallible: Item = Result<T,E>.

**Mental Model (Simplified):** Short-circuit on err.

**Example (Compilable:** Fallible collect.  
```rust
pub fn collect_checked<'a, I>(it: I) -> Result<Vec<&'a Task>>
where
    I: Iterator<Item = Result<&'a Task>>,
{
    it.try_fold(Vec::new(), |mut acc, t| {
        acc.push(t?);
        Ok(acc)
    })
}
```

**Code Triple:**  
**Rust (Try fold):**  
```rust
it.try_fold(0, |acc, x| Ok(acc + x?))
```  

**C/C++ (Loop):**  
```cpp
int acc = 0; for(auto& x : xs) { if(err) break; acc += x; }
```  

**Python (Gen):**  
```python
acc = 0; for x in xs: if err: break; acc += x
```

**Rust Failure Variant:** Ownership mix.  
```rust
let v: Vec<Task> = vec![...];
let it = v.into_iter(); // moves
```

**Compiler Output:** E0505 (moved).

**Analysis:**  
- Ownership impact: Move vs borrow.  
- Performance: Early exit.  
- Typical: E0505.

**Takeaway:** Handle errors lazily.

> **Lab – Try This:** Implement fallible iter.  
> **Solution:** Item = Result<&Task>

**Part III Checkpoint:** Iterators lazy?  
**Answers:** Yes, compute on next.

**You Can Now:**  
- Implement iterators.  
- Use advanced adaptors.

**Part III Quiz:** (5 MCQs + 1 open conceptual question)  
1. Iterator method? (a) next (b) get (c) fetch  
   Answer: (a)  
2. True/False: Adaptors eager.  
   Answer: False  
3. Fallible Item? (a) Option (b) Result (c) Vec  
   Answer: (b)  
4. try_fold for? (a) Short-circuit (b) Collect (c) Map  
   Answer: (a)  
5. True/False: iter borrows.  
   Answer: True  
Open Conceptual: Explain lazy vs eager.  
Answer: Compute on demand vs all at once.

**Self-Assessment:**  
[ ] Built iterators.  
[ ] Handled fallible.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part IV: Application, Testing, and API Evolution

**You Will Be Able To:**  
- Apply in project with workspaces/iterators.  
- Test modular code.  
- Evolve APIs with semver.  

### Core Concept: File-Backed Streaming Store

**Problem / Motivation:** Persistent data; streaming load.

**Definition (Formal):** Owning iter for files.

**Mental Model (Simplified):** Parse lines lazily.

**Example (Compilable:** FS iter.  
```rust
use std::io::BufRead;
pub struct FsOwnedIter<R: std::io::BufRead> { lines: std::io::Lines<R> }
impl<R: std::io::BufRead> Iterator for FsOwnedIter<R> {
    type Item = Result<Task>;
    fn next(&mut self) -> Option<Self::Item> {
        self.lines.next().map(|res| {
            let line = res.map_err(Error::Io)?;
            Task::from_line(&line)
        })
    }
}
```

**Code Triple:**  
**Rust (Streaming):**  
```rust
let iter = FsOwnedIter { /* ... */ };
```  

**C/C++ (File stream):**  
```cpp
std::ifstream f; std::string line; while (std::getline(f, line)) { parse(line); }
```  

**Python (File iter):**  
```python
with open('file') as f: for line in f: parse(line)
```

**Analysis:**  
- Ownership impact: Owns reader.  
- Performance: Lazy parse.  
- Typical: IO errors.

**Takeaway:** Stream persistence.

> **Lab – Try This:** Implement FS store.  
> **Solution:** BufRead lines.

### Core Concept: API Evolution and Semver

**Problem / Motivation:** Changes break users.

**Definition (Formal):** Deprecate; feature flags.

**Mental Model (Simplified):** Controlled evolution.

**Example (Compilable:** Deprecated.  
```rust
#[deprecated = "Use new_method"]
fn old_method() {}
```

**Analysis:**  
- Ownership impact: None.  
- Performance: None.  
- Typical: Warnings.

**Takeaway:** Semver guides.

> **Lab – Try This:** Add flag for FS.  
> **Solution:** [feature = "fs"]

### Core Concept: Workspace Engineering and CI Hardening

**Problem / Motivation:** Consistent builds.

**Definition (Formal):** Lints in CI.

**Mental Model (Simplified):** Automate quality.

**Example (YAML):** CI lints.  
```yaml
- name: Lints
  run: |
    cargo fmt -- --check
    cargo clippy --workspace --all-targets -- -D warnings
    RUSTDOCFLAGS="-D warnings -D rustdoc::broken_intra_doc_links" cargo doc --workspace --no-deps
- name: Tests
  run: cargo test --workspace --all-features
```

**Analysis:**  
- Ownership impact: None.  
- Performance: CI time.  
- Typical: Lint fails.

**Takeaway:** Harden workflows.

> **Lab – Try This:** Add CI yaml.  
> **Solution:** Run lints/tests.

**Part IV Checkpoint:** Testing for?  
**Answers:** Boundaries/invariants.

**You Can Now:**  
- Evolve APIs.  
- Harden CI.

**Part IV Quiz:** (5 MCQs + 1 open conceptual question)  
1. Deprecated for? (a) Remove (b) Warn (c) Error  
   Answer: (b)  
2. True/False: Features optional.  
   Answer: True  
3. trybuild for? (a) Fail tests (b) Unit (c) Prop  
   Answer: (a)  
4. CI lints? (a) Optional (b) Enforce (c) Ignore  
   Answer: (b)  
5. True/False: Streaming owns.  
   Answer: True  
Open Conceptual: Explain semver.  
Answer: Compatible changes.

**Self-Assessment:**  
[ ] Applied workspace/iterators.  
[ ] Tested modular.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Exercises: Tiered Reasoning

### Tier 1: Concept Rebuilds

1. Module Def  
   mod domain { pub struct Task; }  
   **Solution:** Use domain::Task.

2. Iterator Impl  
   Simple range.  
   **Solution:** struct Range { cur: i32, end: i32 } impl Iterator { ... }

### Tier 2: Comparative Rewrites

1. C Header to Module  
   Re-export.  
   **Solution:** pub use.

2. Python Gen to Iterator  
   Lazy yield.  
   **Solution:** next yields Option.

### Tier 3: Challenge Extensions

1. Fallible Pipeline  
   try_fold.  
   **Solution:** Short-circuit err.

2. Granular Visibility  
   pub(in path).  
   **Solution:** Limit scope.

**Self-Assessment:**  
[ ] Completed one per tier.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Recap and Synthesis Reflection

**Table Completion Exercise:**  
| Rust Feature | C/C++ Issue | Python Trade-off |
|--------------|-------------|------------------|
| Modules | Header mess | Dynamic import |
| Crates/Workspaces | Build complexity | Package overhead |
| Iterators | Verbose loops | Eager lists |

**Self-Quiz:** (Design-level)  
1. Modules for?  
2. Iterators lazy?  
3. Facade purpose?  
Answers:  
1. Organization.  
2. Yes.  
3. Stable API.

**Final Takeaway:** Modules/crates/iterators organize/process.

**By Session End:**  
- Organize with modules/crates.  
- Use pub/use.  
- Create workspaces.  
- Implement/use iterators.  
- Compose adaptors.  
- Fix visibility/dependency errors.  
- Extend CLI with modules/iterators.

**Glossary Appendix Update:** Add: Module, Crate, Workspace, Iterator, Adaptor.

**Error Code Index:**  
| Code   | Description                     | Example Case |
|--------|---------------------------------|--------------|
| E0603  | Item is private                 | Private access |
| E0433  | Failed to resolve               | Missing use |
| E0599  | Method not found                | No Iterator impl |
| E0308  | Mismatched types                | Item mismatch |
| E0038  | Trait not object safe           | Trait object fail |
| E0117  | Only one impl for trait         | Orphan rule |
| E0463  | Can't find crate                | Missing dep |

**Primary References:** Rust Book Ch. 7 (Modules), Ch. 13 (Iterators).  
**Suggested Deep Dives:** Cargo workspaces; custom iterators.

**Concept Map:** (Text-based ASCII)  
Modules (mod/use/pub)  
Crates (lib/bin)  
  └── Workspaces ([workspace])  
Iterators (next/Item)  
  └── Adaptors (map/filter)  
Applied (Task example)

**Self-Assessment:**  
[ ] Reviewed concept map and quiz answers.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

**Deep Dive Appendix:**  
- Paths: Absolute vs relative.  
- Iterator fusion: Optimizes chains.  
- Property tests: Use proptest for fuzz (e.g., parse never panics).
