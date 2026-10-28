# 15 — Box, Deref, Dynamically Sized Types, and Cow

**Course 2, day 5 · Module 15 of 90**  
`█████░░░░░░░░░░░░░░░` **15/90**

[← Module 14: RAII, Drop, Unwinding, and Failure Atomicity](../module-14-raii-drop-unwinding-and-failure-atomicity/index.md) · [Course 2 overview](../index.md) · [Ninety-module map](../../../COURSE_MAP.md) · [Module 16: Rc, Weak, and Ownership Graphs →](../module-16-rc-weak-and-ownership-graphs/index.md)

## The question

> When is indirection required by representation or ownership, what metadata travels with a pointer, and when should an API borrow-or-own conditionally?

## Why this comes now

Recursive values, dynamically sized data, and conditional allocation require indirection, but indirection is not one undifferentiated trick. `Box`, dereference coercion, DST metadata, and `Cow` are studied together because each changes where ownership lives while preserving a different access contract.

## What you will be able to do

- Use Box for exclusive heap-owned indirection and recursive finite-size representation without equating Box with shared ownership.
- Explain Deref, deref coercion, method lookup, and why custom Deref is not ordinary inheritance.
- Reason about sized and dynamically sized types, fat pointers, metadata, unsizing, boxed slices, and boxed strings.
- Use Cow only when the common path can borrow and a well-defined transformation sometimes requires ownership.
- Choose among inline ownership, Box, Rc, handles, arenas, and borrowed views from topology and cost.

## Core model

### Box is exclusive owned indirection

`Box<T>` owns one `T` in a heap allocation and has one ordinary owner. Moving the `Box` transfers allocation ownership; it does not clone `T` and does not imply shared ownership. A `Box` can be useful because:

- recursive types need an indirection to obtain finite size;
- a large value should have stable allocation ownership independent of stack frame size;
- an unsized value such as `[T]` or `str` needs an owning pointer;
- a trait-object boundary may own a dynamically dispatched value (Course 3).

`Box<T>` does not by itself pin `T`; the pointee can be moved out when the type permits and the box is not pinned under a stronger contract.

### Recursive representation

```rust
pub enum Expr {
    Number(i64),
    Add(Box<Expr>, Box<Expr>),
    Negate(Box<Expr>),
}
```

Without indirection, the enum would contain itself with no finite size. The boxes establish an ownership tree. They are not needed because “trees use boxes”; they are needed at recursive edges that break size recursion and own children.

### Deref is a contract, not inheritance

`Deref` lets a pointer-like wrapper expose a target for `*` and supports deref coercions/method lookup. Implementing it changes implicit behavior and should be reserved for types that are genuinely pointer-like. It is not a general way to forward every method or simulate class inheritance.

When `Box<String>` is passed to a function expecting `&str`, several steps may occur: borrow the box, dereference to `String`, then coerce to `str`. Learn to identify the final borrowed target and owner rather than memorizing the chain.

### Dynamically sized types and metadata

Types such as `[T]` and `str` do not have a compile-time-known size and normally appear behind a pointer. A reference to a slice or `str` is a wide pointer carrying data address plus metadata (length). A reference to a sized `T` is normally thin, but exact representation claims should remain within documented guarantees.

`Box<[T]>` owns exactly a slice allocation without spare vector capacity. `Box<str>` owns UTF-8 string contents without a `String` capacity field. Converting from `Vec<T>` or `String` may shrink or reuse allocations according to library behavior; do not assume a particular allocator action unless documented.

### Cow and conditional ownership

`Cow<'a, B>` represents either a borrowed `&'a B` or owned `<B as ToOwned>::Owned`. It is useful when:

- the common input already satisfies the canonical form and can be borrowed;
- some inputs require a transformation and owned storage;
- callers can use the result within the returned lifetime or accept the owned variant.

```rust
use std::borrow::Cow;

pub fn normalize_spaces(input: &str) -> Cow<'_, str> {
    let trimmed = input.trim();
    let canonical = !trimmed.chars().any(|ch| ch.is_whitespace() && ch != ' ')
        && !trimmed.contains("  ");

    if canonical {
        Cow::Borrowed(trimmed)
    } else {
        Cow::Owned(trimmed.split_whitespace().collect::<Vec<_>>().join(" "))
    }
}
```

This still scans input and may allocate a temporary vector in the owned path. “Borrowed fast path” is a measured design hypothesis, not automatic performance superiority. Course 9 owns benchmarking.

### Choosing indirection

Ask:

| Requirement | Candidate |
|---|---|
| one owner, recursive edge | `Box<T>` |
| shared immutable liveness, single thread | `Rc<T>` |
| non-owning observer of Rc allocation | `Weak<T>` |
| stable logical identity independent of borrows | generational handle |
| temporary view | `&T` / slice |
| borrow if unchanged, own if transformed | `Cow` |
| address-sensitive invariant | possibly `Pin`, only after proof |

Heap allocation is not an architecture. The ownership and liveness graph is.

### Worked derivation: expression engine

A boxed expression tree owns every child exactly once. Evaluation borrows the tree recursively, so it allocates nothing during ordinary traversal. A depth or step budget prevents uncontrolled recursion in hostile input. Parsing may return typed errors. If subexpressions must be shared, replacing every `Box` with `Rc` changes topology and cycle considerations; do not do it preemptively.

### Derive it yourself

A query representation contains literals, conjunctions, and optional normalization. Decide which recursive edges need `Box`, whether repeated subtrees need shared ownership, and whether normalized tokens should use `Cow` or owned strings. State allocation points.

### Misconception clinic

- Box gives one owner, not shared ownership and not automatic pinning.
- Deref should model pointer-like access, not convenience delegation.
- Wide pointers carry metadata; not every pointer is one word.
- Cow helps only when borrowed and owned paths match a real workload and lifetime boundary.

`Box<T>` owns one `T`. When the box is dropped, the contained value is dropped and its allocation is released. There is one ordinary ownership path unless the box itself is moved into another owner.

```rust
let count = Box::new(41_u64);
assert_eq!(*count + 1, 42);
```

The important facts are:

- `count` owns the box value;
- the box owns the `u64` allocation;
- borrowing `&*count` does not transfer ownership;
- moving `count` transfers responsibility for destruction;
- cloning a `Box<T>` clones `T` when `T: Clone`, creating a separate allocation and value.

### Heap placement is an implementation fact with API consequences

A `Box<T>` generally stores a pointer-sized handle inline and places `T` in an allocation. Do not infer that heap allocation is automatically slower, stable forever, or suitable for sharing. Allocation cost, cache behavior, and optimizer transformations depend on context. The semantic reason to use `Box` should be structural:

- break infinite recursive size;
- own an unsized value through a sized pointer;
- reduce the size of an outer enum variant;
- transfer one exclusive owner behind indirection;
- later, establish pinned heap storage.

### Moving a box versus moving its referent

Moving `Box<T>` transfers the pointer handle; the allocation normally remains at the same address. This observation alone does **not** create a pinning guarantee. Safe code may still move `T` out of an unpinned box when permitted:

```rust
let boxed = Box::new(String::from("owned"));
let text: String = *boxed;
```

The allocation is consumed and the `String` value is moved out. Address stability is a separate contract introduced by `Pin`.

### Borrowing through a box

```rust
fn length(text: &str) -> usize {
    text.len()
}

let text = Box::new(String::from("memory"));
assert_eq!(length(&text), 6);
```

Dereference coercions can turn `&Box<String>` through `&String` into `&str`. No allocation or clone is required. The box remains the owner.

### `Box` is not shared ownership

Passing `&Box<T>` is usually needlessly specific; accept `&T` unless the box identity or ownership wrapper itself matters. Multiple shared references may temporarily observe one boxed value, but there is still one owner. If independent long-lived owners are required, Module 16 evaluates `Rc`.

### API review

When a field type is `Box<T>`, ask what invariant the indirection carries. “The value is large” is not enough without measurement and outer-layout reasoning. “This enum must remain compact,” “this recursion needs finite size,” or “this owner must contain a DST” are inspectable claims.

A directly recursive enum has no finite compile-time size:

```rust,compile_fail
pub enum Expression {
    Number(i64),
    Add(Expression, Expression),
}
```

To store an `Expression`, Rust would need to know the size of two more expressions, each containing two more, indefinitely. Indirection makes recursive edges fixed-size:

```rust
pub enum Expression {
    Number(i64),
    Add(Box<Expression>, Box<Expression>),
}
```

The enum now contains pointer-sized boxes for recursive children. Each node is separately owned.

### Put indirection at the correct edge

Alternatives include:

```rust
Add(Box<(Expression, Expression)>)
```

or a separate node structure. These produce different allocation counts and layouts. The type should reflect traversal and mutation needs, not only compile.

A list may use:

```rust
enum List<T> {
    Empty,
    Cons(T, Box<List<T>>),
}
```

This creates one allocation per nonempty node. For sequence workloads, `Vec<T>` is usually more compact and faster to traverse. Recursive ownership is appropriate when tree shape and structural edits are central, not as a default container exercise.

### Enum size and cold variants

An enum's size must accommodate its largest variant plus discriminant and padding under the chosen representation. Boxing a very large, rare variant can reduce every enum value's inline size:

```rust
enum Event {
    Tick,
    Message(String),
    Snapshot(Box<[u8; 4096]>),
}
```

This trades an allocation on snapshot creation for a smaller common event. Module 18 teaches how to measure the actual size and how little of `repr(Rust)` layout should be assumed.

### Stable recursive identity

A boxed tree gives each allocation a temporary address, but domain identity should not be its address unless the design explicitly depends on address sensitivity. Replacing a subtree drops one allocation and creates another. Equality should normally compare domain values or explicit IDs.

### Traversal depth

A recursive type invites recursive algorithms. Deep adversarial input can overflow the call stack even though the ownership representation is valid. Iterative traversal with an explicit `Vec<&Node>` may be safer. Memory topology and control-flow topology are separate review dimensions.

### Clone semantics

Deriving `Clone` for a boxed tree performs a deep clone. That can be expensive and semantically wrong if callers expect shared structure. Course 6 explores shared ownership; Course 4 explores functional persistent approaches. In this module, expose cloning only when an independent deep copy is part of the contract.

`Deref` defines a target reached by the unary `*` operator and participates in certain coercions and method lookup. It is powerful because it changes how a type behaves in ordinary expressions.

```rust
use std::ops::Deref;

struct Name(String);

impl Deref for Name {
    type Target = str;

    fn deref(&self) -> &Self::Target {
        self.0.as_str()
    }
}
```

Now `&Name` can coerce to `&str` in expected contexts. This may be reasonable for a transparent smart-pointer-like wrapper, but it can also erase domain boundaries unexpectedly.

### Dereference coercion chain

For:

```rust
fn print_text(text: &str) {}
let value = Box::new(String::from("hello"));
print_text(&value);
```

The compiler can apply deref steps from `&Box<String>` to `&String` and then to `&str`. These are borrowed conversions. The `String` is not moved, and no `str` value is created separately.

### Method lookup auto-borrows and dereferences

A method call such as `value.len()` searches candidate receiver forms involving dereferencing and borrowing. This convenience can make ownership wrappers look like their targets. When behavior is ambiguous, use explicit forms such as `String::len(&value)` or inspect the receiver type in documentation.

### `DerefMut` adds authority

Implementing `DerefMut` permits mutable coercion to the target. That can allow callers to bypass wrapper invariants:

```rust
struct NonEmpty(String);
```

If `NonEmpty` dereferences mutably to `String`, callers can clear it. A domain newtype should expose invariant-preserving methods rather than `DerefMut`.

### Not a general inheritance mechanism

`Deref` should not be used to make one domain object “inherit” all methods of an inner service. It creates implicit conversion behavior in many contexts and confuses which invariants the outer type protects. Composition with named accessors is clearer:

```rust
impl NonEmpty {
    fn as_str(&self) -> &str {
        &self.0
    }
}
```

### Generic APIs

Prefer direct target bounds when the wrapper is irrelevant:

```rust
fn count_bytes(text: &str) -> usize { text.len() }
```

A caller can pass `String`, `Box<String>`, `Cow<str>`, or another deref-capable owner by borrowing appropriately. Accepting `&Box<str>` unnecessarily requires one ownership representation.

Most Rust types are `Sized`: their size is known at compile time. Some types are dynamically sized types (DSTs), including `str`, slices `[T]`, and trait objects. A DST cannot normally be stored directly as a local variable or struct field because its size is not known statically.

```rust
let text: &str = "hello";
let values: &[u32] = &[1, 2, 3];
```

The references are sized even though their referents are not. They carry metadata needed to interpret the pointee.

### Wide pointers

A reference to a sized `T` is typically represented by one address-sized component. A slice reference additionally carries a length; a `str` reference has byte length; a trait-object reference carries metadata used for dynamic dispatch. Exact layout should be observed and documented only within language guarantees, but the conceptual address-plus-metadata model explains `size_of_val` and unsizing.

### `T: ?Sized`

Generic type parameters are `Sized` by default:

```rust
fn inspect<T>(value: &T) {}
```

To accept a DST behind a reference:

```rust
fn inspect<T: ?Sized>(value: &T) -> usize {
    std::mem::size_of_val(value)
}
```

`?Sized` relaxes the implicit `Sized` bound; it does not mean “must be unsized.” Both sized and unsized referents are accepted.

### The unsized field rule

A struct may contain a DST only as its final field, making the struct itself dynamically sized:

```rust
struct Packet<T: ?Sized> {
    kind: u16,
    payload: T,
}
```

Ordinary code constructs and owns such values through pointers such as `Box<Packet<[u8]>>`; direct custom construction is more specialized than this course needs. The important design fact is that metadata for the tail determines the complete pointee size.

### `str` is not `[char]`

`str` is a valid UTF-8 byte sequence, dynamically sized by byte length. A character may occupy multiple bytes. String slices therefore carry byte length, and indexing by arbitrary integer is not provided. Range slicing must respect UTF-8 boundaries.

### `Sized` method restrictions

Methods taking `self` by value generally require a sized receiver unless special pointer forms are used. Trait and object-safety implications belong to Course 3. Here, recognize that unsized values are manipulated through references or owning pointers whose own size is known.

### Metadata is part of pointer validity

An address alone is insufficient to describe a slice or trait object. Any low-level representation work must preserve correct metadata as well as alignment and provenance. This is one reason arbitrary pointer reconstruction belongs to the systems/unsafe course.

A `Vec<T>` owns a growable allocation and stores length plus capacity. When growth is no longer required, converting it to `Box<[T]>` communicates fixed length and may release excess capacity:

```rust
let values = vec![1_u16, 2, 3];
let fixed: Box<[u16]> = values.into_boxed_slice();
assert_eq!(&*fixed, &[1, 2, 3]);
```

A `String` can similarly become `Box<str>`:

```rust
let text: Box<str> = String::from("immutable payload").into_boxed_str();
```

These remain owned, mutable only through exclusive access where the pointee API permits, and automatically reclaimed.

### Array-to-slice unsizing

A boxed array can coerce to a boxed slice:

```rust
let array: Box<[u8; 4]> = Box::new([1, 2, 3, 4]);
let slice: Box<[u8]> = array;
```

The owner changes its pointer metadata from statically known array length to dynamic slice length. The elements are not cloned.

### Why fixed ownership can improve APIs

A field of `Box<[T]>` promises there is no spare-capacity/growth interface through that field. This can reduce accidental mutation surface and sometimes reduce control-block size compared with `Vec<T>`. Measure representation in Module 18 rather than assume.

### Recovering growability

Converting a boxed slice back to `Vec<T>` is possible, but doing so repeatedly signals an unstable ownership contract. Choose the representation that matches the dominant phase.

### Unsizing and coercion sites

Rust performs certain unsizing coercions at assignment, argument, return, and other coercion sites. Not every nested custom wrapper automatically forwards unsizing. Do not assume `Wrapper<Box<[T; N]>>` becomes `Wrapper<Box<[T]>>` unless the wrapper and coercion rules support it.

### Boxed trait objects are a later specialization

`Box<dyn Trait>` owns an erased concrete implementor behind dynamic dispatch. Trait-object design, object safety, and architecture belong to Course 3. In this course it serves only as another example of owning a DST.

### Capstone use

A document snapshot that is immutable and fixed can store `Box<str>` instead of `String`. The live editable document still needs `String`. The distinction makes phase and capability visible.

`Cow<'a, B>` represents either borrowed data `&'a B` or an owned form associated with `B`. It supports clone-on-write: read-only operations use the borrowed input; mutation calls `to_mut`, cloning only if the value is currently borrowed.

For strings, `B = str` and the owned type is `String`:

```rust
use std::borrow::Cow;

fn normalize_spaces(input: &str) -> Cow<'_, str> {
    if input.contains("  ") {
        Cow::Owned(input.split_whitespace().collect::<Vec<_>>().join(" "))
    } else {
        Cow::Borrowed(input)
    }
}
```

The function avoids allocation on already-normal input while returning owned normalized text when required.

### `Cow` is an enum with a policy

Conceptually:

```text
Borrowed(&'a B)
Owned(B::Owned)
```

The caller must handle a return whose ownership varies. Methods through dereferencing can read `B` uniformly; `into_owned` guarantees an owned result, cloning when necessary.

### Mutation

```rust
fn ensure_period(text: &mut Cow<'_, str>) {
    if !text.ends_with('.') {
        text.to_mut().push('.');
    }
}
```

If borrowed and already terminated, no allocation occurs. If mutation is needed, `to_mut` creates owned storage. Repeated mutations then use that same owned value.

### When `Cow` helps

Use it when:

- a common path can return a view of caller data;
- a less common path must transform or synthesize owned data;
- callers can use either uniformly;
- avoiding the common-path allocation matters enough to justify a sum type.

### When `Cow` obscures design

If every path allocates, return the owned type. If callers almost always call `into_owned` immediately, borrowing saved little. If mutation semantics are central, accept or return `String`. If multiple ownership sources are involved, `Cow` may not solve identity or lifetime coupling.

### Lifetime effect

A borrowed `Cow` keeps the source borrowed. Returning it can extend that borrow just like returning `&str`. The owned variant does not erase the function's declared lifetime parameter, but once converted into an owned result it is independent of the source.

### Cost analysis
Course 9 will benchmark. Here, write branch tests and allocation reasoning without inventing performance claims. The API should first be correct and comprehensible.

Use this decision sequence.

### 1. Does the value need ownership here?

If the callee only inspects, borrow. If ownership is transferred and inline storage is fine, store `T` directly. Do not allocate to avoid a straightforward lifetime.

### 2. Is the type recursively sized?

Place indirection on recursive edges. Compare `Box` trees with arena/index representations and flat vectors.

### 3. Is the value dynamically sized?

Own it through `Box<str>`, `Box<[T]>`, or another suitable pointer. If growth is needed, use `String`/`Vec`.

### 4. Is outer size the problem?

Boxing a rare large variant may shrink the common enum. Verify with layout observations and workload evidence.

### 5. Is shared ownership required?

`Box` does not provide it. Borrow if one owner outlives all users; use `Rc` in single-threaded shared topology only when independent owners are real.

### 6. Is address sensitivity required?

An ordinary box does not prevent moving the pointee out. Pinning adds a separate contract. Do not conflate “currently allocated” with “cannot be moved.”

### 7. Is conditional ownership real?

Use `Cow` when borrowed and owned branches are both meaningful and common-path allocation avoidance matters.

### 8. Does `Deref` preserve the outer abstraction?

If mutable target access can violate an invariant, do not expose `DerefMut`. Prefer named accessors for domain wrappers.

### Observation table
For each indirection field, record:

| field | owner count | mutability | size reason | growth | address-sensitive | alternative rejected |
|---|---:|---|---|---|---|---|

A box whose only justification is “Rust likes boxes” fails review.

A query language supports literals, conjunction, negation, and a predicate implemented by an extension. The design must choose unique recursion, borrowed/owned text, and optional dynamic dispatch without treating every pointer as interchangeable.

### Closed built-in syntax

```rust
enum Expr<'source> {
    Literal(Cow<'source, str>),
    And(Box<Expr<'source>>, Box<Expr<'source>>),
    Not(Box<Expr<'source>>),
}
```

`Box` makes recursive variants finite and preserves unique ownership. `Cow` lets parser literals borrow source while normalized literals own text. If the AST must outlive source, convert it to an owned form at the boundary.

### Why not `Rc`

The syntax tree has one owner. Traversal borrows it; rewrite uses `&mut`. Sharing identical subexpressions could justify `Rc`, but then liveness and mutation policy change. Do not introduce shared ownership for cheap cloning before measuring or specifying DAG semantics.

### Extension predicate

An open plugin predicate might use `Box<dyn Predicate>` in a variant. That is type erasure and dynamic dispatch. Course 3 will study object safety; here the ownership question is that the AST uniquely owns the erased implementation.

### DST boundary

`dyn Predicate` and `str` are dynamically sized, so they appear behind a pointer/reference carrying metadata. `Box<dyn Predicate>` has a known inline owner representation while the concrete object size varies.

### `Deref` restraint

A `Query` newtype should not implement `Deref<Target = Expr>` merely to expose internal methods. Named methods can preserve validation and leave room for representation changes. `Box` implements `Deref` because pointer-like access is its purpose.

### Clone-on-write normalization

A method can call `to_mut` on `Cow` only when a transformation is required. Borrowed literals allocate then; owned literals mutate in place. The API should report that normalization may allocate. If every literal is normalized at parse time, returning owned `Box<str>` may be simpler.

### Destruction

Dropping the root recursively drops boxes and predicate owners. Deep adversarial trees can overflow the call stack during recursive traversal/destruction; a production parser may enforce depth or use iterative arenas. Memory safety does not imply unbounded-depth robustness.

## Use the idea in a complete program

The course capstone is **Memory Workspace**, an in-memory document workspace with handles, snapshots, edit sessions, and caches. Introduce immutable snapshots and conditional query ownership. Use `Box` or `Cow` only where the product needs indirection or conditional allocation. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-05-boxed-expressions/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 16 when you can:

- answer the module question—“When is indirection required by representation or ownership, what metadata travels with a pointer, and when should an API borrow-or-own conditionally?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Use Box for exclusive heap-owned indirection and recursive finite-size representation without equating Box with shared ownership;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [std::boxed](https://doc.rust-lang.org/std/boxed/)
- [std::ops::Deref](https://doc.rust-lang.org/std/ops/trait.Deref.html)
- [std::borrow::Cow](https://doc.rust-lang.org/std/borrow/enum.Cow.html)

[← Module 14](../../../02-rust-ownership-lifetimes-memory/course-book/module-14-raii-drop-unwinding-and-failure-atomicity/index.md) · [ninety-module map](../../../COURSE_MAP.md) · [Module 16 →](../../../02-rust-ownership-lifetimes-memory/course-book/module-16-rc-weak-and-ownership-graphs/index.md)

## Continue

1. Complete the [Module 15 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 15 — Boxed Expression Tree](../../labs/module-05-boxed-expressions/README.md) from its public contract.
3. Apply the Module 15 increment in the [Memory Workspace engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
