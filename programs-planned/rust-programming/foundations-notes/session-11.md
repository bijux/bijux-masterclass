# Session 11: Async – Non-Blocking Concurrency with Tokio

**Target Audience & Scope:** This series assumes familiarity with C/Python, basic memory models (e.g., stack/heap, pointers/references, GC internals), and command-line tools. It targets programmers with systems or dynamic language experience new to Rust. Tone balances explanation for beginners in Rust but avoids over-simplifying semantics for intermediates.

**Assumed background:** familiarity with modules/crates, iterators, and a multi-crate workspace; a simple CLI ‘Task Manager’ helps but is not required.

We pin the course toolchain to stable 1.91 (Edition 2024).

**Conceptual Learning Goals:**  
- Grasp async for non-blocking IO.  

**Mechanical Learning Goals:**  
- Set up async with tokio runtime; use async/await.  
- Read and fix errors related to async lifetimes.  

**Design Learning Goals:**  
- Extend the Task Manager with async IO (e.g., file load).  
- Choose async for IO-bound work.  
- Test concurrent code with barriers or channels.  

**By the End of This Session, You Can:**  
- Write async functions with tokio.  
- Design async APIs.  
- Fix async errors.  
- Extend CLI with async.  

**Project Narrative:** Introduce Tokio for async file IO.

**Error Handling Policy:** Library returns task_core::Result<T> with typed thiserror errors. CLI uses anyhow + .context().

**Safety & Lints:**  
```rust
#![forbid(unsafe_code)]
#![deny(unused_must_use, missing_docs)]
// In CI via clippy:
// -D clippy::unwrap_used -D clippy::expect_used -D clippy::panic -D clippy::missing_errors_doc
```

**Toolchain**  
This session compiles on the course-pinned toolchain: stable 1.91 (Edition 2024).

**.cargo/config.toml Hardening (Workspace-Wide)**  
```toml
[target.'cfg(all())']
rustflags = ["-Dwarnings"]
rustdocflags = ["-Dwarnings", "-Drustdoc::broken_intra_doc_links"]
```

**Feature Flags (Gated, MSRV-Safe)**  
```toml
[features]
async_rt = ["dep:tokio","dep:tokio-stream","dep:futures-core","dep:tokio-util","dep:tracing","dep:tracing-subscriber"]

[dependencies]
tokio = { version = "1", features = ["rt-multi-thread", "macros", "fs", "time"], optional = true }
tokio-stream = { version = "0.1", optional = true }
futures-core = { version = "0.3", optional = true }
tokio-util = { version = "0.7", features = ["sync"], optional = true }
tracing = { version = "0.1", optional = true }
tracing-subscriber = { version = "0.3", features = ["fmt"], optional = true }
```

**Decision Framework: Async**  
- IO-bound concurrency → Async with tokio.  
- Message passing → tokio::sync::mpsc channels over shared state. For async code, prefer tokio::sync::mpsc; std::sync::mpsc blocks the executor.  
- tokio::spawn on multi-thread ⇒ future must be Send + 'static. Need non-Send? Use #[tokio::main(flavor="current_thread")] and spawn_local.

**Anti-Patterns to Avoid**  
- Holding locks across await; redesign to drop guards early.  

**Public API Policy**  
- Expose async APIs as futures; use impl Future.  
- Document Send/Sync requirements.  
- Do not expose channels, mutex guards, or runtime types in public APIs; prefer impl Future<Output = T> and impl Stream<Item = T>. Return impl Stream<Item = T> via futures_core::Stream or tokio_stream (don’t expose tokio::sync::mpsc::Receiver<T>). If you need async in traits, use async-trait or return Pin<Box<dyn Future<Output = T> + Send + 'a>> (GATs allow nicer signatures on recent compilers). Public APIs must not expose thread handles, channel endpoints, mutex guards, or Tokio types. Return owned data, impl Future<Output=T> + Send, or impl Stream<Item=T> + Send.

**Perf and Binary Size Guidance**  
- Async: Futures are allocation-free state machines; the executor and IO driver add overhead. Throughput wins on IO-bound workloads; CPU-bound work should use spawn_blocking. Bound async concurrency explicitly (e.g., semaphore) to avoid unbounded task fan-out.  

**Architecture Ideas (Optional)**  
- Async file store with tokio::fs.  

**End-to-End Delta for Task Manager (Coherent, Compilable)**  
```rust
// task_store_fs/src/lib.rs
use std::path::Path;

pub struct FsStore { /* ... */ }

impl FsStore {
    pub async fn load_async(path: &Path) -> std::io::Result<Self> {
        let buf = tokio::fs::read_to_string(path).await?;
        // parse...
        Ok(Self { /* ... */ })
    }
}
```

```rust
// task_cli/src/main.rs (sync CLI boundary, hiding async)
#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let store = FsStore::load_async("tasks.json").await?;
    // ...
    Ok(())
}
```

**Runtime Ownership Policy**  
Libraries must not start a runtime. Only binaries own #[tokio::main]. Library APIs should be generic over an existing runtime.  

---

## Setup Checklist

Verify and extend with focus on async.

1. **Verify Existing Setup**  
   ```bash
   cargo --version
   rustc --version
   cargo fmt
   cargo clippy -- -D warnings
   cargo test
   cargo test --doc
   ```
   Expect recent versions; update with `rustup update`. Confirm rust-analyzer (hover for bounds).

2. **Add Dependencies for Async**  
   ```bash
   cargo add tokio --features=rt-multi-thread,macros,fs,time --optional
   cargo add tokio-stream --optional
   cargo add futures-core --optional
   cargo add tokio-util --features=sync --optional
   cargo add tracing --optional
   cargo add tracing-subscriber --features=fmt --optional
   ```

3. **Optional: Tokio Console for Profiling**  
   ```bash
   cargo install tokio-console
   ```

4. **Run your CLI**  
   ```bash
   cargo run
   ```
   Ensure Task Manager works.

> **Lab – Try This:** Run `cargo check --features async_rt`. Note new bounds.  
> **Solution:** Reveals Send needs. Takeaway: Feature gates.  

**Debug the Error Mini-Lab (Retention Test):** Modify to await outside async; predict error; fix with async fn.  
**Solution:** E0728; wrap in async.

**Self-Assessment:**  
[ ] Verified setup and completed mini-lab.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part I: Async – Non-Blocking Concurrency

**You Will Be Able To:**  
- Write async fn.  
- Use tokio runtime.  
- Await futures.  

### Core Concept: Case 1 – Async Basics with Tokio

**Problem / Motivation:** IO wait; blocking vs non.

**Definition (Formal):** Async: Cooperative multitask.

**Mental Model (Simplified):** Await yields.

**Example (Compilable):** Async.  
```rust
use tokio::fs::read_to_string;
async fn load() -> std::io::Result<String> {
    read_to_string("file.txt").await
}
```

**Code Triple:**  
**Rust (Async):**  
```rust
async fn { .await }
```  

**C/C++ (Coroutines):**  
```cpp
co_await read();
```  

**Python (Async):**  
```python
async def: await
```

**Rust Failure Variant:** No runtime.  
```rust
load().await // E0728
fn main() {}
```

**Compiler Output:** E0728 (await outside async).

**Analysis:**  
- Ownership impact: Future owns.  
- Performance: Non-block.  
- Typical: E0728.

**Takeaway:** IO concurrent.

> **Lab – Try This:** Async file.  
> **Solution:** .await

### Core Concept: Case 2 – Tokio Runtime and Tasks

**Problem / Motivation:** Run async.

**Definition (Formal):** Runtime: Schedule tasks.

**Mental Model (Simplified):** Executor.

**Example (Compilable):** Runtime.  
```rust
#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let s = tokio::fs::read_to_string("file.txt").await?;
    println!("{s}");
    Ok(())
}
```

**Code Triple:**  
**Rust (Runtime):**  
```rust
#[tokio::main]
```  

**C/C++ (Asio):**  
```cpp
io_context.run();
```  

**Python (Loop):**  
```python
asyncio.run()
```

**Analysis:**  
- Ownership impact: Block main.  
- Performance: Multi-task.  
- Typical: No error.

**Note:** tokio::spawn (multi-thread runtime) requires the spawned future to be Send + 'static. If you must spawn a non-Send future, use current-thread runtime and tokio::task::spawn_local. LocalSet provides an executor for !Send futures. spawn_local tasks never hop threads; do not mix Rc with tokio::spawn on multi-thread runtimes.

```rust
// Non-Send type (e.g., Rc) on multi-thread runtime ⇒ use spawn_local
#[tokio::main(flavor = "current_thread")]
async fn main() {
    use std::rc::Rc;
    let x = Rc::new(1);

    tokio::task::LocalSet::new()
        .run_until(async move {
            tokio::task::spawn_local(async move {
                let _ = *x; // OK: non-Send, stays on this thread
            }).await;
        })
        .await;
}
```

**Takeaway:** Run async.

> **Lab – Try This:** Block on async.  
> **Solution:** #[tokio::main]

**Part I Checkpoint:** Async for?  
**Answers:** IO.

**You Can Now:**  
- Write async.

**Part I Quiz:** (5 MCQs + 1 open conceptual question)  
1. Await does? (a) Block (b) Yield (c) Join  
   Answer: (b)  
2. True/False: Async threads.  
   Answer: False  
3. Runtime for? (a) Schedule (b) Spawn (c) Channel  
   Answer: (a)  
4. Block_on? (a) Async (b) Sync (c) Both  
   Answer: (b)  
5. True/False: Futures Send.  
   Answer: False  
Open Conceptual: Explain async vs threads.  
Answer: IO vs CPU.

**Self-Assessment:**  
[ ] Wrote async.  
[ ] Used runtime.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part II: Application and Advanced

**You Will Be Able To:**  
- Apply async in project.  
- Test concurrent.  
- Profile perf.  

**Do Not Do This**  
- Avoid std::fs, std::net, std::process, and std::thread::sleep() inside async contexts. Use tokio::fs, tokio::net, tokio::process, and tokio::time::sleep() (or spawn_blocking for CPU).  

**Cancellation-Safety Policy**  
Any .await is a cancellation point. Keep invariants valid on drop. Commit mutations before .await, or use small transaction structs. I/O in Tokio is cancellation-safe; your state updates must be too.  

### Core Concept: Holding Locks Across Await

**Problem / Motivation:** Lock await.

**Definition (Formal):** Drop guard early.

**Mental Model (Simplified):** Scope guard.

**Example (Compilable):** Fix lock.  
```rust
let m = tokio::sync::Mutex::new(vec![]);
// BAD: guard held across .await
let mut g = m.lock().await;
g.push(1);
do_async().await; // wrong; guard is still held here

// GOOD: limit scope
{
    let mut g = m.lock().await;
    g.push(1);
} // guard dropped
do_async().await;
```

**Code Triple:**  
**Rust (Scope guard):**  
```rust
{ let g = lock(); ... }
```  

**C/C++ (Guard):**  
```cpp
{ std::lock_guard g(m); ... }
```  

**Python (With):**  
```python
with lock: ...
```

**Analysis:**  
- Ownership impact: Drop early.  
- Performance: No contention.  
- Typical: No error.

**Takeaway:** Drop guards early.

> **Lab: Lock-across-await Slowdown → Fix**  
> Count ops/sec with and without scoping the guard (small loop with tokio::time::Instant).

This applies equally to std::sync::Mutex used via spawn_blocking; never hold a blocking lock during .await. If you must protect data across awaits, prefer tokio::sync::Mutex over std::sync::Mutex; never hold a std::sync::MutexGuard across an .await.

RwLock caveat: RwLock can starve writers under load; prefer Mutex or sharded state. If heavy read sharing is required, consider dashmap (feature-gated, optional) with clear guidance about contention and shard count.

### Core Concept: Bounded Fan-Out with Semaphore

**Problem / Motivation:** Fan-out control.

**Definition (Formal):** Semaphore limit.

**Mental Model (Simplified):** Permit pool.

**Example (Compilable):** Fan-out.  
```rust
use std::{path::PathBuf, sync::Arc};
use tokio::{sync::Semaphore, task::JoinSet};

async fn load_many(paths: Vec<PathBuf>, limit: usize) -> anyhow::Result<Vec<String>> {
    let sem = Arc::new(Semaphore::new(limit));
    let mut set = JoinSet::new();
    for p in paths {
        let permit = sem.clone().acquire_owned().await?;
        set.spawn(async move {
            let _permit = permit;
            tokio::fs::read_to_string(p).await
        });
    }
    let mut out = Vec::new();
    while let Some(res) = set.join_next().await {
        let v: String = res.map_err(|e| anyhow::anyhow!("join error: {e}"))??;
        out.push(v);
    }
    Ok(out)
}
```

**Analysis:**  
- Ownership impact: Permit drop.  
- Performance: Bound.  
- Typical: No error.

**Takeaway:** Control concurrency.

> **Lab: Bounded Fan-Out**  
> Bounded fan-out with Semaphore. Show capping concurrency while reading many files.

### Core Concept: Cancellation & Timeouts

**Problem / Motivation:** Long async.

**Definition (Formal):** Timeout future.

**Mental Model (Simplified):** Race timeout.

**Example (Compilable):** Timeout.  
```rust
use std::time::Duration;
use tokio::time::timeout;
let res = timeout(Duration::from_secs(2), do_work()).await;
```

**Code Triple:**  
**Rust (Timeout):**  
```rust
timeout(dur, future)
```  

**C/C++ (Select):**  
```cpp
select timeout
```  

**Python (Asyncio):**  
```python
asyncio.wait_for(fut, timeout)
```

**Analysis:**  
- Ownership impact: Drop future.  
- Performance: None.  
- Typical: Err timeout.

**Takeaway:** Bound time. A timeout cancels by dropping the inner future; no implicit cancellation of child tasks: timing out a parent future drops it; spawned tasks keep running unless you hold their JoinHandle and cancel or use a CancellationToken.

> **Lab – Try This:** Timeout async.  
> **Solution:** timeout

### Core Concept: Join Handles & Error Surfacing

**Problem / Motivation:** Await multiple.

**Definition (Formal):** Join handle.

**Mental Model (Simplified):** Wait task.

**Example (Compilable):** Join.  
```rust
let h = tokio::spawn(async { do_io().await });
let out = h.await??; // join error + inner Result
```

**Code Triple:**  
**Rust (Join):**  
```rust
handle.await
```  

**C/C++ (Future):**  
```cpp
future.get();
```  

**Python (Await):**  
```python
await task
```

**Analysis:**  
- Ownership impact: Wait.  
- Performance: Concurrent.  
- Typical: JoinError.

**Takeaway:** Error prop.

> **Lab – Try This:** Spawn await.  
> **Solution:** h.await?

This example assumes the enclosing function returns anyhow::Result<_>; otherwise, unwrap/handle JoinError explicitly.

### Core Concept: Select for Racing Tasks

**Problem / Motivation:** Multiple await.

**Definition (Formal):** Select branches.

**Mental Model (Simplified):** First complete.

**Example (Compilable):** Select.  
```rust
use tokio_util::sync::CancellationToken;

tokio::select! {
    r = task1() => { r?; }
    _ = shutdown.cancelled() => { /* graceful stop */ }
}
```

**Code Triple:**  
**Rust (Select):**  
```rust
tokio::select! {}
```  

**C/C++ (Poll):**  
```cpp
poll fds
```  

**Python (Await first):**  
```python
asyncio.wait(tasks, return_when=FIRST_COMPLETED)
```

**Analysis:**  
- Ownership impact: Cancel others.  
- Performance: Efficient.  
- Typical: No error.

**Takeaway:** Race tasks. tokio::select! is fair by default; use biased; to evaluate branches in order if you need bias.

> **Lab: Cancel Select**  
> Cancel via select!. Add a shutdown watch::Receiver or CancellationToken (from tokio-util) and demonstrate cancel + drain.

### Core Concept: Spawn Blocking for CPU in Async

**Problem / Motivation:** CPU in async.

**Definition (Formal):** Block in thread.

**Mental Model (Simplified):** Offload CPU.

**Example (Compilable):** Blocking.  
```rust
let sum = tokio::task::spawn_blocking(|| heavy_cpu()).await?;
```

**Code Triple:**  
**Rust (Blocking):**  
```rust
spawn_blocking(|| {})
```  

**C/C++ (Thread):**  
```cpp
std::thread t([] { heavy(); });
```  

**Python (Process):**  
```python
multiprocessing.Process(target=heavy).start()
```

**Analysis:**  
- Ownership impact: Move.  
- Performance: No starve.  
- Typical: No error.

**Takeaway:** CPU off async. The blocking pool expands but caps throughput; it is not a CPU pool. For sustained CPU, offload to Rayon and communicate via channels.

> **Lab – Try This:** Spawn blocking.  
> **Solution:** spawn_blocking

fn heavy_cpu() -> u64 { (0..10_000_000).sum() }

### Core Concept: Async Channels to Stream

**Problem / Motivation:** Stream channel.

**Definition (Formal):** Adapt receiver.

**Mental Model (Simplified):** Channel stream.

**Example (Compilable):** Stream.  
```rust
use tokio::sync::mpsc;
use tokio_stream::wrappers::ReceiverStream;
fn stream_of_items() -> impl futures_core::Stream<Item = u64> + Send {
    let (tx, rx) = mpsc::channel(32);
    tokio::spawn(async move {
        for i in 0..100 { let _ = tx.send(i).await; }
    });
    ReceiverStream::new(rx)
}
```

**Analysis:**  
- Ownership impact: Adapt.  
- Performance: Stream.  
- Typical: No error.

**Takeaway:** Adapt channel.

> **Lab – Try This:** Channel to stream.  
> **Solution:** ReceiverStream

### Core Concept: Observability with Tracing

**Problem / Motivation:** Trace async.

**Definition (Formal):** Span trace.

**Mental Model (Simplified):** Log span.

**Example (Compilable):** Tracing.  
```rust
#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt().with_target(false).json().init();
    // ...
    Ok(())
}
```

**Analysis:**  
- Ownership impact: None.  
- Performance: Low.  
- Typical: No error.

**Takeaway:** Trace spans.

> **Lab – Try This:** Init tracing.  
> **Solution:** tracing_subscriber

**Part II Checkpoint:** Select for?  
**Answers:** Race.

**You Can Now:**  
- Apply in project.

**Part II Quiz:** (5 MCQs + 1 open conceptual question)  
1. Select for? (a) Race (b) Join (c) Lock  
   Answer: (a)  
2. True/False: Timeout drop.  
   Answer: True  
3. JoinError? (a) Panic (b) Cancel (c) Both  
   Answer: (c)  
4. Lock across await? (a) Ok (b) Bad (c) Panic  
   Answer: (b)  
5. True/False: Spawn local Send.  
   Answer: False  
Open Conceptual: Explain cancellation.  
Answer: Drop future.

**Self-Assessment:**  
[ ] Applied async.  
[ ] Tested.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Exercises: Tiered Reasoning

### Tier 1: Concept Rebuilds

1. Async Fn  
   Await IO.  
   **Solution:** async/await

### Tier 2: Comparative Rewrites

1. Python Await to Rust  
   Async.  
   **Solution:** .await

### Tier 3: Challenge Extensions

1. Bounded Fan-Out  
   Semaphore.  
   **Solution:** Semaphore + JoinSet

**Self-Assessment:**  
[ ] Completed one per tier.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Recap and Synthesis Reflection

**Table Completion Exercise:**  
| Rust Feature | C/C++ Issue | Python Trade-off |
|--------------|-------------|------------------|
| Async | Manual polling/epoll complexity without unified safety model. | Await GIL |

**Self-Quiz:** (Design-level)  
1. Async for?  
Answers:  
1. IO.

**Final Takeaway:** Async safe multi-task.

**Glossary Appendix Update:** Add: Async, Future, Runtime.

**Error Code Index:**  
| Code   | Description                     | Example Case |
|--------|---------------------------------|--------------|
| E0728  | Await outside async             | No async fn |
| E0759 | async block may outlive borrowed value | Holding a reference captured into tokio::spawn without 'static |

**Primary References:** Rust Book Ch. 20 (Async).

**Suggested Deep Dives:** Tokio docs.

**Concept Map:** (Text-based ASCII)  
Async (await)  
  └── Runtime (tokio)  
Applied (Task example)

**Self-Assessment:**  
[ ] Reviewed map/quiz.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

**Deep Dive Appendix:**  
- Future poll: Async mech.  
- Tokio tasks: Spawn async.

**“Done Means Done” Checklist**  
- Architecture: Async integrated.  
- API: No raw async; abstract traits.  
- Quality: Clippy/docs pass.  
- Tests: Async tests.  
- Perf: Profile contention.

**Compile-Fail Mini-Labs (Retention + Rigor)**  
1. Await Outside Async (E0728)  
   ```rust,compile_fail
   fn main() {
       let _ = tokio::fs::read_to_string("x").await; // E0728
   }
   ```  
2. Non-Send Future in Spawn (E0277)  
   ```rust,compile_fail
   use std::rc::Rc;
   #[tokio::main(flavor = "multi_thread")] async fn main() {
       let x = Rc::new(1);
       tokio::spawn(async move { let _ = *x; }); // E0277
   }
   ```  
3. Non-'static Capture in Spawn (E0759)  
   ```rust,compile_fail
   #[tokio::main(flavor = "multi_thread")]
   async fn main() {
       let s = String::from("x");
       let r = &s; // borrowed
       tokio::spawn(async move { println!("{}", r); }); // E0759
   }
   ```  

Automate with trybuild in task_core/tests/compile_fail/.
Place files under task_core/tests/compile_fail/*.rs and use trybuild = "1" in dev-dependencies.

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
use task_core::internal::ConcurrencyType; // Should not be publicly reachable
fn main() {}
```

**Testing Guidance for Async Code**  
```rust
#[tokio::test(start_paused = true)]
async fn async_works() -> std::io::Result<()> {
    let s = tokio::fs::read_to_string("Cargo.toml").await?;
    assert!(s.contains("[package]"));
    Ok(())
}
```
