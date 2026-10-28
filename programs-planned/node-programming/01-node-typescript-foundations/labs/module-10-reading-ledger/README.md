# Laboratory 10 — Reading Ledger

## Product and purpose

Reading Ledger is the independent transfer product. It reuses the reasoning method but has different states and fields, so copying StudyLedger and renaming identifiers would miss the learning objective.

## Entry standard

Write an architecture map for the new product before reading any StudyLedger source: tokens, domain states, decoder, storage, application order, rendering, and process boundary. Reconstruct the Course 1 reasoning tables and predict Module 10 cases. The starter supplies a small domain seed only; copying the capstone structure without deriving these authorities does not satisfy the lab.

## Public contract

Books progress queued → reading → finished, or queued/reading → dropped. Finished books alone have pages; dropped books have a reason; IDs are positive and monotonic. The V1 document is versioned and deterministic. Missing file, invalid JSON, invalid schema, and I/O failure remain distinct.

## Required construction sequence

Begin with the union and pure transitions, then queries and summary, then unknown-data decoding, then async repository functions. Add unit, codec, and temporary-filesystem tests. Preserve older ledger values and check illegal transitions. The starter deliberately supplies only a small baseline.

Keep the public surface small. Add private helpers only when they name a real step or invariant. Each exported function needs at least one success test and one boundary or failure test.

## Adversarial review

Exercise duplicate IDs, invalid next ID, malformed state-specific fields, illegal transitions, missing initial file, malformed existing file, permission failure, save rejection, deterministic re-encoding, and aliases to previous ledger values. A mutating command must not report success before persistence, and a failed load or save must not be converted into plausible empty state.

## Prohibited shortcuts

Do not reuse StudyLedger field shapes mechanically, make pages optional on every state, cast JSON, catch every load failure as empty, mutate prior ledgers, or report save success before the promise fulfills.

A shortcut is prohibited because it destroys the reasoning target, not because the reference implementation uses a different style.

## Completion evidence

The laboratory is complete when the new product has its own legal-state model, strict V1 decoder, candidate loading, immutable transitions, deterministic queries and encoding, awaited persistence, and unit/codec/filesystem evidence. Provide an architecture and claim map showing where it differs from StudyLedger; similarity of filenames is not evidence of independent design.

## Independent transfer

Add ratings 1–5 only for finished books. Decide whether V1 can add the field compatibly under the existing strict unknown-key policy; if not, design V2 and an explicit migration.

Write a compatibility decision before changing the model. If V2 is required, define accepted V1/V2 inputs, canonical output, migration authority, unknown-key behavior, and fixtures that prove ratings never appear on unfinished books.
