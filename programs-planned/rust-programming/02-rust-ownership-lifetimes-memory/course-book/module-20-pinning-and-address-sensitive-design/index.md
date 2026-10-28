# 20 — Pinning and Address-Sensitive Design

**Course 2, day 10 · Module 20 of 90**  
`███████░░░░░░░░░░░░░` **20/90**

[← Module 19: Subtyping, Variance, PhantomData, and Drop Checking](../module-19-subtyping-variance-phantomdata-and-drop-checking/index.md) · [Course 2 overview](../index.md) · [Ninety-module map](../../../COURSE_MAP.md) · [Module 21: Traits as Behavioral Contracts →](../../../03-rust-traits-generics-architectural-design/course-book/module-21-traits-as-behavioral-contracts/index.md)

## The question

> What invariant becomes invalid after mechanical movement, who promises not to move the value, and can the design avoid address sensitivity entirely?

## Why this comes now

Pinning is last because it is frequently reached for before the problem is understood. Only after move semantics, indirection, destruction, representation, and variance are stable can address sensitivity be recognized honestly. The module teaches the contract, the projection hazards, and—equally important—the designs that avoid pinning entirely.

## What you will be able to do

- Distinguish ownership movement from mechanical relocation and identify genuine address-sensitive invariants.
- Explain Pin<P> as a contract on the pointee mediated by a pointer, not as a magical immovable allocation.
- Use Unpin and PhantomPinned correctly and construct pinned values without exposing moves after invariant activation.
- Reason about structural pinning, field projection, the drop guarantee, and why unsafe projection requires proof beyond compiler acceptance.
- Prefer handles, indices, owned indirection, scoped callbacks, or redesigned state when they eliminate self-reference or address dependence.

## Core model

### Mechanical movement versus ownership movement

Moving an owner variable does not necessarily relocate its pointee. Moving a `Box<T>` copies/transfers the box handle while the allocation normally remains at the same address. Moving a plain `T` may relocate its bytes. Pinning concerns the pointee's address-sensitive invariant, not whether a wrapper binding changes stack position.

Before using `Pin`, state the invariant:

```text
value type:
operation that activates address sensitivity:
which address/reference is stored or externally relied upon:
what relocation would invalidate:
who promises no relocation:
when the promise ends:
what Drop must preserve:
```

If these fields cannot be completed, pinning is likely ceremonial.

### Pin is a pointer-mediated contract

`Pin<P>` wraps a pointer-like `P` and restricts access to the pointee when the pointee is `!Unpin`. It does not freeze the `Pin` wrapper itself. It does not make every heap value immovable. For `T: Unpin`, pinning imposes no special movement restriction because `Pin<P>` can expose ordinary mutable access under the library contract.

`PhantomPinned` is a marker commonly used to opt a type out of automatic `Unpin`. It does not by itself pin an instance. The value becomes protected only after construction behind an appropriate pinned pointer and after the invariant is established through APIs that respect the contract.

### Safe construction order

A safe-facing address tracker can:

1. allocate the value in `Box<T>` with no active self-address invariant;
2. convert to `Pin<Box<T>>`;
3. initialize the self-address while accessed through a pinned mutable reference;
4. expose only pinned operations afterward;
5. keep fields private and avoid any safe method that moves/replaces the `!Unpin` value.

The lab stores an address token for diagnostic comparison; it does not promote raw self-pointers as a general architecture.

### Structural pinning and projection

Pinning a struct does not automatically pin every field in the same semantic way. A field may be structurally pinned if the type's contract promises it will not be moved before drop; other fields may remain movable. Safe projection from `Pin<&mut Struct>` to `Pin<&mut Field>` is nontrivial because the projection must uphold the parent type's pin contract and drop behavior.

Unsafe projection code needs a proof covering:

- the field is not moved by any safe method or Drop implementation;
- replacement/destructuring paths are controlled;
- the parent remains valid through drop;
- `Unpin` implementation/derivation matches the structural choice.

This course teaches audit literacy. Authoring general unsafe projection belongs to later advanced/unsafe courses.

### The drop guarantee

Once a value is pinned under an address-sensitive contract, it must remain valid at its location until its destructor runs or the storage is otherwise invalidated according to the pinning contract. Simply losing a `Pin<&mut T>` does not grant permission to move the still-live pointee. Pinning and destruction are linked because intrusive structures or self-references may rely on location until drop.

Leaks can prevent Drop, so designs must tolerate leak in the same sense required by the pin contract. Pin is not a universal cleanup guarantee.

### Prefer redesign when possible

Many apparent pinning needs can be removed by:

- storing byte ranges/indices rather than internal references;
- using generational handles;
- keeping owner and view separate;
- recomputing borrowed views;
- using scoped callbacks;
- placing independently owned nodes behind stable indirection without self-reference;
- using an ecosystem abstraction whose unsafe core is audited.

The `memory-workspace` capstone deliberately uses handles, owned edit candidates, `Rc` snapshots, and borrowed views. No invariant depends on a document object's address, so adding `Pin` would increase API burden without solving a real problem.

### Worked derivation: pinned tracker

A tracker stores payload plus `PhantomPinned` and a private optional address token. Before pinning, the token is absent, so ordinary movement is harmless. After `Pin<Box<Tracker>>` construction, a method taking `Pin<&mut Self>` records the pointee address. Later methods taking `Pin<&Self>` compare the current address. No safe method returns `&mut Self`, replaces the tracker, or moves fields declared structurally pinned.

The token is an educational assertion, not proof that all self-referential designs are sound. Real raw-pointer dereference would require unsafe validity and aliasing proofs beyond this course.

### Derive it yourself

A parser wants to store a buffer and slices into that buffer. Produce two designs: one using indices and ordinary ownership, one using a pinned self-reference. Compare construction, mutation, drop, projection, and unsafe proof burden. Select the simpler truthful design.

### Misconception clinic

- Moving `Pin<Box<T>>` moves the pointer wrapper, not necessarily the pinned pointee.
- Heap allocation alone is not pinning.
- `PhantomPinned` opts out of Unpin; it does not pin an instance.
- Pin is appropriate only when mechanical relocation would break a named invariant.

Rust's ordinary semantic move transfers ownership. For many types, it is irrelevant whether bytes are physically copied because validity depends only on value contents and ownership.

```rust
let first = String::from("text");
let second = first;
```

The `String` control value has moved semantically. The compiler may optimize physical copies. Its heap buffer may remain where it was, but no language promise says the `String` value itself has a stable address.

### Address-sensitive value

A value is address-sensitive when moving its storage after some initialization point would invalidate internal or external relationships. Examples include:

- a field holding a pointer into another field of the same object;
- an intrusive linked-list node registered by address;
- a state machine whose internal pointers refer into its own frame;
- a foreign subsystem retaining an address until explicit deregistration.

### Moving an owner handle

Moving `Box<T>` or `Rc<T>` usually moves only a pointer-like owner handle while the pointee allocation stays put. However, ordinary safe APIs may permit moving `T` out when uniqueness/ownership allows. Heap allocation alone is not a permanent no-move contract.

### Stable address begins at a point

Many types are freely movable before initialization establishes address-sensitive relationships, then must not move afterward. Pinning models this transition by restricting future safe access through a pinned pointer.

### Address versus identity

A domain ID does not require stable address. If relationships can use handles or ranges, the owner may move freely. Conversely, stable address should not become domain identity unless the product truly integrates with address-based infrastructure.

### Detecting unnecessary pinning

Ask:

- What stored relationship would become invalid on move?
- Can it be recomputed?
- Can it be represented as an index/range/handle?
- Can owner and view be separate values?
- Can a central arena provide stable lookup without stable addresses?

If no concrete invariant depends on address, `Pin` is not needed.

`Pin<P>` wraps a pointer-like type `P` and restricts access to its target so safe code cannot move an address-sensitive value after it has been pinned, unless the target implements `Unpin`.

Common forms include:

```text
Pin<&mut T>
Pin<&T>
Pin<Box<T>>
```

Pinning applies to the pointee reached through `P`, not to the `Pin` wrapper's own stack address. Moving `Pin<Box<T>>` is fine because the box handle moves while the pinned `T` remains in its allocation.

### Pin does not change layout

`Pin<P>` is an API contract wrapper. It does not add a hidden lock to the pointee or make memory read-only. Methods can still mutate fields when doing so does not move structurally pinned data.

### The pointer must uphold the promise

Constructing a pin for `!Unpin` data requires that the pointer's behavior and destruction respect stable address. Safe constructors such as `Box::pin` provide this. Creating an arbitrary `Pin<&mut T>` with unchecked APIs is unsafe because the caller must prove the referent will not later move before drop.

### Shared pinned access

`Pin<&T>` provides shared access. `get_ref` exposes `&T`, which cannot move the value. This is always safe.

### Mutable pinned access

`Pin<&mut T>` permits mutation through methods that preserve pinning. Obtaining an unrestricted `&mut T` would allow `mem::replace` and move the old value, so `get_mut` is available safely only when `T: Unpin`.

For `!Unpin` types, methods accept `self: Pin<&mut Self>` and manually restrict operations to pin-safe field changes.

### Pin is not lifetime extension

A pinned reference still has a lifetime. `Pin<&mut T>` cannot outlive the borrowed storage. Pinning prevents move during validity; it does not make a stack local `'static`.

### Pin is not ownership

`Pin<&mut T>` borrows. `Pin<Box<T>>` owns. The same pinning contract can sit over different pointer topologies. Always analyze both ownership and pinning.

Most Rust types implement the auto trait `Unpin`. For them, pinning imposes no additional move restriction: safe code may obtain ordinary mutable access through a pinned pointer.

This is correct because those types do not rely on stable address for validity.

### `Unpin` is about the pointee, not pointer placement

A type can contain heap allocations and still be `Unpin`; moving its control value does not invalidate it. A small inline type can be `!Unpin` if it establishes self-address relationships.

### Opting out with `PhantomPinned`

```rust
use std::marker::PhantomPinned;

struct AddressSensitive {
    label: String,
    _pin: PhantomPinned,
}
```

`PhantomPinned` prevents automatic `Unpin`. It does not by itself create a self-reference or make constructors safe. It only tells pin APIs that unrestricted moving access must not be granted.

### Structural composition

A struct is generally `Unpin` when its fields are `Unpin`, unless it opts out. Pointer wrappers often implement `Unpin` based on their own semantics rather than pointee, which is why exact standard-library trait implementations matter.

### Manual `Unpin`

Implementing `Unpin` is safe syntax but a serious semantic promise: moving the type is valid. For address-sensitive types, an incorrect implementation defeats pinning. This course does not manually implement `Unpin` for such types.

### Negative reasoning

If a type contains `PhantomPinned` but no invariant depends on address, the marker adds restrictions without value. Reviewers should demand the exact post-initialization relationship.

### Lifecycle phases

A good design documents:

1. movable construction state;
2. pinning operation;
3. initialization of address-sensitive links through pinned access;
4. permitted pinned methods;
5. destruction at the pinned address.

Skipping phase boundaries is a common source of unsound unsafe code.

### Heap pinning

```rust
use std::pin::Pin;

let pinned: Pin<Box<String>> = Box::pin(String::from("movable type"));
```

`String: Unpin`, so the pin does not restrict moving the `String` semantically through safe APIs once ownership access allows. The same constructor becomes meaningful for a `!Unpin` type.

### Stack pinning

The `pin!` macro creates pinned storage in the current scope:

```rust
use std::pin::pin;

let mut value = pin!(AddressSensitive::new("local"));
value.as_mut().initialize();
```

The pinned reference cannot escape the stack storage lifetime. Moving the `Pin<&mut T>` handle is fine; moving the referent through it is restricted.

### Reborrowing pins

`as_ref` creates `Pin<&T>`; `as_mut` creates a shorter `Pin<&mut T>` reborrow. Use them instead of consuming the original pin when making repeated calls.

```rust
let address = value.as_ref().address();
value.as_mut().record();
```

### Access for `Unpin`

For `T: Unpin`, `Pin<&mut T>::get_mut` is safe because moving `T` cannot violate an address invariant. For `!Unpin`, only shared `get_ref` is directly available; mutable methods must operate through pinned receivers.

### `Pin::new`

Safe `Pin::new(pointer)` requires the target to be `Unpin` in cases where the pointer would otherwise not guarantee pinning. Use safe owning constructors for `!Unpin` values.

### Dropping the pin handle

Dropping `Pin<Box<T>>` drops the pinned `T` in place and deallocates afterward. Dropping a `Pin<&mut T>` ends the borrow; the underlying owner remains responsible for respecting the pinning promise for the rest of the value's lifetime.

This is why unchecked temporary pin creation can be unsound: after the pin reference ends, ordinary owner access might move the value.

### Lab rule

The lab constructs `!Unpin` values only with `Box::pin` or `pin!`. It never invokes unchecked pin constructors.

Given `Pin<&mut Outer>`, obtaining `Pin<&mut Field>` is called pin projection. It is not automatically safe for every field because moving or replacing the field may or may not violate `Outer`'s pinning invariant.

### Structurally pinned field

A field is structurally pinned when pinning the outer value promises that the field will not move until it is dropped. Safe APIs must expose it only as pinned access.

### Unpinned field

Other fields may be replaceable even while the outer object is pinned. For example, a counter or label may not participate in address sensitivity. A pinned method can update such fields if it can reach them safely without moving the pinned structure.

### Why ordinary field syntax is restricted

An unrestricted `&mut Outer` would allow:

```rust
let old = std::mem::replace(&mut outer.field, new_field);
```

If `field` is structurally pinned, this mechanically moves the old field. Therefore projection requires a proof about each field and the outer destructor.

### Unsafe projection primitives

The standard library exposes unchecked mapping methods whose caller must prove soundness. Procedural projection crates can generate reviewed unsafe code. Both belong to Course 5/6 implementation work. This course only audits supplied code and uses safe methods that do not require pinned field projection.

### Encapsulation

A `!Unpin` type should keep fields private and expose methods with pinned receivers. Public fields let callers attempt operations the abstraction cannot control through other ownership paths.

### `Drop` and projection

If a field is structurally pinned, the destructor must not move it before it is dropped. Ordinary pattern moves or `mem::take` can violate the invariant. Pinned drop projection requires additional care and often generated/unsafe support.

### Design alternative

If projection complexity dominates, store address-sensitive components in their own `Pin<Box<Field>>` and let the outer container remain movable. This separates invariants at allocation boundaries, though it adds allocations.

### Review statement

For every field of a `!Unpin` type, label it:

- structurally pinned;
- freely replaceable under pin;
- derived pointer/metadata;
- marker.

Without this table, a projection implementation is unauditable.

Pinning's usefulness depends not only on “do not move” but also on the pinned storage remaining valid until destruction completes. Address-sensitive neighbors or external systems may rely on receiving notice before storage is reused or invalidated.

### In-place destruction

A pinned value must be dropped at its pinned location before the storage is reused or deallocated, unless it is deliberately leaked. The pointer owner must uphold this when it releases storage.

`Pin<Box<T>>` does: dropping the box runs `T`'s destructor in place, then deallocates.

### Overwrite

Replacing a pinned value must first drop the old value in place rather than move it out. Safe pin APIs provide only operations consistent with this contract.

### Leaks remain possible

As with ordinary `Drop`, safe Rust can leak a pinned value. Pinning's contract allows non-destruction through leaking; what is forbidden is moving/reusing storage while pretending the pinned relationship remains valid.

### Intrusive structures

An intrusive node may be linked by address into neighbors. Its destructor must unlink before storage disappears. If destructor execution can be skipped by leak, the node/storage also remains, so pointers are not dangling; logical resources may still leak.

### Panic in pinned destructor

The same double-panic concerns apply. A destructor that must repair external pointer relationships should avoid panicking and be designed around infallible local operations.

### Stack pinning lifetime

A stack-pinned value is destroyed before its stack storage is reclaimed under normal scope exit/unwinding. Abort can skip destructors, but the process also ceases to use the addresses. Cross-process/external durable registrations need separate cleanup guarantees.

Pinning can support self-referential structures, but it does not remove initialization and projection hazards.

### Two-phase construction

A typical self-referential design needs:

1. allocate/construct fields without internal references;
2. pin the value so its address will remain stable;
3. initialize internal pointers using pinned access;
4. prevent mutation that reallocates/moves referents;
5. drop internal relationships in place.

Safe Rust cannot generally store a normal reference with a lifetime tied to the same owning object because the type system cannot express the self-borrow directly. Implementations use raw pointers internally and unsafe invariants—reserved for Course 6.

### Backing allocation may move internally

Even if the outer struct is pinned, a `String` field can reallocate its buffer when mutated. A pointer into that buffer becomes invalid. Pinning the outer struct does not pin separately allocated buffer contents against reallocation.

This is a critical correction to simplistic self-reference examples.

### Better representations

- store byte ranges into `String` and revalidate after mutation;
- freeze text into `Box<str>` before taking views;
- separate owner and borrowed view;
- use `Rc<str>` with ranges for shared immutable backing;
- use generational handles into centralized storage;
- recompute derived references.

### Futures motivation

Compiler-generated async state machines may contain references between fields after they have begun execution. Polling uses pinned receivers so the future's frame is not moved after such relationships can form. Async semantics belong to Course 8; this is the memory reason `Pin<&mut Self>` appears in `Future::poll`.

### Do not pin the capstone

`memory-workspace` stores text, ranges, handles, snapshots, and caches without internal pointers. Strings may reallocate safely because ranges are validated against revisions. Pinning would add restrictions without protecting a real invariant.

Recognizing that non-use is part of mastery.

This course includes one isolated case study with a small unsafe self-referential type. Do not extend it. The audit method is the deliverable.

### Course rule

If the audit cannot establish every obligation, reject the abstraction and use an alternative representation. “It did not crash” is not evidence of soundness.

The final review treats the capstone as one system.

### Ownership topology

- workspace owns slots;
- live slot owns document;
- handles are non-owning index/generation evidence;
- edit sessions own staged copies;
- snapshot cache and consumers strongly own immutable snapshots;
- watchers are weak;
- caches are interior derived state.

### Lifetime surface

- views borrow workspace/document;
- iterators keep immutable borrows active;
- scoped callbacks prevent temporary normalization views escaping;
- durable operations use handles and ranges.

### Cleanup surface

- ordinary owners reclaim memory;
- staged sessions discard on drop;
- no custom destructor performs fallible work;
- reference-count topology has no cycles.

### Representation surface

- live text uses growable `String`;
- immutable snapshots use fixed `Box<str>` inside shared `Rc`;
- memory reports distinguish control/payload and observations/guarantees;
- no raw layout persistence exists.

### Variance/marker surface

- reference-bearing views get relationships from real fields;
- runtime handles carry no artificial lifetimes;
- optional type-state markers encode session protocol only;
- no marker is selected without a variance statement.

### Pinning surface

No stored relationship depends on an object's address. Moving workspace/document control values is semantically valid. String-buffer reallocation is handled through revision invalidation. Therefore the production capstone deliberately does not use `Pin`.

### Final proof

You must defend one rejected alternative in each category: clone-heavy borrowing, one-lifetime API, leaked/static scratch, broad guard, boxes everywhere, strong cycle, `Rc<RefCell>` live model, raw-layout report, covariant mutable marker, and unnecessary pinning.

A device API requires an object address to remain stable from registration until deregistration. To study the safe-facing contract without FFI, the lab stores a `NonNull<Self>` address token and compares it on observation; it never dereferences the pointer.

### Type state

```rust
struct Tracker {
    label: String,
    registered_at: Cell<Option<NonNull<Tracker>>>,
    observations: Cell<u64>,
    _pin: PhantomPinned,
}
```

Before initialization, movement is harmless because no address relation exists. After pinning and initialization, the stored token must equal the current address for every observation.

### Construction

`Tracker::new` returns an ordinary unpinned value. Caller chooses `Box::pin` or scoped stack `pin!`. Initialization receives `Pin<&Self>`:

```text
obtain address from pinned shared reference
if uninitialized, store token
if initialized, verify same token or return error
```

No raw dereference is needed. `NonNull::from(self.get_ref())` obtains the token safely.

### Why `Cell`

Address token and count are copyable. Methods can take `Pin<&Self>` and mutate cells without exposing `&mut Self`. This does not make address stability; pinning plus `!Unpin` does.

### Safe movement restrictions

Because `PhantomPinned` makes the type `!Unpin`, safe code cannot call `Pin::get_mut` on `Pin<&mut Tracker>` or move the value out. A compile-fail specimen preserves that fact. Before pinning, the value may move freely because the invariant is not yet active.

### What the lab does not prove

It does not implement a self-reference, dereference stored pointers, interact with an external registry, or provide unsafe projection. It demonstrates initialization timing and the safe API surface.

### Field movement

The `String` field's owner resides inside the pinned struct, but its heap buffer can reallocate if mutated. The lab does not store a pointer into that buffer. A real self-reference would have to restrict buffer-changing operations separately.

### Drop

The address token becomes irrelevant as destruction begins. No external system can call back, so no custom drop is required. A real registration would need deregistration ordering and panic/abort policy.

### Alternative design

The capstone uses handles and offsets, so pinning is rejected. If logical identity suffices, a pinned tracker is unnecessary. You must be able to remove `Pin` from designs without address-sensitive state.

## Use the idea in a complete program

The course capstone is **Memory Workspace**, an in-memory document workspace with handles, snapshots, edit sessions, and caches. Conduct an address-sensitivity review and reject pinning unless an invariant truly depends on stable location. Defend the simpler architecture when handles and indirection suffice. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-10-pinned-tracker/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 21 when you can:

- answer the module question—“What invariant becomes invalid after mechanical movement, who promises not to move the value, and can the design avoid address sensitivity entirely?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Distinguish ownership movement from mechanical relocation and identify genuine address-sensitive invariants;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [std::pin](https://doc.rust-lang.org/std/pin/)
- [Pin](https://doc.rust-lang.org/std/pin/struct.Pin.html)
- [Unpin](https://doc.rust-lang.org/std/marker/trait.Unpin.html)

[← Module 19](../../../02-rust-ownership-lifetimes-memory/course-book/module-19-subtyping-variance-phantomdata-and-drop-checking/index.md) · [ninety-module map](../../../COURSE_MAP.md) · [Module 21 →](../../../03-rust-traits-generics-architectural-design/course-book/module-21-traits-as-behavioral-contracts/index.md)

## Continue

1. Complete the [Module 20 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 20 — Pinned Tracker](../../labs/module-10-pinned-tracker/README.md) from its public contract.
3. Apply the Module 20 increment in the [Memory Workspace engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
