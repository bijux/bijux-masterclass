# Session 5: Structs, Enums, Option/Result, Error Handling + Testing – Type-Safe Data Modeling

**Target Audience & Scope:** This series assumes familiarity with C/Python, basic memory models (e.g., stack/heap, pointers/references, GC internals), and command-line tools. It targets programmers with systems or dynamic language experience new to Rust. Tone balances explanation for beginners in Rust but avoids over-simplifying semantics for intermediates.

**Prerequisites:** Session 4 concepts (borrowing, references, slices, lifetime intuition); Task CLI v3 with borrowed APIs.

**Conceptual Learning Goals:**  
- Model domain data using structs and enums for type safety, emphasizing sum types, newtypes, and invariants.  
- Represent optional values and errors with Option and Result, propagating explicitly without exceptions.  
- Integrate testing to validate types, invariants, and error paths, including table-driven and property-based approaches.  

**Mechanical Learning Goals:**  
- Define structs with methods, enums with variants, and newtypes for safety.  
- Use combinators like map/and_then on Option; ? on Result with precise error types.  
- Write unit tests with assert macros, table-driven cases, and integration tests.  
- Read and fix errors related to type mismatches, unhandled Results, or invariant violations.

**Design Learning Goals:**  
- Extend the CLI with richer types, explicit error boundaries (library vs CLI), and testable APIs.  
- Choose between Option for absence and Result for failures, avoiding anti-patterns like unwrap in library code.  
- Design side-effect-free core logic with traits for isolation and testing.

**By the End of This Session, You Can:**  
- Model data with structs, enums, and newtypes enforcing invariants.  
- Use Option/Result for absence and errors, propagating with ?.  
- Define error policies: thiserror for library, anyhow for CLI.  
- Write advanced tests: table-driven, property-based, integration.  
- Fix type mismatch/unhandled errors/invariant violations.  
- Extend CLI with typed parsing and testable storage.

**Project Narrative:** Building on the borrowed access patterns from Session 4, elevate Task Manager to v4, splitting into task_core (lib) for pure logic and task_cli (bin) for I/O. Introduce newtypes and enums for robust modeling, FromStr for parsing, a TaskStore trait for testability, explicit errors with thiserror/anyhow boundaries, and comprehensive tests.

**Time Estimate:** 60 minutes.

**Error Handling Policy:** Library returns task_core::Result<T> with typed thiserror errors. CLI uses anyhow + .context().

**MSRV Note:** This session uses GATs (MSRV ≥1.65). Add rust-version = "1.65" to Cargo.toml and create rust-toolchain.toml with:  
```
[toolchain]
channel = "stable"
```

---

## Setup Checklist

Verify and extend with testing emphasis.

1. **Verify Existing Setup**  
   ```bash
   cargo --version
   rustc --version
   cargo fmt
   cargo clippy
   cargo test
   cargo test --doc
   ```
   Expect recent versions; update with `rustup update`. Confirm rust-analyzer (hover for types).

2. **Install and Use Clippy** (if not already)  
   ```bash
   rustup component add clippy
   cargo clippy
   ```
   Lints for idiomatic code, e.g., unnecessary unwraps.

3. **Add Dependencies for Errors and Testing**  
   ```bash
   cargo add thiserror
   cargo add anyhow
   cargo add proptest --dev  # For property tests
   ```

4. **Restructure Project into Lib and Bin**  
   ```bash
   cargo new --lib task_core
   # Move core logic to task_core/src/lib.rs
   # Create task_cli/src/main.rs that uses task_core
   ```
   Add to task_core/src/lib.rs:  
   ```rust
   #![forbid(unsafe_code)]
   ```
   For CI (optional for now): Set RUSTDOCFLAGS="-D missing-docs" in workflows; RUSTFLAGS="-D unused-must-use"; CLIPPY="-D clippy::unwrap_used -D clippy::expect_used -D clippy::panic".

5. **Run Your Session 4 CLI**  
   ```bash
   cargo run
   ```
   Ensure Task Manager v3 works, then migrate to new structure.

> **Lab – Try This:** Run `cargo clippy` on your code. Apply suggestions (e.g., redundant unwrap).  
> **Solution:** Clippy flags non-idiomatic patterns; fix and re-run. Takeaway: Automated reviewer for safety.  
> Expected: Warnings like "unnecessary unwrap"; help: use ? or match.

**Debug the Error Mini-Lab (Retention Test from Session 4):** Modify a borrowed function to return a dangling slice. Predict error; fix by returning owned data.  
**Solution:** E0515 (cannot return reference to local); return String instead of &str for owned.

**Self-Assessment:**  
[ ] Verified setup and completed mini-lab.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

**Time Estimate:** 15 minutes.

---

## Part I: Structs – Structured Data with Methods and Invariants

**You Will Be Able To:**  
- Define structs with fields, methods, and invariants via Result-returning constructors.  
- Use receivers like &self/&mut self.  
- Contrast with C/C++/Python data modeling.

**Time Estimate:** 15 minutes.

### Core Concept: Case 1 – Struct Basics, Constructors, and Invariants

**Problem / Motivation:** C/C++ structs/classes manual; Python classes dynamic. Rust structs static, with invariants returning errors instead of panicking.

**Definition (Formal):** Struct: Named fields; try_new returns Result<Self> for invariants.

**Mental Model (Simplified):** Group data; enforce rules without panic.

**Example (Compilable):** Struct with invariant.  
```rust
use std::num::NonZeroU32;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TaskId(NonZeroU32);

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Status { Pending, Done }

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Task {
    id: TaskId,
    title: String,
    status: Status,
}

impl Task {
    /// Creates a new task if title is valid.
    ///
    /// # Examples
    ///
    /// ```
    /// use task_core::{Task, TaskId, Result};
    /// use std::num::NonZeroU32;
    /// let id = TaskId(NonZeroU32::new(1).unwrap());
    /// let t: Result<Task> = Task::try_new(id, "Valid".to_string());
    /// assert!(t.is_ok());
    /// ```
    pub fn try_new(id: TaskId, title: String) -> Result<Self> {
        if title.trim().is_empty() {
            return Err(Error::Parse(ParseCommandError::EmptyTitle));
        }
        Ok(Self { id, title, status: Status::Pending })
    }
}
```

**Code Triple:**  
**Rust (Invariant via Result):**  
```rust
pub fn try_new(id: TaskId, title: String) -> Result<Self> { /* check */ }
```  

**C/C++ (Throw):**  
```cpp
Task(int id, std::string title) { if (title.empty()) throw; }
```  

**Python (Raise):**  
```python
def __init__(self, id, title): if not title.strip(): raise ValueError
```

**Rust Failure Variant:** Missing field.  
```rust
let task = Task { id: TaskId(NonZeroU32::new(1).unwrap()), title: "x".to_string() };  // Missing status
```

**Compiler Output (Key lines; messages may vary):**  
```
error[E0063]: missing field `status` in initializer of `Task`
```  
Error code: E0063.

**Compiler Reasoning Steps:**  
- Checks fields: id, title, status.  
- At init: Missing status.  
- Rejects: Ensures complete.

**Analysis:**  
- Ownership impact: Fields own data.  
- Performance: O(1) access.  
- Typical compiler error: E0063 (missing field).

**ASCII Diagram: Struct Layout**  
```
Task {
  id: TaskId (NonZeroU32)
  title: String (ptr, len, cap)
  status: Status (tag)
}
```

**Micro-Challenge Variations:** Predict: Err on empty title.  

**Solution to Micro-Challenge:** Yes; returns Error.

**Contrast:** C++ throw; Python raise (runtime).

**Takeaway:** Invariants via Result prevent panic in library; no direct literals bypassing try_new.

> **Lab – Try This:** Define Task; try_new with invalid title. Handle Err.  
> **Solution:** Match on Result; fix with valid.

[Design] **Reflection – Think:** Result in constructors vs panic?  
[Answer] **Model Answer:** Propagates; no crash.

[Semantics] **Think like the Compiler:** What for field mismatch? (Answer: E0308.)

### Core Concept: Case 2 – Methods with Receivers

**Definition (Formal):** impl: Methods; &self immutable, &mut self mutable.

**Mental Model (Simplified):** Methods borrow instance.

**Example (Compilable):**  
```rust
impl Task {
    pub fn complete(&mut self) { self.status = Status::Done; }
    pub fn is_complete(&self) -> bool { matches!(self.status, Status::Done) }
}
```

**Code Triple:**  
**Rust:**  
```rust
fn complete(&mut self) { self.status = Status::Done; }
```  

**C/C++:**  
```cpp
void complete() { status = Done; }
```  

**Python:**  
```python
def complete(self): self.status = "Done"
```

**Rust Failure Variant:** Mutate immutable.  
```rust
fn complete(&self) { self.status = Status::Done; }
```

**Compiler Output (Key lines; messages may vary):**  
```
error[E0594]: cannot assign to `self.status`
```  
Error code: E0594.

**Compiler Reasoning Steps:**  
- Receiver immutable.  
- Assign needs mut.  
- Rejects.

**Analysis:**  
- Ownership impact: Borrow.  
- Performance: O(1).  
- Typical compiler error: E0594.

**ASCII Diagram: Receiver Borrow**  
```
&self --> immutable
&mut self --> mutable
```

**Micro-Challenge Variations:** Predict: Call mut on immutable binding.  

**Solution to Micro-Challenge:** E0596; add let mut task = ...; task.complete();.

**Contrast:** C++ const; Python no check.

**Takeaway:** Receivers enforce borrowing; mutable binding required for &mut self.

> **Lab – Try This:** Add methods to Task; call on let mut task.  
> **Solution:** E0596 if immutable; add mut.

[Design] **Reflection – Think:** &self default why?  
[Answer] **Model Answer:** Safe immutable.

[Semantics] **Think like the Compiler:** What for move self? (Answer: Reject unless consuming.)

**Part I Checkpoint:** Struct for? Invariants?  
**Answers:** Group data. Via Result.

**You Can Now:**  
- Define structs/methods/invariants.  
- Use receivers.

**Part I Quiz:** (5 MCQs + 1 open conceptual question)  
1. Struct init requires? (a) All fields (b) Some (c) None  
   Answer: (a)  
2. &mut self for? (a) Read (b) Write (c) Own  
   Answer: (b)  
3. True/False: Constructors return Result.  
   Answer: True  
4. Method performance? (a) O(n) (b) O(1) (c) Variable  
   Answer: (b)  
5. True/False: Mutate &self error.  
   Answer: True  
Open Conceptual: Explain Result in constructors.  
Answer: Propagate errors safely.

**Self-Assessment:**  
[ ] Defined struct with invariants.  
[ ] Fixed mutate error.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part II: Enums and Newtypes – Variant Data and Strong Typing

**You Will Be Able To:**  
- Define enums with data and newtypes for safety.  
- Match on variants exhaustively.  
- Contrast with C/C++/Python.

**Time Estimate:** 15 minutes.

### Core Concept: Case 1 – Enum Basics and Sum Types

**Problem / Motivation:** C enums numeric; Python no sum types. Rust enums algebraic for states.

**Definition (Formal):** Enum: Tagged variants; newtype: Wrapper for invariants.

**Mental Model (Simplified):** Enums for choices; newtypes for typed primitives.

**Example (Compilable):** Status enum.  
```rust
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Status { Pending, Done }

impl std::fmt::Display for Status {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", match self {
            Status::Pending => "Pending",
            Status::Done => "Done",
        })
    }
}
```

**Code Triple:**  
**Rust:**  
```rust
enum Status { Pending, Done }
```  

**C/C++:**  
```cpp
enum Status { Pending, Done };  // No data
```  

**Python:**  
```python
Status = Union["Pending", "Done"]  // Dynamic
```

**Rust Failure Variant:** Non-exhaustive.  
```rust
match status {
    Status::Pending => (),
}
```

**Compiler Output (Key lines; messages may vary):**  
```
error[E0004]: non-exhaustive patterns: `Done` not covered
```  
Error code: E0004.

**Compiler Reasoning Steps:**  
- Variants: Pending, Done.  
- Match misses Done.  
- Rejects.

**Analysis:**  
- Ownership impact: Own data.  
- Performance: O(1) match.  
- Typical compiler error: E0004.

**ASCII Diagram: Enum Layout**  
```
Status: tag (Pending | Done)
```

**Micro-Challenge Variations:** Predict: Match Status.  

**Solution to Micro-Challenge:** Exhaustive arms.

**Contrast:** C no data; Python runtime.

**Takeaway:** Sum types prevent invalid.

> **Lab – Try This:** Use Status in Task; match in methods.  
> **Solution:** Replace bool; update is_complete to matches!.

[Design] **Reflection – Think:** Enum vs bool?  
[Answer] **Model Answer:** Explicit states.

[Semantics] **Think like the Compiler:** What for missing arm? (Answer: E0004.)

### Core Concept: Case 2 – Data-Carrying Variants and Newtypes

**Definition (Formal):** Variants hold types; newtype wraps for safety.

**Mental Model (Simplified):** Tag union; newtype adds methods/invariants.

**Example (Compilable:**)  
```rust
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Command {
    Add { title: String },
    Complete { id: TaskId },
    List,
}

impl std::fmt::Display for TaskId {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl std::str::FromStr for TaskId {
    type Err = ParseCommandError;
    fn from_str(s: &str) -> std::result::Result<Self, Self::Err> {
        let n: u32 = s.parse().map_err(|_| ParseCommandError::BadId(s.into()))?;
        NonZeroU32::new(n).ok_or_else(|| ParseCommandError::BadId(s.into())).map(TaskId)
    }
}

impl std::convert::TryFrom<u32> for TaskId {
    type Error = ParseCommandError;
    fn try_from(n: u32) -> Result<Self, Self::Error> {
        NonZeroU32::new(n).map(TaskId).ok_or(ParseCommandError::BadId(n.to_string()))
    }
}
```

**Code Triple:**  
**Rust:**  
```rust
Command::Add { title } => ...
```  

**C/C++:**  
```cpp
union { std::string title; int id; };
```  

**Python:**  
```python
if "add" in cmd:  // Runtime
```

**Rust Failure Variant:** Mismatch pattern.  
```rust
match cmd {
    Command::Add => (),  // Missing { title }
}
```

**Compiler Output (Key lines; messages may vary):**  
```
error[E0005]: refutable pattern
```  
Error code: E0005.

**Compiler Reasoning Steps:**  
- Variant expects pattern.  
- No bind.  
- Rejects.

**Analysis:**  
- Ownership impact: Move unless ref.  
- Performance: Efficient.  
- Typical compiler error: E0005.

**ASCII Diagram: Match Destructure**  
```
match cmd {
  Add { title } => use title
}
```

**Micro-Challenge Variations:** Predict: TryFrom<u32> "0".  

**Solution to Micro-Challenge:** Err (non-zero).

**Contrast:** C union unsafe; Python dynamic.

**Takeaway:** Newtypes prevent misuse.

> **Lab – Try This:** Implement TryFrom for TaskId; test.  
> **Solution:** Handle invalid; return Err.

[Design] **Reflection – Think:** Newtype vs u32?  
[Answer] **Model Answer:** Type safety.

[Semantics] **Think like the Compiler:** What for pattern mismatch? (Answer: E0308.)

**Part II Checkpoint:** Enum for? Newtype?  
**Answers:** Variants. Safety.

**You Can Now:**  
- Define enums/newtypes.  
- Match variants.

**Part II Quiz:** (5 MCQs + 1 open conceptual question)  
1. Enum is? (a) Product (b) Sum (c) Both  
   Answer: (b)  
2. Match requires? (a) Partial (b) Exhaustive (c) Optional  
   Answer: (b)  
3. True/False: Newtypes wrap.  
   Answer: True  
4. Destructure performance? (a) O(n) (b) O(1) (c) Variable  
   Answer: (b)  
5. True/False: Non-exhaustive error.  
   Answer: True  
Open Conceptual: Explain newtype benefit.  
Answer: Strong typing.

**Self-Assessment:**  
[ ] Defined enum/newtype.  
[ ] Fixed non-exhaustive.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part III: Option/Result – Handling Absence and Failure with Combinators

**You Will Be Able To:**  
- Use Option for nullable with combinators.  
- Use Result for errors with ?.  
- Define error policy: thiserror library, anyhow CLI.

**Time Estimate:** 15 minutes.

### Core Concept: Case 1 – Option<T> for Absence with Combinators

**Problem / Motivation:** Null NPE; explicit handling.

**Definition (Formal):** Option: Some/None; map/and_then chain.

**Mental Model (Simplified):** Explicit nullable.

**Example (Compilable):** Combinators.  
```rust
fn find_title(store: &impl TaskStore, id: TaskId) -> Option<&str> {
    store.get(id).map(|t| t.title.as_str())
}
```

**Code Triple:**  
**Rust:**  
```rust
.map(|t| ...)
```  

**C/C++:**  
```cpp
if (ptr) ptr->title;
```  

**Python:**  
```python
if obj: obj.title
```

**Rust Failure Variant:** Unwrap None (anti-pattern in library).  

**Compiler Output (Key lines; messages may vary):** Runtime panic.

**Analysis:**  
- Ownership impact: Some owns.  
- Performance: Efficient.  
- Typical: Panic unwrap (avoid).

**ASCII Diagram: Option to Result Propagation**  
```
Option<T> --ok_or_else--> Result<T, E> --?--> propagate
```

**Micro-Challenge Variations:** Predict: and_then.  

**Solution to Micro-Challenge:** Chain.

**Contrast:** Null UB; None runtime.

**Takeaway:** Combinators safe chain.

> **Lab – Try This:** Use map on Option.  
> **Solution:** Transform without unwrap.

[Design] **Reflection – Think:** Option vs unwrap?  
[Answer] **Model Answer:** Explicit safe.

[Semantics] **Think like the Compiler:** What for unused Option? (Answer: Warning.)

### Core Concept: Case 2 – Result<T, E> for Errors

**Problem / Motivation:** Exceptions implicit; codes ignored.

**Definition (Formal):** Result: Ok/Err; ? propagates.

**Mental Model (Simplified):** Explicit error.

**Example (Compilable):**  
```rust
pub type Result<T> = std::result::Result<T, Error>;

#[derive(thiserror::Error, Debug)]
pub enum Error {
    #[error("not found: {0}")]
    NotFound(TaskId),
    #[error(transparent)]
    Io(#[from] std::io::Error),
    #[error(transparent)]
    Parse(#[from] ParseCommandError),
}

#[derive(thiserror::Error, Debug)]
pub enum ParseCommandError {
    #[error("empty title")]
    EmptyTitle,
    #[error("unknown verb: {0}")]
    UnknownVerb(String),
    #[error("expected numeric id, got: {0}")]
    BadId(String),
}

fn get_required(store: &impl TaskStore, id: TaskId) -> Result<&Task> {
    store.get(id).ok_or_else(|| Error::NotFound(id))
}
```

**Code Triple:**  
**Rust:**  
```rust
? // propagate
```  

**C/C++:**  
```cpp
if (err) return err;
```  

**Python:**  
```python
raise
```

**Rust Failure Variant:** Unused Result.  

**Compiler Output (Key lines; messages may vary):** Warning unused.

**Analysis:**  
- Ownership impact: Own.  
- Performance: No unwind.  
- Typical: Lint unused.

**ASCII Diagram: Result Flow**  
```
Ok(T) | Err(E)
? --> propagate Err
```

**Micro-Challenge Variations:** Predict: ? in CLI with anyhow.  

**Solution to Micro-Challenge:** .context("msg").

**Contrast:** Exceptions unwind; codes ignored.

**Takeaway:** Policy: thiserror library, anyhow CLI.

> **Lab – Try This:** Define ParseCommandError; use in try_new.  
> **Solution:** Typed Err variants.

[Security] **Reflection – Think:** Result vs ignore?  
[Answer] **Model Answer:** Forces handle.

[Semantics] **Think like the Compiler:** What for ? on Ok? (Answer: Unwrap.)

**Part III Checkpoint:** Option for? Result policy?  
**Answers:** Absence. thiserror library, anyhow CLI.

**You Can Now:**  
- Use Option/Result combinators.  
- Define error boundaries.

**Part III Quiz:** (5 MCQs + 1 open conceptual question)  
1. Option replaces? (a) Null (b) Exceptions (c) Codes  
   Answer: (a)  
2. ? does? (a) Panic (b) Propagate (c) Ignore  
   Answer: (b)  
3. True/False: thiserror for library.  
   Answer: True  
4. Combinators performance? (a) Slow (b) Efficient (c) Variable  
   Answer: (b)  
5. True/False: Unwrap in library ok.  
   Answer: False  
Open Conceptual: Explain anyhow vs thiserror.  
Answer: Context vs typed.

**Self-Assessment:**  
[ ] Used combinators.  
[ ] Defined Error.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part IV: Parsing, Storage, and Advanced Testing

**You Will Be Able To:**  
- Parse with FromStr.  
- Use traits for storage.  
- Write table-driven/property tests.

**Time Estimate:** 15 minutes.

### Core Concept: Parsing with FromStr

**Example (Compilable):**  
```rust
impl std::str::FromStr for Command {
    type Err = ParseCommandError;
    fn from_str(s: &str) -> std::result::Result<Self, Self::Err> {
        let s = s.trim();

        if let Some(rest) = s.strip_prefix("add") {
            let title = rest.trim_start();
            if title.is_empty() {
                Err(ParseCommandError::EmptyTitle)
            } else {
                Ok(Command::Add { title: title.to_string() })
            }
        } else if let Some(rest) = s.strip_prefix("complete") {
            let rem = rest.trim_start();
            let id_str = rem.split_once(' ').map(|(a, _)| a).unwrap_or(rem);
            if id_str.is_empty() {
                return Err(ParseCommandError::BadId("<missing>".into()));
            }
            let id: TaskId = id_str.parse().map_err(|_| ParseCommandError::BadId(id_str.into()))?;
            Ok(Command::Complete { id })
        } else if s == "list" {
            Ok(Command::List)
        } else if s.is_empty() {
            Err(ParseCommandError::UnknownVerb("<empty>".into()))
        } else {
            let verb = s.split_whitespace().next().unwrap().to_string();
            Err(ParseCommandError::UnknownVerb(verb))
        }
    }
}
```

**Code Triple:**  
**Rust:**  
```rust
line.parse::<Command>()?
```  

**C/C++:**  
```cpp
sscanf
```  

**Python:**  
```python
split  // runtime
```

**Analysis:**  
- Ownership impact: Borrow input.  
- Performance: O(n).  
- Typical error: Parse fail.

**Takeaway:** Typed parsing; ignores trailing for "complete" (documented; reject if needed).

> **Lab – Try This:** Implement FromStr for Command.  
> **Solution:** As example; handle cases.

### Core Concept: Storage Trait and Executor

**Example (Compilable):**  
```rust
pub trait TaskStore {
    type Iter<'a>: Iterator<Item = &'a Task> where Self: 'a;

    fn insert(&mut self, t: Task) -> Result<()>;
    fn get(&self, id: TaskId) -> Option<&Task>;
    fn get_mut(&mut self, id: TaskId) -> Option<&mut Task>;
    fn list(&self) -> Self::Iter<'_>;
}

pub fn execute<S: TaskStore>(store: &mut S, cmd: Command) -> Result<()> {
    match cmd {
        Command::Add { title } => {
            let id = next_id(store)?;
            let t = Task::try_new(id, title)?;
            store.insert(t)
        }
        Command::Complete { id } => {
            let t = store.get_mut(id).ok_or(Error::NotFound(id))?;
            t.complete();
            Ok(())
        }
        Command::List => Ok(()),
    }
}

fn next_id<S: TaskStore>(s: &S) -> Result<TaskId> {
    use std::num::NonZeroU32;
    let max = s.list().map(|t| t.id.0.get()).max().unwrap_or(0);
    let next = max.checked_add(1).ok_or_else(|| Error::Parse(ParseCommandError::BadId("overflow".into())))?;
    let nz = NonZeroU32::new(next).ok_or_else(|| Error::Parse(ParseCommandError::BadId("zero".into())))?;
    Ok(TaskId(nz))
}

#[derive(Default)]
pub struct InMemoryStore { tasks: Vec<Task> }

impl TaskStore for InMemoryStore {
    type Iter<'a> = std::slice::Iter<'a, Task>;

    fn insert(&mut self, t: Task) -> Result<()> { self.tasks.push(t); Ok(()) }
    fn get(&self, id: TaskId) -> Option<&Task> { self.tasks.iter().find(|t| t.id == id) }
    fn get_mut(&mut self, id: TaskId) -> Option<&mut Task> { self.tasks.iter_mut().find(|t| t.id == id) }
    fn list(&self) -> Self::Iter<'_> { self.tasks.iter() }
}
```

**Analysis:**  
- Ownership impact: Mut borrow.  
- Performance: O(1) insert.  
- Typical: Trait bound E0277.

**Takeaway:** Isolate for tests; TaskStore with GATs is not object-safe; use static dispatch. If you need trait objects later, switch list() to return Box<dyn Iterator<...>>.

> **Lab – Try This:** Implement execute.  
> **Solution:** Use ?; no unwrap.

### Core Concept: Advanced Testing

**Example (Compilable):** Table/property.  
```rust
#[cfg(test)]
mod tests {
    use super::*;
    use proptest::prelude::*;

    #[test]
    fn fromstr_table() {
        let cases = [
            ("list", Ok(Command::List)),
            ("add do stuff", Ok(Command::Add { title: "do stuff".into() })),
            ("complete 1", Ok(Command::Complete { id: TaskId(NonZeroU32::new(1).unwrap()) })),
            ("add", Err(ParseCommandError::EmptyTitle)),
            ("complete x", Err(ParseCommandError::BadId("x".into()))),
        ];
        for (inp, exp) in cases {
            let got = inp.parse::<Command>();
            match (got, exp) {
                (Ok(Command::List), Ok(Command::List)) => {},
                (Ok(Command::Add { title: a }), Ok(Command::Add { title: b })) => assert_eq!(a, b),
                (Ok(Command::Complete { id: a }), Ok(Command::Complete { id: b })) => assert_eq!(a, b),
                (Err(ParseCommandError::EmptyTitle), Err(ParseCommandError::EmptyTitle)) => {},
                (Err(ParseCommandError::BadId(x)), Err(ParseCommandError::BadId(y))) => assert_eq!(x, y),
                other => panic!("mismatch: {:?}", other),
            }
        }
    }

    proptest! {
        #[test]
        fn never_panic_on_arbitrary_input(s in ".*") {
            let _ = s.parse::<Command>();
        }

        #[test]
        fn parse_never_yields_empty_add_title(s in ".*") {
            if let Ok(Command::Add { title }) = s.parse::<Command>() {
                prop_assert!(!title.trim().is_empty());
            }
        }

        #[test]
        fn complete_only_accepts_numeric_nonzero(id in ".*") {
            let s = format!("complete {id}");
            let _ = s.parse::<Command>();
        }
    }
}
```

**Analysis:**  
- Ownership impact: Test clone.  
- Performance: Fast.  
- Typical: Assert fail.

**Takeaway:** Cover paths; never panic.

> **Lab – Try This:** Write table test for parse.  
> **Solution:** Valid/invalid.

**Part IV Checkpoint:** FromStr for? Trait for?  
**Answers:** Parsing. Isolation.

**You Can Now:**  
- Parse FromStr.  
- Use traits.  
- Advanced tests.

**Part IV Quiz:** (5 MCQs + 1 open conceptual question)  
1. FromStr returns? (a) Option (b) Result (c) String  
   Answer: (b)  
2. Trait for storage? (a) Coupling (b) Isolation (c) I/O  
   Answer: (b)  
3. True/False: Table-driven exhaustive.  
   Answer: True  
4. Property tests for? (a) Specific (b) Fuzz (c) Integration  
   Answer: (b)  
5. True/False: Unwrap in tests ok.  
   Answer: True (for setup, not behavior under test)  
Open Conceptual: Explain table vs single tests.  
Answer: Coverage concise.

**Self-Assessment:**  
[ ] Implemented parse/execute/tests.  
[ ] Tested errors.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Exercises: Tiered Reasoning

### Tier 1: Concept Rebuilds

1. Invariant Struct  
   Add to Task try_new.  
   **Solution:** Err on invalid.

2. Enum Match  
   Exhaustive Status.  
   **Solution:** Arms for Pending/Done.

### Tier 2: Comparative Rewrites

1. C Union to Enum  
   Safe variants.  
   **Solution:** Data-carrying.

2. Python None to Option  
   Explicit.  
   **Solution:** map chain.

### Tier 3: Challenge Extensions

1. Property Test  
   Round-trip Command FromStr.  
   **Solution:** proptest any string.

2. Integration Test  
   Script commands; assert state.  
   **Solution:** InMemoryStore in tests/cli_roundtrip.rs feeding commands, assert IDs/titles/status.

**Self-Assessment:**  
[ ] Completed one per tier.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Recap and Synthesis Reflection

**Table Completion Exercise:**  
| Rust Feature | C/C++ Issue | Python Trade-off |
|--------------|-------------|------------------|
| Structs/Invariants | Manual checks | Runtime errors |
| Enums/Newtypes | Unions unsafe | Dynamic types |
| Option/Result | Null/codes | None/exceptions |
| FromStr/Traits | Ad-hoc parse | Split runtime |
| Advanced Tests | External libs | Pytest dynamic |

**Self-Quiz:** (Design-level)  
1. Invariants where?  
2. Result policy?  
3. Table tests for?  
Answers:  
1. Constructors via Result.  
2. thiserror library, anyhow CLI.  
3. Coverage.

**Final Takeaway:** Types/errors/tests drive safe design.

**By Session End:**  
- Model with structs/enums/newtypes.  
- Use Option/Result/combinators.  
- Define error policies.  
- Write advanced tests.  
- Fix errors/violations.  
- Extend CLI with parsing/storage.

**Glossary Appendix Update:** Add: Newtype, Sum type, FromStr, Result alias, thiserror.

**Error Code Index:**  
| Code   | Description                     | Example Case |
|--------|---------------------------------|--------------|
| E0063  | Missing field                   | Struct init |
| E0004  | Non-exhaustive match            | Enum arms |
| E0594  | Assign to immutable             | &self mutate |
| E0308  | Mismatched types                | Option/Result |
| E0277  | Trait bound not satisfied       | Storage use |
| E0596  | Cannot borrow as mutable         | Immutable call |
| E0515  | Cannot return ref to local      | Dangling slice |

**Primary References:** Rust Book Ch. 5 (Structs), Ch. 6 (Enums), Ch. 9 (Errors), Ch. 11 (Testing).  
**Suggested Deep Dives:** thiserror crate; proptest for properties.

**Concept Map:** (Text-based ASCII)  
Structs (fields, invariants, methods)  
Enums/Newtypes (variants, safety)  
Option/Result (combinators, ?)  
FromStr/Parsing (boundaries)  
Traits/Testing (isolation, coverage)  
Applied (Task v4)

**Bridge to Session 6:** Types to generics/traits.

**Self-Assessment:**  
[ ] Reviewed map/quiz.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

**Deep Dive Appendix:**  
- thiserror vs anyhow: Typed for library, context for CLI.  
- Property tests: Use proptest for fuzz (e.g., parse never panics).