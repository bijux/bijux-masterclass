# Session 8B: Smart Pointers & Interior Mutability – Sharing Without Leaks

**Target Audience & Scope:** This series assumes familiarity with C/Python, basic memory models (e.g., stack/heap, pointers/references, GC internals), and command-line tools. It targets programmers with systems or dynamic language experience new to Rust. Tone balances explanation for beginners in Rust but avoids over-simplifying semantics for intermediates.

**Assumed background:** familiarity with modules/crates, iterators, and a multi-crate workspace; a simple CLI ‘Task Manager’ helps but is not required.

We pin the course toolchain to stable 1.91 (Edition 2024).

**Conceptual Learning Goals:**  
- Use smart pointers for heap allocation, shared ownership, and interior mutability.  

**Mechanical Learning Goals:**  
- Use Box<T>, Rc/Arc<T>, RefCell/Mutex<T> in code.  
- Apply Deref and Drop traits with smart pointers.  

**Design Learning Goals:**  
- Choose appropriate smart pointers based on ownership needs (single vs shared, immutable vs mutable).  
- Test code involving smart pointers, including panic scenarios for RefCell.  

**By the End of This Session, You Can:**  
- Use smart pointers for heap and shared data.  
- Handle interior mutability safely.  
- Design APIs with shared state.  
- Fix smart pointer errors.  
- Extend CLI with smart pointers.  

**Project Narrative:** Introduce smart pointers into the ‘Task Manager’ example. Use Box for recursive tasks and Rc<RefCell<Config>> (CLI scope only) for shared mutable configuration.

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

**Decision Framework: Lifetime vs Smart Pointer**  
- Short-lived borrow → &T / &mut T with 'a.  
- Heap allocation without sharing → Box<T>.  
- Shared immutable → Rc<T> (single-thread) / Arc<T> (multi-thread).  
- Shared mutable → Rc<RefCell<T>> (single) / Arc<Mutex<T>> (multi).  
- 'static for globals/constants.  

**Anti-Patterns to Avoid**  
- Using RefCell as a "borrow checker escape hatch"; prefer redesign.  
- Raw pointers (*const/*mut); stick to safe smart pointers.  
- Cloning Rc/Arc excessively; share the pointer instead.  

**Public API Policy**  
- Do: Expose owned fields (String, Vec<T>, Arc<T>). Provide borrowed accessors that return &str, &[T], or iterators with clear lifetime ties.  
- Do not: Expose Rc<RefCell<_>>, Arc<Mutex<_>>, Arc<RwLock<_>>, or lock guards in public signatures.  
- Do not: Store borrowed fields (&'a str, &'a [T]) in public structs. Use owned data; offer borrowed views via methods.  
- Do: Prefer impl Trait returns internally. Use dyn Trait only at plugin or dynamic boundaries.

**Perf and Binary Size Guidance**  
- Box: One heap allocation + pointer indirection; measure with Criterion if it matters.  
- Rc/Arc: Ref-counting adds atomic ops for Arc.  
- RefCell: Runtime borrow checks; use for rare interior mutability.  
- Profile with flamegraph if sharing impacts perf.

**Architecture Update**  
- Introduce recursive types, e.g., Task with optional Box<Task> for subtasks.  
- Shared config: Rc<RefCell<Config>> in CLI for mutable settings across commands.  
- Iterator interplay: Ensure iter<'a>() lifetimes align with smart pointer borrows.

**End-to-End Delta for Task Manager (Coherent, Compilable)**  
```rust
// task_core/src/domain/task.rs
pub struct Task {
    pub id: u64,
    pub title: String,
    pub deps: Vec<Box<Task>>, // recursive via Box
}

// task_cli/src/config.rs (bin crate only; not public API)
use std::{cell::RefCell, rc::Rc};

#[derive(Default)]
pub struct Config { pub verbose: bool }

#[derive(Clone)]
pub(crate) struct SharedConfig(Rc<RefCell<Config>>);

impl SharedConfig {
    pub fn new() -> Self { Self(Rc::new(RefCell::new(Config::default()))) }
    pub fn set_verbose(&self, b: bool) { self.0.borrow_mut().verbose = b; }
    pub fn verbose(&self) -> bool { self.0.borrow().verbose }
}

// Borrowed iterator API remains lifetime-safe
impl Task {
    pub fn titles<'a>(&'a self) -> impl Iterator<Item = &'a str> + 'a {
        std::iter::once(self.title.as_str())
            .chain(self.deps.iter().flat_map(|d| d.titles()))
    }
    pub fn into_titles(self) -> impl Iterator<Item = String> {
        std::iter::once(self.title).chain(self.deps.into_iter().flat_map(|d| d.into_titles()))
    }
}
```
See 8A for Vec<Box<Task>> rationale.

**Send/Sync & Interior Mutability (Boundary Clarity)**  
| Type | Send | Sync | Notes |
|------|------|------|-------|
| T | if T: Send | if T: Sync | Base rule. |
| Box<T> | if T: Send | if T: Sync | No sharing semantics. |
| Rc<T> | No | No | Single-thread only. |
| Arc<T> | if T: Send + Sync | if T: Send + Sync | Cross-thread shared. |
| RefCell<T> | if T: Send | No | Not Sync; don’t share across threads.¹ |
| Mutex<T> | if T: Send | if T: Send | Guard enforces exclusivity; T needn’t be Sync. |
| RwLock<T> | if T: Send | if T: Send + Sync | Readers run concurrently → T must be Sync. |  
¹ Arc<RefCell<T>> is not Sync → do not share it across threads; use Arc<Mutex<T>>/Arc<RwLock<T>>.  
Note: Arc<RefCell<T>> is not Sync; do not share it across threads. Use Arc<Mutex<T>> or redesign with message passing. If you find yourself cloning Arc<Mutex<T>> widely, reconsider your ownership and concurrency model.

---

## Setup Checklist

Verify and extend with emphasis on smart pointers.

1. **Verify Existing Setup**  
   ```bash
   cargo --version
   rustc --version
   cargo fmt
   cargo clippy -- -D warnings
   cargo test
   cargo test --doc
   ```
   Expect recent versions; update with `rustup update`. Confirm rust-analyzer (hover for lifetimes).

2. **Add Dependencies for Smart Pointers (if needed)**  
   ```bash
   cargo add anyhow --features=backtrace
   ```

3. **Install Flamegraph for Profiling (Optional)**  
   ```bash
   cargo install flamegraph
   ```

4. **Run the CLI**  
   ```bash
   cargo run
   ```
   Ensure the CLI runs end-to-end.

**Self-Assessment:**  
[ ] Verified setup.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part II: Smart Pointers – Heap and Shared Ownership

**You Will Be Able To:**  
- Use Box for heap.  
- Share with Rc/Arc.  
- Contrast with C/C++/Python alloc.  

### Core Concept: Case 1 – Box for Heap Allocation

**Problem / Motivation:** Stack limits; recursive types.

**Definition (Formal):** Box: Owned heap allocation with deterministic drop.

**Mental Model (Simplified):** Owned heap allocation with deterministic drop.

**Example (Compilable):** Recursive.  
```rust
enum Tree { Node(i32, Box<Tree>, Box<Tree>), Leaf }
```

**Code Triple:**  
**Rust (Box):**  
```rust
let b = Box::new(42);
```  

**C/C++ (New):**  
```cpp
int* b = new int(42); // manual delete
```  

**Python (Auto):**  
```python
b = 42  # GC
```

**Rust Failure Variant:** Large stack.  
```rust
struct Big([u8; 1_000_000]); // stack overflow
fn main() {}
```

**Compiler Output:** None; runtime panic.

**Analysis:**  
- Ownership impact: Moves with Box.  
- Performance: One heap allocation + pointer indirection; measure with Criterion if it matters.  
- Typical: No error; use Box.

**Takeaway:** Heap safe.

> **Lab – Try This:** Box recursive enum.  
> **Solution:** Box<Tree>

### Core Concept: Case 2 – Rc/Arc for Shared Ownership

**Problem / Motivation:** Multiple owners; ref-count.

**Definition (Formal):** Rc: Single-thread count; Arc: Atomic.

**Mental Model (Simplified):** Share, auto-drop on zero.

**Example (Compilable):** Shared.  
```rust
use std::rc::Rc;
let shared = Rc::new(42);
let clone1 = Rc::clone(&shared);
```

**Code Triple:**  
**Rust (Rc):**  
```rust
Rc::new(vec![])
```  

**C/C++ (Shared_ptr):**  
```cpp
std::shared_ptr<std::vector<int>> p = std::make_shared<std::vector<int>>();
```  

**Python (Ref):**  
```python
p = []  # GC shares
```

**Rust Failure Variant:** Cycle leak.  
```rust
#[derive(Default)] struct Node { next: RefCell<Option<Rc<Node>>> }
let a = Rc::new(Node::default());
let b = Rc::new(Node::default());
*a.next.borrow_mut() = Some(b.clone());
*b.next.borrow_mut() = Some(a.clone()); // cycle
fn main() {}
```

**Compiler Output:** None; memory leak.

**Analysis:**  
- Ownership impact: Shared.  
- Performance: Count ops.  
- Typical: No error.

**Takeaway:** Safe sharing.

> **Lab – Try This:** Rc shared config.  
> **Solution:** Rc::new(Config)

### Core Concept: Case 3 – Weak for Cycle Avoidance

**Problem / Motivation:** Rc cycles leak memory.

**Definition (Formal):** Weak: Non-owning ref; no count increment.

**Mental Model (Simplified):** Break cycles with weak links.

**Example (Compilable):** Weak fix.  
```rust
#[derive(Default)] struct Node2 { next: RefCell<Option<Weak<Node2>>> }
let a = Rc::new(Node2::default());
let b = Rc::new(Node2::default());
*a.next.borrow_mut() = Some(Rc::downgrade(&b));
*b.next.borrow_mut() = Some(Rc::downgrade(&a)); // no cycle
```

**Rust Failure Variant:** Use after drop.  
```rust
let w = Rc::downgrade(&rc); drop(rc); w.upgrade() // None
fn main() {}
```

**Compiler Output:** None; Option::None.

**Analysis:**  
- Ownership impact: No own.  
- Performance: Check upgrade.  
- Typical: None at runtime.

**Takeaway:** Avoid leaks.

> **Lab: Cycle Leak → Weak Fix**  
> Start with the leak (two Rc<Node> pointing to each other via RefCell<Option<Rc<_>>>).  
> Measure drop behavior and memory via strong/weak counts.  
> Fix with Weak, then re-check counts; confirm drops.  
> **Solution:** assert_eq!(Rc::strong_count(&a), 1); assert_eq!(Rc::weak_count(&a), 1);

### Core Concept: Case 4 – Rc/Arc::new_cyclic for Self-Referential

**Problem / Motivation:** Initialize self-ref.

**Definition (Formal):** Cyclic new.

**Mental Model (Simplified):** Weak self in init.

**Example (Compilable):** Cyclic.  
```rust
use std::{rc::{Rc, Weak}, cell::RefCell};

struct Node { next: RefCell<Option<Weak<Node>>> }

let a = std::rc::Rc::new_cyclic(|me| Node { next: RefCell::new(Some(me.clone())) });
// Use `me` only to store Weak self-links. Do not upgrade & read inside the closure.
// Access self-links after construction completes.
```

**Analysis:**  
- Ownership impact: Safe cyclic.  
- Performance: Count.  
- Typical: No error.

**Takeaway:** Self-ref graphs. Caution: only for truly self-referential graphs, prefer IDs/arena when possible.

> **Lab – Try This:** Use new_cyclic.  
> **Solution:** Rc::new_cyclic

### Core Concept: Case 5 – Arc::make_mut / Clone-on-Write Ergonomics

**Problem / Motivation:** Mutate shared if unique.

**Definition (Formal):** Make mut if refcount 1.

**Mental Model (Simplified):** Detach on write.

**Example (Compilable):** Make mut.  
```rust
let mut a = Arc::new(vec![1,2,3]);
let s1 = a.clone();
let s2 = a.clone();
// unique mutable access (detaches) if strong_count > 1
Arc::make_mut(&mut a).push(4);
```

**Analysis:**  
- Ownership impact: Unique mut.  
- Performance: Clone if shared; clone cost is type-dependent.  
- Typical: No error.

**Takeaway:** Prefer immut; cow on need.

> **Lab: Arc::make_mut COW under Contention**  
> Use make_mut in API.  
> **Solution:** Arc::make_mut

### Core Concept: Case 6 – Cow<'a, T> as Lifetime-Aware API

**Problem / Motivation:** Borrow or own return.

**Definition (Formal):** Cow: Borrowed or owned.

**Mental Model (Simplified):** Efficient return.

**Example (Compilable):** Cow.  
```rust
use std::borrow::Cow;
fn get_name<'a>(name: &'a str, needs_compute: bool) -> Cow<'a, str> {
    if !needs_compute {
        Cow::Borrowed(name)
    } else {
        Cow::Owned(format!("computed_{}", name))
    }
}
```

**Analysis:**  
- Ownership impact: Borrow prefer.  
- Performance: No clone if borrow.  
- Typical: No error.

**Takeaway:** Lifetime-aware. Warn against returning &'a String—return &'a str or Cow<'a, str> instead. Mention Cow<'a, [T]> for zero-copy view/clone of small vectors in hot paths.

> **Lab – Try This:** Return Cow in API.  
> **Solution:** Cow<'a, str>

### Core Concept: Case 7 – Arena/ID Pattern (Self-Ref Alternative)

**Problem / Motivation:** Avoid self-ref.

**Definition (Formal):** IDs instead of refs.

**Mental Model (Simplified):** Index access.

**Example (Compilable):** Arena.  
```rust
struct Arena<T> { items: Vec<T> }
type Id = usize;
impl<T> Arena<T> {
    fn insert(&mut self, t: T) -> Id { self.items.push(t); self.items.len()-1 }
    fn get(&self, id: Id) -> Option<&T> { self.items.get(id) }
}
```

**Analysis:**  
- Ownership impact: Central own.  
- Performance: Index access.  
- Typical: No error.

**Takeaway:** Safe alternative. Prefer a newtype Id(usize) for type safety.  
```rust
#[repr(transparent)]
struct TaskId(usize);
```

> **Lab – Try This:** Use arena for graph.  
> **Solution:** Store IDs.

**Part II Checkpoint:** Box for?  
**Answers:** Heap/single owner.

**You Can Now:**  
- Use Box/Rc/Arc/Weak/Cow.

**Part II Quiz:** (5 MCQs + 1 open conceptual question)  
1. What does Box own? (a) Stack (b) Heap (c) Static  
   Answer: (b)  
2. True/False: Rc multi-thread.  
   Answer: False  
3. Arc overhead? (a) Atomic (b) None (c) GC  
   Answer: (a)  
4. Cycle with Rc? (a) Panic (b) Leak (c) Error  
   Answer: (b)  
5. True/False: Weak owns.  
   Answer: False  
Open Conceptual: Explain Rc vs Arc.  
Answer: Single vs multi-thread.  
Design Question: When would you replace Rc<RefCell<T>> with an Arena<T> indexed by Id? Provide one concrete invariants advantage.

**Self-Assessment:**  
[ ] Used smart pointers.  
[ ] Shared data.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part III: Interior Mutability – Mutable Through Immutable Refs

**You Will Be Able To:**  
- Use RefCell/Mutex.  
- Handle runtime borrows.  
- Integrate with iterators/dyn.  

### Core Concept: Case 1 – RefCell for Single-Thread Mut

**Problem / Motivation:** Mutate shared immutable.

**Definition (Formal):** RefCell: Runtime borrow check.

**Mental Model (Simplified):** Borrow at runtime.

**Example (Compilable):** Interior.  
```rust
use std::{cell::RefCell, rc::Rc};
let shared = Rc::new(RefCell::new(42));
*shared.borrow_mut() += 1;
```

**Rust Failure Variant:** Double mut borrow.  
```rust
let b1 = shared.borrow_mut();
let b2 = shared.borrow_mut(); // panic
fn main() {}
```

**Compiler Output:** None; runtime panic.

**Analysis:**  
- Ownership impact: Interior.  
- Performance: Runtime check.  
- Typical: Panic.

**Takeaway:** Flexible mut.

> **Lab – Try This:** Rc<RefCell> shared mut.  
> **Solution:** borrow_mut()

### Core Concept: Case 2 – Mutex for Multi-Thread Mut

**Problem / Motivation:** Safe concurrent mut.

**Definition (Formal):** Mutex: Lock-based mut.

**Mental Model (Simplified):** Guarded access.

**Example (Compilable):** Thread-safe.  
```rust
use std::sync::{Arc, Mutex};
let shared = Arc::new(Mutex::new(42));
let guard = shared.lock().unwrap();
```

**Rust Failure Variant:** Poisoned.  
```rust
let guard = shared.lock(); panic!(); // poisons
let next = shared.lock().map_err(|e| anyhow!(e.to_string()))?; // Err
fn main() {}
```

**Compiler Output:** None; Err(poison).

**Analysis:**  
- Ownership impact: Shared mut.  
- Performance: Lock contention.  
- Typical: Poison error.

**Poisoning & Recovery**  
```rust
match shared.lock() {
    Ok(guard) => { /* use guard */ }
    Err(poisoned) => {
        let _guard = poisoned.into_inner(); // recover if invariants allow
    }
}
```

If panic may leave T inconsistent, do not recover. Only recover from a poisoned Mutex if your T maintains an internal invariant independent of the panicked update; otherwise, propagate error.

**Takeaway:** Concurrent safe.

> **Lab – Try This:** Arc<Mutex> multi-thread.  
> **Solution:** lock().unwrap()

### Core Concept: Case 3 – RwLock vs Mutex Trade-Off (Read-Heavy vs Write-Heavy)

**Problem / Motivation:** Read-many/write-few.

**Definition (Formal):** RwLock: Multiple readers or one writer.

**Mental Model (Simplified):** Optimized lock.

**Example (Compilable):** RwLock.  
```rust
use std::sync::{Arc, RwLock};
let db = Arc::new(RwLock::new(String::new()));
{
    let r = db.read().unwrap(); r.len(); // many readers OK
}
{
    let mut w = db.write().unwrap(); w.push_str("x"); // exclusive write
}
```

**Analysis:**  
- Ownership impact: Shared read.  
- Performance: Better for read-heavy.  
- Typical: No error.

**RwLock vs Mutex rule-of-thumb:**  
- Write-heavy or small critical sections → Mutex<T>.  
- Read-many/write-few with large read sections → RwLock<T>.  
- RwLock<T>: Send if T: Send and Sync if T: Send + Sync. Because readers run concurrently, T must be Sync for RwLock<T> to be Sync. Avoid in highly contended paths.  

**Takeaway:** Optimized for reads.

> **Lab – Try This:** Use RwLock in db.  
> **Solution:** read()/write()

**When Not to Use RefCell/Mutex**  
Prefer message passing for: high contention hot path or API surface risk (guard leakage).  

**Part III Checkpoint:** RefCell for?  
**Answers:** Interior mut.

**You Can Now:**  
- Use RefCell/Mutex/RwLock.  
- Integrate with prior.

**Part III Quiz:** (5 MCQs + 1 open conceptual question)  
1. RefCell checks? (a) Compile (b) Runtime (c) None  
   Answer: (b)  
2. True/False: Mutex single-thread.  
   Answer: False  
3. Poisoned mutex? (a) Panic (b) Err (c) Ok  
   Answer: (b)  
4. Interior mut for? (a) Immutable mutate (b) Heap (c) Lifetime  
   Answer: (a)  
5. True/False: Arc<RefCell<T>> thread-safe.  
   Answer: False  
Open Conceptual: Explain interior mut.  
Answer: Mutate via immut ref.

**Self-Assessment:**  
[ ] Handled mutability.  
[ ] Fixed panics.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part IV: Application and Integration

**You Will Be Able To:**  
- Apply smart pointers in project.  
- Test with them.  
- Profile perf.  

### Core Concept: Deref and Drop with Smart Pointers

**Problem / Motivation:** Pointer behavior; custom cleanup.

**Definition (Formal):** Deref: *p like &T.

**Mental Model (Simplified):** Transparent access.

**Example (Compilable):** Deref.  
```rust
let b = Box::new(42);
let x = *b; // deref
```

**Analysis:**  
- Ownership impact: Drop on scope.  
- Performance: Minimal.  
- Typical: No error.

**Deref pitfalls:** Explicit &*guard in APIs.

```rust
use std::sync::Mutex;
let m = Mutex::new(String::new());
let guard = m.lock().unwrap();
// method on &str? take a ref explicitly:
let s: &str = &*guard; // deref to String, then coerce to &str
assert!(s.is_empty());
```

**Takeaway:** Smart behavior.

* &Box<T> → &T
* &String → &str
* &Vec<T> → &[T]

> **Lab – Try This:** Impl Drop for custom.  
> **Solution:** impl Drop { fn drop(&mut self) { ... } }

### Core Concept: Interplay with Iterators and Dyn

**Problem / Motivation:** Borrow in chains; dyn with pointers.

**Definition (Formal):** Box<dyn Trait> for vtables.

**Mental Model (Simplified):** Dynamic with safety.

**Example (Compilable):** Dyn iter.  
```rust
let it: Box<dyn Iterator<Item = i32>> = Box::new(1..10);
```

**Analysis:**  
- Ownership impact: Trait object.  
- Performance: Vtable.  
- Typical: Object-safe.

**Dyn vs impl Trait boundary rule:** Prefer impl Trait internally; expose dyn Trait only at plugin/dynamic boundaries to decouple compilation units. If used cross-thread, require dyn Trait + Send + Sync.

**Takeaway:** Flexible dispatch.

> **Lab – Try This:** Box<dyn> plugin.  
> **Solution:** Box<dyn CommandHandler>

### Core Concept: Try Unwrap and Failure Path

**Problem / Motivation:** Regain ownership.

**Definition (Formal):** Try unwrap if count 1.

**Mental Model (Simplified):** Unique then own.

**Example (Compilable):** Try unwrap.  
```rust
match Arc::try_unwrap(arc) {
    Ok(inner) => inner,
    Err(a) => {
        // still multiple owners; clone if cheap or refactor ownership model
        (*a).clone() // requires T: Clone
    }
}
fn main() {}
```

**Analysis:**  
- Ownership impact: Regain.  
- Performance: Check count.  
- Typical: Err if shared.

**Takeaway:** Ownership control. If cloning T is expensive, refactor ownership instead of cloning on the slow path.

> **Lab – Try This:** Use try_unwrap.  
> **Solution:** match Arc::try_unwrap

### Core Concept: Rc::try_unwrap

**Problem / Motivation:** Regain single-thread.

**Definition (Formal):** Try unwrap Rc.

**Mental Model (Simplified):** Unique then own.

**Example (Compilable):** Rc unwrap.  
```rust
let rc = std::rc::Rc::new(String::from("x"));
if let Ok(inner) = std::rc::Rc::try_unwrap(rc) {
    // unique, ownership regained
}
fn main() {}
```

**Analysis:**  
- Ownership impact: Regain.  
- Performance: Check count.  
- Typical: Err if shared.

**Takeaway:** Single-thread regain.

> **Lab – Try This:** Rc try_unwrap.  
> **Solution:** Rc::try_unwrap

### Core Concept: Iterator Recursion: Stack Depth Note

**Problem / Motivation:** Deep recursion stack overflow.

**Definition (Formal):** Iterative alternative.

**Mental Model (Simplified):** Stack for recursion.

**Example (Compilable):** Iterative.  
```rust
use std::collections::VecDeque;
pub fn titles_iter<'a>(&'a self) -> impl Iterator<Item = &'a str> {
    let mut q: VecDeque<&'a Self> = VecDeque::from([self]);
    std::iter::from_fn(move || {
        while let Some(t) = q.pop_front() {
            q.extend(t.deps.iter().map(|b| &**b));
            return Some(t.title.as_str());
        }
        None
    })
}
```

**Analysis:**  
- Ownership impact: No recursion.  
- Performance: Stack safe.  
- Typical: No error.

If dependency depth can be large, prefer an explicit stack (Vec) to avoid deep recursion.

**Takeaway:** Safe recursion. Iterator captures 'a and cannot outlive self; this is expected and correct.

> **Lab – Try This:** Iterative titles.  
> **Solution:** VecDeque stack.

All iterator examples in S8 continue to use the GAT-based TaskStore iterators introduced in Session 7; do not introduce as_slice() helpers.

**Part IV Checkpoint:** Deref for?  
**Answers:** Access inner.

**You Can Now:**  
- Integrate concepts.

**Part IV Quiz:** (5 MCQs + 1 open conceptual question)  
1. Deref to? (a) &T (b) T (c) Box  
   Answer: (a)  
2. True/False: Drop custom.  
   Answer: True  
3. Dyn with? (a) Box (b) & (c) Both  
   Answer: (c)  
4. Object-safe? (a) Generics ok (b) No generics (c) Static  
   Answer: (b)  
5. True/False: Iter with lifetimes.  
   Answer: True  
Open Conceptual: Explain dyn vs impl Trait.  
Answer: Dynamic vs static.

**Self-Assessment:**  
[ ] Applied in project.  
[ ] Tested/profiling.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Exercises: Tiered Reasoning

### Tier 1: Concept Rebuilds

1. Box Def  
   Heap struct.  
   **Solution:** Box::new(T)

### Tier 2: Comparative Rewrites

1. C New to Box  
   Safe alloc.  
   **Solution:** Box::new

2. Python GC to Rc  
   Shared.  
   **Solution:** Rc::new

### Tier 3: Challenge Extensions

1. RefCell Shared  
   Mutable config.  
   **Solution:** Rc<RefCell<T>>

2. Mutex Thread  
   Concurrent.  
   **Solution:** Arc<Mutex<T>>

**Self-Assessment:**  
[ ] Completed one per tier.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Recap and Synthesis Reflection

**Table Completion Exercise:**  
| Rust Feature | C/C++ Issue | Python Trade-off |
|--------------|-------------|------------------|
| Box | Manual delete | Refcounting plus periodic GC; cycles require GC; performance depends on interpreter and workload, not just language semantics. |
| Rc/Arc | Shared_ptr race | Refcounting plus periodic GC; cycles require GC; performance depends on interpreter and workload, not just language semantics. |
| RefCell/Mutex | Mutable const | Always mutable; no compile-time checks; threading requires explicit locks. |

**Self-Quiz:** (Design-level)  
1. Smart pointers for?  
2. Interior mut when?  
Answers:  
1. Heap/share.  
2. Mutate immut.

**Final Takeaway:** Smart pointers enable safe sharing and mutability.

**Glossary Appendix Update:** Add: Box, Rc/Arc, RefCell/Mutex, Deref, Weak, Cow, RwLock.

**Error Code Index:**  
| Code   | Description                     | Example Case |
|--------|---------------------------------|--------------|
| E0505  | Cannot move out of borrowed     | Ownership |
| E0277  | Required trait bound not satisfied (e.g., Send, Sync, Sized, etc.) | Rc<T> sent to a thread (not Send) / missing Sized / other unsatisfied bounds. |
| E0596  | Cannot borrow as mutable         | Immutable call |
| E0038  | Trait not object safe           | Trait object fail |

**Primary References:** Rust Book Ch. 15 (Smart Pointers), Ch. 16 (Concurrency).

**Suggested Deep Dives:** Interior mut patterns.

**Concept Map:** (Text-based ASCII)  
Smart Pointers  
  ├── Box (heap)  
  ├── Rc/Arc (share)  
  └── RefCell/Mutex (mut)  
Applied (Task example)

**Self-Assessment:**  
[ ] Reviewed map/quiz.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

**Deep Dive Appendix:**  
- Deref coercion: Box to &T.  
- Poisoning: Mutex after panic.

**“Done Means Done” Checklist**  
- Correctness: Send/Sync table corrected; no unsafe/misleading example; cycle with Weak covered and tested.  
- API: No RefCell in public types; clear impl Trait vs dyn Trait boundary.  
- Tests: trybuild suite for policy; prelude-only import rule in place; property tests still pass.  
- Docs: Arc::make_mut patterns documented.  
- Perf: Criterion benches present; claims toned down and evidenced.  

**Compile-Fail Mini-Labs (Retention + Rigor)**  
1. Public RefCell (Custom Policy)  
   ```rust
   pub struct BadAPI { pub cfg: std::rc::Rc<std::cell::RefCell<u32>> } // ❌ public RefCell
   fn main() {}
   ```  
2. Object Safety (E0038)  
   ```rust
   trait Bad { fn generic<T>(&self); } let _ = Box::new(dyn Bad); // E0038
   fn main() {}
   ```  
3. Public Lock Guard (Custom Policy)  
   ```rust
   use std::sync::{Arc, Mutex, MutexGuard};

   pub struct Bad {
       pub guard: MutexGuard<'static, u32>, // exposing guard is a public API leak
   }
   fn main() {}
   ```

**Testing Guidance for RefCell Panics**  
```rust
#[test]
#[should_panic(expected = "already borrowed: BorrowMutError")]
fn refcell_double_mut_panics() {
    use std::cell::RefCell;
    let x = RefCell::new(0);
    let _g1 = x.borrow_mut();
    let _g2 = x.borrow_mut();
}
```

```rust
use std::cell::RefCell;

#[test]
fn refcell_scoped_ok() {
    let x = RefCell::new(0);
    {
        let _g = x.borrow_mut(); // guard dropped here
    }
    {
        let _g2 = x.borrow_mut(); // ok
    }
}
```

**Criterion Bench (Prove Claims)**  
```rust
// benches/arc_make_mut.rs
use std::sync::Arc;
use criterion::{criterion_group, criterion_main, Criterion, black_box};

fn arc_make_mut_bench(c: &mut Criterion) {
    c.bench_function("arc_make_mut shared", |b| {
        let mut a = Arc::new(vec![0u64; 10_000]);
        let _a2 = a.clone();
        b.iter(|| {
            let v = Arc::make_mut(&mut a);
            v[0] = black_box(1);
        })
    });
}
fn arc_make_mut_contended(c: &mut Criterion) {
    c.bench_function("arc_make_mut contended", |b| {
        b.iter(|| {
            let mut a = Arc::new(vec![0u64; 1024]);
            let _c1 = a.clone();
            let _c2 = a.clone();
            let v = Arc::make_mut(&mut a); // forces clone
            criterion::black_box(v).push(1);
        })
    });
}
criterion_group!(benches, arc_make_mut_bench, arc_make_mut_contended);
criterion_main!(benches);
```

```toml
# task_core/Cargo.toml
[dev-dependencies]
criterion = { version = "0.5", default-features = false }
[[bench]]
name = "arc_make_mut"
harness = false
```

**Migration Note:** C++ shared_ptr<T> + mutex → prefer Arc<T> + message passing or Arc<RwLock<T>> (read-heavy), but never expose the lock guard in public API.
