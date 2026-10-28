# Laboratory 9 — Async File Index

## Product and purpose

The file index is the first lab where completion order can differ from result order. It teaches promise ownership, explicit bounds, cancellation requests, contextual I/O errors, and deterministic reconstruction.

## Entry standard

Draw a promise-ownership graph for directory listing, per-entry stat operations, aggregate completion, cancellation checks, and final sorting. Predict the Module 9 cases before running the starter. The baseline proves one awaited filesystem operation; it does not own a batch of work or define deterministic completion semantics.

## Public contract

The operation lists one directory, rejects when entry count exceeds the bound, checks an optional signal before listing and before each stat starts, owns all stat promises through one `Promise.all`, omits nonregular entries, and sorts final records by filename. Any stat failure rejects with path context.

## Required construction sequence

Build the pure renderer first, then the async index. Use temporary directories for empty, files, subdirectory, and Unicode names. Test abort-before-start and bound rejection. Simulate or tolerate deletion between listing and stat as a contextual failure rather than a snapshot promise.

Keep the public surface small. Add private helpers only when they name a real step or invariant. Each exported function needs at least one success test and one boundary or failure test.

## Adversarial review

Test empty directories, Unicode names, subdirectories, entry counts at and above the bound, abort before listing, abort after listing but before later stats, deletion or permission failure between listing and stat, and deliberately scrambled completion timing. Every started promise must be observed; final records must follow the documented filename order rather than completion order.

## Prohibited shortcuts

Do not detach promises, use async `forEach`, sort by completion order, catch stat failures and silently omit files, or claim that checking AbortSignal rolls back completed operations. Do not start unbounded work before checking the entry limit.

A shortcut is prohibited because it destroys the reasoning target, not because the reference implementation uses a different style.

## Completion evidence

The laboratory is complete when all started promises have aggregate ownership, entry-count policy is checked before unbounded stat work, cancellation is described as a request rather than rollback, path failures retain context, and final order is independent of completion timing. Demonstrate these claims with temporary-directory and delayed-fake evidence before comparing with the reference.

## Independent transfer

Add a concurrency limit smaller than the entry bound. Preserve source-independent deterministic filename order and account for every started promise.

Define queue capacity, active-work limit, submission order, cancellation behavior, and terminal accounting before implementation. Use delayed operations to prove the active bound and stable final sort independently.


Document the snapshot boundary explicitly: the directory may change between listing and stat, and the product reports that race rather than pretending the result was atomic.
