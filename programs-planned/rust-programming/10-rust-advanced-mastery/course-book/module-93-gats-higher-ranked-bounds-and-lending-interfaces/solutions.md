# Module 93 Solutions — GATs, Higher-Ranked Bounds, and Lending Interfaces

[Workbook](workbook.md) · [Chapter](index.md) · [AxiomStore guide](../capstone.md)

These are reasoned reference answers. Compare your predicted phase, invariant owner, and failure state before comparing syntax. A different implementation is stronger when it preserves the same contract with a smaller proof surface.

## Part 1 — Prediction

### Prediction 1 — Retained lending item

The first view keeps the mutable borrow of the cursor active for its lifetime, so the second mutable borrow is rejected unless the first view is released or converted to owned data.

### Prediction 2 — Higher-ranked callback

The function chooses each short lifetime; `F` must work for all of them. Safe code cannot store a reference beyond the individual call unless external state is valid for every such lifetime, which is generally impossible.

### Prediction 3 — Ordinary iterator alternative

An ordinary iterator yielding `&'input str` can permit multiple rows to coexist. Lending is unnecessary unless advancing invalidates views or they borrow cursor-local scratch state.

### Prediction 4 — Trait object request

A lifetime-indexed associated family complicates dyn use. Keep lending static and erase a separate dyn-compatible policy interface if runtime extension is the actual requirement.

## Part 2 — Diagnose and repair

Judge every repair against the quantifier-and-borrow map: the decisive relationship must become clearer, not disappear behind cloning, erasure, broad bounds, visibility, unchecked construction, or deleted validation.

### Repair 1 — One lifetime for source and method borrow

**Causal defect.** An API uses the same named lifetime for the input buffer, cursor, and each call, causing an exclusive borrow to last too long.

**Principled repair.** Separate source lifetime from method-borrow lifetime through the GAT family. Let reborrowing shorten the source reference for each call.

A strong answer updates the quantifier-and-borrow map and includes a negative case that fails for the original cause.

### Repair 2 — GAT added to avoid all allocation

**Causal defect.** Every consumer needs to keep all rows, but the API forces a lending cursor and immediate cloning.

**Principled repair.** Use owned rows or an ordinary iterator over independent source slices. A lending protocol that conflicts with dominant use is not a win.

A strong answer updates the quantifier-and-borrow map and includes a negative case that fails for the original cause.

### Repair 3 — Escaping scoped view

**Causal defect.** A higher-ranked callback returns the temporary view supplied by the producer.

**Principled repair.** Return an owned conversion or a result independent of the temporary lifetime. HRTBs guarantee scoped capability, not lifetime extension.

A strong answer updates the quantifier-and-borrow map and includes a negative case that fails for the original cause.

## Part 3 — Focused exercises

### Exercise 1 — Quantifier translation

The construction should answer: Translate four prose requirements into ordinary lifetime parameters or `for<'a>` bounds.

The decisive acceptance criterion is: Each answer states who chooses the lifetime and what must outlive it.

Evaluate the result through the quantifier-and-borrow map; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 2 — Lending cursor

The construction should answer: Implement a cursor over temporary row scratch state.

The decisive acceptance criterion is: A compile-fail example proves retained views block the next call.

Evaluate the result through the quantifier-and-borrow map; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 3 — Coexisting views redesign

The construction should answer: Change the requirement so two rows must coexist and redesign the API.

The decisive acceptance criterion is: The chosen ownership or stable-source model permits coexistence without unsound lifetime widening.

Evaluate the result through the quantifier-and-borrow map; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 4 — Owned boundary

The construction should answer: Add a deliberate `to_owned` transition at the point retention begins.

The decisive acceptance criterion is: Lifetimes do not spread into the storage and policy layers.

Evaluate the result through the quantifier-and-borrow map; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Cross-course transfer

Full credit may conclude that **GATs, Higher-Ranked Bounds, and Lending Interfaces** should not be retrofitted into the earlier artifact. The comparison must identify the current owner, the proof benefit, maintenance cost, and a concrete failure that would change.


### Applied case study — a lending cursor and a retained index

The lending cursor's item family is indexed by the borrow used for one call: `type View<'a> where Self: 'a`. The method borrows `&'a mut self` and returns `Option<Self::View<'a>>`. The lifetime is not the lifetime of the original input alone; it is bounded by the current mutable loan because the next advance may mutate or compact cursor state. The `Self: 'a` clause states that the implementor and data it contains remain valid for the selected loan.

A report that survives later cursor advances must cross an ownership boundary. The caller should copy only the fields it selected, or call a deliberate `to_owned` conversion after deciding retention is required. A `Vec<View<'_>>` spanning repeated calls should be rejected because the first item keeps the cursor mutably borrowed and because compaction could invalidate its storage.

`with_next` can accept `F: for<'a> FnOnce(Self::View<'a>) -> R` only when the result `R` does not carry `'a`. The higher-ranked bound means the callback must work for whichever fresh lifetime the method chooses; the caller cannot demand one preselected long lifetime and smuggle the view outward.

Owned output is preferable when records must routinely outlive the cursor, cross threads, enter long-lived caches, or survive buffer replacement. In that product, lending every field may transfer complexity to every caller without removing meaningful copying. The advanced mechanism earns its cost only when temporary borrowed processing is common and retention is exceptional.

## Part 4 — Independent laboratory

A complete [Lending Table](../../labs/module-03-lending-table/README.md) satisfies its public contract and makes the quantifier-and-borrow map inspectable. The reference implementation is not canonical; compare accepted input, rejected input, state after failure, ownership/lifetime surface, deterministic behavior, and extension authority in that order.

Build a table cursor whose row view is tied to each mutable cursor borrow, then add an explicit owned escape for callers that need retention.

The transfer variant for Lending Table must alter at least two substantive dimensions and preserve an independent oracle; a domain-name substitution is not evidence of mastery.

## Part 5 — Capstone transfer

Implement and document AxiomStore’s `RecordCodec::View<'a>` and `LendingRecords::View<'a>` families. Add negative documentation showing that a record view cannot outlive the snapshot or coexist with a conflicting cursor advance.

A strong capstone change keeps the responsibility described by the quantifier-and-borrow map local. Reject any design that spreads the mechanism across unrelated AxiomStore modules without a named requirement.

## Part 6 — Reconstruct and defend

Read each lifetime quantifier in plain language, explain why source lifetime and method-borrow lifetime differ, and decide whether the lending protocol matches the consumer’s retention needs.

The defense passes when it reconstructs the quantifier-and-borrow map from the requirement, shows a causal rejected construction, compares a simpler alternative, maps evidence, and names residual risk. Terminology without that chain is not mastery.
