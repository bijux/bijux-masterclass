# Module 94 — Const Generics, Witness Types, and Compile-Time Invariants

**Course 10 · Day 4 · Module 94 of 100**
`████████████████████████░` **94/100**

[Program](../../../README.md) · [Course 10](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-04-bounded-matrix/README.md) · [AxiomStore guide](../capstone.md)

[← Module 93: GATs, Higher-Ranked Bounds, and Lending Interfaces](../module-93-gats-higher-ranked-bounds-and-lending-interfaces/index.md) · [Module 95: Opaque and Erased Types: impl Trait, dyn Trait, Any, and Plugin Boundaries →](../module-95-opaque-and-erased-types-impl-trait-dyn-trait-any-and-plugin-boundaries/index.md)

## The question

> Which numeric and state facts belong in types, which remain runtime data, and how do you avoid turning a library into an unusable type-level calculator?

## Why this comes now

Rust can parameterize types by constants, allowing array dimensions, inline capacities, and fixed protocol widths to participate in type identity. Newtypes and unconstructible fields can act as witnesses that validation has occurred. These tools can eliminate whole classes of mismatch, but they also multiply monomorphized types, complicate inference, and cannot express every arithmetic relation on stable Rust. Module 94 teaches restraint: encode facts that are stable, local, and valuable to downstream composition; validate the rest at runtime with equally explicit types.

Course 1 used arrays and newtypes; Course 6 distinguished representation from runtime policy; Course 9 measured code-size cost. This module decides which numeric facts deserve type identity.

Const generics are useful when a value changes type-level composition or storage, not merely because the value is known. This module forces a three-way split: facts encoded in type identity, facts validated once and carried by a witness, and policies that must remain runtime data. The quality of the design depends more on that split than on the number of const parameters.

### Prerequisite bridge

Module 93 established **GATs, Higher-Ranked Bounds, and Lending Interfaces**. Before continuing, verify that you can choose between lending, ownership transfer, callback-based access, and copied values according to retention needs. This module preserves that capability and adds the ability to use const parameters when a numeric fact changes representation, layout, or legal composition. Module 95, **Opaque and Erased Types: impl Trait, dyn Trait, Any, and Plugin Boundaries**, will rely on both when it asks: *When should an API hide one concrete type, erase many concrete types behind a contract, or preserve explicit variants—and what information is lost at each boundary?*

### Scope boundary

This module owns the reasoning for **const generics, witness types, and compile-time invariants** inside Course 10. The course selects stable mechanisms that serve real product requirements. It does not reward obscure syntax, nightly-feature collecting, unsafe code retained for display, or lower-level compiler output used where source-level reasoning is already decisive. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

After completing this module, you will be able to:

- use const parameters when a numeric fact changes representation, layout, or legal composition
- construct witness types only through checked functions and preserve their proof through private fields
- distinguish compile-time capacity from runtime length and enforce both without off-by-one ambiguity
- design APIs that compose equal dimensions while rejecting mismatched shapes before execution
- recognize code-size, inference, ergonomics, and semver costs created by excessive const parameterization
- choose runtime validation when the value is data-dependent, frequently changing, or not worth a new type identity

## Core model

### The governing model

Use a **static/dynamic invariant table**. For each number or state, record whether it changes layout, legal method composition, runtime occupancy, external configuration, or compatibility. A const parameter earns its place only when downstream code composes on the fact; a witness earns its place when validated evidence must travel without exposing a forgeable field.

### 1. Const parameters make selected values part of type identity

`Matrix<T, 3, 4>` and `Matrix<T, 4, 3>` are different types. That distinction is useful when shape changes which operations are legal or how storage is represented. It is less useful when dimensions are loaded from a file and vary for every request. A const parameter should buy a real compile-time composition rule, not merely move a runtime number into angle brackets.

**Ask whether identity changes.** Would `Matrix<T, 2, 3>` and `Matrix<T, 3, 2>` require different legal operations, or merely different runtime values?

### 2. Capacity and length are different facts

An inline collection with capacity `N` still has a runtime length from zero through `N`. The const parameter controls storage and maximum occupancy; it does not prove that every slot is initialized. The implementation must track initialized length and preserve it through push, pop, clear, move, panic, and drop. Confusing capacity with initialization is a soundness defect when raw storage is involved and a logic defect even in safe arrays.

**Separate capacity from occupancy.** For `InlineBatch<T, N>`, list what `N` proves and what the runtime `len` must still prove.

### 3. Witness types carry validated evidence

A `BoundedIndex<N>` constructed only after `value < N` means later indexing can rely on that checked fact. The field must remain private so callers cannot forge the witness. The witness should expose the minimum required observation, such as `get()`, without promising more. This pattern scales beyond numbers: validated identifiers, negotiated versions, open sessions, and committed transactions can all carry evidence through type identity.

**Protect the witness.** Explain why `pub struct BoundedIndex<const N: usize>(pub usize)` destroys the evidence carried by construction.

### 4. Compile-time arithmetic has practical boundaries

Many useful relations—nonzero sizes, products that do not overflow, one dimension equal to another—cannot always be expressed ergonomically in stable generic signatures. Do not hide unstable assumptions behind clever marker arrays. Validate complex arithmetic in constructors, store the checked result, and document the distinction between type-level equality and runtime arithmetic safety. A hybrid design is often clearer than forcing every fact into the type system.

**Handle zero deliberately.** For `N = 0`, state which methods remain meaningful and which assumptions about indexing or allocation must be rejected.

### 5. Monomorphization is an architectural cost

Each distinct const instantiation can produce separate code after monomorphization. A handful of capacities may be harmless; accepting arbitrary public const values can increase compile time and binary size. Measure the artifact in Course 9’s terms. If behavior is identical and only capacity varies, consider one dynamic implementation behind a small generic wrapper or a runtime capacity with bounded allocation.

**Constrain arithmetic claims.** If `R * C` can overflow `usize`, decide whether the relation belongs in stable const expressions or a checked constructor.

### 6. Public const parameters are compatibility commitments

Adding, reordering, or changing the meaning of a const parameter affects downstream type names and inference. Default const parameters can ease some evolution but do not erase semantic commitments. Keep representation constants private when callers do not need to compose on them. Expose a type-level number only when downstream code benefits from the proof.

**Count instantiations.** List the public const values likely to appear in a real program and the potential code-size/compile-time consequence.

### 7. Witnesses do not replace runtime policy

A type can prove that an index is below `N`; it cannot prove that a user is authorized to access the indexed record or that the record remains current after a generation change. Combine local structural witnesses with runtime identity, version, and policy checks. The strongest design gives each mechanism one fact to own.

**Preserve runtime policy.** Explain why archive record count, format version, and user-selected limits should not automatically become const parameters.

### Worked boundary analysis: fixed transaction capacity

AxiomStore’s `Transaction<'_, MAX_RECORD, TX_CAP>` uses `TX_CAP` to determine inline storage. That makes two facts easy to confuse:

```text
TX_CAP = number of slots physically available
len    = number of slots currently initialized
```

The type system distinguishes `Transaction<_, 8>` from `Transaction<_, 32>`, but it does not know whether either transaction currently contains zero, five, or all available operations. `InlineBatch` must preserve `0 <= len <= TX_CAP`, and its unsafe proof must concern the initialized prefix, not the const parameter alone.

Would `TX_CAP` be better as runtime data? If the implementation used `Vec<Operation>`, callers could configure arbitrary capacities without generating a new type for each value. The const-generic design earns its complexity only if inline representation and bounded stack-local storage are product requirements. If those requirements disappear, type identity becomes unnecessary compatibility and monomorphization cost.

Now consider `MAX_RECORD`. It affects which archives a concrete store instance can open, so exposing many different values can create surprising incompatibility between otherwise similar stores. The capstone uses defaults and keeps codec internals private, but a production library would need to decide whether the limit is a format property, a deployment policy, or an implementation budget. A format property belongs in versioned bytes; a deployment policy usually belongs in runtime configuration; an implementation budget may be a private const or internal specialization.

Witness types solve a different problem. `BoundedIndex<N>` carries evidence about one validated runtime value. It should not be confused with a const parameter that determines storage. This distinction—type identity, validated runtime witness, mutable runtime state—is the core of the module.

### A decision table

| Design question | Principled evidence or mechanism | Weak substitute to reject |
|---|---|---|
| Does the value alter representation or legal composition? | const generic or witness type | runtime integer passed everywhere |
| Is the value loaded from data and frequently variable? | runtime validation and private checked state | unbounded public const instantiations |
| Is a slot initialized? | runtime length and transition invariant | capacity as a false initialization proof |
| Do callers need the proof in their types? | public witness with private construction | private type-level complexity leaking without compositional benefit |

### A rigorous working procedure

1. Inventory every numeric or state fact in the API.
2. Classify each as layout, type composition, validated witness, runtime occupancy, or external policy.
3. Make fields of witness types private and expose only observations required by consumers.
4. Define zero, maximum, and overflow behavior before implementing generic methods.
5. Compare the generic design with one runtime-capacity design and one hybrid wrapper.
6. Record public type-identity and monomorphization consequences before stabilizing the API.

### Failure patterns and principled repairs

Const-generic designs fail when a number is used decoratively rather than connected to construction, layout, or a method's availability. Repair the API by deciding which limit is part of type identity, which must remain a runtime policy, and which proof belongs in a private constructor or witness type.

### Encoding configuration as type identity

Keep deployment- or file-selected values as checked runtime data unless representation genuinely differs.

### Forging a witness through a public tuple field

Make fields private and expose one checked constructor.

### Assuming `N > 0` without expressing or validating it

Define the empty case or reject it in a constructor whose result carries the proof.

### Ignoring monomorphization and semver cost

Bound the supported const family and measure representative artifact size and compile time.

### What the compiler cannot decide for you

Const generics can reject incompatible shapes and make selected capacities part of type identity. They do not prove that all slots are initialized, that arithmetic cannot overflow, that a record is authorized, or that a particular public set of const values is operationally wise. Witness types carry evidence only if construction is controlled.

A mature design uses type-level numbers sparingly. If callers do not need to compose on the number, a checked runtime value is usually easier to evolve and cheaper to instantiate.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For use const parameters when a numeric fact changes representation, layout, or legal composition, construct one positive and one causal negative example. Mark the first decisive fact in the **const witness proof** and state which evidence could falsify the claim.

2. **Outcome 2.** For construct witness types only through checked functions and preserve their proof through private fields, construct one positive and one causal negative example. Mark the first decisive fact in the **const witness proof** and state which evidence could falsify the claim.

3. **Outcome 3.** For distinguish compile-time capacity from runtime length and enforce both without off-by-one ambiguity, construct one positive and one causal negative example. Mark the first decisive fact in the **const witness proof** and state which evidence could falsify the claim.

4. **Outcome 4.** For design APIs that compose equal dimensions while rejecting mismatched shapes before execution, construct one positive and one causal negative example. Mark the first decisive fact in the **const witness proof** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

Read `BoundedIndex<N>` as a proof object: construction validates `value < N`, and the private field prevents forgery. Then inspect `Matrix<T, R, C>` and identify which shape relationships are enforced by method signatures and which arithmetic facts remain runtime concerns.

```rust
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct BoundedIndex<const N: usize>(usize);

impl<const N: usize> BoundedIndex<N> {
    fn new(value: usize) -> Option<Self> {
        (value < N).then_some(Self(value))
    }

    fn get(self) -> usize {
        self.0
    }
}

struct Matrix<T, const ROWS: usize, const COLS: usize> {
    cells: [[T; COLS]; ROWS],
}

impl<T, const R: usize, const C: usize> Matrix<T, R, C> {
    fn get(&self, row: BoundedIndex<R>, col: BoundedIndex<C>) -> &T {
        &self.cells[row.get()][col.get()]
    }
}
```

### Trace the example

For `Matrix<T, R, C>::get`, follow the evidence from `BoundedIndex::new` to array indexing. Explain why the bounds check has already occurred semantically even if a compiler may still retain or eliminate machine checks. Next, design multiplication `Matrix<T, R, K> × Matrix<T, K, C>` and identify the type equality that makes composition legal.

Now replace `R` and `C` with runtime fields. List what compile-time rejection is lost, what dynamic flexibility is gained, and whether the product actually needs arbitrary dimensions. The correct answer may be the runtime design.

### Use it in AxiomStore

AxiomStore uses const generics for the maximum encoded record size and transaction batch capacity because those values determine inline representation and legal local operations. Runtime archive limits, schema versions, record counts, and migration policies remain checked data. The course makes that separation visible so a configurable product does not become a combinatorial family of incompatible types.

AxiomStore’s const-boundary record is:

```text
fact
why callers compose on it
layout or method effect
runtime state still required
zero and maximum behavior
public compatibility cost
expected instantiation set
simpler dynamic alternative
```

Apply it separately to maximum encoded record size and inline transaction capacity. Keep archive count, current transaction length, format version, and migration policy as runtime facts.

## Practice sequence

1. **Witness construction.** Implement a nonforgeable `BoundedIndex<N>` and prove the first invalid value is rejected for `N = 0`, `1`, and a larger bound.
2. **Shape composition.** Implement matrix multiplication whose inner dimension equality is expressed by the types.
3. **Overflow boundary.** Add a checked constructor for a runtime matrix and demonstrate why stable const arithmetic is not the right owner of every size calculation.
4. **Capacity audit.** Model `N` and `len` separately for a fixed-capacity collection; write the complete state range.
5. **Instantiation budget.** Compare three fixed capacities with a publicly arbitrary const value and write a compatibility/code-size decision.

Complete the [workbook](workbook.md) and [Bounded Matrix](../../labs/module-04-bounded-matrix/README.md). Every compiler case must state whether the rejected fact is type identity, witness construction, or merely a runtime policy that the compiler cannot know.

## Ready to continue

Continue when you can defend each const parameter with a downstream composition benefit, keep occupancy separate from capacity, design an unforgeable witness, and reject an over-generic API when dynamic data is the real requirement. You should be able to explain zero-capacity behavior without hand-waving.

## Primary Rust references

- The Rust Reference: const parameters
- The standard library array and MaybeUninit documentation
- Cargo and rustc material on monomorphization and code-size observation

Const-generic syntax evolves, so verify exact stable expression rules against the Reference for the pinned toolchain. Keep arithmetic safety and API policy outside claims the type system does not make.

## Continue

Continue to [Module 95 — Opaque and Erased Types: impl Trait, dyn Trait, Any, and Plugin Boundaries](../module-95-opaque-and-erased-types-impl-trait-dyn-trait-any-and-plugin-boundaries/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
