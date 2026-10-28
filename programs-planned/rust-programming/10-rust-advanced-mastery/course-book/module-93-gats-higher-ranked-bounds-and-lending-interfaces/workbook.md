# Module 93 Workbook — GATs, Higher-Ranked Bounds, and Lending Interfaces

[Chapter](index.md) · [AxiomStore guide](../capstone.md) · [Solutions](solutions.md)

This workbook turns the chapter’s **quantifier-and-borrow map** into evidence. Write predictions before compiling or running anything. Preserve the stated product requirement during repair; a green build obtained by deleting the difficult relationship is not a solution.

## Part 1 — Predict

For each case, submit: expected category (`compile-pass`, `compile-fail`, `run-pass`, `run-fail`, or `manual-review`), first decisive phase or event, governing relationship, and the strongest conclusion the outcome would justify.

Your prediction sheet must make the quantifier-and-borrow map visible. For one case, change exactly one assumption and explain why the decisive phase or outcome moves.

### Prediction 1 — Retained lending item

A cursor trait defines `type View<'a>` and `next<'a>(&'a mut self)`. A caller stores the first view and calls `next` again. Predict the result.

### Prediction 2 — Higher-ranked callback

A function requires `F: for<'a> Fn(&'a str)` and passes references to several short-lived local strings. Who chooses `'a`, and may `F` store the reference in external state?

### Prediction 3 — Ordinary iterator alternative

Rows are immutable slices into one stable input string and advancing uses only an index. Decide whether a lending cursor is required.

### Prediction 4 — Trait object request

A registry asks for `Box<dyn LendingCursor>`. Predict the design difficulty and identify a hybrid alternative.

## Part 2 — Diagnose and repair

Each repair must leave a more precise quantifier-and-borrow map. Reject fixes that merely erase the type, lifetime, state, compatibility, or artifact fact that the exercise is designed to expose.

### Repair 1 — One lifetime for source and method borrow

An API uses the same named lifetime for the input buffer, cursor, and each call, causing an exclusive borrow to last too long.

Required direction: Separate source lifetime from method-borrow lifetime through the GAT family. Let reborrowing shorten the source reference for each call.

Submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the quantifier-and-borrow map changes.

### Repair 2 — GAT added to avoid all allocation

Every consumer needs to keep all rows, but the API forces a lending cursor and immediate cloning.

Required direction: Use owned rows or an ordinary iterator over independent source slices. A lending protocol that conflicts with dominant use is not a win.

Submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the quantifier-and-borrow map changes.

### Repair 3 — Escaping scoped view

A higher-ranked callback returns the temporary view supplied by the producer.

Required direction: Return an owned conversion or a result independent of the temporary lifetime. HRTBs guarantee scoped capability, not lifetime extension.

Submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the quantifier-and-borrow map changes.

## Part 3 — Focused exercises

### Exercise 1 — Quantifier translation

Translate four prose requirements into ordinary lifetime parameters or `for<'a>` bounds.

Completion standard: Each answer states who chooses the lifetime and what must outlive it.

### Exercise 2 — Lending cursor

Implement a cursor over temporary row scratch state.

Completion standard: A compile-fail example proves retained views block the next call.

### Exercise 3 — Coexisting views redesign

Change the requirement so two rows must coexist and redesign the API.

Completion standard: The chosen ownership or stable-source model permits coexistence without unsound lifetime widening.

### Exercise 4 — Owned boundary

Add a deliberate `to_owned` transition at the point retention begins.

Completion standard: Lifetimes do not spread into the storage and policy layers.

### Cross-course transfer

Choose one artifact from Courses 1–9 and reassess it through **GATs, Higher-Ranked Bounds, and Lending Interfaces**. Reconstruct its current invariant owner, then decide whether the quantifier-and-borrow map reveals a genuine defect. A justified no-change decision is valid when the advanced mechanism would add proof or compatibility cost without removing a real invalid state.


### Applied case study — a lending cursor and a retained index

A log reader stores one input buffer and exposes a cursor. `next` should lend a record view from the cursor's current mutable borrow; advancing may compact the buffer. A caller also wants to retain selected records for a later report. One design returns `&'input Record`; another returns an owned `Record` every time; a third uses a GAT family and an explicit `to_owned` escape hatch.

Draw the lifetime relationship for the GAT design and explain why the item lifetime must be chosen by each call. State the `where Self: 'a` requirement and what it communicates. Then analyze the reporting requirement: which selected data must become owned, at what boundary, and why retaining the borrowed item in a vector should fail.

Add a higher-ranked callback operation `with_next` that allows arbitrary callers to inspect one temporary view but not return it. Explain the quantifier represented by `for<'a>` and why choosing one long lifetime at the caller is weaker protection. Finish with one API simplification: identify a circumstance in which returning owned records is the better design despite the additional allocation.

## Part 4 — Independent laboratory

Build [Lending Table](../../labs/module-03-lending-table/README.md) from its `starter/` package.

Build a table cursor whose row view is tied to each mutable cursor borrow, then add an explicit owned escape for callers that need retention.

Before implementation, freeze Lending Table’s public behavior and the quantifier-and-borrow map. After implementation, complete its transfer task in a domain with different ownership, version, capacity, extension, or failure policy; renaming types does not demonstrate transfer.

## Part 5 — Capstone transfer

Implement and document AxiomStore’s `RecordCodec::View<'a>` and `LendingRecords::View<'a>` families. Add negative documentation showing that a record view cannot outlive the snapshot or coexist with a conflicting cursor advance.

Update AxiomStore’s quantifier-and-borrow map before code. Record the changed invariant owner, new failure paths, compatibility effect, and falsifying evidence. Then run the full capstone route because this module can invalidate guarantees outside its local file.

### Evidence quality review

Before leaving the module, identify the lifetime you first assigned to the producer, the borrow that actually chooses the view lifetime, and the exact retention boundary that forces ownership. Record one consumer for whom the lending interface is a poor fit. The reflection is complete only when you can explain both why the GAT is valid and when an owned iterator would be the more honest API.

## Part 6 — Reconstruct and defend

Read each lifetime quantifier in plain language, explain why source lifetime and method-borrow lifetime differ, and decide whether the lending protocol matches the consumer’s retention needs.

Finish without notes by reconstructing the quantifier-and-borrow map. Name the requirement, the simpler design, the decisive rejected construction, the state after failure, and the evidence that could falsify your claim. End by stating one condition under which this mechanism should be removed.

The defense is complete only when another reader can reproduce the reasoning behind Lending Table and the AxiomStore increment without seeing your final implementation.
