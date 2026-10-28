# Reasoned Solutions — Module 18: Memory Representation, Validity, and Layout

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-08-layout-observatory/README.md) · [Memory Workspace guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 18: Memory Representation, Validity, and Layout**. Compare the reasoning against this question: *Is a claim a language guarantee, a standard-library contract, a target-conditioned fact, a current observation, or an unsupported assumption?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `01-repr-c-layout.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** repr(C) permits target-based field layout calculation.
- **Causal explanation:** The specimen compiles because repr(C) permits target-based field layout calculation.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not promote a target observation into a portable layout or validity guarantee.

### 2. `02-default-layout-observation.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Default field addresses are observations only.
- **Causal explanation:** The specimen compiles because default field addresses are observations only.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not promote a target observation into a portable layout or validity guarantee.

### 3. `03-unsized-local.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A str value cannot be stored directly as a local.
- **Causal explanation:** The compiler rejects the specimen because a str value cannot be stored directly as a local.
- **Principled repair:** Use `&str`, `Box<str>`, or `String`; an unsized `str` must be accessed through a pointer-like form.
- **Weak repair to reject:** Do not guess a stack size for an unsized value.

### 4. `04-size-of-val-slice.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** size_of_val uses slice metadata.
- **Causal explanation:** The specimen compiles because size_of_val uses slice metadata.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not promote a target observation into a portable layout or validity guarantee.

### 5. `05-owner-versus-payload.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** String owner size differs from logical payload length.
- **Causal explanation:** The specimen compiles because string owner size differs from logical payload length.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not promote a target observation into a portable layout or validity guarantee.

### 6. `06-zero-sized-values.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** ZSTs carry logical values without payload bytes.
- **Causal explanation:** The specimen compiles because zSTs carry logical values without payload bytes.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not promote a target observation into a portable layout or validity guarantee.

### 7. `07-option-size-observations.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Option sizes can reveal documented and undocumented niches.
- **Causal explanation:** The specimen compiles because option sizes can reveal documented and undocumented niches.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not promote a target observation into a portable layout or validity guarantee.

### 8. `08-transmute-requires-unsafe.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Raw representation copying crosses an unsafe boundary.
- **Causal explanation:** The compiler rejects the specimen because raw representation copying crosses an unsafe boundary.
- **Principled repair:** Prefer documented byte conversions; if representation reinterpretation is truly required, isolate a small unsafe operation with validity and layout proofs.
- **Weak repair to reject:** Do not wrap an unexplained `transmute` in a broad unsafe block.

## Exercise reasoning and worked answers
1. The ledger must separate Reference/std guarantees from one-build observations. A target pointer width or current `String` size is observational unless a specific API guarantee says otherwise.
2. Apply each field's alignment in declaration order, insert internal padding, then round total size to the maximum alignment. Verify only for `repr(C)` and named target assumptions.
3. Printing addresses is acceptable observation. A test that fails when default-layout fields reorder is not portable and should be diagnostic, not acceptance.
4. `size_of` measures the inline owner/control value. Length is initialized logical elements/bytes; capacity is allocation reservation; payload bytes live elsewhere for heap owners. Shared payload must not be multiplied by handle count.
5. DST pointer metadata supplies dynamic size: slice element count, str byte count, and trait-object concrete layout information. The reference itself remains sized.
6. Some null-pointer optimizations are documented for references/nonzero pointer-like types; arbitrary equal-size options are observations. Never decode assumed niche bytes.
7. ZST collections track logical length despite no per-element payload. Addresses may coincide; explicit IDs are required for identity.
8. Transparent representation aligns layout/ABI with the one non-ZST field under its rules. It does not define endian-neutral serialization, validation, or semantic interchangeability.
9. Encode fields deliberately, including version, lengths, UTF-8, numeric byte order, and enum codes. Parse into checked domain constructors.
10. Report inline bytes, exposed capacities, logical payload, and shared snapshot deduplication. State allocator overhead and hidden implementation bookkeeping are excluded or estimated.

### Claim discipline

Three categories must remain distinct. A **language or standard-library guarantee** may support portable correctness. A **target-conditioned fact** is valid only under named assumptions such as pointer width, ABI, and representation attribute. An **observation** reports what one compiler build emitted and is useful for investigation, not for a public contract. The same numeric result can appear in all three categories for different reasons; the provenance of the claim is what matters.

`size_of::<String>()` does not report the string's allocation, allocator metadata, spare capacity, or shared ownership elsewhere. Likewise, summing `size_of::<Rc<T>>()` for handles counts inline handles repeatedly but does not identify unique payload allocations. A useful memory report must name its accounting boundary and deduplicate shared payloads by allocation identity when possible through safe APIs such as `Rc::ptr_eq`.

Niche observations require extra restraint. Seeing `Option<X>` equal `X` in size does not grant permission to infer an all-zero encoding, inspect invalid bit patterns, or serialize the in-memory bytes. The safe conclusion is only the documented representation guarantee, if one exists. Representation attributes govern layout and ABI properties within their specified scope; they do not validate domain values or define a durable wire format.

A portable serializer therefore starts from semantics: version marker, field order, explicit integer encoding, length framing, text encoding, and validation. It does not start from `size_of`, padding, or the current discriminant location. Layout observation can inform performance investigations, but persistence requires an independently specified grammar.

### Post-key transfer

Review a binary protocol that writes Rust values directly; replace layout assumptions with an explicit codec and evidence taxonomy.

## Reference implementation comparison

The complete laboratory implementation is in [`module-08-layout-observatory/solution`](../../labs/module-08-layout-observatory/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Memory Representation, Validity, and Layout**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Separate semantic value, validity invariant, abstract layout guarantee, ABI promise, and measured observation.
- Reason about size, alignment, padding, field non-overlap, repr(Rust), repr(C), and repr(transparent) without overclaiming offsets.
- Explain thin and wide pointers, metadata, slices, str, trait-object previews, and unsized tails.
- Classify enum discriminant and niche claims by documented guarantees rather than pattern extrapolation.
- Build memory reports that distinguish inline size, length, capacity, shared allocation deduplication, allocator overhead, and exclusions.

A complete explanation of **Memory Representation, Validity, and Layout** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.

## Deep reasoning and transfer

### Decisive model

> Is a claim a language guarantee, a standard-library contract, a target-conditioned fact, a current observation, or an unsupported assumption?

Build a **representation table**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Separate semantic value, validity invariant, abstract layout guarantee, ABI promise, and measured observation.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Reason about size, alignment, padding, field non-overlap, repr(Rust), repr(C), and repr(transparent) without overclaiming offsets.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Explain thin and wide pointers, metadata, slices, str, trait-object previews, and unsized tails.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Classify enum discriminant and niche claims by documented guarantees rather than pattern extrapolation.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Build memory reports that distinguish inline size, length, capacity, shared allocation deduplication, allocator overhead, and exclusions.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Separate semantic value, validity invariant, abstract layout guarantee, ABI promise, and measured observation.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the representation table.

### Laboratory transfer review

For [Layout Observatory](../../labs/module-08-layout-observatory/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In Memory Workspace, Module 18 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Memory Representation, Validity, and Layout**, which relationship decides this question: “Is a claim a language guarantee, a standard-library contract, a target-conditioned fact, a current observation, or an unsupported assumption?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to Memory Workspace?
