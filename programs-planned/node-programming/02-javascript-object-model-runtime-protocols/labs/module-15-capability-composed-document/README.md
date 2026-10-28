# Laboratory 15 — Capability-Composed Document

## Product

Build a document application from narrow capabilities rather than a deep class hierarchy or a broad environment object. The product loads text, applies tag and version operations, renders a result, and saves a plain snapshot.

## Authority model

- the store can load and save document records;
- the clock can produce one timestamp when a version is committed;
- the renderer can turn a read view into text;
- the document core owns title, text, tags, and version history;
- the application service owns operation order and error propagation.

No collaborator receives the whole application. No import performs global registration. Tests must replace each effect independently and record exact call order.

## Required design work

1. Define the smallest interfaces that support the product.
2. Keep domain transformations ordinary pure functions where identity is unnecessary.
3. Use a closure or class private state for the document core and expose a narrow read view.
4. Decide whether tag behavior is forwarding, nested composition, or a mixin; explain the chosen conflict policy.
5. Save only after a complete candidate version exists.
6. Keep rendering outside persistence.

## Invariants

- titles and tags are normalized;
- tags are unique and deterministically ordered;
- committing a version asks the clock exactly once;
- failed save does not produce a success result;
- the store never receives the live core object;
- the renderer cannot mutate the document;
- replacing the renderer does not require changing storage or domain code.

## Prohibited shortcuts

Do not create `class SearchableTaggableVersionedPersistentDocument extends ...`. Do not pass `{store, clock, renderer, logger, config, process}` as one environment bag. Do not let the store call the renderer. Do not expose mutable arrays.

## Transfer

Add an audit capability that observes committed version summaries but cannot read document text. Explain how its least-authority boundary differs from a logger receiving the whole document.
