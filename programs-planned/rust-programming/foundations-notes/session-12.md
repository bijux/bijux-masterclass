# Session 12: Capstone Project, Concurrency, and Interop – Building Real-World Applications

**Target Audience & Scope:** This series assumes familiarity with C/Python, basic memory models (e.g., stack/heap, pointers/references, GC internals), and command-line tools. It targets programmers with systems or dynamic language experience new to Rust. Tone balances explanation for beginners in Rust but avoids over-simplifying semantics for intermediates.

**Prerequisites:** Sessions 1–9 concepts (ownership, borrowing, lifetimes, generics, traits, modules, iterators, smart pointers, concurrency/async basics); Task Manager v9 with generics, traits, modules, iterators, lifetimes, smart pointers, and basic concurrency/async.

**Conceptual Learning Goals:**  
- Integrate all prior concepts into a cohesive, non-trivial application.  
- Understand high-level concurrency patterns and trade-offs between threads and async.  
- Grasp interop fundamentals for bridging Rust with C/C++ or Python ecosystems.  

**Mechanical Learning Goals:**  
- Build and finalize a capstone project using a chosen option.  
- Use threads, channels, and async runtimes in practice.  
- Implement basic FFI with extern "C" and expose Rust to Python via PyO3.  
- Read and fix errors related to Send/Sync bounds, FFI types, or interop lifetimes.  

**Design Learning Goals:**  
- Design a modular, testable application with clear separation of concerns.  
- Choose concurrency models based on workload (CPU vs IO-bound).  
- Handle interop safely, managing ownership across language boundaries.  
- Reflect on Rust's impact compared to C/C++/Python.  

**By the End of This Session, You Can:**  
- Build and deploy a complete Rust application.  
- Apply concurrency and async in real scenarios.  
- Integrate safe interop with C and Python.  
- Profile and secure your code.  
- Reflect on design trade-offs.  
- Finalize the Task Manager or chosen capstone.  

**Project Narrative:** Finalize the Task Manager as a capstone, incorporating concurrency for parallel operations, async for IO, and interop for extensions (e.g., C plugin or Python binding). Choose one capstone option and extend with interop.

**Time Estimate:** 120 minutes (extended for capstone).

**Error Handling Policy:** Library returns task_core::Result<T> with typed thiserror errors. CLI uses anyhow + .context(). For interop, propagate via custom error types.

**Safety & Lints:**  
```rust
#![forbid(unsafe_code)]
#![deny(unused_must_use, missing_docs)]
// In CI via clippy:
// -D clippy::unwrap_used -D clippy::expect_used -D clippy::panic -D clippy::missing_errors_doc
```
Apply #![forbid(unsafe_code)] to all safe crates (core, stores, CLI). The FFI crate (task_ffi) is the single, documented unsafe boundary and intentionally does not use forbid(unsafe_code).

**MSRV Note:** Add rust-version = "1.65" to Cargo.toml and create rust-toolchain.toml with:  
```
[toolchain]
channel = "stable"
```

**Decision Framework: Concurrency vs Interop**  
- CPU-bound parallelism → Threads or rayon.  
- IO-bound concurrency → Async with tokio.  
- Data sharing → Arc<Mutex> for mut, Arc for immut. For read-dominated access patterns, prefer Arc<RwLock<T>> over Arc<Mutex<T>>.  
- Message passing → mpsc channels over shared state. For async code, prefer tokio::sync::mpsc; std::sync::mpsc blocks the executor.  
- tokio::spawn on multi-thread ⇒ future must be Send + 'static. Need non-Send? Use #[tokio::main(flavor="current_thread")] and spawn_local.  
- Interop: C FFI for performance-critical; PyO3 for Python integration.  

**Anti-Patterns to Avoid**  
- Spawning threads without join; use scoped threads.  
- Holding locks across await; redesign to drop guards early.  
- Non-Send types in threads; check bounds.  
- Busy-waiting; use condvars or channels.  
- Blocking in async; use spawn_blocking.  
- Exporting Rust structs over C ABI. (Use POD or opaque IDs.)  
- Exposing Arc<Mutex<_>>, channels, or executors in public APIs.  

**Public API Policy**  
- Expose async APIs as futures; use impl Future.  
- No raw threads in public; abstract with traits.  
- Document Send/Sync requirements.  
- Do not expose channels, mutex guards, or runtime types in public APIs; prefer impl Future<Output = T> and impl Stream<Item = T>. Return impl Stream<Item = T> via futures_core::Stream or tokio_stream (don’t expose tokio::sync::mpsc::Receiver<T>). If you need async in traits, use async-trait or return Pin<Box<dyn Future<Output = T> + Send + 'a>> (GATs allow nicer signatures on recent compilers). Prefer Pin<Box<dyn Future<Output = T> + Send + 'a>> for trait methods unless you standardize on GATs across the workspace, to keep MSRV=1.65 stable.
- Libraries: owned types; impl Future for async; thiserror errors.  

**Perf and Binary Size Guidance**  
- Threads: Overhead per thread; limit with pools.  
- Channels: Buffered for perf; unbounded risky.  
- Async: Futures are allocation-free state machines; the executor and IO driver add overhead. Throughput wins on IO-bound workloads; CPU-bound work should use threads or spawn_blocking. Bound async concurrency explicitly (e.g., semaphore) to avoid unbounded task fan-out.  
- Profile with tokio-console or flamegraph.  
- ThinLTO in release for size; avoid unbounded async fan-out.  

**Architecture Ideas (Capstone Integration)**  
- Add parallel query with rayon.  
- Async file store with tokio::fs.  
- Channels for task workers.  
- Shared state with Arc<Mutex<Store>>.  
- Architecture: Split into task_core (domain + traits), task_store_mem, task_store_fs, task_cli, optional task_ffi, task_py.  

**.cargo/config.toml Hardening (Workspace-Wide)**  
```toml
[target.'cfg(all())']
rustflags = ["-Dwarnings"]
rustdocflags = ["-Dwarnings", "-Drustdoc::broken_intra_doc_links"]
```

**Feature Flags (Gated, MSRV-Safe)**  
```toml
[features]
rayon = ["dep:rayon"]
async_rt = ["dep:tokio"]
concurrency = ["rayon","async_rt"]
ffi = []
py_bindings = ["dep:pyo3"]

[dependencies]
rayon = { version = "1", optional = true }
tokio = { version = "1", features = ["rt-multi-thread", "macros", "fs", "time"], optional = true }
pyo3 = { version = "0.20", optional = true }
```

**End-to-End Delta for Task Manager (Coherent, Compilable)**  
```rust
// task_core/src/query/parallel.rs (feature = "rayon")
#[cfg(feature = "rayon")]
use rayon::prelude::*;
#[derive(Clone, Copy, PartialEq, Eq)]
pub enum Status { Pending, Done }
#[derive(Clone)]
pub struct Task { pub id: u64, pub status: Status }
pub fn pending_ids_parallel(tasks: &[Task]) -> Vec<u64> {
    tasks
        .par_iter()
        .filter(|t| t.status == Status::Pending)
        .map(|t| t.id)
        .collect()
}

// task_store_fs/src/async_store.rs
#![cfg(feature = "async_rt")]

use std::path::Path;
use tokio::fs;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
pub struct Task { pub id: u64, pub title: String, pub done: bool }

pub type Result<T> = std::result::Result<T, std::io::Error>;

pub async fn load_tasks_json(path: &Path) -> Result<Vec<Task>> {
    let data = fs::read(path).await?;
    Ok(serde_json::from_slice(&data)?)
}

// task_ffi/src/lib.rs (feature = "ffi"; no forbid(unsafe_code))
use std::ffi::{c_char, CStr};
#[repr(C)]
#[derive(Copy, Clone)]
pub struct CTask { pub status: u8 }
/// Count tasks with status == Pending (0).
/// # Safety
/// - `tasks` must be non-null, properly aligned for CTask,
/// - points to `len` **initialized** elements,
/// - memory valid for the entire call (no aliasing UB).
/// - Each element must be a valid `CTask`.
#[no_mangle]
pub unsafe extern "C" fn tm_count_pending(tasks: *const CTask, len: usize) -> usize {
    if tasks.is_null() { return 0; }
    let slice = std::slice::from_raw_parts(tasks, len);
    slice.iter().filter(|t| t.status == 0).count()
}
/// Example: parse a C string and return its length (no Rust types exposed)
#[no_mangle]
pub unsafe extern "C" fn tm_strlen(s: *const c_char) -> usize {
    if s.is_null() { return 0; }
    CStr::from_ptr(s).to_bytes().len()
}

// task_py/src/lib.rs (feature = "py_bindings")
use pyo3::prelude::*;
#[pyclass]
struct PyTask {
    #[pyo3(get)]
    title: String,
    #[pyo3(get)]
    done: bool,
}
#[pymethods]
impl PyTask {
    #[new]
    fn new(title: String) -> Self { Self { title, done: false } }
    fn complete(&mut self) { self.done = true; }
}
#[pyfunction]
fn make_tasks(titles: Vec<String>) -> PyResult<Vec<PyTask>> {
    Ok(titles.into_iter().map(PyTask::new).collect())
}
#[pymodule]
fn task_py(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PyTask>()?;
    m.add_function(wrap_pyfunction!(make_tasks, m)?)?;
    Ok(())
}
```

---

## Setup Checklist

Verify and extend with capstone focus.

1. **Verify Existing Setup**  
   ```bash
   cargo --version
   rustc --version
   cargo fmt
   cargo clippy --workspace --all-targets -- -D warnings
   RUSTDOCFLAGS="-D warnings -D rustdoc::broken_intra_doc_links" cargo doc --workspace --no-deps
   cargo test --workspace --all-features
   ```
   Confirm rust-analyzer (hover for Send/Sync).

2. **Install Dependencies for Capstone**  
   ```bash
   cargo add serde --features derive
   cargo add serde_json
   cargo add rayon --optional
   cargo add tokio --features rt-multi-thread,macros,fs,time --optional
   cargo add pyo3 --optional
   cargo add criterion --dev
   cargo install flamegraph  # For profiling
   ```

3. **Set Up Capstone Workspace**  
   If not already, expand to include capstone-specific crates (e.g., task_ffi, task_py).

4. **Run Your Session 9 CLI**  
   ```bash
   cargo run
   ```
   Ensure concurrency/async works.

> **Lab – Try This:** Add a bench:  
> ```rust
> use criterion::{criterion_group, Criterion};
> fn bench_filter(c: &mut Criterion) { /* ... */ }
> ```  
> Run `cargo bench`.  
> **Solution:** Measures perf. Takeaway: Evidence claims.

**Debug the Error Mini-Lab (Retention Test from Session 9):** Spawn non-Send future. Predict error; fix with 'static or local_spawn.  
**Solution:** E0277; use Arc or redesign.

**Self-Assessment:**  
[ ] Verified setup and completed mini-lab.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

**Time Estimate:** 15 minutes.

---

## Part I: Capstone Options – Choosing and Structuring Your Project

**You Will Be Able To:**  
- Select and plan a capstone aligned with your goals.  
- Integrate prior concepts into a modular design.  
- Set up testing and CI for the project.

**Time Estimate:** 20 minutes.

### Core Concept: Case 1 – Capstone Planning and Modular Design

**Problem / Motivation:** Tie concepts into real app; avoid monolith.

**Definition (Formal):** Capstone: Integrated project using all tools.

**Mental Model (Simplified):** Build iteratively; test at boundaries.

**Example (Structure):** For Option A (CLI with persistence).  
```rust
// task_core/src/lib.rs
pub mod domain;
pub mod store;
pub mod query;

// task_cli/src/main.rs
use task_core::{domain::Task, store::FileStore};
fn main() -> anyhow::Result<()> {
    let mut store = FileStore::new("tasks.json")?;
    store.add(Task::new("Capstone"))?;
    Ok(())
}
```

**Code Triple:**  
**Rust (Modular, testable):**  
```rust
pub mod store;  // Clear boundaries
```  

**C/C++ (Headers, linking):**  
```cpp
#include "store.h"  // Manual includes
```  

**Python (Imports, dynamic):**  
```python
from store import FileStore  // Runtime resolution
```

**Analysis:**  
- Ownership impact: Borrow for queries.  
- Performance: Persist async.  
- Typical: Integration tests.

**Takeaway:** Modular for reuse.

> **Lab – Try This:** Sketch capstone modules.  
> **Solution:** Domain, store, CLI.

### Capstone Options (Choose 1)

1. **Option A: Advanced CLI Task Manager**  
   - Persistence: JSON via serde.  
   - Features: add/list/complete; indexed search by title/substring.  
   - Concurrency: parallel predicate search with rayon.  
   - Interop: export a C ABI function tm_count_pending (POD input).  
   - Python: minimal PyO3 PyTask + make_tasks.

2. **Option B: Simple HTTP Service**  
   - Use axum/warp (add dep).  
   - Endpoints: CRUD for tasks.  
   - Async: Tokio runtime.  
   - Interop: Call C lib.

3. **Option C: Data Processing Tool**  
   - Batch process CSV/JSON.  
   - Parallel: Rayon for transforms.  
   - Interop: Python binding for extension.

4. **Option D: Sandbox Simulation**  
   - Grid model with updates.  
   - Concurrency: Threads for workers.  
   - Interop: FFI for viz.

**Requirements for All:**  
- Modules + lib crate.  
- Generics/traits/errors.  
- Unit/integration tests.  
- Iterators/lifetimes/smart pointers.

**Reflection Prompt:** How does this change your C/C++/Python approach?

> **Lab – Try This:** Choose option; add serde.  
> **Solution:** cargo add serde.

**Part I Checkpoint:** Capstone for?  
**Answers:** Integration.

**You Can Now:**  
- Plan capstone.  
- Structure modular.

**Part I Quiz:** (5 MCQs + 1 open conceptual question)  
1. Capstone integrates? (a) All (b) Some (c) None  
   Answer: (a)  
2. True/False: Modules required.  
   Answer: True  
3. Serde for? (a) Persist (b) Concurrency (c) FFI  
   Answer: (a)  
4. Reflection on? (a) Rust vs others (b) Code (c) Perf  
   Answer: (a)  
5. True/False: Tests mandatory.  
   Answer: True  
Open Conceptual: Why modular?  
Answer: Reuse/testability.

**Self-Assessment:**  
[ ] Chose option; sketched.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part II: Deepening Concurrency – Threads, Channels, and Async in Practice

**You Will Be Able To:**  
- Apply threads and channels for safe parallelism.  
- Use async for IO in capstone.  
- Handle shared state securely.

**Time Estimate:** 25 minutes.

### Core Concept: Case 1 – Threaded Parallelism with Rayon

**Problem / Motivation:** CPU-bound tasks need parallelism without races.

**Definition (Formal):** Threads: OS-level; rayon for data-parallel.

**Mental Model (Simplified):** Par iter for easy parallel.

**Example (Compilable):** Parallel sum.  
```rust
use rayon::prelude::*;
fn par_sum(nums: &[i64]) -> i64 {
    nums.par_iter().sum()
}
```

**Code Triple:**  
**Rust (Safe parallel):**  
```rust
nums.par_iter().sum()
```  

**C/C++ (Manual threads):**  
```cpp
// pthread_create + join; manual sync
```  

**Python (Multiprocess):**  
```python
# multiprocessing.Pool; GIL bypass
```

**Rust Failure Variant:** Non-Send data.  
```rust
use std::rc::Rc;
let rc = Rc::new(1); std::thread::spawn(move || *rc);  // E0277
```

**Compiler Output (Key lines):**  
```
error[E0277]: `Rc<i32>` cannot be sent between threads safely
```

Error code: E0277.

**Analysis:**  
- Ownership impact: Clone for par.  
- Performance: Speedup.  
- Typical: Races prevented.

**Takeaway:** Rayon simplifies.

> **Lab – Try This:** Add par_filter to capstone.  
> **Solution:** Filter pending.

### Core Concept: Case 2 – Message Passing with Channels

**Problem / Motivation:** Communicate without shared mut.

**Definition (Formal):** mpsc: Multi-producer, single-consumer.

**Mental Model (Simplified):** Send/receive; owns data.

**Example (Compilable):** Worker channel.  
```rust
use std::sync::mpsc;
let (tx, rx) = mpsc::channel();
std::thread::spawn(move || tx.send(Task::new("work")).unwrap());
let task = rx.recv().unwrap();
```

**Code Triple:**  
**Rust (Owned send):**  
```rust
tx.send(task)
```  

**C/C++ (Queues, locks):**  
```cpp
// std::queue + mutex
```  

**Python (Queue):**  
```python
# multiprocessing.Queue
```

**Analysis:**  
- Ownership impact: Move to thread.  
- Performance: Buffered.  
- Typical: Deadlock if drop.

**Takeaway:** Prefer over locks.

> **Lab – Try This:** Channel for capstone workers.  
> **Solution:** Send results.

### Core Concept: Case 3 – Async in Capstone

**Problem / Motivation:** Non-blocking IO.

**Definition (Formal):** async/await with runtime.

**Mental Model (Simplified):** Await pauses; runtime polls.

**Example (Compilable):** Async load.  
```rust
use anyhow::Context;
#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let data = tokio::fs::read("tasks.json")
        .await
        .context("reading tasks.json")?;
    // parse or hand off to your store
    Ok(())
}
```

**Code Triple:**  
**Rust (Async await):**  
```rust
.read().await
```  

**C/C++ (Callbacks):**  
```cpp
// epoll + handlers
```  

**Python (asyncio):**  
```python
await asyncio.read
```

**Analysis:**  
- Ownership impact: 'static for spawn.  
- Performance: High throughput.  
- Typical: Poll ready.

**Takeaway:** For IO scale.

> **Lab – Try This:** Async persist in capstone.  
> **Solution:** Write await.

**Part II Checkpoint:** Concurrency for?  
**Answers:** Parallel/IO.

**You Can Now:**  
- Use threads/channels/async.

**Part II Quiz:** (5 MCQs + 1 open conceptual question)  
1. Rayon for? (a) IO (b) CPU (c) Both  
   Answer: (b)  
2. True/False: Channels move.  
   Answer: True  
3. Async runtime? (a) Std (b) Tokio (c) None  
   Answer: (b)  
4. Send bound? (a) Optional (b) Required (c) Auto  
   Answer: (b)  
5. True/False: Await blocks.  
   Answer: False  
Open Conceptual: Threads vs async.  
Answer: CPU vs IO.

**Self-Assessment:**  
[ ] Added concurrency to capstone.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part III: Interop – Bridging Rust with C and Python

**You Will Be Able To:**  
- Implement safe FFI with C.  
- Expose Rust to Python via PyO3.  
- Manage ownership across boundaries.

**Time Estimate:** 25 minutes.

### Core Concept: Case 1 – C FFI Basics

**Problem / Motivation:** Leverage existing C libs.

**Definition (Formal):** extern "C" for ABI compat.

**Mental Model (Simplified):** No_mangle; manage ptrs.

**Example (Compilable):** Export fn.  
```rust
#[no_mangle]
pub extern "C" fn rust_add(a: i32, b: i32) -> i32 {
    a + b
}
```

**Code Triple:**  
**Rust (Safe wrapper):**  
```rust
extern "C" { fn c_func(); }
```  

**C/C++ (Direct):**  
```cpp
extern "C" int rust_add(int, int);
```  

**Python (ctypes):**  
```python
# ctypes.CDLL
```

**Rust Failure Variant:** Unsafe ptr deref.  
```rust
unsafe { *ptr }  // If invalid, UB
```

**Compiler Output:** No compile error; runtime UB.

Error code: N/A (unsafe).

**Analysis:**  
- Ownership impact: Manual.  
- Performance: Zero overhead.  
- Typical: Ptr leaks.

**Takeaway:** Wrap unsafe.

> **Lab – Try This:** Export capstone fn to C.  
> **Solution:** Count tasks.

### Core Concept: Case 2 – Python Interop with PyO3

**Problem / Motivation:** Embed/extend Python.

**Definition (Formal):** PyO3 for bindings.

**Mental Model (Simplified):** Pyfn/pyclass; Gil-bound.

**Example (Compilable):** Py fn.  
```rust
use pyo3::prelude::*;
#[pyfunction]
fn py_add(a: i32, b: i32) -> PyResult<i32> {
    Ok(a + b)
}
#[pymodule]
fn my_mod(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(py_add, m)?)?;
    Ok(())
}
```

**Code Triple:**  
**Rust (Typed bindings):**  
```rust
#[pyfunction]
```  

**C/C++ (Py C API):**  
```cpp
// PyObject* manual
```  

**Python (Native):**  
```python
def add(a, b): return a + b
```

**Analysis:**  
- Ownership impact: PyRef.  
- Performance: Overhead.  
- Typical: Gil lock.

**Takeaway:** For integration.

> **Lab – Try This:** Add PyO3 to capstone.  
> **Solution:** Py add_task.

**Part III Checkpoint:** Interop for?  
**Answers:** Ecosystems.

**You Can Now:**  
- FFI with C/Python.

**Part III Quiz:** (5 MCQs + 1 open conceptual question)  
1. extern "C" for? (a) ABI (b) Syntax (c) Perf  
   Answer: (a)  
2. True/False: Unsafe required FFI.  
   Answer: True  
3. PyO3 for? (a) C (b) Python (c) Both  
   Answer: (b)  
4. No_mangle? (a) Optional (b) Required (c) Auto  
   Answer: (b)  
5. True/False: Ownership manual FFI.  
   Answer: True  
Open Conceptual: Trade-offs interop.  
Answer: Perf vs safety.

**Self-Assessment:**  
[ ] Added interop to capstone.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part IV: Performance, Security, and Reflection – Polishing and Assessing

**You Will Be Able To:**  
- Profile and benchmark your capstone.  
- Apply security best practices.  
- Reflect on Rust's paradigm shift.

**Time Estimate:** 20 minutes.

### Core Concept: Case 1 – Profiling with Flamegraph

**Problem / Motivation:** Identify hotspots.

**Definition (Formal):** Stack sampling.

**Mental Model (Simplified):** Visualize calls.

**Example (Command):**  
```bash
cargo flamegraph --bin task_cli
```

**Analysis:**  
- Ownership impact: None.  
- Performance: Overhead low.  
- Typical: IO bound.

**Takeaway:** Evidence perf.

> **Lab – Try This:** Profile capstone.  
> **Solution:** Flame SVG.

### Core Concept: Case 2 – Security with Clippy and Audits

**Problem / Motivation:** Prevent vulns.

**Definition (Formal):** Lints for safety.

**Mental Model (Simplified):** Automate checks.

**Example (Command):**  
```bash
cargo clippy -- -D clippy::missing_safety_doc
```

**Analysis:**  
- Ownership impact: Borrow checks.  
- Performance: N/A.  
- Typical: Unwrap in prod.

**Takeaway:** Clippy ally.

> **Lab – Try This:** Run clippy on capstone.  
> **Solution:** Fix warnings.

### Reflection and Self-Assessment

**Prompts:**  
- When is C the right call vs Rust FFI from Python?  
- Which boundaries do you keep dynamic (trait objects) vs generic (monomorphized)?  

**GitHub Push:** README, tests, CI, notes.

**Part IV Checkpoint:** Reflection for?  
**Answers:** Insights.

**You Can Now:**  
- Profile/secure.  
- Reflect.

**Part IV Quiz:** (5 MCQs + 1 open conceptual question)  
1. Flamegraph for? (a) Hotspots (b) Memory (c) Tests  
   Answer: (a)  
2. True/False: Clippy required.  
   Answer: False  
3. Reflection on? (a) Paradigms (b) Code (c) Perf  
   Answer: (a)  
4. CI for? (a) Lints/tests (b) Deploy (c) Both  
   Answer: (a)  
5. True/False: Push GitHub.  
   Answer: True  
Open Conceptual: Rust vs Python.  
Answer: Safety vs ease.

**Self-Assessment:**  
[ ] Profiled/reflected.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Exercises: Tiered Reasoning

### Tier 1: Concept Rebuilds

1. Thread Spawn  
   Simple worker.  
   **Solution:** spawn/join.

2. Async Fn  
   Await read.  
   **Solution:** tokio::fs.

### Tier 2: Comparative Rewrites

1. C Thread to Rust  
   Safe spawn.  
   **Solution:** No races.

2. Python Async to Rust  
   Await chain.  
   **Solution:** Typed.

### Tier 3: Challenge Extensions

1. FFI Wrapper  
   Safe around unsafe.  
   **Solution:** Check ptr.

2. PyO3 Class  
   Pyclass Task.  
   **Solution:** Impl methods.

**Self-Assessment:**  
[ ] Completed one per tier.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Recap and Synthesis Reflection

**Table Completion Exercise:**  
| Rust Feature | C/C++ Issue | Python Trade-off |
|--------------|-------------|------------------|
| Concurrency | Races/leaks | GIL/slow |
| Async | Callback hell | Await GIL |
| FFI | ABI mismatches | ctypes overhead |
| PyO3 | Manual API | Native speed |
| Capstone | Monolith | Dynamic mess |

**Self-Quiz:** (Design-level)  
1. Capstone purpose?  
2. Interop trade-offs?  
3. Reflection value?  
Answers:  
1. Integrate.  
2. Safety/perf.  
3. Insights.

**Final Takeaway:** Capstone ties; concurrency/interop extend; reflection solidifies.

**By Session End:**  
- Build/deploy app.  
- Apply concurrency/async.  
- Implement interop.  
- Profile/secure.  
- Reflect.  
- Finalize capstone.

**Glossary Appendix Update:** Add: Capstone, FFI, PyO3, Flamegraph.

**Error Code Index:**  
| Code   | Description                     | Example Case |
|--------|---------------------------------|--------------|
| E0277  | Bound not satisfied (Send/Sync) | Non-Send spawn |
| E0373  | Closure outlives                | Borrow thread |
| E0728  | Await outside async             | No async fn |
| E0308  | Mismatched types                | FFI ABI |

**Primary References:** Rust Book Ch. 20 (Web Server), Ch. 16 (Concurrency), Nomicon (FFI). PyO3 docs.

**Suggested Deep Dives:** Axum for services; cbindgen for headers.

**Concept Map:** (Text-based ASCII)  
Capstone (integrate all)  
  ├── Concurrency (threads/channels)  
  └── Async (tokio/await)  
Interop (FFI/PyO3)  
  └── Perf/Security (bench/flamegraph/clippy)  
Reflection (paradigms)

**Self-Assessment:**  
[ ] Completed capstone/reflection.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

**Deep Dive Appendix:**  
- FFI ownership: IntoRaw/FromRaw.  
- PyO3 GIL: Py<PyAny>.  
- Bench vs profile: Micro vs whole.

**“Done Means Done” Checklist**  
- All crates pass fmt/clippy/doc/test gates.  
- Public API exposes only owned/domain types.  
- No async runtime types or locks in public signatures.  
- FFI layer documented with safety sections and either POD or opaque handles.  
- A minimal benchmark or flamegraph is committed as evidence.  
- One integration test proves end-to-end flow.

**Optional Niceties (only if time allows)**  
- cbindgen to generate .h for task_ffi.  
- maturin for Python wheels (but don’t let packaging overshadow correctness).  
- tokio-console for IO profiling (keep it out of public API).
