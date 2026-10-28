# Session 4: Borrowing, References, Slices, Lifetime Intuition – Safe and Efficient Data Access

**Target Audience & Scope:** This series assumes familiarity with C/Python, basic memory models (e.g., stack/heap, pointers/references, GC internals), and command-line tools. It targets programmers with systems or dynamic language experience new to Rust. Tone balances explanation for beginners in Rust but avoids over-simplifying semantics for intermediates.

**Prerequisites:** Session 3 concepts (ownership, moves, Copy/Clone, RAII); Task CLI v2.

**Conceptual Learning Goals:**  
- Understand borrowing rules and aliasing.  
- Use &T/&mut T in practice.  
- Work with slices &[T]/&str.  
- Build lifetime intuition to predict errors.  

**Mechanical Learning Goals:**  
- Refactor owning APIs to borrowed.  
- Respect aliasing rule.  
- Use slices for views.  
- Visualize lifetimes.  
- Write tests for borrowed fns.  

**Design Learning Goals:**  
- Extend the CLI with borrowed APIs.  
- Fix borrow errors with scoping/restructuring.  
- Design functions with &T/&mut T trade-offs.

**By the End of This Session, You Can:**  
- Refactor owning APIs to borrowed.  
- Respect aliasing rule.  
- Use slices for views.  
- Visualize lifetimes.  
- Write tests for borrowed fns.  
- Fix borrow errors.  
- Extend CLI with borrows.

**Project Narrative:** Building on the move/clone/RAII model from Session 3, refactor Task Manager to v3, using borrows for efficient access without transfer.

**Time Estimate:** 60 minutes.

---

## Setup Checklist

Verify and add testing.

1. **Verify Existing Setup**  
   ```bash
   cargo --version
   rustc --version
   cargo fmt
   cargo clippy
   ```
   Confirm rust-analyzer (hover lifetimes).

2. **Introduce Testing Workflow**  
   ```bash
   cargo test
   ```
   Runs #[test] functions.

3. **Optional: Practice Adding a Dependency**  
   ```bash
   cargo add thiserror
   ```

4. **Run Your Session 3 CLI**  
   ```bash
   cargo run
   ```
   Ensure Task List v2 works.

> **Lab – Try This:** Add dummy test:  
> ```rust
> #[cfg(test)]
> mod tests {
>     #[test]
>     fn it_works() {
>         assert_eq!(2 + 2, 4);
>     }
> }
> ```  
> Run `cargo test`.  
> **Solution:**  
> ```
> running 1 test
> test tests::it_works ... ok
> ```  
> Takeaway: Verify borrows in tests.

**Debug the Error Mini-Lab (Retention Test from Session 3):** Modify add_task to double drop. Predict error; fix.  
**Solution:** E0382; remove second drop.

**Self-Assessment:**  
[ ] Verified setup and completed mini-lab.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

**Time Estimate:** 15 minutes.

---

## Part I: Borrowing Rules – Temporary Access Without Ownership

**You Will Be Able To:**  
- Explain borrowing laws.  
- Predict aliasing errors.  
- Contrast with C/C++/Python.

**Time Estimate:** 15 minutes.

**Borrowing Laws (for this session):**  
- References borrow from owners; never own.  
- Many &T or one &mut T; no mix.  
- References must not outlive owners (lifetimes).  
- &self/&mut self sugar for &T/&mut T.

### Core Concept: Case 1 – Immutable Borrowing

**Problem / Motivation:** Owning APIs require move/clone; C/C++ aliases unsafe; Python shares without guarantees.

**Definition (Formal):** &T: Immutable reference; temporary view.

**Mental Model (Simplified):** Read-only borrow; no transfer.

**Example (Compilable):** Implicit borrow.  
```rust
let s = String::from("hello");
let len = s.len();  // Implicit borrow via method
```

**Code Triple:**  
**Rust (Safe borrow):**  
```rust
let s = String::from("hello");
let len = s.len();  // Implicit borrow via method
```  

**C/C++ (Raw pointer alias):**  
```cpp
std::string s = "hello";
const char* ptr = s.c_str();  // Alias; risk if s modified
```  

**Python (Shared ref):**  
```python
s = "hello"
len_s = len(s)  // Shared ref, GC handles
```

**Rust Failure Variant:** Borrow after move.  
```rust
fn main() {
    let s = String::from("hello");
    let t = s;  // Move
    let len = s.len();  // Borrow after move
}
```

**Compiler Output (Key lines; messages may vary):**  
```
error[E0382]: borrow of moved value: `s`
 --> src/main.rs:4:15
  |
2 |     let s = String::from("hello");
  |         - move occurs because `s` has type `String`, which does not implement the `Copy` trait
3 |     let t = s;
  |             - value moved here
4 |     let len = s.len();
  |               ^ value borrowed here after move
```  
Error code: E0382.

**Compiler Reasoning Steps:**  
- Move detected.  
- At borrow: Check valid.  
- Rejects: Prevents invalid access.

**Analysis:**  
- Ownership impact: No transfer; multiple OK.  
- Performance: Borrow O(1).  
- Typical compiler error: E0382 (borrow moved).

**ASCII Diagram: Immutable Borrow**  
```
Owner: s --> "hello" (heap)
Borrow: ref --> points to s (valid while s lives)
```

**Micro-Challenge Variations:** Predict: Pass String without move. Signature?  

**Solution to Micro-Challenge:** fn length(s: &str) -> usize { s.len() }  

**Contrast:** C++ risk invalidate; Python runtime.  

**Takeaway:** Immutable borrowing enables read without clones.

> **Lab – Try This:** Refactor Session 3 function like print_tasks to &Vec<Task>. Call multiple times without clone/move.  
> **Solution:**  
> ```rust  
> fn print_tasks(ts: &Vec<Task>) { println!("{:?}", ts); }  
> print_tasks(&tasks);  // Borrow  
> print_tasks(&tasks);  // Ok, multiple immutable  
> ```  

[Design] **Reflection – Think:** How does this fix Session 3's clumsiness?  
[Answer] **Model Answer:** No ownership transfer; call functions repeatedly without clone overhead.

[Semantics] **Think like the Compiler:** What for mut on &T? (Answer: Reject; suggest &mut.)

### Core Concept: Case 2 – Mutable Borrowing and Aliasing Rule

**Problem / Motivation:** Shared mutable causes races. C/C++ lax; Python GIL limits.

**Definition (Formal):** &mut T: Mutable reference; exclusive access.

**Mental Model (Simplified):** One writer; no readers during.

**Example (Compilable):** Mutable method.  
```rust
let mut s = String::from("hello");
s.push_str(", world");  // Implicit &mut self
```

**Code Triple:**  
**Rust (Exclusive mutable):**  
```rust
let mut s = String::from("hello");
s.push_str(", world");  // Implicit &mut self
```  

**C/C++ (Shared mutable alias):**  
```cpp
std::string s = "hello";
char* ptr = &s[0];  // Mutable alias; races if threaded
```  

**Python (Shared mutable):**  
```python
def append(xs, extra):
    xs.append(extra)  # mutates the list in place
```

**Rust Failure Variant:** Multiple mutable.  
```rust
fn main() {
    let mut x = 0;
    let r1 = &mut x;
    let r2 = &mut x;  // Second mutable
}
```

**Compiler Output (Key lines; messages may vary):**  
```
error[E0499]: cannot borrow `x` as mutable more than once at a time
 --> src/main.rs:3:14
  |
2 |     let r1 = &mut x;
  |              ------ first mutable borrow occurs here
3 |     let r2 = &mut x;
  |              ^^^^^^ second mutable borrow occurs here
```  
Error code: E0499.

**Compiler Reasoning Steps:**  
- First &mut: Exclusive borrow.  
- Second: Overlap check.  
- Rejects: Enforces rule.

**Analysis:**  
- Ownership impact: Exclusive mut.  
- Performance: O(1) borrow.  
- Typical compiler error: E0499 (multiple mut).

**ASCII Diagram: Aliasing Rule**  
```
// Valid states for a given value:
State A: 0..N immutable borrows, 0 mutable borrows.
State B: 1 mutable borrow, 0 immutable borrows.
// Anything else: borrow checker error.
```

**Micro-Challenge Variations:** Predict: Fix multiple mut by scoping.  

**Solution to Micro-Challenge:** Inner scope for first.  

**Contrast:** C++ manual; Python GIL.  

**Takeaway:** Exclusive mutable ensures thread-safety without locks.

> **Lab – Try This:** Add mutable borrow to Task CLI, e.g., mark complete.  
> **Solution:**  
> ```rust  
> fn mark_complete(task: &mut Task) {  
>     task.completed = true;  
> }  
> mark_complete(&mut my_task);  
> ```  

[Semantics] **Reflection – Think:** Why no GIL like Python?  
[Answer] **Model Answer:** Rust doesn’t need a global interpreter lock like Python because the type system and ownership rules ensure that shared mutable state must go through explicit synchronization types (Mutex, RwLock, atomic types, etc.). There’s no blanket global lock, and you only pay for coordination where you actually share state.

[Semantics] **Think like the Compiler:** What for mixed borrows? (Answer: Reject overlap.)

### Core Concept: Case 3 – Borrow Checker Errors and Fixes

**Problem / Motivation:** Borrow errors teach safe design. C/C++ has no equivalent; Python has no compile checks.

**Definition (Formal):** Borrow checker enforces rules at compile time.

**Mental Model (Simplified):** Errors guide restructuring.

**Example (Compilable):** N/A.

**Code Triple:**  
**Rust (Rejected mixed):**  
```rust
let mut s = String::from("hello");
let r = &s;  // Immutable
s.push_str("!");  // Mutable while immutable active
```  

**C/C++ (Compiles, risk):**  
```cpp
std::string s = "hello";
const char* r = s.c_str();  // Immutable alias
s += "!";  // Mutable; may invalidate r
```  

**Python (Runtime-managed with no static lifetime checks):**  
```python
s = "hello"
r = s  // Shared
s += "!"  // New str; old r unchanged
```

**Rust Failure Variant:** Mixed borrows.  
```rust
fn main() {
    let mut s = String::from("hello");
    let r = &s;
    s.push_str("!");
    println!("{}", r);
}
```

**Compiler Output (Key lines; messages may vary):**  
```
error[E0502]: cannot borrow `s` as mutable because it is also borrowed as immutable
 --> src/main.rs:4:5
  |
3 |     let r = &s;
  |             -- immutable borrow occurs here
4 |     s.push_str("!");
  |     ^ mutable borrow occurs here
5 |     println!("{}", r);
  |                    - immutable borrow later used here
```  
Error code: E0502.

**Compiler Reasoning Steps:**  
- Immutable active.  
- At mut: Check overlap.  
- Rejects: Hints scope.

**Analysis:**  
- Ownership impact: Restructure for rules.  
- Performance: No runtime cost.  
- Typical compiler error: E0502 (mut while immut).

**ASCII Diagram:** N/A.

**Micro-Challenge Variations:** Predict: Fix mixed with scope.  

**Solution to Micro-Challenge:** Mutate first or scope.  

**Contrast:** C++ runtime; Python no static.  

**Takeaway:** Errors guide safer designs.

> **Lab – Try This:** Trigger E0502 in your code and use compiler hints to fix.  
> **Solution:** Follow "borrow occurs here" notes; reorder or scope.

[Design] **Reflection – Think:** Borrow errors vs C++ crashes?  
[Answer] **Model Answer:** Compile-time vs runtime; faster iteration.

[Semantics] **Think like the Compiler:** What for mixed? (Answer: Reject; suggest scope.)

**Table of Common Borrow Checker Errors:**  
| Code   | Cause                           | Typical Fix |
|--------|---------------------------------|-------------|
| E0382  | Borrow after move               | Clone or borrow before move |
| E0502  | Mut while immut                 | Scope/reorder borrows |
| E0499  | Multiple mut                    | Scope mut borrows |

**Part I Checkpoint:** What is borrowing? What is the aliasing rule in Rust?  
**Answers:** Temporary access to a value via a reference, without taking ownership. Many immutable OR one mutable.

**You Can Now:**  
- Use &T and &mut T for borrowing.  
- Respect aliasing rule.  

**Part I Quiz:** (5 MCQs + 1 open conceptual question)  
1. Borrowing purpose? (a) Own (b) Access without own (c) Copy  
   Answer: (b)  
2. Aliasing rule? (a) Many mut (b) Many immut or one mut (c) Any  
   Answer: (b)  
3. True/False: Mut behind &.  
   Answer: False  
4. Borrow performance? (a) O(n) (b) O(1) (c) Variable  
   Answer: (b)  
5. True/False: Multiple &mut OK.  
   Answer: False  
Open Conceptual: Explain many readers or one writer.  
Answer: Prevents races.

**Self-Assessment:**  
[ ] Predicted aliasing error.  
[ ] Completed labs.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part II: References – &T and &mut T in Practice

**You Will Be Able To:**  
- Write function signatures with references.  
- Understand self in methods.  
- Predict mutability errors.

**Time Estimate:** 15 minutes.

**Design Cheat Sheet:**  
- fn f(x: T) – takes ownership.  
- fn f(x: &T) – borrows immutably.  
- fn f(x: &mut T) – borrows mutably.

### Part 2A: Immutable References (&T)

**Problem / Motivation:** References enable borrowing; C/C++ refs like aliases but unsafe; Python no distinction.

**Definition (Formal):** &T: Immutable reference.

**Mental Model (Simplified):** Read-only; no mut.

**Example (Compilable):**  
```rust
fn read_only(s: &str) { println!("{}", s); }
```

**Code Triple:**  
**Rust:**  
```rust
fn read_only(s: &str) { println!("{}", s); }
```  

**C/C++:**  
```cpp
void read_only(const std::string& s) { std::cout << s; }
```  

**Python:**  
```python
def read_only(s): print(s)
```

**Rust Failure Variant:** Mutate immutable.  
```rust
fn mutate(s: &String) { s.push_str("!"); }
```

**Compiler Output (Key lines; messages may vary):**  
```
error[E0596]: cannot borrow `*s` as mutable, as it is behind a `&` reference
 --> src/main.rs:2:5
  |
1 | fn mutate(s: &String) {
  |              ------- help: consider changing this to be a mutable reference: `&mut String`
2 |     s.push_str("!");
  |     ^^^^^^^^^^^^^^ `s` is a `&` reference, so the data it refers to cannot be borrowed as mutable
```  
Error code: E0596.

**Compiler Reasoning Steps:**  
- Signature &T.  
- At mut: Check immut.  
- Rejects: Suggest &mut.

**Analysis:**  
- Ownership impact: No change; multiple OK.  
- Performance: O(1).  
- Typical compiler error: E0596.

**ASCII Diagram:** N/A.

**Micro-Challenge Variations:** Predict: Mut ref function. Usable after?  

**Solution to Micro-Challenge:** Yes; no transfer.  

**Contrast:** C++ const &; Python no distinction.  

**Takeaway:** &T for read-only.

[Semantics] **Reflection – Think:** &T vs owning?  
[Answer] **Model Answer:** Efficient; no clone/move.

[Semantics] **Think like the Compiler:** What for multiple &T? (Answer: Allow; immut safe.)

### Part 2B: Mutable References (&mut T)

**Problem / Motivation:** Safe mutation without full ownership.

**Definition (Formal):** &mut T: Mutable reference.

**Mental Model (Simplified):** Exclusive mut access.

**Example (Compilable):**  
```rust
fn append(s: &mut String, extra: &str) { s.push_str(extra); }
```

**Code Triple:**  
**Rust:**  
```rust
fn append(s: &mut String, extra: &str) { s.push_str(extra); }
```  

**C/C++:**  
```cpp
void append(std::string* s, const char* extra) { *s += extra; }
```  

**Python:**  
```python
def append(xs, extra):
    xs.append(extra)  # mutates the list in place
```

**Rust Failure Variant:** Immutable while mutable.  
```rust
let mut s = String::from("hello");
let r = &s;  // Immutable
append(&mut s, "!");
```

**Compiler Output (Key lines; messages may vary):**  
```
error[E0502]: cannot borrow `s` as mutable because it is also borrowed as immutable
 --> src/main.rs:4:5
  |
3 |     let r = &s;
  |             -- immutable borrow occurs here
4 |     append(&mut s, "!");
  |     ^ mutable borrow occurs here
5 |     println!("{}", r);
  |                    - immutable borrow later used here
```  
Error code: E0502.

**Compiler Reasoning Steps:**  
- Immutable active.  
- At &mut: Overlap check.  
- Rejects: Enforces exclusive.

**Analysis:**  
- Ownership impact: Exclusive; owner mut.  
- Performance: O(1).  
- Typical compiler error: E0502.

**ASCII Diagram:** N/A.

**Micro-Challenge Variations:** Predict: Use &mut in loop. Error when?  

**Solution to Micro-Challenge:** If immut in loop; scope mut.  

**Contrast:** C++ *; Python shared mut.  

**Takeaway:** &mut T for exclusive mutation.

[Semantics] **Reflection – Think:** &mut vs C++ &?  
[Answer] **Model Answer:** Both mut aliases; Rust checks exclusivity compile-time.

[Semantics] **Think like the Compiler:** What for &mut with immut? (Answer: Reject; hint scope.)

**Part II Checkpoint:** How do you write a function that takes ownership of a String? How do you write a function that borrows immutably / borrows mutably? Can a function simultaneously hold a &mut String and a &String to the same value? Why or why not?  
**Answers:** fn f(s: String). fn f(s: &str) / fn f(s: &mut String). No; that would violate the aliasing rule. You can have many &String or one &mut String, but never both at the same time for the same value in safe Rust.

**You Can Now:**  
- Write borrowing functions.  
- Predict mutability errors.

**Part II Quiz:** (5 MCQs + 1 open conceptual question)  
1. &T allows? (a) Mut (b) Read (c) Own  
   Answer: (b)  
2. &mut requires? (a) Multiple (b) Exclusive (c) Shared  
   Answer: (b)  
3. True/False: Owner mut for &mut.  
   Answer: True  
4. Ref performance? (a) O(n) (b) O(1) (c) Variable  
   Answer: (b)  
5. True/False: Methods implicit ref.  
   Answer: True  
Open Conceptual: Explain self in methods.  
Answer: Sugar for &T/&mut T.

**Self-Assessment:**  
[ ] Wrote ref functions.  
[ ] Fixed mut error.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part III: Slices – Efficient Borrowed Views

**You Will Be Able To:**  
- Use &[T]/&str for views.  
- Understand fat pointers.  
- Predict bounds panics.

**Time Estimate:** 15 minutes.

### Core Concept: Slices (&[T] and &str)

**Problem / Motivation:** Efficient subsets without copy; C/C++ arithmetic risky; Python slicing new list.

**Definition (Formal):** &[T]: Fat pointer (ptr + len) borrow.

**Mental Model (Simplified):** Zero-copy contiguous view.

**Example (Compilable):**  
```rust
let v = vec![1,2,3,4];
let slice = &v[1..3];  // &[2,3]
```

**Code Triple:**  
**Rust:**  
```rust
let v = vec![1,2,3,4];
let slice = &v[1..3];  // &[2,3]
```  

**C/C++:**  
```cpp
int v[4] = {1,2,3,4};
int* slice = v + 1;  // No len
```  

**Python:**  
```python
v = [1,2,3,4]
slice = v[1:3]  // New list
```

**Rust Failure Variant:** Out-of-bounds.  
```rust
let slice = &v[1..5];
```

**Compiler Output:** No compile; runtime panic.

**Compiler Reasoning Steps:**  
- Dynamic range: Runtime check.  
- Const: Compile reject if eval.

**Analysis:**  
- Ownership impact: Borrow; no move.  
- Performance: O(1).  
- Typical compiler error: None; runtime panic.

**ASCII Diagram: Fat Pointer**  
```
&[T]: ptr --> data, len: N
```

**Fat-Pointer Layout Diagram:**  
```
ptr (8B) | len (8B)  // 64-bit
--> data
```

**Micro-Challenge Variations:** Predict: Slice String to &str. Coercion?  

**Solution to Micro-Challenge:** &s[0..5]; "hello".  

**Contrast:** C++ no len; Python copy.  

**Takeaway:** Slices: zero-copy views.

> **Lab – Try This:** Implement first_word on &str.  
> **Solution:**  
> ```rust  
> fn first_word(s: &str) -> &str {  
>     let bytes = s.as_bytes();  
>     for (i, &item) in bytes.iter().enumerate() {  
>         if item == b' ' { return &s[0..i]; }  
>     }  
>     s  
> }  
> ```  

[Performance] **Reflection – Think:** Slices vs Python?  
[Answer] **Model Answer:** Borrow vs copy; efficient large data. Python list slicing allocates a new list container, but the elements are the same objects (shared references). So you pay for a new list container, but mutable elements inside are still shared.

[Semantics] **Think like the Compiler:** What for out-of-bounds? (Answer: Runtime panic if dynamic.)

**Part III Checkpoint:** Slice structure? &str vs String?  
**Answers:** Ptr + len. Borrowed UTF-8 vs owned.

**You Can Now:**  
- Use slices in functions.  
- Handle bounds safely.

**Part III Quiz:** (5 MCQs + 1 open conceptual question)  
1. Slice is? (a) Owned (b) Borrow (c) Copy  
   Answer: (b)  
2. Fat pointer? (a) Ptr only (b) Ptr + len (c) Heap  
   Answer: (b)  
3. True/False: &str from String.  
   Answer: True (coerce)  
4. Slice performance? (a) O(n) (b) O(1) (c) Variable  
   Answer: (b)  
5. True/False: Bounds compile always.  
   Answer: False (runtime dynamic)  
Open Conceptual: Explain slice benefit.  
Answer: Efficient views without copy.

**Self-Assessment:**  
[ ] Used slices.  
[ ] Predicted panic.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part IV: Lifetime Intuition – Why Borrows Can't Outlive Owners

**You Will Be Able To:**  
- Understand lifetime basics.  
- Predict dangle errors.  
- Visualize lifetimes.

**Time Estimate:** 15 minutes.

### Core Concept: Lifetime Basics

**Problem / Motivation:** Ensure refs valid; C/C++ manual; Python GC.

**Definition (Formal):** Lifetime: Scope ref valid.

**Mental Model (Simplified):** Borrow <= owner life.

**Example (Compilable):** N/A.

**Code Triple:**  
**Rust (Rejected dangle):**  
```rust
fn dangle() -> &str {
    let s = String::from("dangle");
    &s
}
```  

**C/C++ (Dangling OK):**  
```cpp
const char* dangle() {
    std::string s = "dangle";
    return s.c_str();
}
```  

**Python (GC prevents):**  
```python
def dangle():
    s = "dangle"
    return s  // Ref kept alive
```

**Rust Failure Variant:** Above.

**Compiler Output (Key lines; messages may vary):**  
```
error[E0515]: cannot return reference to local variable `s`
 --> src/main.rs:3:5
  |
3 |     &s
  |     ^^ returns a reference to data owned by the current function
```  
Error code: E0515.

**Compiler Reasoning Steps:**  
- Analyzes borrow: Local s.  
- Checks outlive: No.  
- Rejects: Prevents dangle.

**Analysis:**  
- Ownership impact: Borrow tied to owner.  
- Performance: Compile inference.  
- Typical compiler error: E0515.

**ASCII Diagram: Dangling Ref**  
```
Fn scope
  Local s lives here
  Ref &s
Fn end: s drop
Ref outlives s --> Error
```

**Ownership Timeline Diagram (x-axis = scope):**  
```
Scope start --------------------------- Scope end
s owns ------------------------------- drop s
Borrow ------------------------------- (must end <= s)
```

**Micro-Challenge Variations:** Predict: Fix dangle. How?  

**Solution to Micro-Challenge:** Return String.  

**Contrast:** C++ runtime; Python GC.  

**Takeaway:** Lifetimes prevent dangles compile-time.

> **Lab – Try This:** Trigger borrow error in refactor; fix with scoping.  
> **Solution:** Use {} for temporary mut borrow.

[Semantics] **Reflection – Think:** Lifetimes vs Session 3?  
[Answer] **Model Answer:** Borrows efficient; lifetimes safe.

[Semantics] **Think like the Compiler:** What for borrow outlive? (Answer: Reject; suggest own.)

**Part IV Checkpoint:** Lifetime purpose? Dangle prevention?  
**Answers:** Ref validity scope. Borrows can't outlive owners.

**You Can Now:**  
- Predict lifetime errors.  
- Fix with owned returns.

**Part IV Quiz:** (5 MCQs + 1 open conceptual question)  
1. Lifetime purpose? (a) Own (b) Validity (c) Copy  
   Answer: (b)  
2. Dangle error? (a) Runtime (b) Compile (c) GC  
   Answer: (b)  
3. True/False: Implicit most.  
   Answer: True  
4. NLL ends borrow? (a) Block (b) Last use (c) Function  
   Answer: (b)  
5. True/False: Borrow > owner life.  
   Answer: False  
Open Conceptual: Explain lifetime intuition.  
Answer: Ref valid while owner lives.

**Self-Assessment:**  
[ ] Visualized lifetime.  
[ ] Fixed dangle.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Exercises: Tiered Reasoning

### Tier 1: Concept Rebuilds

1. Immutable Borrow  
   Fn takes &[i32] returns sum.  
   **Solution:**  
   ```rust
   fn sum(nums: &[i32]) -> i32 { nums.iter().sum() }
   ```

2. Mutable Borrow  
   Fn &mut Vec<Task> toggles completed.  
   **Solution:**  
   ```rust
   fn toggle_all(tasks: &mut Vec<Task>) {
       for task in tasks { task.completed = !task.completed; }
   }
   ```

### Tier 2: Comparative Rewrites

1. C++ Pointer to Rust Ref  
   Safe borrow.  
   **Solution:** &T; no dangle. Diff: Compile safe.

2. Python Shared to Rust Borrow  
   Immutable access.  
   **Solution:**  
   ```rust
   fn inspect(lst: &[i32]) { dbg!(lst); }
   ```  
   Diff: No mut surprise.

### Tier 3: Challenge Extensions

1. Mixed Borrow Fix  
   Scope solution.  
   **Solution:** Mutate first or scope.

2. Slice Function  
   Max in slice.  
   **Solution:**  
   ```rust
   fn max_slice(s: &[i32]) -> Option<i32> { s.iter().max().cloned() }
   ```

**Self-Assessment:**  
[ ] Completed one per tier.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Recap and Synthesis Reflection

**Table Completion Exercise:**  
| Rust Feature | C/C++ Issue | Python Trade-off |
|--------------|-------------|------------------|
| Borrowing | Dangling pointers | Runtime-managed; no static checks |
| Aliasing Rule | Races | GIL limits |
| Slices | Pointer arithmetic | Copy overhead |

**Self-Quiz:** (Design-level)  
1. &T purpose?  
2. Aliasing rule?  
3. Lifetime intuition?  
Answers:  
1. Immutable borrow.  
2. Many read or one write.  
3. Ref scope validity.

**Final Takeaway:** Borrowing safe/efficient access; checker ally.

**By Session End:**  
- Refactor to borrowed.  
- Respect aliasing.  
- Use slices.  
- Visualize lifetimes.  
- Write borrow tests.  
- Fix borrow errors.  
- Extend CLI with borrows.

**Glossary Appendix:**  
- Ownership: Single binding controls resource lifetime.  
- Borrow: Temporary reference (&T immutable, &mut T mutable).  
- Move: Transfer ownership without copy.  
- Drop: Deallocate at scope end via `Drop` trait.  
- Lifetime: Region where borrow is valid (`'a`).  
- Trait: Interface (e.g., `Copy`, `Clone`).  
- Crate: Compilation unit/package.  
- Macro!: Compile-time code gen (e.g., println!).  
- Pattern: Destructure values.  
- NLL: Non-lexical lifetimes—precise borrow tracking.  

**Error Code Index:**  
| Code   | Description                     | Example Case |
|--------|---------------------------------|--------------|
| E0106  | Missing lifetime specifier      | Dangling ref |
| E0515  | Cannot return ref to local      | Dangling ref |
| E0382  | Use of moved value              | Double free, move after use |
| E0499  | Multiple mutable borrows        | Data race   |
| E0308  | Mismatched types                | Expression vs statement, type mismatch |
| E0004  | Non-exhaustive match            | Missing arm |
| E0597  | Borrow outlives owner           | Scope borrow |
| E0433  | Unresolved macro                | Macro typo  |

**Primary References:** Rust Book Ch. 4 (References/Borrowing), Ch. 8 (Collections).  
**Suggested Deep Dives:** Rustonomicon (borrow checker); RFCs for NLL.

**Further Reading:** Rust Book Ch. 4 (References/Borrowing), Ch. 8 (Collections).

**Concept Map:** (Text-based ASCII)  
Borrowing  
  ├── &T (immut, many)  
  ├── &mut T (mut, one)  
  └── Aliasing rule (no mix)  
      └── Slices (&[T]/&str)  
          └── Lifetimes (no outlive)  
              └── Applied (Task v3 refactor)

**Bridge to Session 5:** Borrowing with lifetimes; extend Task with complex structs.

**Self-Assessment:**  
[ ] Reviewed concept map and quiz answers.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

**Deep Dive Appendix:**  
- Deref coercion: &String to &str.  
- Interior mut: Cell/RefCell.  
- Lifetime elision infers patterns.

