# Module 100 — Architectural Synthesis: Building and Defending a Long-Lived Rust System

**Course 10 · Day 10 · Module 100 of 100**
`█████████████████████████` **100/100**

[Program](../../../README.md) · [Course 10](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-10-architecture-council/README.md) · [AxiomStore guide](../capstone.md)

[← Module 99: Long-Lived APIs: SemVer, MSRV, Features, Migrations, and Workspace Stewardship](../module-99-long-lived-apis-semver-msrv-features-migrations-and-workspace-stewardship/index.md)

## The question

> Can you turn ten courses of mechanisms into one restrained architecture whose guarantees, unsafe core, verification evidence, compatibility policy, and operating limits can survive independent review?

## Why this comes now

The final module introduces no mechanism merely for novelty. It asks you to choose among all mechanisms learned so far and reject most of them. A mature Rust design does not maximize type-level sophistication, unsafe cleverness, async concurrency, or abstraction count. It gives each invariant one owner, keeps proof surfaces small, exposes honest failure, and records why alternatives were rejected. Module 100 is an architecture council: you complete AxiomStore, implement an unseen format evolution, and defend the system from source contract through machine artifact and long-term stewardship.

Modules 91–99 added no independent destination; they prepared one architecture council. The final module asks you to retain only the mechanisms that own real invariants and to defend their combined cost.

The final module is not a parade of advanced features. It is a selection exercise. AxiomStore must remain understandable after GATs, const bounds, erasure, unsafe storage, format evolution, and verification are combined. The architecture is mature only when every mechanism owns one requirement, every claim has evidence, and several sophisticated alternatives are deliberately rejected.

### Prerequisite bridge

Module 99 established **Long-Lived APIs: SemVer, MSRV, Features, Migrations, and Workspace Stewardship**. Before beginning the final module, verify that you can govern a multi-crate workspace through dependency direction, shared policy, release order, and compatibility evidence. This module preserves that capability and adds the ability to construct an invariant map connecting product claims to types, runtime validation, synchronization, unsafe proofs, tests, and operational policy; the final architecture defense must demonstrate both under an unseen change.

### Scope boundary

This module owns the reasoning for **architectural synthesis: building and defending a long-lived rust system** inside Course 10. The course selects stable mechanisms that serve real product requirements. It does not reward obscure syntax, nightly-feature collecting, unsafe code retained for display, or lower-level compiler output used where source-level reasoning is already decisive. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

After completing this module, you will be able to:

- construct an invariant map connecting product claims to types, runtime validation, synchronization, unsafe proofs, tests, and operational policy
- choose static, dynamic, enum, const-generic, borrowing, owned, generated, concurrent, async, and unsafe mechanisms only where their proof benefit exceeds complexity
- review dependency direction, public surface, failure taxonomy, resource bounds, and deterministic behavior as one architecture
- perform a threat, compatibility, verification, and production-readiness review without confusing those evidence categories
- implement an unseen cross-cutting requirement while preserving old data, public behavior, and safety invariants
- present a concise architecture defense that identifies residual risk and evidence gaps rather than claiming perfection

## Core model

### The governing model

Build an **architecture defense dossier**: product boundary, invariant ownership map, authority and variation map, failure taxonomy, unsafe dossier, compatibility matrix, verification matrix, artifact identity, residual risks, and rejected alternatives. The dossier must be reconstructible from the public behavior and source, not from private author memory.

### 1. Architecture begins with invariant ownership

List every property the product promises: valid archive bytes, unique keys, bounded record size, transaction atomicity, borrowed-view lifetime, validator order, initialized inline slots, supported format versions, deterministic output, and migration failure state. Assign each property one primary owner: a private type, constructor, codec, transaction state, registry, unsafe invariant, or release policy. Tests support the owner; they should not be the only place the rule exists.

**Assign one owner.** For unique keys, record size, validator order, initialized slots, and format version, name exactly one primary type or transition that owns each invariant.

### 2. Mechanism selection is a proof-cost decision

A const generic can reject capacity mismatch but creates type diversity. A GAT can express zero-copy views but constrains retention and dyn use. A trait object permits runtime extension but erases concrete relationships. Unsafe inline storage may remove allocation but creates a permanent safety dossier. For each mechanism, state the requirement it proves, the complexity it introduces, the simpler alternative, and the evidence that justifies retaining it.

**Price the mechanism.** For every advanced feature in AxiomStore, state the invalid state or ambiguity it removes and the proof cost it introduces.

### 3. Public architecture is smaller than internal architecture

Callers need stable records, errors, snapshots, transactions, validators, and format/version observations. They do not need internal buffer layouts, parser cursors, helper traits, or every codec implementation. Keep fields private and expose behavioral constructors. Use opaque return types or private modules to preserve room for change. Publicly exposing a mechanism converts today’s implementation into tomorrow’s compatibility obligation.

**Minimize public surface.** Identify which codecs, storage fields, validator internals, and unsafe details callers must not depend on.

### 4. Failure taxonomy controls recovery

Differentiate invalid input, unsupported version, validation rejection, duplicate key, capacity exhaustion, stale snapshot, pre-commit I/O failure, post-install durability uncertainty, migration failure, unsupported replacement platforms, unsafe defects, and CLI misuse. Each category needs a stable state-after-failure contract. Pre-rename transaction failures leave the previous archive unchanged; a directory-synchronization failure is reported separately because replacement may already be visible. Migrations preserve the source and refuse to overwrite an existing destination. Unsafe invariant violations are defects, not recoverable user errors.

**Classify failures.** Separate invalid record, policy rejection, capacity, malformed bytes, unsupported version, checksum, duplicate key, migration, I/O, and usage behavior by recovery owner.

### 5. Verification is a portfolio

Map type-level claims to compile-fail fixtures, codec behavior to known vectors and properties, transaction semantics to a reference model, unsafe storage to drop tests and Miri, compatibility to golden archives and downstream crates, and artifact cost to measured profiles. Record missing evidence explicitly. The final defense is stronger when it says “this claim remains manual review” than when it hides the gap under a global green badge.

**Map evidence.** Match each invariant to compile-time, runtime, model, unsafe, compatibility, or artifact evidence; do not cite one aggregate test command.

### 6. Long-lived systems need change paths

The architecture must answer how to add a validator, record field, format version, feature, migration, or query without rewriting unrelated layers. A change path is not unlimited extensibility. Built-in formats may remain a closed enum under the reader’s authority while validators are open runtime plugins. Version-specific codecs may remain private while the public store exposes stable records. Deliberate closure is often what makes evolution reviewable.

**Design change paths.** For AXIOM02, state reader policy, writer policy, migration, unknown-version behavior, and rollback.

### 7. The unseen extension tests transfer

The final requirement adds `AXIOM02` schema tags while preserving `AXIOM01` reads. No chapter provides a line-by-line implementation. You must decide where version selection occurs, how old bytes map to the stable model, which writer becomes default, how schema tags are validated, what fixtures are added, and whether public APIs change. The score depends on preserved invariants and reasoning, not feature count.

**Exercise transfer.** Add schema tags without exposing internal codec types or invalidating borrowed-view lifetimes.

### 8. An architecture defense includes rejection

Present the final system in twenty minutes: product boundary, data and ownership flow, variation map, unsafe dossier, compatibility matrix, verification matrix, and residual risks. Then identify at least five mechanisms deliberately not used—such as async I/O, a public plugin ABI, lock-free storage, a proc-macro schema, or self-referential records—and explain why their proof and maintenance cost exceeds current value. Restraint is part of mastery.

**Defend rejection.** Explain why async I/O, public plugins, lock-free transactions, memory mapping, and macro-generated schema are not justified now.

### Worked synthesis: deciding whether InlineBatch belongs

AxiomStore could stage transaction operations in a `Vec<Operation>`. That design is entirely safe, dynamically sized, familiar, and likely sufficient for many products. The reference instead uses `InlineBatch<Operation, TX_CAP>`. The advanced mechanism earns its place only under a specific requirement: transaction capacity is intentionally small and fixed per store type, inline storage is desired, and the program is willing to carry a private unsafe proof.

The architecture council should challenge that decision. Compare:

| Question | `Vec` | `InlineBatch` |
|---|---|---|
| safe implementation | yes | no, internal unsafe |
| arbitrary runtime capacity | natural | no |
| fixed inline storage | no | yes |
| initialized-state bookkeeping | library-owned | capstone-owned |
| audit and Miri burden | small | material |
| public type identity | optional | const capacity appears in store type |

If measurements and deployment requirements do not value inline storage, `Vec` is the better architecture. Course 10 does not award points for retaining unsafe code merely because Module 96 taught it. The same test applies to every feature: GAT views must serve ephemeral zero-copy inspection; dynamic validators must serve runtime policy; const bounds must serve real composition or storage; format versioning must serve durable compatibility.

The final defense also includes operations that are deliberately ordinary. `BTreeMap` gives canonical ordering; a private constructor gives valid records; an enum gives typed errors; a same-directory temporary file plus a documented Unix rename and directory-sync contract gives a bounded single-writer replacement protocol. Mastery is visible when sophisticated and ordinary mechanisms coexist without one becoming an ideology.

### A decision table

| Design question | Principled evidence or mechanism | Weak substitute to reject |
|---|---|---|
| Which component owns each invariant? | one primary type, transition, codec, or policy owner | rules duplicated in callers and tests |
| Does an advanced mechanism earn its proof cost? | retain only when it removes a material invalid state or boundary ambiguity | complexity used to display technique |
| What is public? | stable behavior and deliberate extension points | internal representation exposed for convenience |
| What evidence supports release? | claim-specific verification and explicit residual risk | one aggregate green badge |

### A rigorous working procedure

1. Freeze the product contract and list every externally visible behavior.
2. Assign each invariant and authority to one owner; delete duplicate validation or representation authorities.
3. Review each advanced mechanism against a simpler alternative and retain it only when the proof benefit is material.
4. Trace all success, failure, cleanup, migration, and compatibility paths end to end.
5. Map every claim to evidence and mark gaps, manual review, and expiry conditions.
6. Implement AXIOM02 as an unseen change, rerun the complete matrix, and present the architecture plus rejected alternatives.

### Failure patterns and principled repairs

Synthesis fails when advanced mechanisms are accumulated as trophies rather than selected as invariant owners. Repair the architecture by assigning every requirement to one mechanism, removing duplicate authorities, documenting the proof boundary, and retaining a simpler alternative wherever it preserves the same product contract.

### Maximizing use of Course 10 features

Remove mechanisms that do not own a unique requirement; synthesis is selection, not accumulation.

### Claiming every invariant is statically guaranteed

Separate type proofs, runtime validation, unsafe assumptions, platform contracts, and operating policy.

### Designing extension without compatibility ownership

Name who adds variants or implementations and which downstream code/data must remain valid.

### Hiding residual risk from the defense

Record unsupported scenarios, manual review obligations, and evidence that expires with artifact or toolchain change.

### What the compiler cannot decide for you

No compiler, test suite, model, or review can decide the product’s values for you. The type system may make one class of invalid construction impossible while leaving authorization, durability, compatibility, and operating policy entirely external. Architecture is the disciplined allocation of those responsibilities.

The final standard is not complexity. It is **defensible restraint**: a reader can locate each rule, predict each failure, understand each unsafe assumption, migrate old data, and change one version without rediscovering hidden authority.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For construct an invariant map connecting product claims to types, runtime validation, synchronization, unsafe proofs, tests, and operational policy, construct one positive and one causal negative example. Mark the first decisive fact in the **architecture defense record** and state which evidence could falsify the claim.

2. **Outcome 2.** For choose static, dynamic, enum, const-generic, borrowing, owned, generated, concurrent, async, and unsafe mechanisms only where their proof benefit exceeds complexity, construct one positive and one causal negative example. Mark the first decisive fact in the **architecture defense record** and state which evidence could falsify the claim.

3. **Outcome 3.** For review dependency direction, public surface, failure taxonomy, resource bounds, and deterministic behavior as one architecture, construct one positive and one causal negative example. Mark the first decisive fact in the **architecture defense record** and state which evidence could falsify the claim.

4. **Outcome 4.** For perform a threat, compatibility, verification, and production-readiness review without confusing those evidence categories, construct one positive and one causal negative example. Mark the first decisive fact in the **architecture defense record** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

Use the decision-record example as a miniature architecture council. A decision is incomplete until it names the requirement, chosen mechanism, rejected alternative, proof owner, compatibility effect, and residual risk. Apply the same standard to every AxiomStore mechanism.

```rust
#[derive(Clone, Debug, PartialEq, Eq)]
struct ArchitectureDecision {
    requirement: &'static str,
    chosen_mechanism: &'static str,
    rejected_alternative: &'static str,
    proof_owner: &'static str,
    remaining_risk: &'static str,
}

const DECISIONS: &[ArchitectureDecision] = &[
    ArchitectureDecision {
        requirement: "borrow record fields without allocation",
        chosen_mechanism: "GAT-based private codec and snapshot iterator",
        rejected_alternative: "public self-referential record",
        proof_owner: "snapshot lifetime and compile-fail fixtures",
        remaining_risk: "borrowed views cannot be retained across mutation",
    },
    ArchitectureDecision {
        requirement: "runtime validation policy",
        chosen_mechanism: "Box<dyn Validator<Record>>",
        rejected_alternative: "generic store over validator tuple",
        proof_owner: "registry ordering and stable owned Record boundary",
        remaining_risk: "third-party validator latency is not statically bounded",
    },
];
```

### Trace the example

Take one decision—GAT-based record views, dynamic validators, or `InlineBatch`—and reconstruct it from the requirement. Show the simpler alternative, the exact property lost, the new proof burden, and the evidence that covers it. If the chosen mechanism does not win that comparison, remove it.

Then trace one `put` operation from CLI argument through `Record`, validation, transaction staging, candidate map, AXIOM01 encoding, verification, file replacement, snapshot reopening, and borrowed listing. Mark ownership, failure, cleanup, and compatibility at each boundary.

### Use it in AxiomStore

AxiomStore is completed as the program’s synthesis product. The final review examines its borrowed codec family, static and dynamic variation, const bounds, unsafe inline batch, binary compatibility, migrations, verification matrix, CLI, and release policy together. The independent extension to `AXIOM02` is the mastery proof: it must fit the architecture rather than trigger an ad hoc second system.

The final AxiomStore dossier contains:

```text
1. product and non-goals
2. data/ownership flow
3. invariant ownership map
4. type and variation map
5. failure and recovery taxonomy
6. unsafe InlineBatch dossier
7. AXIOM01/AXIOM02 compatibility matrix
8. verification claim matrix
9. artifact and MSRV record
10. residual risks and rejected alternatives
```

Implement AXIOM02 only after writing the reader/writer policy. Preserve AXIOM01 fixtures, unknown-version rejection, deterministic output, transaction behavior, and the borrowed-view contract.

## Practice sequence

1. **Invariant council.** Assign every capstone promise to one owner and eliminate duplicate policy.
2. **Mechanism subtraction.** Remove one advanced mechanism, implement the simpler alternative, and compare the proof and maintenance surfaces.
3. **End-to-end failure trace.** Follow malformed bytes, validator rejection, capacity exhaustion, and file replacement failure to stable state and user-visible error.
4. **AXIOM02 extension.** Add schema tags while preserving AXIOM01 reads and unknown-version rejection; update fixtures and migration.
5. **Twenty-minute defense.** Present product, architecture, unsafe proof, compatibility, evidence, residual risk, and five rejected mechanisms.

Complete the [workbook](workbook.md) and [Architecture Council](../../labs/module-10-architecture-council/README.md). The final review is passed only when a fresh reader can reproduce the argument and challenge it with an unseen requirement.

## Ready to continue

The program is complete when you can design a Rust system from requirements, choose mechanisms with explicit authority and proof cost, preserve earlier guarantees during change, audit unsafe code as a whole abstraction, and state the limits of every form of evidence. Completion is demonstrated by the AXIOM02 transfer and architecture defense, not by reading all one hundred chapters.

## Primary Rust references

- The Rust Reference and standard library contracts used throughout the program
- Cargo Reference for workspaces, features, profiles, and MSRV
- The Rust API Guidelines, Rustonomicon, rustc development guide, and verification-tool documentation

The final references are intentionally distributed across the Reference, Cargo documentation, rustc guide, standard library, Rustonomicon, and prior course books. Use them to verify exact contracts while keeping AxiomStore’s dossier as the coherent product-specific explanation.

## Continue

Finish the Course 10 final review and the independent AXIOM02 change. The program is complete only when another competent Rust reader can reproduce your invariant map, compatibility decision, unsafe argument, verification limits, and migration reasoning without seeing your implementation first.
