# Session 2: Rust’s Building Blocks – Types, Control Flow, and Pattern Matching

**Target Audience & Scope:** This series assumes familiarity with C/Python, basic memory models (e.g., stack/heap, pointers/references, GC internals), and command-line tools. It targets programmers with systems or dynamic language experience new to Rust. Tone balances explanation for beginners in Rust but avoids over-simplifying semantics for intermediates.

**Prerequisites:** Session 1 concepts (ownership, moves, borrows); basic CLI building.

**Conceptual Learning Goals:**  
- Grasp memory-safe arithmetic with checked ops; trade-offs vs Python's dynamic ints.  
- Use compounds like tuples/arrays with ownership; evolve from Session 1's basics to cost models.  
- Unify flow with expressions; type safety.  
- Integrate ownership: Destructuring moves if not ref.

**By the End of This Session, You Can:**  
- Use types with safety awareness.  
- Expression flow with if/loop/for.  
- Exhaustive match with guards/or.  
- Extend CLI with structs.  
- Fix type/non-exhaustive errors.  
- Apply dbg!/fmt.

**Project Narrative:** You are extending the Session 1 calculator CLI into a type-safe expression engine, integrating new types, flow, and matching for robust handling.

**Time Estimate:** 60 minutes.

---

## Setup Checklist

Skip if verified from Session 1. Otherwise, quickly check:

1. **Verify Existing Setup** (Refer to Session 1 for details)
   ```bash
   cargo --version
   rustc --version
   ```
   Expect cargo 1.91.0 or newer and rustc 1.91.0 or newer (run `rustup update` if older). Confirm rust-analyzer in your editor (e.g., hover for types).

2. **Install and Use rustfmt**
   ```bash
   rustup component add rustfmt
   cargo fmt
   ```
   Formats code per Rust style guide, focusing you on logic. Unlike gofmt, rustfmt preserves semantics while standardizing.

3. **Optional: Practice Adding a Dependency**
   ```bash
   cargo add rand
   ```
   Example usage (add to main.rs and run `cargo run`):
   ```rust
   use rand::Rng;
   fn main() {
       let num = rand::thread_rng().gen::<i32>();
       dbg!(num);
   }
   ```
   Prints a random i32 to stderr.

4. **Run Your Session 1 CLI**
   Ensure your Safe Arithmetic CLI compiles: `cargo run`.

> **Lab – Try This:** Mess up indentation in main.rs. Run `cargo fmt` and note changes. Customize via .rustfmt.toml (create in project root): `max_width = 80`. Rerun `cargo fmt`.
> **Solution:** Reformats to 4-space indents, consistent breaks. With .rustfmt.toml, lines wrap at 80 chars. Takeaway: Tools enforce style; customize for team prefs.
> Expected output: Reformatted code; no errors.  
> Example output: Before: unformatted; after: indented, wrapped.

**Debug the Error Mini-Lab (Retention Test from Session 1):** Take the dangling reference code from Session 1 Case 1. Modify to use Box<i32> and predict error. Fix by returning owned Box.  
**Solution:** Still rejects borrow outliving owner; fix returns Box<i32> (moves ownership).

**Self-Assessment:**  
[ ] Verified setup and completed mini-lab.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

**Time Estimate:** 15 minutes.

---

## Part I: Data Types – Precise, Safe Modeling from Scalars to Compounds

**You Will Be Able To:**  
- Handle arithmetic with overflow safety using checked methods.  
- Use tuples, arrays, and slices with ownership awareness.  
- Contrast Rust's compounds to C/C++ and Python, including memory layouts.

**Time Estimate:** 15 minutes.

### Core Concept: Case 1 – Scalar Types and Overflow Safety

**Problem / Motivation:** C/C++ signed overflow is UB, risking crashes or exploits. Python uses big ints for safety but with perf/memory costs (e.g., 2**1000000 ≈125KB). Rust provides debug panics and controlled methods.

**Definition (Formal):** Scalars include i8-i128, u8-u128, f32/f64, bool, char (Unicode scalar value). Overflow: Exceeding representable range.

**Mental Model (Simplified):** Debug mode panics on overflow; release wraps. Use methods for explicit handling.

**Example (Compilable):** Checked add.  
```rust
let a: i32 = i32::MAX;
let checked = a.checked_add(1);  // None
```

**Code Triple:**  
**Rust (Checked in debug, wrapping in release):**  
```rust
let a: i32 = i32::MAX;
let overflow = a + 1;  // Debug: panic; Release: wrap to i32::MIN (no UB)
```  

**C/C++ (UB):**  
```cpp
int a = INT_MAX;
int overflow = a + 1;  // UB: Arbitrary behavior
```  

**Python (Big int):**  
```python
a = 2**31 - 1
overflow = a + 1  # Big int; O(n) memory/time for large
```

**Rust Failure Variant:** Wrapping in release (logical risk).  
```rust
fn main() {
    let a: i32 = i32::MAX;
    let overflow = a + 1;  // Wraps to i32::MIN; can lead to logic bugs
    println!("{}", overflow);  // -2147483648
}
```

**Compiler Output:** No error (runtime behavior differs by mode).

**Compiler Reasoning Steps:**  
- Infers types: i32 operations.  
- In debug: Inserts overflow checks (panic on overflow).  
- In release: Removes checks for perf, allows wrapping.

**Analysis:**  
- Ownership impact: Primitives like i32 are Copy, no move.  
- Performance: Wrapping O(1); checked adds branch.  
- Typical compiler error: No compile error; runtime panic in debug.

**ASCII Diagram: Scalar Overflow (Mental Model)**  
```
i32: -2^31 ... 2^31-1
MAX + 1 --> Debug: Panic
        --> Release: Wrap to MIN
Checked: None
```

**Micro-Challenge Variations:** Predict: `i32::MAX.checked_add(1)`? Use saturating_add.  

**Solution to Micro-Challenge:** `None` (Option<i32>). Saturating: i32::MAX.

> **Lab – Try This:** Observe overflow behavior: `i32::MAX + 1`. Run debug/release.
> **Solution:** Debug panic; release -2147483648. Expected: Panic msg or wrapped value.

[Performance] **Reflection – Think:** When use checked_add vs debug panic?  
[Answer] **Model Answer:** For graceful handling (e.g., error return) in prod.

[Semantics] **Think like the Compiler:** What constraints does the compiler infer for overflow in release mode? (Answer: No checks; assumes wrapping semantics, no UB.)

### Core Concept: Case 2 – Compound Types: Tuples and Arrays

**Problem / Motivation:** C/C++ array decay loses size; risks overruns. Python lists dynamic, with runtime checks. Rust fixes size/safety at compile time.

**Definition (Formal):** Tuples: Heterogeneous fixed-size groups. Arrays: Homogeneous fixed-size [T; N].

**Mental Model (Simplified):** Tuples for quick grouping; arrays for known-size collections. Ownership applies recursively.

**Example (Compilable):**  
```rust
let arr: [i32; 3] = [1, 2, 3];
let tup: (i32, f64, char) = (42, 3.14, 'π');
```

**Code Triple:**  
**Rust:**  
```rust
let arr: [i32; 3] = [1, 2, 3];
let tup: (i32, f64, char) = (42, 3.14, 'π');
```  

**C/C++:**  
```cpp
int arr[3] = {1, 2, 3};  // Decays to int*
auto tup = std::make_tuple(42, 3.14, 'π');
```  

**Python:**  
```python
arr = [1, 2, 3]  # List (dynamic)
tup = (42, 3.14, 'π')  # Immutable
```

**Rust Failure Variant:** Invalid access.  
```rust
fn main() {
    let tup = (42, 3.14, 'π');
    let _ = tup.3;
}
```

**Compiler Output:** error[E0609]: no field `3` on type `(i32, f64, char)` (msgs may vary; key E0609).

**Compiler Reasoning Steps:**  
- Infers tuple type from elements.  
- At access tup.3: Checks field count (0-2).  
- Rejects: Static index out of bounds.

**Analysis:**  
- Ownership impact: Destructuring moves unless ref.  
- Performance: Copy for small compounds if all fields Copy.  
- Typical compiler error: E0609 (invalid field).

**ASCII Diagram: Tuple Destructuring (Mental Model)**  
```
+----------+----------+----------+
| i32: 42  | f64: 3.14| char: 'π'|
+----------+----------+----------+
          ↓          ↓
        let (x, y, z) = tup;  // Moves ownership
```

**Micro-Challenge Variations:** Predict: Destructure [i32; 3]. Use ref for borrow.  

**Solution to Micro-Challenge:** `let [a, b, c] = arr;` (moves). Ref: `let [ref a, ..] = arr;`.

> **Lab – Try This:** `fn pair(a: i32, b: f64) -> (i32, f64) { (a, b) }`; destructure return.
> **Solution:** Types i32, f64. Output: "42 3.14" (if printed).

[Design] **Reflection – Think:** Tuple vs struct?  
[Answer] **Model Answer:** Tuple for anonymous/quick; struct for named/extensible (>3 fields).

[Semantics] **Think like the Compiler:** What constraints does the compiler infer for array bounds? (Answer: Compile-time rejection if constant index out of range.)

### Core Concept: Case 3 – Slices and &str

**Problem / Motivation:** C/C++ pointers error-prone. Python slices copy, O(n) perf. Rust borrows views safely.

**Definition (Formal):** Slices: Borrowed views &[T] (ptr + len). &str: UTF-8 string slice.

**Mental Model (Simplified):** Fat pointers for bounds-safe borrows without ownership transfer.

**Example (Compilable):**  
```rust
let arr = [1, 2, 3, 4];
let slice: &[i32] = &arr[1..3];  // [2, 3] borrow
```

**Code Triple:**  
**Rust:**  
```rust
let arr = [1, 2, 3, 4];
let slice: &[i32] = &arr[1..3];  // [2, 3] borrow
```  

**C/C++:**  
```cpp
int arr[4] = {1,2,3,4};
int* slice = arr + 1;  // No len
```  

**Python:**  
```python
arr = [1,2,3,4]
slice = arr[1:3]  # Copy [2,3]
```

**Rust Failure Variant:** Bounds.  
```rust
fn main() {
    let arr = [1, 2, 3, 4];
    let _ = &arr[1..5];
}
```

**Compiler Output:** No compile error; runtime panic.

**Compiler Reasoning Steps:**  
- For constant ranges: Const-eval bounds check.  
- Dynamic: Runtime panic if out of bounds.  
- Borrow: Ties lifetime to owner.

**Analysis:**  
- Ownership impact: Borrows, no move.  
- Performance: Slice creation O(1).  
- Typical compiler error: None; runtime index panic.

**ASCII Diagram: Fat Pointer (Mental Model)**  
```
&[T]:
  +-------+
  | ptr   | --> [T, T, T]
  +-------+
  | len   |
  +-------+
```

**Micro-Challenge Variations:** Predict: &str from String. Access slice[4].  

**Solution to Micro-Challenge:** `let str_slice: &str = &s;` (coerces). Access: Runtime panic.

> **Lab – Try This:** `fn first(nums: &[i32]) -> Option<i32> { nums.get(0).copied() }` Test empty/non-empty.
> **Solution:** None/Some. Output: As printed.

[Performance] **Reflection – Think:** &[T] vs Vec<T> in fn?  
[Answer] **Model Answer:** &[T] flexible, no own/clone.

[Semantics] **Think like the Compiler:** What constraints does the borrow checker infer for a slice borrow? (Answer: Lifetime tied to owner; no mutation if immutable borrow.)

**Part I Checkpoint:** Explain overflow, tuple access, slice safety.  
**You Can Now:**  
- Handle optional with match/if let.  
- Test modularly.

**Part I Quiz:** (5 MCQs + 1 open conceptual question)  
1. What happens on debug overflow? (a) Wrap (b) Panic (c) UB  
   Answer: (b)  
2. True/False: Tuples are homogeneous.  
   Answer: False  
3. Slice structure? (a) Ptr only (b) Ptr + len (c) Heap copy  
   Answer: (b)  
4. Performance of slice borrow? (a) O(n) (b) O(1) (c) O(log n)  
   Answer: (b)  
5. True/False: Arrays are always Copy.  
   Answer: False (if T not Copy)  
Open Conceptual: Explain fat pointer.  
Answer: Ptr + len for bounds safety.

**Self-Assessment:**  
[ ] Handled overflow and destructured a tuple.  
[ ] Drew a diagram for slices.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part II: Control Flow – Expression-Oriented for Concise Logic

**You Will Be Able To:**  
- Use if/loop/for as expressions with type safety.  
- Integrate ownership in loop borrows and destructuring.  
- Predict type mismatches in control flow arms.

**Time Estimate:** 15 minutes.

### Core Concept: Case 1: If as Expression

**Problem / Motivation:** C/C++ ternaries limited; Python dynamic. Rust unifies for type-safe value flow.

**Definition (Formal):** If: Conditional expression yielding values from branches.

**Mental Model (Simplified):** Branches must yield same type; optional else yields ().

**Example (Compilable):**  
```rust
let max = if a > b { a } else { b };
```

**Code Triple:**  
**Rust:**  
```rust
let max = if a > b { a } else { b };
```  

**C/C++:**  
```cpp
int max = a > b ? a : b;
```  

**Python:**  
```python
max = a if a > b else b
```

**Rust Failure Variant:** Type mismatch.  
```rust
let res = if true { 42 } else { "forty-two" };
```

**Compiler Output:** error[E0308]: incompatible types (msgs vary; key E0308).

**Compiler Reasoning Steps:**  
- Analyzes branches: Types i32 vs &str.  
- Checks unification: Must match for expression type.  
- Rejects: Type safety.

**Analysis:**  
- Ownership impact: Branches can move values.  
- Performance: Branch O(1).  
- Typical compiler error: E0308 (incompatible types).

**ASCII Diagram: If Expression Flow**  
```
if cond {  
  expr1 --> T  
} else {  
  expr2 --> T  
} --> T
```

**Micro-Challenge Variations:** Predict: If for Option. No else.  

**Solution to Micro-Challenge:** `if cond { Some(42) } else { None };` (Option<i32>). No else: Yields ().

[Semantics] **Reflection – Think:** Ties to Session 1 blocks?  
[Answer] **Model Answer:** Unifies statements/expressions for concise code.

[Semantics] **Think like the Compiler:** What constraints does the compiler infer for if branch types? (Answer: Must unify to a single type.)

### Core Concept: Case 2: Loops with Values

**Problem / Motivation:** C/C++/Python loops statements, need vars. Rust yields values from breaks.

**Definition (Formal):** Loop: Infinite with break yield. While/for: Conditional/iterator-based.

**Mental Model (Simplified):** Break carries value; for borrows or moves over iterators.

**Example (Compilable):**  
```rust
let result = loop {
    count += 1;
    if count == 5 { break count * 2; }
};
```

**Code Triple:**  
**Rust:**  
```rust
let result = loop {
    count += 1;
    if count == 5 { break count * 2; }
};
```  

**C/C++:**  
```cpp
int result; while(true) { ... result = ...; break; }
```  

**Python:**  
```python
while True: ... result = ...; break
```

**Rust Failure Variant:** Type mismatch.  
```rust
let result: i32 = loop { break; };
```

**Compiler Output:** error[E0308]: expected i32, found ().

**Compiler Reasoning Steps:**  
- Loop: Infers type from break expressions.  
- No value break: Yields ().  
- Rejects: Mismatch with expected.

**Analysis:**  
- Ownership impact: For moves if into_iter.  
- Performance: Iteration O(n) for ranges.  
- Typical compiler error: E0308 (mismatched types).

**ASCII Diagram: For Borrow**  
```
nums: Vec<i32>
&nums --> for n in &nums { dbg!(n); }  // Immutable borrow
```

**Micro-Challenge Variations:** Predict: Sum 1..=5. For move vs borrow.  

**Solution to Micro-Challenge:** for i in 1..=5 { sum += i; } (15). Move consumes nums.

> **Lab – Try This:** dbg! in loop.
> **Solution:** Prints iterations to stderr.

[Semantics] **Reflection – Think:** for vs while?  
[Answer] **Model Answer:** for collections/ranges; while arbitrary conds. Note: while let for pattern loops.

[Semantics] **Think like the Compiler:** What constraints does the borrow checker infer in `for n in &nums`? (Answer: Immutable borrow for loop duration.)

**Part II Checkpoint:** Why if expression? Loop yield?  
**You Can Now:**  
- Use expression flow.  
- Borrow in loops.

**Part II Quiz:** (5 MCQs + 1 open conceptual question)  
1. If branches yield? (a) Different types (b) Same type (c) Unit  
   Answer: (b)  
2. Loop break yields? (a) () (b) Value (c) Panic  
   Answer: (b)  
3. True/False: for moves ownership.  
   Answer: True (without &)  
4. Performance of range loop? (a) O(1) (b) O(n) (c) O(log n)  
   Answer: (b)  
5. True/False: while let destructures.  
   Answer: True  
Open Conceptual: Explain for borrow vs move.  
Answer: & borrows; no & moves/consumes.

**Self-Assessment:**  
[ ] Used a loop to yield a value.  
[ ] Borrowed in a for loop.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part III: Pattern Matching – Exhaustive, Powerful Decomposition

**You Will Be Able To:**  
- Write exhaustive matches with guards and or patterns.  
- Destructure with ref/mut for ownership control.  
- Fix non-exhaustive and type mismatch errors in matches.

**Time Estimate:** 15 minutes.

### Core Concept: Match Exhaustiveness

**Problem / Motivation:** C switch fall-through bugs; Python no exhaustiveness. Rust enforces coverage.

**Definition (Formal):** Match: Deconstruct values via patterns, exhaustive by default.

**Mental Model (Simplified):** Patterns cover all cases; _ wildcard last.

**Example (Compilable):**  
```rust
let desc = match num {
    1 | 2 => "small odd",
    3..=10 if num > 0 => "small positive",
    _ => "other",
};
```

**Code Triple:**  
**Rust:**  
```rust
let desc = match num {
    1 | 2 => "small odd",
    3..=10 if num > 0 => "small positive",
    _ => "other",
};
```  

**C:**  
```c
switch(num) { case 1: ... break; }  // Fall-through risk
```  

**Python:**  
```python
match num:
    case 1:
        ...
    case _:
        ...
```

**Rust Failure Variant:** Non-exhaustive.  
```rust
match true { true => (), }
```

**Compiler Output:** error[E0004]: `false` not covered (key E0004).

**Rust Failure Variant:** Type mismatch.  
```rust
match n { 0 => 0, _ => "non-zero", }
```

**Compiler Output:** error[E0308]: incompatible types.

**Compiler Reasoning Steps:**  
- Analyzes patterns: Checks coverage (exhaustive).  
- Arms: Unifies types.  
- Rejects: Missing cases or mismatch.

**Analysis:**  
- Ownership impact: Destructuring moves unless ref.  
- Performance: Match O(1) for small enums.  
- Typical compiler error: E0004 (non-exhaustive), E0308 (types).

**ASCII Diagram: Match Flow**  
```
match value {  
  pat1 => expr1 --> T  
  pat2 if guard => expr2 --> T  
  _ => exprN --> T  
} --> T (exhaustive)
```

**Micro-Challenge Variations:** Predict: Tuple match. With guard.  

**Solution to Micro-Challenge:** `(0, _) =>`, `(_, 0) =>`, `_ =>`. Guard: `n if n > 0 =>`.

[Design] **Reflection – Think:** Match vs if-elif?  
[Answer] **Model Answer:** Prefer match when pattern coverage conveys program invariants; exhaustive, decomposes; compiler omissions.

[Semantics] **Think like the Compiler:** What constraints does the compiler infer for match exhaustiveness? (Answer: All variants covered; suggests missing patterns.)

**Part III Checkpoint:** Why exhaustive? Same type? Guards?  
**You Can Now:**  
- Use patterns for decomposition.  
- Ensure exhaustiveness.

**Part III Quiz:** (5 MCQs + 1 open conceptual question)  
1. Match requires? (a) Partial (b) Exhaustive (c) Optional  
   Answer: (b)  
2. Guards are? (a) Patterns (b) Conditionals (c) Types  
   Answer: (b)  
3. True/False: Destructuring borrows with ref.  
   Answer: True  
4. Performance of literal match? (a) O(n) (b) O(1) (c) O(log n)  
   Answer: (b)  
5. True/False: _ is required for exhaustive.  
   Answer: True (if not all covered)  
Open Conceptual: Explain or in patterns.  
Answer: Alternatives like 1 | 2.

**Self-Assessment:**  
[ ] Wrote an exhaustive match with guard.  
[ ] Fixed a non-exhaustive error.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Part IV: Applied Expressiveness – Multi-Op Calculator v1

**You Will Be Able To:**  
- Integrate types, flow, and matching in an extended CLI.  
- Use structs to unify match arms.  
- Profile and test the CLI for perf and correctness.

**Time Estimate:** 15 minutes.

Recap Session 1 CLI: If missing, `fn safe_div(a: i32, b: i32) -> Option<i32> { if b == 0 { None } else { Some(a / b) } }`. Use consistent op, x, y.

### Checkpoint 1: Add `fizzbuzz` with `match`

```rust
fn fizzbuzz(n: i32) -> String {
    match (n % 3, n % 5) {
        (0, 0) => "FizzBuzz".to_string(),
        (0, _) => "Fizz".to_string(),
        (_, 0) => "Buzz".to_string(),
        _ => n.to_string(),
    }
}
```
to_string() owned String; format! for complex.

> **Lab – Try This:** Print fizzbuzz(15,3,5,7). Expected: FizzBuzz, Fizz, Buzz, 7.

### Checkpoint 2: Broken Attempt – Type Mix

Intentional break:
```rust
let result = match op {
    "add" => add(x, y),  // i32
    "div" => safe_div(x, y),  // Option<i32>
    "fizzbuzz" => fizzbuzz(x),  // String
    _ => 0,
};
```
**Compiler Output:** error[E0308]: incompatible types.

**Explanation:** Arms must unify type.

### Checkpoint 3: Fix – `OpResult` Type

```rust
#[derive(Debug, Clone, PartialEq, Eq)]
struct OpResult {
    description: String,
    output: String,
}

impl OpResult {
    fn new(desc: &str, output: impl ToString) -> Self {
        Self { description: desc.to_string(), output: output.to_string() }
    }
}

fn add_result(a: i32, b: i32) -> OpResult { OpResult::new("sum", a + b) }
// Similar for sub, mul

fn div_result(a: i32, b: i32) -> Option<OpResult> {
    safe_div(a, b).map(|q| OpResult::new("quotient", q))
}

fn fizzbuzz_result(n: i32) -> OpResult { OpResult::new("fizzbuzz", fizzbuzz(n)) }
```

Main:
```rust
let result_opt: Option<OpResult> = match op {
    "add" => Some(add_result(x, y)),
    "div" => div_result(x, y),
    "fizzbuzz" => Some(fizzbuzz_result(x)),
    _ => None,
};

if let Some(result) = result_opt {
    println!("operation: {}, output: {}", result.description, result.output);
} else {
    eprintln!("Unknown op: {op}");
}
```

> **Lab – Try This:** Test ops; div by 0. Add tests:
> ```rust
> #[cfg(test)]
> mod tests {
>     use super::*;
>     #[test]
>     fn test_fizzbuzz() {
>         assert_eq!(fizzbuzz_result(15).output, "FizzBuzz");
>         assert_eq!(fizzbuzz_result(0).output, "0");  // Edge
>     }
>     #[test]
>     fn test_add() {
>         assert_eq!(add_result(1, 2), OpResult::new("sum", 3));
>     }
> }
> ```
> Run `cargo test`. Expected: Pass.

[Design] **Reflection – Think:** Similar to Session 1 Option?  
[Answer] **Model Answer:** Option for absence; richer payload like enum variants (success/failure).

**Part IV Checkpoint:** You should build extended CLI with structs.  
**You Can Now:**  
- Unify types in match.  
- Test with derives.

**Part IV Quiz:** (5 MCQs + 1 open conceptual question)  
1. Struct unifies match by? (a) Types (b) Ownership (c) Performance  
   Answer: (a)  
2. True/False: Derive PartialEq for tests.  
   Answer: True  
3. fizzbuzz match is? (a) Partial (b) Exhaustive (c) Optional  
   Answer: (b)  
4. Performance of struct new? (a) O(n) (b) O(1) (c) Variable  
   Answer: (b)  
5. True/False: Result better for errors.  
   Answer: True  
Open Conceptual: Explain struct vs tuple in CLI.  
Answer: Named fields for clarity.

**Self-Assessment:**  
[ ] Extended CLI and ran tests.  
[ ] Profiled with Instant.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Exercises: Tiered Reasoning
### Tier 1: Concept Rebuilds
1. Annotate: `let pi = 3.14;` **Solution:** f64.

2. Slice: From array. **Solution:** `let mid = &arr[1..4];`.

### Tier 2: Comparative Rewrites
1. C array to slice. **Solution:** &arr[start..end]; bounds safe.

2. Python loop to for. **Solution:** `for &n in &nums { sum += n; }` Borrow, no index.

### Tier 3: Challenge Extensions
1. Guarded match. **Solution:**
```rust
let desc = match n {
    n if n % 2 == 0 => "even",
    _ => "odd",
};
```

2. Nested. **Solution:**
```rust
let sum = match (opt1, opt2) {
    (Some(a), Some(b)) => a + b,
    _ => 0,
};
```

3. Result Extension: Rewrite safe_div with Result<i32, String>.  
**Solution:** `if b == 0 { Err("div zero".to_string()) } else { Ok(a / b) }`.

> **Intermediate Lab – Try This:** Borrow vec in loop, then mutate—error. Fix: Scope `{ let slice = &vec; ... }`.
> **Solution:** Compiles post-scope.

**Self-Assessment:**  
[ ] Completed exercises and labs.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

---

## Recap and Synthesis Reflection

**Table Completion Exercise:**
| Rust Feature | C/C++ Issue | Python Trade-off |
|--------------|-------------|------------------|
| Scalar Overflow | UB | Big int perf hit (e.g., ≈125KB for 2**1000000) |
| Slices | Pointer overrun | Copy O(n) |
| Match Exhaustive | Fall-through | No compile check |
| Ownership Enforcement | Raw pointer freedom | GC pauses |
| Pattern Matching | N/A | Dynamic overhead |
| Expression Semantics | Statement-oriented | Dynamic types |

**Self-Quiz:** (Design-level)  
1. Panic on debug overflow?  
2. Slice internal?  
3. Pattern guards?  
Answers:  
1. Early bug detect.  
2. Ptr + len.  
3. Conditional match.

**Final Takeaway:** Types + pattern matching = compile-time safety; prevents UB, enforces handling.

**By Session End:**  
- Use types with safety awareness.  
- Expression flow with if/loop/for.  
- Exhaustive match with guards/or.  
- Extend CLI with structs.  
- Fix type/non-exhaustive errors.  
- Apply dbg!/fmt.

**Glossary Appendix Update:** Add Slice: Borrowed view &[T]; &str: String slice.  

**Error Code Index:**  
| Code   | Description                     | Example Case |
|--------|---------------------------------|--------------|
| E0308  | Incompatible types              | If/match mismatch |
| E0609  | Invalid field                   | Tuple access |
| E0004  | Non-exhaustive match            | Missing arm |

**Primary References:** Rust Book Ch. 3 (Data Types), Ch. 6 (Enums/Match), Ch. 8 (Collections).  
**Suggested Deep Dives:** Rustonomicon (types); RFCs for pattern syntax.

**Concept Map:** (Text-based ASCII)  
Types  
  ├── Scalars (overflow safety)  
  ├── Compounds (tuples/arrays)  
  └── Slices (&[T], lifetimes)  
Control Flow (expressions)  
  └── If/loop/for (yield values)  
Pattern Matching (exhaustive)  
  └── Destructuring (ownership)  
Applied (CLI + structs/Option)

**Bridge to Session 3:** Types and patterns integrate with lifetimes; slices borrow with 'a inference. Extend CLI with lifetime-safe functions.

**Self-Assessment:**  
[ ] Reviewed concept map and quiz.  
Rate 1–3: How confident are you? (1: Need review; 3: Fully grasp.)

**Deep Dive Appendix:**  
- Checked ops with Result for propagation.  
- Slices IntoIterator; &str UTF-8 methods.  
- For consumes if into_iter().  
