# Laboratory 6 — Bounded NDJSON Decoder

**Module 46: Incremental Text Decoding, Framing, and Bounded Parsers**

## Product

Implement a byte-to-object Transform with fatal UTF-8 decoding, CRLF handling, exact physical line numbers, maximum line bytes, structured syntax errors, runtime object validation, and explicit final-line behavior.

This is an independent mechanism study. It deliberately excludes FlowLedger’s other stages so failures can be attributed to one contract.

## Governing question

> How do you turn arbitrary byte chunks into complete text records without corrupting split characters, accepting unbounded frames, or losing the physical location of malformed input?

## Public surface

- `decodeNdjson(source, options)` yields validated object records incrementally.

- Options define fatal UTF-8 behavior, maximum line bytes, and final-line policy.

- Errors identify physical line and trust phase.

## Required invariants

- Chunk partitioning does not change decoded records.

- Malformed UTF-8 is rejected rather than replaced when strict mode is selected.

- Pending line bytes never exceed the configured limit.

- CRLF is normalized without leaving a trailing carriage return.

- JSON arrays, primitives, and null do not pass an object-record validator.

## Implementation sequence

1. Build the incremental decoder and prove a split scalar.

2. Add line framing and pending-state accounting.

3. Implement CRLF and final-line policy.

4. Add JSON syntax errors with line context.

5. Add runtime object validation.

6. Generate chunk-partition tests and exact-limit cases.

Do not begin by reading the reference. The starter defines the vocabulary and a baseline, not the final design.

## Adversarial cases

- every split position of a multibyte character;

- delimiter split across chunks;

- empty lines and whitespace-only lines;

- a line exactly at the byte limit and one byte beyond;

- malformed UTF-8;

- malformed JSON after earlier valid records;

- valid JSON primitive or array;

- final line with and without newline;

Add cases in the smallest order that falsifies an incorrect model. Avoid arbitrary sleeps; use exact chunks, counters, injected callbacks, or explicit state transitions.

## Prohibited shortcuts

- decoding each chunk independently;

- measuring `string.length` as external byte length;

- collecting the whole file before parsing;

- checking the line limit only after finding a newline;

- casting `JSON.parse` output directly to the domain type;

A shortcut is prohibited because it removes the mechanism the laboratory exists to teach, not because one implementation style is preferred.

## Completion evidence

1. a chunk-partition property test;

2. physical line numbers for multiple failure phases;

3. exact-boundary tests for pending bytes;

4. a stated final-line and empty-line policy;

5. a transfer design for a length-prefixed text protocol;

## Independent transfer

Design a length-prefixed JSON protocol. State how prefix size, payload size, UTF-8 validity, JSON grammar, schema validation, and EOF truncation are reported separately.

Your transfer design must reconstruct the module ledger for the new domain. Renaming the laboratory types is not transfer.

## Chunk-partition matrix

Choose one canonical UTF-8 input containing ASCII, a multibyte character, an empty final line policy case, and two complete records. Generate partitions that split before and after every byte. Each partition must produce the same records, source-line numbers, and canonical diagnostics as the one-chunk input. This test separates framing semantics from transport chunking.

Add a line whose encoded byte length is exactly the limit and another one byte larger. Explain whether the bound applies to encoded bytes, decoded code units, or characters, and enforce only the declared unit. The decoder must reject before retaining an unbounded partial line. For malformed JSON, report the physical record position without echoing an arbitrarily large source line. Finally, trace decoder state across `write`, delimiter discovery, final flush, and error. The trace should make clear which bytes are undecoded, which text is decoded but unframed, and which complete record has been handed to JSON validation.

## Comparing with the reference

After your tests pass, inspect `reference/` and locate the first meaningful difference. Adopt it only when it proves an invariant your design misses; otherwise retain the simpler design.
