# Session 10: Concurrency – Threads & Channels

**Target Audience & Scope:** This series assumes familiarity with C/Python, basic memory models (e.g., stack/heap, pointers/references, GC internals), and command-line tools. It targets programmers with systems or dynamic language experience new to Rust. Tone balances explanation for beginners in Rust but avoids over-simplifying semantics for intermediates.

**Assumed background:** familiarity with modules/crates, iterators, and a multi-crate workspace; a simple CLI ‘Task Manager’ helps but is not required.

We pin the course toolchain to stable 1.91 (Edition 2024).

**Conceptual Learning Goals:**  
- Understand threads for parallelism and channels for safe communication.  
- Grasp Send/Sync traits for thread safety.  

**Mechanical Learning Goals:**  
- Spawn threads with std::thread::spawn and join handles.  
- Use crossbeam channels for message passing.  
- Read and fix errors related to non-Send types.  

**Design Learning Goals:**  
- Extend the Task Manager with parallel queries.  
- Choose threads for CPU-bound work.  
- Test concurrent code with barriers or channels.  

**By the End of This Session, You Can:**  
- Spawn and join threads safely.  
- Send messages via channels.  
- Design parallel APIs.  
- Fix Send/Sync errors.  
- Extend CLI with concurrency.  

**Project Narrative:** Introduce threads/channels for CPU pipelines; share state with Arc<Mutex<T>> when needed.

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
concurrency = ["dep:crossbeam-channel","dep:rayon"]

[dependencies]
crossbeam-channel = { version = "0.5", optional = true }
rayon = { version = "1", optional = true }
```

**Decision Framework: Threads vs Shared State vs Message Passing**  
- CPU-bound parallelism → threads or rayon; prefer rayon for data-parallel loops.  
- Data sharing → Arc<Mutex> for mut, Arc for immut.  
- Message passing → crossbeam channels over shared state.  

**Anti-Patterns to Avoid**  
- Spawning threads without join; use scoped threads.  
- Non-Send types in threads; check bounds.  
- Busy-waiting; use condvars or channels.  

**Public API Policy**  
- No raw threads in public; abstract with traits.  
- Document Send/Sync requirements.  
- Public APIs must not expose thread handles, channel endpoints, or mutex guards. Return owned data or trait abstractions (e.g., a worker trait or callback).

**Perf and Binary Size Guidance**  
- Threads: Overhead per thread; limit with pools.  
- Channels: Buffered for perf; unbounded risky.  
- Profile with flamegraph if sharing impacts perf.

**Architecture Ideas (Optional)**  
- Add parallel query with rayon.  
- Channels for task workers.  
- Shared state with Arc<Mutex<Store>>.

**End-to-End Delta for Task Manager (Coherent, Compilable)**  
```rust
// task_core/src/query/parallel.rs
pub struct Task { pub id: u64 }

pub fn sum_ids_parallel(tasks: &[Task]) -> u64 {
    #[cfg(feature = "concurrency")]
    {
        use rayon::prelude::*;
        tasks.par_iter().map(|t| t.id).sum()
    }
    #[cfg(not(feature = "concurrency"))]
    {
        tasks.iter().map(|t| t.id).sum()
    }
}
```

```rust
// task_cli/src/main.rs (sync CLI boundary, hiding concurrency)
use crossbeam_channel::{bounded, Sender};
fn spawn_worker(tx: Sender<u64>) {
    std::thread::spawn(move || {
        std::thread::sleep(std::time::Duration::from_secs(1)); // simulate work
        let v = compute();
        tx.send(v).ok();
    });
}

fn compute() -> u64 { 42 }
```

**Mutex vs RwLock**  
- Mutex<T>: write-heavy, small CS. Mutex<T>: Send if T: Send; &Mutex<T>: Sync if T: Send.  
- RwLock<T>: read-heavy, large CS; T: Send and T: Sync requirements clarified. RwLock<T>: Send if T: Send; &RwLock<T>: Sync if T: Send + Sync.  

---

## Setup Checklist

Verify and extend with focus on concurrency.

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

2. **Add Dependencies for Concurrency**  
   ```bash
   cargo add crossbeam-channel --optional
   cargo add rayon --optional
   ```

3. **Run your CLI**  
   ```bash
   cargo run
   ```
   Ensure Task Manager works.

> **Lab – Try This:** Run `cargo check --features concurrency`. Note new bounds.  
> **Solution:** Reveals Send/Sync needs. Takeaway: Feature gates.  

**Debug the Error Mini-Lab (Retention Test):** Modify Rc to thread; predict error; fix with Arc.  
**Solution:** E0277; use Arc.

**Self-Assessment:**  
[ ] Verified setup and completed mini-lab.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part I: Threads – Parallel Execution with Safety

**You Will Be Able To:**  
- Spawn/join threads.  
- Share data with Arc.  
- Contrast with C/Python threads.  

### Core Concept: Case 1 – Spawning and Joining Threads

**Problem / Motivation:** Parallel CPU work; C races; Python GIL.

**Definition (Formal):** Thread: OS execution unit.

**Mental Model (Simplified):** Fork-join model.

**Example (Compilable):** Spawn.  
```rust
use std::thread;
let handle = thread::spawn(|| { 42 });
let result = handle.join().unwrap();
```

**Code Triple:**  
**Rust (Spawn):**  
```rust
thread::spawn(|| {})
```  

**C/C++ (Thread):**  
```cpp
std::thread t([] { return 42; }); t.join();
```  

**Python (Thread):**  
```python
threading.Thread(target=fn).start()
```

**Rust Failure Variant:** Non-Send.  
```rust
use std::rc::Rc;
let rc = Rc::new(42);
thread::spawn(move || drop(rc));
fn main() {}
```

**Compiler Output:** E0277 (not Send).

**Analysis:**  
- Ownership impact: Move to thread.  
- Performance: OS overhead.  
- Typical: E0277.

**Takeaway:** Safe parallelism.

> **Lab – Try This:** Spawn compute.  
> **Solution:** thread::spawn

### Core Concept: Case 2 – Scoped Threads

**Problem / Motivation:** Borrow in threads.

**Definition (Formal):** Scoped: Borrow from parent.

**Mental Model (Simplified):** No move needed.

**Example (Compilable):** Scoped.  
```rust
use std::thread::scope;
let data = vec![1,2,3];
thread::scope(|s| {
    s.spawn(|| {
        // can read `data` by borrow; no 'static required
        assert_eq!(data.len(), 3);
    });
});
```

**Code Triple:**  
**Rust (Scope):**  
```rust
thread::scope(|s| s.spawn(|| {}))
```  

**C/C++ (No):**  
```cpp
// manual join
```  

**Python (No):**  
```python
# context managers approximate
```

**Rust Failure Variant:** Outlive.  
```rust
fn main() {
    let local = 42;
    // closure must be 'static; borrowed `local` cannot outlive main
    std::thread::spawn(|| { let _ = &local; }); // E0373
}
```

**Compiler Output:** E0373 (closure may outlive).

**Analysis:**  
- Ownership impact: Borrow ok.  
- Performance: No clone.  
- Typical: E0373.

**Takeaway:** Scoped borrow.

> **Lab – Try This:** Scoped borrow.  
> **Solution:** thread::scope

**Part I Checkpoint:** Threads for?  
**Answers:** Parallelism.

**You Can Now:**  
- Spawn/join threads.

**Part I Quiz:** (5 MCQs + 1 open conceptual question)  
1. Spawn returns? (a) JoinHandle (b) Thread (c) Result  
   Answer: (a)  
2. True/False: Rc Send.  
   Answer: False  
3. E0277 cause? (a) Not Send (b) Lifetime (c) Move  
   Answer: (a)  
4. Scoped for? (a) Borrow (b) Move (c) Async  
   Answer: (a)  
5. True/False: GIL in Rust.  
   Answer: False  
Open Conceptual: Explain Send/Sync.  
Answer: Cross-thread safe.

**Self-Assessment:**  
[ ] Spawned threads.  
[ ] Fixed E0277.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part II: Message Passing – Safe Communication

**You Will Be Able To:**  
- Use crossbeam channels.  
- Send/recv messages.  
- Contrast with C/Python queues.  

### Core Concept: Case 1 – Crossbeam Channels

**Problem / Motivation:** Data transfer without share.

**Definition (Formal):** Mpsc: Multi-producer single-consumer.

**Mental Model (Simplified):** Safe pipe.

**Example (Compilable):** Channel.  
```rust
use crossbeam_channel::bounded;
let (tx, rx) = bounded(1);
tx.send(42).unwrap();
let msg = rx.recv().unwrap();
```

**Code Triple:**  
**Rust (Channel):**  
```rust
bounded(1)
```  

**C/C++ (Queue):**  
```cpp
std::queue<int> q; // manual lock
```  

**Python (Queue):**  
```python
queue.Queue()
```

**Rust Failure Variant:** Closed.  
```rust
drop(tx); rx.recv() // Err
fn main() {}
```

**Compiler Output:** None; RecvError.

**Analysis:**  
- Ownership impact: Send moves.  
- Performance: Buffered.  
- Typical: RecvError.

**Takeaway:** Message safe.

> **Lab: Bounded Backpressure (Measured)**  
> Show bounded(1) vs bounded(1024) throughput; capture elapsed with Instant. This makes capacity effects concrete.

**Note:** crossbeam_channel::{Sender, Receiver} are Send + Sync iff T: Send. Clone a Sender per producer; keep one Receiver on the consumer.

**Part II Checkpoint:** Channels for?  
**Answers:** Communication.

**You Can Now:**  
- Use channels.

**Part II Quiz:** (5 MCQs + 1 open conceptual question)  
1. Mpsc means? (a) Multi send (b) Multi prod (c) Single send  
   Answer: (b)  
2. True/False: Send borrows.  
   Answer: False  
3. Recv err? (a) Closed (b) Timeout (c) Both  
   Answer: (a)  
4. Bounded channel? (a) bounded (b) Async (c) Mpsc  
   Answer: (a)  
5. True/False: Channels Sync.  
   Answer: True  
Open Conceptual: Explain message vs share.  
Answer: No race.

**Self-Assessment:**  
[ ] Used channels.  
[ ] Handled err.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part III: Application and Advanced

**You Will Be Able To:**  
- Apply concurrency in project.  
- Test concurrent.  
- Profile perf.  

### Core Concept: Deadlock Demo and Fix

**Problem / Motivation:** Race hard to test.

**Definition (Formal):** Deadlock: Cyclic wait.

**Mental Model (Simplified):** Lock order.

**Example (Compilable):** Fix deadlock.  
```rust
use std::sync::{Arc, Mutex};
let m1 = Arc::new(Mutex::new(1));
let m2 = Arc::new(Mutex::new(2));
// Inverted order in one thread causes deadlock
let h1 = std::thread::spawn({ let m1 = m1.clone(); let m2 = m2.clone(); move || {
    let _g1 = m1.lock().unwrap();
    let _g2 = m2.lock().unwrap();
}});
let _g2 = m2.lock().unwrap();
let _g1 = m1.lock().unwrap(); // deadlock

// Fix: consistent order or message passing
```

**Analysis:**  
- Ownership impact: Guard.  
- Performance: Block.  
- Typical: Hang.

**Takeaway:** Order locks. Use consistent lock ordering or message passing to eliminate cycles.

> **Lab: Deadlock → Fix**  
> Two Mutexes with inverted lock order; fix by ordering or message passing. Add a test using Barrier to make the deadlock deterministic, then fix.

### Core Concept: Testing Concurrent Code

**Problem / Motivation:** Race hard to test.

**Definition (Formal):** Barrier/channel test.

**Mental Model (Simplified):** Sync points.

**Example (Compilable):** Test.  
```rust
use std::{sync::{Arc, Barrier}, thread};
#[test]
fn concurrent() {
    let barrier = Arc::new(Barrier::new(2));
    let t1 = thread::spawn({ let b = barrier.clone(); move || b.wait() });
    barrier.wait();
    t1.join().unwrap();
}
```

**Code Triple:**  
**Rust (Barrier):**  
```rust
Barrier::new(n)
```  

**C/C++ (Barrier):**  
```cpp
std::barrier b(2);
```  

**Python (Barrier):**  
```python
threading.Barrier(2)
```

**Analysis:**  
- Ownership impact: Arc share.  
- Performance: Sync.  
- Typical: No error.

**Takeaway:** Deterministic test.

> **Lab – Try This:** Test race.  
> **Solution:** Barrier sync.

### Core Concept: Rayon for Parallel Iterators

**Problem / Motivation:** Easy parallel.

**Definition (Formal):** Rayon: Data parallel.

**Mental Model (Simplified):** Par iter.

**Example (Compilable):** Rayon.  
```rust
use rayon::prelude::*;
// owns the range => into_par_iter(); use par_bridge() for borrowed iterators from a store.
let sum = (1..10).into_par_iter().sum::<i32>();
```

**Code Triple:**  
**Rust (Par):**  
```rust
into_par_iter()
```  

**C/C++ (OpenMP):**  
```cpp
#pragma omp parallel for
```  

**Python (Multiprocess):**  
```python
multiprocessing.Pool().map
```

**Analysis:**  
- Ownership impact: Send.  
- Performance: Parallel.  
- Typical: No error.

**Takeaway:** Easy parallel. Prefer rayon for data-parallel loops; manual threads are didactic.

> **Lab – Try This:** Par sum.  
> **Solution:** into_par_iter().sum()

### Core Concept: Join Error Handling & Panic Propagation

**Problem / Motivation:** Error in thread.

**Definition (Formal):** Join error.

**Mental Model (Simplified):** Propagate panic.

**Example (Compilable):** Join err.  
```rust
let h = std::thread::spawn(|| panic!("boom"));
match h.join() {
    Err(e) => eprintln!("thread panicked: {:?}", e), // join error
    Ok(_) => {}
}
```

**Analysis:**  
- Ownership impact: Join.  
- Performance: None.  
- Typical: JoinError.

**Takeaway:** Propagate. Never .unwrap() joins in libraries; surface them.

> **Lab – Try This:** Handle join err.  
> **Solution:** match h.join()

### Core Concept: Crossbeam Select

**Problem / Motivation:** Race channels.

**Definition (Formal):** Select recv.

**Mental Model (Simplified):** First ready.

**Example (Compilable):** Select.  
```rust
use crossbeam_channel::{bounded, select};
let (tx1, rx1) = bounded::<u32>(0);
let (tx2, rx2) = bounded::<u32>(0);
std::thread::spawn(move || tx1.send(1).ok());
std::thread::spawn(move || tx2.send(2).ok());
select! {
    recv(rx1) -> v => { /* ... */ }
    recv(rx2) -> v => { /* ... */ }
}
```

**Analysis:**  
- Ownership impact: None.  
- Performance: Efficient.  
- Typical: No error.

**Takeaway:** Race channels.

> **Lab: Cancel Select**  
> Select with cancellation. Add a stop channel to model shutdown.

### Core Concept: Atomics vs Mutex

**Problem / Motivation:** Simple sync.

**Definition (Formal):** Atomic ops.

**Mental Model (Simplified):** No lock.

**Example (Compilable):** Atomic.  
```rust
use std::sync::Arc;
use std::sync::atomic::{AtomicU64, Ordering};
let counter = Arc::new(AtomicU64::new(0));
let c = counter.clone();
std::thread::spawn(move || c.fetch_add(1, Ordering::SeqCst));
counter.load(Ordering::SeqCst);
```

**Analysis:**  
- Ownership impact: Arc.  
- Performance: Fast.  
- Typical: No error.

**Takeaway:** Counters → AtomicU64 (fetch_add) if you only need arithmetic; otherwise Mutex for compound invariants. Use Ordering::SeqCst unless you can prove weaker orderings are correct end-to-end.

> **Lab – Try This:** Atomic counter.  
> **Solution:** fetch_add

### Core Concept: Thread Naming

**Problem / Motivation:** Debug threads.

**Definition (Formal):** Builder name.

**Mental Model (Simplified):** Label thread.

**Example (Compilable):** Naming.  
```rust
let h = std::thread::Builder::new()
    .name("worker-1".into())
    .stack_size(2 << 20)
    .spawn(|| /* work */ ) // -> std::io::Result<JoinHandle<_>> in real code if you wrap errors
    .expect("spawn");
h.join().expect("join");
```

**Analysis:**  
- Ownership impact: None.  
- Performance: None.  
- Typical: No error.

**Takeaway:** Improves debuggability and avoids pathological stack growth issues.

> **Lab – Try This:** Name thread.  
> **Solution:** Builder::new().name

**Part III Checkpoint:** Crossbeam for?  
**Answers:** Channels.

**You Can Now:**  
- Apply in project.

**Part III Quiz:** (5 MCQs + 1 open conceptual question)  
1. Select for? (a) Race (b) Join (c) Lock  
   Answer: (a)  
2. True/False: Atomic lock.  
   Answer: False  
3. Deadlock fix? (a) Order (b) Channel (c) Both  
   Answer: (c)  
4. Naming for? (a) Debug (b) Perf (c) Sync  
   Answer: (a)  
5. True/False: Atomics compound.  
   Answer: False  
Open Conceptual: Explain atomic vs mutex.  
Answer: Simple ops.

**Self-Assessment:**  
[ ] Applied concurrency.  
[ ] Tested.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Exercises: Tiered Reasoning

### Tier 1: Concept Rebuilds

1. Thread Spawn  
   Simple thread.  
   **Solution:** thread::spawn

2. Channel Send  
   crossbeam.  
   **Solution:** tx.send

### Tier 2: Comparative Rewrites

1. C Thread to Rust  
   Safe spawn.  
   **Solution:** spawn/join

2. Python Queue to Channel  
   Message.  
   **Solution:** bounded plus select!

### Tier 3: Challenge Extensions

1. Parallel Sum  
   Rayon iter.  
   **Solution:** into_par_iter().sum()

2. Deadlock Fix  
   Order locks.  
   **Solution:** Consistent order

**Self-Assessment:**  
[ ] Completed one per tier.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Recap and Synthesis Reflection

**Table Completion Exercise:**  
| Rust Feature | C/C++ Issue | Python Trade-off |
|--------------|-------------|------------------|
| Threads | Race prone | GIL limit |
| Channels | Pipe manual | Queue throughput is OK but lacks static typing and zero-cost moves. |

**Self-Quiz:** (Design-level)  
1. Threads for?  
2. Channels avoid?  
Answers:  
1. CPU.  
3. Race.

**Final Takeaway:** Concurrency safe multi-task.

**Glossary Appendix Update:** Add: Thread, Channel.

**Error Code Index:**  
| Code   | Description                     | Example Case |
|--------|---------------------------------|--------------|
| E0277  | Required trait bound not satisfied (e.g., Send/Sync) | Rc<T> sent to a thread (not Send) |
| E0373  | Closure outlives                | Borrow thread |
| E0507  | Cannot move out                 | Moving out of a &T or &mut T |
| E0502  | Borrow later used               | NLL violation |
| E0596  | Cannot borrow as mutable         | Immutable call |

**Primary References:** Rust Book Ch. 16 (Concurrency).

**Suggested Deep Dives:** Crossbeam docs; Rayon guide; Crossbeam select! cookbook.

**Concept Map:** (Text-based ASCII)  
Concurrency  
  ├── Threads (spawn/join)  
  └── Channels (mpsc)  
Applied (Task example)

**Self-Assessment:**  
[ ] Reviewed map/quiz.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

**Deep Dive Appendix:**  
- Send/Sync: Cross-thread safe.

**“Done Means Done” Checklist**  
- Architecture: Parallel integrated.  
- API: No raw threads; abstract traits.  
- Quality: Clippy/docs pass.  
- Tests: Concurrent tests with barriers.  
- Perf: Profile contention.

**Compile-Fail Mini-Labs (Retention + Rigor)**  
1. Non-Send (E0277)  
   ```rust,compile_fail
   use std::rc::Rc;
   let rc = Rc::new(1); thread::spawn(move || drop(rc)); // E0277
   fn main() {}
   ```  
2. Borrow Outlive (E0373)  
   ```rust,compile_fail
   fn main() {
       let local = 42;
       // closure must be 'static; borrowed `local` cannot outlive main
       std::thread::spawn(|| { let _ = &local; }); // E0373
   }
   ```  
3. Move Out Borrowed (E0507)  
   ```rust,compile_fail
   fn main() {
       let v = vec![1,2,3];
       let r: &Vec<i32> = &v;
       let _moved = *r; // E0507: cannot move out of `*r`
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

**Criterion Bench (Prove Claims)**  
```rust
// benches/thread_vs_seq.rs
use criterion::{criterion_group, criterion_main, Criterion};
fn seq_sum(n: u64) -> u64 { (1..=n).sum() }
fn thread_sum(n: u64) -> u64 {
    use std::thread;
    let mid = n / 2;
    let h1 = thread::spawn(move || (1..=mid).sum::<u64>());
    let h2 = thread::spawn(move || (mid+1..=n).sum::<u64>());
    h1.join().unwrap() + h2.join().unwrap()
}
fn bench(c: &mut Criterion) {
    c.bench_function("seq_sum", |b| b.iter(|| seq_sum(1_000_000)));
    c.bench_function("thread_sum", |b| b.iter(|| thread_sum(1_000_000)));
}
criterion_group!(benches, bench);
criterion_main!(benches);
// Note: For data-parallel, prefer rayon; manual threads are didactic. Benchmarks can be noisy; compare relative speedups. For n = 1_000_000, the threaded version will likely be slower due to overhead; this is didactic.
```

```toml
# task_core/Cargo.toml
[dev-dependencies]
criterion = { version = "0.5", default-features = false }
[[bench]]
name = "thread_vs_seq"
harness = false
```

**Testing Guidance for Concurrent Code**  
```rust
use std::{sync::{Arc, Barrier}, thread};
#[test]
fn concurrent_works() {
    let barrier = Arc::new(Barrier::new(2));
    let t1 = thread::spawn({ let b = barrier.clone(); move || b.wait() });
    barrier.wait();
    t1.join().unwrap();
}

#[test]
fn deadlock_fixed_by_lock_order() {
    use std::sync::{Arc, Mutex};
    let (a, b) = (Arc::new(Mutex::new(0)), Arc::new(Mutex::new(0)));

    let t = {
        let (a, b) = (a.clone(), b.clone());
        std::thread::spawn(move || {
            let _g1 = a.lock().unwrap();
            let _g2 = b.lock().unwrap();
        })
    };
    // Same order here → no deadlock
    let _g1 = a.lock().unwrap();
    let _g2 = b.lock().unwrap();
    t.join().unwrap();
}
```