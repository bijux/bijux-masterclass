# M05C01 · Loop Invariants and Variants – Constructing Correctness from First Principles

**Goal.** This core furnishes a mechanical procedure for deriving loop invariants and variants, thereby establishing partial and total correctness for iterative algorithms. Upon completion, practitioners will systematically construct invariants and variants for scans, searches, and updates, guaranteeing that implementations maintain designated properties while ensuring finite termination.

**Scope** (explicit delimiters):
- Deterministic while/for loops over finite, discrete state (arrays, counters, sets).
- Invariants as predicates over tracked state; variants as non-negative integers or well-founded tuples.
- Partial correctness (preservation) and total correctness (termination via variant).
- Excludes concurrency, probabilistic loops, or infinite-state systems (M18/M10).
- Assumes no break/return inside loops; desugar or treat as separate proof obligations if present.

Within this scope, the workflow yields verifiable proofs for standard loops in systems code.

---

## 1. Core Definitions

A loop invariant $I$ is a predicate that holds:
- **Initialisation**: Precondition $P$ implies $I$.
- **Preservation**: If $I \land G$ (guard), then body $B$ implies $I$ post-execution.
- **Postcondition**: $I \land \neg G$ implies postcondition $Q$. (Note: this ensures correctness on exit; termination is addressed separately via $V$.)

A loop variant $V$ (well-founded, e.g., $\mathbb{N}$ or lexicographic $\mathbb{N}^k$) ensures termination:
- Defined and $V \ge 0$ under $I \land G$.
- Strictly decreases after $B$ (under $I \land G$).
- Bounded below, precluding infinite descent.

**Theorem** (Hoare logic): If $P \implies I$, preservation holds, $I \land \neg G \implies Q$, and $V$ satisfies the above (non-negative under $I \land G$, decreases strictly post-$B$, well-founded), then the loop is partially correct w.r.t. $\{P\}$ loop $\{Q\}$ and terminates (total correctness).

---

## 2. Mechanical Derivation Workflow

For `while G: B` with $P$, $Q$:

1. Specify $P$, $Q$.
2. Identify loop variables and tracked state.
3. Derive $I$: From $Q$, restrict to "processed prefix/region"; add bounds (e.g., $0 \le i \le n$). Weaken by dropping conjuncts until preservation holds; simulate 0/1 iterations.
4. Prove preservation: Assume $I \land G$; show post-$B$ implies $I$.
5. Verify initialisation: $P \implies I$.
6. Exhibit $V$; prove decrease under $I \land G$, well-foundedness.
7. Verify consequence: $I \land \neg G \implies Q$.

**Heuristic**: $I$ = "$Q$ on processed prefix/region" + explicit bounds. Test: Holds after 0 iterations? After 1? On exit?

---

## 3. Canonical Example 1 – Linear Search

Find minimal `i` with `arr[i] == target` or -1 if absent.

$P$: `len(arr) = n \ge 0`.
$Q$: Returns minimal such `i` or -1.  
Code: `n = len(arr); i = 0; while i < n and arr[i] != target: i += 1; return i if i < n else -1`.

**Hoare Triple**: $\{P\}$ loop $\{Q\}$.

**Invariant**: $I$: $0 \le i \le n \land \forall j < i: \text{arr}[j] \ne \text{target}$.

- **Initialisation**: $i=0 \implies I$ (vacuous $\forall$).
- **Preservation**: Assume $I \land i < n \land \text{arr}[i] \ne \text{target}$. Post-$i += 1$: $0 \le i+1 \le n$; $\forall j < i+1$: holds for $j < i$ by $I$, for $j = i$ by guard.
- **Consequence**: If $i < n$, then $\text{arr}[i] = \text{target}$ (else guard fails); minimality by prefix. If $i = n$, absent.

**Variant**: $V = n - i$ ($\mathbb{N}$). Under $I \land G$: $V > 0$. Post-$B$: $V' = V - 1 < V$. Well-founded: $\ge 0$, $\le n$ steps.

---

## 4. Canonical Example 2 – Binary Search

Find minimal `i` in sorted `arr[L0:H0)` with `arr[i] >= target` or `H0` if absent. (Assumes non-decreasing `arr`; half-open intervals `[low, high)` throughout.)

$P$: `0 <= L0 <= H0 <= n`; `arr` sorted.  
$Q$: Returns minimal such `i` in `[L0, H0)` or `H0`.  
Code: `low = L0; high = H0; while low < high: mid = (low + high) // 2; if arr[mid] < target: low = mid + 1; else: high = mid`.

**Hoare Triple**: $\{P\}$ loop $\{Q\}$.

**Invariant**: $I$: $L0 \le \text{low} \le \text{high} \le H0 \land \forall j \in [L0, \text{low}): \text{arr}[j] < \text{target} \land \forall j \in [\text{high}, H0): \text{arr}[j] \ge \text{target}$.

- **Initialisation**: `low = L0`, `high = H0` $\implies I$ (vacuous $\forall$).
- **Preservation**: Assume $I \land \text{low} < \text{high}$. Let `mid = (low + high) // 2` ($\text{low} \le \text{mid} < \text{high}$).  
  - If `arr[mid] < target`: Set `low = mid + 1`. New bounds: $L0 \le \text{low}' = \text{mid}+1 \le \text{high} = \text{high}' \le H0$. For left $\forall j \in [L0, \text{low}'):$  
    - $j \in [L0, \text{low}):$ holds by old $I$.  
    - $j \in [\text{low}, \text{mid}]:$ sortedness and `arr[mid] < target` imply $\text{arr}[j] \le \text{arr[mid]} < \text{target}$.  
    Right $\forall$ unchanged (`high' = high`).  
  - Else: Set `high = mid`. New bounds hold. Left $\forall$ unchanged (`low' = low`). For right: $\forall j \in [\text{mid}, H0):$  
    - For $j = \text{mid}$, holds by branch condition `arr[mid] >= target`.  
    - For $j > \text{mid}$, sortedness implies $\text{arr}[j] \ge \text{arr[mid]} \ge \text{target}$.
- **Consequence**: `low == high` collapses interval. By $I$, if solution exists, `low` is minimal (left side <, right >=); else all < so `H0`.

**Variant**: $V = \text{high} - \text{low}$ ($\mathbb{N}$). Under $I \land G$: $V > 0$. Post-$B$:  
- If `arr[mid] < target`: $V' = \text{high} - (\text{mid}+1) \le \text{high} - (\text{low}+1) = V - 1 < V$.  
- Else: $V' = \text{mid} - \text{low} \le (\text{high}-1) - \text{low} = V - 1 < V$.  
Well-founded: $\ge 0$, $\le H0 - L0$ steps.

---

## 5. Quick Reference – Patterns

| Loop Type              | Invariant Sketch                                      | Variant Example                  |
|------------------------|-------------------------------------------------------|----------------------------------|
| Linear scan/search     | Prefix `[0..i)` satisfies partial $Q$; `0 <= i <= n` | $n - i$                          |
| Accumulator (sum/prod) | Accum = aggregate `[0..i)`; `0 <= i <= n`             | $n - i$                          |
| Two-pointer (partition)| `[L0..l) < pivot`; `[r..H0) >= pivot`; `l <= r`       | $r - l + 1$                      |
| Nested (i=0..n; j=0..M)| Outer prefix complete; inner to `j`; bounds           | $(n - i, M - j)$ (lex order)     |
| Decreasing (while >0)  | Remaining = initial - processed; processed ok         | Remaining count                  |

**Note**: Lexicographic order on tuples: Decreases if first differing component decreases.

---

## 6. Robustness – Tracked State and Mutations

- **Mutations**: Include all modified state in $I$ (e.g., "arr[0..i] sorted ascending"). Unmentioned mutations invalidate preservation.
- **Early exit**: Ensure $\neg G$ covers all paths to $Q$; desugar breaks/returns as separate cases.
- **Debug**: Assert $I$ at loop head (release: optional).

**Example**: Insertion sort outer: $I$: "arr[0..i] sorted"; variant: $n - i$.

---

## 7. Permanent Habit

Annotate every loop:

```python
def linear_search(arr, target):
    # Pre: n = len(arr) >= 0
    # Post: min i: arr[i]==target or -1
    n = len(arr)
    i = 0
    # Inv: 0 <= i <= n and for all j < i: arr[j] != target
    # Var: n - i (strictly decreases; value in N = {0, 1, 2, ...})
    while i < n and arr[i] != target:
        # assert 0 <= i <= n and all(arr[j] != target for j in range(i)) # debug
        i += 1
    return i if i < n else -1
```

Derive/prove before implement; simulate edges.

---

## 8. What You Must Carry Forward

1. $I$: Init from $P$; preserved by $B$; + $\neg G$ $\implies Q$.
2. $V$: $\ge 0$ under $I \land G$; strict decrease post-$B$; well-founded.
3. Workflow: $P/Q \to I$ (prefix + bounds) $\to$ proofs $\to V$.
4. Patterns: Prefix for scans; intervals for search/partition.
5. Track all mutations in $I$; no unmentioned state changes.

## 9. Progress Note & What’s Next in M05

After M05C01, derive proofs for deterministic loops, catching common errors.

M05C01 complete.

Next: **M05C02 – Induction for Arrays, Lists, Trees**: Strong induction on recursive structures.

---

## 10. Glossary & Notation

- $P$: Precondition – predicate over initial state before the loop.
- $Q$: Postcondition – predicate over final state after the loop.
- $G$: Guard – loop condition (Boolean expression controlling the loop).
- $B$: Body – the statement(s) executed on each loop iteration.
- $I$: Invariant – predicate preserved by each iteration; must hold on entry and at loop exit.
- $V$: Variant – non-negative, well-founded measure that strictly decreases on each iteration under $I \land G$; used to prove termination.
- Hoare triple $\{P\} S \{Q\}$: Program $S$ started in a state satisfying $P$ is guaranteed, if it terminates, to end in a state satisfying $Q$; with a valid variant, we obtain total correctness (termination + postcondition).
- $\mathbb{N}$: Set of non-negative integers $\{0,1,2,\dots\}$.
- Lexicographic order (“lex”): Order on tuples where $(a_1,\dots,a_k) < (b_1,\dots,b_k)$ if for the first index $i$ with $a_i \ne b_i$, we have $a_i < b_i$. Used for multi-dimensional variants.
- Processed prefix/region: Portion of an array or state that has already been examined/updated and is covered by the invariant.
- $\land$: Logical AND.
- $\neg$: Logical NOT.
- $\forall$: Universal quantifier ("for all").
# M05C02 · Induction for Arrays, Lists, Trees – Proving Recursive Algorithms

**Goal.** Equip practitioners with a mechanical framework for structural induction to verify recursive algorithms on arrays, lists, and trees. After this core, you will derive base cases, inductive hypotheses (IH), and steps for recursive functions, establishing correctness via strong induction—essential for proving invariants in divide-and-conquer, traversals, and transformations in Pythonic code.

**Scope** (explicit delimiters):
- Finite, well-founded structures (arrays of size $n \in \mathbb{N}$, lists via cons, binary trees).
- Strong induction: Assume IH for all smaller substructures; prove for current.
- Pre/postconditions on recursive calls; Python recursion (functions, not loops).
- Excludes coinduction, infinite structures, or probabilistic recursion (M10/M18).
- Assumes recursion depth is bounded by a function of input size small enough to fit within Python’s recursion limits; for unbounded depths, prefer iterative formulations.

Within this scope, the workflow certifies the typical recursive patterns used in data-structure and algorithmic code.

---

## 1. Core Definitions

Structural induction proves properties $P(S)$ over structures $S$ by:
- **Base case**: Verify $P$ for minimal $S$ (e.g., empty array/list, leaf tree).
- **Inductive hypothesis (IH)**: Assume $P$ holds for all proper substructures of $S$ (strong form: all smaller sizes).
- **Inductive step**: Using IH, prove $P(S)$ for arbitrary $S$.

For recursive algorithm $f(S)$ with precondition $Pre(S)$ and postcondition $Post(S, f(S))$:
- Base: $Pre(base) \implies Post(base, f(base))$.
- Step: Assume $Pre(sub) \implies Post(sub, f(sub))$ for substructures; show $Pre(S) \implies Post(S, f(S))$ via recursive calls.

**Theorem** (structural induction): If base holds and step uses strong IH, then $Pre(S) \implies Post(S, f(S))$ for all $S$. This establishes correctness assuming termination. Together with a well-founded size measure $|S|$ that strictly decreases on every recursive call, we obtain total correctness.

This mirrors Hoare logic for recursion: $\{Pre\} f \{Post\}$.

---

## 2. Mechanical Derivation Workflow

For a recursive $f$ on a structure $S$ with a chosen well-founded size measure $|S| \in \mathbb{N}$ (e.g. length for arrays/lists, number of nodes for trees):

1. Define $Pre(S)$, $Post(S, res)$.
2. Identify base ($|S|=0/1$) and recursive decomposition ($S \to sub_1, \dots, sub_k$ with $|sub_i| < |S|$).
3. Base: Prove directly (no IH).
4. IH: Assume for all $S'$ with $|S'| < |S|$, $Pre(S') \implies Post(S', f(S'))$.
5. Step: From $Pre(S)$, show recursive calls satisfy $Pre(sub_i)$; apply IH to get $Post(sub_i, f(sub_i))$; combine to $Post(S, f(S))$.
6. Termination: Each call on proper substructure ($|sub| < |S|$); well-founded via $\mathbb{N}$.
7. Verify: Simulate small $|S|$; check against Python REPL.

**Heuristic**: IH = "$Post$ on proper prefixes/subs"; step mirrors recursion skeleton.

**Strong vs. Simple**: Strong assumes all smaller; use when step relies on multiple sizes (e.g., Fibonacci: $f(n) = f(n-1) + f(n-2)$, needs IH for both). Sketch: $Pre(n): n \ge 0$; $Post(n, f(n))$: $f(n)$ = mathematical Fibonacci. Base $n=0,1$: $f(0)=0$, $f(1)=1$. Step: $f(n) = f(n-1) + f(n-2)$; IH for $n-1 < n$ and $n-2 < n$ $\implies Post(n)$. In the step, we use the IH for both $n-1$ and $n-2$, which are both $< n$; this is exactly what strong (not simple) induction buys us.

---

## 3. Canonical Example 1 – Recursive Array Sum

Compute $\sum arr[0..n)$ recursively. For this example, we instantiate $S := (arr, n)$, and write $Pre(S)$, $Post(S, res)$ interchangeably with $Pre(arr, n)$, $Post(arr, n, res)$; $arr$ is fixed and $n$ decreases.

$Pre(S)$: $0 \le n \le \text{len}(arr)$.  
$Post(S, res)$: $res = \sum_{i=0}^{n-1} arr[i]$.  
Code:
```python
from typing import List

def sum_rec(arr: List[int], n: int) -> int:
    if n == 0:
        return 0
    return arr[n-1] + sum_rec(arr, n-1)  # simple linear recursion
```

**Inductive Proof** (measure: $n$):

- **Base** ($n=0$): $Pre(S) \implies sum_rec(arr,0) = 0 = \sum \emptyset$, holds.
- **IH**: For all $m < n$, $Pre(arr,m) \implies Post(arr,m, sum_rec(arr,m))$.
- **Step** ($n > 0$): $Pre(S)$ holds ($0 < n \le \text{len}(arr)$). Recursive call: sum_rec(arr, n-1); $Pre(arr,n-1)$ ($0 \le n-1 < n \le \text{len}(arr)$); IH $\implies Post(arr,n-1, sum_rec(arr,n-1)) = \sum_{i=0}^{n-2} arr[i]$. Then $res = arr[n-1] +$ that $= \sum_{i=0}^{n-1} arr[i] = Post(S,res)$.
- **Termination**: Each call decreases $n$ by 1; $\le n$ steps (well-founded $\mathbb{N}$).

Pythonic note: Use slicing `sum(arr[:n])` but recursion exposes structure; links to M05C01 loop invariants for iterative sum.

---

## 4. Canonical Example 2 – Recursive List Reversal

Reverse list $lst$ of length $n$ into new list. Here the structure $S$ is the list $lst$, with size $|S| = \text{len}(lst)$.

Mathematical reverse: Defined inductively as reverse([]) = []; reverse([x] + tail) = reverse(tail) + [x]. This is the abstract, mathematical reverse we want to implement.

$Pre(S)$: $S$ finite list.  
$Post(S, res)$: $res =$ mathematical reverse of $S$.  
Code:
```python
from typing import List

def reverse_rec(lst: List[int]) -> List[int]:
    # Pre: lst finite list
    # Post: res = mathematical reverse of lst
    if not lst:
        return []
    return reverse_rec(lst[1:]) + [lst[0]]
```

**Inductive Proof** (measure: $n = \text{len}(lst)$):

- **Base** ($n = 0$): lst = [], `reverse_rec([]) = []` = reverse([]), holds.
- **IH**: For all $m < n$, for all lists xs with len(xs) = m, `reverse_rec(xs)` = reverse(xs).
- **Step** ($n > 0$): Write lst = [x] + tail with len(tail) = n-1 < n. By IH, `reverse_rec(tail)` = reverse(tail). Result = `reverse_rec(tail) + [x]` = reverse(tail) + [x]. The second equality is exactly the inductive definition of the mathematical reverse: reverse([x] + tail) = reverse(tail) + [x] = reverse(lst).
- **Termination**: Calls on shorter tails; $\le n$ steps.

Pythonic: `lst[::-1]` canonical, but recursion teaches cons/decons.

---

## 5. Canonical Example 3 – Binary Tree Inorder Traversal

Traverse binary tree $T$ of height $h$, collect inorder list. Here the structure $S$ is the (sub)tree rooted at root, with size $|S| =$ number of nodes in that subtree.

Define TreeNode:
```python
from typing import List, Optional

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right
```

$Pre(S)$: $S$ finite binary tree.  
$Post(S, res)$: $res =$ [inorder vals: left, root, right].  
Code:
```python
def inorder_rec(root: Optional[TreeNode]) -> List[int]:
    if not root:
        return []
    return inorder_rec(root.left) + [root.val] + inorder_rec(root.right)
```

**Inductive Proof** (strong on subtrees; measure = number of nodes):

- **Base** ($S=$ None/leaf, size 0/1): $[] / [val]$, holds (vacuous/empty subs).
- **IH**: For all proper subtrees $S'$ (fewer nodes), $Pre(S') \implies Post(S', inorder_rec(S'))$.
- **Step** ($S$ non-leaf): Subs $left, right$ proper (fewer nodes). IH $\implies inorder_rec(left) =$ left inorder, similarly right. Then $res =$ left + [val] + right $=$ inorder($S$).
- **Termination**: Each recursive call is on a proper subtree with strictly fewer nodes. Since the number of nodes is a natural number and decreases on every call, recursion terminates.

Pythonic: Aligns with `itertools` patterns; recursion natural for trees.

---

## 6. Quick Reference – Patterns

| Structure     | Base Case                          | IH (Subs)                  | Step (Combine)             |
|---------------|------------------------------------|----------------------------|----------------------------|
| Array (len n) | n=0: res = neutral element (e.g. 0, []) | Prefix m<n satisfies Post  | Combine prefix result with arr[n-1] |
| List (cons)   | []: res=[]                         | Tail m<n reverses          | IH(tail) + head            |
| Tree (node)   | None/leaf: []/[val]                | Left/right subtrees        | IH(left) + [val] + IH(right)|
| Nested (mat)  | Row 0: base row                    | Rows 0..i-1 correct        | IH(i-1) + process row i    |

**Note**: Measure: len/nodes/height; strong IH over all smaller.

---

## 7. Robustness – Recursion and Python

- **Stack overflow**: Depth grows with the chosen size measure. CPython limits recursion depth (≈1000 by default), so for unbounded inputs prefer iterative implementations; `sys.setrecursionlimit` is a last resort.
- **Immutability**: Python lists mutable; when reasoning, treat the contents of the slice arr[:n] as the logical sequence; mutations outside that slice do not affect the proof (assuming the algorithm itself only reads from arr[:n] and does not mutate this logical prefix between recursive calls).
- **Typing**: Use type hints + mypy to catch obvious misuse, but this is orthogonal to the proof.
- **Debug**: Assert IH post-subcall (e.g., assert len(res) == n).

**Performance Note**: In reverse_rec and inorder_rec, list concatenation with + gives O(n²) behaviour due to repeated copying. We use it here because it mirrors the inductive specification cleanly; a production implementation would instead build the result in an explicit accumulator and reverse at the end, or use a generator (yield from) to avoid copying.

**Example**: Merge sort recursive: IH sorted halves; step merge preserves sorted.

---

## 8. Permanent Habit

Annotate recursions:

```python
def sum_rec(arr: List[int], n: int) -> int:
    # Pre: 0 <= n <= len(arr)
    # Post: res = sum(arr[0:n])
    if n == 0:  # Base: res = 0
        return 0
    # IH: sum_rec(arr, m) = sum(arr[0:m]) for m < n
    sub = sum_rec(arr, n-1)  # Pre(n-1) holds
    # assert sub == sum(arr[:n-1])  # debug IH
    return arr[n-1] + sub  # Step: + last
```

Prove base/IH/step before code; test small n.

---

## 9. What You Must Carry Forward

1. Base: Direct for minimal.
2. IH: Strong on smaller subs.
3. Step: Decompose, apply IH, combine.
4. Workflow: $Pre/Post \to$ base $\to$ IH/step $\to$ termination.
5. Patterns: Prefix/cons for seq; recurse+combine for trees.
6. Python: Type/recursion limits; assert subs.

## 10. Progress Note & What’s Next in M05

After M05C02, prove recursive correctness via structural induction, bridging loops to trees.

M05C02 complete.

Next: **M05C03 – Pre/postconditions and contracts in Python**: Runtime enforcement via typing/decorators.

---

## 11. Glossary & Notation

- $P$: Precondition – predicate on input structure.
- $Q$: Postcondition – predicate on output given input.
- IH: Inductive hypothesis – assumption for smaller cases.
- Base: Minimal structure case (no IH).
- Step: Proof using IH on decomposition.
- $\{P\} f \{Q\}$: Hoare triple for function $f$.
- $\mathbb{N}$: Non-negative integers $\{0,1,2,\dots\}$.
- Proper substructure: Immediate children or prefixes (smaller measure).
- Strong induction: Assume all $k < n$; prove $n$.
# M05C03 · Pre/postconditions and Contracts in Python – Enforcing Correctness at Runtime

**Goal.** This core establishes a disciplined approach to specifying and enforcing pre/postconditions for functions and methods in Python, transforming informal assumptions into verifiable contracts. Upon completion, practitioners will systematically annotate code with preconditions, postconditions, and invariants, leveraging type hints, assertions, and decorators to catch errors early—bridging theoretical proofs (M05C01–C02) to robust, production-grade implementations.

**Scope** (explicit delimiters):
- Functions/methods with finite, discrete inputs/outputs (e.g., DS operations, algorithms).
- Static (type hints/mypy) and dynamic (assertions/decorators) enforcement.
- Hoare-style triples $\{Pre\} f \{Post\}$; excludes full verification tools (e.g., Dafny).
- Python 3.10+; focuses on stdlib/typing (no external libs unless noted).
- Assumes deterministic code; no concurrency or side-effect-heavy I/O (M18/M20).

Within this scope, the workflow integrates contracts into Pythonic code, aligning with community best practices (PEP 484, mypy).

---

## 1. Core Definitions

A function contract specifies:
- **Precondition $Pre(x)$**: Predicate on inputs $x$; must hold before $f(x)$.
- **Postcondition $Post(x, y)$**: Predicate on inputs $x$ and output $y = f(x)$; must hold after.
- **Invariant $I(S)$**: State predicate preserved across calls (from M05C01–C02).

Hoare triple $\{Pre\} f \{Post\}$: If $Pre(x)$ holds, $f$ terminates with $Post(x, f(x))$.

**Enforcement**:
- **Static**: Type hints for shape (e.g., `List[int]`); mypy checks types but ignores semantic strings in `Annotated` (purely documentary).
- **Dynamic**: Assertions/decorators for predicates; fail-fast on violation.

**Theorem** (contract composition): If $\{Pre_1\} f_1 \{Post_1 = Pre_2\}$ and $\{Pre_2\} f_2 \{Post_2\}$, then $\{Pre_1\} f_1; f_2 \{Post_2\}$ (sequential correctness).

Contracts prevent misuse: Caller ensures $Pre$; callee assumes it, guarantees $Post$.

---

## 2. Mechanical Derivation Workflow

For $f$ with inputs $x$, output $y$ (Pre/postconditions here are exactly the $P/Q$ predicates from M05C01–C02; invariants from loops/recursions get turned into assert checks at boundaries):

1. Specify $Pre(x)$, $Post(x,y)$ (logical predicates; e.g., $0 \le n \le \text{len}(arr)$).
2. Encode statically: Type hints for shape; `Annotated` for documentary metadata (mypy ignores strings).
3. Encode dynamically: Decorator with callables for $Pre/Post$ or inline `assert` (e.g., `assert Pre(x)` pre-call; `assert Post(x,y)` post).
4. Integrate invariants: For loops/recursion, assert $I$ at boundaries (M05C01–C02).
5. Test: Unit tests exercising boundaries; mypy for static errors.
6. Production: Use explicit exceptions for public $Pre$ violations; disable `assert` via `-O`.
7. Verify: Fuzz inputs (M05C07); check against spec.

**Heuristic**: $Pre$ from caller assumptions; $Post$ from callee guarantees. Use dataclasses for structured $x/y$. Properties like sortedness, bounds, or invariants are semantic conditions beyond what standard typing encodes; they must be enforced dynamically (asserts/contract decorator) or by external tools.

---

## 3. Canonical Example 1 – Array Prefix Sum with Contracts

Compute prefix sums up to $n$; enforce bounds.

$Pre(arr, n)$: $arr$ list[int], $0 \le n \le \text{len}(arr)$.  
$Post(arr, n, res)$: $len(res) = n$ and $\forall k=1\dots n: res[k-1] = \sum_{i=0}^{k-1} arr[i]$ (or $res=[]$ if $n=0$).  
Code (iterative, with callable-based decorator):
```python
from collections.abc import Callable
from functools import wraps
from typing import List, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

def contract(
    pre: Callable[..., bool] | None = None,
    post: Callable[..., bool] | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator for runtime contracts via callables (no eval).
    Intended for internal/debug builds; uses assert, so checks are
    removed under python -O.
    """
    def decorator(f: Callable[P, R]) -> Callable[P, R]:
        @wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            if pre is not None:
                assert pre(*args, **kwargs), f"Precondition failed for {f.__name__}"
            result = f(*args, **kwargs)
            if post is not None:
                # Convention: post sees *args, **kwargs, result
                assert post(*args, **kwargs, result), f"Postcondition failed for {f.__name__}"
            return result
        return wrapper
    return decorator

def check_bounds(arr: List[int], n: int) -> bool:
    return 0 <= n <= len(arr)

def check_prefix(arr: List[int], n: int, res: List[int]) -> bool:
    # Rich check: O(n^2) due to sum; for prod, use cheaper proxy (e.g., len + sum(res) == sum(arr[:n]))
    if n == 0:
        return res == []
    return (len(res) == n and
            all(sum(arr[:k]) == res[k-1] for k in range(1, n+1)))

@contract(pre=check_bounds, post=check_prefix)
def prefix_sum(arr: List[int], n: int) -> List[int]:
    res = []
    total = 0
    for i in range(n):
        total += arr[i]
        res.append(total)
    return res
```

**Verification**:
- Static: Type hints + mypy catches shape errors (e.g., wrong arg types).
- Dynamic: Decorator asserts $Pre$ entry, $Post$ exit; fails on $n<0$ or wrong sums.
- Invariant (loop): $total = \sum arr[0..i)$; assert at head for debug.

Usage: `prefix_sum([1,2,3], 2) → [1,3]`; `prefix_sum([], -1)` raises AssertionError.

---

## 4. Canonical Example 2 – Stack Operations with Method Contracts

Simple stack class; enforce non-empty pop.

$Pre(stack, elem)$: Stack finite list (any elem).  
$Post(stack, elem, new_stack)$: $new_stack = stack + [elem]$.  
For pop: $Pre(stack)$: $\text{len}(stack) > 0$; $Post(stack, elem)$: $elem = stack[-1]$, new_stack = stack[:-1].  
Code (dataclass + inline checks):
```python
from dataclasses import dataclass
from typing import Generic, List, TypeVar

T = TypeVar("T")

@dataclass
class Stack(Generic[T]):
    _data: List[T]

    def push(self, elem: T) -> None:
        # Pre: none (any elem); Post: length +1, top=elem (partial check)
        old_len = len(self._data)
        self._data.append(elem)
        # Cost-effective approx to 'new_stack = old_stack + [elem]'
        assert len(self._data) == old_len + 1, "Post violation: length unchanged"
        assert self._data[-1] == elem, "Post violation: top not elem"
    
    def pop(self) -> T:
        # Pre: non-empty (public API: raise, not assert)
        if not self._data:
            raise IndexError("pop from empty stack")  # Caller bug
        old_len = len(self._data)
        old_top = self._data[-1]
        elem = self._data.pop()
        # Post: length -1, elem == old top (partial; trust list.pop for prefix unchanged)
        assert len(self._data) == old_len - 1, "Post violation: length unchanged"
        assert elem == old_top, "Post violation: not last element"
        return elem
    
    @property
    def size(self) -> int:
        # Pre/Post: always true
        return len(self._data)
```

**Verification**:
- Static: Type hints + mypy for generics/shape.
- Dynamic: Inline asserts for $Post$; explicit `raise` for public $Pre$ (not assert, as disabled in `-O`).
- Invariant: Size non-decreasing post-push, decreasing post-pop.

Usage: `s = Stack([]); s.push(1); s.pop()` → 1; `s.pop()` → IndexError.

Pythonic: Dataclasses for state; properties for views.

---

## 5. Canonical Example 3 – Binary Search with Full Contracts

Find insertion point in sorted array (from M05C01).

$Pre(arr, target)$: $arr$ sorted non-decreasing list[int].  
$Post(arr, target, idx)$: $0 \le idx \le \text{len}(arr)$ and ($\forall j < idx: arr[j] < target$) and ($idx = \text{len}(arr)$ or $arr[idx] \ge target$).  
Code (with contracts):
```python
from typing import List
from bisect import bisect_left  # oracle for test

def is_sorted(arr: List[int]) -> bool:
    return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))

def binary_search(arr: List[int], target: int) -> int:
    # Pre: arr sorted; dynamic check optional in debug
    if __debug__:
        assert is_sorted(arr), "Pre violation: arr not sorted"
    low, high = 0, len(arr)
    # Inv: low <= high /\ forall j in [0,low): arr[j] < target /\
    #      forall j in [high,len(arr)): arr[j] >= target
    while low < high:
        mid = (low + high) // 2
        assert 0 <= mid < len(arr)  # Inv bound (debug)
        if arr[mid] < target:
            low = mid + 1
        else:
            high = mid
    # Post: low == high is insertion point
    assert 0 <= low <= len(arr)
    assert low == 0 or arr[low-1] < target
    assert low == len(arr) or arr[low] >= target
    return low
```

**Verification**:
- Static: Type hints + mypy for lists/ints.
- Dynamic: `__debug__` guards $Pre$ (disabled in `-O`); asserts for Inv/$Post$.
- Test: `assert binary_search([1,3,5], 2) == 1`; oracle: `bisect_left(arr, target)`.

Pythonic: Complements `bisect`; contracts enable safe reuse.

---

## 6. Quick Reference – Patterns

| Construct     | Encoding Static                  | Encoding Dynamic             | Common Pitfalls              |
|---------------|----------------------------------|------------------------------|------------------------------|
| Function Pre  | Type hints (shape only)          | `if not Pre: raise ValueError` | Using assert for public API  |
| Function Post | Return type hints                | Inline `assert Post`         | Mutable outputs (aliasing)   |
| Method Inv    | `@property` with check           | Loop/recursion asserts       | Side effects in subs         |
| DS Contract   | Dataclass fields hinted          | `__init__` raises on invalid | Empty/full state violations  |

**Note**: Annotated[T, "doc"] for documentary metadata; mypy ignores strings, treats as T. Use `@beartype` for advanced runtime if needed.

---

## 7. Robustness – Contracts in Practice

- **Overhead**: Assert checks run in normal/debug mode and are stripped in optimized runs (`python -O`), so they are effectively free in optimized builds; mypy fast for CI.
- **Mutability**: For lists, contract on views/slices; use immutable types (tuples) where possible.
- **Assert vs Exceptions**: Public API $Pre$ violations → explicit `raise` (ValueError/IndexError); internal invariants/$Post$ → `assert` (compiled away in opt).
- **Composition**: Chain via $Post_1 \implies Pre_2$; test intermediates.
- **Testing**: Hypothesis for boundary fuzz (M05C07); coverage on $Pre$ violations.

**Example**: Queue: $Pre(append, elem)$: any; $Post$: size +=1; $Pre(dequeue)$: size>0 (raise Empty).

---

## 8. Permanent Habit

Annotate systematically:

```python
from typing import List

def prefix_sum(arr: List[int], n: int) -> List[int]:
    # Pre: 0 <= n <= len(arr)  # doc; raise if public
    if n < 0 or n > len(arr):
        raise ValueError("n out of bounds")
    # Post: len(res)==n /\ sums correct
    res = [sum(arr[:k]) for k in range(1, n+1)]
    assert len(res) == n  # internal Post
    return res
```

Spec → prove (M05C01–C02) → annotate → test; mypy in CI.

---

## 9. What You Must Carry Forward

1. $\{Pre\} f \{Post\}$: $Pre$ caller duty; $Post$ callee guarantee.
2. Static: Type hints/mypy (shape); dynamic: raise/assert.
3. Workflow: Spec $Pre/Post$ → encode → verify → integrate Inv.
4. Patterns: Bounds for indices; sortedness for search; size for DS.
5. Fail-fast: Raise public $Pre$; assert internal.

## 10. Progress Note & What’s Next in M05

After M05C03, enforce specs at runtime/static, enabling safe composition.

M05C03 complete.

Next: **M05C04 – Termination arguments and well-founded measures**: Beyond variants to general programs.

---

## 11. Glossary & Notation

- $Pre(x)$: Precondition – must-hold predicate on inputs $x$.
- $Post(x,y)$: Postcondition – must-hold on $x$, $y=f(x)$.
- $\{Pre\} f \{Post\}$: Hoare triple – correctness guarantee.
- Annotated[T, "doc"]: Typing for documentary metadata; mypy ignores strings, treats as T.
- Invariant $I$: Preserved state (M05C01–C02).
- Fail-fast: Raise on violation early (vs silent error).
# M05C04 · Termination Arguments and Well-Founded Measures – Proving Finiteness

**Goal.** This core provides a mechanical toolkit for establishing termination in general programs, extending loop variants (M05C01) and inductive measures (M05C02) to arbitrary structures via well-founded orders. Upon completion, practitioners will derive termination arguments for recursive functions, iterative processes, and composite algorithms, ensuring no infinite loops or non-terminating recursion—critical for safe, predictable systems code. Total correctness = partial correctness (M05C01–C03) + termination.

**Scope** (explicit delimiters):
- Programs where each possible transition step strictly decreases a well-founded measure $V$. Determinism is not required for the theorem, but we restrict to deterministic algorithms in this core.
- Well-founded partial orders $(\mathcal{W}, <)$; measures $V: State \to \mathcal{W}$.
- Termination: Every execution is finite (no infinite paths).
- Excludes non-determinism or probabilistic termination (M10/M18).
- Pythonic focus: Depth-bounded recursion; iterative fallbacks for production.

Within this scope, the workflow certifies termination for standard algorithmic patterns.

---

## 1. Core Definitions

A program terminates if every execution sequence from any initial state is finite, reaching a state with no further transitions.

**Transition system**: States $State$; relation $\to \subseteq State \times State$; fixed points: $s$ with no $s \to s'$.

**Well-founded order $(\mathcal{W}, <)$**: Strict partial order with no infinite descending chains ($w_1 > w_2 > \dots$ impossible).

**Termination measure $V: State \to \mathcal{W}$**: For non-fixed $s \to s'$, $V(s') < V(s)$ (strict decrease).

**Theorem** (well-founded measure termination): Let $(\mathcal{W}, <)$ be well-founded and $V: State \to \mathcal{W}$. If for all non-fixed transitions $s \to s'$ we have $V(s') < V(s)$, then every sequence from any initial $s_0$ is finite (ends at fixed point).  
*Proof sketch*: Assume for contradiction an infinite $s_0 \to s_1 \to s_2 \to \dots$; then $V(s_0) > V(s_1) > V(s_2) > \dots$, contradicting well-foundedness (no infinite descent).

Extends M05C01 variants ($\mathcal{W} = \mathbb{N}$); composes with contracts (M05C03). Upgrade from M05C01: Loop variant $V \in \mathbb{N}$ is special case ($s \to s'$ decreases counter); here generalize to multi-component lex orders.

---

## 2. Mechanical Derivation Workflow

For program $Prog$ with states $State$, transitions $\to$:

1. Define fixed points: States with no outgoing $\to$ (e.g., guards false).
2. Choose well-founded $\mathcal{W}$ (e.g., $\mathbb{N}$ for linear, lex $\mathbb{N}^k$ for nested).
3. Define $V: State \to \mathcal{W}$ (e.g., remaining work).
4. Prove decrease: For each transition rule, non-fixed $s \to s'$ has $V(s') < V(s)$.
5. Apply theorem: No infinite paths; all executions finite.
6. Optional bound: If $V \in \mathbb{N}$ and decreases by $\ge 1$, length $\le V(init)$.
7. Verify: Simulate sequences; test max steps.

**Heuristic**: $V =$ "global remaining work" (e.g., unprocessed nodes + max depth); use lex for multi-level (decreases outer before inner); sums over tasks for worklists (total work decreases, even if local increases).

---

## 3. Canonical Example 1 – Iterative Fibonacci (Scalar Measure)

Compute $F_n$ iteratively.

$Pre(n)$: $n \ge 0$.  
$Post(n, res)$: $res = F_n$. Fixed: $i \ge n$.  
Code:
```python
def fib_iter(n: int) -> int:
    if n == 0:
        return 0
    a, b = 0, 1
    i = 1
    while i < n:  # G: i < n
        a, b = b, a + b  # Step
        i += 1
    return b
```

**Termination Proof** (measure: $V = n - i \in \mathbb{N}$; upgrade from M05C01 variant):

- **Fixed points**: $i \ge n$ (G false).
- **Decrease**: Assume G ($i < n$, $V > 0$): Post-step $i' = i+1$, $V' = n - (i+1) = V - 1 < V$.
- **Well-founded**: $\mathbb{N}$; no descent.
- **Apply theorem**: No infinite paths; execution finite.
- **Bound**: Decreases by 1; $\le n$ steps.

Pythonic: O(n) efficient; scalar $V$ reinforces M05C01.

---

## 4. Canonical Example 2 – Mutual Recursion: Even/Odd Parity

Parity check via mutual recursion.

$Pre(n)$: $n \ge 0$.  
$Post(n, even(n))$: True iff n even. Fixed: $n=0$.  
Code:
```python
def is_even(n: int) -> bool:
    if n == 0:
        return True
    return is_odd(n - 1)

def is_odd(n: int) -> bool:
    if n == 0:
        return False
    return is_even(n - 1)
```

**Termination Proof** (measure: $V = n \in \mathbb{N}$; mutual induction on both functions):

- **Fixed points**: $n=0$ (bases return).
- **Decrease**: $even(n>0) \to odd(n-1)$: $V' = n-1 < n$; $odd(n>0) \to even(n-1)$: same.
- **Well-founded**: $\mathbb{N}$.
- **Apply theorem**: No infinite paths.
- **Mutual induction**: Prove by simultaneous IH on $n$: Assume for all $m < n$, both terminate; from $n$, calls $n-1 < n$ (terminates by IH); chain finite.
- **Bound**: Depth $\le n$ (each call decreases $n$ by 1).

Pythonic: Illustrates mutual; prefer bit ops (`n % 2 == 0`) for prod.

---

## 5. Canonical Example 3 – Nested Loops: Matrix Transpose (Lex Measure)

Transpose $n \times m$ matrix iteratively. Worked lex example: outer loop over columns, inner loop over rows.

$Pre(mat, n, m)$: $mat$ list[list[int]] with $n$ rows, each len $m$.  
$Post$: $transposed = [[mat[j][i] \text{ for } j=0..n-1] \text{ for } i=0..m-1]$. Fixed: $i \ge m$, $j \ge n$.  
Code:
```python
def transpose_nested(mat: list[list[int]], n: int, m: int) -> list[list[int]]:
    trans = [[0] * n for _ in range(m)]
    i = 0  # col
    while i < m:  # Outer G: i < m
        j = 0  # row
        while j < n:  # Inner G: j < n
            trans[i][j] = mat[j][i]
            j += 1
        i += 1
    return trans
```

**Termination Proof** (measure: $V = (m - i, n - j) \in \mathbb{N}^2$, lex order; first coord outer, second inner):

- **Fixed points**: $i \ge m$ (outer false); inner $j \ge n$.
- **Decrease**:
  - Inner step ($j < n$): $j' = j+1$, $V' = (m-i, n-(j+1)) < (m-i, n-j)$ (second coord drops).
  - Outer step (inner finished, $j \ge n$): $i' = i+1$, resets $j=0$; $V$ at end of inner = $(m-i, 0)$; next outer start $V' = (m-(i+1), n-0)$; first coord drops ($m-i-1 < m-i$), second resets but lex ignores.
- **Well-founded**: Lex $\mathbb{N}^2$; no descent.
- **Apply theorem**: No infinite paths.
- **Bound**: Outer $\le m$, inner $\le n$ per outer; total $\le m \cdot n$.

Pythonic: Explicit loops for control; lex $V$ for nested.

---

## 6. Quick Reference – Patterns

| Program Type | Measure $V$                  | Decrease on Step             | Invariant/Fixed              |
|--------------|------------------------------|------------------------------|------------------------------|
| Loop (while) | Remaining iters $\in \mathbb{N}$ | Guard true → iter +1         | Guard false                  |
| Recursion    | Args lex $\mathbb{N}^k$      | Call on smaller args         | Base cases                   |
| Mutual Rec   | Shared param $\in \mathbb{N}$ | Each drops param             | Bases ($n=0$)                |
| Graph Search | #unvisited $\in \mathbb{N}$ | Mark node; recurse subs      | All visited; visit once      |
| Worklist     | len(worklist) $\in \mathbb{N}$ | Process item; add finite subs | Worklist empty               |

**Note**: Lex: Prioritizes first coord; use for multi-level. Invariant often key (e.g., no re-process). For monotone dataflow (finite-height lattice), $V =$ height of current approximation; each update decreases (each update moves the global state down in the lattice order and the lattice has no infinite descending chains).

---

## 7. Robustness – Termination in Python

- **Stack overflow**: If recursion depth $\le V(init)$ (e.g., $V$ tracks calls), safe; else iterative. `sys.setrecursionlimit` last resort (default 1000).
- **Infinite loops**: Guards must cover paths; assert $V$ decrease in debug.
- **Composition**: $V = (V_1, V_2)$ lex if sequential.
- **Timeouts**: Engineering safeguard (e.g., `signal.alarm`); appropriate when no termination argument, but does not prove logical finiteness.
- **Testing**: Simulate max $V(init)$; Hypothesis paths (M05C07).

**Example**: Quicksort: $V =$ subarray size lex over calls; each recurses on strictly smaller.

---

## 8. Permanent Habit

Annotate with measure:

```python
def fib_iter(n: int) -> int:
    # Pre: n >= 0; Post: res = F_n
    # Term: V = n - i \in N; decreases on i +=1
    if n == 0:
        return 0
    a, b = 0, 1
    i = 1
    while i < n:  # G: i < n
        # assert n - i > 0  # V > 0 under G (debug)
        a, b = b, a + b
        i += 1  # V decreases
    return b
```

Prove decrease before code; test max steps.

---

## 9. What You Must Carry Forward

1. $V: State \to \mathcal{W}$: Well-founded, strict decrease on steps.
2. Fixed: No transitions (guards false).
3. Workflow: Fixed → $V$ → decrease proof → well-founded induction.
4. Patterns: $\mathbb{N}$ for linear; lex $\mathbb{N}^k$ for nested/mutual.
5. Python: Depth $\le V$; iterative for safety.

## 10. Progress Note & What’s Next in M05

After M05C04, prove termination for general programs, completing correctness toolkit.

M05C04 complete.

Next: **M05C05 – Encoding invariants as runtime checks and debug modes**: From proof to code.

---

## 11. Glossary & Notation

- $V$: Termination measure – maps to well-founded set, decreases strictly.
- $\mathcal{W}$: Well-founded order – no infinite descents (e.g., $\mathbb{N}^k$ lex).
- Lex: Lexicographic – $(a,b) < (c,d)$ if $a<c$ or ($a=c, b<d$).
- Fixed point: State with no outgoing transition.
- Termination: Every execution finite (no infinite paths).
# M05C05 · Encoding Invariants as Runtime Checks and Debug Modes – From Proof to Code

**Goal.** This core translates mathematical invariants and variants (M05C01–C04) into runtime assertions and debug-mode checks in Python, enabling early detection of violations without production overhead. Upon completion, practitioners will embed invariants as conditional asserts, using `__debug__` and logging to verify correctness during development and testing—transforming proofs into self-checking code that fails fast on bugs.

**Scope** (explicit delimiters):
- Deterministic code with proved invariants/variants (loops, recursion, DS).
- Debug-mode enforcement: `__debug__`, `if DEBUG:`; excludes full symbolic execution.
- Python 3.10+ stdlib (logging, assert); no external tools (e.g., Hypothesis in M05C07).
- Focuses on fail-fast invariants; excludes performance-critical paths (M02).
- Assumes specs proved (M05C01–C04); runtime checks approximate (not exhaustive): The asserts are monitors: they detect violations if they happen; they do not constitute a proof.

Within this scope, the workflow embeds checks without altering semantics, aligning with Pythonic practices (logging best practices).

---

## 1. Core Definitions

**Invariant encoding**: From proved $I$ (holds pre/post body), insert `assert I` at loop/recursion boundaries.

**Variant encoding**: From proved $V$ decrease, snapshot pre/post-step; insert `assert V_post < V_pre` (or `V > 0` under guard).

**Debug mode**: Use `__debug__` (True unless `python -O`): Guards checks; disabled in optimized/production.

**Fail-fast principle**: Violations raise AssertionError early (debug); log in release for monitoring.

**Theorem** (soundness preservation): Adding `assert I` at invariant points preserves semantics if $I$ proved (M05C01–C04); checks are no-ops when true.

Extends contracts (M05C03): Invariants as internal $Post$ on steps; composes with termination (M05C04). Never put side effects in assert expressions (e.g., no mutations); they vanish under -O.

---

## 2. Mechanical Derivation Workflow

For proved $Prog$ with invariants $I$, variants $V$:

1. Identify check points: Loop head/tail (for $I$), body post (for $V$ decrease), recursion entry/exit.
2. Encode $I$: `if __debug__: assert I` (predicate as bool expr).
3. Encode $V$: Snapshot pre/post; `if __debug__: assert V_post < V_pre`.
4. Logging: Optional `logging.debug(f"I: {I}")` for traces (DEBUG level; configure at entrypoint).
5. Modes: `__debug__` for asserts; env var `DEBUG=True` for extras.
6. Test: Inject violations (e.g., mutate guard); verify raises/logs.
7. Production: `-O` strips asserts; logs optional.

**Heuristic**: Simple expr for $I/V$ (e.g., `len(visited) == i`); snapshot temps for pre/post.

---

## 3. Canonical Example 1 – Loop Invariant Check: Linear Search

From M05C01: Invariant $I$: $0 \le i \le n \land \forall j < i: arr[j] \ne target$.

Code with encoded checks:
```python
import logging

# Configure at entrypoint, e.g., if __name__ == "__main__":
#     logging.basicConfig(level=logging.DEBUG if __debug__ else logging.INFO)

def linear_search(arr: list[int], target: int) -> int:
    n = len(arr)
    i = 0
    # Inv: 0 <= i <= n and all(arr[j] != target for j in range(i))
    while i < n and arr[i] != target:
        if __debug__:
            assert 0 <= i <= n, "Invariant violation: i out of bounds"
            assert all(arr[j] != target for j in range(i)), "Invariant violation: target in prefix"
            logging.debug(f"Loop head: i={i}, prefix clean")
        i += 1
    # Post-check Inv (holds on exit)
    if __debug__:
        assert 0 <= i <= n, "Invariant violation on exit"
        assert all(arr[j] != target for j in range(i)), "Invariant violation on exit"
    return i if i < n else -1
```

**Verification**:
- Debug run: Asserts/log traces each iter; inject `arr[0] = target` mid-loop → raises on next head.
- Optimized (`-O`): No overhead; equivalent to unchecked.
- Ties to M05C01: Head assert verifies preservation; tail confirms consequence.

Pythonic: `__debug__` std; logging for traces.

---

## 4. Canonical Example 2 – Recursive IH Check: Array Sum

From M05C02: IH for $m < n$: $sum_rec(arr,m) = \sum arr[0:m]$.

Code with encoded checks:
```python
import logging

# Configure at entrypoint: logging.basicConfig(level=logging.DEBUG if __debug__ else logging.INFO)

def sum_rec(arr: list[int], n: int) -> int:
    # Pre: 0 <= n <= len(arr); Post: res = sum(arr[0:n])
    if n == 0:
        if __debug__:
            assert sum(arr[:0]) == 0, "Base postcondition violation"
        return 0
    # IH check: recursive on m = n-1 < n
    sub = sum_rec(arr, n-1)
    if __debug__:
        # Snapshot pre-recursion V = n
        assert 0 <= n-1 < n <= len(arr), "IH Pre violation"
        # Post-recursion: assert IH Post for m=n-1
        assert sub == sum(arr[:n-1]), "IH violation: sub not prefix sum"
        logging.debug(f"Recursion return: sub={sub} for n-1={n-1}")
    res = arr[n-1] + sub
    if __debug__:
        assert res == sum(arr[:n]), "Step Post violation"
    return res
```

**Verification**:
- Debug: Asserts IH Pre/Post per call; inject wrong arr → raises on assert.
- Optimized: No overhead.
- Ties to M05C02: Entry assert IH Pre; return assert IH Post; composes with contracts (M05C03).

Pythonic: Recursion-friendly; logging hierarchies via indent.

---

## 5. Canonical Example 3 – Variant Check: Iterative Fibonacci

From M05C04: Variant $V = n - i$; decreases by 1 each iter.

Code with encoded variant check:
```python
def fib_iter(n: int) -> int:
    # Pre: n >= 0; Post: res = F_n
    # Term: V = n - i; decreases on i +=1
    if n == 0:
        return 0
    a, b = 0, 1
    i = 1
    while i < n:
        if __debug__:
            V_pre = n - i
            assert V_pre > 0, "Variant must be positive under guard"
        a, b = b, a + b
        i += 1
        if __debug__:
            V_post = n - i
            assert V_post < V_pre, "Variant did not decrease"
    return b
```

**Verification**:
- Debug: Positivity under guard; decrease post-body; inject `i -= 1` → raises on assert.
- Optimized: No overhead.
- Ties to M05C04: Explicit V_pre/post snapshots; reinforces scalar variant.

Pythonic: Simple temps for snapshots; no logging needed for variant.

---

## 6. Quick Reference – Patterns

| Element      | Check Point                    | Encoding Example             | Mode Guard                   |
|--------------|--------------------------------|------------------------------|------------------------------|
| Loop Inv     | Head (pre-body)                | `if __debug__: assert I`     | `__debug__`                  |
| Loop Var     | Post-body                      | `assert V_post < V_pre`      | `__debug__`                  |
| Rec IH       | Entry/exit                     | `assert Pre_sub; ... assert Post_sub` | `__debug__`                  |
| DS Inv       | `__post_init__`/post-mut       | `assert 0 <= len <= cap`     | `__debug__`                  |
| Prop Access  | Property body                  | `assert I on read`           | `__debug__`                  |

**Note**: Log with `logging.debug(f"Inv: {I}")` for traces (configure at entrypoint); env `DEBUG=True` for extras. Heavy checks (e.g., full forall) in tests, not runtime. Properties: Avoid O(n) Inv in hot paths.

---

## 7. Robustness – Runtime Checks in Practice

- **Overhead**: `__debug__` guards zero-cost in `-O`; logging configurable (DEBUG level off in prod).
- **False negatives**: Approximate checks (e.g., sample forall); full in tests (M05C07).
- **Exceptions**: AssertionError for Inv; ValueError for Pre (M05C03).
- **Composition**: Check at boundaries; chain Inv across calls.
- **Testing**: Mutate state mid-proof; verify raises (Hypothesis shrink).

**Example**: BST insert: Assert height/balance post-rot (debug only).

---

## 8. Permanent Habit

Embed checks:

```python
def linear_search(arr: list[int], target: int) -> int:
    n = len(arr)
    i = 0
    # Inv: 0 <= i <= n and all(arr[j] != target for j in range(i))
    while i < n and arr[i] != target:
        if __debug__:
            assert 0 <= i <= n and all(arr[j] != target for j in range(i))
        i += 1
    if __debug__:
        assert 0 <= i <= n and all(arr[j] != target for j in range(i))
    return i if i < n else -1
```

Prove Inv first (M05C01); add checks second; test violations.

---

## 9. What You Must Carry Forward

1. Embed $I/V$ as `__debug__` asserts at boundaries.
2. Fixed: Head/post-body for loops; entry/exit for recursion.
3. Workflow: Prove → identify points → encode guarded → test.
4. Patterns: Inv head for preservation; Var post for decrease.
5. Python: `__debug__` for zero-opt-cost; log traces.

## 10. Progress Note & What’s Next in M05

After M05C05, invariants live in code as debug checks, closing proof-to-practice loop.

M05C05 complete.

Next: **M05C06 – Hypothesis: strategies, shrinking, stateful tests**: Automated invariant falsification.

---

## 11. Glossary & Notation

- $I$: Invariant – preserved predicate (M05C01–C02).
- $V$: Variant – decreasing measure (M05C04).
- `__debug__`: True unless `python -O`; guards runtime checks.
- AssertionError: Raised on Inv violation (fail-fast).
- Logging: `logging.debug` for traces (DEBUG level).
# M05C06 · Hypothesis: Strategies, Shrinking, Stateful Tests – Automated Invariant Falsification

**Goal.** This core introduces property-based testing with Hypothesis to systematically generate inputs that falsify invariants and contracts (M05C01–C03), uncovering edge cases beyond manual tests. Upon completion, practitioners will define strategies for data generation, leverage shrinking for minimal counterexamples, and use stateful testing for data structures—transforming proofs into resilient, bug-resistant code through automated exploration.

**Scope** (explicit delimiters):
- Deterministic properties/invariants on finite inputs (e.g., DS ops, algorithms).
- Hypothesis library (pip install hypothesis); focuses on strategies, shrinking, stateful.
- Python 3.10+; stdlib integration (typing, unittest); excludes coverage tools.
- Falsification: Break naive Inv/$Pre/$Post$; assumes proofs (M05C01–C03) guide properties.
- Excludes non-deterministic or probabilistic testing (M10/M18).

Within this scope, Hypothesis heuristically explores input spaces to find violations, aligning with Pythonic practices (unittest, Hypothesis docs).

---

## 1. Core Definitions

**Property-based testing**: Specify properties (e.g., "reverse(reverse(x)) == x"); generate inputs to falsify via random/structured search.

**Strategy**: Generator for test cases (e.g., `st.integers(0, 100)` for bounded ints; composable via `flatmap`, `filter`).

**Shrinking**: From failing input, minimize to smallest counterexample (e.g., large list → len=1 violating case) using heuristics.

**Stateful testing**: Model DS as state machine; initial state + rules (mutators/observers); property: Inv holds after each rule.

**Falsification**: Hypothesis finds violating input; shrinking reveals root cause; no formal coverage guarantee (heuristic, biased toward simple/extreme values).

No theorem: Hypothesis provides empirical confidence, not exhaustive search; effectiveness depends on strategy design and property clarity.

Extends M05C05 checks: Manual asserts reactive; Hypothesis proactive (searches for breaks, complements proofs M05C01–C03).

---

## 2. Mechanical Derivation Workflow

For property from proved Inv/$Pre/$Post$:

1. Define property: Bool fn on inputs (e.g., `def prop_reverse(x): return reverse(reverse(x)) == x`); tie to spec (e.g., IH from M05C02).
2. Strategy: `@given` with primitives (e.g., `given(st.lists(st.integers(0, 100)))`); bound size (`max_size=100`). For complex dependencies, use `st.data()`.
3. Test fn: `def test_prop(xs): assume(Pre(xs)); assert property(xs)`.
4. Run: `pytest --hypothesis-show-statistics`; inspect failures/shrinks.
5. Stateful: `class StateMachine(RuleBasedStateMachine): @rule def push(self, x): ...; @invariant def inv(self): assert Inv()`.
6. Refine: Prefer building strategies that only generate valid inputs; use `filter(Pre)` or `assume(Pre)` for valid space when that is awkward; increase `max_examples=1000`.
7. Verify: Shrunk examples as manual tests; repro with `--hypothesis-seed=123`.

**Heuristic**: Start scalar (`integers`); scale to DS (`lists`, `dictionaries`); use `st.data()` only for dependent gen.

---

## 3. Canonical Example 1 – Falsifying List Reversal Invariant

From M05C02: Invariant for reversal IH: Preserves length; double reversal idempotent (Post: reverse(reverse(lst)) = lst).

Buggy impl: Off-by-one drops first element.

Strategy: Bounded lists of ints (min_size=0 to demonstrate assume).

Code:
```python
from hypothesis import given, assume, settings
from hypothesis.strategies import lists, integers

def buggy_reverse(xs):
    return xs[1:][::-1]  # Bug: drops xs[0]

@given(lists(integers(-100, 100), min_size=0, max_size=10))
@settings(max_examples=100)
def test_reverse_length(xs):
    # Pre: non-empty (from M05C02 finite lst)
    assume(len(xs) > 0)
    rev = buggy_reverse(xs)
    # Property: len(rev) == len(xs) (encodes length preservation Inv)
    assert len(rev) == len(xs)

@given(lists(integers(-100, 100), min_size=1, max_size=10))
@settings(max_examples=100)
def test_reverse_idempotent(xs):
    # Pre: non-empty enforced by min_size=1
    rev = buggy_reverse(xs)
    # Property: buggy_reverse(rev) == xs (encodes IH: reverse preserves structure)
    assert buggy_reverse(rev) == xs

# Run: pytest -v --hypothesis-show-statistics
# Falsifies test_reverse_length: e.g., xs=[1] → rev=[] (len=0 !=1); shrinks to [1]
# Falsifies test_reverse_idempotent: e.g., xs=[1,2] → rev=[1] → buggy_reverse(rev)=[] != [1,2]; shrinks to [1,2]
```

**Verification**:
- Generates random xs; falsifies length mismatch (shrinks to minimal non-empty [1]); idempotence fails on double drop (shrinks to two-element).
- Ties to M05C02: Properties encode IH "reverse on proper subs"; shrunk [1] exposes base-case drop, revealing proof gap in step (decomposition assumes full cons).

Pythonic: `@given` declarative; separate tests isolate properties for clearer shrinking.

---

## 4. Canonical Example 2 – Stateful Stack Testing

From M05C03: Stack contracts – push appends to end (Post: new_stack = old + [elem]); pop returns/ removes top if non-empty (Pre: len>0; Post: elem = old[-1]).

Buggy impl: Pop removes from front (FIFO-like, LIFO violation).

Strategy: Initial empty; rules push/pop on impl and model (reference list); invariant compares states.

Code:
```python
from hypothesis.stateful import RuleBasedStateMachine, rule, initialize, invariant
from hypothesis.strategies import integers

class BuggyStack:
    def __init__(self):
        self._data = []
    
    def push(self, elem):
        self._data.append(elem)
    
    def pop(self):
        if not self._data:
            raise IndexError("pop from empty")
        # Bug: removes from front (FIFO-like), not top (LIFO)
        if len(self._data) == 1:
            return self._data.pop()
        return self._data.pop(0)  # Wrong: removes from front

class StackMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.model = []  # Reference impl
        self.impl = BuggyStack()
    
    @initialize()
    def init(self):
        self.model = []
        self.impl = BuggyStack()
    
    @rule(x=integers(-100, 100))
    def push(self, x):
        self.model.append(x)
        self.impl.push(x)
    
    @rule()
    def pop(self):
        if self.model:
            expected = self.model.pop()
            actual = self.impl.pop()
            assert actual == expected, f"LIFO violation: expected {expected}, got {actual}"
    
    @invariant()
    def states_match(self):
        # Inv: impl._data == model (encodes Post preservation across ops)
        assert self.impl._data == self.model

StackTest = StackMachine.TestCase

# Run: pytest test_stack.py -v --hypothesis-show-statistics
# Falsifies pop rule: e.g., seq push(1), push(2), pop() → actual=1 !=2; shrinks to push(1), push(2), pop()
```

**Verification**:
- Generates push/pop sequences; falsifies LIFO on pop (shrinks to minimal two-push, one-pop); invariant catches state divergence earlier.
- Ties to M05C03: Rules encode mutators; @invariant enforces DS Inv ("stack contents preserved"); shrunk seq exposes Pre/Post gap (pop assumes top removal).

Pythonic: Model/impl separation; @rule for transitions.

---

## 5. Canonical Example 3 – Shrinking Binary Search Invariant Violation

From M05C01: Invariant $I$: $L0 \le low \le high \le H0 \land \forall j \in [L0, low): arr[j] < target \land \forall j \in [high, H0): arr[j] \ge target$. Post: $low$ is insertion point ($0 \le low \le n \land (low=0 \lor arr[low-1] < target) \land (low=n \lor arr[low] \ge target)$).

Buggy impl: Uses `<=` in branch (shifts to right-insertion for equals, skipping existing targets).

Strategy: Sorted lists and arbitrary target (jointly generated).

Code:
```python
from hypothesis import given
from hypothesis.strategies import lists, integers

def buggy_binary_search(arr, target):
    low, high = 0, len(arr)
    while low < high:
        mid = (low + high) // 2
        if arr[mid] <= target:  # Bug: <= instead of < (bisect_right behavior)
            low = mid + 1
        else:
            high = mid
    return low

@given(
    lists(integers(-100, 100), min_size=1, max_size=20).map(sorted),
    integers(-101, 101)
)
def test_binary_search_post_invariant(arr, target):
    # Pre: arr sorted (enforced by .map(sorted))
    idx = buggy_binary_search(arr, target)
    # Property: Post Inv holds (encodes consequence from M05C01)
    assert 0 <= idx <= len(arr)
    assert idx == 0 or arr[idx-1] < target
    assert idx == len(arr) or arr[idx] >= target

# Run: pytest -v --hypothesis-show-statistics
# Falsifies: e.g., arr=[1], target=1 → idx=1 (skips existing); postcondition fails because arr[idx-1] < target is false
```

**Verification**:
- Generates sorted arr/target pairs; falsifies insertion for existing target (shrinks to minimal [x], target=x); returns len(arr) instead of position.
- Ties to M05C01: Property encodes proved Post ($I \land \neg G \implies Q$); shrunk case reveals preservation fail (branch assumes strict < for leftmost). Note: This bug yields a valid alternative spec (right insertion); Hypothesis enforces consistency with the chosen one.

Pythonic: Joint @given for correlated args; .map for Pre.

---

## 6. Quick Reference – Patterns

| Property Type | Strategy Example               | Shrinking Benefit            | Stateful Twist               |
|---------------|--------------------------------|------------------------------|------------------------------|
| Inv Falsify   | `given(lists(integers()))`     | Minimal violating input      | Rules mutate model/impl; assert match |
| Contract Break| `given(integers(0,100))`       | Smallest n failing Pre/Post  | Initial + mutators; Inv each step |
| DS Inv        | `given(lists(integers()))`     | Edge case seq (len=1)        | @invariant for global holds |
| Rec IH        | `given(integers(min_value=0))` | Small n exposing IH fail     | Mock recursion with loops    |

**Note**: max_size bounds gen; `settings(max_examples=1000)` for coverage. Excludes: Known cases via `assume`/`filter`. Generation biased toward simple/extreme; no formal coverage.

---

## 7. Robustness – Hypothesis in Practice

- **Overhead**: Gen/shrinking cost depends on strategy complexity and failure patterns; measure with pytest timings if it matters.
- **False positives**: Common from wrong properties or missed Pre; use `assume(Pre(x))` judiciously (over-filter slows).
- **Stateful limits**: Stateful runs can be costly; bound the number of steps per run (e.g., `max_examples`, `stateful_step_count`) and keep per-step work small.
- **Integration**: pytest plugin; seed for repro (`--hypothesis-seed=123`).
- **Testing**: Cover proved Inv; manual on shrunk fails; main risk is property mis-spec, not generation.

**Example**: Quicksort Inv: `@given(lists(integers()))` assert sorted(output).

---

## 8. Permanent Habit

Define properties:

```python
from hypothesis import given, assume
from hypothesis.strategies import lists, integers

@given(lists(integers(-100, 100), max_size=100))
def test_reverse_invariant(xs):
    # Property from M05C02 IH
    assume(len(xs) > 0)  # Pre: non-empty
    rev = xs[::-1]  # replace with your impl under test
    assert len(rev) == len(xs)
    assert rev[::-1] == xs  # Falsify if impl buggy
```

Prove spec (M05C01–C03) → property → gen strategy → run/shrink.

---

## 9. What You Must Carry Forward

1. Properties encode proved Inv/$Pre/$Post$.
2. `@given` strategies for inputs; shrinking for mins.
3. Stateful: Rules mutate; assert post-rule Inv.
4. Workflow: Spec → property → gen → falsify/shrink.
5. Patterns: Lists/integers base; joint args for deps.

## 10. Progress Note & What’s Next in M05

After M05C06, automate Inv falsification, completing proofs-to-tests pipeline.

M05C06 complete.

Next: **M05C07 – Using property tests to break naive invariants and corner cases**: Advanced Hypothesis.

---

## 11. Glossary & Notation

- Property: Bool fn falsified by gen inputs.
- Strategy: Generator (e.g., `st.lists(...)`).
- Shrinking: Minimize failing input.
- Stateful: State machine with rules/mutators.
- `@given`: Hypothesis decorator for tests.
# M05C07 · Using Property Tests to Break Naive Invariants and Corner Cases

**Goal.** This core demonstrates how to use Hypothesis to expose defects in naive implementations that violate the assumptions underlying invariant proofs (M05C01–C03). These bugs often survive broad property tests (M05C06) but emerge under edge cases targeting specific proof hypotheses. Practitioners will learn to identify vulnerable assumptions in derivations, construct input strategies to reach critical states, and interpret shrunk counterexamples—integrating empirical testing with formal reasoning to ensure code adheres to proof logic.

**Scope** (explicit delimiters):
- Focus: Falsifying proof assumptions like guard conditions, index safety, and loop progress guarantees.
- Techniques: Targeted Hypothesis strategies (composition, flatmap, bounded constructors); minimal assume; no global filters.
- Hypothesis nature: Pseudo-random generation with strategies biased toward edge shapes; no exhaustive or deterministic guarantees.
- Python 3.10+; Hypothesis with pytest; examples refer back to invariants and hypotheses from M05C01, using minimally defective implementations that pass typical inputs.
- Assumes M05C06; focuses on “passes broad tests, fails a specific assumption” (e.g., off-by-one guard causing an out-of-bounds access).
- Excludes nondeterministic behavior, performance characteristics, concurrency, and properties unrelated to invariants/contracts.

Within this scope, Hypothesis is used to stress the specific states required by the proof assumptions, complemented by M05C05 monitors for diagnostics.

---

## 1. Core Definitions

**Proof hypothesis**: Assumption enabling an Inv step (e.g., "i < n before arr[i]" in preservation).

**Hypothesis violation**: Input satisfying typical Inv but breaching the assumption (e.g., i = n under loose guard).

**Shrunk counterexample**: Reduced input isolating the breach (e.g., len=1 array triggering boundary access).

**Targeted strategy**: Structured generator biased toward critical shapes (e.g., absent-target arrays forcing full scan), constructed to avoid heavy use of filter and large discard rates.

No theorem: Shrinking provides concise failures heuristically; it augments proofs by revealing misalignments, not exhaustive verification.

Extends M05C06: Shifts from broad properties to assumption-targeted probes; naive bugs evade general runs but surface under shaped inputs, clarifying where the implementation diverges from the proof’s assumptions.

---

## 2. Mechanical Derivation Workflow

For a naive implementation tied to a quoted Inv from M05C01:

1. Identify the proof clause: Quote the hypothesis (e.g., M05C01 preservation: "Assume I ∧ i < n; i += 1 maintains bounds").
2. Locate or hypothesize a minimal defect: a change that violates the assumption while leaving typical behavior intact (e.g., i <= n instead of i < n, allowing arr[n] access).
3. Define the probing property: Check the clause under edge conditions (e.g., "full scan without IndexError").
4. Build a targeted strategy: Use flatmap to correlate elements inducing the violation (e.g., absent target yielding i = n).
5. Add monitoring: Instrument with M05C05 asserts for clause checks or use try/except for exceptions.
6. Run falsification: `pytest --hypothesis-show-statistics`; map shrunk input to the hypothesis.
7. Remediate: Fix defect; re-derive Inv; re-run probe.

**Heuristic**: One hypothesis per test; strategies bias toward the critical state; interpret shrinks against proof phrasing.

---

## 3. Canonical Example 1 – Linear Search: Guard Condition Violated

Proof hypothesis (M05C01).  
Preservation assumes i < n so arr[i] is defined.

Naive defect.  
Use i <= n, allowing arr[n] evaluation for absent targets.

Targeted strategy.  
Generate arrays guaranteed not to contain the target, forcing i to reach n.

Code:
```python
from hypothesis import given
from hypothesis.strategies import integers, lists, just, one_of

def buggy_linear_search(arr, target):
    n = len(arr)
    i = 0
    while i <= n and arr[i] != target:  # off-by-one bug
        i += 1
    return i if i < n else -1

def absent_target_strategy():
    return integers(-10, 10).flatmap(
        lambda target: lists(
            one_of(just(target - 1), just(target + 1)),  # values != target
            min_size=1, max_size=5
        ).map(lambda arr: (arr, target))
    )

@given(absent_target_strategy())
def test_linear_search_guard_hypothesis(arr_target):
    arr, target = arr_target
    # Proof-level property: full scan must not index arr[n]
    try:
        idx = buggy_linear_search(arr, target)
        assert idx == -1
    except IndexError:
        # Hypothesis violation exposed
        assert False, "Guard hypothesis violated: accessed arr[n]"
```

Interpretation.  
Hypothesis shrinks the failing case to the smallest array where the violation occurs (e.g., arr=[x], target≠x).  
This directly falsifies the proof assumption “i < n before access”.

---

## 4. Canonical Example 2 – Binary Search: Progress Assumption Violated

Proof hypothesis (M05C01).  
On the < branch:  
If arr[mid] < target, then low' = mid + 1 (ensures progress: low' > mid).

Naive defect.  
Use low = mid, which stalls on plateaus.

Targeted strategy.  
Generate arrays where all elements are the same value < target, forcing repeated < branches.

Code:
```python
from hypothesis import given, settings
from hypothesis.strategies import integers, lists, just
from typing import List

def buggy_binary_search(arr: List[int], target: int) -> int:
    low, high = 0, len(arr)
    steps = 0
    while low < high:
        steps += 1
        if steps > len(arr) + 10:  # fuel limit
            raise RuntimeError("Non-terminating: progress hypothesis violated")
        mid = (low + high) // 2
        if arr[mid] < target:
            low = mid  # defect: no +1
        else:
            high = mid
    return low

def plateau_strategy():
    return integers(2, 5).flatmap(
        lambda n: integers(-10, 10).flatmap(
            lambda v: lists(just(v), exact_length=n).map(lambda arr: (arr, v + 1))
        )
    )

@settings(deadline=None)
@given(plateau_strategy())
def test_binary_search_progress_hypothesis(arr_target):
    arr, target = arr_target
    try:
        idx = buggy_binary_search(arr, target)
        assert idx == len(arr)
    except RuntimeError:
        assert False, "Progress hypothesis violated: low failed to advance"
```

Interpretation.  
On a plateau, the proof requires strict movement.  
The faulty implementation stalls (low = mid).  
Fuel-based detection captures the invariant violation precisely.

---

## 5. Quick Reference – Patterns

| Hypothesis Type | Targeted Strategy Example       | Probing Property Example          | Shrink Outcome                    |
|-----------------|---------------------------------|-----------------------------------|-----------------------------------|
| Guard Safety    | flatmap(absent target)          | No IndexError on full scan        | Len=1 absent target               |
| Branch Progress | flatmap(plateau < target)       | Advance to end without stall      | Len=2 plateau                     |

**Note**: Align strategy to critical state; `max_examples=500`; fuel for potential non-termination; map shrink to assumption.

---

## 6. Robustness – Hypothesis Falsification in Practice

- **Heuristic nature**: Strategies bias toward edges; Hypothesis explores pseudo-randomly within shapes—use seeds for repro.
- **Non-termination**: Fuel counters raise explicit failures (RuntimeError) for stalls.
- **Alignment**: Properties reflect proof clauses; exceptions signal violations directly.
- **Diagnostics**: M05C05 for state traces; pytest reruns on shrinks.
- **Limits**: Targets assumptions, not totality; complement with proofs.

**Example**: Partition: flatmap(pivot equals all) probes symmetry assumption.

---

## 7. Permanent Habit

Target assumptions:

```python
from hypothesis import given
from hypothesis.strategies import integers, lists, just, one_of

@given(integers(-10,10).flatmap(lambda target: lists(one_of(just(target-1), just(target+1)), min_size=1).map(lambda arr: (arr, target))))
def test_guard(arr_target):
    arr, target = arr_target
    # M05C01 assumption: i < n before arr[i]
    try:
        idx = linear_search(arr, target)
        assert idx == -1
    except IndexError:
        assert False, "Assumption violated: accessed arr[n]"
```

Derive → identify assumption → minimal defect → targeted probe → falsify/shrink/remediate.

---

## 8. What You Must Carry Forward

1. Identify proof clauses as test targets.
2. Strategies narrow and structural, not random.
3. Shrunk counterexamples map to violated assumptions.
4. Runtime monitors check implementation state.
5. Goal: proof-code alignment, not test volume.

## 9. Progress Note & What’s Next in M05

After M05C07, targeted tests fortify code against proof assumptions.

M05C07 complete.

Next: **M05C08 – 8. Proof sketch for binary search or partition correctness.**: Applied derivation.

---

## 10. Glossary & Notation

- Proof hypothesis: Step assumption (e.g., "i < n safe").
- Hypothesis violation: Input breaching assumption.
- Targeted strategy: Biased generator for critical shapes.
- Shrunk counterexample: Minimal breach isolator.
# M05C08 · Proof Sketch for Partition Correctness – Verifying Quicksort's Core Primitive

**Goal.** This core furnishes a rigorous proof sketch for the partition algorithm underpinning quicksort, deriving invariants and variants to establish correctness and termination. Upon completion, practitioners will mechanically verify partition's postcondition (elements $< p$ left, $\ge p$ right) while preserving bounds, composing with selection invariants (M05C01–C02) for full quicksort proofs—bridging deterministic partitioning to randomized pivots (M10) and empirical validation (M05C06–C07).

**Scope** (explicit delimiters):
- Deterministic partition on finite arrays; Lomuto or Hoare scheme.
- Invariants over indices and subarray properties; variants for termination.
- Partial/total correctness via Hoare triples; assumes sortedness not required pre-partition.
- Excludes randomization (M10), concurrency (M18), or multi-pivot variants.
- Pythonic: In-place mutation; focuses on simple $< p$ / $\ge p$ partition; duplicate handling and 3-way schemes treated separately.

Within this scope, the workflow certifies partition as a reusable primitive, aligning with stdlib `sorted` internals and quicksort derivations.

---

## 1. Core Definitions

Partition rearranges `arr[L:R)` around pivot $p = arr[R-1]$ (Lomuto): All $j < i$ satisfy $arr[j] < p$; all $j \ge i$ satisfy $arr[j] \ge p$; returns split index $i$.

**Precondition $Pre(L, R, arr)$**: $0 \le L < R \le n = \text{len}(arr)$; pivot at $arr[R-1]$.

**Postcondition $Post(L, R, i, arr)$**: $L \le i < R \land \forall j \in [L, i): arr[j] < arr[i] \land \forall j \in [i, R): arr[j] \ge arr[i]$.

**Hoare triple**: $\{Pre\} \ partition(arr, L, R) \ \{Post\}$.

**Invariant $I$** (scheme-specific; see Examples): Predicate over loop indices and regions ensuring prefix/suffix properties.

**Variant $V$**: Non-negative integer strictly decreasing per iteration (e.g., unprocessed span).

**Theorem** (partition correctness): If $Pre \Rightarrow I$ (initialisation), $I \land G \Rightarrow \{B\} I$ (preservation), $I \land \neg G \Rightarrow Post$ (consequence), and $V \ge 0$ under $I \land G$ with strict decrease post-$B$ in $\mathbb{N}$, then the loop establishes $\{Pre\} \ partition \ \{Post\}$ with termination (total correctness).

Extends M05C01 scans: Prefix for left, suffix for right; composes with recursion (M05C02) for quicksort.

---

## 2. Mechanical Derivation Workflow

For `partition(arr, L, R)` (Lomuto: `i = L; j = L; while j < R-1: if arr[j] < p: swap(arr[i], arr[j]); i += 1; j += 1; swap(arr[i], arr[R-1]); return i`):

1. Specify $Pre$, $Post$ (bounds, left $< p$, right $\ge p$).
2. Initialise: Set `i = L`, `j = L`; derive $I$: Left prefix $< p$ (vacuous), scanned middle $\ge p$ (vacuous).
3. Preservation: Assume $I \land j < R-1$; post-body ($B$ + $j += 1$), show new $I$ (cases: swap extends left, increments boundary; skip extends middle).
4. Consequence: $\neg G$ ($j \ge R-1$) $\land I \Rightarrow$ pre-final properties; final swap yields $Post$.
5. Variant: $V = R - 1 - j \in \mathbb{N}$; decreases by $1$ on $j += 1$.
6. Verify: Simulate edges (length $1$, all $< p$, all $\ge p$); tie to quicksort recursion.

**Heuristic**: $I$ = "left prefix $< p$ + scanned middle $\ge p$ + unprocessed suffix"; test $0/1$ iterations.

---

## 3. Canonical Example 1 – Lomuto Partition: Invariant Derivation

$Pre$: $0 \le L < R \le n$; $p = arr[R-1]$.

$Post$: $L \le i < R \land \forall j \in [L,i): arr[j] < p \land \forall j \in [i,R): arr[j] \ge p$ (equivalent to general $Post$ since $arr[i] = p$ at exit).

Code (Pythonic `for` syntactic sugar; proof on explicit `while`):
```python
def lomuto_partition(arr: list[int], L: int, R: int) -> int:
    # Pre: 0 <= L < R <= len(arr); pivot p = arr[R-1]
    # Post: L <= i < R /\ forall j in [L,i): arr[j] < p /\
    #       forall j in [i,R): arr[j] >= p
    p = arr[R-1]
    i = L
    j = L
    while j < R - 1:
        # Invariant (at loop top, before if):
        # L <= i <= j <= R-1 /\
        # forall k in [L, i): arr[k] < p /\
        # forall k in [i, j): arr[k] >= p /\
        # arr[R-1] = p
        if arr[j] < p:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
        j += 1
    # Exit: j >= R-1, invariant holds for all scanned j < R-1
    # (L <= i <= R-1 and forall k in [L, i): arr[k] < p,
    #  forall k in [i, R-1): arr[k] >= p)
    arr[i], arr[R - 1] = arr[R - 1], arr[i]
    # Now: arr[i] == p; forall k in [L, i): arr[k] < p;
    #      forall k in [i + 1, R): arr[k] >= p
    return i
```

**Hoare Triple**: $\{Pre\} \ partition \ \{Post\}$.

**Invariant $I$** (at loop top, before `if` for current $j$; after prior $j += 1$):  
$L \le i \le j \le R-1 \land \forall k \in [L,i): arr[k] < p \land \forall k \in [i,j): arr[k] \ge p \land arr[R-1] = p$.

- **Initialisation** ($j = L$): $i = L$, $j = L$; intervals $[L,L) = \emptyset$ (vacuous $\forall$); $arr[R-1] = p$; $I$ holds.
- **Preservation**: Assume $I \land j < R-1$. Post-body ($B$ + $j += 1$):  
  - **Case $arr[j] < p$**:  
    - **Subcase $i = j$**: Swap $arr[i]$ and $arr[j]$ is no-op ($arr[j] < p$). Then $i += 1$: New left $[L,i') = [L,j+1)$, all $< p$ (old $[L,j) < p$ by left + middle up to $j-1$, $arr[j] < p$). New middle $[i',j') = [i+1,j+1) = \emptyset$ (vacuous $\ge p$).  
    - **Subcase $i < j$**: By $I$, $arr[i] \in [i,j) \Rightarrow arr[i] \ge p$. Swap: $arr[i] \gets arr[j] < p$, $arr[j] \gets arr[i] \ge p$. Then $i += 1$: New left $[L,i') = [L,i+1)$ is old left ($< p$) + new $arr[i] < p$. New middle $[i',j) = [i+1,j)$ is old middle subset ($\ge p$).  
  - **Case $arr[j] \ge p$**: No swap; $j += 1$: New middle $[i,j') = [i,j+1)$ is old middle ($\ge p$) + $arr[j] \ge p$. Left unchanged.  
  In all subcases, $I$ holds at next loop top.
- **Consequence**: Loop exit ($j \ge R-1$): $I$ yields $\forall k \in [L,i): arr[k] < p \land \forall k \in [i,R-1): arr[k] \ge p \land arr[R-1] = p$. Final swap: $arr[i] \leftrightarrow arr[R-1]$ ($arr[i]$ was $\ge p$ from $[i,R-1)$). Post-swap: $arr[i] = p \ge p$; old $arr[i] \ge p$ now at $R-1 \in [i+1,R)$ (old $[i+1,R-1) \ge p$). Thus $\forall k \in [i,R): arr[k] \ge p$; left unchanged ($< p$).
- **Variant**: $V = R - 1 - j \in \mathbb{N}$. Under $G$ ($j < R-1$): $V > 0$. Post-body: $j' = j+1$, $V' = V - 1 < V$. Well-founded: $\ge 0$, $\le R-L-1$ steps.

**Remark on Stability**: Lomuto preserves relative order among $< p$ elements (discovered sequentially via $j$, swapped in order to left). Elements $\ge p$ may reorder due to swaps with $< p$ (unstable overall, as expected for quicksort).

---

## 4. Canonical Example 2 – Hoare Partition: Dual Pointers

Alternative: Two pointers from ends; fewer swaps, possible crossover.

$Pre$, $Post$ as above.

Code:
```python
def hoare_partition(arr: list[int], L: int, R: int) -> int:
    p = arr[R-1]
    lo = L
    hi = R - 2
    while lo <= hi:  # G: lo <= hi
        # Skip left < p
        while lo <= hi and arr[lo] < p: lo += 1
        # Skip right >= p
        while lo <= hi and arr[hi] >= p: hi -= 1
        if lo <= hi:
            arr[lo], arr[hi] = arr[hi], arr[lo]
            lo += 1
            hi -= 1
    return lo  # Split at lo: [L,lo) < p, [lo,R) >= p
```

**Invariant $I$** (post-inner skips, pre-swap decision):  
$L \le lo \le R \land L \le hi \le R-1 \land (lo > hi \lor (arr[lo] \ge p \land arr[hi] < p)) \land \forall k \in [L, lo): arr[k] < p \land \forall k \in [hi+1, R-1): arr[k] \ge p \land arr[R-1] = p$.

- **Initialisation**: $lo = L$, $hi = R-2$; skips adjust to first violations (or cross); vacuous if empty.
- **Preservation** (sketch): Inner skips extend clean left/right ($\forall$ hold by induction on advances). If $lo > hi$: Done. Else swap violations ($arr[lo] \ge p \leftrightarrow arr[hi] < p$): Post-swap, $arr[lo] < p$, $arr[hi] \ge p$; increments: $lo +=1$ (past new $< p$), $hi -=1$ (past new $\ge p$). New cleans: Left to new $lo$ ($< p$ by old + swapped), right from new $hi+1$ ($\ge p$ by old + swapped).
- **Consequence**: Exit ($lo > hi$): $[L, lo) < p$ (full left clean), $[hi+1, R) \ge p$ (full right clean + $p$); empty middle.
- **Variant**: $V = hi - lo + 1 \in \mathbb{N}$. Under $G$: $V > 0$. Skips preserve $V$; post-swap/increments: $V' = V - 2 < V$.

Fewer swaps than Lomuto; crossover avoids final swap.

---

## 5. Canonical Example 3 – Composition with Quicksort Recursion

Full quicksort: Partition, recurse left $[L,i)$, right $[i+1,R)$.

From M05C02: IH for smaller subarrays: Sorted.

**Termination**: Lex variant $(R-L, 1)$; partition linear, recurses on proper subintervals.

Code sketch:
```python
def quicksort_rec(arr: list[int], L: int, R: int) -> None:
    # Pre: 0 <= L < R <= len(arr)
    # Post: sorted(arr[L:R])
    if R - L <= 1: return  # Base
    i = lomuto_partition(arr, L, R)
    quicksort_rec(arr, L, i)  # |[L,i)| < R-L
    quicksort_rec(arr, i + 1, R)  # |[i+1,R)| < R-L
    # IH: subs sorted; Post: left all < arr[i] <= all right; concatenated sorted
```

**Proof Sketch**: Base trivial ($|S| \le 1$). IH: Assume for $m < R-L$, sorts subarray of length $m$. Step: Partition $Post \Rightarrow$ left all $< p \le$ all right ($p$ at $i$). IH sorts left/right; $p$ fits between, yielding sorted $[L,R)$.

---

## 6. Quick Reference – Patterns

| Scheme      | Invariant Sketch                                      | Variant                  | Notes                        |
|-------------|-------------------------------------------------------|--------------------------|------------------------------|
| Lomuto     | $[L,i) < p$; $[i,j) \ge p$ (scanned); $j$ scans      | $R-1 - j$                | Linear scans; relative $< p$ stable |
| Hoare      | $[L,lo) < p$; $[hi+1,R) \ge p$; $lo,hi$ violations   | $hi - lo + 1$            | Fewer swaps; crossover       |
| 3-Way      | $[L,lt) < p$; $[gt,R) > p$; $[lt,gt) = p$ (dups)     | Lex $(gt-lt, gt-lt)$     | Dutch flag; avoids $\Theta(n^2)$ |

**Note**: For dups, extend with equality band; lex variant for nested loops.

---

## 7. Robustness – Partition in Practice

- **Duplicates**: Simple scheme correct but $O(n^2)$ worst-case; 3-way mitigates via separate $=p$ region.
- **In-Place**: $O(1)$ space; $I$ tracks mutations.
- **Edges**: Length $1$ ($i=L$); all $< p$ ($i=R-1$, swap to end); all $\ge p$ ($i=L$).
- **Debug**: Assert $I$ mid-loop (M05C05); Hypothesis on random/particular arr (M05C06–C07).
- **Random Pivot**: Compose with M10: Expected $O(n \log n)$ via prob bounds.

**Example**: All $=p$: $i=L$, minimal movement.

---

## 8. Permanent Habit

Annotate partitions:

```python
def lomuto_partition(arr: list[int], L: int, R: int) -> int:
    # Pre: L < R; Post: split i with left < p, right >= p
    # Inv: [L,i) < p; [i,j) >= p; j scans (at loop top)
    # Var: R-1 - j decreases
    p = arr[R-1]
    i = L
    j = L
    while j < R - 1:
        if __debug__:
            assert all(arr[k] < p for k in range(L, i))  # Left clean
            assert all(arr[k] >= p for k in range(i, j))  # Scanned kept
        if arr[j] < p:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
        j += 1
    arr[i], arr[R-1] = arr[R-1], arr[i]
    if __debug__:
        assert L <= i < R
        assert all(arr[k] < arr[i] for k in range(L, i))  # p now at i
        assert all(arr[k] >= arr[i] for k in range(i, R))
    return i
```

Derive $I/V$ before code; simulate; probe with Hypothesis (all $<p$, dups).

---

## 9. What You Must Carry Forward

1. Partition $Post$: Left $< p$, right $\ge p$, bounds.
2. $I$: Left clean + scanned middle $\ge p$ + unprocessed.
3. $V$: Unprocessed span decreases ($1$ or $2$).
4. Workflow: $Pre/Post \to I$ (regions) $\to$ cases $\to V$.
5. Patterns: Lomuto simplicity; Hoare efficiency; 3-way dups.
6. Compose: With recursion for quicksort total.

## 10. Progress Note & What’s Next in M05

After M05C08, partition proofs enable verified quicksort, synthesizing loop/recursion proofs.

M05C08 complete.

Next: **M05C09 – Spec + proof sketch for a simple DS (stack/queue)**.

---

## 11. Glossary & Notation

- $Pre$: Precondition – bounds and pivot position.
- $Post$: Postcondition – split with left $< p$, right $\ge p$.
- $I$: Invariant – left clean, scanned middle $\ge p$, unprocessed.
- $V$: Variant – unprocessed span, strict decrease.
- $\{P\} S \{Q\}$: Hoare triple for statement $S$.
- Lomuto/Hoare: Partition schemes (single/dual pointers).
- 3-Way: Extension for duplicates (Dutch national flag).
# M05C09 · Spec + Proof Sketch for a Simple DS

**Goal.** This core guides practitioners in deriving a complete specification, representation invariant, and proof sketch for a simple mutable data structure, such as a stack, by composing pre/postconditions (M05C03), invariants (M05C01–C02), termination arguments (M05C04), and runtime checks (M05C05). Upon completion, you will formulate Hoare triples for operations, prove preservation and termination, and embed assertions for validation—culminating in a verified module with targeted Hypothesis probes (M05C06–C07) to confirm fidelity to the spec.

**Scope** (explicit delimiters):
- Simple DS: Mutable stack with push/pop/size; finite, deterministic operations on type T.
- Full derivation: Abstract spec, RepInv, per-op triples, preservation/termination proofs.
- Python 3.10+; dataclasses/typing; no external libs.
- Assumes M05C01–C07; emphasizes composition (contracts + Inv + variant).
- Excludes advanced DS (M07), concurrency (M18), or probabilistic (M10).

Within this scope, the workflow yields a spec-complete stack, aligning with Pythonic practices (dataclasses, asserts) and bridging theory to implementable code.

---

## 1. Core Definitions

**Abstract spec**: Mathematical model (e.g., stack as sequence $S \in T^*$); Pre/Post for ops.

**Abstraction function Abs**: $\mathrm{Abs}(self) = \mathrm{tuple}(self.\_data)$ (maps concrete to abstract $S$).

**Representation Inv (RepInv)**: Predicate constraining concrete rep (e.g., the semantic structure of _data matches Abs); we additionally assume self._data is exclusively owned: no external code mutates it; all access goes through Stack methods.

**Hoare triple**: $\{\mathrm{Pre}\} \ op \ \{\mathrm{Post}\}$: If Pre $\wedge$ RepInv holds, op terminates with Post $\wedge$ RepInv (total via variant).

**DS proof**: Per-op triples + composition (Post$_1$ $\wedge$ RepInv $\Rightarrow$ Pre$_2$); preservation (Pre $\wedge$ RepInv $\Rightarrow$ RepInv post-body).

**Theorem** (DS total correctness): If each op satisfies $\{\mathrm{RepInv} \wedge \mathrm{Pre}\} \ op \ \{\mathrm{RepInv} \wedge \mathrm{Post}\}$ and variant decreases under Pre (trivial $V=0$ for push/size; $V = \mathrm{len}(S)$ decreasing by 1 for pop), then DS upholds $\mathrm{Abs}(self) = S$ across sequences.

Extends M05C03: RepInv as internal contract; composes M05C01 loops/M05C02 IH/M05C04 variants/M05C05 checks/M05C07 probes.

---

## 2. Mechanical Derivation Workflow

For stack DS with ops push($T$) $\to$ None, pop() $\to T$, size() $\to$ int:

1. Abstract spec: $S \in T^*$ (sequence); push(elem): Post $S' = S + [elem]$; pop: Pre $\mathrm{len}(S) > 0$, Post elem = $S[-1]$, $S' = S[:-1]$; size: Post res = $\mathrm{len}(S)$.
2. Concrete rep: @dataclass Stack[$T$]: _data: list[$T$] = field(default_factory=list).
3. RepInv: The semantic structure of _data matches Abs (e.g., prefix/top consistency via ops); we additionally assume self._data is exclusively owned: no external code mutates it; all access goes through Stack methods.
4. Per-op triple: Prove $\{\mathrm{RepInv} \wedge \mathrm{Pre}\} \ op \ \{\mathrm{RepInv} \wedge \mathrm{Post}\}$ via preservation (body maintains RepInv) and termination (variant $V = \mathrm{len}(\_data)$).
5. Composition: Post op $\wedge$ RepInv $\Rightarrow$ Pre next; global: init RepInv holds.
6. Embed checks: __debug__ assert RepInv pre/post; M05C07 probes for edges (e.g., pop semantics).
7. Verify: Simulate sequences; Hypothesis for Inv holds post-ops.

**Heuristic**: Prove read-only (size) first; mutators second; use Abs for abstract reasoning.

---

## 3. Canonical Example 1 – Stack Abstract Spec and Representation

Abstract model: Stack as finite sequence $S \in T^*$; Abs(self) = tuple(self._data).

RepInv: The semantic structure of _data matches Abs (e.g., prefix/top consistency via ops); we additionally assume self._data is exclusively owned: no external code mutates it; all access goes through Stack methods.

Init triple: $\{\mathrm{true}\} \ Stack(\mathrm{initial}: \mathrm{list}[T]) \ \{\mathrm{RepInv} \wedge \mathrm{Abs}(self) = \mathrm{tuple}(\mathrm{initial})\}$.

Code:
```python
from dataclasses import dataclass, field
from typing import Generic, TypeVar, Tuple, List

T = TypeVar('T')

def Abs(stack: 'Stack[T]') -> Tuple[T, ...]:
    return tuple(stack._data)

@dataclass
class Stack(Generic[T]):
    _data: List[T] = field(default_factory=list)

    def __post_init__(self):
        # {true} init {RepInv ∧ S = tuple(initial)}
        # We rely on dataclass construction and the Abs definition;
        # RepInv is a semantic / modelling invariant, not runtime-checked here.
        pass
```

**Proof sketch**: Constructor yields list; Abs = tuple(_data); RepInv holds by type/semantics. Since __post_init__ does not modify _data, and Abs(self) = tuple(self._data), the postcondition Abs(self) = tuple(initial) follows immediately from Python’s semantics of dataclass initialization. Termination trivial.

**Verification**: Stack([1,2]) → Abs = (1,2); RepInv holds.

---

## 4. Canonical Example 2 – Push Operation Triple and Proof

Op spec: push(elem: T) → None; Pre: true; Post: $S' = S + [elem]$.

Triple: $\{\mathrm{RepInv} \wedge \mathrm{true}\} \ push(\mathrm{elem}) \ \{\mathrm{RepInv} \wedge \mathrm{Abs}(self) = \mathrm{Abs}(\mathrm{old}) + (\mathrm{elem},)\}$.

Code:
```python
    def push(self, elem: T) -> None:
        # {RepInv ∧ Pre} pre
        old_abs = Abs(self)
        old_data = self._data[:]  # Snapshot for prefix check
        self._data.append(elem)
        # {RepInv ∧ Post} post
        if __debug__:
            assert self._data[:-1] == old_data, "Prefix preserved"
            assert Abs(self) == old_abs + (elem,), "Post: S' = S + [elem]"
```

**Proof sketch** (M05C03 contract + M05C01 preservation):
- $\{\mathrm{RepInv} \wedge \mathrm{true}\}$ pre: old_abs = Abs(self).
- Body: append extends list; _data[:-1] unchanged by semantics; Abs' = old_abs + (elem,).
- Preservation: RepInv pre $\wedge$ append $\Rightarrow$ RepInv post (list type, ownership assumed).
- Consequence: RepInv post $\wedge$ Abs' = old_abs + (elem,) $\Rightarrow$ Post.
- Termination: O(1) amortized (M04); no loop, trivial variant $V = 0$.
- Sequential composition example: $\{\mathrm{RepInv}\} \ push(a) \ \{\mathrm{RepInv} \wedge S = S_0 + (a,)\} \ push(b) \ \{\mathrm{RepInv} \wedge S = S_0 + (a,b)\}$.

**Verification**: $S = (1,)$; push(2) → $S' = (1,2)$; Post holds; RepInv preserved (prefix [1] == [1]).

---

## 5. Canonical Example 3 – Pop Operation Triple and Proof

Op spec: pop() → T; Pre: $\mathrm{len}(S) > 0$; Post: elem = $S[-1]$, $S' = S[:-1]$.

Triple: $\{\mathrm{RepInv} \wedge \mathrm{len}(\mathrm{Abs}(self)) > 0\} \ pop() \ \{\mathrm{RepInv} \wedge \mathrm{elem} = \mathrm{Abs}(\mathrm{old})[-1] \wedge \mathrm{Abs}(self) = \mathrm{Abs}(\mathrm{old})[:-1]\}$.

Code:
```python
    def pop(self) -> T:
        # Pre: len >0 (raise if not)
        if len(self._data) == 0:
            raise IndexError("pop from empty stack")
        # {RepInv ∧ Pre} pre
        old_abs = Abs(self)
        old_prefix = self._data[:-1]  # Snapshot
        old_len = len(self._data)
        elem = self._data.pop()
        # {RepInv ∧ Post} post
        if __debug__:
            assert self._data == old_prefix, "Prefix preserved"
            assert elem == old_abs[-1], "Post: elem = old top"
            assert Abs(self) == old_abs[:-1], "Post: S' = S[:-1]"
            # Variant V = len(Abs(self)); V' = V - 1 < V
            assert len(Abs(self)) == old_len - 1, "Variant decrease"
        return elem
```

**Proof sketch** (M05C03 + M05C04):
- $\{\mathrm{RepInv} \wedge \mathrm{len} > 0\}$ pre: old_abs = Abs(self).
- Body: pop removes last; _data == old[:-1]; Abs' = old_abs[:-1].
- Preservation: RepInv pre $\wedge$ pop $\Rightarrow$ RepInv post (list type, ownership assumed).
- Consequence: RepInv post $\wedge$ elem = old[-1] $\wedge$ Abs' = old[:-1] $\Rightarrow$ Post.
- Termination: O(1); variant $V = \mathrm{len}(\mathrm{Abs}(self))$; $V' = V - 1 < V$ under Pre.
- Sequential composition: $\{\mathrm{RepInv} \wedge \mathrm{len} > 0\} \ pop() \ \{\mathrm{RepInv} \wedge S = S_0[:-1]\} \ push(b) \ \{\mathrm{RepInv} \wedge S = S_0[:-1] + (b,)\}$.

**Verification**: $S = (1,2)$; pop() → elem=2, $S' = (1,)$; Post holds; RepInv preserved (prefix [1] == [1]).

---

## 6. Canonical Example 4 – Size Operation Triple and Proof

Op spec: size() → int; Pre: true; Post: res = $\mathrm{len}(S)$.

Triple: $\{\mathrm{RepInv} \wedge \mathrm{true}\} \ size() \ \{\mathrm{RepInv} \wedge \mathrm{res} = \mathrm{len}(\mathrm{Abs}(self))\}$.

Code:
```python
    def size(self) -> int:
        # {RepInv ∧ Pre} pre
        old_abs = Abs(self)
        res = len(self._data)
        # {RepInv ∧ Post} post
        if __debug__:
            assert res == len(old_abs), "Post: res = len(S)"
        return res
```

**Proof sketch** (M05C03 read-only):
- Body: len pure; res = len(_data) = len(Abs(self)).
- Preservation: true (no state change).
- Consequence: RepInv $\wedge$ res = len(Abs) $\Rightarrow$ Post.
- Termination: O(1); no loop.
- Sequential composition: $\{\mathrm{RepInv}\} \ size() \ \{\mathrm{RepInv} \wedge \mathrm{res} = \mathrm{len}(S)\} \ pop() \ \{\mathrm{RepInv} \wedge \dots\}$ (Pre pop from Post size).

**Verification**: $S = (1,2)$; size() → res=2; Post holds.

---

## 7. Canonical Example 5 – M05C07 Probe for Stack Edges

From M05C07: Probe RepInv under pop Pre (len >0); use model for Inv.

Model: Ghost list mirroring Abs.

Code:
```python
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant
from hypothesis.strategies import integers

class StackMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.model: List[int] = []  # Ghost model
        self.stack = Stack[int]()

    @rule(x=integers(-10, 10))
    def push(self, x):
        self.model.append(x)
        self.stack.push(x)

    @rule()
    def pop(self):
        # Respect Pre: only if non-empty
        if len(self.model) > 0:
            expected = self.model.pop()
            actual = self.stack.pop()
            assert actual == expected, "Post: elem == model top"

    @invariant()
    def rep_inv(self):
        # RepInv: Abs(stack) == tuple(model)
        assert Abs(self.stack) == tuple(self.model)

StackTest = StackMachine.TestCase

# Run: pytest -v --hypothesis-show-statistics
# Probes: push/pop seq; Inv holds; if buggy push/pop alters prefix or top, model diverges; shrinks to push/pop
```

**Verification**: Rules honor Pre; Inv assert catches RepInv breaches (e.g., wrong pop order); model enforces abstract correctness.

---

## 8. Quick Reference – Patterns

| Op Type     | Triple Sketch                      | Preservation Arg                  | Termination Variant              |
|-------------|------------------------------------|-----------------------------------|----------------------------------|
| Mutator (push) | {RepInv} push {RepInv ∧ S' = S + [elem]} | append preserves tuple prefix     | N/A (O(1))                       |
| Mutator (pop) | {RepInv ∧ len >0} pop {RepInv ∧ elem = S_old[-1] ∧ S' = S_old[:-1]} | pop preserves prefix tuple        | V = len(S); V' = V -1            |
| Accessor (size) | {RepInv} size {RepInv ∧ res = len(S)} | len pure, no change               | N/A (O(1))                       |

**Note**: Abs = tuple(_data); assert Abs pre/post; compose Post ∧ RepInv ⇒ Pre next.

---

## 9. Robustness – DS Proofs in Practice

- **Composition**: Post op ∧ RepInv ⇒ Pre next; global init RepInv.
- **Overhead**: Asserts debug-only (-O elides); dataclass for rep.
- **Errors**: Pre raise IndexError; RepInv assert AssertionError (internal bug).
- **Aliasing**: RepInv assumes exclusive _data ownership (no external refs mutate it); for shared, use immutable T or copy.
- **Testing**: M05C06 properties (pop(push(x)) = x); M05C07 edges (repeated pop).
- **Limits**: Finite T; aliasing risk (immutable T mitigates); extend to queue via dual RepInv.

**Example**: Queue: RepInv "deque == front + rear"; variant len for dequeue.

---

## 10. Permanent Habit

Derive DS rigorously:

```python
@dataclass
class Stack(Generic[T]):
    _data: List[T] = field(default_factory=list)

    def push(self, elem: T) -> None:
        old_abs = Abs(self)
        old_data = self._data[:]
        self._data.append(elem)
        if __debug__:
            assert self._data[:-1] == old_data
            assert Abs(self) == old_abs + (elem,)

    def pop(self) -> T:
        if len(self._data) == 0:
            raise IndexError("empty")
        old_abs = Abs(self)
        old_prefix = self._data[:-1]
        elem = self._data.pop()
        if __debug__:
            assert self._data == old_prefix
            assert elem == old_abs[-1]
            assert Abs(self) == old_abs[:-1]
        return elem
```

Spec → Abs + RepInv → per-op triple → preservation/termination → embed checks → probe edges.

---

## 11. What You Must Carry Forward

1. Abs maps concrete to abstract; RepInv constrains rep.
2. Prove {RepInv ∧ Pre} op {RepInv ∧ Post}; variant for total.
3. Workflow: Abstract → rep + RepInv → op triples → compose.
4. Patterns: Pre raise caller; assert RepInv/Post callee.
5. Python: Dataclass; __debug__ zero-cost; M05C07 for edges.

## 12. Progress Note & What’s Next in M05

After M05C09, DS derivations enable verified modules, completing the proofs toolkit.

M05C09 complete.

Next: **M05C10 – Program-wide discipline: spec → prove → implement → test → measure**: Synthesis.

---

## 13. Glossary & Notation

- Abs: Abstraction function (concrete → abstract).
- RepInv: Representation Inv (constrains concrete rep).
- {Pre} op {Post}: Hoare triple (total with variant).
- Preservation: Pre ∧ RepInv ⇒ RepInv post-body.
# M05C10 · Program-Wide Discipline: Spec → Prove → Implement → Test → Measure – Synthesis

**Goal.** This core synthesizes the M05 toolkit into a cohesive development discipline for producing correct, performant, and verifiable programs. Upon completion, practitioners will apply the full pipeline—specifying contracts, proving invariants/termination, implementing with checks, testing via properties, and measuring empirically—to small-to-medium artifacts like quicksort or a stack, ensuring logical guarantees align with runtime behavior and performance predictions (M02/M04)—bridging theoretical proofs to production-grade code.

**Scope** (explicit delimiters):
- End-to-end workflow for deterministic, finite-state programs/DS (e.g., algorithms from M05C01–C02, M05C08–C09).
- Integration of spec/proof (M05C03–C04), implementation/checks (M05C05), testing (M05C06–C07), measurement (M02/M04 asymptotics).
- Python 3.10+; focuses on synthesis via one canonical artifact (quicksort); excludes concurrency (M18), distribution (M20), or non-determinism (M10).
- Assumes prior cores; yields a "gold standard" template for future modules (M06+).

Within this scope, the workflow produces a self-contained, annotated module with spec, proof sketch, code, tests, and metrics, aligning with OSS practices (e.g., PEP 8, pytest, Hypothesis).

---

## 1. Core Definitions

**Development pipeline**: Sequential phases ensuring correctness (partial/total via Hoare triples $\{Pre\} prog \{Post\}$), termination ($V$ well-founded), testability (properties falsify $I$, $Pre$, $Post$), and performance (asymptotics validated empirically).

- **Spec**: $Pre/Post$ contracts (M05C03); abstract model (e.g., sorted array).
- **Prove**: Invariants $I$ (M05C01–C02), variants $V$ (M05C04), composition (M05C08–C09).
- **Implement**: Code with embedded checks (M05C05); type hints/mypy.
- **Test**: Property-based (M05C06–C07); coverage on edges/assumptions.
- **Measure**: Microbenchmarks (M02); asymptotic alignment (M04); energy proxies.

**Pipeline Discipline** (informal guarantee): Formal phases yield logical guarantees (e.g., $\{Pre\} prog \{Post\}$ via proved $I/V$ and checks); empirical phases provide confidence (no property falsifications, measurements empirically supporting an $f(n)$ scaling over tested ranges). Violations iterate back (e.g., test fail $\to$ refine $I$). This is methodological: proofs ensure partial correctness; tests/measurements bound practical robustness.

Extends M05: Composes contracts + proofs + checks + PBT + metrics; upgrades to "program-wide" (full artifact, not isolated loops/ops).

---

## 2. Mechanical Derivation Workflow

For artifact $Prog$ (e.g., quicksort on array of size $n$):

1. **Spec**: Define $Pre(n, arr): n \ge 0 \land \text{len}(arr) \ge n$, where $\texttt{arr}$ is a $\texttt{list[int]}$; $Post(n, arr): arr[0{:}n)$ sorted non-decreasing $\land \mathrm{multiset}(arr[0{:}n)) = \mathrm{multiset}(arr_0[0{:}n))$. Abstract model (e.g., permutation preserving elements).
2. **Prove**: Decompose (e.g., partition + recursion); derive $I/V$ per component (M05C01/C08); compose triples (Post_partition $\Rightarrow$ Pre_recurse); total via lex $V$ (M05C04).
3. **Implement**: Code from proof skeleton; embed contracts (M05C03), checks (M05C05: `__debug__` asserts $I$); type hints.
4. **Test**: Properties (M05C06: e.g., sorted(output) $\land$ elements preserved); stateful for DS (M05C07: target assumptions like pivot placement).
5. **Measure**: Benchmarks (M02: `timeit` warmup, `perf` flamegraphs); asymptotic fit (M04: plot $T(n)$ vs $n \log n$); Hypothesis for logical edge cases; hand-crafted adversarial inputs for performance (e.g., sorted arrays).
6. **Iterate**: Violations $\to$ refine spec/proof/impl; coverage $\ge 90\%$; doc pipeline in README.
7. **Verify**: Run full suite; OSS-style CI (mypy, pytest); report gaps.

**Heuristic**: Start small (loop/DS op); scale to full $Prog$; template: Spec in docstring, proof in comments, tests in sep file.

---

## 3. Canonical Example 1 – Quicksort: Full Pipeline Application

Artifact: In-place quicksort on `arr[0{:}n)`; orchestrates M05C08 partition (assume `lomuto_partition` exported from prior module).

**Spec** ($Pre/Post$):  
$Pre(n, arr): n \ge 0 \land \text{len}(arr) \ge n$, where $\texttt{arr}$ is a $\texttt{list[int]}$.  
$Post(n, arr): arr[0{:}n)$ sorted non-decreasing $\land \mathrm{multiset}(arr[0{:}n)) = \mathrm{multiset}(arr_0[0{:}n))$, where $arr_0$ denotes the initial value of $arr$ before quicksort executes.  
Abstract: Permutation of input preserving counts.

**Prove** (orchestration; details in M05C08/C02):  
Decompose: Base ($n \le 1$: true); recurse: Partition $\{Pre\} \to \{Post_{part}\}$ ($[L,i) < p \le [i+1,R)$); $\{Post_{part} \land len < n\} \to \{Post_{sub}\}$ (IH strong on size); compose: Sorted subs + pivot placement $\Rightarrow Post$.  
Variant: $V = R - L$; each recursive call satisfies $R' - L' < R - L$.

**Implement** (with checks; imports M05C08 partition):
```python
from typing import List
# Assume lomuto_partition from M05C08 in scope

def quicksort(arr: List[int], n: int) -> None:
    # Pre: n >= 0 and len(arr) >= n
    if __debug__:
        assert n >= 0 and len(arr) >= n
    # Post: arr[0:n] (Python half-open) sorted non-decreasing and multiset preserved
    # Prove: Partition I/V (M05C08) + IH on subs (M05C02); V = R - L
    def qs(L: int, R: int) -> None:
        if R - L <= 1: return
        i = lomuto_partition(arr, L, R)
        qs(L, i)
        qs(i + 1, R)

    qs(0, n)
```

**Test** (M05C06–C07; pytest + Hypothesis):
```python
import pytest
from hypothesis import given, settings
from hypothesis.strategies import lists, integers
# Assume lomuto_partition from M05C08

@given(lists(integers(-100, 100), min_size=0, max_size=100))
@settings(max_examples=500)
def test_quicksort_correctness(xs):
    orig = xs[:]
    quicksort(xs, len(xs))
    assert xs == sorted(orig)  # Post: sorted and multiset preserved

@given(lists(integers(-100, 100), min_size=2, max_size=10))
def test_partition_assumption(xs):
    # M05C07: Targeted regression for all >= p (should i=L)
    p = xs[-1]
    xs = [p+1] * (len(xs)-1) + [p]
    i = lomuto_partition(xs, 0, len(xs))
    assert i == 0  # No swaps, pivot stays
```

**Measure** (M02/M04):  
`timeit` avg over 1000 runs: $T(n) \approx 1.2 n \log n$ (plot empirically supports $n \log n$ scaling over tested ranges); flamegraph shows partition hot; benchmarks on sorted inputs reveal $O(n^2)$ behavior.

---

## 4. Canonical Example 2 – Stack DS: Pipeline for Mutable Structure

Artifact: Stack with push/pop/size (orchestrates M05C09).

**Spec**: Abstract $S \in T^*$; push($e$): $S' = S + [e]$; pop(): Pre $|S|>0$, returns $S[-1]$, $S' = S[:-1]$; size(): $|S|$.

**Prove** (M05C09 orchestration): Abs($self) = tuple($\_data$); RepInv assumes no external aliasing of $_data$ (mutated only via methods); triples per op preserve Post; variant $V = len(S)$ for pop. This RepInv is not enforced by Python’s type system; it is a module-level convention (clients must not touch $_data$).

**Implement** (dataclass + checks; RepInv via API discipline):
```python
from dataclasses import dataclass, field
from typing import Generic, TypeVar, List, Tuple

T = TypeVar('T')

def Abs(stack: 'Stack[T]') -> Tuple[T, ...]:
    return tuple(stack._data)

@dataclass
class Stack(Generic[T]):
    _data: List[T] = field(default_factory=list)
    # RepInv: _data mutated only via Stack methods (no external aliasing)

    def push(self, e: T) -> None:
        # Pre: true; Post: Abs' = Abs + (e,)
        old_abs = Abs(self)
        self._data.append(e)
        if __debug__:
            assert Abs(self) == old_abs + (e,)  # Post

    def pop(self) -> T:
        # Pre: len(self._data) > 0; Post: e = old[-1], Abs' = old[:-1]
        if not self._data:
            raise IndexError("pop empty")
        old_abs = Abs(self)
        e = self._data.pop()
        if __debug__:
            assert e == old_abs[-1]
            assert Abs(self) == old_abs[:-1]  # Post
        return e

    def size(self) -> int:
        # Pre: true; Post: res = len(Abs)
        res = len(self._data)
        if __debug__:
            assert res == len(Abs(self))
        return res
```

**Test** (stateful M05C06; edges M05C07):
```python
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant
from hypothesis.strategies import integers

class StackMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.model: List[int] = []
        self.s = Stack[int]()

    @rule(x=integers(-10, 10))
    def push(self, x):
        self.model.append(x)
        self.s.push(x)

    @rule()
    def pop(self):
        if self.model:
            assert self.s.pop() == self.model.pop()

    @invariant()
    def rep_inv(self):
        assert Abs(self.s) == tuple(self.model)

StackTest = StackMachine.TestCase
```

**Measure**: Push/pop $O(1)$ amortized (M04 potential); benchmark 1M ops: $T \approx 50 ns/op$; adversarial (alternating) no regression.

---

## 5. Canonical Example 3 – Prefix Sum Scan: Algorithmic Pipeline

Artifact: Iterative prefix sum up to $n$ (M05C01 accumulator).

**Spec**: $Pre(arr, n): 0 \le n \le \text{len}(arr)$, where $\texttt{arr}$ is a $\texttt{list[int]}$; $Post(res): \text{len}(res)=n \land \forall k=1..n: res[k-1] = \sum_{t=0}^{k-1} arr[t]$.

**Prove**: Inv: $total = \sum_{t=0}^{i-1} arr[t]$, $0 \le i \le n$; $V = n-i$; preservation: $total += arr[i]$; consequence: $i=n \Rightarrow Post$.

**Implement**:
```python
def prefix_sum(arr: List[int], n: int) -> List[int]:
    # Pre: 0 <= n <= len(arr)
    # Post: res contains prefix sums of arr[0:n] (half-open)
    if n < 0 or n > len(arr):
        raise ValueError("bounds")
    res = []
    total = 0
    for i in range(n):
        if __debug__:
            assert total == sum(arr[:i])  # Inv (O(i); debug-only, fine for small n)
        total += arr[i]
        res.append(total)
    if __debug__:
        assert len(res) == n
        assert all(sum(arr[:k]) == res[k-1] for k in range(1, n+1))
    return res
```

**Test**:
```python
@given(lists(integers(-10,10), min_size=0, max_size=50), integers(0,50))
def test_prefix(arr, n):
    assume n <= len(arr)
    res = prefix_sum(arr, n)
    assert len(res) == n
    assert all(sum(arr[:k]) == res[k-1] for k in range(1, n+1))
```

**Measure**: $O(n)$ linear; timeit: $T(n) \sim 10 n$ ns (run with `python -O` to disable $O(n^2)$ debug checks); vs naive sum: $O(n^2)$ quadratic.

---

## 6. Quick Reference – Patterns

| Phase       | Key Artifact                          | Ties to M05C#                  | Metrics/Checks                  |
|-------------|---------------------------------------|--------------------------------|---------------------------------|
| Spec       | $Pre/Post$ docstrings; abstract model | M05C03 contracts               | mypy static; Hypothesis assume |
| Prove      | $I/V$ comments; triples per op/loop  | M05C01–C02/C04/C08–C09 proofs | `__debug__` assert $I$         |
| Implement  | Annotated code; embedded checks      | M05C05 runtime Inv             | Branch coverage: $\ge 90\%$    |
| Test       | @given properties; stateful machines | M05C06–C07 PBT falsification   | Shrinks: Minimal violations    |
| Measure    | timeit/flamegraph; asymptotic plots  | M02 benchmarks/M04 analysis    | $T(n) \sim f(n)$ fit           |

**Note**: Iterate on failures (e.g., test break $\to$ refine $I$); CI: pytest + mypy.

---

## 7. Robustness – Pipeline in Practice

- **Composition**: Post_phase$i \Rightarrow Pre_{i+1}$ (e.g., partition Post $\to$ recurse Pre); chain via contracts.
- **Overhead**: Checks `-O` elided; Hypothesis bounded ($max_examples=1000$); benchmarks warmed.
- **Errors**: Spec gaps $\to$ test falsify; proof mismatches $\to$ assert fail; perf regressions $\to$ adversarial inputs (M05C07).
- **Scalability**: Small artifacts first; for larger (M06+), modularize (one phase per submodule).
- **Tools**: pytest/Hypothesis CI; `asv` for perf regression; doc pipeline in README.md.

**Example**: Quicksort adversarial (sorted): Benchmarks on sorted inputs show $O(n^2)$; randomized pivots (M10) mitigate in practice.

---

## 8. Permanent Habit

Adopt pipeline template:

```python
# spec.py: Pre/Post
def quicksort(arr: List[int], n: int) -> None:
    # Pre: n >= 0 /\ len(arr) >= n
    # Post: sorted(arr[0:n]) /\ multiset preserved
    # Prove: Partition I/V (M05C08) + IH (M05C02)
    # ... impl with __debug__ asserts

# test_quicksort.py: Hypothesis properties
# benchmark_quicksort.py: timeit + plots
```

For every $Prog$: Spec $\to$ Prove sketch $\to$ Impl + checks $\to$ PBT $\to$ Measure; CI all; report in notes.

---

## 9. What You Must Carry Forward

1. Pipeline: Spec ($Pre/Post$) $\to$ Prove ($I/V$, triples) $\to$ Impl (checks) $\to$ Test (properties) $\to$ Measure (bench/asymp).
2. Composition: Post$_i \Rightarrow$ Pre$_{i+1}$; iterate on violations.
3. Workflow: Modular phases; template per artifact.
4. Patterns: Docstrings spec; comments proofs; pytest/Hypo tests; timeit metrics.
5. Python: `__debug__` zero-cost; Hypothesis edges; mypy static.

## 10. Progress Note & What’s Next in M05

After M05C10, M05 toolkit synthesizes into disciplined development, ready for algorithmic tracks.

M05C10 complete.

Next: **M06C01 – Binary Heaps: Invariants and Array Layout** (S02 begins).

---

## 11. Glossary & Notation

- Pipeline: Spec $\to$ Prove $\to$ Impl $\to$ Test $\to$ Measure – end-to-end discipline.
- $\{Pre\} prog \{Post\}$: Hoare triple – correctness guarantee.
- $I$: Invariant – preserved predicate (M05C01–C02).
- $V$: Variant – decreasing measure (M05C04).
- PBT: Property-based testing – Hypothesis falsification (M05C06–C07).
- $\Theta(f(n))$ Asymptotic tight bound (M04); in practice, approximated by $T(n) \sim f(n)$ on tested ranges.
