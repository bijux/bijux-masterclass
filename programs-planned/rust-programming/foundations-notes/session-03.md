# Session 3: Ownership, Moves, Copy/Clone, and RAII – Enforcing Safety Through Single Ownership

**Target Audience & Scope:** This series assumes familiarity with C/Python, basic memory models (e.g., stack/heap, pointers/references, GC internals), and command-line tools. It targets programmers with systems or dynamic language experience new to Rust. Tone balances explanation for beginners in Rust but avoids over-simplifying semantics for intermediates.

**Prerequisites:** Sessions 1 and 2 concepts (mindset, types, control flow, pattern matching); basic CLI with Option and structs.

**Conceptual Learning Goals:**  
- Trace ownership moves in code and predict compiler errors on use-after-move.  
- Distinguish Copy (implicit) from Clone (explicit) and know when to use each.  
- Implement Drop for custom cleanup and understand RAII's deterministic nature.  

**Mechanical Learning Goals:**  
- Pass and return ownership in functions, designing APIs around move vs clone trade-offs.  
- Use `dbg!` to inspect ownership and `cargo clippy` for ownership-related lints.  
- Read and fix errors related to moved values or unnecessary clones.  

**Design Learning Goals:**  
- Extend the CLI with heap-owned state like `Vec<T>`, showing how moves affect APIs and design.

**By the End of This Session, You Can:**  
- Trace ownership moves and predict compiler errors.  
- Distinguish Copy from Clone and apply them appropriately.  
- Implement Drop for RAII-style cleanup.  
- Design functions that take/return ownership.  
- Use dbg!/clippy.  
- Fix moved/unnecessary clone errors.  
- Extend CLI with Vec.

**Project Narrative:** Building on ownership and type control from Sessions 1–2, evolve the CLI into a Task Manager v2, using ownership with heap-allocated state to manage tasks.

**Time Estimate:** 60 minutes.

---

## Setup Checklist

Follow these to verify and extend your setup. Rustup manages toolchains.

1. **Verify Existing Setup**  
   ```bash
   cargo --version
   rustc --version
   cargo fmt
   ```
   Expect recent versions; update with `rustup update`. Confirm rust-analyzer (hover for types).

2. **Install and Use Clippy**  
   ```bash
   rustup component add clippy
   cargo clippy
   ```
   Lints for idiomatic code, e.g., unnecessary clones.

3. **Optional: Practice Adding a Dependency**  
   ```bash
   cargo add anyhow
   ```
   Adds to Cargo.toml for error handling (used later).

4. **Run Your Session 2 CLI**  
   ```bash
   cargo run
   ```
   Ensure Multi-Op Calculator v1 works.

> **Lab – Try This:** Run `cargo clippy` on your code. Apply suggestions (e.g., redundant clone).  
> **Solution:**  
> Clippy flags non-idiomatic patterns; fix and and re-run. Takeaway: Automated reviewer for efficiency.  
> Expected: Warnings like "redundant clone"; help: remove.

**Debug the Error Mini-Lab (Retention Test from Session 2):** Modify fizzbuzz to mismatch types in match. Predict error; fix.  
**Solution:** E0308; unify arms.

**Self-Assessment:**  
[ ] Verified setup and completed mini-lab.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

**Time Estimate:** 15 minutes.

---

## Part I: Ownership Rules – Single Owner, No More, No Less

**You Will Be Able To:**  
- Explain ownership laws and contrast with C/C++/Python.  
- Predict moves and compiler rejections.  
- Use terminology like binding consistently.

**Time Estimate:** 15 minutes.

**Ownership Laws (for this session):**  
- Each value has exactly one owner at a time.  
- Assigning or passing a non-Copy value moves ownership and invalidates the old binding.  
- Copy types are duplicated implicitly instead of moved.  
- When a value’s owner goes out of scope, its destructor (Drop) runs automatically.  
- (Preview for next session) References (&T, &mut T) never own data; they borrow from owners.

### Core Concept: Case 1 – Single Ownership and Moves

**Problem / Motivation:** C/C++ allows multiple aliases, leading to use-after-free or double-free. Python uses reference counting, risking cycles/leaks or overhead.

**Definition (Formal):** A value has a single owner responsible for its lifetime. Move: Transfer ownership, invalidating old binding.

**Mental Model (Simplified):** Assignment or function call moves ownership for non-Copy types; old binding unusable.

**Example (Compilable):** Valid move.  
```rust
fn main() {
    let s1 = String::from("owned");
    let s2 = s1;  // Move: s1 invalid
}
```

**Code Triple:**  
**Rust (Move enforces single owner):**  
```rust
let s1 = String::from("owned");
let s2 = s1;  // Move: s1 invalid
```  

**C/C++ (Aliases allowed):**  
```cpp
std::string s1 = "owned";
std::string* p1 = &s1;
std::string* p2 = &s1;  // Multiple aliases; risk if deleted
```  

**Python (Ref counting):**  
```python
s1 = "owned"  # Ref count 1
s2 = s1       # Ref count 2; CPython uses reference counting plus a cycle-detecting GC. Sharing is easy but lifetime is managed at runtime, not enforced at compile time.
```

**Rust Failure Variant:** Use after move.  
```rust
fn main() {
    let s1 = String::from("owned");
    let s2 = s1;
    println!("{s1}");
}
```

**Compiler Output (Key lines; messages may vary):**  
```
error[E0382]: borrow of moved value: `s1`
 --> src/main.rs:4:14
  |
2 | let s1 = String::from("owned");
  | -- move occurs because `s1` has type `String`, which does not implement the `Copy` trait
3 | let s2 = s1;
  | -- value moved here
4 | println!("{s1}");
  |          ^^^^^ value borrowed here after move
```  
Error code: E0382.

**Compiler Reasoning Steps:**  
- Identifies s1 owns String.  
- At assignment: Moves to s2.  
- At print: Borrow of moved value.  
- Rejects: Ensures single owner.

**Analysis:**  
- Ownership impact: Transfer invalidates old binding.  
- Performance: Move O(1); shallow stack copy.  
- Typical compiler error: E0382 (use after move).

**ASCII Diagram: Memory Model (Stack/Heap)**  
```
Stack: s1 { ptr --> Heap: "owned", len:5, cap:5 }
After move: s2 { ptr --> Heap: "owned" }, s1 invalid
```

**Ownership Timeline Diagram (x-axis = scope):**  
```
Scope start --------------------------- Scope end
s1 owns ------------------ invalid
                 s2 owns --------------- drop
Move here ^
```

**Micro-Challenge Variations:** Predict: Move a scalar like i32. Compiles after move?  

**Solution to Micro-Challenge:** Yes; i32 Copy, implicit duplicate.  

**Contrast:** C++ aliases risk; Python shared refs (GC cost).  

**Takeaway:** Single ownership eliminates aliasing bugs at compile time.

> **Lab – Try This:** Add `dbg!(s1);` before and after the move. Run `cargo run` and observe.  
> **Solution:** Before: Prints value; after: Compiler error on use after move.

[Design] **Reflection – Think:** How does this prevent use-after-free?  
[Answer] **Model Answer:** No dangling aliases; owner transfer invalidates old access.

[Semantics] **Think like the Compiler:** What constraints does the borrow checker infer after move? (Answer: Old binding invalid; new owns.)

### Core Concept: Case 2 – Copy vs Clone

**Problem / Motivation:** C/C++ implicit copies expensive; Python shared mutable surprises. Rust explicit explicit for heap, implicit for cheap.

**Definition (Formal):** Copy: Implicit bitwise duplicate for types where all fields Copy and no Drop. Clone: Explicit copy, potentially deep/custom.

**Mental Model (Simplified):** Copy auto for scalars (cheap); Clone manual for heap (expensive).

**Example (Compilable):** Explicit clone.  
```rust
fn main() {
    let s1 = String::from("clone me");
    let s2 = s1.clone();  // Deep copy
}
```

**Code Triple:**  
**Rust (Explicit clone):**  
```rust
let s1 = String::from("clone me");
let s2 = s1.clone();  // Deep copy
```  

**C/C++ (Copy ctor):**  
```cpp
std::string s1 = "clone me";
std::string s2 = s1;  // Conceptually this creates a new, independent string that owns its own buffer. Implementations may optimize small strings, but you should think of it as an implicit copy of the data.
```  

**Python (Mutable surprise):**  
```python
lst1 = [1,2]
lst2 = lst1  # Shared ref; mutate lst2 affects lst1
lst2.append(3)
# Now both names see the mutation:
print(lst1)  # [1, 2, 3]
print(lst2)  # [1, 2, 3]
```

**Rust Failure Variant:** No implicit clone.  
```rust
fn takes_ownership(s: String) { /* ... */ }
fn main() {
    let s = String::from("no clone");
    takes_ownership(s);
    println!("{s}");
}
```

**Compiler Output (Key lines; messages may vary):**  
```
error[E0382]: borrow of moved value: `s`
 --> src/main.rs:4:14
  |
2 |     let s = String::from("no clone");
  |         - move occurs because `s` has type `String`, which does not implement the `Copy` trait
3 |     takes_ownership(s);
  |                     - value moved here
4 |     println!("{s}");
  |              ^^^^^ value borrowed here after move
```  
Error code: E0382.

**Compiler Reasoning Steps:**  
- Checks type: String no Copy.  
- At call: Moves ownership.  
- At print: Use after move.  
- Rejects: Forces explicit clone.

**Analysis:**  
- Ownership impact: Copy duplicates; Clone explicit.  
- Performance: Copy O(1); Clone O(n) for heap.  
- Typical compiler error: E0382 (use after move).

**ASCII Diagram:** N/A.

**Micro-Challenge Variations:** Predict: Make struct Copy. Requirements?  

**Solution to Micro-Challenge:** All fields Copy, no Drop. Failing example: struct with String (no Copy).  

**Contrast:** C++ implicit copy; Python shared mut.  

**Takeaway:** Explicit clone forces awareness of costs.

> **Lab – Try This:** Time clone on large Vec with Instant. Compare to move.  
> **Solution:** Clone O(n); move O(1). Use --release for accurate.

[Performance] **Reflection – Think:** When is clone acceptable?  
[Answer] **Model Answer:** Small data or infrequent; otherwise borrow.

[Semantics] **Think like the Compiler:** What for Copy impl? (Answer: All fields Copy, no Drop; else illegal.)

**Performance Table: Move/Copy/Clone**  
| Operation | Time | Space | When Use |
|-----------|------|-------|----------|
| Move      | O(1) | O(1)  | Transfer ownership |
| Copy      | O(1) | O(1)  | Implicit for scalars |
| Clone     | O(n) | O(n)  | Explicit duplication |

### Core Concept: Case 3 – Drop and RAII

**Problem / Motivation:** C/C++ manual cleanup invites leaks/doubles. Python GC non-deterministic.

**Definition (Formal):** RAII: Resource init in ctor, cleanup in dtor (Drop trait).

**Mental Model (Simplified):** Auto drop at scope exit, reverse order.

**Example (Compilable):** Auto drop.  
```rust
{ let s = String::from("raii"); }  // Drop at scope end
```

**Code Triple:**  
**Rust (Auto drop):**  
```rust
{ let s = String::from("raii"); }  // Drop at scope end
```  

**C/C++ (Manual vs RAII):**  
```cpp
// Manual allocation style (error-prone)
char* s = new char[5];
// ... use s ...
delete[] s;  // must remember this

// RAII style with std::string
{
    std::string s2 = "raii";  // Destructor runs automatically at scope end
}
```  

**Python (GC):**  
```python
s = "raii"  # Lifetime managed by refcounts + GC; destruction timing may not align exactly with scope.
```

**Rust Failure Variant:** Double drop attempt.  
```rust
fn main() {
    let s = String::from("drop");
    drop(s);
    drop(s);
}
```

**Compiler Output (Key lines; messages may vary):**  
```
error[E0382]: use of moved value: `s`
 --> src/main.rs:4:10
  |
3 | drop(s);
  | - value moved here
4 | drop(s);
  | ^ value used here after move
```  
Error code: E0382.

**Compiler Reasoning Steps:**  
- At first drop: Moves ownership.  
- At second: Use after move.  
- Rejects: Prevents double drop.

**Analysis:**  
- Ownership impact: Drop when owner out of scope.  
- Performance: Drop O(1) + destructor cost.  
- Typical compiler error: E0382 (use after move).

**ASCII Diagram: Scope Drops**  
```
{ let a = ...; let b = ...; }  // Drop b, then a
```

**Ownership Timeline Diagram (x-axis = scope):**  
```
Scope start --------------------------- Scope end
a owns ------------------------------- drop a
b owns ------------------------------- drop b (reverse)
```

**Micro-Challenge Variations:** Predict: Impl Drop with print. When called?  

**Solution to Micro-Challenge:** At scope end.  

**Contrast:** C++ manual free; Python GC timing.  

**Takeaway:** Deterministic cleanup without manual calls.

> **Lab – Try This:** Nest scopes and observe drop order.  
> **Solution:** Inner first, then outer (LIFO).

[Design] **Reflection – Think:** How is RAII in Rust similar to Python’s `with` blocks and context managers?  
[Answer] **Model Answer:** Both give you a way to run setup code and guaranteed cleanup around a scope. In Python, `with` relies on runtime protocols; in Rust, the compiler enforces that `Drop` is called at scope end and you can’t forget to clean up.

[Semantics] **Think like the Compiler:** What constraints for Drop impl? (Answer: Runs at scope end, reverse order.)

**Anti-Pattern Box:** Returning ownership just to reuse variable – preview borrowing as better.

**Part I Checkpoint:** Explain move after use, Copy vs Clone, Drop timing.  
**You Can Now:**  
- Predict moves and errors.  
- Use Copy/Clone appropriately.

**Part I Quiz:** (5 MCQs + 1 open conceptual question)  
1. What after move? (a) Valid (b) Invalid (c) Copy  
   Answer: (b)  
2. Copy is? (a) Explicit (b) Implicit (c) Deep  
   Answer: (b)  
3. Drop called when? (a) Manual (b) Scope end (c) GC  
   Answer: (b)  
4. What is the performance of a move? (a) O(n) (b) O(1) (c) O(log n)  
   Answer: (b)  
5. True/False: Drop and Copy compatible.  
   Answer: False  
Open Conceptual: Explain single ownership benefit.  
Answer: Prevents aliasing bugs.

**Self-Assessment:**  
[ ] Completed all micro-challenges and reflections.  
[ ] Can explain the three cases to a peer.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part II: Ownership in Functions – Passing and Returning

**You Will Be Able To:**  
- Pass/return ownership in functions.  
- Design APIs around move/clone trade-offs.  
- Predict errors in function calls.

**Time Estimate:** 15 minutes.

**Transition Logic:** Ownership with data transfer.

### Part 2A: Ownership Transfer into Functions

**Problem / Motivation:** C/C++ pass-by-value copies or by-ref aliases; Python by-ref with mut surprises.

**Definition (Formal):** Passing by value moves ownership into function.

**Mental Model (Simplified):** Caller gives up ownership unless Copy or cloned.

**Example (Compilable):** Takes ownership.  
```rust
fn consume(s: String) { }  // Takes ownership
```

**Code Triple:**  
**Rust:**  
```rust
fn consume(s: String) { }  // Takes ownership
```  

**C/C++:**  
```cpp
void consume(std::string s) { }  // std::string s is passed by value, which conceptually makes a copy (though modern compilers can elide this with move semantics/RVO).
```  

**Python:**  
```python
def consume(s): pass  # Python passes references to objects; whether mutation is possible depends on the object (e.g., lists/dicts are mutable, str is not).
```

**Rust Failure Variant:** Use after transfer.  
```rust
fn main() {
    let s = String::from("transferred");
    consume(s);
    println!("{s}");
}
```

**Compiler Output (Key lines; messages may vary):**  
```
error[E0382]: borrow of moved value: `s`
 --> src/main.rs:4:14
  |
2 |     let s = String::from("transferred");
  |         - move occurs because `s` has type `String`, which does not implement the `Copy` trait
3 |     consume(s);
  |             - value moved here
4 |     println!("{s}");
  |              ^^^^^ value borrowed here after move
```  
Error code: E0382.

**Compiler Reasoning Steps:**  
- At call: Moves ownership.  
- At print: Borrow moved value.  
- Rejects: Prevents use after.

**Analysis:**  
- Ownership impact: Transfer to function.  
- Performance: Move O(1).  
- Typical compiler error: E0382 (borrow after move).

**ASCII Diagram: Scope Drops**  
N/A

**Micro-Challenge Variations:** Predict: Return ownership. Compiles?  

**Solution to Micro-Challenge:** Yes; moves back.  

**Contrast:** C++ copy; Python shared ref.  

**Takeaway:** Functions taking value require move/clone.

> **Lab – Try This:** Time a `clone` on a large `Vec<i32>` using `std::time::Instant`. Compare to a simple move (assignment).  
> **Solution:**  
> ```rust  
> use std::time::Instant;  
>   
> fn main() {  
>     let v = vec![0; 1_000_000];  
>   
>     let start = Instant::now();  
>     let _moved = v; // Just a move  
>     println!("Move took: {:?}", start.elapsed());  
> }  
> ```  
>   
> Then compare with:  
> ```rust  
> let v = vec![0; 1_000_000];  
> let start = Instant::now();  
> let _cloned = v.clone(); // Deep copy  
> println!("Clone took: {:?}", start.elapsed());  
> ```  
> You should see that clone() shows a noticeably larger duration than a simple move, especially for big vectors. The exact numbers don’t matter; the order-of-magnitude difference does. If you run in debug mode, timings will be noisy; in optimized builds (cargo run --release), the contrast is clearer. In optimized builds, the compiler might optimize away some of this code because _moved / _cloned are unused; treat the numbers as rough intuition, not a benchmark. The important bit: moves are O(1) pointer copies, clones of big collections are O(n) data copies.  
>   
> Takeaway: moves are just pointer copies; clones allocate and copy data.  
> (Don’t obsess over exact timings; the goal is to *feel* the difference.)

[Design] **Reflection – Think:** When take ownership?  
[Answer] **Model Answer:** When function consumes or owns long-term.

[Semantics] **Think like the Compiler:** What after ownership transfer? (Answer: Caller invalid; callee owns.)

### Part 2B: Ownership Out of Functions

**Problem / Motivation:** C/C++ return pointers risk dangles; Python GC.

**Definition (Formal):** Returning owned transfers to caller.

**Mental Model (Simplified):** Safe transfer; no dangle.

**Example (Compilable):** Returns owned.  
```rust
fn create() -> String { String::from("owned") }  // Transfers out
```

**Code Triple:**  
**Rust:**  
```rust
fn create() -> String { String::from("owned") }  // Transfers out
```  

**C/C++:**  
```cpp
char* create() { return new char[6]; }  // Caller must free
```  

**Python:**  
```python
def create(): return "owned"  # GC
```

**Rust Failure Variant:** Dangling return.  
```rust
fn dangle() -> &String {
    let s = String::from("dangle");
    &s
}
```

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
- Analyzes return: Borrow local.  
- Checks lifetime: Outlives owner.  
- Rejects: Prevents dangle.

**Analysis:**  
- Ownership impact: Transfer to caller.  
- Performance: Move O(1).  
- Typical compiler error: E0515 (ref to local).

**ASCII Diagram:** N/A.

**Micro-Challenge Variations:** Predict: Fix dangle. How?  

**Solution to Micro-Challenge:** Return String (owned).  

**Contrast:** C++ manual free; Python GC.  

**Takeaway:** Owned returns safe; borrows checked.

[Design] **Reflection – Think:** Ownership vs C++ unique_ptr?  
[Answer] **Model Answer:** Similar unique ownership, but Rust at lang level. Modern C++ has move semantics and std::unique_ptr that approximate Rust’s ownership model, but Rust builds these concepts into the language and enforces them consistently, whereas C++ relies more on conventions and careful use of libraries.

[Semantics] **Think like the Compiler:** What constraints for return ref? (Answer: Must outlive function.)

**Anti-Pattern Box:** Returning ownership just to reuse – preview borrowing as better.

**Part II Checkpoint:** What happens to a binding after its value is moved? When is `Copy` automatic? When is `Drop` called for a value in Rust?  
**Answers:**  
- The old binding becomes unusable; the compiler rejects any further access to prevent use-after-free-style bugs.  
- For types that are small and cheap to duplicate (like integers and other `Copy` types) and don’t implement Drop.  
- At the end of the value’s scope, in reverse order of declaration, so resources are released deterministically.

**You Can Now:**  
- Use blocks as expressions.  
- Trace moves in function arguments (e.g., passing `String` by value moves ownership).

**Part II Quiz:** (5 MCQs + 1 open conceptual question)  
1. Passing value does? (a) Borrow (b) Move (c) Copy  
   Answer: (b)  
2. Return owned? (a) Dangle (b) Transfer (c) Clone  
   Answer: (b)  
3. True/False: Use after consume.  
   Answer: False  
4. Performance of return move? (a) O(n) (b) O(1) (c) Variable  
   Answer: (b)  
5. True/False: Functions own params.  
   Answer: True (by value)  
Open Conceptual: Explain roundtrip ownership.  
Answer: Move in/out.

**Self-Assessment:**  
[ ] Traced moves and drops in examples.  
[ ] Completed labs and micro-challenges.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part III: Security and Performance – Ownership's Impact

**You Will Be Able To:**  
- Explain ownership's security benefits.  
- Analyze clone overhead.  
- Use tools for ownership lints.

**Time Estimate:** 15 minutes.

### Core Concept: Preventing Vulnerabilities

**Problem / Motivation:** Ownership stops memory bugs without runtime cost.

**Definition (Formal):** Ownership prevents UAF/double-free at compile time.

**Mental Model (Simplified):** Single owner; no invalid aliases.

**Example (Compilable):** N/A (conceptual).

**Code Triple (Use-After-Free):**  
**Rust (Rejected – use after move):**  
```rust
fn main() {
    let s = String::from("hi");
    let t = s;
    println!("{s}"); // use after move; Rust rejects this
}
```  

**C++ (Compiles; returns pointer to freed stack memory):**  
```cpp
std::string* leak() {
    std::string s = "hi";
    return &s;  // returns pointer to stack memory that will be freed
}
```  

**Python (No raw pointers, but no static guarantees):**  
```python
s = "hi"
t = s  # shared reference; CPython's refcounting plus GC prevent UAF,
       # but there's no compile-time check about aliasing or lifetime
```

**Rust Failure Variant:** The Rust code above.

**Compiler Output (Key lines; messages may vary):**  
```
error[E0382]: borrow of moved value: `s`
 --> src/main.rs:4:14
  |
2 |     let s = String::from("hi");
  |         - move occurs because `s` has type `String`, which does not implement the `Copy` trait
3 |     let t = s;
  |             - value moved here
4 |     println!("{s}"); // use after move; Rust rejects this
  |              ^^^^^ value borrowed here after move
```  
Error code: E0382.

**Compiler Reasoning Steps:**  
- Detects move.  
- At use: Borrow moved.  
- Rejects: Prevents UAF.

**Analysis:**  
- Ownership impact: No dangling aliases.  
- Performance: Compile-time checks no runtime overhead.  
- Typical compiler error: E0382 (borrow after move).

**ASCII Diagram:** N/A.

**Micro-Challenge Variations:** Predict: C++ equivalent with delete.  

**Solution to Micro-Challenge:** Dangling pointer; UAF if deref.  

**Contrast:** C++ runtime crash; Python GC safe but overhead.  

**Takeaway:** Safety without GC/bookkeeping.

> **Lab – Try This:** Trigger E0382 in your code and use compiler hints to fix.  
> **Solution:** Follow "value moved here" notes; clone or restructure.

[Semantics] **Reflection – Think:** Ownership vs C++ smart pointers?  
[Answer] **Model Answer:** Similar; Rust built-in, consistent.

[Semantics] **Think like the Compiler:** What prevents UAF? (Answer: Invalid after move.)

### Core Concept: Clone Overhead

**Problem / Motivation:** Indiscriminate clone hurts perf.

**Definition (Formal):** Clone: Explicit deep copy.

**Mental Model (Simplified):** O(n) for collections; use sparingly.

**Example (Compilable):** N/A (conceptual).

**Code Triple:** N/A.

**Rust Failure Variant:** N/A.

**Compiler Output:** N/A.

**Compiler Reasoning Steps:** N/A.

**Analysis:**  
- Ownership impact: Duplicate for multiple owners.  
- Performance: O(n); avoid hot paths.  
- Typical compiler error: N/A; Clippy warns redundant.

**ASCII Diagram:** N/A.

**Micro-Challenge Variations:** Predict: Clippy on unnecessary clone.  

**Solution to Micro-Challenge:** Warns; suggests remove.  

**Contrast:** C++ implicit; Python copy module.  

**Takeaway:** Clone mindful; tools help.

> **Lab – Try This:** Time clone on large Vec with Instant. Compare to move.  
> **Solution:** Clone O(n); move O(1). Use --release.

[Performance] **Reflection – Think:** Clone vs borrow teaser?  
[Answer] **Model Answer:** Clone copies; borrow views O(1).

[Performance] **Think like the Compiler:** What for redundant clone? (Answer: Clippy lint.)

**Clippy Walkthrough:** Run on redundant clone: warning: redundant clone; help: remove.

**Performance Table: Move/Copy/Clone**  
| Operation | Time | Space | When Use |
|-----------|------|-------|----------|
| Move      | O(1) | O(1)  | Transfer ownership |
| Copy      | O(1) | O(1)  | Implicit for scalars |
| Clone     | O(n) | O(n)  | Explicit duplication |

**Part III Checkpoint:** Explain security, clone impact.  
**You Can Now:**  
- Analyze ownership vulnerabilities.  
- Optimize with mindful clone.

**Part III Quiz:** (5 MCQs + 1 open conceptual question)  
1. Ownership prevents? (a) All bugs (b) Memory bugs (c) Logic bugs  
   Answer: (b)  
2. Clone performance? (a) O(1) (b) O(n) (c) O(log n)  
   Answer: (b)  
3. True/False: Clone for security.  
   Answer: False (for duplication)  
4. Tool for lints? (a) Cargo (b) Clippy (c) Fmt  
   Answer: (b)  
5. True/False: Overhead in hot loops.  
   Answer: True  
Open Conceptual: Explain clone when ok.  
Answer: Small/infrequent data.

**Self-Assessment:**  
[ ] Analyzed clone in code.  
[ ] Used Clippy.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part IV: Applied Ownership – Task List CLI v2

**You Will Be Able To:**  
- Extend CLI with heap state.  
- Handle ownership in functions.  
- Test ownership patterns.

**Time Estimate:** 15 minutes.

From Session 2 calculator, start Task Manager. Work with heap data.

### Checkpoint 1: Introduce Heap State with `Vec<Task>`

```rust
#[derive(Debug, Clone)]
struct Task {
    title: String,
    completed: bool,
}
```

Derive Clone to feel cost; later borrow.

```rust
fn main() {
    let mut tasks: Vec<Task> = Vec::new();
    tasks.push(Task { title: String::from("Task 1"), completed: false });
    // ...
}
```

### Checkpoint 2: Broken Attempt – Move into Function

```rust
fn print_tasks(ts: Vec<Task>) {
    println!("{:?}", ts);
}

fn main() {
    let mut tasks: Vec<Task> = Vec::new();
    tasks.push(Task {
        title: String::from("Task 1"),
        completed: false,
    });

    print_tasks(tasks);
    println!("Again: {:?}", tasks);  // Error: moved
}
```

**Compiler Output (Key lines; messages may vary):**  
```
error[E0382]: borrow of moved value: `tasks`
 --> src/main.rs:13:25
  |
7  | let mut tasks: Vec<Task> = Vec::new();
  |     --------- move occurs because `tasks` has type `Vec<Task>`, which does not implement the `Copy` trait
...
12 | print_tasks(tasks);
  |             ----- value moved here
13 | println!("Again: {:?}", tasks);  // Error: moved
  |                         ^^^^^^ value borrowed here after move
```  
Error code: E0382.

### Checkpoint 3: Fix with Clone or Return

Option 1: Clone.  
```rust
print_tasks(tasks.clone());
```

[Performance] **Reflection – Think:** Cost for large tasks? Avoid how?  
[Answer] **Model Answer:** O(n); borrow (next session).

Option 2: Roundtrip.  
```rust
fn print_and_return(ts: Vec<Task>) -> Vec<Task> {
    println!("{:?}", ts);
    ts
}
let tasks = print_and_return(tasks);
```

> **Lab – Try This:**  
> 1. Add:  
> ```rust
> fn add_task(mut tasks: Vec<Task>, title: String) -> Vec<Task> {
>     tasks.push(Task { title, completed: false });
>     tasks
> }
> ```  
> 2. Use:  
> ```rust
> tasks = add_task(tasks, String::from("New Task"));
> ```  
> 3. Print before/after; observe moves.  

[Design] **Reflection – Think:** Clumsy? Borrow fix?  
[Answer] **Model Answer:** Yes; move/clone every call. Borrow temporary access.

**Part IV Checkpoint:** Explain move in functions, fixes.  
**You Can Now:**  
- Extend CLI with Vec.  
- Handle ownership transfers.

**Part IV Quiz:** (5 MCQs + 1 open conceptual question)  
1. Function takes Vec requires? (a) Borrow (b) Move/clone (c) Copy  
   Answer: (b)  
2. True/False: Return transfers back.  
   Answer: True  
3. Clone for large Vec? (a) Efficient (b) Costly (c) Free  
   Answer: (b)  
4. Performance of roundtrip? (a) O(n) (b) O(1) (c) Variable  
   Answer: (b)  
5. True/False: Borrow teaser compiles.  
   Answer: True  
Open Conceptual: Explain clumsy owning API.  
Answer: Move/clone per call; borrow avoids.

**Self-Assessment:**  
[ ] Built Task CLI v2.  
[ ] Fixed div by zero case.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Exercises: Tiered Reasoning

### Tier 1: Concept Rebuilds

1. Ownership Annotation  
   Annotate moves:  
   ```rust
   fn takes_vec(v: Vec<i32>) { /* ... */ }

   let v = vec![1];  // v owns the Vec
   takes_vec(v);     // move: ownership transfers into the function
   // Can I use v here? Why / why not?
   ```  
   **Solution:** No; moved into function.

2. Drop Impl  
   Simple logger prints on drop.  
   **Solution:**  
   ```rust
   struct Logger;
   impl Drop for Logger {
       fn drop(&mut self) { println!("Dropping!"); }
   }
   { let _log = Logger; }  // Prints
   ```

3. Copy vs non-Copy  
   Program with String/i32; predict compiles.  
   **Solution:** i32 yes (Copy); String no (move).

### Tier 2: Comparative Rewrites

1. C++ Manual Free to Rust  
   Rewrite malloc/free as Rust.  
   **Solution:**  
   ```rust
   { let buf = vec![0u8; 1024]; } // auto drop
   ```  
   Diff: No manual free.

2. Python List Share to Rust  
   Shared list to explicit clone.  
   **Solution:**  
   ```rust
   let nums1 = vec![1, 2, 3];
   let nums2 = nums1.clone();
   ```  
   Diff: Explicit; no mut surprise.

### Tier 3: Challenge Extensions

1. Custom Drop  
   File struct prints on drop.  
   **Solution:**  
   ```rust
   struct File { name: String }
   impl Drop for File {
       fn drop(&mut self) { println!("Closing: {}", self.name); }
   }
   { let _f = File { name: "example.txt".to_string() }; }
   ```

2. Ownership Chain  
   Multi-fn transfer.  
   **Solution:**  
   ```rust
   fn fn1(s: String) -> String { s }
   fn fn2(s: String) -> String { fn1(s) }
   fn fn3(s: String) -> String { fn2(s) }
   ```

**Self-Assessment:**  
[ ] Completed one per tier.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Recap and Synthesis Reflection

**Table 1: Rust Rules vs Other Languages Tradeoffs** (Expanded)  
| Rust Rule              | C++ Failure Mode      | Python Cost                     |
|------------------------|-----------------------|---------------------------------|
| Ownership & Moves      | Double free, aliases  | GC overhead, no compile proof   |
| Borrowing & Lifetimes  | Dangling refs         | Runtime ref counting            |
| Mut Exclusivity        | Data races            | GIL limits parallelism          |
| Drop Determinism       | Memory leaks          | Nondeterministic GC             |
| Error Handling (Option/Result) | UB or exceptions | Dynamic errors at runtime       |
| Expressions            | Verbose assignments   | Step-by-step, no block yield    |
| Traits (e.g., Copy)    | Manual copies         | Implicit refs                   |

**Self-Quiz:** (Design-level)  
1. Why invalidate after move?  
2. Copy vs Clone difference?  
3. Drop called when?  
Answers:  
1. Ensure single owner.  
2. Implicit cheap vs explicit deep.  
3. Scope end, reverse.

**Final Takeaway:** Ownership foundation for secure/performant code without runtime cost.

**By Session End:**  
- Trace moves.  
- Distinguish Copy/Clone.  
- Implement Drop.  
- Design owning APIs.  
- Use dbg!/clippy.  
- Fix moved/unnecessary clone errors.  
- Extend CLI with Vec.

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

**Primary References:** Rust Book Ch. 4 (Ownership), Ch. 10 (Lifetimes), Ch. 11 (Testing).  
**Suggested Deep Dives:** Rustonomicon (ownership semantics); RFCs for NLL.

**Further Reading:** Rust Book Ch. 4 (Ownership), Ch. 15 (Smart Pointers).

**Concept Map:** (Text-based ASCII)  
Ownership  
  ├── Moves (O(1) transfer)  
  │   └── Invalidate old  
  ├── Copy (implicit)  
  ├── Clone (explicit)  
  └── Drop (scope end)  
      └── Safety (no UAF/double-free)  
          └── Performance (O(1) moves)  
              └── Applied (Task CLI v2)

**Bridge to Session 4:** Ownership requires move/clone; borrowing temporary access without. Extend Task CLI with borrows.

**Self-Assessment:**  
[ ] Reviewed concept map and quiz answers.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

**Deep Dive Appendix:**  
- Moves shallow: stack copy.  
- Copy if no Drop.  
- Panic unwind runs Drop.  
- Async Drop caveat: Determinism in async await contexts (drops after .await).  
- Why Copy + Drop = illegal: Double-free risk.
