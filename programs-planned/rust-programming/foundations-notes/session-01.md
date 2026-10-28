# Session 1: Rust's Mindset – Correctness Through Ownership and Compile-Time Guarantees

**Target Audience & Scope:** This series assumes familiarity with C/Python, basic memory models (e.g., stack/heap, pointers/references, GC internals), and command-line tools. It targets programmers with systems or dynamic language experience new to Rust. Tone balances explanation for beginners in Rust but avoids over-simplifying semantics for intermediates.

**Prerequisites:** Basic programming knowledge in C or Python; familiarity with memory management concepts.

**Conceptual Learning Goals:**  
- Shift thinking from ‘who frees memory’ to ‘who owns data and when.’  
- Understand compile-time ownership/borrowing checks with no runtime cost (though runtime includes bounds checks, destructors; deterministic only in synchronous flow—async futures alter timing).  
- Progressive framing: Session 1 focuses on what & why; later sessions cover representation/cost, design trade-offs, and abstractions/lifetimes.

**By the End of This Session, You Can:**  
- Install Rust and verify your setup.  
- Create and run a basic project with Cargo.  
- Understand how the compiler catches errors early through ownership and borrowing rules.  
- Trace ownership transfers and predict compiler rejections for dangling refs, double frees, and data races.

**Project Narrative:** Build a safe arithmetic CLI v0, applying ownership to prevent common bugs.

**Time Estimate:** 60 minutes.

---

## Setup Checklist

Follow these procedural steps to get Rust running. Verify each one. Rustup is preferred as a multi-toolchain manager, allowing easy switches between stable, beta, and nightly versions (e.g., const generics on nightly).

1. **Install Rust via rustup**  
   - Linux/macOS (bash terminal):  
     `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`  
     Follow prompts (default options). Troubleshooting: If curl fails due to proxy issues, fix the proxy configuration or download the installer manually from the official site https://rustup.rs.  
   - Windows: Download installer from [https://www.rust-lang.org/tools/install](https://www.rust-lang.org/tools/install). Run as Administrator for PATH; verify in new PowerShell.  
   Restart terminal after. Update via `rustup update`.

2. **Verify Tools**  
   `rustc --version`  
   `cargo --version`  
   Expected Output: `rustc 1.91.0` or later, `cargo 1.91.0` or later. If older, run `rustup update`.

3. **Set Up Editor with rust-analyzer**  
   - VS Code: Install Extensions > "rust-analyzer" > install > restart.  
   - Vim/Neovim: Use rust-analyzer via coc-rust-analyzer, rust-tools.nvim, or equivalent for completion and diagnostics.  
   - Emacs: Use lsp-mode or eglot with rust-analyzer.  
   - IntelliJ/CLion: Install Rust plugin for IDE support.

4. **Create First Project**  
   `cargo new hello_rust`  
   `cd hello_rust`  
   Edit `src/main.rs`:  
   ```rust
   fn main() {
       println!("Hello, Rust!");
   }
   ```  
   Run:  
   `cargo run`  
   Expected Output: "Hello, Rust!"

> **Lab – Try This:** (Predict → Run → Reflect) Predict what happens if you change `println!` to `printl!` in `main.rs`. Run `cargo check` and note the error. Reflect: How does this demonstrate compile-time macro resolution?  
> **Solution:**  
> Prediction: Compiler rejects unresolved macro.  
> rust-analyzer shows red underline: "Unresolved macro `printl!`".  
> Compiler output (key lines; messages may vary by version):  
> ```
> error[E0433]: failed to resolve: use of undeclared crate or module `printl`
> ```  
> Expected Output: No binary produced.  
> Reflection Model Answer: Macros like `println!` are expanded at compile time; typos fail early, preventing runtime surprises. Takeaway: Rust's strong macro hygiene.

> **Common Error Box:** Proxy? Fix config or manual download.

**Self-Assessment:**  
[ ] Verified Rust installation and ran first project.  
[ ] Completed the lab and reflected on macro errors.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

**Time Estimate:** 15 minutes.

**Appendix: Platform-Specific Notes**  
- Windows: Run installer as admin for PATH setup; verify in new PowerShell.  
- Unix: Ensure curl uses HTTPS; manual download if needed.

---

## Part I: Rust's Reason for Being – Why Trade Convenience for Correctness?

**You Will Be Able To:**  
- Explain three key safety guarantees of Rust compared to C/C++ and Python.  
- Predict compiler errors for dangling references, double frees, and data races.  
- Contrast memory models using a comparative table.

**Time Estimate:** 15 minutes.

Examine three cases where C/C++ allows bugs and Python hides issues with runtime costs, but Rust rejects them at compile time. Use "binding" consistently (avoid “variable” when ownership semantics matter). Bindings associate names to values; they may own or borrow. We'll revisit how these rules apply in async contexts (Futures) and multithreading later.

**Memory Model Comparison Table (Rust / C++ / Python):**  
| Language | Memory Model                  | Safety Mechanism          | Trade-offs                                                                 |
|----------|-------------------------------|---------------------------|----------------------------------------------------------------------------|
| Rust     | Affine (single ownership, moves/borrows) | Compile-time borrow checker | No runtime overhead for ownership/borrowing checks; deterministic destruction in sync code. |
| C++      | Manual (pointers, RAII)       | Programmer responsibility | UB risks like double free heap corruption (e.g., real-world exploits like IE zero-day use-after-free). |
| Python   | Refcounted + tracing GC       | Runtime GC                | Pauses that can be on the order of tens to hundreds of milliseconds in large heaps, depending on workload; GIL limits threads, multiprocessing parallels but with higher overhead (no shared memory, forks). As of 2025, Python 3.14 has experimental no-GIL via PEP 703. |

### Core Concept: Case 1 – Dangling Reference

**Problem / Motivation:** In C/C++, returning pointers to locals compiles but leads to UB such as crashes or corruption. Python avoids raw pointers via GC, but incurs runtime overhead. Rust rejects at compile time for safety without cost.

**Definition (Formal):** A dangling reference occurs when a borrow (`&T`) outlives its owner, pointing to deallocated memory.  

**Mental Model (Simplified):** Function scope deallocates stack/heap; returning a borrow escapes this, invalidating it. Note: Compiler may optimize, but semantics equivalent to shallow stack copy for moves.  

**Example (Compilable):** Valid Rust version: Return owned value instead.  
```rust
fn not_dangling() -> i32 {
    let x = 42;
    x  // Ownership transferred (move O(1))
}

fn main() {
    let val = not_dangling();
    println!("{}", val);
}
```  

**Code Triple:**  
**Rust (Rejected—see failure below):**  
```rust
fn dangling() -> &i32 {
    let x = 42;
    &x
}

fn main() {
    let ptr = dangling();
    println!("{}", ptr);
}
```  

**C++ (Compiles, UB—demonstrated with runtime crash):**  
```cpp
int* dangling() {
    int x = 42;
    return &x;
}

int main() {
    int* p = dangling();
    std::cout << *p;  // Likely crashes or prints garbage (UB)
}
```  

**Python:** Doesn't expose raw pointers; uses GC and references, so this bug doesn't appear, but pays runtime GC cost (reference counting for non-cyclic objects deterministic, tracing GC for cycles with pauses).

**Rust Failure Variant:** See code triple above.

**Compiler Output (Key lines; messages may vary):**  
```
error[E0106]: missing lifetime specifier
error[E0515]: cannot return reference to local variable `x`
```  
Error code: E0106, E0515.

**Compiler Reasoning Steps:**  
- Parses signature: Reference return without lifetime.  
- Analyzes body: Borrow from local `x`.  
- Checks lifetimes: Borrow exceeds `x`'s scope.  
- Rejects: Prevents dangling access.

**Analysis:**  
- Ownership impact: Borrow can't outlive owner.  
- Performance: Compile-time check O(1) per borrow (borrow graph size typically small).  
- Typical compiler error: E0106/E0515 (lifetime mismatch).

**ASCII Diagram of Stack → Deallocation → Dangling Ref:**  
```
Function Scope:
  Stack Frame:
    [x: 42]
  Borrow: &x --> x
End Scope:
  Stack popped, x deallocated
Outside Use:
  &x --> ??? (dangling, rejected)
```

**Micro-Challenge Variations:** Predict: Does changing the return to `-> &'static i32` compile? Why or why not? (Hint: `'static` denotes a lifetime that lasts the entire program.) Change to Box<i32> (heap alloc).  

**Solution to Micro-Challenge:** No for &'static, `x` not 'static. Fix with `static X: i32 = 42; &X`. For Box: No, Box owns heap but drops on return; borrow outlives. Fix: Return Box<i32>.  

**Contrast:** C++ allows UB; Python GC hides but with cost. Real-world C++ exploit: Double free → heap corruption, e.g., IE zero-day use-after-free.

**Takeaway:** Rust never lets a borrowed reference outlive its owned value; C++ allows it, leading to UB; Python hides the issue behind GC.

[Design] **Reflection – Think:** Consider how this rule influences API design in a large codebase (hint: encourages returning owned values for safety).  
[Answer] **Model Answer:** Encourages returning owned values (e.g., String) for safety, reduces lifetime bugs in complex systems.

[Semantics] **Think like the Compiler:** What constraints must the borrow checker infer for the reference in `fn dangling() -> &i32`? (Answer: The reference's lifetime must be tied to something that outlives the function, but `x` doesn't.)

### Core Concept: Case 2 – Double Free

**Problem / Motivation:** C/C++ manual memory management allows double deletes, corrupting heaps and causing UB. Python GC automates deallocation but introduces pauses. Rust rejects at compile time via moves.

**Definition (Formal):** Attempting to drop the same owned value twice, leading to invalid memory access.  

**Mental Model (Simplified):** Moves transfer ownership (shallow bitwise copy of the stack struct, heap unchanged); old binding invalid.  

**Example (Compilable):** Valid with Clone (explicit deep copy, O(n)).  
```rust
fn main() {
    let s = String::from("data");
    let s2 = s.clone();  // Deep copy heap
    drop(s2);
    drop(s);
}
```  

**Code Triple:**  
**Rust (Rejected):**  
```rust
fn main() {
    let s = String::from("data");
    drop(s);
    drop(s);
}
```  

**C++ (Compiles, UB—demonstrated with runtime corruption):**  
```cpp
void double_free() {
    int* p = new int(42);
    delete p;
    delete p;  // Heap corruption, potential crash
}
```  

**Python:** GC handles—no manual free, but collection pauses (reference counting immediate for non-cycles, tracing GC for cycles with pauses).

**Rust Failure Variant:** See code triple above.

**Compiler Output (Key lines; messages may vary):**  
```
error[E0382]: use of moved value: `s`
```  
Error code: E0382.

**Compiler Reasoning Steps:**  
- Scans bindings: `s` owns String.  
- At first drop: Moves ownership.  
- At second drop: Detects use of moved value.  
- Rejects: Ensures single ownership.

**Analysis:**  
- Ownership impact: Move invalidates old binding.  
- Performance: Move O(1); Clone O(n) for heap data.  
- Typical compiler error: E0382 (use after move).

**ASCII Diagram: Full Stack/Heap Visual**  
```
Before:
  Stack: s [ptr, len, cap]
  Heap:  --> "data"
After drop(s):
  Stack: s invalid
  Heap: Freed
Second drop: Rejected
```

**Micro-Challenge Variations:** Predict: For i32 (Copy), compiles? Why? Add non-Copy composite (e.g., Bad struct).  

**Solution to Micro-Challenge:** Yes for i32, duplicates no move. For Bad: Move rejects second use.  

**Contrast:** C++ UB (heap corruption); Python GC (acyclic deterministic, cycles delay).  

**Takeaway:** Ownership and moves make double free impossible in safe Rust; C++ requires manual vigilance; Python GC adds runtime cost.

[Design] **Reflection – Think:** Consider the flexibility loss from this rule (hint: can't "share" without explicit types like `Arc`).  
[Answer] **Model Answer:** Can't "share" without explicit types like `Arc`; gains predictability in large systems.

[Semantics] **Think like the Compiler:** What does the borrow checker track after the first `drop(s)`? (Answer: Ownership moved; any further use of `s` is a moved value error.)

### Core Concept: Case 3 – Data Race Teaser

**Problem / Motivation:** C/C++ allows unsynchronized shared mutable access, leading to races. Python's GIL serializes but limits parallelism. Rust rejects at compile time.

**Definition (Formal):** Unsynchronized simultaneous mutable access in concurrent code.  

**Mental Model (Simplified):** Mutable borrows exclusive; no aliasing during mutation.  

**Example (Compilable):** Valid with sync (teaser).  
```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let shared = Arc::new(Mutex::new(0));
    let shared1 = shared.clone();
    let h1 = thread::spawn(move || *shared1.lock().unwrap() += 1);
    let shared2 = shared.clone();
    let h2 = thread::spawn(move || *shared2.lock().unwrap() += 1);
    h1.join().unwrap();
    h2.join().unwrap();
}
```  

**Code Triple:**  
**Rust (Rejected):**  
```rust
fn main() {
    let mut x = 0;
    let r1 = &mut x;
    let r2 = &mut x;  // Exclusive mut
    *r1 += 1;
    *r2 += 1;
}
```  

**C++ (Compiles, race if threaded—demonstrated):**  
```cpp
#include <thread>

int x = 0;
void inc1() { x += 1; }
void inc2() { x += 1; }

int main() {
    std::thread t1(inc1);
    std::thread t2(inc2);
    t1.join(); t2.join();  // Potential race, x may not be 2
}
```  

**Python (GIL serializes in threads):**  
```python
import threading
x = 0
def inc():
    global x
    x += 1  # GIL prevents true races but limits parallelism
t1 = threading.Thread(target=inc)
t2 = threading.Thread(target=inc)
t1.start(); t2.start()
t1.join(); t2.join()
```

**Rust Failure Variant:** See code triple above.

**Compiler Output (Key lines; messages may vary):**  
```
error[E0499]: cannot borrow `x` as mutable more than once at a time
```  
Error code: E0499.

**Compiler Reasoning Steps:**  
- Identifies `&mut x`: Exclusive mutable borrow.  
- At second `&mut x`: Checks for overlapping mutable borrows.  
- Rejects: Enforces "aliasing XOR mutability" axiom.

**Analysis:**  
- Ownership impact: Exclusive mutable borrows prevent aliasing.  
- Performance: Compile-time check O(1).  
- Typical compiler error: E0499 (multiple mutable borrows).

**ASCII Diagram: Exclusive Mutable Borrow**  
```
Owned: x (mutable)
Borrow1: &mut x --> x (exclusive lock)
Borrow2: &mut x --> Rejected (no aliasing during mutation)
```

**Micro-Challenge Variations:** Predict: Multiple immutable borrows (&x, &x) compile? How to allow shared mutable? (Hint: Synchronization primitives.)  

**Solution to Micro-Challenge:** Yes for multiple &T (immutable). For shared mut: Use `Mutex` or `RwLock`.  

**Contrast:** C++ needs manual locks; Python GIL limits threads (multiprocessing workaround adds overhead).  

**Takeaway:** Mutable exclusivity prevents races; C++ manual; Python GIL/multiprocessing.

[Design] **Reflection – Think:** Consider the trade-off of this rule (hint: flexibility for predictability in large systems).  
[Answer] **Model Answer:** Flexibility for predictability in large systems; forces sync design upfront.

[Semantics] **Think like the Compiler:** What constraints must the borrow checker infer for two `&mut x`? (Answer: Exclusive access; second borrow overlaps, violating mutability rule.)

**Part I Checkpoint:** You should now explain: Why dangling references fail, how moves prevent double free, mutable borrow rule.  
**You Can Now:**  
- Predict and fix ownership-related compiler errors.  
- Contrast Rust's compile-time safety with C++ UB and Python runtime costs.

**Part I Quiz:** (5 MCQs + 1 open conceptual question)  
1. Why does Rust reject returning a reference to a local? (a) Syntax error (b) Borrow outlives owner (c) Runtime panic  
   Answer: (b)  
2. What does a move do for a `String`? (a) Deep copy heap (b) Shallow copy stack struct (c) Reference count  
   Answer: (b)  
3. True/False: Rust allows multiple mutable borrows simultaneously.  
   Answer: False  
4. What is the performance of a move? (a) O(n) (b) O(1) (c) O(log n)  
   Answer: (b)  
5. True/False: Python's GIL allows true parallelism in threads.  
   Answer: False  
Open Conceptual: Explain how exclusive mutability prevents data races.  
Answer: No aliasing during mutation ensures synchronized access.

**Self-Assessment:**  
[ ] Completed all micro-challenges and reflections.  
[ ] Can explain the three cases to a peer.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part II: The Rust Evaluation Model – Expressions, Ownership, and Scopes

**You Will Be Able To:**  
- Distinguish expressions from statements and use them for value flow.  
- Trace ownership moves and drops in scopes.  
- Predict type mismatches in block expressions.

**Time Estimate:** 15 minutes.

### Part 2A: Expressions vs Statements

**Problem / Motivation:** Many languages separate statements from expressions, leading to verbose code. Rust unifies for concise constructs. C/C++ lack block yields; Python is dynamic.

**Definition (Formal):** Expressions evaluate to values; statements perform actions and yield unit `()`.  

**Mental Model (Simplified):** Blocks/loops/if/match are expressions if no trailing semicolon on last item.  

**Example (Compilable):**  
```rust
fn main() {
    let value = {
        let a = 10;
        a + 20
    };
    println!("{}", value);  // 30
}
```  

**Code Triple:**  
**Rust:**  
```rust
let value = {
    let a = 10;
    a + 20
};
```  

**C++ (No block yield):**  
```cpp
int value;
{
    int a = 10;
    value = a + 20;
}
```  

**Python (Step-by-step):**  
```python
a = 10
value = a + 20
```  

**Rust Failure Variant:** (Full compilable snippet)  
```rust
fn main() {
    let value: i32 = {
        42;
    };
}
```  

**Compiler Output (Key lines):**  
```
error[E0308]: mismatched types
```  
Error code: E0308.  

**Compiler Reasoning Steps:**  
- Parses block: Last item with ; yields `()`.  
- Checks type: `()` vs expected `i32`.  
- Rejects: Enforces type safety.

**Analysis:**  
- Ownership impact: Expressions can move values.  
- Performance: Evaluation O(1).  
- Typical compiler error: E0308 (mismatched types).

**ASCII Diagram: Block Evaluation (Multiline ASCII)**  
```
Block {  
  let a = 10;  --> ()  // Statement  
  a + 20       --> i32 // Yielded as expression  
} --> i32  
```

**Micro-Challenge Variations:** Predict: Add ; after `a + 20`. What error? How to fix? What if block empty?  

**Solution to Micro-Challenge:** Error: Mismatched `()` vs `i32`. Fix: Remove ;. Empty yields `()`.  

**Contrast:** C++ no block yield; Python dynamic.  

**Takeaway:** Expressions yield values; statements yield `()`—encourages functional code.

> **Lab – Try This:** (Predict → Run → Reflect) Rewrite the C++ assignment as a Rust block. Compile, add ;, observe.  
> **Solution:**  
> ```rust
> let value = {
>     let a = 10;
>     a + 20
> };
> ```  
> Add ;: Yields `()`, type mismatch. Expected Output: No build on mismatch. Reflection Model Answer: Encourages value flow without temps.

[Semantics] **Reflection – Think:** Consider how this encourages functional style (hint: chaining yields, fewer temp vars).  
[Answer] **Model Answer:** Chaining yields, less temp vars; values from control flow.

**Table: Semicolon Impact on Expression Type**  
| With Semicolon | Without Semicolon | Type Yielded |
|----------------|-------------------|--------------|
| Yes            | No                | ()          |
| No             | Yes               | Value type  |

[Semantics] **Think like the Compiler:** What type does the block infer if the last expression is omitted? (Answer: `()` unit type.)

### Part 2B: Ownership and Moves

**Problem / Motivation:** C/C++ copies/pointers risk leaks/aliases. Python references with GC hide ownership but add cost. Rust uses moves for single ownership.

**Definition (Formal):** Ownership: Single binding controls resource lifetime and access. Move: Transfer ownership without copy.  

**Mental Model (Simplified):** Assignment/pass moves for non-Copy; invalidates old. For Copy: Duplicate.  

**Example (Compilable):** Before/after clone vs borrow (teaser).  
```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1.clone();  // Clone O(n)
    println!("{s1} {s2}");  // Both valid
}
```  

**Code Triple:**  
**Rust (Move):**  
```rust
let s1 = String::from("hello");
let s2 = s1;
```  

**C++ (Copy or pointer):**  
```cpp
std::string s1 = "hello";
std::string s2 = s1;  // Deep copy
```  

**Python (Ref):**  
```python
s1 = "hello"
s2 = s1  // Shared reference
```

**Rust Failure Variant:** (Full)  
```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1;
    println!("{s1}");
}
```  

**Compiler Output:** E0382.  

**Compiler Reasoning Steps:**  
- `s1` owns String.  
- `s2 = s1`: Moves ownership.  
- `println!("{s1}")`: Attempts borrow of moved value.  
- Rejects: Invalidates old binding.

**Analysis:**  
- Ownership impact: Move transfers, invalidates old.  
- Performance: Move O(1); Clone O(n).  
- Typical compiler error: E0382 (use after move).

**ASCII Diagram: Ownership Move (Multiline ASCII)**  
```
Before:  
  Stack: s1 [ptr, len, cap]  
  Heap:  --> "hello"  
After move to s2:  
  Stack: s2 [ptr, len, cap], s1 invalid  
  Heap:  --> "hello" (unchanged)  
```

**Micro-Challenge Variations:** Predict: `let x = 5; let y = x; println!("{x}");` compile? Why? Non-Copy composite (struct with String).  

**Solution to Micro-Challenge:** Yes, i32 Copy. For composite: Move rejects use after.  

**Contrast:** C++ deep copy or pointer (alias risk); Python shared ref (GC cost). C++ std::move discussion: Explicit transfer like Rust move.  

**Takeaway:** Moves ensure single ownership; `Copy` for cheap duplication.

[Semantics] **Reflection – Think:** Consider how this prevents aliasing (hint: no multiple owners for mutable data).  
[Answer] **Model Answer:** No multiple owners for mutable data; clear state.

[Semantics] **Think like the Compiler:** What does the borrow checker infer after `s2 = s1`? (Answer: Ownership transferred; s1 no longer valid for borrows or uses.)

### Part 2C: Scopes and Deterministic Drop

**Problem / Motivation:** C/C++ manual cleanup risks leaks. Python GC nondeterministic. Rust uses scopes for deterministic drops.

**Definition (Formal):** Scopes define lexical lifetimes; Drop trait called at end for deterministic cleanup.  

**Mental Model (Simplified):** Drops in reverse declaration order at scope end; like RAII but enforced.  

**Example (Compilable):** Custom Drop impl.  
```rust
struct File { fd: i32 }  // Simulated
impl Drop for File {
    fn drop(&mut self) { println!("Closing FD {}", self.fd); }  // Close resource
}
fn main() {
    {
        let f = File { fd: 42 };
    }  // Drop called here
}
```  

**Code Triple:**  
**Rust:**  
```rust
{
    let s = String::from("scoped");
}  // s dropped here → memory reclaimed deterministically
```  

**C++ (RAII similar):**  
```cpp
{
    std::string s = "scoped";
}  // Destructor called here
```  

**Python (GC eventual):**  
```python
s = "scoped"  # GC later, nondeterministic
```

**Rust Failure Variant:** Borrow across scopes (full).  
```rust
fn main() {
    let ref_s;
    {
        let s = String::from("data");
        ref_s = &s;
    }
    println!("{ref_s}");
}
```  

**Compiler Output:** E0597.  

**Compiler Reasoning Steps:**  
- Inner scope: `s` owns, `ref_s` borrows.  
- Scope end: Drops `s`.  
- Outer use: Borrow outlives owner.  
- Rejects: Lifetime violation.

**Analysis:**  
- Ownership impact: Borrows can't cross owner drops.  
- Performance: Drop O(1) typically.  
- Typical compiler error: E0597 (borrow outlives owner).

**ASCII Diagram: Scope Trace (Multiline)**  
```
Outer scope  
  Inner scope:  
    let s = ... --> Alloc own  
  Inner end: Drop s --> Free (reverse if multiple)  
Outer: No s  
```

**Micro-Challenge Variations:** Predict: Two vars in scope, drop order? (let a; let b;) Shadowing vs mut.  

**Solution to Micro-Challenge:** b then a (reverse). Shadow new binding; mut changes existing.  

**Contrast:** C++ RAII destructor (direct compare: ~RAII() { free(); }); CPython destruction vs cycle GC (acyclic deterministic, cycles delay).  

**Takeaway:** Scopes ensure drop; deterministic cleanup.

[Design] **Reflection – Think:** Contrast with C++ RAII (hint: similar drop, but Rust enforces no misses).  
[Answer] **Model Answer:** Similar drop, but Rust compiler enforces no misses.

**Part II Checkpoint:** You should explain: Semicolon changes type, move semantics, drop timing.  
**You Can Now:**  
- Use blocks as expressions.  
- Trace moves in function arguments (e.g., passing `String` by value moves ownership).

**Part II Quiz:** (5 MCQs + 1 open conceptual question)  
1. What does a semicolon do to an expression? (a) Yields value (b) Yields `()` (c) Syntax error  
   Answer: (b)  
2. When does drop occur? (a) GC pause (b) Scope end (c) Manual call  
   Answer: (b)  
3. True/False: Moves deep copy heap data.  
   Answer: False (shallow stack copy)  
4. What is the performance of a drop? (a) O(n) (b) O(1) (c) Variable  
   Answer: (b)  
5. True/False: Shadowing moves ownership.  
   Answer: True (if non-Copy)  
Open Conceptual: Explain how semicolons affect block types.  
Answer: With ; yields (); without yields last expression type.

**Self-Assessment:**  
[ ] Traced moves and drops in examples.  
[ ] Completed labs and micro-challenges.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part III: Tooling and Compiler Interaction

**You Will Be Able To:**  
- Use Cargo for project management and testing.  
- Debug code with `dbg!` and read compiler errors.  
- Fix common errors using diagnostic patterns.

**Time Estimate:** 15 minutes.

### Core Concept: Cargo Workflow

**Problem / Motivation:** C++ Makefiles verbose; Python no compile step. Rust's Cargo unifies build/testing.

**Definition (Formal):** Cargo: Rust's package manager and build tool.

**Mental Model (Simplified):** Commands for create, build, test, run; toml for metadata.

**Example (Compilable):** N/A (tool).

**Code Triple:** N/A.

**Rust Failure Variant:** N/A.

**Compiler Output:** N/A.

**Compiler Reasoning Steps:** N/A (tool).

**Analysis:**  
- Ownership impact: N/A.  
- Performance: Build O(project size).  
- Typical compiler error: N/A.

**ASCII Diagram:** N/A.

**Micro-Challenge Variations:** Predict: Add `rand` dep, generate random i32. Command to install? Use in code.  

**Solution to Micro-Challenge:** `cargo add rand`. Code: `use rand::Rng; dbg!(rand::thread_rng().gen::<i32>());`.  

**Contrast:** C++ manual build; Python pip.  

**Takeaway:** Unified tooling, no ad-hoc scripts.

> **Lab – Try This:** (Predict → Run → Reflect) `cargo build --release`, compare binary size/time.  
> **Solution:** Release smaller/faster due to optimizations. Expected Output: Binaries in target/release. Reflection: Debug for dev, release for perf.

### Core Concept: dbg! Macro

**Problem / Motivation:** C++ printf error-prone; Python print dynamic. Rust's dbg! is typed and expression-yielding.

**Definition (Formal):** dbg!: Macro for debugging prints to stderr, yields value.

**Mental Model (Simplified):** Inserts print in expressions without disrupting flow.

**Example (Compilable):**  
```rust
let y = dbg!(5 * 2);  // Prints to stderr, yields 10
```  

**Code Triple:**  
**Rust:**  
```rust
let y = dbg!(5 * 2);  // Prints to stderr, yields 10
```  

**C++:**  
```cpp
std::cout << 5 * 2 << std::endl;  // No yield
```  

**Python:**  
```python
print(5 * 2)  // No yield
```

**Rust Failure Variant:** Type mismatch with `dbg!` (e.g., expected i32, dbg! yields String).  

**Compiler Output:** E0308 if mismatch.  

**Compiler Reasoning Steps:**  
- Expands macro: Prints and yields.  
- Checks type: Yields original.  
- Rejects if mismatch.

**Analysis:**  
- Ownership impact: Borrows value if needed.  
- Performance: Runtime print O(1).  
- Typical compiler error: E0308 (type mismatch).

**ASCII Diagram:** N/A.

**Micro-Challenge Variations:** Predict output of `dbg!({ 42 })`. In loop?  

**Solution to Micro-Challenge:** `[file:line] { 42 } = 42`. In loop: Multiple prints, overhead.  

**Contrast:** C++ no yield; Python no type check.  

**Takeaway:** Typed, non-intrusive debug.

### Error Reading Lab

**Meta-Pattern Cheat Sheet for Compiler Diagnostics:**  
| Element | Description | Example |
|---------|-------------|---------|
| -->     | Points to error line | --> src/main.rs:5:5 |
| note:   | Additional context | note: move occurs because `s` has type `String` |
| help:   | Suggested fix | help: consider cloning the value |

**Broken 1: Move After Use** (Full code, wrong vs right)  
Wrong:  
```rust
fn main() {
    let s = String::from("hi");
    let t = s;
    println!("{s}");
}
```  
Message: E0382.  
Fix (right): `let t = s.clone();` or borrow `&s`. Before: Unformatted; after rustfmt: Indented.  
Questions: Rule enforced? Fail in C++/Python?  
**Answers:** Ownership move. C++ deep copy or UB; Python shared ref.

**Broken 2: Type Mismatch in If**  
Wrong:  
```rust
fn main() {
    let res = if true { 1 } else { "one" };
}
```  
Message: E0308.  
Fix: Same types, e.g., { 1 } else { 2 }.  
**Answers:** Branches same type. C++ ternary same; Python dynamic runtime error.

**Broken 3: Non-Exhaustive Match**  
Wrong:  
```rust
fn main() {
    match true {
        true => (),
    }
}
```  
Message: E0004.  
Fix: Add false arm.  
**Answers:** Exhaustive cases. C++ switch fall-through; Python if no check.

**Broken 4: Lifetime Error**  
From Case 1. Message: E0106/E0515.  
**Answers:** Borrow lifetime. C++ UB; Python GC.

**Broken 5: String vs &str Mismatch**  
Wrong:  
```rust
fn main() {
    let s: String = "hello".to_string();
    let r: &str = s;  // Mismatch
}
```  
Message: E0308.  
Fix: `&s` (Deref coercion).  
**Answers:** Ownership vs borrow. C++ implicit cast; Python no types.

**Takeaway:** Errors teach rules; read spans/notes. Complete lab with correct answers.

**Clippy Example:** Run `cargo clippy` on redundant clone:  
```rust
let s2 = s.clone(); // If unnecessary
```  
Output: warning: redundant clone; help: remove this.

**Part III Checkpoint:** You should explain Cargo commands, `dbg!` usage, error patterns.  
**You Can Now:**  
- Add dependencies and run tests.  
- Use `dbg!` for probing.

**Part III Quiz:** (5 MCQs + 1 open conceptual question)  
1. What does `cargo check` do? (a) Run code (b) Type check only (c) Optimize  
   Answer: (b)  
2. Where does `dbg!` print? (a) Stdout (b) Stderr (c) File  
   Answer: (b)  
3. True/False: Cargo.toml defines dependencies.  
   Answer: True  
4. What is clippy for? (a) Build (b) Lints (c) Test  
   Answer: (b)  
5. True/False: dbg! has runtime overhead.  
   Answer: True  
Open Conceptual: Explain how to read a compiler note.  
Answer: Provides context like move reason.

**Self-Assessment:**  
[ ] Ran a test with `cargo test`.  
[ ] Fixed an error using compiler help notes.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part IV: Applied Safety Thinking – Guided Build of Safe Arithmetic CLI v0

**You Will Be Able To:**  
- Build a CLI using ownership rules and Option.  
- Handle optional values with match/if let.  
- Test functions modularly with cargo test.

**Time Estimate:** 15 minutes.

**Prerequisites Explicit:** i32 signed (-2^31 to 2^31-1); Option enums Some/None for absence. Recap if from prior: None.

**Checkpoint 1: Plain Functions** (Full v0)  
```rust
fn add(a: i32, b: i32) -> i32 { a + b }
fn sub(a: i32, b: i32) -> i32 { a - b }
fn mul(a: i32, b: i32) -> i32 { a * b }

fn main() {
    let op = "add";
    let x = 10;
    let y = 5;
    let result = match op {
        "add" => add(x, y),
        "sub" => sub(x, y),
        "mul" => mul(x, y),
        _ => {
            eprintln!("Unknown op: {op}");
            return;
        }
    };
    println!("{op}({x}, {y}) = {result}");
}
```  
Expected Output: "add(10, 5) = 15". Reflect: Types static.

**Checkpoint 2: Add safe_div**  
Broken:  
```rust
fn safe_div(a: i32, b: i32) -> Option<i32> {
    if b == 0 { None } else { Some(a / b) }
}
// In match: "div" => safe_div(x, y),  // Option vs i32
```  
Output: E0308 mismatch. Explanation: Arms uniform type.

**Checkpoint 3: Fix with Option** (Full final)  
```rust
fn add(a: i32, b: i32) -> i32 { a + b }
fn sub(a: i32, b: i32) -> i32 { a - b }
fn mul(a: i32, b: i32) -> i32 { a * b }
fn safe_div(a: i32, b: i32) -> Option<i32> {
    if b == 0 { None } else { Some(a / b) }
}

fn main() {
    let op = "div";
    let x = 10;
    let y = 0;

    let result_opt: Option<i32> = match op {
        "add" => Some(add(x, y)),
        "sub" => Some(sub(x, y)),
        "mul" => Some(mul(x, y)),
        "div" => safe_div(x, y),
        _ => {
            eprintln!("Unknown op: {op}");
            return;
        }
    };

    if let Some(result) = result_opt {
        println!("{op}({x}, {y}) = {result}");
    } else {
        println!("Error: Div by zero");
    };
}
```  
Expected Output: "Error: Div by zero". Note: Option<T> for absence. Expand: unwrap (panic if None), unwrap_or(default), map(transform). Teaser: Result for errors. if let destructures.

**Checkpoint 4: Add dbg!**  
```rust
let debugged = dbg!(add(x, y));
```  
Reflect: Yields i32, prints debug.

> **Suggestion:** After snippet, run `cargo fmt` (format), `cargo clippy` (lints). Habit saves mistakes.

[Design] **Reflection – Think:** Consider Option vs panic (hint: explicit handling, no unwind).  
[Answer] **Model Answer:** Option for explicit; no exceptions like panic unwind. Reflection link: Enum variant design like success/failure.

> **Lab – Try This:** (Predict → Run → Reflect) Add unit test with derived PartialEq, edge-cases (div_0).  
> **Solution:**  
> ```rust
> #[derive(PartialEq)]
> enum OpResult { Sum(i32), Error }
> #[test]
> fn test_safe_div() {
>     assert_eq!(safe_div(10, 0), None);
>     assert_eq!(safe_div(10, 2), Some(5));
> }
> ```  
> `cargo test`: "ok". Edge: div_0 None. Reflection: Testing first-class.

**Part IV Checkpoint:** You should build safe CLI with Option.  
**You Can Now:**  
- Handle optional with match/if let.  
- Test modularly.

**Cumulative Project Extension (Optional Depth, Scales to ~2000 Lines Total):** Extend CLI v3 with borrowing/lifetimes preview: fn process(&str) -> String; integrate.

**Part IV Quiz:** (5 MCQs + 1 open conceptual question)  
1. What does Some represent in Option? (a) Error (b) Value (c) None  
   Answer: (b)  
2. True/False: if let moves ownership.  
   Answer: True (unless ref)  
3. What is unwrap? (a) Safe get (b) Panic on None (c) Default  
   Answer: (b)  
4. Performance of match on Option? (a) O(n) (b) O(1) (c) Variable  
   Answer: (b)  
5. True/False: Result is like Option for errors.  
   Answer: True  
Open Conceptual: Explain why Option encourages explicit handling.  
Answer: Forces check for None, no silent failures.

**Self-Assessment:**  
[ ] Built and tested the CLI.  
[ ] Handled div by zero case.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Exercises: Tiered Reasoning

Annotate tier difficulty/time: Tier 1 straightforward (5min), Tier 3 stretch (15min, design). Tie to ownership. Balance: Harder Tier 1, deeper Tier 3.

### Tier 1: Concept Rebuilds

1. Ownership Tracing (With commentary)  
   Annotate moves/drops:  
   ```rust
   fn main() {
       let s = String::from("hi");  // owns
       let t = s;  // move to t
       println!("{t}");  // borrow t
   }  // drop t
   ```  
   **Solution:** s owns → move to t (s invalid) → print ok → drop t.

2. Expression Block  
   Rewrite C++ to Rust if expression.  
   **Solution:** `let val = if true { 42 } else { 0 };`.

### Tier 2: Comparative Rewrites

1. Dangling Fix  
   Rewrite C++ dangling to Rust owned return.  
   **Solution:**  
   ```rust
   fn not_dangling() -> i32 { 42 }
   ```  
   Diff: Owned, no ref.

2. Python Add to Rust  
   Add types, pass by value (move).  
   **Solution:**  
   ```rust
   fn add(a: i32, b: i32) -> i32 { a + b }  // Primitives copy
   ```  
   Diff: Static types, ownership in args.

### Tier 3: Challenge Extensions

1. Mut vs Shadow  
   Compare variants.  
   **Solution:**  
   ```rust
   let count = 0;
   let count = count + 1;  // Shadow new

   let mut mut_count = 0;
   mut_count += 1;  // Mut existing
   ```  
   Shadow for transform; mut for state. Ownership: Shadow moves if non-Copy.

2. Non-Exhaustive Fix  
   Add arm.  
   **Solution:**  
   ```rust
   match true {
       true => (),
       false => (),
   }
   ```

3. Destructuring Preview  
   `let (x, y) = (1, 2);`  
   **Solution:** x=1, y=2; ties to match.

**Self-Assessment:**  
[ ] Completed at least one exercise per tier.  
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
1. Can't return &i32 to local? Borrow outlives.  
2. dbg! cost? Runtime stderr.  
3. Ownership in functions? Move unless Copy or &.  
4. API trade-offs? Own vs borrow: Safety vs perf.  
5. Slice structure? Ptr + len.

**Final Takeaway:** Rust’s compiler enforces correctness ahead of time; this mindset contrasts with languages relying on runtime tolerance. Strengthen: Types + pattern matching = compile-time safety.

**By Session End:**  
- Explain why Rust rejects a function that returns `&i32` to a local.  
- Predict when a binding moves and when it’s copied.  
- Explain why two `&mut` borrows to the same value are illegal.  
- Use `Option` to represent a possibly-missing value.  
- Read and fix common compiler errors about moves, types, and lifetimes.  
- Build and run a small CLI with `cargo run`, and test it with `cargo test`.

**Glossary Appendix:**  
- Ownership: Single binding controls resource lifetime.  
- Borrow: Temporary reference (`&T` immutable, `&mut T` mutable).  
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
| E0004  | Non-exhaustive match            | Non-exhaustive |
| E0597  | Borrow outlives owner           | Scope borrow |
| E0433  | Unresolved macro                | Macro typo  |

**Primary References:** Rust Book Ch. 4 (Ownership), Ch. 10 (Lifetimes), Ch. 11 (Testing).  
**Suggested Deep Dives:** Rustonomicon (ownership semantics); RFCs for NLL.

**Concept Map:** (Text-based ASCII)  
Ownership  
  ├── Moves (O(1) transfer)  
  │   └── Invalidate old  
  ├── Borrows (&/&mut)  
  │   └── Lifetimes (outlive check)  
  ├── Drop (scope end)  
  └── Safety (no dangling/double free/races)  
      └── Tooling (Cargo/dbg!)  
          └── Applied (CLI + Option)

**Bridge to Session 2:** Rules like moves (O(1)) and drops carry over, now applied to compound types and patterns. Expressions unify flow; ownership in destructuring adds precision. Extend the CLI into a type-safe expression engine.

**Self-Assessment:**  
[ ] Reviewed concept map and quiz answers.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

**Deep Dive Appendix:**  
- Lifetime parameters: `fn dangling<'a>() -> &'a i32 { let x = 42; &x }` fails as `'a` outlives `x`. In async, Drop tied to future.  
- Drop + Copy: Illegal if Drop impl. Compare C++ std::move.  
- Exceptions like Cell/RefCell for interior mutability. Arc for concurrent sharing.
