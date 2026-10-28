# Session 6: Generics and Traits – Reusable and Extensible Code

**Target Audience & Scope:** This series assumes familiarity with C/Python, basic memory models (e.g., stack/heap, pointers/references, GC internals), and command-line tools. It targets programmers with systems or dynamic language experience new to Rust. Tone balances explanation for beginners in Rust but avoids over-simplifying semantics for intermediates.

**Prerequisites:** Session 5 concepts (structs, enums, Option/Result, error handling, testing); Task Manager v4 with richer types and tests.

**Conceptual Learning Goals:**  
- Understand generics for writing flexible, type-safe code that works with multiple types.  
- Use traits to define shared behaviors and achieve polymorphism without inheritance.  
- Apply trait bounds and where clauses to constrain generics.  

**Mechanical Learning Goals:**  
- Define generic functions, structs, and enums with type parameters.  
- Define and implement traits for custom types.  
- Use trait bounds in generics and where clauses for constraints.  
- Read and fix errors related to generic type mismatches or unsatisfied bounds.  

**Design Learning Goals:**  
- Extend the Task Manager with generic data structures and trait-based APIs for extensibility.  
- Design polymorphic code using traits instead of enums for open extension.  
- Test generic code with concrete types and mock implementations.

**By the End of This Session, You Can:**  
- Define and use generics in functions and types.  
- Define traits and implement them for types.  
- Apply trait bounds and where clauses.  
- Design extensible APIs with traits.  
- Fix generic-related compiler errors.  
- Extend CLI with generics and traits.

**Project Narrative:** Building on the type-safe modeling from Session 5, enhance Task Manager to v5 by introducing generics for flexible storage and traits for command handling, enabling reusable and extensible code.

**Time Estimate:** 60 minutes.

**Error Handling Policy:** Library returns task_core::Result<T> with typed thiserror errors. CLI uses anyhow + .context().

**Safety & Lints:**  
```rust
#![forbid(unsafe_code)]
#![deny(unused_must_use, missing_docs)]
// In CI via clippy:
// -D clippy::unwrap_used -D clippy::expect_used -D clippy::panic -D clippy::missing_errors_doc
```

**MSRV Note:** This session uses GATs (MSRV ≥1.65). Add rust-version = "1.65" to Cargo.toml and create rust-toolchain.toml with:  
```
[toolchain]
channel = "stable"
```

**Decision Framework: Enum vs Generics vs Trait vs dyn**  
- Closed set of variants now → enum.  
- Open set; performance / inlining → generics (<T: Trait> / impl Trait).  
- Open set; plugins/runtime composition / smaller binary → Box<dyn Trait + Send + Sync + 'static>.  
- Want related types on the behavior → trait with associated types.  
- Need heterogeneous collections → trait object (dyn) and ensure object safety.

**Anti-Patterns to Avoid**  
- Wide public generic APIs that explode monomorphized code; prefer dyn at boundaries.  
- Traits with generic methods you later want as trait objects (object-safety blocker).  
- Blanket impls with broad bounds that preclude future impls.  
- Foreign trait for foreign type (orphan rule): always newtype.  
- Leaking internal type params in public signatures; prefer impl Trait in args.  
- Generic methods in traits you plan to use as trait objects.

**Public API Policy**  
- Use impl Trait in parameters on public fns.  
- Do not leak generic params unnecessarily; avoid pub struct Foo<T> unless T is part of the model.  
- No impl Trait in trait methods (disallowed on MSRV); prefer associated types.

**Dispatch Policy**  
- Static (<T: Trait>) inside task_core.  
- Dynamic (dyn Trait) in task_cli and plugin/FFI boundaries.  
- If size blows up or compile times spike, move hot public APIs to dyn and enable ThinLTO in release.

**Perf and Binary Size Guidance**  
Generics are zero-cost per call, but monomorphization can bloat binaries if public APIs are overly generic. Prefer dyn at integration/plugin boundaries; use ThinLTO for size; avoid templating hot public functions with many type parameters.

---

## Setup Checklist

Verify and extend with focus on generics and traits.

1. **Verify Existing Setup**  
   ```bash
   cargo --version
   rustc --version
   cargo fmt
   cargo clippy -- -D warnings
   cargo test
   cargo test --doc
   ```
   Expect recent versions; update with `rustup update`. Confirm rust-analyzer (hover for types and bounds).

2. **Install and Use Clippy** (if not already)  
   ```bash
   rustup component add clippy
   cargo clippy -- -D warnings
   ```
   Lints for idiomatic code, e.g., missing bounds.

3. **Add Dependencies for Testing**  
   ```bash
   cargo add proptest --dev
   cargo add trybuild --dev
   ```

4. **Run Your Session 5 CLI**  
   ```bash
   cargo run
   ```
   Ensure Task Manager v4 works.

> **Lab – Try This:** Run `cargo clippy -- -D warnings` on your code. Apply suggestions.  
> **Solution:** Clippy flags issues; fix and re-run. Takeaway: Enforces bounds in generics.  
> Expected: Warnings like "missing trait bound".

**Mini-Lab: Trait-Bound Errors in Generics (E0277)**: Modify a generic function to lack a bound (e.g., use + without Add). Predict error; fix with bound.  
**Solution:** E0277 (trait bound not satisfied); add <T: Add>.

**Self-Assessment:**  
[ ] Verified setup and completed mini-lab.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

**Time Estimate:** 15 minutes.

---

## Part I: Generics – Flexible, Reusable Code

**You Will Be Able To:**  
- Define generics with type parameters.  
- Use generics in functions and types.  
- Contrast with C++ templates and Python typing.

**Time Estimate:** 15 minutes.

### Core Concept: Case 1 – Generic Functions

**Problem / Motivation:** Duplicate code for types; C++ templates heavy; Python dynamic no checks.

**Definition (Formal):** Generics: Type parameters <T> for abstract types.

**Mental Model (Simplified):** Placeholder for types; monomorphized at compile.

**Example (Compilable):** Generic function.  
```rust
fn identity<T>(value: T) -> T {
    value
}
```

**Code Triple:**  
**Rust (Compile-time):**  
```rust
fn sum<T: std::ops::Add<Output = T>>(a: T, b: T) -> T { a + b }
```  

**C/C++ (Template):**  
```cpp
template <typename T> T sum(T a, T b) { return a + b; }
```  

**Python (Dynamic):**  
```python
def sum(a, b): return a + b
```

**Rust Failure Variant:** No bound for op.  
```rust
fn sum<T>(a: T, b: T) -> T { a + b }
```

**Compiler Output (Key lines; messages may vary):**  
```
error[E0277]: cannot add `T` to `T`
```  
Error code: E0277.

**Compiler Reasoning Steps:**  
- T no Add.  
- + requires Add.  
- Rejects.

**Analysis:**  
- Ownership impact: T owns if moved.  
- Performance: Monomorphization O(1); can bloat binary—use dyn for trade-off.  
- Typical compiler error: E0277 (bound not satisfied).

**ASCII Diagram: Generic Expansion**  
```
fn sum<i32>(a: i32, b: i32) -> i32
fn sum<f64>(a: f64, b: f64) -> f64
```

**Micro-Challenge Variations:** Predict: Call with String.  

**Solution to Micro-Challenge:** E0277; add bound or impl Add for String.

**Contrast:** C++ SFINAE; Python runtime error.

**Takeaway:** Generics reuse with safety.

> **Lab – Try This:** Define generic sum; call with i32/f64.  
> **Solution:** Add bound; compiles.

[Design] **Reflection – Think:** Generics vs duplication?  
[Answer] **Model Answer:** Reuse, safety.

[Semantics] **Think like the Compiler:** What for unbound T? (Answer: E0277.)

### Core Concept: Case 2 – Generic Types

**Problem / Motivation:** Type-specific structs; generics generalize.

**Definition (Formal):** Struct< T > with fields of T.

**Mental Model (Simplified):** Parametric types.

**Example (Compilable):** Generic struct.  
```rust
#[derive(Default, Debug, Clone)]
pub struct IdMap<K, V> {
    inner: std::collections::BTreeMap<K, V>,
}

impl<K: Ord, V> IdMap<K, V> {
    pub fn insert(&mut self, k: K, v: V) -> Option<V> { self.inner.insert(k, v) }
    pub fn get(&self, k: &K) -> Option<&V> { self.inner.get(k) }
    pub fn iter(&self) -> impl Iterator<Item = (&K, &V)> { self.inner.iter() }
}
```

**Code Triple:**  
**Rust:**  
```rust
struct IdMap<K, V> { inner: BTreeMap<K, V> }
```  

**C/C++:**  
```cpp
template <typename K, typename V> struct IdMap { std::map<K, V> inner; };
```  

**Python:**  
```python
class IdMap: def __init__(self): self.inner = {}
```

**Rust Failure Variant:** Mismatched T.  
```rust
let m = IdMap::default();
m.insert(1, "s"); // If K=i32, V=String ok; mismatched would fail at call
```

**Compiler Output (Key lines; messages may vary):**  
```
error[E0308]: mismatched types
```  
Error code: E0308.

**Compiler Reasoning Steps:**  
- Types must match.  
- Differ.  
- Rejects.

**Analysis:**  
- Ownership impact: Owns K,V.  
- Performance: No overhead.  
- Typical compiler error: E0308.

**ASCII Diagram: N/A**

**Micro-Challenge Variations:** Predict: Use with TaskId, Task.  

**Solution to Micro-Challenge:** Ok if Ord impl.

**Contrast:** C++ multi-template; Python any.

**Takeaway:** Generalize structures.

> **Lab – Try This:** Define IdMap; use with types.  
> **Solution:** Insert/get.

[Design] **Reflection – Think:** When multi generics?  
[Answer] **Model Answer:** Different types.

[Semantics] **Think like the Compiler:** What for mismatched? (Answer: E0308.)

**Part I Checkpoint:** Generics for? Bounds?  
**Answers:** Reuse. Constraints.

**You Can Now:**  
- Define generics.  
- Use in functions/types.

**Part I Quiz:** (5 MCQs + 1 open conceptual question)  
1. Generics use? (a) <T> (b) [T] (c) {T}  
   Answer: (a)  
2. Bounds for? (a) Ops (b) Any (c) None  
   Answer: (a)  
3. True/False: Monomorphized.  
   Answer: True  
4. Performance? (a) Runtime (b) Compile (c) Both  
   Answer: (b)  
5. True/False: Multi params ok.  
   Answer: True  
Open Conceptual: Explain generics vs dynamic.  
Answer: Compile safe.

**Self-Assessment:**  
[ ] Defined generic function/type.  
[ ] Fixed bound error.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part II: Traits – Defining Shared Behaviors

**You Will Be Able To:**  
- Define traits.  
- Impl traits for types.  
- Contrast with C++ interfaces, Python protocols.

**Time Estimate:** 15 minutes.

### Core Concept: Case 1 – Trait Basics

**Problem / Motivation:** Common behaviors; no inheritance.

**Definition (Formal):** Trait: Interface with methods.

**Mental Model (Simplified):** Contract for types.

**Example (Compilable):** Trait definition.  
```rust
trait Displayable {
    fn display(&self) -> String;
}
```

**Code Triple:**  
**Rust:**  
```rust
impl Displayable for Task { fn display(&self) -> String { format!("Task: {}", self.title) } }
```  

**C/C++ (Virtual):**  
```cpp
class Displayable { virtual std::string display() = 0; };
```  

**Python (Protocol):**  
```python
class Displayable: def display(self): pass
```

**Rust Failure Variant:** No impl.  
```rust
let t: Task = ...;
t.display();
```

**Compiler Output (Key lines; messages may vary):**  
```
error[E0599]: no method named `display` found for type `Task`
```  
Error code: E0599.

**Compiler Reasoning Steps:**  
- Type no impl.  
- Method call.  
- Rejects.

**Analysis:**  
- Ownership impact: Methods borrow self.  
- Performance: Static dispatch default.  
- Typical compiler error: E0599.

**ASCII Diagram: N/A**

**Micro-Challenge Variations:** Predict: Impl for multiple.  

**Solution to Micro-Challenge:** Yes; traits multi-impl.

**Contrast:** C++ virtual runtime; Python duck.

**Takeaway:** Traits polymorphism.

> **Lab – Try This:** Define Displayable; impl for Task.  
> **Solution:** Call display.

[Design] **Reflection – Think:** Traits vs inheritance?  
[Answer] **Model Answer:** Composition.

[Semantics] **Think like the Compiler:** What for no impl? (Answer: E0599.)

### Core Concept: Case 2 – Default Methods and Associated Types

**Definition (Formal):** Default impl; associated types.

**Mental Model (Simplified):** Optional methods; associated types.

**Example (Compilable):** Default.  
```rust
trait Logger {
    fn log(&self, msg: &str) { println!("{}", msg); }
}
```

**Code Triple:**  
**Rust:**  
```rust
trait Iterator { type Item; fn next(&mut self) -> Option<Self::Item>; }
```  

**C/C++:**  
```cpp
template<class T> class Iterator { typedef T value_type; virtual value_type next() = 0; };
```  

**Python:**  
```python
class Iterator: def next(self): pass
```

**Rust Failure Variant:** No assoc type.  

**Compiler Output (Key lines; messages may vary):** N/A (ok if no need).

**Analysis:**  
- Ownership impact: Assoc own.  
- Performance: Flexible.  
- Typical: E0191 if missing.

**ASCII Diagram: N/A**

**Micro-Challenge Variations:** Predict: Override default.  

**Solution to Micro-Challenge:** Yes.

**Contrast:** C++ default virtual; Python none.

**Takeaway:** Defaults ease; assoc generalize.

> **Lab – Try This:** Define trait with default; impl override.  
> **Solution:** Custom log.

[Design] **Reflection – Think:** Assoc types when?  
[Answer] **Model Answer:** Related types.

[Semantics] **Think like the Compiler:** What for missing assoc? (Answer: E0191.)

**Part II Checkpoint:** Traits for? Defaults?  
**Answers:** Behaviors. Optional.

**You Can Now:**  
- Define/impl traits.  
- Use defaults/assoc.

**Part II Quiz:** (5 MCQs + 1 open conceptual question)  
1. Traits define? (a) Data (b) Behaviors (c) Both  
   Answer: (b)  
2. Impl for? (a) One type (b) Many (c) None  
   Answer: (b)  
3. True/False: Defaults optional.  
   Answer: True  
4. Assoc types for? (a) Methods (b) Related types (c) Bounds  
   Answer: (b)  
5. True/False: Runtime dispatch default.  
   Answer: False  
Open Conceptual: Explain traits vs classes.  
Answer: Interfaces no data.

**Self-Assessment:**  
[ ] Defined trait/impl.  
[ ] Used default.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part III: Trait Bounds and Where Clauses – Constraining Generics

**You Will Be Able To:**  
- Use trait bounds in generics.  
- Apply where clauses for complex constraints.  
- Contrast with C++ concepts.

**Time Estimate:** 15 minutes.

### Core Concept: Case 1 – Trait Bounds

**Problem / Motivation:** Unconstrained generics limited.

**Definition (Formal):** <T: Trait> requires impl Trait.

**Mental Model (Simplified):** Ensure capabilities.

**Example (Compilable):** Bound.  
```rust
fn print<T: std::fmt::Display>(value: T) {
    println!("{}", value);
}
```

**Code Triple:**  
**Rust:**  
```rust
<T: Add<Output = T>>
```  

**C/C++:**  
```cpp
template <std::integral T> T sum(T a, T b);
```  

**Python:**  
```python
def sum(a, b): return a + b  // Runtime
```

**Rust Failure Variant:** No bound.  
```rust
fn print<T>(value: T) { println!("{}", value); }
```

**Compiler Output (Key lines; messages may vary):**  
```
error[E0277]: `T` doesn't implement `std::fmt::Display`
```  
Error code: E0277.

**Compiler Reasoning Steps:**  
- {} needs Display.  
- T no bound.  
- Rejects.

**Analysis:**  
- Ownership impact: Bounds on T.  
- Performance: Static.  
- Typical compiler error: E0277.

**ASCII Diagram: N/A**

**Micro-Challenge Variations:** Predict: Multi bounds.  

**Solution to Micro-Challenge:** T: Trait1 + Trait2.

**Contrast:** C++ concepts; Python no.

**Takeaway:** Bounds safety.

> **Lab – Try This:** Add Display bound; call.  
> **Solution:** Works for impl Display.

[Design] **Reflection – Think:** Bounds vs any?  
[Answer] **Model Answer:** Compile checks.

[Semantics] **Think like the Compiler:** What for no bound? (Answer: E0277.)

### Core Concept: Case 2 – Where Clauses

**Definition (Formal):** Where for complex.

**Mental Model (Simplified):** Separate constraints.

**Example (Compilable):** Where.  
```rust
fn complex<T, U>(a: T, b: U) where T: Display, U: Clone {}
```

**Code Triple:**  
**Rust:**  
```rust
where T: Trait
```  

**C/C++:**  
```cpp
requires std::integral<T>
```  

**Python:**  
N/A

**Rust Failure Variant:** Missing where.  

**Compiler Output (Key lines; messages may vary):** Ok if simple.

**Analysis:**  
- Ownership impact: Same.  
- Performance: N/A.  
- Typical: Readability.

**ASCII Diagram: N/A**

**Micro-Challenge Variations:** Predict: Multi where.  

**Solution to Micro-Challenge:** Yes.

**Contrast:** C++ requires; Python none.

**Takeaway:** Where clarity.

> **Lab – Try This:** Use where for multi.  
> **Solution:** Complex signatures.

[Design] **Reflection – Think:** When where?  
[Answer] **Model Answer:** Long bounds.

[Semantics] **Think like the Compiler:** What for unsatisfied? (Answer: E0277.)

**Part III Checkpoint:** Bounds for? Where?  
**Answers:** Constraints. Complex.

**You Can Now:**  
- Use bounds/where.

**Part III Quiz:** (5 MCQs + 1 open conceptual question)  
1. Bounds use? (a) :Trait (b) =Trait (c) &Trait  
   Answer: (a)  
2. Where for? (a) Simple (b) Complex (c) None  
   Answer: (b)  
3. True/False: Multi bounds +.  
   Answer: True  
4. Error for no bound? (a) E0277 (b) E0308 (c) E0599  
   Answer: (a)  
5. True/False: Runtime check.  
   Answer: False  
Open Conceptual: Explain bounds benefit.  
Answer: Safety/reuse.

**Self-Assessment:**  
[ ] Used bounds/where.  
[ ] Fixed E0277.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part IV: Application and Testing with Generics/Traits

**You Will Be Able To:**  
- Apply generics/traits in project.  
- Test generic code.  

**Time Estimate:** 15 minutes.

### Core Concept: Generics and Traits in Practice

**Example (Compilable):** Trait for commands.  
```rust
// --- Prelude (place once before any code that uses Task*/Result) ---
pub type Result<T> = std::result::Result<T, Error>;

#[derive(thiserror::Error, Debug)]
pub enum Error {
    #[error("not found: {0:?}")]
    NotFound(TaskId),
    #[error(transparent)]
    Io(#[from] std::io::Error),
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub struct TaskId(std::num::NonZeroU32);

#[derive(Debug, Clone)]
pub struct Task { pub id: TaskId, pub title: String }

pub trait TaskStore {
    type Key: Eq + Ord + Clone;
    type Value: Clone;
    type Iter<'a>: Iterator<Item = &'a Self::Value> where Self: 'a;

    fn insert(&mut self, key: Self::Key, value: Self::Value) -> Result<()>;
    fn get(&self, key: &Self::Key) -> Option<&Self::Value>;
    fn get_mut(&mut self, key: &Self::Key) -> Option<&mut Self::Value>;
    fn list(&self) -> Self::Iter<'_>;
}

pub fn next_id<S>(s: &S) -> Result<TaskId>
where
    S: TaskStore<Key = TaskId, Value = Task>,
{
    let max = s.list().map(|t| t.id.0.get()).max().unwrap_or(0);
    let next = max.checked_add(1).ok_or_else(|| std::io::Error::from(std::io::ErrorKind::Other))?;
    let nz = std::num::NonZeroU32::new(next).ok_or_else(|| std::io::Error::from(std::io::ErrorKind::Other))?;
    Ok(TaskId(nz))
}
// --- End Prelude ---

// Static: performance inside task_core
pub trait CommandHandler<S: TaskStore> {
    type Output;
    fn handle(&self, store: &mut S) -> Result<Self::Output>;
}

// Dynamic: open extension at CLI/plugin boundary
pub trait DynCommandHandler: Send + Sync {
    fn handle_dyn(&self, store: &mut dyn TaskStore<Key = TaskId, Value = Task>) -> Result<()>;
}

pub struct AddCmd { pub title: String }

impl<S: TaskStore<Key = TaskId, Value = Task>> CommandHandler<S> for AddCmd {
    type Output = ();
    fn handle(&self, store: &mut S) -> Result<Self::Output> {
        let id = next_id(store)?;
        let t  = Task { id, title: self.title.clone() };
        store.insert(t.id.clone(), t)
    }
}

impl DynCommandHandler for AddCmd {
    fn handle_dyn(&self, store: &mut dyn TaskStore<Key = TaskId, Value = Task>) -> Result<()> {
        let id = next_id(store)?;
        let t  = Task { id, title: self.title.clone() };
        store.insert(t.id.clone(), t)
    }
}
```

**Code Triple:**  
**Rust:**  
```rust
impl CommandHandler for AddCommand { ... }
```  

**C/C++:**  
```cpp
class CommandHandler { virtual void handle() = 0; };
```  

**Python:**  
```python
class CommandHandler: def handle(self): pass
```

**Analysis:**  
- Ownership impact: Borrow store.  
- Performance: Static.  
- Typical: E0277 if unbound.

**Takeaway:** Extensible APIs.

> **Lab – Try This:** Define trait; impl for command.  
> **Solution:** Handle calls.

**Part IV Checkpoint:** Application for?  
**Answers:** Reuse/extension.

**You Can Now:**  
- Apply in project.  
- Test generics.

**Part IV Quiz:** (5 MCQs + 1 open conceptual question)  
1. Traits with generics? (a) Yes (b) No (c) Sometimes  
   Answer: (a)  
2. Test generics with? (a) Concrete (b) Abstract (c) None  
   Answer: (a)  
3. True/False: Traits data.  
   Answer: False  
4. Bounds performance? (a) Runtime (b) Compile (c) Both  
   Answer: (b)  
5. True/False: Where required.  
   Answer: False  
Open Conceptual: Explain static vs dynamic dispatch.  
Answer: Compile vs runtime.

**Self-Assessment:**  
[ ] Applied in CLI.  
[ ] Tested generics.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Exercises: Tiered Reasoning

### Tier 1: Concept Rebuilds

1. Generic Fn  
   Identity<T>.  
   **Solution:** fn identity<T>(v: T) -> T { v }

2. Trait Def  
   Printable.  
   **Solution:** trait Printable { fn print(&self); }

### Tier 2: Comparative Rewrites

1. C Template to Rust Generic  
   Sum.  
   **Solution:** fn sum<T: Add>(a: T, b: T) -> T::Output

2. Python Class to Trait  
   Interface.  
   **Solution:** Trait with methods.

### Tier 3: Challenge Extensions

1. Bounded Generic  
   Display list.  
   **Solution:** fn print_list<T: Display>(list: &[T])

2. Trait Impl  
   For custom type.  
   **Solution:** impl Trait for Type { ... }

**Self-Assessment:**  
[ ] Completed one per tier.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Recap and Synthesis Reflection

**Table Completion Exercise:**  
| Rust Feature | C/C++ Issue | Python Trade-off |
|--------------|-------------|------------------|
| Generics | Template errors | Dynamic no checks |
| Traits | Virtual overhead | Duck typing runtime |
| Bounds | SFINAE complex | No constraints |

**Self-Quiz:** (Design-level)  
1. Generics purpose?  
2. Traits for?  
3. Bounds error?  
Answers:  
1. Reuse.  
2. Behaviors.  
3. E0277.

**Final Takeaway:** Generics/traits flexible safe code.

**By Session End:**  
- Define/use generics.  
- Define/impl traits.  
- Apply bounds/where.  
- Design trait APIs.  
- Fix generic errors.  
- Extend CLI with generics/traits.

**Glossary Appendix Update:** Add: Generic, Type parameter, Trait, Bound, Where clause.

**Error Code Index:**  
| Code   | Description                     | Example Case |
|--------|---------------------------------|--------------|
| E0277  | Trait bound not satisfied       | No impl |
| E0308  | Mismatched types                | Generic mismatch |
| E0599  | Method not found                | No impl |
| E0191  | Assoc type not found            | Missing assoc |
| E0038  | Trait not object safe           | Trait object fail |
| E0117  | Only one impl for trait         | Orphan rule |

**Primary References:** Rust Book Ch. 10 (Generics/Traits/Lifetimes).

**Suggested Deep Dives:** Associated types; dyn Trait dispatch.

**Concept Map:** (Text-based ASCII)  
Generics (<T>)  
  ├── Functions/Types  
  └── Bounds (:Trait)  
Traits (interface)  
  ├── Impl  
  └── Defaults/Assoc  
Applied (Task v5)

**Bridge to Session 7:** Generics/traits to modules/iterators.

**Self-Assessment:**  
[ ] Reviewed map/quiz.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

**Deep Dive Appendix:**  
- Static vs dyn dispatch: Compile vs vtable.  
- Orphan rules: Impl coherence.