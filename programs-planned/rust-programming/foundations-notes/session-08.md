# Session 8A: Lifetimes – Ensuring References Live Long Enough

**Target Audience & Scope:** This series assumes familiarity with C/Python, basic memory models (e.g., stack/heap, pointers/references, GC internals), and command-line tools. It targets programmers with systems or dynamic language experience new to Rust. Tone balances explanation for beginners in Rust but avoids over-simplifying semantics for intermediates.

**Assumed background:** familiarity with modules/crates, iterators, and a multi-crate workspace; a simple CLI ‘Task Manager’ helps but is not required.

We pin the course toolchain to stable 1.91 (Edition 2024).

**Conceptual Learning Goals:**  
- Internalize lifetime syntax and intuition for safe references across functions and types.  
- Understand lifetime subtyping, variance, and when to apply 'static.  

**Mechanical Learning Goals:**  
- Annotate lifetimes with 'a in functions, structs, and traits.  
- Read and fix lifetime-related errors like outlived borrows or missing specifiers.  

**Design Learning Goals:**  
- Extend the Task Manager with lifetime-safe APIs.  
- Test code involving lifetimes, including borrowed iterators.  

**By the End of This Session, You Can:**  
- Annotate and elide lifetimes correctly.  
- Design APIs with borrowed returns.  
- Fix lifetime errors.  
- Extend CLI with lifetime-safe iterators.  

**Project Narrative:** Introduce lifetime annotations into the ‘Task Manager’ example. Ensure borrowed iterator APIs are lifetime-safe.

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
extras = []
```

**Public API Policy**  
- Do: Expose owned fields (String, Vec<T>, Arc<T>). Provide borrowed accessors that return &str, &[T], or iterators with clear lifetime ties.  
- Do not: Expose Rc<RefCell<_>>, Arc<Mutex<_>>, Arc<RwLock<_>>, or lock guards in public signatures.  
- Do not: Store borrowed fields (&'a str, &'a [T]) in public structs. Use owned data; offer borrowed views via methods.  
- Do: Prefer impl Trait returns internally. Use dyn Trait only at plugin or dynamic boundaries.  
- Lifetime parameters in public APIs should be explicit if not elidable.  
- Document lifetime relationships in API docs.

**Architecture Update**  
- Add lifetime params to TaskQuery<'a, S> if not already.  
- Borrowed iterator API remains lifetime-safe  
```rust
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

**End-to-End Delta for Task Manager (Coherent, Compilable)**  
```rust
// task_core/src/domain/task.rs
pub struct Task {
    pub id: u64,
    pub title: String,
    pub deps: Vec<Box<Task>>, // recursive via Box
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
Vec<Box<Task>> provides stable addresses and cheap moves (pointer size); possible cache penalty. If you rarely move tasks and want tighter cache locality, Vec<Task> is fine.

---

## Setup Checklist

Verify and extend with emphasis on lifetimes.

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

2. **Run the CLI**  
   ```bash
   cargo run
   ```
   Ensure the CLI runs end-to-end.

> **Lab – Try This:** Run `cargo expand` on a function with lifetimes (install via `cargo install cargo-expand`). Note expanded code.  
> **Solution:** Shows desugared lifetimes. Takeaway: Tooling demystifies.  
> Expected: Expanded impls.

**Debug the Error Mini-Lab (Retention Test):** Modify an iterator to mismatch Item type. Predict error; fix.  
**Solution:** E0308; unify types.

**Self-Assessment:**  
[ ] Verified setup and completed mini-lab.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part I: Lifetimes – Ensuring References Live Long Enough

**You Will Be Able To:**  
- Annotate lifetimes with 'a.  
- Use elision rules.  
- Predict outlive errors.  
- Contrast with C/C++ lifetimes and Python GC.  

**Lifetime Rules (for this session):**  
- References must not outlive owners.  
- 'a ties ref to owner scope.  
- Elision: Inferred in common patterns.  
- 'static: Lives for the program’s duration or type does not carry non-'static refs (e.g., string literals).  

**Lifetime Elision Rules:**  
1. Each reference parameter gets a distinct inferred lifetime.  
2. If there is exactly one input reference, its lifetime is assigned to all output references.  
3. If there are multiple input references but one is &self/&mut self, the output uses self’s lifetime.  

### Core Concept: Case 1 – Basic Lifetime Annotations

**Problem / Motivation:** Dangling refs; C/C++ manual; Python GC hides.

**Definition (Formal):** Lifetime: Scope where ref valid.

**Mental Model (Simplified):** Compiler tracks survival.

**Example (Compilable):** Annotated fn.  
```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}
```

**Code Triple:**  
**Rust (Lifetime):**  
```rust
fn borrow<'a>(s: &'a str) -> &'a str { s }
```  

**C/C++ (Pointer):**  
```cpp
const char* borrow(const char* s) { return s; } // manual check
```  

**Python (Ref):**  
```python
def borrow(s): return s  # GC manages
```

**Rust Failure Variant:** Dangling ref.  
```rust
fn dangling() -> &str { let s = "temp".to_string(); &s }
fn main() {}
```

**Compiler Output (Key lines; messages may vary):**  
```
error[E0515]: cannot return reference to local variable `s`
 --> src/main.rs:1:24
  |
1 | fn dangling() -> &str { let s = "temp".to_string(); &s }
  |                         ^^^^^^^^^^^^^^^^^^^^^^^^^^ returns a reference to a variable which is dropped here
```

Error code: E0515.

**Compiler Reasoning Steps:**  
- Tracks s drop at block end.  
- Rejects return beyond.

**Analysis:**  
- Ownership impact: Borrows tied to owner.  
- Performance: Compile only.  
- Typical: E0515.

**ASCII Diagram: Lifetime Scope**  
```
fn foo<'a>(x: &'a T) -> &'a T {
  // 'a starts here
  x  // valid within 'a
}  // 'a ends
```

**Micro-Challenge Variations:** Predict: Elision in fn(&T) -> &T.  

**Solution to Micro-Challenge:** Inferred as <'a>.  
```rust
fn id(x: &str) -> &str { x }
// desugared to:
fn id<'a>(x: &'a str) -> &'a str { x }
```

**Contrast:** C++ use-after-free; Python no issue.  

**Takeaway:** Lifetimes prevent dangles.

> **Lab – Try This:** Add lifetime to fn returning slice.  
> **Solution:** fn head<'a>(v: &'a [i32]) -> Option<&'a i32> { v.first() } Accepting &[T] is strictly more general than &Vec<T>.

### Core Concept: Case 2 – Lifetime Subtyping and Variance

**Problem / Motivation:** Complex borrows; variance mismatches.

**Definition (Formal):** Lifetime outlives / subtyping: 'static outlives every lifetime. Therefore, &'static T can be used where &'a T is required, but not vice versa.

**Mental Model (Simplified):** Refs flexible in scopes.

**Example (Compilable):** Subtype.  
```rust
fn hold<'a>(s: &'a str) -> &'a str { s }
let s_static: &'static str = "hi";
let s_short: &str = hold(s_static); // 'static → 'a (shorter) OK
```

**Code Triple:**  
**Rust (Variance):**  
```rust
struct Ref<'a, T>(&'a T); // covariant
```  

**C/C++ (Const):**  
```cpp
const char* ref = "str"; // manual
```  

**Python (N/A):**  
```python
ref = "str"  # no explicit
```

**Rust Failure Variant:** Outlive.  
```rust
fn outlive<'a>() -> &'a str { "local" }
fn main() {}
```

**Compiler Output:** E0515 (outlives).

**Analysis:**  
- Ownership impact: Borrows respect.  
- Performance: None.  
- Typical: E0106.

**Variance & PhantomData (Precision)**  
- &'a T is covariant in 'a and T.  
- Cell<T> and RefCell<T> are invariant in T.  
- Adding PhantomData<&'a T> makes your type covariant in 'a; PhantomData<Cell<&'a T>> makes it invariant in 'a; PhantomData<fn(T) -> ()> makes it contravariant in T.  
When you actually need this: custom collections and FFI only; discourage casual use.

**Example (Compilable):** Phantom.  
```rust
use std::cell::Cell;
use std::marker::PhantomData;

struct Covariant<'a, T>(PhantomData<&'a T>);            // covariant in 'a and T
struct Invariant<'a, T>(PhantomData<Cell<&'a T>>);       // invariant in 'a
struct Contravariant<T>(PhantomData<fn(T) -> ()>);       // contravariant in T
```

**Rust Failure Variant:** Shorter borrow in Cell.  
```rust
use std::cell::Cell;
let c: Cell<&'static str> = Cell::new("static");
let short = String::from("short");
c.set(short.as_str()); // E0308: &'short str not assignable to &'static str
fn main() {}
```

**Compiler Output:** E0308 (mismatch).

**Analysis:**  
- Ownership impact: Invariant prevents.  
- Performance: None.  
- Typical: E0308.

**Takeaway:** Variance safe.

> **Lab – Try This:** Fix outlive with 'static.  
> **Solution:** &'static str = "const";

**Lab: Variance Fail→Fix**  
Start with Cell<&'static str> misuse; show E0308; fix by loosening expectation or removing Cell. If you need covariance on a wrapper type, prefer storing a reference (&'a T) or using PhantomData<&'a T>. If the type must own T, accept invariance or redesign the API to avoid assuming subtyping relations.

### Core Concept: Case 3 – NLL & Reborrowing Patterns

**Problem / Motivation:** Borrow ends before scope.

**Definition (Formal):** NLL: Non-Lexical Lifetimes – Precise borrow tracking.

**Mental Model (Simplified:** Borrows last to last use.

**Example (Compilable):** NLL.  
```rust
let mut v = vec![1,2,3];
let r = &v[0];       // immutable borrow
println!("{r}");      // last use of r here
v.push(4);           // ok under NLL; immutable borrow ended before this line
```

**Rust Failure Variant:** Borrow lives long.  
```rust
let mut v = vec![1,2,3];
let r = &v[0];
v.push(4);          // error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
println!("{r}");
fn main() {}
```

**Compiler Output:** E0502 (borrow later used).

**Analysis:**  
- Ownership impact: Early release.  
- Performance: None.  
- Typical: E0502.

**Takeaway:** Precise borrows.

> **Lab – Try This:** Fix borrow with scope.  
> **Solution:** { let r = &v; ... }

### Core Concept: Case 4 – Lifetime Ergonomics for Iterators

**Problem / Motivation:** Borrow in chains; owning vs borrowing iterators.

**Definition (Formal):** Borrowed iter borrows self.

**Mental Model (Simplified):** Align lifetimes with iters.

**Example (Compilable):** Borrowed vs owning.  
```rust
pub fn iter_names<'a>(&'a self) -> impl Iterator<Item=&'a str> + 'a { self.items.iter().map(|x| x.name.as_str()) }
pub fn into_names(self) -> impl Iterator<Item=String> { self.items.into_iter().map(|x| x.name) }
```

**Rust Failure Variant:** Borrow outlives.  
```rust
let it = self.iter_names(); drop(self); it.next(); // E0597
fn main() {}
```

**Compiler Output:** E0597 (borrow outlives).

**Analysis:**  
- Ownership impact: Borrow locks.  
- Performance: No copy.  
- Typical: E0597.

**Takeaway:** Choose borrow/own.

> **Lab – Try This:** Fix E0597 storing iter.  
> **Solution:** Use owning variant.

### Core Concept: Case 5 – HRTB where it matters (for<'a>)

**Problem / Motivation:** Generic borrows across adapters.

**Definition (Formal):** HRTB: Higher-Ranked Trait Bounds – For any 'a.

**Mental Model (Simplified):** Closure accepts any 'a.

**Example (Compilable):** HRTB.  
```rust
fn visit_all<T>(v: &[T], mut f: impl for<'a> FnMut(&'a T)) {
    for item in v { f(item); }
}
```

**Analysis:**  
- Ownership impact: Flexible borrow.  
- Performance: None.  
- Typical: No error.

**Takeaway:** Generic closures. Without for<'a>, closures capturing shorter borrows may fail to type-check (non-higher-ranked).

> **Lab – Try This:** Use HRTB in callback.  
> **Solution:** impl for<'a> FnMut

**Part I Checkpoint:** Lifetimes for?  
**Answers:** Ref validity.

**You Can Now:**  
- Annotate lifetimes.  
- Use elision/'static.

**Part I Quiz:** (5 MCQs + 1 open conceptual question)  
1. What does 'a mean? (a) Scope (b) Type (c) Value  
   Answer: (a)  
2. True/False: Elision always.  
   Answer: False  
3. What causes E0515? (a) Dangling (b) Mismatch (c) Move  
   Answer: (a)  
4. 'static for? (a) Temp (b) Eternal (c) Mutable  
   Answer: (b)  
5. True/False: Subtyping shortens.  
   Answer: True  
Open Conceptual: Explain variance.  
Answer: Ref flexibility.  
Design Question: You need to return a view of internal data without cloning. Provide two API shapes: borrowed &[T] and iterator; discuss pros/cons re: locking and lifetime propagation.

**Self-Assessment:**  
[ ] Annotated lifetimes.  
[ ] Fixed E0515.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Compile-Fail Mini-Labs (Retention + Rigor)  
1. Missing Lifetime (E0106)  
   ```rust
   fn no_lifetime(s: &str) -> &str { s } // E0106
   fn main() {}
   ```  
2. Return Local Ref (E0515)  
   ```rust
   fn dangling() -> &str { let s = "temp".to_string(); &s }
   fn main() {}
   ```  
3. Iter Outlives Self (E0597)  
   ```rust
   struct S { items: Vec<String> }
   impl S {
       fn iter_names<'a>(&'a self) -> impl Iterator<Item = &'a str> {
           self.items.iter().map(|x| x.as_str())
       }
   }
   fn main() {
       let s = S { items: vec!["a".into()] };
       let it = s.iter_names();
       drop(s);
       let _ = it.next(); // E0597
   }
   ```  

**Migration Note:** C++ raw pointer returns can dangle at runtime; Python GC hides issues. Rust catches at compile-time (e.g., E0515), forcing owned or borrowed APIs.

**Final Takeaway:** Lifetimes prevent dangling references at compile time.

**Glossary Appendix Update:** Add: Lifetime, 'a, Elision, NLL, HRTB, Variance.

**Error Code Index:**  
| Code   | Description                     | Example Case |
|--------|---------------------------------|--------------|
| E0515  | Cannot return ref to local      | Dangling |
| E0106  | Missing lifetime specifier      | No 'a |
| E0597  | Borrow outlives owner           | Scope borrow |
| E0502  | Borrow later used               | NLL violation |
| E0308  | Mismatched types                | Variance mismatch |

**Primary References:** Rust Book Ch. 10 (Lifetimes).

**Suggested Deep Dives:** Variance RFCs.

**Concept Map:** (Text-based ASCII)  
Lifetimes ('a)  
  ├── Annotation/Elision  
  ├── NLL/Reborrowing  
  └── Subtyping/Variance  

**Self-Assessment:**  
[ ] Reviewed map/quiz.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

**Deep Dive Appendix:**  
- Lifetime elision: Three rules for fns.  
- Deref coercion: Box to &T (preview for 8B).

**“Done Means Done” Checklist**  
- Correctness: No threads/async; variance explained precisely.  
- Tests: trybuild suite for E0106/E0515/E0597; doctests for lifetime elision.  
- Docs: NLL examples; variance with "when needed" note.  
