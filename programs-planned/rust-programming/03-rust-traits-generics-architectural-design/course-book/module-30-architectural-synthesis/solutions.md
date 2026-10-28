# Reasoned solutions — Module 30: Architectural Synthesis

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the Review Engine engineering guide](../capstone.md)

Use these explanations to review your reasoning about **Architectural Synthesis**, not to substitute for an attempt. The decisive question is: *Given a real source of variation, how do you choose among enums, generics, trait objects, closures, functions, and ordinary composition?* When your design differs, separate three possibilities: a Rust rule was applied incorrectly, the product contract changed, or two architectures satisfy the same contract with different trade-offs.

## Compiler specimen reasoning

### 1. `01-hybrid-dispatch.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Hybrid dispatch.
- **Causal explanation:** The specimen compiles because hybrid dispatch.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Erase every boundary for uniform appearance.

### 2. `02-hybrid-associated-type-mismatch.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Hybrid associated type mismatch.
- **Causal explanation:** The compiler rejects the specimen because hybrid associated type mismatch.
- **Principled repair:** Constrain the associated type at the engine boundary.
- **Weak repair to reject:** Convert arbitrary items to strings.

### 3. `03-registry-dyn-compatibility.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Registry dyn compatibility.
- **Causal explanation:** The compiler rejects the specimen because registry dyn compatibility.
- **Principled repair:** Split static construction from dyn execution.
- **Weak repair to reject:** Make all input String.

### 4. `04-builder-state-gate.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Builder state gate.
- **Causal explanation:** The compiler rejects the specimen because builder state gate.
- **Principled repair:** Complete the typestate transition.
- **Weak repair to reject:** Add a runtime panic in build.

### 5. `05-coherence-adapter-need.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Coherence adapter need.
- **Causal explanation:** The compiler rejects the specimen because coherence adapter need.
- **Principled repair:** Introduce a local adapter newtype.
- **Weak repair to reject:** Use a type alias.

### 6. `06-opaque-report-view.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Opaque report view.
- **Causal explanation:** The specimen compiles because opaque report view.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Box the iterator without runtime need.

### 7. `07-object-lifetime-in-registry.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Object lifetime in registry.
- **Causal explanation:** The compiler rejects the specimen because object lifetime in registry.
- **Principled repair:** Give the registry an explicit lifetime or own the data.
- **Weak repair to reject:** Leak the borrowed string.

### 8. `08-sealed-integrated-extension.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Sealed integrated extension.
- **Causal explanation:** The compiler rejects the specimen because sealed integrated extension.
- **Principled repair:** Implement the open execution trait or use a supported factory.
- **Weak repair to reject:** Expose sealing internals publicly.

## Exercise reasoning

Final answers are requirement-dependent. A passing answer makes selection time, openness, caller knowledge, coherence ownership, and evolution consequences explicit. Static and dynamic paths must share domain semantics. ADRs name credible alternatives. An unseen rule should enter through construction/registry extension without modifying the executor. Reporter output changes should remain visible through `R::Output`. Removing an abstraction passes when no independent variation or contract is lost.

## Variation map

A strong map usually keeps source and reporter as generic outer boundaries because one execution selects one concrete implementation of each. Their associated types preserve item and error families. Rules form a runtime heterogeneous ordered collection, so trait objects are justified there. CLI commands are a closed enum. Pure helpers remain functions. Builder states are type parameters only until construction succeeds.

The map is not a feature inventory. It is a record of who chooses variation, when selection occurs, and whether several types must coexist.

## Failure repairs

Making every component dynamic erases useful relationships and spreads lifetime/object concerns. Making every rule generic produces an engine type proportional to the rule combination and cannot hold an open heterogeneous set. Public arbitrary state mutation destroys typestate. An overbroad closure blanket implementation consumes coherence space; a named adapter wrapper localizes it. Stringifying errors too early loses classification. Deterministic ordering requires an ordered registry and tests over observable output.

## Changed requirement

Warning-only behavior usually belongs in finding severity or rule outcome data, not a second rule trait. Explanation can be a required or default object-safe method when every rule has meaningful metadata, or stored registry metadata when behavior objects should remain minimal. Loading submissions is unrelated, so the command path should query the configured policy directly. The dynamic registry remains justified because configured concrete rule types still coexist at runtime.

## Independent build

The new domain proves transfer only when names, inputs, and failure modes differ. The static relationship should be one implementation-selected family, the dynamic collection should represent real runtime openness, and typestate should remove a concrete invalid call. A downstream-style test should construct only through public APIs.

## Final defense

Begin with the product's sources of variation. Rust mechanisms follow. A convincing defense includes rejected alternatives and explains what future change each chosen boundary makes easy or difficult.

## Laboratory comparison

The complete laboratory implementation is in [`module-10-inspection-platform/solution`](../../labs/module-10-inspection-platform/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Architectural Synthesis**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Map axes of variation before selecting polymorphism mechanisms.
- Combine static and dynamic dispatch without duplicating domain semantics.
- Review an architecture for coherence, dyn compatibility, state validity, and evolution.
- Implement an unseen cross-cutting feature while preserving public contracts.
- Defend the selected architecture and identify a credible alternative.

A complete explanation of **Architectural Synthesis** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.
