# Workbook — Module 18: Memory Representation, Validity, and Layout

[Chapter](index.md) · [Laboratory](../../labs/module-08-layout-observatory/README.md) · [Memory Workspace guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Memory Representation, Validity, and Layout** has become a usable model rather than remembered vocabulary. Its governing question is: *Is a claim a language guarantee, a standard-library contract, a target-conditioned fact, a current observation, or an unsupported assumption?* Preserve your first prediction and record decisive facts in a **representation table**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 17 — Interior Mutability and Runtime Borrows that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **Is a claim a language guarantee, a standard-library contract, a target-conditioned fact, a current observation, or an unsupported assumption?**
3. Draw the smallest **representation table** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Memory Representation, Validity, and Layout** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-repr-c-layout.rs`](../../compiler-labs/module-08/01-repr-c-layout.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-default-layout-observation.rs`](../../compiler-labs/module-08/02-default-layout-observation.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-unsized-local.rs`](../../compiler-labs/module-08/03-unsized-local.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-size-of-val-slice.rs`](../../compiler-labs/module-08/04-size-of-val-slice.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-owner-versus-payload.rs`](../../compiler-labs/module-08/05-owner-versus-payload.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-zero-sized-values.rs`](../../compiler-labs/module-08/06-zero-sized-values.rs) | Pass or fail? What exact rule decides? |
| 7 | [`07-option-size-observations.rs`](../../compiler-labs/module-08/07-option-size-observations.rs) | Pass or fail? What exact rule decides? |
| 8 | [`08-transmute-requires-unsafe.rs`](../../compiler-labs/module-08/08-transmute-requires-unsafe.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 02-rust-ownership-lifetimes-memory
```

## Part 2 — Diagnose and repair

A program writes `size_of::<Header>()` bytes copied from a Rust struct and later reads them back as the same type. It uses default representation, contains a `String`, assumes little endian, and treats an enum discriminant as one byte.

### Defects

- pointer/control bytes are persisted instead of string contents;
- padding is copied;
- default field order/enum encoding is assumed;
- addresses are meaningless in another process;
- invalid input can create invalid Rust values;
- no version or length limits exist.

### Repair

Design an explicit versioned codec with fixed integer encodings, length-prefixed UTF-8, declared enum codes, bounds checks, and unknown-field/version errors. Keep `repr` decisions separate from persistence.

## Part 3 — Focused exercises

### Access protocol

Attempt every required exercise and commit the attempt before opening `exercise-answers.md`. Mark each as:

1. Build a guarantee ledger for ten size/alignment claims on your target.
2. Calculate a `repr(C)` struct's expected padding from target primitive alignments and verify.
3. Observe default-layout field addresses without asserting source order as portable.
4. Compare owner size, length, capacity, and payload bytes for `String`, `Vec`, `Box<[T]>`, and `Rc<str>`.
5. Use `size_of_val` on slices, str, and a trait-object reference; explain metadata.
6. Observe `Option` sizes for references, nonzero integers, and ordinary integers; classify guarantees.
7. Explore ZST arrays and vectors without treating addresses as identity.
8. Design a `repr(transparent)` ID and explain what it does not guarantee.
9. Replace a memory-copy serializer with explicit encoding.
10. Create a capstone memory report with approximation labels and shared-allocation deduplication.

### Interleaved reasoning pass

1. For **Separate semantic value, validity invariant, abstract layout guarantee, ABI promise, and measured observation**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the representation table.
2. For **Reason about size, alignment, padding, field non-overlap, repr(Rust), repr(C), and repr(transparent) without overclaiming offsets**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the representation table.
3. For **Explain thin and wide pointers, metadata, slices, str, trait-object previews, and unsized tails**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the representation table.
4. For **Classify enum discriminant and niche claims by documented guarantees rather than pattern extrapolation**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the representation table.

5. Identify one guarantee from an earlier course that a careless implementation of **Memory Representation, Validity, and Layout** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build a safe executable/library that records layout observations while refusing to present them as universal guarantees.

```text
labs/module-08-layout-observatory/
├── starter/
└── solution/
```

### Required experiments

- primitive, array, tuple, and struct size/alignment;
- one `repr(C)` padding calculation;
- one `repr(transparent)` newtype;
- thin and wide pointer observations;
- `size_of_val` for slices and strings;
- `String`, `Vec`, `Box<[T]>`, and `Rc<str>` owner/payload distinctions;
- `Option` size observations with guarantee labels;
- zero-sized types and logical collection length.

### Output model

Each row contains claim, observed value, classification (`Guaranteed` or `Observed`), target architecture, and explanatory note. Tests assert semantic/guaranteed relationships only; observed exact sizes are snapshot output, not portable pass conditions unless target-gated explicitly.

### Prohibitions

No unsafe blocks, transmute, raw byte reads, field-offset macros, or serialization from memory representation.

### Acceptance

```bash
cargo test -p rust-olm-lab-08-layout-observatory --all-targets
cargo clippy -p rust-olm-lab-08-layout-observatory --all-targets -- -D warnings
```

### Report architecture

Represent classification in the type system rather than embedding words in free-form notes:

```rust
pub enum ClaimClass {
    Guaranteed,
    TargetConditioned,
    Observed,
}
```

Each observation records a stable claim identifier, measured values, the classification, target metadata available from safe standard APIs or compile-time configuration, and a concise rationale. Rendering must be deterministic so two reports from the same executable can be compared. Exact observed sizes must not become unconditional tests.

For the `repr(C)` specimen, calculate expected offsets on the active target from field size and alignment, then compare the resulting total size and alignment. Because safe Rust cannot directly read field offsets without additional facilities, do not pretend to verify each offset. State the boundary precisely. For default `repr(Rust)` structs, record size and alignment only as observations and never infer declaration-order offsets.

### Owner versus payload worksheet

For `String`, `Vec<u32>`, `Box<[u32]>`, and `Rc<str>`, report separately:

- inline owner or handle bytes;
- logical payload length;
- exposed capacity where the API provides one;
- whether payload ownership is exclusive or shared;
- whether multiple handles may refer to one allocation;
- what allocator overhead is excluded.

Use `size_of_val` on dynamically sized referents and explain why a wide reference remains a sized value even though its referent is not `Sized`.

### Acceptance checks
Tests must establish general relationships—alignment is nonzero and a power of two, array size scales by element count when arithmetic fits, transparent wrappers match the represented field under the documented conditions, and slice `size_of_val` reflects length. Generate a human-readable observation report as an artifact, but mark target-specific snapshots as informational. Include a paragraph rejecting direct memory serialization and explaining the separate semantic codec that would be required.

### Tiered hints

Do not open a later tier until the previous tier has produced a written attempt.

- **Hint 1 — concept:** return to the governing question: Is a claim a language guarantee, a standard-library contract, a target-conditioned fact, a current observation, or an unsupported assumption?
- **Hint 2 — topology:** draw owners/borrows/states/errors before changing syntax; identify the one boundary that should own the invariant.
- **Hint 3 — structure:** separate validation from mutation and pure transformation from effects. Use the standard operation that encodes the safety fact before inventing an abstraction.
- **Hint 4 — implementation-adjacent:** consult only the relevant standard-library or Reference page; do not open `solution/src`.

The executable starter and reference implementation are in [module-08-layout-observatory](../../labs/module-08-layout-observatory/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

### Laboratory acceptance trace

Before opening the reference implementation for **Layout Observatory**, record:

- the public behavior that demonstrates **Separate semantic value, validity invariant, abstract layout guarantee, ABI promise, and measured observation**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

### Outcomes mapped

- Separate semantic value, validity invariant, abstract layout guarantee, ABI promise, and measured observation.
- Reason about size, alignment, padding, field non-overlap, repr(Rust), repr(C), and repr(transparent) without overclaiming offsets.
- Explain thin and wide pointers, metadata, slices, str, trait-object previews, and unsized tails.
- Classify enum discriminant and niche claims by documented guarantees rather than pattern extrapolation.
- Build memory reports that distinguish inline size, length, capacity, shared allocation deduplication, allocator overhead, and exclusions.

Add `Workspace::memory_report()` and a CLI command that reports:

- live document count and logical UTF-8 bytes;
- title/text capacities for live editable strings;
- cache payload lengths;
- snapshot count by handle/revision;
- unique shared snapshot allocation count using process-local `Rc::ptr_eq` grouping;
- observed inline owner sizes for relevant types;
- explicit exclusions: allocator metadata, executable code, stack frames, and standard-library private bookkeeping.

Do not use pointer addresses as persistent identifiers. Do not serialize raw values. Label every exact size as observed on the current target/toolchain. Tests verify arithmetic consistency and shared-snapshot deduplication, not universal byte constants.

### Capstone defense

Review a binary protocol that writes Rust values directly; replace layout assumptions with an explicit codec and evidence taxonomy.

### Capstone invariant trace

For the Module 18 Memory Workspace increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Complete this checkpoint closed-book. Compiler access is allowed only after the prediction portion has been committed.

### Outcome reconstruction

For each outcome, write a claim, one example, one non-example, and one limitation.

Without reopening the chapter, reconstruct the outcomes for **Module 18: Memory Representation, Validity, and Layout**. Compare your list with the earlier outcome map only after writing it, then mark each item as modelled, predicted, repaired, built, transferred, or still unsupported.

### Closed-book checkpoint

1. Classify layout statements as semantic guarantee, representation guarantee, or observation.
2. Calculate `repr(C)` padding for an unseen struct.
3. State default representation's safe guarantees without assuming field order.
4. Distinguish owner size from controlled allocation size.
5. Explain wide pointer metadata for slice and str.
6. Discuss niche optimization without overclaiming arbitrary enum layout.
7. Explain why ZST addresses are not identity.
8. State what `repr(transparent)` guarantees and does not.
9. Reject raw memory serialization with at least five concrete defects.
10. Defend the limits printed by the capstone memory report.

### Transfer defense

Transfer **Module 18: Memory Representation, Validity, and Layout** to a product unrelated to the course capstone. Change the domain model and failure mode, preserve the governing relationship, and identify which part of the original design was essential rather than accidental.

Your answer must include:

- the governing rule for **Module 18: Memory Representation, Validity, and Layout** in plain language;
- state, ownership, or authority before and after the decisive operation;
- one causal negative case that fails for the intended reason;
- one principled repair and one easier repair that deletes a requirement;
- the limit of the evidence you used;
- one transfer to a product with different data and failure behavior.


Complete the first two sections without notes. Compile observation programs only after recording predictions. The target is not memorizing sizes; it is classifying claims and refusing to derive stronger contracts from weaker evidence.

#### Part A — Closed-book retrieval

Answer each question in two or three precise sentences.

1. What exactly does `size_of::<T>()` measure for a sized type?
2. What does `size_of::<String>()` exclude?
3. How do length and capacity differ for `String` and `Vec<T>`?
4. What is alignment, and how can it affect an aggregate's size?
5. What is padding, and why is it not semantic payload?
6. Why may padding bytes be uninitialized even when every field is initialized?
7. What minimum facts may safe code rely on under default Rust representation?
8. Why is source field order not a general durable-format contract under `repr(Rust)`?
9. What does `#[repr(C)]` strengthen?
10. What does `#[repr(C)]` still fail to make target-independent?
11. Under what broad shape is `#[repr(transparent)]` useful?
12. Why does a transparent representation not erase the wrapper's semantic invariants?
13. What is a dynamically sized type?
14. Why is a reference to `str` or `[T]` conceptually more than a data address?
15. What metadata accompanies a slice-like pointer?
16. Why is `Box<str>` a sized owner of a dynamically sized referent?
17. What is a niche?
18. Why is a niche an encoding opportunity rather than a universal optimization guarantee?
19. Which source can turn a niche observation into a contract for a specific standard-library type?
20. Why does equal size not establish equal encoding or ABI compatibility?
21. Why can an application rule such as “handle generation is never zero” fail to create a type-level niche?
22. Why is `usize` unsuitable as an unstated portable wire width?
23. What does `size_of_val` report for a slice, and what does it still exclude?
24. How should an `Rc<T>` allocation be counted when ten `Rc` handles point to it?
25. Why can a workspace be small by `size_of::<Workspace>()` and own gigabytes?
26. What is a zero-sized type, and why can a vector of ZST values still have meaningful length?
27. Why does smaller representation not automatically mean faster execution?
28. What four labels should be available for every layout statement in this course?
29. What evidence is required before layout becomes part of a safety argument?
30. Why must persistence encode semantic fields explicitly?

#### Part B — Claim classification

Classify every statement as one of:

- **semantic guarantee**;
- **documented representation/library contract**;
- **target observation**;
- **unsupported inference**.

Then justify the label.

1. “A `String` owns valid UTF-8 text.”
2. “On this x86-64 run, `String` occupies 24 inline bytes.”
3. “Every future Rust target stores `String` as pointer, length, capacity in that source order.”
4. “A slice reference carries enough metadata to determine the slice length.”
5. “Because `Option<&u8>` is the same size as `&u8`, every optional pointer wrapper is also pointer-sized.”
6. “This `repr(C)` header may contain padding required by the target C layout.”
7. “Writing the bytes of that `repr(C)` header produces a portable file.”
8. “A `NonZeroU64` value cannot represent zero.”
9. “The standard library's documented optional nonzero representation applies under its stated conditions.”
10. “`Option<MyHandle>` is eight bytes on the machine used by this test.”
11. “`Option<MyHandle>` will remain eight bytes because stale handle values are invalid in the application.”
12. “Two `Rc` clones can own the same allocation.”
13. “Dropping one of two strong `Rc` owners releases the referent.”
14. “A weak pointer does not keep the referent alive.”
15. “`size_of::<Vec<Box<str>>>()` includes every boxed string.”

A correct answer names the boundary. For example, statement 7 is not repaired by saying “usually false”; explain that C-oriented in-memory layout still does not define byte order, versioning, pointer meaning, or target-independent widths.

#### Part C — Prediction laboratory

Before running, predict the relationships rather than exact numbers:

```rust
use std::mem::{align_of, size_of};
use std::num::NonZeroU64;
use std::rc::{Rc, Weak};

#[derive(Clone, Copy)]
struct DocumentHandle {
    slot: u32,
    generation: u32,
}

#[repr(transparent)]
struct NonZeroHandle(NonZeroU64);

#[repr(C)]
struct Header {
    kind: u8,
    length: u32,
    flags: u16,
}

fn row<T>(name: &str) {
    println!("{name:32} size={:>3} align={:>2}", size_of::<T>(), align_of::<T>());
}

fn main() {
    row::<DocumentHandle>("DocumentHandle");
    row::<Option<DocumentHandle>>("Option<DocumentHandle>");
    row::<NonZeroU64>("NonZeroU64");
    row::<Option<NonZeroU64>>("Option<NonZeroU64>");
    row::<NonZeroHandle>("NonZeroHandle");
    row::<Option<NonZeroHandle>>("Option<NonZeroHandle>");
    row::<&str>("&str");
    row::<Box<str>>("Box<str>");
    row::<Rc<str>>("Rc<str>");
    row::<Weak<str>>("Weak<str>");
    row::<Header>("Header");
    row::<()>("unit");
    row::<[(); 1_000]>("[(); 1000]");
}
```

For every row, record:

```text
Prediction about relative size/alignment:
Observed result:
What the result establishes:
What the result cannot establish:
Whether any product code may depend on it:
```

Do not convert a successful equality assertion into a portability claim. The laboratory is an observatory, not a serialization generator.

#### Part D — Memory-accounting derivation

A workspace contains:

- a `Vec<Slot>` with length 500 and capacity 768;
- 400 occupied documents;
- each document owns a title `String`, text `String`, and `Vec<String>` tags;
- each document may own one cached `Vec<Range<usize>>`;
- a map stores 100 `Rc<DocumentSnapshot>` values;
- callers may hold additional strong snapshot clones;
- callers may hold edit sessions containing candidate strings.

Design a report with at least these categories:

1. inline workspace and field-owner observations;
2. slot vector reserved storage;
3. live document logical payload;
4. live document reserved string/tag capacity;
5. cache range capacity;
6. unique cached snapshot payload reachable from the workspace;
7. snapshot control-block and allocator exclusions;
8. caller-owned snapshots and edit sessions excluded from workspace ownership;
9. target/toolchain label for every `size_of` observation.

Write a formula using variables. An acceptable form is:

```text
slot_capacity × size_of::<Slot>()
+ Σ live document string/tag capacities
+ Σ cache range capacities × size_of::<Range<usize>>()
+ Σ unique cached snapshot payload
```

Then list everything omitted. The formula is not required to match resident-set size; it is required to describe its scope honestly.

#### Part E — Adversarial transfer problems

##### 1. Memory-dump persistence

A teammate proposes:

```rust
#[repr(C)]
struct Record {
    kind: u8,
    id: u64,
    length: u32,
}
```

They want to write `size_of::<Record>()` bytes from the struct to disk. Produce a rejection explaining padding, endianness, validity, versioning, and target dependence. Then define an explicit version-1 byte grammar and decoding checks.

##### 2. Optional compact handle

The product demands that an optional handle occupy eight bytes. Compare:

- relying on observed `Option<DocumentHandle>` size;
- packing slot/generation into `NonZeroU64` with a transparent wrapper;
- storing an explicit validity bit elsewhere;
- accepting a larger option.

For each, state range limits, invalid encodings, API invariants, and future-evolution cost. Select one only after the product's slot/generation bounds are explicit.

##### 3. Shared snapshot counting

The cache map contains 100 keys but two keys accidentally point to the same `Rc` allocation, and callers hold 500 clones. Define three different counts:

- number of cache entries;
- number of unique allocations reachable from the cache;
- number of strong owner handles known to one local graph walk.

Explain why none is automatically total process memory.

##### 4. ZST capacity reasoning

A `Vec<Marker>` where `Marker` is zero-sized has length one million. Explain why the vector can report that logical length without allocating one million payload bytes, and why iteration still performs one million logical steps. Separate representation cost from algorithmic work.

##### 5. Layout-driven optimization request

A benchmark shows a compact enum is faster in one microbenchmark. Write the additional evidence required before changing a public representation: workload relevance, cache behavior, branch effects, target coverage, API compatibility, and whether an explicit `repr` would freeze an unnecessary contract.

#### Part F — Answer criteria

A passing response must demonstrate all of the following:

- inline size is never described as transitive owned memory;
- padding is never treated as initialized payload;
- `repr(C)` is not described as a portable storage format;
- niche claims are tied to exact documented types or labeled observations;
- pointer metadata and referent allocation are distinguished from pointer-owner size;
- shared allocations are deduplicated by identity when the report claims unique payload;
- every external boundary has an explicit encoding;
- target observations include target/toolchain context;
- performance claims require measurement and do not follow from size alone.

### Closed-book defense

In five minutes, answer “Is a claim a language guarantee, a standard-library contract, a target-conditioned fact, a current observation, or an unsupported assumption?” using the **representation table**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside Memory Workspace. A list of APIs without the deciding relationship is incomplete.
